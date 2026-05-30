# Règles d'affectation analytique — GLC

> **Implémentation actuelle :** plan **unique** GLC (11 axes) — voir [ETAT_NOMENCLATURE_ANALYTIQUE.md](./ETAT_NOMENCLATURE_ANALYTIQUE.md) et [ETAT_MODULE_ACTUEL.md](./ETAT_MODULE_ACTUEL.md). La ventilation salariale overlay (Palier 2) n'est **plus** dans le produit ; les écritures de paie suivent la comptabilité analytique standard.

**Projet :** Suivi d'activité GLC  
**Version :** V1.1  
**Statut :** Annexe obligatoire à la spécification fonctionnelle  
**Référence :** [Spécification V1](./README.md) — sections 4, 6 et 8

---

## 1. Principe

GLC utilise **deux plans analytiques Odoo 19** :

1. **Plan Activités** — *Que consomme et que produit chaque activité ?*
2. **Plan Financements** — *D'où viennent les ressources ?*

Les règles ci-dessous définissent, pour chaque type de pièce comptable, quels axes sont **obligatoires**, **interdits** ou **optionnels**.

> Le plan Financements ne doit pas devenir un second plan d'activité. Il qualifie la nature des ressources, pas les opérations.

---

## 2. Matrice d'affectation par type de pièce

| Type de pièce | Plan Activités | Plan Financements | Exemple |
|---|---|---|---|
| Facture fournisseur | **Obligatoire** | Interdit en V1 | Achats bar → `BAR` |
| Facture client (hors subvention) | **Obligatoire** | **Obligatoire** | Vente bar → `BAR` + `RESSOURCES_PROPRES` |
| Point de vente (POS) | **Obligatoire** | **Obligatoire** | Vente boisson → `BAR` + `RESSOURCES_PROPRES` |
| Billetterie / événement | **Obligatoire** | **Obligatoire** | Billetterie conte → `PRESTATIONS` + `RESSOURCES_PROPRES` |
| Privatisation facturée | **Obligatoire** | **Obligatoire** | Location jardin → `PRIVATISATIONS` + `RESSOURCES_PROPRES` |
| Loyer Radio Grand Lieu | **Obligatoire** | **Obligatoire** | Loyer mensuel → `LOCATION_RADIO` + `RESSOURCES_PROPRES` |
| Subvention perçue | Optionnel (projet) | **Obligatoire** | Subvention résidence → `RESIDENCES` + `SUBVENTIONS` |
| Adhésion | Interdit | **Obligatoire** | Cotisation → `ADHESIONS` |
| Don | Interdit | **Obligatoire** | Don ponctuel → `DONS` |
| Écriture de paie (631/641…) | **Obligatoire** sur axe activité | Interdit | Analytique comptable — source **Cumul RH** du Contrôle de gestion |
| Note de frais / remboursement mission | **Obligatoire** | Interdit | IK mission → `MISSIONS` |
| Écriture bancaire sans facture | Selon nature | Selon nature | À affecter manuellement avant clôture |

### Règle subventions affectées

Lorsqu'une subvention est **affectée à un projet identifiable** (ex. résidence artistique), la ligne de produit doit porter **les deux axes** :

- Plan Activités → compte du projet (`RESIDENCES`, etc.)
- Plan Financements → `SUBVENTIONS`

Cela permet le rapprochement *financement / consommation* dans le rapport mensuel.

---

## 3. Règles Radio Grand Lieu / Bar

| Nature de l'opération | Plan Activités | Plan Financements | Remarque |
|---|---|---|---|
| Loyer mensuel Radio | `LOCATION_RADIO` | `RESSOURCES_PROPRES` | Montant de référence paramétré (contrat locatif) |
| Consommations bar/cuisine Radio | `BAR` | `RESSOURCES_PROPRES` | Distinct du loyer |
| Refacturation charges communes à Radio | `LOCATION_RADIO` | `RESSOURCES_PROPRES` | Si facturée à Radio |
| Charges communes non refacturables | `STRUCTURE` | — | Électricité, entretien global du site |

---

## 4. Règles STRUCTURE et charges indirectes

### V1 — Pas de répartition automatique

- Toute charge **non identifiable** à une activité opérationnelle → `STRUCTURE`.
- Pas de clé de répartition structure → activités en V1 (évolution V3).

### Critères d'affectation

| Charge | Activité cible |
|---|---|
| Logiciel, assurance, frais bancaires, gouvernance | `STRUCTURE` |
| Achat boissons pour le bar | `BAR` |
| Cachet artiste pour un spectacle | `PRESTATIONS` |
| Hébergement artiste en résidence | `RESIDENCES` |
| Frais kilométriques mission extérieure | `MISSIONS` |
| Location ponctuelle du lieu | `PRIVATISATIONS` |

### Alerte

Si le poids de `STRUCTURE` dépasse le seuil paramétré (% des charges totales), le rapport mensuel doit signaler un **point d'attention** (risque de fourre-tout).

---

## 5. Modèles de distribution par défaut (Odoo 19)

> **Palier 0 :** les plans GLC sont installés avec applicabilité `optional` — pas de blocage à la validation des pièces.  
> **Palier 1 :** rapport d'anomalies ([TICKET_PALIER_1.md](./TICKET_PALIER_1.md)) — diagnostic non bloquant.  
> **Post-Palier 1 :** passage en `mandatory` selon la matrice ci-dessous + validation MOA explicite.

À paramétrer en Phase 1 sur les journaux comptables :

| Journal / source | Distribution Activités par défaut | Distribution Financements par défaut |
|---|---|---|
| Achats | Aucune (saisie obligatoire) | — |
| Ventes | Selon modèle produit | `RESSOURCES_PROPRES` |
| POS bar | `BAR` | `RESSOURCES_PROPRES` |
| Banque (recettes HelloAsso adhésions) | — | `ADHESIONS` |
| Banque (recettes HelloAsso dons) | — | `DONS` |

Les modèles accélèrent la saisie ; le gestionnaire reste responsable du contrôle mensuel.

---

## 6. Contrôles avant clôture analytique

1. Toute facture fournisseur du mois possède une affectation Plan Activités.
2. Toute recette d'activité possède les deux axes (Activités + Financements).
3. Aucune écriture de paie ne porte d'analytique salaire (`RH_PERSONNEL` interdit).
4. Les pièces sans analytique obligatoire sont listées dans le rapport « anomalies du mois ».

---

## 7. Correspondance terminologique

| Terme métier | Terme Odoo | Terme rapport |
|---|---|---|
| Activité | Compte analytique (plan Activités) | Activité |
| Financement | Compte analytique (plan Financements) | Source de financement |
| Affectation | `analytic_distribution` | — |
| Solde brut | — | Produits − charges directes |
| Solde de gestion | — | Solde brut − salaires ventilés |
| Solde complet | — | Solde de gestion − valorisation bénévolat |
