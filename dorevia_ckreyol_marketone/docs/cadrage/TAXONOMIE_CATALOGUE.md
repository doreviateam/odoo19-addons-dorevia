# Taxonomie catalogue C-Kreyol / Marketone

| Champ | Valeur |
|-------|--------|
| **Statut** | **GO MOA** — doctrine catalogue (2026-05-19, amendements standard Odoo + navigation transversale) |
| **ADR** | [ADR-029](DECISIONS.md#adr-029--taxonomie-catalogue-convention-odoo-catégories-e-commerce) |
| **Contrat** | [C3.C](CONTRACTS.md#c3c--taxonomie-catalogue-moa-2026-05-19) |

---

## Règle centrale (convention Odoo pragmatique)

**Support technique** : `product.public.category` (standard `website_sale`).

Odoo autorise **plusieurs** catégories e-commerce par produit. Marketone introduit une **convention métier** sur ce support :

```text
Un produit = une catégorie e-commerce principale (convention MOA).
Un produit = 0 à 3 catégories e-commerce secondaires (max 4 catégories au total).
Pas de modèle marketone.shop.collection pour l’instant.
```

| Rôle MOA | Support Odoo | Cardinalité convention |
|----------|--------------|------------------------|
| **Catégorie principale** | `product.public.category` | **1** par produit — nature du produit (obligatoire) |
| **Catégories secondaires** | `product.public.category` (autres rattachements) | **0..3** — sélections, usages, mises en avant, parcours complémentaires |
| **Total catégories e-commerce** | — | **min 1 · max 4** par produit vendable |
| **Origine** | Attribut **Origine** + `marketone.shop.origin` | Territoire(s) |
| **Porte** | `/shop?marketone_mode=…` | Entrée navigation — **pas** une catégorie |

> **Hors scope immédiat** : modèle dédié `marketone.shop.collection` — **reporté** ; réévaluation possible si les catégories secondaires deviennent insuffisantes (volume, SEO, gouvernance BO).

### Règle synthétique (MOA)

```text
La catégorie principale structure le menu.
Les catégories secondaires enrichissent les parcours.
Les origines situent le produit.
Les portes orientent l’entrée.
```

---

## Pourquoi la catégorie principale ?

La notion de **catégorie principale** est introduite afin d’offrir au visiteur une **navigation transversale stable par nature de produit**.

Même si Odoo permet plusieurs catégories e-commerce publiques par produit, Marketone distingue une **catégorie principale de référence**, utilisée pour structurer le menu de navigation par catégories, et des **catégories secondaires** utilisées pour les sélections, usages ou mises en avant.

### Objectif utilisateur

Permettre au visiteur de parcourir la boutique par **grands rayons lisibles**, qui répondent à :

> **« Quel type de produit est-ce que je cherche ? »**

**Liste cible des catégories principales** (MOA 2026-05-19) : Biscuits salés · Biscuits sucrés · Épices · Assaisonnements · Sauces · Condiments · Confitures · Sirops · Boissons · Farines · Fécules · Kits & Coffrets · **Miels**.

> **Kits & Coffrets** : principale **uniquement** si le produit est un kit ou coffret packagé réel.

Ces rayons alimentent un menu transversal **Catégories** (cible UX — hors scope code immédiat).

### Rattachement catégories e-commerce (MOA)

Chaque produit vendable doit être rattaché à **au moins une** catégorie e-commerce, correspondant à sa **catégorie principale**. Les catégories secondaires sont autorisées pour les sélections, usages et mises en avant, **dans la limite de trois rattachements supplémentaires**. Un produit **ne doit pas dépasser quatre** catégories e-commerce au total.

**Mapping catalogue recette** : [`MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md`](MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md) (27 produits `ckr-marketone-01`, validation MOA 2026-05-19).

---

## Définitions

### Catégorie principale (convention MOA)

**Question** : « Qu’est-ce que c’est ? » / « Quel type de produit je cherche ? »

- **rayon principal** / nature du produit ;
- nature **stable** et **descriptive** ;
- une seule catégorie **désignée principale** par produit (convention métier — marquage technique = ticket futur si besoin) ;
- **référence** pour structurer le menu de navigation par catégories ;
- exemples : Biscuits salés · Confitures · Épices · Boissons.

### Catégories secondaires (convention MOA)

**Question** : « Dans quelles sélections ou contextes le montrer ? »

- rattachements **additionnels** à d’autres `product.public.category` ;
- transversales à la nature du produit ;
- intention d’achat, mise en avant, usage, rayon complémentaire ;
- exemples : Incontournables · Apéritif créole · Cuisine du manioc · Idées cadeaux.

**Alignement Lot 6.1** : la porte **Incontournables** filtre sur la catégorie publique « Incontournables » — elle est une **catégorie secondaire** (sélection), pas la catégorie principale du produit.

### Origine

Territoire créolophone (attribut catalogue + profil Culture/Boutique). **Distinct et indépendant** des catégories e-commerce : la catégorisation d’un produit **ne dépend pas** de son origine. L’harmonisation origine BO / contenus Culture relève du chantier **Origines / Culture**, pas du chantier **Catégories**.

### Porte

Entrée de navigation vers une sélection sur `/shop`. Consomme une source Odoo (souvent une **catégorie secondaire**, un attribut, une pricelist…).

---

## Exemple MOA

**Produit** : Crackers manioc Sainte-Anne

| Rôle | Valeur(s) |
|------|-----------|
| **Catégorie principale** | Biscuits salés |
| **Catégories secondaires** | Incontournables · Apéritif créole · Cuisine du manioc |
| **Origine** | Martinique ou Guadeloupe — chantier Origines / Culture (hors catégories) |

```text
Catégorie principale   → rayon / nature du produit (menu Catégories)
Catégories secondaires → sélections / usages / mises en avant
Origine                → territoire
Porte                  → entrée /shop (ex. Incontournables → filtre catégorie secondaire)
```

### Conséquence UX (exemple Crackers)

Dans un menu transversal **Catégories**, le produit apparaît **d’abord** sous :

- **Biscuits salés**

Il peut aussi être trouvé via :

- **Incontournables** (porte / catégorie secondaire) ;
- **Origines** → territoire attribut (parcours complémentaire ; harmonisation BO hors chantier Catégories) ;
- **Apéritif créole** ;
- **Cuisine du manioc**.

---

## Conséquences

| # | Conséquence |
|---|-------------|
| 1 | **Ne pas** implémenter `marketone.shop.collection` sans ticket dédié. |
| 2 | En BO : chaque produit a une catégorie **principale** obligatoire + **0 à 3** secondaires (max **4** catégories e-commerce ; dont Incontournables si pertinent). |
| 3 | **Ne pas** confondre catégorie principale et secondaire dans les libellés BO (ex. « Incontournables » = secondaire, pas nature du produit). |
| 4 | Les portes Boutique s’appuient sur le **standard Odoo** (catégorie, attribut, pricelist…) — pas sur un moteur parallèle. |
| 5 | **Culture** et **Savoirs** hors grille `/shop` ; pas de recette comme `product.template` vendable. |
| 6 | **Pas de code** pour matérialiser « principale vs secondaire » ni le menu transversal Catégories sans ticket MOA. |
| 7 | Menu **Catégories** (cible UX) : structuré par catégories **principales** ; les secondaires, origines et portes **enrichissent** les parcours sans remplacer le rayon de référence. |

---

## Évolution documentée

| Date | Décision |
|------|----------|
| 2026-05-19 (v1) | Distinction catégorie / **collection dédiée** — cible `marketone.shop.collection`. |
| 2026-05-19 (v2) | **Amendement MOA** : adapter au standard Odoo — principale + secondaires sur `product.public.category` ; collection dédiée **mise de côté**. |
| 2026-05-19 (v3) | **Clarification MOA** : motivation catégorie principale = navigation transversale stable par nature ; règle synthétique menu / parcours / origine / porte. |
| 2026-05-19 (v4) | **13e principale Miels** ; règle min 1 / max 4 catégories e-commerce ; mapping recette 27 produits validé en principe. |
| 2026-05-19 (v5) | **Indépendance catégorisation / origine** ; Crackers validé en catégories (Biscuits salés + 3 secondaires). |

---

## Références

- [`MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md`](MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md) — tableau produit → catégories (`ckr-marketone-01`)
- [`CONTRACTS.md`](CONTRACTS.md) — C3, C3.A, C3.C
- [`DECISIONS.md`](DECISIONS.md) — ADR-023, ADR-029
- [`NOTE_UNIVERS_CK_MARKETONE.md`](NOTE_UNIVERS_CK_MARKETONE.md) — § Taxonomie catalogue
- [`TICKET_MARKETONE_CONSOLIDATION_PORTES_BOUTIQUE.md`](../tickets/TICKET_MARKETONE_CONSOLIDATION_PORTES_BOUTIQUE.md)
