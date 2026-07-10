# Inventaire catalogue seed — référence sandbox `18079`

| Champ | Valeur |
| --- | --- |
| Date extraction | 10 juillet 2026 |
| Source | Base `dorevia_ck_marketone_01` · http://localhost:18079 |
| Méthode | PostgreSQL (produits/catégories) + curl HTML (DOM home) |
| Branche | `feat/ck-catalog-seed-moa-v1` |
| Cadrage parent | [NOTE_MOA_CADRAGE_CK_DEPLOYABLE_SEED_CODE_FIRST_20260710.md](NOTE_MOA_CADRAGE_CK_DEPLOYABLE_SEED_CODE_FIRST_20260710.md) |

---

## Synthèse

| Métrique | Valeur mesurée |
| --- | --- |
| Templates publiés | **9** |
| Templates `ck_is_featured` | **6** |
| Variantes (templates featured) | **7** (Manio = 2 variantes) |
| Cartes vedettes **affichées** Home | **4** (cap `FEATURED_CURATED_MAX`) |
| Racines catégories publiques | **5** (dont Coups de cœur) |
| Langue site | `fr_FR` · website `C-Kréyòl` |
| Slug catégorie Épicerie | `/shop/category/epicerie-1` → **200** |

---

## 1. Produits publiés (liste seed figée)

| ID | Nom | `ck_is_featured` | Prix | `website_sequence` | Variantes | Rôle seed |
| ---: | --- | :---: | ---: | ---: | ---: | --- |
| 3 | Confiture de goyave | ✅ | 5,50 € | 10005 | 1 | Vedette · origine |
| 4 | Manio Crackers | ✅ | 3,60 € | 10010 | **2** | Vedette · variantes salé/sucré |
| 20 | Galettes de manioc | ❌ | 7,50 € | 10015 | 1 | Catalogue manioc (hors vedettes) |
| 7 | Savon vétiver | ✅ | 6,30 € | 10025 | 1 | Vedette · soin |
| 1076 | Chapeau Panama | ✅ | 17,60 € | 10030 | 1 | Vedette · UOM card |
| 2336 | Pâte de manioc | ✅ | 3,95 € | 10035 | 1 | Vedette · manioc |
| 2593 | Jus Mont-Pelé | ❌ | 5,00 € | 10040 | 1 | Boissons · MOA-2 UOM |
| 4491 | Tambour Gro Ka | ✅ | 435,00 € | 10045 | 1 | Vedette · artisanat |
| 4583 | Coffret découverte créole | ❌ | 29,90 € | 10050 | 1 | Bloc coffret Home |

**Images :** tous les templates publiés ont une image BO (filestore) sur la sandbox — à exporter vers `static/img/catalog/` (Phase 2).

### 1.1 Variantes Manio Crackers (template 4)

| Variant ID | Libellé |
| ---: | --- |
| 21 | Manio Crackers (combinaison 2) |
| 22 | Manio Crackers (combinaison 3) |

### 1.2 Pool vedettes vs affichage Home (mesure HTML `/`)

Ordre d’affichage **constaté** (4 cartes, cap atteint) :

| # carte | Image servie |
| ---: | --- |
| 1 | `/web/image/product.template/3/image_512` — Confiture |
| 2 | `/web/image/product.product/21/image_512` — Manio v1 |
| 3 | `/web/image/product.product/22/image_512` — Manio v2 |
| 4 | `/web/image/product.template/7/image_512` — Savon vétiver |

Templates featured **hors top-4 affiché** (présents en seed, tri `website_sequence`) : Chapeau Panama, Pâte de manioc, Tambour Gro Ka.

---

## 2. Catégories publiques

### 2.1 Racines (`parent_id` NULL)

| ID | Nom exact BO |
| ---: | --- |
| 1 | Épicerie |
| 123 | Boissons |
| 2 | Soin & Bien-être |
| 3 | Artisanat |
| 24 | Coups de cœur |

### 2.2 Sous-catégories (extrait — seed NAV Phase 3)

| ID | Nom | Parent |
| ---: | --- | --- |
| 183 | Biscuits | Épicerie |
| 184 | Confitures | Épicerie |
| 388 | Farines & manioc | Épicerie |
| 185 | Épices | Épicerie |
| 186 | Jus de fruits | Boissons |
| 187 | Alcools | Boissons |
| 188 | Liqueurs | Boissons |
| 189 | Savons | Soin & Bien-être |
| 190 | Huiles | Soin & Bien-être |
| 970 | Musique | Artisanat |

---

## 3. Site & branding (référence)

| Champ | Valeur 18079 |
| --- | --- |
| `website.name` | C-Kréyòl |
| `website.default_lang_id` | `fr_FR` |
| Slug Épicerie | `epicerie-1` (HTTP 200) |

---

## 4. Home — composition DOM (gate `accept-moa`)

### 4.1 Ordre snippets (`data-snippet` sur `/`)

1. `s_ck_hero` (+ 3× `s_ck_hero_slide`)
2. `s_ck_reassurance`
3. `s_ck_featured_products`
4. 4× `s_ck_univers_card`
5. (coffret, dual, éditorial — présents plus bas dans l’arch)

### 4.2 Sélecteurs gate **B3** (figés)

| Contexte | Sélecteur retenu |
| --- | --- |
| Bloc vedettes | `.ck-featured-products` |
| Grille stable | `.ck-featured-products__grid--stable` |
| Cartes (count = 4) | `.ck-product-card__img` |
| Image produit | attribut `src` matching `/web/image/product\.(template\|product)/\d+/image_` |

**Note :** sur `/shop`, le markup shop utilise `.oe_product img` — **ne pas** utiliser ce sélecteur pour B3 Home.

### 4.3 Hero assets (référence)

3 slides : `ck_hero_crepe_manioc.webp` · `ck_hero_pate_manioc_2.webp` · `ck_hero_flag_market.webp`

---

## 5. Mapping export images → fichiers seed (Phase 2)

| Produit | Fichier cible proposé |
| --- | --- |
| Confiture de goyave | `catalog/confiture_goyave.webp` |
| Manio Crackers (×2 si distinct) | `catalog/manio_crackers_sale.webp` · `catalog/manio_crackers_sweet.webp` |
| Galettes de manioc | `catalog/galettes_manioc.webp` |
| Savon vétiver | `catalog/savon_vetiver.webp` |
| Chapeau Panama | `catalog/chapeau_panama.webp` |
| Pâte de manioc | `catalog/pate_manioc.webp` |
| Jus Mont-Pelé | `catalog/jus_mont_pele.webp` |
| Tambour Gro Ka | `catalog/tambour_gro_ka.webp` |
| Coffret découverte | `catalog/coffret_decouverte.webp` |

Script d’extraction à écrire Phase 2 : `scripts/export_sandbox_images.py` (lecture attachments sandbox → webp).

---

## 6. Écarts connus vs pré-prod actuelle (ne pas reproduire)

| Point | 18079 | Pré-prod (état juil. 2026) |
| --- | --- | --- |
| Produits publiés | 9 | 2 |
| `ck_is_featured` | 6 | 0 |
| Home réassurance | ✅ | ❌ |
| Home vedettes | 4 cartes | ❌ |
| Langue | `fr_FR` | `en_US` |

---

*Inventaire généré en Phase 1 — base du seed XML Phase 3.*
