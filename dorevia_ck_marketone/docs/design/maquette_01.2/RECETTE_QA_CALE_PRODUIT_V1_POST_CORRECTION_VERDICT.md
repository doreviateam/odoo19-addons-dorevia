# Verdict — Recette post-correction Axe C · Cale produit V1

| Champ | Valeur |
| --- | --- |
| Date | 26 juin 2026 — **clôture Axe C** |
| Base | `dorevia_ck_marketone_01` · `http://localhost:18079` |
| Exécutant | Dev / QA (automatisé + HTTP/SQL + recette visuelle) |
| Modules | `dorevia_ck_theme` **19.0.1.59.0** · `dorevia_ck_marketone_content` **19.0.1.44.0** |
| Référence checklist | [`RECETTE_QA_CALE_PRODUIT_V1_POST_CORRECTION.md`](RECETTE_QA_CALE_PRODUIT_V1_POST_CORRECTION.md) |
| Résultat global | **GO final Axe C** — Rail 2 Note 07 peut s'ouvrir |

**Preuves recette visuelle** (26/06/2026) :
- Rapport : `/private/tmp/ck_axe_c_visual_recipe_20260626/axe_c_visual_recipe_report.json` (`allPass: true`)
- Captures : `/private/tmp/ck_axe_c_visual_recipe_20260626/` (A2/A3 · G1–G6)

---

## 0. Prérequis techniques

| # | Action | Résultat |
| --- | --- | --- |
| P1 | `-u dorevia_ck_theme` + redémarrage | ✅ `19.0.1.59.0` |
| P2 | `-u dorevia_ck_marketone_content` + redémarrage | ✅ `19.0.1.44.0` |
| P3 | Corrections BO MOA Axe C | ✅ **Complet** (hors suivi MOA-1 XML Coups de cœur) |

**Tests auto** :
- `dorevia_ck_marketone_home_section3_featured_field` — **5/5 OK**
- `dorevia_ck_axe_c_bo_sync` — **2/2 OK**
- `dorevia_ck_moa2_bo_sync` — **2/2 OK**

---

## 1. Synthèse par bloc

| Bloc | Résultat | Commentaire |
| --- | --- | --- |
| A — Livraisons Dev 26/06 | ✅ | Libellé BO · logo SVG 1280 + 390 px |
| B — Coups de cœur | ✅ | 0 produit en catégorie · menu/filmstrip OK |
| C — Navigation Soin | ✅ | **Soin & Bien-être** · URL HTTP 200 |
| D — Traductions fr_FR | ✅ | Migration 43.0 |
| E — UOM / prix réf. | ✅ | Migration 43.0 |
| F — MOA-2 (Jus / Pâte) | ✅ | Migration 44.0 — l/l · kg/kg |
| G — Cards catalogue | ✅ | Recette visuelle 1280/390 px — G1–G6 OK |

---

## 2. Détail des contrôles exécutés

### A — Livraisons Dev ✅

| # | Contrôle | Résultat |
| --- | --- | --- |
| A1 | Libellé **Afficher sur l'accueil** | ✅ test auto + BO |
| A2 | Logo SVG desktop 1280 px | ✅ `ck-logo.svg` · `aria-label="C-Kréyòl — Accueil"` |
| A3 | Logo SVG mobile 390 px | ✅ pas d'overflow · même source SVG |

### B — Coups de cœur ✅

| # | Contrôle | Résultat | Preuve |
| --- | --- | --- | --- |
| B1 | 0 produit avec catégorie Coups de cœur | ✅ | SQL + recette visuelle |
| B2 | Pas d'entrée menu Coups de cœur | ✅ | header 1280/390 |
| B3 | Pas de pill filmstrip `/shop` | ✅ | recette visuelle `/shop` |
| B4 | Home « Nos coups de cœur » | ✅ | section présente |
| B5 | Pilotage `ck_is_featured` | ✅ | tests auto |
| B6 | Catégorie en base (MOA-1) | ☐ suivi | Catégorie en DB · 0 produit — **ticket XML séparé, non bloquant clôture** |

### C — Navigation ✅

| # | Contrôle | Résultat |
| --- | --- | --- |
| C1 | Libellé Soin & Bien-être | ✅ |
| C2 | URL | ✅ HTTP 200 |

### D — Traductions fr_FR ✅

Migration 43.0 — 9 catégories · Galettes · Origine/Guadeloupe.

### E — UOM et prix de référence ✅

Migration 43.0 — g/kg (4 masse) · Panama sans prix réf.

### F — MOA-2 ✅

Migration 44.0 — Jus Mont-Pelé **l/l** · Pâte de manioc **kg/kg**.

### G — Cards catalogue ✅

| # | Contrôle | Résultat |
| --- | --- | --- |
| G1 | Grille `/shop` 1280/390 | ✅ pas d'UOM absurdes · pas de pill Coups de cœur |
| G2 | Rayon Boissons | ✅ Jus Mont-Pelé · badge OK |
| G3 | Rayon Soin & Bien-être | ✅ produit/badge attendus |
| G4 | Rayon Artisanat | ✅ badge OK |
| G5 | Fiche produit témoin | ✅ |
| G6 | Panier | ✅ badge `0 → 1` |

---

## 3. Écarts résiduels (non bloquants clôture)

| Suivi | Écart | Responsable |
| --- | --- | --- |
| MOA-1 | Catégorie « Coups de cœur » en DB (B6) | MOA — ticket XML `noupdate` / retrait |
| — | Action 6 origines sur 6 produits | MOA — hors périmètre migrations 43/44 |

---

## 4. Décision

```text
☑ Cale produit V1 clôturée — Rail 2 Note 07 peut s'ouvrir
☐ Corrections BO complémentaires bloquantes
```

**Verdict** : **GO final Axe C** — sandbox `dorevia_ck_marketone_01` validée post-upgrade **19.0.1.59.0 / 19.0.1.44.0** + recette visuelle **1280/390 px**.

**Rail 2** : **GO démarrage** lot Note 07 (pages catégories pleine largeur) — cf. [`note_07.md`](../../cadrage/note_07.md) et ticket Dev.

---

## 5. Prochaines actions

| Ordre | Qui | Action |
| --- | --- | --- |
| 1 | Lead / Dev | Ouvrir Rail 2 — ticket Note 07 |
| 2 | MOA | Ticket XML Coups de cœur (MOA-1) en parallèle si souhaité |
| 3 | QA | Baseline recette Note 07 sur slugs cibles |

---

*Verdict final — 26 juin 2026 — sandbox `dorevia_ck_marketone_01`*
