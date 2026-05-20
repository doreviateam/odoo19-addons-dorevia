#!/usr/bin/env python3
"""Pré-traitement source RGBA → fond plein avant normalisation v1.1.

Usage (hôte) :
    python scripts/reprocess_rgba_source_flat.py \\
      --source tools/ck_image_normalizer/input/pilote/02_product-8_crackers-manioc-sainte-anne.png \\
      --output /tmp/crackers8_flat.png
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def flatten_rgba_on_background(
    source: Path,
    dest: Path,
    background: str = "#F8EEDB",
    remove_green_spill: bool = True,
) -> Path:
    bg_rgb = hex_to_rgb(background)
    rgba = Image.open(source).convert("RGBA")
    content_bbox = rgba.getchannel("A").getbbox()
    if content_bbox:
        rgba = rgba.crop(content_bbox)
    flat = Image.new("RGB", rgba.size, bg_rgb)
    flat.paste(rgba, mask=rgba.split()[3])

    if remove_green_spill:
        pixels = flat.load()
        w, h = flat.size
        for y in range(h):
            for x in range(w):
                r, g, b = pixels[x, y]
                if _color_distance_px(r, g, b, bg_rgb) <= 18:
                    continue
                if g > 95 and g > r + 25 and g > b + 25:
                    pixels[x, y] = bg_rgb
                elif b > 110 and b > r + 35 and g > r + 15:
                    pixels[x, y] = bg_rgb

    dest.parent.mkdir(parents=True, exist_ok=True)
    flat.save(dest, format="PNG")
    return dest


def _color_distance_px(r: int, g: int, b: int, ref: tuple[int, int, int]) -> float:
    return ((r - ref[0]) ** 2 + (g - ref[1]) ** 2 + (b - ref[2]) ** 2) ** 0.5


def main() -> int:
    parser = argparse.ArgumentParser(description="Aplatir RGBA sur fond plein recette v1.1")
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--background", default="#F8EEDB")
    args = parser.parse_args()
    flatten_rgba_on_background(args.source, args.output, args.background)
    print(f"OK flat RGB → {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
