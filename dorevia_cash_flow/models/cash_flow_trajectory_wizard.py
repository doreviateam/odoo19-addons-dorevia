# -*- coding: utf-8 -*-

from datetime import date, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


def _week_iso_label(d):
    if not d:
        return ""
    if not isinstance(d, date):
        d = fields.Date.from_string(d)
    _y, iso_week, _dow = d.isocalendar()
    return "S%02d" % iso_week


def _week_end_dates_before_situation(fiscal_start, situation_date):
    """Dates de fin de maille hebdo (borne < situation_date), alignement 7 jours depuis fiscal_start."""
    if not fiscal_start or not situation_date:
        return []
    if isinstance(fiscal_start, str):
        fiscal_start = fields.Date.from_string(fiscal_start)
    if isinstance(situation_date, str):
        situation_date = fields.Date.from_string(situation_date)
    if fiscal_start >= situation_date:
        return []
    dates = []
    cur = fiscal_start
    while cur < situation_date:
        week_end = min(cur + timedelta(days=6), situation_date - timedelta(days=1))
        if week_end < cur:
            break
        dates.append(week_end)
        nxt = week_end + timedelta(days=1)
        if nxt >= situation_date:
            break
        cur = nxt
    return dates


class DoreviaCashFlowTrajectoryWizard(models.TransientModel):
    _name = "dorevia.cash.flow.trajectory.wizard"
    _description = "Assistant trajectoire de trésorerie"

    guard_id = fields.Many2one(
        "dorevia.cash.guard",
        string="Projection de trésorerie",
        required=True,
        domain="[('company_id', '=', company_id), ('active', '=', True), ('periodicity', '=', 'week')]",
    )
    company_id = fields.Many2one(
        "res.company",
        string="Société",
        required=True,
        default=lambda self: self.env.company,
    )
    situation_date = fields.Date(
        related="guard_id.situation_date",
        string="Date de situation",
        readonly=True,
    )
    chart_date_end = fields.Date(
        string="Fin horizon projeté (+90 j)",
        compute="_compute_chart_bounds",
    )
    fiscal_date_from = fields.Date(
        string="Début exercice fiscal",
        compute="_compute_chart_bounds",
    )
    alert_threshold = fields.Monetary(
        string="Seuil d'alerte",
        related="guard_id.alert_threshold",
        currency_field="currency_id",
        readonly=True,
    )
    currency_id = fields.Many2one(
        "res.currency",
        related="guard_id.currency_id",
        readonly=True,
    )
    min_balance_on_curve = fields.Monetary(
        string="Point bas (courbe)",
        compute="_compute_curve_stats",
        currency_field="currency_id",
        help="Renseigné après génération de la courbe (bouton « Afficher la trajectoire »).",
    )
    min_balance_date_on_curve = fields.Date(
        string="Date du point bas",
        compute="_compute_curve_stats",
    )
    info_message = fields.Char(
        string="Information",
        compute="_compute_curve_stats",
    )
    point_ids = fields.One2many(
        "dorevia.cash.flow.trajectory.point",
        "wizard_id",
        string="Points",
    )

    @api.depends("guard_id", "guard_id.situation_date", "guard_id.company_id")
    def _compute_chart_bounds(self):
        for wiz in self:
            guard = wiz.guard_id
            sit = guard.situation_date if guard else False
            if not sit:
                wiz.chart_date_end = False
                wiz.fiscal_date_from = False
                continue
            wiz.chart_date_end = sit + timedelta(days=90)
            company = guard.company_id
            fiscal_from = False
            if company and hasattr(company, "compute_fiscalyear_dates"):
                fy = company.compute_fiscalyear_dates(sit)
                fiscal_from = fy.get("date_from") if isinstance(fy, dict) else False
            if not fiscal_from:
                fiscal_from = date(sit.year, 1, 1)
            wiz.fiscal_date_from = fiscal_from

    @api.depends("point_ids", "point_ids.balance", "point_ids.anchor_date", "point_ids.segment")
    def _compute_curve_stats(self):
        for wiz in self:
            pts = wiz.point_ids
            if not pts:
                wiz.min_balance_on_curve = 0.0
                wiz.min_balance_date_on_curve = False
                wiz.info_message = ""
                continue
            min_pt = min(pts, key=lambda p: (p.balance or 0.0, p.anchor_date or date.min))
            wiz.min_balance_on_curve = min_pt.balance
            wiz.min_balance_date_on_curve = min_pt.anchor_date
            if not any(p.segment == "projected" for p in pts):
                wiz.info_message = _(
                    "Aucune maille projetée dans l'horizon (date de situation + 90 j) : "
                    "seul le constaté est affiché."
                )
            else:
                wiz.info_message = ""

    @api.model
    def _resolve_reference_guard(self):
        """Projection Cash Guard de référence pour la société courante (V1.1)."""
        company = self.env.company
        domain = [
            ("company_id", "=", company.id),
            ("active", "=", True),
            ("periodicity", "=", "week"),
        ]
        candidates = self.env["dorevia.cash.guard"].search(
            domain, order="situation_date desc, write_date desc, id desc"
        )
        for guard in candidates:
            if guard.weekly_line_ids:
                return guard
        return self.env["dorevia.cash.guard"].browse()

    @api.model
    def action_open_reference_trajectory(self):
        """Parcours nominal menu : courbe immédiate sans sélection utilisateur (V1.1)."""
        company = self.env.company
        guard = self._resolve_reference_guard()
        if not guard:
            raise UserError(
                _(
                    "Aucune projection hebdomadaire active avec des lignes calculées n'a été trouvée "
                    "pour la société « %(company)s ». "
                    "Veuillez créer ou actualiser une projection de trésorerie dans les Projections "
                    "de trésorerie (Cash Guard).",
                    company=company.display_name,
                )
            )
        wiz = self.create({"company_id": company.id, "guard_id": guard.id})
        return wiz._prepare_chart_action()

    @api.model
    def action_open_guard_cockpit(self):
        """Accueil menu Projection : trajectoire de référence + raccourcis atelier (lecture seule).

        Même résolution de projection et même graphique que le menu Analyse ; les actions
        d'atelier ouvrent Cash Guard sans dupliquer la logique de courbe.
        """
        company = self.env.company
        guard = self._resolve_reference_guard()
        if not guard:
            raise UserError(
                _(
                    "Aucune projection hebdomadaire active avec des lignes calculées n'a été trouvée "
                    "pour la société « %(company)s ». "
                    "Créez ou actualisez une projection depuis Projection > Trésorerie.",
                    company=company.display_name,
                )
            )
        wiz = self.create({"company_id": company.id, "guard_id": guard.id})
        action = wiz._prepare_chart_action()
        action.setdefault("params", {})
        action["params"]["cockpit"] = True
        action["params"]["guard_id"] = guard.id
        action["name"] = _("Cockpit trésorerie")
        return action

    def action_refresh_points_from_guard(self):
        """Reconstruit les points à partir du document Guard (après actualisation projection)."""
        self.ensure_one()
        self._ensure_guard_eligible()
        self.point_ids.unlink()
        Point = self.env["dorevia.cash.flow.trajectory.point"].sudo()
        for vals in self._build_point_rows():
            vals["wizard_id"] = self.id
            Point.create(vals)
        self.invalidate_recordset(["point_ids"])
        return True

    def _ensure_guard_eligible(self):
        self.ensure_one()
        guard = self.guard_id
        if not guard:
            raise UserError(_("Sélectionnez une projection de trésorerie."))
        if guard.periodicity != "week":
            raise UserError(
                _(
                    "Seules les projections à périodicité « Semaine » sont prises en charge pour "
                    "la trajectoire de trésorerie. Ouvrez ou créez une projection hebdomadaire dans "
                    "les Projections de trésorerie (Cash Guard)."
                )
            )
        if not guard.weekly_line_ids:
            raise UserError(
                _(
                    "Aucune maille de projection n'est disponible pour ce document. "
                    "Ouvrez la projection dans les Projections de trésorerie (Cash Guard) et "
                    "actualisez le calcul avant d'afficher la trajectoire."
                )
            )

    def _build_point_rows(self):
        self.ensure_one()
        guard = self.guard_id.sudo()
        sit = guard.situation_date
        fiscal_start = self.fiscal_date_from
        chart_end = self.chart_date_end
        rows = []
        seq = 10
        fiscal_week_index = 0

        week_ends = _week_end_dates_before_situation(fiscal_start, sit)
        for wend in week_ends:
            fiscal_week_index += 1
            bal = guard._compute_bank_balance_at_date(wend)
            rows.append(
                {
                    "sequence": seq,
                    "anchor_date": wend,
                    "label": _week_iso_label(wend),
                    "balance": bal,
                    "segment": "actual",
                    "series_key": "current_actual",
                    "series_label": _("Constaté exercice courant"),
                    "series_type": "actual",
                    "fiscal_week_index": fiscal_week_index,
                }
            )
            seq += 10

        fiscal_week_index += 1
        rows.append(
            {
                "sequence": seq,
                "anchor_date": sit,
                "label": _week_iso_label(sit),
                "balance": guard.observed_balance,
                "segment": "actual",
                "series_key": "current_actual",
                "series_label": _("Constaté exercice courant"),
                "series_type": "actual",
                "fiscal_week_index": fiscal_week_index,
            }
        )
        seq += 10

        forecast_weeks = guard.weekly_line_ids.filtered(
            lambda w: w.period_type == "forecast"
            and w.date_from > sit
            and w.date_to <= chart_end
        ).sorted("week_index")

        for week in forecast_weeks:
            fiscal_week_index += 1
            rows.append(
                {
                    "sequence": seq,
                    "anchor_date": week.date_to,
                    "label": week.week_label or _week_iso_label(week.date_to),
                    "balance": week.projected_balance,
                    "segment": "projected",
                    "series_key": "current_projected",
                    "series_label": _("Projeté 90 jours"),
                    "series_type": "projected",
                    "fiscal_week_index": fiscal_week_index,
                }
            )
            seq += 10

        return rows

    def _prepare_chart_action(self):
        self.ensure_one()
        self._ensure_guard_eligible()
        self.point_ids.unlink()
        Point = self.env["dorevia.cash.flow.trajectory.point"].sudo()
        for vals in self._build_point_rows():
            vals["wizard_id"] = self.id
            Point.create(vals)
        self.invalidate_recordset(["point_ids"])
        return {
            "type": "ir.actions.client",
            "tag": "dorevia_cash_flow_trajectory_chart",
            "name": _("Trajectoire de trésorerie"),
            "params": {
                "wizard_id": self.id,
            },
            "target": "current",
        }

    def action_open_chart(self):
        self.ensure_one()
        return self._prepare_chart_action()
