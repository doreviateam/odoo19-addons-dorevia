# -*- coding: utf-8 -*-

from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.exceptions import UserError, ValidationError
from odoo.fields import Command
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGlcSalaryAllocation(AccountTestInvoicingCommon):
    """Palier 2 — ventilation salariale GLC."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.ref("base.user_admin").group_ids += cls.env.ref(
            "dorevia_glc_analytics.group_glc_manager"
        )
        cls.env = cls.env(user=cls.env.ref("base.user_admin"))

        plan = cls.env.ref("dorevia_glc_analytics.analytic_plan_glc_activites")
        cls.env["account.analytic.account"].sudo().search(
            [("plan_id", "=", plan.id)]
        ).write({"company_id": cls.env.company.id})

        cls.employee = cls.env["hr.employee"].create(
            {
                "name": "Salarié GLC Test",
                "company_id": cls.env.company.id,
            }
        )
        cls.bar = cls.env.ref("dorevia_glc_analytics.analytic_account_glc_bar")
        cls.structure = cls.env.ref("dorevia_glc_analytics.analytic_account_glc_structure")
        cls.prestations = cls.env.ref("dorevia_glc_analytics.analytic_account_glc_prestations")
        cls.adhesions = cls.env.ref("dorevia_glc_analytics.analytic_account_glc_adhesions")
        cls.period = "2026-06-01"

    def _create_cost_line(self, cost_amount=3000.0, reference_hours=151.67):
        return self.env["glc.employee.cost.line"].create(
            {
                "company_id": self.env.company.id,
                "employee_id": self.employee.id,
                "period_date": self.period,
                "cost_amount": cost_amount,
                "reference_hours": reference_hours,
            }
        )

    def _create_allocation(self, method="percent", cost_line=None):
        cost_line = cost_line or self._create_cost_line()
        return self.env["glc.salary.allocation"].create(
            {
                "company_id": self.env.company.id,
                "employee_id": self.employee.id,
                "period_date": self.period,
                "employee_cost_line_id": cost_line.id,
                "method": method,
            }
        )

    def test_menus_salary_allocation_exist(self):
        """CA1 — menus Coûts salariés et Ventilations."""
        cost_menu = self.env.ref("dorevia_glc_analytics.menu_glc_employee_cost_lines")
        alloc_menu = self.env.ref("dorevia_glc_analytics.menu_glc_salary_allocations")
        self.assertEqual(
            cost_menu.action.id,
            self.env.ref("dorevia_glc_analytics.action_glc_employee_cost_line").id,
        )
        self.assertEqual(
            alloc_menu.action.id,
            self.env.ref("dorevia_glc_analytics.action_glc_salary_allocation").id,
        )

    def test_cost_line_hourly_computed(self):
        """CA2 — coût horaire calculé."""
        cost_line = self._create_cost_line(cost_amount=3000.0, reference_hours=150.0)
        self.assertEqual(cost_line.hourly_cost, 20.0)

    def test_percent_validate_at_100(self):
        """CA3 — ventilation percent 100 % validable."""
        allocation = self._create_allocation(method="percent")
        self.env["glc.salary.allocation.line"].create(
            [
                {
                    "allocation_id": allocation.id,
                    "activity_account_id": self.bar.id,
                    "percent": 60.0,
                },
                {
                    "allocation_id": allocation.id,
                    "activity_account_id": self.structure.id,
                    "percent": 40.0,
                },
            ]
        )
        move_count = self.env["account.move"].search_count([])
        allocation.action_validate()
        self.assertEqual(allocation.state, "validated")
        self.assertEqual(self.env["account.move"].search_count([]), move_count)

    def test_percent_partial_draft_then_validate_refused(self):
        """CA4 — partiel OK en brouillon, validation refusée si ≠ 100 %."""
        allocation = self._create_allocation(method="percent")
        self.env["glc.salary.allocation.line"].create(
            {
                "allocation_id": allocation.id,
                "activity_account_id": self.bar.id,
                "percent": 50.0,
            }
        )
        self.assertEqual(allocation.total_percent, 50.0)
        with self.assertRaises(UserError):
            allocation.action_validate()

    def test_hours_validate_with_reference_hours(self):
        """CA5 — ventilation heures avec reference_hours > 0."""
        cost_line = self._create_cost_line(cost_amount=2000.0, reference_hours=100.0)
        allocation = self._create_allocation(method="hours", cost_line=cost_line)
        line = self.env["glc.salary.allocation.line"].create(
            {
                "allocation_id": allocation.id,
                "activity_account_id": self.prestations.id,
                "hours": 100.0,
            }
        )
        self.assertEqual(line.amount, 2000.0)
        allocation.action_validate()
        self.assertEqual(allocation.state, "validated")

    def test_funding_activity_refused(self):
        """CA6 — activité Financements refusée."""
        allocation = self._create_allocation(method="percent")
        with self.assertRaises(ValidationError):
            self.env["glc.salary.allocation.line"].create(
                {
                    "allocation_id": allocation.id,
                    "activity_account_id": self.adhesions.id,
                    "percent": 100.0,
                }
            )

    def test_negative_percent_refused(self):
        """Pourcentage négatif refusé en ventilation salariale."""
        allocation = self._create_allocation(method="percent")
        with self.assertRaises(ValidationError):
            self.env["glc.salary.allocation.line"].create(
                {
                    "allocation_id": allocation.id,
                    "activity_account_id": self.bar.id,
                    "percent": -10.0,
                }
            )

    def test_negative_hours_refused(self):
        """Heures négatives refusées en ventilation salariale."""
        allocation = self._create_allocation(method="hours")
        with self.assertRaises(ValidationError):
            self.env["glc.salary.allocation.line"].create(
                {
                    "allocation_id": allocation.id,
                    "activity_account_id": self.bar.id,
                    "hours": -5.0,
                }
            )

    def test_payroll_variance_banner_informative(self):
        """CA7 — bandeau écart masse comptable informatif."""
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
                    "name": "Salaires test GLC P2",
                    "code": "641200",
                    "account_type": "expense",
                }
            )

        self._create_invoice_one_line(
            price_unit=10000.0,
            move_type="in_invoice",
            invoice_date="2026-06-15",
            tax_ids=[Command.clear()],
            post=True,
        ).invoice_line_ids[0].write({"account_id": payroll_account.id})

        allocation = self._create_allocation(method="percent")
        self.env["glc.salary.allocation.line"].create(
            {
                "allocation_id": allocation.id,
                "activity_account_id": self.bar.id,
                "percent": 100.0,
            }
        )
        allocation.action_validate()
        allocation.invalidate_recordset(
            [
                "accounting_payroll_mass",
                "validated_allocated_total",
                "payroll_variance_pct",
                "payroll_variance_alert",
            ]
        )
        self.assertGreater(allocation.accounting_payroll_mass, 0.0)
        self.assertGreater(allocation.payroll_variance_pct, 5.0)
        self.assertTrue(allocation.payroll_variance_alert)

    def test_hours_without_reference_hours_refused_at_validation(self):
        """reference_hours > 0 requis pour méthode hours."""
        cost_line = self._create_cost_line(cost_amount=2000.0, reference_hours=0.0)
        allocation = self._create_allocation(method="hours", cost_line=cost_line)
        self.env["glc.salary.allocation.line"].create(
            {
                "allocation_id": allocation.id,
                "activity_account_id": self.bar.id,
                "hours": 0.0,
            }
        )
        with self.assertRaises(UserError):
            allocation.action_validate()
