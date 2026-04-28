# Spécification — Nom CK et information secondaire sur la tuile produit

> **Titre historique du fichier** : « Nom CK et drill-down « Pour info » » — le libellé **« Pour info »** et le pattern **`<details>`** décrivent une **phase d’implémentation** (≈ **19.0.1.10.53–10.54**). La **décision actuelle** est l’**icône info** dans le **rail coin média** (wishlist + info) ; voir [NOTE_TECH_TUILE_CORNER_ACTIONS.md](NOTE_TECH_TUILE_CORNER_ACTIONS.md).

| Champ | Valeur |
|--------|--------|
| **Statut** | **Livrée** — champ BO **Nom CK** + tuile `/shop` ; **information secondaire** : rail **`ckr-product-card__corner-actions`** (bouton **`fa-info`**, panneau tooltip) depuis **≈ 19.0.1.10.55+** (affinements **10.6x** : wishlist native, halo commun, nettoyage pseudo-éléments). **Historique** : **10.54** = filet sous titre + ancien **« Pour info »** en pied ; **10.53** = intro Nom CK + `<details>`. Fiche produit détaillée et SEO **hors périmètre** (spec source §8). |
| **Source** | Spécification MOA intégrée au dépôt le **2026-04-26**. |

## Synthèse (décision actuelle)

- **Objectif** : titre boutique **sobre** (`ck_product_name` ou repli `name`) ; **méta**, **nom Odoo** et **ligne descriptive** accessibles **à la demande** via le bouton **info** (`fa-info`) dans le **même rail visuel** que la **wishlist** (`ckr-product-card__corner-actions` sur la média) — **pas** de libellé « Pour info » dans le corps de carte, **pas** de `<details>` dans le pied.
- **Backend** : inchangé — `product.template.ck_product_name` (**Nom CK**), onglet **Ventes** / e-commerce, **avant** `public_categ_ids` — vue `product_template_ck_product_name_views.xml`.
- **Front** : `views/pages/ckr_shop_classic_tile_restore.xml` ; `layout/_shop.scss` ; neutralisation défensive `ckr_shop.xml` (`ckr_shop_corner_actions_style`) si besoin. Détail technique et validation architecte : [NOTE_TECH_TUILE_CORNER_ACTIONS.md](NOTE_TECH_TUILE_CORNER_ACTIONS.md).
- **Contenu du panneau info** : même **source de données** qu’historiquement — méta `_ckr_get_shop_tile_meta_line`, `name` (+ variante), `_ckr_get_shop_tile_description_line()` ou `_ckr_get_shop_tile_subtitle()` (voir § Règles). `_ckr_shop_tile_has_more_block` continue de qualifier l’**utilité** du bloc côté métier ; le rendu **liste /shop** affiche le rail (wishlist + info) pour les tuiles concernées selon QWeb (page wishlist : voir note corner).

## Historique d’implémentation (à conserver pour la traçabilité)

- **19.0.1.10.53–10.54** : information secondaire sous forme de **`<details>`** avec résumé libellé **« Pour info »** (corps = méta, nom Odoo, ligne desc.) ; **10.54** : déplacement du bloc dans le **pied** carte (sous le filet titre), flux principal **image → nom (2 lignes) → filet → prix \| CTA**.
- **Affichage conditionnel (époque `<details>`)** : si `_ckr_shop_tile_has_more_block` était faux, le `<details>` n’était pas rendu (évite doublon vide). Le comportement exact après passage au rail est documenté dans [NOTE_TECH_TUILE_CORNER_ACTIONS.md](NOTE_TECH_TUILE_CORNER_ACTIONS.md).

## Règles (rappel) — contenu métier du panneau

1. **Nom principal** : `(ck_product_name or '').strip() or name` (+ variante si applicable).
2. **Panneau information secondaire** : méta `_ckr_get_shop_tile_meta_line` ; `name` (+ variante) ; troisième ligne = `_ckr_get_shop_tile_description_line()` ou repli `_ckr_get_shop_tile_subtitle()`.
3. **Hors périmètre** : ne pas modifier `name` pour les documents ; pas de changement fiche produit / SEO / routes (cf. spec source §8).

## Références code

- `models/product_template.py` — `ck_product_name`, `_ckr_shop_tile_has_more_block`
- `views/product_template_ck_product_name_views.xml`
- `views/pages/ckr_shop_classic_tile_restore.xml` — gabarit **`ckr_shop_wishlist_on_product_media`** (rail coin : wishlist + info + corps **`ckr-product-card__details-body`**)
- `tests/test_ckr_product_tile_name.py` (`dorevia_ckr_tile_name`)
- `tests/test_ckr_shop_wave1.py` (`dorevia_ckr_shop_wave1`) — invariants rail coin

## Document source (exigences détaillées)

Les sections 1 à 11 de la spec d’origine (objectif, contexte, critères d’acceptation, intention UX) restent valides ; elles ne sont pas recopiées ici pour éviter la duplication. En cas de divergence sur le **comportement actuel**, **ce fichier** + [NOTE_TECH_TUILE_CORNER_ACTIONS.md](NOTE_TECH_TUILE_CORNER_ACTIONS.md) + le **code** font foi.
