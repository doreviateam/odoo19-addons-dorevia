# Retour d'expert — Recadrage « odoo-iste » CK Marketone

| Champ | Valeur |
|-------|--------|
| **Module** | `dorevia_ckreyol_marketone` |
| **Version analysée** | `19.0.15.14.1` |
| **Date** | 2026-06-08 |
| **Référence MOA** | [`README.md`](./README.md) |
| **Statut** | Analyse code + écarts — **sans implémentation** |

---

## Synthèse

Le module est **techniquement solide et bien testé** (~20 fichiers de tests, héritages QWeb sur `website_sale`). Il **s'appuie réellement sur le moteur Odoo** pour le catalogue, le panier et le checkout.

En revanche, le **back-office produit** et une partie de la **couche image** donnent encore l'impression d'un **système e-commerce parallèle** — exactement ce que le recadrage MOA veut corriger. Le travail de recadrage **n'a pas encore été engagé dans le code** : le README cadrage2 est une directive, pas une livraison.

**Verdict global** : le front boutique est bien porté par `website_sale` ; le problème principal est **UX back-office et sémantique** (fiche produit, champs techniques visibles). Le premier livrable concret devrait être **uniquement BO** — sans toucher au front, déjà fonctionnel et couvert par les tests.

---

## 1. Alignement avec la cible « site Odoo standard »

| Brique cadrage2 | État actuel | Commentaire |
|-----------------|-------------|-------------|
| **Website** | ✅ `depends: website` | Layout, header, footer custom mais sur le socle natif |
| **eCommerce** | ✅ `website_sale` + `website_sale_wishlist` | Moteur catalogue / panier / checkout natif, étendu proprement |
| **Blog** | ❌ absent | **Tension documentaire** : cadrage2 le cite, mais les ADR Culture / Savoirs l'excluent volontairement |
| **Forum** | ❌ absent | Idem — interdit explicitement pour Savoirs v1 |
| **Catégories eCommerce** | ✅ `product.public.category` | Sidebar, portes, facettes — bon choix |
| **Attributs / variantes** | ✅ attribut « Origines » (`no_variant`) | Standard Odoo, enrichi par `marketone.shop.origin` |
| **Images produits** | ⚠️ double système | `image_1920` (master) + `image_shop_tile` (dérivé grille) |
| **Publication site** | ✅ `website_published` | Utilisé partout (collections, origines, produits) |

### Dépendances actuelles (`__manifest__.py`)

```python
"depends": [
    "portal",
    "website",
    "website_sale",
    "website_sale_wishlist",
],
```

Pas de `website_blog` ni `website_forum`. Cohérent avec [`cadrage/DECISIONS.md`](../cadrage/DECISIONS.md) et les tickets Culture / Savoirs, mais **à arbitrer** avec le cadrage2.

---

## 2. Ce qui est bien fait (à conserver)

### 2.1 Extension native du catalogue Odoo 19

Le contrôleur étend `WebsiteSale` et injecte les filtres via `_search_get_detail` — bonne pratique Odoo 19, pas un moteur parallèle.

Fichier : `models/product_template.py` — extension `_search_get_detail` pour portes featured, origines, catégories principales.

Fichier : `models/product_template_shop_collection.py` — facette collections via le même mécanisme.

### 2.2 Modèles métier bien calibrés

| Modèle | Rôle | Appréciation |
|--------|------|--------------|
| `marketone.shop.collection` | Merchandising éditorial (ADR-030) | Contraintes propres, menu sous Configuration Website — lisible |
| `marketone.shop.origin` | Surcouche éditoriale sur `product.attribute.value` | Pas un doublon de catalogue |
| `product.attribute` « Origines » | Filtrage / fiche produit | `create_variant=no_variant` — conforme au standard |

### 2.3 Front = héritages QWeb, pas un front externe

Les templates héritent de `website_sale.products`, `products_item`, `product`, etc. Le JS utilise le pattern Odoo 19 `interactions/`. Panier, wishlist et checkout restent natifs.

Exemple : `views/pages/shop.xml` hérite de `website_sale.products` avec renforts CSS (cover mode, sidebar catégories).

### 2.4 Qualité d'ingénierie

- ~20 suites de tests (`tests/test_marketone_*.py`) : sidebar, tuiles, wishlist, portes, culture, régressions.
- Feature flag `marketone.shop_tile_enabled` pour basculer le dérivé image.
- Doctrine image v2 documentée et implémentée — seul `validated_grid` active l'affichage grille.
- Droits d'accès propres (`security/ir.model.access.csv` : designer vs user).

---

## 3. Écarts par rapport au recadrage cadrage2

### 3.1 Fiche produit — point le plus critique

Le bloc « Tuile commerce /shop » est **collé à `image_1920`** dans la vue formulaire standard.

Fichier : `views/product_template_shop_tile_views.xml`

```xml
<group string="Tuile commerce /shop" name="marketone_shop_tile_group">
    <field name="image_shop_tile" widget="image"/>
    <field name="shop_tile_status"/>
    <field name="shop_tile_recipe_version"/>
    <field name="shop_tile_processed_at"/>
    <field name="shop_tile_source_run"/>
    <field name="shop_tile_moa_note"/>
</group>
```

Pour un utilisateur BO, cela ressemble à **deux images produit + une chaîne de production batch** — exactement l'effet que le cadrage2 veut éviter.

Les champs `shop_tile_recipe_version` et `shop_tile_source_run` portent explicitement la sémantique **CLI / pipeline externe** (`models/product_template_shop_tile.py`).

### 3.2 Classification des champs spécifiques CK

Proposition conforme au travail attendu du README cadrage2 (supprimer / masquer / conserver-renommer).

| Champ / bloc | Catégorie | Recommandation |
|--------------|-----------|----------------|
| `image_1920` | Standard Odoo | Inchangé — master |
| `image_shop_tile` | **Masquer technique** | Onglet « Qualité image / contenu », groupe réservé profils média |
| `shop_tile_status` | **Masquer technique** | Renommer « Statut média grille » ; visible groupe technique |
| `shop_tile_recipe_version` | **Masquer technique** | Onglet technique / debug uniquement |
| `shop_tile_processed_at` | **Masquer technique** | Idem |
| `shop_tile_source_run` | **Masquer technique** | Idem |
| `shop_tile_moa_note` | **Conserver, renommer** | « Note qualité visuelle » — langage métier MOA |
| `marketone_collection_ids` | **Conserver** | Regrouper dans onglet « Catalogue CK » |
| Attribut « Origines » + `marketone.shop.origin` | **Conserver** | Standard Odoo + enrichissement éditorial légitime |
| `public_categ_ids` | Standard Odoo | Inchangé |
| Param `marketone.shop_tile_enabled` | **Masquer technique** | Reste en `ir.config_parameter`, pas en fiche produit |

**À ne pas supprimer** (pour l'instant) : `image_shop_tile` et sa logique — la [doctrine image v2](../cadrage/DOCTRINE_IMAGE_V2.md) est saine (master intact, dérivé contrôlé, fallback `image_1920`). C'est la **présentation BO** qu'il faut recadrer, pas le modèle de données.

### 3.3 Back-office non structuré

Aujourd'hui, les extensions produit sont **éparpillées** :

| Extension | Emplacement actuel | Fichier |
|-----------|-------------------|---------|
| Tuile image | Après `image_1920` | `views/product_template_shop_tile_views.xml` |
| Collections | Après `public_categ_ids` | `views/marketone_shop_collection_views.xml` |

Le cadrage2 propose des onglets dédiés — **non implémentés** :

- **Publication site** : `website_published`, `public_categ_ids`, séquence site…
- **Catalogue CK** : collections, origines
- **Qualité image / contenu** : dérivé grille, statut, note MOA
- **Technique** : recette, run batch, traces debug (groupe `base.group_no_one`)

### 3.4 Complexité front encore en croissance

Le contrôleur `controllers/website_sale.py` fait **~1000 lignes** (portes, facettes, canonicalisation URL, chips filtres, preview in-place UX-4…).

Ce n'est pas un anti-pattern en soi, mais cela contredit la consigne du README cadrage2 : *« Ne plus ajouter de logique front spécifique tant que l'intégration standard Odoo Website/eCommerce/Blog/Forum n'a pas été posée et testée. »*

Les derniers lots (UX-4 preview, CTA tuile, wishlist custom) ajoutent de la logique front spécifique au-dessus d'un socle déjà riche.

### 3.5 Catégories principales — résolution fragile

Fichier : `models/marketone_shop_category.py`

Liste hardcodée `MARKETONE_PRIMARY_PUBLIC_CATEGORY_NAMES` (Biscuits salés, Épices, etc.) avec repli sur `ir.config_parameter`.

Fonctionnel mais **pas odoo-iste** à long terme. Piste : champ booléen ou séquence sur `product.public.category`, ou écran de configuration BO dédié.

---

## 4. Tension Blog / Forum : cadrage2 vs ADR existantes

Le cadrage2 liste Blog et Forum comme modules à vérifier. Or la doctrine actuelle dit explicitement :

- **Culture v1/v2** : pas de blog (pages légères custom — `controllers/culture.py`).
- **Savoirs v1** : modèle `marketone.savoir.recipe`, **pas** `website_blog`, **pas** de forum.

Références : [`cadrage/DECISIONS.md`](../cadrage/DECISIONS.md), tickets Culture et Savoirs.

### Options d'arbitrage MOA

| Option | Pour | Contre |
|--------|------|--------|
| **A — Maintenir l'exclusion** | Cohérence univers Boutique / Culture / Savoirs, BO simple | Écart avec cadrage2 littéral |
| **B — Blog pour Culture uniquement** | Natif Odoo, SEO, workflow rédactionnel | Refonte Culture, risque « blog-like » déjà refusé en recette |
| **C — Forum plus tard pour Savoirs** | Communauté | Complexité modération, hors socle |

**Avis intégrateur** : Option A reste la plus saine pour CK, à condition de **mettre à jour le README cadrage2** pour refléter cette décision plutôt que de réintroduire Blog/Forum par défaut.

---

## 5. Bilan technique

| Dimension | Appréciation | Commentaire |
|-----------|--------------|-------------|
| Architecture e-commerce | ⭐⭐⭐⭐ | `website_sale` bien utilisé, pas de moteur parallèle |
| Back-office produit | ⭐⭐ | Champs techniques visibles, pas d'onglets structurés |
| Maintenabilité code | ⭐⭐⭐ | Bonne doc + tests, contrôleur en croissance |
| Conformité cadrage2 | ⭐⭐ | Directive non traduite en code |
| Image / média | ⭐⭐⭐⭐ | Doctrine v2 solide, présentation BO à revoir |
| Dette front custom | ⭐⭐⭐ | Acceptable si gelée le temps du recadrage BO |

---

## 6. Plan d'action recommandé

### Phase 0 — Gel fonctionnel (immédiat)

- **Stop** aux nouveaux lots UX front (preview in-place, tuile CTA, etc.) tant que le BO n'est pas recadré — conformément au README cadrage2.

### Phase 1 — Back-office produit (1–2 jours dev)

1. Créer un notebook sur `product.template` :
   - **Publication site** : champs standard Odoo eCommerce
   - **Catalogue CK** : `marketone_collection_ids`, lien attribut Origines
   - **Qualité image** : `image_shop_tile`, `shop_tile_status`, `shop_tile_moa_note`
   - **Technique** (`base.group_no_one`) : recette, run CLI, dates batch
2. Retirer le groupe « Tuile commerce /shop » de la zone image principale.
3. Renommer les labels en langage métier (supprimer « CLI », « /shop », « tuile » côté utilisateur).

### Phase 2 — Stabilisation catalogue (2–3 jours)

1. Remplacer la liste hardcodée de catégories par un marquage BO sur `product.public.category`.
2. Documenter formellement la classification des champs (table §3.2 validée MOA).
3. Arbitrage MOA Blog/Forum → mise à jour cadrage2 + ADR.

### Phase 3 — Rationalisation front (ultérieur)

1. Découper `controllers/website_sale.py` en mixins ou sous-modules thématiques.
2. Évaluer si certaines facettes peuvent repasser sur les **filtres attributs natifs** Odoo.

### Phase 4 — Blog / Savoirs (selon arbitrage MOA)

- Si Savoirs v1 est relancé : modèle dédié (déjà cadré), pas `website_blog`.
- Si Culture passe au blog : migration `/culture/<slug>` → `website.blog.post` — **refonte**, pas un simple ajout de dépendance.

---

## 7. Inventaire des champs et modèles CK (référence)

### Modèles dédiés Marketone

| Modèle | Fichier | Rôle front |
|--------|---------|------------|
| `marketone.shop.collection` | `models/marketone_shop_collection.py` | Facette sidebar, merchandising |
| `marketone.shop.origin` | `models/marketone_shop_origin.py` | Porte origines, pages Culture |
| — | `models/marketone_shop_category.py` | Extension `product.public.category` |

### Champs `product.template` spécifiques CK

| Champ | Fichier | Usage front |
|-------|---------|-------------|
| `image_shop_tile` | `models/product_template_shop_tile.py` | Grille `/shop` si `validated_grid` + flag |
| `shop_tile_*` (5 champs) | idem | Gouvernance média / batch |
| `marketone_collection_ids` | `models/product_template_collection.py` | Filtre collections sidebar |

### Paramètres système

| Clé | Rôle |
|-----|------|
| `marketone.shop_tile_enabled` | Active l'affichage dérivé grille |
| `dorevia_ckreyol_marketone.primary_public_category_ids` | IDs catégories sidebar (option stable) |
| `dorevia_ckreyol_marketone.featured_public_category_id` | Porte Incontournables |

---

## 8. Conclusion

Le module **n'est pas un front externe déguisé** : c'est une extension Odoo 19 sérieuse, bien testée, avec une vraie doctrine produit. Le problème n'est **pas architectural au niveau e-commerce** ; il est **UX back-office et sémantique**.

Le recadrage cadrage2 est **pertinent et opportun** maintenant (socle boutique stabilisé, lots 1–6 livrés). Le premier livrable concret devrait être **uniquement BO** : restructurer la fiche produit et masquer le technique — **sans toucher au front**.

---

## Documents liés

| Document | Rôle |
|----------|------|
| [`README.md`](./README.md) | Directive MOA recadrage |
| [`../cadrage/ARCHITECTURE.md`](../cadrage/ARCHITECTURE.md) | Architecture cible |
| [`../cadrage/DOCTRINE_IMAGE_V2.md`](../cadrage/DOCTRINE_IMAGE_V2.md) | Deux images, trois décisions |
| [`../cadrage/DECISIONS.md`](../cadrage/DECISIONS.md) | ADR (collections, culture, savoirs) |
| [`../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md) | Invariants anti-régression `/shop` |
