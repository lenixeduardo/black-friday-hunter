# Black Friday Hunter — Instalação local e execução

**Data:** 06/11/2026  
**Status:** `PROTÓTIPO PWA EXECUTADO LOCALMENTE / QA COM RESSALVAS`  
**Repositório GitHub remoto:** **NÃO ENCONTRADO** — sem publicação ou merge remoto.

## Entregues neste repositório Git local

- Skill Codex instalada em `.agents/skills/black-friday-hunter/SKILL.md`.
- `AGENTS.md` e `DESIGN.md` como regras de interpretação e design.
- PWA inicial (`app/index.html`, `app/manifest.webmanifest`, `app/sw.js`, ícones 192/512).
- Hero com Magikarp e animação em curva, menu hambúrguer, preferência local TCG/Tecnologia, seções TCG/mini BB/cartas avulsas.
- Telas sem inventar preços, links, pontos ou status de integrações.
- Testes, QA de assets, smoke Playwright e workflow CI GitHub Actions prontos para o push.

## Execuções reais

| Verificação | Resultado | Evidência |
|---|---|---|
| Testes Python | **7/7 PASS** | `python -m pytest -q` |
| Assets sem fundo | **9/9 PASS** | `artifacts/qa-assets.json` |
| Browser HTML via fixture | **28/28 PASS** | `artifacts/web-app-fixture/report.json`, capturas 390/768/1440 |
| HTTP local via Python/curl | **7/7 HTTP 200** | página, manifesto, SW, ícones e assets |
| Browser HTTP via Playwright | **BLOCKED** | `ERR_BLOCKED_BY_ADMINISTRATOR` para `127.0.0.1` |
| Instalação PWA em dispositivo | **NÃO TESTADA** | Chromium bloqueou navegação HTTP |
| Persistência entre sessões no navegador | **NÃO TESTADA** | implementação inspecionada; teste de browser com origem real bloqueado |
| Shopee/Mercado Livre / WhatsApp / pontos backend | **NÃO IMPLEMENTADO** | exigem integrações e autorização |

## QA e segurança

- O service worker guarda somente a home e assets públicos permitidos, não URLs genéricas de conta/API.
- Scripts de planejamento geram briefs para papéis; **não** são um motor que executa agentes LLM sozinho.
- Dados de cards e totais não são apresentados como dados reais. Os dados dentro de assets conceituais devem ser substituídos por componentes dinâmicos quando necessário.
- Este protótipo usa HTML/CSS/JavaScript, **não Next.js**; instalar dependências e migrar para a stack final é etapa posterior.
- Nenhum link de afiliado foi inventado, nenhuma mensagem foi enviada, nenhum ponto foi creditado.

## Aprovação

Aprovação limitada ao protótipo local e às verificações descritas. **Não aprovado para produção.** Falta GitHub remoto correspondente, fontes de preços oficiais, autenticação, ledger de pontos, WhatsApp Cloud API e QA de integração real.