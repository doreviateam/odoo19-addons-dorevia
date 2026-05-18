# Roadmap — `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **Statut global** | Lot 2.1 GO avec réserves — Lot 4 ticket en préparation |
| **Dernière mise à jour** | 2026-05-18 (recette visuelle Lot 2.1) |
| **Décision de départ** | Nouveau module, pas de copie mécanique de `dorevia_ckreyol_marketplace` |

---

## Vue d’ensemble

```text
Lot 0  Cadrage + audit          ← GO (2026-05-18)
Lot 1  Socle installable        ← GO (2026-05-18)
Lot 2  Identité front minimale  ← GO (2026-05-18)
Lot 3  Boutique /shop propre    ← LIVRÉ
Lot 2.1 Design system minimal   ← GO avec réserves (`19.0.3.1.0`, 2026-05-18)
Lot 4  Fiche produit            ← TICKET PRÊT (validation humaine avant exécution)
Lot 5  Panier / checkout smoke
Lot 6  Portes catalogue
```

Chaque lot se clôture par une décision **GO / GO avec réserves / NO GO** humaine avant le lot suivant.

**Doctrine produit** (ADR-018) : C-Kreyol articule **vendre, raconter, transmettre** sans les confondre. Lots 1-5 = socle e-commerce ; Lot 6 = portes catalogue ; lots suivants = éditorial et connaissance. Voir `cadrage/ARCHITECTURE.md` §2.

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

**Statut** : ticket préparé — **aucune exécution** avant validation humaine du ticket.

**Ticket** : `docs/tickets/TICKET_MARKETONE_LOT4_PRODUCT.md`

**Prérequis** : GO Lot 2.1 (obtenu avec réserves).

**Objectif** : fiche produit crédible pour ouverture commerciale, **au moins au niveau visuel** du design system Artisanal Terroir (Lot 2.1).

**Garde-fous ADR-018 / C7.4**

- Produit et CTA d'achat prioritaires
- Récit / réassurance en appui, pas d'article encyclopédique
- Pas de couche « savoir » lourde au Lot 4

**Critère GO**

```text
Une fiche produit peut être consultée, comprise et ajoutée au panier sans friction.
```

**Condition** : données produit propres en BO — sinon **GO avec réserves** ou report.

---

## Lot 5 — Panier / checkout smoke

**Objectif** : sécuriser le tunnel standard Odoo.

**Contenu attendu**

- Tests panier et checkout minimal (invité)
- Pas de refonte checkout
- Micro-ajustements visuels éventuels

**Critère GO**

```text
Un client invité peut ajouter au panier et progresser dans le tunnel
sans erreur 500 ni rupture visuelle majeure.
```

**Réserve** : E2E paiement avec `payment_demo` = tag séparé, non bloquant pour GO shop.

---

## Lot 6 — Portes catalogue

**Objectif** : réintroduire prudemment l’orientation par portes (après stabilisation home / shop / product / cart / checkout).

**Prérequis**

- Lots 1 à 5 validés
- Contrats URL mis à jour dans `cadrage/CONTRACTS.md`
- Un tag de test par porte

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

## Prochaine action

1. Validation humaine du ticket `TICKET_MARKETONE_LOT2_1_DESIGN_SYSTEM_MINIMAL`
2. Exécution Lot 2.1 après GO
3. Ticket Lot 4 après GO Lot 2.1
