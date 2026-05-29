# -*- coding: utf-8 -*-


def migrate(cr, version):
    from odoo.addons.dorevia_glc_analytics.hooks import (
        _migrate_glc_activity_type_legacy_values,
        _normalize_glc_activity_accounts,
        _normalize_glc_funding_accounts,
    )

    _migrate_glc_activity_type_legacy_values(cr)
    _normalize_glc_activity_accounts(cr)
    _normalize_glc_funding_accounts(cr)
