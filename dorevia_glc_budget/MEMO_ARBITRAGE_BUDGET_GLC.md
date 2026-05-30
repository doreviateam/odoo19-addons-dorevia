# Mémo MOA — Reprise du budget prévisionnel GLC

**Document :** arbitrage fonctionnel et technique  
**Public :** MOA · direction · gestionnaire · équipe dev  
**Date de rédaction :** 2026-05-30  
**Réunion cible :** MOA — 31 mai 2026  
**Auteur :** équipe Dorevia / GLC  
**Statut :** **Proposition de cadrage** — à valider en MOA

**Contexte produit :**

- Module socle actif : `dorevia_glc_analytics` (**`19.0.14.x`**, Contrôle de gestion en **réalisé seul**)
- Module budget : **`dorevia_glc_budget` retiré du dépôt** (`19.0.14.0.0`, PR #51)
- Sandbox recette : `glc-rgl-test-import`

**Documents liés (analytics) :**

- [ETAT_MODULE_ACTUEL.md](../dorevia_glc_analytics/docs/ETAT_MODULE_ACTUEL.md)
- [TICKET_PALIER_3.md](../dorevia_glc_analytics/docs/TICKET_PALIER_3.md) *(historique — spec initiale)*
- [CADRAGE_BUDGET_COCKPIT.md](../dorevia_glc_analytics/docs/CADRAGE_BUDGET_COCKPIT.md) *(historique)*
- [RELEASE_NOTE_19.0.14_SIMPLIFICATION_PILOTAGE.md](../dorevia_glc_analytics/docs/RELEASE_NOTE_19.0.14_SIMPLIFICATION_PILOTAGE.md)

---

## 1. Synthèse exécutive (1 minute)

GLC dispose aujourd’hui d’un **Contrôle de gestion fiable sur le réalisé comptable** (Ressources · Cumul RH · Dépenses · Solde), mais **sans trajectoire prévisionnelle**.

La question MOA n’est pas « faut-il un budget ? » — c’est **comment le remettre en place sans re-complexifier le produit**, en s’appuyant sur le socle analytique déjà livré.

**Recommandation dev :**

1. **Ne pas installer** le module vendor `base_account_budget` (Cybrosys).
2. **Recréer** un module léger **`dorevia_glc_budget`**, calé sur les **11 axes analytiques GLC** et la grammaire actuelle du cockpit.
3. Livrer en **2 temps** :
   - **Lot B1** — saisie et validation du prévisionnel (module budget autonome) ;
   - **Lot B2** — réintégration **optionnelle et progressive** des écarts dans le Contrôle de gestion.

Cette approche reprend le cadrage Palier 3 **validé MOA en 2026-05-27**, adapté à l’état actuel du produit (plan analytique unique, cockpit simplifié, Palier 2 retiré).

---

## 2. Pourquoi en reparler maintenant ?

### 2.1 Ce qui fonctionne (à préserver)

| Élément | Statut |
|---|---|
| Plan analytique GLC — 11 axes sur un plan unique | Actif |
| Contrôle de gestion — Tableau de bord + détail par axe | Actif — réalisé seul |
| Trésorerie (compte bancaire de référence) | Actif — indépendant du budget |
| Qualité comptable & suivi paiement (GQ-6) | Actif |
| Alertes rouge / orange / vert (couverture charges) | Actif — sur réalisé |

### 2.2 Ce qui manque côté pilotage

Sans budget, le CA / la direction ne peut pas répondre facilement à :

- « Avons-nous respecté la trajectoire prévue sur le trimestre ? »
- « Quel écart prévu / réalisé sur Prestations, Bar, ou le cumul RH ? »
- « Le budget initial ou le budget révisé est-il la référence de l’année ? »

Le **réalisé seul** répond à « où en sommes-nous ? », pas à « où devions-nous être ? ».

### 2.3 Ce qui s’est passé récemment (rappel factuel)

| Date / version | Décision |
|---|---|
| `19.0.13.0.0` | Retrait budget + Palier 2 du cockpit — focus réalisé |
| `19.0.14.0.0` | Suppression du module `dorevia_glc_budget` du dépôt |
| `19.0.14.1.0` | Stabilisation MOA — menus Contrôle de gestion · Audit · Axes |

**Motif MOA de la simplification :** réduire la surface produit, éliminer les doubles lectures (overlay RH, colonnes budget partielles, ambiguïtés de périmètre).

**Conséquence :** la **doctrine réalisé** est saine ; le **prévisionnel** doit revenir **proprement**, pas en recollant l’ancien empilement.

---

## 3. Question centrale pour la MOA demain

> **Souhaite-t-on relancer un budget GLC centré sur les axes analytiques et les scénarios annuels, sans réintroduire de module comptable générique, avec réintégration progressive des écarts dans le Contrôle de gestion ?**

Questions dérivées à trancher :

| # | Question MOA |
|---|---|
| Q1 | Le budget est-il **obligatoire** pour valider la V1 pilotage, ou **phase 2** après stabilisation UX cockpit ? |
| Q2 | Quel **scénario** est la référence par défaut dans le cockpit : `initial`, `revised`, ou choix utilisateur ? |
| Q3 | Faut-il budgétiser **Ressources + Cumul RH + Dépenses** séparément, ou seulement un sous-ensemble (ex. ressources + masse salariale) ? |
| Q4 | Les **4 axes financement** (`ADHESIONS`, `DONS`, `SUBVENTIONS`, `RESSOURCES_PROPRES`) entrent-ils dans le budget V1 ? |
| Q5 | Qui **saisit** et qui **valide** le budget (Gestionnaire GLC seul ? CA en lecture ?) ? |
| Q6 | Réintégration cockpit : **colonnes écart** dans le détail, **KPI écart** dans le Tableau de bord, ou **écran budget dédié** seulement en V1 ? |

---

## 4. Option A — Installer `base_account_budget` (vendor)

**Emplacement analysé :** `odoo19-addons-vendor/base_account_budget` (Cybrosys, Odoo 19 Community).

### 4.1 Fonctionnement du module vendor

| Modèle | Rôle |
|---|---|
| `account.budget.post` | Poste budgétaire = **ensemble de comptes GL** (641, 645, 706…) |
| `budget.budget` | En-tête budget (dates, workflow multi-états) |
| `budget.lines` | Ligne = poste GL + compte analytique + montant prévu |
| Champs calculés | Réalisé lu sur `account.analytic.line` filtré par comptes du poste |

### 4.2 Points forts (inspiration utile)

- UX éprouvée : en-tête budget + lignes, workflow brouillon → validé ;
- Notion **prévu / réalisé / écart / taux d’atteinte** ;
- Lien avec les comptes analytiques Odoo.

### 4.3 Limites pour GLC

| Limite | Impact GLC |
|---|---|
| Granularité **comptes GL**, pas **axes GLC** | Décalage avec la lecture MOA Bar / Prestations / etc. |
| Pas de typage `recette / charge / financement` | Incompatible avec la cartographie cockpit actuelle |
| Calcul réalisé **dans le module budget** | Double moteur avec le Contrôle de gestion (risque d’écarts) |
| SQL legacy sur analytique | Fragile vs distribution analytique Odoo 19 |
| Dépendance vendor (LGPL Cybrosys) | Dette de maintenance, hors stack Dorevia |
| Pas de scénarios `initial / revised / landing` | Besoin MOA non couvert |

### 4.4 Verdict option A

**Ne pas installer.**  
S’en **inspirer** pour l’UX (écrans, workflow, lecture prévu/réalisé), **sans** reprendre le modèle de données ni le calcul du réalisé.

---

## 5. Option B — Module dédié `dorevia_glc_budget` (recommandé)

### 5.1 Principe

```text
Prévisionnel  →  glc.budget.line        (saisie MOA, stockée, versionnée)
Réalisé       →  account.analytic.line  (déjà calculé par dorevia_glc_analytics)
Croisement    →  Contrôle de gestion     (lecture seule, règles MOA figées)
```

**Règles d’or (non négociables côté dev) :**

| # | Règle |
|---|---|
| R1 | Aucune écriture comptable générée |
| R2 | Aucune écriture analytique générée |
| R3 | Le réalisé cockpit **reste** la source `account.analytic.line` — le budget ne recalcule pas le réel |
| R4 | Module **séparé** de `dorevia_glc_analytics` — dépendance simple |
| R5 | Pas d’OCA Budget en V1 |

### 5.2 Alignement avec le référentiel analytique actuel

**État au 2026-05-30** ([ETAT_NOMENCLATURE_ANALYTIQUE.md](../dorevia_glc_analytics/docs/ETAT_NOMENCLATURE_ANALYTIQUE.md)) :

- **Un plan** : `GLC - Activités`
- **11 axes** : 7 activités + 4 financements (codes `ADHESIONS`, `DONS`, `SUBVENTIONS`, `RESSOURCES_PROPRES`)
- Type GLC sur chaque axe : `recette` · `charge` · `mixte`

**Adaptation vs ticket Palier 3 initial :**  
Le ticket historique supposait 2 plans (Activités + Financements). Le budget V1 doit cibler le **plan unique** et filtrer par **code / type GLC**, pas par plan séparé.

### 5.3 Modèle de données proposé

#### `glc.budget` — en-tête

| Champ | Description |
|---|---|
| `name` | Ex. « Budget 2026 — initial » |
| `year` | Année budgétaire |
| `company_id` | Société |
| `scenario` | `initial` · `revised` · `landing` |
| `state` | `draft` · `validated` · `archived` |
| `line_ids` | Lignes mensuelles |
| `note` | Commentaire global |
| `validated_by` / `validated_date` | Traçabilité validation |

**Unicité :** `(company_id, year, scenario)` — un scénario par année et société.

#### `glc.budget.line` — ligne mensuelle

| Champ | Description |
|---|---|
| `budget_id` | Budget parent |
| `period_date` | **1er jour du mois** concerné |
| `analytic_account_id` | Axe GLC (domaine : plan GLC) |
| `line_type` | `revenue` · `expense` · `funding` |
| `amount` | Montant prévu ≥ 0 |
| `note` | Commentaire ligne |

**Unicité :** `(budget_id, period_date, analytic_account_id, line_type)`.

**Cohérence type / axe (proposition) :**

| `line_type` | Axes autorisés |
|---|---|
| `revenue` | Axes type GLC `recette` ou `mixte` |
| `expense` | Axes type GLC `charge` ou `mixte` |
| `funding` | Codes financement (`ADHESIONS`, `DONS`, `SUBVENTIONS`, `RESSOURCES_PROPRES`) |

### 5.4 Workflow MOA proposé

| État | Droits | Description |
|---|---|---|
| `draft` | Gestionnaire GLC | Saisie / modification libre |
| `validated` | Lecture large | Budget de référence — modification via déverrouillage contrôlé |
| `archived` | Lecture seule | Exercice ou scénario clos |

Validation **non bloquante** pour la comptabilité Odoo.

---

## 6. Règles de croisement prévu / réalisé (cockpit)

Ces règles ont été **recettées** avant simplification (`19.0.4.x`) et restent la base MOA recommandée.

### 6.1 Période utilisateur vs mois budgétaire

| Donnée | Règle |
|---|---|
| **Réalisé** | Somme des écritures analytiques **entre `date_from` et `date_to`** exactes |
| **Budget** | **Mois calendaire complet** dès que le mois est **touché** par la période |

**Exemple :** période `15 mars → 30 avril`

- Mars et avril apparaissent comme mois ;
- Réalisé mars = du 15 au 31 mars seulement ;
- Budget mars = **montant budgétaire du mois entier**.

> **Point MOA à confirmer :** cette asymétrie est volontaire (comparer trajectoire mensuelle vs réalisé partiel) ou faut-il prorata budget sur période partielle ?

### 6.2 Agrégation cockpit (grammaire actuelle)

| Indicateur cockpit | Budget `line_type` | Réalisé (source analytics) |
|---|---|---|
| **Ressources** | `revenue` + `funding` *(si MOA valide)* | Classe 7 + axes financement |
| **Cumul RH** | `expense` sur axes paie / RH | Classe 6 — comptes paie (631, 633, 641, 645…) |
| **Dépenses** | `expense` hors paie | Classe 6 hors paie |
| **Solde** | Ressources − Cumul RH − Dépenses (budgétés) | Idem sur réalisé |

**Point ouvert historique :** ligne budget `STRUCTURE` en `expense` — alimente **Dépenses** ou **Cumul RH** ?  
→ À trancher MOA avant Lot B2 (cartographie par code analytique ou par comptes paie).

### 6.3 Scénario actif dans le cockpit

Proposition V1 :

- Paramètre société ou cockpit : **scénario par défaut** (`initial` par défaut) ;
- Sélecteur optionnel : basculer vers `revised` / `landing` ;
- Message discret si **aucune ligne budget** sur la période (`has_budget_data = False`).

---

## 7. Intégration avec le Contrôle de gestion

### 7.1 État actuel du cockpit (ne pas casser)

| Onglet | Contenu aujourd’hui |
|---|---|
| **Tableau de bord** | KPI réalisé + graphiques (Solde, Structure, Par axe) |
| **Détail par axe analytique** | Tableau mensuel Ressources / Cumul RH / Dépenses / Solde |
| **Charges de structure** | Synthèse réalisé |
| **Trésorerie** | Flux compte bancaire référence |
| **Contrôles qualité** | Q1–Q2 + lettrage |
| **Tiers & paiements** | Q3 cycle facturation |

Onglets masqués MOA : Ressources, Infos.  
Période par défaut : **3 derniers mois calendaires**.

### 7.2 Lot B2 — réintégration budget (proposition phased)

| Phase | Périmètre | Valeur MOA |
|---|---|---|
| **B2a** | Indicateur discret « Budget disponible / absent » + scénario actif | Visibilité sans surcharge |
| **B2b** | Colonnes **Budget** et **Écart** dans Détail par axe (toggle affichage) | Comparaison fine |
| **B2c** | KPI Tableau de bord : écart global période, graphique réel vs budget | Pilotage direction |
| **B2d** | Export PDF / Excel budget vs réalisé | Reporting CA |

**Recommandation :** valider **B1 seul** en premier jalon MOA ; **B2b minimum** comme critère de succès « budget utile ».

### 7.3 Ce qu’on ne remet **pas** (accord simplification MOA)

- Overlay ventilation salariale Palier 2 dans le cockpit ;
- Colonnes budget partielles sans message de périmètre ;
- Double calcul du réalisé dans le module budget ;
- Terminologie « Marge d’activité » / « Performance » — grammaire actuelle **Solde** conservée.

---

## 8. Parcours utilisateur cible

### 8.1 Gestionnaire — saisie annuelle

1. **Facturation → Pilotage GLC → Budgets GLC** *(menu à créer)*
2. Créer « Budget 2026 — initial »
3. Saisir les lignes mensuelles par axe (grille ou liste filtrée)
4. Valider le budget → statut `validated`
5. En cours d’année : dupliquer ou créer « Budget 2026 — revised »

### 8.2 Direction — lecture cockpit

1. **Facturation → Pilotage GLC → Contrôle de gestion**
2. Choisir période (ex. 3 derniers mois)
3. Tableau de bord : KPI réalisé + écart vs budget *(Lot B2)*
4. Détail : mois × axes avec colonnes budget / écart *(Lot B2)*

### 8.3 Inspiration UX reprise du vendor (sans l’installer)

| Idée vendor | Adaptation GLC |
|---|---|
| Liste budgets + formulaire | Oui — menu Pilotage GLC |
| Workflow multi-états | Simplifier : 3 états (`draft` / `validated` / `archived`) |
| Lignes inline | Oui — onglet lignes sur `glc.budget` |
| % achievement | Écart % uniquement si MOA le demande (V2) |
| Postes budgétaires GL | **Non** — remplacés par axes + `line_type` |

---

## 9. Plan de livraison proposé

### Lot B1 — Module budget autonome (4 à 6 j dev)

| Livrable | Détail |
|---|---|
| Squelette `dorevia_glc_budget` | Manifest, sécurité, dépendance `dorevia_glc_analytics` |
| Modèles `glc.budget` + `glc.budget.line` | Contraintes, domaines axes |
| Écrans saisie | Liste + formulaire + lignes |
| Menu | Sous **Pilotage GLC** |
| Tests automatisés | CRUD, unicité, domaines, workflow |
| Recette MOA | `RECETTE_MANUELLE_PALIER_3.md` à réactiver / mettre à jour |

**Critère GO Lot B1 :** saisir et valider un budget 2026 complet sans toucher au cockpit.

### Lot B2 — Croisement cockpit (3 à 5 j dev)

| Livrable | Détail |
|---|---|
| Extension `dorevia_glc_analytics` | Dépendance optionnelle ou `hasattr` module budget |
| Service agrégation budget | `_budget_lines()` — règles §6 |
| UI cockpit | Colonnes / KPI / messages |
| Tests | Non-régression 49+ tests cockpit |
| Recette | Scénarios R4 période partielle + multi-mois |

**Critère GO Lot B2 :** écarts cohérents sur période mars–mai avec budget test.

### Lot B3 — Confort (post-MOA)

- Import CSV lignes budgétaires ;
- Duplication budget année N → N+1 ;
- Comparaison côte à côte `initial` vs `revised` ;
- Commentaires de gestion par mois.

---

## 10. Sécurité et gouvernance

| Rôle | Budget | Cockpit écarts |
|---|---|---|
| **Utilisateur GLC** | Lecture *(proposé)* | Lecture |
| **Gestionnaire GLC** | CRUD + validation | Lecture |
| **Administration Odoo** | Tout | Tout |

Traçabilité : `validated_by`, `validated_date`, chatter optionnel sur déverrouillage.

---

## 11. Risques et mitigations

| Risque | Mitigation |
|---|---|
| Re-complexifier le cockpit | Lot B1 isolé ; B2 avec toggles et messages périmètre |
| Ambiguïté STRUCTURE / Cumul RH | Cartographie MOA explicite avant B2 |
| Budget partiel (axes sans ligne) | Afficher `—` + hint « axe non budgétisé » |
| Divergence réalisé budget vs analytics | Réalisé **jamais** recalculé côté budget |
| Rejection MOA après simplification | B1 utilisable sans B2 — pas de régression cockpit |
| Dette vendor | Ne pas installer Cybrosys |

---

## 12. Hors périmère V1 budget

- Registre bénévole et valorisation heures ;
- Ventilation salariale Palier 2 ;
- Écritures comptables ou analytiques auto ;
- OCA Budget / Enterprise budget ;
- Projections fin d’année / atterrissage automatique ;
- Bloc trésorerie budget vs réalisé ;
- Clôture analytique mensuelle ;
- Rapport PDF CA complet (spec V1.1 §11).

---

## 13. Décisions MOA attendues demain

### 13.1 Décisions structurantes (GO / NO GO)

| ID | Décision | Options |
|---|---|---|
| **D-MOA-01** | Relancer `dorevia_glc_budget` | GO / NON / REPORTER |
| **D-MOA-02** | Stratégie technique | Module dédié (reco) / Vendor / Autre |
| **D-MOA-03** | Périmètre Lot 1 | B1 seul / B1+B2a / B1+B2 complet |
| **D-MOA-04** | Scénario par défaut cockpit | `initial` / `revised` / choix utilisateur |

### 13.2 Décisions de règles métier

| ID | Décision |
|---|---|
| **D-MOA-05** | Budget période partielle : mois complet vs prorata |
| **D-MOA-06** | Budgétiser les 4 axes financement en V1 ? |
| **D-MOA-07** | Mapping `STRUCTURE` et cumul RH — voir §6.2 |
| **D-MOA-08** | Qui valide / déverrouille un budget ? |

### 13.3 Décisions UX

| ID | Décision |
|---|---|
| **D-MOA-09** | Menu « Budgets GLC » sous Pilotage GLC — OK ? |
| **D-MOA-10** | Colonnes écart visibles par défaut ou toggle ? |
| **D-MOA-11** | Import CSV en V1 ou V2 ? |

---

## 14. Recommandation finale équipe dev

| Sujet | Recommandation |
|---|---|
| Module vendor | **Ne pas installer** — inspiration UX seulement |
| Architecture | **Recréer `dorevia_glc_budget`** selon §5 |
| Séquence | **B1** (saisie) puis **B2b** (écarts détail) |
| Cockpit | Ne pas toucher tant que B1 non validé MOA |
| Référentiel | Plan unique 11 axes — pas de retour 2 plans |
| Documentation | Réactiver TICKET_PALIER_3 avec addendum plan unique |

---

## 15. Annexe A — Comparaison synthétique

| Critère | `base_account_budget` | `dorevia_glc_budget` |
|---|---|---|
| Axe principal | Comptes GL (postes) | Axes analytiques GLC |
| Scénarios | Non | `initial` / `revised` / `landing` |
| Lien cockpit GLC | À recoder entièrement | Natif |
| Réalisé | Calcul interne SQL | Délégué à analytics |
| Maintenance | Vendor externe | Stack Dorevia |
| Risque double lecture | Élevé | Faible (doctrine §5.1) |
| Effort V1 | Installation + customisation lourde | ~4–6 j (B1) |

---

## 16. Annexe B — Exemple de saisie budget (à valider MOA)

**Budget 2026 — initial — avril**

| Mois | Axe | Type | Montant prévu |
|---|---|---|---|
| 2026-04-01 | Prestation & Animation | `revenue` | 3 000 € |
| 2026-04-01 | Bar & Restau | `revenue` | 8 000 € |
| 2026-04-01 | *(axe RH / paie)* | `expense` | 8 500 € |
| 2026-04-01 | Frais généraux / STRUCTURE | `expense` | 1 200 € |
| 2026-04-01 | Subventions | `funding` | 5 000 € |

---

## 17. Annexe C — Mapping axes MOA (rappel)

| Libellé MOA | Code analytique |
|---|---|
| Bar & Restau | `BAR` |
| Prestation & Animation | `PRESTATIONS` |
| Privatisation Espace | `PRIVATISATIONS` |
| Résidence artiste | `RESIDENCES` |
| Déplacement & Mission | `MISSIONS` |
| Frais généraux | `STRUCTURE` |
| Adhésions | `ADHESIONS` |
| Dons | `DONS` |
| Subventions | `SUBVENTIONS` |
| Ressources propres | `RESSOURCES_PROPRES` |

*(Liste complète : menu Pilotage GLC → Axes analytiques.)*

---

## 18. Prochaines étapes si GO MOA

1. Valider les décisions §13 (compte-rendu réunion).
2. Mettre à jour [TICKET_PALIER_3.md](../dorevia_glc_analytics/docs/TICKET_PALIER_3.md) — addendum plan unique + statut « repris ».
3. Créer branche `feat/glc-budget-b1` — squelette module.
4. Développer Lot B1 + recette.
5. Atelier MOA Lot B2 (écarts cockpit) sur données réelles budget test.

---

*Fin du mémo — version 1.0 — 2026-05-30*
