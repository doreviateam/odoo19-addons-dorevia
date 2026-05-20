#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Applique les décisions MOA revue visuelle validated_grid (statuts uniquement).

Usage dry-run :

    docker exec -i sandbox-odoo19-odoo-1 odoo shell -c /etc/odoo/odoo.conf \\
      -d ckr-marketone-01 --no-http <<'EOF'
exec(open("/mnt/odoo19-addons-dorevia/dorevia_ckreyol_marketone/scripts/apply_moa_revue_visuelle.py").read())
run_apply(env, apply=False)
EOF

Usage apply :

    run_apply(env, apply=True)
"""

from __future__ import annotations

import csv
from pathlib import Path

DECISION_TO_STATUS = {
    "validated_grid": "validated_grid",
    "validated_storage": "validated_storage",
    "needs_review_source": "needs_review_source",
    # Doctrine v2 — pas de statut Odoo dédié ; fallback = pending_review sans tuile.
    "fallback_master": "pending_review",
    "exclusion_temporaire": "pending_review",
}

DEFAULT_MANIFEST = Path(
    "/mnt/odoo19-addons-dorevia/dorevia_ckreyol_marketone/docs/recette/boutique"
    "/TRAME_REVUE_VISUELLE_MOA_PRODUIT_PAR_PRODUIT.csv"
)


def _repo_manifest() -> Path:
    module_file = globals().get("__file__")
    candidates = []
    if module_file:
        candidates.append(
            Path(module_file).resolve().parents[1]
            / "docs/recette/boutique/TRAME_REVUE_VISUELLE_MOA_PRODUIT_PAR_PRODUIT.csv"
        )
    candidates.append(DEFAULT_MANIFEST)
    for path in candidates:
        if path.is_file():
            return path
    return candidates[-1]


def _moa_note(row: dict) -> str:
    motif = (row.get("motif_principal") or "").strip()
    comment = (row.get("commentaire_moa") or "").strip()
    date = (row.get("date_revue_moa") or "").strip()
    prefix = f"MOA_REVUE_{date.replace('-', '')}" if date else "MOA_REVUE"
    parts = [prefix, (row.get("decision_moa") or "").strip()]
    if motif:
        parts.append(motif)
    if comment:
        parts.append(comment)
    return " — ".join(parts)


def run_apply(env, manifest_path: str | Path | None = None, apply: bool = False) -> dict:
    manifest_path = Path(manifest_path or _repo_manifest())
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Manifest introuvable: {manifest_path}")

    Product = env["product.template"].sudo()
    summary = {
        "validated_grid": 0,
        "validated_storage": 0,
        "needs_review_source": 0,
        "fallback_master": 0,
        "error": 0,
        "lines": [],
    }

    with manifest_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    for row in rows:
        product_id = (row.get("product_id") or "").strip()
        decision = (row.get("decision_moa") or "").strip()
        name = (row.get("product_name") or product_id).strip()

        if not product_id or not decision:
            summary["error"] += 1
            summary["lines"].append(f"ERROR ligne incomplète: {name}")
            continue

        if decision not in DECISION_TO_STATUS:
            summary["error"] += 1
            summary["lines"].append(f"ERROR décision inconnue '{decision}' product {product_id}")
            continue

        product = Product.browse(int(product_id))
        if not product.exists():
            summary["error"] += 1
            summary["lines"].append(f"ERROR product.template/{product_id} introuvable")
            continue

        status = DECISION_TO_STATUS[decision]
        vals = {
            "shop_tile_status": status,
            "shop_tile_moa_note": _moa_note(row),
        }
        if decision == "fallback_master":
            vals["image_shop_tile"] = False

        before_use = product.marketone_use_shop_tile_on_grid()
        before_status = product.shop_tile_status
        before_tile = bool(product.image_shop_tile)
        before_1920 = bool(product.image_1920)

        if apply:
            product.write(vals)

        after_use = product.marketone_use_shop_tile_on_grid() if apply else (
            product._marketone_shop_tile_feature_enabled()
            and bool(product.image_shop_tile if decision != "fallback_master" else False)
            and status == "validated_grid"
        )
        after_status = status if apply else before_status
        after_tile = False if decision == "fallback_master" else before_tile

        action = "APPLY" if apply else "DRY-RUN"
        summary[decision] = summary.get(decision, 0) + 1
        summary["lines"].append(
            f"{action} {product.id}|{name}|decision={decision}|"
            f"status {before_status}->{after_status}|use_grid {before_use}->{after_use}|"
            f"tile {before_tile}->{after_tile}|1920={before_1920}"
        )

    if apply:
        env.cr.commit()

    print(f"Manifest: {manifest_path}")
    print(f"{'APPLY' if apply else 'DRY-RUN'}: {len(rows)} lignes")
    for key in ("validated_grid", "validated_storage", "needs_review_source", "fallback_master"):
        print(f"  {key}: {summary.get(key, 0)}")
    print(f"  error: {summary['error']}")
    for line in summary["lines"]:
        print(line)

    if apply:
        grid = Product.search_count([("shop_tile_status", "=", "validated_grid")])
        use_grid = Product.search([("shop_tile_status", "=", "validated_grid")])
        active = sum(1 for p in use_grid if p.marketone_use_shop_tile_on_grid())
        print(f"POST validated_grid count: {grid}")
        print(f"POST marketone_use_shop_tile_on_grid True: {active}")
        print(f"POST image_shop_tile count: {Product.search_count([('image_shop_tile', '!=', False)])}")

    return summary
