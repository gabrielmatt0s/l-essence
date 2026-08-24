# L'Essence — Site Institucional

Fonte permanente de instruções para todo o desenvolvimento do site institucional da L'Essence. Este documento tem prioridade sobre preferências genéricas de estilo ou produtividade quando houver conflito.

## 1. Fonte de verdade da identidade visual

Os arquivos oficiais da identidade visual da L'Essence são **imutáveis**.

Quando forem adicionados ao projeto, a pasta `assets/brand/` será a **única fonte de verdade** para logos, símbolos, cores e assets oficiais.

É terminantemente proibido:

- redesenhar o símbolo;
- revectorizar o símbolo;
- simplificar o SVG;
- suavizar novamente o SVG;
- alterar paths;
- alterar proporções;
- modificar viewBox para deformar o desenho;
- recriar o logo com CSS;
- substituir o lettering por uma fonte parecida;
- gerar uma nova versão do logo;
- modificar os arquivos oficiais para facilitar animações.

Para aplicações diferentes, usar os arquivos oficiais existentes. Se uma animação exigir manipulação do símbolo, preservar integralmente sua geometria original.

### 1.1 Animação do símbolo oficial

O SVG oficial **nunca** pode sofrer morph ou alteração de geometria durante animações.

São **permitidos** somente efeitos que preservem integralmente o path original:

- opacity;
- transform;
- translate;
- scale uniforme;
- clip-path/mask;
- reveal;
- animação do container.

São **proibidos**:

- morph;
- alteração de path `d`;
- skew;
- deformação;
- alteração de proporção;
- reconstrução de stroke;
- qualquer técnica que modifique visualmente a geometria oficial.

### 1.2 Uso do dourado oficial

Não existe um token universal chamado "gold" ou "dourado" para substituir os gradientes presentes nos SVGs.

Os gradientes internos dos assets oficiais devem permanecer exatamente como estão.

Não extrair uma única cor intermediária do gradiente para substituir o dourado oficial dos logos.

O dourado **não será usado automaticamente** como:

- cor de texto;
- fundo;
- CTA;
- borda de cards;
- decoração recorrente.

Qualquer uso de dourado fora dos assets oficiais deverá ser definido e aprovado especificamente na etapa de design tokens/UI.

### 1.3 Tokens de interface

`docs/design-tokens.md` é a **fonte de verdade** dos tokens de interface aprovados (cores funcionais, espaçamento, container, raio, linhas, sombras). Este arquivo (CLAUDE.md) continua sendo a fonte de verdade da identidade visual oficial; `docs/design-tokens.md` documenta como essa identidade é aplicada na UI.

### 1.4 Sistema de grid

`docs/grid-system.md` é a **fonte de verdade** do sistema de grid aprovado (breakpoints, colunas, gutters, margens, container, regras full-bleed/editoriais e comportamento das 8 seções da homepage).

## 2. Direção do projeto

Site institucional premium da **L'Essence by Dra. Valéria Oliveira**.

Localização: Batel, Curitiba - PR.

Objetivos principais:

1. posicionamento e autoridade;
2. apresentar a clínica e a Dra. Valéria;
3. comunicar estética com naturalidade;
4. apresentar os dois pilares de atuação;
5. demonstrar experiência e acolhimento;
6. usar prova social real;
7. converter visitantes para WhatsApp.

A identidade **não deve parecer**:

- template de clínica;
- template gerado por IA;
- SaaS;
- dashboard;
- landing page genérica;
- clínica genérica bege e dourada;
- site de joalheria;
- página baseada em excesso de cards.

Direção desejada: editorial, sofisticada, feminina sem clichês, contemporânea, minimalista, premium, quente, clínica, com muito espaço negativo, hierarquia tipográfica forte, fotografia como elemento relevante, detalhes extremamente controlados.

## 3. Arquitetura obrigatória

A homepage seguirá esta arquitetura:

### NAV

Logo à esquerda. Links centrais. CTA WhatsApp à direita.

### HERO

- Eyebrow: `L'ESSENCE · BATEL`
- Headline principal: `Realce sua beleza sem perder sua essência.`
- Texto de apoio.
- CTA WhatsApp.
- Uso do símbolo oficial como elemento visual e/ou animação.

### SOBRE A DRA. VALÉRIA

Foto editorial. Apresentação. Credenciais profissionais em composição fina e editorial. **Não usar cards** para credenciais.

### SERVIÇOS

Somente dois pilares principais:

1. Estética do Sorriso
2. Estética Facial

Não transformar a seção em grid genérico de vários procedimentos. Procedimentos individuais podem aparecer como conteúdo secundário dentro dos respectivos pilares.

### EXPERIÊNCIA L'ESSENCE

Comunicar: acolhimento, ambiente, cuidado, tranquilidade, atendimento humano, tecnologia, experiência da clínica. Basear a comunicação no que pacientes reais destacam.

### PROVA SOCIAL

Depoimentos reais do Google. Priorizar poucos relatos fortes e legíveis. Não criar carrossel genérico apenas para exibir grande quantidade de avaliações.

### LOCALIZAÇÃO + CTA FINAL

Batel. Endereço. Mapa. Horários. CTA forte para WhatsApp.

### FOOTER

Informações institucionais. Contato. Instagram. Dados profissionais. SEO/GEO.

## 4. Princípios de UI

**Aplicar**: composição editorial, grid consistente, grandes áreas de respiro, ritmo vertical, contraste claro de hierarquia, linhas finas, microdetalhes controlados, botões sofisticados e claros, responsividade real, estados hover/focus coerentes, componentes reduzidos ao necessário.

**Evitar**: excesso de cards, glassmorphism, sombras genéricas, bordas arredondadas excessivas, pills gratuitas, blobs decorativos, gradientes inventados, excesso de ícones, textos centralizados em todas as seções, layouts repetitivos, emojis, elementos visuais sem função, excesso de dourado.

Dourado deve funcionar como acabamento e detalhe, não como tinta dominante.

## 5. Desenvolvimento

Stack principal: HTML semântico, CSS, JavaScript, GSAP quando necessário.

Não adicionar React, Next.js ou frameworks sem necessidade técnica clara e aprovação explícita.

Organizar CSS usando design tokens.

Priorizar: simplicidade estrutural, manutenção, semântica, acessibilidade, performance, responsividade, Core Web Vitals.

## 6. Skills obrigatórias

Antes de definir visualmente uma nova área relevante, considerar e utilizar:

- `frontend-design:frontend-design`
- `design-taste-frontend`

A skill `frontend-design:frontend-design` é **obrigatória** nas principais revisões visuais.

As recomendações das skills **nunca** possuem autoridade para modificar a identidade visual oficial.

### Animações

Quando necessário, utilizar: `gsap-core`, `gsap-timeline`, `gsap-scrolltrigger`, `gsap-performance`.

Movimento deve ter função. Não adicionar animações apenas porque são possíveis.

### QA

Após implementação:

- usar `run`;
- realizar inspeção visual;
- usar `claude-in-chrome` quando disponível;
- testar desktop, tablet, mobile;
- navegação por teclado;
- estados interativos;
- links;
- WhatsApp;
- console.

### Código

Antes de commits relevantes: `simplify`, `code-review`, ferramentas relevantes do `pr-review-toolkit`.

Antes de deploy: `security-review`.

Utilizar `commit-commands` para fluxo Git quando apropriado.

## 7. SEO e GEO

Mesmo sem skill dedicada, revisar manualmente:

`<title>`, meta description, canonical, Open Graph, semântica HTML, headings, alt text, sitemap.xml, robots.txt, dados estruturados, schema.org (Dentist, LocalBusiness), endereço, telefone, horários, localização, links sociais.

O conteúdo deve ser compreensível também por mecanismos generativos e crawlers. Não fazer keyword stuffing.

## 8. Acessibilidade

Mesmo sem skill dedicada:

contraste adequado, navegação por teclado, foco visível, HTML semântico, labels, aria somente quando necessário, alt text adequado, áreas de toque, `prefers-reduced-motion`, evitar dependência exclusiva de cor.

## 9. Performance

Mesmo sem skill dedicada de Lighthouse, priorizar:

imagens WebP/AVIF, dimensões explícitas, lazy loading quando apropriado, preload somente de recursos críticos, evitar JavaScript desnecessário, evitar layout shift, fontes otimizadas, animações GPU-friendly, minimizar custo de GSAP, Core Web Vitals.

## 10. Processo obrigatório

Não desenvolver a homepage inteira de uma única vez.

Fluxo:

1. entender os assets;
2. analisar a identidade;
3. definir design tokens;
4. definir grid;
5. definir tipografia;
6. criar NAV + HERO;
7. executar frontend-design;
8. executar design-taste-frontend;
9. revisar;
10. obter aprovação;
11. seguir para próxima seção;
12. repetir revisão;
13. construir responsivo;
14. QA;
15. performance;
16. acessibilidade;
17. SEO/GEO;
18. code review;
19. security review;
20. commit/deploy.

Não avançar várias etapas importantes sem validação.

## 11. Regra contra decisões inventadas

Quando informação real estiver faltando: **NÃO inventar**. Isso inclui: procedimentos, formação, credenciais, números, telefone, endereço, avaliações, frases atribuídas a pacientes, fotos, horários, certificações, premiações.

Usar placeholder claramente identificado ou solicitar o dado.

## 12. Regra final

Fidelidade de marca possui prioridade sobre criatividade arbitrária.

Qualidade visual possui prioridade sobre quantidade de elementos.

Clareza possui prioridade sobre efeito.

Experiência possui prioridade sobre decoração.
