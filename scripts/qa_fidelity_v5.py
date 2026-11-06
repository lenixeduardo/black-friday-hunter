#!/usr/bin/env python3
"""Visual/interaction QA for the audited Black Friday Hunter V5 layout.

Serves the actual checkout-free static source locally. Screenshots are
evidence of this branch's source, not production-browser captures.
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
WIDTHS = [390, 768, 1440]


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
    url = f"http://127.0.0.1:{server.server_port}/app/"
    reports = []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
            for width in WIDTHS:
                page = browser.new_page(viewport={"width": width, "height": 900},
                    reduced_motion="reduce", service_workers="block")
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                response = page.goto(url, wait_until="domcontentloaded", timeout=25000)
                assert response and response.status == 200, f"HTML HTTP {response.status if response else 'none'}"
                page.wait_for_function(
                    "document.querySelector('#amazon-result-count')?.textContent.includes('4 de 10')",
                    timeout=20000
                )
                assert not errors, errors
                assert page.locator("#amazon-grid .amazon-item").count() == 10
                assert page.locator("#amazon-grid .amazon-item:visible").count() == 4
                assert page.locator("#amazon-show-all").get_attribute("aria-expanded") == "false"
                assert page.locator("#amazon-curadoria").get_attribute("data-verified") == "false"
                assert page.locator("#tcg-boxes img").count() == 3
                assert page.locator("#singles img").count() == 3
                # Trigger offscreen lazy images before asserting their actual load state.
                page.evaluate("""() => [...document.querySelectorAll('#tcg-boxes img, #singles img')]
                    .forEach(img => { img.loading = 'eager'; })""")
                page.wait_for_function("""() => [...document.querySelectorAll('#tcg-boxes img, #singles img')]
                    .every(img => img.complete && img.naturalWidth > 0)""", timeout=15000)
                # Wait for async PNG/WebP decoding, not just the network load.
                page.evaluate("""async () => {
                    await Promise.all([...document.querySelectorAll('#tcg-boxes img, #singles img')]
                        .map(img => img.decode()));
                }""")
                images_loaded = True
                overflow = page.evaluate("document.documentElement.scrollWidth - innerWidth")
                assert overflow <= 2, f"Horizontal page overflow: {overflow} at {width}"
                sizes = page.evaluate("""() => {
                  const px = selector => Number.parseFloat(getComputedStyle(document.querySelector(selector)).fontSize);
                  return {
                    offerTitle: px('#singles .offer h3'),
                    offerMeta: px('#singles .offer small'),
                    amazonTitle: px('#amazon-grid .amazon-item h3'),
                    cardButton: document.querySelector('#amazon-grid a.amazon-list-link').getBoundingClientRect().height,
                    sectionButton: document.querySelector('#singles .section-heading button').getBoundingClientRect().height,
                    expandButton: document.querySelector('#amazon-show-all').getBoundingClientRect().height
                  };
                }""")
                assert sizes["offerTitle"] >= 14, sizes
                assert sizes["offerMeta"] >= 12, sizes
                assert sizes["amazonTitle"] >= 12, sizes
                assert all(sizes[k] >= 43.5 for k in ("cardButton", "sectionButton", "expandButton")), sizes
                if width == 390:
                    stats = page.locator("#singles .offers").evaluate(
                        "(el) => ({sw:el.scrollWidth,cw:el.clientWidth,tabindex:el.getAttribute('tabindex')})"
                    )
                    assert stats["sw"] > stats["cw"] + 100, stats
                    assert stats["tabindex"] == "0", stats
                    assert page.locator("#mobile-tcg-art").is_visible()
                    page.locator("#singles .offers").focus()
                    before = page.locator("#singles .offers").evaluate("(el) => el.scrollLeft")
                    page.keyboard.press("ArrowRight")
                    after = page.locator("#singles .offers").evaluate("(el) => el.scrollLeft")
                    assert after >= before, (before, after)
                else:
                    assert page.locator("#mobile-tcg-art").is_hidden()

                # Avoid transient keyboard focus rings in full-page visual evidence.
                page.evaluate("""() => {
                    document.activeElement?.blur();
                    for (const rail of document.querySelectorAll('.offers')) rail.scrollLeft = 0;
                    window.scrollTo(0,0);
                }""")
                page.wait_for_timeout(250)
                page.screenshot(path=str(output / f"home-{width}.png"), full_page=True,
                    animations="disabled", timeout=45000)
                page.locator("#singles").scroll_into_view_if_needed()
                page.screenshot(path=str(output / f"cards-{width}.png"), animations="disabled")

                page.locator("#amazon-show-all").click()
                assert page.locator("#amazon-grid .amazon-item:visible").count() == 10
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
                assert not errors, errors
                reports.append({"width": width, "outcome": "PASS", "overflowPx": overflow,
                    "touchAndText": sizes, "allSixReferenceImagesLoaded": images_loaded,
                    "catalogVisibleInitially": 4, "catalogVisibleExpanded": 10,
                    "categoryCardCount": 6, "searchPassed": True})
                print(f"QA V5 {width}: PASS", flush=True)
                page.close()
            browser.close()
    finally:
        server.shutdown()
    (output / "results.json").write_text(json.dumps(reports, ensure_ascii=False, indent=2), encoding="utf-8")
    print("QA visual V5: PASS —", len(reports), "viewports; evidence:", output)


if __name__ == "__main__":
    main()
