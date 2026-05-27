# -*- coding: utf-8 -*-

import itertools
from calendar import monthrange
from datetime import date

from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.exceptions import UserError
from odoo.fields import Command, Date
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGlcCoverageCockpit(AccountTestInvoicingCommon):
    """Palier 4 — cockpit couverture des charges de structure GLC."""

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

    def _month_label(self, year, month):
        month_names = {
            1: "Janvier",
            2: "Février",
            3: "Mars",
            4: "Avril",
            5: "Mai",
            6: "Juin",
            7: "Juillet",
            8: "Août",
            9: "Septembre",
            10: "Octobre",
            11: "Novembre",
            12: "Décembre",
        }
        return "%s %s" % (month_names[month], year)

    def _month_key(self, year, month):
        return "%04d-%02d" % (year, month)

    def _month_bounds(self, year, month):
        return date(year, month, 1), date(year, month, monthrange(year, month)[1])

    def _create_cockpit(
        self,
        date_from=None,
        date_to=None,
        year=None,
        month="6",
        skip_auto_refresh=False,
    ):
        if date_from is None or date_to is None:
            year = year or self.test_year
            month = int(month)
            date_from, date_to = self._month_bounds(year, month)
        env = self.env["glc.coverage.cockpit"]
        if skip_auto_refresh:
            env = env.with_context(glc_cockpit_auto_refreshing=True)
        return env.create(
            {
                "company_id": self.env.company.id,
                "date_from": date_from,
                "date_to": date_to,
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

    def _create_validated_allocation(self, amount=3000.0, bar_percent=100.0, employee=None, period_date=None):
        employee = employee or self.employee
        period_date = period_date or self.period
        cost_line = self.env["glc.employee.cost.line"].create(
            {
                "company_id": self.env.company.id,
                "employee_id": employee.id,
                "period_date": period_date,
                "cost_amount": amount,
                "reference_hours": 151.67,
            }
        )
        allocation = self.env["glc.salary.allocation"].create(
            {
                "company_id": self.env.company.id,
                "employee_id": employee.id,
                "period_date": period_date,
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
        """CA1 — menu Cockpit couverture des charges de structure."""
        menu = self.env.ref("dorevia_glc_analytics.menu_glc_coverage_cockpit")
        action = self.env.ref("dorevia_glc_analytics.action_glc_coverage_cockpit")
        self.assertEqual(menu.action.id, action.id)
        self.assertEqual(action.state, "code")

    def test_action_open_default_cockpit(self):
        """CA-UX10 — ouverture directe avec filtres par défaut et recalcul auto."""
        today = Date.context_today(self.env["glc.coverage.cockpit"])
        action = self.env["glc.coverage.cockpit"].action_open_default_cockpit()
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "glc.coverage.cockpit")
        cockpit = self.env["glc.coverage.cockpit"].browse(action["res_id"])
        self.assertEqual(cockpit.company_id, self.env.company)
        self.assertEqual(cockpit.date_from, date(today.year, today.month, 1))
        self.assertEqual(
            cockpit.date_to,
            date(today.year, today.month, monthrange(today.year, today.month)[1]),
        )
        self.assertEqual(cockpit.budget_scenario, "initial")
        self.assertFalse(cockpit.activity_account_id)
        self.assertTrue(cockpit.is_refreshed)
        self.assertIn("Cockpit GLC ·", cockpit.display_title)
        self.assertNotIn("Toutes activités", cockpit.display_title)
        action2 = self.env["glc.coverage.cockpit"].action_open_default_cockpit()
        self.assertEqual(action2["res_id"], action["res_id"])

    def test_action_open_detail_grouped(self):
        """UX-G1 — ouverture d'une vraie vue liste avec group_by natif."""
        year = self._next_test_year()
        self._create_revenue_on_account(
            self.bar, 1000.0, invoice_date="%s-01-15" % year
        )
        self._create_revenue_on_account(
            self.bar, 2000.0, invoice_date="%s-02-15" % year
        )
        cockpit = self._create_cockpit(
            date_from=date(year, 1, 1),
            date_to=date(year, 2, 28),
        )
        cockpit.action_refresh()

        action = cockpit.action_open_detail_grouped()
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "glc.coverage.cockpit.line")
        self.assertEqual(action["view_mode"], "list")
        self.assertIn(("cockpit_id", "=", cockpit.id), action["domain"])
        self.assertIn(("line_kind", "=", "activity"), action["domain"])
        self.assertEqual(action["context"]["search_default_group_month"], 1)
        list_view = self.env.ref(
            "dorevia_glc_analytics.view_glc_coverage_cockpit_line_list_grouped"
        )
        self.assertEqual(action["views"], [(list_view.id, "list")])

    def test_invalid_date_range_rejected(self):
        """P4 — période invalide refusée."""
        with self.assertRaises(UserError):
            self._create_cockpit(
                date_from=date(2026, 4, 30),
                date_to=date(2026, 4, 1),
                skip_auto_refresh=True,
            )

    def test_write_filters_triggers_refresh(self):
        """CA-UX10 — changement de filtre recalcule automatiquement le cockpit."""
        cockpit = self._create_cockpit(year=self.test_year, month="6", skip_auto_refresh=True)
        self.assertFalse(cockpit.is_refreshed)
        cockpit.with_context(glc_cockpit_auto_refreshing=False).write(
            {"date_to": date(self.test_year, 7, 31)}
        )
        self.assertTrue(cockpit.is_refreshed)

    def test_web_read_triggers_refresh(self):
        """CA-UX10 — affichage formulaire recalcule un cockpit non initialisé."""
        cockpit = self._create_cockpit(year=self.test_year, month="6", skip_auto_refresh=True)
        self.assertFalse(cockpit.is_refreshed)
        payload = cockpit.with_context(glc_cockpit_auto_refreshing=False).web_read(
            {"is_refreshed": {}, "alert_status": {}}
        )
        self.assertTrue(payload[0]["is_refreshed"])
        self.assertTrue(payload[0]["alert_status"])

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
            lambda line: line.line_kind == "activity"
            and line.analytic_account_id == self.bar
        )
        self.assertTrue(bar_lines)
        self.assertAlmostEqual(sum(bar_lines.mapped("revenue_realized")), 4000.0)
        self.assertAlmostEqual(sum(bar_lines.mapped("payroll_realized")), 2000.0)
        self.assertGreater(cockpit.detail_line_count, 0)

    def test_multi_month_detail_activity_only(self):
        """UX-GROUPBY C — backend ne produit que des lignes activity (sous-totaux côté OWL)."""
        year = self._next_test_year()
        self._create_revenue_on_account(
            self.bar, 1000.0, invoice_date="%s-01-15" % year
        )
        self._create_revenue_on_account(
            self.bar, 2000.0, invoice_date="%s-02-15" % year
        )
        cockpit = self._create_cockpit(
            date_from=date(year, 1, 1),
            date_to=date(year, 2, 28),
        )
        cockpit.action_refresh()

        activity_lines = cockpit.line_ids.filtered(lambda line: line.line_kind == "activity")
        self.assertEqual(len(activity_lines), 2)
        # UX-G5 par construction : aucune ligne artificielle en base.
        self.assertFalse(
            cockpit.line_ids.filtered(
                lambda line: line.line_kind in ("month_total", "period_total")
            )
        )
        self.assertAlmostEqual(
            sum(activity_lines.mapped("revenue_realized")), 3000.0
        )
        self.assertAlmostEqual(cockpit.resources_realized, 3000.0)
        self.assertEqual(
            sorted(activity_lines.mapped("month_key")),
            sorted([self._month_key(year, 1), self._month_key(year, 2)]),
        )

    def test_single_month_has_no_artificial_totals(self):
        """UX-GROUPBY C — mois unique : pas de lignes artificielles."""
        year = self._next_test_year()
        self._create_revenue_on_account(
            self.bar, 1500.0, invoice_date="%s-03-15" % year
        )
        cockpit = self._create_cockpit(
            date_from=date(year, 3, 1),
            date_to=date(year, 3, 31),
        )
        cockpit.action_refresh()

        self.assertTrue(
            cockpit.line_ids.filtered(lambda line: line.line_kind == "activity")
        )
        self.assertFalse(
            cockpit.line_ids.filtered(
                lambda line: line.line_kind in ("month_total", "period_total")
            )
        )

    def test_detail_activity_sums_match_cockpit_aggregates(self):
        """UX-G5 — sommes activité = agrégats cockpit (pas de double comptage)."""
        year = self._next_test_year()
        self._create_revenue_on_account(
            self.bar, 1000.0, invoice_date="%s-01-15" % year
        )
        self._create_revenue_on_account(
            self.bar, 2000.0, invoice_date="%s-02-15" % year
        )
        cockpit = self._create_cockpit(
            date_from=date(year, 1, 1),
            date_to=date(year, 2, 28),
        )
        cockpit.action_refresh()

        activity_lines = cockpit.line_ids.filtered(lambda line: line.line_kind == "activity")
        self.assertAlmostEqual(
            sum(activity_lines.mapped("revenue_realized")),
            cockpit.activity_revenue_realized,
        )
        self.assertAlmostEqual(cockpit.activity_revenue_realized, 3000.0)

    def test_partial_month_excludes_entries_before_date_from(self):
        """P4 — période partielle : réalisé limité aux dates exactes."""
        year = self._next_test_year()
        self._create_revenue_on_account(
            self.bar, 500.0, invoice_date="%s-03-10" % year
        )
        self._create_revenue_on_account(
            self.bar, 1500.0, invoice_date="%s-03-20" % year
        )
        cockpit = self._create_cockpit(
            date_from=date(year, 3, 15),
            date_to=date(year, 3, 31),
        )
        cockpit.action_refresh()

        self.assertAlmostEqual(cockpit.activity_revenue_realized, 1500.0)
        self.assertIn("15 mars", cockpit.period_range_label)
        bar_line = cockpit.line_ids.filtered(
            lambda line: line.line_kind == "activity"
            and line.analytic_account_id == self.bar
        )
        self.assertAlmostEqual(bar_line.revenue_realized, 1500.0)

    def test_partial_period_includes_full_month_budget(self):
        """P4 / R4 — budget V1 : mois touché = mois budgétaire complet."""
        year = self._next_test_year()
        self._create_validated_budget(
            year,
            [
                {
                    "period_date": "%s-03-01" % year,
                    "line_type": "revenue",
                    "analytic_account_id": self.bar.id,
                    "amount": 3000.0,
                },
                {
                    "period_date": "%s-04-01" % year,
                    "line_type": "revenue",
                    "analytic_account_id": self.bar.id,
                    "amount": 4000.0,
                },
            ],
        )
        cockpit = self._create_cockpit(
            date_from=date(year, 3, 15),
            date_to=date(year, 4, 30),
        )
        cockpit.action_refresh()

        self.assertAlmostEqual(cockpit.activity_revenue_budget, 7000.0)

    def test_single_full_month_title_uses_month_name(self):
        """P4 — titre mensuel complet conservé."""
        year = self._next_test_year()
        cockpit = self._create_cockpit(
            date_from=date(year, 4, 1),
            date_to=date(year, 4, 30),
        )
        self.assertIn("Avril", cockpit.display_title)
        self.assertNotIn("→", cockpit.display_title)

    def test_detail_empty_state_without_lines(self):
        """CA-UX13 — synthèse calculée sans détail : pas de bandeau alerte en vue."""
        year = self._next_test_year()
        invoice_date = "%s-08-15" % year
        self._create_revenue_on_account(
            self.subventions, 5000.0, invoice_date=invoice_date
        )

        cockpit = self._create_cockpit(
            date_from=date(year, 8, 1),
            date_to=date(year, 8, 31),
        )
        cockpit.action_refresh()

        self.assertFalse(
            cockpit.line_ids.filtered(lambda line: line.line_kind == "activity")
        )
        self.assertEqual(cockpit.detail_line_count, 0)
        self.assertTrue(cockpit.is_refreshed)
        self.assertGreater(cockpit.resources_realized, 0)
        self.assertEqual(cockpit.alert_status, "green")

    def test_refresh_clears_legacy_activity_filter(self):
        """CA-UX14 — le filtre Activité n'est plus appliqué au recalcul."""
        cockpit = self._create_cockpit(year=self.test_year, skip_auto_refresh=True)
        cockpit.with_context(glc_cockpit_auto_refreshing=True).write(
            {"activity_account_id": self.bar.id}
        )
        cockpit.action_refresh()
        self.assertFalse(cockpit.activity_account_id)

    def test_filter_change_rebuilds_detail_lines(self):
        """R10 — changement de période recalcule les lignes détail."""
        year = self._next_test_year()
        self._create_revenue_on_account(
            self.bar, 1000.0, invoice_date="%s-01-15" % year
        )
        self._create_revenue_on_account(
            self.bar, 2000.0, invoice_date="%s-04-15" % year
        )
        cockpit = self._create_cockpit(
            date_from=date(year, 4, 1),
            date_to=date(year, 4, 30),
        )
        cockpit.action_refresh()

        april_lines = cockpit.line_ids.filtered(
            lambda line: line.line_kind == "activity"
            and line.month_label == self._month_label(year, 4)
        )
        self.assertTrue(april_lines)
        self.assertAlmostEqual(sum(april_lines.mapped("revenue_realized")), 2000.0)

        cockpit.with_context(glc_cockpit_auto_refreshing=False).write(
            {"date_from": date(year, 1, 1), "date_to": date(year, 1, 31)}
        )
        january_lines = cockpit.line_ids.filtered(
            lambda line: line.line_kind == "activity"
            and line.month_label == self._month_label(year, 1)
        )
        april_lines_after = cockpit.line_ids.filtered(
            lambda line: line.month_label == self._month_label(year, 4)
        )
        self.assertTrue(january_lines)
        self.assertFalse(april_lines_after)
        self.assertAlmostEqual(sum(january_lines.mapped("revenue_realized")), 1000.0)
        self.assertEqual(cockpit.refresh_key, cockpit._current_refresh_key())

    def test_write_ignores_client_line_ids_commands(self):
        """R10 — le save client ne doit pas recréer des lignes sans cockpit_id."""
        year = self._next_test_year()
        self._create_revenue_on_account(
            self.bar, 1000.0, invoice_date="%s-01-15" % year
        )
        cockpit = self._create_cockpit(
            date_from=date(year, 1, 1),
            date_to=date(year, 1, 31),
        )
        cockpit.action_refresh()
        self.assertTrue(cockpit.line_ids)

        cockpit.with_context(glc_cockpit_auto_refreshing=False).write(
            {
                "date_to": date(year, 2, 28),
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "period_date": date(year, 1, 1),
                            "activity_label": "Ligne client interdite",
                        },
                    )
                ],
            }
        )
        self.assertFalse(
            cockpit.line_ids.filtered(
                lambda line: line.activity_label == "Ligne client interdite"
            )
        )
        self.assertEqual(cockpit.date_to, date(year, 2, 28))

    def test_web_save_ignores_client_line_ids_commands(self):
        """R10 — web_save client ne doit jamais recréer des lignes sans cockpit_id."""
        year = self._next_test_year()
        self._create_revenue_on_account(
            self.bar, 1000.0, invoice_date="%s-01-15" % year
        )
        cockpit = self._create_cockpit(
            date_from=date(year, 1, 1),
            date_to=date(year, 1, 31),
        )
        cockpit.action_refresh()
        self.assertTrue(cockpit.line_ids)

        cockpit.with_context(glc_cockpit_auto_refreshing=False).web_save(
            {
                "date_to": date(year, 2, 28),
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "period_date": date(year, 1, 1),
                            "activity_label": "Ligne client interdite",
                        },
                    )
                ],
            },
            {"line_ids": {"fields": {}}},
        )
        self.assertFalse(
            cockpit.line_ids.filtered(
                lambda line: line.activity_label == "Ligne client interdite"
            )
        )
        self.assertEqual(cockpit.date_to, date(year, 2, 28))

    def test_client_line_create_without_refresh_context_is_noop(self):
        """Les créations client orphelines sont ignorées sans erreur."""
        created = self.env["glc.coverage.cockpit.line"].with_context(
            glc_cockpit_auto_refreshing=False
        ).create(
            [
                {
                    "period_date": date(2026, 5, 1),
                    "activity_label": "Ligne client orpheline",
                }
            ]
        )
        self.assertFalse(created)

    def test_multi_month_shortened_to_q1_rebuilds_lines(self):
        """R10 cas 1 — multi-mois vers période plus courte."""
        year = self._next_test_year()
        self._create_revenue_on_account(
            self.bar, 1000.0, invoice_date="%s-01-15" % year
        )
        self._create_revenue_on_account(
            self.bar, 2000.0, invoice_date="%s-04-15" % year
        )
        cockpit = self._create_cockpit(
            date_from=date(year, 1, 1),
            date_to=date(year, 4, 30),
        )
        cockpit.action_refresh()
        self.assertTrue(
            cockpit.line_ids.filtered(
                lambda line: line.month_label == self._month_label(year, 4)
            )
        )

        cockpit.with_context(glc_cockpit_auto_refreshing=False).write(
            {"date_to": date(year, 3, 31)}
        )
        self.assertFalse(
            cockpit.line_ids.filtered(
                lambda line: line.month_label == self._month_label(year, 4)
            )
        )
        self.assertTrue(
            cockpit.line_ids.filtered(
                lambda line: line.month_label == self._month_label(year, 1)
            )
        )
        activity_lines = cockpit.line_ids.filtered(
            lambda line: line.line_kind == "activity"
        )
        self.assertAlmostEqual(
            sum(activity_lines.mapped("revenue_realized")), 1000.0
        )

    def test_web_read_refreshes_stale_lines_after_period_change(self):
        """R10 — web_read recalcule si refresh_key désalignée."""
        year = self._next_test_year()
        self._create_revenue_on_account(
            self.bar, 1500.0, invoice_date="%s-02-15" % year
        )
        cockpit = self._create_cockpit(
            date_from=date(year, 4, 1),
            date_to=date(year, 4, 30),
            skip_auto_refresh=True,
        )
        cockpit.with_context(glc_cockpit_auto_refreshing=True).write(
            {
                "date_from": date(year, 2, 1),
                "date_to": date(year, 2, 28),
                "is_refreshed": True,
                "refresh_key": "%s|%s|initial"
                % (date(year, 4, 1), date(year, 4, 30)),
            }
        )
        cockpit.with_context(glc_cockpit_auto_refreshing=False).web_read(
            {"line_ids": {"fields": {}}}
        )
        february_lines = cockpit.line_ids.filtered(
            lambda line: line.line_kind == "activity"
            and line.month_label == self._month_label(year, 2)
        )
        self.assertTrue(february_lines)
        self.assertEqual(cockpit.refresh_key, cockpit._current_refresh_key())
