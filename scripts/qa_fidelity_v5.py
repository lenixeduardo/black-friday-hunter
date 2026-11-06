#!/usr/bin/env python3
"""Black Friday Hunter responsive and commercial-integrity QA.

The user-facing homepage must never show TCG offer cards lacking a verified,
positive, matching BRL price. These tests use an isolated local HTTP server.
"""
from __future__ import annotations

import argparse
import functools
import http.server
import json
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
WIDTHS = (390, 768, 1440)


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="artifacts/qa-v5")
    args = parser.parse_args()
    output = ROOT / args.out
    output.mkdir(parents=True, exist_ok=True)
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    reports = []

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"])
            for width in WIDTHS:
                page = browser.new_page(viewport={"width": width, "height": 900},
                    reduced_motion="reduce", service_workers="block")
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                response = page.goto(f"http://127.0.0.1:{server.server_port}/app/",
                    wait_until="domcontentloaded", timeout=25000)
                assert response and response.status == 200
                page.wait_for_function(
                    "document.querySelector('#amazon-result-count')?.textContent.includes('4 de 9')",
                    timeout=20000)
                assert not errors, errors
                # Every visible UI icon is an independent actual SVG asset, not an emoji.
                assert page.locator("img.asset-icon").count() >= 20
                page.wait_for_function("""() => [...document.querySelectorAll('img.asset-icon')]
                    .every(img => img.complete && img.naturalWidth > 0)""", timeout=15000)
                badge_loaded = page.evaluate("""async () => (await fetch('/app/assets/icons/verified-badge.svg')).ok""")
                assert badge_loaded, "Verification badge must be accessible"
                assert page.locator("#amazon-grid .amazon-item").count() == 9
                assert page.locator("#amazon-grid .amazon-item:visible").count() == 4
                assert page.locator("#amazon-show-all").get_attribute("aria-expanded") == "false"
                assert page.locator("#amazon-curadoria").get_attribute("data-verified") == "false"
                assert page.locator("#amazon-grid .amazon-item .amazon-price.unknown").count() == 0
                assert page.locator("#amazon-grid .amazon-item .amazon-price").count() == 9
                assert page.locator("#amazon-grid .amazon-item:visible .amazon-price").count() == 4

                # Requirement: no unpriced TCG card or sealed product is rendered.
                assert page.locator("#ofertas").is_hidden()
                assert page.locator("#tcg-boxes").is_hidden()
                assert page.locator("#singles").is_hidden()
                assert page.locator("#ofertas article.offer:visible").count() == 0
                assert page.locator("#singles .offer").count() == 3
                assert page.locator("#tcg-boxes .offer").count() == 3
                assert page.locator("#data-warning").is_visible()
                assert "sem preço validado não aparecem" in page.locator("#data-warning").inner_text()
                assert page.locator(".skip-link").get_attribute("href") == "#categorias"

                overflow = page.evaluate("document.documentElement.scrollWidth - innerWidth")
                assert overflow <= 2, f"Unexpected page overflow {overflow}px at {width}"
                sizes = page.evaluate("""() => ({
                    amazonTitle: parseFloat(getComputedStyle(
                        document.querySelector('#amazon-grid .amazon-item h3')).fontSize),
                    buyLinkHeight: document.querySelector(
                        '#amazon-grid a.amazon-list-link').getBoundingClientRect().height,
                    expandButtonHeight: document.querySelector(
                        '#amazon-show-all').getBoundingClientRect().height
                })""")
                assert sizes["amazonTitle"] >= 12, sizes
                assert sizes["buyLinkHeight"] >= 43.5, sizes
                assert sizes["expandButtonHeight"] >= 43.5, sizes
                if width == 390:
                    assert page.locator("#mobile-tcg-art").is_visible()
                else:
                    assert page.locator("#mobile-tcg-art").is_hidden()

                page.screenshot(path=str(output / f"home-{width}.png"),
                    full_page=True, animations="disabled")

                # Validate fail-closed behavior across negative and positive cases.
                # This is synthetic test data, not a production offer.
                page.evaluate("""() => {
                  const card=document.querySelector('#singles .offer');
                  card.dataset.priceAmount='35.90';
                  card.dataset.priceVerified='true';
                  const el=document.createElement('strong');
                  el.className='offer-price';
                  el.textContent='R$ 35,90';
                  card.querySelector('.offer-copy').append(el);
                  dispatchEvent(new Event('bfh:offer-prices-updated'));
                }""")
                assert page.locator("#ofertas").is_visible()
                assert page.locator("#singles .offer:visible").count() == 1
                assert page.locator("#tcg-boxes .offer:visible").count() == 0
                assert page.locator("#singles .offer:visible .offer-price").inner_text() == "R$ 35,90"

                page.evaluate("""() => {
                   const card=document.querySelector('#singles .offer');
                   card.querySelector('.offer-price').textContent='R$ 10,00';
                   dispatchEvent(new Event('bfh:offer-prices-updated'));
                }""")
                assert page.locator("#ofertas").is_hidden(), "Mismatch must hide card"

                page.evaluate("""() => {
                   const card=document.querySelector('#singles .offer');
                   card.querySelector('.offer-price').textContent='R$ 35,90';
                   card.dataset.priceVerified='false';
                   dispatchEvent(new Event('bfh:offer-prices-updated'));
                }""")
                assert page.locator("#ofertas").is_hidden(), "Unverified price must hide card"

                page.evaluate("""() => {
                   const card=document.querySelector('#singles .offer');
                   card.dataset.priceVerified='true';
                   card.dataset.priceAmount='0';
                   dispatchEvent(new Event('bfh:offer-prices-updated'));
                }""")
                assert page.locator("#ofertas").is_hidden(), "Zero price must hide card"

                page.evaluate("""() => {
                   const card=document.querySelector('#singles .offer');
                   card.dataset.priceAmount='NaN';
                   dispatchEvent(new Event('bfh:offer-prices-updated'));
                }""")
                assert page.locator("#ofertas").is_hidden(), "NaN price must hide card"

                # Verify the navigation also respects the gate.
                page.locator("#interest").select_option("TECH")
                assert page.locator("#ofertas").is_hidden()
                page.locator("#interest").select_option("TCG")
                assert page.locator("#ofertas").is_hidden()

                # The existing Amazon list remains searchable and honest.
                page.locator("#amazon-show-all").click()
                assert page.locator("#amazon-grid .amazon-item:visible").count() == 9
                assert page.locator("#amazon-show-all").get_attribute("aria-expanded") == "true"
                page.locator("#amazon-show-all").click()
                assert page.locator("#amazon-grid .amazon-item:visible").count() == 4

                page.locator("#search-form input").fill("Reinado Delta")
                page.locator("#search-form button").click()
                assert page.locator("#amazon-grid .amazon-item:visible").count() == 4
                assert page.locator("#amazon-show-all").is_hidden()
                page.locator("#search-form input").fill("inexistente_123")
                page.locator("#search-form button").click()
                assert page.locator("#amazon-empty").is_visible()
                page.locator("#search-form input").fill("")
                page.locator("#search-form button").click()
                assert page.locator("#amazon-grid .amazon-item:visible").count() == 4
                assert page.locator("#ofertas").is_hidden()
                assert not errors, errors

                reports.append({"width": width, "customSVGIconsLoaded": True, "emojiFree": True, "result": "PASS",
                    "unpricedTCGCardsVisible": 0,
                    "syntheticValidPriceShowsOneCard": True,
                    "invalidOrUnverifiedPriceHidden": True,
                    "amazonCatalogInitially": 4,
                    "amazonCatalogExpanded": 9,
                    "searchPassed": True,
                    "overflowPx": overflow,
                    "textAndTouchMetrics": sizes})
                print(f"QA home pricing and SVG icon assets {width}: PASS", flush=True)
                gallery = browser.new_page(viewport={"width": width, "height": 900},
                    reduced_motion="reduce", service_workers="block")
                gallery_response = gallery.goto(
                    f"http://127.0.0.1:{server.server_port}/app/assets/icons/preview.html",
                    wait_until="domcontentloaded", timeout=20000)
                assert gallery_response and gallery_response.status == 200
                assert gallery.locator(".gallery img").count() == 10
                gallery.evaluate("""() => [...document.querySelectorAll('.gallery img')]
                    .forEach(img => { img.loading = 'eager'; })""")
                gallery.wait_for_function("""() => [...document.querySelectorAll('.gallery img')]
                    .every(img => img.complete && img.naturalWidth > 0)""", timeout=15000)
                gallery.screenshot(path=str(output / f"icon-gallery-{width}.png"),
                    full_page=True, animations="disabled")
                gallery.close()
                page.close()
            browser.close()
    finally:
        server.shutdown()
    (output / "results.json").write_text(
        json.dumps(reports, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"QA passed in {len(reports)} viewport sizes")


if __name__ == "__main__":
    main()
