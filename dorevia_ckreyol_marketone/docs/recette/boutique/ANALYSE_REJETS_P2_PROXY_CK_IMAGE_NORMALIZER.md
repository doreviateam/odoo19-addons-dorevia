# Analyse Dev — 7 rejets batch P2 proxy legacy

| Champ | Valeur |
|-------|--------|
| **Type** | Livrable Dev — réponse demande MOA |
| **Date** | 2026-05-20 |
| **Batch** | `tools/ck_image_normalizer/reports/batch_20260520T105124Z.json` |
| **Réponse MOA** | [`REPONSE_MOA_P2_PROXY_LEGACY_CK_IMAGE_NORMALIZER.md`](./REPONSE_MOA_P2_PROXY_LEGACY_CK_IMAGE_NORMALIZER.md) |
| **Recette** | `ck_shop_tile_v1` — seuil `content_area_ratio_max: 0.95` (profil `packshot`) |

---

## Synthèse

| Constat | Détail |
|---------|--------|
| **Cause unique des 7 REJECTED** | Règle `content_area_ratio > 0.95` sur profil **packshot** |
| **Profil lifestyle** | Aucun rejet sur ratio plein cadre (règle max non appliquée) |
| **Tuiles produites malgré rejet** | 7/7 — previews disponibles pour revue MOA visuelle |
| **Recommandation globale** | Assouplir la règle plein cadre packshot : `REJECTED` → `NEEDS_REVIEW` ou `OK_WITH_WARNINGS` selon bande |

---

## Tableau détaillé — 7 REJECTED

| # | Fichier | Profil | Règle déclenchée | Métrique | Valeur | Cause probable | Recommandation Dev |
|---|---------|--------|------------------|----------|--------|----------------|-------------------|
| 1 | `exemple_produit_manioc_crackers_la_platine.backup_pre_retouche.png` | packshot | `content_area_ratio > 0.95` | `content_area_ratio` | **1.0** | Packshot fiche produit plein cadre — produit occupe quasi toute la source ; fond blanc non isolé par flood-fill (ombres / anti-alias) | **Seuil trop strict** → `NEEDS_REVIEW` · revue MOA preview |
| 2 | `exemple_produit_manioc_crackers_la_platine.png` | packshot | `content_area_ratio > 0.95` | `content_area_ratio` | **1.0** | Idem #1 — version retouchée, même géométrie source | **Seuil trop strict** → `NEEDS_REVIEW` |
| 3 | `homepage_manioc_pates_mayotte_la_platine.png` | packshot | `content_area_ratio > 0.95` | `content_area_ratio` | **1.0** | Produit vertical (sachet/pot) touchant les bords haut/bas après normalisation fond | **Seuil trop strict** → `NEEDS_REVIEW` · tuile probablement exploitable |
| 4 | `mvp02_reference_coffret_gourmand_bois.png` | packshot | `content_area_ratio > 0.95` | `content_area_ratio` | **0.997** | Coffret multi-produits + fond bois — scène composition, pas packshot unitaire | **Image source non adaptée** + **profil mal renseigné** → `lifestyle` ou rejet légitime si strict packshot |
| 5 | `stitch_curry_powder_pouch.png` | packshot | `content_area_ratio > 0.95` | `content_area_ratio` | **1.0** | Export Stitch carré plein cadre — produit remplit la source | **Image source non adaptée** (Stitch) → `NEEDS_REVIEW` ou profil `lifestyle` |
| 6 | `stitch_guava_jam_jar.png` | packshot | `content_area_ratio > 0.95` | `content_area_ratio` | **1.0** | Export Stitch bocal centré plein cadre | **Image source non adaptée** → `NEEDS_REVIEW` |
| 7 | `stitch_scotch_bonnet_sauce.png` | packshot | `content_area_ratio > 0.95` | `content_area_ratio` | **1.0** | Export Stitch bouteille plein cadre | **Image source non adaptée** → `NEEDS_REVIEW` |

### Métriques secondaires (non déclencheuses)

| Fichier | `background_entropy` | Warning |
|---------|---------------------|---------|
| Tous les 7 | 0.002 – 0.24 | Aucun n'a dépassé `0.42` — pas de rejet entropy |

---

## Répartition des recommandations

| Recommandation | Count | Fichiers |
|----------------|-------|----------|
| **Seuil trop strict** → `NEEDS_REVIEW` | 3 | `exemple_produit_*`, `homepage_manioc_pates_*` |
| **Image source non adaptée** → `NEEDS_REVIEW` | 3 | `stitch_curry_*`, `stitch_guava_*`, `stitch_scotch_*` |
| **Profil mal renseigné** | 1 | `mvp02_reference_coffret_*` (plutôt lifestyle / éditorial) |
| **Rejet légitime** (si politique packshot strict) | 0–1 | Coffret selon arbitrage MOA |

**Aucun rejet ne correspond à un échec technique** (crash, bbox introuvable, export manquant).

---

## Analyse règle `content_area_ratio > 0.95`

### Comportement actuel

```yaml
# ck_shop_tile_v1 — profil packshot
reject_if:
  content_area_ratio_max: 0.95   # → statut REJECTED immédiat
```

La métrique mesure la surface du bounding box contenu **après** replace fond, **avant** composition canvas 1024. Un ratio proche de 1.0 signifie « le produit occupe déjà toute l'image source » — fréquent sur :

- exports design (Stitch) déjà carrés ;
- packshots fournisseur sans marge ;
- fiches produit recadrées serré.

### Problème

Le moteur **compose quand même une tuile 1024×1024 valide** (padding calculé, centrage OK). Le rejet est **métier/heuristique**, pas qualité output.

Exemple : `stitch_jerk_marinade_bottle.png` — ratio **0.929** → `OK_WITH_WARNINGS` (même famille, seuil juste en dessous).

### Proposition calibrage — `ck_shop_tile_v1.1` (draft)

| Bande ratio (packshot) | Statut proposé | Logique |
|------------------------|----------------|---------|
| `< 0.15` | `REJECTED` | Produit trop petit — inutilisable tuile |
| `0.15 – 0.95` | `OK` / `OK_WITH_WARNINGS` | Zone normale |
| `0.95 – 1.0` | **`NEEDS_REVIEW`** | Plein cadre — revue MOA, pas rejet auto |
| `> 1.0` | `REJECTED` | Impossible (garde-fou) |

**Impact estimé sur batch proxy** : 7 `REJECTED` → **7 `NEEDS_REVIEW`** · OK rate auto inchangé (67 %) · Rejected rate auto **0 %**.

> MOA décide si `NEEDS_REVIEW` compte comme acceptable en phase POC ou seulement en revue humaine.

### Alternative conservatrice

Garder `REJECTED` au-delà de 0.98, `NEEDS_REVIEW` entre 0.95 et 0.98 — ne transformer en `OK_WITH_WARNINGS` qu'après validation preview MOA.

---

## Recommandation Dev — suite MOA (4 options)

| Option MOA | Action Dev | Quand |
|------------|-----------|-------|
| **1 — Recalibrer recette** | Implémenter `ck_shop_tile_v1.1` (bande NEEDS_REVIEW) + relancer batch proxy | Si MOA valide proposition § ci-dessus |
| **2 — Conserver recette** | Aucun changement code · documenter que proxy = lot difficile | Si MOA estime les 7 rejets légitimes |
| **3 — Batch ciblé post-ajustement** | Relancer 7 fichiers seuls après v1.1 | Après option 1 |
| **4 — Valider lot 21 refs** | Confirmer échantillon officiel MOA · décision sur batch v1.1 | **Retenu MOA 2026-05-20** (révision depuis 30) |

**Recommandation Dev** : **option 1 + 3** — faible effort (~0.5 j/h), débloque la revue visuelle MOA sur les 7 previews. *(Option 4 retenue par MOA le 2026-05-20 : 21 refs = lot officiel.)*

---

## Points pour recette visuelle MOA (P3)

Les 7 previews `REJECTED` méritent une **revue G1–G6** — plusieurs tuiles normalisées peuvent être visuellement acceptables malgré le statut auto.

| Priorité | Fichiers | Question MOA |
|----------|----------|----------------|
| Haute | `homepage_manioc_pates_*`, `exemple_produit_*` | Tuile exploitable `/shop` ? |
| Haute | `stitch_guava_jam_jar`, `stitch_scotch_bonnet_sauce` | Packshot ou hors périmètre tuile ? |
| Moyenne | `stitch_curry_powder_pouch` | Sachet — texture préservée (G5) ? |
| Basse | `mvp02_reference_coffret_*` | Coffret = tuile ou lifestyle ? |

**G6 (couture `#F8EEDB`)** : à noter sur les **14 OK + 7 NEEDS_REVIEW potentiels**, pas seulement les rejets.

---

## Rappel

- **Pas de code Odoo**
- **Pas de remplacement `image_1920`**
- Calibrage recette = fichier YAML + logique `determine_status()` dans le CLI externe uniquement

---

## Historique

| Date | Auteur | Action |
|------|--------|--------|
| 2026-05-20 | Dev | Analyse 7 REJECTED + proposition `ck_shop_tile_v1.1` |
