# -*- coding: utf-8 -*-

"""Remplit les journaux de liquidité à partir du journal bancaire historique (V1)."""

from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    Guard = env["dorevia.cash.guard"]
    guards = Guard.search([("bank_journal_id", "!=", False)])
    for guard in guards:
        if guard.liquidity_journal_ids:
            continue
        guard.with_context(skip_cash_guard_recompute=True).write(
            {"liquidity_journal_ids": [(6, 0, [guard.bank_journal_id.id])]}
        )
