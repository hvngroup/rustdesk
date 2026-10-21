#!/usr/bin/env python3
"""Generate every HVN Remote Hub icon from one drawing.

Usage (from the repository root, needs Pillow):
  python3 res/hvn_icons.py

The artwork matches the HVN Remote Hub 1.x Mac app: a brand-red tile with a
white monitor that carries the HVN GROUP mark and a remote cursor. The mark is
drawn from the polygons of the official HVN GROUP logo SVG. Small sizes, the
tray and notification icons use the mark alone, which stays legible at 16 px.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent

BRAND_RED = "#EA4445"
DARK_RED = "#C93939"
CHARCOAL = "#333333"
MEDIUM_GRAY = "#808080"
LIGHT_GRAY = "#F5F5F5"
WHITE = "#FFFFFF"

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


def mark_polygons(center, width, red=BRAND_RED, gray=MEDIUM_GRAY):
    """The HVN mark `width` units wide, centered on `center`, as (points, fill) pairs."""
    x0, y0, x1, y1 = MARK_BOX
    factor = width / (x1 - x0)
    left = center[0] - (x1 - x0) * factor / 2
    top = center[1] - (y1 - y0) * factor / 2

    def place(points):
        return [(left + (x - x0) * factor, top + (y - y0) * factor) for x, y in points]

    return [(place(p), red) for p in MARK_RED] + [(place(p), gray) for p in MARK_GRAY]


# Shapes in a 1024-unit square. Each is (kind, geometry, fill[, extra]).
SCREEN = (188, 250, 836, 690)
INNER = (SCREEN[0] + 30, SCREEN[1] + 30, SCREEN[2] - 30, SCREEN[3] - 30)
CURSOR_TIP = (694, 548)


def monitor_shapes():
    tip = CURSOR_TIP
    cursor = [tip, (tip[0], tip[1] + 150), (tip[0] + 38, tip[1] + 114), (tip[0] + 66, tip[1] + 174),
              (tip[0] + 92, tip[1] + 162), (tip[0] + 64, tip[1] + 104), (tip[0] + 112, tip[1] + 102)]
    shapes = [
        ("shadow", (SCREEN[0], SCREEN[1] + 20, SCREEN[2], SCREEN[3] + 20, 44), "#500000", 0.47),
        ("shadow", (392, 760, 632, 812, 26), "#500000", 0.35),
        ("rrect", (*SCREEN, 44), WHITE),
        ("rrect", (*INNER, 22), LIGHT_GRAY),
        ("rrect", (472, SCREEN[3], 552, 756, 0), WHITE),
        ("rrect", (392, 740, 632, 792, 26), WHITE),
    ]
    center = ((INNER[0] + INNER[2]) / 2, (INNER[1] + INNER[3]) / 2 - 6)
    shapes += [("poly", points, fill) for points, fill in mark_polygons(center, 236)]
    shapes.append(("poly", cursor, CHARCOAL, (WHITE, 10)))
    return shapes


def mark_only_shapes(fill=None, width=640):
    center = (512, 512)
    if fill:
        return [("poly", points, fill) for points, _ in mark_polygons(center, width)]
    return [("poly", points, f) for points, f in mark_polygons(center, width, WHITE, WHITE)]


# ---------------------------------------------------------------- raster

def _rgba(color, alpha=1.0):
    color = color.lstrip("#")
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4)) + (round(255 * alpha),)


def _gradient(size):
    top, bottom = _rgba(BRAND_RED), _rgba(DARK_RED)
    column = Image.new("RGBA", (1, size))
    for y in range(size):
        t = y / (size - 1)
        column.putpixel((0, y), tuple(round(a + (b - a) * t) for a, b in zip(top, bottom)))
    return column.resize((size, size))


def render(shapes, size=1024, background=True):
    """Rasterize shapes drawn in 1024 units into a size x size RGBA image."""
    big = 1024 * SCALE
    s = lambda v: v * SCALE
    art = _gradient(big) if background else Image.new("RGBA", (big, big), (0, 0, 0, 0))
    for shape in shapes:
        kind, geometry, fill = shape[:3]
        if kind == "shadow":
            layer = Image.new("RGBA", (big, big), (0, 0, 0, 0))
            x0, y0, x1, y1, r = geometry
            ImageDraw.Draw(layer).rounded_rectangle((s(x0), s(y0), s(x1), s(y1)), radius=s(r),
                                                    fill=_rgba(fill, shape[3]))
            art.alpha_composite(layer.filter(ImageFilter.GaussianBlur(s(22))))
            continue
        draw = ImageDraw.Draw(art)
        if kind == "rrect":
            x0, y0, x1, y1, r = geometry
            draw.rounded_rectangle((s(x0), s(y0), s(x1), s(y1)), radius=s(r), fill=_rgba(fill))
        elif kind == "poly":
            outline = shape[3] if len(shape) > 3 else None
            points = [(s(x), s(y)) for x, y in geometry]
            if outline:
                draw.polygon(points, fill=_rgba(fill), outline=_rgba(outline[0]), width=s(outline[1]))
            else:
                draw.polygon(points, fill=_rgba(fill))
    return art.resize((size, size), Image.LANCZOS)


def masked(image, shape="rounded", inset=0.0, shadow=False):
    """Cut image into a rounded square or circle, optionally inset with a drop shadow."""
    size = image.width
    inner = round(size * (1 - 2 * inset))
    big = inner * SCALE
    mask = Image.new("L", (big, big), 0)
    if shape == "circle":
        ImageDraw.Draw(mask).ellipse((0, 0, big, big), fill=255)
    else:
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, big, big), radius=round(big * 0.225), fill=255)
    mask = mask.resize((inner, inner), Image.LANCZOS)
    art = image.resize((inner, inner), Image.LANCZOS)
    art.putalpha(mask)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    offset = (size - inner) // 2
    if shadow:
        drop = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        drop.paste((0, 0, 0, 90), (offset, offset + size // 100), mask)
        canvas.alpha_composite(drop.filter(ImageFilter.GaussianBlur(size / 73)))
    canvas.alpha_composite(art, (offset, offset))
    return canvas


# ---------------------------------------------------------------- svg

def svg(shapes, rounded=True):
    """The same drawing as an SVG document in a 1024-unit viewBox."""
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">',
        '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BRAND_RED}"/><stop offset="1" stop-color="{DARK_RED}"/>'
        '</linearGradient><filter id="blur" x="-20%" y="-20%" width="140%" height="140%">'
        '<feGaussianBlur stdDeviation="22"/></filter></defs>',
        f'<rect width="1024" height="1024" rx="{230 if rounded else 0}" fill="url(#bg)"/>',
    ]
    for shape in shapes:
        kind, geometry, fill = shape[:3]
        if kind in ("shadow", "rrect"):
            x0, y0, x1, y1, r = geometry
            extra = f' fill-opacity="{shape[3]}" filter="url(#blur)"' if kind == "shadow" else ""
            parts.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="{r}" '
                         f'fill="{fill}"{extra}/>')
        else:
            points = " ".join(f"{x:.1f},{y:.1f}" for x, y in geometry)
            stroke = ""
            if len(shape) > 3:
                stroke = f' stroke="{shape[3][0]}" stroke-width="{shape[3][1]}" stroke-linejoin="round"'
            parts.append(f'<polygon points="{points}" fill="{fill}"{stroke}/>')
    parts.append("</svg>\n")
    return "\n".join(parts)


# ---------------------------------------------------------------- outputs

def save(image, path, **options):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True, **options) if path.suffix == ".png" else image.save(path, **options)


def save_ico(path, sizes, large, small):
    """An .ico whose 32 px and smaller frames use the simplified small icon."""
    frames = [(small if size <= 32 else large).resize((size, size), Image.LANCZOS) for size in sizes]
    frames[-1].save(ROOT / path, format="ICO", sizes=[(s, s) for s in sizes], append_images=frames[:-1])


def main():
    full = render(monitor_shapes())                     # full-bleed square artwork
    tile = masked(full)                                 # rounded tile, transparent corners
    small = masked(render(mark_only_shapes(width=700)))  # mark on the red tile, for 32 px and below

    # Desktop and in-app icons.
    save(tile, "res/icon.png")
    save(masked(full, inset=(1024 - 824) / 2048, shadow=True), "res/mac-icon.png")
    save(masked(full, inset=(1024 - 824) / 2048, shadow=True), "flutter/macos/Runner/AppIcon.icns",
         format="ICNS")
    for name, size in (("32x32", 32), ("64x64", 64), ("128x128", 128), ("128x128@2x", 256)):
        save((small if size <= 32 else tile).resize((size, size), Image.LANCZOS), f"res/{name}.png")
    save_ico("res/icon.ico", [16, 24, 32, 48, 64, 128, 256], tile, small)
    save_ico("flutter/windows/runner/resources/app_icon.ico", [16, 24, 32, 48, 64, 128, 256], tile, small)
    save_ico("res/tray-icon.ico", [16, 24, 32], tile, small)
    (ROOT / "res/scalable.svg").write_text(svg(monitor_shapes()))
    (ROOT / "flutter/assets/icon.svg").write_text(svg(monitor_shapes()))

    # macOS menu bar: a template image, so only the alpha channel matters.
    black_mark = render(mark_only_shapes(fill="#000000", width=900), background=False)
    save(black_mark.resize((60, 60), Image.LANCZOS), "res/mac-tray-dark-x2.png")
    white_mark = render(mark_only_shapes(fill=WHITE, width=900), background=False)
    save(white_mark.resize((48, 48), Image.LANCZOS), "res/mac-tray-light-x2.png")

    # iOS: opaque full-bleed square; the system applies its own mask.
    ios = Path("flutter/ios/Runner/Assets.xcassets/AppIcon.appiconset")
    for points, scales in ((20, (1, 2, 3)), (29, (1, 2, 3)), (40, (1, 2, 3)), (60, (2, 3)), (76, (1, 2)),
                           (83.5, (2,)), (1024, (1,))):
        for scale in scales:
            label = f"{points:g}x{points:g}@{scale}x"
            size = round(points * scale)
            save(full.convert("RGB").resize((size, size), Image.LANCZOS), ios / f"Icon-App-{label}.png")

    # Android: legacy and round launcher icons, adaptive foreground on the brand-red
    # background (ic_launcher_background), a monochrome mark for themed icons, and the
    # white notification icon.
    android = Path("flutter/android/app/src/main/res")
    foreground = render(monitor_shapes(), background=False)
    adaptive = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    content = round(1024 * 72 / 108)  # the visible part of the adaptive icon layer
    adaptive.alpha_composite(foreground.resize((content, content), Image.LANCZOS), ((1024 - content) // 2,) * 2)
    monochrome = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    mark = render(mark_only_shapes(fill=WHITE, width=1024), background=False)
    monochrome.alpha_composite(mark.resize((content, content), Image.LANCZOS), ((1024 - content) // 2,) * 2)
    notification = render(mark_only_shapes(fill=WHITE, width=900), background=False)
    for density, scale in (("mdpi", 1), ("hdpi", 1.5), ("xhdpi", 2), ("xxhdpi", 3), ("xxxhdpi", 4)):
        folder = android / f"mipmap-{density}"
        launcher = round(48 * scale)
        save(masked(full).resize((launcher, launcher), Image.LANCZOS), folder / "ic_launcher.png")
        save(masked(full, "circle").resize((launcher, launcher), Image.LANCZOS), folder / "ic_launcher_round.png")
        layer = round(108 * scale)
        save(adaptive.resize((layer, layer), Image.LANCZOS), folder / "ic_launcher_foreground.png")
        save(monochrome.resize((layer, layer), Image.LANCZOS), folder / "ic_launcher_monochrome.png")
        status = round(24 * scale)
        save(notification.resize((status, status), Image.LANCZOS).convert("LA"), folder / "ic_stat_logo.png")
    save(masked(full).resize((256, 256), Image.LANCZOS), "fastlane/metadata/android/en-US/images/icon.png")

    print("HVN Remote Hub icons written.")


if __name__ == "__main__":
    main()
