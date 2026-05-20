# -*- coding: utf-8 -*-
"""Seed 23 produits catalogue — extension 27 → 50 SKU (ckr-marketone-01).

Usage (depuis l'hôte) :

    docker exec -i sandbox-odoo19-odoo-1 odoo shell -c /etc/odoo/odoo.conf \\
      -d ckr-marketone-01 --no-http < /mnt/odoo19-addons-dorevia/dorevia_ckreyol_marketone/scripts/seed_catalogue_extension_23.py

Idempotent : ignore les produits déjà présents (nom ou default_code).
"""

import base64
from pathlib import Path

ASSETS = Path("/mnt/odoo19-addons-dorevia/dorevia_ckreyol_marketplace/docs/assets")
Product = env["product.template"].sudo()
ATTR_ORIGIN = env["product.attribute"].sudo().browse(3)

ORIGIN = {
    "Guadeloupe": 19,
    "Martinique": 20,
    "La Réunion": 51,
}

CAT = {
    "incontournables": 11,
    "aperitif": 68,
    "assaisonnements": 69,
    "biscuits_sales": 70,
    "biscuits_sucres": 71,
    "boissons": 72,
    "condiments": 73,
    "confitures": 74,
    "manioc": 75,
    "epices": 83,
    "farines": 76,
    "fecules": 77,
    "cadeaux": 78,
    "kits": 79,
    "miels": 80,
    "sauces": 81,
    "sirops": 82,
}


def load_image(filename):
    path = ASSETS / filename
    if not path.is_file():
        return False
    return base64.b64encode(path.read_bytes())


def categ_ids(*keys):
    return [CAT[k] for k in keys]


def create_product(spec):
    name = spec["name"]
    code = spec["code"]
    existing = Product.search(
        ["|", ("name", "=", name), ("default_code", "=", code)], limit=1
    )
    if existing:
        print("SKIP exists", existing.id, existing.name)
        return existing

    vals = {
        "name": name,
        "default_code": code,
        "list_price": spec["price"],
        "sale_ok": True,
        "website_published": True,
        "public_categ_ids": [(6, 0, categ_ids(*spec["categs"]))],
        "attribute_line_ids": [
            (
                0,
                0,
                {
                    "attribute_id": ATTR_ORIGIN.id,
                    "value_ids": [(6, 0, [ORIGIN[spec["origin"]]])],
                },
            )
        ],
    }
    img = load_image(spec.get("image", ""))
    if img:
        vals["image_1920"] = img

    product = Product.create(vals)
    print("CREATED", product.id, product.name, "img", bool(img))
    return product


PRODUCTS = [
    {
        "name": "Sauce scotch bonnet créole",
        "code": "CK-MO-028",
        "price": 7.90,
        "origin": "Martinique",
        "categs": ("incontournables", "aperitif", "sauces"),
        "image": "stitch_scotch_bonnet_sauce.png",
    },
    {
        "name": "Confiture goyave rose",
        "code": "CK-MO-029",
        "price": 6.50,
        "origin": "Guadeloupe",
        "categs": ("incontournables", "confitures", "cadeaux"),
        "image": "stitch_guava_jam_jar.png",
    },
    {
        "name": "Pochette curry des Antilles",
        "code": "CK-MO-030",
        "price": 5.90,
        "origin": "Martinique",
        "categs": ("incontournables", "epices"),
        "image": "stitch_curry_powder_pouch.png",
    },
    {
        "name": "Marinade jerk citron vert",
        "code": "CK-MO-031",
        "price": 8.20,
        "origin": "Martinique",
        "categs": ("incontournables", "aperitif", "assaisonnements"),
        "image": "stitch_jerk_marinade_bottle.png",
    },
    {
        "name": "Biscuits banane confiture",
        "code": "CK-MO-032",
        "price": 4.80,
        "origin": "Guadeloupe",
        "categs": ("incontournables", "biscuits_sucres"),
        "image": "hero_reference_direction_a_biscuits_confiture.png",
    },
    {
        "name": "Palettes coco vanille",
        "code": "CK-MO-033",
        "price": 5.20,
        "origin": "Martinique",
        "categs": ("incontournables", "biscuits_sucres", "cadeaux"),
        "image": "homepage_maniocookies_sale_la_platine.png",
    },
    {
        "name": "Chips patate douce créole",
        "code": "CK-MO-034",
        "price": 3.90,
        "origin": "Guadeloupe",
        "categs": ("incontournables", "aperitif", "biscuits_sales"),
        "image": "homepage_manioc_crackers_sale_ste_anne.png",
    },
    {
        "name": "Crackers sarrasin Réunion",
        "code": "CK-MO-035",
        "price": 4.50,
        "origin": "La Réunion",
        "categs": ("incontournables", "biscuits_sales"),
        "image": "exemple_produit_manioc_crackers_la_platine.png",
    },
    {
        "name": "Sauce chien antillaise",
        "code": "CK-MO-036",
        "price": 6.80,
        "origin": "Guadeloupe",
        "categs": ("incontournables", "aperitif", "condiments"),
        "image": "stitch_tropical_spread.png",
    },
    {
        "name": "Tapenade agrumes confits",
        "code": "CK-MO-037",
        "price": 7.40,
        "origin": "Martinique",
        "categs": ("incontournables", "condiments"),
        "image": "stitch_caribbean_spread.png",
    },
    {
        "name": "Confiture christophine gingembre",
        "code": "CK-MO-038",
        "price": 6.90,
        "origin": "Guadeloupe",
        "categs": ("incontournables", "confitures"),
        "image": "mvp02_reference_confitures_tropicaux_panier.png",
    },
    {
        "name": "Confiture papaye muscovado",
        "code": "CK-MO-039",
        "price": 7.10,
        "origin": "La Réunion",
        "categs": ("incontournables", "confitures", "cadeaux"),
        "image": "mvp02_reference_tropical_panier_fleurs_plage.png",
    },
    {
        "name": "Quatre épices créoles",
        "code": "CK-MO-040",
        "price": 5.50,
        "origin": "Guadeloupe",
        "categs": ("incontournables", "epices"),
        "image": "mvp02_reference_epices_curry_piments.png",
    },
    {
        "name": "Poudre colombo créole",
        "code": "CK-MO-041",
        "price": 5.80,
        "origin": "Martinique",
        "categs": ("incontournables", "epices"),
        "image": "mvp02_reference_epicerie_verre_etagere.png",
    },
    {
        "name": "Bouillon légumes des îles",
        "code": "CK-MO-042",
        "price": 4.20,
        "origin": "Guadeloupe",
        "categs": ("incontournables", "assaisonnements"),
        "image": "stitch_caribbean_kitchen.png",
    },
    {
        "name": "Rougail tomate créole",
        "code": "CK-MO-043",
        "price": 6.30,
        "origin": "La Réunion",
        "categs": ("incontournables", "assaisonnements"),
        "image": "stitch_hero_ambiance_food.png",
    },
    {
        "name": "Sirop jambosier",
        "code": "CK-MO-044",
        "price": 8.90,
        "origin": "Martinique",
        "categs": ("incontournables", "sirops", "aperitif"),
        "image": "stitch_hero_pantry_shelf.png",
    },
    {
        "name": "Sirop banane flambée",
        "code": "CK-MO-045",
        "price": 8.50,
        "origin": "Guadeloupe",
        "categs": ("incontournables", "sirops"),
        "image": "mvp02_reference_miel_pot_mains.png",
    },
    {
        "name": "Jus goyave passion",
        "code": "CK-MO-046",
        "price": 4.90,
        "origin": "Guadeloupe",
        "categs": ("incontournables", "boissons"),
        "image": "stitch_tropical_spread.png",
    },
    {
        "name": "Infusion bois bandé",
        "code": "CK-MO-047",
        "price": 5.60,
        "origin": "Martinique",
        "categs": ("incontournables", "boissons"),
        "image": "stitch_caribbean_kitchen.png",
    },
    {
        "name": "Farine banane plantain",
        "code": "CK-MO-048",
        "price": 6.20,
        "origin": "Guadeloupe",
        "categs": ("incontournables", "farines", "manioc"),
        "image": "homepage_manioc_pates_mayotte_la_platine.png",
    },
    {
        "name": "Flocons manioc instantanés",
        "code": "CK-MO-049",
        "price": 5.40,
        "origin": "La Réunion",
        "categs": ("incontournables", "fecules", "manioc"),
        "image": "homepage_manioc_pates_mayotte_la_platine.png",
    },
    {
        "name": "Miel polyfloral créole",
        "code": "CK-MO-050",
        "price": 9.90,
        "origin": "Martinique",
        "categs": ("incontournables", "miels", "cadeaux"),
        "image": "mvp02_reference_miel_pot_mains.png",
    },
]

for spec in PRODUCTS:
    create_product(spec)

env.cr.commit()

total = Product.search_count(
    [("active", "=", True), ("sale_ok", "=", True), ("website_published", "=", True)]
)
print("TOTAL PUBLISHED", total)
