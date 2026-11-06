"""Guardrails for user-provided Amazon promo artwork and affiliate destination."""
from pathlib import Path
import json
from bs4 import BeautifulSoup
from PIL import Image
R=Path(__file__).resolve().parents[1]


def test_tcg_amazon_cards_link_only_to_supplied_storefront():
    doc=BeautifulSoup((R/'app/index.html').read_text('utf-8'),'html.parser')
    section=doc.select_one('#amazon-curadoria')
    assert section
    items=section.select('.amazon-item')
    assert len(items)==9  # one source item has no poster price and stays out of the home
    assert sum(not card.has_attr('hidden') for card in items)==4
    for card in items:
        link=card.select_one('a.amazon-list-link')
        assert link['href']=='https://amzn.to/4846Sow'
        assert 'sponsored' in link['rel']
        assert 'noopener' in link['rel']
        assert 'noreferrer' in link['rel']
        assert 'consultar preço' not in card.text.lower()
        assert card.select_one('.amazon-price').get_text(strip=True).startswith('R
        img=card.select_one('img')
        asset=R/img['src'].lstrip('/')
        assert asset.is_file()
        with Image.open(asset) as im:assert im.width>=300 and im.height>=200


def test_curadoria_metadata_is_explicitly_unverified():
    data=json.loads((R/'app/assets/amazon/curadoria.json').read_text('utf-8'))
    assert data['status']=='manual_unverified'
    assert len(data['items'])==10
    assert all(x['price_verified'] is False and x['url']==data['affiliate_destination'] for x in data['items'])


def test_search_and_interest_toggle_are_wired():
    html=(R/'app/index.html').read_text('utf-8')
    assert "document.querySelector('#amazon-curadoria').hidden=v!=='TCG'" in html
    assert 'amazon-result-count' in html
    assert 'amazon-grid' in html
    assert 'scrollIntoView' in html
)
        img=card.select_one('img')
        asset=R/img['src'].lstrip('/')
        assert asset.is_file()
        with Image.open(asset) as im:assert im.width>=300 and im.height>=200


def test_curadoria_metadata_is_explicitly_unverified():
    data=json.loads((R/'app/assets/amazon/curadoria.json').read_text('utf-8'))
    assert data['status']=='manual_unverified'
    assert len(data['items'])==10
    assert all(x['price_verified'] is False and x['url']==data['affiliate_destination'] for x in data['items'])


def test_search_and_interest_toggle_are_wired():
    html=(R/'app/index.html').read_text('utf-8')
    assert "document.querySelector('#amazon-curadoria').hidden=v!=='TCG'" in html
    assert 'amazon-result-count' in html
    assert 'amazon-grid' in html
    assert 'scrollIntoView' in html
