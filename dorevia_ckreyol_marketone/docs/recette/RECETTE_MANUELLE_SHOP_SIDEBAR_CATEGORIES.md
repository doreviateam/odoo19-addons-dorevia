# Recette manuelle — Sidebar /shop — catégories principales

| Champ | Valeur |
|-------|--------|
| **Ticket** | [`TICKET_MARKETONE_SHOP_SIDEBAR_FILTRES_CATEGORIES`](../tickets/TICKET_MARKETONE_SHOP_SIDEBAR_FILTRES_CATEGORIES.md) |
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079/shop |
| **Version module** | `19.0.10.7.0` |
| **Statut recette** | **GO MOA** — signée **`19.0.10.7.0`** (2026-05-19, repasse `_107`) |

---

## Prérequis

| Élément | Détail |
|---------|--------|
| Ticket BO catégories | **Clôturé GO MOA** — [`RECETTE_MANUELLE_CATALOGUE_CATEGORIES.md`](RECETTE_MANUELLE_CATALOGUE_CATEGORIES.md) |
| Module | `dorevia_ckreyol_marketone` **≥ `19.0.10.7.0`** (upgrade `-u` sur `ckr-marketone-01`) |
| Facette catégories | Query répétable `marketone_category=<slug>` (logique **OU**) |
| JS | `marketone_shop_sidebar.js` — catégories, attributs Origine, `data-url` prix |
| Données | 13 principales + 4 secondaires sur `ckr-marketone-01` |
| Tests auto | Tag `dorevia_marketone_shop_sidebar` — **12** tests, **0** failed |
| Navigateur | Vider le cache ou hard refresh après upgrade (assets frontend) |

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf -d ckr-marketone-01 -u dorevia_ckreyol_marketone --stop-after-init
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf -d ckr-marketone-01 --test-enable --stop-after-init --http-port=18084 --test-tags=dorevia_marketone_shop_sidebar
```

---

## Règles fonctionnelles (référence MOA)

| Facette | Logique |
|---------|---------|
| **Catégories** (cases) | **OU** entre catégories cochées |
| **Origine** (attribut sidebar) | Logique existante Lot 6.2 (`attribute_values` dans l’URL) |
| **Combinaison** | Catégories **ET** Origine **ET** Prix = **AND** |
| **Conservation URL** | Cocher / décocher une facette **ne doit pas** effacer les autres paramètres actifs |

**Exemple** : Biscuits salés + Épices + Martinique → produits dans (Biscuits salés **OU** Épices) **ET** origine Martinique.

---

## Grille de recette

Cocher **MOA** après validation visuelle et fonctionnelle. La colonne **Tech** reflète les tests automatiques (à ne pas confondre avec le GO MOA).

| # | Critère | Scénario | Action / URL | Attendu | MOA | Tech |
|---|---------|----------|--------------|---------|-----|------|
| **1** | G1 | Ordre sidebar | `/shop` (desktop ≥ lg) | **Origine** → **Catégories** → **Fourchette de prix** | ☑ | ☑ |
| **2** | G1–G3 | Bloc Catégories visible | Même | Titre **Catégories** (accordéon) ; chevron comme **Origine** ; **13 cases** ouvertes par défaut ; **pas** « Tous les produits » | ☑ | ☑ |
| **2b** | G3 | Accordéon Catégories | Cliquer l’en-tête **Catégories** | Liste masquée / affichée ; chevron suit l’état | ☑ | ☑ |
| **3** | G2, G8 | Allowlist 13 principales | Parcourir la liste | Biscuits salés … Miels ; **pas** Incontournables, Apéritif créole, Cuisine du manioc, Idées cadeaux | ☑ | ☑ |
| **4** | G4, G5 | Filtre mono | Cocher **Biscuits salés** | URL `?marketone_category=…` ; grille cohérente (ex. Crackers manioc) ; case cochée | ☑ | ☑ |
| **4b** | G11 | Multi OR | Cocher **Biscuits salés** + **Épices** | Union des deux familles ; URL avec **2** `marketone_category` ; les **2** cases cochées | ☑ | ☑ |
| **4c** | G11 | Décocher / tout voir | Décocher toutes les cases catégories | Retour `/shop` **sans** `marketone_category` ; catalogue global | ☑ | ☑ |
| **4d** | G6 | **AND Catégories + Origine** | Cocher **Biscuits salés** + **Épices**, puis **Martinique** (Origine) | Cases catégories **restent cochées** ; URL garde `marketone_category` (×2) **et** `attribute_values` ; grille = intersection attendue | ☑ | ☑ |
| **4e** | G6 | Origine seule puis catégories | Cocher **Martinique**, puis **Biscuits salés** | URL : `marketone_category=…` **et** `attribute_values=3-20` ; case Martinique cochée | ☑ | ☑ |
| **5** | G12 | Pas de bandeau horizontal | `/shop` — zone sous le titre, au-dessus de la grille | **Aucun** filmstrip / ruban catégories (`o_wsale_categories_filmstrip` absent) | ☑ | ☑ |
| **6** | G10 | Porte Incontournables | `/incontournables` | **301** → `marketone_mode=featured` ; **pas** de `marketone_category` dans la cible | ☑ | ☑ |
| **7** | G6 | Filtre Origine seul | Cocher une origine sans catégorie | Grille filtrée ; pas d’erreur ; pas de cases catégories cochées par effet de bord | ☑ | ☑ |
| **8** | G7 | Filtre Prix seul | Ajuster la fourchette de prix | `min_price` / `max_price` dans l’URL ; grille cohérente | ☑ | ☑ |
| **8b** | G7 | Prix après catégories + origine | **4d** puis ajuster le **slider prix** | URL conserve `marketone_category` + `attribute_values` + prix ; cases catégories et origine **inchangées** | ☑ | ☑ |
| **9** | G9 | Non-régression BO | Fiche produit (ex. Crackers) | Rattachements catégories BO **inchangés** (hors périmètre sidebar) | ☐ | — |

---

## Détail scénarios sensibles

### 4d — Catégories + Origine (bloquant corrigé en `19.0.10.5.0`)

1. Ouvrir `/shop` (sans filtre).
2. Cocher **Biscuits salés** puis **Épices** — vérifier l’URL et la grille (OR).
3. Cocher **Martinique** dans **Origine**.
4. **Contrôles** :
   - Les cases **Biscuits salés** et **Épices** restent cochées.
   - Barre d’adresse : `marketone_category=…` (deux fois) **et** `attribute_values=…` (ex. `3-20` pour Martinique).
   - La grille ne montre que des produits dans le périmètre **(catégories OR) ET origine**.

### 4e — Origine puis catégories (symétrie de 4d)

1. Ouvrir `/shop` sans filtre.
2. Cocher **Martinique** (Origine) — URL avec `attribute_values=…`.
3. Cocher **Biscuits salés**.
4. **Contrôles** : URL contient **à la fois** `attribute_values` et `marketone_category` ; les deux cases restent cochées.

### 8b — Prix après facettes

1. Reprendre l’état **4d** (ou au minimum une catégorie + une origine).
2. Déplacer le slider **Fourchette de prix**.
3. **Contrôles** : paramètres catégories et origine toujours présents dans l’URL ; cases sidebar cohérentes avec l’URL.

---

## Verdict MOA

| Date | Verdict | Commentaire |
|------|---------|-------------|
| 2026-05-19 | **GO visuel V2** | Accordéon + cases alignées sur Origine |
| 2026-05-19 | **GO technique Option A** | Facette `marketone_category` multi OR |
| 2026-05-19 | **Correctif 4d** | `19.0.10.5.0` — conservation facettes entre Catégories / Origine / Prix |
| 2026-05-19 | **NO GO MOA** | `19.0.10.5.0` — cases Catégories sans `marketone_category` en URL (JS `isMarketoneShop` faux sélecteur) |
| 2026-05-19 | **Correctif init JS** | `19.0.10.6.0` — détection `#wrap.marketone-shop` + `.oe_website_sale` descendant |
| 2026-05-19 | **NO GO MOA** | `19.0.10.6.0` — **4e** KO : catégorie après origine perd `attribute_values` |
| 2026-05-19 | **Correctif 4e** | `19.0.10.7.0` — `buildShopParamsFromCategories` fusionne cases Origine (`form.js_attributes`) |
| 2026-05-19 | **GO MOA** | Repasse `_107` sur **`19.0.10.7.0`** — grille **1–6**, **4b–4e**, **8b** validée ; **8** (prix seul) et **9** (BO) non repassés explicitement |

**Clôture ticket sidebar** : **GO MOA** proposable sur **`19.0.10.7.0`** ; captures `_107` jointes (voir ci-dessous).

---

## Notes techniques (référence)

| Sujet | Choix |
|-------|--------|
| Résolution catégories | Allowlist par **libellé** + ordre MOA ; paramètre optionnel `dorevia_ckreyol_marketone.primary_public_category_ids` |
| Principales sans produit publié | Masquées visiteur (`has_published_products`) |
| Filmstrip | `opt_wsale_categories_top` = **False** sur `/shop` |
| Multi-catégories | `marketone_category` × n → `public_categ_ids in` (OU) |
| Combinaison AND | Hooks `_get_shop_domain` / `_search_get_detail` + JS qui **fusionne** les query params (ne pas s’appuyer sur le `onChangeAttribute` Odoo seul pour les catégories) |
| Init JS (`19.0.10.6.0`) | `isMarketoneShop()` = `#wrap.marketone-shop` contenant `.oe_website_sale` — **pas** `.oe_website_sale.marketone-shop` sur le même nœud |
| Symétrie facettes (`19.0.10.7.0`) | Changement **catégorie** → lit aussi `attribute_values` / `tags` depuis `form.js_attributes` (cases Origine cochées) |
| Recette navigateur | Après upgrade : `data-marketone-shop-sidebar-js="1"` sur `<body>` ; clic case → URL avec `marketone_category` |

---

## Captures (hors git — repasse `_107`)

| Fichier | Scénario |
|---------|----------|
| `marketone_sidebar_107_shop.png` | **1**, **2**, **3**, **5** |
| `marketone_sidebar_107_biscuits.png` | **4** |
| `marketone_sidebar_107_multi_or.png` | **4b** |
| `marketone_sidebar_107_4d_categories_origin.png` | **4d** |
| `marketone_sidebar_107_4e_origin_then_category.png` | **4e** |
| `marketone_sidebar_107_uncheck_all.png` | **4c** |
| `marketone_sidebar_107_8b_price_after_facets.png` | **8b** |

Emplacement local : `/private/tmp/` (hors dépôt git).
