# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    _rec_names_search = [
        "complete_name",
        "email",
        "ref",
        "vat",
        "company_registry",
        "pseudonym",
    ]

    pseudonym = fields.Char(
        string="Pseudonyme",
        copy=False,
        index=True,
        help=(
            "Nom d'enseigne partagé entre plusieurs sociétés "
            "(ex. Super U pour Super U Bouaye, Super U Montaigu) "
            "ou surnom d'une personne. Facultatif."
        ),
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "pseudonym" in vals:
                vals["pseudonym"] = self._normalize_pseudonym(vals.get("pseudonym"))
        return super().create(vals_list)

    def write(self, vals):
        if "pseudonym" in vals:
            vals = dict(vals)
            vals["pseudonym"] = self._normalize_pseudonym(vals.get("pseudonym"))
        return super().write(vals)

    @api.model
    def _normalize_pseudonym(self, value):
        if not value:
            return False
        normalized = value.strip()
        return normalized or False
