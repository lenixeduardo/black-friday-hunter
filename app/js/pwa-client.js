/* Black Friday Hunter: user-initiated PWA installation and safe update UX. */
(() => {
  'use strict';
  const installButton=document.getElementById('pwa-install');
  const installCopy=document.getElementById('pwa-install-copy');
  const guide=document.getElementById('pwa-install-guide');
  const guideText=document.getElementById('pwa-guide-text');
  const guideClose=document.getElementById('pwa-guide-dismiss');
  const updateBanner=document.getElementById('pwa-update-banner');
  const updateNow=document.getElementById('pwa-update-now');
  const updateDismiss=document.getElementById('pwa-update-dismiss');
  const offlineBar=document.getElementById('pwa-offline-bar');
  const mobileIOS=/iPad|iPhone|iPod/i.test(navigator.userAgent) ||
    (navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
  let deferredPrompt=null;
  let registration=null;
  let reloadRequested=false;
  const standalone=()=>window.matchMedia('(display-mode: standalone)').matches ||
    navigator.standalone===true;
  function installedState(){
    if(!installButton || !standalone())return;
    installButton.disabled=true;
    installButton.querySelector('span').textContent='Aplicativo instalado';
    if(installCopy)installCopy.textContent='Já está disponível na tela inicial do dispositivo.';
    if(guide)guide.hidden=true;
  }
  function connectivity(){
    if(offlineBar)offlineBar.hidden=navigator.onLine!==false;
  }
  function installationGuide(){
    if(!guide||!guideText)return;
    if(updateBanner)updateBanner.hidden=true;
    if(mobileIOS){
      guideText.textContent='No iPhone: abra o menu Compartilhar do navegador, escolha “Adicionar à Tela de Início” e confirme “Adicionar”.';
    }else if(/Android/i.test(navigator.userAgent)){
      guideText.textContent='Abra o menu do navegador e escolha “Instalar app” ou “Adicionar à tela inicial”.';
    }else{
      guideText.textContent='Use o ícone de instalação na barra do navegador ou abra o menu e escolha “Instalar aplicativo”.';
    }
    guide.hidden=false;
  }
  window.addEventListener('beforeinstallprompt',event=>{
    event.preventDefault();
    deferredPrompt=event;
    if(installCopy&&!standalone())installCopy.textContent='Instale o Black Friday Hunter como aplicativo.';
  });
  window.addEventListener('appinstalled',()=>{
    deferredPrompt=null;
    installedState();
  });
  installButton?.addEventListener('click',async()=>{
    if(standalone()){installedState();return;}
    if(deferredPrompt){
      const choice=deferredPrompt;
      deferredPrompt=null;
      try{await choice.prompt();await choice.userChoice;}
      catch{installationGuide();}
    }else{
      installationGuide();
    }
  });
  guideClose?.addEventListener('click',()=>{if(guide)guide.hidden=true;});
  updateDismiss?.addEventListener('click',()=>{if(updateBanner)updateBanner.hidden=true;});
  updateNow?.addEventListener('click',()=>{
    if(registration?.waiting){
      reloadRequested=true;
      registration.waiting.postMessage({type:'SKIP_WAITING'});
      if(updateBanner)updateBanner.hidden=true;
    }
  });
  function offerUpdate(){
    if(registration?.waiting&&navigator.serviceWorker.controller&&updateBanner){
      updateBanner.hidden=false;
    }
  }
  window.addEventListener('online',connectivity);
  window.addEventListener('offline',connectivity);
  connectivity();
  installedState();
  if(!('serviceWorker' in navigator) || !/^https?:$/.test(location.protocol))return;
  navigator.serviceWorker.addEventListener('controllerchange',()=>{
    if(reloadRequested){reloadRequested=false;location.reload();}
  });
  const register=async()=>{
    try{
      registration=await navigator.serviceWorker.register('/app/sw.js',{scope:'/app/'});
      offerUpdate();
      registration.addEventListener('updatefound',()=>{
        const worker=registration.installing;
        worker?.addEventListener('statechange',()=>{
          if(worker.state==='installed')offerUpdate();
        });
      });
    }catch{/* The online app remains functional if the browser blocks SW. */}
  };
  if(document.readyState==='complete')register();
  else window.addEventListener('load',register,{once:true});
})();
