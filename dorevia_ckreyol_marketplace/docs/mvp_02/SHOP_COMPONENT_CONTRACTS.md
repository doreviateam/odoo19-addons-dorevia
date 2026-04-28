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
| **Shortcuts commerciales** | Lecture rapide des filtres commerciaux (`Tout`, `Promotions`, `Incontournables`, `Kits / Packs`) | [views/pages/ckr_shop.xml](../../views/pages/ckr_shop.xml) ; [static/src/scss/layout/_shop.scss](../../static/src/scss/layout/_shop.scss) | Hrefs sous `/shop` uniquement ; `Tout` = `/shop` sans query ; chips commerciaux = `ckr_mode=promo|featured|pack` ; état actif cohérent ; ne pas devenir une seconde sidebar | Pas de filtrage profond ; pas de lien direct vers `/promotions`, `/incontournables`, `/kits` depuis les chips |
| **Sidebar (filtres + navigation CK)** | Ordre rail **Catégories → Collections → Origines → Prix** (19.0.1.10.18+) puis autres facettes ; rail force **`opt_wsale_categories`** ; **`show_price_filter = opt_wsale_filter_price`** (**10.52**, pas de `True` seul — évite **500** sans bornes) ; data **`ckr_shop_filter_price_activation.xml`** ; **`WebsiteSaleCKR._ckr_get_price_filter_shop_values`** ; **`ckr_shop_filter_products_price_standalone`** ; **Collections** / **Origines** = checkboxes sous `/shop` (`ckr_collection`, `ckr_origin`) ; **Prix** déplié par défaut quand affiché (**10.28**) | [static/src/scss/layout/_shop.scss](../../static/src/scss/layout/_shop.scss) ; [views/pages/ckr_shop.xml](../../views/pages/ckr_shop.xml) ; [controllers/website_sale_ckr.py](../../controllers/website_sale_ckr.py) ; [`views/ckr_shop_sidebar_rail_maquette.xml`](../../views/ckr_shop_sidebar_rail_maquette.xml) ; `website_sale` | Même moteur facettes Odoo ; pas de canonical `/shop?ckr_mode=collection` ; facette **Origine** masquée si CK **Origines** alimenté (**10.17**) ; catégories via `ckr_category` plutôt que navigation `/shop/category/...` depuis la facette CK | **E2** : premier accordéon ouvert par porte *(hors bloc Prix, ouvert par défaut)* — [SHOP_MAQUETTE_ECARTS.md §2](SHOP_MAQUETTE_ECARTS.md). |
| **Grille produits** | Densité retail et lecture comparative | [static/src/scss/layout/_shop.scss](../../static/src/scss/layout/_shop.scss) | 4 / 3 / 2 / 1-2 colonnes selon breakpoint ; pas de rupture pagination / offcanvas mobile | Pas de moteur de layout parallèle au listing Odoo |
| **Carte produit V1** | Désirabilité produit + action e-commerce | [views/pages/ckr_shop_classic_tile_restore.xml](../../views/pages/ckr_shop_classic_tile_restore.xml) ; [static/src/scss/layout/_shop.scss](../../static/src/scss/layout/_shop.scss) ; [models/product_template.py](../../models/product_template.py) (`ck_product_name`, `_ckr_shop_tile_has_more_block`) ; [NOTE_TECH_TUILE_SHOP_FOOTER.md](NOTE_TECH_TUILE_SHOP_FOOTER.md) ; [NOTE_TECH_TUILE_CORNER_ACTIONS.md](NOTE_TECH_TUILE_CORNER_ACTIONS.md) ; [SPEC_CK_NOM_CK_TUILE_PRODUIT.md](SPEC_CK_NOM_CK_TUILE_PRODUIT.md) | Image homogène ; **titre** = **Nom CK** (`ck_product_name`) ou repli **`name`** ; **information secondaire** : bouton **`fa-info`** dans **`ckr-product-card__corner-actions`** (même rail que la wishlist) — méta, nom Odoo, ligne descriptive (voir spec) ; **wishlist native** `o_add_wishlist` + **`ckr-wishlist-ghost`** (même bouton) + attributs Odoo ; **pas** de **« Pour info »** / `<details>` dans le corps ni le pied de la tuile liste ; **rubans** `.o_wsale_ribbon` **`o_left` / `o_right`** ; **wishlist** si **`website_sale_wishlist`** ; badge prioritaire unique ; prix lisible ; **pied carte** prix \| CTA **une ligne** ; neutralisation `product_price` / `shop_product_buttons` ; exclusion pied CK vs `display: contents` ; CTA non dupliqué (`o_quick_add_btn` masqué en `.ckr-shop`) | Pas de faux signaux commerciaux ; pas de multi-badges brouillons |
| **Compatibilité routes Collections** | Conserver les anciennes entrées publiques comme compatibilité, mais faire converger l’usage boutique vers `/shop?...` | [controllers/website_sale_ckr.py](../../controllers/website_sale_ckr.py) ; [views/pages/ckr_shop.xml](../../views/pages/ckr_shop.xml) ; [DOCTRINE_SHOP_CONTENEUR_UNIQUE.md](DOCTRINE_SHOP_CONTENEUR_UNIQUE.md) | Les facettes sidebar **ne pointent pas** vers `/collections` ; elles utilisent `ckr_collection` sous `/shop`. Les routes legacy peuvent rediriger vers `/shop?ckr_collection=<slug>` ; jamais de canonical visiteur vers `/shop?ckr_mode=collection` | Pas de second **moteur de filtre** collections ; pas de navigation parallèle depuis les chips/sidebar |

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
- Filtre **Prix** rendu avec gabarit natif mais **bornes `None`** → **HTTP 500** (`'%f' % None`) ; ne pas forcer `show_price_filter` sans vue active + valeurs — voir **10.52** / [2_SHOP.md §4](2_SHOP.md).

## Sujets futurs (non contractuels à ce jour)

- **Sidebar — comportement post-filtre** : navigation, état actif, coches, combinaisons des quatre blocs — gel **visuel** acté ; spec comportementale **reportée** ([TICKET_SHOP_SIDEBAR_CATEGORIES.md — Backlog fonctionnel](TICKET_SHOP_SIDEBAR_CATEGORIES.md#backlog-fonctionnel-hors-périmètre-gel-visuel)).

## Références

- [SHOP_EXEC_MATRIX.md](SHOP_EXEC_MATRIX.md)
- [DOCTRINE_SHOP_CONTENEUR_UNIQUE.md](DOCTRINE_SHOP_CONTENEUR_UNIQUE.md)
- [2_SHOP.md](2_SHOP.md)
- [TICKET_SHOP_MVP22_VISIBLE_WAVE1.md](../crea/TICKET_SHOP_MVP22_VISIBLE_WAVE1.md)
- [SPEC_SHOP_PORTES.md](../mvp_01/SPEC_SHOP_PORTES.md)
- [SHOP_MAQUETTE_ECARTS.md](SHOP_MAQUETTE_ECARTS.md) — synthèse bloc par bloc maquette vs Odoo (écarts, contraintes E0)
- [NOTE_TECH_TUILE_SHOP_FOOTER.md](NOTE_TECH_TUILE_SHOP_FOOTER.md) — pied tuile `/shop` (DOM, grille, cascade)
- [NOTE_TECH_TUILE_CORNER_ACTIONS.md](NOTE_TECH_TUILE_CORNER_ACTIONS.md) — rail wishlist + info sur la média

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
| 2026-04-26 | **10.52** — sidebar : `show_price_filter = opt_wsale_filter_price`, data + `_ckr_get_price_filter_shop_values` + gabarit standalone ; carte : rubans + wishlist ghost ; risque 500 documenté. |
| 2026-04-26 | **10.53** — carte : **Nom CK** + drill-down **Pour info** (`<details>`) ; [SPEC_CK_NOM_CK_TUILE_PRODUIT.md](SPEC_CK_NOM_CK_TUILE_PRODUIT.md). |
| 2026-04-26 | **10.55+** — carte : information secondaire **rail coin** (`ckr-product-card__corner-actions`, wishlist native + `fa-info`) ; contrat mis à jour ; [NOTE_TECH_TUILE_CORNER_ACTIONS.md](NOTE_TECH_TUILE_CORNER_ACTIONS.md). |
| 2026-04-25 | **Sujets futurs** — backlog **sidebar post-filtre** (navigation, actif, combinaisons) tracé ; gel rendu visuel. |
| 2026-04-25 | **Carte produit V1** — lien QWeb `ckr_shop_classic_tile_restore.xml`, note [NOTE_TECH_TUILE_SHOP_FOOTER.md](NOTE_TECH_TUILE_SHOP_FOOTER.md), invariants pied prix \| CTA et risque cascade `#o_wsale_products_grid`. |
