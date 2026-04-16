# -*- coding: utf-8 -*-

from odoo import fields, models


class MembershipLine(models.Model):
    _inherit = "membership.membership_line"

    dorevia_helloasso_payment_id = fields.Many2one(
        "dorevia.helloasso.payment",
        string="Paiement HelloAsso (pont)",
        index=True,
        copy=False,
        ondelete="set null",
        help="Si renseigné, cette ligne provient du pont pivot paiement → adhésion (idempotence).",
    )

    _membership_line_helloasso_payment_unique = models.Constraint(
        "unique(dorevia_helloasso_payment_id)",
        "Une ligne d'adhésion existe déjà pour ce paiement HelloAsso (pont).",
    )
