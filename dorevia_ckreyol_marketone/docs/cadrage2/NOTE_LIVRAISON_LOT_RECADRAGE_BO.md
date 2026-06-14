# Note de livraison — Lot recadrage BO produit

| Champ | Valeur |
|-------|--------|
| **Version** | `19.0.16.0.0` |
| **Référence MOA** | [`DECISION_MOA_RECADRAGE_BO.md`](./DECISION_MOA_RECADRAGE_BO.md) |
| **Date livraison** | 2026-06-08 |
| **Statut** | **Clôturé — GO avec réserves MOA** (2026-06-08) |

### Résultats tests automatisés (`ckr-marketone-01`)

| Suite | Résultat |
|-------|----------|
| `dorevia_marketone_bo` (9 tests) | **0 échec** |
| `dorevia_marketone_shop_tile` (12 tests) | **11 OK** · 1 échec pré-existant (`test_t5_import_manifest_validates_offline` — JPEG pilote absents de l'environnement, hors périmètre lot BO) |

---

## Périmètre respecté

| Contrainte MOA | Statut |
|----------------|--------|
| Lot strictement BO produit | ✅ |
| Aucun changement front | ✅ |
| Aucune modification QWeb / contrôleur / asset / route `/shop` | ✅ |
| Aucun ajout fonctionnel e-commerce | ✅ |
| Aucune dépendance `website_blog` / `website_forum` | ✅ |
| Aucun nouveau groupe de sécurité | ✅ |
| Noms techniques Python inchangés | ✅ |

---

## Confirmation « aucun diff front »

Aucun fichier modifié dans les zones front :

| Zone | Fichiers touchés |
|------|------------------|
| `views/pages/` | **0** |
| `views/layout/` | **0** |
| `controllers/` | **0** |
| `static/src/` | **0** |
| `data/` (front) | **0** |

---

## Fichiers modifiés

| Fichier | Action |
|---------|--------|
| `__manifest__.py` | Version `19.0.16.0.0` · remplacement vue BO |
| `views/product_template_marketone_bo_views.xml` | **Créé** — 4 onglets CK + masquage champs eCommerce dupliqués |
| `views/product_template_shop_tile_views.xml` | **Supprimé** — bloc « Tuile commerce /shop » retiré |
| `views/marketone_shop_collection_views.xml` | Extension produit retirée (collections → onglet Catalogue CK) |
| `models/product_template_shop_tile.py` | Libellés métier (`string` / Selection) uniquement |
| `tests/test_marketone_product_form_bo.py` | **Créé** — tests vues BO + non-régression logique tuile |
| `tests/__init__.py` | Import nouveau test |

---

## Livrable fonctionnel BO

### Fiche produit (`product.template`)

| Onglet | Contenu |
|--------|---------|
| **Publication site** | `is_published`, `website_id`, `public_categ_ids`, `website_sequence`, `website_ribbon_id`, `description_ecommerce` |
| **Catalogue CK** | `marketone_collection_ids` + aide origines |
| **Qualité image / contenu** | `image_shop_tile`, `shop_tile_status`, `shop_tile_moa_note` |
| **Technique** | `shop_tile_recipe_version`, `shop_tile_processed_at`, `shop_tile_source_run` (`base.group_no_one`) |

### Champs masqués à l'emplacement Odoo standard (réaffichés dans Publication site)

- `is_published`, `public_categ_ids`, `website_sequence`, `website_ribbon_id`, `website_id` (groupe `extra_info`)
- Groupe `ecom_description` (`description_ecommerce`)

### Image principale

- `image_1920` : **inchangée**, zone standard Odoo — aucun bloc CK adjacent.

---

## Tests

### Nouveaux

Tag : `dorevia_marketone_bo`

Fichier : `tests/test_marketone_product_form_bo.py`

- Absence bloc « Tuile commerce /shop »
- Présence des 4 onglets CK
- Onglet Technique réservé `base.group_no_one`
- Champs batch absents de l'onglet Qualité image
- Libellés sans « /shop », « tuile », « CLI »
- Logique `marketone_use_shop_tile_on_grid()` inchangée

### Non-régression (à exécuter en recette)

```bash
odoo-bin -d <base_test> \
  --test-tags=dorevia_marketone_bo,dorevia_marketone_shop_tile \
  -u dorevia_ckreyol_marketone --stop-after-init
```

Puis suite complète module si disponible.

---

## Checklist recette MOA

Recette manuelle : [`RECETTE_MANUELLE_RECADRAGE_BO_PRODUIT.md`](./RECETTE_MANUELLE_RECADRAGE_BO_PRODUIT.md) — **GO avec réserves MOA** (2026-06-08).

- [x] R1–R11 BO (fiche produit)
- [x] F1–F5 non-régression `/shop`
- [x] Tests auto `dorevia_marketone_bo` : 9/9 OK
- [ ] Backlog séparé : `test_t5_import_manifest_validates_offline` (JPEG pilotes)

---

## Comportement front garanti inchangé

| Mécanisme | Fichier | Modifié |
|-----------|---------|---------|
| Affichage vignette grille | `views/pages/shop_product_tile_image.xml` | Non |
| Méthode `marketone_use_shop_tile_on_grid()` | `models/product_template_shop_tile.py` | Non (logique) |
| Flag global | `data/marketone_shop_tile_config.xml` | Non |
| Import batch | `scripts/import_shop_tiles.py` | Non |
