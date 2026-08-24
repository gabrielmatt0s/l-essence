# L'Essence — identidade visual FINAL V2 — curvas lisas

## Revisão cirúrgica solicitada
Esta versão substitui a revisão anterior e mantém a geometria aprovada, com correção localizada de duas irregularidades visuais apontadas pelo usuário:

1. transição superior interna do traço, próxima à curva do topo;
2. início da curva inferior esquerda do perfil/pescoço.

As correções foram feitas diretamente nas curvas Bézier, sem aplicar filtro global e sem redesenhar o restante do símbolo.

## Regra do pacote
- um único master vetorial do símbolo;
- todas as variações (dourado, branco, preto e marrom) reutilizam a mesma geometria;
- todos os logos completos e sem descritor usam o mesmo master normalizado;
- SVGs usam curvas Bézier cúbicas;
- PNGs são renderizações dos SVGs corrigidos;
- arquivos de wordmark sem símbolo foram mantidos inalterados.

## Fonte de verdade
`00_master_simbolo/REFERENCIA_MESTRA_USUARIO.png`

## Validação visual
Veja a pasta `05_validacao/`, especialmente:
- `comparacao-antes-depois-curvas.png`
- `correcao-topo-ampliada.png`
- `correcao-curva-inferior-ampliada.png`
- `preview-logo-completo.png`

## Observação técnica
A referência fornecida é raster. O objetivo desta revisão é preservar a forma visual da referência e eliminar irregularidades de vetorização, sem converter serrilhado de pixel em geometria.
