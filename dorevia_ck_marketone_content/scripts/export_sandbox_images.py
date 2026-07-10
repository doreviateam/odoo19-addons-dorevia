#!/usr/bin/env python3
"""Export images produit MOA depuis une sandbox Odoo → assets statiques catalog/.

Usage one-shot (extraction référence 18079) :

    python3 dorevia_ck_marketone_content/scripts/export_sandbox_images.py \\
        --base-url http://localhost:18079 \\
        --out-dir dorevia_ck_marketone_content/static/img/catalog

Ne pas utiliser en runtime deploy — outil d'extraction seed uniquement.
"""
from __future__ import annotations

import argparse
import io
import sys
import urllib.error
import urllib.request
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover
    raise SystemExit('Pillow requis : pip install Pillow') from exc

# Mapping figé — INVENTAIRE_CATALOGUE_SEED_18079.md §5
EXPORT_MAP = (
    ('confiture_goyave.webp', 'product.template', 3),
    ('manio_crackers_sale.webp', 'product.product', 21),
    ('manio_crackers_sweet.webp', 'product.product', 22),
    ('galettes_manioc.webp', 'product.template', 20),
    ('savon_vetiver.webp', 'product.template', 7),
    ('chapeau_panama.webp', 'product.template', 1076),
    ('pate_manioc.webp', 'product.template', 2336),
    ('jus_mont_pele.webp', 'product.template', 2593),
    ('tambour_gro_ka.webp', 'product.template', 4491),
    ('coffret_decouverte.webp', 'product.template', 4583),
)

IMAGE_FIELD = 'image_1024'
WEBP_QUALITY = 85
MIN_BYTES = 500


def _fetch_image(base_url: str, model: str, record_id: int) -> bytes:
    url = f'{base_url.rstrip("/")}/web/image/{model}/{record_id}/{IMAGE_FIELD}'
    req = urllib.request.Request(url, headers={'User-Agent': 'ck-export-sandbox-images/1.0'})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    if len(data) < MIN_BYTES:
        raise ValueError(f'image trop petite ({len(data)} o) — {url}')
    return data


def _to_webp(raw: bytes, dest: Path) -> None:
    with Image.open(io.BytesIO(raw)) as img:
        if img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGBA' if 'A' in img.getbands() else 'RGB')
        dest.parent.mkdir(parents=True, exist_ok=True)
        img.save(dest, format='WEBP', quality=WEBP_QUALITY, method=6)


def export_catalog(base_url: str, out_dir: Path) -> list[Path]:
    written: list[Path] = []
    for filename, model, record_id in EXPORT_MAP:
        dest = out_dir / filename
        raw = _fetch_image(base_url, model, record_id)
        _to_webp(raw, dest)
        written.append(dest)
        print(f'  ✓ {filename} ({len(raw)} o → {dest.stat().st_size} o webp)')
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Export images catalogue MOA depuis sandbox Odoo')
    parser.add_argument('--base-url', default='http://localhost:18079', help='URL sandbox (défaut 18079)')
    parser.add_argument(
        '--out-dir',
        type=Path,
        default=Path(__file__).resolve().parent.parent / 'static' / 'img' / 'catalog',
        help='Répertoire cible des .webp',
    )
    args = parser.parse_args(argv)
    print(f'Export {len(EXPORT_MAP)} images depuis {args.base_url} → {args.out_dir}')
    try:
        export_catalog(args.base_url, args.out_dir)
    except (urllib.error.URLError, ValueError, OSError) as err:
        print(f'ERREUR: {err}', file=sys.stderr)
        return 1
    print('Terminé.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
