#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Import tuiles /shop validées MOA dans product.template.image_shop_tile.

Usage — validation dry-run (hors Odoo) :

    python scripts/import_shop_tiles.py \\
      --manifest docs/recette/boutique/import_pilote_43_shop_tiles.csv

Usage — import Odoo (dry-run par défaut) :

    docker exec -i sandbox-odoo19-odoo-1 odoo shell -c /etc/odoo/odoo.conf \\
      -d ckr-marketone-01 --no-http <<'EOF'
exec(open("/mnt/odoo19-addons-dorevia/dorevia_ckreyol_marketone/scripts/import_shop_tiles.py").read())
run_import(env, manifest_path="/mnt/odoo19-addons-dorevia/dorevia_ckreyol_marketone/docs/recette/boutique/import_pilote_43_shop_tiles.csv", apply=False)
EOF

Usage — import apply :

    ... run_import(..., apply=True)
"""

from __future__ import annotations

import argparse
import base64
import csv
import sys
from datetime import datetime
from pathlib import Path

ALLOWED_STATUS = {
    "validated_grid",
    "validated_storage",
    "validated_reserve",
    "pending_review",
    "needs_review_source",
    "rejected",
    # Legacy manifest pilote — remappé validated_storage à l'import.
    "validated",
}
IMPORTABLE_STORAGE_STATUSES = {
    "validated_storage",
    "validated_reserve",
    "pending_review",
    "needs_review_source",
    "rejected",
    "validated",
}
FORBIDDEN_IMPORT_FIELDS = frozenset({"image_1920", "image_1024", "image_512"})
RECIPE_VERSION = "ck_shop_tile_v1.1"
BLOCKED_RECIPE_VERSIONS = {"ck_shop_tile_v1.2-alpha", "ck_shop_tile_v1.2"}
BLOCKED_JPEG_SUFFIXES = {".png", ".webp"}


def _repo_root() -> Path:
    module_file = globals().get("__file__")
    if module_file:
        return Path(module_file).resolve().parents[1]
    return Path("/mnt/odoo19-addons-dorevia/dorevia_ckreyol_marketone")


def load_manifest(manifest_path: Path) -> list[dict]:
    rows = []
    with manifest_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows.append(row)
    return rows


def _jpeg_lookup_roots() -> list[Path]:
    """Racines pour résoudre source_jpeg_path (hôte vs conteneur recette)."""
    module = _repo_root()
    return [
        module.parent.parent,  # …/dorevia-saas sur l'hôte
        Path("/Users/doreviateam/dorevia-saas"),
        Path("/tmp/marketone_pilote_import"),
    ]


def resolve_jpeg_path(raw: str) -> Path:
    raw_path = Path(raw.strip())
    if raw_path.is_file():
        return raw_path

    rel: Path | None
    host_saas = Path("/Users/doreviateam/dorevia-saas")
    if raw_path.is_absolute():
        try:
            rel = raw_path.relative_to(host_saas)
        except ValueError:
            rel = None
    else:
        rel = raw_path

    if rel is not None:
        for root in _jpeg_lookup_roots():
            candidate = root / rel
            if candidate.is_file():
                return candidate
    return raw_path


def normalize_import_status(raw: str) -> str:
    """Doctrine v2 — legacy ``validated`` pilote → ``validated_storage``."""
    status = (raw or "").strip()
    if status == "validated":
        return "validated_storage"
    return status


def validate_manifest_rows(rows: list[dict]) -> list[str]:
    errors = []
    for idx, row in enumerate(rows, start=2):
        for forbidden in FORBIDDEN_IMPORT_FIELDS:
            if row.get(forbidden):
                errors.append(
                    f"Ligne {idx}: interdit d'importer {forbidden} "
                    f"(doctrine v2 — master inchangé)"
                )
        status = (row.get("shop_tile_status") or "").strip()
        if status not in ALLOWED_STATUS:
            errors.append(f"Ligne {idx}: statut non importable '{status}'")
        recipe_version = (row.get("shop_tile_recipe_version") or RECIPE_VERSION).strip()
        if recipe_version in BLOCKED_RECIPE_VERSIONS:
            errors.append(
                f"Ligne {idx}: recette alpha retirée du flux actif '{recipe_version}' "
                f"(doctrine image pleine v1.1 uniquement)"
            )
        jpeg = resolve_jpeg_path(row.get("source_jpeg_path") or "")
        if not jpeg.is_file():
            errors.append(f"Ligne {idx}: fichier JPEG introuvable '{jpeg}'")
        elif jpeg.suffix.lower() in BLOCKED_JPEG_SUFFIXES:
            errors.append(
                f"Ligne {idx}: format alpha interdit pour image_shop_tile '{jpeg.name}' "
                f"(JPEG v1.1 image pleine uniquement)"
            )
        if not (row.get("product_id") or row.get("default_code")):
            errors.append(f"Ligne {idx}: product_id ou default_code requis")
    return errors


def resolve_product(env, row: dict):
    Product = env["product.template"].sudo()
    default_code = (row.get("default_code") or "").strip()
    product_id = (row.get("product_id") or "").strip()
    reference = (row.get("reference") or "").strip()

    if default_code:
        product = Product.search([("default_code", "=", default_code)], limit=1)
        if product:
            return product
    if product_id:
        product = Product.browse(int(product_id))
        if product.exists():
            return product
    if reference:
        product = Product.search([("name", "=", reference)], limit=1)
        if product:
            return product
    return Product.browse()


def run_import(env, manifest_path: str | Path, apply: bool = False) -> dict:
    manifest_path = Path(manifest_path)
    rows = load_manifest(manifest_path)
    errors = validate_manifest_rows(rows)
    if errors:
        for err in errors:
            print("ERROR", err)
        raise SystemExit(1)

    summary = {"ok": 0, "skip": 0, "error": 0, "lines": []}
    for row in rows:
        product = resolve_product(env, row)
        ref_label = row.get("reference") or row.get("default_code") or row.get("product_id")
        if not product:
            summary["error"] += 1
            summary["lines"].append(f"ERROR not found: {ref_label}")
            continue

        jpeg_path = resolve_jpeg_path(row["source_jpeg_path"])
        if not jpeg_path.is_file():
            summary["error"] += 1
            summary["lines"].append(f"ERROR jpeg missing: {ref_label} ({jpeg_path})")
            continue
        image_b64 = base64.b64encode(jpeg_path.read_bytes()).decode("ascii")
        status = normalize_import_status(row["shop_tile_status"])
        vals = {
            "image_shop_tile": image_b64,
            "shop_tile_status": status,
            "shop_tile_recipe_version": row.get("shop_tile_recipe_version") or RECIPE_VERSION,
            "shop_tile_processed_at": datetime.utcnow(),
            "shop_tile_source_run": (row.get("shop_tile_source_run") or "").strip(),
            "shop_tile_moa_note": (row.get("shop_tile_moa_note") or "").strip() or False,
        }

        if apply:
            product.write(vals)
            action = "APPLY"
        else:
            action = "DRY-RUN"
        summary["ok"] += 1
        summary["lines"].append(
            f"{action} product.template/{product.id} {product.name} <- {jpeg_path.name}"
        )

    if apply and env is not None:
        env.cr.commit()

    print(f"Import {'apply' if apply else 'dry-run'}: {summary['ok']} ok, {summary['error']} errors")
    for line in summary["lines"]:
        print(line)
    return summary


def cli_validate_only(manifest_path: Path) -> int:
    rows = load_manifest(manifest_path)
    errors = validate_manifest_rows(rows)
    if errors:
        for err in errors:
            print("ERROR", err)
        return 1
    print(f"OK manifest {manifest_path}: {len(rows)} lignes importables")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Import tuiles /shop validées MOA")
    parser.add_argument(
        "--manifest",
        default=str(
            _repo_root()
            / "docs/recette/boutique/import_pilote_43_shop_tiles.csv"
        ),
        help="CSV manifest import pilote 43",
    )
    args = parser.parse_args(argv)
    return cli_validate_only(Path(args.manifest))


if __name__ == "__main__" and Path(sys.argv[0]).name == "import_shop_tiles.py":
    sys.exit(main())
