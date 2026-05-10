# -*- coding: utf-8 -*-

"""Resynchronise le libellé du menu racine (traductions FR résiduelles)."""

from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    menu = env.ref(
        "dorevia_cash_guard.menu_dorevia_cash_guard_root", raise_if_not_found=False
    )
    if not menu:
        return
    label = "Prévision de trésorerie"
    menu.write({"name": label})
    for lang in env["res.lang"].search([("active", "=", True)]):
        if lang.code.startswith("fr"):
            menu.with_context(lang=lang.code).write({"name": label})
