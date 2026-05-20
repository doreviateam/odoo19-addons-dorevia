# Trame revue visuelle MOA — promotion `validated_grid` produit par produit

| Champ | Valeur |
|-------|--------|
| **Signal MOA** | GO préparation trame revue visuelle produit par produit |
| **Date** | 2026-05-20 |
| **Base** | `ckr-marketone-01` · sandbox `http://localhost:18079` |
| **Flag** | `marketone.shop_tile_enabled = True` |
| **Doctrine** | [`DOCTRINE_IMAGE_V2.md`](../../cadrage/DOCTRINE_IMAGE_V2.md) |
| **Phase précédente** | Alignement doctrine v2 — **clôturée MOA** |
| **Statut phase** | **Clôturée — GO visuel MOA post-promotion** (2026-05-20) |

---

## 1) Objectif MOA

Permettre à la MOA de promouvoir en **`validated_grid`** uniquement les tuiles réellement conformes à la cible visuelle grille `/shop`.

> Un dérivé stocké dans `image_shop_tile` **n'est pas** automatiquement affichable.  
> Seul `shop_tile_status = validated_grid` active l'affichage tuile en grille (si flag actif).

---

## 2) État actuel (extrait base 2026-05-20)

| Indicateur | Valeur |
|-----------|--------|
| Tuiles dérivées (`image_shop_tile` présent) | **40** |
| **`validated_grid`** (affichage tuile actif) | **0** |
| **`validated_storage`** (périmètre principal revue) | **20** |
| **`validated_reserve`** | **17** |
| **`pending_review`** | **3** |
| Fallback master P1/P2 (sans tuile) | **3** (154, 156, 471) |
| Recette active | `ck_shop_tile_v1.1` uniquement |
| Master `image_1920` | **protégé** — jamais modifié par cette phase |

**Affichage grille actuel** : fallback master sur **100 %** du pilote (0 `validated_grid`).

---

## 3) Critères MOA de promotion `validated_grid`

Une tuile ne peut passer en `validated_grid` **que si** :

| Critère | Attendu |
|---------|---------|
| Image pleine | bord à bord, ou rendu naturellement intégré |
| Rectangle interne | **absent** |
| Produit flottant | **absent** |
| Halo / frange | **absent** |
| Transparence | **absente** |
| Cohérence grille | homogène avec les autres tuiles `/shop` |
| Rendu premium | acceptable sur mobile et desktop |

**Référence comportementale** : photo pleine type **Colombo master** (lifestyle maîtrisé), pas un produit détouré flottant sur fond bake-in.

---

## 4) Mode opératoire revue MOA

### 4.1 Parcours recommandé (par produit)

1. Ouvrir la fiche produit Odoo (BO) — vérifier `image_1920` (master) et `image_shop_tile` (dérivé).
2. Ouvrir le lien sandbox `/shop` (colonne `lien_shop_sandbox`) — **constater le rendu réel grille** (aujourd'hui = master).
3. Ouvrir le JPEG tuile dérivée (colonne `lien_jpeg_tuile`) — comparer au rendu attendu si promotion.
4. Renseigner dans le CSV : `decision_moa`, `motif_principal`, `commentaire_moa`.
5. Optionnel : joindre une capture écran nommée `capture_revue_{product_id}_{slug}.png`.

### 4.2 URL sandbox

Préfixe : `http://localhost:18079`

Exemple Crackers (8) : `http://localhost:18079/shop/crackers-manioc-sainte-anne-8`

### 4.3 Fichiers CSV à compléter

| Fichier | Contenu |
|---------|---------|
| [`TRAME_REVUE_VISUELLE_MOA_VALIDATED_STORAGE.csv`](./TRAME_REVUE_VISUELLE_MOA_VALIDATED_STORAGE.csv) | **20 produits** — périmètre principal |
| [`TRAME_REVUE_VISUELLE_MOA_ANNEXE.csv`](./TRAME_REVUE_VISUELLE_MOA_ANNEXE.csv) | 17 `validated_reserve` + 3 `pending_review` + 3 fallback P1/P2 |
| [`TRAME_REVUE_VISUELLE_MOA_PRODUIT_PAR_PRODUIT.csv`](./TRAME_REVUE_VISUELLE_MOA_PRODUIT_PAR_PRODUIT.csv) | Vue consolidée **43 lignes** |

---

## 5) Colonnes décision MOA (à renseigner)

### `decision_moa` — valeurs autorisées

| Valeur | Effet attendu (phase Dev suivante) |
|--------|-------------------------------------|
| **`validated_grid`** | Promotion affichage tuile en grille `/shop` |
| **`validated_storage`** | Maintien stockage dérivé · pas d'affichage grille |
| **`needs_review_source`** | Gouvernance source · redemande / recadrage fournisseur |
| **`fallback_master`** | Pas de tuile en grille · master `image_1920` seul |
| **`exclusion_temporaire`** | Produit exclu du lot promotion · revue ultérieure |

### `motif_principal` — valeurs autorisées

| Valeur | Usage |
|--------|-------|
| `OK_visuel` | Conforme globalement |
| `image_pleine_conforme` | Image pleine bord à bord — référence cible |
| `rectangle_interne` | Effet carte / cadre interne visible |
| `produit_flottant` | Produit détouré flottant sur fond |
| `halo` | Frange / halo autour du produit |
| `source_faible` | Qualité ou cadrage source insuffisant |
| `recadrage_necessaire` | Source exploitable après recadrage |
| `a_completer` | Motif non listé — détailler en commentaire |

---

## 6) Liste principale — `validated_storage` (20 produits)

> **Cas particulier MOA** : **Crackers manioc Sainte-Anne (8)** — reste `validated_storage` jusqu'à revue capture MOA. **Aucune promotion automatique.**

| ID | default_code | Produit | Lien /shop | JPEG tuile |
|----|--------------|---------|------------|------------|
| 8 | — | Crackers manioc Sainte-Anne | [/shop/...-8](http://localhost:18079/shop/crackers-manioc-sainte-anne-8) | `reprocess_product8_20260520` · master backup archivé |
| 155 | — | Shrub agrumes créole | [/shop/...-155](http://localhost:18079/shop/shrub-agrumes-creole-155) | `06_product-155_shrub-agrumes-creole.jpg` |
| 177 | — | Coffret gourmand îles créoles | [/shop/...-177](http://localhost:18079/shop/coffret-gourmand-iles-creoles-177) | `16_product-177_coffret-gourmand-iles-creoles.jpg` |
| 178 | — | Palets manioc croustillants La Platine | [/shop/...-178](http://localhost:18079/shop/palets-manioc-croustillants-la-platine-178) | `17_product-178_palets-manioc-croustillants-la-platine.jpg` |
| 183 | — | Chips banane plantain salées | [/shop/...-183](http://localhost:18079/shop/chips-banane-plantain-salees-183) | `22_product-183_chips-banane-plantain-salees.jpg` |
| 187 | — | Marinade jerk authentique | [/shop/...-187](http://localhost:18079/shop/marinade-jerk-authentique-187) | `26_product-187_marinade-jerk-authentique.jpg` |
| 470 | CK-MO-031 | Marinade jerk citron vert | [/shop/...-470](http://localhost:18079/shop/ck-mo-031-marinade-jerk-citron-vert-470) | `31_ck-mo-031_marinade-jerk-citron-vert.jpg` |
| 473 | CK-MO-034 | Chips patate douce créole | [/shop/...-473](http://localhost:18079/shop/ck-mo-034-chips-patate-douce-creole-473) | `34_ck-mo-034_chips-patate-douce-creole.jpg` |
| 474 | CK-MO-035 | Crackers sarrasin Réunion | [/shop/...-474](http://localhost:18079/shop/ck-mo-035-crackers-sarrasin-reunion-474) | `35_ck-mo-035_crackers-sarrasin-reunion.jpg` |
| 475 | CK-MO-036 | Sauce chien antillaise | [/shop/...-475](http://localhost:18079/shop/ck-mo-036-sauce-chien-antillaise-475) | `36_ck-mo-036_sauce-chien-antillaise.jpg` |
| 476 | CK-MO-037 | Tapenade agrumes confits | [/shop/...-476](http://localhost:18079/shop/ck-mo-037-tapenade-agrumes-confits-476) | `37_ck-mo-037_tapenade-agrumes-confits.jpg` |
| 477 | CK-MO-038 | Confiture christophine gingembre | [/shop/...-477](http://localhost:18079/shop/ck-mo-038-confiture-christophine-gingembre-477) | `38_ck-mo-038_confiture-christophine-gingembre.jpg` |
| 478 | CK-MO-039 | Confiture papaye muscovado | [/shop/...-478](http://localhost:18079/shop/ck-mo-039-confiture-papaye-muscovado-478) | `39_ck-mo-039_confiture-papaye-muscovado.jpg` |
| 479 | CK-MO-040 | Quatre épices créoles | [/shop/...-479](http://localhost:18079/shop/ck-mo-040-quatre-epices-creoles-479) | `40_ck-mo-040_quatre-epices-creoles.jpg` |
| 480 | CK-MO-041 | Poudre colombo créole | [/shop/...-480](http://localhost:18079/shop/ck-mo-041-poudre-colombo-creole-480) | `41_ck-mo-041_poudre-colombo-creole.jpg` |
| 481 | CK-MO-042 | Bouillon légumes des îles | [/shop/...-481](http://localhost:18079/shop/ck-mo-042-bouillon-legumes-des-iles-481) | `42_ck-mo-042_bouillon-legumes-des-iles.jpg` |
| 482 | CK-MO-043 | Rougail tomate créole | [/shop/...-482](http://localhost:18079/shop/ck-mo-043-rougail-tomate-creole-482) | `43_ck-mo-043_rougail-tomate-creole.jpg` |
| 483 | CK-MO-044 | Sirop jambosier | [/shop/...-483](http://localhost:18079/shop/ck-mo-044-sirop-jambosier-483) | `44_ck-mo-044_sirop-jambosier.jpg` |
| 485 | CK-MO-046 | Jus goyave passion | [/shop/...-485](http://localhost:18079/shop/ck-mo-046-jus-goyave-passion-485) | `46_ck-mo-046_jus-goyave-passion.jpg` |
| 486 | CK-MO-047 | Infusion bois bandé | [/shop/...-486](http://localhost:18079/shop/ck-mo-047-infusion-bois-bande-486) | `47_ck-mo-047_infusion-bois-bande.jpg` |

Chemin JPEG pilote (racine repo) : `tools/ck_image_normalizer/reports/runs/pilote_20260520/output/jpeg/`

---

## 7) Annexe — autres statuts (23 produits)

### 7.1 `validated_reserve` (17) — tuile stockée avec réserve historique

Produits : 7, 153, 158, 159, 160, 163, 164, 179, 180, 181, 185, 186, 467, 468, 469, 472, 489.

> Revue MOA recommandée avant toute promotion : plusieurs cas lifestyle avec produit petit dans la scène.

### 7.2 `pending_review` / Lot B (3) — tuile stockée, source à questionner

| ID | Produit | Note Dev |
|----|---------|----------|
| 9 | Pâtes de manioc Mayotte | NEEDS_REVIEW_SOURCE — effet rectangle interne |
| 184 | Semoule manioc fine Mayotte | NEEDS_REVIEW_SOURCE — effet rectangle interne |
| 188 | Coffret biscuits et douceurs | NEEDS_REVIEW_SOURCE — effet rectangle interne |

### 7.3 Fallback master P1/P2 (3) — sans tuile active

| ID | Produit | Affichage actuel | Rapport |
|----|---------|------------------|---------|
| 154 | Colombo des Antilles (épices) | `image_1920` master | [`RAPPORT_P1_P2_FALLBACK_RECTANGLE_EXECUTION.md`](./RAPPORT_P1_P2_FALLBACK_RECTANGLE_EXECUTION.md) |
| 156 | Biscuits coco vanille | `image_1920` master | idem |
| 471 | Biscuits banane confiture | `image_1920` master | idem |

Décision MOA attendue : confirmer maintien fallback master ou rouvrir gouvernance source.

---

## 8) Cas spécial — Crackers manioc Sainte-Anne (product_id=8)

| Élément | Détail |
|---------|--------|
| Statut actuel | `validated_storage` |
| Master `image_1920` | **restauré** · RGBA 285×271 · backup `docs/recette/boutique/reprocess/product-8_image_1920_master_backup_20260520.png` |
| Tuile `image_shop_tile` | retraitée v1.1 fill 0.92 · run `reprocess_product8_20260520` |
| Affichage grille | **fallback master** (pas de promotion auto) |
| Action MOA | Revue visuelle capture `/shop` + JPEG tuile avant toute décision |

---

## 9) Garde-fous (maintenus pendant la revue)

- `image_1920` **jamais modifié** sans décision MOA explicite
- Pas de promotion automatique en `validated_grid`
- Pas d'alpha · pas d'IA / rembg · pas de cron · pas de traitement massif
- Rollback global via `marketone.shop_tile_enabled`
- Phase Dev suivante = **import CSV décisions MOA uniquement** (pas de retraitement moteur sans GO séparé)

---

## 10) Retour MOA attendu

1. CSV complété (`decision_moa` + `motif_principal` + `commentaire_moa` + `date_revue_moa` + `revue_par`)
2. Captures optionnelles pour cas litigieux (rectangle, halo, flottant)
3. Signal explicite : **GO exécution promotions `validated_grid`**

---

## 11) Références

- [`DOCTRINE_IMAGE_V2.md`](../../cadrage/DOCTRINE_IMAGE_V2.md)
- [`PLAN_ALIGNEMENT_DOCTRINE_IMAGE_V2.md`](./PLAN_ALIGNEMENT_DOCTRINE_IMAGE_V2.md)
- [`RAPPORT_P1_P2_FALLBACK_RECTANGLE_EXECUTION.md`](./RAPPORT_P1_P2_FALLBACK_RECTANGLE_EXECUTION.md)
- [`import_reprocess_product8_crackers.csv`](./import_reprocess_product8_crackers.csv)
- [`import_pilote_43_shop_tiles.csv`](./import_pilote_43_shop_tiles.csv)

---

## Signal Dev

```text
Trame revue visuelle MOA livrée — 20 validated_storage (périmètre principal) + 23 lignes annexe — 0 validated_grid en base — aucune action technique avant retour CSV MOA.
```
