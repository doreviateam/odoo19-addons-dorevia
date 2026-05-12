# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DoreviaCashGuardWeek(models.Model):
    _name = "dorevia.cash.guard.week"
    _description = "Détail de projection"
    _rec_name = "week_label"
    _order = "guard_id, week_index"

    guard_id = fields.Many2one(
        "dorevia.cash.guard",
        string="Projet de trésorerie",
        required=True,
        ondelete="cascade",
        index=True,
    )
    alert_threshold = fields.Monetary(
        related="guard_id.alert_threshold",
        currency_field="currency_id",
        string="Seuil d'alerte",
        readonly=True,
    )
    week_index = fields.Integer(string="Indice période", required=True)
    week_label = fields.Char(string="Période", required=True)
    date_from = fields.Date(string="Début", required=True)
    date_to = fields.Date(string="Fin", required=True)
    period_type = fields.Selection(
        [
            ("historical", "Constaté"),
            ("current", "Situation"),
            ("forecast", "Projeté"),
        ],
        string="État",
        required=True,
        index=True,
    )
    opening_balance = fields.Monetary(string="Solde début")
    inflow_amount = fields.Monetary(string="Entrées")
    outflow_amount = fields.Monetary(string="Sorties")
    closing_balance = fields.Monetary(
        string="Solde",
        help=(
            "Solde de trésorerie constaté ou rejoué sur la période "
            "(fin de maille, trajectoire synthétique)."
        ),
    )
    projected_balance = fields.Monetary(
        string="Projection",
        help=(
            "Solde après prise en compte des factures ouvertes validées, à leur date "
            "d'échéance projetée (montant résiduel)."
        ),
    )
    margin_amount = fields.Monetary(
        string="Couverture",
        compute="_compute_margin_amount",
        currency_field="currency_id",
        help=(
            "Couverture en euros : projection moins le seuil d'alerte (réservé / échéance critique "
            "à couvrir, même devise). Couverture positive : le seuil est couvert ; négative : il "
            "manque ce montant. Une évolution ultérieure pourra afficher en complément un ratio "
            "(% du seuil) sans remplacer le montant."
        ),
    )
    invoice_inflow_amount = fields.Monetary(
        string="Encaissements projetés (factures)",
        help="Somme des entrées de trésorerie attendues issues des factures ouvertes sur la période.",
    )
    invoice_outflow_amount = fields.Monetary(
        string="Décaissements projetés (factures)",
        help="Somme des sorties de trésorerie attendues issues des factures ouvertes sur la période.",
    )
    invoice_net_amount = fields.Monetary(
        string="Impact net factures",
        currency_field="currency_id",
        help="Somme des impacts signés des factures ouvertes sur la maille (détail V1.3).",
        readonly=True,
    )
    invoice_move_count = fields.Integer(
        string="Nb pièces (factures)",
        readonly=True,
    )
    document_count_label = fields.Char(
        string="Documents",
        compute="_compute_document_count_label",
    )
    projection_move_ids = fields.One2many(
        "dorevia.cash.guard.period.move",
        "week_id",
        string="Pièces de projection",
        readonly=True,
    )
    min_balance = fields.Monetary(string="Point bas")
    risk_status = fields.Selection(
        [
            ("safe", "Confort"),
            ("warning", "Vigilance"),
            ("tension", "Tension"),
            ("risk", "Risque"),
        ],
        string="Statut",
        help=(
            "Statut par rapport aux seuils d'alerte et de confort : "
            "confort (vert) / vigilance (bleu) / tension (orange) / risque (rouge)."
        ),
    )
    currency_id = fields.Many2one(
        "res.currency",
        related="guard_id.currency_id",
        store=True,
        readonly=True,
    )
    company_id = fields.Many2one(
        "res.company",
        related="guard_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )

    @api.depends("invoice_move_count")
    def _compute_document_count_label(self):
        for rec in self:
            rec.document_count_label = str(rec.invoice_move_count) if rec.invoice_move_count else ""

    @api.depends("week_label")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = _("Détail de projection — %s", rec.week_label or "")

    @api.depends("projected_balance", "guard_id.alert_threshold")
    def _compute_margin_amount(self):
        for line in self:
            th = line.guard_id.alert_threshold or 0.0
            proj = line.projected_balance or 0.0
            line.margin_amount = proj - th

    def action_view_period_documents(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Documents — %s", self.week_label or ""),
            "res_model": "dorevia.cash.guard.period.move",
            "view_mode": "list",
            "domain": [("week_id", "=", self.id)],
            "context": {"create": False, "delete": False},
            "target": "new",
        }

    @api.constrains("guard_id", "week_index")
    def _check_week_index_unique(self):
        for line in self:
            dup = self.search_count(
                [
                    ("guard_id", "=", line.guard_id.id),
                    ("week_index", "=", line.week_index),
                    ("id", "!=", line.id),
                ]
            )
            if dup:
                raise ValidationError(
                    _("L'indice de période doit être unique par document de projection.")
                )
