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
Cash Guard  (atelier : journaux, situation, seuil, mailles, audit)
        ↓
Mailles de projection
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

## Rôle de chaque brique

### `dorevia_cash_flow`

| | |
|--|--|
| **Rôle** | **Lecture graphique de référence** pour la société courante. |
| **Fait** | Identifie une projection Cash Guard de référence (règles documentées dans `dorevia_cash_flow` / SPEC), construit les points de courbe, affiche le graphique de pilotage (repères situation / seuil, constaté / projeté). |
| **Ne fait pas** | Recalcul de projection, logique de simulation, atelier d’hypothèses, écriture sur les documents Cash Guard. |

L’entrée menu **Comptabilité > Analyse > Trajectoire de trésorerie** est l’**écran métier principal de lecture** : ouverture directe sur la trajectoire de référence (V1.1), sans sélection obligatoire pour le cas standard. Un parcours secondaire permet de choisir une autre projection pour audit.

---

### `dorevia_cash_guard`

| | |
|--|--|
| **Rôle** | **Atelier de projection** : préparer, structurer, documenter et contrôler les projections. |
| **Fait** | Journaux suivis, date de situation, seuils, calcul des mailles, explication des tensions, recalcul à la demande, traçabilité des hypothèses intégrées au document de projection. Peut **réafficher** la trajectoire de référence (Cash Flow) en **lecture seule** comme fil d’Ariane d’accueil — voir § *Réutilisation dans Cash Guard*. |
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
| **Trajectoire de référence** | `dorevia_cash_flow` | « Où va ma trésorerie ? » — une courbe, société courante. |
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

> À l’état actuel, la trajectoire de référence est consultable dans `dorevia_cash_flow` via **Comptabilité > Analyse > Gestion > Trajectoire de trésorerie**.  
> Cash Guard reste l’atelier de projection, accessible via le menu **Projection > Trésorerie**.  
> Le ticket `dorevia_cash_guard/docs/TICKET_CASH_GUARD_HOME_REFERENCE_TRAJECTORY.md` décrit une évolution UX future : afficher cette même trajectoire de référence en lecture seule dans un cockpit d’accueil Cash Guard, avec les actions d’atelier autour.  
> Cette évolution n’est pas encore implémentée et ne remet pas en cause la séparation actuelle des rôles.

---

## Anti-doublons et responsabilités

| Risque | Doctrine |
|--------|----------|
| Deux « vérités » de trajectoire | Une seule **trajectoire de référence** : **Cash Flow**. Les autres écrans sont projection détaillée ou simulation. |
| Simulation = réalité | Libellés et aide en ligne doivent dire **hypothèse** ; les montants ne deviennent « réels » que via la chaîne comptable / Cash Guard selon les règles métier. |
| Cash Flow qui recalcule | Interdit : Cash Flow **lit** les mailles déjà produites ; le recalcul est côté **Cash Guard** (ou module source). |
| Cash Guard et le grand graphique | Le **détail** opérationnel peut rester dans Cash Guard. La **synthèse** lecture référence est **Cash Flow** ; si Cash Guard **embarque** la trajectoire d’accueil, ce doit être la **même** restitution Cash Flow, en **lecture seule** — pas une courbe « maison » concurrente. |

**Chaîne de responsabilité** : qualité des mailles et des hypothèses → **Cash Guard** ; exactitude de la courbe et des repères affichés → **Cash Flow** (sur la base des données fournies) ; périmètre des scénarios → **modules de simulation** + règles documentées de chaque module.

---

## Règles UX (à aligner progressivement)

- **Trajectoire de trésorerie** = lecture de **référence** (menu Analyse / Reporting, pas l’atelier).
- **Projections de trésorerie** (Cash Guard) = **atelier** de travail, recalcul, audit.
- **Simulation** (ventes / achats / …) = **hypothèses** ; titres et menus doivent éviter « trajectoire officielle » en doublon de Cash Flow.
- **Accueil Cash Guard** (évolution ciblée) : peut centrer un **bloc trajectoire** issu de **Cash Flow**, **lecture seule**, entouré des **actions d’atelier** (ouvrir projection, recalcul, documents, paramètres, simulations) — voir ticket `dorevia_cash_guard/docs/TICKET_CASH_GUARD_HOME_REFERENCE_TRAJECTORY.md`.
- Les **README** des modules Cash (`dorevia_cash_flow`, `dorevia_cash_guard`, `dorevia_cash_simulation`, …) doivent **renvoyer à ce document** pour le positionnement relatif.

---

## Évolution documentaire

- **Implémentation** : specs et recettes par module (`docs/` dans chaque addon).
- **Doctrine transverse** : **ce fichier** ; toute évolution de périmètre Cash (nouveau module, nouveau menu) met à jour ce document en priorité, puis les README concernés.

---

## Références utiles

- `dorevia_cash_flow/README.md` — parcours V1.1, menu nominal.
- `dorevia_cash_flow/docs/SPEC_CASH_FLOW_TRAJECTORY.md` — § 5.5 résolution de référence.
- `dorevia_cash_flow/docs/TICKET_CASH_FLOW_V1_1_TRAJECTOIRE_REFERENCE.md` — cadrage ticket V1.1.
- `dorevia_cash_guard/README.md` — atelier de projection.
- `dorevia_cash_guard/docs/TICKET_CASH_GUARD_HOME_REFERENCE_TRAJECTORY.md` — accueil Cash Guard centré sur la trajectoire de référence (lecture seule, réutilisation Cash Flow).
- `dorevia_cash_simulation/README.md` — hypothèses devis / extension Cash Guard.
