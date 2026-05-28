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
    _description = "Cockpit couverture des charges de structure GLC"
    _rec_name = "display_title"

    company_id = fields.Many2one(
        "res.company",
        string="Société",
        required=True,
        default=lambda self: self.env.company,
    )
    date_from = fields.Date(
        string="Date de début",
        required=True,
        default=lambda self: self._default_date_range()[0],
    )
    date_to = fields.Date(
        string="Date de fin",
        required=True,
        default=lambda self: self._default_date_range()[1],
    )
    activity_account_id = fields.Many2one(
        "account.analytic.account",
        string="Activité",
        check_company=True,
        domain=lambda self: [
            ("plan_id", "=", self.env.ref("dorevia_glc_analytics.analytic_plan_glc_activites").id),
            "|",
            ("company_id", "=", False),
            ("company_id", "in", self.env.companies.ids),
        ],
    )
    budget_scenario = fields.Selection(
        string="Scénario budgétaire",
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
    period_range_label = fields.Char(
        string="Période analysée",
        compute="_compute_period_labels",
        store=True,
    )
    display_title = fields.Char(
        string="Titre",
        compute="_compute_display_title",
        store=True,
    )

    activity_revenue_realized = fields.Monetary(
        string="Recettes réalisées",
        readonly=True,
        currency_field="currency_id",
    )
    funding_realized = fields.Monetary(
        string="Financements réalisés",
        readonly=True,
        currency_field="currency_id",
    )
    resources_realized = fields.Monetary(
        string="Ressources disponibles (réalisé)",
        readonly=True,
        currency_field="currency_id",
    )
    payroll_realized = fields.Monetary(
        string="Dont masse salariale (réalisé)",
        readonly=True,
        currency_field="currency_id",
    )
    general_expenses_realized = fields.Monetary(
        string="Dont frais généraux (réalisé)",
        readonly=True,
        currency_field="currency_id",
    )
    fixed_charges_realized = fields.Monetary(
        string="Charges de structure (réalisé)",
        readonly=True,
        currency_field="currency_id",
        help="Masse salariale + frais généraux.",
    )

    activity_revenue_budget = fields.Monetary(
        string="Recettes prévues",
        readonly=True,
        currency_field="currency_id",
    )
    funding_budget = fields.Monetary(
        string="Financements prévus",
        readonly=True,
        currency_field="currency_id",
    )
    resources_budget = fields.Monetary(
        string="Ressources disponibles (prévu)",
        readonly=True,
        currency_field="currency_id",
    )
    payroll_budget = fields.Monetary(
        string="Dont masse salariale (prévu)",
        readonly=True,
        currency_field="currency_id",
    )
    general_expenses_budget = fields.Monetary(
        string="Dont frais généraux (prévu)",
        readonly=True,
        currency_field="currency_id",
    )

    salary_coverage_rate = fields.Float(
        string="Couverture masse salariale (%)",
        digits=(16, 2),
        readonly=True,
        help="Lecture intermédiaire : ressources disponibles / masse salariale.",
    )
    balance_after_payroll = fields.Monetary(
        string="Solde après masse salariale",
        readonly=True,
        currency_field="currency_id",
    )
    balance_after_fixed = fields.Monetary(
        string="Solde après charges de structure",
        readonly=True,
        currency_field="currency_id",
    )
    alert_status = fields.Selection(
        string="Statut alerte",
        selection=[
            ("red", "Rouge — masse salariale non couverte"),
            ("orange", "Orange — charges de structure partiellement couvertes"),
            ("green", "Vert — charges de structure couvertes"),
        ],
        readonly=True,
    )
    alert_message = fields.Char(string="Message alerte", readonly=True)
    is_refreshed = fields.Boolean(string="Calcul effectué", readonly=True, default=False)
    refresh_key = fields.Char(string="Clé recalcul", readonly=True, copy=False)
    line_ids = fields.One2many(
        "glc.coverage.cockpit.line",
        "cockpit_id",
        readonly=True,
    )
    detail_line_count = fields.Integer(
        string="Nombre de lignes détail",
        compute="_compute_detail_line_count",
    )

    _FILTER_FIELDS = frozenset(
        {"company_id", "date_from", "date_to", "activity_account_id", "budget_scenario"}
    )

    @api.model
    def _default_date_range(self, reference=None):
        today = reference or fields.Date.context_today(self)
        date_from = date(today.year, today.month, 1)
        date_to = date(today.year, today.month, monthrange(today.year, today.month)[1])
        return date_from, date_to

    @api.model
    def _default_open_values(self):
        date_from, date_to = self._default_date_range()
        return {
            "company_id": self.env.company.id,
            "date_from": date_from,
            "date_to": date_to,
            "budget_scenario": "initial",
            "activity_account_id": False,
        }

    @api.model
    def _domain_for_open_values(self, values):
        domain = []
        for field_name in (
            "company_id",
            "date_from",
            "date_to",
            "budget_scenario",
            "activity_account_id",
        ):
            value = values[field_name]
            if field_name == "activity_account_id" and not value:
                domain.append((field_name, "=", False))
            else:
                domain.append((field_name, "=", value))
        return domain

    @api.model
    def action_open_default_cockpit(self):
        values = self._default_open_values()
        cockpit = self.search(
            self._domain_for_open_values(values),
            limit=1,
            order="id desc",
        )
        if not cockpit:
            cockpit = self.create(values)
        cockpit.with_context(glc_cockpit_auto_refreshing=True).action_refresh()
        return {
            "type": "ir.actions.act_window",
            "name": _("Cockpit couverture des charges de structure"),
            "res_model": self._name,
            "res_id": cockpit.id,
            "view_mode": "form",
            "target": "current",
            "context": {
                "form_view_initial_mode": "edit",
                "no_breadcrumbs": True,
            },
        }

    def action_open_detail_grouped(self):
        """Ouvre une vraie vue liste Odoo (group_by natif non fiable en one2many inline)."""
        self.ensure_one()
        if self._needs_refresh():
            self.with_context(glc_cockpit_auto_refreshing=True).action_refresh()
        list_view = self.env.ref(
            "dorevia_glc_analytics.view_glc_coverage_cockpit_line_list_grouped"
        )
        return {
            "type": "ir.actions.act_window",
            "name": _("Détail par activité — %s") % (self.display_title or ""),
            "res_model": "glc.coverage.cockpit.line",
            "view_mode": "list",
            "views": [(list_view.id, "list")],
            "domain": [
                ("cockpit_id", "=", self.id),
                ("line_kind", "=", "activity"),
            ],
            "context": {
                "search_default_group_month": 1,
                "create": False,
                "edit": False,
                "delete": False,
            },
            "target": "current",
        }

    @api.model_create_multi
    def create(self, vals_list):
        cleaned_vals_list = [
            {key: value for key, value in vals.items() if key != "line_ids"}
            for vals in vals_list
        ]
        cockpits = super().create(cleaned_vals_list)
        stale = cockpits.filtered(lambda c: not c.is_refreshed)
        if stale and not self.env.context.get("glc_cockpit_auto_refreshing"):
            stale.with_context(glc_cockpit_auto_refreshing=True).action_refresh()
        return cockpits

    def web_read(self, specification):
        self._ensure_refreshed_for_display()
        return super().web_read(specification)

    def web_save(self, vals, specification, next_id=None):
        if "line_ids" in vals:
            vals = {key: value for key, value in vals.items() if key != "line_ids"}
        return super().web_save(vals, specification, next_id=next_id)

    def _ensure_refreshed_for_display(self):
        if self.env.context.get("glc_cockpit_auto_refreshing"):
            return
        stale = self.filtered(lambda cockpit: cockpit._needs_refresh())
        if stale:
            stale.with_context(glc_cockpit_auto_refreshing=True).action_refresh()

    def _current_refresh_key(self):
        self.ensure_one()
        return "%s|%s|%s" % (
            self.date_from or "",
            self.date_to or "",
            self.budget_scenario or "",
        )

    def _needs_refresh(self):
        self.ensure_one()
        if not self.is_refreshed or not self.refresh_key:
            return True
        return self.refresh_key != self._current_refresh_key()

    @api.model
    def _cron_refresh_cockpits(self):
        for cockpit in self.search([]):
            cockpit.action_refresh()

    def write(self, vals):
        if "line_ids" in vals:
            vals = {key: value for key, value in vals.items() if key != "line_ids"}
        res = super().write(vals)
        if not self.env.context.get("glc_cockpit_auto_refreshing"):
            should_refresh = self._FILTER_FIELDS.intersection(vals) or self.filtered(
                lambda cockpit: cockpit._needs_refresh()
            )
            if should_refresh:
                self.with_context(glc_cockpit_auto_refreshing=True).action_refresh()
        return res

    @api.depends("company_id")
    def _compute_currency_id(self):
        for cockpit in self:
            cockpit.currency_id = cockpit.company_id.currency_id

    _SHORT_MONTHS = {
        1: "janv.",
        2: "févr.",
        3: "mars",
        4: "avr.",
        5: "mai",
        6: "juin",
        7: "juil.",
        8: "août",
        9: "sept.",
        10: "oct.",
        11: "nov.",
        12: "déc.",
    }

    _LONG_MONTHS = {
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

    @api.model
    def _format_short_date(self, value):
        return "%s %s" % (value.day, self._SHORT_MONTHS[value.month])

    @api.depends("date_from", "date_to")
    def _compute_period_labels(self):
        for cockpit in self:
            if cockpit.date_from and cockpit.date_to:
                start = cockpit._format_short_date(cockpit.date_from)
                end = cockpit._format_short_date(cockpit.date_to)
                cockpit.period_range_label = _("%(start)s → %(end)s", start=start, end=end)
            else:
                cockpit.period_range_label = False

    @api.depends("date_from", "date_to", "budget_scenario")
    def _compute_display_title(self):
        scenario_labels = dict(self._fields["budget_scenario"].selection)
        for cockpit in self:
            if not cockpit.date_from or not cockpit.date_to:
                cockpit.display_title = _("Cockpit GLC")
                continue
            scenario = scenario_labels.get(
                cockpit.budget_scenario, cockpit.budget_scenario
            )
            if cockpit._is_full_single_calendar_month():
                period = cockpit._LONG_MONTHS[cockpit.date_from.month]
            else:
                start = cockpit._format_short_date(cockpit.date_from)
                end = cockpit._format_short_date(cockpit.date_to)
                period = _("%(start)s → %(end)s", start=start, end=end)
            cockpit.display_title = _(
                "Cockpit GLC · %(year)s · %(period)s · %(scenario)s",
                year=cockpit.date_from.year,
                period=period,
                scenario=scenario,
            )

    @api.depends("line_ids", "line_ids.line_kind")
    def _compute_detail_line_count(self):
        for cockpit in self:
            cockpit.detail_line_count = len(
                cockpit.line_ids.filtered(lambda line: line.line_kind == "activity")
            )

    @api.constrains("date_from", "date_to")
    def _check_date_range(self):
        for cockpit in self:
            if cockpit.date_from and cockpit.date_to and cockpit.date_from > cockpit.date_to:
                raise UserError(
                    _("La date de début doit être antérieure ou égale à la date de fin.")
                )

    def _is_full_single_calendar_month(self):
        self.ensure_one()
        if not self.date_from or not self.date_to:
            return False
        if (
            self.date_from.year != self.date_to.year
            or self.date_from.month != self.date_to.month
        ):
            return False
        last_day = monthrange(self.date_from.year, self.date_from.month)[1]
        return self.date_from.day == 1 and self.date_to.day == last_day

    def _period_bounds(self):
        self.ensure_one()
        return self.date_from, self.date_to

    def _month_slice_bounds(self, month_start):
        self.ensure_one()
        date_from, date_to = self._period_bounds()
        month_end = date(
            month_start.year,
            month_start.month,
            monthrange(month_start.year, month_start.month)[1],
        )
        return max(date_from, month_start), min(date_to, month_end)

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

    @api.model
    def _is_funding_analytic_account(self, account):
        """Compte analytique de financement (plan Financements GLC ou type financement)."""
        if not account:
            return False
        if account.glc_activity_type == "financement":
            return True
        plan_financements = self.env.ref(
            "dorevia_glc_analytics.analytic_plan_glc_financements",
            raise_if_not_found=False,
        )
        if plan_financements and account.plan_id == plan_financements:
            return True
        return account.code in GLC_COCKPIT_FUNDING_CODES

    def _cockpit_analytic_accounts(self):
        """Tous les comptes analytiques exploitables cockpit (tous plans par défaut)."""
        self.ensure_one()
        if self.activity_account_id:
            return self.activity_account_id
        excluded = self._excluded_analytic_accounts()
        domain = [("company_id", "in", [False, self.company_id.id])]
        if excluded:
            domain.append(("id", "not in", excluded.ids))
        return self.env["account.analytic.account"].search(domain)

    def _funding_analytic_accounts(self):
        return self._cockpit_analytic_accounts().filtered(
            lambda account: self._is_funding_analytic_account(account)
        )

    def _activity_revenue_analytic_accounts(self):
        return self._cockpit_analytic_accounts() - self._funding_analytic_accounts()

    def _activity_accounts(self):
        """Alias rétrocompat — périmètre élargi à tous les plans analytiques."""
        return self._cockpit_analytic_accounts()

    def _excluded_analytic_accounts(self):
        codes = set(GLC_COCKPIT_SALARY_EXCLUDED_ANALYTIC_CODES) | set(GLC_LEGACY_ANALYTIC_CODES)
        return self.env["account.analytic.account"].search(
            [
                ("code", "in", list(codes)),
                ("company_id", "in", [False, self.company_id.id]),
            ]
        )

    def _plan_column_names(self):
        """Colonnes analytiques Odoo 19 (account_id, x_plan3_id, x_plan4_id, …)."""
        return self.env["account.analytic.line"]._get_plan_fnames()

    def _or_domain(self, field_name, operator, values):
        columns = self._plan_column_names()
        if not columns:
            return [("auto_account_id", operator, values)]
        if len(columns) == 1:
            return [(columns[0], operator, values)]
        domain = ["|"] * (len(columns) - 1)
        for column in columns:
            domain.append((column, operator, values))
        return domain

    def _analytic_accounts_domain(self, analytic_accounts):
        if not analytic_accounts:
            return [(1, "=", 0)]
        return self._or_domain("placeholder", "in", analytic_accounts.ids)

    def _excluded_analytic_domain(self):
        excluded = self._excluded_analytic_accounts()
        if not excluded:
            return []
        columns = self._plan_column_names()
        if not columns:
            return [("auto_account_id", "not in", excluded.ids)]
        match_excluded = self._or_domain("placeholder", "in", excluded.ids)
        return ["!"] + match_excluded

    @api.model
    def _prefix_or_domain(self, field_name, prefixes):
        if not prefixes:
            return []
        if len(prefixes) == 1:
            return [(field_name, "=like", prefixes[0] + "%")]
        domain = ["|"] * (len(prefixes) - 1)
        for prefix in prefixes:
            domain.append((field_name, "=like", prefix + "%"))
        return domain

    @api.model
    def _class_prefix_domain(self, class_prefix):
        """Garde-fou explicite : code GL commence par `class_prefix` (`'6'` ou `'7'`)."""
        return [("general_account_id.code", "=like", class_prefix + "%")]

    def _common_period_domain(self, date_from, date_to, analytic_accounts):
        return [
            ("company_id", "=", self.company_id.id),
            ("date", ">=", date_from),
            ("date", "<=", date_to),
            *self._analytic_accounts_domain(analytic_accounts),
            *self._excluded_analytic_domain(),
        ]

    def _revenue_analytic_line_domain(self, date_from, date_to, analytic_accounts):
        """Recettes / financements — classe 7 + analytique exploitable."""
        domain = [
            *self._common_period_domain(date_from, date_to, analytic_accounts),
            (
                "general_account_id.account_type",
                "in",
                list(GLC_INCOME_ACCOUNT_TYPES),
            ),
            *self._class_prefix_domain("7"),
        ]
        for prefix in GLC_EXCLUDED_GL_ACCOUNT_PREFIXES:
            domain.append(("general_account_id.code", "not like", prefix + "%"))
        return domain

    def _expense_analytic_line_domain(self, date_from, date_to, analytic_accounts):
        """Dépenses hors masse salariale — classe 6 hors payroll + analytique exploitable."""
        domain = [
            *self._common_period_domain(date_from, date_to, analytic_accounts),
            (
                "general_account_id.account_type",
                "in",
                list(GLC_EXPENSE_ACCOUNT_TYPES),
            ),
            *self._class_prefix_domain("6"),
        ]
        for prefix in GLC_PAYROLL_ACCOUNT_PREFIXES + GLC_EXCLUDED_GL_ACCOUNT_PREFIXES:
            domain.append(("general_account_id.code", "not like", prefix + "%"))
        return domain

    def _payroll_analytic_line_domain(self, date_from, date_to, analytic_accounts):
        """Masse salariale — classe 6 payroll (631/633/641/645) + analytique exploitable."""
        domain = [
            *self._common_period_domain(date_from, date_to, analytic_accounts),
            (
                "general_account_id.account_type",
                "in",
                list(GLC_EXPENSE_ACCOUNT_TYPES),
            ),
            *self._class_prefix_domain("6"),
            *self._prefix_or_domain(
                "general_account_id.code", GLC_PAYROLL_ACCOUNT_PREFIXES
            ),
        ]
        for prefix in GLC_EXCLUDED_GL_ACCOUNT_PREFIXES:
            domain.append(("general_account_id.code", "not like", prefix + "%"))
        return domain

    @api.model
    def _signed_analytic_amount(self, line):
        """Montant exploitable toujours positif pour le cockpit."""
        return abs(line.amount)

    def _sum_lines(self, domain):
        lines = self.env["account.analytic.line"].search(domain)
        return sum(self._signed_analytic_amount(line) for line in lines)

    def _sum_revenue_realized(self, analytic_accounts, date_from, date_to):
        """Σ classe 7 + analytique sur les comptes passés (recettes ou financements)."""
        if not analytic_accounts:
            return 0.0
        return self._sum_lines(
            self._revenue_analytic_line_domain(date_from, date_to, analytic_accounts)
        )

    def _sum_expense_realized(self, analytic_accounts, date_from, date_to):
        """Σ classe 6 hors payroll + analytique sur les comptes passés (dépenses)."""
        if not analytic_accounts:
            return 0.0
        return self._sum_lines(
            self._expense_analytic_line_domain(date_from, date_to, analytic_accounts)
        )

    def _sum_payroll_realized(self, date_from, date_to, activity_account=None):
        """Σ classe 6 payroll + analytique (toutes activités par défaut)."""
        if activity_account:
            analytic_accounts = activity_account
        else:
            analytic_accounts = self._cockpit_analytic_accounts()
        if not analytic_accounts:
            return 0.0
        return self._sum_lines(
            self._payroll_analytic_line_domain(date_from, date_to, analytic_accounts)
        )

    def _ensure_budget_module(self):
        if "glc.budget.line" not in self.env:
            raise UserError(
                _(
                    "Le module dorevia_glc_budget doit être installé pour utiliser le cockpit Palier 4."
                )
            )

    def _budget_lines(self, date_from=None, date_to=None, analytic_accounts=None, line_type=None):
        self._ensure_budget_module()
        period_start, period_end = self._period_bounds()
        date_from = date_from or period_start
        date_to = date_to or period_end
        month_period_from = date(date_from.year, date_from.month, 1)
        month_period_to = date(date_to.year, date_to.month, 1)
        domain = [
            ("company_id", "=", self.company_id.id),
            ("scenario", "=", self.budget_scenario),
            ("budget_id.state", "in", ("validated", "archived")),
            ("period_date", ">=", month_period_from),
            ("period_date", "<=", month_period_to),
        ]
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
                    "Les ressources disponibles ne couvrent pas la masse salariale."
                ),
            )
        if resources < payroll + general_expenses:
            return (
                "orange",
                _(
                    "Les ressources couvrent la masse salariale, "
                    "mais pas toutes les charges de structure."
                ),
            )
        return (
            "green",
            _(
                "Les ressources couvrent les charges de structure."
            ),
        )

    def _aggregate_period(self, period_start, period_end):
        self.ensure_one()
        cockpit_accounts = self._cockpit_analytic_accounts()
        funding_accounts = self._funding_analytic_accounts()
        activity_revenue_accounts = self._activity_revenue_analytic_accounts()
        revenue_budget_accounts = self._analytic_accounts_by_codes(
            GLC_COCKPIT_ACTIVITY_REVENUE_CODES
        )
        general_budget_accounts = self._analytic_accounts_by_codes(
            (GLC_COCKPIT_GENERAL_EXPENSE_CODE,)
        )
        payroll_budget_accounts = self._analytic_accounts_by_codes(
            GLC_COCKPIT_PAYROLL_BUDGET_CODES
        )

        activity_revenue_realized = self._sum_revenue_realized(
            activity_revenue_accounts, period_start, period_end
        )
        funding_realized = self._sum_revenue_realized(
            funding_accounts, period_start, period_end
        )
        general_expenses_realized = self._sum_expense_realized(
            cockpit_accounts, period_start, period_end
        )
        payroll_realized = self._sum_payroll_realized(
            period_start,
            period_end,
            self.activity_account_id,
        )

        activity_revenue_budget = self._sum_budget(
            period_start, period_end, revenue_budget_accounts, "revenue"
        )
        funding_budget = self._sum_budget(
            period_start, period_end, funding_accounts, "funding"
        )
        general_expenses_budget = self._sum_budget(
            period_start, period_end, general_budget_accounts, "expense"
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
        for cockpit in self:
            cockpit._action_refresh_single()
        return True

    def _action_refresh_single(self):
        self.ensure_one()
        if self.activity_account_id:
            super(
                GlcCoverageCockpit,
                self.with_context(glc_cockpit_auto_refreshing=True),
            ).write({"activity_account_id": False})
        self._ensure_budget_module()
        self.line_ids.with_context(glc_cockpit_auto_refreshing=True).unlink()
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
        cockpit_accounts = self._cockpit_analytic_accounts()
        for month_start in self._month_starts_in_period():
            slice_from, slice_to = self._month_slice_bounds(month_start)
            month_end = date(
                month_start.year,
                month_start.month,
                monthrange(month_start.year, month_start.month)[1],
            )
            for account in cockpit_accounts:
                revenue_realized = self._sum_revenue_realized(
                    account, slice_from, slice_to
                )
                if self._is_funding_analytic_account(account):
                    revenue_budget = self._sum_budget(
                        month_start, month_end, account, "funding"
                    )
                elif account.code in GLC_COCKPIT_ACTIVITY_REVENUE_CODES:
                    revenue_budget = self._sum_budget(
                        month_start, month_end, account, "revenue"
                    )
                else:
                    revenue_budget = 0.0

                expense_realized = self._sum_expense_realized(
                    account, slice_from, slice_to
                )
                if account.code == GLC_COCKPIT_GENERAL_EXPENSE_CODE:
                    expense_budget = self._sum_budget(
                        month_start, month_end, account, "expense"
                    )
                else:
                    expense_budget = 0.0

                payroll_realized = self._sum_payroll_realized(
                    slice_from, slice_to, account
                )
                if account.code in GLC_COCKPIT_PAYROLL_BUDGET_CODES:
                    payroll_budget = self._sum_budget(
                        month_start, month_end, account, "expense"
                    )
                else:
                    payroll_budget = 0.0

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

                line_amounts = {
                    "revenue_realized": revenue_realized,
                    "revenue_budget": revenue_budget,
                    "expense_realized": expense_realized,
                    "expense_budget": expense_budget,
                    "payroll_realized": payroll_realized,
                    "payroll_budget": payroll_budget,
                }
                line_vals.append(
                    self._prepare_activity_line_vals(
                        month_start,
                        account,
                        line_amounts,
                    )
                )

        if line_vals:
            self.env["glc.coverage.cockpit.line"].with_context(
                glc_cockpit_auto_refreshing=True
            ).create(line_vals)

        self.with_context(glc_cockpit_auto_refreshing=True).write(
            {
                **totals,
                "salary_coverage_rate": salary_coverage_rate,
                "balance_after_payroll": balance_after_payroll,
                "balance_after_fixed": balance_after_fixed,
                "alert_status": alert_status,
                "alert_message": alert_message,
                "is_refreshed": True,
                "refresh_key": self._current_refresh_key(),
            }
        )

        return True

    @api.model
    def _empty_line_amounts(self):
        return {
            "has_amounts": False,
            "revenue_realized": 0.0,
            "revenue_budget": 0.0,
            "expense_realized": 0.0,
            "expense_budget": 0.0,
            "payroll_realized": 0.0,
            "payroll_budget": 0.0,
        }

    @api.model
    def _accumulate_line_amounts(self, target, source):
        for key in (
            "revenue_realized",
            "revenue_budget",
            "expense_realized",
            "expense_budget",
            "payroll_realized",
            "payroll_budget",
        ):
            target[key] += source[key]
        target["has_amounts"] = True

    @api.model
    def _month_key(self, month_start):
        return "%04d-%02d" % (month_start.year, month_start.month)

    @api.model
    def _month_label(self, month_start):
        return _("%(month)s %(year)s") % {
            "month": self._LONG_MONTHS[month_start.month],
            "year": month_start.year,
        }

    @api.model
    def _analytic_section_for_account(self, account):
        if self._is_funding_analytic_account(account):
            return "funding"
        plan_activites = self.env.ref(
            "dorevia_glc_analytics.analytic_plan_glc_activites",
            raise_if_not_found=False,
        )
        if plan_activites and account.plan_id == plan_activites:
            return "activity"
        return "other"

    def _prepare_activity_line_vals(self, month_start, account, amounts):
        self.ensure_one()
        section = self._analytic_section_for_account(account)
        return {
            "cockpit_id": self.id,
            "line_kind": "activity",
            "analytic_section": section,
            "period_date": month_start,
            "month_key": self._month_key(month_start),
            "month_label": self._month_label(month_start),
            "analytic_account_id": account.id,
            "activity_label": account.display_name,
            "revenue_realized": amounts["revenue_realized"],
            "revenue_budget": amounts["revenue_budget"],
            "expense_realized": amounts["expense_realized"],
            "expense_budget": amounts["expense_budget"],
            "payroll_realized": amounts["payroll_realized"],
            "payroll_budget": amounts["payroll_budget"],
            "variance_revenue": amounts["revenue_realized"] - amounts["revenue_budget"],
            "variance_payroll": amounts["payroll_realized"] - amounts["payroll_budget"],
            "variance_expense": amounts["expense_realized"] - amounts["expense_budget"],
        }

    def _prepare_total_line_vals(self, period_date, line_kind, amounts, label):
        self.ensure_one()
        if line_kind == "period_total":
            month_key = "9999-99"
            month_label = ""
        else:
            month_key = self._month_key(period_date)
            month_label = self._month_label(period_date)
        return {
            "cockpit_id": self.id,
            "line_kind": line_kind,
            "period_date": period_date,
            "month_key": month_key,
            "month_label": month_label,
            "activity_label": label,
            "revenue_realized": amounts["revenue_realized"],
            "revenue_budget": amounts["revenue_budget"],
            "expense_realized": amounts["expense_realized"],
            "expense_budget": amounts["expense_budget"],
            "payroll_realized": amounts["payroll_realized"],
            "payroll_budget": amounts["payroll_budget"],
            "variance_revenue": amounts["revenue_realized"] - amounts["revenue_budget"],
            "variance_payroll": amounts["payroll_realized"] - amounts["payroll_budget"],
            "variance_expense": amounts["expense_realized"] - amounts["expense_budget"],
        }


class GlcCoverageCockpitLine(models.TransientModel):
    _name = "glc.coverage.cockpit.line"
    _description = "Détail cockpit couverture GLC"
    _order = "month_key, analytic_section, activity_label, id"
    _rec_name = "activity_label"

    cockpit_id = fields.Many2one(
        "glc.coverage.cockpit",
        required=True,
        ondelete="cascade",
    )
    line_kind = fields.Selection(
        string="Type de ligne",
        selection=[
            ("activity", "Activité"),
            ("month_total", "Total mensuel"),
            ("period_total", "Total période"),
        ],
        required=True,
        default="activity",
    )
    period_date = fields.Date(string="Mois", required=True)
    month_key = fields.Char(string="Clé mois", required=True, index=True)
    month_label = fields.Char(string="Libellé mois")
    analytic_account_id = fields.Many2one(
        "account.analytic.account",
        string="Activité",
    )
    activity_label = fields.Char(string="Libellé activité")
    analytic_section = fields.Selection(
        string="Famille analytique",
        selection=[
            ("activity", "Activités"),
            ("funding", "Financements"),
            ("other", "Autres"),
        ],
        required=True,
        default="activity",
    )
    currency_id = fields.Many2one(
        related="cockpit_id.currency_id",
        store=True,
        readonly=True,
    )
    revenue_realized = fields.Monetary(
        string="Recettes réel",
        currency_field="currency_id",
    )
    revenue_budget = fields.Monetary(
        string="Recettes budget",
        currency_field="currency_id",
    )
    expense_realized = fields.Monetary(
        string="Frais gén. réel",
        currency_field="currency_id",
    )
    expense_budget = fields.Monetary(
        string="Frais gén. budget",
        currency_field="currency_id",
    )
    payroll_realized = fields.Monetary(
        string="Masse sal. réel",
        currency_field="currency_id",
    )
    payroll_budget = fields.Monetary(
        string="Masse sal. budget",
        currency_field="currency_id",
    )
    variance_revenue = fields.Monetary(
        string="Écart recettes",
        currency_field="currency_id",
    )
    variance_payroll = fields.Monetary(
        string="Écart masse sal.",
        currency_field="currency_id",
    )
    variance_expense = fields.Monetary(
        string="Écart frais gén.",
        currency_field="currency_id",
    )
    performance_realized = fields.Monetary(
        string="Performance réel",
        currency_field="currency_id",
        compute="_compute_performance",
    )
    performance_budget = fields.Monetary(
        string="Performance budget",
        currency_field="currency_id",
        compute="_compute_performance",
    )
    variance_performance = fields.Monetary(
        string="Écart performance",
        currency_field="currency_id",
        compute="_compute_performance",
    )

    @api.depends(
        "revenue_realized",
        "revenue_budget",
        "payroll_realized",
        "payroll_budget",
        "expense_realized",
        "expense_budget",
    )
    def _compute_performance(self):
        for line in self:
            line.performance_realized = (
                line.revenue_realized
                - line.payroll_realized
                - line.expense_realized
            )
            line.performance_budget = (
                line.revenue_budget
                - line.payroll_budget
                - line.expense_budget
            )
            line.variance_performance = (
                line.performance_realized - line.performance_budget
            )

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.context.get("glc_cockpit_auto_refreshing"):
            return self.browse()
        cockpit_model = self.env["glc.coverage.cockpit"]
        cleaned_vals_list = []
        for vals in vals_list:
            if not vals.get("cockpit_id"):
                continue
            if not vals.get("analytic_section"):
                account = self.env["account.analytic.account"].browse(
                    vals.get("analytic_account_id")
                )
                if account:
                    vals["analytic_section"] = cockpit_model._analytic_section_for_account(
                        account
                    )
                else:
                    vals["analytic_section"] = "activity"
            cleaned_vals_list.append(vals)
        if not cleaned_vals_list:
            return self.browse()
        return super().create(cleaned_vals_list)

    def write(self, vals):
        if not self.env.context.get("glc_cockpit_auto_refreshing"):
            return True
        return super().write(vals)

    def unlink(self):
        if not self.env.context.get("glc_cockpit_auto_refreshing"):
            return True
        return super().unlink()
