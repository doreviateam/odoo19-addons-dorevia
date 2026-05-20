# TICKET — CK Image Normalizer — V1.5 Odoo lite — Implémentation (P7)

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION` |
| **Univers** | **Boutique** — tuiles commerce `/shop` |
| **Type** | **Implémentation Odoo lite** — strictement bornée |
| **Statut** | **Recette Dev OK** (2026-05-20) · P7-6 exécuté · P7-7 revue visuelle MOA en attente |
| **Ticket amont cadrage** | [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_CADRAGE`](./TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_CADRAGE.md) — **P6 validé MOA** |
| **Ticket amont pilote** | [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA`](./TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md) — clôturé · **43/50 (86 %)** |
| **Module** | `dorevia_ckreyol_marketone` |
| **Recette source** | `ck_shop_tile_v1.1` |
| **ADR** | [ADR-033](../../cadrage/DECISIONS.md#adr-033--ck-image-normalizer-v1--poc-tuiles-commerce-shop) |
| **Effort indicatif** | **8–12 j/h Dev** + **2–4 h MOA** import pilote |

---

## Signal MOA

```text
GO implémentation P7 — V1.5 Odoo lite — périmètre strict tuiles /shop · image_shop_tile dérivé · image_1920 master · flag off par défaut · import pilote 43 images · lot X exclu.
```

```text
P6 cadrage validé MOA — GO ouverture ticket P7 implémentation V1.5 lite — P7 strict, réversible, limité aux tuiles /shop.
```

**Ce GO autorise l’implémentation dans ce ticket P7.** Il ne couvre pas l’industrialisation catalogue ni l’extension au lot X.

---

## Objectif P7

Permettre à la grille `/shop` d’utiliser une **image dérivée validée** (`image_shop_tile`) tout en conservant `image_1920` comme **master produit inchangé**.

```text
image_1920       → master (fiche, BO, usages standard)
image_shop_tile  → dérivé tuile /shop (import CLI validé MOA)
grille /shop     → image_shop_tile si présent + flag actif, sinon image_512
```

Intégration **légère**, **réversible**, **sans cron**, **sans BO complet**.

---

## Décisions MOA validées (P6 → P7)

| Sujet | Décision MOA |
|-------|--------------|
| Champ dérivé | **`image_shop_tile`** |
| Modèle | **`product.template` uniquement** |
| Master | **`image_1920` conservé, jamais écrasé** |
| Usage | **Grille `/shop` uniquement** |
| Fallback | **`image_512`** si `image_shop_tile` absent |
| Feature flag | **`marketone.shop_tile_enabled`** |
| Recette source | **`ck_shop_tile_v1.1`** |
| Import | **Manuel / semi-manuel** · `--dry-run` par défaut |
| Traçabilité | **statut · version recette · date traitement · source run** |
| QWeb | **Héritage minimal** sur `website_sale.products_item` |
| Rollback | **Feature flag off** → suppression champ si besoin |

---

## Périmètre P7 — livrables autorisés

| # | Livrable | Détail |
|---|----------|--------|
| **L1** | Champs `product.template` | `image_shop_tile` + métadonnées traçabilité |
| **L2** | Vue BO minimale | Groupe « Tuile /shop » sur fiche produit |
| **L3** | Feature flag | `ir.config_parameter` `marketone.shop_tile_enabled` |
| **L4** | Héritage QWeb | Vignette `website_sale.products_item` uniquement |
| **L5** | Script import | `scripts/import_shop_tiles.py` · dry-run par défaut |
| **L6** | Tests | T1–T7 (voir § Tests) |
| **L7** | Import pilote | **43 images validées** uniquement |
| **L8** | Doc opérateur | Procédure import + rollback · lien recette pilote |

---

## Hors périmètre P7 (interdit)

| Élément | Statut |
|---------|--------|
| Remplacement `image_1920` | ❌ |
| Traitement auto à l’upload | ❌ |
| Cron massif | ❌ |
| BO complet / studio recette | ❌ |
| Galerie fiche produit | ❌ |
| Hero / éditorial / culture / origines | ❌ |
| IA / détourage / `rembg` | ❌ |
| Modification moteur e-commerce | ❌ |
| Import lot X (7) | ❌ |
| Import images non validées MOA | ❌ |
| Génération image depuis Odoo | ❌ |
| Variantes `product.product` | ❌ V1.5 |
| Module séparé `dorevia_ck_media` | ❌ V2+ |

---

## Spécification technique

### 1. Modèle — extension `product.template`

Fichier proposé : `models/product_template_shop_tile.py` (ou extension de `product_template.py` si plus cohérent avec l’existant).

| Champ | Type | Attributs | Valeurs / notes |
|-------|------|-----------|-----------------|
| `image_shop_tile` | `Binary` | `attachment=True` | JPEG 1024×1024 importé depuis CLI |
| `shop_tile_status` | `Selection` | `required=False` | `none` · `validated` · `validated_reserve` · `pending_review` · `rejected` |
| `shop_tile_recipe_version` | `Char` | | ex. `ck_shop_tile_v1.1` |
| `shop_tile_processed_at` | `Datetime` | | date import |
| `shop_tile_source_run` | `Char` | | ex. `pilote_20260520` |
| `shop_tile_moa_note` | `Char` | | réserve MOA optionnelle |

**Helper recommandé** :

```python
def _marketone_shop_tile_enabled(self):
    return self.env["ir.config_parameter"].sudo().get_param(
        "marketone.shop_tile_enabled", "False"
    ) == "True"
```

Pas de `@api.onchange` sur `image_1920`. Pas de recalcul auto.

### 2. Feature flag

Fichier : `data/marketone_shop_tile_config.xml`

```xml
<!-- Valeur par défaut recommandée : False jusqu’à recette MOA post-import -->
<record id="config_shop_tile_enabled" model="ir.config_parameter">
  <field name="key">marketone.shop_tile_enabled</field>
  <field name="value">False</field>
</record>
```

**Rollback immédiat (MOA)** : passer `marketone.shop_tile_enabled` à `False` → grille 100 % standard Odoo.

### 3. Vue BO minimale

Fichier : `views/product_template_shop_tile_views.xml`

- Héritage `product.template` form view (mode développeur ou groupe dédié si existant).
- Groupe **« Tuile commerce /shop »** :
  - `image_shop_tile` (widget image)
  - `shop_tile_status` · `shop_tile_recipe_version` · `shop_tile_processed_at` · `shop_tile_source_run` · `shop_tile_moa_note`
- **Pas** de bouton « regénérer » · **pas** de preview batch.

### 4. QWeb — héritage minimal

Fichier : `views/pages/shop_product_tile_image.xml`

| Règle | Détail |
|-------|--------|
| Template cible | `website_sale.products_item` |
| Priority | `50` (basse — ne pas écraser surcharges marketplace) |
| Modification | **Vignette image uniquement** |
| Condition | `marketone.shop_tile_enabled` **et** `product.image_shop_tile` |
| Sinon | Comportement Odoo standard (`image_512`) |

**Zones exclues** : fiche produit (`product.xml`), cart, checkout, wishlist, home, culture.

### 5. Script import semi-manuel

Fichier : `scripts/import_shop_tiles.py`

```bash
# Dry-run (défaut)
python scripts/import_shop_tiles.py \
  --manifest docs/recette/boutique/import_pilote_43_shop_tiles.csv \
  --dry-run

# Application explicite
python scripts/import_shop_tiles.py \
  --manifest docs/recette/boutique/import_pilote_43_shop_tiles.csv \
  --apply
```

| Option | Rôle |
|--------|------|
| `--manifest` | CSV liste des 43 imports autorisés (SKU, chemin JPEG, statut, run) |
| `--dry-run` | **Défaut** — log sans écriture |
| `--apply` | Écriture explicite |
| `--format` | `jpeg` (V1.5 — compat Odoo binary) |

**Règles import** :

- Importer **uniquement** lignes `validated` ou `validated_reserve` ;
- **Rejeter** toute ligne absente du manifest pilote 43 ;
- Écrire **`image_shop_tile` + métadonnées** · **jamais** `image_1920` ;
- Log : `import_shop_tiles_YYYYMMDD.log`.

### 6. Manifest import pilote (43 images)

Fichier à produire en P7 : `docs/recette/boutique/import_pilote_43_shop_tiles.csv`

Sources agrégées :

| Origine | Run / décision |
|---------|----------------|
| OK + OK_WITH_WARNINGS batch principal | `pilote_20260520` |
| NEEDS_REVIEW E/R P4 | `pilote_operateur.csv` |
| Lot M corrigé (5 OK MOA) | `pilote_20260520_lot_m_corrige` |
| Manioc sources distinctes (2) | `pilote_20260520_lot_manioc_sources` |

**Lot X (7)** : **exclu** — voir `lot_x_arbitrage_moa.csv`.

Colonnes manifest proposées :

```text
product_template_id,default_code,reference,source_jpeg_path,shop_tile_status,shop_tile_recipe_version,shop_tile_source_run,shop_tile_moa_note
```

---

## Plan d’implémentation

| Phase | Action | Responsable | Statut |
|-------|--------|-------------|--------|
| **P7-1** | Modèle + champs + config flag | Dev | ✅ |
| **P7-2** | Vue BO minimale | Dev | ✅ |
| **P7-3** | Héritage QWeb vignette | Dev | ✅ |
| **P7-4** | Script import + manifest 43 | Dev | ✅ |
| **P7-5** | Tests T1–T7 | Dev | ✅ 7/7 verts (`ckr-marketone-01`) |
| **P7-6** | Import pilote dry-run + apply | Dev + MOA | ✅ 43/43 · `image_1920` inchangé |
| **P7-7** | Revue visuelle /shop MOA | MOA | 🔄 **GO avec réserves** — fond image tuile à ajuster |
| **P7-7b** | Ajustement fond image tuile `#FCFAF6` | Dev | ✅ v `19.0.15.7.17` |
| **P7-7c** | Occupation zone photo + fond `#FDFCFA` | Dev | ✅ v `19.0.15.7.18` · capture v2 |
| **P7-7d** | Masque CSS 14 px + zoom 1.32 · note V1.2 instructionnelle | Dev | ✅ v `19.0.15.7.19` · capture v3 · `NOTE_CK_IMAGE_NORMALIZER_V1_2_TRANSPARENT_PROPOSAL.md` |
| **P7-7e** | POC V1.2-alpha sur 3 packshots + 1 lifestyle contrôle | Dev | ✅ `RAPPORT_POC_V1_2_ALPHA_3_PACKSHOTS.md` · capture comparative |
| **P7-8** | Activation flag + recette manuelle | MOA | 🔄 flag **True** — revue visuelle MOA en cours |

---

## Tests minimaux T1–T7

| # | Test | Fichier cible | Attendu |
|---|------|---------------|---------|
| **T1** | Produit avec tuile sur `/shop` | `tests/test_marketone_shop_tile_image.py` | `image_shop_tile` affiché |
| **T2** | Produit sans tuile | idem | `image_512` — identique avant P7 |
| **T3** | Fiche produit | idem | **Pas** `image_shop_tile` |
| **T4** | Flag `shop_tile_enabled=False` | idem | Fallback total |
| **T5** | Import dry-run | script / test | 0 écriture · log OK |
| **T6** | Import apply 1 SKU | idem | Champs remplis |
| **T7** | Suppression `image_shop_tile` | idem | Retour fallback immédiat |

Base existante : `tests/test_marketone_lot3_shop.py`.

---

## Rollback

| Niveau | Action | Effet |
|--------|--------|-------|
| **R0 — immédiat (MOA)** | `marketone.shop_tile_enabled = False` | Grille standard Odoo instantanée |
| **R1 — produit** | Vider `image_shop_tile` | Fallback unitaire |
| **R2 — code** | Désactiver héritage QWeb (upgrade module) | Retour natif |
| **R3 — données** | Conserver champs en base | Réactivation possible |

**Exigence MOA** : R0 doit être testé en recette avant GO production flag.

---

## Critères d’acceptation P7

| Critère | Seuil |
|---------|-------|
| Champs présents sur `product.template` | ✅ |
| `image_1920` jamais modifié par import | ✅ obligatoire |
| Fallback `image_512` fonctionnel | ✅ |
| Flag off = grille identique à avant | ✅ |
| Import 43/43 dry-run sans erreur | ✅ |
| Import apply 43/43 avec log | ✅ |
| Revue MOA /shop sur échantillon | ≥ 5 tuiles OK visuel |
| Lot X non importé | 0 ligne lot X |
| Tests T1–T7 verts | ✅ |

---

## Risques et mitigations

| Risque | Mitigation |
|--------|------------|
| XPath QWeb fragile | Tests · xpath robuste · flag off |
| Tuile obsolète si master change | Doc opérateur · `shop_tile_processed_at` |
| Confusion master/dérivé | Libellés BO · import log |
| Régression grille sans tuile | T2 · T4 · fallback obligatoire |
| Scope creep | Ticket strict · revue MOA avant extension |

---

## Garde-fous maintenus

```text
Pas de remplacement image_1920
Pas de traitement automatique à l’upload
Pas de cron massif
Pas de BO complet
Pas de galerie fiche produit
Pas d’usage hero / éditorial / culture
Pas d’IA · pas de détourage
website_sale reste le moteur unique (ADR-002)
```

---

## Fichiers à créer / modifier (indicatif Dev)

| Fichier | Action |
|---------|--------|
| `models/product_template_shop_tile.py` | ✅ Créé |
| `models/__init__.py` | ✅ Import |
| `views/product_template_shop_tile_views.xml` | ✅ Créé |
| `views/pages/shop_product_tile_image.xml` | ✅ Créé |
| `data/marketone_shop_tile_config.xml` | ✅ Créé |
| `scripts/import_shop_tiles.py` | ✅ Créé |
| `docs/recette/boutique/import_pilote_43_shop_tiles.csv` | ✅ Créé · 43 lignes |
| `docs/recette/boutique/RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_V1_5_SHOP_TILE.md` | ✅ Créé (L8) |
| `tests/test_marketone_shop_tile_image.py` | ✅ Créé |
| `__manifest__.py` | ✅ v `19.0.15.7.16` |

**Aucun changement** dans `tools/ck_image_normalizer/` (CLI reste externe).

---

## Décision finale

```text
P7 implémentation V1.5 Odoo lite livrée (L1–L8) — en attente recette MOA P7-6→P7-8 sur ckr-marketone-01.
```

**Signal Dev** :

```text
Implémentation P7 terminée côté code — manifest 43 validé offline — upgrade module + tests Odoo + import pilote à exécuter en recette.
```

---

## Références

| Document | Rôle |
|----------|------|
| [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_CADRAGE.md`](./TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_CADRAGE.md) | P6 validé MOA |
| [`RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md`](../../recette/boutique/RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md) | Pilote · 43/50 |
| [`REGLE_CATALOGUE_IMAGES_SOURCE.md`](../../cadrage/REGLE_CATALOGUE_IMAGES_SOURCE.md) | Règle source |
| [`REPONSE_MOA_CLOTURE_PILOTE_MEDIA_CATALOGUE.md`](../../recette/boutique/REPONSE_MOA_CLOTURE_PILOTE_MEDIA_CATALOGUE.md) | Clôture pilote |
| `tools/ck_image_normalizer/reports/runs/pilote_20260520/` | Run principal |
| `…/lot_x_arbitrage_moa.csv` | Lot X — **exclu import** |

---

## Mise à jour doctrinale (post-P8)

```text
Verdict MOA final P8-5 :
GO avec réserves gouvernées — modèle hybride v1.1 + v1.2-alpha validé.
Lot B maintenu en NEEDS_REVIEW_SOURCE sous gouvernance source.
```

Cette décision confirme la cohérence V1.5 :

- `image_shop_tile` limité à `/shop`
- `image_1920` master inchangé
- fallback/rollback maintenus
- séparation master/dérivé respectée

Référence de clôture : `TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_2_ALPHA_P8.md`.

---

## Historique

| Date | Auteur | Action |
|------|--------|--------|
| 2026-05-20 | MOA | **GO visuel avec réserves** — fond image tuile trop beige |
| 2026-05-20 | MOA | **GO technique avec réserve visuelle** — fond zone photo + effet carré interne |
| 2026-05-20 | Dev | **P7-7c** — fond `#FDFCFA` · `cover` + zoom 1.2 · classe `marketone-shop-tile-photo` |
| 2026-05-20 | MOA | **NO GO visuel zone photo V1.5 actuelle** — ajustement fond + occupation requis |
| 2026-05-20 | Dev | **P7-7d** — masque CSS 14 px + zoom 1.32 · note V1.2 packshots transparents instruite |
| 2026-05-20 | MOA | **Doctrine clarifiée** — packshots transparents · lifestyle conservés · demande POC ciblé |
| 2026-05-20 | Dev | **P7-7e POC v1.2-alpha** — 3 packshots transparents · 1/3 excellent, 2/3 limites classification |
| 2026-05-20 | Dev | **P7 ticket ouvert** — ce document |
| 2026-05-20 | MOA | **GO implémentation P7** — périmètre strict validé (L1–L8) |
| 2026-05-20 | Dev | **Recette P7-6** · upgrade · tests 7/7 · import 43/43 · rollback R0 validé · flag **False** |
| 2026-05-20 | MOA | **Verdict final P8-5 consigné** — GO avec réserves gouvernées · modèle hybride validé · 5 cas sous gouvernance source |
