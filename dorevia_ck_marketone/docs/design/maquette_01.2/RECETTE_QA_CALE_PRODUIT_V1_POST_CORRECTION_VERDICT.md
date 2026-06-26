# Verdict — Recette post-correction Axe C · Cale produit V1

| Champ | Valeur |
| --- | --- |
| Date | 26 juin 2026 (rejeu post-upgrade 19.0.1.43.0) |
| Base | `dorevia_ck_marketone_01` · `http://localhost:18079` |
| Exécutant | Dev / QA (automatisé + HTTP/SQL) |
| Modules | `dorevia_ck_theme` **19.0.1.59.0** · `dorevia_ck_marketone_content` **19.0.1.43.0** |
| Référence checklist | [`RECETTE_QA_CALE_PRODUIT_V1_POST_CORRECTION.md`](RECETTE_QA_CALE_PRODUIT_V1_POST_CORRECTION.md) |
| Résultat global | **GO avec réserves** — bloc F (MOA-2) + recette visuelle mobile restants |

---

## 0. Prérequis techniques

| # | Action | Résultat |
| --- | --- | --- |
| P1 | `-u dorevia_ck_theme` + redémarrage | ✅ `19.0.1.59.0` |
| P2 | `-u dorevia_ck_marketone_content` + redémarrage | ✅ `19.0.1.43.0` (migration D/E exécutée) |
| P3 | Corrections BO MOA Axe C | ⚠️ **Partielles** — D/E au vert · F en attente MOA-2 |

**Tests auto post-upgrade** :
- `dorevia_ck_marketone_home_section3_featured_field` — **5/5 OK**
- `dorevia_ck_axe_c_bo_sync` — **2/2 OK**

---

## 1. Synthèse par bloc

| Bloc | Résultat | Commentaire |
| --- | --- | --- |
| A — Livraisons Dev 26/06 | ✅ | Libellé BO + logo SVG (A3 mobile à confirmer visuellement) |
| B — Coups de cœur | ✅ | 0 produit en catégorie · menu/filmstrip OK · upgrade `-u` n'a pas re-rattaché Panama |
| C — Navigation Soin | ✅ | Menu **Soin & Bien-être** · URL HTTP 200 |
| D — Traductions fr_FR | ✅ | Migration 43.0 — 9 catégories · Galettes · Origine/Guadeloupe |
| E — UOM / prix réf. | ✅ | Migration 43.0 — g/kg sur 4 masse · Panama `show_ref=False` |
| F — MOA-2 (Jus / Pâte) | ☐ | Hors migration 43.0 — UOM à arbitrer MOA |
| G — Cards catalogue | ⚠️ | Smoke HTTP OK (`/shop`, rayons Boissons/Artisanat/Soin) · recette visuelle 1280/390 px restante |

---

## 2. Détail des contrôles exécutés

### A — Livraisons Dev ✅

| # | Contrôle | Résultat |
| --- | --- | --- |
| A1 | Libellé **Afficher sur l'accueil** | ✅ `ir_model_fields` + test auto |
| A2 | Logo SVG desktop | ✅ `ck-logo.svg` (×2) sur `/` |
| A3 | Logo mobile | ☐ Recette visuelle 390 px à confirmer MOA/QA |

### B — Coups de cœur ✅

| # | Contrôle | Résultat | Preuve |
| --- | --- | --- | --- |
| B1 | 0 produit avec catégorie Coups de cœur | ✅ | SQL `produits_coups_coeur = 0` (post `-u`) |
| B2 | Pas d'entrée menu Coups de cœur | ✅ | `website_menu` : 0 ligne |
| B3 | Pas de pill filmstrip `/shop` | ✅ | HTML `/shop` : aucune occurrence « Coups de cœur » |
| B4 | Home « Nos coups de cœur » | ✅ | Section présente sur `/` |
| B5 | Pilotage `ck_is_featured` | ✅ | Tests auto |
| B6 | Catégorie en base (MOA-1) | ☐ | Catégorie toujours en DB · **0 produit** rattaché — arbitrage MOA-1 ouvert |

### C — Navigation ✅

| # | Contrôle | Résultat |
| --- | --- | --- |
| C1 | Libellé Soin & Bien-être | ✅ Menu `Soin & Bien-être` |
| C2 | URL | ✅ `/shop/category/soin-bien-etre-2` · HTTP 200 |

### D — Traductions fr_FR ✅

| # | Contrôle | Résultat | Preuve |
| --- | --- | --- | --- |
| D1 | Attribut Origine | ✅ | `origine_fr = Origine` |
| D2 | Valeur Guadeloupe | ✅ | `guadeloupe_fr = Guadeloupe` |
| D3 | Galettes de manioc | ✅ | `name->>'fr_FR' = Galettes de manioc` |
| D4 | Sous-catégories Épicerie (+ Soin) | ✅ | **9/9** catégories cibles sans `fr_FR` NULL |

### E — UOM et prix de référence ✅

| Produit | UOM nette | UOM réf. | `show_ref` | Résultat |
| --- | --- | --- | --- | --- |
| Confiture de goyave | g | kg | true | ✅ |
| Manio Crackers | g | kg | true | ✅ |
| Galettes de manioc | g | kg | true | ✅ |
| Savon vétiver | g | kg | true | ✅ |
| Chapeau Panama | *(vide)* | *(vide)* | **false** | ✅ |

### F — MOA-2 ☐

| Produit | État actuel | Attendu |
| --- | --- | --- |
| Jus Mont-Pelé | net **l** · réf **l** · `show_ref=true` | Arbitrage MOA-2 (migration 44.0) |
| Pâte de manioc | net **kg** · réf **kg** · `show_ref=true` | Idem |

### G — Cards catalogue ⚠️

| # | Contrôle | Résultat |
| --- | --- | --- |
| G1 | Grille `/shop` | ✅ HTTP 200 · smoke OK |
| G2 | Rayon Boissons | ✅ HTTP 200 · Jus Mont-Pelé visible |
| G3 | Rayon Soin | ✅ HTTP 200 |
| G4 | Rayon Artisanat | ✅ HTTP 200 |
| G5–G6 | Fiche produit · panier | ☐ Recette visuelle / parcours MOA |

---

## 3. Écarts bloquants clôture Axe C

| Priorité | Écart | Responsable |
| --- | --- | --- |
| ~~P1~~ | ~~Coups de cœur (B1/B3)~~ | ✅ Corrigé |
| ~~P2~~ | ~~Traductions fr_FR (D)~~ | ✅ Migration 43.0 |
| ~~P2~~ | ~~UOM périmètre E~~ | ✅ Migration 43.0 |
| **P1** | Jus Mont-Pelé · Pâte de manioc (F) | MOA — MOA-2 → migration 44.0 |
| P2 | Recette visuelle mobile 390 px (A3, G) | QA / MOA |
| P3 | Catégorie Coups de cœur en base (B6 / MOA-1) | MOA — ticket XML séparé |

---

## 4. Décision

```text
☐ Cale produit V1 clôturée — Rail 2 Note 07 peut s'ouvrir
☑ Corrections BO complémentaires requises avant clôture (F + QA visuelle)
```

**Verdict** : **GO avec réserves** — upgrade **19.0.1.59.0 / 19.0.1.43.0** validé · blocs **A–E** au vert (hors A3 visuel).  
**NO GO clôture Axe C** tant que **MOA-2** (Jus / Pâte) et recette visuelle mobile ne sont pas au vert.

---

## 5. Prochaines actions

| Ordre | Qui | Action |
| --- | --- | --- |
| 1 | MOA | Arbitrage MOA-2 → migration **19.0.1.44.0** (Jus / Pâte) |
| 2 | MOA | Décision MOA-1 + ticket XML « Coups de cœur » (`noupdate` / retrait) |
| 3 | QA | Recette visuelle 390 px (logo, filmstrip, cards G) |
| 4 | Lead | Clôture Axe C → GO démarrage Rail 2 Note 07 |

---

*Verdict post-upgrade — 26 juin 2026 — sandbox `dorevia_ck_marketone_01`*
