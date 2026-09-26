#!/usr/bin/env python3
"""Generate the Open Graph / social preview card for the profile page.

1200x630 is the size LinkedIn, X, Slack and WhatsApp render best. Colours match
the site hero gradient defined in _sass/custom.scss.

The portrait is composited as a circle on the right, matching the hero avatar.
Run tools/prepare_profile_image.py first to produce assets/images/profile.jpg;
if that file is missing the card is still generated, text-only.

Usage:
    python3 tools/generate_og_image.py
    python3 tools/generate_og_image.py --photo assets/images/profile.jpg
"""

import argparse
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

W, H = 1200, 630
OUT = os.path.join(ROOT, "assets", "images", "og-profile.png")
DEFAULT_PHOTO = os.path.join(ROOT, "assets", "images", "profile.jpg")

NAVY_START = (0, 43, 91)      # #002b5b
NAVY_END = (10, 61, 117)      # #0a3d75
WHITE = (255, 255, 255)
MUTED_ROLE = (214, 226, 240)
MUTED_LOC = (176, 199, 224)
RULE = (120, 165, 214)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REGULAR = os.path.join(FONT_DIR, "DejaVuSans.ttf")

NAME_LINES = ["Tharun Kumar", "Ksheerasagar"]
ROLE = "Senior Architect — System Architecture & Hardware Simulation"
LOCATION = "Hyderabad, India"

MARGIN = 72
PHOTO_D = 300          # circle diameter
PHOTO_CX = 966
PHOTO_CY = 315
PHOTO_RING = 6         # white ring, mirrors the hero avatar border


def gradient(width, height, c1, c2):
    """Diagonal gradient, matching linear-gradient(135deg, ...) in CSS."""
    base = Image.new("RGB", (width, height), c1)
    draw = ImageDraw.Draw(base)
    span = width + height
    for i in range(span):
        t = i / (span - 1)
        colour = tuple(round(c1[j] + (c2[j] - c1[j]) * t) for j in range(3))
        draw.line([(i, 0), (0, i)], fill=colour)
    return base


def fit(draw, text, path, max_size, max_width):
    """Shrink font until the text fits max_width."""
    size = max_size
    while size > 16:
        font = ImageFont.truetype(path, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 2
    return ImageFont.truetype(path, size)


def fit_lines(draw, lines, path, max_size, max_width):
    """Shrink font until the widest of several lines fits max_width."""
    size = max_size
    while size > 16:
        font = ImageFont.truetype(path, size)
        if all(draw.textlength(line, font=font) <= max_width for line in lines):
            return font
        size -= 2
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, max_width):
    """Greedy word wrap to max_width."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if not current or draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paste_circle(canvas, photo, cx, cy, diameter, ring, ring_colour=WHITE):
    """Composite a circular portrait with a thin ring, centred on cx/cy."""
    plate = Image.new("RGBA", (diameter + 2 * ring, diameter + 2 * ring), (0, 0, 0, 0))
    ImageDraw.Draw(plate).ellipse(
        (0, 0, diameter + 2 * ring - 1, diameter + 2 * ring - 1), fill=ring_colour + (255,)
    )
    mask = Image.new("L", (diameter, diameter), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, diameter - 1, diameter - 1), fill=255)
    face = photo.convert("RGB").resize((diameter, diameter), Image.LANCZOS)
    plate.paste(face, (ring, ring), mask)
    canvas.paste(plate, (cx - diameter // 2 - ring, cy - diameter // 2 - ring), plate)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--photo", default=DEFAULT_PHOTO, help="square portrait to composite")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img = gradient(W, H, NAVY_START, NAVY_END)
    draw = ImageDraw.Draw(img)

    photo = None
    if os.path.exists(args.photo):
        photo = Image.open(args.photo)
        paste_circle(img, photo, PHOTO_CX, PHOTO_CY, PHOTO_D, PHOTO_RING)
    else:
        print(f"note: {os.path.relpath(args.photo, ROOT)} not found, generating text-only card")

    text_w = (PHOTO_CX - PHOTO_D // 2) - MARGIN - 48 if photo else W - 2 * MARGIN

    name_font = fit_lines(draw, NAME_LINES, BOLD, 64, text_w)
    role_font = ImageFont.truetype(REGULAR, 28)
    role_lines = wrap(draw, ROLE, role_font, text_w)
    loc_font = ImageFont.truetype(REGULAR, 26)

    name_lh = int(name_font.size * 1.18)
    role_lh = int(role_font.size * 1.34)
    block = (
        name_lh * len(NAME_LINES)
        + 20
        + role_lh * len(role_lines)
        + 30
        + 3
        + 30
        + 30
    )
    y = max(0, (H - block) // 2)

    for line in NAME_LINES:
        draw.text((MARGIN, y), line, font=name_font, fill=WHITE)
        y += name_lh

    y += 20
    for line in role_lines:
        draw.text((MARGIN, y), line, font=role_font, fill=MUTED_ROLE)
        y += role_lh

    y += 30
    # Hairline divider, echoing the section rules on the page.
    draw.rectangle([MARGIN, y, MARGIN + 96, y + 3], fill=RULE)

    y += 30
    draw.text((MARGIN, y), LOCATION, font=loc_font, fill=MUTED_LOC)

    img.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {os.path.relpath(OUT, ROOT)}  {img.size[0]}x{img.size[1]}  {size / 1024:.1f} KB")
    if photo:
        print(f"      portrait {os.path.relpath(args.photo, ROOT)}  {photo.size[0]}x{photo.size[1]}")


if __name__ == "__main__":
    main()
