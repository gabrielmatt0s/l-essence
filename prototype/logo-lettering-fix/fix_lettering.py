"""
Limpeza vetorial do lettering do descritor (BY DRA. VALERIA OLIVEIRA / CIRURGIA-DENTISTA & HOF).

Pipeline por subpath (= por letra/contraforma), operando sobre o poligono
denso original (so M/L/Z -- confirmado que essas duas linhas nao usam
curvas, sao auto-trace puro de raster):

  1. deteccao de cantos: angulo de virada calculado com vizinhanca por
     comprimento de arco (nao por contagem de pontos, que seria sensivel
     a densidade irregular do trace). Pontos com angulo de virada acima
     do limiar sao marcados como cantos e NUNCA suavizados/removidos --
     preserva serifas e junções que devem continuar agudas.
  2. suavizacao por media movel (janela por comprimento de arco) aplicada
     SOMENTE nos trechos entre cantos -- remove o ruido de alta frequencia
     (dentes/micro-picos) preservando a curvatura real de baixa frequencia
     da letra. RDP sozinho nao faz isso: ele preserva qualquer desvio
     maior que a tolerancia, entao ruido de amplitude maior que a
     tolerancia simplesmente permanece codificado com menos pontos.
  3. RDP indexado sobre a sequencia ja suavizada, para reduzir o numero
     de nos a um conjunto minimo que ainda descreve a forma.
  4. ajuste de 1 Bezier cubica por trecho entre nos consecutivos
     (mínimos quadrados, tangentes estimadas por regressao local nas
     pontas do trecho -- estavel mesmo com poucos pontos), ou reta pura
     quando o trecho already for essencialmente reto.

So os paths correspondentes as duas linhas do descritor sao tocados.
O simbolo (path[0]) e o wordmark L'ESSENCE (path[1]) sao copiados
byte-a-byte do arquivo original.
"""

import re
import numpy as np

SRC = "logo-vertical-completo-principal.ORIGINAL.svg"
DST = "logo-vertical-completo-principal.CORRECTED.svg"

PRESMOOTH_RADIUS = 0.20       # suavizacao leve (sem barreira de canto) so p/ tirar o jitter de altissima frequencia
CORNER_ANGLE_DEG = 30.0       # abaixo disso nao e canto (curva suave normal de letra)
CORNER_LOOKAROUND = 0.5       # calibrado empiricamente: pequeno o suficiente p/ nao confundir curvas
                               # apertadas (bojo de letras pequenas) com cantos verdadeiros
SMOOTH_RADIUS = 0.45          # reduzido: raio anterior (1.1) colapsava serifas finas em si mesmas
                               # (self-intersection). Serifas tem poucas unidades de largura.
RDP_TOLERANCE = 0.10          # unidades do viewBox, aplicado DEPOIS da suavizacao
STRAIGHT_TOLERANCE = 0.06


def parse_subpaths(d):
    subpaths_raw = re.findall(r"M[^M]*", d)
    subpaths = []
    for raw in subpaths_raw:
        nums = re.findall(r"-?\d+\.?\d*", raw)
        pts = [(float(nums[i]), float(nums[i + 1])) for i in range(0, len(nums) - 1, 2)]
        clean = [pts[0]]
        for p in pts[1:]:
            if p != clean[-1]:
                clean.append(p)
        if clean[0] == clean[-1] and len(clean) > 1:
            clean = clean[:-1]
        subpaths.append(np.array(clean, dtype=float))
    return subpaths


def arc_lengths(points_closed):
    """Comprimento acumulado ao longo do poligono fechado (points[0..n-1], retorna a n)."""
    n = len(points_closed)
    diffs = np.diff(np.vstack([points_closed, points_closed[:1]]), axis=0)
    seg = np.hypot(diffs[:, 0], diffs[:, 1])
    return np.concatenate([[0.0], np.cumsum(seg)])  # tamanho n+1, cum[n] = perimetro


def neighbor_by_arclen(cum, total, i, n, dist, direction):
    """Indice do ponto a 'dist' de comprimento de arco de i, para frente (+1) ou para tras (-1)."""
    target = (cum[i] + direction * dist) % total
    # busca no array cum (tamanho n+1, cum[0..n-1] valores crescentes, cum[n]=total)
    idx = np.searchsorted(cum[:n], target % total)
    idx = idx % n
    return idx


def detect_corners(points):
    n = len(points)
    if n < 6:
        return np.ones(n, dtype=bool)
    cum = arc_lengths(points)
    total = cum[n]
    corners = np.zeros(n, dtype=bool)
    for i in range(n):
        j_back = neighbor_by_arclen(cum, total, i, n, CORNER_LOOKAROUND, -1)
        j_fwd = neighbor_by_arclen(cum, total, i, n, CORNER_LOOKAROUND, +1)
        v_in = points[i] - points[j_back]
        v_out = points[j_fwd] - points[i]
        n_in = np.linalg.norm(v_in)
        n_out = np.linalg.norm(v_out)
        if n_in < 1e-9 or n_out < 1e-9:
            continue
        cos_a = np.clip(np.dot(v_in, v_out) / (n_in * n_out), -1.0, 1.0)
        angle = np.degrees(np.arccos(cos_a))
        if angle > CORNER_ANGLE_DEG:
            corners[i] = True
    return corners


def smooth_uniform_closed(points, radius):
    """Media movel simples (sem barreira de canto) -- so p/ denoise de altissima
    frequencia antes da deteccao de canto, que precisa de direcoes estaveis."""
    n = len(points)
    cum = arc_lengths(points)
    total = cum[n]
    out = points.copy()
    for i in range(n):
        acc = [points[i]]
        j = i
        while True:
            j_prev = (j - 1) % n
            if ((cum[i] - cum[j_prev]) % total) > radius:
                break
            acc.append(points[j_prev])
            j = j_prev
            if j == i:
                break
        j = i
        while True:
            j_next = (j + 1) % n
            if ((cum[j_next] - cum[i]) % total) > radius:
                break
            acc.append(points[j_next])
            j = j_next
            if j == i:
                break
        out[i] = np.mean(acc, axis=0)
    return out


def smooth_closed(points, corners):
    """Media movel por janela de comprimento de arco, mas cada ponto so 'enxerga'
    vizinhos ate encontrar um canto (cantos atuam como barreira, nunca sao cruzados
    nem alterados). Distancias por comprimento de arco tratadas em modulo do
    perimetro para lidar corretamente com o wraparound do poligono fechado."""
    n = len(points)
    cum = arc_lengths(points)  # tamanho n+1; cum[i] = arco acumulado ate points[i]; cum[n] = perimetro
    total = cum[n]
    out = points.copy()

    for i in range(n):
        if corners[i]:
            continue
        acc = [points[i]]

        j = i
        while True:
            j_prev = (j - 1) % n
            dist_back = (cum[i] - cum[j_prev]) % total
            if corners[j_prev] or dist_back > SMOOTH_RADIUS:
                break
            acc.append(points[j_prev])
            j = j_prev
            if j == i:
                break

        j = i
        while True:
            j_next = (j + 1) % n
            dist_fwd = (cum[j_next] - cum[i]) % total
            if corners[j_next] or dist_fwd > SMOOTH_RADIUS:
                break
            acc.append(points[j_next])
            j = j_next
            if j == i:
                break

        out[i] = np.mean(acc, axis=0)
    return out


def _point_line_dists(points, start, end):
    line_vec = end - start
    line_len = np.hypot(*line_vec)
    if line_len == 0:
        return np.hypot(*(points - start).T)
    line_unit = line_vec / line_len
    vecs = points - start
    proj = np.outer(vecs @ line_unit, line_unit)
    perp = vecs - proj
    return np.hypot(perp[:, 0], perp[:, 1])


def rdp_indices(points, idx, epsilon):
    if len(idx) < 3:
        return list(idx)
    start, end = points[0], points[-1]
    dists = _point_line_dists(points[1:-1], start, end) if len(points) > 2 else np.array([])
    if len(dists) == 0:
        return [idx[0], idx[-1]]
    local_i = int(np.argmax(dists))
    dmax = dists[local_i]
    i = local_i + 1
    if dmax > epsilon:
        left = rdp_indices(points[: i + 1], idx[: i + 1], epsilon)
        right = rdp_indices(points[i:], idx[i:], epsilon)
        return left[:-1] + right
    return [idx[0], idx[-1]]


def rdp_closed_indices(points, corners, epsilon):
    n = len(points)
    if n < 4:
        return list(range(n))
    forced = set(np.where(corners)[0].tolist())
    if len(forced) < 2:
        i0 = int(np.argmin(points[:, 0]))
        i1 = int(np.argmax(points[:, 0]))
        if i0 == i1:
            i1 = (i0 + n // 2) % n
        forced = {i0, i1}

    anchors = sorted(forced)

    def arc_idx(a, b):
        if a <= b:
            return list(range(a, b + 1))
        return list(range(a, n)) + list(range(0, b + 1))

    result_set = []
    for k in range(len(anchors)):
        a = anchors[k]
        b = anchors[(k + 1) % len(anchors)]
        idxs = arc_idx(a, b)
        simp = rdp_indices(points[idxs], idxs, epsilon)
        result_set.extend(simp[:-1])

    seen = set()
    dedup = []
    for v in result_set:
        if v not in seen:
            dedup.append(v)
            seen.add(v)
    return dedup


def local_tangent(chunk, at_start):
    """Direcao estavel via regressao sobre os primeiros/ultimos ~25% do trecho."""
    k = max(2, len(chunk) // 4)
    sub = chunk[:k] if at_start else chunk[-k:][::-1]
    if len(sub) < 2:
        d = chunk[1] - chunk[0] if at_start else chunk[-2] - chunk[-1]
        nrm = np.linalg.norm(d)
        return d / nrm if nrm > 1e-9 else np.array([1.0, 0.0])
    d = sub[-1] - sub[0]
    nrm = np.linalg.norm(d)
    if nrm < 1e-9:
        d = sub[1] - sub[0]
        nrm = np.linalg.norm(d)
    return d / nrm if nrm > 1e-9 else np.array([1.0, 0.0])


def fit_cubic(chunk):
    p0, p3 = chunk[0], chunk[-1]
    if len(chunk) <= 2:
        c1 = p0 + (p3 - p0) / 3.0
        c2 = p0 + (p3 - p0) * 2.0 / 3.0
        return c1, c2

    t0 = local_tangent(chunk, at_start=True)
    t1 = local_tangent(chunk, at_start=False)

    seg = np.linalg.norm(np.diff(chunk, axis=0), axis=1)
    cum = np.concatenate([[0], np.cumsum(seg)])
    total = cum[-1] if cum[-1] > 0 else 1.0
    t = cum / total

    A = np.zeros((2, 2))
    bvec = np.zeros(2)
    dot01 = float(np.dot(t0, t1))
    for ti, pt in zip(t, chunk):
        b0 = (1 - ti) ** 3
        b1 = 3 * (1 - ti) ** 2 * ti
        b2 = 3 * (1 - ti) * ti ** 2
        b3 = ti ** 3
        rhs = pt - (b0 * p0 + b3 * p3)
        A[0, 0] += b1 * b1
        A[0, 1] += b1 * b2 * dot01
        A[1, 0] += b1 * b2 * dot01
        A[1, 1] += b2 * b2
        bvec[0] += b1 * np.dot(rhs, t0)
        bvec[1] += b2 * np.dot(rhs, t1)

    try:
        a1, a2 = np.linalg.solve(A + np.eye(2) * 1e-9, bvec)
    except np.linalg.LinAlgError:
        a1 = a2 = np.linalg.norm(p3 - p0) / 3.0

    seg_len = np.linalg.norm(p3 - p0)
    min_a = max(seg_len * 0.01, 1e-4)
    max_a = seg_len * 1.5 if seg_len > 0 else 10.0
    a1 = float(np.clip(a1, min_a, max_a))
    a2 = float(np.clip(a2, min_a, max_a))

    c1 = p0 + t0 * a1
    c2 = p3 + t1 * a2
    return c1, c2


def max_deviation_from_chord(chunk):
    p0, p1 = chunk[0], chunk[-1]
    dists = _point_line_dists(chunk, p0, p1)
    return np.max(dists) if len(dists) else 0.0


def rebuild_subpath(original_points):
    n = len(original_points)
    denoised = smooth_uniform_closed(original_points, PRESMOOTH_RADIUS)
    corners = detect_corners(denoised)
    smoothed = smooth_closed(denoised, corners)
    simplified_idx = rdp_closed_indices(smoothed, corners, RDP_TOLERANCE)
    if len(simplified_idx) < 3:
        simplified_idx = list(range(n))

    m = len(simplified_idx)
    d_parts = []
    n_curves = 0
    n_lines = 0

    start = smoothed[simplified_idx[0]]
    d_parts.append(f"M {start[0]:.3f},{start[1]:.3f}")

    for k in range(m):
        a = simplified_idx[k]
        b = simplified_idx[(k + 1) % m]
        if b >= a:
            chunk = smoothed[a : b + 1]
        else:
            chunk = np.vstack([smoothed[a:], smoothed[: b + 1]])
        if len(chunk) < 2:
            continue

        dev = max_deviation_from_chord(chunk)
        p1 = chunk[-1]
        if dev <= STRAIGHT_TOLERANCE or len(chunk) <= 2:
            d_parts.append(f"L {p1[0]:.3f},{p1[1]:.3f}")
            n_lines += 1
        else:
            c1, c2 = fit_cubic(chunk)
            d_parts.append(
                f"C {c1[0]:.3f},{c1[1]:.3f} {c2[0]:.3f},{c2[1]:.3f} {p1[0]:.3f},{p1[1]:.3f}"
            )
            n_curves += 1

    d_parts.append("Z")
    return " ".join(d_parts), m, n_lines, n_curves


def process_path_d(d):
    subpaths = parse_subpaths(d)
    out = []
    stats = {"subpaths": len(subpaths), "nodes_before": 0, "nodes_after": 0, "lines": 0, "curves": 0}
    for sp in subpaths:
        stats["nodes_before"] += len(sp)
        new_d, n_nodes, n_lines, n_curves = rebuild_subpath(sp)
        stats["nodes_after"] += n_nodes
        stats["lines"] += n_lines
        stats["curves"] += n_curves
        out.append(new_d)
    return " ".join(out), stats


def main():
    with open(SRC, encoding="utf-8") as f:
        content = f.read()

    path_matches = list(re.finditer(r"<path\b[^>]*?/>|<path\b[^>]*?>.*?</path>", content, re.DOTALL))
    assert len(path_matches) == 4, f"esperado 4 paths, encontrado {len(path_matches)}"

    new_content = content
    report = []

    for idx in (3, 2):
        m = path_matches[idx]
        seg = m.group(0)
        d_match = re.search(r'\bd="([^"]*)"', seg)
        old_d = d_match.group(1)
        new_d, stats = process_path_d(old_d)
        new_seg = seg[: d_match.start(1)] + new_d + seg[d_match.end(1) :]
        new_content = new_content[: m.start()] + new_seg + new_content[m.end() :]
        report.append((idx, len(old_d), len(new_d), stats))

    with open(DST, "w", encoding="utf-8") as f:
        f.write(new_content)

    path_matches_new = list(re.finditer(r"<path\b[^>]*?/>|<path\b[^>]*?>.*?</path>", new_content, re.DOTALL))
    assert path_matches_new[0].group(0) == path_matches[0].group(0), "simbolo foi alterado!"
    assert path_matches_new[1].group(0) == path_matches[1].group(0), "L'ESSENCE foi alterado!"

    print("OK - path[0] (simbolo) e path[1] (L'ESSENCE) IDENTICOS ao original.\n")
    for idx, old_len, new_len, stats in sorted(report):
        label = "BY DRA. VALERIA OLIVEIRA" if idx == 2 else "CIRURGIA-DENTISTA & HOF"
        print(f"path[{idx}] ({label}):")
        print(f"  subpaths (letras/contraformas): {stats['subpaths']}")
        print(f"  d length: {old_len} -> {new_len} chars ({(1 - new_len/old_len)*100:.1f}% menor)")
        print(f"  nos totais: {stats['nodes_before']} -> {stats['nodes_after']}")
        print(f"  segmentos retos (L): {stats['lines']}  |  curvas cubicas (C): {stats['curves']}")
        print()


if __name__ == "__main__":
    main()
