# Grid System — L'Essence

Este documento é a **fonte de verdade do sistema de grid aprovado** para o site institucional da L'Essence. Complementa `docs/design-tokens.md` (cores, espaçamento, container, raio) e não altera nada em `assets/brand/`.

Status: **aprovado** (etapa 4 do processo obrigatório), com as 4 correções desta rodada. Tipografia, HTML, CSS e JS de produção ainda não foram definidos.

---

## 1. Breakpoints e colunas

| Breakpoint | Colunas | Gutter (`--gutter`) | Margem lateral (`--page-gutter`) |
|---|---|---|---|
| **Desktop muito largo** (≥1440px) | 12 | 24px | 64px |
| **Desktop** (1280–1439px) | 12 | 24px | 48px |
| **Tablet** (768–1279px) | 8 | 20px | 32px |
| **Mobile** (<768px) | **4 (definitivo, sem sistema alternativo)** | 16px | 24px |

**Regra mobile (correção 1):** não existe um "modo coluna única" separado. Todo elemento full-width em mobile é expresso como `span 4` dentro do grid de 4 colunas — o grid de 4 colunas já produz o efeito de largura total quando um bloco ocupa as 4 colunas. Isso mantém um único sistema de grid em todos os breakpoints, apenas com números de coluna diferentes.

## 2. Container

**Revisado na auditoria de espaço/grid horizontal:** `container-max = 1440px` (antes 1200px — o valor antigo, somado ao padrão antigo de `max-width` + `padding-inline` interno, desperdiçava largura útil em telas grandes; validado visualmente antes de congelar).

Fórmula única, usada por toda seção **contida** (classe `.container`, reutilizada por Navbar, Hero, Sobre e qualquer seção futura não-imersiva):

```css
.container {
  width: min(calc(100% - 2 * var(--page-gutter)), var(--container-max));
  margin-inline: auto;
}
```

Isso substitui o padrão antigo (`max-width: container-max` + `padding-inline: margem` no mesmo elemento), que descontava a margem duas vezes. Com a fórmula única, a margem lateral (`--page-gutter`) só "aparece" como espaço vazio quando o viewport é mais estreito que `container-max + 2 × page-gutter`; em telas muito largas (1920px+), o container trava em 1440px e o excedente vira margem externa simétrica — sem esticar o conteúdo infinitamente.

## 3. Regras full-bleed (exceção, não padrão)

- **Full-bleed deixou de ser o padrão.** Por definição, toda seção é **contida** (`.container`) a menos que esteja explicitamente marcada como imersiva.
- Seções imersivas aprovadas para romper o container: Hero **não** é uma delas (contido); Experiência L'Essence, painéis fotográficos específicos e o bloco de mapa/localização podem usar full-bleed (100vw) quando implementados.
- **Sobre e Serviços:** Sobre é contida (mosaico de fotos não encosta na borda do viewport, respeita `--page-gutter` como qualquer outra seção). Serviços permanece full-bleed (díptico fotográfico grande, já aprovado) — é a única seção de conteúdo, além das futuras imersivas, que rompe o container.
- Fotografia de conteúdo (mosaico da Dra. Valéria, fotos de Serviços) nunca é "parcialmente" full-bleed: ou está contida no grid/container, ou sangra deliberadamente até a borda do viewport — nunca os dois ao mesmo tempo.
- **Sangria direcional (correção 3, mantida):** quando uma seção imersiva futura dividir texto + imagem (ex.: mapa/localização), a sangria acontece apenas do lado externo da composição, nunca em direção ao bloco de texto. Isso preserva a "coluna-espinha" de alinhamento editorial (Seção 4).
- Em mobile, seções full-bleed continuam full-bleed (100vw); seções contidas usam a mesma `.container` com `--page-gutter: 24px`.

## 4. Regras editoriais

- Sem centralização de bloco de texto como padrão (Anti-Center-Bias). Headlines e corpo alinham à esquerda, ancorados a uma coluna real do grid.
- **Coluna-espinha**: a borda esquerda dos blocos de texto mantém-se no mesmo eixo vertical ao longo de toda a página, mesmo quando a composição visual (fotografia, sangria, proporção) muda de seção para seção.
- Proibido o padrão "headline grande à esquerda + parágrafo explicativo flutuando no canto superior direito" (Split-Header Ban). Headline + corpo sempre empilhados na mesma coluna, largura máxima de leitura ~65ch.
- Eyebrows usados com parcimônia: no máximo 3 no total das 8 seções, nunca em seções consecutivas.
- Nenhuma seção usa proporção literalmente 50/50 nas divisões de conteúdo (exceto o díptico de Serviços — ver Seção 5, item 4 — que é intencionalmente simétrico por tratar dois pilares de mesmo peso institucional).

## 5. Comportamento das 8 seções

### 1. NAV
Logo em 2–3 colunas à esquerda, links centrais no miolo, CTA em 2 colunas à direita. Altura ≤80px, uma linha. Idêntico em todos os breakpoints (colapsa para menu compacto em mobile, mantendo altura ≤80px).

### 2. HERO — split assimétrico
Desktop: texto (eyebrow + headline + subtexto + CTA) em 7/12 à esquerda; símbolo/fotografia em 5/12 à direita.
Tablet: 5/8 texto, 3/8 símbolo/foto.
Mobile: empilhado — texto primeiro (`span 4`), símbolo/foto depois (`span 4`).

### 3. SOBRE A DRA. VALÉRIA — mosaico + conteúdo, seção CONTIDA (revisado na auditoria de espaço)
Desktop: seção usa `.container` (não é mais full-bleed). Mosaico fotográfico 2×2 em ~5/12 à esquerda, conteúdo (eyebrow + headline + texto, depois credenciais) em ~7/12 à direita, gap estrutural entre as duas áreas. Mosaico e coluna de conteúdo terminam na mesma altura (stretch natural do grid, sem height fixa). O mosaico **não** encosta na borda do viewport — respeita a mesma margem lateral (`--page-gutter`) que Hero e Navbar usam, ficando alinhado ao mesmo eixo esquerdo. `border-hairline` entre linhas de credencial — sem cards.
Tablet: mesma proporção de colunas, gap reduzido.
Mobile: empilhado — eyebrow, headline, texto, mosaico 2×2 (1 coluna abaixo de ~390px), credenciais — nessa ordem, dentro do mesmo `.container` (sem full-bleed).

### 4. SERVIÇOS — díptico horizontal (correção 2)
**Desktop:** dois pilares lado a lado, cada um **6/12**:
- Estética do Sorriso = 6/12 (esquerda)
- Estética Facial = 6/12 (direita)

Cada pilar é uma composição fotográfica/editorial grande (heading + imagem), **não um card** — sem borda fechada, sem sombra, sem fundo de superfície delimitando um retângulo. A separação entre os dois pilares é apenas o gutter do grid (ou uma linha fina vertical opcional), nunca uma moldura. Cada painel pode romper para full-bleed vertical dentro da própria coluna que ocupa (a foto do pilar pode encostar no topo/base da seção), mas não invade a coluna do pilar vizinho.

**Tablet:** os dois pilares permanecem lado a lado (4/8 + 4/8) enquanto houver espaço visual suficiente para leitura confortável do heading e da imagem; é o próprio conteúdo (tamanho mínimo de heading legível) que determina o ponto de colapso, não um breakpoint arbitrário adicional.

**Mobile:** os dois pilares empilham verticalmente, cada um em `span 4`, na ordem Estética do Sorriso → Estética Facial, cada um full-bleed horizontalmente na fotografia e com heading em bloco inset.

### 5. EXPERIÊNCIA L'ESSENCE — bloco imersivo full-width
Fotografia de atmosfera 100vw com citação curta ancorada em uma coluna contida (não centralizada) sobre a imagem. Idêntico em intenção em todos os breakpoints; em mobile o texto ancora na parte inferior do bloco para não competir com a leitura da imagem em telas estreitas.

### 6. PROVA SOCIAL — stack editorial de citações
Desktop: um depoimento em destaque (6/12) + dois depoimentos menores (3/12 cada), lado a lado.
Tablet: depoimento em destaque em 8/8 (largura total), os dois menores em 4/8 + 4/8 abaixo.
Mobile: todos empilhados em `span 4`, depoimento em destaque primeiro.

### 7. LOCALIZAÇÃO + CTA FINAL — split contido (correção 3, revisado após integração do mapa real)
**Desktop:**
```
[ Label / headline / texto / endereço / CTA ]  |  [   MAPA (iframe, contido)   ]
                  5/12                                      7/12
```
Informações (label, headline, texto, endereço, CTA WhatsApp) = **5/12 à esquerda**. Mapa (iframe do Google Maps) = **7/12 à direita**, altura fixa compacta (~450px desktop) — **revisado**: a versão original previa o mapa rompendo o container e sangrando até a borda direita do viewport; na implementação com o iframe real isso deixou a seção pesada e "app-like", então o mapa passou a ficar **contido dentro do mesmo `.container` global** das demais seções, sem sangria.

Tablet: informações em 3/8, mapa em 5/8, mesma altura compacta, ainda dentro do container.

**Mobile** (revisado na implementação — ordem definida explicitamente pelo usuário): conteúdo primeiro, mapa por último. Ordem: label editorial → headline → texto → endereço → CTA WhatsApp → mapa full-bleed (sangra a margem lateral, sem overflow horizontal). CTA fica antes do mapa, não depois — o CTA é o fechamento textual da seção, o mapa é o elemento visual final.

### 8. FOOTER — grid institucional (correção 4)
Footer **visual**, 3 colunas em desktop (cada uma 4/12), empilhadas em mobile (`span 4` cada):
- Marca / institucional
- Contato / redes
- Localização

Rodapé inferior (abaixo das 3 colunas, seção estreita full-width): copyright, CRO e informações legais quando aplicável.

**Não existe** uma coluna visual chamada "SEO/GEO". Schema.org, JSON-LD, meta tags e dados estruturados são implementação técnica no `<head>`/markup semântico do código — não um bloco de conteúdo visível ao usuário.

---

## 6. Wireframes (corrigidos)

### Desktop

```
┌──────────────────────────────────────────────────────────┐
│ [Logo]         [Link Link Link Link]           [CTA WA]   │ NAV
├──────────────────────────────────────────────────────────┤
│ EYEBROW                          │                        │
│ Headline grande                  │    [Símbolo / foto]    │ HERO
│ subtexto · [CTA]                 │                        │
├──────────────────────────────────────────────────────────┤
│ [ Foto editorial grande  ]  │  Apresentação                │ SOBRE
│ [    (sangra à esquerda) ]  │  ── credencial                │
│                              │  ── credencial                │
├──────────────────────────────────────────────────────────┤
│  ESTÉTICA DO SORRISO          │  ESTÉTICA FACIAL             │
│ [   painel fotográfico   ]    │ [   painel fotográfico    ]  │ SERVIÇOS
│ [       6/12              ]    │ [        6/12              ]  │ (díptico)
├──────────────────────────────────────────────────────────┤
│ [============ foto de atmosfera full-bleed ==============] │
│              "citação curta ancorada"                       │ EXPERIÊNCIA
├──────────────────────────────────────────────────────────┤
│  ┌────────────────────┐   ┌───────────┐  ┌───────────┐    │
│  │ depoimento em       │   │depoimento │  │depoimento │    │ PROVA SOCIAL
│  │ destaque (6/12)     │   │  (3/12)   │  │  (3/12)   │    │
│  └────────────────────┘   └───────────┘  └───────────┘    │
├──────────────────────────────────────────────────────────┤
│ Endereço             │ [======= MAPA (sangra à direita) ===]│ LOCALIZAÇÃO
│ Horários              │ [==================================]│ + CTA FINAL
│ [CTA WA]               │ [==================================]│
│      5/12                            7/12                    │
├──────────────────────────────────────────────────────────┤
│ Marca / institucional │  Contato / redes │  Localização      │ FOOTER
│──────────────────────────────────────────────────────────│
│           copyright · CRO · informações legais              │
└──────────────────────────────────────────────────────────┘
```

### Mobile (grid de 4 colunas, blocos full-width em span 4)

```
┌───────────────────┐
│ [Logo]      [☰/CTA]│ NAV
├───────────────────┤
│ EYEBROW             │
│ Headline             │ HERO
│ subtexto             │
│ [CTA WhatsApp]       │
│ [Símbolo/foto]       │
├───────────────────┤
│ [foto full-bleed]    │
│ Apresentação          │ SOBRE
│ ── credencial         │
│ ── credencial         │
├───────────────────┤
│ ESTÉTICA DO SORRISO   │
│ [foto full-bleed]     │ SERVIÇOS
│ ESTÉTICA FACIAL       │ (empilhado)
│ [foto full-bleed]     │
├───────────────────┤
│ [foto full-bleed]     │
│ "citação"              │ EXPERIÊNCIA
├───────────────────┤
│ depoimento em destaque │
│ depoimento 2            │ PROVA SOCIAL
│ depoimento 3            │
├───────────────────┤
│ Label · Headline · Texto  │
│ Endereço                   │ LOCALIZAÇÃO
│ [CTA WhatsApp]              │ + CTA FINAL
│ [mapa contido, ~340px alt.]  │
├───────────────────┤
│ Marca / institucional      │
│ Contato / redes             │ FOOTER
│ Localização                  │
│──────────────────────│
│ copyright · CRO · legal       │
└───────────────────┘
```
