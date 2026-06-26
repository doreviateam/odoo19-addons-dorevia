# Note de livraison — Alignement card Shop sur canon Homepage

| Champ | Valeur |
| --- | --- |
| Date | 26 juin 2026 |
| Commit | _à compléter_ |
| Verdict QA | **GO technique** — [`RECETTE_QA_CARD_SHOP_CANON_HOME_VERDICT.md`](../design/maquette_01.2/RECETTE_QA_CARD_SHOP_CANON_HOME_VERDICT.md) |
| Modules | `dorevia_ck_theme` **19.0.1.67.0** · `dorevia_ck_marketone_content` **19.0.1.47.0** |
| Instance recette | `dorevia_ck_marketone_01` · `http://localhost:18079` |

---

## Objectif

Parité informationnelle et comportementale des cards catalogue (`/shop`, catégories, recherche) avec le canon **« Nos coups de cœur »** (Home).

---

## Modifications

### 3.1 Origine dans la ligne méta (retrait eyebrow P2A)

| Fichier | Changement |
| --- | --- |
| `dorevia_ck_marketone_content/views/website_sale_product_card.xml` | Suppression du `<p class="ck-product-card__origin">` au-dessus du titre |
| `dorevia_ck_marketone_content/home_featured.py` | `_get_shop_card_secondary_line` délègue à `_get_featured_card_metadata_line` (origine · tags · format · prix/kg) |
| `dorevia_ck_marketone_content/models/product_template.py` | Suppression de `get_ck_shop_card_origin_label` ; doc meta alignée canon Home |
| `dorevia_ck_theme/static/src/scss/website_sale.scss` | Retrait styles `.ck-product-card__origin` |

**Règle** : `_join_featured_metadata_parts` ignore les segments vides — pas de `·` orphelin.

### 3.2 CTA plus compact (desktop / tablette)

| Fichier | Changement |
| --- | --- |
| `dorevia_ck_theme/static/src/scss/website_sale.scss` | CTA `6px 10px`, `font-size: 11px` (aligné `.ck-product-card--home`) ; `--o-wsale-card-btn-submit-padding-x: 10px` |
| Mobile ≤ 575 px | CTA pleine largeur conservé, `min-height: 44px`, `8px 14px` (tactile, non-régression 65.0) |

### 3.3 Padding interne

| Zone | Home (réf.) | Shop (67.0) |
| --- | --- | --- |
| Body | `8px 12px 4px` | identique |
| Foot | `8px 12px 10px`, gap `6px` | identique |
| Titre / méta | `13px` / `10px` | identique |

**Contrainte technique** : le padding natif Odoo sur `.o_wsale_product_information` était cumulé avec le mixin body (`12px 14px`) — neutralisé via `padding: 0` sur le conteneur shop uniquement.

---

## Non modifié (hors périmètre)

- Homepage, fiche produit, checkout, BO
- Wishlist shop, badges, logique panier
- Grille 4/2/1, visibility CTA, pied desktop ligne (66.0)

---

## Tests

Tag `dorevia_ck_shop_card` :

- `test_metadata_line_matches_home_canon`
- `test_shop_card_no_separate_origin_label`
- Vues : absence `ck-product-card__origin` / `get_ck_shop_card_origin_label`

---

## Recette visuelle suggérée

| Vueport | Pages |
| --- | --- |
| Desktop 1280 | `/shop`, `/shop/category/epicerie-1`, catégorie pauvre (Soin ou Artisanat) |
| Mobile 390 | `/shop` — pas d’overflow ; pied colonne + CTA pleine largeur |

Comparer avec section Home « Nos coups de cœur » : ordre titre → méta → séparateur → prix | CTA.

---

## Recette (26/06)

- Tests auto : **22/22** (`dorevia_ck_shop_card` + `dorevia_ck_shop_s1`)
- Playwright : `technicalPass: true` — [`card_shop_canon_home_results.json`](../design/maquette_01.2/captures/card_shop_canon_home_20260626/card_shop_canon_home_results.json)
- Captures : `captures/card_shop_canon_home_20260626/`

---

## Réserve

Captures avant/après : à produire en recette MOA (PNG hors git, JSON recette si script Playwright).
