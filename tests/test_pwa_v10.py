"""PWA installability, offline safety, icon fidelity, and service worker contract."""
from __future__ import annotations
import json
import re
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
APP=ROOT/"app"

def test_pwa_metadata_installability():
    manifest=json.loads((APP/"manifest.webmanifest").read_text("utf-8"))
    assert manifest["name"]=="Black Friday Hunter"
    assert manifest["id"]=="/app/"
    assert manifest["start_url"]=="/app/"
    assert manifest["scope"]=="/app/"
    assert manifest["lang"]=="pt-BR"
    assert manifest["display"]=="standalone"
    assert manifest["theme_color"].lower()=="#ffffff"
    assert len(manifest["shortcuts"])>=2
    for shortcut in manifest["shortcuts"]:
        assert shortcut["url"].startswith("/app/#")
    by_purpose={}
    for icon in manifest["icons"]:
        by_purpose.setdefault(icon["purpose"],set()).add(icon["sizes"])
        path=ROOT/icon["src"].lstrip("/")
        assert path.is_file(), path
        with Image.open(path) as im:
            n=int(icon["sizes"].split("x")[0])
            assert im.size==(n,n)
            assert im.mode in ("RGB","RGBA")
    assert {"192x192","512x512"}<=by_purpose["any"]
    assert {"192x192","512x512"}<=by_purpose["maskable"]
    with Image.open(APP/"apple-touch-icon.png") as touch:
        assert touch.size==(180,180)

def test_approved_brand_and_iphone_install_meta():
    home=(APP/"index.html").read_text("utf-8")
    for needed in ('apple-mobile-web-app-capable','apple-mobile-web-app-title',
                   'apple-touch-icon.png','pwa-install','pwa-install-guide',
                   'pwa-update-banner','pwa-offline-bar','pwa-client.js',
                   'hero hero-v9','magikarp-scooter.webp'):
        assert needed in home
    assert 'bfh-shell-v10' not in home
    assert 'Faltam para a Black Friday' not in home
    assert not any(ch in home for ch in ("★","✓"))
    assert 'id="ofertas" hidden' in home

def test_service_worker_public_scope_and_offline_precache():
    worker=(APP/"sw.js").read_text("utf-8")
    assert "bfh-shell-v10" in worker
    assert "function cacheable(url)" in worker
    assert "!cacheable(url)" in worker
    assert "url.pathname.startsWith('/app/assets/')" in worker
    assert "event.data.type==='SKIP_WAITING'" in worker
    assert "self.clients.claim()" in worker
    assert "cache.addAll(PRECACHE)" in worker
    assert "request.mode==='navigate'" in worker
    assert "url.origin!==self.location.origin" in worker
    assert "'/api/'" not in worker
    for path in ("offline.html","pwa-client.js","amazon-catalog.mjs",
                 "amazon-catalog-ui.mjs","curadoria.json","icon-maskable-192.png",
                 "icon-maskable-512.png","apple-touch-icon.png"):
        assert path in worker
    offline=(APP/"offline.html").read_text("utf-8")
    assert "Você está sem conexão" in offline
    assert "preços devem ser conferidos" in offline
    assert "Black Friday Hunter" in offline

def test_pwa_installation_never_requests_notification_permission():
    client=(APP/"js/pwa-client.js").read_text("utf-8")
    assert "beforeinstallprompt" in client
    assert "appinstalled" in client
    assert "registration.waiting.postMessage" in client
    assert "controllerchange" in client
    assert "Adicionar à Tela de Início" in client
    assert "navigator.onLine" in client
    assert "Notification.requestPermission" not in client
    assert "PushManager" not in client
    assert "window.location.href=" not in client
