# TICKET — CK Image Normalizer — V1.5 Odoo lite — Cadrage (P6)

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_CADRAGE` |
| **Univers** | **Boutique** — tuiles commerce `/shop` |
| **Type** | **Cadrage uniquement** — pas d’implémentation |
| **Statut** | **Clôturé MOA** (2026-05-20) · **P6 validé** · **GO P7 ouvert** |
| **Ticket amont POC** | [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_POC`](./TICKET_MARKETONE_CK_IMAGE_NORMALIZER_POC.md) — clôturé GO avec réserves |
| **Ticket amont pilote** | [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA`](./TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md) — clôturé · **43/50 (86 %)** |
| **Signal MOA** | [`REPONSE_MOA_CLOTURE_PILOTE_MEDIA_CATALOGUE.md`](../../recette/boutique/REPONSE_MOA_CLOTURE_PILOTE_MEDIA_CATALOGUE.md) |
| **Module cible** | `dorevia_ckreyol_marketone` |
| **Recette candidate** | `ck_shop_tile_v1.1` |
| **ADR** | [ADR-033](../../cadrage/DECISIONS.md#adr-033--ck-image-normalizer-v1--poc-tuiles-commerce-shop) |
| **Effort cadrage** | **1–2 j/h Dev** (ce document) |
| **Effort implémentation V1.5 lite (estimation)** | **8–12 j/h Dev** + **2–4 h MOA** import pilote |

---

## Contexte — pilote clôturé

```text
GO pilote avec réserves confirmé
Recette candidate : ck_shop_tile_v1.1
Taux exploitable final : 43 / 50 = 86 %
Lot X restant : 7 / 50 = 14 %
REJECTED définitif : 0
```

Combinaison validée :

```text
moteur ck_shop_tile_v1.1 + revue opérateur + correction source ciblée
```

Le moteur prouve sa valeur. Le pilote confirme aussi que la **qualité source** et le **sas opérateur** restent indispensables.

État technique actuel Marketone :

| Élément | État |
|---------|------|
| Tuiles `/shop` | Natives `website_sale.products_item` — **aucun héritage QWeb image** |
| Style tuiles | SCSS `--o-wsale-card-*` · fond `#F8EEDB` · ratio 1:1 · `object-fit: contain` |
| Image produit master | `product.template.image_1920` (+ dérivés Odoo) |
| Image tuile dédiée | **Aucun champ** |
| CLI normalizer | `tools/ck_image_normalizer/` — opérationnel · recette v1.1 validée |

Référence cadrage initial : [`NOTE_CK_IMAGE_NORMALIZER_SHOP_V1.md`](../../cadrage/NOTE_CK_IMAGE_NORMALIZER_SHOP_V1.md) §10.1

---

## Objectif P6

Définir comment Odoo pourrait utiliser une **image dérivée validée** pour les tuiles commerce `/shop`, **sans toucher au master produit**.

```text
image_1920          = source / master (inchangé)
image_shop_tile     = dérivé tuile /shop (normalisé CLI, import contrôlé)
grille /shop        = image_shop_tile si présente, sinon fallback standard
fiche produit / hero / culture = image standard uniquement
```

**Ce ticket ne contient pas de code.** L’implémentation nécessitera un ticket séparé après validation MOA de ce cadrage.

---

## Hypothèse fonctionnelle V1.5 lite

Mécanisme Odoo **léger** et **réversible** :

| Rôle | Champ / comportement |
|------|---------------------|
| Master | `image_1920` — jamais écrasé par le normalizer |
| Dérivé tuile | `image_shop_tile` — JPEG/WebP 1024×1024 baked-in `#F8EEDB` |
| Fallback | `image_512` si `image_shop_tile` absent |
| Usage | Grille `/shop` uniquement (`website_sale.products_item`) |
| Traçabilité | statut · version recette · date traitement |
| Import | Manuel ou semi-manuel depuis sorties CLI validées MOA |

---

## Proposition de modèle Odoo lite

### Extension `product.template`

| Champ | Type | Recommandation Dev |
|-------|------|-------------------|
| **`image_shop_tile`** | `Binary` | **Nom retenu** — clair, aligné cadrage MOA/pilote, suffisant pour V1.5 |
| **`shop_tile_status`** | `Selection` | `none` · `validated` · `validated_reserve` · `pending_review` · `rejected` |
| **`shop_tile_recipe_version`** | `Char` | ex. `ck_shop_tile_v1.1` |
| **`shop_tile_processed_at`** | `Datetime` | date import / validation opérateur |
| **`shop_tile_source_run`** | `Char` | optionnel — ex. `pilote_20260520` · traçabilité batch CLI |
| **`shop_tile_moa_note`** | `Char` | optionnel — réserve MOA courte (ex. « scène dense ») |

**Nom alternatif écarté pour V1.5** : `ck_image_shop_tile` — plus verbeux, sans gain fonctionnel ; réservé si collision future avec un champ standard Odoo.

### Pourquoi `product.template` uniquement ?

| Question | Réponse |
|----------|---------|
| Mettre sur `product.template` ? | **Oui** — la grille `/shop` itère sur `product.template` dans `products_item` |
| Variantes (`product.product`) ? | **Non en V1.5** — une tuile par template suffit pour Marketone retail-first |
| `product.image` galerie ? | **Non** — hors périmètre · risque confusion master / dérivé |

### Champs de traçabilité — utilité réelle

| Champ | Utile V1.5 ? | Rôle |
|-------|:------------:|------|
| `shop_tile_status` | **Oui** | Distinguer exploitable / réserve / rejeté sans relire le rapport CLI |
| `shop_tile_recipe_version` | **Oui** | Savoir quelle recette a produit la tuile · réimport si recette évolue |
| `shop_tile_processed_at` | **Oui** | Audit · détection tuiles obsolètes si `image_1920` change |
| `shop_tile_source_run` | Recommandé | Lien vers run CLI · import traçable |
| `shop_tile_moa_note` | Optionnel | Documenter réserve MOA sans BO lourd |

**Hors V1.5** : score G1–G6, `content_area_ratio`, preview live, historique versions multiples.

---

## Logique de fallback

### Chaîne recommandée (grille `/shop` uniquement)

```text
1. product.image_shop_tile présent     → afficher image_shop_tile
2. sinon product.image_512             → comportement Odoo standard actuel
3. jamais image_1920 direct en tuile   → laisser Odoo gérer ses dérivés
```

### Pourquoi `image_512` et pas `image_1920` ?

- Cohérent avec le rendu natif Odoo 19 sur `products_item` ;
- bande passante adaptée à la grille ;
- pas de régression perf ;
- le master `image_1920` reste réservé fiche produit / back-office.

### Feature flag (recommandé)

Paramètre `ir.config_parameter` :

```text
marketone.shop_tile_enabled = True | False
```

Si `False` : QWeb inchangé · rollback instantané sans migration de données.

---

## Adaptation QWeb minimale

### Principe

Un seul héritage ciblé sur `website_sale.products_item` dans `dorevia_ckreyol_marketone` :

- remplacer **uniquement** la source de l’image vignette ;
- ne pas toucher titre, prix, wishlist, structure UX-3 ;
- **priorité basse** (ex. `priority="50"`) pour laisser les surcharges thème/marketplace s’appliquer sur le reste.

### Approche recommandée

**Option A — xpath conditionnel (recommandée V1.5)** :

```xml
<!-- Pseudo-code cadrage — pas de code livré dans ce ticket -->
<template inherit_id="website_sale.products_item">
  <xpath expr="//span[contains(@t-field, 'image_512') or @t-field='product.image_512']" position="replace">
    <t t-if="product.image_shop_tile and request.env['ir.config_parameter'].sudo().get_param('marketone.shop_tile_enabled')">
      <span t-field="product.image_shop_tile"
            t-options="{'widget': 'image', 'qweb_img_res_model': 'product.template', ...}"/>
    </t>
    <t t-else="">
      <span t-field="product.image_512" t-options="..."/>
    </t>
  </xpath>
</template>
```

**Option B — helper Python** `_get_shop_grid_image_field()` :

- retourne `'image_shop_tile'` ou `'image_512'` ;
- QWeb plus propre mais nécessite adapter le widget image Odoo — légèrement plus de Dev.

**Recommandation** : **Option A** pour V1.5 lite — lisible, réversible, testable.

### Périmètre QWeb strict

| Zone | Utilise `image_shop_tile` ? |
|------|:----------------------------:|
| Grille `/shop` | **Oui** (si présent) |
| Fiche produit `/shop/<slug>` | **Non** |
| Panier / checkout | **Non** |
| Wishlist | **Non** (garder standard) |
| Hero / home / culture | **Non** |

### Régression `website_sale` standard

| Risque | Mitigation |
|--------|------------|
| Cas sans tuile dérivée | Fallback `image_512` — comportement identique à aujourd’hui |
| Feature flag off | Aucun changement visuel |
| SCSS UX-3 | Inchangé — tuile baked-in `#F8EEDB` + fond SCSS `#F8EEDB` = cohérent |
| Variantes / combinaisons | V1.5 ignore — template-level only |
| Module marketplace / thème | Tester héritages existants sur `products_item` (priorités 68–69 CK marketplace) |

**Marketone** (`dorevia_ckreyol_marketone`) n’a **pas** d’héritage `products_item` image aujourd’hui → surface de changement minimale sur l’instance Marketone pure. Si déploiement avec surcharges marketplace, valider compatibilité xpath en recette.

---

## Séparation master / dérivé

| Règle | Détail |
|-------|--------|
| **Écriture** | Import CLI → **`image_shop_tile` uniquement** |
| **Interdit** | Écrire `image_1920` depuis le normalizer ou un cron |
| **Lecture fiche** | Toujours `image_1920` / galerie standard |
| **Lecture grille** | `image_shop_tile` → fallback `image_512` |
| **Suppression tuile** | Vider `image_shop_tile` → retour immédiat au standard |
| **Obsolescence** | Si `image_1920` change · tuile dérivée **non recalculée auto** — alerte opérateur via comparaison dates (V1.5 lite : note doc · V2 : warning BO) |

Schéma :

```text
Source fournisseur / BO
        │
        ▼
   image_1920  ──────────────────►  fiche produit · BO · autres usages
        │
        │  CLI externe (ck_shop_tile_v1.1)
        ▼
   image_shop_tile  ─────────────►  grille /shop uniquement
```

---

## Flux d’import manuel / semi-manuel

### Principe

Pas d’automatisation dangereuse. Import **contrôlé par opérateur** après validation MOA du lot CLI.

### Flux proposé V1.5

```text
1. CLI batch → output/webp/ + output/jpeg/ + reports/batch_*.csv
2. MOA valide les lignes exploitables (E/R/OK) — pilote_operateur.csv ou équivalent
3. Opérateur lance script import (ticket implémentation)
4. Script : match SKU / default_code / référence manifest → product.template
5. Écrit image_shop_tile + shop_tile_* metadata
6. Log import CSV (succès / skip / erreur)
7. Revue visuelle /shop sur échantillon
```

### Script proposé (implémentation future)

```text
scripts/import_shop_tiles.py
  --run-dir tools/ck_image_normalizer/reports/runs/<run_id>/
  --decisions pilote_operateur.csv   # ou export MOA filtré validated only
  --dry-run                          # défaut recommandé
  --apply                            # écriture explicite
  --format jpeg|webp                 # jpeg recommandé V1.5 (compat Odoo binary)
```

### Garde-fous import

| Règle | Détail |
|-------|--------|
| `--dry-run` par défaut | Aucune écriture sans flag explicite |
| Filtre statuts | Importer **uniquement** `validated` / `validated_reserve` |
| Pas de cron | Import = action opérateur |
| Pas de massif catalogue | Lot par lot · GO MOA par lot |
| Log traçable | Fichier `import_shop_tiles_YYYYMMDD.log` |

---

## Vue BO minimale (V1.5 lite)

**Pas de BO complet.** Extension légère :

| Élément | Détail |
|---------|--------|
| Onglet ou groupe « Tuile /shop » | Sur formulaire `product.template` · mode développeur ou groupe dédié |
| Champs visibles | `image_shop_tile` · `shop_tile_status` · `shop_tile_recipe_version` · `shop_tile_processed_at` |
| Preview | Image widget standard Odoo |
| Masqué en V1.5 | Studio recette · batch · regénération auto |

---

## Tests minimaux (implémentation future)

| # | Test | Attendu |
|---|------|---------|
| T1 | Produit **avec** `image_shop_tile` sur `/shop` | Tuile dérivée affichée |
| T2 | Produit **sans** `image_shop_tile` | `image_512` — identique à avant |
| T3 | Fiche produit | `image_1920` / image standard — **pas** tuile dérivée |
| T4 | `marketone.shop_tile_enabled=False` | Fallback total · aucune tuile dérivée |
| T5 | Import dry-run | 0 écriture · log correct |
| T6 | Import apply sur 1 SKU pilote | Champs remplis · `/shop` OK |
| T7 | Suppression `image_shop_tile` | Retour fallback immédiat |

Framework : tests HTTP `HttpCase` Marketone existants (`test_marketone_lot3_shop.py` comme base).

---

## Estimation effort V1.5 lite

| Lot | Contenu | Effort |
|-----|---------|--------|
| **M1** | Modèle `product.template` + champs traçabilité | **1–2 j/h** |
| **M2** | Vue BO minimale | **0.5–1 j/h** |
| **M3** | Héritage QWeb `products_item` + feature flag | **2–3 j/h** |
| **M4** | Script import semi-manuel + log | **2–3 j/h** |
| **M5** | Tests T1–T7 + recette manuelle | **2–3 j/h** |
| **MOA** | Import pilote 43 SKU + revue /shop | **2–4 h** |
| **Total** | | **8–12 j/h Dev** + MOA |

Hors scope V1.5 (V2+) : cron · on_write · BO audit · WebP natif · multi-recettes · variantes.

---

## Risques

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Double fond (#F8EEDB baked-in + SCSS) | Faible | Cohérent UX-3 B1 · pas de multiply |
| Tuile obsolète si master change | Moyen | `shop_tile_processed_at` · procédure opérateur · pas d’auto-sync V1.5 |
| XPath QWeb fragile (Odoo / thème) | Moyen | Tests · feature flag · xpath robuste · recette upgrade Odoo |
| Confusion opérateur master/dérivé | Moyen | Doc · libellés BO clairs · import log |
| Taille binaire catalogue | Faible | JPEG 1024×1024 acceptable · ~80–200 Ko/tuile |
| Scope creep vers BO complet | Élevé | Ticket implémentation strict · garde-fous MOA |
| Régression grille sans tuile | Élevé si mal cadré | Fallback obligatoire · T2 · feature flag |

---

## Stratégie de rollback

| Niveau | Action | Effet |
|--------|--------|-------|
| **R0 — immédiat** | `marketone.shop_tile_enabled = False` | Grille revient à 100 % standard |
| **R1 — produit** | Vider `image_shop_tile` | Fallback unitaire |
| **R2 — module** | Désinstaller / désactiver héritage QWeb | Retour natif `website_sale` |
| **R3 — données** | Conserver champs · ne pas migrer | Réactivation possible |

Les champs peuvent rester en base sans impact visuel si QWeb est désactivé.

---

## Critères GO / NO GO — implémentation V1.5

### GO implémentation si

| Critère | Seuil pilote | État |
|---------|--------------|------|
| Pilote clôturé GO avec réserves | Oui | ✅ |
| Recette candidate stable | `ck_shop_tile_v1.1` | ✅ |
| Taux exploitable mesuré | ≥ 80 % | ✅ **86 %** |
| Sas opérateur viable | Oui | ✅ |
| Séparation master/dérivé acceptée MOA | Oui | ✅ |
| Ce ticket P6 validé MOA | Oui | ☐ **En attente** |
| Import manuel / semi-manuel accepté | Oui | ☐ **En attente** |

### NO GO implémentation si

- MOA exige traitement auto à l’upload ou cron massif ;
- MOA exige remplacement `image_1920` ;
- MOA exige BO studio complet en V1.5 ;
- incompatibilité QWeb non résolue avec surcharges marketplace actives.

---

## Hors périmètre P6 et V1.5 lite

| Élément | Statut |
|---------|--------|
| BO complet retraitement image | ❌ V2+ |
| Cron massif | ❌ |
| Traitement auto à l’upload | ❌ |
| Remplacement `image_1920` | ❌ |
| Génération image depuis Odoo | ❌ |
| IA / détourage / `rembg` | ❌ |
| Galerie fiche produit | ❌ |
| Hero / éditorial / culture / origines | ❌ |
| Moteur média global CK | ❌ |
| Modification recette v1.1 | ❌ sans arbitrage MOA |
| Code dans ce ticket P6 | ❌ **cadrage uniquement** |

---

## Réponses aux questions MOA

| # | Question | Réponse Dev |
|---|----------|-------------|
| 1 | Nom de champ ? | **`image_shop_tile`** — aligné pilote/cadrage · suffisant V1.5 |
| 2 | `product.template` uniquement ? | **Oui** — retail-first · pas de variante en V1.5 |
| 3 | Fallback si vide ? | **`image_512`** — comportement standard grille Odoo |
| 4 | Héritage QWeb minimal ? | **Un xpath** sur image vignette `products_item` · feature flag |
| 5 | Éviter régression `website_sale` ? | **Fallback obligatoire** + flag off + tests T2/T4 |
| 6 | Séparation master/dérivé ? | **Champs séparés** · import n’écrit jamais `image_1920` |
| 7 | Import CLI sans automatisme ? | **Script semi-manuel** · dry-run · filtre statuts MOA · log |
| 8 | Champs traçabilité utiles ? | **status + recipe_version + processed_at** (+ source_run optionnel) |
| 9 | Tests minimaux ? | **T1–T7** (grille, fiche, fallback, flag, import) |
| 10 | Effort V1.5 lite ? | **8–12 j/h Dev** + 2–4 h MOA |
| 11 | Risques techniques / UX ? | Obsolescence tuile · xpath fragile · confusion opérateur — voir § Risques |
| 12 | Rollback ? | **Feature flag** → vider champ → désactiver héritage QWeb |

---

## Garde-fous maintenus

Même en P6 et pour toute implémentation V1.5 future :

```text
Pas de remplacement image_1920
Pas de traitement massif automatique
Pas de cron
Pas de BO complet
Pas d'industrialisation sans GO MOA
Pas de modification du moteur e-commerce
website_sale reste le moteur unique (ADR-002)
```

---

## Plan P6 → implémentation

| Phase | Action | Responsable | Statut |
|-------|--------|-------------|--------|
| **P6** | Cadrage V1.5 Odoo lite | MOA + Dev | ✅ **Validé MOA** (2026-05-20) |
| **P6-MOA** | Validation cadrage MOA | MOA | ✅ **GO validation P6** |
| **P7** | Ticket implémentation V1.5 lite | Dev | ✅ **Ouvert** · [`TICKET_V1_5_IMPLEMENTATION`](./TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION.md) |
| **P7-MOA** | Import pilote 43 SKU + revue /shop | MOA | ☐ |
| **P8** | Extension lot X / catalogue élargi | MOA | ☐ **Hors V1.5 initiale** |

**Séquence figée** :

```text
POC (clôturé) → Pilote (clôturé) → P6 cadrage V1.5 (ce ticket) → P7 implémentation V1.5 (ticket séparé)
```

---

## Décision MOA (2026-05-20)

```text
GO validation P6 cadrage V1.5 Odoo lite — autorisation d’ouvrir un ticket P7 d’implémentation séparé.
```

```text
P6 cadrage validé MOA — GO ouverture ticket P7 implémentation V1.5 lite.
```

→ [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION.md`](./TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION.md)

**Décision Dev (cadrage livré)** :

```text
P6 cadrage validé MOA — P7 implémentation ouvert — en attente démarrage Dev.
```

---

## Références

| Document | Rôle |
|----------|------|
| [`REPONSE_MOA_CLOTURE_PILOTE_MEDIA_CATALOGUE.md`](../../recette/boutique/REPONSE_MOA_CLOTURE_PILOTE_MEDIA_CATALOGUE.md) | Clôture pilote · signal P6 |
| [`RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md`](../../recette/boutique/RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md) | Clôture pilote · bilan 43/50 |
| [`REGLE_CATALOGUE_IMAGES_SOURCE.md`](../../cadrage/REGLE_CATALOGUE_IMAGES_SOURCE.md) | Règle source distincte |
| [`NOTE_CK_IMAGE_NORMALIZER_SHOP_V1.md`](../../cadrage/NOTE_CK_IMAGE_NORMALIZER_SHOP_V1.md) | Cadrage technique initial |
| [`RECETTE_MANUELLE_SHOP_UX3_PRODUCT_CARDS.md`](../../recette/ux/RECETTE_MANUELLE_SHOP_UX3_PRODUCT_CARDS.md) | Contexte visuel tuiles |
| [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION.md`](./TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION.md) | **P7 implémentation** — ouvert MOA |
| [`tools/ck_image_normalizer/README.md`](../../../../tools/ck_image_normalizer/README.md) | CLI opérateur |
| `static/src/scss/_shop_product_cards.scss` | Tokens tuiles actuels |

---

## Historique

| Date | Auteur | Action |
|------|--------|--------|
| 2026-05-20 | MOA | **P6 validé** · **GO P7** · [`TICKET_V1_5_IMPLEMENTATION`](./TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION.md) |
| 2026-05-20 | MOA | **GO ouverture P6** — cadrage V1.5 · pas de GO implémentation directe |
| 2026-05-20 | Dev | **P6 cadrage livré** — ce ticket |
