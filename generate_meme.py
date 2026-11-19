#!/usr/bin/env python3
"""Generate the gta6-meme-x-01 v2 meme image (1024x1024 PNG).

Concept (user's own, 19 Nov 22:50 WIB): the GTA VI "Mission Passed"
waiting meme, FULLY IN ENGLISH. A bored man in a Hawaiian shirt has
waited 13 years for GTA 6; his friends got married and had kids, and he
is still waiting for one mission that hasn't been completed. The make.fun
ghost floats above it all -- the ghost spent the wait getting paid in
make.fun bounties instead.

Build: an AI-generated text-free scene plate (assets/scene-v2-plate.png,
same composition as the user's reference image) plus ALL text and UI
drawn deterministically with Pillow, so every word is spelled exactly
right -- no AI-rendered text anywhere. The make.fun ghost
(assets/mark-1024.png, press kit) is composited twice: big in the sky
and small in the "MAKE.FUN GHOST" panel row, plus the make.fun wordmark.

Deterministic: fixed coordinates, fixed fonts, no randomness, no
network. Re-running produces the same bytes.

Usage: python3 generate_meme.py  (writes meme.png next to this script)
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
OUT = HERE / "meme.png"

W, H = 1024, 1024

PINK = (255, 110, 199)
PINK_DEEP = (255, 46, 154)
PINK_SOFT = (255, 122, 217)
WHITE = (255, 255, 255)
BLACK = (10, 8, 12)
INK = (36, 23, 8)          # marker ink on the cardboard sign
CARDBOARD = (178, 128, 74)
PANEL = (8, 8, 12)
ROW_LINE = (48, 48, 56)


def find_font(size, italic=False):
    """Pick a font that exists on this machine."""
    candidates = []
    if italic:
        candidates += [
            "/usr/share/fonts/truetype/noto/NotoSans-BoldItalic.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansDisplay-BoldItalic.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf",
        ]
    candidates += [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    ]
    if not italic:
        candidates.append("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    raise FileNotFoundError("no usable font found")


def font_regular(size):
    for path in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    ]:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return find_font(size)


def text_center(draw, cx, y, text, font, fill, stroke=0, stroke_fill=BLACK):
    """Draw text centred on cx, top at y. Returns the text height."""
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    draw.text((cx - (bbox[2] + bbox[0]) // 2, y), text, font=font,
              fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    return bbox[3] - bbox[1]


def text_left(draw, x, y, text, font, fill):
    draw.text((x, y), text, font=font, fill=fill)
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[3] - bbox[1]


def text_right(draw, x, y, text, font, fill):
    """Draw text right-aligned to x, top at y."""
    bbox = draw.textbbox((0, 0), text, font=font)
    draw.text((x - (bbox[2] - bbox[0]), y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]


def rounded_bubble(draw, box, radius, fill, outline, width):
    draw.rounded_rectangle(box, radius=radius, fill=fill,
                           outline=outline, width=width)


def star_points(cx, cy, outer, inner, points=5):
    import math
    pts = []
    for i in range(points * 2):
        r = outer if i % 2 == 0 else inner
        angle = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    return pts


def draw_clock(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=3)
    draw.line([cx, cy, cx, cy - r + 5], fill=WHITE, width=3)
    draw.line([cx, cy, cx + r - 6, cy + 4], fill=WHITE, width=3)


def draw_trophy(draw, cx, cy, s):
    # Cup bowl, two handles, stem, base -- all white, simple and bold.
    draw.polygon([(cx - s, cy - s), (cx + s, cy - s),
                  (cx + s * 0.55, cy + s * 0.1), (cx - s * 0.55, cy + s * 0.1)],
                 fill=WHITE)
    draw.ellipse([cx - s - 6, cy - s + 2, cx - s + 6, cy - s * 0.1],
                 outline=WHITE, width=3)
    draw.ellipse([cx + s - 6, cy - s + 2, cx + s + 6, cy - s * 0.1],
                 outline=WHITE, width=3)
    draw.rectangle([cx - 3, cy + s * 0.1, cx + 3, cy + s * 0.6], fill=WHITE)
    draw.rectangle([cx - s * 0.7, cy + s * 0.6, cx + s * 0.7, cy + s * 0.85],
                   fill=WHITE)


def paste_ghost(img, x, y, size, shadow=True):
    """Paste the make.fun ghost (white, transparent bg) at (x, y)."""
    ghost = Image.open(ASSETS / "mark-1024.png").convert("RGBA")
    ghost = ghost.resize((size, size), Image.LANCZOS)
    if shadow:
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        black = Image.new("RGBA", ghost.size, (0, 0, 0, 150))
        alpha = ghost.split()[3]
        sh = Image.composite(black, Image.new("RGBA", ghost.size, (0, 0, 0, 0)), alpha)
        sh = sh.filter(ImageFilter.GaussianBlur(8))
        layer.paste(sh, (x + 6, y + 8), sh)
        img.alpha_composite(layer)
    img.paste(ghost, (x, y), ghost)


def main():
    # Scene plate: 1600x1600 text-free illustration -> 1024x1024.
    plate = Image.open(ASSETS / "scene-v2-plate.png").convert("RGB")
    img = plate.resize((W, H), Image.LANCZOS).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")

    # ---- GTA VI logo, top-left -------------------------------------
    logo = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 54)
    vi_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 104)
    script = find_font(42, italic=True)
    draw.text((30, 22), "GRAND", font=logo, fill=WHITE, stroke_width=2, stroke_fill=BLACK)
    draw.text((30, 78), "THEFT", font=logo, fill=WHITE, stroke_width=2, stroke_fill=BLACK)
    draw.text((30, 134), "AUTO", font=logo, fill=WHITE, stroke_width=2, stroke_fill=BLACK)
    auto_w = draw.textbbox((0, 0), "AUTO", font=logo, stroke_width=2)[2]
    draw.text((30 + auto_w + 12, 96), "VI", font=vi_font, fill=PINK_DEEP, stroke_width=3, stroke_fill=BLACK)
    draw.text((30, 208), "Vice city", font=script, fill=PINK_SOFT,
              stroke_width=2, stroke_fill=BLACK)

    # ---- make.fun ghost + wordmark, top-right (judge's first check) --
    paste_ghost(img, 845, 18, 170)
    draw = ImageDraw.Draw(img, "RGBA")
    text_center(draw, 930, 192, "make.fun",
                find_font(34), WHITE, stroke=2)

    # ---- thought bubble: "WHEN'S IT COMING OUT, BRO?" ---------------
    rounded_bubble(draw, [470, 88, 700, 192], 20, WHITE, BLACK, 3)
    bubble_font = find_font(26)
    text_center(draw, 585, 100, "WHEN'S IT", bubble_font, BLACK)
    text_center(draw, 585, 128, "COMING OUT,", bubble_font, BLACK)
    text_center(draw, 585, 156, "BRO?", bubble_font, BLACK)
    for (cx, cy, r) in [(480, 200, 7), (466, 192, 5), (454, 182, 4)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE,
                     outline=BLACK, width=2)

    # ---- speech bubble from the cop --------------------------------
    rounded_bubble(draw, [500, 215, 840, 325], 18, WHITE, BLACK, 3)
    # Tail juts from the bubble's right edge toward the cop's mouth.
    draw.polygon([(838, 290), (838, 318), (866, 308)], fill=WHITE)
    draw.line([(838, 290), (866, 308)], fill=BLACK, width=3)
    draw.line([(838, 318), (866, 308)], fill=BLACK, width=3)
    text_center(draw, 670, 227, "BE PATIENT, BRO.", bubble_font, BLACK)
    text_center(draw, 670, 255, "VICE CITY WASN'T", bubble_font, BLACK)
    text_center(draw, 670, 283, "BUILT OVERNIGHT.", bubble_font, BLACK)

    # ---- "WELCOME TO VICE CITY" board on the left wall -------------
    draw.rectangle([10, 330, 160, 450], fill=(139, 90, 43, 255),
                   outline=(60, 35, 12, 255), width=3)
    small = find_font(19)
    mid = find_font(36)
    text_center(draw, 85, 340, "WELCOME TO", small, (30, 18, 8))
    text_center(draw, 85, 364, "VICE", mid, PINK_DEEP)
    text_center(draw, 85, 402, "CITY", mid, PINK_DEEP)

    # ---- cardboard sign: the wait, in the man's hands ---------------
    sign_font1 = find_font(29)
    sign_font2 = find_font(60)
    sign_font3 = find_font(40)
    sign_font4 = find_font(27)
    text_center(draw, 461, 388, "WAITING FOR", sign_font1, INK)
    text_center(draw, 461, 420, "GTA 6", sign_font2, INK)
    text_center(draw, 461, 488, "13 YEARS", sign_font3, INK)
    text_center(draw, 461, 534, "2011 – 2024", sign_font4, INK)

    # ---- Mission Passed panel ---------------------------------------
    draw.rounded_rectangle([40, 585, 984, 885], radius=24, fill=PANEL)
    title = find_font(60)
    sub = find_font(40)
    text_center(draw, 512, 602, "MISSION PASSED!", title, PINK)
    text_center(draw, 512, 668, "RESPECT +", sub, WHITE)
    draw.line([90, 724, 934, 724], fill=(70, 70, 78), width=2)

    rows = [
        ("WAITING FOR", "13 YEARS", "clock"),
        ("MAKE.FUN GHOST", "GOT PAID", "ghost"),
        ("PATIENCE LEVEL", "LEGENDARY", "star"),
        ("PRIZE", "GTA 6 + FIRST PRIZE", "trophy"),
    ]
    row_font = find_font(30)
    row_ys = [752, 790, 828, 866]
    for (label, value, icon), y in zip(rows, row_ys):
        cy = y + 15
        if icon == "clock":
            draw_clock(draw, 77, cy, 14)
        elif icon == "ghost":
            mini = Image.open(ASSETS / "mark-1024.png").convert("RGBA")
            mini = mini.resize((32, 32), Image.LANCZOS)
            img.paste(mini, (61, cy - 16), mini)
            draw = ImageDraw.Draw(img, "RGBA")
        elif icon == "star":
            draw.polygon(star_points(77, cy, 16, 7), fill=WHITE)
        elif icon == "trophy":
            draw_trophy(draw, 77, cy, 13)
        text_left(draw, 110, y, label, row_font, WHITE)
        text_right(draw, 914, y, value, row_font, PINK)
    for y in (771, 809, 847):
        draw.line([110, y, 914, y], fill=ROW_LINE, width=1)

    # ---- loading bar + quote ----------------------------------------
    load_font = find_font(28)
    text_center(draw, 512, 900, "LOADING VICE CITY...", load_font, PINK)
    draw.rounded_rectangle([200, 936, 780, 960], radius=12,
                           outline=PINK, width=3, fill=(30, 10, 25, 255))
    draw.rounded_rectangle([203, 939, 771, 957], radius=10, fill=PINK)
    draw.text((792, 934), "99%", font=load_font, fill=WHITE)
    text_center(draw, 512, 972,
                "ROME WASN'T BUILT IN A DAY. NEITHER WAS VICE CITY.",
                font_regular(21), WHITE)

    img.convert("RGB").save(OUT, "PNG")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
