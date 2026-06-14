# Rapport QA proxy — Lot 6.3a Promotions · Chantier B · 2026-06-14

| Champ | Valeur |
|-------|--------|
| **Chantier** | **B — `dorevia_ckreyol_marketone`** · **Lot 6.3a uniquement** |
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079 |
| **Module** | **19.0.19.0.1** (post-merge PR #62 · commit `388e515`) |
| **Grille source** | [`RECETTE_MANUELLE_LOT6_3A_PROMO.md`](./RECETTE_MANUELLE_LOT6_3A_PROMO.md) |
| **Rôle** | QA temporaire · proxy · **ne clôt pas MOA** |
| **Exécuteur** | QA Cursor · 2026-06-14 |

```text
Périmètre strict Lot 6.3a — pas de clôture MOA · pas d'élargissement 6.3b/SEO.
Verdict MOA navigateur : en attente signature MOA.
```

---

## Synthèse proxy

| Nature | Verdict proxy |
|--------|---------------|
| Tests auto `dorevia_marketone_lot6_3a_promo` | ✅ **18/18** |
| Grille P1–P3 · P5 · P8 · N1 · N3 · R1 · R3 · R4 | ✅ **OK proxy** |
| P4 · P6 (manipulation pricelist BO) | ☐ **Non exécuté** — MOA / BO |
| P7 multi-pricelist | **S/O** (une pricelist active) |
| N2 (doc 2026-06-08) | ⚠️ **Écart doc vs code post-merge** — voir § Navigation |
| R2 sidebar (sélecteur Playwright) | ⚠️ **Faux négatif** — corrigé proxy DOM · voir § R2 |

**Recommandation QA → MOA** : base **favorable** pour recette navigateur 6.3a · compléter **P4 · P6** si MOA souhaite rejouer scénarios pricelist · **ne pas signer clôture** sur ce seul rapport.

---

## Tests automatisés

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf -d ckr-marketone-01 \
  --test-enable --stop-after-init --http-port=18084 \
  --test-tags=dorevia_marketone_lot6_3a_promo
```

| Métrique | Résultat |
|----------|----------|
| post-tests | **18** |
| failed | **0** |
| error(s) | **0** |
| Date | 2026-06-14 10:08 UTC |

---

## Grille Porte Promotions (P1–P8)

| # | Scénario | Proxy | Preuve / note | MOA |
|---|----------|-------|---------------|-----|
| **P1** | Alias `/promotions` | ✅ | HTTP **301** · `Location: /shop?marketone_mode=promo` | ☐ |
| **P2** | Grille promo | ✅ | HTTP 200 · intro `.marketone-shop-promo-intro` · titre Promotions · **Maniocookies** + **Crackers** présents · **Pâtes de manioc Mayotte absente** | ☐ |
| **P3** | Prix Odoo natif | ✅ | Fiche promo : prix `4,90 €` · pas script recalcul JS Marketone | ☐ |
| **P4** | État vide | ☐ | **Non exécuté** — requiert désactivation items BO · prep [`PREP_RECETTE_LOT6_3A_PROMO.md`](../../cadrage2/PREP_RECETTE_LOT6_3A_PROMO.md) | ☐ |
| **P5** | Tous les produits | ✅ | Lien `href="/shop"` sans `marketone_mode` | ☐ |
| **P6** | Promo globale | ☐ | **Non exécuté** — activation item `3_global` id BO · MOA | ☐ |
| **P7** | Multi-pricelist | **S/O** | Une pricelist visiteur (`Default`) | ☐ |
| **P8** | Portes featured / origin | ✅ | HTTP 200 `/shop?marketone_mode=featured` et `origin` | ☐ |

### Détail P2 — produits recette

| Produit | `/shop?marketone_mode=promo` | `/shop` (catalogue) |
|---------|------------------------------|---------------------|
| Maniocookies salés La Platine | ✅ présent | ✅ |
| Crackers manioc Sainte-Anne | ✅ présent | ✅ |
| Pâtes de manioc Mayotte (hors promo) | ✅ **absent** | ✅ présent |

Liens produits distincts sur grille promo : **2** (cohérent jeu promo A/B).

---

## Navigation — Chip header (N1–N3)

| # | Scénario | Proxy | Preuve / note | MOA |
|---|----------|-------|---------------|-----|
| **N1** | Chip Promotions | ✅ | Header · `href="/promotions"` · libellé Promotions | ☐ |
| **N2** | Pas de chip Kits *(doc 2026-06-08)* | ⚠️ | **Chip Kits & Coffrets présent** post-merge **19.0.19.0.1** (Lot 6.3b livré même PR). Doc recette datée **17.0.0** · critère N2 **obsolète** sur branche actuelle — **à arbitrer MOA** (non bloquant 6.3a promo si MOA acte cohabitation chips) | ☐ |
| **N3** | Pas chip porte dans filtres actifs | ✅ | Pas de chip « Promotions » dans barre filtres UX-1 | ☐ |

---

## Non-régression (R1–R4)

| # | Scénario | Proxy | Preuve / note | MOA |
|---|----------|-------|---------------|-----|
| **R1** | Smoke `/shop` | ✅ | HTTP 200 | ☐ |
| **R2** | Sidebar / facettes | ✅ | DOM `/shop` : `marketone-shop-categories` · `accordion` · `o_wsale_products_main_row` présents *(Playwright initial : sélecteur `.marketone-shop-sidebar` inexistant — faux négatif)* | ☐ |
| **R3** | Tuiles / images | ✅ | 48 tuiles · 24 images sur `/shop` | ☐ |
| **R4** | Panier smoke | ✅ | `/shop/cart` HTTP 200 | ☐ |

Checkout complet : couvert par tests auto `test_cart_checkout_regression` (18/18).

---

## ADR-034 — rappel

```text
Fonctionnalité Odoo native préservée : product.pricelist · product.pricelist.item
Marketone : présentation + filtre grille /shop?marketone_mode=promo uniquement
Aucun moteur Odoo remplacé
```

---

## Non exécuté / réserves

| Point | Traitement |
|-------|------------|
| P4 état vide pricelist | MOA + BO ou replay prep + manipulation items |
| P6 promo globale | MOA + BO item `3_global` |
| P7 | S/O base recette |
| N2 vs Kits chip | Arbitrage MOA · doc 6.3a à actualiser post-merge 19.0.19.0.1 |
| Prix comparatif grille vs fiche multi-produits | Échantillon 1 fiche · MOA peut approfondir |
| Recette navigateur visuelle | MOA — chips · intro · empty state P4 |

---

## Verdict MOA — **clôturé · navigateur 2026-06-14**

| Date | Verdict proxy QA | Verdict MOA navigateur |
|------|------------------|------------------------|
| 2026-06-14 | ✅ Favorable · P4/P6 non exécutés | ✅ **GO clôture Chantier B · lot 6.3a validé** |
| 2026-06-14 | N2 doc vs chips Kits | ✅ **Arbitré OK release 6.3** — cohabitation chips validée |

```text
Arbitrage N2 (MOA 2026-06-14) : critère doc « pas de chip Kits » obsolète post-merge 6.3b.
  Chips Promotions + Kits & Coffrets cohabitants = OK release 6.3 complète · non bloquant 6.3a.

Doctrine P4/P6 (MOA 2026-06-14) : acceptés non rejoués — manipulations BO couvertes 2026-06-08.
  Pas de rejeu requis recette navigateur 2026-06-14.

Rapport clôture : RAPPORT_RECETTE_NAVIGATEUR_CHANTIER_B_20260614.md
```

---

## Gouvernance versionnement

| Décision MOA | Statut |
|--------------|--------|
| Clôture navigateur MOA | ✅ **Actée 2026-06-14** |
| Commit docs dédié | ☐ En attente acte MOA séparé |

**Aucun commit docs** sans acte MOA dédié.

---

## Documents liés

| Document | Rôle |
|----------|------|
| [`RECETTE_MANUELLE_LOT6_3A_PROMO.md`](./RECETTE_MANUELLE_LOT6_3A_PROMO.md) | Grille MOA |
| [`RAPPORT_RECETTE_NAVIGATEUR_CHANTIER_B_20260614.md`](./RAPPORT_RECETTE_NAVIGATEUR_CHANTIER_B_20260614.md) | Clôture navigateur |
| [`RAPPORT_QA_DEV_REPRISE_MARKETONE_20260614.md`](./RAPPORT_QA_DEV_REPRISE_MARKETONE_20260614.md) | Gate post-merge |
| [`CONFIRMATION_TECHNIQUE_PR62_20260614.md`](./CONFIRMATION_TECHNIQUE_PR62_20260614.md) | B1 merge |

**Hors périmètre** : Chantier A · A1 header · `dorevia_ck_marketone_01`.

---

*Rapport QA proxy Lot 6.3a · Chantier B · clôture navigateur MOA 2026-06-14.*
