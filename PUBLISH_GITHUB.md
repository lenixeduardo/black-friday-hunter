# Publicar o repositório Black Friday Hunter no GitHub

**Nome escolhido:** `black-friday-hunter`

**Proprietário esperado:** `lenixeduardo`

**Descrição:** Plataforma de monitoramento de promoções, afiliados e alertas personalizados com foco em Shopee, Mercado Livre e TCG.

## Opção A — GitHub CLI (recomendada)

O projeto já é um repositório Git com a branch `main` e histórico preservado. No computador com GitHub CLI instalado e autenticado, execute na pasta deste projeto:

```bash
gh auth login
gh repo create lenixeduardo/black-friday-hunter --private --source=. --remote=origin --push
```

O comando cria o repositório privado, associa o remoto e envia a branch atual. Escolha `--public` somente se desejar tornar o código público.

## Opção B — Site + Git

1. Abra https://github.com/new e crie um repositório **vazio**, denominado `black-friday-hunter`, no perfil `lenixeduardo`. Não marque README, .gitignore ou licença, porque estes arquivos já estão no projeto.
2. No diretório local do projeto, execute:

```bash
git remote add origin https://github.com/lenixeduardo/black-friday-hunter.git
git push -u origin main
```

## Validar

```bash
git remote -v
git status -sb
python -m pytest -q
```

Depois de publicar, verifique a aba Actions e acompanhe o workflow `Black Friday Hunter QA`.

## Importante

A integração GitHub disponível no ChatGPT nesta sessão não oferece ação de criação de repositório, portanto a publicação remota não foi executada. O projeto não contém as integrações reais de lojas/WhatsApp e não deve ser divulgado como MVP completo.