# Plan de retrait — v1.2-alpha — STOP transparence

| Champ | Valeur |
|-------|--------|
| **Décision MOA** | **STOP v1.2-alpha** — abandon fond transparent |
| **Date** | 2026-05-20 |
| **Statut** | **Exécuté Dev** — GO MOA R1→R5 (2026-05-20) |
| **Base actuelle** | `ckr-marketone-01` · `marketone.shop_tile_enabled = True` |
| **Contexte amont** | P8 hybride clôturé · P1/P2 fallback rectangle exécutés (3 produits) |

---

## Signal MOA

```text
STOP v1.2-alpha — suppression de la possibilité de fond transparent — retour à une doctrine image pleine sans alpha.
```

---

## Doctrine cible (post-alpha)

```text
Image source correcte     → normalisation image pleine (ck_shop_tile_v1.1)
Image mal cadrée          → recadrage source
Image non adaptée         → fallback image_1920 ou demande fournisseur
Lifestyle                 → image pleine bord à bord
Packshot                  → image pleine propre, jamais alpha
image_1920                → master inchangé
image_shop_tile           → dérivé tuile /shop, sans transparence
```

**Règle visuelle tuile `/shop`** :

- l'image remplit la zone photo ;
- pas d'effet « image dans l'image » ;
- pas de carré interne visible ;
- **pas de fond transparent** ;
- pas de détourage alpha / halo / produit flottant.

---

## État actuel (inventaire Dev)

| Indicateur | Valeur |
|-----------|--------|
| Produits encore en `ck_shop_tile_v1.2-alpha` | **9** |
| Tuiles dérivées actives (`image_shop_tile`) | **40** (43 − 3 fallback P1/P2) |
| Tuiles `v1.1` actives | **31** |
| Fallback temporaire P1/P2 (sans tuile) | **3** (Colombo, Biscuits coco, Biscuits banane) |

---

## Les 9 produits alpha — proposition par cas

Sources v1.1 existantes : run `pilote_20260520` / `import_pilote_43_shop_tiles.csv` (JPEG baked-in déjà produits).

| # | Produit | ID | Rendu alpha (audit) | Action proposée | Fallback si NON OK v1.1 |
|---|---------|---:|---------------------|-----------------|-------------------------|
| 1 | Crackers manioc Sainte-Anne | 8 | OK (bbox 0.53) | **Retour v1.1** — réimport JPEG pilote | Recadrage source si rectangle revient |
| 2 | Chips banane plantain salées | 183 | OK (0.53) | **Retour v1.1** | — |
| 3 | Chips patate douce créole | 473 | OK (0.53) | **Retour v1.1** | — |
| 4 | Shrub agrumes créole | 155 | OK (0.58) | **Retour v1.1** | — |
| 5 | Marinade jerk authentique | 187 | OK (0.58) | **Retour v1.1** | — |
| 6 | Marinade jerk citron vert | 470 | OK (0.58) | **Retour v1.1** | — |
| 7 | Maniocookies salés La Platine | 7 | Présence faible (0.32) | **Retour v1.1** + `validated_reserve` | Fallback `image_1920` si rectangle |
| 8 | Mix beignets manioc | 163 | Présence faible (0.32) | **Retour v1.1** + `validated_reserve` | Fallback si rectangle |
| 9 | Palettes coco vanille | 472 | Présence faible (0.32) | **Retour v1.1** + `validated_reserve` | Fallback si rectangle |

**Principe** : réutiliser les **JPEG v1.1 déjà validés MOA** au pilote P7 — pas de retraitement créatif, pas de nouvelle recette.

---

## Plan de retrait en 5 phases (sans exécution immédiate)

### Phase R0 — Validation MOA du plan (cette étape)

- MOA valide ce document.
- **Aucune modification base / CLI / import** avant GO explicite.

### Phase R1 — Retrait flux alpha (CLI + garde-fous import)

| Action | Fichier / zone | Détail |
|--------|----------------|--------|
| R1.1 | `recipes/ck_shop_tile_v1.2-alpha.yaml` | Marquer **DEPRECATED** · retirer du catalogue actif opérateur |
| R1.2 | `scripts/import_shop_tiles.py` | **Rejeter** manifest si `recipe_version = ck_shop_tile_v1.2-alpha` ou format PNG alpha |
| R1.3 | `processor.py` / `recipe.py` | Conserver code alpha en **legacy non exposé** (rollback technique possible) ou retirer branche alpha si MOA le demande |
| R1.4 | Scripts P8 | `run_p8_packshot_alpha*.py`, `poc_v12_alpha.py` → dossier archive / README « deprecated » |
| R1.5 | Doc opérateur | `RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_V1_5_SHOP_TILE.md` — retirer toute mention alpha active |

**Hors scope R1** : suppression historique P8 (tickets, rapports POC) — archivage documentaire seulement.

### Phase R2 — Rebasculage Odoo des 9 produits alpha → v1.1

| Action | Détail |
|--------|--------|
| R2.1 | Générer manifest `import_retrait_alpha_v11_9.csv` (9 lignes JPEG v1.1 pilote) |
| R2.2 | Dry-run import obligatoire |
| R2.3 | Apply import : écraser `image_shop_tile` PNG alpha par JPEG v1.1 |
| R2.4 | Mettre à jour `shop_tile_recipe_version = ck_shop_tile_v1.1` sur les 9 produits |
| R2.5 | Notes MOA : `RETRAIT_ALPHA_MOA — retour v1.1 image pleine` |

**Résultat attendu** : **0 produit** en `ck_shop_tile_v1.2-alpha` · **40 tuiles** toutes en v1.1 (ou fallback).

### Phase R3 — Frontend (simplification rendu)

| Action | Fichier | Détail |
|--------|---------|--------|
| R3.1 | `_shop_product_cards.scss` | Réviser branche `.marketone-shop-tile-photo` — objectif : rendu **image pleine** uniforme v1.1 |
| R3.2 | `shop_product_tile_image.xml` | Conserver logique `image_shop_tile` · retirer distinction alpha si devenue inutile |
| R3.3 | QWeb | Vérifier que plus aucune tuile ne sert de PNG transparent |

**Note** : le masque CSS 14 px + zoom reste utile pour certains v1.1 baked-in ; à réévaluer visuellement post-R2.

### Phase R4 — Documentation & ADR

| Document | Action |
|----------|--------|
| `TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_2_ALPHA_P8.md` | Statut → **Clôturé MOA — STOP alpha** |
| `TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION.md` | Doctrine → **v1.1 seule** |
| `DECISIONS.md` ADR-033 | Ajouter amendement **STOP v1.2-alpha** |
| `NOTE_CK_IMAGE_NORMALIZER_V1_2_TRANSPARENT_PROPOSAL.md` | Marquer **historique / non retenu** |
| `RAPPORT_POC_V1_2_ALPHA_3_PACKSHOTS.md` | Conserver comme leçon apprise |

### Phase R5 — Revue MOA finale

- Capture `/shop` après R2 + R3.
- Vérifier absence PNG alpha dans HTML (`image_shop_tile` = JPEG uniquement).
- Confirmer : plus d'effet « produit flottant sur fond conteneur ».
- Arbitrer cas v1.1 encore NON OK (rectangle) → gouvernance source / fallback (comme P1/P2).

---

## Critères d'acceptation post-retrait

| Critère | Seuil |
|---------|-------|
| Produits `shop_tile_recipe_version = ck_shop_tile_v1.2-alpha` | **0** |
| Import PNG alpha dans `image_shop_tile` | **interdit** |
| Recette active opérateur | **`ck_shop_tile_v1.1` uniquement** |
| `image_1920` master | **inchangé** |
| Tests T1–T7 | **verts** |
| Rollback flag | **opérationnel** |

---

## Garde-fous maintenus

- `image_1920` inchangé
- pas d'IA / rembg
- pas de cron
- pas de traitement massif
- pas de modification fiche produit (hors champs tuile dérivée)
- rollback via `marketone.shop_tile_enabled`
- usage limité à `/shop`
- lot X inchangé

---

## Risques & mitigations

| Risque | Mitigation |
|--------|------------|
| Retour v1.1 réintroduit effet rectangle sur packshots | Revue MOA cas par cas · fallback ou source |
| Régression visuelle Crackers (excellent en alpha) | Accepter trade-off MOA · ou recadrage source packshot plein cadre |
| Code alpha mort dans CLI | Legacy commenté ou branche isolée · pas supprimé brutalement sans MOA |
| CSS alpha-specific incohérent | Phase R3 ciblée post-import |

---

## Effort indicatif

| Phase | Effort Dev | Effort MOA |
|-------|-----------|------------|
| R0 validation plan | — | 30 min |
| R1 retrait flux CLI | 2–3 h | — |
| R2 rebasculage 9 produits | 1–2 h | 30 min revue |
| R3 frontend | 1–2 h | 30 min revue |
| R4 documentation | 1 h | — |
| R5 revue finale | — | 1 h |
| **Total** | **5–8 h** | **2 h** |

---

## Décision attendue MOA

```text
GO plan retrait alpha R1→R5 — exécution autorisée après validation de ce document.
```

ou

```text
GO partiel — R2 seul (rebasculage 9 produits) — R1/R3/R4 ensuite.
```

**Signal Dev (état actuel)** :

```text
Plan retrait v1.2-alpha proposé — 9 produits identifiés — doctrine image pleine sans alpha — en attente GO MOA avant exécution.
```
