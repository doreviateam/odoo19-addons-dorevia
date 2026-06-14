#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prépare la base recette MOA Lot 6.3a Promo sur ckr-marketone-01.

Usage (sandbox) :
  docker exec sandbox-odoo19-odoo-1 odoo shell -d ckr-marketone-01 --no-http \\
    < /mnt/odoo19-addons-dorevia/dorevia_ckreyol_marketone/scripts/prep_recette_lot6_3a_promo.py

Crée :
- 2 items produit strictement réducteurs sur la pricelist visiteur public ;
- 1 produit témoin hors promo (aucun item actif réducteur) ;
- 1 item global ``3_global`` (option P6) — désactivé par défaut via date_end passée,
  activable BO pour le scénario P6.
"""
from datetime import datetime, timedelta

MARKER = "[RECETTE_LOT6_3A]"


def _visitor_pricelist(env):
    website = env["website"].search([], limit=1)
    pub = env.ref("base.public_partner")
    pl = pub.property_product_pricelist
    if not pl:
        pl = env["product.pricelist"].search([], limit=1)
        pub.property_product_pricelist = pl
    return website, pl, pub


def _published_products(env, limit=8):
    return env["product.template"].search(
        [
            ("sale_ok", "=", True),
            ("is_published", "=", True),
        ],
        order="id asc",
        limit=limit,
    )


def _remove_recette_items(env, pricelist, product_ids):
    Item = env["product.pricelist.item"].sudo()
    domain = [
        ("pricelist_id", "=", pricelist.id),
        "|",
        ("product_tmpl_id", "in", list(product_ids)),
        ("applied_on", "=", "3_global"),
    ]
    old = Item.search(domain)
    # Ne supprimer que nos items recette (percentage 15/20 sur ces produits ou global 5%)
    to_unlink = old.filtered(
        lambda i: (
            i.applied_on == "3_global"
            and i.compute_price == "percentage"
            and i.percent_price == 5.0
        )
        or (
            i.product_tmpl_id.id in product_ids
            and i.compute_price == "percentage"
            and i.percent_price in (15.0, 20.0)
        )
    )
    if to_unlink:
        to_unlink.unlink()


def _create_product_item(pricelist, product, percent=15.0, label=""):
    return env["product.pricelist.item"].sudo().create(
        {
            "name": f"{MARKER} {label} {product.name}"[:128],
            "pricelist_id": pricelist.id,
            "applied_on": "1_product",
            "product_tmpl_id": product.id,
            "compute_price": "percentage",
            "percent_price": percent,
            "date_start": False,
            "date_end": False,
        }
    )


def _create_global_item(pricelist, percent=5.0, active=True):
    vals = {
        "name": f"{MARKER} Global promo P6",
        "pricelist_id": pricelist.id,
        "applied_on": "3_global",
        "compute_price": "percentage",
        "percent_price": percent,
    }
    if active:
        vals["date_start"] = False
        vals["date_end"] = False
    else:
        end = datetime.now() - timedelta(days=1)
        vals["date_end"] = end.strftime("%Y-%m-%d %H:%M:%S")
    return env["product.pricelist.item"].sudo().create(vals)


website, pl, pub = _visitor_pricelist(env)
products = _published_products(env)
if len(products) < 3:
    raise SystemExit("Pas assez de produits publiés (min 3).")

promo_a, promo_b, control = products[0], products[1], products[2]

_remove_recette_items(env, pl, products.ids)
item_a = _create_product_item(pl, promo_a, percent=15.0, label="Promo A")
item_b = _create_product_item(pl, promo_b, percent=20.0, label="Promo B")
item_global = _create_global_item(pl, percent=5.0, active=False)

env.cr.commit()

ids = pl._marketone_get_promo_template_ids(pricelist=pl)
print("=== PREP RECETTE LOT 6.3a ===")
print(f"website_id={website.id} pricelist_id={pl.id} name={pl.name}")
print(f"promo_products={[promo_a.id, promo_b.id]} names={[promo_a.name, promo_b.name]}")
print(f"control_product={control.id} name={control.name}")
print(f"items={[item_a.id, item_b.id, item_global.id]}")
print(f"resolver_ids={ids}")
print("P6 global item created INACTIVE (date_end past) — id", item_global.id)
print("URLs:")
print("  /promotions")
print("  /shop?marketone_mode=promo")
print("  /shop (control — full catalog)")
