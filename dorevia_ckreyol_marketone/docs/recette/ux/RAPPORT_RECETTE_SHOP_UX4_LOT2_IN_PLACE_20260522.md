# Rapport recette — UX-4 Lot 2 — Panier in-place

| Champ | Valeur |
|-------|--------|
| Recette | `RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md` |
| Lot | UX-4 Lot 2 — Panier sans sortie |
| Version cible | `19.0.15.12.1` (correctif post NO GO) |
| Branche | `feat/marketone-ux4-lot2-cart-in-place` |
| Base | `ckr-marketone-01` |
| URL | http://localhost:18079/shop |
| Date | 2026-05-22 |
| Exécuteur | Codex |

## Verdict

**NO GO Lot 2** après reprise `19.0.15.12.1`.

Le correctif `19.0.15.12.1` améliore nettement le desktop : le premier clic panier depuis la grille ajoute bien sans quitter `/shop`, sans ouvrir le configurateur, avec compteur header synchronisé (`9 -> 10`).

Deux points restent bloquants pour un GO MOA :

- le feedback carte `Ajouté au panier` reste caché après le clic direct desktop (`hidden`, `display: none`, pas de classe `.marketone-shop-card--added-to-cart`) ;
- en mobile 390 px, le panier de tuile reste non exploitable visuellement et le clic forcé sur le bouton finit sur la fiche produit au lieu de rester sur `/shop`.

Le verdict actif reste donc **NO GO**, mais le diagnostic a changé : le blocage configurateur desktop est corrigé ; les blocages restants sont **feedback carte** et **mobile**.

### Historique première passe `19.0.15.12.0`

Les tests automatisés sont verts et le desktop prouve un chemin fonctionnel après passage par le configurateur Odoo. En revanche, le comportement attendu Lot 2 n'est pas validé de bout en bout :

- le premier clic panier grille desktop ouvre le configurateur Odoo au lieu d'appliquer directement le feedback carte ;
- le feedback carte apparaît après clic secondaire `Ajouter au panier` dans le configurateur ;
- le compteur header desktop est bien synchronisé dans ce chemin (`7 -> 8`) ;
- le lien `Voir le panier` visible dans la carte navigue bien vers `/shop/cart` ;
- en mobile 390 px, le bouton panier grille n'est pas visible/accessibilisé dans la tuile et le clic direct ne déclenche pas l'ajout.

Le point bloquant MOA est donc **L2 mobile** et, en réserve forte, le fait que le parcours desktop nécessite une étape configurateur non explicitée dans la recette Lot 2.

## Pré-contrôle

| Contrôle | Attendu | Observé | Statut |
|----------|---------|---------|--------|
| Branche active | `feat/marketone-ux4-lot2-cart-in-place` | `feat/marketone-ux4-lot2-cart-in-place` | OK |
| Version module | `19.0.15.12.0` | `19.0.15.12.0` | OK |
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

Résultat : **82 tests, 0 failed, 0 error(s)**.

Tests Lot 2 observés :

- `test_cart_add_jsonrpc_adds_product_line`
- `test_shop_grid_cart_uses_marketone_handler`
- `test_shop_stays_on_shop_after_cart_json_add`

## Scénario visiteur public L2

| Étape | Attendu | Observé | Verdict |
|-------|---------|---------|---------|
| L2.1 | Clic panier depuis `/shop`, URL reste `/shop` | URL reste `/shop`, mais ouverture du configurateur Odoo | Réserve forte |
| L2.2 | État `Ajouté au panier` visible sur la carte | Visible après clic `Ajouter au panier` dans le configurateur, pas au premier clic grille | Réserve forte |
| L2.3 | Compteur header +1 | OK dans le chemin configurateur : `7 -> 8` | OK |
| L2.4 | Lien `Voir le panier` sur carte | OK : navigation volontaire vers `/shop/cart` | OK |
| L2.5 | Clic header panier | Navigation `/shop/cart` acceptée ; smoke auto OK | OK |

## Mobile

| Contrôle | Attendu | Observé | Verdict |
|----------|---------|---------|---------|
| Mobile 390 px | Pas de débordement horizontal | OK | OK |
| Bouton panier tuile | Action panier exploitable depuis la grille | KO : bouton non visible/accessibilisé dans la tuile mobile |
| Clic panier mobile | Rester `/shop` + feedback carte | KO : clic direct sur zone panier ne déclenche pas l'ajout ; clic forcé locator a navigué vers fiche produit lors d'une tentative |

## Régression Lot 2

| Section | Contrôle | Verdict | Notes |
|---------|----------|---------|-------|
| B1 | Smoke `/shop`, `/shop/cart`, `/shop/wishlist` | OK | Tests auto + HTTP OK |
| B4 | Cards conversion | Partiel | Desktop OK après configurateur ; mobile panier KO |
| B8 | Panier in-place | **KO** | Mobile non validé ; desktop avec réserve configurateur |
| Conversion tile panier survol | Panier au survol desktop | Partiel | Bouton présent dans DOM ; interaction visible dépendante du survol/configurateur |
| Lot 1 wishlist | Non-régression | OK | Tests auto wishlist toujours verts |

## Warnings observés

| Warning | Statut recette |
|---------|----------------|
| `Error-prone use of @class` sur sidebar desktop | Warning existant, hors UX-4 Lot 2 |
| `Unknown directives or unused attributes: {'t-nocache', 't-nocache-product_template_id'} in 1808` | Warning non bloquant pour ce verdict |

## Captures

### `/shop` desktop avant ajout

![UX4 L2 desktop avant](/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ckreyol_marketone/docs/recette/ux/capture_ux4_l2_shop_desktop_before_20260522.png)

### `/shop` desktop après ajout via configurateur

![UX4 L2 desktop ajouté](/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ckreyol_marketone/docs/recette/ux/capture_ux4_l2_shop_desktop_added_20260522.png)

### Header compteur panier

![UX4 L2 header compteur](/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ckreyol_marketone/docs/recette/ux/capture_ux4_l2_header_compteur_20260522.png)

### Mobile avant ajout

![UX4 L2 mobile avant](/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ckreyol_marketone/docs/recette/ux/capture_ux4_l2_shop_mobile_before_20260522.png)

### Mobile tentative ajout

![UX4 L2 mobile tentative](/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ckreyol_marketone/docs/recette/ux/capture_ux4_l2_shop_mobile_added_20260522.png)

## Signal Dev proposé

```text
NO GO UX-4 Lot 2.
Tests auto 82/82 OK, mais recette navigateur KO/partielle :
- desktop : premier clic panier grille reste sur /shop mais ouvre le configurateur Odoo ; feedback carte et compteur +1 uniquement après clic secondaire dans le configurateur ;
- lien "Voir le panier" OK ;
- mobile 390 px : bouton panier non visible/accessibilisé dans la tuile ; clic direct ne déclenche pas l'ajout in-place.
Bloquant : L2 mobile + clarification attendue sur le rôle du configurateur dans le parcours Lot 2.
```

## Correctif Dev `19.0.15.12.1` (2026-05-22)

**Cause racine desktop :** `cart.add()` avec `isConfigured: false` déclenche `/website_sale/should_show_product_configurator` (produits optionnels ou variante non marquée configurée). Le configurateur s’ouvre avant l’ajout ; le feedback carte n’apparaît qu’après validation dans le dialogue.

**Correctif desktop :** add direct `/shop/cart/add` quand `product_id` est déjà présent dans la tuile · `data-show-quantity="False"` · sync header via `updateCartNavBar`.

**Cause racine mobile :** bouton panier masqué (`opacity: 0` / `pointer-events: none`) hors survol — clic traverse vers le lien photo.

**Correctif mobile :** panier visible et cliquable en `@media (max-width: 768px)` et `(hover: none)`.

**Action MOA :** rejouer § L2 sur version **`19.0.15.12.1`** (PR #13 mise à jour).

## Reprise MOA `19.0.15.12.1` (2026-05-22)

### Pré-contrôle reprise

| Contrôle | Attendu | Observé | Statut |
|----------|---------|---------|--------|
| Branche active | `feat/marketone-ux4-lot2-cart-in-place` | `feat/marketone-ux4-lot2-cart-in-place` | OK |
| Version module | `19.0.15.12.1` | `19.0.15.12.1` | OK |
| Base | `ckr-marketone-01` | `ckr-marketone-01` | OK |
| URL | `/shop` | `/shop` | OK |

### Tests automatisés reprise

Résultat : **82 tests, 0 failed, 0 error(s)**.

### Scénario visiteur public L2 — reprise

| Étape | Attendu | Observé reprise `12.1` | Verdict |
|-------|---------|-------------------------|---------|
| L2.1 | Clic panier depuis `/shop`, URL reste `/shop` | OK : URL reste `/shop`, pas de configurateur | OK |
| L2.2 | État `Ajouté au panier` visible sur la carte | KO : feedback présent dans le DOM mais toujours caché (`hidden`, `display: none`) | KO |
| L2.3 | Compteur header +1 | OK : `9 -> 10` | OK |
| L2.4 | Lien `Voir le panier` sur carte | Non testable en reprise : lien masqué avec le feedback | KO |
| L2.5 | Clic header panier | Navigation `/shop/cart` attendue, smoke auto OK | OK |

### Mobile reprise

| Contrôle | Attendu | Observé reprise `12.1` | Verdict |
|----------|---------|-------------------------|---------|
| Mobile 390 px | Pas de débordement horizontal | OK | OK |
| Bouton panier tuile | Action panier visible/exploitable depuis la grille | KO : bouton présent dans le DOM mais opacity `0` |
| Clic panier mobile | Rester `/shop` + feedback carte | KO : clic forcé locator navigue vers `/shop/maniocookies-sales-la-platine-7` | KO |

### Régression reprise

| Section | Contrôle | Verdict | Notes |
|---------|----------|---------|-------|
| B1 | Smoke `/shop`, `/shop/cart`, `/shop/wishlist` | OK | Tests auto verts |
| B4 | Cards conversion | Partiel | Structure OK ; feedback panier KO |
| B8 | Panier in-place | **KO** | Compteur OK, feedback et mobile KO |
| Lot 1 wishlist | Non-régression | OK | Tests auto wishlist toujours verts |

### Captures reprise `12.1`

![UX4 L2 12.1 desktop avant](/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ckreyol_marketone/docs/recette/ux/capture_ux4_l2_12_1_desktop_before_20260522.png)

![UX4 L2 12.1 desktop après](/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ckreyol_marketone/docs/recette/ux/capture_ux4_l2_12_1_desktop_after_20260522.png)

![UX4 L2 12.1 header](/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ckreyol_marketone/docs/recette/ux/capture_ux4_l2_12_1_header_20260522.png)

![UX4 L2 12.1 mobile avant](/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ckreyol_marketone/docs/recette/ux/capture_ux4_l2_12_1_mobile_before_20260522.png)

![UX4 L2 12.1 mobile après](/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ckreyol_marketone/docs/recette/ux/capture_ux4_l2_12_1_mobile_after_20260522.png)

### Signal Dev reprise proposé

```text
NO GO UX-4 Lot 2 — reprise 19.0.15.12.1.
Tests auto 82/82 OK.
Desktop : progrès confirmé, premier clic panier reste sur /shop, plus de configurateur, compteur header +1.
Bloquants restants :
- feedback carte Ajouté au panier non visible après clic direct (feedback encore hidden/display none, pas de classe card added) ;
- mobile 390 px : bouton panier non exploitable visuellement, clic forcé navigue vers la fiche produit.
L2.2 / L2.4 / mobile restent KO.
```

## Correctif Dev `19.0.15.12.2` (2026-05-22)

**Cause racine feedback desktop :** `wSaleUtils.updateCartNavBar(data)` lève une exception sur `/shop` (`document.querySelector('.oe_cart')` absent) après la mise à jour du compteur header — `setVisualState` jamais atteint.

**Correctif feedback :** sync header via `_syncCartHeader` (copie ciblée de `_updateCartIcon` Odoo) · `setVisualState` systématique après add réussi · renfort CSS classe `--added-to-cart`.

**Cause racine mobile :** Odoo 19 `product_tile.scss` — `@media (max-width: lg)` + `actions_onhover` → `visibility: hidden` + `.btn { opacity: 0; transform: translateY(100%) }` (notre seul `opacity` ne suffisait pas).

**Correctif mobile :** override `< lg` sur `#o_wsale_products_grid.o_wsale_products_opt_actions_onhover` — `visibility` / `opacity` / `transform` / `z-index` / `pointer-events`.

**Action MOA :** rejouer § L2 sur version **`19.0.15.12.2`** (PR #13 mise à jour).
