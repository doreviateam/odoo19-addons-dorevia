# -*- coding: utf-8 -*-

"""Force les libellés menus/actions Cash Guard dans toutes les langues actives."""

from odoo import SUPERUSER_ID, api


LABELS = {
    "dorevia_cash_guard.menu_dorevia_cash_guard_root": "Projection de trésorerie",
    "dorevia_cash_guard.menu_dorevia_cash_guard_points": "Cash Guards",
    "dorevia_cash_guard.action_dorevia_cash_guard": "Cash Guards",
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
