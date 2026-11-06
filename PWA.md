# Black Friday Hunter — PWA instalável (V10)

## Instalação

Acesse https://black-friday-hunter.vercel.app/app/ via HTTPS.

- **iOS 16.4+**: menu Compartilhar do navegador → **Adicionar à Tela de Início** → Adicionar. O suporte pode variar conforme o navegador.
- **Android/Chromium**: menu ou ícone Instalar aplicativo; também há a opção no menu do Black Friday Hunter.
- **Desktop Chromium**: clique no ícone de instalação próximo à barra de endereços ou utilize Instalar aplicativo no menu.

O botão **Instalar aplicativo** no menu oferece instruções quando o navegador não expõe `beforeinstallprompt` (por exemplo, no iPhone).

## Capacidades

- Manifesto Web App com `start_url`, `scope`, `display: standalone` e ícones `any` e `maskable`.
- Ícone 180x180 para a tela inicial do iPhone, gerado a partir **do mascote original** já aprovado, sem recriar a arte.
- Service worker versionado e limitado a HTML/CSS/JS e assets estáticos públicos.
- Conteúdo do último carregamento disponível offline; indicador explícito avisa que preços podem estar desatualizados.
- Cache não intercepta endpoints de API, sessões privadas, pagamentos ou domínios externos.
- Atualização controlada pelo usuário: aviso de nova versão, botão Atualizar e troca segura do service worker.
- Suporte a `prefers-reduced-motion` na hero aprovada.

## Limites

PWA **não é APK nem IPA**. Instalação depende de browser e sistema operacional; não envolve App Store.
A loja Amazon requer internet, e os nove valores oriundos da arte enviada continuam **referenciais, não cotações atuais**.
Push, WhatsApp, resgate de pontos e integrações oficiais **não estão ativos**. A instalação não solicita permissão de notificação.

## Validação

`python -m pytest -q` e `python scripts/qa_pwa_v10.py`.
O CI confere manifestos, ícones, service worker, instalação manual, carregamento offline e os três breakpoints 390/768/1440 px.
