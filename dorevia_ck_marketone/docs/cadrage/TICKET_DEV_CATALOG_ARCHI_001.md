# Ticket Dev — Gouvernance d'exposition catalogue CK (CATALOG-ARCHI-001)

| Champ | Valeur |
| --- | --- |
| Date | 3 juillet 2026 |
| Référence métier | [`note_10.md`](note_10.md) |
| Référence technique | [`note_10_reponse.md`](note_10_reponse.md) |
| Projet | C-Kréyòl / CK Marketone |
| Base cible | `dorevia_ck_marketone_01` |
| Périmètre | `product.public.category` / `product.template` — statut d'exposition, nav header/Home/footer, cards, SEO/sitemap, filtres |
| Hors périmètre | Refonte Home/Shop, moteur de filtres avancé, précommandes, checkout, fiche produit détaillée, pages légales, contenu éditorial définitif (cf. §4 de la note) |
| Modules | `dorevia_ck_marketone_content` (principal) · `dorevia_ck_theme` (templates cards/badges) |
| Priorité | P0 (Lot A hors seuil nav + correction data) → P1 (reste Lot A/B) → P1 (Lot C) → P2 (Lot D) |
| Estimation Lot A | **5–5,5 j-h Dev + 1,5–2 j-h QA** (détail §"Chiffrage Lot A") |
| Statut | **Lots A + B livrés, validés et poussés sur GitHub 3 juillet 2026** — commits `a72a5e36`/`95cc19e7` (Lot A) et `abae03f2` (Lot B) sur `origin/main` de `odoo19-addons-dorevia`, module `dorevia_ck_marketone_content` v19.0.1.84.0. **Lot C : NO GO code direct — mini-note d'approche à produire avant démarrage** (cf. arbitrage MOA Lot B ci-dessous). |

---

## Arbitrage MOA (3 juillet 2026)

| Sujet | Décision |
| --- | --- |
| Cadrage architecture (ce ticket + `note_10_reponse.md`) | **GO** |
| Préparation QA (recette §19–§20 de `note_10.md`) | **GO** — la QA peut préparer scénarios/scripts dès maintenant |
| Chiffrage Lot A | **GO** — le Dev peut chiffrer le Lot A (statut d'exposition + nav header/Home/footer) |
| Démarrage Dev effectif (tout lot) | **NO GO tant que les 2 réserves ci-dessous ne sont pas levées** |

### Réserves bloquantes avant Dev effectif

1. **Footer actif — RÉSOLU 3 juillet 2026, vérification directe en base `dorevia_ck_marketone_01`.**
   `select name, state from ir_module_module where name in (...)` confirme `dorevia_ckreyol_marketplace` et `dorevia_ckreyol_marketone` **`uninstalled`** — le fichier `ckr_footer.xml` évoqué en réserve est du code mort, hors périmètre. Le footer réel est `ir_ui_view.id = 1069`, `key = 'website.footer_custom'`, `name = "CK Footer Phase 1"` — un `<xpath expr="//div[@id='footer']" position="replace">` complet (4 colonnes : C-Kréyòl / Boutique / Découvrir / CK), patché ensuite par `bootstrap_footer_legal_links` pour les liens légaux. La colonne **Boutique** ne contient aujourd'hui que 2 `<li>` statiques : `/shop` (Tous les produits) et `/shop/category/epicerie-creole-1` (Épicerie créole) — aucun lien Boissons/Soin/Artisanat. Le Lot A doit rendre cette liste dynamique (générée depuis `_is_ck_exposable()`) au lieu de la coder en dur.
2. **Scope badges Lot B — toujours ouvert, à arbitrer par le MOA** (décision produit/marque, pas technique) : voir options ci-dessous.

**Reserve 1 levée → le Dev peut démarrer l'implémentation du Lot A. Reserve 2 ne bloque que le Lot B, pas le Lot A.**

### Arbitrages MOA V1 (3 juillet 2026) — les deux réserves sont levées

1. **Home "Acheter par univers"** : fonctionnement figé accepté pour ce lot. `bootstrap_home_univers()` reste le mécanisme — un changement de `ck_exposure_status` nécessitera un re-bootstrap manuel documenté (procédure à ajouter dans le README/CHANGELOG du module). Le rendu live est **hors périmètre** de CATALOG-ARCHI-001.
2. **Badges Lot B** : option (a) sobre validée. Pas de pool multi-badges dans ce lot. On conserve le `website_ribbon_id` existant, avec un chip discret origine/producteur en complément si compatible avec l'existant (réutilisation du pattern Chips-U2).

**Les deux réserves sont levées — Lot A et Lot B peuvent démarrer.**

### Options réserve 2 — scope badges cards (pour arbitrage MOA)

| Option | Contenu | Effort estimé | Recommandation |
| --- | --- | --- | --- |
| **(a) Sobre** | Garder un seul `website_ribbon_id` (standard Odoo, déjà en place) + ajouter un chip producteur/origine sur les cards shop/home, en réutilisant tel quel le pattern déjà livré et validé en fiche produit (`get_ck_product_page_chips`, [[project_ck_chips_u2]]) | 0,5–1 j-h Dev (portage d'un composant déjà existant) | **Recommandé** — cohérent avec la doctrine de sobriété de la note (§11.2 "ne pas créer un rendu marketplace criard"), risque quasi nul |
| **(b) Pool multi-badges priorisé** | Construire un vrai système de badges empilables (Bio/Coup de cœur/Nouveau/Producteur/Origine) avec règle de priorité §11.3, sur les cards shop/home — remplace le ribbon unique actuel | 3–4 j-h Dev + tests dédiés priorité | Plus fidèle au texte littéral de la note, mais reconstruit un mécanisme qui n'existe nulle part aujourd'hui sur les cards — à ne retenir que si le MOA juge le rendu actuel (ribbon seul) réellement insuffisant visuellement |

**Point notable découvert en marge (Lot A, Home) :** la section "Acheter par univers" de la Home n'est pas rendue dynamiquement à chaque requête — c'est un **contenu figé** (cf. [[project_ck_frozen_content_pattern]]) : `bootstrap_home_univers()` / `build_home_univers_arch()` ([home_univers.py](../../dorevia_ck_marketone_content/home_univers.py)) génère un HTML statique pour 4 cards fixes (épicerie/boissons/soin/artisanat) écrit une fois dans `arch_db` de la page d'accueil. Résultat concret : même une fois `ck_exposure_status` posé, changer le statut d'un univers ne fera **pas** disparaître/neutraliser son CTA sur la Home tant que quelqu'un n'aura pas manuellement rejoué `bootstrap_home_univers(env)` (+ redémarrage si nécessaire) — ce n'est pas un calcul live. À trancher avec le MOA : (i) accepter cette cohérence différée comme pour le reste du contenu Home, en documentant la procédure de re-bootstrap après tout changement de statut, ou (ii) convertir cette section en template QWeb qui lit `ck_exposure_status` à chaque affichage (charge supplémentaire non chiffrée ici, casse potentiellement l'édition WYSIWYG Website Builder de ce bloc).

---

## 0. Pré-requis transverse (tous lots)

* Créer une constante unique `CK_CATEGORY_ACTIVE_MIN_PRODUCTS = 3` et `CK_CATEGORY_FILTER_MIN_PRODUCTS = 5`, centralisées (ex. nouveau fichier `ck_catalog_exposure.py`), consommées par la nav, le rebond existant (`shop_rebound.py`) et les filtres — ne pas dupliquer le seuil `3` déjà en dur dans `shop_rebound.py`.
* Avant Lot A : confirmer en BO quelle vue rend le footer réellement actif sur `dorevia_ck_marketone_01` (cf. `note_10_reponse.md` §1) — ne pas toucher `dorevia_ckreyol_marketplace` sans validation.

---

## Lot A — Statut d'exposition catégories + navigation header/Home/footer

**Objectif** : dissocier `website_published` de l'exposition CK réelle, corriger l'exposition prématurée de catégories pauvres au header (cause racine identifiée : `_category_has_published_products`, seuil actuel = 1 produit).

### Contenu

1. Nouveau champ `ck_exposure_status` (Selection : `active`/`promise`/`hidden`/`draft`/`archived`, défaut `active`) sur `product.public.category`, dans [`models/product_public_category.py`](../../dorevia_ck_marketone_content/models/product_public_category.py).
2. Méthode `_is_ck_exposable()` combinant `website_published` + `ck_exposure_status == 'active'` + `_category_has_published_products(env, self) >= CK_CATEGORY_ACTIVE_MIN_PRODUCTS` (avec exception 2 produits + description éditoriale renseignée, cf. §6.3 de la note).
3. Migration de données (`post-migrate.py`) : backfill `ck_exposure_status` sur les catégories existantes — `active` si déjà éligibles aujourd'hui (≥1 produit publié), sinon `hidden`, pour ne pas faire disparaître silencieusement des entrées actuellement visibles au déploiement. **État réel constaté en base (3 juillet 2026)** : Épicerie 2 produits publiés (exception §6.3 déjà satisfaite — `show_category_description=True` et description renseignée depuis `bootstrap_epicerie_category`), Boissons/Soin & Bien-être/Artisanat 1 produit publié chacune. Sous le seuil brut de 3, **aucune des 4 racines ne passerait `active` sauf Épicerie via l'exception** — le backfill "sans régression" préserve donc les 4 en `active` au déploiement ; c'est ensuite au MOA de repasser Boissons/Soin/Artisanat en `promise` ou `hidden` via le nouveau champ, une fois qu'il existe. C'est exactement l'usage voulu du champ, mais MOA doit savoir qu'il faudra le faire manuellement juste après déploiement pour que le lot ait un effet visible.
4. `nav_sync.py` : `_get_ck_nav_root_categories` / `_get_ck_nav_child_categories` ([nav_sync.py:619](../../dorevia_ck_marketone_content/nav_sync.py#L619)) doivent filtrer sur `_is_ck_exposable()` au lieu de `_category_has_published_products` seul. Adapter les tests existants (`test_ck_nav_catalogue_sync.py`) qui figent le comportement actuel.
5. Footer — **RÉSOLU** : générer dynamiquement la liste `<li>` de la colonne "Boutique" de la vue `website.footer_custom` (id 1069, "CK Footer Phase 1") depuis les catégories `_is_ck_exposable()`, au lieu des 2 liens statiques actuels (`/shop`, `/shop/category/epicerie-creole-1`). Rejouer cette génération à chaque `bootstrap_ck_catalogue_navigation` pour rester synchronisée.
6. Home "Acheter par univers" — **complexité découverte, cf. encadré ci-dessus** : la section est un contenu figé généré une fois par `bootstrap_home_univers()`/`build_home_univers_arch()` ([home_univers.py](../../dorevia_ck_marketone_content/home_univers.py)), pas un rendu live. Portée V1 retenue par défaut (à confirmer MOA) : `_resolve_univers_cards()` filtre les cards non `_is_ck_exposable()` au moment de la génération (donc correct dès le prochain re-bootstrap, pas en continu) — pas de passage à un rendu QWeb live dans ce lot.

### Décisions figées

| # | Sujet | Décision |
| --- | --- | --- |
| A1 | Backfill migration | `active` si déjà éligible aujourd'hui, `hidden` sinon — jamais de régression silencieuse de nav au déploiement |
| A2 | Catégorie `promise` en Home | Bloc éditorial autorisé, jamais comme rayon principal header, CTA neutre ou vers page promesse |
| A3 | `Boutique`/`/shop` | Hors statut — reste toujours visible, gouverné indépendamment (§13.1 de la note) |

### Critères d'acceptation

* Une catégorie `hidden`/`draft`/`archived` n'apparaît plus dans le header, la Home, le footer (§18.16 de la note).
* Une catégorie `promise` n'est jamais rayon principal (§18.17).
* Aucun CTA Home univers ne pointe vers une catégorie vide/`hidden`/`draft`/`archived` (§18.5) — **sous réserve de re-bootstrap Home documentée ci-dessus**.

### Chiffrage Lot A

| Bloc | Détail | Estimation |
| --- | --- | --- |
| Modèle | Champ `ck_exposure_status` + `_is_ck_exposable()` + centralisation seuils (`CK_CATEGORY_ACTIVE_MIN_PRODUCTS`/`CK_CATEGORY_FILTER_MIN_PRODUCTS`, refactor `shop_rebound.py` pour consommer la constante partagée) | 1 j-h |
| Migration | Backfill non régressif + vue formulaire catégorie (champ visible BO) | 0,5 j-h |
| Nav header | `nav_sync.py` filtrage `_is_ck_exposable()` + mise à jour tests existants | 1–1,5 j-h |
| Footer | Génération dynamique colonne Boutique (`website.footer_custom`) | 0,5–1 j-h |
| Home univers | Filtrage `_resolve_univers_cards()` à la génération (contenu figé, pas de rendu live) | 1 j-h |
| Tests unitaires | statut/éligibilité/backfill/footer/nav | 1 j-h |
| **Total Dev** | | **5–5,5 j-h** |
| QA | Recette visuelle header/Home/footer sur les 4 univers, desktop 1280 + mobile 390, avant/après bascule statut | 1,5–2 j-h |

*Hors chiffrage* : passage de la Home à un rendu live (option ii de l'encadré ci-dessus) — à chiffrer séparément si le MOA le retient.

---

## Lot B — Correction catégorisation produits + qualification cards

**Objectif** : séparer produit publié Odoo et produit qualifié CK ; corriger les 6 catégorisations signalées.

### Contenu

1. **Tâche QA/BO (pas de code)** : recatégoriser en base les 6 produits cités (Pâte de manioc → épicerie, Savon vétiver → soin si univers actif, Chapeau Panama → artisanat, Jus Mont-Pelé → boissons, Tambour → artisanat, Coffret découverte → concret ou traité en promesse). À faire directement en BO, vérifié en recette — **ne bloque pas le développement du Lot B**, peut être fait en parallèle.
2. Champ `ck_is_qualified_for_public_exposure` (Boolean, calculé ou stocké) sur `product.template` — fiche minimale §7.3 de la note (nom, image exploitable, prix, catégorie, origine, producteur, format, disponibilité). Modéliser sur le pattern déjà validé `ck_availability_mode` (cf. [[project_ck_prod_001_availability]]) : champ + migration + vue formulaire, pas de nouvel écran.
3. Détection "produit orphelin" (publié, sans catégorie `active`/`promise`) : rapport ou filtre BO (liste `product.template` avec action serveur ou vue filtrée) — pas de blocage automatique de la fiche.
4. Normalisation ligne meta cards par famille produit (§10) : le template carte actuel (`website_sale.products_item` hérité dans [`website_sale_product_card.xml`](../../dorevia_ck_theme/views/website_sale_product_card.xml)) rend une ligne meta unique pour tous les produits — introduire une méthode `product_template._get_ck_card_meta_line()` qui bascule le format selon la famille (alimentaire/boisson/soin/artisanat/coffret), appelée depuis le template shop/catégorie ET réutilisée sur les vedettes Home (`home_featured.py`) pour éviter la divergence des deux implémentations actuelles.
5. Priorité badges cards (§11.3) : scope à confirmer avec MOA (cf. amendement note_10_reponse §2.3) — aujourd'hui un seul `website_ribbon_id` par produit sur les cards. V1 recommandée : garder un seul ribbon + ajouter un chip producteur/origine réutilisant le pattern Chips-U2 ([[project_ck_chips_u2]]), plutôt que construire un vrai pool multi-badges.

### Critères d'acceptation

* Aucune card produit alimentaire n'affiche de métadonnée "Bien-être" (§18.13, test §20.2 de la note).
* Aucun produit artisanal mis en avant sans origine/matière/producteur minimale (§18.14).
* Ligne meta cohérente avec la famille produit sur `/shop`, catégories et Home (§18.8).

### Livré et validé (3 juillet 2026)

Voir [`RECETTE_LOT_B_CATALOG_ARCHI_001.md`](RECETTE_LOT_B_CATALOG_ARCHI_001.md) pour le détail des bugs
trouvés/corrigés (BUG-B1/B2/B3) et des points de contrôle vérifiés sur rendu réel.

* `_is_ck_qualified_for_public_exposure()` (méthode, pas un champ stocké — équivalent fonctionnel) + `ck_is_orphan` (champ calculé stocké + filtre BO) sur `product.template`.
* Qualification branchée sur `get_curated_featured_variants()` — un produit incomplet ne remonte plus en "Coups de cœur" même si `ck_is_featured` est coché.
* Nom producteur ajouté à la ligne meta canonique (`_get_featured_card_metadata_line`, partagée shop/Home) — additif, aucun impact sur les produits sans producteur configuré.
* Badges (§11.3/§11.5) : scope interprété plus étroitement que "chip discret" — pas de nouvel élément visuel ajouté aux cards dans ce lot (le ribbon existant reste seul élément visuel). Seul le texte de la ligne meta a été enrichi.
* §10 (formats par famille) : pas de reconstruction en 5 templates distincts — le mécanisme générique existant (UOM masse/volume configurable + résolution origine attribut/tag) couvre déjà structurellement les formats alimentaire/boisson/soin. Coffret et matière/usage artisanat restent non couverts.
* Recatégorisation des 6 produits nommés : **toujours hors scope Dev** (tâche QA/BO). Confirmé en conditions réelles que Pâte de manioc affiche toujours "Bien-être" sur `/shop`.

### Arbitrage MOA (3 juillet 2026) — GO push + 2 interprétations Dev confirmées

| Sujet | Décision |
| --- | --- |
| Push GitHub Lot B | **GO** — poussé `95cc19e7..abae03f2` sur `origin/main` |
| Badges V1 | **Confirmé** : option sobre, pas de nouveau chip visuel, pas de pool multi-badges dans CATALOG-ARCHI-001. Multi-badges reste backlog éventuel. |
| Formats par famille | **Confirmé** : réutilisation du mécanisme générique existant validée pour ce lot. Pas de 5 templates dédiés maintenant. Coffret / artisanat dédiés à traiter plus tard si de nouveaux champs structurés s'avèrent nécessaires. |
| Démarrage Lot C | **NO GO direct** — une mini-note d'approche routes/noindex/sitemap doit être préparée avant tout code, compte tenu du niveau de risque du lot (net-new intégral, cf. §"Lot C" ci-dessous). |

---

## Lot C — SEO / sitemap / noindex / routes catégories

**Objectif** : le plus risqué et net-new du découpage — comportement des routes catégories, `noindex` et sitemap selon `ck_exposure_status`.

**Statut (3 juillet 2026)** : cadrage préalable fait — [`note_11.md`](note_11.md) (mini-note d'approche MOA) + [`note_11_reponse.md`](note_11_reponse.md) (vérification technique Dev). **NO GO code** — en attente du GO MOA final sur la matrice V1 ci-dessous.

### Matrice V1 validée en approche (note 11)

| Statut     | Route directe                                        | Navigation                      | SEO / sitemap           |
| ---------- | ----------------------------------------------------- | ---------------------------------- | -------------------------- |
| `active`   | 200 catégorie marchande                              | visible si exposable            | indexable si contenu OK |
| `promise`  | 302 vers `/shop` (pas de page promesse en V1, sauf validation MOA explicite) | non visible en navigation forte | hors sitemap            |
| `hidden`   | 302 vers `/shop`                                     | invisible                       | hors sitemap            |
| `draft`    | 404                                                  | invisible                       | hors sitemap            |
| `archived` | 301 vers `ck_replacement_category_id` si renseigné, sinon 404 | invisible                       | hors sitemap            |

### Contenu (points d'accroche techniques confirmés — note_11_reponse §1-3)

1. **Redéclaration de la route** `shop()` dans `CkWebsiteSaleController` ([`controllers/website_sale.py`](../../dorevia_ck_marketone_content/controllers/website_sale.py)) — le point d'insertion est confirmé juste après `category = self._validate_and_get_category(category)` dans la méthode standard `website_sale.controllers.main.WebsiteSale.shop()`. Décision route/redirect/404 isolée dans un helper pur (pas de logique dispersée dans le contrôleur, cf. Risque 3 de la note 11).
2. **Sitemap** : la même redéclaration de route doit fournir sa propre fonction `sitemap=` (le standard Odoo utilise `sitemap_shop`, qui énumère toutes les catégories sans filtre d'exposabilité) — pas de coût séparé, la route et le sitemap se règlent dans la même redéclaration.
3. **Noindex** : `website.layout` a déjà un mécanisme générique (`main_object.website_indexed` → `<meta name="robots" content="noindex"/>`), mais `product.public.category` n'a pas de champ `website_indexed` (hérite de `website.seo.metadata`, pas de `website.page`). **Moins coûteux qu'estimé initialement** : ajouter un champ équivalent sur la catégorie plutôt que construire un mécanisme noindex de zéro.
4. Champ `ck_replacement_category_id` (Many2one `product.public.category`) pour le cas `archived`.
5. Filtrage du sitemap : garde-fou testable "jamais noindex + présent dans le sitemap" (§13.3 de note_10.md, test §20.5).

### Critères d'acceptation

* Comportement de route stable et documenté par statut, conforme à la matrice V1 ci-dessus.
* Aucune page `noindex` présente dans le sitemap public.
* Recette sur les 6 routes listées en §19.1 de note_10.md, desktop 1280 px + mobile 390 px, cf. tests QA minimaux détaillés dans note_11.md §6.

---

## Lot D — Filtres contextuels et seuils d'affichage

**Objectif** : masquer les filtres non actionnables sous le seuil `CK_CATEGORY_FILTER_MIN_PRODUCTS = 5`. Peut glisser au sprint suivant sans bloquer A/B/C.

### Contenu

1. Dans `CkWebsiteSaleController._get_additional_shop_values` ([controllers/website_sale.py:24](../../dorevia_ck_marketone_content/controllers/website_sale.py#L24)), masquer `ck_shop_filter_tag_groups` (origine/producteur) si `values['search_count'] < CK_CATEGORY_FILTER_MIN_PRODUCTS` — réutiliser `search_count`, déjà disponible et déjà consommé par `shop_rebound.py`.
2. Conserver un tri simple (prix croissant/décroissant, nouveauté) même filtres masqués.
3. Sous-catégories (§15) : n'exposer une sous-catégorie dans la nav/tuiles que si elle est elle-même `_is_ck_exposable()` (réutilise le Lot A, pas de nouveau mécanisme).

### Critères d'acceptation

* Une catégorie avec un seul produit n'affiche pas la liste complète des filtres (§14.2, critère d'acceptation note).
* Tri simple toujours disponible même filtres masqués.

---

## Validation Lot A (3 juillet 2026)

Implémenté et vérifié sur le sandbox `dorevia_ck_marketone_01` (module upgrade réel, pas de simulation) :

* Migration `19.0.1.83.0` appliquée sans erreur. État réel constaté après migration : Épicerie 4 produits qualifiés (comptage via sous-catégories) → exposable ; Boissons 1, Soin & Bien-être 1, Artisanat 2 → non exposables. La nav a immédiatement supprimé 4 entrées de menu devenues non exposables.
* Footer : colonne Boutique vérifiée en base — ne contient plus que "Tous les produits" + "Épicerie" (les 2 liens statiques Boissons/Soin/Artisanat d'origine ont disparu).
* Home "Acheter par univers" : après re-bootstrap manuel (`bootstrap_home_univers`), les 3 univers non exposables pointent vers `/shop`, Épicerie garde son lien spécifique — conforme à l'amendement §12.2.
* **Bug trouvé et corrigé pendant l'implémentation** : le garde-fou anti-régénération de `home_univers.py` (`_univers_arch_matches_bo`) comparait les hrefs par sous-chaîne, ce qui devenait un faux positif dès que plusieurs cards partagent la valeur de repli `/shop` — corrigé par comparaison du bloc HTML complet de chaque card.
* Suite de tests complète exécutée avant/après (avec isolation via `git stash` pour distinguer les échecs pré-existants des régressions réelles) : **aucune régression introduite par le Lot A**. 2 bugs trouvés dans mes propres fichiers de test ont été corrigés (structure XML du footer de test, produits de fixture mal répartis sur les sous-catégories) — tous les tests du Lot A et de non-régression nav passent au final (37/37 sur la portée ciblée).
* Correction apportée en cours de route à la note MOA : `product.public.category` standard Odoo 19 n'a pas de champ `website_published` (vérifié dans le code source `website_sale`) — `_is_ck_exposable()` ne s'appuie donc que sur `ck_exposure_status` + le comptage de produits qualifiés.

## Séquencement recommandé

1. **Lot A** (P0/P1) — corrige la cause racine du signal MOA (nav trop permissive), déverrouille le reste.
2. **Correction data des 6 produits** en parallèle (BO, QA) — indépendante du planning Dev.
3. **Lot B** (P1) — qualification + cards, dépend du champ de statut posé en Lot A pour la détection orpheline.
4. **Lot C** (P1, le plus risqué) — peut démarrer en parallèle du Lot B une fois Lot A mergé (dépend de `ck_exposure_status`).
5. **Lot D** (P2) — sans dépendance bloquante, peut glisser au sprint suivant.

## Recette

Voir §19–§20 de [`note_10.md`](note_10.md) pour les routes, viewports et tests automatisés attendus. Verdict QA attendu au format `GO QA` / `NO GO QA` (§22 de la note).
