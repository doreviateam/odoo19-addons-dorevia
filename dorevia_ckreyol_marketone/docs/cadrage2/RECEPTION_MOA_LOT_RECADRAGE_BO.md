# Réception MOA — Lot recadrage BO produit `19.0.16.0.0`

| Champ | Valeur |
|-------|--------|
| **Version** | `19.0.16.0.0` |
| **Date réception** | 2026-06-08 |
| **Décision initiale** | [`DECISION_MOA_RECADRAGE_BO.md`](./DECISION_MOA_RECADRAGE_BO.md) |
| **Livraison Dev** | [`NOTE_LIVRAISON_LOT_RECADRAGE_BO.md`](./NOTE_LIVRAISON_LOT_RECADRAGE_BO.md) |
| **Recette manuelle** | [`RECETTE_MANUELLE_RECADRAGE_BO_PRODUIT.md`](./RECETTE_MANUELLE_RECADRAGE_BO_PRODUIT.md) |
| **Verdict livraison** | **Reçu — GO recette manuelle** |
| **Verdict recette R1–F5** | **GO avec réserves** (2026-06-08) |
| **Clôture lot** | **GO avec réserves MOA** |

---

## Réponse MOA

Lot `19.0.16.0.0` bien reçu.

La livraison respecte le périmètre demandé : recadrage BO produit uniquement, sans modification front, sans nouvelle logique `/shop`, sans changement contrôleur, QWeb front ou assets.

### Points validés à la lecture

- fiche produit restructurée en 4 onglets CK ;
- bloc **« Tuile commerce /shop »** retiré de la zone image principale ;
- libellés métier côté utilisateur ;
- champs batch regroupés dans l'onglet **Technique** avec restriction `base.group_no_one` ;
- `image_shop_tile` conservé comme dérivé média contrôlé ;
- logique front `marketone_use_shop_tile_on_grid()` inchangée ;
- documentation de livraison et recette manuelle présentes.

### Résultat tests (prise de note MOA)

| Suite | Résultat | Commentaire MOA |
|-------|----------|-----------------|
| `dorevia_marketone_bo` | **OK** | Valide le lot BO |
| `dorevia_marketone_shop_tile` | 1 échec pré-existant | Hors périmètre BO — suivi backlog séparé |

---

## Décision

**GO recette MOA manuelle** sur `ckr-marketone-01`, selon [`RECETTE_MANUELLE_RECADRAGE_BO_PRODUIT.md`](./RECETTE_MANUELLE_RECADRAGE_BO_PRODUIT.md).

### Clôture recette (2026-06-08)

**Verdict final : GO avec réserves.**

| Zone | Résultat |
|------|----------|
| Tests `dorevia_marketone_bo` | **9/9 OK** |
| Tests `dorevia_marketone_shop_tile` | **11/12 OK** |
| Grille BO R1–R11 | **Validée** |
| Grille front F1–F5 | **Validée** |

Réserve unique : `test_t5_import_manifest_validates_offline` (JPEG pilotes absents) — **hors périmètre BO**, identifié pour backlog technique / environnement de test.

---

## Réserve MOA

L'échec `test_t5_import_manifest_validates_offline` **ne bloque pas** ce lot BO, mais doit rester identifié dans le **backlog technique / environnement de test**, pour éviter qu'il ne masque de futures régressions.

| Élément | Détail |
|---------|--------|
| Test | `tests/test_marketone_shop_tile_image.py` · `test_t5_import_manifest_validates_offline` |
| Cause | Fichiers JPEG pilote absents de l'environnement (`tools/ck_image_normalizer/…`) |
| Action | Ticket maintenance [`TICKET_MARKETONE_TEST_T5_IMPORT_JPEG_PILOTE.md`](../tickets/maintenance/TICKET_MARKETONE_TEST_T5_IMPORT_JPEG_PILOTE.md) |

---

## Prochaine étape

~~1. Exécuter la recette **R1–R11** (BO) + **F1–F5** (`/shop`) sur `ckr-marketone-01`.~~  
~~2. Renseigner le verdict dans la recette manuelle.~~  
~~3. Clôturer le lot : **GO**, **GO avec réserves** ou **NO GO**.~~

**Lot clôturé** — voir verdict dans [`RECETTE_MANUELLE_RECADRAGE_BO_PRODUIT.md`](./RECETTE_MANUELLE_RECADRAGE_BO_PRODUIT.md).

Backlog séparé (non bloquant) : corriger l'environnement ou les fixtures du test `test_t5_import_manifest_validates_offline`.

---

## Chaîne documentaire cadrage2

```text
README (directive)
  → RETOUR_EXPERT
  → DECISION_MOA
  → PROPOSITION_DEV
  → NOTE_LIVRAISON (19.0.16.0.0)
  → RECEPTION_MOA (ce document) ← GO recette manuelle
  → RECETTE_MANUELLE → GO avec réserves MOA (2026-06-08) ✓
```
