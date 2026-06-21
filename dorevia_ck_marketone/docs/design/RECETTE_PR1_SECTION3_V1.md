# Recette PR-1 — Durcissements `dorevia_ck_marketone_content` · V1

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` · C-Kreyol / CK |
| **Lot** | **PR-1** — durcissements QA (L1 · M2 · M4 · M1) |
| **Module** | `dorevia_ck_marketone_content` **19.0.1.21.16** (+ `dorevia_ck_theme` à jour) |
| **Instance** | `dorevia_ck_marketone_01` · http://localhost:18079 |
| **Date** | 2026-06-17 |
| **Exécuteur** | Dev / QA |
| **Verdict** | **GO avec réserves — mergeable** |
| **Source QA** | [`RAPPORT_QA_CODE_DOREVIA_CK_MARKETONE_CONTENT_20260617.docx`](./RAPPORT_QA_CODE_DOREVIA_CK_MARKETONE_CONTENT_20260617.docx) |

```text
PR-1 = durcissements sûrs issus du rapport QA content.
L1 sanitization couleurs ruban · M2 footer légal robuste · M4 doc SQL · M1 scope refresh vedettes.
H1/H2/H3 hors périmètre (PR-2/3/4).
```

---

## 1. Périmètre PR-1

| ID | Correctif | Fichier |
|----|-----------|---------|
| **L1** | `_safe_css_color()` — filtre `bg_color`/`text_color` du ruban avant inline style | `home_featured.py` |
| **M2** | Footer légal robuste — repli + `_logger.warning`, plus d'échec silencieux | `hooks.py` |
| **M4** | Docstring SQL direct (`_featured_label_parts_from_sql`) | `home_featured.py` |
| **M1** | `_ck_touches_featured()` — refresh vedettes limité à la curation active | `models/product_template.py` |

---

## 2. Upgrade

| Étape | Résultat |
|-------|----------|
| `-u dorevia_ck_marketone_content,dorevia_ck_theme --stop-after-init` | ✅ Chargement sans erreur bloquante |

---

## 3. Tests automatisés Odoo

| Lot | Tag | Résultat |
|-----|-----|----------|
| Section 3 + curation + lot 1 + catalogue | `dorevia_ck_marketone_home_section3`, `…_curation`, `…_home_lot1`, `…_catalog_manioc` | ✅ **44/44** — 0 failed · 0 error |
| Mentions légales / footer (M2) | `dorevia_ck_marketone_legal` | ✅ **8/8** |

**Réserves tests :**

- `test_ck_catalog_manioc_variants` **skipped** (bootstrap catalogue vedettes MOA impossible) — hors périmètre PR-1 strict, à surveiller sur la base recette.
- Log non bloquant pendant les tests HTTP : `ERROR: cannot execute UPDATE in a read-only transaction` (écriture `ir_ui_view` pendant une requête en lecture). **N'a pas fait échouer la suite.** → manifestation de **H2** (auto-réparation home en `_pre_dispatch`), à résoudre en PR-3.

---

## 4. Contrôles navigateur (desktop / mobile)

| Script | Viewport | Verdict |
|--------|----------|---------|
| `ck_section3_post_merge_recette.mjs` | 1280 + 390 | ✅ OK — 3 cartes, pas d'overflow, ordre hero → réassurance → vedettes |
| `ck_hero_slide_editor_recette.mjs` | 1440 (builder) | ✅ GO (2ᵉ exécution — voir réserve flaky) |
| `ck_s4_univers_editor_recette.mjs` | 1440 (builder) | ✅ GO |
| `ck_lot1_home_hero_qa.mjs` | 1280 + 390 | ✅ OK — critères clés validés |

**Section 3 — métriques clés :** 3 cartes (Confiture + 2 Manio) · `overflow: false` · `noNativeCarousel: true`.
Captures : `captures/recette_section3_post_merge/section3_odoo_1280.png` · `section3_odoo_390.png`.

---

## 5. Grille manuelle PR-1

| ID | Contrôle | Résultat |
|----|----------|----------|
| **L1** | `_safe_css_color()` filtre une valeur malveillante ; hex/rgba acceptés | ✅ `L1_ok: true` |
| **M2** | Footer `/` et `/shop` : `/legal`, `/privacy`, `/terms#cgv` présents | ✅ (curl + 8 tests HTTP) |
| **M1** | `write` hors « Coups de cœur » → arch home inchangée ; dans la catégorie → rebuild | ✅ (hors : Galettes de manioc · dedans : Confiture de goyave) |

---

## 6. Non-régression sections déjà validées

| Section | Statut |
|---------|--------|
| Hero carousel (builder) | ✅ GO après rejeu isolé |
| S4 univers (builder) | ✅ GO |
| Lot 1 hero (public 1280/390) | ✅ OK |
| Section 3 vedettes (public) | ✅ OK |

**Réserve opérationnelle :** après recettes Playwright **parallèles**, la home a temporairement affiché 2 slides hero (au lieu de 3). Restauration via `bootstrap_home_hero(env)` → 3 slides, 3 `product-card-labels`. Dérive de session recette (auto-réparation concurrente), pas un défaut PR-1 → intégrer `bootstrap_home_hero` + `refresh_home_featured_products` en fin de grille.

---

## 7. Synthèse par livrable

| Livrable | Verdict |
|----------|---------|
| L1 — sanitization couleurs ruban | ✅ GO |
| M2 — footer légal + log warning fallback | ✅ GO |
| M4 — docstring SQL labels | ✅ GO (couvert par tests section 3) |
| M1 — `_ck_touches_featured()` scope curation | ✅ GO |

---

## 8. Réserves (non bloquantes pour merge PR-1)

1. **Hero builder flaky** — 1er lancement en parallèle → timeout iframe (NO GO) ; rejeu isolé → GO. À jouer en séquentiel.
2. **Tag tests légaux** — utiliser `dorevia_ck_marketone_legal` dans la doc recette (pas `dorevia_ck_mentions_legales`).
3. **`catalog_manioc` skipped** sur cette base.
4. **Dérive arch home** pendant recettes Playwright — prévoir `bootstrap_home_hero` + `refresh_home_featured_products` en fin de grille.
5. **Écart M1 mode repli** (relevé QA, **non couvert par cette recette**) — le guard `_ck_touches_featured()` suspend le refresh si la catégorie « Coups de cœur » existe mais est **vide** (sélection auto). Sur cette instance la curation est active avec produits → comportement correct. Correctif 1-ligne (`if featured and featured.product_tmpl_ids:`) **acté en tête de PR-2** avec son test (catégorie vide → rebuild).

---

## 9. Conclusion

```text
PR-1 est mergeable sur la base de cette recette.
GO avec réserves — toutes non bloquantes.
```

---

## 10. Suite

| # | Action | Statut |
|---|--------|--------|
| 1 | Merge PR-1 (L1 · M2 · M4 · M1) | ✅ Recette GO |
| 2 | Correctif M1 mode repli + test | ⏩ **En tête de PR-2** |
| 3 | PR-2 — guard empreinte CMS + `home_arch.py` (B1) + migration freeze | ⏸ Draft à valider avant écriture |
| 4 | PR-3 — H2 (sortir l'écriture du GET ; lève le log read-only transaction) | ⏸ |
| 5 | PR-4 — H1 (remplacement mock HTTP) + tests prix | ⏸ |

**Arbitrages PR-2 confirmés MOA :** Home **B1** (pas de guard empreinte home) · guard empreinte **pages CMS uniquement** · **migration freeze** obligatoire (pose des empreintes sans `view.write`) · helper commun **`home_arch.py`** (pas d'import depuis `home_featured`).

---

*Recette PR-1 · `dorevia_ck_marketone_content` · GO avec réserves · 2026-06-17.*
