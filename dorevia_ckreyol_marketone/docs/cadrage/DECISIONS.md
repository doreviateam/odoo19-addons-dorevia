# Décisions d’architecture (ADR) — `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **Format** | Une décision par entrée, datée, réversible explicitement |
| **Statut Lot 0** | Décisions de cadrage — pas de code |

---

## ADR-001 — Création du module Marketone

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | Acceptée |
| **Contexte** | `dorevia_ckreyol_marketplace` accumule dette (manifeste, XPath, thème tiers, monolithes). |
| **Décision** | Créer `dorevia_ckreyol_marketone` comme **nouveau module** Odoo 19 CE, inspiration conceptuelle uniquement. |
| **Conséquences** | Pas de migration automatique depuis marketplace ; bascule MOA distincte. |

---

## ADR-002 — `website_sale` moteur unique

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | Acceptée |
| **Décision** | Catalogue, panier, checkout et paiement restent 100 % `website_sale`. |
| **Conséquences** | Marketone = présentation + orientation ; pas de routes e-commerce parallèles. |
| **Contrat** | C1 dans `cadrage/CONTRACTS.md` |

---

## ADR-003 — Conteneur `/shop` unique

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | Acceptée |
| **Contexte** | Doctrine gelée sur marketplace (`DOCTRINE_SHOP_CONTENEUR_UNIQUE.md`, 2026-04-28). |
| **Décision** | Reprendre le principe `/shop + query` ; reporter l’implémentation filtres au Lot 6. |
| **Conséquences** | Pas de pages `/collections/<slug>` autonomes dans la cible Marketone. |
| **Réserve** | Noms de paramètres `marketone_*` à figer avant Lot 6 (remplace `ckr_*`). |

---

## ADR-004 — Pas de thème tiers obligatoire

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | Acceptée |
| **Contexte** | `theme_classic_store` a imposé `ckr_shop_classic_tile_restore.xml` et CSS défensif massif. |
| **Décision** | Ne pas dépendre de `theme_classic_store` ni d’un thème OCA/Enterprise au socle. |
| **Conséquences** | Tuile produit = structure Odoo standard + SCSS scoped ; risque visuel initial plus « Odoo natif ». |
| **Alternative rejetée** | Reprendre Classic Store pour fidélité pixel — trop couplé. |

---

## ADR-005 — Dépendances minimales Lot 1

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | Acceptée |
| **Décision** | Lot 1 : `website`, `website_sale`, `portal` uniquement. |
| **Optionnelles** | `website_sale_wishlist`, `website_crm`, `mass_mailing`, `product_pack` — activation par ticket MOA. |
| **Conséquences** | Porte Kits (pack) bloquée tant que `product_pack` non validé. |

---

## ADR-006 — Préfixe `marketone_`

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | Acceptée |
| **Décision** | Préfixer paramètres URL, classes CSS et tags tests par `marketone_` / `dorevia_marketone_*`. |
| **Conséquences** | Pas de collision avec `ckr_*` en cas d’erreur de co-installation. |

---

## ADR-007 — Manifeste sobre

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | Acceptée |
| **Décision** | Le champ `description` du manifeste ne sert pas de changelog ; l’historique vit dans git et `cadrage/DECISIONS.md`. |
| **Conséquences** | Lisibilité install ; pas de reprise des 140+ entrées legacy. |

---

## ADR-008 — Pas de code avant validation Lot 0

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | Acceptée |
| **Décision** | Aucun Python/XML/SCSS/JS avant GO humain explicite sur le cadrage. |
| **Conséquences** | Lot 0 = documentation uniquement. |

---

## ADR-009 — Filtres via `_search_get_detail` (Lot 6)

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | Acceptée (principe) — implémentation Lot 6 |
| **Contexte** | Pattern validé sur `product_template.py` du module legacy. |
| **Décision** | Reprendre le **pattern** hook Odoo 19, pas le fichier (~900+ lignes cumulées). |
| **Conséquences** | Contrôleur allégé ; une porte = un increment test + contrat URL. |

---

## ADR-010 — Portes catalogue après stabilisation tunnel

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | Acceptée |
| **Décision** | Lot 6 uniquement après GO Lots 1–5 (home, shop, product, cart, checkout). |
| **Conséquences** | Homepage sans liens Explorer vers filtres non implémentés (Lot 2). |

---

## ADR-011 — Pas de reprise doc legacy volumineuse

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | Acceptée |
| **Contexte** | ~132 fichiers docs marketplace, contradictions collections URL nobles vs 301. |
| **Décision** | Extraire principes dans `cadrage/CONTRACTS.md` / `cadrage/DECISIONS.md` ; ne pas copier l’arborescence `docs/mvp_*`. |
| **Conséquences** | Référence ponctuelle aux chemins legacy pour audit, pas de duplication. |

---

## ADR-012 — Tests taggés par périmètre

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | Acceptée |
| **Décision** | Reprendre la discipline de tags Odoo du legacy (`dorevia_ckr_*` → `dorevia_marketone_*`). |
| **Conséquences** | CI peut exécuter sous-ensembles ; smoke obligatoire à chaque lot. |

---

## ADR-013 — Base de référence `ckr-marketone-01`

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | Acceptée — base créée sur sandbox |
| **Décision** | L’environnement de référence Marketone est la base PostgreSQL **`ckr-marketone-01`** sur Docker `sandbox-odoo19-odoo-1` (Odoo `19.0-20260324`, URL http://localhost:18079). |
| **Règles** | Pas de `dorevia_ckreyol_marketplace`, pas de thème tiers, pas d’optionnel Marketone sans ticket ; socle `website` + `website_sale` + `portal`. |
| **Conséquences** | Lot 1 (install / update / smoke) s’exécute uniquement sur cette base ; procédure dans `docs/recette/ENV_REFERENCE.md`. |
| **Note** | `website_sale_wishlist` et `website_sale_comparison` auto-installés par Odoo 19 ont été désinstallés après init pour garder un périmètre minimal. |

---

## ADR-017 — Design system minimal « Artisanal Terroir » (ticket prêt)

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | Proposée — en attente validation / exécution |
| **Décision** | Jalon Lot 2.1 avant Lot 4 : tokens Artisanal Terroir, EB Garamond + Hanken Grotesk, header/footer minimaux, adaptation home/shop existants. |
| **Référence design** | Stitch — inspiration uniquement, pas de copie HTML/CSS. |
| **Polices** | Google Fonts provisoire ; self-host possible Lot 2.2. |
| **Footer** | Option A clair (ivoire) ; Option B sombre reportée. |
| **Ticket** | `docs/tickets/TICKET_MARKETONE_LOT2_1_DESIGN_SYSTEM_MINIMAL.md` |
| **Version cible** | `19.0.3.1.0` (proposition) |

---

## ADR-016 — Lot 3 boutique `/shop`

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | Acceptée — livré |
| **Version module** | `19.0.3.0.0` |
| **Décision** | Lot 3 = ancre CSS `marketone-shop` sur `website_sale.products` + `_shop.scss` scoped ; pas de JS, contrôleur, `_search_get_detail`, ni héritage `website_sale.product`. |
| **Version cible** | `19.0.3.0.0` |
| **Patron** | Ancre CSS unique (aligné KIT PRO / contrat C5), distinct du monolithe legacy `ckr_shop`. |
| **Tests** | Tag `dorevia_marketone_lot3` ; retrait assertion négative `marketone-shop` du Lot 2. |
| **Ticket** | `docs/tickets/TICKET_MARKETONE_LOT3_SHOP.md` |

---

## ADR-015 — Lot 2 identité front

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | Acceptée — GO validé 2026-05-18 |
| **Décision** | Lot 2 = tokens SCSS `$marketone-*`, scope `.marketone-root`, home QWeb minimal (intro + CTA `/shop`), tests `dorevia_marketone_lot2` ; pas de JS, pas de `/shop`, pas de portes. |
| **Version module** | `19.0.2.0.0` |
| **Polices** | **Google Fonts** (Playfair Display + Inter) chargées via `views/layout/website_layout.xml` — **solution provisoire acceptable au Lot 2** (dépendance réseau tierce, RGPD/perf à arbitrer). |
| **Réserve** | Lot 2.1 possible : self-host des polices ou stack système seule si MOA l’exige. |
| **Palette** | Reprise conceptuelle charte Phase 1 sans copier fichiers legacy `ckr_*`. |
| **Copies home** | Textes MOA provisoires validés au GO exécution (épicerie fine créole, C-Kreyol, accroche, CTA, 3 puces réassurance). |

---

## ADR-014 — Lot 1 socle installable

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | Acceptée — GO humain 2026-05-18 |
| **Décision** | Lot 1 = manifeste + asset SCSS placeholder + tests smoke ; pas de contrôleur, modèle, vue ni JS au socle. |
| **Version module** | `19.0.1.0.0` |
| **Validation** | `-i` / `-u` sur `ckr-marketone-01` + tag `dorevia_marketone_smoke` |

---

## ADR-017 — Lot 2.1 design system minimal « Artisanal Terroir »

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | Acceptée — **GO humain avec réserves** (recette visuelle 2026-05-18) |
| **Version module** | `19.0.3.1.0` |
| **Décision** | Lot 2.1 = tokens SCSS Artisanal Terroir, composants `_buttons` / `_header` / `_footer`, polices EB Garamond + Hanken Grotesk (Google Fonts provisoire), QWeb minimal header/footer, tests `dorevia_marketone_lot2_1` ; pas de JS, contrôleur, modèle ni logique catalogue. |
| **Réserves MOA** | 2–3 produits recette en BO pour cartes `/shop` (pas de seed XML) ; Contact `/contactus` native → ticket futur ; logo texte provisoire ; footer contact à compléter avant ouverture commerciale. |
| **Réserves techniques** | Logo texte `C-Kreyol` ; contact footer « à compléter » ; Google Fonts provisoire ; `Powered by odoo` masqué via `d-none` sur `.o_footer_copyright` + barre copyright Marketone (pas de suppression DOM agressive). |
| **Hors périmètre** | Fiche produit (Lot 4), panier/checkout (Lot 5), portes catalogue (Lot 6). |
| **Ticket** | `docs/tickets/TICKET_MARKETONE_LOT2_1_DESIGN_SYSTEM_MINIMAL.md` |

---

## ADR-018 — Articulation des trois dimensions C-Kreyol

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | Acceptée — doctrine produit |
| **Contexte** | `CK` signifie `C-Kreyol`. Le canal a vocation à proposer des produits produits dans des zones où l'on parle créole. Il ne doit pas être réduit à un site de produits antillais, une boutique exotique, une marketplace générique ou un site uniquement agro-transformé. |
| **Notion centrale** | Produits issus de territoires créolophones — territoire, langue, culture, production, transmission. |
| **Dimensions** | 1. e-commerce (vendre) ; 2. éditorial culturel (raconter) ; 3. partage de connaissance (transmettre). |
| **Décision** | C-Kreyol est conçu comme un canal e-commerce éditorialisé autour de produits issus de territoires créolophones. Le site articule les trois dimensions ci-dessus. Ces dimensions doivent être clairement agencées afin que l'éditorial et la connaissance enrichissent l'achat sans brouiller le parcours e-commerce. |
| **Doctrine courte** | C-Kreyol articule trois dimensions — vendre, raconter, transmettre — sans jamais les confondre. |
| **Agencement** | Le produit d'abord. Le récit ensuite. Le savoir en prolongement. |
| **Écueils** | Boutique pure (site marchand sans âme) ; mélange commerce / culture / savoir partout (parcours confus). |
| **Progression Marketone** | Lots 1-5 : socle e-commerce ; Lot 6 : portes catalogue ; lots suivants : éditorial et connaissance. |
| **Garde-fous Marketone** | Pas de contenus culturels lourds dans `/shop` trop tôt ; fiche produit non encyclopédique ; CTA d'achat non brouillé ; navigation complexe reportée ; possibilité éditoriale préparée sans implémentation prématurée. |
| **Conséquence technique** | Dans Marketone, le socle e-commerce reste prioritaire jusqu'à stabilisation des parcours boutique, fiche produit, panier et checkout (`website_sale` souverain). |
| **Impact Lot 4** | La fiche produit peut être enrichie par du récit ou de la réassurance si les données BO existent, mais ne devient pas un article encyclopédique et ne brouille pas le CTA d'achat. |
| **Références** | `docs/README.md` § Doctrine ; `cadrage/ARCHITECTURE.md` §2 |

---

## ADR-019 — Références d'inspiration 750g et Caribshopper

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | Acceptée — références MOA (hors exécution immédiate) |
| **Contexte** | C-Kreyol articule e-commerce, éditorial culturel et partage de connaissance (ADR-018). Deux sites servent de **références d'intention**, pas de modèles à porter dans Odoo. |
| **750g** | Inspiration pour recettes, usages, ingrédients, « que faire avec ? », transmission de savoir. |
| **Caribshopper** | Inspiration pour e-commerce territoires caribéens, logique pays/territoire, produits populaires, nouveautés, recettes, diaspora. |
| **Décision** | Conserver ces références pour les **futurs lots** éditoriaux et connaissance, **après** Lots 1–5 (socle e-commerce) et Lot 6 (portes catalogue) selon roadmap. |
| **Interdictions Marketone (socle)** | Ne pas copier la densité média de 750g ; ne pas copier la logique marketplace large de Caribshopper. |
| **Invariants** | Direction **Artisanal Terroir** ; parcours d'achat simple ; fiche produit non encyclopédique ; doctrine « le produit d'abord, le récit ensuite, le savoir en prolongement ». |
| **Impact Lot 4** | **Aucune modification** du ticket ou du périmètre technique Lot 4 à ce stade. |
| **Références** | `cadrage/ARCHITECTURE.md` §2.5 |

---

## ADR-020 — Banque visuelle marketplace `docs/assets`

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | Acceptée |
| **Contexte** | Le module legacy `dorevia_ckreyol_marketplace` versionne une banque PNG sous `docs/assets/` (packshots, moodboards MVP02, exports Stitch). Marketone ne cohabite pas avec marketplace sur une même base, mais peut **réutiliser** ces fichiers en recette et cadrage. |
| **Décision** | Autoriser l'exploitation de cette banque pour : (1) **recette BO** — 2 à 3 produits avec images réelles (`homepage_*`, `exemple_produit_*`) ; (2) **cadrage** lots éditoriaux futurs ; (3) **inspiration** Stitch — sans copie HTML/CSS. |
| **Interdictions** | Pas de seed XML produit dans Marketone ; pas de copie mécanique des blocs marketplace (Explorer, hero legacy) ; pas d'assets lourds sur fiche Lot 4 au-delà du retail sobre ; fichiers `stitch_*` = inspiration uniquement. |
| **Référence opérationnelle** | `docs/recette/ASSETS_REFERENCE.md` ; inventaire complet : `dorevia_ckreyol_marketplace/README.md` § Références visuelles. |
| **Impact Lot 4** | Recette visuelle : importer manuellement 2–3 packshots en BO — **aucun** changement de périmètre technique du ticket. |

---

## ADR-021 — Lot 4 fiche produit `marketone-product`

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | Acceptée — **GO avec réserves mineures** (recette MOA 2026-05-18) |
| **Version module** | `19.0.4.0.0` |
| **Décision** | Lot 4 = ancre CSS `marketone-product` sur `website_sale.product` + `_product.scss` scoped ; pas de JS, contrôleur, modèle, seed XML, portes ni `_search_get_detail`. |
| **Garde-fous** | ADR-018 / C7.4 : fiche retail, CTA prioritaire, pas encyclopédique ; niveau visuel ≥ Artisanal Terroir Lot 2.1. |
| **Tests** | Tag `dorevia_marketone_lot4` ; 37/37 (smoke + lot2 + lot2_1 + lot3 + lot4). |
| **Recette MOA** | `docs/recette/RECETTE_MANUELLE_LOT4.md` — réserve : compteur panier `2` = double clic recette, pas bug. |
| **Ticket** | `docs/tickets/TICKET_MARKETONE_LOT4_PRODUCT.md` |

---

## ADR-022 — Lot 5 panier / checkout smoke (`marketone-cart` / `marketone-checkout`)

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | **Acceptée — GO** (recette MOA 2026-05-18) |
| **Version module cible** | `19.0.5.0.0` |
| **Décision** | Lot 5 = smoke tunnel invité `website_sale` : scopes `marketone-cart` / `marketone-checkout` via `checkout_layout` (path HTTP, incl. `/shop/address` Odoo 19), SCSS scoped minimal, tests `dorevia_marketone_lot5` (12 tests, 49/49 non-régression). **Pas** de refonte checkout, JS, contrôleur, modèle, ni modification moteur panier / paiement. |
| **Contrats** | C8.1–C8.2 ; C8.3 (`payment_demo`) = tag étendu optionnel, non bloquant GO. |
| **Critère GO** | Visiteur invité : ajout → panier → modif / suppression → retour shop → 1ʳᵉ étape checkout sans 500 ; cohérence visuelle minimale Artisanal Terroir. |
| **Recette MOA** | `docs/recette/RECETTE_MANUELLE_LOT5.md` — réserve : compteur panier `3` = test quantité recette, pas bug. |
| **Ticket** | `docs/tickets/TICKET_MARKETONE_LOT5_CART_CHECKOUT.md` |

---

## ADR-023 — Lot 6.1 porte Incontournables (`marketone_mode=featured`)

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | **Acceptée — GO avec réserves** (cadrage + exécution + recette MOA) |
| **Version module** | `19.0.6.0.0` |
| **Décision** | Première porte catalogue : `marketone_mode=featured` sur `/shop`, alias `/incontournables` → 301, filtre via `product.public.category` référencée par paramètre système, hook `_search_get_detail` / `_get_search_options` / `_get_shop_domain` (alignement fourchette prix). Présentation minimale (titre Incontournables, intro, lien retour). **Pas** de modèle collection custom, tag, champ produit, JS, ni dépendance marketplace. |
| **Contrats** | C2, C3.A ; non-régression C1, C8, scopes Lots 2–5 |
| **Réserves cadrage** | (1) catégorie publique = source simple, collection éditoriale plus tard ; (2) SEO canonical/noindex documenté sans implémentation Lot 6.1 ; (3) filtres natifs Odoo conservés |
| **Réserves recette MOA** | (4) **`website_id` site courant** sur la catégorie = **prérequis d’exploitation** (recette / pré-prod), consolidé GO portes Boutique 2026-05-18 — sinon **500** sur featured ; (5) après `-u` : **redémarrer Odoo** pour `/incontournables` (routing HTTP) |
| **Recette** | `docs/recette/RECETTE_MANUELLE_LOT6_1.md` — 60/60 tests auto |
| **Tickets** | Cadrage : `TICKET_MARKETONE_LOT6_1_PORTE_INCONTOURNABLES` · Exécution : `TICKET_MARKETONE_LOT6_1_INCONTOURNABLES_EXEC` (**clôturé**) · Consolidation : `TICKET_MARKETONE_CONSOLIDATION_PORTES_BOUTIQUE` (**GO**) |

---

## ADR-024 — Structuration C-Kreyol en trois univers : Boutique, Culture, Savoirs

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | **Acceptée — GO MOA** (2026-05-18 ; document uniquement, aucun code) |
| **Contexte** | ADR-018 pose les trois dimensions (vendre, raconter, transmettre). Le MOA formalise le nommage **Boutique / Culture / Savoirs** pour structurer le site à terme, après stabilisation du socle e-commerce (Lots 1–5) et première porte catalogue (Lot 6.1). |
| **Décision** | C-Kreyol est structuré en trois univers : **1. Boutique** — acheter ; **2. Culture** — découvrir ; **3. Savoirs** — transmettre. Les **portes catalogue** appartiennent d’abord à l’univers **Boutique** (orientation de la grille `/shop` sans moteur parallèle). Les contenus **Culture** et **Savoirs** seront introduits **progressivement** dans des **espaces dédiés**, pas en transformant `/shop` en portail éditorial. |
| **Savoirs — contribution** | À terme, un **utilisateur identifié** pourra **proposer** une recette ; **publication** uniquement après **validation / modération** back-office. *Déposer une recette ≠ publier automatiquement.* |
| **Formule** | *Ceux qui savent transmettent à ceux qui découvrent.* |
| **Relation ADR-018** | ADR-024 **nomme** et **spatialise** les trois dimensions ; ADR-018 conserve l’agencement : produit d’abord, récit ensuite, savoir en prolongement. |
| **Garde-fous** | Produit prioritaire au parcours d’achat ; éditorial enrichit sans brouiller ; Savoirs sans forum ouvert ; une porte catalogue par lot ; pas de code univers sans ticket MOA GO ; pas de dépendance marketplace. |
| **Hors scope immédiat** | Implémentation navigation multi-univers ; module recette ; portes multiples simultanées ; copie code legacy `ckr_*`. |
| **Note détaillée** | `docs/cadrage/NOTE_UNIVERS_CK_MARKETONE.md` (audit legacy, impacts Lots 6.2+, Culture, Savoirs) |
| **Prochaine étape** | Culture v1 (ADR-026) après GO exécution ; Lots **6.3+** Boutique ; Savoirs séparé. |

---

## ADR-025 — Lot 6.2 porte Origines (`marketone_mode=origin`)

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | **GO MOA** (`19.0.7.0.0`, 2026-05-18) |
| **Version module cible** | `19.0.7.0.0` |
| **Contexte** | ADR-024 : porte **Boutique** ; Culture (récit territoire) reportée. Lot 6.1 a validé le pattern `_search_get_detail` + `_get_search_options`. |
| **Décision** | Porte **Origines** : `marketone_mode=origin`, facette `marketone_origin=<slug>`, alias `/origines` → 301. Vérité catalogue = attribut **Origine** ; profil **`marketone.shop.origin`** minimal (slug, phrase visiteur, visibilité) — **sans** portage `ckr.shop.origin`. Mode seul = catalogue complet + bandeau. Slug invalide → `/shop` nu. Présentation `/shop` minimale ; fiche produit origine légère avec lien optionnel vers la porte. **Un seul** `marketone_mode` actif. |
| **Contrats** | C2, C3.B ; C7.4 ; ADR-024 |
| **Réserves** | Cadrage : (1)–(5) inchangées · **Exploitation** : redémarrage daemon après `-u` pour alias `/origines` (comme `/incontournables`) |
| **Tickets** | Cadrage : `TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES` · Exécution : `TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES_EXEC` |
| **Hors scope** | Hub Culture, Savoirs, autres portes, JS, marketplace, cumul featured+origin |

---

## ADR-026 — Culture v1 — page territoire pilote (`/culture/<slug>`)

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | **Acceptée — GO MOA** (`19.0.8.0.0`, 2026-05-18) |
| **Version module** | `19.0.8.0.0` |
| **Contexte** | ADR-024 : récit territoire = univers **Culture**. Lot 6.2 a livré la porte Boutique Origines ; le récit est reporté hors `/shop`. Consolidation portes Boutique **GO**. |
| **Décision** | Premier lot Culture : **une page** territoire pilote via **`/culture/<slug>`** (pages `website` + présentation Marketone), contenu **court et visuel**, CTA vers porte Origines filtrée. **Pas** de modèle Culture dédié v1 ; **pas** d’extension encyclopédique de `marketone.shop.origin` ; **pas** de hub « toutes les origines » ; **pas** de contenu Culture long sur `/shop`. Liens contextuels depuis fiche produit et bandeau Origines facetté. Entrée menu header Culture **reportée**. SEO : note doc uniquement. |
| **Contrats** | C8 ; C7.4 ; ADR-024, ADR-025 |
| **Réserves** | (R1) page courte, élégante, visuelle ; (R2) pas de blog Culture ; (R3) pas de Culture long dans `/shop` ; (R4) profil origine Boutique inchangé ; (R5) Savoirs hors lot |
| **Tickets** | Cadrage : `TICKET_MARKETONE_CULTURE_TERRITOIRES_CADRAGE` (**clôturé**) · Exécution : `TICKET_MARKETONE_CULTURE_TERRITOIRES_EXEC` (**clôturé GO MOA**) |
| **Réserves exploitation** | Redémarrage daemon post-`-u` si route `/culture/<slug>` absente (routing) |
| **Hors scope** | Hub Culture, modèle ORM territoire (par défaut), Savoirs, Lot 6.3 Boutique, SEO avancé, portage marketplace |

---

## ADR-027 — Culture v2 légère — territoires additionnels (`martinique`, `reunion`)

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | **Acceptée — GO MOA** (`19.0.9.0.0`, 2026-05-18) |
| **Version module** | `19.0.9.0.0` |
| **Contexte** | Culture v1 **GO MOA** (ADR-026) : grammaire `/culture/<slug>` validée sur pilote `guadeloupe`. MOA : ne pas ouvrir Lot 6.3 Boutique ; prouver la **réplicabilité** éditoriale sans portail massif. |
| **Décision** | Étendre Culture à **+2 territoires** (`martinique`, `reunion`) via la **même** infra v1 : sections génériques, variation BO limitée (`name_visitor`, `context_phrase`, slug). **Option A** : pas de code fonctionnel nouveau si slugs publiés — BO + recette + tests `dorevia_marketone_culture_v2`. **Pas** de hub `/culture`, **pas** de menu header, **pas** de liens croisés, **pas** d’images par territoire, **pas** de champs longs sur `marketone.shop.origin`. |
| **Contrats** | C8 (v2) ; ADR-024, ADR-026 |
| **Réserves** | (R1) slugs sous réserve profils BO ; (R2) pas de champs longs ; (R3) pas de hub ; (R4) pas de menu header ; (R5) pas de 6.3 / Savoirs en parallèle |
| **Tickets** | Cadrage : `TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_CADRAGE` (**clôturé**) · Exécution : `TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_EXEC` (**clôturé GO MOA**) |
| **Réserves exploitation** | Redémarrage daemon post-`-u` si route `/culture/<slug>` absente |
| **Hors scope** | Hub Culture, menu header, modèle Culture, Lot 6.3, Savoirs, SEO avancé |

---

## ADR-028 — Savoirs v1 — recettes contributives (`marketone.savoir.recipe`)

| | |
|---|---|
| **Date** | 2026-05-18 |
| **Statut** | **Acceptée — GO cadrage avec réserves légères** (exécution après GO ticket exec) |
| **Version module cible** | `19.0.10.0.0` (proposition) |
| **Contexte** | Arbitrage MOA : Option 2 Savoirs après Boutique stable et Culture v1+v2 GO. Troisième univers à cadrer avant Culture v3 ou Lot 6.3. |
| **Décision** | Premier lot Savoirs : modèle minimal **`marketone.savoir.recipe`** avec états `draft` / `pending` / `published` / `rejected` / `archived` ; contributeur **portal** ; modération BO obligatoire ; URLs `/savoirs/<slug>`, `/savoirs/proposer` ; **pas** de hub `/savoirs` v1 ; produit lié **obligatoire** si publié ; bloc fiche « Idées & recettes » (0–3) **sous** CTA achat. **Pas** de `website_blog`, forum, commentaires, publication auto. |
| **Doctrine boutique** | **2026-05-19** — Les recettes / usages **ne sont pas** des produits vendables : **Boutique** = produits vendables uniquement ; **Savoirs** = `marketone.savoir.recipe` (liées à un produit, jamais listées dans `/shop`). Interdit de créer des `product.template` nommés « Recette … » pour tester Culture ou Savoirs. |
| **Contrats** | C9 ; C7.4 ; ADR-018, ADR-024 |
| **Réserves** | (R1) modèle minimal ; (R2) pas de hub ; (R3) pas commentaires ; (R4) pas auto-publication ; (R5) recettes sous CTA ; (R6) pas 6.3/Culture v3 en parallèle |
| **Tickets** | Cadrage : `TICKET_MARKETONE_SAVOIRS_V1_CADRAGE` (**clôturé**) · Exécution : `TICKET_MARKETONE_SAVOIRS_V1_EXEC` |
| **Hors scope** | Hub Savoirs, menu header, notifications contributeur, SEO avancé, Culture v3, Lot 6.3 |

---

## ADR-029 — Taxonomie catalogue : convention Odoo catégories e-commerce

| | |
|---|---|
| **Date** | 2026-05-19 — amendements même jour (standard Odoo ; navigation transversale) |
| **Statut** | **Acceptée — GO MOA** (documentation ; **pas de code** sans ticket dédié) |
| **Contexte** | Enrichissement catalogue recette, portes Boutique 6.1/6.2. Première rédaction : distinguer catégorie vs **collection dédiée** (`marketone.shop.collection`). Clarification MOA : s’aligner sur **`product.public.category`** (Odoo autorise plusieurs catégories par produit). |
| **Décision** | **Support unique (provisoire)** : `product.public.category`. **Convention MOA** : **une catégorie principale** obligatoire (rayon / nature — stable, descriptive) + **0 à 3 catégories secondaires** ; **max 4** catégories e-commerce par produit vendable. **Origine** = territoire. **Porte** = entrée navigation `/shop`. **Ne pas** implémenter `marketone.shop.collection` pour l’instant. |
| **Rattachement** | Chaque produit vendable : **min 1** catégorie e-commerce (principale). Secondaires : max **3**. Formulation : voir C3.C.9–C3.C.10. |
| **Principales (13)** | Biscuits salés · Biscuits sucrés · Épices · Assaisonnements · Sauces · Condiments · Confitures · Sirops · Boissons · Farines · Fécules · Kits & Coffrets · **Miels** — mapping recette : [`MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md`](cadrage/MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md). |
| **Pourquoi principale** | La notion de catégorie principale est introduite afin d’offrir au visiteur une **navigation transversale stable par nature de produit**. Même si Odoo permet plusieurs catégories e-commerce publiques par produit, Marketone distingue une **catégorie principale de référence**, utilisée pour structurer le menu de navigation par catégories, et des **catégories secondaires** utilisées pour les sélections, usages ou mises en avant. Question visiteur cible : *« Quel type de produit est-ce que je cherche ? »* (grands rayons : Biscuits salés, Épices, Confitures, Boissons, etc.). |
| **Règle synthétique** | La catégorie principale **structure le menu**. Les catégories secondaires **enrichissent les parcours**. Les origines **situent** le produit. Les portes **orientent l’entrée**. |
| **Indépendance origine** | La catégorisation **ne dépend pas** de l’origine. Harmonisation Martinique / Guadeloupe = chantier **Origines / Culture**, sans impact sur principale / secondaires. |
| **Exemple** | Crackers manioc Sainte-Anne → principale *Biscuits salés* ; secondaires *Incontournables*, *Apéritif créole*, *Cuisine du manioc* — **validé** (catégories) ; origine = axe séparé. |
| **Évolution** | Modèle collection commercial — voir **ADR-030** (objet métier cible distinct ; secondaires = transitoire). |
| **Lot 6.1** | Porte Incontournables via catégorie publique « Incontournables » = **aligné** (catégorie **secondaire** + filtre porte) — **statut transitoire** (ADR-030). |
| **Contrat** | C3.C |
| **Document** | [`cadrage/TAXONOMIE_CATALOGUE.md`](cadrage/TAXONOMIE_CATALOGUE.md) |

---

## ADR-030 — Collection commerciale Marketone

| | |
|---|---|
| **Date** | 2026-05-19 |
| **Statut** | **Brouillon validé MOA** (2026-05-19) — pas de code sans ticket exec Lot A |
| **Contexte** | ADR-029 a provisionné les catégories secondaires comme enrichissement BO (`product.public.category`) et reporté `marketone.shop.collection`. Doctrine MOA (2026-05-19) : une **collection commerciale** répond à une intention d’achat transversale, distincte de la nature produit (principale), du territoire (origine) et de l’offre packagée (pack). Sidebar `/shop` cible : rubrique **Collections** en complément d’Origine, Catégories et Prix. Référence technique sidebar catégories : `19.0.10.9.0` (facettes contextuelles C4). |
| **Décision** | La **collection commerciale** est un **objet métier cible distinct** — pas une simple catégorie e-commerce secondaire. Elle constitue une **proposition d’achat transversale**, permanente ou temporaire, construite par regroupement de produits **indépendamment** de leur catégorie principale et de leur origine. Elle agit comme **filtre transversal** du catalogue (`/shop`) et comme **entrée commerciale** dans la boutique (porte, mise en avant). **Pas d’implémentation** tant qu’un ticket exec n’est pas validé après relecture de cet ADR. |
| **Définition** | Proposition d’achat transversale : regroupement éditorial / commercial de `product.template` publiés, sans imposer une lecture par nature (principale) ni par territoire (origine). |
| **Peut contenir** | Produits **unitaires** et **packs** ; produits de **plusieurs** catégories principales ; produits de **plusieurs** origines. |
| **Attributs cibles** (à terme) | Nom · slug · description courte · image · produits associés (M2M) · date début / fin · actif / publié · ordre d’affichage · mise en avant homepage / boutique (optionnel). Modèle indicatif : `marketone.shop.collection` (nom à confirmer au ticket). |
| **Phrase de synthèse** | La **catégorie** classe · l’**origine** situe · le **pack** compose une offre vendable · la **collection commerciale** propose. |
| **Distinctions** | Voir tableau ci-dessous. |
| **Sidebar cible `/shop`** | Ordre MOA : **Origine** · **Catégories** · **Collections** · **Fourchette de prix**. La rubrique Collections **n’remplace pas** catégories ni origines ; elle ajoute une lecture commerciale transversale. Facette attendue (indicatif) : `marketone_collection` — philosophie alignée C4 (valeur visible si produit dans `search_product` **ou** déjà sélectionnée). **État actuel** : Collections **non implémentées** ; sidebar livrée = Origine + Catégories (C4) + Prix. |
| **Secondaires BO — statut transitoire** | Les 4 secondaires ADR-029 (*Incontournables*, *Apéritif créole*, *Cuisine du manioc*, *Idées cadeaux*) **peuvent préfigurer** des collections mais **ne sont pas** le modèle cible. **Lot 6.1** (*Incontournables* + `marketone_mode=featured` + `/incontournables` → 301) = **pattern transitoire** (filtre via `product.public.category` + porte), pas définition de la collection commerciale à terme. |
| **Relation ADR-029** | Catégories principales / secondaires = taxonomie **nature** et enrichissement BO. Collections = axe **intention d’achat** — orthogonal. Un produit garde sa principale et son origine **en plus** d’appartenir à 0..n collections (cardinalité à trancher au ticket). |
| **Contrats** | C3.4 (priorité modes) · C3.C (taxonomie) — extensions collections à rédiger au ticket |
| **Références** | ADR-029 · [`TAXONOMIE_CATALOGUE.md`](TAXONOMIE_CATALOGUE.md) · [`MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md`](MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md) · Lot 6.1 featured · sidebar C4 `19.0.10.9.0` |

### Distinctions — questions visiteur

| Notion | Question visiteur | Rôle Marketone | Support actuel |
|--------|-------------------|----------------|----------------|
| **Catégorie principale** | « Ce produit est quoi ? » | Structure le menu / sidebar **Catégories** | `product.public.category` (13 principales) · facette `marketone_category` |
| **Origine** | « D’où vient ce produit ? » | Situe le produit · sidebar **Origine** | Attribut Origine · porte `marketone_mode=origin` |
| **Pack** | « J’achète un ensemble ? » | Offre vendable composée | `marketone_mode=pack` (contrat · **non livré**) |
| **Catégorie secondaire** | Enrichissement parcours / sélection | **Transitoire** — usages, mises en avant BO | `product.public.category` (4 secondaires) — **≠** collection cible |
| **Collection commerciale** | « Quelle proposition / intention d’achat ? » | Filtre transversal · entrée boutique | **À créer** — objet métier dédié |

### Décisions ouvertes (avant ticket implémentation)

| # | Sujet | Options / question | Décideur |
|---|--------|------------------|----------|
| **D1** | Devenir des **4 secondaires** actuelles | (a) Maintien BO seul · (b) Migration progressive vers collections · (c) Double rattachement transitoire (secondaire + collection) | MOA + tech |
| **D2** | Coexistence **`marketone_mode=featured`** (Lot 6.1) et future facette **`marketone_collection`** | Porte unique vs facette sidebar vs les deux · impact priorité modes `pack > promo > featured > origin > collection` | MOA |
| **D3** | **Packs** dans une collection | Inclusion du template pack (`pack_ok`) · résolution composants · affichage grille | MOA + tech |
| **D4** | Cardinalité produit ↔ collection | 0..n collections par produit · règles publication | MOA |
| **D5** | Collections **temporaires** | Champs date début/fin · comportement hors fenêtre (404 / masqué sidebar / archive) | MOA |
| **D6** | SEO / URLs | Porte `/collections/<slug>` vs query `marketone_collection` vs les deux (alias 301) | MOA SEO |

### Découpage implémentation proposé (indicatif)

| Lot | Périmètre | Livrable attendu |
|-----|-----------|------------------|
| **Lot A** | Modèle BO + rattachement produits | `marketone.shop.collection` (ou nom retenu) · admin · M2M templates · publication / dates |
| **Lot B** | Facette sidebar **Collections** | Rubrique sidebar · filtre transversal `/shop` · C4-like · combinaison AND avec Origine / Catégories / Prix |
| **Lot C** | Homepage / mise en avant | Blocs éditoriaux · liens portes · hors scope Lot A/B |

### Hors scope (cet ADR)

- Implémentation code · migrations · QWeb sidebar Collections.
- Refonte Lot 6.1 *Incontournables* (sauf arbitrage D2).
- Lot 2 sidebar Origines contextuelles (ticket séparé).
- Savoirs · `shop_ppg`.

### Prochaine étape

| Étape | Statut |
|-------|--------|
| Relecture MOA ADR-030 | ✅ 2026-05-19 |
| Ticket Lot A BO | [`TICKET_MARKETONE_COLLECTION_LOT_A.md`](../tickets/TICKET_MARKETONE_COLLECTION_LOT_A.md) — **clôturé** `19.0.11.0.0` |
| Ticket Lot B sidebar | [`TICKET_MARKETONE_COLLECTION_LOT_B_SIDEBAR.md`](../tickets/TICKET_MARKETONE_COLLECTION_LOT_B_SIDEBAR.md) — **clôturé** `19.0.12.0.0` |
| Lot C (homepage) | Ticket ultérieur |

---

## Décisions en attente (à trancher avant Lots 6.3+)

| Sujet | Options | Décideur |
|-------|---------|----------|
| Contrainte catégories e-commerce | Principale obligatoire · max 4 publiques · distinction principale/secondaire — **ticket dédié** | MOA (post mapping BO) |
| Marquage catégorie principale vs secondaire | Convention BO seule vs champ produit / ordre — **hors scope sans ticket** | MOA (ticket dédié) |
| Modèle `marketone.shop.collection` | **ADR-030 validé** — ticket Lot A ; D1–D3 · D6 hors Lot A | MOA — [`TICKET_MARKETONE_COLLECTION_LOT_A`](../tickets/TICKET_MARKETONE_COLLECTION_LOT_A.md) |
| Alias HTTP legacy | `/kits`, `/promotions`, etc. en 301 | MOA SEO — Lot 6.2+ |
| `product_pack` | Dépendance optionnelle pour porte Kits | MOA |
| SEO `canonical` / `noindex` | Politique indexation URLs portes | MOA SEO |

---

## Décisions legacy à ne pas reprendre

| Legacy | Raison |
|--------|--------|
| Changelog dans `__manifest__.py` | Dette lisibilité |
| `request._ckr_collection_ctx` | État implicite difficile à déboguer |
| Exceptions comme flux 302 origine invalide | Préférer redirect explicite contrôleur |
| 11 migrations historiques | Nouveau socle sans historique version |
| Hero rotateur JS Lot 1 | Complexité / perf mobile |
| ACL public lecture collections | À rediscuter au Lot 6 avec surface minimale |
