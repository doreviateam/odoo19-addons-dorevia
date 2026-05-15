# Boutique `/shop` — alignement maquette / doc et écarts Odoo

**Référence** : maquette validée (composition, hiérarchie) + [2_SHOP.md](2_SHOP.md), [SHOP_COMPONENT_CONTRACTS.md](SHOP_COMPONENT_CONTRACTS.md), [TICKET_SHOP_MVP22_VISIBLE_WAVE1.md](../crea/TICKET_SHOP_MVP22_VISIBLE_WAVE1.md) (Vague **E0** initiale ; le **rail 4 blocs** et le fallback **catégories** + garde-fous **Prix** (**10.52**) sont **livrés** — voir §2 et [TICKET_SHOP_SIDEBAR_CATEGORIES.md](TICKET_SHOP_SIDEBAR_CATEGORIES.md) ; **E2** = surtout **premier accordéon par porte** pour Catégories / Collections / Origines).

**Règle produit** : le libellé **« Meilleures ventes » / Best sellers** et tout équivalent statistique fictif sont **interdits** tant qu’il n’y a pas de calcul réel sur ventes ([2_SHOP.md §5, §9](2_SHOP.md)). La maquette créa peut les montrer : **l’implémentation suit la doc** → chips **Incontournables** + **Toute la Boutique**, pas « best sellers ».

---

## 1. Hero

| Attendu (maquette + doc) | Implémentation | Écart / contrainte |
|--------------------------|----------------|---------------------|
| Bandeau pleine largeur conteneur, coins arrondis (~16–18px), image + voile, titre + accroche | `ckr_shop_hero_wave1` + `.ckr-shop-hero--retail` (image module si `--asset`) | **OK** (rayon `clamp(14px–18px)`). |
| Image et copy **par porte** / BO riche | — | **Hors Vague 1** ([MOA-2](TICKET_SHOP_MVP22_VISIBLE_WAVE1.md)) : pas de 6 visuels contextuels BO ; un seul asset module possible sur le lane retail. |
| Copy hero | Textes contextuels QWeb + accroche retail « terroirs » sur `/shop` nu | **À trancher post-recette** ([MOA-3](TICKET_SHOP_MVP22_VISIBLE_WAVE1.md)) : soit **strictement** les textes des bandeaux historiques, soit **assumer** l’accroche maquette — noter la décision ici une fois actée. |

---

## Décisions produit à suivre (trace)

| Sujet | Contexte | Statut |
|--------|----------|--------|
| **MOA-3 — copy hero `/shop` nu** | Recette visuelle cible **19.0.1.10.14** puis arbitrage : bandeaux historiques **vs** accroche « terroirs » maquette. | **Ouvert** — mettre à jour la ligne « Copy hero » du §1 après décision. |
| **Incontournables vs « Best sellers »** | Doc §5 / §9 : pas de libellé statistique sans données réelles. | **Fermé** — implémentation : **Incontournables** ([2_SHOP.md §5](2_SHOP.md)). |
| **Sidebar — post-filtre (comportement)** | Gel **visuel** du rail acté ; en revanche : après sélection des filtres, préciser navigation, état actif, cases cochées, combinaisons **Catégories / Collections / Origines / Prix** et cas limites. | **Report** — sujet fonctionnel futur ; pas de chantier immédiat ; détail [TICKET_SHOP_SIDEBAR_CATEGORIES.md — Backlog fonctionnel](TICKET_SHOP_SIDEBAR_CATEGORIES.md#backlog-fonctionnel-hors-périmètre-gel-visuel). |

---

## 2. Sidebar « Filtrer par »

### Alignement maquette / doc (quatre blocs)

La maquette et [2_SHOP.md §4](2_SHOP.md) décrivent une sidebar sous **« Filtrer par »** composée de **quatre blocs explicites**, en accordéons, avec ordre et ouverture pilotables selon la porte :

1. **Catégories**  
2. **Collections**  
3. **Origines**  
4. **Prix**

**État livré (≥ 19.0.1.10.18 ; filtre Prix & stabilité **19.0.1.10.52+**)** : ordre maquette / [2_SHOP.md §4](2_SHOP.md) dans le rail desktop : **Catégories** (natif + fallback `opt_wsale_categories = True` **10.24+**) → **Collections** → **Origines** (navigation CK, accordéons) → **Prix** (natif, **`show_price_filter = opt_wsale_filter_price`** dans le rail — plus de `True` forcé : évite **HTTP 500** si le gabarit natif reçoit des bornes **None**) ; data **`ckr_shop_filter_price_activation.xml`** ; recalcul **`_ckr_get_price_filter_shop_values`** ; gabarit **`ckr_shop_filter_products_price_standalone`** ; repositionné avant les autres facettes → éventuellement **autres attributs / tags** Odoo dans le bloc facettes. **Collections** / **Origines** : liens **`/collections/<slug>`** et **`/shop?ckr_mode=origin&ckr_origin=<slug>`** ; facette attribut **Origine** masquée si le bloc CK est alimenté (**10.17**). **Finition rail (10.19)** : **pas de boîte blanche** sur le rail (fond = page) ; typo maquette (titre serif fort, sections sans-serif) ; séparateurs fins ; bande crème légère **Collections + Origines** ; prix / facettes en flux plat. **Liens catégories Odoo 19** : plus de `website_url` sur `product.public.category` — construction **`keep('%s/category/%s' % (shop_path, slug(c)))`** (**10.27**). **Offcanvas** : retrait d’un héritage QWeb fragile sur l’en-tête catégories (**10.26**). **Prix** : panneau **déplié par défaut** quand le bloc est affiché (**10.28**, comportement natif). L’**accordéon ouvert en premier selon la porte** (les trois premiers blocs) reste **E2**.

| Bloc maquette | État (19.0.1.10.18) | Commentaire |
|---------------|----------------------|-------------|
| **Catégories** | Partiel (natif + CK) | **Widget natif** Odoo ; le module **force** `opt_wsale_categories` dans le rail pour garantir le bloc sans activer la vue en BO (`ckr_shop_sidebar_rail_maquette.xml`). Intitulés / hiérarchie peuvent différer de la maquette. Libellés FR + accordéon maquette : `ckr_shop_categories_list_fr` / gabarits associés. Liens : patron **`website_sale.categorie_link`** (Odoo 19, **10.27**). |
| **Collections** | **Navigation CK dans le rail** | Liste des `ckr.shop.collection` visibles (`_ckr_visible_domain`) → liens nobles `/collections/<slug>` ; compteur produit si renseigné. Doctrine inchangée : pas de `ckr_mode=collection` en URL publique de référence ([SHOP_COMPONENT_CONTRACTS.md](SHOP_COMPONENT_CONTRACTS.md)). |
| **Origines** | **Navigation CK dans le rail** | Bloc dédié : profils `ckr.shop.origin` publiés + lien « Toutes les origines » ; filtrage via la porte Origines existante. **Facette attribut catalogue « Origine » masquée** dès que le bloc CK est alimenté (19.0.1.10.17) — une seule entrée « Origines » dans le rail. |
| **Prix** | Partiel (natif + garde-fous CK) | Le rail aligne **`show_price_filter`** sur **`opt_wsale_filter_price`** (**10.52**) : bloc **absent** si la vue native n’est pas active (évite **500**). À l’`-u`, **`ckr_shop_filter_price_activation.xml`** active la vue ; **`_ckr_get_price_filter_shop_values`** complète les bornes si le contexte les omet. Libellé FR + styles rail : `ckr_shop_filter_price_fr`. **Déplié par défaut** quand affiché (**10.28**). |

**Reste cible E2 (finition)** : orchestration **stricte** maquette (ordre figé des quatre blocs, premier accordéon ouvert par contexte porte) si la recette l’exige.

---

| Attendu | Implémentation | Écart / contrainte |
|---------|----------------|---------------------|
| Titre **Filtrer par** | `ckr_shop_sidebar_filter_heading` + `.ckr-shop-sidebar__filter-heading` | **OK** (intégré rail, charcoal — 10.17). |
| Ordre **Catégories → Collections → Origines → Prix** | CK inject **26** ; prix rail **29–30** ; catégories / prix natifs | **OK** (10.18) ; facettes supplémentaires après **Prix**. |
| Blocs **Collections** / **Origines** | `ckr_shop_sidebar_ck_sections` + `ckr_sidebar_*` | **OK** (navigation CK). |
| Cases cochées bordeaux | SCSS `:checked` sur `.form-check-input` dans `#products_grid_before` | **OK** (habillage). |
| Libellés **Catégories**, lien **Toute la boutique** | `ckr_shop_categories_list_fr` + accordéon FR | **OK** (remplace l’anglais natif sur le bloc catégories natif). |
| **Effacer les filtres** | `ckr_shop_clear_filters_fr` | **OK** (libellé FR sur le lien natif). |
| Rail **maquette** (plat, pas carte Odoo) | `layout/_shop.scss` + `ckr_shop_sidebar-ck__cluster` | **OK** (19.0.1.10.19). |

---

## 3. Toolbar (chips, compteur, tri)

| Attendu | Implémentation | Écart / contrainte |
|---------|----------------|---------------------|
| Chips + compteur + tri sur une ligne au-dessus de la grille | `ckr_shop_explorer_shortcuts` + tri / liste de prix dans `__tools` ; doublon masqué dans la toolbar Odoo | **OK** ; un seul moteur de tri natif ([contrat](SHOP_COMPONENT_CONTRACTS.md)). |
| **4** raccourcis dont **Toute la Boutique**, **Incontournables**, **Kits** | Liens `/shop`, `/promotions`, `/incontournables`, `/kits` | **OK** ; pas de chip « Best sellers » (doc §9). |
| Style inactif contour bordeaux, actif plein | `.ckr-shop-shortcuts__link` | **OK** (aligné maquette variante contour). |

---

## 4. Grille produit

| Attendu | Implémentation | Écart / contrainte |
|---------|----------------|---------------------|
| 4 col. desktop large, 3 / 2 / 1 selon [2_SHOP.md §6](2_SHOP.md) | 4 col. dès **1200px**, 3 col. ≥992px, 2 col. par défaut, 1 col. &lt;380px | **OK** (ajusté pour coller au « desktop large »). |
| Gouttière ~20–24px | `--ckr-shop-grid-gap: clamp(1rem, 1.15vw, 1.5rem)` | **OK**. |
| `ppr` / data Odoo | Grille **CSS** sur `#o_wsale_products_grid_table` | **Contrainte** : le moteur de placement reste celui d’Odoo ; on surcharge la **présentation** en grid (pas de second moteur). |

---

## 5. Cartes produit

| Attendu | Implémentation | Écart / contrainte |
|---------|----------------|---------------------|
| Image carrée, badge haut gauche, wishlist haut droite, catégorie, nom serif, prix, CTA | QWeb `ckr_shop_classic_tile_restore.xml` + SCSS : **titre** = **Nom CK** ou `name` ; **rail coin** **`ckr-product-card__corner-actions`** (wishlist + **`fa-info`**) pour méta + nom Odoo + ligne desc. — [SPEC_CK_NOM_CK_TUILE_PRODUIT.md](SPEC_CK_NOM_CK_TUILE_PRODUIT.md), [NOTE_TECH_TUILE_CORNER_ACTIONS.md](NOTE_TECH_TUILE_CORNER_ACTIONS.md) ; **rubans** `o_left` / `o_right` ; pied **prix \| CTA** — [NOTE_TECH_TUILE_SHOP_FOOTER.md](NOTE_TECH_TUILE_SHOP_FOOTER.md). *Ancien rendu* : « Pour info » / `<details>` (10.53–10.54), voir spec § Historique. | **OK** ; détail notes tuile. |
| Badges **SÉLECTION** vert, **PROMOTION** rouge, **RUPTURE** gris | Rubans Odoo `product.ribbon` + classes `html_class` | **Contrainte** : les couleurs **par type** imposent un **mapping** ruban BO → classe CSS (ou rubans dédiés) ; pas de vérité unique dans le standard sans convention métier. |
| Wishlist | Si module **website_sale_wishlist** | **MOA-1** : pas de bouton factice si absent ; rendu **ghost** sur l’image si présent. |
| Bouton panier carré bordeaux | `.o_wsale_product_btn_primary` | **OK** (variante proche maquette). |

---

## 6. Espaces et alignements

| Attendu | Implémentation | Écart / contrainte |
|---------|----------------|---------------------|
| Fond page crème | `#wrap.o_wsale_products_page.ckr-shop { #fcf9f7 }` | **OK** (surcharge `.ckr-page`). |
| Haut de sidebar ~ aligné barre chips | `padding-top` réduit sur `#products_grid_before` (≥992px) | **Approximation** : le `pt` natif de l’`aside` et le **dropzone** éditable peuvent varier ; recette visuelle sur instance. |
| Filmstrip catégories sous le header | Masqué si hero CK | **OK** (évite doublon avec rail + hero). |
| Breadcrumb | Masqué si hero | **Écart optionnel [MOA-4](TICKET_SHOP_MVP22_VISIBLE_WAVE1.md)** : le fil **peut** rester ; masqué pour réduire la redondance avec le hero — réactivation possible si MOA exige le fil visible. |

---

## Historique

| Date | Événement |
|------|-----------|
| 2026-04-25 | §5 — pied tuile **prix \| CTA** une ligne : doc alignée sur `ckr_shop_classic_tile_restore.xml` + [NOTE_TECH_TUILE_SHOP_FOOTER.md](NOTE_TECH_TUILE_SHOP_FOOTER.md) (**19.0.1.10.51**). |
| 2026-04-26 | Création — synthèse écarts / contraintes pour relecture maquette vs Odoo 19 `website_sale`. |
| 2026-04-26 | Section « Décisions produit à suivre » — MOA-3 ouvert post-recette **19.0.1.10.14** ; Incontournables acté. |
| 2026-04-26 | §2 — écart **sidebar 4 blocs** (dont **Collections** absent du rail `/shop`) tracé comme **non traité Vague 1** ; **cible E2** explicite (Catégories / Collections / Origines / Prix). |
| 2026-04-26 | §2 — **Collections** + **Origines** : blocs navigation CK dans le rail `/shop` (19.0.1.10.15) ; catégories/prix natifs ; doc §2 réalignée ; finition E2 (ordre / premier accordéon / doublon facettes) ouverte. |
| 2026-04-26 | §2 — finition **rail unifié** (19.0.1.10.16) : coquille sidebar + sections flush, typographie accordéons alignée. |
| 2026-04-26 | §2 — **10.17** : hiérarchie titres sidebar (charcoal, hover terracotta) ; masquage facette **Origine** si bloc CK **Origines** présent. |
| 2026-04-26 | §2 — **10.18** : ordre rail **Catégories → Collections → Origines → Prix** (Prix avant autres facettes). |
| 2026-04-26 | §2 — **10.19** : rendu sidebar aligné maquette (rail plat, typo, cluster CK, taupe). |
| 2026-04-25 | §2 — **10.25–10.28** : `show_price_filter` forcé rail ; données démo **4 blocs** ; **10.26** retrait xpath offcanvas fragile ; **10.27** liens catégorie sans `website_url` (Odoo 19) ; **10.28** bloc **Prix** déplié par défaut ; tableau Catégories / Prix et paragraphe « État livré » alignés. |
| 2026-04-26 | **10.52** + doc : §2 **Prix** — `show_price_filter = opt_wsale_filter_price`, data activation, fallback contrôleur, gabarit standalone ; §5 wishlist ghost + rubans `o_left`/`o_right` dans `_shop.scss`. |
| 2026-04-26 | **10.53** : §5 — **Nom CK** (`ck_product_name`) + **Pour info** (`<details>`) ; [SPEC_CK_NOM_CK_TUILE_PRODUIT.md](SPEC_CK_NOM_CK_TUILE_PRODUIT.md). |
| 2026-04-26 | **10.54** : §5 — maquette **flux principal** (titre + filet) ; **Pour info** dans le **pied** (hors colonne titre) ; compactage SCSS. |
| 2026-04-26 | **10.55+** (doc **2026-04-26**) : §5 — information secondaire **rail coin média** (`ckr-product-card__corner-actions`, wishlist native + `fa-info`) ; fin du libellé **« Pour info »** / `<details>` sur la tuile liste — [NOTE_TECH_TUILE_CORNER_ACTIONS.md](NOTE_TECH_TUILE_CORNER_ACTIONS.md), [SPEC_CK_NOM_CK_TUILE_PRODUIT.md](SPEC_CK_NOM_CK_TUILE_PRODUIT.md). |
| 2026-04-25 | **Décisions produit** — ligne **Sidebar post-filtre** : gel rendu visuel ; backlog comportement (navigation, actif, coches, combinaisons 4 blocs) tracé sans chantier. |
