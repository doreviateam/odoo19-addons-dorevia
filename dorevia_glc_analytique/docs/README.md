# Spécification fonctionnelle V1 — Suivi d’activité GLC

**Projet :** Suivi d’activité GLC  
**Version :** V1.1  
**Statut :** Document de référence fonctionnel — cahier des charges pour développement futur  
**Périmètre :** Odoo 19 / pilotage analytique / coûts complets / bénévolat / rapport mensuel CA  
**Association concernée :** GLC — Saint-Aignan-de-Grand-Lieu  

**Annexes :**

- [Découpage en paliers](./PALIERS.md)
- [Règles d’affectation analytique](./REGLES_AFFECTATION.md)
- [Matrice de migration analytique](./MATRICE_MIGRATION.md)

---

## 1. Introduction

### 1.1 Nom du projet

Le projet est nommé :

> **Suivi d’activité GLC**

Il vise à structurer dans Odoo un dispositif de pilotage analytique permettant à l’association GLC de comprendre, mois par mois, le comportement économique de ses activités.

L’objectif n’est pas seulement comptable. Il s’agit de fournir une lecture de gestion claire, exploitable par les salariés, la direction, la trésorerie et le Conseil d’Administration.

### 1.2 Contexte général

GLC est une association implantée à **Saint-Aignan-de-Grand-Lieu**.

Ses missions s’articulent autour de plusieurs dimensions :

- le conte ;
- la nature ;
- le lac de Grand-Lieu ;
- la transmission culturelle ;
- les activités associatives ;
- l’accueil de publics ;
- la mise à disposition d’un lieu vivant.

L’association dispose d’un site physique structurant : un **ancien presbytère**, avec un **grand jardin**, un **bar**, un **restaurant** et une **cuisine**.

Ce lieu permet à GLC d’organiser des activités internes, d’accueillir des événements, de proposer des animations, de recevoir des artistes et de développer des recettes propres.

### 1.3 Partenaires

Un partenaire important est **Radio Grand Lieu**, qui occupe une partie du site en tant que **locataire**.

Cette relation génère une recette récurrente, notamment via un loyer mensuel.

### 1.4 Publics concernés

Le projet de suivi d’activité concerne indirectement plusieurs publics :

- les adhérents ;
- les bénévoles ;
- les salariés ;
- les artistes ;
- les spectateurs ;
- les clients de privatisation ;
- les partenaires institutionnels ;
- les financeurs ;
- les membres du Conseil d’Administration.

### 1.5 Ressources de l’association

GLC mobilise plusieurs types de ressources :

- adhésions ;
- dons ;
- subventions ;
- recettes propres ;
- bénévolat ;
- mises à disposition ;
- recettes de bar, restauration, billetterie ou privatisation ;
- loyers ou participations de partenaires.

La spécification V1 vise à rendre ces ressources lisibles sans les confondre avec les activités opérationnelles.

---

## 2. Problématique

### 2.1 Situation actuelle

GLC dispose déjà d’une comptabilité analytique, mais celle-ci est structurée autour d’un plan existant comportant **9 comptes analytiques**.

Ce plan permet une première lecture, mais il ne répond pas suffisamment aux besoins de pilotage par activité.

### 2.2 Limite principale : bloc RH monolithique

Le compte analytique actuel **RH_PERSONNEL** apparaît comme un bloc monolithique d’environ :

> **-20 608 €**

Ce montant global rend visible le poids des salaires, mais ne permet pas de comprendre quelles activités consomment réellement du temps salarié.

### 2.3 Problèmes identifiés

Les limites actuelles sont les suivantes :

1. **Impossible de savoir quelle activité consomme quoi en salaire.**  
   Les salaires sont visibles comme une masse globale, mais non ventilés vers les activités réelles.

2. **Pas de suivi structuré du bénévolat dans Odoo.**  
   Le temps bénévole est une ressource essentielle, mais il reste invisible dans le pilotage.

3. **Pas de coût complet par activité.**  
   Les soldes actuels peuvent donner une vision partielle, car ils ne prennent pas en compte l’ensemble des ressources réellement consommées.

4. **Décisions du CA prises sur des soldes bruts.**  
   Le Conseil d’Administration peut voir des recettes, des dépenses ou des soldes, mais sans toujours comprendre la charge réelle de fonctionnement ou d’animation derrière chaque activité.

5. **Risque de mauvaise interprétation économique.**  
   Une activité peut sembler rentable si les salaires et le bénévolat ne sont pas intégrés. À l’inverse, une activité peut sembler déficitaire alors qu’elle répond à une mission associative ou bénéficie de financements dédiés.

### 2.4 Besoin cible

GLC a besoin d’un outil permettant de répondre à des questions simples :

- Quelles activités consomment le plus de temps salarié ?
- Quelles activités reposent fortement sur le bénévolat ?
- Quelles activités génèrent des recettes propres ?
- Quelles activités sont structurellement déficitaires mais utiles à la mission associative ?
- Les financements couvrent-ils réellement les activités et les charges de structure ?
- Le Conseil d’Administration dispose-t-il d’une lecture fiable pour arbitrer ?

---

## 3. Objectifs

### 3.1 Objectif général

Mettre en place un module de suivi d’activité permettant de produire une lecture mensuelle claire des activités de GLC, en intégrant les dépenses directes, le temps salarié ventilé, le bénévolat et les recettes générées.

### 3.2 Objectifs fonctionnels V1

La V1 doit permettre de :

1. **Remplacer le plan analytique actuel par 7 activités pilotables.**  
   Le pilotage ne doit plus reposer sur des comptes analytiques trop techniques ou trop éclatés, mais sur des activités compréhensibles par les salariés et le CA.

2. **Ventiler les salaires sur les activités.**  
   Le module doit permettre d’affecter chaque mois une part du temps salarié aux différentes activités.

3. **Intégrer le suivi du bénévolat.**  
   Le bénévolat doit pouvoir être déclaré, contrôlé puis rattaché à une activité.

4. **Calculer le coût complet par activité.**  
   Le coût complet doit intégrer :
   - les dépenses directes ;
   - le coût salarié ventilé ;
   - le bénévolat en lecture de gestion.

5. **Produire un rapport mensuel pour le Conseil d’Administration.**  
   Le rapport doit être lisible, synthétique et exploitable pour prendre des décisions.

### 3.3 Hors périmètre V1

La V1 ne vise pas à :

- remplacer la comptabilité générale ;
- automatiser complètement les temps salariés ;
- donner un accès direct aux bénévoles dans Odoo ;
- monétiser comptablement le bénévolat ;
- produire une comptabilité analytique certifiée indépendante ;
- gérer le prévisionnel complet ;
- gérer les sous-activités fines ;
- gérer plusieurs exercices en comparaison avancée ;
- répartir automatiquement les charges de structure vers les activités ;
- produire des écritures analytiques de paie ;
- consolider plusieurs sociétés ;
- valoriser le bénévolat en comptabilité générale (même à titre provisionnel).

---

## 4. Architecture fonctionnelle

### 4.1 Principe général

La cible repose sur une architecture analytique à **2 plans analytiques** :

1. **Plan Activités**
2. **Plan Financements**

Cette séparation est fondamentale.

Le plan **Activités** sert à piloter ce que fait GLC.

Le plan **Financements** sert à qualifier les ressources qui alimentent l’équilibre de l’association.

### 4.2 Plan Activités

Le plan Activités contient 7 comptes analytiques pilotables :

| Code | Nom | Type | Rôle |
|---|---|---|---|
| `STRUCTURE` | Structure & Administration | Charge | Fonctionnement général |
| `BAR` | Bar, Restauration & Cuisine | Mixte | Activité bar, restaurant, cuisine |
| `PRESTATIONS` | Prestations & Animations | Mixte | Conte, animations, billetterie |
| `RESIDENCES` | Résidences artistiques | Charge subventionnée | Accueil, hébergement, logistique artiste |
| `MISSIONS` | Déplacements & Missions | Charge | Déplacements, missions, justificatifs |
| `PRIVATISATIONS` | Privatisation d’espace | Mixte | Location ponctuelle du lieu à des tiers |
| `LOCATION_RADIO` | Location Radio Grand Lieu | Recette | Loyer mensuel Radio Grand Lieu |

### 4.3 Plan Financements

Le plan Financements contient 4 comptes analytiques :

| Code | Nom | Rôle |
|---|---|---|
| `ADHESIONS` | Adhésions | Ressource associative récurrente |
| `DONS` | Dons | Ressource volontaire |
| `SUBVENTIONS` | Subventions | Financements publics ou institutionnels |
| `RESSOURCES_PROPRES` | Ressources propres | Recettes générées par l’activité économique |

### 4.4 Rôle différencié des plans

Le plan Activités répond à la question :

> **Que consomme et que produit chaque activité ?**

Le plan Financements répond à la question :

> **Quelles ressources alimentent le budget global de l’association ?**

Le plan Financements ne doit pas devenir un second plan d’activité. Il sert à qualifier la nature des ressources, pas à piloter les opérations.

### 4.5 Flux des données

Les données proviennent de plusieurs sources :

1. **Factures fournisseurs**  
   Elles alimentent les dépenses directes des activités.

2. **Factures clients / ventes / billetterie / POS**  
   Elles alimentent les recettes propres des activités.

3. **Ventilation salariale mensuelle**  
   Elle répartit les coûts salariés entre activités.

4. **Registre bénévole**  
   Il enregistre les heures bénévoles par activité.

5. **Paramètres de coût horaire**  
   Ils permettent de calculer un coût salarié ventilé et une valorisation de gestion du bénévolat.

6. **Modules Dorevia existants** (cf. §4.8)  
   Billetterie HelloAsso, adhésions, dons, POS bar, verrouillage comptable.

### 4.6 Lecture cible

Chaque mois, le module doit être capable de produire une synthèse du type :

| Activité | Produits | Charges directes | Salaires ventilés | Bénévolat (h) | Coût complet | Solde brut | Solde de gestion | Solde complet |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BAR | X € | X € | X € | X h | X € | X € | X € | X € |
| PRESTATIONS | X € | X € | X € | X h | X € | X € | X € | X € |
| STRUCTURE | X € | X € | X € | X h | X € | −X € | −X € | −X € |

**Trois niveaux de solde** (cf. §8.4) :

- **Solde brut** : produits − charges directes (vision comptable partielle).
- **Solde de gestion** : solde brut − salaires ventilés (vision opérationnelle pour le CA).
- **Solde complet** : solde de gestion − valorisation bénévolat (indicateur enrichi, non comptable).

### 4.7 Correspondance Odoo 19

| Concept métier | Objet Odoo cible | Remarque |
|---|---|---|
| Plan Activités / Financements | `account.analytic.plan` | 2 plans, distribution paramétrée par société |
| Activité pilotable | `account.analytic.account` | 7 + 4 comptes ; pas de modèle parallèle sauf extension légère |
| Affectation factures / écritures | `analytic_distribution` sur lignes | JSON multi-plans natif Odoo 19 |
| Ventilation salariale | `glc.salary.allocation` (custom) | **Hors écriture comptable** — overlay de gestion |
| Ligne de ventilation salariale | `glc.salary.allocation.line` (custom) | Contrainte : total = 100 % ou heures de référence |
| Registre bénévole | `glc.volunteer.timesheet` (custom) | Heures uniquement, pas de `account.move` |
| Coût salarié mensuel | `glc.employee.cost.line` (custom) | Historique mensuel par salarié |
| Rapport mensuel | `ir.actions.report` + agrégation | Source = move lines + ventilations + bénévolat |

**Règle architecturale :** les salaires restent en comptabilité générale (631/641…). La ventilation mensuelle **ne génère pas** d’écritures analytiques salariales en V1.

### 4.8 Intégrations modules Dorevia

| Source | Module | Affectation cible V1 | Automatisation |
|---|---|---|---|
| Billetterie | `dorevia_helloasso_billetterie` | `PRESTATIONS` + `RESSOURCES_PROPRES` | Manuelle en V1 ; mapping événement en V2 |
| Adhésions | `dorevia_membership_adhesions` | `ADHESIONS` | Manuelle en V1 |
| Dons HelloAsso | `dorevia_helloasso_payment` | `DONS` | Manuelle en V1 |
| POS bar | `point_of_sale` | `BAR` + `RESSOURCES_PROPRES` | Modèles de distribution par défaut |
| Verrouillage comptable | `dorevia_posted_lock` | — | Clôture comptable préalable à la clôture analytique |
| Trésorerie | `dorevia_cash_guard` | Lecture seule | Pas de doublon ; tableau de bord croisé en V2 |

La V1 **accepte des affectations manuelles** si une intégration n’est pas prête. Voir [Règles d’affectation](./REGLES_AFFECTATION.md).

---

## 5. Fiches activités

## 5.1 `STRUCTURE`

### Code

`STRUCTURE`

### Nom

Structure & Administration

### Type

Charge

### Description

L’activité `STRUCTURE` regroupe les charges de fonctionnement général de l’association.

Elle correspond aux coûts nécessaires pour que GLC existe, fonctionne, administre ses projets, respecte ses obligations et maintienne son organisation.

### Ressources consommées

- salaires administratifs ;
- temps de coordination ;
- frais généraux ;
- assurances ;
- abonnements ;
- logiciels ;
- fournitures ;
- téléphonie ;
- frais bancaires ;
- maintenance administrative ;
- frais de gouvernance ;
- temps bénévole de gestion ou d’administration.

### Recettes générées

En principe, `STRUCTURE` ne génère pas directement de recettes d’activité.

Elle est couverte par :

- les excédents des activités ;
- les adhésions ;
- les dons ;
- les subventions ;
- les ressources propres globales.

### Spécificités

`STRUCTURE` ne doit pas être utilisée comme compte fourre-tout.

Une dépense doit aller dans `STRUCTURE` seulement si elle relève du fonctionnement général et non d’une activité identifiable.

### Exemples concrets

- abonnement logiciel de gestion ;
- assurance de l’association ;
- frais postaux ;
- frais bancaires ;
- fournitures administratives ;
- temps salarié passé à la préparation du CA ;
- temps bénévole de secrétariat associatif.

---

## 5.2 `BAR`

### Code

`BAR`

### Nom

Bar, Restauration & Cuisine

### Type

Mixte

### Description

L’activité `BAR` regroupe les activités liées au bar, à la restauration, à la cuisine et aux consommations associées.

Elle inclut les consommations liées à Radio Grand Lieu lorsque celles-ci sont rattachées au bar ou à la cuisine.

### Ressources consommées

- achats de boissons ;
- achats alimentaires ;
- consommables bar ;
- produits de restauration ;
- temps salarié de service, préparation ou gestion ;
- temps bénévole au bar ;
- frais de cuisine ;
- petit matériel lié à l’activité bar/restauration.

### Recettes générées

- ventes bar ;
- ventes restauration ;
- ventes POS ;
- consommations facturées ;
- recettes de cuisine ou petite restauration.

### Spécificités

Le bar peut être une activité économique visible mais aussi une activité fortement consommatrice de temps bénévole.

Le module doit permettre de distinguer :

- les recettes encaissées ;
- les achats directs ;
- le temps salarié consommé ;
- le temps bénévole mobilisé.

### Exemples concrets

- un bénévole tient le bar 4 heures un samedi ;
- achat de boissons pour le bar ;
- vente de boissons via le point de vente ;
- repas préparés dans la cuisine pour un événement ;
- consommations liées à Radio Grand Lieu.

---

## 5.3 `PRESTATIONS`

### Code

`PRESTATIONS`

### Nom

Prestations & Animations

### Type

Mixte

### Description

L’activité `PRESTATIONS` regroupe les prestations artistiques, animations, interventions, ateliers, spectacles, contes et événements donnant lieu à billetterie ou facturation.

### Ressources consommées

- cachets ou prestations artistiques ;
- achats liés à une animation ;
- temps salarié de préparation ou animation ;
- temps bénévole d’accueil ;
- frais techniques ;
- communication spécifique ;
- matériel événementiel.

### Recettes générées

- billetterie Odoo ;
- facturation de prestations ;
- participations du public ;
- ventes liées à des animations ;
- recettes d’ateliers.

### Spécificités

Cette activité peut avoir une forte valeur associative même si son solde économique est faible ou négatif.

Il est donc important de lire :

- les recettes directes ;
- les financements éventuels ;
- le coût salarié ;
- l’apport bénévole.

### Exemples concrets

- spectacle de conte avec billetterie ;
- animation nature ;
- atelier pédagogique ;
- intervention facturée à une collectivité ;
- accueil bénévole des spectateurs.

---

## 5.4 `RESIDENCES`

### Code

`RESIDENCES`

### Nom

Résidences artistiques

### Type

Charge subventionnée

### Description

L’activité `RESIDENCES` regroupe les coûts liés à l’accueil d’artistes ou d’intervenants en résidence.

Elle couvre l’hébergement, l’accueil, la logistique et les dépenses directement liées à la présence d’artistes ou de prestataires dans le cadre d’une résidence.

### Ressources consommées

- hébergement ;
- logement chez l’habitant ;
- dédommagements d’accueil ;
- repas directement liés à la résidence ;
- logistique d’accueil ;
- temps salarié de coordination ;
- temps bénévole d’accueil ;
- matériel spécifique à la résidence.

### Recettes générées

En V1, cette activité est principalement considérée comme une charge.

Elle peut être couverte par :

- des subventions ;
- des financements de projet ;
- des dons ;
- des ressources propres affectées.

### Spécificités

`RESIDENCES` ne doit pas être confondu avec `MISSIONS`.

Une résidence concerne l’accueil d’artistes ou de prestataires chez GLC ou dans son réseau d’accueil.

Un déplacement d’un salarié ou artiste vers une mission extérieure relève plutôt de `MISSIONS`.

### Exemples concrets

- hébergement d’un conteur accueilli en résidence ;
- logement chez l’habitant avec dédommagement ;
- repas d’accueil directement lié à une résidence ;
- temps salarié de coordination de l’accueil ;
- temps bénévole pour installer ou accueillir un artiste.

---

## 5.5 `MISSIONS`

### Code

`MISSIONS`

### Nom

Déplacements & Missions

### Type

Charge

### Description

L’activité `MISSIONS` regroupe les frais liés aux déplacements, missions extérieures et interventions nécessitant des justificatifs.

### Ressources consommées

- frais kilométriques ;
- carburant ;
- péages ;
- train ;
- transports ;
- hébergement de mission ;
- repas de déplacement ;
- temps salarié en mission ;
- temps bénévole en mission.

### Recettes générées

En principe, `MISSIONS` ne génère pas directement de recettes.

Elle peut toutefois être liée à une prestation ou à un projet financé.

### Spécificités

Les justificatifs sont obligatoires.

Les frais de bouche ne doivent être affectés à `MISSIONS` que lorsqu’ils correspondent réellement à une mission extérieure ou un déplacement.

### Exemples concrets

- déplacement pour une réunion partenaire ;
- frais de train pour une mission ;
- repas pris lors d’une mission extérieure ;
- indemnités kilométriques ;
- déplacement lié à une intervention hors site.

---

## 5.6 `PRIVATISATIONS`

### Code

`PRIVATISATIONS`

### Nom

Privatisation d’espace

### Type

Mixte

### Description

L’activité `PRIVATISATIONS` regroupe les locations ponctuelles du lieu par des tiers.

Elle concerne la mise à disposition de l’ancien presbytère, du jardin, du bar, de la cuisine ou d’un espace identifié pour des événements privés ou professionnels.

### Ressources consommées

- temps salarié de préparation ;
- temps salarié d’accueil ;
- temps bénévole d’installation ;
- nettoyage ;
- petits achats liés à la privatisation ;
- fluides ou consommables ;
- usure ou maintenance du lieu.

### Recettes générées

- facturation de location d’espace ;
- forfaits de mise à disposition ;
- prestations complémentaires ;
- éventuelles consommations associées.

### Spécificités

La privatisation peut sembler rentable si seules les recettes sont observées.

Le module doit permettre d’intégrer :

- le temps de préparation ;
- le temps d’accueil ;
- le nettoyage ;
- les dépenses directes ;
- le bénévolat éventuel.

### Exemples concrets

- location ponctuelle du jardin ;
- privatisation du bar pour un événement ;
- accueil d’un tiers dans le presbytère ;
- temps bénévole de remise en état après événement.

---

## 5.7 `LOCATION_RADIO`

### Code

`LOCATION_RADIO`

### Nom

Location Radio Grand Lieu

### Type

Recette

### Description

L’activité `LOCATION_RADIO` regroupe les recettes liées à la location ou mise à disposition d’un espace à Radio Grand Lieu.

### Ressources consommées

En principe, cette activité consomme peu de ressources directes.

Elle peut toutefois consommer :

- charges de structure ;
- fluides ;
- maintenance du lieu ;
- temps administratif ;
- consommations bar ou cuisine si rattachées à la relation avec Radio Grand Lieu.

### Recettes générées

- loyer mensuel ;
- participation forfaitaire ;
- refacturations éventuelles.

### Spécificités

Cette activité doit être suivie séparément afin de distinguer les recettes récurrentes de location des autres recettes d’activité.

Le **montant de loyer de référence** (contrat locatif Radio Grand Lieu) est paramétré dans les réglages du module — il ne constitue pas une règle figée dans la fiche activité.

Règles d’affectation détaillées : voir [Règles d’affectation — §3 Radio / Bar](./REGLES_AFFECTATION.md#3-règles-radio-grand-lieu--bar).

### Exemples concrets

- facture mensuelle de loyer à Radio Grand Lieu ;
- participation à des charges ;
- consommations Radio rattachées au bar si elles concernent l’activité bar/cuisine.

---

## 6. Plan Financements

### 6.1 Principe

Le plan Financements sert à suivre les ressources qui alimentent le budget de GLC.

Il ne doit pas être piloté comme une activité opérationnelle.

Sa finalité est de répondre à la question :

> **D’où viennent les ressources qui permettent de financer les activités et la structure ?**

### 6.2 Comptes du plan Financements

| Code | Nom | Description |
|---|---|---|
| `ADHESIONS` | Adhésions | Cotisations des adhérents |
| `DONS` | Dons | Contributions volontaires, mécénat, dons ponctuels |
| `SUBVENTIONS` | Subventions | Financements publics, institutionnels ou affectés |
| `RESSOURCES_PROPRES` | Ressources propres | Recettes issues de l’activité économique de l’association |

### 6.3 Rôle des financements

Les financements alimentent le budget global.

Ils peuvent couvrir :

- les charges de structure ;
- les activités déficitaires mais nécessaires ;
- les résidences ;
- les missions ;
- les projets associatifs ;
- la masse salariale ;
- les investissements ou charges spécifiques.

### 6.4 Principe de non-confusion

Une subvention affectée à une résidence peut être suivie dans `SUBVENTIONS`, tandis que la dépense de résidence est suivie dans `RESIDENCES`.

Cela permet de distinguer :

- la nature de la ressource ;
- l’activité financée ;
- le coût complet de l’activité.

### 6.5 Ressources propres

Les ressources propres ne remplacent pas les activités.

Par exemple, une recette de bar peut être rattachée à l’activité `BAR` dans le plan Activités et qualifiée comme `RESSOURCES_PROPRES` dans le plan Financements.

### 6.6 Règles d’affectation

La matrice complète d’affectation par type de pièce (factures, POS, subventions, paie…) est documentée dans l’annexe [Règles d’affectation analytique](./REGLES_AFFECTATION.md). Elle est **obligatoire** pour le paramétrage Odoo 19 et le contrôle mensuel.

---

## 7. Parcours utilisateurs

## 7.1 Gestionnaire — workflow mensuel complet

### Rôle

Le gestionnaire est responsable de la production mensuelle des données de pilotage.

### Étapes mensuelles

1. Vérifier les écritures comptables du mois.
2. Contrôler les affectations analytiques des factures fournisseurs.
3. Contrôler les affectations analytiques des recettes.
4. Saisir ou vérifier la ventilation salariale mensuelle.
5. Saisir les heures bénévoles à partir des justificatifs signés.
6. Contrôler les anomalies.
7. Générer le rapport mensuel.
8. Transmettre le rapport au CA.
9. Archiver la version mensuelle du rapport.

### Résultat attendu

À la fin du workflow, le mois est considéré comme pilotable.

Le CA peut lire :

- les recettes par activité ;
- les charges directes ;
- les salaires ventilés ;
- le bénévolat mobilisé ;
- le coût complet ;
- les soldes de gestion.

---

## 7.2 Salarié — saisie timesheet V2

### Statut V1

En V1, les salariés ne saisissent pas nécessairement leurs temps eux-mêmes.

La saisie peut être centralisée par le gestionnaire.

### Cible V2

En V2, les salariés pourront saisir leurs temps par activité via un mécanisme de timesheet.

### Objectif futur

La saisie salarié permettra de fiabiliser la ventilation salariale.

Elle devra rester simple :

- date ;
- salarié ;
- activité ;
- durée ;
- commentaire ;
- validation éventuelle.

---

## 7.3 Bénévole — déclaration contrôlée

### Principe V1

Le bénévole ne saisit pas directement dans Odoo en V1.

Le processus cible est :

> **papier signé → contrôle → saisie par un salarié ou gestionnaire**

### Étapes

1. Le bénévole réalise une action.
2. Il déclare ses heures sur une fiche papier ou formulaire validé.
3. Le document est signé.
4. Un salarié ou gestionnaire contrôle la cohérence.
5. Les heures sont saisies dans le registre bénévole.
6. Les heures sont rattachées à une activité.

### Données minimales

- nom du bénévole ;
- date ;
- activité ;
- durée ;
- description courte ;
- signature ;
- personne ayant saisi ;
- date de saisie.

### Exemple

Un bénévole tient le bar 4 heures un samedi.

La saisie cible est :

| Champ | Valeur |
|---|---|
| Bénévole | David |
| Date | Samedi concerné |
| Activité | `BAR` |
| Durée | 4h |
| Nature | Bénévolat |
| Justificatif | Fiche signée |
| Saisi par | Salarié ou gestionnaire |

---

## 7.4 Conseil d’Administration — lecture rapport PDF

### Rôle

Le CA utilise le rapport pour comprendre la situation économique réelle de l’association.

### Besoin

Le rapport doit être lisible par des administrateurs non techniciens.

Il doit permettre de répondre rapidement à ces questions :

- quelles activités coûtent le plus ?
- quelles activités génèrent des recettes ?
- quelles activités consomment le plus de temps salarié ?
- où le bénévolat est-il déterminant ?
- les financements couvrent-ils les charges ?
- quelles décisions doivent être prises ?

### Support

Le support cible V1 est un **rapport PDF mensuel**.

---

## 8. Règles métier

## 8.1 Règle 1 — Pas de compte salaire

Il ne doit pas exister de compte analytique d’activité nommé “salaire” ou “RH_PERSONNEL” dans le plan Activités cible.

Les salaires sont des ressources consommées par les activités.

Ils doivent être ventilés vers les activités, et non isolés dans un compte monolithique.

### Formulation de la règle

> Un salaire n’est pas une activité. C’est une ressource consommée par une activité.

---

## 8.2 Règle 2 — Ventilation mensuelle obligatoire

Chaque mois, les coûts salariés doivent être ventilés sur les activités.

La ventilation peut être faite :

- en heures ;
- en pourcentage ;
- ou selon une clé mensuelle validée.

### Contrôle attendu

Le total ventilé pour un salarié sur un mois doit représenter 100 % de son temps ou de son coût ventilable.

### Exemple

| Salarié | Mois | BAR | PRESTATIONS | STRUCTURE | Total |
|---|---|---:|---:|---:|---:|
| Salarié A | Janvier | 20 % | 50 % | 30 % | 100 % |

---

## 8.3 Règle 3 — Bénévolat = heures comptées, pas monétisées en compta

Le bénévolat doit être suivi en heures.

En V1, il ne doit pas être monétisé dans la comptabilité générale.

Il peut toutefois être valorisé dans la lecture de gestion du coût complet.

### Formulation de la règle

> Le bénévolat est compté en heures dans Odoo. Sa valorisation éventuelle sert au pilotage, pas à modifier la comptabilité générale.

---

## 8.4 Règle 4 — Coût complet et trois niveaux de solde

Le coût complet d’une activité inclut :

1. les charges directes ;
2. le coût salarié ventilé ;
3. la valorisation de gestion du bénévolat.

### Formule — coût complet

```text
Coût complet activité =
Charges directes activité
+ Coût salarié ventilé activité
+ Valorisation de gestion du bénévolat activité
```

### Trois niveaux de solde

Le rapport et les écrans de pilotage doivent distinguer **trois indicateurs** :

```text
Solde brut =
Produits directs activité − Charges directes activité

Solde de gestion =
Solde brut − Coût salarié ventilé activité

Solde complet =
Solde de gestion − Valorisation de gestion du bénévolat activité
```

**Lecture CA :**

- Le **solde brut** reflète la performance comptable directe (sans salaires ni bénévolat).
- Le **solde de gestion** est l’indicateur principal d’arbitrage opérationnel.
- Le **solde complet** intègre le bénévolat valorisé — indicateur enrichi, **non comptable**, présenté avec une note méthodologique dans le rapport PDF.

Le bénévolat est affiché en **heures** dans les tableaux principaux ; la valorisation monétaire figure en encart ou annexe.

---

## 8.5 Règle 5 — Un bénévole signe, un salarié saisit

En V1, la déclaration bénévole doit être contrôlée.

Le bénévole signe la déclaration.

Un salarié ou gestionnaire saisit les heures dans Odoo.

### Objectif

Cette règle permet de garantir :

- la traçabilité ;
- la fiabilité ;
- la responsabilité de la saisie ;
- la possibilité d’audit interne.

---

## 8.6 Formules de calcul

### Coût horaire salarié

```text
Coût horaire salarié =
Coût mensuel chargé du salarié
/ Nombre d’heures mensuelles de référence
```

### Coût salarié ventilé par activité

```text
Coût salarié activité =
Heures salarié affectées à l’activité
× Coût horaire salarié
```

Ou, en ventilation par pourcentage :

```text
Coût salarié activité =
Coût mensuel chargé du salarié
× Pourcentage affecté à l’activité
```

### Heures bénévoles par activité

```text
Heures bénévoles activité =
Somme des heures bénévoles validées sur l’activité
```

### Valorisation de gestion du bénévolat

```text
Valorisation bénévolat activité =
Heures bénévoles activité
× Taux horaire de valorisation
```

### Produits directs activité

```text
Produits directs activité =
Somme des écritures de produits affectées à l’activité
```

### Charges directes activité

```text
Charges directes activité =
Somme des écritures de charges affectées à l’activité
```

### Solde brut activité

```text
Solde brut activité =
Produits directs activité
- Charges directes activité
```

### Solde de gestion activité

```text
Solde de gestion activité =
Solde brut activité
- Coût salarié ventilé activité
```

### Solde complet activité

```text
Solde complet activité =
Solde de gestion activité
- Valorisation bénévolat activité
```

### Contrôle ventilation salariale vs compta

```text
Écart salarial =
| Total coûts ventilés du mois − Masse salariale comptable du mois|
/ Masse salariale comptable du mois

Si écart > 5 % → alerte
```

---

## 8.7 Règle 6 — Clôture mensuelle analytique

Chaque mois, le gestionnaire exécute une **clôture analytique** distincte de la clôture comptable.

### Prérequis

1. Écritures comptables du mois validées (lien avec `dorevia_posted_lock` si installé).
2. 100 % des salariés actifs ventilés pour le mois.
3. Bénévolat saisi et validé.
4. Affectations analytiques obligatoires contrôlées (cf. [Règles d’affectation](./REGLES_AFFECTATION.md)).

### Workflow

1. Contrôler les anomalies (pièces sans analytique, ventilations incomplètes).
2. Générer le rapport mensuel.
3. Passer le mois au statut **Verrouillé**.
4. Archiver le PDF (référence `GLC-RPT-AAAA-MM-v1`).

### Après verrouillage

Toute modification nécessite le rôle « Responsable pilotage » et laisse une trace dans le fil de discussion (chatter).

### Calendrier cible

Clôture analytique à **J+10** après la clôture comptable (paramétrable).

---

## 8.8 Règle 7 — Charges indirectes et STRUCTURE

En V1, les charges **non identifiables** à une activité opérationnelle sont affectées à `STRUCTURE`.

Il n’existe **pas de répartition automatique** structure → activités en V1 (évolution V3).

Si le poids de `STRUCTURE` dépasse un seuil paramétré (% des charges totales), le rapport mensuel doit afficher une **alerte** (risque de compte fourre-tout).

---

## 8.9 Règle 8 — Radio Grand Lieu / Bar

| Nature | Activité |
|---|---|
| Loyer mensuel Radio | `LOCATION_RADIO` |
| Consommations bar/cuisine Radio | `BAR` |
| Refacturation charges communes à Radio | `LOCATION_RADIO` |
| Charges communes non refacturables | `STRUCTURE` |

Détail : [Règles d’affectation — §3](./REGLES_AFFECTATION.md#3-règles-radio-grand-lieu--bar).

---

## 9. Modèle de données fonctionnel

Cette section décrit les entités attendues sans spécifier de code technique.

## 9.1 Activité

### Rôle

Représente une activité pilotable de GLC.

### Données principales

- code ;
- nom ;
- type ;
- description ;
- activité active / inactive ;
- compte analytique associé ;
- ordre d’affichage ;
- couleur ou indicateur visuel ;
- responsable éventuel ;
- commentaire de pilotage.

### Exemples

- `BAR`
- `PRESTATIONS`
- `STRUCTURE`

---

## 9.2 Ventilation salariale

### Rôle

Permet d’affecter mensuellement le coût salarié aux activités.

### Données principales

- mois ;
- exercice ;
- société (`company_id`) ;
- salarié (`employee_id` → `hr.employee`) ;
- coût mensuel chargé ;
- devise ;
- méthode de ventilation (`percent` | `hours`) ;
- lignes de ventilation ;
- activité ;
- pourcentage ou heures ;
- montant calculé ;
- statut ;
- validé par ;
- date de validation.

### Source du coût mensuel chargé (V1)

- **Saisie manuelle** mensuelle par salarié, ou import CSV.
- Définition : salaire brut + charges patronales + avantages en nature (à valider avec la paie).
- Historique conservé dans `glc.employee.cost.line` pour comparabilité inter-mois.
- Lien `hr_payroll` : hors périmètre V1, évolution V2.

### Statuts possibles

- brouillon ;
- à contrôler ;
- validé ;
- verrouillé.

### Règle de validation

La somme des lignes doit atteindre 100 % ou le total d’heures attendu.

---

## 9.3 Registre bénévole

### Rôle

Permet d’enregistrer les heures bénévoles validées.

### Données principales

- bénévole (`partner_id` — contact) ;
- date ;
- activité ;
- durée ;
- description ;
- justificatif papier existant ;
- pièce jointe scan (`attachment_ids`) ;
- référence du justificatif ;
- signé ;
- saisi par ;
- date de saisie ;
- validé par ;
- statut.

### Données personnelles (RGPD)

- Accès limité aux groupes autorisés.
- Durée de conservation paramétrable.
- Pas d’exposition des données bénévoles dans le rapport CA (agrégats par activité uniquement).

### Statuts possibles

- saisi ;
- à contrôler ;
- validé ;
- rejeté ;
- archivé.

---

## 9.4 Employé — extension

### Rôle

Permet de disposer des paramètres nécessaires au calcul du coût salarié.

### Données principales

- salarié ;
- coût mensuel chargé ;
- heures mensuelles de référence ;
- coût horaire calculé ;
- actif / inactif ;
- date de début ;
- date de fin ;
- commentaire ;
- lignes d’historique mensuel (`glc.employee.cost.line`).

### Principe

Le coût horaire n’est pas nécessairement affiché à tous les utilisateurs.

Les droits d’accès doivent permettre de protéger les données sensibles (cf. §15).

---

## 9.5 Paramètres

### Rôle

Centralise les règles de calcul du module.

### Données principales

- taux horaire de valorisation du bénévolat (+ date d’effet) ;
- montant de loyer Radio de référence (contrat locatif) ;
- méthode de ventilation par défaut ;
- verrouillage mensuel ;
- activité par défaut interdite ou autorisée ;
- plans analytiques par défaut (Activités, Financements) ;
- modèles de distribution par journal ;
- génération rapport PDF ;
- période de référence ;
- droits de validation ;
- seuils d’alerte (% poids STRUCTURE, activité déficitaire N mois consécutifs, écart salarial 5 %).

---

## 9.6 Correspondance technique Odoo 19

Récapitulatif des objets natifs et custom (détail §4.7) :

| Modèle custom | Rôle |
|---|---|
| `glc.salary.allocation` | Ventilation salariale mensuelle |
| `glc.salary.allocation.line` | Ligne d’affectation par activité |
| `glc.employee.cost.line` | Historique coût mensuel chargé |
| `glc.volunteer.timesheet` | Registre bénévole |
| `glc.activity.report` | Snapshot mensuel verrouillé (optionnel) |

Les activités pilotables **réutilisent** `account.analytic.account` — pas de duplication du référentiel analytique Odoo.

---

## 10. Interfaces

## 10.1 Tableau de bord

### Type d’écran

Kanban ou tableau synthétique.

### Objectif

Donner une vision immédiate des activités.

### Contenu attendu

Pour chaque activité :

- nom ;
- code ;
- type ;
- produits du mois ;
- charges directes ;
- coût salarié ventilé ;
- heures bénévoles ;
- coût complet ;
- solde complet ;
- indicateur visuel.

### Indicateurs possibles

- activité excédentaire ;
- activité déficitaire ;
- activité non ventilée ;
- bénévolat élevé ;
- salaires non ventilés ;
- données incomplètes.

---

## 10.2 Liste activités

### Objectif

Afficher les 7 activités pilotables.

### Colonnes attendues

- code ;
- nom ;
- type ;
- actif ;
- responsable ;
- produits mois ;
- charges mois ;
- solde complet mois.

### Actions

- ouvrir la fiche activité ;
- consulter le rapport ;
- filtrer par type ;
- comparer les mois.

---

## 10.3 Fiche activité

### Objectif

Donner le détail d’une activité.

### Sections attendues

1. Informations générales
2. Description
3. Données du mois
4. Charges directes
5. Produits directs
6. Ventilation salariale
7. Bénévolat
8. Historique mensuel
9. Commentaire de gestion

### Lecture cible

La fiche doit expliquer l’activité, pas seulement afficher des montants.

---

## 10.4 Écran ventilation salaires

### Objectif

Permettre au gestionnaire de ventiler les salaires mensuellement.

### Fonctionnalités attendues

- sélection du mois ;
- liste des salariés ;
- coût mensuel chargé ;
- affectation par activité ;
- saisie en pourcentage ou heures ;
- contrôle total 100 % ;
- validation ;
- verrouillage ;
- commentaires.

### Contrôles

- total obligatoire ;
- activité obligatoire ;
- salarié actif ;
- période ouverte ;
- validation par utilisateur autorisé.

---

## 10.5 Écran registre bénévoles

### Objectif

Suivre les heures bénévoles.

### Fonctionnalités attendues

- création d’une déclaration ;
- sélection du bénévole ;
- date ;
- activité ;
- durée ;
- description ;
- indication justificatif signé ;
- statut ;
- validation.

### Contrôles

- durée positive ;
- activité obligatoire ;
- justificatif signé avant validation ;
- saisie par salarié ou gestionnaire ;
- traçabilité de validation.

---

## 10.6 Fiche employé — coût horaire

### Objectif

Paramétrer les éléments nécessaires au calcul du coût salarié.

### Données visibles selon droits

- coût mensuel chargé ;
- heures mensuelles de référence ;
- coût horaire calculé ;
- historique éventuel ;
- statut actif.

### Sécurité

L’accès doit être limité aux utilisateurs autorisés.

---

## 10.7 Configuration

### Objectif

Paramétrer le module.

### Paramètres attendus

- taux horaire de valorisation du bénévolat ;
- montant de loyer Radio de référence ;
- méthode de ventilation par défaut ;
- période de verrouillage ;
- activités actives ;
- plans analytiques par défaut ;
- modèles de distribution par journal ;
- modèle de rapport ;
- seuils d’alerte ;
- droits de validation.

---

## 11. Rapports

## 11.1 Rapport PDF par activité

### Objectif

Produire une synthèse mensuelle lisible pour le CA.

### Fréquence

Le rapport est produit chaque mois.

### Destinataires

- Conseil d’Administration ;
- direction ;
- trésorerie ;
- gestionnaire ;
- éventuellement partenaires internes.

---

## 11.2 Contenu du rapport

Le rapport PDF doit contenir :

0. **Note méthodologique** (1/2 page) — définitions des soldes, taux bénévolat, hors comptabilité
1. Page de synthèse générale (KPI — cf. §11.7)
2. Tableau des activités (trois niveaux de solde)
3. Détail par activité (+ drill-down : 10 principales écritures)
4. Synthèse des financements (équilibre global)
5. Lecture des salaires ventilés
6. Lecture du bénévolat (heures en priorité)
7. Alertes et points d’attention
8. Commentaire de gestion
9. Annexes éventuelles

**Formats :** PDF obligatoire ; export XLSX pour le trésorier (V1.1 si effort compatible, sinon V2).

**Référence document :** `GLC-RPT-AAAA-MM-v1`.

---

## 11.3 Tableau de synthèse

Exemple de structure :

| Activité | Produits | Charges directes | Salaires | Bénévolat h | Coût complet | Solde brut | Solde gestion | Solde complet |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| STRUCTURE | 0 € | X € | X € | X h | X € | −X € | −X € | −X € |
| BAR | X € | X € | X € | X h | X € | X € | X € | X € |
| PRESTATIONS | X € | X € | X € | X h | X € | X € | X € | X € |

---

## 11.4 Rapport par activité

Chaque fiche activité du rapport doit présenter :

- description courte ;
- produits du mois ;
- charges directes ;
- salaires ventilés ;
- bénévolat ;
- coût complet ;
- solde brut ;
- solde de gestion ;
- solde complet ;
- commentaire ;
- alerte éventuelle.

---

## 11.5 Synthèse bénévolat

Le rapport doit rendre visible :

- total heures bénévoles du mois ;
- heures bénévoles par activité ;
- activités les plus dépendantes du bénévolat ;
- valorisation de gestion éventuelle ;
- commentaire qualitatif.

---

## 11.6 Synthèse salaires

Le rapport doit rendre visible :

- total coût salarié ventilé ;
- ventilation par activité ;
- activités les plus consommatrices de temps salarié ;
- écarts ou mois non ventilés ;
- commentaire de gestion.

---

## 11.7 KPI de synthèse (page 1)

Quatre indicateurs minimum en page de synthèse :

| KPI | Formule | Usage CA |
|---|---|---|
| Taux de couverture | Produits directs / coût complet | Activité autosuffisante ? |
| Part du bénévolat | Heures activité / heures totales | Dépendance bénévole |
| Intensité salariale | Coût salarié ventilé / produits directs | Poids du travail salarié |
| Poids STRUCTURE | Coût STRUCTURE / total coûts | Charge de fonctionnement |

---

## 12. Déploiement

## 12.1 Phase 0 — Préparation

### Objectif

Préparer la migration vers le nouveau pilotage analytique.

### Actions

- valider la liste des 7 activités ;
- valider le plan Financements ;
- identifier les comptes existants à migrer ;
- **compléter et valider la [Matrice de migration](./MATRICE_MIGRATION.md)** ;
- définir les règles d’affectation ([annexe](./REGLES_AFFECTATION.md)) ;
- préparer les utilisateurs ;
- définir les droits ;
- valider les modèles de rapport.

### Livrables

- plan analytique cible ;
- matrice de correspondance ancien / nouveau ([MATRICE_MIGRATION.md](./MATRICE_MIGRATION.md)) ;
- règles de saisie ([REGLES_AFFECTATION.md](./REGLES_AFFECTATION.md)) ;
- modèle de rapport CA.

---

## 12.2 Phase 1 — Paramétrage

### Objectif

Configurer Odoo selon la cible.

### Actions

- créer le plan Activités ;
- créer le plan Financements ;
- créer les comptes analytiques ;
- paramétrer les droits ;
- paramétrer les coûts horaires ;
- paramétrer le taux de valorisation du bénévolat ;
- préparer les écrans ;
- tester le rapport.

### Critère de sortie

Les activités et financements sont prêts à être utilisés.

---

## 12.3 Phase 2 — Migration données

### Objectif

Reclasser les données existantes selon la nouvelle nomenclature.

### Actions

- analyser les écritures existantes ;
- migrer ou réaffecter les comptes analytiques ;
- traiter le bloc `RH_PERSONNEL` ;
- préparer une première ventilation salariale ;
- contrôler les soldes ;
- produire un premier rapport test.

### Risque principal

La migration peut révéler des écritures mal affectées ou trop générales.

Ces écarts doivent être documentés, pas masqués.

---

## 12.4 Phase 3 — Routinisation

### Objectif

Installer le rituel mensuel.

### Actions

- définir une date mensuelle de clôture analytique ;
- saisir les ventilations salariales ;
- saisir le bénévolat ;
- contrôler les écritures ;
- produire le rapport ;
- le présenter au CA ;
- archiver le rapport.

### Critère de réussite

Le CA reçoit chaque mois une lecture fiable et comparable.

---

## 12.5 Phase 4 — Évolution

### Objectif

Préparer les versions futures.

### Actions

- recueillir les retours utilisateurs ;
- identifier les besoins d’automatisation ;
- préparer les timesheets salariés ;
- améliorer les alertes ;
- préparer le multi-exercice ;
- envisager les sous-activités.

---

## 13. Évolutions

## 13.1 V2 — Timesheets salariés

### Objectif

Permettre aux salariés de déclarer directement leur temps par activité.

### Fonctionnalités possibles

- saisie hebdomadaire ou mensuelle ;
- activité obligatoire ;
- durée ;
- commentaire ;
- validation par responsable ;
- transformation automatique en ventilation salariale.

---

## 13.2 V2 — Alertes automatiques

### Objectif

Signaler les anomalies.

### Alertes possibles

- mois non ventilé ;
- ventilation inférieure ou supérieure à 100 % ;
- bénévolat non signé ;
- activité sans affectation ;
- hausse anormale d’une charge ;
- activité déficitaire plusieurs mois ;
- absence de rapport mensuel.

---

## 13.3 V3 — Multi-exercice

### Objectif

Comparer les exercices.

### Fonctionnalités possibles

- comparaison N / N-1 ;
- cumul annuel ;
- graphiques d’évolution ;
- export CA annuel ;
- rapport de synthèse exercice.

---

## 13.4 V3 — Sous-activités

### Objectif

Affiner le pilotage sans complexifier la V1.

### Exemples

- sous-activité bar ;
- sous-activité restauration ;
- sous-activité conte ;
- sous-activité animation nature ;
- sous-activité résidence ;
- sous-activité privatisation.

---

## 13.5 V3 — Prévisionnel

### Objectif

Comparer réalisé et budget.

### Fonctionnalités possibles

- budget par activité ;
- prévision mensuelle ;
- écart budget / réalisé ;
- simulation ;
- alerte de dépassement ;
- projection de fin d’exercice.

---

## 14. Glossaire

### Activité

Unité de pilotage correspondant à ce que fait concrètement GLC.

Exemples : bar, prestations, résidences, privatisations.

### Plan analytique

Organisation des axes de suivi permettant de ventiler les écritures et données de gestion.

### Plan Activités

Plan analytique principal permettant de piloter les 7 activités de GLC.

### Plan Financements

Plan analytique permettant de qualifier l’origine des ressources financières ou contributives.

### Coût direct

Charge directement affectée à une activité.

Exemple : achat de boissons pour le bar.

### Coût salarié ventilé

Part du coût salarié affectée à une activité selon une clé mensuelle.

### Bénévolat

Temps donné volontairement à l’association, suivi en heures et rattaché à une activité.

### Valorisation de gestion

Conversion d’une donnée non monétaire en valeur de pilotage.

Exemple : heures bénévoles × taux horaire de référence.

### Coût complet

Somme des charges directes, du coût salarié ventilé et de la valorisation de gestion du bénévolat.

### Solde brut

Produits directs moins charges directes.

### Solde de gestion

Solde brut moins coût salarié ventilé. Indicateur principal d'arbitrage pour le CA.

### Solde complet

Solde de gestion moins valorisation de gestion du bénévolat. Indicateur enrichi, non comptable.

### Clôture analytique

Processus mensuel de contrôle, génération du rapport et verrouillage des données de pilotage (cf. §8.7).

### Correspondance Odoo 19

Mapping entre concepts métier GLC et objets natifs Odoo (`account.analytic.plan`, `analytic_distribution`, modèles custom). Cf. §4.7 et §9.6.

### CA

Conseil d’Administration.

### Ressources propres

Recettes générées directement par les activités économiques ou opérationnelles de l’association.

### Subvention

Financement public ou institutionnel, affecté ou non à un projet.

### Adhésion

Cotisation versée par un adhérent.

### Don

Contribution volontaire sans contrepartie directe.

---

## 15. Sécurité et droits d'accès

### 15.1 Groupes utilisateurs

| Groupe | Ventilation salariale | Coûts salariés | Bénévolat | Rapport PDF | Clôture mensuelle | Analytique factures |
|---|---|---|---|---|---|---|
| Gestionnaire pilotage | R/W | Lecture | R/W | Génération | Oui | R/W |
| Direction / Trésorier | — | Lecture | — | Lecture | — | Lecture |
| Conseil d'Administration | — | — | — | Lecture seule | — | — |
| Salarié | — | — | Saisie (V1) | — | — | — |
| Comptable | — | — | — | — | — | R/W |

### 15.2 Données sensibles

Les champs suivants sont masqués aux profils non autorisés :

- coût mensuel chargé ;
- coût horaire calculé ;
- données nominatives bénévoles (rapport CA : agrégats uniquement).

### 15.3 Traçabilité

Toute validation (ventilation salariale, bénévolat, clôture mensuelle) enregistre :

- utilisateur ;
- date ;
- statut avant / après ;
- message dans le chatter du document.

---

# Annexe — Matrice RACI

## A.1 Rôles

| Rôle | Description |
|---|---|
| CA | Conseil d’Administration |
| Président / Bureau | Gouvernance associative |
| Gestionnaire | Personne responsable du suivi mensuel |
| Salarié | Personne salariée participant aux activités |
| Bénévole | Personne donnant du temps à l’association |
| Trésorier | Responsable financier associatif |
| Développeur | Personne ou équipe développant le module |
| AMOA | Assistance à maîtrise d’ouvrage / cadrage métier |

## A.2 Matrice RACI

| Action | CA | Bureau | Gestionnaire | Salarié | Bénévole | Trésorier | Développeur | AMOA |
|---|---|---|---|---|---|---|---|---|
| Valider la nomenclature des activités | A | R | C | C | I | C | I | R |
| Valider le plan Financements | A | R | C | I | I | C | I | R |
| Paramétrer les activités | I | C | R | I | I | A | R | C |
| Saisir les factures avec analytique | I | I | R | C | I | A | I | C |
| Ventiler les salaires | I | C | R | C | I | A | I | C |
| Déclarer les heures bénévoles | I | I | I | C | R | I | I | C |
| Contrôler les déclarations bénévoles | I | C | R | C | C | A | I | C |
| Saisir le registre bénévole | I | I | R | R | C | A | I | C |
| Générer le rapport mensuel | I | C | R | I | I | A | I | C |
| Lire et commenter le rapport | R | R | C | I | I | A | I | C |
| Arbitrer les décisions de gestion | A | R | C | I | I | C | I | C |
| Faire évoluer le module | C | C | C | C | I | C | R | A |

## A.3 Légende RACI

| Lettre | Signification |
|---|---|
| R | Responsible — réalise l’action |
| A | Accountable — porte la responsabilité finale |
| C | Consulted — consulté avant décision |
| I | Informed — informé |

---

# Décision de référence V1

La V1.1 du module **Suivi d’activité GLC** doit permettre de passer d’une lecture comptable analytique partielle à une lecture de gestion par activité.

Le principe central est :

> **Une activité doit porter son vrai coût : dépenses directes, salaires consommés et bénévolat mobilisé.**

Le Conseil d’Administration doit pouvoir décider à partir d’une vision complète, et non à partir de soldes bruts incomplets.

**Documents associés obligatoires :**

- [Règles d’affectation analytique](./REGLES_AFFECTATION.md)
- [Matrice de migration analytique](./MATRICE_MIGRATION.md)
