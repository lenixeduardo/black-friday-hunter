# Black Friday Hunter — QA visual V2

Data: 2026-11-06

## Entrega

- Identidade: white mode, logotipo V4 original, Magikarp na scooter original, banner TCG original; arquivos WebP convertidos dos PNGs aprovados.
- Interações: menu hambúrguer, interesse TCG/TECH/GAMES/HOME persistido, aviso de API não conectada, modal de alertas, categoria e recompensas.
- Layout: desktop 1440 px, mobile 390 px; animação de entrada em curva com redução de movimento.
- Sem contagem regressiva. Não há preços, comissões, descontos, saldos ou links inventados.

## Verificação

- Local: **15/15 testes automatizados PASSOU**; Chromium em 390 e 1440: sem erros JS, sem scroll horizontal, imagens carregadas, menu, categoria e modal funcionais.
- GitHub Actions: **PASSOU**, execução https://github.com/lenixeduardo/black-friday-hunter/actions/runs/42223331612.
- Vercel: deploy de produção marcado **READY** na branch main, com assets estáticos publicados.
- Capturas: `artifacts/fidelity/home-1440.png` e `artifacts/fidelity/home-390.png` apenas no pacote local, não são capturas da produção.

## Nota de fidelidade

- Mockup aprovado versus frontend local correspondente ao código implantado: **7,5/10** (avaliação visual estimada, não medição pixel a pixel).
- Lacunas para a meta 9,5: fotos oficiais reais de produtos/cartas, microdetalhes, banner TCG mobile e verificação de captura da produção em navegador.

## Não implementado

- APIs de afiliados, estoque, preço histórico, automação de WhatsApp, e-mail, autenticação e pontos de servidor.
- As ações desses recursos mostram avisos de integração pendente; não fingem envio de mensagens ou emissão de pontos.
