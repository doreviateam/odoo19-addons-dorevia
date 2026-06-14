# Rapport QA Dev — Reprise Marketone · 2026-06-14

| Champ | Valeur |
|-------|--------|
| **Module** | `dorevia_ckreyol_marketone` |
| **Objet** | Reprise post-crash Codex · QA Lot 6.3a Promotions · Lot 6.3b Kits & Coffrets · SEO portes `/shop` · sidebar collections · wishlist grille · nettoyage warnings Odoo 19 |
| **Base** | `ckr-marketone-01` |
| **Conteneur** | `sandbox-odoo19-odoo-1` |
| **URL** | http://localhost:18079 |
| **Date** | 2026-06-14 |
| **Exécuteur** | QA / Codex (reprise post-crash) |
| **Verdict** | **GO technique ciblé** |

```text
GO technique ciblé pour poursuivre.
Warnings Marketone actionnables nettoyés.
Tests ciblés verts.
Ne pas nettoyer le worktree globalement : trier et découper avant commit.
```

---

## Contexte incident

| Élément | Détail |
|---------|--------|
| Crash initial | Application Codex — **pas Odoo** |
| Signature | `EXC_BREAKPOINT` · thread `CrBrowserMain` · pile Chromium / Node / V8 |
| Contournement | Pas d'in-app browser · validation via Odoo HTTP / tests |
| Limite Codex | Écriture fichier rapport rejetée (quota usage) — rapport transmis via chat Dev |

---

## Correctifs appliqués

### `views/layout/header.xml`

- Ajout header chips `/promotions` et `/kits`.
- XPath conforme Odoo 19 : `hasclass('navbar-nav')`.

### `views/pages/shop_sidebar_collections.xml`

- Remplacement `contains(@class, 'marketone-shop-categories-accordion')` par `hasclass('marketone-shop-categories-accordion')`.

### `views/pages/shop_product_tile_conversion.xml`

- Suppression des attributs QWeb inutilisés `t-nocache` / `t-nocache-product_template_id`.
- Le calcul `product._is_in_wishlist()` et le bouton `data-action="o_wishlist"` **restent présents**.

---

## QA exécutée

### Validation XML

```bash
find dorevia_ckreyol_marketone/views -name '*.xml' | sort | xargs xmllint --noout
```

**Résultat** : OK.

### Compilation Python

```bash
PYTHONPYCACHEPREFIX=/private/tmp/codex_pycache_marketone python3 -m py_compile ...
```

**Résultat** : OK.

### Anti-régression patterns warnings

```bash
rg -n "contains\(@class|t-nocache|t-nocache-product_template_id" dorevia_ckreyol_marketone/views
```

**Résultat** : aucune occurrence.

### Tests Odoo ciblés Lot 6.3 / SEO

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf -d ckr-marketone-01 \
  -u dorevia_ckreyol_marketone --test-enable \
  --test-tags=dorevia_marketone_lot6_3a_promo,dorevia_marketone_lot6_3b_pack,dorevia_marketone_seo_portes_shop \
  --stop-after-init --http-port=18080
```

| Métrique | Résultat |
|----------|----------|
| post-tests | 39 |
| failed | 0 |
| error(s) | 0 |

### Suite large (smoke + lots 2–6.3 + SEO + BO)

```bash
--test-tags=dorevia_marketone_smoke,dorevia_marketone_lot2,dorevia_marketone_lot3,dorevia_marketone_lot4,dorevia_marketone_lot5,dorevia_marketone_lot6_3a_promo,dorevia_marketone_lot6_3b_pack,dorevia_marketone_seo_portes_shop,dorevia_marketone_bo
```

| Métrique | Résultat |
|----------|----------|
| post-tests | 91 |
| failed | 0 |
| error(s) | **1** |

**Analyse** : timeout isolé `Read timed out (12s)` sur `TestMarketoneLot3Shop.test_shop_has_wsale_structure`. `/shop` a répondu en **200** juste après. Rerun Lot 3 isolé vert.

### Rerun Lot 3

```bash
--test-tags=dorevia_marketone_lot3
```

| Métrique | Résultat |
|----------|----------|
| post-tests | 11 |
| failed | 0 |
| error(s) | 0 |

### QA finale après nettoyage warnings

```bash
--test-tags=dorevia_marketone_shop_sidebar_collections,dorevia_marketone_shop_wishlist,dorevia_marketone_lot3,dorevia_marketone_lot6_3a_promo,dorevia_marketone_lot6_3b_pack,dorevia_marketone_seo_portes_shop
```

| Métrique | Résultat |
|----------|----------|
| post-tests | 72 |
| failed | 0 |
| error(s) | 0 |

---

## État fonctionnel validé

| Contrôle | Résultat |
|----------|----------|
| `/promotions` → 301 → `/shop?marketone_mode=promo` | OK |
| `/shop?marketone_mode=promo` | OK |
| Promo via `product.pricelist.item` | OK |
| `/kits` → 301 → `/shop?marketone_mode=pack` | OK |
| Pack via `pack_ok=True` | OK |
| Priorité `pack > promo > featured > origin` | OK |
| Header Promotions + Kits | OK |
| Sidebar collections | OK |
| Wishlist grille | OK |
| SEO canonical / noindex portes | OK |
| Panier / checkout smoke Lot 6.3 | OK |

---

## Points d'attention Dev

| # | Point | Consigne |
|---|-------|----------|
| 1 | Git | **Ne pas** faire de nettoyage Git global destructif |
| 2 | Worktree | Très sale · changements hors périmètre Marketone (notamment `dorevia_glc_analytics`) |
| 3 | Fichiers non suivis | Modèles `product_pricelist.py`, `website.py` · tests Lot 6.3 · vues `shop_promo.xml`, `shop_pack.xml` · SCSS promo/pack · scripts prep recette |
| 4 | Commits | Découper par périmètre : **6.3a** · **6.3b** · **SEO** · **BO** · **nettoyage warnings** |
| 5 | Avant commit | Relancer la QA finale (commande § QA finale ci-dessus) |
| 6 | Timeout `/shop` | Réserve performance sandbox — **pas anomalie fonctionnelle** |
| 7 | Warnings vendor | Incompatibles hors Marketone observés pendant `-u` · traiter infra si nécessaire |

---

## Fichiers Marketone encore non suivis (git status au 2026-06-14)

```text
models/product_pricelist.py
models/website.py
scripts/prep_recette_lot6_3a_promo.py
scripts/prep_recette_lot6_3b_pack.py
static/src/scss/_shop_pack.scss
static/src/scss/_shop_promo.scss
tests/marketone_gate_helpers.py
tests/test_marketone_lot6_3a_promo.py
tests/test_marketone_lot6_3b_pack.py
tests/test_marketone_product_form_bo.py
tests/test_marketone_seo_portes_shop.py
views/pages/shop_pack.xml
views/pages/shop_promo.xml
views/product_template_marketone_bo_views.xml
docs/cadrage2/ (dossier entier)
docs/recette/lots/RECETTE_MANUELLE_LOT6_3*.md
docs/recette/maintenance/
docs/tickets/ (plusieurs tickets Lot 6.3 / SEO / maintenance)
```

---

## Documents liés

| Document | Rôle |
|----------|------|
| [`RECEPTION_MOA_LOT6_3A_PROMO.md`](../../cadrage2/RECEPTION_MOA_LOT6_3A_PROMO.md) | Clôture MOA 6.3a |
| [`RECEPTION_MOA_LOT6_3B_PACK.md`](../../cadrage2/RECEPTION_MOA_LOT6_3B_PACK.md) | Réception 6.3b |
| [`DECISION_MOA_SEO_PORTES_SHOP.md`](../../cadrage2/DECISION_MOA_SEO_PORTES_SHOP.md) | Doctrine SEO portes |
| [`RECETTE_MANUELLE_LOT6_3A_PROMO.md`](../RECETTE_MANUELLE_LOT6_3A_PROMO.md) | Recette navigateur promo |
| [`RECETTE_MANUELLE_LOT6_3B_PACK.md`](../RECETTE_MANUELLE_LOT6_3B_PACK.md) | Recette navigateur pack |
| [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../REFERENCE_RECETTE_BOUTIQUE_MOA.md) | Invariants boutique |

---

*Rapport QA Dev — reprise post-crash Codex · transmis MOA → Dev · 2026-06-14.*
