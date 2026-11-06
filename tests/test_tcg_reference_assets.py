"""Contract tests for the three authentic TCG category reference assets."""
from __future__ import annotations

import json
import struct
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = {
    "01-vintage-squirtle-base1-63.png": ("Squirtle 63/102", "Vintage"),
    "02-illustration-rare-pikachu-173.png": ("Pikachu 173/165", "Illustration Rare"),
    "03-double-rare-charizard-ex-006.png": ("Charizard ex 006/165", "Double Rare"),
}


class Images(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            self.tags.append(dict(attrs))


class TestTCGCategoryAssets(unittest.TestCase):
    def setUp(self):
        self.assets = ROOT / "app" / "assets" / "tcg"
        self.html = (ROOT / "app" / "index.html").read_text(encoding="utf-8")
        self.manifest = json.loads((self.assets / "manifest.json").read_text(encoding="utf-8"))

    def test_3_authentic_reference_files_exist_with_rgba(self):
        for filename in CARDS:
            with self.subTest(file=filename):
                path = self.assets / filename
                self.assertTrue(path.is_file(), str(path))
                with path.open("rb") as f:
                    self.assertEqual(f.read(8), b"\x89PNG\r\n\x1a\n")
                    self.assertEqual(struct.unpack(">I", f.read(4))[0], 13)
                    self.assertEqual(f.read(4), b"IHDR")
                    width, height, depth, color_type = struct.unpack(">IIBB", f.read(10))
                    self.assertEqual((width, height), (1056, 1472))
                    self.assertEqual((depth, color_type), (8, 6))  # RGBA

    def test_correct_category_assets_are_rendered(self):
        parsed = Images()
        parsed.feed(self.html)
        for filename, (card, category) in CARDS.items():
            with self.subTest(category=category):
                url = "/app/assets/tcg/" + filename
                matches = [tag for tag in parsed.tags if tag.get("src") == url]
                self.assertEqual(len(matches), 1)
                self.assertIn(card.split()[0], matches[0].get("alt", ""))
                self.assertEqual(matches[0].get("loading"), "lazy")

    def test_original_sources_and_rights_are_recorded(self):
        self.assertFalse(self.manifest.get("commercial_reuse_authorized"))
        self.assertEqual(len(self.manifest["assets"]), 3)
        for asset in self.manifest["assets"]:
            self.assertTrue(asset["source_url"].startswith("https://images.pokemontcg.io/"))
            self.assertFalse(asset["commercial_reuse_authorized"])
            self.assertTrue(asset["source_sha256"])

    def test_old_generic_placeholders_removed_from_singles(self):
        singles = self.html.split('id="singles"', 1)[1].split('id="data-warning"', 1)[0]
        self.assertEqual(singles.count('class="offer-art real-card"'), 3)
        for old in ("Ilustração genérica de carta", "class=\"symbol\">F", "class=\"symbol\">V"):
            self.assertNotIn(old, singles)


if __name__ == "__main__":
    unittest.main()
