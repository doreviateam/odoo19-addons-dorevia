# Doctrine — modules Cash Dorevia

**Périmètre** : chaîne **Cash Guard** → **Cash Flow** → (éventuellement) **modules de simulation**  
**Dépôt** : `odoo19-addons-dorevia`  
**Statut** : doctrine produit — cohérence post **V1.1** `dorevia_cash_flow` (trajectoire de référence automatique)

---

## Formules de synthèse

> **Cash Flow affiche la trajectoire de référence.**  
> **Cash Guard prépare et contrôle les projections.**  
> **Les modules de simulation enrichissent les hypothèses.**

La trajectoire ainsi produite et affichée par **`dorevia_cash_flow`** constitue la **vérité de référence** du **pilotage cash** : tout autre écran (y compris dans Cash Guard) qui la reprend doit la montrer en **cohérence** avec Cash Flow, **sans** la redéfinir ni la rendre éditable hors du périmètre prévu.

Ces trois phrases définissent la **séparation des rôles** : lecture synthétique / atelier de projection / hypothèses. Aucun module ne doit empiéter sur le rôle principal d’un autre sans arbitrage explicite.

---

## Chaîne fonctionnelle cible

### Flux nominal (référence)

```text
Données comptables / bancaires / factures
        ↓
Cash Guard  (atelier + projection de référence système : journaux, situation, mailles)
        ↓
Mailles de la projection de référence
        ↓
Cash Flow   (lecture : trajectoire de référence, graphique)
        ↓
Trajectoire de référence
```

### Avec simulation (hypothèses)

```text
Devis / commandes / hypothèses métier
        ↓
Modules de simulation  (scénarios contrôlés)
        ↓
Cash Guard enrichi     (mêmes mailles / même document de projection)
        ↓
Cash Flow
        ↓
Trajectoire affichée   (reflète les montants déjà présents dans les mailles)
```

**Règle** : la simulation **n’alimente pas** un second écran de « trajectoire officielle » parallèle. Elle enrichit **Cash Guard** ; **Cash Flow** ne fait que **restituer** ce qui figure dans les données de projection déjà calculées.

---

## Projection de référence système (Cash Guard)

**Décision produit** : la **projection de trésorerie de référence** pour la société courante est une **donnée préparée et maintenue** côté **`dorevia_cash_guard`** (ou par des mécanismes **système / administrateur** qu’il expose). Elle est **hebdomadaire**, porte une **date de situation**, produit ses **mailles**, et est **identifiable** comme projection servant la lecture cockpit / trajectoire.

**`dorevia_cash_flow`** **consomme** cette référence pour construire les **points** et afficher la **trajectoire**. Il **ne doit pas** créer ni posséder en silence la **vie** d’un document Guard de référence : pas de fabrication opaque d’une projection « pour les beaux yeux du graphique » hors cadre Guard.

**Parcours nominal métier** : ouvrir **Projection > Trésorerie > Accueil graphique** → voir la trajectoire — **sans** prérequis du type « aller dans Projections de trésorerie, choisir le document 1, activer, recalculer, revenir ». Si la référence **manque**, la remédiation relève du **système** ou de l’**administration**, pas d’une obligation fonctionnelle équivalente pour l’utilisateur métier dans le même parcours.

**Implémentation** : l’heuristique actuelle de résolution (premier Guard éligible) est un **palliatif** tant qu’une **référence système explicite** n’est pas livrée — voir **`dorevia_cash_guard/docs/TICKET_CASH_GUARD_SYSTEM_REFERENCE_PROJECTION.md`** (V1 : projection standard **`is_system_reference`**, unicité par société, résolution prioritaire Cash Flow, protection archivage / suppression, message admin si absence).

---

## Rôle de chaque brique

### `dorevia_cash_flow`

| | |
|--|--|
| **Rôle** | **Lecture graphique de référence** pour la société courante. |
| **Fait** | Identifie la **projection de référence** fournie par Cash Guard (règles documentées dans `dorevia_cash_flow` / SPEC), construit les points de courbe, affiche le graphique de pilotage (repères situation / seuil, constaté / projeté). |
| **Ne fait pas** | Créer ou maintenir le **document** de projection de référence sur `dorevia.cash.guard` ; recalcul de projection ; logique de simulation ; atelier d’hypothèses ; écriture sur les documents Cash Guard. |

L’**Accueil graphique** et les raccourcis **Analyse** sont les **entrées de lecture** : ouverture directe sur la trajectoire lorsque la référence est **disponible** (voir § *Projection de référence système*). Un parcours secondaire permet de choisir une **autre** projection pour audit.

---

### `dorevia_cash_guard`

| | |
|--|--|
| **Rôle** | **Atelier de projection** : préparer, structurer, documenter et contrôler les projections. |
| **Fait** | Journaux suivis, date de situation, seuils, calcul des mailles, explication des tensions, recalcul à la demande, traçabilité des hypothèses intégrées au document de projection. **Cible** : maintenir une **projection de référence système** par société pour alimenter Cash Flow sans prérequis manuel métier sur le parcours nominal — voir `dorevia_cash_guard/docs/TICKET_CASH_GUARD_SYSTEM_REFERENCE_PROJECTION.md`. Peut **réafficher** la trajectoire (Cash Flow) en **lecture seule** (**Accueil graphique**) — voir § *Réutilisation dans Cash Guard*. |
| **Ne fait pas** | Porter une **deuxième** trajectoire graphique « officielle » concurrente de Cash Flow, ni un second moteur de courbe / de points dupliqué ; **ne pas modifier** la trajectoire de référence depuis l’UI Cash Guard lorsqu’elle est embarquée en réutilisation. |

Cash Guard reste la **source contrôlée** des mailles et des hypothèses portées par le document de projection.

---

### Modules de simulation (ex. `dorevia_cash_simulation`)

| | |
|--|--|
| **Rôle** | **Enrichissement des hypothèses** (devis, commandes, scénarios), dans le cadre défini par chaque module. |
| **Fait** | Propose des scénarios qui **alimentent** ou **paramètrent** Cash Guard selon les règles du module ; reste explicitement dans la couche « hypothèse ». |
| **Ne fait pas** | Produire une **trajectoire de référence concurrente** ni un rapport de lecture synthétique équivalent à Cash Flow ; ne pas laisser croire qu’une simulation est une donnée comptable certaine. |

---

## Distinctions produit à respecter

| Notion | Où ça vit | Lecture utilisateur typique |
|--------|-----------|-------------------------------|
| **Projection de référence (système)** | `dorevia_cash_guard` (donnée préparée) | « Quel document sert la vérité cash pour la société ? » — un Guard désigné, hebdo, mailles, non choisi à la main par l’utilisateur métier dans le parcours nominal. |
| **Trajectoire de référence** | `dorevia_cash_flow` | « Où va ma trésorerie ? » — une courbe, société courante (à partir de la projection de référence système). |
| **Projection de trésorerie** | `dorevia_cash_guard` | « Comment est construite ma projection ? » — document, mailles, audit. |
| **Simulation / hypothèses** | Modules dédiés | « Que se passe-t-il si… ? » — scénario, impact sur Cash Guard. |

---

## Réutilisation de la trajectoire de référence dans Cash Guard

- **`dorevia_cash_flow`** porte la **trajectoire de référence** (construction des points, graphique, repères) : c’est la **vérité affichée** pour le pilotage cash.
- Cette trajectoire peut être **affichée dans `dorevia_cash_guard`** (par exemple page ou bloc d’**accueil** / cockpit), pour donner le même fil conducteur qu’à l’utilisateur qui entre par l’atelier.
- Elle est **non modifiable depuis Cash Guard** : pas d’édition directe de la courbe, des paramètres graphiques propres à Cash Flow, ni de contournement des règles de résolution de référence définies côté Cash Flow.
- Cash Guard fournit les **actions de travail autour** de cette vérité : ouvrir la projection source, recalculer / actualiser la projection, consulter les documents explicatifs, ajuster les paramètres de projection, tester des hypothèses, accéder aux simulations — le tout en restant dans le périmètre **atelier / document de projection**.
- Toute réutilisation doit se faire **sans duplication de logique** ni **second moteur graphique concurrent** : réutiliser les vues / actions / services exposés par **`dorevia_cash_flow`** (ou une dépendance technique explicite documentée), pas une réimplémentation parallèle de la courbe.

Ticket d’évolution associé : `dorevia_cash_guard/docs/TICKET_CASH_GUARD_HOME_REFERENCE_TRAJECTORY.md`.

### État actuel de l’UI vs cible cockpit

> **Parcours nominal** : **Comptabilité > Projection > Trésorerie > Accueil graphique** — même trajectoire de référence (`dorevia_cash_flow`), lecture seule sur la courbe, raccourcis atelier. **Atelier** : **Projection > Trésorerie > Projections de trésorerie**. **Budgets** : entrée **Projection > Budgets** (menu budget existant).  
> **Raccourcis Analyse** (secondaire, libellés explicites) : **Trajectoire (Analyse)** et **Trajectoire — choix projection (Analyse)** sous **Comptabilité > Analyse** (chemin intermédiaire *Gestion* selon la base).  
> Le ticket `dorevia_cash_guard/docs/TICKET_CASH_GUARD_HOME_REFERENCE_TRAJECTORY.md` formalise le cadrage ; les menus **Accueil graphique** sont déclarés dans **`dorevia_cash_flow`** pour respecter la dépendance module (pas de cycle Guard → Flow).

---

## Anti-doublons et responsabilités

| Risque | Doctrine |
|--------|----------|
| Deux « vérités » de trajectoire | Une seule **trajectoire de référence** : **Cash Flow**. Les autres écrans sont projection détaillée ou simulation. |
| Simulation = réalité | Libellés et aide en ligne doivent dire **hypothèse** ; les montants ne deviennent « réels » que via la chaîne comptable / Cash Guard selon les règles métier. |
| Cash Flow qui recalcule | Interdit : Cash Flow **lit** les mailles déjà produites ; le recalcul est côté **Cash Guard** (ou module source). |
| Cash Guard et le grand graphique | Le **détail** opérationnel peut rester dans Cash Guard. La **synthèse** lecture référence est **Cash Flow** ; si Cash Guard **embarque** la trajectoire d’accueil, ce doit être la **même** restitution Cash Flow, en **lecture seule** — pas une courbe « maison » concurrente. |
| Référence « inventée » par l’heuristique | La **projection de référence** doit être une **donnée système** identifiable côté Guard ; éviter qu’une simple règle de tri sur des documents métier **remplace** durablement cette intention sans cadrage explicite — voir ticket système. |

**Chaîne de responsabilité** : **existence et qualité** de la projection de référence système → **Cash Guard** (et mécanismes admin / système associés) ; exactitude de la courbe et des repères affichés → **Cash Flow** (sur la base des données fournies) ; périmètre des scénarios → **modules de simulation** + règles documentées de chaque module.

---

## Règles UX (à aligner progressivement)

- **Trajectoire de référence** = lecture **Accueil graphique** (**Projection > Trésorerie**) ou raccourci **Trajectoire (Analyse)** ; pas l’atelier de saisie.
- **Projections de trésorerie** (Cash Guard) = **atelier** de travail, recalcul, audit (**Projection > Trésorerie > Projections de trésorerie**).
- **Simulation** (ventes / achats / …) = **hypothèses** ; titres et menus doivent éviter « trajectoire officielle » en doublon de Cash Flow.
- **Accueil graphique** : **Projection > Trésorerie > Accueil graphique** (`dorevia_cash_flow`) — voir tickets `TICKET_CASH_GUARD_HOME_REFERENCE_TRAJECTORY.md` (UI) et `TICKET_CASH_GUARD_SYSTEM_REFERENCE_PROJECTION.md` (donnée de référence).
- Les **README** des modules Cash (`dorevia_cash_flow`, `dorevia_cash_guard`, `dorevia_cash_simulation`, …) doivent **renvoyer à ce document** pour le positionnement relatif.

---

## Évolution documentaire

- **Implémentation** : specs et recettes par module (`docs/` dans chaque addon).
- **Doctrine transverse** : **ce fichier** ; toute évolution de périmètre Cash (nouveau module, nouveau menu) met à jour ce document en priorité, puis les README concernés.

---

## Références utiles

- `docs/cash/PV_RECETTE_NAVIGATION_CASH.md` — PV recette navigation Cash (**GO**), captures sous `docs/cash/captures/`.
- `dorevia_cash_flow/README.md` — parcours V1.1, menu nominal.
- `dorevia_cash_flow/docs/SPEC_CASH_FLOW_TRAJECTORY.md` — § 5.5 résolution de référence.
- `dorevia_cash_flow/views/cash_guard_bridge_menus.xml` — **Accueil graphique** sous **Projection > Trésorerie**.
- `dorevia_cash_flow/docs/TICKET_CASH_FLOW_V1_1_TRAJECTOIRE_REFERENCE.md` — cadrage ticket V1.1.
- `dorevia_cash_guard/README.md` — atelier de projection.
- `dorevia_cash_guard/docs/TICKET_CASH_GUARD_SYSTEM_REFERENCE_PROJECTION.md` — projection de référence **système** (cible produit, périmètre technique).
- `dorevia_cash_guard/docs/TICKET_IMPL_CASH_GUARD_SYSTEM_REFERENCE.md` — implémentation code + tests (sous-ticket dev).
- `dorevia_cash_guard/docs/TICKET_CASH_GUARD_HOME_REFERENCE_TRAJECTORY.md` — accueil graphique / trajectoire (lecture seule, réutilisation Cash Flow).
- `dorevia_cash_simulation/README.md` — hypothèses devis / extension Cash Guard.
