/** Official Amazon Creators API integration. No storefront scraping.
 * Configure only on backend: AMAZON_CREATORS_CLIENT_ID,
 * AMAZON_CREATORS_CLIENT_SECRET, AMAZON_ASSOCIATE_TAG, AMAZON_LIST_ASINS.
 */
import {extractCreatorsProducts} from '../app/js/amazon-catalog.mjs';
let token=null,expiry=0;
async function jsonPost(url,headers,payload){
 const response=await fetch(url,{method:'POST',headers:{'content-type':'application/json',...headers},body:JSON.stringify(payload),signal:AbortSignal.timeout(9000)});
 if(!response.ok)throw new Error('Upstream HTTP '+response.status);
 return response.json();
}
async function accessToken(id,secret){
 if(token&&Date.now()<expiry)return token;
 const auth=await jsonPost('https://api.amazon.com/auth/o2/token',{},{
  grant_type:'client_credentials',client_id:id,client_secret:secret,scope:'creatorsapi::default'
 });
 if(!auth.access_token)throw new Error('Missing access token');
 token=auth.access_token;
 expiry=Date.now()+Math.max(0,Number(auth.expires_in||3600)-120)*1000;
 return token;
}
export default async function handler(req,res){
 res.setHeader('Content-Type','application/json; charset=utf-8');
 res.setHeader('X-Content-Type-Options','nosniff');
 if(req.method!=='GET'){
  res.setHeader('Allow','GET');
  return res.status(405).json({status:'method_not_allowed',items:[]});
 }
 const id=process.env.AMAZON_CREATORS_CLIENT_ID;
 const secret=process.env.AMAZON_CREATORS_CLIENT_SECRET;
 const tag=process.env.AMAZON_ASSOCIATE_TAG;
 const asins=[...new Set(String(process.env.AMAZON_LIST_ASINS||'').toUpperCase().split(/[\s,;]+/).filter(x=>/^[A-Z0-9]{10}$/.test(x)))].slice(0,100);
 if(!id||!secret||!tag||!asins.length){
  res.setHeader('Cache-Control','no-store');
  return res.status(200).json({status:'not_configured',items:[],message:'Configure credenciais oficiais e os ASINs da sua lista.'});
 }
 try{
  const bearer=await accessToken(id,secret),updatedAt=new Date().toISOString(),items=[];
  for(let i=0;i<asins.length;i+=10){
   const response=await jsonPost('https://creatorsapi.amazon/catalog/v1/getItems',{
    authorization:'Bearer '+bearer,'x-marketplace':'www.amazon.com.br'
   },{
    itemIds:asins.slice(i,i+10),itemIdType:'ASIN',marketplace:'www.amazon.com.br',partnerTag:tag,
    resources:['itemInfo.title','images.primary.large','images.primary.medium','offersV2.listings.price','offersV2.listings.availability','offersV2.listings.isBuyBoxWinner']
   });
   items.push(...extractCreatorsProducts(response,updatedAt));
  }
  res.setHeader('Cache-Control','public, s-maxage=900, stale-while-revalidate=300');
  return res.status(200).json({status:'official',source:'amazon_creators_api',updatedAt,items});
 }catch{
  res.setHeader('Cache-Control','no-store');
  return res.status(502).json({status:'provider_unavailable',items:[],message:'Não foi possível consultar a API oficial.'});
 }
}
