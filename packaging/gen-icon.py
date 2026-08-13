#!/usr/bin/env python3
"""Gera o ícone do app BT Charge: fone de ouvido com o símbolo Bluetooth
dentro. A bandeja continua usando o bt-charge-emoji (fone branco) — este
ícone é só para o .desktop / lista de aplicativos."""
from PIL import Image, ImageDraw
import os

BG = (30, 41, 59, 255)        # slate-800 (fundo)
HEAD = (248, 250, 252, 255)   # branco (fone)
PAD = (203, 213, 225, 255)    # slate-300 (almofada interna das conchas)
BT = (56, 189, 248, 255)      # sky-400 (símbolo bluetooth)

OUT = os.path.expanduser("~/bt-charge/icons")


def draw_icon(size):
    S = size
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    # fundo: quadrado arredondado
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.22), fill=BG)

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
    cx, cy, H = 128, 160, 52
    s = H / 20.0
    outer = [(17.71, 7.71), (12, 2), (11, 2), (11, 9.59), (6.41, 5),
             (5, 6.41), (10.59, 12), (5, 17.59), (6.41, 19), (11, 14.41),
             (11, 22), (12, 22), (17.71, 16.29), (13.41, 12), (17.71, 7.71)]
    poly = [(cx + (x - 11.5) * s, cy + (y - 12) * s) for x, y in outer]
    d.polygon(poly, fill=BT)
    # recortes internos (traço duplo do lado direito)
    for tri in (((13, 5.83), (14.88, 7.71), (13, 9.59)),
                ((14.88, 16.29), (13, 18.17), (13, 14.41))):
        hole = [(cx + (x - 11.5) * s, cy + (y - 12) * s) for x, y in tri]
        d.polygon(hole, fill=BG)

    return im


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    master = draw_icon(256)
    master.save(os.path.join(OUT, "bt-charge.png"))
    for size in (128, 64, 48, 32):
        d = os.path.join(OUT, f"{size}x{size}")
        os.makedirs(d, exist_ok=True)
        draw_icon(size).save(os.path.join(d, "bt-charge.png"))
    print("ícones gerados em", OUT)
