# -*- coding: utf-8 -*-
"""CK-HOME-001C — hygiène visible home : marque C-Kréyòl, carte Boissons, newsletter FR."""
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})

    from odoo.addons.dorevia_ck_marketone_content.hooks import (
        bootstrap_brand_name,
        bootstrap_footer_copyright_brand,
        bootstrap_mentions_legales_page,
        bootstrap_privacy_page,
        bootstrap_terms_page,
    )
    from odoo.addons.dorevia_ck_marketone_content.home_editorial import (
        bootstrap_home_editorial,
    )
    from odoo.addons.dorevia_ck_marketone_content.home_univers import (
        bootstrap_home_univers,
    )
    from odoo.addons.dorevia_ck_marketone_content.home_dual_engage import (
        bootstrap_home_dual_engage,
    )

    bootstrap_brand_name(env)
    bootstrap_footer_copyright_brand(env)
    bootstrap_home_editorial(env)
    bootstrap_mentions_legales_page(env)
    bootstrap_privacy_page(env)
    bootstrap_terms_page(env)
    bootstrap_home_univers(env)
    bootstrap_home_dual_engage(env)
    cr.commit()

    _logger.info(
        'CK-HOME-001C : marque C-Kréyòl harmonisée, carte Boissons ajoutée, '
        'snapshot newsletter home régénéré (fr_FR).'
    )
