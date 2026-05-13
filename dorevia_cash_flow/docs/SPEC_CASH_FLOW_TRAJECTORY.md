# Spécification technique — Trajectoire de trésorerie (`dorevia_cash_flow`)

**Version cible** : V1 (alignement [README](../README.md)).  
**Statut** : **validée pour développement V1** (arbitrages produit / technique intégrés ci-dessous).

---

## Décisions validées V1

| Thème | Décision |
| --- | --- |
| **Rendu graphique** | **Option A** retenue : vue **Graph** Odoo native sur modèle transitoire de points. Pas d’OWL ni de Chart.js en V1. Si le rendu natif s’avère insuffisant visuellement, documenter l’écart en recette et reporter une **V2** éventuelle en client action OWL (§ 5.4). |
| **Périodicité** | **Restriction stricte** : seules les projections avec `periodicity == 'week'` sont éligibles. Sinon : **message utilisateur clair** (pas de courbe mensuelle / trimestrielle qui contredirait le README). |
| **Raccord constaté / projeté** | Dernier point **constaté** : `anchor_date = situation_date`, `balance = guard.observed_balance`. Partie **projetée** : mailles `forecast` suivantes uniquement ; **pas** de second point en `situation_date` côté projeté — la bascule visuelle et fonctionnelle est ce dernier point constaté ; le graph relie ce point au premier point `forecast` sans ambiguïté de double marqueur. |
| **Point bas** | Calculé **exclusivement** sur les points **effectivement affichés** dans la courbe. `guard.forecast_min_balance` / `min_balance_date` : **contrôle** ou tests uniquement, pas source d’affichage du point bas du rapport. |
| **Seuil d’alerte** | Afficher dans le graph **si** la vue Graph le permet **sans complexifier** la V1 (ex. mesure secondaire). **À défaut** (ou en complément) : bandeau / en-tête du wizard avec seuil + point bas. **Priorité V1** : courbe lisible, point bas, séparation constaté / projeté. |
| **Sécurité** | Même périmètre que la **lecture des projections Cash Guard** : groupe **`dorevia_cash_guard.group_cash_guard_user`** pour le menu et l’accès aux transients. Pas d’élargissement aux seuls utilisateurs comptables sans ce groupe tant que les droits ne sont pas repris en revue produit. |
| **Recalcul** | **Interdit** : `dorevia_cash_flow` ne doit **jamais** appeler automatiquement `action_recompute_projection()`. Si `weekly_line_ids` est vide ou manifestement obsolète : **message** invitant l’utilisateur à ouvrir le document dans **Projections de trésorerie** (Cash Guard) et à y déclencher le recalcul. |
| **Extensibilité** | Le transient `dorevia.cash.flow.trajectory.point` inclut `series_key`, `series_label`, `series_type`, `fiscal_week_index` pour préparer V2+ **sans** ajouter de séries comparatives en V1 (voir § 2.3.1). |

---

## 1. Dépendances module

### 1.1 Manifeste (`__manifest__.py`)

| Dépendance | Motif |
| --- | --- |
| `account` | Menus sous **Comptabilité**, société, devise, exercices fiscaux (`res.company`), cohérence avec le périmètre comptable standard. |
| `dorevia_cash_guard` | Source métier unique des projections : modèle `dorevia.cash.guard`, mailles `dorevia.cash.guard.week`, méthodes de solde bancaire déjà alignées sur le périmètre des journaux de la projection. |
| `web` | Interface backend (actions fenêtre, vues graphique standard — **pas** d’assets OWL dédiés en V1). |

**Non requis pour la V1** (sauf décision contraire) : `dorevia_cash_simulation` — aucune dépendance directe ; les montants éventuellement issus de la simulation restent ceux déjà matérialisés dans les lignes / mailles Cash Guard.

### 1.2 Rendu graphique (V1)

**Retenu** : **vue Graph** Odoo sur un modèle transitoire (`dorevia.cash.flow.trajectory.point`) + mesure secondaire pour le seuil **uniquement si** simple à mettre en œuvre (voir § 5.3 et tableau « Décisions validées »).

Avantages : peu de JavaScript, maintenance standard, conformité à l’objectif « restitution graphique simple ».

**V2 (hors périmètre V1)** : client action OWL + librairie de graphiques si le constat de recette documente une insuffisance visuelle de la vue native.

---

## 2. Modèles Odoo à créer ou réutiliser

### 2.1 Modèles réutilisés (lecture seule)

| Modèle | Usage |
| --- | --- |
| `dorevia.cash.guard` | Document de projection sélectionné ; champs `situation_date`, `date_from`, `date_to`, `company_id`, `currency_id`, `periodicity`, `liquidity_journal_ids`, `bank_journal_id`, `alert_threshold`, `observed_balance`, `forecast_min_balance`, `min_balance_date`, etc. Relation One2many vers les mailles : **`weekly_line_ids`** (nom exact dans le code Cash Guard). |
| `dorevia.cash.guard.week` | Mailles de suivi (`dorevia.cash.guard.week`), lues via **`guard.weekly_line_ids`** : `week_index`, `week_label`, `date_from`, `date_to`, `period_type` (`historical` / `current` / `forecast`), `projected_balance`, `closing_balance`. |

**Ne pas** modifier ces modèles depuis `dorevia_cash_flow` (hors périmètre — § 6).

### 2.2 Méthodes Cash Guard à réutiliser (appel lecture)

| Méthode | Modèle | Rôle |
| --- | --- | --- |
| `_compute_bank_balance_at_date(target_date)` | `dorevia.cash.guard` | Solde de trésorerie à une date sur les **mêmes** journaux que la projection sélectionnée (logique déjà homogène avec le constaté Cash Guard). |
| `_liquidity_journals()` | idem | Vérifications éventuelles (déjà garanties par les contraintes du guard). |

**Remarque** : ces méthodes ne sont pas une API publique documentée ; en V1 on les **appelle depuis le même serveur** en tant que module dépendant. Si à terme Dorevia souhaite figer un contrat, une extraction vers un mixin partagé pourra être envisagée **hors** périmètre `dorevia_cash_flow` V1.

### 2.3 Modèles à créer dans `dorevia_cash_flow`

#### A. `dorevia.cash.flow.trajectory.wizard` (`TransientModel`)

| Champ | Type | Description |
| --- | --- | --- |
| `guard_id` | `Many2one('dorevia.cash.guard', required=True)` | Projection source. Domaine recommandé : même `company_id` que `env.company`, `active=True` (sauf besoin d’inclure les archivés — par défaut **exclure** les documents `active=False` pour coller à l’usage courant). |
| `company_id` | `Many2one` related ou calculé depuis `guard_id` | Filtrage droits / cohérence. |
| `situation_date` | `Date` related `guard_id.situation_date` | Affichage et trace dans l’UI. |
| `chart_date_end` | `Date` compute | `situation_date + 90 jours` (règle métier README). |
| `fiscal_date_from` | `Date` compute | Début d’exercice fiscal **courant** contenant `situation_date` (voir § 3.3). |
| `point_ids` | `One2many` vers `dorevia.cash.flow.trajectory.point` | Rempli par `action_build_series()` (ou équivalent). |
| Champs d’info (compute / readonly) | `Monetary` / `Char` | Ex. `min_balance_on_curve`, `min_balance_date_on_curve`, `alert_threshold` (copie pour affichage en bandeau), message d’éligibilité si `periodicity != 'week'` ou si `weekly_line_ids` vide (voir § 4.3 et § 4.5). |

Méthodes :

- `action_open_chart()` : (re)construit les lignes `point_ids`, retourne `ir.actions.act_window` en mode `graph` (+ `list` secondaire) sur `dorevia.cash.flow.trajectory.point` avec domaine `[('wizard_id', '=', self.id)]` (ou recréation à chaque ouverture avec id wizard — pattern classique : wizard garde son id en transient jusqu’à expiration).

#### B. `dorevia.cash.flow.trajectory.point` (`TransientModel`)

Une ligne = **un point** affiché sur l’axe temporel (fin de période de constaté ou maille projetée).

| Champ | Type | Description |
| --- | --- | --- |
| `wizard_id` | `Many2one` vers le wizard | Lien parent. |
| `sequence` | `Integer` | Ordre d’affichage strict (tri chronologique — § 4.4). |
| `anchor_date` | `Date` | Date de référence du point (typiquement **fin de maille** ou borne utilisée pour le constaté hebdomadaire — § 4). |
| `label` | `Char` | Libellé abscisse (ex. `S12`, ou `DD/MM` si besoin). |
| `balance` | `Monetary` | Ordonnée principale : trésorerie sur la courbe. |
| `segment` | `Selection` `[('actual', 'Constaté'), ('projected', 'Projeté')]` | Qualifie le **segment de courbe** (`actual` / `projected`) pour liste, export, bandeau et V2 ; **pas** utilisé comme deuxième série dans la vue Graph V1 (voir § 5.3 — éviter les zéros artificiels). |
| `series_key` | `Char` | Clé technique stable de la série (V1 : `current_actual`, `current_projected`). Permet d’ajouter en V2 `prior_year_actual`, `budget`, `scenario_avg`, etc. sans refondre le modèle. |
| `series_label` | `Char` | Libellé affichable (V1 : libellés ci-dessous § 2.3.1). |
| `series_type` | `Selection` (extensible) | V1 : `actual`, `projected`. Prévoir en base les valeurs futures documentées (`historical`, `budget`, `scenario`, …) même si non utilisées en UI V1 — implémentation typique : `Char` contrôlé par constantes Python **ou** `Selection` enrichi lors des évolutions. |
| `fiscal_week_index` | `Integer` | Rang de la semaine **dans l’exercice fiscal courant** (1 = première semaine calendaire qui intersecte `[fiscal_date_from, …]` selon la même convention de découpe hebdomadaire que pour les points constatés). V1 : alimenté pour chaque point ; utilisé surtout en V2 pour aligner N, N-1, N-2 sur le même axe d’index sans comparer brutalement des dates civiles différentes. |
| `alert_threshold` | `Monetary` (related ou copie) | Dupliqué par point pour permettre une **deuxième mesure** plate dans le graph (si retenu en Option A). |
| `currency_id` | `Many2one` related `guard_id.currency_id` | Champ devise des Monetary. |

**Alternative** : un seul modèle transitoire avec champs JSON pour la série et une client action — moins idiomatique en Odoo ; non recommandé sauf contrainte forte.

##### 2.3.1 Extensibilité des séries (architecture V1 / évolutions)

La **V1** graphique n’affiche qu’**une** trajectoire (mesure `balance` dans le temps) ; les métadonnées `series_*` / `segment` servent à qualifier les points (liste, exports, V2). Des **trajectoires comparatives** distinctes (N-1, budget, scénario, etc.) restent hors périmètre V1 mais le schéma de point les accueillera sans refonte.

**Alimentation V1** (pour chaque ligne `dorevia.cash.flow.trajectory.point` créée) :

| Segment constaté (`segment=actual`) | Segment projeté (`segment=projected`) |
| --- | --- |
| `series_key = "current_actual"` | `series_key = "current_projected"` |
| `series_label = "Constaté exercice courant"` (libellé FR ; traduction i18n à prévoir) | `series_label = "Projeté 90 jours"` |
| `series_type = "actual"` | `series_type = "projected"` |

**Hors périmètre V1 — comparaison N-x** :

> La comparaison avec les trajectoires d’exercices antérieurs (N-1, N-2, …) est **hors périmètre V1**. Le modèle de points reste toutefois **extensible** via une notion de **série typée** (`series_key`, `series_label`, `series_type`, `fiscal_week_index`) afin de permettre ultérieurement des comparaisons historiques, budgétaires ou par scénario **sans** élargir le périmètre fonctionnel livré en V1.

En V1, la vue Graph n’emploie **pas** `segment` comme dimension de série (voir § 5.3) ; `segment` et les champs d’extension restent visibles dans la **liste** des points et pour les évolutions V2 (couleurs par segment sur une seule courbe, etc.).

### 2.4 Sécurité

- **Règles d’accès** : droits CRUD sur les transients réservés aux utilisateurs autorisés à utiliser le rapport (même périmètre que Cash Guard en lecture).
- **Groupes (V1 validé)** : menu `ir.ui.menu`, actions et modèles `dorevia.cash.flow.*` — **`groups="dorevia_cash_guard.group_cash_guard_user"`** (identique à la lecture des **Projections de trésorerie**). Pas d’accès élargi aux seuls groupes comptables génériques sans ce groupe en V1.

---

## 3. Mapping des données

### 3.1 Date de situation (`situation_date`)

| Élément | Valeur |
| --- | --- |
| Champ Odoo | `dorevia.cash.guard.situation_date` (`fields.Date`) |
| Sémantique | Identique au README : borne de bascule **constaté / projeté** ; en base, valeur maintenue par Cash Guard (recalcul lors des `write` / `action_recompute_projection`, avec garde-fous `allow_cash_guard_situation_write`). |

`dorevia_cash_flow` **ne modifie jamais** `situation_date`.

### 3.2 Horizon du projeté

| Niveau | Règle |
| --- | --- |
| Métier (documentation) | Partie projetée : **`situation_date` → `situation_date + 90 jours`** (inclus selon convention de borne retenue en implémentation — à documenter dans l’aide du rapport). |
| Implémentation | `chart_date_end = situation_date + timedelta(days=90)` (utiliser `date` Python / API Odoo dates). |

**Alignement avec Cash Guard** : à l’état actuel du code, la création / réalignement d’un document utilise `date_to` cohérent avec un horizon **90 jours** à partir de la situation. Le champ `dorevia.cash.guard.date_to` peut servir de **contrôle de cohérence** (ex. avertissement si `date_to` ≠ `situation_date + 90` pour d’anciens documents), mais **l’horizon graphique V1** reste **toujours** `situation_date + 90` pour respecter le README.

### 3.3 Début d’exercice comptable courant

| Élément | Proposition technique |
| --- | --- |
| Source | `guard.company_id` + API standard Odoo comptabilité pour les bornes d’exercice fiscal contenant `situation_date`. |
| Référence typique | `company.compute_fiscalyear_dates(situation_date)` → dictionnaire avec `date_from` / `date_to` de l’**exercice fiscal courant** (selon paramètres `fiscalyear_last_month` / `fiscalyear_last_day` de la société). |
| Champ dérivé | `fiscal_date_from =` résultat `date_from` ci-dessus. |

Si l’API ou le nom exact diffère selon version Odoo 19 du projet, l’implémentation doit **s’aligner sur la même source** que le reste des rapports comptables Dorevia (vérifier dans le codebase `res.company` / `account` du vendor).

### 3.4 Partie projetée — semaines et montants

| Donnée | Source |
| --- | --- |
| Mailles | `guard.weekly_line_ids` (`dorevia.cash.guard.week`), tri `week_index`. |
| Filtre temporel | Uniquement les mailles avec **`period_type == 'forecast'`**, tri `week_index`, telles que l’intervalle intersecte `]situation_date, chart_date_end]` (ex. `date_to <= chart_date_end` et pas de maille entièrement « avant » la zone projetée — cohérent avec § 4.2). |
| Ordonnée principale | `projected_balance` — **aligné sur la colonne « Projection »** du suivi Cash Guard (cumul situation + factures ouvertes + logique déjà appliquée dans `_sync_weekly_lines`). |

**Ne pas** recalculer une trajectoire parallèle à partir de `dorevia.cash.guard.line` seul en V1 : la vérité affichage projeté = **mailles** `dorevia.cash.guard.week` déjà synchronisées.

### 3.5 Partie constatée — solde réel

| Donnée | Source |
| --- | --- |
| Méthode | `guard._compute_bank_balance_at_date(d)` pour chaque date d’ancrage `d` du segment constaté (§ 4.1). |
| Périmètre journaux | Celui de `guard` (déjà encapsulé dans `_compute_bank_balance_at_date`). |

Cela garantit la cohérence avec le **solde constaté** utilisé par Cash Guard sur les mêmes journaux.

### 3.6 Seuil d’alerte et point bas

| Élément | Source / règle V1 |
| --- | --- |
| Seuil | `guard.alert_threshold`. **Graph** : mesure secondaire « plate » **si** faisable simplement dans la vue Graph native. **Sinon** (ou en complément) : affichage obligatoire dans le **bandeau / en-tête** du wizard. |
| Point bas (indicateur) | **Minimum** des `balance` sur **uniquement** les points de la **série affichée** (constaté + projeté sur l’horizon du rapport). **Ne pas** prendre `guard.forecast_min_balance` comme valeur affichée du point bas (écart possible avec la série tronquée à `situation_date + 90 j`). Utilisation de `forecast_min_balance` / `min_balance_date` réservée aux **tests de cohérence** ou analyses internes. |

---

## 4. Construction de la série graphique

### 4.1 Segment constaté

**Intervalle métier** : du **début d’exercice fiscal courant** (`fiscal_date_from`) jusqu’à **`situation_date`** (README).

**Granularité** : **hebdomadaire** — pas de sous-échantillonnage quotidien en V1.

**Algorithme V1** :

1. Construire les points intermédiaires constatés : bornes de **fin de semaine** (alignement ISO / politique Dorevia identique à Cash Guard pour `periodicity == 'week'`) de `fiscal_date_from` jusqu’à **strictement avant** `situation_date` : pour chaque borne `d` avec `d < situation_date`, `balance = guard._compute_bank_balance_at_date(d)`, `segment='actual'`.
2. **Dernier point constaté (obligatoire)** : `anchor_date = situation_date`, `balance = guard.observed_balance`, `segment='actual'` — c’est la **bascule fonctionnelle** alignée sur le document Cash Guard.
3. Tests : si un écart apparaît entre le dernier `_compute_bank_balance_at_date` avant `situation_date` et `observed_balance`, la **vérité affichée** au dernier point constaté reste **`observed_balance`**.
4. Pour chaque point constaté : renseigner **`fiscal_week_index`** (incrément 1-based depuis la première semaine d’exercice touchée par le constaté, même convention de bornes que les `anchor_date` intermédiaires — § 2.3.1).
5. Sur **chaque** point constaté : renseigner aussi `series_key`, `series_label`, `series_type` selon le tableau § 2.3.1 (colonne constaté).

**Segment** : `segment='actual'`.

### 4.2 Segment projeté

**Intervalle métier** : après la date de situation, jusqu’à **`chart_date_end`** (`situation_date + 90 jours`).

**Source des points** : uniquement les mailles `dorevia.cash.guard.week` avec **`period_type == 'forecast'`** intersectant l’horizon `]situation_date, chart_date_end]` (implémentation : filtrer les `forecast` avec `date_to <= chart_date_end` et exclure toute maille entièrement avant ou égale à `situation_date` si la maille ne porte que du constaté — cohérent avec l’exclusion du double point en `situation_date` côté projeté).

- Abscisse : `date_to` de la maille (ou `week_label` selon le rendu Graph) ; ordonnée : **`projected_balance`**. Renseigner **`fiscal_week_index`** pour chaque point projeté (suite logique du compteur fiscal après les semaines constatées, ou index dérivé de `anchor_date` dans le même référentiel 1…n d’exercice — à implémenter de façon **déterministe** et documentée pour que N / N-1 futurs partagent la même définition).

**Raccord visuel** : le dernier point **constaté** est déjà en `(situation_date, observed_balance)`. Les points **projetés** commencent à la **première maille `forecast`** ; **aucun** point supplémentaire en `situation_date` avec `segment='projected'`. La courbe joint naturellement le dernier constaté au premier `forecast` (lisibilité, pas d’ambiguïté de double marqueur à la bascule).

Sur **chaque** point projeté : `series_key`, `series_label`, `series_type` selon le tableau § 2.3.1 (colonne projeté).

**Segment** : `segment='projected'`.

### 4.3 Périodicité du guard (V1)

Le modèle `dorevia.cash.guard` autorise `periodicity` ∈ `week` / `month` / `quarter`. Le README impose une **trajectoire hebdomadaire**.

**Règle V1 validée** :

- **Éligibilité** : uniquement `periodicity == 'week'`.
- **Comportement** si `periodicity != 'week'` : **pas** de génération de courbe ; afficher un **message clair** (wizard ou `UserError` à l’action « Afficher la trajectoire ») expliquant que seules les projections à mailles hebdomadaires sont prises en charge et invitant à dupliquer / créer une projection hebdomadaire si besoin.
- **Domaine du many2one** `guard_id` (recommandé) : inclure `('periodicity', '=', 'week')` pour limiter la sélection ; conserver la validation côté bouton si le domaine est contourné.

### 4.4 Tri chronologique

- Trier les `dorevia.cash.flow.trajectory.point` par `(anchor_date, sequence)` croissant.
- `sequence` incrémenté monotoniquement lors de la construction (constaté puis projeté).

### 4.5 Semaines sans mouvement / sans donnée

| Cas | Comportement |
| --- | --- |
| Semaine constatée sans écriture | `_compute_bank_balance_at_date` retourne quand même un solde (souvent plat) — **point affiché**. |
| Aucune maille projetée dans l’horizon (donnée vide) | Afficher message « Pas de mailles projetées pour cet horizon » + constaté seul si applicable. |
| `weekly_line_ids` vide ou données manifestement absentes | **Aucun** appel à `guard.action_recompute_projection()` depuis `dorevia_cash_flow`. Afficher un **message explicite** invitant l’utilisateur à ouvrir le document dans **Projections de trésorerie** (Cash Guard) et à y lancer le recalcul / actualisation. Ne pas ouvrir de vue Graph vide sans explication. |

---

## 5. Vue / interface

### 5.1 Menu

- **Chemin** : **Comptabilité > Analyse > Trajectoire de trésorerie** (conforme README).
- **Implémentation** : `ir.ui.menu` avec `parent` = menu parent standard des analyses comptables Odoo 19 du projet (souvent sous `account.menu_finance_reports` ou équivalent « Analyse » — **à vérifier** dans les XML `account` / personnalisations Dorevia pour l’id exact du parent « Analyse »).
- **Action** : `ir.actions.act_window` sur `dorevia.cash.flow.trajectory.wizard` en vue **form** (mode single page).

### 5.2 Flux utilisateur

1. L’utilisateur ouvre le menu → formulaire wizard.
2. Choisit `guard_id` (many2one, recherche par nom / société).
3. Clique sur **« Afficher la trajectoire »** (libellé à valider) → méthode qui purge/crée les `point_ids` puis ouvre une fenêtre **graph** (+ liste optionnelle) sur `dorevia.cash.flow.trajectory.point`.

### 5.3 Affichage graphique (vue Graph native, V1)

- **Modèle métier d’un point** : `anchor_date` = date du point ; `balance` = **solde de trésorerie** à cette date ; `segment` = `actual` ou `projected` et **qualifie le segment de courbe**, sans constituer une deuxième trajectoire indépendante. **Priorité V1** : lecture **correcte** de la trajectoire (une courbe, pas de zéros artificiels hors plage) ; la distinction visuelle fine constaté / projeté passe derrière si le natif ne la permet pas sans artefacts.
- **Type** : `graph` view (`type="line"`), **une seule mesure** `balance`, axe temporel `anchor_date` (tri implicite / ordre des points selon le moteur). **Ne pas** utiliser `segment` (ni deux mesures `balance_actual` / `balance_projected`) en dimension « colonne » : le moteur Graph complète alors les séries par des **zéros** hors segment, ce qui contredit la trajectoire métier (deux segments successifs d’**une** courbe, pas deux courbes parallèles).
- **Lecture constaté / projeté** : continuité sur la **même ligne** ; le détail `segment` / `series_label` est porté par la **vue liste** des points (et les champs du transient pour export / V2).
- **Seuil d’alerte** : bandeau wizard (décision V1) ; deuxième mesure « plate » dans le graph seulement si évolution ultérieure sans effet de bord sur la série principale.
- **Point bas** : **toujours** dans le bandeau / en-tête du wizard : montant + date, calculés sur la série construite (voir tableau « Décisions validées »). Les **repères visuels idéaux** dans le graphique (ligne verticale à la situation, horizontale au seuil, marqueur du point bas) sont décrits dans **`docs/RECETTE_VUE_GRAPH.md`** ; en V1 natif ils ne sont en général **pas** tracés dans le graph (voir § 5.4).

### 5.4 Écart visuel natif → V2 (OWL / Chart.js)

Le **rendu cible** inclut idéalement : **ligne verticale** à la date de situation, **ligne horizontale** au seuil d’alerte, **marqueur du point bas**, tout en conservant **une seule courbe** `date / balance` sans zéros artificiels (voir `docs/RECETTE_VUE_GRAPH.md`).

La vue **Graph native** Odoo V1 ne couvre en général **pas** ces repères dans le graphique sans contournement lourd ou sans dégrader la lecture (double série, etc.). Ces écarts sont **documentés en recette** ; la **V2** prévue est une **client action OWL** (ex. Chart.js) dans `dorevia_cash_flow`, **sans** modifier les assets de `dorevia_cash_guard`.

---

## 5.5 V1.1 — Trajectoire de référence (sélection automatique)

Document de cadrage / recette associé : **`docs/TICKET_CASH_FLOW_V1_1_TRAJECTOIRE_REFERENCE.md`**.  
Doctrine transverse Cash (positionnement vs Cash Guard et simulation) : **`../../docs/cash/DOCTRINE_CASH_MODULES.md`**.

**Objectif** : le parcours principal ne impose plus de choisir une projection dans un formulaire avant d’afficher la courbe.

**Règle de résolution** (`dorevia.cash.flow.trajectory.wizard._resolve_reference_guard`) :

1. `company_id` = société courante (`env.company`) ;
2. `dorevia.cash.guard` avec `active = True` ;
3. `periodicity == 'week'` ;
4. au moins une ligne dans `weekly_line_ids` (mailles calculées) ;
5. parmi les candidats, tri **`situation_date` décroissant**, puis `write_date`, puis `id` — **premier** document retenu.

**Ouverture menu** : `ir.actions.server` exécute `action_open_reference_trajectory()` — création d’un transient wizard avec le `guard_id` résolu, génération des `dorevia.cash.flow.trajectory.point`, retour `ir.actions.client` vers le graphique de pilotage (identique au flux « Afficher la trajectoire » après sélection manuelle).

**Absence de candidat** : `UserError` avec message orientant vers la création ou l’actualisation d’une projection dans Cash Guard — **aucune** courbe vide.

**Parcours secondaire** : `ir.actions.act_window` sur le wizard (formulaire) + bouton **Changer de projection** côté client action — **aucun** recalcul Cash Guard automatique depuis `dorevia_cash_flow`.

---

## 6. Hors périmètre technique

| Interdit en V1 |
| --- |
| Appel automatique ou implicite à `action_recompute_projection()` (ou tout recalcul équivalent) depuis `dorevia_cash_flow`. |
| Recalcul complet de projection déclenché par l’ouverture du rapport ou la construction des points. |
| Écriture sur `dorevia.cash.guard`, `dorevia.cash.guard.week`, `dorevia.cash.guard.line`, `dorevia.cash.guard.period.move` depuis `dorevia_cash_flow`. |
| Logique métier **simulation** (sélection de devis / commandes, scénarios, comparaison réel / simulé, multi-courbes). |
| Dépendance ou imports « profonds » vers `dorevia_cash_simulation`. |
| Trajectoires comparatives **N-1 / N-2** (ou budget / scénarios **en tant que séries additionnelles**) — le modèle de points reste **préparé** (§ 2.3.1) mais aucune donnée ni courbe secondaire en V1. |

---

## 7. Critères de recette technique

| # | Critère |
| --- | --- |
| 1 | Installation du module `dorevia_cash_flow` sans erreur sur une base avec `account` + `dorevia_cash_guard` installés. |
| 2 | Menu **Comptabilité > Analyse > Trajectoire de trésorerie** visible pour le groupe cible (§ 2.4). |
| 3 | Ouverture du menu **Trajectoire de trésorerie** : résolution automatique d’une projection de référence (§ 5.5) et affichage du graphique **sans** sélection préalable obligatoire ; parcours secondaire avec assistant toujours disponible. |
| 4 | Affichage d’une courbe (graph) avec au moins un point constaté et, si données présentes, au moins un point projeté. |
| 5 | Dernier point constaté (ou point à `situation_date`) cohérent avec `observed_balance` du guard (tolérance arrondi monétaire). |
| 6 | Aucun point projeté avec `anchor_date` (ou borne de maille) **strictement supérieur** à `situation_date + 90 jours` selon la convention de borne retenue. |
| 7 | Montants projetés sur l’horizon = valeurs `projected_balance` des mailles `forecast` sélectionnées (tests sur jeu de données fixé). |
| 8 | Aucune création / modification de données Cash Guard lors de l’ouverture du rapport (vérifier en comptant les `write` sur `dorevia.cash.guard` ou absence d’appel `action_recompute_projection`). |
| 9 | Tests automatisés Python (module `tests/`) couvrant au minimum : construction de série sur un guard en `periodicity='week'` avec `weekly_line_ids` peuplés ; cas limite `weekly_line_ids` vide (message, **sans** `action_recompute_projection`) ; **V1.1** : ouverture référence sans sélection manuelle, message si aucun guard éligible, priorité `situation_date` pour le choix automatique. |
| 10 | Projection avec `periodicity != 'week'` : refus avec message clair (pas de courbe). |
| 11 | Point bas affiché = minimum sur les `point_ids` générés ; cohérence optionnelle en test avec les agrégats Cash Guard hors troncature. |

---

## 8. Points ouverts (implémentation)

1. **Parent du menu « Comptabilité > Analyse »** : implémentation V1 retenue — **`account.menu_finance_reports`** (menu standard *Reporting* / traduction souvent *Analyse*). Ajuster le `parent` dans `views/menus.xml` si une personnalisation du projet place les rapports d’analyse ailleurs.
2. **Cockpit sous Projection** : entrée **Projection > Cockpit trésorerie** dans `views/cash_guard_bridge_menus.xml` — même résolution de référence et même client action que la trajectoire Analyse ; paramètre `cockpit` sur l’action client pour masquer les contrôles d’audit sur le graphique et afficher les raccourcis atelier (sans second moteur graphique).

Les arbitrages groupes, périodicité, rendu Graph vs OWL et recalcul automatique sont **clos** pour la V1 (section « Décisions validées V1 »).

---

## 9. Références code (Cash Guard)

Fichiers utiles pour l’implémentation :

- `dorevia_cash_guard/models/cash_guard.py` — champs `situation_date`, `date_to`, `observed_balance`, `_compute_bank_balance_at_date`, `_split_exercise_periods`, `action_recompute_projection`.
- `dorevia_cash_guard/models/cash_guard_week.py` — champs `period_type`, `projected_balance`, `date_from`, `date_to`, `week_index`.

Cette spécification doit rester **alignée** sur le [README](../README.md) ; en cas de divergence, le README produit prévaut.
