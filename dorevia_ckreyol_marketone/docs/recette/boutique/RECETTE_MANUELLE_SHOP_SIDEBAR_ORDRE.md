# Recette manuelle — Sidebar /shop — ordre des rubriques + libellé Origines

| Champ | Valeur |
|-------|--------|
| **Périmètre** | Ordre fixe des rubriques sidebar · renommage **Origine** → **Origines** |
| **ADR** | [ADR-030](../../cadrage/DECISIONS.md#adr-030--collection-commerciale-marketone) |
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079/shop |
| **Version module** | `19.0.12.1.0` |
| **Statut recette** | **GO MOA** — O1–O9 validés (2026-05-19) |

---

## Contexte MOA

La sidebar doit d’abord proposer les **intentions commerciales**, puis la **nature produit**, puis la **provenance** :

1. **Collections**
2. **Catégories**
3. **Origines**
4. **Fourchette de prix**

**Hors périmètre** : pas de paramétrage BO de séquence ; pas de changement fonctionnel sur les filtres (C4, AND, slugs, etc.).

**Évolution documentée (non livrée)** : séquence BO par rubrique sidebar — voir ADR-030.

---

## Prérequis

| Élément | Détail |
|---------|--------|
| Module | `dorevia_ckreyol_marketone` **≥ `19.0.12.1.0`** |
| Lots préalables | Collections Lot B **GO** (`19.0.12.0.0`) · Catégories + C4 **GO** |
| Upgrade | Obligatoire avant recette |

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf -d ckr-marketone-01 \
  -u dorevia_ckreyol_marketone --stop-after-init

docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf -d ckr-marketone-01 \
  --test-enable --stop-after-init --http-port=18084 \
  --test-tags=dorevia_marketone_shop_sidebar,dorevia_marketone_shop_sidebar_collections
```

| Navigateur | Hard refresh (Ctrl+Shift+R) après upgrade — assets SCSS |

---

## Implémentation (référence tech)

| Couche | Détail |
|--------|--------|
| QWeb | Collections injectées **avant** le bloc catégories (`shop_sidebar_collections.xml`) ; offcanvas idem |
| SCSS | `flex-order` sur `#products_grid_before .o_wsale_products_grid_before_rail` |
| Libellé | QWeb `shop_sidebar_origin_label.xml` + `marketone_origin_attribute_id` (contrôleur) |
| Data | `marketone_product_attribute_origin_label.xml` (nouvelles bases) |

---

## Grille de recette

Cocher **MOA** après validation. **Tech** = test auto ou inspection code.

### Desktop (≥ lg)

| # | Scénario | Action | Attendu | MOA | Tech |
|---|----------|--------|---------|-----|------|
| **O1** | Ordre rubriques | `/shop` — lire la sidebar gauche de haut en bas | **Collections** → **Catégories** → **Origines** → **Fourchette de prix** | ☑ | ☑ `test_shop_sidebar_rubrique_order` |
| **O2** | Libellé Origines | Même — en-tête accordéon attribut territoire | Titre **Origines** (pas « Origine ») | ☑ | ☑ |
| **O3** | Collections ouvertes | `/shop` nu | Rubrique **Collections** en **première** position ; accordéon dépliable | ☑ | ☑ |
| **O4** | Non-régression filtres | **Apéritif créole** + **Épices** + **Martinique** | URL : `marketone_collection=aperitif-creole` + `marketone_category=epices-83` + `attribute_values=3-20` · grille filtrée | ☑ | ☑ |
| **O5** | Effacer les filtres | Avec filtres actifs | Bouton visible **au-dessus** des rubriques ; clic → `/shop` nu | ☑ | ☑ |

### Mobile (offcanvas filtres)

| # | Scénario | Action | Attendu | MOA | Tech |
|---|----------|--------|---------|-----|------|
| **O6** | Ordre offcanvas | Icône filtres → panneau latéral | **Collections** → **Catégories** → **Origines** → **Fourchette de prix** | ☑ | ☑ |
| **O7** | Libellé offcanvas | Même | En-tête attribut = **Origines** | ☑ | ☑ |

### Non-régression croisée

| # | Scénario | Référence | Attendu | MOA | Tech |
|---|----------|-----------|---------|-----|------|
| **O8** | C4 catégories | `RECETTE_MANUELLE_SHOP_SIDEBAR_CATEGORIES_C4_MULTI.md` (absent du dépôt) | Multi-sélection catégories toujours possible | ☑ | ☑ |
| **O9** | Collections Lot B | [`RECETTE_MANUELLE_SHOP_SIDEBAR_COLLECTIONS.md`](./RECETTE_MANUELLE_SHOP_SIDEBAR_COLLECTIONS.md) | Facette `marketone_collection` inchangée | ☑ | ☑ |

---

## Détail O1 — ordre desktop

1. Ouvrir `/shop` en fenêtre **≥ 992 px** (sidebar visible).
2. Repérer le rail gauche (`#products_grid_before`).
3. Noter l’ordre des **titres** d’accordéon / rubriques :
   - **Collections**
   - **Catégories**
   - **Origines**
   - **Fourchette de prix** (ou libellé Odoo « Price Range » selon langue site)

> Le bouton **Effacer les filtres** peut apparaître **en tête** du rail lorsque des filtres sont actifs — ce n’est pas une rubrique MOA.

---

## Détail O2 — libellé Origines

- Vérifier l’**en-tête** de la rubrique attribut (pas les valeurs Martinique / Guadeloupe).
- Attendu MOA : **Origines** au pluriel.

---

## Verdict

| Date | Verdict | Commentaire |
|------|---------|-------------|
| 2026-05-19 | **GO technique / GO MOA structure** | Module `19.0.12.1.0` · tests auto **30/30** (`dorevia_marketone_shop_sidebar` + `dorevia_marketone_shop_sidebar_collections`) · desktop + offcanvas validés |

### Synthèse exécution (2026-05-19)

| Contrôle | Résultat |
|----------|----------|
| Version module | `19.0.12.1.0` confirmée |
| Tests auto | **30** post-tests · **0** failed · **0** error(s) |
| Test ordre | `test_shop_sidebar_rubrique_order` OK |
| Desktop `/shop` | Collections → Catégories → Origines → Fourchette de prix |
| Libellé | **Origines** (pluriel) |
| O4 | `marketone_collection=aperitif-creole` + `marketone_category=epices-83` + `attribute_values=3-20` |
| O5 | Clear au-dessus des rubriques · retour `/shop` nu |
| Non-régression | C4 catégories · Collections Lot B OK |

**Réserves non bloquantes** : ~~warnings QWeb `@class`~~ · ~~`read_group` déprécié~~ — corrigées `19.0.12.2.0` ([`TICKET_MARKETONE_NETTOYAGE_WARNINGS_ODOO19`](../../tickets/maintenance/TICKET_MARKETONE_NETTOYAGE_WARNINGS_ODOO19.md)).

---

## Captures

| Fichier | Scénario |
|---------|----------|
| `/private/tmp/marketone_sidebar_ordre_o1_o2.png` | O1–O2 — ordre desktop + libellé Origines |
| `/private/tmp/marketone_sidebar_ordre_o4_filtres.png` | O4 — combinaison 3 facettes |
| `/private/tmp/marketone_sidebar_ordre_o5_clear_visible.png` | O5 — bouton clear visible |
| `/private/tmp/marketone_sidebar_ordre_o5_after_clear.png` | O5 — après clear (`/shop` nu) |

---

## Documents liés

| Document | Lien |
|----------|------|
| Collections Lot B | [`RECETTE_MANUELLE_SHOP_SIDEBAR_COLLECTIONS.md`](./RECETTE_MANUELLE_SHOP_SIDEBAR_COLLECTIONS.md) |
| Catégories | [`RECETTE_MANUELLE_SHOP_SIDEBAR_CATEGORIES.md`](./RECETTE_MANUELLE_SHOP_SIDEBAR_CATEGORIES.md) |
| C4 multi | `RECETTE_MANUELLE_SHOP_SIDEBAR_CATEGORIES_C4_MULTI.md` (absent du dépôt) |
| Décisions | [`DECISIONS.md`](../../cadrage/DECISIONS.md) — ADR-030 |
