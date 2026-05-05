# -*- coding: utf-8 -*-
"""Migration 19.0.1.10.77 : whitelist champ ``referred`` formulaires CRM + MVP03."""

from odoo.addons.dorevia_ckreyol_marketplace.hooks import (
    _whitelist_crm_lead_referred_for_website_form,
)


def migrate(cr, version):
    _whitelist_crm_lead_referred_for_website_form(cr)
