# -*- coding: utf-8 -*-
"""Migration 19.0.1.10.93 : whitelist ``ckr_callback_slot`` (formulaire rappel MVP03+)."""

from odoo.addons.dorevia_ckreyol_marketplace.hooks import _whitelist_crm_lead_pro_form_fields


def migrate(cr, version):
    _whitelist_crm_lead_pro_form_fields(cr)
