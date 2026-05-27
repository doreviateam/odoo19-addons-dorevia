# Ticket de cadrage — Cockpit GLC · Onglet 1 « Synthèse graphique »

**Module :** `dorevia_glc_analytics`  
**Branche :** `feat/glc-cockpit-synthese-graphique`  
**Version cible :** `19.0.4.6.1` (implémentation + wording MOA Marge d'activité)  
**Statut :** **Cadrage MOA — GO global** (2026-05-27) — **wording Marge d'activité acté `19.0.4.6.1`**  
**Prérequis :** vue **Détail par activité** validée comme cible UX (`19.0.4.5.3`, PR #35 mergée)

**Références :** [TICKET_UX_GROUP_BY_DETAIL_COCKPIT.md](./TICKET_UX_GROUP_BY_DETAIL_COCKPIT.md) · [recette période libre](./recette/RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md) · [TICKET_PALIER_4BIS.md](./TICKET_PALIER_4BIS.md)

> **Note de lecture :** ce ticket fige le cadrage MOA du nouvel onglet de synthèse graphique. Aucun code n'est livré avant validation MOA des sections 4 (contenu), 5 (doctrine), 6 (cible UX) et 7 (implémentation).

---

## 1. Contexte MOA

Le palier **Détail par activité** est livré et validé (`19.0.4.5.3`) :

- 4 blocs métier : **RECETTES | SALAIRES | DÉPENSES | MARGE D'ACTIVITÉ** *(libellé MOA `19.0.4.6.1` ; bloc historiquement nommé « Performance »)* ;
- sous-totaux mensuels + total période ;
- séparation visuelle finalisée ; cible UX validée.

Cette vue répond à la **lecture détaillée et à la justification chiffrée**. Il reste à doter le cockpit GLC d'une **lecture immédiate de pilotage** : la **synthèse graphique**.

---

## 2. Objectif

Donner aux dirigeants une lecture instantanée du pilotage de l'activité, sans avoir besoin de descendre dans le détail chiffré, sur la même période et le même scénario budgétaire que les autres onglets.

> Est-ce que mon activité couvre ses charges sur la période ? Avec quelle tendance mensuelle ? Quelles activités tirent la marge d'activité ?

---

## 3. Cible de navigation cockpit

Nouvelle structure des onglets du cockpit GLC (ordre cible) :

```text
Synthèse graphique | Détail par activité | Ressources | Charges de structure | Infos
```

**Doctrine d'usage MOA :**

| Onglet | Rôle |
|---|---|
| **Synthèse graphique** | Lecture immédiate de pilotage — onglet par défaut |
| **Détail par activité** | Lecture détaillée et justification chiffrée |
| Ressources | Ressources disponibles (recettes + financements) |
| Charges de structure | Couverture salaires / dépenses |
| Infos | Métadonnées cockpit |

---

## 4. Contenu cible proposé MOA

### 4.1. Bandeau KPI de tête

4 cartes synthétiques, sur la période choisie :

| KPI (libellé UI) | Source | Format |
|---|---|---|
| **Marge réelle** | Σ `performance_realized` des lignes activité | Monétaire (couleur vert/rouge selon signe) |
| **Marge budget** | Σ `performance_budget` des lignes activité | Monétaire (neutre) |
| **Écart de marge** | `performance_realized − performance_budget` | Monétaire (couleur vert/rouge) |
| **Couverture des salaires** | **`Recettes réelles / Salaires réels × 100`** sur la période | Pourcentage (seuils MOA : vert ≥ 100 %, orange 80–100 %, rouge < 80 %) |

> **Wording MOA `19.0.4.6.1` :** les libellés UI s'appuient sur **Marge d'activité** (ou **Marge** selon la place). Les **noms techniques** des champs sont conservés (`performance_realized`, `performance_budget`, `variance_performance`).

**Affichage :**
- zéros monétaires → `—` (cohérent avec la doctrine widget Détail) ;
- **Taux de couverture des salaires :** affichage `—` si `salaires_realized == 0` (pas de division par zéro, pas de carte colorée).

### 4.2. Graphique principal — Marge d'activité mensuelle

- **Type :** barres groupées (mois × {Réel, Budget})
- **Axes :** X = mois (`month_label`) · Y = montant marge d'activité
- **Couleurs :** réel `#198754` (vert sobre), budget gris neutre
- **Source :** `performance_realized` / `performance_budget` agrégés par mois sur les lignes activité

### 4.3. Graphique de structure mensuelle

- **Type :** barres groupées par mois — décomposition **Recettes / Salaires / Dépenses**
- **Convention de signe MOA :** **salaires et dépenses sont affichés en valeurs positives de consommation** (et **non en négatif comptable**). Lecture homogène avec les recettes sur le même axe Y. Le caractère « consommé » est porté par la position dans la légende et la couleur, pas par le signe.
- **Source :** `revenue_realized`, `payroll_realized`, `expense_realized` agrégés par mois (`Math.abs(...)` à l'affichage pour garantir la convention)

### 4.4. Graphique par activité

- **Type :** barres horizontales — **marge réelle cumulée** sur la période, **une barre par activité**
- **Tri :** décroissant marge réelle
- **Couleurs :** vert si positive, rouge si négative
- **Source :** Σ `performance_realized` par `activity_label` (group by activity côté client)

### 4.5. Principes UX

- **3 à 4 visuels maximum** dans l'onglet — pas plus ;
- typographie et palette **cohérentes avec le widget Détail par activité** ;
- aucun lien externe ni drill-down ; les exports/details restent dans les autres onglets ;
- aucune duplication du tableau chiffré.

---

## 5. Doctrine métier (rappel et engagement MOA)

| Bloc (libellé UI) | Définition métier |
|---|---|
| **Recettes** | Recettes d'activité du périmètre cockpit (axes Activités) |
| **Salaires** | Masse salariale — **ressource humaine mobilisée**, séparée des dépenses *(libellé conservé tel quel par décision MOA)* |
| **Dépenses** | **Dépenses hors salaires** (frais généraux, charges de structure non RH) |
| **Marge d'activité** | Indicateur de synthèse : `Recettes − Salaires − Dépenses hors salaires` *(libellé MOA `19.0.4.6.1` ; ex « Performance »)* |

La synthèse graphique respecte cette grammaire **sans la réinterpréter** : les salaires ne sont jamais fusionnés avec les dépenses dans les visuels.

---

## 6. Cible UX — maquette texte

```text
┌────────────────────────────────────────────────────────────────────┐
│ Filtres : période + scénario budgétaire (partagés avec les onglets)│
├────────────────────────────────────────────────────────────────────┤
│ Synthèse graphique │ Détail par activité │ Ressources │ Charges …  │
├────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────┐ │
│  │ Marge réelle │ │ Marge budget │ │ Écart marge  │ │ Couverture │ │
│  │   12 450 €   │ │   10 000 €   │ │  + 2 450 €   │ │  salaires  │ │
│  │              │ │              │ │              │ │   118 %    │ │
│  └──────────────┘ └──────────────┘ └──────────────┘ └────────────┘ │
│                                                                    │
│  Marge d'activité mensuelle (réel vs budget)                       │
│  ████ ▒▒▒▒  ████ ▒▒▒▒  ████ ▒▒▒▒  ████ ▒▒▒▒  ████ ▒▒▒▒             │
│   Jan       Fév        Mar        Avr        Mai                   │
│                                                                    │
│  Structure mensuelle (Recettes / Salaires / Dépenses)              │
│  ░░░ ▓▓▓ ▒▒  ░░░ ▓▓▓ ▒▒  …                                         │
│                                                                    │
│  Marge d'activité par activité (cumul période)                     │
│  [BAR] Bar, Restauration         ████████████████  + 9 800 €       │
│  [STRUCTURE] Structure & Admin   ███               + 2 650 €       │
└────────────────────────────────────────────────────────────────────┘
```

---

## 7. Choix d'implémentation — à arbitrer MOA

### 7.1. Option A — Vues `<graph>` natives Odoo

| Avantages | Inconvénients |
|---|---|
| Aucun JS custom ; courbes natives ; tri/group by Odoo standard | Difficile de combiner 4 KPI + 3 graphiques dans un même onglet sans dupliquer le cockpit ; rendu peu fidèle à la palette du widget Détail |

### 7.2. Option B — Composant OWL custom `glc_coverage_synthesis` (recommandée a priori)

| Avantages | Inconvénients |
|---|---|
| Cohérence visuelle directe avec le widget `glc_coverage_detail` ; contrôle complet de la mise en page (KPI cards + Chart.js) ; pas de page intermédiaire | Code JS/SCSS supplémentaire ; tests visuels manuels |

**Pile technique pressentie (Option B) :**
- Composant OWL `glc_coverage_synthesis` (lecture seule)
- Chart.js (déjà packagé avec Odoo 19, utilisé par `web/static/lib/Chart`)
- Données : `groupedData` calculées côté client à partir de `line_ids` (réutilise la mécanique du widget Détail — pas de duplication backend)

### 7.3. Option C — Mixte (KPI cards QWeb + 3 vues graph séparées)

| Avantages | Inconvénients |
|---|---|
| Moins de JS custom | Triple aller-retour serveur, UX moins fluide, palette hétérogène |

### 7.4. Recommandation technique MOA

**Option B** — cohérente avec l'arbitrage du palier Détail (composant OWL custom retenu).

À confirmer en validation MOA section 11.

---

## 8. Architecture envisagée (Option B)

| Couche | Détail |
|---|---|
| **Modèle** | Aucun champ nouveau attendu ; agrégations calculées côté client comme pour le widget Détail. Champs `performance_*` déjà existants sur `glc.coverage.cockpit.line` |
| **Vue** | Ajout d'une nouvelle `<page string="Synthèse graphique">` **placée en premier** dans la `<notebook>` ; `<field name="line_ids" widget="glc_coverage_synthesis" readonly="1"/>` |
| **Widget OWL** | `static/src/js/glc_coverage_synthesis_widget.esm.js` — réutilise la mécanique de `groupedData` (regroupement mois / activité) + KPI cards + 3 graphes Chart.js |
| **Template QWeb** | `static/src/xml/glc_coverage_synthesis_widget.xml` |
| **SCSS** | `static/src/scss/glc_coverage_synthesis_widget.scss` — palette alignée sur Détail (verts sobres, fond `#f8f9fa` Marge d'activité) |
| **Tests** | Pas de nouveaux tests Python attendus (pas de modèle modifié) ; tests existants doivent rester verts |

---

## 9. Hors périmètre

- Pas d'export PDF / Excel ad-hoc depuis l'onglet (resterait à cadrer en palier ultérieur si besoin) ;
- Pas de drill-down depuis les graphiques vers les lignes — l'utilisateur reste sur l'onglet Détail pour cela ;
- Pas de nouveau scénario budgétaire ni nouveau champ sur les lignes ;
- Pas de changement des formules Marge d'activité / Couverture salaires (formule inchangée — seul le wording UI évolue).

---

## 10. Tests / non-régression

| Type | Couverture |
|---|---|
| Tests Python existants | Doivent rester verts (67 post-tests) |
| Recette MOA | Ajout d'une section R13 dans la recette période libre — points de contrôle KPI / graphiques |
| Test visuel manuel | Conformité maquette texte section 6, palette cohérente avec Détail, seuils couleur couverture salaires |

---

## 11. Décisions MOA — verdict global GO (2026-05-27)

| Point à valider | Décision MOA |
|---|---|
| Ordre des onglets : **Synthèse graphique en premier** | **GO** |
| 4 KPI de tête (Marge réelle / Marge budget / Écart de marge / Couverture salaires) | **GO** |
| 3 graphiques (Marge d'activité mensuelle / Structure mensuelle / Marge d'activité par activité) | **GO** |
| Seuils couleur Couverture salaires (vert ≥ 100, orange 80–100, rouge < 80) | **GO** |
| Option technique **B (composant OWL custom + Chart.js)** | **GO** |
| Doctrine grammaire métier (Recettes / Salaires / Dépenses hors salaires / Marge d'activité) | **GO** |
| **Wording MOA `19.0.4.6.1`** : SALAIRES conservé, PERFORMANCE → MARGE D'ACTIVITÉ (formule inchangée) | **GO** |

**Précisions intégrées au cadrage (post-GO MOA) :**

1. **Taux de couverture des salaires** : formule explicite `Recettes réelles / Salaires réels × 100` ; affichage `—` si `salaires_realized == 0`.
2. **Graphique Structure mensuelle** : salaires et dépenses affichés en **valeurs positives de consommation**, **jamais en négatif comptable**.
3. **Wording MOA (`19.0.4.6.1`) :** bloc historiquement nommé **PERFORMANCE** désormais libellé **« Marge d'activité »** dans l'UI (ou **« Marge »** selon la place). Termes UI : KPI *Marge réelle / Marge budget / Écart de marge*. **Noms techniques conservés** (`performance_realized`, `performance_budget`, `variance_performance`, `o_glc_family_performance`, `computePerformanceAmounts`).

---

## 12. Trajectoire d'implémentation (post-validation MOA)

1. Création de la page `<page string="Synthèse graphique">` dans `glc_coverage_cockpit_views.xml` (placée en première position)
2. Implémentation du widget OWL `glc_coverage_synthesis` (KPI + 3 graphes)
3. SCSS aligné Détail (palette, séparation, fond Marge d'activité)
4. Ajout R13 dans `RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md`
5. Upgrade + restart + hard refresh recette MOA
6. Bump `19.0.4.6.0` (layout + Chart.js) puis `19.0.4.6.1` (wording MOA Marge d'activité)
7. Commit + PR `feat/glc-cockpit-synthese-graphique` → `main`

---

*Ticket de cadrage rédigé MOA — 2026-05-27.  
Verdict MOA : **GO global** — 2026-05-27.  
Wording **Marge d'activité** acté MOA — `19.0.4.6.1` — 2026-05-27.  
Suite logique du palier UX Détail par activité (`19.0.4.5.3`, PR #35 mergée).*
