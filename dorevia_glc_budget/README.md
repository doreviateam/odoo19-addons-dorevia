# dorevia_glc_budget — Budget prévisionnel GLC

Module Odoo 19 CE — **Budget prévisionnel mensuel** par axe analytique GLC (Palier 3).

> Overlay de gestion uniquement : **aucune écriture comptable** ni **analytique**.

## Périmètre Palier 3

| Élément | Détail |
|---|---|
| Modèles | `glc.budget`, `glc.budget.line` |
| Scénarios | `initial`, `revised`, `landing` |
| Types de ligne | `revenue`, `expense`, `funding` |
| Workflow | brouillon → validé → archivé |
| Menu | Comptabilité → **Pilotage GLC** → Budgets prévisionnels |

## Dépendances

```text
dorevia_glc_analytics
```

Pas d'OCA Budget.

## Documentation

| Document | Description |
|---|---|
| [Ticket Palier 3](../dorevia_glc_analytics/docs/TICKET_PALIER_3.md) | Spécification MOA |
| [Recette manuelle Palier 3](./docs/RECETTE_MANUELLE_PALIER_3.md) | Scénario MOA |
| [Cadrage Budget & Cockpit](../dorevia_glc_analytics/docs/CADRAGE_BUDGET_COCKPIT.md) | Vision Palier 4 |

## Tests automatisés

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d glc-rgl-test-import -i dorevia_glc_budget \
  --test-enable --test-tags=/dorevia_glc_budget --stop-after-init --no-http
```

## Version

**Palier 3** — `19.0.1.0.0`
