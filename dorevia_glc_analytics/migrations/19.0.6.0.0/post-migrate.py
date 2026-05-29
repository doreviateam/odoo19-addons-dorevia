# -*- coding: utf-8 -*-


def migrate(cr, version):
    from odoo.addons.dorevia_glc_analytics.hooks import (
        _migrate_glc_activity_type_legacy_values,
        _migrate_glc_analytic_codes,
        _migrate_to_single_glc_plan,
        _normalize_glc_analytic_accounts,
    )

    _migrate_glc_activity_type_legacy_values(cr)
    _migrate_glc_analytic_codes(cr)
    _migrate_to_single_glc_plan(cr)
    _normalize_glc_analytic_accounts(cr)
