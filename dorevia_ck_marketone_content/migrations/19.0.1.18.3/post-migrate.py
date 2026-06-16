# -*- coding: utf-8 -*-
"""Section 3 — rubans produit sur cartes vedettes + réinjection home."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID
    from odoo.addons.dorevia_ck_marketone_content.home_featured import (
        bootstrap_home_featured_products,
    )

    env = api.Environment(cr, SUPERUSER_ID, {})
    ribbon = env.ref(
        'dorevia_ck_marketone_content.ribbon_coups_de_coeur',
        raise_if_not_found=False,
    )
    nouveau = env['product.ribbon'].sudo().search([('name', 'ilike', 'nouveau')], limit=1)
    Template = env['product.template'].sudo()

    confiture = Template.search([('name', '=', 'Confiture de goyave')], limit=1)
    if confiture and ribbon and not confiture.website_ribbon_id:
        confiture.website_ribbon_id = ribbon

    manio = Template.search([('name', '=', 'Manio Crackers')], limit=1)
    if manio and nouveau and not manio.website_ribbon_id:
        manio.website_ribbon_id = nouveau

    bootstrap_home_featured_products(env)
