# Doctrine boutique — `/shop` conteneur unique

| Champ | Valeur |
|-------|--------|
| **Statut** | Doctrine front boutique à appliquer aux chips et à la sidebar |
| **Principe** | `/shop` est la seule grille boutique ; les actions UI affinent cette grille par query string |
| **Portée** | Page `/shop`, chips commerciaux, sidebar Catégories / Collections / Origines / Prix |

## Règle produit

Le visiteur ne doit pas avoir l’impression de quitter la boutique lorsqu’il utilise les chips ou la sidebar. Les chips et les facettes ne sont donc pas des pages de destination : ce sont des filtres appliqués à la grille `/shop`.

Forme canonique attendue :

```text
/shop + paramètres de filtre
```

Les anciennes routes d’entrée (`/promotions`, `/kits`, `/collections/<slug>`, etc.) peuvent rester comme compatibilité ou raccourci externe, mais elles doivent converger vers `/shop?...`. Elles ne sont pas le modèle de navigation à reproduire dans les chips ou la sidebar.

## Chips commerciaux

Les chips attendus sont :

- `Tout`
- `Promotions`
- `Incontournables`
- `Kits / Packs`

Contrat :

- `Tout` pointe vers `/shop` sans query et retire tous les filtres actifs.
- `Promotions` ajoute `ckr_mode=promo`.
- `Incontournables` ajoute `ckr_mode=featured`.
- `Kits / Packs` ajoute `ckr_mode=pack`.
- Un chip commercial actif se combine en **ET** avec les facettes sidebar.
- Les chips ne doivent pas pointer vers `/promotions`, `/incontournables`, `/kits` ou une autre page.

## Sidebar

La sidebar contient quatre groupes :

- Catégories
- Collections
- Origines
- Prix

Les groupes Catégories, Collections et Origines portent une case `Toutes`.

Contrat `Toutes` :

- `Toutes` est cochée par défaut.
- `Toutes` signifie : aucune restriction pour ce groupe.
- `Toutes` n’est pas une catégorie, pas une collection, pas une origine.
- Si une valeur spécifique est cochée, `Toutes` se décoche.
- Plusieurs valeurs spécifiques peuvent rester cochées dans le même groupe.
- Si la dernière valeur spécifique est décochée, `Toutes` redevient cochée.
- Si l’utilisateur clique `Toutes`, les valeurs spécifiques du groupe sont décochées.

## Sémantique des filtres

Dans un même groupe, la logique est **OU** :

```text
ckr_category=biscuits&ckr_category=boissons
= Biscuits OU Boissons
```

Entre les groupes, la logique est **ET** :

```text
ckr_mode=promo
ET ckr_category=biscuits OU boissons
ET ckr_origin=guadeloupe OU martinique
ET ckr_collection=saint-anne OU decouverte
```

## Paramètres publics

| Groupe | Paramètre | Répétable | Sens |
|--------|-----------|-----------|------|
| Chips commerciaux | `ckr_mode` | Oui techniquement, un seul émis par l’UI | `promo`, `featured`, `pack` |
| Catégories | `ckr_category` | Oui | Slug `product.public.category` |
| Collections | `ckr_collection` | Oui | Slug `ckr.shop.collection` |
| Origines | `ckr_origin` | Oui | Slug `ckr.shop.origin` |
| Prix | `min_price`, `max_price` | Non | Bornes du filtre prix natif |

Exemples attendus :

```text
/shop?ckr_category=biscuits&ckr_category=boissons
/shop?ckr_origin=guadeloupe&ckr_origin=martinique
/shop?ckr_collection=saint-anne&ckr_collection=decouverte
/shop?ckr_mode=promo&ckr_category=biscuits&ckr_category=boissons&ckr_origin=guadeloupe&ckr_collection=saint-anne
```

## Points d’implémentation

| Zone | Fichiers | Contrat |
|------|----------|---------|
| Domaine produit | `controllers/website_sale_ckr.py`, `models/product_template.py` | Lire les paramètres répétables avec `request.httprequest.args.getlist`; appliquer OU intra-groupe et ET inter-groupes |
| Chips | `views/pages/ckr_shop.xml` | Générer des `href` sous `/shop`, préserver les facettes existantes pour les chips commerciaux, reset global pour `Tout` |
| Sidebar | `views/pages/ckr_shop.xml`, `views/ckr_shop_sidebar_rail_maquette.xml` | Rendre des checkboxes, pas des liens de navigation |
| Comportement client | `static/src/js/ckr_shop_sidebar.js` | Gérer `Toutes`, multi-sélection, suppression du groupe, et redirection vers `/shop?...` |
| Canonical / pagination | `models/website.py`, hooks `WebsiteSale` | Réémettre les paramètres CK utiles sans transformer les facettes en routes |
| Tests | `tests/test_ckr_shop_container_contract.py` | Verrouiller `/shop` conteneur unique, multi-paramètres, reset, canonical, et absence de routes parallèles dans les facettes |

## Compatibilité legacy

Les routes historiques ou externes peuvent rester disponibles si elles redirigent vers `/shop` :

- `/promotions` → `/shop?ckr_mode=promo`
- `/kits` → `/shop?ckr_mode=pack`
- `/incontournables` → `/shop?ckr_mode=featured`
- `/collections/<slug>` → `/shop?ckr_collection=<slug>`
- `/shop/category/<slug>` → `/shop?ckr_category=<slug>`

Elles ne doivent pas être réintroduites comme destinations de la sidebar ou des chips.

## Critères d’acceptation

- Les chips affichés sont `Tout`, `Promotions`, `Incontournables`, `Kits / Packs`.
- Le chip `Tout` pointe vers `/shop` sans query.
- Les chips commerciaux restent sous `/shop?...`.
- La sidebar ne contient pas de `href` vers `/shop/category/...`, `/collections`, `/origines`, `/promotions` ou `/kits` dans les facettes CK.
- Les cases `Toutes` sont cochées par défaut.
- Cocher une valeur spécifique ne remplace pas les valeurs déjà cochées du même groupe.
- Les paramètres `ckr_category`, `ckr_collection`, `ckr_origin` sont répétables.
- Une combinaison complète chip + catégories + collections + origines reste en HTTP 200 sous `/shop`.
- Le canonical conserve les filtres utiles sous `/shop?...`.
