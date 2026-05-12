# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import AccessError


_MOVE_TYPE_LABELS = {
    "out_invoice": "Facture client",
    "in_invoice": "Facture fournisseur",
    "out_refund": "Avoir client",
    "in_refund": "Avoir fournisseur",
}


class DoreviaCashGuardPeriodMove(models.Model):
    """Document expliquant la projection : factures ouvertes + documents simulés (dérivé, régénéré)."""

    _name = "dorevia.cash.guard.period.move"
    _description = "Document de projection"
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
    period_risk_status = fields.Selection(
        related="week_id.risk_status",
        string="Statut période",
        store=True,
        readonly=True,
    )
    display_status = fields.Selection(
        [
            ("safe", "Confort"),
            ("warning", "Vigilance"),
            ("tension", "Tension"),
            ("risk", "Risque"),
            ("simulation", "Simulation"),
        ],
        string="Statut",
        readonly=True,
    )
    period_risk_sequence = fields.Integer(
        string="Ordre statut",
        compute="_compute_period_risk_sequence",
        store=True,
        index=True,
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
    is_simulation = fields.Boolean(
        string="Simulation",
        default=False,
        readonly=True,
    )
    document_type_label = fields.Char(
        string="Type",
        readonly=True,
    )
    move_id = fields.Many2one(
        "account.move",
        string="Pièce comptable",
        required=False,
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
    days_overdue = fields.Integer(
        string="Jours de retard",
        readonly=True,
        help="Nombre de jours entre la date de situation et l'échéance de référence (0 si non échue).",
    )
    days_overdue_label = fields.Char(
        string="Retard",
        compute="_compute_days_overdue_label",
        readonly=True,
    )

    @api.depends("is_overdue")
    def _compute_is_overdue_label(self):
        for line in self:
            line.is_overdue_label = "Oui" if line.is_overdue else "Non"

    @api.depends("days_overdue")
    def _compute_days_overdue_label(self):
        for line in self:
            d = line.days_overdue or 0
            line.days_overdue_label = f"{d} j" if d > 0 else ""

    @api.depends("week_id.risk_status")
    def _compute_period_risk_sequence(self):
        order = {"risk": 10, "tension": 15, "warning": 20, "safe": 30}
        for line in self:
            line.period_risk_sequence = order.get(line.week_id.risk_status, 99)

    def action_open_source_document(self):
        """Ouvre le document source : facture, devis ou commande achat (extensible)."""
        self.ensure_one()
        if self.move_id:
            return self._action_open_invoice()
        return False

    def _action_open_invoice(self):
        """Ouvre la facture / avoir source (droits ``account.move`` standards)."""
        self.ensure_one()
        move = self.move_id
        try:
            move.check_access("read")
        except AccessError:
            raise AccessError(
                _("Vous n'avez pas les droits pour ouvrir cette pièce comptable.")
            ) from None
        return {
            "type": "ir.actions.act_window",
            "name": move.display_name,
            "res_model": "account.move",
            "res_id": move.id,
            "view_mode": "form",
            "target": "new",
        }

    def action_open_source_invoice(self):
        """Alias conservé pour compatibilité descendante."""
        return self.action_open_source_document()
