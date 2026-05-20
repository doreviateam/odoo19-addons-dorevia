# Rapport POC — CK Image Normalizer V1.2-alpha (3 packshots transparents)

| Champ | Valeur |
|-------|--------|
| **Type** | POC technique ciblé · 3 packshots + 1 lifestyle contrôle |
| **Demande MOA** | Évaluer rendu /shop avec packshots transparents (alpha=0) |
| **Date** | 2026-05-20 |
| **Recette candidate** | `ck_shop_tile_v1.2-alpha` (`recipes/ck_shop_tile_v1.2-alpha.yaml`) |
| **Script POC** | `tools/ck_image_normalizer/poc_v12_alpha.py` |
| **Run** | `reports/runs/poc_v12_alpha_20260520/` |
| **Base** | `ckr-marketone-01` · flag **`True`** · module v `19.0.15.7.19` |

---

## 1. Réponses aux questions techniques MOA (§ 6)

| # | Question | Réponse |
|---|----------|---------|
| 6.1 | `image_shop_tile` peut-il porter WebP/PNG transparent ? | **Oui** — `fields.Image(attachment=True)` accepte tout binaire image, alpha conservé. |
| 6.2 | Format le plus sûr V1.5 ? | **PNG-24** universel (testé). WebP alpha équivalent mais navigateurs >97 %. |
| 6.3 | Compatibilité widget image Odoo ? | **Oui** — `t-options="{'widget': 'image'}"` sert via `/web/image/`, alpha préservé. |
| 6.4 | Comment distinguer packshot/lifestyle ? | Via `shop_tile_recipe_version` dans le manifest CSV et le modèle Odoo (`ck_shop_tile_v1.1` / `ck_shop_tile_v1.2-alpha`). |
| 6.5 | Recette candidate `ck_shop_tile_v1.2-alpha` ? | **Créée** · `background: transparent` · `output_format: PNG`. |
| 6.6 | Risques halos / détourage sale ? | **Confirmés** sur 2 des 3 images testées (voir § 3). |
| 6.7 | Garder `v1.1` pour lifestyle ? | **Oui — recommandé** (option hybride). |
| 6.8 | Test sur Crackers, Colombo, Pâtes ? | **Effectué** — résultats en § 3. |

---

## 2. Pipeline POC

```text
source PNG (archive/orig)
  → trim_uniform_border (V1.1 héritée)
  → flood-fill 4 coins → alpha=0 (au lieu de fill bg_rgb)
  → bbox content par alpha
  → resize content_fill_ratio 0.78
  → paste sur canvas 1024×1024 RGBA (255,255,255,0)
  → save PNG-24 optimize compress_level=6
```

Aucune dépendance IA. Pas de halos AI à craindre. Détourage déterministe par flood-fill couleur depuis les coins.

---

## 3. Résultats par image (sur fond conteneur `#FDFCFA`)

### 3.1 Crackers manioc Sainte-Anne (product 8) — ✅ EXCELLENT

| Métrique | Valeur |
|----------|--------|
| Source | Packshot fond blanc/écru uni |
| Pixels opaques | 37.5 % |
| Halos | Aucun |
| Rendu /shop | **Parfait** — produit sur fond off-white pur, aucun effet « image dans l'image » |

**Verdict** : la cible MOA est atteinte sur ce profil de source.

### 3.2 Pâtes de manioc Mayotte (product 9) — ⚠️ ACCEPTABLE AVEC RÉSERVE

| Métrique | Valeur |
|----------|--------|
| Source | Sachet sur plan de travail (gris/blanc non uniforme) |
| Pixels opaques | 41.6 % |
| Halos | Présents — pixels résiduels du plan de travail autour du sachet |
| Rendu /shop | Effet « image dans l'image » supprimé mais halos visibles |

**Verdict** : pseudo-packshot. Le flood-fill ne suit pas le contour du sachet ; bords visibles.

### 3.3 Colombo des Antilles (product 154) — ❌ NON ADAPTÉ

| Métrique | Valeur |
|----------|--------|
| Source | Scène lifestyle (cuisine + sachet + épices + fond ensoleillé) |
| Pixels opaques | 50.0 % |
| Halos | Forts — la scène entière est partiellement conservée |
| Rendu /shop | Mauvais — image mi-détourée, mi-scène lifestyle |

**Verdict** : ce visuel **n'est pas un packshot** mais un lifestyle. Ne doit pas passer en alpha.

### 3.4 Confiture banane flambée (product 153) — contrôle V1.1 lifestyle

| Métrique | Valeur |
|----------|--------|
| Recette | `ck_shop_tile_v1.1` (inchangé) |
| Rendu /shop | Acceptable — léger fond beige sur les bords du JPEG, mais lifestyle pleine zone |

**Verdict** : V1.1 reste valide pour vrais lifestyle.

---

## 4. Découvertes clés du POC

### 4.1 La piste alpha **fonctionne** sur les vrais packshots à fond uni clair

`Crackers Sainte-Anne` démontre que la cible MOA est techniquement atteignable sans IA.

### 4.2 Le détourage simple flood-fill **ne suffit pas** pour les fonds complexes

Les sources avec arrière-plan non uniforme (table, scène, fenêtre) génèrent des halos.

### 4.3 La distinction packshot / lifestyle dans le manifest source **n'est pas fiable**

`Colombo` est étiqueté packshot dans le catalogue mais est en réalité un lifestyle. Sur 3 sources POC, 1/3 mal classée.

**Action requise amont** : audit classification packshot/lifestyle MOA sur le lot pilote 43 — colonne dédiée dans le manifest source.

---

## 5. Recommandation Dev — option C affinée

```text
recette v1.1 → lifestyle (JPEG baked #F8EEDB)
recette v1.2-alpha → packshot fond uni clair (PNG-24 alpha=0)
classification source → décision MOA / opérateur catalogue
```

Étapes proposées :

| Phase | Action | Effort | Responsable |
|-------|--------|--------|-------------|
| **P8-1** | Audit classification packshot/lifestyle pilote 43 | 1 j/h | MOA + Dev |
| **P8-2** | Intégrer `v1.2-alpha` dans CLI (vrai pipeline, pas POC) | 2 j/h | Dev |
| **P8-3** | Re-export packshots audités en alpha | 0.5 j/h | Dev |
| **P8-4** | Import comparatif `/shop` | 0.5 j/h | Dev |
| **P8-5** | Revue MOA finale | 1 j/h | MOA |

---

## 6. Captures (sur sandbox `ckr-marketone-01` flag `True`)

| Capture | Contenu |
|---------|---------|
| `capture_moa_v12_alpha_shop.png` | Grille `/shop` complète |
| `capture_moa_v12_alpha_crackers.png` | Crackers V1.2-alpha **vs** Crackers sarrasin V1.1 (à côté) |
| `capture_moa_v12_alpha_pates.png` | Pâtes manioc V1.2-alpha (halo visible) |
| `capture_moa_v12_alpha_colombo.png` | Colombo V1.2-alpha (problème classification) |
| `capture_moa_v12_alpha_lifestyle_banane.png` | Confiture banane V1.1 lifestyle (contrôle) |
| `tools/.../comparaison_v11_vs_v12_alpha.png` | Preview avant/après hors Odoo |

URL live : http://localhost:18079/shop

---

## 7. Garde-fous respectés

| Garde-fou | Statut |
|-----------|--------|
| `image_1920` master | **Inchangé** sur 8, 9, 154 (vérifié assertion script) |
| Fiche produit | **Inchangée** |
| Flag `marketone.shop_tile_enabled` | `True` (recette) — rollback opérationnel |
| Fallback | Inchangé |
| Sidebar / structure carte / prix / CTA | Inchangés |
| Tests T1–T7 | Verts |
| Lot X | Toujours exclu |
| Pas de cron | Confirmé |

---

## 8. Décision MOA attendue

| Option | Effort | Effet |
|--------|--------|-------|
| **A** — GO V1.2-alpha sur packshots fond uni uniquement (option C affinée) + audit classification | 4–5 j/h | Cible MOA atteinte sur ~40–60 % du catalogue |
| **B** — Reporter, conserver V1.5 baked actuel | 0 j/h | Frange beige résiduelle assumée |
| **C** — Re-shooter les packshots en studio fond blanc strict (amont MOA) | hors Dev | Cible MOA atteinte sur 100 % du catalogue (long terme) |
| **D** — Explorer détourage IA (rembg, BiRefNet) | 3–5 j/h R&D | Risque halos non maîtrisés sur cheveux/fumée — non recommandé pour épicerie |

**Recommandation Dev** : **option A** (V1.2-alpha + audit classification).

---

## 9. Références

| Document | Rôle |
|----------|------|
| [`NOTE_CK_IMAGE_NORMALIZER_V1_2_TRANSPARENT_PROPOSAL.md`](../../cadrage/NOTE_CK_IMAGE_NORMALIZER_V1_2_TRANSPARENT_PROPOSAL.md) | Instruction MOA amont |
| `tools/ck_image_normalizer/recipes/ck_shop_tile_v1.2-alpha.yaml` | Recette candidate |
| `tools/ck_image_normalizer/poc_v12_alpha.py` | Script POC reproductible |
| [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION.md`](../../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION.md) | Ticket P7 |
