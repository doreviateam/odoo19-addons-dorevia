# -*- coding: utf-8 -*-
"""Header CK V2.2 — construction HTML mega-menus produit (grammaire 4 colonnes)."""
import logging
from urllib.parse import quote
from xml.sax.saxutils import escape

from .nav_v22_config import (
    ARTISANAT_FAMILIES,
    ARTISANAT_SELECTIONS,
    BOISSONS_FAMILIES,
    BOISSONS_SELECTIONS,
    EPICERIE_FAMILIES,
    EPICERIE_SELECTIONS,
    MAISON_FAMILIES,
    MAISON_SELECTIONS,
    MEGA_MENU_ARTISANAT,
    MEGA_MENU_BOISSONS,
    MEGA_MENU_EPICERIE,
    MEGA_MENU_MAISON,
    NAV_MAISON_LABEL,
    NAV_PRODUCTEURS_URL,
    ORIGINS_EPICERIE,
    PARAM_BOISSONS_FRAICHES,
)

_logger = logging.getLogger(__name__)


def _normalize_token(value):
    text = (value or '').strip().lower().replace('œ', 'oe')
    for src, dst in (
        ('é', 'e'), ('è', 'e'), ('ê', 'e'), ('ë', 'e'),
        ('î', 'i'), ('ï', 'i'), ('ô', 'o'), ('ù', 'u'),
        ('û', 'u'), ('ç', 'c'), ('à', 'a'), ('&', ''),
    ):
        text = text.replace(src, dst)
    return ' '.join(text.split())


def _category_shop_url(env, category):
    if not category:
        return None
    slug = env['ir.http'].sudo()._slug(category)
    return f'/shop/category/{slug}'


def _category_has_published_products(env, category):
    if not category:
        return False
    return bool(env['product.template'].sudo().search([
        ('sale_ok', '=', True),
        ('is_published', '=', True),
        ('website_published', '=', True),
        ('public_categ_ids', 'child_of', category.id),
    ], limit=1))


def _tag_has_published_products(env, tag):
    if not tag:
        return False
    return bool(env['product.template'].sudo().search([
        ('sale_ok', '=', True),
        ('is_published', '=', True),
        ('website_published', '=', True),
        '|',
        ('product_tag_ids', 'in', tag.ids),
        ('product_variant_ids.additional_product_tag_ids', 'in', tag.ids),
    ], limit=1))


def _resolve_tag(env, tag_name):
    Tag = env['product.tag'].sudo()
    tag = Tag.search([('name', '=ilike', tag_name.replace('_', ' '))], limit=1)
    if not tag:
        tag = Tag.search([('name', '=ilike', tag_name)], limit=1)
    return tag if tag and _tag_has_published_products(env, tag) else Tag.browse()


def _tag_shop_url(env, tag_name):
    tag = _resolve_tag(env, tag_name)
    if not tag:
        return None
    return f'/shop?tags={tag.id}'


def _supplier_shop_url(env, supplier_name):
    Partner = env['res.partner'].sudo()
    supplier = Partner.search([
        ('supplier_rank', '>', 0),
        ('name', 'ilike', supplier_name),
    ], limit=1)
    if not supplier:
        return None
    if not env['product.template'].sudo().search([
        ('sale_ok', '=', True),
        ('is_published', '=', True),
        ('website_published', '=', True),
        ('seller_ids.partner_id', '=', supplier.id),
    ], limit=1):
        return None
    return f'/shop?search={quote(supplier.name)}'


def _resolve_origin_attribute(env):
    return env['product.attribute'].sudo().search([
        '|', ('name', 'ilike', 'origine'), ('name', 'ilike', 'origin'),
    ], limit=1)


def _origin_shop_url(env, territory_slug):
    attr = _resolve_origin_attribute(env)
    if not attr:
        return None
    territory_name = territory_slug.replace('-', ' ').title()
    if territory_slug == 'guadeloupe':
        territory_name = 'Guadeloupe'
    elif territory_slug == 'martinique':
        territory_name = 'Martinique'
    elif territory_slug == 'dominique':
        territory_name = 'Dominique'
    elif territory_slug == 'guyane':
        territory_name = 'Guyane'
    value = env['product.attribute.value'].sudo().search([
        ('attribute_id', '=', attr.id),
        ('name', '=ilike', territory_name),
    ], limit=1)
    if not value:
        return None
    if not env['product.template'].sudo().search([
        ('sale_ok', '=', True),
        ('is_published', '=', True),
        ('website_published', '=', True),
        ('attribute_line_ids.value_ids', 'in', value.id),
    ], limit=1):
        return None
    return f'/shop?attrib={attr.id}-{value.id}'


def _find_root_category(env, root_label):
    from .nav_v22_config import RAYON_ROOT_ALIASES

    Category = env['product.public.category'].sudo()
    aliases = RAYON_ROOT_ALIASES.get(root_label, (root_label,))
    for alias in aliases:
        cat = Category.search([
            ('name', '=ilike', alias),
            ('parent_id', '=', False),
        ], limit=1)
        if cat:
            return cat
    return Category.browse()


def _match_family_category(env, root_category, aliases):
    if not root_category:
        return None
    normalized_aliases = {_normalize_token(a) for a in aliases}
    for child in root_category.child_id.sorted(key=lambda c: (c.sequence, c.name or '')):
        if _normalize_token(child.name) in normalized_aliases:
            if _category_has_published_products(env, child):
                return child
        for alias in aliases:
            if alias.lower() in (child.name or '').lower():
                if _category_has_published_products(env, child):
                    return child
    return None


def _resolve_families(env, root_label, family_specs, *, skip_conditional=False):
    root = _find_root_category(env, root_label)
    rows = []
    param = env['ir.config_parameter'].sudo()
    boissons_fraiches = param.get_param(PARAM_BOISSONS_FRAICHES, 'False') == 'True'
    for spec in family_specs:
        label = spec[0]
        aliases = spec[2] if len(spec) > 2 else (label,)
        conditional = len(spec) > 3 and spec[3]
        if conditional and not boissons_fraiches:
            continue
        category = _match_family_category(env, root, aliases)
        if not category:
            continue
        url = _category_shop_url(env, category)
        if url:
            rows.append({'label': label, 'url': url})
    return rows


def _resolve_selections(env, selection_specs):
    rows = []
    for label, kind, source in selection_specs:
        url = None
        if kind == 'tag':
            url = _tag_shop_url(env, source)
        elif kind == 'supplier':
            url = _supplier_shop_url(env, source)
        if url:
            rows.append({'label': label, 'url': url})
    return rows


def _resolve_origins(env, origin_specs):
    rows = []
    for label, slug in origin_specs:
        url = _origin_shop_url(env, slug)
        if url:
            rows.append({'label': label, 'url': url})
    return rows


def _get_visual_block(env, menu_key):
    Block = env['ck.mega.menu.visual.block'].sudo()
    today = fields_date_today(env)
    blocks = Block.search([
        ('menu_key', '=', menu_key),
        ('active', '=', True),
    ], order='sequence, id')
    for block in blocks:
        if block.date_start and block.date_start > today:
            continue
        if block.date_end and block.date_end < today:
            continue
        return block
    return Block.browse()


def fields_date_today(env):
    from odoo import fields
    return fields.Date.context_today(env['ck.mega.menu.visual.block'].sudo())


def _get_rayon_visual(env, menu_key):
    """P4 — visuel éditorial permanent du rayon (identité), curaté en BO.

    Distinct de _get_visual_block (campagne datée) : pas de date_start/
    date_end, pas de lien produit. Priorité 2 dans _visual_column — une
    campagne active reste prioritaire sur le visuel d'identité.
    """
    Visual = env['ck.mega.menu.rayon.visual'].sudo()
    return Visual.search([('menu_key', '=', menu_key), ('active', '=', True)], limit=1)


def _links_column(title, links):
    if not links:
        return ''
    items = ''.join(
        f'<li><a class="nav-link ck-mega-menu__link" href="{escape(row["url"])}">'
        f'{escape(row["label"])}</a></li>'
        for row in links
    )
    return (
        f'<div class="ck-mega-menu__col">'
        f'<h6 class="ck-mega-menu__title dropdown-header">{escape(title)}</h6>'
        f'<ul class="list-unstyled mb-0 ck-mega-menu__list">{items}</ul>'
        f'</div>'
    )


# P3 — fallback éditorial CK quand aucun bloc visuel BO n'est saisi. Évite
# qu'un rayon en seed pauvre (Épicerie : 1 seule colonne réelle) se réduise à
# un panneau de simples listes de liens sans présence de marque.
_FALLBACK_VISUAL_COPY = {
    'epicerie': ('Épicerie créole', 'Saveurs et producteurs sélectionnés dans les territoires créolophones.'),
    'boissons': ('Boissons créoles', 'Jus, sirops et boissons locales, origine identifiée.'),
    'maison_bien_etre': (NAV_MAISON_LABEL, 'Rituels, senteurs et soins inspirés des Caraïbes.'),
    'artisanat': ('Artisanat créole', 'Créations authentiques, faites main par nos artisans.'),
}


def _visual_column(block, rayon_visual=None, menu_key=None):
    if block:
        image_url = f'/web/image/ck.mega.menu.visual.block/{block.id}/image'
        subtitle = (
            f'<p class="ck-mega-menu__visual-subtitle small text-muted mb-2">'
            f'{escape(block.subtitle)}</p>'
            if block.subtitle else ''
        )
        return (
            f'<div class="ck-mega-menu__col ck-mega-menu__col--visual d-none d-lg-block">'
            f'<div class="ck-mega-menu__visual">'
            f'<img class="ck-mega-menu__visual-img img-fluid rounded" '
            f'src="{image_url}" alt="{escape(block.title)}" loading="lazy"/>'
            f'<h6 class="ck-mega-menu__visual-title mt-3 mb-1">{escape(block.title)}</h6>'
            f'{subtitle}'
            f'<a class="btn btn-sm btn-primary ck-mega-menu__visual-cta" '
            f'href="{escape(block.target_url)}">{escape(block.cta_label)}</a>'
            f'</div></div>'
        )

    # P4 — priorité 2 : visuel d'identité du rayon curaté en BO (pas de
    # campagne active). Photo de territoire/ambiance, jamais un produit
    # nommé comme tel — title/subtitle restent éditoriaux (rayon), pas
    # le nom du produit éventuellement utilisé comme image.
    if rayon_visual:
        image_url = f'/web/image/ck.mega.menu.rayon.visual/{rayon_visual.id}/image'
        subtitle = (
            f'<p class="ck-mega-menu__visual-subtitle small mb-0">'
            f'{escape(rayon_visual.subtitle)}</p>'
            if rayon_visual.subtitle else ''
        )
        return (
            '<div class="ck-mega-menu__col ck-mega-menu__col--visual '
            'ck-mega-menu__col--visual-fallback d-none d-lg-block">'
            '<div class="ck-mega-menu__visual ck-mega-menu__visual--fallback '
            f'ck-mega-menu__visual--photo" style="background-image:url(\'{image_url}\')">'
            '<p class="ck-mega-menu__visual-eyebrow mb-1">C-Kréyòl</p>'
            f'<h6 class="ck-mega-menu__visual-title mb-1">{escape(rayon_visual.title)}</h6>'
            f'{subtitle}'
            '</div></div>'
        )

    # Priorité 3 : carte de marque texte seul (rien saisi en BO).
    title, tagline = _FALLBACK_VISUAL_COPY.get(
        menu_key, ('C-Kréyòl', 'Épicerie créole, sélection et confiance.'),
    )
    return (
        '<div class="ck-mega-menu__col ck-mega-menu__col--visual '
        'ck-mega-menu__col--visual-fallback d-none d-lg-block">'
        '<div class="ck-mega-menu__visual ck-mega-menu__visual--fallback">'
        '<p class="ck-mega-menu__visual-eyebrow mb-1">C-Kréyòl</p>'
        f'<h6 class="ck-mega-menu__visual-title mb-1">{escape(title)}</h6>'
        f'<p class="ck-mega-menu__visual-subtitle small mb-0">{escape(tagline)}</p>'
        '</div></div>'
    )


def _mobile_accordion(sections):
    if not sections:
        return ''
    items = []
    for idx, (title, links) in enumerate(sections):
        if not links:
            continue
        collapse_id = f'ck-mega-acc-{idx}'
        link_rows = ''.join(
            f'<a class="nav-link ck-mega-menu__link" href="{escape(row["url"])}">'
            f'{escape(row["label"])}</a>'
            for row in links
        )
        items.append(
            f'<div class="accordion-item border-0">'
            f'<h2 class="accordion-header">'
            f'<button class="accordion-button collapsed" type="button" '
            f'data-bs-toggle="collapse" data-bs-target="#{collapse_id}" '
            f'aria-expanded="false">{escape(title)}</button>'
            f'</h2>'
            f'<div id="{collapse_id}" class="accordion-collapse collapse">'
            f'<div class="accordion-body py-2">{link_rows}</div>'
            f'</div></div>'
        )
    return (
        '<div class="accordion d-lg-none ck-mega-menu__accordion">'
        + ''.join(items)
        + '</div>'
    )


def build_product_mega_menu_html(env, *, menu_key, root_label, family_specs,
                                 selection_specs, origin_specs,
                                 origins_title='Origines & producteurs',
                                 origins_footer=None):
    """Construit le HTML mega-menu 4 colonnes (desktop) + accordéon (mobile)."""
    families = _resolve_families(env, root_label, family_specs)
    selections = _resolve_selections(env, selection_specs)
    origins = _resolve_origins(env, origin_specs)
    if origins_footer:
        origins = list(origins)
        origins.append({'label': origins_footer[0], 'url': origins_footer[1]})
    block = _get_visual_block(env, menu_key)
    rayon_visual = _get_rayon_visual(env, menu_key)

    desktop_cols = [
        _links_column('Acheter par famille', families),
        _links_column('Sélections CK', selections),
        _links_column(origins_title, origins),
        _visual_column(block, rayon_visual=rayon_visual, menu_key=menu_key),
    ]
    desktop = (
        '<div class="row g-4 d-none d-lg-flex ck-mega-menu__desktop">'
        + ''.join(desktop_cols)
        + '</div>'
    )
    mobile = _mobile_accordion([
        ('Acheter par famille', families),
        ('Sélections CK', selections),
        (origins_title, origins),
    ])
    if not families and not selections and not origins:
        return (
            '<div class="container py-3 ck-mega-menu">'
            '<p class="text-muted mb-0">Contenu à venir.</p></div>'
        )
    return (
        '<div class="container py-3 py-lg-4 ck-mega-menu">'
        f'{desktop}{mobile}{_trust_strip()}'
        '</div>'
    )


# P4 — bandeau de preuves CK en pied de mega-menu (desktop). Reprend des
# formulations déjà existantes au bandeau N1, aucune promesse nouvelle.
_TRUST_STRIP_ITEMS = ('Origines identifiées', 'Expédié depuis Nantes', 'Sélection créole')


def _trust_strip():
    items = ''.join(f'<span>{escape(t)}</span>' for t in _TRUST_STRIP_ITEMS)
    return f'<div class="ck-mega-menu__trust-strip d-none d-lg-flex">{items}</div>'


def build_epicerie_mega(env):
    return build_product_mega_menu_html(
        env,
        menu_key=MEGA_MENU_EPICERIE,
        root_label='Épicerie',
        family_specs=EPICERIE_FAMILIES,
        selection_specs=EPICERIE_SELECTIONS,
        origin_specs=ORIGINS_EPICERIE,
        origins_footer=('Voir les producteurs', NAV_PRODUCTEURS_URL),
    )


def build_boissons_mega(env):
    return build_product_mega_menu_html(
        env,
        menu_key=MEGA_MENU_BOISSONS,
        root_label='Boissons',
        family_specs=BOISSONS_FAMILIES,
        selection_specs=BOISSONS_SELECTIONS,
        origin_specs=ORIGINS_EPICERIE,
        origins_footer=('Voir les producteurs', NAV_PRODUCTEURS_URL),
    )


def build_maison_mega(env):
    return build_product_mega_menu_html(
        env,
        menu_key=MEGA_MENU_MAISON,
        root_label=NAV_MAISON_LABEL,
        family_specs=MAISON_FAMILIES,
        selection_specs=MAISON_SELECTIONS,
        origin_specs=ORIGINS_EPICERIE,
        origins_footer=('Voir les producteurs', NAV_PRODUCTEURS_URL),
    )


def build_artisanat_mega(env):
    return build_product_mega_menu_html(
        env,
        menu_key=MEGA_MENU_ARTISANAT,
        root_label='Artisanat',
        family_specs=ARTISANAT_FAMILIES,
        selection_specs=ARTISANAT_SELECTIONS,
        origin_specs=ORIGINS_EPICERIE,
        origins_title='Origines & artisans',
        origins_footer=('Voir les producteurs', NAV_PRODUCTEURS_URL),
    )


def count_artisanat_families(env):
    return len(_resolve_families(env, 'Artisanat', ARTISANAT_FAMILIES))


def build_espace_pro_dropdown_html():
    rows = ''.join(
        f'<a class="dropdown-item ck-nav-espace-pro__link" href="{escape(url)}">'
        f'{escape(label)}</a>'
        for label, url in __import__(
            'odoo.addons.dorevia_ck_marketone_content.nav_v22_config',
            fromlist=['ESPACE_PRO_LINKS'],
        ).ESPACE_PRO_LINKS
    )
    return f'<div class="py-2 ck-nav-espace-pro__menu">{rows}</div>'


def build_coffrets_mini_dropdown_html(env):
    from .nav_v22_config import COFFRETS_ANGLES

    rows = []
    for label, kind, source in COFFRETS_ANGLES:
        if kind != 'tag':
            continue
        url = _tag_shop_url(env, source)
        if url:
            rows.append({'label': label, 'url': url})
    if len(rows) < 3:
        return ''
    items = ''.join(
        f'<a class="dropdown-item" href="{escape(row["url"])}">{escape(row["label"])}</a>'
        for row in rows[:5]
    )
    return f'<div class="py-2 ck-nav-coffrets__menu">{items}</div>'
