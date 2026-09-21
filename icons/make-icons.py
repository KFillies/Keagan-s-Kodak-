#!/usr/bin/env python3
"""iOS home-screen icons.

iOS applies its own rounded mask, so unlike the macOS icon these are drawn
full bleed with no squircle and no shadow. Same mark: one sunset, cut into
three slides that still line up.
"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFilter

SS = 4
SIZE = 1024 * SS


def lerp(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def vertical_gradient(size, stops):
    w, h = size
    img = Image.new("RGB", (1, h))
    px = img.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        lo, hi = stops[0], stops[-1]
        for i in range(len(stops) - 1):
            if stops[i][0] <= t <= stops[i + 1][0]:
                lo, hi = stops[i], stops[i + 1]
                break
        span = max(hi[0] - lo[0], 1e-6)
        px[0, y] = lerp(lo[1], hi[1], (t - lo[0]) / span)
    return img.resize((w, h), Image.NEAREST)


def build_scene(size):
    w, h = size
    scene = vertical_gradient((w, h), [
        (0.00, (255, 209, 148)),
        (0.34, (255, 138, 112)),
        (0.66, (196, 94, 140)),
        (1.00, (58, 52, 112)),
    ]).convert("RGBA")

    sun_r = int(h * 0.15)
    cx, cy = int(w * 0.38), int(h * 0.42)
    glow = Image.new("RGBA", size, (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse(
        [cx - sun_r * 3, cy - sun_r * 3, cx + sun_r * 3, cy + sun_r * 3],
        fill=(255, 226, 170, 70))
    scene = Image.alpha_composite(scene, glow.filter(ImageFilter.GaussianBlur(sun_r * 0.9)))

    draw = ImageDraw.Draw(scene, "RGBA")
    draw.ellipse([cx - sun_r, cy - sun_r, cx + sun_r, cy + sun_r], fill=(255, 243, 214, 255))

    def wave(t, base, terms):
        return base + sum(a * math.sin(f * t + p) for a, f, p in terms)

    steps = 160
    for base, terms, colour in (
        (0.66, [(0.045, 3.1, 0.6), (0.022, 6.4, 2.2)], (104, 74, 128, 255)),
        (0.80, [(0.055, 2.2, 1.9), (0.018, 4.7, 0.3)], (46, 38, 78, 255)),
    ):
        pts = [(w * i / steps, h * wave(i / steps, base, terms)) for i in range(steps + 1)]
        draw.polygon(pts + [(w, h), (0, h)], fill=colour)

    return scene


# The plate the three slides sit on. Light is the default icon; dark is for
# use against a black background, where a near-white plate reads as a glare.
PLATES = {
    "light": [(0.0, (250, 250, 252)), (1.0, (222, 223, 232))],
    "dark":  [(0.0, (44, 44, 46)),    (1.0, (22, 22, 26))],
}


def build_icon(plate="light"):
    # Full bleed backing, so iOS's mask never reveals a transparent corner.
    icon = vertical_gradient((SIZE, SIZE), PLATES[plate]).convert("RGBA")

    inset = int(SIZE * 0.115)
    gap = int(SIZE * 0.036)
    inner_w = inner_h = SIZE - inset * 2
    panel_w = (inner_w - gap * 2) // 3
    panel_radius = int(SIZE * 0.05)

    scene = build_scene((inner_w, inner_h))
    mask = Image.new("L", (inner_w, inner_h), 0)
    mdraw = ImageDraw.Draw(mask)
    for i in range(3):
        x0 = i * (panel_w + gap)
        mdraw.rounded_rectangle([x0, 0, x0 + panel_w, inner_h - 1],
                                radius=panel_radius, fill=255)

    icon.paste(scene, (inset, inset), mask)
    return icon


def main():
    here = os.path.dirname(os.path.abspath(__file__))

    master = build_icon("light").resize((1024, 1024), Image.LANCZOS)
    for size in (180, 192, 512, 1024):
        master.resize((size, size), Image.LANCZOS).save(
            os.path.join(here, f"icon-{size}.png"))

    dark = build_icon("dark").resize((1024, 1024), Image.LANCZOS)
    for size in (180, 512):
        dark.resize((size, size), Image.LANCZOS).save(
            os.path.join(here, f"icon-dark-{size}.png"))

    # Maskable variant: same art, extra breathing room for Android's safe zone.
    pad = Image.new("RGBA", (1024, 1024), (246, 246, 250, 255))
    inner = master.resize((820, 820), Image.LANCZOS)
    pad.paste(inner, (102, 102), inner)
    pad.save(os.path.join(here, "icon-maskable-512.png"))
    print("icons written to", here)


if __name__ == "__main__":
    main()
