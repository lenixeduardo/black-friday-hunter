"""Legacy structural regression checks adapted to the approved V4 assets."""
from pathlib import Path
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]
APP=(ROOT/'app/index.html').read_text(encoding='utf-8')
MANIFEST=json.loads((ROOT/'app/manifest.webmanifest').read_text(encoding='utf-8'))

class StaticTests(unittest.TestCase):
    def test_visual_identity(self):
        for text in ('Black Friday Hunter','logo-v4.webp','magikarp-scooter.webp','banner-tcg.webp','Economize mais.'):
            self.assertIn(text,APP)
    def test_menu(self):
        for text in ('id="menu-toggle"','id="drawer"','aria-expanded','setMenu('):
            self.assertIn(text,APP)
    def test_categories(self):
        for text in ('TCG','Mini BB / boosters','Booster boxes','Cartas avulsas','ETBs especiais'):
            self.assertIn(text,APP)
    def test_no_fake_prices(self):
        self.assertNotIn('R$ 289,90',APP)
        self.assertNotIn('2.780',APP)
        self.assertIn('Sem preço validado',APP)
        self.assertIn('Sem oferta validada',APP)
    def test_reduced_motion(self):
        self.assertIn('prefers-reduced-motion:reduce',APP)
    def test_pwa_manifest(self):
        self.assertEqual(MANIFEST['start_url'],'/app/')
        self.assertEqual(MANIFEST['display'],'standalone')
    def test_official_api_not_faked(self):
        self.assertIn('A integração oficial com WhatsApp Business ainda não foi ativada',APP)
        self.assertIn('pontos disponíveis',APP)

if __name__=='__main__':
    unittest.main()
