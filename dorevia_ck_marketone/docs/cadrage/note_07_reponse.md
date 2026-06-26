# Retour Dev / QA — Note 07 · Évolution pages catégories Boutique C-Kréyòl V1

| Champ | Valeur |
| --- | --- |
| Date | 26 juin 2026 |
| Référence | `note_07.md` v1.1 |
| Destinataires | Produit / UX, Lead Tech |
| Statut | **Validé MOA** — ticket Dev [`TICKET_DEV_SHOP_CATEGORY_PAGES_CK_NOTE_07.md`](TICKET_DEV_SHOP_CATEGORY_PAGES_CK_NOTE_07.md) |
| Auteur | Dev / QA |

---

## Synthèse

| Élément | Réponse |
| --- | --- |
| **Faisabilité** | **Oui** — avec arbitrages produit mineurs (bloc rebond, copy/CTA) |
| **Approche** | Héritages xpath légers sur `website_sale.products` + offcanvas natif Odoo 19 — **pas** de réécriture du template |
| **Estimation** | **4–5,5 j-h Dev** + **1,5–2 j-h QA** — livrable en **1 sprint court** |
| **Implémentation** | **Ticket Dev ouvert** — voir `TICKET_DEV_SHOP_CATEGORY_PAGES_CK_NOTE_07.md` |

---

## 1. Faisabilité technique

| Verdict | Justification |
| --- | --- |
| **Oui** | Le périmètre s'appuie sur des mécanismes déjà en place : héritages QWeb sur `website_sale.products`, offcanvas natif Odoo 19, cards CK, header rayon P2B (Épicerie). Aucun nouveau modèle métier requis. |
| **Partiellement** | Le **bloc de rebond** (§2.5) et l'**affichage conditionnel des sous-catégories** (§2.4) hors Épicerie nécessitent une petite couche Python (helper ou extension contrôleur) + copy/CTA validés par Produit. |

---

## 2. État des lieux code (base CK installée)

### Modules actifs concernés

| Module | Rôle actuel |
| --- | --- |
| `dorevia_ck_theme` | Classe `.ck-shop-page`, sidebar « Affiner ma sélection », toolbar SCSS, cards, filmstrip pills |
| `dorevia_ck_marketone_content` | Métadonnées card (`t-if` origine/ligne secondaire), header rayon P2B Épicerie (`.ck-rayon-families`) |

### Modules non installés sur la base CK

`dorevia_ckreyol_marketone`, `dorevia_ckreyol_marketplace` : leurs surcharges shop (sidebar custom, offcanvas enrichi) sont **inertes** — pas de conflit direct, mais ne pas s'en inspirer sans vérifier l'isolation multi-site.

### Héritages existants sur `website_sale.products` (CK)

- `dorevia_ck_theme.products_ck_sidebar_polish` — classe `.ck-shop-sidebar` sur `#products_grid_before`
- `dorevia_ck_theme.products_ck_shop_compose` — intro `s_ck_shop_intro`
- `dorevia_ck_marketone_content.website_sale_rayon_editorial` — header P2B Épicerie

### Cards produit

Les champs optionnels (origine, ligne secondaire producteur/format/prix réf.) sont déjà gérés via `t-if` dans `dorevia_ck_marketone_content/views/website_sale_product_card.xml` — le lot note 07 §2.7 est surtout un **audit CSS** (marges / min-height résiduels).

### Point d'attention produit

Le ticket P2 (§4.5) demandait de *conserver* la sidebar ; la note 07 la supprime. C'est un **changement de direction assumé** — les tests S1 devront être réécrits en conséquence.

---

## 3. Approche recommandée (par exigence UX)

### §2.1 / §2.2 — Suppression sidebar + grille pleine largeur

**Recommandation : héritage léger xpath + SCSS scopé `.ck-shop-page` — pas de template alternatif, pas de réécriture de `website_sale.products`.**

1. Masquer `#products_grid_before` (desktop) via xpath (`d-none`) ou SCSS.
2. Étendre la grille `#products_grid` / colonne produits en `col-12` (xpath sur le conteneur Bootstrap natif).
3. Conserver le formulaire `form.js_attributes` **dans le DOM** (dans l'offcanvas) pour ne pas casser le JS de filtrage Odoo.

**Rejeté :** template alternatif par catégorie → dette de maintenance, risque de divergence avec les mises à jour Odoo.

### §2.3 — Filtres dans un drawer

**Recommandation : réutiliser l'offcanvas natif `#o_wsale_offcanvas` — ne pas réinjecter manuellement `website_sale.products_attributes`.**

Odoo 19 duplique déjà filtres desktop (sidebar) et mobile (offcanvas). Le chemin le moins risqué :

1. Cacher la sidebar desktop.
2. Rendre le bouton « Filtrer » (`data-bs-target="#o_wsale_offcanvas"`) **visible aussi sur desktop** (retirer `d-lg-none` ou équivalent via xpath).
3. Styliser l'offcanvas CK :
   - **Desktop** : `offcanvas-end`, largeur ~360–400 px.
   - **Mobile 390 px** : plein écran (classes Bootstrap + SCSS existant header offcanvas CK réutilisable).
4. Conserver les micro-libellés S1 (`Affiner ma sélection`, `Origines & préférences`, `Budget`) — déjà branchés sur sidebar **et** offcanvas.

**Pas de JS custom** sauf badge « filtre actif » si le natif ne suffit pas (vérification en recette).

### §2.4 — Sous-catégories visuelles conditionnelles

**Recommandation : généraliser le pattern P2B existant.**

- **Épicerie** : déjà couvert par `get_ck_rayon_editorial()` + `.ck-rayon-families` (seuil catalogue §6 P2B).
- **Autres catégories** : helper du type `get_ck_category_family_tiles()` réutilisant `_category_has_published_products` et la logique image produit de `shop_rayon_editorial.py`.
- Condition d'affichage : **au moins 1 enfant direct avec produit publié** — pas seulement `child_id` non vide.

Cela couvre Boissons / Soin / Artisanat (pas de tuiles si enfants vides) et Épicerie (tuiles Biscuits, Confitures, Farines).

### §2.5 — Bloc de rebond

**Recommandation : snippet/template statique + helper Python via `_get_additional_shop_values` (extension légère `WebsiteSale` dans `dorevia_ck_marketone_content`).**

Condition proposée :

```python
show_rebound = (
    category
    and not search
    and not ck_shop_has_active_filters(request, post)  # attrib, tags, min/max price
    and products_count < 3
)
```

- **Ne pas afficher** si recherche, filtre attribut/prix/tags actif, ou catégorie vide (message Odoo natif).
- **Tri modifié** : le glossaire mentionne « état initial sans tri modifié », mais la checklist QA ne le teste pas — **à trancher** : soit on ignore le tri (plus simple), soit on masque aussi si `order != default` (plus strict).

**Arbitrage Produit requis** : texte du message + CTA (vers `/shop` ? catégorie sœur la plus fournie ? mapping fixe ?).

### §2.6 — Toolbar compacte

**Recommandation : xpath de réorganisation légère + SCSS sur `#o_wsale_products_header`.**

Une seule ligne Filtrer | Recherche | Tri, sans réécrire les `t-call` natifs (`products_sort`, barre de recherche). Inspiration interne possible : `_shop_grid_header.scss` (module Marketone, non installé sur base CK).

### §2.7 — Card sans ligne vide

**Recommandation : audit CSS uniquement** — la logique `t-if` est en place ; vérifier `min-height` / marges résiduelles sur `.ck-product-card__body` quand origine et meta sont absents.

### §2.8 — Responsive mobile 390 px

**Recommandation : SCSS responsive sur toolbar + offcanvas + grille `col-12`** ; réutiliser les scripts de recette existants (`ck_nav_shop_recette_mobile_390.mjs` comme modèle).

---

## 4. Réponses aux questions ouvertes (note 07 §5)

| Question | Réponse |
| --- | --- |
| Override `website_sale.products` ? | **Non** — héritages xpath multiples, priorité 20–45, comme aujourd'hui. |
| Réinjecter `products_attributes` dans offcanvas ? | **Non** — l'offcanvas natif les contient déjà. |
| Dépendance Bootstrap offcanvas ? | **Oui** — déjà utilisée (header mobile CK). Pas de nouvelle lib. |
| Drawer plein écran mobile / latéral desktop ? | **Oui** — aligné UX et pratique Odoo. |
| Condition rebond | `count < 3 AND NOT search AND NOT filter_active` (+ catégorie définie). |
| Grille Bootstrap vs CSS Grid | **Bootstrap natif** (`col-12 col-md-6 col-lg-4`) + centrage conditionnel SCSS si < 3 produits — pas de refonte Grid. |
| Card réutilisable `t-call` ? | **Oui** — `website_sale.products_item` hérité ; affiner `t-if` / CSS, pas de duplication. |
| Module surchargeant déjà `website_sale.products` ? | **Oui, côté CK** : `dorevia_ck_theme` + `dorevia_ck_marketone_content`. **Non** : modules `dorevia_ckreyol_*` (désinstallés sur base CK). |

### Slugs réels (instance seed `dorevia_ck_marketone_01`)

À intégrer dans la checklist QA (remplacer les exemples de la note) :

| Catégorie | Slug confirmé |
| --- | --- |
| Boutique | `/shop` |
| Épicerie | `/shop/category/epicerie-1` |
| Boissons | `/shop/category/boissons-123` |
| Soin & Bien-être | `/shop/category/soin-bien-etre-2` |
| Artisanat | `/shop/category/artisanat-3` |

---

## 5. Risques de régression

| Risque | Niveau | Mitigation |
| --- | --- | --- |
| Filtres cassés (soumission `js_attributes`) | **Moyen** | Ne pas déplacer le markup des filtres ; tester attrib + prix + reset |
| Tests auto S1 obsolètes (sidebar attendue) | **Élevé** | Mettre à jour `test_ck_shop_structure_s1.py` |
| Impact multi-site | **Moyen** | `.ck-theme` s'applique à tout site utilisant le thème — vérifier qu'aucun autre site Odoo n'installe `dorevia_ck_theme` sans intention CK |
| Pages hors catégorie (`/shop?search=`, marques si activées) | **Faible** | Changements scopés `.ck-shop-page` uniquement |
| SEO | **Faible** | Suppression `<aside>` filtres : neutre ; H1 inchangé ; URLs filtres/pagination identiques |
| Conflit P2B Épicerie | **Faible** | Header rayon + filmstrip : vérifier qu'on ne duplique pas sous-catégories (masquer filmstrip sur page catégorie si tuiles P2B actives ?) |
| Header / offcanvas z-index | **Faible** | Recette 390 px : drawer filtres vs menu burger |

---

## 6. Estimation

| Lot | Contenu | Jours-homme |
| --- | --- | --- |
| A | Sidebar → offcanvas desktop + grille pleine largeur + toolbar | **1,5–2 j** |
| B | Sous-catégories génériques + rebond (helper + template) | **1–1,5 j** |
| C | Cards CSS + responsive 390 px + badge filtre actif | **0,5–1 j** |
| D | Tests auto + mise à jour recettes + captures | **1 j** |
| **Total Dev** | | **4–5,5 j-h** |
| **QA** | Recette §4 + non-régression | **1,5–2 j-h** |

**Verdict planning : livrable en 1 sprint court** (1 semaine dev + QA en parallèle fin de sprint), sous réserve de validation copy/CTA rebond sous 48 h.

**Prérequis :** aucune montée de lib ; possible bump version `dorevia_ck_theme` (assets-only) + petit ajout Python dans `dorevia_ck_marketone_content`.

---

## 7. Plan de tests de non-régression

### 7.1 Pages `website_sale` à parcourir systématiquement

| Page | Scénario |
| --- | --- |
| `/shop` | Grille pleine largeur, toolbar, drawer filtres, filmstrip, intro S1 |
| `/shop/category/epicerie-1` | Tuiles sous-familles, pas de sidebar, P2B intact |
| `/shop/category/boissons-123` | 1 produit, rebond, pas de tuiles |
| `/shop/category/soin-bien-etre-2` | Badge Bio, rebond |
| `/shop/category/artisanat-3` | Badge Nouveau, rebond |
| `/shop/category/epicerie-biscuits-183` | Sous-catégorie L2, pas de rebond si ≥ 3 produits |
| `/shop?search=manioc` | Pas de rebond, grille filtrée |
| `/shop/category/epicerie-1?attrib=…` | Drawer + filtre actif + pas de rebond |
| `/shop/product/<slug>` | Fiche inchangée |
| `/shop/cart` → checkout | Ajout panier depuis grille |
| `/` (home) | Cards home non impactées |

### 7.2 Tests automatiques à adapter / ajouter

- `dorevia_ck_theme.tests.test_ck_shop_structure_s1` → drawer au lieu de sidebar.
- Nouveau : `test_ck_shop_rebound_sparse_category`, `test_ck_shop_filters_offcanvas_desktop`.
- Conserver : `test_ck_shop_product_card`, `test_ck_shop_phase3_compose`, tests nav shop V2.

### 7.3 Viewports

- Desktop 1280 px
- Tablette 800 px
- Mobile **390 px** (checklist note 07 §4.1)

### 7.4 Scripts de capture

Étendre `ck_shop_structure_s1_captures.mjs` ou créer `ck_shop_category_v1_recette.mjs` (même base que nav shop V2).

---

## 8. Points de vigilance / blocants

1. **Copy et CTA du bloc rebond** — bloquant conception détaillée si non fournis.
2. **Tri modifié** — clarifier si le rebond doit disparaître (glossaire vs checklist).
3. **Filmstrip vs tuiles catégorie** — sur `/shop/category/epicerie-1`, risque de double navigation (pills filmstrip + cercles P2B) ; proposer de masquer le filmstrip sur les pages catégorie racine éditorialisées.
4. **Tests S1** — actuellement verts sur sidebar ; rupture intentionnelle.
5. **Multi-site** — si un second site Odoo partage l'instance sans thème CK, confirmer l'isolation (aujourd'hui `ck-theme` est global au module installé).

---

## 9. Livrables attendus après validation MOA / Dev / QA

1. Note technique courte (xpath listés, variables contrôleur rebond).
2. Maquettes ou captures cibles desktop + 390 px.
3. Fiche recette QA dérivée de la note 07 avec slugs réels.
4. Go implémentation.

---

## 10. Arbitrages Produit attendus avant GO Dev

| # | Sujet | Options |
| --- | --- | --- |
| 1 | Texte + CTA bloc rebond | `/shop` · catégorie sœur dynamique · mapping fixe |
| 2 | Tri modifié masque-t-il le rebond ? | Oui (strict) · Non (simple) |
| 3 | Filmstrip sur pages catégorie Épicerie | Conserver · Masquer si tuiles P2B actives |

---

*Document Dev/QA — en réponse à `note_07.md` v1.1 — 26 juin 2026*
