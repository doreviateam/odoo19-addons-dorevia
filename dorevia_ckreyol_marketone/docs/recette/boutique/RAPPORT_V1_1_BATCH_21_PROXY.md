# Rapport — CK Image Normalizer — Batch officiel 21 images en v1.1

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-05-20 |
| **Recette** | `ck_shop_tile_v1.1` |
| **Run** | `tools/ck_image_normalizer/reports/runs/v1_1_proxy_21/` |
| **Déclencheur** | P3 ciblé clôturé — décision 2 |
| **Statut** | **GO POC avec réserves MOA** — batch 21 refs validé comme base candidate, sans code Odoo |

---

## Résultat automatique

| Statut | Nombre |
|--------|-------:|
| `OK` | 13 |
| `OK_WITH_WARNINGS` | 1 |
| `NEEDS_REVIEW` | 7 |
| `REJECTED` | 0 |

| Indicateur | Valeur |
|------------|-------:|
| Total | 21 |
| OK rate | 67 % |
| Rejected rate | 0 % |
| GO candidate automatique | Oui |

---

## Lecture MOA

Le recalibrage `ck_shop_tile_v1.1` corrige le problème principal du batch proxy v1 : les images plein cadre ne sont plus rejetées automatiquement, elles passent en `NEEDS_REVIEW`.

Ce comportement est cohérent avec la décision P3 ciblée :

```text
GO clôture P3 ciblé — 7 NEEDS_REVIEW notés — décision 2
```

Le batch 21 v1.1 constitue le **lot officiel POC** (21 refs MOA).

---

## Revue grille MOA (2026-05-20)

| Axe | Verdict | Notes |
|-----|---------|-------|
| Grille desktop 4 colonnes | **GO avec réserves** | La grille est plus homogène et plus chaude ; les produits ont globalement un meilleur poids visuel. |
| Grille mobile 2 colonnes | **GO avec réserves** | Lisibilité suffisante en petit format ; les statuts `NEEDS_REVIEW` restent visibles comme garde-fou qualité. |
| Fond `#F8EEDB` baked-in | **Accepté** | Le fond réchauffe la grille et s'intègre correctement avec les cartes. |
| Détection `NEEDS_REVIEW` | **Validée** | Les cas plein cadre sont correctement sortis du flux automatique plutôt que rejetés brutalement. |
| Artefacts visuels | **Réserve** | `homepage_manioc_pates_mayotte_la_platine` et `stitch_guava_jam_jar` nécessitent reprise manuelle ; `stitch_curry_powder_pouch` et `stitch_scotch_bonnet_sauce` restent acceptables sous réserve. |
| Code Odoo | **Interdit à ce stade** | Le POC valide la logique média, pas encore l'intégration produit. |

**Décision MOA** :

```text
GO POC avec réserves — lot officiel 21 refs validé — recette candidate ck_shop_tile_v1.1
```

Ce verdict valide la poursuite du chantier média, mais ne vaut pas autorisation d'intégration Odoo immédiate.

---

## Livrables

| Livrable | Chemin |
|----------|--------|
| Rapport JSON | `tools/ck_image_normalizer/reports/runs/v1_1_proxy_21/reports/batch_20260520T111233Z.json` |
| Rapport CSV | `tools/ck_image_normalizer/reports/runs/v1_1_proxy_21/reports/batch_20260520T111233Z.csv` |
| Previews | `tools/ck_image_normalizer/reports/runs/v1_1_proxy_21/reports/previews/` |
| Grille normalisée | `tools/ck_image_normalizer/reports/runs/v1_1_proxy_21/reports/mock_grid_v1_1_normalized_desktop_mobile.html` |
| Comparatif source / normalisée | `tools/ck_image_normalizer/reports/runs/v1_1_proxy_21/reports/mock_grid_v1_1_compare_desktop_mobile.html` |

---

## Suite recommandée

1. Documenter les réserves opérateur pour les fichiers `NEEDS_REVIEW`.
2. Préparer un ticket pilote média / catalogue limité si la MOA souhaite poursuivre.
3. Maintenir le principe : pas de code Odoo et pas de remplacement `image_1920` avant ticket d'intégration dédié.
