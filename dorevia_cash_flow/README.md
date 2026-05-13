# Dorevia Cash Flow

## Objectif

Le module `dorevia_cash_flow` ajoute un rapport graphique de **trajectoire de trésorerie** dans Odoo.

Il répond à cette question :

> Comment la trésorerie a-t-elle évolué depuis le début de l’exercice, et où va-t-elle sur les **90 prochains jours** à partir de la **date de situation** de la **projection de référence** (Cash Guard) ?

Le rapport permet de lire **une seule trajectoire** : à chaque date, **le solde de trésorerie** (`balance`). Les champs **constaté / projeté** (`segment`) qualifient **le segment** de cette même courbe (avant / après la date de situation), et ne doivent **pas** être lus comme deux trajectoires parallèles ni complétés par des zéros hors plage.

- la trésorerie constatée depuis le début de l’exercice ;
- la suite projetée sur l’horizon défini ;
- les points bas ;
- les périodes de vigilance ou de tension.

Ce module ne crée **pas** un nouveau moteur de projection de trésorerie.  
Il fournit une **vue graphique d’analyse**, en combinant les données comptables constatées et les lignes **déjà produites** par les **Projections de trésorerie** (module `dorevia_cash_guard` et dépendances éventuelles).

---

## Vocabulaire produit

| Libellé | Signification |
| --- | --- |
| **Projections de trésorerie** | Le module / l’écran opérationnel qui produit et maintient les données de projection (`dorevia_cash_guard`, etc.). |
| **Trajectoire de trésorerie** | Le rapport graphique fourni par `dorevia_cash_flow` : lecture d’analyse, distincte de l’écran de saisie ou de recalcul de projection. |

Cette distinction évite de confondre l’outil opérationnel de projection avec la vue d’analyse graphique.

**Doctrine transverse (Cash Guard / Cash Flow / simulation)** : voir **[Doctrine modules Cash](../docs/cash/DOCTRINE_CASH_MODULES.md)** dans ce dépôt.

---

## Menu cible

**Parcours principal (pilotage cash)** — même courbe, même moteur :

**Comptabilité > Projection > Trésorerie > Accueil graphique**

**Doctrine** : la **projection de trésorerie de référence** doit être une **donnée système** préparée côté Cash Guard (pas un prérequis « choisir un document » pour l’utilisateur métier) — voir **`../../docs/cash/DOCTRINE_CASH_MODULES.md`** (§ *Projection de référence système*) et **`dorevia_cash_guard/docs/TICKET_CASH_GUARD_SYSTEM_REFERENCE_PROJECTION.md`**. Tant que ce mécanisme n’est pas livré, la résolution repose sur l’heuristique documentée en SPEC § 5.5.

Lecture de la **trajectoire de référence** en **lecture seule** sur le graphique, avec raccourcis atelier (ouvrir la projection, actualiser le calcul, liste des projections, audit autre projection, ouverture de la vue Analyse).  
La déclaration XML de ce menu vit dans **`dorevia_cash_flow`** (`views/cash_guard_bridge_menus.xml`) : le module dépend déjà de `dorevia_cash_guard`, ce qui évite une dépendance circulaire.

**Atelier** (documents de projection) :

**Comptabilité > Projection > Trésorerie > Projections de trésorerie**

### Raccourcis sous Analyse (secondaire)

Les mêmes actions restent disponibles sous **Comptabilité > Analyse** (souvent avec un sous-menu intermédiaire *Gestion* selon la base), avec des libellés explicites pour éviter une double porte « principale » sans contexte :

- **Trajectoire (Analyse)** — ouverture directe du graphique de référence (équivalent V1.1) ;
- **Trajectoire — choix projection (Analyse)** — assistant de sélection.

Libellé anglais possible (Reporting) : à aligner sur la traduction des menus `account`.

### V1.1 — Parcours nominal (trajectoire de référence)

Depuis la **V1.1**, l’entrée **Accueil graphique** (Projection) ou **Trajectoire (Analyse)** ouvre **directement** le graphique de pilotage pour la **société courante** : le module choisit automatiquement une projection Cash Guard **active**, **hebdomadaire**, avec **mailles calculées**, la plus récente au sens de la **date de situation** (`situation_date` décroissante). Aucune sélection manuelle n’est requise dans ce parcours.

- **Parcours secondaire** : menu **Trajectoire — choix projection (Analyse)** ou bouton **Changer de projection** sur le graphique (hors mode accueil graphique) pour cibler un autre document (audit, comparaison).
- **Données manquantes** : message explicite invitant à créer ou actualiser une projection dans **Projection > Trésorerie > Projections de trésorerie** (sans recalcul automatique déclenché par Cash Flow).

## Intention fonctionnelle

La courbe représente **une seule trajectoire** : en ordonnée, le **solde de trésorerie** à la date considérée ; le constaté et le projeté sont deux **segments successifs** de cette trajectoire (repère : date de situation), et non deux courbes concurrentes.

La lecture attendue est une courbe simple :

- axe X : semaines ;
- axe Y : montant de trésorerie ;
- granularité : hebdomadaire ;
- période couverte par la courbe : du **début de l’exercice comptable courant** jusqu’à **date de situation + 90 jours** (aligné sur l’horizon standard des **Projections de trésorerie**).

La courbe doit permettre d’identifier rapidement :

- la tendance globale ;
- les points bas ;
- les périodes de vigilance ;
- les périodes de tension ou de risque ;
- l’effet de la projection sur la trésorerie future.

---

## Périmètre fonctionnel (V1 / V1.1)

Le rapport doit rester simple, lisible et robuste.

### Parcours principal (V1.1)

1. ouvrir **Comptabilité > Projection > Trésorerie > Accueil graphique** (parcours nominal) **ou** **Comptabilité > Analyse > … > Trajectoire (Analyse)** (raccourci secondaire) ;
2. voir **directement** la courbe de trajectoire de **référence** pour la société courante (projection résolue automatiquement) ;
3. lire date de situation, seuil, point bas et segments constaté / projeté sur le graphique de pilotage.

### Parcours secondaire

- Menu **Trajectoire — choix projection (Analyse)** ou bouton **Changer de projection** : sélection explicite d’une projection puis **Afficher la trajectoire** (comportement historique V1).

### Lecture attendue (inchangé)

Le rapport permet aussi de :

- visualiser une courbe semaine / montant ;
- identifier le segment **constaté** puis **projeté** sur la même courbe (repères sur le graphique de pilotage ; détail dans la **liste** des points — voir `docs/RECETTE_VUE_GRAPH.md`) ;
- identifier le point bas et les périodes de tension ;
- afficher le seuil d’alerte lorsque la projection le fournit.

## Date de bascule constaté / projeté

La date de bascule entre le **constaté** et le **projeté** est la **date de situation** (`situation_date`) de la projection **utilisée** (référence automatique ou projection choisie en parcours secondaire).

La trajectoire graphique se compose de deux segments :

### 1. Période constatée

- du **début de l’exercice comptable courant** ;
- jusqu’à la **date de situation** (incluse ou borne selon convention d’affichage retenue en implémentation).

Cette partie s’appuie sur les **soldes réels** de trésorerie issus des **journaux** suivis par la projection (banque / caisse), comme pour le constaté dans **Projections de trésorerie**.

### 2. Période projetée

Règle métier V1 :

> La partie projetée couvre la période allant de la **date de situation** jusqu’à **date de situation + 90 jours**.

C’est l’**horizon standard** aligné sur les **Projections de trésorerie** (Cash Guard).  
Si le modèle expose déjà un champ technique de fin de période **équivalent** à cette règle (par ex. `date_to` recalé sur situation + 90 jours), l’implémentation peut s’y appuyer ; le README documente la **règle métier** : **situation + 90 jours**.

Cette partie s’appuie sur les **lignes déjà produites** par la projection (mailles hebdomadaires, etc.), **sans recalcul** dans `dorevia_cash_flow`.

Pour chaque semaine du segment projeté, le graphique reprend le montant déjà disponible dans les lignes de projection.

---

## Principe d’architecture

`dorevia_cash_flow` ne doit **pas** recalculer la trésorerie de manière indépendante.

Règle synthétique :

> **Cash Guard** calcule la projection.  
> Un **module de simulation** peut enrichir la projection en amont.  
> **Cash Flow** affiche la **trajectoire** de la projection de **référence** (ou choisie en parcours secondaire), telle que les données existent dans les lignes.

Le module restitue graphiquement une trajectoire combinant :

- le constaté comptable / bancaire ;
- le projeté **déjà calculé** ailleurs.

---

## Comportement attendu

Depuis **Projection > Trésorerie > Accueil graphique** ou **Trajectoire (Analyse)**, l’utilisateur obtient la **trajectoire de référence** (V1.1) ou, via le menu secondaire **Trajectoire — choix projection (Analyse)**, ouvre un assistant pour **choisir** une projection puis afficher la courbe.

La courbe doit afficher :

- les semaines en abscisse ;
- le montant de trésorerie en ordonnée ;
- la partie constatée ;
- la partie projetée ;
- le point bas de trésorerie sur la période affichée ;
- le seuil d’alerte si les données de la projection le permettent.

La distinction constaté / projeté peut être visuelle (trait plein / pointillé, couleurs, ligne verticale à la **date de situation**, etc.) — la décision graphique exacte peut rester simple en V1.

---

## Données réelles et données projetées

| Zone | Nature | Source |
| --- | --- | --- |
| Constaté | Données réelles | Soldes issus des journaux de trésorerie suivis |
| Projeté | Données déjà calculées | Lignes produites par **Projections de trésorerie** |

---

## Lecture métier attendue

Le rapport doit permettre de visualiser :

- le démarrage de l’exercice ;
- l’évolution de la trésorerie **jusqu’à la date de situation** ;
- la projection **sur les 90 jours** suivant la date de situation ;
- si la trajectoire reste au-dessus du seuil d’alerte (lorsque affiché) ;
- à quelle semaine apparaît le point bas ;
- si la tendance est stable, favorable ou préoccupante.

---

## Hors périmètre V1

Ne pas intégrer dans cette première version :

- nouveau moteur de projection ;
- recalcul complet et indépendant de trésorerie ;
- **logique métier ou interface de simulation** dans `dorevia_cash_flow` (pas de sélection de devis / commandes, pas de comparaison réel / simulé, pas de multi-courbes de scénarios, pas de retraitement des hypothèses — la simulation reste dans les modules dédiés) ;
- dashboard complexe ;
- reporting budgétaire ;
- analyse multi-scénarios avancée ;
- comparaison de plusieurs projections ;
- consolidation multi-sociétés ;
- modification du fonctionnement du module **Projections de trésorerie** ;
- création d’un nouveau workflow métier.

**Note** : si la projection sélectionnée contient déjà des montants issus d’autres modules (y compris simulation), `dorevia_cash_flow` peut les **restituer tels qu’ils figurent** dans les lignes de projection, **sans les recalculer ni les interpréter**. Hors périmètre = **aucune logique propre** à la simulation **dans** ce module.

---

## Critères de recette

Le module `dorevia_cash_flow` est installable sans erreur.

Les entrées **Projection > Trésorerie > Accueil graphique** et **Analyse > … > Trajectoire (Analyse)** ouvrent directement le graphique de référence (V1.1).

Un second menu sous Analyse, **Trajectoire — choix projection (Analyse)**, permet le parcours avec sélection manuelle.

La trajectoire de référence s’appuie sur une projection Cash Guard **résolue automatiquement** (société courante, active, hebdomadaire, mailles présentes, `situation_date` la plus récente).

La courbe démarre au début de l’exercice comptable courant.

L’horizon affiché respecte la règle métier **date de situation → date de situation + 90 jours** pour le segment projeté (implémentation alignée sur les données Cash Guard).

La bascule constaté / projeté est lisible à la **date de situation**.

Les montants projetés correspondent aux lignes de projection existantes.

Le rapport permet d’identifier le point bas sur la période affichée.

Le module ne modifie pas le comportement des **Projections de trésorerie**.

---

## Implémentation technique (V1)

Le code du module est livré dans ce dépôt (`dorevia_cash_flow`). La conception détaillée est dans **`docs/SPEC_CASH_FLOW_TRAJECTORY.md`**. Le **rendu cible** (une courbe, repères visuels, limites du graph natif, priorité V1, confirmation V2) est décrit dans **`docs/RECETTE_VUE_GRAPH.md`**.

Le menu d’accès est rattaché au menu standard comptable **`account.menu_finance_reports`** (souvent intitulé *Reporting* ou *Analyse* selon la langue).

---

## Livraison V1 / V1.1 (clôture fonctionnelle)

**Décision** : **GO V1** (recette initiale 2026-05-13) puis **GO V1.1** (relance recette après lecture module — même jour, run **`RECETTE CASH FLOW V1 20260513-002`**).

Documents et preuves conservés dans le dépôt :

| Rôle | Fichier |
| --- | --- |
| Cadrage produit (ce README) | `README.md` |
| Spécification technique | `docs/SPEC_CASH_FLOW_TRAJECTORY.md` |
| Scénario de recette manuelle | `docs/RECETTE_MANUELLE_V1.md` |
| Procès-verbal de recette | `docs/PV_RECETTE_MANUELLE_V1.md` |
| Recette fonctionnelle (checklist étendue) | `docs/RECETTE_FONCTIONNELLE_V1.md` |
| Limites vue Graph native | `docs/RECETTE_VUE_GRAPH.md` |
| Ticket V1.1 (cadrage) | `docs/TICKET_CASH_FLOW_V1_1_TRAJECTOIRE_REFERENCE.md` |
| Doctrine modules Cash (transverse, dépôt) | `../docs/cash/DOCTRINE_CASH_MODULES.md` |
| Capture de preuve V1.1 (terrain) | `docs/captures/recette_cash_flow_trajectory_20260513_002.png` |

La capture **`recette_cash_flow_trajectory_20260513.png`** (V1) peut rester comme archive si présente ; la preuve **V1.1** attendue dans le dépôt est le fichier **`_002`** référencé dans le PV.

**Hors périmètre reporté** (évolutions ultérieures) : enrichissements graphiques avancés, comparaison N-1 / N-2, exports dédiés, intégration plus poussée avec Cash Guard — à traiter dans des livraisons séparées.

---

## Convention de nommage

Module technique :

```text
dorevia_cash_flow
```
