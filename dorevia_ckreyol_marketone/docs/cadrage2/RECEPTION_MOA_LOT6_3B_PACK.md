# Réception MOA — Lot 6.3b Porte Kits & Coffrets `19.0.18.0.0`

| Champ | Valeur |
|-------|--------|
| **Version** | `19.0.18.0.0` |
| **Date réception** | 2026-06-08 |
| **Date clôture** | 2026-06-08 |
| **Cadrage** | [`TICKET_LOT6_3B_PORTE_KITS_COFFRETS.md`](./TICKET_LOT6_3B_PORTE_KITS_COFFRETS.md) — GO cadrage MOA avec réserves |
| **Décision MOA** | [`DECISION_MOA_LOT6_3B_KITS_COFFRETS.md`](./DECISION_MOA_LOT6_3B_KITS_COFFRETS.md) |
| **Ticket exécution** | [`TICKET_MARKETONE_LOT6_3B_PORTE_PACK_EXEC.md`](../tickets/lots/TICKET_MARKETONE_LOT6_3B_PORTE_PACK_EXEC.md) |
| **Livraison Dev** | [`NOTE_LIVRAISON_LOT6_3B_PACK.md`](./NOTE_LIVRAISON_LOT6_3B_PACK.md) |
| **Recette manuelle** | [`RECETTE_MANUELLE_LOT6_3B_PACK.md`](../recette/lots/RECETTE_MANUELLE_LOT6_3B_PACK.md) |
| **Préparation base** | [`PREP_RECETTE_LOT6_3B_PACK.md`](./PREP_RECETTE_LOT6_3B_PACK.md) |
| **Verdict livraison** | **Reçu — GO recette architecture + GO recette navigateur** |
| **Verdict grille K1–R4** | **Signée — GO** (2026-06-08) |
| **Clôture lot** | **GO MOA** (2026-06-08) |

---

## Réponse MOA

Lot `19.0.18.0.0` **clôturé GO MOA**.

```text
Odoo exécute. Marketone habille et oriente.
Aucun moteur Odoo remplacé.
```

### Points validés

| Point | Verdict |
|-------|---------|
| Source vérité pack = `product_pack` · `pack_ok` · `product.pack.line` | ✓ |
| Filtre porte = `[('pack_ok', '=', True)]` uniquement (C3.E) | ✓ |
| Alias `/kits` → **301** → `/shop?marketone_mode=pack` | ✓ |
| Chip header **Kits & Coffrets** · **Promotions** conservé | ✓ |
| Prix affiché / calculé par Odoo — Marketone filtre et oriente | ✓ |
| Panier v1 = **1 ligne pack** (produit standard `website_sale`) | ✓ |
| En-tête recette ADR-034 · ADR-035 obligatoire | ✓ |
| `sale_product_pack` **non activé** en v1 | ✓ |

### Tests automatisés (MOA)

| Suite | Résultat |
|-------|----------|
| `dorevia_marketone_lot6_3b_pack` | **13/13 OK** |
| Non-régression 6.3a · 6.1 · 6.2 · lot3 · lot5 | **80/81 OK** — réserve `test_origin_mode_alone_full_catalog` hors clôture |

---

## Clôture recette navigateur (2026-06-08)

Recette exécutée et signée sur `ckr-marketone-01` — détail : [`RECETTE_MANUELLE_LOT6_3B_PACK.md`](../recette/lots/RECETTE_MANUELLE_LOT6_3B_PACK.md) § Signature MOA.

| Zone | Résultat |
|------|----------|
| K1–K8 | **Validé** |
| N1–N3 | **Validé** |
| R1–R4 | **Validé** — smoke `/shop`, facettes, images, panier/checkout |

### Contrôles clés MOA

- Porte pack : **Maniocookies** (tmpl **7**) + **Crackers** (tmpl **8**) uniquement · **Pâtes de manioc Mayotte** (tmpl **9**) absente
- K4 prix : affichage / panier = moteur Odoo (pricelist active · items promo 6.3a encore présents sur **7**/**8**) · aucun recalcul JS Marketone
- K6 état vide : `pack_ok` désactivé temporairement sur **7**/**8** → message « Aucun kit ou coffret… » + grille vide
- R4 panier : pack **7** ajouté → **1 ligne** · `/shop/cart` et checkout smoke OK
- **État base restauré** : script prep rejoué · `pack_ok=True` sur **7**/**8**

> **Accès sandbox** : session via http://localhost:18079/web/login · base **`ckr-marketone-01`** avant recette front.

---

## Réserves et hors périmètre

| Sujet | Traitement |
|-------|------------|
| `sale_product_pack` | **Hors v1** — [`TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md`](../tickets/maintenance/TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md) |
| Explosion composants vente / stock / préparation / facturation | **Non recettée 6.3b** · **hors clôture v1** |
| Échec isolé lot 6.2 (`test_origin_mode_alone_full_catalog`) | **Hors clôture 6.3b** — aucun impact navigateur constaté |
| SEO canonical / noindex | Note documentaire — ticket SEO séparé |

---

## Verdict final

| Date | Verdict |
|------|---------|
| 2026-06-08 | ☑ **GO recette architecture** · ☑ **GO recette navigateur** · ☑ **GO clôture MOA** |

**Note livraison opposable** : *Aucun moteur Odoo remplacé.*

---

## Suite

- Port OCA `sale_product_pack` — diagnostic [`DIAGNOSTIC_MOA_SALE_PRODUCT_PACK_19.md`](./DIAGNOSTIC_MOA_SALE_PRODUCT_PACK_19.md) · ticket [`TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md`](../tickets/maintenance/TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md) · **activation reportée** · Phase A port OCA
- Reprise progressive autres lots front gelés — [`REPRISE_LOTS_FRONT_CADRAGE2.md`](./REPRISE_LOTS_FRONT_CADRAGE2.md)
