# -*- coding: utf-8 -*-

from odoo import fields, models


class GlcAnalyticAnomalyLine(models.TransientModel):
    _name = "glc.analytic.anomaly.line"
    _description = "Ligne d'anomalie analytique GLC"
    _order = "date desc, id desc"

    wizard_id = fields.Many2one(
        "glc.analytic.anomaly.wizard",
        required=True,
        ondelete="cascade",
    )
    date = fields.Date()
    move_id = fields.Many2one("account.move", string="Pièce comptable")
    move_line_id = fields.Many2one("account.move.line", string="Ligne comptable")
    journal_id = fields.Many2one("account.journal", string="Journal")
    partner_id = fields.Many2one("res.partner", string="Partenaire")
    account_id = fields.Many2one("account.account", string="Compte comptable")
    name = fields.Char(string="Libellé")
    amount = fields.Monetary(currency_field="currency_id")
    currency_id = fields.Many2one(related="wizard_id.company_id.currency_id")
    anomaly_type = fields.Selection(
        selection=[
            ("a1_vendor_no_activity", "A1 — Fournisseur sans activité"),
            ("a2_revenue_no_activity", "A2 — Recette sans activité"),
            ("a2_revenue_no_funding", "A2 — Recette sans financement"),
            ("a2_revenue_incomplete", "A2 — Recette incomplète"),
            ("a4_payroll_analytic", "A4 — Paie avec analytique"),
            ("a5_legacy_account", "A5 — Ancien compte analytique"),
        ],
        required=True,
    )
    message = fields.Char(required=True)
    recommendation = fields.Char()
    activity_account_ids = fields.Many2many(
        "account.analytic.account",
        "glc_anomaly_line_activity_rel",
        "line_id",
        "account_id",
        string="Activités détectées",
    )
    funding_account_ids = fields.Many2many(
        "account.analytic.account",
        "glc_anomaly_line_funding_rel",
        "line_id",
        "account_id",
        string="Financements détectés",
    )

    def action_open_move(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": self.env._("Pièce comptable"),
            "res_model": "account.move",
            "res_id": self.move_id.id,
            "view_mode": "form",
            "target": "current",
        }
