# Design Tokens — L'Essence

Este documento é a **fonte de verdade dos tokens de interface aprovados** para o site institucional da L'Essence. Nenhum valor aqui substitui ou altera os arquivos de `assets/brand/`, que permanecem imutáveis (ver `CLAUDE.md`, Seção 1).

Status: **aprovado** (etapa 3 do processo obrigatório), com as correções desta rodada. Tipografia, grid, HTML e CSS de produção ainda não foram definidos.

---

## A. Identidade oficial imutável

Valores lidos diretamente dos arquivos em `assets/brand/`. Não são tokens de UI — são a matéria-prima de onde os tokens funcionais (Seção B) derivam.

| Nome | Valor | Origem |
|---|---|---|
| `brand-blush` | `#EDDFDC` | `01_paleta/cores-principais.csv` ("Blush claro") |
| `brand-nude` | `#D8B3A0` | `01_paleta/cores-principais.csv` ("Nude") |
| `brand-terracota` | `#B2644D` | `01_paleta/cores-principais.csv` ("Terracota") — **imutável**, continua sendo o acento cromático principal da marca |
| `brand-marrom` | `#54250D` | Fill real de `00_master_simbolo/simbolo-master-marrom.svg` e `02_svg/wordmark-lessence.svg` — continua sendo a tinta principal da marca |
| `brand-preto` | `#000000` | `00_master_simbolo/simbolo-master-preto.svg` — reservado principalmente aos assets/variações oficiais que efetivamente usam preto (símbolo/wordmark "preto", lockups `*-sobre-preto`). Não é mais usado como `bg-inverse` padrão de UI |
| `brand-branco` | `#FFFFFF` | `00_master_simbolo/simbolo-master-branco.svg` |
| `brand-gradient-dourado-simbolo` | gradiente de 7 stops (`#9E6F17 → #F4D778 → #B88321 → #EFCB60 → #B47B17 → #F1CE62 → #A66E13`) | `00_master_simbolo/simbolo-master-dourado.svg` — não portátil, existe só dentro do SVG |
| `brand-gradient-dourado-lockup` | gradiente de 5 stops (`#BD9444 → #F4DBA1 → #EACA7F → #D8AF5C → #9A722D`) | `02_svg/logo-vertical-completo-principal.svg` — não portátil, receita diferente da anterior |

---

## B. Tokens funcionais de UI

### Backgrounds

| Nome | Valor | Origem | Função |
|---|---|---|---|
| `bg-base` | `#FAF1E8` | `neutros-extraidos.csv`, linha 4 coluna 6 | Fundo padrão das seções claras |
| `bg-base-alt` | `#F9EFE5` | `neutros-extraidos.csv`, linha 4 coluna 5 | Alternância sutil entre seções claras adjacentes |
| `bg-inverse` | `brand-marrom` (`#54250D`) | Parte A | Fundo de seções escuras (ex.: bloco de localização/CTA final). **Alterado nesta rodada**: não usa mais `#000000` |
| `bg-brand-blush` | `brand-blush` (`#EDDFDC`) | Parte A | Fundo editorial de marca para uso **seletivo em uma ou poucas seções** — não é o fundo padrão do site |

### Superfícies

| Nome | Valor | Origem | Função |
|---|---|---|---|
| `surface-raised` | `#F1E7DE` | `neutros-extraidos.csv`, linha 3 coluna 6 | Diferenciar um bloco de conteúdo do fundo por tom, sem sombra |
| `surface-brand-nude` | `brand-nude` (`#D8B3A0`) | Parte A | Superfície/acento editorial pontual — não é card genérico, uso intencional e localizado |

`surface-inverse` (`#1A1A1A`) foi **removido** desta rodada — não há necessidade validada de introduzir um near-black funcional novo.

`surface-inverse-subtle` (`brand-branco` a 6% sobre `bg-inverse`) foi introduzido para o placeholder de mapa da seção Localização e depois **removido**: a seção passou a usar `bg-base-alt` com o iframe real do Google Maps, tornando o token sem uso.

### Texto principal

| Nome | Valor | Função |
|---|---|---|
| `text-primary` | `brand-marrom` (`#54250D`) | Texto principal sobre fundo claro |
| `text-primary-inverse` | `brand-branco` (`#FFFFFF`) | Texto principal sobre fundo escuro (`bg-inverse`) |

### Texto secundário

| Nome | Valor | Função |
|---|---|---|
| `text-secondary` | `brand-marrom` a **70%** de opacidade | Legendas, metadados, texto de apoio sobre fundo claro. **Alterado nesta rodada** de 65% → 70% por exigência de contraste (ver Seção Validação) |
| `text-secondary-inverse` | `brand-branco` a 70% de opacidade | Texto de apoio sobre `bg-inverse` |

### Bordas / divisores

| Nome | Valor | Função |
|---|---|---|
| `border-hairline` | `brand-marrom` a 12% de opacidade | Linhas finas entre seções/credenciais, substituindo cards |
| `border-hairline-inverse` | `brand-branco` a 15% de opacidade | Mesma função sobre `bg-inverse` |

### CTA primário

| Nome | Valor | Origem | Função |
|---|---|---|---|
| `cta-primary-bg` | `#A95E47` | **Token funcional derivado**: `brand-terracota` misturado com ~10% de `brand-marrom`. Não substitui `brand-terracota` na identidade oficial | Fundo do botão de conversão principal (WhatsApp) |
| `cta-primary-text` | `#FFFFFF` | Parte A | Texto sobre o CTA primário |

`brand-terracota` (`#B2644D`) puro com texto branco **não é usado** em botões de texto normal: falha WCAG AA (ver Validação). `cta-primary-bg` existe exatamente para resolver isso sem alterar a cor oficial da marca.

### CTA secundário

| Nome | Valor | Função |
|---|---|---|
| `cta-secondary-border` | `brand-marrom` (`#54250D`) | Contorno do botão secundário sobre fundo claro |
| `cta-secondary-text` | `brand-marrom` (`#54250D`) | Texto do botão secundário sobre fundo claro |
| `cta-secondary-border-inverse` | `brand-branco` (`#FFFFFF`) | Contorno do botão secundário sobre `bg-inverse` |
| `cta-secondary-text-inverse` | `brand-branco` (`#FFFFFF`) | Texto do botão secundário sobre `bg-inverse` |

O par `cta-secondary-border`/`text` em marrom **não deve ser usado sobre `bg-inverse`** (marrom sobre marrom = 1:1, ilegível). Sobre fundo escuro, usar sempre a variante `-inverse`.

### Estados hover / focus

| Nome | Valor | Origem | Função |
|---|---|---|---|
| `cta-primary-hover` | `cta-primary-bg` misturado com ~15% de `brand-marrom` (≈ `#9C553E`) | Derivação funcional de `cta-primary-bg` + `brand-marrom` | Escurecimento sutil no hover do CTA primário |
| `cta-secondary-hover-bg` | `brand-marrom` a 6% de opacidade | Derivado de `brand-marrom` | Preenchimento sutil no hover do botão secundário |
| `focus-ring` | `brand-marrom` (`#54250D`), 2px, offset 2px | Parte A | Indicador de foco de teclado em elementos sobre fundo claro |
| `focus-ring-inverse` | `brand-branco` (`#FFFFFF`), 2px, offset 2px | Parte A | Indicador de foco de teclado sobre `bg-inverse` |

Hover é sempre derivado por mistura entre `brand-terracota`/`brand-marrom` — nenhum novo hex "solto" é introduzido fora dessa relação.

### Escala de espaçamento

`space-1` a `space-12`, base 8px: **4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 160, 192px**. Mantida conforme aprovado — sustenta a diretriz de "muito espaço negativo" do CLAUDE.md.

### Sistema de container

| Nome | Valor | Status |
|---|---|---|
| `container-max` | 1440px | **Revisado** (era 1200px) — auditoria de espaço/grid horizontal, validado visualmente em 1440/1536/1600px |
| `page-gutter` | 64px (≥1440px) · 48px (1280–1439px) · 32px (tablet) · 24px (mobile) | Substitui `container-padding-inline`/`margin-lateral` — ver `docs/grid-system.md` Seção 2 |

### Border-radius

| Nome | Valor | Função |
|---|---|---|
| `radius-sharp` | 0px | Padrão: imagens, seções, inputs, blocos estruturais |
| `radius-soft` | 8px | Única exceção documentada, reservada a botões. **Alterado nesta rodada** de 2px → 8px, aprovação explícita do usuário |

### Espessuras de linha

| Nome | Valor | Função |
|---|---|---|
| `line-hairline` | 1px | Divisores padrão |
| `line-emphasis` | 1.5px | Uso pontual (sublinhado ativo em nav, divisor de destaque) |

### Sombras

| Nome | Valor | Status |
|---|---|---|
| `shadow-none` | nenhuma | Padrão da UI |
| `shadow-subtle` | `0 1px 2px rgba(84, 37, 13, 0.08)` | Reservado — só entra em uso **se surgir necessidade concreta** posteriormente (ex.: nav fixa) |

---

## C. Derivações permitidas

Toda cor funcional que não seja um valor da Parte A precisa ser rastreável a uma das operações abaixo — nunca um hex "inventado" isoladamente:

1. **Mistura entre cores oficiais** (`color-mix()` ou equivalente) — ex.: `cta-primary-bg` = `brand-terracota` + ~10% `brand-marrom`; `cta-primary-hover` = `cta-primary-bg` + ~15% `brand-marrom`.
2. **Opacidade sobre uma cor oficial** — ex.: `text-secondary` = `brand-marrom` a 70%; `border-hairline` = `brand-marrom` a 12%.
3. **Amostragem direta da textura oficial** — ex.: `bg-base`, `bg-base-alt`, `surface-raised`, todos lidos de `neutros-extraidos.csv`, não inventados.

Qualquer token novo fora dessas três origens exige aprovação explícita antes de entrar neste documento.

## D. Regras de aplicação

- `brand-terracota` é o único acento de ação da UI. `cta-primary-bg` (sua derivação funcional) é o que efetivamente aparece nos botões — nenhuma segunda cor de destaque deve surgir em outra seção.
- `brand-marrom` é a tinta padrão de texto e bordas em fundo claro.
- `bg-brand-blush` e `surface-brand-nude` existem para reforçar reconhecimento de marca em pontos específicos e intencionais — não são o fundo/superfície padrão do site. Uso sugerido: uma seção editorial isolada (ex.: "Experiência L'Essence") ou um destaque pontual, nunca a repetição em todas as seções.
- Sobre `surface-brand-nude`, o texto deve ser sempre `text-primary` (marrom) — ver Validação: texto branco sobre nude falha contraste gravemente.
- `bg-inverse` (agora `brand-marrom`) é reservado a blocos de fechamento/contraste (ex.: localização + CTA final), não ao corpo geral do site.
- `brand-preto` (`#000000`) só aparece via os próprios assets oficiais que o usam (símbolo/wordmark "preto", lockups `*-sobre-preto`) — não é mais escolhido como cor de fundo de UI.
- `container-max` (1440px) e `page-gutter` foram revisados na auditoria de espaço/grid horizontal — ver `docs/grid-system.md` Seção 2.

## E. Usos proibidos

- Usar `#000000` puro como `bg-inverse` de UI (revertido nesta rodada).
- Introduzir qualquer near-black novo (`#1A1A1A` ou similar) sem necessidade validada.
- Usar `brand-terracota` puro (`#B2644D`) com texto branco normal em botões — falha WCAG AA (4,35:1).
- Usar `text-secondary` a 65% de opacidade — falha WCAG AA (4,23:1); o valor vigente é 70%.
- Usar `cta-secondary` em marrom sobre `bg-inverse` (marrom sobre marrom, ilegível).
- Usar texto branco sobre `surface-brand-nude` (1,93:1, falha gravemente).
- Transformar `bg-brand-blush` no fundo de todas as seções, ou `surface-brand-nude` em card genérico repetido.
- Extrair um hex único do gradiente dourado para uso geral de UI (regra já registrada no CLAUDE.md 1.2, reafirmada aqui).
- Criar qualquer token de cor que não seja rastreável à Parte A ou às derivações da Parte C.

---

## Validação de contraste (WCAG 2.1)

Cálculo por luminância relativa (fórmula padrão WCAG), com blend de opacidade sobre o fundo quando aplicável. Metas: AA texto normal ≥ 4.5:1, AA texto grande ≥ 3.0:1.

| Par | Resultado efetivo | Razão | AA normal (4.5) | AA grande (3.0) | AAA normal (7.0) |
|---|---|---|---|---|---|
| `brand-terracota` puro + branco (**rejeitado**) | `#B2644D` / `#FFFFFF` | 4,35:1 | FALHA | passa | FALHA |
| `cta-primary-text` sobre `cta-primary-bg` | `#FFFFFF` / `#A95E47` | 4,80:1 | **passa** | passa | FALHA |
| `cta-primary-text` sobre `cta-primary-hover` (≈`#9C553E`) | `#FFFFFF` / `#9C553E` | 5,55:1 | passa | passa | FALHA |
| `text-primary` sobre `bg-base` | `#54250D` / `#FAF1E8` | 11,42:1 | passa | passa | passa |
| `text-primary` sobre `bg-base-alt` | `#54250D` / `#F9EFE5` | 11,23:1 | passa | passa | passa |
| `text-primary` sobre `surface-raised` | `#54250D` / `#F1E7DE` | 10,46:1 | passa | passa | passa |
| `text-secondary` 65% sobre `bg-base` (**valor antigo, rejeitado**) | `#8E6C5A` efetivo / `#FAF1E8` | 4,23:1 | FALHA | passa | FALHA |
| `text-secondary` 70% sobre `bg-base` (**valor vigente**) | `#86624F` efetivo / `#FAF1E8` | 4,86:1 | **passa** | passa | FALHA |
| `text-primary-inverse` sobre `bg-inverse` | `#FFFFFF` / `#54250D` | 12,75:1 | passa | passa | passa |
| `text-secondary-inverse` 70% sobre `bg-inverse` | `#CCBEB6` efetivo / `#54250D` | 7,05:1 | passa | passa | passa |
| `cta-secondary-text/border` sobre `bg-base` | `#54250D` / `#FAF1E8` | 11,42:1 | passa | passa | passa |
| `cta-secondary` marrom sobre `bg-inverse` (**inválido, não usar**) | `#54250D` / `#54250D` | 1,00:1 | FALHA | FALHA | FALHA |
| `cta-secondary-*-inverse` (branco) sobre `bg-inverse` | `#FFFFFF` / `#54250D` | 12,75:1 | passa | passa | passa |
| `text-primary` sobre `bg-brand-blush` | `#54250D` / `#EDDFDC` | 9,83:1 | passa | passa | passa |
| `text-primary` sobre `surface-brand-nude` | `#54250D` / `#D8B3A0` | 6,60:1 | passa | passa | FALHA |
| Texto branco sobre `surface-brand-nude` (**não usar**) | `#FFFFFF` / `#D8B3A0` | 1,93:1 | FALHA | FALHA | FALHA |

**Nota sobre bordas (WCAG 1.4.11, componentes não-textuais):** `border-hairline` (marrom 12%) sobre `bg-base` mede ≈1,24:1, abaixo do 3:1 recomendado para componentes de UI essenciais. Como o uso previsto é decorativo/estrutural (divisor entre blocos, não um controle interativo essencial à compreensão), isso não bloqueia esta etapa — mas fica registrado para atenção na implementação: se algum divisor precisar comunicar um limite funcionalmente importante (ex.: borda de um campo de formulário), a opacidade deverá subir o suficiente para atingir 3:1 naquele contexto específico.

**Conclusão:** todos os pares de texto aprovados atingem AA para texto normal. Nenhum par usado como texto de leitura atinge AAA — isso é aceitável para AA (padrão do projeto), não foi exigido AAA.
