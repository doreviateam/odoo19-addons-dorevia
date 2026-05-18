# Note de cadrage — Les trois univers C-Kreyol (Marketone)

| Champ | Valeur |
|-------|--------|
| **Statut** | **GO MOA** (2026-05-18) — **référence de cadrage officielle** ; document uniquement |
| **Date** | 2026-05-18 (version consolidée validée MOA) |
| **ADR** | [ADR-024](DECISIONS.md#adr-024--structuration-c-kreyol-en-trois-univers-boutique-culture-savoirs) — **GO** |
| **Complète** | [ADR-018](DECISIONS.md#adr-018--articulation-des-trois-dimensions-c-kreyol) (vendre / raconter / transmettre) |
| **Contexte projet** | Lots 1–5 **GO** ; Lot 6.1 **GO avec réserves** ; Lot 6.2 Origines **GO** (`19.0.7.0.0`) |

---

## 1. Les trois univers — définitions

C-Kreyol n’est pas seulement une boutique, ni seulement un média. Le site est structuré en **trois univers** complémentaires, chacun avec un verbe d’action clair :

| Univers | Verbe | Définition |
|---------|-------|------------|
| **1. Boutique** | **Acheter** | Parcours e-commerce : découvrir et commander des produits issus de territoires créolophones. |
| **2. Culture** | **Découvrir** | Explorer territoires, langues, producteurs, histoires, imaginaires et pratiques culturelles des mondes créolophones. |
| **3. Savoirs** | **Transmettre** | Partager usages, recettes, techniques, vocabulaire et pratiques — pour aider ceux qui découvrent les produits. |

**Correspondance avec la doctrine ADR-018**

| ADR-018 (dimensions) | Univers (nommage MOA) |
|----------------------|------------------------|
| Vendre | **Boutique** |
| Raconter | **Culture** |
| Transmettre | **Savoirs** |

Les deux formulations coexistent : ADR-018 pour l’agencement produit ; **Boutique / Culture / Savoirs** pour la navigation et la communication MOA.

**Formule de référence (Savoirs)**

```text
Ceux qui savent transmettent à ceux qui découvrent.
```

**Intuition métier**

Nous vendons des produits issus de territoires créolophones à des clients — notamment européens — qui ne savent pas toujours quoi en faire. L’univers **Savoirs** permet à ceux qui connaissent usages et recettes d’aider ceux qui découvrent.

---

## 2. Rôle de chaque univers

### 2.1 Boutique — acheter

**Mission** : convertir l’intention d’achat en commande fiable, mobile-first, sans friction.

**Périmètre fonctionnel** (socle stabilisé Marketone) :

| Élément | Statut Marketone |
|---------|------------------|
| Accueil orientant vers la boutique | Lot 2 — `marketone-root` |
| Catalogue `/shop` | Lot 3 — `marketone-shop` |
| Fiche produit | Lot 4 — `marketone-product` |
| Panier / checkout | Lot 5 — `marketone-cart` / `marketone-checkout` |
| Portes catalogue | Lot 6 — Incontournables (6.1), **Origines (6.2 GO)** ; une porte à la fois |

**Souveraineté technique** : `website_sale` reste le moteur catalogue, panier, checkout et paiement. Marketone **présente** et **oriente** ; il ne remplace pas Odoo.

### 2.2 Culture — découvrir

**Mission** : donner du sens aux produits et à la marque — territoires, langues, producteurs, récits, imaginaires — **sans** ralentir ni brouiller l’achat.

**Contenus visés** (progressifs, espaces dédiés) :

- pages ou rubriques territoire / origine / producteur ;
- récits éditoriaux (saisons, imaginaires, diaspora) ;
- médias légers (photos, citations, cartes conceptuelles) ;
- liens **depuis** la Boutique vers la Culture (fiche produit, porte Origines), jamais l’inverse en priorité.

**Ce n’est pas** : un second catalogue produit, un fil d’actualité social, ni un mur de texte sur `/shop`.

### 2.3 Savoirs — transmettre

**Mission** : prolonger l’achat par des repères actionnables — usages, recettes, techniques, vocabulaire.

**Workflow cible** (futur, hors socle actuel) :

```text
Utilisateur identifié → proposition de recette
Back-office / modération → validation
Site public → publication
```

**Règle non négociable** :

```text
Déposer une recette ne signifie pas publier automatiquement.
```

**Ce n’est pas** : un forum ouvert, un wiki collaboratif sans modération, ni une encyclopédie sur la fiche produit.

---

## 3. Portes catalogue dans l’univers Boutique

Les **portes catalogue** sont des entrées éditoriales **dans** l’univers Boutique : elles filtrent ou orientent la **grille produit** `/shop`, sans créer un moteur parallèle.

| Principe | Application |
|----------|-------------|
| Conteneur unique | `/shop` + paramètres de lecture (`marketone_mode`, facettes natives Odoo) |
| Une porte à la fois | Lots 6.1 et 6.2 livrés séparément ; Lot 6.3+ = cadrage MOA par porte |
| Filtres natifs conservés | Sidebar, tri, attributs, prix — `website_sale` souverain |
| Présentation minimale | Titre, intro courte, lien retour — pas de refonte Explorer legacy |

**Cartographie portes → Boutique**

| Porte (indicatif) | Mécanisme Marketone (cible) | Univers |
|-------------------|----------------------------|---------|
| Tous les produits | `/shop` sans mode | Boutique |
| Incontournables | `marketone_mode=featured` + catégorie publique BO | Boutique |
| Origines | `marketone_mode=origin` + `marketone_origin` — **GO** (ADR-025) | Boutique *(filtre produit)* ; **Culture** *(récit territoire — plus tard)* |
| Promotions | pricelist / promo (Lot 6.x) | Boutique |
| Kits / Packs | `pack_ok` + dépendance `product_pack` (décision MOA) | Boutique |
| Collections | modèle ou catégories (décision MOA post-6.1) | Boutique |
| Panier / checkout | tunnel `website_sale` | Boutique |

**Doctrine portes** (héritée du legacy, validée Marketone) :

```text
Les portes orientent.
Les filtres Odoo sélectionnent.
Marketone ne crée pas un moteur parallèle.
```

Une porte **Origines** (Lot 6.2 **GO**) reste dans la Boutique au sens **URL et grille** (`/shop`, alias `/origines`) ; le **récit** territoire relève de la **Culture** et vivra dans des pages dédiées **ultérieurement**, liées depuis la porte ou la fiche produit — **sans** hub Culture sur `/shop` ni modèle `marketone.shop.origin` encyclopédique.

---

## 4. Audit ciblé — ce que `dorevia_ckreyol_marketplace` préfigurait

Audit **lecture seule** du module legacy `dorevia_ckreyol_marketplace` (Odoo 19). Objectif : repérer les intuitions utiles, **sans** copier le code ni les monolithes `ckr_*`.

### 4.1 Univers Boutique — déjà fort

| Élément legacy | Fichiers / mécanismes | Intuition |
|----------------|----------------------|-----------|
| Portes `ckr_mode` | `controllers/website_sale_ckr.py`, `views/pages/ckr_shop.xml` | Whitelist modes, alias 301 (`/incontournables`, `/promotions`, `/kits`), priorité modes |
| Conteneur `/shop` unique | `docs/mvp_02/DOCTRINE_SHOP_CONTENEUR_UNIQUE.md` | Grille + facettes sur un seul moteur |
| Incontournables | `featured_collection_id` → `ckr.shop.collection` | Sélection curatoriale achetable (Marketone : catégorie publique) |
| Promotions / packs | `_search_get_detail`, pricelist | Filtres commerciaux alignés grille et prix |
| Collections | `ckr.shop.collection`, routes `/collections` | Curation M2M éditoriale → produits |
| Explorer homepage | `views/snippets/ckr_entries.xml` | Cartes portes vers `/shop?ckr_mode=…` |
| Homepage sélection | `ckr_homepage_featured_1..4` | 4 produits mis en avant (≠ Incontournables boutique) |
| Fiche produit merchandising | `views/pages/ckr_product.xml`, tickets MVP24 | Tuiles, origines affichées, collections liées |
| Canon URL | `models/website.py` | SEO cohérent sur `/shop?…` |

### 4.2 Univers Culture — amorcé, souvent masqué ou stub

| Élément legacy | Fichiers / mécanismes | Intuition |
|----------------|----------------------|-----------|
| Hero + copy territoires | `views/snippets/ckr_hero.xml` | CTA « Explorer les origines » |
| Bloc fournisseur | `views/snippets/ckr_supplier.xml` | Partenaires / origines réelles (souvent masqué MVP) |
| Bloc éditorial | `views/snippets/ckr_editorial.xml` | Récit « par saison ou par usage » → CTA collections |
| Origines structurées | `ckr.shop.origin`, attribut catalogue « Origine » | Couche Culture (profil visiteur) + facet Boutique |
| Fiche : bloc origines | `ckr_product_origins_block` | Récit non cliquable (évite confusion variante) |
| Vision long terme | `docs/direction/VISION_CK_MEDIA_COMMERCE.md` | « Média-commerce » : e-commerce + éditorial + communauté |
| Menu / structure | `docs/direction/STRUCTURE_MENU_PRINCIPAL.md` | Navigation multi-mondes (legacy) |

### 4.3 Univers Savoirs — annoncé, peu implémenté

| Élément legacy | Fichiers / mécanismes | Intuition |
|----------------|----------------------|-----------|
| Page `/recettes` | `views/pages/ckr_recettes.xml` | **Stub** Phase 1 — « bientôt disponible » |
| Menu Recettes | `views/layout/ckr_header.xml`, footer | Promesse nav sans contenu structuré |
| Newsletter `opt_recipes` | `models/ckr_circle_subscriber.py` | Intention Savoirs (préférences) |
| Copy produit / usages | helpers fiche produit | Usages en texte libre — pas de modèle recette |
| Inspiration 750g | référencé ADR-019 Marketone | « Que faire avec ? » — référence hors code |

### 4.4 Ambiguïtés legacy utiles à ne pas reproduire

| Ambiguïté | Risque |
|-----------|--------|
| **Featured** homepage vs **featured** boutique | Deux sens du même mot (`ckr_homepage_featured_*` vs `ckr_mode=featured`) |
| Porte Origines = filtre **et** récit territoire | Mélange Culture/Boutique sur une seule URL si mal cadré |
| Bloc éditorial « par usage » → CTA **shop** seulement | Usages/recettes confondus avec filtre catalogue |
| Menu **Communauté** + stubs Recettes / Offrir | Promesse Savoirs/Culture sans livrable |
| Monolithe `website_sale_ckr.py` | Dette maintenance, état implicite `request._ckr_*` |

---

## 5. Intuitions à conserver

| # | Intuition | Univers |
|---|-----------|---------|
| I1 | **Produit d’abord** — parcours Accueil → Boutique → Fiche → Panier → Commande | Boutique |
| I2 | **Conteneur boutique unique** `/shop` + paramètres de lecture + tests de contrat URL | Boutique |
| I3 | **Portes = orientation**, filtres Odoo = sélection | Boutique |
| I4 | **Origines** : attribut catalogue (vérité stock) + profil visiteur (récit) — deux couches | Boutique + Culture |
| I5 | **Territoires créolophones** comme fil rouge — pas « épicerie exotique » générique | Culture |
| I6 | **Transmission** utile pour clients qui découvrent les produits | Savoirs |
| I7 | **Contribution modérée** — proposition ≠ publication | Savoirs |
| I8 | **Inspiration 750g / Caribshopper** — intentions, pas copie densité ou marketplace | Culture + Savoirs + Boutique |
| I9 | **Présentation Marketone sobre** (Artisanal Terroir) — éditorial enrichit sans envahir | Transversal |

---

## 6. Ce qu’il ne faut pas reprendre

| Exclusion | Raison |
|----------|--------|
| Code et imports depuis `dorevia_ckreyol_marketplace` | Cohabitation interdite (C11) ; dette `ckr_*` |
| Monolithe contrôleur + `request._ckr_*` | État implicite, difficile à tester et maintenir |
| Explorer homepage asymétrique + chips multi-portes dès Lot 6.2 | Refonte shop / scope creep |
| Modèle `ckr.shop.collection` tel quel | Marketone 6.1 a choisi catégorie publique ; collections = décision MOA séparée |
| Stubs `/recettes` en navigation sans contenu | Promesse Savoirs vide |
| Fiche produit encyclopédique ou mur média type 750g | ADR-018 / C7.4 |
| Marketplace large type Caribshopper | ADR-019 |
| Multi-portes simultanées en exécution | Une porte par lot |
| Module recette / UGC maintenant | Hors phase ; workflow modération d’abord cadré |
| Transformer `/shop` en portail éditorial | `website_sale` souverain |

---

## 7. Impacts futurs (planning indicatif)

### 7.1 Lot 6.2 — porte Origines (Boutique — **GO MOA**, `19.0.7.0.0`)

| Sujet | Statut |
|-------|--------|
| URL | `marketone_mode=origin` + `marketone_origin=<slug>` ; alias `/origines` → 301 — ADR-025, C3.B |
| Source | Attribut **Origine** + `marketone.shop.origin` **minimal** (profil visiteur / slug / phrase / visibilité) |
| Hybride Origines | **Boutique** : filtre achetable sur `/shop` · **Culture** : récit territoire **reporté** (tickets dédiés) |
| Culture | Aucun hub territoire ni contenu long sur `/shop` au Lot 6.2 |
| Clôture | [`TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES_EXEC.md`](../tickets/TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES_EXEC.md) · [`RECETTE_MANUELLE_LOT6_2.md`](../recette/RECETTE_MANUELLE_LOT6_2.md) |

### 7.2 Lots Culture (post-socle, espaces dédiés)

| Lot indicatif | Contenu possible |
|---------------|------------------|
| Rubrique territoires / origines | Pages `website` + snippets Marketone scoped |
| Producteurs / histoires | Contenu éditorial léger, liens vers Boutique |
| Accueil | Réactiver l’équivalent **fournisseur / éditorial** legacy — version Marketone sobre |
| Navigation | Entrées **Culture** distinctes de **Boutique** (pas seulement des portes shop) |

**Hors scope immédiat** : communauté, régie publicitaire, B2B élargi (vision legacy `VISION_CK_MEDIA_COMMERCE.md`).

### 7.3 Lots Savoirs / recettes contributives

| Étape | Contenu |
|-------|---------|
| Cadrage | Modèle contenu recette (website, blog, module dédié ?), champs, liens produits |
| Workflow | Utilisateur identifié → brouillon → modération BO → publication |
| UX | Espace « proposer une recette » ; pas de publication automatique |
| Lien Boutique | Depuis fiche produit : 1–3 recettes liées en **prolongement**, CTA achat prioritaire |
| Inspiration | 750g (structure recette, ingrédients) — densité maîtrisée |

**Interdit au premier lot Savoirs** : forum, commentaires libres, SEO recettes masquant le parcours achat.

---

## 8. Garde-fous

| # | Garde-fou |
|---|-----------|
| G1 | **Le produit reste prioritaire** dans le parcours d’achat (fiche, panier, checkout). |
| G2 | **L’éditorial enrichit sans brouiller** — Culture et Savoirs en espaces ou blocs secondaires. |
| G3 | **Les Savoirs prolongent sans transformer la boutique en forum** — modération obligatoire. |
| G4 | **Contribution recette** = utilisateur **identifié** + **validation BO** avant publication. |
| G5 | **Une porte catalogue à la fois** en exécution (Lots 6.x). |
| G6 | **Pas de code univers** tant qu’un ticket MOA dédié n’est pas **GO**. |
| G7 | **Pas de dépendance** `dorevia_ckreyol_marketplace` sur les bases Marketone. |
| G8 | **Non-régression** : chaque lot porte conserve les scopes et tests des lots précédents. |

**Agencement rappel (ADR-018 / ADR-024)**

```text
Le produit d'abord.
Le récit ensuite.
Le savoir en prolongement.
```

---

## 9. Prochaines actions (hors ce document)

*Dernière mise à jour : 2026-05-18 — alignée sur l’état projet post-Lot 6.2.*

| # | Action | Statut |
|---|--------|--------|
| 1 | Valider **ADR-024** et cette note (version consolidée) | **GO MOA** (2026-05-18) |
| 2 | Lot 6.2 Origines — cadrage, exécution, recette | **GO** — `19.0.7.0.0`, commit `3c179ae` |
| 3 | **Consolidation portes Boutique** (6.1 + 6.2) | **GO** (2026-05-18) — [`TICKET_MARKETONE_CONSOLIDATION_PORTES_BOUTIQUE.md`](../tickets/TICKET_MARKETONE_CONSOLIDATION_PORTES_BOUTIQUE.md) |
| 4 | **Culture** — territoires v1 | **GO MOA** `19.0.8.0.0` — `/culture/<slug>` (pilote `guadeloupe`) |
| 5 | **Culture v2 légère** (`martinique`, `reunion`) | **Livré** `19.0.9.0.0` — grammaire réplicable |
| 6 | **Lot 6.3+** (Promotions, Kits, Collections…) | Gel MOA — socle Boutique stable |
| 6 | **Savoirs** — recettes contributives (identifié → modération BO → publication) | Cadrage **futur** ; pas de forum, pas de publication automatique |
| 7 | **Pas de code univers** | Tant qu’aucun ticket MOA dédié Culture / Savoirs n’est **GO** |

**Rappel** : `dorevia_ckreyol_marketplace` = mémoire d’intuitions (§4), **pas** source technique à copier.

---

## Références

| Document | Rôle |
|----------|------|
| `cadrage/DECISIONS.md` — ADR-018, ADR-019, ADR-023, ADR-024 | Décisions architecture |
| `cadrage/ARCHITECTURE.md` §2 | Doctrine trois dimensions |
| `cadrage/CONTRACTS.md` — C3, C3.A | Portes catalogue |
| `pilotage/ROADMAP.md` | Lots 6.x et backlog |
| `dorevia_ckreyol_marketplace/docs/direction/VISION_CK_MEDIA_COMMERCE.md` | Vision legacy (lecture seule) |
| `dorevia_ckreyol_marketplace/docs/mvp_02/DOCTRINE_SHOP_CONTENEUR_UNIQUE.md` | Doctrine shop unique |
