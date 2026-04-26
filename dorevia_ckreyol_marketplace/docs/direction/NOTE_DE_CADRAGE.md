# C-Kreyol — Note de cadrage Phase 1

## 1. Objet du document

Cette note de cadrage a pour objet de transformer l’intention posée dans le README du projet **C-Kreyol** en un cadre de travail opérationnel pour la **Phase 1**.

Elle vise à :

- préciser le **but concret** de la phase de lancement ;
- cadrer le **modèle opératoire initial** ;
- distinguer ce qui est **indispensable**, **souhaitable** ou **hors périmètre** ;
- identifier les **arbitrages à rendre** avant mise en ligne ;
- fournir une base commune de pilotage pour les choix métier, techniques, logistiques et juridiques.

Cette note ne constitue ni un business plan détaillé, ni une consultation juridique exhaustive. Elle a vocation à servir de **document de référence de cadrage** pour le lancement de la première version exploitable du canal.

Le **socle technique cible** pour concrétiser la Phase 1 est **Odoo 19 Community Edition** : le présent cadrage est rédigé **en vue de son implémentation** (paramétrage, modules, flux e-commerce, stock et logistique selon le modèle retenu). Il complète le [README](../../README.md) du dépôt projet, le [cadrage design / front-end](DESIGN.md), la [structure cible du menu principal](STRUCTURE_MENU_PRINCIPAL.md), le [wireframe homepage](WIREFRAME_HOMEPAGE.md), la [spec hero homepage](SPEC_HERO_HOMEPAGE.md), le [brief visuel hero Phase 1](BRIEF_VISUEL_HERO_PHASE1.md), la [charte graphique minimale Phase 1](CHARTE_GRAPHIQUE_PHASE1.md), le [brief synthétique direction artistique Phase 1](BRIEF_SYNTHETIQUE_CK.md) et les [directions artistiques Phase 1](DIRECTIONS_ARTISTIQUES_PHASE1.md).

Les **décisions d’architecture** structurantes sont consignées dans le [registre ADR](ARCHITECTURE_DECISION_RECORD.md) (à ce jour : **ADR-CKR-001** — doctrine de construction Phase 1, §3.5 ; **ADR-CKR-002** — spécifique Phase 1 présumé légitime = **front-end** uniquement ; **ADR-CKR-003** — **menu principal** et **footer** entièrement personnalisés en Phase 1 ; **ADR-CKR-004** — **modèle commercial Phase 1** : **achat-revente** (**C-Kreyol** vend au client final, **encaisse**, **achète** à **La Platine**) ; **ADR-CKR-005** — **modèle logistique cible** : **hub léger à Nantes**, **flux tendu**, **stock consigné** — avec **points ouverts** de consignation / propriété / Odoo à affiner, cf. §5.4).

---

## 2. Contexte

**C-Kreyol** est un **canal e-commerce spécialisé** porté comme une **marque** et un **actif commercial propre**.

**Localisation** : le projet **C-Kreyol** est **localisé à Nantes** (France) — ancrage opérationnel du canal (à distinguer de l’**origine géographique** des produits agro transformés antillais). La **forme juridique**, l’adresse de siège et leur traduction dans les mentions légales / facturation seront figées en Phase 1.

**C-Kreyol est opéré depuis Nantes**, avec vocation à mettre en marché des produits agro transformés antillais en s’appuyant non seulement sur une **marque** et un **canal digital**, mais aussi sur une **montée en compétence réelle** en **logistique import-export** : capacité à **organiser**, **comprendre** et **fiabiliser** des flux entre territoires. Ce double ancrage — **métropole** pour l’opération, **Antilles** pour l’offre — structure la lecture du projet : C-Kreyol n’est pas seulement « un site sur les Antilles », mais un **canal opéré depuis un point commercial en métropole**, porteur d’une **promesse de compétence** qui dépasse la simple vitrine.

Le projet vise la commercialisation en ligne de **produits agro transformés antillais**, avec une exigence de sérieux sur :

- la lisibilité de l’offre ;
- la qualité perçue ;
- la confiance dans l’achat ;
- la tenue des promesses de service.

Le projet ne part pas d’un terrain abstrait : **La Platine** constitue le **premier fournisseur** de **C-Kreyol** et son **premier point d’appui commercial**. Pour autant, **C-Kreyol n’a pas vocation à se confondre avec La Platine** ni à n’être que l’extension de son activité.

L’hypothèse structurante actuellement privilégiée est la suivante : **C-Kreyol pourrait fonctionner sans stock centralisé systématique**, en s’appuyant sur un ou plusieurs **fournisseurs partenaires** pour tout ou partie de la préparation ou de l’expédition, tandis que **C-Kreyol** porterait la **marque**, le **canal de vente**, l’**expérience client** et l’**orchestration commerciale**.

Cette lecture est **affûtée** par l’**orientation cible** **hub léger à Nantes**, **flux tendu** et **stock consigné** (§4.4, §5.4, [ADR-CKR-005](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005)), avec **modèle commercial** **achat-revente** ([ADR-CKR-004](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-004)) — sous réserve des **validations** et du **détail** opérationnel / juridique.

À ce stade, les **mécanismes fins** (transfert de propriété, risques, Odoo) restent à **documenter** sans remettre en cause la **direction** retenue tant qu’une décision contraire n’est pas actée.

---

## 3. Vision rappelée et objectif de la Phase 1

### 3.1 Vision rappelée

À moyen terme, **C-Kreyol** a vocation à devenir une **marque identifiable** et un **canal de vente crédible** pour les produits agro transformés antillais, avec :

- une offre lisible ;
- une origine assumée ;
- une expérience d’achat sérieuse ;
- des promesses logistiques tenues ;
- une capacité d’élargissement progressive à d’autres fournisseurs ou gammes.

### 3.2 Vision à horizon 3 ans (composante logistique)

À horizon **3 ans**, **C-Kreyol** vise à être non seulement une **marque** et un **canal e-commerce crédibles**, mais aussi un acteur capable d’apporter une **orchestration logistique import-export sérieuse** au service de la mise en marché de produits agro transformés antillais — en cohérence avec l’**ancrage opérationnel à Nantes** (cf. §4.4) et avec le niveau de **rôle logistique** effectivement retenu (pur canal, hub léger, ou montée en puissance).

### 3.3 Objectif de la Phase 1

L’objectif de la **Phase 1** n’est pas de construire une marketplace multi-vendeurs complète, ni un système parfait.

L’objectif est d’ouvrir un **premier canal de vente réellement opérable**, permettant de :

- publier un **catalogue initial réel** ;
- accepter une **commande réelle** ;
- l’encaisser ;
- l’exécuter correctement ;
- valider un **premier flux bout en bout** ;
- disposer d’une base exploitable pour itération.

### 3.4 Succès observable de la Phase 1

La Phase 1 sera considérée comme utile si, à son terme :

- une première offre sérieuse est en ligne ;
- la chaîne commande → paiement → préparation → livraison / retrait fonctionne ;
- les responsabilités opérationnelles sont claires ;
- les pages et informations minimales obligatoires sont publiées ;
- le canal peut servir de base réelle de croissance.

### 3.5 Doctrine de construction de la Phase 1

La Phase 1 ne part pas d’une logique de création *ex nihilo*, mais d’une logique de **composition maîtrisée**.

Le socle **Odoo 19 Community Edition** est considéré comme **fonctionnellement riche** via ses modules activables. La limite principale du projet n’est donc pas l’absence totale de couverture, mais la capacité à **produire une solution harmonieuse**, lisible et opérable en puisant dans les couvertures fonctionnelles effectivement disponibles.

En conséquence, la Phase 1 vise en priorité à :

- tirer parti du **socle standard Odoo CE** et de ses activations pertinentes ;
- éviter la surconstruction ou le développement prématuré ;
- rechercher la **cohérence d’ensemble** entre catalogue, commande, paiement, livraison, information client et exécution ;
- n’ajouter du spécifique que lorsque le standard ou la composition des modules activables ne suffit pas à soutenir correctement le modèle retenu.

**Périmètre du spécifique en Phase 1** : le seul spécifique **présumé légitime** sans dossier d’exception préalable est le **front-end** (thème, assets, habillage du site, héritages de vues *website* à visée **présentationnelle**). **Tout le reste** doit **d’abord** trouver sa solution dans le **standard Odoo CE** et les **modules activables** ; tout écart reste **exceptionnel** et doit être **justifié** (voir [ADR-CKR-002](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-002)).

**Navigation et pied de page** : le **menu de navigation principal** et le **footer** font partie des éléments **obligatoirement personnalisés** en Phase 1 pour éviter une perception « standard Odoo » du canal, tout en restant dans le champ **présentationnel** défini par l’ADR-CKR-002 (voir [ADR-CKR-003](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-003)).

L’objectif n’est pas de démontrer une sophistication maximale, mais de construire un **premier canal harmonieux**, crédible et réellement exploitable.

**Décisions d’architecture** : **ADR-CKR-001** (composition maîtrisée), **ADR-CKR-002** (spécifique = front-end par défaut en Phase 1) et **ADR-CKR-003** (menu principal + footer entièrement personnalisés) dans le [registre ADR](ARCHITECTURE_DECISION_RECORD.md) — statuts **acceptés** pour la Phase 1. **ADR-CKR-004** (**achat-revente** : **C-Kreyol** vend et encaisse, achète à **La Platine**) et **ADR-CKR-005** (**hub léger Nantes**, **flux tendu**, **stock consigné**) y figurent également comme décisions **acceptées**, sous réserve des **affûtages** juridiques et opérationnels détaillés en **§5.4**.

---

## 4. Positionnement et modèle opératoire visé

## 4.1 Positionnement

**C-Kreyol** est conçu comme :

- une **marque** ;
- un **canal retail digital spécialisé** ;
- un **opérateur de commercialisation** ;
- un vecteur de **mise en marché en ligne** pour des produits agro transformés antillais.

**C-Kreyol** a également vocation, **à terme**, à jouer un rôle d’**intermédiaire B2B** pour la mise en marché de produits agro transformés antillais, **sans** que cette composante soit nécessairement **pleinement activée** dès la Phase 1 (arbitrages §5, §6, §14).

**C-Kreyol** n’est pas seulement un **canal de vente en ligne** : il a aussi vocation à développer une **capacité d’orchestration logistique et commerciale** entre les **Antilles** et les **marchés cibles**, avec un **ancrage opérationnel à Nantes** (cf. §2 et §4.4). La promesse ne se limite pas à la marque et au digital : elle inclut la **fiabilité des flux** et, à terme, une **compétence import-export** assumée au niveau attendu par le positionnement.

Le projet ne doit pas être compris comme :

- le simple site vitrine de **La Platine** ;
- une marketplace multi-vendeurs pleinement constituée dès le départ ;
- un acteur obligé d’acheter, stocker et expédier systématiquement toute l’offre en propre.

## 4.2 Hypothèse opératoire privilégiée

L’hypothèse actuelle est celle d’un fonctionnement **sans stock centralisé systématique**, avec une répartition possible des rôles entre **C-Kreyol** et ses **fournisseurs partenaires**.

Dans cette hypothèse :

- **C-Kreyol** porte la **marque**, le **site**, la **présentation de l’offre**, l’**expérience client**, le **canal commercial** et une partie de l’**orchestration** ;
- le ou les **fournisseurs** peuvent porter tout ou partie de la **préparation**, du **stock** ou de l’**expédition**, selon les accords retenus.

L’**hypothèse de travail préférée** décrite en **§4.4** et dans les **[ADR-CKR-004](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-004) / [ADR-CKR-005](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005)** **affine** la formulation « **sans** stock centralisé **systématique** » : il ne s’agit **pas** d’un **stock lourd classique** acheté en masse et **immobilisé**, mais d’une visée de **rotation** avec **point d’appui physique** à **Nantes** et **logique de consignation** à **cadrer juridiquement** (événements de transfert, risques, suivi — cf. **§5.4**).

Cette hypothèse doit être confrontée aux contraintes :

- juridiques ;
- fiscales ;
- comptables ;
- logistiques ;
- de qualité de service ;
- de responsabilité vis-à-vis du client final.

## 4.3 Point d’appui initial

Au démarrage, **La Platine** constitue :

- le **premier fournisseur** de **C-Kreyol** ;
- la première source de produits ;
- un premier ancrage réel ;
- un premier point d’appui pour crédibiliser le lancement.

## 4.4 Ancrage opérationnel à Nantes et rôle logistique visé

**Nantes** n’est pas seulement une mention d’adresse : elle conditionne la **lecture stratégique** du projet (siège / opérateur en métropole, offre antillaise, flux internationaux ou inter-territoires). Il convient de trancher **quel rôle logistique** C-Kreyol entend réellement porter — au départ et à **horizon 3 ans** — parmi au moins **trois familles de modèle** :

1. **Pur canal commercial** — pas de passage physique systématique des marchandises par Nantes ; orchestration contractuelle, information, relation client ; exécution physique surtout **côté fournisseurs** ou tiers logistiques.
2. **Hub léger** — **certains flux** sont **regroupés**, **contrôlés** ou **redistribués** depuis Nantes (réception partielle, consolidation ponctuelle, point de contrôle qualité, etc.) sans entrepôt complet jour 1.
3. **Montée en puissance logistique** — Nantes devient un **vrai point d’appui** (stock, redistribution, préparation) au fil du temps, en cohérence avec la vision **import-export** et les capacités internes à bâtir.

**Hypothèse de travail préférée pour la Phase 1** (à consolider avec le **juridique** / **fiscal** et l’**opérationnel**) : viser un **hub logistique léger à Nantes**, en **flux tendu**, avec **stock consigné** comme logistique privilégiée — ce n’est **ni** un pur **dropshipping**, **ni** une simple **vitrine**, **ni** un **stock lourd** classique, mais une logique de **hub commercial et logistique léger** (cf. [ADR-CKR-005](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005)). Le **modèle commercial** associé (**achat-revente**, **C-Kreyol** vend et encaisse, achats auprès de **La Platine**) est posé en [ADR-CKR-004](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-004).

**Questions structurantes** (à traiter avec §5 et §8) :

- Nantes est-il **uniquement** le siège / l’opérateur **commercial** et administratif, ou aussi un **point de passage logistique** ?
- **Stock local** à Nantes ou non ? **Réception / regroupement / redistribution** depuis Nantes ou pas ?
- La **compétence import-export** est-elle portée **par C-Kreyol**, par **un partenaire**, ou **partagée** — et à quel niveau de preuve pour le client (transparence, responsabilité) ?
- Schémas de flux possibles : **Antilles → Nantes → client final** ; **Antilles → client final** (direct) ; **hybride** selon produits ?
- Quelle **valeur ajoutée logistique** C-Kreyol veut-il afficher **par rapport à un simple site vitrine** ou à une expédition « tout fournisseur » sans orchestration ?

Ces arbitrages sont **structurants** pour le modèle économique, les **flux Odoo** (stock, entrepôts, livraisons), les **CGV** et la **communication** sur le site.

## 4.5 Benchmark d’inspiration — Caribshopper

**Caribshopper** constitue un **benchmark d’inspiration** important pour **C-Kreyol**, non seulement comme site de vente de produits caribéens, mais surtout comme exemple de **logique retail digital**.

Le site illustre plusieurs éléments structurants :

- des **entrées de navigation commerciales et éditoriales** (ex. *Bestsellers*, *New Arrivals*, *Recipes*, *Reviews*) ;
- des portes d’entrée par **origine / territoire** (ex. *Jamaica*, *Trinidad*, *Guyana*) ;
- des **collections thématiques** (ex. *Spice it Up!*, *Coffee Lovers*, *Chocoholics*, *Sweetness*) ;
- une logique **cadeau** structurée (*Gift Guide*, *Gift Boxes*, cadeaux par profil et par prix) ;
- un renvoi explicite vers un **site wholesale (B2B)** distinct du parcours grand public.

### Lecture pour C-Kreyol

Ce benchmark suggère que **C-Kreyol** ne doit pas être pensé comme un simple catalogue exposé en ligne, mais comme un **dispositif retail digital** :

- mise en scène de l’offre ;
- navigation par **usages**, **occasions** et **collections** ;
- rôle fort du **front-end** dans la perception de marque (en cohérence avec les [ADR du registre](ARCHITECTURE_DECISION_RECORD.md) sur le spécifique front-end et la navigation) ;
- possibilité, **à terme**, de distinguer plus clairement une face **retail B2C** et une face **intermédiation B2B** — sans préjuger des arbitrages juridiques et opératoires à traiter en §5 et §6.

### Conséquence stratégique pour la Phase 1

En **Phase 1**, **C-Kreyol** n’a **pas** besoin de reproduire la **largeur** du catalogue de Caribshopper. En revanche, il peut s’inspirer fortement de sa **logique** :

- **entrées commerciales** claires et hiérarchisées ;
- **collections éditorialisées** (même modestes au départ) ;
- **front-end** et **navigation** fortement travaillés dans le respect des ADR ;
- visée **qualité retail** du canal (crédibilité, lisibilité, envie d’explorer l’offre).

---

## 5. Modèle commercial et juridique à arbitrer

Cette section a pour objet d’identifier le modèle de relation à retenir entre **C-Kreyol**, **La Platine** et le **client final**.

## 5.1 Questions structurantes

Les points suivants doivent être tranchés :

- Qui **vend juridiquement** au client final ?
- Qui **encaisse** le paiement ?
- Qui **facture** ?
- Qui **porte le stock** ?
- Qui **prépare** la commande ?
- Qui **expédie** ?
- Qui gère le **SAV**, les **retours** et les **litiges** ?
- Qui porte la responsabilité en cas de :
  - retard ;
  - casse ;
  - non-conformité ;
  - rupture ;
  - défaut de qualité produit ?

**Ancrage Nantes et chaîne physique** (lien §4.4) :

- quel **rôle** pour Nantes dans la chaîne (siège seul, hub, stock) ?
- flux **Antilles → Nantes → client** vs **Antilles → client** (ou mix) ?
- **qui** porte la compétence **import-export** opérationnelle et **vis-à-vis des autorités / transporteurs** ?
- **stock** local à Nantes ou non ; **réception / regroupement / redistribution** depuis Nantes ou pas ;
- **valeur ajoutée logistique** de C-Kreyol vs vitrine seule ou expédition 100 % fournisseur.

## 5.2 Modèles envisageables

Options à étudier :

- **achat-revente** ;
- **dépôt** ;
- **commission / intermédiation** ;
- **mandat** ;
- **modèle hybride** selon familles de produits.

## 5.3 Impacts à documenter

Le choix du modèle a des impacts sur :

- les **CGV** ;
- la **TVA** ;
- la **facturation** ;
- la **comptabilité** ;
- la **gestion de stock** ;
- les **flux Odoo** ;
- l’identité du **vendeur affiché** ;
- la responsabilité client.

## 5.4 Décision attendue

Décision cible pour la Phase 1 :  
**C-Kreyol achète les produits à La Platine, les revend au client final, encaisse les paiements, et vise un modèle de hub léger à Nantes en flux tendu, avec stock consigné comme hypothèse logistique privilégiée.**

Justification :  
Ce modèle permet de construire **C-Kreyol** comme un **actif commercial autonome**, tout en limitant l’**immobilisation de trésorerie** (pas de stock lourd classique visé en Phase 1), en donnant à **Nantes** un **rôle logistique réel**, et en préparant une **montée en puissance progressive** du canal (y compris **B2B** à terme, cf. §4.1).

### Points encore à cadrer (sans bloquer l’ouverture sur une perfection jour 1)

**Déjà posé dans les ADR** : **C-Kreyol** **vend** au client final et **encaisse** ; **achat-revente** auprès de **La Platine** ([ADR-CKR-004](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-004)) ; **hub léger Nantes**, **flux tendu**, **stock consigné** ([ADR-CKR-005](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005)).

**À définir précisément** (avec **conseils experts**) :

- **moment** où le stock devient **propriété de C-Kreyol** (réception à Nantes, vente au client final, sortie de stock, autre **événement contractuel**) ;
- **suivi** de la **consignation** (opérationnel et comptable) ;
- **risques** (casse, perte, **péremption**) pendant la période de consignation ;
- **traduction Odoo 19 CE** : **figer d’abord** le **modèle métier** et les **flux réels**, puis retenir la **représentation la plus simple acceptable** dans le standard — **pas** l’inverse ; éviter une **sur-modélisation** de la consignation si elle **retarde** le lancement (cf. §11.3, [ADR-CKR-005](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005)).

**Phase 1 pragmatique** : ne pas exiger une sophistication juridique / stock **maximale** dès le premier jour si elle **retarde** une chaîne **opérable** ; **itérer** après preuve terrain, sous contrôle de la **sur-promesse** (§12.2).

---

## 6. Périmètre fonctionnel V1

## 6.1 Fonctionnel indispensable avant ouverture

Fonctionnalités minimales attendues :

- catalogue ;
- fiche produit ;
- panier ;
- tunnel de commande ;
- moyen de paiement ;
- mode de livraison et/ou retrait ;
- e-mails transactionnels minimum ;
- pages légales obligatoires ;
- contact clair ;
- **expérience mobile (navigateur) exigée** : parcours **catalogue → fiche → panier → commande** **utilisable et de qualité** sur **smartphone** (approche **responsive / mobile-first**, vérification sur appareils réels) — **must have** avant ouverture ; distincte d’une **application mobile native** (cf. §6.3).

## 6.2 Fonctionnel souhaitable si charge acceptable

Éléments souhaitables :

- compte client ;
- historique de commandes ;
- codes promotionnels ;
- newsletter ;
- FAQ ;
- avis clients ;
- pages éditoriales complémentaires.

## 6.3 Hors périmètre Phase 1

Éléments explicitement hors périmètre :

- marketplace multi-vendeurs avancée ;
- **application mobile native** (store) — **hors Phase 1** ; cela **ne dispense pas** de l’**expérience mobile web** exigée en §6.1 ;
- automatisation avancée non indispensable au premier euro ;
- design “agence” complet avant ouverture ;
- ERP étendu non requis à court terme.

---

## 7. Catalogue initial et offre

## 7.1 Objectif du catalogue initial

Le catalogue initial doit être :

- crédible ;
- limité ;
- exploitable ;
- correctement renseigné ;
- cohérent avec la capacité réelle d’exécution.

## 7.2 Références ciblées au démarrage

À préciser :

- nombre de références visé ;
- catégories de produits ;
- produits prioritaires ;
- produits exclus au démarrage.

## 7.3 Niveau minimal de qualité des fiches

Chaque fiche produit devra préciser au minimum :

- nom produit ;
- photo ;
- description ;
- origine ;
- composition / ingrédients ;
- allergènes si pertinents ;
- poids / format ;
- prix ;
- conditions de livraison ou retrait ;
- toute information réglementaire pertinente.

## 7.4 Arbitrages restants

À trancher :

- assortiment initial ;
- seuil minimal de références ;
- cohérence prix / coût logistique ;
- produits incompatibles avec le modèle retenu.

---

## 8. Logistique, exécution et promesse de service

## 8.1 Principes

La logistique doit être pensée à partir de la **promesse réellement tenable**, et non d’un idéal abstrait.

## 8.2 Questions à cadrer

- Où se trouve le stock ?
- Qui prépare ?
- Qui emballe ?
- Qui expédie ?
- Avec quel transporteur ou mode de remise ?
- Quel délai est annoncé ?
- Quel délai est réellement tenable ?
- Qui informe le client en cas d’aléa ?
- Comment sont gérées les ruptures ?

**Complément — Nantes et import-export** (articulation avec §4.4) :

- le flux passe-t-il **physiquement** par Nantes pour tout ou partie des commandes ?
- **délai et coût** comparés entre expédition **directe Antilles → client** et passage **via Nantes** ;
- **traçabilité** et **information client** lorsque plusieurs segments de chaîne coexistent ;
- **responsabilité** en cas d’incident sur un segment **outre-mer / import** vs segment **métropole**.

## 8.3 Promesse de service minimale

À définir :

- délai standard ;
- zone desservie ;
- mode de suivi ;
- politique incident / retard ;
- gestion du contact client.

## 8.4 Décisions attendues

Décisions logistiques Phase 1 :  
**[à compléter]**

---

## 9. Parcours client et expérience attendue

## 9.1 Intention

Le parcours client doit inspirer :

- confiance ;
- clarté ;
- simplicité ;
- cohérence entre promesse et réalité.

## 9.2 Points d’attention

À cadrer :

- ton de marque ;
- lisibilité des produits ;
- transparence sur l’origine ;
- clarté prix / frais / livraison ;
- qualité du tunnel de commande ;
- messages post-commande ;
- facilité de contact ;
- **qualité de l’expérience sur mobile** (lisibilité, performances perçues, tunnel de commande sans friction majeure) — alignée avec le **must have** fonctionnel §6.1.

## 9.3 Niveau de service minimal attendu

À définir :  
**[à compléter]**

---

## 10. Contraintes légales et conformité minimale

Avant ouverture, les éléments suivants doivent être traités :

- mentions légales ;
- CGV ;
- politique de confidentialité ;
- identité du vendeur ;
- règles de livraison ;
- règles de retour / réclamation ;
- conformité des informations produit ;
- politique de contact client.

Les points nécessitant validation externe ou arbitrage spécifique devront être listés ici.

Points ouverts :  
**[à compléter]**

---

## 11. Choix techniques V1

## 11.1 Socle cible

Le socle technique cible est :

- **Odoo 19 Community Edition**
- site web + boutique + back-office dans une base maîtrisée.

## 11.2 Décisions techniques à poser

À préciser :

- nom de domaine ;
- hébergement ;
- thème / socle site ;
- modules nécessaires ;
- e-mails transactionnels ;
- paiement ;
- gestion logistique ;
- sauvegardes ;
- environnement de recette.

## 11.3 Principe de construction

Le projet pourra s’appuyer sur une logique :

- **socle réutilisable** ;
- **extension C-Kreyol** spécifique ;
- progression incrémentale.

**Implémentation du modèle hub / consignation dans Odoo** : **d’abord** figer le **modèle métier** et les **flux réels** (cf. **§5.4**, [ADR-CKR-005](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005)) ; **ensuite** choisir la **traduction** dans **Odoo 19 CE** la **plus simple acceptable** — **pas** l’inverse.

---

## 12. Risques, dépendances et hypothèses

## 12.1 Dépendances

- disponibilité du premier fournisseur ;
- **cohérence** entre l’ambition **Nantes + import-export** et la **capacité réelle** (équipe, partenaires, financement) ;
- qualité et complétude des données produits ;
- capacité réelle de préparation / expédition ;
- arbitrage juridique/comptable du modèle ;
- cohérence entre promesse marketing et exécution réelle.

## 12.2 Risques principaux

- confusion de rôle entre **C-Kreyol** et **La Platine** ;
- ouverture prématurée sans chaîne opératoire claire ;
- coûts logistiques sous-estimés ;
- promesses de délai non tenues ;
- SAV insuffisamment cadré ;
- catalogue trop large trop tôt ;
- modèle économique non clarifié ;
- **sur-promesse** (retail, logistique, import-export, délais, qualité perçue) **par rapport à la capacité réellement tenable** en Phase 1 — risque de décrédibilisation du canal ;
- **complexification prématurée dans Odoo** pour coller à une **consignation** « parfaite » sur le papier **avant** stabilisation des **flux physiques réels** (cf. §5.4, §11.3, [ADR-CKR-005](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005)).

## 12.3 Hypothèses de travail

- démarrage avec **La Platine** comme premier fournisseur dominant ;
- catalogue initial limité ;
- montée en charge progressive ;
- validation par itération.

---

## 13. Critères de succès Phase 1

La Phase 1 sera considérée comme réussie si les conditions suivantes sont remplies :

1. première commande réelle payée et honorée ;
2. catalogue initial réellement publiable ;
3. responsabilité commerciale et opératoire clarifiée ;
4. moyens de paiement et de livraison fonctionnels ;
5. pages légales publiées ;
6. chaîne d’exécution reproductible ;
7. expérience client cohérente avec la promesse ;
8. **parcours mobile web** utilisable **sans friction majeure**, du **catalogue** à la **commande** (cf. §6.1, §9.2).

---

## 14. Arbitrages à rendre

**Orientation actée** (à **décliner** juridiquement, contractuellement et dans **Odoo**) : voir **§5.4** et les **[ADR-CKR-004](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-004)** / **[ADR-CKR-005](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005)**. Les arbitrages ci-dessous incluent encore des **affûtages**, des **validations externes** et des sujets **transverses**.

Les arbitrages suivants doivent être rendus avant gel Phase 1 :

- modèle commercial / juridique (**cadre principal** : §5.4 ; **détail** consignation / transfert de propriété / facturation fournisseur à finaliser) ;
- identité du vendeur final (**C-Kreyol** côté client — cohérence mentions / factures) ;
- **rôle de Nantes** (hypothèse cible : **hub léger** — cf. §4.4, [ADR-CKR-005](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005) ; **détail** opérationnel et **répartition** des flux à opérationnaliser) ;
- **compétence import-export** : niveau cible, titulaire des actes, transparence client ;
- zone de vente initiale ;
- B2B / B2C prioritaire ;
- niveau d’internalisation stock / logistique ;
- livraison vs retrait ;
- compte client dès V1 ou non ;
- seuil de catalogue initial ;
- niveau de transparence vis-à-vis du fournisseur ;
- politique SAV / retours / incident.

---

## 15. Plan d’exécution Phase 1

## 15.1 Lots proposés

### Lot 1 — Arbitrages structurants
- modèle commercial (**cadre** : [ADR-CKR-004](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-004), §5.4) ;
- responsabilités ;
- **rôle de Nantes** et **modèle logistique** visé (**cadre** : [ADR-CKR-005](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005), §4.4, §5.4) ;
- **import-export** : niveau de compétence et titulaire des actes ;
- zone de vente ;
- promesse logistique.

### Lot 2 — Offre et catalogue
- sélection produits ;
- fiches ;
- visuels ;
- règles de publication.

### Lot 3 — Socle technique
- instance Odoo ;
- thème ;
- modules ;
- paramétrages de base.

### Lot 4 — Vente et exécution
- paiement ;
- livraison / retrait ;
- **scénarios physiques** cohérents avec §4.4 (passage ou non par Nantes, direct fournisseur, etc.) ;
- e-mails ;
- scénarios de commande.

### Lot 5 — Cadre légal et confiance
- mentions ;
- CGV ;
- confidentialité ;
- contact.

### Lot 6 — Recette bout en bout
- commande test ;
- paiement test ;
- préparation ;
- remise / livraison ;
- communication client.

### Lot 7 — Ouverture contrôlée
- mise en ligne ;
- suivi ;
- premières corrections.

---

## 16. Décisions prises / à compléter

### Décisions déjà acquises
- C-Kreyol = **marque + canal retail digital spécialisé**
- La Platine = **premier fournisseur**
- V1 = **boutique spécialisée crédible**
- **Modèle commercial Phase 1** ([ADR-CKR-004](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-004)) : **achat-revente** — **C-Kreyol** **vend** au client final, **encaisse**, **achète** à **La Platine**
- **Modèle logistique cible Phase 1** ([ADR-CKR-005](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005)) : **hub léger à Nantes**, **flux tendu**, **stock consigné** — distinct d’un pur dropshipping, d’une simple vitrine et d’un stock lourd classique
- **Pas** de **stock centralisé systématique** au sens d’un **stock lourd** immobilisant ; la **consignation** et le **hub** **affinent** cette lecture (cf. §4.2, §4.4)
- **ancrage opérationnel** du projet = **Nantes** (France) ; **promesse de compétence** incluant une montée en maîtrise **logistique import-export** — la **famille** de rôle retenue comme **cible** est le **hub léger** (§4.4), avec **détail** physique et contractuel à **opérationnaliser**

### Décisions à compléter
- **Consignation** : **transfert de propriété** (événements déclencheurs), **suivi** opérationnel / comptable, **risques** (casse, perte, péremption) pendant consignation — avec **conseil juridique** / **fiscal** et alignement **CGV** (cf. §5.4)
- **Représentation dans Odoo 19 CE** : schéma **minimal acceptable** pour le **hub** et la **consignation** après stabilisation des **flux réels** (cf. §11.3, [ADR-CKR-005](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005))
- **[à compléter]**

---

## 17. Historique du document

| Date | Changement |
|------|------------|
| 2026-04-20 | Création du squelette initial de la note de cadrage Phase 1. |
| 2026-04-21 | Cadrage explicitement **orienté implémentation Odoo 19 CE** ; lien avec le [README](../../README.md) du projet. |
| 2026-04-21 | **Localisation** : projet C-Kreyol **localisé à Nantes** (France) ; distinction ancrage opérationnel / origine produits ; juridique à figer. |
| 2026-04-21 | **Nantes + import-export** : enrichissement du contexte (opéré depuis Nantes, promesse de compétence) ; vision **horizon 3 ans** (§3.2) ; positionnement §4.1 ; nouveau **§4.4** (trois modèles logistiques + questions) ; questions §5.1, §8.2, arbitrages §14, dépendances §12.1, décisions §16. |
| 2026-04-21 | **§3.5 Doctrine de construction Phase 1** : composition maîtrisée sur **Odoo 19 CE**, cohérence d’ensemble, spécifique seulement si le standard ne suffit pas. |
| 2026-04-21 | **ADR-CKR-001** : doctrine §3.5 inscrite au [registre ADR](ARCHITECTURE_DECISION_RECORD.md) (décision d’architecture acceptée). |
| 2026-04-21 | **ADR-CKR-002** : spécifique Phase 1 présumé légitime = **front-end** ; §3.5 enrichi ; README mis à jour. |
| 2026-04-21 | **ADR-CKR-003** : menu principal et **footer** entièrement personnalisés en Phase 1 ; §3.5 et README mis à jour. |
| 2026-04-21 | **§4.5** : benchmark d’inspiration **Caribshopper** (logique retail digital, collections, navigation éditoriale ; lecture Phase 1). |
| 2026-04-21 | **§6.1 / §6.3 / §9.2** : **expérience mobile web** (navigateur) = **must have** Phase 1 ; hors périmètre = **app native** uniquement. |
| 2026-04-21 | **§4.1** : formulation **retail digital** ; vocation **intermédiaire B2B** à terme. **§12.2** : risque **sur-promesse**. **§13** : critère de succès **mobile web**. **§16** : lien vers **ADR-CKR-004** (*modèle opératoire Phase 1*, ébauche registre). |
| 2026-04-21 | **Modèle opératoire cible** : **§4.2** / **§4.4** / **§5.4** — hub **Nantes**, **flux tendu**, **stock consigné** ; **ADR-CKR-004** (**achat-revente**) et **ADR-CKR-005** (**logistique**) **acceptées** ; règle **métier d’abord** puis **Odoo simple** (§11.3) ; risque **sur-complexification Odoo** §12.2. |
| 2026-04-21 | **[DESIGN.md](DESIGN.md)** : cadrage **design / retail / front** (benchmarks, principes, zones de page, mobile, ADR) ; lien depuis §1 et README. |
| 2026-04-21 | **[STRUCTURE_MENU_PRINCIPAL.md](STRUCTURE_MENU_PRINCIPAL.md)** : structure menu principal Phase 1 ; lien §1 note, README, **DESIGN** §6. |
| 2026-04-21 | **[WIREFRAME_HOMEPAGE.md](WIREFRAME_HOMEPAGE.md)** : filaire homepage Phase 1 ; lien §1 note, README, **DESIGN** §7. |
| 2026-04-21 | **[SPEC_HERO_HOMEPAGE.md](SPEC_HERO_HOMEPAGE.md)** : cadrage hero ; lien §1 note, README, **WIREFRAME** bloc 2. |
| 2026-04-21 | **[CHARTE_GRAPHIQUE_PHASE1.md](CHARTE_GRAPHIQUE_PHASE1.md)** : charte minimale avant gel hero ; lien §1 note, README, **DESIGN** §14, **SPEC_HERO** §2. |
| 2026-04-21 | **[CHARTE_GRAPHIQUE_PHASE1.md](CHARTE_GRAPHIQUE_PHASE1.md)** : **restructuration** ; **Direction A** gelée ; périmètre **§3**, détail **§§4–9**, décision **§11** ; états UI **à décliner**. |
| 2026-04-21 | **[BRIEF_SYNTHETIQUE_CK.md](BRIEF_SYNTHETIQUE_CK.md)** : brief **direction artistique** Phase 1 ; lien §1 note, README, **CHARTE**, **DESIGN**, **SPEC_HERO**. |
| 2026-04-21 | **[DIRECTIONS_ARTISTIQUES_PHASE1.md](DIRECTIONS_ARTISTIQUES_PHASE1.md)** : **3 pistes** DA + recommandation ; lien §1 note, README, **BRIEF** §11, **CHARTE** §3. |
| 2026-04-21 | **[BRIEF_VISUEL_HERO_PHASE1.md](BRIEF_VISUEL_HERO_PHASE1.md)** : brief **production** visuelle hero ; lien §1 note, README, **SPEC_HERO**, **CHARTE**. |