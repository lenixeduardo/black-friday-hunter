export const AMAZON_LIST_URL='https://amzn.to/4846Sow';
const ASIN_RE=/^[A-Z0-9]{10}$/;
export function isAmazonProductLink(raw){
 try{
  const u=new URL(raw);
  return u.protocol==='https:'&&['www.amazon.com.br','amazon.com.br'].includes(u.hostname)&&/^\/(?:[^/]+\/)?(?:dp|gp\/product)\/[A-Z0-9]{10}(?:\/|$)/i.test(u.pathname);
 }catch{return false}
}
function safeImage(raw){
 if(typeof raw!=='string')return null;
 if(/^\/app\/assets\/amazon\/[a-z0-9-]+\.webp$/.test(raw))return raw;
 try{const u=new URL(raw);if(u.protocol==='https:'&&['m.media-amazon.com','images-na.ssl-images-amazon.com'].includes(u.hostname))return u.href}catch{}
 return null;
}
const safeAmount=n=>typeof n==='number'&&Number.isFinite(n)&&n>0&&n<1e6?n:null;
export function extractArtworkProducts(list){
 if(!list||!Array.isArray(list.items))return [];
 return list.items.map((item,i)=>({
  id:String(item.slug||'art-'+i),asin:ASIN_RE.test(item.asin||'')?item.asin:null,
  name:String(item.name||'Produto sem nome'),image:safeImage(item.image),
  price:{amount:safeAmount(item.poster_price_brl),currency:'BRL',verified:false,source:'arte_enviada',observedAt:null},
  productUrl:isAmazonProductLink(item.product_url)?item.product_url:null,
  listUrl:list.affiliate_destination===AMAZON_LIST_URL?AMAZON_LIST_URL:null,
  category:String(item.category||'TCG'),status:'referencia_nao_verificada'
 }));
}
export function extractCreatorsProducts(payload,observedAt=new Date().toISOString()){
 const raw=payload?.itemsResult?.items||payload?.itemResults?.items||[];
 if(!Array.isArray(raw))return [];
 return raw.flatMap(item=>{
  const asin=String(item.asin||'');
  if(!ASIN_RE.test(asin))return [];
  const productUrl=isAmazonProductLink(item.detailPageURL)?item.detailPageURL:null;
  if(!productUrl)return [];
  const ls=Array.isArray(item.offersV2?.listings)?item.offersV2.listings:[];
  const offer=ls.find(l=>l?.price?.money?.currency==='BRL'&&!l?.violatesMAP)||null;
  const amount=safeAmount(offer?.price?.money?.amount);
  const image=safeImage(item.images?.primary?.large?.url)||safeImage(item.images?.primary?.medium?.url)||safeImage(item.images?.primary?.small?.url);
  const availability=offer?.availability?.type||'UNKNOWN';
  return [{
   id:asin,asin,name:String(item.itemInfo?.title?.displayValue||'Produto '+asin),image,
   price:{amount,currency:'BRL',verified:amount!==null,source:'creators_api',observedAt},
   productUrl,listUrl:null,category:'TCG',
   status:['OUTOFSTOCK','UNAVAILABLE'].includes(availability)?'indisponivel':'consultado',
   availability
  }];
 });
}
export function formatBRL(price){
 if(!price||typeof price.amount!=='number')return null;
 return new Intl.NumberFormat('pt-BR',{style:'currency',currency:'BRL'}).format(price.amount);
}
