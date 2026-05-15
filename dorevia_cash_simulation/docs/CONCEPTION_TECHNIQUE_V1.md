# Conception technique V1 — dorevia_cash_simulation

Périmètre : strictement conforme au README V1 validé.

Ajustements MOA intégrés avant implémentation (4 points) :

1. Contrainte de date via `create()`/`write()` (pas de `@api.constrains`)
2. Recompute `include_simulation` via surcharge de `write()` (pas de mutation de constante)
3. `_sync_weekly_lines` : `projected_balance` affecté, `inflow_amount`/`outflow_amount` non (acceptable V1)
4. Devise via `self.currency_id` (`related="company_id.currency_id"`, stocké)

---

## 1. Modèles

### 1.1 Modèles hérités

| Modèle               | Type d'héritage | Objectif                                       |
| --------------------- | --------------- | ---------------------------------------------- |
| `sale.order`          | `_inherit`      | Ajout des champs de simulation                 |
| `dorevia.cash.guard`  | `_inherit`      | Ajout du toggle simulation + surcharge calcul  |

### 1.2 Modèles créés

Aucun. La V1 ne crée pas de nouveau modèle.

Les lignes de simulation sont calculées à la volée et ne sont pas persistées en base.

---

## 2. Champs ajoutés

### 2.1 Sur `sale.order`

```python
cash_simulation_ok = fields.Boolean(
    string="Inclure dans la simulation de trésorerie",
    default=False,
    tracking=True,
)
cash_simulation_due_date = fields.Date(
    string="Date d'échéance simulation",
    tracking=True,
)
cash_simulation_eligible = fields.Boolean(
    compute="_compute_cash_simulation_eligible",
    store=False,
)
```

### 2.2 Validation — via `create()` / `write()`, pas `@api.constrains`

La validation est implémentée dans une méthode `_check_cash_simulation_activation(vals)` appelée depuis `create()` et `write()`.

Elle bloque uniquement quand :

* `cash_simulation_ok` passe à `True` (activation) ;
* ou `cash_simulation_due_date` change alors que `cash_simulation_ok` est `True`.

Elle ne bloque jamais une sauvegarde sans rapport avec la simulation (ex. modification du `note` sur un devis dont la date de simulation est périmée).

### 2.3 Sur `dorevia.cash.guard`

```python
include_simulation = fields.Boolean(
    string="Inclure les simulations commerciales",
    default=False,
    tracking=True,
)
simulation_order_count = fields.Integer(
    compute="_compute_simulation_order_count",
)
```

Le recompute est déclenché via une surcharge de `write()` qui teste `"include_simulation" in vals`, en évitant le double recompute si un autre champ de `_RECOMPUTE_GUARD_WRITE_FIELDS` est aussi modifié dans le même `write()`.

---

## 3. Point d'extension dans Cash Guard

### 3.1 Stratégie retenue

Pas de modification du code source de `dorevia_cash_guard`.

Surcharge pure via `_inherit` de `_manual_line_net_by_week_index`.

### 3.2 Méthode surchargée

```python
def _manual_line_net_by_week_index(self, meta, situation_date):
    buckets = super()._manual_line_net_by_week_index(meta, situation_date)
    if not self.include_simulation:
        return buckets
    sim_buckets = self._get_sale_simulation_buckets(meta, situation_date)
    for week_idx, net in sim_buckets.items():
        buckets[week_idx] = buckets.get(week_idx, 0.0) + net
    return buckets
```

### 3.3 Impact vérifié sur `_sync_weekly_lines`

Analyse du code existant :

* `projected_balance` utilise `proj_map` issu de `_cumulative_projected_by_week_index`, qui consomme le résultat de `_manual_line_net_by_week_index` → **affecté par la surcharge** ✓
* `inflow_amount` / `outflow_amount` dans les mailles forecast sont calculés directement depuis `self.line_ids` → **non affectés** par la surcharge

Conséquence V1 : la colonne Projection et le risk_status incluent les montants simulés. Le détail entrées/sorties par maille ne les inclut pas. C'est acceptable car le résultat de projection est correct et le smart button montre le détail des devis.

---

## 4. Règle exacte de recherche des devis éligibles

```python
def _get_simulation_order_domain(self):
    today = fields.Date.today()
    return [
        ("cash_simulation_ok", "=", True),
        ("cash_simulation_due_date", ">", today),
        ("state", "in", ("draft", "sent")),
        ("invoice_ids", "=", False),
        ("company_id", "=", self.company_id.id),
        ("currency_id", "=", self.currency_id.id),
    ]
```

Le domaine utilise `self.currency_id` qui est `related="company_id.currency_id"` (stocké) sur `dorevia.cash.guard`.

---

## 5. Format des lignes simulées retournées

Format identique à celui de `_manual_line_net_by_week_index` :

```python
{week_index (int): net_amount (float)}
```

Où `net_amount` est positif (encaissement). Exemple : `{3: 1250.00, 5: 8400.00}`

Affichage détaillé via smart button (approche B) ouvrant la liste des `sale.order` éligibles.

---

## 6. Vues modifiées

### 6.1 `sale.order` — formulaire

XPath après `payment_term_id` : bloc séparé par un `<separator>`, masqué si `state not in ('draft', 'sent')`, restreint au groupe `group_cash_guard_user`.

### 6.2 `sale.order` — listes (devis + commandes)

Colonne optionnelle `cash_simulation_ok` après `amount_total`, masquée par défaut (`optional="hide"`).

### 6.3 `dorevia.cash.guard` — formulaire

* Toggle `include_simulation` après `comfort_threshold_rate`
* Smart button `simulation_order_count` dans un `oe_button_box`, visible seulement si `include_simulation`

### 6.4 `dorevia.cash.guard` — liste

Colonne optionnelle `include_simulation` avant `risk_status`.

---

## 7. Droits d'accès

Pas de nouveau modèle → pas de `ir.model.access.csv`.

Visibilité des champs contrôlée via `groups="dorevia_cash_guard.group_cash_guard_user"` dans les vues XML.

---

## 8. Tests implémentés

17 tests dans `tests/test_cash_simulation.py` :

| Catégorie | Tests |
|---|---|
| Contraintes | activation sans date, date passée, date future OK, changement date vers passé, write non lié sur simulation périmée |
| Éligibilité | draft OK, sent OK, non marqué KO, confirmé KO, annulé KO |
| Domaine | autre société exclue, date périmée exclue |
| Projection | simulation OFF inchangée, simulation ON ajoute montant, bucket correct par maille |
| Recompute | toggle déclenche recompute |
| Smart button | count correct ON, count 0 OFF, action retourne sale.order |

---

## 9. Arborescence du module

```
dorevia_cash_simulation/
├── __init__.py
├── __manifest__.py
├── README.md
├── docs/
│   └── CONCEPTION_TECHNIQUE_V1.md
├── models/
│   ├── __init__.py
│   ├── sale_order.py
│   └── cash_guard.py
├── views/
│   ├── sale_order_views.xml
│   └── cash_guard_views.xml
└── tests/
    ├── __init__.py
    └── test_cash_simulation.py
```

---

## 10. Résumé des décisions techniques

| Décision                            | Choix V1                                                          |
| ----------------------------------- | ----------------------------------------------------------------- |
| Nouveau modèle                      | Non                                                               |
| Persistance des lignes simulées     | Non — calcul dynamique                                            |
| Modification de `dorevia_cash_guard`| Non — surcharge via `_inherit` uniquement                         |
| Point d'extension                   | Surcharge de `_manual_line_net_by_week_index`                     |
| Format de retour                    | `{week_index: net_amount}` — identique à l'existant              |
| Toggle simulation                   | Champ `include_simulation` par projection                         |
| Recompute toggle                    | Via surcharge de `write()` (pas de mutation de constante)         |
| Contrainte date                     | Via `create()`/`write()` (pas de `@api.constrains`)              |
| Devise                              | `self.currency_id` = `related company_id.currency_id` (stocké)   |
| Groupes de sécurité                 | Réutilisation de `group_cash_guard_user`                          |
| Affichage détaillé                  | Smart button ouvrant la liste des devis éligibles                 |
| Conversion devise                   | Exclue en V1                                                      |
| Conditions de paiement              | 1 devis = 1 flux (`amount_total` à `cash_simulation_due_date`)   |
| `inflow_amount` / `outflow_amount`  | Non affectés en V1 (acceptable, projection correcte)             |
