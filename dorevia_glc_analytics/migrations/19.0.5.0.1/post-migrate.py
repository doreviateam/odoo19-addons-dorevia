# -*- coding: utf-8 -*-


def migrate(cr, version):
    from odoo.addons.dorevia_glc_analytics.hooks import _normalize_glc_activity_accounts

    _normalize_glc_activity_accounts(cr)
