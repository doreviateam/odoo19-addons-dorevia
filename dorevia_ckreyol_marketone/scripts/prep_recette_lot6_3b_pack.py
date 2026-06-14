#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prépare la base recette MOA Lot 6.3b Kits & Coffrets sur ckr-marketone-01.

Usage (sandbox) :
  docker exec -i sandbox-odoo19-odoo-1 odoo shell -d ckr-marketone-01 --no-http \\
    < odoo19-addons-dorevia/dorevia_ckreyol_marketone/scripts/prep_recette_lot6_3b_pack.py

Configure :
- ≥ 2 produits ``pack_ok=True`` publiés avec composants ;
- ≥ 1 produit unitaire témoin (``pack_ok=False``) ;
- désactive ``pack_ok`` sur les autres produits recette précédents si marqués.
"""
MARKER = "[RECETTE_LOT6_3B]"


def _published_products(env, limit=8):
    return env["product.template"].search(
        [
            ("sale_ok", "=", True),
            ("is_published", "=", True),
        ],
        order="id asc",
        limit=limit,
    )


def _component(env, name, list_price=5.0):
    return env["product.product"].create(
        {
            "name": f"{MARKER} {name}",
            "type": "consu",
            "list_price": list_price,
        }
    )


def _configure_pack(template, component, label):
    template.write(
        {
            "pack_ok": True,
            "pack_type": "non_detailed",
            "pack_component_price": "ignored",
            "sale_ok": True,
            "is_published": True,
        }
    )
    variant = template.product_variant_id
    line = env["product.pack.line"].search(
        [
            ("parent_product_id", "=", variant.id),
            ("product_id", "=", component.id),
        ]
    )
    if not line:
        env["product.pack.line"].create(
            {
                "parent_product_id": variant.id,
                "product_id": component.id,
                "quantity": 1.0,
            }
        )
    print(f"  pack {label}: tmpl={template.id} name={template.name!r}")


def _clear_other_packs(env, keep_ids):
    others = env["product.template"].search(
        [
            ("pack_ok", "=", True),
            ("id", "not in", list(keep_ids)),
        ]
    )
    if others:
        others.write({"pack_ok": False})
        print(f"  cleared pack_ok on {len(others)} other template(s)")


products = _published_products(env)
if len(products) < 3:
    raise SystemExit("Pas assez de produits publiés (min 3).")

pack_a, pack_b, control = products[0], products[1], products[2]
comp_a = _component(env, "Composant Pack A")
comp_b = _component(env, "Composant Pack B")

_configure_pack(pack_a, comp_a, "A")
_configure_pack(pack_b, comp_b, "B")
control.write({"pack_ok": False, "sale_ok": True, "is_published": True})
_clear_other_packs(env, {pack_a.id, pack_b.id})

env.cr.commit()

pack_count = env["product.template"].search_count(
    [
        ("pack_ok", "=", True),
        ("sale_ok", "=", True),
        ("is_published", "=", True),
    ]
)
print("=== PREP RECETTE LOT 6.3b ===")
print(f"pack_products={[pack_a.id, pack_b.id]} names={[pack_a.name, pack_b.name]}")
print(f"control_product={control.id} name={control.name!r}")
print(f"published_pack_count={pack_count}")
print("URLs:")
print("  /kits")
print("  /shop?marketone_mode=pack")
print("  /shop (control — full catalog)")
