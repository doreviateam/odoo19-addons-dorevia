# Rapport QA proxy — Lot 6.3b Kits & Coffrets · Chantier B · 2026-06-14

| Champ | Valeur |
|-------|--------|
| **Chantier** | **B — `dorevia_ckreyol_marketone`** · **Lot 6.3b uniquement** |
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079 |
| **Module** | **19.0.19.0.1** (post-merge PR #62 · commit `388e515`) |
| **Grille source** | [`RECETTE_MANUELLE_LOT6_3B_PACK.md`](./RECETTE_MANUELLE_LOT6_3B_PACK.md) |
| **Rôle** | QA temporaire · proxy · **ne clôt pas MOA** |
| **Exécuteur** | QA Cursor · 2026-06-14 |

```text
Périmètre strict Lot 6.3b — pas de clôture MOA · pas d'élargissement SEO.
Contexte MOA 6.3a : base favorable · P4/P6 non rejoués · N2 doc arbitré (chips cohabitants OK release 6.3).
```

---

## Synthèse proxy

| Nature | Verdict proxy |
|--------|---------------|
| Tests auto `dorevia_marketone_lot6_3b_pack` | ✅ **13/13** |
| Grille K1–K5 · K7–K8 · N1–N3 · R1–R4 | ✅ **OK proxy** |
| K6 état vide (`pack_ok` BO) | ☐ **Non exécuté** — MOA · même doctrine que P4/P6 (6.3a) |
| Priorité pack > promo (K7) | ✅ |

**Recommandation QA → MOA** : base **favorable** pour recette navigateur 6.3b · **K6 non rejoué** sauf anomalie · **ne pas clôturer** sur ce rapport seul.

---

## Tests automatisés

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf -d ckr-marketone-01 \
  --test-enable --stop-after-init --http-port=18085 \
  --test-tags=dorevia_marketone_lot6_3b_pack
```

| Métrique | Résultat |
|----------|----------|
| post-tests | **13** |
| failed | **0** |
| error(s) | **0** |
| Date | 2026-06-14 10:13 UTC |

---

## Grille Porte Kits & Coffrets (K1–K8)

| # | Scénario | Proxy | Preuve / note | MOA |
|---|----------|-------|---------------|-----|
| **K1** | Alias `/kits` | ✅ | HTTP **301** · `Location: /shop?marketone_mode=pack` | ☐ |
| **K2** | Grille pack | ✅ | HTTP 200 · intro `.marketone-shop-pack-intro` · **Kits & Coffrets** · Maniocookies + Crackers | ☐ |
| **K3** | Témoin unitaire | ✅ | Pâtes de manioc Mayotte : **présente** `/shop` · **absente** porte pack | ☐ |
| **K4** | Prix Odoo | ✅ | Fiche pack : `4,90 €` · pas recalcul JS Marketone | ☐ |
| **K5** | Tous les produits | ✅ | `href="/shop"` sans `marketone_mode` | ☐ |
| **K6** | État vide | ☐ | **Non exécuté** — désactivation `pack_ok` BO · MOA acte : ne pas rejouer sauf anomalie | ☐ |
| **K7** | Priorité pack > promo | ✅ | `?marketone_mode=pack&marketone_mode=promo` → intro pack · **pas** intro promo | ☐ |
| **K8** | Portes promo / featured / origin | ✅ | HTTP 200 · promo intro présente sur mode promo | ☐ |

### Détail K2 — produits recette

| Produit | ID tmpl (prep doc) | Porte pack | Catalogue `/shop` |
|---------|-------------------|------------|-------------------|
| Maniocookies salés La Platine | 7 | ✅ `/shop/maniocookies-sales-la-platine-7` | ✅ |
| Crackers manioc Sainte-Anne | 8 | ✅ `/shop/crackers-manioc-sainte-anne-8` | ✅ |
| Pâtes de manioc Mayotte | 9 | ✅ **absent** | ✅ |

---

## Navigation — Chips header (N1–N3)

| # | Scénario | Proxy | Preuve / note | MOA |
|---|----------|-------|---------------|-----|
| **N1** | Chip Kits & Coffrets | ✅ | Header · `href="/kits"` | ☐ |
| **N2** | Chip Promotions conservé | ✅ | Header · `href="/promotions"` · cohérent release 6.3 complète | ☐ |
| **N3** | Pas chip porte dans filtres | ✅ | Pas de chip kit/coffret dans filtres actifs UX-1 | ☐ |

---

## Non-régression (R1–R4)

| # | Scénario | Proxy | Preuve / note | MOA |
|---|----------|-------|---------------|-----|
| **R1** | Smoke `/shop` | ✅ | HTTP 200 | ☐ |
| **R2** | Sidebar / facettes | ✅ | `marketone-shop-categories` présent | ☐ |
| **R3** | Tuiles / images | ✅ | 48 tuiles · 24 images | ☐ |
| **R4** | Panier smoke | ✅ | `/shop/cart` HTTP 200 | ☐ |

Checkout pack : couvert tests auto `test_cart_checkout_regression` (13/13).

---

## ADR-034 / ADR-035 — rappel

```text
product.template.pack_ok · product_pack · product.pack.line
Prix = website_sale / pricelist Odoo
Marketone : filtre grille /shop?marketone_mode=pack uniquement
sale_product_pack / explosion composants : hors v1 · non recetté 6.3b
```

---

## Réserves MOA (inchangées doc)

| Sujet | Traitement |
|-------|------------|
| K6 état vide | Non exécuté proxy · MOA : ne pas rejouer sauf anomalie navigateur |
| `sale_product_pack` OCA | Hors v1 |
| Explosion composants vente/stock | Non recettée 6.3b |
| SEO canonical / noindex | **Lot séparé** — proxy SEO en cours · [`RAPPORT_QA_PROXY_SEO_PORTES_SHOP_20260614.md`](./RAPPORT_QA_PROXY_SEO_PORTES_SHOP_20260614.md) |

---

## Verdict MOA — **clôturé · navigateur 2026-06-14**

| Date | Verdict proxy QA | Verdict MOA navigateur |
|------|------------------|------------------------|
| 2026-06-14 | ✅ **Favorable · K6 non exécuté** | ✅ **GO clôture Chantier B · lot 6.3b validé** |

**Doctrine K6 (MOA 2026-06-14)** : accepté non rejoué — manipulation BO `pack_ok` couverte 2026-06-08. Pas de rejeu requis recette navigateur 2026-06-14.

```text
Rapport clôture : RAPPORT_RECETTE_NAVIGATEUR_CHANTIER_B_20260614.md
Chips Promotions + Kits : arbitrage N2 OK release 6.3 (rapport 6.3a).
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
| [`RECETTE_MANUELLE_LOT6_3B_PACK.md`](./RECETTE_MANUELLE_LOT6_3B_PACK.md) | Grille MOA |
| [`RAPPORT_RECETTE_NAVIGATEUR_CHANTIER_B_20260614.md`](./RAPPORT_RECETTE_NAVIGATEUR_CHANTIER_B_20260614.md) | Clôture navigateur |
| [`RAPPORT_QA_PROXY_LOT6_3A_20260614.md`](./RAPPORT_QA_PROXY_LOT6_3A_20260614.md) | Proxy 6.3a · verdict intermédiaire MOA favorable |
| [`DECISION_MOA_LOT6_3B_KITS_COFFRETS.md`](../../cadrage2/DECISION_MOA_LOT6_3B_KITS_COFFRETS.md) | Doctrine pack |

**Hors périmètre** : Chantier A · A1 header · clôture MOA · proxy SEO livré (verdict intermédiaire MOA acté).

---

*Rapport QA proxy Lot 6.3b · Chantier B · clôture navigateur MOA 2026-06-14.*
