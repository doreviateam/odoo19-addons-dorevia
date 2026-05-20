# Recette manuelle — Tuile shop conversion — `/shop`

| Champ | Valeur |
|-------|--------|
| **Module** | `dorevia_ckreyol_marketone` |
| **Version cible** | **`19.0.15.8.1`** |
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079/shop |
| **Statut recette** | **GO MOA** |
| **Signal MOA** | GO photo pleine **≥ 30 tuiles** · GO CTA Voir gauche + prix droite · **GO panier au survol + popup au clic** |
| **Rapport exécution** | [`RAPPORT_RECETTE_SHOP_CONVERSION_TILE_20260520.md`](./RAPPORT_RECETTE_SHOP_CONVERSION_TILE_20260520.md) |

---

## Périmètre

Recette **visuelle et comportementale** de la tuile produit `/shop` — variante conversion MOA.

**Hors périmètre (inchangé)** :

- doctrine image v2 · `image_1920` · `image_shop_tile` · `validated_grid` · fallback master
- fiche produit · sidebar · filtres · panier page · checkout

**Fichiers concernés** :

| Fichier | Rôle |
|---------|------|
| `views/pages/shop.xml` | Classe `o_wsale_products_opt_thumb_cover` sur la grille |
| `views/pages/shop_product_tile_conversion.xml` | QWeb tuile conversion |
| `views/pages/shop_product_tile_image.xml` | Image grille (`validated_grid` / fallback) |
| `static/src/scss/_shop_product_cards.scss` | Styles cartes `.marketone-shop` |

---

## Structure cible MOA

```text
Photo pleine (clic → fiche produit)
  + wishlist overlay (haut droit)
  + panier au survol (bas droit zone photo)

Titre produit — 2 lignes réservées

Voir                                      8,90 €
```

| Zone | Comportement attendu |
|------|---------------------|
| Photo | Pleine bord à bord · `object-fit: cover` · **pas d’effet « image dans l’image »** · pas de marge beige entre bord tuile et photo |
| Wishlist | Icône cœur discrète · overlay haut droit |
| Panier | Visible au **survol** de la carte / zone photo · add-to-cart Odoo standard |
| Titre | 2 lignes réservées · troncature propre si long |
| Description courte | **Absente** en grille (`description_sale` masquée) |
| Ligne basse | **Voir** à gauche · **prix** poussé au bord droit · séparation nette |
| CTA Voir | Lien vers fiche produit (`product_href`) |

---

## Prérequis

1. Module à jour :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone --stop-after-init
docker restart sandbox-odoo19-odoo-1
```

2. Hard refresh navigateur (Cmd+Shift+R / Ctrl+Shift+R).
3. Flag tuile actif (état pilote) :

```text
marketone.shop_tile_enabled = True
```

4. État image attendu (post-promotion MOA) :

```text
Produits publiés /shop      : 50
validated_grid actifs       : 19  (100 % à contrôler — V1b)
validated_storage           : 4
needs_review_source         : 17
fallback / pending / none   : 10
```

---

## V1 — Grille desktop (≥ 992px)

| Étape | Vérification | Attendu | ☐ |
|-------|--------------|---------|---|
| 1 | Ouvrir `/shop` | Grille 4 colonnes · scope `.marketone-shop` | |
| 2 | Carte — zone photo | Image pleine · cover · pas de rectangle interne · pas de produit flottant · **bords photo = bords zone image** | |
| 3 | Produit `validated_grid` (ex. Shrub 155, Coffret 177) | Tuile dérivée affichée si conforme MOA | |
| 4 | Produit fallback (ex. Crackers 8, Colombo 154) | Master `image_1920` · pas de dégradé vs GO post-promotion | |
| 5 | Wishlist | Cœur discret haut droit · ne masque pas le produit | |
| 6 | Survol carte | Panier apparaît bas droit **sur la photo** · pas dans la ligne basse | |
| 7 | Titre | Hauteur 2 lignes réservée · grille homogène | |
| 8 | Description courte | **Absente** sous le titre | |
| 9 | Ligne basse | `Voir` collé à gauche · prix collé à droite · espace central libre | |
| 10 | Clic photo | Navigation fiche produit | |
| 11 | Clic `Voir` | Navigation fiche produit (même URL que titre) | |
| 12 | Clic panier | Ajout panier · reste sur `/shop` | |

---

## V1b — Photo pleine bord à bord (point critique MOA)

Recette ciblée sur la régression **« image inset »** — contrôle **systématique sur au moins 30 tuiles** visibles sur `/shop`, et **non** sur un seul produit témoin.

### Protocole d’échantillonnage — minimum 30 tuiles

| Règle | Exigence |
|-------|----------|
| **Volume minimal** | **≥ 30 tuiles** relevées sur `/shop` |
| **Couverture obligatoire** | **100 % des 19 `validated_grid`** (liste A ci-dessous) |
| **Complément fallback** | **≥ 11 tuiles** supplémentaires parmi master / autres statuts (liste B) |
| **Méthode** | Parcourir `/shop` page par page · desktop ≥ 992px · hard refresh |
| **Critère unique par tuile** | Photo touche les bords de la zone image · **pas de bande beige inset** · pas d’effet « image dans l’image » |
| **Verdict global V1b** | **GO** si ≥ 30 tuiles OK ou réserve mineure · **KO** si ≥ 1 `validated_grid` en inset net · **KO** si > 10 % de l’échantillon en inset |

> Les produits **153** (Confiture banane flambée) et **9** (Pâtes de manioc Mayotte) servent de **repères visuels**, pas de périmètre suffisant à eux seuls.

### Diagnostic connu (ne pas confondre avec un KO CSS seul)

| Cause | Symptôme visuel | Correction Dev (`19.0.15.8.1`) |
|-------|-----------------|--------------------------------|
| Padding interne Odoo `design_grid` (`--o-wsale-card-padding`) | Marge beige entre le bord de la tuile et la photo | `--o-wsale-card-padding: 0` sur `.oe_product_cart` |
| Letterboxing bake-in JPEG v1.1 (~77 % de remplissage du carré) | Aplat beige **dans** l’image · effet cadre même avec `cover` | Zoom léger (`×1.29`) sur `.marketone-shop-tile-photo` uniquement |
| Fallback master (`image_1920`) | — | Pas de zoom · rendu cover standard |

> Doctrine image v2 **inchangée** : aucun retraitement de `image_shop_tile` dans cette correction.

### Critères MOA — contrôle technique (une fois par session)

| Étape | Vérification | Attendu | ☐ |
|-------|--------------|---------|---|
| 1 | DevTools — grille `#o_wsale_products_grid` | Classe `o_wsale_products_opt_thumb_cover` présente | |
| 2 | DevTools — tuile `validated_grid` (échantillon) | Wrapper `marketone-shop-tile-photo` sur le dérivé | |
| 3 | DevTools — tuile fallback master (échantillon) | Absence de `marketone-shop-tile-photo` | |
| 4 | DevTools — `.oe_product_cart` | `--o-wsale-card-padding: 0` effectif | |
| 5 | Survol carte (≥ 3 tuiles `validated_grid`) | Zoom hover `×1.02` conservé · pas de saut · pas de bande réapparue | |

### Liste A — 19 `validated_grid` (contrôle intégral obligatoire)

| ID | Produit | Photo pleine | Verdict ☐ OK · ☐ réserve · ☐ KO |
|----|---------|--------------|----------------------------------|
| 9 | Pâtes de manioc Mayotte | | |
| 153 | Confiture banane flambée | | |
| 155 | Shrub agrumes créole | | |
| 158 | Sauce piment cadji | | |
| 159 | Rougail épices Réunion | | |
| 160 | Chutney mangue verte | | |
| 164 | Miel créole baie rose | | |
| 177 | Coffret gourmand îles créoles | | |
| 178 | Palets manioc croustillants La Platine | | |
| 181 | Assortiment apéritif créole | | |
| 184 | Semoule manioc fine Mayotte | | |
| 186 | Trio sirops des Antilles | | |
| 187 | Marinade jerk authentique | | |
| 467 | Sauce scotch bonnet créole | | |
| 469 | Pochette curry des Antilles | | |
| 470 | Marinade jerk citron vert | | |
| 477 | Confiture christophine gingembre | | |
| 479 | Quatre épices créoles | | |
| 489 | Miel polyfloral créole | | |

### Liste B — complément fallback master (≥ 11 tuiles à relever)

Sélectionner **au moins 11 lignes** parmi :

| ID | Produit | Statut | Photo pleine | Verdict ☐ OK · ☐ réserve · ☐ KO |
|----|---------|--------|--------------|----------------------------------|
| 7 | Maniocookies salés La Platine | `validated_storage` | | |
| 8 | Crackers manioc Sainte-Anne | `validated_storage` | | |
| 188 | Coffret biscuits et douceurs | `validated_storage` | | |
| 474 | Crackers sarrasin Réunion | `validated_storage` | | |
| 154 | Colombo des Antilles | `pending_review` | | |
| 156 | Biscuits coco vanille | `pending_review` | | |
| 471 | Biscuits banane confiture | `pending_review` | | |
| 163 | Mix beignets manioc | `needs_review_source` | | |
| 179 | Mélange épices caraïbes | `needs_review_source` | | |
| 180 | Tartinade coco citron vert | `needs_review_source` | | |
| 183 | Chips banane plantain salées | `needs_review_source` | | |
| 185 | Confiture fruits de la passion | `needs_review_source` | | |
| 468 | Confiture goyave rose | `needs_review_source` | | |
| 472 | Palettes coco vanille | `needs_review_source` | | |
| 473 | Chips patate douce créole | `needs_review_source` | | |
| 475 | Sauce chien antillaise | `needs_review_source` | | |
| 476 | Tapenade agrumes confits | `needs_review_source` | | |
| 478 | Confiture papaye muscovado | `needs_review_source` | | |
| 480 | Poudre colombo créole | `needs_review_source` | | |
| 481 | Bouillon légumes des îles | `needs_review_source` | | |
| 482 | Rougail tomate créole | `needs_review_source` | | |
| 483 | Sirop jambosier | `needs_review_source` | | |
| 485 | Jus goyave passion | `needs_review_source` | | |
| 486 | Infusion bois bandé | `needs_review_source` | | |
| 157 | Sirop de canne vanille | `none` | | |
| 161 | Café arabica Antilles | `none` | | |
| 162 | Infusion vétiver citronnelle | `none` | | |
| 182 | Confiture ananas vanille | `none` | | |
| 484 | Sirop banane flambée | `none` | | |
| 487 | Farine banane plantain | `none` | | |
| 488 | Flocons manioc instantanés | `none` | | |

**Synthèse MOA V1b** — exécution 2026-05-20 :

```text
Tuiles relevées        : 50 / ≥ 30
validated_grid OK      : 19 / 19
fallback OK            : 31 / ≥ 11
Réserve(s)             : —
KO                     : —
Verdict global V1b     : ☑ GO · ☐ GO sous réserve · ☐ KO
```

### Référence visuelle — KO vs OK

```text
KO (inset)                         OK (photo pleine)
┌─────────────────────┐            ┌─────────────────────┐
│ ░░░░░░░░░░░░░░░░░░░ │            │█████████████████████│
│ ░░┌─────────────┐░░ │            │█████████████████████│
│ ░░│   photo     │░░ │            │███████ photo ███████│
│ ░░└─────────────┘░░ │            │█████████████████████│
│ ░░░░░░░░░░░░░░░░░░░ │            └─────────────────────┘
└─────────────────────┘
  marge beige visible              bords photo = zone image
```

### Cas limite — hors scope correction CSS

| ID | Produit | Note MOA |
|----|---------|----------|
| 9 | Pâtes de manioc Mayotte | Remplissage JPEG ~43 % · marges latérales possibles malgré zoom · candidat `needs_review_source` ou re-export normalizer |

Si une tuile présente encore un inset **après** `19.0.15.8.1` : noter l’**ID** dans la synthèse V1b · comparer avec le JPEG source · escalader vers pipeline normalizer (pas de patch CSS produit par produit).

---

## V2 — Ligne commerciale (point critique MOA)

| Étape | Vérification | Attendu | ☐ |
|-------|--------------|---------|---|
| 1 | Alignement | Deux pôles visibles : exploration (gauche) · décision prix (droite) | |
| 2 | Prix | **Non collé** au CTA · `justify-content: space-between` effectif | |
| 3 | Produit promo | Prix barré lisible à droite si applicable | |
| 4 | Titre court vs long | Ligne basse reste alignée · pas de chevauchement | |

**Référence visuelle** :

```text
Voir                                      12,50 €
```

---

## V3 — Panier au survol

| Étape | Vérification | Attendu | ☐ |
|-------|--------------|---------|---|
| 1 | État repos | Panier **invisible** dans le footer | |
| 2 | Survol desktop | Bouton panier visible sur zone photo | |
| 3 | Clic panier | Comportement Odoo standard (`shop_product_buttons`) | |
| 4 | Produits configurables | Pas de régression si variantes / quick add | |

---

## V4 — Mobile (≤ 768px)

| Étape | Vérification | Attendu | ☐ |
|-------|--------------|---------|---|
| 1 | Grille mobile | Cartes lisibles · pas de débordement | |
| 2 | Ligne `Voir` / prix | Deux pôles conservés ou empilage propre | |
| 3 | Titre | 2 lignes max · taille réduite acceptable | |
| 4 | Panier | Action accessible (survol ou tap selon device) | |
| 5 | Images | Pas de régression cover · pas de halo · **spot-check ≥ 8 tuiles** (dont 4 `validated_grid`) | |

---

## V5 — Cohérence doctrine image v2

| Étape | Vérification | Attendu | ☐ |
|-------|--------------|---------|---|
| 1 | Échantillon 19 `validated_grid` | Rendu homogène · conforme GO visuel post-promotion | |
| 2 | Échantillon fallback master | Pas de tuile dérivée affichée | |
| 3 | Fiche produit (clic carte) | Master standard · description disponible | |
| 4 | Comparaison avant/après conversion | **Pas de régression image** sur mêmes produits | |
| 5 | V1b — photo pleine | **≥ 30 tuiles** relevées · **19/19 `validated_grid`** · **≥ 11 fallback** · synthèse V1b complétée | |

Produits repère (au sein des listes A/B — **ne remplacent pas** le minimum 30) :

| ID | Produit | Statut | Rôle |
|----|---------|--------|------|
| 153 | Confiture banane flambée | `validated_grid` | Repère KO inset corrigé (lifestyle) |
| 9 | Pâtes de manioc Mayotte | `validated_grid` | Repère cas limite remplissage JPEG |
| 155 | Shrub agrumes créole | `validated_grid` | Repère tuile + ligne basse |
| 154 | Colombo des Antilles | `pending_review` | Repère fallback master · pas de zoom dérivé |
| 177 | Coffret gourmand îles créoles | `validated_grid` | Repère lifestyle tuile |

---

## V6 — Non-régression boutique

| Étape | Vérification | Attendu | ☐ |
|-------|--------------|---------|---|
| 1 | Sidebar catégories | Inchangée | |
| 2 | Chips filtres UX-1 | Inchangées | |
| 3 | Compteur produits | Inchangé | |
| 4 | Fiche produit | Hors scope · pas de tuile conversion | |
| 5 | `/shop/cart` | Panier page inchangé | |

---

## Tests automatisés

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone \
  --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_lot3 \
  --http-port=8072
```

Contrôles couverts par `test_shop_conversion_tile_structure` :

- présence `marketone-shop-card-title` · `marketone-shop-card-footer` · `marketone-shop-card-cta`
- CTA pointe vers `/shop/...` (fiche produit)
- wishlist overlay présent
- absence `oe_subdescription`
- `o_wsale_product_btn` conservé

Contrôles couverts par `test_shop_tile_photo_full_bleed_markup` :

- classe `o_wsale_products_opt_thumb_cover` sur la grille
- classe `marketone-shop-tile-photo` sur les tuiles dérivées

Suite complète (recommandée avant GO) :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone \
  --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_smoke,dorevia_marketone_lot2,dorevia_marketone_lot2_1,dorevia_marketone_lot3,dorevia_marketone_lot4,dorevia_marketone_lot5,dorevia_marketone_lot6_1_featured \
  --http-port=8072
```

Attendu : **`0 failed, 0 error(s)`**

---

## Rollback

| Niveau | Action | Effet |
|--------|--------|-------|
| **R0** | Désactiver vue `marketone_products_item_conversion` (BO → Vues) | Retour tuile Odoo standard · image doctrine conservée |
| **R1** | `marketone.shop_tile_enabled = False` | Grille sans tuile dérivée · master Odoo |
| **R2** | Revert commit conversion | Suppression QWeb + SCSS conversion |

> Rollback image / statuts : voir [`RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_V1_5_SHOP_TILE.md`](./RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_V1_5_SHOP_TILE.md)

---

## Historique MOA

| Date | Verdict | Note |
|------|---------|------|
| 2026-05-20 | GO visuel post-promotion `validated_grid` | [`RAPPORT_REVUE_VISUELLE_MOA_EXECUTION.md`](./RAPPORT_REVUE_VISUELLE_MOA_EXECUTION.md) |
| 2026-05-20 | NO GO conversion v1 | Panier retiré + régression image suspectée |
| 2026-05-20 | Correction Dev | Panier restauré (survol photo) · ligne `Voir` gauche / prix droite |
| 2026-05-20 | Correction Dev `19.0.15.8.1` | Photo pleine : padding carte à 0 · cover grille · zoom `.marketone-shop-tile-photo` (letterboxing v1.1) |
| 2026-05-20 | **GO technique — GO MOA proposable** | Recette exécutée · V1b 50/50 tuiles · 0 inset · Lot 3 (11) + suite Lots 1–6.1 (63) OK |
| 2026-05-20 | **GO MOA** | Panier au survol + popup au clic validés humainement — réserve levée |

---

## Références

| Document | Rôle |
|----------|------|
| [`DOCTRINE_IMAGE_V2.md`](../../cadrage/DOCTRINE_IMAGE_V2.md) | Doctrine image (inchangée) |
| [`RAPPORT_REVUE_VISUELLE_MOA_EXECUTION.md`](./RAPPORT_REVUE_VISUELLE_MOA_EXECUTION.md) | GO grille 19 tuiles |
| [`RAPPORT_RECETTE_SHOP_CONVERSION_TILE_20260520.md`](./RAPPORT_RECETTE_SHOP_CONVERSION_TILE_20260520.md) | Exécution recette conversion · V1–V6 + V1b |
| [`RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_V1_5_SHOP_TILE.md`](./RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_V1_5_SHOP_TILE.md) | Tuiles image / statuts |
| [`RECETTE_MANUELLE_SHOP_UX3_PRODUCT_CARDS.md`](../ux/RECETTE_MANUELLE_SHOP_UX3_PRODUCT_CARDS.md) | Jalon UX cartes (Palier A) |

---

## Signal Dev post-recette

```text
Recette manuelle tuile conversion — GO MOA 2026-05-20 — V1–V6 + V1b photo pleine — 50 tuiles · 0 inset — panier survol + popup clic OK — Lot 3 (11) · suite Lots 1–6.1 (63) OK — doctrine image v2 inchangée.
```

Captures : [`capture_recette_conversion_tile_desktop.png`](./capture_recette_conversion_tile_desktop.png) · [`capture_recette_conversion_tile_mobile_390.png`](./capture_recette_conversion_tile_mobile_390.png)
