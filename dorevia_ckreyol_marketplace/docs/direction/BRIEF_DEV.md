# BRIEF_DEV_FRONT_PHASE1 — C-Kreyol

## 1. Objet du document

Ce document a pour objet de cadrer le **travail de développement front-end Phase 1** pour le projet **C-Kreyol** sur **Odoo 19 Community Edition**.

Il sert de point d’entrée opérationnel pour le développeur front, en synthèse des documents de cadrage, de design et des ADR déjà produits. Il complète le [README](../../README.md) (vision, phases, inventaire `docs/assets/`) sans les dupliquer.

---

## 2. Contexte projet

**C-Kreyol** est un **canal e-commerce spécialisé** autour de **produits agro transformés antillais**.

Le projet est porté comme :

- une **marque propre** ;
- un **canal retail digital** ;
- un front-end devant être **distinct d’un rendu standard Odoo**.

Le front-end est un chantier stratégique de la Phase 1, car il porte :

- la lisibilité de l’offre ;
- la perception de marque ;
- la qualité retail ;
- la crédibilité du canal ;
- la cohérence mobile.

Autant que possible, le projet cherche à **respecter Odoo 19 Community Edition**, côté **front-end** comme côté **back-office**, en évitant les **réécritures inutiles** et les **contournements prématurés** du standard.

---

## 3. Objectif du lot front Phase 1

L’objectif de ce lot est de produire un **premier socle front-end intégré dans Odoo 19 CE**, cohérent avec les documents de référence, permettant au minimum :

- un **header** incluant un **menu principal entièrement personnalisé** ;
- un **footer** entièrement personnalisé ;
- une **homepage** structurée selon le wireframe validé (**variante retail enrichie**, cohérente avec le menu principal **Option B**) ;
- un **hero homepage** intégré selon la spec validée ;
- une première cohérence visuelle avec la **charte graphique Phase 1** ;
- une **expérience mobile web utilisable**.

---

## 4. Périmètre à développer maintenant

Le périmètre immédiat de développement comprend :

- le **thème front Phase 1** ;
- les **assets** globaux nécessaires ;
- le **header** (menu principal personnalisé inclus) ;
- le **footer** ;
- la **homepage** ;
- le **hero homepage** ;
- l’usage des **visuels versionnés** sous `docs/assets/` pour **intégration** ou **placeholders** : distinguer **visuel hero principal** (logique **macro / matière / transformation**, moodboard — [CHARTE_GRAPHIQUE_PHASE1.md](CHARTE_GRAPHIQUE_PHASE1.md) §7.2, [BRIEF_VISUEL_HERO_PHASE1.md](BRIEF_VISUEL_HERO_PHASE1.md) §10.2) et **banque packshots homepage** (bibliothèque produit / blocs catalogue — même charte §7.2, brief §10.3) ;
- les premiers styles de base :
  - couleurs,
  - typographies,
  - boutons / CTA,
  - espacements,
  - responsive.

Selon avancement, peuvent aussi être abordés :

- les **cartes produit** ;
- la première structure visuelle de la **boutique / collection**.

---

## 5. Décisions déjà figées

Les éléments suivants sont considérés comme **actés** pour ce lot :

- **Odoo 19 Community Edition** comme socle ;
- doctrine **standard d’abord** ;
- le **spécifique légitime** en Phase 1 est le **front-end** ;
- le **menu principal** et le **footer** doivent être **entièrement personnalisés** ;
- direction artistique Phase 1 retenue :
  **Direction A — Épicerie fine tropicale** ;
- la homepage suit la logique du [WIREFRAME_HOMEPAGE.md](WIREFRAME_HOMEPAGE.md) (**variante retail enrichie**, menu **Option B** — [STRUCTURE_MENU_PRINCIPAL.md](STRUCTURE_MENU_PRINCIPAL.md)) ;
- le hero suit la structure validée dans [SPEC_HERO_HOMEPAGE.md](SPEC_HERO_HOMEPAGE.md) (**copy et cadrage visuel gelés** au §7, avec **micro-réserve** documentée sur le libellé « agro transformés » et **titre de secours** possible) ;
- dans le hero :
  - **Nantes** n’est pas mis en avant ;
  - **La Platine** ne doit pas absorber la marque ;
  - l’**origine des produits** peut être visible ;
- l’expérience **mobile web** est un **must have**.

### 5.1 Évolution documentée — Phase 2 (Explorer)

Après gel Phase 1, la **homepage** intègre une section **Explorer / Par où commencer** : **cinq portes d’exploration catalogue** (ordre et libellés : [ADR-CKR-008](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008), [WIREFRAME_HOMEPAGE.md](WIREFRAME_HOMEPAGE.md) Bloc 3), **distinctes** du menu Option B — voir [STRUCTURE_MENU_PRINCIPAL.md §11](STRUCTURE_MENU_PRINCIPAL.md). Le **hero** peut comporter un **second CTA** ancré vers Explorer ([SPEC_HERO_HOMEPAGE.md](SPEC_HERO_HOMEPAGE.md) §3.3).

---

## 6. Ce qui reste provisoire / à confirmer

Les éléments suivants peuvent encore évoluer **sans remettre en cause** le socle du lot :

- le **polissage copy** du hero **après** le gel [SPEC_HERO_HOMEPAGE.md](SPEC_HERO_HOMEPAGE.md) §7 (ex. formulation plus **grand public** que « agro transformés », ou bascule vers le **titre de secours** si la marque le demande) ;
- le choix des **assets visuels finaux** (shooting / export HD) en remplacement ou complément des **fichiers de référence** dans `docs/assets/` ;
- le détail des **états UI** (tokens / SCSS) ;
- certains **contenus éditoriaux secondaires** (hors hero gelé) ;
- le nom du **responsable validation marque** dans la charte ([CHARTE_GRAPHIQUE_PHASE1.md](CHARTE_GRAPHIQUE_PHASE1.md) §11).

Le développeur ne doit pas bloquer le lot sur ces points si des valeurs provisoires cohérentes permettent d’avancer (y compris **placeholders** images alignés sur les références versionnées).

---

## 7. Doctrine technique à respecter

Le développement doit respecter les règles suivantes :

- autant que possible, respecter les **logiques natives** d’**Odoo 19 CE**, côté **front** comme côté **back-office** ;
- **personnaliser** là où l’identité **C-Kreyol** l’exige, sans rompre **inutilement** avec la **structure** du standard ;
- autant que possible, respecter la **structure** et les **comportements natifs** utiles d’**Odoo 19 CE**, y compris côté **front**, tant qu’ils ne contredisent pas les **exigences de marque** et de **qualité retail** ;
- ne pas recréer une **logique métier parallèle** dans le front ;
- rester dans le champ **présentationnel / thème / UX** ;
- éviter les contournements lourds du standard Odoo ;
- privilégier la **maintenabilité** ;
- viser une intégration **sobre, claire et responsive** ;
- ne pas laisser subsister un rendu final perçu comme **standard Odoo** sur les zones stratégiques.

---

## 8. Documents de référence

Le développement doit s’appuyer en priorité sur les documents suivants (chemins relatifs au dossier `docs/`) :

| Document | Rôle |
|----------|------|
| [README.md](../../README.md) | Vue d’ensemble, phases, **tableau des PNG** sous `docs/assets/`. |
| [VISION_CK_MEDIA_COMMERCE.md](VISION_CK_MEDIA_COMMERCE.md) | Vision **trois mondes** (e-commerce, éditorial, communautaire), garde-fous publicité / tunnel d’achat — contexte produit et priorisation ([ADR-CKR-009](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-009)). |
| [DOCTRINE_CK_ECOMMERCE_B2C_B2B.md](DOCTRINE_CK_ECOMMERCE_B2C_B2B.md) | **B2C** / **B2B** : prix public conseillé vs prix partenaire distributeur, catalogue commun, Odoo standard — ([ADR-CKR-010](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-010)). |
| [DOCTRINE_CK_LANGUES_CREOLES.md](DOCTRINE_CK_LANGUES_CREOLES.md) | Langues **créoles** : qualité, variantes, gouvernance — orientation long terme, **sans** mandat MVP — ([ADR-CKR-011](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-011)) ; distinct de [EXPLOITATION_I18N_DEVISES.md](EXPLOITATION_I18N_DEVISES.md) (FR/EN/ES). |
| [DOCTRINE_CK_PACK_VS_KIT.md](DOCTRINE_CK_PACK_VS_KIT.md) | **Pack** (homogène, conditionnement) vs **kit** (hétérogène, usage / expérience) — copy et catalogue ; complément [ADR-CKR-008](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008) (porte **Kits** / `pack_ok`). |
| [NOTE_DE_CADRAGE.md](NOTE_DE_CADRAGE.md) | Arbitrages métier, juridique, logistique, périmètre V1. |
| [ARCHITECTURE_DECISION_RECORD.md](ARCHITECTURE_DECISION_RECORD.md) | **ADR-CKR-001** à **011** (doctrine Odoo 19 CE, front spécifique, menu/footer, modèle commercial, promesse / disponibilité, homepage/portes, vision média-commerce, **e-commerce B2C+B2B**, **langues créoles**). |
| [DESIGN.md](DESIGN.md) | Principes design / retail / front, zones de page, mobile. |
| [STRUCTURE_MENU_PRINCIPAL.md](STRUCTURE_MENU_PRINCIPAL.md) | Menu **Option B**, entrées cibles, mobile. |
| [WIREFRAME_HOMEPAGE.md](WIREFRAME_HOMEPAGE.md) | Structure homepage Phase 1 (blocs, variante retenue). |
| [SPEC_HERO_HOMEPAGE.md](SPEC_HERO_HOMEPAGE.md) | Hero : **copy gelé** §7, CTA, hiérarchie provenance, **banque photos** homepage. |
| [CHARTE_GRAPHIQUE_PHASE1.md](CHARTE_GRAPHIQUE_PHASE1.md) | Direction A, palette, typos, CTA, photo §7 (dont **7.2** hiérarchie packshots / hero). |
| [BRIEF_VISUEL_HERO_PHASE1.md](BRIEF_VISUEL_HERO_PHASE1.md) | Production visuelle hero : moodboard §10.2, packshots §10.3. |
| [BRIEF_SYNTHETIQUE_CK.md](BRIEF_SYNTHETIQUE_CK.md) | Direction artistique synthétique (contexte). |
| [DIRECTIONS_ARTISTIQUES_PHASE1.md](DIRECTIONS_ARTISTIQUES_PHASE1.md) | Pistes DA et recommandation (contexte). |

---

## 9. Livrables attendus

Les livrables attendus pour ce lot sont :

- un **thème front Phase 1** exploitable ;
- un **header** avec **menu principal** personnalisé ;
- un **footer** personnalisé ;
- une **homepage** intégrée ;
- un **hero** intégré avec le **copy gelé** et le **cadrage visuel** (macro / matière ; pas un packshot banque **seul** comme visuel hero définitif sans arbitrage marque) ;
- un premier système visuel cohérent :
  - couleurs,
  - typographies,
  - CTA,
  - espacements,
  - responsive de base.

---

## 10. Points de vigilance

Le développeur doit être attentif en particulier à :

- la **lisibilité mobile** ;
- la différence perçue avec un **front Odoo standard** ;
- la cohérence entre le **hero**, le **menu**, le **footer** et la **charte** ;
- l’absence de **sur-promesse visuelle** sur disponibilité ou logistique ;
- la hiérarchie de marque entre **C-Kreyol** et **La Platine** ;
- la distinction **visuel hero** vs **packshots homepage** (cf. charte **7.2**), pour éviter qu’un **sachet fabricant** ne devienne l’unique image d’accroche sans traitement éditorial.

---

## 11. Critères d’acceptation

Le lot sera considéré comme satisfaisant si :

- le **header** (menu principal) et le **footer** sont clairement **personnalisés** ;
- la homepage suit le **wireframe validé** ;
- le hero respecte la **spec validée** (titres, sous-texte, CTA, règles **Nantes** / **La Platine** / **origine**) ;
- les **images** des blocs homepage hors hero peuvent s’appuyer sur la **banque packshots** ; le **hero principal** reste aligné **macro / matière / transformation** (ou équivalent validé), conformément à la charte **7.2** ;
- le rendu global est cohérent avec la **Direction A** ;
- la lecture mobile du parcours principal est correcte ;
- le front ne donne pas une impression de **template Odoo par défaut**.

---

## 12. Hors périmètre de ce lot

Hors périmètre immédiat :

- logique métier additionnelle ;
- développement back-office spécifique ;
- architecture logistique détaillée ;
- application mobile native ;
- charte graphique étendue complète ;
- automatisations non indispensables au front Phase 1.

---

## 13. Historique

| Date | Changement |
|------|------------|
| 2026-04-21 | Création du brief développeur front Phase 1. |
| 2026-04-21 | **Analyse / amendement** : liens markdown et **tableau** des références ; homepage **Option B** / variante wireframe ; **hiérarchie visuelle** hero vs packshots (`docs/assets/`, charte **7.2**, brief visuel **10.2–10.3**) ; **copy hero** nuancé (gel spec §7 vs **polissage** / assets finaux provisoires) ; critères d’acceptation et livrables **hero** précisés ; renvoi **README**. |
| 2026-04-21 | **§2** + **§7** : principe explicite **respect maximal d’Odoo 19 CE** (front + back-office), personnalisation **mesurée** ; **§3** + **§4** : formulation **header** + menu personnalisé. |