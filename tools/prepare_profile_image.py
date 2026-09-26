#!/usr/bin/env python3
"""Derive the web image assets from the source portrait in ../tex.

The source is 4:5 (1080x1280), so a square crop keeps the full width and only the
vertical anchor moves. Three anchors were rendered as previews and C was chosen,
because it leaves headroom above the head:

    A  --offset 0    face sits at ~60% height (tight, low)
    B  --offset 100  face sits at ~51% height (centred)
    C  --offset 200  face sits at ~42% height (default)

Nothing is ever upscaled: the crop is full-width, and both outputs are
downsampled from it.

Usage:
    python3 tools/prepare_profile_image.py              # default anchor C
    python3 tools/prepare_profile_image.py --offset 100 # switch to anchor B
    python3 tools/prepare_profile_image.py --src /path/to/photo.jpg
"""

import argparse
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

DEFAULT_SRC = os.path.join(ROOT, "..", "tex", "Tharun_image.jpeg")
OUT_PROFILE = os.path.join(ROOT, "assets", "images", "profile.jpg")
OUT_ICON = os.path.join(ROOT, "assets", "images", "apple-touch-icon.png")

# 600px is already ~1.3x oversampled for a 150px avatar on a 3x display, so a
# larger master would only add weight to every page load.
PROFILE_SIZE = 600
ICON_SIZE = 180
JPEG_QUALITY = 85
DEFAULT_OFFSET = 200


def square_crop(img, offset):
    """Full-width square crop, `offset` px from the top of the source."""
    width, height = img.size
    side = min(width, height)
    left = (width - side) // 2
    top = max(0, min(height - side, offset))
    return img.crop((left, top, left + side, top + side))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--src", default=DEFAULT_SRC, help="source portrait")
    parser.add_argument(
        "--offset",
        type=int,
        default=DEFAULT_OFFSET,
        help="square crop offset from the top, in source pixels",
    )
    args = parser.parse_args()

    source = Image.open(args.src).convert("RGB")
    side = min(source.size)
    print(f"source  {os.path.relpath(args.src, ROOT)}  {source.size[0]}x{source.size[1]}")
    print(f"crop    {side}x{side} at offset {args.offset}px from top")

    crop = square_crop(source, args.offset)
    os.makedirs(os.path.dirname(OUT_PROFILE), exist_ok=True)

    # Hero avatar and the source for the social card. Progressive + optimised so
    # it paints sensibly on slow connections.
    crop.resize((PROFILE_SIZE, PROFILE_SIZE), Image.LANCZOS).save(
        OUT_PROFILE, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True
    )

    # iOS applies its own squircle mask to apple-touch-icon, so this has to stay
    # full-bleed: no alpha, no pre-rounded corners, no transparent padding.
    crop.resize((ICON_SIZE, ICON_SIZE), Image.LANCZOS).save(OUT_ICON, "PNG", optimize=True)

    for path in (OUT_PROFILE, OUT_ICON):
        with Image.open(path) as out:
            dims = f"{out.size[0]}x{out.size[1]}"
        size_kb = os.path.getsize(path) / 1024
        print(f"wrote   {os.path.relpath(path, ROOT)}  {dims}  {size_kb:.1f} KB")


if __name__ == "__main__":
    main()
