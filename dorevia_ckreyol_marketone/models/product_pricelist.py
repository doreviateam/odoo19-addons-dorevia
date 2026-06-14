# -*- coding: utf-8 -*-
"""Extension ``product.pricelist`` — source de vérité porte Promotions (C3.D).

Un ``product.template`` est « en promotion » pour le visiteur ssi il existe,
sur **la pricelist courante**, au moins un ``product.pricelist.item`` actif et
strictement réducteur. Aucune notion promo parallèle côté Marketone.

**Limites documentées (règles Odoo complexes)** :

* ``compute_price=fixed`` sur ``2_product_category`` / ``3_global`` : l'item
  est retenu comme réducteur par prudence (comparaison ``list_price`` impossible
  au niveau item seul) — cf. ``_marketone_pricelist_item_is_reducer``.
* ``formula`` : seul ``price_discount > 0`` est pris en compte ; surcharges /
  arrondis peuvent marginalement fausser le caractère réducteur.
* ``sale_loyalty`` / coupons : hors scope Lot 6.3a — point d'union ouvert en fin
  de ``_marketone_get_promo_template_ids``.
"""
from odoo import fields, models
from odoo.http import request


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    def _marketone_get_promo_template_ids(self, website=None, pricelist=None):
        """Ids ``product.template`` en promotion pour la pricelist courante.

        :returns:
            * ``None`` — promo globale ``3_global`` active (pas de filtre produit).
            * ``set()`` — aucune promo active (état vide porte).
            * ``set`` non vide — ids templates éligibles.
        """
        pricelist = pricelist or self._marketone_resolve_visitor_pricelist(website)
        if not pricelist:
            return set()

        Item = self.env["product.pricelist.item"].sudo()
        items = Item.search(
            self._marketone_active_pricelist_items_domain(
                pricelist, fields.Datetime.now()
            )
        )

        template_ids = set()
        categ_ids_promo = set()
        global_is_promo = False

        for item in items:
            if not self._marketone_pricelist_item_is_reducer(item):
                continue
            applied = item.applied_on
            if applied == "0_product_variant" and item.product_id:
                template_ids.add(item.product_id.product_tmpl_id.id)
            elif applied == "1_product" and item.product_tmpl_id:
                template_ids.add(item.product_tmpl_id.id)
            elif applied == "2_product_category" and item.categ_id:
                categ_ids_promo.add(item.categ_id.id)
            elif applied == "3_global":
                global_is_promo = True

        if global_is_promo:
            return None

        if categ_ids_promo:
            templates_in_categ = self.env["product.template"].sudo().search(
                [
                    ("categ_id", "child_of", list(categ_ids_promo)),
                    ("is_published", "=", True),
                ]
            )
            template_ids.update(templates_in_categ.ids)

        return template_ids

    def _marketone_resolve_visitor_pricelist(self, website=None):
        """Pricelist courante visiteur — chaîne alignée ``website_sale`` (C3.D / M7)."""
        if website is None:
            website = self.env["website"].get_current_website(fallback=False)
        if not website:
            website = self.env["website"].sudo().search([], limit=1)

        pricelist = self.env["product.pricelist"]
        if request and getattr(request, "pricelist", None):
            pricelist = request.pricelist
        elif website:
            pricelist = website._get_and_cache_current_pricelist()

        if not pricelist:
            partner = self.env.user.partner_id
            if partner:
                pricelist = partner.property_product_pricelist
                if website and pricelist:
                    available = website.get_pricelist_available()
                    if available and pricelist not in available:
                        pricelist = available[0]

        if not pricelist and website:
            available = website.get_pricelist_available()
            if available:
                pricelist = available[0]

        if not pricelist:
            pricelist = self.env["product.pricelist"].search([], limit=1)

        return pricelist

    def _marketone_active_pricelist_items_domain(self, pricelist, now):
        """Items actifs sur la pricelist à l'instant ``now``."""
        return [
            ("pricelist_id", "=", pricelist.id),
            "|",
            ("date_start", "=", False),
            ("date_start", "<=", now),
            "|",
            ("date_end", "=", False),
            ("date_end", ">=", now),
        ]

    def _marketone_pricelist_item_is_reducer(self, item):
        """True si l'item applique une remise stricte."""
        compute = item.compute_price
        if compute == "percentage":
            return bool(item.percent_price) and item.percent_price > 0.0
        if compute == "formula":
            return bool(item.price_discount) and item.price_discount > 0.0
        if compute == "fixed":
            if not item.fixed_price:
                return False
            if item.applied_on == "0_product_variant" and item.product_id:
                return item.fixed_price < item.product_id.list_price
            if item.applied_on == "1_product" and item.product_tmpl_id:
                return item.fixed_price < item.product_tmpl_id.list_price
            return True
        return False
