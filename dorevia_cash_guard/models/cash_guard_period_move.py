# -*- coding: utf-8 -*-

from odoo import api, fields, models


class DoreviaCashGuardPeriodMove(models.Model):
    """Détail V1.3 : pièces ``account.move`` expliquant l'impact factures par maille (dérivé, régénéré)."""

    _name = "dorevia.cash.guard.period.move"
    _description = "Pièce de projection (factures ouvertes)"
    _order = "sequence, id"

    _cash_guard_period_move_guard_move_uniq = models.Constraint(
        "unique(guard_id, move_id)",
        "Une même facture ne peut apparaître qu'une fois par document de projection.",
    )

    sequence = fields.Integer(string="Séquence", default=10, index=True)
    guard_id = fields.Many2one(
        "dorevia.cash.guard",
        string="Document de projection",
        required=True,
        ondelete="cascade",
        index=True,
    )
    week_id = fields.Many2one(
        "dorevia.cash.guard.week",
        string="Période",
        required=True,
        ondelete="cascade",
        index=True,
    )
    week_index = fields.Integer(
        related="week_id.week_index",
        string="Indice période",
        store=True,
        readonly=True,
    )
    week_label = fields.Char(
        related="week_id.week_label",
        string="Libellé période",
        store=False,
        readonly=True,
    )
    week_invoice_net_amount = fields.Monetary(
        related="week_id.invoice_net_amount",
        string="Impact net période",
        currency_field="currency_id",
        readonly=True,
    )
    week_invoice_move_count = fields.Integer(
        related="week_id.invoice_move_count",
        string="Nb pièces période",
        readonly=True,
    )
    move_id = fields.Many2one(
        "account.move",
        string="Pièce comptable",
        required=True,
        ondelete="cascade",
        index=True,
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Partenaire",
        readonly=True,
    )
    move_type = fields.Selection(
        related="move_id.move_type",
        readonly=True,
    )
    move_name = fields.Char(string="Référence pièce", readonly=True)
    invoice_date = fields.Date(string="Date facture", readonly=True)
    invoice_date_due = fields.Date(string="Échéance", readonly=True)
    projected_date = fields.Date(string="Date projetée", readonly=True, index=True)
    amount_residual = fields.Monetary(
        string="Résidu (valeur absolue)",
        currency_field="currency_id",
        readonly=True,
        help="Montant résiduel en valeur absolue (devise société du document).",
    )
    signed_amount = fields.Monetary(
        string="Impact",
        currency_field="currency_id",
        readonly=True,
        help="Impact signé sur la trésorerie (même doctrine que la projection V1.2).",
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Devise",
        required=True,
        readonly=True,
    )
    company_id = fields.Many2one(
        "res.company",
        string="Société",
        required=True,
        readonly=True,
    )
    explanation_type = fields.Selection(
        [("inflow", "Entrée"), ("outflow", "Sortie")],
        string="Sens",
        readonly=True,
    )
    is_overdue = fields.Boolean(
        string="Retard",
        readonly=True,
        help="Vrai si la date d'échéance (ou date facture) de référence est antérieure à la date de situation.",
    )
    is_overdue_label = fields.Char(
        string="Échue",
        compute="_compute_is_overdue_label",
        readonly=True,
    )

    @api.depends("is_overdue")
    def _compute_is_overdue_label(self):
        for line in self:
            line.is_overdue_label = "Oui" if line.is_overdue else "Non"
