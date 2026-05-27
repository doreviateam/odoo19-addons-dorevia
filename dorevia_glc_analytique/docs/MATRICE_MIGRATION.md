# Matrice de migration analytique — GLC

**Projet :** Suivi d'activité GLC  
**Version :** V1.1  
**Statut :** Document de travail — **à valider en Phase 0**  
**Référence :** [Spécification V1](./README.md) — section 12.1

---

## 1. Contexte

GLC dispose aujourd'hui d'un plan analytique comportant **9 comptes**. Le plan cible en compte **11** (7 Activités + 4 Financements) répartis sur **2 plans analytiques Odoo 19**.

Inventaire Phase 0 extrait de la base **`glc-rgl-test-import`** le **27/05/2026** :

- source comptes : `account.analytic.account`, hors comptes créés par le module `dorevia_glc_analytique` ;
- source soldes : agrégat `account.analytic.line.amount` par compte analytique ;
- résultat : **0 ligne analytique trouvée** sur les 9 comptes historiques, donc soldes analytiques extraits à `0,00`.

> **Périmètre de l'inventaire :** base de **recette / import** (`glc-rgl-test-import`).  
> Les codes, soldes et correspondances ci-dessous sont une **première photographie** à **confirmer ultérieurement** sur la **base de production GLC** ou la **base source finale** retenue pour la bascule (notamment le solde `RH_PERSONNEL` et la présence de lignes analytiques historiques).

Ce document formalise la correspondance **ancien → nouveau** et les règles de traitement des soldes historiques.

---

## 2. Paramètres de bascule

| Paramètre | Valeur | Statut |
|---|---|---|
| Date de bascule cible | *À définir en Phase 0* | ☐ |
| Premier mois pilote (sans rapport CA officiel) | *À définir* | ☐ |
| Premier rapport CA officiel | *À définir* | ☐ |
| Traitement historique antérieur | Lecture seule sur ancien plan | ☐ Validé |
| Reclassement rétroactif des écritures | Non en V1 (sauf correction d'erreurs documentées) | ☐ Validé |

---

## 3. Inventaire des comptes analytiques existants avant migration GLC

Extraction réalisée après installation du Palier 0 sur la base de recette **`glc-rgl-test-import`**. Les comptes cibles GLC créés par le module sont exclus de ce tableau. **À rejouer sur base prod / source finale avant gel Phase 0.**

| Code | Nom | Plan analytique | Statut | Société | Solde analytique extrait | Lignes analytiques |
|---|---|---|---|---|---:|---:|
| `ADHESION_GLC` | Adhésions | Activités GLC | Actif | My Company | 0,00 | 0 |
| `BAR_RESTAU` | Bar & Restau | Activités GLC | Actif | My Company | 0,00 | 0 |
| `DEPLACEMENT_MISSION` | Déplacement & Mission | Activités GLC | Actif | My Company | 0,00 | 0 |
| `ESPACE_GLC` | Privatisation Espace | Activités GLC | Actif | My Company | 0,00 | 0 |
| `FRAIS_STRUCTURE` | Frais généraux | Activités GLC | Actif | My Company | 0,00 | 0 |
| `PRESTA_GLC` | Prestation & Animation | Activités GLC | Actif | My Company | 0,00 | 0 |
| `RESIDENCE_GLC` | Résidence artiste | Activités GLC | Actif | My Company | 0,00 | 0 |
| `RH_PERSONNEL` | RH / Personnel | Activités GLC | Actif | My Company | 0,00 | 0 |
| `SUBVENTION_GLC` | Subvention d'exploitation | Activités GLC | Actif | My Company | 0,00 | 0 |

> Point d'attention : l'ancienne note de cadrage mentionnait un solde cumulé d'environ `-20 608 €` sur `RH_PERSONNEL`. Ce solde n'apparaît pas dans la base `glc-rgl-test-import` via `account.analytic.line.amount` au 27/05/2026. À confirmer avec le gestionnaire : autre base source, période filtrée, écritures non importées, ou solde issu d'un export externe.

---

## 4. Matrice de correspondance

> **Important :** les 9 codes ci-dessous sont extraits de `glc-rgl-test-import`. La correspondance métier reste à valider avec le gestionnaire et le trésorier lors de la Phase 0, notamment les regroupements recettes/financements.

| # | Ancien compte (plan actuel) | Solde type | Nouveau plan | Nouveau compte | Règle de migration |
|---|---|---|---|---|---|
| 1 | `RH_PERSONNEL` — RH / Personnel | Charge salariale | — | Ventilation salariale | **Ne pas migrer en solde analytique.** Traiter via ventilation mensuelle à partir du mois de bascule. Solde source à confirmer car extraction recette = `0,00`. |
| 2 | `BAR_RESTAU` — Bar & Restau | Mixte | Activités | `BAR` | Reclasser les nouvelles écritures vers `BAR`. Historique à laisser en lecture seule sauf correction documentée. |
| 3 | `PRESTA_GLC` — Prestation & Animation | Mixte | Activités | `PRESTATIONS` | Reclasser les nouvelles écritures vers `PRESTATIONS`. Historique à laisser en lecture seule sauf correction documentée. |
| 4 | `RESIDENCE_GLC` — Résidence artiste | Charge subventionnée | Activités | `RESIDENCES` | Reclasser les nouvelles écritures vers `RESIDENCES`. Historique à laisser en lecture seule sauf correction documentée. |
| 5 | `DEPLACEMENT_MISSION` — Déplacement & Mission | Charge | Activités | `MISSIONS` | Reclasser les nouvelles écritures vers `MISSIONS`. Historique à laisser en lecture seule sauf correction documentée. |
| 6 | `ESPACE_GLC` — Privatisation Espace | Mixte | Activités | `PRIVATISATIONS` | Reclasser les nouvelles écritures vers `PRIVATISATIONS`. Historique à laisser en lecture seule sauf correction documentée. |
| 7 | *Aucun compte source dédié identifié* | Recette | Activités | `LOCATION_RADIO` | Nouveau compte cible à alimenter à partir de la bascule. Vérifier si des écritures historiques sont dans `FRAIS_STRUCTURE`, `PRESTA_GLC` ou `ESPACE_GLC`. |
| 8 | `FRAIS_STRUCTURE` — Frais généraux | Charge | Activités | `STRUCTURE` | Reclasser les nouvelles écritures vers `STRUCTURE`. Surveiller le risque de compte fourre-tout. |
| 9 | `SUBVENTION_GLC` — Subvention d'exploitation | Recette / financement | Financements | `SUBVENTIONS` | Reclasser les nouvelles écritures vers `SUBVENTIONS`. Historique à laisser en lecture seule sauf correction documentée. |
| 10 | `ADHESION_GLC` — Adhésions | Recette / financement | Financements | `ADHESIONS` | Reclasser les nouvelles écritures vers `ADHESIONS`. Historique à laisser en lecture seule sauf correction documentée. |
| 11 | *Aucun compte source dédié identifié* | Recette / financement | Financements | `DONS` | Nouveau compte cible à alimenter à partir de la bascule. Vérifier si les dons historiques sont mélangés dans `ADHESION_GLC` ou `SUBVENTION_GLC`. |
| 12 | *Aucun compte source dédié identifié* | Recette / financement | Financements | `RESSOURCES_PROPRES` | Nouveau compte cible à alimenter par double affectation des recettes propres à partir de la bascule. |

### Comptes Financements cibles (nouveau plan)

Les comptes `ADHESIONS`, `DONS`, `SUBVENTIONS` et `RESSOURCES_PROPRES` existent dans le plan cible Palier 0. Ils n'existent pas tous dans le plan actuel. Leur alimentation repose sur :

- le reclassement des recettes existantes mal qualifiées ;
- la double affectation des nouvelles pièces à partir de la date de bascule.

---

## 5. Traitement spécifique — `RH_PERSONNEL`

### Problème

La spec initiale indique que le compte `RH_PERSONNEL` concentre environ **−20 608 €** sans ventilation par activité. L'extraction réalisée sur `glc-rgl-test-import` ne retrouve toutefois **aucune ligne analytique** sur ce compte et donne un solde analytique disponible de `0,00`.

Cette divergence doit être clarifiée en Phase 0 avant ouverture du Palier 1 : base source différente, écritures non importées, période d'analyse, ou solde issu d'un export hors `account.analytic.line`.

### Décision V1

1. **Désactiver** le compte `RH_PERSONNEL` dans le plan Activités cible (cf. règle 8.1).
2. **Ne pas reclasser** les écritures salariales historiques vers les 7 activités en V1.
3. À partir du mois de bascule, alimenter le pilotage via **ventilation salariale mensuelle** (modèle `glc.salary.allocation`).
4. Produire une **première ventilation rétrospective** sur le mois pilote pour calibrer les clés (optionnel, non officiel).

### Contrôle post-migration

```text
Total coûts salariaux ventilés du mois
≈ Masse salariale comptable du mois (631/641…)
Écart > 5 % → alerte
```

---

## 6. Checklist Phase 0

- [x] Inventorier les 9 comptes analytiques actuels (codes exacts, libellés, soldes) — *recette `glc-rgl-test-import`*
- [ ] **Rejouer l'inventaire sur base de production ou base source finale**
- [ ] Valider la matrice ligne par ligne avec le gestionnaire
- [ ] Trancher le traitement des écritures antérieures à la date de bascule
- [ ] Définir la date de bascule et le mois pilote
- [ ] Préparer la première ventilation salariale
- [ ] Produire un rapport test et comparer avec l'ancienne lecture
- [ ] Documenter les écarts (écritures mal affectées, trop générales)

---

## 7. Livrables Phase 0

| Livrable | Responsable | Statut |
|---|---|---|
| Liste des 9 comptes actuels (export Odoo) | AMOA | ☑ Extrait de `glc-rgl-test-import` le 27/05/2026 |
| Matrice validée (ce document complété) | AMOA + Gestionnaire | ☐ |
| Procédure de saisie analytique | Gestionnaire | ☐ |
| Modèle de rapport CA | AMOA | ☐ |
| Calendrier de bascule | Bureau / CA | ☐ |

---

## 8. Risques identifiés

| Risque | Impact | Mitigation |
|---|---|---|
| Écritures historiques mal affectées | Rapport incohérent | Documenter les écarts, ne pas masquer |
| `STRUCTURE` fourre-tout | Poids structure artificiel | Règles d'affectation + alerte seuil |
| Financements non qualifiés sur recettes existantes | Synthèse financements incomplète | Double affectation progressive à partir de la bascule |
| Ventilation salariale arbitraire | Coût complet non fiable | Validation mensuelle + contrôle vs paie comptable |
