# Release note — Jalon GLC Paliers 0–4


> **Document historique** — ne décrit plus le produit installé depuis **`19.0.13.0.0`** / **`19.0.14.0.0`**. État actuel : [ETAT_MODULE_ACTUEL.md](./ETAT_MODULE_ACTUEL.md).

---

**Date de jalon :** 2026-05-27  
**Base de recette :** `glc-rgl-test-import`  
**Verdict MOA :** **Jalon Paliers 0–4 terminé proprement** — socle stable, gelé

---

## 1. Synthèse métier

La chaîne de pilotage GLC est opérationnelle de bout en bout :

```text
Réalisé analytique     → account.analytic.line
Budget prévisionnel    → glc.budget.line
Masse salariale fiable → ventilations Palier 2 (validated / locked)
Cockpit soutenabilité  → couverture salaires, frais généraux, alertes rouge / orange / vert
```

**Question métier couverte :**

> Est-ce que les recettes d'activité et les financements couvrent les salaires, puis les frais généraux ?

Menu cockpit : **Facturation → Pilotage GLC → Contrôle de gestion**

---

## 2. Modules livrés

| Module | Version | Paliers | Statut MOA |
|---|---|---|---|
| `dorevia_glc_analytics` | **`19.0.4.0.0`** | 0, 1, 2, **4** | **Validé MOA · gelé** |
| *(budget retiré)* | — | 3 | **Validé MOA · gelé** |

### Contenu par palier

| Palier | Module | Livrable principal |
|---|---|---|
| **0** | `dorevia_glc_analytics` | Plans Activités / Financements, comptes GLC, sécurité de base |
| **1** | `dorevia_glc_analytics` | Assistant anomalies analytiques (A1–A6), règles financement A3 |
| **2** | `dorevia_glc_analytics` | Coûts salariés, ventilations `percent` / `hours`, overlay sans écriture comptable |
| **3** | `dorevia_glc_budget` | Budget prévisionnel mensuel par axe (`initial` / `revised` / `landing`) |
| **4** | `dorevia_glc_analytics` | Contrôle de gestion, KPI, alertes, détail Activité × Mois |

---

## 3. Décisions MOA (jalon)

| Date | Décision | Référence |
|---|---|---|
| 2026-05-27 | Audit officiel Paliers 0–3 — GO avec réserves légères | [AUDIT_GLC_ANALYTICS_BUDGET_AVANT_PALIER_4.md](./AUDIT_GLC_ANALYTICS_BUDGET_AVANT_PALIER_4.md) · PR #29 |
| 2026-05-27 | Maintenance P2 pré-Palier 4 (robustesse, tests) | PR #30 |
| 2026-05-27 | Règle RH / Personnel cockpit figée | PR #31 |
| 2026-05-27 | Cadrage final Palier 4 — invariants I1–I7 validés (Option A) | [CADRAGE_FINAL_PALIER_4.md](./CADRAGE_FINAL_PALIER_4.md) · PR #32 |
| 2026-05-27 | GO développement cockpit (G7) | Branche `feat/glc-cockpit-palier-4` |
| 2026-05-27 | Recette Palier 4 P4.1–P4.6 validée | [RECETTE_MANUELLE_PALIER_4.md](./RECETTE_MANUELLE_PALIER_4.md) |
| 2026-05-27 | **Merge et gel Palier 4** | PR #33 |

### Invariants structurants (Palier 4)

| # | Règle |
|---|---|
| I1 | Prévisionnel = `glc.budget.line` (lecture seule Palier 3) |
| I2 | Réalisé analytique = `account.analytic.line` (hors masse salariale) |
| I3 | Masse salariale = ventilations Palier 2 `validated` / `locked` |
| I4 | Pas de double comptage RH |
| I5 | Exclusion flux bilan / trésorerie |
| I6 | Alertes rouge / orange / vert |
| I7 | Aucune évolution fonctionnelle de `dorevia_glc_budget` dans le Palier 4 |

---

## 4. Pull requests mergées (jalon)

| PR | Objet |
|---|---|
| [#25](https://github.com/doreviateam/odoo19-addons-dorevia/pull/25) | Palier 1 — anomalies analytiques |
| [#26](https://github.com/doreviateam/odoo19-addons-dorevia/pull/26) | Palier 2 — ventilation salariale |
| [#27](https://github.com/doreviateam/odoo19-addons-dorevia/pull/27) | Renommage `dorevia_glc_analytics` |
| [#28](https://github.com/doreviateam/odoo19-addons-dorevia/pull/28) | Palier 3 — `dorevia_glc_budget` |
| [#29](https://github.com/doreviateam/odoo19-addons-dorevia/pull/29) | Audit officiel Paliers 0–3 |
| [#30](https://github.com/doreviateam/odoo19-addons-dorevia/pull/30) | Maintenance P2 pré-Palier 4 |
| [#31](https://github.com/doreviateam/odoo19-addons-dorevia/pull/31) | Règle RH Palier 4 |
| [#32](https://github.com/doreviateam/odoo19-addons-dorevia/pull/32) | Cadrage final Palier 4 |
| [#33](https://github.com/doreviateam/odoo19-addons-dorevia/pull/33) | **Palier 4 — cockpit** |

---

## 5. Tests automatisés (recette)

Base : `glc-rgl-test-import`

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d glc-rgl-test-import -u dorevia_glc_analytics \
  --test-enable --test-tags=/dorevia_glc_analytics \
  --stop-after-init --no-http
```

| Suite | Résultat jalon |
|---|---|
| `/dorevia_glc_analytics` | **42 tests, 0 échec** |
| `/dorevia_glc_analytics` | **14 tests, 0 échec** |
| **Total** | **46 post-tests, vert** |

---

## 6. Limites connues (non bloquantes jalon)

| Sujet | Détail | Impact |
|---|---|---|
| Warning multi-société | Domaine `glc.salary.allocation.line.activity_account_id` — warning Odoo connu au chargement des vues | **Non bloquant** — recette P2 et P4 OK |
| RH historique pré-bascule | Mois antérieurs à la bascule Palier 2 : règle MOA à confirmer si lecture historique `account.analytic.line` requise | Hors V1 cockpit (post-bascule = ventilations) |
| Budget RH sur STRUCTURE | Le prévisionnel RH peut être saisi sur l'axe STRUCTURE en recette Palier 3 — séparation RH / frais généraux en budget à discipliner en saisie MOA | Variance budget cockpit, pas d'erreur technique |
| Pas d'écriture auto | *(retiré — ventilations)* et budgets restent des **overlays de gestion** — aucune génération comptable/analytique à la validation | Doctrine voulue |
| OCA Budget | Non retenu — module GLC dédié | Hors périmètre |

---

## 7. Hors périmètre jalon — Palier 5 (pause MOA)

Palier 5 **en pause courte** — à cadrer ultérieurement :

- graphiques avancés multi-scénarios ;
- comparaison budget initial / révisé / atterrissage dans le cockpit ;
- exports Excel / PDF ;
- commentaires de gestion par mois ;
- projections fin d'année ;
- bloc trésorerie ;
- intégration OCA Budget.

Éléments spec V1.1 reportés (cf. [PALIERS.md](./PALIERS.md)) :

- registre bénévole ;
- rapport CA mensuel PDF classique ;
- clôture analytique mensuelle.

---

## 8. Déploiement recette / production

```bash
# Mise à jour modules jalon
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d <base> -u dorevia_glc_analytics \
  --stop-after-init --no-http

docker compose restart odoo
```

**Ordre :** `dorevia_glc_analytics` puis `dorevia_glc_budget` (dépendance).

---

## 9. Documents de référence

| Document | Rôle |
|---|---|
| [PALIERS.md](./PALIERS.md) | Roadmap consolidée |
| [AUDIT_GLC_ANALYTICS_BUDGET_AVANT_PALIER_4.md](./AUDIT_GLC_ANALYTICS_BUDGET_AVANT_PALIER_4.md) | Audit officiel pré-Palier 4 |
| [CADRAGE_FINAL_PALIER_4.md](./CADRAGE_FINAL_PALIER_4.md) | Invariants cockpit |
| [RECETTE_MANUELLE_PALIER_4.md](./RECETTE_MANUELLE_PALIER_4.md) | Recette MOA Palier 4 |
| [CADRAGE_BUDGET_COCKPIT.md](./CADRAGE_BUDGET_COCKPIT.md) | Doctrine budget & cockpit |

---

## 10. Verdict jalon

**GLC Paliers 0–4 : livrés, recettés, gelés MOA.**

Prochaine étape MOA : **cadrage Palier 5** (en pause) — pas de développement immédiat sans décision explicite.

---

*Release note jalon — `main` · 2026-05-27*
