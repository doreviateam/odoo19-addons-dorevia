# Recette manuelle — CK Image Normalizer V1.5 — Tuile /shop Odoo lite

| Champ | Valeur |
|-------|--------|
| **Ticket implémentation** | [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION`](../../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION.md) |
| **Ticket cadrage** | [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_CADRAGE`](../../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_CADRAGE.md) — validé MOA |
| **Module** | `dorevia_ckreyol_marketone` |
| **Recette CLI** | `ck_shop_tile_v1.1` |
| **Import pilote** | **43 images** — [`import_pilote_43_shop_tiles.csv`](./import_pilote_43_shop_tiles.csv) |

---

## Principe

```text
image_1920       = master produit (inchangé)
image_shop_tile  = dérivé tuile /shop (import CLI validé MOA)
grille /shop     = image_shop_tile si flag actif, sinon comportement Odoo 19 standard
fiche produit    = image standard uniquement
```

Feature flag (désactivé par défaut) :

```text
marketone.shop_tile_enabled = False | True
```

---

## 0. Prérequis conteneur — JPEGs pilote

Les chemins du manifest pointent vers `tools/ck_image_normalizer/` (hôte). Dans Docker, copier les JPEGs avant import Odoo :

```bash
BASE=/Users/doreviateam/dorevia-saas/tools/ck_image_normalizer/reports/runs
docker exec -u root sandbox-odoo19-odoo-1 rm -rf /tmp/marketone_pilote_import
docker exec sandbox-odoo19-odoo-1 mkdir -p /tmp/marketone_pilote_import/tools/ck_image_normalizer/reports/runs
for run in pilote_20260520 pilote_20260520_lot_m_corrige pilote_20260520_lot_manioc_sources; do
  docker exec sandbox-odoo19-odoo-1 mkdir -p "/tmp/marketone_pilote_import/tools/ck_image_normalizer/reports/runs/$run/output"
  docker cp "$BASE/$run/output/jpeg" "sandbox-odoo19-odoo-1:/tmp/marketone_pilote_import/tools/ck_image_normalizer/reports/runs/$run/output/"
done
```

Le script résout automatiquement les chemins hôte vers `/tmp/marketone_pilote_import/…`.

---

## 0bis. Upgrade module + redémarrage

Après `-u dorevia_ckreyol_marketone`, **redémarrer le conteneur Odoo** pour recharger le QWeb :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf -d ckr-marketone-01 \
  -u dorevia_ckreyol_marketone --stop-after-init
docker restart sandbox-odoo19-odoo-1
```


Hors Odoo :

```bash
cd odoo19-addons-dorevia/dorevia_ckreyol_marketone
python scripts/import_shop_tiles.py \
  --manifest docs/recette/boutique/import_pilote_43_shop_tiles.csv
```

Attendu :

```text
OK manifest ... : 43 lignes importables
```

---

## 2. Import Odoo — dry-run puis apply

Dry-run (aucune écriture) :

```bash
docker exec -i sandbox-odoo19-odoo-1 odoo shell -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 --no-http <<'EOF'
exec(open("/mnt/odoo19-addons-dorevia/dorevia_ckreyol_marketone/scripts/import_shop_tiles.py").read())
run_import(env, manifest_path="/mnt/odoo19-addons-dorevia/dorevia_ckreyol_marketone/docs/recette/boutique/import_pilote_43_shop_tiles.csv", apply=False)
EOF
```

Apply (après validation MOA du dry-run) :

```bash
run_import(..., apply=True)
```

Garde-fous :

- **43 lignes max** (manifest pilote)
- statuts importables : **`validated_grid`** · **`validated_storage`** · **`validated_reserve`** · **`pending_review`** · **`needs_review_source`** · **`rejected`**
- legacy manifest **`validated`** → remappé **`validated_storage`** à l'import
- **grille `/shop`** : affichage dérivé **uniquement** si `validated_grid`
- **interdit** : toute colonne `image_1920` dans le manifest
- **lot X exclu**
- **jamais** d'écriture dans `image_1920`

---

## 3. Activation contrôlée

1. Vérifier `/shop` avec flag **désactivé** — comportement identique à avant.
2. Activer :

```text
Paramètre système : marketone.shop_tile_enabled = True
```

3. Contrôler `/shop` sur échantillon produits importés.
4. Vérifier fiche produit — **pas** de `image_shop_tile`.

---

## 4. Rollback immédiat

| Niveau | Action |
|--------|--------|
| **R0** | `marketone.shop_tile_enabled = False` | Grille standard Odoo instantanée (via UI BO ; si changement via shell externe, redémarrer le worker ou attendre invalidation cache) |
| **R1** | Vider `image_shop_tile` sur produit concerné |

Test rollback obligatoire avant GO production du flag.

---

## 5. Tests automatisés T1–T7

```bash
# Dans l'environnement Odoo de recette
odoo-bin -d ckr-marketone-01 --test-tags dorevia_marketone_shop_tile
```

| Test | Vérification |
|------|--------------|
| T1 | `/shop` avec flag ON → URL `image_shop_tile` |
| T2 | `/shop` avec flag OFF → pas de `image_shop_tile` |
| T3 | Fiche produit → pas de `image_shop_tile` |
| T4 | Flag OFF ignore tuile même si champ rempli |
| T5 | Manifest 43 valide offline |
| T6 | Import n'altère pas `image_1920` |
| T7 | Vider tuile → plus utilisée en grille |

---

## Références

| Document | Rôle |
|----------|------|
| [`RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md`](./RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md) | Pilote · 43/50 |
| [`import_pilote_43_shop_tiles.csv`](./import_pilote_43_shop_tiles.csv) | Manifest import autorisé |
| [`import_retrait_alpha_v11_9.csv`](./import_retrait_alpha_v11_9.csv) | Rebasculage alpha → v1.1 (9 produits) |
| [`DOCTRINE_IMAGE_V2.md`](../../cadrage/DOCTRINE_IMAGE_V2.md) | Doctrine image v2 validée MOA |
| [`PLAN_ALIGNEMENT_DOCTRINE_IMAGE_V2.md`](./PLAN_ALIGNEMENT_DOCTRINE_IMAGE_V2.md) | Alignement code |
| [`tools/ck_image_normalizer/README.md`](../../../../tools/ck_image_normalizer/README.md) | CLI amont |

---

## Doctrine active (post-retrait alpha, 2026-05-20)

**Référence canonique : [`DOCTRINE_IMAGE_V2.md`](../../cadrage/DOCTRINE_IMAGE_V2.md)**

```text
Recette active     : ck_shop_tile_v1.1 uniquement
Transparence alpha : interdite (recette v1.2-alpha deprecated)
Import Odoo        : JPEG image pleine seulement — PNG/WebP rejetés
Import alpha       : manifest ck_shop_tile_v1.2-alpha bloqué
Master             : image_1920 jamais écrasé par import
Grille /shop       : image_shop_tile si validated_grid uniquement
Pilote importé     : validated → validated_storage (non affiché par défaut)
```
