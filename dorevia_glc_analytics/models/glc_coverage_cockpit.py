# -*- coding: utf-8 -*-

from calendar import monthrange
from collections import defaultdict
from datetime import date

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError

from .glc_constants import (
    GLC_COCKPIT_AUTO_REFRESH_CTX,
    GLC_COCKPIT_FUNDING_CODES,
    GLC_COCKPIT_SALARY_EXCLUDED_ANALYTIC_CODES,
    GLC_EXCLUDED_GL_ACCOUNT_PREFIXES,
    GLC_EXPENSE_ACCOUNT_TYPES,
    GLC_INCOME_ACCOUNT_TYPES,
    GLC_INTERNAL_TRANSFER_GL_PREFIXES,
    GLC_LEGACY_ANALYTIC_CODES,
    GLC_PAYROLL_ACCOUNT_PREFIXES,
)


def _glc_cockpit_require_auto_refresh(env):
    if not env.context.get(GLC_COCKPIT_AUTO_REFRESH_CTX):
        raise AccessError(
            _(
                "Les lignes calculées du contrôle de gestion ne peuvent être "
                "modifiées que lors du recalcul automatique."
            )
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
        string="Axe analytique",
        check_company=True,
        domain=lambda self: [
            ("plan_id", "=", self.env.ref("dorevia_glc_analytics.analytic_plan_glc_activites").id),
            "|",
            ("company_id", "=", False),
            ("company_id", "in", self.env.companies.ids),
        ],
    )
    reference_bank_journal_id = fields.Many2one(
        "account.journal",
        string="Compte bancaire de référence",
        check_company=True,
        domain="[('type', '=', 'bank'), ('company_id', '=', company_id)]",
        default=lambda self: self._default_reference_bank_journal_id(),
        help="Point de vue trésorerie du cockpit — n'affecte pas les KPI d'exploitation.",
    )
    reference_bank_account_id = fields.Many2one(
        "account.account",
        string="Compte 512 de référence",
        compute="_compute_reference_bank_account_id",
        store=True,
        readonly=True,
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
        string="Recettes d'activité",
        readonly=True,
        currency_field="currency_id",
    )
    funding_realized = fields.Monetary(
        string="Financements",
        readonly=True,
        currency_field="currency_id",
    )
    resources_realized = fields.Monetary(
        string="Ressources",
        readonly=True,
        currency_field="currency_id",
    )
    payroll_realized = fields.Monetary(
        string="Cumul RH",
        readonly=True,
        currency_field="currency_id",
    )
    general_expenses_realized = fields.Monetary(
        string="Dépenses",
        readonly=True,
        currency_field="currency_id",
    )
    fixed_charges_realized = fields.Monetary(
        string="Charges de structure",
        readonly=True,
        currency_field="currency_id",
        help="Cumul RH + dépenses.",
    )

    salary_coverage_rate = fields.Float(
        string="Couverture masse salariale (%)",
        digits=(16, 2),
        readonly=True,
        help="Lecture intermédiaire : ressources / cumul RH.",
    )
    revenue_eligible_line_count = fields.Integer(
        string="Ressources éligibles (lignes)",
        readonly=True,
    )
    revenue_invoiced_line_count = fields.Integer(
        string="Ressources facturées (lignes)",
        readonly=True,
    )
    revenue_eligible_amount = fields.Integer(
        string="Ressources éligibles (lignes, alias)",
        readonly=True,
        help="Alias transitoire : utiliser revenue_eligible_line_count.",
    )
    revenue_invoiced_amount = fields.Integer(
        string="Ressources facturées (lignes, alias)",
        readonly=True,
        help="Alias transitoire : utiliser revenue_invoiced_line_count.",
    )
    revenue_invoiced_rate = fields.Float(
        string="Ressources facturées (%)",
        digits=(16, 2),
        readonly=True,
    )
    expense_eligible_line_count = fields.Integer(
        string="Dépenses éligibles (lignes)",
        readonly=True,
    )
    expense_invoiced_line_count = fields.Integer(
        string="Dépenses facturées (lignes)",
        readonly=True,
    )
    expense_eligible_amount = fields.Integer(
        string="Dépenses éligibles (lignes, alias)",
        readonly=True,
        help="Alias transitoire : utiliser expense_eligible_line_count.",
    )
    expense_invoiced_amount = fields.Integer(
        string="Dépenses facturées (lignes, alias)",
        readonly=True,
        help="Alias transitoire : utiliser expense_invoiced_line_count.",
    )
    expense_invoiced_rate = fields.Float(
        string="Dépenses facturées (%)",
        digits=(16, 2),
        readonly=True,
    )
    balance_after_payroll = fields.Monetary(
        string="Solde après cumul RH",
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
    treasury_inflow = fields.Monetary(
        string="Entrées trésorerie",
        readonly=True,
        currency_field="currency_id",
    )
    treasury_outflow = fields.Monetary(
        string="Sorties trésorerie",
        readonly=True,
        currency_field="currency_id",
    )
    treasury_internal_inflow = fields.Monetary(
        string="Virements internes (entrées)",
        readonly=True,
        currency_field="currency_id",
    )
    treasury_internal_outflow = fields.Monetary(
        string="Virements internes (sorties)",
        readonly=True,
        currency_field="currency_id",
    )
    treasury_net = fields.Monetary(
        string="Solde trésorerie période",
        readonly=True,
        currency_field="currency_id",
    )
    treasury_has_data = fields.Boolean(
        string="Mouvements trésorerie sur la période",
        readonly=True,
    )
    treasury_line_ids = fields.One2many(
        "glc.coverage.cockpit.treasury.line",
        "cockpit_id",
        string="Virements internes par axe",
        readonly=True,
    )

    _FILTER_FIELDS = frozenset(
        {
            "company_id",
            "date_from",
            "date_to",
            "activity_account_id",
            "reference_bank_journal_id",
        }
    )

    @api.model
    def _default_reference_bank_journal_id(self):
        company = self.env.company
        if company.glc_default_bank_journal_id:
            return company.glc_default_bank_journal_id.id
        journal = self.env["account.journal"].search(
            [
                ("type", "=", "bank"),
                ("company_id", "=", company.id),
            ],
            limit=1,
        )
        return journal.id if journal else False

    @api.model
    def _journal_bank_account(self, journal):
        if not journal:
            return self.env["account.account"]
        return (
            journal.default_account_id
            or journal.payment_debit_account_id
            or journal.payment_credit_account_id
        )

    @api.depends("reference_bank_journal_id")
    def _compute_reference_bank_account_id(self):
        for cockpit in self:
            cockpit.reference_bank_account_id = cockpit._journal_bank_account(
                cockpit.reference_bank_journal_id
            )

    def _resolve_reference_bank_account(self):
        self.ensure_one()
        return self._journal_bank_account(self.reference_bank_journal_id)

    @api.model
    def _default_date_range(self, reference=None):
        """3 derniers mois calendaires incluant le mois courant, fin = aujourd'hui."""
        today = reference or fields.Date.context_today(self)
        month = today.month - 2
        year = today.year
        if month <= 0:
            month += 12
            year -= 1
        date_from = date(year, month, 1)
        date_to = today
        return date_from, date_to

    @api.model
    def _default_open_values(self):
        date_from, date_to = self._default_date_range()
        return {
            "company_id": self.env.company.id,
            "date_from": date_from,
            "date_to": date_to,
            "activity_account_id": False,
            "reference_bank_journal_id": self._default_reference_bank_journal_id(),
        }

    @api.model
    def _domain_for_open_values(self, values, include_dates=True):
        field_names = [
            "company_id",
            "activity_account_id",
            "reference_bank_journal_id",
        ]
        if include_dates:
            field_names = [
                "company_id",
                "date_from",
                "date_to",
                *field_names[1:],
            ]
        domain = []
        for field_name in field_names:
            value = values[field_name]
            if field_name in ("activity_account_id", "reference_bank_journal_id") and not value:
                domain.append((field_name, "=", False))
            else:
                domain.append((field_name, "=", value))
        return domain

    @api.model
    def action_open_default_cockpit(self):
        date_from, date_to = self._default_date_range()
        values = self._default_open_values()
        cockpit = self.search(
            self._domain_for_open_values(values, include_dates=False),
            limit=1,
            order="id desc",
        )
        if cockpit:
            updates = {}
            if cockpit.date_from != date_from:
                updates["date_from"] = date_from
            if cockpit.date_to != date_to:
                updates["date_to"] = date_to
            if updates:
                cockpit.write(updates)
        else:
            cockpit = self.create(values)
        cockpit.with_context(glc_cockpit_auto_refreshing=True).action_refresh()
        return {
            "type": "ir.actions.act_window",
            "name": _("Contrôle de gestion"),
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
        return "%s|%s|%s|%s|%s" % (
            self.company_id.id or "",
            self.date_from or "",
            self.date_to or "",
            self.activity_account_id.id or "",
            self.reference_bank_journal_id.id or "",
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

    @api.model
    def _format_period_date(self, value):
        month = self._LONG_MONTHS[value.month].lower()
        return "%(day)s %(month)s %(year)s" % {
            "day": value.day,
            "month": month,
            "year": value.year,
        }

    @api.depends("date_from", "date_to")
    def _compute_period_labels(self):
        for cockpit in self:
            if cockpit.date_from and cockpit.date_to:
                start = cockpit._format_period_date(cockpit.date_from)
                end = cockpit._format_period_date(cockpit.date_to)
                cockpit.period_range_label = _("%(start)s → %(end)s", start=start, end=end)
            else:
                cockpit.period_range_label = False

    @api.depends("date_from", "date_to", "activity_account_id")
    def _compute_display_title(self):
        for cockpit in self:
            if not cockpit.date_from or not cockpit.date_to:
                cockpit.display_title = _("Cockpit GLC")
                continue
            if cockpit._is_full_single_calendar_month():
                period = cockpit._LONG_MONTHS[cockpit.date_from.month]
            else:
                start = cockpit._format_short_date(cockpit.date_from)
                end = cockpit._format_short_date(cockpit.date_to)
                period = _("%(start)s → %(end)s", start=start, end=end)
            title = _(
                "Cockpit GLC · %(year)s · %(period)s",
                year=cockpit.date_from.year,
                period=period,
            )
            if cockpit.activity_account_id:
                axis = self._activity_business_label(cockpit.activity_account_id)
                title = _("%(title)s · %(axis)s", title=title, axis=axis)
            cockpit.display_title = title

    @api.depends("line_ids", "line_ids.line_kind")
    def _compute_detail_line_count(self):
        for cockpit in self:
            cockpit.detail_line_count = len(
                cockpit.line_ids.filtered(lambda line: line.line_kind == "activity")
            )

    @api.onchange("company_id")
    def _onchange_company_id_reference_bank(self):
        if self.company_id:
            self.reference_bank_journal_id = self.with_company(
                self.company_id
            )._default_reference_bank_journal_id()

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
        """Compte analytique de financement (axe ressource — identification par code)."""
        return bool(account and account.code in GLC_COCKPIT_FUNDING_CODES)

    def _cockpit_analytic_plan(self):
        return self.env.ref(
            "dorevia_glc_analytics.analytic_plan_glc_activites",
            raise_if_not_found=False,
        )

    def _cockpit_analytic_accounts(self):
        """Comptes analytiques exploitables cockpit sur le plan GLC officiel."""
        self.ensure_one()
        if self.activity_account_id:
            return self.activity_account_id
        plan = self._cockpit_analytic_plan()
        if not plan:
            return self.env["account.analytic.account"]
        excluded = self._excluded_analytic_accounts()
        domain = [
            ("plan_id", "=", plan.id),
            ("company_id", "in", [False, self.company_id.id]),
        ]
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
        """Alias rétrocompat — périmètre du plan analytique GLC officiel."""
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

    def _sum_lines_matching(self, domain, predicate):
        lines = self.env["account.analytic.line"].search(domain)
        return sum(
            self._signed_analytic_amount(line)
            for line in lines
            if predicate(line)
        )

    def _sum_lines_paid(self, domain):
        """Σ lignes analytiques dont la pièce source est considérée payée."""
        return self._sum_lines_matching(
            domain, self._glc_analytic_line_is_paid_for_cockpit
        )

    def _analytic_account_ids_from_line(self, line, eligible_ids):
        account_ids = set()
        for column in self._plan_column_names():
            account = line[column]
            if account and account.id in eligible_ids:
                account_ids.add(account.id)
        return account_ids

    def _sum_lines_by_account_month(self, domain, analytic_accounts, predicate=None):
        """Pré-agrège les montants par mois et axe pour éviter les recherches N×M."""
        result = defaultdict(float)
        if not analytic_accounts:
            return result
        eligible_ids = set(analytic_accounts.ids)
        lines = self.env["account.analytic.line"].search(domain)
        for line in lines:
            if predicate and not predicate(line):
                continue
            month_start = date(line.date.year, line.date.month, 1)
            amount = self._signed_analytic_amount(line)
            for account_id in self._analytic_account_ids_from_line(line, eligible_ids):
                result[(month_start, account_id)] += amount
        return result

    def _period_activity_amount_maps(self, date_from, date_to, cockpit_accounts):
        return {
            "revenue_realized": self._sum_lines_by_account_month(
                self._revenue_analytic_line_domain(
                    date_from, date_to, cockpit_accounts
                ),
                cockpit_accounts,
            ),
            "revenue_realized_paid": self._sum_lines_by_account_month(
                self._revenue_analytic_line_domain(
                    date_from, date_to, cockpit_accounts
                ),
                cockpit_accounts,
                predicate=self._glc_analytic_line_is_paid_for_cockpit,
            ),
            "expense_realized": self._sum_lines_by_account_month(
                self._expense_analytic_line_domain(
                    date_from, date_to, cockpit_accounts
                ),
                cockpit_accounts,
            ),
            "expense_realized_paid": self._sum_lines_by_account_month(
                self._expense_analytic_line_domain(
                    date_from, date_to, cockpit_accounts
                ),
                cockpit_accounts,
                predicate=self._glc_analytic_line_is_paid_for_cockpit,
            ),
            "payroll_realized": self._sum_lines_by_account_month(
                self._payroll_analytic_line_domain(
                    date_from, date_to, cockpit_accounts
                ),
                cockpit_accounts,
            ),
            "payroll_realized_paid": self._sum_lines_by_account_month(
                self._payroll_analytic_line_domain(
                    date_from, date_to, cockpit_accounts
                ),
                cockpit_accounts,
                predicate=self._glc_analytic_line_is_paid_for_cockpit,
            ),
        }

    def _sum_revenue_realized(self, analytic_accounts, date_from, date_to):
        """Σ classe 7 + analytique sur les comptes passés (recettes ou financements)."""
        if not analytic_accounts:
            return 0.0
        return self._sum_lines(
            self._revenue_analytic_line_domain(date_from, date_to, analytic_accounts)
        )

    def _sum_revenue_realized_paid(self, analytic_accounts, date_from, date_to):
        if not analytic_accounts:
            return 0.0
        return self._sum_lines_paid(
            self._revenue_analytic_line_domain(date_from, date_to, analytic_accounts)
        )

    def _sum_expense_realized(self, analytic_accounts, date_from, date_to):
        """Σ classe 6 hors payroll + analytique sur les comptes passés (dépenses)."""
        if not analytic_accounts:
            return 0.0
        return self._sum_lines(
            self._expense_analytic_line_domain(date_from, date_to, analytic_accounts)
        )

    def _count_lines(self, domain):
        return self.env["account.analytic.line"].search_count(domain)

    def _count_lines_matching(self, domain, predicate):
        lines = self.env["account.analytic.line"].search(domain)
        return sum(1 for line in lines if predicate(line))

    def _count_internal_transfer_revenue_lines(
        self, analytic_accounts, date_from, date_to, buckets=None
    ):
        """Chaque bucket 580 avec entrée = 1 ligne ressource éligible (hors facture)."""
        self.ensure_one()
        if not analytic_accounts:
            return 0
        eligible_ids = set(analytic_accounts.ids)
        count = 0
        if buckets is None:
            buckets = self._aggregate_treasury_internal_buckets(date_from, date_to)
        for bucket in buckets:
            if bucket["internal_inflow"] < 0.005:
                continue
            acc = bucket["analytic_account"]
            if acc and acc.id in eligible_ids:
                count += 1
        return count

    def _count_internal_transfer_expense_lines(
        self, analytic_accounts, date_from, date_to, buckets=None
    ):
        """Chaque bucket 580 avec sortie = 1 ligne dépense éligible (hors facture)."""
        self.ensure_one()
        if not analytic_accounts:
            return 0
        eligible_ids = set(analytic_accounts.ids)
        count = 0
        if buckets is None:
            buckets = self._aggregate_treasury_internal_buckets(date_from, date_to)
        for bucket in buckets:
            if bucket["internal_outflow"] < 0.005:
                continue
            acc = bucket["analytic_account"]
            if acc and acc.id in eligible_ids:
                count += 1
        return count

    def _count_revenue_eligible_lines(
        self, analytic_accounts, date_from, date_to, buckets=None
    ):
        if not analytic_accounts:
            return 0
        return self._count_lines(
            self._revenue_analytic_line_domain(date_from, date_to, analytic_accounts)
        ) + self._count_internal_transfer_revenue_lines(
            analytic_accounts, date_from, date_to, buckets=buckets
        )

    def _count_revenue_invoiced_lines(self, analytic_accounts, date_from, date_to):
        if not analytic_accounts:
            return 0
        return self._count_lines_matching(
            self._revenue_analytic_line_domain(date_from, date_to, analytic_accounts),
            self._glc_analytic_line_is_customer_invoice_for_cockpit,
        )

    def _count_expense_eligible_lines(
        self, analytic_accounts, date_from, date_to, buckets=None
    ):
        if not analytic_accounts:
            return 0
        return self._count_lines(
            self._expense_analytic_line_domain(date_from, date_to, analytic_accounts)
        ) + self._count_internal_transfer_expense_lines(
            analytic_accounts, date_from, date_to, buckets=buckets
        )

    def _count_expense_invoiced_lines(self, analytic_accounts, date_from, date_to):
        if not analytic_accounts:
            return 0
        return self._count_lines_matching(
            self._expense_analytic_line_domain(date_from, date_to, analytic_accounts),
            self._glc_analytic_line_is_supplier_invoice_for_cockpit,
        )

    def _document_quality_rate(self, invoiced_count, eligible_count):
        if eligible_count <= 0:
            return 0.0
        return (invoiced_count / eligible_count) * 100.0

    def _aggregate_document_quality(
        self, period_start, period_end, internal_buckets=None
    ):
        """KPI Synthèse — part des lignes ressource / dépense issue d'une facture."""
        self.ensure_one()
        cockpit_accounts = self._cockpit_analytic_accounts()
        revenue_eligible = self._count_revenue_eligible_lines(
            cockpit_accounts, period_start, period_end, buckets=internal_buckets
        )
        revenue_invoiced = self._count_revenue_invoiced_lines(
            cockpit_accounts, period_start, period_end
        )
        expense_eligible = self._count_expense_eligible_lines(
            cockpit_accounts, period_start, period_end, buckets=internal_buckets
        )
        expense_invoiced = self._count_expense_invoiced_lines(
            cockpit_accounts, period_start, period_end
        )
        return {
            "revenue_eligible_line_count": revenue_eligible,
            "revenue_invoiced_line_count": revenue_invoiced,
            "revenue_eligible_amount": revenue_eligible,
            "revenue_invoiced_amount": revenue_invoiced,
            "revenue_invoiced_rate": self._document_quality_rate(
                revenue_invoiced, revenue_eligible
            ),
            "expense_eligible_line_count": expense_eligible,
            "expense_invoiced_line_count": expense_invoiced,
            "expense_eligible_amount": expense_eligible,
            "expense_invoiced_amount": expense_invoiced,
            "expense_invoiced_rate": self._document_quality_rate(
                expense_invoiced, expense_eligible
            ),
        }

    def _sum_expense_realized_paid(self, analytic_accounts, date_from, date_to):
        if not analytic_accounts:
            return 0.0
        return self._sum_lines_paid(
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

    def _sum_payroll_realized_paid(self, date_from, date_to, activity_account=None):
        if activity_account:
            analytic_accounts = activity_account
        else:
            analytic_accounts = self._cockpit_analytic_accounts()
        if not analytic_accounts:
            return 0.0
        return self._sum_lines_paid(
            self._payroll_analytic_line_domain(date_from, date_to, analytic_accounts)
        )

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

    @api.model
    def _is_cash_account(self, account):
        if not account:
            return False
        if account.account_type == "asset_cash":
            return True
        return (account.code or "").startswith("53")

    @api.model
    def _is_internal_transfer_gl_account(self, account):
        code = account.code or ""
        return any(code.startswith(prefix) for prefix in GLC_INTERNAL_TRANSFER_GL_PREFIXES)

    @api.model
    def _analytic_accounts_from_move_line(self, line):
        """Comptes analytiques portés par une ligne comptable (distribution ou AAL)."""
        Account = self.env["account.analytic.account"]
        accounts = Account
        distribution = line.analytic_distribution or {}
        if distribution:
            account_ids = [int(account_id) for account_id in distribution.keys()]
            accounts |= Account.browse(account_ids).exists()
        analytic_lines = self.env["account.analytic.line"].search(
            [("move_line_id", "=", line.id)]
        )
        accounts |= analytic_lines.mapped("account_id")
        for column in self._plan_column_names():
            accounts |= analytic_lines.mapped(column)
        return accounts

    def _internal_transfer_qualifications_weighted(self, move):
        """Qualifications (axe analytique, compte 580, poids) d'un virement interne."""
        self.ensure_one()
        items = []
        transfer_lines = move.line_ids.filtered(
            lambda line: self._is_internal_transfer_gl_account(line.account_id)
        )
        for line in transfer_lines:
            transfer_code = line.account_id.code or "580"
            distribution = line.analytic_distribution or {}
            if distribution:
                total = sum(distribution.values()) or 100.0
                for account_id, percent in distribution.items():
                    account = self.env["account.analytic.account"].browse(
                        int(account_id)
                    ).exists()
                    if account:
                        items.append((account, transfer_code, percent / total))
                continue
            accounts = self._analytic_accounts_from_move_line(line)
            if accounts:
                weight = 1.0 / len(accounts)
                for account in accounts:
                    items.append((account, transfer_code, weight))
        return items

    def _aggregate_treasury_internal_buckets(self, date_from, date_to):
        """Ventile les virements internes par axe analytique, compte 580 et période."""
        self.ensure_one()
        buckets = {}
        if not self._resolve_reference_bank_account():
            return []
        bank_lines = self.env["account.move.line"].search(
            self._treasury_move_line_domain(date_from, date_to)
        )
        for bank_line in bank_lines:
            if not self._is_internal_transfer_move(bank_line.move_id):
                continue
            qualifications = self._internal_transfer_qualifications_weighted(
                bank_line.move_id
            )
            if not qualifications:
                transfer_code = "580"
                transfer_lines = bank_line.move_id.line_ids.filtered(
                    lambda line: self._is_internal_transfer_gl_account(line.account_id)
                )
                if transfer_lines:
                    transfer_code = transfer_lines[0].account_id.code or "580"
                qualifications = [
                    (self.env["account.analytic.account"], transfer_code, 1.0)
                ]
            for analytic_account, transfer_code, weight in qualifications:
                key = (analytic_account.id or 0, transfer_code)
                bucket = buckets.setdefault(
                    key,
                    {
                        "analytic_account": analytic_account,
                        "transfer_gl_account_code": transfer_code,
                        "internal_inflow": 0.0,
                        "internal_outflow": 0.0,
                    },
                )
                if bank_line.debit:
                    bucket["internal_inflow"] += bank_line.debit * weight
                if bank_line.credit:
                    bucket["internal_outflow"] += bank_line.credit * weight
        return list(buckets.values())

    def _aggregate_treasury_internal_lines(self, date_from, date_to):
        """Ventile les virements internes par axe analytique et compte 580."""
        return self._aggregate_treasury_internal_buckets(date_from, date_to)

    def _internal_transfer_amounts_for_account(
        self, account, date_from, date_to, buckets=None
    ):
        """Entrées / sorties virement interne pour un axe sur une tranche de dates."""
        self.ensure_one()
        target_id = account.id if account else 0
        inflow = outflow = 0.0
        if buckets is None:
            buckets = self._aggregate_treasury_internal_buckets(date_from, date_to)
        for bucket in buckets:
            analytic_account = bucket["analytic_account"]
            if (analytic_account.id or 0) != target_id:
                continue
            inflow += bucket["internal_inflow"]
            outflow += bucket["internal_outflow"]
        return inflow, outflow

    def _is_internal_transfer_move(self, move):
        """Virement interne : trésorerie ↔ trésorerie ou compte 580."""
        if any(
            self._is_internal_transfer_gl_account(line.account_id)
            for line in move.line_ids
        ):
            return True
        cash_lines = move.line_ids.filtered(
            lambda line: self._is_cash_account(line.account_id)
        )
        account_ids = set(cash_lines.mapped("account_id.id"))
        return len(cash_lines) >= 2 and len(account_ids) >= 2

    def _treasury_move_line_domain(self, date_from, date_to):
        self.ensure_one()
        account = self._resolve_reference_bank_account()
        if not account:
            return [(0, "=", 1)]
        return [
            ("company_id", "=", self.company_id.id),
            ("parent_state", "=", "posted"),
            ("date", ">=", date_from),
            ("date", "<=", date_to),
            ("account_id", "=", account.id),
        ]

    def _aggregate_treasury(self, date_from, date_to):
        """Lecture trésorerie S1 — account.move.line sur le compte 512 de référence."""
        self.ensure_one()
        empty = {
            "treasury_inflow": 0.0,
            "treasury_outflow": 0.0,
            "treasury_internal_inflow": 0.0,
            "treasury_internal_outflow": 0.0,
            "treasury_net": 0.0,
            "treasury_has_data": False,
        }
        if not self._resolve_reference_bank_account():
            return empty
        lines = self.env["account.move.line"].search(
            self._treasury_move_line_domain(date_from, date_to)
        )
        inflow = outflow = internal_in = internal_out = 0.0
        for line in lines:
            is_internal = self._is_internal_transfer_move(line.move_id)
            if line.debit:
                inflow += line.debit
                if is_internal:
                    internal_in += line.debit
            if line.credit:
                outflow += line.credit
                if is_internal:
                    internal_out += line.credit
        return {
            "treasury_inflow": inflow,
            "treasury_outflow": outflow,
            "treasury_internal_inflow": internal_in,
            "treasury_internal_outflow": internal_out,
            "treasury_net": inflow - outflow,
            "treasury_has_data": bool(lines),
        }

    def _sum_internal_transfer_inflow(
        self, analytic_accounts, date_from, date_to, buckets=None
    ):
        """Entrées virement interne 580 qualifiées → recette cockpit."""
        self.ensure_one()
        if not analytic_accounts:
            return 0.0
        eligible_ids = set(analytic_accounts.ids)
        if buckets is None:
            buckets = self._aggregate_treasury_internal_buckets(date_from, date_to)
        return sum(
            bucket["internal_inflow"]
            for bucket in buckets
            if bucket["analytic_account"] and bucket["analytic_account"].id in eligible_ids
        )

    def _sum_internal_transfer_outflow(
        self, analytic_accounts, date_from, date_to, buckets=None
    ):
        """Sorties virement interne 580 qualifiées → dépense cockpit."""
        self.ensure_one()
        if not analytic_accounts:
            return 0.0
        eligible_ids = set(analytic_accounts.ids)
        if buckets is None:
            buckets = self._aggregate_treasury_internal_buckets(date_from, date_to)
        return sum(
            bucket["internal_outflow"]
            for bucket in buckets
            if bucket["analytic_account"] and bucket["analytic_account"].id in eligible_ids
        )

    def _aggregate_period(self, period_start, period_end, internal_buckets=None):
        self.ensure_one()
        cockpit_accounts = self._cockpit_analytic_accounts()
        funding_accounts = self._funding_analytic_accounts()
        activity_revenue_accounts = self._activity_revenue_analytic_accounts()
        if internal_buckets is None:
            internal_buckets = self._aggregate_treasury_internal_buckets(
                period_start, period_end
            )

        activity_revenue_realized = self._sum_revenue_realized(
            activity_revenue_accounts, period_start, period_end
        ) + self._sum_internal_transfer_inflow(
            activity_revenue_accounts,
            period_start,
            period_end,
            buckets=internal_buckets,
        )
        funding_realized = self._sum_revenue_realized(
            funding_accounts, period_start, period_end
        ) + self._sum_internal_transfer_inflow(
            funding_accounts,
            period_start,
            period_end,
            buckets=internal_buckets,
        )
        general_expenses_realized = self._sum_expense_realized(
            cockpit_accounts, period_start, period_end
        ) + self._sum_internal_transfer_outflow(
            cockpit_accounts,
            period_start,
            period_end,
            buckets=internal_buckets,
        )
        payroll_realized = self._sum_payroll_realized(
            period_start,
            period_end,
            self.activity_account_id,
        )

        resources_realized = activity_revenue_realized + funding_realized
        fixed_charges_realized = payroll_realized + general_expenses_realized

        return {
            "activity_revenue_realized": activity_revenue_realized,
            "funding_realized": funding_realized,
            "resources_realized": resources_realized,
            "payroll_realized": payroll_realized,
            "general_expenses_realized": general_expenses_realized,
            "fixed_charges_realized": fixed_charges_realized,
        }

    def action_refresh(self):
        for cockpit in self:
            cockpit._action_refresh_single()
        return True

    def _action_refresh_single(self):
        self.ensure_one()
        refresh_ctx = {GLC_COCKPIT_AUTO_REFRESH_CTX: True}
        self.line_ids.sudo().with_context(**refresh_ctx).unlink()
        self.treasury_line_ids.sudo().with_context(**refresh_ctx).unlink()
        date_from, date_to = self._period_bounds()
        period_internal_buckets = self._aggregate_treasury_internal_buckets(
            date_from, date_to
        )
        totals = self._aggregate_period(
            date_from, date_to, internal_buckets=period_internal_buckets
        )
        treasury = self._aggregate_treasury(date_from, date_to)
        document_quality = self._aggregate_document_quality(
            date_from, date_to, internal_buckets=period_internal_buckets
        )
        treasury_internal_lines = period_internal_buckets

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
        activity_amount_maps = self._period_activity_amount_maps(
            date_from, date_to, cockpit_accounts
        )
        for month_start in self._month_starts_in_period():
            slice_from, slice_to = self._month_slice_bounds(month_start)
            monthly_internal_buckets = self._aggregate_treasury_internal_buckets(
                slice_from, slice_to
            )
            for account in cockpit_accounts:
                amount_key = (month_start, account.id)
                revenue_realized = activity_amount_maps["revenue_realized"][
                    amount_key
                ]
                revenue_realized_paid = activity_amount_maps[
                    "revenue_realized_paid"
                ][amount_key]
                expense_realized = activity_amount_maps["expense_realized"][
                    amount_key
                ]
                expense_realized_paid = activity_amount_maps[
                    "expense_realized_paid"
                ][amount_key]
                payroll_realized = activity_amount_maps["payroll_realized"][
                    amount_key
                ]
                payroll_realized_paid = activity_amount_maps[
                    "payroll_realized_paid"
                ][amount_key]

                internal_inflow, internal_outflow = (
                    self._internal_transfer_amounts_for_account(
                        account,
                        slice_from,
                        slice_to,
                        buckets=monthly_internal_buckets,
                    )
                )
                revenue_realized += internal_inflow
                expense_realized += internal_outflow
                revenue_realized_paid += internal_inflow
                expense_realized_paid += internal_outflow

                if not any(
                    (
                        revenue_realized,
                        expense_realized,
                        payroll_realized,
                        revenue_realized_paid,
                        expense_realized_paid,
                        payroll_realized_paid,
                    )
                ):
                    continue

                line_amounts = {
                    "revenue_realized": revenue_realized,
                    "revenue_realized_paid": revenue_realized_paid,
                    "expense_realized": expense_realized,
                    "expense_realized_paid": expense_realized_paid,
                    "payroll_realized": payroll_realized,
                    "payroll_realized_paid": payroll_realized_paid,
                }
                line_vals.append(
                    self._prepare_activity_line_vals(
                        month_start,
                        account,
                        line_amounts,
                    )
                )

        if line_vals:
            self.env["glc.coverage.cockpit.line"].sudo().with_context(
                **refresh_ctx
            ).create(line_vals)

        treasury_line_vals = []
        for bucket in treasury_internal_lines:
            analytic_account = bucket["analytic_account"]
            treasury_line_vals.append(
                {
                    "cockpit_id": self.id,
                    "analytic_account_id": analytic_account.id or False,
                    "activity_label": analytic_account
                    and self._activity_business_label(analytic_account)
                    or _("Non qualifié"),
                    "transfer_gl_account_code": bucket["transfer_gl_account_code"],
                    "internal_inflow": bucket["internal_inflow"],
                    "internal_outflow": bucket["internal_outflow"],
                }
            )
        if treasury_line_vals:
            self.env["glc.coverage.cockpit.treasury.line"].sudo().with_context(
                **refresh_ctx
            ).create(treasury_line_vals)

        self.with_context(**refresh_ctx).write(
            {
                **totals,
                **treasury,
                **document_quality,
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
            "expense_realized": 0.0,
            "payroll_realized": 0.0,
        }

    @api.model
    def _accumulate_line_amounts(self, target, source):
        for key in (
            "revenue_realized",
            "expense_realized",
            "payroll_realized",
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

    @api.model
    def _strip_analytic_code_prefix(self, label):
        label = (label or "").strip()
        if label.startswith("[") and "]" in label:
            return label.split("]", 1)[1].strip() or label
        return label

    @api.model
    def _activity_business_label(self, account):
        """Libellé MOA : nom métier seul (sans préfixe [CODE])."""
        name = self._strip_analytic_code_prefix(account.name)
        if name and not name.startswith("["):
            return name
        return self._strip_analytic_code_prefix(account.display_name)

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
            "activity_label": self._activity_business_label(account),
            "revenue_realized": amounts["revenue_realized"],
            "revenue_realized_paid": amounts.get("revenue_realized_paid", 0.0),
            "expense_realized": amounts["expense_realized"],
            "expense_realized_paid": amounts.get("expense_realized_paid", 0.0),
            "payroll_realized": amounts["payroll_realized"],
            "payroll_realized_paid": amounts.get("payroll_realized_paid", 0.0),
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
            "expense_realized": amounts["expense_realized"],
            "payroll_realized": amounts["payroll_realized"],
        }


class GlcCoverageCockpitLine(models.TransientModel):
    _name = "glc.coverage.cockpit.line"
    _description = "Détail cockpit couverture GLC"
    _order = "month_key, activity_label, id"
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
    activity_label = fields.Char(string="Libellé axe analytique")
    analytic_code = fields.Char(
        string="Code analytique",
        related="analytic_account_id.code",
        readonly=True,
    )
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
        string="Ressources",
        currency_field="currency_id",
    )
    revenue_realized_paid = fields.Monetary(
        string="Ressources (payé)",
        currency_field="currency_id",
    )
    expense_realized = fields.Monetary(
        string="Dépenses",
        currency_field="currency_id",
    )
    expense_realized_paid = fields.Monetary(
        string="Dépenses (payé)",
        currency_field="currency_id",
    )
    payroll_realized = fields.Monetary(
        string="Cumul RH",
        currency_field="currency_id",
    )
    payroll_realized_paid = fields.Monetary(
        string="Cumul RH (payé)",
        currency_field="currency_id",
    )
    performance_realized = fields.Monetary(
        string="Solde",
        currency_field="currency_id",
        compute="_compute_performance",
    )

    @api.depends(
        "revenue_realized",
        "payroll_realized",
        "expense_realized",
    )
    def _compute_performance(self):
        for line in self:
            line.performance_realized = (
                line.revenue_realized
                - line.payroll_realized
                - line.expense_realized
            )

    @api.model_create_multi
    def create(self, vals_list):
        _glc_cockpit_require_auto_refresh(self.env)
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
        _glc_cockpit_require_auto_refresh(self.env)
        return super().write(vals)

    def unlink(self):
        _glc_cockpit_require_auto_refresh(self.env)
        return super().unlink()


class GlcCoverageCockpitTreasuryLine(models.TransientModel):
    _name = "glc.coverage.cockpit.treasury.line"
    _description = "Virement interne cockpit GLC par axe analytique"
    _order = "activity_label, transfer_gl_account_code, id"
    _rec_name = "activity_label"

    cockpit_id = fields.Many2one(
        "glc.coverage.cockpit",
        required=True,
        ondelete="cascade",
    )
    analytic_account_id = fields.Many2one(
        "account.analytic.account",
        string="Axe analytique",
    )
    analytic_code = fields.Char(
        string="Code analytique",
        related="analytic_account_id.code",
        readonly=True,
    )
    activity_label = fields.Char(string="Qualification métier", required=True)
    transfer_gl_account_code = fields.Char(
        string="Compte comptable",
        required=True,
        help="Compte de virement interne (ex. 580001).",
    )
    currency_id = fields.Many2one(
        related="cockpit_id.currency_id",
        store=True,
        readonly=True,
    )
    internal_inflow = fields.Monetary(
        string="Entrée virement interne",
        currency_field="currency_id",
    )
    internal_outflow = fields.Monetary(
        string="Sortie virement interne",
        currency_field="currency_id",
    )

    @api.model_create_multi
    def create(self, vals_list):
        _glc_cockpit_require_auto_refresh(self.env)
        cleaned_vals_list = [
            vals for vals in vals_list if vals.get("cockpit_id")
        ]
        if not cleaned_vals_list:
            return self.browse()
        return super().create(cleaned_vals_list)

    def write(self, vals):
        _glc_cockpit_require_auto_refresh(self.env)
        return super().write(vals)

    def unlink(self):
        _glc_cockpit_require_auto_refresh(self.env)
        return super().unlink()
