# -*- coding: utf-8 -*-

from datetime import date
from unittest.mock import patch

from odoo import fields
from odoo.addons.dorevia_cash_guard.models import cash_guard as cash_guard_module
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestCashGuardSystemReferenceCron(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.bank_journal = cls.env["account.journal"].search([("type", "=", "bank")], limit=1)
        if not cls.bank_journal:
            raise AssertionError("Aucun journal bancaire pour les tests Cash Guard.")
        cls.company = cls.bank_journal.company_id

    def _create_week_guard(self, date_today, date_from, date_to, **extra):
        with patch.object(fields.Date, "context_today", return_value=date_today):
            vals = {
                "date_from": date_from,
                "date_to": date_to,
                "bank_journal_id": self.bank_journal.id,
                "company_id": self.company.id,
                "alert_threshold": 50.0,
                "periodicity": "week",
            }
            vals.update(extra)
            guard = self.env["dorevia.cash.guard"].create(vals)
        with patch.object(type(guard), "_compute_bank_balance_at_date", return_value=1.0):
            guard.action_recompute_projection()
        return guard

    def test_cron_targets_only_system_reference(self):
        """Le cron quotidien ne recalcule que les projections taguées référence système."""
        g_work = self._create_week_guard(
            date(2026, 6, 1), "2026-06-01", "2026-08-31"
        )
        g_sys = self._create_week_guard(
            date(2026, 1, 5), "2026-01-01", "2026-01-31", is_system_reference=True
        )
        calls = []

        def track_recompute(self):
            for r in self:
                calls.append(r.id)
            return True

        with patch.object(
            cash_guard_module.DoreviaCashGuard,
            "action_recompute_projection",
            track_recompute,
        ):
            self.env["dorevia.cash.guard"]._cron_recompute_system_reference_projections()
        self.assertEqual(calls, [g_sys.id])
        self.assertNotIn(g_work.id, calls)

    def test_second_system_reference_demotes_first(self):
        """Une seule référence active par société : la dernière promue retire le drapeau des autres."""
        g1 = self._create_week_guard(date(2026, 2, 1), "2026-02-01", "2026-02-28")
        g1.write({"is_system_reference": True})
        self.assertTrue(g1.is_system_reference)
        g2 = self._create_week_guard(
            date(2026, 3, 1), "2026-03-01", "2026-03-31", is_system_reference=True
        )
        self.assertTrue(g2.is_system_reference)
        self.assertFalse(g1.is_system_reference)

    def test_system_reference_must_be_weekly(self):
        """La référence système active impose la périodicité hebdomadaire."""
        g = self._create_week_guard(date(2026, 4, 1), "2026-04-01", "2026-04-30")
        g.write({"is_system_reference": True})
        with self.assertRaises(ValidationError):
            g.write({"periodicity": "month"})
