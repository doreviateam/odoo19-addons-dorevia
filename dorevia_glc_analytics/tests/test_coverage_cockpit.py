# -*- coding: utf-8 -*-

import itertools

from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.fields import Command
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGlcCoverageCockpit(AccountTestInvoicingCommon):
    """Palier 4 — cockpit couverture des salaires GLC."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.ref("base.user_admin").group_ids += cls.env.ref(
            "dorevia_glc_analytics.group_glc_manager"
        )
        cls.env = cls.env(user=cls.env.ref("base.user_admin"))

        plan_ids = [
            cls.env.ref("dorevia_glc_analytics.analytic_plan_glc_activites").id,
            cls.env.ref("dorevia_glc_analytics.analytic_plan_glc_financements").id,
        ]
        cls.env["account.analytic.account"].sudo().search(
            [("plan_id", "in", plan_ids)]
        ).write({"company_id": cls.env.company.id})

        cls.bar = cls.env.ref("dorevia_glc_analytics.analytic_account_glc_bar")
        cls.prestations = cls.env.ref("dorevia_glc_analytics.analytic_account_glc_prestations")
        cls.privatisations = cls.env.ref("dorevia_glc_analytics.analytic_account_glc_privatisations")
        cls.structure = cls.env.ref("dorevia_glc_analytics.analytic_account_glc_structure")
        cls.subventions = cls.env.ref("dorevia_glc_analytics.analytic_account_glc_subventions")
        existing_years = cls.env["glc.budget"].search([]).mapped("year")
        cls.test_year = max(y for y in existing_years + [2050] if y < 2100) + 1
        cls.period = "%s-06-01" % cls.test_year
        cls.invoice_date = "%s-06-15" % cls.test_year
        cls.employee = cls.env["hr.employee"].create(
            {
                "name": "Salarié cockpit GLC",
                "company_id": cls.env.company.id,
            }
        )
        existing_years = cls.env["glc.budget"].search([]).mapped("year")
        cls._year_counter = itertools.count(max(existing_years + [cls.test_year]) + 1)

    def _next_test_year(self):
        year = next(self._year_counter)
        if year >= 2100:
            year = self.test_year
        return year

    def _create_cockpit(self, year=None, month="6"):
        year = year or self.test_year
        return self.env["glc.coverage.cockpit"].create(
            {
                "company_id": self.env.company.id,
                "year": year,
                "month": month,
                "budget_scenario": "initial",
            }
        )

    def _create_validated_budget(self, year, lines):
        budget = self.env["glc.budget"].create(
            {
                "name": "Budget cockpit %s" % year,
                "year": year,
                "scenario": "initial",
                "company_id": self.env.company.id,
            }
        )
        for line_vals in lines:
            self.env["glc.budget.line"].create(
                {"budget_id": budget.id, **line_vals},
            )
        budget.action_validate()
        return budget

    def _create_revenue_on_account(self, account, amount, invoice_date=None):
        invoice_date = invoice_date or self.invoice_date
        invoice = self._create_invoice_one_line(
            price_unit=amount,
            move_type="out_invoice",
            invoice_date=invoice_date,
            tax_ids=[Command.clear()],
            post=False,
        )
        line = invoice.invoice_line_ids.filtered(
            lambda move_line: move_line.display_type == "product"
        )[:1]
        line.write({"analytic_distribution": {str(account.id): 100}})
        invoice.action_post()
        return invoice

    def _create_expense_on_account(self, account, amount, invoice_date=None):
        invoice_date = invoice_date or self.invoice_date
        invoice = self._create_invoice_one_line(
            price_unit=amount,
            move_type="in_invoice",
            invoice_date=invoice_date,
            tax_ids=[Command.clear()],
            post=False,
        )
        line = invoice.invoice_line_ids.filtered(
            lambda move_line: move_line.display_type == "product"
        )[:1]
        line.write({"analytic_distribution": {str(account.id): 100}})
        invoice.action_post()
        return invoice

    def _create_validated_allocation(self, amount=3000.0, bar_percent=100.0, employee=None):
        employee = employee or self.employee
        cost_line = self.env["glc.employee.cost.line"].create(
            {
                "company_id": self.env.company.id,
                "employee_id": employee.id,
                "period_date": self.period,
                "cost_amount": amount,
                "reference_hours": 151.67,
            }
        )
        allocation = self.env["glc.salary.allocation"].create(
            {
                "company_id": self.env.company.id,
                "employee_id": employee.id,
                "period_date": self.period,
                "employee_cost_line_id": cost_line.id,
                "method": "percent",
            }
        )
        self.env["glc.salary.allocation.line"].create(
            {
                "allocation_id": allocation.id,
                "activity_account_id": self.bar.id,
                "percent": bar_percent,
            }
        )
        allocation.action_validate()
        return allocation

    def test_menu_cockpit_exists(self):
        """CA1 — menu Cockpit couverture des salaires."""
        menu = self.env.ref("dorevia_glc_analytics.menu_glc_coverage_cockpit")
        action = self.env.ref("dorevia_glc_analytics.action_glc_coverage_cockpit")
        self.assertEqual(menu.action.id, action.id)

    def test_alert_green_when_resources_cover_fixed_charges(self):
        """CA6 — alerte verte si ressources ≥ salaires + frais généraux."""
        year = self.test_year
        self._create_validated_budget(
            year,
            [
                {
                    "period_date": self.period,
                    "line_type": "revenue",
                    "analytic_account_id": self.bar.id,
                    "amount": 10000.0,
                },
            ],
        )
        self._create_revenue_on_account(self.bar, 12000.0)
        self._create_revenue_on_account(self.subventions, 2000.0)
        self._create_validated_allocation(amount=3000.0)
        self._create_expense_on_account(self.structure, 1500.0)

        cockpit = self._create_cockpit(year=year)
        cockpit.action_refresh()

        self.assertEqual(cockpit.alert_status, "green")
        self.assertGreaterEqual(cockpit.resources_realized, cockpit.payroll_realized)
        self.assertGreaterEqual(
            cockpit.resources_realized,
            cockpit.payroll_realized + cockpit.general_expenses_realized,
        )

    def test_alert_red_when_resources_below_payroll(self):
        """CA6 — alerte rouge si ressources < masse salariale."""
        year = self.test_year
        self._create_revenue_on_account(self.bar, 1000.0)
        self._create_validated_allocation(amount=5000.0)

        cockpit = self._create_cockpit(year=year)
        cockpit.action_refresh()

        self.assertEqual(cockpit.alert_status, "red")
        self.assertLess(cockpit.resources_realized, cockpit.payroll_realized)

    def test_alert_orange_when_resources_cover_payroll_only(self):
        """CA6 — alerte orange si ressources ≥ salaires mais < salaires + frais généraux."""
        year = self.test_year
        self._create_revenue_on_account(self.bar, 6500.0)
        self._create_validated_allocation(amount=3000.0)
        self._create_expense_on_account(self.structure, 4000.0)

        cockpit = self._create_cockpit(year=year)
        cockpit.action_refresh()

        self.assertEqual(cockpit.alert_status, "orange")
        self.assertGreaterEqual(cockpit.resources_realized, cockpit.payroll_realized)
        self.assertLess(
            cockpit.resources_realized,
            cockpit.payroll_realized + cockpit.general_expenses_realized,
        )

    def test_payroll_from_validated_allocation_only(self):
        """CA3 — masse salariale lue depuis ventilations validées uniquement."""
        year = self.test_year
        draft_employee = self.env["hr.employee"].create(
            {"name": "Salarié brouillon cockpit", "company_id": self.env.company.id}
        )
        draft_allocation = self.env["glc.salary.allocation"].create(
            {
                "company_id": self.env.company.id,
                "employee_id": draft_employee.id,
                "period_date": self.period,
                "employee_cost_line_id": self.env["glc.employee.cost.line"].create(
                    {
                        "company_id": self.env.company.id,
                        "employee_id": draft_employee.id,
                        "period_date": self.period,
                        "cost_amount": 9000.0,
                        "reference_hours": 151.67,
                    }
                ).id,
                "method": "percent",
            }
        )
        self.env["glc.salary.allocation.line"].create(
            {
                "allocation_id": draft_allocation.id,
                "activity_account_id": self.bar.id,
                "percent": 100.0,
            }
        )
        self._create_validated_allocation(amount=2500.0)

        cockpit = self._create_cockpit(year=year)
        cockpit.action_refresh()

        self.assertAlmostEqual(cockpit.payroll_realized, 2500.0)

    def test_budget_aggregation_from_glc_budget_line(self):
        """CA1 — prévisionnel lu depuis glc.budget.line validé."""
        year = self._next_test_year()
        period = "%s-06-01" % year
        self._create_validated_budget(
            year,
            [
                {
                    "period_date": period,
                    "line_type": "revenue",
                    "analytic_account_id": self.bar.id,
                    "amount": 5000.0,
                },
                {
                    "period_date": period,
                    "line_type": "funding",
                    "analytic_account_id": self.subventions.id,
                    "amount": 1500.0,
                },
                {
                    "period_date": period,
                    "line_type": "expense",
                    "analytic_account_id": self.structure.id,
                    "amount": 800.0,
                },
            ],
        )

        cockpit = self._create_cockpit(year=year)
        cockpit.action_refresh()

        self.assertAlmostEqual(cockpit.activity_revenue_budget, 5000.0)
        self.assertAlmostEqual(cockpit.funding_budget, 1500.0)
        self.assertAlmostEqual(cockpit.resources_budget, 6500.0)
        self.assertAlmostEqual(cockpit.general_expenses_budget, 800.0)

    def test_detail_lines_activity_by_month(self):
        """CA — détail Activité × Mois."""
        year = self.test_year
        self._create_revenue_on_account(self.bar, 4000.0)
        self._create_validated_allocation(amount=2000.0)

        cockpit = self._create_cockpit(year=year)
        cockpit.action_refresh()

        bar_lines = cockpit.line_ids.filtered(
            lambda line: line.analytic_account_id == self.bar
        )
        self.assertTrue(bar_lines)
        self.assertAlmostEqual(sum(bar_lines.mapped("revenue_realized")), 4000.0)
        self.assertAlmostEqual(sum(bar_lines.mapped("payroll_realized")), 2000.0)
