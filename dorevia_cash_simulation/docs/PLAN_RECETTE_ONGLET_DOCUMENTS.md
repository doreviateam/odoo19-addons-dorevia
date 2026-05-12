# Plan de recette fonctionnelle — Onglet Documents et intégration des simulations

## 0. Objectif

Valider que l'onglet `Facturation` est renommé `Documents`, qu'il affiche une liste unifiée des documents expliquant la projection (factures réelles + documents simulés retenus), et que la distinction visuelle (type, couleur, impact) est conforme au ticket.

Référence : `docs/TICKET_ONGLET_DOCUMENTS.md`

---

## 1. Préconditions

Sur `tenant_o8` :

```text
Module dorevia_cash_guard mis à jour
Module dorevia_cash_simulation mis à jour
Module dorevia_cash_simulation_purchase mis à jour
Tests automatisés OK
Utilisateur avec droits Cash Guard
Au moins une projection Cash Guard avec des factures ouvertes
Devise société = EUR
```

Créer ou identifier une projection Cash Guard de test avec :

```text
Au moins 1 facture client ouverte (out_invoice)
Au moins 1 facture fournisseur ouverte (in_invoice)
```

Préparer :

```text
D1 = Devis client brouillon, validity_date dans la période, montant 1 000 €
D2 = Devis client envoyé, validity_date dans la période, montant 2 000 €
D3 = Devis client brouillon, validity_date HORS période, montant 3 000 €
P1 = Commande achat brouillon, date_planned dans la période, montant 500 €
P2 = Commande achat brouillon, date_planned dans la période, montant 1 500 € (utilisé pour confirmation au test 7 du plan V1.0.1 — ne pas réutiliser après confirmation)
P3 = Commande achat brouillon, date_planned dans la période, montant 1 500 € (jeu frais pour le test 10)
```

---

## 2. Test 1 — Renommage de l'onglet

### Action

Ouvrir une projection Cash Guard en mode formulaire.

### Résultat attendu

```text
L'onglet « Facturation » n'existe plus.
L'onglet « Documents » est présent.
Les trois onglets sont : Projection / Documents / Notes.
```

Statut : `OK / KO`

---

## 3. Test 2 — Mode simulation OFF : Documents = factures réelles uniquement

### Action

```text
Mode simulation = OFF (ou non activé)
Ouvrir l'onglet Documents
```

### Résultat attendu

```text
L'onglet Documents affiche les factures ouvertes uniquement.
Aucune ligne « Devis client simulé » ni « Commande achat simulée ».
La colonne Type affiche « Facture client » ou « Facture fournisseur ».
La colonne Statut affiche Confort / Vigilance / Tension / Risque.
Les couleurs sont appliquées selon le risque :
  Risque = rouge
  Tension = orange
  Vigilance = bleu
  Confort = vert
```

Statut : `OK / KO`

---

## 4. Test 3 — Mode simulation ON : Documents = factures + devis simulés

### Action

```text
Mode simulation = ON
Devis = D1, D2
Sauvegarder / Actualiser
Ouvrir l'onglet Documents
```

### Résultat attendu

```text
Les factures ouvertes sont toujours affichées.
2 nouvelles lignes « Devis client simulé » apparaissent (D1 et D2).
```

Pour chaque ligne simulée (D1 et D2) :

| Champ | Valeur attendue |
| ----- | --------------- |
| Statut | Simulation |
| Période | correspond à la maille contenant validity_date |
| Document | numéro du devis (ex. S00xxx) |
| Partenaire | client du devis |
| Type | Devis client simulé |
| Échéance | validity_date du devis |
| Retard | vide |
| Impact | + montant TTC (D1 = +1 000 €, D2 = +2 000 €) |
| Échue | Non |
| Lien | bouton ouvrant le devis |

Statut : `OK / KO`

---

## 5. Test 4 — Mode simulation ON : Documents = factures + achats simulés

### Action

```text
Mode simulation = ON
Devis = D1
Commandes achat = P1
Sauvegarder / Actualiser
Ouvrir l'onglet Documents
```

### Résultat attendu

```text
Les factures ouvertes sont affichées.
1 ligne « Devis client simulé » (D1).
1 ligne « Commande achat simulée » (P1).
```

Pour P1 :

| Champ | Valeur attendue |
| ----- | --------------- |
| Statut | Simulation |
| Période | correspond à la maille contenant date_planned |
| Document | numéro de la commande (ex. P00xxx) |
| Partenaire | fournisseur |
| Type | Commande achat simulée |
| Échéance | date_planned (date) |
| Retard | vide |
| Impact | −500 € (négatif = décaissement) |
| Échue | Non |
| Lien | bouton ouvrant la commande achat |

Statut : `OK / KO`

---

## 6. Test 5 — Couleur neutre des documents simulés

### Action

Observer les lignes simulées dans l'onglet Documents.

### Résultat attendu

```text
Les lignes simulées (Devis client simulé, Commande achat simulée)
sont affichées en couleur neutre (noir / anthracite).
Elles ne sont PAS colorées en rouge, orange, bleu ou vert.
Les factures réelles conservent leur couleur de risque.
```

Vérifier visuellement que la distinction est claire.

**Capture visuelle requise** : réaliser une capture d'écran de l'onglet `Documents` en mode simulation ON avec au moins une facture réelle, un devis client simulé et une commande achat simulée visibles simultanément. Joindre la capture au PV de recette.

Statut : `OK / KO`

---

## 7. Test 6 — Devis non éligible exclu de Documents

### Action

```text
Mode simulation = ON
Devis = D1, D3 (D3 hors période)
Sauvegarder / Actualiser
Ouvrir l'onglet Documents
```

### Résultat attendu

```text
D1 apparaît dans l'onglet Documents (éligible).
D3 n'apparaît PAS dans l'onglet Documents (hors période = non retenu).
Seuls les documents retenus dans le calcul sont affichés.
```

Statut : `OK / KO`

---

## 8. Test 7 — Lien d'ouverture des documents

### Action

Dans l'onglet Documents, cliquer sur le bouton lien (icône externe) pour :

1. Une facture client réelle
2. Un devis client simulé
3. Une commande achat simulée

### Résultat attendu

```text
Facture : ouvre le formulaire de la facture (account.move)
Devis : ouvre le formulaire du devis (sale.order)
Commande achat : ouvre le formulaire de la commande (purchase.order)
Les trois ouvertures fonctionnent sans erreur.
```

Statut : `OK / KO`

---

## 9. Test 8 — Réinitialiser

### Action

Depuis une projection avec simulation ON et des documents sélectionnés :

```text
Cliquer sur « Réinitialiser »
```

### Résultat attendu

```text
date_from = date du jour
Mode simulation = OFF
Devis simulés = vidés
Commandes achat simulées = vidées
Projection recalculée sans hypothèses
L'onglet Documents n'affiche que les factures réelles.
```

Statut : `OK / KO`

---

## 10. Test 9 — Aucun effet comptable des simulations

### Action

Vérifier après l'ensemble des tests.

### Résultat attendu

```text
Aucune facture créée par les simulations.
Aucune écriture comptable créée.
Aucun paiement créé.
Aucun mouvement bancaire créé.
Les devis et commandes achat source restent inchangés.
```

Statut : `OK / KO`

---

## 11. Test 10 — Cohérence impacts et signes

### Action

Réinitialiser le jeu de données simulation (ou utiliser des documents frais).

```text
Mode simulation = ON
Devis = D1 (1 000 €), D2 (2 000 €)
Commandes achat = P1 (500 €), P3 (1 500 €)
Sauvegarder / Actualiser
Vérifier l'onglet Documents
```

### Résultat attendu

```text
D1 : Impact = +1 000 €
D2 : Impact = +2 000 €
P1 : Impact = −500 €
P3 : Impact = −1 500 €
Si un total de colonne Impact est affiché, il inclut factures + simulations.
Le solde projeté global reflète bien l'impact net des simulations.
```

Statut : `OK / KO`

---

## Grille de décision

| Zone testée | Attendu | Statut |
| ----------- | ------- | ------ |
| Tests automatiques | Tous verts (base + simulation + purchase) | OK / KO |
| Renommage onglet | Facturation → Documents | OK / KO |
| Simulation OFF | Documents = factures réelles uniquement | OK / KO |
| Simulation ON + devis | Devis simulés affichés, type correct | OK / KO |
| Simulation ON + achats | Achats simulés affichés, type correct | OK / KO |
| Couleur neutre simulations | Pas de coloration risque sur les simulations | OK / KO |
| Devis non éligible | Exclu de Documents | OK / KO |
| Liens d'ouverture | Facture, devis, commande achat s'ouvrent | OK / KO |
| Réinitialiser | Simulation OFF, documents vidés, projection prudente | OK / KO |
| Aucun effet comptable | Aucun flux réel créé | OK / KO |
| Cohérence impacts | Signes +/− corrects, somme cohérente | OK / KO |

---

## Conclusion attendue

La recette est **GO** si :

```text
L'onglet Facturation est renommé Documents.
En mode simulation OFF, seules les factures réelles sont affichées.
En mode simulation ON, les documents simulés retenus apparaissent.
Les types sont clairement distincts (Devis client simulé / Commande achat simulée).
Les documents simulés sont en couleur neutre (pas de coloration risque).
Les impacts sont correctement signés (+/−).
Les échéances utilisent validity_date (ventes) et date_planned (achats).
Les liens d'ouverture fonctionnent.
Réinitialiser remet la projection en mode prudent.
Aucune facture, écriture comptable ou paiement n'est créé.
```

Limite maintenue :

```text
Les simulations impactent projected_balance et risk_status,
pas encore inflow_amount / outflow_amount.
Pas de conversion multi-devise.
Pas d'éclatement selon conditions de paiement.
```
