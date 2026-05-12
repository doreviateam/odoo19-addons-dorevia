# Spécification V1.1 — Simulation achats (`purchase.order`)

Extension du module `dorevia_cash_simulation` pour intégrer les demandes de prix et commandes d'achat fournisseur comme hypothèses de décaissement dans Cash Guard.

---

## 1. Objectif

La V1 couvre les devis clients (`sale.order`) comme encaissements simulés.

La V1.1 ajoute les devis fournisseurs / demandes de prix (`purchase.order`) comme décaissements simulés.

L'objectif est de compléter la vision bilatérale de la trésorerie simulée :

```text
sale.order   brouillon / envoyé   → encaissement simulé (+)
purchase.order   brouillon / envoyé / demande de prix   → décaissement simulé (−)
```

---

## 2. Positionnement

| Version | Périmètre simulation |
| ------- | -------------------- |
| V1      | Devis clients (`sale.order`) — encaissements |
| V1.1    | Devis clients + demandes de prix / commandes achat (`purchase.order`) — encaissements + décaissements |

La V1.1 ne rouvre pas la V1. Elle l'étend strictement par ajout.

---

## 3. Dépendances

```python
{
    "depends": [
        "purchase",
        "sale_management",
        "dorevia_cash_guard",
    ],
}
```

La dépendance `purchase` est ajoutée en V1.1.

Point d'attention : si `purchase` n'est pas installé, le module ne doit pas bloquer. Deux stratégies possibles :

* **Option A** : ajouter `purchase` comme dépendance dure dans `dorevia_cash_simulation` (simple, mais impose l'installation de `purchase`)
* **Option B** : créer un sous-module `dorevia_cash_simulation_purchase` séparé (plus propre, n'impose pas `purchase` aux utilisateurs V1)

Arbitrage MOA requis.

---

## 4. Champs ajoutés sur `purchase.order`

Symétrique de `sale.order` :

```python
cash_simulation_ok = fields.Boolean(
    string="Inclure dans la simulation de trésorerie",
    default=False,
    tracking=True,
    help=(
        "Permet d'utiliser cette demande de prix / commande achat comme hypothèse "
        "de décaissement futur dans Cash Guard lorsque le mode simulation est activé."
    ),
)
cash_simulation_due_date = fields.Date(
    string="Date d'échéance simulation",
    tracking=True,
    help=(
        "Date prévisionnelle de décaissement utilisée uniquement pour la simulation "
        "de trésorerie. Indépendante de la date de commande."
    ),
)
cash_simulation_eligible = fields.Boolean(
    compute="_compute_cash_simulation_eligible",
    store=False,
)
```

---

## 5. Règles d'éligibilité

Un bon de commande achat est éligible à la simulation Cash Guard si :

* `cash_simulation_ok = True`
* `cash_simulation_due_date` renseignée et strictement supérieure à la date du jour
* `state in ('draft', 'sent')` (demande de prix ou envoyée, pas encore confirmée)
* pas de facture fournisseur liée (`invoice_ids = False`)
* même société que la projection Cash Guard
* même devise que la projection Cash Guard

### États éligibles

| État `purchase.order.state` | Éligible ? | Raison |
| --- | ---: | --- |
| `draft` | Oui | Demande de prix brouillon |
| `sent` | Oui | Demande de prix envoyée |
| `purchase` | Non | Commande confirmée — risque de double comptage |
| `done` | Non | Commande verrouillée |
| `cancel` | Non | Annulée |

---

## 6. Règle anti double comptage

Identique à la V1 côté ventes :

```text
Un bon de commande confirmé, verrouillé, annulé ou ayant au moins une facture fournisseur liée
n'est jamais intégré comme simulation.
```

---

## 7. Sens du flux

```text
Montant simulé = purchase.order.amount_total
Date du flux simulé = purchase.order.cash_simulation_due_date
Sens du flux = décaissement prévisionnel (négatif)
```

Le montant est soustrait de la projection (sortie de trésorerie).

---

## 8. Intégration dans Cash Guard

### 8.1 Toggle existant

Le même toggle `include_simulation` sur `dorevia.cash.guard` active les deux types de simulation (ventes + achats). Pas de toggle séparé en V1.1.

### 8.2 Point d'extension

La méthode `_get_sale_simulation_buckets` existante gère les ventes.

Ajouter une méthode `_get_purchase_simulation_buckets` symétrique, avec montants négatifs.

Surcharger `_manual_line_net_by_week_index` pour y ajouter les buckets achats :

```python
def _manual_line_net_by_week_index(self, meta, situation_date):
    buckets = super()._manual_line_net_by_week_index(meta, situation_date)
    if not self.include_simulation:
        return buckets
    # V1.1 : ajouter les décaissements simulés
    purchase_buckets = self._get_purchase_simulation_buckets(meta, situation_date)
    for week_idx, net in purchase_buckets.items():
        buckets[week_idx] = buckets.get(week_idx, 0.0) + net
    return buckets
```

### 8.3 Smart button

Le smart button existant affiche les devis clients simulés.

V1.1 : soit étendre le compteur pour inclure les achats, soit ajouter un second smart button dédié. Arbitrage MOA requis.

---

## 9. Validation de date

Même logique que V1 :

* Blocage à l'activation si date absente ou non future
* Pas de blocage sur un write non lié à la simulation si la date est périmée
* Exclusion automatique des bons périmés du calcul

---

## 10. Affichage

Les lignes simulées issues d'achats doivent être clairement identifiées :

```text
Simulation Achat — PO00042 — Fournisseur ABC — −3 500,00 € — échéance 20/06/2026
```

---

## 11. Contraintes

Le module V1.1 ne doit pas :

* créer de facture fournisseur automatiquement
* créer d'écriture comptable
* modifier la logique native de confirmation des bons de commande achat
* permettre un double comptage entre bon de commande simulé et flux réel

---

## 12. Critères de recette V1.1

* un bon de commande achat `draft` ou `sent` peut être marqué simulation
* une date d'échéance de simulation peut être renseignée
* Odoo bloque l'activation sans date future
* un bon de commande périmé est exclu du calcul
* un bon de commande confirmé (`state = 'purchase'`) n'est plus intégré
* un bon de commande avec facture fournisseur liée n'est plus intégré
* Cash Guard simulation OFF : aucun achat simulé inclus
* Cash Guard simulation ON : les achats éligibles réduisent la projection
* les lignes simulées achats sont clairement distinguées des lignes réelles
* aucune facture fournisseur créée automatiquement
* aucune écriture comptable créée
* les devis clients V1 continuent de fonctionner sans régression

---

## 13. Limite V1.1

```text
Même limite que V1 : les simulations impactent projected_balance et risk_status,
pas encore inflow_amount / outflow_amount dans la grille hebdomadaire.
```

---

## 14. Architecture — arbitrage MOA

**Décision MOA : Option B retenue.**

Le volet achats est implémenté dans un module séparé `dorevia_cash_simulation_purchase` qui dépend de :

```python
"depends": [
    "purchase",
    "dorevia_cash_simulation",
]
```

La V1 (`dorevia_cash_simulation`) reste figée et inchangée.

### Smart button

**Décision MOA : deux smart buttons séparés.**

Le smart button existant « Devis simulés » reste dédié aux ventes (`sale.order`).

Un second smart button « Achats simulés » est ajouté par `dorevia_cash_simulation_purchase` pour les demandes de prix / bons de commande achat (`purchase.order`).

Le sens des flux étant opposé (encaissement vs décaissement), cette séparation préserve la lisibilité.
