# Ticket — Refactoring simulation : scénario porté par Cash Guard

**Module** : `dorevia_cash_simulation` (V1.0.1) + `dorevia_cash_simulation_purchase` (V1.1)
**Type** : refactoring majeur (changement de doctrine)
**Statut** : implémenté, en attente de recette

### Versioning

| Version | Module | Contenu |
| ------- | ------ | ------- |
| V1.0.0 | `dorevia_cash_simulation` | Simulation portée par `sale.order` (champs sur le devis) — **obsolète** |
| V1.0.1 | `dorevia_cash_simulation` | Refactoring : simulation portée par Cash Guard via `simulation_sale_order_ids` |
| V1.1 | `dorevia_cash_simulation_purchase` | Extension achats via `simulation_purchase_order_ids` |

---

## 1. Contexte

La V1 de `dorevia_cash_simulation` portait la simulation directement sur les devis (`sale.order`) via trois champs :

```python
cash_simulation_ok = fields.Boolean(...)
cash_simulation_due_date = fields.Date(...)
cash_simulation_eligible = fields.Boolean(compute=...)
```

La projection Cash Guard recherchait ensuite tous les devis éligibles de la société par un domaine ORM global.

### Problèmes identifiés

1. **Pollution des devis** : des champs de simulation ajoutés sur `sale.order` sans rapport avec le cycle commercial natif.
2. **Effet de bord** : d'anciens devis marqués simulation pouvaient réapparaître dans une nouvelle projection sans intention de l'utilisateur.
3. **Scénario diffus** : la simulation n'était pas un scénario explicite attaché à une projection, mais un état réparti sur N devis.
4. **Date artificielle** : `cash_simulation_due_date` dupliquait la logique de `validity_date` sans la réutiliser.
5. **Extensibilité achats** : le même pattern (champs sur `purchase.order`) alourdissait le modèle achat.

---

## 2. Décision produit

> La simulation devient un scénario attaché à la projection Cash Guard, et non plus un état porté par les devis.

Le mode simulation reste activé par le toggle `include_simulation` sur `dorevia.cash.guard`.

Les devis à simuler sont sélectionnés explicitement dans un champ Many2many sur la projection.

---

## 3. Changements techniques

### 3.1 `dorevia_cash_simulation` (ventes)

#### Supprimé sur `sale.order`

| Champ | Type | Raison |
| ----- | ---- | ------ |
| `cash_simulation_ok` | Boolean | Remplacé par sélection M2M sur Cash Guard |
| `cash_simulation_due_date` | Date | Remplacé par `validity_date` natif |
| `cash_simulation_eligible` | Boolean compute | Éligibilité calculée côté Cash Guard |

Toute la logique de validation (`_check_cash_simulation_fields`, surcharges `create`/`write`) est supprimée de `sale.order`.

#### Ajouté sur `dorevia.cash.guard`

| Champ | Type | Détails |
| ----- | ---- | ------- |
| `simulation_sale_order_ids` | Many2many `sale.order` | Devis sélectionnés pour le scénario |

#### Logique modifiée

| Méthode | Avant | Après |
| ------- | ----- | ----- |
| Recherche devis | `_get_simulation_order_domain()` → domaine global | `_get_eligible_sale_simulation_orders()` → filtre `simulation_sale_order_ids` |
| Date de projection | `cash_simulation_due_date` | `validity_date` |
| Compteur smart button | `search_count` global | `len(eligible)` depuis M2M |
| Validation | `@api.constrains` sur `sale.order` | `@api.constrains` sur `dorevia.cash.guard` |
| Toggle OFF | Pas de nettoyage | Vide automatiquement `simulation_sale_order_ids` |

#### Règles d'éligibilité

Un devis sélectionné est effectivement intégré si :

```text
state in ('draft', 'sent')
invoice_ids = False
company_id = cash_guard.company_id
currency_id = cash_guard.currency_id
validity_date renseignée
validity_date dans [date_from, date_to] de la projection
```

#### Contrainte

```text
Mode simulation ON → au moins un devis sélectionné (si seul dorevia_cash_simulation est installé)
Mode simulation OFF → champ Devis vidé automatiquement
```

Si `dorevia_cash_simulation_purchase` est également installé, la contrainte est assouplie : Mode simulation ON exige au moins un document de simulation, devis **ou** achat.

### 3.2 `dorevia_cash_simulation_purchase` (achats)

Même doctrine appliquée symétriquement.

| Champ | Type | Détails |
| ----- | ---- | ------- |
| `simulation_purchase_order_ids` | Many2many `purchase.order` | Commandes achat sélectionnées |

Date de projection : `purchase.order.date_planned` (Datetime → `.date()` pour le bucketing).

Montants : **négatifs** (décaissement simulé).

---

## 4. Vues

### Formulaire `dorevia.cash.guard`

Colonne gauche, sous Journaux :

```text
Nom
Société
Responsable
Journaux
Mode simulation        [toggle]
Devis                  [many2many_tags]    (visible si simulation ON)
Commandes achat        [many2many_tags]    (visible si simulation ON, module purchase)
```

Domaine de sélection sur les M2M : filtré pour ne montrer que les devis/PO pertinents (état, société, devise, date renseignée).

### Smart buttons

- « Devis simulés » (icône `fa-line-chart`) : devis ventes éligibles
- « Achats simulés » (icône `fa-shopping-cart`) : PO éligibles

---

## 5. Tests

### `dorevia_cash_simulation` — 16 tests

| # | Test | Vérification |
| - | ---- | ------------ |
| 1 | Simulation ON sans devis | `ValidationError` |
| 2 | Simulation ON avec devis | OK |
| 3 | Toggle OFF vide les devis | M2M vidé |
| 4 | Éligible draft + validity_date | `eligible = True` |
| 5 | Éligible sent + validity_date | `eligible = True` |
| 6 | Sans validity_date | Exclu |
| 7 | validity_date hors période | Exclu |
| 8 | Confirmé | Exclu |
| 9 | Annulé | Exclu |
| 10 | Autre société | Exclu |
| 11 | Simulation OFF | Aucun impact projection |
| 12 | Simulation ON | Montant positif dans les buckets |
| 13 | Bucket bonne semaine | Montant dans la bonne semaine |
| 14 | Toggle déclenche recompute | `forecast_final_balance` change |
| 15 | Compteur smart button | Comptage correct |
| 16 | Devis sélectionné mais confirmé | Reste dans M2M, exclu de la projection |

### `dorevia_cash_simulation_purchase` — 12 tests

| # | Test | Vérification |
| - | ---- | ------------ |
| 1 | PO draft éligible | `eligible = True` |
| 2 | PO confirmé | Exclu |
| 3 | PO hors période | Exclu |
| 4 | Simulation OFF | Aucun impact |
| 5 | Simulation ON | Montant négatif dans les buckets |
| 6 | Combinaison ventes + achats | Net = vente − achat |
| 7 | Compteur achats | Comptage correct |
| 8 | Compteur OFF | = 0 |
| 9 | Action smart button | `res_model = purchase.order` |
| 10 | Toggle OFF vide les PO | M2M vidé |
| 11 | PO draft éligible (redondant) | Confirmation du filtre |
| 12 | PO sent éligible | `eligible = True` |

---

## 6. Migration

Les anciens champs `cash_simulation_ok`, `cash_simulation_due_date`, `cash_simulation_eligible` ne sont plus déclarés dans le modèle Python. Après mise à jour du module, ils ne sont plus utilisés par l'application. Les colonnes techniques éventuellement restantes en base pourront être nettoyées ultérieurement par migration SQL si nécessaire.

Aucune migration fonctionnelle de données n'est requise.

---

## 7. Doctrine UX

| Onglet Cash Guard | Contenu | Nature |
| --- | --- | --- |
| **Projection** | Trajectoire du solde par période | Vision temporelle agrégée |
| **Facturation** | Factures / pièces comptables réelles | Flux réels |
| **Notes** | Contexte libre | Commentaires |

Aujourd'hui, la simulation est visible et pilotée via le toggle **Mode simulation**, les champs M2M (Devis, Commandes achat) et les smart buttons. Elle impacte `projected_balance` et `risk_status` dans l'onglet Projection, mais ne pollue jamais l'onglet Facturation.

Un onglet **Simulation** dédié dans le notebook Cash Guard pourra être ajouté dans une version future pour afficher le détail des hypothèses retenues (devis, achats, montants, dates).

---

## 8. Limites maintenues

- Les simulations impactent `projected_balance` et `risk_status`, pas `inflow_amount` / `outflow_amount`.
- Pas de conversion multi-devise.
- Pas d'éclatement selon conditions de paiement.
- Le toggle est unique pour ventes + achats (pas de granularité séparée).
