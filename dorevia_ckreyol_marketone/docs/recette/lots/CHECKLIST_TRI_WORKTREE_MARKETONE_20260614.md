# Checklist tri worktree — Marketone · 2026-06-14

> Reprise post-crash Codex · base `ckr-marketone-01` · **ne pas nettoyer Git globalement**.

| Légende | Signification |
|---------|---------------|
| ✅ | Inclure dans commit Marketone |
| ⛔ | **Exclure** — hors périmètre / autre module |
| 📦 | Commit cible (numéro) |
| ⏸ | Laisser unstaged — décision MOA / autre chantier |

---

## ⛔ Hors périmètre — ne pas committer ici

| Chemin | Action |
|--------|--------|
| `dorevia_glc_analytics/**` | ⛔ **Exclure** — chantier GLC séparé |
| `dorevia_ck_theme/**` | ⏸ Module CK maquette — autre GO MOA |
| `dorevia_ck_marketone/**` | ⏸ Module CK contenu — autre GO MOA |
| `dorevia_ck_marketone_content/**` | ⏸ Idem |

---

## 📦 Commit 1 — Documentation cadrage2 + recettes + tickets

| Fichier | Statut git | 📦 |
|---------|------------|-----|
| `docs/cadrage2/**` | untracked | 1 |
| `docs/recette/lots/RECETTE_MANUELLE_LOT6_3.md` | untracked | 1 |
| `docs/recette/lots/RECETTE_MANUELLE_LOT6_3A_PROMO.md` | untracked | 1 |
| `docs/recette/lots/RECETTE_MANUELLE_LOT6_3B_PACK.md` | untracked | 1 |
| `docs/recette/lots/RAPPORT_QA_DEV_REPRISE_MARKETONE_20260614.md` | untracked | 1 |
| `docs/recette/maintenance/**` | untracked | 1 |
| `docs/tickets/boutique/TICKET_MARKETONE_SEO_PORTES_SHOP.md` | untracked | 1 |
| `docs/tickets/lots/TICKET_MARKETONE_LOT6_3A_PORTE_PROMO_EXEC.md` | untracked | 1 |
| `docs/tickets/lots/TICKET_MARKETONE_LOT6_3B_PORTE_PACK_EXEC.md` | untracked | 1 |
| `docs/tickets/maintenance/**` | untracked | 1 |
| `docs/README.md` | modified | 1 |
| `docs/cadrage/CONTRACTS.md` | modified | 1 |
| `docs/cadrage/DECISIONS.md` | modified | 1 |
| `docs/recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md` | modified | 1 |

---

## 📦 Commit 2 — BO recadrage produit

| Fichier | Statut git | 📦 |
|---------|------------|-----|
| `views/product_template_marketone_bo_views.xml` | untracked | 2 |
| `tests/test_marketone_product_form_bo.py` | untracked | 2 |
| `models/product_template.py` | modified | 2 |
| `models/product_template_shop_tile.py` | modified | 2 |
| `views/marketone_shop_collection_views.xml` | modified | 2 |
| `views/product_template_shop_tile_views.xml` | **deleted** | 2 |

---

## 📦 Commit 3 — Lot 6.3a Promotions

| Fichier | Statut git | 📦 |
|---------|------------|-----|
| `views/pages/shop_promo.xml` | untracked | 3 |
| `static/src/scss/_shop_promo.scss` | untracked | 3 |
| `models/product_pricelist.py` | untracked | 3 |
| `tests/test_marketone_lot6_3a_promo.py` | untracked | 3 |
| `scripts/prep_recette_lot6_3a_promo.py` | untracked | 3 |

---

## 📦 Commit 4 — Lot 6.3b Kits & Coffrets

| Fichier | Statut git | 📦 |
|---------|------------|-----|
| `views/pages/shop_pack.xml` | untracked | 4 |
| `static/src/scss/_shop_pack.scss` | untracked | 4 |
| `tests/test_marketone_lot6_3b_pack.py` | untracked | 4 |
| `scripts/prep_recette_lot6_3b_pack.py` | untracked | 4 |

---

## 📦 Commit 5 — SEO portes `/shop`

| Fichier | Statut git | 📦 |
|---------|------------|-----|
| `models/website.py` | untracked | 5 |
| `tests/test_marketone_seo_portes_shop.py` | untracked | 5 |
| `views/layout/website_layout.xml` | modified | 5 |
| `views/pages/shop_featured.xml` | modified | 5 |
| `views/pages/shop_grid_title.xml` | modified | 5 |
| `views/pages/shop_origin.xml` | modified | 5 |

---

## 📦 Commit 6 — Nettoyage warnings Odoo 19

| Fichier | Statut git | 📦 |
|---------|------------|-----|
| `views/pages/shop_sidebar_collections.xml` | modified | 6 |
| `views/pages/shop_product_tile_conversion.xml` | modified | 6 |

> Vérifier post-commit : `rg 'contains\(@class\|t-nocache' views/` → 0 occurrence.

---

## 📦 Commit 7 — Intégration contrôleur, header, manifest et gates

| Fichier | Statut git | 📦 | Note |
|---------|------------|-----|------|
| `controllers/website_sale.py` | modified | 7 | promo + pack + SEO + filtres |
| `views/layout/header.xml` | modified | 7 | chips Promotions/Kits + xpath Odoo 19 |
| `static/src/scss/_header.scss` | modified | 7 | styles chips |
| `__manifest__.py` | modified | 7 | `19.0.19.0.1` · depends `product_pack` |
| `models/__init__.py` | modified | 7 | pricelist + website |
| `tests/__init__.py` | modified | 7 | imports lot6.3 + seo + bo |
| `tests/marketone_gate_helpers.py` | untracked | 7 | helpers gates |
| `tests/test_marketone_lot2_home.py` | modified | 7 | alignement gates |
| `tests/test_marketone_lot3_shop.py` | modified | 7 | alignement gates |
| `tests/test_marketone_lot4_product.py` | modified | 7 | alignement gates |
| `tests/test_marketone_lot5_cart_checkout.py` | modified | 7 | alignement gates |

> **Commit 7 obligatoire** pour module installable · tests verts uniquement après ce commit.

---

## QA avant push

```bash
# Depuis odoo19-addons-dorevia/
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf -d ckr-marketone-01 \
  -u dorevia_ckreyol_marketone --test-enable --stop-after-init --http-port=18080 \
  --test-tags=dorevia_marketone_shop_sidebar_collections,dorevia_marketone_shop_wishlist,dorevia_marketone_lot3,dorevia_marketone_lot6_3a_promo,dorevia_marketone_lot6_3b_pack,dorevia_marketone_seo_portes_shop
```

Attendu : **72 post-tests · 0 failed · 0 error(s)**.

---

## Ordre d'exécution Git recommandé

```text
1 → docs
2 → BO
3 → 6.3a (fichiers neufs)
4 → 6.3b (fichiers neufs)
5 → SEO (fichiers neufs + vues layout/pages)
6 → warnings (2 vues)
7 → intégration (controller · manifest · header · tests)
```

---

*Checklist tri worktree — Marketone · 2026-06-14.*
