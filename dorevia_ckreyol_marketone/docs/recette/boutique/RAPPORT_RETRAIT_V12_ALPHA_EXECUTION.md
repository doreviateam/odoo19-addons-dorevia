# Rapport exécution — Retrait v1.2-alpha — R1→R5

| Champ | Valeur |
|-------|--------|
| **Décision MOA** | **GO retrait v1.2-alpha R1→R5** |
| **Date exécution** | 2026-05-20 |
| **Base** | `ckr-marketone-01` |
| **Flag** | `marketone.shop_tile_enabled = True` |
| **Plan source** | [`PLAN_RETRAIT_V12_ALPHA_MOA.md`](./PLAN_RETRAIT_V12_ALPHA_MOA.md) |
| **Manifest import** | [`import_retrait_alpha_v11_9.csv`](./import_retrait_alpha_v11_9.csv) |

---

## Signal MOA

```text
GO retrait v1.2-alpha R1→R5 — retour doctrine image pleine sans transparence — v1.1 reste recette active.
```

---

## R1 — Retrait flux alpha CLI

| Action | Statut | Détail |
|--------|--------|--------|
| Recette `ck_shop_tile_v1.2-alpha.yaml` | ✅ | Marquée `deprecated: true` |
| Blocage CLI `ck_image_normalizer run` | ✅ | Refus recette alpha / fond transparent |
| Blocage import `import_shop_tiles.py` | ✅ | Rejet `ck_shop_tile_v1.2-alpha` + PNG/WebP |
| Scripts P8 archivés | ✅ | Bannière DEPRECATED + `archive/README_DEPRECATED_V12_ALPHA.md` |
| Commit auto import Odoo | ✅ | `env.cr.commit()` ajouté sur `apply=True` |

**Vérification blocage alpha** :

```bash
python3 scripts/import_shop_tiles.py --manifest docs/recette/boutique/import_p8_packshots_alpha_9.csv
# → ERROR recette alpha retirée + format PNG interdit (9 lignes)
```

```bash
.venv/bin/python -m ck_image_normalizer run --recipe recipes/ck_shop_tile_v1.2-alpha.yaml ...
# → Recette retirée du flux actif : ck_shop_tile_v1.2-alpha
```

---

## R2 — Rebasculage Odoo (9 produits alpha → v1.1)

Import apply (JPEG pilote P7, sans retraitement) :

| ID | Produit | Recette | Statut | Note MOA |
|---:|---------|---------|--------|----------|
| 7 | Maniocookies salés La Platine | `ck_shop_tile_v1.1` | `validated_reserve` | RETRAIT_ALPHA_MOA — surveillance qualité source |
| 8 | Crackers manioc Sainte-Anne | `ck_shop_tile_v1.1` | `validated` | RETRAIT_ALPHA_MOA |
| 155 | Shrub agrumes créole | `ck_shop_tile_v1.1` | `validated` | RETRAIT_ALPHA_MOA |
| 163 | Mix beignets manioc | `ck_shop_tile_v1.1` | `validated_reserve` | RETRAIT_ALPHA_MOA — surveillance qualité source |
| 183 | Chips banane plantain salées | `ck_shop_tile_v1.1` | `validated` | RETRAIT_ALPHA_MOA |
| 187 | Marinade jerk authentique | `ck_shop_tile_v1.1` | `validated` | RETRAIT_ALPHA_MOA |
| 470 | Marinade jerk citron vert | `ck_shop_tile_v1.1` | `validated` | RETRAIT_ALPHA_MOA |
| 472 | Palettes coco vanille | `ck_shop_tile_v1.1` | `validated_reserve` | RETRAIT_ALPHA_MOA — surveillance qualité source |
| 473 | Chips patate douce créole | `ck_shop_tile_v1.1` | `validated` | RETRAIT_ALPHA_MOA |

---

## R3 — Frontend (rendu image pleine uniforme)

| Fichier | Action |
|---------|--------|
| `static/src/scss/_shop_product_cards.scss` | Commentaires alpha retirés · doctrine **image pleine v1.1** confirmée |
| `views/pages/shop_product_tile_image.xml` | Inchangé — rendu unique `marketone-shop-tile-photo` pour toutes tuiles dérivées |

Pas de branche alpha-specific restante. Toutes les tuiles `image_shop_tile` utilisent le même rendu cover + masque 14 px.

**Action sandbox** : redémarrer Odoo ou `-u dorevia_ckreyol_marketone` si assets SCSS non rechargés automatiquement.

---

## R4 — Documentation / ADR / tickets

| Document | Mise à jour |
|----------|-------------|
| `PLAN_RETRAIT_V12_ALPHA_MOA.md` | Statut → **Exécuté** |
| `DECISIONS.md` ADR-033 | Amendement STOP v1.2-alpha |
| `TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_2_ALPHA_P8.md` | Clôturé — STOP alpha |
| `RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_V1_5_SHOP_TILE.md` | Doctrine v1.1 seule |
| `archive/README_DEPRECATED_V12_ALPHA.md` | Archive scripts P8 |

---

## R5 — État final base

| Indicateur | Avant | Après |
|-----------|------:|------:|
| Produits `ck_shop_tile_v1.2-alpha` | 9 | **0** |
| Tuiles `ck_shop_tile_v1.1` actives | 31 | **40** |
| Tuiles dérivées totales | 40 | **40** |
| Import PNG alpha actif | oui | **non** |

```text
ALPHA_COUNT 0
V11_TILE 40
TOTAL_TILE 40
SHOP_TILE_ENABLED True
```

---

## Produits en fallback ou gouvernance source (inchangés)

### Fallback temporaire P1/P2 (sans `image_shop_tile`)

| ID | Produit | Motif |
|---:|---------|-------|
| 154 | Colombo des Antilles (épices) | P1 — effet rectangle interne |
| 156 | Biscuits coco vanille | P2 — NEEDS_REVIEW_SOURCE |
| 471 | Biscuits banane confiture | P2 — NEEDS_REVIEW_SOURCE |

### Surveillance qualité source post-retrait alpha (3)

| ID | Produit | Statut |
|---:|---------|--------|
| 7 | Maniocookies salés La Platine | `validated_reserve` |
| 163 | Mix beignets manioc | `validated_reserve` |
| 472 | Palettes coco vanille | `validated_reserve` |

### Lot B — NEEDS_REVIEW_SOURCE (5 lifestyle, v1.1 maintenu)

Gouvernance source documentée — pas de retraitement massif · pas d'alpha.

---

## Capture /shop — contrôle MOA

Contrôle visuel recommandé sur sandbox `http://localhost:18079` :

- plus aucun produit avec rendu « produit flottant sur fond conteneur » ;
- tuiles rebasculées : Maniocookies, Crackers, Shrub, Mix beignets, Chips banane, Marinades, Palettes coco, Chips patate douce ;
- vérifier les 3 `validated_reserve` post-retrait.

*(Route `/shop` non accessible en HTTP direct sur ce sandbox au moment de l'exécution — revue MOA via navigateur connecté ou environnement publié.)*

---

## Garde-fous confirmés

- `image_1920` inchangé ✅
- pas d'IA / rembg ✅
- pas de cron ✅
- pas de traitement massif ✅
- pas de modification fiche produit (hors champs tuile dérivée) ✅
- rollback via `marketone.shop_tile_enabled` ✅
- scope `/shop` uniquement ✅

---

## Doctrine finale active

```text
ck_shop_tile_v1.1 = recette active unique
image pleine · sans transparence · sans alpha · sans détourage
problème rectangle → source / recadrage / fallback
```

**Signal Dev clôture** :

```text
RETRAIT v1.2-alpha exécuté R1→R5 — 0 alpha actif — 40 tuiles v1.1 — import PNG alpha bloqué.
```
