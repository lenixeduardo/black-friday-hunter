from pathlib import Path
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]
APP=(ROOT/"app/index.html").read_text(encoding="utf-8")
MANIFEST=json.loads((ROOT/"app/manifest.webmanifest").read_text(encoding="utf-8"))

class StaticTests(unittest.TestCase):
    def test_visual_identity(self):
        self.assertIn("BLACK",APP)
        self.assertIn("FRIDAY",APP)
        self.assertIn("Economize mais.",APP)
    def test_menu(self):
        self.assertIn('id="menu"',APP)
        self.assertIn('id="drawer"',APP)
        self.assertIn("aria-expanded",APP)
    def test_categories(self):
        for s in ("TCG","Mini Booster Box","Boosters avulsos","Cartas Pokémon","Booster Box"):
            self.assertIn(s,APP)
    def test_no_fake_prices(self):
        self.assertNotIn("R$ 289,90",APP)
        self.assertIn("Aguardando ofertas verificadas",APP)
    def test_reduced_motion(self):
        self.assertIn("prefers-reduced-motion",APP)
    def test_pwa_manifest(self):
        self.assertEqual(MANIFEST["start_url"],"/app/")
        self.assertEqual(MANIFEST["display"],"standalone")
    def test_official_api_not_faked(self):
        self.assertIn("ainda não configurada",APP)
        self.assertIn("0 pontos",APP)

if __name__=="__main__":
    unittest.main()