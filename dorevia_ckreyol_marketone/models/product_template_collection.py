# -*- coding: utf-8 -*-
"""Rattachement produit ↔ collections commerciales (Lot A)."""

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    marketone_collection_ids = fields.Many2many(
        comodel_name="marketone.shop.collection",
        relation="marketone_shop_collection_product_rel",
        column1="product_id",
        column2="collection_id",
        string="Collections commerciales",
    )
