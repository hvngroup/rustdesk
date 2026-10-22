#!/usr/bin/env python3
"""Build the macOS app icon set for HVN Remote Hub.

Usage:
  python3 scripts/make-app-icon.py              # draw the built-in HVN brand artwork
  python3 scripts/make-app-icon.py artwork.png  # use full-bleed square artwork instead

The built-in artwork is a brand-red tile with a white monitor that carries the
HVN GROUP mark, drawn from the polygons of the official logo SVG (never
redrawn by an image model). The artwork is masked into the macOS rounded
square (824 px inside a 1024 px canvas, with a soft shadow) and written as
every size `iconutil` needs. Requires Pillow.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
ICONSET = ROOT / "Resources" / "AppIcon.iconset"
PREVIEW = ROOT / "docs" / "images" / "app-icon.png"

BRAND_RED = (0xEA, 0x44, 0x45)
DARK_RED = (0xC9, 0x39, 0x39)
CHARCOAL = (0x33, 0x33, 0x33)
MEDIUM_GRAY = (0x80, 0x80, 0x80)
LIGHT_GRAY = (0xF5, 0xF5, 0xF5)
WHITE = (0xFF, 0xFF, 0xFF)

CANVAS = 1024
SHAPE = 824
RADIUS = 185
SCALE = 4  # draw large, then downsample for smooth edges

# The HVN GROUP mark from the official logo (dark variant, viewBox 0 0 495.9 127.7).
MARK_RED = [
    [(253.6, 106.3), (211.1, 63.8), (168.6, 106.3), (188.7, 106.3), (211.1, 83.9), (233.6, 106.4)],
    [(168.6, 35.5), (168.6, 84.1), (168.6, 98.3), (182.8, 84.1), (182.8, 21.3)],
]
MARK_GRAY = [
    [(216.1, 58.8), (224.6, 67.3), (224.6, 58.8), (224.6, 50.3)],
    [(230.6, 44.3), (230.6, 73.3), (239.1, 81.8), (239.1, 72.4), (239.1, 63.9), (239.1, 53.7), (239.1, 45.2),
     (239.1, 35.8)],
    [(245.1, 29.8), (245.1, 87.8), (253.6, 96.3), (253.6, 90.4), (253.6, 81.9), (253.6, 38.3), (253.6, 29.8),
     (253.6, 21.3)],
]
MARK_BOX = (168.6, 21.3, 253.6, 106.4)


def draw_mark(draw, center, size):
    """Draw the HVN mark scaled to `size` pixels wide, centered on `center`."""
    x0, y0, x1, y1 = MARK_BOX
    factor = size / (x1 - x0)
    left = center[0] - (x1 - x0) * factor / 2
    top = center[1] - (y1 - y0) * factor / 2

    def place(points):
        return [(left + (x - x0) * factor, top + (y - y0) * factor) for x, y in points]

    for polygon in MARK_RED:
        draw.polygon(place(polygon), fill=BRAND_RED)
    for polygon in MARK_GRAY:
        draw.polygon(place(polygon), fill=MEDIUM_GRAY)


def brand_artwork():
    """Brand-red tile, a white monitor with the HVN mark and a remote cursor."""
    size = CANVAS * SCALE
    s = lambda v: v * SCALE

    gradient = Image.new("RGB", (1, size))
    for y in range(size):
        t = y / (size - 1)
        gradient.putpixel((0, y), tuple(round(a + (b - a) * t) for a, b in zip(BRAND_RED, DARK_RED)))
    art = gradient.resize((size, size)).convert("RGBA")

    screen = (s(188), s(250), s(836), s(690))
    shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((screen[0], screen[1] + s(20), screen[2], screen[3] + s(20)), radius=s(44),
                                  fill=(80, 0, 0, 120))
    shadow_draw.rounded_rectangle((s(392), s(760), s(632), s(812)), radius=s(26), fill=(80, 0, 0, 90))
    art.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(s(22))))

    draw = ImageDraw.Draw(art)
    # Monitor: white bezel, light screen, neck and foot.
    draw.rounded_rectangle(screen, radius=s(44), fill=WHITE)
    inner = (screen[0] + s(30), screen[1] + s(30), screen[2] - s(30), screen[3] - s(30))
    draw.rounded_rectangle(inner, radius=s(22), fill=LIGHT_GRAY)
    draw.rectangle((s(472), screen[3], s(552), s(756)), fill=WHITE)
    draw.rounded_rectangle((s(392), s(740), s(632), s(792)), radius=s(26), fill=WHITE)

    draw_mark(draw, ((inner[0] + inner[2]) / 2, (inner[1] + inner[3]) / 2 - s(6)), s(236))

    # Remote cursor at the lower right of the screen.
    tip = (s(694), s(548))
    cursor = [tip, (tip[0], tip[1] + s(150)), (tip[0] + s(38), tip[1] + s(114)), (tip[0] + s(66), tip[1] + s(174)),
              (tip[0] + s(92), tip[1] + s(162)), (tip[0] + s(64), tip[1] + s(104)), (tip[0] + s(112), tip[1] + s(102))]
    draw.polygon(cursor, fill=CHARCOAL, outline=WHITE, width=s(10))

    return art.resize((CANVAS, CANVAS), Image.LANCZOS)


def masked_icon(artwork):
    """Fit artwork into the macOS rounded square with a drop shadow."""
    art = artwork.convert("RGBA").resize((SHAPE * SCALE, SHAPE * SCALE), Image.LANCZOS)
    mask = Image.new("L", art.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, *art.size), radius=RADIUS * SCALE, fill=255)
    mask = mask.resize((SHAPE, SHAPE), Image.LANCZOS)
    art = art.resize((SHAPE, SHAPE), Image.LANCZOS)
    art.putalpha(mask)

    offset = (CANVAS - SHAPE) // 2
    canvas = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 90), (offset, offset + 10), mask)
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(14)))
    canvas.alpha_composite(art, (offset, offset))
    return canvas


def write_iconset(icon):
    """Write the file names `iconutil -c icns` expects."""
    ICONSET.mkdir(parents=True, exist_ok=True)
    for points in (16, 32, 128, 256, 512):
        for scale in (1, 2):
            name = f"icon_{points}x{points}{'@2x' if scale == 2 else ''}.png"
            icon.resize((points * scale, points * scale), Image.LANCZOS).save(ICONSET / name, optimize=True)
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    icon.resize((256, 256), Image.LANCZOS).save(PREVIEW, optimize=True)


def main():
    artwork = Image.open(sys.argv[1]) if len(sys.argv) > 1 else brand_artwork()
    write_iconset(masked_icon(artwork))
    print(f"Wrote {ICONSET.relative_to(ROOT)} and {PREVIEW.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
