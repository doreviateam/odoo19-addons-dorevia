# -*- coding: utf-8 -*-
"""Toolbar boutique — filmstrip rayons métier uniquement (Micro-lot 3A)."""

from odoo.addons.dorevia_ck_marketone_content.nav_v22_config import (
    NAV_ARTISANAT_LABEL,
    NAV_BOISSONS_LABEL,
    NAV_EPICERIE_LABEL,
    NAV_MAISON_LABEL,
    RAYON_ROOT_ALIASES,
)

CK_QA_CATEGORY_NAME_PREFIXES = (
    'CK Sparse Grid QA',
)

# Ordre filmstrip MOA (Épicerie → Soin → Artisanat → Boissons).
CK_TOOLBAR_FILMSTRIP_ORDER = (
    NAV_EPICERIE_LABEL,
    NAV_MAISON_LABEL,
    NAV_ARTISANAT_LABEL,
    NAV_BOISSONS_LABEL,
)


def ck_toolbar_allowed_category_names():
    names = set()
    for nav_label in CK_TOOLBAR_FILMSTRIP_ORDER:
        names.update(RAYON_ROOT_ALIASES.get(nav_label, (nav_label,)))
    return frozenset(names)


def is_ck_qa_public_category(category):
    name = category.name or ''
    return any(name.startswith(prefix) for prefix in CK_QA_CATEGORY_NAME_PREFIXES)


def _ck_toolbar_sort_key(category):
    for idx, nav_label in enumerate(CK_TOOLBAR_FILMSTRIP_ORDER):
        aliases = RAYON_ROOT_ALIASES.get(nav_label, (nav_label,))
        if category.name in aliases:
            return (idx, category.sequence, category.id)
    return (len(CK_TOOLBAR_FILMSTRIP_ORDER), category.sequence, category.id)


def filter_ck_toolbar_categories(categories):
    """Retourne uniquement les racines rayons métier visibles dans le filmstrip /shop."""
    if not categories:
        return categories
    allowed = ck_toolbar_allowed_category_names()
    return categories.filtered(
        lambda c: c.name in allowed and not is_ck_qa_public_category(c)
    ).sorted(key=_ck_toolbar_sort_key)


def purge_ck_qa_public_categories(env):
    """Supprime catégories et produits résidus QA (post-migrate / ops)."""
    Category = env['product.public.category'].sudo()
    Product = env['product.template'].sudo()
    qa_cats = Category.search([('name', 'ilike', 'CK Sparse Grid QA%')])
    if not qa_cats:
        return 0
    products = Product.search([('public_categ_ids', 'in', qa_cats.ids)])
    products.unlink()
    count = len(qa_cats)
    qa_cats.unlink()
    return count
