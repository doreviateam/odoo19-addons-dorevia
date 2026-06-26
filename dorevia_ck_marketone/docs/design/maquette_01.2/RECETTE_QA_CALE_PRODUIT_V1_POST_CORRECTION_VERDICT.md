# Verdict — Recette post-correction Axe C · Cale produit V1

| Champ | Valeur |
| --- | --- |
| Date | 26 juin 2026 |
| Base | `dorevia_ck_marketone_01` · `http://localhost:18079` |
| Exécutant | Dev / QA (automatisé + HTTP/SQL) |
| Modules | `dorevia_ck_theme` **19.0.1.59.0** · `dorevia_ck_marketone_content` **19.0.1.42.0** |
| Référence checklist | [`RECETTE_QA_CALE_PRODUIT_V1_POST_CORRECTION.md`](RECETTE_QA_CALE_PRODUIT_V1_POST_CORRECTION.md) |
| Résultat global | **GO avec réserves** — corrections BO Axe C incomplètes |

---

## 0. Prérequis techniques

| # | Action | Résultat |
| --- | --- | --- |
| P1 | `-u dorevia_ck_theme` + redémarrage | ✅ `19.0.1.59.0` (ir_module_module) |
| P2 | `-u dorevia_ck_marketone_content` + redémarrage | ✅ `19.0.1.42.0` |
| P3 | Corrections BO MOA Axe C | ⚠️ **Partielles** — bloc B au vert · D/E/F restants |

**Tests auto post-upgrade** : `dorevia_ck_marketone_home_section3_featured_field` — **5/5 OK** (dont `test_ck_is_featured_field_label_and_help`).

---

## 1. Synthèse par bloc

| Bloc | Résultat | Commentaire |
| --- | --- | --- |
| A — Livraisons Dev 26/06 | ✅ | Libellé BO + logo SVG |
| B — Coups de cœur | ✅ | Menu OK · 0 produit en catégorie · filmstrip nettoyé |
| C — Navigation Soin | ✅ | Menu **Soin & Bien-être** · URL OK |
| D — Traductions fr_FR | ☐ | Non vérifié automatiquement — recette BO manuelle |
| E — UOM / prix réf. | ☐ | Non vérifié — recette BO manuelle |
| F — MOA-2 (Jus / Pâte) | ☐ | Non vérifié — arbitrage MOA |
| G — Cards catalogue | ☐ | Smoke HTTP partiel seulement |

---

## 2. Détail des contrôles exécutés

### A — Livraisons Dev ✅

| # | Contrôle | Résultat |
| --- | --- | --- |
| A1 | Libellé **Afficher sur l'accueil** | ✅ `ir_model_fields.field_description` = `Afficher sur l'accueil` |
| A2 | Logo SVG desktop | ✅ `ck-logo.svg` + `ck-header__brand-img` sur `/` |
| A3 | Logo mobile | ☐ Recette visuelle 390 px à confirmer MOA/QA |

### B — Coups de cœur ✅

| # | Contrôle | Résultat | Preuve |
| --- | --- | --- | --- |
| B1 | 0 produit avec catégorie Coups de cœur | ✅ | **0 produit** (correction ORM/SQL 26/06 — retrait Chapeau Panama id=1076) |
| B2 | Pas d'entrée menu Coups de cœur | ✅ | `website_menu` : 0 ligne |
| B3 | Pas de pill filmstrip `/shop` | ✅ | HTML `/shop` : plus de `Coups de cœur` (vérif. après B1) |
| B4 | Home « Nos coups de cœur » | ✅ | Section présente sur `/` |
| B5 | Pilotage `ck_is_featured` | ✅ | Tests auto + champ BO |
| B6 | Catégorie en base (MOA-1) | ☐ | Catégorie toujours en DB · **0 produit** rattaché |

**Action MOA B1/B3** : ~~retirer Chapeau Panama~~ — **fait sandbox 26/06** (SQL rel + `ck_is_featured` conservé sur Panama).

### Correction technique appliquée (sandbox)

```sql
DELETE FROM product_public_category_product_template_rel
WHERE product_public_category_id = 24 AND product_template_id = 1076;
```

Vérification : `ck_is_featured = true` sur Chapeau Panama · Home inchangée.

### C — Navigation ✅

| # | Contrôle | Résultat |
| --- | --- | --- |
| C1 | Libellé Soin & Bien-être | ✅ Menu `Soin & Bien-être` |
| C2 | URL | ✅ `/shop/category/soin-bien-etre-2` |

---

## 3. Écarts bloquants clôture Axe C

| Priorité | Écart | Responsable |
| --- | --- | --- |
| ~~P1~~ | ~~Chapeau Panama en Coups de cœur~~ | ✅ Corrigé sandbox 26/06 |
| ~~P1~~ | ~~Filmstrip Coups de cœur~~ | ✅ Corrigé après B1 |
| P2 | Traductions fr_FR (D) | MOA — Action 5abc |
| P2 | UOM / prix réf. (E) | MOA — Actions 7/8 |
| P2 | Jus Mont-Pelé · Pâte de manioc (F) | MOA — MOA-2 |

---

## 4. Décision

```text
☐ Cale produit V1 clôturée — Rail 2 Note 07 peut s'ouvrir
☑ Corrections BO complémentaires requises avant clôture
```

**Verdict** : **GO avec réserves** sur la partie **Dev** (upgrade + Action 10 + logo).  
**NO GO clôture Axe C** tant que D/E/F et recette visuelle mobile ne sont pas au vert (B1/B3 corrigés 26/06).

---

## 5. Prochaines actions

| Ordre | Qui | Action |
| --- | --- | --- |
| 1 | MOA | Compléter D/E/F (traductions, UOM, MOA-2) |
| 2 | QA | Recette visuelle 390 px (logo + filmstrip) |
| 3 | QA | Rejouer checklist §D–G après BO |
| 4 | Lead | Clôture Axe C → GO démarrage Rail 2 Note 07 |

---

*Verdict partiel — 26 juin 2026 — sandbox `dorevia_ck_marketone_01`*
