# Réponse MOA — CK Image Normalizer — GO cadrage pilote média

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-05-20 |
| **Ticket** | [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md`](../../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md) |
| **Décision** | **GO cadrage pilote média catalogue** |
| **Volume retenu** | **50 SKU** (extension 75 si préparation fluide) |

---

## Décision

La proposition post-POC est validée : passer du POC CLI (**GO avec réserves**) à un **pilote média catalogue**, sans intégration Odoo.

```text
GO cadrage pilote média catalogue
Pas de GO implémentation Odoo
Pas de traitement massif catalogue
Pas de remplacement image_1920
```

Le pilote reste strictement :

- hors module Odoo ;
- hors remplacement `image_1920` ;
- hors traitement massif catalogue ;
- limité aux tuiles commerce `/shop` ;
- basé sur `ck_shop_tile_v1.1`.

---

## Volume pilote

Approche prudente : **50 SKU** en premier lot.

La cible **75 SKU** reste possible en extension si la préparation est fluide.

Mesures attendues :

- temps opérateur réel ;
- taux OK / WARN / REVIEW / REJECTED ;
- charge revue humaine ;
- volume reprises manuelles ;
- qualité visuelle grille.

---

## Composition et seuils — validés

- ~**70 %** packshots · ~**30 %** lifestyle / complexe ;
- cas difficiles volontaires inclus ;
- exclusion images POC (sauf reprises ciblées) ;
- seuils GO pilote § ticket (55 % / 15 % / 35 % / 20 % reprises).

---

## Flux opérateur — validé

| Statut | Décision MOA |
|--------|--------------|
| `OK` | Utilisable après contrôle rapide |
| `OK_WITH_WARNINGS` | Utilisable avec vérification |
| `NEEDS_REVIEW` | Revue humaine · E/R/M/X |
| `REJECTED` | Non utilisable sans reprise source |

Suivi temps opérateur requis — fichier `pilote_operateur.csv`.

---

## V1.5 Odoo lite

**Hors périmètre.** Cadrage possible **après** pilote si gain visuel · flux tenable · recette stable · reprises acceptables.

---

## Signal de lancement exécution (P3)

```text
GO exécution pilote média — 50 SKU sélectionnés — manifest prêt
```

---

## Préparation Dev livrée

| Livrable | Chemin |
|----------|--------|
| Dossier pilote | `tools/ck_image_normalizer/input/pilote/` |
| Template manifest | `tools/ck_image_normalizer/manifest.pilote.template.csv` |
| Template suivi opérateur | `tools/ck_image_normalizer/pilote_operateur.template.csv` |
| Procédure MOA | `tools/ck_image_normalizer/input/pilote/README.md` |

**Validé par** : MOA · **Date** : 2026-05-20
