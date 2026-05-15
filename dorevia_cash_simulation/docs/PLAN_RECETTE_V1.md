# Plan de recette fonctionnelle — `dorevia_cash_simulation` V1

## 0. Objectif de la recette

Valider que les devis marqués en simulation peuvent enrichir une projection Cash Guard **uniquement en mode simulation ON**, sans double comptage, sans facture générée, sans écriture comptable, et sans impact parasite sur les flux réels.

---

## 1. Préconditions

Sur `tenant_o8` :

```text
Module dorevia_cash_simulation installé
Tests automatisés OK
Utilisateur avec droits Cash Guard
Au moins une projection Cash Guard disponible
Au moins un client disponible
Devise société = EUR
```

Créer ou identifier une projection Cash Guard de test.

Noter avant test :

```text
Solde projeté initial :
Risk status initial :
Mode simulation : OFF
```

---

## 2. Jeu de données à créer

Créer 5 devis clients.

| Réf. | État                    | Simulation OK | Date simulation | Montant TTC | Résultat attendu                     |
| ---- | ----------------------- | ------------: | --------------- | ----------: | ------------------------------------ |
| D1   | Brouillon               |           Oui | Future          |     1 000 € | Inclus en simulation                 |
| D2   | Envoyé                  |           Oui | Future          |     2 000 € | Inclus en simulation                 |
| D3   | Brouillon               |           Non | Future          |     3 000 € | Exclu                                |
| D4   | Brouillon               |           Oui | Date passée     |     4 000 € | Refusé ou exclu                      |
| D5   | Brouillon puis confirmé |           Oui | Future          |     5 000 € | Inclus puis exclu après confirmation |

---

## 3. Test 1 — Simulation OFF

### Action

Dans Cash Guard :

```text
include_simulation = False
```

Lancer le recalcul de la projection.

### Résultat attendu

```text
Les devis D1 et D2 ne sont pas pris en compte.
Le solde projeté reste prudent.
Le risk_status ne tient pas compte des devis simulés.
Le smart button simulation est masqué ou indique 0 selon implémentation.
```

Statut : `OK / KO`

---

## 4. Test 2 — Activation simulation ON

### Action

Dans Cash Guard :

```text
include_simulation = True
```

Recalculer la projection.

### Résultat attendu

```text
D1 est pris en compte pour +1 000 €
D2 est pris en compte pour +2 000 €
D3 est exclu car Simulation OK = False
Le solde projeté augmente de 3 000 € au total
Le risk_status est recalculé avec cette simulation
```

Point V1 à vérifier :

```text
projected_balance et risk_status changent.
inflow_amount / outflow_amount ne changent pas forcément en V1.
```

Statut : `OK / KO`

---

## 5. Test 3 — Smart button simulations

### Action

Cliquer sur le smart button :

```text
Simulations
```

### Résultat attendu

La liste doit afficher uniquement :

```text
D1
D2
```

Ne doivent pas apparaître :

```text
D3 : non marqué simulation
D4 : date passée
D5 : selon état au moment du test
```

Statut : `OK / KO`

---

## 6. Test 4 — Validation date obligatoire

### Action

Créer un devis brouillon, cocher :

```text
Inclure dans la simulation de trésorerie = Oui
```

sans renseigner la date de simulation.

### Résultat attendu

Odoo bloque la sauvegarde avec un message du type :

```text
Un devis de simulation doit avoir une date d'échéance.
```

Statut : `OK / KO`

---

## 7. Test 5 — Validation date future

### Action

Créer ou modifier un devis avec :

```text
Simulation OK = Oui
Date simulation = aujourd'hui ou date passée
```

### Résultat attendu

Odoo bloque la sauvegarde ou l'activation avec un message du type :

```text
La date d'échéance de simulation doit être supérieure à aujourd'hui.
```

Statut : `OK / KO`

---

## 8. Test 6 — Exclusion après confirmation

### Action

Prendre D5 :

```text
Brouillon
Simulation OK = Oui
Date future
Montant = 5 000 €
```

Vérifier qu'il est inclus en simulation ON.

Puis confirmer le devis.

### Résultat attendu

Après confirmation :

```text
D5 passe en state = sale
D5 n'est plus inclus dans la simulation
Le smart button ne l'affiche plus
Le solde projeté retire les 5 000 € simulés
Aucun double comptage avec le réel
```

Statut : `OK / KO`

---

## 9. Test 7 — Exclusion après facture liée

### Action

Sur un devis simulé éligible, créer une facture liée, même brouillon si possible.

### Résultat attendu

```text
Le devis n'est plus inclus dans la simulation dès qu'une facture liée existe.
Le smart button ne l'affiche plus.
Le solde projeté retire le montant simulé.
```

Même si la facture est brouillon, l'exclusion est attendue en V1.

Statut : `OK / KO`

---

## 10. Test 8 — Date devenue périmée

### Action

Prendre un devis déjà marqué simulation avec date future.

Modifier uniquement la date de simulation pour la mettre à hier.

### Résultat attendu

Deux cas acceptables selon implémentation :

```text
Cas A : Odoo bloque la modification car on touche un champ simulation.
Cas B : Odoo accepte mais le devis est exclu du calcul.
```

Comportement implémenté :

```text
Odoo bloque si un champ simulation est touché et que la date finale est invalide.
```

À tester aussi :

Modifier un champ non lié à la simulation sur un devis déjà périmé.

Résultat attendu :

```text
Pas de blocage si aucun champ simulation n'est touché.
```

Statut : `OK / KO`

---

## 11. Test 9 — Multi-société

Seulement si `tenant_o8` a plusieurs sociétés.

### Action

Créer un devis simulé dans une autre société.

### Résultat attendu

```text
Le devis n'apparaît pas dans les simulations de la projection Cash Guard de la société courante.
Il n'impacte pas le solde projeté.
```

Statut : `OK / KO / Non testé`

---

## 12. Test 10 — Devise différente

Seulement si une devise étrangère est activée.

### Action

Créer un devis simulé en USD ou autre devise différente de la devise Cash Guard.

### Résultat attendu

```text
Le devis est exclu de la simulation V1.
Aucune conversion automatique n'est faite.
```

Statut : `OK / KO / Non testé`

---

## 13. Test 11 — Aucun effet comptable

### Action

Après création de devis simulés, vérifier :

```text
Factures
Écritures comptables
Paiements
Mouvements bancaires
```

### Résultat attendu

```text
Aucune facture créée automatiquement.
Aucune écriture comptable créée.
Aucun paiement créé.
Aucun mouvement bancaire créé.
```

Statut : `OK / KO`

---

## 14. Test 12 — Retour simulation OFF

### Action

Repasser Cash Guard en :

```text
include_simulation = False
```

Recalculer.

### Résultat attendu

```text
Les devis simulés ne sont plus pris en compte.
Le solde projeté revient à la projection prudente.
Le risk_status revient à la lecture sans simulation.
```

Statut : `OK / KO`

---

## Grille de décision

| Zone testée           | Attendu                            | Statut        |
| --------------------- | ---------------------------------- | ------------- |
| Installation module   | Module installé                    | OK / KO       |
| Tests automatiques    | 19 tests verts                     | OK            |
| Simulation OFF        | Aucun devis simulé inclus          | OK / KO       |
| Simulation ON         | D1 + D2 inclus                     | OK / KO       |
| Smart button          | Liste correcte                     | OK / KO       |
| Date absente          | Blocage                            | OK / KO       |
| Date passée           | Blocage si champ simulation touché | OK / KO       |
| Devis confirmé        | Exclusion                          | OK / KO       |
| Devis facturé         | Exclusion                          | OK / KO       |
| Multi-société         | Exclusion autre société            | OK / KO / N/A |
| Devise différente     | Exclusion autre devise             | OK / KO / N/A |
| Aucun effet comptable | Aucun flux réel créé               | OK / KO       |
| Retour OFF            | Projection prudente retrouvée      | OK / KO       |

---

## Conclusion attendue

La recette est **GO V1** si :

```text
Simulation ON ajoute uniquement les devis éligibles.
Simulation OFF les exclut.
Aucun devis confirmé/facturé n'est double compté.
Aucune facture ni écriture comptable n'est créée.
Les limites V1 sont explicites.
```

Limite V1 assumée à noter dans le PV :

```text
Les simulations impactent projected_balance et risk_status,
mais ne sont pas encore ventilées dans inflow_amount / outflow_amount.
```
