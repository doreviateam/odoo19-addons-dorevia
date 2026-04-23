# -*- coding: utf-8 -*-
"""Extension ``product.public.category`` — porte Explorer **Catégories**.

Matérialise la convergence boutique via l’**URL native** Odoo
``/shop/category/<id>-<slug>`` (contrôleur ``website_sale``), sans
paramètre ``ckr_mode`` : le filtrage produit est entièrement celui du
standard (taxonomie ``product.public.category``).

Le point d’entrée **URL courte visiteur** ``/categories`` est résolu en
**redirection HTTP 301** vers cette URL native — voir
``docs/phase_2/CONTRAT_URL_CATEGORIES.md`` §12 (**Hybride H1 — cible
native**).
"""
from odoo import api, models


CKR_EXPLORER_PUBLIC_CATEGORY_PARAM = (
    "dorevia_ckreyol_marketplace.explorer_public_category_id"
)


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    @api.model
    def _ckr_get_explorer_entry_shop_path(self, website):
        """Chemin relatif ``/shop/category/<id>-<slug>`` pour la carte Explorer.

        :param website: ``website.website`` courant (obligatoire en pratique).
        :returns: chaîne commençant par ``/shop/category/``, ou ``None`` si
            aucune catégorie publique exploitable n’est trouvée (l’alias
            ``/categories`` retombera alors sur ``/shop`` nu).

        **Résolution** (dans l’ordre) :

        1. ``ir.config_parameter`` ``dorevia_ckreyol_marketplace.explorer_public_category_id``
           : id numérique d’une ``product.public.category`` **valide** pour le
           site (``website_id`` vide ou égal au site courant).
        2. **Sinon** : première **racine** de l’arbre (``parent_id`` absent),
           filtrée par site, tri ``sequence, id``, limite 1.

        Aucune donnée n’est dupliquée : la source de vérité reste le modèle
        standard Odoo et les rattachements produits existants.
        """
        if not website:
            return None
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

        if not category:
            return None

        # Aligné sur ``website_sale.controllers.main.WebsiteSale._get_shop_path`` :
        # slug via ``ir.http._slug`` (Odoo 19 — plus d’export ``slug`` depuis
        # ``http_routing.models.ir_http``).
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
