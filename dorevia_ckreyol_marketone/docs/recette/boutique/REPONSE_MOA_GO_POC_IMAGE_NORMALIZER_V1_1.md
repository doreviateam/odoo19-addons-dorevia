# Réponse MOA — CK Image Normalizer — GO POC avec réserves

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-05-20 |
| **Lot officiel POC** | 21 images — `dorevia_ckreyol_marketplace/docs/assets` |
| **Recette candidate** | `ck_shop_tile_v1.1` |
| **Run** | `tools/ck_image_normalizer/reports/runs/v1_1_proxy_21/` |
| **Décision** | **GO POC avec réserves** |

---

## Décision

La revue grille 21 images confirme que `ck_shop_tile_v1.1` améliore réellement la cohérence de la grille `/shop` :

- meilleure homogénéité visuelle ;
- fond `#F8EEDB` accepté ;
- aucun `REJECTED` sur le lot officiel ;
- les cas plein cadre sont correctement orientés vers `NEEDS_REVIEW` ;
- la grille est plus chaude et plus premium qu'avec les sources hétérogènes.

Le POC est donc validé **avec réserves**, sans autoriser encore une intégration Odoo.

---

## Réserves

| Réserve | Impact |
|---------|--------|
| Certaines images `NEEDS_REVIEW` exigent une reprise manuelle | `homepage_manioc_pates_mayotte_la_platine`, `stitch_guava_jam_jar` |
| Les images lifestyle restent moins homogènes que les packshots | Utiliser le statut `NEEDS_REVIEW` comme sas opérateur |
| Le moteur ne remplace pas une charte source fournisseur | Prévoir règles de qualité image en amont |

---

## Signal MOA

```text
GO POC avec réserves — lot officiel 21 refs validé — recette candidate ck_shop_tile_v1.1
```

---

## Garde-fous maintenus

- Pas de code Odoo immédiat.
- Pas de remplacement `product.template.image_1920`.
- Pas d'intégration automatique avant ticket dédié.
- Les originaux restent conservés.
- Les `NEEDS_REVIEW` doivent rester visibles dans le rapport opérateur.

---

## Suite possible

Ouvrir un ticket pilote limité pour définir :

- le flux opérateur des images `NEEDS_REVIEW` ;
- les règles de reprise manuelle ;
- le périmètre d'une éventuelle V1.5 Odoo lite ;
- le mode de stockage des tuiles dérivées sans écraser les images originales.
