# Spécification d’implémentation — Portes Explorer → Boutique `/shop`

| Champ | Valeur |
|--------|--------|
| **Statut** | **Synthèse vivante** — **vagues A et B** (**Promotions**, **Pack/Kits**, **Catégories**, **Origines**) : **livrées** en module. **Vague C** (**Collections**) : **livrée + recettée MOA** en module **19.0.1.6.1** (2026-04-22) — contrôleur public `WebsiteSaleCKR` avec routes nobles **`/collections`** / **`/collections/<slug>`** / **`/collections/union/<path:path>`**, **301** normalisation + **302** replis (flash session one-shot), **canonical self**, bandeaux §8 + état vide §12 A, bloc fiche produit (ACL **public** + **portail** read-only sur `ckr.shop.collection`), cleanup stub CMS ; filtre catalogue sur **`product.template._search_get_detail`** (point unique Odoo 19, bloc `ckr_collection_only` + `ckr_collection_template_ids`) ; priorité **`ckr_mode`** **figée** **`pack > promo > origin > collection`** (collection **en fin**) ; tests **`dorevia_ckr_collections`** exécutés réellement : **23** méthodes (9 Model + 14 HTTP), **0 FAIL / 0 ERROR / 0 `skipTest`**, 13,92 s. Checklist §13 `SPEC_IMPL_COLLECTIONS.md` **clôturée** ; PV **Conforme** (preuves `docs/mvp_01/evidences/`). |
| **Date** | 2026-04-21 (création) ; **cohérence éditoriale** : 2026-04-22 |
| **Périmètre** | Section homepage **Explorer / Par où commencer** : cinq portes, **destination commerciale unique** `/shop`, variation par **mode de lecture** (filtre / contexte). |
| **Doctrine** | [ADR-CKR-007](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007) (convergence `/shop`), [ADR-CKR-008](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008) (cinq portes), [ADR-CKR-001](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-001) (standard d’abord), [DOCTRINE_CK_PACK_VS_KIT.md](../direction/DOCTRINE_CK_PACK_VS_KIT.md) (pack homogène vs kit hétérogène — copy / catalogue). |

**Extension MVP2.2 (2026-04-25) — porte Incontournables** : cadrage MOA dans **[2_SHOP.md](../mvp_02/2_SHOP.md)** ; intégration **officielle** dans la présente SPEC — **§4.6**. **Livrée** en module (**19.0.1.10.x**, clôture exploitation paramètre **19.0.1.10.5**) : contrat **`/incontournables`** → **301** → **`/shop?ckr_mode=featured`** ; canonical **`/shop?ckr_mode=featured`** ; source **`dorevia_ckreyol_marketplace.featured_collection_id`** ; priorité **`pack > promo > featured > origin > collection`** (tests **`dorevia_ckr_collections`**, RC-14). **Exploitation** du paramètre : **§4.6** *Exploitation — paramètre `featured_collection_id`*.

Ce document **ne remplace pas** les ADR : il détaille **comment** implémenter la convergence boutique une fois les choix métier / données posés. Pour une porte donnée, tant que **source de vérité** ou **contrat d’URL** manquent, les liens Explorer correspondants restent au mieux **cohérents en intention**, au pire **décoratifs**. **État courant des portes** (lecture 2026-04-22) :

- La porte **Promotions** est **déployée** (v19.0.1.2.0, 2026-04-21). Source de vérité **A2** (`product.pricelist.item` actif strictement réducteur sur la pricelist courante), contrat d’URL **Hybride H1** — `/promotions` en **301** vers `/shop?ckr_mode=promo`, résolveur `product.pricelist._ckr_get_promo_template_ids`, bandeau visiteur + **état vide dédié**, canonical injecté. Détail : [CONTRAT_URL_PROMOTIONS.md §12-13](CONTRAT_URL_PROMOTIONS.md). Pré-requis ops non bloquant : alimentation back-office d’au moins une pricelist datée avec remise effective ; groupe `product.group_product_pricelist` actif sur `tenant_o7`.
- La porte **Pack** (libellé visiteur : **Kits** — cf. règle de bi-lexique [ADR-CKR-008](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008)) est **déployée** (v19.0.1.1.0). Source de vérité : booléen **`product.template.pack_ok`** (module OCA **`product_pack`**, case *« Est un pack ? »* et onglet *Pack* en back-office). Contrat d’URL **Hybride H1** — `/kits` en **301** vers `/shop?ckr_mode=pack`, filtre domaine `("pack_ok", "=", True)`, bandeau visiteur « Kits », stub CMS retiré. Détail : [CONTRAT_URL_PACKS.md §12](CONTRAT_URL_PACKS.md). Point ouvert résiduel : niveau d’affichage des **lignes de pack** (`pack_line_ids`) sur la fiche produit. Dans tout ce document, la grille de vocabulaire **Pack** est retenue pour les éléments **techniques / sources de vérité / implémentation** ; la grille **Kits** désigne le **libellé visiteur** (URL visible `/kits`, titre de carte Explorer, copy marketing). **Doctrine métier** ([DOCTRINE_CK_PACK_VS_KIT.md](../direction/DOCTRINE_CK_PACK_VS_KIT.md)) : réserver **pack** aux compositions **homogènes** (conditionnement) et **kit** aux **hétérogènes** (usage / expérience) dans les **libellés et contenus** ; la porte technique liste aujourd’hui l’ensemble des `pack_ok`.
- La porte **Catégories** est **déployée** (v19.0.1.3.0, 2026-04-22). Source de vérité **`product.public.category`** (taxonomie e-commerce standard). Contrat d’URL **Hybride H1 — cible native** — `/categories` en **301** vers **`/shop/category/<id>-<slug>`** (pas de `ckr_mode` ; filtre et fil d’Ariane **100 % `website_sale`**). Résolution de la catégorie d’entrée : paramètre système optionnel `dorevia_ckreyol_marketplace.explorer_public_category_id`, sinon première racine publique du site ; repli **`/shop`** nu si aucune catégorie. Détail : [CONTRAT_URL_CATEGORIES.md §12-13](CONTRAT_URL_CATEGORIES.md).
- La porte **Origines** est **livrée** (vague B, module **19.0.1.4.x**). **[CONTRAT_URL_ORIGINES.md](CONTRAT_URL_ORIGINES.md)** : **§13** = **référence métier stable** ; implémentation selon **[SPEC_IMPL_ORIGINES.md](SPEC_IMPL_ORIGINES.md)** et recette **[PV_RECETTE_ORIGINES_V1.md](PV_RECETTE_ORIGINES_V1.md)** ; alias **`/origines`** → **301** vers **`/shop?ckr_mode=origin`** ; stub CMS associé **retiré** (cleanup data). **§13** figé hors nouvelle décision MOA **écrite**.
- La porte **Collections** (vague C) : **[CADRAGE_FONCTIONNEL_COLLECTIONS.md](CADRAGE_FONCTIONNEL_COLLECTIONS.md)**, **[CONTRAT_URL_COLLECTIONS.md](CONTRAT_URL_COLLECTIONS.md)** (URLs nobles + combinaison **S1**), **[SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md)** et **[PV_RECETTE_COLLECTIONS_V1.md](PV_RECETTE_COLLECTIONS_V1.md)** (recette **RC-01…RC-14**, tests **`dorevia_ckr_collections`**) : **prêts implémentation v1** (MOA 2026-04-22), **zéro résidu documentaire** — priorité **`ckr_mode`** figée **`pack > promo > origin > collection`** (**§4.3** contrat + [SPEC_IMPL §5.1](SPEC_IMPL_COLLECTIONS.md#51-constantes-alignement-packs--promos--origines--priorité-ckr_mode-figée-moa-2026-04-22)). Carte Explorer : lien **`/collections`** (stub CMS **transitoire** jusqu’aux routes CK).
- La porte **Incontournables** *(MVP2.2 — sélection éditoriale, nom technique **`featured`*)* : **livrée** (**19.0.1.10.x**, exploitation paramètre sécurisée **19.0.1.10.5**) — **[2_SHOP.md](../mvp_02/2_SHOP.md)** et **§4.6** ci-dessous. Contrat : **`/incontournables`** → **301** → **`/shop?ckr_mode=featured`** ; source **`dorevia_ckreyol_marketplace.featured_collection_id`** ; pas de duplication hors **`ckr.shop.collection`** ; interdits **`best_sellers`** / **`top_sales`** sans calcul réel sur ventes. Priorité : **`pack > promo > featured > origin > collection`**. **Exploitation** : §4.6 *Exploitation — paramètre `featured_collection_id`*.

### Règle cible universelle (rappel ferme)

> **Les cinq cartes de la section Explorer doivent converger vers la Boutique `/shop`.** ([ADR-CKR-007](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007))
>
> - **Destination commerciale unique** : `/shop` (forme native ou forme canonique de `/shop`).
> - **Modes d’entrée différents** : Promotions, Collections, Kits *(grille interne : Pack)*, Catégories, Origines — un **contexte de lecture** par porte (filtre / paramètre / catégorie publique / URL native).
> - **Pas d’exception** : aucune porte ne débouche à terme sur une vitrine de remplacement.
>
> Les entrées **stub** ou **alias** vers la boutique tiennent le lien tant que la porte n’est pas **câblée** comme prévu : aujourd’hui, **`/kits`** et **`/origines`** sont des **redirections 301** actives vers la lecture **`/shop`** (ou catégorie native pour Catégories) ; **`/collections`** reste en règle générale un **stub CMS transitoire** jusqu’à l’implémentation des **routes nobles** actées au contrat. Issue finale pour chaque porte : **redirection** ou **façade** alignée sur la doctrine [ADR-CKR-007](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007).

### Snapshot — état actuel des liens Explorer vs cible

L’état courant de `views/snippets/ckr_entries.xml` (version 19.0.1.3.0) :

| Carte | `href` actuel | Statut actuel | Cible finale |
|-------|---------------|---------------|--------------|
| **Promotions** | `/promotions` | **Déployé — Hybride H1 opérationnel** ([CONTRAT_URL_PROMOTIONS.md §12-13](CONTRAT_URL_PROMOTIONS.md)) : redirection **301** portée par `WebsiteSaleCKRAliases`, filtre source de vérité A2 (pricelist datée avec remise, résolu par `product.pricelist._ckr_get_promo_template_ids`), bandeau titre « Promotions » + **état vide dédié**, canonical forcé sur `/shop?ckr_mode=promo` | **Cible atteinte** *(v19.0.1.2.0)*. Reste : alimentation back-office d’au moins une pricelist datée avec remise (pré-requis ops non bloquant — porte affichée en état vide tant que non alimentée) |
| **Collections** | `/collections` | **Déployé + Recetté MOA** — URLs nobles CK opérationnelles (module **19.0.1.6.1**, recette 2026-04-22) : contrôleur public `WebsiteSaleCKR` étendu avec routes **`/collections`** / **`/collections/<slug>`** / **`/collections/union/<path:path>`** (+ garde `/collections/union`) ; **301** normalisation (tri lexicographique, collapse doublons → `/collections/<slug>`) ; **302** replis (slug inconnu, union incomplète, **repli A** union invalide) avec **flash session one-shot** (`ckr_collection_notice` — **sans** `ckr_notice` en query) ; **canonical self** (pas de fuite `/shop?ckr_mode=collection`) ; bandeaux **§8** + **état vide §12 A** + lien *Retour aux collections* ; bloc fiche produit → liens `/collections/<slug>` (ACL **public** + **portail** read-only sur `ckr.shop.collection`) ; filtre catalogue sur **`product.template._search_get_detail`** (point unique Odoo 19) ; **cleanup** stub CMS `/collections` (data `ckr_cleanup_collections_stub.xml`). Priorité **`ckr_mode`** figée : **`pack > promo > origin > collection`** (collection **en fin** — non-régression absolue portes livrées). Tests **`dorevia_ckr_collections`** : **23** méthodes (9 Model + 14 HTTP), **0 FAIL / 0 ERROR / 0 `skipTest`**, 13,92 s ; PV **Conforme** + preuves `docs/mvp_01/evidences/`. Objet CK éditorial — §4.2 | **Cible atteinte + recettée** *(v19.0.1.6.1)*. Pré-requis ops : alimentation BO d'au moins une collection visible (patron Origines) — sans collection alimentée, `/collections` rend une grille vide (standard Odoo) sans effet secondaire |
| **Kits** *(interne : Pack)* | `/kits` | **Déployé — Hybride H1 opérationnel** ([CONTRAT_URL_PACKS.md §12](CONTRAT_URL_PACKS.md)) : redirection **301** portée par le contrôleur CK, filtre `pack_ok=True` appliqué, bandeau titre « Kits », canonical ciblé sur `/shop?ckr_mode=pack`, stub CMS retiré | **Cible atteinte.** Seul point ouvert résiduel : affichage des `pack_line_ids` sur la fiche produit (décision ultérieure) |
| **Catégories** | `/categories` | **Déployé — Hybride H1 cible native** ([CONTRAT_URL_CATEGORIES.md §12-13](CONTRAT_URL_CATEGORIES.md)) : redirection **301** `/categories` → `/shop/category/<id>-<slug>` (résolution via `product.public.category._ckr_get_explorer_entry_shop_path`, paramètre système optionnel + repli racine), **sans** `ckr_mode` ; titre / breadcrumb **natifs** `website_sale` | **Cible atteinte** *(v19.0.1.3.0)*. Pré-requis ops : au moins une **catégorie publique** racine (sinon repli 301 vers `/shop` nu) |
| **Origines** | `/origines` | **Livrée** (vague B, **19.0.1.4.x**) — **§13** MOA verrouillé ; alias **301** → **`/shop?ckr_mode=origin`** ; filtre **OU**, bandeau, canonical, fiche produit ; [SPEC_IMPL_ORIGINES.md](SPEC_IMPL_ORIGINES.md), [PV_RECETTE_ORIGINES_V1.md](PV_RECETTE_ORIGINES_V1.md) ; stub **retiré** | **`/shop`** + signaux CK — **cible atteinte** (itérations mineures possibles hors scope §13) |
| **Incontournables** *(featured)* | `/incontournables` | **Livrée** (**19.0.1.10.x**) — [2_SHOP.md](../mvp_02/2_SHOP.md), **§4.6** : **301** → **`/shop?ckr_mode=featured`** ; canonical **`/shop?ckr_mode=featured`** ; **`dorevia_ckreyol_marketplace.featured_collection_id`** → **`ckr.shop.collection`** ; fallback **`/shop`** ; bandeau + chip ; priorité **`pack > promo > featured > origin > collection`** ; tests **`dorevia_ckr_collections`**. **Exploitation paramètre** : §4.6 *Exploitation* (migration **19.0.1.10.5**) | **Cible atteinte** *(v19.0.1.10.x)* — exécuter **une fois par base** **`-u dorevia_ckreyol_marketplace`** ≥ **19.0.1.10.5** pour la migration paramètre |

> **Lecture** : les portes **Kits**, **Promotions**, **Catégories** et **Origines** sont **livrées** en module (v19.0.1.1.0 → **19.0.1.4.x** selon porte) — convergence boutique matérialisée (**H1** + `ckr_mode` pour Pack/Promo ; **H1 — cible native** pour Catégories ; **Origines** : **`/origines`** → **301** **`/shop?ckr_mode=origin`**). **Collections** : stub **`/collections`** **transitoire** ; **cadrage + contrat URL + spec impl. + PV recette** **ouverts** ([CADRAGE_FONCTIONNEL_COLLECTIONS.md](CADRAGE_FONCTIONNEL_COLLECTIONS.md), [CONTRAT_URL_COLLECTIONS.md](CONTRAT_URL_COLLECTIONS.md), [SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md), [PV_RECETTE_COLLECTIONS_V1.md](PV_RECETTE_COLLECTIONS_V1.md)) — **impl. module à venir** (§4.2). Capitalisation : [CONTRAT_URL_PROMOTIONS §13.6](CONTRAT_URL_PROMOTIONS.md) ; pour Catégories, la cible 301 est **`/shop/category/…`** — [CONTRAT_URL_CATEGORIES.md §13.1](CONTRAT_URL_CATEGORIES.md).

**Note (UI homepage, hors contrat URL)** : la **mise en scène** des cinq cartes sur l’accueil (rail horizontal, boutons précédent/suivant, **sans autoplay**, accessibilité, rythme vertical avec le hero) est documentée dans **[WIREFRAME_HOMEPAGE.md](../direction/WIREFRAME_HOMEPAGE.md)** — Bloc 3, sous-section *Présentation front (implémentation)*. Le présent document reste centré sur les **liens** et le **comportement boutique** des portes.

---

## 1. Légende — Standard Odoo, construction CK, transitoire

| Tag | Signification |
|-----|----------------|
| **Standard Odoo** | Mécanisme fourni par **Odoo 19 CE** (`website_sale`, eCommerce, prix, catégories publiques, attributs, etc.) sans logique métier parallèle dans le module CK. |
| **Brique OCA installée** | Module **OCA** adopté comme socle (ex. **`product_pack`**) : sa **source de vérité produit** (champ, modèle, onglet back-office) est traitée à l’égal d’un standard tant que la brique reste installée et supportée. La construction CK s’y limite à la **couche navigation / présentation** sur le site. |
| **Construction CK** | Extension **dorevia_ckreyol_marketplace** (ou module CK dédié) : contrôleur, domaine produit, champs, modèles, ou convention d’URL **non** entièrement couverte par le seul clic utilisateur sur l’UI standard boutique. |
| **Transitoire** | Comportement ou artefact **temporaire** (stub CMS, lien nu `/shop`, paramètre non encore interprété) en attendant la matrice données et le contrat d’URL figés. **À retirer ou rediriger** une fois la porte « réelle ». |

---

## 2. Principes transverses (toutes portes)

1. **Cible unique** : la **liste produits** de la boutique (`website_sale`) sur **`/shop`** (y compris les variantes de chemin **nativement** supportées par Odoo pour la catégorie, ex. `/shop/category/...` si retenu).
2. **Cohérence** : le **domaine** `product.template` (et variantes si applicable) affiché pour une porte doit être **le même** que celui obtenu en reproduisant l’action équivalente depuis la boutique (pas deux définitions divergentes).
3. **Contrat d’URL** : pour chaque porte, une **convention stable** (chemin + paramètres autorisés), documentée, **whitelist** côté serveur pour les paramètres CK éventuels.
4. **Combinaisons** : règles explicites avec `search`, `page`, `order`, facettes `attrib` (compatibilité, refus, ou sémantique définie).
5. **Références invalides** : ID ou slug inconnu / non publié → comportement défini (ex. **302** vers `/shop` nu + message, ou **404** « soft » avec CTA boutique).
6. **SEO** : si plusieurs URLs mènent au même jeu de produits, stratégie **canonical** ou consolidation à documenter.
7. **Analytics** : traçabilité par porte (ex. `utm_medium=explorer` + clé de mode) sans collision avec les paramètres métier.

---

## 3. Priorisation validée (vagues)

| Vague | Portes (grille interne / libellé visiteur) | Objectif |
|-------|--------|----------|
| **A** | **Catégories**, **Promotions**, **Pack** *(front : **Kits**)* | Première livraison **à forte dose de standard Odoo / OCA installé** ; source de vérité déjà cadrée (standard Odoo pour Catégories & Promotions ; `product_pack` pour la porte Pack). Réduit le risque de dette technique. |
| **B** | **Origines** | **Livrée** — **§13** + impl. module (voir [SPEC_IMPL_ORIGINES.md](SPEC_IMPL_ORIGINES.md), [PV_RECETTE_ORIGINES_V1.md](PV_RECETTE_ORIGINES_V1.md)). |
| **C** | **Collections** | **Cadrage** + **[CONTRAT_URL_COLLECTIONS.md](CONTRAT_URL_COLLECTIONS.md)** + **[SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md)** + **[PV_RECETTE_COLLECTIONS_V1.md](PV_RECETTE_COLLECTIONS_V1.md)** : **prêts impl. v1 — zéro résidu** (MOA 2026-04-22) ; priorité **`ckr_mode`** figée (**`pack > promo > origin > collection`**) ; **impl. module** en ouverture (§4.2). |

*Note de phasage* : la porte **Pack** (front **Kits**) rejoint la **vague A** depuis le recadrage 2026-04-21 (adossement au module OCA `product_pack` installé ; case *« Est un pack ? »* et onglet *Pack* vérifiés en back-office). Le reste à trancher pour cette porte ne concerne plus la **source de vérité** — désormais actée — mais le **contrat d’URL** et la **traduction front**.

**Séquence (décision 2026-04-22, mise à jour après livraison Origines)** : vague **A** déployée → vague **B** (**Origines**) **livrée** → vague **C** (**Collections**) : **cadrage** + **[CONTRAT_URL_COLLECTIONS.md](CONTRAT_URL_COLLECTIONS.md)** + **[SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md)** + **[PV_RECETTE_COLLECTIONS_V1.md](PV_RECETTE_COLLECTIONS_V1.md)** **prêts impl. v1 — zéro résidu** (priorité **`ckr_mode`** figée **`pack > promo > origin > collection`**) ; **implémentation** en ouverture (§4.2, §4.5).

---

## 4. Fiche par porte (matrice d’implémentation)

Les colonnes suivantes sont le **contrat de complétion** avant autorisation de développement sur `/shop`.

### 4.1 Promotions

**Décision actée (2026-04-21)** : la porte **Promotions** est **adossée au standard Odoo**. Elle **ne** doit **pas** être traitée par défaut comme une **construction CK** à inventer pour modéliser « la promotion ». Le socle retenu sur l’instance est celui des fonctionnalités **eCommerce** déjà activées côté standard, en particulier **Remises, Fidélité & Cartes-cadeaux** et **Listes de prix** (règles de prix, avantages visibles sur le site selon paramétrage Odoo).

La suite du travail n’est donc plus « comment modéliser la promotion », mais **comment traduire proprement dans le front et sur `/shop`** ce que le standard expose déjà (prix, contexte liste de prix, signaux type comparaison / rubans, programmes fidélité & cartes-cadeaux selon périmètre web), conformément à [ADR-CKR-001](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-001) (**standard d’abord**). Une **construction CK** n’intervient qu’**après** constat documenté que le **standard ne suffit pas** pour l’intention « porte Explorer » (ex. libellé contextuel, lien stable reproductible, mise en avant visuelle) — et alors de façon **minimale**, sans dupliquer la logique métier des remises ou des listes de prix.

#### Traçabilité technique (build Odoo 19 — sans réouverture de décision)

Le libellé **Apps** (ex. *Remises, Fidélité & Cartes-cadeaux*) correspond côté code, sur un build **Odoo 19** standard, aux briques suivantes — **à confirmer une fois** sur votre base via **Apps** (recherche par nom technique) si le dépôt ne versionne pas le manifest racine du projet :

| Brique fonctionnelle (tel que paramétré sur l’instance) | Nom technique usuel (module) | Rôle / modèles utiles (rappel) |
|--------------------------------------------------------|-------------------------------|--------------------------------|
| **Remises, Fidélité & Cartes-cadeaux** | **`sale_loyalty`** | Programmes de remise, fidélité, eWallet / cartes-cadeaux ; intégration au flux vente (et au **site** lorsque les programmes s’y appliquent). Documentation officielle : [Remises et fidélité](https://www.odoo.com/documentation/19.0/applications/sales/sales/products_prices/loyalty_discount.html), [eWallets et cartes-cadeaux](https://www.odoo.com/documentation/19.0/applications/sales/sales/products_prices/ewallets_giftcards.html). |
| **Listes de prix** | **`product`** (+ chaîne **`sale`** / **`website_sale`** selon contexte) | **`product.pricelist`** et **`product.pricelist.item`** (règles) ; le **site** e-commerce s’appuie sur **`website_sale`** pour afficher les **prix** cohérents avec la liste de prix du site / du visiteur. |

**Note** : cette table sert uniquement la **traçabilité** (revue technique, onboarding). Elle **ne modifie pas** la décision de fond : socle promo = **standard Odoo** ; points ouverts = **contrat d’URL**, **contexte visible sur `/shop`**, **comportement de lecture visiteur** (liste *Points restants à trancher* en fin de §4.1).

| Champ | Contenu |
|--------|---------|
| **Libellé front** | **Promotions** |
| **Cible** | Liste boutique **`/shop`** avec une **lecture visiteur** filtrée sur les produits effectivement réduits par la pricelist courante (source de vérité **A2** — [CONTRAT_URL_PROMOTIONS §5](CONTRAT_URL_PROMOTIONS.md)). |
| **URL visible visiteur** | **`/promotions`** (carte Explorer, liens extérieurs, bookmarks). |
| **Contrat d’URL** | **Acté et déployé (2026-04-21, v19.0.1.2.0) — Hybride H1** ([CONTRAT_URL_PROMOTIONS.md §12-13](CONTRAT_URL_PROMOTIONS.md)). URL visiteur **`/promotions`** → **redirection HTTP 301** vers URL technique canonique **`/shop?ckr_mode=promo`**. `<link rel="canonical">` pointe sur `/shop?ckr_mode=promo`. Paramètre CK **`ckr_mode`** whitelisté, valeurs autorisées : `{"pack", "promo"}`. Compatibilité préservée avec `search`, `order`, `page`, `attrib`. |
| **Source de vérité** | **Standard Odoo — A2 : `product.pricelist.item` actif strictement réducteur** sur la pricelist courante du visiteur. Résolu par `product.pricelist._ckr_get_promo_template_ids` (bornes dates ouvertes ou englobantes, rejet des items neutres / mark-ups, résolution `applied_on` `0_product_variant` / `1_product` / `2_product_category`, sentinel `None` pour `3_global`). Aucun second marqueur « promo » parallèle côté CK. |
| **Mécanisme Odoo ou CK** | **Standard Odoo** pour le **cœur promotionnel** (moteur de prix `product.pricelist` / `product.pricelist.item`). **Construction CK minimale** : (1) contrôleur `WebsiteSaleCKR` (whitelist `ckr_mode=promo`, extension domaine via `ckr_promo_only`) ; (2) alias `/promotions` → 301 (`WebsiteSaleCKRAliases`) ; (3) `product.pricelist._ckr_get_promo_template_ids` (résolveur A2) ; (4) `product.template._search_get_detail` étendu ; (5) bandeau visiteur + **état vide dédié** ; (6) canonical injecté via `Website._get_canonical_url`. |
| **Comportement attendu sur `/shop`** | Liste filtrée sur les `product.template` en promotion effective ; bandeau « **Promotions** » + copy contextuelle ; **état vide dédié** (« Aucune offre en cours pour le moment ») si aucune promo active ; pas de liste décorative ; pas de seconde vitrine commerciale. |
| **Statut de maturité** | **Déployée (v19.0.1.2.0)** — source de vérité **actée** (A2 pricelist datée), **contrat d’URL acté** et **implémenté**, **filtrage E2E vérifié**, bandeau et état vide **opérationnels**. Pré-requis ops confirmé : activation du groupe `product.group_product_pricelist` (fait le 2026-04-21 sur `tenant_o7`). Alimentation en pricelists promotionnelles = **prérogative back-office** non bloquante. |
| **Stub / redirection / filtre réel** | **Aucun stub préexistant à retirer** (contrairement à `/kits` qui avait un `website.page`). La carte Explorer pointait sur `/shop` nu — bascule de `href` vers `/promotions` + route contrôleur d’alias = **suffisant**. Aucune donnée XML à nettoyer. |

**Tag synthèse** : **Standard Odoo** (cœur — `product.pricelist.item`) + **Construction CK minimale** (couche navigation / présentation / résolveur A2) — **Déployée**.

**Points restants à trancher (hors remise en cause du socle)** :

1. ~~**§A Source de vérité**~~ → **Acté le 2026-04-21** : A2 (pricelist datée avec remise).
2. ~~**§B Contrat d’URL**~~ → **Acté le 2026-04-21** : Hybride H1 + `ckr_mode=promo`.
3. ~~**Contexte visible sur `/shop`**~~ → **Livré** : bandeau `ckr_shop_promo_banner` + copy contextuelle + variante `--empty`.
4. ~~**Comportement de lecture**~~ → **Livré** : filtre posé via `_search_get_detail` (même point d’extension que Pack).
5. **Extension A3 (loyalty `program_type='promotion'`)** : hook ouvert (commenté dans `product_pricelist.py`) ; pas livré en v19.0.1.2.0 — à ré-examiner si le back-office exprime le besoin de promos par règle (ex. *-10 % sur tous les épices*) plutôt que par item pricelist.

---

### 4.2 Collections

**Référence fonctionnelle de départ (versionnée)** : [CADRAGE_FONCTIONNEL_COLLECTIONS.md](CADRAGE_FONCTIONNEL_COLLECTIONS.md) — définition marketing / thématique, règle de visibilité (**Active** + **période de validité** optionnelle), vocabulaire (**titre affiché**, **slug**). **Suite du chantier** : [CONTRAT_URL_COLLECTIONS.md](CONTRAT_URL_COLLECTIONS.md) + [SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md) + [PV_RECETTE_COLLECTIONS_V1.md](PV_RECETTE_COLLECTIONS_V1.md) ; **dev** en ouverture (**zéro résidu documentaire** — priorité **`ckr_mode`** figée **`pack > promo > origin > collection`**, [SPEC_IMPL §5.1](SPEC_IMPL_COLLECTIONS.md#51-constantes-alignement-packs--promos--origines--priorité-ckr_mode-figée-moa-2026-04-22)).

**Cadrage acté (2026-04-22) — documents de suite ouverts**

1. **Constat standard / OCA** : dans **Odoo 19 CE** (`website_sale`), il n’existe **pas** d’entité e-commerce **native centrale** « collection » **équivalente** à une **`product.public.category`** (famille de catalogue) ni à un mécanisme **promotionnel** adossé au moteur de prix (`product.pricelist` / `product.pricelist.item`) tel que cadré pour la porte Promotions. Les regroupements du type « sélection éditoriale / saison / thème » relèvent de **conventions métier** ou d’**extensions**, pas d’un modèle unique livré avec le socle boutique.
2. **OCA** : à ce stade, **aucune brique OCA de référence** n’est **actée** chez C-Kreyol pour ce besoin précis (à distinguer de `product_pack` pour la porte Pack).
3. **Écosystème tiers** : les modules du type « collection page » / vitrines curées hors schéma standard relèvent en général de **solutions tierces** ; hors périmètre tant qu’une **contre-indication argumentée** (brique existante, périmètre, maintenance, alignement [ADR-CKR-001](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-001)) n’est pas produite.

**Posture par défaut** : sauf **décision documentée** de réutiliser une brique standard ou OCA **réellement adaptée**, la porte **Collections** est traitée comme **objet éditorial / métier propre à CK** (modèle de données dédié, rattachement produit explicite). **Séquence** : la porte **Origines** (vague B) est **livrée** ; la vague **C** porte désormais sur **l’implémentation** — **doc complète et zéro résidu** ([CONTRAT_URL_COLLECTIONS.md](CONTRAT_URL_COLLECTIONS.md) **§13** tout coché, [SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md) **§5.1** figée).

**État chantier (2026-04-22)** : la porte **Origines** est **cadrée et livrée**. **Collections** : [CADRAGE_FONCTIONNEL_COLLECTIONS.md](CADRAGE_FONCTIONNEL_COLLECTIONS.md), [CONTRAT_URL_COLLECTIONS.md](CONTRAT_URL_COLLECTIONS.md), [SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md) et [PV_RECETTE_COLLECTIONS_V1.md](PV_RECETTE_COLLECTIONS_V1.md) (**RC-01…RC-14**, preuves **`dorevia_ckr_collections`**) sont **prêts implémentation v1** — **zéro résidu documentaire** : priorité **`ckr_mode`** figée **`pack > promo > origin > collection`** (**§13** contrat + [SPEC_IMPL §5.1](SPEC_IMPL_COLLECTIONS.md#51-constantes-alignement-packs--promos--origines--priorité-ckr_mode-figée-moa-2026-04-22)). **Implémentation** en ouverture ; non-régression portes livrées **testée** par `TestCkrCollectionsPVModel.test_ckr_col_rc14_effective_mode_priority` + `TestCkrCollectionsPVHttp.test_ckr_col_rc14_regression_other_gates`.

| Champ | Contenu |
|--------|---------|
| **Libellé front** | **Collections** |
| **Cible** | **`/shop`** avec lecture **orientée collection** (sélection éditoriale / curatoire). |
| **Contrat d’URL** | **Prêt impl. v1 — zéro résidu** : [CONTRAT_URL_COLLECTIONS.md](CONTRAT_URL_COLLECTIONS.md) — **URLs nobles** + **S1** ; **repli union A** ; **302** + flash / session ; **copies minimales** **et** **priorité `ckr_mode`** (**`pack > promo > origin > collection`** — [SPEC_IMPL §5.1](SPEC_IMPL_COLLECTIONS.md#51-constantes-alignement-packs--promos--origines--priorité-ckr_mode-figée-moa-2026-04-22)) : **figés** (MOA 2026-04-22). |
| **Source de vérité** | *À trancher.* **Par défaut** : **construction CK** — lier chaque collection visible à un **ensemble de produits** identifiable en base. |
| **Mécanisme Odoo ou CK** | **Construction CK** **probable** (véhicule + domaine). Sous-option **Standard** résiduelle : uniquement si chaque collection = **sous-arbre** `product.public.category` **sans** sémantique éditoriale supplémentaire (rare en pratique pour l’intention « collection »). |
| **Comportement attendu sur `/shop`** | Liste filtrée ; titre / breadcrumb alignés sur la collection ; pas de second catalogue HTML parallèle. |
| **Statut de maturité** | **Contrat d’URL**, **spec d’impl.** et **PV recette v1** : **prêts impl. — zéro résidu** (MOA 2026-04-22 — priorité **`ckr_mode`** figée **`pack > promo > origin > collection`**). **Impl. module** : **en ouverture**. **Posture** : CK éditorial par défaut. |
| **Stub / redirection / filtre réel** | Page CMS **`/collections`** (stub) = **transitoire** jusqu’aux **routes CK** et au retrait ordonné du stub (patron cleanup **Origines** / **Kits**). |

**Tag synthèse** : **Construction CK** (posture par défaut) — **Standard Odoo** (cas exceptionnel catégorie pure uniquement).

---

### 4.3 Pack *(libellé visiteur : Kits)*

**Décision actée (2026-04-21)** : la **source de vérité** de la porte 5 est **la logique Pack** (module OCA **`product_pack`**, case *« Est un pack ? »* = `pack_ok`, onglet *Pack*). Le **libellé visiteur** est **Kits** (règle de bi-lexique [ADR-CKR-008](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008) — plus naturel dans l’univers alimentaire : *kit colombo*, *kit apéritif*, *kit découverte*). Ce document utilise **Pack** pour tout ce qui est technique / implémentation, et **Kits** pour tout ce qui est libellé visiteur / URL visible. L’ancienne doctrine interne « composition / assemblage » n’est plus retenue. Conformément à [ADR-CKR-001](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-001) (**standard d’abord**) et à la légende §1, la porte est classée comme **adossée à une brique OCA installée** : la **source de vérité** (quels produits sont « pack ») est portée par Odoo / `product_pack`, la **construction CK** se limite à la couche **navigation / présentation** sur `/shop` et à la porte Explorer.

#### Traçabilité technique (build Odoo 19 — sans réouverture de décision)

| Brique fonctionnelle (back-office) | Nom technique (module) | Rôle / modèles utiles |
|-------------------------------------|------------------------|-----------------------|
| Case **« Est un pack ? »** sur la fiche produit + onglet **Pack** | **`product_pack`** (OCA — branche `19.0`) | Champ booléen **`pack_ok`** sur `product.template` (libellé *« Is Pack? »*). Champs secondaires pour le comportement commande / fiche : `pack_type` (`detailed` / `non_detailed`), `pack_component_price` (`detailed` / `totalized` / `ignored`). Modèle **`product.pack.line`** (composants et quantités) accessible via `product.template.pack_line_ids` (relation vers `product.product.pack_line_ids`). Méthode **`_is_pack_to_be_handled()`** = combinaison de `pack_ok` + `pack_type` + contexte (utile back-office / vente, **pas** pour le filtrage boutique simple). Sert de **source de vérité produit** pour distinguer un pack d’un article simple. |

**Note** : la table sert la **traçabilité**. La décision de fond (socle = `product_pack`) n’est **pas** réouverte ; les points restants concernent le **contrat d’URL**, la **traduction front** sur `/shop` et le **comportement de lecture** (détails en fin de §4.3).

| Champ | Contenu |
|--------|---------|
| **Libellé visiteur (front)** | **Kits** — règle de bi-lexique [ADR-CKR-008](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008). Utilisé dans la section Explorer, les URL visibles et la copy marketing ; stub CMS **`/kits`** **retiré** (alias **301** actif). |
| **Grille interne (doctrine / source de vérité)** | **Pack** — module OCA `product_pack`. Utilisé dans les specs, le code, les paramètres CK internes, les requêtes domaine. |
| **Cible** | **`/shop`** avec lecture **orientée pack** (coffrets, assortiments, multi-produits groupés, portés par `pack_ok=True`). |
| **URL visible visiteur** | **`/kits`** (aligné libellé front). |
| **Contrat d’URL** | **Acté (2026-04-21) — Hybride H1** ([CONTRAT_URL_PACKS.md §12](CONTRAT_URL_PACKS.md)). URL visiteur **`/kits`** → **redirection HTTP 301** vers URL technique canonique **`/shop?ckr_mode=pack`**. `<link rel="canonical">` pointe sur `/shop?ckr_mode=pack`. Paramètre CK **`ckr_mode`** whitelisté, valeur autorisée en phase courante : `{"pack"}`. Compatibilité préservée avec les filtres natifs `search`, `order`, `page`, `attrib`. |
| **Source de vérité** | **Brique OCA installée** — module **`product_pack`** : `product.template.pack_ok` (booléen principal *« Is Pack? »*) + `pack_line_ids` (composants). Pas de second marqueur « pack » parallèle côté CK. |
| **Mécanisme Odoo ou CK** | **Brique OCA installée** pour la **source de vérité produit**. **Construction CK** **minimale** : (1) contrôleur héritant `WebsiteSale` qui interprète `ckr_mode=pack` et étend le domaine avec `("pack_ok", "=", True)` ; (2) contrôleur alias `/kits` → redirection 301 ; (3) rendu du titre / surtitre / breadcrumb visiteur « **Kits** » quand `ckr_mode=pack` est actif ; (4) injection du `canonical` ; (5) éventuelle mise en avant des **lignes de pack** sur la fiche produit si le visuel natif `product_pack` ne suffit pas (décision ultérieure). |
| **Comportement attendu sur `/shop`** | Liste filtrée **`pack_ok=True`** ; titre / breadcrumb cohérents avec « **Kits** » côté visiteur ; cohérence avec la **fiche produit** (affichage des composants selon `pack_type` / `pack_component_price`) ; pas de second catalogue HTML parallèle. |
| **Statut de maturité** | **Déployée (v19.0.1.1.0)** — source de vérité **actée** (OCA installé, champ `pack_ok`), **contrat d’URL acté** et **implémenté** (H1 + `ckr_mode=pack`, alias **301**, stub retiré). **Reliquat** : affichage des **`pack_line_ids`** sur la fiche produit (points §4.3 ci-dessous). |
| **Stub / redirection / filtre réel** | **Livré** : **`/kits`** → **redirection 301** vers **`/shop?ckr_mode=pack`** ; `website.page` stub **retirée** (`data/ckr_cleanup_kits_stub.xml`). |

**Tag synthèse** : **Brique OCA installée** (**décision actée** — `product_pack`) — **Construction CK** **minimale** réservée à la couche **navigation / présentation** sur `/shop` et à l’entrée Explorer.

**Points restants à trancher (hors remise en cause du socle `product_pack`)** :

1. ~~**Contrat d’URL**~~ → **Acté le 2026-04-21** : Hybride H1 + `ckr_mode=pack` ([CONTRAT_URL_PACKS.md §12](CONTRAT_URL_PACKS.md)).
2. **Traduction front sur `/shop?ckr_mode=pack`** : libellé exact du titre / surtitre « Kits », fil d’Ariane CK (faut-il un niveau dédié ou juste un surtitre au-dessus de la liste ?), message court introduisant la porte, état vide (aucun produit `pack_ok=True` publié sur le site).
3. **Comportement de lecture** : niveau de mise en avant des **composants** (`pack_line_ids`) côté fiche produit — natif `product_pack` suffisant ou habillage CK additionnel (bloc « contenu du kit » avec visuels, quantités mises en forme) ?
4. ~~**Statut du stub `/kits`**~~ → **Acté** : devient une **redirection 301** portée par le contrôleur CK vers `/shop?ckr_mode=pack` ; la `website.page` stub `website_page_compositions` est **retirée** (ou dépubliée) lors de la même vague d’implémentation, avec un ordre de déploiement **contrôleur d’abord, stub ensuite** pour éviter tout 404.

---

### 4.4 Catégories

| Champ | Contenu |
|--------|---------|
| **Libellé front** | **Catégories** |
| **Cible** | Liste boutique en **lecture par famille de produits** : URL native **`/shop/category/<id>-<slug>`** (contrôleur `website_sale` — même univers commercial que `/shop`). |
| **URL visible visiteur** | **`/categories`** (carte Explorer, liens courts). |
| **Contrat d’URL** | **Acté et déployé (2026-04-22, v19.0.1.3.0) — Hybride H1, cible native** ([CONTRAT_URL_CATEGORIES.md §12-13](CONTRAT_URL_CATEGORIES.md)). **`/categories`** → **redirection HTTP 301** vers **`/shop/category/<id>-<slug>`** (slug via **`env["ir.http"]._slug(category)`**, aligné `website_sale`). **Pas** de paramètre **`ckr_mode`** : le filtre produit reste **100 % standard** ; pas d’override `website._get_canonical_url` CK sur cette porte (canonical = comportement natif Odoo sur la page catégorie). Query params entrants **préservés** sauf **`ckr_mode`** (retiré à la volée pour éviter un mélange avec les modes Pack/Promo). |
| **Source de vérité** | **`product.public.category`** + rattachements **`product.template`** / site tels que gérés par Odoo. |
| **Mécanisme Odoo ou CK** | **Standard Odoo** pour tout le filtrage et l’UI (breadcrumb, sidebar). **Construction CK minimale** : (1) résolution déterministe de la catégorie d’entrée `product.public.category._ckr_get_explorer_entry_shop_path(website)` — paramètre **`dorevia_ckreyol_marketplace.explorer_public_category_id`** (`ir.config_parameter`) si entier valide pour le site, sinon **première racine** (`parent_id` absent, domaine site, ordre `sequence, id`) ; (2) route **`/categories`** → 301 dans `WebsiteSaleCKRAliases` ; (3) data `ckr_explorer_category_parameter.xml` (valeur initiale `0` = laisser le repli automatique). |
| **Comportement attendu** | Même expérience qu’un accès direct à la catégorie depuis le menu boutique : fil d’Ariane et titre **natifs** ; pas de bandeau CK redondant « Catégories ». **Repli** : si aucune catégorie publique n’existe → **301** vers **`/shop`** nu (variante **hub** documentée). |
| **Statut de maturité** | **Déployée (v19.0.1.3.0)** — contrat d’URL acté, résolveur implémenté, carte Explorer basculée vers **`/categories`**. |
| **Stub / redirection / filtre réel** | **Aucun stub CMS** ; entrée **`/categories`** portée **uniquement** par le contrôleur CK (301). |

**Tag synthèse** : **Standard Odoo** (cœur — filtrage catégorie) + **Construction CK minimale** (alias + résolution d’entrée).

**Points restants (hors périmètre de la vague)** : affinage **ops** (choix explicite de la racine d’entrée via le paramètre système si la première racine par `sequence` ne convient pas).

**Note technique (front `/shop`, module ≥ 19.0.1.10.27)** : en **Odoo 19 CE**, `product.public.category` ne fournit plus le helper **`website_url`** utilisé par d’anciens gabarits pour les liens dans la colonne filtres. Le thème CK aligne les `href` des entrées catégorie (sidebar desktop et offcanvas) sur le fragment natif **`website_sale.categorie_link`** : `keep('%s/category/%s' % (shop_path, slug(c)))`, afin d’éviter une erreur serveur sur **`/shop`** lorsque le bloc Catégories est affiché. Détail opérationnel : [TICKET_SHOP_SIDEBAR_CATEGORIES.md](../mvp_02/TICKET_SHOP_SIDEBAR_CATEGORIES.md).

---

### 4.5 Origines

**Séquence (MOA 2026-04-22)** : la vague **A** (Promotions, Kits, Catégories) est **déployée** ; la vague **B** (**Origines**) est **cadrée et livrée** (voir [CONTRAT_URL_ORIGINES.md](CONTRAT_URL_ORIGINES.md), [SPEC_IMPL_ORIGINES.md](SPEC_IMPL_ORIGINES.md)). La vague **C** (**Collections**) enchaîne avec le **cadrage fonctionnel** versionné ([CADRAGE_FONCTIONNEL_COLLECTIONS.md](CADRAGE_FONCTIONNEL_COLLECTIONS.md)), le [CONTRAT_URL_COLLECTIONS.md](CONTRAT_URL_COLLECTIONS.md), la [SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md) et le [PV_RECETTE_COLLECTIONS_V1.md](PV_RECETTE_COLLECTIONS_V1.md) — **implémentation** en ouverture (**zéro résidu documentaire** ; priorité **`ckr_mode`** figée **`pack > promo > origin > collection`**) (§4.2).

#### Décision de fond — dimension éditoriale

**Acté** : **Origines** ne doit **pas** être réduite à un **simple tag technique** ni à une **métadonnée de fiche produit** sans portée visiteur. L’intention produit est une **porte d’accès de navigation** avec **portée de lecture** et **mise en scène** côté site — comparable en *niveau d’ambition* à une entrée Explorer « digne de ce nom » (contexte visible, signification, cohérence avec la charte CK), et **non** à un critère de filtrage discret seul.

**Précision MOA (formulation 2026-04-22)** : (1) la dimension **éditoriale** doit être **opérationnalisée** dans les livrables (obligations vérifiables, pas seulement une formule d’intention) ; (2) l’entrée par **Origines** ne doit **pas** se limiter à l’activation **silencieuse** d’un filtre catalogue — le visiteur doit disposer d’un **contexte de lecture visible et compréhensible**. Détail : [CONTRAT_URL_ORIGINES.md](CONTRAT_URL_ORIGINES.md) §2 et §3.

**Double question** (le cadrage technique devra traiter les **deux** explicitement) :

1. **Données** : comment disposer d’une base **exploitable** côté produits (rattachement fiable, multi-valeurs éventuelles, cohérence catalogue / site) en restant **sobre** si possible ([ADR-CKR-001](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-001) — standard d’abord lorsqu’un mécanisme natif suffit).
2. **Expérience** : comment faire d’**Origines** une porte **lisible, signifiante et éditorialement exploitable** pour le visiteur sur **`/shop`** (et au-delà : évolutivité front **sans plafonner** la richesse future — bandeaux, copy, jalons visuels, etc.).

**Critères d’arbitrage pour la solution retenue** (orientations MOA) :

* **Backend** : préférer la **sobriété** et la **traçabilité** ; éviter la sur-ingénierie si un socle standard (ex. attribut e-commerce / facettes) couvre partiellement le besoin **sans** suffire à la dimension éditoriale — alors **complément CK** ciblé plutôt que duplication métier.
* **Front** : la livrable ne peut pas se limiter à « un facet invisible » ; il faut prévoir dès le cadrage les **signaux éditoriaux** (titre, intro, état vide éventuel, cohérence avec les autres portes Explorer).
* **Évolutivité** : laisser **ouverte** une montée en richesse (contenus, visuels, parcours) **sans** remettre en cause le modèle de données au premier enrichissement front.

Le document **[CONTRAT_URL_ORIGINES.md](CONTRAT_URL_ORIGINES.md)** porte le **verrouillage MOA** (**§13**). La **[SPEC_IMPL_ORIGINES.md](SPEC_IMPL_ORIGINES.md)** et le **[PV_RECETTE_ORIGINES_V1.md](PV_RECETTE_ORIGINES_V1.md)** ont porté l’**implémentation livrée** (résidu **§12** clos pour la v1 livrée). **Patron de convergence** `/shop` ([ADR-CKR-007](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007)).

| Champ | Contenu |
|--------|---------|
| **Libellé front** | **Origines** |
| **Cible** | **`/shop`** avec lecture **orientée origine** (repère géographique / territorial) **et** couche **éditoriale** visible (portée de lecture / mise en scène — pas seul filtre discret). |
| **Contrat d’URL** | **Acté et déployé** — **Hybride H1** : **`/origines`** → **301** → **`/shop?ckr_mode=origin`** ; paramètres **`ckr_origin`** répétables (**OU**) ; repli **302** **`/shop`** nu si référence invalide (**§13.9**). Détail : [CONTRAT_URL_ORIGINES.md](CONTRAT_URL_ORIGINES.md) **§5**, **§12–§13**. |
| **Source de vérité** | **Verrouillé** (**§13.3**) : donnée **structurée multi-valeurs** ; **pas** tag libre final, **pas** champ texte faible, **pas** modèle lourd v1 sans besoin ; **A1** prioritaire, **A2** si insuffisance documentée. Doctrine **§4.0** inchangée en intention. |
| **Mécanisme Odoo ou CK** | **A1** (attribut e-commerce) **ou** **A2** (léger) pour le **socle** ; **CK** pour **projection** (**§3.1**, bandeau, fiche produit — **§13.4–§13.7**). |
| **Comportement attendu sur `/shop`** | Liste avec filtre **OU** si multi-sélection (**§13.2**) ; **signal minimal §3 + §3.1** ; **état vide dédié** + rebonds (**§13.10**) ; **repli** `/shop` nu si référence invalide (**§13.9**) ; **non** grille indiscernable (**§2.2**). |
| **Statut de maturité** | **Livrée** (module **19.0.1.4.x**) — **§13** métier verrouillé ; **impl.** déployée (profils **`ckr.shop.origin`**, hooks, canonical, bandeau, fiche produit). Évolutions futures : hors réouverture **§13** sans MOA écrite. |
| **Stub / redirection / filtre réel** | **Stub retiré** ; alias **`/origines`** → **301** **`/shop?ckr_mode=origin`** (cleanup data — voir [SPEC_IMPL_ORIGINES.md](SPEC_IMPL_ORIGINES.md)). |

**Tag synthèse** : **Standard Odoo** *lorsque utile pour la donnée produit* — **Construction CK** *pour la portée navigation / éditoriale* — **sans** réduction à un tag anonyme.

---

### 4.6 Incontournables *(sélection éditoriale — `ckr_mode=featured`)*

**Référence MOA / UX** : **[2_SHOP.md](../mvp_02/2_SHOP.md)** — §5 *Porte Incontournables — spécification cible (impl.)* (principe, transparence des libellés, micro-copy, non-objectifs).

**Statut** : **livrée** en module (**19.0.1.10.x**) — recette technique + tests **`dorevia_ckr_collections`** ; **clôture exploitation** paramètre système en **19.0.1.10.5** (voir *Exploitation* ci-dessous). **Ticket dev** : [TICKET_INCONTOURNABLES_SHOP_FEATURED_MVP22.md](../crea/TICKET_INCONTOURNABLES_SHOP_FEATURED_MVP22.md).

#### Principe

La porte **Incontournables** expose une **sélection éditoriale manuelle** de produits. Elle **ne correspond pas** à un classement statistique des ventes.

#### URL

- **URL courte visiteur** : `/incontournables`
- **Redirection** : **301** vers `/shop?ckr_mode=featured`
- **URL canonique** : `/shop?ckr_mode=featured`

#### Source de vérité

**Collection éditoriale** **`ckr.shop.collection`**, configurée **par site** via le paramètre système :

`dorevia_ckreyol_marketplace.featured_collection_id`

**Interdit** : second mécanisme parallèle (pas de duplication de la logique collection hors **`ckr.shop.collection`**). **Interdits** tant qu’aucun calcul réel sur ventes confirmées : slugs / modes du type **`best_sellers`**, **`top_sales`**.

#### Comportement attendu

Si le paramètre est **renseigné** et pointe vers une collection **active** :

- la grille sur `/shop?ckr_mode=featured` affiche les **produits de cette collection** ;
- le **bandeau** utilise le contexte « Incontournables » ;
- la **chip** « Incontournables » est **active**.

Si le paramètre est **absent**, **invalide** ou pointe vers une collection **inactive** :

- **fallback** vers `/shop` (boutique générique) ;
- **aucun faux contenu** ;
- **message discret** possible si aucune sélection n’est disponible (copy / recette).

#### Priorité multi-modes

**Priorité figée** (impl. + tests **`dorevia_ckr_collections`**, RC-14) :

`pack > promo > featured > origin > collection`

> **Lecture** : la porte **Collections** (URLs nobles) reste **en dernier** dans cette chaîne lorsque **`ckr_mode`** est utilisé ; réf. [SPEC_IMPL_COLLECTIONS §5.1](SPEC_IMPL_COLLECTIONS.md#51-constantes-alignement-packs--promos--origines--priorité-ckr_mode-figée-moa-2026-04-22) pour le contexte historique **`pack > promo > origin > collection`** avant l’introduction de **`featured`**.

| Champ | Contenu |
|--------|---------|
| **Libellé front** | **Incontournables** (prioritaire) ; variante **Notre sélection** ([2_SHOP.md](../mvp_02/2_SHOP.md)). |
| **Cible** | **`/shop?ckr_mode=featured`** avec lecture filtrée sur les produits de la collection désignée par **`featured_collection_id`**. |
| **URL visible visiteur** | **`/incontournables`** (carte Explorer, liens courts — lorsque câblé). |
| **Contrat d’URL** | **Cible MOA (2026-04-25)** — **Hybride H1** (même famille que `/promotions`, `/kits`, `/origines`) : **`/incontournables`** → **redirection HTTP 301** vers **`/shop?ckr_mode=featured`** ; **`<link rel="canonical">`** sur `/shop?ckr_mode=featured`. Paramètre CK **`ckr_mode`** : valeur **`featured`** à **whitelist** côté serveur. **Contrat détaillé / recette** : extension **`mvp_01`** (document dédié ou section contrat) + mise à jour des renvois dans le présent fichier lors de l’impl. |
| **Source de vérité** | **`ckr.shop.collection`** référencée par **`dorevia_ckreyol_marketplace.featured_collection_id`** (`ir.config_parameter`, par site / `website_id`). |
| **Mécanisme Odoo ou CK** | **Réutilisation** du modèle **`ckr.shop.collection`** et des mécanismes de filtrage catalogue déjà prévus pour les collections (ex. jeux d’IDs template) — **construction CK** : alias 301, interprétation `ckr_mode=featured`, extension **whitelist**, bandeau, chip, fallback, canonical. |
| **Comportement attendu sur `/shop`** | Grille cohérente avec la collection ; bandeau Incontournables ; chip active ; pas de liste décorative hors source de vérité. |
| **Statut de maturité** | **Livrée** (**19.0.1.10.x**) — exploitation paramètre documentée §4.6 *Exploitation*. |
| **Stub / redirection / filtre réel** | **Déployé** : alias **`/incontournables`** (301) ; filtre catalogue via mécanique **Collections** (`ckr_collection_*` / `_search_get_detail`). |

**Tag synthèse** : **Construction CK** (navigation / présentation / paramètre) — **source produit** = **objet CK existant** **`ckr.shop.collection`** (**sans** nouvelle logique parallèle).

**Livrables techniques attendus (ordre logique chiffrage dev)** :

1. Contrôleur / route (`/incontournables`, `WebsiteSaleCKR`, whitelist `featured`).
2. Domaine produit / `_search_get_detail` (réutiliser le lien collection → templates).
3. Canonical / 301 (aligné autres portes H1).
4. Bandeau contextuel QWeb (`ckr_shop.xml` ou équivalent).
5. Chip active (raccourcis boutique).
6. Tests HTTP + **non-régression** multi-modes.

**Note vigilance (dev)** : **`ckr_mode=featured`** ne doit **pas** recoder ni **dupliquer** la logique « collection » (visibilité, appartenance produits, filtre catalogue). Il doit **uniquement consommer** la **`ckr.shop.collection`** désignée par **`dorevia_ckreyol_marketplace.featured_collection_id`**, en **réutilisant** les mécanismes déjà prévus pour les collections sur `product.template` (ex. extension **`_search_get_detail`**, jeux d’IDs template — alignement porte **Collections**). Cela préserve la **sobriété** du module et évite une **deuxième mécanique éditoriale parallèle**.

#### Exploitation — paramètre `featured_collection_id` *(clôture sous-lot **19.0.1.10.5**)*

Pour **ne pas perdre** l’id de collection « Incontournables » configuré en production lors des **`odoo -u dorevia_ckreyol_marketplace`** :

1. **Pas de valeur opérationnelle en XML** — le paramètre **`dorevia_ckreyol_marketplace.featured_collection_id`** n’est **plus** défini dans un fichier **data** du module. Un upgrade **ne réapplique donc pas** une valeur par défaut **`0`** par rechargement XML.
2. **Première installation** — le **`post_init_hook`** crée la clé avec la valeur **`0`** **uniquement si** aucun enregistrement **`ir.config_parameter`** n’existe encore pour cette clé (**aucun écrasement** d’une valeur déjà présente).
3. **Passage module `19.0.1.10.5`** — migration **`pre-migration`** / **`post-migration`** : sauvegarde puis réinjection de la valeur **avant / après** le chargement des data, afin d’éviter toute perte si le retrait de l’ancien XML entraîne un **unlink** côté **`ir.model.data`**.
4. **Obligation exploitation** — exécuter **une fois par base concernée** un **`odoo -u dorevia_ckreyol_marketplace`** (ou équivalent, ex. conteneur Docker) **jusqu’à au moins la version `19.0.1.10.5`**, afin d’appliquer cette migration et le comportement « hors XML ».
5. **Après coup** — la valeur métier (id **`ckr.shop.collection`**) se configure et se maintient comme toute donnée d’exploitation : **Paramètres techniques** → Paramètres système, ou procédure interne équivalente.

---

## 5. Synthèse visuelle — Standard / CK / Transitoire

| Porte (interne / front) | Vague | Standard Odoo / OCA installé | Construction CK | Transitoire (état actuel typique) |
|-------------------------|-------|-------------------------------|------------------|-----------------------------------|
| **Catégories** | A | **Fort (déployé)** — `product.public.category` + `/shop/category/...` natif | **Déployée (v19.0.1.3.0)** — alias `/categories` → **301** vers `/shop/category/<id>-<slug>` (`_ckr_get_explorer_entry_shop_path`), paramètre système optionnel + repli racine / `/shop` nu ([CONTRAT_URL_CATEGORIES.md §12-13](CONTRAT_URL_CATEGORIES.md)) | **Carte → `/categories`** ; repli `/shop` si aucune catégorie publique |
| **Promotions** | A | **Fort (déployé)** — `product.pricelist` / `product.pricelist.item` (groupe `product.group_product_pricelist` actif) | **Déployée (v19.0.1.2.0)** — contrôleur multi-modes `WebsiteSaleCKR` (whitelist `ckr_mode=promo`, extension domaine via `ckr_promo_only`), alias `/promotions` → **301**, résolveur **`product.pricelist._ckr_get_promo_template_ids`** (A2), bandeau visiteur « Promotions » + **état vide dédié**, `canonical` forcé sur `/shop?ckr_mode=promo` ([CONTRAT_URL_PROMOTIONS.md §12-13](CONTRAT_URL_PROMOTIONS.md)) | **Pas de stub** à retirer (lien Explorer basculé de `/shop` → `/promotions`). Reliquat ops : alimentation d’au moins une pricelist datée avec remise (non bloquant — état vide affiché tant que non alimentée) |
| **Pack** *(front : **Kits**)* | A | **Fort (déployé)** — **OCA `product_pack`** installé : `pack_ok`, `pack_line_ids`, onglet Pack | **Déployée (v19.0.1.1.0)** — contrôleur `WebsiteSaleCKR` (héritage `WebsiteSale`, whitelist `ckr_mode=pack`, extension domaine `pack_ok=True`), alias `/kits` → **301** (`WebsiteSaleCKRAliases`), titre visiteur « Kits » (bandeau `ckr_shop_pack_banner`), `canonical` forcé sur `/shop?ckr_mode=pack` via `Website._get_canonical_url` ([CONTRAT_URL_PACKS.md §12](CONTRAT_URL_PACKS.md)) | **Stub `/kits` retiré** (v19.0.1.1.0, `data/ckr_cleanup_kits_stub.xml`). Reliquat : affichage détaillé des `pack_line_ids` sur la fiche produit |
| **Origines** | B (**déployée**) | **A1** (attribut « Origine ») + **CK** `ckr.shop.origin` (**§13.3**) | **Livrée** — contrôleur `ckr_mode=origin`, alias `/origines` 301, filtre OU, canonical, bandeau, fiche produit ([SPEC_IMPL_ORIGINES.md](SPEC_IMPL_ORIGINES.md)) | Stub `/origines` **retiré** (cleanup data) |
| **Collections** | C (**docs ouverts**, **impl. à venir**) | Pas d’entité native « collection » en Odoo 19 CE ; pas d’OCA de référence actée | **Objet CK éditorial** — [CADRAGE_FONCTIONNEL_COLLECTIONS.md](CADRAGE_FONCTIONNEL_COLLECTIONS.md) + [CONTRAT_URL_COLLECTIONS.md](CONTRAT_URL_COLLECTIONS.md) + [SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md) + [PV_RECETTE_COLLECTIONS_V1.md](PV_RECETTE_COLLECTIONS_V1.md) | Stub **`/collections`** **transitoire** jusqu’aux routes nobles |
| **Incontournables** *(featured)* | **MVP2.2** (**SPEC §4.6**, **livrée 19.0.1.10.x**) | **`ckr.shop.collection`** (collection désignée par paramètre site) | **Déployée** — alias **`/incontournables`** → **301** → **`/shop?ckr_mode=featured`** ; filtre (mécanique Collections) ; bandeau + chip ; fallback **`/shop`** ; priorité **`pack > promo > featured > origin > collection`** ([2_SHOP.md](../mvp_02/2_SHOP.md), §4.6) | **Paramètre** `dorevia_ckreyol_marketplace.featured_collection_id` — **exploitation** §4.6 *Exploitation* (**19.0.1.10.5**) ; tests **`dorevia_ckr_collections`** |

---

## 6. Décisions attendues avant développement

*Titre de section conservé pour la continuité du document ; le tableau ci-dessous reflète l’**état courant** du chantier (cohérence 2026-04-22).*

Les lignes suivantes doivent être **complétées et validées** (atelier métier + technique), puis répercutées dans ce document (version + date).

- [x] **Promotions** : ~~mécanisme (standard Odoo acté)~~ → **confirmé** ; ~~source de vérité~~ → **actée** (**A2 — pricelist datée avec remise**, résolveur `product.pricelist._ckr_get_promo_template_ids`) ; ~~contrat d’URL~~ → **acté** (**H1** + `ckr_mode=promo`, canonical `/shop?ckr_mode=promo`, alias `/promotions` 301 — [CONTRAT_URL_PROMOTIONS.md §12-13](CONTRAT_URL_PROMOTIONS.md)) ; ~~implémentation~~ → **déployée (v19.0.1.2.0)** : contrôleur multi-modes, résolveur A2, filtre `_search_get_detail`, canonical, bandeau « Promotions » + **état vide dédié**. **Reste** : alimentation back-office d’au moins une pricelist datée avec remise (pré-requis ops non bloquant). Hook A3 (loyalty `promotion`) ouvert pour extension ultérieure.
- [x] **Pack** (libellé visiteur : **Kits**) : ~~modèle produit~~ → **acté** (**OCA `product_pack`** : `pack_ok`, `pack_line_ids`) ; ~~contrat d’URL~~ → **acté** (H1 + `ckr_mode=pack`, canonical `/shop?ckr_mode=pack`, alias `/kits` 301 — [CONTRAT_URL_PACKS.md §12](CONTRAT_URL_PACKS.md)) ; ~~implémentation~~ → **déployée (v19.0.1.1.0)** : contrôleur, filtre, canonical, bandeau visiteur « Kits », retrait du stub. **Reste** : niveau d’affichage des composants (`pack_line_ids`) sur la fiche produit (décision ultérieure).
- [x] **Catégories** : ~~URL par défaut~~ → **actée** (**H1 — cible native** : `/categories` 301 → `/shop/category/<id>-<slug>` — [CONTRAT_URL_CATEGORIES.md §12](CONTRAT_URL_CATEGORIES.md)) ; ~~implémentation~~ → **déployée (v19.0.1.3.0)** : résolveur `product.public.category._ckr_get_explorer_entry_shop_path`, route `/categories`, paramètre `dorevia_ckreyol_marketplace.explorer_public_category_id`, repli première racine puis `/shop` nu. **Reste** : ajuster le paramètre système en prod si la racine par défaut ne convient pas.
- [x] **Origines** : ~~**§13 MOA verrouillé**~~ → **livré** (module **19.0.1.4.x** — `ckr_mode=origin`, profils `ckr.shop.origin`, tests `dorevia_ckr_origins`, [PV recette](PV_RECETTE_ORIGINES_V1.md) ; résidu **§12** traité via spec + recette).
- [ ] **Collections** : **cadrage** + **contrat URL §13** (coché ; priorité **`ckr_mode`** = **`pack > promo > origin > collection`**) + **[SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md)** + **[PV_RECETTE_COLLECTIONS_V1.md](PV_RECETTE_COLLECTIONS_V1.md)** **prêts impl. v1 — zéro résidu documentaire** (MOA 2026-04-22) ; **impl.** + tests **`dorevia_ckr_collections`** en ouverture ; posture = **objet CK éditorial** (§4.2).
- [x] **Incontournables** (`featured`) : **livrée** (**19.0.1.10.x**) — route **`/incontournables`** → **301** → **`/shop?ckr_mode=featured`** ; paramètre **`dorevia_ckreyol_marketplace.featured_collection_id`** (exploitation **19.0.1.10.5**, §4.6 *Exploitation*) ; whitelist **`featured`** ; bandeau + chip ; fallback **`/shop`** ; priorité **`pack > promo > featured > origin > collection`** ; tests **`dorevia_ckr_collections`** ; ref. **[2_SHOP.md](../mvp_02/2_SHOP.md)**.
- [ ] **Stub** **`/collections`** : **transitoire** jusqu’à impl. routes CK (voir [SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md)) ; **`/origines`** : stub **retiré** (vague B livrée) ; **`/kits`** : stub **retiré** (v19.0.1.1.0).
- [ ] **Sécurité** : validation des `ckr_ref` (site, publication, droits).
- [ ] **SEO / canonical** : règle pour les doublons d’URL.
- [ ] **Analytics** : convention de tracking stable.

---

## 7. Références

- [2_SHOP.md](../mvp_02/2_SHOP.md) — **MVP2.2 Boutique** : UX, doctrine libellés / transparence, **porte Incontournables** (`featured`, `/incontournables`, `featured_collection_id`).
- [ARCHITECTURE_DECISION_RECORD.md](../direction/ARCHITECTURE_DECISION_RECORD.md) — ADR-CKR-006, 007, 008.
- [CONTRAT_URL_ORIGINES.md](CONTRAT_URL_ORIGINES.md) — **§13** verrouillage MOA ; **§12** résidu PV / impl.
- [SPEC_IMPL_ORIGINES.md](SPEC_IMPL_ORIGINES.md) — **spec d’implémentation** v1 (technique, alignée §13 + §12.2).
- [SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md) — **spec d’impl.** porte Collections (routes nobles, S1, modèle CK, résidu contrat §13).
- [CADRAGE_FONCTIONNEL_COLLECTIONS.md](CADRAGE_FONCTIONNEL_COLLECTIONS.md) — **cadrage fonctionnel** porte Collections (définition, visibilité, navigation, slug, etc.).
- [CONTRAT_URL_COLLECTIONS.md](CONTRAT_URL_COLLECTIONS.md) — contrat d’URL Collections : **`/collections`**, **`/collections/<slug>`**, **`/collections/union/…`** (**S1**) ; pas de **`/shop?ckr_mode=collection…`** en référence publique.
- [PV_RECETTE_COLLECTIONS_V1.md](PV_RECETTE_COLLECTIONS_V1.md) — **PV de recette V1** ; cas **RC-01…RC-14** ; exécution **`--test-tags=dorevia_ckr_collections`** (alignement [SPEC_IMPL_COLLECTIONS §12](SPEC_IMPL_COLLECTIONS.md#12-tests-automatisés)).
- [WIREFRAME_HOMEPAGE.md](../direction/WIREFRAME_HOMEPAGE.md) — Bloc 3 Explorer.
- [STRUCTURE_MENU_PRINCIPAL.md](../direction/STRUCTURE_MENU_PRINCIPAL.md) — §11 (Explorer ≠ menu).
- [BRIEF_DEV.md](../direction/BRIEF_DEV.md) — principes d’implémentation front module CK.

---

## Historique du document

| Date | Changement |
|------|------------|
| 2026-04-21 | Création — spécification d’implémentation des portes Explorer vers `/shop` ; phasage A/B/C ; légende Standard Odoo / CK / transitoire ; matrice par porte ; prérequis avant dev. |
| 2026-04-21 | **§4.1 Promotions** : décision **standard Odoo** (listes de prix + remises / fidélité / cartes-cadeaux) ; retrait du postulat « construction CK probable » pour le cœur promo ; maturité rehaussée côté socle ; points restants = URL + signaux visiteur sur `/shop` + CK uniquement si gap front documenté. |
| 2026-04-21 | **§4.1** : ajout encadré **traçabilité technique** — modules **`sale_loyalty`**, **`product`** / chaîne **`website_sale`** (documentation Odoo 19) ; rappel de vérification sur le build ; **sans** réouverture de la décision de fond. |
| 2026-04-21 | **§4.3 Packs** (ex-« Kits ») : recadrage complet — l’ancien libellé et la doctrine interne « composition » sont **retirés** ; porte désormais **adossée à la brique OCA `product_pack`** installée (case *« Est un pack ? »*, onglet *Pack*, `pack_ok`, `pack_line_ids`). Nouvelle catégorie de légende **Brique OCA installée** ajoutée au §1. Phasage : **Packs rejoint la vague A**. Stub **`/packs`** remplace **`/kits`**. Synthèse, checklist et introduction alignées. |
| 2026-04-21 | **§4.3** : rectification de vocabulaire technique après lecture du module OCA `product_pack` — le marqueur principal est le booléen **`pack_ok`** (*« Is Pack? »*) et non `is_pack` ; `pack_type` / `pack_component_price` sont des sélecteurs secondaires ; `pack_line_ids` porte les composants. Ouverture du sujet **contrat d’URL** dans un document comparatif dédié : **[CONTRAT_URL_PACKS.md](CONTRAT_URL_PACKS.md)** (à trancher avant tout développement filtre `/shop`). |
| 2026-04-21 | **§4.3 — règle de bi-lexique** ([ADR-CKR-008](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008)) : titre de la fiche mis en **Pack *(libellé visiteur : Kits)***. Dans tout le document, **Pack** désigne désormais la grille technique / source de vérité, **Kits** désigne le libellé visiteur (URL visible **`/kits`**, copy, titre de carte Explorer). La fiche, la synthèse, la checklist et le phasage sont alignés sur cette dissociation. Ouverture d’un point complémentaire dans [CONTRAT_URL_PACKS.md](CONTRAT_URL_PACKS.md) : choix du nom du paramètre CK (`pack` interne aligné source de vérité vs `kits` aligné front). |
| 2026-04-21 | **Intro — confirmation ferme** de la règle cible [ADR-CKR-007](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007) : **5 portes → `/shop`**, sans exception. Ajout d’un encart **« Règle cible universelle »** en tête et d’un **snapshot** des liens actuels de `ckr_entries.xml` (version 19.0.1.0.29) vs cible — trois stubs transitoires (`/collections`, `/kits`, `/origines`), deux convergences sans contexte (`/shop` nu) pour Promotions & Catégories. |
| 2026-04-21 | **§4.3 — contrat d’URL acté** : **Hybride H1** + paramètre **`ckr_mode=pack`** ([CONTRAT_URL_PACKS.md §12](CONTRAT_URL_PACKS.md)). Lignes « Contrat d’URL », « Mécanisme Odoo ou CK », « Statut de maturité », « Stub / redirection / filtre réel » alignées. Points restants à trancher réduits à la **traduction front**, à **l’affichage des composants** sur la fiche produit, et au **retrait ordonné du stub `/kits`**. Snapshot mis à jour (stub `/kits` = contrat acté, en attente du contrôleur). Synthèse §5 alignée. Checklist §6 : case Pack/Kits cochée ; stubs hors `/kits` dissociés. |
| 2026-04-21 | **§4.1 — ouverture de l’arbitrage Promotions** dans un document comparatif dédié : **[CONTRAT_URL_PROMOTIONS.md](CONTRAT_URL_PROMOTIONS.md)** (à trancher avant tout développement). Deux décisions structurantes exposées : **§A source de vérité** (4 candidats : ribbon `Sale`, pricelist datée, loyalty `promotion`, tag produit — recommandation : **pricelist datée**) et **§B véhicule d’URL** (3 options + hybrides — recommandation : **Hybride H1** par transposition du patron Pack). Checklist §6 Promotions et points restants §4.1 alignés sur le nouveau document. |
| 2026-04-21 | **§4.1 — porte Promotions mise en service** (module **19.0.1.2.0**). Le statut bascule de *contrat à trancher* à *déployé et vérifié*. Arbitrages validés : source de vérité **A2** (pricelist datée avec remise effective) ; véhicule d’URL **H1** (`/promotions` 301 → `/shop?ckr_mode=promo`) ; paramètre CK **`ckr_mode=promo`** ; **état vide dédié** ; pré-requis ops activation du groupe `product.group_product_pricelist` (fait sur `tenant_o7`). Livraisons : `controllers/website_sale_ckr.py` refactoré multi-modes (constantes `CKR_MODE_PROMO`, `CKR_MODES_ALLOWED`, `CKR_MODE_TITLES`, `CKR_ALIAS_MODE` ; whitelist stricte `_ckr_current_mode` ; dispatch par mode dans les hooks `_get_search_options` / `_get_shop_domain` / `_get_additional_shop_values` ; route `/promotions` portée par `WebsiteSaleCKRAliases` via helper `_ckr_redirect` partagé avec `/kits`) ; nouveau `models/product_pricelist.py` (**résolveur A2** `_ckr_get_promo_template_ids` + helpers `_ckr_active_items_domain` / `_ckr_item_is_reducer`) ; `product.template._search_get_detail` étendu à `ckr_promo_only` (sentinel `None` = global promo, `set()` = état vide forcé via `('id', '=', 0)`) ; `website._get_canonical_url` généralisé à tout `ckr_mode ∈ CKR_MODES_ALLOWED` ; bandeau `ckr_shop_promo_banner` + variante SCSS `--empty` ; carte Explorer Promotions basculée de `/shop` à `/promotions`. Tests E2E validés : 301 `/promotions` → `/shop?ckr_mode=promo` (paramètres préservés), non-régression `/kits` et `/shop`, bandeau + état vide, canonical correct, exclusivité filtre (path chargé avec pricelist test temporaire), non-régression modes `pack` et default. Snapshot §3 et synthèse §5 alignés ; checklist §6 case Promotions cochée. Points ouverts résiduels : alimentation back-office (non bloquant) ; hook A3 loyalty documenté comme extension future. |
| 2026-04-22 | **§3 / §4.2 / §4.5 / §5 / §6** : constat acté — pas d’entité e-commerce native « collection » en Odoo 19 CE comparable à catégorie publique / promo ; pas d’OCA de référence actée pour ce besoin ; modules « collection page » tiers hors doctrine par défaut. **Collections** = **objet éditorial CK par défaut** ; spec dédié **après Origines**. **Séquence** : **Origines (B) avant Collections (C)**. |
| 2026-04-22 | **MOA — orientation chantier** : **Collections** **gelée** (aucun lancement de spec/impl à ce stade ; document dédié ultérieur). **Origines** = **priorité actuelle** ; **décision de fond** : dimension **éditoriale** assumée (porte de navigation avec portée de lecture / mise en scène — **exclut** la réduction à un simple tag ou métadonnée sans signification visiteur). Snapshot §3, §4.2 (gel), §4.5 (élargissement), §5, §6 alignés. |
| 2026-04-22 | **CONTRAT_URL_ORIGINES.md** créé (cadrage initial) : obligations **signal éditorial minimal** (§3), interdit **filtre silencieux** (§2.2), options source de vérité / URL / front ; §12 check-list atelier. **SPEC** : intro portes, §4.5 (précision MOA + liens), §6, §7 références, checklist §6 ; précision formulation MOA (éditorial opérationnalisé, contexte de lecture visible). |
| 2026-04-22 | **CONTRAT_URL_ORIGINES.md** : **validation MOA du cadre** comme base d’atelier ; **§12.1** = cinq arbitrages minimum explicites (alignés demande MOA) ; **§12.2** compléments. **SPEC** checklist §6 Origines alignée sur §12.1 / §12.2. |
| 2026-04-22 | **CONTRAT_URL_ORIGINES §4.0** : position MOA pré-atelier **source de vérité** (socle structuré + projection CK ; hiérarchie options A1–A5) ; **§12.3** questions explicites ; verdicts §4.2–§4.6 alignés. **SPEC** §4.5 matrice + checklist §6 mises à jour. |
| 2026-04-22 | **Confirmation MOA** : séquence atelier **§4.0 + §12.1 + §12.3** validée comme point de départ ; suite atelier → PV → implémentation. **CONTRAT** §4.0 (paragraphe confirmation) ; **SPEC** puce intro Origines. |
| 2026-04-22 | **CONTRAT_URL_ORIGINES §13** : **verrouillage arbitrages métier** MOA (multi + OU, source structurée, §3.1, pas hub v1, repli invalide, vide dédié, fiche produit) ; **§12** = résidu PV/impl. **SPEC** : intro, snapshot, §4.5 matrice, §5 synthèse, §6 checklist, §7 ref. |
| 2026-04-22 | **Confirmation MOA** : **§13** = référence métier **stable** ; résidu **§12** (notamment **§12.2**) via PV / spec d’impl. ; pas de réouverture **§13** sans décision MOA écrite. **CONTRAT** §13 (paragraphe) ; **SPEC** puce Origines. |
| 2026-04-22 | **[SPEC_IMPL_ORIGINES.md](SPEC_IMPL_ORIGINES.md)** : spec d’implémentation technique porte Origines (réf. §7). |
| 2026-04-22 | **§4.2 Collections** : **[CADRAGE_FONCTIONNEL_COLLECTIONS.md](CADRAGE_FONCTIONNEL_COLLECTIONS.md)** versionné (définition, Active + période de validité, vocabulaire titre affiché / slug). Renvoi depuis §4.2 ; mise à jour **état chantier** (Origines livrée ; impl. Collections toujours conditionnée à contrat d’URL + spec). Snapshot §3 Collections : cadrage fonctionnel ouvert, impl. différée. |
| 2026-04-22 | **Collections** : création de **[CONTRAT_URL_COLLECTIONS.md](CONTRAT_URL_COLLECTIONS.md)** — trame puis **décisions MOA** : **chemins nobles** **`/collections`** / **`/collections/<slug>`** ; prolongement **combinaison** = URL noble dédiée (**§4.6**) ; pas de **`/shop?ckr_mode=collection…`** en référence publique (**§4.3**). Table §4.2 « Contrat d’URL », §7 références et suite documentaire **CADRAGE** alignés. |
| 2026-04-22 | **Collections** : contrat — **syntaxe S1 actée** **`/collections/union/<slug-1>/…`** (tri canonique, **301** de normalisation, **slug `union` interdit** côté collection) ; **CADRAGE §9.1** aligné. |
| 2026-04-22 | **Collections** : création de **[SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md)** — impl. v1 (réf. §7). |
| 2026-04-22 | **§4.4 — porte Catégories mise en service** (module **19.0.1.3.0**). Contrat **Hybride H1 — cible native** : `/categories` → 301 → `/shop/category/<id>-<slug>` (sans `ckr_mode`). Livrables : `models/product_public_category.py` (`_ckr_get_explorer_entry_shop_path`, validation site, domaine racines) ; route `ckr_categories_alias` dans `controllers/website_sale_ckr.py` (strip de `ckr_mode` sur les query params) ; `data/ckr_explorer_category_parameter.xml` ; `ckr_entries.xml` (`href` → `/categories`) ; document **[CONTRAT_URL_CATEGORIES.md](CONTRAT_URL_CATEGORIES.md)**. Snapshot §3, synthèse §5, checklist §6, intro « portes déployées » alignés. |
| 2026-04-21 | **§4.3 — porte Kits mise en service** (module **19.0.1.1.0**). Le statut bascule de *contrat acté / controleur en attente* à *déployé et vérifié*. Livraisons : dépendance `product_pack` ajoutée au manifest ; `WebsiteSaleCKR` (héritage `WebsiteSale`, hooks `_get_search_options` / `_get_shop_domain` / `_shop_get_query_url_kwargs` / `_get_additional_shop_values`) ; `WebsiteSaleCKRKitsAlias` (route `/kits` → redirection **301** vers `/shop?ckr_mode=pack`, params préservés) ; `product.template._search_get_detail` enrichi (ajout de `[('pack_ok', '=', True)]` au `base_domain` si `options.ckr_pack_only`) ; `website._get_canonical_url` enrichi (ré-injection **ciblée** de `ckr_mode=pack` pour le couple `/shop` + param — seule dérogation au comportement natif *« canonical URLs should not have qs »* de `_url_localized`, strictement limitée à cette porte) ; bandeau visiteur `ckr_shop_pack_banner` (xpath sur `website_sale.products`, `t-if="ckr_pack_mode"`) + styles SCSS ; retrait du stub `/kits` (record `website_page`, template `ckr_page_compositions`, fichier `views/pages/ckr_compositions.xml` supprimé ; nettoyage via `data/ckr_cleanup_kits_stub.xml`). Snapshot du §3 mis à jour en conséquence : `/kits` passe de *STUB transitoire* à *redirection 301 active*. Points ouverts restants pour cette porte : niveau d’affichage des `pack_line_ids` sur la fiche produit (décision ultérieure). |
| 2026-04-22 | **Cohérence éditoriale** : en-tête (**statut** / **date**), intro **état des portes**, **snapshot** §3, **vague C**, **§4.2–§4.5** (maturité, stubs), **§5** synthèse, **§6** stubs — alignement sur **Origines livrée** et **Collections** (cadrage + contrat + spec impl. **ouverts**, impl. **à venir**). **Historique antérieur** : **inchangé**. |
| 2026-04-22 | **Collections** : [CONTRAT_URL_COLLECTIONS.md](CONTRAT_URL_COLLECTIONS.md) + [SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md) — verrouillages MOA (**repli union A**, **message flash**, **copies**, **titre union**) ; **§4.2** tableau « Contrat d’URL » aligné. |
| 2026-04-22 | **Collections** : création de **[PV_RECETTE_COLLECTIONS_V1.md](PV_RECETTE_COLLECTIONS_V1.md)** — recette **RC-01…RC-14**, tag **`dorevia_ckr_collections`** ; **SPEC_IMPL §12.0** (grille PV ↔ tests) ; renvois **§4.2**, **§5**, **§6**, **§7**. |
| 2026-04-22 | **Collections — feu vert code MOA** : **dernier résidu §13** soldé — priorité **`ckr_mode`** figée **`pack > promo > origin > collection`** (`collection` **en dernier**, non-régression absolue des portes livrées) ; **[CONTRAT_URL_COLLECTIONS.md](CONTRAT_URL_COLLECTIONS.md) §13** tout coché, **[SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md) §5.1** figée (constantes + snippet `CKR_MODE_PRIORITY`) ; statut **zéro résidu documentaire** ; snapshot §3, §4.2, §4.5 (vague C), §6 checklist, **intro** et **état chantier** alignés. |
| 2026-04-22 | **Collections — étape 1 checklist (module 19.0.1.5.0)** : bump `__manifest__.py` + création `models/ckr_shop_collection.py` (champs **SPEC_IMPL §2.1**, contraintes **§2.2** — slug unique par site, slug `union` réservé, fenêtre de dates, M2M `product_template_ids`) + helpers visibilité RC-03 (`_ckr_visible_domain` / `_ckr_is_visible` / `_ckr_resolve_visible_slugs`) + ACL `security/ir.model.access.csv` (patron Origines). Reste à faire : inverse M2M `product.template`, vues BO, routes `/collections`, hooks contrôleur (**§5.1** `CKR_MODE_COLLECTION` + priorité figée), bandeaux + copies §8, fiche produit, cleanup stub, impl. tests `dorevia_ckr_collections` RC-01…RC-14. |
| 2026-04-22 | **Collections — étape 2 checklist (BO complet)** : inverse M2M `ckr_collection_ids` sur `product.template` (même table `ckr_shop_collection_product_template_rel`, colonnes inversées) ; `views/ckr_shop_collection_views.xml` — search (actives / archivées / en période / expirées / à venir / regroupement site) + list (handle sequence, slug, titre, compteur produits, dates, site) + form (ribbon archivée, identité URL, publication, période, notebook Produits rattachés) + action + **menus Configuration + Catalog** (patron Origines, séquence 20) ; `views/product_template_ckr_collection_views.xml` — extension héritée de `product_template_form_view_ckr_origin`, champ `ckr_collection_ids` placé après `ckr_origin_value_ids`. **RC-01 / RC-02 prêts** en BO. Reste à faire : constantes `CKR_MODE_COLLECTION` + routes publiques + hooks + canonical + bandeaux visiteur + fiche produit visiteur + cleanup stub + impl. tests. |
| 2026-04-22 | **Collections — recette MOA / clôture §13 (module 19.0.1.6.1)** — suite **`dorevia_ckr_collections`** exécutée réellement sur base dédiée (`ckr_collections_recette`, sandbox Odoo 19) : **23 tests verts** (9 `TestCkrCollectionsPVModel` + 14 `TestCkrCollectionsPVHttp`, **0 FAIL / 0 ERROR / 0 `skipTest`**, 13,92 s, 2 016 requêtes). Cinq correctifs mineurs issus de la recette, tous livrés dans le bump **19.0.1.6.1** : (i) `product.template._search_get_detail` — bloc `ckr_collection_only` qui injecte `[('id', 'in', ckr_collection_template_ids)]` dans le `base_domain` ; en Odoo 19 `website_sale._shop_lookup_products` ne passe plus par `_get_shop_domain`, `_search_get_detail` devient le **point unique** de filtrage catalogue ; (ii) `controllers/website_sale_ckr._get_search_options` — pose `options['ckr_collection_template_ids']` en paire avec `ckr_collection_only` ; (iii) `security/ir.model.access.csv` — ACL **read-only** publiques (`base.group_public`) + portail (`base.group_portal`) sur `ckr.shop.collection`, indispensables au rendu du bloc Collections sur la fiche produit visiteur ; (iv) `views/ckr_shop_collection_views.xml` — retrait de `string=` sur `<group>` search (compat RNG Odoo 19) ; (v) fixtures HTTP — `TestCkrCollectionsPVHttp.setUpClass` utilise `date.today()` (alignement `fields.Date.context_today`). [PV_RECETTE_COLLECTIONS_V1.md](PV_RECETTE_COLLECTIONS_V1.md) : §4 colonne *Résultat observé* renseignée, §7 anomalies **A1–A4 résolues**, §8 **Conforme**, §9 visas MOA / Dev posés. Preuves dans `docs/mvp_01/evidences/` (`run_rc_collections_v1_summary.log` + `v2_summary.log` + `README.md`). Snapshot §3, §4.2, §6, en-tête *Statut* et §5 alignés sur **19.0.1.6.1**. **Porte Collections acceptée en recette**, checklist §13 `SPEC_IMPL_COLLECTIONS.md` **clôturée**. |
| 2026-04-22 | **Collections — étape 3 checklist §13 livrée (module 19.0.1.6.0)** — **porte Collections déployée**. Intro *Statut* de l'en-tête, §3 snapshot (*Cible atteinte v19.0.1.6.0*), §4.2 maturité, §4.5 synthèse, §6 checklist et **« Ouverture code en cours »** alignés sur la **cible atteinte**. Contrôleur `WebsiteSaleCKR` étendu : constante `CKR_MODE_COLLECTION` **en fin** de `CKR_MODE_PRIORITY` (pack > promo > origin > collection — non-régression absolue), routes nobles **`/collections`** + **`/collections/<slug>`** + **`/collections/union`** + **`/collections/union/<path:path>`** (**301** normalisation + **302** replis + **flash session one-shot** `ckr_collection_notice` **sans** `ckr_notice` en query), **canonical self** (le garde `path == /shop` de `models/website.py` exclut déjà les URLs nobles), bandeaux §8 (général / unitaire fallback / union) + état vide §12 A + lien *Retour aux collections*, bloc fiche produit → liens `/collections/<slug>` (helper `_ckr_get_visible_collections`), **cleanup** stub CMS (`data/ckr_cleanup_collections_stub.xml`, retrait `website_page_collections`, suppression `views/pages/ckr_collections.xml`). **Tests** : activation intégrale — `TestCkrCollectionsPVModel.test_ckr_col_rc14_effective_mode_priority` (priorité `_ckr_effective_mode` figée, multi-modes, collection seule lisible) + **12** méthodes `TestCkrCollectionsPVHttp` (RC-04 / 05 / 06 / 07 ×2 / 08 ×3 / 09 / 10 / 11 / 12 / 13 / 14) avec `setUpClass` déterministe (A/B visibles avec produit, C visible sans produit, D archivée, E expirée, lonely sans collection). **20** méthodes totales tag **`dorevia_ckr_collections`**, **0** `skipTest` résiduel. |
| 2026-04-23 | Après le **snapshot** §3 : **note UI homepage** — renvoi explicite vers **[WIREFRAME_HOMEPAGE.md](../direction/WIREFRAME_HOMEPAGE.md)** (Bloc 3 *Présentation front*) pour le rail Explorer **manuel** (sans autoplay, prev/next, accessibilité, rythme vertical) ; périmètre SPEC inchangé (**URLs / `/shop`**). |
| 2026-04-25 | **Porte Incontournables** (`ckr_mode=featured`) : intégration **officielle** — paragraphe d’extension sous l’en-tête ; puce **état des portes** ; **snapshot** §3 ; nouvelle fiche **§4.6** (URL 301, canonical, `dorevia_ckreyol_marketplace.featured_collection_id`, comportements, priorité cible **`pack > promo > featured > origin > collection`**, matrice, livrables dev, non-objectifs) ; **§5** synthèse ; **§6** checklist ; **§7** ref. **[2_SHOP.md](../mvp_02/2_SHOP.md)**. **Impl. module** : *à venir* ; **tests** non-régression à prévoir. |
| 2026-04-25 | **§4.6** : *Note vigilance (dev)* — `featured` = **consommation** de la collection configurée, **pas** de duplication de la logique collection / seconde mécanique éditoriale. |
| 2026-04-25 | **Porte Incontournables** — **clôture exploitation** : §4.6 *Exploitation — paramètre `featured_collection_id`* (module **19.0.1.10.5**) : paramètre **hors XML**, création **post_init** si absent uniquement, migration **pre/post** pour préserver la valeur au passage **19.0.1.10.5**, obligation **`odoo -u dorevia_ckreyol_marketplace`** **une fois par base** ≥ **19.0.1.10.5**. Statuts §4.6 / snapshot / §5 / §6 checklist alignés sur **livrée**. |
| 2026-04-25 | **§4.4 Catégories** : note technique **Odoo 19** — absence de `website_url` sur `product.public.category` pour les liens sidebar ; patron `website_sale.categorie_link` documenté (**19.0.1.10.27**) ; renvoi [TICKET_SHOP_SIDEBAR_CATEGORIES.md](../mvp_02/TICKET_SHOP_SIDEBAR_CATEGORIES.md). |
