"""Guardrails for the manually supplied Amazon promotional poster and priced home."""
from pathlib import Path
import json
from bs4 import BeautifulSoup
from PIL import Image

R=Path(__file__).resolve().parents[1]


def test_amazon_home_shows_only_posted_prices_and_reuses_supplied_storefront():
    doc=BeautifulSoup((R/'app/index.html').read_text('utf-8'),'html.parser')
    section=doc.select_one('#amazon-curadoria')
    assert section is not None
    cards=section.select('.amazon-item')
    assert len(cards)==9
    assert sum(not card.has_attr('hidden') for card in cards)==4
    for card in cards:
        link=card.select_one('a.amazon-list-link')
        assert link['href']=='https://amzn.to/4846Sow'
        assert all(v in link['rel'] for v in ('sponsored','noopener','noreferrer'))
        assert 'consultar preço' not in card.get_text().lower()
        price=card.select_one('.amazon-price')
        assert price is not None and price.get_text(strip=True).startswith('R'+chr(36))
        assert 'Valor da arte enviada' in card.get_text()
        img=card.select_one('img')
        asset=R/img['src'].lstrip('/')
        assert asset.is_file()
        with Image.open(asset) as im:
            assert im.width>=300 and im.height>=200


def test_curadoria_keeps_unpriced_tenth_item_only_as_source_data():
    data=json.loads((R/'app/assets/amazon/curadoria.json').read_text('utf-8'))
    assert data['status']=='manual_unverified'
    assert len(data['items'])==10
    assert sum(x['poster_price_brl'] is not None for x in data['items'])==9
    assert all(x['price_verified'] is False and x['url']==data['affiliate_destination'] for x in data['items'])


def test_search_and_interest_toggle_are_wired():
    html=(R/'app/index.html').read_text('utf-8')
    assert "document.querySelector('#amazon-curadoria').hidden=v!=='TCG'" in html
    assert 'amazon-result-count' in html
    assert 'amazon-grid' in html
    assert 'scrollIntoView' in html
