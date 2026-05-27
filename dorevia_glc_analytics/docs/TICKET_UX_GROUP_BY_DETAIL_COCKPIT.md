# Ticket UX — Détail par activité avec sous-totaux mensuels

**Module :** `dorevia_glc_analytics`  
**Branche :** `feat/glc-cockpit-detail-groupby`  
**Version livrée :** `19.0.4.4.2`  
**Statut :** **GO MOA UX-GROUPBY** (2026-05-27) — implémentation **Option C : composant OWL custom** retenue après arbitrage  
**Prérequis :** Palier 4 période libre **GO avec réserves** sur `19.0.4.2.5`

**Références :** [TICKET_PALIER_4BIS.md](./TICKET_PALIER_4BIS.md) · [recette période libre](./recette/RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md) · [CADRAGE_FINAL_PALIER_4.md](./CADRAGE_FINAL_PALIER_4.md)

> **Note de lecture :** ce ticket conserve la **trajectoire complète d'arbitrage MOA** (cadrage initial, options A/A2/B/C, allers-retours UX). Le verdict final, les décisions techniques arbitrées et les caractéristiques de la version livrée sont en **section 11** en bas du document.

---

## 1. Contexte MOA

Le Palier 4 période libre est **fonctionnellement validé** (R1–R10 OK, `19.0.4.2.5`).

L’onglet **Détail par activité** reste toutefois **trop dense** en lecture multi-mois. Le tableau affiche aujourd’hui à plat :

- les lignes d’activité (`line_kind = activity`) ;
- les lignes artificielles `Total Janvier 2026`, `Total Février 2026`, … (`line_kind = month_total`) ;
- une ligne `Total période` (`line_kind = period_total`).

Cette approche fonctionne, mais n’exploite pas les mécanismes standards Odoo de **regroupement** et de **sous-total**.

**Décision MOA :** avec sous-totaux, **ne plus fabriquer visuellement des lignes « Total mois »** si Odoo sait déjà les produire proprement via `group_by` + `sum` sur colonnes numériques.

---

## 2. Objectif

Faire évoluer l’onglet **Détail par activité** vers une lecture Odoo native :

- regroupement par mois ;
- lignes d’activité dans chaque mois ;
- sous-total automatique par mois ;
- total général de période ;
- groupes pliables / dépliables.

---

## 3. Cible UX

```text
▾ Janvier 2026
   [BAR] Bar, Restauration & Cuisine
   [STRUCTURE] Structure & Administration
   Sous-total Janvier 2026

▾ Février 2026
   [BAR] Bar, Restauration & Cuisine
   [STRUCTURE] Structure & Administration
   Sous-total Février 2026

▾ Mars 2026
   ...

Total général période
```

Sur une période `01/01/2026 → 31/07/2026` :

- l’utilisateur voit les mois comme **groupes** ;
- il peut **plier / déplier** chaque mois ;
- chaque mois affiche ses lignes d’activité ;
- chaque mois affiche son **sous-total natif Odoo** ;
- le bas du tableau affiche le **total général** de la période ;
- **aucune ligne ambiguë** du type `Juillet | Total période` ne doit apparaître.

---

## 4. Principe technique

Utiliser le fonctionnement standard Odoo 19 :

- `group_by` sur un champ mois ;
- sommes natives sur les colonnes numériques (`sum="…"` sur les `<field>` monétaires) ;
- sous-totaux de groupe calculés par le client web ;
- total général en bas de liste.

### État actuel (à remplacer côté vue)

| Élément | Implémentation actuelle |
|---|---|
| Totaux mensuels | Lignes `month_total` créées en Python dans `_action_refresh_single()` |
| Total période | Ligne `period_total` créée en Python |
| Vue | `<list>` inline dans le formulaire cockpit, tri `period_date, line_kind` |
| Champs ligne | `period_date`, `month_label`, `line_kind`, montants `revenue_*`, `payroll_*`, `expense_*`, `variance_*` |

### Cible technique

| Élément | Cible |
|---|---|
| Vue principale | `<list>` avec `default_group_by="month_key"` *(ou équivalent Odoo 19)* |
| Lignes affichées | Uniquement `line_kind = activity` *(domaine ou filtre vue)* |
| Sous-totaux mensuels | Group footer Odoo — **plus de lignes `month_total` en vue** |
| Total période | Footer global liste (`sum` sur colonnes) — **plus de ligne `period_total` en vue** |
| Lignes `month_total` / `period_total` | Conserver en modèle si utile tests / RPC ; **masquer ou ne plus générer** si redondant |

### Règle de vue principale

La vue principale **Détail par activité** doit afficher **uniquement** les lignes :

- `line_kind = activity`

Le `group_by` et les sous-totaux natifs Odoo (`sum` sur colonnes) s’appliquent **exclusivement** sur ce périmètre.

Les lignes `month_total` et `period_total`, si elles sont conservées techniquement *(compatibilité, tests, RPC)*, doivent être **exclues de la vue principale** afin d’éviter tout **double comptage** avec les sous-totaux natifs Odoo. Elles ne doivent **jamais polluer** la vue utilisateur.

**Implémentation attendue :** domaine ou filtre vue sur `line_ids` limité à `activity` ; vérifier que les footers de groupe et le total général ne cumulent que ces lignes.

---

## 5. Champs nécessaires

### À confirmer / ajouter sur `glc.coverage.cockpit.line`

| Champ | Type | Rôle |
|---|---|---|
| `month_key` | `Char` *(store)* | Clé technique de tri et group_by — ex. `2026-01`, `2026-02` |
| `month_label` | `Char` | Libellé affichable groupe — ex. `Janvier 2026` *(existe déjà)* |
| `activity_label` | `Char` | Activité affichée *(existe déjà)* |
| `line_kind` | `Selection` | Conserver pour le moteur ; la vue filtre sur `activity` |
| `period_date` | `Date` | Conserver pour tri interne / compatibilité |

### Point critique — ordre chronologique

Le group_by ne doit **pas** produire un ordre alphabétique :

```text
Avril → Février → Janvier → Mars   ❌
```

Il doit respecter :

```text
Janvier → Février → Mars → Avril   ✅
```

**Piste :** `month_key` format `YYYY-MM` (tri lexicographique = tri chronologique) + `group_by` sur `month_key` avec libellé affiché via `month_label` ou `_groupby` custom si nécessaire.

---

## 6. Colonnes numériques avec sous-totaux

Les colonnes suivantes doivent porter `sum="…"` pour alimenter sous-totaux de groupe et total général :

| Colonne MOA | Champ technique actuel |
|---|---|
| Recettes réel | `revenue_realized` |
| Recettes budgétées | `revenue_budget` |
| Écart recettes | `variance_revenue` |
| Masse salariale réelle | `payroll_realized` |
| Masse salariale budgétée | `payroll_budget` |
| Écart masse salariale | `variance_payroll` |
| Frais généraux réels | `expense_realized` |
| Frais généraux budgétés | `expense_budget` |
| Écart frais généraux | `variance_expense` |

Exemple XML attendu *(noms de champs réels du module)* :

```xml
<field name="revenue_realized" sum="Total recettes réelles"/>
<field name="revenue_budget" sum="Total recettes budgétées"/>
<field name="variance_revenue" sum="Total écart recettes"/>
<!-- idem payroll_* et expense_* -->
```

### Note MOA — colonnes solde

Les soldes (**Solde réel / budgété / écart**) sont lus aujourd’hui dans l’onglet **Charges de structure**, pas dans le tableau détail (recette R9). **Hors périmètre V1** de ce ticket sauf décision MOA explicite d’ajouter ces champs sur `glc.coverage.cockpit.line`.

---

## 7. Critères d’acceptation

### UX-G1 — Groupement par mois

- [ ] La vue est regroupée par mois **par défaut**.
- [ ] Les mois sont dans l’**ordre chronologique**.
- [ ] Les groupes sont **lisibles et dépliables**.

### UX-G2 — Sous-totaux mensuels

- [ ] Chaque groupe mensuel affiche un **sous-total natif Odoo**.
- [ ] Le sous-total correspond à la somme des lignes activité du mois.
- [ ] Les lignes artificielles `Total <mois> <année>` **n’apparaissent plus** dans la vue principale.

### UX-G3 — Total général période

- [ ] Le **total général** de la période est visible en bas de liste.
- [ ] Il correspond à la somme des mois affichés.
- [ ] Il n’est **pas rattaché visuellement** au dernier mois *(pas de ligne `Juillet | Total période`)*.

### UX-G4 — Pas de régression fonctionnelle

- [ ] Filtres `date_from` / `date_to` / scénario **opérationnels**.
- [ ] Rafraîchissement R10 **OK** (pas d’erreur `cockpit_id`, data fraîches sans F5).
- [ ] Règles de calcul V1 **inchangées** (réalisé dates exactes, masse sal. mois complet, budget mois complet).
- [ ] Recette R1–R10 et **62 post-tests** verts.

### UX-G5 — Absence de double comptage

- [ ] Les sous-totaux Odoo ne cumulent **que** les lignes `activity`.
- [ ] Les lignes `month_total` / `period_total` ne sont **pas incluses** dans les sommes visibles.
- [ ] Le total général correspond à la somme des lignes activité **uniquement**.

---

## 8. Hors périmètre

- Nouveaux graphiques
- Export Excel / PDF
- Drill-down vers écritures comptables
- Arbitrage `STRUCTURE` / `payroll_budget`
- Modification des règles de calcul budgétaire
- Colonnes solde dans le tableau détail *(sauf décision MOA)*

---

## 9. Impacts dev prévus

| Zone | Impact |
|---|---|
| `models/glc_coverage_cockpit.py` | Ajout `month_key` ; option stop génération `month_total` / `period_total` si redondant |
| `views/glc_coverage_cockpit_views.xml` | `default_group_by`, domaine `line_kind=activity`, `sum` sur colonnes |
| `tests/test_coverage_cockpit.py` | Adapter assertions totaux ; conserver couverture agrégats |
| JS cockpit | Vérifier non-régression autosave filtres (`19.0.4.2.5`) |

---

## 10. Verdict attendu *(cadrage initial)*

Cette évolution est une **amélioration UX de lecture**.

Elle **ne remet pas en cause** le **GO avec réserves** Palier 4 période libre (`19.0.4.2.5`).

Elle vise à rendre le détail **exploitable comme une vraie vue Odoo** : groupée, repliable, avec sous-totaux natifs — **plus maintenable** que des lignes métier artificielles.

---

## 11. Verdict final MOA — `19.0.4.4.2` (2026-05-27)

### 11.1. Trajectoire d'arbitrage

| Étape | Version | Approche tentée | Verdict MOA |
|---|---|---|---|
| 1 | `19.0.4.3.0` | `default_group_by="period_date:month"` + `sum="…"` sur `<list>` x2many **inline** | **NO GO** — la liste reste plate ; les sous-totaux et le footer global ne s'affichent pas dans une liste x2many embarquée |
| 2 | `19.0.4.3.1` | Bouton « Voir le détail groupé » ouvrant une **act_window** vers une vraie vue list groupée Odoo (parcours principal) | **NO GO** — l'utilisateur ne doit pas sortir du cockpit pour lire le détail |
| 3 | `19.0.4.3.2` | Mêmes ajustements + correctifs annexes (`currency_id` stored, `display_title` stored, `_rec_name` ligne, `expand="1"` sur la vue list externe) | NO GO — fix techniques OK, mais parcours toujours hors cockpit |
| 4 | `19.0.4.3.3` (A2) | Lignes `month_total` / `period_total` matérialisées en base, `<list>` inline sans `sum=` natif, décorations Bootstrap | NO GO UX — impression de « tableau fabriqué », encadrement violet trop marqué, lignes sous-totaux assimilées à des records |
| 5 | `19.0.4.4.0` (C) | **Composant OWL custom** `glc_coverage_detail` — lecture seule, regroupement et sous-totaux **calculés côté client** sur les seules lignes `activity` produites par le backend | GO fonctionnel — UX à affiner |
| 6 | `19.0.4.4.1` | Affinage UX : bandeau mois sobre, header à 2 niveaux (familles Recettes / Masse salariale / Frais généraux), sous-totaux gras + italique, couleurs d'écart sobres | GO UX — polish à finaliser |
| 7 | **`19.0.4.4.2`** | Polish final : zéros → `—` atténué, double bordure noire sur Total période, suppression du lien externe | **GO MOA UX-GROUPBY** |

### 11.2. Constat technique acté

**Odoo 19 ne supporte pas le `group_by` natif avec sous-totaux dans une `<list>` x2many embarquée dans un formulaire.** Limite structurelle du framework web (composant `X2ManyField` qui n'expose pas d'API `read_group`). Confirmé en lisant le code source. La condition initiale du ticket (« ne plus fabriquer de Total mois si Odoo sait déjà les produire ») **tombe par construction** : Odoo ne sait pas les produire dans ce contexte.

→ Le seul moyen d'obtenir une lecture mensuelle structurée **directement dans l'onglet du cockpit** sans sortir vers une act_window est un **composant de présentation custom**.

### 11.3. Architecture retenue — Option C

| Couche | Responsabilité |
|---|---|
| **Backend** (`models/glc_coverage_cockpit.py`) | Calcul métier — produit uniquement des lignes `line_kind = activity` ; aucune ligne artificielle (`month_total` / `period_total`) en base → **UX-G5 garanti par construction** |
| **Vue** (`views/glc_coverage_cockpit_views.xml`) | `<field name="line_ids" widget="glc_coverage_detail" readonly="1"/>` dans l'onglet **Détail par activité** ; plus de `<list>` inline, plus de bouton externe |
| **Widget OWL** (`static/src/js/glc_coverage_detail_widget.esm.js`) | Présentation pure : regroupement par mois, calcul des sous-totaux et du total période côté client, formatage monétaire `formatMonetary` natif Odoo |
| **Template QWeb** (`static/src/xml/glc_coverage_detail_widget.xml`) | Table HTML 2 niveaux d'entête, bandeaux mois, lignes activité, sous-totaux mensuels, footer `<tfoot>` séparé pour Total période |
| **SCSS** (`static/src/scss/glc_coverage_detail_widget.scss`) | Style sobre aligné Bootstrap 5 / variables Odoo |

### 11.4. Caractéristiques UX validées MOA

**Structure**
- En-tête à 2 niveaux : familles métier **Recettes / Masse salariale / Frais généraux** + sous-libellés **Réel / Budget / Écart**
- Séparation verticale fine entre les 3 familles, propagée sur toutes les lignes
- Bandeau « mois » sobre : fond gris léger, majuscules petites, bordures fines 1 px (plus de violet marqué)
- Lignes d'activité indentées sous chaque mois, codes `[BAR]`, `[STRUCTURE]`, etc. conservés
- Sous-total mensuel : gras, libellé en italique, bordure supérieure fine, fond très léger
- **Total période** : `<tfoot>` séparé, **double bordure noire** (`3px double`), majuscules, fond gris léger — clairement non rattaché au dernier mois

**Lecture des montants**
- Alignement à droite homogène
- Format monétaire natif Odoo (`formatMonetary` + devise du cockpit)
- **Zéros → `—`** affichés en gris clair (`o_glc_zero`) — réduit drastiquement le bruit visuel dans les colonnes peu renseignées
- **Écarts colorés** sobrement : négatif `#b02a2a`, positif `#198754`, **zéro non coloré** (pas de rouge/vert sur 0)
- Sur sous-totaux mensuels, les écarts passent en gras supplémentaire

**Parcours**
- Lecture détaillée **entièrement contenue dans l'onglet Détail par activité**
- **Aucun lien externe exposé** à l'utilisateur (pas de bouton « Voir le détail groupé »)
- L'action serveur `action_open_detail_grouped()` et la vue list groupée Odoo native **restent disponibles côté code** (utiles pour réactivation future ou debug), mais **hors parcours MOA**

### 11.5. Critères UX-G1 à UX-G5 — état final

| Critère | Statut final | Implémentation |
|---|---|---|
| **UX-G1** Groupement par mois, ordre chronologique | **OK** | `month_key = YYYY-MM` trié lexicographique = chronologique |
| **UX-G2** Sous-totaux mensuels visibles | **OK** | Lignes `o_glc_subtotal_row` calculées côté OWL |
| **UX-G3** Total général période distinct, non rattaché au dernier mois | **OK** | `<tfoot>` séparé, double bordure noire |
| **UX-G4** Pas de régression : filtres, R10, calculs V1 | **OK** | 65 post-tests verts ; autosave filtres conservé (`19.0.4.2.5`) |
| **UX-G5** Absence de double comptage | **OK par construction** | Backend ne produit que des lignes `activity` — aucune ligne artificielle à exclure |
| **Pliable/dépliable** (objectif initial) | **Hors portée** | Limite framework Odoo 19 ; compromis MOA assumé : lecture entièrement affichée à plat dans l'onglet |

### 11.6. Tests automatisés

- `test_multi_month_detail_activity_only` — vérifie que le backend ne crée **aucune** ligne `month_total` / `period_total`
- `test_single_month_has_no_artificial_totals` — pas d'artefact en mois unique
- `test_detail_activity_sums_match_cockpit_aggregates` — cohérence sommes activité / agrégats cockpit
- `test_action_open_detail_grouped` — l'action serveur reste fonctionnelle (utilisable côté code)
- **65 post-tests verts, 0 failed, 0 error** sur `dorevia_glc_analytics` + `dorevia_glc_budget`

### 11.7. Points documentés MOA

- les zéros sont remplacés par `—` **uniquement en affichage cockpit** (pas en base, pas dans les exports/RPC) ;
- les **écarts nuls ne prennent pas de couleur** rouge/verte ;
- la ligne **TOTAL PÉRIODE** est distinguée par une **double bordure** noire ;
- le **lien externe** vers la vue liste groupée Odoo native **n'est plus exposé** à l'utilisateur ;
- l'**action technique** `action_open_detail_grouped` et sa vue list **restent disponibles côté code**, mais hors parcours MOA.

---

## 12. Complément fonctionnel — bloc PERFORMANCE (`19.0.4.5.0`)

**Statut :** **GO MOA fonctionnel** — 2026-05-27.

### 12.1. Objectif métier

Permettre de lire directement, par activité et par mois :

> Est-ce que chaque activité couvre ses charges réelles ?

### 12.2. Structure des colonnes (header widget)

```text
RECETTES | SALAIRES | FRAIS | PERFORMANCE
Réel     | Budget   | Écart
```

Renommages MOA :
- **Masse salariale** → **Salaires**
- **Frais généraux** → **Frais**

### 12.3. Formules

| Indicateur | Formule |
|---|---|
| Performance réelle | `revenue_realized - payroll_realized - expense_realized` |
| Performance budget | `revenue_budget - payroll_budget - expense_budget` |
| Écart performance | `performance_realized - performance_budget` |

Disponible sur :
- chaque ligne activité ;
- chaque sous-total mensuel (agrégation des montants de base puis formule) ;
- la ligne **TOTAL PÉRIODE**.

### 12.4. Implémentation

| Couche | Détail |
|---|---|
| Modèle `glc.coverage.cockpit.line` | Champs calculés `performance_realized`, `performance_budget`, `variance_performance` |
| Widget OWL | Bloc PERFORMANCE + libellés Salaires/Frais ; sous-totaux et total période via `computePerformanceAmounts()` |
| Affichage | Zéros → `—` ; performance/écart positifs vert discret, négatifs rouge discret ; zéro non coloré |

### 12.5. Tests

- `test_activity_line_performance_formula`
- `test_multi_month_performance_sums_from_activity_lines`

---

## 13. Finition UX — séparation visuelle des familles (`19.0.4.5.1`)

**Statut :** **GO MOA UX** — 2026-05-27.

### 13.1. Objectif

Renforcer la lecture en **4 blocs métier distincts** (RECETTES | SALAIRES | FRAIS | PERFORMANCE), et non une suite continue de 12 colonnes.

### 13.2. Implémentation (SCSS + classes XML)

| Élément | Détail |
|---|---|
| Séparateurs verticaux | Après chaque colonne **Écart** des blocs Recettes, Salaires et Frais : `border-right: 1px solid #d6d9de` + `padding-right: 14px` |
| Respiration inter-blocs | `padding-left: 14px` au début des blocs Salaires et Frais |
| Headers familles | `font-weight: 700`, `letter-spacing: 0.04em`, fond `#f3f4f6`, `border-radius: 3px`, `padding: 2px 6px` |
| Bloc Performance | Légèrement détaché : `border-left: 2px solid #b8bdc5`, `padding-left: 16px`, fond discret `#f8f9fa` sur les 3 colonnes |

### 13.3. Conservé sans régression

Bandeaux mois, sous-totaux mensuels, double bordure TOTAL PÉRIODE, zéros `—`, couleurs vert/rouge sur valeurs non nulles, aucun lien externe/fallback exposé.

### 13.4. Verdict MOA — cible UX validée

La vue **Détail par activité** est la **cible UX validée** pour ce palier (`19.0.4.5.1`) :

- blocs clairement séparés ;
- lecture immédiate des 4 familles métier ;
- performance calculée sur lignes activité, sous-totaux mensuels et total période ;
- parcours utilisateur entièrement contenu dans le cockpit.

### 13.5. Polish optionnel — fond bloc Performance (`19.0.4.5.2`)

Fond gris bleuté très discret `#f8f9fa` sur les 3 colonnes Performance (header, lignes, sous-totaux, total période). Polish non bloquant — renforce la lecture « indicateur synthétique / conclusion » sans alourdir le tableau.

---

*Ticket rédigé MOA — 2026-05-27.  
Verdict final MOA UX-GROUPBY — 2026-05-27 (version livrée `19.0.4.4.2`).  
Complément PERFORMANCE — `19.0.4.5.0` — GO MOA fonctionnel 2026-05-27.  
Finition séparation familles — `19.0.4.5.1` — GO MOA UX 2026-05-27 — **cible UX validée pour ce palier**.*
