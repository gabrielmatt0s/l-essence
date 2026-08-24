"""
Gera os PNGs de favicon a partir do simbolo oficial (favicon.svg, copia
byte-a-byte de assets/brand/00_master_simbolo/simbolo-master-marrom.svg).

Nao usa nenhum "auto-trace" nem redesenho: os pontos de controle das
curvas C sao os mesmos do arquivo oficial, apenas escalados/transladados
para caber no canvas de destino (transformacao linear, preserva
proporcao). O preenchimento usa fill-rule evenodd exatamente como o SVG
(XOR entre os 3 subpaths), com supersampling 16x + downsample LANCZOS
para anti-aliasing limpo.

Script de suporte, nao faz parte do site.
"""
import re
import numpy as np
from PIL import Image, ImageDraw

SRC = "favicon.svg"
SUPERSAMPLE = 16

with open(SRC, encoding="utf-8") as f:
    content = f.read()

vb = re.search(r'viewBox="([^"]*)"', content).group(1)
vb_x, vb_y, vb_w, vb_h = [float(v) for v in vb.split()]

d = re.search(r'\bd="([^"]*)"', content).group(1)


def parse_and_flatten(d, samples_per_curve=40):
    """Retorna lista de subpaths, cada um uma lista de pontos (x,y) flattened."""
    tokens = re.findall(r"[MCZ]|-?\d+\.?\d*", d)
    subpaths = []
    i = 0
    cur = []
    pos = None
    while i < len(tokens):
        t = tokens[i]
        if t == "M":
            if cur:
                subpaths.append(cur)
            pos = (float(tokens[i + 1]), float(tokens[i + 2]))
            cur = [pos]
            i += 3
        elif t == "C":
            c1 = (float(tokens[i + 1]), float(tokens[i + 2]))
            c2 = (float(tokens[i + 3]), float(tokens[i + 4]))
            p3 = (float(tokens[i + 5]), float(tokens[i + 6]))
            p0 = np.array(pos)
            c1a = np.array(c1)
            c2a = np.array(c2)
            p3a = np.array(p3)
            for k in range(1, samples_per_curve + 1):
                tt = k / samples_per_curve
                pt = (
                    (1 - tt) ** 3 * p0
                    + 3 * (1 - tt) ** 2 * tt * c1a
                    + 3 * (1 - tt) * tt ** 2 * c2a
                    + tt ** 3 * p3a
                )
                cur.append((pt[0], pt[1]))
            pos = p3
            i += 7
        elif t == "Z":
            i += 1
        else:
            i += 1
    if cur:
        subpaths.append(cur)
    return subpaths


subpaths = parse_and_flatten(d)
print(f"subpaths no simbolo oficial: {len(subpaths)} "
      f"(pontos: {[len(sp) for sp in subpaths]})")


def render(size, fg_rgb, bg_rgb, out_path, pad_ratio=0.09):
    canvas = size * SUPERSAMPLE
    # margem de respiro (favicons ficam melhores com um pouco de padding)
    pad = vb_w * pad_ratio
    scale = canvas / max(vb_w + 2 * pad, vb_h + 2 * pad)
    off_x = (canvas - (vb_w + 2 * pad) * scale) / 2
    off_y = (canvas - (vb_h + 2 * pad) * scale) / 2

    def to_px(pt):
        x = (pt[0] - vb_x + pad) * scale + off_x
        y = (pt[1] - vb_y + pad) * scale + off_y
        return (x, y)

    # evenodd via XOR acumulado entre subpaths (cada subpath vira mascara propria)
    acc = np.zeros((canvas, canvas), dtype=bool)
    for sp in subpaths:
        mask_img = Image.new("1", (canvas, canvas), 0)
        draw = ImageDraw.Draw(mask_img)
        pts = [to_px(p) for p in sp]
        draw.polygon(pts, fill=1)
        acc ^= np.array(mask_img, dtype=bool)

    alpha_arr = (acc.astype(np.uint8) * 255)
    alpha = Image.fromarray(alpha_arr, mode="L")
    alpha = alpha.resize((size, size), Image.LANCZOS)

    if bg_rgb is None:
        out = Image.new("RGBA", (size, size), (0, 0, 0, 0))  # transparente (favicon padrão)
    else:
        out = Image.new("RGBA", (size, size), bg_rgb + (255,))  # apple-touch-icon: fundo sólido obrigatório

    fg_layer = Image.new("RGBA", (size, size), fg_rgb + (255,))
    out = Image.composite(fg_layer, out, alpha)

    out.save(out_path)
    print("gerado:", out_path, out.size)


BRAND_MARROM = (0x54, 0x25, 0x0D)   # --brand-marrom / --text-primary
BRAND_BG_BASE = (0xFA, 0xF1, 0xE8)  # --bg-base

render(16, BRAND_MARROM, None, "favicon-16x16.png")
render(32, BRAND_MARROM, None, "favicon-32x32.png")
render(180, BRAND_MARROM, BRAND_BG_BASE, "apple-touch-icon.png", pad_ratio=0.16)
