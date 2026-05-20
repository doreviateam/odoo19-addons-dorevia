# TICKET — Lot 5 Panier / checkout smoke `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_LOT5_CART_CHECKOUT` |
| **Lot** | 5 — Panier / checkout smoke (tunnel standard Odoo) |
| **Statut** | **GO** (recette MOA 2026-05-18) |
| **Version livrée** | `19.0.5.0.0` |
| **Version cible module** | `19.0.5.0.0` (proposition) |
| **Base** | `ckr-marketone-01` |
| **Prérequis** | **GO Lot 4 avec réserves mineures** (`19.0.4.0.0`, 2026-05-18) ; Lots 1, 2, 2.1, 3 livrés |
| **Référence design** | Artisanal Terroir (Lot 2.1) — cohérence visuelle **minimale**, pas de refonte tunnel |
| **Contrats** | C8 (panier / checkout), C1 (moteur unique), C4 / C5 (présentation) |

---

## Objectif

Sécuriser le **parcours invité standard** `website_sale` : ajout au panier → consultation panier → modification → accès première étape checkout, **sans 500** et avec une **cohérence visuelle minimale** Artisanal Terroir.

```text
Critère GO Lot 5 :
Un visiteur invité peut ajouter un produit au panier, consulter le panier,
modifier son panier et accéder au checkout standard Odoo sans erreur,
avec une cohérence visuelle minimale et sans altérer website_sale.
```

**Ce lot n’est pas une refonte du tunnel d’achat.**

---

## Contexte

| Élément | État |
|---------|------|
| Lot 4 | GO avec réserves — fiche `marketone-product`, ajout panier validé en recette MOA |
| Panier / checkout actuels | Templates et routes **`website_sale` natifs** — sans ancre Marketone dédiée |
| Recette Lot 4 | Panier accessible, quantité modifiable — **smoke fonctionnel**, pas couverture tunnel complète |
| Doctrine | Marketone **présente** ; Odoo **vend** (panier, checkout, paiement) |

**Rappel** : le compteur panier > 1 après double clic CTA en recette Lot 4 est documenté comme **non-bug**.

---

## Doctrine (garde-fous)

| Règle | Lot 5 |
|-------|-------|
| Moteur | `website_sale` **inchangé** — logique panier, lignes, quantités, checkout |
| Pas de refonte | Pas de réorganisation des étapes, formulaires, ni workflow checkout |
| Pas de checkout custom | Pas de routes, contrôleurs ou templates parallèles |
| Scope CSS | **`.marketone-cart`** et **`.marketone-checkout`** uniquement sur leurs pages respectives |
| Scopes existants | `.marketone-root`, `.marketone-shop`, `.marketone-product` **inchangés** |
| Design system | Tokens Lots 2.1 — micro-ajustements lisibilité (typo, espacements, CTA) |
| Pas de JS | Aucun fichier JS |
| Pas de Python métier | Pas de `models/`, pas de surcharge `website.py` |
| Pas de portes | Pas de `marketone_mode`, filtres catalogue, alias |
| ADR-018 / ADR-019 | Pas de contenu éditorial, 750g, Caribshopper au tunnel |

---

## Périmètre inclus

### 1. Parcours fonctionnel à couvrir (invité)

| Étape | Route / action Odoo standard | Attendu |
|-------|------------------------------|---------|
| Ajout | Fiche produit → CTA « Ajouter au panier » | Ligne créée, pas de 500 |
| Accès panier | `/shop/cart` (ou lien header panier) | HTTP 200 |
| Consultation | Page panier | Lignes, prix, totaux visibles |
| Quantité | Contrôle quantité natif | Modification possible |
| Suppression | Action supprimer ligne native | Ligne retirée |
| Retour boutique | Lien « Continuer mes achats » / équivalent | Retour `/shop` 200 |
| Checkout | Première étape checkout standard | HTTP 200, formulaire / étape Odoo visible |

*Routes exactes : s’aligner sur les templates `website_sale` de l’instance (Odoo 19 CE). En recette, noter l’URL réelle si différente de `/shop/checkout`.*

### 2. Stratégie d’intégration — ancres CSS (patron Lots 3–4)

| Template Odoo (référence) | Page | Lot 5 |
|---------------------------|------|-------|
| `website_sale.cart` | `/shop/cart` | **Oui** — `marketone-cart` sur `#wrap` |
| Template checkout `website_sale` (ex. `website_sale.checkout` ou équivalent CE) | Première étape checkout | **Oui** — `marketone-checkout` sur `#wrap` |
| `website_sale.products` | `/shop` | **Non** — `marketone-shop` (Lot 3) |
| `website_sale.product` | Fiche produit | **Non** — `marketone-product` (Lot 4) |

**Contraintes QWeb**

- Héritage minimal, `priority` ≤ 20 (C5.4).
- `add` sur `class` du `#wrap`, pas de `replace`.
- Pas de `<style>` inline.
- Pas de modification des formulaires panier / checkout (champs, étapes, boutons métier).

### 3. Fichiers attendus (proposition)

```text
dorevia_ckreyol_marketone/
├── __manifest__.py                         # 19.0.5.0.0
├── views/pages/
│   ├── cart.xml                            # NEW — inherit website_sale.cart
│   └── checkout.xml                        # NEW — inherit template checkout CE
├── static/src/scss/
│   ├── _cart.scss                          # NEW — .marketone-cart { ... }
│   └── _checkout.scss                      # NEW — .marketone-checkout { ... }
└── tests/
    └── test_marketone_lot5_cart_checkout.py  # NEW — tag dorevia_marketone_lot5
```

**Ordre assets** : `_product.scss` → `_cart.scss` → `_checkout.scss` → `marketone.scss`.

### 4. SCSS — cibles autorisées

Sous **`.marketone-cart`** uniquement :

| Zone | Intention |
|------|-----------|
| Fond page | Cohérence `$marketone-bg` / `$marketone-bg-soft` |
| Tableau / lignes panier | Lisibilité, espacement mobile |
| Prix / totaux | Contraste, typo Hanken Grotesk |
| CTA « Commander » / checkout | `@include marketone-btn-primary` scoped |
| Liens retour boutique | Lisibilité |

Sous **`.marketone-checkout`** uniquement :

| Zone | Intention |
|------|-----------|
| Fond / titres étape | Cohérence charte |
| Formulaires | Lisibilité labels — **sans** masquer champs requis |
| Boutons navigation étape | Style primaire / secondaire cohérent |

**Interdictions SCSS**

- Pas de règles hors `.marketone-cart` / `.marketone-checkout` (sauf tokens partagés).
- Pas de `!important` (C4.3).
- Pas de `display: none` sur CTA checkout, quantité, suppression, paiement.
- Pas de styles sur home, `/shop` liste, fiche produit, BO, portal.

### 5. Tests automatisés — tag `dorevia_marketone_lot5`

Fichier : `tests/test_marketone_lot5_cart_checkout.py`

| Test (indicatif) | Intention |
|------------------|-----------|
| `test_cart_http_200` | `/shop/cart` répond 200 |
| `test_cart_has_marketone_cart_scope` | Présence `marketone-cart` |
| `test_checkout_http_200` | Première étape checkout 200 (panier non vide en setUp) |
| `test_checkout_has_marketone_checkout_scope` | Présence `marketone-checkout` |
| `test_add_to_cart_via_product` | POST / RPC ajout depuis fiche ou route standard — panier non vide |
| `test_cart_has_line_controls` | Structure quantité / suppression native |
| `test_cart_no_other_scopes` | Pas de `marketone-shop` / `marketone-product` sur panier |
| `test_checkout_no_catalog_gates` | Pas de portes / `marketone_mode` |
| Non-régression | `/`, `/shop`, fiche produit : scopes Lots 2–4 inchangés |

**Non-régression obligatoire** (commande complète) :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone \
  --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_smoke,dorevia_marketone_lot2,dorevia_marketone_lot2_1,dorevia_marketone_lot3,dorevia_marketone_lot4,dorevia_marketone_lot5 \
  --http-port=8071
```

**Tag étendu (hors GO bloquant)** : `dorevia_marketone_payment_demo` — E2E `payment_demo` si MOA l’exige plus tard (contrat C8.3).

---

## Hors périmètre

| Exclusion | Report |
|-----------|--------|
| Paiement réel (Stripe, etc.) | Hors sandbox |
| Refonte checkout | Interdit |
| Checkout custom (routes, templates parallèles) | Interdit |
| Modification moteur panier Odoo | Interdit |
| Paiement / transporteurs / `delivery` | Interdit |
| JavaScript custom | Interdit |
| Contrôleur Python | Interdit |
| Modèle `models/` | Interdit |
| Portes catalogue | Lot 6 |
| 750g / Caribshopper / éditorial | Lots ultérieurs |
| Seed XML produits | Non — recette BO existante (3 produits) |
| Page Contact `/contactus` | Ticket futur |
| Header / footer globaux | Lot 2.1 — non-régression uniquement |

---

## Recette manuelle MOA (à exécuter post-livraison)

**Prérequis** : session invité (navigation privée), panier vidé au départ, 1 produit de référence (ex. Crackers Sainte-Anne).

| # | Test | Attendu |
|---|------|---------|
| L5-01 | Ajout depuis fiche | Produit dans le panier |
| L5-02 | `/shop/cart` | 200, lignes visibles, prix € |
| L5-03 | Modifier quantité | Mise à jour sans 500 |
| L5-04 | Supprimer ligne | Panier vide ou message adapté |
| L5-05 | Ré-ajout + retour `/shop` | 200, `marketone-shop` intact |
| L5-06 | Accès checkout | 200, première étape standard visible |
| L5-07 | Scope panier | `marketone-cart` sur panier uniquement |
| L5-08 | Scope checkout | `marketone-checkout` sur checkout uniquement |
| L5-09 | Non-régression | `/`, `/shop`, fiche : scopes et rendu Lots 2–4 OK |
| L5-10 | Mobile 375 px | Panier + checkout sans scroll horizontal |

**Plan** : [`docs/recette/RECETTE_MANUELLE_LOT5.md`](../../recette/lots/RECETTE_MANUELLE_LOT5.md)

---

## Critères GO / NO GO

### GO

- [x] Parcours invité : ajout → panier → modif quantité → suppression → retour shop → checkout **sans 500**
- [x] `marketone-cart` **uniquement** sur panier ; `marketone-checkout` **uniquement** sur checkout (`/shop/address`)
- [x] Cohérence visuelle **minimale** ≥ niveau lisibilité Lots 2.1 / 4 (pas de rupture majeure)
- [x] `/`, `/shop`, fiche produit sans régression scope ni visuelle majeure
- [x] Tests smoke + lot2 + lot2_1 + lot3 + lot4 + **lot5** verts (49/49)
- [x] Aucune logique panier/checkout/paiement ajoutée

### GO avec réserves

- [ ] Micro-ajustements visuels mineurs post-recette MOA
- [ ] Étape checkout : libellés Odoo natifs acceptés en sandbox

### NO GO

- [ ] 500 sur panier ou checkout invité
- [ ] CTA checkout / quantité / suppression masqués ou cassés
- [ ] Refonte layout checkout ou panier
- [ ] Styles hors scope (home, shop, fiche) ou fuite vers BO
- [ ] JS, contrôleur, modèle, seed XML, portes introduits
- [ ] Régression Lots 2–4

---

## Checklist validation humaine (ticket — ouverture)

```text
[x] Périmètre smoke tunnel standard compris (pas refonte)
[x] Hors périmètre paiement / moteur / JS / portes compris
[x] Ancres CSS marketone-cart / marketone-checkout acceptées
[x] Tag tests dorevia_marketone_lot5 accepté
[x] Critère GO Lot 5 aligné MOA

Décision ticket : [x] GO pour exécution  [ ] En attente  [ ] NO GO
```

---

## Architecture livrée (delta Lot 5)

```text
Présentation uniquement :
  cart.xml       → scope marketone-cart / marketone-checkout via checkout_layout (path HTTP)
  checkout.xml   → rattachement Lot 5 (scope centralise dans cart.xml)
  _cart.scss     → styles scoped panier
  _checkout.scss → styles scoped checkout (micro)
  tests lot5     → 12 tests HTTP + parcours invité smoke
```

### Note technique Odoo 19

- Panier : `/shop/cart` → `marketone-cart`
- Checkout invité : `/shop/checkout` → **303** → `/shop/address` → `marketone-checkout`
- Scope appliqué sur `body` + `#wrap` via `website_sale.checkout_layout`

## Résultats automatisés (2026-05-18)

| Commande | Résultat |
|----------|----------|
| `-u dorevia_ckreyol_marketone` | OK (v `19.0.5.0.0`) |
| Tests smoke + lot2 + lot2_1 + lot3 + lot4 + lot5 | **49/49** OK |

---

## Recette visuelle MOA (post-livraison)

**Plan** : [`docs/recette/RECETTE_MANUELLE_LOT5.md`](../../recette/lots/RECETTE_MANUELLE_LOT5.md)

```text
[x] Ajout panier depuis fiche OK
[x] /shop/cart 200, marketone-cart, lignes / quantité / suppression
[x] Modification quantité et suppression OK ; panier vide correct
[x] Retour /shop, marketone-shop intact
[x] Checkout invité : /shop/checkout → /shop/address 200, marketone-checkout
[x] Pas de marketone-cart au checkout
[x] Non-régression / (marketone-root) et fiche (marketone-product)
[x] Mobile 375 px sans débordement horizontal
[x] 49 tests auto verts

Décision livraison : [x] GO  [ ] GO avec réserves  [ ] NO GO
```

### Réserve non bloquante (2026-05-18)

| Réserve | Impact |
|---------|--------|
| Compteur panier à `3` sur certaines captures | Test modification quantité en recette — **pas** une anomalie fonctionnelle |

---

## Références

| Document | Lien |
|----------|------|
| ROADMAP | `docs/pilotage/ROADMAP.md` § Lot 5 |
| Contrats C8 | `docs/cadrage/CONTRACTS.md` |
| ADR-022 | `docs/cadrage/DECISIONS.md` |
| Recette env | `docs/recette/reference/ENV_REFERENCE.md` |
| Lot 4 clôturé | `docs/tickets/TICKET_MARKETONE_LOT4_PRODUCT.md` |

---

## Prochaine étape

**Lot 6** — portes catalogue (ticket à préparer, une porte à la fois, sans casser le socle Lots 1–5).
