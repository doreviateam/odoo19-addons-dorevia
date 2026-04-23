# Contrat d’URL de la porte **Catégories** — analyse et décision

| Champ | Valeur |
|--------|--------|
| **Statut** | **Tranché et déployé** — Hybride **H1 — cible native** (2026-04-22, module **19.0.1.3.0**). Voir §12 « Décision actée » et §13 « Mise en service ». |
| **Date** | 2026-04-22 |
| **Périmètre** | Forme de l’URL empruntée par la carte **Catégories** de la section Explorer pour ouvrir la boutique en **lecture par famille de produits** (`product.public.category`). |
| **Prérequis actés** | **Standard Odoo** pour le filtrage e-commerce ([SPEC_SHOP_PORTES §4.4](SPEC_SHOP_PORTES.md)) ; **convergence boutique** sans vitrine parallèle ([ADR-CKR-007](../ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007)) ; **pas de réouverture** des portes Pack / Promotions ni du paramètre `ckr_mode` pour cette porte. |

---

## 1. Cadre doctrinal rappelé

1. **Standard Odoo d’abord** ([ADR-CKR-001](../ARCHITECTURE_DECISION_RECORD.md#adr-ckr-001)) : la taxonomie e-commerce est **`product.public.category`** ; le contrôleur **`website_sale`** sait déjà servir **`/shop/category/<id>-<slug>`** avec fil d’Ariane, facettes et pagination natifs.
2. **Convergence commerciale** ([ADR-CKR-007](../ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007)) : la destination reste la **boutique** — le chemin **`/shop/category/…`** est une **forme native** de la même destination que **`/shop`** (pas de catalogue HTML parallèle).
3. **Capitalisation du patron H1** : comme pour **`/kits`** et **`/promotions`**, on conserve une **URL courte visiteur** dédiée à la carte Explorer, résolue par **redirection HTTP 301** vers la **forme canonique** retenue — ici la **cible technique est l’URL Odoo native**, pas ` /shop?ckr_mode=…` (évite de réimplémenter le domaine catégorie côté CK).
4. **Construction CK minimale** ([ADR-CKR-002](../ARCHITECTURE_DECISION_RECORD.md#adr-ckr-002)) : une route d’alias + une résolution déterministe de la catégorie d’entrée ; **aucun** second filtre produit CK.

---

## 2. État des lieux (SPEC Phase 2)

La [SPEC_SHOP_PORTES §4.4](SPEC_SHOP_PORTES.md#44-catégories) posait déjà :

| Élément | Contenu |
|--------|---------|
| **Source de vérité** | `product.public.category` + produits publiés. |
| **Préférence URL** | **`/shop/category/<id>-<slug>`** (aligné sur Odoo). |
| **Variante « hub »** | **`/shop`** nu si l’on ne veut pré-sélectionner aucune famille. |

Le lien Explorer pointait encore sur **`/shop`** sans contexte : **transitoire** à lever.

---

## 3. Options pour le **véhicule d’URL** (comparatif bref)

### 3.1 Option A — Lien direct vers une catégorie native (sans alias)

- **Mécanisme** : la carte Explorer pointe en dur ou via QWeb dynamique vers **`/shop/category/<id>-<slug>`**.
- **Avantages** : zéro route CK ; URL canonique immédiate.
- **Inconvénients** : dans notre module **statique** (`ckr_entries.xml`), l’**id** dépend du contenu de base ; risque de casse à l’import / copie de site ; pas d’URL mémorable unique **`/categories`** pour campagnes et analytics homogènes avec les autres portes.

### 3.2 Option B — `ckr_mode=category` + filtre CK

- **Mécanisme** : parallèle strict à Pack / Promotions : `/shop?ckr_mode=category` + domaine CK.
- **Inconvénient doctrinal majeur** : **duplique** la logique déjà portée par **`website_sale`** sur **`/shop/category/…`** (breadcrumb, règles d’accès, SEO, sitemap) ; charge de maintenance et risque de divergence avec le standard.

**Verdict** : **non retenu**.

### 3.3 Option C — **Hybride H1 — cible native** *(retenu)*

- **URL visiteur** (carte Explorer, partages courts) : **`/categories`**.
- **Mécanisme** : route CK → **HTTP 301** vers **`/shop/category/<id>-<slug>`** où `<id>-<slug>` est produit par **`env["ir.http"]._slug(record)`** (même API que `website_sale.controllers.main.WebsiteSale._get_shop_path` — Odoo 19 ne réexporte plus `slug` depuis `http_routing.models.ir_http`).
- **Résolution de la catégorie cible** : voir §12.2 (paramètre système optionnel + repli sur la première racine publique du site).
- **Repli** : si aucune catégorie publique n’existe → **301** vers **`/shop`** nu (comportement sûr, cohérent avec la variante « hub »).

**Verdict** : **retenu** — même esprit que H1 (court → canonique), **sans** `ckr_mode`, **sans** surcouche de domaine produit.

---

## 4. Cohabitation avec les portes `ckr_mode`

Les requêtes **`/categories?ckr_mode=pack`** (etc.) sont **normalisées** : le paramètre **`ckr_mode`** est **retiré** lors de la construction de l’URL cible pour éviter un mélange ambigu avec le contexte catégorie natif. Les autres paramètres (`search`, `order`, …) restent **préservés** s’ils sont présents.

---

## 12. Décision actée (gel)

### 12.1 Véhicule d’URL

| Axe | Décision |
|-----|----------|
| **URL visiteur** | **`/categories`** |
| **Redirection** | **HTTP 301** permanente |
| **URL technique canonique** | **`/shop/category/<id>-<slug>`** (native `website_sale`) |
| **Paramètre CK** | **Aucun** — pas d’extension de la whitelist `ckr_mode` pour cette porte. |
| **Canonical** | **Géré par Odoo** sur la page catégorie ; **aucune** exception dans `website._get_canonical_url` du module CK. |

### 12.2 Résolution de la catégorie d’entrée

| Priorité | Règle |
|----------|--------|
| **1 — Paramètre** | Si `ir.config_parameter` **`dorevia_ckreyol_marketplace.explorer_public_category_id`** contient un **entier > 0** désignant une `product.public.category` **existante** et **compatible site** (`website_id` vide ou = site courant) → cette catégorie sert d’entrée. |
| **2 — Repli** | Sinon → **première racine** (`parent_id` absent) du site, ordre **`sequence`, `id`**, domaine site identique à (1). |
| **3 — Absence** | Si toujours aucun record → redirection vers **`/shop`**. |

Fichier data : `data/ckr_explorer_category_parameter.xml` (valeur initiale **`0`** = laisser le repli automatique).

### 12.3 Présentation visiteur

Le **titre** et le **breadcrumb** sont ceux **natifs** de la page catégorie Odoo. **Pas** de bandeau CK du type Pack / Promotions : la SPEC demandait déjà une lecture cohérente avec le **standard** ; un bandeau « Catégories » ferait double emploi avec le H1 / fil d’Ariane natif.

---

## 13. Mise en service (19.0.1.3.0)

### 13.1 Livrables techniques

| Fichier | Rôle |
|---------|------|
| `models/product_public_category.py` | `_ckr_get_explorer_entry_shop_path(website)` + helpers de validation / domaine racine. |
| `controllers/website_sale_ckr.py` | Route **`/categories`** → 301 vers chemin résolu ; strip de `ckr_mode` sur les query params entrants. |
| `data/ckr_explorer_category_parameter.xml` | Paramètre système (clé documentée §12.2). |
| `views/snippets/ckr_entries.xml` | `href` carte **Catégories** : **`/categories`**. |
| `__manifest__.py` | Version **19.0.1.3.0** ; data + description. |

### 13.2 Documentation synchronisée

| Document | Mise à jour |
|----------|-------------|
| [SPEC_SHOP_PORTES.md](SPEC_SHOP_PORTES.md) | §4.4, snapshot, synthèse §5, checklist §6, historique. |
| [ARCHITECTURE_DECISION_RECORD.md](../ARCHITECTURE_DECISION_RECORD.md) | Historique (décision + déploiement). |
| [README.md](../../README.md) | Statut des portes Explorer. |

### 13.3 Vérifications attendues (recette)

1. **`/categories`** → **301** vers un chemin **`/shop/category/…`** dès qu’au moins une catégorie publique racine existe.
2. Avec paramètre explicite → la catégorie configurée est ciblée.
3. **Préservation** `?search=…&order=…` ; **absence** de `ckr_mode` dans l’URL cible si présent en entrée sur `/categories`.
4. **Non-régression** : `/kits`, `/promotions`, `/shop?ckr_mode=pack` inchangés.

**Constat sandbox `tenant_o7` (2026-04-22)** — après **`-u dorevia_ckreyol_marketplace`** et **`docker restart sandbox-odoo19-odoo-1`** (rechargement registry HTTP) :

| # | Scénario | Attendu | Observé |
|---|----------|---------|--------|
| A | `GET /categories` + `X-Odoo-Database: tenant_o7` | 301 `Location: /shop/category/…` | ✅ `301` → `/shop/category/biscuits-1` |
| B | `GET /categories?search=foo&order=name+asc&ckr_mode=pack` | 301, `ckr_mode` absent de la cible, autres params conservés | ✅ `Location: …/biscuits-1?search=foo&order=name+asc` |
| C | `GET` sur l’URL catégorie issue de (A) | 200 | ✅ `200` |
| D | `/kits`, `/promotions` | 301 vers shop pack/promo | ✅ inchangé |
| E | `/` contient lien Explorer | `href="/categories"` | ✅ |

---

## 14. Références

- [SPEC_SHOP_PORTES.md §4.4](SPEC_SHOP_PORTES.md#44-catégories)
- [CONTRAT_URL_PACKS.md](CONTRAT_URL_PACKS.md) — patron H1 avec `ckr_mode` (contraste utile).
- [CONTRAT_URL_PROMOTIONS.md §13.6](CONTRAT_URL_PROMOTIONS.md) — check-list de capitalisation (adapter quand la cible 301 n’est pas `/shop?ckr_mode=…`).
- [ADR-CKR-007](../ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007), [ADR-CKR-008](../ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008)

---

## Historique du document

| Date | Changement |
|------|------------|
| 2026-04-22 | Création — analyse courte ; décision **H1 — cible native** ; §12–13 mise en service ; lien SPEC / ADR / README. |
| 2026-04-22 | **Implémentation technique** : remplacement de l’import `slug` depuis `http_routing` (inexistant en Odoo 19) par **`env["ir.http"]._slug(category)`**, aligné sur `website_sale` — évite `ImportError` au chargement du module. **§13.3** complété par les résultats HTTP réels sur `tenant_o7` (redémarrage conteneur nécessaire pour prise en compte de la route `/categories` côté worker HTTP). |
