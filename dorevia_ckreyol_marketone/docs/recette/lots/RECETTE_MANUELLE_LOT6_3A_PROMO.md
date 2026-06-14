# Recette manuelle — Lot 6.3a Porte Promotions

| Champ | Valeur |
|-------|--------|
| **Ticket exécution** | [`TICKET_MARKETONE_LOT6_3A_PORTE_PROMO_EXEC.md`](../../tickets/lots/TICKET_MARKETONE_LOT6_3A_PORTE_PROMO_EXEC.md) |
| **Cadrage** | [`TICKET_LOT6_3_PORTE_PROMO_PACK.md`](../../cadrage2/TICKET_LOT6_3_PORTE_PROMO_PACK.md) — GO MOA 2026-06-08 |
| **ADR** | [ADR-034](../../cadrage/DECISIONS.md#adr-034--arbitrage-architecture-cadrage2-socle-odoo-natif) |
| **Base** | `ckr-marketone-01` |
| **URL shop** | http://localhost:18079/shop |
| **Version module** | `19.0.19.0.1` |
| **Statut recette** | **Clôturée — GO navigateur MOA** (2026-06-14) · voir [`RAPPORT_RECETTE_NAVIGATEUR_CHANTIER_B_20260614.md`](./RAPPORT_RECETTE_NAVIGATEUR_CHANTIER_B_20260614.md) |

---

## Préparation base (Dev — 2026-06-08)

Jeu de données prêt sur `ckr-marketone-01` — détail : [`PREP_RECETTE_LOT6_3A_PROMO.md`](../../cadrage2/PREP_RECETTE_LOT6_3A_PROMO.md)

| Rôle | Produit recette | Attendu porte promo |
|------|-----------------|---------------------|
| Promo A | Maniocookies salés La Platine | Visible |
| Promo B | Crackers manioc Sainte-Anne | Visible |
| Hors promo | Pâtes de manioc Mayotte | **Absent** de `/shop?marketone_mode=promo` |
| P6 global | Item `3_global` id **41** | Inactif par défaut — activer en BO pour P6 |

```bash
# Rejouer la préparation si besoin
docker exec -i sandbox-odoo19-odoo-1 odoo shell -d ckr-marketone-01 --no-http \
  < odoo19-addons-dorevia/dorevia_ckreyol_marketone/scripts/prep_recette_lot6_3a_promo.py
```

**Ordre recette MOA** : P1 → N1/N2 → P2/P3 → P5/P8 → R1–R4 → P4 → P7 *(si multi-pricelist)*

**Réserves** : échec isolé lot 6.2 hors clôture 6.3a · 6.3b hors périmètre.

---

## Validation MOA — architecture + tests auto (2026-06-08)

| Élément | Verdict |
|---------|---------|
| Doctrine ADR-034 · C3.D | **GO** — aucun point bloquant |
| Tests `dorevia_marketone_lot6_3a_promo` | **18/18 OK** |
| Tests `dorevia_marketone_lot3` + `lot5` | **23/23 OK** |
| Réception MOA | [`RECEPTION_MOA_LOT6_3A_PROMO.md`](../../cadrage2/RECEPTION_MOA_LOT6_3A_PROMO.md) |

> **Recette navigateur MOA exécutée le 2026-06-08** : P1–P8 · N1–N3 · R1–R4 signés. P7 non applicable sur `ckr-marketone-01` : une seule pricelist active (`Default`, id 3).

## Signature MOA — navigateur (2026-06-08)

| Contrôle | Preuve recette | Verdict |
|----------|----------------|---------|
| P1 | `GET /promotions` → 301 `/shop?marketone_mode=promo` | **OK** |
| P2 | `/shop?marketone_mode=promo` → 200 · titre **Promotions** · Maniocookies + Crackers visibles · Pâtes de manioc Mayotte absente | **OK** |
| P3 | Prix grille et fiche cohérents, affichés par Odoo ; aucun recalcul JS Marketone constaté | **OK** |
| P4 | Items 39/40 expirés temporairement → 200 · message « Aucune promotion n'est active... » · grille vide | **OK** |
| P5 | Lien « Tous les produits » → `/shop` sans `marketone_mode` | **OK** |
| P6 | Item global 41 activé temporairement → catalogue complet visible ; état initial restauré ensuite | **OK** |
| P7 | Non applicable : une seule pricelist active sur la base recette | **S/O** |
| P8 | `/shop?marketone_mode=featured` et `/shop?marketone_mode=origin` → 200 | **OK** |
| N1–N3 | Header Promotions présent · aucun `/kits` · pas de chip porte dans filtre actif | **OK** |
| R1–R4 | `/shop`, facettes, images, panier/checkout smoke contrôlés | **OK** |

## Arbitrages MOA — recette navigateur 2026-06-14

| Sujet | Décision |
|-------|----------|
| **P4 / P6** | Acceptés **non rejoués** — manipulations BO couvertes 2026-06-08 |
| **N2** | Cohabitation chips Promotions + Kits · **OK release 6.3** |
| **Clôture** | [`RAPPORT_RECETTE_NAVIGATEUR_CHANTIER_B_20260614.md`](./RAPPORT_RECETTE_NAVIGATEUR_CHANTIER_B_20260614.md) |

---

## En-tête obligatoire (ADR-034)

**ADR-034 :** [`ARBITRAGE_ARCHITECTURE_CADRAGE2.md`](../../cadrage2/ARBITRAGE_ARCHITECTURE_CADRAGE2.md)

**Fonctionnalité Odoo native préservée :** Listes de prix · Promotions

**Mécanisme Odoo concerné :** `product.pricelist` · `product.pricelist.item` · règles de prix Odoo

**Non-régression référence boutique :** [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../REFERENCE_RECETTE_BOUTIQUE_MOA.md) — sections **B1 · B2 · B3 · B4 · B6 · B7**

---

## Prérequis recette BO

| Élément | Détail |
|---------|--------|
| **Pricelist site** | Pricelist utilisée par le visiteur public (partenaire public / site) |
| **Items promo** | ≥ 2 produits avec `product.pricelist.item` **actif** et **strictement réducteur** |
| **Hors promo** | ≥ 1 produit sans item réducteur actif |
| **Global promo** *(optionnel)* | 1 scénario item `applied_on=3_global` strictement réducteur |

---

## Grille — Porte Promotions

| # | Scénario | Action | Attendu | MOA |
|---|----------|--------|---------|-----|
| **P1** | Alias | `GET /promotions` | **301** → `/shop?marketone_mode=promo` | ☑ |
| **P2** | Grille promo | Ouvrir canonique | 200 · titre **Promotions** · produits éligibles uniquement | ☑ |
| **P3** | Prix affichés | Comparer fiche / grille | Prix = moteur Odoo · **pas** recalcul JS Marketone | ☑ |
| **P4** | État vide | Désactiver items promo test | 200 · message sobre · grille vide | ☑ |
| **P5** | Retour catalogue | Lien « Tous les produits » | `/shop` sans `marketone_mode` | ☑ |
| **P6** | Promo globale | Item `3_global` actif réducteur | Catalogue complet visible (pas de filtre produit) | ☑ |
| **P7** | Multi-pricelist | Changer pricelist visiteur (si activé) | Jeu promo = pricelist **courante** | ☑ S/O |
| **P8** | Portes existantes | `/shop?marketone_mode=featured` · origin | Non-régression 6.1 / 6.2 | ☑ |

---

## Navigation — Chip header (M5)

| # | Scénario | Action | Attendu | MOA |
|---|----------|--------|---------|-----|
| **N1** | Chip Promotions | Header site depuis `/shop` | Lien **Promotions** → `/promotions` | ☑ |
| **N2** | Cohabitation chips *(arbitrage MOA 2026-06-14)* | Header site | Chips **Promotions** + **Kits & Coffrets** cohabitants · **OK release 6.3** *(critère « pas de chip Kits » obsolète post-merge 6.3b)* | ☑ |
| **N3** | Chips filtres | Filtre sidebar + porte promo | **Pas** de chip porte dans barre filtres actifs (UX-1 G10) | ☑ |

---

## Non-régression globale

| # | Scénario | Référence | MOA |
|---|----------|-----------|-----|
| **R1** | Smoke `/shop` | REFERENCE § B1 | ☑ |
| **R2** | Sidebar facettes | REFERENCE § B3 | ☑ |
| **R3** | Tuiles / images | REFERENCE § B4 | ☑ |
| **R4** | Panier / checkout smoke | Lot 5 | ☑ |

---

## Tests automatisés

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d ckr-marketone-01 \
  --test-tags=dorevia_marketone_lot6_3a_promo \
  --stop-after-init --http-port=0
```

Non-régression :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d ckr-marketone-01 \
  --test-tags=dorevia_marketone_lot6_1_featured,dorevia_marketone_lot6_2_origin,dorevia_marketone_lot5 \
  --stop-after-init --http-port=0
```

---

## Note de livraison (phrase obligatoire)

> **Aucun moteur Odoo remplacé** — les promotions s’appuient sur `product.pricelist` / `product.pricelist.item` (pricelist courante visiteur). Marketone présente et filtre la grille `/shop` uniquement.

---

## Verdict MOA

| Date | Verdict | Commentaire |
|------|---------|-------------|
| 2026-06-08 | ☑ **GO recette architecture** · ☑ **GO recette navigateur** · ☑ **GO clôture** · ☐ NO GO | P1–P8 · N1–N3 · R1–R4 signés · P7 S/O car une seule pricelist active · état pricelist restauré |
