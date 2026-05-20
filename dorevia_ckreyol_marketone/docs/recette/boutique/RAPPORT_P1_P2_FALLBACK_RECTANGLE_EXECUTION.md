# Rapport exécution — P1 + P2 — fallback rectangle interne

| Champ | Valeur |
|-------|--------|
| **Décision MOA** | GO P1 + GO P2 |
| **Date exécution** | 2026-05-20 |
| **Base** | `ckr-marketone-01` |
| **Flag** | `marketone.shop_tile_enabled = True` |
| **Script** | `scripts/apply_p1_p2_fallback_temp.py` |

---

## 1) Actions exécutées

### P1 — Colombo des Antilles (`product_id=154`)

| Avant | Après |
|-------|-------|
| `image_shop_tile` présent | **`image_shop_tile` vidé** |
| `marketone_use_shop_tile_on_grid()` = True | **False** → fallback `image_1920` |
| statut `validated` | `pending_review` |

Note MOA : `FALLBACK_TEMP_P1_MOA — retrait image_shop_tile · effet rectangle interne · fallback image_1920`

### P2 — Biscuits coco vanille (`156`) + Biscuits banane confiture (`471`)

| Produit | Avant | Après |
|---------|-------|-------|
| Biscuits coco vanille (156) | tuile dérivée active | **`image_shop_tile` vidé** · fallback `image_1920` |
| Biscuits banane confiture (471) | tuile dérivée active | **`image_shop_tile` vidé** · fallback `image_1920` |

Note MOA : `FALLBACK_TEMP_P2_MOA — fallback image_1920 · NEEDS_REVIEW_SOURCE · effet rectangle interne`

---

## 2) État final

| Indicateur | Valeur |
|-----------|--------|
| Tuiles dérivées actives (`image_shop_tile`) | **40** (43 − 3 fallback) |
| `image_1920` master | **inchangé** sur les 3 produits |
| Rollback flag | **maintenu** |
| Autres cas Lot B / A2 | **aucune action** (gouvernance source) |
| Packshots alpha Lot A | **maintien avec réserve** (aucun retrait) |

---

## 3) Produits sans action (confirmé MOA)

- Pâtes de manioc Mayotte (9)
- Coffret biscuits et douceurs (188)
- Semoule manioc fine Mayotte (184)
- Pochette curry des Antilles (469)
- Palets manioc La Platine (178)

---

## 4) Garde-fous confirmés

- `image_1920` inchangé
- pas d'alpha sur lifestyle
- pas d'IA / rembg
- pas de cron / pas de traitement massif
- pas de modification fiche produit (hors champs tuile dérivée)
- rollback via flag maintenu

---

## 5) Capture /shop

Contrôle recommandé MOA sur `/shop` :

- Colombo des Antilles → image standard (plus de tuile dérivée)
- Biscuits coco vanille → image standard
- Biscuits banane confiture → image standard

---

## Signal Dev

```text
P1 + P2 exécutés — Colombo + Biscuits coco + Biscuits banane en fallback image_1920 — 40 tuiles dérivées restantes — garde-fous maintenus.
```
