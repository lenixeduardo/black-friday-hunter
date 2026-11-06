# Black Friday Hunter

Repositório do **Black Friday Hunter**, aplicativo de monitoramento de ofertas com prioridade para Shopee e Mercado Livre, personalização TCG e planejamento de alertas e recompensas.

## Status de implantação

**Protótipo publicamente versionado, não MVP de produção.** O projeto remoto possui uma interface PWA white mode inicial em `app/index.html`, manifesto, service worker, skill para Codex, design e testes estruturais. Esta publicação não inclui ainda os 9 PNGs originais, o protótipo local completo e todos os scripts detalhados de QA disponíveis no pacote entregue na conversa.

O espaço da hero usa atualmente uma ilustração SVG simplificada como substituto visual; a animação e a arte original do Magikarp devem ser integradas a partir de `assets/home/04-magikarp-scooter.png` quando os assets forem sincronizados.

**Não há promoções ao vivo, login, histórico, pontuação de servidor ou mensagens WhatsApp em funcionamento.** Nunca apresente exemplos como descontos reais nem conceda pontos sem verificação no backend.

## Execução local

```bash
git clone https://github.com/lenixeduardo/black-friday-hunter.git
cd black-friday-hunter
python -m http.server 8765
# Abrir http://localhost:8765/app/
```

## Verificação

```bash
python -m unittest discover -s tests -p "test_*.py" -v
python -m json.tool app/manifest.webmanifest
```

O workflow `.github/workflows/qa.yml` executa essas verificações a cada push/PR. Esses checks são estruturais e não substituem os testes no navegador ou as integrações reais.

## Agentes

Consulte `AGENTS.md`, `DESIGN.md` e `.agents/skills/black-friday-hunter/SKILL.md`. O fluxo esperado é: **especificação → implementação → QA independente → correção → evidências**.

## Próximas integrações

1. Sincronizar os PNGs originais da home e o restante do pacote local.
2. Substituir a arte provisória da hero pelo Magikarp aprovado.
3. Ligar Next.js/Supabase e fontes autorizadas de Shopee/Mercado Livre.
4. Criar ledger de pontos no backend e validação antiabuso.
5. Integrar WhatsApp Business Cloud API após consentimento, credenciais e templates.
6. Validar experiência real em 390, 768 e 1440 px.
