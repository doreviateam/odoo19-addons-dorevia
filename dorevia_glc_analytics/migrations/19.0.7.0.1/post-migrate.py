# -*- coding: utf-8 -*-

def migrate(cr, version):
    from odoo.addons.dorevia_glc_analytics.hooks import migrate_glc_analytic_nomenclature

    migrate_glc_analytic_nomenclature(cr)
