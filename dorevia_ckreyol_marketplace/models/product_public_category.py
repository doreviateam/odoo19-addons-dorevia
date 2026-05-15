# -*- coding: utf-8 -*-
"""Extension ``product.public.category`` — porte Explorer **Catégories**.

Doctrine **conteneur unique** : l’alias visiteur ``/categories`` converge
vers ``/shop?ckr_category=<slug>`` (filtre ``website_sale`` via
``ProductTemplate._search_get_detail``, même sémantique que la grille
catégorie sans chemins parallèles ``/shop/category/…`` en entrée).

Le helper ``_ckr_get_explorer_entry_shop_path`` conserve la forme native
``/shop/category/<id>-<slug>`` pour les rares cas (tests, liens internes).
"""
from odoo import api, models


CKR_EXPLORER_PUBLIC_CATEGORY_PARAM = (
    "dorevia_ckreyol_marketplace.explorer_public_category_id"
)


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    @api.model
    def _ckr_resolve_explorer_public_category(self, website):
        """Catégorie d’entrée Explorer (paramètre système ou première racine).

        :returns: ``product.public.category`` (0 ou 1 enregistrement).
        """
        if not website:
            return self.env["product.public.category"].browse()
        website = website.sudo()
        Category = self.env["product.public.category"].sudo()
        ICP = self.env["ir.config_parameter"].sudo()

        raw = ICP.get_param(CKR_EXPLORER_PUBLIC_CATEGORY_PARAM, default="") or ""
        category = Category.browse()
        if raw.strip().isdigit():
            cid = int(raw.strip())
            if cid > 0:
                candidate = Category.browse(cid)
                if candidate.exists() and self._ckr_category_valid_for_website(
                    candidate, website
                ):
                    category = candidate

        if not category:
            category = Category.search(
                self._ckr_explorer_root_domain(website), order="sequence, id", limit=1
            )
        return category

    @api.model
    def _ckr_get_explorer_entry_shop_path(self, website):
        """Chemin relatif **natif** ``/shop/category/<id>-<slug>`` (legacy).

        Préférer l’alias ``/categories`` → ``/shop?ckr_category=…`` pour la
        navigation visiteur (doctrine conteneur unique).
        """
        category = self._ckr_resolve_explorer_public_category(website)
        if not category:
            return None
        slug = self.env["ir.http"].sudo()._slug
        return "/shop/category/%s" % slug(category)

    @api.model
    def _ckr_category_valid_for_website(self, category, website):
        """True ssi la catégorie est exposable sur le site courant."""
        if not category.exists():
            return False
        wid = category.website_id
        if wid and wid != website:
            return False
        return True

    @api.model
    def _ckr_explorer_root_domain(self, website):
        """Domaine des racines de catégories publiques pour le site."""
        return [
            ("parent_id", "=", False),
            "|",
            ("website_id", "=", False),
            ("website_id", "=", website.id),
        ]
