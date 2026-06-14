# TICKET — Lot 6.3b Exécution Porte Kits & Coffrets `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_LOT6_3B_PORTE_PACK_EXEC` |
| **Lot** | 6.3b — Porte **Kits & Coffrets** (implémentation) |
| **Statut** | **GO clôture MOA** (2026-06-08) |
| **Décision MOA** | [`DECISION_MOA_LOT6_3B_KITS_COFFRETS.md`](../../cadrage2/DECISION_MOA_LOT6_3B_KITS_COFFRETS.md) |
| **Version cible module** | `19.0.18.0.0` |
| **Base** | `ckr-marketone-01` |
| **Prérequis** | Lots 1–5 **GO** · 6.1 **GO** · 6.2 **GO** · 6.3a **GO clôture MOA** `19.0.17.0.0` · cadrage 6.3b **GO MOA** — [`TICKET_LOT6_3B_PORTE_KITS_COFFRETS.md`](../../cadrage2/TICKET_LOT6_3B_PORTE_KITS_COFFRETS.md) |
| **ADR** | [ADR-034](../../cadrage/DECISIONS.md#adr-034--arbitrage-architecture-cadrage2-socle-odoo-natif) · [ADR-035](../../cadrage/DECISIONS.md#adr-035--activation-product_pack-lot-63b-kits--coffrets) · ADR-002 · ADR-003 · ADR-009 |
| **Contrats** | C2 · C3.1–C3.7 · **C3.E** |
| **Arbitrage** | [`ARBITRAGE_ARCHITECTURE_CADRAGE2.md`](../../cadrage2/ARBITRAGE_ARCHITECTURE_CADRAGE2.md) §5 |
| **Fiche MOA** | [`FICHE_MOA_LOT6_3B_KITS_COFFRETS.md`](../../cadrage2/FICHE_MOA_LOT6_3B_KITS_COFFRETS.md) |
| **Recette** | [`RECETTE_MANUELLE_LOT6_3B_PACK.md`](../../recette/lots/RECETTE_MANUELLE_LOT6_3B_PACK.md) — **GO clôture MOA** (2026-06-08) |

> **GO cadrage MOA 2026-06-08** — implémentation autorisée. **Réserve** : `sale_product_pack` hors v1 — [`TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md`](../maintenance/TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md).

---

## En-tête recette obligatoire (ADR-034 · REPRISE §2)

```markdown
**ADR-034 :** [ARBITRAGE_ARCHITECTURE_CADRAGE2.md](../../cadrage2/ARBITRAGE_ARCHITECTURE_CADRAGE2.md)

**Fonctionnalité Odoo native préservée :** Produits pack · Listes de prix · Vente eCommerce

**Mécanisme Odoo concerné :** product.template (pack_ok) · product_pack / product.pack.line · website_sale

**Non-régression référence boutique :** [REFERENCE_RECETTE_BOUTIQUE_MOA.md](../../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md) — sections B1 · B2 · B3 · B4 · B6 · B7
```

---

## Objectif

Implémenter la porte catalogue **Kits & Coffrets** sans moteur pack/prix parallèle, en s’appuyant sur **`product.template.pack_ok`** (module OCA **`product_pack`**) et le comportement natif **`website_sale`**.

```text
Critère GO Lot 6.3b :
La porte Kits & Coffrets oriente la grille /shop vers les produits pack_ok publiés,
affiche les prix via website_sale natif, expose le chip header /kits,
et ne remplace aucun moteur Odoo.
```

---

## Décisions MOA figées (cadrage GO 2026-06-08)

| # | Décision |
|---|----------|
| **K1** | **`product_pack`** dans `depends` |
| **K2** | **`sale_product_pack` hors v1** — ticket OCA séparé |
| **K3** | Filtre = **`pack_ok=True` uniquement** |
| **K4** | Chip header **Kits & Coffrets** → `/kits` |
| **K5** | Libellé **Kits & Coffrets** |
| **K6** | Composants fiche = **natif OCA** · **aucun widget Marketone** |
| **K7** | État vide = message sobre + grille vide |
| **K8** | Non-régression 6.1 / 6.2 / 6.3a + smoke panier |
| **K9** | **ADR-035** acceptée MOA |
| **M6** | SEO canonical : note documentaire · ticket SEO séparé |

**Doctrine opposable** : **Odoo exécute. Marketone habille et oriente.** · **Aucun moteur Odoo remplacé.**

---

## Périmètre inclus

### 1. Manifest — dépendance `product_pack`

| Livrable | Détail |
|----------|--------|
| `depends` | Ajouter **`product_pack`** (OCA `19.0.1.0.2`) |
| Exclus v1 | **`sale_product_pack`** — non installable 19.0 au 2026-06-08 |
| Version module | **`19.0.18.0.0`** |

### 2. Modèle `product.template` — filtre grille

Extension `_search_get_detail` :

| Option | Comportement |
|--------|--------------|
| `marketone_pack_only=True` | Domaine `[('pack_ok', '=', True)]` |
| Publication | Respecter filtres eCommerce standard (`sale_ok`, visibilité site) |
| État vide | Aucun pack publié → domaine impossible ou message porte |

**Interdit** : filtre par catégorie « Kits & Coffrets » seule · liste IDs hardcodée.

### 3. Contrôleur — extension `WebsiteSale`

| Règle | Application |
|-------|-------------|
| Mode | Ajouter `pack` à `MARKETONE_IMPLEMENTED_MODES` |
| Constante | `MARKETONE_MODE_PACK = "pack"` · `MARKETONE_PACK_CANONICAL_QUERY` |
| Whitelist | `marketone_mode=pack` — un seul mode actif (C3.6) |
| Priorité | `pack > promo > featured > origin > collection` (C3.4) — tests cumul query |
| Options | Injection `_get_search_options` → `marketone_pack_only` |
| Alias | `GET /kits` → **301** → `/shop?marketone_mode=pack` |
| Prix panier | Inchangé — moteur Odoo · pack = **une ligne** panier standard v1 |
| Filtres sidebar | **Conservés** (C3.7) |

Variables QWeb indicatives : `marketone_pack_mode`, `marketone_pack_empty`, `marketone_shop_grid_title` = **Kits & Coffrets**.

### 4. QWeb — bandeau porte `/shop`

Héritage `website_sale.products` sous `.marketone-shop` (pattern 6.3a) :

| Élément | Contenu |
|---------|---------|
| Titre | **Kits & Coffrets** |
| Intro | 1–2 phrases courtes |
| Lien retour | « Tous les produits » → `/shop` (sans `marketone_mode`) |
| État vide | Message sobre si aucun pack publié |
| Prix grille | **Natif** `website_sale` |
| Composants fiche | **Natif OCA** selon config BO `pack_type` — Marketone n’ajoute pas de widget custom |

Fichier indicatif : `views/pages/shop_pack.xml`.

### 5. Chip header navigation (M5 / K4)

| Élément | Règle |
|---------|-------|
| Libellé | **Kits & Coffrets** |
| Cible | `/kits` (alias 301) |
| Emplacement | Header site (`.marketone-chrome`) — symétrie chip Promotions |
| Exclus | Barre chips filtres actifs sidebar (UX-1 G10) |
| Tests | Autoriser `/kits` dans **header global** uniquement · mettre à jour `marketone_gate_helpers` |

### 6. Données recette BO

| Élément | Détail |
|---------|--------|
| Jeu minimal | ≥ 2 produits `pack_ok=True` publiés · ≥ 1 produit unitaire hors porte |
| Pilotes suggérés | Coffret biscuits et douceurs · Coffret gourmand îles créoles · *(option)* Assortiment apéritif · Trio sirops |
| Script prep | `scripts/prep_recette_lot6_3b_pack.py` |
| Seed | **Manuel BO / script shell** — pas de seed XML produits (C10) |

---

## Périmètre exclu

- **`sale_product_pack`** en v1 *(sauf décision MOA K2 contraire)*
- Coupons / `sale_loyalty`
- BO custom « gestion kits CK »
- SEO canonical / noindex implémenté
- Refonte Palier B2 complète (Tout · Promo · Kits · …)
- Modification tunnel checkout
- Résolution composants dans collections sidebar (ADR D3 — ticket séparé)
- Champ `marketone.pack.*` · liste composants codée en dur

---

## Tests — tag `dorevia_marketone_lot6_3b_pack`

| Test | Attendu |
|------|---------|
| `test_pack_shop_200` | `/shop?marketone_mode=pack` → 200 |
| `test_kits_301` | `/kits` → 301 · Location canonique |
| `test_pack_filters_products` | Grille = produits `pack_ok=True` publiés uniquement |
| `test_non_pack_excluded` | Produit unitaire absent de la porte pack |
| `test_pack_empty_state` | Aucun pack publié → 200 · grille vide · message |
| `test_pack_priority_over_promo` | Query `pack` + `promo` → mode **pack** actif |
| `test_unknown_mode_unchanged` | Non-régression modes existants |
| `test_featured_origin_promo_unchanged` | Portes 6.1 / 6.2 / 6.3a non régressées |
| `test_header_kits_chip` | Lien `/kits` présent header · absent chips filtres |
| `test_promotions_chip_still_present` | Chip Promotions conservé |
| `test_cart_checkout_regression` | Panier + checkout OK · prix = Odoo |
| Non-régression | Suites lot3 · lot5 · lot6_3a + lot6_3b vertes |

Fichier indicatif : `tests/test_marketone_lot6_3b_pack.py`.

---

## Fichiers attendus

```text
dorevia_ckreyol_marketone/
├── __manifest__.py                          # 19.0.18.0.0 · + product_pack
├── models/product_template.py               # étendu — branche pack
├── controllers/website_sale.py              # mode pack · alias /kits
├── views/pages/shop_pack.xml                # NEW
├── views/layout/header.xml                  # chip Kits & Coffrets
├── static/src/scss/_shop_pack.scss          # NEW (si styles porte)
├── scripts/prep_recette_lot6_3b_pack.py     # NEW
├── tests/test_marketone_lot6_3b_pack.py     # NEW
├── docs/cadrage/DECISIONS.md                # ADR-035 acceptée
├── docs/cadrage/CONTRACTS.md                # C3.E figé
├── docs/cadrage2/PREP_RECETTE_LOT6_3B_PACK.md
└── docs/recette/lots/RECETTE_MANUELLE_LOT6_3B_PACK.md
```

---

## Note de livraison (phrase obligatoire)

```text
Aucun moteur Odoo remplacé — les kits et coffrets s’appuient sur product_pack
(pack_ok, composants natifs) et les listes de prix Odoo.
Marketone présente et filtre la grille /shop uniquement.
```

---

## Critères GO exécution

- [x] GO cadrage MOA K1–K9 signé · ADR-035 acceptée (2026-06-08)
- [x] `/kits` → 301 → `/shop?marketone_mode=pack`
- [x] Grille = `pack_ok` publiés · prix affichés = Odoo natif
- [x] Chip header **Kits & Coffrets** visible · chip **Promotions** conservé
- [x] Portes 6.1 / 6.2 / 6.3a · sidebar · panier : non-régression
- [x] Tests `dorevia_marketone_lot6_3b_pack` verts
- [x] Recette MOA signée
- [x] Note livraison : **« aucun moteur Odoo remplacé »**

---

## Références

| Document | Rôle |
|----------|------|
| [`TICKET_LOT6_3B_PORTE_KITS_COFFRETS.md`](../../cadrage2/TICKET_LOT6_3B_PORTE_KITS_COFFRETS.md) | Cadrage MOA |
| [`TICKET_MARKETONE_LOT6_3A_PORTE_PROMO_EXEC.md`](./TICKET_MARKETONE_LOT6_3A_PORTE_PROMO_EXEC.md) | Pattern porte · clôturé GO |
| [`TICKET_MARKETONE_LOT6_1_INCONTOURNABLES_EXEC.md`](./TICKET_MARKETONE_LOT6_1_INCONTOURNABLES_EXEC.md) | Pattern porte |
| [`TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES_EXEC.md`](./TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES_EXEC.md) | Pattern porte |

---

## Verdict MOA exécution

| Date | Verdict | Commentaire |
|------|---------|-------------|
| 2026-06-08 | ☑ **Livré Dev** · ☑ **GO recette navigateur** · ☑ **GO clôture MOA** · ☐ NO GO | K1–K8 · N1–N3 · R1–R4 signés · [`RECEPTION_MOA_LOT6_3B_PACK.md`](../../cadrage2/RECEPTION_MOA_LOT6_3B_PACK.md) |
