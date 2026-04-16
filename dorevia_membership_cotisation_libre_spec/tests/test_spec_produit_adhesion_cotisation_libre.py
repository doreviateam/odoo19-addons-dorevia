# -*- coding: utf-8 -*-
# ZeDocs : SPEC_TESTS_AUTOMATISES_PRODUIT_ADHESION_COTISATION_LIBRE_TENANT_01.md
# Spec fonctionnelle : SPEC_PRODUIT_ADHESION_COTISATION_LIBRE_TENANT_01.md
#
# Bloc A — tag : membership_spec_bloc_a
# Bloc B (écarts possibles spec vs standard + cas limites T05, T10, T11) — tag : membership_spec_bloc_b

from datetime import date
from datetime import timedelta

from freezegun import freeze_time

from odoo.tests import Form, common, tagged


@freeze_time("2026-06-15")
@tagged("post_install", "-at_install", "membership_spec_bloc_a")
class TestMembershipCotisationLibreBlocA(common.TransactionCase):
    """T01–T04, T06–T09 : conformité attendue si le produit est bien paramétré."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.account_partner = cls.env["account.account"].create(
            {
                "name": "GLZ spec receivable",
                "code": "GLZAR",
                "account_type": "asset_receivable",
                "reconcile": True,
            }
        )
        cls.account_income = cls.env["account.account"].create(
            {
                "name": "GLZ spec income",
                "code": "GLZIN",
                "account_type": "income",
            }
        )
        cls.journal = cls.env["account.journal"].create(
            {
                "name": "GLZ spec journal",
                "code": "GLZJ",
                "type": "sale",
                "default_account_id": cls.account_income.id,
            }
        )
        cls.partner_mathilde = cls.env["res.partner"].create(
            {
                "name": "Mathilde Panot",
                "property_account_receivable_id": cls.account_partner.id,
            }
        )
        cls.product_glz_2026 = cls.env["product.product"].create(
            {
                "type": "service",
                "name": "Adhésion GLZ 2026",
                "membership": True,
                "membership_date_from": date(2026, 1, 1),
                "membership_date_to": date(2026, 12, 31),
                "list_price": 10.0,
            }
        )
        cls.product_glz_2026.product_tmpl_id.write({"taxes_id": [(5, 0, 0)]})

    def _invoice_with_membership_line(self, invoice_date, price_unit, partner=None):
        partner = partner or self.partner_mathilde
        invoice_form = Form(
            self.env["account.move"].with_context(default_move_type="out_invoice")
        )
        invoice_form.invoice_date = invoice_date
        invoice_form.journal_id = self.journal
        invoice_form.partner_id = partner
        with invoice_form.invoice_line_ids.new() as line_form:
            line_form.product_id = self.product_glz_2026
            line_form.quantity = 1.0
            line_form.price_unit = price_unit
        return invoice_form.save()

    def _membership_line_from_invoice(self, invoice):
        inv_line = invoice.invoice_line_ids.filtered(
            lambda l: l.product_id == self.product_glz_2026
        )
        self.assertEqual(len(inv_line), 1)
        mline = self.env["membership.membership_line"].search(
            [("account_invoice_line", "=", inv_line.id)]
        )
        self.assertEqual(len(mline), 1)
        return mline

    def test_T01_parametrage_annuel_civil_du_produit(self):
        """Fenêtre produit + prix catalogue (ZeDocs §8 T01)."""
        self.assertEqual(self.product_glz_2026.membership_date_from, date(2026, 1, 1))
        self.assertEqual(self.product_glz_2026.membership_date_to, date(2026, 12, 31))
        self.assertEqual(self.product_glz_2026.list_price, 10.0)

    def test_T02_preenplissage_montant_defaut_wizard(self):
        """Wizard membership.invoice → 10 € par défaut (ZeDocs §8 T02)."""
        with Form(self.env["membership.invoice"]) as wiz_form:
            wiz_form.product_id = self.product_glz_2026
            self.assertEqual(wiz_form.member_price, 10.0)

    def test_T03_montant_librement_modifiable_vers_facture_25(self):
        """10 € → 25 € puis facture à 25 € (ZeDocs §8 T03)."""
        with Form(self.env["membership.invoice"]) as wiz_form:
            wiz_form.product_id = self.product_glz_2026
            self.assertEqual(wiz_form.member_price, 10.0)
            wiz_form.member_price = 25.0
            produit = wiz_form.product_id
            montant = wiz_form.member_price
        invoice = self.partner_mathilde.create_membership_invoice(produit, montant)
        if not invoice.journal_id:
            invoice.write({"journal_id": self.journal.id})
        line = invoice.invoice_line_ids.filtered(
            lambda l: l.product_id == self.product_glz_2026
        )
        self.assertEqual(line.price_unit, 25.0)

    def test_T04_date_fin_au_31_12_facture_2026_04_14(self):
        """date_to sur la ligne d'adhésion (ZeDocs §8 T04)."""
        invoice = self._invoice_with_membership_line(date(2026, 4, 14), 10.0)
        mline = self._membership_line_from_invoice(invoice)
        self.assertEqual(mline.date_to, date(2026, 12, 31))

    def test_T06_pas_de_logique_glissante_12_mois(self):
        """Fin d'année civile, pas +12 mois après le début (ZeDocs §8 T06)."""
        invoice = self._invoice_with_membership_line(date(2026, 11, 20), 10.0)
        mline = self._membership_line_from_invoice(invoice)
        self.assertEqual(mline.date_from, date(2026, 11, 20))
        self.assertEqual(mline.date_to, date(2026, 12, 31))
        faux_glissant = mline.date_from + timedelta(days=365)
        self.assertNotEqual(mline.date_to, faux_glissant)
        self.assertNotEqual(mline.date_to, date(2027, 11, 20))

    def test_T07_pas_de_prorata_automatique_fin_annee(self):
        """Montant saisi conservé tel quel (ZeDocs §8 T07)."""
        invoice = self._invoice_with_membership_line(date(2026, 12, 28), 7.0)
        self.assertEqual(invoice.amount_untaxed, 7.0)
        mline = self._membership_line_from_invoice(invoice)
        self.assertEqual(mline.member_price, 7.0)

    def test_T08_defaut_10_sans_contrainte_facture_12(self):
        """Proposition 10 € remplaçable par 12 € sur la facture (ZeDocs §8 T08)."""
        with Form(self.env["membership.invoice"]) as wiz_form:
            wiz_form.product_id = self.product_glz_2026
            self.assertEqual(wiz_form.member_price, 10.0)
            wiz_form.member_price = 12.0
            produit = wiz_form.product_id
            montant = wiz_form.member_price
        invoice = self.partner_mathilde.create_membership_invoice(produit, montant)
        if not invoice.journal_id:
            invoice.write({"journal_id": self.journal.id})
        line = invoice.invoice_line_ids.filtered(
            lambda l: l.product_id == self.product_glz_2026
        )
        self.assertEqual(line.price_unit, 12.0)

    def test_T09_coherence_ligne_adhesion(self):
        """Produit, montant, fin de période, état « en attente » en brouillon (ZeDocs §8 T09)."""
        invoice = self._invoice_with_membership_line(date(2026, 4, 14), 15.0)
        mline = self._membership_line_from_invoice(invoice)
        self.assertEqual(mline.membership_id, self.product_glz_2026)
        self.assertEqual(mline.member_price, 15.0)
        self.assertEqual(mline.date_to, date(2026, 12, 31))
        self.assertEqual(mline.state, "waiting")
        self.assertEqual(invoice.state, "draft")


@freeze_time("2026-06-15")
@tagged("post_install", "-at_install", "membership_spec_bloc_b")
class TestMembershipCotisationLibreBlocB(common.TransactionCase):
    """T05, T10, T11 : référence spec et frontières ; T05/T10 peuvent révéler un écart."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.account_partner = cls.env["account.account"].create(
            {
                "name": "GLZ spec B receivable",
                "code": "GLZBR",
                "account_type": "asset_receivable",
                "reconcile": True,
            }
        )
        cls.account_income = cls.env["account.account"].create(
            {
                "name": "GLZ spec B income",
                "code": "GLZBI",
                "account_type": "income",
            }
        )
        cls.journal = cls.env["account.journal"].create(
            {
                "name": "GLZ spec B journal",
                "code": "GLZB",
                "type": "sale",
                "default_account_id": cls.account_income.id,
            }
        )
        cls.partner_mathilde = cls.env["res.partner"].create(
            {
                "name": "Mathilde Panot",
                "property_account_receivable_id": cls.account_partner.id,
            }
        )
        cls.product_glz_2026 = cls.env["product.product"].create(
            {
                "type": "service",
                "name": "Adhésion GLZ 2026",
                "membership": True,
                "membership_date_from": date(2026, 1, 1),
                "membership_date_to": date(2026, 12, 31),
                "list_price": 10.0,
            }
        )
        cls.product_glz_2026.product_tmpl_id.write({"taxes_id": [(5, 0, 0)]})

    def _invoice_with_membership_line(self, invoice_date, price_unit):
        invoice_form = Form(
            self.env["account.move"].with_context(default_move_type="out_invoice")
        )
        invoice_form.invoice_date = invoice_date
        invoice_form.journal_id = self.journal
        invoice_form.partner_id = self.partner_mathilde
        with invoice_form.invoice_line_ids.new() as line_form:
            line_form.product_id = self.product_glz_2026
            line_form.quantity = 1.0
            line_form.price_unit = price_unit
        return invoice_form.save()

    def _membership_line_from_invoice(self, invoice):
        inv_line = invoice.invoice_line_ids.filtered(
            lambda l: l.product_id == self.product_glz_2026
        )
        self.assertEqual(len(inv_line), 1)
        mline = self.env["membership.membership_line"].search(
            [("account_invoice_line", "=", inv_line.id)]
        )
        self.assertEqual(len(mline), 1)
        return mline

    def test_T05_date_debut_egale_date_facture_dans_fenetre(self):
        """date_from = date de facture (ZeDocs §8 T05)."""
        invoice = self._invoice_with_membership_line(date(2026, 4, 14), 10.0)
        mline = self._membership_line_from_invoice(invoice)
        self.assertEqual(
            mline.date_from,
            date(2026, 4, 14),
            "Référence spec : alignement date début / date facture dans la fenêtre produit.",
        )

    def test_T10_synthese_membership_sur_fiche_contact(self):
        """membership_start / membership_stop / état (ZeDocs §8 T10).

        Si ``membership_extension`` est installé, ``membership_start`` / ``membership_stop``
        ne s'appuient que sur les lignes en état ``invoiced``, ``free`` ou ``paid`` :
        la facture doit être validée pour peupler la synthèse.
        """
        invoice = self._invoice_with_membership_line(date(2026, 4, 14), 10.0)
        invoice.action_post()
        mline = self._membership_line_from_invoice(invoice)
        self.assertEqual(mline.state, "invoiced")
        self.partner_mathilde.invalidate_recordset(
            ["membership_start", "membership_stop", "membership_state"]
        )
        self.assertEqual(self.partner_mathilde.membership_start, mline.date_from)
        self.assertEqual(self.partner_mathilde.membership_start, date(2026, 4, 14))
        self.assertEqual(self.partner_mathilde.membership_stop, date(2026, 12, 31))
        self.assertEqual(self.partner_mathilde.membership_state, "invoiced")

    def test_T11_facture_au_31_12_frontiere_periode_produit(self):
        """Dernier jour = borne haute produit : inégalité stricte sur date_to (ZeDocs §8 T11).

        Standard membership : si ``invoice_date < membership_date_to`` est faux (ex. facture
        le 31/12 alors que ``membership_date_to`` vaut aussi le 31/12), la date de début
        effective n'est pas recalée sur la date de facture : elle reste ``membership_date_from``.
        """
        invoice = self._invoice_with_membership_line(date(2026, 12, 31), 10.0)
        mline = self._membership_line_from_invoice(invoice)
        self.assertEqual(mline.date_to, date(2026, 12, 31))
        self.assertEqual(
            mline.date_from,
            date(2026, 1, 1),
            "Comportement standard : facture le dernier jour de la fenêtre produit "
            "ne remplace pas date_from par la date de facture (test d'inégalité stricte).",
        )
