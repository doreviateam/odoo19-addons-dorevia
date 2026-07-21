# Rapport recette navigateur — Chantier B · clôture MOA · 2026-06-14

| Champ | Valeur |
|-------|--------|
| **Chantier** | **B — `dorevia_ckreyol_marketone`** |
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079 |
| **Module** | **19.0.19.0.1** (post-merge PR #62 · commit `388e515`) |
| **Lots** | 6.3a Promotions · 6.3b Kits & Coffrets · SEO portes `/shop` |
| **Statut** | **Clôturé MOA — GO navigateur 2026-06-14** |

---

## Synthèse exécutive

| Contrôle | Résultat |
|----------|----------|
| Tests auto 6.3a | **18/18 OK** |
| Tests auto 6.3b | **13/13 OK** |
| Tests auto SEO | **8/8 OK** |
| **Total lots B** | **39/39 OK** |
| Recette navigateur proxy HTTP live | **56/56 OK** |
| Écarts bloquants | **Aucun** |
| Impact Chantier A / contenu légal | **Aucun** |

**Verdict MOA** : **GO clôture Chantier B navigateur** — 6.3a + 6.3b + SEO portes/shop.

---

## Périmètre validé

- Promotions (`/promotions` · `/shop?marketone_mode=promo`)
- Kits & Coffrets (`/kits` · `/shop?marketone_mode=pack`)
- SEO portes `/shop` (doctrine D1–D6)
- Alias 301 · canonical / noindex
- Navigation boutique · chips header
- Smoke panier / catalogue (R1–R4)

**Hors périmètre** (inchangé) : Chantier A · A1 header · A7 Git CK · lot contenu légal local · `sale_product_pack` explosion composants · sitemap XML custom.

---

## Arbitrages MOA actés

### N2 — Cohabitation chips Promotions + Kits

| Élément | Décision |
|---------|----------|
| Contexte | Critère doc 6.3a « pas de chip Kits » obsolète post-merge 6.3b |
| Arbitrage | **OK release 6.3** — chips Promotions + Kits & Coffrets cohabitants |
| Impact | Non bloquant lot 6.3a |

### P4 / P6 / K6 — Non rejoués

| ID | Scénario | Décision |
|----|----------|----------|
| **P4** | État vide pricelist | **Accepté non rejoué** — doctrine MOA 2026-06-08 |
| **P6** | Promo globale `3_global` | **Accepté non rejoué** — idem |
| **K6** | État vide `pack_ok` | **Accepté non rejoué** — idem |

Pas de rejeu BO requis dans la recette navigateur 2026-06-14.

---

## Lot 6.3a — Promotions

Grille source : [`RECETTE_MANUELLE_LOT6_3A_PROMO.md`](./RECETTE_MANUELLE_LOT6_3A_PROMO.md)  
Proxy détaillé : [`RAPPORT_QA_PROXY_LOT6_3A_20260614.md`](./RAPPORT_QA_PROXY_LOT6_3A_20260614.md)

| Zone | Verdict navigateur |
|------|-------------------|
| P1 · P2 · P3 · P5 · P8 | ✅ OK |
| P4 · P6 | ☐ Non rejoué · **accepté MOA** |
| P7 | S/O (une pricelist) |
| N1 · N3 | ✅ OK |
| N2 | ⚠️ → **arbitré OK release 6.3** |
| R1–R4 | ✅ OK |

---

## Lot 6.3b — Kits & Coffrets

Grille source : [`RECETTE_MANUELLE_LOT6_3B_PACK.md`](./RECETTE_MANUELLE_LOT6_3B_PACK.md)  
Proxy détaillé : [`RAPPORT_QA_PROXY_LOT6_3B_20260614.md`](./RAPPORT_QA_PROXY_LOT6_3B_20260614.md)

| Zone | Verdict navigateur |
|------|-------------------|
| K1–K5 · K7 · K8 | ✅ OK |
| K6 | ☐ Non rejoué · **accepté MOA** |
| N1–N3 | ✅ OK |
| R1–R4 | ✅ OK |

---

## SEO portes / shop

Doctrine : [`DECISION_MOA_SEO_PORTES_SHOP.md`](../../cadrage2/DECISION_MOA_SEO_PORTES_SHOP.md)  
Proxy détaillé : [`RAPPORT_QA_PROXY_SEO_PORTES_SHOP_20260614.md`](./RAPPORT_QA_PROXY_SEO_PORTES_SHOP_20260614.md)

| Zone | Verdict navigateur |
|------|-------------------|
| D1 alias 301 (4/4) | ✅ OK |
| D6/T0 `/shop` nu | ✅ OK |
| D2/T2 portes simples | ✅ OK |
| D3/T3 origines facettées | ✅ OK |
| D3 multi-slugs | ✅ OK |
| D4/T4 bruit order/search | ✅ OK |
| D5/T5 pagination | ✅ OK |
| Slug invalide → `/shop` | ✅ OK |

---

## Observations techniques (non bloquantes)

| Sujet | Note |
|-------|------|
| Canonical HTML `&amp;` | Comportement Odoo normal |
| D1 vérification 301 | Utiliser `curl -I` sans follow |
| Slugs origine sidebar | Absents du DOM porte origin seule — contrôle via URLs directes |
| R2 Playwright | Sélecteur `.marketone-shop-sidebar` inexistant — sidebar OK via `marketone-shop-categories` |

---

## Gouvernance versionnement

| Décision MOA | Statut |
|--------------|--------|
| Clôture documentaire préparée | ✅ 2026-06-14 |
| **Commit / PR docs** | ☐ **En attente acte MOA dédié** |
| Fichiers concernés | Rapport clôture · mises à jour proxy · grilles recette 6.3a N2 |

**Aucun commit** sans acte MOA explicite.

---

## Acte MOA — clôture

```text
Décision MOA : GO clôture Chantier B navigateur — 6.3a + 6.3b + SEO portes/shop
Arbitrages : N2 OK release 6.3 · P4/P6/K6 acceptés non rejoués
Validé par : MOA CK · 2026-06-14
```

---

*Rapport recette navigateur Chantier B · clôture MOA · 2026-06-14.*
