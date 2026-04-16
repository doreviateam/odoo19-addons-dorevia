# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase, tagged

from .helloasso_account_test_guard import HelloassoAccountTestGuard


@tagged("post_install", "-at_install", "dorevia_membership_helloasso_bridge")
class TestBridgePaymentMembershipLine(HelloassoAccountTestGuard, TransactionCase):
    """E1-3 + E1-4 : pivot simulé → service pont → ligne sans facture, idempotence no-op strict."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls._helloasso_guard_setup(
            cls.company,
            {
                "name": "Compte HA bridge test",
                "environment": "sandbox",
                "membership_bridge_enabled": False,
                "membership_pont_rail": "v1_line",
                "membership_bridge_product_id": False,
            },
            payment_ref_prefixes=("pay_bridge_",),
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Payeur bridge test",
                "email": "bridge_payer@test.dorevia.local",
                "company_id": cls.company.id,
            }
        )
        cls.membership_product = cls.env["product.product"].create(
            {
                "name": "Adhésion bridge test",
                "type": "service",
                "membership": True,
                "membership_date_from": fields.Date.today(),
                "membership_date_to": fields.Date.today() + timedelta(days=365),
                "list_price": 50.0,
            }
        )

    def _create_payment(self, ref_suffix="001"):
        # Éviter le hook E3 (import réel) : ces tests ciblent le service pont directement.
        return self.env["dorevia.helloasso.payment"].with_context(
            membership_bridge_skip_hook=True
        ).create(
            {
                "helloasso_payment_ref": "pay_bridge_%s" % ref_suffix,
                "company_id": self.company.id,
                "helloasso_account_id": self.helloasso_account.id,
                "payment_kind": "online",
                "amount_total": 42.0,
                "amount_tariff": 42.0,
                "payer_email": self.partner.email,
                "payment_date": fields.Datetime.now(),
            }
        )

    def test_process_creates_one_line_without_invoice(self):
        payment = self._create_payment()
        bridge = self.env["dorevia.membership.helloasso.bridge"]
        out = bridge.process_payment_to_membership_line(payment, self.membership_product)
        self.assertEqual(out["state"], "created")
        line = out["line"]
        self.assertTrue(line.exists())
        self.assertEqual(line.partner, self.partner)
        self.assertEqual(line.membership_id, self.membership_product)
        self.assertEqual(line.dorevia_helloasso_payment_id, payment)
        self.assertFalse(line.account_invoice_id)
        self.assertEqual(line.member_price, 42.0)
        self.assertEqual(line.state, "paid")

    def test_process_twice_is_strict_noop(self):
        payment = self._create_payment("noop")
        bridge = self.env["dorevia.membership.helloasso.bridge"]
        out1 = bridge.process_payment_to_membership_line(payment, self.membership_product)
        self.assertEqual(out1["state"], "created")
        line1 = out1["line"]
        out2 = bridge.process_payment_to_membership_line(payment, self.membership_product)
        self.assertEqual(out2["state"], "noop")
        self.assertEqual(out2["line"], line1)
        lines = self.env["membership.membership_line"].search(
            [("dorevia_helloasso_payment_id", "=", payment.id)]
        )
        self.assertEqual(len(lines), 1)

    def test_rejects_non_membership_product(self):
        payment = self._create_payment("prod")
        other = self.env["product.product"].create(
            {"name": "Pas une adhésion", "type": "service", "membership": False}
        )
        with self.assertRaises(UserError):
            self.env["dorevia.membership.helloasso.bridge"].process_payment_to_membership_line(
                payment, other
            )

    def test_rejects_inactive_partner(self):
        """S3-1 piste A : contact résolu mais archivé → refus métier côté bridge."""
        self.partner.write({"active": False})
        payment = self._create_payment("inactive_partner")
        with self.assertRaises(UserError) as cm:
            self.env["dorevia.membership.helloasso.bridge"].process_payment_to_membership_line(
                payment, self.membership_product
            )
        self.assertIn("archiv", (cm.exception.args[0] or "").lower())

    def test_rejects_archived_payment(self):
        """Piste B (éligibilité) : pivot archivé → refus avant résolution contact."""
        payment = self._create_payment("archived_pivot")
        payment.with_context(membership_bridge_skip_hook=True).write({"active": False})
        with self.assertRaises(UserError) as cm:
            self.env["dorevia.membership.helloasso.bridge"].process_payment_to_membership_line(
                payment, self.membership_product
            )
        msg = (cm.exception.args[0] or "").lower()
        self.assertIn("archiv", msg)
        self.assertIn("paiement", msg)

    def test_rejects_ambiguous_partner_email(self):
        payment = self._create_payment("amb")
        self.env["res.partner"].create(
            {
                "name": "Doublon email",
                "email": self.partner.email,
                "company_id": self.company.id,
            }
        )
        with self.assertRaises(UserError):
            self.env["dorevia.membership.helloasso.bridge"].process_payment_to_membership_line(
                payment, self.membership_product
            )

    def test_rejects_payment_date_outside_product_period(self):
        prod = self.env["product.product"].create(
            {
                "name": "Adhésion fenêtre 2020",
                "type": "service",
                "membership": True,
                "membership_date_from": date(2020, 1, 1),
                "membership_date_to": date(2020, 12, 31),
                "list_price": 50.0,
            }
        )
        payment = self.env["dorevia.helloasso.payment"].with_context(
            membership_bridge_skip_hook=True
        ).create(
            {
                "helloasso_payment_ref": "pay_bridge_outside_window",
                "company_id": self.company.id,
                "helloasso_account_id": self.helloasso_account.id,
                "payment_kind": "online",
                "amount_total": 42.0,
                "amount_tariff": 42.0,
                "payer_email": self.partner.email,
                "payment_date": datetime(2026, 4, 14, 12, 0, 0),
            }
        )
        with self.assertRaises(UserError):
            self.env["dorevia.membership.helloasso.bridge"].process_payment_to_membership_line(
                payment, prod
            )

    def test_accepts_payment_date_on_product_period_boundaries(self):
        """Une date de paiement le 1er jan. ou le 31 déc. (dans la fenêtre) est acceptée.

        Deux partenaires distincts : avec la règle V1 anti-recoupement, deux lignes pour le
        même contact + même produit sur la même période seraient impossibles.
        """
        prod = self.env["product.product"].create(
            {
                "name": "Adhésion fenêtre 2025",
                "type": "service",
                "membership": True,
                "membership_date_from": date(2025, 1, 1),
                "membership_date_to": date(2025, 12, 31),
                "list_price": 50.0,
            }
        )
        bridge = self.env["dorevia.membership.helloasso.bridge"]
        for idx, when in enumerate(
            (datetime(2025, 1, 1, 12, 0, 0), datetime(2025, 12, 31, 12, 0, 0))
        ):
            payer = self.env["res.partner"].create(
                {
                    "name": "Payeur borne %s" % idx,
                    "email": "boundary_payer_%s@test.dorevia.local" % idx,
                    "company_id": self.company.id,
                }
            )
            payment = self.env["dorevia.helloasso.payment"].with_context(
                membership_bridge_skip_hook=True
            ).create(
                {
                    "helloasso_payment_ref": "pay_bridge_boundary_%s" % idx,
                    "company_id": self.company.id,
                    "helloasso_account_id": self.helloasso_account.id,
                    "payment_kind": "online",
                    "amount_total": 10.0,
                    "amount_tariff": 10.0,
                    "payer_email": payer.email,
                    "payment_date": when,
                }
            )
            out = bridge.process_payment_to_membership_line(payment, prod)
            self.assertEqual(out["state"], "created", msg="boundary %s" % when)
            self.assertEqual(out["line"].date_from, date(2025, 1, 1))
            self.assertEqual(out["line"].date_to, date(2025, 12, 31))

    def test_rejects_overlapping_period_same_partner_and_product(self):
        bridge = self.env["dorevia.membership.helloasso.bridge"]
        Line = self.env["membership.membership_line"].sudo()
        df = self.membership_product.membership_date_from
        dt_to = self.membership_product.membership_date_to
        Line.create(
            {
                "partner": self.partner.id,
                "membership_id": self.membership_product.id,
                "member_price": 1.0,
                "date": fields.Date.today(),
                "date_from": df,
                "date_to": dt_to,
                "state": "paid",
            }
        )
        payment = self._create_payment("overlap_same_prod")
        with self.assertRaises(UserError):
            bridge.process_payment_to_membership_line(payment, self.membership_product)

    def test_creates_line_when_prior_line_other_period_non_overlapping(self):
        """Renouvellement : autre période (autre produit) → nouvelle ligne autorisée."""
        bridge = self.env["dorevia.membership.helloasso.bridge"]
        Line = self.env["membership.membership_line"].sudo()
        prod_old = self.env["product.product"].create(
            {
                "name": "Adhésion fenêtre 2019",
                "type": "service",
                "membership": True,
                "membership_date_from": date(2019, 1, 1),
                "membership_date_to": date(2019, 12, 31),
                "list_price": 10.0,
            }
        )
        Line.create(
            {
                "partner": self.partner.id,
                "membership_id": prod_old.id,
                "member_price": 10.0,
                "date": date(2019, 6, 1),
                "date_from": date(2019, 1, 1),
                "date_to": date(2019, 12, 31),
                "state": "paid",
            }
        )
        payment = self._create_payment("renew_other_window")
        out = bridge.process_payment_to_membership_line(payment, self.membership_product)
        self.assertEqual(out["state"], "created")
        self.assertEqual(out["line"].membership_id, self.membership_product)

    def test_s72_require_member_type_raises_when_opt_in_and_missing(self):
        """E2 S7-2 option A : typologie exigée sur le compte et contact sans member_type_id."""
        self.helloasso_account.write({"membership_bridge_require_member_type": True})
        payment = self._create_payment("s72_no_member_type")
        with self.assertRaises(UserError) as cm:
            self.env["dorevia.membership.helloasso.bridge"].process_payment_to_membership_line(
                payment, self.membership_product
            )
        msg = (cm.exception.args[0] or "").lower()
        self.assertIn("type", msg)
        self.assertIn("typologie", msg)

    def test_s72_require_member_type_passes_when_typology_set(self):
        """E2 S7-2 : avec typologie exigée, contact typé → ligne créée."""
        cat = self.env["res.partner.category"].create(
            {"name": "Typologie S72 test bridge"}
        )
        self.partner.write({"member_type_id": cat.id})
        self.helloasso_account.write({"membership_bridge_require_member_type": True})
        payment = self._create_payment("s72_with_member_type")
        out = self.env["dorevia.membership.helloasso.bridge"].process_payment_to_membership_line(
            payment, self.membership_product
        )
        self.assertEqual(out["state"], "created")
