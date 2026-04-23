# -*- coding: utf-8 -*-
{
    "name": "C-Kreyol - Canal e-commerce specialise",
    "version": "19.0.1.6.16",
    "category": "Website/Theme",
    "summary": "Theme front Phase 1 du canal C-Kreyol (produits agro transformes antillais).",
    "description": """
C-Kreyol - Canal e-commerce specialise (front Phase 1)
======================================================

Module de theme pour le canal de vente en ligne specialise C-Kreyol
(projet Dorevia), sur Odoo 19 Community Edition.

Portee :

* Header + menu principal personnalises (menu Option B : Boutique,
  Collections, Offrir, Recettes, A propos, Contact).
* Footer personnalise.
* Homepage structuree selon le wireframe Phase 1 (variante retail
  enrichie) : hero gele (copy SPEC_HERO §7), bloc Explorer
  (Promotions, Collections, Kits, Catégories, Origines),
  mise en avant fournisseur / origine, selection produits, bloc
  editorial, bloc confiance 3 axes.
* Regle de bi-lexique ADR-CKR-008 : cote front / visiteur, libelle
  "Kits" (univers alimentaire : kit colombo, kit aperitif…) ; cote
  back-office et source de verite, logique "Pack" du module OCA
  product_pack (champ pack_ok, onglet Pack).
* Porte Kits/Pack : contrat d URL Hybride H1 (decision 2026-04-21,
  CONTRAT_URL_PACKS.md §12). URL visiteur /kits --> redirection HTTP
  301 vers /shop?ckr_mode=pack (canonique). Parametre CK dedie
  ckr_mode=pack qui declenche, via un controleur herite de
  WebsiteSale, le filtre product.template.pack_ok = True. Titre
  visiteur « Kits » injecte sur /shop?ckr_mode=pack.
* Porte Promotions : contrat d URL Hybride H1 (decision 2026-04-21,
  CONTRAT_URL_PROMOTIONS.md §12). URL visiteur /promotions -->
  redirection HTTP 301 vers /shop?ckr_mode=promo (canonique).
  Parametre CK ckr_mode=promo qui declenche le filtre sur la
  source de verite A2 : product.pricelist.item actif, strictement
  reducteur, sur la pricelist courante du visiteur (patron Pack
  capitalise ; extension A3 loyalty type promotion laissee ouverte
  en hook pour une vague future). Etat vide dedie : bandeau
  « Aucune offre en cours » si la source retourne zero produit
  (pre-requis ops non bloquant : alimentation d au moins une
  pricelist datee avec remise).
* Porte Categories : Hybride H1 variante cible native (decision
  2026-04-22, CONTRAT_URL_CATEGORIES.md §12). URL visiteur
  /categories --> redirection HTTP 301 vers /shop/category/id-slug
  (forme standard website_sale). Pas de ckr_mode : filtre et
  fil d Ariane natifs Odoo. Resolution de la categorie d entree :
  parametre systeme optionnel explorer_public_category_id puis
  premiere racine product.public.category du site ; repli /shop nu.
* Porte Origines : contrat d URL Hybride H1 (decision 2026-04-22,
  CONTRAT_URL_ORIGINES.md §13 + SPEC_IMPL_ORIGINES.md). URL visiteur
  /origines --> redirection HTTP 301 vers /shop?ckr_mode=origin
  (catalogue complet + bandeau Origines). Parametre repetable
  ckr_origin=<slug> qui declenche, via un controleur herite de
  WebsiteSale, le filtre OU sur product.template porteurs d une
  valeur d attribut « Origine » correspondant a un profil CK
  publie. Source de verite = socle catalogue standard (A1 —
  product.attribute.value + attribute_line_ids), couche CK legere
  ckr.shop.origin pour les metadonnees editoriales §3.1 (nom
  visiteur, phrase de contexte, slug stable, ordre, publication).
  Repli HTTP 302 sur /shop nu en cas de slug inconnu, non publie
  ou orphelin (SPEC_IMPL §3.3). Canonical multi-slugs : dedupe +
  tri lexicographique pour garantir l unicite de l URL canonique
  (SPEC_IMPL §3.4). Conflit multi-ckr_mode : priorite figee
  pack > promo > origin via helper _ckr_effective_mode
  (SPEC_IMPL §4). Droits : lecture employe / CRUD editeur site,
  pas d acces public.
* Porte Collections : objet editorial CK pur (CADRAGE_FONCTIONNEL_
  COLLECTIONS.md, CONTRAT_URL_COLLECTIONS.md §13, SPEC_IMPL_
  COLLECTIONS.md, PV_RECETTE_COLLECTIONS_V1.md — MOA 2026-04-22,
  zero residu documentaire). URLs publiques nobles dediees
  /collections, /collections/<slug>, /collections/union/<a>/<b>/…
  (syntaxe S1, n >= 2, tri lexicographique + 301 de normalisation,
  slug reserve 'union' interdit cote collection). Filtre OU sur
  M2M produit <-> collection (source de verite CK, pas d attribut
  catalogue). Repli combinaison = option A seule (302 /collections
  + message flash/session si au moins un slug invalide ; pas de
  recomposition partielle en v1). Canonical self sur chaque URL
  noble (jamais /shop?ckr_mode=collection…). Copies minimales §8
  figees (vue generale, unitaire fallback, union, etat vide §12 A).
  Modele ckr.shop.collection (champs : name translate, slug unique
  par site, sequence, active, date_start / date_end, M2M produits,
  website_id optionnel). Conflit multi-ckr_mode : priorite figee
  pack > promo > origin > collection — collection en dernier, non-
  regression absolue des portes livrees (SPEC_IMPL_COLLECTIONS.md
  §5.1). Droits : lecture employe / CRUD editeur site + lecture
  publique / portail read-only sur ckr.shop.collection (necessaire
  au rendu du bloc Collections sur la fiche produit visiteur —
  recette MOA 19.0.1.6.1). Filtre catalogue porte par le point
  unique product.template._search_get_detail (bloc ckr_collection_
  only + ckr_collection_template_ids) : en Odoo 19 le hook
  website_sale._shop_lookup_products passe exclusivement par
  website._search_with_fuzzy, qui lit _search_get_detail et non plus
  _get_shop_domain. Preuve auto : tag tests dorevia_ckr_collections
  (RC-01 a RC-14, 23 methodes, 0 skipTest, PV v1 Conforme —
  docs/phase_2/evidences/run_rc_collections_v2_summary.log).
* Pages stubs Offrir, Recettes, Collections, Origines, A propos,
  Contact. (Les stubs /kits et /promotions ont ete materialises
  comme redirections 301 portees par les controleurs CK en meme
  temps que la mise en service de leurs contrats H1 respectifs.)
* Charte graphique Phase 1 (Direction A "epicerie fine tropicale") :
  palette terracotta / sauge / amber / off-white / charcoal ;
  typographie Playfair Display + Inter.

Principe : respect maximal d Odoo 19 CE - standard d abord, specifique
legitime limite au front-end, pas de logique metier parallele.

Documentation : voir `docs/` (BRIEF_DEV, CHARTE_GRAPHIQUE_PHASE1,
SPEC_HERO_HOMEPAGE, WIREFRAME_HOMEPAGE, STRUCTURE_MENU_PRINCIPAL,
ARCHITECTURE_DECISION_RECORD).
""",
    "author": "Dorevia Team",
    "website": "https://dorevia.fr",
    "license": "LGPL-3",
    "depends": [
        "portal",
        "website",
        "website_sale",
        # Source de verite de la porte "Kits" (libelle front) /
        # "Pack" (back-office) : module OCA product_pack (champ
        # product.template.pack_ok + onglet Pack).
        "product_pack",
    ],
    "data": [
        # --- Securite (acces modeles CK) ---
        "security/ir.model.access.csv",
        # --- Attribut catalogue « Origine » (A1) + champ confort fiche produit ---
        "data/ckr_product_attribute_origin.xml",
        # --- Back-office : profils origine (menus + vues) ---
        "views/ckr_shop_origin_views.xml",
        "views/product_template_ckr_origin_views.xml",
        # --- Back-office : collections editoriales CK (menus + vues) ---
        # Charge apres les vues Origines pour que l heritage de
        # `product_template_form_view_ckr_origin` (extension champ
        # collections apres origines) resolve correctement.
        "views/ckr_shop_collection_views.xml",
        "views/product_template_ckr_collection_views.xml",
        # --- Activation des variantes natives Odoo ---
        # (selecteur de langue : inline + codes, cf. docs/EXPLOITATION_I18N_DEVISES.md)
        "data/website_selectors_activation.xml",
        "data/ckr_explorer_category_parameter.xml",
        # --- Layout global (header + footer) ---
        "views/layout/ckr_header.xml",
        "views/layout/ckr_footer.xml",
        # --- Portail client (/my) ---
        "views/portal/ckr_portal.xml",
        # --- Auth front (login Mon compte) ---
        "views/auth/ckr_login.xml",
        # --- Snippets homepage ---
        "views/snippets/ckr_hero.xml",
        "views/snippets/ckr_entries.xml",
        "views/snippets/ckr_supplier.xml",
        "views/snippets/ckr_selection.xml",
        "views/snippets/ckr_editorial.xml",
        "views/snippets/ckr_trust.xml",
        # --- Pages ---
        "views/pages/ckr_homepage.xml",
        "views/pages/ckr_about.xml",
        "views/pages/ckr_contact.xml",
        # Note : views/pages/ckr_collections.xml (stub transitoire) a ete
        # retire en 19.0.1.6.0 - la route /collections est desormais
        # portee par le controleur WebsiteSaleCKR (routes /collections,
        # /collections/<slug>, /collections/union/<a>/<b>/…). Cleanup
        # des installations existantes : data/ckr_cleanup_collections_stub.xml.
        "views/pages/ckr_offrir.xml",
        "views/pages/ckr_recettes.xml",
        "views/pages/ckr_product.xml",
        "views/pages/ckr_shop.xml",
        # --- Pages website (apres pages pour que les URLs existent) ---
        "data/website_pages_data.xml",
        # --- Nettoyage / migrations data ---
        # Retrait du stub /kits (website.page + template ckr_page_compositions)
        # suite a la mise en service du controleur H1
        # (controllers/website_sale_ckr.py). Charge apres
        # website_pages_data.xml.
        "data/ckr_cleanup_kits_stub.xml",
        # Retrait du stub /origines (website.page + template
        # ckr_page_origines) suite a la mise en service du contrat
        # d URL H1 pour la porte Origines (controleur +
        # redirection 301 vers /shop?ckr_mode=origin).
        "data/ckr_cleanup_origines_stub.xml",
        # Retrait du stub /collections (website.page + template
        # ckr_page_collections) suite a la mise en service des
        # routes nobles /collections, /collections/<slug>,
        # /collections/union/<a>/<b>/… portees par
        # WebsiteSaleCKR.ckr_collections_* (MOA 2026-04-22,
        # CONTRAT_URL_COLLECTIONS.md §4.1-§4.6).
        "data/ckr_cleanup_collections_stub.xml",
        # Note : les 6 entrees de menu Option B sont creees via post_init_hook
        # (voir hooks.py) car le menu racine d un site est "Top Menu for
        # Website N" et ne peut etre cible par un simple search XML.
    ],
    "post_init_hook": "post_init_hook",
    "assets": {
        # Tokens SCSS charges en variables primaires pour etre disponibles
        # des la resolution des variables Bootstrap / Odoo et surchargeables.
        "web._assets_primary_variables": [
            "dorevia_ckreyol_marketplace/static/src/scss/tokens/_colors.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/tokens/_typography.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/tokens/_spacing.scss",
        ],
        # Frontend : ordre = concatenation.
        "web.assets_frontend": [
            # Layout
            "dorevia_ckreyol_marketplace/static/src/js/ckr_header_drawer.js",
            "dorevia_ckreyol_marketplace/static/src/js/ckr_entries_carousel.js",
            "dorevia_ckreyol_marketplace/static/src/scss/layout/_header.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/layout/_locale.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/layout/_product.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/layout/_shop.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/layout/_footer.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/layout/_portal.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/layout/_login.scss",
            # Components
            "dorevia_ckreyol_marketplace/static/src/scss/components/_buttons.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/components/_hero.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/components/_entries.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/components/_supplier.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/components/_selection.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/components/_editorial.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/components/_trust.scss",
            # Point d entree
            "dorevia_ckreyol_marketplace/static/src/scss/ckr_main.scss",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
