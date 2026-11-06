"""Static PWA and visual integration tests; do not misrepresent them as live offer API tests."""
import json
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]

def test_pwa_manifest_is_installable():
    data=json.loads((R/'app/manifest.webmanifest').read_text(encoding='utf-8'))
    assert data['name']=='Black Friday Hunter'
    assert data['display']=='standalone'
    assert data['start_url']=='/app/'
    assert data['scope']=='/app/'
    assert {'192x192','512x512'} <= {x['sizes'] for x in data['icons']}
    for icon in data['icons']:
        filename=R/icon['src'].lstrip('/')
        assert filename.exists()
        with Image.open(filename) as image:
            n=int(icon['sizes'].split('x')[0]);assert image.size==(n,n)

def test_home_uses_approved_original_assets():
    html=(R/'app/index.html').read_text(encoding='utf-8')
    for asset in ('logo-v4.webp','magikarp-scooter.webp','banner-tcg.webp'):
        assert f'/app/assets/{asset}' in html
        with Image.open(R/'app/assets'/asset) as img:
            assert img.width>300
            assert img.mode in ('RGBA','RGB')

def test_home_is_interactive_and_does_not_fabricate_offers():
    html=(R/'app/index.html').read_text(encoding='utf-8')
    for control in ('menu-toggle','drawer','interest','tcg-hero','search-form','recompensas'):
        assert f'id="{control}"' in html
    for phrase in ('Mini BB / boosters','Cartas avulsas','Sem preço validado','pontos disponíveis','Sem oferta validada','localStorage.setItem'):
        assert phrase in html
    assert '12.460' not in html
    assert '2.780' not in html
    assert 'Faltam para a Black Friday' not in html
    assert '@media(prefers-reduced-motion:reduce)' in html

def test_service_worker_caches_only_safe_static_assets():
    script=(R/'app/sw.js').read_text(encoding='utf-8')
    assert "function cacheable(url)" in script
    assert "!cacheable(url)" in script
    assert "url.pathname.startsWith('/app/assets/')" in script
    for path in ('/app/index.html','/app/assets/magikarp-scooter.webp','/app/assets/logo-v4.webp'):
        assert path in script
    assert '/api/' not in script
