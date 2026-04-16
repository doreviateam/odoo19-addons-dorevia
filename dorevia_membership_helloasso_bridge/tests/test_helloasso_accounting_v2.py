# -*- coding: utf-8 -*-

"""Batterie T-V2 (prioritaire + extension F2) : rail, idempotence, partenaires, mapping §5.3."""

from datetime import timedelta
from unittest.mock import MagicMock, patch

from odoo import fields
from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.exceptions import UserError
from odoo.tests.common import tagged

from .helloasso_account_test_guard import HelloassoAccountTestGuard


@tagged("post_install", "-at_install", "helloasso_v2_accounting")
class TestHelloassoAccountingV2(HelloassoAccountTestGuard, AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls._helloasso_guard_setup(
            cls.company,
            {
                "name": "Compte HA V2 test",
                "environment": "sandbox",
                "use_for_members": True,
                "membership_bridge_enabled": True,
                "membership_pont_rail": "v2_accounting",
            },
            payment_ref_prefixes=("pay_v2_",),
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Payeur V2 test",
                "email": "v2_payer_accounting@test.dorevia.local",
                "company_id": cls.company.id,
                "property_account_receivable_id": cls.company_data[
                    "default_account_receivable"
                ].id,
            }
        )
        cls.membership_product = cls.env["product.product"].create(
            {
                "name": "Adhésion V2 test",
                "type": "service",
                "membership": True,
                "membership_date_from": fields.Date.today() - timedelta(days=2),
                "membership_date_to": fields.Date.today() + timedelta(days=365),
                "list_price": 10.0,
                "property_account_income_id": cls.company_data[
                    "default_account_revenue"
                ].id,
            }
        )
        cls.helloasso_account.write(
            {"membership_bridge_product_id": cls.membership_product.id}
        )

    def _create_pivot_payment(self, ref="pay_v2_001", skip_hook=False, **extra):
        vals = {
            "helloasso_payment_ref": ref,
            "company_id": self.company.id,
            "helloasso_account_id": self.helloasso_account.id,
            "payment_kind": "online",
            "amount_total": 10.0,
            "amount_tariff": 10.0,
            "payer_email": self.partner.email,
            "payment_date": fields.Datetime.now(),
            "campaign_type": "Membership",
        }
        vals.update(extra)
        Pay = self.env["dorevia.helloasso.payment"]
        if skip_hook:
            Pay = Pay.with_context(membership_bridge_skip_hook=True)
        return Pay.create(vals)

    def test_tv201_pivot_links_invoice_and_payment(self):
        """T-V2-01 : liens pivot → facture postée + paiement."""
        payment = self._create_pivot_payment()
        self.assertTrue(payment.membership_v2_out_invoice_id)
        move = payment.membership_v2_out_invoice_id
        self.assertEqual(move.move_type, "out_invoice")
        self.assertEqual(move.state, "posted")
        self.assertEqual(move.payment_state, "paid")
        self.assertEqual(
            move.ref,
            f"HelloAsso:{payment.helloasso_payment_ref}",
        )
        line = move.invoice_line_ids.filtered(lambda l: l.display_type == "product")[:1]
        self.assertTrue(line)
        self.assertIn("HelloAsso", line.name)
        self.assertIn(self.membership_product.display_name, line.name)
        self.assertTrue(payment.membership_v2_account_payment_id)
        self.assertEqual(payment.membership_v2_processing_state, "processed")
        # Marketing (UTM) : renseigné depuis le pivot (§ bloc Autres informations)
        if "campaign_id" in move._fields:
            self.assertTrue(move.source_id)
            self.assertEqual(move.source_id.name, "HelloAsso")
            self.assertTrue(move.medium_id)
            self.assertEqual(move.medium_id.name, "Membership")
            self.assertTrue(move.campaign_id)
            self.assertIn(payment.helloasso_payment_ref, move.campaign_id.name)
        if "preferred_payment_method_line_id" in move._fields:
            self.assertTrue(
                move.preferred_payment_method_line_id,
                "Mode de paiement facture aligné sur la ligne HelloAsso (V2).",
            )
            self.assertIn(
                "HelloAsso",
                move.preferred_payment_method_line_id.name,
            )
        act_inv = payment.action_open_membership_v2_invoice()
        self.assertEqual(act_inv.get("type"), "ir.actions.act_window")
        self.assertEqual(act_inv.get("res_model"), "account.move")
        self.assertEqual(act_inv.get("res_id"), move.id)
        act_pay = payment.action_open_membership_v2_account_payment()
        self.assertEqual(act_pay.get("res_model"), "account.payment")
        self.assertEqual(
            act_pay.get("res_id"),
            payment.membership_v2_account_payment_id.id,
        )

    def test_s63_open_v2_actions_raise_without_links(self):
        """S6-3 : pas de pièce liée → UserError (appel direct / garde)."""
        payment = self._create_pivot_payment("pay_v2_no_bridge_stat", skip_hook=True)
        self.assertFalse(payment.membership_v2_out_invoice_id)
        with self.assertRaises(UserError):
            payment.action_open_membership_v2_invoice()
        with self.assertRaises(UserError):
            payment.action_open_membership_v2_account_payment()

    def test_s64_search_domain_v2_rail_without_invoice(self):
        """S6-4 : domaine « Pont V2 — sans facture » (recherche)."""
        domain = [
            ("helloasso_account_id.membership_pont_rail", "=", "v2_accounting"),
            ("membership_v2_out_invoice_id", "=", False),
        ]
        Pay = self.env["dorevia.helloasso.payment"].sudo()
        pivot_no_inv = self._create_pivot_payment("pay_v2_s64_skip", skip_hook=True)
        self.assertFalse(pivot_no_inv.membership_v2_out_invoice_id)
        self.assertEqual(
            Pay.search_count(domain + [("id", "=", pivot_no_inv.id)]),
            1,
        )
        pivot_with_inv = self._create_pivot_payment("pay_v2_s64_done")
        self.assertTrue(pivot_with_inv.membership_v2_out_invoice_id)
        self.assertEqual(
            Pay.search_count(domain + [("id", "=", pivot_with_inv.id)]),
            0,
        )

    def test_tv201b_invoice_line_prefers_campaign_name_with_helloasso_suffix(self):
        """T-V2-01b : libellé ligne = campagne + suffixe (sans écraser la campagne)."""
        payment = self._create_pivot_payment(
            "pay_v2_campaign_lbl",
            campaign_name="Adhésion GLZ 2026",
        )
        move = payment.membership_v2_out_invoice_id
        line = move.invoice_line_ids.filtered(lambda l: l.display_type == "product")[:1]
        self.assertIn("Adhésion GLZ 2026", line.name)
        self.assertIn("HelloAsso", line.name)
        self.assertTrue(line.name.endswith("HelloAsso") or " — HelloAsso" in line.name)
        if "campaign_id" in move._fields:
            self.assertEqual(move.campaign_id.name, "Adhésion GLZ 2026")

    def test_tv201c_invoice_line_no_duplicate_helloasso_in_label(self):
        """T-V2-01c : si la campagne contient déjà « HelloAsso », pas de suffixe doublon."""
        payment = self._create_pivot_payment(
            "pay_v2_no_dup_ha",
            campaign_name="Partenariat HelloAsso 2026",
        )
        move = payment.membership_v2_out_invoice_id
        line = move.invoice_line_ids.filtered(lambda l: l.display_type == "product")[:1]
        self.assertEqual(line.name.count("HelloAsso"), 1)

    def test_tv202_second_process_is_noop(self):
        """T-V2-02 : idempotence globale (second passage)."""
        payment = self._create_pivot_payment("pay_v2_noop")
        move1 = payment.membership_v2_out_invoice_id
        pay1 = payment.membership_v2_account_payment_id
        AccountingV2 = self.env["dorevia.membership.helloasso.accounting.v2"]
        out = AccountingV2.process_payment(payment, self.membership_product)
        self.assertEqual(out["state"], "noop")
        self.assertEqual(payment.membership_v2_processing_state, "noop")
        self.assertEqual(payment.membership_v2_out_invoice_id, move1)
        self.assertEqual(payment.membership_v2_account_payment_id, pay1)

    def test_tv211_no_direct_membership_line_create_in_service(self):
        """T-V2-11 : le service V2 ne crée pas de ligne d'adhésion hors flux facture OCA."""
        payment = self._create_pivot_payment(
            "pay_v2_count_create", skip_hook=True
        )
        LineModel = self.env.registry["membership.membership_line"]
        create_calls = []
        real_create = LineModel.create

        def counting_create(sudo_self, vals_list, *args, **kwargs):
            create_calls.append(1)
            return real_create(sudo_self, vals_list, *args, **kwargs)

        LineModel.create = counting_create
        try:
            self.env["dorevia.membership.helloasso.accounting.v2"].process_payment(
                payment, self.membership_product
            )
        finally:
            LineModel.create = real_create

        # Une création attendue depuis la ligne de facture (OCA membership / extension).
        self.assertEqual(
            len(create_calls),
            1,
            "Le rail V2 ne doit pas appeler membership.membership_line.create en plus du flux facture.",
        )
        self.assertEqual(payment.membership_v2_processing_state, "processed")

    def test_tv203_service_refused_when_rail_not_v2(self):
        """T-V2-03 : appel service V2 hors rail constatation → refus, aucune facture."""
        AccountingV2 = self.env["dorevia.membership.helloasso.accounting.v2"]
        self.helloasso_account.write({"membership_pont_rail": "v1_line"})
        try:
            payment = self._create_pivot_payment(
                "pay_v2_wrong_rail", skip_hook=True
            )
            inv_before = self.env["account.move"].search_count(
                [
                    ("ref", "=", f"HelloAsso:{payment.helloasso_payment_ref}"),
                    ("company_id", "=", self.company.id),
                ]
            )
            with self.assertRaises(UserError) as cm:
                AccountingV2.process_payment(payment, self.membership_product)
            self.assertIn("constatation comptable", str(cm.exception.args[0]).lower())
            inv_after = self.env["account.move"].search_count(
                [
                    ("ref", "=", f"HelloAsso:{payment.helloasso_payment_ref}"),
                    ("company_id", "=", self.company.id),
                ]
            )
            self.assertEqual(inv_before, inv_after)
        finally:
            self.helloasso_account.write({"membership_pont_rail": "v2_accounting"})

    def test_tv204_partner_not_found_distinct_message(self):
        """T-V2-04 : e-mail sans contact → message introuvable dédié."""
        AccountingV2 = self.env["dorevia.membership.helloasso.accounting.v2"]
        payment = self._create_pivot_payment(
            "pay_v2_no_partner",
            skip_hook=True,
            payer_email="definitely_no_such_user_zz@test.dorevia.local",
        )
        with self.assertRaises(UserError) as cm:
            AccountingV2.process_payment(payment, self.membership_product)
        msg = str(cm.exception.args[0])
        self.assertIn("aucun contact enregistré", msg.lower())
        self.assertIn("prénom et nom payeur", msg.lower())
        self.assertIn("pont v2", msg.lower())

    def test_tv204b_archived_partner_refused(self):
        """S3-1 / alignement V1 : contact résolu mais archivé → V2 refuse."""
        payment = self._create_pivot_payment("pay_v2_archived_partner", skip_hook=True)
        self.partner.write({"active": False})
        AccountingV2 = self.env["dorevia.membership.helloasso.accounting.v2"]
        with self.assertRaises(UserError) as cm:
            AccountingV2.process_payment(payment, self.membership_product)
        self.assertIn("archiv", str(cm.exception.args[0]).lower())

    def test_tv204c_archived_payment_refused(self):
        """Piste B : pivot archivé → V2 refuse avant résolution partenaire."""
        payment = self._create_pivot_payment("pay_v2_archived_pivot", skip_hook=True)
        payment.with_context(membership_bridge_skip_hook=True).write({"active": False})
        AccountingV2 = self.env["dorevia.membership.helloasso.accounting.v2"]
        with self.assertRaises(UserError) as cm:
            AccountingV2.process_payment(payment, self.membership_product)
        msg = str(cm.exception.args[0]).lower()
        self.assertIn("archiv", msg)
        self.assertIn("paiement", msg)

    def test_tv205_partner_ambiguous_distinct_message(self):
        """T-V2-05 : deux contacts même e-mail → message ambiguïté dédié."""
        email = "ambiguous_tv205@test.dorevia.local"
        self.env["res.partner"].create(
            {
                "name": "Doublon A TV205",
                "email": email,
                "company_id": False,
                "property_account_receivable_id": self.company_data[
                    "default_account_receivable"
                ].id,
            }
        )
        self.env["res.partner"].create(
            {
                "name": "Doublon B TV205",
                "email": email,
                "company_id": False,
                "property_account_receivable_id": self.company_data[
                    "default_account_receivable"
                ].id,
            }
        )
        AccountingV2 = self.env["dorevia.membership.helloasso.accounting.v2"]
        payment = self._create_pivot_payment(
            "pay_v2_ambiguous",
            skip_hook=True,
            payer_email=email,
        )
        with self.assertRaises(UserError) as cm:
            AccountingV2.process_payment(payment, self.membership_product)
        msg = str(cm.exception.args[0])
        self.assertIn("ambiguïté", msg.lower())
        self.assertIn("pont v2", msg.lower())

    def test_tv205b_disambiguate_same_email_with_prénom_nom(self):
        """T-V2-05b : même e-mail sur deux fiches — le prénom + nom du pivot désambiguïse."""
        email = "shared_tv205b@test.dorevia.local"
        self.env["res.partner"].create(
            {
                "name": "Alice Martin",
                "email": email,
                "company_id": False,
                "property_account_receivable_id": self.company_data[
                    "default_account_receivable"
                ].id,
            }
        )
        self.env["res.partner"].create(
            {
                "name": "Bob Martin",
                "email": email,
                "company_id": False,
                "property_account_receivable_id": self.company_data[
                    "default_account_receivable"
                ].id,
            }
        )
        payment = self._create_pivot_payment(
            "pay_v2_disambig",
            payer_email=email,
            payer_firstname="Alice",
            payer_lastname="Martin",
        )
        move = payment.membership_v2_out_invoice_id
        self.assertTrue(move)
        inv_partner = move.partner_id
        self.assertEqual((inv_partner.firstname or "").strip(), "Alice")
        self.assertEqual((inv_partner.lastname or "").strip(), "Martin")

    def test_tv214_auto_create_partner_when_identity_not_in_odoo(self):
        """T-V2-14 : prénom+nom+e-mail ne matchent aucune fiche → création contact (e-mail déjà ailleurs OK)."""
        parent = self.env["res.partner"].create(
            {
                "name": "Parent Seul",
                "email": "famille_tv214@test.dorevia.local",
                "company_id": False,
                "property_account_receivable_id": self.company_data[
                    "default_account_receivable"
                ].id,
            }
        )
        self.assertTrue(parent)
        payment = self._create_pivot_payment(
            "pay_v2_autocreate_child",
            payer_email="famille_tv214@test.dorevia.local",
            payer_firstname="Luc",
            payer_lastname="Enfant",
        )
        self.assertEqual(payment.membership_v2_processing_state, "processed")
        child = payment.membership_v2_out_invoice_id.partner_id
        self.assertEqual(child.email, "famille_tv214@test.dorevia.local")
        self.assertIn("Luc", child.name)
        self.assertIn("Enfant", child.name)
        self.assertNotEqual(child, parent)

    def test_tv206_non_membership_product_rejected(self):
        """T-V2-06 : produit non-adhésion → erreur, pas de facture."""
        AccountingV2 = self.env["dorevia.membership.helloasso.accounting.v2"]
        other = self.env["product.product"].create(
            {"name": "Service sans membership", "type": "service", "membership": False}
        )
        payment = self._create_pivot_payment("pay_v2_bad_prod", skip_hook=True)
        with self.assertRaises(UserError):
            AccountingV2.process_payment(payment, other)

    def test_tv206_payment_date_outside_product_period(self):
        """T-V2-06 : date de paiement hors fenêtre produit → erreur."""
        AccountingV2 = self.env["dorevia.membership.helloasso.accounting.v2"]
        narrow = self.env["product.product"].create(
            {
                "name": "Adhésion fenêtre étroite TV206",
                "type": "service",
                "membership": True,
                "membership_date_from": fields.Date.today() + timedelta(days=50),
                "membership_date_to": fields.Date.today() + timedelta(days=400),
                "list_price": 10.0,
                "property_account_income_id": self.company_data[
                    "default_account_revenue"
                ].id,
            }
        )
        payment = self._create_pivot_payment("pay_v2_bad_date", skip_hook=True)
        with self.assertRaises(UserError):
            AccountingV2.process_payment(payment, narrow)

    def test_tv207_payment_method_mapping_and_unknown_warning(self):
        """T-V2-07 : classification §5.3 + avertissement si moyen inconnu."""
        AccountingV2 = self.env["dorevia.membership.helloasso.accounting.v2"]
        log_name = (
            "odoo.addons.dorevia_membership_helloasso_bridge.models."
            "membership_helloasso_accounting_v2"
        )
        pay = self._create_pivot_payment("pay_v2_classif", skip_hook=True)
        pay.payment_method = "Carte bancaire"
        self.assertEqual(AccountingV2._classify_helloasso_payment_method(pay), "carte")
        pay.payment_method = "SEPA"
        self.assertEqual(AccountingV2._classify_helloasso_payment_method(pay), "virement")
        pay.payment_method = "Espèce"
        self.assertEqual(AccountingV2._classify_helloasso_payment_method(pay), "especes")
        pay.payment_method = "MoyenExotiqueInconnu"
        with self.assertLogs(log_name, level="WARNING") as captured:
            bucket = AccountingV2._classify_helloasso_payment_method(pay)
        self.assertEqual(bucket, "hors_ligne")
        self.assertTrue(
            any("non reconnu" in line.lower() for line in captured.output),
            captured.output,
        )
        pay.payment_method = False
        pay.payment_method_raw = False
        with self.assertLogs(log_name, level="DEBUG") as captured_empty:
            bucket_empty = AccountingV2._classify_helloasso_payment_method(pay)
        self.assertEqual(bucket_empty, "hors_ligne")
        self.assertTrue(captured_empty.output, captured_empty.output)

    def test_tv208_idempotent_journal_and_method_line(self):
        """T-V2-08 : double appel helpers → mêmes enregistrements."""
        AccountingV2 = self.env["dorevia.membership.helloasso.accounting.v2"]
        j1 = AccountingV2._get_helloasso_sale_journal(self.company)
        j2 = AccountingV2._get_helloasso_sale_journal(self.company)
        self.assertEqual(j1, j2)
        bank = AccountingV2._default_bank_journal(self.company)
        pay = self._create_pivot_payment("pay_v2_method_idem", skip_hook=True)
        pay.payment_method = "Virement bancaire"
        ml1 = AccountingV2._get_or_create_helloasso_payment_method_line(bank, pay)
        ml2 = AccountingV2._get_or_create_helloasso_payment_method_line(bank, pay)
        self.assertEqual(ml1, ml2)

    def test_hook_v2_skips_v1_bridge_method(self):
        """T-V2-10 : le hook rail V2 n'appelle pas ``process_payment_to_membership_line`` (V1)."""
        BridgeCls = self.env.registry["dorevia.membership.helloasso.bridge"]
        with patch.object(
            BridgeCls,
            "process_payment_to_membership_line",
            autospec=True,
        ) as mock_v1:
            payment = self._create_pivot_payment("pay_v2_hook_isolation")
            mock_v1.assert_not_called()
        self.assertTrue(payment.membership_v2_out_invoice_id)

    def test_f24_error_after_action_post_rollback_and_pivot_error(self):
        """F2-4 : échec après ``action_post`` → rollback invoqué (tout-ou-rien).

        On ne vérifie pas ici l'état pivot ``error`` en base : avec ``TransactionCase``, une
        exception remontée depuis ``process_payment`` peut annuler le savepoint du test avant
        lecture. La persistance erreur (curseur isolé + commit) est couverte en recette / HTTP ;
        l'essentiel automatisé est que le rollback V2 est bien déclenché.
        """
        AccountingV2 = self.env["dorevia.membership.helloasso.accounting.v2"]
        payment = self._create_pivot_payment("pay_v2_f24_regfail", skip_hook=True)
        v2_cls = (
            "odoo.addons.dorevia_membership_helloasso_bridge.models."
            "membership_helloasso_accounting_v2.DoreviaMembershipHelloassoAccountingV2"
        )
        rb_tracker = MagicMock(wraps=AccountingV2._rollback_v2_accounting)
        with patch(
            f"{v2_cls}._rollback_v2_accounting",
            new=rb_tracker,
        ):
            with patch(
                f"{v2_cls}._register_payment_on_invoice",
                side_effect=UserError("F2-4 forced"),
            ):
                with self.assertRaises(UserError):
                    AccountingV2.process_payment(payment, self.membership_product)
        rb_tracker.assert_called()

    def test_f25_invoice_cancel_blocked_keeps_invoice_link(self):
        """Facture postée non annulable : rollback conserve le lien pivot, pas d'unlink forcé."""
        AccountingV2 = self.env["dorevia.membership.helloasso.accounting.v2"]
        payment = self._create_pivot_payment("pay_v2_f25_cancel", skip_hook=True)
        sale_journal = AccountingV2._get_helloasso_sale_journal(self.company)
        move = self.env["account.move"].sudo().create(
            {
                "move_type": "out_invoice",
                "partner_id": self.partner.id,
                "company_id": self.company.id,
                "journal_id": sale_journal.id,
                "invoice_date": fields.Date.today(),
                "date": fields.Date.today(),
                "ref": f"HelloAsso:{payment.helloasso_payment_ref}",
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.membership_product.id,
                            "quantity": 1.0,
                            "price_unit": 10.0,
                            "name": "Ligne test F25",
                        },
                    )
                ],
            }
        )
        move.action_post()
        payment.with_context(membership_bridge_skip_hook=True).write(
            {"membership_v2_out_invoice_id": move.id}
        )
        with patch(
            "odoo.addons.account.models.account_move.AccountMove.button_cancel",
            side_effect=UserError("période verrouillée"),
        ):
            rb = AccountingV2._rollback_v2_accounting(
                payment, move, self.env["account.payment"]
            )
        self.assertTrue(rb.get("invoice_cancel_failed"))
        payment.invalidate_recordset()
        self.assertEqual(payment.membership_v2_out_invoice_id, move)
        self.assertEqual(move.state, "posted")

    def test_retry_after_error_resumes_and_clears_error_message(self):
        """Pivot en erreur avec facture postée impayée : nouveau passage enregistre le paiement."""
        AccountingV2 = self.env["dorevia.membership.helloasso.accounting.v2"]
        payment = self._create_pivot_payment("pay_v2_retry_err", skip_hook=True)
        sale_journal = AccountingV2._get_helloasso_sale_journal(self.company)
        move = self.env["account.move"].sudo().create(
            {
                "move_type": "out_invoice",
                "partner_id": self.partner.id,
                "company_id": self.company.id,
                "journal_id": sale_journal.id,
                "invoice_date": fields.Date.today(),
                "date": fields.Date.today(),
                "ref": f"HelloAsso:{payment.helloasso_payment_ref}",
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.membership_product.id,
                            "quantity": 1.0,
                            "price_unit": 10.0,
                            "name": "Ligne test retry",
                        },
                    )
                ],
            }
        )
        move.action_post()
        payment.with_context(membership_bridge_skip_hook=True).write(
            {
                "membership_v2_out_invoice_id": move.id,
                "membership_v2_processing_state": "error",
                "membership_v2_error_message": "Échec précédent simulé",
            }
        )
        AccountingV2.process_payment(payment, self.membership_product)
        payment.invalidate_recordset()
        self.assertEqual(payment.membership_v2_processing_state, "processed")
        self.assertFalse(payment.membership_v2_error_message)
        self.assertEqual(move.payment_state, "paid")
        self.assertTrue(payment.membership_v2_account_payment_id)
