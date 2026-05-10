# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DoreviaCashGuardWeek(models.Model):
    _name = "dorevia.cash.guard.week"
    _description = "Solde de trésorerie Cash Guard"
    _order = "guard_id, week_index"

    guard_id = fields.Many2one(
        "dorevia.cash.guard",
        string="Point de trésorerie",
        required=True,
        ondelete="cascade",
        index=True,
    )
    week_index = fields.Integer(string="Indice période", required=True)
    week_label = fields.Char(string="Période", required=True)
    date_from = fields.Date(string="Début", required=True)
    date_to = fields.Date(string="Fin", required=True)
    period_type = fields.Selection(
        [
            ("historical", "Constaté"),
            ("current", "Situation"),
            ("forecast", "Prévisionnel"),
        ],
        string="Lecture",
        required=True,
        index=True,
    )
    opening_balance = fields.Monetary(string="Solde début")
    inflow_amount = fields.Monetary(string="Entrées")
    outflow_amount = fields.Monetary(string="Sorties")
    closing_balance = fields.Monetary(
        string="Solde",
        help="Solde de trésorerie en fin de période (trajectoire synthétique).",
    )
    projected_balance = fields.Monetary(
        string="Solde projeté",
        help=(
            "Solde après intégration des factures clients/fournisseurs validées ouvertes "
            "(montant résiduel à la date d'échéance projetée)."
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
    min_balance = fields.Monetary(string="Point bas")
    risk_status = fields.Selection(
        [
            ("safe", "Sécurisé"),
            ("warning", "Vigilance"),
            ("risk", "Risque"),
        ],
        string="Statut",
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
                    _("L'indice de période doit être unique par point de trésorerie.")
                )
