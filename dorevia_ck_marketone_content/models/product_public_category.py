# -*- coding: utf-8 -*-
from odoo import api, fields, models

from ..ck_catalog_exposure import CK_CATEGORY_ACTIVE_MIN_PRODUCTS


class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    # Homepage « Nos coups de cœur » pilotée par product.template.ck_is_featured
    # depuis 19.0.1.28.3 — plus de refresh sur write catégorie.

    ck_exposure_status = fields.Selection([
        ('active',   'Active — rayon principal'),
        ('promise',  'Promesse — bloc éditorial uniquement'),
        ('hidden',   'Masquée — structurante BO seulement'),
        ('draft',    'Brouillon — en préparation'),
        ('archived', 'Archivée'),
    ], string="Statut d'exposition CK", default='active', required=True, index=True,
       help="Intention MOA d'exposition publique CK (CATALOG-ARCHI-001). "
            "Distinct de la publication technique Odoo (website_published) : "
            "l'exposition réelle en nav/Home/footer/SEO dépend en plus du "
            "nombre de produits qualifiés — voir _is_ck_exposable().")

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

    def _ck_exposable_products_count(self):
        """Produits publiés/vendables rattachés (soi + descendants) — CATALOG-ARCHI-001."""
        self.ensure_one()
        Category = self.env['product.public.category'].sudo()
        Product = self.env['product.template'].sudo()
        all_children = Category.search([('id', 'child_of', self.id)])
        return Product.search_count([
            ('sale_ok', '=', True),
            ('is_published', '=', True),
            ('website_published', '=', True),
            ('public_categ_ids', 'in', all_children.ids),
        ])

    def _is_ck_exposable(self):
        """Éligibilité réelle d'exposition CK (nav/Home/footer/SEO) — CATALOG-ARCHI-001 §5.

        NB : `product.public.category` standard Odoo 19 n'a pas de champ
        `website_published` (contrairement à ce que suppose la note MOA §5.1) —
        seul `has_published_products` existe nativement, sans seuil ni notion
        de qualification. La "publication technique" d'une catégorie se réduit
        donc ici au fait d'avoir au moins un produit qualifié rattaché, ce que
        le calcul de seuil ci-dessous couvre déjà.
        Combine l'intention MOA (ck_exposure_status) et la maturité commerciale
        réelle (nombre de produits qualifiés). Exception §6.3 : 2 produits
        acceptés si la catégorie porte déjà un titre + une description éditoriale.
        """
        self.ensure_one()
        if self.ck_exposure_status != 'active':
            return False
        count = self._ck_exposable_products_count()
        if count >= CK_CATEGORY_ACTIVE_MIN_PRODUCTS:
            return True
        if count == 2 and self.show_category_description and (self.website_description or '').strip():
            return True
        return False
