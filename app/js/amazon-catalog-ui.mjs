import {extractArtworkProducts,formatBRL} from './amazon-catalog.mjs';
const grid=document.querySelector('#amazon-grid');
if(grid){
 const count=document.querySelector('#amazon-result-count');
 const disclosure=document.querySelector('#amazon-disclosure');
 const node=(tag,cls,text)=>{
  const element=document.createElement(tag);
  if(cls)element.className=cls;
  if(text!==undefined)element.textContent=text;
  return element;
 };
 function makeCard(product){
  const article=node('article','amazon-item');
  article.dataset.product=(product.name+' '+product.category).toLocaleLowerCase('pt-BR');
  const photo=node('div','amazon-item-photo');
  if(product.image){
   const image=node('img');
   image.src=product.image;
   image.alt=product.name;
   image.loading='lazy';
   image.decoding='async';
   photo.append(image);
  }else photo.append(node('span','muted','Imagem não disponível'));
  const info=node('div','amazon-item-info');
  info.append(node('span','amazon-kind',product.category),node('h3','',product.name));
  const formatted=formatBRL(product.price);
  if(formatted){
   info.append(node('div','amazon-price',formatted));
   info.append(node('small','amazon-price-origin',product.price.verified?'Preço informado pela Amazon':'Valor da arte enviada · não atualizado'));
   if(product.price.verified&&product.price.observedAt)
    info.append(node('small','amazon-price-origin','Consultado: '+new Date(product.price.observedAt).toLocaleString('pt-BR',{timeZone:'America/Sao_Paulo'})));
  }else info.append(node('div','amazon-price unknown','Consultar preço na Amazon'));
  const destination=product.productUrl||product.listUrl;
  if(destination){
   const link=node('a','amazon-list-link',product.productUrl?'Ver produto na Amazon ↗':'Ver na lista de afiliado ↗');
   link.href=destination;
   link.target='_blank';
   link.rel='noopener noreferrer sponsored';
   link.setAttribute('aria-label',(product.productUrl?'Ver produto ':'Abrir lista para encontrar ')+product.name+' na Amazon');
   info.append(link);
  }else info.append(node('span','amazon-price-origin','Link individual pendente'));
  article.append(photo,info);
  return article;
 }
 function render(items){
  grid.replaceChildren(...items.map(makeCard));
  const query=document.querySelector('#search-form input')?.value.trim().toLocaleLowerCase('pt-BR')||'';
  const cards=[...grid.querySelectorAll('.amazon-item')];
  cards.forEach(card=>card.hidden=Boolean(query&&!card.dataset.product.includes(query)));
  if(count)count.textContent=cards.filter(card=>!card.hidden).length+' de '+items.length+' itens';
 }
 async function jsonFrom(url){
  const response=await fetch(url,{headers:{accept:'application/json'},cache:'no-cache'});
  if(!response.ok)throw new Error('HTTP '+response.status);
  return response.json();
 }
 try{
  const artwork=await jsonFrom('/app/assets/amazon/curadoria.json');
  render(extractArtworkProducts(artwork));
  if(disclosure)disclosure.textContent='Produtos e valores transcritos da arte enviada. Não representam preços nem disponibilidade atuais. Os botões abrem a lista de afiliado até a integração com links individuais pela API oficial.';
 }catch{
  if(disclosure)disclosure.textContent='Não foi possível carregar a curadoria. Consulte o link da sua lista Amazon.';
 }
 try{
  const live=await jsonFrom('/api/amazon-products');
  if(live.status==='official'&&Array.isArray(live.items)&&live.items.length){
   render(live.items);
   if(disclosure)disclosure.textContent='Preços, imagens e links fornecidos pela Creators API da Amazon. Valores e disponibilidade podem mudar. Confirme antes de comprar.';
  }
 }catch{
  // Keep the clearly labeled artwork reference; never fake live prices.
 }
}
