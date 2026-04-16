# -*- coding: utf-8 -*-

from odoo import fields, models


class DoreviaHelloassoAccount(models.Model):
    _inherit = "dorevia.helloasso.account"

    membership_pont_rail = fields.Selection(
        [
            ("none", "Désactivé"),
            ("v1_line", "V1 — Ligne d'adhésion sans facture"),
            ("v2_accounting", "V2 — Constatation comptable (facture + paiement)"),
        ],
        string="Rail pont adhésion HelloAsso",
        default="v1_line",
        help=(
            "V1 et V2 sont exclusifs par compte HelloAsso. "
            "V2 enregistre une facture client et un paiement ; la ligne d'adhésion suit la facture (OCA)."
        ),
    )

    membership_bridge_enabled = fields.Boolean(
        string="Activer le pont HelloAsso → Adhésion Odoo",
        default=False,
        help=(
            "Si activé avec « Adhésions (Membership) », chaque import ou mise à jour de "
            "pivot paiement éligible tente de créer une ligne d'adhésion via le service pont "
            "(opt-in ; désactivé par défaut pour la recette progressive)."
        ),
    )
    membership_bridge_product_id = fields.Many2one(
        "product.product",
        string="Produit d'adhésion (pont)",
        domain="[('membership', '=', True), ('type', '=', 'service'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help=(
            "Produit membership utilisé pour créer la ligne d'adhésion lorsque le pont est "
            "activé. Oblatoire pour que le pont s'exécute après collecte des paiements."
        ),
    )
    membership_bridge_require_member_type = fields.Boolean(
        string="Exiger une typologie adhérent (V1)",
        default=False,
        help=(
            "Si activé (rail V1 uniquement), le pont refuse de créer une ligne d'adhésion "
            "lorsque le contact payeur n'a pas de « Type d'adhésion » (member_type_id) renseigné. "
            "Désactivé par défaut (story E2 S7-2)."
        ),
    )
