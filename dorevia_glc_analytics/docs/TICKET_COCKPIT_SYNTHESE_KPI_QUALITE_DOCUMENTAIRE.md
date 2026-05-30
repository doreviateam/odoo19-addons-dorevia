# Ticket — Cockpit GLC · KPI qualité documentaire (Synthèse graphique)

**Module :** `dorevia_glc_analytics`  
**Version cible :** **`19.0.10.0.0`** *(à confirmer à l’implémentation)*  
**Statut :** **Implémenté** — version **`19.0.10.0.0`**  
**Prérequis :** cockpit Palier 4 · Synthèse graphique (`glc_coverage_synthesis`) · filtre Payé uniquement **hors périmètre**

**Références :** [TICKET_COCKPIT_SYNTHESE_GRAPHIQUE.md](./TICKET_COCKPIT_SYNTHESE_GRAPHIQUE.md) · [TICKET_COCKPIT_DETAIL_PAYE_UNIQUEMENT.md](./TICKET_COCKPIT_DETAIL_PAYE_UNIQUEMENT.md) · [TICKET_COCKPIT_QUALITE_COMPTABLE_ANALYTIQUE_SUIVI_PAIEMENT.md](./TICKET_COCKPIT_QUALITE_COMPTABLE_ANALYTIQUE_SUIVI_PAIEMENT.md) · [RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md](./recette/RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md)

---

## 1. Contexte

L’onglet **Synthèse graphique** offre une lecture immédiate de pilotage :

- Solde réel / Solde budget
- Ressources totales
- Couverture du cumul RH
- Graphiques mensuels et solde par axe analytique

Le cockpit raisonne sur des **lignes comptables / écritures comptables éligibles au pilotage**, pas sur un comptage de factures.

Nous souhaitons ajouter **deux indicateurs de qualité documentaire** mesurant, **en montant**, quelle part des montants **Ressource** et **Dépense** provient d’une écriture de type **facture**.

> **Nommage UX retenu MOA :** **Ressources facturées** · **Dépenses facturées**  
> *(éviter « taux de facturation » en interface — risque de confusion avec un comptage de documents)*

---

## 2. Objectif

Répondre à :

> *Quelle part de mes ressources et de mes dépenses cockpit est documentée par une facture client / fournisseur ?*

Sans modifier les montants, graphiques ou KPI existants.

---

## 3. Demande fonctionnelle

### 3.1. Deux KPI à ajouter

```text
RESSOURCES FACTURÉES
xx %
part des ressources issues de factures client
```

```text
DÉPENSES FACTURÉES
xx %
part des dépenses issues de factures fournisseur
```

### 3.2. Emplacement UI

Bandeau KPI haut de **Synthèse graphique** — ordre cible :

```text
Solde réel
Solde budget
[Écart de solde]          ← si budget présent (existant)
Ressources totales
Ressources facturées      ← NOUVEAU
Dépenses facturées        ← NOUVEAU
Couverture du Cumul RH
```

Fichiers concernés :

- `static/src/xml/glc_coverage_synthesis_widget.xml` — cartes KPI
- `static/src/js/glc_coverage_synthesis_widget.esm.js` — formatage / classes
- `static/src/scss/glc_coverage_synthesis_widget.scss` — grille responsive si 6–7 cartes

Si la largeur est juste : adapter la grille (`flex-wrap`, cartes plus compactes), **sans retirer** les deux nouveaux KPI de la zone haute.

### 3.3. Règles d’affichage

| Cas | Affichage |
|-----|-----------|
| Dénominateur > 0 | `xx %` (arrondi entier acceptable, cohérent avec Couverture RH) |
| Dénominateur = 0 | `—` (**pas** `0 %`) |
| Sous-titre | Texte d’aide sous le pourcentage (voir § 3.1) |

**Option visuelle V1 (non bloquante) :** seuils couleur

```text
≥ 90 %  : OK
60–89 % : à surveiller
< 60 %  : à qualifier
```

Priorité : **calcul juste** + présentation sobre.

---

## 4. Doctrine MOA (corrigée)

### 4.1. Ce qu’on mesure

```text
On ne compte pas les factures.
On somme les montants des lignes comptables éligibles au cockpit.
Puis on regarde si l’écriture d’origine est une facture ou non.
```

Une facture multi-lignes analytiques peut alimenter plusieurs axes — **normal**, le cockpit travaille déjà en logique de lignes / montants.

### 4.2. Distinction Payé vs Facturé

| Lecture | Objet |
|---------|--------|
| **Payé uniquement** *(tableau Détail)* | Paiement / trésorerie / rapprochement |
| **Facturé** *(Synthèse — ce ticket)* | Origine documentaire = écriture facture |

Une écriture bancaire peut être **payée mais non facturée** :

- reste dans les montants cockpit si éligible ;
- peut rester en vue Payé uniquement ;
- **n’alimente pas** le numérateur Ressources / Dépenses facturées ;
- **diminue** le taux concerné (reste au dénominateur).

### 4.3. Cumul RH

**Hors périmètre V1** — les deux KPI ne portent que sur **Ressource** et **Dépense**.

---

## 5. Définitions métier

### 5.1. Ressources facturées

```text
Ressources facturées =
  Σ montants lignes Ressource éligibles cockpit
  dont move d’origine = facture client
/
  Σ montants lignes Ressource éligibles cockpit
```

**Numérateur — inclus :**

- lignes analytiques éligibles au domaine **Ressource** du cockpit ;
- rattachées à une pièce `move_type = out_invoice`.

**Dénominateur — inclus :**

- **toutes** les lignes Ressource éligibles : factures client, banque, OD, financements sans facture, virements internes 580 qualifiés, etc.

**Avoir client (`out_refund`) :** **exclu du numérateur** en V1 *(à traiter comme non facturé pour ce KPI ; documenter si MOA souhaite l’inclure ultérieurement)*.

### 5.2. Dépenses facturées

```text
Dépenses facturées =
  Σ montants lignes Dépense éligibles cockpit
  dont move d’origine = facture fournisseur
/
  Σ montants lignes Dépense éligibles cockpit
```

**Numérateur — inclus :**

- lignes analytiques domaine **Dépense** (classe 6 hors payroll) ;
- pièce `move_type = in_invoice`.

**Dénominateur — inclus :**

- toutes les lignes Dépense éligibles : factures fournisseur, banque directe, OD, virements internes sortie, etc.

**Avoir fournisseur (`in_refund`) :** **exclu du numérateur** en V1.

---

## 6. Cas particuliers (obligatoires)

| Cas | Ressource / Dépense cockpit | Numérateur facturé |
|-----|----------------------------|--------------------|
| Facture client / fournisseur postée + analytique | Oui | **Oui** |
| Écriture banque sans facture (512, OD journal banque) | Oui si éligible | **Non** |
| OD / écriture diverse (`move_type = entry`) | Oui si éligible | **Non** |
| Virement interne **580** (VIR_INT…) | Oui *(Ressource ou Dépense selon sens)* | **Non** |
| Ligne analytique **sans** `move_line_id` | Oui si dans dénominateur agrégé cockpit | **Non** |
| Paiement / lettrage | **Sans effet** sur ce KPI | — |

> Les virements internes sont ajoutés au réalisé cockpit via `_internal_transfer_amounts_for_account()` — ils entrent au **dénominateur** mais **pas** au numérateur, sauf rattachement explicite à une facture *(cas non attendu)*.

---

## 7. Périmètre technique Dev

### 7.1. À faire

| # | Tâche |
|---|--------|
| T1 | Champs calculés sur `glc.coverage.cockpit` *(recommandé)* ou agrégation au `action_refresh()` |
| T2 | Méthodes `_sum_revenue_invoiced` / `_sum_expense_invoiced` + taux dérivés |
| T3 | Réutiliser **strictement** les domaines existants : `_revenue_analytic_line_domain`, `_expense_analytic_line_domain`, `_signed_analytic_amount`, `_cockpit_analytic_accounts()` |
| T4 | Helper `_glc_analytic_line_is_customer_invoice(line)` / `_…_supplier_invoice(line)` dans `glc_quality_mixin.py` *(miroir de la règle payé)* |
| T5 | Inclure les **montants 580** internes dans le dénominateur Ressource / Dépense *(cohérent avec `revenue_realized` / `expense_realized` détail)* |
| T6 | Exposer les taux au widget Synthèse *(champs cockpit ou relatedFields)* |
| T7 | Deux cartes KPI dans `glc_coverage_synthesis_widget.xml` |
| T8 | Tests auto + recette manuelle |

### 7.2. Proposition de champs cockpit

```python
revenue_invoiced_amount      # numérateur Ressources facturées
revenue_eligible_amount      # dénominateur (contrôle / debug)
revenue_invoiced_rate        # % ou False si dénominateur nul

expense_invoiced_amount
expense_eligible_amount
expense_invoiced_rate
```

Le widget lit `revenue_invoiced_rate` / `expense_invoiced_rate` ; affiche `—` si `False` / `None`.

### 7.3. Algorithme de référence

```python
def _line_is_invoiced_revenue(self, analytic_line):
    move_line = analytic_line.move_line_id
    if not move_line:
        return False
    return move_line.move_id.move_type == "out_invoice"

def _line_is_invoiced_expense(self, analytic_line):
    move_line = analytic_line.move_line_id
    if not move_line:
        return False
    return move_line.move_id.move_type == "in_invoice"

def _sum_lines_invoiced(self, domain, invoice_checker):
    lines = self.env["account.analytic.line"].search(domain)
    return sum(
        self._signed_analytic_amount(line)
        for line in lines
        if invoice_checker(line)
    )
```

Taux :

```python
rate = (numerator / denominator * 100) if denominator else False
```

**Cohérence dénominateur :**

```text
revenue_eligible_amount
  = Σ lignes domaine ressource (tous axes cockpit)
  + Σ entrées virement interne 580 (même règle que refresh détail)

expense_eligible_amount
  = Σ lignes domaine dépense (tous axes cockpit)
  + Σ sorties virement interne 580
```

> **Important :** le KPI **Ressources totales** affiché aujourd’hui = `resources_realized` (recettes activité + financements). Le KPI **Ressources facturées** porte sur le périmètre **Ressource colonne détail** (domaine ressource), **pas** sur le libellé carte « Ressources totales » seul. Les financements sans facture **diminuent** le taux — comportement MOA voulu.

### 7.4. Hors périmètre

- Nouveau graphique
- Drill-down
- Colonne dans le tableau Détail
- Correction automatique des écritures
- Cumul RH
- Lien avec filtre **Payé uniquement**
- Modification des montants / graphiques / KPI existants

---

## 8. Non-régression (invariants)

| Invariant | Attendu |
|-----------|---------|
| `activity_revenue_realized`, `resources_realized`, `general_expenses_realized`, etc. | **Inchangés** |
| Graphiques Chart.js (3 blocs) | **Inchangés** |
| KPI Solde / Budget / Couverture RH | **Inchangés** |
| Tableau Détail · Payé uniquement | **Inchangés** |
| Onglets Trésorerie · Qualité · Tiers | **Inchangés** |

---

## 9. Critères de recette

| Réf. | Critère | OK |
|------|---------|:--:|
| **RT-DOC-01** | Les deux KPI visibles en Synthèse graphique | [ ] |
| **RT-DOC-02** | Calcul **en montant** sur lignes éligibles, pas en nombre de factures | [ ] |
| **RT-DOC-03** | Facture client → numérateur Ressources facturées | [ ] |
| **RT-DOC-04** | Ressource sans facture → dénominateur seulement | [ ] |
| **RT-DOC-05** | Facture fournisseur → numérateur Dépenses facturées | [ ] |
| **RT-DOC-06** | Dépense sans facture → dénominateur seulement | [ ] |
| **RT-DOC-07** | Banque directe sans facture → non facturée | [ ] |
| **RT-DOC-08** | Virement interne 580 → non facturé | [ ] |
| **RT-DOC-09** | Dénominateur nul → `—` | [ ] |
| **RT-DOC-10** | KPI / graphiques / montants existants inchangés | [ ] |
| **RT-DOC-11** | Filtre Payé uniquement (Détail) sans impact | [ ] |

### Jeu de données recette suggéré

| Pièce | Montant | Ressources fact. | Dépenses fact. |
|-------|--------:|:----------------:|:--------------:|
| Facture client payée + analytique Bar | 1 000 € | ↑ num. | — |
| Facture client impayée + analytique Bar | 800 € | ↑ num. | — |
| Facture fournisseur payée Structure | 400 € | — | ↑ num. |
| Facture fournisseur impayée Structure | 300 € | — | ↑ num. |
| OD banque + analytique Missions | 275 € | — | ↓ dénom. seul |
| VIR_INT entrée 580 | 9 000 € | ↓ dénom. seul | — |

Exemple attendu (ordre de grandeur) :

```text
Ressources facturées ≈ 1 800 / 11 800 ≈ 15 %   (1 000 + 800 sur 1 800 + 9 000 + …)
Dépenses facturées   ≈   700 /   975 ≈ 72 %   (400 + 300 sur 700 + 275 + …)
```

*(Ajuster selon périmètre exact financements / axes de la période test.)*

---

## 10. Tests automatisés attendus

Classe suggérée : `TestGlcCoverageCockpitSynthesisDocumentQuality`

| Test | Scénario |
|------|----------|
| DOC-01 | Facture client seule → taux ressource = 100 % |
| DOC-02 | Banque sans facture seule → taux ressource = 0 % |
| DOC-03 | Mix facture + banque → taux cohérent |
| DOC-04 | Facture fournisseur seule → taux dépense = 100 % |
| DOC-05 | 580 VIR_INT → hors numérateur ressource |
| DOC-06 | Dénominateur nul → taux `False` / pas de division |
| DOC-INV-01 | Refresh cockpit → KPI exploitation inchangés |

Tag : `/dorevia_glc_analytics:TestGlcCoverageCockpitSynthesisDocumentQuality`

---

## 11. Message court Dev (copier-coller)

```text
Nouvelle demande MOA — Ajouter deux KPI de qualité documentaire dans “Synthèse graphique”

Je souhaite ajouter deux indicateurs visuels dans l’onglet Synthèse graphique :

- RESSOURCES FACTURÉES
- DÉPENSES FACTURÉES

Attention doctrine : il ne s’agit pas de compter les factures.

Le cockpit raisonne sur des lignes comptables / écritures comptables éligibles au pilotage. Les KPI doivent donc mesurer, en montant, la part des lignes Ressource et Dépense dont l’écriture d’origine est une facture.

Définitions attendues :

Ressources facturées =
montant des lignes Ressource éligibles au cockpit dont l’écriture d’origine est une facture client
/
montant total des lignes Ressource éligibles au cockpit

Dépenses facturées =
montant des lignes Dépense éligibles au cockpit dont l’écriture d’origine est une facture fournisseur
/
montant total des lignes Dépense éligibles au cockpit

Ces indicateurs mesurent la qualité documentaire des écritures, pas le paiement.

Distinction MOA :
- Payé uniquement = lecture paiement / trésorerie / rapprochement
- Facturé = écriture issue d’une facture

Une écriture bancaire sans facture peut donc être payée mais non facturée : elle reste dans les montants du cockpit si elle est éligible, mais elle ne doit pas alimenter le numérateur du taux de facturation.

Emplacement souhaité :
dans la ligne haute des KPI de Synthèse graphique, idéalement entre “Ressources totales” et “Couverture du cumul RH”.

Règle d’affichage :
- afficher un pourcentage ;
- afficher “—” si le dénominateur est nul ;
- ne pas modifier les graphiques existants ;
- ne pas modifier les montants existants.

Hors périmètre :
- pas de drill-down ;
- pas de nouveau graphique ;
- pas de nouvelle colonne dans le détail ;
- pas de traitement du Cumul RH dans cette passe.

Critères de recette :
- les deux KPI sont visibles ;
- le calcul est fait en montant sur les lignes comptables éligibles ;
- les écritures issues de factures alimentent le numérateur ;
- les écritures sans facture restent au dénominateur uniquement ;
- les écritures bancaires directes et virements internes sont considérés comme non facturés ;
- aucun impact sur les KPI, graphiques et montants existants.

Ticket détaillé : docs/TICKET_COCKPIT_SYNTHESE_KPI_QUALITE_DOCUMENTAIRE.md
```

---

## 12. Critères de GO MOA

- [ ] RT-DOC-01 à RT-DOC-11 validés
- [ ] Tests auto **0 failed**
- [ ] Recette navigateur Synthèse graphique
- [ ] Aucune régression Payé uniquement / Détail / Trésorerie

**Verdict :** *(à compléter après livraison)*

---

*Demande MOA corrigée — ne pas confondre avec Q3 « Tiers & paiements » (cycle facturation) ni avec le filtre « Payé uniquement » (tableau Détail).*
