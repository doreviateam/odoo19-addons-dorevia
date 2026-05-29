# -*- coding: utf-8 -*-


def migrate(cr, version):
    from odoo.addons.dorevia_glc_analytics.hooks import _normalize_glc_official_analytic_seed

    _normalize_glc_official_analytic_seed(cr)
