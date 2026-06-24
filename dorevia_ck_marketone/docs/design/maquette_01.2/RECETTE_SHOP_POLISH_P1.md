# Recette — Shop CK V1 · polish boutique mature P1

| Champ | Valeur |
| --- | --- |
| Date | 2026-06-23 |
| Périmètre | `/shop` et `/shop/category/...` — intro, sidebar filtres, barre catalogue, cards |
| Statut | **Implémenté et conservé** (risque jugé faible sur les 4 axes — pas de piste réversible) |
| Module | `dorevia_ck_theme` **19.0.1.51.0** |

---

## 0. Correction préalable de l'audit

L'agent de recherche utilisé pour le premier passage d'audit a exploré et rapporté du code dans `dorevia_ckreyol_marketone` et `dorevia_ckreyol_marketplace` — deux modules présents dans le dossier d'addons mais **désinstallés** sur la base de travail (`dorevia_ck_marketone_01`), vérifié via `ir.module.module`. Leur contenu (chips `ckr-shop-shortcuts`, sidebar custom, libellé "Filtrer par") est **inerte sur la page réellement servie** et n'a pas été utilisé. L'audit ci-dessous a été refait à la main, sur les seuls modules installés (`dorevia_ck_theme`, `dorevia_ck_marketone_content`), vérifié directement sur le DOM live et le code source.

---

## 1. Audit (état réel, vérifié)

| Zone | Implémentation réelle |
| --- | --- |
| Intro | `dorevia_ck_theme/views/snippets/ck_snippet_shop_intro.xml` (`s_ck_shop_intro`), composé via `website_sale_shop_compose.xml` dans `website_sale.products` |
| Sidebar filtres | 100 % markup natif Odoo (`js_attributes`, accordéons), libellé "Étiquettes" = nom d'attribut DB natif (non touché). `<aside>` déjà `position-sticky` nativement. Classe `.ck-shop-sidebar` existait en SCSS mais **n'était appliquée nulle part** (CSS mort) |
| Catégories | Filmstrip natif Odoo (`#o_wsale_categories_filmstrip`), tuiles image+texte avec images de catégorie vides sur ce seed |
| Recherche / tri | Markup natif Odoo (`o_wsale_products_header_search_form_container`, `o_sortby_dropdown`), dans le même `<header>` que le filmstrip mais visuellement empilés |
| Compteur produits | `search_count` déjà exposé par le contrôleur natif (aliasé `product_count`, "common for all searchbox") — jamais affiché |
| Cards | `website_sale_product_card.xml` + `website_sale.scss` (override shop) + `product_card.scss` (mixin partagé, déjà ajusté pour la home au ticket précédent) |
| `/shop/category/...` | Confirmé 200, réutilise exactement les mêmes templates (mêmes classes `s_ck_shop_intro`, `o_wsale_products_header`) |

---

## 2. Décisions prises, par axe

### 2.1 Intro compacte + preuves CK
- H1 ramené de la taille Bootstrap `.h2` à `$ck-text-2xl`, padding vertical réduit (`$ck-space-5 $ck-space-3` au lieu de `pt32 pb16`).
- Ligne de preuves en pills ajoutée (*Origines identifiées · Expédié depuis Nantes · Sélection créole*) — même recette visuelle que le bandeau de pied de mega-menu du header (cohérence header/shop), placée **hors de la zone `o_editable`** (contenu fixe, non éditable par accident).
- Pas de hero marketing : aucune image, aucun nouveau bloc lourd.

### 2.2 Sidebar filtres structurée
- Classe `.ck-shop-sidebar` (existante, jamais utilisée) appliquée à l'`<aside>` via xpath sur attribut `class` — fond/radius/padding cohérents avec le reste du thème.
- Titre "FILTRES" ajouté en tête de colonne (xpath, hors zone scrollable de la sidebar pour rester visible).
- Accordéons "Étiquettes"/"Fourchette de prix" restylés (typo Fraunces, espacement régulier) — **aucune facette renommée ni logique touchée**.
- Sticky desktop déjà natif Odoo (`position-sticky`) — confirmé fonctionnel au scroll (capture `after_desktop_scroll.png`), pas de CSS supplémentaire nécessaire.

### 2.3 Barre catalogue unifiée
- **Décision clé** : plutôt que réécrire le filmstrip catégories, activation du variant natif Odoo **"pills"** (`website_sale.filmstrip_categories_pills`, `active=False` par défaut dans website_sale) via un simple `<record>` data. Zéro nouveau template, comportement clic/JS natif inchangé.
- `$primary` étant déjà remappé sur le terracotta CK (`frontend_bootstrap_variables.scss`, chargé avant Bootstrap dans `web.assets_frontend`), le rendu est nativement aux couleurs CK sans CSS supplémentaire.
- Fond `$ck-bg-soft` + radius appliqués à `#o_wsale_products_header` entier : titre, filmstrip-pills, recherche et tri se lisent désormais comme une seule bande.
- Compteur "N produits" ajouté via `search_count` (déjà calculé nativement par le contrôleur, aucune requête supplémentaire).

### 2.4 Cards shop — réduction de l'effet « mur de CTA »
- Padding vertical du bouton réduit (`8px` → `7px`), conservé plein (pas de suppression, conforme à la contrainte MOA).
- État hover/focus enrichi (ombre douce + léger lift `translateY(-1px)`) plutôt qu'un aplat statique — le bouton "respire" sans changer de poids visuel au repos.
- Scope strictement `.ck-shop-page` — la home (déjà simplifiée au ticket précédent : un seul CTA, pas de bouton secondaire) n'est pas affectée.

---

## 3. Incident technique rencontré et corrigé

Première tentative d'ajout du compteur produits : xpath `//div[hasclass('o_wsale_products_header_search_form_container')]` **a fait échouer le chargement complet du registre** (`ParseError: élément ne peut être localisé dans la vue parente`) — la base entière refusait de démarrer. Corrigé en retargetant sur `//header[@id='o_wsale_products_header']` (ancre `id` statique, plus robuste qu'un xpath sur classe dynamique `t-attf-class`). Rebuild propre confirmé avant de poursuivre — **aucune version cassée n'a été laissée en l'état**.

---

## 4. Vérifications machine

| Vérification | Résultat |
| --- | --- |
| `/shop` répond 200 | ✅ |
| `/shop/category/epicerie-1` répond 200 | ✅ |
| Débordement horizontal (desktop/tablette/mobile) | ✅ Aucun, sur les 3 gabarits |
| Nombre de cards inchangé avant/après | ✅ 7 avant, 7 après (cf. note §6) |
| Filtres utilisables | ✅ Coche "Dominique (Ile)" → `?tags=283` appliqué en URL, état coché conservé |
| Panier rapide fonctionnel | ✅ `POST /shop/cart/add` confirmé, badge panier 0→1 |
| Tests automatisés shop (`dorevia_ck_shop_card`, `dorevia_ck_product_origin`) | ✅ 19/19 |

---

## 5. Captures

Dossier : `captures/shop_polish_p1/`

| Fichier | Avant | Après |
| --- | --- | --- |
| Desktop 1280 haut de page | `before_desktop_top.png` | `after_desktop_top.png` |
| Desktop 1280 scroll grille | `before_desktop_scroll.png` | `after_desktop_scroll.png` |
| Tablette 800 | `before_tablet_800.png` | `after_tablet_800.png` |
| Mobile 390 | `before_mobile_390.png` | `after_mobile_390.png` |
| Catégorie /shop/category/epicerie-1 | `before_category_epicerie.png` | `after_category_epicerie.png` |

---

## 6. Limites et points à arbitrer

- **Catalogue seed réduit** : la page n'affiche que **7 produits publiés/vendables** sur cette instance (constat fait en vérifiant le nombre de cards, pas une régression de ce lot — confirmé identique avant/après mes changements via capture "avant" prise en tout début de ticket). Pour mémoire, une session antérieure (ticket homepage) avait mesuré 14 cards sur `/shop` ; l'écart est antérieur à ce lot et relève du contenu catalogue (hors périmètre), pas du code. À signaler côté contenu/MOA si ce n'est pas voulu.
- **Filmstrip catégories** : les images de catégorie sont vides sur ce seed (aucune image définie en BO) ; le mode "pills" choisi masque justement cette limite (texte seul, pas d'image), ce qui est un bénéfice indirect du choix technique mais ne résout pas l'absence d'images si un autre mode était souhaité plus tard.
- **Compteur produits** : affiché de façon minimale (texte simple), pas de traitement visuel poussé — à enrichir si la MOA le souhaite après lecture des captures.
- **CTA cards** : ajustement volontairement léger (padding + hover), pas de changement de couleur/poids — conforme à la consigne « ne pas supprimer sans arbitrage », mais une évolution plus marquée (ex. variante outline par défaut) resterait à arbitrer séparément si le « mur de CTA » est encore jugé trop fort après cette première passe.

---

## 7. Statut

```text
P1 implémenté et conservé sur les 4 axes (intro, sidebar, barre catalogue, cards).
Aucune facette/logique catalogue modifiée — uniquement habillage + activation
d'un variant natif Odoo (filmstrip pills) + affichage d'une donnée déjà calculée
(search_count). Vérifications machine toutes au vert. GO MOA en attente de
votre lecture des captures avant/après.
```
