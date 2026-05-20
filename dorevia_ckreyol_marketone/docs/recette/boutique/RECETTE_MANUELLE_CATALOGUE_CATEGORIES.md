# Recette manuelle — Catégories e-commerce catalogue recette

| Champ | Valeur |
|-------|--------|
| **Ticket** | [`TICKET_MARKETONE_CATALOGUE_CATEGORIES_BO_RECETTE`](../../tickets/boutique/TICKET_MARKETONE_CATALOGUE_CATEGORIES_BO_RECETTE.md) |
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079 |
| **Univers** | Boutique — taxonomie catalogue (pas Culture, pas Savoirs) |
| **ADR / Contrat** | ADR-029 · C3.C |
| **Mapping** | [`MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md`](../../cadrage/MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md) |
| **Statut recette** | **GO MOA** (2026-05-19) — BO + contrôles techniques validés |

---

## Prérequis

| Élément | Détail |
|---------|--------|
| Ticket BO | Phase 1–3 exécutées — **clôturé** |
| Produits | **27** vendables publiés — pas de « Recette … » |
| Catégories | **17** sur site courant (13 principales + 4 secondaires) |
| `website_id` | Toutes les catégories e-commerce sur **My Website** |
| Hors scope | Origines, Savoirs v1, code Marketone |

---

## Grille de recette

| # | Scénario | Action / URL | Attendu | MOA | Tech |
|---|----------|--------------|---------|-----|------|
| **1** | Inventaire catégories BO | *Site web* → catégories eCommerce | **17** catégories (13 principales + 4 secondaires) | ☑ | ☑ |
| **2** | `website_id` catégories | Vérifier échantillon + **Incontournables** | Site courant sur toutes | ☑ | ☑ |
| **3** | Crackers — rattachements | Fiche *Crackers manioc Sainte-Anne* | Principale **Biscuits salés** ; secondaires **Incontournables**, **Apéritif créole**, **Cuisine du manioc** (4 max) | ☑ | ☑ |
| **4** | Miel — principale | Fiche *Miel créole baie rose* | Principale **Miels** ; secondaires selon mapping | ☑ | ☑ |
| **5** | Échantillon 5 produits | Contrôle croisé mapping (1 par famille principale) | Conforme au tableau mapping | ☑ | ☑ |
| **6** | Max 4 catégories | Parcours 27 fiches / script shell | Aucun produit **> 4** catégories e-commerce | ☑ | ☑ |
| **7** | Min 1 catégorie | Les 27 produits | Chacun a la **principale** du mapping (+ secondaires si prévues) | ☑ | ☑ |
| **8** | Porte Incontournables | `GET /incontournables` | **301** → `/shop?marketone_mode=featured` ; grille filtrée | ☑ | ☑ |
| **9** | Shop général | `/shop` | **200**, grille produits recette visible | ☑ | ☑ |
| **10** | Filtre catégorie Odoo | `/shop` → filtre **Biscuits salés** | Crackers, chips, maniocookies, palets listés | ☑ | ☑ |
| **11** | Indépendance origine | Crackers : catégories validées ; origine non modifiée | Origine BO **Martinique** — hors chantier Catégories | ☑ | ☑ |
| **12** | Kits conditionnels | Assortiment apéritif · Trio sirops | Principale **Kits & Coffrets** (condition MOA lot/coffret) | ☑ | ☑ |
| **13** | Non-régression Savoirs | `GET /savoirs` | **404** — pas de hub Savoirs déployé dans ce lot | ☑ | ☑ |

---

## Preuves de contrôle (captures MOA)

Conservées comme pièces jointes de recette (hors dépôt git si non versionnées) :

| Fichier | Contenu |
|---------|---------|
| `marketone_catalogue_shop.png` | Grille `/shop` |
| `marketone_catalogue_biscuits_sales.png` | Filtre catégorie **Biscuits salés** |
| `marketone_catalogue_featured.png` | Porte **Incontournables** (`marketone_mode=featured`) |

---

## Contrôles BO (échantillon script)

```bash
docker exec -i sandbox-odoo19-odoo-1 odoo shell -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 --no-http <<'PY'
Product = env['product.template'].sudo()
domain = [('active','=',True),('sale_ok','=',True),('is_published','=',True)]
for p in Product.search(domain, order='name'):
    n = len(p.public_categ_ids)
    flag = 'OK' if 1 <= n <= 4 else 'ANOMALIE'
    print(flag, n, p.name, '->', ', '.join(p.public_categ_ids.mapped('name')))
PY
```

**Résultat attendu** : **27** lignes `OK` ; aucune `ANOMALIE` — **obtenu**.

---

## Synthèse recette

| Champ | Valeur |
|-------|--------|
| Date | 2026-05-19 |
| Exécutant | Équipe technique (sandbox) + validation MOA |
| Résultat global | ☑ **GO** |
| Écarts | Aucun bloquant |
| Suite | Ticket contrainte technique (principale obligatoire · max 4 en BO) · menu Catégories front · harmonisation Origines / Culture (chantier séparé) |

---

## Références

- [`MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md`](../../cadrage/MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md)
- [`TAXONOMIE_CATALOGUE.md`](../../cadrage/TAXONOMIE_CATALOGUE.md)
- [`ENV_REFERENCE.md`](../reference/ENV_REFERENCE.md)
