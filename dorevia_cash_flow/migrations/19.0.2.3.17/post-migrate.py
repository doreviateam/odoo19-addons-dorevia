# -*- coding: utf-8 -*-

"""Force les libellés menus/actions Cash Flow dans toutes les langues actives."""

from odoo import SUPERUSER_ID, api


LABELS = {
    "dorevia_cash_flow.menu_dorevia_cash_flow_guard_cockpit": "Cash Flow",
    "dorevia_cash_flow.action_dorevia_cash_flow_guard_cockpit": "Cash Flow",
}


def _write_label(record, label, languages):
    record.write({"name": label})
    for lang in languages:
        record.with_context(lang=lang.code).write({"name": label})


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    languages = env["res.lang"].search([("active", "=", True)])
    for xmlid, label in LABELS.items():
        record = env.ref(xmlid, raise_if_not_found=False)
        if record:
            _write_label(record, label, languages)
