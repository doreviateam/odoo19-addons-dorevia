# -*- coding: utf-8 -*-
"""Collections commerciales Marketone — Lot A (BO uniquement, ADR-030)."""

import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

_PUBLISHED_PRODUCT_DOMAIN = [
    ("sale_ok", "=", True),
    ("website_published", "=", True),
]


class MarketoneShopCollection(models.Model):
    _name = "marketone.shop.collection"
    _description = "Marketone — collection commerciale"
    _order = "sequence, name, id"

    name = fields.Char(required=True, translate=True)
    slug = fields.Char(required=True, index=True)
    teaser = fields.Char(string="Description courte", translate=True)
    image = fields.Image(string="Image")
    product_ids = fields.Many2many(
        comodel_name="product.template",
        relation="marketone_shop_collection_product_rel",
        column1="collection_id",
        column2="product_id",
        string="Produits",
        domain=_PUBLISHED_PRODUCT_DOMAIN,
    )
    product_count = fields.Integer(
        string="Produits publiés",
        compute="_compute_product_count",
    )
    date_start = fields.Date(string="Date de début")
    date_end = fields.Date(string="Date de fin")
    website_published = fields.Boolean(string="Publié", default=False)
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)
    website_id = fields.Many2one(
        comodel_name="website",
        string="Site web",
        ondelete="cascade",
        index=True,
    )
    homepage_featured = fields.Boolean(
        string="Mise en avant homepage (préparation)",
        default=False,
        help="Sans effet visiteur en Lot A — réservé Lot C.",
    )

    _marketone_collection_slug_website_uniq = models.Constraint(
        "unique(website_id, slug)",
        "Le slug de collection doit être unique par site.",
    )

    @api.depends("product_ids", "product_ids.sale_ok", "product_ids.website_published")
    def _compute_product_count(self):
        for record in self:
            record.product_count = len(
                record.product_ids.filtered(
                    lambda product: product.sale_ok and product.website_published
                )
            )

    @api.constrains("slug")
    def _check_slug_format(self):
        for record in self:
            slug = (record.slug or "").strip()
            if not slug:
                raise ValidationError(_("Le slug de collection ne peut pas être vide."))
            if not _SLUG_RE.match(slug):
                raise ValidationError(
                    _(
                        "Le slug « %s » est invalide : minuscules, chiffres "
                        "et tirets uniquement."
                    )
                    % slug
                )

    @api.constrains("date_start", "date_end")
    def _check_date_range(self):
        for record in self:
            if record.date_start and record.date_end and record.date_end < record.date_start:
                raise ValidationError(
                    _("La date de fin doit être postérieure ou égale à la date de début.")
                )

    @api.constrains("website_published", "product_ids")
    def _check_published_requires_sellable_products(self):
        """MOA : publiée ⇒ ≥ 1 produit vendable publié ; brouillon peut être vide."""
        for record in self:
            if not record.website_published:
                continue
            if record._marketone_sellable_product_ids():
                continue
            raise ValidationError(
                _(
                    "Une collection publiée doit contenir au moins un produit "
                    "vendable et publié sur le site."
                )
            )

    def _marketone_sellable_product_ids(self):
        self.ensure_one()
        return self.product_ids.filtered(
            lambda product: product.sale_ok and product.website_published
        )
