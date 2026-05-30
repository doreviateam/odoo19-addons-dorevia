# -*- coding: utf-8 -*-
"""Recette indépendante RT-PAY — filtre « Payé uniquement » tableau détail."""

from datetime import date

from odoo.tests import tagged

from .test_coverage_cockpit_treasury import TestGlcCoverageCockpitTreasury


@tagged("post_install", "-at_install")
class TestGlcCoverageCockpitDetailPaidRecette(TestGlcCoverageCockpitTreasury):
    """Jeu RT-PAY-01 … RT-PAY-10 — données maîtrisées, rejeu serveur autonome."""

    # Montants figés recette (juin de l'année test)
    AMT_REV_PAID = 1100.0
    AMT_REV_UNPAID = 820.0
    AMT_EXP_PAID = 430.0
    AMT_EXP_UNPAID = 310.0
    AMT_RH_PAID = 520.0
    AMT_RH_UNPAID = 610.0
    AMT_BANK_NO_INV = 275.0
    AMT_VIR_INT = 9000.0

    def _recette_year(self):
        return self._next_test_year()

    def _recette_date(self, year, day=18):
        return date(year, 6, day)

    def _pay_invoice(self, invoice):
        wizard = (
            self.env["account.payment.register"]
            .with_context(active_model="account.move", active_ids=invoice.ids)
            .create({})
        )
        wizard.action_create_payments()

    def _create_payroll_vendor_bill(self, analytic_account, amount, invoice_date):
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
                            "name": "Paie recette RT-PAY",
                            "quantity": 1,
                            "price_unit": amount,
                            "account_id": payroll_account.id,
                            "analytic_distribution": {str(analytic_account.id): 100},
                            "tax_ids": [(6, 0, [])],
                        },
                    )
                ],
            }
        )
        invoice.action_post()
        return invoice

    def _create_bank_analytic_expense(
        self, analytic_account, amount, move_date, expense_code="622100"
    ):
        expense_account = self._get_or_create_expense_account(expense_code)
        amount = abs(amount)
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
                            "analytic_distribution": {str(analytic_account.id): 100},
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
        return move

    def _build_recette_cockpit(self):
        year = self._recette_year()
        move_date = self._recette_date(year)
        invoice_date = move_date.isoformat()

        rev_paid = self._create_revenue_on_account(
            self.bar, self.AMT_REV_PAID, invoice_date=invoice_date
        )
        self._pay_invoice(rev_paid)
        self._create_revenue_on_account(
            self.bar, self.AMT_REV_UNPAID, invoice_date=invoice_date
        )

        exp_paid = self._create_expense_on_account(
            self.structure, self.AMT_EXP_PAID, invoice_date=invoice_date
        )
        self._pay_invoice(exp_paid)
        self._create_expense_on_account(
            self.structure, self.AMT_EXP_UNPAID, invoice_date=invoice_date
        )

        rh_paid = self._create_payroll_vendor_bill(
            self.prestations, self.AMT_RH_PAID, invoice_date
        )
        self._pay_invoice(rh_paid)
        self._create_payroll_vendor_bill(
            self.prestations, self.AMT_RH_UNPAID, invoice_date
        )

        self._create_bank_analytic_expense(
            self.missions, self.AMT_BANK_NO_INV, move_date
        )

        transfer_account = self._get_or_create_transfer_account()
        vir_int = self._get_or_create_vir_int_account()
        self._create_internal_transfer_via_580(
            self.bank_journal,
            self.bank_account,
            transfer_account,
            vir_int,
            self.AMT_VIR_INT,
            move_date,
            outflow=False,
        )

        cockpit = self._create_treasury_cockpit(year)
        cockpit.action_refresh()
        return cockpit, year

    def _activity_line(self, cockpit, account, year, month=6):
        return cockpit.line_ids.filtered(
            lambda line: line.line_kind == "activity"
            and line.analytic_account_id == account
            and line.month_key == "%04d-%02d" % (year, month)
        )[:1]

    def _month_activity_lines(self, cockpit, year, month=6):
        key = "%04d-%02d" % (year, month)
        return cockpit.line_ids.filtered(
            lambda line: line.line_kind == "activity" and line.month_key == key
        )

    def _simulate_paid_view_totals(self, lines):
        """Reproduit applyPaidDisplayMode + agrégation sous-totaux widget."""
        totals = {
            "revenue_realized": 0.0,
            "payroll_realized": 0.0,
            "expense_realized": 0.0,
        }
        for line in lines:
            totals["revenue_realized"] += line.revenue_realized_paid or 0.0
            totals["payroll_realized"] += line.payroll_realized_paid or 0.0
            totals["expense_realized"] += line.expense_realized_paid or 0.0
        totals["performance_realized"] = (
            totals["revenue_realized"]
            - totals["payroll_realized"]
            - totals["expense_realized"]
        )
        return totals

    def _simulate_engaged_view_totals(self, lines):
        totals = {
            "revenue_realized": sum(lines.mapped("revenue_realized")),
            "payroll_realized": sum(lines.mapped("payroll_realized")),
            "expense_realized": sum(lines.mapped("expense_realized")),
        }
        totals["performance_realized"] = (
            totals["revenue_realized"]
            - totals["payroll_realized"]
            - totals["expense_realized"]
        )
        return totals

    def test_rt_pay_recette_complete(self):
        """RT-PAY-01 … RT-PAY-10 — jeu de recette indépendant."""
        cockpit, year = self._build_recette_cockpit()
        month_lines = self._month_activity_lines(cockpit, year)
        self.assertTrue(month_lines, "Aucune ligne détail sur la période recette.")

        bar = self._activity_line(cockpit, self.bar, year)
        structure = self._activity_line(cockpit, self.structure, year)
        prestations = self._activity_line(cockpit, self.prestations, year)
        missions = self._activity_line(cockpit, self.missions, year)
        vir_int = self._activity_line(cockpit, self._get_or_create_vir_int_account(), year)

        # RT-PAY-01 — vue complète (engagée)
        self.assertAlmostEqual(
            bar.revenue_realized, self.AMT_REV_PAID + self.AMT_REV_UNPAID
        )
        engaged = self._simulate_engaged_view_totals(month_lines)
        self.assertAlmostEqual(
            engaged["revenue_realized"],
            self.AMT_REV_PAID + self.AMT_REV_UNPAID + self.AMT_VIR_INT,
        )
        self.assertAlmostEqual(
            engaged["payroll_realized"], self.AMT_RH_PAID + self.AMT_RH_UNPAID
        )
        self.assertAlmostEqual(
            engaged["expense_realized"],
            self.AMT_EXP_PAID + self.AMT_EXP_UNPAID + self.AMT_BANK_NO_INV,
        )

        # RT-PAY-02 — vue payée uniquement
        paid = self._simulate_paid_view_totals(month_lines)
        self.assertAlmostEqual(
            paid["performance_realized"],
            paid["revenue_realized"]
            - paid["payroll_realized"]
            - paid["expense_realized"],
        )
        self.assertLess(paid["revenue_realized"], engaged["revenue_realized"])
        self.assertLess(paid["payroll_realized"], engaged["payroll_realized"])
        self.assertLess(paid["expense_realized"], engaged["expense_realized"])

        # RT-PAY-03 — ressource payée conservée
        self.assertAlmostEqual(bar.revenue_realized_paid, self.AMT_REV_PAID)

        # RT-PAY-04 — ressource non payée exclue
        self.assertAlmostEqual(
            bar.revenue_realized - bar.revenue_realized_paid, self.AMT_REV_UNPAID
        )

        # RT-PAY-05 — dépense payée conservée
        self.assertAlmostEqual(structure.expense_realized_paid, self.AMT_EXP_PAID)

        # RT-PAY-06 — dépense non payée exclue
        self.assertAlmostEqual(
            structure.expense_realized - structure.expense_realized_paid,
            self.AMT_EXP_UNPAID,
        )

        # RT-PAY-07 — RH payée conservée
        self.assertAlmostEqual(prestations.payroll_realized_paid, self.AMT_RH_PAID)

        # RT-PAY-08 — RH non payée exclue
        self.assertAlmostEqual(
            prestations.payroll_realized - prestations.payroll_realized_paid,
            self.AMT_RH_UNPAID,
        )
        self.assertNotAlmostEqual(
            prestations.payroll_realized, prestations.payroll_realized_paid
        )

        # RT-PAY-09 — écriture bancaire sans facture
        self.assertAlmostEqual(missions.expense_realized, self.AMT_BANK_NO_INV)
        self.assertAlmostEqual(missions.expense_realized_paid, self.AMT_BANK_NO_INV)

        # VIR_INT — ressource bancaire 580
        self.assertAlmostEqual(vir_int.revenue_realized, self.AMT_VIR_INT)
        self.assertAlmostEqual(vir_int.revenue_realized_paid, self.AMT_VIR_INT)

        # Sous-totaux / total période cohérents
        self.assertAlmostEqual(paid["revenue_realized"], self.AMT_REV_PAID + self.AMT_VIR_INT)
        self.assertAlmostEqual(paid["payroll_realized"], self.AMT_RH_PAID)
        self.assertAlmostEqual(
            paid["expense_realized"], self.AMT_EXP_PAID + self.AMT_BANK_NO_INV
        )
