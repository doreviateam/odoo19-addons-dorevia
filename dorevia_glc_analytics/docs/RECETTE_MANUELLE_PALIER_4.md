# Recette manuelle — Cockpit couverture des salaires · Palier 4

**Module :** `dorevia_glc_analytics` (extension Palier 4)  
**Version cible :** `19.0.4.0.0`  
**Prérequis :** `dorevia_glc_analytics` + `dorevia_glc_budget` installés (Paliers 0–3 gelés MOA)  
**Références :** [CADRAGE_FINAL_PALIER_4.md](./CADRAGE_FINAL_PALIER_4.md) · [TICKET_PALIER_4.md](./TICKET_PALIER_4.md) · [PR #33](https://github.com/doreviateam/odoo19-addons-dorevia/pull/33)

**Statut document :** **Validé MOA** — recette exécutée sur `glc-rgl-test-import` (2026-05-27)

---

## Contexte de recette

```text
URL  : http://localhost:18079
Base : glc-rgl-test-import
Branche : feat/glc-cockpit-palier-4 (PR #33 — non mergée)
Menu : Comptabilité → Pilotage GLC → Cockpit couverture des salaires
```

---

## Prérequis installation

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d glc-rgl-test-import -u dorevia_glc_analytics \
  --stop-after-init --no-http

docker compose restart odoo
```

---

## Parcours nominal P4.1–P4.6

| Pas | Action | Contrôle attendu | OK | Observations |
|---|---|---|---|---|
| P4.1 | Menu **Cockpit couverture des salaires** | Accès Utilisateur GLC | ☑ | |
| P4.2 | Filtres société / année / mois / activité / scénario budget | Filtres opérationnels | ☑ | |
| P4.3 | **Actualiser** — KPI ressources / masse salariale / frais généraux | Montants cohérents | ☑ | |
| P4.4 | Bandeau alerte | Rouge / orange / vert cohérents | ☑ | |
| P4.5 | Onglet **Détail Activité × Mois** | Lignes par compte et mois | ☑ | |
| P4.6 | Masse salariale | Ventilations Palier 2 `validated`/`locked` uniquement | ☑ | Pas de double comptage RH |

---

## Contrôles complémentaires (shell / recette MOA)

| Contrôle | Résultat |
|---|---|
| Masse salariale = ventilations Palier 2 `validated` + `locked` | OK |
| Pas de double comptage avec écriture analytique paie `641` | OK |
| Exclusion flux bilan / trésorerie (`164`) | OK |
| Aucun effet fonctionnel sur `dorevia_glc_budget` au refresh cockpit | OK |
| Module budget non modifié (PR #33) | OK |

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
| Tests `/dorevia_glc_analytics` (dont cockpit) | **42 post-tests, 0 échec, 0 erreur** |
| Tests `/dorevia_glc_budget` | **14 post-tests, 0 échec, 0 erreur** |
| **Total** | **46 post-tests, vert** |

---

## Critères MOA

- [x] CA1 — Prévisionnel lu depuis `glc.budget.line` (budget validé/archivé)
- [x] CA2 — Réalisé analytique lu depuis `account.analytic.line` (hors masse salariale)
- [x] CA3 — Masse salariale depuis ventilations Palier 2 `validated`/`locked`
- [x] CA4 — Pas de double comptage RH
- [x] CA5 — Exclusion flux bilan / trésorerie
- [x] CA6 — Alertes rouge / orange / vert
- [x] CA7 — Filtres société / année / mois / activité
- [x] CA8 — Aucune modification fonctionnelle de `dorevia_glc_budget`

---

## Clôture recette — `glc-rgl-test-import` (2026-05-27)

| Contrôle | Résultat |
|---|---|
| Parcours P4.1–P4.6 | OK |
| Tests automatisés (46) | OK |
| Invariants I1–I7 | OK |
| PR #33 | **Mergée** — Palier 4 **gelé MOA** (`19.0.4.0.0`) |

### Points de vigilance (non bloquants)

- Warning Odoo connu sur le domaine multi-société de `glc.salary.allocation.line.activity_account_id` — sans impact recette Palier 4.
- Fichier non suivi `dorevia_ckreyol_marketone/...` — hors périmètre GLC.

### Suite immédiate

- Palier 4 **gelé MOA** sur `main`.
- Palier 4bis / **période libre** : [Recette manuelle période libre](./recette/RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md).
- Palier 5 : enrichissements cockpit (hors périmètre immédiat).
