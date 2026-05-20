# Plan d'alignement — Doctrine image v2

| Champ | Valeur |
|-------|--------|
| **Statut** | **Clôturé MOA** — GO alignement (2026-05-20) · prochaine étape : revue visuelle → `validated_grid` |
| **Doctrine** | [`DOCTRINE_IMAGE_V2.md`](../../cadrage/DOCTRINE_IMAGE_V2.md) |

---

## Objectif

Alignement **doctrinal et fonctionnel** minimal — pas de nouvelle recette image.

> Distinguer ce qui est **stocké**, ce qui est **affiché**, et ce qui reste en **gouvernance source**.

---

## Phase A — Documentation ✅

| Livrable | Statut |
|----------|--------|
| `DOCTRINE_IMAGE_V2.md` | ✅ |
| Ce plan | ✅ |
| Mise à jour `RECETTE_MANUELLE` opérateur | ✅ |
| Amendement ADR-033 | ✅ |

---

## Phase B — Code Odoo ✅

| # | Action | Fichier | Statut |
|---|--------|---------|--------|
| B1 | Statuts enrichis | `models/product_template_shop_tile.py` | ✅ |
| B2 | Affichage grille = `validated_grid` uniquement | `marketone_use_shop_tile_on_grid()` | ✅ |
| B3 | Legacy `validated` → non affiché (storage) | idem | ✅ |
| B4 | Fallback master automatique (QWeb existant) | `shop_product_tile_image.xml` | ✅ inchangé |
| B5 | Tests T1–T7 adaptés | `tests/test_marketone_shop_tile_image.py` | ✅ |

---

## Phase C — Import / garde-fous ✅

| # | Action | Fichier | Statut |
|---|--------|---------|--------|
| C1 | Statuts import autorisés v2 | `scripts/import_shop_tiles.py` | ✅ |
| C2 | Legacy `validated` → `validated_storage` à l'import | idem | ✅ |
| C3 | **Interdit** écriture `image_1920` via import | idem | ✅ |
| C4 | Import explicite `validated_grid` seul pour grille | manifest MOA requis | ✅ |

---

## Phase D — Données pilote (à exécuter MOA)

| Action | Détail |
|--------|--------|
| D1 | Migration statuts : `validated` → `validated_storage` sur les 43 pilotes | Script shell proposé ci-dessous |
| D2 | Promotion cas par cas → `validated_grid` après revue MOA visuelle | Colombo-like uniquement |
| D3 | Crackers (8) : `validated_grid` si reprise source MOA OK | Après revue capture |

**Script migration statuts pilote** (dry-run puis apply) :

```bash
docker exec -i sandbox-odoo19-odoo-1 odoo shell -c /etc/odoo/odoo.conf -d ckr-marketone-01 --no-http <<'EOF'
Product = env['product.template'].sudo()
legacy = Product.search([('shop_tile_status', '=', 'validated'), ('image_shop_tile', '!=', False)])
print('legacy validated count', len(legacy))
for p in legacy:
    print(' ', p.id, p.name)
# apply=True pour migrer :
# legacy.write({'shop_tile_status': 'validated_storage', 'shop_tile_moa_note': 'DOCTRINE_V2 — validated → validated_storage'})
# env.cr.commit()
EOF
```

---

## Phase E — Hors scope (confirmé MOA)

- Nouvelle recette image v1.2 / v2
- Alpha / rembg / cron massif
- Modification `image_1920` via pipeline

---

## Critères d'acceptation

| Critère | Seuil |
|---------|-------|
| `marketone_use_shop_tile_on_grid()` | True **iff** `validated_grid` |
| Import script | Rejette toute clé `image_1920` |
| Import `validated` legacy | Remappé `validated_storage` |
| Master | Jamais touché par import |
| Doctrine documentée | `DOCTRINE_IMAGE_V2.md` validé MOA |

---

## Signal Dev

```text
Doctrine image v2 alignée — validated_grid seul affiché en grille — image_1920 protégé — pilote en validated_storage par défaut.
```

## Clôture MOA (2026-05-20)

```text
GO doctrine v2 alignée — prochaine étape : revue visuelle produit par produit avant promotion validated_grid.
```

**Prochaine phase** : revue MOA cas par cas — promotion `validated_grid` uniquement si rendu conforme (image pleine, pas rectangle interne, pas halo, pas produit flottant).

**Crackers (8)** : `validated_storage` · grille désactivée · revue capture MOA avant promotion éventuelle.
