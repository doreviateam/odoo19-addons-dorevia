# -*- coding: utf-8 -*-
"""Contrôleur C-Kreyol — portes Explorer convergeant vers ``/shop``.

Matérialise le **patron Hybride H1** acté successivement pour :

* **Kits / Pack** — [CONTRAT_URL_PACKS.md §12](../docs/mvp_01/CONTRAT_URL_PACKS.md)
  (module 19.0.1.1.0) : ``/kits`` → **301** → ``/shop?ckr_mode=pack``.
* **Promotions** — [CONTRAT_URL_PROMOTIONS.md §12](../docs/mvp_01/CONTRAT_URL_PROMOTIONS.md)
  (module 19.0.1.2.0) : ``/promotions`` → **301** → ``/shop?ckr_mode=promo``.
* **Incontournables** — [SPEC_SHOP_PORTES.md §4.6](../docs/mvp_01/SPEC_SHOP_PORTES.md) :
  ``/incontournables`` → **301** → ``/shop?ckr_mode=featured`` ; périmètre =
  une ``ckr.shop.collection`` désignée par paramètre système
  (réutilisation du filtre ``ckr_collection_*`` / ``_search_get_detail``).
* **Catégories** — [CONTRAT_URL_CATEGORIES.md §12](../docs/mvp_01/CONTRAT_URL_CATEGORIES.md)
  (module 19.0.1.3.0) : ``/categories`` → **301** → ``/shop/category/<id>-<slug>``
  (**cible native** Odoo ; pas de ``ckr_mode`` — le filtre est celui du
  standard ``website_sale``).
* **Origines** — [CONTRAT_URL_ORIGINES.md §13](../docs/mvp_01/CONTRAT_URL_ORIGINES.md)
  + [SPEC_IMPL_ORIGINES.md](../docs/mvp_01/SPEC_IMPL_ORIGINES.md)
  (module 19.0.1.4.0) : ``/origines`` → **301** → ``/shop?ckr_mode=origin``
  (catalogue complet + bandeau) ; paramètre **répétable**
  ``ckr_origin=<slug>`` pour filtrer en **OU** sur les
  ``product.template`` rattachés via l'attribut catalogue « Origine ».
  Source de vérité = socle standard Odoo (A1) ; couche CK légère
  ``ckr.shop.origin`` pour les métadonnées éditoriales §3.1. Repli
  **HTTP 302** sur ``/shop`` nu en cas de slug inconnu / non publié
  / orphelin (SPEC_IMPL §3.3).
* **Collections** — [CONTRAT_URL_COLLECTIONS.md](../docs/mvp_01/CONTRAT_URL_COLLECTIONS.md)
  + [SPEC_IMPL_COLLECTIONS.md](../docs/mvp_01/SPEC_IMPL_COLLECTIONS.md)
  (module 19.0.1.6.0, MOA 2026-04-22). Rupture doctrinale par rapport
  aux portes précédentes : les **URL visiteur** sont **nobles** —
  ``/collections``, ``/collections/<slug>``, et **S1** union
  ``/collections/union/<slug-1>/…/<slug-n>`` (**n ≥ 2**) —
  **sans** redirection 301 vers ``/shop?ckr_mode=collection`` (cf.
  [CONTRAT §4.3](../docs/mvp_01/CONTRAT_URL_COLLECTIONS.md)). En
  coulisse la lecture réutilise le rendu ``/shop`` via l'attribut
  **non-persistant** ``request._ckr_collection_ctx`` (ADR local —
  alternative explicite au détour par la query string technique
  ``ckr_mode=collection`` côté visiteur). Source de vérité = M2M
  ``ckr.shop.collection.product_template_ids`` (curation CK pure —
  cf. CADRAGE §9.2, donc **pas** d'attribut catalogue). Logique
  **OU** sur l'union des collections résolues. **301** de
  normalisation (tri lexicographique + déduplication + collapse à
  un seul segment). **302** + message **flash session one-shot**
  (``ckr_collection_notice``) pour les replis (**repli A** V1 —
  pas de recomposition partielle si au moins un slug de l'union
  est invalide, cf. [SPEC_IMPL §6](../docs/mvp_01/SPEC_IMPL_COLLECTIONS.md)).
  Priorité ``ckr_mode`` figée **en dernier** : non-régression
  absolue des portes déjà livrées.

Doctrine (ADR-CKR-007, 008) :

* toutes les cartes de la section Explorer convergent vers ``/shop``
  **côté rendu** ; les URL visiteur peuvent rester nobles
  (**Collections**) ou alias 301 (**Pack / Promo / Origines**) ;
* ce qui change d'une porte à l'autre, c'est le **mode de lecture** ;
* le paramètre **``ckr_mode``** est **whitelisté** : seules les valeurs
  connues (``pack``, ``promo``, ``featured``, ``origin``, ``collection``) sont
  interprétées, les autres sont silencieusement ignorées (pas de 40x,
  pas de log ; pour éviter toute dérive de crawler) ;
* **conflit multi-``ckr_mode``** (SPEC_IMPL §4 Origines, §5.1
  Collections ; porte **Incontournables** SPEC §4.6) : une seule valeur
  est effective par requête, selon la **priorité déterministe**
  ``pack`` > ``promo`` > ``featured`` > ``origin`` > ``collection``
  (**Collections en dernier** — non-régression
  absolue des portes livrées ; cohérent avec le fait que
  ``/shop?ckr_mode=collection…`` n'est **pas** une URL publique de
  référence, cf. [CONTRAT_URL_COLLECTIONS §4.3]
  (../docs/mvp_01/CONTRAT_URL_COLLECTIONS.md)) ; implémentation via
  le helper unique :func:`_ckr_effective_mode`.

Conception technique :

* **Aucune surcharge frontale de ``shop()``** : on se greffe sur les
  points d'extension natifs de ``WebsiteSale``
  (``_get_search_options``, ``_get_shop_domain``, ``_shop_get_query_url_kwargs``,
  ``_get_additional_shop_values``) pour rester aligné API Odoo 19.
* **Filtre produit** : passé au modèle via ``options['ckr_*_only']``,
  consommé dans ``ProductTemplate._search_get_detail`` (point
  d'extension unique du ``base_domain``, garantit la cohérence
  facettes / pagination / min-max prix).
* **Source de vérité par porte** :
    * Pack   → ``product.template.pack_ok`` (module OCA ``product_pack``).
    * Promo  → ``product.pricelist`` × ``product.pricelist.item`` actif,
      strictement réducteur, sur la pricelist courante du visiteur
      (résolution dans ``product.pricelist._ckr_get_promo_template_ids``).
    * Origine → ``product.attribute.value`` (attribut « Origine »)
      référencé depuis les ``product.template`` standard ; profil CK
      ``ckr.shop.origin`` publié pour la décoration / routage.
"""
from werkzeug.urls import url_encode

from odoo import _, http
from odoo.fields import Domain
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


# ---------------------------------------------------------------------------
# Convention lexicale interne
# ---------------------------------------------------------------------------
# - CKR_MODE_PARAM     : paramètre de query-string réellement exposé côté HTTP.
# - CKR_MODE_*         : valeurs CK dédiées à chaque porte (whitelist stricte).
# - CKR_MODES_ALLOWED  : whitelist appliquée à toutes les lectures du paramètre.
# - CKR_MODE_PRIORITY  : ordre de priorité déterministe (SPEC_IMPL_ORIGINES §4)
#                        appliqué par `_ckr_effective_mode` quand plusieurs
#                        valeurs sont candidates pour la même requête.
# - CKR_MODE_TITLES    : libellé visiteur rendu sur /shop?ckr_mode=<value>.
# - CKR_ALIAS_MODE     : URL visiteur courte ↔ mode cible (bi-lexique Kits,
#                        mono-lexique Promotions / Origines).
# - CKR_ORIGIN_PARAM   : paramètre répétable de filtrage d'origine(s) par slug.
# ---------------------------------------------------------------------------
CKR_MODE_PARAM = "ckr_mode"
CKR_ORIGIN_PARAM = "ckr_origin"

CKR_MODE_PACK = "pack"
CKR_MODE_PROMO = "promo"
CKR_MODE_FEATURED = "featured"
CKR_MODE_ORIGIN = "origin"
CKR_MODE_COLLECTION = "collection"

# Paramètre système : id ``ckr.shop.collection`` « Incontournables » (SPEC §4.6).
CKR_FEATURED_COLLECTION_PARAM = "dorevia_ckreyol_marketplace.featured_collection_id"

CKR_MODES_ALLOWED = frozenset({
    CKR_MODE_PACK,
    CKR_MODE_PROMO,
    CKR_MODE_FEATURED,
    CKR_MODE_ORIGIN,
    CKR_MODE_COLLECTION,
})

# Ordre déterministe (SPEC_IMPL_ORIGINES §4 + SPEC_IMPL_COLLECTIONS §5.1,
# MOA 2026-04-22) : si plusieurs modes sont lisibles pour une même
# requête (plusieurs valeurs pour la clé `ckr_mode`, ou URL malformée),
# on retient **le premier présent dans cette liste**. Garantit qu'un
# lien externe concaténant par erreur `ckr_mode=promo&ckr_mode=origin`
# se résout à `promo` de manière reproductible côté canonical comme
# côté filtre.
#
# **Collections en dernier** : non-régression absolue des portes déjà
# livrées + cohérence doctrinale (`/shop?ckr_mode=collection…` n'est
# pas une URL publique de référence, CONTRAT §4.3).
CKR_MODE_PRIORITY = (
    CKR_MODE_PACK,
    CKR_MODE_PROMO,
    CKR_MODE_FEATURED,
    CKR_MODE_ORIGIN,
    CKR_MODE_COLLECTION,
)

CKR_MODE_TITLES = {
    CKR_MODE_PACK: "Kits",
    CKR_MODE_PROMO: "Promotions",
    CKR_MODE_FEATURED: "Incontournables",
    # Valeur de **repli** : le titre affiché du bandeau Origines suit la
    # règle dynamique SPEC_IMPL §6.1 (nom visiteur si exactement une
    # origine est active, sinon « Origines »).
    CKR_MODE_ORIGIN: "Origines",
    # Valeur **par défaut** : le titre affiché pour Collections varie
    # selon la lecture (générale / unitaire / union) ; cf. route
    # correspondante dans `WebsiteSaleCKR` + bandeau QWeb
    # `ckr_shop_collection_banner`.
    CKR_MODE_COLLECTION: "Collections",
}

CKR_CANONICAL_PATH = "/shop"

# URL visiteur (carte Explorer / bookmarks / partage externe) → mode cible.
# Chaque entrée donne lieu à une route d'alias HTTP 301 (cf.
# ``WebsiteSaleCKRAliases``) vers ``/shop?ckr_mode=<mode>``.
#
# **Collections** n'a **pas** d'entrée ici : sa face publique est une
# route noble dédiée (``/collections[/…]``) qui rend directement le
# contenu (cf. ``WebsiteSaleCKR.ckr_collections_*``), et non une 301
# vers ``/shop?ckr_mode=collection`` (CONTRAT §4.3, §4.6).
CKR_ALIAS_MODE = {
    "/kits": CKR_MODE_PACK,
    "/promotions": CKR_MODE_PROMO,
    "/incontournables": CKR_MODE_FEATURED,
    "/origines": CKR_MODE_ORIGIN,
}

# ---------------------------------------------------------------------------
# Constantes Collections (porte CK — URL publiques nobles, MOA 2026-04-22)
# ---------------------------------------------------------------------------
# - CKR_COLLECTION_BASE_PATH : préfixe de toutes les URL nobles Collections.
# - CKR_COLLECTION_UNION_SEGMENT : littéral « union » réservé (slug interdit
#   sur ``ckr.shop.collection`` — `_check_slug_format`).
# - CKR_COLLECTION_KIND_* : valeurs discriminantes du contexte de lecture
#   propagé via ``request._ckr_collection_ctx`` (lu par les hooks natifs
#   et le bandeau QWeb `ckr_shop_collection_banner`).
# - CKR_COLLECTION_FLASH_SESSION_KEY : clé de session « one-shot » pour le
#   transport du message après 302 (CONTRAT §8 — pas de `?ckr_notice=`
#   visible sur la Location).
# - CKR_COLLECTION_UNAVAILABLE_NOTICE : libellé figé SPEC_IMPL §7.
# ---------------------------------------------------------------------------
CKR_COLLECTION_BASE_PATH = "/collections"
CKR_COLLECTION_UNION_SEGMENT = "union"
CKR_COLLECTION_KIND_GENERAL = "general"
CKR_COLLECTION_KIND_SINGLE = "single"
CKR_COLLECTION_KIND_UNION = "union"
CKR_COLLECTION_FLASH_SESSION_KEY = "ckr_collection_notice"
CKR_COLLECTION_UNAVAILABLE_NOTICE = (
    "Nous n’avons pas retrouvé exactement la collection demandée. "
    "Voici les collections actuellement disponibles."
)


# ---------------------------------------------------------------------------
# Résolution du mode effectif (SPEC_IMPL_ORIGINES §4)
# ---------------------------------------------------------------------------
def _ckr_candidate_modes(post=None):
    """Ensemble brut des modes *whitelistés* lisibles depuis la requête.

    Lit **toutes** les occurrences de ``ckr_mode`` (post prime sur query,
    puis cas query multi-valeurs) et filtre par ``CKR_MODES_ALLOWED``.
    Les valeurs inconnues sont silencieusement ignorées (conforme à la
    doctrine whitelist stricte).
    """
    values = []
    if post and post.get(CKR_MODE_PARAM):
        raw = post.get(CKR_MODE_PARAM)
        if isinstance(raw, (list, tuple)):
            values.extend(raw)
        else:
            values.append(raw)
    elif request and getattr(request, "httprequest", None):
        # `args.getlist` couvre le cas ?ckr_mode=promo&ckr_mode=origin.
        values.extend(request.httprequest.args.getlist(CKR_MODE_PARAM))
    return {v for v in values if v in CKR_MODES_ALLOWED}


def _ckr_effective_mode(post=None):
    """Mode effectif unique pour la requête courante (priorité §4).

    Règle (SPEC_IMPL_ORIGINES §4 + SPEC_SHOP_PORTES §4.6) : parmi les
    valeurs ``ckr_mode`` whitelistées lues dans la requête, retenir la
    **première** dans l'ordre ``pack`` > ``promo`` > ``featured`` >
    ``origin`` > ``collection``. Toute autre valeur est ignorée ;
    aucune erreur HTTP n'est levée — une requête malformée retombe au
    pire sur ``/shop`` nu.

    :returns: valeur CK (str) si au moins un mode whitelisté est
        présent, sinon ``None``.
    """
    candidates = _ckr_candidate_modes(post)
    if not candidates:
        return None
    for mode in CKR_MODE_PRIORITY:
        if mode in candidates:
            return mode
    return None


# Alias conservé pour compatibilité avec les call sites historiques
# (Kits / Promo / Catégories). Pointe désormais sur
# `_ckr_effective_mode` : même sémantique en l'absence de conflit, et
# respect de la priorité sinon.
_ckr_current_mode = _ckr_effective_mode


def _ckr_is_mode(mode, post=None):
    """True ssi le mode effectif de la requête courante est ``mode``."""
    return _ckr_effective_mode(post) == mode


# ---------------------------------------------------------------------------
# Résolution des origines sélectionnées (SPEC_IMPL_ORIGINES §3.2)
# ---------------------------------------------------------------------------
def _ckr_read_origin_slugs(post=None):
    """Lit la liste brute des slugs ``ckr_origin`` de la requête.

    Préserve l'ordre d'apparition côté HTTP (utile pour la trace /
    debug ; le canonical re-trie de toute façon — §3.4). Ne filtre
    **pas** la whitelist ici : la résolution (existence, publication,
    orphelins) est la responsabilité de ``ckr.shop.origin``.

    **Important** : pour un GET ``?ckr_origin=a&ckr_origin=b``, le
    dict ``kwargs`` fusionné par le routeur peut ne conserver qu'une
    seule valeur pour la clé répétable. On lit donc **en priorité**
    ``request.httprequest.args.getlist`` lorsque la requête HTTP est
    disponible (SPEC_IMPL §3.2 — filtre OU multi-slugs).
    """
    values = []
    if request and getattr(request, "httprequest", None):
        values.extend(request.httprequest.args.getlist(CKR_ORIGIN_PARAM))
    if not values and post and post.get(CKR_ORIGIN_PARAM):
        raw = post.get(CKR_ORIGIN_PARAM)
        if isinstance(raw, (list, tuple)):
            values.extend(raw)
        else:
            values.append(raw)
    # Dédupliquer en conservant l'ordre d'apparition HTTP.
    seen = set()
    out = []
    for item in values:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def _ckr_resolve_origin_profiles(post=None):
    """Résout les profils ``ckr.shop.origin`` publiés pour la requête.

    :returns: tuple ``(profiles, requested_any, invalid)`` où

        * ``profiles`` est un recordset ``ckr.shop.origin`` (publiés,
          dédupliqués, ordre d'apparition dans la requête) — peut être
          vide ;
        * ``requested_any`` est ``True`` ssi au moins un ``ckr_origin``
          non vide était présent dans la requête (quel que soit sa
          validité) ;
        * ``invalid`` est ``True`` ssi ``requested_any`` mais aucun
          profil résolu → déclenche le repli HTTP 302 (§3.3).

    Le choix de ne **pas** résoudre en ``None`` permet au contrôleur
    de distinguer clairement « mode origin seul » (§3.2) de « mode
    origin + filtres invalides » (§3.3).
    """
    slugs = _ckr_read_origin_slugs(post)
    if not slugs:
        return (request.env["ckr.shop.origin"].sudo().browse(), False, False)
    website = getattr(request, "website", None) if request else None
    profiles = request.env["ckr.shop.origin"].sudo()._ckr_resolve_published_slugs(
        slugs, website=website
    )
    return (profiles, True, not profiles)


def _ckr_canonical_origin_slugs(post=None):
    """Slugs dédupliqués et triés lexicographiquement pour le canonical.

    SPEC_IMPL_ORIGINES §3.4 : une seule URL canonique pour un même
    ensemble de ``ckr_origin``, quelle que soit l'ordre d'apparition.
    Tri ASCII/C stable sur les slugs **résolus et publiés** (les slugs
    invalides ne sont pas ré-émis, pour rester cohérent avec le repli
    §3.3).
    """
    profiles, _requested, _invalid = _ckr_resolve_origin_profiles(post)
    return sorted({p.slug for p in profiles if p.slug})


def _ckr_resolve_promo_template_ids():
    """Résout la source de vérité A2 (pricelist datée) côté contrôleur.

    Retourne :

    * ``None`` → aucun filtre à appliquer (cas « global promo » : au moins
      un item pricelist actif s'applique à **tout le catalogue**, donc la
      porte Promotions = toute la boutique légitimement).
    * ``set()`` vide → **aucun produit en promotion** (état vide dédié).
    * ``set`` non vide → ensemble des ``product.template.id`` en promo.

    Le calcul est délégué à ``product.pricelist._ckr_get_promo_template_ids``
    (source de vérité §5 de ``CONTRAT_URL_PROMOTIONS.md``).
    """
    if not request or not getattr(request, "website", None):
        return set()
    return request.env["product.pricelist"].sudo()._ckr_get_promo_template_ids(
        website=request.website
    )


# ---------------------------------------------------------------------------
# Porte Collections — contexte de requête (SPEC_IMPL_COLLECTIONS §4, §5)
# ---------------------------------------------------------------------------
# Plutôt que de passer par un ``ckr_mode=collection`` exposé dans la
# query string (proscrit par CONTRAT §4.3), on propage la lecture en
# cours via un **attribut non-persistant** sur l'objet ``request``. Les
# hooks natifs ``_get_search_options`` / ``_get_shop_domain`` /
# ``_get_additional_shop_values`` consomment ce contexte pour appliquer
# le filtre M2M et alimenter les variables QWeb du bandeau.
#
# ``_ckr_collection_ctx`` est un dict :
#
#     {
#         "kind": "general" | "single" | "union",
#         "collections": <recordset ckr.shop.collection>,
#     }
#
# Il est posé **uniquement** par les routes ``/collections[/…]`` et
# consommé par les hooks sur la même requête. Aucune persistance.
# ---------------------------------------------------------------------------
def _ckr_collection_ctx_get():
    """Retourne le contexte Collections courant (ou ``None``)."""
    if not request:
        return None
    return getattr(request, "_ckr_collection_ctx", None)


def _ckr_collection_ctx_set(kind, collections):
    """Positionne le contexte Collections sur la requête courante."""
    if not request:
        return
    request._ckr_collection_ctx = {
        "kind": kind,
        "collections": collections,
    }


def _ckr_collection_flash_consume():
    """Lit puis **retire** le message flash Collections de la session.

    Consommation « one-shot » : appelée par ``_get_additional_shop_values``
    au moment du rendu de ``/collections`` (après 302). Aucune
    retransmission en query string — alignement CONTRAT §8.
    """
    if not request or not getattr(request, "session", None):
        return ""
    notice = request.session.pop(CKR_COLLECTION_FLASH_SESSION_KEY, "")
    return notice or ""


def _ckr_collection_flash_set(notice=None):
    """Dépose un message flash Collections dans la session (one-shot)."""
    if not request or not getattr(request, "session", None):
        return
    request.session[CKR_COLLECTION_FLASH_SESSION_KEY] = (
        notice or CKR_COLLECTION_UNAVAILABLE_NOTICE
    )


def _ckr_collection_redirect_unavailable():
    """302 vers ``/collections`` avec message flash (repli CONTRAT §8)."""
    _ckr_collection_flash_set()
    return request.redirect(CKR_COLLECTION_BASE_PATH, code=302)


def _ckr_collection_union_canonical_path(slugs):
    """Construit la forme canonique ``/collections/union/<s1>/<s2>/…``.

    ``slugs`` doit déjà être la séquence **dédupliquée** et **triée
    lexicographiquement**. Cette fonction est un pur helper de mise
    en forme ; toute la logique de résolution / normalisation est
    portée par la route ``ckr_collections_union``.
    """
    return "{base}/{union}/{path}".format(
        base=CKR_COLLECTION_BASE_PATH,
        union=CKR_COLLECTION_UNION_SEGMENT,
        path="/".join(slugs),
    )


def _ckr_collection_resolve_template_ids(collections):
    """Ids de ``product.template`` publiés au sein de ``collections``.

    Retourne la **liste** (pas un set) pour rester compatible avec les
    domaines Odoo. L'ordre n'est pas significatif (filtre ``id IN``).
    Filtrage complémentaire à ``is_published`` fait par ``/shop`` /
    ``_search_get_detail`` (non réécrit ici).
    """
    if not collections:
        return []
    return list({pid for pid in collections.product_template_ids.ids})


def _ckr_resolve_featured_collection():
    """Résout la collection « Incontournables » (SPEC_SHOP_PORTES §4.6).

    Source : ``ir.config_parameter``
    ``dorevia_ckreyol_marketplace.featured_collection_id`` → id
    ``ckr.shop.collection``. Valeur ``0`` ou id inexistant / non visible
    → recordset vide (repli 302 depuis ``_get_search_options``).
    """
    if not request:
        return None
    raw = (
        request.env["ir.config_parameter"]
        .sudo()
        .get_param(CKR_FEATURED_COLLECTION_PARAM, "0")
    )
    try:
        cid = int(str(raw).strip() or "0")
    except ValueError:
        return request.env["ckr.shop.collection"].browse()
    if not cid:
        return request.env["ckr.shop.collection"].browse()
    Collection = request.env["ckr.shop.collection"].sudo()
    coll = Collection.browse(cid).exists()
    # ``request.website`` peut être un recordset **vide** (routage sans
    # site résolu — ex. requêtes outil avec ``X-Odoo-Database``). Dans
    # ce cas, passer ce recordset à ``_ckr_is_visible`` fausse le test
    # ``website_id`` (empty.id ≠ coll.website_id.id → faux négatif).
    web = getattr(request, "website", None)
    if web is not None and not web.id:
        web = None
    if not coll or not coll._ckr_is_visible(website=web):
        return Collection.browse()
    return coll


class WebsiteSaleCKR(WebsiteSale):
    """Extension de ``WebsiteSale`` pour les portes Explorer (Hybride H1).

    Le dispatch par mode est fait **ici, au plus haut niveau** des hooks
    natifs, de sorte que chaque porte n'altère la sémantique de ``/shop``
    **que** quand son mode est actif. Aucune surcharge de ``shop()``.
    """

    # ------------------------------------------------------------------
    # Pré-hook : repli 302 sur référence d'origine invalide (§3.3)
    # ------------------------------------------------------------------
    # Odoo 19 n'expose pas de pré-dispatch trivial sur `/shop` ; on
    # intercepte dans `_get_search_options` (le premier hook rencontré
    # pour toute requête `/shop`), ce qui évite de surcharger `shop()`.
    # Le repli est effectué par une exception `werkzeug.Redirect`
    # remontée sous forme de réponse HTTP par le framework.
    def _get_search_options(self, **kwargs):
        options = super()._get_search_options(**kwargs)
        mode = _ckr_effective_mode(kwargs)
        if mode == CKR_MODE_PACK:
            options["ckr_pack_only"] = True
        elif mode == CKR_MODE_PROMO:
            options["ckr_promo_only"] = True
        elif mode == CKR_MODE_FEATURED:
            coll = _ckr_resolve_featured_collection()
            if not coll:
                raise _CKR_FEATURED_INVALID_REDIRECT()
            # Réutilise le même couple d’options que la porte Collections
            # (``product.template._search_get_detail`` — point unique Odoo 19).
            options["ckr_collection_only"] = True
            options["ckr_collection_template_ids"] = list(
                _ckr_collection_resolve_template_ids(coll)
            )
        elif mode == CKR_MODE_ORIGIN:
            profiles, requested, invalid = _ckr_resolve_origin_profiles(kwargs)
            if invalid:
                # Slugs demandés mais aucun résolu → 302 /shop nu
                # (§3.3). On court-circuite la recherche pour éviter
                # tout rendu avec contexte erroné.
                raise _CKR_ORIGIN_INVALID_REDIRECT()
            options["ckr_origin_only"] = True
            # Liste d'ids catalogue à consommer par `_search_get_detail`
            # (évite un second lookup SQL dans le modèle).
            options["ckr_origin_attribute_value_ids"] = (
                profiles.mapped("attribute_value_id").ids if requested else []
            )
        # --- Porte Collections : lecture noble /collections[/…] --------
        # Le contexte `_ckr_collection_ctx` est posé par les routes
        # `ckr_collections_*` **avant** l'appel à `super().shop()`. Ce
        # chemin est **distinct** du dispatcher `ckr_mode=` ci-dessus :
        # aucun flag `ckr_mode=collection` n'est attendu côté visiteur
        # (CONTRAT §4.3). On reste donc **additif** — pas de `elif`.
        ctx = _ckr_collection_ctx_get()
        if ctx is not None and _ckr_effective_mode(kwargs) != CKR_MODE_FEATURED:
            options["ckr_collection_only"] = True
            # Pré-calcul des template_ids éligibles — consommé par
            # ``product.template._search_get_detail`` (point unique de
            # filtrage catalogue `/shop` en Odoo 19 : `_get_shop_domain`
            # n'est plus appliqué par `_shop_lookup_products`). Le fait
            # de **toujours** injecter la clé (même liste vide) garantit
            # que la vue générale / unitaire / union filtrent strictement
            # leur périmètre ; sans collection visible résolue le
            # résultat est canoniquement vide (état vide §12 A pris en
            # charge par le bandeau).
            options["ckr_collection_template_ids"] = list(
                _ckr_collection_resolve_template_ids(ctx.get("collections"))
            )
        return options

    # ------------------------------------------------------------------
    # Hook 2 : cohérence du calcul min/max prix (domaine boutique complet)
    # ------------------------------------------------------------------
    def _get_shop_domain(
        self, search, category, attribute_value_dict, search_in_description=True
    ):
        domain = super()._get_shop_domain(
            search,
            category,
            attribute_value_dict,
            search_in_description=search_in_description,
        )
        mode = _ckr_effective_mode()
        if mode == CKR_MODE_PACK:
            domain = Domain.AND([domain, Domain([("pack_ok", "=", True)])])
        elif mode == CKR_MODE_PROMO:
            promo_ids = _ckr_resolve_promo_template_ids()
            if promo_ids is None:
                # Cas « global promo » : toute la boutique est en promo.
                # Aucun filtre supplémentaire ; le bandeau « Promotions »
                # reste affiché et le contexte de porte tient.
                pass
            elif not promo_ids:
                # Aucune promo active : forcer l'ensemble vide via un
                # domaine canoniquement impossible. Préférable à une
                # exception ou une 404 : le template d'état vide dédié
                # prend le relais côté vue.
                domain = Domain.AND([domain, Domain([("id", "=", 0)])])
            else:
                domain = Domain.AND(
                    [domain, Domain([("id", "in", list(promo_ids))])]
                )
        elif mode == CKR_MODE_FEATURED:
            coll = _ckr_resolve_featured_collection()
            if coll:
                template_ids = _ckr_collection_resolve_template_ids(coll)
                if template_ids:
                    domain = Domain.AND(
                        [domain, Domain([("id", "in", template_ids)])]
                    )
                else:
                    domain = Domain.AND([domain, Domain([("id", "=", 0)])])
        elif mode == CKR_MODE_ORIGIN:
            # SPEC_IMPL §3.2 : `ckr_mode=origin` seul = catalogue complet
            # (aucun filtre implicite). On ne restreint que si au moins
            # un profil publié a été résolu.
            profiles, requested, invalid = _ckr_resolve_origin_profiles()
            if requested and not invalid:
                value_ids = profiles.mapped("attribute_value_id").ids
                if value_ids:
                    domain = Domain.AND(
                        [
                            domain,
                            Domain(
                                [
                                    (
                                        "attribute_line_ids.value_ids",
                                        "in",
                                        value_ids,
                                    )
                                ]
                            ),
                        ]
                    )
        # --- Porte Collections : filtre OU sur M2M produit ↔ collection -
        # SPEC_IMPL §3.2 / §5.2 : le filtre est l'union des
        # `product_template_ids` de toutes les collections résolues pour
        # la lecture courante (générale = toutes visibles, unitaire = 1,
        # union = n ≥ 2). Le domaine produit final est `('id', 'in',
        # [ids])`, ce qui fonctionne de concert avec le calcul min/max
        # prix natif (Odoo applique ce domaine en amont de la pagination
        # et des facettes).
        ctx = _ckr_collection_ctx_get()
        if ctx is not None and _ckr_effective_mode() != CKR_MODE_FEATURED:
            collections = ctx.get("collections")
            template_ids = _ckr_collection_resolve_template_ids(collections)
            if template_ids:
                domain = Domain.AND(
                    [domain, Domain([("id", "in", template_ids)])]
                )
            else:
                # Aucune ligne M2M résolue : on force un ensemble vide
                # (état vide §12 A pour la vue unitaire, liste vide pour
                # la vue générale/union). Préférable à l'absence de
                # filtre, qui afficherait le catalogue entier.
                domain = Domain.AND([domain, Domain([("id", "=", 0)])])
        return domain

    # ------------------------------------------------------------------
    # Hook 3 : préservation de ckr_mode + ckr_origin dans pagination / filtres
    # ------------------------------------------------------------------
    def _shop_get_query_url_kwargs(
        self, search, min_price, max_price, order=None, tags=None, **kwargs
    ):
        result = super()._shop_get_query_url_kwargs(
            search, min_price, max_price, order=order, tags=tags, **kwargs
        )
        mode = _ckr_effective_mode(kwargs)
        if mode:
            result[CKR_MODE_PARAM] = mode
        if mode == CKR_MODE_ORIGIN:
            # Re-sérialisation des slugs dans l'ordre canonique §3.4
            # (tri lexicographique), pour garantir des liens internes
            # stables et alignés sur l'URL canonique.
            canonical_slugs = _ckr_canonical_origin_slugs(kwargs)
            if canonical_slugs:
                result[CKR_ORIGIN_PARAM] = canonical_slugs
        return result

    # ------------------------------------------------------------------
    # Hook 4 : variables QWeb pour le titre visiteur + état vide
    # ------------------------------------------------------------------
    def _get_additional_shop_values(self, values, **kwargs):
        result = super()._get_additional_shop_values(values, **kwargs)
        mode = _ckr_effective_mode(kwargs)
        if mode == CKR_MODE_PACK:
            result.update(
                {
                    "ckr_pack_mode": True,
                    "ckr_pack_title": CKR_MODE_TITLES[CKR_MODE_PACK],
                }
            )
        elif mode == CKR_MODE_PROMO:
            # Recalcul de l'état vide pour le bandeau : on ne peut pas se
            # reposer sur le simple nombre de produits affichés par la
            # page courante (paginée, filtrée par facettes), on requête la
            # source de vérité une seconde fois — coût négligeable, la
            # méthode est un ``search`` sur ``product.pricelist.item``
            # scopé à la pricelist courante. Permet au visiteur de voir
            # un message dédié plutôt qu'une page boutique « vide » qui
            # pourrait laisser croire à un catalogue en rupture.
            promo_ids = _ckr_resolve_promo_template_ids()
            is_empty = promo_ids is not None and not promo_ids
            result.update(
                {
                    "ckr_promo_mode": True,
                    "ckr_promo_title": CKR_MODE_TITLES[CKR_MODE_PROMO],
                    "ckr_promo_empty": is_empty,
                }
            )
        elif mode == CKR_MODE_FEATURED:
            coll = _ckr_resolve_featured_collection()
            template_ids = (
                _ckr_collection_resolve_template_ids(coll) if coll else []
            )
            is_empty = not template_ids
            result.update(
                {
                    "ckr_featured_mode": True,
                    "ckr_featured_title": CKR_MODE_TITLES[CKR_MODE_FEATURED],
                    "ckr_featured_collection": coll,
                    "ckr_featured_empty": is_empty,
                }
            )
        elif mode == CKR_MODE_ORIGIN:
            profiles, requested, _invalid = _ckr_resolve_origin_profiles(kwargs)
            # État vide = au moins une origine valide résolue mais
            # `search_count = 0` (origine(s) valide(s) sans produit).
            # On lit `search_count` tel que calculé par le standard
            # Odoo pour éviter une seconde requête SQL.
            search_count = (values or {}).get("search_count") or 0
            is_empty = bool(profiles) and not search_count
            # Titre dynamique (SPEC_IMPL §6.1) : état vide dédié §6.1
            # (titre figé) ; sinon `name_visitor` si exactement une
            # origine publiée est active ; sinon repli « Origines ».
            if is_empty:
                title = _("Aucun produit pour cette sélection.")
                context_phrase = ""
            elif len(profiles) == 1:
                profile = profiles[0]
                title = profile.display_name_visitor or CKR_MODE_TITLES[CKR_MODE_ORIGIN]
                context_phrase = profile.context_phrase or ""
            else:
                title = CKR_MODE_TITLES[CKR_MODE_ORIGIN]
                context_phrase = ""
            result.update(
                {
                    "ckr_origin_mode": True,
                    "ckr_origin_title": title,
                    "ckr_origin_context_phrase": context_phrase,
                    "ckr_origin_filtered": bool(profiles),
                    "ckr_origin_profiles": profiles,
                    "ckr_origin_requested": requested,
                    "ckr_origin_empty": is_empty,
                }
            )
        # --- Porte Collections : variables QWeb du bandeau (SPEC_IMPL §8)
        ctx = _ckr_collection_ctx_get()
        if ctx is not None and _ckr_effective_mode(kwargs) != CKR_MODE_FEATURED:
            kind = ctx.get("kind")
            collections = ctx.get("collections")
            search_count = (values or {}).get("search_count") or 0
            # État vide §12 A : **vue unitaire** valide mais sans produit.
            # Pour la vue générale ou union, on ne déclenche pas la copy
            # §12 A (qui parle d'« cette collection » — singulier), on
            # affiche la grille vide du standard avec le bandeau normal.
            is_empty_single = (
                kind == CKR_COLLECTION_KIND_SINGLE
                and bool(collections)
                and not search_count
            )
            # Titre + sous-texte (copies §8 figées MOA 2026-04-22).
            if kind == CKR_COLLECTION_KIND_SINGLE and collections:
                title = collections[:1].name or CKR_MODE_TITLES[CKR_MODE_COLLECTION]
                subtext = _("Parcourez les produits rattachés à cette collection.")
            elif kind == CKR_COLLECTION_KIND_UNION:
                title = _("Collections sélectionnées")
                subtext = _(
                    "Voici les produits appartenant à au moins une des "
                    "collections combinées."
                )
            else:
                # general
                title = CKR_MODE_TITLES[CKR_MODE_COLLECTION]
                subtext = _("Découvrez les collections actuellement disponibles.")
            result.update(
                {
                    "ckr_collection_mode": True,
                    "ckr_collection_kind": kind,
                    "ckr_collection_title": title,
                    "ckr_collection_subtext": subtext,
                    "ckr_collection_collections": collections,
                    "ckr_collection_empty": is_empty_single,
                    # Flash : message « one-shot » consommé au rendu de
                    # la vue générale (/collections) après un 302. Pour
                    # éviter de le ré-afficher sur les lectures
                    # unitaires / union suivantes dans la même session,
                    # la consommation est effectuée quel que soit le
                    # `kind` (sémantique one-shot stricte § CONTRAT §8).
                    "ckr_collection_flash": _ckr_collection_flash_consume(),
                    # Lien « Retour aux collections » (§12 A).
                    "ckr_collection_base_path": CKR_COLLECTION_BASE_PATH,
                }
            )
        # QWeb barre commerciale (Vague 1) : évite une clé absente hors
        # contexte Collections sur les expressions `not ckr_collection_mode`.
        result.setdefault("ckr_collection_mode", False)
        result["ckr_shop_shortcut_mode"] = mode
        return result

    # ------------------------------------------------------------------
    # Surcharge `shop()` : repli HTTP 302 /shop nu pour référence invalide
    # ------------------------------------------------------------------
    # Intercepte les signaux internes _CKR_ORIGIN_INVALID_REDIRECT et
    # _CKR_FEATURED_INVALID_REDIRECT levés depuis `_get_search_options`
    # (SPEC_IMPL §3.3 origines ; SPEC_SHOP_PORTES §4.6 Incontournables).
    # Aucune autre logique métier n'est ajoutée ici — la surcharge reste
    # strictement limitée au try/except requis pour le repli.
    def shop(
        self,
        page=0,
        category=None,
        search="",
        min_price=0.0,
        max_price=0.0,
        ppg=False,
        **post,
    ):
        try:
            return super().shop(
                page=page,
                category=category,
                search=search,
                min_price=min_price,
                max_price=max_price,
                ppg=ppg,
                **post,
            )
        except _CKR_ORIGIN_INVALID_REDIRECT:
            return request.redirect(CKR_CANONICAL_PATH, code=302)
        except _CKR_FEATURED_INVALID_REDIRECT:
            return request.redirect(CKR_CANONICAL_PATH, code=302)

    # ==================================================================
    # Porte Collections — routes publiques nobles
    # (CONTRAT_URL_COLLECTIONS.md §4.1 / §4.2 / §4.6 ; SPEC_IMPL §3)
    # ==================================================================
    # Les routes ci-dessous matérialisent la décision MOA 2026-04-22 :
    # la face publique de la porte Collections est **une URL noble**
    # (``/collections[/…]``), **pas** une query ``/shop?ckr_mode=…``.
    # En coulisse chaque route :
    #
    # 1. **Normalise** (déduplication, lowercase pour `union`, tri
    #    lexicographique) et émet **301** vers la forme canonique si
    #    la réception diffère (§4.6 / §9).
    # 2. **Résout** les slugs via ``ckr.shop.collection._ckr_resolve_
    #    visible_slugs`` (source de vérité visibilité : `active` +
    #    période + website).
    # 3. **Replie** en **302** + message flash session one-shot
    #    ``ckr_collection_notice`` (§8, SPEC_IMPL §7) si au moins un
    #    slug n'est pas résolvable (**repli A** V1, pas de
    #    recomposition partielle — §6).
    # 4. **Délègue** à ``self.shop(**post)`` pour réutiliser le
    #    rendu `/shop` en coulisse (QWeb `website_sale.products`,
    #    pagination, facettes) ; le contexte est transporté via
    #    l'attribut non-persistant ``request._ckr_collection_ctx``
    #    consommé par les hooks natifs ``_get_search_options`` /
    #    ``_get_shop_domain`` / ``_get_additional_shop_values``.
    #
    # Le canonical auto-référence est assuré par le
    # `website._get_canonical_url` natif (chemin courant, sans
    # substitution `/shop?ckr_mode=collection…` qui est **proscrite**
    # par CONTRAT §9 — cf. `models/website.py` qui limite la
    # réécriture au seul ``path == /shop``).
    # ------------------------------------------------------------------
    @http.route(
        "/collections",
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def ckr_collections_general(self, **post):
        """Vue générale — produits appartenant à **au moins une**
        collection visible (CONTRAT §5, SPEC_IMPL §3.1).
        """
        Collection = request.env["ckr.shop.collection"].sudo()
        collections = Collection.search(
            Collection._ckr_visible_domain(website=request.website)
        )
        _ckr_collection_ctx_set(CKR_COLLECTION_KIND_GENERAL, collections)
        return self.shop(**post)

    @http.route(
        "/collections/<string:slug>",
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def ckr_collections_single(self, slug, **post):
        """Vue unitaire — liste restreinte à une collection
        (CONTRAT §6, SPEC_IMPL §3.2).

        Le littéral ``union`` **ne peut pas** arriver ici : une route
        plus spécifique (``/collections/union``) existe. Par sécurité
        défensive : la résolution renverra un empty recordset puisque
        ``union`` est réservé par ``ckr.shop.collection._check_slug_format``
        (CONTRAT §4.6).
        """
        # Un slug vide est impossible via le routeur Werkzeug
        # (``<string:slug>`` exige au moins 1 caractère). Garde-fou
        # néanmoins symétrique aux cas union.
        if not slug:
            return _ckr_collection_redirect_unavailable()
        collections = (
            request.env["ckr.shop.collection"]
            .sudo()
            ._ckr_resolve_visible_slugs([slug], website=request.website)
        )
        if not collections:
            return _ckr_collection_redirect_unavailable()
        _ckr_collection_ctx_set(CKR_COLLECTION_KIND_SINGLE, collections)
        return self.shop(**post)

    @http.route(
        "/collections/union",
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def ckr_collections_union_empty(self, **_post):
        """``/collections/union`` sans slug suivant → 302 repli
        (CONTRAT §7).
        """
        return _ckr_collection_redirect_unavailable()

    @http.route(
        "/collections/union/<path:path>",
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def ckr_collections_union(self, path, **post):
        """Lecture union S1 — OU sur **n ≥ 2** collections
        (CONTRAT §4.6 / §7, SPEC_IMPL §3.3).

        Pipeline strictement séquentiel :

        1. **Parser** les segments (split + trim + filtre vides).
        2. **Normaliser** (lowercase + déduplication stable).
        3. **Résoudre** la visibilité (sudo).
        4. **Décider** 301 / 302 / 200 selon :

           * au moins un slug non résolu → **302** repli A (§6) ;
           * après dédup il ne reste qu'un slug :
             - raw_count > 1 (doublons) → **301**
               ``/collections/<slug>`` (collapse canonical — PV RC-07) ;
             - raw_count == 1 (``/collections/union/<un_seul>``)
               → **302** (n ≥ 2 exigé — CONTRAT §7, PV RC-08) ;
           * n ≥ 2 valides mais chemin ≠ canonique (tri / dédup)
             → **301** chemin canonique (§9) ;
           * n ≥ 2 valides et chemin déjà canonique → **200** rendu.
        """
        segments = [seg for seg in (path or "").split("/") if seg]
        if not segments:
            return _ckr_collection_redirect_unavailable()

        raw_count = len(segments)

        # Déduplication stable + normalisation lowercase (règle cohérente
        # avec `_check_slug_format` : slug stocké en minuscules / tirets).
        normalized = []
        seen = set()
        for seg in segments:
            value = (seg or "").strip().lower()
            if not value or value in seen:
                continue
            seen.add(value)
            normalized.append(value)

        if not normalized:
            return _ckr_collection_redirect_unavailable()

        collections = (
            request.env["ckr.shop.collection"]
            .sudo()
            ._ckr_resolve_visible_slugs(normalized, website=request.website)
        )
        # Repli A : au moins un slug non résolvable → 302 (pas de
        # recomposition partielle V1 — SPEC_IMPL §6).
        if len(collections) != len(normalized):
            return _ckr_collection_redirect_unavailable()

        # Après dédup il reste un seul slug :
        # - issu de doublons (raw_count > 1) : collapse canonical 301
        #   vers /collections/<slug> (PV RC-07) ;
        # - issu d'un seul segment au départ : n ≥ 2 exigé, 302 (PV RC-08).
        if len(collections) == 1:
            if raw_count > 1:
                return request.redirect(
                    "{base}/{slug}".format(
                        base=CKR_COLLECTION_BASE_PATH,
                        slug=collections.slug,
                    ),
                    code=301,
                )
            return _ckr_collection_redirect_unavailable()

        # n ≥ 2 : vérifier ordre canonique (tri lexicographique strict
        # sur les slugs normalisés — identique à la logique §9 contrat).
        canonical_slugs = sorted(normalized)
        canonical_path = _ckr_collection_union_canonical_path(canonical_slugs)
        # `request.httprequest.path` est la cible canonique côté Werkzeug
        # (inclut le préfixe website le cas échéant, mais `/collections…`
        # n'est pas un préfixe localisé par défaut). On compare sur la
        # forme nue pour éviter les faux 301 sur trailing slash.
        current_path = (request.httprequest.path or "").rstrip("/")
        if current_path != canonical_path:
            return request.redirect(canonical_path, code=301)

        _ckr_collection_ctx_set(CKR_COLLECTION_KIND_UNION, collections)
        return self.shop(**post)


# ---------------------------------------------------------------------------
# Exceptions internes : signaux court-circuit 302 /shop nu
# ---------------------------------------------------------------------------
class _CKR_ORIGIN_INVALID_REDIRECT(Exception):
    """Signal interne levé depuis ``_get_search_options`` pour déclencher
    un repli HTTP 302 vers ``/shop`` nu lorsqu'une sélection
    ``ckr_origin`` ne résout aucun profil publié (SPEC_IMPL §3.3).
    Intercepté par ``WebsiteSaleCKR.shop``.
    """


class _CKR_FEATURED_INVALID_REDIRECT(Exception):
    """Signal interne levé lorsque ``ckr_mode=featured`` est demandé mais
    la collection configurée (paramètre ``featured_collection_id``) est
    absente ou non visible (SPEC_SHOP_PORTES §4.6). Même repli 302 que
    l'origine invalide. Intercepté par ``WebsiteSaleCKR.shop``.
    """


class WebsiteSaleCKRAliases(http.Controller):
    """Alias URL visiteur → ``/shop?ckr_mode=<mode>`` (redirection HTTP 301).

    Chaque route de ``CKR_ALIAS_MODE`` est l'URL **visiteur** de sa porte
    (carte Explorer, liens extérieurs, bookmarks). Elles ne rendent
    **aucun** contenu : elles redirigent en permanence vers la
    destination commerciale unique ``/shop`` enrichie de leur
    ``ckr_mode``. Les pages stubs CMS correspondantes sont retirées du
    data set du module pour éviter toute collision de routage.

    Les paramètres de query-string entrants (``?search=…``, ``?order=…``,
    etc.) sont **préservés** lors de la redirection (cas bookmarks avec
    recherche ou tri). En cas de ``ckr_mode`` déjà présent dans
    l'entrée, il est écrasé par la valeur de la route (source de vérité
    unique = la route visiteur).
    """

    @http.route("/kits", type="http", auth="public", website=True, sitemap=False)
    def ckr_kits_alias(self, **kwargs):
        return self._ckr_redirect(CKR_MODE_PACK, kwargs)

    @http.route(
        "/promotions", type="http", auth="public", website=True, sitemap=False
    )
    def ckr_promotions_alias(self, **kwargs):
        return self._ckr_redirect(CKR_MODE_PROMO, kwargs)

    @http.route(
        "/incontournables",
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def ckr_incontournables_alias(self, **kwargs):
        """Alias visiteur **Incontournables** → ``/shop?ckr_mode=featured`` (301)."""
        return self._ckr_redirect(CKR_MODE_FEATURED, kwargs)

    @http.route(
        "/origines", type="http", auth="public", website=True, sitemap=False
    )
    def ckr_origines_alias(self, **kwargs):
        """Alias visiteur **Origines** → ``/shop?ckr_mode=origin`` (301).

        Préserve les ``ckr_origin`` éventuels en entrée (cas d'un lien
        externe déjà contextualisé par slug). Le contrôleur
        :class:`WebsiteSaleCKR` prendra ensuite en charge la résolution
        et, le cas échéant, le repli §3.3 (HTTP 302).
        """
        return self._ckr_redirect(CKR_MODE_ORIGIN, kwargs)

    @http.route(
        "/categories", type="http", auth="public", website=True, sitemap=False
    )
    def ckr_categories_alias(self, **kwargs):
        """Alias visiteur **Catégories** → URL native ``/shop/category/…``.

        Ne réutilise pas ``_ckr_redirect`` : la cible n’est pas
        ``/shop?ckr_mode=…`` mais le chemin standard Odoo résolu par
        ``product.public.category._ckr_get_explorer_entry_shop_path``.
        Les paramètres de query entrants sont préservés **sauf**
        ``ckr_mode`` (évite un mélange incohérent avec les modes Pack /
        Promo). Si aucune catégorie publique n’est résoluble, retombe
        sur ``/shop`` nu (301).
        """
        website = request.website
        path = request.env["product.public.category"]._ckr_get_explorer_entry_shop_path(
            website
        )
        if not path:
            path = CKR_CANONICAL_PATH
        params = {
            k: v
            for k, v in kwargs.items()
            if k != CKR_MODE_PARAM and v is not None and v != ""
        }
        if params:
            target = "{path}?{qs}".format(path=path, qs=url_encode(params))
        else:
            target = path
        return request.redirect(target, code=301)

    # ------------------------------------------------------------------
    # Redirection commune : source de vérité unique pour le code 301,
    # la construction de l'URL cible, et l'échappement de query string.
    # ------------------------------------------------------------------
    def _ckr_redirect(self, mode, kwargs):
        if mode not in CKR_MODES_ALLOWED:
            # Sécurité défensive : route déclarée mais mode hors whitelist
            # → on retombe sur /shop nu plutôt que de propager une valeur
            # inconnue. Ne devrait pas arriver si CKR_ALIAS_MODE reste
            # cohérente avec CKR_MODES_ALLOWED.
            return request.redirect(CKR_CANONICAL_PATH, code=301)
        # Préserver tous les paramètres sauf ckr_mode entrant : la source
        # de vérité est la route visiteur elle-même. Les ckr_origin
        # éventuels sont conservés en l'état (ils seront triés par le
        # canonical côté `/shop`).
        params = []
        for k, v in kwargs.items():
            if k == CKR_MODE_PARAM:
                continue
            if v is None or v == "":
                continue
            if isinstance(v, (list, tuple)):
                for item in v:
                    if item not in (None, ""):
                        params.append((k, item))
            else:
                params.append((k, v))
        params.append((CKR_MODE_PARAM, mode))
        target = "{path}?{qs}".format(
            path=CKR_CANONICAL_PATH,
            qs=url_encode(params),
        )
        return request.redirect(target, code=301)
