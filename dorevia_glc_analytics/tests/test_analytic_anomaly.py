# -*- coding: utf-8 -*-

from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.fields import Command
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGlcAnalyticAnomaly(AccountTestInvoicingCommon):
    """Palier 1 — assistant anomalies analytiques GLC."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        manager_group = cls.env.ref("dorevia_glc_analytics.group_glc_manager")
        cls.env.ref("base.user_admin").group_ids += manager_group
        cls.env = cls.env(user=cls.env.ref("base.user_admin"))

        plan = cls.env.ref("dorevia_glc_analytics.analytic_plan_glc_activites")
        cls.env["account.analytic.account"].sudo().search(
            [("plan_id", "=", plan.id)]
        ).write({"company_id": cls.env.company.id})

        cls.bar = cls.env.ref("dorevia_glc_analytics.analytic_account_glc_bar")
        cls.ressources = cls.env.ref(
            "dorevia_glc_analytics.analytic_account_glc_ressources_propres"
        )
        cls.structure = cls.env.ref("dorevia_glc_analytics.analytic_account_glc_structure")
        cls.adhesions = cls.env.ref("dorevia_glc_analytics.analytic_account_glc_adhesions")

        cls.income_account = cls.company_data["default_account_revenue"]
        cls.expense_account = cls.company_data["default_account_expense"]

    def _distribution(self, *accounts):
        return {str(account.id): 100.0 for account in accounts}

    def _run_wizard(self, date_from="2026-05-01", date_to="2026-05-31"):
        wizard = self.env["glc.analytic.anomaly.wizard"].create(
            {
                "company_id": self.env.company.id,
                "date_from": date_from,
                "date_to": date_to,
                "include_posted": True,
            }
        )
        wizard.action_analyze()
        return wizard

    def _product_line(self, move):
        return move.invoice_line_ids.filtered(
            lambda line: line.display_type == "product"
        )[:1]

    def test_menu_anomaly_wizard_exists(self):
        """CA1 — menu Anomalies analytiques pour Gestionnaire GLC."""
        menu = self.env.ref("dorevia_glc_analytics.menu_glc_analytic_anomalies")
        action = self.env.ref("dorevia_glc_analytics.action_glc_analytic_anomaly_wizard")
        self.assertEqual(menu.action.id, action.id)
        self.assertIn(
            self.env.ref("dorevia_glc_analytics.group_glc_manager"),
            menu.group_ids,
        )

    def test_a1_vendor_without_activity(self):
        """CA2 — facture fournisseur sans activité → A1."""
        bill = self._create_invoice_one_line(
            price_unit=120.0,
            move_type="in_invoice",
            invoice_date="2026-05-10",
            tax_ids=[Command.clear()],
            post=True,
        )
        line = self._product_line(bill)
        line.analytic_distribution = False

        wizard = self._run_wizard()
        a1_lines = wizard.line_ids.filtered(
            lambda anomaly: anomaly.anomaly_type == "a1_vendor_no_activity"
        )
        self.assertTrue(a1_lines)
        self.assertIn(bill, a1_lines.move_id)

    def test_a2_revenue_incomplete(self):
        """CA3 — facture client sans double axe → A2."""
        invoice = self._create_invoice_one_line(
            price_unit=200.0,
            move_type="out_invoice",
            invoice_date="2026-05-11",
            tax_ids=[Command.clear()],
            post=True,
        )
        self._product_line(invoice).analytic_distribution = False

        wizard = self._run_wizard()
        a2_lines = wizard.line_ids.filtered(
            lambda anomaly: anomaly.anomaly_type.startswith("a2_revenue")
        )
        self.assertTrue(a2_lines)

    def test_a2_ok_bar_and_ressources_propres(self):
        """CA4 — BAR + RESSOURCES_PROPRES → pas d'anomalie A2."""
        invoice = self._create_invoice_one_line(
            price_unit=150.0,
            move_type="out_invoice",
            invoice_date="2026-05-12",
            tax_ids=[Command.clear()],
            post=True,
        )
        self._product_line(invoice).analytic_distribution = self._distribution(
            self.bar, self.ressources
        )

        wizard = self._run_wizard()
        a2_lines = wizard.line_ids.filtered(
            lambda anomaly: anomaly.anomaly_type.startswith("a2_revenue")
            and anomaly.move_id == invoice
        )
        self.assertFalse(a2_lines)

    def test_a4_payroll_with_analytic(self):
        """CA5 — écriture paie avec analytique → A4."""
        payroll_account = self.env["account.account"].search(
            [
                ("company_ids", "in", self.env.company.id),
                ("code", "=like", "641%"),
            ],
            limit=1,
        )
        if not payroll_account:
            payroll_account = self.env["account.account"].create(
                {
                    "name": "Salaires test GLC",
                    "code": "641100",
                    "account_type": "expense",
                }
            )

        bill = self._create_invoice_one_line(
            price_unit=1000.0,
            move_type="in_invoice",
            invoice_date="2026-05-13",
            tax_ids=[Command.clear()],
            post=False,
        )
        line = self._product_line(bill)
        line.write(
            {
                "account_id": payroll_account.id,
                "analytic_distribution": self._distribution(self.structure),
            }
        )
        bill.action_post()

        wizard = self._run_wizard()
        a4_lines = wizard.line_ids.filtered(
            lambda anomaly: anomaly.anomaly_type == "a4_payroll_analytic"
        )
        self.assertTrue(a4_lines)

    def test_a5_legacy_account_after_cutover(self):
        """CA6 — ancien compte après bascule → A5."""
        icp = self.env["ir.config_parameter"].sudo()
        icp.set_param("dorevia_glc_analytics.cutover_date", "2026-01-01")

        legacy_plan = self.env.ref("dorevia_glc_analytics.analytic_plan_glc_activites")
        legacy_account = self.env["account.analytic.account"].create(
            {
                "name": "Legacy BAR",
                "code": "BAR_RESTAU",
                "plan_id": legacy_plan.id,
            }
        )

        invoice = self._create_invoice_one_line(
            price_unit=80.0,
            move_type="out_invoice",
            invoice_date="2026-05-14",
            tax_ids=[Command.clear()],
            post=True,
        )
        self._product_line(invoice).analytic_distribution = self._distribution(legacy_account)

        wizard = self._run_wizard()
        a5_lines = wizard.line_ids.filtered(
            lambda anomaly: anomaly.anomaly_type == "a5_legacy_account"
        )
        self.assertTrue(a5_lines)
        self.assertTrue(wizard.a5_enabled)

    def test_a3_inactive_without_mapping(self):
        """A3 désactivé sans mapping explicite."""
        wizard = self._run_wizard()
        self.assertFalse(wizard.a3_enabled)
        self.assertTrue(wizard.a3_info_message)
        self.assertFalse(
            wizard.line_ids.filtered(
                lambda anomaly: anomaly.anomaly_type == "a3_funding_missing"
            )
        )

    def test_a3_with_explicit_mapping(self):
        """A3 actif uniquement avec glc.account.funding.rule."""
        invoice = self._create_invoice_one_line(
            price_unit=50.0,
            move_type="out_invoice",
            invoice_date="2026-05-15",
            tax_ids=[Command.clear()],
            post=False,
        )
        line = self._product_line(invoice)
        self.env["glc.account.funding.rule"].create(
            {
                "company_id": self.env.company.id,
                "account_id": line.account_id.id,
                "funding_code": "ADHESIONS",
            }
        )
        line.analytic_distribution = False
        invoice.action_post()

        wizard = self._run_wizard()
        self.assertTrue(wizard.a3_enabled)
        a3_lines = wizard.line_ids.filtered(
            lambda anomaly: anomaly.anomaly_type == "a3_funding_missing"
        )
        self.assertTrue(a3_lines)
        a2_lines = wizard.line_ids.filtered(
            lambda anomaly: anomaly.anomaly_type.startswith("a2_revenue")
            and anomaly.move_id == invoice
        )
        self.assertFalse(a2_lines)

    def test_non_blocking_invoice_validation(self):
        """CA7 — validation facture toujours possible."""
        bill = self._create_invoice_one_line(
            price_unit=90.0,
            move_type="in_invoice",
            invoice_date="2026-05-16",
            tax_ids=[Command.clear()],
            post=False,
        )
        self._product_line(bill).analytic_distribution = False
        bill.action_post()
        self.assertEqual(bill.state, "posted")

    def test_a6_structure_summary_not_line_anomaly(self):
        """A6 — synthèse wizard, pas de ligne d'anomalie dédiée."""
        bill = self._create_invoice_one_line(
            price_unit=300.0,
            move_type="in_invoice",
            invoice_date="2026-05-17",
            tax_ids=[Command.clear()],
            post=True,
        )
        self._product_line(bill).analytic_distribution = self._distribution(self.structure)

        wizard = self._run_wizard()
        self.assertGreater(wizard.structure_weight_pct, 0.0)
        self.assertFalse(
            wizard.line_ids.filtered(
                lambda anomaly: "structure" in (anomaly.anomaly_type or "")
            )
        )
