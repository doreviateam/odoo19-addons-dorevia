# PLAN — Méthodologie projet digital / front Odoo
## avec modèles documentaires

## 1. Objet du document

Ce document a pour objet de formaliser une **méthodologie de conduite de projet digital**, en particulier pour des projets **front-end / e-commerce / canal digital** s’appuyant sur **Odoo Community Edition** comme socle.

Il vise à :

- structurer la conduite de projet entre **vision**, **cadrage**, **décision**, **design**, **développement** et **recette** ;
- capitaliser une méthode réutilisable pour d’autres projets ;
- définir une **chaîne documentaire type** ;
- préparer la création de **modèles documentaires** réutilisables.

---

## 2. Intention de la méthode

L’objectif de cette méthode est d’éviter :

- le lancement prématuré du design ou du développement sans clarification du projet ;
- le mélange confus entre métier, juridique, design et technique ;
- les allers-retours permanents faute de décisions explicites ;
- la surconstruction technique trop tôt ;
- l’absence de capitalisation documentaire d’un projet à l’autre.

La méthode repose sur une progression par couches successives :

1. **clarifier ce qu’est le projet** ;
2. **le cadrer opérationnellement** ;
3. **figer les décisions structurantes** ;
4. **traduire le positionnement en design / expérience** ;
5. **formuler des briefs ciblés** ;
6. **traduire le tout en plan d’implémentation** ;
7. **faire une recette structurée** ;
8. **séparer le polish de la première livraison**.

---

## 3. Principes méthodologiques

### 3.1 Clarifier avant de produire

Ne pas partir directement dans :
- la maquette ;
- le design détaillé ;
- le développement ;
- ou l’intégration.

Toujours commencer par clarifier :

- la nature du projet ;
- son positionnement ;
- son rôle ;
- ses limites ;
- son vocabulaire ;
- son périmètre réel.

### 3.2 Distinguer les couches

Ne pas mélanger dans un seul document :

- la vision projet ;
- le cadrage métier ;
- les décisions structurantes ;
- le design ;
- la direction artistique ;
- le brief dev ;
- la recette.

Chaque couche doit avoir son ou ses documents dédiés.

### 3.3 Décider explicitement

Les décisions structurantes ne doivent pas rester implicites.  
Elles doivent être formalisées dans un registre de décisions (ADR ou équivalent) pour éviter de rouvrir sans cesse les mêmes arbitrages.

### 3.4 Respecter le socle technique

Autant que possible, respecter le socle **Odoo CE**, côté **front-end** comme côté **back-office**.

Le spécifique ne doit pas être un réflexe.  
Il intervient lorsque :
- le standard ne suffit pas ;
- ou que l’identité de marque / la qualité d’expérience l’exige clairement.

### 3.5 Ne pas faire mentir le design

Le design doit renforcer la lisibilité, la désirabilité et la crédibilité du canal.  
Il ne doit pas :
- sur-promettre ;
- embellir au point de masquer la réalité opératoire ;
- ni compenser artificiellement une faiblesse métier ou logistique.

### 3.6 Séparer livraison et polish

Une première livraison doit pouvoir être déclarée **satisfaisante** sans attendre la perfection.

Les éléments de finition, d’ajustement ou de confort visuel doivent être isolés dans une phase distincte :
- stabilisation ;
- polish ;
- Phase 1bis ;
- backlog non bloquant.

---

## 4. Chaîne documentaire type

### 4.1 Niveau identité / intention

#### `README.md`
Rôle :
- présenter ce qu’est le projet ;
- poser la vision ;
- rappeler le positionnement ;
- donner une porte d’entrée documentaire.

Contenu type :
- nom du projet ;
- nature du projet ;
- vision / mission ;
- publics ;
- valeur ;
- phases ;
- liens vers la documentation.

---

### 4.2 Niveau cadrage projet

#### `NOTE_DE_CADRAGE.md`
Rôle :
- transformer l’intention en cadre de travail opérationnel ;
- poser le périmètre, les arbitrages, les risques et les lots.

Contenu type :
- objet du document ;
- contexte ;
- vision rappelée ;
- objectif de phase ;
- positionnement ;
- modèle opératoire ;
- périmètre fonctionnel ;
- risques ;
- arbitrages à rendre ;
- plan d’exécution ;
- décisions prises / à compléter.

---

### 4.3 Niveau décisions structurantes

#### `ARCHITECTURE_DECISION_RECORD.md`
Rôle :
- consigner les décisions structurantes du projet ;
- éviter la rediscussion implicite ;
- fournir une doctrine stable.

Contenu type d’une entrée ADR :
- identifiant ;
- statut ;
- date ;
- contexte ;
- décision ;
- conséquences ;
- références.

---

### 4.4 Niveau design / expérience

#### `DESIGN.md`
Rôle :
- cadrer le design, la logique retail, l’expérience et les benchmarks ;
- traduire le positionnement en expérience visible.

Contenu type :
- objet ;
- rôle du design ;
- benchmarks ;
- principes front-end ;
- principes retail ;
- zones de page ;
- mobile ;
- éléments à éviter ;
- questions ouvertes.

---

### 4.5 Niveau structure front

#### `STRUCTURE_MENU_PRINCIPAL.md`
Rôle :
- cadrer la navigation principale ;
- fixer les options et la structure de niveau 1.

#### `WIREFRAME_HOMEPAGE.md`
Rôle :
- structurer la homepage ;
- définir les blocs et l’ordre de lecture.

#### `SPEC_HERO_HOMEPAGE.md`
Rôle :
- cadrer le premier écran ;
- fixer la hiérarchie du message, le CTA, le visuel et les exclusions.

---

### 4.6 Niveau direction artistique

#### `BRIEF_SYNTHETIQUE_<PROJET>.md`
Rôle :
- transmettre au graphiste / DA un brief simple et ciblé.

#### `DIRECTIONS_ARTISTIQUES_PHASE1.md`
Rôle :
- comparer plusieurs pistes de direction artistique ;
- permettre un arbitrage documenté.

#### `CHARTE_GRAPHIQUE_PHASE1.md`
Rôle :
- geler le socle visuel minimal ;
- fournir les règles nécessaires à l’implémentation front.

#### `BRIEF_VISUEL_HERO_PHASE1.md`
Rôle :
- produire les visuels du hero de façon cohérente avec la charte et la spec.

---

### 4.7 Niveau exécution développement

#### `BRIEF_DEV.md`
Rôle :
- donner au développeur un point d’entrée opérationnel ;
- synthétiser les décisions, le périmètre, la doctrine et les livrables.

#### `PLAN_IMPLEMENTATION.md`
Rôle :
- traduire le projet en architecture technique, arborescence, fichiers et ordre de réalisation.

---

### 4.8 Niveau recette / stabilisation

#### `RECETTE_FRONT_PHASE1.md`
Rôle :
- organiser la recette front de manière structurée ;
- distinguer conformité, écarts, blocants et non-bloquants.

#### `BACKLOG_PHASE_1BIS_FRONT.md`
Rôle :
- isoler les finitions et ajustements non bloquants ;
- éviter de rouvrir la livraison principale.

---

## 5. Ordre recommandé de production

Ordre type recommandé :

1. `README.md`
2. `NOTE_DE_CADRAGE.md`
3. `ARCHITECTURE_DECISION_RECORD.md`
4. `DESIGN.md`
5. `STRUCTURE_MENU_PRINCIPAL.md`
6. `WIREFRAME_HOMEPAGE.md`
7. `SPEC_HERO_HOMEPAGE.md`
8. `BRIEF_SYNTHETIQUE_<PROJET>.md`
9. `DIRECTIONS_ARTISTIQUES_PHASE1.md`
10. `CHARTE_GRAPHIQUE_PHASE1.md`
11. `BRIEF_VISUEL_HERO_PHASE1.md`
12. `BRIEF_DEV.md`
13. `PLAN_IMPLEMENTATION.md`
14. implémentation
15. `RECETTE_FRONT_PHASE1.md`
16. `BACKLOG_PHASE_1BIS_FRONT.md`

Cet ordre peut être ajusté selon le projet, mais la logique générale doit rester :

**cadrer → décider → designer → briefer → implémenter → recetter → polisher**

---

## 6. Règles de conduite de projet

### Règle 1 — Ne pas lancer le développement dans le vide
Aucun développement significatif ne doit commencer sans :
- clarification minimale du projet ;
- périmètre de phase ;
- doctrine de construction.

### Règle 2 — Chaque document a un destinataire principal
Exemples :
- décideur / porteur de projet ;
- AMO / chef de projet ;
- graphiste / DA ;
- développeur ;
- relecteur recette.

### Règle 3 — Les décisions doivent être traçables
Les décisions structurantes doivent être inscrites dans un registre ou équivalent.

### Règle 4 — Le spécifique doit être justifié
Le spécifique ne doit pas être une habitude.  
Il doit être justifié par :
- un besoin métier ;
- un besoin d’identité ;
- ou une insuffisance réelle du standard.

### Règle 5 — Le design ne doit pas contredire l’opérationnel
La promesse visuelle doit rester compatible avec :
- les produits réels ;
- les contenus disponibles ;
- la logistique réelle ;
- la promesse de service.

### Règle 6 — Le projet doit pouvoir être livré avant d’être parfait
Une première version peut être déclarée livrée si :
- le cœur de la promesse tient ;
- l’expérience principale fonctionne ;
- les écarts restants sont non bloquants et documentés.

---

## 7. Modèles documentaires à prévoir

Un répertoire de modèles réutilisables peut être créé, par exemple :

`docs/templates/`

Contenu cible :

- `README_TEMPLATE.md`
- `NOTE_DE_CADRAGE_TEMPLATE.md`
- `ADR_TEMPLATE.md`
- `DESIGN_TEMPLATE.md`
- `STRUCTURE_MENU_TEMPLATE.md`
- `WIREFRAME_HOMEPAGE_TEMPLATE.md`
- `SPEC_HERO_TEMPLATE.md`
- `BRIEF_DA_TEMPLATE.md`
- `DIRECTIONS_ARTISTIQUES_TEMPLATE.md`
- `CHARTE_PHASE1_TEMPLATE.md`
- `BRIEF_VISUEL_TEMPLATE.md`
- `BRIEF_DEV_TEMPLATE.md`
- `PLAN_IMPLEMENTATION_TEMPLATE.md`
- `RECETTE_TEMPLATE.md`
- `BACKLOG_1BIS_TEMPLATE.md`

---

## 8. Positionnement du rôle projet

Cette méthode formalise un rôle hybride pouvant être tenu par le porteur de projet ou l’AMO :

- **chef de projet**
- **architecte de cadrage**
- **AMO**
- **interface entre métier, design et développement**

Ce rôle consiste à :

- clarifier ;
- structurer ;
- décider ;
- documenter ;
- briefer ;
- recetter ;
- capitaliser.

---

## 9. Livrable cible de cette méthodologie

Le livrable final de cette méthodologie n’est pas seulement un site ou une implémentation.  
C’est aussi :

- une **chaîne documentaire réutilisable** ;
- une **méthode de conduite de projet** ;
- une base pour travailler plus vite et plus proprement sur les projets suivants.

---

## 10. Prochaine étape recommandée

À partir de ce plan, les prochaines étapes naturelles sont :

1. créer le document maître de méthode ;
2. ouvrir le dossier `docs/templates/` ;
3. produire les premiers modèles documentaires ;
4. tester la méthode sur un second projet pour consolidation.

---

## 11. Historique du document

| Date | Changement |
|------|------------|
| 2026-04-21 | Création du plan de méthodologie projet digital / front Odoo avec chaîne documentaire type et préparation des modèles documentaires. |