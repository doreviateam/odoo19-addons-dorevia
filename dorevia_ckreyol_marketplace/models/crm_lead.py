# -*- coding: utf-8 -*-
"""Pont formulaire Website (website_crm) — demande compte pro MVP03."""

from odoo import fields, models

# Valeur attendue du champ ``referred`` (formulaire page dédiée, champ masqué).
CKR_MVP03_FORM_REFERRED = "CK-MVP03-demande-compte-pro"

# Libellé métier — traçabilité CRM / ticket MVP03.
CKR_MVP03_LEAD_LABEL = "Demande compte pro C-Kreyol MVP03"


class CrmLead(models.Model):
    _inherit = "crm.lead"

    ckr_activity_type = fields.Selection(
        selection=[
            ("boutique_epicerie", "Boutique / épicerie fine"),
            ("restaurant_traiteur", "Restaurant / traiteur"),
            ("distributeur", "Distributeur"),
            ("collectivite_ce", "Collectivité / comité d'entreprise"),
            ("association", "Association / organisation"),
            ("autre", "Autre"),
        ],
        string="Type d'activité",
        tracking=False,
    )

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

        act_key = values.get("ckr_activity_type")
        if act_key:
            sel = self._fields["ckr_activity_type"].selection
            pairs = sel(self) if callable(sel) else sel
            labels = dict(pairs)
            line_fr = f"\n\nType d'activité : {labels.get(act_key, act_key)}"
            values["description"] = (values.get("description") or "").rstrip() + line_fr

        return values
