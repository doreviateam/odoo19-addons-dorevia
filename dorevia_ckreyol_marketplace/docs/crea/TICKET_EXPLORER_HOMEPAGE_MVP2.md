# TICKET — Explorer Homepage MVP2 (grille asymétrique)

**ID** : `EXPLORER-HOMEPAGE-MVP2`  
**Date d’ouverture** : 2026-04-24  
**Priorité** : **P1** (bloc stratégique homepage).  
**Statut** : **Clôturé — GO MOA (2026-04-24)** — preuve : [PV_RECETTE_EXPLORER_HOMEPAGE_MVP2_CK.md](PV_RECETTE_EXPLORER_HOMEPAGE_MVP2_CK.md) (réserve mineure §3).  
**Exécution : clos** — checklists §0 soldées ; homepage MVP2.1 : voir [README MVP 02](../mvp_02/README.md).  
**Module** : `dorevia_ckreyol_marketplace`  
**Périmètre** : **bloc Explorer uniquement** (`views/snippets/ckr_entries.xml` + SCSS / JS associés si périmètre rail modifié).

**Décision MOA** : [DECISION_EXPLORER_HOMEPAGE_MVP2.md](../mvp_02/DECISION_EXPLORER_HOMEPAGE_MVP2.md) (grille asymétrique MVP2, ordre des portes).

**Rattachement** : [TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md](TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md) ; peut être livré **après** ou **en parallèle** du hero V2 — coordonner conflits Git sur `ckr_homepage.xml` / assets.

---

## Contexte

Décision MOA validée : **remplacer le rail V1** par une **grille asymétrique MVP2**.  
Voir [DECISION_EXPLORER_HOMEPAGE_MVP2.md](../mvp_02/DECISION_EXPLORER_HOMEPAGE_MVP2.md).  
Cadrage §2 : [1_HOMEPAGE.md](../mvp_02/1_HOMEPAGE.md).

---

## Objectif

Transformer le bloc **Explorer** en zone d’**orientation claire** vers les **5 portes catalogue** CK (sans dupliquer le menu principal).

---

## Périmètre

### Structure cible (desktop)

Grille **asymétrique** ; hiérarchie visuelle :

| # | Porte | Poids carte |
|---|--------|-------------|
| 1 | **Promotions** | Dominante |
| 2 | **Kits** | Secondaire fort |
| 3 | **Catégories** | Carte simple |
| 4 | **Collections** | Carte simple |
| 5 | **Origines** | Carte simple |

### Routes (`href` — contrats MVP1 inchangés)

| Porte | Route |
|--------|--------|
| Promotions | `/promotions` |
| Kits | `/kits` |
| Catégories | `/categories` |
| Collections | `/collections` |
| Origines | `/origines` |

*(Comportements détaillés : [SPEC_SHOP_PORTES.md](../mvp_01/SPEC_SHOP_PORTES.md), `docs/mvp_01/`.)*

---

## Rendu attendu

- **5 cartes** visibles sur desktop dans l’**ordre validé** ;
- **Carte entière** cliquable ;
- **Hover / focus** sobres ;
- **Visuels** cohérents CK ; **textes** courts et lisibles ;
- **Pas d’autoplay** ;
- **Responsive** mobile propre (empilement / breakpoints — cf. maquette ou ticket §0).

---

## Contraintes

- Remplacer le **rail V1** uniquement **dans ce bloc** ;
- **Ne pas** modifier le **menu principal** ;
- **Ne pas** changer les **contrats d’URL** [MVP1](../mvp_01/) (chemins ci-dessus) ;
- Pas de **visuel abstrait** décoratif ; pas de **faux packaging** ; pas de **surcharge** d’animation.

---

## Technique (attendu)

- **Modification QWeb** autorisée (grille, ordre DOM, adaptation / suppression nav prev-next si hors périmètre) ;
- **Adaptation SCSS** autorisée (layout asymétrique, responsive) ;
- Vérifier **accessibilité** clavier / focus / rôles ARIA (révision si le pattern n’est plus un rail `carrousel`) ;
- **Préserver** l’ancre **`#explorer-catalogue`** sur la section si elle est **référencée** (liens internes, tests, analytics) — à vérifier dans le snippet avant merge.

---

## Hors périmètre

- **Aucune** nouvelle porte catalogue ;
- **Pas** de refonte globale de **`/shop`** ;
- **Pas** de modification des **routes / contrats** MVP1 au-delà du **réordonnancement DOM** et du **layout** dans ce snippet.

---

## Critères d’acceptation

- [x] Les **5 portes** sont présentes dans l’**ordre** : Promotions → Kits → Catégories → Collections → Origines ;
- [x] **Promotions** est **visuellement dominante** ; **Kits** est **secondaire fort** ; les **3** autres cartes sont **équilibrées** (simples) ;
- [x] Chaque carte mène à la **bonne** route (table Routes) ;
- [x] **Desktop** et **mobile** validés MOA ;
- [x] **Pas d’autoplay** ; hover / focus sobres ;
- [x] Cohérence [SPEC_SHOP_PORTES.md](../mvp_01/SPEC_SHOP_PORTES.md) côté serveur / portes (inchangé hors front) ;
- [x] **WIREFRAME** [Bloc 3](../direction/WIREFRAME_HOMEPAGE.md) aligné **avec** la PR ou commit doc **immédiatement après** merge.

---

## Recette

- **PV** : [PV_RECETTE_EXPLORER_HOMEPAGE_MVP2_CK.md](PV_RECETTE_EXPLORER_HOMEPAGE_MVP2_CK.md) ;
- Validation **MOA** desktop + mobile ; cohérence marque ([PLATEFORME_MARQUE_CK_V1.md](PLATEFORME_MARQUE_CK_V1.md)).

---

## 0. Prêt pour dev — checklist pilotage *(soldée — clos 2026-04-24)*

1. [x] **Branche** / intégration — livrée (module ≥ `19.0.1.8.2`).
2. [x] **Spec** — grille asymétrique **8+4**, responsive (recette MOA).
3. [x] **Ordre DOM** — **Promotions → Kits → Catégories → Collections → Origines**.
4. [x] **Copy** — validée MOA ([PV](PV_RECETTE_EXPLORER_HOMEPAGE_MVP2_CK.md) §3).
5. [x] **Visuels** — 5 assets `static/src/img/` (cf. README module).
6. [x] **Accessibilité** — recette MOA (focus / clavier).
7. [x] **WIREFRAME / doc** — alignés avec la livraison (cf. historique ticket).
8. [x] **`__manifest__.py`** — bump effectué en phase de livraison.
9. [x] **Recette** — [PV_RECETTE_EXPLORER_HOMEPAGE_MVP2_CK.md](PV_RECETTE_EXPLORER_HOMEPAGE_MVP2_CK.md) **GO MOA**.
10. [x] **Instance / relecteur** — recette MOA complétée.

---

## Livrables techniques (synthèse)

| Livrable | Détail |
|----------|--------|
| **QWeb** | Grille asymétrique ; 5 cartes réordonnées ; rail + nav retirés (MVP2). |
| **SCSS** | Spans dominants / secondaire / simples ; responsive. |
| **Routes** | `href` strictement selon table **Routes** (MVP1). |

---

## Historique

| Date | Changement |
|------|------------|
| 2026-04-24 | Création — suite [DECISION_EXPLORER_HOMEPAGE_MVP2.md](../mvp_02/DECISION_EXPLORER_HOMEPAGE_MVP2.md). |
| 2026-04-24 | **Réécriture** — structure Contexte / Objectif / Périmètre (grille + routes) ; rendu ; contraintes ; technique (`#explorer-catalogue`) ; hors périmètre ; critères d’acceptation ; recette ; checklist §0 conservée. |
| 2026-04-24 | **Livraison code** `19.0.1.8.0` — `ckr_entries.xml` + `_entries.scss` ; suppression `ckr_entries_carousel.js` ; CTA hero `/origines` ; tests `dorevia_ckr_explorer` ; docs (WIREFRAME, 1_HOMEPAGE, README, DECISION). **Recette MOA / PV** : en attente. |
| 2026-04-24 | **`19.0.1.8.1`** — visuels Explorer (assets `docs/assets` → `static/src/img/`) ; relecture `__manifest__` (RST) ; tests images ; README mapping. **Recette MOA** : toujours attendue. |
| 2026-04-24 | **`19.0.1.8.2`** — asymétrie renforcée (8+4, médias) ; micro-copy MOA ; `explorer_porte_origines.png` ← `mvp02_reference_epices_curry_piments.png`. |
| 2026-04-24 | **Recette MOA** : **GO** (réserve mineure : libellé « coups de cœur » Collections — [PV](PV_RECETTE_EXPLORER_HOMEPAGE_MVP2_CK.md) §3). **Chantier 3/5** (Sélection produits dynamique) : déblocable. |
| 2026-04-25 | **Documentation** — statut ticket **Clôturé** ; **Exécution : clos** ; checklists §0 soldées (alignement homepage MVP2.1 close MOA). |
