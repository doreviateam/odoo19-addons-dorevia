# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    # Homepage « Nos coups de cœur » pilotée par product.template.ck_is_featured
    # depuis 19.0.1.28.3 — plus de refresh sur write catégorie.

    ck_universe = fields.Selection([
        ('epicerie',   'Épicerie'),
        ('boissons',   'Boissons'),
        ('soin',       'Soin & bien-être'),
        ('artisanat',  'Artisanat'),
    ], string="Univers CK", index=True,
       help="Univers éditorial de la catégorie racine. Les sous-catégories héritent "
            "automatiquement de l'univers de leur ancêtre — ne pas renseigner sur les enfants.")

    ck_subtitle = fields.Char(
        string="Accroche banner univers",
        help="Accroche courte affichée dans le banner d'entrée d'univers "
             "(catégories niveau 0 uniquement). Laisser vide pour masquer le bloc accroche.")

    def _get_ck_universe(self):
        """Remonte l'arborescence pour trouver le premier ck_universe défini."""
        self.ensure_one()
        cat = self
        while cat:
            if cat.ck_universe:
                return cat.ck_universe
            cat = cat.parent_id
        return None

    @api.model
    def get_ck_shop_banner(self, category=None):
        """Point d'entrée unique pour la bannière shop et catégories.

        Appelé depuis le template QWeb avec category=False (page /shop)
        ou category=<record> (page catégorie).  Retourne toujours un dict
        {title, phrase} — avec families/highlights/proof en plus pour Épicerie
        quand les seuils sont atteints.
        """
        from ..shop_rayon_editorial import get_rayon_editorial
        return get_rayon_editorial(self.env, category or None)

    def get_ck_rayon_editorial(self):
        """Contenu éditorial de rayon P2B (cf. shop_rayon_editorial.py)."""
        self.ensure_one()
        from ..shop_rayon_editorial import get_rayon_editorial
        return get_rayon_editorial(self.env, self)

    def get_ck_category_family_tiles(self):
        """Tuiles visuelles des enfants directs (Note 07 Lot B), ou []."""
        self.ensure_one()
        from ..shop_category_tiles import get_ck_category_family_tiles
        return get_ck_category_family_tiles(self.env, self)
