# TICKET — Lot 3 Boutique `/shop` `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_LOT3_SHOP` |
| **Lot** | 3 — Boutique `/shop` lisible et retail |
| **Statut** | Livré — validation auto OK (2026-05-18) |
| **Base** | `ckr-marketone-01` |
| **Prérequis** | GO Lot 2 validé (2026-05-18) |
| **Version cible module** | `19.0.3.0.0` |

---

## Objectif

Rendre la page **`/shop`** plus lisible, **mobile-first** et crédible **retail** pour C-Kreyol, **sans modifier le moteur** `website_sale`.

```text
Critère GO Lot 3 :
La page /shop reste fonctionnellement standard Odoo,
mais devient plus lisible, mobile-first et crédible retail pour C-Kreyol.
```

---

## Contexte

| Élément | État |
|---------|------|
| Lot 1 | Socle installable, tests `dorevia_marketone_smoke` |
| Lot 2 | Home `.marketone-root`, tokens SCSS, tests `dorevia_marketone_lot2` |
| `/shop` actuel | Rendu `website_sale` natif Odoo 19 CE — **sans** classe `marketone-shop` |
| Legacy | `dorevia_ckreyol_marketplace` — **anti-référence** (`ckr_shop.xml`, `_shop.scss` monolithiques) |

**Rappel doctrine** : Marketone **présente** ; Odoo **vend**. Le Lot 3 est une couche de **présentation** sur la liste boutique, pas un moteur catalogue.

---

## Doctrine (rappel)

| Règle | Lot 3 |
|-------|-------|
| Moteur | `website_sale` inchangé (domaine, tri, filtres natifs, panier, options builder) |
| Scope CSS | **`.marketone-shop`** uniquement sur la liste `/shop` |
| Scope home | `.marketone-root` inchangé (Lot 2) — pas de mélange |
| Pas de JS | Aucun fichier JS |
| Pas de portes | Pas de `marketone_mode`, chips, alias `/promotions`, etc. |
| Contrats | C4 (présentation), C5 (QWeb), C1 (moteur unique) |

---

## Périmètre inclus

### 1. Stratégie d’intégration — ancre CSS unique

Reprendre le **patron validé** KIT PRO / décision architecture (habillage, pas réécriture) :

1. Un héritage **minimal** sur `website_sale.products`.
2. Ajout de la classe `marketone-shop` sur `div#wrap` (attribut `class`, pas `replace`).
3. Tout le style dans `static/src/scss/_shop.scss` sous **`.marketone-shop`** uniquement.

**Référence technique** (autre module Dorevia, non à copier) :

```xml
<!-- pro_website_base — patron ancre CSS -->
<xpath expr="//div[@id='wrap']" position="attributes">
    <attribute name="class" add="kit-pro-shop" separator=" "/>
</xpath>
```

**Équivalent Marketone** : `add="marketone-shop"`.

| Template Odoo | Page | Lot 3 |
|---------------|------|-------|
| `website_sale.products` | `/shop` (liste) | **Oui** — `marketone-shop` |
| `website_sale.product` | `/shop/<product>` | **Non** — Lot 4 (`marketone-product`) |

### 2. QWeb

| Fichier | Rôle |
|---------|------|
| `views/pages/shop.xml` | Héritage `website_sale.products` — classe `marketone-shop` sur `#wrap` |

**Contraintes QWeb**

- `priority` ≤ 20 (contrat C5.4).
- Pas de `<style>` inline en QWeb.
- Pas de `replace` du `#wrap` ni de la grille produits.
- Pas d’insertion de bandeaux « porte » (promo, kits, explorer).
- Pas de modification des templates `website_sale.products_item` **sauf** si un micro-ajustement structurel est indispensable — par défaut **CSS seul**.

### 3. SCSS — `_shop.scss`

Nouveau fichier chargé **après** `_home.scss` dans le manifeste.

**Cibles autorisées** (sous `.marketone-shop` uniquement) :

| Zone | Intention retail |
|------|------------------|
| Fond page | Ivoire chaud cohérent charte (`$marketone-bg-soft`) |
| `#o_wsale_container` | Respiration verticale mobile-first |
| Titre boutique | Typo serif, lisible |
| Cartes `.oe_product` / `.o_wsale_products_grid` | Espacement, bordures légères, radius |
| Titre produit carte | Lisibilité, hiérarchie |
| Prix | Contraste, taille, alignement |
| Filtres / sidebar / tri | Lisibilité sans casser l’offcanvas natif |
| Pagination | Cohérence visuelle |
| CTA « Ajouter au panier » | **Visibilité** uniquement — pas de déplacement DOM |

**Interdictions SCSS**

- Pas de règles hors `.marketone-shop` (sauf tokens partagés).
- Pas de `!important` (C4.3).
- Pas de ciblage global `body`, `.o_main`.
- Pas de règles sur `/shop/cart`, checkout, portal.
- Pas de `display: none` sur actions natives (panier rapide, wishlist si un jour installé).
- Pas de refonte grille (`col-*`, `ppr`, `ppg` restent Odoo).

**Volume cible** : fichier **léger** (< 250 lignes) — pas de monolithe legacy (~3300 lignes).

### 4. Manifeste

- Version : **`19.0.3.0.0`**
- `data` : ajouter `views/pages/shop.xml`
- `assets` : ajouter `_shop.scss` après `_home.scss`

### 5. Tests

| Tag | Fichier | Rôle |
|-----|---------|------|
| `dorevia_marketone_smoke` | `test_marketone_smoke.py` | Non-régression install + `/` + `/shop` 200 |
| `dorevia_marketone_lot2` | `test_marketone_lot2_home.py` | Non-régression home — **adapter** (voir § migration tests) |
| `dorevia_marketone_lot3` | `test_marketone_lot3_shop.py` | **Nouveau** |

**Tests Lot 3 proposés** (`HttpCase`, `post_install`) :

1. `test_shop_http_200` — `/shop` → 200
2. `test_shop_has_marketone_shop_scope` — HTML contient `marketone-shop` sur `/shop`
3. `test_shop_has_wsale_grid` — présence structure native (`o_wsale_products` ou équivalent Odoo 19)
4. `test_home_has_no_marketone_shop` — `/` contient `marketone-root`, **pas** `marketone-shop`
5. `test_product_page_no_marketone_shop_yet` — `/shop` sans produit : skip ou produit démo ; si catalogue vide, vérifier qu’aucun template product n’est requis — **option** : créer 1 produit en setUpClass ou tester seulement la liste
6. `test_shop_no_catalog_gates` — pas de `marketone_mode=`, `/promotions`, `/kits`, chips portes
7. `test_shop_add_to_cart_control_present` — au moins un lien/bouton add cart ou structure `website_sale` si produits en base

**Migration tests Lot 2**

Le test Lot 2 `test_shop_no_marketone_shop_scope` valide l’**absence** de `marketone-shop` au Lot 2. Au Lot 3 :

- **Retirer** ce test de `test_marketone_lot2_home.py` (ou le marquer deprecated) ;
- **Reporter** l’assertion positive dans `test_marketone_lot3_shop.py`.

Les tests Lot 2 restants doivent rester **verts** (home, pas de portes sur `/`).

### 6. Documentation

- ADR-016 dans `cadrage/DECISIONS.md` après livraison
- `pilotage/ROADMAP.md` — statut Lot 3
- `recette/ENV_REFERENCE.md` — commandes test Lot 3
- `docs/README.md` — ligne ticket Lot 3

---

## Hors périmètre

| Exclusion | Report |
|-----------|--------|
| Fiche produit `/shop/<slug>` | Lot 4 — classe `marketone-product` |
| Panier `/shop/cart`, checkout, paiement | Lot 5 |
| Portes catalogue, filtres métier, alias URL | Lot 6 |
| `_search_get_detail`, options contrôleur | Lot 6 |
| Contrôleur Python, modèle `website.py` | Non — sauf besoin prouvé et refusé par défaut |
| JavaScript | Non |
| Sidebar « maquette » custom, chips, hero shop | Non |
| Remplacement tuile produit (Classic Store pattern) | Non |
| `website_sale_wishlist`, `theme_classic_store`, marketplace | Non |
| Header / footer globaux | Ticket dédié si MOA |

---

## Livrables attendus (checklist exécution)

```text
[ ] views/pages/shop.xml (classe marketone-shop sur #wrap)
[ ] static/src/scss/_shop.scss (scope strict)
[ ] __manifest__.py → 19.0.3.0.0 + data + asset
[ ] tests/test_marketone_lot3_shop.py + tests/__init__.py
[ ] Retrait / adaptation test_shop_no_marketone_shop_scope (Lot 2)
[ ] -u sans erreur sur ckr-marketone-01
[ ] dorevia_marketone_smoke + lot2 + lot3 : tous verts
[ ] Recette visuelle /shop mobile + desktop (PV court)
```

---

## Critères GO / NO GO

### GO

- [ ] `/shop` HTTP 200, grille produits native fonctionnelle
- [ ] Classe `marketone-shop` présente **uniquement** sur la liste boutique
- [ ] Lisibilité retail améliorée (cartes, prix, respiration mobile)
- [ ] Home Lot 2 intacte (`marketone-root`, pas de régression visuelle)
- [ ] Fiche produit **sans** `marketone-shop` (Lot 4 pas anticipé)
- [ ] Aucune logique catalogue ajoutée
- [ ] Tests smoke + lot2 (adapté) + lot3 verts
- [ ] Aucune dépendance ajoutée

### GO avec réserves

- [ ] Catalogue vide en recette : styles validés sur structure HTML même sans produit
- [ ] Ajustements mineurs post-recette visuelle MOA

### NO GO

- [ ] 500 sur `/shop` ou régression panier depuis la liste
- [ ] Styles hors scope (checkout, home, fiche produit)
- [ ] Portes, filtres métier, ou contrôleur introduit
- [ ] JS ou `!important` massif
- [ ] Dépendance optionnelle installée

---

## Risques

| Risque | Mitigation |
|--------|------------|
| XPath `#wrap` fragile | Patron `attributes` + `add` uniquement ; test HTTP |
| Spécificité vs thème Odoo | Scope `.marketone-shop` ; pas de override global |
| Catalogue vide en base test | Documenter recette avec 1–3 produits démo BO ou accepter GO avec réserve |
| Tentation portes / chips | Tests `test_shop_no_catalog_gates` |
| Confusion Lot 3 / Lot 4 | Ne pas hériter `website_sale.product` |
| Fuite styles home | Tests `test_home_has_no_marketone_shop` |

---

## Règles de non-régression

1. `dorevia_marketone_smoke` : 6/6 OK.
2. `dorevia_marketone_lot2` : tests home OK (après retrait assertion négative shop).
3. `/` : toujours `marketone-root`, textes MOA Lot 2 présents.
4. `/shop` : options builder Odoo toujours utilisables (filtres, tri, pagination).
5. Modules interdits toujours `uninstalled`.
6. Pas de modification panier / checkout.

---

## Commandes de validation

```bash
# Mise à jour
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone --stop-after-init

# Tests (port 8071 si daemon sur 8069)
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone \
  --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_smoke,dorevia_marketone_lot2,dorevia_marketone_lot3 \
  --http-port=8071

# HTTP
curl -sS -o /dev/null -w '%{http_code}\n' \
  -H 'X-Odoo-Database: ckr-marketone-01' http://localhost:18079/shop
```

**Recette visuelle** : base `ckr-marketone-01`, `/shop` en mobile (~375px) et desktop — cartes lisibles, CTA visibles, pas de scroll horizontal.

**Recette fonctionnelle minimale** (manuelle) :

- Ouvrir un produit depuis la grille → fiche standard OK
- Ajouter au panier depuis la liste ou la fiche → panier accessible
- Tri / pagination / filtres natifs si activés en BO

---

## Architecture cible (delta Lot 3)

```text
dorevia_ckreyol_marketone/
├── __manifest__.py                    # 19.0.3.0.0
├── static/src/scss/
│   └── _shop.scss                     # NEW — .marketone-shop { ... }
├── views/pages/
│   └── shop.xml                       # NEW — inherit website_sale.products
└── tests/
    └── test_marketone_lot3_shop.py    # NEW
```

Toujours **absents** : `controllers/`, `models/`, `static/src/js/`.

---

## Décision explicite — pas de moteur catalogue

```text
Le Lot 3 n’introduit aucune règle de filtrage produit,
aucun paramètre URL marketone_*, aucun hook _search_get_detail.
La sélection et le tri restent 100 % website_sale.
```

---

## Références (lecture, pas portage)

| Document / code | Usage |
|-----------------|-------|
| `pro_website_base/views/inherits/website_sale_kit_pro.xml` | Patron ancre CSS |
| `pro_website_base/static/src/scss/inherits/_shop_kit_pro.scss` | Inspiration cibles SCSS |
| `dorevia_ckreyol_marketplace/views/pages/ckr_shop.xml` | **À ne pas reproduire** |
| `cadrage/CONTRACTS.md` C5 | Héritages QWeb |
| `cadrage/DECISIONS.md` ADR-015 | Polices Lot 2 (inchangé Lot 3) |

---

### Résultats automatises (2026-05-18)

| Commande | Résultat |
|----------|----------|
| `-u dorevia_ckreyol_marketone` | OK (v `19.0.3.0.0`) |
| Tests smoke + lot2 + lot3 | **20/20** OK |
| `marketone-shop` sur `/shop` | Présent |
| Fiche produit test | Sans `marketone-shop` |
| Produit recette | Créé en setUp test si catalogue vide |

**Réserve recette visuelle** : la base peut rester sans produits en BO ; un produit est créé uniquement pendant les tests HTTP Lot 3 (pas de seed XML module).

---

## Checklist validation humaine (post-livraison)

```text
[ ] /shop plus lisible et retail (mobile-first)
[ ] Mécanique Odoo standard préservée (grille, panier, tri)
[ ] Pas de portes ni filtres métier
[ ] Home Lot 2 non dégradée
[ ] Tests automatisés OK

Décision : [ ] GO  [ ] GO avec réserves  [ ] NO GO

Réserves :
_________________________________________________

Validé par : _______________  Date : __________
```

---

## Prochaine étape après GO Lot 3

Préparer ou exécuter **Lot 4** — fiche produit (`marketone-product`, `views/pages/product.xml`, `_product.scss`).
