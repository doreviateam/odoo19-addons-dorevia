# Roadmap — `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **Statut global** | Lots 1–5 **GO** ; **6.1 GO avec réserves** ; **6.2 GO** ; **consolidation portes Boutique GO** |
| **Dernière mise à jour** | 2026-05-18 (GO consolidation portes Boutique) |
| **Décision de départ** | Nouveau module, pas de copie mécanique de `dorevia_ckreyol_marketplace` |

---

## Vue d’ensemble

```text
Lot 0  Cadrage + audit          ← GO (2026-05-18)
Lot 1  Socle installable        ← GO (2026-05-18)
Lot 2  Identité front minimale  ← GO (2026-05-18)
Lot 3  Boutique /shop propre    ← LIVRÉ
Lot 2.1 Design system minimal   ← GO avec réserves (`19.0.3.1.0`, 2026-05-18)
Lot 4  Fiche produit            ← GO avec réserves mineures (`19.0.4.0.0`, 2026-05-18)
Lot 5  Panier / checkout smoke   ← GO (`19.0.5.0.0`, 2026-05-18)
Lot 6  Portes catalogue        ← 6.1 GO avec réserves ; 6.2 Origines GO ; 6.3+ à cadrer
```

Chaque lot se clôture par une décision **GO / GO avec réserves / NO GO** humaine avant le lot suivant.

**Doctrine produit** (ADR-018, **ADR-024**) : trois univers — **Boutique** (acheter), **Culture** (découvrir), **Savoirs** (transmettre). Lots 1-5 = socle e-commerce ; Lot 6 = portes catalogue (univers Boutique) ; lots suivants = espaces Culture et Savoirs. Note : [`cadrage/NOTE_UNIVERS_CK_MARKETONE.md`](../cadrage/NOTE_UNIVERS_CK_MARKETONE.md).

**Inspirations MOA** (ADR-019) : 750g (connaissance / recettes), Caribshopper (e-commerce territoires caribéens) — références pour lots futurs, **pas** copie au socle ni élargissement du Lot 4.

---

## Lot 0 — Cadrage et audit

**Objectif** : extraire les enseignements de `dorevia_ckreyol_marketplace` sans les copier.

| Livrable | Statut |
|----------|--------|
| `docs/README.md` | ✅ Index documentaire |
| `docs/cadrage/BRIEF_INITIAL.md` | ✅ Brief initial |
| `docs/cadrage/ARCHITECTURE.md` | ✅ |
| `docs/pilotage/ROADMAP.md` | ✅ |
| `docs/cadrage/CONTRACTS.md` | ✅ |
| `docs/cadrage/DECISIONS.md` | ✅ |
| `docs/tickets/TICKET_MARKETONE_LOT0_CADRAGE.md` | ✅ |

**Décisions figées**

- `website_sale` reste le moteur e-commerce.
- `/shop` reste la route catalogue centrale.
- Aucun moteur catalogue parallèle.
- Pas de B2B/B2C avancé au socle initial.
- Pas de thème tiers obligatoire.
- Mobile-first dès le départ.
- Pas de reprise mécanique de l’ancien module.

**Critère GO**

```text
Le cadrage est lisible, sobre, validable par un humain,
et permet de générer le socle technique sans ambiguïté.
```

**Hors périmètre Lot 0** : tout code (Python, XML, SCSS, JS).

---

## Lot 1 — Socle module installable

**Objectif** : module Odoo 19 CE vide mais propre, installable sur une base avec `website_sale`.

**Contenu attendu**

- `__manifest__.py` sobre (pas de changelog intégré)
- Dépendances : `website`, `website_sale`, `portal`
- `__init__.py`, contrôleur minimal, `website.py` minimal
- Assets SCSS/JS déclarés (peuvent être quasi vides)
- `test_marketone_smoke.py`
- `ir.model.access.csv` si modèles exposés

**Critère GO**

```text
Le module s’installe sans erreur sur une base Odoo 19 CE avec website_sale.
```

**NO GO si**

- Dépendance non justifiée ajoutée
- Erreur à l’install ou à l’update `-u`
- Test smoke en échec

---

## Lot 2 — Identité front minimale

**Objectif** : empreinte C-Kreyol légère sans casser le thème Odoo natif.

**Ticket** : `docs/tickets/TICKET_MARKETONE_LOT2_IDENTITE_FRONT.md`

**Contenu prévu**

- Tokens SCSS `$marketone-*` + classes `marketone-*`
- `_layout.scss` (scope `.marketone-root`) + `_home.scss`
- QWeb home minimal (section intro + CTA `/shop`)
- Polices Playfair / Inter via layout (sans JS)
- Tests tag `dorevia_marketone_lot2`
- Version module `19.0.2.0.0`

**Critère GO**

```text
La home devient identifiable C-Kreyol de manière sobre et mobile-first,
sans casser le thème Odoo ni modifier le comportement standard de website_sale.
```

**Hors périmètre** : `/shop`, header/footer complets, portes, JS, thème tiers.

**Réserve** : copies MOA (H1, accroche) peuvent rester placeholder jusqu’validation texte.

---

## Lot 3 — Boutique `/shop` propre

**Objectif** : améliorer la lisibilité retail de la boutique standard.

**Ticket** : `docs/tickets/TICKET_MARKETONE_LOT3_SHOP.md`

**Contenu prévu**

- Ancre CSS `marketone-shop` sur `website_sale.products` (`#wrap`)
- `static/src/scss/_shop.scss` (scope strict, fichier léger)
- Tests tag `dorevia_marketone_lot3`
- Version module `19.0.3.0.0`
- Adaptation test Lot 2 `test_shop_no_marketone_shop_scope`

**Critère GO**

```text
La page /shop reste fonctionnellement standard Odoo,
mais devient plus lisible, mobile-first et crédible retail pour C-Kreyol.
```

**Hors périmètre** : fiche produit, portes, `_search_get_detail`, JS, panier/checkout.

**NO GO si**

- Logique catalogue parallèle introduite
- Dépendance à un thème tiers requise
- Régression 500 sur `/shop`
- Classe `marketone-shop` sur fiche produit (Lot 4)

---

## Lot 2.1 — Design system minimal « Artisanal Terroir »

**Statut** : **GO avec réserves** (recette visuelle MOA 2026-05-18).

**Ticket** : `docs/tickets/TICKET_MARKETONE_LOT2_1_DESIGN_SYSTEM_MINIMAL.md`

**Version** : `19.0.3.1.0`

**Réserves MOA acceptées**

- 2–3 produits de recette en BO pour cartes `/shop` (pas de seed XML)
- Contact `/contactus` Odoo native → ticket futur « Contact minimal C-Kreyol »
- Logo texte provisoire ; footer contact « à compléter » avant ouverture commerciale

---

## Lot 4 — Fiche produit

**Statut** : **GO avec réserves mineures** (`19.0.4.0.0`, recette MOA 2026-05-18).

**Ticket** : `docs/tickets/TICKET_MARKETONE_LOT4_PRODUCT.md`

**Livrables** : `views/pages/product.xml`, `_product.scss`, tests `dorevia_marketone_lot4` (37/37 tests auto OK).

**Recette MOA** : [`docs/recette/RECETTE_MANUELLE_LOT4.md`](../recette/RECETTE_MANUELLE_LOT4.md)

**Réserves mineures**

- Compteur panier à `2` sur captures : double clic CTA pendant recette — pas d’anomalie fonctionnelle.

**Critère GO** — validé

```text
Une fiche produit peut être consultée, comprise et ajoutée au panier sans friction.
Rendu visuel au moins au niveau Artisanal Terroir (Lot 2.1).
```

---

## Lot 5 — Panier / checkout smoke

**Statut** : **GO** (`19.0.5.0.0`, recette MOA 2026-05-18).

**Ticket** : `docs/tickets/TICKET_MARKETONE_LOT5_CART_CHECKOUT.md`

**Recette MOA** : [`docs/recette/RECETTE_MANUELLE_LOT5.md`](../recette/RECETTE_MANUELLE_LOT5.md)

**Livrables** : `cart.xml` (scope via `checkout_layout`), `_cart.scss`, `_checkout.scss`, tests `dorevia_marketone_lot5` (49/49 non-régression).

**Réserves non bloquantes**

- Compteur panier à `3` sur captures : test modification quantité en recette — pas bug.

**Critère GO** — validé

```text
Un visiteur invité peut ajouter un produit au panier, consulter le panier,
modifier son panier et accéder au checkout standard Odoo sans erreur,
avec une cohérence visuelle minimale et sans altérer website_sale.
```

Checkout invité Odoo 19 : `/shop/checkout` → `/shop/address` avec `marketone-checkout`.

---

## Lot 6 — Portes catalogue

**Objectif** : réintroduire prudemment l’orientation par portes (après stabilisation home / shop / product / cart / checkout).

**Stratégie** : **une porte à la fois** — démarrage par **Lot 6.1 Incontournables**.

**Lot 6.1 — Incontournables**

| Étape | Statut |
|-------|--------|
| Cadrage | **GO avec réserves** (2026-05-18) — [`TICKET_MARKETONE_LOT6_1_PORTE_INCONTOURNABLES.md`](../tickets/TICKET_MARKETONE_LOT6_1_PORTE_INCONTOURNABLES.md) |
| ADR-023 + CONTRATS C3.A | ✅ |
| Exécution | **GO avec réserves** — `19.0.6.0.0`, 60/60 tests — [`TICKET_MARKETONE_LOT6_1_INCONTOURNABLES_EXEC.md`](../tickets/TICKET_MARKETONE_LOT6_1_INCONTOURNABLES_EXEC.md) (clôturé) |
| Recette MOA | [`RECETTE_MANUELLE_LOT6_1.md`](../recette/RECETTE_MANUELLE_LOT6_1.md) — GO avec réserves |

**Lot 6.2 — Origines** (`19.0.7.0.0`)

| Étape | Statut |
|-------|--------|
| ADR-024 / Note univers | **GO MOA** (2026-05-18) |
| Cadrage | **GO avec réserves** — [`TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES.md`](../tickets/TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES.md) |
| ADR-025 + C3.B | ✅ |
| Exécution | **GO** — `19.0.7.0.0`, 76/76 tests — [`TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES_EXEC.md`](../tickets/TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES_EXEC.md) (clôturé) |
| Recette MOA | [`RECETTE_MANUELLE_LOT6_2.md`](../recette/RECETTE_MANUELLE_LOT6_2.md) — GO |

**Principe** : porte **Boutique** (`/shop`) ; récit territoire **Culture** — lots dédiés ultérieurs.

**Consolidation portes Boutique** (2026-05-18)

| Étape | Statut |
|-------|--------|
| Cadrage | **GO** — [`TICKET_MARKETONE_CONSOLIDATION_PORTES_BOUTIQUE.md`](../tickets/TICKET_MARKETONE_CONSOLIDATION_PORTES_BOUTIQUE.md) (clôturé, référence) |
| Photographie | `/shop` · `/incontournables` → `featured` · `/origines` → `origin` |
| Suite validée | **Culture v1 GO** — Lot 6.3+ sur décision MOA |

**Prérequis exploitation (consolidés)**

| Porte | Prérequis |
|-------|-----------|
| Incontournables | Catégorie publique avec **`website_id` = site courant** (obligatoire recette / pré-prod) ; paramètre `featured_public_category_id` |
| Origines | Profils `marketone.shop.origin` publiés sur le site courant ; attribut **Origine** |
| Alias | Redémarrage Odoo après `-u` pour `/incontournables` et `/origines` |

**Portes envisagées** (ordre indicatif)

| # | Porte | Filtre source (référence legacy) |
|---|-------|----------------------------------|
| 1 | Promotions | Pricelist items réducteurs |
| 2 | Kits/Packs | `pack_ok` (nécessite `product_pack` — décision dépendance) |
| 3 | Incontournables | Collection featured (param système) |
| 4 | Origines | Attribut Origine |
| 5 | Collections | M2M collection (modèle à redéfinir ou réutiliser) |
| 6 | Catégories | `product.public.category` |

**Doctrine**

```text
Les portes orientent.
Les filtres Odoo sélectionnent.
Marketone ne crée pas un moteur parallèle.
```

**Critère GO (par porte)**

```text
Alias ou lien → /shop?… → grille filtrée correcte → canonical cohérent → tests verts.
```

---

## Lots hors roadmap initiale (backlog)

À ne pas engager sans ticket MOA dédié :

- Compte professionnel / CRM (`website_crm`)
- Newsletter / Cercle (`mass_mailing`)
- Wishlist (`website_sale_wishlist`)
- Hero rotateur homepage
- Pages légales / recettes / offrir (contenu éditorial volumineux)
- Demande de rappel conseiller
- E2E paiement étendu

---

## Jalons et responsabilités

| Rôle | Responsabilité |
|------|----------------|
| Architecture | David + ChatGPT — doctrine, contrats |
| Développement | Agent IA — exécution ticket validé |
| Qualité | Codex — relecture, tests, régressions |
| Décision GO | Humaine |

---

## Environnement de référence

| Champ | Valeur |
|-------|--------|
| **Base** | `ckr-marketone-01` |
| **Instance** | `sandbox-odoo19-odoo-1` — http://localhost:18079 |
| **Documentation** | `docs/recette/ENV_REFERENCE.md` |
| **Décision** | ADR-013 |

Créée le 2026-05-18 : socle `website` + `website_sale` + `portal`, sans marketplace ni thème tiers.

---

## Univers Culture — Territoires v1

| Étape | Statut |
|-------|--------|
| Cadrage | **GO avec réserves légères** (2026-05-18) — [`TICKET_MARKETONE_CULTURE_TERRITOIRES_CADRAGE.md`](../tickets/TICKET_MARKETONE_CULTURE_TERRITOIRES_CADRAGE.md) |
| ADR-026 + C8 | ✅ |
| Exécution | **Clôturé — GO MOA** `19.0.8.0.0` — [`TICKET_MARKETONE_CULTURE_TERRITOIRES_EXEC.md`](../tickets/TICKET_MARKETONE_CULTURE_TERRITOIRES_EXEC.md) |
| Recette | [`RECETTE_MANUELLE_CULTURE_V1.md`](../recette/RECETTE_MANUELLE_CULTURE_V1.md) — **GO** |
| Grammaire URL | `/culture/guadeloupe` — alias Boutique `/origines` inchangé |
| Tests | **85** post-tests (Lots 1–6.2 + Culture v1), **0** failed |

**Réserve exploitation** : redémarrage Odoo post-`-u` si route Culture absente sur daemon déjà lancé.

---

## Culture v2 légère — Territoires additionnels

| Étape | Statut |
|-------|--------|
| Cadrage | **GO avec réserves** — [`TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_CADRAGE.md`](../tickets/TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_CADRAGE.md) |
| Exécution | **Livré** `19.0.9.0.0` — [`TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_EXEC.md`](../tickets/TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_EXEC.md) — recette MOA |
| Tests | **91** post-tests, **0** failed |
| ADR-027 + C8.v2 | ✅ |
| Lot 6.3 Boutique | **Gel MOA** |

---

## Prochaine action

1. **MOA** : recette Culture v2 — `martinique`, `reunion`, `guadeloupe`
2. **Lot 6.3+ Boutique** — **pas** d’ouverture immédiate
3. **Savoirs** — ticket séparé
