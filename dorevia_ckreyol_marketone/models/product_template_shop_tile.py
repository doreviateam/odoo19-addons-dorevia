# -*- coding: utf-8 -*-
"""Tuile commerce /shop — image dérivée (V1.5 lite · doctrine image v2)."""

from odoo import api, fields, models

# Doctrine v2 — DOCTRINE_IMAGE_V2.md
SHOP_TILE_STATUS = [
    ("none", "Aucune"),
    ("validated_grid", "Validée grille /shop"),
    ("validated_storage", "Validée stockage (non affichée)"),
    ("validated_reserve", "Validée avec réserve"),
    ("pending_review", "En revue"),
    ("needs_review_source", "Source à revoir"),
    ("rejected", "Rejetée"),
    # Legacy pilote P7/P8 — équivalent validated_storage (non affiché).
    ("validated", "Validée (legacy pilote)"),
]

CONFIG_KEY_SHOP_TILE_ENABLED = "marketone.shop_tile_enabled"

# Statuts autorisés pour affichage grille /shop (doctrine v2).
SHOP_TILE_GRID_DISPLAY_STATUSES = frozenset({"validated_grid"})


class ProductTemplate(models.Model):
    _inherit = "product.template"

    image_shop_tile = fields.Image(
        string="Tuile /shop",
        max_width=1024,
        max_height=1024,
        attachment=True,
        help="Image dérivée normalisée pour la grille /shop uniquement. "
        "Ne remplace pas image_1920.",
    )
    shop_tile_status = fields.Selection(
        selection=SHOP_TILE_STATUS,
        string="Statut tuile /shop",
        default="none",
    )
    shop_tile_recipe_version = fields.Char(
        string="Recette tuile",
        help="Version recette CLI, ex. ck_shop_tile_v1.1",
    )
    shop_tile_processed_at = fields.Datetime(string="Tuile traitée le")
    shop_tile_source_run = fields.Char(
        string="Run source CLI",
        help="Identifiant run batch, ex. pilote_20260520",
    )
    shop_tile_moa_note = fields.Char(string="Note MOA tuile")

    @api.model
    def _marketone_shop_tile_feature_enabled(self):
        value = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(CONFIG_KEY_SHOP_TILE_ENABLED, "False")
        )
        return value in ("True", "1", "true")

    def marketone_use_shop_tile_on_grid(self):
        """True si la grille /shop doit afficher ``image_shop_tile``.

        Doctrine v2 (DOCTRINE_IMAGE_V2.md) :
        - seul ``validated_grid`` active le dérivé en grille ;
        - sinon fallback ``image_1920`` (comportement QWeb standard) ;
        - ``validated`` legacy pilote = stockage, non affiché.
        """
        self.ensure_one()
        if not self._marketone_shop_tile_feature_enabled() or not self.image_shop_tile:
            return False
        return (self.shop_tile_status or "none") in SHOP_TILE_GRID_DISPLAY_STATUSES
