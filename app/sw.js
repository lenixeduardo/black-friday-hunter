/* Black Friday Hunter PWA V10: public, installable, and privacy-safe.
 * No API, account, payment, private data or third-party content is cached. */
const CACHE = 'bfh-shell-v10';
const CACHE_PREFIX = 'bfh-shell-';
const OFFLINE_PAGE = '/app/offline.html';
const PRECACHE = [
  '/app/', '/app/index.html', OFFLINE_PAGE, '/app/manifest.webmanifest',
  '/app/css/fidelity-v5.css', '/app/css/brand-icon-assets-v7.css',
  '/app/css/affiliate-cta-v8.css', '/app/css/hero-variant-2-v9.css',
  '/app/css/pwa-v10.css',
  '/app/js/pwa-client.js', '/app/js/amazon-catalog.mjs', '/app/js/amazon-catalog-ui.mjs',
  '/app/icon-192.png','/app/icon-512.png','/app/icon-maskable-192.png',
  '/app/icon-maskable-512.png','/app/apple-touch-icon.png',
  '/app/assets/logo-v4.webp', '/app/assets/magikarp-scooter.webp',
  '/app/assets/banner-tcg.webp',
  '/app/assets/icons/points-medallion.svg','/app/assets/icons/rewards-parcel.svg',
  '/app/assets/icons/alert-message.svg','/app/assets/icons/notification-bell.svg',
  '/app/assets/icons/discount-tag.svg','/app/assets/icons/verified-badge.svg',
  '/app/assets/icons/search-lens.svg','/app/assets/icons/tcg-cards.svg',
  '/app/assets/icons/mail-envelope.svg','/app/assets/icons/benefits-spark.svg',
  '/app/assets/icons/external-link.svg',
  '/app/assets/amazon/curadoria.json',
  '/app/assets/amazon/catalogo-enviado.webp',
  '/app/assets/amazon/colecao-parceiro-inicial.webp',
  '/app/assets/amazon/reinado-delta-bundle.webp',
  '/app/assets/amazon/celebracao-poster.webp',
  '/app/assets/amazon/reinado-delta-atb.webp',
  '/app/assets/amazon/reinado-delta-sleeved.webp',
  '/app/assets/amazon/celebracao-bundle.webp',
  '/app/assets/amazon/reinado-delta-box.webp',
  '/app/assets/amazon/caos-ascendente-box.webp',
  '/app/assets/amazon/escuridao-sleeved.webp',
  '/app/assets/tcg/01-vintage-squirtle-base1-63.png',
  '/app/assets/tcg/02-illustration-rare-pikachu-173.png',
  '/app/assets/tcg/03-double-rare-charizard-ex-006.png'
];
const PRECACHE_SET=new Set(PRECACHE);
function cacheable(url){
  return PRECACHE_SET.has(url.pathname) || url.pathname.startsWith('/app/assets/');
}
self.addEventListener('install',event=>{
  event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(PRECACHE)));
});
self.addEventListener('activate',event=>{
  event.waitUntil(
    caches.keys().then(keys=>Promise.all(
      keys.filter(key=>key.startsWith(CACHE_PREFIX)&&key!==CACHE)
          .map(key=>caches.delete(key))
    )).then(()=>self.clients.claim())
  );
});
self.addEventListener('message',event=>{
  if(event.data && event.data.type==='SKIP_WAITING') self.skipWaiting();
});
async function appNavigation(request){
  const cache=await caches.open(CACHE);
  try {
    const response=await fetch(request);
    if(response.ok && new URL(request.url).pathname.startsWith('/app/')){
      await cache.put('/app/index.html',response.clone());
    }
    return response;
  }catch{
    return await cache.match('/app/index.html') ||
      await cache.match('/app/') ||
      await cache.match(OFFLINE_PAGE) ||
      Response.error();
  }
}
async function cachedStatic(request){
  const cache=await caches.open(CACHE);
  const hit=await cache.match(request,{ignoreSearch:true});
  if(hit)return hit;
  const response=await fetch(request);
  if(response.ok && response.type==='basic'){
    try{await cache.put(request,response.clone());}catch{/* quota exceeded: online still works */}
  }
  return response;
}
self.addEventListener('fetch',event=>{
  const request=event.request,url=new URL(request.url);
  if(request.method!=='GET'||url.origin!==self.location.origin)return;
  // Only same-origin navigations inside /app/ receive a cached app shell.
  if(request.mode==='navigate' && url.pathname.startsWith('/app/')){
    if(url.pathname===OFFLINE_PAGE){
      event.respondWith(cachedStatic(request));
    }else{
      event.respondWith(appNavigation(request));
    }
    return;
  }
  if(!cacheable(url))return;
  event.respondWith(cachedStatic(request));
});
