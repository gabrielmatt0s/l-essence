# General Sans — arquivos pendentes

A fonte de corpo/interface do site (`--font-body`) é **General Sans**
(Indian Type Foundry / Fontshare). O projeto carregava essa fonte pela
API do Fontshare (`api.fontshare.com`), mas essa API está atualmente
retornando erro ("Access to the Fontshare API has been temporarily
restricted") em vez do CSS da fonte — por isso o site inteiro estava
caindo na fonte de fallback do sistema (`-apple-system` / `Segoe UI`).

`styles.css` já tem as regras `@font-face` prontas, apontando para os
arquivos abaixo, que ainda não existem neste diretório:

```
assets/fonts/general-sans/GeneralSans-Regular.woff2   (peso 400)
assets/fonts/general-sans/GeneralSans-Medium.woff2    (peso 500)
```

## Como resolver

1. Baixar os arquivos self-hosted diretamente em
   https://www.fontshare.com/fonts/general-sans (botão "Get font" →
   "Download family" ou "Get embed code" → self-host), respeitando a
   licença da Indian Type Foundry.
2. Do pacote baixado, copiar apenas os pesos **Regular (400)** e
   **Medium (500)** em formato `.woff2` para esta pasta, com exatamente
   esses nomes de arquivo.
3. Nenhuma outra alteração é necessária — as regras `@font-face` em
   `styles.css` e o `--font-body` já apontam para cá.

Até isso ser feito, o site continua funcional, só que exibindo a fonte
de fallback do sistema em vez de General Sans.
