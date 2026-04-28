# Note technique développeur — Pied de tuile produit `/shop`

**Objet**  
Correction du footer de la tuile produit sur `/shop` pour obtenir un rendu stable ; complété par le **Nom CK** et, sur la **média**, le **rail wishlist + info** (information secondaire par **icône `fa-info`**, plus de **« Pour info »** / `<details>` dans le corps ou le pied) — [SPEC_CK_NOM_CK_TUILE_PRODUIT.md](SPEC_CK_NOM_CK_TUILE_PRODUIT.md), [NOTE_TECH_TUILE_CORNER_ACTIONS.md](NOTE_TECH_TUILE_CORNER_ACTIONS.md) :

- prix à gauche ;
- CTA à droite ;
- même ligne horizontale ;
- compatibilité avec les wrappers Odoo `website_sale`.

## Problème rencontré

Le footer de la carte n’était pas composé d’éléments HTML simples. Odoo injecte :

- le prix via `t-out="product_price"` ;
- les actions via `t-call="website_sale.shop_product_buttons"`.

Ces sorties ajoutent leurs propres wrappers et comportements CSS, notamment sur :

- `.o_wsale_product_sub` ;
- `.o_wsale_product_btn` ;
- `.o_wsale_product_action_row`.

Résultat :

- empilements verticaux non voulus ;
- alignements incohérents ;
- ordre visuel qui ne suivait pas toujours l’intention CSS ;
- comportements instables à cause de wrappers hérités du thème / d’Odoo.

## Principe du correctif

Le footer a été reconstruit comme un sous-bloc autonome, avec un layout déterministe, au lieu de dépendre du comportement par défaut de `website_sale`.

## Implémentation

### 1. Structure QWeb

Fichier : [`views/pages/ckr_shop_classic_tile_restore.xml`](../../views/pages/ckr_shop_classic_tile_restore.xml).

Structure retenue :

- `.ckr-product-card__footer`
- `.ckr-product-card__footer-row`
- `.ckr-product-card__footer-price`
- `.ckr-product-card__footer-cta`

### 2. Ordre DOM

Le prix est rendu **avant** le CTA dans le HTML, ce qui évite de dépendre d’un simple réordonnancement CSS.

Ordre final : prix → CTA.

### 3. Grille deux colonnes

Fichier : [`static/src/scss/layout/_shop.scss`](../../static/src/scss/layout/_shop.scss) (bloc `.o_wsale_product_sub.ckr-product-card__footer`).

Layout retenu :

- `display: grid` ;
- `grid-template-columns: minmax(0, 1fr) max-content`.

Effet recherché :

- colonne 1 : le prix prend l’espace disponible ;
- colonne 2 : le CTA garde sa largeur naturelle ;
- alignement stable même avec les wrappers injectés par Odoo.

Des styles **inline** sur la rangée / colonnes dans le QWeb sécurisent le rendu face à la cascade du thème ; une remise au propre vers le SCSS seulement est possible après validation que la cascade finale reste stable.

### 4. Neutralisation des comportements hérités Odoo (actions)

Surcharges sur (dans le scope du pied carte) :

- `.o_wsale_product_btn` ;
- `.o_wsale_product_action_row` ;
- `.o_wsale_product_btn_primary.ckr-product-card__cart-btn`.

Objectif :

- supprimer les effets de positionnement hérités ;
- empêcher les retours à la ligne parasites ;
- conserver un bouton de largeur naturelle ;
- garder le CTA dans le flux normal.

Points clés typiques : `position: static`, `float: none`, `width: auto`, `max-width: none` où pertinent, `display: flex` / `inline-flex`.

### 5. Stabilisation du rendu prix

Le bloc prix est forcé pour :

- rester sur une seule ligne (y compris promo avec prix barré) ;
- garder un alignement horizontal cohérent.

## Cascade `#o_wsale_products_grid`

La règle globale `display: contents !important` sur `.o_wsale_product_action_row` (grille produits) **ne s’applique pas** au pied CK : sélecteur  
`.o_wsale_product_sub:not(.ckr-product-card__footer)`  
afin que le pied conserve `inline-flex` sur la rangée d’action et ne soit pas écrasé par la spécificité du `#id`.

## Pourquoi ce choix

Un simple flex sur le footer n’était pas suffisamment robuste à cause des wrappers générés par `website_sale`. La combinaison retenue :

- DOM dans le bon ordre ;
- grille 2 colonnes ;
- neutralisation des wrappers Odoo ;

est celle qui a donné le comportement le plus stable.

## Résultat attendu

Sur la tuile produit :

- prix à gauche ;
- CTA à droite ;
- une seule ligne basse ;
- plus d’empilement vertical intempestif ;
- comportement stable malgré `product_price` et `shop_product_buttons` injectés par Odoo.

## Nom CK et information secondaire (liste `/shop`) — état actuel

- **Champ** : `product.template.ck_product_name` (libellé BO **Nom CK**) — surcharge éditoriale **uniquement** pour l’affichage tuile ; `name` reste la référence interne.
- **Titre** : `(ck_product_name or '').strip() or name` (+ libellé de variante si présent).
- **Information secondaire** : plus de **`<details>` « Pour info »** dans le pied ou sous le titre. Le contenu (méta, nom Odoo, ligne descriptive) est dans un **panneau** ouvert au survol / focus du bouton **info** (`fa-info`), regroupé avec la **wishlist** dans le rail **`ckr-product-card__corner-actions`** sur la **média**. Comportement wishlist **natif Odoo** conservé (`o_add_wishlist`, `data-action`, ids produit). Détail : [NOTE_TECH_TUILE_CORNER_ACTIONS.md](NOTE_TECH_TUILE_CORNER_ACTIONS.md).

### Historique (19.0.1.10.53–10.54)

- **Drill-down** : élément HTML **`<details>`** avec **`<summary>Pour info</summary>`** ; corps = méta catalogue (`_ckr_get_shop_tile_meta_line`), nom Odoo + variante, puis ligne descriptive. **Rendu retail (10.54)** : bloc rendu **dans le pied carte** (sous le filet du titre).
- **Masquage** : si `_ckr_shop_tile_has_more_block` était faux, le `<details>` n’était pas rendu.

## Média, rubans et wishlist (liste `/shop`)

Hors du pied carte, la tuile **`ckr_shop_classic_tile_restore`** et **`static/src/scss/layout/_shop.scss`** positionnent :

- **Wishlist + info** : rail **`ckr-product-card__corner-actions`** — bouton wishlist **unique** avec classes Odoo **`o_add_wishlist`** + présentation CK **`ckr-wishlist-ghost`** (même élément que dans le QWeb), à côté du bouton info **`ckr-product-card__info-action`** / **`fa-info`** ; **coin image** ; nécessite le module **`website_sale_wishlist`** pour un bouton wishlist fonctionnel (**MOA-1** : pas de bouton factice). Gabarit : **`ckr_shop_wishlist_on_product_media`** dans `ckr_shop_classic_tile_restore.xml`.
- **Rubans** (`product.ribbon` → `.o_wsale_ribbon`) : classes explicites **`o_left`** et **`o_right`**, rotation, `z-index`, et garde-fous **`overflow`** sur le média pour éviter la découpe des rubans et séparer visuellement ruban gauche / coin actions droite.

Détail maquette vs code : [SHOP_MAQUETTE_ECARTS.md §5](SHOP_MAQUETTE_ECARTS.md).

## Références

- [SHOP_COMPONENT_CONTRACTS.md](SHOP_COMPONENT_CONTRACTS.md) — contrat « Carte produit V1 » ;
- [2_SHOP.md §7](2_SHOP.md) — canon carte V1 ;
- [SHOP_MAQUETTE_ECARTS.md §5](SHOP_MAQUETTE_ECARTS.md) — synthèse maquette vs livré.
- [SPEC_CK_NOM_CK_TUILE_PRODUIT.md](SPEC_CK_NOM_CK_TUILE_PRODUIT.md) — Nom CK + information secondaire (panneau info) ;
- [NOTE_TECH_TUILE_CORNER_ACTIONS.md](NOTE_TECH_TUILE_CORNER_ACTIONS.md) — rail coin média (wishlist native + `fa-info`).
