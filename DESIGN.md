# BLACK FRIDAY HUNTER — DESIGN.md

> **Status:** especificação de produto, design, arquitetura e operação de agentes.  
> **Versão:** 1.0 — 06/11/2026  
> **Escopo atual:** design e instruções de execução; nenhuma integração, funcionalidade ou teste é considerado implementado por este documento.

## 1. Propósito

Construir um aplicativo web responsivo e instalável como PWA para encontrar promoções reais, comparar preços e entregar alertas personalizados por WhatsApp. O produto combina **personalização por interesses**, **prioridade para ofertas elegíveis a afiliados Shopee e Mercado Livre**, **gamificação por atividade** e um dashboard em **white mode minimalista**.

**Proposta de valor:** “Encontre antes. Economize mais.”

### Resultados desejados

- O usuário identifica rapidamente ofertas relevantes, com histórico e nível de verificação explícitos.
- Usuários interessados em **TCG** veem primeiro booster boxes, mini booster boxes/mini BB, boosters, ETBs, coleções e cartas avulsas.
- O usuário pode receber alertas no WhatsApp **somente após consentimento válido e configuração da integração oficial**.
- A abertura de ofertas externas pode gerar pontos de atividade, com regras antifraude e resgates claramente definidos.
- O administrador acompanha fontes, afiliados, links, cliques, comissões verificadas, filas e falhas sem números inventados.

## 2. Regras imutáveis do projeto

1. **White mode obrigatório:** fundo claro, tipografia escura, vermelho Black Friday como principal destaque; nunca alterar para dark mode sem comando explícito.
2. **Logotipo aprovado — variante V4:** “BLACK” preto em estilo itálico impactante, “FRIDAY” branco sobre cápsula/faixa vermelha, “HUNTER” abaixo com espaçamento entre letras; arco/swoosh vermelho sutil. A identidade não deve ser trocada ou redesenhada a cada iteração.
3. **Tipografia:** Poppins ExtraBold/SemiBold no branding, títulos e CTAs; Inter para textos, navegação, filtros, preços auxiliares e dados. O logo deve preferencialmente ser um asset vetorial próprio, não texto aproximado por CSS.
4. **Hero:** mascote **Magikarp na scooter vermelha**, com balões de cupons, caixas e aparência consistente com o asset já aprovado; imagem em transparência real (canal alfa). Não gerar versões diferentes do personagem sem solicitação.
5. **Remover contagem regressiva** e qualquer cartão “Faltam X dias para a Black Friday”.
6. **Navegação:** botão hambúrguer no canto **superior esquerdo**; menu lateral **fechado por padrão**, aberto por overlay/drawer quando acionado. Não manter sidebar fixa ocupando a home.
7. **Hero animada:** a scooter entra em trajetória curva, desacelera e **para na posição final**; sem looping que faça o mascote sair repetidamente.
8. **Afiliados:** dar prioridade operacional a Shopee e Mercado Livre, mas **nunca falsificar a validação de descontos nem priorizar comissão acima da relevância e da segurança**.
9. **Home personalizada:** interesses explícitos do usuário controlam os destaques. Para `TCG`, apresentar seções prioritárias de produtos selados e cartas avulsas.
10. **Sem dados falsos apresentados como reais:** estatísticas, estoque, preços, avaliações, pontuações, comissões e status de integrações precisam vir de fonte real. Em protótipos, usar estados vazios ou marcadores claramente identificados como **Dados demonstrativos**.
11. **Sem recriar cartas oficiais para fingir listagens reais:** fotos de produtos e cartas vêm de fontes/autorização apropriadas; usar placeholders neutros quando faltar imagem.
12. **Sem emojis como ícones de UI:** usar ícones vetoriais consistentes (Lucide ou biblioteca equivalente).
13. **Não assumir funcionamento de integrações** sem credenciais, permissões, teste e evidência.
14. **Não inventar depoimentos, parceiros ou benefícios ativos**; oferecer configuração real no painel.
15. **Responsivo obrigatório:** validar 390 px, 768 px e 1440 px, além de estados intermediários.

## Hero aprovada — variante 02 (06/11/2026)

A variante **02** foi aprovada explicitamente pelo usuário, substituindo a hero anterior de três colunas. Referência de composição, não imagem achatada no frontend.

- Cabeçalho de navegação **externo ao card**, white mode, logo V4 original e menu no canto superior esquerdo.
- Hero como **um card vermelho de cantos arredondados**; gradiente tonal discreto e bastante espaço negativo.
- **Duas colunas desktop:** conteúdo textual conciso à esquerda; **mesmo asset original** `/app/assets/magikarp-scooter.webp` à direita, sem redesenho.
- Título “Encontre antes. Economize mais.”, segunda frase em capsule branca com texto vermelho.
- Somente CTA principal **Explorar Amazon TCG**, com link de afiliado fornecido, e CTA secundário **Alertas de ofertas** com modal transparente de integração pendente; não prometer alertas ativos.
- Não repetir banner/editorial TCG dentro da hero nem inventar números, preços ou resultados. Preservar o banner original como asset histórico, sem renderizá-lo ali.
- Mobile: texto primeiro, ações acessíveis com 48 px, mascote abaixo sem cortar, nenhum overflow; animação curva uma vez e `prefers-reduced-motion`.
- **Sem emojis de WhatsApp, coroas ou símbolos genéricos** como assets. Não trocar o logo V4 nem alterar personagem e suas cores.
- Não modificar módulos fora da hero, exceto testes, PWA e documentação necessários.

## 3. Design system

### 3.1 Cores

| Token | Valor inicial | Uso |
|---|---|---|
| `--background` | `#FFFFFF` | Fundo da aplicação |
| `--surface` | `#FAFAFB` | Seções, cards e inputs |
| `--surface-muted` | `#F3F4F6` | Estados secundários |
| `--foreground` | `#111114` | Texto principal |
| `--muted-foreground` | `#6B7280` | Textos auxiliares |
| `--brand-red` | `#E50914` | CTAs, logotipo, preços em destaque |
| `--brand-red-hover` | `#C90711` | Estados hover |
| `--border` | `#E5E7EB` | Bordas discretas |
| `--whatsapp` | `#25D366` | Identificação específica do canal |
| `--success` | `#16864B` | Status realmente verificados |
| `--warning` | `#A45C00` | Desconto não verificado, dados insuficientes |

Não usar vermelho para indicar indiscriminadamente sucesso, erro e desconto ao mesmo tempo. Verificar contraste conforme WCAG 2.2 AA.

### 3.2 Tipografia e medidas

- **Branding:** Poppins ExtraBold, inclinação itálica e espaçamento controlado, V4.
- **Títulos:** Poppins Semibold/ExtraBold, escala `clamp()` responsiva.
- **Interface:** Inter 400/500/600; preços principais com peso 700/800.
- **Espaçamento:** grade de 4/8 px; padding confortável; altura mínima de alvo interativo de 44 px.
- **Raios:** cards 16–24 px; botões 12–16 px; pills 999 px.
- **Sombras:** suaves, sem brilho neon dominante; movimento limitado e funcional.
- **Ícones:** stroke coerente, 20–24 px; sem emojis substituindo ícones.

### 3.3 Layout

- **Desktop 1440:** topo fixo leve, largura máxima de conteúdo 1320 px; 4 cards de oferta por linha se houver espaço; hero em duas colunas.
- **Tablet 768:** hero adaptada, catálogo em 2 colunas, drawer de navegação.
- **Mobile 390:** topo com hambúrguer na esquerda, logo compacto, pontos/perfil à direita; hero com texto primeiro e mascote abaixo ou ao lado sem corte; cards em uma coluna ou trilho horizontal acessível; nenhuma rolagem horizontal acidental.
- **Acessibilidade:** foco visível, operação por teclado, labels dos controles, `prefers-reduced-motion`, navegação com leitor de tela.

## 4. Identidade e conteúdo da hero

### 4.1 Topbar

`[ícone menu] [LOGO BLACK FRIDAY HUNTER] [saldo de pontos] [notificações] [perfil]`

O hambúrguer abre drawer com: Início, Explorar ofertas, Meus alertas, Favoritos, Recompensas, Configurações e, apenas para usuários autorizados, Central de Afiliados, Integrações, Relatórios e Administração.

### 4.2 Hero

**Título:** Encontre antes. **Economize mais.**  
**Subtítulo:** Promoções selecionadas para seus interesses, descontos verificados e alertas no WhatsApp.  
**CTA primário:** Ativar alertas no WhatsApp.  
**CTA secundário:** Explorar ofertas.  
**Imagem:** Magikarp dirigindo scooter vermelha, pacotes e balões de cupons, asset transparente já aprovado.

Evitar repetir o logotipo em tamanho excessivo dentro da hero: o branding fica destacado na topbar e a headline domina a área de conteúdo. Não mostrar contagem regressiva.

### 4.3 Animação do mascote (requisito funcional)

1. **Inicial:** mascote fora da área visível, preferencialmente à direita ou conforme sentido definido pela composição.
2. **Entrada:** deslocamento seguindo caminho curvo (SVG motion path ou trajetória Bézier equivalente) com leve rotação alinhada ao percurso.
3. **Desaceleração:** easing suave, sem rebote exagerado; rodas/partículas podem acompanhar o movimento.
4. **Parada:** mascote permanece visível e estável na posição final, sem obstruir texto, navegação ou botões.
5. **Mobile:** rota e escala próprias, respeitando viewport e `overflow`; nunca cortar scooter/rosto/balões.
6. **Acessibilidade:** com `prefers-reduced-motion`, apresentar diretamente o quadro final, sem trajetória.
7. **Performance:** animar preferencialmente `transform` e `opacity`; carregar asset otimizado; evitar layout shift.

**Critério de aceite:** animação roda uma vez por entrada pertinente da hero, termina na posição correta e não recomeça a cada atualização de estado do dashboard.

## 5. Personalização por interesse

### 5.1 Entrada e preferências

- Primeiro acesso: permitir selecionar um ou mais interesses — TCG, Tecnologia, Games, Smartphones, Computadores, Eletrodomésticos, Casa, Moda, Beleza e Outros.
- Persistir preferências no perfil autenticado; permitir editar em um seletor discreto no topo da home.
- Não presumir que o usuário é fã de Pokémon: somente priorizar TCG quando escolhido ou aprendido a partir de comportamento autorizado e transparente.
- Caso não haja preferências ou dados, mostrar feed geral com convites para personalizar.

### 5.2 Home com interesse TCG

**Ordem inicial de seções:**

1. **Banner editorial TCG em oferta**, sem ofertas fictícias: somente campanha ativa que possua dados autorizados.
2. **Booster boxes e coleções seladas:** booster boxes, ETBs, kits e boxes especiais.
3. **Mini BB e boosters:** mini booster boxes e boosters unitários, em destaque visual próximo ao topo.
4. **Cartas avulsas:** singles com imagem real, nome, set, numeração, acabamento (foil/não foil), idioma, condição declarada e loja.
5. **Quedas de preço para seus favoritos:** só com histórico real suficiente.
6. **Outras categorias:** visíveis, mas secundárias.

**Card TCG selado:** imagem original, título, coleção, quantidade de boosters quando confirmada, preço atual, referência histórica, disponibilidade, fonte, cashback/cupom quando confirmados, desconto verificado ou aviso de incerteza, botão “Ver na loja”, pontos possíveis conforme regra vigente.

**Card de carta avulsa:** foto real da carta, identificação exata, raridade se disponível, variação/foil, idioma, condição NM/LP/MP etc. conforme anúncio, preço, frete quando disponível e link afiliado elegível. Não combinar versões distintas da mesma carta na comparação de preços.

### 5.3 Personalização de ranking

`relevância do interesse + oportunidade verificada + disponibilidade + qualidade do anúncio + prioridade de afiliado`.

Manter dois índices auditáveis:

- `opportunity_score (0–100)`: qualidade da promoção calculada a partir de evidências.
- `affiliate_priority_score (0–100)`: elegibilidade e relevância comercial, sem adulterar o primeiro índice.

Ofertas não verificadas podem aparecer, mas com rótulo claro e sem selo de “oferta verificada”.

## 6. Telas e fluxos

| Tela | Conteúdo obrigatório | Ação principal |
|---|---|---|
| **Home** | Hero, interesses, busca, ofertas relevantes e TCG quando selecionado | Explorar / criar alerta |
| **Explorar** | Busca, filtros, ordenação, loja, faixa de preço, desconto verificado | Ver oferta |
| **Detalhes da oferta** | Produto/variante, preços e histórico, fonte, data, condições, risco de desatualização | Abrir link de afiliado |
| **Meus alertas** | Produtos, categoria, palavras-chave, preço-alvo, frequência, estado | Criar/editar alerta |
| **WhatsApp** | Número verificado, consentimento, categorias, janelas de silêncio, status | Ativar/pausar |
| **Favoritos** | Produtos salvos e histórico, sem dados fictícios | Acompanhar |
| **Pontos e recompensas** | Saldo, extrato, regras, benefícios disponíveis, resgate | Resgatar benefício |
| **Central de Afiliados** | Shopee e Mercado Livre prioritários, status, links, cliques, conversões verificadas | Configurar integração |
| **Administração** | Coletas, filas, webhooks, logs, antifraude, entregas e incidentes | Diagnosticar |

### 6.1 Abertura do menu

- Clique no hambúrguer → drawer aparece com overlay, foco gerenciado, fechar por `Esc`, clique fora ou botão fechar.
- Fechado por padrão em todos os breakpoints; priorizar navegação simplificada para o público geral.

### 6.2 Abrir oferta em navegador externo

- Botão “Ver na loja” abre URL de destino afiliado autorizada por fluxo de redirecionamento controlado.
- **Pontuação é concedida pelo evento elegível de saída validado no servidor**, não por alegar que a página externa foi carregada ou houve compra.
- Em PWA/mobile, usar comportamento de abrir navegador compatível com a plataforma; não prometer forçar um navegador específico em todos os sistemas.
- Mostrar aviso discreto “Link de afiliado: podemos receber comissão, sem custo adicional para você”.
- Impedir redirecionamentos abertos (`open redirect`), links expirados, destinos não autorizados e manipulação dos parâmetros de afiliado.

## 7. Programa de pontos e recompensas

### 7.1 Obtenção de pontos

- Ação elegível: clique validado em “Ver na loja” com redirecionamento externo permitido.
- Configurar no admin: pontos por evento, teto por dia, janela de repetição e elegibilidade por usuário/produto.
- Somente usuários autenticados podem acumular saldo persistente; visitante pode explorar ofertas sem pontos.
- Não recompensar múltiplos cliques repetidos no mesmo anúncio dentro da janela antifraude.
- Registrar cada crédito/débito em **ledger imutável**, com idempotência.

### 7.2 Resgate

- **Notícias por e-mail:** benefício de assinatura/digest por período ou condição configurável.
- **Alertas WhatsApp:** benefício de alertas segmentados ou recurso premium por período configurável.
- O catálogo de recompensas e custo em pontos vem da base de dados; **não fixar valores como 500 pontos sem decisão do administrador**.
- Mesmo após resgatar, exigir consentimento independente, opt-in e a possibilidade de cancelar o recebimento.
- O sistema não deve incentivar envios excessivos nem contornar políticas da WhatsApp Business Platform.

### 7.3 Estado visual

- Saldo real no topo; extrato de créditos e resgates; nível de progresso somente se existir regra publicada.
- Banner secundário: “Acumule pontos ao explorar ofertas elegíveis”.
- Evitar prometer pontos, descontos e comissões sem regras efetivamente ativas.

## 8. Afiliados e monitoramento de promoções

### 8.1 Prioridades

1. **Shopee** — produtos elegíveis às condições reais do programa do usuário.
2. **Mercado Livre** — produtos elegíveis e links rastreáveis válidos.
3. Demais plataformas — apenas quando houver fonte autorizada e, se aplicável, vínculo de afiliado.

Mostrar status real por plataforma: `ativa`, `aguardando credenciais`, `limitada`, `inativa` ou `não suportada`. Não exibir “conectada” sem credenciais validadas.

### 8.2 Pipeline

`Agendador → Fonte autorizada → Normalização → Identificação de produto/variante → Histórico de preço → Verificação do desconto → Scoring → Filtro de interesse → Validação do link afiliado → Distribuição → Métricas`.

- Coletar por APIs oficiais, feeds licenciados ou outros meios permitidos.
- Salvar timestamps e proveniência para cada preço.
- Identificar anúncios duplicados, variações e disponibilidade.
- Considerar frete e cupom quando calculáveis; explicitar limitações.
- Não criar histórico de 30/90 dias antes de existirem observações suficientes.

### 8.3 Canais

- **WhatsApp Business Cloud API:** consentimento explícito, templates aprovados quando necessários, limites e controle de erros/reentrega.
- **E-mail:** provedor transacional/marketing compatível, opt-in, opt-out e logs.
- Notificação enviada ≠ mensagem entregue ≠ mensagem lida; apresentar apenas status confirmados por webhook.

## 9. Arquitetura técnica sugerida

- **Frontend:** Next.js + TypeScript + Tailwind CSS + shadcn/ui; PWA com cache apropriado e atualização controlada.
- **Banco/Auth:** Supabase PostgreSQL, Supabase Auth, políticas RLS e migrations versionadas.
- **Backend:** rotas/API ou servidor Node.js para catálogo, alertas, links externos, pontuação e administração.
- **Coletas/filas:** workers com agendador, controle de taxa por fonte, idempotência, retentativas e dead-letter queue.
- **Integrações:** adaptadores específicos para Shopee, Mercado Livre e plataformas adicionais quando credenciais e permissões forem confirmadas.
- **Mensageria:** WhatsApp Cloud API e fornecedor de e-mail; webhooks assinados/validados.
- **Infra:** frontend hospedado na Vercel; jobs longos/recorrentes executados em infraestrutura apropriada, não em requisições HTTP longas.
- **Segurança:** segredo no servidor, autenticação por papéis, autorização admin, LGPD, mínimo de dados pessoais, auditoria, rate limits, allowlist de destinos e proteção contra fraude de pontos.

### 9.1 Modelo de dados mínimo

| Entidade | Campos relevantes |
|---|---|
| `profiles` | `user_id`, `display_name`, `interests`, `created_at` |
| `stores` | `id`, `name`, `domain`, `status`, `affiliate_enabled` |
| `integrations` | `store_id`, `state`, `last_sync_at`, `last_error`, referência de segredo seguro |
| `products` | `id`, `title`, `brand`, `category`, `normalized_key`, `image_source` |
| `product_variants` | `product_id`, `condition`, `language`, `foil`, `edition`, `set_code`, `card_number` |
| `offers` | `store_id`, `variant_id`, `price`, `currency`, `shipping`, `availability`, `source_url`, `verified_at`, `affiliate_url`, `status` |
| `price_observations` | `offer_id`, `observed_at`, `price`, `source`, `confidence` |
| `alert_rules` | `user_id`, `interests`, `filters`, `channel`, `frequency`, `enabled` |
| `notification_consents` | `user_id`, `channel`, `scope`, `consented_at`, `revoked_at`, evidência |
| `notification_deliveries` | `user_id`, `offer_id`, `status`, `provider_message_id`, `attempts`, timestamps |
| `outbound_clicks` | `user_id`, `offer_id`, `destination`, `click_id`, `eligible`, `created_at` |
| `points_ledger` | `user_id`, `event_key`, `delta`, `reason`, `created_at` |
| `rewards` / `redemptions` | `name`, `points_cost`, `terms`, `user_id`, `state`, `redeemed_at` |
| `affiliate_events` | `store_id`, `click_id`, `conversion_status`, `commission_amount`, `verified_at` |
| `audit_logs` | `actor`, `action`, `target`, `metadata`, `created_at` |

Não armazenar credenciais em texto puro nos registros ou no cliente. Definir índices, constraints, unicidade e políticas RLS antes de publicar.

## 10. Estados, acessibilidade e qualidade

- **Loading:** skeletons com layout estável.
- **Vazio:** “Ainda não encontramos ofertas verificadas para este filtro”; permitir ajustar filtros.
- **Sem histórico:** “Histórico insuficiente para validar o desconto”.
- **Falha da integração:** erro específico no admin, sem esconder indisponibilidade do público.
- **Oferta expirada:** botão desativado ou revalidado; evitar pontuação por oferta inválida.
- **Rede instável:** fallback, retry limitado e PWA informando data da última sincronização.
- **Conformidade:** política de privacidade, consentimentos, transparência de afiliados e preferências de comunicação.

## 11. Contrato do agente orquestrador de prompts

> **Objetivo:** receber cada comando do usuário, transformá-lo em uma instrução precisa e executável, acionar um especialista de desenvolvimento e um especialista QA, e só apresentar a alteração como pronta depois de verificar evidências reais.

### 11.1 Papel e hierarquia

**Agente Orquestrador/Prompt Engineer**

- Tratar a mensagem mais recente do usuário como **mudança incremental**, preservando todos os requisitos anteriores não revogados.
- Separar: (a) alteração solicitada, (b) regras imutáveis, (c) decisões de implementação, (d) critérios verificáveis.
- Não pedir confirmação de detalhes já estabelecidos; completar pequenas lacunas com decisões reversíveis e registrá-las.
- Quando o usuário disser “corrija”, “aplique”, “adicione” ou “remova”, converter em tarefa operacional específica, não apenas conselho textual.
- Nunca interpretar mockup como funcionalidade implementada.
- Se uma nova ordem conflitar com uma regra anterior, priorizar a instrução mais recente **apenas no ponto de conflito**.
- Delegar sempre que possível à dupla **Especialista Fullstack** + **QA**; para visual, incluir **UX/UI**.

### 11.2 Prompt-base para iniciar um agente

```text
Você é o ORQUESTRADOR do projeto BLACK FRIDAY HUNTER.
Fonte de verdade: DESIGN.md + último comando explícito do usuário + arquivos reais do repositório.

Objetivo: transformar a solicitação recebida em mudança implementável e validável.

PROCESSO OBRIGATÓRIO:
1. Leia o DESIGN.md e identifique o escopo exato da mudança.
2. Preserve white mode, marca V4 Poppins, vermelho/preto, menu hambúrguer, hero com Magikarp/scooter e interesses TCG, salvo alteração explícita.
3. Escreva um prompt técnico conciso para um especialista de desenvolvimento, incluindo arquivos prováveis, fluxos, acessibilidade, segurança, responsividade e critérios de aceite.
4. Escreva um prompt independente para QA cobrindo o risco específico da mudança.
5. Se ferramentas e repositório estiverem disponíveis, execute/coordene implementação e testes reais; não simule execução.
6. Antes de solicitar aprovação visual, rode smoke tests rápidos e obtenha evidências desktop/mobile.
7. Se testes falharem, produza correções e reexecute o que for afetado.
8. Entregue relatório: modificado, testado, evidências, pendências, nota justificada (0–10) e status real.

RESTRIÇÕES:
- Não inventar dados reais, integrações ativas, preços, comissões, testes, screenshots ou URLs.
- Não alterar partes não solicitadas sem necessidade técnica declarada.
- Nunca afirmar “aplicado” ou “aprovado” quando apenas um plano/prompt/mockup foi criado.
- Reportar bloqueios de credenciais/ambiente e o próximo passo viável.

ENTRADA: <ÚLTIMO_COMANDO_DO_USUÁRIO>
SAÍDA:
[A] Escopo incremental
[B] Prompt do desenvolvedor
[C] Prompt do QA
[D] Plano de smoke test
[E] Evidências e status, se executado
```

### 11.3 Prompt do especialista Fullstack

```text
Papel: Desenvolvedor Fullstack sênior especialista em Next.js, TypeScript, Tailwind, Supabase, PWA, filas e integrações autorizadas.

Execute somente a alteração delimitada pelo Orquestrador, verificando o código existente antes de editar.
Preserve tokens, branding, responsividade, animação com reduced-motion, integridade de dados e segurança.
Implemente componentes reutilizáveis, estados loading/empty/error, logs e testes relacionados.
Para links externos com pontos, valide no servidor, use idempotência e allowlist; não confunda clique com conversão.
Para WhatsApp, respeite consentimentos, templates e respostas dos webhooks.
Ao concluir, liste arquivos alterados, razão, comandos de validação e limitações reais.
Não marque testes como aprovados sem executá-los.
```

### 11.4 Prompt do especialista QA

```text
Papel: Engenheiro de QA sênior, independente do desenvolvedor.

Receba o diff, DESIGN.md e critérios de aceite. Valide, quando houver ambiente:
- build, lint, typecheck e testes unitários críticos;
- smoke test do fluxo diretamente alterado;
- regressão visual em 390, 768 e 1440 px;
- navegação, foco, contraste, reduced-motion e ausência de overflow;
- consistência com logo V4, white mode e asset aprovado;
- veracidade dos dados, preços, estados das integrações e fontes;
- segurança de redirect, pontuação, consentimento e afiliados quando aplicável.

Registre PASS/FAIL/BLOCKED para cada verificação, com evidência real (logs, screenshot, teste e URL de ambiente quando existir).
Rejeite implementação que ainda apresente falhas de alta gravidade.
Atribua nota 0–10 com justificativa por critério, não por impressão subjetiva.
Nunca aprove com base apenas em mockup estático se a tarefa exigir comportamento real.
```

### 11.5 Ciclo rápido antes da aprovação

**Meta operacional:** feedback inicial em segundos **quando o ambiente e os testes permitirem**, sem prometer tempo fixo nem reduzir cobertura crítica.

1. **0. Interpretação:** analisar comando, gerar prompts e critérios objetivos.
2. **1. Implementação:** alteração isolada pelo especialista.
3. **2. Smoke imediato:** tipo/rota/componente alterado, console, navegação principal e teste de comportamento específico.
4. **3. Visual:** capturas reais em 390/768/1440, comparação com referência e correção de quebras.
5. **4. Segurança/integrações:** validação proporcional ao risco, incluindo casos negativos.
6. **5. Iteração:** FAIL → corrigir → testar novamente; bloqueios devem ser declarados.
7. **6. Aceite:** só classificar como pronto se os testes aplicáveis passaram e não houver defeito crítico.

Smoke tests podem ser rápidos; testes end-to-end externos, webhooks, integrações e performance podem demandar mais tempo. **Nunca substituir testes reais por afirmações.**

## 12. Matriz inicial de QA (aceite visual + funcional)

| ID | Cenário | Resultado esperado |
|---|---|---|
| UI-01 | Home desktop 1440 | White mode, logo V4 legível, sem contagem regressiva, hero sem sobreposições |
| UI-02 | Mobile 390 | Hambúrguer no canto esquerdo, CTA legível, imagem inteira, sem overflow |
| UI-03 | Tablet 768 | Grade adaptada e cards acessíveis |
| UI-04 | Menu | Abre/fecha por clique, Escape e overlay; foco administrado |
| ANI-01 | Entrada da scooter | Trajetória curva, desaceleração, parada final estável |
| ANI-02 | Reduced motion | Sem animação obrigatória; mascote estático no destino |
| PERS-01 | Interesse TCG | Prioriza booster boxes, mini BB/boosters e cartas avulsas |
| PERS-02 | Trocar interesse | Reorganiza home sem perder preferências e sem ofertas inexistentes |
| TCG-01 | Carta avulsa | Identificação de set/número/foil/condição preservada e imagem legítima |
| AFF-01 | Shopee/Mercado Livre | Prioridade comercial sem alterar score de qualidade |
| AFF-02 | Link afiliado | Host autorizado, link válido e disclosure visível |
| PTS-01 | Clique elegível | Um crédito idempotente no ledger; saldo consistente |
| PTS-02 | Clique repetido | Não acumula pontos abusivamente; limites e auditoria |
| PTS-03 | Resgate | Deduz pontos atomicamente; confirma benefício somente após sucesso |
| MSG-01 | WhatsApp sem opt-in | Nenhum envio promocional |
| MSG-02 | WhatsApp com opt-in | Envio conforme regra vigente; estado baseado no provedor |
| DATA-01 | Sem histórico | “Desconto não verificado”; sem porcentagem inventada |
| DATA-02 | Sem integração ativa | Estado correto; nenhum selo fictício de conexão |
| SEC-01 | Redirect malicioso | Bloqueado no backend |

**Peso sugerido da revisão UX/UI:** marca/fidelidade 20%, composição/hierarquia 20%, responsividade 20%, acessibilidade 15%, interação/animação 15%, estados/dados 10%. Uma nota 9,5/10 é **meta de qualidade**, nunca resultado presumido. Bloqueadores funcionais e de segurança impedem aprovação independentemente da nota.

## 13. Critérios para entrega e relato

Todo ciclo de alteração deverá entregar:

1. **Pedido interpretado** — diferenças frente ao estado anterior.
2. **Prompt técnico executado** — objetivo, restrições e critérios.
3. **Artefatos reais** — arquivos/diff/capturas ou, para etapa de conceito, mockup identificado como conceito.
4. **QA** — lista de testes realmente rodados, PASS/FAIL/BLOCKED, evidências e riscos.
5. **Nota fundamentada 0–10** — quando houver material suficiente para avaliar.
6. **Pendências** — credenciais, fontes, APIs, assets ou decisões faltantes.
7. **Status inequívoco:** `DESIGN`, `IMPLEMENTADO SEM VALIDAÇÃO`, `TESTADO COM RESSALVAS` ou `PRONTO PARA APROVAÇÃO`.

### Próximo corte recomendado

**Entrega visual inicial:** home white mode 1440/390 com logo V4, menu hambúrguer fechado, hero com Magikarp e animação curva, seletor de interesse TCG, trilhos de booster boxes/mini BB/cartas avulsas, placeholders honestos, pontos e recompensas. A dupla Desenvolvimento/QA valida a experiência em um protótipo executável antes de propor implementação de integrações de produção.

---

**Nota:** este documento descreve o projeto e seus critérios de execução; não comprova que código, testes automatizados, URLs de afiliado ou envios por WhatsApp já estejam funcionando.