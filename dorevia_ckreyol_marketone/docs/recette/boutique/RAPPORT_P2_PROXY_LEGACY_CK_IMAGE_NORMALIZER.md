# Rapport — P2 proxy legacy — CK Image Normalizer POC

| Champ | Valeur |
|-------|--------|
| **Type** | Batch **legacy v1** — 21 PNG banque marketplace (lot officiel POC après révision MOA) |
| **Date batch** | 2026-05-20 |
| **Recette** | `ck_shop_tile_v1` |
| **Source** | `odoo19-addons-dorevia/dorevia_ckreyol_marketplace/docs/assets/` (21 PNG) |
| **Rapport technique** | `tools/ck_image_normalizer/reports/batch_20260520T105124Z.json` |
| **Ticket** | [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_POC.md`](../../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_POC.md) |

> **Révision MOA 2026-05-20** : l’échantillon officiel POC est **21 références** (banque `marketplace/docs/assets`). Ce rapport P2 v1 reste l’historique du premier batch ; le lot de décision est le **batch v1.1** ([`RAPPORT_V1_1_BATCH_21_PROXY.md`](./RAPPORT_V1_1_BATCH_21_PROXY.md)).

> *(Historique)* Ce batch était initialement qualifié de **proxy technique** en attendant un lot MOA de 30 refs. Cette attente est **levée** — 21 refs = lot officiel.

---

## Synthèse résultats (automatique Dev)

| Métrique | Valeur | Seuil GO POC |
|----------|--------|--------------|
| **Total** | 21 | 21 (cible MOA) |
| **OK** | 13 | — |
| **OK_WITH_WARNINGS** | 1 | — |
| **NEEDS_REVIEW** | 0 | — |
| **REJECTED** | 7 | — |
| **OK rate** | **67 %** | ≥ 60 % ✅ |
| **Rejected rate** | **33 %** | ≤ 10 % ❌ |
| **GO candidate (auto)** | **non** | — |

---

## Lecture Dev

### Ce que le proxy démontre

1. **Le moteur produit des sorties exploitables** sur packshots fond clair propres (`homepage_maniocookies_*`, `homepage_manioc_crackers_*`).
2. **Le profil `lifestyle` est conservateur** — 12/12 lifestyle/hero → `OK` (pas de replace bg agressif).
3. **Les rejets packshot sont majoritairement heuristiques** — 7/7 `REJECTED` ont `content_area_ratio ≥ 0.99` (*« produit très proche des bords source »*), pas une dégradation visuelle avérée.
4. **Les tuiles sont produites même en `REJECTED`** — previews disponibles pour arbitrage MOA visuel.

### Causes des 7 REJECTED (packshot)

| Fichier | Ratio | Cause probable |
|---------|-------|----------------|
| `exemple_produit_manioc_crackers_la_platine*.png` | 1.0 | Produit plein cadre / fond non isolé |
| `homepage_manioc_pates_mayotte_la_platine.png` | 1.0 | Verticalité + bords source |
| `mvp02_reference_coffret_gourmand_bois.png` | 0.997 | Coffret multi-produits plein cadre |
| `stitch_curry_powder_pouch.png` | 1.0 | Export Stitch plein cadre |
| `stitch_guava_jam_jar.png` | 1.0 | Export Stitch plein cadre |
| `stitch_scotch_bonnet_sauce.png` | 1.0 | Export Stitch plein cadre |

**Interprétation** : les exports `stitch_*` et certaines refs MVP02 ne sont **pas des packshots source** au sens recette — le rejet auto est **cohérent**, pas un bug.

### Limites du proxy legacy

| Limite | Impact |
|--------|--------|
| 21 refs | Seuils GO sur **21** (≥ 13 OK · ≤ 2 REJECTED) |
| Banque recette / inspiration | Mix lifestyle, hero, stitch — hors tuile commerce stricte |
| Pas de visuels fournisseurs réels | Sous-représente l’hétérogénéité catalogue |
| Fond baked-in `#F8EEDB` | **Non arbitré MOA** — recette P3 requise |

---

## Livrables P2 proxy (Dev)

| Livrable | Chemin |
|----------|--------|
| Rapport JSON | `tools/ck_image_normalizer/reports/batch_20260520T105124Z.json` |
| Rapport CSV | `tools/ck_image_normalizer/reports/batch_20260520T105124Z.csv` |
| Previews avant/après | `tools/ck_image_normalizer/reports/previews/` |
| Grille mock source | `tools/ck_image_normalizer/reports/mock_grid_source_desktop_mobile.html` |
| Grille mock normalisée | `tools/ck_image_normalizer/reports/mock_grid_normalized_desktop_mobile.html` |
| Grille mock comparatif | `tools/ck_image_normalizer/reports/mock_grid_compare_desktop_mobile.html` |
| Grille notation MOA G1–G6 | `tools/ck_image_normalizer/reports/moa_scoring_g1_g6.csv` (à compléter MOA) |
| Manifest proxy | `tools/ck_image_normalizer/manifest.csv` |

---

## Décision Dev — suite proxy

| Verdict | Détail |
|---------|--------|
| **GO recette POC** | **Non** — proxy legacy seul |
| **GO technique intermédiaire** | **Oui** — moteur opérationnel, recette testable visuellement |
| **P0 MOA** | **21 refs** — validation lot officiel (aligné banque assets) |
| **P3 MOA** | **Prioritaire** — notation G1–G6 sur previews + grilles mock, surtout fond `#F8EEDB` baked-in (G6) |

### Prochaines étapes

1. **MOA** : compléter `moa_scoring_g1_g6.csv` sur les 21 previews (focus packshots OK + REJECTED).
2. **MOA** : arbitrer visuellement le fond `#F8EEDB` baked-in via grilles mock.
3. **MOA** : valider les **21 refs** comme lot officiel P0 — voir batch v1.1 pour décision GO.
4. **Dev** : ajuster recette si MOA le demande (ex. `content_area_ratio_max` packshot → `NEEDS_REVIEW` au lieu de `REJECTED` pour plein cadre).

---

## Historique

| Date | Auteur | Action |
|------|--------|--------|
| 2026-05-20 | Dev | Batch P2 proxy legacy — 21 images marketplace assets |
| 2026-05-20 | MOA | Prise d’acte résultats — GO candidate : non |
