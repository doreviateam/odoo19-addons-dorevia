# Audit GLC Analytics / Budget — avant Palier 4


> **Document historique** — ne décrit plus le produit installé depuis **`19.0.13.0.0`** / **`19.0.14.0.0`**. État actuel : [ETAT_MODULE_ACTUEL.md](./ETAT_MODULE_ACTUEL.md).

---

**Date :** 2026-05-27  
**Base de recette :** `glc-rgl-test-import`  
**Base technique de vérification :** `glc-audit-paliers-0-3`  
**Modules audités :** `dorevia_glc_analytics`, `dorevia_glc_budget`

## 1. Verdict synthétique

**GO avec réserves légères avant ouverture du Palier 4.**

Les Paliers 0 à 3 sont fonctionnellement cohérents, séparés proprement et testés. Le socle donne une lecture exploitable du réalisé analytique, des coûts salariés ventilés et du prévisionnel budgétaire. Le futur cockpit peut agréger les données, mais la règle RH / Personnel doit être figée avant développement : le cockpit ne doit pas mélanger implicitement écritures analytiques RH historiques et ventilations salariales Palier 2.

Réserves à traiter ou documenter avant Palier 4 :

- Figer la règle d'agrégation RH / Personnel.
- Corriger deux points de robustesse mineurs dans `dorevia_glc_analytics` : import `_` manquant dans `glc_account_funding_rule.py`, et refus explicite des pourcentages/heures négatifs en ventilation salariale.
- Stabiliser les tests budget sur base de recette déjà utilisée : les années fixes 2026/2032 peuvent collisionner avec les budgets créés par la recette manuelle.
- Clarifier les flux exclus du cockpit : emprunts, virements internes, reprises de solde, flux bilan.

## 2. Périmètre audité

| Module | Version | Paliers | Rôle |
|---|---:|---|---|
| `dorevia_glc_analytics` | `19.0.3.1.0` | 0, 1, 2 | Socle analytique, anomalies, coûts et ventilations salariales |
| `dorevia_glc_budget` | `19.0.1.0.0` | 3 | Budget prévisionnel annuel et mensuel |

Hors périmètre confirmé : cockpit, alertes Palier 4, exports, trésorerie, OCA Budget, génération automatique d'écritures comptables ou analytiques.

## 3. Audit fonctionnel

### 3.1 `dorevia_glc_analytics`

**Verdict fonctionnel : conforme Paliers 0 à 2.**

Points vérifiés :

- Plans analytiques `GLC - Activités` et `GLC - Financements` présents.
- Comptes GLC attendus présents : activités `STRUCTURE`, `BAR`, `PRESTATIONS`, `RESIDENCES`, `MISSIONS`, `PRIVATISATIONS`, `LOCATION_RADIO`; financements `ADHESIONS`, `DONS`, `SUBVENTIONS`, `RESSOURCES_PROPRES`.
- Applicabilités analytiques non bloquantes, conformes à la doctrine Palier 0.
- Assistant d'anomalies fonctionnel : A1 à A5 en lignes, A6 en synthèse STRUCTURE.
- A3 activable par mapping explicite `glc.account.funding.rule`.
- A5 dépend bien du paramètre `dorevia_glc_analytics.cutover_date`.
- *(retiré — coûts salariés)* utilisables via `glc.employee.cost.line`.
- *(retiré — ventilations)* `percent` et `hours` validables.
- Refus des comptes du plan Financements en ventilation salariale.
- Validation des ventilations sans génération d'écriture comptable.
- Validation des ventilations sans création d'écriture analytique directe dans le modèle Palier 2.
- Menus regroupés sous `Pilotage GLC`, compréhensibles pour la MOA.
- Parcours MOA reproductible par tests et recette manuelle.

Réponse à la question clé : **oui, le module donne une lecture fiable du réalisé analytique et des coûts salariés ventilés**, sous réserve que la saisie analytique réelle soit disciplinée et que le Palier 4 décide explicitement comment traiter la masse salariale.

### 3.2 `dorevia_glc_budget`

**Verdict fonctionnel : conforme Palier 3.**

Points vérifiés :

- Création d'un budget annuel par société, année et scénario.
- Scénarios disponibles : `initial`, `revised`, `landing`.
- Lignes mensuelles via `period_date`.
- Types disponibles : `revenue`, `expense`, `funding`.
- Montants négatifs refusés.
- `SUBVENTIONS` accepté en `funding`.
- `SUBVENTIONS` refusé en `expense` et, par règle commune, en `revenue`.
- Comptes Activités refusés en `funding`.
- Workflow `draft` -> `validated` -> `archived` fonctionnel.
- Budget et lignes verrouillés après validation.
- Archivage réservé aux budgets validés.
- Aucune écriture comptable générée.
- Aucune écriture analytique générée.
- Aucun début caché de cockpit dans le module.

Réponse à la question clé : **oui, le module stocke proprement le prévisionnel attendu par le Palier 4**. Le modèle `glc.budget.line` est directement exploitable par mois, axe analytique, type et montant.

## 4. Audit technique

### 4.1 Architecture modules

L'architecture est saine :

- `dorevia_glc_analytics` porte le socle, les contrôles et les ventilations salariales.
- `dorevia_glc_budget` est séparé et dépend uniquement de `dorevia_glc_analytics`.
- Pas de dépendance à OCA Budget.
- Les groupes de sécurité sont définis une fois dans `analytics` puis réutilisés par `budget`.
- Les menus `budget` se branchent proprement sur le menu racine `Pilotage GLC`.

### 4.2 Modèles

`dorevia_glc_analytics` :

- Extension de `account.analytic.account` limitée à des métadonnées GLC.
- `glc.account.funding.rule` pour le mapping A3.
- `glc.analytic.anomaly.wizard` et `glc.analytic.anomaly.line` en `TransientModel`, choix technique adapté.
- `glc.employee.cost.line`, `glc.salary.allocation`, `glc.salary.allocation.line` pour la ventilation salariale.
- Contraintes d'unicité utiles : coût mensuel par salarié/mois, ventilation par salarié/mois, activité unique par ventilation.

`dorevia_glc_budget` :

- `glc.budget` : en-tête annuel société/scénario.
- `glc.budget.line` : mois, axe analytique, type, montant.
- Contrainte unique `(company_id, year, scenario)` présente.
- Contrainte unique `(budget_id, period_date, analytic_account_id, line_type)` présente.
- Contrôle des plans Activités / Financements centralisé dans `glc.budget.mixin`.

### 4.3 Sécurité

Groupes :

- `group_glc_user` implique `analytic.group_analytic_accounting`.
- `group_glc_manager` implique `group_glc_user`.

Droits :

- Utilisateur GLC : lecture sur coûts salariés, ventilations, budgets et lignes.
- Gestionnaire GLC : CRUD sur coûts salariés, ventilations, budgets, lignes, anomalies et règles A3.

Verdict : **cohérent pour un usage GLC mono-société ou peu multi-société**. Pour un vrai multi-société strict, ajouter des `ir.rule` dédiées serait préférable.

### 4.4 Migrations

Le nom final `dorevia_glc_analytics` est utilisé dans le code actif. Les références à `dorevia_glc_analytique` restantes sont documentaires ou liées au mécanisme de migration.

Renommage :

- `hooks.py` migre `ir_module_module`, `ir_module_module_dependency`, `ir_model_data` et les clés `ir.config_parameter`.
- `migrations/19.0.3.1.0/pre-migrate.py` réutilise la même logique.
- La logique est idempotente et prévoit le cas d'un doublon de module cible.

Pas de dette cachée bloquante liée au renommage identifiée.

### 4.5 Vues / menus

Les vues sont simples et adaptées :

- Listes et formulaires lisibles.
- Statusbar sur ventilations et budgets.
- Boutons de workflow visibles selon état.
- Menus `Pilotage GLC`, `Anomalies analytiques`, `*(retiré — coûts salariés)*`, `*(retiré — ventilations)*`, `*(retiré — budgets)*`, `*(retiré — lignes budget)*`.

Réserve mineure : vérifier côté MOA les libellés des scénarios `Initial`, `Révisé`, `Atterrissage` par rapport aux termes `initial`, `revised`, `landing`.

### 4.6 Tests

Vérifications exécutées :

- Syntaxe Python : OK.
- XML vues/données/sécurité : OK.
- `dorevia_glc_budget` sur base technique fraîche `glc-audit-paliers-0-3` : **12 post-tests, 0 échec, 0 erreur**.
- `dorevia_glc_analytics` sur base technique fraîche `glc-audit-paliers-0-3` : **25 post-tests, 0 échec, 0 erreur**.

Observation importante : sur la base de recette `glc-rgl-test-import`, les tests budget peuvent échouer si un budget `2026 / initial` existe déjà à la suite de la recette manuelle. Ce n'est pas un défaut fonctionnel du module, mais une dette de test : les tests utilisent des années fixes et ne sont pas totalement isolés des données de recette persistantes.

## 5. Audit qualité code

### 5.1 Lisibilité

Le code est globalement lisible :

- Noms de modèles explicites.
- Champs métier compréhensibles.
- Workflows séparés dans des méthodes `action_*`.
- Contraintes métier proches des modèles concernés.
- Messages utilisateur en français.

### 5.2 Robustesse

Points robustes :

- Contraintes SQL sur les clés fonctionnelles.
- Validation des totaux avant validation salariale.
- Refus explicite des plans analytiques incohérents.
- Vérification de non-création d'écritures comptables dans les tests.
- Budget verrouillé après validation.

Points à renforcer :

- `glc_account_funding_rule.py` utilise `_()` sans l'importer. Le cas courant passe car les comptes de financement existent, mais le chemin d'erreur peut lever un `NameError` au lieu d'une `ValidationError` lisible.
- `glc.salary.allocation.line` ne refuse pas explicitement `percent < 0` ou `hours < 0`. Une ventilation négative compensée pourrait théoriquement atteindre 100 %.
- Le domaine multi-société de `glc.salary.allocation.line.activity_account_id` déclenche un warning Odoo car le modèle ligne n'a pas de `company_id` stocké.

### 5.3 Maintenabilité

La maintenabilité est correcte :

- Les fichiers restent courts.
- Les responsabilités sont claires.
- Les règles budget et salary ont chacune leur mixin.
- Les tests sont orientés critères d'acceptation.

Dette non bloquante : les contrôles de plans Activités / Financements existent dans deux mixins (`glc.salary.mixin`, `glc.budget.mixin`). Une factorisation commune pourrait être utile si le Palier 4 ajoute un service d'agrégation partagé.

### 5.4 Dette technique

| Priorité | Sujet | Impact | Décision |
|---|---|---|---|
| P1 | Règle RH / Personnel non figée | Risque d'agrégation cockpit fausse | À décider avant Palier 4 |
| P2 | Import `_` manquant dans règle A3 | Erreur non lisible sur cas limite | À corriger avant ou au démarrage Palier 4 |
| P2 | Valeurs négatives en ventilation salariale | Risque de saisie incohérente | À corriger avant ou au démarrage Palier 4 |
| P2 | Tests budget avec années fixes | Instabilité sur base de recette persistante | À corriger avant CI stricte |
| P3 | Domaine multi-société warning ligne salary | Bruit technique, risque faible mono-société | À corriger si multi-société |
| P3 | Libellés scénario | Clarification MOA | À valider en recette |

## 6. Préparation Palier 4

### 6.1 Données disponibles

| Donnée Palier 4 | Source attendue | Statut |
|---|---|---|
| Budget prévisionnel | `glc.budget.line` | Disponible |
| Réalisé analytique | `account.analytic.line` | Disponible via Odoo standard |
| Masse salariale réelle | `glc.salary.allocation` / `glc.salary.allocation.line` | Disponible, règle d'usage à figer |
| Recettes activité | comptes Activités `BAR`, `PRESTATIONS`, `PRIVATISATIONS`, etc. | Disponible |
| Financements | plan Financements, dont `SUBVENTIONS` | Disponible |
| Frais généraux | axe `STRUCTURE` | Disponible |
| Alertes | calcul cockpit Palier 4 | À construire |

### 6.2 Données ambiguës

Les données ambiguës avant cockpit sont :

- RH / Personnel historique présent ou non dans `account.analytic.line`.
- Écritures comptables de paie sur comptes `631`, `633`, `641`, `645`.
- *(retiré — ventilations)* Palier 2, qui sont un overlay de gestion et non des écritures analytiques.
- Flux bilan et flux non opérationnels à exclure du cockpit.

### 6.3 Point RH / Personnel

Décision recommandée :

Le cockpit doit lire la masse salariale réelle prioritairement depuis les **ventilations salariales Palier 2 validées ou verrouillées**, car elles portent la lecture de gestion par activité. Les écritures analytiques RH existantes ne doivent pas être additionnées automatiquement, sinon le cockpit risque un double comptage.

Règle proposée :

1. Pour les mois postérieurs à la bascule Palier 2 : source RH = `glc.salary.allocation.line.amount` des ventilations `validated` et `locked`.
2. Pour les mois antérieurs à la bascule : source RH = règle MOA à confirmer, soit lecture historique `account.analytic.line`, soit import de ventilations de reprise.
3. Les écritures comptables de paie restent utiles comme contrôle de cohérence, pas comme source de ventilation par activité.

### 6.4 Points à figer avant cockpit

- Date de bascule RH.
- Statuts de ventilation inclus : recommandé `validated`, `locked`.
- Traitement des mois sans ventilation.
- Exclusion des écritures analytiques RH historiques après bascule.
- Liste des comptes comptables exclus du réalisé d'exploitation.
- Mapping précis des axes cockpit : recettes activité, financements, structure/frais généraux.

## 7. Risques identifiés

| Risque | Niveau | Commentaire |
|---|---|---|
| Double comptage RH | Élevé | Principal risque Palier 4 si écritures analytiques RH et ventilations sont additionnées |
| Tests budget non isolés de la base recette | Moyen | Le code est stable sur base fraîche, mais la recette persistante peut faire échouer les tests |
| Multi-société incomplet | Faible à moyen | Acceptable si GLC mono-société ; à renforcer sinon |
| A3 erreur non lisible sur cas limite | Faible | Import `_` manquant |
| Saisie salary négative | Faible à moyen | Facile à corriger par contrainte |
| Flux bilan inclus dans cockpit | Moyen | À exclure explicitement en Palier 4 |

## 8. Corrections nécessaires avant Palier 4

1. Décider et documenter la source RH du cockpit.
2. Corriger l'import `_` dans `models/glc_account_funding_rule.py`.
3. Ajouter une contrainte empêchant `percent < 0` et `hours < 0` sur `glc.salary.allocation.line`.
4. Adapter les tests budget pour ne pas dépendre d'années fixes déjà présentes en recette.
5. Documenter les flux exclus du cockpit : emprunts, virements internes, reprises de solde, flux bilan.

## 9. Corrections reportables après Palier 4

- Factoriser les mixins de contrôle de plans si le cockpit introduit un service commun.
- Ajouter des règles multi-société strictes si le contexte GLC évolue.
- Harmoniser les descriptions manifest avec la roadmap réelle Budget / Cockpit.
- Ajouter des vues pivot/graph simples sur les lignes budgétaires si la MOA en exprime le besoin.

## 10. Décision MOA

**Décision proposée : GO avec réserves légères.**

Les Paliers 0 à 3 peuvent être considérés comme gelés pour ouvrir le cadrage technique du Palier 4, à condition de traiter en premier la règle RH / Personnel. Le cockpit doit être développé comme couche d'agrégation et d'alerte, sans modifier la doctrine des modules existants : `analytics` reste la source du réalisé et des ventilations salariales, `budget` reste la source du prévisionnel.

