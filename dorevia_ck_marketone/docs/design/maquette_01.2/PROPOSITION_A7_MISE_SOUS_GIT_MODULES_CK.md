# Proposition MOA — A7 · Mise sous Git modules CK maquette

| Champ | Valeur |
|-------|--------|
| **Chantier** | **A — Reprise maquette CK V1.2.x / go-live CMS** |
| **Statut** | **GO A7 partiel signé MOA · 2026-06-14 · commits A7-1 à A7-4a autorisés** |
| **Date** | 2026-06-14 |
| **Repo cible** | `doreviateam/odoo19-addons-dorevia` |

```text
Séparation stricte Chantier A / Chantier B :
  A7 ne concerne PAS dorevia_ckreyol_marketone (PR #62 · Chantier B).
```

---

## Constats

| Point | État actuel |
|-------|-------------|
| Modules Odoo CK | `dorevia_ck_theme` · `dorevia_ck_marketone_content` — **untracked** |
| Dossier projet / docs | `dorevia_ck_marketone/docs/` — **untracked** (~52 Mo, dont scripts Playwright) |
| Instance recette | `dorevia_ck_marketone_01` — fonctionne en local |
| Traçabilité | **Aucune** sur Git · pas de CI reproductible · risque perte / divergence post-crash |
| Verdict go-live | **Non signé** — A7 ≠ go-live · prérequis industrialisation |

---

## Modules concernés

| Module | Version | Fichiers code | Rôle |
|--------|---------|---------------|------|
| `dorevia_ck_theme` | `19.0.1.12.0` | ~39 | Tokens · SCSS · snippets · layout · header Phase 10 A1-OK |
| `dorevia_ck_marketone_content` | `19.0.1.0.0` | ~19 | Bootstraps CMS · pages · newsletter · tests phases 3–9 |
| `dorevia_ck_marketone/docs/` | — | ~293+ | Gouvernance · recettes · scripts QA · artifacts maquette |

**Note** : `dorevia_ck_marketone/` n'est **pas** un module Odoo installable — c'est le **dossier projet** (documentation + scripts). Les modules installables sont `dorevia_ck_theme` et `dorevia_ck_marketone_content`.

---

## Branche cible recommandée

| Option | Branche | Usage |
|--------|---------|-------|
| **Recommandée** | `feat/ck-maquette-v1-2-x-reprise-odoo` | Toute la reprise maquette CK · revue MOA dédiée |
| Alternative | `feat/ck-theme-19.0.1.11.0` | Si MOA préfère decouper thème seul d'abord |

**Base** : `main` du repo `odoo19-addons-dorevia` (après merge PR #62 si souhaité — **indépendant** des commits A7).

---

## Périmètre proposé — ordre des commits

### Commit A7-1 — Module thème (socle)

```text
feat(ck-theme): socle dorevia_ck_theme 19.0.1.12.0 — tokens, snippets, header Phase 10 A1-OK
```

| Inclure | Exclure |
|---------|---------|
| `dorevia_ck_theme/**` (manifest, views, scss, hooks, migrations, tests phase10 + technique) | — |

**Gate** : `--test-tags=dorevia_ck_theme_phase10,dorevia_ck_theme_technical`

---

### Commit A7-2 — Module contenu CK

```text
feat(ck-content): dorevia_ck_marketone_content 19.0.1.0.0 — bootstraps CMS phases 3–9
```

| Inclure | Exclure |
|---------|---------|
| `dorevia_ck_marketone_content/**` | — |

**Gate** : `--test-tags=dorevia_ck_marketone_content` (tags phases 3–9)

**Depends** : `dorevia_ck_theme` (A7-1)

---

### Commit A7-3 — Gouvernance et recettes (docs projet)

```text
docs(ck-maquette): gouvernance MOA, recettes Phase 1–10 et scripts QA
```

| Inclure | Exclure |
|---------|---------|
| `dorevia_ck_marketone/docs/design/maquette_01.2/**` | `scripts/node_modules/` |
| `dorevia_ck_marketone/docs/cadrage/**` | `scripts/package-lock.json` (gitignore local) |
| Scripts `ck_phase*_ci.sh` · recettes · décisions MOA | Artifacts HTML lourds si MOA acte exclusion |

**`.gitignore` à ajouter** (A7-3) :

```gitignore
# Playwright / Node — recette locale uniquement
docs/design/maquette_01.2/scripts/node_modules/
docs/design/maquette_01.2/scripts/package-lock.json
```

---

### Commit A7-4 (optionnel) — Artifacts maquette statiques

```text
docs(ck-maquette): artifacts HTML/CSS maquette V1.2.x Lot 1–3
```

| Inclure | Exclure |
|---------|---------|
| `docs/design/maquette_01.2/artifact/*.html` · `ck-maquette.css` | PDF lourds si > limite repo · `rapport/*.pdf` → LFS ou hors repo |

**Décision MOA requise** : versionner les PDF (`rapport/RAPPORT_MOA_*.pdf`) ou lien externe uniquement.

---

## Exclusions explicites (tous commits A7)

| Chemin | Raison |
|--------|--------|
| `dorevia_ckreyol_marketone/**` | **Chantier B** · PR #62 |
| `dorevia_glc_analytics/**` | Chantier GLC séparé |
| `.env` · credentials · dumps DB | Secrets |
| `node_modules/` | Dépendances locales recette |
| Bases Odoo · filestore | Données runtime |

---

## Risques si on continue uniquement en local

| Risque | Impact | Mitigation A7 |
|--------|--------|---------------|
| Perte post-crash (Codex / machine) | Retravail phases 1–10 | Git + remote |
| Divergence Dev / MOA / prod | Recette non reproductible | Branche + tags version |
| Impossible CI gate | Régressions silencieuses | Scripts `ck_phase*_ci.sh` en repo |
| Merge accidentel Chantier B | Contamination périmètre | Branche A7 dédiée · checklist tri |
| Go-live sans snapshot code | Déploiement artisanal | Tag `ck-maquette-v1.2.x-rc1` post A7 |

---

## Prérequis avant acte MOA A7

| # | Prérequis | Statut |
|---|-----------|--------|
| 1 | Verdict **A1** header signé (ou GO Dev header clôturé) | ✅ **A1-OK** · 2026-06-14 |
| 2 | Split thème / contenu §4bis **non rouvert** | ✅ acté |
| 3 | Checklist tri worktree · pas de fichiers B dans commit A | ✅ exécuté · 2026-06-14 |
| 4 | Gates phases 1–10 passent sur branche A7 | ☐ post-commit A7-1/2 |
| 5 | MOA acte périmètre commits A7-1 à A7-4a | ✅ **GO A7 partiel** · 2026-06-14 |

---

## Modèle acte MOA — GO A7

```text
GO A7 partiel — Mise sous Git modules CK maquette V1.2.x
Repo : odoo19-addons-dorevia
Branche : feat/ck-maquette-v1-2-x-reprise-odoo
Commits autorisés : A7-1 thème · A7-2 contenu · A7-3 docs · A7-4a artifacts légers
Exclusions : Chantier B · GLC · secrets · node_modules · PDF/captures rapport/ (A7-4b NO GO)
Validé par : MOA CK
Date : 2026-06-14
```

---

## Documents liés

| Document | Rôle |
|----------|------|
| [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) §4bis | Split thème / contenu |
| [`RECETTE_MOA_ECRAN_A1_HEADER_PHASE10.md`](./RECETTE_MOA_ECRAN_A1_HEADER_PHASE10.md) | Prérequis A1 avant A7 recommandé |
| [`GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md`](./GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md) | Doctrine reprise |

---

*Proposition A7 — Chantier A uniquement · aucun commit sans acte MOA · 2026-06-14.*
