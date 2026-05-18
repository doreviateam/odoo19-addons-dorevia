# Environnement de référence — `ckr-marketone-01`

| Champ | Valeur |
|-------|--------|
| **Base PostgreSQL** | `ckr-marketone-01` |
| **Rôle** | Environnement propre pour `dorevia_ckreyol_marketone` (Lot 1+) |
| **Instance** | Docker `sandbox-odoo19` |
| **Odoo** | `19.0-20260324` |
| **URL** | http://localhost:18079 |
| **Statut** | Créée et initialisée le 2026-05-18 |

---

## Règles d’usage

| Règle | Application |
|-------|-------------|
| Ne pas installer `dorevia_ckreyol_marketplace` | ✅ `uninstalled` |
| Pas de thème tiers au départ | ✅ `theme_classic_store` = `uninstalled` |
| Pas de dépendance optionnelle Marketone sans validation | ✅ wishlist / comparaison retirés après init |
| Socle e-commerce cible | `website`, `website_sale`, `portal` installés |
| Base de référence Lot 1 | install / update / smoke test |

**Ne pas utiliser** `tenant_o5`, `ckr_collections_recette` ni une autre base marketplace pour valider Marketone.

---

## Infrastructure

```text
Conteneur Odoo : sandbox-odoo19-odoo-1
Conteneur DB   : sandbox-odoo19-db-1
Config         : /Users/doreviateam/sandbox-odoo19/odoo.conf
Addons Dorevia : /Users/doreviateam/dorevia-saas/odoo19-addons-dorevia → /mnt/odoo19-addons-dorevia
```

Sélection de la base dans le navigateur : choisir **`ckr-marketone-01`** sur l’écran de login, ou en-tête HTTP :

```http
X-Odoo-Database: ckr-marketone-01
```

Identifiants init : **admin** / **admin** (mot de passe maître config : `admin` dans `odoo.conf`).

---

## Modules — état attendu

### Installés (socle + chaîne Odoo standard)

| Module | Rôle |
|--------|------|
| `website` | Site web |
| `website_sale` | Boutique en ligne |
| `portal` | Espace client |

La chaîne transitive Odoo 19 (vente, paiement, mail, etc.) est installée (~67 modules) : c’est le comportement normal d’un `-i website_sale`.

### Interdits / absents

| Module | État |
|--------|------|
| `dorevia_ckreyol_marketplace` | `uninstalled` |
| `theme_classic_store` | `uninstalled` |
| `dorevia_ckreyol_marketone` | installé après `-i` Lot 1 |

### Retirés après init (auto-install Odoo 19)

L’installation initiale d’`website_sale` sur Odoo 19 CE a tiré **`website_sale_wishlist`** et **`website_sale_comparison`** (auto-install bundle). Ils ont été **désinstallés** pour respecter le périmètre minimal :

| Module | État |
|--------|------|
| `website_sale_wishlist` | `uninstalled` |
| `website_sale_comparison` | `uninstalled` |
| `website_sale_comparison_wishlist` | `uninstalled` |

> Réactiver wishlist ou comparaison uniquement après validation MOA (ticket dédié).

---

## Procédure de création (reproductible)

### 1. Créer la base PostgreSQL

```bash
docker exec sandbox-odoo19-db-1 psql -U odoo -d postgres \
  -c 'CREATE DATABASE "ckr-marketone-01" OWNER odoo;'
```

### 2. Initialiser Odoo (sans démo)

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 \
  -i base,website,website_sale,portal \
  --without-demo=true \
  --stop-after-init
```

### 3. Retirer wishlist / comparaison (optionnel mais recommandé)

```bash
docker exec -i sandbox-odoo19-odoo-1 odoo shell -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 --no-http <<'PY'
for name in (
    'website_sale_comparison_wishlist',
    'website_sale_wishlist',
    'website_sale_comparison',
):
    mod = env['ir.module.module'].search([
        ('name', '=', name), ('state', '=', 'installed')
    ])
    if mod:
        mod.button_immediate_uninstall()
env.cr.commit()
PY
```

### 4. Vérifier l’état

```bash
docker exec sandbox-odoo19-db-1 psql -U odoo -d ckr-marketone-01 -c \
  "SELECT name, state FROM ir_module_module
   WHERE name IN (
     'dorevia_ckreyol_marketplace','theme_classic_store',
     'website','website_sale','portal',
     'website_sale_wishlist','website_sale_comparison'
   ) ORDER BY name;"
```

### 5. Smoke HTTP

```bash
curl -sS -o /dev/null -w '%{http_code}\n' \
  -H 'X-Odoo-Database: ckr-marketone-01' \
  http://localhost:18079/shop
# Attendu : 200
```

---

## Commandes Lot 1 (à venir)

Une fois le socle `dorevia_ckreyol_marketone` livré :

```bash
# Installation
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 \
  -i dorevia_ckreyol_marketone \
  --stop-after-init

# Mise à jour
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 \
  -u dorevia_ckreyol_marketone \
  --stop-after-init

# Tests smoke + lots 2 / 2.1 / 3 (port alternatif si le daemon tourne déjà sur 8069)
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 \
  -u dorevia_ckreyol_marketone \
  --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_smoke,dorevia_marketone_lot2,dorevia_marketone_lot2_1,dorevia_marketone_lot3,dorevia_marketone_lot4,dorevia_marketone_lot5,dorevia_marketone_lot6_1_featured,dorevia_marketone_lot6_2_origin,dorevia_marketone_culture_v1 \
  --http-port=8071
```

**Culture v1 — page territoire** (`19.0.8.0.0`, **GO MOA** 2026-05-18) :

| Prérequis | Détail |
|-----------|--------|
| Profil BO | `marketone.shop.origin` publié, slug pilote ex. `guadeloupe` |
| URL Culture | `GET /culture/<slug>` — ex. `/culture/guadeloupe` — **pas** de hub `/culture` |
| CTA achetable | `/shop?marketone_mode=origin&marketone_origin=<slug>` |
| Recette | [`RECETTE_MANUELLE_CULTURE_V1.md`](RECETTE_MANUELLE_CULTURE_V1.md) |

**Lot 6.2 — porte Origines** (`19.0.7.0.0`, **GO MOA** 2026-05-18) :

| Prérequis | Détail |
|-----------|--------|
| Attribut catalogue | **Origine** — multi-valeurs, sans variante |
| Profils BO | `marketone.shop.origin` : slug, nom visiteur, phrase, publié, `website_id` = site courant |
| URL | `/shop?marketone_mode=origin` ; facette `marketone_origin=<slug>` ; alias `/origines` → 301 |
| Recette | [`RECETTE_MANUELLE_LOT6_2.md`](RECETTE_MANUELLE_LOT6_2.md) |

**Consolidation portes Boutique** (**GO** 2026-05-18) — référence [`TICKET_MARKETONE_CONSOLIDATION_PORTES_BOUTIQUE.md`](../tickets/TICKET_MARKETONE_CONSOLIDATION_PORTES_BOUTIQUE.md) :

| Entrée | Canonique |
|--------|-----------|
| Tous les produits | `/shop` |
| Incontournables | `/shop?marketone_mode=featured` — alias `/incontournables` → 301 |
| Origines | `/shop?marketone_mode=origin` — alias `/origines` → 301 ; facette `marketone_origin=<slug>` |

**Lot 6.1 — porte Incontournables** (`19.0.6.0.0`, **GO avec réserves** 2026-05-18) :

| Prérequis | Détail |
|-----------|--------|
| Paramètre système | `dorevia_ckreyol_marketone.featured_public_category_id` = id `product.public.category` « Incontournables » |
| Catégorie BO | **Prérequis d’exploitation (obligatoire)** : la catégorie publique **Incontournables** doit avoir `website_id` = site courant (**My Website** sur `ckr-marketone-01`, idem recette / pré-prod). Sans rattachement site → **500** sur `/shop?marketone_mode=featured` — consolidé GO portes Boutique, pas une simple réserve historique |
| Produits | 2–3 produits publiés rattachés à la catégorie (manuel, pas de seed XML) |
| Recette | [`RECETTE_MANUELLE_LOT6_1.md`](RECETTE_MANUELLE_LOT6_1.md) |

**Exploitation sandbox** : après `-u dorevia_ckreyol_marketone`, un daemon Odoo déjà lancé (ex. port `18079`) peut nécessiter un **redémarrage du conteneur / service** pour que les routes alias `GET /incontournables`, `GET /origines` et `GET /culture/<slug>` soient prises en compte (rechargement routing). Les runs `--stop-after-init` n’ont pas ce problème.

```bash
docker compose -f /Users/doreviateam/sandbox-odoo19/docker-compose.yml restart odoo
```

---

## Recette visuelle — produits BO (sans seed XML)

Pour valider `/shop` (cartes) et la future fiche produit Lot 4, créer **2 à 3 produits publiés** manuellement en BO (Website → eCommerce → Products) :

- nom, prix, image, description courte ;
- catégorie e-commerce si besoin ;
- **aucun** fichier seed XML dans le module Marketone.

**Images de recette** : utiliser les packshots réels de la banque legacy — voir [`ASSETS_REFERENCE.md`](ASSETS_REFERENCE.md) (`dorevia_ckreyol_marketplace/docs/assets/`, fichiers `homepage_*` ou `exemple_produit_*`).

Réserve acceptée au **GO Lot 2.1 avec réserves** (2026-05-18).

---

## Recréer la base from scratch

```bash
docker exec sandbox-odoo19-db-1 psql -U odoo -d postgres \
  -c 'DROP DATABASE IF EXISTS "ckr-marketone-01" WITH (FORCE);'
# Puis reprendre la procédure de création § ci-dessus
```

---

## Recette manuelle MOA

Plan de recette pas à pas (home, shop, fiche produit Lot 4, panier, grilles GO/NO GO) :

→ [`RECETTE_MANUELLE.md`](RECETTE_MANUELLE.md)

---

## Références

- `cadrage/DECISIONS.md` — ADR-013
- `cadrage/CONTRACTS.md` — C11 (non cohabitation marketplace)
- Sandbox : `/Users/doreviateam/sandbox-odoo19/`
