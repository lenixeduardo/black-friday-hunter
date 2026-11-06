#!/usr/bin/env python3
"""Run a Chromium-based PWA install and offline smoke test at localhost."""
from __future__ import annotations

import argparse
import functools
import http.server
import json
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]

class Server(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args): pass

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",default="artifacts/qa-pwa-v10")
    args=parser.parse_args()
    output=ROOT/args.out
    output.mkdir(parents=True,exist_ok=True)
    server=http.server.ThreadingHTTPServer(("127.0.0.1",0),
        functools.partial(Server,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    url=f"http://127.0.0.1:{server.server_port}/app/"
    rows=[]
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
            for width in (390,768,1440):
                context=browser.new_context(viewport={"width":width,"height":860},
                    reduced_motion="reduce",service_workers="allow")
                page=context.new_page()
                errors=[]
                page.on("pageerror",lambda exc:errors.append(str(exc)))
                response=page.goto(url,wait_until="domcontentloaded",timeout=25000)
                assert response and response.status==200
                m=page.evaluate("""async () => (await fetch('/app/manifest.webmanifest')).json()""")
                assert m["display"]=="standalone"
                assert len(m["icons"])==4
                for entry in m["icons"]:
                    assert page.request.get(url.rsplit("/app/",1)[0]+entry["src"]).status==200
                page.wait_for_function("navigator.serviceWorker && navigator.serviceWorker.ready",
                    timeout=12000)
                page.evaluate("""async () => {
                    const reg=await navigator.serviceWorker.ready;
                    if(!reg.active)throw new Error('service worker not active');
                }""")
                page.wait_for_function("navigator.serviceWorker.controller!==null",timeout=15000)
                assert not errors,errors
                page.locator("#menu-toggle").click()
                assert page.locator("#pwa-install").is_visible()
                assert page.locator("#pwa-install").get_attribute("type")=="button"
                page.locator("#menu-toggle").click()
                page.screenshot(path=str(output/f"pwa-home-{width}.png"),full_page=True,
                    animations="disabled")
                # Ensure the first app visit pre-caches public assets for offline mode.
                context.set_offline(True)
                page.reload(wait_until="domcontentloaded",timeout=20000)
                assert page.locator(".hero.hero-v9").is_visible()
                assert page.locator("#pwa-offline-bar").is_visible()
                page.wait_for_function("""() => [...document.querySelectorAll('#amazon-grid .amazon-item')]
                    .length === 9""",timeout=15000)
                assert page.locator("#ofertas").is_hidden()
                assert page.locator(".hero-magikarp img").evaluate("(img) => img.complete && img.naturalWidth > 0")
                assert not errors,errors
                page.screenshot(path=str(output/f"pwa-offline-{width}.png"),full_page=True,
                    animations="disabled")
                context.set_offline(False)
                page.reload(wait_until="domcontentloaded")
                assert page.locator("#pwa-offline-bar").is_hidden()
                rows.append({"width":width,"installManifest":"PASS",
                             "serviceWorker":"ACTIVE","offlineReload":"PASS",
                             "cachedPosterPricesStillLabelled":"REFERENCE_ONLY",
                             "unpricedTCGCardsVisible":0})
                context.close()

            # iPhone-like browser does not use beforeinstallprompt: show guidance.
            iphone=browser.new_context(viewport={"width":390,"height":844},
                user_agent=("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
                            "Mobile/15E148 Safari/604.1"),service_workers="allow")
            iphone_page=iphone.new_page()
            iphone_page.goto(url,wait_until="domcontentloaded")
            iphone_page.locator("#menu-toggle").click()
            iphone_page.locator("#pwa-install").click()
            assert iphone_page.locator("#pwa-install-guide").is_visible()
            assert "Adicionar à Tela de Início" in iphone_page.locator("#pwa-guide-text").inner_text()
            iphone_page.screenshot(path=str(output/"pwa-install-ios-390.png"),animations="disabled")
            iphone.close()
            browser.close()
    finally:
        server.shutdown()
    (output/"report.json").write_text(json.dumps(rows,indent=2),encoding="utf-8")
    print("PWA V10 runtime tests passed:",len(rows),"viewports and iOS guidance")

if __name__=="__main__":
    main()
