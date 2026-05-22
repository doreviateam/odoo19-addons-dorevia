# Rapport recette — UX-4 Lot 1 — Wishlist toggle in-place

| Champ | Valeur |
|-------|--------|
| Recette | `RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md` |
| Lot | UX-4 Lot 1 — Wishlist toggle sans sortie |
| Version cible | `19.0.15.11.0` |
| Branche | `feat/marketone-ux4-lot1-wishlist-toggle` |
| Base | `ckr-marketone-01` |
| URL | http://localhost:18079/shop |
| Date | 2026-05-22 |
| Exécuteur | Codex |

## Verdict

**NO GO Lot 1** (recette initiale sur `19.0.15.11.0`).

Les tests automatisés sont verts et l'ajout wishlist depuis `/shop` ne provoque plus de navigation vers la fiche produit. En revanche, le scénario manuel prioritaire échoue sur le toggle complet : le retrait par second clic depuis `/shop` ne fonctionne pas de manière fiable.

### Correctif Dev `19.0.15.11.1` (2026-05-22)

**Cause racine :** Odoo 19 utilise l'API `Interaction` (`add_product_to_wishlist_button.js`), pas `publicWidget.ProductWishlist`. Le handler standard est add-only et appelle `updateDisabled(el, true)` — comportement observé en recette.

**Correctif :** Interaction `marketone_shop_wishlist_toggle.js` · retrait `o_add_wishlist` sur bouton grille · route `/shop/wishlist/remove_by_product` en `jsonrpc`.

**Action MOA :** rejouer § L1 sur version **`19.0.15.11.1`** (PR #12 mise à jour).

## Pré-contrôle

| Contrôle | Attendu | Observé | Statut |
|----------|---------|---------|--------|
| Branche active | `feat/marketone-ux4-lot1-wishlist-toggle` | `feat/marketone-ux4-lot1-wishlist-toggle` | OK |
| Version module | `19.0.15.11.0` | `19.0.15.11.0` | OK |
| Base | `ckr-marketone-01` | `ckr-marketone-01` | OK |
| URL | `/shop` | `/shop` | OK |

## Tests automatisés

Commande exécutée :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf -d ckr-marketone-01 \
  -u dorevia_ckreyol_marketone --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_shop_in_place,dorevia_marketone_shop_wishlist,dorevia_marketone_shop_regression,dorevia_marketone_shop_filter_state,dorevia_marketone_shop_sidebar,dorevia_marketone_shop_sidebar_collections,dorevia_marketone_smoke,dorevia_marketone_lot3_shop \
  --http-port=8073
```

Résultat : **79 tests, 0 failed, 0 error(s)**.

Tests UX-4 observés dans la sortie :

- `test_no_duplicate_grid_wishlist_button`
- `test_shop_grid_wishlist_uses_is_in_wishlist`
- `test_shop_stays_on_shop_after_wishlist_json_ops`
- `test_wishlist_toggle_add_remove_json`

## Warnings observés

| Warning | Statut recette |
|---------|----------------|
| `@route(type='json')` déprécié, attendu `jsonrpc` en Odoo 19 | À traiter tech, non bloquant recette visuelle |
| `Error-prone use of @class` sur sidebar desktop | Warning existant, hors UX-4 Lot 1 |
| `Unknown directives or unused attributes: {'t-nocache-product_template_id', 't-nocache'} in 1808` | À investiguer : apparu pendant rendu `/shop`, potentiellement lié au rendu wishlist par carte |

## Scénario visiteur public L1

| Étape | Attendu | Observé | Verdict |
|-------|---------|---------|---------|
| L1.0 | Pas d'erreur JS rouge au chargement | Logs navigateur vides | OK |
| L1.1 | `/shop` 200, grille visible | OK | OK |
| L1.2 | URL `/shop`, compteur visible | OK | OK |
| L1.3 | 1er clic coeur : pas de navigation | URL reste `/shop` | OK |
| L1.4 | Coeur plein terracotta + carte retenue | Partiellement OK sur certains produits ; un produit ajouté reste `disabled` sans état `o_in_wishlist` | KO |
| L1.5 | Compteur header +1 | OK (`4 → 5` sur le produit testé) | OK |
| L1.6 | Second clic même coeur : retrait wishlist | KO : le bouton reste actif ou `disabled`, retrait non prouvé depuis `/shop` | KO |
| L1.7 | Coeur retour repos | KO | KO |
| L1.8 | Compteur header -1 | KO : compteur reste inchangé sur le retrait testé | KO |
| L1.9 | Répéter sur 2e produit | Ajout in-place observé, retrait non validé | KO |
| L1.10 | Clic `Voir` ou titre | Navigation fiche autorisée | OK |

## Détail technique constaté côté DOM

### Ajout in-place

Produit testé : `productProductId=154`.

Avant clic :

```text
title="Ajouter à la liste"
aria-label="Ajouter à la liste"
aria-pressed="false"
class="marketone-shop-card-wishlist btn o_add_wishlist"
compteur header=4
url=/shop
```

Après clic :

```text
url=/shop
compteur header=5
class="marketone-shop-card-wishlist btn o_add_wishlist disabled"
title="Ajouter à la liste"
aria-label="Ajouter à la liste"
aria-pressed="false"
```

Conclusion : l'ajout côté compteur/session est effectif, mais l'état du bouton ne bascule pas correctement vers `Retirer de la liste` / `o_in_wishlist` pour ce produit, ce qui empêche le second clic attendu.

### Retrait in-place

Produit actif testé : `productProductId=153`.

Avant clic :

```text
title="Retirer de la liste"
aria-pressed="true"
class="marketone-shop-card-wishlist btn o_add_wishlist o_in_wishlist is-active"
compteur header=5
url=/shop
```

Après clic :

```text
url=/shop
compteur header=5
title="Retirer de la liste"
aria-pressed="true"
class inchangée
```

Conclusion : le second clic ne retire pas l'article depuis `/shop`.

## Régression référence

| Section | Contrôle | Verdict | Notes |
|---------|----------|---------|-------|
| B1 | Smoke `/shop`, `/shop/cart`, `/shop/wishlist`, fiche produit | OK tests auto | Navigateur `/shop` OK |
| B4 | Cards : structure, Voir, prix, coeur, panier | Partiel | Structure OK ; toggle coeur KO |
| B5 | Wishlist header, pas de doublon card | Partiel | Pas de doublon ; compteur add OK ; remove KO |
| B6 | Mobile 375 px, offcanvas ordre | OK | Pas de débordement, ordre Catégories → Collections → Origines → Prix |
| B7 | Toggle wishlist sans sortie `/shop` | **KO** | Add sans sortie OK ; remove sans sortie KO |
| W1 | Un seul bouton wishlist par card | OK | Pas de doublon observé |
| W2 | Repos / hover / retenu / retrait | **KO** | Retenu/retrait non fiable |
| W3 | Extension légère standard Odoo | À confirmer tech | Présence contrôleur JSON dédié observée dans les warnings |
| W4 | Fiche produit wishlist secondaire | OK | Non-régression observée |

## Captures

### `/shop` desktop — état retenu / compteur

![UX4 retenu](/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ckreyol_marketone/docs/recette/ux/capture_ux4_l1_shop_desktop_retenu_20260522.png)

### `/shop` mobile

![UX4 mobile](/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ckreyol_marketone/docs/recette/ux/capture_ux4_l1_shop_mobile_20260522.png)

### Mobile offcanvas

![UX4 mobile filters](/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ckreyol_marketone/docs/recette/ux/capture_ux4_l1_mobile_filters_20260522.png)

## Signal Dev proposé

```text
NO GO UX-4 Lot 1.
Tests auto 79/79 OK, mais recette navigateur KO :
- ajout wishlist depuis /shop reste bien sur /shop et compteur +1 ;
- le bouton ajouté peut rester disabled sans basculer en o_in_wishlist / Retirer de la liste ;
- second clic sur coeur actif depuis /shop ne retire pas l'article, compteur inchangé.
Bloquant : L1.6–L1.8 / B7 / W2.
```
