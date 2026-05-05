# -*- coding: utf-8 -*-
{
    "name": "C-Kreyol - Canal e-commerce specialise",
    "version": "19.0.1.10.66",
    "category": "Website/Theme",
    "summary": "Theme front Phase 1 du canal C-Kreyol (produits agro transformes antillais).",
    "description": """
C-Kreyol - Canal e-commerce specialise (front Phase 1)
======================================================

Module de theme pour le canal de vente en ligne specialise C-Kreyol
(projet Dorevia), sur Odoo 19 Community Edition.

Portee :

* Header + menu principal personnalises (menu Option B : Boutique,
  Collections, Idées cadeaux, Recettes, A propos, Contact).
* Footer personnalise.
* Homepage structuree selon le wireframe Phase 1 (variante retail
  enrichie) : hero gele (copy SPEC_HERO §7), bloc Explorer
  (Promotions, Kits, Catégories, Collections, Origines),
  mise en avant fournisseur / origine, selection produits, bloc
  editorial, bloc confiance 3 axes.
* 19.0.1.9.3 : homepage `ckr_hpage_mvp1_tail_blocks=0` masque
  Fournisseur/Éditorial/Confiance (V1) pour recette Sélection
  (Hero+Explorer+Sélection) ; 1 = réintègre les trois blocs.
* 19.0.1.9.4 : test TransactionCase repli sélection (emplacement
  BO sans visuel ignoré) ; poursuite recette produits dynamiques.
* 19.0.1.9.5 : 4 fiches vitrine (Crêpes, Bière, Sucre de canne, Chips) +
  visuel PNG ; affectation des 4 emplacements accueil sur chaque site
  si vides (hook + migration) pour grille 4 cartes en recette MOA.
* 19.0.1.9.6 : données vitrine — retrait uom_po_id (n existe plus sur
  product.template en Odoo 19) ; recharger le module.
* 19.0.1.9.7 : visuels Sélection — PNG `docs/assets` mvp02 →
  `static/src/img/selection/` (4 fiches distinctes) ; migration re-injecte
  `image_1920` ; repli URL statique CK si fiche sans binaire.
* 19.0.1.10.0 : bloc Cercle (inscription e-mail) entre Selection et
  le footer, modele `ckr.circle.subscriber`, POST `/ckr/circle/subscribe`,
  page statique `/privacy`, menus BO Cercle (newsletter) ; chantier 4/5
  MVP2.1. Chantier 5/5 = Reassurance.
* 19.0.1.10.10 : /shop nu — hero retail type maquette PJ (photo + voile
  sombre, titre blanc, accroche terroirs) ; rail filtres titre serif ;
  tests wave1 ajustes.
* 19.0.1.10.11 : boutique avec hero — masque filmstrip catégories + champ
  recherche sous le hero (recherche header + filtres latéraux conservés).
* 19.0.1.10.12 : barre chips + compteur + tri/liste de prix au-dessus de
  l’en-tête produits ; chips aussi sur catégories et origines ; fil d’Ariane
  masqué si hero ; pas de doublon tri dans la toolbar Odoo.
* 19.0.1.10.13 : barre raccourcis — styles alignés référence MOA (fond crème,
  chips inactifs clairs, actif terracotta + texte blanc gras, tri encadré blanc,
  valeur de tri en gras, compteur avec chiffre en gras 700).
* 19.0.1.10.14 : alignement global maquette/doc — titre rail « Filtrer par »,
  libellés FR catégories, fond page #FCF9F7, hero rayon 14–18px, grille 4 col. dès
  1200px, chips contour bordeaux, cartes (fond blanc, rayon 12px, prix/nom bordeaux,
  wishlist circulaire), doc SHOP_MAQUETTE_ECARTS.md.
* 19.0.1.10.15 : rail `/shop` — accordéons **Collections** (liens `/collections/<slug>`)
  et **Origines** (liens porte + slug) ; FR **Prix** / **Effacer les filtres** ;
  SCSS `.ckr-shop-sidebar-ck` ; doc SHOP_MAQUETTE_ECARTS §2.
* 19.0.1.10.16 : sidebar boutique — rail unifié (coquille légère + sections flush,
  finition sans cartes par facette) ; offcanvas filtres aligné sur la même lecture.
* 19.0.1.10.17 : sidebar — titres accordéon homogènes (charcoal, pas terracotta à l’ouverture) ;
  « Filtrer par » intégré au rail (séparateur, pas bandeau) ; masquage facette attribut
  **Origine** dès que le bloc CK **Origines** est alimenté (suppression doublon UX).
* 19.0.1.10.18 : ordre rail maquette **Catégories → Collections → Origines → Prix**
  (Prix déplacé avant les autres facettes `website_sale`) ; vues `ckr_shop_sidebar_price_rail_*`.
* 19.0.1.10.19 : sidebar — alignement **maquette MVP2.2** : rail plat (sans carte blanche /
  ombre), « Filtrer par » serif fort, sections sans-serif, séparateurs légers, liens /
  cases taupe, cluster crème **Collections + Origines** (`ckr_shop_sidebar-ck__cluster`),
  curseur prix affiné.
* 19.0.1.10.21 : sidebar — **finition visuelle maquette PJ** (SCSS) : ligne produits
  `align-items: flex-start` (colonne filtres au contenu, fin du « puits » blanc sous le prix),
  en-têtes d’accordéon bande crème + bord léger, « Filtrer par » et titres de section
  renforcés, espacements et cluster CK harmonisés, neutralisation fonds blancs hérités.
* 19.0.1.10.22 : sidebar — **4 blocs maquette** : Catégories en accordéon explicite + cases à
  cocher ; Collections / Origines sans cluster (double `accordion-item` dans un seul flush) ;
  Prix en accordéon replié par défaut ; rail sans `vh-100` ; `is_sidebar_collapsible` forcé
  pour le template prix Odoo ; vue native `products_categories_list_collapsible` désactivée
  (remplacée par le gabarit CK).
* 19.0.1.10.23 : fix chargement module — xpath offcanvas « Catégories » via
  `#o_wsale_offcanvas_categories_header` (évite échec si `data-bs-target` non présent tel quel
  sur la vue parente fusionnée).
* 19.0.1.10.24 : sidebar `/shop` — **fallback** `opt_wsale_categories=True` (bloc Catégories
  toujours rendu, alignement maquette 4 blocs) ; doc `docs/mvp_02/TICKET_SHOP_SIDEBAR_CATEGORIES.md`
  (option native « Categories in Left Side » + recette).
* 19.0.1.10.25 : **cas nominal maquette** — `show_price_filter=True` sans exiger les facettes
  attributs ; données démo `data/ckr_shop_sidebar_nominal_demo_data.xml` (collection Saint-Anne,
  origine Guadeloupe + produits vitrine) pour afficher les 4 blocs ensemble sur instance neuve.
* 19.0.1.10.26 : retrait héritage QWeb offcanvas « Catégories » (xpath introuvable si thème
  supprime le bloc natif) pour débloquer `-u` sur toutes les instances.
* 19.0.1.10.27 : fix **500 /shop** — Odoo 19 : `product.public.category` n’a plus `website_url` ;
  liens catégories sidebar = `keep('%s/category/%s' % (shop_path, slug(c)))` (aligné
  `website_sale.categorie_link`).
* 19.0.1.10.28 : bloc **Prix** sidebar /shop — déplié par défaut (comportement natif) ;
  styles maquette (item + bouton) conservés dans `ckr_shop_filter_price_fr`.
* 19.0.1.10.29 : hero boutique `.ckr-shop-hero` — coins **supérieurs** sans arrondi ;
  `clamp(14px–18px)` conservé en **bas** uniquement (`layout/_shop.scss`).
* 19.0.1.10.30 : **carte produit /shop** — micro-catégorie (`public_categ_ids` tri `sequence`)
  au-dessus du titre ; bouton **Ajouter au panier** FR + CTA **toujours visible**
  (neutralise `o_wsale_products_opt_actions_onhover`) ; wishlist plus lisible ;
  bloc prix + CTA structuré (bordure, bouton renforcé) ; rubans lisibles (max-width,
  ombre ; couleurs BO conservées si définies) ; carte un peu plus « retail » (`_shop.scss`,
  `ckr_shop.xml`).
* 19.0.1.10.31 : fix compilation SCSS **web.assets_frontend** — `max-width: min(88%, 11.5rem)`
  via `unquote(...)` (évite *Incompatible units: rem and %* avec `min()` Sass).
* 19.0.1.10.32 : **carte produit** — micro-catégorie avec repli `product.categ_id` (sans lien) ;
  hiérarchie titre + filet ; ligne **prix à gauche / panier à droite** ; wishlist **rond**
  calé **haut droite** sur la tuile (`o_add_wishlist` absolu sur le wrapper) ; rubans (ombre /
  lisibilité). `ckr_shop.xml`, `layout/_shop.scss`.
* 19.0.1.10.33 : cartes **alignées maquette** — titre en **texte foncé** (lien hover terracotta) ;
  micro-cat **gris discret** ; **pastille panier** crème + **icône seule** (`visually-hidden` FR) ;
  wishlist **pastille crème** comme la maquette ; prix promo **rouge** si `del` ; fix marge titre
  `.mb-2` vs filet.
* 19.0.1.10.45 : tuile /shop + Classic Store — wishlist **dans** `oe_product_image` (coin image fiable) ;
  bloc info en `position: static` ; filet titre→pied plus lisible ; pied prix+panier (ligne + léger fond) ;
  repli `display:none` sur `o_quick_add_btn` en `.ckr-shop`. `ckr_shop_classic_tile_restore.xml`, `_shop.scss`.
* 19.0.1.10.46 : fix chargement module — désactivation `o_quick_add_btn` en héritant `website_sale.products_item`
  (priorité 50) au lieu de `classic_store_restore_quick_add` (xpath introuvable sur l’arch parente).
* 19.0.1.10.47 : retrait gabarit `ckr_shop_disable_classic_quick_add_bar` — le xpath `o_quick_add_btn` reste introuvable
  si le DOM shop diffère ; masquage quick-add conservé via `_shop.scss` (`.ckr-shop`).
* 19.0.1.10.48 : tuile /shop — wishlist « fantôme » sur image ; ruban explicite (z-index, visibilité) ;
  ligne prix+panier alignée ; titre slot 2 lignes fixe (`_shop.scss`).
* 19.0.1.10.49 : assets — `_shop.scss` chargé **après** `ckr_main` ; wishlist sans dépendre de
  `o_wsale_product_grid_wrapper` ; ruban QWeb `show_ribbons and ribbon` ; finitions tuile (cascade).
* 19.0.1.10.50 : tuile /shop — retrait QWeb ruban (régression) ; `ckr-wishlist-ghost` + couche `#wrap`
  pour annuler la pastille BS ; bandeau prix+panier (`space-between`, fond unifié) ; rythme titre/filet.
* 19.0.1.10.51 : tuile /shop — pied carte **prix | CTA** sur une ligne (grille `minmax(0,1fr) max-content`,
  wrappers `ckr-product-card__footer-*`, `footer-cta` + `shop_product_buttons`) ; cascade `#o_wsale_products_grid` :
  `display: contents` sur `.o_wsale_product_action_row` **exclut** `.ckr-product-card__footer` ; doc
  `docs/mvp_02/NOTE_TECH_TUILE_SHOP_FOOTER.md` ; mises à jour `2_SHOP`, `SHOP_COMPONENT_CONTRACTS`,
  `SHOP_MAQUETTE_ECARTS`, `mvp_02/README`.
* 19.0.1.10.52 : boutique — activation data `website_sale.filter_products_price` (`ckr_shop_filter_price_activation.xml`)
  pour que le rail maquette affiche le bloc **Prix** (`opt_wsale_filter_price`) sans forcer `show_price_filter=True` (évite 500).
* 19.0.1.10.53 : tuile /shop — champ BO **`ck_product_name`** (Nom CK) sur `product.template` ; titre tuile =
  `ck_product_name.strip() or name` ; méta / nom Odoo / ligne descriptive dans **`<details>` « Pour info »**
  (replié par défaut) ; `docs/mvp_02/SPEC_CK_NOM_CK_TUILE_PRODUIT.md`.
* 19.0.1.10.54 : tuile /shop — **rendu retail** : flux principal = image + titre (2 lignes) + **filet** ; « Pour info »
  déplacé **dans le pied** (au-dessus prix | CTA) ; pied sans double bordure, typo titre un peu plus compacte.
* 19.0.1.10.55 : tuile /shop — informations secondaires = **bouton info** FontAwesome **`fa-info`**
  (`ckr-product-card__info-action` / `ckr-product-card__info-icon`) dans le rail
  **`ckr-product-card__corner-actions`**, à côté de la wishlist sur la **média** (gabarit
  `ckr_shop_wishlist_on_product_media`) ; fin du libellé « Pour info » / `<details>` sur la tuile liste ;
  panneau **`ckr-product-card__details-body`** au-dessus des pastilles (`overflow` média si ouvert).
* 19.0.1.10.56 : fix **assets frontend** — panneau infos tuile : `max-width` / `max-height` en `unquote("min(...)")` pour éviter
  l’erreur Sass « calc is not a number for min » sur `web.assets_frontend`.
* 19.0.1.10.57 : tuile /shop — **icône i toujours** dans le coin média (plus liée à `_ckr_shop_tile_has_more_block` seul) ; coin rendu sur
  toute la grille boutique, wishlist inchangée.
* 19.0.1.10.58 : fix SCSS **sélecteur double `.ckr-shop`** (règles imbriquées dans `.ckr-shop { }` ne doivent pas préfixer `.ckr-shop` à nouveau) :
  coin média + pastille « i » + masquage quick-add / wishlist pied — l’icône info était hors cadre (overflow) alors que le cœur restait calé par le thème.
* 19.0.1.10.59 : tuile /shop — **Classic Store** : neutraliser `position:absolute` sur `.wishlist-above-title .btn` dans le coin média
  (sinon le cœur recouvre la pastille « i ») ; ordre flex **i** puis **cœur** ; xpath `oe_product_image` élargi (`hasclass` ou `t-attf-class`).
* 19.0.1.10.60 : tuile /shop — coin média en **grille absolue** : conteneur largeur fixe `calc(2×2rem + gap)`, « i » en `left:0`,
  wishlist en `right:0` (plus de flex seul vs thème) ; renfort `#wrap.o_wsale_products_page.ckr-shop`.
* 19.0.1.10.62 : données ``data/ckr_shop_contract_recette_seed_data.xml`` — 2ᵉ origine
  (Martinique), collection Découverte, 2 catégories eCommerce + ``public_categ_ids`` sur les
  fiches vitrine Sélection ; recette reproductible pour ``--test-tags=dorevia_ckr_shop_contract``.
* 19.0.1.10.63 : /shop — finition UI maquette PJ sans changement fonctionnel :
  sidebar plus sobre, chips intégrées au catalogue, bloc Prix plus lisible, cartes
  produit homogénéisées et grille resserrée quand il y a peu de résultats.
* 19.0.1.10.66 : page stub `/offrir` — titre et en-tête **Idées cadeaux**
  (alignement menu + nom de page Website).
* 19.0.1.10.65 : menu principal et footer — libellé **Idées cadeaux** pour
  `/offrir` (resync menu au upgrade).
* 19.0.1.10.64 : fiche produit — Lot 2 UI proche maquette : sections
  éditoriales basses alimentées par données Odoo, bloc recommandations fiable,
  réassurance structurée et finition galerie/CTA sans changement de routes.
* 19.0.1.10.61 : doc **NOTE_TECH_TUILE_CORNER_ACTIONS.md** (rail wishlist + info) ; SCSS : harmonisation **tous** les blocs
  `.ckr-product-card__info-action` — plus de `::before` texte, **`.fa` / `.ckr-product-card__info-icon` visibles** (correction d’un
  `display:none` sur `.fa` dans `.ckr-shop` qui masquait `fa-info`).
* Homepage MVP2.1 : chantier 1/5 — hero immersif V2 (image fond,
  overlay G->D, 2 CTA /shop + /origines). Chantier 2/5 — bloc
  Explorer grille asymétrique MVP2 (Promotions dominante, Kits
  secondaire fort, Catégories / Collections / Origines en cartes
  simples ; ordre et href DECISION_EXPLORER_HOMEPAGE_MVP2.md ;
  fin du rail carrousel V1 ; visuels portes depuis docs/assets
  mvp02 vers static/src/img/explorer_porte_*.png). Itération
  19.0.1.8.2 : desktop 8+4 (Promo/Kits), micro-copy e-commerce, image
  Origines épices-terroir. Chantier 3/5 (19.0.1.9.x) : selection
  produits (BO + repli catalogue ; priorite homepage 2000 en 9.1).
  (Chantier 4/5 = Cercle en 10.0 ; 5/5 = Reassurance.)
  Voir docs/mvp_02/DECISION_HERO_HOMEPAGE_V2.md,
  docs/crea/TICKET_HERO_HOMEPAGE_V2.md,
  docs/mvp_02/DECISION_EXPLORER_HOMEPAGE_MVP2.md.
  Ordre homepage gele : Hero -> Explorer -> Produits -> Editorial
  (V1) -> Inscription -> Reassurance —
  docs/mvp_02/DECISION_ORDRE_BLOCS_HOMEPAGE_MVP21.md.
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
* Porte Collections : objet editorial CK pur
  (CADRAGE_FONCTIONNEL_COLLECTIONS.md, CONTRAT_URL_COLLECTIONS.md §13,
  SPEC_IMPL_COLLECTIONS.md, PV_RECETTE_COLLECTIONS_V1.md — MOA 2026-04-22,
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
  pack > promo > origin > collection — collection en dernier,
  non-regression absolue des portes livrees (SPEC_IMPL_COLLECTIONS.md
  §5.1). Droits : lecture employe / CRUD editeur site + lecture
  publique / portail read-only sur ckr.shop.collection (necessaire
  au rendu du bloc Collections sur la fiche produit visiteur —
  recette MOA 19.0.1.6.1). Filtre catalogue porte par le point
  unique product.template._search_get_detail (bloc ckr_collection_only
  + ckr_collection_template_ids) : en Odoo 19 le hook
  website_sale._shop_lookup_products passe exclusivement par
  website._search_with_fuzzy, qui lit _search_get_detail et non plus
  _get_shop_domain. Preuve auto : tag tests dorevia_ckr_collections
  (RC-01 a RC-14, 23 methodes, 0 skipTest, PV v1 Conforme —
  docs/mvp_01/evidences/run_rc_collections_v2_summary.log).
* Pages stubs Idées cadeaux (/offrir), Recettes, Collections, Origines, A propos,
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
        # Theme Classic Store : remplace `products_item` (prix dans la colonne texte,
        # panier dans `o_quick_add_btn`) — le module CK restaure la tuile standard
        # Odoo pour la structure carte /shop (voir `ckr_shop_classic_tile_restore.xml`).
        "theme_classic_store",
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
        # --- Fiche produit : Nom CK (tuile /shop) — après vue Origines (xpath avant public_categ_ids) ---
        "views/product_template_ck_product_name_views.xml",
        # --- Back-office : collections editoriales CK (menus + vues) ---
        # Charge apres les vues Origines pour que l heritage de
        # `product_template_form_view_ckr_origin` (extension champ
        # collections apres origines) resolve correctement.
        "views/ckr_shop_collection_views.xml",
        "views/product_template_ckr_collection_views.xml",
        "views/ckr_circle_subscriber_views.xml",
        # --- Activation des variantes natives Odoo ---
        # (selecteur de langue : inline + codes, cf. docs/direction/EXPLOITATION_I18N_DEVISES.md)
        "data/website_selectors_activation.xml",
        "data/ckr_shop_filter_price_activation.xml",
        "data/ckr_explorer_category_parameter.xml",
        # Paramètre ``featured_collection_id`` : **hors XML** (hooks + migrations)
        # pour qu'un ``-u`` ne réécrase jamais la valeur opérationnelle (§4.6 SPEC).
        # --- Layout global (header + footer) ---
        "views/layout/ckr_header.xml",
        "views/layout/ckr_footer.xml",
        "views/website_ckr_homepage_featured.xml",
        # Fiches et visuels minimum pour le bloc « Sélection » (recette 4/4)
        "data/ckr_product_selection_showcase_data.xml",
        "data/ckr_shop_sidebar_nominal_demo_data.xml",
        "data/ckr_shop_contract_recette_seed_data.xml",
        # --- Portail client (/my) ---
        "views/portal/ckr_portal.xml",
        # --- Auth front (login Mon compte) ---
        "views/auth/ckr_login.xml",
        # --- Snippets homepage ---
        "views/snippets/ckr_hero.xml",
        "views/snippets/ckr_entries.xml",
        "views/snippets/ckr_supplier.xml",
        "views/snippets/ckr_selection.xml",
        "views/snippets/ckr_circle.xml",
        "views/snippets/ckr_editorial.xml",
        "views/snippets/ckr_trust.xml",
        # --- Pages ---
        "views/pages/ckr_homepage.xml",
        "views/pages/ckr_about.xml",
        "views/pages/ckr_contact.xml",
        "views/pages/ckr_privacy.xml",
        "views/pages/ckr_terms.xml",
        # Note : views/pages/ckr_collections.xml (stub transitoire) a ete
        # retire en 19.0.1.6.0 - la route /collections est desormais
        # portee par le controleur WebsiteSaleCKR (routes /collections,
        # /collections/<slug>, /collections/union/<a>/<b>/…). Cleanup
        # des installations existantes : data/ckr_cleanup_collections_stub.xml.
        "views/pages/ckr_offrir.xml",
        "views/pages/ckr_recettes.xml",
        "views/pages/ckr_product.xml",
        "views/ckr_shop_sidebar_rail_maquette.xml",
        "views/pages/ckr_shop_classic_tile_restore.xml",
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
            "dorevia_ckreyol_marketplace/static/src/js/ckr_shop_sidebar.js",
            "dorevia_ckreyol_marketplace/static/src/js/ckr_homepage_hero_rotator.js",
            "dorevia_ckreyol_marketplace/static/src/scss/layout/_header.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/layout/_locale.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/layout/_product.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/layout/_footer.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/layout/_portal.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/layout/_login.scss",
            # Components
            "dorevia_ckreyol_marketplace/static/src/scss/components/_buttons.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/components/_hero.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/components/_entries.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/components/_supplier.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/components/_selection.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/components/_circle.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/components/_editorial.scss",
            "dorevia_ckreyol_marketplace/static/src/scss/components/_trust.scss",
            # Point d entree
            "dorevia_ckreyol_marketplace/static/src/scss/ckr_main.scss",
            # Boutique : après ckr_main pour garder la main sur la cascade (tuiles, wishlist, rubans).
            "dorevia_ckreyol_marketplace/static/src/scss/layout/_shop.scss",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
