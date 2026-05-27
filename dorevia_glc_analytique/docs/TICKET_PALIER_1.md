# Ticket Palier 1 — Rapport d'anomalies analytiques du mois

**Module :** `dorevia_glc_analytique`  
**Branche cible :** `feat/glc-analytique-palier-1`  
**Statut :** Cadrage validé MOA / architecture — prêt pour développement  
**Prérequis :** merge PR #23 (Palier 0) · merge PR #24 (Phase 0 doc) recommandé  
**Références :** [PALIERS.md](./PALIERS.md) · [REGLES_AFFECTATION.md](./REGLES_AFFECTATION.md) · [MATRICE_MIGRATION.md](./MATRICE_MIGRATION.md)

---

## Contexte

Le Palier 0 a installé le socle analytique GLC :

- plan `GLC - Activités` ;
- plan `GLC - Financements` ;
- 11 comptes analytiques cibles ;
- applicabilités **non bloquantes** (`optional`) ;
- recette MOA validée sur `glc-rgl-test-import`.

Le Palier 1 vise à **contrôler la qualité des affectations analytiques** sans bloquer brutalement la saisie comptable.

---

## Objectif

Créer un premier rapport / assistant d'**anomalies analytiques mensuelles** permettant au gestionnaire de repérer les écritures non conformes aux règles d'affectation GLC.

Le rapport prépare la future discipline de clôture analytique (Palier 5), **sans** produire le rapport CA complet (Palier 4).

---

## Périmètre Palier 1

### 1. Assistant de sélection période

Wizard `glc.analytic.anomaly.wizard` :

| Champ | Description |
|---|---|
| `company_id` | Société |
| `date_from` / `date_to` | Période |
| `include_posted` | Écritures validées (défaut : oui) |
| `include_draft` | Brouillons (défaut : non) |

**Nom fonctionnel :** Anomalies analytiques GLC  
**Menu :** `Comptabilité → Pilotage GLC → Anomalies analytiques`  
**Groupe :** Gestionnaire GLC (lecture) ; génération réservée Gestionnaire GLC

Action : bouton **Analyser** → liste `glc.analytic.anomaly.line` (transient).

---

### 2. Contrôles attendus

Source technique : `account.move.line` avec `analytic_distribution` (JSON `{account_id: percentage}`).  
Résolution plan : `account.analytic.account.plan_id` vs plans XML `analytic_plan_glc_activites` / `analytic_plan_glc_financements`.

#### A1 — Factures fournisseurs sans activité

**Cible :** lignes charge sur `in_invoice`, `in_refund` sans compte du plan Activités GLC.

| Élément | Règle |
|---|---|
| Types de pièce | Facture fournisseur, avoir fournisseur |
| Lignes | Comptes charge (`account_type` expense*) |
| Anomalie | Aucune clé du plan `GLC - Activités` dans `analytic_distribution` |

**Message :** `Facture fournisseur sans activité GLC`

#### A2 — Recettes d'activité sans double axe

**Cible :** lignes produit sur `out_invoice`, `out_refund` devant porter Activités + Financements.

| Manque | Message |
|---|---|
| Activité | `Recette sans activité GLC` |
| Financement | `Recette sans financement GLC` |
| Les deux | `Recette incomplète : double axe attendu` |

**Cas :** bar, prestations, privatisations, loyer Radio, ressources propres (cf. [REGLES_AFFECTATION.md](./REGLES_AFFECTATION.md) §2).

**Exception Palier 1 :** subventions / adhésions / dons purs (axe Financements seul) — voir A3, pas A2.

#### A3 — Financements sans plan Financements

Recettes devant porter uniquement (ou principalement) l'axe Financements : adhésions, dons, subventions.

| Cas | Message |
|---|---|
| Adhésion | `Adhésion sans financement ADHESIONS` |
| Don | `Don sans financement DONS` |
| Subvention | `Subvention sans financement SUBVENTIONS` |

**Limite Palier 1 — décision MOA :** ne **pas** détecter A3 par libellé, partenaire ou heuristique fragile. Le contrôle A3 n'est **actif** que si un **mapping explicite** existe (`glc.account.funding.rule`). Sinon : message informatif sur le wizard, contrôle **désactivé** ou report **Palier 1.1**.

#### A4 — Écritures de paie avec analytique interdite

Lignes sur comptes de paie / charges sociales avec `analytic_distribution` non vide.

**Préfixes comptables indicatifs :** `631`, `633`, `641`, `645` (à confirmer plan comptable GLC).

**Message :** `Écriture de paie avec analytique directe interdite`

**Doctrine :** salaires ventilés au Palier 2, pas d'analytique directe en V1.

#### A5 — Anciens comptes analytiques après bascule

Usage des 9 comptes historiques (cf. [MATRICE_MIGRATION.md](./MATRICE_MIGRATION.md) §3) sur pièces **postérieures** à la date de bascule.

**Codes :** `ADHESION_GLC`, `BAR_RESTAU`, `DEPLACEMENT_MISSION`, `ESPACE_GLC`, `FRAIS_STRUCTURE`, `PRESTA_GLC`, `RESIDENCE_GLC`, `RH_PERSONNEL`, `SUBVENTION_GLC`

**Message :** `Ancien compte analytique utilisé après bascule`

**Paramètre :** `dorevia_glc_analytique.cutover_date` — si absent, contrôle **désactivé** ou mode informatif (warning wizard).

#### A6 — Poids STRUCTURE élevé (synthèse)

**Non line-by-line** — bloc récapitulatif en tête du résultat :

```text
Poids STRUCTURE = charges plan Activités sur STRUCTURE / total charges plan Activités
```

**Seuil :** `dorevia_glc_analytique.structure_weight_alert_pct` (défaut documenté : 30 %).

**Message :** `Poids STRUCTURE élevé — risque de compte fourre-tout`

**Décision MOA :** A6 est une **synthèse / bandeau** sur le wizard (`structure_weight_pct`, `structure_alert_message`). **Pas** une ligne d'anomalie comptable dans `glc.analytic.anomaly.line`.

---

### 3. Résultat attendu

Liste d'anomalies (`glc.analytic.anomaly.line`) avec :

| Champ | Description |
|---|---|
| `date` | Date pièce |
| `move_id` | Pièce comptable (lien) |
| `move_line_id` | Ligne source |
| `journal_id` | Journal |
| `partner_id` | Partenaire |
| `account_id` | Compte comptable |
| `name` | Libellé ligne |
| `amount` | Montant (signed selon sens) |
| `anomaly_type` | Code A1–A6 |
| `message` | Libellé anomalie |
| `activity_account_ids` | Comptes Activités détectés |
| `funding_account_ids` | Comptes Financements détectés |
| `recommendation` | Texte court corrective |

---

### 4. Format de sortie

**Minimal (Palier 1) :**

- vue liste Odoo (transient) ;
- bouton **Analyser** sur le wizard ;
- ouverture pièce comptable depuis la ligne.

**Optionnel si effort raisonnable :**

- compteurs par type d'anomalie (smart buttons ou bandeau) ;
- filtre par `anomaly_type` ;
- export XLSX.

**Hors scope :** PDF.

---

### 5. Mode bloquant / non bloquant

Palier 1 **non bloquant** par défaut :

- diagnostiquer, lister, corriger manuellement ;
- applicabilités Odoo restent `optional` ;
- passage `mandatory` documenté, **non activé** sans validation MOA explicite.

---

### 6. Modèle technique — décision architecture

**Retenu : Option A — wizard transient + lignes transient**

| Modèle | Rôle |
|---|---|
| `glc.analytic.anomaly.wizard` | Saisie période + lancement analyse |
| `glc.analytic.anomaly.line` | Résultats (TransientModel, `_transient_max_hours` standard) |

**Motifs :**

- simple, maintenable, pas de fausse clôture (Palier 5) ;
- pas d'historisation obligatoire en V1 ;
- regénération à la demande par période.

**Option B** (campagne persistante) : reporté si besoin d'archivage mensuel avant Palier 5.

**Dépendances manifest :** inchangées Palier 0 (`account`, `analytic`).

**Sécurité :** `ir.model.access.csv` — wizard + lines pour `group_glc_manager`.

---

### 7. Hors périmètre Palier 1

- ventilation salariale (Palier 2) ;
- registre bénévole (Palier 3) ;
- coût complet / rapport CA (Palier 4) ;
- clôture analytique (Palier 5) ;
- corrections automatiques ;
- migration rétroactive massive ;
- blocage validation comptable ;
- modification automatique des écritures.

---

### 8. Critères d'acceptation

| ID | Critère |
|---|---|
| CA1 | Menu `Anomalies analytiques` visible pour Gestionnaire GLC |
| CA2 | Facture fournisseur sans activité → anomalie A1 |
| CA3 | Facture client sans double axe → anomalie A2 |
| CA4 | Facture client `BAR` + `RESSOURCES_PROPRES` → **pas** d'anomalie A2 |
| CA5 | Écriture paie avec analytique → anomalie A4 |
| CA6 | Ancien compte après date bascule → anomalie A5 (si date paramétrée) |
| CA7 | Validation factures toujours possible (non bloquant) |
| CA8 | Tests auto : wizard, A1, A2, exclusion correcte, A5 si date, non-régression Palier 0 |

---

### 9. Documentation attendue

- [ ] Mettre à jour [PALIERS.md](./PALIERS.md)
- [ ] Ajuster [REGLES_AFFECTATION.md](./REGLES_AFFECTATION.md) si besoin (Palier 1 vs mandatory)
- [ ] [RECETTE_MANUELLE_PALIER_1.md](./RECETTE_MANUELLE_PALIER_1.md) — cas A1–A6 sur `glc-rgl-test-import`

---

### 10. Règle de livraison

```text
Branche : feat/glc-analytique-palier-1
Base    : main (après merge #23)

Ne pas mélanger avec :
- PR #23 — Palier 0
- PR #24 — Phase 0 migration documentaire
```

**Séquence :**

1. Merge #23 → merge #24  
2. Validation gestionnaire matrice migration  
3. Développement Palier 1 sur branche dédiée  
4. Recette Palier 1 → durcissement applicabilités (option MOA, post-Palier 1)

---

## Annexe — mapping anomaly_type

| Code | Contrôle |
|---|---|
| `a1_vendor_no_activity` | A1 |
| `a2_revenue_no_activity` | A2 (partiel activité) |
| `a2_revenue_no_funding` | A2 (partiel financement) |
| `a2_revenue_incomplete` | A2 (double axe) |
| `a3_funding_missing` | A3 |
| `a4_payroll_analytic` | A4 |
| `a5_legacy_account` | A5 |
| — | A6 : synthèse wizard uniquement (pas de `anomaly_type` ligne) |

---

## Vigilance MOA (gel cadrage)

1. **A3** — jamais de détection par libellé ; mapping `glc.account.funding.rule` obligatoire pour activer le contrôle.
2. **A6** — bandeau / champs synthèse sur le wizard, pas une anomalie ligne à ligne.
3. **Non bloquant** — pas de `mandatory` sans validation MOA explicite post-recette Palier 1.
