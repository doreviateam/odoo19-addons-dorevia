# -*- coding: utf-8 -*-
"""Catalogue CK — produit coffret découverte pour le bloc home Lot 3."""
import base64
from pathlib import Path

from .ck_product_placeholders import is_tiny_product_image
from .home_discovery_pack import (
    DISCOVERY_PACK_EDITORIAL_NAME,
    DISCOVERY_PACK_EDITORIAL_TEASER,
    DISCOVERY_PACK_STATIC_IMAGE,
)

DISCOVERY_PACK_PRODUCT_NAME = DISCOVERY_PACK_EDITORIAL_NAME
DISCOVERY_PACK_LIST_PRICE = 29.9


def _discovery_pack_image_b64():
    try:
        from .catalog_seed import load_catalog_image_b64
        return load_catalog_image_b64('coffret_decouverte.webp')
    except OSError:
        pass
    image_path = Path(__file__).resolve().parent / 'static' / 'img' / 'ck_discovery_pack.jpg'
    return base64.b64encode(image_path.read_bytes())


def bootstrap_catalog_discovery_pack_product(env):
    """Assure un coffret publié avec image — alimente ``get_discovery_pack_product()``."""
    Template = env['product.template'].sudo()
    product = Template.search([('name', '=', DISCOVERY_PACK_PRODUCT_NAME)], limit=1)
    image_b64 = _discovery_pack_image_b64()
    vals = {
        'name': DISCOVERY_PACK_PRODUCT_NAME,
        'is_published': True,
        'website_published': True,
        'sale_ok': True,
        'list_price': DISCOVERY_PACK_LIST_PRICE,
        'description_sale': DISCOVERY_PACK_EDITORIAL_TEASER,
    }
    if not product:
        vals['image_1920'] = image_b64
        Template.create(vals)
        return True
    if is_tiny_product_image(product.image_1920):
        vals['image_1920'] = image_b64
    product.write(vals)
    return True
