# -*- coding: utf-8 -*-
"""Branding CK — footer reproductible sur install existante.

La vue CK Footer (website.footer_custom + copyright) est rechargée par les
données du module lors de l'update. Ce post-migrate seede le branding société
(nom/site/email, gardé et idempotent) et ré-enrichit dynamiquement le footer
(colonne Boutique, liens légaux, copyright legacy).
"""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    from odoo.addons.dorevia_ck_marketone_content.hooks import (
        bootstrap_brand_name,
        bootstrap_footer_copyright_brand,
        bootstrap_footer_legal_links,
    )
    from odoo.addons.dorevia_ck_marketone_content.footer_boutique import (
        bootstrap_footer_boutique_links,
    )

    bootstrap_brand_name(env)
    bootstrap_footer_copyright_brand(env)
    bootstrap_footer_legal_links(env)
    bootstrap_footer_boutique_links(env)
