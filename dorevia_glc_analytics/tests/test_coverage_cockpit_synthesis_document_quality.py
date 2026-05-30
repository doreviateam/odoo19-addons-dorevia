# -*- coding: utf-8 -*-

from datetime import date

from odoo.tests import tagged

from .test_coverage_cockpit_treasury import TestGlcCoverageCockpitTreasury


@tagged("post_install", "-at_install")
class TestGlcCoverageCockpitSynthesisDocumentQuality(TestGlcCoverageCockpitTreasury):
    """KPI Synthèse — qualité documentaire (RT-DOC / DOC)."""

    def _cockpit_june(self, year):
        cockpit = self._create_cockpit(
            date_from=date(year, 6, 1),
            date_to=date(year, 6, 30),
        )
        cockpit.action_refresh()
        return cockpit

    def test_doc_01_revenue_invoiced_rate_full_when_only_customer_invoices(self):
        """DOC-01 — factures client seules : ressources facturées = 100 %."""
        year = self._next_test_year()
        invoice_date = "%s-06-12" % year
        self._create_revenue_on_account(self.bar, 500.0, invoice_date=invoice_date)
        self._create_revenue_on_account(self.bar, 300.0, invoice_date=invoice_date)
        cockpit = self._cockpit_june(year)
        self.assertEqual(cockpit.revenue_eligible_line_count, 2)
        self.assertEqual(cockpit.revenue_invoiced_line_count, 2)
        self.assertEqual(cockpit.revenue_eligible_amount, 2)
        self.assertEqual(cockpit.revenue_invoiced_amount, 2)
        self.assertAlmostEqual(cockpit.revenue_invoiced_rate, 100.0)

    def test_doc_02_revenue_invoiced_rate_zero_when_only_bank_entries(self):
        """DOC-02 / RT-DOC-07 — banque sans facture : 0 % ressources facturées."""
        year = self._next_test_year()
        move_date = date(year, 6, 14)
        income = self._get_or_create_income_account("741100")
        amount = 450.0
        move = self.env["account.move"].create(
            {
                "move_type": "entry",
                "date": move_date,
                "journal_id": self.bank_journal.id,
                "company_id": self.env.company.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": income.id,
                            "debit": 0.0,
                            "credit": amount,
                            "analytic_distribution": {str(self.bar.id): 100},
                        },
                    ),
                    (
                        0,
                        0,
                        {"account_id": self.bank_account.id, "debit": amount, "credit": 0.0},
                    ),
                ],
            }
        )
        move.action_post()
        cockpit = self._cockpit_june(year)
        self.assertEqual(cockpit.revenue_eligible_line_count, 1)
        self.assertEqual(cockpit.revenue_invoiced_line_count, 0)
        self.assertAlmostEqual(cockpit.revenue_invoiced_rate, 0.0)

    def test_doc_03_revenue_invoiced_rate_mixed_invoice_and_bank_by_line_count(self):
        """DOC-03 — mix facture + banque : taux = lignes facturées / lignes éligibles."""
        year = self._next_test_year()
        invoice_date = "%s-06-15" % year
        self._create_revenue_on_account(self.bar, 600.0, invoice_date=invoice_date)
        move_date = date(year, 6, 16)
        income = self._get_or_create_income_account("741100")
        bank_amount = 400.0
        move = self.env["account.move"].create(
            {
                "move_type": "entry",
                "date": move_date,
                "journal_id": self.bank_journal.id,
                "company_id": self.env.company.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": income.id,
                            "debit": 0.0,
                            "credit": bank_amount,
                            "analytic_distribution": {str(self.bar.id): 100},
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "account_id": self.bank_account.id,
                            "debit": bank_amount,
                            "credit": 0.0,
                        },
                    ),
                ],
            }
        )
        move.action_post()
        cockpit = self._cockpit_june(year)
        self.assertEqual(cockpit.revenue_eligible_line_count, 2)
        self.assertEqual(cockpit.revenue_invoiced_line_count, 1)
        self.assertAlmostEqual(cockpit.revenue_invoiced_rate, 50.0)

    def test_doc_03b_large_bank_line_does_not_dominate_rate(self):
        """RT-DOC — montant banque élevé : le taux reste basé sur le nombre de lignes."""
        year = self._next_test_year()
        invoice_date = "%s-06-15" % year
        self._create_revenue_on_account(self.bar, 100.0, invoice_date=invoice_date)
        move_date = date(year, 6, 16)
        income = self._get_or_create_income_account("741100")
        move = self.env["account.move"].create(
            {
                "move_type": "entry",
                "date": move_date,
                "journal_id": self.bank_journal.id,
                "company_id": self.env.company.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": income.id,
                            "debit": 0.0,
                            "credit": 50000.0,
                            "analytic_distribution": {str(self.bar.id): 100},
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "account_id": self.bank_account.id,
                            "debit": 50000.0,
                            "credit": 0.0,
                        },
                    ),
                ],
            }
        )
        move.action_post()
        cockpit = self._cockpit_june(year)
        self.assertEqual(cockpit.revenue_eligible_line_count, 2)
        self.assertEqual(cockpit.revenue_invoiced_line_count, 1)
        self.assertAlmostEqual(cockpit.revenue_invoiced_rate, 50.0)

    def test_doc_03c_multi_line_invoice_counts_each_eligible_line(self):
        """RT-DOC — facture multi-lignes : chaque ligne éligible compte au dénominateur."""
        year = self._next_test_year()
        invoice_date = "%s-06-15" % year
        income = self._get_or_create_income_account("741100")
        invoice = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.partner_a.id,
                "invoice_date": invoice_date,
                "date": invoice_date,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Ligne 1",
                            "quantity": 1,
                            "price_unit": 200.0,
                            "account_id": income.id,
                            "analytic_distribution": {str(self.bar.id): 100},
                            "tax_ids": [(6, 0, [])],
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "Ligne 2",
                            "quantity": 1,
                            "price_unit": 300.0,
                            "account_id": income.id,
                            "analytic_distribution": {str(self.bar.id): 100},
                            "tax_ids": [(6, 0, [])],
                        },
                    ),
                ],
            }
        )
        invoice.action_post()
        cockpit = self._cockpit_june(year)
        self.assertEqual(cockpit.revenue_eligible_line_count, 2)
        self.assertEqual(cockpit.revenue_invoiced_line_count, 2)
        self.assertAlmostEqual(cockpit.revenue_invoiced_rate, 100.0)

    def test_doc_04_expense_invoiced_rate_full_when_only_supplier_invoices(self):
        """DOC-04 / RT-DOC-05 — factures fournisseur seules : 100 %."""
        year = self._next_test_year()
        invoice_date = "%s-06-17" % year
        self._create_expense_on_account(self.structure, 250.0, invoice_date=invoice_date)
        self._create_expense_on_account(self.structure, 150.0, invoice_date=invoice_date)
        cockpit = self._cockpit_june(year)
        self.assertEqual(cockpit.expense_eligible_line_count, 2)
        self.assertEqual(cockpit.expense_invoiced_line_count, 2)
        self.assertAlmostEqual(cockpit.expense_invoiced_rate, 100.0)

    def test_doc_05_bank_expense_not_invoiced_numerator(self):
        """DOC-05 / RT-DOC-06-08 — dépense banque sans facture : dénominateur seulement."""
        year = self._next_test_year()
        move_date = date(year, 6, 18)
        expense_account = self._get_or_create_expense_account("622100")
        amount = 275.0
        move = self.env["account.move"].create(
            {
                "move_type": "entry",
                "date": move_date,
                "journal_id": self.bank_journal.id,
                "company_id": self.env.company.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": expense_account.id,
                            "debit": amount,
                            "credit": 0.0,
                            "analytic_distribution": {str(self.missions.id): 100},
                        },
                    ),
                    (
                        0,
                        0,
                        {"account_id": self.bank_account.id, "debit": 0.0, "credit": amount},
                    ),
                ],
            }
        )
        move.action_post()
        cockpit = self._cockpit_june(year)
        self.assertEqual(cockpit.expense_eligible_line_count, 1)
        self.assertEqual(cockpit.expense_invoiced_line_count, 0)
        self.assertAlmostEqual(cockpit.expense_invoiced_rate, 0.0)

    def test_doc_05b_internal_transfer_counts_in_denominator_only(self):
        """DOC-05 / RT-DOC-08 — virement interne 580 : dénominateur ressource, pas numérateur."""
        year = self._next_test_year()
        move_date = date(year, 6, 11)
        self._create_revenue_on_account(self.bar, 1000.0, invoice_date="%s-06-10" % year)
        transfer_account = self._get_or_create_transfer_account()
        self._create_internal_transfer_via_580(
            self.bank_journal,
            self.bank_account,
            transfer_account,
            self.bar,
            9000.0,
            move_date,
            outflow=False,
        )
        cockpit = self._create_treasury_cockpit(year)
        cockpit.action_refresh()
        self.assertEqual(cockpit.revenue_invoiced_line_count, 1)
        self.assertEqual(cockpit.revenue_eligible_line_count, 2)
        self.assertAlmostEqual(cockpit.revenue_invoiced_rate, 50.0)

    def test_doc_06_zero_eligible_amounts_when_no_data(self):
        """DOC-06 / RT-DOC-09 — dénominateur nul : compteurs et taux à 0."""
        year = self._next_test_year()
        cockpit = self._cockpit_june(year)
        self.assertEqual(cockpit.revenue_eligible_line_count, 0)
        self.assertAlmostEqual(cockpit.revenue_invoiced_rate, 0.0)
        self.assertEqual(cockpit.expense_eligible_line_count, 0)
        self.assertAlmostEqual(cockpit.expense_invoiced_rate, 0.0)

    def test_doc_inv_01_document_quality_does_not_change_exploitation_kpis(self):
        """DOC-INV-01 / RT-DOC-10 — KPI exploitation inchangés."""
        year = self._next_test_year()
        invoice_date = "%s-06-20" % year
        self._create_revenue_on_account(self.bar, 1200.0, invoice_date=invoice_date)
        self._create_expense_on_account(self.structure, 350.0, invoice_date=invoice_date)
        self._create_payroll_on_account(
            self.prestations, 180.0, invoice_date=invoice_date
        )
        cockpit = self._cockpit_june(year)
        expected = {
            "activity_revenue_realized": cockpit.activity_revenue_realized,
            "resources_realized": cockpit.resources_realized,
            "payroll_realized": cockpit.payroll_realized,
            "general_expenses_realized": cockpit.general_expenses_realized,
            "salary_coverage_rate": cockpit.salary_coverage_rate,
        }
        cockpit.action_refresh()
        self.assertAlmostEqual(
            cockpit.activity_revenue_realized, expected["activity_revenue_realized"]
        )
        self.assertAlmostEqual(cockpit.resources_realized, expected["resources_realized"])
        self.assertAlmostEqual(cockpit.payroll_realized, expected["payroll_realized"])
        self.assertAlmostEqual(
            cockpit.general_expenses_realized, expected["general_expenses_realized"]
        )
        self.assertAlmostEqual(
            cockpit.salary_coverage_rate, expected["salary_coverage_rate"]
        )
        self.assertGreater(cockpit.revenue_invoiced_line_count, 0)

    def test_rt_doc_payroll_excluded_from_expense_invoiced_rate(self):
        """RT-DOC — Cumul RH hors périmètre : facture 645 n'impacte pas dépenses facturées."""
        year = self._next_test_year()
        invoice_date = "%s-06-21" % year
        payroll_account = self._get_or_create_payroll_account("645200")
        invoice = self.env["account.move"].create(
            {
                "move_type": "in_invoice",
                "partner_id": self.partner_a.id,
                "invoice_date": invoice_date,
                "date": invoice_date,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Paie test DOC",
                            "quantity": 1,
                            "price_unit": 520.0,
                            "account_id": payroll_account.id,
                            "analytic_distribution": {str(self.prestations.id): 100},
                            "tax_ids": [(6, 0, [])],
                        },
                    )
                ],
            }
        )
        invoice.action_post()
        cockpit = self._cockpit_june(year)
        self.assertAlmostEqual(cockpit.payroll_realized, 520.0)
        self.assertEqual(cockpit.expense_eligible_line_count, 0)
        self.assertEqual(cockpit.expense_invoiced_line_count, 0)

    def test_doc_07_supplier_receipt_in_receipt_counts_as_invoiced(self):
        """DOC-07 — reçu fournisseur Odoo (in_receipt) compte au numérateur."""
        year = self._next_test_year()
        invoice_date = "%s-06-22" % year
        expense_account = self._get_or_create_expense_account("622100")
        receipt = self.env["account.move"].create(
            {
                "move_type": "in_receipt",
                "partner_id": self.partner_a.id,
                "invoice_date": invoice_date,
                "date": invoice_date,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Ticket fournisseur test",
                            "quantity": 1,
                            "price_unit": 42.0,
                            "account_id": expense_account.id,
                            "analytic_distribution": {str(self.missions.id): 100},
                            "tax_ids": [(6, 0, [])],
                        },
                    )
                ],
            }
        )
        receipt.action_post()
        cockpit = self._cockpit_june(year)
        self.assertEqual(cockpit.expense_eligible_line_count, 1)
        self.assertEqual(cockpit.expense_invoiced_line_count, 1)
        self.assertAlmostEqual(cockpit.expense_invoiced_rate, 100.0)
