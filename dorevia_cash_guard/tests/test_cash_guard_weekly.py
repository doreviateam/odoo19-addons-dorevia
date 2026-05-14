# -*- coding: utf-8 -*-

from datetime import date
from unittest.mock import patch

from odoo import fields
from odoo.tests.common import TransactionCase


class TestCashGuardWeekly(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.bank_journal = cls.env["account.journal"].search([("type", "=", "bank")], limit=1)
        if not cls.bank_journal:
            raise AssertionError("Aucun journal bancaire disponible pour les tests.")
        cls.company = cls.bank_journal.company_id
        cls.account = (
            cls.bank_journal.default_account_id
            or cls.bank_journal.payment_debit_account_id
            or cls.bank_journal.payment_credit_account_id
        )
        if not cls.account:
            raise AssertionError("Aucun compte de liquidite disponible sur le journal bancaire.")
        cls.budget_post = cls.env["account.budget.post"].create(
            {
                "name": "CG Weekly Budget Post",
                "account_ids": [(6, 0, [cls.account.id])],
            }
        )

    def _create_guard(self, periodicity="week"):
        with patch.object(fields.Date, "context_today", return_value=date(2026, 5, 15)):
            return self.env["dorevia.cash.guard"].create(
                {
                    "date_from": "2026-05-01",
                    "date_to": "2026-05-31",
                    "bank_journal_id": self.bank_journal.id,
                    "company_id": self.company.id,
                    "alert_threshold": 0.0,
                    "periodicity": periodicity,
                }
            )

    def test_weekly_lines_count_and_period_types_may_situation_mid_month(self):
        guard = self._create_guard()
        with patch.object(fields.Date, "context_today", return_value=date(2026, 5, 15)):
            with patch.object(type(guard), "_compute_bank_balance_at_date", return_value=0.0):
                guard.action_recompute_projection()
        weeks = guard.weekly_line_ids.sorted("week_index")
        self.assertEqual(len(weeks), 5)
        self.assertEqual(weeks[0].period_type, "historical")
        self.assertEqual(weeks[1].period_type, "historical")
        self.assertEqual(weeks[2].period_type, "current")
        self.assertEqual(weeks[3].period_type, "forecast")
        self.assertEqual(weeks[4].period_type, "forecast")
        self.assertEqual(
            [w.week_label for w in weeks],
            ["S18", "S19", "S20", "S21", "S22"],
        )

    def test_forecast_week_net_from_lines_after_situation(self):
        """Flux strictement après la date de situation : agrégés en mailles projection engagée."""
        guard = self._create_guard()
        self.env["dorevia.cash.guard.line"].create(
            {
                "guard_id": guard.id,
                "projection_date": "2026-05-22",
                "budget_post_id": self.budget_post.id,
                "direction": "inflow",
                "line_type": "planned",
                "label": "Weekly test inflow",
                "projected_amount": 500.0,
                "sequence": 10,
                "cash_state": "planned",
            }
        )
        with patch.object(fields.Date, "context_today", return_value=date(2026, 5, 15)):
            with patch.object(type(guard), "_compute_bank_balance_at_date", return_value=100.0):
                guard.action_recompute_projection()
        week_may22 = guard.weekly_line_ids.filtered(
            lambda w: w.date_from <= date(2026, 5, 22) <= w.date_to
        )
        week_may22.ensure_one()
        self.assertEqual(week_may22.period_type, "forecast")
        self.assertEqual(week_may22.inflow_amount, 500.0)
        self.assertEqual(week_may22.closing_balance, 600.0)

    def test_month_periodicity_single_segment_may(self):
        guard = self._create_guard(periodicity="month")
        with patch.object(fields.Date, "context_today", return_value=date(2026, 5, 15)):
            with patch.object(type(guard), "_compute_bank_balance_at_date", return_value=0.0):
                guard.action_recompute_projection()
        lines = guard.weekly_line_ids.sorted("week_index")
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines.week_label, "P0")
        self.assertEqual(lines.period_type, "current")

    def test_quarter_periodicity_may_segment_label(self):
        guard = self._create_guard(periodicity="quarter")
        with patch.object(fields.Date, "context_today", return_value=date(2026, 5, 15)):
            with patch.object(type(guard), "_compute_bank_balance_at_date", return_value=0.0):
                guard.action_recompute_projection()
        lines = guard.weekly_line_ids.sorted("week_index")
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines.week_label, "P0")
