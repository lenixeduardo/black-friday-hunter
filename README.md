# Black Friday Hunter

PWA white mode para descoberta de promoções por interesse, com prioridade futura em Shopee e Mercado Livre e destaque TCG.

## Status atual — Design V2 publicado

**A home está publicada na Vercel**, com logotipo V4, Magikarp na scooter e banner TCG aprovados (3 assets gráficos originais convertidos para WebP transparente, sem recriação de imagem). Menu hambúrguer, categoria persistente, busca, cards e área de recompensas são componentes HTML/CSS/JS responsivos. As demais imagens de UI foram mantidas como referência para não fixar informações como saldos e preços ilustrativos.

**Isto ainda não é o MVP comercial.** Não há preços ao vivo, estoque, comissões, integração oficial de Shopee/Mercado Livre, login, pontos de servidor ou WhatsApp integrado. As ofertas exibidas são exemplos de categorias, claramente rotulados, sem link de compra nem valores inventados.

## URLs

- Produção: https://black-friday-hunter.vercel.app/app/
- Repositório: https://github.com/lenixeduardo/black-friday-hunter
- Relatório: `QA_FIDELITY.md`

## Execução local

```bash
python -m pip install 'pytest>=8,<10' 'Pillow>=10,<13'
python -m http.server 8765
# Navegue para http://localhost:8765/app/
```

## QA

```bash
python -m pytest -q
```

O workflow de GitHub Actions executa testes estruturais, de PWA e referências de assets. Testes visuais de 390 e 1440 px foram feitos localmente, não pela URL de produção.

## Agentes

Consulte `AGENTS.md`, `DESIGN.md` e `.agents/skills/black-friday-hunter/SKILL.md`.

## Próximas etapas

1. Buscar fotos oficiais dos produtos por fonte autorizada e renderizar cards com dados verificáveis.
2. Implementar autenticação e ledger antifraude de pontos no Supabase.
3. Implementar integrações de afiliados da Shopee/Mercado Livre.
4. Configurar alertas via WhatsApp Business Cloud API com consentimento explícito.
5. Auditar a produção em navegador com capturas comparadas ao mockup e corrigir o que falta para 9,5/10.


### Seleção Amazon TCG (curadoria manual)

A home inclui os 10 produtos identificados visualmente no criativo enviado por @eduardotrainerTCG, com recortes da própria arte (não são fotografias verificadas do catálogo). Todos os botões abrem o **mesmo link fornecido pelo responsável** (`https://amzn.to/4846Sow`), sem atribuição individual de ASIN nem preços falsos. A API/vitrine Amazon não pôde ser consultada; disponibilidade, produto exato e valor final dependem de confirmação no site ou app oficial. A seção apresenta transparência sobre afiliação. Os cards não atribuem pontos nem notificações.
