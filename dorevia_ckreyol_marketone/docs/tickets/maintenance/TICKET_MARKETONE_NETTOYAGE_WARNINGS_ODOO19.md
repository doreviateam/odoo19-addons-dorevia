# TICKET — Nettoyage warnings Odoo 19 (sidebar /shop)

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_NETTOYAGE_WARNINGS_ODOO19` |
| **Type** | **Tech debt** — conformité Odoo 19 · zéro régression fonctionnelle |
| **Statut** | **Clôturé GO MOA** — `91ee35b` · `19.0.12.2.0` (2026-05-19) |
| **Version cible** | **`19.0.12.2.0`** (patch) |
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079/shop |
| **Prérequis** | Sidebar **GO MOA** — ordre rubriques `19.0.12.1.0` · Collections Lot B · Catégories C4 |
| **Merge** | 1. `feat/marketone-sidebar-ordre-12-1-0` → `main` · 2. `chore/marketone-warnings-odoo19-12-2-0` → après (1) |

---

## Contexte

Les recettes sidebar `/shop` sont **GO**. Deux **réserves non bloquantes** récurrentes dans les logs upgrade / tests :

| # | Warning | Source observée |
|---|---------|-----------------|
| W1 | QWeb — usage fragile de `@class` dans les XPath | `ir.ui.view` validation à l’upgrade |
| W2 | `read_group` déprécié → `_read_group` / `formatted_read_group` | `DeprecationWarning` au runtime |

**Objectif** : supprimer ces warnings **sans modifier** le comportement fonctionnel validé MOA.

---

## Périmètre fonctionnel inchangé (non-régression)

| Fonctionnalité | Référence recette |
|----------------|-------------------|
| Rubrique **Collections** | [`RECETTE_MANUELLE_SHOP_SIDEBAR_COLLECTIONS.md`](../../recette/boutique/RECETTE_MANUELLE_SHOP_SIDEBAR_COLLECTIONS.md) |
| Rubrique **Catégories** + C4 | [`RECETTE_MANUELLE_SHOP_SIDEBAR_FACETTES_CONTEXTUELLES.md`](../../recette/boutique/RECETTE_MANUELLE_SHOP_SIDEBAR_FACETTES_CONTEXTUELLES.md) · `RECETTE_MANUELLE_SHOP_SIDEBAR_CATEGORIES_C4_MULTI.md` (absent du dépôt) |
| **Ordre** rubriques | [`RECETTE_MANUELLE_SHOP_SIDEBAR_ORDRE.md`](../../recette/boutique/RECETTE_MANUELLE_SHOP_SIDEBAR_ORDRE.md) |
| **Effacer les filtres** | [`RECETTE_MANUELLE_SHOP_SIDEBAR_CATEGORIES.md`](../../recette/boutique/RECETTE_MANUELLE_SHOP_SIDEBAR_CATEGORIES.md) |

**Hors périmètre** : Savoirs · `shop_ppg` · évolutions UX sidebar.

---

## W1 — QWeb `@class` → `hasclass()`

### Symptôme

```
Error-prone use of @class in view … use the hasclass(*classes) function
```

### Règle Odoo 19

Remplacer les sélecteurs du type :

```xml
contains(@class, 'ma-classe')
```

par :

```xml
hasclass('ma-classe')
```

Pour plusieurs classes sur le même nœud : `hasclass('py-3', 'border-bottom')`.

### Fichiers cibles

| Fichier | XPath actuel (indicatif) | Action |
|---------|--------------------------|--------|
| `views/pages/shop_sidebar_collections.xml` | `contains(@class, 'o_wsale_products_grid_before_rail')` | `hasclass('o_wsale_products_grid_before_rail')` |
| `views/pages/shop_clear_filters.xml` | `contains(@class, 'py-3')` · `border-bottom` · `oi-close` · `border-top` | `hasclass(...)` |

> Les XPath sur `@t-attf-class` (`shop_sidebar_origin_label.xml`) ne déclenchent pas ce warning — hors lot sauf observation contraire en upgrade.

---

## W2 — `read_group` → `_read_group`

### Symptôme

```
read_group is deprecated. Please use _read_group in the backend code
```

### Fichier cible

`models/marketone_shop_category.py` — méthode `_marketone_primary_public_categories_for_shop` (C4 catégories contextuelles).

### Migration indicatif

**Avant** (`read_group` public API) :

```python
groups = self.env["product.template"].read_group(
    [("id", "in", search_product.ids)],
    ["public_categ_ids"],
    ["public_categ_ids"],
)
categ_ids_with_products = {
    row["public_categ_ids"][0]
    for row in groups
    if row.get("public_categ_ids")
    and row["public_categ_ids"][0] in allowlist_ids
}
```

**Après** (`_read_group` ORM 19 — aligné `website_sale`) :

```python
grouped = self.env["product.template"]._read_group(
    domain=[("id", "in", search_product.ids)],
    groupby=["public_categ_ids"],
)
categ_ids_with_products = {
    group[0].id
    for group in grouped
    if group[0] and group[0].id in allowlist_ids
}
```

**Invariant** : ensemble des principales affichées = allowlist ∩ catégories ayant ≥ 1 produit dans `search_product` ∪ catégories actives.

---

## Livrables

| Livrable | Détail |
|----------|--------|
| Patch code | W1 + W2 ci-dessus |
| Version | Bump patch `19.0.12.2.0` |
| Tests auto | Tags `dorevia_marketone_shop_sidebar` · `dorevia_marketone_shop_sidebar_collections` — **0** failed |
| Logs | Upgrade + tests sans warnings W1 / W2 |

---

## Validation attendue

```bash
# Upgrade (doit charger les vues sans warning @class)
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf -d ckr-marketone-01 \
  -u dorevia_ckreyol_marketone --stop-after-init 2>&1 | tee /tmp/marketone_upgrade.log

# Tests sidebar
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf -d ckr-marketone-01 \
  --test-enable --stop-after-init --http-port=18084 \
  --test-tags=dorevia_marketone_shop_sidebar,dorevia_marketone_shop_sidebar_collections 2>&1 | tee /tmp/marketone_tests.log
```

| Critère | Attendu |
|---------|---------|
| Tests | **30/30** (ou effectif actuel) · **0** failed |
| Log upgrade | **Aucun** warning `Error-prone use of @class` sur vues Marketone sidebar |
| Log tests | **Aucun** `read_group is deprecated` depuis `marketone_shop_category.py` |

Recette manuelle : **non obligatoire** si tests auto + inspection logs OK (changement interne sans impact UX).

---

## Critères d’acceptation

| # | Critère | Tech |
|---|---------|------|
| G1 | W1 corrigé sur `shop_sidebar_collections.xml` et `shop_clear_filters.xml` | ☑ |
| G2 | W2 corrigé sur `marketone_shop_category.py` | ☑ |
| G3 | Non-régression tests sidebar + collections | ☑ **30/30** |
| G4 | Logs upgrade / tests sans les deux warnings listés | ☑ **0** `Error-prone` à l’upgrade |
| G5 | Aucun changement hors fichiers du périmètre | ☑ |

---

## Risques

| Risque | Mitigation |
|--------|------------|
| XPath `hasclass` ne matche plus le parent | Vérifier upgrade module + test HTTP existants |
| `_read_group` M2M format différent | Aligner sur `website_sale` `product_public_category` · tests C4 |

---

## Références

| Document | Lien |
|----------|------|
| Recette ordre (réserves) | [`RECETTE_MANUELLE_SHOP_SIDEBAR_ORDRE.md`](../../recette/boutique/RECETTE_MANUELLE_SHOP_SIDEBAR_ORDRE.md) |
| Ticket C4 | [`TICKET_MARKETONE_SHOP_SIDEBAR_FACETTES_CONTEXTUELLES.md`](../boutique/TICKET_MARKETONE_SHOP_SIDEBAR_FACETTES_CONTEXTUELLES.md) |
| Odoo 19 `hasclass` | Validation `ir.ui.view` |
| Odoo 19 `_read_group` | `odoo.orm.models.BaseModel._read_group` |
