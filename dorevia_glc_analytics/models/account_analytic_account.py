# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    glc_activity_type = fields.Selection(
        selection=[
            ("charge", "Charge"),
            ("recette", "Recette"),
            ("mixte", "Mixte"),
        ],
        string="Type GLC",
        help="Nature de lecture cockpit GLC : charge, recette ou mixte.",
    )
    glc_display_sequence = fields.Integer(
        string="Ordre rapport GLC",
        default=10,
        help="Ordre d'affichage dans les tableaux de pilotage GLC.",
    )
    glc_report_active = fields.Boolean(
        string="Actif rapport GLC",
        default=True,
        help="Inclure ce compte dans les rapports de pilotage GLC.",
    )
    glc_pilotage_comment = fields.Text(
        string="Commentaire de pilotage",
        help="Note de gestion visible sur la fiche activité et les rapports.",
    )
