# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from unittest.mock import patch

from odoo import fields
from odoo.tests.common import TransactionCase


class TestPurchaseSimulation(TransactionCase):
    """Tests V1.1 for dorevia_cash_simulation_purchase — purchase order simulation via Cash Guard selection."""

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

    def _future_dt(self, days=30):
        return datetime.combine(self._future(days), datetime.min.time())

    def _create_guard(self, include_simulation=False, sale_orders=None, purchase_orders=None):
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
            if purchase_orders:
                vals["simulation_purchase_order_ids"] = [(6, 0, purchase_orders.ids)]
            return self.env["dorevia.cash.guard"].create(vals)

    def _create_sale_quote(self, amount=1000.0, validity_date=None):
        product = self.env["product.product"].create(
            {"name": "Prod Vente Sim", "list_price": amount}
        )
        return self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "company_id": self.company.id,
                "validity_date": validity_date or self._future(20),
                "order_line": [
                    (0, 0, {"product_id": product.id, "product_uom_qty": 1, "price_unit": amount}),
                ],
            }
        )

    def _create_po(self, amount=1000.0, date_planned=None, state="draft"):
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
                            "date_planned": date_planned or self._future_dt(20),
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
    # 1. Éligibilité PO
    # ──────────────────────────────────────────────────────────────────────

    def test_eligible_draft_po(self):
        sale = self._create_sale_quote()
        po = self._create_po(date_planned=self._future_dt(20))
        guard = self._create_guard(
            include_simulation=True, sale_orders=sale, purchase_orders=po
        )
        eligible = guard._get_eligible_purchase_simulation_orders()
        self.assertIn(po, eligible)

    def test_confirmed_po_not_eligible(self):
        sale = self._create_sale_quote()
        po = self._create_po(date_planned=self._future_dt(20))
        guard = self._create_guard(
            include_simulation=True, sale_orders=sale, purchase_orders=po
        )
        po.button_confirm()
        guard.invalidate_recordset()
        eligible = guard._get_eligible_purchase_simulation_orders()
        self.assertNotIn(po, eligible)

    def test_po_outside_period_not_eligible(self):
        sale = self._create_sale_quote()
        po = self._create_po(date_planned=self._future_dt(120))
        guard = self._create_guard(
            include_simulation=True, sale_orders=sale, purchase_orders=po
        )
        eligible = guard._get_eligible_purchase_simulation_orders()
        self.assertNotIn(po, eligible)

    # ──────────────────────────────────────────────────────────────────────
    # 2. Projection — montants négatifs
    # ──────────────────────────────────────────────────────────────────────

    def test_simulation_off_no_impact(self):
        po = self._create_po(amount=5000, date_planned=self._future_dt(20))
        guard = self._create_guard(include_simulation=False)
        self._recompute_with_zero_balance(guard)
        meta = guard._split_exercise_periods()
        sit = guard.situation_date
        buckets = guard._manual_line_net_by_week_index(meta, sit)
        total = sum(buckets.values())
        self.assertEqual(total, 0.0)

    def test_simulation_on_subtracts_amount(self):
        sale = self._create_sale_quote()
        po = self._create_po(amount=5000, date_planned=self._future_dt(20))
        guard = self._create_guard(
            include_simulation=True, sale_orders=sale, purchase_orders=po
        )
        self._recompute_with_zero_balance(guard)
        meta = guard._split_exercise_periods()
        sit = guard.situation_date
        with patch.object(fields.Date, "context_today", return_value=self._today()):
            buckets = guard._get_purchase_simulation_buckets(meta, sit)
        total = sum(buckets.values())
        self.assertAlmostEqual(total, -po.amount_total, places=2)

    # ──────────────────────────────────────────────────────────────────────
    # 3. Combinaison ventes + achats
    # ──────────────────────────────────────────────────────────────────────

    def test_sale_and_purchase_simulation_combined(self):
        sale = self._create_sale_quote(amount=3000, validity_date=self._future(15))
        po = self._create_po(amount=1000, date_planned=self._future_dt(15))
        guard = self._create_guard(
            include_simulation=True, sale_orders=sale, purchase_orders=po
        )
        self._recompute_with_zero_balance(guard)
        meta = guard._split_exercise_periods()
        sit = guard.situation_date
        with patch.object(fields.Date, "context_today", return_value=self._today()):
            buckets = guard._manual_line_net_by_week_index(meta, sit)
        total = sum(buckets.values())
        expected_net = sale.amount_total - po.amount_total
        self.assertAlmostEqual(total, expected_net, places=2)

    # ──────────────────────────────────────────────────────────────────────
    # 4. Smart button achats
    # ──────────────────────────────────────────────────────────────────────

    def test_purchase_simulation_count(self):
        sale = self._create_sale_quote()
        po1 = self._create_po(date_planned=self._future_dt(20))
        po2 = self._create_po(date_planned=self._future_dt(25))
        guard = self._create_guard(
            include_simulation=True,
            sale_orders=sale,
            purchase_orders=po1 | po2,
        )
        guard.invalidate_recordset()
        self.assertEqual(guard.simulation_purchase_count, 2)

    def test_purchase_simulation_count_off(self):
        guard = self._create_guard(include_simulation=False)
        guard.invalidate_recordset()
        self.assertEqual(guard.simulation_purchase_count, 0)

    def test_action_view_purchase_simulation_orders(self):
        sale = self._create_sale_quote()
        po = self._create_po(date_planned=self._future_dt(20))
        guard = self._create_guard(
            include_simulation=True, sale_orders=sale, purchase_orders=po
        )
        action = guard.action_view_purchase_simulation_orders()
        self.assertEqual(action["res_model"], "purchase.order")

    # ──────────────────────────────────────────────────────────────────────
    # 5. Toggle OFF vide les PO
    # ──────────────────────────────────────────────────────────────────────

    def test_toggle_off_clears_purchase_orders(self):
        sale = self._create_sale_quote()
        po = self._create_po(date_planned=self._future_dt(20))
        guard = self._create_guard(
            include_simulation=True, sale_orders=sale, purchase_orders=po
        )
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
        self.assertFalse(guard.simulation_purchase_order_ids)
