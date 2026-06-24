# Recette — Lot S1 · Shop Structure V1 sobre

| Champ | Valeur |
| --- | --- |
| Date | 2026-06-24 |
| Branche | `codex/ck-home-shop-consolidation-20260624` |
| Module | `dorevia_ck_theme` **19.0.1.56.0** |
| Instance | `dorevia_ck_marketone_01` · `http://localhost:18079` |
| Statut | Livré · recette machine au vert |

---

## 1. Ce qui a été modifié

### Intro Shop (`s_ck_shop_intro`)

- Wording public corrigé : **Boutique C-Kréyòl**
- Phrase de promesse ajoutée : *Produits créoles sélectionnés, aux origines identifiées.*
- Compteur dynamique via `search_count` dans l’intro (`N produit(s) sélectionné(s)`)
- Pas de mention Nantes / France / Europe / livraison dans l’intro
- Pas de CTA intro (scroll naturel suffisant en mobile)

### Barre catalogue

- Compteur retiré de la toolbar (`products_ck_toolbar_count` désactivée) — **pas de doublon**
- Recherche et tri conservés, SCSS allégé (taille réduite, couleurs discrètes)
- Filmstrip pills natif Odoo inchangé

### Sidebar

- Titre CK : **Affiner ma sélection** (remplace « Filtres »)
- Facette tags : **Origines & préférences** (desktop + offcanvas mobile)
- Facette prix : libellé **Budget** (quand le bloc est affiché)
- Règle slider prix option B : masqué si `search_count < 15`, sauf filtre prix actif (`isFilteringByPrice`)

### Cards produit

- Aucune refonte — vérification conforme (origine conditionnelle, CTA panier, pas de producteur, pas d’étoiles vides)

---

## 2. Hors périmètre (volontairement non traité)

| Sujet | Lot |
| --- | --- |
| Home | H2 |
| Fiche produit | — |
| Rating / étoiles | R1 |
| Producteur en card | P1 |
| Rayons éditorialisés complets | P2B |
| Refonte moteur facettes | — |
| Alignement libellés catégories BO (Soin & bien-être, Coup de cœur) | S3 |
| Total publié indépendant pour slider prix | S2 |
| Header / footer | — |

---

## 3. Captures produites

Dossier : `captures/shop_structure_s1/`

| Fichier | Vue | Résultat |
| --- | --- | --- |
| `shop_desktop_top.png` | `/shop` 1280 · haut de page | ✅ 200 |
| `shop_desktop_grid.png` | `/shop` 1280 · zone grille | ✅ 200 |
| `shop_category_epicerie_desktop.png` | `/shop/category/epicerie-1` 1280 | ✅ 200 |
| `shop_tablet_800.png` | `/shop` 800 | ✅ pas d’overflow |
| `shop_mobile_390.png` | `/shop` 390 | ✅ pas d’overflow |

Rapport machine : `shop_structure_s1_results.json`

---

## 4. Tests réalisés

### Tests automatisés (`dorevia_ck_shop_s1`)

| Test | Résultat |
| --- | --- |
| Intro promesse + wording C-Kréyòl | ✅ |
| Compteur dans intro, absent toolbar | ✅ |
| Sidebar micro-copy | ✅ |
| Outils natifs préservés (filmstrip, grille, cards) | ✅ |
| `/shop/category/epicerie-1` non régressé | ✅ |
| Pas d’intro dupliquée | ✅ |

**6/6 au vert** sur `dorevia_ck_marketone_01`.

### Tests manuels / captures

| Critère | Résultat |
| --- | --- |
| `/shop` répond 200 | ✅ |
| `/shop/category/epicerie-1` répond 200 | ✅ |
| Recherche shop fonctionnelle | ✅ (markup natif conservé) |
| Tri fonctionnel | ✅ |
| Filtres tags fonctionnels | ✅ |
| Panier rapide | ✅ (CTA `card-cart-cta` présent) |
| Overflow horizontal 1280 / 800 / 390 | ✅ aucun |
| Promesse visible avant outils catalogue | ✅ |

### Cards

- Grille : **14** éléments `.oe_product` comptés en capture (comportement Odoo inchangé, pas de régression structurelle du lot)
- Compteur intro : **7** (`search_count` filtré publié/vendable) — écart catalogue seed antérieur au lot, pas introduit par S1

---

## 5. Arbitrages à remonter MOA

| Sujet | Constat | Recommandation |
| --- | --- | --- |
| **Slider prix** | Option B livrée (`search_count < 15`) — slider masqué avec 7 produits | Valider S2 si la MOA veut le total publié indépendant des filtres |
| **Budget** | Libellé prêt mais bloc masqué tant que seuil non atteint | Normal en V1 ; visible dès 15+ produits ou filtre prix actif |
| **Coup de cœur** | Présent dans le filmstrip natif (catégorie BO publiée) | Arbitrer S3 : porte d’entrée catalogue ou badge seul |
| **Soin & bien-être** | Filmstrip affiche « Soin & Bien-être » ; nav header encore « Maison & Bien-être » | Correction BO/migration (lot S3), pas hack template |
| **CTA intro mobile** | Non ajouté — scroll suffisant sur capture 390 | Garder hors S1 sauf retour MOA |

---

## 6. Fichiers touchés

```
dorevia_ck_theme/
  views/snippets/ck_snippet_shop_intro.xml
  views/website_sale_toolbar_count.xml
  views/website_sale_sidebar.xml
  views/website_sale_sidebar_labels.xml
  views/website_sale_price_filter_threshold.xml
  static/src/scss/website_sale.scss
  tests/test_ck_shop_structure_s1.py
  __manifest__.py (19.0.1.56.0)

dorevia_ck_marketone_content/
  tests/test_ck_shop_phase3_compose.py (assertion wording)
```

---

## 7. Verdict

```text
Lot S1 livré.
La page /shop se lit désormais comme un rayon boutique C-Kréyòl :
promesse → catégories → outils secondaires → produits achetables.
Odoo intact (recherche, tri, filtres, URLs, panier rapide).
```

Critère de réussite MOA : **atteint** sur instance de recette.
