# Recette manuelle — Cockpit GLC — Période libre

## Statut

**GO avec réserves** sur Palier 4 période libre (`19.0.4.2.5`) — R1–R10 OK.  
**GO MOA UX-GROUPBY** sur `19.0.4.4.2` — R11 (composant OWL `glc_coverage_detail`) — 2026-05-27.  
Tests automatisés **65/65 OK** sur `dorevia_glc_analytics` + `dorevia_glc_budget`.

*(Passages précédents : GO avec réserves — navigation sans erreur ; correctifs `19.0.4.2.1` → `19.0.4.2.5` ; itérations UX-GROUPBY `19.0.4.3.0` → `19.0.4.4.2`.)*

## Module

| Élément | Valeur |
|---|---|
| Module cockpit | `dorevia_glc_analytics` |
| Module budget (prérequis) | `dorevia_glc_budget` |
| Version attendue | `19.0.4.4.2` |
| Palier | 4 — Cockpit GLC |
| Évolution | période libre `date_from` / `date_to` + regroupement mensuel automatique |

**Références :** [TICKET_PALIER_4BIS.md](../TICKET_PALIER_4BIS.md) · [RECETTE_MANUELLE_PALIER_4.md](../RECETTE_MANUELLE_PALIER_4.md) · [CADRAGE_FINAL_PALIER_4.md](../CADRAGE_FINAL_PALIER_4.md)

## Objectif

Vérifier que le cockpit GLC permet désormais une lecture sur période libre, avec :

- choix d'une date de début ;
- choix d'une date de fin ;
- scénario budgétaire conservé ;
- titre dynamique ;
- période analysée calculée ;
- regroupement automatique par mois si la période couvre plusieurs mois ;
- exclusion correcte des écritures hors période.

---

## Pré-requis

- Instance de recette redémarrée.
- **Restart obligatoire du worker Odoo** après upgrade (`docker compose restart odoo`) — un `-u dorevia_glc_analytics` met à jour la DB mais **ne recharge pas le code Python en mémoire** du processus serveur.
- Navigateur rafraîchi avec **hard refresh** (`Ctrl+Shift+R` / `Cmd+Shift+R`) — **requis MOA** après upgrade pour charger le JS `glc_coverage_cockpit_form_view.esm.js` (refactor `webSave`).
- Modules installés ou mis à jour en version `19.0.4.4.2` :

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d glc-rgl-test-import -u dorevia_glc_analytics \
  --stop-after-init --no-http

docker compose restart odoo
```

- Accès au menu :

`Comptabilité → Pilotage GLC → Cockpit couverture des charges de structure`

*(libellé technique ; équivalent MOA « Cockpit GLC »)*

- Contexte recette :

```text
URL  : http://localhost:18079
Base : glc-rgl-test-import
```

### Règles V1 arbitrées (rappel)

| Flux | Règle recette |
|---|---|
| **Réalisé analytique** | Dates exactes dans chaque tranche mensuelle |
| **Masse salariale** | Mois touché = ventilation mensuelle complète incluse |
| **Budget** | Mois budgétaire complet dès que le mois est touché (pas de prorata V1) |

### Historique recette

| Passage | Verdict | Détail |
|---|---|---|
| 1er passage | NO GO | R4 KO — budget mars exclu sur période partielle (`7000` attendu, `4000` obtenu) |
| Correctif Dev | — | `_budget_lines()` : suppression filtre `period_date >= date_from` exact |
| Rejeu R4 | OK | Budget `7000.0` confirmé |
| Rejeu global R1–R9 | GO avec réserves | Tous scénarios OK |
| Anomalie R10 (lignes non recalculées au changement de période) | **NO GO temporaire** | Titre/période OK, `line_ids` stale côté UI |
| Correctif Dev R10 | — | `refresh_key` + reload JS après save filtres |
| Rejeu MOA R10 | **OK technique** | 3 cas validés après upgrade `19.0.4.2.1` |
| Hard refresh navigateur MOA | **À confirmer** | Non exécutable depuis navigateur intégré Codex (accès `localhost:18079` bloqué par politique réseau locale) |
| Erreur validation `cockpit_id` au changement de période | **Corrigé Dev** | `19.0.4.2.3` — save JS filtres-only + ignore `line_ids` dans `web_save` + créations client ignorées |
| Rejeu MOA R10 post-`19.0.4.2.2` | **OK technique (cas 2)** | Plus d'erreur `cockpit_id` ; `line_ids` client ignorées ; janvier seul affiché |
| Détail par activité non rafraîchi navigateur après save filtres | **Corrigé Dev** | `19.0.4.2.4` — JS save bascule sur `webSave` + `_setData(result[0])` pour data fraîches (titre + période + `line_ids`) |
| Worker Odoo gardait l'ancien code Python après `-u` | **Corrigé Dev** | Procédure recette mise à jour : `docker compose restart odoo` obligatoire avant rejeu |
| Rejeu MOA complet R1–R10 post-`19.0.4.2.4` | **OK technique** | R1–R10 validés côté serveur / RPC |
| Correctif UX autosave filtres date | **Corrigé Dev** | `19.0.4.2.5` — save auto au changement filtre + flux natif Odoo |
| Navigation MOA navigateur post-`19.0.4.2.5` | **OK MOA** *(passage précédent)* | Aucune erreur en navigation manuelle |
| **Rejeu MOA complet R1–R10 post-`19.0.4.2.5`** | **OK** | R1–R10 validés ; R10 cas 1, 2, 3 OK |

---

## R1 — Ouverture par défaut

### Action

Ouvrir le cockpit GLC sans modifier les filtres.

### Résultat attendu

- Le cockpit s'ouvre sur le mois courant complet.
- Les champs visibles sont :
  - Date de début ;
  - Date de fin ;
  - Scénario budgétaire ;
  - Période analysée.
- Les anciens champs Année / Mois ne sont plus utilisés comme filtres principaux.
- La période analysée est calculée automatiquement.

### Verdict

- [x] OK
- [ ] KO

**Observations :** ouverture par défaut OK sur mai 2026 ; titre `Cockpit GLC · 2026 · Mai · Initial`, période `1 mai → 31 mai`, lignes calculées.

---

## R2 — Période mono-mois complète

### Action

Saisir :

- Date de début : `01/04/2026`
- Date de fin : `30/04/2026`
- Scénario : `Initial`

### Résultat attendu

Le titre doit être du type :

`Cockpit GLC · 2026 · Avril · Initial`

La période analysée doit indiquer :

`1 avr. → 30 avr.`

Dans l'onglet **Détail par activité** :

- les lignes restent lisibles par activité ;
- le comportement est équivalent à l'ancien affichage mensuel ;
- les totaux sont cohérents pour avril uniquement.

### Verdict

- [x] OK
- [ ] KO

**Observations :** avril complet OK ; titre `Cockpit GLC · 2026 · Avril · Initial`, période `1 avr. → 30 avr.`, lignes mono-mois Avril.

---

## R3 — Période multi-mois complète

### Action

Saisir :

- Date de début : `01/01/2026`
- Date de fin : `30/04/2026`
- Scénario : `Initial`

### Résultat attendu

Le titre doit être du type :

`Cockpit GLC · 2026 · 1 janv. → 30 avr. · Initial`

Dans l'onglet **Détail par activité** :

- les lignes sont regroupées par mois ;
- les mois attendus sont visibles :
  - Janvier 2026 ;
  - Février 2026 ;
  - Mars 2026 ;
  - Avril 2026 ;
- chaque mois dispose d'un total mensuel ;
- une ligne **Total période** est présente en fin de tableau ;
- les totaux période correspondent à la somme des mois affichés.

### Critère MOA

L'utilisateur doit comprendre immédiatement quel mois il est en train de lire.

### Verdict

- [x] OK
- [ ] KO

**Observations :** janvier à avril OK ; regroupement Janvier, Février, Mars, Avril avec totaux mensuels et Total période.

---

## R4 — Période partielle

### Action

Saisir :

- Date de début : `15/03/2026`
- Date de fin : `30/04/2026`
- Scénario : `Initial`

**Préparation données (si besoin) :**

- Au moins une recette **BAR** en mars **avant** le 15/03 (ex. 10/03) et une **après** le 15/03 (ex. 20/03).
- Au moins une recette **BAR** en avril.

### Résultat attendu

Dans le réalisé analytique :

- les écritures avant le `15/03/2026` sont exclues ;
- mars est calculé uniquement du `15/03/2026` au `31/03/2026` ;
- avril est calculé du `01/04/2026` au `30/04/2026`.

Le regroupement mensuel doit rester lisible :

- Mars 2026 ;
- Avril 2026 ;
- Total période.

### Point d'attention

La masse salariale et le budget suivent les règles V1 arbitrées :

- masse salariale : mois touché = ventilation mensuelle complète incluse ;
- budget : mois budgétaire complet dès que le mois est touché ;
- pas de prorata budgétaire en V1.

### Verdict

- [x] OK
- [ ] KO

**Observations :** période partielle `15 mars → 30 avr.` OK ; Mars et Avril visibles, Total période présent, réel borné aux dates et budget lu en mois touchés.

<details>
<summary>Historique rejeu précédent (R4)</summary>

| Contrôle | Résultat |
|---|---|
| Réalisé BAR (dates exactes) | `4000.0` — écriture du 10/03 exclue, celle du 20/03 inclue |
| Masse salariale | `2000.0` — mars + avril inclus en entier |
| Budget recettes | `7000.0` — mars (`3000`) + avril (`4000`) en mois complets |
| Budget salaires | `1500.0` |
| Frais généraux réalisés | `700.0` |
| Détail mensuel | Mars · Avril · **Total période** |

Scénario R4 pur : ne pas mélanger une ligne budget `STRUCTURE` en `expense` avec le contrôle budget recettes (voir réserve MOA).

</details>

---

## R5 — Période invalide

### Action

Saisir :

- Date de début : `30/04/2026`
- Date de fin : `01/04/2026`

### Résultat attendu

- L'action est refusée.
- Un message d'erreur utilisateur clair est affiché *(attendu : « La date de début doit être antérieure ou égale à la date de fin. »)*.
- Aucun cockpit incohérent n'est calculé.
- Aucun tableau faux n'est présenté.

### Verdict

- [x] OK
- [ ] KO

**Observations :** UserError bloquant OK avec le message attendu : « La date de début doit être antérieure ou égale à la date de fin. »

---

## R6 — Onglet Ressources

### Action

Tester une période multi-mois :

- Date de début : `01/01/2026`
- Date de fin : `30/04/2026`
- Scénario : `Initial`

Puis ouvrir l'onglet **Ressources**.

### Résultat attendu

- Les ressources sont agrégées sur toute la période `date_from → date_to`.
- Les montants ne se limitent pas à une seule année/mois.
- L'affichage reste cohérent avec la période analysée.

### Verdict

- [x] OK
- [ ] KO

**Observations :** onglet Ressources cohérent sur période multi-mois ; réalisé et prévu agrégés sur la période affichée.

---

## R7 — Onglet Charges de structure

### Action

Tester une période multi-mois :

- Date de début : `01/01/2026`
- Date de fin : `30/04/2026`
- Scénario : `Initial`

Puis ouvrir l'onglet **Charges de structure**.

### Résultat attendu

- Les charges de structure sont agrégées sur toute la période `date_from → date_to`.
- Les montants correspondent à la période affichée.
- L'affichage reste cohérent avec le bandeau d'alerte.

### Verdict

- [x] OK
- [ ] KO

**Observations :** charges de structure cohérentes ; masse salariale, frais généraux et soldes alignés sur la période.

---

## R8 — Bandeau d'alerte et état vide

### Action

Comparer le bandeau d'alerte avec le contenu du tableau sur une période mono-mois puis multi-mois.

Tester aussi une période sans ligne activité (ex. financement seul, sans détail activité).

### Résultat attendu

- Le bandeau d'alerte est basé sur les lignes activité uniquement.
- Les lignes de total mensuel et total période ne créent pas de faux signal.
- En absence de données activité, l'état vide explicite s'affiche et le bandeau est masqué.

### Verdict

- [x] OK
- [ ] KO

**Observations :** état vide OK ; aucune ligne détaillée, bandeau d'alerte masqué par `detail_line_count = 0`.

---

## R9 — Colonnes

### Action

Contrôler l'onglet **Détail par activité**.

### Résultat attendu

Les colonnes suivantes sont présentes dans le tableau détail :

| Colonne MOA | Colonne technique | Statut V1 |
|---|---|---|
| Mois | Mois | Visible |
| Activité | Activité | Visible |
| Recettes réel | Recettes réel | Visible |
| Recettes budgétées | Recettes budget | Visible |
| Écart recettes | Écart recettes | Visible |
| Masse salariale réelle | Masse sal. réel | Visible |
| Masse salariale budgétée | Masse sal. budget | Visible |
| Écart masse salariale | Écart masse sal. | Visible |
| Frais généraux réels | Frais gén. réel | Optional (affichable) |
| Frais généraux budgétés | Frais gén. budget | Optional (affichable) |
| Écart frais généraux | Écart frais gén. | Optional (affichable) |
| Solde réel | — | **Hors tableau détail V1** *(soldes dans onglet Charges de structure)* |
| Solde budgété | — | **Hors tableau détail V1** |
| Écart solde | — | **Hors tableau détail V1** |

Les frais généraux restent en **optional** : les afficher via le menu colonnes du tableau si besoin.

### Verdict

- [x] OK
- [ ] KO

**Observations :** colonnes conformes ; les trois colonnes frais généraux restent optional/affichables avec sommes.

---

## R10 — Recalcul automatique des lignes au changement de filtre

### Cas 1 — Multi-mois vers période plus courte

1. Saisir `01/01/2026 → 30/04/2026`
2. Vérifier janvier à avril (+ totaux mensuels + total période)
3. Modifier `date_to` en `31/03/2026`

**Attendu :**

- avril disparaît ;
- janvier, février, mars restent visibles ;
- total période recalculé ;
- onglets **Ressources** / **Charges de structure** / bandeau alignés.

### Cas 2 — Multi-mois vers mono-mois

1. Saisir `01/01/2026 → 30/04/2026`
2. Modifier en `date_to = 31/01/2026`

**Attendu :**

- seul janvier reste visible ;
- titre mensuel janvier ;
- aucune ligne avril ne reste affichée.

### Cas 3 — Mono-mois vers autre mono-mois

1. Saisir `01/04/2026 → 30/04/2026`
2. Modifier en `01/01/2026 → 31/01/2026`

**Attendu :**

- avril disparaît ;
- janvier apparaît ;
- montants recalculés.

### Critère GO R10

Le tableau doit toujours correspondre exactement à la période affichée dans le titre et dans **Période analysée**.

### Verdict

- [x] OK
- [ ] KO

**Rejeu MOA `19.0.4.2.5` — cocher cas par cas :**

| Cas | Action | OK | KO | Observations |
|---|---|:---:|:---:|---|
| Cas 1 | Multi-mois → période plus courte | [x] | [ ] | Avril disparaît ; Janvier, Février, Mars restent ; titre/période/lignes alignés. |
| Cas 2 | Multi-mois → mono-mois (janvier) | [x] | [ ] | Seul Janvier reste visible ; aucune ligne Avril ; pas d'erreur `cockpit_id`. |
| Cas 3 | Mono-mois → autre mono-mois | [x] | [ ] | Avril disparaît, Janvier apparaît ; montants recalculés. |

**Points de contrôle :** pas d'erreur `cockpit_id` ; titre + période + lignes recalculés **sans F5**.

<details>
<summary>Historique rejeux techniques précédents</summary>

| Version | Cas | Résultat |
|---|---|---|
| `19.0.4.2.1` | Cas 1, 2, 3 | OK — regroupement et recalcul lignes |
| `19.0.4.2.2` | Cas 2 ciblé | OK — plus d'erreur validation |
| `19.0.4.2.3` | Cas 2 MOA | KO — détail vide après save filtres |
| `19.0.4.2.4` | Rejeu R1–R10 | OK technique |
| `19.0.4.2.5` | Autosave filtres date | OK MOA *(navigation sans erreur)* |

</details>

---

## R11 — UX-GROUPBY (composant OWL `glc_coverage_detail`)

### Contexte

Évolution UX MOA livrée en `19.0.4.4.2` après arbitrage Option C — composant OWL custom dans l'onglet **Détail par activité**.

**Référence ticket :** [TICKET_UX_GROUP_BY_DETAIL_COCKPIT.md](../TICKET_UX_GROUP_BY_DETAIL_COCKPIT.md) (section 11 — Verdict final).

### Pré-requis spécifiques

- Upgrade en `19.0.4.4.2` puis **restart Odoo** + **hard refresh** navigateur (`Cmd+Shift+R`) pour recharger les assets backend (JS, XML, SCSS du widget).

### Procédure R11

1. Ouvrir le cockpit GLC sur une période **multi-mois** (ex. `1 janv. → 31 mai`).
2. Onglet **Détail par activité** — vérifier le rendu point par point :

| Référence | Point de contrôle | OK | Observations |
|---|---|:---:|---|
| R11-UX-G1 | Blocs mensuels chronologiques visibles (Janvier 2026 → Février → Mars …) | [x] | Bandeau sobre, fond gris léger, majuscules petites |
| R11-UX-G2 | Sous-total mensuel sous chaque bloc, libellé `Sous-total <Mois Année>` | [x] | Gras, italique, bordure haute fine, fond très léger |
| R11-UX-G3 | Ligne **TOTAL PÉRIODE** en bas, séparée du dernier mois par **double bordure** | [x] | `<tfoot>` séparé, double bordure noire `3px double` |
| R11-UX-G4 | Filtres `date_from` / `date_to` / scénario rafraîchissent le widget sans F5 | [x] | OWL réactif, R10 conservé |
| R11-UX-G5 | Aucune ligne artificielle en base (`month_total` / `period_total`) | [x] | Backend ne produit que des lignes `activity` — UX-G5 par construction |
| R11-FAM | Header à 2 niveaux : familles Recettes / Masse salariale / Frais généraux + Réel / Budget / Écart | [x] | Séparation verticale fine entre familles |
| R11-ZERO | Zéros affichés en `—` atténué gris clair | [x] | Réduit le bruit visuel des colonnes peu renseignées ; zéro **non coloré** (pas rouge/vert) |
| R11-VAR | Écarts négatifs en rouge sobre `#b02a2a`, positifs en vert sobre `#198754` | [x] | Sur sous-totaux mensuels, écarts en gras supplémentaire |
| R11-PARC | Lecture détaillée entièrement contenue dans l'onglet ; **aucun bouton externe exposé** | [x] | L'action serveur `action_open_detail_grouped` reste disponible côté code mais hors parcours MOA |
| R11-MONO | En période **mono-mois**, aucun sous-total ni total période n'est affiché | [x] | Le widget ne rend les sous-totaux que si `multiMonth = true` |

### Points documentés MOA

- les zéros sont remplacés par `—` **uniquement en affichage cockpit** (pas en base, pas en RPC, pas en export) ;
- les **écarts nuls ne prennent pas de couleur** rouge/verte (cohérence visuelle avec les autres zéros) ;
- la ligne **TOTAL PÉRIODE** est distinguée par une **double bordure noire** (`3px double var(--bs-emphasis-color)`) ;
- le **lien externe** vers la vue liste groupée Odoo native **n'est plus exposé** à l'utilisateur ;
- l'**action technique** `action_open_detail_grouped` et la vue list groupée Odoo native (`view_glc_coverage_cockpit_line_list_grouped`) **restent disponibles côté code** — utiles pour réactivation future ou debug, mais hors parcours MOA.

### Verdict R11

- [x] **GO UX-GROUPBY** sur `19.0.4.4.2` (2026-05-27)
- [ ] KO

**Observations :** rendu validé MOA — hiérarchie visuelle claire, blocs mensuels comme titres de section, sous-totaux clairement identifiables, total période séparé, écarts colorés sobrement, zéros atténués, lien externe supprimé. La voie CSS/XML/OWL custom est confirmée comme arbitrage final.

---

## R12 — Bloc PERFORMANCE + séparation familles (`19.0.4.5.1`)

> **Note de wording — `19.0.4.6.1` :** le bloc historiquement nommé **PERFORMANCE** est désormais libellé **« Marge d'activité »** dans l'UI (en-tête famille, KPI, titres de graphiques). Les noms techniques (`performance_realized`, `performance_budget`, `variance_performance`, `o_glc_family_performance`, `computePerformanceAmounts`) sont **conservés**. Formule inchangée : Marge d'activité = Recettes − Salaires − Dépenses hors salaires.

### Contexte

Complément MOA post-validation UX `19.0.4.4.2` :

1. ajout d'un quatrième bloc **PERFORMANCE** dans le widget `glc_coverage_detail` (`19.0.4.5.0`) ;
2. finition UX de séparation visuelle entre les 4 familles métier (`19.0.4.5.1`).

**Référence ticket :** [TICKET_UX_GROUP_BY_DETAIL_COCKPIT.md](../TICKET_UX_GROUP_BY_DETAIL_COCKPIT.md) (sections 12 et 13).

### Pré-requis

- Upgrade en **`19.0.4.5.1`** + restart Odoo + hard refresh navigateur.

### Procédure R12

1. Cockpit multi-mois (ex. `1 janv. → 31 mai`).
2. Onglet **Détail par activité** :

| Référence | Point de contrôle | OK | Observations |
|---|---|:---:|---|
| R12-LBL | Libellés familles : **Recettes**, **Salaires**, **Dépenses**, **Performance** | [x] | Dépenses = hors salaires (doctrine MOA pilotage) |
| R12-COL | Bloc Performance : colonnes Réel / Budget / Écart | [x] | 4e famille dans le header à 2 niveaux |
| R12-FORM | Formule activité : Perf. réelle = Recettes − Salaires − Dépenses (réel) | [x] | Vérifier une ligne `[BAR]` avec recettes et masse sal. |
| R12-SUB | Sous-total mensuel inclut Performance (Réel / Budget / Écart) | [x] | Cohérent avec somme des lignes activité du mois |
| R12-TOT | **TOTAL PÉRIODE** inclut Performance | [x] | Double bordure conservée |
| R12-ZERO | Performance nulle affichée `—`, sans couleur | [x] | |
| R12-COLOR | Performance positive verte, négative rouge (Réel et Écart) | [x] | Vert `#198754`, rouge `#b02a2a` |
| R12-PARC | Aucun lien/fallback externe réintroduit | [x] | |
| R12-SEP | Séparateurs verticaux après Écart (Recettes, Salaires, Dépenses) | [x] | Lecture en 4 blocs, pas une suite de 12 colonnes |
| R12-HDR | Headers familles renforcés (fond gris `#f3f4f6`, gras) | [x] | Pas de surlignage bleu CSS — sélection navigateur si visible sur capture |
| R12-PERF-UX | Bloc Performance légèrement détaché (bordure gauche + fond `#f8f9fa`) | [x] | Synthèse décisionnelle plus marquée, sobre |

### Verdict R12

- [x] **GO UX / GO fonctionnel** (2026-05-27)
- [ ] KO

**Observations :** vue **Détail par activité** validée comme **cible UX pour ce palier** — blocs RECETTES | SALAIRES | DÉPENSES | PERFORMANCE clairement distingués (dépenses = hors salaires), performance sur activités/sous-totaux/total période, zéros `—`, couleurs cohérentes, mois/sous-totaux/total période lisibles, aucun lien externe exposé.

---

## Tests automatisés (non-régression)

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d glc-rgl-test-import -u dorevia_glc_analytics,dorevia_glc_budget \
  --test-enable --test-tags post_install \
  --stop-after-init --no-http
```

| Résultat attendu | Résultat recette `19.0.4.7.0` |
|---|---|
| Tests `dorevia_glc_analytics` | **70 tests** |
| Tests `dorevia_glc_budget` | **14 tests** |
| **Total** | **74 post-tests**, **0 failed**, **0 error(s)** |

Tests source réalisé R14 :
- `test_payroll_from_analytic_lines_not_allocations` — Palier 2 ≠ source cockpit
- `test_realized_payroll_from_bank_recon_645_analytic` — 645200 + STRUCTURE → SALAIRES
- `test_no_double_count_payroll_allocation_and_analytic` — anti-doublon
- `test_excluded_treasury_512_not_in_cockpit` / `test_excluded_partner_411_401_not_in_cockpit`

Tests UX-GROUPBY / PERFORMANCE :
- `test_multi_month_detail_activity_only` — UX-G5 par construction
- `test_single_month_has_no_artificial_totals` — pas d'artefact mono-mois
- `test_detail_activity_sums_match_cockpit_aggregates` — cohérence agrégats cockpit
- `test_action_open_detail_grouped` — action serveur technique
- `test_activity_line_performance_formula` — formules performance ligne activité
- `test_multi_month_performance_sums_from_activity_lines` — agrégation mensuelle performance

---

## Synthèse de recette

| Référence | Contrôle | Verdict | Commentaire |
|---|---|:---:|---|
| R1 | Ouverture par défaut | OK | Mai 2026 complet, titre et lignes calculées |
| R2 | Période mono-mois complète | OK | Avril complet |
| R3 | Période multi-mois complète | OK | Janvier à avril + totaux |
| R4 | Période partielle | OK | Mars partiel à avril |
| R5 | Période invalide | OK | UserError bloquant |
| R6 | Onglet Ressources | OK | Agrégation période cohérente |
| R7 | Onglet Charges de structure | OK | Masse salariale, frais généraux, soldes |
| R8 | Bandeau / état vide | OK | Bandeau masqué sans détail |
| R9 | Colonnes | OK | Colonnes et optional conformes |
| R10 | Recalcul lignes au changement filtre | OK | Cas 1, 2, 3 validés (`19.0.4.2.5`) |
| **R11** | **UX-GROUPBY (composant OWL `glc_coverage_detail`)** | **GO** | Blocs mensuels, sous-totaux, total période, zéros `—` (`19.0.4.4.2`) |
| **R12** | **PERFORMANCE + séparation familles (cible UX validée)** | **GO** | `19.0.4.5.1` — blocs distincts, formules performance, finition visuelle familles |
| **R13** | **Synthèse graphique — Marge d'activité (4 KPI + 3 graphes Chart.js)** | **GO** | `19.0.4.6.1` — onglet 1 cockpit GLC, wording MOA Marge |
| **R14** | **Source de vérité réalisé cockpit (compta analytique + Palier 2 contrôle R2)** | **GO (auto)** | `19.0.4.7.0` — refonte `_sum_payroll_realized` |

---

## R13 — Onglet Synthèse graphique — Marge d'activité (`19.0.4.6.1`)

### Contexte

Création du **premier onglet** du cockpit GLC : lecture immédiate de pilotage en complément du Détail par activité (cible UX validée).

**Doctrine wording MOA (`19.0.4.6.1`) :** le bloc historiquement nommé **PERFORMANCE** est désormais libellé **« Marge d'activité »** (ou **« Marge »** selon la place). **SALAIRES** est conservé. Formule inchangée :

> Marge d'activité = Recettes − Salaires − Dépenses hors salaires

**Référence ticket :** [TICKET_COCKPIT_SYNTHESE_GRAPHIQUE.md](../TICKET_COCKPIT_SYNTHESE_GRAPHIQUE.md).

### Pré-requis

- Upgrade en **`19.0.4.6.1`** + restart Odoo + hard refresh navigateur.
- Cockpit multi-mois (ex. `1 janv. → 31 mai`) avec au moins une activité ayant recettes, salaires et dépenses sur la période.

### Procédure R13

| Référence | Point de contrôle | OK | Observations |
|---|---|:---:|---|
| R13-ORDER | Ordre des onglets : Synthèse graphique · Détail par activité · Ressources · Charges de structure · Infos | [x] | Synthèse en premier |
| R13-WORDING | Wording **Marge d'activité** (et non « Performance ») dans KPI, titres graphes et intro onglet | [x] | Doctrine `19.0.4.6.1` : SALAIRES conservé, PERFORMANCE → MARGE D'ACTIVITÉ |
| R13-FORMULE | Précision visible : « Marge d'activité = Recettes − Salaires − Dépenses hors salaires » | [x] | Sous le titre de l'onglet Synthèse |
| R13-KPI-MR | KPI **Marge réelle** signée (vert si > 0, rouge si < 0, neutre si 0) | [x] | Format `+ x €` / `- x €` / `—` |
| R13-KPI-MB | KPI **Marge budget** affichée neutre | [x] | |
| R13-KPI-VM | KPI **Écart de marge** signé, vert/rouge selon signe | [x] | |
| R13-KPI-COV | KPI Couverture salaires : seuils vert ≥ 100 %, orange 80–100 %, rouge < 80 % | [x] | Formule `Recettes réelles / Salaires réels × 100` ; `—` si salaires = 0 |
| R13-GR1 | Graphique **Marge d'activité mensuelle** (barres réel vs budget) | [x] | Vert réel, gris budget |
| R13-GR2 | Graphique Structure mensuelle (barres Recettes / Salaires / Dépenses) | [x] | **Salaires et dépenses en valeurs positives de consommation** |
| R13-GR3 | Graphique **Marge d'activité par activité** (barres horizontales) | [x] | Tri décroissant ; vert si positive, rouge si négative |
| R13-LAYOUT | Grille graphiques : 2 par ligne (responsive 1 colonne sous 992 px) | [x] | `19.0.4.6.0` |
| R13-REFRESH | Modification des filtres → graphes mis à jour | [x] | Auto-save + re-render Chart.js |
| R13-EMPTY | Période sans données → message bandeau, pas de canvas vide | [x] | |
| R13-COHESION | Palette cohérente avec le widget Détail (verts/rouges sobres, fond `#f8f9fa` Marge) | [x] | |
| R13-PARC | Aucun lien externe / drill-down réintroduit | [x] | Onglet en lecture pure |

### Verdict R13

- [x] **GO** (2026-05-27)
- [ ] KO

**Observations :** onglet **Synthèse graphique** validé MOA comme **onglet 1 de pilotage**. 4 KPI + 3 graphes Chart.js conformes ; grammaire **RECETTES | SALAIRES | DÉPENSES | MARGE D'ACTIVITÉ** appliquée de manière cohérente dans toute la doc et le code UI ; formule visible sous le titre ; couverture des salaires sur les seuils MOA validés ; pas de lien externe / drill-down.

---

## Verdict final MOA

- [x] **GO** — R1–R12 OK sur `19.0.4.5.1`
- [x] **GO** — R1–R13 OK sur `19.0.4.6.1` — **onglet 1 Synthèse graphique validé MOA**

---

## R14 — Source de vérité du réalisé cockpit (`19.0.4.7.0`)

**Objectif :** valider que le réalisé cockpit agrège les écritures charge/produit + analytique (toutes origines), avec Palier 2 en **contrôle R2** uniquement.

**Référence :** [TICKET_COCKPIT_SOURCE_REALISE.md](../TICKET_COCKPIT_SOURCE_REALISE.md) · cadrage I2/I3 révisés.

| Réf | Cas | Famille attendue | Auto |
|---|---|---|:---:|
| R14-FAC-CLI | Facture client 7xxx + analytique [BAR] | RECETTES | ✅ |
| R14-FAC-FOU | Facture fournisseur 6xxx hors payroll + [STRUCTURE] | DÉPENSES | ✅ |
| R14-BNK-6XX | Rapprochement / OD 6xxx hors payroll + analytique | DÉPENSES | ✅ |
| R14-BNK-645 | Rapprochement 645200 + [STRUCTURE] | **SALAIRES** | ✅ |
| R14-NODOUBLON | Compta analytique payroll + ventilation Palier 2 même mois | Pas de double comptage | ✅ |
| R14-EXCL-512 | Ligne trésorerie 512 + analytique | **Exclue** | ✅ |
| R14-EXCL-411 | Ligne tiers 411 + analytique | **Exclue** | ✅ |

**Recette manuelle MOA (complément) :**

| Réf | Cas | Statut MOA |
|---|---|:---:|
| R14-CAISSE | Opération caisse charge/produit + analytique | [ ] |
| R14-OD | Écriture comptable directe + analytique | [ ] |
| R14-645-REEL | Cas révélateur 645200 + [STRUCTURE] rapprochement bancaire sur `glc-rgl-test-import` | [ ] |

**Verdict R14 automatisé :** **GO** — 7 tests Python verts sur `19.0.4.7.0`.

---

## Verdict recette (mise à jour)
- [ ] GO avec réserves
- [ ] NO GO

*(Le verdict « GO avec réserves » du Palier 4 période libre est levé : les réserves non bloquantes restent documentées ; l'UX-GROUPBY, le complément Marge d'activité et la Synthèse graphique sont validés en complément. Le cockpit GLC dispose désormais d'une **double lecture** : Synthèse graphique pour le pilotage immédiat, Détail par activité pour la justification chiffrée.)*

## Réserves éventuelles

| Réserve | Bloquante | Commentaire |
|---|---:|---|
| Mapping budget **`STRUCTURE`** vs **`payroll_budget`** | Non | Ambiguïté KPI budget masse salariale vs frais généraux — hors périmètre recette période libre. |
| **Rechargement code Python après upgrade** | Non *(procédure connue)* | `docker compose restart odoo` obligatoire après `-u`. |
| **Hard refresh navigateur après upgrade JS** | Non *(procédure connue)* | `Cmd+Shift+R` requis pour recharger le widget `glc_coverage_detail` (JS + XML + SCSS). |
| **Groupes pliables / dépliables dans l'onglet** | Non *(limite Odoo)* | `group_by` natif non supporté dans une `<list>` x2many inline — compromis MOA acté ; lecture entièrement à plat dans l'onglet. |

---

## Exécution recette

| Champ | Valeur |
|---|---|
| Date (passage initial R1–R9) | 2026-05-27 |
| Date (rejeu R10 `19.0.4.2.1`) | 2026-05-27 |
| Date (rejeu ciblé R10 cas 2 `19.0.4.2.2`) | 2026-05-27 |
| Date (rejeu complet `19.0.4.2.4`) | 2026-05-27 |
| Date (rejeu complet `19.0.4.2.5`) | 2026-05-27 |
| Date (R11 UX-GROUPBY `19.0.4.4.2`) | 2026-05-27 |
| Date (R12 PERFORMANCE + familles `19.0.4.5.1`) | 2026-05-27 |
| Date (R13 Synthèse graphique — Marge d'activité `19.0.4.6.1`) | 2026-05-27 |
| Exécutant | MOA |
| Base / environnement | `glc-rgl-test-import` · `http://localhost:18079` |
| Version module | `dorevia_glc_analytics` **`19.0.4.6.1`** (Synthèse graphique + wording Marge d'activité) |
| Verdict global | **GO** — R1–R13 OK — **double lecture cockpit validée** (Synthèse graphique + Détail par activité) |
| Merge | **À soumettre** — branche `feat/glc-cockpit-synthese-graphique` |

---

## Décision attendue

Cette recette valide :

1. que le cockpit GLC n'est plus limité à une lecture mensuelle fixe, mais devient un outil de pilotage sur **période libre** (R1–R10 sur `19.0.4.2.5`) ;
2. que l'onglet **Détail par activité** propose une **lecture structurée par mois** avec sous-totaux mensuels et total période visibles, **entièrement contenue dans le cockpit** (R11 sur `19.0.4.4.2`) ;
3. que le bloc **Marge d'activité** et la **séparation visuelle des 4 familles** métier répondent aux attentes MOA (R12 sur `19.0.4.5.1`) — **cible UX validée** pour la vue Détail ;
4. que l'onglet **Synthèse graphique** offre une **lecture immédiate de pilotage** (4 KPI + 3 graphes Marge / Structure / Par activité) avec la grammaire métier **Recettes | Salaires | Dépenses | Marge d'activité** (R13 sur `19.0.4.6.1`) — **onglet 1 cockpit GLC validé MOA**.

**Critères de GO :**

> Le cockpit doit permettre une lecture fiable du réel, du budget et des écarts sur une période choisie par l'utilisateur, avec regroupement mensuel automatique lorsque la période couvre plusieurs mois.  
> Le détail par activité doit afficher une hiérarchie visuelle claire mois → activités → sous-total mensuel → total période, avec 4 blocs RECETTES | SALAIRES | DÉPENSES | MARGE D'ACTIVITÉ clairement distingués, sans sortie de l'onglet.  
> La synthèse graphique doit offrir une lecture instantanée du pilotage (marge d'activité, structure mensuelle, marge par activité) en complément du détail chiffré.

**Statut :** **GO** sur `19.0.4.7.0` — R1–R14 (auto) OK, **74 post-tests verts**, recette manuelle R14-CAISSE/OD/645-REEL en attente MOA.

**Évolution UX référence :** [TICKET_UX_GROUP_BY_DETAIL_COCKPIT.md](../TICKET_UX_GROUP_BY_DETAIL_COCKPIT.md) — sections 11–13 (UX-GROUPBY, Marge d'activité, séparation familles) · [TICKET_COCKPIT_SYNTHESE_GRAPHIQUE.md](../TICKET_COCKPIT_SYNTHESE_GRAPHIQUE.md) — onglet 1 Synthèse graphique.
