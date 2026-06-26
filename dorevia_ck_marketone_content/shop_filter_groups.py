# -*- coding: utf-8 -*-
"""Drawer filtres boutique — regroupement métier des product.tag (Micro-lot 3B)."""

from odoo.addons.dorevia_ck_marketone_content.ck_product_origin import (
    ck_is_geographic_origin_name,
)

CK_SHOP_FILTER_GROUP_ORIGIN = 'origin'
CK_SHOP_FILTER_GROUP_PRODUCER = 'producer'
CK_SHOP_FILTER_GROUP_PREFERENCE = 'preference'

CK_SHOP_FILTER_GROUP_ORDER = (
    CK_SHOP_FILTER_GROUP_ORIGIN,
    CK_SHOP_FILTER_GROUP_PRODUCER,
    CK_SHOP_FILTER_GROUP_PREFERENCE,
)

CK_SHOP_FILTER_GROUP_LABELS = {
    CK_SHOP_FILTER_GROUP_ORIGIN: 'Origines',
    CK_SHOP_FILTER_GROUP_PRODUCER: 'Producteurs',
    CK_SHOP_FILTER_GROUP_PREFERENCE: 'Préférences',
}

# Tags producteur connus (complément à la détection géographique).
_CK_PRODUCER_TAG_NAMES = frozenset({
    'komla',
    'la platine',
    'rwan ltd',
})

# Tags exclus du drawer public (confusion navigation / non filtrables MOA).
_CK_EXCLUDED_DRAWER_TAG_NAMES = frozenset({
    'bien-être',
    'bien-etre',
    'épicerie',
    'epicerie',
    'artisanat',
    'boissons',
    'coups de cœur',
    'coups de coeur',
})

AGRICULTURE_BIO_TAG_NAME = 'Agriculture Bio'
AGRICULTURE_BIO_RIBBON_NAME = 'Agriculture Bio'
BIEN_ETRE_TAG_NAME = 'Bien-être'
GUADELOUPE_TAG_NAME = 'Guadeloupe'


def _normalize_tag_name(name):
    return (name or '').strip().lower().replace('œ', 'oe')


def ck_infer_shop_filter_group(tag_name):
    """Infère le groupe métier d'une étiquette (migration / ops)."""
    normalized = _normalize_tag_name(tag_name)
    if not normalized or normalized in _CK_EXCLUDED_DRAWER_TAG_NAMES:
        return False
    if ck_is_geographic_origin_name(name=tag_name):
        return CK_SHOP_FILTER_GROUP_ORIGIN
    if normalized in _CK_PRODUCER_TAG_NAMES:
        return CK_SHOP_FILTER_GROUP_PRODUCER
    if normalized in ('sans gluten', 'agriculture bio'):
        return CK_SHOP_FILTER_GROUP_PREFERENCE
    return False


def ck_shop_filter_active_tag_ids(values, kwargs):
    """Identifiants de tags actifs dans le contexte shop courant."""
    tags_val = values.get('tags') if values else None
    if tags_val is None:
        tags_val = kwargs.get('tags')
    if not tags_val:
        return set()
    if hasattr(tags_val, 'ids'):
        return set(tags_val.ids)
    if isinstance(tags_val, (list, tuple, set)):
        return {int(tag_id) for tag_id in tags_val if tag_id}
    return {
        int(part)
        for part in str(tags_val).split(',')
        if part.strip().isdigit()
    }


def partition_ck_shop_filter_tags(tags, active_tag_ids=None):
    """Partitionne un recordset product.tag selon ck_shop_filter_group."""
    active_tag_ids = active_tag_ids or set()
    grouped = {key: tags.browse() for key in CK_SHOP_FILTER_GROUP_ORDER}
    for tag in tags:
        group = tag.ck_shop_filter_group
        if group in grouped:
            grouped[group] |= tag
    return grouped


def build_ck_shop_filter_tag_groups(tags, active_tag_ids=None):
    """Construit la structure QWeb : sections ordonnées avec état actif."""
    active_tag_ids = active_tag_ids or set()
    grouped = partition_ck_shop_filter_tags(tags, active_tag_ids)
    sections = []
    for key in CK_SHOP_FILTER_GROUP_ORDER:
        section_tags = grouped[key].sorted(key=lambda tag: (tag.sequence, tag.id))
        if not section_tags:
            continue
        sections.append({
            'key': key,
            'label': CK_SHOP_FILTER_GROUP_LABELS[key],
            'tags': section_tags,
            'active': any(tag.id in active_tag_ids for tag in section_tags),
            'dom_id': f'o_wsale_offcanvas_ck_tags_{key}',
        })
    return sections


def bootstrap_ck_shop_filter_tags(env):
    """Migration / ops — classe les tags, corrige visibilité, sync Agriculture Bio."""
    Tag = env['product.tag'].sudo()
    Product = env['product.template'].sudo()
    Ribbon = env['product.ribbon'].sudo()

    for tag in Tag.search([]):
        updates = {}
        group = tag.ck_shop_filter_group or ck_infer_shop_filter_group(tag.name)
        if group:
            updates['ck_shop_filter_group'] = group
        normalized = _normalize_tag_name(tag.name)
        if normalized in _CK_EXCLUDED_DRAWER_TAG_NAMES:
            updates['visible_to_customers'] = False
        elif group == CK_SHOP_FILTER_GROUP_ORIGIN and normalized == _normalize_tag_name(GUADELOUPE_TAG_NAME):
            updates['visible_to_customers'] = True
        elif group and tag.visible_to_customers is False and normalized not in _CK_EXCLUDED_DRAWER_TAG_NAMES:
            updates['visible_to_customers'] = True
        if updates:
            tag.write(updates)

    bio_tag = Tag.search([('name', '=', AGRICULTURE_BIO_TAG_NAME)], limit=1)
    if not bio_tag:
        bio_tag = Tag.create({
            'name': AGRICULTURE_BIO_TAG_NAME,
            'visible_to_customers': True,
            'ck_shop_filter_group': CK_SHOP_FILTER_GROUP_PREFERENCE,
        })
    else:
        bio_tag.write({
            'visible_to_customers': True,
            'ck_shop_filter_group': CK_SHOP_FILTER_GROUP_PREFERENCE,
        })

    bio_ribbon = Ribbon.search([('name', '=', AGRICULTURE_BIO_RIBBON_NAME)], limit=1)
    if bio_ribbon:
        for product in Product.search([
            ('website_ribbon_id', '=', bio_ribbon.id),
            ('is_published', '=', True),
        ]):
            if bio_tag not in product.product_tag_ids:
                product.write({'product_tag_ids': [(4, bio_tag.id)]})

    bien_etre = Tag.search([('name', '=', BIEN_ETRE_TAG_NAME)], limit=1)
    if bien_etre:
        bien_etre.write({'visible_to_customers': False})

    return True
