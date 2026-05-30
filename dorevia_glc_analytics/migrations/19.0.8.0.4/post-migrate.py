# -*- coding: utf-8 -*-

from odoo.addons.dorevia_glc_analytics.hooks import migrate_glc_analytic_nomenclature


def migrate(cr, version):
    migrate_glc_analytic_nomenclature(cr)
