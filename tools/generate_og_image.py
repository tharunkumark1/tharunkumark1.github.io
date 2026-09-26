"""Generate the Open Graph / social preview card for the profile page.

1200x630 is the size LinkedIn, X, Slack and WhatsApp render best. Colours match
the site hero gradient defined in _sass/custom.scss.
"""

from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
OUT = "assets/images/og-profile.png"

NAVY_START = (0, 43, 91)      # #002b5b
NAVY_END = (10, 61, 117)      # #0a3d75
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REGULAR = os.path.join(FONT_DIR, "DejaVuSans.ttf")

NAME = "Tharun Kumar Ksheerasagar"
ROLE = "Senior Architect — System Architecture & Hardware Simulation"
LOCATION = "Hyderabad, India"


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


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img = gradient(W, H, NAVY_START, NAVY_END)
    draw = ImageDraw.Draw(img)

    margin = 80
    inner_w = W - 2 * margin

    name_font = fit(draw, NAME, BOLD, 68, inner_w)
    role_font = fit(draw, ROLE, REGULAR, 34, inner_w)
    loc_font = ImageFont.truetype(REGULAR, 26)

    y = 168
    draw.text((margin, y), NAME, font=name_font, fill=WHITE)
    y += name_font.size + 26

    draw.text((margin, y), ROLE, font=role_font, fill=(214, 226, 240))
    y += role_font.size + 34

    # Hairline divider, echoing the section rules on the page.
    draw.rectangle([margin, y, margin + 96, y + 3], fill=(120, 165, 214))
    y += 40

    draw.text((margin, y), LOCATION, font=loc_font, fill=(176, 199, 224))

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT}  {img.size[0]}x{img.size[1]}  {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
