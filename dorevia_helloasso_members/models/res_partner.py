# -*- coding: utf-8 -*-

from odoo import api, fields, models


_HELLOASSO_SYNC_STATUS = [
    ("never", "Jamais"),
    ("pending", "En attente"),
    ("pending_review", "En révision"),
    ("ok", "OK"),
    ("synced", "Synchronisé"),
    ("error", "Erreur"),
]


class ResPartner(models.Model):
    _inherit = "res.partner"

    member_type_id = fields.Many2one(
        "res.partner.category",
        string="Type d'adhésion",
        help=(
            "Classification optionnelle (catégorie de partenaire Odoo). "
            "Toute automatisation ou règle d'affectation au-delà d'une saisie manuelle "
            "relève du pilote métier documenté (modules membership ou pont HelloAsso), "
            "pas du connecteur HelloAsso."
        ),
    )
    helloasso_external_id = fields.Char(
        string="ID paiement HelloAsso",
        index=True,
        copy=False,
    )
    helloasso_order_id = fields.Char(string="ID commande HelloAsso", copy=False)
    helloasso_source_form = fields.Char(
        string="Réf. formulaire HelloAsso",
        index=True,
        copy=False,
    )
    helloasso_source_form_title = fields.Char(
        string="Titre formulaire HelloAsso",
        copy=False,
    )
    helloasso_form_type = fields.Char(string="Type de formulaire HelloAsso", copy=False)
    helloasso_payment_date = fields.Datetime(
        string="Date de paiement HelloAsso",
        copy=False,
    )
    helloasso_payment_mean = fields.Char(string="Moyen de paiement HelloAsso", copy=False)
    helloasso_payment_amount = fields.Float(
        string="Montant HelloAsso (€)",
        digits=(16, 2),
        copy=False,
    )
    helloasso_sync_status = fields.Selection(
        _HELLOASSO_SYNC_STATUS,
        string="Statut synchro HelloAsso",
        default="never",
        index=True,
    )
    helloasso_last_sync_at = fields.Datetime(
        string="Dernière synchro HelloAsso",
        copy=False,
    )
    helloasso_sync_form_caption = fields.Char(
        string="Libellé campagne (HelloAsso)",
        compute="_compute_helloasso_sync_form_caption",
        store=True,
        readonly=True,
    )
    helloasso_account_id = fields.Many2one(
        "dorevia.helloasso.account",
        string="Compte HelloAsso source",
        ondelete="set null",
        index=True,
        help="Dernier compte HelloAsso ayant alimenté les champs adhésion sur ce contact.",
    )

    @api.depends("helloasso_source_form_title", "helloasso_source_form")
    def _compute_helloasso_sync_form_caption(self):
        for partner in self:
            partner.helloasso_sync_form_caption = (
                partner.helloasso_source_form_title
                or partner.helloasso_source_form
                or ""
            )
