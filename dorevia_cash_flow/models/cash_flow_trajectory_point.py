# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class DoreviaCashFlowTrajectoryPoint(models.TransientModel):
    _name = "dorevia.cash.flow.trajectory.point"
    _description = "Point de trajectoire de trésorerie"
    _order = "sequence, id"

    wizard_id = fields.Many2one(
        "dorevia.cash.flow.trajectory.wizard",
        string="Assistant",
        required=True,
        ondelete="cascade",
    )
    guard_id = fields.Many2one(
        related="wizard_id.guard_id",
        comodel_name="dorevia.cash.guard",
        string="Projection",
        store=False,
    )
    sequence = fields.Integer(string="Séquence", required=True, default=10)
    anchor_date = fields.Date(string="Date", required=True)
    label = fields.Char(string="Période")
    balance = fields.Monetary(string="Trésorerie", required=True)
    segment = fields.Selection(
        [("actual", "Constaté"), ("projected", "Projeté")],
        string="Segment",
        required=True,
    )
    series_key = fields.Char(string="Clé série")
    series_label = fields.Char(string="Libellé série")
    series_type = fields.Selection(
        [
            ("actual", "Constaté"),
            ("projected", "Projeté"),
            ("historical", "Historique"),
            ("budget", "Budget"),
            ("scenario", "Scénario"),
        ],
        string="Type de série",
        required=True,
    )
    fiscal_week_index = fields.Integer(string="Semaine fiscale", required=True)
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
