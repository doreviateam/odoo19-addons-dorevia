# -*- coding: utf-8 -*-
"""Extension de ``product.template`` pour les portes Explorer → ``/shop``.

Consomme les options injectées par ``controllers/website_sale_ckr.py``
dans les options passées à ``website._search_with_fuzzy`` :

* ``ckr_pack_only`` → porte **Kits/Pack** (voir
  ``docs/phase_2/CONTRAT_URL_PACKS.md`` §12). Restriction aux produits
  dont ``pack_ok = True`` (module OCA ``product_pack``).
* ``ckr_promo_only`` → porte **Promotions** (voir
  ``docs/phase_2/CONTRAT_URL_PROMOTIONS.md`` §12). Restriction aux
  ``product.template.id`` retournés par
  ``product.pricelist._ckr_get_promo_template_ids`` (source de vérité
  A2 : pricelist datée avec remise).
* ``ckr_origin_only`` + ``ckr_origin_attribute_value_ids`` → porte
  **Origines** (voir ``docs/phase_2/SPEC_IMPL_ORIGINES.md`` §5).
  Restriction aux ``product.template`` qui portent **au moins une**
  des valeurs d'attribut cibles (logique **OU**) dans leurs lignes
  d'attribut standard. Si ``ckr_origin_only`` est vrai sans ids de
  valeurs (``ckr_mode=origin`` seul) : **aucune** restriction — le
  catalogue complet est affiché (§3.2).

Cette extension ne touche qu'à la couche *recherche* (``base_domain``
du moteur Odoo). Aucune logique métier parallèle n'est introduite —
chaque porte reste entièrement adossée à sa source de vérité standard /
OCA.

Champ **``ckr_origin_value_ids``** : raccourci éditeur sur l'attribut
catalogue « Origine » (``data/ckr_product_attribute_origin.xml``),
synchronisé avec ``attribute_line_ids`` — évite de chercher l'onglet
« Attributs & variantes » réservé au groupe Variantes.
"""
from odoo import api, fields, models
from odoo.fields import Command


# Sentinel : ``id = 0`` est la manière canonique Odoo de forcer
# « aucun résultat » dans un domaine sans déclencher d'exception.
_CKR_EMPTY_DOMAIN = [("id", "=", 0)]


class ProductTemplate(models.Model):
    _inherit = "product.template"

    ckr_origin_value_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        string="Origines",
        compute="_compute_ckr_origin_value_ids",
        inverse="_inverse_ckr_origin_value_ids",
        store=False,
        help=(
            "Valeurs de l'attribut catalogue « Origine » pour ce produit. "
            "Équivalent à une ligne « Origine » dans Attributs & variantes."
        ),
    )

    # ------------------------------------------------------------------
    # Porte Collections — rattachement M2M (SPEC_IMPL_COLLECTIONS §2.1)
    # ------------------------------------------------------------------
    # Inverse stocké du M2M déclaré côté ``ckr.shop.collection``. Le
    # ``relation`` (et l'ordre ``column1``/``column2``) doivent **refléter**
    # exactement la déclaration d'origine (colonnes **inversées** par
    # rapport au forward) pour que les deux côtés partagent bien la même
    # table de liaison.
    ckr_collection_ids = fields.Many2many(
        comodel_name="ckr.shop.collection",
        relation="ckr_shop_collection_product_template_rel",
        column1="product_template_id",
        column2="collection_id",
        string="Collections",
        help=(
            "Collections éditoriales C-Kreyol auxquelles ce produit est "
            "rattaché. Source de vérité de la porte /collections (voir "
            "docs/phase_2/SPEC_IMPL_COLLECTIONS.md §2.1). Un produit "
            "peut appartenir à plusieurs collections (RC-02) : la vue "
            "/collections/<slug> filtre par appartenance, "
            "/collections/union/<a>/<b>/… applique le OU."
        ),
    )

    @api.model
    def _ckr_origin_attribute(self):
        return self.env.ref(
            "dorevia_ckreyol_marketplace.ckr_product_attribute_origin",
            raise_if_not_found=False,
        )

    @api.depends(
        "attribute_line_ids",
        "attribute_line_ids.attribute_id",
        "attribute_line_ids.value_ids",
    )
    def _compute_ckr_origin_value_ids(self):
        attr = self._ckr_origin_attribute()
        Value = self.env["product.attribute.value"]
        if not attr:
            for tmpl in self:
                tmpl.ckr_origin_value_ids = Value.browse()
            return
        for tmpl in self:
            line = tmpl.attribute_line_ids.filtered(lambda l: l.attribute_id == attr)[:1]
            tmpl.ckr_origin_value_ids = line.value_ids

    def _inverse_ckr_origin_value_ids(self):
        attr = self._ckr_origin_attribute()
        if not attr:
            return
        Line = self.env["product.template.attribute.line"]
        for tmpl in self:
            line = tmpl.attribute_line_ids.filtered(lambda l: l.attribute_id == attr)[:1]
            if tmpl.ckr_origin_value_ids:
                if line:
                    line.value_ids = tmpl.ckr_origin_value_ids
                else:
                    Line.create(
                        {
                            "product_tmpl_id": tmpl.id,
                            "attribute_id": attr.id,
                            "value_ids": [Command.set(tmpl.ckr_origin_value_ids.ids)],
                        }
                    )
            elif line:
                # Pas de ligne vide : contrainte Odoo sur
                # product.template.attribute.line (valeurs requises si actif).
                line.unlink()

    def _search_get_detail(self, website, order, options):
        """Ajoute le filtre de porte au ``base_domain`` selon les options CK.

        Se greffe sur le ``base_domain`` (liste de domaines AND-és par le
        moteur de recherche) au lieu d'introduire un mécanisme parallèle :
        garantit que les facettes / pagination / calcul min-max prix
        convergent vers le même périmètre produit.

        Les portes sont traitées en séquence (indépendantes) ; une
        éventuelle combinaison hypothétique ``ckr_mode=pack`` + promo
        (qui ne peut pas se produire côté HTTP, whitelist exclusive du
        contrôleur, mais qui pourrait se produire côté appel direct
        Python) serait interprétée comme **intersection** des
        restrictions, ce qui est la sémantique AND naturelle du
        ``base_domain`` Odoo.
        """
        detail = super()._search_get_detail(website, order, options)
        base_domain = list(detail.get("base_domain") or [])

        if options.get("ckr_pack_only"):
            base_domain.append([("pack_ok", "=", True)])

        if options.get("ckr_promo_only"):
            promo_ids = (
                self.env["product.pricelist"]
                .sudo()
                ._ckr_get_promo_template_ids(website=website)
            )
            if promo_ids is None:
                # Cas « global promo » : aucun filtre supplémentaire
                # (toute la boutique est légitimement en promotion).
                pass
            elif not promo_ids:
                # État vide : aucune promo active → on garantit un
                # résultat vide via le sentinel. Le bandeau dédié
                # (ckr_shop_promo_banner, flag ckr_promo_empty) prend le
                # relais côté vue.
                base_domain.append(_CKR_EMPTY_DOMAIN)
            else:
                base_domain.append([("id", "in", list(promo_ids))])

        if options.get("ckr_origin_only"):
            # SPEC_IMPL §3.2 / §5 :
            # - sans value_ids : `ckr_mode=origin` seul → pas de
            #   restriction (catalogue complet + bandeau) ;
            # - avec value_ids : filtre OU sur les lignes d'attribut
            #   standard du template (`attribute_line_ids.value_ids`).
            value_ids = options.get("ckr_origin_attribute_value_ids") or []
            if value_ids:
                base_domain.append(
                    [("attribute_line_ids.value_ids", "in", list(value_ids))]
                )

        if options.get("ckr_collection_only"):
            # Porte **Collections** — SPEC_IMPL_COLLECTIONS §3.2 / §5.2.
            # L'option est toujours posée en paire avec
            # ``ckr_collection_template_ids`` par le contrôleur
            # (`controllers/website_sale_ckr.py` — `_get_search_options`).
            # La sémantique est **stricte** : aucun template_id résolu
            # (collection unique sans produit, union vide au sens des
            # rattachements, vue générale sans collection visible…) →
            # résultat catalogue **vide**. C'est exactement l'état vide
            # §12 A rendu par ``ckr_shop_collection_banner`` ; éviter
            # un domaine vide (``[]``) qui autoriserait l'ensemble du
            # catalogue est **impératif**.
            template_ids = options.get("ckr_collection_template_ids") or []
            if template_ids:
                base_domain.append([("id", "in", list(template_ids))])
            else:
                base_domain.append(_CKR_EMPTY_DOMAIN)

        detail["base_domain"] = base_domain
        return detail

    # ------------------------------------------------------------------
    # Helper fiche produit (SPEC_IMPL §7)
    # ------------------------------------------------------------------
    def _ckr_get_origin_profiles(self, website=None):
        """Profils ``ckr.shop.origin`` publiés pour ce template.

        Utilisé depuis la fiche produit (héritage
        ``website_sale.product``) pour afficher les libellés visiteur
        des origines attachées au produit. Résolution côté standard :
        on lit les ``product.attribute.value`` du template via les
        lignes d'attribut, puis on filtre sur les profils CK publiés.

        :returns: recordset ``ckr.shop.origin`` (ordre `_order` du
            modèle) ; vide si le produit n'a aucune origine associée.
        """
        self.ensure_one()
        value_ids = self.attribute_line_ids.value_ids.ids
        if not value_ids:
            return self.env["ckr.shop.origin"].browse()
        domain = [
            ("attribute_value_id", "in", value_ids),
            ("website_published", "=", True),
        ]
        if website is not None:
            domain.append(("website_id", "in", [False, website.id]))
        return self.env["ckr.shop.origin"].sudo().search(domain)

    # ------------------------------------------------------------------
    # Helper fiche produit — porte Collections
    # (SPEC_IMPL_COLLECTIONS §10, CONTRAT §11 — MOA 2026-04-22)
    # ------------------------------------------------------------------
    def _ckr_get_visible_collections(self, website=None):
        """Collections **visibles** auxquelles ce template est rattaché.

        Utilisé depuis la fiche produit (héritage
        ``website_sale.product`` — cf. ``views/pages/ckr_product.xml``)
        pour afficher un bloc de liens uniquement vers
        ``/collections/<slug>`` (CONTRAT §11 : pas d'union depuis
        fiche en V1).

        Filtrage :

        * M2M ``ckr_collection_ids`` (inverse du forward porté par
          ``ckr.shop.collection.product_template_ids``) ;
        * visibilité navigation publique via
          ``ckr.shop.collection._ckr_is_visible`` — ``active`` +
          fenêtre de validité + site courant.

        :param website: ``website.website`` ou ``None`` (aucune
            restriction site).

        :returns: recordset ``ckr.shop.collection`` trié par
            ``_order`` (``sequence, name, id``). Vide si le produit
            n'est rattaché à aucune collection visible.
        """
        self.ensure_one()
        if not self.ckr_collection_ids:
            return self.env["ckr.shop.collection"].browse()
        # On lit en sudo côté fiche produit publique : ACL masquerait
        # les collections au visiteur non authentifié sinon.
        collections = self.ckr_collection_ids.sudo()
        return collections.filtered(lambda c: c._ckr_is_visible(website=website))
