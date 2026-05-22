# Recette manuelle — UX-4 Boutique continue / Shop-in-place — `/shop`

| Champ | Valeur |
|-------|--------|
| **Ticket** | [`TICKET_MARKETONE_UX4_SHOP_IN_PLACE`](../../tickets/ux/TICKET_MARKETONE_UX4_SHOP_IN_PLACE.md) |
| **Version cible Lot 1** | **`19.0.15.11.0`** |
| **Branche Lot 1** | `feat/marketone-ux4-lot1-wishlist-toggle` |
| **URL** | http://localhost:18079/shop |
| **Base** | `ckr-marketone-01` |
| **Statut recette** | **Lot 1 — à exécuter** · Lots 2–4 — planifiés |

**Régression obligatoire :** [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../REFERENCE_RECETTE_BOUTIQUE_MOA.md)  
**Sections à rejouer selon lot :** voir tableau ci-dessous.

---

## Doctrine recette MOA

Chaque évolution UX-4 doit prouver **deux choses** :

1. le **nouveau comportement** fonctionne ;
2. les **comportements boutique déjà validés** ne régressent pas.

**Aucun lot UX-4 n’est clôturable** sans sa section de recette associée et ses liens vers les recettes déjà validées.

### Références antérieures (non-régression)

| Document | Rôle | Statut |
|----------|------|--------|
| [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../REFERENCE_RECETTE_BOUTIQUE_MOA.md) | Invariants B1–B10 | Actif |
| [`RECETTE_VISUELLE_WISHLIST_STANDARD.md`](../RECETTE_VISUELLE_WISHLIST_STANDARD.md) | Wishlist standard + cosmétique CK | GO MOA `15.10.3` |
| [`RECETTE_MANUELLE_SHOP_CONVERSION_TILE.md`](../boutique/RECETTE_MANUELLE_SHOP_CONVERSION_TILE.md) | Tuile conversion | GO MOA |
| [`RECETTE_MANUELLE_SHOP_UX1_ETAT_FILTRES.md`](RECETTE_MANUELLE_SHOP_UX1_ETAT_FILTRES.md) | Haut grille · chips | GO `9.4` |
| [`RECETTE_MANUELLE_SHOP_UX2_SIDEBAR.md`](RECETTE_MANUELLE_SHOP_UX2_SIDEBAR.md) | Sidebar · offcanvas | GO MOA |
| [`RECETTE_MANUELLE_SHOP_SIDEBAR_ORDRE.md`](../boutique/RECETTE_MANUELLE_SHOP_SIDEBAR_ORDRE.md) | Ordre rubriques | GO |
| [`RAPPORT_RECETTE_WISHLIST_REGRESSION_BOUTIQUE_20260522.md`](../RAPPORT_RECETTE_WISHLIST_REGRESSION_BOUTIQUE_20260522.md) | Dernière régression B1–B6 | GO |

### Matrice recette par lot

| Lot | Sections UX-4 | Régression référence | Tests auto tag |
|-----|---------------|----------------------|----------------|
| **Lot 1** | § L1 | B1 · B4 · B5 · B6 · W1–W4 | `dorevia_marketone_shop_in_place` + wishlist + régression |
| **Lot 2** | § L2 | B1 · B4 · B8 · conversion tile | + smoke lot3 |
| **Lot 3** | § L3 | B1 · B4 · B9 · B10 | + preview tests |
| **Lot 4** | § L4 | **B1–B10 complet** | Suite complète § C référence |

---

## Prérequis communs

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone --stop-after-init
docker restart sandbox-odoo19-odoo-1
```

- Hard refresh navigateur (Cmd+Shift+R).
- Module **≥ `19.0.15.11.0`** pour Lot 1.
- Prérequis fonctionnels : wishlist GO MOA (`15.10.3`) · UX-1 · UX-2 · conversion tile.

---

# Lot 1 — Wishlist toggle sans sortie + feedback carte

## Objectif MOA

Depuis `/shop`, l’utilisateur peut **ajouter et retirer** un produit de la wishlist via le cœur overlay **sans quitter la page**. Le compteur header reste synchronisé. Le cœur reste terracotta lorsque le produit est retenu.

## Prérequis Lot 1

- Branche `feat/marketone-ux4-lot1-wishlist-toggle` déployée.
- JS `marketone_shop_in_place.js` chargé (vérifier absence d’erreur console).
- Recette wishlist antérieure lue : [`RECETTE_VISUELLE_WISHLIST_STANDARD.md`](../RECETTE_VISUELLE_WISHLIST_STANDARD.md) § 3 cards.

## Scénario visiteur public (prioritaire)

| # | Étape | Résultat attendu | ☐ |
|---|-------|------------------|---|
| L1.1 | Ouvrir `/shop` en navigation privée | HTTP 200 · grille visible | |
| L1.2 | Noter URL et compteur wishlist header (ex. 0) | URL = `/shop` | |
| L1.3 | Cliquer cœur d’une carte (1er clic) | **Pas de navigation** · URL inchangée · animation optionnelle vers header | |
| L1.4 | Observer cœur + carte | Cœur plein terracotta `#C4715A` · carte `.marketone-shop-card--in-wishlist` (bordure discrète) | |
| L1.5 | Observer compteur header | +1 (ex. 0 → 1) | |
| L1.6 | **Second clic** sur le même cœur | **Pas de navigation** · retrait wishlist | |
| L1.7 | Observer cœur + carte | Cœur contour repos · état carte normalisé | |
| L1.8 | Observer compteur header | -1 (ex. 1 → 0) | |
| L1.9 | Répéter sur 2e produit différent | Même comportement toggle | |
| L1.10 | Clic **Voir** ou titre (contrôle non-régression) | Navigation fiche produit **autorisée** (hors Lot 1) | |

## Scénario connecté (réserve documentaire)

> Compte test MOA non fourni — section **documentaire** jusqu’à disponibilité compte.  
> Référence : [`RECETTE_VISUELLE_WISHLIST_STANDARD.md`](../RECETTE_VISUELLE_WISHLIST_STANDARD.md) § Vigilance P3–P6.

| # | Étape | Résultat attendu | ☐ |
|---|-------|------------------|---|
| L1.C1 | Connecté · toggle add/remove depuis `/shop` | Pas de navigation · compteur cohérent | |
| L1.C2 | Persistance après refresh `/shop` | État cœurs cohérent avec wishlist partenaire | |

## Régression Lot 1 (obligatoire)

Rejouer depuis [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../REFERENCE_RECETTE_BOUTIQUE_MOA.md) :

| Section | Contrôle | ☐ |
|---------|----------|---|
| **B1** | Smoke `/shop`, `/shop/cart`, `/shop/wishlist` | |
| **B4** | Structure tuile · Voir + prix · panier survol | |
| **B5** | Wishlist header · pas de doublon card | |
| **B6** | Mobile 375 px · cœur cliquable · offcanvas ordre | |
| **B7** | Toggle wishlist sans sortie `/shop` | |

## Captures attendues Lot 1

| ID | Objet | Fichier suggéré |
|----|-------|-----------------|
| C-L1-1 | `/shop` desktop — cœur repos | `capture_ux4_l1_shop_desktop_repos_YYYYMMDD.png` |
| C-L1-2 | `/shop` desktop — produit retenu (terracotta + carte) | `capture_ux4_l1_shop_desktop_retenu_YYYYMMDD.png` |
| C-L1-3 | Header compteur après ajout | `capture_ux4_l1_header_compteur_YYYYMMDD.png` |
| C-L1-4 | Mobile 375 px — toggle | `capture_ux4_l1_shop_mobile_YYYYMMDD.png` |

## Tests auto Lot 1

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf -d ckr-marketone-01 \
  -u dorevia_ckreyol_marketone --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_shop_in_place,dorevia_marketone_shop_wishlist,dorevia_marketone_shop_regression,dorevia_marketone_shop_filter_state,dorevia_marketone_shop_sidebar,dorevia_marketone_shop_sidebar_collections,dorevia_marketone_smoke,dorevia_marketone_lot3_shop \
  --http-port=8073
```

**Attendu :** 0 failed.

## Verdict Lot 1

| Verdict | Condition |
|---------|-----------|
| **GO MOA Lot 1** | L1.1–L1.9 OK · B1/B4/B5/B6/B7 OK · tests auto verts |
| **GO avec réserve** | Comportement public OK · scénario connecté non rejoué (documenté) |
| **NO GO** | Navigation forcée au toggle · compteur incohérent · régression B4/B5/B6 |

**Verdict :** ☐ GO · ☐ GO avec réserve · ☐ NO GO

**Réserves :**

---

# Lot 2 — Panier sans sortie + feedback carte

> **Statut :** planifié — ne pas recetter avant implémentation Lot 2.

## Objectif MOA

Ajout au panier depuis la grille `/shop` **sans redirection** `/shop/cart`. Feedback local sur la carte : état « Ajouté au panier », lien secondaire « Voir le panier », compteur header synchronisé.

## Prérequis Lot 2

- Lot 1 **GO MOA**.
- `website.add_to_cart_action = stay` (défaut Odoo — à vérifier BO site).
- Recette conversion tile : [`RECETTE_MANUELLE_SHOP_CONVERSION_TILE.md`](../boutique/RECETTE_MANUELLE_SHOP_CONVERSION_TILE.md) § panier survol.

## Scénario visiteur public

| # | Étape | Résultat attendu | ☐ |
|---|-------|------------------|---|
| L2.1 | `/shop` · survol photo · clic panier | URL reste `/shop` | |
| L2.2 | Observer carte | État « Ajouté au panier » visible | |
| L2.3 | Observer header | Compteur panier +1 | |
| L2.4 | Lien « Voir le panier » sur carte (si présent) | Navigation **volontaire** vers `/shop/cart` | |
| L2.5 | Clic header panier | Navigation `/shop/cart` acceptée (secondaire) | |

## Scénario connecté

| # | Étape | Résultat attendu | ☐ |
|---|-------|------------------|---|
| L2.C1 | Connecté · ajout depuis grille | Pas de navigation · panier compte cohérent | |

## Régression Lot 2

| Section | ☐ |
|---------|---|
| B1 · B4 · **B8** · conversion tile panier survol | |

## Captures attendues Lot 2

| ID | Objet |
|----|-------|
| C-L2-1 | Carte état « Ajouté au panier » |
| C-L2-2 | Header compteur panier |
| C-L2-3 | Mobile — add sans navigation |

## Verdict Lot 2

**Verdict :** ☐ GO · ☐ GO avec réserve · ☐ NO GO · ☐ Non exécuté (Lot 2 pending)

---

# Lot 3 — Voir sans sortie / preview in-page

> **Statut :** **GELÉ P2** — ne pas exécuter avant arbitrage MOA Lot 3 et implémentation.

## Objectif MOA

Le CTA **« Voir »** ouvre une prévisualisation produit **non modale** dans `/shop`. Photo et titre restent des liens vers la fiche complète.

## Scénario visiteur public (spec)

| # | Étape | Résultat attendu | ☐ |
|---|-------|------------------|---|
| L3.1 | Clic **Voir** | Preview s’ouvre · URL `/shop` (éventuellement hash/query) | |
| L3.2 | Desktop | Panneau latéral droit · grille reste visible | |
| L3.3 | Mobile | Bloc détail intégré / accordéon sous tuile | |
| L3.4 | Lien « Voir la fiche complète » | Navigation fiche produit | |
| L3.5 | Clic photo ou titre | Navigation fiche produit (gel MOA) | |
| L3.6 | Fermeture preview (ESC / croix) | Retour état grille · pas de modal | |

## Régression Lot 3

| Section | ☐ |
|---------|---|
| B1 · B4 · **B9** · **B10** | |

## Verdict Lot 3

**Verdict :** ☐ GO · ☐ NO GO · ☐ Non exécuté (gel P2)

---

# Lot 4 — Régression globale boutique

> **Statut :** à rejouer **à chaque jalon** (Lots 1, 2, 3) — pas uniquement en fin de chantier.

## Objectif MOA

Validation transversale : tous les invariants boutique + critères UX-4 B7–B10.

## Checklist complète

| Section | Description | Lot 1 | Lot 2 | Lot 3 |
|---------|-------------|-------|-------|-------|
| B1 | Smoke URLs | ☐ | ☐ | ☐ |
| B2 | Haut grille UX-1 | ☐ | ☐ | ☐ |
| B3 | Sidebar + offcanvas | ☐ | ☐ | ☐ |
| B4 | Cards conversion | ☐ | ☐ | ☐ |
| B5 | Wishlist | ☐ | ☐ | ☐ |
| B6 | Mobile | ☐ | ☐ | ☐ |
| B7 | Wishlist toggle in-place | ☐ | — | ☐ |
| B8 | Panier in-place | — | ☐ | ☐ |
| B9 | Preview Voir in-place | — | — | ☐ |
| B10 | Destinations secondaires | ☐ | ☐ | ☐ |

## Tests auto complets

Commande identique à [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../REFERENCE_RECETTE_BOUTIQUE_MOA.md) § C + tag `dorevia_marketone_shop_in_place` dès Lot 1.

## Verdict global UX-4

| Verdict | Condition |
|---------|-----------|
| **GO MOA UX-4** | Lots exécutés GO · B1–B10 OK · doctrine respectée |
| **GO partiel** | Lot(s) validé(s) · autres lots pending documenté |
| **NO GO** | Régression bloquante § A référence |

**Verdict global :** ☐ GO · ☐ GO partiel · ☐ NO GO

---

## Grille d’exécution

| Date | Lot | Version | Exécuteur | Verdict | Rapport |
|------|-----|---------|-----------|---------|---------|
| | L1 | `19.0.15.11.0` | | | |

---

## Fichiers Lot 1 (implémentation)

| Fichier | Rôle |
|---------|------|
| `controllers/website_sale_wishlist.py` | Route `remove_by_product` |
| `static/src/js/marketone_shop_in_place.js` | Toggle grille |
| `views/pages/shop_product_tile_conversion.xml` | QWeb `_is_in_wishlist` |
| `static/src/scss/_shop_product_cards.scss` | Feedback carte |
| `tests/test_marketone_shop_in_place.py` | Tests auto |
