# Ticket — Sidebar `/shop` : bloc **Catégories** toujours affiché

## Contexte technique

Sur la page produits `website_sale.products`, le flag QWeb `opt_wsale_categories` pilote :

- l’affichage du `div.products_categories` (desktop + offcanvas) ;
- indirectement `hasLeftColumn` avec `opt_wsale_attributes` (colonne gauche présente ou non).

En standard Odoo 19, la variable est définie ainsi :

```text
opt_wsale_categories = is_view_active('website_sale.products_categories')
```

La vue QWeb **`website_sale.products_categories`** (« **Categories in Left Side** ») est **`active="False"`** à l’installation. Tant qu’elle n’est pas activée via le site, **`opt_wsale_categories` est faux** : le bloc Catégories **n’est pas rendu**, même si des catégories e-commerce existent.

## Action BO (instance) — option native

À utiliser si vous **ne** forcez **pas** le fallback module (voir ci‑dessous) ou pour comprendre le réglage d’origine.

1. Connectez-vous au **site web** (frontend).
2. Ouvrez la page **Boutique** (`/shop`).
3. Cliquez sur **Modifier** (mode édition / Website Builder).
4. Ouvrez le panneau **Personnaliser** (Customize).
5. Activez l’option du type **« Categories in Left Side »** / **« Catégories sur le côté gauche »** (libellé selon langue / thème) — elle correspond à la vue `website_sale.products_categories`.

Vérification technique (mode développeur) : **Paramètres → Technique → Interface utilisateur → Vues**, rechercher `products_categories` (xml id `website_sale.products_categories`) : la case **Actif** doit être cochée.

## Fallback C-Kreyol (livré)

Le module **`dorevia_ckreyol_marketplace`** surcharge le `t-set` dans `views/ckr_shop_sidebar_rail_maquette.xml` (`ckr_shop_sidebar_rail_layout`) pour :

```text
opt_wsale_categories = True
```

Effet : le rail affiche **systématiquement** le bloc Catégories (accordéon + cases à cocher CK), conformément à la maquette à 4 blocs, **sans** dépendre de l’activation manuelle de la vue native.

- La **logique catalogue** (liste des racines `categories`, construction des liens, JS `ckr_shop_sidebar.js`) reste alignée sur le standard : en **Odoo 19 CE**, `product.public.category` **n’expose plus** `website_url` pour les gabarits QWeb — les `href` des lignes catégorie (desktop + offcanvas) suivent le patron natif **`website_sale.categorie_link`** : `keep('%s/category/%s' % (shop_path, slug(c)))` (**19.0.1.10.27**).
- **Offcanvas** : un héritage QWeb sur l’en-tête offcanvas « Catégories » a été **retiré** (**19.0.1.10.26**) car l’xpath pouvait être absent selon le thème et bloquer le `-u` du module ; la traduction / finition mobile repose sur le rendu natif + les mêmes gabarits que le desktop lorsque le bloc est présent.
- Si aucune **catégorie e-commerce** n’existe, la liste peut se limiter à « Toute la boutique » — comportement attendu côté données.

## Cas nominal démo (4 blocs garantis sur instance neuve)

1. **`show_price_filter`** — en standard : `opt_wsale_filter_price and opt_wsale_attributes`.  
   Depuis **19.0.1.10.52**, le rail aligne **`show_price_filter = opt_wsale_filter_price`** (`ckr_shop_sidebar_rail_maquette.xml`) : le bloc **Prix** n’apparaît que si la vue native **`website_sale.filter_products_price`** est active — sinon le gabarit natif peut provoquer une **HTTP 500** (`min_price` / `max_price` absents). Le module charge **`data/ckr_shop_filter_price_activation.xml`** pour activer cette vue à l’`-u`, et **`WebsiteSaleCKR._ckr_get_price_filter_shop_values`** complète les bornes catalogue si le contexte les omet.

2. **Données CK** — fichier `data/ckr_shop_sidebar_nominal_demo_data.xml` (chargé après les fiches vitrine Sélection) :
   - **Collection** « Collection Saint-Anne » (`slug` `saint-anne`) + produits Crêpes / Chips ;
   - **Origine** « Guadeloupe » (valeur d’attribut Origine + profil `ckr.shop.origin` publié).

Après **`-u dorevia_ckreyol_marketplace`** sur une base où ces xmlids n’existent pas encore, la sidebar `/shop` affiche **les quatre intitulés** (les lignes à cocher Catégories peuvent n’être que « Toute la boutique » si aucune catégorie e-commerce n’est créée — le bloc est toutefois présent).

## Critère d’acceptation

Sur **`/shop`** (desktop `≥ lg`), la sidebar montre clairement **dans l’ordre maquette** :

1. **Catégories** (accordéon + cases à cocher)  
2. **Collections**  
3. **Origines**  
4. **Prix**  

Recette : hard refresh, `-u dorevia_ckreyol_marketplace`, ouvrir `/shop` sur une instance de démo avec données ci-dessus chargées.

**Bloc Prix** : affiché seulement si **`opt_wsale_filter_price`** (vue active, **10.52**) ; **déplié par défaut** quand le bloc est rendu (comportement natif) ; libellés FR et classes maquette dans `ckr_shop_filter_price_fr` (**19.0.1.10.28**).

**Gel chantier (MOA)** : la sidebar est jugée **alignée recette visuelle** — pas d’ajustements structurels lourds tant que la recette (accordéons, cases à cocher, mobile/offcanvas, non-régression `/shop`, `/collections/...`, Origines) ne remonte pas d’écart ciblé.

---

## Backlog fonctionnel (hors périmètre gel visuel)

**Gel** : le **rendu** et la **composition** du rail (4 blocs, homogénéité, FR, mobile/offcanvas) sont **figés** pour l’instant.

**Report volontaire** — comportement **après** interaction avec les filtres (chantier **non** lancé à ce stade) :

- navigation URL / rechargement vs état local ;
- **état actif** des entrées (surbrillance, accordéon, fil d’Ariane) ;
- **cohérence des cases cochées** avec le contexte catalogue réel ;
- **combinaisons** et règles produit entre **Catégories** (facettes natif), **Collections** et **Origines** (navigation CK + portes), et **Prix** (fourchette natif) — y compris cas limites et messages visiteur.

Trace produit / recette : [SHOP_MAQUETTE_ECARTS.md — Décisions produit](SHOP_MAQUETTE_ECARTS.md) ; cadrage UX : [2_SHOP.md §4](2_SHOP.md).
