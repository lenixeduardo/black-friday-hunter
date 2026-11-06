"""No emoji glyphs: every interface icon uses an original standalone SVG asset."""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "app" / "index.html"
ICONS = ROOT / "app" / "assets" / "icons"
EXPECTED = {
    "points-medallion.svg",
    "rewards-parcel.svg",
    "alert-message.svg",
    "notification-bell.svg",
    "discount-tag.svg",
    "verified-badge.svg",
    "search-lens.svg",
    "tcg-cards.svg",
    "mail-envelope.svg",
    "benefits-spark.svg",
}
EMOJI = re.compile(r"[\u2600-\u27BF\U0001F300-\U0001FAFF]")


def test_no_emoji_in_home_css_or_custom_assets():
    html = HTML.read_text(encoding="utf-8")
    css = (ROOT / "app" / "css" / "brand-icon-assets-v7.css").read_text(encoding="utf-8")
    for path, source in ((HTML, html), ("V7 CSS", css)):
        assert EMOJI.search(source) is None, f"Emoji-looking character found in {path}"
        assert "font-family:emoji" not in source.lower()
        assert "content:'✓'" not in source
    for path in ICONS.glob("*.svg"):
        assert EMOJI.search(path.read_text(encoding="utf-8")) is None, path


def test_every_asset_is_independent_valid_vector_svg():
    assert {p.name for p in ICONS.glob("*.svg")} == EXPECTED
    for file in ICONS.glob("*.svg"):
        root = ET.parse(file).getroot()
        assert root.tag == "{http://www.w3.org/2000/svg}svg"
        assert root.attrib["viewBox"] == "0 0 64 64"
        assert root.attrib.get("fill") == "none"
        assert not list(root.iter("{http://www.w3.org/2000/svg}image"))
        assert 'href="http' not in file.read_text(encoding="utf-8")
        assert "href=" not in file.read_text(encoding="utf-8")


def test_every_used_custom_icon_is_a_local_asset_with_accessible_semantics():
    doc = BeautifulSoup(HTML.read_text(encoding="utf-8"), "html.parser")
    icons = doc.select("img.asset-icon")
    assert len(icons) >= 20, len(icons)
    for img in icons:
        assert img["src"].startswith("/app/assets/icons/")
        assert (ROOT / img["src"].lstrip("/")).is_file()
        assert img.get("alt") == ""
        if img.get("aria-hidden") is not None:
            assert img.get("aria-hidden") == "true"
        assert int(img["width"]) >= 17 and int(img["height"]) >= 17
    assert "✓" not in str(doc)
    assert "★" not in str(doc)
    assert "url('/app/assets/icons/verified-badge.svg')" in (
        ROOT / "app" / "css" / "brand-icon-assets-v7.css").read_text(encoding="utf-8")


def test_icon_pwa_cache_and_brand_unchanged():
    sw = (ROOT / "app" / "sw.js").read_text(encoding="utf-8")
    for name in EXPECTED:
        assert "/app/assets/icons/" + name in sw
    assert "bfh-shell-v7" in sw
    html = HTML.read_text(encoding="utf-8")
    for required in ("logo-v4.webp","magikarp-scooter.webp","banner-tcg.webp","fidelity-v5.css","brand-icon-assets-v7.css"):
        assert required in html
    assert 'id="ofertas" hidden' in html
