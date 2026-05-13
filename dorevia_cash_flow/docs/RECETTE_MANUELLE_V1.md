# Scénario de recette manuelle — Trajectoire de trésorerie (V1 / V1.1)

**Module** : `dorevia_cash_flow`  
**Version cible** : **V1.1** (parcours nominal : trajectoire de **référence** sans sélection préalable) ; le parcours **assistant + bouton** reste disponible en **secondaire**.  
**Rôle testeur** : utilisateur métier ou fonctionnel avec droits Cash Guard  
**Références** : `SPEC_CASH_FLOW_TRAJECTORY.md` (§ 5.5 V1.1), `docs/TICKET_CASH_FLOW_V1_1_TRAJECTOIRE_REFERENCE.md`, **[Doctrine modules Cash](../../docs/cash/DOCTRINE_CASH_MODULES.md)** (rôles Cash / lecture vs projection), `RECETTE_VUE_GRAPH.md`, `RECETTE_FONCTIONNELLE_V1.md`

Ce document est le **guide d’exécution** : actions dans l’interface, observations, critères de succès. Le cadrage objectifs / hors périmètre détaillé reste dans `RECETTE_FONCTIONNELLE_V1.md`.

---

## Menus concernés

| Menu | Rôle |
|------|------|
| **Comptabilité > Analyse > Trajectoire de trésorerie** | **Parcours nominal V1.1** : ouverture **directe** du graphique de pilotage (projection de référence résolue automatiquement). |
| **Comptabilité > Analyse > Trajectoire (choix de projection)** | **Parcours secondaire** : assistant + sélection manuelle d’une projection puis **Afficher la trajectoire**. |

---

## Avant de commencer (cochez quand c’est prêt)

| # | Contrôle | ☐ |
|---|-----------|---|
| A1 | Modules `account`, `dorevia_cash_guard`, `dorevia_cash_flow` installés (version **≥ 19.0.2.0.0** pour la V1.1 menu direct) | ☐ |
| A2 | Utilisateur dans le groupe autorisé pour Cash Guard | ☐ |
| A3 | Pour la société courante : au moins une projection **hebdomadaire**, **active**, avec **mailles hebdomadaires** calculées (`weekly_line_ids`), **date de situation** et **seuil d’alerte** cohérents | ☐ |
| A4 | **Optionnel mais recommandé** : identifier dans Cash Guard la projection attendue comme **référence** (parmi les actives hebdo avec mailles : celle avec la **date de situation la plus récente**) ; noter **date de situation**, **seuil**, **solde constaté** pour contrôle croisé avec le bandeau du graphique | ☐ |

**Données idéales** : plusieurs semaines constatées depuis le début d’exercice + plusieurs mailles projetées après la date de situation.

---

## Parcours nominal — trajectoire de référence (V1.1)

À exécuter **dans l’ordre**. Pour chaque pas : **Action** → **Contrôles** → cocher **OK** ou noter l’écart dans **Observations**.

### Repères visuels (M5 à M7) — cible fonctionnelle vs acceptable

Pour la **ligne verticale** « situation », le **plein / pointillé** (constaté / projeté) et la **ligne horizontale** de seuil :

- **Cible fonctionnelle** : repères **visibles sur le graphique de pilotage** (écran après le menu nominal). Le scénario peut rester **strict** sur cette cible.
- **Acceptable** si contrôle limité à la **vue Graph native** (après **Liste des points**) : informations claires dans le **sous-titre / bandeau** + limites documentées dans *RECETTE_VUE_GRAPH.md* — cocher **OK avec réserve** et préciser en **Observations**.

| Pas | Action (manuelle) | Contrôles (observer) | OK | Observations |
|-----|-------------------|----------------------|----|----------------|
| M1 | Ouvrir **Comptabilité > Analyse > Trajectoire de trésorerie** | Le **graphique de pilotage** s’affiche **directement** dans la zone principale (pas d’étape obligatoire d’assistant au préalable) ; pas d’erreur bloquante ; le libellé du menu est clair ; on n’est pas dans le menu opérationnel des projections Cash Guard | ☐ | |
| M2 | Lire le **bandeau / sous-titre** sous le titre du graphique | Le **nom de la projection** utilisée est affiché ; la **date de situation** et le **seuil d’alerte** sont rappelés et cohérents avec la projection de référence attendue (cf. règle : société courante, active, hebdomadaire, mailles présentes, `situation_date` la plus récente — voir § 5.5 de la spec) | ☐ | |
| M3 | Vérifier la présence du **point bas** dans le bandeau (si données) | **Point bas** (montant + date) et/ou **message d’information** affichés lorsque la courbe et les calculs le permettent ; pas de bandeau vide alors que la courbe est chargée | ☐ | |
| M4 | Regarder la **courbe** principale | **Une seule** trajectoire de solde dans le temps ; pas deux courbes « concurrentes » ; pas de chute artificielle à zéro sur le constaté | ☐ | |
| M5 | Repérer la **ligne verticale** « situation » | **Cible** : ligne verticale visible ; à gauche **constaté**, à droite **projeté**. **Acceptable** : date de situation claire dans le sous-titre + *RECETTE_VUE_GRAPH.md* si Graph native seule — noter la réserve. | ☐ | |
| M6 | Comparer trait **plein** vs **pointillé** | **Cible** : **trait plein** côté constaté, **pointillé** côté projeté. **Acceptable** : distinction lisible (texte / légende) + *RECETTE_VUE_GRAPH.md* si Graph native seule. | ☐ | |
| M7 | Repérer la **ligne horizontale** de seuil | **Cible** : ligne visible sur le graphique ; valeur cohérente avec le sous-titre. **Acceptable** : seuil dans le sous-titre sans ligne sur la Graph native ; *RECETTE_VUE_GRAPH.md*. | ☐ | |
| M8 | Vérifier l’**axe des dates** (graduations) | Ordre chronologique logique ; horizon projeté d’environ **90 jours** après la date de situation | ☐ | |
| M9 | Vérifier l’**axe des montants** | Libellés en **soldes** (monnaie), pas une lecture « flux mensuels » trompeuse | ☐ | |
| M10 | Cliquer **Liste des points** | Fenêtre avec liste + vue Graph **native** possible ; cohérence des valeurs avec la courbe (audit) | ☐ | |

---

## Parcours secondaire — choix manuel de projection

À exécuter **en complément** ou pour audit / comparaison. Même critères graphiques une fois le graphique ouvert.

| Pas | Action (manuelle) | Contrôles (observer) | OK | Observations |
|-----|-------------------|----------------------|----|----------------|
| S1 | Ouvrir **Comptabilité > Analyse > Trajectoire (choix de projection)** **ou**, depuis le graphique, cliquer **Changer de projection** | Un **assistant** (formulaire) s’ouvre ; le champ projection est disponible | ☐ | |
| S2 | Choisir une projection **hebdomadaire** | Domaine cohérent (société, actif, semaine) ; date de situation et seuil visibles sur le formulaire | ☐ | |
| S3 | Cliquer **Afficher la trajectoire** | Le graphique de pilotage s’ouvre comme en parcours nominal ; les contrôles M4–M10 s’appliquent | ☐ | |

---

## Contrôles complémentaires (recette manuelle)

### C1 — Pas de recalcul intempestif Cash Guard

Pendant **M1** (ouverture directe) ou **S3** : vous ne devez **pas** voir un recalcul complet de projection déclenché **automatiquement** par Cash Flow. Comportement attendu : **lecture** des mailles déjà présentes, **sauf** si vous aviez vous-même lancé un recalcul ailleurs.

| OK | Observations |
|----|----------------|
| ☐ | |

### C2 — Liste des points vs courbe

Après **M10** : trier par date ; segments **Constaté** puis **Projeté** ; pas de valeurs fantaisistes à zéro intercalées.

| OK | Observations |
|----|----------------|
| ☐ | |

---

## Cas limites (sessions de test séparées)

### L0 — Aucune projection exploitable (parcours nominal)

**Action** : pour la société courante, désactiver ou archiver toutes les projections hebdomadaires avec mailles **ou** ne laisser que des projections sans mailles calculées ; ouvrir **Trajectoire de trésorerie** (menu nominal).

**Contrôle** : message **clair** (pas de courbe vide trompeuse) invitant à créer ou actualiser une projection dans **Projections de trésorerie** (Cash Guard).

| OK | Observations |
|----|----------------|
| ☐ | |

### L1 — Projection non hebdomadaire (parcours secondaire)

**Action** : via **Trajectoire (choix de projection)** ou équivalent, tenter une projection **mensuelle** / **trimestrielle** si le domaine le permet.

**Contrôle** : message d’erreur **clair** ; seule la périodicité **semaine** est prise en charge ; aucune courbe absurde.

| OK | Observations |
|----|----------------|
| ☐ | |

### L2 — Projection sans mailles hebdo

**Action** : projection hebdo sans `weekly_line_ids` (ou données incomplètes) — scénario nominal **ou** secondaire selon le cas testé.

**Contrôle** : message invitant à **actualiser / recalculer** depuis Cash Guard ; pas de graphique vide sans explication.

| OK | Observations |
|----|----------------|
| ☐ | |

### L3 — Horizon projeté

**Action** : compter ou estimer le nombre de points **projetés** après la date de situation.

**Contrôle** : aucun point projeté **au-delà** de la règle « situation + 90 jours » (tolérance d’une maille en bord de semaine).

| OK | Observations |
|----|----------------|
| ☐ | |

---

## Décision (à remplir en fin de session)

| Verdict | ☐ GO | ☐ GO avec réserves | ☐ NO GO |
|---------|--------|---------------------|---------|

**Réserves / anomalies** :

```text

```

**Signature / date** :

```text

```
