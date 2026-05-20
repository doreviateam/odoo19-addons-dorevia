# Recette P3 ciblée — Revue visuelle 7 fichiers `NEEDS_REVIEW` (v1.1)

| Champ | Valeur |
|-------|--------|
| **Statut** | **Clôturé MOA** |
| **Date** | 2026-05-20 |
| **Recette** | `ck_shop_tile_v1.1` — calibrage **accepté comme base de revue** |
| **Réponse MOA** | [`REPONSE_MOA_P3_CIBLE_7FICHIERS.md`](./REPONSE_MOA_P3_CIBLE_7FICHIERS.md) |
| **Rapport batch** | [`RAPPORT_V1_1_RECALIBRATION_7FICHIERS.md`](./RAPPORT_V1_1_RECALIBRATION_7FICHIERS.md) |

---

## Objectif

Arbitrer visuellement les **7 tuiles** passées de `REJECTED` (v1) à `NEEDS_REVIEW` (v1.1), et décider de la suite recette.

**Pas de GO POC final** tant que cette revue n'est pas clôturée.

---

## Fichiers à examiner

Previews avant/après :

```text
tools/ck_image_normalizer/reports/runs/v1_1_recal_7/reports/previews/
```

| # | Fichier | Référence | Ratio |
|---|---------|-----------|-------|
| 1 | `exemple_produit_manioc_crackers_la_platine.backup_pre_retouche.png` | Crackers — avant retouche | 1.0 |
| 2 | `exemple_produit_manioc_crackers_la_platine.png` | Crackers — retouché | 1.0 |
| 3 | `homepage_manioc_pates_mayotte_la_platine.png` | Pâtes Mayotte | 1.0 |
| 4 | `mvp02_reference_coffret_gourmand_bois.png` | Coffret bois | 0.997 |
| 5 | `stitch_curry_powder_pouch.png` | Pochette curry | 1.0 |
| 6 | `stitch_guava_jam_jar.png` | Pot goyave | 1.0 |
| 7 | `stitch_scotch_bonnet_sauce.png` | Sauce scotch bonnet | 1.0 |

CSV notation : [`moa_scoring_p3_cible_7.csv`](../../../../tools/ck_image_normalizer/reports/runs/v1_1_recal_7/reports/moa_scoring_p3_cible_7.csv)

---

## Grille G1–G6 (noter 1–5 par critère)

| Critère | Question MOA |
|---------|--------------|
| **G1 — Lisibilité** | Produit identifiable en ~320 px (tuile mobile) ? |
| **G2 — Chaleur / premium** | Cohérent ligne CK UX-3 B1 (sobre, chaleureux) ? |
| **G3 — Cohérence grille** | Poids visuel comparable aux tuiles OK du proxy ? |
| **G4 — Absence artificiel** | Pas de halo agressif, pas de « sale », pas d'effet IA ? |
| **G5 — Texture / étiquette** | Matière, texte étiquette préservés ? |
| **G6 — Couture `#F8EEDB`** | Transition image / corps carte `#FDF9F0` naturelle ? |

---

## Décision par fichier (choix unique)

| Code | Signification |
|------|---------------|
| **E** | **Exploitable** telle quelle en tuile `/shop` |
| **R** | **Acceptable avec réserve** — utilisable sous conditions |
| **M** | **Reprise manuelle** source ou retouche requise |
| **X** | **Exclure** du futur process catalogue auto |

---

## Tableau de notation MOA

| # | Référence | G1 | G2 | G3 | G4 | G5 | G6 | Décision E/R/M/X | Notes |
|---|-----------|----|----|----|----|----|----|------------------|-------|
| 1 | Crackers — avant retouche | 4 | 3 | 3 | 3 | 4 | 3 | R | Produit lisible ; réserve sur ligne noire basse et cadrage plein cadre |
| 2 | Crackers — retouché | 4 | 3 | 3 | 3 | 4 | 3 | R | Exploitable sous réserve ; ligne noire et poids visuel à valider |
| 3 | Pâtes Mayotte | 3 | 2 | 2 | 1 | 2 | 2 | M | Artefacts forts de fond à droite et en bas ; reprise requise |
| 4 | Coffret bois | 4 | 4 | 4 | 4 | 4 | 4 | E | Cohérent, premium, exploitable tel quel |
| 5 | Pochette curry | 4 | 3 | 3 | 2 | 4 | 3 | R | Produit lisible ; artefacts de fond visibles, acceptable avec réserve |
| 6 | Pot goyave | 4 | 3 | 3 | 2 | 4 | 2 | M | Produit lisible mais artefacts bas/table trop visibles |
| 7 | Sauce scotch bonnet | 4 | 4 | 4 | 3 | 4 | 3 | R | Bon impact produit ; réserve sur découpe de scène et couture fond |

*(CSV complété MOA 2026-05-20.)*

---

## Décision globale post-revue (MOA)

Cocher **une** option :

```text
[ ] 1 — Adopter ck_shop_tile_v1.1 comme recette candidate POC
[x] 2 — Adopter v1.1 + relancer batch complet 21 images proxy
[ ] 3 — Ajuster encore la règle plein cadre (préciser : _____________)
[ ] 4 — Autre : _____________
```

### Synthèse MOA P3 ciblé (2026-05-20)

| Décision | Nombre | Lecture |
|----------|-------:|---------|
| E — Exploitable | 1 | Le plein cadre peut produire une tuile directement exploitable |
| R — Acceptable avec réserve | 4 | Le statut `NEEDS_REVIEW` est utile comme sas de contrôle humain |
| M — Reprise manuelle | 2 | Le moteur signale correctement des cas à ne pas valider automatiquement |
| X — Exclure | 0 | Aucun cas à exclure définitivement sur cette revue |

**Conclusion** : majorité `E/R` (**5/7**). Le calibrage `ck_shop_tile_v1.1` est accepté comme recette candidate de revue, mais ne vaut pas GO POC final.

**Signal MOA** :

```text
GO clôture P3 ciblé — 7 NEEDS_REVIEW notés — décision 2
```

**Suite autorisée côté Dev** : relancer le batch complet des 21 images proxy en `ck_shop_tile_v1.1`, puis comparer les statuts et la grille. Toujours **pas de code Odoo** et **pas de GO POC final** à ce stade.

---

## Contexte comparatif (optionnel)

Pour juger G3, comparer avec tuiles **OK** du batch proxy v1 :

- `homepage_maniocookies_sale_la_platine.png`
- `homepage_manioc_crackers_sale_ste_anne.png`

Grilles mock (si disponibles) :

- `tools/ck_image_normalizer/reports/mock_grid_*_desktop_mobile.html`

---

## Rappels

- Pas de code Odoo
- Pas de remplacement `image_1920`
- P0 (21 refs) — lot aligné banque assets

---

## Clôture P3 ciblé

Quand le tableau et le CSV sont complétés, signaler :

```text
GO clôture P3 ciblé — 7 NEEDS_REVIEW notés — décision [1/2/3/4]
```
