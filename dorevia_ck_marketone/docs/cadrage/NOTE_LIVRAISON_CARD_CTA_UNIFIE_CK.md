# Note de livraison — Cards Produit CK · CTA unifié

| Champ | Valeur |
| --- | --- |
| Date | 26 juin 2026 |
| Commit | `b92c57f` |
| Verdict QA | **GO technique** — [`RECETTE_QA_CARD_CTA_UNIFIE_VERDICT.md`](../design/maquette_01.2/RECETTE_QA_CARD_CTA_UNIFIE_VERDICT.md) |
| Modules | `dorevia_ck_theme` **19.0.1.66.0** (pied canon) · **65.0** (CTA unifié) · `dorevia_ck_marketone_content` _(tests)_ |
| Instance recette | `dorevia_ck_marketone_01` |

---

## Résumé

Uniformisation du CTA **« Ajouter au panier »** (bouton texte pill terre cuite) sur les grilles catalogue CK (`/shop`, catégories, recherche), aligné sur le canon Home « Nos coups de cœur ». Suppression du CTA icône ronde P2A. Grille catalogue **4 colonnes desktop** (`shop_ppr = 4`), cohérente avec la Home.

---

## Fichiers modifiés (attendus)

### `dorevia_ck_theme`

| Fichier | Modification |
| --- | --- |
| `views/website_sale_product_card.xml` | `shop_product_buttons_ck_card` — libellé visible |
| `static/src/scss/website_sale.scss` | Retrait surcharge CTA icône 38×38 px ; pied card mobile colonne |
| `static/src/scss/product_card.scss` | _(si nécessaire)_ extension `ck-product-card-foot-desktop` à `--shop` |
| `data/website_shop_grid.xml` *(nouveau)* | `website.shop_ppr = 4` |
| `__manifest__.py` | Bump version + déclaration data |

### `dorevia_ck_marketone_content`

| Fichier | Modification |
| --- | --- |
| `tests/test_ck_shop_product_card.py` | Assertions CTA visible + fix non-régression home |

---

## Templates Odoo touchés

| Clé XML | Héritage |
| --- | --- |
| `dorevia_ck_theme.shop_product_buttons_ck_card` | `website_sale.shop_product_buttons` |
| _(inchangé)_ `dorevia_ck_theme.products_item_ck_card` | `website_sale.products_item` |
| _(inchangé)_ `dorevia_ck_marketone_content.products_item_ck_card_metadata` | métadonnées card |

---

## Classes CSS impactées

| Classe | Effet |
| --- | --- |
| `.card-cart-cta` | Retour au mixin pill texte (`ck-product-card-cta-cart`) |
| `.card-cart-cta__label` | Visible (plus `visually-hidden`) |
| `.ck-product-card--shop .ck-product-card__foot` | Layout pied réaligné Home |
| `.o_wsale_product_btn_primary.card-cart-cta` | Plus de règles 38×38 px circulaires |

---

## Déploiement

```bash
# Exemple — adapter chemins instance
odoo-bin -u dorevia_ck_theme,dorevia_ck_marketone_content -d dorevia_ck_marketone_01 --stop-after-init
# Redémarrer le worker si assets modifiés
```

Hard refresh navigateur (`Cmd+Shift+R`) obligatoire pour valider les assets SCSS.

---

## Tests automatisés

```bash
odoo-bin -d dorevia_ck_marketone_01 --test-tags dorevia_ck_shop_card --stop-after-init
```

Résultat attendu : **tous verts**.

---

## Captures à joindre au dossier QA

Dossier suggéré : `docs/design/maquette_01.2/captures/card_cta_unifie_YYYYMMDD/`

| # | Vue | Fichier suggéré |
| --- | --- | --- |
| 1 | Home — section Coups de cœur (référence) | `01_home_1280.png` |
| 2 | `/shop` desktop | `02_shop_1280_avant.png` / `02_shop_1280_apres.png` |
| 3 | Catégorie riche (Épicerie) | `03_epicerie_1280.png` |
| 4 | Catégorie pauvre (Boissons) | `04_boissons_1280.png` |
| 5 | Mobile 390 px — `/shop` | `05_shop_390.png` |
| 6 | Mobile 390 px — catégorie | `06_category_390.png` |

---

## Correctif 19.0.1.66.0 — pied canon Home (post-GO 65.0)

| Élément | Correction |
| --- | --- |
| Desktop ≥ 768 px | Prix + CTA sur **une ligne**, bouton compact (`ck-product-card-foot-desktop` sur `--shop`) |
| Séparateur | `border-top` explicite sur le pied card |
| Mobile ≤ 575 px | Colonne + CTA pleine largeur conservés (non-régression 65.0) |

**Recette** : en attente MOA/QA ciblée desktop 1280 + 390 px.

---

## Correctif 19.0.1.65.0 (post-recette QA 26/06)

| Bloquant QA | Correction |
| --- | --- |
| CTA `visibility: hidden` < 992 px | Neutralisation `actions_onhover` Odoo 19 — `visibility: visible !important` sur bouton + `.o_label` |
| Grille 800 px = 4 cols | `--o-wsale-ppr: 2` + `grid-column: span 6` (576–991 px) |
| Grille 390 px = 2 cols | `--o-wsale-ppr: 1` + `grid-column: span 12` (≤575 px) — remplace règles `table/td` obsolètes |

Fichier : `website_sale.scss` — sections « CTA unifié · responsive < lg » et « Lot D · grille 4/2/1 ».

**Re-recette 26/06** : **GO technique QA** — `technicalPass: true`, `failures: []`.

---

## Non-régression vérifiée

- [ ] Home inchangée
- [ ] Note 07 layout (grille, toolbar, drawer) intact
- [ ] Ajout panier grille fonctionnel
- [ ] Wishlist boutique fonctionnelle
- [ ] Prix référence logique CK respectée

---

## Recette QA

Voir [`RECETTE_QA_CARD_CTA_UNIFIE_CK.md`](../design/maquette_01.2/RECETTE_QA_CARD_CTA_UNIFIE_CK.md).
