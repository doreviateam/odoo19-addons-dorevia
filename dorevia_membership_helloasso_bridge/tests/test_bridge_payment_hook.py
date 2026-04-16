# -*- coding: utf-8 -*-

import datetime

from odoo import fields
from odoo.tests.common import TransactionCase, tagged

from .helloasso_account_test_guard import HelloassoAccountTestGuard


@tagged("post_install", "-at_install", "dorevia_membership_helloasso_bridge")
class TestBridgePaymentHook(HelloassoAccountTestGuard, TransactionCase):
    """E3 : pivot créé/mis à jour → pont invoqué si compte opt-in (sans logique dans helloasso_sync)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls._helloasso_guard_setup(
            cls.company,
            {
                "name": "Compte HA hook test",
                "environment": "sandbox",
                "use_for_members": True,
                "membership_bridge_enabled": False,
                "membership_pont_rail": "v1_line",
                "membership_bridge_product_id": False,
            },
            payment_ref_prefixes=("pay_hook_",),
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Payeur hook test",
                "email": "hook_payer@test.dorevia.local",
                "company_id": cls.company.id,
            }
        )
        cls.membership_product = cls.env["product.product"].create(
            {
                "name": "Adhésion hook test",
                "type": "service",
                "membership": True,
                "membership_date_from": fields.Date.today(),
                "membership_date_to": fields.Date.today()
                + datetime.timedelta(days=365),
                "list_price": 50.0,
            }
        )

    def test_hook_creates_membership_line_when_bridge_enabled(self):
        self.helloasso_account.write(
            {
                "membership_bridge_enabled": True,
                "membership_bridge_product_id": self.membership_product.id,
            }
        )
        payment = self.env["dorevia.helloasso.payment"].create(
            {
                "helloasso_payment_ref": "pay_hook_enabled_001",
                "company_id": self.company.id,
                "helloasso_account_id": self.helloasso_account.id,
                "payment_kind": "online",
                "amount_total": 42.0,
                "amount_tariff": 42.0,
                "payer_email": self.partner.email,
                "payment_date": fields.Datetime.now(),
                "campaign_type": "Membership",
            }
        )
        line = self.env["membership.membership_line"].search(
            [("dorevia_helloasso_payment_id", "=", payment.id)]
        )
        self.assertEqual(len(line), 1)
        self.assertEqual(line.partner, self.partner)
        self.assertEqual(line.state, "paid")
        self.assertFalse(payment.membership_v2_out_invoice_id)
        self.assertFalse(payment.membership_v2_account_payment_id)

    def test_tv209_v1_rail_hook_leaves_no_v2_accounting_links(self):
        """T-V2-09 : rail V1 — ligne membership sans facture, aucun lien constatation V2 sur le pivot."""
        self.helloasso_account.write(
            {
                "membership_pont_rail": "v1_line",
                "membership_bridge_enabled": True,
                "membership_bridge_product_id": self.membership_product.id,
            }
        )
        payment = self.env["dorevia.helloasso.payment"].create(
            {
                "helloasso_payment_ref": "pay_hook_tv209_v1",
                "company_id": self.company.id,
                "helloasso_account_id": self.helloasso_account.id,
                "payment_kind": "online",
                "amount_total": 42.0,
                "amount_tariff": 42.0,
                "payer_email": self.partner.email,
                "payment_date": fields.Datetime.now(),
                "campaign_type": "Membership",
            }
        )
        self.assertTrue(
            self.env["membership.membership_line"].search_count(
                [("dorevia_helloasso_payment_id", "=", payment.id)]
            )
        )
        self.assertFalse(payment.membership_v2_out_invoice_id)
        self.assertFalse(payment.membership_v2_account_payment_id)

    def test_hook_accepts_french_csv_campaign_type_adhesion(self):
        """Export CSV HelloAsso : colonne « Type de campagne » = Adhésion (pas seulement Membership)."""
        self.helloasso_account.write(
            {
                "membership_bridge_enabled": True,
                "membership_bridge_product_id": self.membership_product.id,
            }
        )
        payment = self.env["dorevia.helloasso.payment"].create(
            {
                "helloasso_payment_ref": "pay_hook_adhesion_fr_001",
                "company_id": self.company.id,
                "helloasso_account_id": self.helloasso_account.id,
                "payment_kind": "online",
                "amount_total": 42.0,
                "amount_tariff": 42.0,
                "payer_email": self.partner.email,
                "payment_date": fields.Datetime.now(),
                "campaign_type": "Adhésion",
            }
        )
        line = self.env["membership.membership_line"].search(
            [("dorevia_helloasso_payment_id", "=", payment.id)]
        )
        self.assertEqual(len(line), 1)

    def test_write_trigger_only_on_pivot_fields(self):
        """Import : write purement technique (ex. payload) → pas de réévaluation du pont."""
        Payment = self.env["dorevia.helloasso.payment"]
        self.assertFalse(
            Payment._membership_bridge_write_triggers_pivot({"source_payload": "{}"})
        )
        self.assertFalse(Payment._membership_bridge_write_triggers_pivot({}))
        self.assertTrue(
            Payment._membership_bridge_write_triggers_pivot({"payer_email": "x@y.z"})
        )
        self.assertTrue(
            Payment._membership_bridge_write_triggers_pivot(
                {"source_payload": "{}", "amount_tariff": 10.0}
            )
        )

    def test_hook_does_not_create_line_when_bridge_disabled(self):
        self.helloasso_account.write({"membership_bridge_enabled": False})
        payment = self.env["dorevia.helloasso.payment"].create(
            {
                "helloasso_payment_ref": "pay_hook_disabled_001",
                "company_id": self.company.id,
                "helloasso_account_id": self.helloasso_account.id,
                "payment_kind": "online",
                "amount_total": 42.0,
                "amount_tariff": 42.0,
                "payer_email": self.partner.email,
                "payment_date": fields.Datetime.now(),
                "campaign_type": "Membership",
            }
        )
        line = self.env["membership.membership_line"].search(
            [("dorevia_helloasso_payment_id", "=", payment.id)]
        )
        self.assertFalse(line)
