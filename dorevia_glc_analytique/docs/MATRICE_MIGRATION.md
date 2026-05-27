# Matrice de migration analytique — GLC

**Projet :** Suivi d'activité GLC  
**Version :** V1.1  
**Statut :** Document de travail — **à valider en Phase 0**  
**Référence :** [Spécification V1](./README.md) — section 12.1

---

## 1. Contexte

GLC dispose aujourd'hui d'un plan analytique comportant **9 comptes**. Le plan cible en compte **11** (7 Activités + 4 Financements) répartis sur **2 plans analytiques Odoo 19**.

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

## 3. Matrice de correspondance

> **Important :** seul le compte `RH_PERSONNEL` est identifié avec certitude dans la spec initiale. Les 8 autres comptes ci-dessous sont des **hypothèses de travail** à confirmer avec le gestionnaire et le trésorier lors de la Phase 0. Adapter les lignes marquées « À valider ».

| # | Ancien compte (plan actuel) | Solde type | Nouveau plan | Nouveau compte | Règle de migration |
|---|---|---|---|---|---|
| 1 | `RH_PERSONNEL` | Charge (~−20 608 € cumulé) | — | Ventilation salariale | **Ne pas migrer en solde analytique.** Traiter via ventilation mensuelle à partir du mois de bascule. |
| 2 | *Compte bar / restauration* (À valider) | Mixte | Activités | `BAR` | Reclasser les écritures ou laisser en lecture seule selon date |
| 3 | *Compte prestations / animations* (À valider) | Mixte | Activités | `PRESTATIONS` | Idem |
| 4 | *Compte résidences* (À valider) | Charge | Activités | `RESIDENCES` | Idem |
| 5 | *Compte missions / déplacements* (À valider) | Charge | Activités | `MISSIONS` | Idem |
| 6 | *Compte privatisation* (À valider) | Mixte | Activités | `PRIVATISATIONS` | Idem |
| 7 | *Compte location Radio* (À valider) | Recette | Activités | `LOCATION_RADIO` | Idem |
| 8 | *Compte structure / admin* (À valider) | Charge | Activités | `STRUCTURE` | Idem |
| 9 | *Compte financements / subventions* (À valider) | Recette | Financements | `SUBVENTIONS` ou `ADHESIONS` / `DONS` | Ventiler selon nature réelle |

### Comptes Financements à créer (nouveau plan)

Les comptes `ADHESIONS`, `DONS`, `SUBVENTIONS` et `RESSOURCES_PROPRES` n'existent probablement pas dans le plan actuel. Leur alimentation repose sur :

- le reclassement des recettes existantes mal qualifiées ;
- la double affectation des nouvelles pièces à partir de la date de bascule.

---

## 4. Traitement spécifique — `RH_PERSONNEL`

### Problème

Le compte `RH_PERSONNEL` concentre environ **−20 608 €** sans ventilation par activité. Il masque la consommation salariale réelle de chaque activité.

### Décision V1

1. **Désactiver** le compte `RH_PERSONNEL` dans le plan Activités cible (cf. règle 8.1).
2. **Ne pas reclassement** les écritures salariales historiques vers les 7 activités en V1.
3. À partir du mois de bascule, alimenter le pilotage via **ventilation salariale mensuelle** (modèle `glc.salary.allocation`).
4. Produire une **première ventilation rétrospective** sur le mois pilote pour calibrer les clés (optionnel, non officiel).

### Contrôle post-migration

```text
Total coûts salariaux ventilés du mois
≈ Masse salariale comptable du mois (631/641…)
Écart > 5 % → alerte
```

---

## 5. Checklist Phase 0

- [ ] Inventorier les 9 comptes analytiques actuels (codes exacts, libellés, soldes)
- [ ] Valider la matrice ligne par ligne avec le gestionnaire
- [ ] Trancher le traitement des écritures antérieures à la date de bascule
- [ ] Définir la date de bascule et le mois pilote
- [ ] Préparer la première ventilation salariale
- [ ] Produire un rapport test et comparer avec l'ancienne lecture
- [ ] Documenter les écarts (écritures mal affectées, trop générales)

---

## 6. Livrables Phase 0

| Livrable | Responsable | Statut |
|---|---|---|
| Liste des 9 comptes actuels (export Odoo) | Gestionnaire | ☐ |
| Matrice validée (ce document complété) | AMOA + Gestionnaire | ☐ |
| Procédure de saisie analytique | Gestionnaire | ☐ |
| Modèle de rapport CA | AMOA | ☐ |
| Calendrier de bascule | Bureau / CA | ☐ |

---

## 7. Risques identifiés

| Risque | Impact | Mitigation |
|---|---|---|
| Écritures historiques mal affectées | Rapport incohérent | Documenter les écarts, ne pas masquer |
| `STRUCTURE` fourre-tout | Poids structure artificiel | Règles d'affectation + alerte seuil |
| Financements non qualifiés sur recettes existantes | Synthèse financements incomplète | Double affectation progressive à partir de la bascule |
| Ventilation salariale arbitraire | Coût complet non fiable | Validation mensuelle + contrôle vs paie comptable |
