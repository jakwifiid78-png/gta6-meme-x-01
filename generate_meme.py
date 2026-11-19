#!/usr/bin/env python3
"""Generate the gta6-meme-x-01 meme image (1024x1024 PNG).

Concept: a GTA VI loading-screen parody. The player waited 13 years for
GTA 6; the make.fun ghost (the entrant's AI agent) spent those 13 years
earning real money in make.fun bounties instead. The ghost is the big
visual anchor (the judge's first criterion is make.fun in the picture),
the joke is GTA-specific, and the punchline sells make.fun in the joke's
own voice.

Built with Pillow only, from the make.fun press-kit ghost
(https://make.fun/press/mark-1024.png). Deterministic: fixed seed, no
network, no randomness that changes the output.

Usage: python3 generate_meme.py  (writes meme.png next to this script)
"""

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
OUT = HERE / "meme.png"

W, H = 1024, 1024

# make.fun brand pink, GTA sunset palette, high-contrast meme text.
MAGENTA = (226, 0, 122)
DARK_TOP = (26, 11, 46)
DARK_BOTTOM = (18, 6, 31)
SUNSET_MID = (176, 38, 106)
SUNSET_LOW = (255, 92, 88)
YELLOW = (255, 210, 63)
WHITE = (255, 255, 255)
BLACK = (10, 5, 18)


def find_font(bold=True):
    """Pick a heavy sans font available on this machine."""
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return path
    raise FileNotFoundError("no bold sans font found")


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vertical_gradient(size, stops):
    """stops: list of (position 0..1, rgb). Returns an RGB image."""
    img = Image.new("RGB", size)
    px = img.load()
    width, height = size
    for y in range(height):
        t = y / max(height - 1, 1)
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if p0 <= t <= p1:
                local = 0 if p1 == p0 else (t - p0) / (p1 - p0)
                colour = lerp(c0, c1, local)
                break
        else:
            colour = stops[-1][1]
        for x in range(width):
            px[x, y] = colour
    return img


def text_outlined(draw, centre_x, y, text, font, fill, outline=BLACK, width=4):
    """Centre-aligned text with a thick outline, meme style."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = centre_x - tw // 2
    for dx in range(-width, width + 1):
        for dy in range(-width, width + 1):
            if dx * dx + dy * dy <= width * width:
                draw.text((x + dx, y + dy), text, font=font, fill=outline)
    draw.text((x, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]


def main():
    rng = random.Random(20261119)
    font_path = find_font()

    # Sky: dark purple night at the top, Vice City sunset band low down.
    img = vertical_gradient(
        (W, H),
        [
            (0.00, DARK_TOP),
            (0.42, (58, 16, 72)),
            (0.58, SUNSET_MID),
            (0.72, SUNSET_LOW),
            (1.00, DARK_BOTTOM),
        ],
    )
    draw = ImageDraw.Draw(img, "RGBA")

    # Stars in the dark upper sky (fixed seed: deterministic).
    for _ in range(90):
        x = rng.randint(8, W - 8)
        y = rng.randint(8, 300)
        r = rng.choice([1, 1, 2])
        alpha = rng.randint(90, 200)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, alpha))

    # Leonida skyline silhouette: a thin strip above the brand bar, kept
    # clear of the joke text so nothing fights the punchline.
    skyline_base = 948
    x = -20
    while x < W + 20:
        bw = rng.randint(52, 110)
        bh = rng.randint(30, 58)
        draw.rectangle([x, skyline_base - bh, x + bw, skyline_base + 40],
                       fill=(16, 6, 28, 255))
        # A few lit windows so the skyline reads at small size.
        for _ in range(rng.randint(2, 6)):
            wx = rng.randint(x + 6, x + bw - 10)
            wy = rng.randint(skyline_base - bh + 8, skyline_base - 12)
            draw.rectangle([wx, wy, wx + 5, wy + 7], fill=(255, 210, 63, 220))
        x += bw + rng.randint(4, 18)

    # The make.fun ghost, big and centred: the judge's first criterion.
    ghost = Image.open(ASSETS / "mark-1024.png").convert("RGBA")
    ghost = ghost.resize((430, 430), Image.LANCZOS)
    # Soft drop shadow from the ghost's own alpha.
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow_ghost = Image.new("RGBA", ghost.size, (0, 0, 0, 0))
    alpha = ghost.split()[3]
    shadow_ghost.putalpha(alpha)
    black = Image.new("RGBA", ghost.size, (0, 0, 0, 160))
    shadow_ghost = Image.composite(black, shadow_ghost, alpha)
    shadow_ghost = shadow_ghost.filter(ImageFilter.GaussianBlur(14))
    shadow.paste(shadow_ghost, (297 + 10, 128 + 14), shadow_ghost)
    img = Image.alpha_composite(img.convert("RGBA"), shadow)
    img.paste(ghost, (297, 128), ghost)
    draw = ImageDraw.Draw(img, "RGBA")

    # Header: the game, loud and small, so the joke lands as GTA first.
    header_font = ImageFont.truetype(font_path, 46)
    text_outlined(draw, W // 2, 34, "GRAND THEFT AUTO VI", header_font,
                  fill=(255, 236, 170), width=3)

    # The joke: setup in white, punchline in make.fun yellow.
    big = ImageFont.truetype(font_path, 62)
    punch = ImageFont.truetype(font_path, 54)
    y = 592
    y += text_outlined(draw, W // 2, y, "I WAITED 13 YEARS", big, fill=WHITE) + 8
    y += text_outlined(draw, W // 2, y, "FOR GTA 6.", big, fill=WHITE) + 22
    y += text_outlined(draw, W // 2, y, "MY GHOST SPENT THEM", punch,
                       fill=YELLOW) + 6
    y += text_outlined(draw, W // 2, y, "GETTING PAID ON MAKE.FUN.", punch,
                       fill=YELLOW)

    # Bottom brand bar: the name, unmissable even at timeline size.
    draw.rectangle([0, 948, W, H], fill=MAGENTA + (255,))
    bar_font = ImageFont.truetype(font_path, 54)
    bbox = draw.textbbox((0, 0), "make.fun", font=bar_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 962), "make.fun", font=bar_font, fill=WHITE)

    img.convert("RGB").save(OUT, "PNG")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
