# -*- coding: utf-8 -*-

from odoo import api, fields, models


class MembershipLine(models.Model):
    _inherit = "membership.membership_line"

    validite_adhesion = fields.Selection(
        selection=[
            ("en_cours", "En cours"),
            ("depasse", "Dépassé"),
        ],
        string="Validité",
        compute="_compute_validite_adhesion",
        store=True,
        readonly=True,
        copy=False,
        help=(
            "Uniquement si le statut est « Membre facturé » ou « Membre payant » : "
            "comparaison entre la date du jour et la date de fin d'adhésion."
        ),
    )

    @api.depends("state", "date_to")
    def _compute_validite_adhesion(self):
        today = fields.Date.context_today(self)
        states_avec_validite = ("invoiced", "paid")
        for line in self:
            if line.state not in states_avec_validite or not line.date_to:
                line.validite_adhesion = False
                continue
            line.validite_adhesion = (
                "en_cours" if line.date_to >= today else "depasse"
            )
