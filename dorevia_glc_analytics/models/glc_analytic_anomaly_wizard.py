# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from .glc_constants import (
    GLC_EXPENSE_ACCOUNT_TYPES,
    GLC_FUNDING_ANALYTIC_CODES,
    GLC_INCOME_ACCOUNT_TYPES,
    GLC_LEGACY_ANALYTIC_CODES,
    GLC_PAYROLL_ACCOUNT_PREFIXES,
)


class GlcAnalyticAnomalyWizard(models.TransientModel):
    _name = "glc.analytic.anomaly.wizard"
    _description = "Assistant anomalies analytiques GLC"

    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.company,
    )
    date_from = fields.Date(
        required=True,
        default=lambda self: fields.Date.context_today(self).replace(day=1),
    )
    date_to = fields.Date(required=True, default=fields.Date.context_today)
    include_posted = fields.Boolean(string="Écritures validées", default=True)
    include_draft = fields.Boolean(string="Brouillons", default=False)
    line_ids = fields.One2many(
        "glc.analytic.anomaly.line",
        "wizard_id",
        string="Anomalies",
        readonly=True,
    )
    line_count = fields.Integer(compute="_compute_line_count")
    structure_weight_pct = fields.Float(
        string="Poids STRUCTURE (%)",
        digits=(16, 2),
        readonly=True,
    )
    structure_alert_active = fields.Boolean(readonly=True)
    structure_alert_message = fields.Char(readonly=True)
    a5_enabled = fields.Boolean(readonly=True)
    a5_info_message = fields.Char(readonly=True)
    count_a1 = fields.Integer(readonly=True)
    count_a2 = fields.Integer(readonly=True)
    count_a4 = fields.Integer(readonly=True)
    count_a5 = fields.Integer(readonly=True)

    @api.depends("line_ids")
    def _compute_line_count(self):
        for wizard in self:
            wizard.line_count = len(wizard.line_ids)

    @api.constrains("date_from", "date_to")
    def _check_dates(self):
        for wizard in self:
            if wizard.date_from and wizard.date_to and wizard.date_from > wizard.date_to:
                raise UserError(_("La date de début doit être antérieure à la date de fin."))

    def action_analyze(self):
        self.ensure_one()
        self.line_ids.unlink()
        self._reset_summary_fields()

        move_lines = self._get_move_lines()
        anomaly_vals = []
        for line in move_lines:
            anomaly_vals.extend(self._analyze_move_line(line))

        if anomaly_vals:
            self.env["glc.analytic.anomaly.line"].create(anomaly_vals)

        self._compute_structure_weight(move_lines)
        self._update_control_status()
        self._update_counters()

        return {
            "type": "ir.actions.act_window",
            "name": _("Audit"),
            "res_model": "glc.analytic.anomaly.wizard",
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }

    def _reset_summary_fields(self):
        self.write(
            {
                "structure_weight_pct": 0.0,
                "structure_alert_active": False,
                "structure_alert_message": False,
                "a5_enabled": False,
                "a5_info_message": False,
                "count_a1": 0,
                "count_a2": 0,
                "count_a4": 0,
                "count_a5": 0,
            }
        )

    def _update_control_status(self):
        icp = self.env["ir.config_parameter"].sudo()
        cutover = icp.get_param("dorevia_glc_analytics.cutover_date")
        vals = {
            "a5_enabled": bool(cutover),
            "a5_info_message": (
                False
                if cutover
                else _(
                    "Contrôle A5 inactif : paramètre dorevia_glc_analytics.cutover_date absent."
                )
            ),
        }
        self.write(vals)

    def _update_counters(self):
        lines = self.line_ids
        self.write(
            {
                "count_a1": len(lines.filtered(lambda line: line.anomaly_type == "a1_vendor_no_activity")),
                "count_a2": len(
                    lines.filtered(
                        lambda line: line.anomaly_type.startswith("a2_revenue")
                    )
                ),
                "count_a4": len(lines.filtered(lambda line: line.anomaly_type == "a4_payroll_analytic")),
                "count_a5": len(lines.filtered(lambda line: line.anomaly_type == "a5_legacy_account")),
            }
        )

    def _get_move_lines(self):
        self.ensure_one()
        if not self.include_posted and not self.include_draft:
            raise UserError(_("Sélectionnez au moins un état d'écriture (validée ou brouillon)."))

        states = []
        if self.include_posted:
            states.append("posted")
        if self.include_draft:
            states.append("draft")

        domain = [
            ("company_id", "=", self.company_id.id),
            ("display_type", "not in", ("line_section", "line_note")),
            ("move_id.state", "in", states),
            ("date", ">=", self.date_from),
            ("date", "<=", self.date_to),
        ]
        return self.env["account.move.line"].search(domain)

    def _get_plan(self, xmlid):
        return self.env.ref(f"dorevia_glc_analytics.{xmlid}")

    def _distribution_account_ids(self, distribution):
        if not distribution:
            return []
        return [int(account_id) for account_id in distribution.keys()]

    def _accounts_for_plan(self, distribution, plan):
        account_ids = self._distribution_account_ids(distribution)
        if not account_ids:
            return self.env["account.analytic.account"]
        return self.env["account.analytic.account"].browse(account_ids).filtered(
            lambda account: account.plan_id == plan
        )

    def _line_base_vals(self, line):
        return {
            "wizard_id": self.id,
            "date": line.date,
            "move_id": line.move_id.id,
            "move_line_id": line.id,
            "journal_id": line.journal_id.id,
            "partner_id": line.partner_id.id,
            "account_id": line.account_id.id,
            "name": line.name,
            "amount": line.balance,
        }

    def _accounts_from_distribution(self, distribution):
        account_ids = self._distribution_account_ids(distribution)
        if not account_ids:
            return self.env["account.analytic.account"]
        return self.env["account.analytic.account"].browse(account_ids).exists()

    def _analyze_move_line(self, line):
        distribution = line.analytic_distribution or {}
        plan_activites = self._get_plan("analytic_plan_glc_activites")
        distributed_accounts = self._accounts_from_distribution(distribution)
        funding_accounts = distributed_accounts.filtered(
            lambda account: account.code in GLC_FUNDING_ANALYTIC_CODES
        )
        activity_accounts = distributed_accounts.filtered(
            lambda account: account.plan_id == plan_activites
            and account.code not in GLC_FUNDING_ANALYTIC_CODES
        )
        base = self._line_base_vals(line)
        common = {
            **base,
            "activity_account_ids": [(6, 0, activity_accounts.ids)],
            "funding_account_ids": [(6, 0, funding_accounts.ids)],
        }
        anomalies = []

        anomalies.extend(self._check_a1(line, activity_accounts, common))
        anomalies.extend(self._check_a2(line, activity_accounts, funding_accounts, common))
        anomalies.extend(self._check_a4(line, distribution, common))
        anomalies.extend(
            self._check_a5(line, distribution, common)
        )
        return anomalies

    def _check_a1(self, line, activity_accounts, common):
        if line.move_id.move_type not in ("in_invoice", "in_refund"):
            return []
        if line.account_id.account_type not in GLC_EXPENSE_ACCOUNT_TYPES:
            return []
        if activity_accounts:
            return []
        return [
            {
                **common,
                "anomaly_type": "a1_vendor_no_activity",
                "message": _("Facture fournisseur sans activité GLC"),
                "recommendation": _(
                    "Affecter un compte du plan GLC - Activités sur la ligne de charge."
                ),
            }
        ]

    def _check_a2(self, line, activity_accounts, funding_accounts, common):
        if line.move_id.move_type not in ("out_invoice", "out_refund"):
            return []
        if line.account_id.account_type not in GLC_INCOME_ACCOUNT_TYPES:
            return []

        has_activity = bool(activity_accounts)
        has_funding = bool(funding_accounts)
        if has_activity and has_funding:
            return []

        if not has_activity and not has_funding:
            return [
                {
                    **common,
                    "anomaly_type": "a2_revenue_incomplete",
                    "message": _("Recette incomplète : double axe attendu"),
                    "recommendation": _(
                        "Renseigner Activités GLC et Financements GLC sur la ligne de produit."
                    ),
                }
            ]
        if not has_activity:
            return [
                {
                    **common,
                    "anomaly_type": "a2_revenue_no_activity",
                    "message": _("Recette sans activité GLC"),
                    "recommendation": _(
                        "Affecter un compte du plan GLC - Activités (ex. BAR, PRESTATIONS)."
                    ),
                }
            ]
        return [
            {
                **common,
                "anomaly_type": "a2_revenue_no_funding",
                "message": _("Recette sans financement GLC"),
                "recommendation": _(
                    "Affecter un axe financement GLC (ex. RESSOURCES_PROPRES)."
                ),
            }
        ]

    def _is_payroll_account(self, account):
        code = (account.code or "").replace(" ", "")
        return any(code.startswith(prefix) for prefix in GLC_PAYROLL_ACCOUNT_PREFIXES)

    def _check_a4(self, line, distribution, common):
        if not distribution:
            return []
        if not self._is_payroll_account(line.account_id):
            return []
        return [
            {
                **common,
                "anomaly_type": "a4_payroll_analytic",
                "message": _("Écriture de paie avec analytique directe interdite"),
                "recommendation": _(
                    "Retirer l'analytique sur les comptes de paie ; le cumul RH est lu depuis la comptabilité analytique."
                ),
            }
        ]

    def _check_a5(self, line, distribution, common):
        icp = self.env["ir.config_parameter"].sudo()
        cutover_raw = icp.get_param("dorevia_glc_analytics.cutover_date")
        if not cutover_raw:
            return []

        cutover = fields.Date.to_date(cutover_raw)
        if line.date <= cutover:
            return []

        legacy_accounts = self.env["account.analytic.account"].search(
            [("code", "in", list(GLC_LEGACY_ANALYTIC_CODES))]
        )
        if not legacy_accounts:
            return []

        used_legacy = legacy_accounts.filtered(
            lambda account: str(account.id) in distribution
        )
        if not used_legacy:
            return []

        return [
            {
                **common,
                "anomaly_type": "a5_legacy_account",
                "message": _("Ancien compte analytique utilisé après bascule"),
                "recommendation": _(
                    "Remplacer %(legacy)s par le compte GLC cible correspondant.",
                    legacy=", ".join(used_legacy.mapped("code")),
                ),
            }
        ]

    def _compute_structure_weight(self, move_lines):
        plan_activites = self._get_plan("analytic_plan_glc_activites")
        structure = self.env.ref("dorevia_glc_analytics.analytic_account_glc_structure")
        activity_accounts = self.env["account.analytic.account"].search(
            [("plan_id", "=", plan_activites.id)]
        )

        total_activity_amount = 0.0
        structure_amount = 0.0

        for line in move_lines:
            if line.account_id.account_type not in GLC_EXPENSE_ACCOUNT_TYPES:
                continue
            distribution = line.analytic_distribution or {}
            line_activity_accounts = self._accounts_for_plan(distribution, plan_activites)
            if not line_activity_accounts:
                continue

            line_amount = abs(line.balance)
            for account in line_activity_accounts:
                pct = float(distribution.get(str(account.id), 0.0))
                allocated = line_amount * (pct / 100.0)
                total_activity_amount += allocated
                if account == structure:
                    structure_amount += allocated

        weight_pct = (
            (structure_amount / total_activity_amount) * 100.0
            if total_activity_amount
            else 0.0
        )

        icp = self.env["ir.config_parameter"].sudo()
        threshold = float(
            icp.get_param("dorevia_glc_analytics.structure_weight_alert_pct", "30")
        )
        alert_active = bool(total_activity_amount) and weight_pct >= threshold

        self.write(
            {
                "structure_weight_pct": weight_pct,
                "structure_alert_active": alert_active,
                "structure_alert_message": (
                    _("Poids STRUCTURE élevé — risque de compte fourre-tout")
                    if alert_active
                    else False
                ),
            }
        )
