/* Black Friday Hunter — only cache the static, public shell. */
const CACHE = 'bfh-shell-v2';
const PRECACHE = [
  '/app/', '/app/index.html', '/app/manifest.webmanifest',
  '/app/icon-192.png', '/app/icon-512.png',
  '/app/assets/logo-v4.webp', '/app/assets/magikarp-scooter.webp',
  '/app/assets/banner-tcg.webp'
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
