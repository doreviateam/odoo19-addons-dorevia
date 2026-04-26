# Ticket dev — Boutique MVP2.2 **Vague 1 visible** (retail / risque maîtrisé)

| Champ | Valeur |
|--------|--------|
| **Périmètre** | Page boutique `/shop` (et lectures convergentes : catégorie, portes `ckr_mode`, contexte collections) — **habillage retail** sans refonte moteur catalogue |
| **Statut ticket** | **MOA Vague 1 validé** — **implémentation** selon ordre **C → D → E0 → B → A** ; ne pas rouvrir le moteur **`website_sale`**. |
| **Validation MOA** | **2026-04-25** — go implémentation ; objectif : page boutique **visible, dense, retail** ; **E2** / sidebar structurelle **hors** vague (**E0** seulement, pas de double logique filtres). |
| **Cadrage MOA** | [2_SHOP.md](../mvp_02/2_SHOP.md) ; portes et URLs : [SPEC_SHOP_PORTES.md](../mvp_01/SPEC_SHOP_PORTES.md) |
| **Date** | 2026-04-25 |

**Chaîne documentaire** :

```text
2_SHOP.md
→ structure cible MVP2.2 (grille, carte, barre, hero, sidebar)

SPEC_SHOP_PORTES.md
→ contrats portes / modes (pas de nouvelle logique métier dans ce ticket)

docs/crea/TICKET_SHOP_MVP22_VISIBLE_WAVE1.md
→ Vague 1 : ordre C → D → E0 → B → A (1re passe) — critères d’acceptation + estimation
```

**Règles d’or de la Vague 1** :

```text
1. Standard Odoo d’abord : un seul formulaire / un seul moteur de tri natif (pas de duplication).
2. Pas de refonte structurelle sidebar (pas de lot E2) ; pas de double logique filtres / collections.
3. Pas de gestion BO riche des images hero par contexte dans cette vague.
4. Pas de nouvelle logique métier catalogue (domaines, modes, collections déjà livrés inchangés).
```

**Règle transversale d'orchestration / cleanup** :

```text
1. Un seul H1 visible.
2. Un seul bloc contextuel visible : hero CK OU bandeau porte historique.
3. Pas d'empilement hero CK + bandeau + titre natif Odoo.
4. En contexte recherche, l'utilitaire prime : pas de grand hero.
5. Les shortcuts commerciaux n'ouvrent aucune seconde logique de filtres.
```

Références d'exécution :

- [SHOP_EXEC_MATRIX.md](../mvp_02/SHOP_EXEC_MATRIX.md)
- [SHOP_COMPONENT_CONTRACTS.md](../mvp_02/SHOP_COMPONENT_CONTRACTS.md)

**Conventions Git** *(proposition)* :

| Élément | Valeur |
|---------|--------|
| **Branche** | `feature/shop-mvp22-visible-wave1` |
| **Commit** *(message type)* | `feat(shop): mvp22 wave1 grid, product card, toolbar, hero, sidebar skin` |

---

## Objectif

Livrer une **première vague visible** de la page boutique **MVP2.2** : densité retail, carte produit structurée, barre commerciale au-dessus de la grille, hero pleine largeur (passe simple), habillage léger de la sidebar native — **sans** ouvrir les chantiers lourds (E2, hero multi-images BO, duplication du tri).

**Direction validée** : obtenir une page boutique **visible, dense et retail** en **habillant** le standard **`website_sale`** (présentation, QWeb ciblé, SCSS) — **pas** de remise en cause du **moteur** de listing / filtres / panier natifs.

---

## Périmètre inclus (Vague 1)

| Lot | Intitulé |
|-----|----------|
| **C** | Grille produits responsive dense |
| **D** | Carte produit V1 |
| **E0** | Sidebar légère (habillage natif) |
| **B** | Barre commerciale au-dessus des produits |
| **A** | Hero boutique — **première passe** (pleine largeur, copy contextuelle, fond simple) |

## Hors périmètre explicite

- Refonte sidebar en **4 blocs dédiés** (E2) et logique filtres sur mesure.
- **Gestion BO riche** des images hero par contexte (6 jeux, champs `website` dédiés, etc.).
- **Duplication** du contrôle de **tri** ou second formulaire de tri.
- Nouvelle logique métier catalogue (nouveaux `ckr_mode`, nouveaux domaines, etc.).

---

## Arbitrages MOA actés — Vague 1 *(2026-04-25)*

Décisions reprises dans [2_SHOP.md §3 / §7 / §8 / §11](../mvp_02/2_SHOP.md). **Aucun arbitrage MOA supplémentaire** n’est requis pour enchaîner **C → D → E0 → B → A**.

### MOA-1 — Wishlist *(acté)*

- Afficher le **wishlist** sur les cartes **uniquement** si **`website_sale_wishlist`** est **installé** et **retenu** dans le **périmètre prod**.
- Sinon : l’**emplacement** reste prévu dans la **grammaire de carte** (layout Vague 1), mais le **bouton wishlist n’est pas affiché** ; pas de placeholder vide ni trou visuel incohérent.

### MOA-2 — Asset hero *(acté)*

- **Fallback visuel charte** par défaut (dégradé / couleurs charte).
- **Image statique unique** autorisée **uniquement** si elle existe **déjà** dans les assets du module (pas de nouveau flux média BO pour la Vague 1).
- **Pas** de gestion BO riche ; **pas** de **6 images** contextuelles administrables en BO dans cette vague.
- Les **images distinctes par porte** restent **hors périmètre Vague 1** (report MVP2.2 ultérieur ou vague suivante).

### MOA-3 — Copy hero *(acté)*

- **Réutiliser** les textes **existants** des **bandeaux** actuels (titres / intros par contexte).
- **Pas** d’atelier copy complet à ce stade ; **ajustements courts** uniquement si une **incohérence visible** apparaît.

### MOA-4 — Catégorie native + hero *(acté)*

- Conserver la **logique native Odoo** des catégories (`/shop/category/<id>-<slug>`).
- **Pas** d’empilement « titre catégorie Odoo + hero CK » : **un seul** niveau de **titre principal** visible.
- Si le **hero CK** est présent sur la page catégorie, il **porte le titre de la catégorie** (source de vérité : nom catégorie natif) ; le **titre catégorie** du template standard est **masqué / retiré** du rendu pour éviter la redondance.
- Le **fil d’Ariane** (breadcrumb) natif peut **rester** s’il reste **lisible** et non redondant avec le hero.

### MOA-5 — Hiérarchie badges (carte produit) *(acté)*

**Priorité d’affichage recommandée** (un signal « gagne » quand plusieurs seraient applicables) :

1. **Rupture**
2. **Promotion**
3. **Nouveau** / **Sélection** *(selon signaux disponibles sur la tuile / standard)*
4. **Pack** / **Incontournable** *si utile dans le contexte liste*

- **Éviter** d’afficher **plusieurs badges concurrents** sur une même carte si cela **surcharge** le rendu ; privilégier **un seul** badge prioritaire (exception documentée en PR si le standard impose un second signal non masquable).

---

## Risques et mitigations

| Risque | Gravité | Mitigation |
|--------|---------|------------|
| Structure QWeb **`website_sale`** différente selon mineure Odoo 19 | Moyenne | Xpath défensifs, tests visuels, limiter les surcharges au strict nécessaire |
| **Tri** : repositionnement CSS casse le layout ou l’accessibilité | Moyenne | Préférer **déplacement DOM minimal** ; si impossible, garder tri en place native et documenter |
| **Compteur** : `search_count` non disponible sur tous les contextes | Faible | Masquer le compteur si absent ; pas de requête SQL parallèle |
| **Promo / rupture** sur tuile : données `combination_info` / ribbons incomplets selon config | Moyenne | S’aligner sur le comportement **standard** du listing ; documenter les prérequis pricelist / stock |
| Conflit **hero** avec **bandeaux porte** existants (`ckr_shop_*_banner`) | Moyenne | **Orchestration** : un seul bloc hero visible ; réutiliser les variables QWeb existantes où possible |
| Empilement **hero + shortcuts + header natif** avant la grille | Moyenne | Vérifier la matrice d’exécution ; supprimer tout doublon de titre / contexte ; compacter les zones de pilotage |
| Sidebar visuellement plus forte que la grille | Moyenne | Limiter le poids du rail natif ; préférer la lisibilité à l’effet panneau pleine hauteur |

---

## Ordre d’implémentation *(figé — validation MOA 2026-04-25)*

1. **C** — Grille produits responsive dense.
2. **D** — Carte produit V1 *(couplage visuel avec C)*.
3. **E0** — Habillage léger de la **sidebar native** *(pas E2 ; pas de double logique filtres)*.
4. **B** — Barre commerciale au-dessus des produits *(compteur, tri natif)*.
5. **A** — Hero première passe *(copy bandeaux existants, fond MOA-2)*.

---

## Lots — livrables et critères d’acceptation

### Lot C — Grille produits responsive dense

**Livrables** : SCSS (prioritaire) dans `static/src/scss/layout/_shop.scss` (ou fichier dédié importé) ; ajustements QWeb **minimes** si le core impose des classes colonnes.

**Critères d’acceptation** :

- [ ] **Desktop large** : **4** colonnes produits (zone grille principale).
- [ ] **Desktop moyen** : **3** colonnes.
- [ ] **Tablette** : **2** colonnes.
- [ ] **Mobile** : **1** ou **2** colonnes selon breakpoint retenu pour lisibilité (documenter le choix dans la PR).
- [ ] **Gouttières** et **densité** retail cohérentes avec les tokens charte (pas d’effet « galerie trop aérée »).
- [ ] Pas de régression sur **pagination**, **layout** filtre offcanvas mobile natif.
- [ ] Vérification sur **au moins** : `/shop` nu, `/shop?ckr_mode=promo`, `/collections` (vue grille).

**Type technique** : principalement **SCSS** ; risque **Δ** standard : **faible**.

---

### Lot D — Carte produit V1

**Livrables** : héritage QWeb sur le template de tuile liste `website_sale` (fichier existant `views/pages/ckr_shop.xml` ou vue dédiée) ; SCSS carte.

**Critères d’acceptation** :

- [ ] **Image** : ratio homogène (`object-fit` / hauteur maîtrisée), pas de tuiles visuellement disjointes.
- [ ] **Badge** : zone **haut gauche** ; **une** pastille prioritaire selon **MOA-5** (rupture > promo > nouveau/sélection > pack/incontournable si utile) ; **pas** d’empilement de badges concurrents si cela surcharge la carte.
- [ ] **Wishlist** : zone **haut droite** **uniquement si** `website_sale_wishlist` est **installé** et **retenu** en prod ; sinon **grammaire de carte** respectée mais **bouton non affiché**, sans trou visuel (**MOA-1 acté**).
- [ ] **Micro-info** : catégorie ou info courte sous l’image (selon données dispo standard).
- [ ] **Nom produit** : lisible, hiérarchie typographique charte.
- [ ] **Prix** : visible ; état **promo** : ancien prix barré + prix courant si le standard l’expose sur la tuile.
- [ ] **Ajout panier** : **bas droite** (ou alignement équivalent Stitch) ; **rupture** : bouton désactivé ou masqué selon comportement natif + indication claire.
- [ ] Pas de **double** bouton panier / double lien produit.
- [ ] Tests manuels : produit normal, promo, indisponible (si jeu de données disponible).

**Type technique** : **QWeb** `website_sale` + **SCSS** ; risque **Δ** standard : **moyen**.

---

### Lot B — Barre commerciale au-dessus des produits

**Livrables** : évolution de `ckr_shop_explorer_shortcuts` (ou équivalent) ; SCSS barre ; complément contrôleur **léger** si nécessaire pour `search_count`.

**Critères d’acceptation** :

- [ ] Chips **Promotions**, **Incontournables**, **Kits** (libellés [ADR-CKR-008](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008) / [2_SHOP.md §5](../mvp_02/2_SHOP.md)) avec liens **existants** (`/promotions`, `/incontournables`, `/kits` ou équivalent déjà en prod).
- [ ] **État actif** cohérent avec le contexte (`ckr_mode`, `/shop` nu = « toute la boutique » si prévu au design).
- [ ] **Compteur** produits : affiché **uniquement** si la valeur est disponible **sans** logique métier dupliquée (ex. `search_count` déjà dans `values`) ; sinon masqué ou report documenté.
- [ ] **Tri** : **une seule** instance du contrôle natif ; **repositionnement** autorisé **uniquement** si le markup reste celui d’Odoo (pas de clone de formulaire).
- [ ] **Responsive** : chips scrollables ou wrap propre tablette/mobile ([2_SHOP.md §5](../mvp_02/2_SHOP.md)).
- [ ] Non-régression : filtres, pagination, `ckr_mode` préservés dans les URLs.

**Type technique** : **QWeb** + **SCSS** ; Python **minimal** ; risque **Δ** standard : **moyen** (surtout tri).

---

### Lot A — Hero boutique — première passe

**Livrables** : bloc hero pleine largeur **au-dessus** de la zone sidebar + grille ; copy pilotée par le **contexte porte** déjà exposé (flags `ckr_*_mode`, contexte collections, etc.) ; fond = **fallback charte** par défaut ; **image statique** module **uniquement** si asset déjà présent (**MOA-2 acté**).

**Critères d’acceptation** :

- [ ] Hero **pleine largeur** du contenu boutique, **au-dessus** des deux colonnes (sidebar + produits).
- [ ] **Copy** : **réutilisation** des textes des **bandeaux actuels** par contexte ; **pas** d’atelier copy complet ; retouches **minimales** seulement si incohérence visible (**MOA-3 acté**).
- [ ] **Pas** de module de **6 images** configurable en BO ; **pas** d’images hero **par porte** dans cette vague (**MOA-2 acté**).
- [ ] **Fallback charte** toujours correct si aucune image module ; image de fond **optionnelle** seulement via asset existant.
- [ ] **Page catégorie** : **un seul** titre principal — le hero porte le **nom catégorie natif** ; pas de double titre avec le header catégorie Odoo ; breadcrumb natif conservé si lisible (**MOA-4 acté**).
- [ ] Accessibilité minimale : contraste texte sur overlay.

**Type technique** : **QWeb** + **SCSS** ; risque **Δ** standard : **moyen** (placement dans `website_sale.products`).

---

### Lot E0 — Sidebar légère

**Livrables** : SCSS (accordéon visuel, espacements, titres facettes) ; xpath **léger** sur templates filtres natifs si nécessaire pour classes / wrappers.

**Critères d’acceptation** :

- [ ] **Panneau filtres natif** `website_sale` : lisibilité retail améliorée (typo, espacements, états ouverts/fermés).
- [ ] **Pas** de nouveaux blocs métier « Catégories / Collections / Origines / Prix » séparés de la sémantique Odoo.
- [ ] **Pas** de seconde logique de navigation collections dans la sidebar.
- [ ] Non-régression : offcanvas mobile, attributs, prix, recherche.

**Type technique** : **SCSS** dominant ; **QWeb** léger ; risque **Δ** standard : **faible**.

---

## Estimation resserrée (Vague 1)

Fourchettes en **jours·dev** (un profil Odoo 19 + connaissance du module CK), **hors** recette MOA complète multi-dispositifs *(arbitrages MOA Vague 1 **clos**)*.

| Lot | Estimation |
|-----|------------|
| **C** | **1,5 — 2,5** |
| **D** | **5 — 8** |
| **B** | **3 — 5** |
| **A** | **4 — 6** |
| **E0** | **1,5 — 2,5** |
| **Buffer intégration / QA croisée** | **1,5 — 2** |
| **Total** | **~16,5 — 26** |

> **Note** : si le repositionnement du **tri** (lot B) s’avère trop intrusif, livrer B **sans** déplacement et réduire B d’environ **0,5 — 1 j**.

---

## Preuve PR / recette technique

- Captures ou courte vidéo : **grille** aux 4 breakpoints ; **carte** (promo + normal) ; **barre** avec états actifs ; **hero** sur 2–3 contextes ; **sidebar** repliée/dépliée.
- **`dorevia_ckr_collections`** (ou tag le plus pertinent déjà utilisé) : **non-régression** si les tests touchent le listing ; sinon jeux manuels documentés sur `/shop` et `/collections`.
- Description PR : lister les **fichiers** `ckr_shop.xml`, `_shop.scss`, éventuel `website_sale` secondaire ; expliciter l’**absence** de duplication du tri et l’**absence** de E2.
- Vérifier explicitement :
  - **un seul `h1`** visible ;
  - **aucune coexistence** `hero CK + bandeau porte historique` ;
  - **pas de grand hero** en contexte `search` ;
  - **sidebar** non dominante au premier écran.

---

## Historique

| Date | Événement |
|------|-----------|
| 2026-04-25 | Création du ticket **Vague 1 visible** MVP2.2 — lots C, D, B, A (1re passe), E0 ; critères d’acceptation, dépendances MOA, risques, estimation resserrée. |
| 2026-04-25 | **Arbitrages MOA actés** : **MOA-2** (fallback charte par défaut ; image statique seulement si asset module existant ; pas de BO riche ni images par porte en V1) ; **MOA-4** (catégorie native ; hero = titre catégorie unique ; pas d’empilement avec header Odoo ; breadcrumb natif si lisible) — aligné **2_SHOP.md** §3 / §8 / §11. |
| 2026-04-25 | **Arbitrages MOA actés (suite)** : **MOA-1** (wishlist seulement si module dans périmètre prod ; sinon emplacement prévu, non affiché) ; **MOA-3** (hero : réutiliser bandeaux existants ; pas atelier copy ; ajustements courts si besoin) ; **MOA-5** (badges carte : priorité rupture > promo > nouveau/sélection > pack/incontournable ; pas de multi-badges qui surchargent) — **2_SHOP.md** §7 / §11. |
| 2026-04-25 | **Confirmation MOA** : libellés MOA-1 (**installé** + périmètre prod ; **grammaire de carte** sans bouton si hors scope), MOA-3, MOA-5 repris tels quels ; **tous les arbitrages Vague 1 sont clos** — enchaînement dev **C → D → E0 → B → A** sans blocage MOA ; statut ticket = prêt implémentation. |
| 2026-04-25 | **Validation MOA — go implémentation** : ordre figé **C → D → E0 → B → A** ; **E2** / sidebar structurelle **hors** vague (**E0** uniquement, pas de double logique filtres) ; objectif page **visible, dense, retail** sans rouvrir le moteur **`website_sale`**. |
