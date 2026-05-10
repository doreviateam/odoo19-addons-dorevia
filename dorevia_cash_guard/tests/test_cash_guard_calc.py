# -*- coding: utf-8 -*-

from datetime import date

from odoo import fields
from odoo.tests.common import TransactionCase
from unittest.mock import patch


class TestCashGuardCalc(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.bank_journal = cls.env["account.journal"].search([("type", "=", "bank")], limit=1)
        if not cls.bank_journal:
            raise AssertionError("Aucun journal bancaire disponible pour les tests.")
        cls.company = cls.bank_journal.company_id
        cls.cash_journal = cls.env["account.journal"].search(
            [("type", "=", "cash"), ("company_id", "=", cls.company.id)],
            limit=1,
        )
        cls.currency = cls.company.currency_id
        cls.account = (
            cls.bank_journal.default_account_id
            or cls.bank_journal.payment_debit_account_id
            or cls.bank_journal.payment_credit_account_id
        )
        if not cls.account:
            raise AssertionError("Aucun compte de liquidite disponible sur le journal bancaire.")

        cls.budget_post = cls.env["account.budget.post"].create(
            {
                "name": "CG Budget Post",
                "account_ids": [(6, 0, [cls.account.id])],
            }
        )

    def _create_guard(self, threshold=0.0):
        with patch.object(fields.Date, "context_today", return_value=date(2026, 5, 1)):
            return self.env["dorevia.cash.guard"].create(
                {
                    "date_from": "2026-05-01",
                    "date_to": "2026-05-31",
                    "bank_journal_id": self.bank_journal.id,
                    "company_id": self.company.id,
                    "alert_threshold": threshold,
                }
            )

    def _create_line(self, guard, date_, amount, direction, seq=10, line_type="planned"):
        return self.env["dorevia.cash.guard.line"].create(
            {
                "guard_id": guard.id,
                "projection_date": date_,
                "budget_post_id": self.budget_post.id,
                "direction": direction,
                "line_type": line_type,
                "label": f"Line {date_}-{seq}",
                "projected_amount": amount,
                "sequence": seq,
                "cash_state": "planned",
            }
        )

    def _recompute_with_zero_initial(self, guard):
        with patch.object(fields.Date, "context_today", return_value=date(2026, 5, 1)):
            with patch.object(type(guard), "_compute_bank_balance_at_date", return_value=0.0):
                with patch.object(
                    type(guard),
                    "_search_open_invoice_moves",
                    return_value=self.env["account.move"],
                ):
                    guard.action_recompute_projection()

    def test_new_guard_defaults_month_start_year_end_and_situation_today(self):
        """Sans dates explicites : début = 1er du mois courant, fin = 31/12, situation = jour."""
        with patch.object(fields.Date, "context_today", return_value=date(2026, 5, 10)):
            guard = self.env["dorevia.cash.guard"].create(
                {
                    "bank_journal_id": self.bank_journal.id,
                    "company_id": self.company.id,
                    "alert_threshold": 0.0,
                }
            )
        self.assertEqual(guard.date_from, date(2026, 5, 1))
        self.assertEqual(guard.date_to, date(2026, 12, 31))
        self.assertEqual(guard.situation_date, date(2026, 5, 10))

    def test_initial_balance_only(self):
        guard = self._create_guard(threshold=100.0)
        self._recompute_with_zero_initial(guard)
        self.assertEqual(guard.initial_balance, 0.0)
        self.assertEqual(guard.forecast_final_balance, 0.0)
        self.assertEqual(guard.forecast_min_balance, 0.0)
        self.assertEqual(guard.risk_status, "warning")

    def test_projection_simple_inflow_outflow(self):
        guard = self._create_guard(threshold=800.0)
        self._create_line(guard, "2026-05-02", 1000.0, "inflow", seq=10)
        self._create_line(guard, "2026-05-03", 300.0, "outflow", seq=10)
        self._recompute_with_zero_initial(guard)
        self.assertEqual(guard.forecast_final_balance, 700.0)
        self.assertEqual(guard.forecast_min_balance, 0.0)
        self.assertEqual(guard.risk_status, "warning")

    def test_deterministic_sort_projection_date_sequence_id(self):
        guard = self._create_guard(threshold=0.0)
        line_a = self._create_line(guard, "2026-05-10", 200.0, "outflow", seq=20)
        line_b = self._create_line(guard, "2026-05-10", 100.0, "inflow", seq=10)
        line_c = self._create_line(guard, "2026-05-10", 50.0, "outflow", seq=20)
        self._recompute_with_zero_initial(guard)

        ordered = guard.line_ids.sorted(
            key=lambda l: (l.projection_date, l.sequence, l.id)
        )
        self.assertEqual(ordered.ids, [line_b.id, line_a.id, line_c.id])
        self.assertEqual(ordered[0].balance_after_line, 100.0)
        self.assertEqual(ordered[1].balance_after_line, -100.0)
        self.assertEqual(ordered[2].balance_after_line, -150.0)

    def test_risk_statuses_safe_warning_risk(self):
        guard_safe = self._create_guard(threshold=0.0)
        self._create_line(guard_safe, "2026-05-02", 200.0, "inflow")
        self._recompute_with_zero_initial(guard_safe)
        self.assertEqual(guard_safe.risk_status, "safe")

        guard_warning = self._create_guard(threshold=150.0)
        self._create_line(guard_warning, "2026-05-02", 100.0, "inflow")
        self._recompute_with_zero_initial(guard_warning)
        self.assertEqual(guard_warning.risk_status, "warning")

        guard_risk = self._create_guard(threshold=10.0)
        self._create_line(guard_risk, "2026-05-02", 50.0, "outflow")
        self._recompute_with_zero_initial(guard_risk)
        self.assertEqual(guard_risk.risk_status, "risk")

    def test_risk_when_final_positive_but_min_negative(self):
        guard = self._create_guard(threshold=0.0)
        self._create_line(guard, "2026-05-08", 150.0, "outflow")
        self._create_line(guard, "2026-05-15", 200.0, "inflow")
        self._recompute_with_zero_initial(guard)
        self.assertEqual(guard.forecast_final_balance, 50.0)
        self.assertEqual(guard.forecast_min_balance, -150.0)
        self.assertEqual(guard.risk_status, "risk")

    def test_simulated_line_included_in_projection(self):
        guard = self._create_guard(threshold=0.0)
        self._create_line(guard, "2026-05-02", 100.0, "outflow", line_type="simulated")
        self._recompute_with_zero_initial(guard)
        self.assertEqual(guard.forecast_final_balance, -100.0)
        # En V1, il n'y a pas encore d'option d'exclusion des simulations.
        self.assertEqual(guard.risk_status, "risk")

    def test_simple_variance(self):
        guard = self._create_guard(threshold=0.0)
        line = self._create_line(guard, "2026-05-02", 120.0, "outflow")
        line.realized_amount = 100.0
        line._compute_signed_amounts()
        line._compute_variance_amount()
        self.assertEqual(line.signed_projected_amount, -120.0)
        self.assertEqual(line.signed_realized_amount, -100.0)
        self.assertEqual(line.variance_amount, 20.0)

    def test_alert_threshold_write_updates_risk_status(self):
        guard = self._create_guard(threshold=250.0)
        self._create_line(guard, "2026-05-02", 200.0, "inflow")
        self._recompute_with_zero_initial(guard)
        self.assertEqual(guard.forecast_final_balance, 200.0)
        self.assertEqual(guard.risk_status, "warning")
        with patch.object(fields.Date, "context_today", return_value=date(2026, 5, 1)):
            with patch.object(type(guard), "_compute_bank_balance_at_date", return_value=0.0):
                with patch.object(
                    type(guard),
                    "_search_open_invoice_moves",
                    return_value=self.env["account.move"],
                ):
                    guard.write({"alert_threshold": 0.0})
        self.assertEqual(guard.risk_status, "safe")
        with patch.object(fields.Date, "context_today", return_value=date(2026, 5, 1)):
            with patch.object(type(guard), "_compute_bank_balance_at_date", return_value=0.0):
                with patch.object(
                    type(guard),
                    "_search_open_invoice_moves",
                    return_value=self.env["account.move"],
                ):
                    guard.write({"alert_threshold": 250.0})
        self.assertEqual(guard.risk_status, "warning")

    def test_liquidity_journal_write_recomputes_observed_balance(self):
        if not self.cash_journal:
            self.skipTest("Aucun journal de caisse disponible pour les tests.")
        guard = self._create_guard(threshold=0.0)

        def balance_from_journal_count(record, target_date):
            return 100.0 * len(record._liquidity_journals())

        with patch.object(fields.Date, "context_today", return_value=date(2026, 5, 1)):
            with patch.object(
                type(guard),
                "_compute_bank_balance_at_date",
                autospec=True,
                side_effect=balance_from_journal_count,
            ):
                with patch.object(
                    type(guard),
                    "_search_open_invoice_moves",
                    return_value=self.env["account.move"],
                ):
                    guard.write(
                        {
                            "liquidity_journal_ids": [
                                (6, 0, [self.bank_journal.id, self.cash_journal.id])
                            ]
                        }
                    )

        self.assertEqual(guard.observed_balance, 200.0)
        self.assertEqual(guard.forecast_final_balance, 200.0)

    def test_liquidity_journal_onchange_previews_observed_balance(self):
        if not self.cash_journal:
            self.skipTest("Aucun journal de caisse disponible pour les tests.")
        guard = self.env["dorevia.cash.guard"].new(
            {
                "date_from": "2026-05-01",
                "date_to": "2026-05-31",
                "company_id": self.company.id,
                "alert_threshold": 0.0,
                "liquidity_journal_ids": [(6, 0, [self.bank_journal.id])],
            }
        )

        def balance_from_journal_count(record, target_date):
            return 100.0 * len(record._liquidity_journals())

        with patch.object(fields.Date, "context_today", return_value=date(2026, 5, 1)):
            with patch.object(
                type(guard),
                "_compute_bank_balance_at_date",
                autospec=True,
                side_effect=balance_from_journal_count,
            ):
                with patch.object(
                    type(guard),
                    "_search_open_invoice_moves",
                    return_value=self.env["account.move"],
                ):
                    guard._onchange_projection_inputs()
                    self.assertEqual(guard.observed_balance, 100.0)

                    guard.liquidity_journal_ids = self.bank_journal | self.cash_journal
                    guard._onchange_projection_inputs()

        self.assertEqual(guard.observed_balance, 200.0)
        self.assertEqual(guard.forecast_final_balance, 200.0)
