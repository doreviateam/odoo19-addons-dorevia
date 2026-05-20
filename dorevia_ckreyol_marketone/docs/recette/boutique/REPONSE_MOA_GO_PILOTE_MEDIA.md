# Réponse MOA — CK Image Normalizer — GO pilote média catalogue

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-05-20 |
| **Ticket** | [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md`](../../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md) |
| **Décision** | **GO pilote média catalogue** |
| **Volume** | **50 SKU** (initial) |
| **Recette** | `ck_shop_tile_v1.1` |

---

## Décision

Après validation du cadrage et de la préparation Dev, nous actons le lancement du **pilote média catalogue** :

```text
GO pilote média catalogue — volume initial 50 SKU
Recette : ck_shop_tile_v1.1
Périmètre : tuiles commerce /shop uniquement
Aucun code Odoo
Aucun remplacement image_1920
Aucune industrialisation automatique
```

---

## Garde-fous confirmés

| Règle | Statut |
|-------|--------|
| Hors module Odoo | ✅ |
| Pas de remplacement `image_1920` | ✅ |
| Pas de traitement massif catalogue | ✅ |
| Pas de cron / intégration auto | ✅ |
| Tuiles `/shop` uniquement | ✅ |
| Recette `ck_shop_tile_v1.1` | ✅ |

---

## Suite immédiate

| Phase | Responsable | Action |
|-------|-------------|--------|
| **P1** | MOA | Sélection **50 SKU** · export images → `input/pilote/` |
| **P2** | MOA | Compléter `manifest.pilote.csv` |
| **P3** | Dev | Batch CLI + grilles — **après signal exécution** |

**Signal Dev pour lancer le batch (P3)** :

```text
GO exécution pilote média — 50 SKU sélectionnés — manifest prêt
```

Le **GO pilote** autorise la phase ; le **GO exécution** déclenche le run technique une fois le lot prêt.

---

## Références

- Cadrage validé : [`REPONSE_MOA_GO_CADRAGE_PILOTE_MEDIA.md`](./REPONSE_MOA_GO_CADRAGE_PILOTE_MEDIA.md)
- Procédure MOA : [`tools/ck_image_normalizer/input/pilote/README.md`](../../../../tools/ck_image_normalizer/input/pilote/README.md)
- POC clôturé : [`REPONSE_MOA_GO_POC_IMAGE_NORMALIZER_V1_1.md`](./REPONSE_MOA_GO_POC_IMAGE_NORMALIZER_V1_1.md)

**Validé par** : MOA · **Date** : 2026-05-20
