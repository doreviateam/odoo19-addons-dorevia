# Conception technique V1.1 — `dorevia_cash_simulation_purchase`

Extension optionnelle de `dorevia_cash_simulation` ajoutant les demandes de prix / commandes achat fournisseur comme hypothèses de décaissement dans Cash Guard.

---

## 1. Architecture module

| Élément | Valeur |
| ------- | ------ |
| Nom technique | `dorevia_cash_simulation_purchase` |
| Dépendances | `purchase`, `dorevia_cash_simulation` |
| Modèles hérités | `purchase.order`, `dorevia.cash.guard` |
| Nouveau modèle | Aucun |
| Nouveau groupe | Aucun (réutilise `dorevia_cash_guard.group_cash_guard_user`) |

La V1 (`dorevia_cash_simulation`) reste inchangée et figée.

---

## 2. Modèle `purchase.order` — champs ajoutés

| Champ | Type | Détails |
| ----- | ---- | ------- |
| `cash_simulation_ok` | `Boolean` | `default=False`, `tracking=True` |
| `cash_simulation_due_date` | `Date` | `tracking=True`, date prévisionnelle de décaissement |
| `cash_simulation_eligible` | `Boolean` | `compute`, non stocké |

### Éligibilité (`_compute_cash_simulation_eligible`)

```python
eligible = (
    cash_simulation_ok
    and cash_simulation_due_date > today
    and state in ('draft', 'sent')
    and not invoice_ids
)
```

### Validation (`_check_cash_simulation_fields`)

Appelée dans `create()` et `write()` uniquement si `cash_simulation_ok` ou `cash_simulation_due_date` figure dans les vals :

* `cash_simulation_ok = True` sans date → `ValidationError`
* `cash_simulation_due_date <= today` → `ValidationError`
* Écriture non liée à la simulation sur un bon périmé → aucun blocage

---

## 3. Modèle `dorevia.cash.guard` — extension achats

### 3.1 Champ ajouté

| Champ | Type | Détails |
| ----- | ---- | ------- |
| `simulation_purchase_count` | `Integer` | `compute`, compteur de PO éligibles |

### 3.2 Méthodes ajoutées

| Méthode | Rôle |
| ------- | ---- |
| `_get_purchase_simulation_domain()` | Domaine ORM pour les PO éligibles |
| `_search_eligible_purchase_simulation_orders()` | Recherche des PO éligibles |
| `_get_purchase_simulation_buckets(meta, situation_date)` | Calcul des buckets hebdomadaires (montants **négatifs**) |
| `action_view_purchase_simulation_orders()` | Action smart button → liste des PO éligibles |

### 3.3 Override `_manual_line_net_by_week_index`

```python
def _manual_line_net_by_week_index(self, meta, situation_date):
    buckets = super()._manual_line_net_by_week_index(meta, situation_date)
    if not self.include_simulation:
        return buckets
    purchase_buckets = self._get_purchase_simulation_buckets(meta, situation_date)
    for week_idx, net in purchase_buckets.items():
        buckets[week_idx] = buckets.get(week_idx, 0.0) + net
    return buckets
```

Chaîne d'héritage : `dorevia.cash.guard` (base) → `dorevia_cash_simulation` (ventes +) → `dorevia_cash_simulation_purchase` (achats −).

### 3.4 Domaine de recherche PO

```python
[
    ("cash_simulation_ok", "=", True),
    ("cash_simulation_due_date", ">", today),
    ("state", "in", ("draft", "sent")),
    ("invoice_ids", "=", False),
    ("company_id", "=", self.company_id.id),
    ("currency_id", "=", self.currency_id.id),
]
```

### 3.5 Sens du flux

```text
Montant simulé = −purchase.order.amount_total (décaissement)
Date du flux = purchase.order.cash_simulation_due_date
```

---

## 4. Vues

### 4.1 `purchase.order` — formulaire

Héritage de `purchase.purchase_order_form` via `<xpath expr="//field[@name='payment_term_id']" position="after">`.

Groupe « Simulation trésorerie » visible en état `draft`/`sent` pour `group_cash_guard_user`.

### 4.2 `purchase.order` — liste

Héritage de `purchase.purchase_order_kpis_tree` : colonne optionnelle `cash_simulation_ok`.

### 4.3 `dorevia.cash.guard` — smart button achats

Second smart button « Achats simulés » (icône `fa-shopping-cart`), visible quand `include_simulation = True`.

Séparé du smart button ventes existant (icône `fa-line-chart`) pour lisibilité.

---

## 5. Toggle

Le toggle `include_simulation` existant sur `dorevia.cash.guard` (V1) active simultanément les simulations ventes ET achats. Pas de toggle séparé en V1.1.

---

## 6. Droits d'accès

Réutilisation de `dorevia_cash_guard.group_cash_guard_user` pour :

* la visibilité des champs simulation sur `purchase.order`
* l'accès au smart button achats sur Cash Guard

---

## 7. Tests prévus

| # | Test | Vérification |
| - | ---- | ------------ |
| 1 | Activation sans date | `ValidationError` |
| 2 | Activation avec date passée | `ValidationError` |
| 3 | Activation avec date future | OK |
| 4 | Modification date vers passé | `ValidationError` |
| 5 | Write non-simulation sur bon périmé | Pas de blocage |
| 6 | Éligibilité draft | `eligible = True` |
| 7 | Éligibilité sent | `eligible = True` |
| 8 | Non marqué | `eligible = False` |
| 9 | Confirmé (`purchase`) | `eligible = False` |
| 10 | Annulé | `eligible = False` |
| 11 | Autre société | Exclu du domaine |
| 12 | Date périmée | Exclu du domaine |
| 13 | Simulation OFF | Aucun impact projection |
| 14 | Simulation ON | Montant **négatif** dans les buckets |
| 15 | Bucket correct semaine | Montant dans la bonne semaine, < 0 |
| 16 | Combinaison vente + achat | Net = vente − achat |
| 17 | Compteur achats simulés | Comptage correct |
| 18 | Compteur OFF | = 0 |
| 19 | Action smart button | `res_model = purchase.order` |

Total : **19 tests**.

---

## 8. Limites V1.1

* Les simulations impactent `projected_balance` et `risk_status`, pas encore `inflow_amount` / `outflow_amount`.
* Pas de conversion multi-devise.
* Pas d'éclatement selon conditions de paiement.
* Le toggle est unique pour ventes + achats (pas de granularité séparée).
