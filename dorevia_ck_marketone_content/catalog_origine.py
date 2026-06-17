# -*- coding: utf-8 -*-
"""Catalogue CK — attribut « Origine » (no_variant) pour le chip « pays » des vedettes.

Attribut d'information : il ne génère PAS de variantes (create_variant='no_variant'),
donc il n'interfère pas avec les variantes commerciales (ex. Manio Crackers / Format).
Le chip origine de la home lit cet attribut en priorité (cf. home_featured._get_featured_origin_label).
"""

ORIGIN_ATTRIBUTE_NAME = 'Origine'
ORIGIN_VALUES = ('Réunion', 'Guadeloupe', 'Martinique', 'Guyane', 'Mayotte')

# Affectation initiale du set vedettes (ajustable ensuite librement en BO).
ORIGIN_SEED_BY_TEMPLATE_NAME = {
    'Confiture de goyave': 'Réunion',
    'Manio Crackers': 'Guadeloupe',
    'Galettes de manioc': 'Martinique',
    'Savon vétiver': 'Martinique',
}


def _ensure_origin_attribute(env):
    """Crée l'attribut « Origine » (no_variant) + ses valeurs si absents."""
    Attribute = env['product.attribute'].sudo()
    attribute = Attribute.search([('name', '=', ORIGIN_ATTRIBUTE_NAME)], limit=1)
    if not attribute:
        attribute = Attribute.create({
            'name': ORIGIN_ATTRIBUTE_NAME,
            'create_variant': 'no_variant',
            'display_type': 'radio',
        })
    Value = env['product.attribute.value'].sudo()
    existing = set(attribute.value_ids.mapped('name'))
    for name in ORIGIN_VALUES:
        if name not in existing:
            Value.create({'name': name, 'attribute_id': attribute.id})
    return attribute


def _assign_origin(env, template, value_name):
    """Pose (idempotent) la ligne d'attribut « Origine » = value_name sur le template."""
    attribute = _ensure_origin_attribute(env)
    value = attribute.value_ids.filtered(lambda v: v.name == value_name)[:1]
    if not value:
        return False
    line = template.attribute_line_ids.filtered(
        lambda l: l.attribute_id == attribute
    )[:1]
    if line:
        if value not in line.value_ids:
            line.write({'value_ids': [(4, value.id)]})
    else:
        env['product.template.attribute.line'].sudo().create({
            'product_tmpl_id': template.id,
            'attribute_id': attribute.id,
            'value_ids': [(6, 0, value.ids)],
        })
    return True


def bootstrap_origine_attribute(env):
    """Crée l'attribut « Origine » et amorce les origines du set vedettes MOA."""
    _ensure_origin_attribute(env)
    Template = env['product.template'].sudo()
    seeded = False
    for tmpl_name, origin in ORIGIN_SEED_BY_TEMPLATE_NAME.items():
        tmpl = Template.search([('name', '=', tmpl_name)], limit=1)
        if tmpl:
            _assign_origin(env, tmpl, origin)
            seeded = True
    return seeded
