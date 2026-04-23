# Registre des décisions d’architecture — projet C-Kreyol

Ce fichier consigne les **décisions d’architecture** (ADR) prises pour le canal **C-Kreyol** — en complément de la [note de cadrage Phase 1](NOTE_DE_CADRAGE.md) et du [README](../README.md).

**Règle** : toute décision structurante sur le socle technique, les modules Odoo, ou la doctrine de construction, une fois **actée**, est référencée ici avec un identifiant stable **ADR-CKR-xxx**.

Les **ADR-CKR-001 à 005** couvrent surtout la **Phase 1** ; les **ADR-CKR-006 à 008** couvrent la **doctrine Phase 2** (homepage d’orientation, convergence boutique, portes d’exploration catalogue).

---

<a id="adr-ckr-001"></a>

## ADR-CKR-001 — Doctrine de construction Phase 1 : composition maîtrisée sur Odoo 19 CE

| Champ | Contenu |
|--------|---------|
| **Statut** | **Acceptée** — en vigueur pour la Phase 1 tant qu’elle n’est pas explicitement révisée. |
| **Date** | 2026-04-21 |
| **Périmètre** | Implémentation **Phase 1** du canal C-Kreyol sur **Odoo 19 Community Edition**. |

### Contexte

La Phase 1 ne vise pas une création *ex nihilo* de toutes les briques, mais une mise en ligne **opérable** et **cohérente**. Le socle Odoo 19 CE offre déjà une **couverture fonctionnelle large** via les modules activables ; le risque principal est la **disharmonie** (surconstruction, spécifique prématuré, incohérence catalogue → paiement → livraison).

### Décision

Adopter la **doctrine de composition maîtrisée** détaillée en [NOTE_DE_CADRAGE.md §3.5](NOTE_DE_CADRAGE.md) :

1. **Prioriser** le socle standard Odoo CE et les activations pertinentes.
2. **Éviter** la surconstruction et le développement prématuré.
3. **Viser** la cohérence d’ensemble (catalogue, commande, paiement, livraison, information client, exécution).
4. **N’ajouter du spécifique** (custom module, surcharges lourdes) que si le standard et la composition des modules activables **ne suffisent pas** à tenir le modèle métier retenu.

L’objectif affiché est un **premier canal harmonieux**, crédible et réellement exploitable — **pas** la sophistication maximale à court terme.

### Conséquences

- Les arbitrages **modules / paramétrage** doivent être jugés d’abord sous l’angle **« standard d’abord »**.
- Toute dérogation (nouveau module maison, fork lourd) doit être **justifiée** par un écart documenté par rapport au standard.
- La note de cadrage reste la **source narrative** ; la présente entrée **fige** la décision pour le pilotage technique et les revues de conception.
- Le sens de « spécifique » en Phase 1 est **resserré** par [ADR-CKR-002](#adr-ckr-002) (front-end seul en présumé légitime).

### Références

- [NOTE_DE_CADRAGE.md — §3.5 Doctrine de construction de la Phase 1](NOTE_DE_CADRAGE.md) (texte normatif détaillé).
- [README — Choix technique cible](../README.md) (Odoo 19 CE).

---

<a id="adr-ckr-002"></a>

## ADR-CKR-002 — Phase 1 : seul le front-end est spécifique présumé légitime

| Champ | Contenu |
|--------|---------|
| **Statut** | **Acceptée** — en vigueur pour la Phase 1 tant qu’elle n’est pas explicitement révisée. |
| **Date** | 2026-04-21 |
| **Périmètre** | Implémentation **Phase 1** du canal C-Kreyol sur **Odoo 19 CE**, avec focus sur la distinction **front-end** / **cœur métier**. |
| **Liée à** | [ADR-CKR-001](#adr-ckr-001) (composition maîtrisée). |

### Contexte

L’[ADR-CKR-001](#adr-ckr-001) pose que le spécifique n’intervient que si le standard ne suffit pas. En Phase 1, il faut **resserrer** ce principe pour éviter toute dérive vers du développement « métier » ou « intégration » prématurés alors que le socle couvre déjà la plupart des flux e-commerce.

### Décision

En **Phase 1**, le **seul spécifique présumé légitime** sans dossier d’exception préalable est le **front-end** (thème, assets, habillage du site, héritages de vues *website* à visée **présentationnelle**).

Ce spécifique front-end est légitime tant qu’il reste **présentationnel, éditorial ou UX**, et qu’il ne reconstitue pas en sous-main une logique métier parallèle au standard (y compris via QWeb, contrôleurs *website* ou JavaScript lorsque ceux-ci contournent le cœur métier au lieu de l’habiller).

**Tout le reste** — logique métier additionnelle, automatisations lourdes, connecteurs, contournements du standard pour stock / facturation / e-mails / paiement, etc. — doit **d’abord** chercher sa solution dans le **standard Odoo CE** et les **modules activables**. Tout écart doit rester **exceptionnel** et être **justifié** (écart documenté, risque assumé, coût de possession accepté).

### Conséquences

- Le travail **thème / SCSS / XML front boutique** peut démarrer tôt si nécessaire pour l’identité C-Kreyol.
- Les demandes de **module Python maison**, **override** de modèles comptables / stock, ou **API** dédiées en Phase 1 sont **suspectes par défaut** : elles passent par une revue « standard d’abord » + décision explicite (éventuellement futur ADR ou levée d’exception consignée).
- L’[ADR-CKR-001](#adr-ckr-001) reste valide ; la présente décision **précise** le sens de « spécifique » pour la fenêtre Phase 1.

### Références

- [NOTE_DE_CADRAGE.md — §3.5](NOTE_DE_CADRAGE.md) (doctrine de construction).
- [ADR-CKR-001](#adr-ckr-001).
- [ADR-CKR-003](#adr-ckr-003) — navigation principale et footer entièrement personnalisés en Phase 1.

---

<a id="adr-ckr-003"></a>

## ADR-CKR-003 — Front-end : navigation principale et footer entièrement personnalisés

| Champ | Contenu |
|--------|---------|
| **Statut** | **Acceptée** — en vigueur pour la Phase 1 tant qu’elle n’est pas explicitement révisée. |
| **Date** | 2026-04-21 |
| **Périmètre** | Front-end **website / e-commerce** de C-Kreyol sur **Odoo 19 CE**. |
| **Liée à** | [ADR-CKR-002](#adr-ckr-002) (front-end = spécifique présumé légitime). |

### Contexte

Le rendu standard Odoo du **menu de navigation** et du **footer** ne correspond pas à l’identité recherchée pour **C-Kreyol**. Ces deux éléments sont structurants dans la perception du site : ils portent la marque, la hiérarchie de navigation, la crédibilité visuelle et la sensation d’ensemble du canal.

Le maintien du standard Odoo sur ces zones créerait une dissonance avec l’ambition de **front-end spécifique** posée pour la Phase 1.

### Décision

Pour **C-Kreyol**, le **menu de navigation principal** et le **footer** du front-end doivent être **entièrement personnalisés**.

Cette personnalisation est considérée comme :

- **obligatoire** pour l’identité du canal ;
- **compatible** avec la doctrine « standard d’abord » dès lors qu’elle reste dans le champ du **front-end présentationnel** ;
- distincte de toute réécriture inutile du cœur métier Odoo.

Le standard visuel Odoo sur ces deux éléments n’est **pas retenu** comme base finale pour la Phase 1.

### Conséquences

- Le chantier **front-end** doit inclure explicitement une refonte du **header / navigation** et du **footer**.
- Les comportements fonctionnels utiles du standard peuvent être conservés si nécessaire, mais leur **expression visuelle** et leur **composition** doivent être propres à **C-Kreyol**.
- Toute implémentation devra préserver :
  - la lisibilité ;
  - le responsive ;
  - l’accès aux pages utiles ;
  - la maintenabilité du thème.

### Références

- [ADR-CKR-002](#adr-ckr-002)
- [NOTE_DE_CADRAGE.md — §3.5](NOTE_DE_CADRAGE.md)
- [STRUCTURE_MENU_PRINCIPAL.md](STRUCTURE_MENU_PRINCIPAL.md) — structure cible du menu principal Phase 1
- [WIREFRAME_HOMEPAGE.md](WIREFRAME_HOMEPAGE.md) — structure cible de la homepage Phase 1

---

<a id="adr-ckr-004"></a>

## ADR-CKR-004 — Modèle commercial Phase 1 : achat-revente (C-Kreyol vend et encaisse, achète à La Platine)

| Champ | Contenu |
|--------|---------|
| **Statut** | **Acceptée** — en vigueur pour la Phase 1 tant qu’elle n’est pas explicitement révisée ; **conditions contractuelles détaillées** (prix, facturation fournisseur, TVA, responsabilités) à **documenter** avec les experts. |
| **Date** | 2026-04-21 |
| **Périmètre** | **Phase 1** : relation **C-Kreyol ↔ client final** et **C-Kreyol ↔ La Platine** en tant que **premier fournisseur** (achat marchandises / produits). |
| **Liée à** | [ADR-CKR-001](#adr-ckr-001) (paramétrage Odoo **standard d’abord** : ventes, achats, paiements). [ADR-CKR-005](#adr-ckr-005) (chaîne physique et stock au hub). |

### Contexte

Les **ADR-CKR-001 à 003** ne fixaient pas **qui vend** au client final ni **qui encaisse**. Sans clarification, le canal restait ambigu (vitrine, commission pure, dropshipping « subi », etc.).

**La Platine** est le **premier fournisseur** ; le modèle doit permettre de construire **C-Kreyol** comme **actif commercial autonome** tout en restant compatible avec une **logistique hub + consignation** décrite en [ADR-CKR-005](#adr-ckr-005).

### Décision

Pour la **Phase 1**, **C-Kreyol** :

- **vend** au **client final** (relation commerciale **grand public** portée par **C-Kreyol**) ;
- **encaisse** les paiements clients (dans le cadre des moyens de paiement retenus et des obligations réglementaires) ;
- **achète** les produits à **La Platine** dans une logique d’**achat-revente** (et non une simple vitrine sans acte commercial autonome de **C-Kreyol**).

Le **modèle cible** **combine** une **relation commerciale de type achat-revente** (cette décision) avec une **organisation logistique** en **stock consigné** et **flux tendu** au hub ([ADR-CKR-005](#adr-ckr-005)), sous réserve de **formalisation contractuelle et comptable** précise. Il ne s’agit **pas** d’un dilemme « achat-revente **ou** consignation » : la **revente** qualifie le **flux commercial** ; la **consignation** qualifie la **gestion physique et juridique** des biens **avant** et **après** les **événements de transfert** actés.

Les **modalités contractuelles et comptables** précises (conditions générales d’achat, facturation fournisseur, TVA, alignement avec la **consignation** — cf. ADR-005) font l’objet d’une **documentation complémentaire** avec conseil **juridique / fiscal**.

### Conséquences

- **CGV**, **mentions légales** et **facturation client** : cohérence avec **C-Kreyol** comme **vendeur** vis-à-vis du client final.
- **Odoo** : enchaînement **ventes** (boutique) ↔ **achats** (La Platine) **sans** inventer de module métier tant que le standard suffit ([ADR-CKR-001](#adr-ckr-001)).
- La **physique** (hub, préparation, expédition, stock) est pilotée par [ADR-CKR-005](#adr-ckr-005) ; la présente décision **ne la substitue pas**.

### Références

- [NOTE_DE_CADRAGE.md — §4.3, §5, §5.4](NOTE_DE_CADRAGE.md)

---

<a id="adr-ckr-005"></a>

## ADR-CKR-005 — Modèle logistique cible Phase 1 : hub léger à Nantes, flux tendu, stock consigné

| Champ | Contenu |
|--------|---------|
| **Statut** | **Acceptée** — en vigueur comme **hypothèse de travail cible** pour la Phase 1 ; **événements de transfert de propriété**, **risques** pendant consignation et **représentation stock** dans Odoo restent à **affiner** avec le **juridique** et l’**opérationnel** (cf. note §5.4). |
| **Date** | 2026-04-21 |
| **Périmètre** | **Phase 1** : chaîne **physique** et **stock** (Nantes, fournisseur, client), **sans** prétendre figer dès le jour 1 une **modélisation juridique maximale** si elle bloque l’ouverture. |
| **Liée à** | [ADR-CKR-004](#adr-ckr-004) (achat-revente : écoulement des marchandises **après** achat à La Platine). [ADR-CKR-001](#adr-ckr-001) (traduction Odoo **simple** acceptable). |

### Contexte

Le projet se distingue d’un **pur dropshipping** comme d’un **stock lourd classique** immobilisant massivement la trésorerie. **Nantes** doit avoir un **rôle physique réel** (point d’appui, réception possible, préparation / redistribution selon capacité), en cohérence avec la vision **import-export** à construire.

### Décision

Le **modèle cible privilégié** pour **C-Kreyol** est un **hub logistique léger à Nantes**, fonctionnant en **flux tendu**, avec **stock consigné** **côté fournisseur** (notamment **La Platine**) **tant que les conditions de transfert** (propriété, facturation, ou autres **événements contractuels** à définir) **ne sont pas réalisées**.

Parmi les **trois familles** décrites en [NOTE_DE_CADRAGE.md §4.4](NOTE_DE_CADRAGE.md), cette lecture correspond à un **hub léger** (famille **2**), **pas** à un pur canal sans passage physique (**1**) ni, en Phase 1, à une **logistique lourde** complète (**3**).

Les produits **fournis par La Platine** peuvent **transiter ou être positionnés** sur le **point d’appui nantais** ; la visée est une **rotation rapide** et **peu de stock dormant**, compatible avec l’**achat-revente** posé en [ADR-CKR-004](#adr-ckr-004).

### Conséquences

- **Visibilité stock / disponibilité côté client** : la **promesse** affichée au client (site, fiches produit, délais, messages du tunnel) ne devra **pas excéder** la **fiabilité réelle** du stock **observable** et des **engagements fournisseurs** — sous peine de **sur-promesse** et de friction **front** / **SAV** (cf. note §12.2 ; cohérence avec le **front-end** [ADR-CKR-002](#adr-ckr-002) et la **composition standard** [ADR-CKR-001](#adr-ckr-001)).
- **Préparation** et **expédition** : à **répartir** explicitement (équipe / lieu **Nantes**, **La Platine**, tiers) dans les **procédures** et, le cas échéant, dans **Odoo** (entrepôts, types d’opérations) — sans sur-promesse sur ce qui est **réellement** exécutable jour 1.
- **Règle d’implémentation Odoo** : **figer d’abord** le **modèle métier** et les **flux réels** ; **ensuite** choisir la **traduction** dans **Odoo 19 CE** la **plus simple acceptable** — **pas** l’inverse. Éviter en Phase 1 une **sur-modélisation** de la **consignation** si elle **retarde** une chaîne **opérable** (lien note §5.4, §11.3).
- Les points ouverts (**moment du transfert de propriété**, suivi de **consignation**, **risques** casse / perte / **péremption** pendant consignation) doivent être **listés et tranchés** avec conseils **juridiques** et **opérationnels**, puis reflétés dans les **CGV** et la **communication** (cf. note §12.2 sur-promesse).

### Références

- [NOTE_DE_CADRAGE.md — §4.2, §4.4, §5.4, §8, §12.2](NOTE_DE_CADRAGE.md)
- [ADR-CKR-004](#adr-ckr-004)

---

## Phase 2 — Doctrine de navigation produit et homepage

Les décisions **ADR-CKR-006 à 008** figent la **Phase 2** pour l’**architecture d’orientation** du site, la **convergence commerciale** sur la Boutique et les **cinq portes d’exploration** du catalogue. Elles **complètent** les **ADR-CKR-001 à 005** sans les réviser.

---

<a id="adr-ckr-006"></a>

## ADR-CKR-006 — Homepage Phase 2 : page d’orientation structurée

| Champ | Contenu |
|--------|---------|
| **Statut** | **Acceptée** — en vigueur pour la **Phase 2** (homepage) tant qu’elle n’est pas explicitement révisée. |
| **Date** | 2026-04-21 |
| **Périmètre** | **Homepage** du canal C-Kreyol sur **Odoo 19 CE** (contenus, blocs structurants, cohérence avec header et footer). |
| **Liée à** | [ADR-CKR-001](#adr-ckr-001) (composition maîtrisée). [ADR-CKR-002](#adr-ckr-002) (front-end spécifique légitime). [ADR-CKR-003](#adr-ckr-003) (navigation et footer personnalisés). |

### Contexte

La Phase 1 a livré un **socle front** crédible (hero, blocs, navigation). Sans décision explicite, la homepage risque d’être traitée comme une **simple vitrine** ou une **reprise du menu** en cartes, au détriment d’une **lecture produit** claire pour le visiteur.

Les **ADR-CKR-006 à 008** (ci-dessous) formalisent l’intention : la homepage comme **architecture d’orientation** vers l’offre et les grands sujets du site.

### Décision

La **homepage C-Kreyol** est conçue comme une **page d’orientation structurée**, et non comme une simple vitrine décorative.

Elle :

1. Constitue la **colonne vertébrale du site** : premier cadre de lecture après l’arrivée sur le domaine.
2. Ouvre des **portes vers des sujets précis** (offre, marque, relation).
3. **Distribue les modes d’entrée dans l’offre produit** via une section dédiée (**Explorer** / **Par où commencer**), alignée sur les cinq logiques portées par [ADR-CKR-008](#adr-ckr-008).
4. **Articule** de manière cohérente le **header** (navigation générale du site), le **contenu de la homepage** (hors header et footer), la **Boutique** (convergence commerciale — [ADR-CKR-007](#adr-ckr-007)) et le **footer** (prolongation et stabilisation).

La **navigation générale du header** et la **section Explorer** ne jouent pas le même rôle : le header oriente vers les **grandes rubriques du canal** ; Explorer distribue les **modes d’exploration du catalogue** (détail normatif dans le cadrage Phase 2, §3 et §13.2).

### Conséquences

- Les arbitrages **contenu de la homepage** (ordre des blocs, copy, hiérarchie) doivent être jugés sous l’angle **orientation visiteur** et **cohérence avec la doctrine produit**, pas seulement esthétique.
- La section **Explorer** ne doit **pas** être réduite à un miroir du menu principal sans intention catalogue explicite.
- Les travaux **front** sur la homepage restent dans le champ **présentationnel / UX** posé par [ADR-CKR-002](#adr-ckr-002) ; toute logique métier nouvelle pour matérialiser les portes (filtres, routes) reste soumise à [ADR-CKR-001](#adr-ckr-001).

### Références

- [WIREFRAME_HOMEPAGE.md](WIREFRAME_HOMEPAGE.md) — Bloc 3 Explorer (addendum), cohérence avec le menu.
- [STRUCTURE_MENU_PRINCIPAL.md](STRUCTURE_MENU_PRINCIPAL.md) — §11 (Explorer ≠ menu Option B).
- [ADR-CKR-003](#adr-ckr-003) — menu et footer.

---

<a id="adr-ckr-007"></a>

## ADR-CKR-007 — Boutique (`/shop`) comme point de convergence commercial unique

| Champ | Contenu |
|--------|---------|
| **Statut** | **Acceptée** — en vigueur pour la **Phase 2** (parcours catalogue / boutique) tant qu’elle n’est pas explicitement révisée. |
| **Date** | 2026-04-21 |
| **Périmètre** | Relation entre les **portes d’entrée produit** et la **page Boutique** native Odoo **website_sale** (`/shop`). |
| **Liée à** | [ADR-CKR-006](#adr-ckr-006) (homepage d’orientation). [ADR-CKR-008](#adr-ckr-008) (cinq portes d’exploration). [ADR-CKR-001](#adr-ckr-001) (standard Odoo d’abord). |

### Contexte

Sans règle claire, chaque angle marketing (collection, origine, promotion…) peut déboucher sur des **pages ou silos parallèles** au flux d’achat standard, fragmentant le parcours et alourdissant la maintenance.

Le cadrage Phase 2 pose que les portes d’exploration **orientent** le visiteur mais que le **commerce** reste **centralisé** sur le mécanisme boutique standard.

### Décision

La **page Boutique** (`/shop`) est le **point de convergence commercial unique** : c’est là que s’affichent les **produits à vendre**, selon le **mode d’entrée** choisi par le visiteur.

**Les cinq portes d’exploration** ([ADR-CKR-008](#adr-ckr-008)) — **Promotions**, **Collections**, **Kits** *(libellé visiteur ; grille back-office : Pack)*, **Catégories**, **Origines** — **mènent toutes vers la Boutique** avec une lecture adaptée (filtrage, contexte, paramètres d’URL ou équivalent), et **non** vers des univers commerciaux parallèles qui remplaceraient `/shop` comme lieu principal d’achat. Cette règle est **universelle pour les portes Explorer** : **aucune** n’a vocation à déboucher à terme sur une vitrine de remplacement.

On **évite** les **silos parallèles** au flux boutique standard lorsque l’objectif est l’exploration et l’achat de produits catalogue.

### Statut des pages dédiées actuelles (`/collections`, `/kits`, `/origines`, …)

Les pages stubs actuellement raccordées à certaines cartes Explorer (ex. `/kits`, `/origines`, `/collections`) sont des **états transitoires** : elles tiennent le lien tant que le **contrat d’URL** et le **comportement de filtrage** de la porte correspondante ne sont pas câblés sur `/shop`. Leur **cible finale** est **systématiquement** une des trois issues suivantes :

1. **Disparaître** au profit d’une URL native `/shop?...` (ou `/shop/category/<id>-<slug>`) ;
2. **Se réduire à une redirection** (301 si le nom reste stable, 302 si provisoire) vers la forme canonique retenue sur `/shop` ;
3. **Devenir une façade stricte** (contrôleur CK) qui réexpose le rendu de `/shop` sans divergence — à condition que cette façade soit explicitement documentée et justifiée au cas par cas ([CONTRAT_URL_PACKS.md](phase_2/CONTRAT_URL_PACKS.md) pour la porte Kits/Pack).

Dans tous les cas, **la destination commerciale finale reste `/shop`** ; une page stub n’est jamais une « boutique secondaire ».

### Conséquences

- Les conceptions **URL**, **filtres** et **merchandising** pour chaque porte doivent rester **compatibles** avec une **arrivée sur ou dans** `/shop` (ou comportement équivalent explicitement documenté si le standard impose une variante).
- **Aucune carte Explorer ne doit pointer durablement vers une page qui n’est pas `/shop`** (ou une forme canonique de `/shop`) : tout lien vers une page dédiée est par construction un **stub** qui doit être résolu vers `/shop` à la fin de la vague d’implémentation de la porte concernée.
- Les pages **éditoriales** ou **thématiques** hors `/shop` restent possibles tant qu’elles **complètent** la doctrine (orientation, récit) sans **contredire** la convergence commerciale pour le **cœur catalogue**. Elles ne peuvent pas tenir lieu de cible finale d’une carte Explorer (elles peuvent en revanche être citées **depuis** une porte, au titre du récit).
- Toute évolution future (ex. sous-pages boutique avancées) devra **préserver** cette règle ou faire l’objet d’une **révision explicite** de la présente ADR.

### Références

- [ADR-CKR-006](#adr-ckr-006) — homepage d’orientation.
- [ADR-CKR-008](#adr-ckr-008) — définition des cinq portes.
- [phase_2/SPEC_SHOP_PORTES.md](phase_2/SPEC_SHOP_PORTES.md) — spécification d’implémentation (contrats d’URL, sources de vérité, comportements sur `/shop`, vagues A/B/C).

---

<a id="adr-ckr-008"></a>

## ADR-CKR-008 — Portes d’exploration du catalogue d’offre produit

| Champ | Contenu |
|--------|---------|
| **Statut** | **Acceptée** — en vigueur pour la **Phase 2** (doctrine catalogue) tant qu’elle n’est pas explicitement révisée. |
| **Date** | 2026-04-21 |
| **Périmètre** | **Modèle conceptuel** des entrées dans l’offre produit C-Kreyol ; matérialisation **homepage** (section Explorer) et **relais** navigation / boutique. |
| **Liée à** | [ADR-CKR-006](#adr-ckr-006) (distribution sur la homepage). [ADR-CKR-007](#adr-ckr-007) (convergence sur `/shop`). [ADR-CKR-001](#adr-ckr-001) (standard vs construction CK). |

### Contexte

Le visiteur peut entrer dans l’offre par plusieurs **lectures** (famille produit, mise en scène, assortiment, avantage prix, territoire). Sans lexique partagé, équipe métier et technique mélangent **catégorie**, **collection**, **tag** ou **page éditoriale**.

La présente **ADR-CKR-008** définit les cinq **portes d’exploration** distinctes et leur rapport au **standard Odoo** (voir aussi [WIREFRAME_HOMEPAGE.md](WIREFRAME_HOMEPAGE.md) Bloc 3).

### Décision

Le catalogue d’offre produit C-Kreyol est exploré selon **cinq logiques** distinctes et complémentaires sur le plan conceptuel :

1. **Catégorie** — structuration par **famille stable** de produits (*de quel type de produit s’agit-il ?*).
2. **Collection** — mise en scène **éditoriale** ou curatée (*sous quel angle découvrir une sélection ?*).
3. **Promotion** — entrée par **avantage commercial** identifiable (*quel avantage ou offre du moment ?*).
4. **Origine** — lecture par **repère géographique** ou territorial (*de quel territoire ou provenance ?*).
5. **Pack** — offre **assemblée** ou proposition **multi-produits** identifiée en back-office Odoo par la case **« Est un pack ? »** (booléen **`product.template.pack_ok`**) et l’onglet **Pack** (module OCA **`product_pack`**, installé sur l’instance). Cette logique **Pack** est **la grille interne / source de vérité** de la porte 5 ; le **libellé visiteur** correspondant est **Kits** (cf. règle de bi-lexique ci-dessous). Le vocabulaire ancien « composition / assemblage » **n’est plus retenu** à aucun des deux niveaux.

**Rapport au standard Odoo et socle OCA** (aligné sur le cadrage, §5) :

- **Adossées au standard Odoo** en tant que socle naturel : **catégorie**, **promotion**.
- **Adossée à une brique OCA installée** (et donc traitée au plus près d’un standard en termes de source de vérité produit) : **pack** via `product_pack` — la **construction CK** se limite à la couche de **navigation / présentation** sur `/shop` et à l’entrée Explorer.
- **Construites dans le cadre C-Kreyol** (navigation, merchandising, données ou pages dédiées au-dessus du standard) : **collection**, **origine**.

### Règle de bi-lexique front / back-office

La porte 5 introduit — et formalise pour l’ensemble du projet — une **règle de bi-lexique** explicite entre la grille **back-office / implémentation** et la grille **front / visiteur** :

| Grille | Vocabulaire | Justification | Artefacts concernés |
|--------|-------------|---------------|---------------------|
| **Back-office / source de vérité / implémentation** | **Pack** | Le module OCA `product_pack` porte nativement les champs, l’onglet et la case *« Est un pack ? »* (`pack_ok`). La source de vérité reste **unique** et non traduite côté code. | Documentation technique ([SPEC_SHOP_PORTES.md](phase_2/SPEC_SHOP_PORTES.md), [CONTRAT_URL_PACKS.md](phase_2/CONTRAT_URL_PACKS.md)), paramètres CK internes (ex. `ckr_mode=pack`), noms de champs, requêtes domaine (`pack_ok=True`), XML IDs historiques. |
| **Front / visiteur** | **Kits** | Dans l’univers **alimentaire / épicerie fine** C-Kreyol, **« kit »** est jugé plus immédiatement parlant : *kit colombo*, *kit apéritif*, *kit découverte* — il évoque une préparation, un ensemble prêt à utiliser, une offre guidée. Plus commercial et plus naturel que *pack* pour le client final. | Section Explorer (carte 3), titre de page stub, URL visible **`/kits`**, copy marketing, méta-titres, fil d’Ariane, libellés boutons. |

**Principe d’articulation** : la couche CK **ne recrée pas** une seconde source de vérité pour satisfaire le libellé front. Le **filtrage** produit reste fondé sur `pack_ok`. Le **libellé « Kits »** est une **traduction présentationnelle** légitime au sens de [ADR-CKR-002](#adr-ckr-002) : elle habille le mécanisme, elle ne le duplique pas.

**Portée** : cette règle est **spécifique** à la porte Pack ↔ Kits. Elle **n’impose pas** un bi-lexique systématique pour les autres portes (Promotions, Collections, Catégories, Origines — actuellement sans écart lexical front / back-office). Si un cas analogue se présente (ex. une brique back-office nommée techniquement *X* mais dont le libellé commercial *Y* est plus lisible), cette règle sert de **précédent** : on conserve alors la grille technique inchangée, on explicite le libellé front retenu, et on documente la correspondance.

**Libellés front retenus** sur la homepage (section **Explorer**) — **pluriel**, ordre d’affichage :

1. **Promotions** — entrée par avantage commercial ;
2. **Collections** — entrée par sélection éditoriale ;
3. **Kits** — entrée par produits portés par la logique **Pack** (`product_pack` en back-office) ;
4. **Catégories** — entrée par famille de produits ;
5. **Origines** — entrée par repère géographique.

Le **pluriel** est retenu comme forme par défaut pour **harmoniser la lecture** côté visiteur et signaler que chaque porte ouvre sur un **ensemble à explorer** (et non une notion isolée).

Ces libellés **ne recopient pas** mot à mot la doctrine interne ; ils doivent rester **immédiatement compréhensibles** et **cohérents** avec l’univers commercial du site. Chaque carte doit être reliée à une **cible de navigation**, un **comportement boutique** cohérent ([ADR-CKR-007](#adr-ckr-007)), et le cas échéant à une **source de vérité** métier — détail : [WIREFRAME_HOMEPAGE.md](WIREFRAME_HOMEPAGE.md) Bloc 3.

### Conséquences

- Toute nouvelle « porte » marketing doit être **rattachée** à l’une de ces cinq logiques ou justifier une **extension** du modèle (nouvelle ADR ou révision).
- Les implémentations techniques (champs produit, eCommerce categories, listes de prix, pages CMS, etc.) doivent **rester traçables** vers cette doctrine pour éviter la prolifération de modes implicites.
- La distinction **Odoo natif** / **brique OCA installée** vs **construction CK** guide le **prior backlog** : moins d’invention technique là où le standard ou une brique OCA installée suffit (**catégorie**, **promotion**, **pack** via `product_pack`) ; cadrage plus strict pour **collection**, **origine**.
- La **règle de bi-lexique front Kits / back-office Pack** (ci-dessus) doit être **tenue dans la durée** : toute nouvelle copy, toute nouvelle meta, tout nouveau libellé UI concernant cette porte utilise **Kits** côté visiteur ; tout nouveau code, toute nouvelle spec, toute nouvelle requête domaine utilise **Pack** / `pack_ok`. Les revues de code et de contenu doivent le vérifier.

### Références

- [ADR-CKR-007](#adr-ckr-007) — convergence `/shop`.
- [WIREFRAME_HOMEPAGE.md](WIREFRAME_HOMEPAGE.md) — Bloc 3 Explorer.
- [phase_2/SPEC_SHOP_PORTES.md](phase_2/SPEC_SHOP_PORTES.md) — matrice d’implémentation par porte (standard Odoo vs CK vs transitoire).

---

## Historique du registre

| Date | Changement |
|------|------------|
| 2026-04-21 | Création du registre ; **ADR-CKR-001** — doctrine Phase 1 (composition maîtrisée / Odoo 19 CE). |
| 2026-04-21 | **ADR-CKR-002** — spécifique Phase 1 présumé légitime = **front-end** ; le reste = standard Odoo CE et modules activables d’abord. |
| 2026-04-21 | **ADR-CKR-002** — alignement avec **ADR-CKR-001** : ligne **Périmètre** ; précision **présentationnel / éditorial / UX** et exclusion d’une **logique métier parallèle** déguisée côté front. |
| 2026-04-21 | **ADR-CKR-003** — **menu de navigation principal** et **footer** : personnalisation entière requise en Phase 1 (hors perception « standard Odoo »), dans le champ du front-end présentationnel ([ADR-CKR-002](#adr-ckr-002)). |
| 2026-04-21 | **Pré-cadrage [ADR-CKR-004](#adr-ckr-004)** : comparaison de **familles d’options** (*qui vend*, *qui encaisse*, rôle **Nantes**) — **supersédé** le même jour par la **version acceptée** (**achat-revente** dédiée) et la création de **[ADR-CKR-005](#adr-ckr-005)**. |
| 2026-04-21 | **ADR-CKR-004** refondue — **Acceptée** : **achat-revente** ; **C-Kreyol** **vend** au client final, **encaisse**, **achète** à **La Platine**. **ADR-CKR-005** créée — **Acceptée** : **hub léger Nantes**, **flux tendu**, **stock consigné** ; règle **métier d’abord** puis **Odoo simple** ; détail consignation / propriété **à affiner**. |
| 2026-04-21 | **[STRUCTURE_MENU_PRINCIPAL.md](STRUCTURE_MENU_PRINCIPAL.md)** : cadrage menu principal Phase 1 ; référence ajoutée sous **ADR-CKR-003**. |
| 2026-04-21 | **[WIREFRAME_HOMEPAGE.md](WIREFRAME_HOMEPAGE.md)** : filaire homepage Phase 1 ; référence ajoutée sous **ADR-CKR-003**. |
| 2026-04-21 | **Phase 2 — doctrine navigation produit** : **[ADR-CKR-006](#adr-ckr-006)** (homepage = orientation structurée ; header vs Explorer), **[ADR-CKR-007](#adr-ckr-007)** (`/shop` = convergence commerciale unique), **[ADR-CKR-008](#adr-ckr-008)** (cinq portes d’exploration ; Odoo vs CK). Références transverses : [WIREFRAME_HOMEPAGE.md](WIREFRAME_HOMEPAGE.md), [STRUCTURE_MENU_PRINCIPAL.md](STRUCTURE_MENU_PRINCIPAL.md) §11. |
| 2026-04-21 | **ADR-008** : libellés **front** Explorer — **Promotion**, **Collection**, **Kit**, **Catégorie**, **Origine** (singulier ; **Kit** traduit la logique **composition**) ; ordre d’affichage et exigences cible / boutique. |
| 2026-04-21 | **ADR-008** — libellés Explorer passés au **pluriel** pour harmoniser la lecture visiteur : **Promotions**, **Collections**, **Kits**, **Catégories**, **Origines** (ordre inchangé ; stub **`/kits`** remplace **`/kit`**). |
| 2026-04-21 | Références **ADR-007 / 008** : [phase_2/SPEC_SHOP_PORTES.md](phase_2/SPEC_SHOP_PORTES.md) (spécification d’implémentation portes → `/shop`, hors surcharge du corps des ADR). |
| 2026-04-21 | **ADR-008** — recadrage **porte 5** : l’ancienne logique « composition » est **retirée** du vocabulaire Explorer au profit de **Pack** (front **et** doctrine). Justification : vérification back-office Odoo (case *« Est un pack ? »*, onglet *Pack*) confirmant que la bonne brique de référence est la logique **pack** portée par le module OCA **`product_pack`** (installé sur `tenant_o7`). Conséquences : libellé front **Packs** ; rapport au standard repositionné (porte « adossée à brique OCA installée ») ; construction CK limitée à la couche navigation / présentation ; URL stub **`/packs`** remplace **`/kits`**. |
| 2026-04-21 | **ADR-008** — introduction d’une **règle de bi-lexique front / back-office** : la grille **back-office / source de vérité / implémentation** reste **Pack** (module OCA `product_pack`, `pack_ok`) ; la grille **front / visiteur** adopte **Kits** (univers alimentaire : *kit colombo*, *kit apéritif*, *kit découverte*). Conséquences : libellés Explorer repassent à **Kits** côté carte + intro ; URL visible remise à **`/kits`** ; SPEC / CONTRAT_URL / paramètres CK internes restent en **Pack** (`ckr_mode=pack`, domaine `pack_ok=True`). Règle spécifique à cette porte, réutilisable comme précédent si un cas analogue se présente. |
| 2026-04-21 | **ADR-007** — confirmation **ferme et universelle** de la règle de convergence pour les cinq portes Explorer : **aucune exception** à la cible `/shop`. Ajout d’une section **« Statut des pages dédiées actuelles »** qui qualifie explicitement `/collections`, `/kits`, `/origines` (et équivalents) comme **états transitoires** — issue finale : disparition, redirection ou façade stricte `/shop`. Rafraîchissement du vocabulaire (porte 5 : *Pack* doctrine interne / *Kits* libellé visiteur) en cohérence avec [ADR-CKR-008](#adr-ckr-008). |
| 2026-04-21 | **Contrat d’URL porte Pack (libellé visiteur Kits) — acté** : **Hybride H1** retenu (détails : [phase_2/CONTRAT_URL_PACKS.md §12](phase_2/CONTRAT_URL_PACKS.md)). URL visiteur **`/kits`** (redirection 301) ↔ URL technique canonique **`/shop?ckr_mode=pack`** ; paramètre CK **`ckr_mode=pack`** (whitelist `{"pack"}`) ; filtre domaine `("pack_ok", "=", True)` ; titre visiteur « Kits » rendu par CK. Première application concrète des ADR-001 (source de vérité native `pack_ok`), ADR-007 (canonical = forme native `/shop`), ADR-008 (bi-lexique : URL visible grille Kits / URL technique grille Pack). SPEC §4.3 alignée. |
| 2026-04-21 | **ADR-CKR-008 / Porte Kits — implémentation déployée** (version module **19.0.1.1.0**). Livré : (1) dépendance `product_pack` ajoutée au manifest ; (2) contrôleur `WebsiteSaleCKR` héritant `WebsiteSale` — hooks `_get_search_options` (injection option `ckr_pack_only`), `_get_shop_domain` (cohérence calcul min/max prix), `_shop_get_query_url_kwargs` (préservation du paramètre lors des filtres / pagination), `_get_additional_shop_values` (variables QWeb `ckr_pack_mode` / `ckr_pack_title`) ; (3) contrôleur alias `WebsiteSaleCKRKitsAlias` → `/kits` en **redirection HTTP 301** vers `/shop?ckr_mode=pack` avec préservation des query params entrants ; (4) extension `product.template._search_get_detail` qui ajoute `[('pack_ok', '=', True)]` au `base_domain` quand l’option est active ; (5) extension `website._get_canonical_url` qui rétablit le paramètre `ckr_mode=pack` dans le canonical — exception doctrinale **strictement limitée** au couple (path=`/shop`, `ckr_mode=pack`), toutes les autres URL conservent le comportement natif ; (6) bandeau visiteur **« Kits »** injecté par xpath sur `website_sale.products` (template `ckr_shop_pack_banner`, conditionné à `ckr_pack_mode`) + styles SCSS dédiés ; (7) retrait ordonné du stub : `website_page` `/kits` et template `ckr_page_compositions` supprimés du data set, fichier `views/pages/ckr_compositions.xml` retiré du module, nettoyage des installations existantes via `data/ckr_cleanup_kits_stub.xml` (`<delete>` par recherche sur `url`). Tests fonctionnels OK sur instance `tenant_o7` : `/kits` → 301, préservation `?search=…&order=…`, `/shop?ckr_mode=pack` → 200 avec filtre `pack_ok` appliqué (2 produits publiés → 1 pack retenu), bandeau rendu, canonical pointant bien sur `/shop?ckr_mode=pack`. Contrat Hybride H1 pleinement opérationnel — critères de succès §12 de [CONTRAT_URL_PACKS.md](phase_2/CONTRAT_URL_PACKS.md) validés. |
| 2026-04-21 | **Contrat d’URL porte Promotions — acté** : **Hybride H1** retenu par transposition du patron Pack (détails : [phase_2/CONTRAT_URL_PROMOTIONS.md §12](phase_2/CONTRAT_URL_PROMOTIONS.md)). URL visiteur **`/promotions`** (redirection 301) ↔ URL technique canonique **`/shop?ckr_mode=promo`** ; paramètre CK **`ckr_mode=promo`** (whitelist étendue à `{"pack", "promo"}`) ; **source de vérité A2** = `product.pricelist.item` actif strictement réducteur sur la pricelist courante du visiteur (alignement strict « affiché comme promo ⇔ réduit à la caisse ») ; hook **A3** (`loyalty.program` type `promotion`) **ouvert comme extension future** mais **hors périmètre** de la vague courante ; **état vide dédié** validé (« Aucune offre en cours pour le moment ») ; **pré-requis ops non bloquant** acté : alimentation back-office d’au moins une pricelist datée avec remise. Doctrine confirmée : **standard Odoo d’abord** ([ADR-CKR-001](#adr-ckr-001)) — aucune seconde définition « promo » parallèle côté CK. |
| 2026-04-21 | **ADR-CKR-008 / Porte Promotions — implémentation déployée** (version module **19.0.1.2.0**). Livré : (1) `controllers/website_sale_ckr.py` **refactoré multi-modes** — constantes `CKR_MODE_PROMO`, `CKR_MODES_ALLOWED = {"pack", "promo"}`, `CKR_MODE_TITLES`, `CKR_ALIAS_MODE` ; whitelist stricte `_ckr_current_mode` ; dispatch par mode dans `_get_search_options` (`ckr_pack_only` vs `ckr_promo_only`), `_get_shop_domain` (domaine `pack_ok=True` vs domaine promo résolu), `_get_additional_shop_values` (variables QWeb `ckr_pack_mode` / `ckr_promo_mode` / titres / drapeau `ckr_promo_empty`) ; `WebsiteSaleCKRAliases` regroupe `/kits` **et** `/promotions` via helper partagé `_ckr_redirect` (301, préservation des query params, chemin cible paramétré par `ckr_mode`) ; (2) nouveau `models/product_pricelist.py` — **résolveur A2** `_ckr_get_promo_template_ids(website, pricelist)` : chaîne de résolution de la pricelist courante (paramètre explicite → `website._get_and_cache_current_pricelist()` → fallback `partner.property_product_pricelist` pour les contextes non-HTTP et les instances mono-pricelist), domaine actif via `_ckr_active_items_domain` (bornes `date_start` / `date_end` ouvertes ou englobantes à l’instant *t*), filtre strict réducteur via `_ckr_item_is_reducer` (rejet items neutres / mark-ups pour `percentage` / `formula` ; comparaison à `list_price` pour `fixed` sur `0_product_variant` / `1_product` ; inclusion prudente pour `2_product_category` / `3_global`), résolution `applied_on` → `product.template.id`s (variant, produit, catégorie via `child_of`), **sentinels** : `None` = cas « 3_global » (pas de filtre produit supplémentaire, toute la boutique est légitimement « en promo ») / `set()` = état vide (force `('id', '=', 0)` côté `_search_get_detail` pour garantir liste vide + bandeau empty) / `set` non vide = ids concernés ; (3) `product.template._search_get_detail` étendu à `ckr_promo_only` — délègue au résolveur A2, traduit le sentinel en domaine approprié (aucun filtre ajouté si `None`, `('id', '=', 0)` si `set()`, `('id', 'in', [...])` sinon) ; (4) `website._get_canonical_url` **généralisé** à tout `ckr_mode ∈ CKR_MODES_ALLOWED` sur path `/shop` (exception doctrinale unique déjà ouverte pour Pack, étendue symétriquement à Promo) ; (5) bandeau visiteur **« Promotions »** — template `ckr_shop_promo_banner` héritant `website_sale.products` (priorité 32, xpath avant la liste produits), classe variante `ckr-shop-promo-banner--empty` et copy dédiée quand `ckr_promo_empty`, styles SCSS `.ckr-shop-promo-banner` + `&--empty` ; (6) carte Explorer Promotions — `views/snippets/ckr_entries.xml` : `href` basculé de `/shop` à `/promotions` (aucun stub CMS préexistant à retirer) ; (7) `models/__init__.py` met à jour pour importer `product_pricelist` ; manifest bumpé à **19.0.1.2.0** (description étendue). **Pré-requis ops** : groupe `product.group_product_pricelist` activé sur `tenant_o7` (confirmé indispensable à l’activation effective des pricelists e-commerce). **Tests E2E validés** sur `tenant_o7` : redirection 301 `/promotions` → `/shop?ckr_mode=promo` (paramètres `search` / `order` / `page` préservés) ; non-régression `/kits` 301 et `/shop` 200 nu ; `/shop?ckr_mode=promo` 200 avec bandeau rendu, état vide affiché si pas de promo active ; path chargé avec `product.pricelist` + `product.pricelist.item` temporaires → bandeau non-empty + produit promu listé + produits non-promus filtrés ; canonical correct dans les trois modes (`/shop`, `/shop?ckr_mode=pack`, `/shop?ckr_mode=promo`) ; non-régression croisée entre modes ; résolveur unitaire testé pour les trois sentinels. Contrat Hybride H1 pleinement opérationnel — critères de succès §12 de [CONTRAT_URL_PROMOTIONS.md](phase_2/CONTRAT_URL_PROMOTIONS.md) validés. **Le patron technique Hybride H1 est désormais éprouvé deux fois** (Pack, Promo) et généralisé : [phase_2/CONTRAT_URL_PROMOTIONS.md §13.6](phase_2/CONTRAT_URL_PROMOTIONS.md) formalise la check-list de réutilisation pour les trois portes restantes (Catégories, Origines, Collections). Hook A3 (loyalty promotion) documenté comme extension future, hors livraison. |
| 2026-04-22 | **Contrat d’URL porte Catégories — acté** : **Hybride H1 — cible native** ([phase_2/CONTRAT_URL_CATEGORIES.md §12](phase_2/CONTRAT_URL_CATEGORIES.md)). URL visiteur **`/categories`** (redirection **301**) ↔ URL technique canonique **`/shop/category/<id>-<slug>`** (standard `website_sale`) ; **pas** d’extension de la whitelist `ckr_mode` ; filtrage et fil d’Ariane **100 % natifs**. Résolution de la catégorie d’entrée : paramètre système **`dorevia_ckreyol_marketplace.explorer_public_category_id`** puis première **racine** `product.public.category` du site ; repli **301** vers **`/shop`** nu si aucune catégorie publique. Doctrine [ADR-CKR-001](#adr-ckr-001) / [ADR-CKR-007](#adr-ckr-007) respectée sans dupliquer le domaine catégorie côté CK. |
| 2026-04-22 | **ADR-CKR-008 / Porte Catégories — implémentation déployée** (version module **19.0.1.3.0**). Livré : (1) `models/product_public_category.py` — `_ckr_get_explorer_entry_shop_path(website)`, helpers `_ckr_category_valid_for_website` et `_ckr_explorer_root_domain` ; (2) `controllers/website_sale_ckr.py` — route `ckr_categories_alias` (`/categories` → 301 ; préservation des query params **hors** `ckr_mode`) ; (3) `data/ckr_explorer_category_parameter.xml` ; (4) `views/snippets/ckr_entries.xml` — `href` **Catégories** → `/categories` ; (5) `models/__init__.py` ; manifest **19.0.1.3.0** ; SPEC / README / CONTRAT synchronisés ; §13.6 de [CONTRAT_URL_PROMOTIONS.md](phase_2/CONTRAT_URL_PROMOTIONS.md) complété par la **variante H1 cible native**. |
| 2026-04-22 | **MOA — orientation portes Explorer (post-vague A)** : **Collections** — **gel explicite** (pas de lancement de chantier spec/impl à ce stade ; objet métier/éditorial CK ; document dédié ultérieur : backend, contrat d’URL, sélection produit, projection front). **Origines** — **priorité actuelle** ; **décision de fond** : traitement avec **dimension éditoriale** (porte de navigation avec portée de lecture / mise en scène visiteur ; **exclut** la réduction à un simple tag ou métadonnée sans signification sur le site). Documentation alignée : [phase_2/SPEC_SHOP_PORTES.md](phase_2/SPEC_SHOP_PORTES.md) (§3, §4.2, §4.5, snapshot, checklist), [README.md](../README.md) (statut dépôt). |
| 2026-04-22 | **Porte Origines — livrable de cadrage** : création de [phase_2/CONTRAT_URL_ORIGINES.md](phase_2/CONTRAT_URL_ORIGINES.md) (statut **cadrage initial**, arbitrages §12 ouverts). Contenu : obligations **signal éditorial minimal** (titres + ligne de contexte + cohérence portes A + état vide), interdiction du **filtre silencieux** ; options source de vérité (attribut, champs, tags, pays, modèle CK) ; options URL (H1, `attrib`, hub CMS) ; multi-valeurs, SEO/canonical, non-régression `pack`/`promo`. Précision MOA reprise dans [SPEC_SHOP_PORTES §4.5](phase_2/SPEC_SHOP_PORTES.md#45-origines). |
| 2026-04-22 | **CONTRAT_URL_ORIGINES — validation du cadre MOA** : le document est **reçu** comme **base d’atelier** ; trajectoire atelier → **§12.1** (cinq arbitrages minimum : source de vérité, véhicule d’URL, niveau de signal éditorial, multi-valeurs, référence invalide / états vides) → implémentation. §12 restructuré (12.1 / 12.2). [SPEC_SHOP_PORTES §6](phase_2/SPEC_SHOP_PORTES.md) checklist Origines alignée. |
| 2026-04-22 | **CONTRAT_URL_ORIGINES — position MOA source de vérité (pré-atelier)** : [§4.0](phase_2/CONTRAT_URL_ORIGINES.md) *socle produit structuré sobre + projection éditoriale CK* ; première analyse **A1 attribut** + CK ; **A2** si standard trop limitant ; **A3 tag libre** évité par défaut comme source finale ; **A5 modèle dédié** seulement si besoin démontré. [§12.3](phase_2/CONTRAT_URL_ORIGINES.md) : cinq questions (cardinalité, suffisance attribut, métadonnées par origine, seuil bascule A5, cohérence sans duplication). |
| 2026-04-22 | **CONTRAT_URL_ORIGINES — confirmation MOA (séquence atelier)** : point de départ **§4.0 + §12.1 + §12.3** **reçu** ; pas de préemption du PV ; trajectoire **atelier → verrouillage PV → implémentation** actée (paragraphe ajouté en tête de [§4.0](phase_2/CONTRAT_URL_ORIGINES.md)). |
| 2026-04-22 | **CONTRAT_URL_ORIGINES — verrouillage MOA §13** : doctrine *porte éditoriale → `/shop` + donnée structurée multi + signal visible* ; **multi-valeurs** produit + filtre **OU** ; exclusions tag/texte faible/A5 lourd v1 ; **§3.1** (nom, phrase, slug, ordre, visibilité) ; image/contenu riche hors v1 ; **fiche produit** ; pas hub obligatoire ; repli **`/shop`** propre si invalide ; **état vide dédié** + rebond. [§12](phase_2/CONTRAT_URL_ORIGINES.md) = résidu technique ; [SPEC_SHOP_PORTES](phase_2/SPEC_SHOP_PORTES.md) aligné. |
| 2026-04-22 | **CONTRAT_URL_ORIGINES — confirmation réception verrouillage** : **§13** = **référence métier stable** actée par la MOA ; enchaînement **PV / spec d’impl.** sur **§12** (notamment **§12.2**) puis développement ; **gel de §13** hors nouvelle décision MOA **écrite** (paragraphe en tête de [§13](phase_2/CONTRAT_URL_ORIGINES.md)). |
| 2026-04-22 | **Spec d’implémentation Origines** : création de [phase_2/SPEC_IMPL_ORIGINES.md](phase_2/SPEC_IMPL_ORIGINES.md) (brouillon technique v1 : A1 + modèle léger `ckr.shop.origin`, `ckr_mode=origin` / `ckr_origin`, hooks `WebsiteSale`, `_search_get_detail`, bandeau, fiche produit, repli invalide, tests E2E, §10 ouvert). Référence ajoutée depuis [CONTRAT §12](phase_2/CONTRAT_URL_ORIGINES.md) et [SPEC_SHOP_PORTES §7](phase_2/SPEC_SHOP_PORTES.md). |
