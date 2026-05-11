# -*- coding: utf-8 -*-

"""Tests V1.3 — détail projection (factures ouvertes par période)."""

from datetime import date
from unittest.mock import patch

from odoo import fields
from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.fields import Command
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestCashGuardProjectionExplanation(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.bank_journal = cls.env["account.journal"].search(
            [("type", "=", "bank"), ("company_id", "=", cls.env.company.id)],
            limit=1,
        )
        if not cls.bank_journal:
            raise AssertionError("Journal banque requis pour Cash Guard.")

    def _create_guard(self):
        with patch.object(fields.Date, "context_today", return_value=date(2026, 5, 9)):
            return self.env["dorevia.cash.guard"].sudo().create(
                {
                    "date_from": "2026-05-01",
                    "date_to": "2026-05-31",
                    "bank_journal_id": self.bank_journal.id,
                    "company_id": self.env.company.id,
                    "alert_threshold": 3000.0,
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

    def test_detail_client_future_positive(self):
        inv = self._create_invoice_one_line(
            price_unit=300.0,
            move_type="out_invoice",
            invoice_date="2026-05-09",
            invoice_date_due="2026-05-20",
            tax_ids=[Command.clear()],
            post=True,
        )
        self._force_due_date(inv, "2026-05-20")
        guard = self._create_guard()
        self._recompute(guard, moves=[inv])
        week = guard.weekly_line_ids.filtered(
            lambda w: w.date_from <= date(2026, 5, 20) <= w.date_to
        )
        week.ensure_one()
        detail = guard.projection_period_move_ids.filtered(lambda d: d.move_id == inv)
        detail.ensure_one()
        self.assertEqual(detail.signed_amount, 300.0)
        self.assertEqual(detail.explanation_type, "inflow")
        self.assertFalse(detail.is_overdue)
        self.assertEqual(detail.days_overdue, 0)
        self.assertEqual(detail.days_overdue_label, "")
        self.assertEqual(week.invoice_net_amount, 300.0)
        self.assertEqual(week.invoice_move_count, 1)

    def test_detail_vendor_future_negative(self):
        inv = self._create_invoice_one_line(
            price_unit=500.0,
            move_type="in_invoice",
            invoice_date="2026-05-09",
            invoice_date_due="2026-05-18",
            tax_ids=[Command.clear()],
            post=True,
        )
        self._force_due_date(inv, "2026-05-18")
        guard = self._create_guard()
        self._recompute(guard, moves=[inv])
        detail = guard.projection_period_move_ids.filtered(lambda d: d.move_id == inv)
        detail.ensure_one()
        self.assertEqual(detail.signed_amount, -500.0)
        self.assertEqual(detail.explanation_type, "outflow")

    def test_detail_overdue_flag_and_situation_week(self):
        inv = self._create_invoice_one_line(
            price_unit=150.0,
            move_type="out_invoice",
            invoice_date="2026-05-01",
            invoice_date_due="2026-05-05",
            tax_ids=[Command.clear()],
            post=True,
        )
        self._force_due_date(inv, "2026-05-05")
        guard = self._create_guard()
        self._recompute(guard, moves=[inv])
        detail = guard.projection_period_move_ids.filtered(lambda d: d.move_id == inv)
        detail.ensure_one()
        self.assertEqual(detail.projected_date, date(2026, 5, 9))
        self.assertTrue(detail.is_overdue)
        self.assertEqual(detail.days_overdue, 4)
        self.assertEqual(detail.days_overdue_label, "4 j")
        sit = guard.weekly_line_ids.filtered(lambda w: w.period_type == "current")
        sit.ensure_one()
        self.assertEqual(detail.week_id, sit)

    def test_no_detail_for_paid_invoice(self):
        inv = self._create_invoice_one_line(
            price_unit=100.0,
            move_type="out_invoice",
            invoice_date="2026-05-09",
            invoice_date_due="2026-05-25",
            tax_ids=[Command.clear()],
            post=True,
        )
        self._force_due_date(inv, "2026-05-25")
        self._register_payment(inv, amount=100.0)
        guard = self._create_guard()
        with patch.object(fields.Date, "context_today", return_value=date(2026, 5, 9)):
            with patch.object(
                type(guard),
                "_compute_bank_balance_at_date",
                return_value=2520.0,
            ):
                guard.action_recompute_projection()
        self.assertFalse(guard.projection_period_move_ids)

    def test_aggregates_match_signed_lines_same_week(self):
        inv_a = self._create_invoice_one_line(
            price_unit=200.0,
            move_type="out_invoice",
            invoice_date="2026-05-09",
            invoice_date_due="2026-05-22",
            tax_ids=[Command.clear()],
            post=True,
        )
        self._force_due_date(inv_a, "2026-05-22")
        inv_b = self._create_invoice_one_line(
            price_unit=100.0,
            move_type="in_invoice",
            invoice_date="2026-05-09",
            invoice_date_due="2026-05-22",
            tax_ids=[Command.clear()],
            post=True,
        )
        self._force_due_date(inv_b, "2026-05-22")
        guard = self._create_guard()
        self._recompute(guard, moves=[inv_a, inv_b])
        week = guard.weekly_line_ids.filtered(
            lambda w: w.date_from <= date(2026, 5, 22) <= w.date_to
        )
        week.ensure_one()
        lines = week.projection_move_ids
        self.assertEqual(len(lines), 2)
        net = sum(lines.mapped("signed_amount"))
        self.assertEqual(week.invoice_net_amount, net)
        pos = sum(l.signed_amount for l in lines if l.signed_amount > 0)
        neg = sum(l.signed_amount for l in lines if l.signed_amount < 0)
        self.assertEqual(week.invoice_inflow_amount, pos)
        self.assertEqual(week.invoice_outflow_amount, -neg)

    def test_double_recompute_no_duplicate_moves(self):
        inv = self._create_invoice_one_line(
            price_unit=50.0,
            move_type="out_invoice",
            invoice_date="2026-05-09",
            invoice_date_due="2026-05-28",
            tax_ids=[Command.clear()],
            post=True,
        )
        self._force_due_date(inv, "2026-05-28")
        guard = self._create_guard()
        self._recompute(guard, moves=[inv])
        self._recompute(guard, moves=[inv])
        self.assertEqual(len(guard.projection_period_move_ids), 1)

    def test_complementary_line_not_in_period_detail(self):
        used = set()
        for p in self.env["account.budget.post"].search(
            [("company_id", "=", self.env.company.id), ("active", "=", True)]
        ):
            used.update(p.account_ids.ids)
        acc = self.env["account.account"].search(
            [
                ("company_ids", "in", self.env.company.ids),
                ("active", "=", True),
                ("id", "not in", list(used) if used else [0]),
            ],
            limit=1,
        )
        if not acc:
            self.skipTest("Aucun compte libre pour créer un poste budgétaire de test.")
        budget_post = self.env["account.budget.post"].create(
            {
                "name": "CG V13 flux complémentaire test",
                "company_id": self.env.company.id,
                "account_ids": [(6, 0, acc.ids)],
            }
        )
        inv = self._create_invoice_one_line(
            price_unit=100.0,
            move_type="out_invoice",
            invoice_date="2026-05-09",
            invoice_date_due="2026-05-22",
            tax_ids=[Command.clear()],
            post=True,
        )
        self._force_due_date(inv, "2026-05-22")
        guard = self._create_guard()
        self.env["dorevia.cash.guard.line"].sudo().create(
            {
                "guard_id": guard.id,
                "projection_date": "2026-05-22",
                "budget_post_id": budget_post.id,
                "direction": "inflow",
                "line_type": "planned",
                "label": "Flux test V13",
                "projected_amount": 40.0,
                "sequence": 1,
                "cash_state": "planned",
            }
        )
        self._recompute(guard, moves=[inv])
        self.assertEqual(len(guard.projection_period_move_ids), 1)
        self.assertEqual(guard.projection_period_move_ids.move_id, inv)

    def test_detail_status_order_prioritizes_risk_then_warning_then_safe(self):
        safe_inv = self._create_invoice_one_line(
            price_unit=500.0,
            move_type="in_invoice",
            invoice_date="2026-05-09",
            invoice_date_due="2026-05-15",
            tax_ids=[Command.clear()],
            post=True,
        )
        self._force_due_date(safe_inv, "2026-05-15")
        warning_inv = self._create_invoice_one_line(
            price_unit=600.0,
            move_type="in_invoice",
            invoice_date="2026-05-09",
            invoice_date_due="2026-05-22",
            tax_ids=[Command.clear()],
            post=True,
        )
        self._force_due_date(warning_inv, "2026-05-22")
        risk_inv = self._create_invoice_one_line(
            price_unit=4000.0,
            move_type="in_invoice",
            invoice_date="2026-05-09",
            invoice_date_due="2026-05-29",
            tax_ids=[Command.clear()],
            post=True,
        )
        self._force_due_date(risk_inv, "2026-05-29")
        guard = self._create_guard()
        self._recompute(
            guard,
            bank_balance=4200.0,
            moves=[safe_inv, warning_inv, risk_inv],
        )
        details = guard.projection_period_move_ids.sorted(
            key=lambda line: (
                line.period_risk_sequence,
                line.week_index,
                line.projected_date,
                line.signed_amount,
                line.id,
            )
        )
        self.assertEqual(
            details.mapped("period_risk_status"),
            ["risk", "warning", "safe"],
        )
        self.assertEqual(details.mapped("period_risk_sequence"), [10, 20, 30])
        unsecured_details = guard.projection_unsecured_period_move_ids.sorted(
            key=lambda line: (
                line.period_risk_sequence,
                line.week_index,
                line.projected_date,
                line.signed_amount,
                line.id,
            )
        )
        self.assertEqual(
            unsecured_details.mapped("period_risk_status"),
            ["risk", "warning"],
        )
        self.assertEqual(len(details), 3)

    def test_action_open_source_invoice_returns_move_form(self):
        inv = self._create_invoice_one_line(
            price_unit=300.0,
            move_type="in_invoice",
            invoice_date="2026-05-09",
            invoice_date_due="2026-05-20",
            tax_ids=[Command.clear()],
            post=True,
        )
        self._force_due_date(inv, "2026-05-20")
        guard = self._create_guard()
        self._recompute(guard, moves=[inv])
        detail = guard.projection_period_move_ids.filtered(lambda d: d.move_id == inv)
        detail.ensure_one()
        action = detail.action_open_source_invoice()
        self.assertEqual(action.get("type"), "ir.actions.act_window")
        self.assertEqual(action.get("res_model"), "account.move")
        self.assertEqual(action.get("res_id"), inv.id)
        self.assertEqual(action.get("view_mode"), "form")
