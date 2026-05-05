# -*- coding: utf-8 -*-
"""Pont formulaire Website (website_crm) — demande compte pro MVP03."""

from odoo import models

# Valeur attendue du champ ``referred`` (formulaire page dédiée, champ masqué).
CKR_MVP03_FORM_REFERRED = "CK-MVP03-demande-compte-pro"

# Libellé métier — traçabilité CRM / ticket MVP03.
CKR_MVP03_LEAD_LABEL = "Demande compte pro C-Kreyol MVP03"


class CrmLead(models.Model):
    _inherit = "crm.lead"

    def website_form_input_filter(self, request, values):
        values = super().website_form_input_filter(request, values)
        if values.get("referred") != CKR_MVP03_FORM_REFERRED:
            return values
        company = (values.get("partner_name") or "").strip()
        contact = (values.get("contact_name") or "").strip()
        label = request.env._(CKR_MVP03_LEAD_LABEL)
        if company:
            values["name"] = f"{label} — {company}"
        elif contact:
            values["name"] = f"{label} — {contact}"
        else:
            values["name"] = label
        desc = (values.get("description") or "").strip()
        header = f"[{CKR_MVP03_LEAD_LABEL}]"
        if desc and not desc.startswith(header):
            values["description"] = f"{header}\n\n{desc}"
        elif not desc:
            values["description"] = header
        return values
