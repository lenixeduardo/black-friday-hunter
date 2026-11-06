# Black Friday Hunter — PWA demonstrativa + skill Codex

Este repositório local contém o protótipo PWA executável, design e assets aprovados, skill, gerador de briefs e testes. **Não é produção nem possui feeds de ofertas ou WhatsApp reais.**

## Execução local

```bash
python -m http.server 8765
# navegador: http://127.0.0.1:8765/app/
```

Para instalar a PWA, abra em navegador compatível num contexto seguro (localhost ou HTTPS). Preferência de interesse TCG/Tecnologia persistida apenas neste dispositivo.

## Executar agente e QA

```bash
python scripts/agent.py plan "Instale a skill e teste o Black Friday Hunter" --output artifacts/plan-install
python -m pytest -q
python scripts/qa_assets.py --dir assets/home --out artifacts/qa-assets.json
python scripts/qa_web.py --url http://127.0.0.1:8765/app/ --out artifacts/web-app
```

A skill está instalada neste repositório em `.agents/skills/black-friday-hunter/SKILL.md`, referenciada por `AGENTS.md`. O script `agent.py` gera prompts; não invoca um LLM automaticamente.

## Limitações

- **Publicação remota pendente:** repositório Git local preparado com o nome `black-friday-hunter`. Consulte `PUBLISH_GITHUB.md` para criar o repositório e publicar no GitHub.
- Nenhuma fonte de oferta, integração de afiliados ou link rastreável ativo.
- Sem crédito real de pontos, backend, autenticação ou resgates. Saldos dos assets gráficos são ilustrativos e não usados como dados da UI.
- Envio de WhatsApp e e-mail indisponíveis até configuração de credenciais, consentimento e templates.
- O protótipo atual usa HTML/CSS/JS como prova visual, **não Next.js**; a migração permanece parte da implementação do produto.

## Organização

- `app/`: frontend PWA inicial funcional de navegação e preferências.
- `assets/home/`: assets individuais transparentes e prancha.
- `.agents/skills/black-friday-hunter/`: skill de desenvolvimento/QA.
- `AGENTS.md`, `DESIGN.md`: instruções e design source of truth.
- `scripts/`, `tests/`: automação de briefs e testes.