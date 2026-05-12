# Plan de recette fonctionnelle — V1.0.1 + V1.1 — Scénario porté par Cash Guard

## 0. Objectif

Valider que la simulation est désormais portée par la projection Cash Guard (et non par les devis), que les devis / achats sont sélectionnés explicitement, et que les règles d'éligibilité restent appliquées.

---

## 1. Préconditions

Sur `tenant_o8` :

```text
Module dorevia_cash_simulation mis à jour (V1.0.1)
Module dorevia_cash_simulation_purchase installé (V1.1)
Tests automatisés OK
Utilisateur avec droits Cash Guard
Au moins une projection Cash Guard disponible
Devise société = EUR
```

Créer ou identifier une projection Cash Guard de test.

Noter avant test :

```text
Solde projeté initial :
Risk status initial :
Mode simulation : OFF
Champ Devis : vide
Champ Commandes achat : vide
```

---

## 2. Jeu de données à créer

### Devis clients

| Réf. | État | validity_date | Montant TTC | Résultat attendu |
| ---- | ---- | ------------- | ----------: | ---------------- |
| D1 | Brouillon | Dans la période | 1 000 € | Éligible si sélectionné |
| D2 | Envoyé | Dans la période | 2 000 € | Éligible si sélectionné |
| D3 | Brouillon | Hors période | 3 000 € | Exclu (validity_date hors période) |
| D4 | Brouillon | Dans la période | 4 000 € | Éligible puis exclu après confirmation |

### Commandes achat

| Réf. | État | date_planned | Montant TTC | Résultat attendu |
| ---- | ---- | ------------ | ----------: | ---------------- |
| P1 | Brouillon | Dans la période | 500 € | Éligible si sélectionné (décaissement) |
| P2 | Brouillon | Dans la période | 1 500 € | Éligible puis exclu après confirmation |

---

## 3. Test 1 — Mode simulation OFF

### Action

Dans Cash Guard :

```text
Mode simulation = OFF
```

### Résultat attendu

```text
Le champ « Devis » est vide ou masqué.
Le champ « Commandes achat » est vide ou masqué.
La projection est prudente (aucun devis/achat simulé inclus).
Les smart buttons simulation sont masqués.
```

Statut : `OK / KO`

---

## 4. Test 2 — Mode simulation ON sans devis

### Action

Activer le mode simulation sans sélectionner de devis :

```text
Mode simulation = ON
Devis = (vide)
Sauvegarder
```

### Résultat attendu

```text
Odoo bloque la sauvegarde avec un message :
« Le mode simulation nécessite au moins un devis sélectionné. »
```

Statut : `OK / KO`

---

## 5. Test 3 — Mode simulation ON avec D1 + D2

### Action

```text
Mode simulation = ON
Devis = D1, D2
Sauvegarder / Actualiser
```

### Résultat attendu

```text
D1 est pris en compte pour +1 000 €
D2 est pris en compte pour +2 000 €
Le solde projeté augmente de 3 000 € au total
Le smart button « Simulations » affiche 2
Le risk_status est recalculé avec la simulation
```

Statut : `OK / KO`

---

## 6. Test 4 — Devis sélectionné mais devenu non éligible

### Action

Sélectionner D4 dans le champ Devis.

Puis confirmer D4 (`state = 'sale'`).

Revenir sur la projection Cash Guard.

### Résultat attendu

```text
D4 reste visible dans le champ « Devis » (il est toujours dans le M2M).
D4 n'apparaît PAS dans le smart button « Simulations ».
D4 n'impacte PAS la projection.
Le compteur smart button ne le compte pas.
```

Statut : `OK / KO`

---

## 7. Test 5 — validity_date hors période

### Action

Sélectionner D3 dans le champ Devis (si le domaine le permet ; sinon, noter que le domaine l'exclut correctement).

### Résultat attendu

```text
Cas A : D3 n'est pas sélectionnable (domaine filtrant correct).
Cas B : D3 est sélectionné mais exclu du calcul et du smart button.
```

Vérifier que D3 n'impacte pas la projection dans les deux cas.

Statut : `OK / KO`

---

## 8. Test 6 — Achat simulé sélectionné (impact négatif)

### Action

```text
Mode simulation = ON
Devis = D1
Commandes achat = P1
Sauvegarder / Actualiser
```

### Résultat attendu

```text
D1 ajoute +1 000 € (encaissement simulé)
P1 retire −500 € (décaissement simulé)
Impact net = +500 €
Le smart button « Achats simulés » affiche 1
Le solde projeté reflète le net simulation
```

Statut : `OK / KO`

---

## 9. Test 7 — Achat confirmé ou facturé → exclu

### Action

Confirmer P2 (`state = 'purchase'`).

Revenir sur la projection Cash Guard.

### Résultat attendu

```text
P2 reste dans le champ « Commandes achat » (M2M inchangé).
P2 n'apparaît PAS dans le smart button « Achats simulés ».
P2 n'impacte PAS la projection.
```

Statut : `OK / KO`

---

## 10. Test 8 — Retour simulation OFF

### Action

```text
Mode simulation = OFF
Sauvegarder
```

### Résultat attendu

```text
Le champ « Devis » est vidé automatiquement.
Le champ « Commandes achat » est vidé automatiquement.
La projection revient au mode prudent.
Le solde projeté ne tient plus compte d'aucune simulation.
Les smart buttons simulation sont masqués.
```

Statut : `OK / KO`

---

## 11. Tests complémentaires

### 11.1 Aucun effet comptable

```text
Aucune facture créée automatiquement.
Aucune écriture comptable créée.
Aucun paiement créé.
```

Statut : `OK / KO`

### 11.2 Devis Odoo non pollués

```text
Le formulaire sale.order ne contient plus de champs « Simulation trésorerie ».
Le formulaire purchase.order ne contient plus de champs « Simulation trésorerie ».
Les devis ne sont pas modifiés par l'activation/désactivation de la simulation.
```

Statut : `OK / KO`

---

## Grille de décision

| Zone testée | Attendu | Statut |
| ----------- | ------- | ------ |
| Tests automatiques | 28 tests verts (16 + 12) | OK / KO |
| Simulation OFF | Champs vidés, projection prudente | OK / KO |
| Simulation ON sans devis | Blocage | OK / KO |
| Simulation ON avec D1+D2 | Impact +3 000 € | OK / KO |
| Devis confirmé dans M2M | Exclu du calcul, visible dans M2M | OK / KO |
| validity_date hors période | Exclu | OK / KO |
| Achat simulé P1 | Impact −500 € | OK / KO |
| Achat confirmé P2 | Exclu | OK / KO |
| Retour OFF | Scénario vidé, projection prudente | OK / KO |
| Aucun effet comptable | Aucun flux réel créé | OK / KO |
| Devis non pollués | Pas de champs simulation sur SO/PO | OK / KO |

---

## Conclusion attendue

La recette est **GO V1.0.1 + V1.1** si :

```text
Le mode simulation est porté par Cash Guard, pas par les devis.
Les devis/achats sont sélectionnés explicitement dans la projection.
Les règles d'éligibilité filtrent les documents sélectionnés.
Le toggle OFF vide le scénario et revient en projection prudente.
Aucune facture ni écriture comptable n'est créée.
Les objets sale.order et purchase.order ne sont plus modifiés.
```

Limite maintenue :

```text
Les simulations impactent projected_balance et risk_status,
pas encore inflow_amount / outflow_amount.
```
