# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class MembershipRole(models.Model):
    _name = "membership.role"
    _description = "Rôle de membre associatif"
    _order = "sequence, name, id"

    name = fields.Char(
        required=True,
        translate=True,
        string="Libellé",
    )
    sequence = fields.Integer(string="Séquence", default=10)
    active = fields.Boolean(string="Actif", default=True)
    company_id = fields.Many2one("res.company", string="Société")
    partner_count = fields.Integer(
        string="Nombre de contacts",
        compute="_compute_partner_count",
    )

    @api.depends("name", "active", "company_id")
    def _compute_partner_count(self):
        Partner = self.env["res.partner"]
        for role in self:
            if not role.id:
                role.partner_count = 0
            else:
                role.partner_count = Partner.search_count(
                    [("membership_role_ids", "in", role.id)]
                )

    def action_open_contacts_with_role(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Contacts avec ce rôle"),
            "res_model": "res.partner",
            "view_mode": "list,form",
            "domain": [("membership_role_ids", "in", [self.id])],
            "context": {"default_is_company": False},
        }

    @api.constrains("name", "company_id")
    def _check_name_company_uniqueness(self):
        for role in self:
            normalized_name = (role.name or "").strip()
            if not normalized_name:
                continue
            duplicates = self.search_count(
                [
                    ("id", "!=", role.id),
                    ("name", "=ilike", normalized_name),
                    ("company_id", "=", role.company_id.id if role.company_id else False),
                ]
            )
            if duplicates:
                raise ValidationError(
                    _(
                        "Un rôle portant le même nom existe déjà pour ce périmètre (société). "
                        "Choisissez un autre libellé ou une autre société."
                    )
                )
