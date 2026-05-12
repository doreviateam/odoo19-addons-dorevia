# -*- coding: utf-8 -*-

from datetime import date, timedelta
from unittest.mock import patch

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestCashSimulation(TransactionCase):
    """Tests for dorevia_cash_simulation — sale order simulation via Cash Guard selection."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.bank_journal = cls.env["account.journal"].search(
            [("type", "=", "bank")], limit=1
        )
        if not cls.bank_journal:
            raise AssertionError("Aucun journal bancaire disponible pour les tests.")
        cls.company = cls.bank_journal.company_id
        cls.currency = cls.company.currency_id
        cls.account = (
            cls.bank_journal.default_account_id
            or cls.bank_journal.payment_debit_account_id
            or cls.bank_journal.payment_credit_account_id
        )
        if not cls.account:
            raise AssertionError("Aucun compte de liquidité disponible.")
        cls.budget_post = cls.env["account.budget.post"].create(
            {
                "name": "Simulation Test Post",
                "account_ids": [(6, 0, [cls.account.id])],
            }
        )
        cls.partner = cls.env["res.partner"].create({"name": "Client Test Simulation"})

    def _today(self):
        return date(2026, 5, 12)

    def _future(self, days=30):
        return self._today() + timedelta(days=days)

    def _create_guard(self, include_simulation=False, sale_orders=None):
        with patch.object(fields.Date, "context_today", return_value=self._today()):
            vals = {
                "date_from": "2026-05-01",
                "date_to": "2026-07-31",
                "bank_journal_id": self.bank_journal.id,
                "company_id": self.company.id,
                "alert_threshold": 0.0,
                "include_simulation": include_simulation,
            }
            if sale_orders:
                vals["simulation_sale_order_ids"] = [(6, 0, sale_orders.ids)]
            return self.env["dorevia.cash.guard"].create(vals)

    def _create_quote(self, amount=1000.0, validity_date=None, state="draft"):
        product = self.env["product.product"].create(
            {"name": "Prod Simulation", "list_price": amount}
        )
        order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "company_id": self.company.id,
                "validity_date": self._future() if validity_date is None else validity_date,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": product.id,
                            "product_uom_qty": 1,
                            "price_unit": amount,
                        },
                    )
                ],
            }
        )
        if state == "sent":
            order.state = "sent"
        return order

    def _recompute_with_zero_balance(self, guard):
        with patch.object(fields.Date, "context_today", return_value=self._today()):
            with patch.object(
                type(guard), "_compute_bank_balance_at_date", return_value=0.0
            ):
                with patch.object(
                    type(guard), "_compute_bank_confirmation_rate", return_value=0.0
                ):
                    with patch.object(
                        type(guard),
                        "_search_open_invoice_moves",
                        return_value=self.env["account.move"],
                    ):
                        guard.action_recompute_projection()

    # ──────────────────────────────────────────────────────────────────────
    # 1. Contrainte : simulation ON sans devis → erreur
    # ──────────────────────────────────────────────────────────────────────

    def test_simulation_on_without_orders_raises(self):
        with self.assertRaises(ValidationError):
            self._create_guard(include_simulation=True, sale_orders=None)

    def test_simulation_on_with_orders_ok(self):
        order = self._create_quote()
        guard = self._create_guard(include_simulation=True, sale_orders=order)
        self.assertTrue(guard.include_simulation)
        self.assertIn(order, guard.simulation_sale_order_ids)

    # ──────────────────────────────────────────────────────────────────────
    # 2. Toggle OFF vide les devis
    # ──────────────────────────────────────────────────────────────────────

    def test_toggle_off_clears_orders(self):
        order = self._create_quote()
        guard = self._create_guard(include_simulation=True, sale_orders=order)
        with patch.object(fields.Date, "context_today", return_value=self._today()):
            with patch.object(
                type(guard), "_compute_bank_balance_at_date", return_value=0.0
            ):
                with patch.object(
                    type(guard), "_compute_bank_confirmation_rate", return_value=0.0
                ):
                    with patch.object(
                        type(guard),
                        "_search_open_invoice_moves",
                        return_value=self.env["account.move"],
                    ):
                        guard.write({"include_simulation": False})
        self.assertFalse(guard.simulation_sale_order_ids)

    # ──────────────────────────────────────────────────────────────────────
    # 3. Éligibilité des devis sélectionnés
    # ──────────────────────────────────────────────────────────────────────

    def test_eligible_draft_with_validity_date(self):
        order = self._create_quote(validity_date=self._future(20))
        guard = self._create_guard(include_simulation=True, sale_orders=order)
        eligible = guard._get_eligible_sale_simulation_orders()
        self.assertIn(order, eligible)

    def test_eligible_sent_with_validity_date(self):
        order = self._create_quote(validity_date=self._future(20), state="sent")
        guard = self._create_guard(include_simulation=True, sale_orders=order)
        eligible = guard._get_eligible_sale_simulation_orders()
        self.assertIn(order, eligible)

    def test_not_eligible_no_validity_date(self):
        order = self._create_quote(validity_date=False)
        guard = self._create_guard(include_simulation=True, sale_orders=order)
        eligible = guard._get_eligible_sale_simulation_orders()
        self.assertNotIn(order, eligible)

    def test_not_eligible_validity_outside_period(self):
        order = self._create_quote(validity_date=date(2026, 9, 15))
        guard = self._create_guard(include_simulation=True, sale_orders=order)
        eligible = guard._get_eligible_sale_simulation_orders()
        self.assertNotIn(order, eligible)

    def test_confirmed_order_not_eligible(self):
        order = self._create_quote(validity_date=self._future(20))
        guard = self._create_guard(include_simulation=True, sale_orders=order)
        order.action_confirm()
        guard.invalidate_recordset()
        eligible = guard._get_eligible_sale_simulation_orders()
        self.assertNotIn(order, eligible)

    def test_cancelled_order_not_eligible(self):
        order = self._create_quote(validity_date=self._future(20))
        guard = self._create_guard(include_simulation=True, sale_orders=order)
        order._action_cancel()
        guard.invalidate_recordset()
        eligible = guard._get_eligible_sale_simulation_orders()
        self.assertNotIn(order, eligible)

    # ──────────────────────────────────────────────────────────────────────
    # 4. Domaine multi-société / devise
    # ──────────────────────────────────────────────────────────────────────

    def test_other_company_not_eligible(self):
        company_b = self.env["res.company"].create({"name": "Société B"})
        partner_b = self.env["res.partner"].create({"name": "Partner B"})
        product_b = self.env["product.product"].create(
            {"name": "Prod B", "list_price": 500}
        )
        order_b = (
            self.env["sale.order"]
            .with_company(company_b)
            .create(
                {
                    "partner_id": partner_b.id,
                    "company_id": company_b.id,
                    "validity_date": self._future(20),
                    "order_line": [
                        (0, 0, {"product_id": product_b.id, "product_uom_qty": 1, "price_unit": 500}),
                    ],
                }
            )
        )
        guard = self._create_guard(include_simulation=True, sale_orders=order_b)
        eligible = guard._get_eligible_sale_simulation_orders()
        self.assertNotIn(order_b, eligible)

    # ──────────────────────────────────────────────────────────────────────
    # 5. Projection Cash Guard
    # ──────────────────────────────────────────────────────────────────────

    def test_simulation_off_no_impact(self):
        order = self._create_quote(amount=5000, validity_date=self._future(20))
        guard = self._create_guard(include_simulation=False)
        self._recompute_with_zero_balance(guard)
        meta = guard._split_exercise_periods()
        sit = guard.situation_date
        buckets = guard._manual_line_net_by_week_index(meta, sit)
        total = sum(buckets.values())
        self.assertEqual(total, 0.0)

    def test_simulation_on_adds_amount(self):
        order = self._create_quote(amount=5000, validity_date=self._future(20))
        guard = self._create_guard(include_simulation=True, sale_orders=order)
        self._recompute_with_zero_balance(guard)
        meta = guard._split_exercise_periods()
        sit = guard.situation_date
        with patch.object(fields.Date, "context_today", return_value=self._today()):
            buckets = guard._manual_line_net_by_week_index(meta, sit)
        total = sum(buckets.values())
        self.assertAlmostEqual(total, order.amount_total, places=2)

    def test_simulation_bucket_correct_week(self):
        due = self._future(20)
        order = self._create_quote(amount=3000, validity_date=due)
        guard = self._create_guard(include_simulation=True, sale_orders=order)
        self._recompute_with_zero_balance(guard)
        meta = guard._split_exercise_periods()
        expected_idx = guard._week_index_for_date(meta, due)
        self.assertIsNotNone(expected_idx)
        with patch.object(fields.Date, "context_today", return_value=self._today()):
            buckets = guard._manual_line_net_by_week_index(meta, sit=guard.situation_date)
        self.assertIn(expected_idx, buckets)

    # ──────────────────────────────────────────────────────────────────────
    # 6. Recompute au changement
    # ──────────────────────────────────────────────────────────────────────

    def test_toggle_triggers_recompute(self):
        order = self._create_quote(amount=2000, validity_date=self._future(20))
        guard = self._create_guard(include_simulation=False)
        self._recompute_with_zero_balance(guard)
        bal_off = guard.forecast_final_balance

        with patch.object(fields.Date, "context_today", return_value=self._today()):
            with patch.object(
                type(guard), "_compute_bank_balance_at_date", return_value=0.0
            ):
                with patch.object(
                    type(guard), "_compute_bank_confirmation_rate", return_value=0.0
                ):
                    with patch.object(
                        type(guard),
                        "_search_open_invoice_moves",
                        return_value=self.env["account.move"],
                    ):
                        guard.write({
                            "include_simulation": True,
                            "simulation_sale_order_ids": [(6, 0, [order.id])],
                        })

        self.assertNotEqual(guard.forecast_final_balance, bal_off)

    # ──────────────────────────────────────────────────────────────────────
    # 7. Smart button
    # ──────────────────────────────────────────────────────────────────────

    def test_simulation_order_count(self):
        o1 = self._create_quote(validity_date=self._future(20))
        o2 = self._create_quote(validity_date=self._future(25))
        guard = self._create_guard(
            include_simulation=True, sale_orders=o1 | o2
        )
        guard.invalidate_recordset()
        self.assertEqual(guard.simulation_order_count, 2)

    def test_simulation_order_count_off(self):
        order = self._create_quote(validity_date=self._future(20))
        guard = self._create_guard(include_simulation=False)
        guard.invalidate_recordset()
        self.assertEqual(guard.simulation_order_count, 0)

    def test_action_view_simulation_orders(self):
        order = self._create_quote(validity_date=self._future(20))
        guard = self._create_guard(include_simulation=True, sale_orders=order)
        action = guard.action_view_simulation_orders()
        self.assertEqual(action["res_model"], "sale.order")

    # ──────────────────────────────────────────────────────────────────────
    # 8. Devis sélectionné mais devenu non éligible
    # ──────────────────────────────────────────────────────────────────────

    def test_selected_but_confirmed_excluded_from_projection(self):
        """A selected order that gets confirmed stays in M2M but is excluded from projection."""
        order = self._create_quote(amount=5000, validity_date=self._future(20))
        guard = self._create_guard(include_simulation=True, sale_orders=order)
        order.action_confirm()
        guard.invalidate_recordset()
        self.assertIn(order, guard.simulation_sale_order_ids)
        eligible = guard._get_eligible_sale_simulation_orders()
        self.assertNotIn(order, eligible)
        self.assertEqual(guard.simulation_order_count, 0)
