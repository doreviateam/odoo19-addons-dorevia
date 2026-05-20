# Rapport recette — Tuile shop conversion — 2026-05-20

| Champ | Valeur |
|-------|--------|
| Recette | `RECETTE_MANUELLE_SHOP_CONVERSION_TILE.md` |
| Base | `ckr-marketone-01` |
| URL | `http://localhost:18079/shop` |
| Version cible | `19.0.15.8.1` |
| Statut | **GO MOA** |

## Exécution

- Module mis à jour via `-u dorevia_ckreyol_marketone`.
- Daemon Odoo redémarré après tests.
- `/shop` contrôlé en HTTP 200 après restart.
- Recette navigateur exécutée sur desktop et mobile 390 px.

## Tests automatisés

### Lot 3 ciblé

```text
0 failed, 0 error(s) of 11 tests
```

Contrôles couverts : structure tuile conversion, CTA, wishlist, absence description courte, bouton panier conservé, classe `o_wsale_products_opt_thumb_cover`, classe `marketone-shop-tile-photo`.

### Suite recommandée Lots 1–6.1

```text
0 failed, 0 error(s) of 63 tests
```

Statistiques Odoo module : `83 tests`.

## V1b — Photo pleine bord à bord

| Contrôle | Résultat |
|----------|----------|
| Tuiles collectées | 50 |
| Produits uniques | 50 |
| `validated_grid` trouvés | 19 / 19 |
| `validated_grid` avec `marketone-shop-tile-photo` | 19 / 19 |
| `validated_grid` bord à bord | 19 / 19 |
| Fallback relevés | 31 |
| Fallback avec wrapper dérivé | 0 |
| Fallback bord à bord | 31 / 31 |
| Inset détecté | 0 |

Verdict V1b : **GO**.

## V1–V6

| Zone | Résultat |
|------|----------|
| Scope `/shop` | `.marketone-shop` présent |
| Grille | Classe `o_wsale_products_opt_thumb_cover` présente |
| Cartes | `--o-wsale-card-padding: 0` effectif |
| Images | `object-fit: cover`, wrapper image aligné à la zone photo |
| Wishlist | Icône cœur présente en haut droit |
| Panier | Bouton présent dans la zone image, masqué au repos · **visible au survol (MOA OK)** · **popup au clic (MOA OK)** |
| Titre | Hauteur 2 lignes réservée |
| Description courte | Absente en grille |
| Ligne basse | `Voir` gauche, prix droite, `space-between` effectif |
| CTA / photo / titre | Hrefs alignés vers la fiche produit |
| Mobile 390 px | 2 colonnes, aucun overflow horizontal détecté |
| Fiche produit | Hors scope `.marketone-shop` confirmé par tests |
| Cart / checkout | Non-régression couverte par la suite recommandée |

Note technique : le survol n'a pas pu être déclenché par l'automatisation navigateur (`:hover`). **Validation MOA humaine** : comportement survol panier et popup au clic **conformes**.

## Captures

- `capture_recette_conversion_tile_desktop.png`
- `capture_recette_conversion_tile_mobile_390.png`

## Verdict

```text
Recette manuelle tuile conversion — GO MOA — V1–V6 + V1b photo pleine — tests Lot 3 + suite recommandée OK — panier survol + popup clic OK — doctrine image v2 inchangée.
```
