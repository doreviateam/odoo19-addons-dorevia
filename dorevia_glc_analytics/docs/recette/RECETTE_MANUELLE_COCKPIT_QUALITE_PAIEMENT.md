# Recette manuelle — Cockpit · Qualité comptable, analytique & suivi paiement

**Module :** `dorevia_glc_analytics` (extension cockpit — lot qualité / paiement)  
**Version cible :** **`19.0.6.x.0`** *(à confirmer à l’implémentation)*  
**Prérequis :** Palier 4 réaligné **`19.0.4.9.0`** gelé · Palier 5 trésorerie **`19.0.5.0.1`** GO complet MOA · `dorevia_glc_budget` installé  
**Statut document :** **Validée MOA — base recette GO cadrage** (2026-05-29) · **GQ-6 en attente — pas de GO code**

**Références :** [TICKET_COCKPIT_QUALITE_COMPTABLE_ANALYTIQUE_SUIVI_PAIEMENT.md](../TICKET_COCKPIT_QUALITE_COMPTABLE_ANALYTIQUE_SUIVI_PAIEMENT.md) · [MEMO_RAFFINEMENT_QUALITE_COMPTABLE_ANALYTIQUE.md](../MEMO_RAFFINEMENT_QUALITE_COMPTABLE_ANALYTIQUE.md) · [Recette Palier 5 trésorerie](./RECETTE_MANUELLE_PALIER_5_TRESORERIE_COMPTE_BANCAIRE_REFERENCE.md) · [Recette période libre Palier 4](./RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md) · [PALIERS.md](../PALIERS.md)

---

## Invariants à prouver

> **Recette · Cumul RH · Dépense · Solde ne doivent jamais être recalculés, corrigés ou filtrés par les statuts de paiement, le lettrage ou la couverture analytique.**

| Couche cockpit | Rôle | Peut modifier exploitation ? |
|---|---|:---:|
| **Exploitation** | Recette · Cumul RH · Dépense · Solde | — *(référence gelée)* |
| **Trésorerie** | Flux compte bancaire de référence | **Non** |
| **Contrôles qualité** | Couverture analytique · lettrage | **Non** |
| **Tiers & paiements** | Cycle facturation / règlement | **Non** |

Texte d’aide attendu sur les nouveaux onglets :

> *« Ces indicateurs mesurent la fiabilité des données et le cycle de paiement. Ils ne modifient pas Recette · Cumul RH · Dépense · Solde. »*

---

## Contexte de recette

```text
URL  : http://localhost:18079
Base : glc-rgl-test-import
Menu : Comptabilité → Pilotage GLC → Cockpit couverture des charges de structure
```

**Onglets attendus post-livraison :**

```text
Synthèse · Détail · Trésorerie · Contrôles qualité · Tiers & paiements · Infos
```

---

## 1. Préconditions

### 1.1 Installation / upgrade

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d glc-rgl-test-import -u dorevia_glc_analytics \
  --stop-after-init --no-http

docker compose restart odoo
```

| Contrôle | Attendu | OK | Observations |
|---|---|:---:|---|
| Version module `dorevia_glc_analytics` | **`19.0.6.x.0`** | [ ] | |
| Palier 5 trésorerie non régressé | Onglet **Trésorerie** présent | [ ] | |
| Worker Odoo redémarré après `-u` | Oui | [ ] | |
| Hard refresh navigateur | `Cmd+Shift+R` | [ ] | |

### 1.2 Société et paramètres cockpit

| Contrôle | Attendu | OK | Observations |
|---|---|:---:|---|
| Société | **`My Company`** | [ ] | |
| Journal bancaire cockpit GLC | **`Compte Courant GLC`** | [ ] | Palier 5 |
| Période de recette figée | du __________ au __________ | [ ] | Noter pour toute la recette |

### 1.3 Jeu de données minimum *(à préparer ou identifier sur la base)*

| Pièce / situation | Rôle recette | Présent | Réf. pièce |
|---|---|:---:|---|
| Facture client **payée** (`paid`) | QP-Q3-01 | [ ] | |
| Facture client **partiellement payée** (`partial`) | QP-Q3-02 | [ ] | |
| Facture client **non payée** (`not_paid`) | QP-Q3-03 | [ ] | |
| Facture client **en cours** (`in_payment`) *(si disponible)* | QP-Q3-04 | [ ] | |
| **Avoir client** (`out_refund`) | QP-Q3-05 | [ ] | |
| Facture fournisseur **payée** | QP-Q3-06 | [ ] | |
| Facture fournisseur **partiellement payée** | QP-Q3-07 | [ ] | |
| Facture fournisseur **non payée** | QP-Q3-08 | [ ] | |
| **Avoir fournisseur** (`in_refund`) | QP-Q3-09 | [ ] | |
| Facture charge / produit **sans analytique** | QP-Q1-01 | [ ] | |
| Facture charge / produit **avec analytique OK** | QP-Q1-02 | [ ] | |
| Ligne client **411 non lettrée** | QP-Q2-01 | [ ] | |
| Ligne fournisseur **401 non lettrée** | QP-Q2-02 | [ ] | |
| Paire lettrée client après rapprochement | QP-Q2-03 | [ ] | |

---

## 2. Non-régression exploitation *(bloquant)*

**Objectif :** prouver que les onglets qualité / paiement et les opérations associées **ne modifient pas** les KPI exploitation.

### 2.1 Relevé initial — onglet Synthèse

Période figée : du __________ au __________

| KPI exploitation | Valeur relevée | Source UI |
|---|---|---|
| **Recette** | | Synthèse · KPI ou onglet **Ressources** |
| **Cumul RH** | | Synthèse · **Charges de structure** |
| **Dépense** | | Synthèse · **Charges de structure** |
| **Solde** | | Synthèse · Solde période |

### 2.2 Navigation onglets qualité / paiement

1. Noter les **quatre KPI** § 2.1.
2. Ouvrir **Contrôles qualité** → parcourir les indicateurs et listes.
3. Ouvrir **Tiers & paiements** → parcourir clients / fournisseurs.
4. Revenir **Synthèse**.

| KPI | Après navigation | Identique ? | OK |
|---|---|---|:---:|
| Recette | | **Oui — obligatoire** | [ ] |
| Cumul RH | | **Oui — obligatoire** | [ ] |
| Dépense | | **Oui — obligatoire** | [ ] |
| Solde | | **Oui — obligatoire** | [ ] |

### 2.3 Scénarios QP-INV *(automatisable)*

| Réf. | Action | Exploitation | Trésorerie | OK |
|---|---|---|:---:|:---:|
| **QP-INV-01** | Ouvrir **Contrôles qualité** · refresh implicite | Inchangée | Inchangée | [ ] |
| **QP-INV-02** | Ouvrir **Tiers & paiements** | Inchangée | Inchangée | [ ] |
| **QP-INV-03** | Cliquer liste pièce non couverte · retour cockpit | Inchangée | Inchangée | [ ] |
| **QP-INV-04** | Cliquer liste facture ouverte · retour cockpit | Inchangée | Inchangée | [ ] |
| **QP-INV-05** | Lettrer une ligne 411 *(hors cockpit)* · refresh cockpit | Inchangée | N/A | [ ] |
| **QP-INV-06** | Enregistrer paiement facture client *(hors cockpit)* · refresh | Inchangée | Peut évoluer *(normal)* | [ ] |

**Verdict section 2 :**

- [ ] **OK** — exploitation strictement stable
- [ ] **NO GO** — au moins un KPI exploitation a changé sans changement de période *(bloquant)*

---

## 3. Non-régression trésorerie Palier 5

**Objectif :** l’ajout des onglets qualité / paiement **n’altère pas** la lecture trésorerie existante.

Compte bancaire de référence : **`Compte Courant GLC`**

| Indicateur trésorerie | Valeur avant recette qualité | Après navigation qualité/paiement | Identique ? | OK |
|---|---|---|:---:|:---:|
| Entrées trésorerie | | | **Oui** | [ ] |
| Sorties trésorerie | | | **Oui** | [ ] |
| Solde trésorerie période | | | **Oui** | [ ] |

| Réf. | Scénario | Attendu | OK |
|---|---|---|:---:|
| **QP-TREF-01** | KPI exploitation inchangés au changement de compte bancaire *(reprise Palier 5)* | Recette · Cumul RH · Dépense · Solde identiques | [ ] |
| **QP-TREF-02** | Montants trésorerie réactifs au compte bancaire | Courant ≠ livret si mouvements | [ ] |

---

## 4. Onglet Contrôles qualité — Q1 Couverture analytique

### 4.1 Affichage et formules

| Réf. | Point de contrôle | Attendu | OK | Observations |
|---|---|---|:---:|---|
| **QP-Q1-VIS** | Onglet **Contrôles qualité** visible | Oui | [ ] | |
| **QP-Q1-TXT** | Texte d’aide non-régression exploitation | Présent | [ ] | |
| **QP-Q1-CNT** | Pièces contrôlées | Entier ≥ 0 | [ ] | |
| **QP-Q1-COV** | Pièces couvertes | ≤ pièces contrôlées | [ ] | |
| **QP-Q1-RATE** | Taux de couverture | = couvertes / contrôlées | [ ] | |
| **QP-Q1-LST** | Lien / liste pièces non couvertes | Actionnable | [ ] | |

### 4.2 Scénarios métier

| Réf. | Scénario | Préparation | Attendu | OK | Observations |
|---|---|---|---|:---:|---|
| **QP-Q1-01** | Pièce sans analytique | Facture charge ou produit postée · ligne métier sans `analytic_distribution` | Taux < 100 % · pièce listée | [ ] | |
| **QP-Q1-02** | Correction analytique | Ajouter axe GLC sur la pièce · refresh cockpit | Taux augmente · pièce disparaît de la liste | [ ] | |
| **QP-Q1-03** | Exclusion lignes techniques | Pièce avec TVA / tiers / banque seuls | Ne fausse pas le taux *(pas comptée comme ligne métier)* | [ ] | |
| **QP-Q1-04** | Pièce hors période | Facture date hors `date_from`/`date_to` | Non comptée dans le taux période | [ ] | |
| **QP-Q1-05** | Brouillon exclu | Facture brouillon sans analytique | Non comptée | [ ] | |

### 4.3 Seuils couleur *(mémo MOA)*

| Taux | Couleur attendue | OK |
|---|---|:---:|
| 100 % | Vert | [ ] |
| 95 % – 99,99 % | Orange | [ ] |
| < 95 % | Rouge | [ ] |

**Verdict section 4 :**

- [ ] **OK**
- [ ] **NO GO**

---

## 5. Onglet Contrôles qualité — Q2 Lettrage tiers

### 5.1 Affichage clients / fournisseurs

| Réf. | Point de contrôle | Attendu | OK | Observations |
|---|---|---|:---:|---|
| **QP-Q2-VIS-C** | Taux lettrage **clients** | % affiché | [ ] | Comptes 411 |
| **QP-Q2-VIS-F** | Taux lettrage **fournisseurs** | % affiché | [ ] | Comptes 401 |
| **QP-Q2-AMT-C** | Montant client non lettré | ≥ 0 | [ ] | |
| **QP-Q2-AMT-F** | Montant fournisseur non lettré | ≥ 0 | [ ] | |
| **QP-Q2-AGE** | Ancienneté non lettrés | Buckets visibles *(0–30 / 31–60 / 61–90 / 90+ j)* | [ ] | |
| **QP-Q2-LST** | Listes actionnables | Ouvre lignes / pièces 411·401 | [ ] | |

### 5.2 Scénarios métier

| Réf. | Scénario | Préparation | Attendu | OK | Observations |
|---|---|---|---|:---:|---|
| **QP-Q2-01** | Client non lettré | Facture client postée · paiement absent ou non lettré | Montant client non lettré > 0 | [ ] | |
| **QP-Q2-02** | Fournisseur non lettré | Facture fournisseur postée · non lettrée | Montant fournisseur non lettré > 0 | [ ] | |
| **QP-Q2-03** | Lettrage complet client | Lettrer facture + paiement · refresh | Montant non lettré ↓ · taux ↑ | [ ] | |
| **QP-Q2-04** | Distinction lettrage / paiement | Facture `partial` mais ligne 411 partiellement lettrée | KPI lettrage ≠ KPI paiement · les deux cohérents | [ ] | |
| **QP-Q2-05** | Lignes produit/charge exclues | Écriture charge 6xx | N’entre pas dans le taux lettrage | [ ] | |

**Verdict section 5 :**

- [ ] **OK**
- [ ] **NO GO**

---

## 6. Onglet Tiers & paiements — Q3 Suivi paiement

### 6.1 Affichage général

| Réf. | Point de contrôle | Attendu | OK | Observations |
|---|---|---|:---:|---|
| **QP-Q3-VIS** | Onglet **Tiers & paiements** visible | Oui | [ ] | |
| **QP-Q3-TXT** | Texte d’aide : comptabilisé ≠ payé | Présent | [ ] | |
| **QP-Q3-LBL** | Libellés statuts = Odoo 19 | `not_paid` · `partial` · `in_payment` · `paid` | [ ] | |

### 6.2 Clients — synthèse

| Indicateur | Valeur relevée | OK | Observations |
|---|---|:---:|---|
| Factures clients émises (nombre / montant) | | [ ] | `out_invoice` postées période |
| Factures clients payées | | [ ] | `payment_state = paid` |
| Partiellement payées | | [ ] | `partial` |
| En cours de paiement | | [ ] | `in_payment` |
| Non payées | | [ ] | `not_paid` |
| Avoirs clients | | [ ] | `out_refund` |
| **Reste à encaisser** | | [ ] | `Σ amount_residual_signed` ouvert |

### 6.3 Fournisseurs — synthèse

| Indicateur | Valeur relevée | OK | Observations |
|---|---|:---:|---|
| Factures fournisseurs reçues | | [ ] | `in_invoice` |
| Payées / partielles / en cours / non payées | | [ ] | |
| Avoirs fournisseurs | | [ ] | `in_refund` |
| **Reste à payer** | | [ ] | |

### 6.4 Scénarios paiement *(cas MOA obligatoires)*

| Réf. | Cas | Préparation | Attendu cockpit | Exploitation inchangée ? | OK |
|---|---|---|---|:---:|:---:|
| **QP-Q3-01** | **Facture client payée** | Client · montant X · paiement total · `paid` | Reste encaissement = **0** · comptée en payées | **Oui** | [ ] |
| **QP-Q3-02** | **Facture client partielle** | Paiement < total · `partial` | Reste > 0 · `partial` visible | **Oui** | [ ] |
| **QP-Q3-03** | **Facture client non payée** | Aucun paiement · `not_paid` | Reste = total · comptée en ouvertes | **Oui** | [ ] |
| **QP-Q3-04** | **En cours de paiement** | Paiement initié · `in_payment` | Statut distinct · reste cohérent | **Oui** | [ ] |
| **QP-Q3-05** | **Avoir client** | `out_refund` lié ou indépendant | Réduit reste à encaisser · signe cohérent | **Oui** | [ ] |
| **QP-Q3-06** | **Facture fournisseur payée** | `in_invoice` + paiement total | Reste à payer = **0** | **Oui** | [ ] |
| **QP-Q3-07** | **Facture fournisseur partielle** | Paiement partiel | Reste > 0 · `partial` | **Oui** | [ ] |
| **QP-Q3-08** | **Facture fournisseur non payée** | Aucun paiement | Reste = total | **Oui** | [ ] |
| **QP-Q3-09** | **Avoir fournisseur** | `in_refund` | Reste à payer cohérent | **Oui** | [ ] |

### 6.5 Grille de cohérence comptabilisé vs payé

Sur **une facture client de référence** (noter n° __________ ) :

| Champ | Valeur pièce Odoo | Reflet cockpit | OK |
|---|---|---|:---:|
| `amount_total_signed` | | Facturé client | [ ] |
| `amount_residual_signed` | | Reste à encaisser | [ ] |
| `payment_state` | | Statut affiché | [ ] |
| Recette exploitation cockpit | | **Indépendante** du `payment_state` | [ ] |

**Verdict section 6 :**

- [ ] **OK**
- [ ] **NO GO**

---

## 7. Filtre période et société

| Réf. | Scénario | Action | Qualité / paiement | Exploitation | OK |
|---|---|---|---|---|:---:|
| **QP-PER-01** | Élargir période | `date_to` +1 mois | Indicateurs recalculés | KPI recalculés *(normal)* | [ ] |
| **QP-PER-02** | Réduire période | Exclure mois avec facture test | Facture test disparaît des compteurs | KPI peuvent baisser *(normal)* | [ ] |
| **QP-PER-03** | Pièce hors période | Facture mois M-1 | Absente des compteurs période M | — | [ ] |
| **QP-CO-01** | Multi-société | Changer société cockpit | Tous indicateurs filtrés société | — | [ ] |

---

## 8. Tests automatisés *(post-implémentation)*

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d glc-rgl-test-import -u dorevia_glc_analytics,dorevia_glc_budget \
  --test-enable --test-tags post_install \
  --stop-after-init --no-http
```

| Lot | Attendu | OK | Observations |
|---|---|:---:|---|
| Post-install global | **0 failed · 0 error** | [ ] | Non-régression Palier 4+5 |
| Bloc qualité / paiement isolé | **≥ 8 tests** dédiés | [ ] | Tag `test_coverage_cockpit_quality` *(à confirmer)* |
| **QP-INV auto** | `test_quality_does_not_change_exploitation_kpis` | [ ] | |
| **QP-TREF auto** | Trésorerie inchangée | [ ] | |

---

## 9. Critères de décision MOA

### 9.1 GO complet

Tous les points suivants :

- [ ] **QP-INV** · non-régression exploitation **OK** (§ 2)
- [ ] **QP-TREF** · non-régression trésorerie **OK** (§ 3)
- [ ] **Q1** couverture analytique **OK** (§ 4)
- [ ] **Q2** lettrage **OK** (§ 5)
- [ ] **Q3** suivi paiement **OK** — cas payé · partiel · impayé · avoir (§ 6)
- [ ] Filtre période / société **OK** (§ 7)
- [ ] Post-install **0 failed** (§ 8)

### 9.2 GO avec réserve

- [ ] Calculs OK · listes partiellement actionnables · wording à ajuster
- [ ] **`in_payment`** non testable sur la base *(statut absent)* — réserve documentée
- [ ] Seuils couleur non implémentés en V1

### 9.3 NO GO *(bloquant)*

Un seul item suffit :

- [ ] KPI **Recette · Cumul RH · Dépense · Solde** modifiés par qualité / paiement / lettrage
- [ ] Onglet **Trésorerie** Palier 5 régressé sans cause période / compte bancaire
- [ ] Facture **payée** comptée dans reste à encaisser / payer
- [ ] Facture **impayée** absente des montants ouverts
- [ ] **Avoir** ignore ou double-compte
- [ ] Lignes TVA / banque polluent couverture analytique
- [ ] Post-install **failed**

---

## 10. Verdict recette MOA

| Champ | Valeur |
|---|---|
| Date recette | |
| Exécutant | |
| Version testée | |
| Base | `glc-rgl-test-import` |
| Période testée | |
| Preuve invariant exploitation | Recette · Cumul RH · Dépense · Solde : |
| Preuve trésorerie | Entrées · Sorties · Solde : |
| Post-install | tests · failed · error |

### Verdict

- [ ] **GO complet**
- [ ] **GO avec réserve**
- [ ] **NO GO**

**Commentaires MOA :**

---

## 11. Séquence de lecture cockpit *(post-livraison)*

1. **Synthèse / Détail** — exploitation *(Recette · Cumul RH · Dépense · Solde)*
2. **Trésorerie** — flux compte bancaire de référence
3. **Contrôles qualité** — fiabilité analytique et lettrage
4. **Tiers & paiements** — cycle facturation / règlement
5. **Infos** — contrôle RH *(Palier 4 — inchangé)*

---

*Recette validée MOA post-GO cadrage 2026-05-29. Implémentation autorisée uniquement après **GO code (GQ-6)** explicite. Ne pas confondre avec recette Palier 5 trésorerie.*
