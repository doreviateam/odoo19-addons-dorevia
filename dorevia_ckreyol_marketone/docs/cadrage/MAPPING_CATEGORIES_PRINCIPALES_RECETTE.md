# Mapping catégories principales — catalogue recette `ckr-marketone-01`

| Champ | Valeur |
|-------|--------|
| **Statut** | **GO MOA** — mapping appliqué et recette validée (2026-05-19) |
| **Base** | `ckr-marketone-01` — lecture seule au moment de l’analyse |
| **Doctrine** | [TAXONOMIE_CATALOGUE.md](TAXONOMIE_CATALOGUE.md) · [ADR-029](DECISIONS.md#adr-029--taxonomie-catalogue-convention-odoo-catégories-e-commerce) · [C3.C](CONTRACTS.md#c3c--taxonomie-catalogue-moa-2026-05-19) |
| **Modifications BO** | **Appliquées** sur `ckr-marketone-01` (2026-05-19) — ticket BO clôturé |

---

## Périmètre analysé

**Critères d’inclusion** : `product.template` avec `active=True`, `sale_ok=True`, `is_published=True`, nom sans « Recette ».

| Élément | Résultat |
|---------|----------|
| Produits retenus | **27** |
| Recettes produit / Culture / Savoirs | **Exclus** (0 recette produit en base ; 0 `marketone.savoir.recipe`) |
| Catégorie e-commerce BO (post-application) | **17** catégories · 27 produits conformes mapping (min 1 / max 4) |

---

## Liste cible des catégories principales (13)

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
13. **Miels** *(13e principale — arbitrage MOA 2026-05-19)*

**Règle Kits & Coffrets** : catégorie principale **uniquement** lorsque le produit vendu est réellement un kit ou un coffret packagé.

---

## Règle de rattachement catégories e-commerce (MOA)

Chaque produit vendable doit être associé à **au moins 1** catégorie e-commerce (`product.public.category`). Cette catégorie correspond à la **catégorie principale**.

| Contrainte | Valeur |
|------------|--------|
| **Minimum** | 1 catégorie e-commerce (principale) |
| **Maximum** | 4 catégories e-commerce au total |
| **Décomposition** | 1 principale obligatoire + **0 à 3** secondaires maximum |

> Formulation contractuelle : voir **C3.C.9–C3.C.11** et **ADR-029**. Contrôle technique BO = **ticket dédié** (hors scope immédiat).

**Objectifs** : menu Catégories exploitable · éviter le fourre-tout · lecture claire · standard Odoo sans `marketone.shop.collection`.

### Indépendance catégorisation / origine (MOA)

La **catégorisation** des produits **ne dépend pas** de l’origine.

| Axe | Rôle | Chantier |
|-----|------|----------|
| Catégorie principale | Nature du produit | **Catégories** |
| Catégories secondaires | Sélections, usages, mises en avant | **Catégories** |
| Origine | Territoire | **Origines / Culture** (harmonisation BO distincte) |
| Porte | Entrée `/shop?marketone_mode=…` | Portes Boutique |

Même si l’origine BO est à harmoniser avec les contenus Culture, cela **ne modifie pas** la catégorie principale ni les secondaires retenues au mapping.

**Exemple validé — Crackers manioc Sainte-Anne** (chantier Catégories **clos**) :

- Principale : **Biscuits salés**
- Secondaires : **Incontournables**, **Apéritif créole**, **Cuisine du manioc**
- Origine Martinique / Guadeloupe : **hors périmètre** de ce mapping — chantier Origines / Culture

---

## Arbitrages MOA (produits ambigus)

| Produit | Décision MOA |
|---------|----------------|
| Miel créole baie rose | Principale **Miels** (13e rayon) |
| Assortiment apéritif créole | Principale **Kits & Coffrets** si assortiment / lot packagé ; sinon requalifier selon contenu |
| Marinade jerk authentique | Principale **Assaisonnements** |
| Shrub agrumes créole | Principale **Sirops** |
| Trio sirops des Antilles | Principale **Kits & Coffrets** si trio packagé ; sinon **Sirops** |
| Crackers manioc Sainte-Anne | Principale **Biscuits salés** ; secondaires Incontournables, Apéritif créole, Cuisine du manioc — **validé** (origine = chantier Origines / Culture, sans impact sur les catégories) |

---

## Table de mapping produit → catégories (cible MOA)

*Secondaires **existantes** en BO au 2026-05-19 : **Incontournables** (seule catégorie publique créée). Les autres secondaires sont **proposées** (à créer en BO après GO final).*

| Produit | Catégorie principale | Catégories secondaires | Total | Origine (BO) | Commentaire |
|---------|----------------------|------------------------|-------|--------------|-------------|
| Assortiment apéritif créole | Kits & Coffrets | Incontournables, Apéritif créole, Idées cadeaux | 4 | Martinique | MOA : OK si lot packagé |
| Biscuits coco vanille | Biscuits sucrés | Incontournables | 2 | Guadeloupe | OK |
| Café arabica Antilles | Boissons | Incontournables | 2 | Martinique | OK |
| Chips banane plantain salées | Biscuits salés | Incontournables, Apéritif créole, Cuisine du manioc | 4 | Guadeloupe | OK |
| Chutney mangue verte | Condiments | Incontournables, Apéritif créole | 3 | Guadeloupe | OK |
| Coffret biscuits et douceurs | Kits & Coffrets | Incontournables, Idées cadeaux, Apéritif créole | 4 | Guadeloupe | OK — coffret réel |
| Coffret gourmand îles créoles | Kits & Coffrets | Incontournables, Idées cadeaux | 3 | Reunion | OK — coffret réel |
| Colombo des Antilles (épices) | Épices | Incontournables | 2 | Martinique | OK |
| Confiture ananas vanille | Confitures | Incontournables, Idées cadeaux | 3 | Reunion | OK — exemple MOA |
| Confiture banane flambée | Confitures | Incontournables, Idées cadeaux | 3 | Guadeloupe | OK |
| Confiture fruits de la passion | Confitures | Incontournables | 2 | Martinique | OK |
| Crackers manioc Sainte-Anne | Biscuits salés | Incontournables, Apéritif créole, Cuisine du manioc | 4 | Martinique (BO) | **OK catégories** — origine Martinique/Guadeloupe : chantier Origines / Culture |
| Infusion vétiver citronnelle | Boissons | Incontournables | 2 | Guadeloupe | OK |
| Maniocookies salés La Platine | Biscuits salés | Incontournables, Apéritif créole, Cuisine du manioc | 4 | Guadeloupe | OK |
| Marinade jerk authentique | Assaisonnements | Incontournables, Apéritif créole | 3 | Martinique | MOA : Assaisonnements |
| Mélange épices caraïbes | Épices | Incontournables | 2 | Martinique | OK |
| Miel créole baie rose | Miels | Incontournables, Idées cadeaux | 3 | Reunion | MOA : principale Miels |
| Mix beignets manioc | Farines | Incontournables, Cuisine du manioc | 3 | Martinique | OK |
| Palets manioc croustillants La Platine | Biscuits salés | Incontournables, Apéritif créole, Cuisine du manioc | 4 | Guadeloupe | OK |
| Pâtes de manioc Mayotte | Fécules | Incontournables, Cuisine du manioc | 3 | Guadeloupe | OK |
| Rougail épices Réunion | Assaisonnements | Incontournables | 2 | Reunion | OK |
| Sauce piment cadji | Sauces | Incontournables, Apéritif créole | 3 | Reunion | OK |
| Semoule manioc fine Mayotte | Fécules | Incontournables, Cuisine du manioc | 3 | Reunion | OK |
| Shrub agrumes créole | Sirops | Incontournables, Apéritif créole | 3 | Martinique | MOA : Sirops |
| Sirop de canne vanille | Sirops | Incontournables | 2 | Martinique | OK |
| Tartinade coco citron vert | Condiments | Incontournables | 2 | Guadeloupe | OK |
| Trio sirops des Antilles | Kits & Coffrets | Incontournables, Idées cadeaux | 3 | Guadeloupe | MOA : Kits si trio packagé ; sinon principale Sirops |

---

## Synthèse par catégorie principale (cible)

| Catégorie principale | Nb produits |
|----------------------|------------|
| Biscuits salés | 4 |
| Biscuits sucrés | 1 |
| Boissons | 2 |
| Condiments | 2 |
| Confitures | 3 |
| Épices | 2 |
| Assaisonnements | 2 |
| Sauces | 1 |
| Sirops | 2 |
| Farines | 1 |
| Fécules | 2 |
| Kits & Coffrets | 4 |
| Miels | 1 |
| **Total** | **27** |

---

## État BO actuel vs cible doctrine

| Aspect | BO actuel (`ckr-marketone-01`) | Cible MOA |
|--------|--------------------------------|-----------|
| Catégories `product.public.category` | **17** (13 principales + 4 secondaires) | Aligné MOA |
| Rattachement produits | **27/27** selon mapping | 1 principale + 0–3 secondaires (max 4) · **0** produit avec Incontournables seul |
| Distinction principale / secondaire | Non matérialisée | Convention + futur ticket technique |
| Origine attribut | Martinique · Guadeloupe · Reunion | Chantier **Origines / Culture** (indépendant des catégories e-commerce) |

**Secondaires à créer en BO** (proposition, hors Incontournables déjà présente) : *Apéritif créole* · *Cuisine du manioc* · *Idées cadeaux* — après validation finale et création des 13 principales.

---

## Prochaines étapes

| Étape | Document |
|-------|----------|
| Application BO + recette `ckr-marketone-01` | [`TICKET_MARKETONE_CATALOGUE_CATEGORIES_BO_RECETTE.md`](../tickets/TICKET_MARKETONE_CATALOGUE_CATEGORIES_BO_RECETTE.md) |
| Grille de validation MOA | [`RECETTE_MANUELLE_CATALOGUE_CATEGORIES.md`](../recette/RECETTE_MANUELLE_CATALOGUE_CATEGORIES.md) |
| Contrainte technique (ultérieur) | Ticket dédié — principale obligatoire · max 4 · marquage principale/secondaire |

---

## Références

- Analyse initiale : conversation MOA 2026-05-19 (27 produits, lecture `ckr-marketone-01`)  
- [`TAXONOMIE_CATALOGUE.md`](TAXONOMIE_CATALOGUE.md)  
- [`DECISIONS.md`](DECISIONS.md) — ADR-029  
- [`CONTRACTS.md`](CONTRACTS.md) — C3.C
