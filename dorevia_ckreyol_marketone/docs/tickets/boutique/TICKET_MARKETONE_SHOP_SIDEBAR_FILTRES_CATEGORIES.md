# TICKET — Raffinement UX sidebar filtres boutique

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_SHOP_SIDEBAR_FILTRES_CATEGORIES` |
| **Type** | **UX / front** — héritage QWeb + SCSS sous `.marketone-shop` |
| **Statut** | **Clôturé GO MOA** — facette multi OR + combinaison facettes · réf. **`19.0.10.8.0`** (2026-05-19) |
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079/shop |
| **Prérequis** | Lot 3 `/shop` livré · Lots 6.1 / 6.2 portes · **ticket BO catégories clôturé GO MOA** |
| **Ticket BO lié (clôturé)** | [`TICKET_MARKETONE_CATALOGUE_CATEGORIES_BO_RECETTE.md`](./TICKET_MARKETONE_CATALOGUE_CATEGORIES_BO_RECETTE.md) |
| **Doctrine** | [ADR-029](../../cadrage/DECISIONS.md#adr-029--taxonomie-catalogue-convention-odoo-catégories-e-commerce) · [C3.C](../../cadrage/CONTRACTS.md#c3c--taxonomie-catalogue-moa-2026-05-19) · [C3.7](../../cadrage/CONTRACTS.md#c3--filtres-catalogue-lot-6) |
| **Mapping BO (inchangé)** | [`MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md`](../../cadrage/MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md) |

---

## Statut par rapport au lot Catégories BO

Le ticket BO catégories est **clôturé GO MOA** :

- mapping appliqué sur `ckr-marketone-01` ;
- recette [`RECETTE_MANUELLE_CATALOGUE_CATEGORIES.md`](../../recette/boutique/RECETTE_MANUELLE_CATALOGUE_CATEGORIES.md) signée ;
- aucune anomalie technique ;
- **aucun changement de code** dans ce lot.

**Ce ticket ne remet pas en cause** le mapping ni la taxonomie BO.

```text
BO = rattachements product.public.category (principale + secondaires).
UX = ce que le visiteur voit et utilise dans la sidebar /shop.
```

---

## Objectif

Améliorer la **lisibilité** et l’**usage** de la **sidebar gauche** sur `/shop`.

La sidebar devient l’espace principal de **filtrage catalogue** (complément des portes éditoriales, hors navigation haute).

**Question utilisateur ciblée** (alignée ADR-029) :

> *« Quel type de produit est-ce que je cherche ? »*

---

## Décision MOA

Dans un **premier temps**, afficher uniquement les **catégories principales** dans le bloc **Catégories** de la sidebar `/shop`.

Les catégories affichées servent à **filtrer** le catalogue — pas à créer une navigation éditoriale parallèle.

---

## Cible UX immédiate

La sidebar gauche présente les filtres dans cet **ordre** :

| # | Bloc |
|---|------|
| 1 | **Origine** |
| 2 | **Catégories** |
| 3 | **Fourchette de prix** |

> Réordonnancement visuel autorisé par héritage template / SCSS — le moteur reste `website_sale` (C1, C3.7).

---

## Catégories à afficher (allowlist — 13 principales)

Afficher **uniquement** ces libellés dans le bloc **Catégories** :

1. Biscuits salés
2. Biscuits sucrés
3. Épices
4. Assaisonnements
5. Sauces
6. Condiments
7. Confitures
8. Sirops
9. Boissons
10. Farines
11. Fécules
12. Kits & Coffrets
13. Miels

**Interaction** : cases à cocher ou liens filtrants — **selon le standard Odoo 19** retenu sur le template filtres (ne pas inventer un moteur de filtre parallèle).

**Ordre d’affichage** : liste ci-dessus (ordre MOA des rayons).

---

## Catégories secondaires — non affichées (cette passe)

**Ne pas afficher** dans le bloc **Catégories** de la sidebar :

- Incontournables
- Apéritif créole
- Cuisine du manioc
- Idées cadeaux

Ces catégories **restent** en BO et dans le mapping validé (secondaires, portes, parcours ultérieurs).

| Secondaire | Rôle actuel (hors sidebar) |
|------------|----------------------------|
| Incontournables | Porte Lot 6.1 · `marketone_mode=featured` |
| Apéritif créole · Cuisine du manioc · Idées cadeaux | Ticket ultérieur (mise en avant / navigation) |

---

## Hors périmètre

| Exclu | Raison |
|-------|--------|
| Navigation haute | Ticket séparé |
| Portes éditoriales (Promo, Kits, Collections…) | Lot 6.3+ gelé |
| `marketone.shop.collection` | ADR-029 — reporté |
| Savoirs v1 | Chantier distinct |
| Origines / Culture (récit, harmonisation BO) | Chantier distinct |
| Distinction technique **principale / secondaire** en BO | Ticket contrainte ultérieur |
| Modification des rattachements BO | Ticket BO **clôturé** |
| Menu transversal **Catégories** (header) | Cible UX ultérieure |

---

## Règles de non-régression

Ce ticket **ne remet pas en cause** :

- le **GO MOA** BO catégories ;
- la recette catalogue ;
- la règle **1 principale + 0 à 3 secondaires** (max 4 en BO) ;
- les rattachements existants sur les 27 produits ;
- le filtre porte **Incontournables** (`/incontournables` → `featured`) ;
- le filtre **Origines** (Lot 6.2) lorsque `marketone_mode=origin` ou facette attribut.

---

## Piste d’implémentation (indicative — à valider à l’exec)

| Élément | Approche attendue |
|---------|-------------------|
| Moteur | `website_sale` — domaine / facettes existantes |
| Templates | Héritage `website_sale.products` (ou template filtres sidebar Odoo 19) sous `.marketone-shop` |
| Allowlist | Liste figée des 13 libellés (`MARKETONE_PRIMARY_PUBLIC_CATEGORY_NAMES`) ; paramètre optionnel `dorevia_ckreyol_marketone.primary_public_category_ids` — **transitoire** documenté |
| Sidebar Odoo 19 | `opt_wsale_categories` forcé à `True` ; `opt_wsale_categories_top` forcé à `False` (pas de filmstrip) |
| Masquage secondaires | Filtrer les entrées `product.public.category` rendues dans le bloc Catégories |
| Style | `static/src/scss/_shop.scss` — scope `.marketone-shop` uniquement (Lot 3) |
| Tests | Tag `dorevia_marketone_shop_sidebar` — **12** tests (HttpCase + modèle), **0** failed |

**Interdit** : nouveau modèle · JS lourd · domaine catalogue parallèle au contrôleur.

---

## Recette MOA (2026-05-19) — livraison

| Verdict | Périmètre |
|---------|-----------|
| **GO visuel V2** | Bloc **Catégories** harmonisé avec **Origine** (accordéon + `form-check`) ; **13** principales ; pas de « Tous les produits » |
| **GO fonctionnel Option A** | Facette `marketone_category` multi **OU** ; combinaison **AND** avec Origine / Prix ; symétrie **4d** / **4e** |
| **Version livrée** | **`19.0.10.8.0`** — recette [`RECETTE_MANUELLE_SHOP_SIDEBAR_CATEGORIES.md`](../../recette/boutique/RECETTE_MANUELLE_SHOP_SIDEBAR_CATEGORIES.md) signée MOA (`19.0.10.7.0` + patch Effacer les filtres) |

### Comportement attendu MOA (multi — à arbitrer)

- Cocher une catégorie **ajoute** au filtre courant ; une deuxième **ne remplace pas** la première.
- Logique **OU** entre catégories cochées (ex. Biscuits salés **OU** Épices).
- Les autres filtres (Origine, Prix, portes…) se **combinent** normalement (AND avec le périmètre catégories).
- Décocher retire la catégorie ; **aucune** case cochée = catalogue global `/shop`.

---

## Arbitrage technique — mono vs multi (signal avant implémentation)

### Ce que fait Odoo 19 `website_sale` en standard

| Mécanisme | Comportement natif |
|-----------|-------------------|
| URL | **Une** catégorie via chemin `/shop/category/<slug>` (pas de multi-sélection sidebar) |
| Domaine | `public_categ_ids` **`child_of`** la catégorie courante (hiérarchie incluse) |
| UI sidebar | Liste de **liens** (ou filmstrip haut) — pas de cases multi-catégories |
| Query `?category=` | **Déprécié** → redirection 301 vers le chemin canonique |

**Conclusion** : le **standard `website_sale` ne fournit pas** le multi-catégorie en cases à cocher dans la sidebar. Ce n’est pas un simple réglage QWeb.

### Ce qui reste « propre » sans moteur catalogue parallèle

Le **domaine Odoo** supporte déjà le **OU** multi-catégories sur les rattachements existants :

```python
("public_categ_ids", "in", [id_biscuits_sales, id_epices])
```

→ produit ayant **au moins une** des catégories cochées (logique OR).

**Pattern déjà validé sur le legacy CK** (même socle `website_sale`) :

- Facette query répétable : `ckr_category=<slug>&ckr_category=<slug>…`
- Hooks **`_get_search_options`** + **`_get_shop_domain`** + **`product.template._search_get_detail`** (même convergence grille / min-max / pagination que les portes Marketone 6.1 / 6.2)
- **Pas** de modèle ni de contrôleur catalogue alternatif

**Piste Marketone** (si MOA confirme le **multi**) :

| Composant | Rôle |
|-----------|------|
| Paramètre | `marketone_category=<slug>` (répétable, allowlist 13 principales) |
| Contrôleur | Lecture slugs → IDs ; injection `marketone_public_category_ids` dans options (symétrique featured / origin) |
| `product.template` | Extension `_search_get_detail` — domaine `public_categ_ids in …` |
| QWeb | Cases cochées selon slugs actifs ; état « aucune » = `/shop` sans facettes catégorie |
| JS **léger** | Au changement de case : navigation `GET /shop?…` (comme CK) — catégories **hors** du formulaire `js_attributes` natif |

**Impact périmètre ticket** : passage de **UX/QWeb seul** à **UX + hook contrôleur existant + JS minimal** — toujours sous doctrine `website_sale`, mais **niveau fonctionnel élargi** par rapport au cadrage initial « pas de JS lourd ».

### Options MOA

| Option | UX | Fonctionnel | Effort |
|--------|----|-------------|--------|
| **A — Multi (recommandé si cases)** | Cases (V2 validée) | OU multi-catégories ; combine avec Origine / Prix | Hook + JS léger + tests |
| **B — Mono** | Revenir à liens / radio implicite | Standard Odoo path unique | Pas d’extension domaine ; **incohérent** avec attente cases multi |
| **C — Report** | V2 figée en recette | Multi = ticket / lot dédié | Clôture partielle visuelle seulement |

**Recommandation technique** : si l’UX reste en **cases à cocher**, acter l’**option A**. L’option B ne satisfait pas le comportement décrit par le MOA.

---

## Critères GO

| ID | Critère |
|----|---------|
| G1 | La sidebar affiche clairement le bloc **Catégories** |
| G2 | **Seules** les 13 catégories principales sont visibles dans ce bloc |
| G3 | Les catégories sont lisibles et utilisables (checkbox ou lien — standard Odoo) |
| G4 | Le filtre par catégorie **fonctionne** sur `/shop` (grille cohérente) |
| G5 | La grille produits reste **visible** et cohérente (C4) |
| G6 | Le filtre **Origine** reste fonctionnel |
| G7 | Le filtre **Prix** reste fonctionnel |
| G8 | Les **4** catégories secondaires ne sont **pas** affichées dans ce bloc |
| G9 | **Aucun** changement de doctrine / rattachements BO |
| G10 | Porte **Incontournables** et mode **origin** : non-régression (smoke) |
| G11 | Cocher **Biscuits salés** + **Épices** → grille = union OR ; décocher retire ; 0 case = `/shop` global | ☑ | ☑ |
| G12 | **Aucun** bandeau horizontal catégories au-dessus de la grille (`opt_wsale_categories_top` désactivé sur `/shop`) | ☑ | ☑ |

---

## Recette

[`RECETTE_MANUELLE_SHOP_SIDEBAR_CATEGORIES.md`](../../recette/boutique/RECETTE_MANUELLE_SHOP_SIDEBAR_CATEGORIES.md) — grille MOA + captures :

- `/shop` sidebar ordre Origine · Catégories · Prix ;
- filtre **Biscuits salés** ;
- absence de **Incontournables** dans le bloc Catégories ;
- non-régression `/incontournables` et facette Origine.

---

## Suite documentée

| Sujet | Ticket / chantier |
|-------|-------------------|
| **Facettes contextuelles (C4)** | [`TICKET_MARKETONE_SHOP_SIDEBAR_FACETTES_CONTEXTUELLES.md`](./TICKET_MARKETONE_SHOP_SIDEBAR_FACETTES_CONTEXTUELLES.md) — **Clôturé GO MOA** `19.0.10.9.0` |
| Secondaires dans l’UI (hors sidebar Catégories) | À cadrer |
| Contrainte BO principale / max 4 | Ticket technique post-mapping |
| Menu header Catégories | UX ultérieur |

---

## Références

- [`TAXONOMIE_CATALOGUE.md`](../../cadrage/TAXONOMIE_CATALOGUE.md)
- [`TICKET_MARKETONE_LOT3_SHOP.md`](../lots/TICKET_MARKETONE_LOT3_SHOP.md)
- [`TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES_EXEC.md`](../lots/TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES_EXEC.md)
- [`recette/reference/ENV_REFERENCE.md`](../../recette/reference/ENV_REFERENCE.md)
