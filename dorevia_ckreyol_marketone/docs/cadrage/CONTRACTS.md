# Contrats fonctionnels — `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **Statut** | Lot 0 — contrats de socle et doctrine |
| **Implémentation** | Non démarrée (sauf mention « futur Lot N ») |

Ce fichier est la **source de vérité fonctionnelle** du module. Le manifeste Odoo et le code ne doivent pas y contredire.

---

## C1 — Moteur e-commerce

| ID | Règle |
|----|-------|
| C1.1 | `website_sale` est le seul moteur catalogue, panier et checkout. |
| C1.2 | Marketone ne crée pas de routes panier/checkout parallèles. |
| C1.3 | Aucun modèle catalogue parallèle au socle (Lots 1–5). |

**Statut** : doctrine — applicable dès Lot 1.

---

## C2 — Page boutique `/shop`

| ID | Règle |
|----|-------|
| C2.1 | `/shop` est le **conteneur catalogue unique**. |
| C2.2 | Les filtres et portes (Lots 6+) s’expriment en **query string** sur `/shop`, pas via des pages catalogue autonomes. |
| C2.3 | Forme canonique : `/shop` + paramètres de filtre whitelistés. |
| C2.4 | Les anciennes routes d’entrée (`/promotions`, `/kits`, etc.) pourront exister en **alias 301** vers `/shop?…` — jamais comme modèle de navigation interne (chips, sidebar). |

**Référence legacy** : `dorevia_ckreyol_marketplace/docs/mvp_02/DOCTRINE_SHOP_CONTENEUR_UNIQUE.md`

**Statut** : doctrine figée — implémentation filtres en Lot 6.

**Paramètres whitelistés** (amendement Lot 6.1 — 2026-05-18)

| Paramètre | Valeurs (Lot 6.1) | Statut |
|-----------|-------------------|--------|
| `marketone_mode` | `featured` (libellé : Incontournables) | **Figé Lot 6.1** |
| `marketone_mode` | `origin` (libellé : Origines) | **Figé Lot 6.2** |
| `marketone_origin` | slug profil origine (répétable, OU) | **Figé Lot 6.2** |
| `marketone_mode` | `promo` (libellé : Promotions) | **Figé Lot 6.3a** — livré `19.0.17.0.0` |
| `marketone_mode` | `pack` (libellé : Kits & Coffrets) | **Figé Lot 6.3b** — livré `19.0.18.0.0` |
| `marketone_mode` | `collection` | Lot 6.x collections |
| `marketone_collection` | slug collection | Lot 6.x collections |

```text
/shop?marketone_mode=featured                    # canonique Incontournables (Lot 6.1)
/incontournables                                 # alias 301 → ci-dessus
/shop?marketone_mode=origin                      # canonique porte Origines (Lot 6.2)
/shop?marketone_mode=origin&marketone_origin=<slug>   # facette origine (OU si plusieurs)
/origines                                        # alias 301 → /shop?marketone_mode=origin
/shop?marketone_mode=promo                       # canonique Promotions (Lot 6.3a)
/promotions                                      # alias 301 → ci-dessus
```

> **Interdit** : paramètre legacy `ckr_origin` — préfixe `marketone_*` uniquement (C11.2).

> Préfixe `marketone_*` (pas `ckr_*`) — C11.2.

---

## C3 — Filtres catalogue (Lot 6+)

| ID | Règle |
|----|-------|
| C3.1 | Toute restriction de grille passe par `product.template._search_get_detail` (hook Odoo 19). |
| C3.2 | Le contrôleur `WebsiteSale` hérité injecte des **options** ; pas de domaine calculé en QWeb. |
| C3.3 | Whitelist stricte des paramètres URL ; paramètres inconnus ignorés silencieusement. |
| C3.4 | Priorité déterministe si plusieurs modes : **pack > promo > featured > origin > collection** (reprise logique legacy validée MOA). |
| C3.5 | Chaque porte s’appuie sur une **source de vérité** Odoo/OCA explicite — pas de liste produit codée en dur. |
| C3.6 | **Un seul** `marketone_mode` actif par requête — pas de cumul (ex. `featured` + `origin`). |
| C3.7 | Filtres natifs Odoo sur `/shop` (sidebar, tri, attributs) **conservés** (Lots 6.1+). |

### C3.A — Porte Incontournables (Lot 6.1 — figé cadrage 2026-05-18)

| Élément | Règle |
|---------|-------|
| Mode URL | `marketone_mode=featured` |
| Libellé MOA | **Incontournables** (pas le mot « featured » côté visiteur) |
| Entrée alias | `GET /incontournables` → **301** → `/shop?marketone_mode=featured` |
| Source produits | `ir.config_parameter` `dorevia_ckreyol_marketone.featured_public_category_id` → `product.public.category` nommée **Incontournables** |
| Multi-catégories | Filtre porte = appartenance à la catégorie publique **Incontournables** (catégorie **secondaire** MOA — ADR-029). Odoo autorise plusieurs catégories ; convention : une **principale** + secondaires. |
| Modèle custom | **Non** — pas de `marketone.shop.collection` (ADR-029) |
| Présentation | Titre + intro courte + lien « Tous les produits » sous `.marketone-shop` — pas de hero, pas de chips multi-portes |
| SEO | `canonical` / `noindex` : **documenter** ; hors scope élargi exécution Lot 6.1 |

**Sources de vérité — autres portes** (Lots 6.2+)

| Porte | Source |
|-------|--------|
| Promotions | `product.pricelist.item` réducteur |
| Kits/Packs | `product.template.pack_ok` (si `product_pack` activé) |
| Origines | Attribut produit « Origine » + `marketone.shop.origin` (C3.B) |
| Sélections éditoriales / commerciales | Catégories e-commerce **secondaires** (`product.public.category`) — ADR-029 |
| Catégories merchandising | `product.public.category` — **principale** + **secondaires** (convention MOA) |

**Statut** : C3.A **implémenté Lot 6.1** — GO avec réserves (recette MOA 2026-05-18). **Prérequis exploitation** : catégorie publique **Incontournables** avec `website_id` = site courant — obligatoire recette / pré-prod (consolidation portes Boutique GO 2026-05-18 ; cf. ADR-023).

### C3.B — Porte Origines (Lot 6.2 — figé cadrage 2026-05-18)

| Élément | Règle |
|---------|-------|
| Univers | **Boutique** — filtre / orientation `/shop` ; récit territoire **Culture** = lot dédié (hors 6.2) |
| Mode URL | `marketone_mode=origin` |
| Libellé MOA | **Origines** |
| Facette | `marketone_origin=<slug>` — logique **OU** si plusieurs slugs ; **pas** `ckr_origin` |
| Mode seul | `marketone_mode=origin` sans facette → **catalogue complet** + bandeau porte |
| Entrée alias | `GET /origines` → **301** → `/shop?marketone_mode=origin` |
| Source catalogue | Attribut produit **Origine** (`product.attribute` + `attribute_line_ids` sur template) |
| Profil éditorial | `marketone.shop.origin` **minimal** : `attribute_value_id`, `slug`, `name_visitor`, `context_phrase`, `sequence`, `website_published`, `website_id` — **pas** page Culture, pas d’image/HTML long obligatoire |
| Portage legacy | **Interdit** `ckr.shop.origin` |
| Origine invalide | Redirect **`/shop` nu** (sans paramètres porte) |
| Présentation `/shop` | Titre (Origines ou nom origine si une facette), intro courte, lien « Tous les produits », état vide sobre |
| Fiche produit | Origine **légère** ; lien optionnel `/shop?marketone_mode=origin&marketone_origin=<slug>` — C7.4 retail-first |
| SEO | `canonical` / `noindex` : **documenter** ; hors implémentation Lot 6.2 |
| Cumul modes | **Un seul** `marketone_mode` — pas `featured` + `origin` |

**Statut** : C3.B **GO MOA** (`19.0.7.0.0`, ADR-025, 2026-05-18).

### C3.C — Taxonomie catalogue (MOA 2026-05-19, amendements standard Odoo + navigation)

> La notion de catégorie principale est introduite afin d’offrir au visiteur une navigation transversale stable par nature de produit. Même si Odoo permet plusieurs catégories e-commerce publiques par produit, Marketone distingue une catégorie principale de référence, utilisée pour structurer le menu de navigation par catégories, et des catégories secondaires utilisées pour les sélections, usages ou mises en avant.

| ID | Règle |
|----|-------|
| C3.C.0 | **Synthèse** : la catégorie principale **structure le menu** ; les catégories secondaires **enrichissent les parcours** ; les origines **situent** le produit ; les portes **orientent l’entrée**. |
| C3.C.1 | Support : **`product.public.category`** (standard `website_sale`) — Odoo autorise plusieurs catégories par produit. |
| C3.C.2 | Convention MOA : **une catégorie e-commerce principale** par produit — rayon / nature descriptive stable ; répond à *« Quel type de produit est-ce que je cherche ? »* ; référence pour le menu transversal **Catégories** (cible UX). |
| C3.C.3 | Convention MOA : **zéro à trois catégories secondaires** (sélections, usages, mises en avant, parcours complémentaires) sur le même support. |
| C3.C.4 | **Origine** = territoire (attribut + `marketone.shop.origin`) — **axe indépendant** : la catégorisation (principale / secondaires) **ne dépend pas** de l’origine ; harmonisation origine = chantier Origines / Culture, pas Catégories. |
| C3.C.5 | **Porte** = entrée navigation `/shop` — consomme une source Odoo (souvent catégorie secondaire, attribut, pricelist…). |
| C3.C.6 | **Pas** de modèle `marketone.shop.collection` sans ticket dédié ; réévaluation possible si secondaires insuffisantes. |
| C3.C.7 | **Pas de code** pour matérialiser principale vs secondaire sans ticket MOA (champ, UI ou procédure BO). |
| C3.C.8 | Porte Incontournables (Lot 6.1) : filtre sur catégorie publique « Incontournables » = catégorie **secondaire** attendue sur les produits concernés. |
| C3.C.9 | Chaque produit vendable doit être rattaché à **au moins une** catégorie e-commerce, correspondant à sa **catégorie principale**. |
| C3.C.10 | Les catégories secondaires sont autorisées **dans la limite de trois** rattachements supplémentaires. Un produit **ne doit pas dépasser quatre** catégories e-commerce au total. |
| C3.C.11 | Liste cible des catégories principales (13) : Biscuits salés · Biscuits sucrés · Épices · Assaisonnements · Sauces · Condiments · Confitures · Sirops · Boissons · Farines · Fécules · Kits & Coffrets · **Miels** — détail produit : [`MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md`](./MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md). |

**Référence** : [`cadrage/TAXONOMIE_CATALOGUE.md`](./TAXONOMIE_CATALOGUE.md) · [`cadrage/MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md`](./MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md).

**Statut** : **GO MOA** — doctrine ; **pas d’implémentation** hors ticket.

### C3.D — Porte Promotions (Lot 6.3a — figé cadrage GO MOA 2026-06-08)

| Élément | Règle |
|---------|-------|
| ADR | [ADR-034](../cadrage/DECISIONS.md#adr-034--arbitrage-architecture-cadrage2-socle-odoo-natif) |
| Doctrine | **Odoo exécute. Marketone habille et oriente.** |
| Mode URL | `marketone_mode=promo` |
| Libellé MOA | **Promotions** |
| Entrée alias | `GET /promotions` → **301** → `/shop?marketone_mode=promo` |
| Source produits | `product.pricelist.item` **actifs**, **strictement réducteurs**, sur la **pricelist courante du visiteur** |
| Résolveur | `product.pricelist._marketone_get_promo_template_ids(website, pricelist)` (nom indicatif) |
| Temporalité | Item actif à `now` (`date_start` / `date_end` ouvertes ou englobantes) |
| Réduction | Rejet items neutres / mark-ups (`percent_price=0`, `fixed_price >= list_price`, etc.) |
| `applied_on` | `0_product_variant` · `1_product` · `2_product_category` · `3_global` |
| Promo globale (`3_global`) | Si item global actif strictement réducteur → **catalogue complet** sans filtre produit supplémentaire (retour `None`) |
| État vide | Aucun item éligible → grille vide + message sobre — **pas** 404 · **pas** 500 |
| Pricelist courante | Chaîne : paramètre explicite → `website._get_and_cache_current_pricelist()` → fallback `partner.property_product_pricelist` — **M7** |
| Prix affichés | **Natif** `website_sale` — Marketone **ne recalcule pas** |
| Présentation | Titre **Promotions** · intro courte · lien « Tous les produits » → `/shop` |
| Chip header | Lien **Promotions** → `/promotions` — **amendement MOA M5** à C2.4 (chip porte autorisé pour Promotions uniquement) |
| Chip Kits | **Autorisé** Lot 6.3b — lien `/kits` → 301 |
| Chips filtres actifs | **Pas** de chip porte dans la barre filtres (UX-1 G10) |
| SEO | `canonical` / `noindex` : **documenter** ; hors implémentation Lot 6.3a |
| Coupons / loyalty | **Hors scope** 6.3a — extension future via ticket + ADR |
| Interdit | Champ promo custom · modèle `marketone.promo.*` · calcul remise Python/JS front · moteur promo parallèle |

**Statut** : C3.D **GO MOA clôturé** — livré `19.0.17.0.0` (2026-06-08) · [`RECEPTION_MOA_LOT6_3A_PROMO.md`](../cadrage2/RECEPTION_MOA_LOT6_3A_PROMO.md) · P7 S/O mono-pricelist recette.

### C3.E — Porte Kits & Coffrets (Lot 6.3b — figé cadrage GO MOA 2026-06-08)

| Élément | Règle |
|---------|-------|
| ADR | ADR-034 · **ADR-035** · ADR-005 |
| Mode URL | `marketone_mode=pack` |
| Libellé MOA | **Kits & Coffrets** — « Pack » = terme technique/interne uniquement |
| Entrée alias | `GET /kits` → **301** → `/shop?marketone_mode=pack` |
| Source produits | `product.template.pack_ok = True` — module **`product_pack`** (OCA) |
| Filtre porte | **`pack_ok=True` uniquement** — pas la catégorie « Kits & Coffrets » seule |
| Dépendance manifest | **`product_pack`** activé · **`sale_product_pack` hors v1** |
| Chip header | **Kits & Coffrets** → `/kits` |
| Prix / composants | Résolution **native** `product_pack` · affichage fiche **natif OCA** — **aucun widget Marketone** |
| Panier v1 | Produit pack = **1 ligne** `website_sale` standard |
| Interdit | Liste composants codée en dur · `marketone.pack.*` · moteur pack parallèle |
| Réserve MOA | Explosion composants vente/stock/préparation/facturation = **hors v1** — [`TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md`](../tickets/maintenance/TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md) |

**Statut** : C3.E **GO MOA clôturé** — livré `19.0.18.0.0` (2026-06-08) · [`RECEPTION_MOA_LOT6_3B_PACK.md`](../cadrage2/RECEPTION_MOA_LOT6_3B_PACK.md) · réserves `sale_product_pack` / explosion composants hors v1 maintenues.

### C8 — Univers Culture — page territoire v1 (cadrage GO avec réserves 2026-05-18)

| Élément | Règle |
|---------|-------|
| Univers | **Culture** — découvrir ; **hors** `/shop` |
| URL | `GET /culture/<slug>` — ex. `/culture/guadeloupe` — **pas** de collision avec alias Boutique `/origines` |
| Conteneur v1 | Pages `website` + templates / snippets Marketone sobres — **pas** de modèle ORM Culture dédié sauf besoin technique démontré |
| Périmètre v1 | **Une** page territoire pilote — **pas** de hub « toutes les origines » |
| Éditorial | Chapô + sections courtes + visuel léger + CTA → `/shop?marketone_mode=origin&marketone_origin=<slug>` |
| `marketone.shop.origin` | Profil Boutique **inchangé** ; même slug possible — **pas** de fusion de modèles |
| Liens Boutique | Fiche produit + bandeau Origines **facetté** → page Culture — **pas** de hub Culture sur `/shop` |
| Navigation | Liens contextuels v1 ; entrée header Culture **reportée** |
| SEO | Documenter seulement — pas de chantier SEO avancé v1 |
| Savoirs | Hors scope — ticket séparé |

**Statut** : C8 **GO MOA** v1 (`19.0.8.0.0`, ADR-026, 2026-05-18) — recette [`RECETTE_MANUELLE_CULTURE_V1.md`](../recette/culture/RECETTE_MANUELLE_CULTURE_V1.md) acceptée.

#### C8.v2 — Réplicabilité territoires (cadrage GO avec réserves 2026-05-18)

| Élément | Règle |
|---------|-------|
| Territoires | **+2** slugs : `martinique`, `reunion` — **sous réserve** profils BO |
| Delta technique | **Aucun** code fonctionnel nouveau si infra v1 suffit — BO + recette + tests |
| Éditorial | Sections **génériques** ; varient `name_visitor`, `context_phrase`, slug, CTA |
| Visuel | **Pas** d’image par territoire v2 |
| Navigation | **Pas** de liens croisés ; **pas** de hub `/culture` ; menu header **reporté** |
| Tests | Tag `dorevia_marketone_culture_v2` ; non-régression **85+** tests |
| Exécution | Après GO [`TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_EXEC.md`](../tickets/culture/TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_EXEC.md) (ADR-027) |

**Statut** : C8.v2 **GO MOA** (`19.0.9.0.0`, ADR-027, 2026-05-18) — recette [`RECETTE_MANUELLE_CULTURE_V2.md`](../recette/culture/RECETTE_MANUELLE_CULTURE_V2.md) acceptée.

### C9 — Univers Savoirs — recettes contributives v1 (cadrage GO avec réserves 2026-05-18)

| Élément | Règle |
|---------|-------|
| Univers | **Savoirs** — transmettre ; **hors** `/shop` |
| Modèle | **`marketone.savoir.recipe`** minimal — **pas** `website_blog` comme conteneur principal |
| Workflow | Portal identifié → proposition → modération BO → publication — **pas** d’auto-publication |
| États | `draft`, `pending`, `published`, `rejected`, `archived` — pas `draft → published` sans modérateur |
| URLs | `/savoirs/<slug-recette>`, `/savoirs/proposer` — **pas** de hub `/savoirs` v1 |
| Liens | Produit **obligatoire** si publié ; origine / Culture optionnels ; fiche produit 0–3 recettes **sous** CTA achat |
| Rôles | Contributeur, modérateur, éditeur, public |
| Interdit v1 | Forum, commentaires, likes, hub index, contenu long sur `/shop` |
| SEO | Documenter seulement |
| Exécution | Après GO [`TICKET_MARKETONE_SAVOIRS_V1_EXEC.md`](../tickets/savoirs/TICKET_MARKETONE_SAVOIRS_V1_EXEC.md) (ADR-028) |

**Statut** : C9 **contractuel** — exécution en attente GO MOA.

---

## C4 — Présentation front

| ID | Règle |
|----|-------|
| C4.1 | Styles scoped sous `.marketone-root` / classes `marketone-*`. |
| C4.2 | Pas de `<style>` inline massif en QWeb pour contourner le thème. |
| C4.3 | Pas de `!important` défensif sauf exception documentée dans `cadrage/DECISIONS.md`. |
| C4.4 | Mobile-first : lisibilité tactile, CTA accessibles, pas de scroll horizontal involontaire. |
| C4.5 | JavaScript uniquement si SCSS ou QWeb insuffisants — justification dans `cadrage/DECISIONS.md`. |

**Statut** : applicable dès Lot 2.

---

## C5 — Héritages QWeb

| ID | Règle |
|----|-------|
| C5.1 | Privilégier xpath sur conteneurs stables (`#wrap`, `#o_wsale_products_grid`). |
| C5.2 | Éviter `replace` massif de templates `website_sale`. |
| C5.3 | Pas de dépendance à la structure DOM d’un thème tiers. |
| C5.4 | Priorité d’héritage ≤ 20 sauf décision contraire documentée. |

**Statut** : applicable dès Lot 3.

---

## C6 — Homepage

| ID | Règle |
|----|-------|
| C6.1 | La home est une page `website` standard enrichie par snippets Marketone. |
| C6.2 | Pas de hero rotatif au socle (Lot 2). |
| C6.3 | L’« Explorer catalogue » (grille de portes) est **reporté** après Lot 6 — pas de liens vers des filtres non implémentés. |

**Statut** : Lot 2 pour structure ; portes home en Lot 6+.

---

## C7 — Fiche produit

| ID | Règle |
|----|-------|
| C7.1 | La fiche reste le template `website_sale` standard enrichi. |
| C7.2 | Blocs éditoriaux (origine, promesse) affichés **uniquement** si les champs BO sont renseignés. |
| C7.3 | Le bouton « Ajouter au panier » n’est pas masqué ni déplacé de façon à casser le tunnel. |
| C7.4 | La fiche n’est pas un article encyclopédique : produit et CTA prioritaires ; récit en appui (ADR-018). |

**Statut** : Lot 4.

---

## C8 — Panier et checkout

| ID | Règle |
|----|-------|
| C8.1 | Tunnel 100 % `website_sale` — pas de refonte. |
| C8.2 | Tests invité : ajout panier → panier → étape checkout accessible sans 500. |
| C8.3 | Tests E2E paiement (`payment_demo`) = périmètre étendu optionnel. |

**Statut** : Lot 5.

---

## C9 — Canonical et SEO

| ID | Règle |
|----|-------|
| C9.1 | Les URLs avec paramètres Marketone whitelistés participent au canonical maîtrisé (extension `website`). |
| C9.2 | Pas de duplication indexable shop / alias sans redirection 301. |
| C9.3 | Politique détaillée portes livrées : [`CADRAGE_SEO_PORTES_SHOP.md`](../cadrage2/CADRAGE_SEO_PORTES_SHOP.md) — exécution ticket [`TICKET_MARKETONE_SEO_PORTES_SHOP.md`](../tickets/boutique/TICKET_MARKETONE_SEO_PORTES_SHOP.md). |

**Statut** : **implémenté** · décision MOA [`DECISION_MOA_SEO_PORTES_SHOP.md`](../cadrage2/DECISION_MOA_SEO_PORTES_SHOP.md) · ADR-036.

---

## C10 — Données et démo

| ID | Règle |
|----|-------|
| C10.1 | Pas de XML seed obligatoire à l’install en production. |
| C10.2 | Données de recette test dans `tests/` ou fichier data chargé uniquement en mode test. |
| C10.3 | Hooks post-install idempotents si menus ou paramètres système — pas de pollution silencieuse. |

**Statut** : applicable dès Lot 1.

---

## C11 — Coexistence modules

| ID | Règle |
|----|-------|
| C11.1 | `dorevia_ckreyol_marketone` et `dorevia_ckreyol_marketplace` ne doivent pas cohabiter sur une même base. |
| C11.2 | Préfixes distincts : `marketone_*` vs `ckr_*`. |

**Statut** : doctrine permanente.

---

## Matrice de couverture tests (cible)

| Contrat | Tag test cible | Lot |
|---------|----------------|-----|
| Install | `dorevia_marketone_smoke` | 1 |
| Shop rendu | `dorevia_marketone_shop` | 3 |
| Cart/checkout | `dorevia_marketone_lot5` | 5 |
| Porte Incontournables | `dorevia_marketone_lot6_1_featured` | 6.1 |
| Porte Origines | `dorevia_marketone_lot6_2_origin` | 6.2 |
| Porte promo | `dorevia_marketone_promo` | 6.2+ |
| … | … | 6 |

---

## Amendements

Toute modification de ce fichier après validation Lot 0 doit :

1. Être datée dans `cadrage/DECISIONS.md`
2. Préciser le lot impacté
3. Ne pas présenter une ambition non livrée comme contractuelle
