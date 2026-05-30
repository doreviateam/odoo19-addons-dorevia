# -*- coding: utf-8 -*-

from datetime import date

from odoo.tests import tagged

from .test_coverage_cockpit_treasury import TestGlcCoverageCockpitTreasury


@tagged("post_install", "-at_install")
class TestGlcCoverageCockpitDetailPaid(TestGlcCoverageCockpitTreasury):
    """Filtre tableau détail — vue payée uniquement."""

    def _detail_line(self, cockpit, account, month=6):
        year = cockpit.date_from.year
        return cockpit.line_ids.filtered(
            lambda line: line.analytic_account_id == account
            and line.month_key == "%04d-%02d" % (year, month)
        )

    def test_detail_paid_excludes_unpaid_customer_invoice(self):
        """DET-PAY-01 — facture client impayée : ressource payée = 0."""
        year = self._next_test_year()
        invoice_date = "%s-06-12" % year
        self._create_revenue_on_account(self.bar, 1200.0, invoice_date=invoice_date)
        cockpit = self._create_cockpit(year=year)
        cockpit.action_refresh()
        line = self._detail_line(cockpit, self.bar)
        self.assertEqual(len(line), 1)
        self.assertAlmostEqual(line.revenue_realized, 1200.0)
        self.assertAlmostEqual(line.revenue_realized_paid, 0.0)

    def test_detail_paid_includes_paid_customer_invoice(self):
        """DET-PAY-02 — facture client payée : ressource payée = ressource engagée."""
        year = self._next_test_year()
        invoice_date = "%s-06-14" % year
        invoice = self._create_revenue_on_account(
            self.bar, 850.0, invoice_date=invoice_date
        )
        wizard = (
            self.env["account.payment.register"]
            .with_context(active_model="account.move", active_ids=invoice.ids)
            .create({})
        )
        wizard.action_create_payments()
        cockpit = self._create_cockpit(year=year)
        cockpit.action_refresh()
        line = self._detail_line(cockpit, self.bar)
        self.assertEqual(len(line), 1)
        self.assertAlmostEqual(line.revenue_realized, 850.0)
        self.assertAlmostEqual(line.revenue_realized_paid, 850.0)

    def test_detail_paid_internal_transfer_always_included(self):
        """DET-PAY-03 — virement interne 580 + VIR_INT : toujours en vue payée."""
        year = self._next_test_year()
        move_date = date(year, 6, 16)
        transfer_account = self._get_or_create_transfer_account()
        vir_int = self._get_or_create_vir_int_account()
        self._create_internal_transfer_via_580(
            self.bank_journal,
            self.bank_account,
            transfer_account,
            vir_int,
            9000.0,
            move_date,
            outflow=False,
        )
        cockpit = self._create_treasury_cockpit(year)
        cockpit.action_refresh()
        line = self._detail_line(cockpit, vir_int)
        self.assertEqual(len(line), 1)
        self.assertAlmostEqual(line.revenue_realized, 9000.0)
        self.assertAlmostEqual(line.revenue_realized_paid, 9000.0)
