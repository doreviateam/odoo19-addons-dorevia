# TICKET — Lot 6.2 Exécution Porte Origines `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES_EXEC` |
| **Lot** | 6.2 — Porte Origines (implémentation) |
| **Statut** | **Ouvert** — en attente validation MOA pour exécution |
| **Version cible module** | `19.0.7.0.0` |
| **Base** | `ckr-marketone-01` |
| **Prérequis** | Lots 1–5 **GO** ; Lot 6.1 **GO avec réserves** ; cadrage **GO avec réserves** — [`TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES.md`](TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES.md) |
| **ADR** | ADR-024, ADR-025 |
| **Contrats** | C2, C3, **C3.B** ; C7 (fiche légère) |

---

## Objectif

Implémenter la porte catalogue **Origines** (univers **Boutique**) sans casser le socle ni la porte Incontournables (6.1), et **sans** implémenter le récit territoire (univers **Culture**).

```text
Critère GO Lot 6.2 :
La porte Origines oriente l’achat dans /shop (filtre + bandeau minimal)
sans moteur parallèle, sans hub Culture, sans rupture du tunnel d’achat.
```

---

## Décisions MOA figées (cadrage 2026-05-18)

| # | Décision |
|---|----------|
| D1 | `marketone_mode=origin` — libellé visible **Origines** |
| D2 | Facette `marketone_origin=<slug>` — **pas** `ckr_origin` |
| D3 | `marketone_mode=origin` **sans** facette → **catalogue complet** + bandeau Origines |
| D4 | Attribut produit **Origine** = vérité catalogue ; **profil** `marketone.shop.origin` minimal (slug, phrase visiteur, visibilité site) — **pas** page Culture |
| D5 | `/origines` → **301** → `/shop?marketone_mode=origin` |
| D6 | Origine invalide (slug / non publié) → redirection **`/shop` nu** |
| D7 | Présentation minimale : titre (Origines ou nom origine si une seule active), intro, lien retour, état vide sobre |
| D8 | Fiche produit : origine **légère**, lien possible vers `/shop?marketone_mode=origin&marketone_origin=<slug>` — **pas** bloc encyclopédique |
| D9 | Pages territoire / Culture → **lot dédié** (hors 6.2) |
| D10 | SEO canonical/noindex → **note doc** uniquement |
| D11 | **Un seul** `marketone_mode` actif — pas de cumul `featured` + `origin` |

**Réserves cadrage** : profil strictement minimal ; Culture hors scope ; pas de portage `ckr.shop.origin` ; fiche retail-first ; récit territoire préparé mais pas dans `/shop`.

---

## Périmètre inclus

### 1. Données catalogue et profil Marketone

| Livrable | Détail |
|----------|--------|
| Attribut **Origine** | `product.attribute` e-commerce, multi-valeurs, **sans** variante (`no_variant` / équivalent Odoo 19) — définition module ou BO recette documentée |
| Modèle **`marketone.shop.origin`** | Champs minimaux : `attribute_value_id`, `slug`, `name_visitor`, `context_phrase`, `sequence`, `website_published`, `website_id` ; contraintes unicité `(website_id, slug)` et `(website_id, attribute_value_id)` |
| Sécurité | CRUD `website.group_website_designer` ; lecture interne ; **pas** d’accès public ORM |
| Données recette | **Manuel BO** : valeurs d’attribut, profils origine, rattachement produits — **pas de seed XML** produits (C10) |

**Interdit** : import ou héritage de `ckr.shop.origin` ; champs image / HTML long / hub territoire sur le profil.

### 2. Contrôleur (extension `WebsiteSale` — pattern 6.1)

| Règle | Application |
|-------|-------------|
| Whitelist `marketone_mode` | Ajouter `origin` ; un seul mode actif (C3.4 si conflit : priorité pack > promo > featured > **origin** > collection) |
| Facette `marketone_origin` | Slugs répétables en query → résolution profils publiés → filtre **OU** sur `attribute_line_ids.value_ids` |
| Mode seul | `marketone_mode=origin` sans `marketone_origin` → pas de restriction domaine origine ; bandeau porte actif |
| Slug invalide | Redirect vers `/shop` sans paramètres porte |
| Alias | `GET /origines` → **301** canonique |
| Options | Injection `_get_search_options` ; **pas** de `request._marketone_*` |
| Prix | `_get_shop_domain` aligné si filtre origine actif (comme 6.1) |

### 3. Modèle `product.template`

Extension `_search_get_detail` : options `marketone_origin_only`, `marketone_origin_value_ids`, `marketone_origin_invalid` (domaine vide si invalide).

### 4. QWeb — `/shop`

Héritage `website_sale.products` sous `.marketone-shop` (symétrique `_shop_featured.xml`) :

| Élément | Condition |
|---------|-----------|
| Bandeau intro | `marketone_origin_mode` (ou équivalent) |
| Titre | **Origines** ou nom visiteur si une seule origine facettée |
| Intro courte | 1–2 phrases |
| Lien retour | `/shop` |
| État vide | Message si filtre actif et 0 produit |

Masquer le H1 shop standard quand le bandeau porte est actif (pattern 6.1).

### 5. QWeb — fiche produit (Lot 4)

Extension minimale `website_sale.product` sous `.marketone-product` :

| Élément | Règle |
|---------|-------|
| Affichage | Libellé(s) origine issus attribut / profil |
| Lien | Option vers `/shop?marketone_mode=origin&marketone_origin=<slug>` |
| Interdit | Bloc encyclopédique, mur de texte, hub Culture |

### 6. SCSS (optionnel)

`_shop_origin.scss` sous `.marketone-shop` ; styles fiche sous `.marketone-product` si nécessaire.

### 7. Tests — tag `dorevia_marketone_lot6_2_origin`

| Test | Attendu |
|------|---------|
| `test_origin_shop_200` | `/shop?marketone_mode=origin` 200 |
| `test_origin_mode_alone_full_catalog` | Sans facette : produit hors origine encore visible |
| `test_origin_facet_filters_products` | Avec `marketone_origin` : grille ⊆ produits attribut |
| `test_origin_facet_or` | Deux slugs → union (si recette BO) |
| `test_origines_301` | `/origines` → 301, Location canonique |
| `test_invalid_origin_redirect` | Slug inconnu → `/shop` nu |
| `test_unknown_mode_ignored` | `marketone_mode=unknown` → shop standard |
| `test_no_ckr_origin_param` | Pas de traitement `ckr_origin` |
| `test_featured_unchanged` | `/shop?marketone_mode=featured` non régressé |
| `test_cart_checkout_regression` | Panier + checkout OK |
| Non-régression | 60 tests existants + lot6.2 verts |

### 8. Documentation

| Fichier | Action |
|---------|--------|
| `RECETTE_MANUELLE_LOT6_2.md` | Fiche recette MOA |
| `ENV_REFERENCE.md` | Commande tests incluant `lot6_2_origin` |

---

## Fichiers attendus (proposition)

```text
dorevia_ckreyol_marketone/
├── __manifest__.py                              # 19.0.7.0.0
├── data/
│   └── marketone_product_attribute_origin.xml   # attribut « Origine » (shell, noupdate)
├── security/
│   └── ir.model.access.csv                      # marketone.shop.origin
├── models/
│   ├── marketone_shop_origin.py                 # NEW
│   └── product_template.py                      # étendu — filtre origine
├── controllers/
│   └── website_sale.py                          # étendu — origin + facet + alias
├── views/
│   ├── marketone_shop_origin_views.xml          # BO profils (minimal)
│   ├── product_template_origin_views.xml        # confort rattachement (optionnel)
│   └── pages/
│       ├── shop_origin.xml                      # bandeau /shop
│       └── product_origin.xml                   # bloc léger fiche
├── static/src/scss/
│   ├── _shop_origin.scss
│   └── _product_origin.scss                     # optionnel
└── tests/
    └── test_marketone_lot6_2_origin.py          # NEW
```

---

## Hors périmètre

| Exclusion | Report |
|-----------|--------|
| Pages Culture / hub territoire | Lot Culture |
| Savoirs / recettes | Lot Savoirs |
| Autres portes (`promo`, `pack`, `collection`) | Lots 6.x |
| Sidebar portes dédiée / Explorer / chips | Hors 6.2 |
| SEO implémentation | Note doc |
| `dorevia_ckreyol_marketplace` | Interdit |
| JS | Interdit |
| Seed XML produits / profils complets | BO recette |

---

## Critères GO / NO GO exécution

### GO

- [ ] `/shop?marketone_mode=origin` 200, bandeau visible
- [ ] Facette `marketone_origin` filtre correctement (OU)
- [ ] Mode seul = catalogue complet + bandeau
- [ ] `/origines` 301 ; slug invalide → `/shop` nu
- [ ] Fiche : origine légère + lien optionnel
- [ ] Lot 6.1 (featured) non régressé
- [ ] Panier / checkout / home OK
- [ ] 60 + tests lot6.2 verts
- [ ] Pas de `ckr_*` ni dépendance marketplace

### NO GO

- [ ] 500 sur `/shop` ou profil mal configuré sans repli
- [ ] Hub Culture ou contenu long sur `/shop`
- [ ] Moteur parallèle ou `request._marketone_*`
- [ ] Régression featured / tunnel

---

## Checklist validation MOA (exécution)

```text
[x] Cadrage Lot 6.2 validé (ADR-025, C3.B)
[x] ADR-024 / séparation Boutique–Culture comprise
[x] Profil marketone.shop.origin minimal accepté
[x] Tag tests dorevia_marketone_lot6_2_origin accepté

Décision exécution : [ ] GO pour implémentation  [ ] En attente  [ ] NO GO
```

---

## Prochaine étape

1. **MOA** : valider ce ticket d’exécution.
2. **Dev** : implémentation `19.0.7.0.0` + recette MOA.
3. **Culture** : ticket séparé — pas dans le même lot.
