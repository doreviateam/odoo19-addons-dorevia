# -*- coding: utf-8 -*-
"""Inscriptions « cercle C-Kreyol » (newsletter légère, sans automation).

Stockage propre côté Odoo (pas d’intégration externe MVP). Le contrôleur
public crée en ``sudo()`` ; l’accès direct au modèle est réservé au back-office.
"""
import re
import secrets

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_CKR_EMAIL_RE = re.compile(
    r"^[^\s@]+@[^\s@]+\.[^\s@]{2,}$",
    re.IGNORECASE,
)


def _ckr_circle_normalize_email(value):
    if not value or not isinstance(value, str):
        return False
    n = " ".join(value.split()).lower()
    if not n or len(n) > 255:
        return False
    if not _CKR_EMAIL_RE.match(n):
        return False
    return n


class CkrCircleSubscriber(models.Model):
    _name = "ckr.circle.subscriber"
    _description = "C-Kreyol — Inscription au cercle (newsletter)"
    _rec_name = "email"
    _order = "create_date desc, id desc"

    @api.model
    def normalize_incoming_email(self, value):
        """Entrée formulaire public : normalise ou retourne False."""
        return _ckr_circle_normalize_email(value)

    email = fields.Char(required=True, index=True, copy=False)
    website_id = fields.Many2one(
        "website",
        string="Site web",
        required=True,
        ondelete="cascade",
        index=True,
    )
    opt_offers = fields.Boolean(string="Offres", default=False)
    opt_recipes = fields.Boolean(string="Recettes", default=False)
    opt_news = fields.Boolean(string="Nouveautés", default=False)
    active = fields.Boolean(default=True)
    unsubscribe_token = fields.Char(
        string="Jeton de désinscription",
        copy=False,
        required=True,
        index=True,
    )

    _ckr_circle_subscriber_email_website_uniq = models.Constraint(
        "unique(website_id, email)",
        "Une inscription existe déjà pour cet e-mail sur ce site.",
    )

    @api.constrains("email")
    def _ckr_check_email(self):
        for rec in self:
            n = _ckr_circle_normalize_email(rec.email)
            if not n:
                raise ValidationError(
                    "Adresse e-mail invalide. Merci d’en saisir une correcte."
                )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("email"):
                vals["email"] = _ckr_circle_normalize_email(vals["email"])
            wid = vals.get("website_id")
            if vals.get("email") and wid:
                if self.search_count(
                    [("email", "=", vals["email"]), ("website_id", "=", wid)],
                    limit=2,
                ):
                    raise ValidationError(
                        "Une inscription existe déjà pour cet e-mail sur ce site."
                    )
            if not vals.get("unsubscribe_token"):
                vals["unsubscribe_token"] = secrets.token_urlsafe(32)
        return super().create(vals_list)

    def write(self, vals):
        if "email" in vals and vals.get("email"):
            vals = dict(vals)
            vals["email"] = _ckr_circle_normalize_email(vals["email"])
        return super().write(vals)
