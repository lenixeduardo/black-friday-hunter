/* Black Friday Hunter — only cache the static, public shell. */
const CACHE = 'bfh-shell-v9';
const PRECACHE = [
  '/app/', '/app/index.html', '/app/manifest.webmanifest',
  '/app/css/fidelity-v5.css', '/app/css/brand-icon-assets-v7.css', '/app/css/affiliate-cta-v8.css', '/app/css/hero-variant-2-v9.css', '/app/js/amazon-catalog-ui.mjs',
  '/app/icon-192.png', '/app/icon-512.png',
  '/app/assets/logo-v4.webp', '/app/assets/magikarp-scooter.webp',
  '/app/assets/banner-tcg.webp',
  '/app/assets/icons/points-medallion.svg',
  '/app/assets/icons/rewards-parcel.svg',
  '/app/assets/icons/alert-message.svg',
  '/app/assets/icons/notification-bell.svg',
  '/app/assets/icons/discount-tag.svg',
  '/app/assets/icons/verified-badge.svg',
  '/app/assets/icons/search-lens.svg',
  '/app/assets/icons/tcg-cards.svg',
  '/app/assets/icons/mail-envelope.svg',
  '/app/assets/icons/benefits-spark.svg',
  '/app/assets/icons/external-link.svg',
  '/app/assets/amazon/catalogo-enviado.webp',
  '/app/assets/tcg/01-vintage-squirtle-base1-63.png',
  '/app/assets/tcg/02-illustration-rare-pikachu-173.png',
  '/app/assets/tcg/03-double-rare-charizard-ex-006.png'
];
function cacheable(url) {
  return PRECACHE.includes(url.pathname) || url.pathname.startsWith('/app/assets/');
}
self.addEventListener('install', event => event.waitUntil(
  caches.open(CACHE).then(cache => cache.addAll(PRECACHE)).then(() => self.skipWaiting())
));
self.addEventListener('activate', event => event.waitUntil(
  caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())
));
self.addEventListener('fetch', event => {
  const request=event.request, url=new URL(request.url);
  if (request.method !== 'GET' || url.origin !== self.location.origin || !cacheable(url)) return;
  event.respondWith(fetch(request).then(response => {
    if(response.ok){const copy=response.clone();caches.open(CACHE).then(cache=>cache.put(request, copy));}
    return response;
  }).catch(()=>caches.match(request)));
});
