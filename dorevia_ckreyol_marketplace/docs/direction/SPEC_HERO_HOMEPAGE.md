# SPEC_HERO_HOMEPAGE — C-Kreyol

Ce document **cadre le hero de la homepage** (Phase 1) : **message**, **ton**, **CTA** et **visuel**. Il complète [WIREFRAME_HOMEPAGE.md](WIREFRAME_HOMEPAGE.md) (**Bloc 2**), [DESIGN.md](DESIGN.md), [CHARTE_GRAPHIQUE_PHASE1.md](CHARTE_GRAPHIQUE_PHASE1.md), [DIRECTIONS_ARTISTIQUES_PHASE1.md](DIRECTIONS_ARTISTIQUES_PHASE1.md) (intentions **visuelles** indicatives), [BRIEF_VISUEL_HERO_PHASE1.md](BRIEF_VISUEL_HERO_PHASE1.md) (**production** des assets hero), [STRUCTURE_MENU_PRINCIPAL.md](STRUCTURE_MENU_PRINCIPAL.md) et les [ADR](ARCHITECTURE_DECISION_RECORD.md) pertinents (**ADR-CKR-003** présentation, **ADR-CKR-005** promesse / disponibilité).

Le hero est le **premier arbitrage narratif** de la page — **gelé** pour le **copy** et le **cadrage visuel** Phase 1 au **§7** (2026-04-21) ; l’**implémentation** (assets finaux, thème) suit. **Évolution structurale** hero (MVP 02) : voir **§8** (décision MOA, ticket, alignement **§7** après merge).

---

## 1. Exigence doctrinale (rappel)

En **une lecture**, le visiteur doit comprendre :

- **quoi** : des **produits agro transformés antillais** ;
- **comment** : via un **canal retail digital spécialisé** porté par la marque **C-Kreyol** ;

sans qu’un **sous-texte** ou un **visuel** **seuls** suffisent à deviner l’offre (éviter le hero **uniquement** « ambiance marque »).

**Hiérarchie du message dans le hero (Phase 1, tranché)** : le hero parle **d’abord** de **l’offre** et de **l’origine lisible des produits** (île, région, territoire — **honnête**, compatible avec le **catalogue réel**, [ADR-CKR-005](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005)), et de **l’esprit** de proposition (cf. §5). Il ne porte **pas** la **mécanique opératoire** (hub, chaîne logistique, « qui opère ») ni l’**ancrage géographique du projet** (**Nantes**) : ces éléments relèvent de blocs **plus bas** sur la homepage, du **bloc confiance** ou de pages type **À propos** (cf. §4).

**Suite homepage / catalogue** : l’**origine** reste un **repère commercial visible** (fiches produit, cartes produit, collections ; à terme entrées **territoires / origines** si pertinent) — cohérent avec ce qui est annoncé **dès** le hero.

---

## 2. Rapport à la charte graphique

La **charte minimale Phase 1** est **gelée** (**Direction A — épicerie fine tropicale**, [CHARTE_GRAPHIQUE_PHASE1.md](CHARTE_GRAPHIQUE_PHASE1.md) **§3–§11**) : **ton**, **palette**, **typos** de référence, **CTA**, **photo**, **icono**, **interdits**. Les **états UI** détaillés restent **à décliner** en implémentation — sans bloquer le **gel du copy** et du **cadrage visuel** du hero.

**Séquence** : **charte gelée** → **figer le hero** (§3–§7, dont §4 **localisation / provenance**) → **implémentation** thème ([ADR-CKR-002](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-002) / [ADR-CKR-003](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-003)).

---

## 3. Les quatre arbitrages — **gel** (2026-04-21)

Les **propositions** ci-dessous restent en **archive** ; les champs **retenu** reflètent l’**arbitrage** documenté en **§7**.

### 3.1 Titre (proposition de valeur courte)

- **Méthode** (rappel) : raisonner par **familles** de hero avant de trancher — voir tableau d’options.
- **Contraintes** : **court**, **concret**, lisible sur **mobile** sans retour ligne abusif.
- **Règle** : le titre doit pouvoir être **compris seul** — sans **dépendre** du visuel ni du sous-texte pour identifier la **nature de l’offre** (renforce le §1).

**Propositions de travail** (Phase 1, **5 max.** — **archive**) :

| # | Famille | Titre (proposition) |
|---|---------|---------------------|
| 1 | **Offre claire** | **C-Kreyol — agro transformés des Antilles, en ligne** |
| 2 | **Origine / territoires** | **Des Antilles à votre table : agro transformés aux origines lisibles** |
| 3 | **Retail / sélection** | **C-Kreyol : une sélection d’agro transformés antillais** |
| 4 | **Cadeau / découverte** | **Agro transformés des Antilles : à table, à offrir** |
| 5 | **Conviction / qualité perçue** | **L’épicerie fine antillaise en ligne : agro transformés d’origine** |

**Titre retenu** : **C-Kreyol : une sélection d’agro transformés antillais** (option **#3** — équilibre **retail** / **sérieux** / **Direction A**).

**Titre de secours** (si retours atelier marque : besoin d’encore plus de **directivité**) : **C-Kreyol — agro transformés des Antilles, en ligne** (option **#1**).

**Micro-réserve** (évolution possible hors gel immédiat) : l’expression **« agro transformés »** est **exacte** côté cadrage / SEO interne, mais un peu **administrative** pour le grand public ; à moyen terme, tester des formulations plus **grand public** (ex. **produits transformés des Antilles**, ou **biscuits, douceurs et épicerie des Antilles** dans le titre) sans casser la **cohérence** avec la [NOTE_DE_CADRAGE.md](NOTE_DE_CADRAGE.md) / fiches produit.

### 3.2 Sous-texte (1 à 2 phrases)

- **Contraintes** : complète le titre sans **répéter** mécaniquement le menu ; **pas** de sur-promesse stock / délais ([ADR-CKR-005](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005)) ; rester **court** sur mobile ; formulations **A / B / C** ci-dessous = **pistes non retenues telles quelles** (trop défensif, jargon interne, etc.).

**Propositions** (Phase 1, **3 max.** — **archive**) :

| # | Sous-texte (proposition) |
|---|--------------------------|
| A | Une sélection d’**agro transformés des Antilles**, avec des **origines lisibles** sur chaque fiche. **Disponibilités et détails** : comme indiqué **en boutique** — sans promesse de délai ni de stock non garanti. |
| B | **C-Kreyol** rassemble des produits authentiques (biscuits, confiseries, épicerie) pour faire découvrir le goût des Antilles **sans folklore**. **Parcourez le catalogue** au fil des arrivages. |
| C | Le plaisir des saveurs antillaises, **choisi avec exigence retail**. **Entrez en boutique** pour composer votre panier selon les références **réellement proposées**. |

**Sous-texte retenu** : **Biscuits, douceurs et épicerie des Antilles, sélectionnés avec soin pour faire découvrir des origines et des saveurs authentiques.**  
*(Inspiré de la piste **B**, adoucie : pas de « sans folklore » ni « exigence retail » en hero ; la **rigueur disponibilité** peut vivre **plus bas** sur la page ou sur les **fiches**.)*

### 3.3 CTA principal

- **Comportement** : un **CTA principal** unique prioritaire ; CTA secondaires **discrètes** si besoin.
- **Règle** : le CTA principal oriente vers une action **immédiatement tenable** en Phase 1, **prioritairement** l’**exploration de la boutique** (éviter un libellé trop **conceptuel** ou une cible pas encore **opérationnelle**).
- **CTA secondaire** (implémentation actuelle) : **« Explorer le catalogue »** — ancre vers la section **Explorer** (`#explorer-catalogue`), cohérent avec [ADR-CKR-006](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-006) et [WIREFRAME_HOMEPAGE.md](WIREFRAME_HOMEPAGE.md) Bloc 3 ; **discret** (bouton secondaire, sans `lg` sur le primaire).

**Propositions de libellé** (Phase 1, **2 max.** — **archive**) :

| # | Libellé CTA |
|---|-------------|
| 1 | **Découvrir la boutique** |
| 2 | **Voir les produits** |

**Libellé retenu** : **Découvrir la boutique** — cible **/shop** (ou équivalent menu **Boutique**, [STRUCTURE_MENU_PRINCIPAL.md](STRUCTURE_MENU_PRINCIPAL.md)).

### 3.4 Visuel

- **Contraintes** : **performance** (formats, poids) ; **cohérence** avec la promesse **honnête** (pas de mise en scène **déconnectée** du catalogue réel) ; alignement [CHARTE_GRAPHIQUE_PHASE1.md](CHARTE_GRAPHIQUE_PHASE1.md) **§7** (photo) et **§9.1** (hero).

**Propositions** (Phase 1, **2 max.** — **archive**) :

| # | Direction visuelle | Description |
|---|-------------------|-------------|
| 1 | **Macro / gros plan** *(recommandé avec la charte **Direction A**)* | Texture **réelle** (biscuit, manioc, confiture, pâte), **lumière naturelle**, fond sobre ; met la **matière** et la **transformation** au centre — **peu ou pas** de scène de vie. |
| 2 | **Plateau calme** | **2 à 4** produits disposés avec **lumière naturelle** et surfaces **bois / neutres** ; reste **centré produit**, sans scène **lifestyle** chargée. |

**À éviter pour ce hero en Phase 1** : photo d’**équipe** dominante, **lifestyle** trop narratif, visuel **institutionnel** (bureau, hub), illustration **décorative** sans lien direct avec le catalogue.

**Direction visuelle retenue** : **Piste 1 — macro / gros plan** sur **matière réelle** (biscuit, manioc, confiture, texture), **lumière naturelle**, composition **sobre** — avec **recadrage** ou **shooting dérivé** si l’image d’**exemple produit** (paragraphe suivant) met trop en avant le **packaging fabricant** au détriment de **C-Kreyol** (cf. **§4**).

#### Référence « exemple de produit » (La Platine — manioc)

Visuel **versionné** dans le dépôt (cadrage type **piste 1** / **piste 2** : produit réel, fond clair, packaging lisible) :

![Exemple produit — crackers manioc (emballage La Platine, origine Guadeloupe)](assets/exemple_produit_manioc_crackers_la_platine.png)

- **Intérêt** : **matière** visible (disques, texture), **origine** lisible sur l’étiquette (ex. **97180 Sainte-Anne**), rendu **sobre** et **e-commerce** — aligné [CHARTE_GRAPHIQUE_PHASE1.md](CHARTE_GRAPHIQUE_PHASE1.md) **§7**.
- **Attention hero** (cf. **§4** ci-dessous) : le packaging porte la marque **fabricant** ; pour le **hero C-Kreyol**, prévoir un **recadrage** ou une **photo déclinée** pour que le **premier message** reste **l’offre canal** + **produit**, sans que **La Platine** **absorbe** la hiérarchie visuelle (détails en **bloc fournisseur** wireframe).

#### Référence composition (moodboard — Direction A)

Visuel **versionné** pour la **piste macro / matière** (sans packaging dominant) :

![Référence composition hero — biscuits, confiture, espace pour texte](assets/hero_reference_direction_a_biscuits_confiture.png)

- **Rôle** : **moodboard** aligné [BRIEF_VISUEL_HERO_PHASE1.md §10.2](BRIEF_VISUEL_HERO_PHASE1.md) ; utile pour **brief** photographe / retouche et **tests** titre + CTA sur **espace négatif**.
- **Copy** : utiliser **uniquement** le texte **gelé** au **§7** (pas de titres alternatifs posés sur l’image seule).

#### Banque photos homepage (packshots)

Visuels **versionnés** pour la **homepage** (sélection produits, vignettes, etc.) — détail et usages : [BRIEF_VISUEL_HERO_PHASE1.md §10.3](BRIEF_VISUEL_HERO_PHASE1.md).

| Aperçu | Fichier |
|--------|---------|
| Maniocookies salés La Platine | `docs/assets/homepage_maniocookies_sale_la_platine.png` |
| Manioc crackers salés Ste-Anne | `docs/assets/homepage_manioc_crackers_sale_ste_anne.png` |
| Manioc pâtes Mayotte | `docs/assets/homepage_manioc_pates_mayotte_la_platine.png` |

Pour le **hero principal**, rester aligné sur la **direction visuelle gelée** §7 (macro / matière + **§10.2** brief) ; ces **packshots** complètent surtout les **autres blocs** de la homepage.

---

## 4. Localisation, provenance et hiérarchie (tranchés Phase 1)

- **Nantes** n’est **pas** mis en avant dans le **hero** en Phase 1 ; cette information relève plutôt du **bloc d’ancrage / de confiance**, d’éléments **plus bas** sur la homepage ou de la page **À propos** — éviter de **brouiller** le premier écran avec du « cadre projet ».
- **La Platine** : **plutôt hors** du **hero principal** ; mise en avant **fournisseur** conforme au [WIREFRAME_HOMEPAGE.md](WIREFRAME_HOMEPAGE.md) **bloc 4** (et au-delà), sans **absorber** la marque **C-Kreyol**.
- L’**origine des produits** (île, région, territoire) constitue en revanche un **élément légitime** de la **promesse visible dès le hero**, dès lors qu’elle reste **lisible**, **honnête** et **compatible** avec l’offre **réellement disponible** ([ADR-CKR-005](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005)).

---

## 5. Ton éditorial (indicatif)

**Direction** : **sérieux** et **chaleureux**, **accessible**, **sans** cliché exotique cheap (cf. [DESIGN.md §14](DESIGN.md)).

**À valider** : tutoiement / vouvoiement, niveau de **technicité** (ingrédients, terroir) dans le hero vs dans le corps de page.

---

## 6. Éléments à éviter

- titre **trop abstrait** ou purement **évocatif** (sans ancrage offre) ;
- sous-texte **trop long** ;
- visuel **décoratif** sans lien **lisible** avec l’offre ;
- **accumulation** dans le premier écran de la marque, des **origines**, de **Nantes**, de **La Platine** et de la **logistique** ;
- **promesse** de disponibilité ou de **délai** non soutenue par la **réalité opérationnelle** ([ADR-CKR-005](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005)).

---

## 7. Décision cible — **hero MVP2.1 immersif** (2026-04-24, livré)

> **Remplace** l’ancienne décision cible **hero Phase 1 gelée** (2026-04-21) **au périmètre structure + copy**, consignée ci-dessous en **§7 bis (archive)**. Les invariants **§1**, **§4** et **ADR-CKR-005** restent **intangibles**.

**Décision MOA** : [DECISION_HERO_HOMEPAGE_V2.md](../mvp_02/DECISION_HERO_HOMEPAGE_V2.md) — **Option B** : hero **immersif**, image produit en fond, **overlay léger**, texte **aligné à gauche**, **2 CTA** visibles sans scroll.

**Arbitrage contenu hero (MVP2.1)** :

| Élément | Décision retenue |
|---------|------------------|
| **Titre** | **Retrouvez les saveurs et savoir-faire créoles.** |
| **Sous-texte** | **C-Kreyol sélectionne avec soin des produits issus de territoires où la culture créole est vivante, auprès de producteurs et créateurs de confiance.** |
| **CTA principal** | **Découvrir la sélection** → **/shop**. |
| **CTA secondaire** | **Explorer les origines** → **/origines** (cible doctrinale) ; **implémentation MVP2.1** : `/shop?ckr_mode=origin` tant que la porte `/origines` n’est pas livrée par le ticket [EXPLORER-HOMEPAGE-MVP2](../crea/TICKET_EXPLORER_HOMEPAGE_MVP2.md). Bascule vers `/origines` dans la PR Explorer MVP2. |
| **Direction visuelle** | **Image produit en fond**, immersive, **appétente**. Asset : `static/src/img/hero_v2_immersive.png`. **Principe unique toutes tailles (`19.0.1.7.11`)** : overlay **dégradé gauche → droite** sur `.ckr-hero__overlay` ; **aucune** carte, **aucun** `backdrop-filter`, **aucun** fond sous `.ckr-hero__content` ; lisibilité par **contraste** + **`text-shadow` sobre** (titre `0 2px 6px rgba(0,0,0,0.5)`, sous-titre `0 1px 4px rgba(0,0,0,0.4)`). **Desktop / tablette (≥768px)** : `linear-gradient(90deg, rgba(0,0,0,0.6) 0%, 0.4 35%, 0.15 65%, 0 85%)` — fondu étendu, image respirante à droite. **Mobile (≤767px)** : `linear-gradient(90deg, rgba(0,0,0,0.65) 0%, 0.45 35%, 0.15 70%, 0.05 100%)` + `.ckr-hero__content` `margin: 5rem 1rem 2rem` / `padding: 2rem 1.5rem` / `max-width: 100%`, CTA colonne pleine largeur (gap `0.9rem`, `margin-top: 1.5rem`). **Titre** `#fff`, `clamp(2.1rem,5vw,3.6rem)` (mobile `clamp(2rem,9vw,2.8rem)`, line-height 1.1). **Sous-titre** `rgba(255,255,255,0.92)`, `clamp(1rem,1.4vw,1.15rem)` (mobile 1rem / 1.45). **CTA secondaire** (toutes tailles) : contour 1 px blanc à 0,8 sur fond transparent ; hover `rgba(255,255,255,0.12)`. **Fond racine** `.ckr-hero.ckr-hero--immersive.ckr-root` **transparent** (`ckr_main.scss`). Chaîne **`19.0.1.7.4`** → **`19.0.1.7.11`** (dont fix `min()` en `19.0.1.7.6`). |
| **Structure** | Section pleine largeur, contenu aligné à gauche, max-width texte ~36–42 rem, min-height hero ≥ 70 vh (desktop ≥ 78 vh) pour garantir la visibilité above-the-fold. |

### 7 bis. Archive — hero Phase 1 gelé (2026-04-21)

Conservé pour traçabilité doctrinale. **Non** appliqué en production MVP2.1.

| Élément | Décision archivée |
|---------|-------------------|
| **Titre** | C-Kreyol : une sélection d’agro transformés antillais. |
| **Sous-texte** | Biscuits, douceurs et épicerie des Antilles, sélectionnés avec soin pour faire découvrir des origines et des saveurs authentiques. |
| **CTA principal** | Découvrir la boutique → /shop. |
| **CTA secondaire** | Explorer le catalogue → ancre `#explorer-catalogue` (remplacé MVP2.1). |
| **Direction visuelle** | Macro / gros plan — matière réelle, lumière naturelle. Assets références : `docs/assets/exemple_produit_manioc_crackers_la_platine.png`, `docs/assets/hero_reference_direction_a_biscuits_confiture.png`. |

### Affinage éditorial ultérieur (sans remise en cause du gel)

Le **wording exact** du hero (**titre** et **sous-texte** tels qu’ils figurent au **§3** / tableau **§7**) pourra être **raffiné** en **atelier éditorial** plus tard (rythme, synonymes, longueur mobile, SEO), **sans** remettre en cause les **décisions déjà gelées** sur :

- la **hiérarchie** du message (§1) ;
- la **place** de l’**origine** produit (§4) ;
- l’**exclusion** de **Nantes** et de **La Platine** du **message principal** du hero (§4) ;
- le **CTA principal** orienté **boutique** (§3.3 / §7) ;
- la **direction visuelle** **macro / matière** (§3.4 / §7).

Tout affinage doit **rester compatible** avec ces **invariants** et avec [ADR-CKR-005](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005).

**À poursuivre** : **responsable validation marque** ([CHARTE_GRAPHIQUE_PHASE1.md](CHARTE_GRAPHIQUE_PHASE1.md) §11) ; **assets finaux** (shooting / export web) selon [BRIEF_VISUEL_HERO_PHASE1.md](BRIEF_VISUEL_HERO_PHASE1.md) ; **états UI** en implémentation ; **tests mobile** sur la composition réelle du bloc hero.

---

## 8. Pilotage — Hero Homepage V2 (MVP 02, 2026-04-24)

**Décision MOA** : [DECISION_HERO_HOMEPAGE_V2.md](../mvp_02/DECISION_HERO_HOMEPAGE_V2.md) — **Option B** : hero **immersif** (fond produit, overlay léger, texte à gauche, deux CTA) ; **modifications QWeb et SCSS** autorisées sur le périmètre hero ; **ticket obligatoire avant PR** : [TICKET_HERO_HOMEPAGE_V2.md](../crea/TICKET_HERO_HOMEPAGE_V2.md).

**Cible copy & contraintes visuelles** (travail MVP 02) : [1_HOMEPAGE.md](../mvp_02/1_HOMEPAGE.md).

**Règle d’alignement doc ↔ code** : au **merge** de la PR hero V2, mettre à jour le **tableau §7** (et les paragraphes qui en dépendent) pour refléter la **nouvelle copy** et la **nouvelle structure** effective — **dans la même PR** que le code **ou** par **commit documentaire immédiat** sur `main` après merge, afin d’éviter toute dérive entre SPEC et production.

**Recette** : [PV_RECETTE_HERO_HOMEPAGE_V2_CK.md](../crea/PV_RECETTE_HERO_HOMEPAGE_V2_CK.md).

**Verdict recette MOA (2026-04-24)** : **GO MOA** — ticket **`HERO-HOMEPAGE-V2` accepté** — build **`19.0.1.7.11`**. Synthèse : desktop OK ; mobile OK ; tablette acceptable ; principe immersif cohérent (overlay G→D, texte intégré, pas de carte ni blur) ; CTA lisibles ; tests auto verts. **Réserve non bloquante** : crop tablette / mobile perfectible (piste d’amélioration future). Détail : **PV §8**. **Feu vert** pour lancer le chantier **2/5** **[EXPLORER-HOMEPAGE-MVP2](../crea/TICKET_EXPLORER_HOMEPAGE_MVP2.md)** (pilotage [README MVP02](../mvp_02/README.md)).

**Lecture transverse** : le ticket [TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md](../crea/TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md) reste le **cadre** appétence / partition ; le présent §8 ne le clos **pas** sur les autres axes (rythme global, blocs §2–5 MVP2, etc.).

---

## Historique du document

| Date | Changement |
|------|------------|
| 2026-04-21 | Création : exigence §1, quatre arbitrages (titre, sous-texte, CTA, visuel), questions Nantes / La Platine, ton, décision **[à compléter]** ; liens wireframe, design, ADR. |
| 2026-04-21 | **§2** : séquence **charte minimale** avant gel hero ; lien **[CHARTE_GRAPHIQUE_PHASE1.md](CHARTE_GRAPHIQUE_PHASE1.md)** ; renumérotation §3–§6 (évolué §3–§7). |
| 2026-04-21 | **§2** : liste des prérequis charte alignée sur **CHARTE** §2 enrichi (ton visuel, états UI, iconographie) — **évolué** : voir **CHARTE** **§3** (tableau figé). |
| 2026-04-21 | **§7** : renvoi **CHARTE** **§3–§9** + responsable §11 ; charte **Direction A** gelée. |
| 2026-04-21 | **§1** : hiérarchie message hero (offre + origine ; pas mécanique opératoire / Nantes). **§4** : Nantes / La Platine / **origine** **tranchés** ; **§5** ex-§4 Ton ; **§6** décision cible clarifiée (devenu **§7**). |
| 2026-04-21 | Ouverture **cadre** ; **§3.1** / **§3.3** règles titre / CTA ; **§6** **Éléments à éviter** ; **§7** décision cible (ex-§6). |
| 2026-04-21 | **§3.1** : méthode **familles** ; **5 propositions** de titre (tableau) ; **§7** : enchaînement titre → 2 sous-textes → CTA → visuel. |
| 2026-04-21 | Intro : lien **[DIRECTIONS_ARTISTIQUES_PHASE1.md](DIRECTIONS_ARTISTIQUES_PHASE1.md)** (intentions visuelles). |
| 2026-04-21 | **§2** : charte **gelée** ; **§3.2–§3.4** : **3** sous-textes, **2** CTA, **2** directions visuelles + **reco** macro / texture ; shortlist titres **#1/#3** ; intro **ADR-CKR-003** ; **§7** consolidation gel hero. |
| 2026-04-21 | **§3.4** : **exemple produit** versionné `docs/assets/exemple_produit_manioc_crackers_la_platine.png` + règles **crop** / hiérarchie vs **§4**. |
| 2026-04-21 | **Gel hero** : **§3** restructuré (**archive** + **retenu**) ; **titre #3**, **sous-texte** adouci (piste B), **CTA** « Découvrir la boutique », **visuel piste 1** ; **§7** tableau décision ; **titre secours #1** ; **micro-réserve** « agro transformés ». |
| 2026-04-21 | **§7** : clause **affinage éditorial** ultérieur **sans** remise en cause hiérarchie, **origine**, **Nantes** / **La Platine**, **CTA boutique**, **visuel macro**. |
| 2026-04-21 | Intro + **§7** : lien **[BRIEF_VISUEL_HERO_PHASE1.md](BRIEF_VISUEL_HERO_PHASE1.md)** (production assets hero). |
| 2026-04-21 | **§3.4** + **§7** : asset `hero_reference_direction_a_biscuits_confiture.png` (moodboard) ; lien **BRIEF** §10.2. |
| 2026-04-21 | **§3.4** : **banque photos homepage** (3 packshots) ; **BRIEF** §10.3. |
| 2026-04-24 | **§8** : pilotage **Hero V2** (MVP 02) — décision MOA, ticket `HERO-HOMEPAGE-V2`, PV recette, règle de mise à jour **§7** après merge PR. |
| 2026-04-24 | **Intro** : renvoi **§8** pour évolution structurale hero (MVP 02). |
| 2026-04-24 | **§7** réécrit — cible **hero MVP2.1 immersif** livrée (copy + CTA + structure + asset) ; ancien §7 Phase 1 déplacé en **§7 bis (archive)**. Livraison code ticket `HERO-HOMEPAGE-V2` : snippet + SCSS + manifest `19.0.1.7.0`. |
| 2026-04-24 | **§7** ligne **Direction visuelle** : itération **lisibilité** après recette visuelle MOA NO-GO — overlay gauche renforcé, léger assombrissement image, H1 / sous-titre / CTA secondaire sur fond sombre ; module **`19.0.1.7.1`**. |
| 2026-04-24 | **§7** ligne **Direction visuelle** : itération **clair / chaud / premium** après NO-GO « hero trop sombre » — suppression assombrissement global, voile léger CK pleine largeur, **panneau crème local** derrière le bloc texte uniquement (`19.0.1.7.2`). |
| 2026-04-24 | **§7** ligne **Direction visuelle** : abandon effet **carte** — retour **dégradé gauche → droite** semi-transparent, texte intégré image, overlay mobile adapté (`19.0.1.7.3`). |
| 2026-04-24 | **Impl. technique** — `19.0.1.7.4` : overlay G→D ré-appliqué dans `_hero.scss` ; `ckr_main.scss` exclut **`h1.ckr-hero__title`** de la couleur `$ckr-text` globale (régression capture recette : H1 noir sur image). |
| 2026-04-24 | **§7** — `19.0.1.7.5` : mobile, voile sombre **local** `rgba(16,14,12,0.88)` sur `.ckr-hero__content::before` (≤767px) ; dégradé plein écran mobile adouci. |
| 2026-04-24 | **Tech** — `19.0.1.7.6` : `max-width: unquote("min(36rem, 100%)")` (fix compilation `web.assets_frontend`). |
| 2026-04-24 | **§7** — `19.0.1.7.7` : mobile, abandon voile `::before` ~88 % au profit d’un fond local ~58 % + blur léger ; overlay mobile = dégradé vertical léger ; CTA colonne pleine largeur. |
| 2026-04-24 | **§7** — `19.0.1.7.8` : correctif recette — fond `.ckr-root` sur section hero retiré (`ckr_main`), `overflow: visible` mobile sur hero, voile texte en `::before` + blur 12px + overlay mobile adouci (backdrop réellement visible). |
| 2026-04-24 | **§7** — `19.0.1.7.9` : alignement **référence MOA** — mobile sans « glass card » : overlay G→D intégré uniquement ; `.ckr-hero__content` transparent, sans `::before` / blur. |
| 2026-04-24 | **§7** — `19.0.1.7.10` (**version finale attendue pour GO mobile**) : overlay G→D simplifié (noir 0.65→0.05), contenu `margin 5rem 1rem 2rem` / `padding 2rem 1.5rem`, titre `clamp(2rem,9vw,2.8rem)` + `text-shadow 0 2px 6px`, sous-titre `rgba(255,255,255,0.92)`, CTA `margin-top: 1.5rem`, secondaire contour 1px blanc sur transparent. |
| 2026-04-24 | **§7** — `19.0.1.7.11` : **alignement desktop/tablette** sur le principe mobile validé (cohérence cross-device) — overlay G→D unique sur `.ckr-hero__overlay` (desktop 0.6→0 / mobile 0.65→0.05) ; suppression voile vertical additionnel ; typo simplifiée (text-shadow sobre) ; CTA secondaire mutualisé (contour 1px blanc / transparent) toutes tailles. |
| 2026-04-24 | **§8** — **GO MOA** : recette visuelle **HERO-HOMEPAGE-V2 acceptée** ; PV §8 ; feu vert **EXPLORER-HOMEPAGE-MVP2** (chantier 2/5). Réserve non bloquante : crop tablette/mobile. |
