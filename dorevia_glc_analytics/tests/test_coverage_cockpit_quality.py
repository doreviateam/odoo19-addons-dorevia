# -*- coding: utf-8 -*-

from odoo.fields import Command
from odoo.tests import tagged

from .test_coverage_cockpit_treasury import TestGlcCoverageCockpitTreasury


@tagged("post_install", "-at_install")
class TestGlcCoverageCockpitQuality(TestGlcCoverageCockpitTreasury):
    """GQ-6 — qualité comptable, analytique et suivi paiement."""

    def _exploitation_snapshot(self, cockpit):
        return {
            "activity_revenue_realized": cockpit.activity_revenue_realized,
            "payroll_realized": cockpit.payroll_realized,
            "general_expenses_realized": cockpit.general_expenses_realized,
            "resources_realized": cockpit.resources_realized,
            "balance_after_fixed": cockpit.balance_after_fixed,
        }

    def test_invariant_exploitation_kpis_unchanged_by_quality_refresh(self):
        """CA-INV-01 — agrégats exploitation identiques après refresh qualité/paiement."""
        year = self._next_test_year()
        invoice_date = "%s-06-15" % year
        self._create_revenue_on_account(self.bar, 5000.0, invoice_date=invoice_date)
        self._create_payroll_on_account(self.bar, 1200.0, invoice_date=invoice_date)
        self._create_expense_on_account(self.structure, 300.0, invoice_date=invoice_date)

        cockpit = self._create_cockpit(year=year)
        before = self._exploitation_snapshot(cockpit)
        cockpit.action_refresh()
        after = self._exploitation_snapshot(cockpit)

        self.assertEqual(before, after)
        self.assertGreater(cockpit.quality_analytic_moves_checked, 0)

    def test_q1_covered_move_increases_coverage_rate(self):
        """CA-Q1-01 — pièce avec analytique = couverte."""
        year = self._next_test_year()
        invoice_date = "%s-06-10" % year
        self._create_revenue_on_account(self.bar, 1000.0, invoice_date=invoice_date)
        cockpit = self._create_cockpit(year=year)
        cockpit.action_refresh()

        self.assertGreaterEqual(cockpit.quality_analytic_moves_checked, 1)
        self.assertGreaterEqual(cockpit.quality_analytic_moves_covered, 1)
        self.assertEqual(cockpit.quality_analytic_moves_uncovered, 0)
        self.assertAlmostEqual(cockpit.quality_analytic_coverage_rate, 100.0)

    def test_q1_uncovered_move_detected(self):
        """CA-Q1-03 — pièce sans analytique remontée comme non couverte."""
        year = self._next_test_year()
        invoice_date = "%s-06-12" % year
        invoice = self._create_invoice_one_line(
            price_unit=800.0,
            move_type="in_invoice",
            invoice_date=invoice_date,
            tax_ids=[Command.clear()],
            post=True,
        )
        product_line = invoice.invoice_line_ids.filtered(
            lambda move_line: move_line.display_type == "product"
        )[:1]
        product_line.write({"analytic_distribution": False})

        cockpit = self._create_cockpit(year=year)
        cockpit.action_refresh()

        self.assertGreaterEqual(cockpit.quality_analytic_moves_uncovered, 1)
        action = cockpit.action_open_quality_uncovered_moves()
        self.assertIn(invoice.id, action["domain"][0][2])

    def test_q2_unreconciled_customer_line_counted(self):
        """CA-Q2-02 — ligne client ouverte comptabilisée."""
        year = self._next_test_year()
        invoice_date = "%s-06-08" % year
        self._create_invoice_one_line(
            price_unit=450.0,
            move_type="out_invoice",
            invoice_date=invoice_date,
            tax_ids=[Command.clear()],
            post=True,
        )
        cockpit = self._create_cockpit(year=year)
        cockpit.action_refresh()

        self.assertGreater(cockpit.quality_unreconciled_count_customer, 0)
        self.assertGreater(cockpit.quality_unreconciled_amount_customer, 0.0)

    def test_q3_customer_not_paid_invoice(self):
        """CA-Q3-01 — facture client non payée."""
        year = self._next_test_year()
        invoice_date = "%s-06-20" % year
        self._create_invoice_one_line(
            price_unit=600.0,
            move_type="out_invoice",
            invoice_date=invoice_date,
            tax_ids=[Command.clear()],
            post=True,
        )
        cockpit = self._create_cockpit(year=year)
        cockpit.action_refresh()

        self.assertGreaterEqual(cockpit.payment_customer_not_paid_count, 1)
        self.assertGreater(cockpit.payment_customer_residual, 0.0)

    def test_q3_customer_paid_invoice_excluded_from_open_residual(self):
        """CA-Q3-04 — facture payée absente du reste à encaisser."""
        year = self._next_test_year()
        invoice_date = "%s-06-18" % year
        invoice = self._create_invoice_one_line(
            price_unit=750.0,
            move_type="out_invoice",
            invoice_date=invoice_date,
            tax_ids=[Command.clear()],
            post=True,
        )
        wizard = (
            self.env["account.payment.register"]
            .with_context(active_model="account.move", active_ids=invoice.ids)
            .create({})
        )
        wizard.action_create_payments()

        cockpit = self._create_cockpit(year=year)
        cockpit.action_refresh()

        self.assertGreaterEqual(cockpit.payment_customer_paid_count, 1)
        self.assertAlmostEqual(cockpit.payment_customer_residual, 0.0, places=2)

    def test_q3_supplier_invoice_tracking(self):
        """CA-Q3-05 — suivi factures fournisseurs."""
        year = self._next_test_year()
        invoice_date = "%s-06-14" % year
        self._create_expense_on_account(self.structure, 400.0, invoice_date=invoice_date)
        cockpit = self._create_cockpit(year=year)
        cockpit.action_refresh()

        self.assertGreaterEqual(cockpit.payment_supplier_invoice_count, 1)
        self.assertGreater(cockpit.payment_supplier_invoice_amount, 0.0)

    def test_quality_fields_do_not_alter_treasury(self):
        """CA-INV-02 — trésorerie Palier 5 non impactée par blocs qualité."""
        year = self._next_test_year()
        self._create_bank_move(
            self.bank_journal,
            self.bank_account,
            900.0,
            move_date="%s-06-05" % year,
            counterpart_account=self.suspense_account,
            inflow=True,
        )
        cockpit = self._create_cockpit(year=year)
        cockpit.write({"reference_bank_journal_id": self.bank_journal.id})
        cockpit.action_refresh()

        self.assertTrue(cockpit.treasury_has_data)
        self.assertAlmostEqual(cockpit.treasury_inflow, 900.0)
        self.assertGreater(cockpit.quality_analytic_moves_checked, 0)
