"""No unpriced product card or collectible card on the homepage."""
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]


def test_tcg_cards_are_hidden_in_server_rendered_home():
    html = (ROOT / "app/index.html").read_text(encoding="utf-8")
    page = BeautifulSoup(html, "html.parser")
    panels = page.select_one("#ofertas")
    assert panels is not None
    assert panels.has_attr("hidden"), "TCG cards cannot flash before JS loads"
    assert len(panels.select("#singles article.offer")) == 3
    assert len(panels.select("#tcg-boxes article.offer")) == 3
    assert "function refreshVerifiedOfferCards()" in html
    assert "function isPricedOffer(card)" in html
    assert "bfh:offer-prices-updated" in html


def test_amazon_price_gate_does_not_render_unknown_prices():
    page = BeautifulSoup((ROOT / "app/index.html").read_text(encoding="utf-8"), "html.parser")
    cards = page.select("#amazon-grid article.amazon-item")
    assert len(cards) == 9, "Only nine items have poster prices"
    for card in cards:
        visible_price = card.select_one(".amazon-price")
        assert visible_price is not None
        assert visible_price.get_text(strip=True).startswith("R$")
        assert "Consultar preço na Amazon" not in card.get_text()
    js = (ROOT / "app/js/amazon-catalog-ui.mjs").read_text(encoding="utf-8")
    assert "products.filter(" in js
    assert "product.price.amount > 0" in js


def test_navigate_to_visible_section_when_price_panels_are_hidden():
    page = BeautifulSoup((ROOT / "app/index.html").read_text(encoding="utf-8"), "html.parser")
    skip = page.select_one(".skip-link")
    assert skip is not None and skip["href"] == "#categorias"
    assert page.select_one("#categorias") is not None
    assert page.select_one("#data-warning") is not None
