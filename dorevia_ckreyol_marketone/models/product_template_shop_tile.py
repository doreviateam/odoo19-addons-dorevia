# -*- coding: utf-8 -*-
"""Dérivé média catalogue — image normalisée (doctrine image v2)."""

from odoo import api, fields, models

# Doctrine v2 — DOCTRINE_IMAGE_V2.md
SHOP_TILE_STATUS = [
    ("none", "Aucune"),
    ("validated_grid", "Validée pour affichage catalogue"),
    ("validated_storage", "Validée — stockage uniquement"),
    ("validated_reserve", "Validée avec réserve"),
    ("pending_review", "En revue"),
    ("needs_review_source", "Source à revoir"),
    ("rejected", "Rejetée"),
    # Legacy pilote P7/P8 — équivalent validated_storage (non affiché).
    ("validated", "Validée (historique pilote)"),
]

CONFIG_KEY_SHOP_TILE_ENABLED = "marketone.shop_tile_enabled"

# Statuts autorisés pour affichage grille /shop (doctrine v2).
SHOP_TILE_GRID_DISPLAY_STATUSES = frozenset({"validated_grid"})


class ProductTemplate(models.Model):
    _inherit = "product.template"

    image_shop_tile = fields.Image(
        string="Vignette catalogue normalisée",
        max_width=1024,
        max_height=1024,
        attachment=True,
        help="Dérivé média pour la grille boutique. Ne remplace pas l'image produit principale.",
    )
    shop_tile_status = fields.Selection(
        selection=SHOP_TILE_STATUS,
        string="Statut média catalogue",
        default="none",
    )
    shop_tile_recipe_version = fields.Char(
        string="Version recette pipeline",
        help="Version recette pipeline, ex. ck_shop_tile_v1.1",
    )
    shop_tile_processed_at = fields.Datetime(string="Traité le")
    shop_tile_source_run = fields.Char(
        string="Identifiant run batch",
        help="Identifiant run batch, ex. pilote_20260520",
    )
    shop_tile_moa_note = fields.Char(string="Note qualité visuelle")

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
