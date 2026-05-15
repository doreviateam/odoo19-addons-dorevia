# MVP2.2 — Boutique

**Statut du document** : **cible UX / structure de page** pour une vague **MVP2.2** (densité retail, lisibilité, contextualisation par porte).  
**Complément technique obligatoire** : portes catalogue, URLs et priorités sont **déjà figées** dans **[SPEC_SHOP_PORTES.md](../mvp_01/SPEC_SHOP_PORTES.md)** et les **ADR** [ADR-CKR-007](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007), [ADR-CKR-008](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008), [ADR-CKR-001](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-001). **Lexique métier pack / kit** (homogène vs hétérogène, copy et titres produits) : **[DOCTRINE_CK_PACK_VS_KIT.md](../direction/DOCTRINE_CK_PACK_VS_KIT.md)**.

> Toute évolution qui **touche aux URL**, au **domaine produit** ou à un **nouveau `ckr_mode`** dépasse le seul design : elle exige **mise à jour des contrats `mvp_01`** + recette.

**Validation MOA (langage public / technique)** : le libellé visiteur **ne suggère pas** un classement statistique fictif ; le nom technique **`featured`** est **neutre** (« mis en avant »). **Interdits** sans calcul réel sur ventes confirmées : `best_sellers`, `top_sales`.

**Gel fonctionnel MOA (2026-04-28)** : la page **`/shop` par défaut** est validée et gelée fonctionnellement. Hors demande MOA explicite, le périmètre d’intervention est limité au **bugfix** et à la **prévention de régression**. Référence opposable : [DOCTRINE_SHOP_CONTENEUR_UNIQUE.md](DOCTRINE_SHOP_CONTENEUR_UNIQUE.md) (§0).

**Amendement doctrine front — conteneur unique** : pour la navigation boutique courante, **`/shop` est le conteneur unique**. Les chips du haut sont des **filtres commerciaux** (`ckr_mode=promo|featured|pack`) et la sidebar est une **facette multi-checkbox** (`ckr_category`, `ckr_collection`, `ckr_origin`, prix). Les routes historiques ou externes peuvent rester des entrées de compatibilité, mais les chips et la sidebar ne doivent pas envoyer vers des pages parallèles. Référence exécutable : [DOCTRINE_SHOP_CONTENEUR_UNIQUE.md](DOCTRINE_SHOP_CONTENEUR_UNIQUE.md).

---

## 0. Écart « livré V1 module » vs « cible MVP2.2 » (analyse)

| Sujet | Livré aujourd’hui (repères) | Cible MVP2.2 (ce document) |
|--------|------------------------------|----------------------------|
| **Bandeau contextuel** | Bandeaux **texte** (titre + intro) par porte `ckr_mode` pack / promo / origin + bandeau collections ; **pas** d’image de fond obligatoire — `views/pages/ckr_shop.xml`, styles associés | **Hero** pleine largeur avec **fond image** + overlay, copy premium |
| **Layout filtres** | Rail **19.0.1.10.18+** ; filtre **Prix** : `show_price_filter = opt_wsale_filter_price` + activation data / recalcul contrôleur (**§4**, **19.0.1.10.52+**) ; fallback **`opt_wsale_categories`** dans `ckr_shop_sidebar_rail_maquette.xml` ; `ckr_shop.xml` + `_shop.scss` ; liens catégorie sans `website_url` (**10.27**) | Sidebar **gauche**, **4 blocs** maquette en **accordéons** ; **ouverture par porte** pour les blocs concernés ([§4](2_SHOP.md)) = cible E2 ; **Prix** déplié par défaut quand le bloc est affiché (**10.28**) |
| **Raccourcis commerciaux** | Portes = **Explorer** (homepage) + **alias** (`/promotions`, `/kits`, etc.) ; **pas** de rangée « chips » Promotions / sélection éditoriale / Kits au-dessus de la grille sur `/shop` nu | Chips / boutons **au-dessus de la grille** + état « Toute la boutique » |
| **Incontournables** *(sélection éditoriale)* | **Câblé** (**19.0.1.10.x**) — bandeau, chip, alias **`/incontournables`** ; exploitation paramètre sécurisée **19.0.1.10.5** | §5 + **[SPEC_SHOP_PORTES.md §4.6](../mvp_01/SPEC_SHOP_PORTES.md)** : **`ckr.shop.collection`** via **`dorevia_ckreyol_marketplace.featured_collection_id`** ; **`/incontournables`** → **301** → **`/shop?ckr_mode=featured`** ; fallback **`/shop`** ; *Exploitation* (une fois par base **`-u`** ≥ **19.0.1.10.5**) |
| **Collections** | URLs **nobles** `/collections`, `/collections/<slug>`… — **pas** d’exposition visiteur de `/shop?ckr_mode=collection` (doctrine) | À intégrer dans la **grammaire visuelle** sans contredire les contrats |
| **Carte produit** | QWeb **`ckr_shop_classic_tile_restore.xml`** + **`_shop.scss`** : **Nom CK** (`ck_product_name`) ou **`name`** ; **rail coin média** **`ckr-product-card__corner-actions`** (wishlist native **`o_add_wishlist`** + **`ckr-wishlist-ghost`** + bouton info **`fa-info`**, panneau méta / nom Odoo / desc.) — [SPEC_CK_NOM_CK_TUILE_PRODUIT.md](SPEC_CK_NOM_CK_TUILE_PRODUIT.md), [NOTE_TECH_TUILE_CORNER_ACTIONS.md](NOTE_TECH_TUILE_CORNER_ACTIONS.md) ; rubans **`o_wsale_ribbon` `o_left` / `o_right`** ; **wishlist** si **`website_sale_wishlist`** (MOA-1). *Historique* : **« Pour info »** / `<details>` (10.53–10.54) documenté dans la spec. | Grammaire carte V1 (badge, wishlist, promo, rupture) |

Cette section sert de **cadrage** : le MVP2.2 peut rester **purement présentationnel** ([ADR-CKR-002](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-002)) ou ouvrir des **exceptions** justifiées si la sidebar / les raccourcis imposent de la logique non couverte par le standard.

---

## 1. Objectif du MVP2.2

Définir la structure cible de la page boutique C-Kreyol : une boutique plus **dense**, plus **retail**, plus **lisible**, avec une entrée **contextualisée** selon les portes d’accès.

Le MVP2.2 vise à figer la **grammaire de page** avant ou pendant l’implémentation Odoo : organisation générale, bandeau contextuel, filtres, raccourcis commerciaux, grille produit et carte produit V1 — **sans** rouvrir seul les **sources de vérité** des portes (déjà documentées dans `mvp_01`).

**Documents d'exécution associés** :

- [SHOP_EXEC_MATRIX.md](SHOP_EXEC_MATRIX.md) — matrice par contexte `/shop` ;
- [SHOP_COMPONENT_CONTRACTS.md](SHOP_COMPONENT_CONTRACTS.md) — mapping composants / code / invariants ;
- [TICKET_SHOP_MVP22_VISIBLE_WAVE1.md](../crea/TICKET_SHOP_MVP22_VISIBLE_WAVE1.md) — ticket Vague 1.

### 1.1 Invariants d'orchestration

Ces règles sont **bloquantes** pour toute implémentation boutique, y compris si l'habillage reste proche du standard `website_sale`.

1. **Un seul `h1` visible** sur la page.
2. **Un seul bloc contextuel principal** :
   - hero CK ;
   - ou bandeau porte historique ;
   - jamais les deux.
3. **La recherche prime sur l'éditorial** :
   - pas de grand hero si `search` est actif ;
   - pas de copy longue parasite sur les résultats.
4. **Les shortcuts commerciaux ne dupliquent pas les filtres** :
   - ils accélèrent l'accès à des portes ;
   - ils ne deviennent pas une seconde sidebar.
5. **La sidebar native ne doit pas dominer visuellement la grille** :
   - son rôle est utilitaire ;
   - elle ne doit pas devenir le premier point focal du premier écran.

---

## 2. Organisation générale de la page

La page boutique est organisée en trois niveaux :

1. Header / navigation
2. Bandeau boutique pleine largeur
3. Zone boutique en deux colonnes :
   - sidebar filtres à gauche ;
   - contenu produits à droite.

Le bandeau boutique est placé au-dessus de la zone deux colonnes. Il ne doit pas être contenu uniquement dans la colonne produits.

**Amendement** : sur **petit écran**, le standard Odoo bascule souvent les filtres en **panneau coulissant** ; la cible « deux colonnes » s’entend comme **desktop**. Préciser en maquette le comportement **tablette** (sidebar repliable ? même logique qu’Odoo ?).

---

## 3. Bandeau / hero contextuel

Le bandeau boutique est le premier élément visuel de la page après la navigation.

Règles cibles :

- placé au-dessus du layout deux colonnes ;
- largeur complète du contenu boutique ;
- **image de fond** : cible MVP2.2 ; **livrable V1** = bandeaux **sans** image (voir §0) — décider si l’image est **obligatoire** dès MVP2.2 ou **progressive enhancement** ;
- overlay sombre ou chaud pour préserver la lisibilité (si fond image) ;
- titre et texte adaptés au contexte d’entrée ;
- rendu éditorial, sobre, chaleureux et premium ;
- hauteur maîtrisée : visible, mais non envahissant.

**Amendement** : prévoir **fallback** si aucune image n’est configurée en back-office (dégradé / couleur charte) pour éviter une régression visuelle.

**Vague 1 visible — acté MOA (asset hero)** : **fallback charte** par défaut ; **image statique** autorisée **uniquement** si elle existe **déjà** dans les assets du module ; **pas** de gestion BO riche ni de **6 images** contextuelles en BO ; **pas** d’images hero **distinctes par porte** dans cette vague (report cible MVP2.2). Voir [TICKET_SHOP_MVP22_VISIBLE_WAVE1.md — MOA-2](../crea/TICKET_SHOP_MVP22_VISIBLE_WAVE1.md).

---

## 4. Sidebar filtres

La sidebar sert aux filtres profonds du catalogue.

Sections prévues :

- Catégories ;
- Collections ;
- Origines ;
- Prix.

Comportement :

- présentation en accordéons ;
- le bloc correspondant à la porte d’entrée peut être affiché en premier ;
- le bloc correspondant à la porte d’entrée est ouvert par défaut lorsque pertinent *(cible E2 pour Catégories / Collections / Origines)* ;
- les autres blocs de cette série restent visibles mais repliés ;
- le bloc **Prix** (natif) est **déplié par défaut** au chargement (**19.0.1.10.28**), comme le standard `website_sale.filter_products_price`.

La sidebar ne porte pas les raccourcis commerciaux principaux.

**Implémentation (module ≥ 19.0.1.10.18 ; ajustements filtre Prix & tuile ≥ 19.0.1.10.52)** : ordre rail desktop **Catégories → Collections → Origines → Prix**. Le rail force **`opt_wsale_categories = True`** (bloc Catégories sans activer la vue native en BO). **`show_price_filter`** n’est **plus** forcé à `True` : il suit **`opt_wsale_filter_price`** (`is_view_active('website_sale.filter_products_price')`), comme le standard — sinon le contrôleur n’injecte pas `min_price` / `max_price` et le gabarit **`filter_products_price`** peut lever **`TypeError`** (`'%f' % None`) → **HTTP 500**. **Collections** / **Origines** = navigation CK (liens nobles / porte). **Prix** : (1) data **`data/ckr_shop_filter_price_activation.xml`** bascule la vue native **`website_sale.filter_products_price`** sur **`active`** à l’`-u` ; (2) **`WebsiteSaleCKR._ckr_get_price_filter_shop_values`** recalcule **`available_min_price` / `available_max_price`** (et bornes affichées) si le contexte les omet, en réutilisant la **même logique Odoo 19** que le shop : **`_get_shop_domain`**, **`product.template._search(domain)`**, **`query.select(SQL(...))`**, **`execute_query`**, taux **`res.currency._get_conversion_rate`** vers **`website.currency_id`** — **sans** APIs non portées sur l’instance (`get_current_pricelist`, `pricelist_id`, `_where_calc`, etc.) ; (3) gabarit **`ckr_shop_filter_products_price_standalone`** dans **`views/pages/ckr_shop.xml`** (attributs **`website.currency_id`** pour symbol / position / rounding, aligné natif) ; widget natif **repositionné** avant facettes ; styles / FR **`ckr_shop_filter_price_fr`**. **Facette attribut Origine** masquée lorsque le bloc CK **Origines** est alimenté. **Liens catégorie** Odoo 19 : `keep('%s/category/%s' % (shop_path, slug(c)))` (**10.27**). Les **autres attributs / tags** actifs restent **sous** ces quatre blocs. **Ouverture par porte** (premier accordéon des trois premiers blocs) : cible E2 — [SHOP_MAQUETTE_ECARTS.md §2](SHOP_MAQUETTE_ECARTS.md).  
**Collections** : pas de seconde logique contradictoire avec **`/collections`** ([contrats `mvp_01`](../mvp_01/SPEC_SHOP_PORTES.md)).

**Gel visuel / backlog** : le **rendu** du rail filtres est **gelé** pour la recette en cours. Le **comportement après sélection** des filtres (navigation, état actif, cases cochées, combinaisons **Catégories / Collections / Origines / Prix**) fait l’objet d’un **report fonctionnel** documenté — pas de chantier ouvert tant que la spec comportementale n’est pas arbitrée ([TICKET_SHOP_SIDEBAR_CATEGORIES.md — Backlog fonctionnel](TICKET_SHOP_SIDEBAR_CATEGORIES.md#backlog-fonctionnel-hors-périmètre-gel-visuel), [SHOP_MAQUETTE_ECARTS.md — tableau décisions](SHOP_MAQUETTE_ECARTS.md#décisions-produit-à-suivre-trace)).

---

## 5. Raccourcis commerciaux

Les raccourcis commerciaux sont affichés dans la colonne produits, au-dessus de la grille.

Boutons prévus :

- Promotions ;
- **Incontournables** ou **Notre sélection** *(libellés visiteur MVP2.2 — porte éditoriale manuelle, §5)* ;
- Kits / Packs.

Rôle :

- proposer des modes de lecture rapides de la boutique ;
- ne pas les confondre avec les filtres profonds de la sidebar ;
- permettre une navigation commerciale immédiate.

Comportement attendu :

- bouton actif visuellement identifiable ;
- retour possible à l’état « Toute la boutique » ;
- sur mobile, les boutons peuvent devenir des chips horizontales scrollables.

**Amendement** : **Promotions** et **Kits** ont déjà des **équivalents URL** (`/shop?ckr_mode=promo`, `pack`). Le raccourci doit **réutiliser** ces signaux (pas de second mécanisme métier).

### Incontournables / sélection éditoriale — doctrine MVP2.2 (décision MOA)

La porte **« Incontournables »** est une **sélection éditoriale manuelle** (back-office). Elle **n’est pas** un classement calculé à partir des ventes réelles.

**Objectifs** :

- **Éviter les faux best-sellers** (intention commerciale assumée, pas de statistique implicite) ;
- **Permettre une mise en avant réaliste dès l’ouverture**, sans attendre un volume d’historique ;
- **Conserver une porte commerciale utile** sans dépendre d’un historique de ventes suffisant.

**Hors scope MVP2.2** : toute **logique de calcul automatique** à partir des commandes / statistiques de vente (requêtes « vrais » tops, courbes, fenêtres glissantes, etc.).

#### Transparence du libellé public

Tant que la porte **n’est pas** alimentée par un **calcul réel** à partir des **ventes confirmées**, le **libellé public** ne doit **pas** laisser entendre un **classement statistique**.

Pour **MVP2.2**, libellés **visiteur** :

- **prioritaire** : **« Incontournables »** ;
- **alternatif** : **« Notre sélection »**.

Le libellé **« Meilleures ventes »** est **réservé** à une **version ultérieure**, uniquement si un **calcul réel**, **documenté** et **vérifiable** est mis en place.

#### Convention URL & `ckr_mode` (actée MOA)

| Élément | Valeur |
|---------|--------|
| **Libellé visiteur** (prioritaire) | Incontournables |
| **URL courte** | `/incontournables` |
| **URL canonique** (boutique filtrée) | `/shop?ckr_mode=featured` |
| **Nom technique** | `featured` |

*(Redirection **301** et canonique : voir **Porte Incontournables — spécification cible** ci-dessous ; synthèse **`mvp_01`** : **[SPEC_SHOP_PORTES.md](../mvp_01/SPEC_SHOP_PORTES.md)** §4.6 — 2026-04-25 ; contrat détaillé / recette dev à compléter à l’implémentation.)*

#### Arbitrage `ckr_mode=featured` (plutôt que `selection`)

**Retenu** : **`featured`**.

- vocabulaire **e-commerce** courant, **compréhensible** pour les profils tech et métier ;
- **neutre statistiquement** : « mis en avant », pas « meilleure vente » ;
- **plus court** et **plus clair** que `selection` pour le **code**, les **logs** et l’**analytics**.

**Ne pas utiliser** `best_sellers`, `top_sales`, ni équivalents **tant qu’aucun** calcul réel sur **ventes confirmées** n’est implémenté et documenté.

### Porte Incontournables — spécification cible (impl.)

#### Principe

La porte Incontournables expose une sélection éditoriale manuelle de produits.

Elle ne correspond pas à un classement statistique des ventes.

#### URL

- URL courte visiteur : `/incontournables`
- Redirection : 301 vers `/shop?ckr_mode=featured`
- URL canonique : `/shop?ckr_mode=featured`

#### Source de vérité

La source de vérité est une collection éditoriale `ckr.shop.collection`, configurée par site via le paramètre :

`dorevia_ckreyol_marketplace.featured_collection_id`

#### Comportement

Si le paramètre est renseigné et pointe vers une collection active :

- la grille affiche les produits de cette collection ;
- le bandeau utilise le contexte « Incontournables » ;
- la chip « Incontournables » est active.

Si le paramètre est absent, invalide ou pointe vers une collection inactive :

- fallback vers `/shop` ;
- aucun faux contenu n’est affiché ;
- un message discret peut indiquer qu’aucune sélection n’est disponible.

#### Exploitation — paramètre `featured_collection_id` *(clôture **19.0.1.10.5**)*

Règle d’exploitation pour **ne pas perdre** la collection « Incontournables » lors des upgrades module :

- le paramètre **`dorevia_ckreyol_marketplace.featured_collection_id`** n’est **plus** porté par un **fichier XML** data : les futurs **`odoo -u dorevia_ckreyol_marketplace`** **ne réécrasent pas** la valeur vers **`0`** ;
- **première installation** : création avec défaut **`0`** **uniquement si** la clé n’existe pas encore (`post_init_hook`) ;
- **passage `19.0.1.10.5`** : migration **pre/post** qui préserve la valeur si l’ancien mécanisme XML est retiré ;
- **obligation** : exécuter **une fois par base** un **`odoo -u dorevia_ckreyol_marketplace`** (ou équivalent) **jusqu’à au moins `19.0.1.10.5`** pour appliquer cette migration.

Détail canonique : **[SPEC_SHOP_PORTES.md §4.6 — *Exploitation — paramètre `featured_collection_id`*](../mvp_01/SPEC_SHOP_PORTES.md)**.

#### Priorité multi-modes

Priorité cible à valider :

`pack > promo > featured > origin > collection`

#### Non-objectifs

- pas de calcul automatique des meilleures ventes ;
- pas de slug technique `best_sellers` ou `top_sales` ;
- pas de duplication de la logique collection hors `ckr.shop.collection`.

#### Vigilance implémentation *(dev)*

**`featured`** doit **consommer** la collection pointée par le paramètre et **réutiliser** les briques catalogue existantes pour les collections — **sans** recopier une logique « collection » parallèle. Détail : **[SPEC_SHOP_PORTES.md](../mvp_01/SPEC_SHOP_PORTES.md)** §4.6, *Note vigilance (dev)*.

**Bandeau ou micro-copy** (sélection éditoriale) — proposition de ton :

> Une sélection de produits mis en avant par C-Kreyol pour découvrir les essentiels de la boutique.

**Documentation technique** : porte **livrée** — **[SPEC_SHOP_PORTES.md](../mvp_01/SPEC_SHOP_PORTES.md)** **§4.6** (contrat + *Exploitation* paramètre **19.0.1.10.5**).

---

## 6. Grille produits responsive

La grille produits doit être dense, lisible et adaptée à la comparaison produit.

Règle responsive cible :

- desktop large : 4 colonnes ;
- desktop moyen : 3 colonnes ;
- tablette : 2 colonnes ;
- mobile : 1 à 2 colonnes selon lisibilité.

Objectif :

- éviter l’effet galerie trop espacée ;
- conserver des images produit lisibles ;
- permettre une lecture retail efficace.

**Amendement** : le module **habille** déjà la grille via `.ckr-shop` ; valider les breakpoints pour **alignement** avec le Design System (tokens dans `static/src/scss/`).

---

## 7. Carte produit V1

La carte produit V1 est figée avec la grammaire suivante :

- image produit homogène ;
- badge éventuel en haut à gauche ;
- rail d’actions en haut à droite : **wishlist native** + **information secondaire** (`fa-info`) dans un même halo visuel ;
- information secondaire accessible à la demande (méta, nom Odoo, ligne descriptive), sans reprendre de place dans le corps de la carte ;
- nom produit lisible ;
- prix visible ;
- panier en bas à droite ;
- gestion promotion ;
- gestion rupture.

Cas promotion :

- badge « Promotion » ;
- ancien prix barré ;
- nouveau prix mis en évidence.

Cas rupture :

- badge « Rupture » *(prioritaire sur les autres badges —* **MOA-5** *)* ;
- panier désactivé ;
- prix éventuellement grisé ;
- wishlist **si** `website_sale_wishlist` est en périmètre prod *(sinon emplacement sans contrôle —* **MOA-1** *)* ;
- accès à la fiche produit conservé.

**Vague 1 — acté MOA** : **wishlist** (**MOA-1**) — affichage **uniquement** si **`website_sale_wishlist`** est **installé** et **retenu** en prod ; sinon **grammaire de carte** inchangée mais **bouton non affiché** (pas de placeholder vide). **Badges** (**MOA-5**) — priorité : **1.** rupture **2.** promotion **3.** nouveau / sélection **4.** pack / incontournable si utile ; **éviter** plusieurs badges concurrents sur une même carte si le rendu est surchargé. Voir [TICKET_SHOP_MVP22_VISIBLE_WAVE1.md](../crea/TICKET_SHOP_MVP22_VISIBLE_WAVE1.md) — **arbitrages Vague 1 clos**, enchaînement dev **C → D → E0 → B → A**.

**Implémentation pied carte (livrée)** : structure QWeb déterministe (`ckr_shop_classic_tile_restore.xml` : `footer-row`, `footer-price`, `footer-cta`), grille deux colonnes et neutralisations SCSS pour les sorties `product_price` / `shop_product_buttons` — détail **[NOTE_TECH_TUILE_SHOP_FOOTER.md](NOTE_TECH_TUILE_SHOP_FOOTER.md)**.

**Amendement rail coin média (livré)** : l’ancien libellé **« Pour info »** / `<details>` est conservé uniquement comme historique documentaire. L’état courant de la liste `/shop` est le rail **`ckr-product-card__corner-actions`** : wishlist Odoo native (`o_add_wishlist`) + bouton info FontAwesome (`fa-info`), avec panneau d’information masqué par défaut. Voir **[NOTE_TECH_TUILE_CORNER_ACTIONS.md](NOTE_TECH_TUILE_CORNER_ACTIONS.md)** et **[SPEC_CK_NOM_CK_TUILE_PRODUIT.md](SPEC_CK_NOM_CK_TUILE_PRODUIT.md)**.

---

## 8. Comportements selon porte d’entrée

La page boutique doit pouvoir adapter son contexte selon la porte d’entrée.

Portes prévues (vue UX) :

- Toute la boutique ;
- Promotions ;
- **Incontournables** / **Notre sélection** *(libellés visiteur — sélection éditoriale, §5)* ;
- Kits / Packs ;
- Catégories ;
- Collections ;
- Origines.

Pour chaque porte :

- le bandeau peut changer de titre, texte et image ;
- le filtre correspondant peut être mis en avant dans la sidebar ;
- la grille affiche les produits correspondant au contexte ;
- la page conserve une structure homogène.

**Amendements** :

- **Catégories** : entrée typique **`/shop/category/<id>-<slug>`** (natif), **sans** `ckr_mode` — **acté Vague 1** : **un seul** titre principal ; si le **hero CK** est affiché, il **porte le titre de la catégorie** (donnée native) et le **header titre** catégorie Odoo ne doit **pas** s’empiler avec ; le **breadcrumb** natif peut rester s’il reste lisible et non redondant. Voir [TICKET_SHOP_MVP22_VISIBLE_WAVE1.md — MOA-4](../crea/TICKET_SHOP_MVP22_VISIBLE_WAVE1.md).
- **Collections** : contexte **`/collections/...`** — ne pas supposer une seule URL **`/shop`** pour toutes les portes en **canonical**.
- **Incontournables** : **`/incontournables`** → **301** → **`/shop?ckr_mode=featured`** ; source **`dorevia_ckreyol_marketplace.featured_collection_id`** — §5 ; fallback **`/shop`** si config invalide.
- **Priorité multi-signaux** : **`pack > promo > featured > origin > collection`** — **cible à valider** à l’implémentation et à **aligner** sur `SPEC_SHOP_PORTES.md` / tests ; jusqu’à livraison **`featured`**, la règle publiée reste **`pack > promo > origin > collection`**.

---

## 9. Points non traités / hors scope V1

Sont hors scope du MVP2.2 :

- fiche produit détaillée *(hors liste — peut faire l’objet d’un autre chantier)* ;
- **calcul automatique** présenté comme **« Meilleures ventes »** ou tout libellé **statistique** équivalent sans donnée réelle vérifiable ; **noms techniques** du type **`best_sellers`** / **`top_sales`** dans l’URL ou le code tant que ce calcul n’existe pas (voir §5 : **`ckr_mode=featured`** + libellés **Incontournables** / **Notre sélection**) ;
- **double source** pour la sélection Incontournables **hors** `ckr.shop.collection` / paramètre **`featured_collection_id`** (pas de logique parallèle) ;
- collections éditoriales avancées ;
- origines détaillées / pages territoire ;
- personnalisation fine mobile *(à préciser : qu’est-ce qui est « fin » vs table stakes ?)* ;
- animations avancées ;
- tunnel panier / checkout ;
- règles métier de stock avancées.

---

## 10. Références implémentation (relecture technique)

| Zone | Fichiers |
|------|----------|
| Scope page `/shop`, bandeaux porte | `views/pages/ckr_shop.xml` |
| Modes, domaines, collections | `controllers/website_sale_ckr.py` |
| Styles liste / cartes / filtres | `static/src/scss/layout/_shop.scss` |
| Rail wishlist + info tuile | `views/pages/ckr_shop_classic_tile_restore.xml` ; `views/pages/ckr_shop.xml` ; `docs/mvp_02/NOTE_TECH_TUILE_CORNER_ACTIONS.md` |
| Matrice exécutable par contexte | `docs/mvp_02/SHOP_EXEC_MATRIX.md` |
| Contrat composants / orchestration | `docs/mvp_02/SHOP_COMPONENT_CONTRACTS.md` |
| Synthèse portes | `docs/mvp_01/SPEC_SHOP_PORTES.md` — **§4.6 Incontournables** (`featured`) |
| Ticket dev — porte Incontournables | [TICKET_INCONTOURNABLES_SHOP_FEATURED_MVP22.md](../crea/TICKET_INCONTOURNABLES_SHOP_FEATURED_MVP22.md) |
| Ticket dev — **Vague 1 visible** boutique (grille, carte, barre, hero 1re passe, sidebar légère) | [TICKET_SHOP_MVP22_VISIBLE_WAVE1.md](../crea/TICKET_SHOP_MVP22_VISIBLE_WAVE1.md) |

---

## 11. Demandes de précisions MOA / produit

1. **Incontournables** : **impl. livrée** (**19.0.1.10.x**) — fallback **302** vers **`/shop`** ; priorité validée (tests **`dorevia_ckr_collections`**) ; **exploitation paramètre** : §5 *Exploitation* + **[SPEC_SHOP_PORTES.md §4.6](../mvp_01/SPEC_SHOP_PORTES.md)**. *Résidu UX / MOA éventuel* : carte Explorer dédiée, copy message fallback.
2. **Hero image** : **acté Vague 1** — fallback charte par défaut ; image statique **seulement** si asset module **déjà** présent ; **pas** de BO riche (6 jeux / images par porte) dans cette vague ; la cible « image par porte + saisie BO » reste **hors Vague 1** (cf. §3 et [TICKET_SHOP_MVP22_VISIBLE_WAVE1.md](../crea/TICKET_SHOP_MVP22_VISIBLE_WAVE1.md)).
3. **Copy hero** : **acté Vague 1** (**MOA-3**) — **réutiliser** les textes **existants** des **bandeaux actuels** ; **pas** d’atelier copy complet à ce stade ; ajustements **courts** seulement si **incohérence visible** (cf. ticket Vague 1).
4. **Sidebar §4** : **Vague 1 visible** — périmètre **E0** uniquement (habillage du panneau filtres **natif**) ; **refonte structurelle** (4 blocs, E2) et **double logique** filtres / collections **hors** cette vague. *Question ouverte pour une vague ultérieure* : refonte profonde **acceptée** ou **composition** stricte avec le natif — ne **bloque** pas l’implémentation **C → D → E0 → B → A** (cf. [TICKET_SHOP_MVP22_VISIBLE_WAVE1.md](../crea/TICKET_SHOP_MVP22_VISIBLE_WAVE1.md)).
5. **Catégorie native** : **acté Vague 1** — pas de double titre ; hero CK = titre catégorie **unique** ; logique catégorie **native** conservée ; breadcrumb natif si lisible (cf. §8 amendement *Catégories* et ticket Vague 1).
6. **Accessibilité** : niveau cible (WCAG) pour accordéons, chips, contrastes sur hero — pour caler la recette créa / QA.
7. **Wishlist** : **acté Vague 1** (**MOA-1**) — affichage sur les cartes **uniquement** si **`website_sale_wishlist`** est **installé** et **retenu** en prod ; sinon **grammaire de carte** sans bouton en Vague 1 (cf. §7).

---

## 12. Historique

| Date | Événement |
|------|-----------|
| *(rédaction initiale)* | Structure MVP2.2 boutique (objectifs §1–9). |
| 2026-04-25 | **Analyse + amendements** (§0, §11, URLs portes). Porte **sélection éditoriale** : manuelle ; **hors scope** calcul auto (§5, §9). |
| 2026-04-25 | **Transparence libellés** : visiteur **« Incontournables »** (prioritaire) ou **« Notre sélection »** ; **« Meilleures ventes »** réservé au futur calcul vérifiable ; micro-copy bandeau §5. |
| 2026-04-25 | **Acté MOA — Incontournables** : **`ckr_mode=featured`** (rejet `selection` pour clarté code / logs / analytics) ; **`/incontournables`** → **301** → **`/shop?ckr_mode=featured`** ; **proscrit** `best_sellers` / `top_sales` sans calcul réel ; **BO** : **collection éditoriale** en priorité — §5. |
| 2026-04-25 | **Spec porte Incontournables** : paramètre **`dorevia_ckreyol_marketplace.featured_collection_id`** ; comportements **actif** / **fallback `/shop`** ; priorité cible **`pack > promo > featured > origin > collection`** (à valider) ; non-objectifs §5. |
| 2026-04-25 | **Clôture cadrage MOA** atelier MVP2.2 Boutique (UX + doctrine + pré-spec Incontournables) — **`2_SHOP.md`** gelé sauf corrections de forme ; intégration **`SPEC_SHOP_PORTES.md` §4.6** ; prochain pas = **chiffrage / impl. dev**. |
| 2026-04-25 | **Ticket dev** : [TICKET_INCONTOURNABLES_SHOP_FEATURED_MVP22.md](../crea/TICKET_INCONTOURNABLES_SHOP_FEATURED_MVP22.md) (6 lots, critères d’acceptation, points à arbitrer). |
| 2026-04-25 | **Clôture exploitation sous-lot Incontournables** : §5 *Exploitation — paramètre `featured_collection_id`* (module **19.0.1.10.5**) — paramètre hors XML, **`odoo -u`** une fois par base ≥ **19.0.1.10.5** ; renvoi canonique **[SPEC_SHOP_PORTES.md §4.6](../mvp_01/SPEC_SHOP_PORTES.md)** ; §0 / §11 alignés. |
| 2026-04-25 | **Ticket dev — Vague 1 visible** MVP2.2 : [TICKET_SHOP_MVP22_VISIBLE_WAVE1.md](../crea/TICKET_SHOP_MVP22_VISIBLE_WAVE1.md) (lots C, D, B, A, E0 ; critères d’acceptation, dépendances MOA, risques, estimation) — réf. §10. |
| 2026-04-25 | **Acté MOA — Vague 1 boutique** : **MOA-2** (hero : fallback charte ; image module optionnelle si existante ; pas BO riche / pas images par porte) — §3 ; **MOA-4** (catégorie : titre unique dans le hero CK ; pas d’empilement avec header Odoo ; breadcrumb si lisible) — §8 amendement *Catégories*, §11 (points 2 et 5). |
| 2026-04-25 | **Acté MOA — Vague 1 boutique (suite)** : **MOA-1** (wishlist : affichage seulement si module en prod ; sinon emplacement sans UI) — §7, §11.7 ; **MOA-3** (copy hero : bandeaux existants ; pas atelier copy) — §11.3 ; **MOA-5** (badges carte : rupture > promo > nouveau/sélection > pack/incontournable ; pas surcharge multi-badges) — §7. |
| 2026-04-25 | **Clôture arbitrages MOA Vague 1** (confirmation MOA-1, MOA-3, MOA-5) : **tous clos** — dev peut enchaîner **C → D → E0 → B → A** sans attente MOA ; §7 / §11 alignés sur [TICKET_SHOP_MVP22_VISIBLE_WAVE1.md](../crea/TICKET_SHOP_MVP22_VISIBLE_WAVE1.md). |
| 2026-04-25 | **Go implémentation Vague 1 boutique** : validation **MOA Vague 1 clos — prêt implémentation** ; ordre figé **C → D → E0 → B → A** ; **E2** hors périmètre (**E0** seulement) ; objectif page **visible, dense, retail** sans rouvrir le moteur **`website_sale`** — ticket [TICKET_SHOP_MVP22_VISIBLE_WAVE1.md](../crea/TICKET_SHOP_MVP22_VISIBLE_WAVE1.md). |
