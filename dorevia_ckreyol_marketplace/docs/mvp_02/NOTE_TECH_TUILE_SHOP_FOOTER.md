# Note technique développeur — Pied de tuile produit `/shop`

**Objet**  
Correction du footer de la tuile produit sur `/shop` pour obtenir un rendu stable :

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

## Références

- [SHOP_COMPONENT_CONTRACTS.md](SHOP_COMPONENT_CONTRACTS.md) — contrat « Carte produit V1 » ;
- [2_SHOP.md §7](2_SHOP.md) — canon carte V1 ;
- [SHOP_MAQUETTE_ECARTS.md §5](SHOP_MAQUETTE_ECARTS.md) — synthèse maquette vs livré.
