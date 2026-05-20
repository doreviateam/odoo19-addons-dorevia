# Préparation MOA — pilote média catalogue 50 SKU

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-05-20 |
| **Ticket** | [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md`](../../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md) |
| **Décision amont** | GO pilote média catalogue |
| **Recette** | `ck_shop_tile_v1.1` |
| **Périmètre** | Tuiles commerce `/shop` uniquement |
| **Statut MOA** | **GO pilote avec réserves** — P5 clôture |

---

## 1. État réel constaté

Contrôle effectué sur la base `ckr-marketone-01` (2026-05-20) :

```text
Produits publiés, vendables, avec image_1920 : 50
Objectif pilote initial : 50 SKU
Écart : 0 — objectif volume atteint
```

Extension catalogue : **23 produits** ajoutés (`CK-MO-028` … `CK-MO-050`) — voir [`MAPPING_CATALOGUE_EXTENSION_23_PRODUITS.md`](../../cadrage/MAPPING_CATALOGUE_EXTENSION_23_PRODUITS.md).

Le dossier pilote médias reste à alimenter :

```text
tools/ck_image_normalizer/input/pilote/
```

```text
GO exécution : acté et exécuté (run pilote_20260520)
GO exploitation : non — P4 revue 29 NEEDS_REVIEW requise
```

---

## 2. Candidats disponibles dans la base

Ces 27 produits peuvent constituer le noyau du lot pilote, sous réserve de contrôle visuel MOA des images sources.

| # | Produit | URL boutique | Catégories publiques |
|---:|---------|--------------|----------------------|
| 1 | Maniocookies salés La Platine | `/shop/maniocookies-sales-la-platine-7` | Incontournables · Apéritif créole · Biscuits salés · Cuisine du manioc |
| 2 | Crackers manioc Sainte-Anne | `/shop/crackers-manioc-sainte-anne-8` | Incontournables · Apéritif créole · Biscuits salés · Cuisine du manioc |
| 3 | Pâtes de manioc Mayotte | `/shop/pates-de-manioc-mayotte-9` | Incontournables · Cuisine du manioc · Fécules |
| 4 | Confiture banane flambée | `/shop/confiture-banane-flambee-153` | Incontournables · Confitures · Idées cadeaux |
| 5 | Colombo des Antilles (épices) | `/shop/colombo-des-antilles-epices-154` | Incontournables · Épices |
| 6 | Shrub agrumes créole | `/shop/shrub-agrumes-creole-155` | Incontournables · Apéritif créole · Sirops |
| 7 | Biscuits coco vanille | `/shop/biscuits-coco-vanille-156` | Incontournables · Biscuits sucrés |
| 8 | Sirop de canne vanille | `/shop/sirop-de-canne-vanille-157` | Incontournables · Sirops |
| 9 | Sauce piment cadji | `/shop/sauce-piment-cadji-158` | Incontournables · Apéritif créole · Sauces |
| 10 | Rougail épices Réunion | `/shop/rougail-epices-reunion-159` | Incontournables · Assaisonnements |
| 11 | Chutney mangue verte | `/shop/chutney-mangue-verte-160` | Incontournables · Apéritif créole · Condiments |
| 12 | Café arabica Antilles | `/shop/cafe-arabica-antilles-161` | Incontournables · Boissons |
| 13 | Infusion vétiver citronnelle | `/shop/infusion-vetiver-citronnelle-162` | Incontournables · Boissons |
| 14 | Mix beignets manioc | `/shop/mix-beignets-manioc-163` | Incontournables · Cuisine du manioc · Farines |
| 15 | Miel créole baie rose | `/shop/miel-creole-baie-rose-164` | Incontournables · Idées cadeaux · Miels |
| 16 | Coffret gourmand îles créoles | `/shop/coffret-gourmand-iles-creoles-177` | Incontournables · Idées cadeaux · Kits & Coffrets |
| 17 | Palets manioc croustillants La Platine | `/shop/palets-manioc-croustillants-la-platine-178` | Incontournables · Apéritif créole · Biscuits salés · Cuisine du manioc |
| 18 | Mélange épices caraïbes | `/shop/melange-epices-caraibes-179` | Incontournables · Épices |
| 19 | Tartinade coco citron vert | `/shop/tartinade-coco-citron-vert-180` | Incontournables · Condiments |
| 20 | Assortiment apéritif créole | `/shop/assortiment-aperitif-creole-181` | Incontournables · Apéritif créole · Idées cadeaux · Kits & Coffrets |
| 21 | Confiture ananas vanille | `/shop/confiture-ananas-vanille-182` | Incontournables · Confitures · Idées cadeaux |
| 22 | Chips banane plantain salées | `/shop/chips-banane-plantain-salees-183` | Incontournables · Apéritif créole · Biscuits salés · Cuisine du manioc |
| 23 | Semoule manioc fine Mayotte | `/shop/semoule-manioc-fine-mayotte-184` | Incontournables · Cuisine du manioc · Fécules |
| 24 | Confiture fruits de la passion | `/shop/confiture-fruits-de-la-passion-185` | Incontournables · Confitures |
| 25 | Trio sirops des Antilles | `/shop/trio-sirops-des-antilles-186` | Incontournables · Idées cadeaux · Kits & Coffrets |
| 26 | Marinade jerk authentique | `/shop/marinade-jerk-authentique-187` | Incontournables · Apéritif créole · Assaisonnements |
| 27 | Coffret biscuits et douceurs | `/shop/coffret-biscuits-et-douceurs-188` | Incontournables · Apéritif créole · Idées cadeaux · Kits & Coffrets |

---

## 3. Décision MOA

Le volume **50 SKU** est couvert côté catalogue BO.

| Option | Statut |
|--------|--------|
| **A — 50 SKU BO** | ✅ **Retenu** — extension +23 appliquée |
| B — Pilote réduit 27 | Non retenu |
| C — Lot mixte hors BO | Non requis |

Inventaire complet : [`catalogue_pilote_50_produits.csv`](./catalogue_pilote_50_produits.csv)

---

## 4. Prochaines actions MOA

### P1 — Compléter le lot

- [x] **50 SKU** vendables publiés en BO (27 + 23 extension)
- [ ] Valider visuellement les fiches sur `/shop`
- [x] **50 images** exportées → `input/pilote/`
- [x] `manifest.pilote.csv` — 50 lignes
- [x] Batch v1.1 exécuté — [`RAPPORT_PILOTE_MEDIA_50SKU_20260520.md`](./RAPPORT_PILOTE_MEDIA_50SKU_20260520.md)
- [x] P4 — 29 `NEEDS_REVIEW` notés · [`RAPPORT_P4_PILOTE_MEDIA_50SKU_20260520.md`](./RAPPORT_P4_PILOTE_MEDIA_50SKU_20260520.md)
- [ ] P5 — validation officielle GO avec réserves

### P2 — Préparer les fichiers

- [ ] Déposer les 50 images dans `tools/ck_image_normalizer/input/pilote/`
- [ ] Créer `tools/ck_image_normalizer/manifest.pilote.csv`
- [ ] Renseigner les colonnes :

```csv
filename,profile,reference,sku_ref,source_type,lot_pilote,notes
```

### P3 — Signal Dev

À envoyer uniquement après contrôle des 50 fichiers et du manifest :

```text
GO exécution pilote média — 50 SKU sélectionnés — manifest prêt
```

---

## 5. Signal actuel

Signal MOA à consigner maintenant :

```text
GO pilote avec réserves — 36/50 exploitable (72 %) — sas NEEDS_REVIEW indispensable — pas d'exploitation auto.
```

Addendum consolidé après mini-batches ciblés :

```text
GO pilote avec réserves — 43/50 exploitables (86 %) — lot X maintenu en demande fournisseur / exclusion temporaire — pas d'exploitation auto.
```
