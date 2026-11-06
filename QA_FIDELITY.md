# Black Friday Hunter — Revisão de fidelidade V2

Data: 2026-11-06

## Escopo executado localmente

- White mode mantido; hero restaurado com o logo V4 original, Magikarp original em scooter e banner TCG original (assets convertidos para WebP sem redesenhar o conteúdo).
- Componentes nativos e responsivos: menu hambúrguer, busca, categorias, cards, indicadores e benefícios.
- Interesse TCG/TECNOLOGIA/GAMES/CASA persiste no `localStorage` e muda os elementos de categoria.
- Magikarp chega de uma curva com animação CSS e estado de redução de movimento.
- Não há contagem regressiva de Black Friday.
- Preços, estoque, lojas conectadas, descontos, pontos e links afiliados não são falsamente apresentados como reais: o projeto ainda não integra nenhuma dessas fontes.

## Evidências

- `artifacts/fidelity/home-1440.png`
- `artifacts/fidelity/home-390.png`
- Screenshots com o HTML local e as imagens originais convertidas para data URI em ambiente de teste; não são capturas da produção.

## Resultados de QA

- 8/8 testes unitários: PASSOU.
- Chromium: 390 e 1440 px, imagens carregadas, sem erro JS, sem overflow horizontal, menu, troca de interesses e modal: PASSOU.
- Produção Vercel: NÃO ATUALIZADA nesta execução; persistem as alterações remotas pendentes.
- Card de produto real/preço real: NÃO TESTÁVEL sem API de afiliados, históricos de preço e fonte de imagens.
- Emissão/uso de pontos: NÃO IMPLEMENTADO (depende de backend, ledger antifraude e consentimento).
- Envio WhatsApp/e-mail: NÃO IMPLEMENTADO (depende da API oficial e consentimento).

## Pontuação provisória (design)

- Mockup vs frontend local: aproximadamente **7,5/10** em fidelidade estrutural e de identidade.
- Lacunas: fotos reais de packs/cartas, fontes reais da web se CDN indisponível, adaptação do banner hero em mobile, e microdetalhes do design. A comparação pixel a pixel não foi certificada.
- Mockup vs Vercel atual: **2,5/10**, avaliação anterior, até sincronizar o código e os binários.

## Release seguro

Copiar **todo** o conteúdo de `app/` (incluindo `app/assets/*.webp` e `app/sw.js`) para o repositório GitHub `lenixeduardo/black-friday-hunter` na mesma árvore. A pasta `assets/home/` mantém as imagens PNG originais e a prancha. Criar commit, verificar GitHub Actions e somente então avaliar a URL de produção.
