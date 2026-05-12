# -*- coding: utf-8 -*-

from datetime import date, timedelta
from unittest.mock import patch

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestPurchaseSimulation(TransactionCase):
    """Tests V1.1 for dorevia_cash_simulation_purchase — purchase order simulation."""

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
                "name": "Purchase Simulation Test Post",
                "account_ids": [(6, 0, [cls.account.id])],
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {"name": "Fournisseur Test Simulation"}
        )

    def _today(self):
        return date(2026, 5, 12)

    def _future(self, days=30):
        return self._today() + timedelta(days=days)

    def _past(self, days=1):
        return self._today() - timedelta(days=days)

    def _create_guard(self, include_simulation=False, threshold=0.0):
        with patch.object(fields.Date, "context_today", return_value=self._today()):
            return self.env["dorevia.cash.guard"].create(
                {
                    "date_from": "2026-05-01",
                    "date_to": "2026-07-31",
                    "bank_journal_id": self.bank_journal.id,
                    "company_id": self.company.id,
                    "alert_threshold": threshold,
                    "include_simulation": include_simulation,
                }
            )

    def _create_po(self, amount=1000.0, simulation=False, due_date=None, state="draft"):
        product = self.env["product.product"].create(
            {"name": "Prod Achat Simulation", "list_price": amount}
        )
        order = self.env["purchase.order"].create(
            {
                "partner_id": self.partner.id,
                "company_id": self.company.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": product.id,
                            "product_qty": 1,
                            "price_unit": amount,
                        },
                    )
                ],
            }
        )
        if simulation:
            order.write(
                {
                    "cash_simulation_ok": True,
                    "cash_simulation_due_date": due_date or self._future(),
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
    # 1. Contraintes de validation
    # ──────────────────────────────────────────────────────────────────────

    def test_activation_without_date_raises(self):
        order = self._create_po(simulation=False)
        with self.assertRaises(ValidationError):
            order.write({"cash_simulation_ok": True})

    def test_activation_with_past_date_raises(self):
        order = self._create_po(simulation=False)
        with self.assertRaises(ValidationError):
            order.write(
                {
                    "cash_simulation_ok": True,
                    "cash_simulation_due_date": self._past(),
                }
            )

    def test_activation_with_future_date_ok(self):
        order = self._create_po(simulation=False)
        order.write(
            {
                "cash_simulation_ok": True,
                "cash_simulation_due_date": self._future(),
            }
        )
        self.assertTrue(order.cash_simulation_ok)
        self.assertEqual(order.cash_simulation_due_date, self._future())

    def test_date_change_to_past_on_active_simulation_raises(self):
        order = self._create_po(simulation=True, due_date=self._future())
        with self.assertRaises(ValidationError):
            order.write({"cash_simulation_due_date": self._past()})

    def test_unrelated_write_on_stale_simulation_ok(self):
        """Modifying an unrelated field on a stale simulation must not raise."""
        order = self._create_po(simulation=True, due_date=self._future(1))
        with patch.object(fields.Date, "today", return_value=self._future(5)):
            order.write({"notes": "test"})

    # ──────────────────────────────────────────────────────────────────────
    # 2. Éligibilité
    # ──────────────────────────────────────────────────────────────────────

    def test_eligible_draft_simulation(self):
        order = self._create_po(simulation=True, due_date=self._future())
        self.assertTrue(order.cash_simulation_eligible)

    def test_eligible_sent_simulation(self):
        order = self._create_po(simulation=True, due_date=self._future(), state="sent")
        self.assertTrue(order.cash_simulation_eligible)

    def test_not_eligible_unmarked(self):
        order = self._create_po(simulation=False)
        self.assertFalse(order.cash_simulation_eligible)

    def test_confirmed_order_not_eligible(self):
        order = self._create_po(simulation=True, due_date=self._future())
        self.assertTrue(order.cash_simulation_eligible)
        order.button_confirm()
        order.invalidate_recordset()
        self.assertFalse(order.cash_simulation_eligible)

    def test_cancelled_order_not_eligible(self):
        order = self._create_po(simulation=True, due_date=self._future())
        order.button_cancel()
        order.invalidate_recordset()
        self.assertFalse(order.cash_simulation_eligible)

    # ──────────────────────────────────────────────────────────────────────
    # 3. Domaine de recherche
    # ──────────────────────────────────────────────────────────────────────

    def test_search_excludes_other_company(self):
        company_b = self.env["res.company"].create({"name": "Société B Achat"})
        partner_b = self.env["res.partner"].create({"name": "Fournisseur B"})
        product_b = self.env["product.product"].create(
            {"name": "Prod B", "list_price": 500}
        )
        order_b = (
            self.env["purchase.order"]
            .with_company(company_b)
            .create(
                {
                    "partner_id": partner_b.id,
                    "company_id": company_b.id,
                    "order_line": [
                        (
                            0,
                            0,
                            {
                                "product_id": product_b.id,
                                "product_qty": 1,
                                "price_unit": 500,
                            },
                        ),
                    ],
                }
            )
        )
        order_b.write(
            {
                "cash_simulation_ok": True,
                "cash_simulation_due_date": self._future(),
            }
        )
        guard = self._create_guard(include_simulation=True)
        orders = guard._search_eligible_purchase_simulation_orders()
        self.assertNotIn(order_b, orders)

    def test_search_excludes_stale_date(self):
        order = self._create_po(simulation=True, due_date=self._future(1))
        guard = self._create_guard(include_simulation=True)
        with patch.object(fields.Date, "today", return_value=self._future(5)):
            orders = guard._search_eligible_purchase_simulation_orders()
        self.assertNotIn(order, orders)

    # ──────────────────────────────────────────────────────────────────────
    # 4. Projection Cash Guard — montants négatifs
    # ──────────────────────────────────────────────────────────────────────

    def test_simulation_off_no_impact(self):
        self._create_po(simulation=True, due_date=self._future(), amount=5000)
        guard = self._create_guard(include_simulation=False)
        self._recompute_with_zero_balance(guard)
        meta = guard._split_exercise_periods()
        sit = guard.situation_date
        buckets = guard._manual_line_net_by_week_index(meta, sit)
        total = sum(buckets.values())
        self.assertEqual(total, 0.0)

    def test_simulation_on_subtracts_amount(self):
        order = self._create_po(
            simulation=True, due_date=self._future(), amount=5000
        )
        guard = self._create_guard(include_simulation=True)
        self._recompute_with_zero_balance(guard)
        meta = guard._split_exercise_periods()
        sit = guard.situation_date
        with patch.object(fields.Date, "context_today", return_value=self._today()):
            buckets = guard._manual_line_net_by_week_index(meta, sit)
        total = sum(buckets.values())
        self.assertAlmostEqual(total, -order.amount_total, places=2)

    def test_simulation_bucket_correct_week(self):
        due = self._future(20)
        self._create_po(simulation=True, due_date=due, amount=3000)
        guard = self._create_guard(include_simulation=True)
        self._recompute_with_zero_balance(guard)
        meta = guard._split_exercise_periods()
        sit = guard.situation_date
        expected_idx = guard._week_index_for_date(meta, due)
        self.assertIsNotNone(expected_idx)
        with patch.object(fields.Date, "context_today", return_value=self._today()):
            buckets = guard._manual_line_net_by_week_index(meta, sit)
        self.assertIn(expected_idx, buckets)
        self.assertLess(buckets[expected_idx], 0.0)

    # ──────────────────────────────────────────────────────────────────────
    # 5. Combinaison ventes + achats
    # ──────────────────────────────────────────────────────────────────────

    def test_sale_and_purchase_simulation_combined(self):
        """Sale inflow and purchase outflow combine correctly."""
        sale_product = self.env["product.product"].create(
            {"name": "Prod Vente Sim", "list_price": 3000}
        )
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "company_id": self.company.id,
                "order_line": [
                    (0, 0, {"product_id": sale_product.id, "product_uom_qty": 1, "price_unit": 3000}),
                ],
            }
        )
        due = self._future(15)
        sale_order.write(
            {"cash_simulation_ok": True, "cash_simulation_due_date": due}
        )
        purchase_order = self._create_po(
            simulation=True, due_date=due, amount=1000
        )

        guard = self._create_guard(include_simulation=True)
        self._recompute_with_zero_balance(guard)
        meta = guard._split_exercise_periods()
        sit = guard.situation_date
        with patch.object(fields.Date, "context_today", return_value=self._today()):
            buckets = guard._manual_line_net_by_week_index(meta, sit)
        total = sum(buckets.values())
        expected_net = sale_order.amount_total - purchase_order.amount_total
        self.assertAlmostEqual(total, expected_net, places=2)

    # ──────────────────────────────────────────────────────────────────────
    # 6. Smart button achats
    # ──────────────────────────────────────────────────────────────────────

    def test_purchase_simulation_count(self):
        self._create_po(simulation=True, due_date=self._future())
        self._create_po(simulation=True, due_date=self._future())
        self._create_po(simulation=False)
        guard = self._create_guard(include_simulation=True)
        guard.invalidate_recordset()
        self.assertEqual(guard.simulation_purchase_count, 2)

    def test_purchase_simulation_count_off(self):
        self._create_po(simulation=True, due_date=self._future())
        guard = self._create_guard(include_simulation=False)
        guard.invalidate_recordset()
        self.assertEqual(guard.simulation_purchase_count, 0)

    def test_action_view_purchase_simulation_orders(self):
        self._create_po(simulation=True, due_date=self._future())
        guard = self._create_guard(include_simulation=True)
        action = guard.action_view_purchase_simulation_orders()
        self.assertEqual(action["res_model"], "purchase.order")
