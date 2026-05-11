# PV de recette fonctionnelle — `dorevia_cash_simulation` V1

## 1. Objet

Procès-verbal de recette du module `dorevia_cash_simulation` pour Odoo 19 CE.

Ce document acte la recette V1 de l'intégration des devis clients marqués en simulation dans une projection Cash Guard, selon le plan de recette :

- `docs/PLAN_RECETTE_V1.md`

Objectif validé :

```text
Les devis marqués en simulation enrichissent la projection Cash Guard uniquement
en mode simulation ON, sans double comptage, sans facture générée automatiquement,
sans écriture comptable automatique, et sans impact parasite en mode simulation OFF.
```

---

## 2. Environnement de recette

| Élément | Valeur |
| ------- | ------ |
| Date de recette | 2026-05-12 |
| URL | `http://localhost:18079` |
| Base | `tenant_o8` |
| Version Odoo | `19.0-20260324` |
| Module | `dorevia_cash_simulation` |
| Module parent | `dorevia_cash_guard` |
| Branche | `feature/shop-mvp22-visible-wave1` |
| Commit de référence | `0b30001a7a2fd46ad294191e74a59f4c6495af6e` |
| Société | `My Company` |
| Devise société | EUR |
| Projection de recette | `RECETTE CASH SIM 20260512-013` |
| ID projection | `1224` |

Note d'environnement :

- La date système Odoo observée pendant les scripts de recette était `2026-05-11`.
- La session utilisateur / poste de recette était en date locale Europe/Paris `2026-05-12`.

---

## 3. Tests automatisés

Commande exécutée :

```bash
docker exec sandbox-odoo19-odoo-1 odoo server \
  -c /etc/odoo/odoo.conf \
  -d tenant_o8 \
  -u dorevia_cash_simulation \
  --test-enable \
  --test-tags /dorevia_cash_simulation \
  --stop-after-init \
  --http-port=18080 \
  --gevent-port=18081 \
  --log-level=test
```

Résultat :

```text
0 failed, 0 error(s) of 19 tests when loading database 'tenant_o8'
```

Statut : **OK**

---

## 4. Jeu de données de recette

Préfixe de recette :

```text
RECETTE CASH SIM 20260512-013
```

Projection Cash Guard :

```text
RECETTE CASH SIM 20260512-013
```

Devis principaux :

| Réf. | État testé | Simulation OK | Date simulation | Montant TTC | Résultat constaté |
| ---- | ---------- | ------------: | --------------- | ----------: | ----------------- |
| D1 | Brouillon | Oui | Future | 1 000,00 € | Inclus en simulation ON |
| D2 | Envoyé | Oui | Future | 2 000,00 € | Inclus en simulation ON |
| D3 | Brouillon | Non | Future | 3 000,00 € | Exclu |
| D4 | Brouillon | Oui | Date passée | 4 000,00 € | Refusé par validation |
| D5 | Brouillon puis confirmé | Oui | Future | 5 000,00 € | Inclus puis exclu après confirmation |

Jeux complémentaires utilisés :

| Réf. | Objet |
| ---- | ----- |
| `NO_DATE` | Validation date obligatoire |
| `TODAY_OR_PAST` | Validation date future stricte |
| `STALE` | Date devenue périmée |
| `STALE_UNRELATED` | Écriture non liée sur devis périmé |
| `D6_INVOICE_LINK` | Exclusion après facture liée brouillon |
| `USD` | Exclusion devise différente |

---

## 5. Résultats fonctionnels

### 5.1 Synthèse

Verdict : **GO V1**

Résultat :

```text
15 OK
0 KO
1 N/A
```

Le point `N/A` concerne le test multi-société : la base `tenant_o8` ne contient qu'une société exploitable pour ce scénario.

### 5.2 Grille de recette

| Zone testée | Statut | Résultat constaté |
| ----------- | :----: | ----------------- |
| Installation module | OK | Module `dorevia_cash_simulation` installé |
| Tests automatisés | OK | 19 tests verts, 0 échec, 0 erreur |
| Simulation OFF | OK | Aucun devis simulé inclus ; smart count = 0 |
| Simulation ON | OK | D1 + D2 inclus ; delta projection = +3 000,00 € |
| Smart button | OK | Bouton `2 Simulations`, liste D1 + D2 uniquement |
| Date absente | OK | Blocage Odoo à l'activation simulation |
| Date aujourd'hui / passée | OK | Blocage Odoo si champ simulation touché |
| Date devenue périmée | OK | Modification de date simulation vers le passé bloquée |
| Écriture non liée sur devis périmé | OK | Pas de blocage si aucun champ simulation n'est touché |
| Devis confirmé | OK | D5 exclu après confirmation, retrait de 5 000,00 € |
| Devis facturé | OK | Devis exclu dès facture brouillon liée |
| Multi-société | N/A | Non testé : `tenant_o8` mono-société |
| Devise différente | OK | Devis USD exclu de la projection EUR |
| Aucun effet comptable automatique | OK | Aucune facture, paiement ou ligne bancaire créée automatiquement par les devis simulés |
| Retour simulation OFF | OK | Projection prudente retrouvée |

---

## 6. Preuves et constats détaillés

### 6.1 Simulation OFF

État constaté :

```text
include_simulation = False
net simulation = 0,00 €
simulation_order_count = 0
forecast_final_balance = 1 320,67 €
risk_status = tension
```

Statut : **OK**

### 6.2 Simulation ON — D1 + D2

État constaté :

```text
include_simulation = True
D1 = +1 000,00 €
D2 = +2 000,00 €
D3 exclu
delta projection = +3 000,00 €
forecast_final_balance = 4 320,67 €
risk_status = safe
```

Comparaison :

| Indicateur | Simulation OFF | Simulation ON |
| ---------- | -------------: | ------------: |
| Projection finale | 1 320,67 € | 4 320,67 € |
| Delta | | +3 000,00 € |
| Statut de risque | Tension | Confort |

Statut : **OK**

### 6.3 Limite V1 confirmée

Constat conforme au plan :

```text
projected_balance et risk_status changent.
inflow_amount / outflow_amount restent à 0,00 € en V1.
```

Cette limite est acceptée pour la V1 : les simulations impactent la trajectoire de projection, mais ne sont pas encore ventilées dans les colonnes d'entrées / sorties.

Statut : **OK**

### 6.4 Smart button

Contrôle en base et dans l'interface Odoo :

```text
Bouton affiché : 2 Simulations
Liste ouverte : D1 et D2 uniquement
```

Devis exclus de la liste :

```text
D3 : non marqué simulation
D4 : date passée refusée
D5 : confirmé
D6_INVOICE_LINK : facture liée
USD : devise différente
```

Statut : **OK**

### 6.5 Validations de date

Messages de blocage constatés :

```text
Le devis « ... » ne peut pas être inclus dans la simulation sans date d'échéance de simulation.
```

```text
Le devis « ... » : la date d'échéance de simulation doit être postérieure à aujourd'hui.
```

Statut : **OK**

### 6.6 Exclusion après confirmation

Scénario D5 :

```text
Avant confirmation : D5 inclus en simulation
Après confirmation : state = sale
D5 exclu de la simulation
Retrait constaté : 5 000,00 €
```

Statut : **OK**

### 6.7 Exclusion après facture liée

Scénario `D6_INVOICE_LINK` :

```text
Facture brouillon liée créée volontairement pour le test.
Le devis est exclu dès existence de la facture liée.
```

Statut : **OK**

### 6.8 Devise différente

Scénario `USD` :

```text
Devis simulé en USD
Projection Cash Guard en EUR
Résultat : devis exclu
```

Statut : **OK**

### 6.9 Aucun effet comptable automatique

Avant création volontaire de la facture liée du test 7, aucun effet comptable automatique n'a été constaté :

```text
Aucune facture automatique
Aucune écriture de paiement automatique
Aucune ligne bancaire automatique
```

Statut : **OK**

---

## 7. Contrôle visuel Odoo

Fiche Cash Guard contrôlée dans l'interface :

```text
RECETTE CASH SIM 20260512-013
```

État visuel final laissé pour contrôle :

```text
include_simulation = True
Smart button = 2 Simulations
Projection finale = 4 320,67 €
Statut de risque = Confort
```

Ouverture du smart button :

```text
Devis en simulation
S00156 — 2 000,00 €
S00155 — 1 000,00 €
```

Statut : **OK**

---

## 8. Réserves et limites

### 8.1 Réserves bloquantes

Aucune réserve bloquante ouverte.

### 8.2 Limites V1 assumées

| Limite | Statut |
| ------ | ------ |
| Les simulations impactent `projected_balance` et `risk_status`, pas encore `inflow_amount` / `outflow_amount` | Accepté V1 |
| Le test multi-société n'a pas été exécuté sur `tenant_o8` | N/A, base mono-société |

### 8.3 Point de vigilance

Le smart button liste tous les devis éligibles de la société et de la devise de la projection. Des jeux de recette précédents restés actifs peuvent donc apparaître si leurs devis sont encore marqués `cash_simulation_ok=True`.

Action effectuée pendant la recette :

```text
Neutralisation des anciens jeux RECETTE CASH SIM 20260512-* avant le run final.
```

---

## 9. Décision

Décision : **GO V1**

Justification :

- Simulation OFF exclut les devis simulés.
- Simulation ON inclut uniquement les devis éligibles.
- D1 + D2 ajoutent exactement 3 000,00 € à la projection.
- Le statut de risque est recalculé avec la trajectoire simulée.
- Les devis confirmés ou facturés sont exclus.
- Les devis en devise différente sont exclus.
- Aucun flux comptable réel n'est créé automatiquement par la simulation.
- Le smart button expose uniquement les devis éligibles attendus.

Conclusion :

```text
dorevia_cash_simulation V1 est validé en recette fonctionnelle sur tenant_o8.
```

---

## 10. Signature / validation

| Rôle | Nom | Statut |
| ---- | --- | ------ |
| Recette fonctionnelle | Codex / Dorevia | Validé |
| Validation produit | À compléter | À compléter |
| Validation technique | À compléter | À compléter |

Date d'acte :

```text
2026-05-12
```

Statut final :

```text
Dorevia Cash Simulation V1 — GO
```
