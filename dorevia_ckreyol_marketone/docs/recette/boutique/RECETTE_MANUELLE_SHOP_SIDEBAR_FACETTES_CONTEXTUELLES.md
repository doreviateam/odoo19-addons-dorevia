# Recette manuelle — Sidebar /shop — facettes contextuelles (C4)

| Champ | Valeur |
|-------|--------|
| **Ticket** | [`TICKET_MARKETONE_SHOP_SIDEBAR_FACETTES_CONTEXTUELLES`](../../tickets/boutique/TICKET_MARKETONE_SHOP_SIDEBAR_FACETTES_CONTEXTUELLES.md) |
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079/shop |
| **Version module** | `19.0.10.9.0` |
| **Statut recette** | **GO MOA** — Lot 1 catégories (2026-05-19) |

---

## Prérequis

| Élément | Détail |
|---------|--------|
| Sidebar de base | **GO MOA** — [`RECETTE_MANUELLE_SHOP_SIDEBAR_CATEGORIES.md`](./RECETTE_MANUELLE_SHOP_SIDEBAR_CATEGORIES.md) · `19.0.10.8.0` |
| Module | `dorevia_ckreyol_marketone` **≥ `19.0.10.9.0`** |
| Tests auto | Tag `dorevia_marketone_shop_sidebar` — **17/17** OK |

---

## Règle C4 (rappel)

Afficher une catégorie principale si :

- elle a **≥ 1** produit dans le périmètre `search_product` courant (hors facette catégorie, pour permettre le multi OR) ;
- **OU** elle est **déjà cochée** (slug actif dans l’URL).

---

## Grille de recette — Lot 1 (catégories)

| # | Scénario | Action | Attendu | MOA | Tech |
|---|----------|--------|---------|-----|------|
| **C1** | Catalogue global | `/shop` sans filtre | Principales avec produits publiés dans le contexte ; pas de secondaires | ☑ | ☑ |
| **C2** | Contexte Origine | Cocher **Martinique** dans la sidebar | Dans le bloc **Catégories**, seules les principales ayant ≥ 1 produit Martinique ; **aucune** principale sans produit compatible Martinique ne doit apparaître (cases absentes) ; catégories actives conservées si applicable | ☑ | ☑ |
| **C3** | Active conservée | Appliquer une combinaison restrictive (ex. Origine + catégorie sans produit commun) avec une catégorie **déjà cochée** | La case de cette catégorie reste **visible et cochée** même si la grille est vide, afin de pouvoir la décocher | ☑ | ☑ |
| **C4** | Multi OR | 2 catégories compatibles avec le contexte | Non-régression multi `marketone_category` | ☑ | ☑ |
| **C5** | AND complet | Catégories + Origine + Prix | Non-régression | ☑ | ☑ |
| **C6** | Effacer filtres | Catégorie active → Effacer | `/shop` sans `marketone_category` | ☑ | ☑ |
| **C7** | Porte | `/incontournables` | 301 featured | ☑ | ☑ |

### Détail C2 (contrôle sidebar)

1. Ouvrir `/shop` — noter les principales visibles.
2. Cocher **Martinique** (attribut Origine).
3. Vérifier le bloc **Catégories** : toute principale listée doit avoir au moins un produit publié **Martinique** dans la grille courante (hors facette catégorie).
4. Vérifier qu’une principale connue sans produit Martinique (ex. si le catalogue le permet) **n’apparaît plus** dans la sidebar.

### Détail C3 (active conservée)

1. Partir d’un contexte filtré (ex. **Martinique**).
2. Cocher une catégorie principale (ex. une catégorie peu peuplée en Martinique).
3. Si la combinaison donne **0 produit** en grille : la case de la catégorie cochée doit rester **affichée et cochée**.
4. Décocher la catégorie → la liste se recalcule ; la grille peut se repeupler.

---

## Verdict MOA

| Date | Verdict | Commentaire |
|------|---------|-------------|
| 2026-05-19 | **GO MOA** | C1–C7 validés navigateur · tests auto 17/17 · Lot 2 Origines / Savoirs / `shop_ppg` hors périmètre |

---

## Réserves non bloquantes

| Sujet | Détail |
|-------|--------|
| QWeb `@class` | Warning Odoo sur `views/pages/shop_clear_filters.xml` (héritage sidebar `19.0.10.8.0`) |
| `read_group` | Deprecation warning dans `models/marketone_shop_category.py` — migration future vers `_read_group` / `formatted_read_group` |

---

## Captures (hors git)

Répertoire local : `/private/tmp/`

| Fichier | Scénario |
|---------|----------|
| `marketone_sidebar_109_c1_shop_global.png` | **C1** — `/shop` sans filtre |
| `marketone_sidebar_109_c2_martinique_categories.png` | **C2** — Origine Martinique, catégories filtrées |
| `marketone_sidebar_109_c3_active_conserved.png` | **C3** — catégorie active visible/cochée, combinaison restrictive |

---

## Tests auto

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone \
  --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_shop_sidebar \
  --http-port=8072
```

Attendu : **0** failed.
