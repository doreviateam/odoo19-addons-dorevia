# TICKET — Lot 4 Fiche produit `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_LOT4_PRODUCT` |
| **Lot** | 4 — Fiche produit retail C-Kreyol |
| **Statut** | **GO avec réserves mineures** (recette MOA 2026-05-18) |
| **Version livrée** | `19.0.4.0.0` |
| **Base** | `ckr-marketone-01` |
| **Prérequis** | GO Lot 2.1 avec réserves (2026-05-18) ; Lots 1, 2, 3 livrés |
| **Version cible module** | `19.0.4.0.0` (proposition) |
| **Référence design** | Design system Artisanal Terroir (Lot 2.1) — **ne pas dégrader** |
| **Inspirations externes** | 750g, Caribshopper (ADR-019) — **hors périmètre Lot 4** ; lots éditoriaux ultérieurs |

---

## Objectif

Rendre la **fiche produit** (`/shop/<product>`) lisible, **mobile-first** et crédible **retail** pour C-Kreyol, en prolongeant le design system Artisanal Terroir, **sans modifier le moteur** `website_sale`.

```text
Critère GO Lot 4 :
Une fiche produit peut être consultée, comprise et ajoutée au panier sans friction.
Le rendu visuel est au moins au niveau du design system Lot 2.1 (home, shop, chrome).
```

---

## Contexte

| Élément | État |
|---------|------|
| Lot 2.1 | GO avec réserves — enveloppe Artisanal Terroir (`19.0.3.1.0`) |
| Lot 3 | `/shop` avec `marketone-shop` + `_shop.scss` |
| Fiche produit actuelle | Template `website_sale.product` natif — **sans** `marketone-product` |
| Doctrine produit | ADR-018 — vendre, raconter, transmettre **sans confondre** |
| Contrat | C7 (fiche produit), C7.4 fiche non encyclopédique |

**Rappel doctrine technique** : Marketone **présente** ; Odoo **vend**.

**Références MOA 750g / Caribshopper (ADR-019)** : inspiration pour les dimensions « raconter » et « transmettre » sur le **long terme** — **sans** élargir le Lot 4 (pas de densité média, pas de logique marketplace, fiche non encyclopédique).

**Réserves Lot 2.1 reportées au Lot 4 (recette)**

- Créer **2 à 3 produits de recette en BO** pour valider cartes `/shop` et fiche produit — **pas de seed XML** dans le module. Images : banque `dorevia_ckreyol_marketplace/docs/assets/` (`homepage_*`, `exemple_produit_*`) — voir `docs/recette/ASSETS_REFERENCE.md` (ADR-020).
- Page Contact native : **hors périmètre** (ticket futur).

---

## Doctrine (garde-fous ADR-018)

| Règle | Lot 4 |
|-------|-------|
| Produit d'abord | Titre, prix, image, variantes, CTA « Ajouter au panier » restent dominants |
| Récit ensuite | Blocs éditoriaux **légers** uniquement si champs BO renseignés |
| Savoir en prolongement | **Pas** de bibliothèque, recettes longues, glossaire au Lot 4 |
| C7.4 | **Pas** d'article encyclopédique ; CTA d'achat non brouillé |
| Moteur | `website_sale` inchangé (panier, variantes, quantités, options) |
| Scope CSS | **`.marketone-product`** uniquement sur la fiche produit |
| Scope shop / home | `.marketone-shop` et `.marketone-root` **inchangés** |
| Design system | Réutiliser tokens Lots 2.1 — pas de palette parallèle |
| Pas de JS | Aucun fichier JS |
| Pas de portes | Pas de `marketone_mode`, filtres métier, alias catalogue |

---

## Périmètre inclus

### 1. Stratégie d'intégration — ancre CSS unique

Patron identique au Lot 3 :

1. Héritage **minimal** sur `website_sale.product`.
2. Ajout de la classe `marketone-product` sur `div[@id='wrap']` (attribut `class`, `add`, pas `replace`).
3. Styles dans `static/src/scss/_product.scss` sous **`.marketone-product`** uniquement.

| Template Odoo | Page | Lot 4 |
|---------------|------|-------|
| `website_sale.products` | `/shop` | **Non** — déjà `marketone-shop` (Lot 3) |
| `website_sale.product` | `/shop/<product>` | **Oui** — `marketone-product` |

### 2. QWeb

| Fichier | Rôle |
|---------|------|
| `views/pages/product.xml` | Héritage `website_sale.product` — classe `marketone-product` sur `#wrap` |

**Contraintes QWeb**

- `priority` ≤ 20 (contrat C5.4).
- Pas de `<style>` inline.
- Pas de `replace` du `#wrap`, de la galerie, du formulaire panier, ni du bloc prix.
- Pas d'insertion de blocs éditoriaux **inventés** sans données BO.
- QWeb éditorial **optionnel** et **minimal** : uniquement si un champ produit / website existe et est documenté — sinon **CSS seul** au Lot 4.

### 3. SCSS — `_product.scss`

Chargé **après** `_shop.scss` dans le manifeste.

**Cibles autorisées** (sous `.marketone-product` uniquement) :

| Zone | Intention |
|------|-----------|
| Fond page | Cohérence `$marketone-bg` / `$marketone-bg-soft` |
| Titre produit (H1) | EB Garamond, hiérarchie claire |
| Prix | Lisibilité, contraste, alignement |
| Galerie / images | Respiration, radius cohérent Lot 2.1 |
| Description / onglets | Typo body Hanken Grotesk, lisibilité mobile |
| CTA primaire | `@include marketone-btn-primary` ou équivalent scoped |
| Bloc réassurance | **Optionnel** — style léger si présent en BO |
| Breadcrumb / retour boutique | Lisibilité sans casser le natif |

**Interdictions SCSS**

- Pas de règles hors `.marketone-product` (sauf tokens / mixins partagés).
- Pas de `!important` (C4.3).
- Pas de `display: none` sur CTA panier, quantité, variantes.
- Pas de styles sur `/shop` liste (reste `.marketone-shop`).
- Pas de refonte layout Odoo (colonnes gallery / details).

**Volume cible** : fichier **léger** (< 200 lignes).

### 4. Manifeste

- Version : **`19.0.4.0.0`**
- `data` : ajouter `views/pages/product.xml`
- `assets` : ajouter `_product.scss` après `_shop.scss`

Ordre bundle (inchangé sauf ajout final avant `marketone.scss`) :

```text
_tokens_* → _layout → _buttons → _header → _footer → _home → _shop → _product → marketone.scss
```

### 5. Tests

| Tag | Fichier |
|-----|---------|
| `dorevia_marketone_lot4` | `tests/test_marketone_lot4_product.py` |

**Tests proposés** (`HttpCase`, `post_install`) :

1. `test_product_http_200` — fiche produit accessible → 200
2. `test_product_has_marketone_product_scope` — HTML contient `marketone-product`
3. `test_shop_has_no_marketone_product` — `/shop` contient `marketone-shop`, **pas** `marketone-product`
4. `test_home_has_no_marketone_product` — `/` sans `marketone-product`
5. `test_product_has_add_to_cart` — présence contrôle ajout panier (structure `website_sale`)
6. `test_product_no_catalog_gates` — pas de `marketone_mode=`, `/promotions`, etc.
7. Non-régression : `dorevia_marketone_smoke`, `lot2`, `lot2_1`, `lot3`

**Produit de test** : créer 1 produit en `setUpClass` si catalogue vide (comme Lot 3) — **pas de seed XML module**.

### 6. Documentation

- ADR-019 dans `cadrage/DECISIONS.md` après livraison
- `pilotage/ROADMAP.md`, `recette/ENV_REFERENCE.md`, `docs/README.md`

---

## Hors périmètre

| Exclusion | Report |
|-----------|--------|
| Liste `/shop` | Lot 3 — `marketone-shop` |
| Panier, checkout, paiement | Lot 5 |
| Portes catalogue, `_search_get_detail` | Lot 6 |
| Page Contact `/contactus` | Ticket futur « Contact minimal C-Kreyol » |
| Champs produit custom / modèles | Hors Lot 4 sauf validation MOA explicite |
| JavaScript, contrôleur, modèle `website.py` | Non |
| Seed XML produits | Non (recette BO manuelle) |
| Couche « savoir » (recettes, glossaire) | Lots ultérieurs |
| Header / footer globaux | Lot 2.1 — ne pas régresser |
| Wordmark logo | Réserve MOA |

---

## Recette visuelle (MOA)

**Plan de recette** : [`docs/recette/RECETTE_MANUELLE_LOT4.md`](../recette/RECETTE_MANUELLE_LOT4.md) (fiche Lot 4) · plan complet [`RECETTE_MANUELLE.md`](../recette/RECETTE_MANUELLE.md)

**Prérequis BO** : 2 à 3 produits publiés avec image, prix, description courte.

| Zone | À vérifier |
|------|------------|
| Fiche desktop / mobile | Lisibilité titre, prix, galerie, CTA |
| Cohérence Artisanal Terroir | Palette, typo, boutons alignés Lots 2.1 / 3 |
| CTA achat | Visible, non masqué, fonctionnel |
| Non-régression | Header, footer, `/`, `/shop` inchangés visuellement |
| Panier | Ajout depuis fiche → panier accessible |
| ADR-018 | Pas de mur de texte ; pas d'encyclopédie |

---

## Critères GO / NO GO

### GO

- [ ] Fiche HTTP 200, `marketone-product` présent **uniquement** sur fiche produit
- [ ] Ajout au panier fonctionnel
- [ ] Rendu **au moins** au niveau visuel Lot 2.1
- [ ] `/shop` et `/` sans régression
- [ ] Tests smoke + lot2 + lot2_1 + lot3 + lot4 verts
- [ ] Aucune logique catalogue ajoutée

### GO avec réserves

- [ ] Données BO incomplètes mais styles validés sur structure
- [ ] Ajustements mineurs post-recette MOA

### NO GO

- [ ] 500 sur fiche ou régression panier
- [ ] CTA panier masqué ou déplacé de façon cassante
- [ ] Styles hors scope (checkout, home, liste shop)
- [ ] Fiche encyclopédique ou surcharge éditoriale
- [ ] Dégradation visible du design system Lot 2.1
- [ ] JS, contrôleur, seed XML, ou portes introduits

---

## Commandes de validation (après exécution)

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone --stop-after-init

docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone \
  --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_smoke,dorevia_marketone_lot2,dorevia_marketone_lot2_1,dorevia_marketone_lot3,dorevia_marketone_lot4 \
  --http-port=8071
```

---

## Architecture cible (delta Lot 4)

```text
dorevia_ckreyol_marketone/
├── __manifest__.py                    # 19.0.4.0.0
├── static/src/scss/
│   └── _product.scss                  # NEW — .marketone-product { ... }
├── views/pages/
│   └── product.xml                    # NEW — inherit website_sale.product
└── tests/
    └── test_marketone_lot4_product.py # NEW
```

---

## Résultats automatises (2026-05-18)

| Commande | Résultat |
|----------|----------|
| `-u dorevia_ckreyol_marketone` | OK (v `19.0.4.0.0`) |
| Tests smoke + lot2 + lot2_1 + lot3 + lot4 | **37/37** OK |
| `marketone-product` sur fiche | Présent |
| `/shop` sans `marketone-product` | OK |
| Produit recette | Créé en setUp test si catalogue vide |

---

## Checklist validation humaine (ticket — 2026-05-18)

```text
[x] Périmètre ancre CSS marketone-product accepté
[x] Garde-fous ADR-018 / C7.4 compris (pas encyclopédique)
[x] Niveau visuel ≥ Artisanal Terroir Lot 2.1 exigé
[x] Hors périmètre (Contact, portes, panier, seed XML) compris
[x] Recette 2-3 produits BO acceptée

Décision ticket : [x] GO pour exécution
```

---

## Recette visuelle MOA (post-livraison)

**Plan** : [`docs/recette/RECETTE_MANUELLE_LOT4.md`](../recette/RECETTE_MANUELLE_LOT4.md)

```text
[x] Fiche lisible mobile + desktop (titre, prix, galerie, CTA)
[x] Ajout panier fonctionnel
[x] Cohérence Artisanal Terroir avec / et /shop
[x] Pas de surcharge éditoriale
[x] 37 tests auto verts (0 failed, 0 error)
[x] `/` marketone-root · `/shop` marketone-shop · fiche marketone-product
[x] 3 produits visibles, prix EUR FR
[x] Mobile 375 px sans débordement horizontal
[x] Fiche retail-first, non encyclopédique (ADR-018)
[x] Pas de dérive 750g / marketplace / portes catalogue

Décision livraison : [ ] GO  [x] GO avec réserves  [ ] NO GO
```

### Réserves mineures (2026-05-18)

| Réserve | Impact |
|---------|--------|
| Compteur panier à `2` sur certaines captures | CTA cliqué deux fois pendant la recette — **pas** une anomalie fonctionnelle |

---

## Prochaine étape

**Lot 5** — [`TICKET_MARKETONE_LOT5_CART_CHECKOUT.md`](TICKET_MARKETONE_LOT5_CART_CHECKOUT.md) (GO 2026-05-18).
