# -*- coding: utf-8 -*-
"""Pont formulaire Website (website_crm) — demande compte pro MVP03."""

from odoo import fields, models

# Valeur attendue du champ ``referred`` (formulaire page dédiée, champ masqué).
CKR_MVP03_FORM_REFERRED = "CK-MVP03-demande-compte-pro"

# Formulaire secondaire « être rappelé » (MVP03+, même page).
CKR_MVP03_RAPPEL_REFERRED = "CK-MVP03-rappel-conseiller"

# Libellé métier — traçabilité CRM / ticket MVP03.
CKR_MVP03_LEAD_LABEL = "Demande compte pro C-Kreyol MVP03"

CKR_MVP03_RAPPEL_LABEL = "Rappel conseiller C-Kreyol MVP03"


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

    ckr_callback_slot = fields.Char(
        string="Créneau souhaité (rappel)",
        tracking=False,
    )

    def website_form_input_filter(self, request, values):
        values = super().website_form_input_filter(request, values)
        ref = values.get("referred")
        if ref == CKR_MVP03_FORM_REFERRED:
            return self._ckr_mvp03_apply_demande_pro(request, values)
        if ref == CKR_MVP03_RAPPEL_REFERRED:
            return self._ckr_mvp03_apply_rappel(request, values)
        return values

    def _ckr_mvp03_apply_demande_pro(self, request, values):
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

    def _ckr_mvp03_apply_rappel(self, request, values):
        label = request.env._(CKR_MVP03_RAPPEL_LABEL)
        contact = (values.get("contact_name") or "").strip()
        phone = (values.get("phone") or "").strip()
        email = (values.get("email_from") or "").strip()
        if contact:
            values["name"] = f"{label} — {contact}"
        elif phone:
            values["name"] = f"{label} — {phone}"
        elif email:
            values["name"] = f"{label} — {email}"
        else:
            values["name"] = label

        msg = (values.get("description") or "").strip()
        slot = (values.get("ckr_callback_slot") or "").strip()
        header = f"[{label}]"
        blocks = [header]
        if msg:
            blocks.append(msg)
        if slot:
            blocks.append(f"Créneau souhaité : {slot}")
        values["description"] = "\n\n".join(blocks)

        return values
