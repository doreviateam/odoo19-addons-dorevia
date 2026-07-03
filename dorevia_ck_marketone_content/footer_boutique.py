# -*- coding: utf-8 -*-
"""CATALOG-ARCHI-001 Lot A §12.3 — colonne Boutique du footer pilotée par _is_ck_exposable().

Le footer réel (id `website.footer_custom`, nom BO « CK Footer Phase 1 »)
n'est pas un template QWeb CK dédié : c'est la vue standard Odoo, patchée au
runtime (même mécanisme que `bootstrap_footer_legal_links` dans hooks.py).
Avant ce lot, la colonne Boutique ne contenait que 2 liens statiques
(Tous les produits, Épicerie créole) — jamais Boissons/Soin/Artisanat.
"""
import logging
from xml.sax.saxutils import escape

_logger = logging.getLogger(__name__)

FOOTER_VIEW_KEY = 'website.footer_custom'
FOOTER_BOUTIQUE_MARKER = '<h5 class="mb-3">Boutique</h5>'
FOOTER_BOUTIQUE_ALL_LABEL = 'Tous les produits'
FOOTER_BOUTIQUE_ALL_URL = '/shop'


def _arch_as_string(arch):
    if isinstance(arch, dict):
        return next(iter(arch.values()), '')
    return arch or ''


def _category_shop_url(env, category):
    slug = env['ir.http'].sudo()._slug(category)
    return f'/shop/category/{slug}'


def _footer_boutique_items(env):
    """Liste ordonnée des <li> Boutique : lien global + racines exposables."""
    items = [(FOOTER_BOUTIQUE_ALL_LABEL, FOOTER_BOUTIQUE_ALL_URL)]
    Category = env['product.public.category'].sudo()
    root_categories = Category.search([('parent_id', '=', False)], order='sequence, name')
    for category in root_categories:
        if not category._is_ck_exposable():
            continue
        items.append((category.name, _category_shop_url(env, category)))
    return items


def _footer_boutique_li_html(env):
    lines = [
        f'<li class="mb-2"><a href="{escape(url)}">{escape(label)}</a></li>'
        for label, url in _footer_boutique_items(env)
    ]
    return '\n                                '.join(lines)


def bootstrap_footer_boutique_links(env):
    """Régénère la colonne Boutique du footer depuis les catégories exposables (idempotent)."""
    website = env['website'].sudo().search([], limit=1)
    if not website:
        return False

    View = env['ir.ui.view'].sudo()
    footer = View.search([('key', '=', FOOTER_VIEW_KEY)], limit=1)
    if not footer:
        _logger.warning(
            'CK footer boutique : vue %s introuvable — colonne Boutique non synchronisée',
            FOOTER_VIEW_KEY,
        )
        return False

    arch = _arch_as_string(footer.arch_db or footer.arch)
    marker_idx = arch.find(FOOTER_BOUTIQUE_MARKER)
    if marker_idx < 0:
        _logger.warning(
            'CK footer boutique : marqueur "%s" introuvable — colonne Boutique non synchronisée',
            FOOTER_BOUTIQUE_MARKER,
        )
        return False

    ul_start = arch.find('<ul', marker_idx)
    ul_open_end = arch.find('>', ul_start) + 1 if ul_start >= 0 else -1
    ul_close = arch.find('</ul>', ul_open_end) if ul_open_end >= 0 else -1
    if ul_start < 0 or ul_open_end <= 0 or ul_close < 0:
        _logger.warning(
            'CK footer boutique : structure <ul> Boutique introuvable — colonne non synchronisée'
        )
        return False

    new_inner = '\n                                ' + _footer_boutique_li_html(env) + '\n                            '
    new_arch = arch[:ul_open_end] + new_inner + arch[ul_close:]
    if new_arch == arch:
        return True

    footer.write({'arch': new_arch})
    return True
