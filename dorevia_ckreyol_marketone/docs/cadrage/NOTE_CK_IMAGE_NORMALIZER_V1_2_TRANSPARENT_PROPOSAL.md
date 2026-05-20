# Note d'instruction — CK Image Normalizer V1.2 (packshots transparents)

| Champ | Valeur |
|-------|--------|
| **Type** | Note d'instruction technique — **pas d'implémentation** |
| **Demande MOA** | Évaluer la faisabilité d'une variante packshots transparents pour la grille `/shop` |
| **Statut amont** | **Historique — non retenu MOA** (2026-05-20 STOP alpha) · recette active `ck_shop_tile_v1.1` |
| **Auteur** | Dev (2026-05-20) |

---

## 1. Constat V1.5 (origine de la piste)

La recette `ck_shop_tile_v1.1` produit des JPEG **1024×1024** avec :

```text
background: #F8EEDB   (baked-in)
padding: 64–128 px    (variable selon visuel)
white_background_replace: true (packshots) / false (lifestyle)
format: JPEG (pas d'alpha)
```

Conséquences perçues MOA sur `/shop` :

1. Le fond `#F8EEDB` est **inscrit dans les pixels** ;
2. Quel que soit le fond CSS conteneur (`#FDFCFA`, `#FCFAF6`…), l'œil perçoit deux surfaces si elles ne sont pas identiques ;
3. Effet « image dans l'image » sur packshots avec faible padding ;
4. Bandes / cadrages internes sur lifestyle au ratio non carré.

**Limite Odoo-side** : aucun travail CSS ne peut éliminer un fond inscrit dans le JPEG sans rogner le produit lui-même.

---

## 2. Proposition V1.2 — variante transparente

### 2.1 Cible

```text
canvas_size: 1024×1024
background: TRANSPARENT (alpha channel)
padding: identique V1.1 (64–128 px)
format: PNG-24 ou WebP avec alpha
white_background_replace: true → fond effectif = alpha=0 (pas de couleur)
lifestyle: rester en JPEG (pas d'alpha utile)
```

### 2.2 Distinction packshot vs lifestyle

| Type | V1.1 actuel | V1.2 proposé |
|------|-------------|--------------|
| **Packshot** (fond uni source) | JPEG fond `#F8EEDB` | **PNG/WebP alpha=0** |
| **Lifestyle** (scène réelle) | JPEG fond `#F8EEDB` | JPEG identique V1.1 |

Détection auto : `white_background_replace: true` dans le `--recipe-type packshot`.

### 2.3 Comportement Odoo attendu

```text
image_shop_tile  → packshot transparent (alpha=0)
.oe_product_image fond CSS = $ck-bg-image-tile (#FDFCFA ou autre)
résultat visuel = produit posé sur conteneur, plus aucun "deuxième fond"
```

Plus besoin de masque CSS ni de zoom 1.32. Le rendu devient **strictement équivalent à une fiche produit Odoo standard sans fond baked-in**.

---

## 3. Faisabilité technique

### 3.1 Formats

| Format | Alpha | Poids relatif | Compatibilité |
|--------|-------|---------------|----------------|
| **PNG-24** | ✅ | ~2–3× JPEG | Universel (Odoo, navigateurs, mobile) |
| **WebP** | ✅ | ~JPEG | Universel >2023 (>97 % navigateurs) |
| **AVIF** | ✅ | <WebP | <90 % navigateurs (à éviter actuellement) |

**Recommandation** : WebP packshots / fallback PNG. Lifestyle reste JPEG.

### 3.2 Champ Odoo `image_shop_tile`

`fields.Image(attachment=True)` accepte tout binaire image. Odoo sert via `/web/image/...` avec conservation de l'alpha. **Aucune adaptation modèle requise.**

### 3.3 Pipeline CLI

Modifications nécessaires dans `tools/ck_image_normalizer/` :

| Fichier | Action |
|---------|--------|
| `recipes/ck_shop_tile_v1.2.yaml` | Nouvelle recette · `background: transparent` |
| `normalizer.py` (ou équivalent) | Branche `format=PNG/WebP` si `background=transparent` |
| Sortie | `output/png/` ou `output/webp/` (en plus de `output/jpeg/`) |
| Recette source dans manifest | `ck_shop_tile_v1.2` |

**Effort indicatif** : 2–4 j/h CLI · 0 j/h Odoo (pas de changement modèle ni vue).

---

## 4. Risques identifiés

| Risque | Mitigation |
|--------|------------|
| **Halos** sur détourage packshot (cheveux, fumée, fonds dégradés) | Pas de produits concernés dans le catalogue actuel (sachets, bouteilles, pots) · si futur produit complexe → NEEDS_REVIEW manuel |
| **Lisibilité** sur écran sombre (mode dark) | `/shop` Marketone est sur fond clair par doctrine ; pas de mode dark prévu |
| **Poids transport** (PNG ~2× JPEG) | Compenser par WebP packshots · ou conserver JPEG résolution réduite 768×768 |
| **Régression V1.1** | Lot pilote 43 conservé en `ck_shop_tile_v1.1` · V1.2 = nouveau ticket POC sur 5–10 SKU pilote |
| **Distinction packshot/lifestyle** | Déjà gérée par `white_background_replace` dans la recette ; mapping auto |
| **Cohabitation des deux** | `shop_tile_recipe_version` distingue déjà la source par enregistrement |

---

## 5. Comparaison visuelle attendue

| Aspect | V1.1 (baked `#F8EEDB`) | V1.5 + masque CSS (actuel) | **V1.2 (alpha)** |
|--------|-----------------------|----------------------------|------------------|
| Fond perçu | Beige `#F8EEDB` | Off-white `#FDFCFA` + frange baked | **Off-white `#FDFCFA` pur** |
| Effet « image dans l'image » | Présent | Atténué (masque 14 px + zoom 1.32) | **Absent** |
| Lifestyle ratio carré | Letterboxing baked | Letterboxing masqué | Idem V1.5 (pas d'alpha utile) |
| Lifestyle ratio non carré | Bandes `#F8EEDB` | Bandes masquées | Idem V1.5 |
| Risque rognage produit | Néant | Possible si scale > 1.35 | **Néant** |
| Cohérence fond `/shop` | Faible | Bonne | **Optimale** |

---

## 6. Décision attendue

| Option | Effort | Effet attendu |
|--------|--------|---------------|
| **A — Conserver V1.5 + masque actuel** | 0 j/h | Rendu actuel · frange beige résiduelle sur 3–5 % packshots à faible padding |
| **B — POC V1.2 packshots transparents** | 2–4 j/h CLI + 0 Odoo | Fond unifié `#FDFCFA` réel · packshots fusionnés conteneur |
| **C — Hybride** : V1.2 packshots / V1.1 lifestyle (option B avec scope packshots seuls) | 2–3 j/h CLI | Idem B sur packshots · lifestyle reste V1.1 (acceptable car bandes peu visibles) |

**Recommandation Dev** : **option C** — POC V1.2 sur 5–10 packshots, comparaison côte à côte avec lot pilote V1.1, décision MOA après revue visuelle.

---

## 7. Hors périmètre de cette note

- Tout changement du master `image_1920` (jamais touché)
- Tout changement du flag `marketone.shop_tile_enabled`
- Tout changement de la fiche produit, sidebar, hero, culture, éditorial
- Tout cron / traitement automatique
- Le lot X (toujours exclu)

**Cette note est strictement instructionnelle** — aucune implémentation tant que MOA n'a pas tranché entre options A / B / C.

---

## 8. Références

| Document | Rôle |
|----------|------|
| [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION.md`](../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION.md) | Ticket P7 en cours |
| [`NOTE_CK_IMAGE_NORMALIZER_SHOP_V1.md`](./NOTE_CK_IMAGE_NORMALIZER_SHOP_V1.md) | Cadrage initial V1 |
| `tools/ck_image_normalizer/recipes/ck_shop_tile_v1.1.yaml` | Recette actuelle baked |
| `docs/recette/boutique/capture_moa_v15_shop_tile_photo_v3_*.png` | Captures recette V1.5 actuelle |
