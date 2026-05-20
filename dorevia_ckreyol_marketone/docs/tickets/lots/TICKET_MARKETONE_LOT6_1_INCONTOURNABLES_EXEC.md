# TICKET — Lot 6.1 Exécution Porte Incontournables `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_LOT6_1_INCONTOURNABLES_EXEC` |
| **Lot** | 6.1 — Porte Incontournables (implémentation) |
| **Statut** | **Clôturé — GO avec réserves** (2026-05-18) |
| **Version cible module** | `19.0.6.0.0` |
| **Base** | `ckr-marketone-01` |
| **Prérequis** | Lots 1–5 **GO** ; cadrage **GO avec réserves** — [`TICKET_MARKETONE_LOT6_1_PORTE_INCONTOURNABLES.md`](./TICKET_MARKETONE_LOT6_1_PORTE_INCONTOURNABLES.md) |
| **ADR** | ADR-023 |
| **Contrats** | C2, C3.A |

---

## Objectif

Implémenter la **première porte catalogue** Marketone — **Incontournables** — sans casser le socle e-commerce stabilisé.

```text
Critère GO Lot 6.1 :
Une première porte catalogue éditoriale peut orienter vers une sélection de produits
sans casser /shop, ni le moteur website_sale, ni le tunnel d’achat.
```

---

## Décisions MOA figées (cadrage 2026-05-18)

| # | Décision |
|---|----------|
| D1 | `marketone_mode=featured` — libellé **Incontournables** |
| D2 | `ir.config_parameter` → `product.public.category` |
| D3 | Catégorie **Incontournables** ; multi-catégories OK ; filtres natifs **conservés** |
| D4 | Pas de tag ni champ produit custom |
| D5 | Pas de `marketone.shop.collection` |
| D6 | `/incontournables` → **301** → `/shop?marketone_mode=featured` |
| D7 | Canonique `/shop?marketone_mode=featured` ; params inconnus ignorés |
| D8 | 301 OK ; SEO canonical/noindex : **note doc** uniquement |
| D9 | Présentation **minimale** (titre, intro, lien retour) |

**Paramètre système proposé** : `dorevia_ckreyol_marketone.featured_public_category_id` (id `product.public.category`).

---

## Périmètre inclus

### 1. Backend / configuration

| Livrable | Détail |
|----------|--------|
| Paramètre système | Clé + aide BO : id catégorie « Incontournables » |
| Résolution catégorie | Si id invalide / catégorie vide → comportement vide documenté (200 + message, pas 500) |
| Données recette | **Manuel BO** : créer catégorie « Incontournables », rattacher 2–3 produits recette — **pas de seed XML** (C10) |

### 2. Contrôleur (héritage `WebsiteSale`)

| Règle | Application |
|-------|-------------|
| Lecture `marketone_mode` | Whitelist : seule valeur `featured` au Lot 6.1 |
| Params inconnus | Ignorés — `/shop` standard |
| Filtre produits | Options injectées vers `_search_get_detail` — **pas** de domaine QWeb |
| État | **Pas** de `request._marketone_*` |
| Route alias | `GET /incontournables` → redirect 301 vers canonique |

### 3. QWeb (présentation minimale)

Héritage `website_sale.products` sous scope existant `.marketone-shop` :

| Élément | Contenu |
|---------|---------|
| Titre | **Incontournables** (H1 ou équivalent zone titre shop) |
| Intro | 1–2 phrases courtes (éditorial C-Kreyol, non encyclopédique) |
| Lien retour | « Tous les produits » → `/shop` (sans `marketone_mode`) |
| Condition | Affiché **uniquement** si `marketone_mode=featured` |

**Interdit** : hero, chips promo/kits/origines, bandeau Explorer, refonte grille.

### 4. SCSS (optionnel minimal)

Sous `.marketone-shop` uniquement — bloc intro porte (typo Artisanal Terroir). Pas de nouveau scope racine.

### 5. Tests — tag `dorevia_marketone_lot6_1_featured`

| Test | Attendu |
|------|---------|
| `test_featured_shop_200` | `/shop?marketone_mode=featured` 200 |
| `test_featured_filters_products` | Grille ⊆ produits catégorie BO |
| `test_incontournables_301` | `/incontournables` → 301, Location canonique |
| `test_unknown_param_ignored` | `/shop?marketone_mode=unknown` → shop standard |
| `test_shop_without_mode_unchanged` | `/shop` sans régression `marketone-shop` |
| `test_featured_no_gates_on_home` | `/` sans `marketone_mode` |
| `test_cart_checkout_regression` | Panier + checkout scopes Lot 5 OK |
| Non-régression | 49 tests Lots 1–5 + lot6.1 verts |

### 6. Documentation

| Fichier | Action |
|---------|--------|
| `RECETTE_MANUELLE_LOT6_1.md` | Fiche recette MOA |
| `ENV_REFERENCE.md` | Commande tests incluant lot6.1 |
| Note SEO courte | Dans ticket ou `DECISIONS.md` — canonical/noindex **à trancher MOA plus tard** |

---

## Fichiers attendus (proposition)

```text
dorevia_ckreyol_marketone/
├── __manifest__.py                              # 19.0.6.0.0
├── data/
│   └── marketone_config_parameter.xml           # définition param (sans valeur prod)
├── controllers/
│   └── website_sale.py                          # NEW ou étendu — mode featured + alias 301
├── models/
│   └── product_template.py                      # NEW — _search_get_detail hook (si pas déjà présent)
├── views/pages/
│   └── shop_featured.xml                        # NEW — titre / intro / lien retour
├── static/src/scss/
│   └── _shop_featured.scss                      # NEW optionnel — sous .marketone-shop
└── tests/
    └── test_marketone_lot6_1_featured.py        # NEW
```

*Structure exacte ajustable si un fichier `website_sale.py` existe déjà au socle.*

---

## Hors périmètre

| Exclusion | Report |
|-----------|--------|
| Autres portes (`promo`, `pack`, `origin`, `collection`) | Lots 6.2+ |
| `product_pack`, promotions, pricelist | Lot 6.x |
| `dorevia_ckreyol_marketplace` | Interdit C11 |
| JS | Interdit |
| Modèle `marketone.shop.collection` | Post 6.1 |
| Masquer filtres sidebar Odoo | Hors 6.1 (réserve cadrage) |
| SEO implémentation canonical/noindex | Documenter seulement |
| Seed XML produits / catégorie | Non — BO recette |

---

## Critères GO / NO GO

### GO

- [x] `/shop?marketone_mode=featured` 200, produits filtrés selon catégorie BO
- [x] `/incontournables` 301 vers canonique
- [x] Présentation minimale visible (titre, intro, retour)
- [x] Filtres natifs `/shop` toujours utilisables
- [x] Fiche, panier, checkout, home : non-régression
- [x] 60 tests (Lots 1–5 + lot6.1) verts
- [x] Pas de moteur parallèle

### NO GO

- [ ] 500 sur `/shop` ou alias
- [ ] Grille non filtrée ou filtre cassant `website_sale`
- [ ] Régression panier / checkout
- [ ] Chips multi-portes ou refonte shop
- [ ] Dépendance marketplace

---

## Checklist validation MOA (exécution)

```text
[x] Cadrage Lot 6.1 validé (ADR-023)
[x] Périmètre une seule porte compris
[x] Source catégorie publique acceptée
[x] Tag tests dorevia_marketone_lot6_1_featured accepté

Décision exécution : [x] GO pour implémentation  [ ] En attente  [ ] NO GO
```

---

## Verdict MOA (2026-05-18)

**GO Lot 6.1 avec réserves**

| Réserve | Documentation |
|---------|----------------|
| Catégorie `Incontournables` : `website_id` = site courant obligatoire | `RECETTE_MANUELLE_LOT6_1.md`, `ENV_REFERENCE.md`, ADR-023 |
| Redémarrage daemon après `-u` pour route `/incontournables` | `RECETTE_MANUELLE_LOT6_1.md`, `ENV_REFERENCE.md`, ADR-023 |

---

## Prochaine étape

1. **Cadrage séparé** Lot 6.2 (une seule porte) — pas de multi-portes simultanées
2. Commit `19.0.6.0.0` sur `main` ✅
