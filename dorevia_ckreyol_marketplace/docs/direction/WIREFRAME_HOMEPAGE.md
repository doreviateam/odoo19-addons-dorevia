# WIREFRAME_HOMEPAGE — C-Kreyol

Ce document décrit la **structure cible de la homepage** de **C-Kreyol** en **Phase 1**.

Il complète :

- [DESIGN.md](DESIGN.md)
- [STRUCTURE_MENU_PRINCIPAL.md](STRUCTURE_MENU_PRINCIPAL.md)
- [NOTE_DE_CADRAGE.md](NOTE_DE_CADRAGE.md)
- [ARCHITECTURE_DECISION_RECORD.md](ARCHITECTURE_DECISION_RECORD.md) (notamment [ADR-CKR-003](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-003), [ADR-CKR-005](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005))
- [SPEC_HERO_HOMEPAGE.md](SPEC_HERO_HOMEPAGE.md) (cadrage du **Bloc 2 — Hero**)
- [CHARTE_GRAPHIQUE_PHASE1.md](CHARTE_GRAPHIQUE_PHASE1.md) (prérequis **visuels** minimaux avant gel du hero)

La homepage doit exprimer la **marque**, la **promesse retail**, la **lisibilité de l’offre** et la **crédibilité du canal**, **sans sur-promesse** ni surcharge (disponibilité, délais — conséquences **ADR-005**).

---

## 1. Rôle de la homepage

La homepage doit :

- présenter immédiatement **C-Kreyol** ;
- faire comprendre ce qui est vendu ;
- orienter vers les bonnes entrées du catalogue ;
- installer une perception **retail** ;
- créer la **confiance** ;
- rester **lisible sur mobile** (must have, cf. note §6.1).

Elle ne doit pas chercher à **tout dire**, ni à reproduire la profondeur d’un **grand agrégateur**.

---

## 2. Principes de construction

- **hiérarchie visuelle** claire ;
- **peu de blocs**, mais bien ordonnés ;
- **équilibre** entre :
  - promesse de **marque**,
  - accès **commercial**,
  - **preuve** de sérieux,
  - **respiration** visuelle ;
- **cohérence** avec la [navigation principale](STRUCTURE_MENU_PRINCIPAL.md) (**Option B** retenue en principe — entrées **Boutique**, **Collections**, **Offrir**, **Recettes**, etc.) ;
- **mobile-first** ;
- **Zéro carrousel imposé** sur le **hero** et sur la **structure principale** du bloc **sélection produits** (cf. §3 Bloc 5) : éviter d’y faire porter la lecture exclusive — risques classiques sur **compréhension**, **mobile**, **performance** et **conversion**. Le **Bloc 3 Explorer** est une **grille asymétrique** de portes (**sans autoplay**) — détail sous le Bloc 3 (*Présentation front*).

---

## 3. Hypothèse de structure Phase 1

Les blocs ci-dessous sont numérotés pour la **lecture** ; l’**ordre vertical** exact et la **densité** sur mobile restent **à arbitrer** avec le contenu réel.

### Bloc 1 — Header / navigation

- menu principal **personnalisé** ([STRUCTURE_MENU_PRINCIPAL.md](STRUCTURE_MENU_PRINCIPAL.md), [ADR-CKR-003](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-003)) ;
- **logo** ;
- accès **panier** / **compte** / **recherche** (zones utilitaires — cohérent avec §6 du document menu).

### Bloc 2 — Hero principal

**Objectif** :

- dire immédiatement ce qu’est **C-Kreyol** ;
- poser la **promesse de marque** ;
- orienter vers l’**action principale**.

**Exigence** : en **une lecture**, le visiteur doit comprendre **qu’il s’agit de produits agro transformés antillais** proposés via un **canal retail digital spécialisé** (marque **C-Kreyol**) — éviter un hero **uniquement** « ambiance marque » **sans** ancrage **offre**.

**Contenus possibles** :

- titre de marque / **proposition de valeur** ;
- court **sous-texte** ;
- **CTA principal** vers la **boutique** ;
- **visuel** fort.

**Cadrage détaillé** (titre, sous-texte, CTA, visuel ; **localisation / provenance** §4) : [SPEC_HERO_HOMEPAGE.md](SPEC_HERO_HOMEPAGE.md).

**Gel Phase 1** (2026-04-21) : **copy** et **direction visuelle** retenus — [SPEC_HERO_HOMEPAGE.md §7](SPEC_HERO_HOMEPAGE.md). **Production des visuels** : [BRIEF_VISUEL_HERO_PHASE1.md](BRIEF_VISUEL_HERO_PHASE1.md).

### Bloc 3 — Explorer / Par où commencer *(addendum Phase 2)*

**Objectif** : distribuer **cinq modes d’entrée dans l’offre produit** (doctrine catalogue), **distincts** de la simple **navigation générale** du header — voir [ADR-CKR-006 / 008](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-006) et [STRUCTURE_MENU_PRINCIPAL.md §11](STRUCTURE_MENU_PRINCIPAL.md).

**Libellés front et ordre d’affichage** (section **Explorer**, grille MVP2) :

1. **Promotions** — avantage commercial *(carte visuellement dominante)* ;
2. **Kits** *(libellé visiteur ; grille back-office / source de vérité : **Pack** — module OCA `product_pack`, `pack_ok`)* — coffrets, assortiments *(carte secondaire forte)* ;
3. **Catégories** — famille de produits *(carte simple)* ;
4. **Collections** — sélection éditoriale *(carte simple)* ;
5. **Origines** — repère géographique *(carte simple)*.

Les libellés sont au **pluriel** et **orientés visiteur** (chaque porte ouvre sur un **ensemble à explorer**) ; ils ne reproduisent pas nécessairement le vocabulaire interne du projet. La porte 3 en est l’illustration : **« Kits »** est le libellé visiteur retenu (plus parlant dans l’univers alimentaire C-Kreyol), **« Pack »** est la grille back-office conservée pour l’implémentation et la source de vérité (règle de bi-lexique [ADR-CKR-008](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008)). Chaque porte doit avoir une **cible** claire, un **comportement** cohérent sur la **Boutique** `/shop` ou pages associées, et une **source de vérité** métier lorsque nécessaire.

**Règle** : ce bloc **n’est pas** la reprise des quatre entrées « Boutique / Collections / Offrir / Recettes » du menu **Option B** ; **Offrir** et **Recettes** restent des **rubriques de site** (menu + blocs éditoriaux éventuels), pas des portes **Explorer** au sens Phase 2.

#### Présentation front (implémentation — **MVP2**)

- **Disposition** : **grille CSS asymétrique** (desktop : Promotions + Kits en première ligne hiérarchisés ; Catégories / Collections / Origines en seconde ligne) ; **empilement** propre en mobile.
- **Contrôle visiteur** : **pas d’autoplay** ; chaque **carte entière** est un lien ; **hover / focus** sobres.
- **Accessibilité** : en-tête de section relié par `aria-labelledby` ; conteneur des liens en `role="navigation"` avec `aria-label` ; focus visible sur les cartes.
- **Mise en page** : en-tête de section **centré** ; **rythme vertical** avec le **hero** et les blocs suivants (tokens de section).
- **Fichiers** : `views/snippets/ckr_entries.xml`, `static/src/scss/components/_entries.scss` (bundle **`web.assets_frontend`** dans `__manifest__.py`).

*(Historique : avant MVP2, un rail horizontal manuel V1 — prev/next, sans autoplay — était décrit ici ; remplacé par la décision [DECISION_EXPLORER_HOMEPAGE_MVP2.md](../mvp_02/DECISION_EXPLORER_HOMEPAGE_MVP2.md), module ≥ 19.0.1.8.0.)*

**Référence Phase 1** : l’intention historique « 2 à 4 cartes sans dupliquer le menu » reste valable en **esprit** (pas de copier-coller du header) ; le **nombre** et le **périmètre** des cartes sont désormais **figés à cinq** par décision produit / ADR.

### Bloc 4 — Mise en avant fournisseur / origine

**Objectif** :

- ancrer l’offre dans le **réel** ;
- faire exister **La Platine** comme **premier fournisseur** **sans absorber** la marque **C-Kreyol**.

**Doctrine** : ce bloc **ancre** l’offre dans un **fournisseur réel** ; il ne doit **pas** transformer la homepage en **page de marque La Platine** ni **inverser** la hiérarchie visuelle **C-Kreyol** → **La Platine**.

### Bloc 5 — Sélection produits / best sellers

**Objectif** :

- montrer rapidement des **produits concrets** ;
- rendre l’offre **achetable** ;

avec **sélections sincères** (cf. [DESIGN.md §5.1](DESIGN.md)) — pas de **sur-promesse** de disponibilité ([ADR-CKR-005](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005)).

**Règles** :

- **sélection courte** (nombre exact **à trancher** — ordre de grandeur **4 à 8** produits en Phase 1 sauf catalogue plus petit) ;
- produits **réellement disponibles** ou **mobilisables** selon les **engagements fournisseurs** et le **stock observable** ;
- **pas** de mise en avant **aspirationnelle** déconnectée de l’**opérable** ;
- **pas** de carrousel comme **structure principale** de ce bloc (cf. §2).

### Bloc 6 — Bloc retail éditorial

**Objectif** : installer une **petite** logique de **collection**, **saison**, **usage** ou **cadeau**.

**Vigilance** : même logique que pour le menu — si **Offrir** / **Recettes** ne sont pas **nourris** crédiblement, **réduire** ou **retirer** ce bloc (repli vers **variante sobre**, §5).

### Bloc 7 — Bloc confiance

**Objectif** : **rassurer** sans alourdir.

**Cadre** : **trois** axes maximum dans le **corps** du bloc pour rester **brefs** et **lisibles** :

1. **Achat** — payer en **confiance** (moyens de paiement, sécurité perçue) ;
2. **Livraison** — promesse **prudente**, alignée sur l’**opérable** ([ADR-CKR-005](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005)) ;
3. **Contact** — accès **humain** / SAV **clair**.

L’**origine produit** peut **monter** dans le **hero** (message sobre, cf. [SPEC_HERO_HOMEPAGE.md](SPEC_HERO_HOMEPAGE.md) §1 / §4) ; les **approfondissements** (fournisseur structurant, **La Platine**, cadre **Nantes** / projet) plutôt **bloc 4** et suivants ou **À propos**. Les thèmes **qualité** ou **détail** peuvent compléter **sans gonfler** le bloc 7.

### Bloc 8 — Footer personnalisé

- liens utiles ;
- **mentions** ;
- **contact** ;
- navigation **secondaire** ([ADR-CKR-003](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-003)).

---

## 4. Ordre de lecture cible

1. **Qui** est C-Kreyol ?
2. **Que** puis-je acheter ici ?
3. **Par où** commencer ?
4. **Pourquoi** faire confiance ?
5. **Comment** aller plus loin ?

---

## 5. Variante sobre

Version avec **peu de blocs** (repli si charge éditoriale ou catalogue **insuffisante** au départ) :

- **Hero**
- **Entrées d’exploration** (nombre réduit)
- **Sélection produits**
- **Bloc confiance**
- **Footer**

*(Le header global reste présent ; il n’est pas compté comme « bloc de contenu » dans cette liste simplifiée.)*

---

## 6. Variante retail enrichie

Version plus **complète**, **alignée** sur le menu **Option B** ([STRUCTURE_MENU_PRINCIPAL.md §10](STRUCTURE_MENU_PRINCIPAL.md)) :

- **Hero**
- **Entrées d’exploration**
- **Mise en avant fournisseur / origine**
- **Sélection produits**
- **Bloc** collection / **Offrir** / **Recettes** (éditorial — **sous réserve** de contenu)
- **Bloc confiance**
- **Footer**

**Hypothèse recommandée à ce stade** : **variante retail enrichie** (§6), sous réserve de la **même vigilance** que pour le menu sur **Offrir** et **Recettes** ; sinon **variante sobre** (§5) en **transitoire** jusqu’à stabilisation du contenu.

---

## 7. Éléments à éviter

- **hero** trop vague ;
- **surcharge** de messages concurrents ;
- **trop** de carrousels ;
- homepage qui cherche à montrer **tout** le catalogue ;
- **sur-promesse** stock / livraison ([ADR-CKR-005](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005), note §12.2) ;
- rendu **standard Odoo** comme état final ([ADR-CKR-003](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-003)) ;
- **front surchargé** (cf. [DESIGN.md §13](DESIGN.md)).

---

## 8. Questions ouvertes

*(Pour le **hero**, voir les arbitrages dans [SPEC_HERO_HOMEPAGE.md](SPEC_HERO_HOMEPAGE.md) — **Nantes** hors hero principal, **La Platine** plutôt **bloc 4+**, **origine produit** légitime dès le hero si sobre.)*

- ~~**combien** d’entrées d’exploration afficher (2, 3 ou 4) ?~~ — **tranché** : **cinq** cartes **Explorer** ([ADR-CKR-008](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008), présent document Bloc 3).
- faut-il un bloc visuel **Offrir** dès l’ouverture ?
- faut-il un bloc **Recettes** dès l’ouverture ?
- **combien** de produits mettre en avant dans la sélection (grille courte) ?

---

## 9. Décision cible à formaliser

**Décision cible Phase 1** :  
La homepage retient la **variante retail enrichie** (§6), **cohérente** avec le menu principal **Option B** ([STRUCTURE_MENU_PRINCIPAL.md §10](STRUCTURE_MENU_PRINCIPAL.md)) :

- **Hero** + **Explorer** (cinq portes : Promotions, **Kits** *(front)* / **Pack** *(back-office)*, Catégories, Collections, Origines) + **mise en avant fournisseur / origine** + **sélection produits** + **bloc éditorial** (collection / Offrir / Recettes selon contenu disponible) + **bloc confiance** + **footer** personnalisé.

**Révision** : si la **charge éditoriale** ou le **catalogue** ne permettent pas une **mise en scène crédible** des blocs **Offrir** / **Recettes** (bloc 3 et/ou bloc 6), basculer en **variante sobre** (§5) jusqu’à stabilisation — sans remettre en cause la **direction** retail.

---

## Historique du document

| Date | Changement |
|------|------------|
| 2026-04-21 | Création : rôle homepage, principes, blocs 1–8, ordre de lecture, variantes sobre / enrichie, hypothèse recommandée, décision cible §9, ADR-003 / ADR-005 ; liens **DESIGN** §7, **README**, **NOTE** §1, **ADR-003**. |
| 2026-04-21 | **Hero** : exigence **une lecture** = offre + canal ; **bloc 3** vs menu ; **doctrine** bloc 4 ; **bloc 7** = 3 axes ; **bloc 5** règles sélection ; **zéro carrousel imposé** §2 / §7 ; lien **[SPEC_HERO_HOMEPAGE.md](SPEC_HERO_HOMEPAGE.md)**. |
| 2026-04-21 | Alignement **SPEC** §4 : **origine** possible **hero** ; **Nantes** / **La Platine** **hors** hero principal ; **bloc 7** ; **§8** questions ouvertes. |
| 2026-04-21 | **Bloc 2** : renvoi **gel** hero Phase 1 — **[SPEC_HERO_HOMEPAGE.md](SPEC_HERO_HOMEPAGE.md) §7**. |
| 2026-04-21 | **Bloc 2** : lien **[BRIEF_VISUEL_HERO_PHASE1.md](BRIEF_VISUEL_HERO_PHASE1.md)** (livrables visuels). |
| 2026-04-21 | **Bloc 3 Explorer** : cinq portes catalogue, distinctes du menu Option B ; libellés front **singuliers** **Promotion**, **Collection**, **Kit**, **Catégorie**, **Origine** (ordre d’affichage ; **Kit** = logique interne composition) ; stub **`/kit`** ; **ADR-006 / 008** ; question « nombre de cartes » close. |
| 2026-04-21 | **Bloc 3 Explorer** — libellés passés au **pluriel** pour harmonisation lecture visiteur : **Promotions**, **Collections**, **Kits**, **Catégories**, **Origines** ; stub **`/kits`** (remplace `/kit`) ; ordre et nombre de cartes inchangés. |
| 2026-04-21 | **Bloc 3 Explorer** — **Kits → Packs** : recadrage après vérification back-office Odoo (case *« Est un pack ? »*, onglet *Pack*) confirmant la logique pack OCA (`product_pack`) comme source de vérité. Libellés retenus désormais : **Promotions**, **Collections**, **Packs**, **Catégories**, **Origines**. Stub **`/packs`** remplace **`/kits`**. La doctrine interne « composition » est retirée de la surface Explorer. |
| 2026-04-21 | **Bloc 3 Explorer** — **règle de bi-lexique** [ADR-CKR-008](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008) : le libellé **visiteur** repasse à **Kits** (univers alimentaire : kit colombo, kit apéritif, kit découverte) ; la **source de vérité** reste **Pack** (module OCA `product_pack`, `pack_ok`). URL visible **`/kits`** ; conventions internes (SPEC, CONTRAT_URL, paramètre CK, domaine) conservées en **Pack**. Libellés Explorer : Promotions, Collections, **Kits**, Catégories, Origines. |
| 2026-04-23 | **§2** : nuance « zéro carrousel imposé » — **hors** Bloc 5 sélection ; **Bloc 3** = rail horizontal **manuel** (sans autoplay). **Bloc 3** : nouveau sous-paragraphe **Présentation front (implémentation)** — boutons prev/next, boucle, accessibilité, titre centré, rythme vertical hero / sections, `dir="ltr"`, fichiers `ckr_entries` + SCSS + JS. |
| 2026-04-24 | **Bloc 3** : passage à la **grille asymétrique MVP2** (ordre Promotions → Kits → Catégories → Collections → Origines) ; documentation **Présentation front** et liste ordre § alignées ; retrait du rail + JS carrousel (module 19.0.1.8.0, [DECISION_EXPLORER_HOMEPAGE_MVP2.md](../mvp_02/DECISION_EXPLORER_HOMEPAGE_MVP2.md)). |
