# DESIGN — C-Kreyol

Document de **cadrage design / front-end** pour le canal **C-Kreyol** (Odoo 19 CE). Il complète la [vision média-commerce](VISION_CK_MEDIA_COMMERCE.md) ([ADR-CKR-009](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-009)), la [doctrine e-commerce B2C / B2B](DOCTRINE_CK_ECOMMERCE_B2C_B2B.md) ([ADR-CKR-010](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-010)), la [doctrine langues créoles](DOCTRINE_CK_LANGUES_CREOLES.md) ([ADR-CKR-011](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-011) — orientation long terme, hors mandat MVP), la [note de cadrage Phase 1](NOTE_DE_CADRAGE.md), le [registre ADR](ARCHITECTURE_DECISION_RECORD.md) et le [README](../../README.md). Il ne remplace pas les **décisions juridiques**, **commerciales** ni le **paramétrage stock** ; il en **reflète** les contraintes côté **promesse affichée** et **expérience utilisateur** — y compris la **protection** du tunnel d’achat et la **secondarité** des signaux non marchands vis-à-vis du CTA (cf. vision §6).

---

## 1. Objet du document

Ce document a pour objet de :

- poser le **rôle du design** dans le projet Phase 1 ;
- lister les **benchmarks** utiles et la **lecture** qu’on en tire pour C-Kreyol ;
- formaliser les **principes** design et **retail**, et les **patterns retail** privilégiés en Phase 1 (§5.1) ;
- décrire les **attendus** par grande zone de page (navigation, accueil, collections, fiche produit, footer) ;
- rappeler les **exigences mobile** et les **zones obligatoirement personnalisées** ;
- signaler les **pièges à éviter** ;
- ouvrir des **pistes d’identité visuelle** et des **questions** encore ouvertes.

**Périmètre technique** : site **website / e-commerce** Odoo 19 CE, dans le respect des [ADR-CKR-001](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-001) à [ADR-CKR-005](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005) (standard d’abord, front-end spécifique maîtrisé, promesse de disponibilité alignée sur la réalité — cf. conséquences ADR-005) et de l’**orientation** [ADR-CKR-009](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-009) (hiérarchie e-commerce vs éditorial / communautaire sur le long terme).

---

## 2. Rôle du design dans le projet

Le design n’est **pas** un habillage tardif : il porte la **crédibilité retail**, la **lisibilité de l’offre** et la **cohérence** entre la **marque C-Kreyol** et le **modèle opératoire** (achat-revente, hub Nantes, flux tendu, stock consigné — ADR-004 / ADR-005).

En Phase 1, le design doit en particulier :

- rendre **C-Kreyol identifiable** (non confondable avec un site « template Odoo » ni avec **La Platine**) ;
- soutenir une **navigation commerciale et éditoriale** sobre mais structurante (sans copier la largeur d’un grand catalogue) ;
- **protéger** le canal contre la **sur-promesse** (disponibilités, délais, « toujours en stock ») — alignement explicite avec les conséquences d’**[ADR-CKR-005](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005)** ;
- garantir une **expérience mobile web** **exigeante** (must have fonctionnel, cf. note §6.1).

---

## 3. Benchmarks de référence

Les benchmarks servent de **références de lecture** (retail, navigation, profondeur d’offre), **pas** de modèles à copier intégralement en Phase 1.

### 3.1 La Maison des Antilles

**Référence** : [lamaisondesantilles.com](https://www.lamaisondesantilles.com/) — acteur français historique de l’**épicerie fine antillaise et créole** en ligne (volumétrie d’offre élevée, services type **entreprises / CSE**, contenus **blog / recettes**, ancrage **boutique physique** à Paris).

**Lecture pour C-Kreyol** :

- démontre qu’un **marché** existe pour l’**épicerie antillaise** sérieuse en France métropolitaine ;
- combine **catalogue profond**, **confiance** (livraisons, service client, preuves sociales) et **rayonnement éditorial** ;
- **C-Kreyol** ne vise **pas** la même **largeur** de catalogue en Phase 1, mais peut s’inspirer de la **tenue retail** (clarté des catégories, sobriété informationnelle relative à la complexité du rayon).

### 3.2 Caribshopper

Déjà cadré en [NOTE_DE_CADRAGE.md §4.5](NOTE_DE_CADRAGE.md) : benchmark **logique retail digital** (entrées **Bestsellers**, **New Arrivals**, **Recipes**, **Reviews** ; axes **territoire** ; **collections thématiques** ; logique **cadeau** ; site **wholesale B2B** distinct).

**Lecture pour C-Kreyol** :

- **dispositif retail** plutôt que simple empilement de fiches ;
- **front-end** et **navigation** comme leviers de **marque** et d’**exploration** de l’offre ;
- **B2B** comme **horizon** (cf. note §4.1), **sans** diluer le focus **B2C retail** Phase 1 sauf décision contraire.

**C-Kreyol** conserve en Phase 1 une **inspiration retail avant tout B2C**, tout en **préparant à terme** une fonction d’**intermédiation B2B** distincte — potentiellement portée par des **parcours**, **contenus** ou **espaces** séparés (sur le modèle *wholesale* distinct observé chez Caribshopper), **sans** les activer comme priorité jour 1 sauf **décision** explicite.

### 3.3 Synthèse pour C-Kreyol

| Dimension | C-Kreyol Phase 1 (direction) |
|-----------|--------------------------------|
| **Identité** | Marque **propre**, **Nantes** + **Antilles** (double ancrage note §2) |
| **Profondeur catalogue** | **Limitée** et **maîtrisée** ; qualité **retail** > exhaustivité |
| **Navigation** | Entrées **commerciales** + **éditoriales** modestes mais **claires** (inspiration Caribshopper, envergure réduite) |
| **B2B** | **Horizon** : parcours / contenus / espace **séparés** possibles plus tard ; **Phase 1** = **retail B2C** prioritaire (note §4.1) |
| **Confiance** | Alignement **strict** promesse / **stock observable** et **engagements fournisseurs** (ADR-005) |
| **Mobile** | **Must have** — parcours complet utilisable sur smartphone |
| **Technique** | Odoo 19 CE — **personnalisation** concentrée sur le **champ présentationnel** (ADR-002 / ADR-003) |

---

## 4. Principes de design front-end

1. **Présentationnel d’abord** — Thème, SCSS, QWeb *website*, JS d’**habillage** ou d’**UX** : oui, dans le cadre [ADR-CKR-002](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-002). **Pas** de logique métier **parallèle** au standard dans le front.
2. **Navigation + footer = identité** — [ADR-CKR-003](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-003) : **menu principal** et **footer** entièrement **personnalisés** ; le rendu standard Odoo sur ces zones **n’est pas** la base finale.
3. **Cohérence système** — Typo, couleurs, espacements, états de survol / focus : **système** reproductible (maintenabilité).
4. **Accessibilité raisonnable** — Contrastes lisibles, tailles de cibles tactiles, textes alternatifs **produit** ; pas d’exigence « WCAG audit complet » figée ici sans arbitrage.
5. **Performance perçue** — Images dimensionnées, lazy-load où pertinent, éviter le surplus d’animations sur **mobile**.

---

## 5. Principes retail

1. **Mise en scène** — L’offre est **curatée** : mises en avant, collections, « nouveautés » **sincères**.
2. **Origine lisible** — Territoires / producteurs / **La Platine** comme **premier fournisseur** : information **honnête**, pas marketing creux.
3. **Collections éditoriales** — Même **petites** en Phase 1 (ex. usages, occasions, saison) pour guider sans noyer.
4. **Tunnel de confiance** — Prix, frais, livraison, délais : **transparence** ; pas de promesse de disponibilité **supérieure** à la réalité (ADR-005).
5. **Qualité perçue** — Photos et textes **au niveau** des produits **agro transformés** (ingrédients, allergènes si pertinent — cf. note §7.3).

### 5.1 Patterns retail à privilégier en Phase 1

- **Mises en avant courtes et sincères** : best sellers **réels**, nouveautés **réelles**, sélections **limitées** ;
- **Collections lisibles** : peu nombreuses, clairement nommées, compréhensibles **sans effort** ;
- **Éditorial léger** : une phrase **utile** vaut mieux qu’un discours long ;
- **Badges sobres** : éviter la prolifération de **labels visuels** concurrents ;
- **Repères de confiance visibles** : contact, livraison, conditions **claires**, sans envahir la page ;
- **Hiérarchie visuelle simple** : le client doit comprendre **vite** où cliquer, quoi regarder, quoi acheter.

---

## 6. Navigation principale

- **Structure** : hiérarchie **claire** — détail des **entrées de niveau 1**, options et arbitrages : voir **[STRUCTURE_MENU_PRINCIPAL.md](STRUCTURE_MENU_PRINCIPAL.md)** ; cohérent avec les **patterns** §5.1.
- **Comportement** : **responsive** / **mobile-first** ; menu mobile **sans friction majeure** (note §6.1, §9.2, §13).
- **Marque** : logo / wordmark **C-Kreyol** cohérent avec le fichier versionné `static/description/c_kreyol_logo.png` (cf. README).
- **E-commerce natif** : conserver les **comportements** utiles d’Odoo (panier, compte, recherche) tout en **contrôlant** la **composition visuelle** (ADR-003).

---

## 7. Homepage

Objectifs **prioritaires** :

- **proposition de valeur** immédiate (marque + spécialité **agro transformés antillais** + **origine produit** lisible dans le **hero** si sobre ; **Nantes** et **cadre projet** plutôt **plus bas** ou **À propos** — [SPEC_HERO_HOMEPAGE.md](SPEC_HERO_HOMEPAGE.md) §1 / §4) ;
- **portes d’entrée** vers le **catalogue** et **1 à 3** blocs **éditoriaux** (collections, mise en avant fournisseur / origine) ;
- **signaux de confiance** (livraison, contact, liens légaux visibles sans encombrer) ;
- **pas** de surcharge type « marketplace » : **discipline** retail Phase 1.

**Filaire détaillé** (blocs, variantes sobre / enrichie, décision cible Phase 1) : **[WIREFRAME_HOMEPAGE.md](WIREFRAME_HOMEPAGE.md)** — cohérent avec [STRUCTURE_MENU_PRINCIPAL.md](STRUCTURE_MENU_PRINCIPAL.md) (**Option B**). **Hero** (message, CTA, visuel) : **[SPEC_HERO_HOMEPAGE.md](SPEC_HERO_HOMEPAGE.md)** ; **production visuelle** hero : **[BRIEF_VISUEL_HERO_PHASE1.md](BRIEF_VISUEL_HERO_PHASE1.md)**.

**Blocs attendus** (résumé — l’ordre implémenté : `ckr_homepage.xml` ; doctrine portes catalogue : [ADR-006 à 008](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-006), [WIREFRAME_HOMEPAGE.md](WIREFRAME_HOMEPAGE.md) Bloc 3) :

1. **Hero principal** — message marque + CTA **boutique** + CTA secondaire **Explorer le catalogue** (ancre section Explorer) ;
2. **Explorer / Par où commencer** — **cinq portes catalogue** : libellés front au **pluriel** **Promotions**, **Collections**, **Kits**, **Catégories**, **Origines**. Pour la porte 3, règle de bi-lexique [ADR-CKR-008](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008) : **Kits** côté visiteur (entrée unique vers les produits `pack_ok`), **Pack** côté back-office et source de vérité (module OCA **`product_pack`**, case *« Est un pack ? »* = `pack_ok`). **Doctrine métier** [DOCTRINE_CK_PACK_VS_KIT.md](DOCTRINE_CK_PACK_VS_KIT.md) : en **copy** et **titres produits**, **pack** = assemblage **homogène** (conditionnement), **kit** = **hétérogène** (usage, recette, expérience) — la carte **Kits** peut donc mener à une liste contenant les deux types, nommés correctement sur chaque fiche. **≠** menu Option B (Boutique / **Communauté** — Idées cadeaux, Recettes, Blog — restent navigation **générale**) ; **présentation** : rail horizontal **sans autoplay**, boutons précédent/suivant + scroll natif + flèches clavier — [WIREFRAME_HOMEPAGE.md — Bloc 3](WIREFRAME_HOMEPAGE.md) (*Présentation front*) ;
3. **Mise en avant fournisseur / origine** — **La Platine** comme **premier fournisseur**, sans confusion de marque ;
4. **Sélection produits** — best sellers / nouveautés **sincères** (ADR-005) ;
5. **Bloc retail éditorial** — collection / saison / cadeau / usages **si contenu crédible** ;
6. **Bloc confiance** — livraison prudente, contact, paiement, qualité / origine ;
7. **Footer** — personnalisé (ADR-003).

---

## 8. Pages collections / catégories

- **Grille** lisible, filtres **si** le catalogue le justifie ; sinon **simplicité** absolue.
- **Cartes produit** : image, titre, prix, **indication d’origine** ou **badge** court si utile.
- **Éditorial léger** en tête de collection (1–2 phrases + visuel optionnel) pour **humaniser** le rayon.

---

## 9. Fiche produit

Alignement avec la note §7.3 : nom, **photo**, description, **origine**, composition / ingrédients, **allergènes** si pertinents, format, prix, **conditions de livraison / retrait**, informations **réglementaires**.

Côté design :

- **hiérarchie** titre → prix → disponibilité / délai (**prudent**) → détail ;
- **pas** d’affichage « marketing » de la disponibilité qui contredirait le **stock réel** ou les engagements (ADR-005) ;
- **cross-sell** modéré (accessoires / même univers) si cohérent avec la taille du catalogue.

---

## 10. Footer

Conformément à [ADR-CKR-003](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-003) :

- **personnalisation entière** (structure, contenus, hiérarchie) ;
- blocs typiques : **liens légaux**, **contact**, **livraison / retours** (renvoi pages dédiées), éventuellement **réseaux** ou **newsletter** si activée ;
- **cohérence visuelle** avec le header (même système typographique et couleurs).

---

## 11. Exigences mobile

Référence normative : note **§6.1**, **§9.2**, **§13** et README.

- Parcours **catalogue → fiche → panier → commande** **utilisable** et **de qualité** sur **smartphone** ;
- **tests** sur appareils réels (tailles d’écran courantes) ;
- **pas** d’application native en Phase 1 (hors périmètre) : l’**exigence** porte sur le **web mobile**.

---

## 12. Éléments obligatoirement personnalisés

- **Menu de navigation principal** ([ADR-CKR-003](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-003)) ;
- **Footer** (idem) ;
- **Thème / assets** globaux portant l’identité **C-Kreyol** (dans le champ ADR-002).

---

## 13. Éléments à éviter

- **Rendu « standard Odoo »** sur le **header / nav** et le **footer** comme état final (ADR-003) ;
- **Sur-promesse** disponibilité / délais / « en stock » **non** soutenus par la **chaîne** et le **stock observable** (ADR-005, note §12.2) ;
- **Sur-personnalisation métier** en front (contournements Python / QWeb lourds) — [ADR-CKR-002](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-002) ;
- **Catalogue** ou **navigation** à la hauteur d’un **agrégateur** dès la Phase 1 (hors vision) ;
- **Polish « agence »** bloquant la **première vente** (README — itérer après mise en ligne si besoin) ;
- **Front-end trop chargé** — multiplication d’**entrées**, **badges**, **couleurs** ou **messages** concurrents au point de **brouiller** la **lecture retail** (inspiration ≠ accumulation).

---

## 14. Pistes d’identité visuelle

**Séquence** : les choix **palette**, **typo** et **usages logo** utiles au **gel du hero** et au **thème** sont à consolider dans **[CHARTE_GRAPHIQUE_PHASE1.md](CHARTE_GRAPHIQUE_PHASE1.md)** (charte **minimale** Phase 1) **avant** de figer définitivement [SPEC_HERO_HOMEPAGE.md](SPEC_HERO_HOMEPAGE.md) — sans attendre une **charte agence** complète.

**Pistes DA** : **[DIRECTIONS_ARTISTIQUES_PHASE1.md](DIRECTIONS_ARTISTIQUES_PHASE1.md)** — trois directions + **recommandation** ; **gel** des choix dans **[CHARTE_GRAPHIQUE_PHASE1.md](CHARTE_GRAPHIQUE_PHASE1.md)** **§3–§11** (**Direction A**).

- **Logo** officiel : `static/description/c_kreyol_logo.png` (cf. README) ;
- **Territoires** : équilibre **métropole (Nantes)** et **Antilles** (origine produits) — éviter les clichés **exotiques** cheap ; viser **chaleur** et **sérieux** ;
- **Palette et typo** : **à définir** dans la charte (system tokens SCSS + polices web **légères** et **lisibles**) ; **propositions** dans [DIRECTIONS_ARTISTIQUES_PHASE1.md](DIRECTIONS_ARTISTIQUES_PHASE1.md) ;
- **Photographie** : produits **réels** ; cohérence de **style** (lumière, fond) sur le catalogue initial.

---

## 15. Questions ouvertes

- **Palette** et **typographies** finales (charte complète ou itération par étapes ?) ;
- **Langues** du site (FR minimum ; créole / anglais : **à trancher** — note README) ;
- **Nombre et intitulés** des entrées **éditoriales** du menu (recettes, cadeaux, territoires : lesquels en V1 ?) ;
- **Nantes** sur la homepage : **pas** de mise en avant dans le **hero** Phase 1 (**tranché** [SPEC_HERO_HOMEPAGE.md](SPEC_HERO_HOMEPAGE.md) §4) ; reste possible **plus bas** (confiance, **À propos**) ;
- **Harmonisation** avec d’éventuels **autres** sites Dorevia (conflit ou réutilisation de patterns) ;
- **Process** de **revue design** vs **revue technique** (qui valide la conformité ADR-002 / disponibilité ADR-005 sur les maquettes ?).

---

## Historique du document

| Date | Changement |
|------|------------|
| 2026-04-21 | Création du squelette **DESIGN.md** : objet, rôle design, benchmarks (Maison des Antilles, Caribshopper), principes front / retail, zones de page, mobile, ADR, questions ouvertes. |
| 2026-04-21 | **§3.2 / §3.3** : dimension **B2B** (horizon, parcours séparés). **§4** : principe **honnêteté visuelle**. **§5.1** : **patterns retail** Phase 1. **§7** : blocs homepage structurés. **§13** : risque **front surchargé**. |
| 2026-04-21 | **§6** : renvoi vers **[STRUCTURE_MENU_PRINCIPAL.md](STRUCTURE_MENU_PRINCIPAL.md)** (structure cible du menu principal Phase 1). |
| 2026-04-21 | **§7** : renvois **[WIREFRAME_HOMEPAGE.md](WIREFRAME_HOMEPAGE.md)** et **[SPEC_HERO_HOMEPAGE.md](SPEC_HERO_HOMEPAGE.md)** ; résumé des blocs aligné menu **Option B** ; wireframe enrichi (hero, carrousel, blocs 3–5–7). |
| 2026-04-21 | **§14** : séquence **charte minimale** → **spec hero** ; lien **[CHARTE_GRAPHIQUE_PHASE1.md](CHARTE_GRAPHIQUE_PHASE1.md)**. |
| 2026-04-21 | **§7** / **§15** : hero = **origine produit** ; **Nantes** hors hero ; renvoi **[SPEC_HERO_HOMEPAGE.md](SPEC_HERO_HOMEPAGE.md)** §1 / §4. |
| 2026-04-21 | **§14** : renvoi **[DIRECTIONS_ARTISTIQUES_PHASE1.md](DIRECTIONS_ARTISTIQUES_PHASE1.md)** (3 pistes DA + reco) ; **palette / typo** reliées à la charte. |
| 2026-04-21 | **§14** : **CHARTE** **Direction A** gelée (**§3–§11**) ; pistes DA = antécédent créatif. |
| 2026-04-21 | **§7** : lien **[BRIEF_VISUEL_HERO_PHASE1.md](BRIEF_VISUEL_HERO_PHASE1.md)** (livrables visuels hero). |
| 2026-04-21 | **§7** : blocs homepage — **Explorer** (cinq portes) documenté via **ADR-006 à 008** + **WIREFRAME** Bloc 3 ; specs portes / contrats d’URL regroupés sous **`docs/mvp_01/`** (anciennement `docs/phase_2/`). |
| 2026-04-23 | **§7** : bloc **Explorer** — précision **présentation front** (rail manuel, sans autoplay, prev/next) ; renvoi **[WIREFRAME_HOMEPAGE.md](WIREFRAME_HOMEPAGE.md)** Bloc 3. |
| 2026-04-21 | **§7** : libellés Explorer — **Promotion**, **Collection**, **Kit**, **Catégorie**, **Origine** (**Kit** = composition). |
| 2026-04-21 | **§7** : libellés Explorer passés au **pluriel** — **Promotions**, **Collections**, **Kits**, **Catégories**, **Origines** (harmonisation lecture visiteur). |
| 2026-04-21 | **§7** : porte **Kits → Packs** — alignement sur la logique pack Odoo / OCA **`product_pack`** après vérification back-office (case *« Est un pack ? »*, onglet *Pack*). Libellés retenus : **Promotions**, **Collections**, **Packs**, **Catégories**, **Origines**. |
| 2026-04-21 | **§7** : règle de **bi-lexique front / back-office** [ADR-CKR-008](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008) — libellé **visiteur** = **Kits** (univers alimentaire C-Kreyol), **grille back-office / source de vérité** = **Pack** (module OCA `product_pack`, `pack_ok`). Libellés Explorer : **Promotions**, **Collections**, **Kits**, **Catégories**, **Origines**. |
| 2026-04-26 | **§7** : doctrine métier **[DOCTRINE_CK_PACK_VS_KIT.md](DOCTRINE_CK_PACK_VS_KIT.md)** — **pack** homogène (conditionnement) vs **kit** hétérogène (usage / expérience) pour **copy** et **titres** ; carte **Kits** = entrée unique `pack_ok`. |
