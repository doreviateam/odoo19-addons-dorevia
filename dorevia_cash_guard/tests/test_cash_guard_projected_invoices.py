# -*- coding: utf-8 -*-

"""Tests V1.2 — solde projeté depuis factures ouvertes (account.move)."""

from datetime import date
from unittest.mock import patch

from odoo import fields
from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.fields import Command
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestCashGuardProjectedInvoices(AccountTestInvoicingCommon):
    """Recourt au plan comptable standard (AccountTestInvoicingCommon)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.bank_journal = cls.env["account.journal"].search(
            [("type", "=", "bank"), ("company_id", "=", cls.env.company.id)],
            limit=1,
        )
        if not cls.bank_journal:
            raise AssertionError("Journal banque requis pour Cash Guard.")

    def _create_guard(self, alert_threshold=3000.0):
        with patch.object(fields.Date, "context_today", return_value=date(2026, 5, 9)):
            return self.env["dorevia.cash.guard"].sudo().create(
                {
                    "date_from": "2026-05-01",
                    "date_to": "2026-05-31",
                    "bank_journal_id": self.bank_journal.id,
                    "company_id": self.env.company.id,
                    "alert_threshold": alert_threshold,
                    "periodicity": "week",
                }
            )

    def _recompute(self, guard, bank_balance=2520.0, moves=None):
        moves = self.env["account.move"].browse([m.id for m in moves or []])
        with patch.object(fields.Date, "context_today", return_value=date(2026, 5, 9)):
            with patch.object(
                type(guard),
                "_compute_bank_balance_at_date",
                return_value=bank_balance,
            ):
                with patch.object(
                    type(guard),
                    "_search_open_invoice_moves",
                    return_value=moves,
                ):
                    guard.action_recompute_projection()

    def _force_due_date(self, move, due_date):
        move.write({"invoice_date_due": due_date})
        receivable_payable = move.line_ids.filtered(
            lambda line: line.account_id.account_type
            in ("asset_receivable", "liability_payable")
        )
        receivable_payable.write({"date_maturity": due_date})
        move.invalidate_recordset(["invoice_date_due"])

    def test_client_open_invoice_future_increases_projected(self):
        """Cas 1 — encaissement projeté sur la période d'échéance."""
        inv = self._create_invoice_one_line(
            price_unit=300.0,
            move_type="out_invoice",
            invoice_date="2026-05-09",
            invoice_date_due="2026-05-20",
            tax_ids=[Command.clear()],
            post=True,
        )
        self._force_due_date(inv, "2026-05-20")
        self.assertGreater(inv.amount_residual, 0.0)
        guard = self._create_guard()
        self._recompute(guard, bank_balance=2520.0, moves=[inv])
        week_due = guard.weekly_line_ids.filtered(
            lambda w: w.date_from <= date(2026, 5, 20) <= w.date_to
        )
        week_due.ensure_one()
        self.assertEqual(week_due.period_type, "forecast")
        self.assertEqual(week_due.projected_balance, 2820.0)
        sit_week = guard.weekly_line_ids.filtered(lambda w: w.period_type == "current")
        sit_week.ensure_one()
        self.assertEqual(sit_week.projected_balance, 2520.0)

    def test_vendor_open_invoice_future_decreases_projected(self):
        """Cas 2 — décaissement projeté."""
        inv = self._create_invoice_one_line(
            price_unit=500.0,
            move_type="in_invoice",
            invoice_date="2026-05-09",
            invoice_date_due="2026-05-18",
            tax_ids=[Command.clear()],
            post=True,
        )
        self._force_due_date(inv, "2026-05-18")
        self.assertGreater(inv.amount_residual, 0.0)
        guard = self._create_guard()
        self._recompute(guard, bank_balance=2520.0, moves=[inv])
        week_due = guard.weekly_line_ids.filtered(
            lambda w: w.date_from <= date(2026, 5, 18) <= w.date_to
        )
        week_due.ensure_one()
        self.assertEqual(week_due.projected_balance, 2020.0)

    def test_partial_payment_uses_residual_only(self):
        """Cas 3 — seul le résidu alimente le projeté."""
        inv = self._create_invoice_one_line(
            price_unit=1000.0,
            move_type="out_invoice",
            invoice_date="2026-05-09",
            invoice_date_due="2026-05-25",
            tax_ids=[Command.clear()],
            post=True,
        )
        self._force_due_date(inv, "2026-05-25")
        self._register_payment(inv, amount=600.0)
        inv.invalidate_recordset()
        self.assertAlmostEqual(inv.amount_residual, 400.0, places=2)
        guard = self._create_guard()
        self._recompute(guard, bank_balance=2520.0, moves=[inv])
        week_due = guard.weekly_line_ids.filtered(
            lambda w: w.date_from <= date(2026, 5, 25) <= w.date_to
        )
        week_due.ensure_one()
        self.assertEqual(week_due.projected_balance, 2920.0)

    def test_overdue_open_invoice_at_situation_date(self):
        """Cas 4 — échéance avant situation : ancrage sur situation_date."""
        inv = self._create_invoice_one_line(
            price_unit=150.0,
            move_type="out_invoice",
            invoice_date="2026-05-01",
            invoice_date_due="2026-05-05",
            tax_ids=[Command.clear()],
            post=True,
        )
        self._force_due_date(inv, "2026-05-05")
        self.assertGreater(inv.amount_residual, 0.0)
        guard = self._create_guard()
        self._recompute(guard, bank_balance=2520.0, moves=[inv])
        sit_week = guard.weekly_line_ids.filtered(lambda w: w.period_type == "current")
        sit_week.ensure_one()
        self.assertEqual(sit_week.projected_balance, 2670.0)

    def test_paid_invoice_excluded(self):
        """Cas 5 — résiduel nul : pas d'impact."""
        inv = self._create_invoice_one_line(
            price_unit=100.0,
            move_type="out_invoice",
            invoice_date="2026-05-09",
            invoice_date_due="2026-05-15",
            tax_ids=[Command.clear()],
            post=True,
        )
        self._force_due_date(inv, "2026-05-15")
        self._register_payment(inv, amount=inv.amount_residual)
        inv.invalidate_recordset()
        self.assertEqual(inv.amount_residual, 0.0)
        guard = self._create_guard()
        self.assertNotIn(inv, guard._search_open_invoice_moves())
        self._recompute(guard, bank_balance=2520.0)
        self.assertTrue(
            all(w.projected_balance == 2520.0 for w in guard.weekly_line_ids)
        )

    def test_draft_invoice_excluded(self):
        """Cas 6 — brouillon ignoré."""
        inv = self._create_invoice_one_line(
            price_unit=9000.0,
            move_type="out_invoice",
            invoice_date="2026-05-09",
            invoice_date_due="2026-05-12",
            tax_ids=[Command.clear()],
            post=False,
        )
        self._force_due_date(inv, "2026-05-12")
        guard = self._create_guard()
        self.assertNotIn(inv, guard._search_open_invoice_moves())
        self._recompute(guard, bank_balance=2520.0)
        self.assertTrue(
            all(w.projected_balance == 2520.0 for w in guard.weekly_line_ids)
        )

    def test_out_refund_negative_impact(self):
        """Cas 7 — avoir client : impact négatif."""
        inv = self._create_invoice_one_line(
            price_unit=200.0,
            move_type="out_refund",
            invoice_date="2026-05-09",
            invoice_date_due="2026-05-21",
            tax_ids=[Command.clear()],
            post=True,
        )
        self._force_due_date(inv, "2026-05-21")
        self.assertGreater(inv.amount_residual, 0.0)
        guard = self._create_guard()
        self._recompute(guard, bank_balance=2520.0, moves=[inv])
        week_due = guard.weekly_line_ids.filtered(
            lambda w: w.date_from <= date(2026, 5, 21) <= w.date_to
        )
        week_due.ensure_one()
        self.assertEqual(week_due.projected_balance, 2320.0)

    def test_in_refund_positive_impact(self):
        """Cas 8 — avoir fournisseur : impact positif."""
        inv = self._create_invoice_one_line(
            price_unit=200.0,
            move_type="in_refund",
            invoice_date="2026-05-09",
            invoice_date_due="2026-05-21",
            tax_ids=[Command.clear()],
            post=True,
        )
        self._force_due_date(inv, "2026-05-21")
        self.assertGreater(inv.amount_residual, 0.0)
        guard = self._create_guard()
        self._recompute(guard, bank_balance=2520.0, moves=[inv])
        week_due = guard.weekly_line_ids.filtered(
            lambda w: w.date_from <= date(2026, 5, 21) <= w.date_to
        )
        week_due.ensure_one()
        self.assertEqual(week_due.projected_balance, 2720.0)

    def test_global_risk_follows_projected_min_not_only_observed(self):
        """Cas 9 — solde constaté confortable mais projeté sous seuil."""
        inv = self._create_invoice_one_line(
            price_unit=8000.0,
            move_type="in_invoice",
            invoice_date="2026-05-09",
            invoice_date_due="2026-05-22",
            tax_ids=[Command.clear()],
            post=True,
        )
        self._force_due_date(inv, "2026-05-22")
        guard = self._create_guard(alert_threshold=100.0)
        self._recompute(guard, bank_balance=5000.0, moves=[inv])
        week_due = guard.weekly_line_ids.filtered(
            lambda w: w.date_from <= date(2026, 5, 22) <= w.date_to
        )
        week_due.ensure_one()
        self.assertEqual(guard.risk_status, "risk")
        self.assertEqual(week_due.risk_status, "risk")
