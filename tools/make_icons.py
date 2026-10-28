#!/usr/bin/env python3
"""Generate app icons: dark neon S-tetromino. Run from the project root."""
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "icons"
OUT.mkdir(parents=True, exist_ok=True)
S = 1024

BG = (4, 6, 12, 255)
CYAN = (55, 230, 255)
BLUE = (70, 150, 255)
VIOLET = (160, 107, 255)
PINK = (255, 77, 141)


def glow_ellipse(size, center, radius, color, alpha=90):
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = int(center[0] * size), int(center[1] * size)
    d.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
              fill=color + (alpha,))
    return layer.filter(ImageFilter.GaussianBlur(radius * 0.55))


def build(size=S, content=1.0):
    img = Image.new("RGBA", (size, size), BG)
    img.alpha_composite(glow_ellipse(size, (0.22, 0.12), int(size * 0.42), (18, 70, 150), 105))
    img.alpha_composite(glow_ellipse(size, (0.85, 0.92), int(size * 0.44), (70, 20, 110), 115))

    # S tetromino in a 3x2 footprint
    cell = size * 0.185 * content
    gap = cell * 0.10
    cols, rows = 3, 2
    total_w = cols * cell + (cols - 1) * gap
    total_h = rows * cell + (rows - 1) * gap
    x0 = (size - total_w) / 2
    y0 = (size - total_h) / 2
    rad = cell * 0.24
    colors = [CYAN, BLUE, VIOLET, PINK]
    cells = [(1, 0), (2, 0), (0, 1), (1, 1)]

    blocks = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bd = ImageDraw.Draw(blocks)
    hl = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hl)
    for i, (cx, cy) in enumerate(cells):
        x = x0 + cx * (cell + gap)
        y = y0 + cy * (cell + gap)
        col = colors[i % len(colors)]
        bd.rounded_rectangle([x, y, x + cell, y + cell], radius=rad, fill=col + (255,))
        hd.rounded_rectangle(
            [x + cell * 0.10, y + cell * 0.10, x + cell * 0.90, y + cell * 0.55],
            radius=rad * 0.65, fill=(255, 255, 255, 26))
        hd.rounded_rectangle(
            [x + cell * 0.10, y + cell * 0.10, x + cell * 0.90, y + cell * 0.16],
            radius=rad * 0.3, fill=(255, 255, 255, 80))
    blocks.alpha_composite(hl)

    halo = blocks.filter(ImageFilter.GaussianBlur(cell * 0.30))
    halo.putalpha(halo.getchannel("A").point(lambda v: min(255, int(v * 0.95))))
    img.alpha_composite(halo)
    img.alpha_composite(blocks)
    return img


def save(img, name, size):
    img.resize((size, size), Image.LANCZOS).convert("RGB").save(OUT / name, optimize=True)


base = build(S, 1.0)
save(base, "icon-512.png", 512)
save(base, "icon-192.png", 192)
save(base, "apple-touch-icon-180.png", 180)
save(build(S, 0.62), "maskable-512.png", 512)
print("icons ->", OUT)
