# Mémo d'arbitrage MOA — Lots A / B · Paramétrage analytique GLC

**Module :** `dorevia_glc_analytics` (+ impact `dorevia_glc_budget`)  
**Référence installée (`main`) :** **`19.0.5.0.1`** — Palier 5 trésorerie GO complet MOA · cadrage GQ docs mergé (PR #43)  
**Travail WIP isolé :** branche `wip/glc-analytic-parametrage-type-glc-plan-unique` · commit `03c8736`  
**Date arbitrage :** 2026-05-29  
**Date décision MOA :** 2026-05-29  
**Statut :** **Décision MOA actée — Option C (report WIP A/B)** · **GQ-6 code : décision séparée, toujours en attente**

**Objectif :** permettre une décision MOA claire **avant** toute branche ou GO code GQ-6 qualité/paiement.

---

## 1. Contexte

### 1.1 État actuel sur `main`

| Élément | État |
|---|---|
| Plans analytiques | **2 plans** : `GLC - Activités` (7 comptes) · `GLC - Financements` (4 comptes) |
| Type GLC (`glc_activity_type`) | 5 valeurs : `charge` · `mixte` · `recette` · `charge_subventionnee` · `financement` |
| Codes analytiques officiels | `BAR` · `PRESTATIONS` · `MISSIONS` · `SUBVENTIONS` · `RESSOURCES_PROPRES` · … |
| Détection financement cockpit | Plan Financements **ou** type `financement` **ou** code dans `GLC_COCKPIT_FUNDING_CODES` |
| Menus | `Activités GLC` + `Financements GLC` |
| Version module | `19.0.5.0.1` |

### 1.2 Travail local WIP (non mergé)

Deux lots ont été implémentés et **combinés** dans un seul commit WIP :

| Lot | Version cible | Intention MOA |
|---|---|---|
| **A** | `19.0.5.0.2` | Simplifier Type GLC → Charge · Recette · Mixte uniquement |
| **B** | `19.0.6.0.0` | Plan analytique unique · renommage codes · financements intégrés au plan Activités |

**Important :** le WIP actuel **n'est pas découpable tel quel** en merge Lot A seul — Lot B inclut et étend Lot A. Un merge Lot A nécessiterait un **cherry-pick / rebase ciblé** depuis le WIP.

**Tests sandbox (WIP complet) :** 96/96 OK après upgrade sur `glc-rgl-test-import` *(non rejoués sur ce mémo)*.

---

## 2. Option A — Type GLC simplifié `19.0.5.0.2`

### 2.1 Périmètre exact

| Zone | Contenu Lot A seul |
|---|---|
| **Modèle** | `account_analytic_account.py` — selection réduite à 3 valeurs |
| **Migration SQL** | `charge_subventionnee` → `charge` · `financement` → `recette` |
| **Hooks** | `_migrate_glc_activity_type_legacy_values` + normalisation types sur comptes seed |
| **Cockpit** | Retrait détection financement via `glc_activity_type == "financement"` *(à conserver : détection par plan Financements)* |
| **Codes / plans** | **Inchangés** — BAR, PRESTATIONS, SUBVENTIONS, 2 plans conservés |
| **Menus / vues** | **Inchangés** |
| **Budget** | **Inchangé** — validation plan Activités vs Financements conservée |
| **Constants** | **Inchangées** |
| **Fichiers touchés (estimation)** | ~4–5 fichiers + migration `19.0.5.0.2/` |

**Hors périmètre Lot A :** renommage codes · fusion plans · menus · budget mixin · anomaly wizard par codes.

### 2.2 Bénéfice métier

- **Lisibilité MOA** : Type GLC redevient une nature de lecture cockpit (charge / recette / mixte), sans typologies hybrides (`charge_subventionnee`, `financement`).
- **Alignement sémantique** : les comptes financement passent en Type GLC = Recette tout en restant identifiables par **plan Financements**.
- **Changement limité** : pas de restructuration des plans ni des codes — MOA continue de parler BAR, SUBVENTIONS, etc.
- **Recettes existantes** : compatibilité maximale avec Palier 4/5 et docs actuelles.

### 2.3 Risque de régression

| Risque | Niveau | Commentaire |
|---|---|---|
| Perte sémantique `charge_subventionnee` | **Faible** | Résidences → `charge` ; pilotage inchangé si code `RESIDENCES` conservé |
| Confusion financement = recette (type) | **Moyen** | Les 4 comptes Financements auront Type GLC = Recette ; la **distinction reste le plan** |
| Cockpit financements | **Faible** | Si plan Financements conservé dans `_is_funding_analytic_account` |
| Budget Palier 3 | **Nul** | Règles plan Activités / Financements inchangées |
| Données custom MOA | **Faible** | Migration SQL sur valeurs legacy uniquement |

### 2.4 Impact migrations

| Migration | Rôle |
|---|---|
| `19.0.5.0.2/post-migrate.py` | Existe dans WIP — appelle migration types + normalisations hooks existantes |
| Réversibilité | **Partielle** — retour arrière types possible manuellement ; pas de downgrade auto |
| Bases prod | Upgrade `-u dorevia_glc_analytics` · durée faible (UPDATE SQL) |
| Coexistence Palier 5 | **Compatible** — pas de toucher trésorerie |

### 2.5 Impact tests

| Fichier | Impact Lot A seul |
|---|---|
| `test_analytic_setup.py` | + test absence types legacy · types recette sur financements |
| `test_coverage_cockpit.py` | Minimal si plan Financements conservé |
| `test_analytic_anomaly.py` | Minimal |
| `test_glc_budget.py` | **Aucun** |
| Estimation | ~2–3 tests ajoutés/modifiés · suite globale ~88–96 tests |

### 2.6 Possibilité de merge seul

**Oui, techniquement** — sous conditions :

1. **Extraire** Lot A du WIP (commit dédié depuis `main`, pas le commit WIP combiné).
2. **Adapter** `glc_coverage_cockpit._is_funding_analytic_account` pour **garder** la détection par plan Financements (le WIP combiné l'a retirée au profit des codes).
3. **Ne pas** bumpper au-delà de `19.0.5.0.2`.
4. PR dédiée · recette MOA ciblée Type GLC · non-régression Palier 5.

**Effort Dev estimé :** 0,5–1 j (découpe WIP + PR + revalidation tests).

---

## 3. Option B — Plan analytique unique `19.0.6.0.0`

### 3.1 Périmètre exact

| Zone | Contenu |
|---|---|
| **Plan** | Un seul plan seed `GLC - Activités` — plan Financements **retiré du XML** |
| **Comptes** | **11 comptes officiels** sur plan unique (activités + ressources + structure) |
| **Codes cibles** | Renommages MOA (voir §3.6) |
| **Type GLC** | 3 valeurs · financements = `recette` |
| **Constants** | `GLC_OFFICIAL_ANALYTIC_CODES` · `GLC_ANALYTIC_CODE_MIGRATION` · codes cockpit/budget mis à jour |
| **Cockpit** | Funding **uniquement par code** (`ADHESIONS`, `DONS`, `FIN_EXT`, `FIN_INT`) |
| **Anomaly wizard** | Split activité/financement par **codes** sur plan unique |
| **Salary mixin** | Exclusion funding par codes |
| **Budget** | Validation funding par codes sur plan Activités unique |
| **UI** | Menu unique `Comptes analytiques GLC` · suppression menu Financements |
| **Hooks** | Migration types + codes + fusion plans + normalisation complète |
| **Fichiers touchés** | **20 fichiers** (+2 migrations) — diff WIP complet |

### 3.2 Absorption ou non du Lot A

**Oui — Lot B absorbe intégralement Lot A.**

| Élément Lot A | Dans Lot B |
|---|---|
| Selection 3 valeurs Type GLC | ✅ Inclus |
| Migration types legacy | ✅ Inclus (`19.0.6.0.0` rappelle `_migrate_glc_activity_type_legacy_values`) |
| Retrait type `financement` pour détection cockpit | ✅ Inclus — remplacé par logique **codes** |

**Conséquence :** si MOA acte Option B, **inutile** de merger Lot A séparément. Une seule PR `19.0.6.0.0`.

### 3.3 Impact plans Activités / Financements

| Avant (`main`) | Après Option B |
|---|---|
| Plan `GLC - Activités` — 7 comptes | Plan `GLC - Activités` — **11 comptes** |
| Plan `GLC - Financements` — 4 comptes | Plan **retiré du seed XML** |
| Comptes financement sur plan Financements | Comptes **déplacés** sur plan Activités |
| Plan Financements en base existante | Migration : comptes → plan Activités · plan renommé **`GLC - Financements (archivé)`** *(Odoo 19 sans champ `active` sur plan)* |

**Point MOA :** le plan archivé peut subsister en base (orphelin de comptes) — visible uniquement si recherche admin. Les écritures historiques restent liées aux comptes (IDs inchangés), seuls **plan_id** et **code** évoluent.

### 3.4 Impact doctrine cockpit

| Doctrine | Impact |
|---|---|
| KPI exploitation (Recette · RH · Dépense · Solde) | **Aucun changement de formule** — agrégation toujours par `account.analytic.line` |
| Détection recettes activité vs financement | **Par code** au lieu de plan + type |
| R15 financements multi-plans | **Simplifié** — un seul plan · codes `FIN_EXT` / `FIN_INT` remplacent `SUBVENTIONS` / `RESSOURCES_PROPRES` |
| Palier 5 trésorerie | **Aucun impact** — couche séparée |
| Filtre axe analytique cockpit | Codes affichés changent (ex. `BAR` → `BAR_REST`) |
| Invariant GQ (futur) | **Compatible** — Q1 couverture analytique bénéficie d'un référentiel unique |

**Changement de lecture MOA :** les financements ne sont plus « sur un autre plan », mais « des comptes recette identifiés par code » sur le même plan.

### 3.5 Impact recettes existantes

| Document | Impact |
|---|---|
| `RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md` | **Mise à jour requise** — références BAR, PRESTATIONS, SUBVENTIONS, MISSIONS, tests R15/R17 |
| `RECETTE_MANUELLE_PALIER_5_TRESORERIE_*.md` | **Partiel** — table legacy déjà amorcée (`BAR_REST` ↔ `BAR`) · à compléter |
| `TICKET_COCKPIT_DOCTRINE_CLASSE_6_7.md` | **Mise à jour** — liste codes et plans |
| `TICKET_COCKPIT_SOURCE_REALISE.md` | **Mise à jour** — axes financement |
| `PALIERS.md` | **Mise à jour** — Palier 0 socle 2 plans → 1 plan |
| Recette GQ (PR #43) | **Faible** — pas de dépendance codes legacy |

**Effort doc post-merge B :** 1–2 j MOA/Dev pour aligner recettes Palier 4/5.

### 3.6 Migration comptes / codes

| Code actuel (`main`) | Code cible (Option B) | Libellé cible |
|---|---|---|
| `STRUCTURE` | `STRUCTURE` | Structure & Administration |
| `BAR` | `BAR_REST` | Bar, Restauration & Cuisine |
| `PRESTATIONS` | `PRESTA` | Prestations & Animations |
| `RESIDENCES` | `RESIDENCES` | Résidences artistiques |
| `MISSIONS` | `DEPL_MIS` | Déplacements & Missions |
| `PRIVATISATIONS` | `LOC_PRIV` | Privatisation d'espace |
| `LOCATION_RADIO` | `LOC_RGL` | Location Radio Grand Lieu |
| `ADHESIONS` | `ADHESIONS` | Adhésions |
| `DONS` | `DONS` | Dons |
| `SUBVENTIONS` | `FIN_EXT` | Financement externe |
| `RESSOURCES_PROPRES` | `FIN_INT` | Financement interne |

**Migrations :**

| Version | Script |
|---|---|
| `19.0.5.0.2` | Types legacy uniquement *(inclus dans chaîne 6.0.0)* |
| `19.0.6.0.0` | Types + codes + fusion plan + normalisation XML noupdate |

**Risque données :** comptes analytiques **custom MOA** (hors seed) non migrés automatiquement — à inventorier avant prod.

### 3.7 Risques MOA

| Risque | Niveau | Mitigation |
|---|---|---|
| Rupture habitudes saisie (2 plans → 1) | **Élevé** | Communication MOA · menu unique · formation |
| Confusion codes renommés | **Élevé** | Table de correspondance · période transition · doc recette |
| Rapports / exports externes référencant BAR, SUBVENTIONS | **Moyen** | Audit usages hors Odoo |
| Plan Financements archivé visible en admin | **Faible** | Renommage explicite « (archivé) » |
| Budgets Palier 3 existants | **Moyen** | Comptes IDs conservés · codes changent · revalidation budgets ouverts |
| Intégrations / imports analytiques | **Moyen à élevé** | Mapping codes à communiquer |
| Régression cockpit R15/R17 | **Faible** si tests OK | 96/96 sandbox · recette MOA navigateur obligatoire |
| Décision MOA prématurée | **Moyen** | Ce mémo — pas de merge sans GO explicite |

---

## 4. Option C — Report du WIP

### 4.1 Ce qu'on conserve

| Élément | Action |
|---|---|
| Branche WIP distante | **Conserver** `wip/glc-analytic-parametrage-type-glc-plan-unique` @ `03c8736` |
| Commit WIP | Référence technique prête si MOA acte A ou B plus tard |
| `main` | Reste sur **`19.0.5.0.1`** — stable · Palier 5 + docs GQ |
| Cadrage GQ (PR #43) | **Déjà sécurisé** sur `main` |

### 4.2 Ce qu'on abandonne (temporairement)

| Élément | Action |
|---|---|
| Merge Lots A/B | **Reporté** — pas de PR ouverte |
| Normalisation codes MOA | **En attente** |
| Plan unique | **En attente** |
| Recette MOA paramétrage | **Non lancée** |

**Note :** « abandonner » ≠ supprimer la branche WIP — le travail reste récupérable.

### 4.3 Conséquence sur GQ-6

| Aspect | Conséquence |
|---|---|
| **GO code GQ-6** | Peut être acté **indépendamment** du report A/B — les lots sont disjoints |
| **Branche GQ-6** | Créable depuis `main` + docs PR #43 **sans attendre** A/B |
| **Couverture analytique Q1** | Fonctionne avec référentiel actuel (2 plans · 5 types GLC) |
| **Dette paramétrage** | Types GLC ambigus et double plan **persistent** — Q1 pourra remonter des cas « financement vs recette » moins lisibles |
| **Version GQ-6** | Voir §5 |

### 4.4 Version recommandée pour GQ-6 si Option C

| Scénario | Version recommandée | Justification |
|---|---|---|
| **Report A/B + GO GQ-6** | **`19.0.6.1.0`** ou **`19.0.7.0.0`** | Évite collision avec `19.0.6.0.0` réservé plan unique · signalise lot fonctionnel distinct |
| Si Lot B mergé **avant** GQ-6 | **`19.0.6.1.0`** | Patch fonctionnel post-paramétrage |
| Si Lot A seul mergé **avant** GQ-6 | **`19.0.5.1.0`** ou **`19.0.6.0.0`** | Selon convention semver interne |

**Recommandation Dev (si report A/B) :** **`19.0.7.0.0`** pour GQ-6 — séparation claire paramétrage (`19.0.6.x`) vs fonctionnel qualité/paiement (`19.0.7.0.0`).

---

## 5. Tableau comparatif synthétique

| Critère | Option A `19.0.5.0.2` | Option B `19.0.6.0.0` | Option C — Report |
|---|---|---|---|
| **Effort Dev merge** | Faible (découpe WIP) | Faible (WIP prêt) | Nul |
| **Effort MOA / change** | Faible | **Élevé** | Nul |
| **Impact recettes** | Minimal | **Important** | Aucun |
| **Impact cockpit KPI** | Nul | Nul (codes) | Nul |
| **Impact budget** | Nul | Moyen (règles codes) | Nul |
| **Risque prod** | Faible | Moyen–élevé | Nul |
| **Lisibilité long terme** | Partielle | **Forte** | Statu quo |
| **Bloque GQ-6 ?** | Non | Non | **Non** |
| **PR prête** | Non (découpe requise) | **Oui** (WIP) | — |

---

## 6. Recommandation Dev *(sans décision automatique)*

### 6.1 Lecture Dev

1. **Option A** est un **pas intermédiaire prudent** : il répond à la demande MOA « simplifier Type GLC » sans bouleverser plans, codes ni recettes. Il ne résout pas la complexité structurelle du double plan.

2. **Option B** est la **vision cible cohérente** avec le WIP et la simplification MOA long terme, mais c'est un **changement de paramétrage majeur** — pas un patch technique. Il exige une **validation MOA explicite des codes cibles** et une **passage recette Palier 4/5** avant prod.

3. **Option C** est **valide tactiquement** si la priorité MOA est GQ-6 qualité/paiement : le report n'empêche pas le GO code GQ-6. La dette analytique reste acceptable à court terme.

### 6.2 Recommandation Dev (ordre de préférence)

| Rang | Option | Motivation |
|:---:|---|---|
| **1** | **C puis B** | Lancer GQ-6 sur `main` stable (`19.0.7.0.0`) · traiter plan unique en parallèle ou juste après · minimiser le risque de mélanger paramétrage + qualité/paiement |
| **2** | **B seul** | Si MOA confirme **maintenant** les codes cibles et accepte la mise à jour recettes — une seule PR · WIP prêt · absorbe A |
| **3** | **A seul** | Si MOA veut une quick win Type GLC **sans** plan unique — découpe WIP requise · valeur limitée vs effort doc futur pour B |

**Non recommandé :** merger A **puis** B en deux temps rapprochés sur prod — double migration · double recette · confusion MOA. Préférer **A seul** ou **B direct**.

### 6.3 Ce que Dev ne décide pas

- Validation métier des **codes cibles** (FIN_EXT, BAR_REST, …)
- Acceptation du **menu unique** vs deux menus
- Priorisation GQ-6 vs paramétrage analytique
- Calendrier prod / sandbox recette

---

## 7. Gates MOA — checklist décision

| # | Question MOA | Option A | Option B | Option C |
|---|---|:---:|:---:|:---:|
| G1 | Type GLC = Charge · Recette · Mixte acté ? | ✅ | ✅ | — |
| G2 | Codes cibles (BAR_REST, FIN_EXT, …) actés ? | — | ✅ requis | — |
| G3 | Plan unique acté (vs 2 plans) ? | ❌ | ✅ | — |
| G4 | Recettes Palier 4/5 mises à jour avant prod ? | optionnel | ✅ requis | — |
| G5 | GO merge paramétrage ? | `19.0.5.0.2` | `19.0.6.0.0` | report |
| G6 | GO code GQ-6 *(séparé)* | après G5 ou en parallèle si C | après G5 ou en parallèle si C | **peut précéder G5** |

---

## 8. Prochaines actions selon décision

### Si Option A

1. Découpe branche `feat/glc-type-glc-19.0.5.0.2` depuis `main`
2. Cherry-pick ciblé + adaptation cockpit (garder plan Financements)
3. PR · recette MOA Type GLC · merge
4. Puis arbitrage B ou GQ-6

### Si Option B

1. Retirer label `wip` · PR `feat/glc-plan-unique-19.0.6.0.0`
2. Mise à jour docs recette Palier 4/5
3. Recette MOA navigateur paramétrage
4. Merge · puis GQ-6 depuis `main` (`19.0.6.1.0` ou `19.0.7.0.0`)

### Si Option C

1. Conserver branche WIP (aucune action)
2. Créer branche GQ-6 depuis `main` — **uniquement après GO MOA GQ-6 explicite**
3. Version cible GQ-6 : **`19.0.7.0.0`** recommandée

---

## 9. Références techniques

| Référence | Valeur |
|---|---|
| Branche WIP | `wip/glc-analytic-parametrage-type-glc-plan-unique` |
| Commit WIP | `03c8736` |
| `main` actuel | `5f84f2d` (post-merge PR #43 docs GQ) |
| Module version `main` | `19.0.5.0.1` |
| Module version WIP | `19.0.6.0.0` |
| PR docs GQ | #43 — mergée |

---

## 10. Décision MOA actée (2026-05-29)

**Option retenue : Option C — Report du WIP A/B.**

### Motifs MOA

- Ne pas mélanger paramétrage analytique et lot qualité/paiement.
- Éviter une migration du plan analytique juste avant GQ-6.
- Conserver le WIP en branche dédiée pour reprise ultérieure.
- Permettre à GQ-6 de partir d'un `main` stable en `19.0.5.0.1` + cadrage docs qualité/paiement (PR #43).
- Réserver le plan unique à une décision MOA séparée, avec validation explicite des codes cibles.

### Conséquences actées

| Élément | Décision |
|---|---|
| PR Lot A (`19.0.5.0.2`) | **Non** — reportée |
| PR Lot B (`19.0.6.0.0`) | **Non** — reportée |
| Branche WIP | **Conservée** — `wip/glc-analytic-parametrage-type-glc-plan-unique` @ `03c8736` |
| Base GQ-6 | `main` @ `19.0.5.0.1` + docs GQ |
| Version cible GQ-6 | **`19.0.7.0.0`** *(recommandée Dev, actée MOA)* |
| GO code GQ-6 | **Décision séparée** — pas de GO code à ce stade |

### Prochaine étape autorisée

1. Attendre **GO MOA explicite « démarrage code GQ-6 »**.
2. Créer branche GQ-6 depuis `main` · version `19.0.7.0.0`.
3. Reprise Lots A/B : **ultérieure**, sur décision MOA distincte (Option A ou B).

---

**Décision MOA :** ☐ Option A · ☐ Option B · ☑ **Option C (report)**  
**Commentaire MOA :** Report WIP A/B · GQ-6 préparable depuis `main` stable après GO code séparé · plan unique = décision future.  
**Date :** 2026-05-29
