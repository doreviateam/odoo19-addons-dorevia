# TICKET — Sidebar /shop — facettes contextuelles (C4)

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_SHOP_SIDEBAR_FACETTES_CONTEXTUELLES` |
| **Type** | **UX / hook** — extension `website_sale` · pas de moteur parallèle |
| **Statut** | **Clôturé GO MOA** — Lot 1 `19.0.10.9.0` (2026-05-19) |
| **Version cible** | **`19.0.10.9.0`** (patch Lot 1) |
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079/shop |
| **Prérequis** | Sidebar multi-catégories **clôturée GO MOA** — [`19.0.10.8.0`](./TICKET_MARKETONE_SHOP_SIDEBAR_FILTRES_CATEGORIES.md) |
| **Ticket parent (clôturé)** | [`TICKET_MARKETONE_SHOP_SIDEBAR_FILTRES_CATEGORIES.md`](./TICKET_MARKETONE_SHOP_SIDEBAR_FILTRES_CATEGORIES.md) |
| **Doctrine** | [ADR-029](../../cadrage/DECISIONS.md#adr-029--taxonomie-catalogue-convention-odoo-catégories-e-commerce) · [C3.7](../../cadrage/CONTRACTS.md#c3--filtres-catalogue-lot-6) |

---

## Contexte

La sidebar `/shop` (commit `1c8fa5a`, réf. **`19.0.10.8.0`**) livre :

- 13 catégories principales en cases (`marketone_category`, multi OR) ;
- combinaison AND avec Origine / Prix ;
- bouton **Effacer les filtres** lorsque des facettes sont actives.

**Limite actuelle** : les catégories affichées reposent sur `has_published_products` **sur tout le catalogue**, pas sur le **contexte courant** (`search_product`). Ex. avec **Origine = Martinique**, des catégories sans produit compatible restent visibles.

**Décision MOA (2026-05-19)** : ouvrir un raffinement UX complémentaire, découpé en lots.

---

## Règle UX — C4 (facettes contextuelles)

Dans la sidebar `/shop`, une **valeur de filtre** est affichée si :

1. elle admet **au moins un produit publié** dans le périmètre **`search_product` courant** (même périmètre que la grille produits) ;
2. **OU** elle est **déjà sélectionnée** (case cochée / facette active), afin que l’utilisateur comprenne l’état actif et puisse la retirer.

**Formulation simple** : pas de produit disponible dans le contexte = item non affiché, **sauf** si déjà actif.

**Interdit** : masquer une facette active sans alternative → grille vide incompréhensible.

```text
Périmètre unique = search_product (website_sale.shop), via hooks existants :
  _get_shop_domain · _search_get_detail · marketone_category / attribute_values / prix
```

**Pas** de moteur catalogue parallèle.

---

## Découpage MOA

| Lot | Périmètre | Version | Statut |
|-----|-----------|---------|--------|
| **Lot 1** | **Catégories principales** contextuelles | `19.0.10.9.0` | **À implémenter** (ce ticket) |
| **Lot 2** | Valeurs **Origine** (attribut) contextuelles | TBD | **Documenté — hors Lot 1** |

> Lot 2 : même règle C4 sur les valeurs d’attribut Origine. Odoo liste aujourd’hui toutes les valeurs de l’attribut ; filtrage contextuel = patch QWeb ou données dérivées de `search_product`. **Ne pas livrer en Lot 1** sauf coût marginal sans risque (arbitrage tech avant merge).

---

## Lot 1 — Catégories contextuelles (périmètre)

### Objectif

Guider l’utilisateur vers des **résultats disponibles** dans le contexte courant, sans exposer toute la taxonomie théorique.

### Règles fonctionnelles

| # | Règle |
|---|--------|
| L1.1 | L’**allowlist MOA** des **13 principales** est inchangée (libellés / ordre ADR-029). |
| L1.2 | Dans cette allowlist, n’afficher que les catégories ayant **≥ 1** produit de `search_product` dans `public_categ_ids`. |
| L1.3 | **Toujours afficher** une catégorie dont le slug est **déjà actif** (`marketone_category` dans l’URL / case cochée), même si la combinaison courante donne 0 produit. |
| L1.4 | Conserver l’**ordre MOA** des 13 (pas de tri par volume). |
| L1.5 | **Pas** de compteur `(n)` à côté des libellés. |
| L1.6 | **Ne pas** afficher les 4 secondaires dans le bloc Catégories (inchangé). |

### Exemple MOA

- Contexte : `attribute_values` = Martinique.
- **Épices** visible si au moins un produit Martinique est rattaché à Épices.
- Si l’utilisateur avait déjà coché **Biscuits salés** puis la combinaison devient vide, **Biscuits salés** reste visible (coché) pour permettre le retrait.

---

## Hors périmètre Lot 1

| Exclu | Raison |
|-------|--------|
| Lot 2 Origines | Ticket / passe séparée |
| Compteurs par catégorie | Hors scope MOA |
| Secondaires dans la sidebar | ADR-029 — inchangé |
| Savoirs v1 | Chantier distinct |
| `shop_ppg` / grille densité | Ticket distinct |
| Navigation haute · portes · collections | Hors sidebar |
| Refonte `has_published_products` globale | Remplacé par logique contextuelle sur allowlist |

---

## Approche technique (Lot 1)

### Principe

Réutiliser `search_product` déjà calculé dans `website_sale.shop()` **avant** l’appel à `_get_additional_shop_values` (présent dans `values`).

### Algorithme cible

```python
# Pseudo-code — marketone_shop_category.py + website_sale.py
allowlist = _marketone_primary_public_categories(website)  # 13, ordre MOA
active_ids = catégories résolues depuis marketone_shop_sidebar_active_category_slugs

ids_with_products = IDs de public_categ_ids présents sur search_product
# ex. read_group(product.template, ['public_categ_ids'], [], domain=[('id','in', search_product.ids)])

visible = [c for c in allowlist if c.id in ids_with_products or c.id in active_ids]
return visible  # ordre allowlist conservé
```

### Fichiers probables

| Fichier | Rôle |
|---------|------|
| `models/marketone_shop_category.py` | Méthode `_marketone_primary_public_categories_for_shop(search_product, active_category_ids, website)` |
| `controllers/website_sale.py` | `_get_additional_shop_values` : passer `search_product` · exposer liste filtrée |
| `views/pages/shop_sidebar_categories.xml` | Inchangé ou variable renommée si besoin |
| `tests/test_marketone_shop_sidebar_categories.py` | Tests HttpCase contexte Martinique + catégorie active conservée |

### Non-régression fonctionnelle (inchangé)

- Facette `marketone_category` multi OR ;
- Combinaisons Catégories + Origine + Prix (AND) ;
- `marketone_shop_sidebar.js` ;
- Effacer les filtres (`19.0.10.8.0`) ;
- `/incontournables` → `marketone_mode=featured`.

---

## Critères GO — Lot 1

| ID | Critère |
|----|---------|
| G1 | `/shop` sans filtre : seules les principales **avec produits publiés** (contexte global) sont listées |
| G2 | `Origine = Martinique` : seules les principales avec **≥ 1** produit Martinique dans `search_product` (+ actives) |
| G3 | Catégorie **active** reste visible si combinaison restrictive (0 produit en grille) |
| G4 | Ordre MOA des 13 conservé parmi les visibles |
| G5 | Multi-catégories OR inchangé |
| G6 | Combinaison Catégories + Origine + Prix inchangée |
| G7 | Effacer les filtres visible dès qu’une catégorie est active |
| G8 | `/incontournables` non-régression |
| G9 | Pas de compteur affiché |
| G10 | Secondaires toujours absentes du bloc Catégories |

---

## Recette manuelle (Lot 1)

Document à créer à l’implémentation :

[`RECETTE_MANUELLE_SHOP_SIDEBAR_FACETTES_CONTEXTUELLES.md`](../../recette/boutique/RECETTE_MANUELLE_SHOP_SIDEBAR_FACETTES_CONTEXTUELLES.md)

### Scénarios MOA (grille)

| # | Scénario | Action | Attendu |
|---|----------|--------|---------|
| **C1** | Catalogue global | `/shop` sans filtre | Principales avec au moins un produit publié global ; pas de secondaires |
| **C2** | Contexte Origine | Cocher **Martinique** | Liste catégories = intersection allowlist × produits Martinique (+ actives) |
| **C3** | Active conservée | Combinaison restrictive avec catégorie cochée | Case catégorie active **visible et cochée** |
| **C4** | Multi OR | 2 catégories compatibles | 2 cases · 2× `marketone_category` |
| **C5** | AND complet | Catégories + Origine + Prix | Non-régression combinaison |
| **C6** | Effacer filtres | Catégorie active → Effacer | `/shop` global · bouton OK |
| **C7** | Porte | `/incontournables` | 301 featured · pas de `marketone_category` |

### Tests auto

| Tag | Attendu |
|-----|---------|
| `dorevia_marketone_shop_sidebar` | Tous les tests existants **verts** + tests C2 / C3 |

---

## Lot 2 — Origines (documentation, hors implémentation)

| Sujet | Détail |
|-------|--------|
| Constat | Odoo 19 `product_attribute_filters_form` itère `a.value_ids` (toutes les valeurs), pas seulement celles de `search_product` |
| Cible | Même règle C4 : valeur visible si présente sur `search_product` **OU** dans `attrib_set` |
| Piste | `marketone_visible_attribute_value_ids` + héritage template filtre Origine |
| Arbitrage | Ticket dédié ou extension de ce ticket **après** GO Lot 1 |

---

## Validation ticket (checklist)

- [x] MOA valide le périmètre Lot 1 et le report Lot 2
- [x] Tech valide l’usage de `search_product` (pas de domaine divergent)
- [x] Recette manuelle C1–C7 — **GO MOA** (2026-05-19)
- [x] Version `19.0.10.9.0` actée
- [x] Upgrade `ckr-marketone-01` · tests auto **17/17**
- [x] Commit dédié (hors Savoirs · hors `shop_ppg`)

---

## Réserves non bloquantes (post-recette MOA)

| Sujet | Détail |
|-------|--------|
| QWeb `@class` | Warning Odoo — `views/pages/shop_clear_filters.xml` |
| `read_group` | Deprecation — `marketone_shop_category.py` ; migration `_read_group` ultérieure |

---

## Références

- Recette Lot 1 : [`RECETTE_MANUELLE_SHOP_SIDEBAR_FACETTES_CONTEXTUELLES.md`](../../recette/boutique/RECETTE_MANUELLE_SHOP_SIDEBAR_FACETTES_CONTEXTUELLES.md) — **GO MOA**
- Recette sidebar (réf.) : [`RECETTE_MANUELLE_SHOP_SIDEBAR_CATEGORIES.md`](../../recette/boutique/RECETTE_MANUELLE_SHOP_SIDEBAR_CATEGORIES.md)
- Commits sidebar : `1ced35e` (`19.0.10.7.0`) · `1c8fa5a` (`19.0.10.8.0`)
