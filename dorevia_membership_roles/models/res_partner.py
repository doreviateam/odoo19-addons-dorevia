# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    membership_role_ids = fields.Many2many(
        comodel_name="membership.role",
        relation="res_partner_membership_role_rel",
        column1="partner_id",
        column2="role_id",
        string="Rôles de membre",
        help="Rôles fonctionnels (hors statut d'adhésion).",
    )

    @api.model_create_multi
    def create(self, vals_list):
        partners = super().create(vals_list)
        for partner in partners:
            if partner.membership_role_ids:
                partner.membership_role_ids.invalidate_recordset(["partner_count"])
        return partners

    def write(self, vals):
        old_roles = self.env["membership.role"]
        if "membership_role_ids" in vals:
            old_roles = self.mapped("membership_role_ids")
        res = super().write(vals)
        if "membership_role_ids" in vals:
            (old_roles | self.mapped("membership_role_ids")).invalidate_recordset(
                ["partner_count"]
            )
        return res
