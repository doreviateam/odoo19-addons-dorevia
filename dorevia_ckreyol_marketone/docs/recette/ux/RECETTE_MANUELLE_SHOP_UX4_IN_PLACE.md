# Recette manuelle — UX-4 Boutique continue / Shop-in-place — `/shop`

| Champ | Valeur |
|-------|--------|
| **Ticket** | [`TICKET_MARKETONE_UX4_SHOP_IN_PLACE`](../../tickets/ux/TICKET_MARKETONE_UX4_SHOP_IN_PLACE.md) |
| **Version cible Lot 1** | **`19.0.15.11.1`** |
| **Branche Lot 1** | `feat/marketone-ux4-lot1-wishlist-toggle` |
| **PR** | **#12** — [`[CK][UX-4] Lot 1 — Wishlist toggle in-place sur /shop`](https://github.com/doreviateam/odoo19-addons-dorevia/pull/12) |
| **URL** | http://localhost:18079/shop |
| **Base** | `ckr-marketone-01` |
| **Statut recette** | ☑ **GO GLOBAL MOA UX-4** · version courante **`19.0.15.14.2`** (reprise MOA 3quater bis · suppression lien tuile · 2026-05-22) |
| **Version de référence UX-4** | **`19.0.15.14.2`** · reprise post-PR #19 |
| **Version Lot 3ter (livrée)** | **`19.0.15.13.9`** (correctif R2 : survol + scroll panneau) |
| **Note arbitrage Lot 3ter** | [`NOTE_ARBITRAGE_UX4_LOT3TER_IMAGE_PREVIEW_CLICK.md`](../../tickets/ux/NOTE_ARBITRAGE_UX4_LOT3TER_IMAGE_PREVIEW_CLICK.md) |
| **Version Lot 3 (fonctionnel)** | **`19.0.15.13.2`** — **figée** |
| **Version Lot 3bis (visuel)** | **`19.0.15.13.4`** (cible — incl. retrait naturel V3bis.12) |
| **Branche Lot 3bis** | `feat/marketone-ux4-lot3bis-preview-premium` (autorisée post-note) |
| **PR Lot 3** | **#14** · **#15** — mergées |
| **PR Lot 3bis** | **#16** — [`[CK][UX-4] Lot 3bis — Finition visuelle preview premium`](https://github.com/doreviateam/odoo19-addons-dorevia/pull/16) |
| **Rapport Lot 3bis** | [`RAPPORT_RECETTE_SHOP_UX4_LOT3BIS_PREVIEW_PREMIUM_20260522.md`](RAPPORT_RECETTE_SHOP_UX4_LOT3BIS_PREVIEW_PREMIUM_20260522.md) |
| **Note arbitrage Lot 3** | [`NOTE_ARBITRAGE_UX4_LOT3_PREVIEW_VOIR.md`](../../tickets/ux/NOTE_ARBITRAGE_UX4_LOT3_PREVIEW_VOIR.md) |
| **Note arbitrage Lot 3bis** | [`NOTE_ARBITRAGE_UX4_LOT3BIS_PREVIEW_PREMIUM.md`](../../tickets/ux/NOTE_ARBITRAGE_UX4_LOT3BIS_PREVIEW_PREMIUM.md) |

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
| **Lot 1** | § L1 · § L1.0 (console) | B1 · B4 · B5 · B6 · B7 · [W1–W4](#w1w4--critères-wishlist-standard-lot-1) | `dorevia_marketone_shop_in_place` + wishlist + régression |
| **Lot 2** | § L2 | B1 · B4 · B8 · conversion tile | + smoke lot3 |
| **Lot 3** | § L3 · § G3 · § L3.F · § L3.M | B1 · **B4** · **B7** · **B8** · **B9** · **B10** | + preview tests |
| **Lot 3bis** | § **V3bis** · smoke L3.F / L3.M | Smoke **G3.6–G3.9** · **G3.1** · **G3.3** | Aucun test auto supplémentaire |
| **Lot 3ter** | § **V3ter** · smoke L1 / L2 / G3.9 | Smoke **G3.6–G3.9** · **G3.1** · **G3.3** | Test grille image preview data |
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

### Contrôle avant recette (obligatoire — Lot 1)

> **Objectif :** éviter de recetter une autre branche, une autre base ou une version antérieure.  
> **Ne pas démarrer § L1** tant que toutes les cases ci-dessous ne sont pas cochées.

| ☐ | Contrôle | Valeur attendue |
|---|----------|-----------------|
| ☐ | **Branche active** (sandbox / déploiement recette) | `feat/marketone-ux4-lot1-wishlist-toggle` |
| ☐ | **Version module** (`__manifest__.py` ou Apps → C-Kreyol Marketone) | **`19.0.15.11.1`** |
| ☐ | **Base de données** | `ckr-marketone-01` |
| ☐ | **URL testée** | http://localhost:18079/shop |
| ☐ | **PR concernée** | **#12** — UX-4 Lot 1 uniquement |
| ☐ | **Lot testé** | **UX-4 Lot 1 uniquement** (pas Lot 2 · pas Lot 3) |

**Vérification rapide version (optionnelle) :**

```bash
grep '"version"' dorevia_ckreyol_marketone/__manifest__.py
# Attendu : "19.0.15.11.1"
```

---

# Lot 1 — Wishlist toggle sans sortie + feedback carte

## Objectif MOA

Depuis `/shop`, l’utilisateur peut **ajouter et retirer** un produit de la wishlist via le cœur overlay **sans quitter la page**. Le compteur header reste synchronisé. Le cœur reste terracotta lorsque le produit est retenu.

## Prérequis Lot 1

- Contrôle avant recette (§ ci-dessus) **100 % coché**.
- Branche `feat/marketone-ux4-lot1-wishlist-toggle` déployée · PR **#12**.
- Recette wishlist antérieure lue : [`RECETTE_VISUELLE_WISHLIST_STANDARD.md`](../RECETTE_VISUELLE_WISHLIST_STANDARD.md) § 3 cards.

## Scénario visiteur public (prioritaire)

| # | Étape | Résultat attendu | ☐ |
|---|-------|------------------|---|
| **L1.0** | Ouvrir la **console navigateur** (F12 / Cmd+Opt+I) sur `/shop` | Aucune **erreur JavaScript rouge** au chargement · bundle frontend contenant l’interaction **`marketone_shop_wishlist_toggle`** (Odoo 19) · **pas d’erreur bloquante** au 1er / 2e clic cœur | |
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

### W1–W4 — Critères wishlist standard (Lot 1)

> Source : [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../REFERENCE_RECETTE_BOUTIQUE_MOA.md) § A5 · détail visuel : [`RECETTE_VISUELLE_WISHLIST_STANDARD.md`](../RECETTE_VISUELLE_WISHLIST_STANDARD.md).

| ☐ | ID | Critère MOA |
|---|-----|-------------|
| ☐ | **W1** | **Un seul** bouton wishlist par card (overlay coin **haut droit** image) — pas de doublon grille Odoo |
| ☐ | **W2** | Cœur repos discret · hover **#C4715A** · **retenu terracotta persistant** après ajout (Lot 1 : toggle add/remove) |
| ☐ | **W3** | Extension **légère** du standard Odoo — pas de modèle / logique métier CK wishlist dédiée |
| ☐ | **W4** | Sur **fiche produit** : wishlist reste **secondaire** vs achat (non-régression — pas modifié par Lot 1) |

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
| **GO MOA Lot 1** | Contrôle avant recette OK · **L1.0–L1.10** OK · B1/B4/B5/B6/B7 OK · W1–W4 OK · tests auto verts |
| **GO avec réserve documentaire** | Scénario **visiteur public** OK (L1.0–L1.10) · régression OK · **scénario connecté non rejoué** faute de compte test MOA (§ L1.C1–C2) |
| **NO GO** | Navigation forcée au toggle · compteur incohérent · erreur JS bloquante L1.0 · régression B4/B5/B6/W1–W4 |

### Formulation réserve documentaire (scénario connecté non rejoué)

Si le visiteur public est **GO** mais que L1.C1–C2 n’a pas pu être exécuté :

> **GO avec réserve documentaire** — Scénario connecté / persistance wishlist non rejoué faute de compte test MOA. Périmètre visiteur public validé. Réserve documentaire **non bloquante** pour Lot 1.

**Verdict :** ☐ GO · ☑ GO avec réserve documentaire · ☐ NO GO

**Réserves :** Scénario connecté / persistance wishlist non rejoué faute de compte test MOA — réserve documentaire **non bloquante** (2026-05-22).

**Rapport :** [`RAPPORT_RECETTE_SHOP_UX4_IN_PLACE_20260522.md`](RAPPORT_RECETTE_SHOP_UX4_IN_PLACE_20260522.md)

---

# Lot 2 — Panier sans sortie + feedback carte

> **Statut :** **GO avec réserve documentaire MOA** (`12.3` — 2026-05-22) · PR #13 mergée.

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
| L2.4 | Lien « Voir le panier » sur carte (si présent) | ~~Navigation volontaire vers `/shop/cart`~~ **Révoqué 14.2** — lien tuile supprimé · navigation panier via **header** | |
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

**Verdict :** ☐ GO · ☑ GO avec réserve documentaire · ☐ NO GO · ☐ Non exécuté (Lot 2 pending)

**Réserves :** Scénario connecté L2.C1 non rejoué · polices Google Fonts CORS en sandbox (non bloquant).

**Rapport :** [`RAPPORT_RECETTE_SHOP_UX4_LOT2_IN_PLACE_20260522.md`](RAPPORT_RECETTE_SHOP_UX4_LOT2_IN_PLACE_20260522.md)

---

# Lot 3 — Voir sans sortie / preview in-page

> **Statut :** **GO avec réserve documentaire MOA** (`13.2` — 2026-05-22) · G3.9 revalidé · PR **#14** (`13.1`) + **#15** (`13.2`).
>
> **Note :** [`NOTE_ARBITRAGE_UX4_LOT3_PREVIEW_VOIR.md`](../../tickets/ux/NOTE_ARBITRAGE_UX4_LOT3_PREVIEW_VOIR.md)

## Objectif MOA

Le CTA **« Voir »** ouvre une prévisualisation produit **non modale** dans `/shop` (URL inchangée). **Photo et titre** restent des liens vers la fiche complète (gel MOA — non modifiable).

## Prérequis Lot 3

- Lots 1–2 **GO MOA** (`11.1` · `12.3`).
- Arbitrage MOA Lot 3 validé (note ci-dessus).

## Arbitrages MOA Lot 3 (V1)

| Sujet | Décision MOA |
|-------|--------------|
| CTA « Voir » | Preview in-page · URL `/shop` · fiche complète = destination secondaire |
| Photo / titre | Liens fiche **inchangés** |
| Desktop | Offcanvas latéral **droit non modal** · grille visible · fermeture × / ESC / re-clic |
| Mobile | Preview **inline sous tuile** · une seule ouverte · **pas de bottom sheet** V1 · 390 px sans débordement |
| Contenu V1 | Image · titre · prix · origine · collection/label (sans filtre) · description courte · panier · wishlist · « Voir la fiche complète » |
| Variantes | Variante unique → preview complète · multi-variante / configurable → **fallback fiche obligatoire** V1 |
| Deep-link preview | **Interdit V1** |
| Modal popup | **Interdit** |

## Critères GO Lot 3 (G3.1–G3.10)

| # | Critère | Recette associée | ☐ |
|---|---------|------------------|---|
| G3.1 | Clic « Voir » : preview visible · **URL `/shop`** (query/hash acceptés · pas navigation fiche) | L3.1 | |
| G3.2 | Desktop : panneau latéral droit · grille reste visible · **pas modal bloquante** | L3.2 | |
| G3.3 | Mobile : preview inline sous tuile · **390 px** sans débordement · une seule preview ouverte | L3.3 | |
| G3.4 | Photo + titre tuile : navigation fiche **inchangée** | L3.5 · **B10** | |
| G3.5 | Contenu minimal V1 présent (§ arbitrages) | L3.7 | |
| G3.6 | Panier depuis preview : comportement aligné Lot 2 · URL `/shop` | L3.8 · **B8** | |
| G3.7 | Wishlist depuis preview : comportement aligné Lot 1 · URL `/shop` | L3.8 · **B7** | |
| G3.8 | Lien « Voir la fiche complète » → fiche produit | L3.4 · **B10** | |
| G3.9 | Fermeture preview (× / **Fermer** / ESC / re-clic) sans erreur JS · retour grille propre | L3.6 · **L3.F** · **L3.M** | |
| G3.10 | Régression **B1 · B4 · B7 · B8 · B9 · B10** · tests auto verts | § Régression Lot 3 | |

## Scénario visiteur public L3

| # | Étape | Résultat attendu | ☐ |
|---|-------|------------------|---|
| L3.1 | Clic **Voir** (produit variante unique) | Preview s’ouvre · URL `/shop` | |
| L3.2 | Desktop | Panneau latéral droit · grille visible · pas de modal | |
| L3.3 | Mobile 390 px | Bloc inline sous tuile · pas de bottom sheet · pas de scroll horizontal | |
| L3.4 | Lien « Voir la fiche complète » | Navigation fiche produit | |
| L3.5 | Clic photo ou titre (tuile) | Navigation fiche produit (gel MOA) | |
| L3.6 | Fermeture preview (× / **Fermer** / ESC / re-clic « Voir ») | Retour état grille · pas de modal · CTA désactivé visuellement | |
| L3.7 | Contenu preview | Image · titre · prix · origine · collection · description courte | |
| L3.8 | Panier + wishlist depuis preview | Add in-place · compteurs header cohérents | |
| L3.V1 | Clic **Voir** (produit multi-variante / configurable) | **Fallback fiche produit** (pas preview interactive V1) | |

## Recette ciblée fermeture preview — desktop (L3.F)

> **Contexte MOA :** retour visuel post-merge `13.1` — fermeture panneau preview insuffisamment maîtrisée · **G3.9 bloquant** jusqu’à revalidation.

| # | Étape | Résultat attendu | ☐ |
|---|-------|------------------|---|
| **L3.F1** | Ouvrir `/shop` desktop (≥ 992 px) | Grille visible · HTTP 200 | |
| **L3.F2** | Cliquer **Voir** sur un produit variante unique | Preview ouverte · URL `/shop` | |
| **L3.F3** | Constater panneau latéral droit | Offcanvas visible · grille reste utilisable · pas de modal | |
| **L3.F4** | Fermer via **croix** ou bouton **Fermer** (header panneau) | Panneau disparaît · contenu preview vidé · CTA « Voir » retour repos | |
| **L3.F5** | Constater grille | Grille scrollable / cliquable · pas de panneau résiduel | |
| **L3.F6** | Rouvrir une preview (même ou autre produit) | Preview s’ouvre normalement | |
| **L3.F7** | Fermer via touche **ESC** | Panneau disparaît · état grille propre | |
| **L3.F8** | Rouvrir une preview | Preview visible | |
| **L3.F9** | **Re-clic « Voir »** sur le produit ouvert **ou** ouvrir un autre produit | Même produit → fermeture · autre produit → remplacement propre (une seule preview) | |
| **L3.F10** | Constater comportement | Une seule preview desktop · pas de double panneau · pas de CTA bloqué actif | |
| **L3.F11** | Console navigateur | Aucune erreur JS **bloquante** | |

## Recette ciblée fermeture preview — mobile (L3.M)

| # | Étape | Résultat attendu | ☐ |
|---|-------|------------------|---|
| **L3.M1** | `/shop` · viewport **390 px** | Pas de débordement horizontal | |
| **L3.M2** | Cliquer **Voir** | Preview **inline** sous tuile | |
| **L3.M3** | Constater bouton **Fermer** dans la preview | Visible · cliquable | |
| **L3.M4** | Fermer via **Fermer** · ESC · re-clic **Voir** | Preview repliée · retour grille compréhensible | |
| **L3.M5** | Ouvrir preview produit A puis produit B | **Une seule** preview ouverte | |
| **L3.M6** | Console | Aucune erreur JS bloquante | |

## Régression Lot 3

| Section | Focus | ☐ |
|---------|-------|---|
| **B1** | Smoke `/shop` · `/shop/cart` · `/shop/wishlist` | |
| **B4** | Tuile conversion : photo · Voir/prix · panier survol · wishlist — **non-régression critique** | |
| **B7** | Wishlist toggle in-place depuis grille — **conservé** | |
| **B8** | Panier in-place depuis grille — **conservé** | |
| **B9** | Preview « Voir » in-place — **nouveau** | |
| **B10** | Destinations secondaires : photo · titre · fiche · header panier/wishlist | |

Recette conversion tile : [`RECETTE_MANUELLE_SHOP_CONVERSION_TILE.md`](../boutique/RECETTE_MANUELLE_SHOP_CONVERSION_TILE.md).

## Captures attendues Lot 3

| ID | Sujet |
|----|-------|
| C-L3-1 | Desktop — preview ouverte · panneau droit · grille visible |
| C-L3-2 | Mobile 390 px — preview inline sous tuile |
| C-L3-3 | Contenu preview V1 complet |
| C-L3-4 | Fermeture preview |
| C-L3-5 | Fallback fiche — produit configurable (si disponible en catalogue) |

## Verdict Lot 3

| Verdict | Condition |
|---------|-----------|
| **GO MOA Lot 3** | G3.1–G3.10 OK · régression B4/B7/B8/B9/B10 OK · tests auto verts · recette desktop + mobile |
| **GO avec réserve documentaire** | Visiteur public OK · réserve documentée (ex. L3.C1 connecté) |
| **NO GO** | Régression tuile · modal · navigation forcée fiche au clic « Voir » · preview configurateur |

**Verdict :** ☐ GO · ☑ **GO avec réserve documentaire MOA** · ☐ NO GO

**Réserves :** **L3.V1** fallback configurable / multi-variante à rejouer dès produit éligible publié · polices Google Fonts CORS sandbox (non bloquant).

**Version livrée :** `19.0.15.13.2` · tests auto **88/88** · G3.9 revalidé (L3.F · L3.M).

**Rapport :** [`RAPPORT_RECETTE_SHOP_UX4_LOT3_IN_PLACE_20260522.md`](RAPPORT_RECETTE_SHOP_UX4_LOT3_IN_PLACE_20260522.md)

---

# Lot 3bis — Finition visuelle premium preview

> **Statut :** **Arbitrage MOA GO** (2026-05-22) · **GO fonctionnel Lot 3 figé** sur `19.0.15.13.2` · passe **strictement visuelle** · branche autorisée post-note.
>
> **Note :** [`NOTE_ARBITRAGE_UX4_LOT3BIS_PREVIEW_PREMIUM.md`](../../tickets/ux/NOTE_ARBITRAGE_UX4_LOT3BIS_PREVIEW_PREMIUM.md)

## Objectif MOA

Améliorer la **qualité perçue** de la preview produit (mini-fiche courte premium, univers CK) **sans modifier le comportement** validé Lot 3.

## Périmètre

| In | Out |
|----|-----|
| SCSS `_shop_product_preview.scss` | JS interactions |
| QWeb léger (wrappers · libellés · structure chips) | Routes · contrôleurs |
| Tokens CK existants | Panier / wishlist comportement |
| Version **`19.0.15.13.3`** | Photo / titre tuile · fallback · deep-link · configurateur |

## Arbitrages MOA figés

| Sujet | Décision |
|-------|----------|
| Titre header | **`Découvrir le produit`** (remplace « Aperçu produit ») |
| Fermeture desktop | **Croix seule** · zone ≥ 44×44 · `aria-label` conservé · pas de bouton texte « Fermer » |
| Fermeture mobile | **Fermer** texte discret conservé |
| Image | **`object-fit: contain`** · cadre pastel · pas cover |
| DA | Fond pastel CK · chips origines/collections · CTA respirant · lien fiche secondaire premium |

## Critères recette visuelle V3bis

| # | Critère | Desktop | Mobile 390 px |
|---|---------|---------|---------------|
| **V3bis.1** | Fond panneau / inline ≠ blanc Bootstrap brut · cohérence pastel CK | ☐ | ☐ |
| **V3bis.2** | Image **cadrée** · contain · masse visuelle maîtrisée | ☐ | ☐ |
| **V3bis.3** | Titre header **« Découvrir le produit »** | ☐ | ☐ |
| **V3bis.4** | Fermeture **lisible** (× desktop · Fermer mobile) | ☐ | ☐ |
| **V3bis.5** | Origines / Collections — chips ou labels pastel élégants | ☐ | ☐ |
| **V3bis.6** | CTA panier **respirant** (pleine largeur recommandée) | ☐ | ☐ |
| **V3bis.7** | Wishlist **intégrée** (cohérence tuile CK) | ☐ | ☐ |
| **V3bis.8** | Lien **« Voir la fiche complète »** — secondaire premium · séparé des CTA | ☐ | ☐ |
| **V3bis.9** | **Respiration** verticale globale (image · infos · actions) | ☐ | ☐ |
| **V3bis.10** | **Cohérence palette** CK (pastel · terracotta · sauge) | ☐ | ☐ |
| **V3bis.11** | Ressenti **maison de sélection** · pas panneau technique | ☐ | ☐ |
| **V3bis.12** | **Retrait naturel** — clic / scroll hors preview · pas effet modal | ☐ | ☐ |

## Recette ciblée retrait naturel — desktop (V3bis.12)

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| V3bis.12-D1 | Ouvrir une preview | Panneau ouvert · grille visible | |
| V3bis.12-D2 | Cliquer dans la **grille boutique** hors panneau | Preview se ferme proprement · pas de backdrop | |
| V3bis.12-D3 | Rouvrir · **scroller** la boutique hors panneau | Preview se retire · URL `/shop` | |
| V3bis.12-D4 | Rouvrir · interactions **dans** le panneau (scroll interne si contenu long) | Preview **reste ouverte** | |
| V3bis.12-D5 | Smoke G3.9 : croix · ESC · re-clic **Voir** | Fermetures existantes OK | |
| V3bis.12-D6 | Console navigateur | Pas d’erreur JS bloquante | |

## Recette ciblée retrait naturel — mobile (V3bis.12)

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| V3bis.12-M1 | Ouvrir preview inline | Bloc sous tuile | |
| V3bis.12-M2 | **Scroller** la page boutique hors preview | Repli propre ou retrait lisible | |
| V3bis.12-M3 | Rouvrir · scroller **dans** la preview | Preview **maintenue** | |
| V3bis.12-M4 | Tap hors preview (hors CTA **Voir**) | Repli propre si applicable | |
| V3bis.12-M5 | Bouton **Fermer** · smoke L3.M | Fermeture explicite OK | |
| V3bis.12-M6 | Mobile 390 px | Pas de débordement horizontal | |

## Recette ciblée retrait naturel intelligent — desktop (R2 — ajout MOA 2026-05-22)

> **Règle MOA :** le panneau preview ne doit jamais disparaître tant que le curseur est à l'intérieur, y compris en cas de scroll de la page.

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| **R2-D1** | Ouvrir preview · placer le curseur dans le panneau · scroller (molette) | **Preview maintenue** · page scrolle · panneau reste | ☑ |
| **R2-D2** | Scroller à nouveau curseur dans le panneau | **Preview maintenue** | ☑ |
| **R2-D3** | Déplacer le curseur à l'intérieur du panneau | **Preview maintenue** | ☑ |
| **R2-D4** | Cliquer dans le corps du panneau hors CTA de fermeture | **Preview maintenue** | ☑ |
| **R2-D5** | Curseur hors panneau · scroller | Preview se ferme (retrait naturel attendu) | ☑ |
| **R2-D6** | Vérifier l'absence de backdrop / modal après fermeture | Pas de backdrop · pas de modal | ☑ |
| **R2-D7** | Smoke : croix · ESC · re-clic « Voir » toujours fonctionnels | Fermetures explicites OK | ☑ |
| **R2-D8** | Console | Aucune erreur JS bloquante | ☑ |

## Recette ciblée retrait naturel intelligent — mobile (R2 — ajout MOA 2026-05-22)

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| **R2-M1** | Ouvrir preview inline · scroller dans le slot preview | **Preview maintenue** | ☑ |
| **R2-M2** | Scroller la page hors du slot preview | **Repli propre** | ☑ |
| **R2-M3** | Rouvrir · bouton **Fermer** | Fermeture explicite OK | ☑ |
| **R2-M4** | Mobile 390 px · pas de débordement horizontal | `hOverflow = false` | ☑ |
| **R2-M5** | Console mobile | Aucune erreur JS bloquante | ☑ |

## Non-régression fonctionnelle obligatoire (smoke)

> Lot 3 **figé** — toute régression bloque le merge 3bis.

| Critère | Référence | ☐ |
|---------|-----------|---|
| Fermeture preview | **G3.9** · **L3.F1–L3.F11** · **L3.M3–L3.M6** | |
| Panier / wishlist depuis preview | **G3.6–G3.7** | |
| Lien fiche complète | **G3.8** | |
| URL `/shop` | **G3.1** | |
| Mobile sans débordement | **G3.3** · **L3.M1** | |
| Console sans erreur JS bloquante | **L3.F11** · **L3.M6** | |

## Captures attendues Lot 3bis

| ID | Sujet |
|----|-------|
| C-V3bis-1 | Desktop — preview ouverte |
| C-V3bis-2 | Desktop — preview fermée |
| C-V3bis-3 | Mobile 390 px — preview ouverte |
| C-V3bis-4 | Mobile 390 px — preview fermée |
| C-V3bis-5 | Produit **packshot** |
| C-V3bis-6 | Produit **lifestyle** (si disponible) |

## Verdict Lot 3bis

| Verdict | Condition |
|---------|-----------|
| **GO MOA Lot 3bis** | V3bis.1–V3bis.12 OK · smoke G3.6–G3.9 OK · captures MOA · pas de régression Lot 3 |
| **NO GO** | Régression fonctionnelle · scope creep · ressenti non premium |

**Verdict :** ☑ **GO MOA Lot 3bis avec réserve documentaire** (`13.4` · PR #16) · ☐ NO GO

**Réserve documentaire :** **R1** — libellé bouton **Fermer** mobile parfois tronqué (`Ferme`) · cliquable · non bloquant.

**Rapport :** [`RAPPORT_RECETTE_SHOP_UX4_LOT3BIS_PREVIEW_PREMIUM_20260522.md`](RAPPORT_RECETTE_SHOP_UX4_LOT3BIS_PREVIEW_PREMIUM_20260522.md)

---

# Lot 3ter — Clic image tuile → preview

> **Statut :** **Arbitrage MOA GO** (2026-05-22) · micro-évolution isolée post-PR #16 · branche `feat/marketone-ux4-lot3ter-image-preview-click`.

## Objectif MOA

Aligner le **clic image tuile** (hors panier / wishlist) sur le comportement du CTA **Voir** — preview in-page · URL `/shop` conservée.

## Périmètre

| In | Out |
|----|-----|
| Clic `oe_product_image_link` → preview | Titre → fiche (inchangé) |
| QWeb data attributes image | Routes · fallback · deep-link |
| JS handler partagé preview | Panier Lot 2 · wishlist Lot 1 |

## Critères recette V3ter

| # | Critère | Desktop | Mobile 390 px |
|---|---------|---------|---------------|
| **V3ter.1** | Clic **image** hors boutons → preview ouverte | ☑ | ☑ |
| **V3ter.2** | Clic **panier** overlay → panier uniquement, pas preview | ☑ | ☑ |
| **V3ter.3** | Clic **wishlist** overlay → wishlist uniquement, pas preview | ☑ | ☑ |
| **V3ter.4** | Clic **titre** → fiche produit complète | ☑ | ☑ |
| **V3ter.5** | Comportement **identique** au CTA **Voir** (toggle / bascule produit) | ☑ | ☑ |
| **V3ter.6** | URL **`/shop`** conservée | ☑ | ☑ |
| **V3ter.7** | Smoke **G3.9** + retrait naturel **V3bis.12** inchangés | ☑ | ☑ |
| **V3ter.8** | Console sans erreur JS bloquante | ☑ | ☑ |

## Non-régression obligatoire (smoke)

| Critère | Référence | ☐ |
|---------|-----------|---|
| Panier in-place depuis overlay | Lot 2 · **G3.6** | ☑ |
| Wishlist toggle depuis overlay | Lot 1 · **G3.7** | ☑ |
| Fermeture / retrait preview | **G3.9** · **V3bis.12** | ☑ |
| URL `/shop` | **G3.1** | ☑ |
| Mobile sans débordement | **G3.3** | ☑ |

## Verdict Lot 3ter

| Verdict | Condition |
|---------|-----------|
| **GO MOA Lot 3ter** | V3ter.1–V3ter.8 OK · smoke Lots 1–2 + G3.9 OK |
| **NO GO** | Régression panier / wishlist / titre / preview |

**Verdict :** ☑ **GO MOA Lot 3ter** · ☐ NO GO · ☐ Non exécuté

**Exécution 2026-05-22 (`19.0.15.13.5`) :** tests auto **88/88 OK**, mais **V3ter.1 bloquant** : le clic/tap image reste sur `/shop` sans ouvrir la preview desktop ni mobile. Par conséquence, **V3ter.5** (toggle / bascule produit via image) n'est pas validable. Panier, wishlist, titre produit, URL `/shop`, console et mobile sans débordement sont non régressés.

**Reprise 2026-05-22 (`ef99bbe`) :** après nouvel upgrade module + restart Odoo, tests auto toujours **88/88 OK**. En contrôle navigateur mobile 390 px, le tap image n'ouvre toujours pas la preview ; le CTA `Voir` ne déclenche pas non plus la preview dans cette passe. Panier, wishlist et titre restent OK. Verdict **NO GO maintenu**.

**Reprise 2026-05-22 (`aab2ab1` · `19.0.15.13.6`) :** upgrade module + restart Odoo OK, tests auto **88/88 OK**. En contrôle navigateur mobile 390 px, le tap image et le CTA `Voir` restent sur `/shop` sans ouvrir la preview. Panier overlay, wishlist overlay, titre produit, console et absence de débordement mobile restent OK. Verdict **NO GO maintenu**.

**Re-recette MOA 2026-05-22 (`132995f` · `19.0.15.13.7`) :** upgrade module + restart Odoo OK, tests auto **88/88 OK**. V3ter.1–8 rejoués en navigateur mobile 390 px : le tap image et le CTA `Voir` restent sur `/shop` sans preview ; le re-tap / bascule produit n'est donc pas validable. Panier overlay, wishlist overlay, titre produit, URL `/shop`, console et absence de débordement mobile restent OK. Verdict **NO GO maintenu**.

**Re-recette MOA 2026-05-22 (`9e14e15` · `19.0.15.13.8`) :** upgrade module + restart Odoo OK, tests auto **88/88 OK**. V3ter.1–8 rejoués en navigateur mobile 390 px : tap image → preview inline ouverte, CTA `Voir` → preview ouverte, panier / wishlist overlay sans preview parasite, titre → fiche produit, re-tap image → fermeture, image A → image B → bascule preview, URL `/shop` conservée, fermeture ESC / clic grille / scroll OK, console sans erreur bloquante, pas de débordement horizontal. Verdict **GO MOA Lot 3ter**.

Rapport : [`RAPPORT_RECETTE_SHOP_UX4_LOT3TER_IMAGE_PREVIEW_CLICK_20260522.md`](RAPPORT_RECETTE_SHOP_UX4_LOT3TER_IMAGE_PREVIEW_CLICK_20260522.md)

**Note arbitrage :** [`NOTE_ARBITRAGE_UX4_LOT3TER_IMAGE_PREVIEW_CLICK.md`](../../tickets/ux/NOTE_ARBITRAGE_UX4_LOT3TER_IMAGE_PREVIEW_CLICK.md)

---

# Lot 3quater — Harmonisation CTA panier tuile / preview

> **Statut :** **Arbitrage MOA GO** (2026-05-22) · passe **strictement visuelle** post-GO `13.9` · branche `feat/marketone-ux4-lot3quater-cart-cta-tile`.
>
> **Note :** [`NOTE_ARBITRAGE_UX4_LOT3QUATER_CART_CTA_TILE.md`](../../tickets/ux/NOTE_ARBITRAGE_UX4_LOT3QUATER_CART_CTA_TILE.md)

## Objectif MOA

Harmoniser visuellement le CTA panier de la **tuile produit** avec l’esprit du CTA preview : action d’achat **explicite**, sans modifier le comportement Lot 2.

## Périmètre

| In | Out |
|----|-----|
| QWeb : libellé `Ajouter` + classe `--tile` | JS interactions |
| SCSS scoped `.oe_product_image .marketone-shop-card-cart--tile` | Routes · preview · wishlist · clic image |
| `aria-label` / `title` = « Ajouter au panier » | Full-width tuile · déplacement overlay |

## Critères recette V3quater

| # | Critère | Desktop | Mobile 390 px |
|---|---------|---------|---------------|
| **V3quater.1** | CTA panier tuile **lisible** (icône + `Ajouter`) | ☑ auto | ☑ auto |
| **V3quater.2** | CTA visible au **survol** image (desktop) | ☑ auto | — |
| **V3quater.3** | CTA **utilisable** sans débordement horizontal | — | ☑ auto |
| **V3quater.4** | Clic CTA panier → panier uniquement, **pas preview** | ☑ auto | ☑ auto |
| **V3quater.5** | Clic image hors CTA → **preview** | ☑ auto | ☑ auto |
| **V3quater.6** | Clic wishlist → wishlist uniquement | ☑ auto | ☑ MOA |
| **V3quater.7** | Feedback « Ajouté au panier » + compteur header | ☑ auto | ☑ MOA |
| **V3quater.8** | Console sans erreur JS bloquante | ☑ auto | ☑ auto |

## Smoke non-régression obligatoire

| Critère | Référence | ☐ |
|---------|-----------|---|
| Panier in-place Lot 2 | **L2.1–L2.5** | ☑ L2.1 auto |
| Isolation panier / wishlist | **I5 · I6** | ☑ auto |
| Retrait naturel preview | **R2-D1** | ☑ auto |

## Verdict Lot 3quater

| Verdict | Condition |
|---------|-----------|
| **GO MOA Lot 3quater** | V3quater.1–V3quater.8 OK · smoke L2 + I5/I6 + R2-D1 OK · captures desktop + mobile |
| **NO GO** | Régression fonctionnelle · débordement mobile · preview / wishlist / image KO |

**Verdict :** ☑ **GO MOA Lot 3quater** · ☐ NO GO · (`14.0` → `14.1` via PR #19)

Rapport : [`RAPPORT_RECETTE_SHOP_UX4_LOT3QUATER_CART_CTA_TILE_20260522.md`](RAPPORT_RECETTE_SHOP_UX4_LOT3QUATER_CART_CTA_TILE_20260522.md)

---

# Lot 3quater bis — Feedback panier tuile (reprise MOA)

> **Statut :** **Re-arbitrage MOA** (2026-05-22) · version **`19.0.15.14.2`**.
>
> **Décision MOA :** supprimer le lien **`Voir le panier`** de la tuile produit (desktop et mobile).
> Navigation panier portée par le **header** (compteur + icône panier).
>
> **Desktop :** bordure sauge + compteur header · CTA `Ajouter` seul au survol · pas de pill `Voir le panier`.
> **Mobile :** label discret « Ajouté au panier » sous le pied de carte · pas de lien · pas d’encart boxed.

## Critères recette V3qR (reprise)

| # | Critère | Desktop | Mobile 390 px |
|---|---------|---------|---------------|
| **V3qR.1** | Absence lien `Voir le panier` dans la tuile | ☑ auto | ☑ auto |
| **V3qR.2** | Clic `Ajouter` → panier uniquement + compteur +1 | ☑ auto | ☑ auto |
| **V3qR.3** | Desktop survol : CTA `Ajouter` seul (pas de pill `Voir le panier`) | ☑ auto | — |
| **V3qR.4** | État ajouté discret (bordure sauge) | ☑ auto | ☑ auto |
| **V3qR.5** | Clic image hors CTA → preview | ☑ auto | ☑ auto |
| **V3qR.6** | Clic wishlist → wishlist uniquement | ☑ auto | ☐ MOA |
| **V3qR.7** | Header panier → `/shop/cart` | ☑ auto | ☐ MOA |
| **V3qR.8** | Mobile : label « Ajouté au panier » sans lien | — | ☑ auto |
| **V3qR.9** | Console sans erreur JS bloquante | ☑ auto | ☑ auto |

## Verdict Lot 3quater bis (reprise)

**Verdict :** ☐ GO MOA reprise · ☐ NO GO · ☑ **En recette** (`14.2`)

Rapport : [`recette_v3qb_reprise_14_2_20260522.json`](recette_v3qb_reprise_14_2_20260522.json)

---

# Lot 3quater bis — historique (14.1 · PR #19 · révoqué)

> Overlay `Voir le panier` desktop + lien mobile — **révoqué** par re-arbitrage MOA 2026-05-22.
> Voir section reprise **`14.2`** ci-dessus.

## Critères recette V3qB (historique 14.1)

| # | Critère | Desktop | Mobile 390 px |
|---|---------|---------|---------------|
| **V3qB.1** | Pas de bloc `Voir le panier` permanent dans le **corps** | ☑ auto | ☑ auto |
| **V3qB.2** | `Voir le panier` visible au **survol** si produit ajouté (overlay image) | ☑ auto | — |
| **V3qB.3** | Feedback ajout **lisible** sans hover | bordure + header | ☑ auto |
| **V3qB.4** | Clic `Voir le panier` → navigation `/shop/cart` | ☑ auto | ☑ auto |
| **V3qB.5** | Clic image hors CTA → **preview** | ☑ auto | ☑ auto |
| **V3qB.6** | Clic CTA `Ajouter` → panier uniquement | ☑ auto | ☑ auto |
| **V3qB.7** | Clic wishlist → wishlist uniquement | ☑ auto | ☑ MOA |
| **V3qB.8** | Compteur header synchronisé | ☑ auto | ☑ auto |
| **V3qB.9** | Console sans erreur JS bloquante | ☑ auto | ☑ auto |

## Smoke non-régression obligatoire

| Critère | Référence | ☐ |
|---------|-----------|---|
| Panier in-place | **L2.1** | ☑ auto |
| Isolation panier / wishlist | **I5 · I6** | ☑ auto |
| Retrait naturel preview | **R2-D1** | ☑ auto |

## Verdict Lot 3quater bis

**Verdict :** ☑ **GO MOA Lot 3quater bis** · ☐ NO GO · (`14.1` · PR #19)

Rapport : [`RAPPORT_RECETTE_SHOP_UX4_LOT3QUATER_BIS_CART_FEEDBACK_20260522.md`](RAPPORT_RECETTE_SHOP_UX4_LOT3QUATER_BIS_CART_FEEDBACK_20260522.md) · recette manuelle PR #19 : [`recette_manuelle_pr19_20260522.json`](recette_manuelle_pr19_20260522.json) (**30/30 OK**)

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
| B7 | Wishlist toggle in-place | ☑ | ☑ | ☑ |
| B8 | Panier in-place | — | ☑ | ☑ |
| B9 | Preview Voir in-place | — | — | ☑ |
| B10 | Destinations secondaires | ☐ | ☐ | ☑ |

## Tests auto complets

Commande identique à [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../REFERENCE_RECETTE_BOUTIQUE_MOA.md) § C + tag `dorevia_marketone_shop_in_place` dès Lot 1.

## Verdict global UX-4

| Verdict | Condition |
|---------|-----------|
| **GO MOA UX-4** | Lots exécutés GO · B1–B10 OK · doctrine respectée |
| **GO partiel** | Lot(s) validé(s) · autres lots pending documenté |
| **NO GO** | Régression bloquante § A référence |

**Verdict global :** ☑ **GO GLOBAL MOA UX-4** (Lots 1–3quater bis validés · version **`19.0.15.14.1`** · PR #19 · 2026-05-22) · ☐ GO partiel · ☐ NO GO

> **Lots 1, 2, 3, 3bis, 3ter, 3quater, 3quater bis** : tous **GO MOA** · réserve **R1** (libellé `Fermer` mobile parfois tronqué en `Ferme`) maintenue **documentaire non bloquante** · réserve **V3q-contrast** (lisibilité pill `Ajouter` selon contrastes images futures) **non bloquante**.
> **Lot 4** : régression B1–B10 reste à rejouer à chaque évolution future.

---

## Grille d’exécution

| Date | Lot | Version | Exécuteur | Verdict | Rapport |
|------|-----|---------|-----------|---------|---------|
| 2026-05-22 | L1 | `19.0.15.11.1` | MOA | **GO avec réserve documentaire** | [`RAPPORT_RECETTE_SHOP_UX4_IN_PLACE_20260522.md`](RAPPORT_RECETTE_SHOP_UX4_IN_PLACE_20260522.md) |
| 2026-05-22 | L2 | `19.0.15.12.3` | MOA | **GO avec réserve documentaire** | [`RAPPORT_RECETTE_SHOP_UX4_LOT2_IN_PLACE_20260522.md`](RAPPORT_RECETTE_SHOP_UX4_LOT2_IN_PLACE_20260522.md) |
| 2026-05-22 | L3 | `19.0.15.13.1` | MOA | **GO avec réserve documentaire** (PR #14) | [`RAPPORT_RECETTE_SHOP_UX4_LOT3_IN_PLACE_20260522.md`](RAPPORT_RECETTE_SHOP_UX4_LOT3_IN_PLACE_20260522.md) |
| 2026-05-22 | L3 | `19.0.15.13.2` | MOA | **GO avec réserve documentaire** (G3.9 · PR #15) | idem |
| 2026-05-22 | L3bis | `19.0.15.13.4` | MOA | **GO avec réserve documentaire** (V3bis.12 · PR #16) | [`RAPPORT_RECETTE_SHOP_UX4_LOT3BIS_PREVIEW_PREMIUM_20260522.md`](RAPPORT_RECETTE_SHOP_UX4_LOT3BIS_PREVIEW_PREMIUM_20260522.md) |
| 2026-05-22 | L3ter | `19.0.15.13.5` | MOA | **NO GO** (V3ter.1 image/tap preview KO) | [`RAPPORT_RECETTE_SHOP_UX4_LOT3TER_IMAGE_PREVIEW_CLICK_20260522.md`](RAPPORT_RECETTE_SHOP_UX4_LOT3TER_IMAGE_PREVIEW_CLICK_20260522.md) |
| 2026-05-22 | L3ter | `19.0.15.13.6` | MOA | **NO GO maintenu** (image + Voir preview KO) | [`RAPPORT_RECETTE_SHOP_UX4_LOT3TER_IMAGE_PREVIEW_CLICK_20260522.md`](RAPPORT_RECETTE_SHOP_UX4_LOT3TER_IMAGE_PREVIEW_CLICK_20260522.md) |
| 2026-05-22 | L3ter | `19.0.15.13.7` | MOA | **NO GO maintenu** (V3ter.1–8 rejoué · preview KO) | [`RAPPORT_RECETTE_SHOP_UX4_LOT3TER_IMAGE_PREVIEW_CLICK_20260522.md`](RAPPORT_RECETTE_SHOP_UX4_LOT3TER_IMAGE_PREVIEW_CLICK_20260522.md) |
| 2026-05-22 | L3ter | `19.0.15.13.8` | MOA | **GO MOA** (V3ter.1–8 OK · smoke OK) | [`RAPPORT_RECETTE_SHOP_UX4_LOT3TER_IMAGE_PREVIEW_CLICK_20260522.md`](RAPPORT_RECETTE_SHOP_UX4_LOT3TER_IMAGE_PREVIEW_CLICK_20260522.md) |
| 2026-05-22 | L3ter | `19.0.15.13.8` | Dev (Playwright 390 px) | **GO contre-recette** (V3ter.1–8 OK · 104 tests OK · 0 console error · réserve R1 conservée) | [`recette_ux4_l3ter_13_8_v3ter_1_8_result.json`](recette_ux4_l3ter_13_8_v3ter_1_8_result.json) |
| 2026-05-22 | **L1 + L2 + L3 + L3bis + L3ter + B1** | `19.0.15.13.8` | Dev (Playwright multi-viewport) | **GO recette manuelle complète** (64/64 OK · 0 console error · 0 request fail · 194 tests auto OK) | [`RAPPORT_RECETTE_MANUELLE_COMPLETE_UX4_13_8_20260522.md`](RAPPORT_RECETTE_MANUELLE_COMPLETE_UX4_13_8_20260522.md) |
| 2026-05-22 | **L3bis V3bis.12 ciblée** | `19.0.15.13.8` | Dev (Playwright desktop 1440 + mobile 390 px) | **GO retrait naturel rejoué** (D1–D6 OK · M1–M6 OK · 13/13 · 0 console error) | [`recette_v3bis12_13_8_20260522.json`](recette_v3bis12_13_8_20260522.json) |
| 2026-05-22 | **L3ter I1–I8 clic image (desktop + mobile)** | `19.0.15.13.8` | Dev (Playwright 1440 + 390 px) | **GO clic image tuile = CTA Voir** (Desktop I1·I2·I3·I5·I6·I7·I8 OK · Mobile I1·I2·I4·I5·I6·I7·I8 OK · 14/14 · 0 console error) | [`recette_image_click_I1_I8_13_8_20260522.json`](recette_image_click_I1_I8_13_8_20260522.json) |
| **2026-05-22** | **UX-4 GLOBAL** | **`19.0.15.13.8`** · `9e14e15` | **MOA** | ☑ **GO GLOBAL MOA UX-4 — clôture documentaire** (Lots 1–3ter validés · 64/64 navigateur · 194/194 auto · V3bis.12 OK · I1–I8 OK · R1 maintenue non bloquante) | § [Clôture documentaire UX-4](#clôture-documentaire-ux-4--version-de-référence-1901513-8) |
| 2026-05-22 | **Correctif R2 — retrait naturel intelligent** | **`19.0.15.13.9`** | Dev (Playwright 1440 + 390 px) | **GO R2** · bug scroll-pendant-hover corrigé · 16/16 OK · 0 console error · smoke G3.9 OK | [`recette_R2_hover_scroll_13_9_20260522.json`](recette_R2_hover_scroll_13_9_20260522.json) |
| 2026-05-22 | **L3quater + L3quater bis** | **`19.0.15.14.1`** · PR **#19** | **MOA** | ☑ **GO MOA PR #19** (V3quater + V3qB + smoke **30/30** · tests **29/29** · merge `9327254`) | [`recette_manuelle_pr19_20260522.json`](recette_manuelle_pr19_20260522.json) · [`RAPPORT_RECETTE_SHOP_UX4_LOT3QUATER_CART_CTA_TILE_20260522.md`](RAPPORT_RECETTE_SHOP_UX4_LOT3QUATER_CART_CTA_TILE_20260522.md) · [`RAPPORT_RECETTE_SHOP_UX4_LOT3QUATER_BIS_CART_FEEDBACK_20260522.md`](RAPPORT_RECETTE_SHOP_UX4_LOT3QUATER_BIS_CART_FEEDBACK_20260522.md) |

---

## Clôture documentaire UX-4 — version de référence `19.0.15.14.1`

> **GO GLOBAL MOA maintenu** · version de référence UX-4 actuelle **`19.0.15.14.1`** · PR **#19** mergée (`9327254` · commits `3f695b1` + `a859c9e`).
> Lots 3quater + 3quater bis : harmonisation visuelle CTA panier tuile + feedback contextualisé « Voir le panier » · périmètre QWeb + SCSS · exception JS défensive preview uniquement.

### Comportements cibles validés

| Cible | État `19.0.15.13.8` |
|-------|---------------------|
| **Image tuile** → preview produit (offcanvas desktop · inline mobile) | ☑ GO |
| **CTA « Voir »** → preview produit (offcanvas desktop · inline mobile) | ☑ GO |
| **Panier** overlay → action panier isolée · pas de preview parasite | ☑ GO |
| **Wishlist** overlay → action wishlist isolée · pas de preview parasite | ☑ GO |
| **Titre produit** → fiche produit complète | ☑ GO |
| **Preview premium** (chips, fond pastel CK, image `contain`, header « Découvrir le produit ») | ☑ GO |
| **Retrait naturel** (clic hors panneau · scroll hors panneau · scroll DANS panneau préservé · tap hors mobile) | ☑ GO (V3bis.12) |
| **Fermetures historiques** (× · ESC · re-clic « Voir » · bouton **Fermer** mobile) | ☑ GO (G3.9) |
| **URL `/shop`** conservée pendant preview | ☑ GO |
| **Desktop ≥ 992 px** + **Mobile 390 px** sans débordement horizontal | ☑ GO |
| **Console** sans erreur JS bloquante (Playwright + tests auto) | ☑ GO |
| **CTA panier tuile** — icône + `Ajouter` overlay bas-droit · feedback « Voir le panier » contextualisé (desktop hover · mobile inline) | ☑ GO (PR #19 · `14.1`) |

### Couverture preuve

| Source | Volume | Verdict |
|--------|--------|---------|
| Tests auto (`dorevia_marketone_*`) | 194 tests | 0 failed · 0 error |
| Recette manuelle complète Lots 1→3ter + B1 (Playwright multi-viewport) | 64 contrôles | 64/64 OK |
| Recette ciblée V3bis.12 (Playwright 1440 + 390 px) | 13 contrôles | 13/13 OK |
| Recette ciblée I1–I8 clic image (Playwright 1440 + 390 px) | 14 contrôles | 14/14 OK |
| Console / requêtes réseau bloquantes | — | 0 |

### Réserves maintenues — documentaires non bloquantes

| ID | Réserve | Statut | Impact |
|----|---------|--------|--------|
| **R1** | Libellé bouton **Fermer** mobile parfois tronqué en `Ferme` | Maintenue | Cliquable · non bloquant |
| **L1.C1 / L1.C2** | Scénario connecté Lot 1 non rejoué faute de compte test MOA | Maintenue | Périmètre visiteur public OK |
| **L2.C1** | Scénario connecté Lot 2 non rejoué faute de compte test MOA | Maintenue | Périmètre visiteur public OK |
| **L3.V1** | Fallback multi-variante / configurable à rejouer dès produit publié | Maintenue | Aucun produit éligible publié au moment du GO |
| **V3q-contrast** | Lisibilité pill `Ajouter` selon contrastes visuels des futures images produits | Maintenue | Non bloquante · surveillance continue |

### Règles maintenues post-GO global UX-4

> Toute évolution dérogeant aux règles ci-dessous **requiert un nouvel arbitrage MOA explicite** avant ouverture de branche.

| # | Règle |
|---|-------|
| **R-UX4-1** | Aucune **extension preview V2** (deep-link, ouverture preview cross-page, scroll-locking, etc.) sans arbitrage MOA dédié |
| **R-UX4-2** | Aucun **configurateur preview** : produit multi-variante / configurable → **fallback fiche produit** obligatoire |
| **R-UX4-3** | Aucune **modification profonde** de la fiche produit (PDP `/shop/<slug>`) sans arbitrage MOA dédié |
| **R-UX4-4** | Aucune **modification profonde** du tunnel panier (`/shop/cart`, `/shop/checkout`) sans arbitrage MOA dédié |
| **R-UX4-5** | Toute évolution UX-4 doit prouver (a) le nouveau comportement et (b) **non-régression Lots 1→3ter + B1–B10** |
| **R-UX4-6** | Tout passage de version impose : tests auto verts + recette manuelle Lots 1→3ter + smoke `RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md` |
| **R-UX4-7** | Réserve **R1** doit être traitée lors d'un futur passage visuel premium · pas de remontée bloquante d'ici là |
| **R-UX4-8** | **Retrait naturel intelligent** — la preview reste ouverte tant que l'utilisateur l'explore (survol · scroll dans le panneau · clic dans le panneau) · elle se retire uniquement quand l'utilisateur reprend la navigation boutique hors preview |
| **R-UX4-9** | **CTA panier tuile explicite** — icône panier + libellé court `Ajouter` sur la tuile · cohérent avec le CTA complet `Ajouter au panier` de la preview · overlay compact bas-droit |
| **R-UX4-10** | **Pas de lien panier sur tuile** — après ajout panier, la tuile ne porte pas de lien `Voir le panier` · navigation panier via header uniquement · feedback tuile = bordure sauge + (mobile) label discret « Ajouté au panier » |

| **Sandbox** | Polices Google Fonts CORS · lazy bundle / images annulées | Filtrée | Non-fonctionnelles |

### Références preuve `19.0.15.14.1` (version de référence actuelle)

| Document | Rôle |
|----------|------|
| [`recette_manuelle_pr19_20260522.json`](recette_manuelle_pr19_20260522.json) | Recette manuelle PR #19 — V3quater + V3qB + smoke (**30/30**) |
| [`recette_v3qb_14_1_20260522.json`](recette_v3qb_14_1_20260522.json) | V3qB.1–9 desktop + mobile (**18/18**) |
| [`recette_v3quater_14_0_20260522.json`](recette_v3quater_14_0_20260522.json) | V3quater.1–8 desktop + mobile (**14/14**) |
| [`RAPPORT_RECETTE_SHOP_UX4_LOT3QUATER_CART_CTA_TILE_20260522.md`](RAPPORT_RECETTE_SHOP_UX4_LOT3QUATER_CART_CTA_TILE_20260522.md) | Rapport Lot 3quater |
| [`RAPPORT_RECETTE_SHOP_UX4_LOT3QUATER_BIS_CART_FEEDBACK_20260522.md`](RAPPORT_RECETTE_SHOP_UX4_LOT3QUATER_BIS_CART_FEEDBACK_20260522.md) | Rapport Lot 3quater bis |
| Captures `recette_v3qb_14_1_*` · `recette_v3quater_14_0_*` | Preuves visuelles desktop + mobile |

| Document | Rôle |
|----------|------|
| [`RAPPORT_RECETTE_MANUELLE_COMPLETE_UX4_13_8_20260522.md`](RAPPORT_RECETTE_MANUELLE_COMPLETE_UX4_13_8_20260522.md) | Rapport recette manuelle complète Lots 1→3ter + B1 (64/64) — base 13.8 |
| [`RAPPORT_RECETTE_SHOP_UX4_LOT3TER_IMAGE_PREVIEW_CLICK_20260522.md`](RAPPORT_RECETTE_SHOP_UX4_LOT3TER_IMAGE_PREVIEW_CLICK_20260522.md) | Rapport Lot 3ter — historique passes 13.5 → 13.8 |
| [`recette_R2_hover_scroll_13_9_20260522.json`](recette_R2_hover_scroll_13_9_20260522.json) | **R2 retrait naturel intelligent** desktop + mobile 13.9 (16/16) |
| [`recette_v3bis12_13_8_20260522.json`](recette_v3bis12_13_8_20260522.json) | V3bis.12 retrait naturel desktop + mobile (13/13) |
| [`recette_image_click_I1_I8_13_8_20260522.json`](recette_image_click_I1_I8_13_8_20260522.json) | I1–I8 clic image desktop + mobile (14/14) |
| [`recette_ux4_l3ter_13_8_v3ter_1_8_result.json`](recette_ux4_l3ter_13_8_v3ter_1_8_result.json) | V3ter.1–8 mobile 390 px |
| [`recette_manuelle_complete_13_8_20260522.json`](recette_manuelle_complete_13_8_20260522.json) | Résultats bruts recette manuelle complète (64/64) |
| Captures `capture_*_13_8_*_20260522.png` + `capture_R2_13_9_*_20260522.png` | Preuves visuelles desktop + mobile · L1→L3ter · V3bis.12 · I1–I8 · R2 |

---

## Fichiers Lot 1 (implémentation)

| Fichier | Rôle |
|---------|------|
| `controllers/website_sale_wishlist.py` | Route `remove_by_product` |
| `static/src/interactions/marketone_shop_wishlist_toggle.js` | Interaction Odoo 19 — toggle grille |
| `views/pages/shop_product_tile_conversion.xml` | QWeb `_is_in_wishlist` |
| `static/src/scss/_shop_product_cards.scss` | Feedback carte |
| `tests/test_marketone_shop_in_place.py` | Tests auto |
