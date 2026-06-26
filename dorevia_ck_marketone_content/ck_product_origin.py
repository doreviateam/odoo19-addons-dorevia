# -*- coding: utf-8 -*-
"""Origine géographique produit CK — attribut « Origines » (source de référence MOA)."""

# Territoires : ne doivent plus être portés par ``product_tag_ids`` (fallback temporaire Option A).
_CK_GEOGRAPHIC_ORIGIN_NAMES = frozenset({
    'guadeloupe',
    'martinique',
    'reunion',
    'guyane',
    'mayotte',
    'haiti',
    'sainte-lucie',
    'dominique',
    'saint-martin',
    'saint-barthelemy',
    'saint pierre et miquelon',
    'nouvelle-caledonie',
    'polynesie francaise',
})


def _normalize_origin_token(value):
    text = (value or '').strip().lower().replace('œ', 'oe')
    for src, dst in (
        ('é', 'e'), ('è', 'e'), ('ê', 'e'), ('ë', 'e'),
        ('î', 'i'), ('ï', 'i'), ('ô', 'o'), ('ù', 'u'),
        ('û', 'u'), ('ç', 'c'), ('à', 'a'),
    ):
        text = text.replace(src, dst)
    return text


def ck_is_geographic_origin_name(name):
    """True si le libellé correspond à une origine géographique CK (pas un tag transversal)."""
    normalized = _normalize_origin_token(name)
    if not normalized:
        return False
    if normalized in _CK_GEOGRAPHIC_ORIGIN_NAMES:
        return True
    if normalized.startswith('la ') and normalized[3:] in _CK_GEOGRAPHIC_ORIGIN_NAMES:
        return True
    # Variantes catalogue : « Dominique (Île) », « Dominique (Ile) », etc.
    base = normalized.split('(')[0].strip()
    if base in _CK_GEOGRAPHIC_ORIGIN_NAMES:
        return True
    if base.startswith('la ') and base[3:] in _CK_GEOGRAPHIC_ORIGIN_NAMES:
        return True
    return False


def ck_origin_from_attribute(product):
    """Lit l'origine depuis l'attribut produit dont le nom contient « origine »."""
    for line in product.attribute_line_ids:
        attr_name = (line.attribute_id.name or '').lower()
        if 'origine' in attr_name or 'origin' in attr_name:
            value = line.value_ids[:1]
            if value and (value.name or '').strip():
                return value.name.strip()
    return ''


def ck_card_origin_and_transversal_tags(tag_names, origin_from_attribute):
    """Sépare origine (attribut + fallback tags Option A) et étiquettes transversales.

    ``tag_names`` : libellés ordonnés (hors exclusions type « Coups de cœur »).
    """
    origin = (origin_from_attribute or '').strip()
    transversal = []

    if origin:
        origin_norm = _normalize_origin_token(origin)
        for name in tag_names:
            label = (name or '').strip()
            if not label:
                continue
            if _normalize_origin_token(label) == origin_norm:
                continue
            if ck_is_geographic_origin_name(label):
                continue
            transversal.append(label)
        return origin, transversal

    # Option A — fallback temporaire : première étiquette géographique = origine.
    for name in tag_names:
        label = (name or '').strip()
        if not label:
            continue
        if not origin and ck_is_geographic_origin_name(label):
            origin = label
            continue
        transversal.append(label)
    return origin, transversal
