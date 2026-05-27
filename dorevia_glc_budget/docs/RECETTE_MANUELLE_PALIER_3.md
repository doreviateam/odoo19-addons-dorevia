# Recette manuelle — dorevia_glc_budget · Palier 3

**Module :** `dorevia_glc_budget`  
**Version cible :** `19.0.1.0.0`  
**Prérequis :** `dorevia_glc_analytics` installé (Paliers 0–2 gelés MOA)  
**Références :** [TICKET_PALIER_3.md](../dorevia_glc_analytics/docs/TICKET_PALIER_3.md)

**Hors périmètre :** cockpit, alertes, exports, trésorerie, OCA Budget, écritures comptables/analytiques.

**Statut document :** **Validé MOA** — recette exécutée sur `glc-rgl-test-import` (2026-05-27).

---

## Contexte de recette

```text
URL  : http://localhost:18079
Base : glc-rgl-test-import
Module : dorevia_glc_budget (Palier 3)
Version : 19.0.1.0.0
```

---

## Prérequis installation

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d glc-rgl-test-import -i dorevia_glc_budget --stop-after-init --no-http

docker compose restart odoo
```

---

## Jeu de données de test

| Jeu | Description | Contrôle attendu |
|---|---|---|
| B1 | Budget 2026 scénario `initial` | Création OK |
| B2 | Ligne charge STRUCTURE avril | Type `expense` + plan Activités |
| B3 | Ligne recette BAR avril | Type `revenue` |
| B4 | Ligne financement SUBVENTIONS avril | Type `funding` + plan Financements |
| B5 | Compte SUBVENTIONS en charge | Refus contrainte |
| B6 | Validation budget | Lignes en lecture seule |
| B7 | Archivage | Statut `archived` |

---

## Parcours nominal

| Pas | Action | Contrôles | OK | Observations |
|---|---|---|---|---|
| P3.1 | Apps → **Dorevia GLC Budget** | Module installé | ☑ | |
| P3.2 | Menu **Budgets prévisionnels** | Accès Utilisateur GLC | ☑ | |
| P3.3 | Créer budget B1 + lignes B2–B4 | Montants enregistrés | ☑ | |
| P3.4 | Tenter B5 (SUBVENTIONS en charge) | Message d'erreur | ☑ | |
| P3.5 | Valider budget | État **Validé** | ☑ | |
| P3.6 | Tenter ajout ligne | Refus | ☑ | |
| P3.7 | Archiver | État **Archivé** | ☑ | |
| P3.8 | Vérifier comptabilité | Aucune nouvelle écriture | ☑ | |

---

## Tests automatisés

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d glc-rgl-test-import -u dorevia_glc_budget \
  --test-enable --test-tags=/dorevia_glc_budget --stop-after-init --no-http
```

| Résultat attendu | Résultat recette |
|---|---|
| Tests `/dorevia_glc_budget` | **12 post-tests, 0 échec, 0 erreur** |
| Non-régression `/dorevia_glc_analytics` | **25 post-tests, 0 échec, 0 erreur** |

---

## Critères MOA

- [x] CA1 — Module installable sans OCA Budget
- [x] CA2 — Scénarios `initial` / `revised` / `landing`
- [x] CA3 — Lignes mensuelles par axe analytique
- [x] CA4 — Types recette / charge / financement
- [x] CA5 — Refus Financements sur recette/charge
- [x] CA6 — Refus Activités sur financement
- [x] CA7 — Workflow brouillon → validé → archivé
- [x] CA8 — Aucune écriture comptable ni analytique

---

## Clôture recette — `glc-rgl-test-import` (2026-05-27)

| Contrôle | Résultat |
|---|---|
| Installation `dorevia_glc_budget` | OK |
| Redémarrage Odoo | OK |
| Tests automatisés `/dorevia_glc_budget` | **12 post-tests, 0 échec, 0 erreur** |
| Non-régression `/dorevia_glc_analytics` | **25 post-tests, 0 échec, 0 erreur** |
| Parcours P3.1–P3.8 (shell + contrôles métier) | OK |
| Budget 2026 scénario `initial` | OK |
| Lignes charge / recette / financement | OK |
| Refus `SUBVENTIONS` en charge | OK |
| Validation budget | OK |
| Refus ajout ligne post-validation | OK |
| Archivage | OK |
| Aucune écriture `account.move` / `account.analytic.line` | OK |

### Points de vigilance (non bloquants)

- Warnings modules OCA incompatibles dans les logs Docker — sans impact sur le périmètre GLC Budget.
- Erreurs SQL de contraintes d'unicité visibles pendant les tests automatisés — **attendues** (tests `test_unique_budget_*`) ; la suite termine en vert.

### Suite immédiate

- Palier 3 **validé MOA** — prêt pour merge **PR #28** et gel Palier 3.
- **Palier 4 cockpit** : hors périmètre jusqu'au gel MOA Palier 3 post-merge.
