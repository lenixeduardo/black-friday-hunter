import { extractArtworkProducts, formatBRL } from './amazon-catalog.mjs';

const grid = document.querySelector('#amazon-grid');
if (grid) {
  const count = document.querySelector('#amazon-result-count');
  const disclosure = document.querySelector('#amazon-disclosure');
  const showAll = document.querySelector('#amazon-show-all');
  const empty = document.querySelector('#amazon-empty');
  const INITIAL_VISIBLE = 4;
  let items = [];
  let expanded = false;
  let searchTerm = '';

  const normalize = value => String(value ?? '').normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('pt-BR').trim();
  const node = (tag, className = '', text) => {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (text !== undefined) element.textContent = text;
    return element;
  };

  function makeCard(product) {
    const article = node('article', 'amazon-item');
    article.dataset.product = normalize(product.name + ' ' + product.category);

    const photo = node('div', 'amazon-item-photo');
    if (product.image) {
      const image = node('img');
      image.src = product.image;
      image.alt = product.name;
      image.loading = 'lazy';
      image.decoding = 'async';
      photo.append(image);
    } else {
      photo.append(node('span', 'muted', 'Imagem não disponível'));
    }

    const info = node('div', 'amazon-item-info');
    info.append(
      node('span', 'amazon-kind', product.category),
      node('h3', '', product.name)
    );
    const formatted = formatBRL(product.price);
    if (formatted) {
      info.append(node('div', 'amazon-price', formatted));
      info.append(node('small', 'amazon-price-origin',
        product.price.verified ? 'Preço informado pela Amazon' : 'Valor da arte enviada · não atualizado'
      ));
      if (product.price.verified && product.price.observedAt) {
        info.append(node('small', 'amazon-price-origin',
          'Consultado: ' + new Date(product.price.observedAt)
            .toLocaleString('pt-BR', { timeZone: 'America/Sao_Paulo' })
        ));
      }
    } else {
      info.append(node('div', 'amazon-price unknown', 'Consultar preço na Amazon'));
    }

    const destination = product.productUrl || product.listUrl;
    if (destination) {
      const individual = Boolean(product.productUrl);
      const link = node('a', 'amazon-list-link',
        individual ? 'Ver produto na Amazon ↗' : 'Ver na lista de afiliado ↗');
      link.href = destination;
      link.target = '_blank';
      link.rel = 'noopener noreferrer sponsored';
      link.setAttribute('aria-label',
        (individual ? 'Ver produto ' : 'Abrir lista para encontrar ') + product.name + ' na Amazon');
      info.append(link);
    } else {
      info.append(node('span', 'amazon-price-origin', 'Link individual pendente'));
    }
    article.append(photo, info);
    return article;
  }

  function updateVisibility() {
    const hasSearch = Boolean(searchTerm);
    let matched = 0;
    let visible = 0;
    [...grid.querySelectorAll('.amazon-item')].forEach((card, index) => {
      const match = !hasSearch || card.dataset.product.includes(searchTerm);
      if (match) matched++;
      const show = match && (hasSearch || expanded || index < INITIAL_VISIBLE);
      card.hidden = !show;
      if (show) visible++;
    });

    if (count) {
      count.textContent = hasSearch
        ? matched + ' de ' + items.length + ' resultados'
        : (expanded ? items.length + ' itens da seleção' : visible + ' de ' + items.length + ' itens em destaque');
    }
    if (showAll) {
      showAll.hidden = hasSearch || items.length <= INITIAL_VISIBLE;
      showAll.setAttribute('aria-expanded', String(expanded));
      showAll.textContent = expanded
        ? 'Mostrar apenas os destaques'
        : 'Ver todos os ' + items.length + ' produtos da seleção';
    }
    if (empty) empty.hidden = !hasSearch || matched > 0;
  }

  function render(products) {
    items = products;
    grid.replaceChildren(...items.map(makeCard));
    updateVisibility();
  }

  showAll?.addEventListener('click', () => {
    expanded = !expanded;
    updateVisibility();
    if (!expanded) document.querySelector('.amazon-catalog-toolbar')?.scrollIntoView({
      behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth',
      block: 'start'
    });
  });

  window.addEventListener('bfh:search', event => {
    searchTerm = normalize(event.detail?.term);
    updateVisibility();
  });

  async function jsonFrom(url) {
    const response = await fetch(url, { headers: { accept: 'application/json' }, cache: 'no-cache' });
    if (!response.ok) throw new Error('HTTP ' + response.status);
    return response.json();
  }

  try {
    const artwork = await jsonFrom('/app/assets/amazon/curadoria.json');
    render(extractArtworkProducts(artwork));
    if (disclosure) disclosure.textContent =
      'Produtos e valores transcritos da arte enviada. Não representam preços nem disponibilidade atuais. Os botões abrem a lista de afiliado até a integração com links individuais pela API oficial.';
  } catch {
    if (disclosure) disclosure.textContent =
      'Não foi possível carregar a curadoria. Consulte o link da sua lista Amazon.';
  }

  try {
    const live = await jsonFrom('/api/amazon-products');
    if (live.status === 'official' && Array.isArray(live.items) && live.items.length) {
      render(live.items);
      if (disclosure) disclosure.textContent =
        'Preços, imagens e links fornecidos pela Creators API da Amazon. Valores e disponibilidade podem mudar. Confirme antes de comprar.';
    }
  } catch {
    // Maintain explicitly identified artwork references. Never synthesize live offers.
  }
}
