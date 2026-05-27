# -*- coding: utf-8 -*-

import itertools

from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGlcBudget(AccountTestInvoicingCommon):
    """Palier 3 — budget prévisionnel GLC."""

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
        cls.structure = cls.env.ref("dorevia_glc_analytics.analytic_account_glc_structure")
        cls.subventions = cls.env.ref("dorevia_glc_analytics.analytic_account_glc_subventions")
        cls.adhesions = cls.env.ref("dorevia_glc_analytics.analytic_account_glc_adhesions")
        cls.period = "2026-04-01"
        existing_years = cls.env["glc.budget"].search([]).mapped("year")
        base_year = max(existing_years + [2100]) + 1
        cls._year_counter = itertools.count(base_year)

    def _next_test_year(self):
        return next(self._year_counter)

    def _create_budget(self, scenario="initial", year=None):
        year = year if year is not None else self._next_test_year()
        return self.env["glc.budget"].create(
            {
                "name": "Budget test %s %s" % (year, scenario),
                "year": year,
                "scenario": scenario,
                "company_id": self.env.company.id,
            }
        )

    def _create_line(self, budget, line_type="expense", account=None, amount=1000.0):
        account = account or self.structure
        return self.env["glc.budget.line"].create(
            {
                "budget_id": budget.id,
                "period_date": self.period,
                "line_type": line_type,
                "analytic_account_id": account.id,
                "amount": amount,
            }
        )

    def test_menu_budget_exists(self):
        """CA1 — module installable, menu Budgets prévisionnels."""
        menu = self.env.ref("dorevia_glc_budget.menu_glc_budgets")
        self.assertEqual(
            menu.action.id,
            self.env.ref("dorevia_glc_budget.action_glc_budget").id,
        )

    def test_budget_scenarios(self):
        """CA2 — scénarios initial / revised / landing."""
        for scenario in ("initial", "revised", "landing"):
            budget = self._create_budget(scenario=scenario)
            self.assertEqual(budget.scenario, scenario)

    def test_budget_line_monthly_activity(self):
        """CA3 — saisie mensuelle par axe analytique."""
        budget = self._create_budget()
        line = self._create_line(budget, line_type="revenue", account=self.bar, amount=3000.0)
        self.assertEqual(line.period_date.isoformat(), self.period)
        self.assertEqual(line.analytic_account_id, self.bar)

    def test_line_types_domains(self):
        """CA4 — types revenue / expense / funding cohérents."""
        budget = self._create_budget()
        self._create_line(budget, line_type="revenue", account=self.bar)
        self._create_line(budget, line_type="expense", account=self.structure)
        self._create_line(budget, line_type="funding", account=self.subventions)

    def test_funding_account_refused_on_expense(self):
        """CA5 — compte Financements refusé sur charge."""
        budget = self._create_budget()
        with self.assertRaises(ValidationError):
            self._create_line(budget, line_type="expense", account=self.subventions)

    def test_activity_account_refused_on_funding(self):
        """CA6 — compte Activités refusé sur financement."""
        budget = self._create_budget()
        with self.assertRaises(ValidationError):
            self._create_line(budget, line_type="funding", account=self.bar)

    def test_workflow_draft_validated_archived(self):
        """CA7 — workflow brouillon → validé → archivé."""
        budget = self._create_budget()
        self._create_line(budget)
        budget.action_validate()
        self.assertEqual(budget.state, "validated")
        self.assertTrue(budget.validated_by)
        with self.assertRaises(UserError):
            self._create_line(budget)
        budget.action_reset_to_draft()
        self.assertEqual(budget.state, "draft")
        self._create_line(budget, line_type="revenue", account=self.bar, amount=500.0)
        budget.action_validate()
        budget.action_archive()
        self.assertEqual(budget.state, "archived")

    def test_no_accounting_entries_generated(self):
        """CA8 — aucune écriture comptable ni analytique."""
        budget = self._create_budget()
        moves_before = self.env["account.move"].search_count([])
        analytic_before = self.env["account.analytic.line"].search_count([])
        self._create_line(budget, line_type="revenue", account=self.bar, amount=5000.0)
        budget.action_validate()
        self.assertEqual(self.env["account.move"].search_count([]), moves_before)
        self.assertEqual(
            self.env["account.analytic.line"].search_count([]), analytic_before
        )

    def test_unique_budget_per_company_year_scenario(self):
        """Contrainte unicité budget."""
        year = self._next_test_year()
        self._create_budget(scenario="initial", year=year)
        with self.assertRaises(Exception):
            self._create_budget(scenario="initial", year=year)

    def test_unique_budget_line(self):
        """Contrainte unicité ligne."""
        budget = self._create_budget()
        self._create_line(budget, line_type="expense", account=self.structure)
        with self.assertRaises(Exception):
            self._create_line(budget, line_type="expense", account=self.structure)

    def test_period_must_be_first_of_month(self):
        """Période = 1er jour du mois."""
        budget = self._create_budget()
        with self.assertRaises(ValidationError):
            self.env["glc.budget.line"].create(
                {
                    "budget_id": budget.id,
                    "period_date": "2026-04-15",
                    "line_type": "expense",
                    "analytic_account_id": self.structure.id,
                    "amount": 100.0,
                }
            )

    def test_negative_amount_refused(self):
        """Montant ≥ 0."""
        budget = self._create_budget()
        with self.assertRaises(ValidationError):
            self._create_line(budget, amount=-1.0)
