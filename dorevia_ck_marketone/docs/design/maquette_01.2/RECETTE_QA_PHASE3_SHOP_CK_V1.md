# Recette QA — Phase 3 · Shop + catégorie principale BO · CK V1.2.x

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Instance** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **Conteneur** | `sandbox-odoo19-odoo-1` |
| **GO MOA** | [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) **§5quater — ACTÉ 2026-06-13** |
| **Prérequis** | Q1 levée §5ter · **2026-06-13** · réserve SSR · Phase 2 OK partiel |
| **Séquence** | [`SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md`](./SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md) Phase 3 |
| **Statut** | **✅ Phase 3 clôturée — OK partiel maîtrisé · gate portable OK · Phase 4 suspendue** |
| **Script composition** | [`scripts/ck_phase3_configure.py`](./scripts/ck_phase3_configure.py) · **portable via `-u dorevia_ck_theme`** |

### Déploiement sur une autre base

```bash
# Prérequis : module dorevia_ck_theme installé · catégorie « Épicerie créole » en BO
odoo -d MA_BASE -u dorevia_ck_theme --stop-after-init
docker restart <conteneur-odoo>
```

| Composant | Source portable |
|-----------|-----------------|
| Intro · réassurance M5 · signal Pro | `dorevia_ck_theme/views/website_sale_shop_compose.xml` |
| Catégorie BO (titre + description) | `dorevia_ck_theme/hooks.py` · idempotent si catégorie existe |
| Home Phase 2 · vedettes SSR | [`scripts/ck_phase2_configure.py`](./scripts/ck_phase2_configure.py) *(encore shell — hors Phase 3)* |

> Header HTTP `X-Odoo-Database: <nom_base>` requis pour les tests sandbox.

---

## 1. Périmètre Phase 3 (strict)

| # | Livrable | Route / composant | Statut Dev |
|---|----------|-------------------|------------|
| 3.1 | Boutique | `/shop` · `website_sale` natif | ☑ |
| 3.2 | Catégorie principale BO | `/shop/category/epicerie-creole-1` | ☑ |
| 3.3 | Grille produits · prix · liens fiches | Grille native Odoo | ☑ |

**Exclus respectés** :

```text
Filtres avancés · recherche custom · AJAX · catalogue parallèle
Modification checkout / panier
Modification home Phase 2 (sauf non-régression)
Modification header / footer Phase 1
Phase 4+ sans recette Phase 3
```

**Garde-fou home vedettes (§5ter)** :

```text
Grille SSR `.ck-featured-products__grid--stable` · 5 produits CK — inchangée
Carousel / Dynamic Products vedettes : interdits V1
```

---

## 2. Contrôles `/shop` — desktop

| Contrôle | Attendu | Résultat |
|----------|---------|----------|
| HTTP 200 | `/shop` accessible | ☑ 200 |
| Grille produits | Produits BO publiés visibles | ☑ **5 cartes** |
| Prix | Prix TTC lisibles sur cartes | ☑ visibles (1,00 € · données QA) |
| Liens fiches | `/shop/…` → 200 | ☑ 5 liens · 0 broken |
| Tri natif | Comportement standard CE | ☑ dropdown tri présent |
| Liens fictifs | Aucun 404 · catégories BO réelles | ☑ filmstrip 2 catégories BO |
| Intro shop | `s_ck_shop_intro` composé | ☑ « Boutique C-Kreyol » |
| Réassurance | `s_ck_reassurance` | ☑ présent |
| Signal Pro | Lien `/professionnels` | ☑ `ck-shop-pro-signal` |

---

## 3. Contrôles `/shop` — mobile 390 px

| Contrôle | Attendu | Résultat |
|----------|---------|----------|
| Overflow | `scrollWidth = 390` | ☑ 390 / 390 |
| Grille | Produits · prix · liens utilisables | ☑ 5 cartes |
| CTA | Touch · panier accessible | ☑ panier accessible |

---

## 4. Catégorie principale BO

| Contrôle | Attendu | Résultat |
|----------|---------|----------|
| URL catégorie | 200 · Épicerie créole | ☑ 200 |
| Breadcrumb | Natif `website_sale` | ☑ breadcrumb + titre catégorie |
| Grille filtrée | Produits de la catégorie | ☑ **4 produits** |
| Description BO | Hero éditorial catégorie | ☑ `o_wsale_category_description` renseigné |
| Prix · liens | Cohérents avec `/shop` | ☑ prix visibles · URLs catégorie `/shop/epicerie-creole-1/…` 200 |
| Liens fictifs | Aucun | ☑ |

---

## 5. Non-régression Phase 1

| Contrôle | Attendu | Résultat |
|----------|---------|----------|
| Header | Boutique · Découvrir · Professionnels | ☑ liens présents |
| Mega Découvrir | Épicerie créole | ☑ entrée mega-menu |
| Footer 4 col | Liens valides | ☑ footer colonnes présentes |
| `/professionnels` | 200 | ☑ 200 |

---

## 6. Non-régression Phase 2

| Contrôle | Attendu | Résultat |
|----------|---------|----------|
| Home `/` | 200 · ordre blocs Phase 2 | ☑ 200 |
| Vedettes SSR | `.ck-featured-products__grid--stable` · **5 cartes** | ☑ 5 cartes |
| Bloc Pro | CTA `/professionnels` | ☑ 7 liens Pro |
| Layout vedettes | Pas d’overflow 390 px | ☑ 390 / 390 · 5 cartes stable |
| Dynamic Products | Absent home | ☑ 0 snippet dynamique |

---

## 7. Verdict QA — confirmé MOA

| Champ | Valeur |
|-------|--------|
| **Verdict Phase 3** | ☑ **OK partiel maîtrisé — clôturé** · ☐ OK · ☐ KO |
| **GO Phase 4** | ☑ **Suspendu** · ☐ Autorisé |
| **Validé par** | **MOA CK** |
| **Date verdict** | **2026-06-13** |

**Motif OK partiel (pas OK plein)** :

```text
Livraison conforme au périmètre §5quater (shop natif, catégorie BO, non-régression Phase 1/2).
Réserve outillage : scripts Playwright v1 utilisaient des sélecteurs inadaptés à la page catégorie
  — corrigés post-verdict (voir §7bis).
Prix catalogue = données QA (1,00 €) — hors périmètre Phase 3.
```

**Points validés MOA** :

```text
/shop : 200 · intro Boutique C-Kreyol · réassurance · signal Pro · 5 cartes · prix · liens OK
/shop/category/epicerie-creole-1 : 200 · 4 produits · description catégorie HTML serveur
Mobile 390 px : pas d’overflow (390/390) sur shop, catégorie et home
Non-régression Phase 1 : header / footer / routes OK
Non-régression Phase 2 : .ck-featured-products__grid--stable · 5 cartes SSR · 0 Dynamic Products
Gate M4 : catégories vides Artisanat / Packs en 404 — cohérent
```

```text
Phase 4 : toujours suspendue jusqu’à acte MOA explicite §5quinquies (ou équivalent)
```

### Gate portable · contrat technique reproductible · **OK 2026-06-13**

```text
Gate portable Phase 3 : OK
Script local         : ck_phase3_ci.sh
Odoo tests           : 14 / 14 OK (dorevia_ck_theme_phase3)
Smoke curl           : / · /shop · /shop/category/epicerie-creole-1 OK
Playwright           : hors gate — recette UX complémentaire
GitHub Actions       : différé
```

**Hiérarchie QA actée** : le script shell = contrat technique portable · Playwright = contrôle d’expérience.

### Gate portable CI local (sans Playwright)

Script MOA/QA : [`scripts/ck_phase3_ci.sh`](./scripts/ck_phase3_ci.sh)

```bash
cd docs/design/maquette_01.2/scripts
./ck_phase3_ci.sh
# ou : CK_CI_DB=ma_base CK_CI_BASE_URL=http://localhost:8069 ./ck_phase3_ci.sh
```

| Étape | Rôle |
|-------|------|
| `-u dorevia_ck_theme` | Upgrade module sur base cible |
| `--test-tags=dorevia_ck_theme_phase3` | Contrat portable Odoo (14 tests) |
| Smoke curl | `/` · `/shop` · catégorie Épicerie créole |

> **Pas de GitHub Actions** tant que ce cycle local n’est pas stabilisé. Playwright = recette UX complémentaire, hors gate module.

**Tests Odoo seuls** :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d MA_BASE \
  --test-enable --stop-after-init \
  --test-tags=dorevia_ck_theme_phase3 --http-port=8072
```

**Recette UX Playwright (complémentaire)** :

```bash
node docs/design/maquette_01.2/scripts/ck_phase3_desktop1280.mjs
node docs/design/maquette_01.2/scripts/ck_phase3_mobile390.mjs
```

---

## 7bis. Réserve outillage — sélecteurs catégorie (levée)

| Symptôme v1 | Cause | Correctif |
|-------------|-------|-----------|
| `categoryTitle: null` | Titre catégorie dans `#o_wsale_products_header[data-category-name]`, pas `h1` | Lecture `dataset.categoryName` |
| `categoryDesc: false` | Description dans `#category_header.o_wsale_category_description` | Sélecteur `#category_header.o_wsale_category_description` |
| `productLinks: 0` | URLs catégorie = `/shop/{cat-slug}/{product-slug}` | Regex `/\/shop\/(.+\/)?[^/]+-\d+$/` · scope `#o_wsale_products_grid` |

**Post-correctif Playwright desktop** (2026-06-13) :

```text
categoryTitle: Épicerie créole · categoryDesc: true · productLinks: 4 · broken: []
category_artisanat_404: 404 · category_packs_404: 404
```

> Cette réserve était **outillage QA**, pas KO applicatif. Les scripts corrigés constituent désormais la preuve opposable catégorie.

---

## 8. Doctrine QA Phase 4+ (réserve discipline MOA)

Toute phase suivante devra reproduire le **même triptyque** :

```text
1. Contrat Odoo portable (module + test-tags)
2. Smoke curl minimal (script shell local ck_phaseN_ci.sh)
3. Recette UX Playwright séparée — hors gate module
```

GitHub Actions : uniquement après stabilisation locale du cycle `-u` + `test-tags` + smoke.

---

## 9. Documents liés

| Document | Rôle |
|----------|------|
| [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) | §5quater · garde-fous |
| [`RECETTE_QA_PHASE2_HOME_SOBER_CK_V1.md`](./RECETTE_QA_PHASE2_HOME_SOBER_CK_V1.md) | Non-régression home |
| [`GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md`](./GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md) | Mapping shop / catégorie |

---

*Recette QA Phase 3 — clôturée OK partiel maîtrisé · gate portable OK · Phase 4 suspendue · 2026-06-13.*
