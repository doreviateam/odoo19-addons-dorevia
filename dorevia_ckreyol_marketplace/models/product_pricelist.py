# -*- coding: utf-8 -*-
"""Extension de ``product.pricelist`` — source de vérité A2 « Promotions ».

Matérialise la décision actée dans
``docs/phase_2/CONTRAT_URL_PROMOTIONS.md`` §5 (option **A2 — Pricelist
datée avec remise**) : la source de vérité de la porte Promotions est
**le mécanisme prix standard d'Odoo**, et rien d'autre.

Un ``product.template`` est « en promotion » pour le visiteur courant ssi
il existe, sur **la pricelist courante du visiteur**, au moins un
``product.pricelist.item`` :

* **actif à l'instant t** (bornes ``date_start`` / ``date_end`` ouvertes
  ou englobant ``now``) ;
* **strictement réducteur** (cf. ``_ckr_item_is_reducer``) — on rejette
  les items neutres ou les mark-ups (ex. ``percent_price=0``,
  ``fixed_price >= list_price``…).

Cette extension **ne réinvente pas** de notion « promo » côté CK : la
définition est entièrement adossée au moteur de prix Odoo standard.
Aucune donnée n'est persistée côté CK ; tout est déduit à la volée de
``product.pricelist.item``.

**Extensibilité A3 (loyalty ``program_type='promotion'``)** : ouverte
comme extension future (CONTRAT_URL_PROMOTIONS §6). Le point
d'entrée pour l'union est la fin de ``_ckr_get_promo_template_ids`` ;
il suffira de fusionner avec l'ensemble des ids éligibles aux
``loyalty.program`` actifs type ``promotion`` sur le site.
"""
from odoo import fields, models


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    # ------------------------------------------------------------------
    # Point d'entrée unique utilisé par le contrôleur et par
    # ProductTemplate._search_get_detail (option ckr_promo_only).
    # ------------------------------------------------------------------
    def _ckr_get_promo_template_ids(self, website=None, pricelist=None):
        """Ids ``product.template`` « en promotion » pour le visiteur courant.

        :param website: ``website.website`` (optionnel). À défaut, fall-back
            sur le premier website publié (contexte hors requête HTTP, ex.
            appel depuis un test ou un cron ultérieur).
        :param pricelist: ``product.pricelist`` (optionnel). À défaut,
            résolution via la chaîne standard Odoo (cf. ci-dessous). Fournir
            une pricelist explicite est utile pour les tests et pour toute
            résolution hors contexte HTTP.

        :returns:

            * ``None`` → **cas « global promo »** : il existe au moins un
              item actif strictement réducteur appliqué à ``3_global`` sur
              la pricelist courante → toute la boutique est en promotion,
              aucun filtre produit supplémentaire à appliquer.
            * ``set()`` → aucune promo active : **état vide**. Le contrôleur
              force ``('id', '=', 0)`` en domaine pour garantir une liste
              vide, et le bandeau affiche un message dédié.
            * ``set`` non vide → ensemble des ids concernés (applied_on
              ``0_product_variant`` / ``1_product`` / ``2_product_category``
              résolus vers des ``product.template.id``).

        **Chaîne de résolution de la pricelist courante** (du plus
        spécifique au plus général) :

        1. ``pricelist`` fourni en paramètre → retenu tel quel.
        2. ``website._get_and_cache_current_pricelist()`` → pricelist du
           visiteur (session HTTP, cart, partenaire), **conditionnel** à
           l'activation du groupe ``product.group_product_pricelist``
           (multi-pricelists). Si le groupe est désactivé, Odoo
           court-circuite en retournant un recordset vide ; on bascule
           alors sur le fallback (3).
        3. ``env.user.partner_id.property_product_pricelist`` → pricelist
           par défaut du partenaire (mode **mono-pricelist** standard
           Odoo, valable aussi pour le partenaire public utilisé en
           navigation anonyme).

        Retour ``set()`` si aucun maillon ne résout : sémantique
        « état vide » — pas d'exception, pas de 404.
        """
        if pricelist is None:
            Website = self.env["website"]
            if website is None:
                website = Website.sudo().search([], limit=1)
            if website:
                pricelist = website._get_and_cache_current_pricelist()
            if not pricelist:
                # Fallback mono-pricelist : la pricelist par défaut du
                # partenaire courant. En mode mono-pricelist (groupe
                # ``product.group_product_pricelist`` désactivé, cas usuel
                # sur une instance « simple »), c'est la seule pricelist
                # qui existe et qui sert effectivement les prix à la caisse.
                # En contexte non-HTTP (test, cron), c'est aussi le
                # fallback qui donne une réponse sensée.
                partner = self.env.user.partner_id
                if partner:
                    pricelist = partner.property_product_pricelist
        if not pricelist:
            return set()

        Item = self.env["product.pricelist.item"].sudo()
        items = Item.search(
            self._ckr_active_items_domain(pricelist, fields.Datetime.now())
        )

        template_ids = set()
        categ_ids_promo = set()
        global_is_promo = False

        for item in items:
            if not self._ckr_item_is_reducer(item):
                continue

            applied = item.applied_on
            if applied == "0_product_variant" and item.product_id:
                # Le produit variant porte le lien vers son template.
                template_ids.add(item.product_id.product_tmpl_id.id)
            elif applied == "1_product" and item.product_tmpl_id:
                template_ids.add(item.product_tmpl_id.id)
            elif applied == "2_product_category" and item.categ_id:
                categ_ids_promo.add(item.categ_id.id)
            elif applied == "3_global":
                global_is_promo = True

        # Cas « global promo » : on signalise par ``None`` ; le caller
        # sait alors qu'aucun filtre produit ne doit être posé (toute la
        # boutique reste légitimement visible en mode promo).
        if global_is_promo:
            return None

        # Résolution catégories → templates (inclut descendants via
        # l'opérateur Odoo ``child_of`` sur le champ hiérarchique
        # ``product.category.parent_id``). On limite aux templates
        # publiés sur le site pour éviter de lister des produits non
        # exposés côté boutique.
        if categ_ids_promo:
            Template = self.env["product.template"].sudo()
            templates_in_categ = Template.search(
                [
                    ("categ_id", "child_of", list(categ_ids_promo)),
                    ("is_published", "=", True),
                ]
            )
            template_ids.update(templates_in_categ.ids)

        return template_ids

    # ------------------------------------------------------------------
    # Helpers internes — exposés en méthodes pour permettre l'override
    # ciblé par un module CK ultérieur (ex. extension A3 loyalty promo).
    # ------------------------------------------------------------------
    def _ckr_active_items_domain(self, pricelist, now):
        """Domaine des items actifs sur la pricelist courante à l'instant t.

        Bornes NULL = ouvertes (convention Odoo), donc :

        * ``date_start`` NULL **ou** ``date_start <= now`` ;
        * ``date_end``   NULL **ou** ``date_end >= now``.
        """
        return [
            ("pricelist_id", "=", pricelist.id),
            "|",
            ("date_start", "=", False),
            ("date_start", "<=", now),
            "|",
            ("date_end", "=", False),
            ("date_end", ">=", now),
        ]

    def _ckr_item_is_reducer(self, item):
        """True ssi l'item applique une remise stricte (rejette les mark-ups).

        Règles par ``compute_price`` :

        * ``percentage`` → ``percent_price > 0`` (remise positive).
          Un ``percent_price`` négatif est un mark-up ; un zéro est
          neutre. Les deux sont écartés.
        * ``formula`` → ``price_discount > 0`` (remise positive du terme
          principal). Ne tient pas compte des ``price_surcharge`` ni des
          arrondis, qui peuvent marginalement transformer un item en
          non-réducteur ; précision acceptable en première version.
        * ``fixed`` → cas contextuel : la comparaison avec le prix de
          référence (``list_price``) n'est possible **qu'au niveau
          produit**. Pour ``0_product_variant`` et ``1_product``, on
          compare directement. Pour ``2_product_category`` et
          ``3_global``, on ne peut pas décider au niveau item ; on
          inclut par prudence (doctrine §1.3 du contrat : mieux vaut un
          faux positif traçable qu'un faux négatif masquant une vraie
          promotion). Ce compromis pourra être resserré après retour
          terrain.
        """
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
