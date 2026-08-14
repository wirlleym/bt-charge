#!/usr/bin/env python3
"""Gera o ícone do app BT Charge com qualidade de app nativo:

  * fundo em gradiente azul vibrante (identidade Bluetooth) — diferente do
    slate-800 antigo, que sumia no fundo escuro da grade do GNOME;
  * cantos arredondados estilo squircle (radius 22%);
  * supersampling 4x + downscale LANCZOS = bordas suaves em todos os
    tamanhos (sem serrilhado);
  * PNGs em todos os tamanhos hicolor (16..256) + SVG escalável.

A bandeja continua usando o bt-charge-emoji (fone branco) — este ícone é
para o .desktop / lista de aplicativos.
"""
from PIL import Image, ImageDraw
import os

# Cores
TOP = (56, 189, 248, 255)        # sky-400 (topo do gradiente)
BOTTOM = (2, 132, 199, 255)      # sky-600 (base do gradiente)
HEAD = (255, 255, 255, 255)      # branco (fone)
PAD = (186, 230, 253, 255)       # sky-200 (almofada interna das conchas)
BT = (12, 74, 110, 255)          # sky-950 (símbolo bluetooth, contraste alto)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "icons")

# Tamanhos hicolor padrão (apps/)
SIZES = (16, 22, 24, 32, 44, 48, 64, 96, 128, 192, 256)


def draw_icon(size, ss=4):
    """Desenha em size*ss (supersampling) e reduz para size."""
    S = size * ss
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))

    # fundo: gradiente vertical (com cantos arredondados)
    bg = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d_bg = ImageDraw.Draw(bg)
    for y in range(S):
        t = y / (S - 1)
        col = tuple(int(TOP[i] + (BOTTOM[i] - TOP[i]) * t) for i in range(3))
        d_bg.line([(0, y), (S, y)], fill=(col[0], col[1], col[2], 255))
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, S - 1, S - 1], radius=int(S * 0.22), fill=255)
    im.paste(bg, (0, 0), mask)

    d = ImageDraw.Draw(im)

    # banda do fone (arco grosso)
    d.arc([int(56 / 256 * S), int(26 / 256 * S), int(200 / 256 * S),
           int(164 / 256 * S)], start=180, end=360,
          fill=HEAD, width=int(34 / 256 * S))

    # conchas
    for cx in (44, 160):
        d.rounded_rectangle([int(cx / 256 * S), int(148 / 256 * S),
                             int((cx + 52) / 256 * S), int(204 / 256 * S)],
                            radius=int(18 / 256 * S), fill=HEAD)
        # almofada interna
        d.rounded_rectangle([int((cx + 12) / 256 * S), int(160 / 256 * S),
                             int((cx + 40) / 256 * S), int(192 / 256 * S)],
                            radius=int(12 / 256 * S), fill=PAD)

    # símbolo bluetooth (path do Material Design "bluetooth", caixa 24x24)
    # — coordenadas na grade 256, escaladas por ss (canvas está em S=size*ss)
    cx, cy, H = 128 * ss, 160 * ss, 52 * ss
    s = H / 20.0
    outer = [(17.71, 7.71), (12, 2), (11, 2), (11, 9.59), (6.41, 5),
             (5, 6.41), (10.59, 12), (5, 17.59), (6.41, 19), (11, 14.41),
             (11, 22), (12, 22), (17.71, 16.29), (13.41, 12), (17.71, 7.71)]
    poly = [(cx + (x - 11.5) * s, cy + (y - 12) * s) for x, y in outer]
    d.polygon(poly, fill=BT)
    # recortes internos (traço duplo do lado direito)
    hole_fill = BG_COLOR_AT(cy + 4, S, TOP, BOTTOM)
    for tri in (((13, 5.83), (14.88, 7.71), (13, 9.59)),
                ((14.88, 16.29), (13, 18.17), (13, 14.41))):
        hole = [(cx + (x - 11.5) * s, cy + (y - 12) * s) for x, y in tri]
        d.polygon(hole, fill=hole_fill)

    if ss > 1:
        im = im.resize((size, size), Image.LANCZOS)
    return im


def BG_COLOR_AT(y, S, top, bottom):
    t = min(max(y / (S - 1), 0), 1)
    return tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))


def svg_icon():
    """Versão SVG escalável (mesmo desenho, viewBox 256)."""
    def P(x, y):
        return f"{x:.1f},{y:.1f}"

    # path do bluetooth Material (24x24) escalado para a posição do PNG
    cx, cy, H = 128, 160, 52
    s = H / 20.0
    outer = [(17.71, 7.71), (12, 2), (11, 2), (11, 9.59), (6.41, 5),
             (5, 6.41), (10.59, 12), (5, 17.59), (6.41, 19), (11, 14.41),
             (11, 22), (12, 22), (17.71, 16.29), (13.41, 12), (17.71, 7.71)]
    poly = " ".join(P(cx + (x - 11.5) * s, cy + (y - 12) * s) for x, y in outer)
    holes = []
    for tri in (((13, 5.83), (14.88, 7.71), (13, 9.59)),
                ((14.88, 16.29), (13, 18.17), (13, 14.41))):
        pts = [P(cx + (x - 11.5) * s, cy + (y - 12) * s) for x, y in tri]
        holes.append(f'<polygon points="{pts[0]} {pts[1]} {pts[2]}" fill="#0c4a6e"/>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#38bdf8"/>
      <stop offset="1" stop-color="#0284c7"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="256" height="256" rx="56" ry="56" fill="url(#bg)"/>
  <path d="M 56 95 A 72 69 0 0 1 200 95" stroke="#ffffff" stroke-width="34" fill="none" stroke-linecap="round"/>
  <rect x="44" y="148" width="52" height="56" rx="18" fill="#ffffff"/>
  <rect x="160" y="148" width="52" height="56" rx="18" fill="#ffffff"/>
  <rect x="56" y="160" width="28" height="32" rx="12" fill="#bae6fd"/>
  <rect x="172" y="160" width="28" height="32" rx="12" fill="#bae6fd"/>
  <polygon points="{poly}" fill="#0c4a6e"/>
  {''.join(holes)}
</svg>
'''


def main():
    os.makedirs(OUT, exist_ok=True)
    master = draw_icon(256)
    master.save(os.path.join(OUT, "bt-charge.png"))
    for size in SIZES:
        d = os.path.join(OUT, f"{size}x{size}")
        os.makedirs(d, exist_ok=True)
        draw_icon(size).save(os.path.join(d, "bt-charge.png"))
    svg_dir = os.path.join(OUT, "scalable")
    os.makedirs(svg_dir, exist_ok=True)
    with open(os.path.join(svg_dir, "bt-charge.svg"), "w") as f:
        f.write(svg_icon())
    print(f"ícones gerados em {OUT}: {len(SIZES)} tamanhos + scalable/bt-charge.svg")


if __name__ == "__main__":
    main()
