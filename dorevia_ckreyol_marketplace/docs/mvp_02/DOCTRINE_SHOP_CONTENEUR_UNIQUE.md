# Doctrine de la page `/shop` — C-Kreyol

| Champ | Valeur |
|-------|--------|
| **Statut** | Référence produit et implémentation boutique (chips, sidebar, hero) |
| **Principe** | `/shop` est le **catalogue unique** ; chips et facettes affinent la grille par query string |
| **Portée** | Page `/shop`, chips commerciaux, sidebar Catégories / Collections / Origines / Prix |

---

## 1. Catalogue unique

La page `/shop` est le **catalogue unique** de la boutique C-Kreyol.

Elle concentre l’exposition produit, les portes d’entrée commerciales, les filtres, le tri, le compteur produits et la grille produit. L’utilisateur ne doit pas avoir l’impression de changer de monde lorsqu’il filtre ou affine sa sélection.

La page `/shop` reste le socle de navigation produit.

Les chips, la sidebar et les filtres doivent agir sur le catalogue courant, sans basculer automatiquement vers des pages métier autonomes.

Comportement attendu :

```text
/shop?ckr_collection=saint-anne
```

et non :

```text
/collections/saint-anne
```

Les pages éditoriales ou dédiées peuvent exister ailleurs, mais elles ne doivent pas être déclenchées par les filtres sidebar de la boutique.

Forme canonique générale :

```text
/shop + paramètres de filtre
```

Les anciennes routes d’entrée (`/promotions`, `/kits`, `/collections/<slug>`, etc.) peuvent rester comme compatibilité ou raccourci externe, mais elles doivent converger vers `/shop?...`. Ce ne sont pas le modèle de navigation à reproduire dans les chips ou la sidebar.

---

## 2. Rôle des chips

Les chips sont des **portes d’entrée rapides** dans le catalogue.

Elles permettent de poser une intention de navigation :

* Toute la sélection ;
* Promotions ;
* Incontournables ;
* Kits / Packs ;
* autres entrées commerciales prévues.

Une chip ne doit pas sortir de `/shop`. Elle doit appliquer un contexte catalogue.

Contrat :

* **Toute la sélection** : `/shop` sans query (réinitialisation des filtres actifs lorsque le produit prévoit un reset global).
* **Promotions** : ajoute typiquement `ckr_mode=promo`.
* **Incontournables** : `ckr_mode=featured`.
* **Kits / Packs** : `ckr_mode=pack`.

Un chip commercial actif se combine en **ET** avec les facettes sidebar.

---

## 3. Rôle de la sidebar

La sidebar sert à **affiner le catalogue**, pas à naviguer vers une autre page.

Elle applique des filtres dans le cadre courant de `/shop` :

* Catégories ;
* Collections ;
* Origines ;
* Prix ;
* autres facettes éventuelles.

Lorsqu’un utilisateur sélectionne une valeur dans la sidebar, il doit rester dans le même cadre catalogue : même page boutique, même structure, même logique de tri, même compteur produits, même grille.

Chaque groupe **Catégories**, **Collections** et **Origines** propose une option **« Toutes »**.

Contrat `Toutes` (comportement logique attendu côté produit et UI mutualiste) :

* **« Toutes »** représente l’absence de restriction pour ce groupe (aucun slug actif dans ce groupe).
* **« Toutes »** n’est pas une catégorie, une collection ni une origine.
* Si au moins une valeur spécifique est cochée, **« Toutes »** n’est pas l’état actif pour ce groupe.
* Plusieurs valeurs spécifiques peuvent être cochées dans le même groupe (**OU** intra-groupe).
* Entre les groupes, la logique est **ET**.

---

## 4. Comportement des blocs sidebar (accordéons)

Chaque bloc de filtre contient une option **« Toutes »**.

Règle générale :

* si **« Toutes »** est sélectionné dans un bloc, ce bloc peut être **replié** par défaut ;
* si une **valeur spécifique** est sélectionnée dans un bloc, ce bloc doit être **déplié** par défaut ;
* cette règle s’applique **indépendamment** à chaque bloc.

Exemples :

* Catégories = Toutes → bloc Catégories replié ;
* Collections = Collection Saint-Anne → bloc Collections déplié ;
* Origines = Guadeloupe → bloc Origines déplié.

---

## 5. Cas particulier du bloc Prix

Le bloc **Prix** est un filtre **transversal**.

Il doit être **toujours déplié par défaut**, même lorsqu’aucun filtre prix n’est actif.

Objectif : permettre à l’utilisateur d’ajuster rapidement son budget sans devoir ouvrir un panneau supplémentaire.

Bornes natives du filtre : `min_price`, `max_price`.

---

## 6. Hero et contexte visuel

Le hero de la boutique doit rester dans la logique **`/shop`**.

Il peut éventuellement être contextualisé selon l’entrée commerciale ou le filtre actif, mais il ne doit pas créer l’impression d’une page autonome de type « Collection Saint-Anne ».

Le contexte doit **enrichir** la boutique, pas **remplacer** la boutique.

---

## 7. Principe directeur

Les chips ouvrent une **intention** de navigation.  
La sidebar **affine** cette intention.  
La page **`/shop`** reste le **cadre unique** du catalogue.

---

## Annexes — Sémantique et paramètres

### Combinaisons de filtres

Dans un même groupe (**OU**) :

```text
ckr_category=biscuits&ckr_category=boissons
→ Biscuits OU Boissons
```

Entre les groupes (**ET**) :

```text
ckr_mode=promo
ET ckr_category=biscuits OU boissons
ET ckr_origin=guadeloupe OU martinique
ET ckr_collection=saint-anne OU decouverte
```

### Paramètres publics typiques

| Groupe | Paramètre | Répétable | Sens |
|--------|-----------|-----------|------|
| Chips commerciaux | `ckr_mode` | Un seul actif dans l’UI produit selon grille | `promo`, `featured`, `pack` |
| Catégories | `ckr_category` | Oui | Slug `product.public.category` |
| Collections | `ckr_collection` | Oui | Slug `ckr.shop.collection` |
| Origines | `ckr_origin` | Oui | Slug `ckr.shop.origin` |
| Prix | `min_price`, `max_price` | Non | Bornes du filtre prix natif |

Exemples :

```text
/shop?ckr_category=biscuits&ckr_category=boissons
/shop?ckr_origin=guadeloupe&ckr_origin=martinique
/shop?ckr_collection=saint-anne&ckr_collection=decouverte
/shop?ckr_mode=promo&ckr_category=biscuits&ckr_category=boissons&ckr_origin=guadeloupe&ckr_collection=saint-anne
```

---

## Annexes — Points d’implémentation

| Zone | Fichiers | Contrat |
|------|----------|---------|
| Domaine produit | `controllers/website_sale_ckr.py`, `models/product_template.py` | Lire les paramètres répétables avec `request.httprequest.args.getlist`; appliquer OU intra-groupe et ET inter-groupes |
| Chips | `views/pages/ckr_shop.xml` | Générer des `href` sous `/shop`, préserver les facettes existantes pour les chips commerciaux, reset global pour « Toute la sélection » |
| Sidebar | `views/pages/ckr_shop.xml`, `views/ckr_shop_sidebar_rail_maquette.xml` | Rendre des cases à cocher (pas une navigation hors `/shop`), état accordéon par groupe |
| Comportement client | `static/src/js/ckr_shop_sidebar.js` | `Toutes`, multi-sélection, redirection canonique sous `/shop?...` |
| Canonical / pagination | `models/website.py`, hooks `WebsiteSale` | Réémettre les paramètres CK utiles sans transformer les facettes en routes hors `/shop` |
| Tests | `tests/test_ckr_shop_container_contract.py`, `tests/test_ckr_shop_wave1.py` | Tags `dorevia_ckr_shop` — conteneur unique, canonical, absence de routes parallèles dans les facettes |

---

## Compatibilité legacy

Les routes historiques peuvent rester disponibles si elles **redirigent** vers `/shop` :

| Entrée | Cible indicative |
|--------|-------------------|
| `/promotions` | `/shop?ckr_mode=promo` |
| `/kits` | `/shop?ckr_mode=pack` |
| `/incontournables` | `/shop?ckr_mode=featured` |
| `/collections/<slug>` | `/shop?ckr_collection=<slug>` |
| `/shop/category/<slug>` | `/shop?ckr_category=<slug>` |

Elles ne doivent pas être réintroduites comme destinations des facettes sidebar ou des chips.

---

## Critères d’acceptation synthétiques

* Les entrées chips commerciales restent sous `/shop?…` (pas de pages « stub » depuis la barre courte).
* La sidebar applique uniquement la query sous `/shop` ; pas de liens métier hors catalogue pour affiner une facette CK.
* Multi-sélection par groupe ; `« Toutes »` cohérente avec l’état neutre du groupe.
* Bloc Prix **toujours** visible ouvert par défaut (transversalité).
* Hero cohérent avec le cadre unique boutique (pas d’illusion de page colonne séparée pour un simple filtre sidebar).
* Les tests automatiques étiquetés `--test-tags=dorevia_ckr_shop` vérifient le contrat canonique lorsqu’ils sont exécutés sur une base avec données recette compatibles.
