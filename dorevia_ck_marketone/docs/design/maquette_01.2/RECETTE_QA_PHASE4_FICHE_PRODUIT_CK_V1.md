# Recette QA — Phase 4 · Fiche produit · CK V1.2.x

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Instance** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **GO MOA** | [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) **§5quinquies — ACTÉ 2026-06-13** |
| **Prérequis** | Phase 3 clôturée · gate [`ck_phase3_ci.sh`](./scripts/ck_phase3_ci.sh) OK |
| **Statut** | **✅ Clôturée OK partiel MOA · Phase 5 suspendue** |
| **Module** | `dorevia_ck_theme` **19.0.1.2.0** |

> Header HTTP `X-Odoo-Database: dorevia_ck_marketone_01` requis.

---

## 1. Périmètre Phase 4 (strict) — conforme

| # | Livrable | Statut Dev |
|---|----------|------------|
| 4.1 | Fiche produit native `/shop/{slug}-{id}` | ☑ |
| 4.2 | Galerie · titre · prix · qty · panier | ☑ natif CE |
| 4.3 | Description enrichie · origine · conservation | ☑ BO bootstrap |
| 4.4 | Signal B2B `/professionnels` | ☑ `ck-product-pro-signal` |
| 4.5 | Lien producteur | ☑ **Différé** (404 CMS — gate M1) |
| 4.6 | Chips catégorie | ☑ `.ck-chip` |

**Exclus respectés** : pas panier/checkout custom · pas cross-sell · home/shop/header intacts.

---

## 2. Triptyque QA — résultats Dev

### Gate portable · **OK Dev 2026-06-13** · contrôle MOA sans relance gate complet

```text
ck_phase4_ci.sh        : OK Dev (upgrade + restart + 12/12 tests + smoke)
Contrôle MOA           : recette/gouvernance · tests/vues · fiche live · Playwright UX
Odoo test-tags         : 12 / 12 OK (dorevia_ck_theme_phase4)
Smoke curl             : fiche · cart · shop · pro · home OK
Playwright UX          : desktop 1280 · mobile 390/390 sans overflow (hors gate)
Portabilité gate       : CK_CI_PRODUCT_PATH optionnel · sinon 1er produit publié sur /shop
```

```bash
./scripts/ck_phase4_ci.sh
docker exec sandbox-odoo19-odoo-1 odoo -d dorevia_ck_marketone_01 \
  --test-enable --stop-after-init --test-tags=dorevia_ck_theme_phase4 --http-port=8074
node scripts/ck_phase4_desktop1280.mjs
node scripts/ck_phase4_mobile390.mjs
```

---

## 3. Contrôles fiche produit

| Contrôle | Attendu | Résultat |
|----------|---------|----------|
| HTTP 200 | `/shop/confiture-de-goyave-3` | ☑ |
| Scope | `ck-product-page` | ☑ |
| Galerie | Images produit | ☑ |
| Titre | Nom produit BO | ☑ |
| Prix | TTC visible | ☑ |
| Quantité | Input qty | ☑ |
| CTA panier | `#add_to_cart` | ☑ |
| Description | `ck-product-enrich` | ☑ |
| Signal Pro | `ck-product-pro-signal` | ☑ |
| Lien producteur | Absent si pas CMS | ☑ absent |

---

## 4. Smoke curl

| Route | Résultat |
|-------|----------|
| Fiche produit | ☑ 200 |
| `/shop/cart` | ☑ 200 |
| `/shop` | ☑ 200 · Phase 3 intact |
| `/professionnels` | ☑ 200 |
| `/` | ☑ 200 · vedettes SSR |

---

## 5. Playwright UX (hors gate)

| Contrôle | Résultat |
|----------|----------|
| Desktop 1280 | ☑ prix · CTA · description · chips |
| Mobile 390 | ☑ 390/390 · pas overflow fiche |
| Non-régression shop/home | ☑ |

---

## 6. Non-régression Phase 1 · 2 · 3

| Phase | Résultat |
|-------|----------|
| Phase 1 header/footer | ☑ |
| Phase 2 home SSR 5 cartes | ☑ |
| Phase 3 shop intro | ☑ |

---

## 7. Verdict QA

| Champ | Valeur |
|-------|--------|
| **Verdict Phase 4** | ☐ OK · ☑ **OK partiel** · ☐ KO |
| **GO Phase 5** | ☑ **Suspendu** |
| **Validé par** | **MOA CK** |
| **Date** | **2026-06-13** |

**Motif OK partiel** : livraison conforme §5quinquies · enrichissements BO bootstrap (pas contenu métier final) · lien producteur différé (M1).

**Contrôle MOA** : recette/gouvernance · inspection tests/vues · HTTP fiche · Playwright desktop 1280 · mobile 390 — gate complet non relancé (upgrade + restart).

---

## 8. Documents liés

| Document | Rôle |
|----------|------|
| [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) | §5quinquies |
| [`RECETTE_QA_PHASE3_SHOP_CK_V1.md`](./RECETTE_QA_PHASE3_SHOP_CK_V1.md) | Prérequis |

---

*Recette QA Phase 4 — clôturée OK partiel MOA · Phase 5 suspendue · 2026-06-13.*
