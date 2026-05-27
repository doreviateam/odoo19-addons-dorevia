# -*- coding: utf-8 -*-

from calendar import monthrange
from datetime import date

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from .glc_constants import (
    GLC_COCKPIT_ACTIVITY_REVENUE_CODES,
    GLC_COCKPIT_FUNDING_CODES,
    GLC_COCKPIT_GENERAL_EXPENSE_CODE,
    GLC_COCKPIT_PAYROLL_BUDGET_CODES,
    GLC_COCKPIT_SALARY_EXCLUDED_ANALYTIC_CODES,
    GLC_EXCLUDED_GL_ACCOUNT_PREFIXES,
    GLC_EXPENSE_ACCOUNT_TYPES,
    GLC_INCOME_ACCOUNT_TYPES,
    GLC_LEGACY_ANALYTIC_CODES,
    GLC_PAYROLL_ACCOUNT_PREFIXES,
)


class GlcCoverageCockpit(models.TransientModel):
    _name = "glc.coverage.cockpit"
    _description = "Cockpit couverture des salaires GLC"
    _rec_name = "display_title"

    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.company,
    )
    year = fields.Integer(
        required=True,
        default=lambda self: fields.Date.context_today(self).year,
    )
    month = fields.Selection(
        selection=[
            ("0", "Toute l'année"),
            ("1", "Janvier"),
            ("2", "Février"),
            ("3", "Mars"),
            ("4", "Avril"),
            ("5", "Mai"),
            ("6", "Juin"),
            ("7", "Juillet"),
            ("8", "Août"),
            ("9", "Septembre"),
            ("10", "Octobre"),
            ("11", "Novembre"),
            ("12", "Décembre"),
        ],
        required=True,
        default="0",
    )
    activity_account_id = fields.Many2one(
        "account.analytic.account",
        string="Activité GLC",
        check_company=True,
        domain=lambda self: [
            ("plan_id", "=", self.env.ref("dorevia_glc_analytics.analytic_plan_glc_activites").id),
            "|",
            ("company_id", "=", False),
            ("company_id", "in", self.env.companies.ids),
        ],
    )
    budget_scenario = fields.Selection(
        selection=[
            ("initial", "Initial"),
            ("revised", "Révisé"),
            ("landing", "Atterrissage"),
        ],
        required=True,
        default="initial",
    )
    currency_id = fields.Many2one(
        "res.currency",
        compute="_compute_currency_id",
    )
    date_from = fields.Date(string="Du", readonly=True)
    date_to = fields.Date(string="Au", readonly=True)
    display_title = fields.Char(
        string="Titre",
        compute="_compute_display_title",
    )

    activity_revenue_realized = fields.Monetary(
        string="Recettes d'activité (réalisé)",
        readonly=True,
        currency_field="currency_id",
    )
    funding_realized = fields.Monetary(
        string="Financements (réalisé)",
        readonly=True,
        currency_field="currency_id",
    )
    resources_realized = fields.Monetary(
        string="Ressources disponibles (réalisé)",
        readonly=True,
        currency_field="currency_id",
    )
    payroll_realized = fields.Monetary(
        string="Masse salariale (réalisé)",
        readonly=True,
        currency_field="currency_id",
    )
    general_expenses_realized = fields.Monetary(
        string="Frais généraux (réalisé)",
        readonly=True,
        currency_field="currency_id",
    )
    fixed_charges_realized = fields.Monetary(
        string="Charges fixes (réalisé)",
        readonly=True,
        currency_field="currency_id",
        help="Masse salariale + frais généraux.",
    )

    activity_revenue_budget = fields.Monetary(
        string="Recettes d'activité (budget)",
        readonly=True,
        currency_field="currency_id",
    )
    funding_budget = fields.Monetary(
        string="Financements (budget)",
        readonly=True,
        currency_field="currency_id",
    )
    resources_budget = fields.Monetary(
        string="Ressources disponibles (budget)",
        readonly=True,
        currency_field="currency_id",
    )
    payroll_budget = fields.Monetary(
        string="Masse salariale (budget)",
        readonly=True,
        currency_field="currency_id",
    )
    general_expenses_budget = fields.Monetary(
        string="Frais généraux (budget)",
        readonly=True,
        currency_field="currency_id",
    )

    salary_coverage_rate = fields.Float(
        string="Taux de couverture des salaires (%)",
        digits=(16, 2),
        readonly=True,
    )
    balance_after_payroll = fields.Monetary(
        string="Solde après salaires",
        readonly=True,
        currency_field="currency_id",
    )
    balance_after_fixed = fields.Monetary(
        string="Solde après salaires et frais généraux",
        readonly=True,
        currency_field="currency_id",
    )
    alert_status = fields.Selection(
        string="Statut alerte",
        selection=[
            ("red", "Rouge — ressources insuffisantes"),
            ("orange", "Orange — salaires couverts, frais généraux non"),
            ("green", "Vert — salaires et frais généraux couverts"),
        ],
        readonly=True,
    )
    alert_message = fields.Char(string="Message alerte", readonly=True)
    is_refreshed = fields.Boolean(string="Calcul effectué", readonly=True, default=False)
    line_ids = fields.One2many(
        "glc.coverage.cockpit.line",
        "cockpit_id",
        readonly=True,
    )

    @api.depends("company_id")
    def _compute_currency_id(self):
        for cockpit in self:
            cockpit.currency_id = cockpit.company_id.currency_id

    @api.depends("year", "month", "budget_scenario", "activity_account_id")
    def _compute_display_title(self):
        month_labels = dict(self._fields["month"].selection)
        scenario_labels = dict(self._fields["budget_scenario"].selection)
        for cockpit in self:
            period = month_labels.get(cockpit.month, "")
            if cockpit.month == "0":
                period = _("Année complète")
            activity = cockpit.activity_account_id.display_name or _("Toutes activités")
            cockpit.display_title = _(
                "Cockpit GLC · %(year)s · %(period)s · %(scenario)s · %(activity)s",
                year=cockpit.year,
                period=period,
                scenario=scenario_labels.get(cockpit.budget_scenario, cockpit.budget_scenario),
                activity=activity,
            )

    @api.constrains("year")
    def _check_year(self):
        for cockpit in self:
            if cockpit.year < 2000 or cockpit.year > 2100:
                raise UserError(_("L'année doit être comprise entre 2000 et 2100."))

    def _period_bounds(self):
        self.ensure_one()
        month = int(self.month)
        if month:
            date_from = date(self.year, month, 1)
            date_to = date(self.year, month, monthrange(self.year, month)[1])
        else:
            date_from = date(self.year, 1, 1)
            date_to = date(self.year, 12, 31)
        return date_from, date_to

    def _month_starts_in_period(self):
        self.ensure_one()
        date_from, date_to = self._period_bounds()
        months = []
        cursor = date(date_from.year, date_from.month, 1)
        end = date(date_to.year, date_to.month, 1)
        while cursor <= end:
            months.append(cursor)
            if cursor.month == 12:
                cursor = date(cursor.year + 1, 1, 1)
            else:
                cursor = date(cursor.year, cursor.month + 1, 1)
        return months

    def _analytic_accounts_by_codes(self, codes):
        return self.env["account.analytic.account"].search(
            [
                ("code", "in", list(codes)),
                ("company_id", "in", [False, self.company_id.id]),
            ]
        )

    def _activity_accounts(self):
        self.ensure_one()
        if self.activity_account_id:
            return self.activity_account_id
        return self.env["account.analytic.account"].search(
            [
                (
                    "plan_id",
                    "=",
                    self.env.ref("dorevia_glc_analytics.analytic_plan_glc_activites").id,
                ),
                ("company_id", "in", [False, self.company_id.id]),
                ("glc_report_active", "=", True),
            ]
        )

    def _excluded_analytic_accounts(self):
        codes = set(GLC_COCKPIT_SALARY_EXCLUDED_ANALYTIC_CODES) | set(GLC_LEGACY_ANALYTIC_CODES)
        return self.env["account.analytic.account"].search(
            [
                ("code", "in", list(codes)),
                ("company_id", "in", [False, self.company_id.id]),
            ]
        )

    def _analytic_line_domain(self, date_from, date_to, analytic_accounts):
        domain = [
            ("company_id", "=", self.company_id.id),
            ("date", ">=", date_from),
            ("date", "<=", date_to),
            (
                "general_account_id.account_type",
                "in",
                list(GLC_INCOME_ACCOUNT_TYPES + GLC_EXPENSE_ACCOUNT_TYPES),
            ),
            "|",
            ("auto_account_id", "in", analytic_accounts.ids),
            ("account_id", "in", analytic_accounts.ids),
        ]
        excluded = self._excluded_analytic_accounts()
        if excluded:
            domain += [
                ("auto_account_id", "not in", excluded.ids),
                ("account_id", "not in", excluded.ids),
            ]
        for prefix in GLC_PAYROLL_ACCOUNT_PREFIXES + GLC_EXCLUDED_GL_ACCOUNT_PREFIXES:
            domain.append(("general_account_id.code", "not like", prefix + "%"))
        return domain

    @api.model
    def _signed_analytic_amount(self, line):
        """Montant exploitable toujours positif pour le cockpit."""
        return abs(line.amount)

    def _sum_analytic_realized(self, analytic_accounts, date_from, date_to):
        if not analytic_accounts:
            return 0.0
        lines = self.env["account.analytic.line"].search(
            self._analytic_line_domain(date_from, date_to, analytic_accounts)
        )
        return sum(self._signed_analytic_amount(line) for line in lines)

    def _sum_payroll_realized(self, date_from, date_to, activity_account=None):
        domain = [
            ("allocation_id.company_id", "=", self.company_id.id),
            ("allocation_id.state", "in", ("validated", "locked")),
            ("allocation_id.period_date", ">=", date_from),
            ("allocation_id.period_date", "<=", date_to),
        ]
        if activity_account:
            domain.append(("activity_account_id", "=", activity_account.id))
        lines = self.env["glc.salary.allocation.line"].search(domain)
        return sum(lines.mapped("amount"))

    def _ensure_budget_module(self):
        if "glc.budget.line" not in self.env:
            raise UserError(
                _(
                    "Le module dorevia_glc_budget doit être installé pour utiliser le cockpit Palier 4."
                )
            )

    def _budget_lines(self, date_from=None, date_to=None, analytic_accounts=None, line_type=None):
        self._ensure_budget_module()
        domain = [
            ("company_id", "=", self.company_id.id),
            ("year", "=", self.year),
            ("scenario", "=", self.budget_scenario),
            ("budget_id.state", "in", ("validated", "archived")),
        ]
        if date_from:
            domain.append(("period_date", ">=", date_from))
        if date_to:
            domain.append(("period_date", "<=", date_to))
        if analytic_accounts:
            domain.append(("analytic_account_id", "in", analytic_accounts.ids))
        if line_type:
            domain.append(("line_type", "=", line_type))
        return self.env["glc.budget.line"].search(domain)

    def _sum_budget(self, date_from, date_to, analytic_accounts, line_type):
        lines = self._budget_lines(date_from, date_to, analytic_accounts, line_type)
        return sum(lines.mapped("amount"))

    @api.model
    def _compute_alert_status(self, resources, payroll, general_expenses):
        if resources < payroll:
            return (
                "red",
                _(
                    "Les ressources disponibles ne couvrent pas la masse salariale "
                    "(recettes d'activité + financements insuffisants)."
                ),
            )
        if resources < payroll + general_expenses:
            return (
                "orange",
                _(
                    "Les ressources couvrent la masse salariale, mais pas les frais généraux "
                    "(Structure & Administration)."
                ),
            )
        return (
            "green",
            _(
                "Les ressources couvrent la masse salariale et les frais généraux."
            ),
        )

    def _aggregate_period(self, period_start, period_end):
        self.ensure_one()
        revenue_accounts = self._analytic_accounts_by_codes(GLC_COCKPIT_ACTIVITY_REVENUE_CODES)
        funding_accounts = self._analytic_accounts_by_codes(GLC_COCKPIT_FUNDING_CODES)
        general_accounts = self._analytic_accounts_by_codes((GLC_COCKPIT_GENERAL_EXPENSE_CODE,))
        payroll_budget_accounts = self._analytic_accounts_by_codes(GLC_COCKPIT_PAYROLL_BUDGET_CODES)

        if self.activity_account_id:
            revenue_accounts = self.activity_account_id & revenue_accounts
            general_accounts = self.activity_account_id & general_accounts

        activity_revenue_realized = self._sum_analytic_realized(
            revenue_accounts, period_start, period_end
        )
        funding_realized = self._sum_analytic_realized(funding_accounts, period_start, period_end)
        general_expenses_realized = self._sum_analytic_realized(
            general_accounts, period_start, period_end
        )
        payroll_realized = self._sum_payroll_realized(
            period_start,
            period_end,
            self.activity_account_id,
        )

        activity_revenue_budget = self._sum_budget(
            period_start, period_end, revenue_accounts, "revenue"
        )
        funding_budget = self._sum_budget(
            period_start, period_end, funding_accounts, "funding"
        )
        general_expenses_budget = self._sum_budget(
            period_start, period_end, general_accounts, "expense"
        )
        payroll_budget = self._sum_budget(
            period_start, period_end, payroll_budget_accounts, "expense"
        )

        resources_realized = activity_revenue_realized + funding_realized
        resources_budget = activity_revenue_budget + funding_budget
        fixed_charges_realized = payroll_realized + general_expenses_realized

        return {
            "activity_revenue_realized": activity_revenue_realized,
            "funding_realized": funding_realized,
            "resources_realized": resources_realized,
            "payroll_realized": payroll_realized,
            "general_expenses_realized": general_expenses_realized,
            "fixed_charges_realized": fixed_charges_realized,
            "activity_revenue_budget": activity_revenue_budget,
            "funding_budget": funding_budget,
            "resources_budget": resources_budget,
            "payroll_budget": payroll_budget,
            "general_expenses_budget": general_expenses_budget,
        }

    def action_refresh(self):
        self.ensure_one()
        self._ensure_budget_module()
        self.line_ids.unlink()
        date_from, date_to = self._period_bounds()
        totals = self._aggregate_period(date_from, date_to)

        salary_coverage_rate = 0.0
        if totals["payroll_realized"]:
            salary_coverage_rate = (
                totals["resources_realized"] / totals["payroll_realized"]
            ) * 100.0

        balance_after_payroll = totals["resources_realized"] - totals["payroll_realized"]
        balance_after_fixed = balance_after_payroll - totals["general_expenses_realized"]
        alert_status, alert_message = self._compute_alert_status(
            totals["resources_realized"],
            totals["payroll_realized"],
            totals["general_expenses_realized"],
        )

        line_vals = []
        activity_accounts = self._activity_accounts()
        for month_start in self._month_starts_in_period():
            month_end = date(
                month_start.year,
                month_start.month,
                monthrange(month_start.year, month_start.month)[1],
            )
            for account in activity_accounts:
                if account.code in GLC_COCKPIT_ACTIVITY_REVENUE_CODES:
                    revenue_realized = self._sum_analytic_realized(
                        account, month_start, month_end
                    )
                    revenue_budget = self._sum_budget(
                        month_start, month_end, account, "revenue"
                    )
                else:
                    revenue_realized = 0.0
                    revenue_budget = 0.0

                expense_realized = 0.0
                expense_budget = 0.0
                if account.code == GLC_COCKPIT_GENERAL_EXPENSE_CODE:
                    expense_realized = self._sum_analytic_realized(
                        account, month_start, month_end
                    )
                    expense_budget = self._sum_budget(
                        month_start, month_end, account, "expense"
                    )

                payroll_realized = self._sum_payroll_realized(
                    month_start, month_end, account
                )
                payroll_budget = 0.0
                if account.code in GLC_COCKPIT_PAYROLL_BUDGET_CODES:
                    payroll_budget = self._sum_budget(
                        month_start, month_end, account, "expense"
                    )

                if not any(
                    (
                        revenue_realized,
                        revenue_budget,
                        expense_realized,
                        expense_budget,
                        payroll_realized,
                        payroll_budget,
                    )
                ):
                    continue

                line_vals.append(
                    {
                        "cockpit_id": self.id,
                        "period_date": month_start,
                        "analytic_account_id": account.id,
                        "revenue_realized": revenue_realized,
                        "revenue_budget": revenue_budget,
                        "expense_realized": expense_realized,
                        "expense_budget": expense_budget,
                        "payroll_realized": payroll_realized,
                        "payroll_budget": payroll_budget,
                        "variance_revenue": revenue_realized - revenue_budget,
                        "variance_payroll": payroll_realized - payroll_budget,
                    }
                )

        if line_vals:
            self.env["glc.coverage.cockpit.line"].create(line_vals)

        self.write(
            {
                "date_from": date_from,
                "date_to": date_to,
                **totals,
                "salary_coverage_rate": salary_coverage_rate,
                "balance_after_payroll": balance_after_payroll,
                "balance_after_fixed": balance_after_fixed,
                "alert_status": alert_status,
                "alert_message": alert_message,
                "is_refreshed": True,
            }
        )

        return {
            "type": "ir.actions.act_window",
            "name": _("Cockpit couverture des salaires"),
            "res_model": "glc.coverage.cockpit",
            "res_id": self.id,
            "view_mode": "form",
            "target": "current",
        }


class GlcCoverageCockpitLine(models.TransientModel):
    _name = "glc.coverage.cockpit.line"
    _description = "Détail cockpit couverture GLC"
    _order = "period_date, analytic_account_id"

    cockpit_id = fields.Many2one(
        "glc.coverage.cockpit",
        required=True,
        ondelete="cascade",
    )
    period_date = fields.Date(string="Mois", required=True)
    analytic_account_id = fields.Many2one(
        "account.analytic.account",
        string="Activité GLC",
        required=True,
    )
    currency_id = fields.Many2one(related="cockpit_id.currency_id")
    revenue_realized = fields.Monetary(
        string="Recettes (réalisé)",
        currency_field="currency_id",
    )
    revenue_budget = fields.Monetary(
        string="Recettes (budget)",
        currency_field="currency_id",
    )
    expense_realized = fields.Monetary(
        string="Frais généraux (réalisé)",
        currency_field="currency_id",
    )
    expense_budget = fields.Monetary(
        string="Frais généraux (budget)",
        currency_field="currency_id",
    )
    payroll_realized = fields.Monetary(
        string="Masse salariale (réalisé)",
        currency_field="currency_id",
    )
    payroll_budget = fields.Monetary(
        string="Masse salariale (budget)",
        currency_field="currency_id",
    )
    variance_revenue = fields.Monetary(
        string="Écart recettes",
        currency_field="currency_id",
    )
    variance_payroll = fields.Monetary(
        string="Écart masse salariale",
        currency_field="currency_id",
    )
