# -*- coding: utf-8 -*-
"""Extension de ``website`` — canonical maîtrisé pour les portes CK.

Le canonical natif d'Odoo (``website._get_canonical_url``) passe par
``ir_http._url_localized`` qui **supprime systématiquement la query
string** (commentaire explicite dans le code natif : *« canonical URLs
should not have qs »*). Ce comportement est sain par défaut, mais entre
en conflit avec la configuration gelée des portes Hybride H1 :

* **Kits / Pack**   → canonical attendu : ``/shop?ckr_mode=pack``.
* **Promotions**    → canonical attendu : ``/shop?ckr_mode=promo``.
* **Origines**      → canonical attendu : ``/shop?ckr_mode=origin``
  (+ ``ckr_origin=<slug>`` éventuellement répété, avec
  **déduplication** et **tri lexicographique** SPEC_IMPL §3.4).

Décision : rétablir les paramètres CK dans le canonical **uniquement**
pour les requêtes ``/shop`` portant déjà un mode CK **whitelisté**.
Respecte la destination commerciale unique ``/shop`` (ADR-CKR-007)
tout en préservant le **contexte de lecture** qui fait la porte
(ADR-CKR-008).

Aucune autre URL n'est affectée : le comportement natif reste la règle
générale, l'extension se limite strictement au couple
(path=``/shop``, ckr_mode ∈ whitelist).
"""
from werkzeug.urls import url_encode

from odoo import models
from odoo.http import request

# Import local pour éviter les dépendances circulaires / charger la
# whitelist et le paramètre une seule fois, au chargement du module. La
# source de vérité du nom du paramètre et des valeurs admises reste
# ``controllers/website_sale_ckr.py`` — ce modèle se limite à les
# consommer.
from odoo.addons.dorevia_ckreyol_marketplace.controllers.website_sale_ckr import (
    CKR_CANONICAL_PATH,
    CKR_MODE_ORIGIN,
    CKR_MODE_PARAM,
    CKR_ORIGIN_PARAM,
    _ckr_canonical_origin_slugs,
    _ckr_effective_mode,
)


class Website(models.Model):
    _inherit = "website"

    def _get_canonical_url(self):
        url = super()._get_canonical_url()
        if not request or not getattr(request, "httprequest", None):
            return url

        # Restreint à /shop + ckr_mode whitelisté. Toute autre URL (y
        # compris un ``/shop`` avec un ``ckr_mode`` inconnu) garde son
        # canonical natif, query string nettoyée par ``_url_localized``.
        if request.httprequest.path != CKR_CANONICAL_PATH:
            return url
        mode = _ckr_effective_mode()
        if not mode:
            return url

        # Construction déterministe de la query string canonique :
        # - `ckr_mode` en tête, en valeur unique (conflit déjà résolu
        #   par `_ckr_effective_mode` selon la priorité SPEC_IMPL §4) ;
        # - pour le mode `origin`, tous les `ckr_origin` valides sont
        #   réémis en **ordre lexicographique croissant** (§3.4), ce
        #   qui garantit une URL canonique unique pour un même
        #   ensemble d'origines quelle que soit l'ordre de saisie.
        params = [(CKR_MODE_PARAM, mode)]
        if mode == CKR_MODE_ORIGIN:
            for slug in _ckr_canonical_origin_slugs():
                params.append((CKR_ORIGIN_PARAM, slug))

        separator = "&" if "?" in url else "?"
        return f"{url}{separator}{url_encode(params)}"
