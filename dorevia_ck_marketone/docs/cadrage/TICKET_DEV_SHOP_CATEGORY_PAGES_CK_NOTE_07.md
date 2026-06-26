# Ticket Dev — Shop CK · Pages catégories pleine largeur (Note 07)

| Champ | Valeur |
| --- | --- |
| Date | 26 juin 2026 |
| Référence UX | [`note_07.md`](note_07.md) v1.1 |
| Référence technique | [`note_07_reponse.md`](note_07_reponse.md) — **validé MOA** |
| Projet | C-Kréyòl / CK Marketone |
| Base cible | `dorevia_ck_marketone_01` |
| Périmètre | `/shop` et `/shop/category/...` — layout catalogue, drawer filtres, rebond, responsive |
| Hors périmètre | Fiche produit · checkout · BO · nouveaux modèles métier · refonte moteur filtres Odoo · header/nav |
| Modules | `dorevia_ck_theme` (principal) · `dorevia_ck_marketone_content` (rebond + tuiles génériques) |
| Estimation | **4–5,5 j-h Dev** + **1,5–2 j-h QA** |
| Priorité | Moyenne — **backlog lot suivant** |
| Statut | **GO technique recette 26/06** — validation MOA R1 (tuiles Boissons) · voir [`RECETTE_QA_NOTE_07_VERDICT.md`](../design/maquette_01.2/RECETTE_QA_NOTE_07_VERDICT.md) |
| Séquencement | **Après clôture Axe C post-correction** (voir §1.1) |

---

## 1. Contexte et validation MOA

La boutique CK doit refléter une **boutique de sélection** : peu de références, qualifiées, sans impression de page vide ni de colonne filtres dominante.

Le lot S1/P2 a structuré l'intro, le filmstrip, la sidebar « Affiner ma sélection » et le header rayon P2B (Épicerie). La **note 07** fait évoluer la grammaire catalogue :

```text
Avant : sidebar permanente + grille partielle
Après : toolbar compacte + grille pleine largeur + filtres en drawer + rebond si rayon pauvre
```

**Validation MOA** : approche technique de `note_07_reponse.md` acceptée — héritages xpath sur `website_sale.products`, offcanvas natif `#o_wsale_offcanvas`, pas de réécriture du template Odoo.

### 1.1 Séquencement et réserve de pilotage (MOA)

> **Ce ticket est prêt, mais il ne doit pas détourner l'objectif immédiat : finir Axe C / cale produit, puis recetter post-correction.**

| Arbitrage MOA | Décision |
| --- | --- |
| Ticket document | **GO** |
| Backlog Dev | **GO** — lot suivant préparé, transmissible au Dev |
| Démarrage immédiat | **NO GO** tant que Axe C n'est pas recetté |

**Ordre impératif avant Lot A Note 07 :**

1. Mise à jour instance (`dorevia_ck_theme` + `dorevia_ck_marketone_content` livraisons 26/06).
2. Corrections BO Axe C (MOA).
3. Recette post-correction cale produit (`RECETTE_QA_CALE_PRODUIT_V1_POST_CORRECTION`).
4. Production de la recette QA finale catalogue.

**Prérequis bloquant recette Note 07** : catalogue BO stabilisé (Axe C post-correction). Le Dev peut préparer le code en parallèle seulement si explicitement dépriorisé par le lead — par défaut **attendre le vert Axe C**.

---

## 2. Objectif

Sur toutes les pages catalogue CK (`.ck-shop-page`) :

1. Supprimer la sidebar filtres permanente desktop.
2. Donner **100 % de la largeur container** à la grille produits.
3. Rendre les filtres accessibles via un **drawer** (bouton Filtrer → offcanvas natif).
4. Afficher les **sous-catégories visuelles** uniquement quand pertinent.
5. Afficher un **bloc de rebond** sous la grille pour les rayons pauvres en état initial.
6. Compacter la **toolbar** (Filtrer · Recherche · Tri).
7. Affiner les **cards** (pas de ligne vide si champ optionnel absent).
8. Garantir le **mobile 390 px** sans overflow horizontal.

---

## 3. Décisions MOA / Produit (figées pour ce ticket)

| # | Sujet | Décision retenue |
| --- | --- | --- |
| D1 | CTA bloc rebond | Lien vers **`/shop`** — libellé **« Découvrir toute la boutique »** |
| D2 | Message rebond (V1) | **« Cette sélection s'enrichit progressivement. Découvrez d'autres produits créoles sur toute la boutique. »** |
| D3 | Tri modifié vs rebond | Le rebond **ne disparaît pas** si seul le tri change (aligné checklist QA §4.2) |
| D4 | Filmstrip sur Épicerie | **Masquer** `#o_wsale_categories_filmstrip` sur les pages catégorie où le header P2B (`.ck-rayon-families`) est actif — éviter double navigation |
| D5 | Seuil rebond | Catégorie définie · **`products_count > 0`** · **`products_count < 3`** · pas de recherche · pas de filtre actif (voir condition complète §Lot C) |

---

## 4. Axes d'implémentation

### Lot A — Sidebar → drawer + grille pleine largeur + toolbar

**Module** : `dorevia_ck_theme`

| # | Tâche | Détail technique |
| --- | --- | --- |
| A1 | Masquer sidebar desktop | `#products_grid_before` → `d-none` (xpath) ou SCSS `.ck-shop-page #products_grid_before { display: none }` |
| A2 | Grille pleine largeur | XPath colonne produits → `col-12` ; conserver `#o_wsale_products_grid` natif |
| A3 | Bouton Filtrer desktop | Rendre visible le toggle `data-bs-target="#o_wsale_offcanvas"` (retirer `d-lg-none` ou équivalent Odoo 19) |
| A4 | Styliser offcanvas CK | Desktop : `offcanvas-end` ~360–400 px · Mobile : plein écran · réutiliser tokens header offcanvas CK |
| A5 | Toolbar compacte | SCSS + xpath léger sur `#o_wsale_products_header` : une ligne Filtrer \| Recherche \| Tri |
| A6 | Conserver micro-copy S1 | « Affiner ma sélection », « Origines & préférences », « Budget » — déjà sur sidebar + offcanvas |
| A7 | Badge filtre actif | Natif Odoo si suffisant ; sinon indicateur visuel minimal sur le bouton Filtrer |

**Fichiers pressentis** :

- `views/website_sale_sidebar.xml` — adapter ou remplacer l'enrichissement sidebar (ne plus exposer desktop)
- `views/website_sale_shop_layout_note07.xml` *(nouveau)* — layout grille + toolbar + offcanvas toggle
- `static/src/scss/website_sale.scss` — toolbar, offcanvas shop, grille pleine largeur
- Désactiver ou adapter styles `.ck-shop-sidebar` desktop

**Interdit** : déplacer ou réécrire `form.js_attributes` · recréer `website_sale.products_attributes`.

---

### Lot B — Sous-catégories conditionnelles + filmstrip

**Module** : `dorevia_ck_marketone_content` + `dorevia_ck_theme`

| # | Tâche | Détail technique |
| --- | --- | --- |
| B1 | Épicerie | Conserver `get_ck_rayon_editorial()` + `.ck-rayon-families` (inchangé fonctionnellement) |
| B2 | Autres racines | Helper `get_ck_category_family_tiles(category)` sur `product.public.category` — enfants directs avec `_category_has_published_products` · image = 1er produit publié de la sous-catégorie (pattern `shop_rayon_editorial.py`) |
| B3 | Template tuiles | Réutiliser `.ck-rayon-family-tile` ou variante allégée · `t-if="tiles"` — **pas de bloc vide** |
| B4 | Filmstrip | Masquer sur page catégorie si `ck_rayon` actif (décision D4) · conserver sur `/shop` |

**Fichiers pressentis** :

- `shop_category_tiles.py` *(nouveau)* ou extension `shop_rayon_editorial.py`
- `models/product_public_category.py` — **méthode/helper template uniquement** (ex. `get_ck_category_family_tiles`) · **sans ajout de champ ni modification structurelle du modèle**
- `views/website_sale_category_tiles.xml` *(nouveau)*
- `views/website_sale_rayon_editorial.xml` — masquage filmstrip si besoin xpath séparé

---

### Lot C — Bloc de rebond

**Module** : `dorevia_ck_marketone_content`

| # | Tâche | Détail technique |
| --- | --- | --- |
| C1 | Helper filtre actif | `ck_shop_has_active_filters(request, post)` — attrib, tags, min/max price |
| C2 | Variables shop | Extension `WebsiteSale._get_additional_shop_values()` → `ck_show_rebound`, `ck_rebound_message`, `ck_rebound_cta_url`, `ck_rebound_cta_label` |
| C3 | Condition affichage | Voir bloc ci-dessous — **jamais** si `products_count == 0` (message natif Odoo catégorie vide) |
| C4 | Template | Section sous `#o_wsale_products_grid` · classes `.ck-shop-rebound` · pas de conflit message Odoo catégorie vide |
| C5 | Copy | Textes D1/D2 — constantes Python ou snippet statique |

**Condition rebond (verrouillée D5 / C3) :**

```text
category définie
AND products_count > 0
AND products_count < 3
AND pas de recherche active
AND pas de filtre actif
```

**Fichiers pressentis** :

- `controllers/website_sale.py` *(nouveau ou extension)*
- `shop_rebound.py` *(nouveau)* — logique pure testable
- `views/website_sale_shop_rebound.xml` *(nouveau)*
- `static/src/scss/website_sale.scss` ou fichier dédié rebond

---

### Lot D — Cards + responsive

**Module** : `dorevia_ck_theme` (+ vérif `dorevia_ck_marketone_content`)

| # | Tâche | Détail technique |
| --- | --- | --- |
| D1 | Cards sans ligne vide | Audit CSS `.ck-product-card__body` — marges/min-height quand `.ck-product-card__origin` et `.ck-product-card__meta` absents (`t-if` déjà en place) |
| D2 | Mobile 390 px | Toolbar wrap · grille 1 col · offcanvas plein écran · tuiles sous-catégories scroll horizontal si débordement |
| D3 | Overflow | `overflow-x: clip` sur container shop si nécessaire — reprendre pattern header mobile CK |

---

## 5. Slugs de recette (instance seed)

| Page | URL |
| --- | --- |
| Boutique | `/shop` |
| Épicerie | `/shop/category/epicerie-1` |
| Boissons | `/shop/category/boissons-123` |
| Soin & Bien-être | `/shop/category/soin-bien-etre-2` |
| Artisanat | `/shop/category/artisanat-3` |
| Sous-catégorie L2 | `/shop/category/epicerie-biscuits-183` |

---

## 6. Contraintes techniques (non négociables)

- **Ne pas recréer** `website_sale.products` ni le moteur de filtres.
- Scope CSS/QWeb : **`.ck-shop-page`** / `.ck-theme` uniquement.
- Conserver : pagination, URLs filtres, tri, recherche, panier, checkout, fiche produit.
- Pas de nouveau modèle Odoo · pas de champ BO · pas de modification `product.public.category` structurelle.
- Modules `dorevia_ckreyol_*` : **non installés** sur base CK — ne pas fusionner leur code sidebar Marketone.

---

## 7. Tests et recette

### 7.1 Tests automatiques

| Fichier | Action |
| --- | --- |
| `dorevia_ck_theme/tests/test_ck_shop_structure_s1.py` | Réécrire : drawer au lieu de sidebar · grille pleine largeur |
| *(nouveau)* `test_ck_shop_category_note07.py` | rebond, offcanvas desktop visible, pas de sidebar |
| `test_ck_shop_product_card.py` | Non-régression cards |
| `test_ck_shop_phase3_compose.py` | Non-régression compose / catégorie |
| `shop_rebound.py` | Tests unitaires helper filtre actif + condition rebond |

**Tags proposés** : `dorevia_ck_shop_note07`

### 7.2 Recette manuelle

Créer : `docs/design/maquette_01.2/RECETTE_QA_SHOP_CATEGORY_PAGES_CK_NOTE_07.md`  
Reprendre checklist intégrale **note_07.md §4** avec slugs §5 ci-dessus.

**Viewports** : 1280 · 800 · **390 px**

**Script capture** : étendre `ck_shop_structure_s1_captures.mjs` ou `ck_shop_category_v1_recette.mjs`

### 7.3 Non-régression obligatoire

- `/shop/product/<slug>` · `/shop/cart` · checkout
- `/` home (cards `ck-product-card--home`)
- Recherche `/shop?search=…` · filtre attrib · tri · pagination
- Header / nav (hors périmètre mais smoke test)

---

## 8. Livrables Dev

1. Code Lots A–D + bump versions modules (`dorevia_ck_theme`, `dorevia_ck_marketone_content`).
2. Fiche recette QA §7.2.
3. Captures avant/après : `/shop` 1280 · `boissons-123` · mobile 390.
4. Note de livraison courte (xpath listés, variables contrôleur rebond).

---

## 9. Plan d'exécution suggéré

| Jour | Lot | Livrable intermédiaire |
| --- | --- | --- |
| J1 | A | Sidebar masquée · drawer desktop · grille pleine largeur · tests S1 adaptés |
| J2 | A + D | Toolbar compacte · responsive 390 · cards CSS |
| J3 | B + C | Tuiles génériques · rebond · masquage filmstrip Épicerie |
| J4 | Tests + QA | Recette · captures · corrections |

---

## 10. Risques et mitigations

| Risque | Mitigation |
| --- | --- |
| Filtres cassés (`js_attributes`) | Ne pas déplacer le markup ; tester attrib + prix + reset |
| Double nav Épicerie | Décision D4 — masquer filmstrip |
| Tests S1 rouges | Mise à jour attendue dès Lot A |
| Rebond affiché après filtre | Tests unitaires `ck_shop_has_active_filters` |
| Rebond sur catégorie vide (`products_count == 0`) | Condition D5/C3 — laisser le message natif Odoo |
| Multi-site | Vérifier qu'aucun autre site n'utilise `dorevia_ck_theme` sans intention CK |

---

## 11. Références

| Document | Rôle |
| --- | --- |
| [`note_07.md`](note_07.md) | Exigences UX et checklist QA source |
| [`note_07_reponse.md`](note_07_reponse.md) | Analyse faisabilité et approche validée |
| [`RECETTE_SHOP_STRUCTURE_S1_20260624.md`](../design/maquette_01.2/RECETTE_SHOP_STRUCTURE_S1_20260624.md) | Baseline S1 (sidebar actuelle) |
| [`TICKET_DEV_SHOP_RAYON_EDITORIALISE_CK_P2.md`](../design/maquette_01.2/TICKET_DEV_SHOP_RAYON_EDITORIALISE_CK_P2.md) | Header rayon P2B Épicerie (à préserver) |

---

*Ticket Dev — Note 07 · Pages catégories boutique C-Kréyòl V1 — 26 juin 2026*
