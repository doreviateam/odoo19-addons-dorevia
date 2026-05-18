# -*- coding: utf-8 -*-
"""Profil éditorial minimal pour la porte Origines (univers Boutique)."""

import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class MarketoneShopOrigin(models.Model):
    _name = "marketone.shop.origin"
    _description = "Marketone — profil origine (porte /shop)"
    _order = "sequence, name_visitor, id"

    attribute_value_id = fields.Many2one(
        comodel_name="product.attribute.value",
        string="Valeur attribut Origine",
        required=True,
        ondelete="cascade",
        index=True,
    )
    name_visitor = fields.Char(string="Nom visiteur", translate=True)
    context_phrase = fields.Char(string="Phrase courte", translate=True)
    slug = fields.Char(required=True, index=True)
    sequence = fields.Integer(default=10)
    website_id = fields.Many2one(
        comodel_name="website",
        string="Site web",
        ondelete="cascade",
        index=True,
    )
    website_published = fields.Boolean(string="Publié", default=True)
    display_name_visitor = fields.Char(
        compute="_compute_display_name_visitor",
    )

    _marketone_origin_slug_website_uniq = models.Constraint(
        "unique(website_id, slug)",
        "Le slug d'origine doit être unique par site.",
    )
    _marketone_origin_value_website_uniq = models.Constraint(
        "unique(website_id, attribute_value_id)",
        "Une seule ligne par valeur d'attribut et par site.",
    )

    @api.depends("name_visitor", "attribute_value_id.name")
    def _compute_display_name_visitor(self):
        for record in self:
            record.display_name_visitor = (
                record.name_visitor or record.attribute_value_id.name or ""
            )

    @api.constrains("slug")
    def _check_slug_format(self):
        for record in self:
            slug = (record.slug or "").strip()
            if not slug:
                raise ValidationError(_("Le slug d'origine ne peut pas être vide."))
            if not _SLUG_RE.match(slug):
                raise ValidationError(
                    _(
                        "Le slug « %s » est invalide : minuscules, chiffres "
                        "et tirets uniquement."
                    )
                    % slug
                )

    @api.model
    def _marketone_resolve_published_slugs(self, slugs, website=None):
        """Profils publiés pour les slugs demandés (ordre conservé, slugs inconnus ignorés)."""
        normalized = []
        seen = set()
        for raw in slugs or ():
            value = (raw or "").strip().lower()
            if not value or value in seen:
                continue
            seen.add(value)
            normalized.append(value)
        if not normalized:
            return self.browse()

        domain = [("slug", "in", normalized), ("website_published", "=", True)]
        if website is not None:
            domain.append(("website_id", "in", [False, website.id]))

        records = self.sudo().search(domain)
        by_slug = {rec.slug: rec for rec in records}
        return self.browse([by_slug[s].id for s in normalized if s in by_slug])
