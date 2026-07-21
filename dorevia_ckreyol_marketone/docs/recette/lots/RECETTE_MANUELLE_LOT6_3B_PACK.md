# Recette manuelle — Lot 6.3b Porte Kits & Coffrets

| Champ | Valeur |
|-------|--------|
| **Ticket exécution** | [`TICKET_MARKETONE_LOT6_3B_PORTE_PACK_EXEC.md`](../../tickets/lots/TICKET_MARKETONE_LOT6_3B_PORTE_PACK_EXEC.md) |
| **Cadrage** | [`TICKET_LOT6_3B_PORTE_KITS_COFFRETS.md`](../../cadrage2/TICKET_LOT6_3B_PORTE_KITS_COFFRETS.md) — GO cadrage MOA avec réserves |
| **Décision MOA** | [`DECISION_MOA_LOT6_3B_KITS_COFFRETS.md`](../../cadrage2/DECISION_MOA_LOT6_3B_KITS_COFFRETS.md) |
| **ADR** | [ADR-034](../../cadrage/DECISIONS.md#adr-034--arbitrage-architecture-cadrage2-socle-odoo-natif) · [ADR-035](../../cadrage/DECISIONS.md#adr-035--activation-product_pack-lot-63b-kits--coffrets) |
| **Base** | `ckr-marketone-01` |
| **URL shop** | http://localhost:18079/shop |
| **Version module** | `19.0.19.0.1` |
| **Statut recette** | **Clôturée — GO navigateur MOA** (2026-06-14) · voir [`RAPPORT_RECETTE_NAVIGATEUR_CHANTIER_B_20260614.md`](./RAPPORT_RECETTE_NAVIGATEUR_CHANTIER_B_20260614.md) |
| **Réception MOA** | [`RECEPTION_MOA_LOT6_3B_PACK.md`](../../cadrage2/RECEPTION_MOA_LOT6_3B_PACK.md) — **GO clôture MOA** |

---

## Préparation base (Dev — 2026-06-08)

Jeu préparé sur `ckr-marketone-01` — détail : [`PREP_RECETTE_LOT6_3B_PACK.md`](../../cadrage2/PREP_RECETTE_LOT6_3B_PACK.md)

| Rôle | Produit | ID template | Attendu porte pack |
|------|---------|-------------|--------------------|
| **Pack A** | Maniocookies salés La Platine | 7 | Visible |
| **Pack B** | Crackers manioc Sainte-Anne | 8 | Visible |
| **Témoin unitaire** | Pâtes de manioc Mayotte | 9 | **Absent** |

```bash
# Rejouer la préparation si besoin
docker exec -i sandbox-odoo19-odoo-1 odoo shell -d ckr-marketone-01 --no-http \
  < odoo19-addons-dorevia/dorevia_ckreyol_marketone/scripts/prep_recette_lot6_3b_pack.py
```

> **Accès sandbox** : ouvrir http://localhost:18079/web/login · base **`ckr-marketone-01`** · puis recette front (évite le 404 multi-base).

**Ordre recette MOA** : K1 → N1/N2/N3 → K2/K3 → K4/K5 → R1–R4 → K6 → K7/K8.

**Réserves** : `sale_product_pack` hors v1 · explosion composants vente / stock / préparation / facturation hors clôture 6.3b · échec isolé lot 6.2 hors clôture 6.3b.

---

## Validation MOA — architecture + tests auto (2026-06-08)

| Élément | Verdict |
|---------|---------|
| Doctrine ADR-034 · C3.E · ADR-035 | **GO cadrage avec réserves** |
| Tests `dorevia_marketone_lot6_3b_pack` | **13/13 OK** |
| Non-régression 6.3a · 6.1 · 6.3 · 6.5 | **80/81 OK** — réserve connue `test_origin_mode_alone_full_catalog` |
| Livraison Dev | [`NOTE_LIVRAISON_LOT6_3B_PACK.md`](../../cadrage2/NOTE_LIVRAISON_LOT6_3B_PACK.md) |

> **Recette navigateur MOA exécutée le 2026-06-08** : K1–K8 · N1–N3 · R1–R4 signés.

## Signature MOA — navigateur (2026-06-08)

| Contrôle | Preuve recette | Verdict |
|----------|----------------|---------|
| K1 | `GET /kits` → 301 `/shop?marketone_mode=pack` | **OK** |
| K2 | `/shop?marketone_mode=pack` → 200 · titre **Kits & Coffrets** · Maniocookies + Crackers visibles | **OK** |
| K3 | Pâtes de manioc Mayotte absente de la porte pack | **OK** |
| K4 | Prix grille / fiche / panier = moteur Odoo (pricelist active) ; aucun recalcul JS Marketone | **OK** |
| K5 | Lien « Tous les produits » → `/shop` sans `marketone_mode` | **OK** |
| K6 | `pack_ok` désactivé temporairement sur **7**/**8** → message « Aucun kit ou coffret… » · grille vide · état restauré | **OK** |
| K7 | `marketone_mode=pack&marketone_mode=promo` → mode pack actif | **OK** |
| K8 | Portes promo / featured / origin → 200 · non-régression | **OK** |
| N1–N3 | Header Kits + Promotions · pas de chip porte dans filtre actif | **OK** |
| R1–R4 | `/shop`, facettes, images, panier/checkout smoke (pack **7** = 1 ligne) | **OK** |

## Arbitrages MOA — recette navigateur 2026-06-14

| Sujet | Décision |
|-------|----------|
| **K6** | Accepté **non rejoué** — manipulation BO `pack_ok` couverte 2026-06-08 |
| **N2** | Cohabitation chips Promotions + Kits · **OK release 6.3** |
| **Clôture** | [`RAPPORT_RECETTE_NAVIGATEUR_CHANTIER_B_20260614.md`](./RAPPORT_RECETTE_NAVIGATEUR_CHANTIER_B_20260614.md) |

---

## En-tête obligatoire (ADR-034 / ADR-035)

**ADR-034 :** [`ARBITRAGE_ARCHITECTURE_CADRAGE2.md`](../../cadrage2/ARBITRAGE_ARCHITECTURE_CADRAGE2.md)

**ADR-035 :** activation `product_pack` Lot 6.3b Kits & Coffrets.

**Fonctionnalité Odoo native préservée :** Produits pack · Listes de prix · Vente eCommerce

**Mécanisme Odoo concerné :** `product.template.pack_ok` · `product_pack` / `product.pack.line` · `website_sale`

**Non-régression référence boutique :** [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../REFERENCE_RECETTE_BOUTIQUE_MOA.md) — sections **B1 · B2 · B3 · B4 · B6 · B7**

---

## Prérequis recette BO

| Élément | Détail |
|---------|--------|
| **Module** | `dorevia_ckreyol_marketone` mis à jour en `19.0.18.0.0` avec dépendance `product_pack` installée |
| **Packs publiés** | ≥ 2 produits `sale_ok=True`, `is_published=True`, `pack_ok=True` avec lignes `product.pack.line` |
| **Témoin unitaire** | ≥ 1 produit publié `pack_ok=False` |
| **Prix** | Prix affichés par `website_sale` / pricelist Odoo, sans recalcul Marketone |
| **Hors v1** | `sale_product_pack` non activé : pas de validation explosion composants en commande |

---

## Grille — Porte Kits & Coffrets

| # | Scénario | Action | Attendu | MOA |
|---|----------|--------|---------|-----|
| **K1** | Alias | `GET /kits` | **301** → `/shop?marketone_mode=pack` | ☑ |
| **K2** | Grille pack | Ouvrir canonique | 200 · titre **Kits & Coffrets** · produits `pack_ok=True` uniquement | ☑ |
| **K3** | Témoin unitaire | Comparer avec `/shop` | Produit `pack_ok=False` absent de la porte pack | ☑ |
| **K4** | Prix affichés | Comparer fiche / grille | Prix = moteur Odoo · **pas** recalcul JS Marketone | ☑ |
| **K5** | Retour catalogue | Lien « Tous les produits » | `/shop` sans `marketone_mode` | ☑ |
| **K6** | État vide | Retirer temporairement `pack_ok` des packs test | 200 · message sobre · grille vide | ☑ |
| **K7** | Priorité modes | Query `marketone_mode=pack&marketone_mode=promo` | Mode **pack** actif · pas de bandeau promo | ☑ |
| **K8** | Portes existantes | `/shop?marketone_mode=promo` · featured · origin | Non-régression 6.3a / 6.1 / 6.2 | ☑ |

---

## Navigation — Chips header

| # | Scénario | Action | Attendu | MOA |
|---|----------|--------|---------|-----|
| **N1** | Chip Kits | Header site depuis `/shop` | Lien **Kits & Coffrets** → `/kits` | ☑ |
| **N2** | Chip Promotions conservé | Header site | Lien **Promotions** → `/promotions` toujours présent | ☑ |
| **N3** | Chips filtres | Filtre sidebar + porte pack | **Pas** de chip porte dans barre filtres actifs (UX-1 G10) | ☑ |

---

## Non-régression globale

| # | Scénario | Référence | MOA |
|---|----------|-----------|-----|
| **R1** | Smoke `/shop` | REFERENCE § B1 | ☑ |
| **R2** | Sidebar facettes | REFERENCE § B3 | ☑ |
| **R3** | Tuiles / images | REFERENCE § B4 | ☑ |
| **R4** | Panier / checkout smoke | Lot 5 · pack vendu comme une ligne produit standard v1 | ☑ |

---

## Tests automatisés

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d ckr-marketone-01 \
  --test-tags=dorevia_marketone_lot6_3b_pack \
  --stop-after-init --http-port=0
```

Non-régression :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d ckr-marketone-01 \
  --test-tags=dorevia_marketone_lot6_3a_promo,dorevia_marketone_lot6_1_featured,dorevia_marketone_lot6_2_origin,dorevia_marketone_lot3,dorevia_marketone_lot5 \
  --stop-after-init --http-port=0
```

---

## Note de livraison (phrase obligatoire)

> **Aucun moteur Odoo remplacé** — les kits et coffrets s'appuient sur `product_pack` (`pack_ok`, composants natifs) et les listes de prix Odoo. Marketone présente et filtre la grille `/shop` uniquement.

---

## Réserves MOA

| Sujet | Traitement |
|-------|------------|
| `sale_product_pack` | **Hors v1** — [`TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md`](../../tickets/maintenance/TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md) |
| Explosion composants vente / stock / préparation / facturation | **Non recettée 6.3b** — pack vendu comme produit standard côté front |
| Échec isolé lot 6.2 | **Hors clôture 6.3b** si aucun impact navigateur constaté |
| SEO canonical / noindex | Note documentaire uniquement — ticket SEO séparé |

---

## Verdict MOA

| Date | Verdict | Commentaire |
|------|---------|-------------|
| 2026-06-08 | ☑ **GO recette architecture** · ☑ **GO recette navigateur** · ☑ **GO clôture** · ☐ NO GO | K1–K8 · N1–N3 · R1–R4 signés · état base restauré après K6 |
