# TICKET — Collections commerciales — Lot B (sidebar `/shop`)

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_COLLECTION_LOT_B_SIDEBAR` |
| **Type** | **UX / hook** — extension `website_sale` · pas de moteur parallèle |
| **Statut** | **Clôturé MOA** — `19.0.12.0.0` (2026-05-19) |
| **Version cible** | **`19.0.12.0.0`** |
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079/shop |
| **Prérequis** | Lot A **GO MOA** — [`19.0.11.0.0`](TICKET_MARKETONE_COLLECTION_LOT_A.md) · commit `e81f920` |
| **ADR** | [ADR-030](../cadrage/DECISIONS.md#adr-030--collection-commerciale-marketone) |
| **Sidebar réf.** | Catégories multi OR `19.0.10.8.0` · C4 catégories `19.0.10.9.0` |
| **Recette** | [`RECETTE_MANUELLE_SHOP_SIDEBAR_COLLECTIONS.md`](../recette/RECETTE_MANUELLE_SHOP_SIDEBAR_COLLECTIONS.md) |

---

## Objectif

Exposer les **collections commerciales** (`marketone.shop.collection`, Lot A) dans la sidebar `/shop` comme **facette transversale** du catalogue, **sans** nouveau modèle métier.

```text
Critère GO Lot B :
Sur /shop, l’utilisateur coche une ou plusieurs collections (OR),
combine avec Origine / Catégories / Prix (AND),
voit la grille filtrée, peut effacer tous les filtres,
et ne voit que les collections pertinentes au contexte (C4).
```

---

## Doctrine MOA (confirmée)

| # | Règle |
|---|--------|
| D1 | Rubrique **Collections** : ordre sidebar = **Origine** · **Catégories** · **Collections** · **Fourchette de prix** |
| D2 | Facette query **`marketone_collection=<slug>`** — répétable (multi OR entre collections) |
| D3 | Combinaison **AND** avec `attribute_values` (Origine), `marketone_category`, min/max prix |
| D4 | **C4** : une collection est listée si **≥ 1** produit dans `search_product` courant (hors facette collection) **OU** slug déjà actif (case cochée) |
| D5 | **Pas** de compteur `(n)` |
| D6 | **Effacer les filtres** : réinitialise aussi `marketone_collection` |
| D7 | Périmètre filtre = même moteur que la grille (`_search_get_detail` / `_get_shop_domain`) — **pas** de moteur parallèle |
| D8 | **Candidatures** : `active` · `website_published` · `website_id` compatible site courant · fenêtre **date_start / date_end** (jour courant) |
| D9 | Slugs **invalides** / collection non publiée / hors date dans l’URL → **ignorés** (pas de grille vide) — voir § ci-dessous |
| D10 | Cadrage général + version **`19.0.12.0.0`** — **GO MOA** (2026-05-19) |

### Phrase de doctrine (ADR-030)

La catégorie classe · l’origine situe · le pack compose · la **collection propose**.

---

## Périmètre inclus (Lot B)

### 1. Sidebar — rubrique Collections

| Élément | Détail |
|---------|--------|
| UI | Accordéon **Collections** — cases à cocher (symétrique **Catégories**) |
| Données | Collections **éligibles** uniquement (D8) · ordre `sequence`, `name` |
| C4 | Liste filtrée via `search_product` **sans** facette `marketone_collection` ∪ collections actives |
| JS | Extension `marketone_shop_sidebar.js` — slugs · navigation · conservation croisée |

### 2. Filtre catalogue `/shop`

| Hook | Rôle |
|------|------|
| `_get_search_options` | Option `marketone_collection_ids` ou slugs résolus |
| `product.template._search_get_detail` | Domaine produit ∈ union des produits des collections actives (OR) |
| `_get_shop_domain` | Cohérence min/max prix si applicable |
| `_shop_get_query_url_kwargs` | Préservation `marketone_collection` (pagination, attributs) |
| `_get_additional_shop_values` | Listes sidebar · slugs actifs · `marketone_has_collection_filter` |

### 3. Paramètre HTTP

```http
/shop?marketone_collection=aperitif-creole
/shop?marketone_collection=aperitif-creole&marketone_collection=idees-cadeaux
```

- Secondaires `product.public.category` : **inchangé** — pas confondues avec collections.

### 3bis. Éligibilité des collections (D8)

Une collection est **candidate** (sidebar + filtre) si **toutes** les conditions :

| Condition | Règle |
|-----------|--------|
| `active` | `True` |
| `website_published` | `True` |
| Site | `website_id` vide **ou** = site courant |
| Dates | `date_start` vide ou ≤ aujourd’hui ; `date_end` vide ou ≥ aujourd’hui |
| Produits BO | ≥ 1 produit `sale_ok` + `website_published` (déjà Lot A) |

Méthode indicatif : `_marketone_is_eligible_for_shop(website, today=None)`.

### 3ter. Slugs invalides — ignorer, pas grille vide (D9)

**Décision MOA** : les slugs `marketone_collection` **non résolus** (inconnu, brouillon, hors date, autre site) sont **ignorés** — le catalogue s’affiche **sans** filtre collection sur ces slugs.

| Comportement | Catégories (existant) | Collections Lot B (MOA) |
|--------------|----------------------|------------------------|
| Slug invalide seul dans l’URL | Grille vide (`marketone_category_invalid`) | **Pas** de filtre collection · catalogue contextualisé (Origine, etc. conservés) |
| Slug valide + invalide | Invalide → grille vide | Filtre sur **valides uniquement** |
| Sidebar | — | Slug invalide **jamais** proposé en case |

**Compatibilité architecture** : **oui**. Même hooks (`_resolve_*` → IDs → `_search_get_detail`). Différence volontaire : **ne pas** poser `marketone_collection_invalid` ; appliquer le filtre seulement si ≥ 1 collection résolue. `_shop_get_query_url_kwargs` / JS ne propagent que les slugs **canoniques valides**.

**Cas limite C4** : slug actif dans l’URL mais collection devenue non éligible → traité comme ignoré (pas de case sidebar, pas de filtre).

### 4. Relaxation facette (C4 + multi OR)

Étendre `_marketone_sidebar_facet_omit` :

| Facette neutralisée | Usage |
|---------------------|--------|
| `category` | Comptage catégories C4 (existant) |
| `collection` | Comptage collections C4 (nouveau) |

Lors du calcul des collections visibles : `search_product` **sans** `marketone_collection`, **avec** Origine / Catégories / Prix / recherche / modes porte inchangés.

### 5. Effacer les filtres

- `marketone_has_collection_filter` si ≥ 1 slug actif.
- `keep(..., marketone_category=0, marketone_collection=0)` — desktop + offcanvas.

### 6. Tests auto

| Tag | Couverture |
|-----|------------|
| `dorevia_marketone_shop_sidebar_collections` | Facette simple · multi OR · AND Origine+catégorie+collection · C4 contexte · clear filters · non-régression |

Non-régression obligatoire : tag `dorevia_marketone_shop_sidebar` (**17** tests existants).

### 7. Fichiers probables

| Fichier | Rôle |
|---------|------|
| `models/marketone_shop_collection.py` | `_marketone_is_eligible_for_shop`, `_marketone_resolve_published_slugs`, `_marketone_collections_for_shop` |
| `controllers/website_sale.py` | Facette collection · omit · additional values |
| `models/product_template.py` | Extension `_search_get_detail` (domaine collection) |
| `views/pages/shop_sidebar_collections.xml` | QWeb cases |
| `views/pages/shop_clear_filters.xml` | Flag collection |
| `static/src/js/marketone_shop_sidebar.js` | Cases collections |
| `tests/test_marketone_shop_sidebar_collections.py` | HttpCase + TransactionCase |

---

## Hors périmètre Lot B

| Exclu | Lot / note |
|-------|------------|
| Homepage · `homepage_featured` | **Lot C** |
| Route `/collections/<slug>` · SEO · canonical | ADR-030 D6 · ticket ultérieur |
| Migration secondaires → collections | ADR-030 D1 |
| Refonte `marketone_mode=featured` / `/incontournables` | Inchangé |
| Lot 2 Origines contextuelles (C4 attribut) | Ticket séparé |
| Nouveau modèle métier | Lot A suffit |
| Savoirs · `shop_ppg` | Hors périmètre |
| Compteurs sidebar | Hors scope MOA |

---

## Décisions MOA actées (2026-05-19)

| # | Sujet | Décision |
|---|--------|----------|
| **B1** | C4 sans produit en contexte | Masquées sauf actives (cochées) |
| **B2** | Slugs invalides | **Ignorer** — pas `id=0` (écart catégories documenté) |
| **B3** | Candidatures | D8 — éligibilité stricte |
| **B4** | `marketone_mode=featured` + collection | AND sur sous-ensemble porte (symétrique catégories) |
| **B5** | Pas de `marketone_mode=collection` | Facette query uniquement |
| **B6** | Données recette | ≥ 2 collections publiées — profils distincts (voir recette) |

---

## Jeu de données recette (MOA)

| Collection (ex.) | Rôle recette | Produits |
|------------------|--------------|----------|
| **A** — ex. *Apéritif créole* | S2, S3, S5 · produits Martinique + autres | Mix origines |
| **B** — ex. *Idées cadeaux* | S3 OR · S7 masquage Martinique | Peu ou pas de Martinique |
| *(optionnel)* brouillon | Hors sidebar | Non publiée |
| *(optionnel)* hors dates | Hors sidebar | `date_end` passée |

Permet : filtre simple · multi OR · AND Martinique · C4 masquage · S8 active conservée.

---

## Critères GO — Lot B

| ID | Critère |
|----|---------|
| G1 | Rubrique **Collections** visible entre Catégories et Prix |
| G2 | Une collection publiée cochée filtre la grille |
| G3 | Multi `marketone_collection` = OR |
| G4 | AND : collection + Origine + catégorie + prix |
| G5 | C4 : avec Origine Martinique, seules collections compatibles (+ actives) |
| G6 | Collection active visible si combinaison restrictive (grille vide) |
| G7 | Effacer les filtres supprime `marketone_category` **et** `marketone_collection` |
| G8 | Conservation croisée Origine ↔ Collections ↔ Catégories (JS) |
| G9 | `/incontournables` non-régression |
| G10 | Tests `dorevia_marketone_shop_sidebar` + `dorevia_marketone_shop_sidebar_collections` verts |
| G11 | URL `marketone_collection=slug-invalide` → catalogue **sans** filtre collection (pas grille vide totale) |

---

## Non-régression

| Zone | Référence |
|------|-----------|
| Catégories multi OR | `19.0.10.8.0` |
| Catégories C4 | `19.0.10.9.0` |
| BO collections | `19.0.11.0.0` |
| Portes featured / origin | Lots 6.1 / 6.2 |

---

## Validation ticket (checklist)

Avant d’implémenter :

- [x] MOA valide doctrine D1–D10 et périmètre
- [x] Arbitrage slugs invalides (ignorer) — B2
- [x] Décisions B1–B6 actées
- [x] Version `19.0.12.0.0` actée
- [x] Structure recette — **GO MOA**
- [x] **Données BO** : collections **Col-A** + **Col-B** publiées (B6)
- [x] **Recette navigateur** S1–S11 exécutée — **GO MOA recette**
- [x] **GO implémentation** (après recette uniquement)

Après implémentation :

- [x] Upgrade `ckr-marketone-01` · tests auto · recette MOA
- [x] Commit dédié (hors Savoirs · hors `shop_ppg`)

---

## Réserves non bloquantes (post-recette)

| Sujet | Détail |
|-------|--------|
| QWeb `@class` | `views/pages/shop_clear_filters.xml` |
| `read_group` | `models/marketone_shop_category.py` (C4) |

---

## Références

- Lot A : [`TICKET_MARKETONE_COLLECTION_LOT_A.md`](TICKET_MARKETONE_COLLECTION_LOT_A.md)
- Sidebar catégories : [`TICKET_MARKETONE_SHOP_SIDEBAR_FILTRES_CATEGORIES.md`](TICKET_MARKETONE_SHOP_SIDEBAR_FILTRES_CATEGORIES.md)
- C4 catégories : [`TICKET_MARKETONE_SHOP_SIDEBAR_FACETTES_CONTEXTUELLES.md`](TICKET_MARKETONE_SHOP_SIDEBAR_FACETTES_CONTEXTUELLES.md)
- Recette : [`RECETTE_MANUELLE_SHOP_SIDEBAR_COLLECTIONS.md`](../recette/RECETTE_MANUELLE_SHOP_SIDEBAR_COLLECTIONS.md)
