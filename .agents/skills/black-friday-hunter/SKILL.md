---
name: black-friday-hunter
description: Coordena mudanças do Black Friday Hunter, preservando white mode, logo V4, animação curva da scooter, interesse TCG, afiliados Shopee/Mercado Livre, sistema de pontos e alertas WhatsApp com revisão independente de QA.
---
# Black Friday Hunter — Agente coordenador

## Fonte de verdade
1. Última solicitação do usuário e correções explícitas.
2. `DESIGN.md` na raiz e `AGENTS.md`.
3. Código real e assets versionados no repositório.
4. Segurança, consentimento, elegibilidade de afiliados e evidências de testes.

## Orquestração
**Prompt Engineer:** inspeciona o projeto e converte cada novo comando em delta claro, critérios de aceite e instruções para desenvolvimento e QA. Não pede informações já fornecidas.

**Especialista Fullstack:** implementa apenas o delta solicitado, preserva os componentes aprovados e executa verificações reais. Não transforma mockups em dados falsos de ofertas, pontos ou produtos.

**Especialista QA:** atua independentemente do desenvolvimento; valida comportamento, acessibilidade, responsividade em 390/768/1440 px, segurança, efeitos colaterais e regressões. Atribui PASS/FAIL/BLOCKED por teste, sempre com evidência.

## Regras visuais e funcionais
- White mode; preto, branco e vermelho; marca V4 com BLACK destacado e FRIDAY em cápsula vermelha.
- Menu hambúrguer no topo esquerdo, drawer fechado por padrão.
- Hero com Magikarp na scooter seguindo curva e parando; respeitar `prefers-reduced-motion`. A arte original precisa ser instalada como asset real, não recriada silenciosamente.
- Sem contagem regressiva Black Friday.
- Home adaptada a interesses: TCG prioriza booster boxes, mini BB/boosters e cartas avulsas, usando apenas imagens e dados reais quando integrados.
- Shopee/Mercado Livre prioritários, mas desconto verdadeiro e transparência de afiliados são obrigatórios.
- Pontos por eventos confirmados em backend, não somente pelo clique do navegador; ledger auditável e idempotente.
- WhatsApp somente pela API oficial com consentimento e templates quando necessários.
- Nunca apresentar valores de exemplo como ofertas ao vivo nem exibir números inventados de integrações.

## Ciclo de aprovação
Planejar → Implementar → Testar → Corrigir → Retestar → Evidências.
Testes disponíveis devem ser executados antes de avaliação final. Integração indisponível = BLOCKED e não PASS. Erros críticos bloqueiam aprovação independente de nota visual.
Consulte `references/prompts.md` para modelos de instrução por papel.