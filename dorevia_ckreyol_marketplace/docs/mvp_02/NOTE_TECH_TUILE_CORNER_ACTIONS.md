# Note technique développeur — Rail wishlist + info (tuile `/shop`)

## Contexte

Sur la tuile produit `/shop`, le rendu wishlist / info était perturbé par des couches CSS héritées (thème **Classic Store**, ordre des assets, cache). Un pseudo-élément `::before { content: "i" }` pouvait doubler le glyphe alors que la wishlist restait calée par des règles `position: absolute` héritées.

## Solution retenue

| Élément | Fichier | Rôle |
|--------|---------|------|
| Rail unique | [`views/pages/ckr_shop_classic_tile_restore.xml`](../../views/pages/ckr_shop_classic_tile_restore.xml) | Gabarit **`ckr_shop_wishlist_on_product_media`** : conteneur `ckr-product-card__media-corner` → `o_wsale_product_btn wishlist-above-title` + **`ckr-product-card__corner-actions`** regroupant wishlist + bouton info (+ panneau **`ckr-product-card__details-body`**). |
| Wishlist Odoo | idem | Un bouton : classes **`o_add_wishlist`** + **`ckr-wishlist-ghost`** ; `data-action="o_wishlist"`, ids produit ; états `btn-light` / `btn-danger o_in_wishlist` ; glyphe **`fa fa-heart`**. |
| Info | idem | `button.ckr-product-card__info-action` + `i.fa.fa-info.ckr-product-card__info-icon`. |
| Styles défensifs | idem | Inline sur le rail et les boutons pour le **halo rectangulaire** commun malgré les anciennes règles / cache. |
| Neutralisation `::before` / `::after` | [`views/pages/ckr_shop.xml`](../../views/pages/ckr_shop.xml) (`ckr_shop_page_scope`) | Bloc `<style id="ckr_shop_corner_actions_style">` sur `#wrap.o_wsale_products_page` ciblant `.ckr-product-card__corner-actions > .ckr-product-card__info-action::before/::after` (`content: none`). |
| Présentation pérenne | [`static/src/scss/layout/_shop.scss`](../../static/src/scss/layout/_shop.scss) | Règles sous `.ckr-shop`, `#wrap.o_wsale_products_page.ckr-shop`, et blocs globaux `.ckr-product-card__corner-actions` / `.ckr-product-card__info-action` (sans `::before` texte — icône FontAwesome uniquement). |

## Tests

- Tag : `dorevia_ckr_shop_wave1` — voir [`tests/test_ckr_shop_wave1.py`](../../tests/test_ckr_shop_wave1.py) (`test_shop_product_tiles_expose_corner_info_action`).

## Validation architecte (palier actuel)

Retour **positif** : la solution respecte les contraintes Odoo et répond au besoin immédiat, avec une **dette CSS acceptée et localisée** (inline + correctifs page volontairement pragmatiques).

### À conserver

- Rail unique **`ckr-product-card__corner-actions`** (abstraction UI : deux actions de coin sur une même zone, pas deux positionnements concurrents).
- Comportement **wishlist natif** : `o_add_wishlist`, `data-action="o_wishlist"`, identifiants produit, classes d’état Odoo (`btn-light` / `btn-danger o_in_wishlist`) — pas de réimplémentation métier.
- Icônes **FontAwesome** explicites (`fa-heart`, `fa-info` / `ckr-product-card__info-icon`) — sortie de l’ambiguïté des anciens pseudo-éléments.
- Absence de **« Pour info »** dans le corps de carte ; information secondaire **via l’icône info** uniquement.
- Neutralisation page du **`i` fantôme** (`ckr_shop.xml`) : correctif défensif face au CSS hérité, sans rouvrir toute la chaîne SCSS en urgence.

### Dette technique (ticket de nettoyage futur)

| Piste | Détail |
|-------|--------|
| Pseudo-éléments | Finaliser la suppression de toute logique résiduelle `::before` / `::after` sur `.ckr-product-card__info-action` si des branches SCSS en rajoutent ; l’icône reste la source de vérité. |
| Inline QWeb | Retirer **progressivement** les styles inline sur le rail et les boutons une fois la cascade validée sur tous les environnements. |
| Centralisation | Rapatrier la **présentation complète** du rail dans [`_shop.scss`](../../static/src/scss/layout/_shop.scss). |
| Recette | Vérifier le rail après **rebuild complet** des assets (`web.assets_frontend`) et sur thème chargé en dernier. |

Les styles inline restent **validés comme mesure transitoire** de stabilisation, pas comme cible long terme.

## Évolutions possibles

- Exécuter le ticket de nettoyage ci-dessus lors d’une itération dédiée (réduction dette, pas de régression wishlist / info).
