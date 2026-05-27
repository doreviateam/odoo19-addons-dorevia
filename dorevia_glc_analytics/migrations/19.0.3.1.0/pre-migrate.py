# -*- coding: utf-8 -*-


def migrate(cr, version):
    from odoo.addons.dorevia_glc_analytics.hooks import _rename_module_records

    _rename_module_records(cr)
