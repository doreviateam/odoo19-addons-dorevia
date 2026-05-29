# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    glc_default_bank_journal_id = fields.Many2one(
        "account.journal",
        string="Journal bancaire cockpit GLC",
        domain="[('type', '=', 'bank'), ('company_id', '=', id)]",
        help="Journal du compte courant utilisé par défaut pour la lecture "
        "trésorerie du cockpit GLC (Palier 5).",
    )
