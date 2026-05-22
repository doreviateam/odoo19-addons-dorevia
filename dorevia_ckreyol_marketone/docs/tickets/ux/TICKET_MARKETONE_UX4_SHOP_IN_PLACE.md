# TICKET — UX-4 — Boutique continue / Shop-in-place interactions

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_UX4_SHOP_IN_PLACE` |
| **Type** | **UX** — extension légère `website_sale` / `website_sale_wishlist` |
| **Statut** | **Lot 1 clôturé GO avec réserve documentaire** · **Lot 2 en cours** · Lot 3 gelé |
| **Version livrée Lot 1** | **`19.0.15.11.1`** |
| **Version cible Lot 2** | **`19.0.15.12.0`** |
| **Branche Lot 2** | `feat/marketone-ux4-lot2-cart-in-place` |
| **PR Lot 1** | **#12** — mergée |
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079/shop |
| **Branche Lot 1** | `feat/marketone-ux4-lot1-wishlist-toggle` |
| **Prérequis** | `main` **≥ `19.0.15.10.3`** (wishlist standard GO MOA) |

---

## Doctrine UX MOA

**`/shop` devient la surface principale d’exploration et d’achat.**

Les CTA de **premier niveau** (Voir, Panier, Wishlist depuis la carte produit) ne doivent **pas** éjecter l’utilisateur de son contexte de navigation.

Les pages **fiche produit**, **panier** et **wishlist** restent accessibles, mais comme **destinations secondaires volontaires** — non imposées par les CTA primaires.

### Doctrine de prudence

- **Encapsuler** le standard Odoo — ne pas le remplacer.
- Ne pas transformer `/shop` en mini-application e-commerce complète trop tôt.
- **Pas de popup modale** pour la preview produit (Lot 3).
- Extension **légère** : JS minimal, QWeb ciblé, SCSS scopé `.marketone-shop`.

### Arbitrage MOA Lot 3 (gelé pour l’instant)

| Zone | Comportement |
|------|--------------|
| **CTA « Voir »** | Déclencheur preview in-page (Lot 3 — P2) |
| **Photo + titre** | **Inchangés** — liens secondaires vers fiche produit complète |
| **Header panier / wishlist** | Destinations secondaires acceptables |

---

## Contexte technique (analyse validée MOA)

Le chantier **ne part pas de zéro** :

| Interaction | Standard Odoo | Écart UX-4 |
|-------------|---------------|------------|
| Wishlist grille | AJAX `/shop/wishlist/add` | Toggle retrait + feedback carte |
| Panier grille | AJAX `/shop/cart/update_json` (mode `stay`) | Feedback carte « Ajouté » |
| CTA Voir | Lien `product_href` | Preview non modale (Lot 3) |
| Photo / titre | Lien fiche | **Gel MOA** — pas de changement |

**Références recette antérieures :**

- [`RECETTE_VISUELLE_WISHLIST_STANDARD.md`](../recette/RECETTE_VISUELLE_WISHLIST_STANDARD.md) — GO MOA `15.10.3`
- [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md) — B1–B6
- [`RECETTE_MANUELLE_SHOP_CONVERSION_TILE.md`](../recette/boutique/RECETTE_MANUELLE_SHOP_CONVERSION_TILE.md)
- [`RECETTE_MANUELLE_SHOP_UX1_ETAT_FILTRES.md`](../recette/ux/RECETTE_MANUELLE_SHOP_UX1_ETAT_FILTRES.md)
- [`RECETTE_MANUELLE_SHOP_UX2_SIDEBAR.md`](../recette/ux/RECETTE_MANUELLE_SHOP_UX2_SIDEBAR.md)

**Recette UX-4 dédiée :** [`RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md`](../recette/ux/RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md)

---

## Découpage en lots

### Lot 1 — Wishlist toggle sans sortie + feedback carte · **P1 · CLÔTURÉ GO avec réserve**

| Élément | Détail |
|---------|--------|
| **Objectif** | Second clic = retrait wishlist depuis `/shop`, sans navigation |
| **Standard** | Routes `/shop/wishlist/add` + nouvelle `/shop/wishlist/remove_by_product` |
| **JS** | Interaction Odoo 19 `marketone_shop_wishlist_toggle.js` — toggle grille |
| **QWeb** | `product._is_in_wishlist()` · retrait `disabled` · `t-nocache` |
| **SCSS** | `.marketone-shop-card--in-wishlist` · cœur terracotta persistant |
| **Tests** | Tag `dorevia_marketone_shop_in_place` |
| **Recette** | § Lot 1 [`RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md`](../recette/ux/RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md) |

**Critère GO Lot 1 :**

- [x] Clic cœur : ajout AJAX · URL reste `/shop`
- [x] Second clic : retrait AJAX · cœur retour repos · compteur header synchronisé
- [x] Cœur retenu terracotta `#C4715A`
- [x] Feedback carte discret (bordure / état `.marketone-shop-card--in-wishlist`)
- [x] Régression B1–B6 + wishlist W1–W4 OK
- [x] Tests auto verts (79/79)

**Verdict MOA (2026-05-22) :** **GO avec réserve documentaire** — visiteur public validé · scénario connecté non rejoué (compte test absent). Rapport : [`RAPPORT_RECETTE_SHOP_UX4_IN_PLACE_20260522.md`](../recette/ux/RAPPORT_RECETTE_SHOP_UX4_IN_PLACE_20260522.md).

---

### Lot 2 — Ajout panier sans sortie + feedback carte · **P1 · EN COURS**

| Élément | Détail |
|---------|--------|
| **Objectif** | Feedback local carte après add-to-cart sans quitter `/shop` |
| **Standard** | Service `cart` Odoo 19 · `/shop/cart/add` · mode `stay` |
| **JS** | Interaction `marketone_shop_cart_add.js` — grille `.marketone-shop-card-cart` |
| **QWeb** | Feedback « Ajouté au panier » · lien « Voir le panier » · retrait `a-submit` |
| **SCSS** | `.marketone-shop-card--added-to-cart` · bandeau feedback |
| **Tests** | Tag `dorevia_marketone_shop_in_place` |
| **Recette** | § Lot 2 recette UX-4 |

**Critère GO Lot 2 :**

- [ ] Ajout panier depuis grille sans navigation
- [ ] État carte visible · lien secondaire panier
- [ ] Régression conversion tile + B8

---

### Lot 3 — Voir sans sortie / preview in-page · **P2 · GELÉ**

| Élément | Détail |
|---------|--------|
| **Objectif** | CTA « Voir » ouvre preview non modale |
| **Desktop** | Panneau latéral (offcanvas end, non modal) |
| **Mobile** | Bloc détail intégré / accordéon sous tuile |
| **Route** | `/shop/product/preview/<template>` (à créer) |
| **Lien secondaire** | « Voir la fiche complète » → `product_href` |
| **Gel MOA** | Photo + titre restent liens fiche produit |
| **Recette** | § Lot 3 recette UX-4 |

**Ne pas lancer** avant arbitrage MOA spécifique Lot 3.

---

### Lot 4 — Recette visuelle + régression boutique · **Continu**

| Élément | Détail |
|---------|--------|
| **Objectif** | Prouver nouveau comportement **et** non-régression |
| **Fréquence** | **À chaque jalon** (Lots 1, 2, 3) — pas seulement en fin de chantier |
| **Référence** | Mise à jour [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md) — critères B7–B10 |
| **Doctrine** | Aucun lot clôturable sans section recette associée |

---

## Périmètre global

### In

| Zone | Détail |
|------|--------|
| Grille `/shop` | CTA carte : Voir · Panier · Wishlist |
| Header | Compteurs panier / wishlist (destinations secondaires OK) |
| Assets | Interaction `marketone_shop_wishlist_toggle.js` · SCSS · QWeb tuile + preview (Lot 3) |
| Contrôleur | Extension wishlist · preview produit (Lot 3) |
| Tests | Tags `dorevia_marketone_shop_in_place` + régression existants |
| Recettes | UX-4 + référence boutique |

### Hors périmètre

| Hors scope | Note |
|------------|------|
| Logique métier wishlist / panier custom | Standard Odoo uniquement |
| Modèles Python dédiés | Interdit |
| Modales popup preview | Interdit MOA |
| Changement photo / titre grille | Gel Lot 3 |
| Refonte fiche produit / page wishlist | Destinations secondaires |
| Connecté / fusion session | Réserve documentaire (comme wishlist P3–P6) |

---

## Architecture légère (vue d’ensemble)

```text
views/pages/shop_product_tile_conversion.xml   → CTA carte (QWeb)
views/pages/shop_product_preview.xml           → Lot 3 — panneau preview
static/src/interactions/marketone_shop_wishlist_toggle.js → Lot 1
static/src/interactions/marketone_shop_cart_add.js      → Lot 2
static/src/scss/_shop_product_cards.scss       → feedback carte
static/src/scss/_shop_product_preview.scss     → Lot 3
controllers/website_sale_wishlist.py           → remove_by_product (Lot 1)
controllers/website_sale.py                    → preview route (Lot 3)
tests/test_marketone_shop_in_place.py          → Lot 1+
```

### Routes

| Route | Lot | Rôle |
|-------|-----|------|
| `/shop/wishlist/add` | — | Standard Odoo |
| `/shop/wishlist/remove_by_product` | 1 | Toggle grille |
| `/shop/cart/add` | 2 | Standard Odoo (stay) |
| `/shop/product/preview/<id>` | 3 | Fragment HTML preview |

---

## Risques et mitigations

| Risque | Niveau | Mitigation |
|--------|--------|------------|
| Régression wishlist GO MOA | Élevé | Recette wishlist + B5 + tests |
| Régression conversion tile | Élevé | B4 · recette conversion tile |
| Régression UX-1 / UX-2 | Moyen | B2 · B3 à chaque lot |
| Variantes produits (panier / preview) | Moyen | Lot 2 : standard Odoo · Lot 3 : sélecteur ou lien fiche |
| SEO (photo/titre) | Faible | Gel MOA — liens fiche conservés |

---

## Critères GO MOA chantier complet (UX-4)

| # | Critère |
|---|---------|
| G1 | Découvrir, comparer, retenir et commencer l’achat depuis `/shop` sans rupture de contexte |
| G2 | CTA premier niveau : pas de navigation forcée |
| G3 | Destinations longues accessibles en liens secondaires |
| G4 | Standard Odoo préservé — extension légère documentée |
| G5 | Recette UX-4 + référence B7–B10 validées à chaque lot |
| G6 | Tests auto régression verts |

---

## Commande tests (Lot 1)

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf -d ckr-marketone-01 \
  -u dorevia_ckreyol_marketone --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_shop_in_place,dorevia_marketone_shop_wishlist,dorevia_marketone_shop_regression,dorevia_marketone_shop_filter_state,dorevia_marketone_shop_sidebar,dorevia_marketone_shop_sidebar_collections,dorevia_marketone_smoke,dorevia_marketone_lot3_shop \
  --http-port=8073
```

---

## Historique

| Date | Version | Lot | Verdict |
|------|---------|-----|---------|
| 2026-05-20 | — | Analyse technique | Validée MOA |
| 2026-05-22 | `19.0.15.11.1` | Lot 1 | **GO avec réserve documentaire** · PR #12 mergée |
| 2026-05-22 | `19.0.15.12.0` | Lot 2 | Implémenté — recette L2 pending |

**Correctif `11.1` (post NO GO recette) :** Odoo 19 utilise l’API `Interaction` (`add_product_to_wishlist_button.js`), pas `publicWidget.ProductWishlist`. Migration vers `marketone_shop_wishlist_toggle.js` · retrait `o_add_wishlist` sur grille · route `remove_by_product` en `jsonrpc`.
