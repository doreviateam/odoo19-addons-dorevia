# dorevia_glc_analytics — Suivi d'activité GLC

Module Odoo 19 CE — **Pilotage analytique associatif** pour GLC (Saint-Aignan-de-Grand-Lieu).

> Passer d'une lecture comptable analytique partielle à une **lecture de gestion par activité** : dépenses directes, salaires ventilés, bénévolat et coût complet.

## État des paliers (MOA)

| Palier | Version intro | Statut |
|---|---|---|
| 0 — Socle analytique | `19.0.1.0.0` | Validé MOA |
| 1 — Anomalies analytiques | `19.0.2.0.0` | Validé MOA |
| 2 — Ventilation salariale | `19.0.3.0.0` | Validé MOA · **gelé** |

**Version courante :** `19.0.3.1.0` (renommage technique du module).

**Suite MOA :** Palier 3 — module `dorevia_glc_budget` (budget prévisionnel) → Palier 4 — cockpit couverture des salaires.  
Voir [cadrage Budget & Cockpit](./docs/CADRAGE_BUDGET_COCKPIT.md) · [ticket Palier 3](./docs/TICKET_PALIER_3.md) · [PALIERS.md](./docs/PALIERS.md).

## Renommage module (`19.0.3.1.0`)

Le module technique a été renommé :

```text
dorevia_glc_analytique  →  dorevia_glc_analytics
```

Sur une base où **`dorevia_glc_analytique` est encore installé** (déploiement du nouveau code sans migration SQL manuelle) :

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d <base> -i dorevia_glc_analytics --stop-after-init --no-http
```

Le `pre_init_hook` renomme alors `ir_module_module`, `ir_module_module_dependency`, `ir_model_data` et les clés `ir.config_parameter`.

Sur une base **déjà migrée** sous `dorevia_glc_analytics`, mettre à jour normalement :

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d <base> -u dorevia_glc_analytics --stop-after-init --no-http

docker compose restart odoo
```

Le script `migrations/19.0.3.1.0/pre-migrate.py` reprend la même logique lors d'un `-u`.

## Documentation

| Document | Description |
|---|---|
| [Spécification fonctionnelle V1.1](./docs/README.md) | Cahier des charges complet (cible) |
| [Cadrage Budget & Cockpit](./docs/CADRAGE_BUDGET_COCKPIT.md) | Roadmap post-Palier 2 |
| [Ticket Palier 3 — Budget](./docs/TICKET_PALIER_3.md) | Module `dorevia_glc_budget` |
| [Ticket Palier 4 — Cockpit](./docs/TICKET_PALIER_4.md) | Couverture des salaires |
| [Recette manuelle Palier 0](./docs/RECETTE_MANUELLE_PALIER_0.md) | Socle analytique |
| [Recette manuelle Palier 1](./docs/RECETTE_MANUELLE_PALIER_1.md) | Anomalies analytiques |
| [Recette manuelle Palier 2](./docs/RECETTE_MANUELLE_PALIER_2.md) | Ventilation salariale |
| [Découpage en paliers](./docs/PALIERS.md) | Roadmap |
| [Règles d'affectation](./docs/REGLES_AFFECTATION.md) | Matrice double axe |
| [Matrice de migration](./docs/MATRICE_MIGRATION.md) | Ancien plan → plan cible |

## Dépendances

```text
account
analytic
hr
```

## Tests automatisés

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d glc-rgl-test-import -u dorevia_glc_analytics \
  --test-enable --test-tags=/dorevia_glc_analytics --stop-after-init --no-http
```
