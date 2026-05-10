# dorevia_cash_guard

Module Odoo 19 CE — **Sécurité Trésorerie**

**Environnement de recette de référence** : URL `http://localhost:18079`, base PostgreSQL **`tenant_o8`** (lettre **o**, pas `tenant_08`), module `dorevia_cash_guard`. Les commandes `docker compose` se lancent depuis le dossier du stack où se trouve **`docker-compose.yml`** (ex. `~/sandbox-odoo19` ; adapter le chemin). Détail et parcours manuel V1.1 : `docs/SCENARIO_MANUEL_V1_1_HEBDO.md`.

## 1. Objectif

`dorevia_cash_guard` est un module de projection de trésorerie destiné à anticiper les tensions de cash avant qu’elles ne deviennent critiques.

Le module répond à une question simple :

> Est-ce que la trésorerie restera positive sur la période à venir ?

Il permet notamment de vérifier à l’avance si l’entreprise ou l’association pourra couvrir ses échéances critiques :

- salaires ;
- charges sociales ;
- fournisseurs ;
- loyers ;
- impôts / taxes ;
- remboursements ;
- grosses dépenses envisagées.

Le principe directeur est simple :

> Ne jamais découvrir trop tard une tension de trésorerie.

---

## 2. Nom métier

| Élément | Valeur |
|---|---|
| Module technique | `dorevia_cash_guard` |
| Entrée menu (racine Comptabilité) | Prévision de trésorerie |
| Objet principal | Point de trésorerie |
| Lignes | Flux prévisionnels |
| Référentiel pivot | Postes budgétaires |

---

## 3. Positionnement

Le module ne remplace pas la comptabilité générale.

Il s’appuie sur les écritures comptables, les postes budgétaires et le rapprochement bancaire pour produire une lecture de trésorerie prévisionnelle.

Le module ajoute une couche de pilotage :

- projection datée des flux ;
- calcul du solde futur ;
- identification du solde minimum ;
- alerte si passage sous zéro ;
- seuil d’alerte de gestion ;
- simulation d’hypothèses ;
- comparaison prévu / réalisé.

Phrase de cadrage :

> La comptabilité donne le réel. `dorevia_cash_guard` ajoute la projection, l’alerte et l’aide à la décision.

---

## 4. Dépendances

Le module dépend de :

```text
account
base_account_budget
base_accounting_kit
mail
```

- **`account`** : comptabilité (écritures, journaux, soldes).
- **`base_account_budget`** : postes budgétaires réutilisés comme pivot des flux.
- **`base_accounting_kit`** : socle comptable / UX attendu sur les instances Dorevia qui livrent Cash Guard avec ce kit (ordre de chargement et cohérence menu).
- **`mail`** : fil de discussion et activités sur les points de trésorerie.

Modèles réutilisés :

| Modèle | Usage |
| --- | --- |
| `account.budget.post` | poste budgétaire pivot |
| `account.budget.post.account_ids` | comptes comptables associés au poste |
| `budget.budget` | enveloppe budgétaire éventuelle |
| `budget.lines` | ligne budgétaire optionnelle |
| `account.analytic.account` | projet, action ou centre analytique |

Décision importante :

> Le module ne crée pas un référentiel séparé de postes de trésorerie. Il réutilise les postes budgétaires.

---

## 5. Doctrine de prudence

Une projection de trésorerie négative ne constitue pas automatiquement une situation juridique de cessation des paiements.

Dans `dorevia_cash_guard`, un passage prévisionnel sous zéro est traité comme une **alerte de gestion**.

Le module ne qualifie pas juridiquement la situation de l’entreprise ou de l’association.

Il ne doit donc pas afficher automatiquement de message du type :

> dépôt de bilan

ou :

> cessation des paiements

Le module doit afficher des statuts de pilotage :

| Statut | Signification |
| --- | --- |
| Sécurisé | la trésorerie reste au-dessus du seuil d’alerte |
| Vigilance | la trésorerie reste positive mais passe sous le seuil d’alerte |
| Risque | un passage sous zéro est prévu |

Formulation retenue :

> Une alerte de trésorerie négative est un signal de pilotage. Elle doit déclencher une action de gestion avant que la situation ne devienne critique.

---

## 6. Inspiration OCA

Le module s’inspire conceptuellement de `mis_builder_cash_flow` côté OCA, notamment pour l’idée suivante :

> unifier les écritures comptables ouvertes et les lignes prévisionnelles manuelles dans une même lecture datée.

Cependant, `dorevia_cash_guard` ne dépend pas de `mis_builder_cash_flow` ni de MIS Builder.

Raisons :

- module OCA disponible en 18.0, non retenu comme base Odoo 19 CE ;
- forte dépendance à MIS Builder ;
- absence de pivot `account.budget.post` ;
- absence de seuil d’alerte métier ;
- absence de simulation ;
- absence de logique spécifique de garde-fou trésorerie ;
- besoin d’un modèle Dorevia maîtrisé.

Décision :

> Inspiration seulement, pas de dépendance technique.

---

## 7. Concepts fonctionnels

### 7.1 Point de trésorerie

Un point de trésorerie représente une projection sur une période.

Exemple :

```text
Point trésorerie — Mai 2026
```

Il contient :

- une période de projection ;
- un journal bancaire ;
- un solde initial calculé ;
- un seuil d’alerte ;
- des flux prévisionnels ;
- un solde final prévu ;
- un solde minimum prévu ;
- un statut de risque.

---

### 7.2 Flux prévisionnel

Un flux prévisionnel représente une entrée ou une sortie datée.

Exemples :

| Date | Poste budgétaire | Type | Montant |
| --- | --- | --- | ---: |
| 15/05/2026 | Subventions | Entrée prévue | +5 000 € |
| 25/05/2026 | Fournisseurs | Sortie prévue | -1 200 € |
| 31/05/2026 | Salaires | Sortie prévue | -6 500 € |

---

### 7.3 Poste budgétaire

Le poste budgétaire est le pivot entre :

- budget ;
- comptabilité ;
- trésorerie ;
- rapprochement bancaire ;
- graphique ;
- comparaison prévu / réalisé.

Exemple :

```text
Poste budgétaire : Salaires
Comptes associés : 421, 641
Sens courant : sortie
```

Le poste budgétaire permet de classer les flux avec une lecture métier stable.

Il devient le point de jonction entre :

```text
Budget
→ comptes comptables
→ écritures comptables
→ flux prévisionnels
→ paiements rapprochés
→ analyse prévu / réalisé
```

---

### 7.4 Nomenclature initiale des postes budgétaires

Le module peut proposer une nomenclature initiale de **20 postes budgétaires**.

Cette nomenclature sert de point de départ pour structurer :

- les projections de trésorerie ;
- les analyses graphiques ;
- les comparaisons prévu / réalisé ;
- les lectures par poste dans les points de trésorerie.

Elle n’est pas figée.

Les utilisateurs habilités peuvent :

- archiver les postes inutiles ;
- créer de nouveaux postes ;
- renommer certains postes ;
- réordonner l’affichage ;
- ajuster les comptes comptables associés.

Règle de gestion :

> Un poste budgétaire déjà utilisé ne doit pas être supprimé. Il doit être archivé afin de préserver l’historique.

#### Entrées

| N° | Poste budgétaire | Sens cash | Exemple |
| -: | --- | --- | --- |
| 1 | Subventions publiques | Entrée | mairie, région, collectivité |
| 2 | Subventions privées / mécénat | Entrée | fondation, entreprise mécène |
| 3 | Cotisations / adhésions | Entrée | adhésions membres |
| 4 | Dons / participations libres | Entrée | dons, contributions libres |
| 5 | Recettes d’activité | Entrée | ventes, ateliers, prestations |
| 6 | Billetterie / événements | Entrée | entrées événement, inscriptions |
| 7 | Remboursements reçus | Entrée | remboursement assurance, avoir fournisseur |
| 8 | Autres entrées | Entrée | produits divers non classés |

#### Sorties

| N° | Poste budgétaire | Sens cash | Exemple |
| -: | --- | --- | --- |
| 9 | Salaires nets | Sortie | paie salariés |
| 10 | Charges sociales | Sortie | URSSAF, caisses, organismes sociaux |
| 11 | Prestations externes | Sortie | intervenants, animation, consultant |
| 12 | Fournisseurs / achats | Sortie | matières, fournitures, marchandises |
| 13 | Loyers / locaux | Sortie | local, salle, charges locatives |
| 14 | Énergie / eau / télécom | Sortie | électricité, eau, internet, téléphone |
| 15 | Assurances | Sortie | responsabilité civile, local, matériel |
| 16 | Communication / marketing | Sortie | flyers, affiches, publicité, graphisme |
| 17 | Déplacements / transport | Sortie | carburant, billets, location véhicule |
| 18 | Impôts / taxes / TVA | Sortie | TVA, taxes, fiscalité |
| 19 | Remboursements / dettes / emprunts | Sortie | prêt, avance, remboursement |
| 20 | Autres sorties | Sortie | charges diverses non classées |

---

### 7.5 Seuil d’alerte

Le seuil d’alerte est une donnée de gestion saisie manuellement.

Il représente le niveau minimal acceptable de trésorerie.

Exemple :

```text
Seuil d’alerte : 5 000 €
```

Ce seuil ne vient pas de la comptabilité.
Il correspond à un consensus de gestion.

Le seuil permet de distinguer une situation simplement positive d’une situation réellement confortable.

---

### 7.6 Simulation

Une ligne simulée permet de tester l’impact d’une décision sans créer d’écriture comptable.

Exemple :

```text
Simulation : achat matériel — 8 000 € — 20/06/2026
```

Une simulation sert à répondre à la question :

> Si j’engage cette dépense, est-ce que je passe sous le seuil ou sous zéro ?

Une ligne simulée :

- ne crée aucune écriture comptable ;
- peut être incluse ou exclue de la projection ;
- peut devenir une ligne prévue si la décision est retenue ;
- sert uniquement à mesurer un impact de gestion.

---

## 8. Règles métier

### 8.1 Solde initial

Le solde initial ne doit pas être saisi manuellement dans le fonctionnement normal.

Il est calculé à partir du journal bancaire sélectionné et des écritures comptables à la date de début du point.

```text
Solde initial = solde comptable du journal bancaire à la date de début
```

Le module doit éviter de recréer une logique de tableur dans Odoo.

---

### 8.2 Projection

Les flux sont ordonnés par date.

Après chaque flux, le module calcule un nouveau solde prévisionnel.

```text
Solde initial
+ entrées prévues datées
- sorties prévues datées
= solde prévisionnel
```

Les lignes sont triées par :

```text
projection_date ASC
sequence ASC
id ASC
```

---

### 8.3 Solde minimum

Le module identifie le solde le plus bas atteint sur la période.

```text
Solde minimum prévu = point bas de la projection
```

C’est l’indicateur central du module.

Le solde final peut être positif alors qu’un passage sous zéro est prévu en cours de période.

Le module doit donc alerter sur le **solde minimum**, pas seulement sur le solde final.

---

### 8.4 Statut de risque

Le statut est calculé à partir du solde minimum et du seuil d’alerte.

| Condition | Statut |
| --- | --- |
| Solde minimum < 0 | Risque |
| Solde minimum >= 0 et < seuil d’alerte | Vigilance |
| Solde minimum >= seuil d’alerte | Sécurisé |

---

### 8.5 Réalisé cash

Le réalisé cash fiable vient prioritairement du rapprochement bancaire.

Niveaux possibles :

| Niveau | Sens |
| --- | --- |
| Prévu | flux anticipé |
| Comptabilisé | facture, OD ou écriture existante |
| Paiement saisi | paiement enregistré dans Odoo |
| Rapproché | confirmé par mouvement bancaire rapproché |
| Écart | réalisé différent du prévu |
| Annulé | flux abandonné |

Le module ne doit pas confondre :

- une facture comptabilisée ;
- une dette ou créance ouverte ;
- un paiement saisi ;
- un mouvement bancaire rapproché.

Le niveau le plus fiable du réalisé cash est le mouvement bancaire rapproché.

---

### 8.6 Prévu / réalisé

Après la période, le module doit permettre de comparer :

```text
prévu vs réalisé bancaire rapproché
```

Exemple :

| Poste | Prévu | Réalisé | Écart |
| --- | ---: | ---: | ---: |
| Salaires | -6 500 € | -6 720 € | -220 € |
| Subventions | +5 000 € | +5 000 € | 0 € |
| Fournisseurs | -1 200 € | -1 350 € | -150 € |

Cette comparaison permet d’améliorer les projections suivantes.

---

### 8.7 Paiements suivis

Le module suit les paiements et encaissements prévus puis réalisés.

Il suit notamment :

- ce qui doit être payé ;
- ce qui doit être encaissé ;
- la date prévue de paiement ou d’encaissement ;
- la date réelle si le flux est rapproché ;
- l’écart entre prévu et réalisé.

La trésorerie n’est pas seulement ce qui est dû : c’est ce qui entre ou sort réellement de la banque.

---

## 9. Modèles prévus

### 9.1 `dorevia.cash.guard`

Objet principal : **Point de trésorerie**

Champs pressentis :

| Champ | Type | Description |
| --- | --- | --- |
| `name` | Char | Nom du point de trésorerie |
| `date_from` | Date | Début de période |
| `date_to` | Date | Horizon de projection |
| `bank_journal_id` | Many2one `account.journal` | Journal bancaire suivi |
| `company_id` | Many2one `res.company` | Société |
| `currency_id` | Many2one `res.currency` | Devise |
| `alert_threshold` | Monetary | Seuil d’alerte |
| `initial_balance` | Monetary | Solde initial calculé |
| `forecast_final_balance` | Monetary | Solde final prévu |
| `forecast_min_balance` | Monetary | Solde minimum prévu |
| `min_balance_date` | Date | Date du point bas |
| `risk_status` | Selection | sécurisé / vigilance / risque |
| `state` | Selection | brouillon / validé / clôturé |
| `responsible_id` | Many2one `res.users` | Responsable |
| `note` | Text | Commentaire |

---

### 9.2 `dorevia.cash.guard.line`

Objet : **Flux prévisionnel**

Champs pressentis :

| Champ | Type | Description |
| --- | --- | --- |
| `guard_id` | Many2one `dorevia.cash.guard` | Point de trésorerie |
| `projection_date` | Date | Date prévue du flux |
| `budget_post_id` | Many2one `account.budget.post` | Poste budgétaire |
| `budget_line_id` | Many2one `budget.lines` | Ligne budgétaire optionnelle |
| `analytic_account_id` | Many2one `account.analytic.account` | Projet / action |
| `direction` | Selection | entrée / sortie |
| `line_type` | Selection | prévu / simulé |
| `label` | Char | Libellé métier |
| `projected_amount` | Monetary | Montant prévu |
| `realized_amount` | Monetary | Montant réalisé |
| `variance_amount` | Monetary | Écart prévu / réalisé |
| `balance_after_line` | Monetary | Solde après ligne |
| `partner_id` | Many2one `res.partner` | Partenaire |
| `source_move_id` | Many2one `account.move` | Facture ou OD source |
| `source_move_line_id` | Many2one `account.move.line` | Ligne comptable source |
| `bank_move_line_id` | Many2one `account.move.line` | Ligne bancaire rapprochée |
| `certainty` | Selection | certain / confirmé / incertain |
| `priority` | Selection | obligatoire / reportable |
| `cash_state` | Selection | prévu / comptabilisé / payé_saisi / rapproché / écart / annulé |
| `sequence` | Integer | Ordre secondaire de projection |
| `note` | Text | Commentaire |

Règle de lecture :

- `line_type` décrit la nature de la ligne (prévue ou simulée) ;
- `cash_state` décrit son niveau d’avancement dans le cycle de réalisation.

Exemples :

```text
line_type = prévu
cash_state = rapproché
```

```text
line_type = simulé
cash_state = prévu
```

---

## 10. Visualisation graphique

Le graphique principal est un histogramme mensuel par poste budgétaire.

### Axes

| Axe | Donnée |
| --- | --- |
| X | Mois |
| Y | Montants |
| Séries | Postes budgétaires |

### Lecture

- les entrées sont affichées en positif ;
- les sorties sont affichées en négatif ;
- les données sont regroupées par mois et poste budgétaire.

### Modes possibles

| Mode | Usage |
| --- | --- |
| Prévu | projection |
| Réalisé | après rapprochement bancaire |
| Écart | comparaison prévu / réalisé |
| Simulation | impact des hypothèses |

Le graphique doit permettre d’identifier rapidement :

- les postes qui pèsent le plus sur la trésorerie ;
- les mois de tension ;
- le poids des salaires et charges sociales ;
- les écarts entre prévu et réalisé ;
- l’impact d’une hypothèse simulée.

---

## 11. Exemple de projection

| Date | Poste budgétaire | Libellé | Entrée | Sortie | Solde prévu |
| --- | --- | --- | ---: | ---: | ---: |
| 01/05/2026 | — | Solde initial Banque |  |  | 18 400 € |
| 15/05/2026 | Fournisseurs | Paiement fournisseur |  | 4 800 € | 13 600 € |
| 25/05/2026 | Recettes d’activité | Encaissement prévu | 6 000 € |  | 19 600 € |
| 31/05/2026 | Salaires | Paie mensuelle |  | 9 000 € | 10 600 € |
| 05/06/2026 | Charges sociales | Échéance sociale |  | 7 400 € | 3 200 € |

Synthèse :

| Indicateur | Montant |
| --- | ---: |
| Solde initial | 18 400 € |
| Solde final prévu | 3 200 € |
| Solde minimum prévu | 3 200 € |
| Seuil d’alerte | 5 000 € |
| Statut | Vigilance |

---

## 12. Périmètre V1

### Inclus

- création d’un point de trésorerie ;
- sélection d’un journal bancaire ;
- calcul du solde initial depuis la comptabilité ;
- saisie du seuil d’alerte ;
- réutilisation des postes budgétaires ;
- initialisation optionnelle d’une nomenclature de 20 postes budgétaires standards ;
- possibilité d’archiver, renommer ou compléter les postes selon les besoins de gestion ;
- création de flux prévisionnels ;
- création de lignes simulées ;
- calcul du solde après chaque flux ;
- calcul du solde minimum ;
- statut sécurisé / vigilance / risque ;
- comparaison simple prévu / réalisé ;
- graphique mensuel par poste budgétaire en V1.1, sauf si rapide via vue graph standard Odoo.

### Exclu V1

- dépendance à MIS Builder ;
- dépendance à `mis_builder_cash_flow` ;
- matching intelligent automatique ;
- alertes email ;
- scénarios complexes multi-hypothèses ;
- interface LYNKR dédiée ;
- intégration Dorevia Vault ;
- recommandations IA ;
- qualification juridique automatique de type cessation des paiements.

---

## 13. Critères de recette V1

Le module est validé si :

| Critère | Attendu |
| --- | --- |
| Créer un point de trésorerie | OK |
| Définir une période | OK |
| Choisir un journal bancaire | OK |
| Calculer le solde initial | OK |
| Saisir un seuil d’alerte | OK |
| Ajouter une ligne prévue | OK |
| Ajouter une ligne simulée | OK |
| Associer une ligne à un poste budgétaire | OK |
| Archiver un poste budgétaire inutilisé | OK |
| Créer un nouveau poste budgétaire si besoin | OK |
| Calculer le solde après chaque ligne | OK |
| Identifier le solde minimum | OK |
| Déclencher un statut Risque si solde minimum < 0 | OK |
| Déclencher un statut Vigilance si solde minimum < seuil | OK |
| Déclencher un statut Sécurisé si solde minimum >= seuil | OK |
| Comparer prévu / réalisé simple | OK |
| Afficher une analyse par poste budgétaire | OK |
| Ne jamais afficher automatiquement “dépôt de bilan” ou “cessation des paiements” | OK |

---

## 14. Évolutions prévues

### V1.1

- graphique mensuel consolidé ;
- amélioration de la comparaison prévu / réalisé ;
- meilleur rattachement aux écritures bancaires rapprochées ;
- vue de synthèse par poste budgétaire.

### V2

- génération semi-automatique des flux depuis factures, OD et écritures ouvertes ;
- rapprochement assisté prévu / réalisé ;
- scénarios de simulation ;
- alertes ;
- restitution LYNKR.

### V3

- intégration Dorevia Vault ;
- scellement des points de trésorerie validés ;
- preuve des décisions ;
- analyse des écarts historiques ;
- aide à la décision augmentée.

---

## 15. Doctrine

`dorevia_cash_guard` est une brique de pilotage.

Elle relie :

```text
Budget
→ Comptabilité
→ Rapprochement bancaire
→ Trésorerie prévisionnelle
→ Simulation
→ Décision
```

Le pivot commun est :

```text
account.budget.post
```

Phrase produit :

> Sécurité Trésorerie permet de projeter le solde bancaire futur à partir des écritures comptables et des postes budgétaires, afin d’anticiper les tensions de trésorerie, sécuriser les échéances critiques et simuler l’impact des décisions avant de les engager.