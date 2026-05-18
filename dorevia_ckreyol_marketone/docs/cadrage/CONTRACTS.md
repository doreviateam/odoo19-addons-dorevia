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
| `marketone_mode` | `promo`, `pack`, `origin`, `collection` | Lots 6.2+ |
| `marketone_collection` | slug collection | Lot 6.x collections |

```text
/shop?marketone_mode=featured          # canonique Incontournables (Lot 6.1)
/incontournables                       # alias 301 → ci-dessus
```

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
| C3.6 | **Lot 6.1** : un seul mode actif — `marketone_mode=featured` uniquement. |
| C3.7 | **Lot 6.1** : filtres natifs Odoo sur `/shop` (sidebar, tri, attributs) **conservés**. |

### C3.A — Porte Incontournables (Lot 6.1 — figé cadrage 2026-05-18)

| Élément | Règle |
|---------|-------|
| Mode URL | `marketone_mode=featured` |
| Libellé MOA | **Incontournables** (pas le mot « featured » côté visiteur) |
| Entrée alias | `GET /incontournables` → **301** → `/shop?marketone_mode=featured` |
| Source produits | `ir.config_parameter` `dorevia_ckreyol_marketone.featured_public_category_id` → `product.public.category` nommée **Incontournables** |
| Multi-catégories | Un produit peut avoir plusieurs catégories publiques ; le filtre porte = appartenance à cette catégorie |
| Modèle custom | **Non** au Lot 6.1 (`marketone.shop.collection` reporté) |
| Présentation | Titre + intro courte + lien « Tous les produits » sous `.marketone-shop` — pas de hero, pas de chips multi-portes |
| SEO | `canonical` / `noindex` : **documenter** ; hors scope élargi exécution Lot 6.1 |

**Sources de vérité — autres portes** (Lots 6.2+)

| Porte | Source |
|-------|--------|
| Promotions | `product.pricelist.item` réducteur |
| Kits/Packs | `product.template.pack_ok` (si `product_pack` activé) |
| Origines | Attribut produit « Origine » |
| Collections éditoriales | Modèle ou mécanisme à définir (hors 6.1) |
| Catégories merchandising | `product.public.category` (navigation générale) |

**Statut** : C3.A **implémenté Lot 6.1** — GO avec réserves (recette MOA 2026-05-18). Prérequis BO : catégorie avec `website_id` site courant (cf. ADR-023).

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

**Statut** : Lot 6 pour paramètres filtres ; Lot 1 peut poser l’extension `website` vide.

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
| Porte promo | `dorevia_marketone_promo` | 6.2+ |
| … | … | 6 |

---

## Amendements

Toute modification de ce fichier après validation Lot 0 doit :

1. Être datée dans `cadrage/DECISIONS.md`
2. Préciser le lot impacté
3. Ne pas présenter une ambition non livrée comme contractuelle
