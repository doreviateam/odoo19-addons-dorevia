# TICKET — Application BO catégories e-commerce catalogue recette

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_CATALOGUE_CATEGORIES_BO_RECETTE` |
| **Type** | **BO + recette manuelle** — **aucun code** |
| **Statut** | **Clôturé — GO MOA** (2026-05-19) — BO `ckr-marketone-01` + recette [`RECETTE_MANUELLE_CATALOGUE_CATEGORIES.md`](../recette/RECETTE_MANUELLE_CATALOGUE_CATEGORIES.md) |
| **Base** | `ckr-marketone-01` |
| **Instance** | `sandbox-odoo19` — http://localhost:18079 |
| **Version module de référence** | `19.0.10.1.0` (grille boutique) — **pas** de montée version requise pour ce ticket |
| **ADR** | [ADR-029](../cadrage/DECISIONS.md#adr-029--taxonomie-catalogue-convention-odoo-catégories-e-commerce) |
| **Contrats** | [C3.C](../cadrage/CONTRACTS.md#c3c--taxonomie-catalogue-moa-2026-05-19) |
| **Mapping source** | [`MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md`](../cadrage/MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md) |
| **Recette** | [`RECETTE_MANUELLE_CATALOGUE_CATEGORIES.md`](../recette/RECETTE_MANUELLE_CATALOGUE_CATEGORIES.md) |
| **Doctrine** | [`TAXONOMIE_CATALOGUE.md`](../cadrage/TAXONOMIE_CATALOGUE.md) |

---

## Objectif

Appliquer dans **`ckr-marketone-01`** le mapping **produit → catégorie principale + catégories secondaires** validé MOA (27 produits vendables), en s’appuyant sur le standard Odoo **`product.public.category`**.

```text
Livrable attendu :
- catégories e-commerce créées en BO (principales + secondaires manquantes) ;
- chaque produit recette rattaché selon le tableau de mapping (max 4 catégories / produit) ;
- recette manuelle MOA signée ;
- aucun changement de code Marketone.
```

---

## Contexte

| Élément | État |
|---------|------|
| Doctrine ADR-029 / C3.C | **GO** — commits doc `2a0ffb8`, `2e77600`, `6e55613` |
| Mapping 27 produits | **GO MOA** — [`MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md`](../cadrage/MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md) |
| BO actuel | 1 catégorie publique : **Incontournables** (tous les produits) |
| Porte Incontournables (Lot 6.1) | **Livré** — doit rester fonctionnelle après rattachements |

**Indépendance Catégories / Origines** : ce ticket **ne modifie pas** les attributs Origine ni les profils Culture. L’harmonisation Martinique / Guadeloupe = chantier **Origines / Culture** séparé.

---

## Périmètre

| Inclus | Détail |
|--------|--------|
| Création BO | 13 catégories **principales** + secondaires manquantes (voir § Arborescence) |
| Rattachement | 27 `product.template` vendables publiés — ligne par ligne selon mapping |
| Vérification | Recette manuelle + contrôles `/shop` et porte Incontournables |
| Convention | Min **1** / max **4** catégories e-commerce par produit (1 principale + 0–3 secondaires) |

---

## Hors périmètre (strict)

| Exclu | Raison |
|-------|--------|
| **Code** Python / XML / tests / `-u` module pour contraintes | Ticket technique **futur** (principale obligatoire, max 4, marquage principale/secondaire) |
| **`marketone.shop.collection`** | ADR-029 — reporté |
| **Savoirs v1** | Chantier distinct — pas de mélange (`marketone.savoir.recipe`, recette exec, manifest Savoirs) |
| **Harmonisation origines** | Chantier Origines / Culture |
| **Menu transversal Catégories** (front) | Cible UX — ticket front ultérieur |
| **Lot 6.3** portes Boutique | Gel MOA — hors ce ticket |
| Produits « Recette … » | Non vendables — doctrine Savoirs / Boutique |

---

## Arborescence cible `product.public.category`

### Catégories principales (13) — à créer

Ordre indicatif pour le menu futur :

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
13. Miels  

### Catégories secondaires — état BO

| Libellé | BO actuel | Action |
|---------|-----------|--------|
| **Incontournables** | Existe | Conserver — `website_id` = site courant (prérequis Lot 6.1) |
| **Apéritif créole** | Absente | Créer |
| **Cuisine du manioc** | Absente | Créer |
| **Idées cadeaux** | Absente | Créer |

> **Note Odoo** : Marketone ne distingue pas encore techniquement « principale » vs « secondaire » en BO. La convention est **documentaire** : la principale est celle du mapping ; les autres rattachements sont secondaires. Ne pas dupliquer une principale comme seule catégorie sans les secondaires prévues quand le mapping en liste.

---

## Procédure BO (pas à pas)

### Phase 0 — Prérequis

- [ ] Base **`ckr-marketone-01`** sélectionnée  
- [ ] Site web **My Website** (ou site recette MOA) actif  
- [ ] Mapping imprimé ou ouvert : [`MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md`](../cadrage/MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md)  
- [ ] **Aucun** produit test nommé « Recette … » dans le périmètre  

### Phase 1 — Créer les catégories e-commerce

**Menu Odoo** : *Site web* → *eCommerce* → *Catégories de produits eCommerce* (`product.public.category`).

Pour **chaque** libellé (13 principales + 3 secondaires à créer) :

- [ ] Nom exact selon mapping (accents, casse MOA)  
- [ ] **`website_id`** = site courant (**obligatoire** — même règle que Incontournables, ADR-023)  
- [ ] Publiée / visible selon options Odoo 19 du site  

**Contrôle** : compter **17** catégories publiques au total (13 + 4 secondaires dont Incontournables déjà existante).

### Phase 2 — Rattacher les produits (27)

**Menu** : *Ventes* → *Produits* → *Produits* — filtrer : publiés, vendables, catalogue recette.

Pour **chaque ligne** du tableau mapping :

- [ ] Onglet **Ventes** / **Site web** → **Catégories eCommerce**  
- [ ] Ajouter la **catégorie principale** (nature du produit)  
- [ ] Conserver ou ajouter **Incontournables** si listé en secondaire  
- [ ] Ajouter les autres secondaires (**max 3** secondaires, **max 4** au total)  
- [ ] Vérifier le **total** ≤ 4  

**Produits sous condition MOA** (vérifier le conditionnement réel avant validation) :

| Produit | Condition |
|---------|-----------|
| Assortiment apéritif créole | Principale **Kits & Coffrets** seulement si lot / assortiment packagé |
| Trio sirops des Antilles | Principale **Kits & Coffrets** si trio packagé ; sinon **Sirops** |

**Exemple validé — Crackers manioc Sainte-Anne** :

- Principale : **Biscuits salés**  
- Secondaires : **Incontournables**, **Apéritif créole**, **Cuisine du manioc**  
- **Ne pas** modifier l’origine dans ce ticket  

### Phase 3 — Contrôles rapides BO

- [ ] Aucun produit recette sans au moins **1** catégorie e-commerce  
- [ ] Aucun produit recette avec **> 4** catégories e-commerce  
- [ ] Aucun produit n’a **Incontournables** comme seule catégorie **sans** principale du mapping (état transitoire actuel à corriger)  

### Phase 4 — Recette MOA

Exécuter : [`RECETTE_MANUELLE_CATALOGUE_CATEGORIES.md`](../recette/RECETTE_MANUELLE_CATALOGUE_CATEGORIES.md).

---

## Critères GO / NO GO

| ID | Critère | GO |
|----|---------|-----|
| G1 | 13 principales + secondaires requises créées avec `website_id` site courant | ☑ (17 catégories, website 1) |
| G2 | 27 produits conformes au mapping (principale + secondaires, max 4) | ☑ (0 seul Incontournables) |
| G3 | Porte `/incontournables` → filtre toujours les produits avec catégorie **Incontournables** | ☑ (301, 27 produits) |
| G4 | `/shop` affiche les produits ; filtres catégories Odoo cohérents | ☑ (200) |
| G5 | Aucun code / module version changé pour ce lot | ☑ |
| G6 | Origines **non** modifiées dans ce ticket (sauf correction accidentelle annulée) | ☑ |
| G7 | Recette manuelle signée MOA | ☑ — **GO MOA** 2026-05-19 |

**NO GO** si : produit hors mapping massif · perte porte Incontournables · mélange avec déploiement Savoirs v1 non validé.

### Clôture MOA (2026-05-19)

| Point validé | Détail |
|--------------|--------|
| Catégories | **17** sur site courant |
| Produits | **27/27** conformes mapping · règle **1–4** catégories |
| Portes | `/shop` **200** · `/incontournables` **301** → `featured` |
| Filtre Odoo | **Biscuits salés** opérationnel |
| Savoirs | `/savoirs` **404** — non-régression |
| Code | **Aucun** changement · **pas** de montée version module |
| Preuves | `marketone_catalogue_shop.png` · `marketone_catalogue_biscuits_sales.png` · `marketone_catalogue_featured.png` |

---

## Ticket technique ultérieur (rappel — ne pas faire ici)

Pour **garantir** en BO la règle min 1 / max 4 et le marquage principale vs secondaire :

- champ ou convention UI Marketone sur `product.template` ;  
- contrainte `public_categ_ids` ;  
- **pas** de `marketone.shop.collection`.  

À cadrer **après** application réussie de ce mapping en recette.

---

## Références

- [`cadrage/MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md`](../cadrage/MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md)  
- [`cadrage/TAXONOMIE_CATALOGUE.md`](../cadrage/TAXONOMIE_CATALOGUE.md)  
- [`recette/ENV_REFERENCE.md`](../recette/ENV_REFERENCE.md)  
- Lot 6.1 : [`TICKET_MARKETONE_LOT6_1_INCONTOURNABLES_EXEC.md`](TICKET_MARKETONE_LOT6_1_INCONTOURNABLES_EXEC.md)
