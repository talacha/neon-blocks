#!/usr/bin/env python3
"""Generate the 1200x630 Open Graph / social card.

Run from the project root: python3 tools/make_og.py
Output: icons/og-image.png
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "icons" / "og-image.png"

W, H = 1200, 630
BG = (4, 6, 12)
CYAN = (55, 230, 255)
BLUE = (70, 150, 255)
VIOLET = (160, 107, 255)
PINK = (255, 77, 141)
WHITE = (233, 248, 255)
MUTED = (150, 176, 196)
DIM = (110, 134, 152)

FONT_DIRS = [
    "/System/Library/Fonts/Supplemental",
    "/System/Library/Fonts",
    "/usr/share/fonts/truetype/dejavu",
]


def ttf(names, size):
    for name in names:
        for d in FONT_DIRS:
            p = Path(d) / name
            if p.exists():
                try:
                    return ImageFont.truetype(str(p), size)
                except OSError:
                    continue
    return ImageFont.load_default()


def heavy(size):
    return ttf(["Arial Black.ttf", "DejaVuSans-Bold.ttf"], size)


def bold(size):
    return ttf(["Arial Bold.ttf", "DejaVuSans-Bold.ttf"], size)


def glow(size, center, radius, color, alpha):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = center
    d.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=color + (alpha,))
    return layer.filter(ImageFilter.GaussianBlur(radius * 0.55))


def tracked(draw, xy, text, font, fill, tracking=0.0):
    """Draw text with letter spacing; returns the end x."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return x - tracking


def tetromino(size, cell, gap_ratio=0.12):
    """The 3x2 S-piece cluster used in the app icons."""
    gap = cell * gap_ratio
    cols, rows = 3, 2
    tw = cols * cell + (cols - 1) * gap
    th = rows * cell + (rows - 1) * gap
    canvas = Image.new("RGBA", (int(tw + cell), int(th + cell)), (0, 0, 0, 0))
    rad = cell * 0.24

    blocks = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    bd = ImageDraw.Draw(blocks)
    hl = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    hd = ImageDraw.Draw(hl)
    colors = [CYAN, BLUE, VIOLET, PINK]

    for i, (cx, cy) in enumerate([(1, 0), (2, 0), (0, 1), (1, 1)]):
        x = cell * 0.5 + cx * (cell + gap)
        y = cell * 0.5 + cy * (cell + gap)
        bd.rounded_rectangle([x, y, x + cell, y + cell], radius=rad, fill=colors[i] + (255,))
        hd.rounded_rectangle(
            [x + cell * 0.10, y + cell * 0.10, x + cell * 0.90, y + cell * 0.55],
            radius=rad * 0.65, fill=(255, 255, 255, 26))
        hd.rounded_rectangle(
            [x + cell * 0.10, y + cell * 0.10, x + cell * 0.90, y + cell * 0.16],
            radius=rad * 0.30, fill=(255, 255, 255, 80))
    blocks.alpha_composite(hl)

    halo = blocks.filter(ImageFilter.GaussianBlur(cell * 0.30))
    halo.putalpha(halo.getchannel("A").point(lambda v: min(255, int(v * 0.95))))
    canvas.alpha_composite(halo)
    canvas.alpha_composite(blocks)
    return canvas


def build():
    img = Image.new("RGBA", (W, H), BG + (255,))
    img.alpha_composite(glow((W, H), (170, 90), 430, (16, 66, 140), 120))
    img.alpha_composite(glow((W, H), (1080, 610), 430, (66, 18, 108), 130))
    img.alpha_composite(glow((W, H), (880, 300), 300, (30, 20, 80), 90))

    d = ImageDraw.Draw(img)
    x = 84

    # kicker
    kf = bold(22)
    tracked(d, (x, 132), "NEON EDITION", kf, CYAN, 6.5)

    # title
    tf = heavy(74)
    end = tracked(d, (x, 172), "NEON STACK", tf, WHITE, 1.5)
    tracked(d, (end + 22, 172), "3D", tf, CYAN, 1.5)

    # tagline
    sf = bold(30)
    d.text((x, 296), "A neon 3D falling-block puzzle", font=sf, fill=MUTED)

    # rule
    d.line([(x, 352), (x + 592, 352)], fill=(60, 90, 110), width=2)

    # feature chips
    cf = bold(20)
    chips = ["7-BAG", "SRS KICKS", "T-SPIN", "HOLD", "GHOST"]
    cx = x
    for c in chips:
        w = d.textlength(c, font=cf) + 26
        d.rounded_rectangle([cx, 382, cx + w, 420], radius=19,
                            fill=(14, 28, 44), outline=(46, 74, 96), width=1)
        d.text((cx + 13, 391), c, font=cf, fill=(150, 205, 230))
        cx += w + 10

    # footer
    uf = bold(26)
    uend = tracked(d, (x, 492), "neon.robs.ws", uf, CYAN, 0.5)
    d.text((uend + 16, 492), "· plays offline", font=uf, fill=DIM)

    cf2 = bold(18)
    tracked(d, (x, 548), "ROB.CR   ·   TALACHA.DEV", cf2, (120, 145, 164), 3.2)

    # art
    art = tetromino(0, 128)
    img.alpha_composite(art, (W - art.width - 46, (H - art.height) // 2 + 10))

    img.save(OUT, "PNG", optimize=True)
    print(f"{OUT}  {OUT.stat().st_size / 1024:.0f} KiB  {W}x{H}")


if __name__ == "__main__":
    build()
