# Cadrage — Budget prévisionnel & Cockpit de soutenabilité GLC


> **Document historique** — ne décrit plus le produit installé depuis **`19.0.13.0.0`** / **`19.0.14.0.0`**. État actuel : [ETAT_MODULE_ACTUEL.md](./ETAT_MODULE_ACTUEL.md).

---

**Date :** 2026-05-27  
**Contexte :** suite Palier 2 validé MOA · module socle `dorevia_glc_analytics` · base recette `glc-rgl-test-import`

---

## Contexte technique

Le module socle est désormais nommé techniquement :

```text
dorevia_glc_analytics
```

(ancien nom : `dorevia_glc_analytique`)

**Palier 2** validé MOA en version **`19.0.3.0.0`** sur `glc-rgl-test-import` — **gelé** après merge PR #26.

Le Palier 2 valide notamment :

- coûts salariés mensuels ;
- ventilations salariales par activité ;
- méthodes `percent` et `hours` ;
- contrôles métier associés ;
- refus des comptes de financement dans les ventilations ;
- bandeau d’écart masse comptable (informatif) ;
- absence d’écriture comptable à la validation ;
- non-régression Palier 1 ;
- correction du domaine multi-société sur `activity_account_id`.

---

## Besoin métier central

La suite ne doit **pas** être pensée comme un simple rapport analytique.

GLC a besoin d’un **cockpit de soutenabilité économique** pour répondre à la question :

> **Génère-t-on assez de recettes pour couvrir les salaires ?**

Puis, en second niveau :

> **Les recettes d’activité et les subventions couvrent-elles aussi les frais généraux et les charges fixes ?**

Phrase cible MOA :

> **Je veux comprendre en un coup d’œil, mois par mois, comment se comportent Bar & Restau, Prestation & Animation, Privatisation Espace, RH / Personnel, Frais généraux, Résidence artiste et Déplacement & Mission, et comment évolue le solde global.**

Cœur du besoin :

```text
Activité × Mois × Produits / Charges / Solde
```

Couche de pilotage supérieure :

```text
Couverture des salaires
Couverture salaires + frais généraux
Écart prévu / réalisé
Alerte de gestion
```

---

## Doctrine validée

### 1. Compte comptable = nature

| Compte | Nature |
|---|---|
| `706` | Ventes de prestations |
| `707` | Ventes de marchandises |
| `641` | Salaires |
| `645` | Charges sociales |
| `626` | Télécom |
| `625` | Missions, déplacements, réceptions |
| `74` | Subventions d’exploitation |
| `164` | Emprunts / dette financière |
| `512` / `53` | Trésorerie / caisse — trace du flux |
| `580` | Virements internes |

### 2. Compte analytique = activité / destination métier

Exemples : Bar & Restau · Prestation & Animation · Privatisation Espace · RH / Personnel · Frais généraux · Résidence artiste · Déplacement & Mission · Subvention d’exploitation · Adhésions / Financements.

### 3. Compte bancaire de référence = point de vue trésorerie *(décision MOA 2026-05-28)*

Le cockpit GLC est rattaché à un **compte bancaire de référence** (sélectionnable ; défaut GLC : **compte courant**).

| Lecture | Règle |
|---|---|
| Entrée sur le compte de référence | Entrée de trésorerie pour le cockpit |
| Sortie du compte de référence | Sortie de trésorerie pour le cockpit |
| Virement interne impliquant ce compte | Visible comme mouvement trésorerie du compte observé |
| Virement interne | **Exclu** de recette, charge, marge d’activité et financement économique |

> **Triple lecture :** compte bancaire de référence = point de vue · compte comptable = nature · compte analytique = qualification métier.

Implémentation : Palier 5 — cf. [TICKET_PALIER_5_TRESORERIE_COMPTE_BANCAIRE_REFERENCE.md](./TICKET_PALIER_5_TRESORERIE_COMPTE_BANCAIRE_REFERENCE.md) · doctrine [TICKET_COCKPIT_COMPTE_BANCAIRE_REFERENCE.md](./TICKET_COCKPIT_COMPTE_BANCAIRE_REFERENCE.md).

### 4. Opérations de bilan hors analytique d’exploitation

Ne **pas** alimenter le plan **Activités GLC** :

- remboursement de capital d’emprunt (`164`) ;
- virement interne ;
- mouvement compte courant / livret ;
- reprise de solde ;
- compte de transfert bancaire.

Ces flux impactent la trésorerie (lecture compte bancaire de référence), pas les KPI d’exploitation Ressources · Cumul RH · Dépenses · Solde.

---

## Roadmap après Palier 2

| Palier | Module | Objectif |
|---|---|---|
| **3** | `dorevia_glc_budget` | Budget prévisionnel mensuel simple par axe analytique |
| **4** | `dorevia_glc_analytics` (+ extension cockpit) | Contrôle de gestion : réalisé vs budget vs alertes |
| **5** | enrichissements | Graphiques, exports, scénarios, commentaires, trésorerie |

> **Ne pas démarrer par OCA Budget.** Module léger dédié GLC.

---

## Indicateurs cockpit (Palier 4)

### Ressources

```text
Recettes d’activité = Bar & Restau + Prestation & Animation + Privatisation Espace
Financements = Subvention d’exploitation + Adhésions / autres financements retenus
Ressources disponibles = Recettes d’activité + Financements
```

### Charges clés

```text
Masse salariale = RH / Personnel
Charges fixes = RH / Personnel + Frais généraux
```

Indicateurs : taux de couverture des salaires · solde après salaires · solde après salaires + frais généraux · écart budget / réalisé · tendance mensuelle.

### Alertes de gestion

| Statut | Condition |
|---|---|
| Rouge | Ressources disponibles < RH / Personnel |
| Orange | Ressources ≥ RH / Personnel mais < RH / Personnel + Frais généraux |
| Vert | Ressources ≥ RH / Personnel + Frais généraux |

---

## Sources de données

| Donnée | Source Palier 4 |
|---|---|
| Réalisé | `account.analytic.line` — agrégation mois × compte analytique × société × type flux |
| Prévisionnel | `glc.budget.line` (Palier 3) — agrégation mois × compte analytique × type |

---

## Décision de cadrage MOA

Après validation du Palier 2, la suite du projet GLC est organisée ainsi :

- **Palier 3** : création du module `dorevia_glc_budget`, destiné à saisir un prévisionnel mensuel simple par axe analytique.
- **Palier 4** : création du cockpit de couverture des salaires, croisant réalisé analytique et budget prévisionnel.
- **Palier 5** : enrichissements de pilotage, scénarios, exports, commentaires et éventuel bloc trésorerie.

Le module **`dorevia_glc_analytics`** reste le socle du réalisé analytique, des coûts salariés et des ventilations salariales.

Le besoin central de GLC est de savoir si les recettes d’activité et les subventions d’exploitation couvrent les salaires, puis les frais généraux.

---

## Paliers V1.1 reportés (post-cockpit)

Éléments présents dans la [spec V1.1](./README.md) mais **repoussés** après les paliers Budget / Cockpit :

- registre bénévole (`glc.volunteer.timesheet`) ;
- rapport CA mensuel PDF classique (§11 spec) ;
- clôture analytique mensuelle (§8.7 spec).

Ils restent dans la cible fonctionnelle globale ; leur ordre de livraison est réorganisé autour du cockpit de soutenabilité.

---

## Documents liés

| Document | Rôle |
|---|---|
| [TICKET_PALIER_3.md](./TICKET_PALIER_3.md) | Spécification développement `dorevia_glc_budget` |
| [TICKET_PALIER_4.md](./TICKET_PALIER_4.md) | Cadrage cockpit couverture des salaires |
| [PALIERS.md](./PALIERS.md) | Roadmap consolidée |
