# TICKET — Test `test_t5_import_manifest_validates_offline` (JPEG pilotes absents)

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_TEST_T5_IMPORT_JPEG_PILOTE` |
| **Type** | **Tech debt / environnement de test** — hors périmètre fonctionnel |
| **Statut** | **Ouvert** — backlog maintenance |
| **Priorité** | Basse — **ne bloque pas** les lots BO ni la reprise front (ADR-034) |
| **Base** | `ckr-marketone-01` |
| **Référence** | Réserve lot BO `19.0.16.0.0` · [`RECEPTION_MOA_LOT_RECADRAGE_BO.md`](../../cadrage2/RECEPTION_MOA_LOT_RECADRAGE_BO.md) |

---

## Contexte

Lors de l'exécution de la suite `dorevia_marketone_shop_tile` :

| Résultat | Détail |
|----------|--------|
| **11/12 OK** | Tests HTTP grille / fiche / modèle tuile |
| **1 échec** | `test_t5_import_manifest_validates_offline` |

**Cause** : le manifest CSV référence des fichiers JPEG sous `tools/ck_image_normalizer/reports/runs/…` absents de l'environnement de test / du dépôt sandbox.

**Périmètre BO** : confirmé **hors périmètre** par la MOA — ne remet pas en cause le GO avec réserves du lot `19.0.16.0.0`.

---

## Risque si non traité

- Masquer une **future régression** sur le script `scripts/import_shop_tiles.py` lors des campagnes CI complètes.
- Faux signal rouge sur `dorevia_marketone_shop_tile` en recette globale.

---

## Fichiers concernés

| Fichier | Rôle |
|---------|------|
| `tests/test_marketone_shop_tile_image.py` | Test `test_t5_import_manifest_validates_offline` |
| `scripts/import_shop_tiles.py` | Script import batch |
| `docs/recette/boutique/import_pilote_43_shop_tiles.csv` | Manifest pilote |
| `tools/ck_image_normalizer/…` | JPEG sources (absents env test) |

---

## Options de résolution (à arbitrer Dev)

| Option | Description | Effort |
|--------|-------------|--------|
| **A — Fixtures minimales** | Copier ou générer 1–2 JPEG factices dans un dossier `tests/fixtures/shop_tiles/` · adapter le test pour un manifest de test dédié | Faible |
| **B — Skip conditionnel** | `@unittest.skipUnless(path.exists(), …)` si JPEG pilotes absents · documenter prérequis recette image | Très faible |
| **C — Tag séparé** | Exclure `test_t5` du tag `dorevia_marketone_shop_tile` par défaut · tag `dorevia_marketone_shop_tile_import` pour recette image complète | Faible |
| **D — Submodule / artefact CI** | Publier le pack JPEG pilote comme artefact CI ou submodule optionnel | Moyen |

**Recommandation Dev** : **Option A + C** — fixtures locales pour CI · tag séparé pour recette pilote média complète.

---

## Critères de clôture

- [ ] `dorevia_marketone_shop_tile` : **0 échec** sur CI standard (sans prérequis externe).
- [ ] Recette import pilote documentée si exécution hors CI (commande + prérequis fichiers).
- [ ] Aucun impact sur le comportement front `/shop` ni sur `marketone_use_shop_tile_on_grid()`.

---

## Non-régression obligatoire à la clôture

- Rejouer `dorevia_marketone_bo` + tests HTTP tuile (`test_t1`–`test_t4` de `TestMarketoneShopTileHttp`).
- Vérifier [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md) § B4 (tuile grille).

---

## Verdict MOA

| Date | Verdict | Commentaire |
|------|---------|-------------|
| | ☐ GO · ☐ Report | Backlog séparé — non bloquant cadrage2 |
