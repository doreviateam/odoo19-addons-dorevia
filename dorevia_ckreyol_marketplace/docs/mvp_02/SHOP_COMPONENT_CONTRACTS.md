# MVP2.2 — Boutique / Contrat des composants

Document de **mapping doc → code** pour la page boutique.

But : permettre à un dev ou à un relecteur de savoir :

- quel composant joue quel rôle ;
- où il est implémenté ;
- quelles règles il ne doit pas violer ;
- quelles régressions éviter quand on touche `website_sale.products`.

## Contrats

| Composant | Rôle produit / UX | Fichiers principaux | Invariants | Non-objectifs |
|-----------|--------------------|---------------------|------------|---------------|
| **Hero contextuel CK** | Porter le contexte principal de la boutique (titre, intro, ambiance) | [views/pages/ckr_shop.xml](../../views/pages/ckr_shop.xml) ; [static/src/scss/layout/_shop.scss](../../static/src/scss/layout/_shop.scss) | Un seul `h1` visible ; pas de coexistence avec un bandeau porte historique ; pas de grand hero en recherche | Pas de logique métier catalogue supplémentaire ; pas de BO riche images par porte en Vague 1 |
| **Bandeaux porte historiques** | Fallback / héritage par porte (`promo`, `pack`, `origin`, `featured`, `collection`) | [views/pages/ckr_shop.xml](../../views/pages/ckr_shop.xml) | Ne doivent pas coexister avec le hero CK principal | Ne pas devenir un second hero concurrent |
| **Header natif Odoo (`#o_wsale_products_header`)** | Porter recherche, tri, éventuel titre natif, breadcrumb | [static/src/scss/layout/_shop.scss](../../static/src/scss/layout/_shop.scss) | Si le hero CK porte le `h1`, le titre natif doit disparaître du rendu ; un seul formulaire de recherche / tri | Pas de duplication markup du tri |
| **Shortcuts commerciales** | Lecture rapide des portes retail (`Toute la boutique`, `Promotions`, `Incontournables`, `Kits`) | [views/pages/ckr_shop.xml](../../views/pages/ckr_shop.xml) ; [static/src/scss/layout/_shop.scss](../../static/src/scss/layout/_shop.scss) | Réutiliser les routes existantes ; état actif cohérent ; ne pas devenir une seconde sidebar | Pas de filtrage profond ; pas de second mécanisme promo / pack / featured |
| **Sidebar (filtres + navigation CK)** | Ordre rail **Catégories → Collections → Origines → Prix** (19.0.1.10.18+) puis autres facettes ; rail force **`opt_wsale_categories`** + **`show_price_filter`** ([`views/ckr_shop_sidebar_rail_maquette.xml`](../../views/ckr_shop_sidebar_rail_maquette.xml)) ; **Collections** / **Origines** = liens routes actées ; **Prix** déplié par défaut (**10.28**) | [static/src/scss/layout/_shop.scss](../../static/src/scss/layout/_shop.scss) ; [views/pages/ckr_shop.xml](../../views/pages/ckr_shop.xml) (`ckr_shop_sidebar_*`, `ckr_shop_sidebar_price_rail_*`, `ckr_shop_filter_price_fr`, `ckr_shop_sidebar_suppress_origin_attribute_facet`) ; [`views/ckr_shop_sidebar_rail_maquette.xml`](../../views/ckr_shop_sidebar_rail_maquette.xml) ; `website_sale` | Même moteur facettes Odoo ; pas de canonical `/shop?ckr_mode=collection` ; facette **Origine** masquée si CK **Origines** alimenté (**10.17**) ; liens catégorie sans `website_url` en Odoo 19 (**10.27**) | **E2** : premier accordéon ouvert par porte *(hors bloc Prix, ouvert par défaut)* — [SHOP_MAQUETTE_ECARTS.md §2](SHOP_MAQUETTE_ECARTS.md). |
| **Grille produits** | Densité retail et lecture comparative | [static/src/scss/layout/_shop.scss](../../static/src/scss/layout/_shop.scss) | 4 / 3 / 2 / 1-2 colonnes selon breakpoint ; pas de rupture pagination / offcanvas mobile | Pas de moteur de layout parallèle au listing Odoo |
| **Carte produit V1** | Désirabilité produit + action e-commerce | [views/pages/ckr_shop_classic_tile_restore.xml](../../views/pages/ckr_shop_classic_tile_restore.xml) ; [static/src/scss/layout/_shop.scss](../../static/src/scss/layout/_shop.scss) ; [NOTE_TECH_TUILE_SHOP_FOOTER.md](NOTE_TECH_TUILE_SHOP_FOOTER.md) | Image homogène ; badge prioritaire unique ; prix lisible ; **pied carte** : prix à gauche et CTA à droite sur **une** ligne (grille `1fr / max-content`, wrappers `footer-price` / `footer-cta`) ; neutralisation des wrappers `product_price` / `shop_product_buttons` ; exclusion du pied CK pour `display: contents` sur `.o_wsale_product_action_row` dans `#o_wsale_products_grid` ; CTA non dupliqué (`o_quick_add_btn` masqué en `.ckr-shop`) ; wishlist seulement si module présent | Pas de faux signaux commerciaux ; pas de multi-badges brouillons |
| **Routes nobles Collections** | Conserver la doctrine publique `/collections...` | [controllers/website_sale_ckr.py](../../controllers/website_sale_ckr.py) ; [views/pages/ckr_shop.xml](../../views/pages/ckr_shop.xml) | Jamais de canonical visiteur vers `/shop?ckr_mode=collection` ; repli 302 + flash conforme | Pas de second **moteur de filtre** collections : la liste rail pointe vers les URL nobles, elle ne duplique pas `_search_get_detail` |

## Règles de priorité d'orchestration

1. **Contexte** :
   hero CK **ou** bandeau historique, pas les deux.
2. **Titre principal** :
   hero CK **ou** header natif Odoo, pas les deux.
3. **Pilotage** :
   recherche / tri natifs = source de vérité ;
   shortcuts = accélérateurs commerciaux seulement.
4. **Filtres** :
   sidebar native = profondeur catalogue ;
   shortcuts ≠ filtres.

## Risques concrets à surveiller

- Empilement `hero + bandeau + header natif`.
- Sidebar visuellement plus lourde que la grille produits.
- Titre catégorie doublé entre hero et header standard.
- Search results trop éditorialisés.
- Shortcuts visibles mais non alignés avec le mode effectif (`ckr_mode`).
- Régression des routes nobles collections au profit d'une lecture `/shop` simplifiée.
- Empilement prix / CTA sur la tuile : wrappers `website_sale` ou règle `#o_wsale_products_grid` qui écrase le pied CK — voir [NOTE_TECH_TUILE_SHOP_FOOTER.md](NOTE_TECH_TUILE_SHOP_FOOTER.md).

## Sujets futurs (non contractuels à ce jour)

- **Sidebar — comportement post-filtre** : navigation, état actif, coches, combinaisons des quatre blocs — gel **visuel** acté ; spec comportementale **reportée** ([TICKET_SHOP_SIDEBAR_CATEGORIES.md — Backlog fonctionnel](TICKET_SHOP_SIDEBAR_CATEGORIES.md#backlog-fonctionnel-hors-périmètre-gel-visuel)).

## Références

- [SHOP_EXEC_MATRIX.md](SHOP_EXEC_MATRIX.md)
- [2_SHOP.md](2_SHOP.md)
- [TICKET_SHOP_MVP22_VISIBLE_WAVE1.md](../crea/TICKET_SHOP_MVP22_VISIBLE_WAVE1.md)
- [SPEC_SHOP_PORTES.md](../mvp_01/SPEC_SHOP_PORTES.md)
- [SHOP_MAQUETTE_ECARTS.md](SHOP_MAQUETTE_ECARTS.md) — synthèse bloc par bloc maquette vs Odoo (écarts, contraintes E0)
- [NOTE_TECH_TUILE_SHOP_FOOTER.md](NOTE_TECH_TUILE_SHOP_FOOTER.md) — pied tuile `/shop` (DOM, grille, cascade)

## Historique

| Date | Événement |
|------|-----------|
| 2026-04-26 | Création — contrat des composants boutique pour rendre la mise en œuvre et la review plus déterministes. |
| 2026-04-26 | Référence [SHOP_MAQUETTE_ECARTS.md](SHOP_MAQUETTE_ECARTS.md) — tableau maquette / contraintes Odoo (E0). |
| 2026-04-26 | Ligne **Sidebar** : lien explicite §2 **SHOP_MAQUETTE_ECARTS** (4 blocs maquette = cible E2, non traité V1). |
| 2026-04-26 | **Sidebar** — blocs navigation **Collections** / **Origines** dans le rail (19.0.1.10.15) ; contrat **Routes nobles** clarifié (pas de double moteur filtre). |
| 2026-04-26 | **Sidebar** — masquage facette attribut **Origine** si rail CK **Origines** non vide (19.0.1.10.17). |
| 2026-04-26 | **Sidebar** — ordre **Catégories → Collections → Origines → Prix** (19.0.1.10.18). |
| 2026-04-25 | **Sidebar** — rail **`opt_wsale_categories`** + **`show_price_filter`** ; **10.27** URLs catégorie ; **10.28** Prix déplié défaut ; **10.26** offcanvas sans xpath fragile ; ligne tableau et non-objectifs E2 précisés. |
| 2026-04-25 | **Sujets futurs** — backlog **sidebar post-filtre** (navigation, actif, combinaisons) tracé ; gel rendu visuel. |
| 2026-04-25 | **Carte produit V1** — lien QWeb `ckr_shop_classic_tile_restore.xml`, note [NOTE_TECH_TUILE_SHOP_FOOTER.md](NOTE_TECH_TUILE_SHOP_FOOTER.md), invariants pied prix \| CTA et risque cascade `#o_wsale_products_grid`. |
