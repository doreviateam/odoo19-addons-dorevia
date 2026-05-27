# Recette manuelle — Cockpit couverture des salaires · Palier 4

**Module :** `dorevia_glc_analytics` (extension Palier 4)  
**Version cible :** `19.0.4.0.0`  
**Prérequis :** `dorevia_glc_analytics` + `dorevia_glc_budget` installés (Paliers 0–3 gelés MOA)  
**Références :** [CADRAGE_FINAL_PALIER_4.md](./CADRAGE_FINAL_PALIER_4.md) · [TICKET_PALIER_4.md](./TICKET_PALIER_4.md)

**Statut document :** **Brouillon** — à compléter en recette MOA post-développement.

---

## Contexte

```text
URL  : http://localhost:18079
Base : glc-rgl-test-import
Menu : Comptabilité → Pilotage GLC → Cockpit couverture des salaires
```

---

## Prérequis

- Budget Palier 3 validé (scénario `initial` 2026 ou année de recette)
- Ventilations salariales Palier 2 `validated` / `locked` sur la période
- Écritures analytiques de recette (BAR, SUBVENTIONS, STRUCTURE, etc.)

---

## Parcours nominal (brouillon)

| Pas | Action | Contrôle attendu |
|---|---|---|
| P4.1 | Ouvrir le cockpit | Formulaire avec filtres société / année / mois / activité / scénario budget |
| P4.2 | Sélectionner année + mois + scénario `initial` | Filtres enregistrés |
| P4.3 | Cliquer **Actualiser** | KPI ressources / masse salariale / frais généraux calculés |
| P4.4 | Vérifier bandeau alerte | Rouge / orange / vert cohérent avec les montants |
| P4.5 | Onglet **Détail Activité × Mois** | Lignes par compte analytique et mois |
| P4.6 | Vérifier masse salariale | Agrégat ventilations Palier 2 — pas double comptage RH historique |

---

## Tests automatisés

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d glc-rgl-test-import -u dorevia_glc_analytics,dorevia_glc_budget \
  --test-enable --test-tags=/dorevia_glc_analytics,/dorevia_glc_budget \
  --stop-after-init --no-http
```

| Résultat attendu | Résultat recette |
|---|---|
| Tests `/dorevia_glc_analytics` (dont cockpit) | **42 post-tests, 0 échec** |
| Tests `/dorevia_glc_budget` | **14 post-tests, 0 échec** |

---

## Critères MOA (brouillon)

- [ ] CA1 — Prévisionnel lu depuis `glc.budget.line` (budget validé/archivé)
- [ ] CA2 — Réalisé analytique lu depuis `account.analytic.line` (hors masse salariale)
- [ ] CA3 — Masse salariale depuis ventilations Palier 2 `validated`/`locked`
- [ ] CA4 — Pas de double comptage RH
- [ ] CA5 — Exclusion flux bilan / trésorerie
- [ ] CA6 — Alertes rouge / orange / vert
- [ ] CA7 — Filtres société / année / mois / activité
- [ ] CA8 — Aucune modification fonctionnelle de `dorevia_glc_budget`
