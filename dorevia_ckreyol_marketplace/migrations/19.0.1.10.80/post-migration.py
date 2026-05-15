# -*- coding: utf-8 -*-
"""Migration 19.0.1.10.80 : whitelist ``ckr_activity_type`` (formulaire demande pro)."""

from odoo.addons.dorevia_ckreyol_marketplace.hooks import _whitelist_crm_lead_pro_form_fields


def migrate(cr, version):
    _whitelist_crm_lead_pro_form_fields(cr)
