"""Affiliate card CTAs must be readable, emoji-free and route honestly."""
from pathlib import Path
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]


def test_static_affiliate_buttons_are_compact_and_disclose_list_destination():
    html=(ROOT/"app/index.html").read_text(encoding="utf-8")
    page=BeautifulSoup(html,"html.parser")
    links=page.select("#amazon-grid .amazon-item a.amazon-list-link")
    assert len(links)==9
    for a in links:
        assert a.get("href")=="https://amzn.to/4846Sow"
        assert set(("noopener","noreferrer","sponsored")).issubset(set(a.get("rel") or []))
        assert a.get_text(" ",strip=True)=="Ver lista Amazon"
        assert "afiliado" in a.get("aria-label","").lower()
        icon=a.select_one("img.affiliate-cta-icon")
        assert icon is not None
        assert icon.get("src")=="/app/assets/icons/external-link.svg"
        assert icon.get("aria-hidden")=="true"
    assert 'affiliate-cta-v8.css' in html


def test_dynamic_affiliate_buttons_have_no_orphan_unicode_arrow():
    ui=(ROOT/"app/js/amazon-catalog-ui.mjs").read_text(encoding="utf-8")
    assert "'Ver lista Amazon'" in ui
    assert "affiliate-cta-icon" in ui
    assert "/app/assets/icons/external-link.svg" in ui
    assert "Ver na lista de afiliado ↗" not in ui
    assert "↗" not in ui
    assert "Ver produto Amazon" in ui


def test_affiliate_button_contrast_and_cache():
    css=(ROOT/"app/css/affiliate-cta-v8.css").read_text(encoding="utf-8")
    assert "min-height:48px" in css
    assert "white-space:nowrap" in css
    assert "background:#17171D" in css and "color:#FFFFFF" in css
    sw=(ROOT/"app/sw.js").read_text(encoding="utf-8")
    assert "bfh-shell-v9" in sw
    assert "/app/css/affiliate-cta-v8.css" in sw
    assert "/app/assets/icons/external-link.svg" in sw
