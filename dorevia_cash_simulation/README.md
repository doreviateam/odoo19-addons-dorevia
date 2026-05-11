# dorevia_cash_simulation

Extension Odoo du module `dorevia_cash_guard` dédiée à la simulation de trésorerie à partir de devis clients.

---

## 1. Objectif

Le module `dorevia_cash_simulation` ajoute une couche optionnelle de projection à `dorevia_cash_guard`.

Il permet d'intégrer certains devis clients comme hypothèses futures de trésorerie, sans les confondre avec des flux réels, comptables ou bancaires.

L'objectif fonctionnel est simple :

> Visualiser l'impact potentiel de certains devis sur la trésorerie prévisionnelle, uniquement lorsque le mode simulation est activé.

---

## 2. Positionnement produit

Le module `dorevia_cash_guard` reste le socle prudent de lecture et d'alerte de trésorerie.

Le module `dorevia_cash_simulation` ajoute un niveau d'hypothèse contrôlé.

| Module                    | Rôle                                                                  |
| ------------------------- | --------------------------------------------------------------------- |
| `dorevia_cash_guard`      | Projection prudente, basée sur les données réelles ou quasi certaines |
| `dorevia_cash_simulation` | Projection enrichie avec des hypothèses issues de devis               |

Un devis utilisé en simulation n'est pas :

* une facture ;
* une créance certaine ;
* une écriture comptable ;
* une preuve financière.

C'est uniquement une hypothèse de pilotage.

---

## 3. Dépendances fonctionnelles

Dépendances V1 :

```python
{
    "depends": [
        "sale_management",
        "dorevia_cash_guard",
    ],
}
```

Ces dépendances sont considérées comme nécessaires et suffisantes pour la V1.

---

## 4. Principe fonctionnel

Le module utilise les devis Odoo (`sale.order`) comme objets de simulation.

Un devis peut être marqué comme intégrable à la simulation de trésorerie.

Lorsque le mode simulation est désactivé dans Cash Guard, ces devis ne sont pas pris en compte.

Lorsque le mode simulation est activé, les devis éligibles sont ajoutés à la projection de trésorerie sous forme de flux futurs simulés.

Les flux simulés ne doivent jamais être confondus avec les flux réels issus de la comptabilité, des paiements ou des mouvements bancaires.

---

## 5. Champs proposés sur les devis

### 5.1 Inclusion dans la simulation

Ajouter un champ booléen sur `sale.order` :

```python
cash_simulation_ok = fields.Boolean(
    string="Inclure dans la simulation de trésorerie",
    default=False,
    tracking=True,
    help="Permet d'utiliser ce devis comme hypothèse d'encaissement futur dans Cash Guard lorsque le mode simulation est activé.",
)
```

Ce champ permet d'indiquer qu'un devis peut être utilisé comme hypothèse de trésorerie.

---

### 5.2 Date d'échéance de simulation

Ajouter un champ date dédié :

```python
cash_simulation_due_date = fields.Date(
    string="Date d'échéance simulation",
    tracking=True,
    help="Date prévisionnelle d'encaissement utilisée uniquement pour la simulation de trésorerie. Cette date est indépendante de la date de validité commerciale du devis.",
)
```

Cette date représente la date prévisionnelle d'encaissement simulé.

Elle est volontairement séparée des dates commerciales natives du devis, notamment `validity_date`, afin de ne pas détourner la logique standard Odoo.

---

## 6. Règles de validation à la saisie

Lorsqu'un utilisateur active la simulation sur un devis :

```text
cash_simulation_ok passe de False à True
```

alors :

```text
cash_simulation_due_date doit être renseignée
cash_simulation_due_date doit être strictement supérieure à la date du jour
```

Un devis ne peut donc pas être marqué comme simulation active sans date future.

En revanche, un devis déjà marqué simulation dont la date devient périmée avec le temps ne doit pas bloquer l'utilisateur au réveil du système ou à l'ouverture du devis.

Dans ce cas, il est simplement exclu automatiquement des calculs Cash Guard.

---

## 7. Règles d'éligibilité au calcul

Un devis est éligible à la simulation Cash Guard si toutes les conditions suivantes sont remplies :

* `cash_simulation_ok = True` ;
* `cash_simulation_due_date` est renseignée ;
* `cash_simulation_due_date` est strictement supérieure à la date du jour ;
* `state in ('draft', 'sent')` ;
* le devis appartient à la même société que la projection Cash Guard ;
* le devis n'a pas généré de facture ;
* la devise du devis est compatible avec la projection Cash Guard selon la règle V1 définie ci-dessous.

États éligibles V1 :

| État `sale.order.state` | Éligible simulation ? | Raison                                                            |
| ----------------------- | --------------------: | ----------------------------------------------------------------- |
| `draft`                 |                   Oui | Devis brouillon encore hypothétique                               |
| `sent`                  |                   Oui | Devis envoyé, encore non confirmé                                 |
| `sale`                  |                   Non | Commande confirmée, risque de double comptage avec les flux réels |
| `done`                  |                   Non | Commande verrouillée / cycle commercial avancé                    |
| `cancel`                |                   Non | Devis annulé                                                      |

---

## 8. Règle anti double comptage

Le module doit empêcher qu'un même flux soit compté à la fois comme simulation et comme flux réel.

Règle V1 :

```text
Un devis confirmé, verrouillé, annulé ou ayant au moins une facture liée n'est jamais intégré comme simulation.
```

Conséquences :

* si un devis passe en `state = 'sale'`, il est exclu de la simulation ;
* si un devis possède au moins une facture liée via `invoice_ids`, il est exclu de la simulation ;
* si la facture ouverte ou le flux réel est repris par `dorevia_cash_guard`, le devis ne doit plus apparaître comme ligne simulée.

Recommandation d'implémentation :

```text
Éligible simulation = state in ('draft', 'sent') and not invoice_ids
```

Le champ `cash_simulation_ok` peut rester coché pour mémoire, mais il ne donne plus lieu à une ligne simulée si les conditions d'éligibilité ne sont plus respectées.

Option future possible : désactiver automatiquement `cash_simulation_ok` lors de la confirmation du devis. Non requis en V1.

---

## 9. Mécanisme d'intégration avec Cash Guard

La V1 privilégie une intégration dynamique, non persistée.

Les devis simulés ne doivent pas générer de lignes `dorevia.cash.guard.line` matérialisées en base uniquement pour la simulation.

Règle V1 :

```text
Les lignes de simulation sont calculées à la volée lors du calcul ou de l'affichage de la projection Cash Guard.
```

Motivation :

* éviter les problèmes de synchronisation si le devis est modifié ;
* éviter les lignes obsolètes en base ;
* conserver une séparation claire entre flux réels persistés et hypothèses calculées ;
* faciliter l'activation / désactivation instantanée du mode simulation.

Recommandation technique :

Ajouter ou utiliser un point d'extension dans `dorevia_cash_guard`, par exemple :

```python
def _get_simulation_lines(self):
    """Return computed simulation lines for the current Cash Guard projection."""
    return []
```

Le module `dorevia_cash_simulation` surcharge cette méthode pour injecter les devis éligibles.

Si `dorevia.cash.guard.line` dispose déjà d'un `line_type = 'simulated'` ou équivalent, ce type peut être utilisé pour le rendu, mais sans obligation de persister ces lignes en base en V1.

### Limite V1 assumée — impact sur la grille de suivi

En V1, la simulation affecte la colonne **Projection** (`projected_balance`) et le **statut de risque** (`risk_status`) dans le suivi hebdomadaire Cash Guard.

En revanche, les colonnes **Entrées** (`inflow_amount`) et **Sorties** (`outflow_amount`) de la grille de suivi ne distinguent pas encore les montants simulés. Ces colonnes reflètent uniquement les flux complémentaires persistés et les factures ouvertes.

L'impact simulé est visible via :

* la colonne Projection (correcte, inclut les simulations) ;
* le smart button « X Simulations » ouvrant le détail des devis éligibles.

Évolution future possible : ventiler les montants simulés dans les colonnes Entrées / Sorties de la grille.

---

## 10. Localisation du mode simulation

Le mode simulation doit être porté par chaque projection Cash Guard.

Ajouter un champ booléen sur le modèle de projection Cash Guard, par exemple `dorevia.cash.guard` :

```python
include_simulation = fields.Boolean(
    string="Inclure les simulations commerciales",
    default=False,
    tracking=True,
    help="Lorsque cette option est activée, la projection inclut les devis éligibles marqués comme simulations de trésorerie.",
)
```

Règle produit :

```text
Le mode simulation est un choix de lecture par projection, pas un paramètre global société ni une préférence utilisateur.
```

Cela permet de comparer deux lectures :

* projection prudente sans simulation ;
* projection enrichie avec simulation.

---

## 11. Devise et multi-société

### 11.1 Multi-société

La V1 doit filtrer systématiquement sur la société.

Règle :

```text
Un devis simulé doit appartenir à la même société que la projection Cash Guard.
```

Aucun devis d'une autre société ne doit être intégré.

---

### 11.2 Devise

Pour la V1, la gestion multi-devise est volontairement limitée.

Règle V1 :

```text
Seuls les devis dont la devise correspond à la devise de la projection Cash Guard sont intégrés.
```

Aucune conversion automatique de devise n'est attendue en V1.

Les devis dans une autre devise sont exclus de la simulation.

Évolution future possible : conversion via taux de change à la date de simulation.

---

## 12. Conditions de paiement et échéancier

La V1 utilise un seul flux simulé par devis.

Règle V1 :

```text
Montant simulé = sale.order.amount_total
Date du flux simulé = sale.order.cash_simulation_due_date
Sens du flux = encaissement prévisionnel
```

Les conditions de paiement natives, les échéanciers 30/60/90 jours et les paiements fractionnés ne sont pas interprétés en V1.

Cette simplification est assumée.

Évolution future possible : éclatement du devis en plusieurs flux simulés selon les conditions de paiement.

---

## 13. Archivage des simulations périmées

En V1, le comportement attendu est l'exclusion automatique des calculs.

L'archivage automatique peut être prévu dans une version ultérieure via une tâche planifiée (`ir.cron`).

Règle V1 :

```text
Un devis de simulation dont la date d'échéance est dépassée n'est plus intégré dans Cash Guard.
```

Option future :

```text
Archiver automatiquement les devis de simulation périmés.
```

---

## 14. Affichage attendu dans Cash Guard

Les lignes simulées doivent être visibles et non ambiguës.

Exemple :

```text
Simulation — Devis SO024 — Client XYZ — +1 250,00 € — échéance 15/06/2026
```

Prévoir un badge ou libellé clair :

```text
Simulation
```

Une ligne simulée ne doit jamais pouvoir être confondue avec :

* une facture validée ;
* un paiement enregistré ;
* une écriture comptable ;
* un mouvement bancaire.

---

## 15. Droits d'accès

La V1 réutilise les droits du module `dorevia_cash_guard`.

Règle :

```text
Seuls les utilisateurs autorisés à utiliser Cash Guard peuvent activer le mode simulation dans Cash Guard.
```

Pour les devis :

```text
Seuls les utilisateurs autorisés à gérer les devis et disposant du droit Cash Guard peuvent marquer un devis comme simulation.
```

Implémentation possible selon les groupes existants :

* réutiliser le groupe fonctionnel de `dorevia_cash_guard` s'il existe ;
* sinon, utiliser a minima `account.group_account_user` ou un groupe dédié à définir dans `dorevia_cash_guard`.

À ne pas faire : laisser l'activation de simulation ouverte à tout utilisateur commercial sans visibilité sur Cash Guard.

---

## 16. Traçabilité

Les champs suivants doivent être tracés dans le chatter si les modèles héritent de `mail.thread` :

* `sale.order.cash_simulation_ok` ;
* `sale.order.cash_simulation_due_date` ;
* `dorevia.cash.guard.include_simulation`.

Objectif : conserver une trace lisible des décisions de simulation.

Aucun journal comptable ni écriture financière ne doit être créé par cette traçabilité.

---

## 17. Contraintes importantes

Le module ne doit pas :

* générer automatiquement de facture ;
* créer d'écriture comptable ;
* modifier la logique native de confirmation des devis ;
* modifier les règles de facturation Odoo ;
* mélanger les lignes simulées avec les flux réels sans distinction visuelle ;
* permettre un double comptage entre devis simulé et flux réel.

---

## 18. Critères de recette V1

Le module sera considéré conforme si :

* un devis en état `draft` ou `sent` peut être marqué comme simulation de trésorerie ;
* une date d'échéance de simulation peut être renseignée ;
* Odoo empêche l'activation d'une simulation sans date future ;
* un devis de simulation périmé est exclu du calcul ;
* un devis confirmé (`state = 'sale'`) n'est plus intégré comme simulation ;
* un devis facturé ou possédant au moins une facture liée n'est plus intégré comme simulation ;
* Cash Guard fonctionne normalement lorsque le mode simulation est désactivé ;
* Cash Guard intègre les devis éligibles lorsque le mode simulation est activé ;
* le mode simulation est porté par la projection Cash Guard, et non par un paramètre global ;
* les lignes simulées sont calculées dynamiquement, sans création obligatoire de lignes persistées en base ;
* les lignes simulées sont clairement distinguées des lignes réelles ;
* les devis d'une autre société sont exclus ;
* les devis dans une devise différente de la projection sont exclus en V1 ;
* aucune facture n'est créée automatiquement ;
* aucune écriture comptable n'est créée ;
* le comportement reste compatible avec le module `dorevia_cash_guard` existant.

---

## 19. Doctrine produit

La séparation produit doit rester claire :

```text
dorevia_cash_guard = réel / prudent / garde-fou

dorevia_cash_simulation = hypothèses / scénarios / projection
```

La simulation aide à décider, mais elle ne constitue pas une preuve.

Elle permet d'éclairer une situation future possible, sans altérer la comptabilité ni la trésorerie réelle.

---

## 20. Périmètre futur possible

Évolutions envisageables après la V1 :

* simulation de sorties de trésorerie ;
* intégration de dépenses prévues ;
* scénarios multiples ;
* comparaison scénario prudent / scénario optimiste ;
* archivage automatique des simulations périmées ;
* tableau de synthèse des impacts simulés ;
* conversion multi-devise ;
* éclatement selon conditions de paiement ;
* historisation des simulations utilisées dans une décision.

Ces évolutions ne font pas partie du périmètre initial V1.
