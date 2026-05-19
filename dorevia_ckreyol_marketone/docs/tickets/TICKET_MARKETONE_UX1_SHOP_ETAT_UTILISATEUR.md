# TICKET — UX-1 — État utilisateur `/shop` (chips filtres actifs)

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_UX1_SHOP_ETAT_UTILISATEUR` |
| **Type** | **UX** — extension `website_sale` · présentation uniquement |
| **Statut** | **Clôturé GO MOA** — `19.0.13.0.4` (recette F1–F4 + régression 3/3) |
| **Version cible** | **`19.0.13.0.2`** (patch UX — R1 prix implicite · R2 libellé compteur) |
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079/shop |
| **Référence graphique** | [`docs/Carole/ux1_qweb.xml`](../Carole/ux1_qweb.xml) · [`docs/Carole/ux1_scss.scss`](../Carole/ux1_scss.scss) |
| **Prérequis techniques** | `main` **≥ `19.0.12.2.0`** (ordre sidebar + warnings Odoo 19) |

---

## 1. Analyse d’intégration du kit Carole

### 1.1 Intention UX retenue

| Élément | Intention Carole | Alignement MOA |
|---------|------------------|----------------|
| **Chips** | Une chip par facette active (Collections, Catégories, Origines, Prix) | ☑ Cible UX-1 |
| **Suppression chip** | Lien URL (croix) retirant **uniquement** cette facette | ☑ Pas de JS si possible |
| **Reset global** | « Effacer les filtres » à proximité des chips | ☑ Réutiliser sémantique `keep(..., *=0)` existante |
| **Compteur** | « **N** produit(s) » au-dessus de la grille | ☑ `search_count` déjà fourni par `website_sale` |
| **Style** | Premium léger, terracotta, pills | ☑ Traduire via tokens Marketone existants |
| **Réunion / Reunion** | Pas de hack QWeb doublon | ☑ **Données BO** (harmonisation libellés attribut) — hors implémentation QWeb |

### 1.2 Écarts entre le kit et l’architecture Marketone

| Point kit Carole | Problème | Intégration proposée |
|------------------|----------|----------------------|
| Variables QWeb `active_collections`, `active_categories`, `active_origins`, `price_min`, `unlink_url` | N’existent pas ; logique absente du contrôleur | **`marketone_active_filter_chips`** construit en Python dans `_get_additional_shop_values` |
| Lecture implicite `request.params` / prix bruts | Contourne `keep()` et `_shop_get_query_url_kwargs` | URLs **`remove_url`** générées côté contrôleur avec la même base que sidebar / clear |
| **`position="replace"`** sur `#o_wsale_products_header` | **Casse** titre shop, fil d’Ariane, recherche, tri, pricelist, structure éditoriale Odoo | **Injection ciblée** : chips **avant** `#products_grid` / `o_wsale_products_main_row` ; compteur **dans** `.products_header` (prepend) |
| Classes `c-kreyol-*`, `c-chip` | Non scopées · doublon tokens | Préfixe **`.marketone-shop`** · BEM `marketone-filter-chips__*` |
| SCSS variables `$coffee`, `$terracotta` en dur | Diverge de `_tokens_colors.scss` | Mapper sur `$marketone-primary-container`, `$marketone-text`, `$marketone-border`, etc. |
| `t-call="website_sale.products_sort"` dans un header remplacé | Fragile si options tri désactivées | **Ne pas remplacer** le header ; conserver `t-call` natif |
| Chips hors périmètre (tags, `search`, `marketone_mode`) | Kit ne les traite pas | UX-1 : **4 types MOA** uniquement ; tags/recherche/portes **hors chips** (comportement Odoo inchangé) |
| Sidebar « Effacer les filtres » | Doublon fonctionnel | **Conserver** le bouton sidebar (recette ordre GO) ; zone chips = **complément** au-dessus de la grille |

### 1.3 Ancrage QWeb recommandé (Odoo 19 CE)

```text
website_sale.products
├── xpath BEFORE div.o_wsale_products_main_row     → barre chips (pleine largeur colonne principale)
└── xpath INSIDE header#o_wsale_products_header
         → div.products_header (prepend)             → compteur résultats (si filtres actifs OU toujours — arbitrage MOA §4.3)
```

**Ne pas** modifier : `#products_grid_before` (sidebar), facettes C4, ordre rubriques `19.0.12.1.0`.

### 1.4 Construction des `remove_url` (sans JS)

Réutiliser le contrat existant :

| Facette | Paramètre query | Retrait d’une chip |
|---------|-----------------|-------------------|
| Collection | `marketone_collection` (répétable) | `keep()` avec liste slugs **sans** le slug retiré |
| Catégorie | `marketone_category` (répétable) | idem |
| Origine | `attribute_values` (`attr_id-value_id`) | `keep()` en retirant **une** paire pour l’attribut Origine |
| Prix | `min_price`, `max_price` | `keep(min_price=0, max_price=0)` |

**Reset global** : aligné sur [`shop_clear_filters.xml`](../../views/pages/shop_clear_filters.xml) :

```python
keep(attribute_values=0, tags=0, min_price=0, max_price=0,
     marketone_category=0, marketone_collection=0)
```

Implémentation Python : méthode dédiée du contrôleur (ex. `_marketone_build_shop_keep_url(**overrides)`) s’appuyant sur `_shop_get_query_url_kwargs` déjà surchargé (`marketone_category`, `marketone_collection`).

**Portes** (`marketone_mode`, `marketone_origin`) : ne pas afficher de chip « mode » en UX-1 ; si le filtre origine passe par `attribute_values`, chip **type `origin`** sur la valeur d’attribut (comme sidebar).

---

## 2. Objectif et périmètre

### 2.1 Objectif

Améliorer la **lisibilité de l’état actif** des filtres **au-dessus de la grille produits** sur `/shop` :

- chips retirables par facette ;
- compteur global de résultats ;
- lien « Effacer les filtres » proche des chips ;
- rendu premium / terracotta cohérent Marketone.

### 2.2 In scope

| # | Livrable |
|---|----------|
| I1 | Structure `marketone_active_filter_chips` (+ flags / URLs) exposée par le contrôleur |
| I2 | Template QWeb dédié (sous-template appelé depuis `website_sale.products`) |
| I3 | SCSS scopé `.marketone-shop` (fichier dédié ou section `_shop.scss`) |
| I4 | Tests HTTP minimalistes (présence chips, `remove_url`, reset, non-régression sidebar) |
| I5 | Recette manuelle MOA |

### 2.3 Hors périmètre UX-1

| Hors scope | Note |
|------------|------|
| Ordre sidebar | Livré `19.0.12.1.0` |
| Compteurs par facette `(n)` | ADR / tickets sidebar |
| Bottom sheet mobile filtres | Ticket futur |
| Refonte cartes produits | — |
| Modification C4 (logique `search_product`) | Inchangée |
| Nouveaux modèles / champs BO | — |
| Savoirs · `shop_ppg` | — |
| JS chips (si URLs suffisent) | **Éviter** |
| Harmonisation BO Réunion/Reunion | Ticket données / Origines — **pas** QWeb |

### 2.4 Non-régression obligatoire

- Facettes : `marketone_collection`, `marketone_category`, `attribute_values`, `min_price` / `max_price`.
- C4 catégories / collections (sidebar).
- Combinaisons AND documentées en recette ordre / collections.
- Bouton sidebar « Effacer les filtres » (desktop + offcanvas).

---

## 3. Variables contrôleur à exposer

Extension de **`WebsiteSale._get_additional_shop_values`** ([`controllers/website_sale.py`](../../controllers/website_sale.py)).

### 3.1 Structure principale

```python
# Liste ordonnée pour l’affichage MOA : Collections → Catégories → Origines → Prix
result["marketone_active_filter_chips"] = [
    {
        "type": "collection",       # collection | category | origin | price
        "label": "Apéritif créole",
        "remove_url": "/shop?...",  # URL absolue ou relative — même origine que keep()
        "key": "aperitif-creole",   # optionnel : slug ou identifiant stable (tests, a11y)
    },
    # ...
]
```

### 3.2 Drapeaux et agrégats

| Variable | Type | Rôle |
|----------|------|------|
| `marketone_active_filter_chips` | `list[dict]` | Chips à afficher (peut être vide) |
| `marketone_has_active_filters` | `bool` | `True` si ≥ 1 chip **ou** filtres hors UX-1 actifs (voir §3.4) |
| `marketone_reset_filters_url` | `str` | URL reset global (équivalent clear sidebar) |
| `marketone_search_count` | `int` | Alias explicite de `search_count` pour QWeb / tests |
| `marketone_show_filter_state_bar` | `bool` | Afficher la barre chips (ex. `bool(chips)`) — évite `t-if` complexes en QWeb |

**Existant à conserver** (sidebar, C4) : `marketone_has_category_filter`, `marketone_has_collection_filter`, `marketone_shop_sidebar_active_*_slugs`, etc.

### 3.3 Règles de construction des chips

| `type` | Source label | Condition d’une chip |
|--------|--------------|----------------------|
| `collection` | `marketone.shop.collection.name` | Slug résolu et actif dans la query (même résolution que facettes) |
| `category` | `product.public.category.name` | Slug `marketone_category` actif (principale allowlist) |
| `origin` | `product.attribute.value.name` | Valeur attribut **Origine** présente dans `attrib_values` / query `attribute_values` |
| `price` | Libellé formaté devise site | `isFilteringByPrice` ou min/max > 0 (aligné `website_sale`) |

**Ordre d’affichage des chips** : Collections → Catégories → Origines → Prix (miroir sidebar MOA).

**Prix** : une seule chip si fourchette active (libellé « Prix : X — Y » ou variante min/max seul), `remove_url` remet `min_price` et `max_price` à 0.

### 3.4 `marketone_has_active_filters`

Proposition MOA (à confirmer) :

```text
True si :
  marketone_active_filter_chips non vide
  OU tags actifs
  OU recherche texte active (search)
```

Pour UX-1, la **barre chips** n’apparaît que si `marketone_show_filter_state_bar` (= chips non vides). Le lien reset global dans la barre suit la même condition. Le bouton sidebar garde sa logique actuelle (inclut tags / attrib / prix).

---

## 4. Stratégie QWeb / SCSS

### 4.1 Fichiers prévus (après GO MOA)

| Fichier | Rôle |
|---------|------|
| `views/pages/shop_filter_state.xml` | Template `marketone_shop_filter_state_bar` + inherit `website_sale.products` |
| `static/src/scss/_shop_filter_state.scss` | Styles chips · import dans `web.assets_frontend` via `_shop.scss` ou manifest |
| `controllers/website_sale.py` | Helpers URL + remplissage `marketone_active_filter_chips` |
| `tests/test_marketone_shop_filter_state.py` | Tag `dorevia_marketone_shop_filter_state` |

### 4.2 QWeb

```xml
<!-- Sous-template réutilisable -->
<template id="marketone_shop_filter_state_bar" name="Marketone: barre état filtres /shop">
  <section t-if="marketone_show_filter_state_bar"
           class="marketone-filter-state"
           aria-label="Filtres actifs">
    <div class="marketone-filter-chips">
      <t t-foreach="marketone_active_filter_chips" t-as="chip">
        <a t-att-href="chip['remove_url']"
           t-attf-class="marketone-filter-chips__chip marketone-filter-chips__chip--#{chip['type']}"
           t-att-title="'Retirer ' + chip['label']">
          <span class="marketone-filter-chips__label" t-out="chip['label']"/>
          <span class="marketone-filter-chips__remove oi oi-close" aria-hidden="true"/>
        </a>
      </t>
      <a t-if="marketone_has_active_filters"
         t-att-href="marketone_reset_filters_url"
         class="marketone-filter-chips__reset">
        Effacer les filtres
      </a>
    </div>
  </section>
</template>
```

*(Exemple indicatif — le markup final sera validé à l’implémentation.)*

**Héritage** (indicatif) :

```xml
<template inherit_id="website_sale.products" name="Marketone: UX-1 état filtres">
  <xpath expr="//div[hasclass('o_wsale_products_main_row')]" position="before">
    <t t-call="dorevia_ckreyol_marketone.marketone_shop_filter_state_bar"/>
  </xpath>
  <xpath expr="//div[hasclass('products_header')]" position="inside">
    <!-- prepend : compteur -->
    <p t-if="marketone_search_count is not None" class="marketone-filter-state__count mb-0">
      <strong t-out="marketone_search_count"/> produit<t t-if="marketone_search_count != 1">s</t>
    </p>
  </xpath>
</template>
```

- XPath **`hasclass()`** uniquement (conformité `19.0.12.2.0`).
- Icône : **`oi oi-close`** (cohérence Odoo) plutôt que SVG inline du kit.
- Pas de logique métier dans le template : **uniquement** boucle sur `marketone_active_filter_chips`.

### 4.3 SCSS

- **Scope racine** : `.marketone-shop .marketone-filter-state { ... }` (ou `#wrap.marketone-shop`).
- **Tokens** : réutiliser `_tokens_colors.scss` — pas de palette parallèle Carole.
- **Traduction visuelle** du kit :
  - pill `border-radius: 100px` ;
  - bordure `$marketone-border` · hover `$marketone-primary-container` ;
  - fond `$marketone-surface` ;
  - reset en `$marketone-primary-container` (terracotta MOA).
- **Responsive** : reprendre intentions Carole (wrap, reset en ligne séparée mobile) sans classes `c-*`.

### 4.4 JavaScript

**Aucun JS UX-1** si les `remove_url` sont correctes (navigation full page). Le JS sidebar existant ([`marketone_shop_sidebar.js`](../../static/src/js/marketone_shop_sidebar.js)) reste la source de vérité pour les **nouveaux** filtres cochés ; les chips ne font qu’**afficher** et **retirer** via URL.

---

## 5. Critères de recette (MOA)

Document cible : `docs/recette/RECETTE_MANUELLE_SHOP_UX1_ETAT_FILTRES.md` (à créer après GO ticket).

### 5.1 Prérequis

- Module **≥ `19.0.13.0.0`** (ou version retenue au merge).
- Données : au moins 1 collection publiée, catégories principales, valeurs Origine (Martinique, etc.).
- Hard refresh navigateur.

### 5.2 Grille MOA

| # | Scénario | Action | Attendu | MOA | Tech |
|---|----------|--------|---------|-----|------|
| **U1** | Sans filtre | `/shop` nu | **Pas** de barre chips ; compteur optionnel selon arbitrage §3.4 | ☐ | ☐ |
| **U2** | 1 collection | Cocher **Col-A** | 1 chip collection · libellé correct · grille filtrée | ☐ | ☐ |
| **U3** | Retrait chip collection | Clic croix sur chip Col-A | URL sans ce `marketone_collection` · filtre retiré · autres facettes conservées | ☐ | ☐ |
| **U4** | Multi catégories | **Épices** + **Biscuits salés** | 2 chips catégories · OR inchangé | ☐ | ☐ |
| **U5** | Origine | **Martinique** | 1 chip **Origines** (libellé valeur) · `attribute_values` conservé ailleurs | ☐ | ☐ |
| **U6** | Combinaison | Col-A + Épices + Martinique | 3+ chips · ordre **Collections → Catégories → Origines** | ☐ | ☐ |
| **U7** | Prix | Fourchette prix | 1 chip prix · libellé avec devise | ☐ | ☐ |
| **U8** | Reset barre | « Effacer les filtres » (barre chips) | `/shop` nu · plus de chips | ☐ | ☐ |
| **U9** | Reset sidebar | Bouton sidebar clear (non-régression) | Même résultat que U8 | ☐ | ☐ |
| **U10** | Compteur | Avec filtres actifs | « **N** produit(s) » cohérent avec la grille | ☐ | ☐ |
| **U11** | C4 | Martinique + liste catégories sidebar | Sidebar C4 inchangée · chips reflètent l’état URL | ☐ | ☐ |
| **U12** | Mobile desktop | Redimensionner | Chips wrap · reset lisible (pas de bottom sheet) | ☐ | ☐ |

### 5.3 Tests auto attendus (tech)

| Test | Assertion |
|------|-----------|
| `test_shop_filter_chips_single_collection` | Chip présente · `remove_url` sans slug |
| `test_shop_filter_chips_remove_category_keeps_origin` | Retrait 1 catégorie · origine conservée |
| `test_shop_reset_filters_url` | Reset = clear sidebar |
| `test_shop_no_chips_without_filters` | Pas de `marketone-filter-chips` dans le HTML |
| Non-régression | `dorevia_marketone_shop_sidebar` + `collections` — **0** failed |

### 5.4 Logs / upgrade

- **0** warning `Error-prone use of @class` sur les nouvelles vues.
- Pas de `read_group` ajouté.

---

## 6. Découpage technique (après GO MOA)

| Étape | Contenu | Version |
|-------|---------|---------|
| **E1** | Helpers URL + `marketone_active_filter_chips` dans le contrôleur | `19.0.13.0.0` |
| **E2** | QWeb + SCSS | idem |
| **E3** | Tests + recette manuelle | idem |

**Estimation** : 1 patch UX (pas de migration données sauf ticket Réunion/Reunion séparé).

---

## 7. Questions ouvertes MOA (avant GO)

| # | Question | Proposition par défaut |
|---|----------|------------------------|
| Q1 | Afficher le compteur **sans** filtre actif ? | Oui, discret dans `.products_header` |
| Q2 | Masquer la barre chips si seul `marketone_mode=origin` (porte) sans `attribute_values` ? | Pas de chips (hors facettes UX-1) |
| Q3 | Libellé chip collection : nom seul ou préfixe « Collection : » ? | Nom seul (comme kit) |
| Q4 | Doublon reset sidebar + barre chips acceptable ? | Oui (recette U8/U9) |

---

## 8. Références

| Document | Lien |
|----------|------|
| Kit Carole QWeb | [`docs/Carole/ux1_qweb.xml`](../Carole/ux1_qweb.xml) |
| Kit Carole SCSS | [`docs/Carole/ux1_scss.scss`](../Carole/ux1_scss.scss) |
| Clear filters | [`views/pages/shop_clear_filters.xml`](../../views/pages/shop_clear_filters.xml) |
| Ordre sidebar GO | [`RECETTE_MANUELLE_SHOP_SIDEBAR_ORDRE.md`](../recette/RECETTE_MANUELLE_SHOP_SIDEBAR_ORDRE.md) |
| Collections Lot B | [`TICKET_MARKETONE_COLLECTION_LOT_B_SIDEBAR.md`](TICKET_MARKETONE_COLLECTION_LOT_B_SIDEBAR.md) |
| Tokens couleurs | [`static/src/scss/_tokens_colors.scss`](../../static/src/scss/_tokens_colors.scss) |

---

## 9. Verdict ticket

| Date | Verdict | Commentaire |
|------|---------|-------------|
| 2026-05-19 | **GO MOA exécution** | Arbitrages Q1–Q4 intégrés · version `19.0.13.0.0` |
| 2026-05-19 | **Recette MOA — réserves** | R1 prix implicite · R2 compteur ambigu → correctifs `19.0.13.0.2` |
| 2026-05-19 | **GO MOA visuel** | Sans / avec filtres — hors UX-2/UX-3/BO Réunion |
| 2026-05-19 | **Clôture fonctionnelle** | R1 retrait chip + C4 sidebar → `19.0.13.0.4` · recette F1–F4 + tag `dorevia_marketone_shop_regression` |
| 2026-05-19 | **GO MOA clôture** | F1–F4 navigateur OK · `dorevia_marketone_shop_regression` 3/3 · captures `/private/tmp/marketone_ux1_cloture_*` |
| | Recette | [`RECETTE_MANUELLE_SHOP_UX1_ETAT_FILTRES.md`](../recette/RECETTE_MANUELLE_SHOP_UX1_ETAT_FILTRES.md) |
