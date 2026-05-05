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

    ckr_callback_date = fields.Date(
        string="Date souhaitée (rappel)",
        tracking=False,
    )

    ckr_callback_window = fields.Selection(
        selection=[
            ("h09_11", "09h–11h"),
            ("h11_13", "11h–13h"),
            ("h14_16", "14h–16h"),
            ("h16_18", "16h–18h"),
        ],
        string="Créneau horaire (rappel)",
        tracking=False,
    )

    # Synthèse lisible pour la liste / recherche (remplie depuis date + fenêtre au dépôt web).
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
        creneau_line = self._ckr_format_rappel_creneau_line(values)
        if creneau_line:
            values["ckr_callback_slot"] = creneau_line

        header = f"[{label}]"
        blocks = [header]
        if msg:
            blocks.append(msg)
        if creneau_line:
            blocks.append(creneau_line)
        values["description"] = "\n\n".join(blocks)

        return values

    def _ckr_format_rappel_creneau_line(self, values):
        """Construit ``Créneau souhaité : JJ/MM/AAAA — 09h–11h`` depuis date + fenêtre."""
        raw_date = values.get("ckr_callback_date")
        win_key = values.get("ckr_callback_window")
        if not raw_date or not win_key:
            return ""

        if isinstance(raw_date, str):
            d = fields.Date.from_string(raw_date)
        else:
            d = raw_date
        if not d:
            return ""

        # Website / ORM peuvent envoyer ``datetime`` ou ``date``.
        if hasattr(d, "date") and callable(getattr(d, "date")):
            try:
                d = d.date()
            except (ValueError, TypeError):
                return ""

        date_fr = d.strftime("%d/%m/%Y")

        sel = self._fields["ckr_callback_window"].selection
        pairs = sel(self) if callable(sel) else sel
        labels = dict(pairs)
        win_label = labels.get(win_key, win_key)

        return f"Créneau souhaité : {date_fr} — {win_label}"
