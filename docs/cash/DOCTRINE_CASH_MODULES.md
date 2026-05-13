# Doctrine — modules Cash Dorevia

**Périmètre** : chaîne **Cash Guard** → **Cash Flow** → (éventuellement) **modules de simulation**  
**Dépôt** : `odoo19-addons-dorevia`  
**Statut** : doctrine produit — cohérence post **V1.1** `dorevia_cash_flow` (trajectoire de référence automatique)

---

## Formules de synthèse

> **Cash Flow affiche la trajectoire de référence.**  
> **Cash Guard prépare et contrôle les projections.**  
> **Les modules de simulation enrichissent les hypothèses.**

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
| **Fait** | Journaux suivis, date de situation, seuils, calcul des mailles, explication des tensions, recalcul à la demande, traçabilité des hypothèses intégrées au document de projection. |
| **Ne fait pas** | Remplacer la lecture synthétique « trajectoire de référence » réservée à Cash Flow ; ne doit pas être présenté comme le seul écran de « vision une courbe » si Cash Flow est installé. |

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

## Anti-doublons et responsabilités

| Risque | Doctrine |
|--------|----------|
| Deux « vérités » de trajectoire | Une seule **trajectoire de référence** : **Cash Flow**. Les autres écrans sont projection détaillée ou simulation. |
| Simulation = réalité | Libellés et aide en ligne doivent dire **hypothèse** ; les montants ne deviennent « réels » que via la chaîne comptable / Cash Guard selon les règles métier. |
| Cash Flow qui recalcule | Interdit : Cash Flow **lit** les mailles déjà produites ; le recalcul est côté **Cash Guard** (ou module source). |
| Cash Guard comme seul grand graphique | Acceptable pour le **détail** opérationnel ; la **synthèse** lecture référence est **Cash Flow** lorsque le module est déployé. |

**Chaîne de responsabilité** : qualité des mailles et des hypothèses → **Cash Guard** ; exactitude de la courbe et des repères affichés → **Cash Flow** (sur la base des données fournies) ; périmètre des scénarios → **modules de simulation** + règles documentées de chaque module.

---

## Règles UX (à aligner progressivement)

- **Trajectoire de trésorerie** = lecture de **référence** (menu Analyse / Reporting, pas l’atelier).
- **Projections de trésorerie** (Cash Guard) = **atelier** de travail, recalcul, audit.
- **Simulation** (ventes / achats / …) = **hypothèses** ; titres et menus doivent éviter « trajectoire officielle » en doublon de Cash Flow.
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
- `dorevia_cash_simulation/README.md` — hypothèses devis / extension Cash Guard.
