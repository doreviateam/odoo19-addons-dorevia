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

## Décisions en attente (à trancher avant Lot 6)

| Sujet | Options | Décideur |
|-------|---------|----------|
| Nom exact des paramètres URL | `marketone_mode` vs `mo_mode` | MOA + archi |
| Modèle collections | Nouveau `marketone.shop.collection` vs réutilisation champs existants | MOA |
| Alias HTTP legacy | Reprendre `/kits`, `/promotions` en 301 | MOA SEO |
| `product_pack` | Dépendance optionnelle pour porte Kits | MOA |

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
