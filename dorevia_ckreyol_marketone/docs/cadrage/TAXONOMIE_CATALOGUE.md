# Taxonomie catalogue C-Kreyol / Marketone

| Champ | Valeur |
|-------|--------|
| **Statut** | **GO MOA** — doctrine catalogue (2026-05-19, amendement standard Odoo) |
| **ADR** | [ADR-029](DECISIONS.md#adr-029--taxonomie-catalogue-convention-odoo-catégories-e-commerce) |
| **Contrat** | [C3.C](CONTRACTS.md#c3c--taxonomie-catalogue-moa-2026-05-19) |

---

## Règle centrale (convention Odoo pragmatique)

**Support technique** : `product.public.category` (standard `website_sale`).

Odoo autorise **plusieurs** catégories e-commerce par produit. Marketone introduit une **convention métier** sur ce support :

```text
Un produit = une catégorie e-commerce principale (convention MOA).
Un produit = zéro, une ou plusieurs catégories e-commerce secondaires.
Pas de modèle marketone.shop.collection pour l’instant.
```

| Rôle MOA | Support Odoo | Cardinalité convention |
|----------|--------------|------------------------|
| **Catégorie principale** | `product.public.category` | **1** par produit — nature du produit |
| **Catégories secondaires** | `product.public.category` (autres rattachements) | **0..n** — sélections, usages, mises en avant, rayons complémentaires |
| **Origine** | Attribut **Origine** + `marketone.shop.origin` | Territoire(s) |
| **Porte** | `/shop?marketone_mode=…` | Entrée navigation — **pas** une catégorie |

> **Hors scope immédiat** : modèle dédié `marketone.shop.collection` — **reporté** ; réévaluation possible si les catégories secondaires deviennent insuffisantes (volume, SEO, gouvernance BO).

---

## Définitions

### Catégorie principale (convention MOA)

**Question** : « Qu’est-ce que c’est ? »

- nature **stable** et **descriptive** du produit ;
- une seule catégorie **désignée principale** par produit (convention métier — marquage technique = ticket futur si besoin) ;
- exemples : Biscuits salés · Confitures · Épices · Boissons.

### Catégories secondaires (convention MOA)

**Question** : « Dans quelles sélections ou contextes le montrer ? »

- rattachements **additionnels** à d’autres `product.public.category` ;
- transversales à la nature du produit ;
- intention d’achat, mise en avant, usage, rayon complémentaire ;
- exemples : Incontournables · Apéritif · Cuisine du manioc · Idées cadeaux.

**Alignement Lot 6.1** : la porte **Incontournables** filtre sur la catégorie publique « Incontournables » — elle est une **catégorie secondaire** (sélection), pas la catégorie principale du produit.

### Origine

Territoire créolophone (attribut catalogue + profil Culture/Boutique). Distinct des catégories e-commerce.

### Porte

Entrée de navigation vers une sélection sur `/shop`. Consomme une source Odoo (souvent une **catégorie secondaire**, un attribut, une pricelist…).

---

## Exemple MOA

**Produit** : Crackers manioc Sainte-Anne

| Rôle | Valeur(s) |
|------|-----------|
| **Catégorie principale** | Biscuits salés |
| **Catégories secondaires** | Incontournables · Apéritif · Cuisine du manioc |
| **Origine** | Guadeloupe |

```text
Catégorie principale   → nature du produit
Catégories secondaires → sélections / mises en avant / rayons complémentaires
Origine                → territoire
Porte                  → entrée /shop (ex. Incontournables → filtre catégorie secondaire)
```

---

## Conséquences

| # | Conséquence |
|---|-------------|
| 1 | **Ne pas** implémenter `marketone.shop.collection` sans ticket dédié. |
| 2 | En BO : chaque produit a une catégorie **principale** descriptive + des catégories **secondaires** optionnelles (dont Incontournables si pertinent). |
| 3 | **Ne pas** confondre catégorie principale et secondaire dans les libellés BO (ex. « Incontournables » = secondaire, pas nature du produit). |
| 4 | Les portes Boutique s’appuient sur le **standard Odoo** (catégorie, attribut, pricelist…) — pas sur un moteur parallèle. |
| 5 | **Culture** et **Savoirs** hors grille `/shop` ; pas de recette comme `product.template` vendable. |
| 6 | **Pas de code** pour matérialiser « principale vs secondaire » sans ticket MOA (champ, convention BO documentée, ou UI). |

---

## Évolution documentée

| Date | Décision |
|------|----------|
| 2026-05-19 (v1) | Distinction catégorie / **collection dédiée** — cible `marketone.shop.collection`. |
| 2026-05-19 (v2) | **Amendement MOA** : adapter au standard Odoo — principale + secondaires sur `product.public.category` ; collection dédiée **mise de côté**. |

---

## Références

- [`CONTRACTS.md`](CONTRACTS.md) — C3, C3.A, C3.C
- [`DECISIONS.md`](DECISIONS.md) — ADR-023, ADR-029
- [`NOTE_UNIVERS_CK_MARKETONE.md`](NOTE_UNIVERS_CK_MARKETONE.md) — § Taxonomie catalogue
- [`TICKET_MARKETONE_CONSOLIDATION_PORTES_BOUTIQUE.md`](../tickets/TICKET_MARKETONE_CONSOLIDATION_PORTES_BOUTIQUE.md)
