# Arbitrage architecture — Suite cadrage2 CK Marketone

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-06-08 |
| **Contexte** | Lot BO `19.0.16.0.0` clôturé **GO avec réserves** |
| **Statut** | **Validé MOA** (2026-06-08) — enregistré [ADR-034](../cadrage/DECISIONS.md#adr-034--arbitrage-architecture-cadrage2-socle-odoo-natif) |
| **Objectif** | Arbitrer Blog / Forum et figer la compatibilité front ↔ Odoo natif **avant** reprise des lots front gelés |

---

## 1. Contexte MOA

Le lot recadrage BO produit est clôturé. Avant toute reprise des lots UX front gelés, la MOA souhaite :

1. **Confirmer la doctrine Blog / Forum** ;
2. **Confirmer** que toute personnalisation front reste compatible avec les fonctionnalités natives Odoo ;
3. **Identifier explicitement** les briques eCommerce Odoo à préserver : catégories, attributs, variantes, listes de prix, promotions, panier, wishlist, checkout, paiement, livraison, portail client, SEO.

**Objectif** : éviter qu’un front sur mesure limite l’exploitation future du standard Odoo.

---

## 2. Principe directeur (proposition)

```text
Odoo exécute. Marketone habille et oriente.
```

| Couche | Rôle | Règle |
|--------|------|-------|
| **Moteur Odoo** | Catalogue, prix, stock, panier, checkout, paiement, livraison, compte | **Intouchable** — extension par héritage, jamais remplacement |
| **Présentation Marketone** | SCSS scoped, QWeb inherit, navigation CK, portes `/shop` | Autorisée si **non bloquante** pour le standard |
| **Enrichissement CK** | Collections, origines éditoriales, Culture, Savoirs | Modèles dédiés **minimalistes** — pas de parallèle e-commerce |

Ce principe est **déjà inscrit** dans [ADR-002](../cadrage/DECISIONS.md#adr-002--website_sale-moteur-unique), [CONTRACTS.md](../cadrage/CONTRACTS.md) C1–C2 et la recette BO clôturée. L’arbitrage cadrage2 le **rend explicite et opposable** aux futurs lots front.

---

## 3. Doctrine Blog / Forum — proposition d’arbitrage

### 3.1 Rappel : le README cadrage2 vs ADR existantes

Le README cadrage2 cite **Blog** et **Forum** comme briques Odoo à vérifier. Or les ADR Culture / Savoirs / univers CK ont déjà tranché **contre** leur usage comme conteneurs principaux.

### 3.2 Proposition MOA (recommandation Dev)

| Brique Odoo | Décision proposée | Justification |
|-------------|-------------------|---------------|
| **`website_blog`** | **Hors socle CK** — non requis au module Marketone | Culture = pages `/culture/<slug>` (ADR Culture v1/v2) · Savoirs = `marketone.savoir.recipe` (ADR Savoirs v1) · évite blog-like sur `/shop` et double workflow éditorial |
| **`website_forum`** | **Hors socle CK** — non requis | Savoirs = contribution modérée portal, pas forum ouvert (ADR-024, garde-fous univers) |
| **Blog (option ultérieure)** | **Ticket MOA séparé** uniquement si besoin magazine éditorial **hors** Boutique / Culture / Savoirs | Ex. rubrique « Mag CK » SEO long format — pas un prérequis e-commerce |
| **Forum (option ultérieure)** | **Reporté** — au mieux après Savoirs v1 stabilisé | Modération, bruit, dérive SEO |

### 3.3 Cartographie univers → conteneur Odoo

| Univers | Verbe | Conteneur retenu | Module Odoo |
|---------|-------|------------------|-------------|
| **Boutique** | Acheter | `website_sale` + produits / catégories / attributs natifs | `website`, `website_sale`, `portal` |
| **Culture** | Découvrir | Pages `website.page` + route `/culture/<slug>` | `website` (pas `website_blog`) |
| **Savoirs** | Transmettre | Modèle `marketone.savoir.recipe` + portal (cadrage) | Module dédié (pas `website_blog` / `website_forum`) |

### 3.4 Formulation MOA suggérée (à valider)

> CK s’appuie sur **Website + eCommerce + Portal** comme socle.  
> **Blog et Forum ne sont pas des dépendances du module Marketone.**  
> L’éditorial Culture et les Savoirs contributifs utilisent des conteneurs **métier CK minimalistes**, compatibles Odoo, sans dupliquer un CMS parallèle.  
> Toute activation ultérieure de `website_blog` ou `website_forum` fera l’objet d’un **ticket et d’un ADR dédiés**, avec analyse d’impact SEO et parcours achat.

---

## 4. Doctrine compatibilité front ↔ Odoo natif

### 4.1 Règles opposables (proposition)

| # | Règle | Application |
|---|-------|-------------|
| **F1** | **Hériter, ne pas remplacer** | QWeb : `inherit_id` sur templates `website_sale.*` / `website.*` — pas de page catalogue autonome |
| **F2** | **Filtrer via le moteur Odoo** | Domaines catalogue via `_search_get_detail` / `_get_shop_domain` — pas de `search()` parallèle en contrôleur pour la grille |
| **F3** | **Conserver les routes standard** | `/shop`, `/shop/cart`, `/shop/checkout`, `/shop/payment`, `/shop/address`, `/my/orders` — pas de tunnel checkout custom |
| **F4** | **Conserver les modèles standard** | `product.template`, `product.product`, `product.public.category`, `product.attribute`, `sale.order` — extensions OK, doublons interdits |
| **F5** | **JS = interaction légère** | Pattern Odoo 19 `interactions/` · pas de réimplémentation panier / wishlist / variant picker |
| **F6** | **Prix = moteur Odoo** | Affichage prix depuis templates / champs standard — pas de calcul prix custom front |
| **F7** | **Variantes = configurateur natif** | Fiche produit multi-variantes : ne pas court-circuiter le sélecteur Odoo sans ticket MOA |
| **F8** | **SEO = champs natifs d’abord** | `website_meta_*`, slugs Odoo, `is_published` — métadonnées custom seulement en complément documenté |
| **F9** | **Test de non-blocage** | Toute livraison front gelée doit inclure une ligne « fonctionnalité Odoo préservée » dans la recette |

### 4.2 Ce que Marketone fait déjà (conforme)

- Contrôleur `WebsiteSale` hérité — portes en query sur `/shop` ([ADR-003](../cadrage/DECISIONS.md#adr-003--conteneur-shop-unique)).
- Catégories = `product.public.category` · attribut Origines = `product.attribute` `no_variant`.
- Panier / checkout = smoke natif Lot 5 · wishlist = `website_sale_wishlist` + overlay léger.
- Culture = pages website, pas blog.

### 4.3 Points de vigilance identifiés (sans remettre en cause le GO BO)

| Zone | Risque | Mitigation proposée |
|------|--------|---------------------|
| Preview in-place UX-4 | Contournement configurateur variantes multi-valeurs | Limiter preview aux produits `_marketone_preview_full_allowed()` · recette explicite multi-variantes |
| Sidebar catégories custom | Masque filmstrip natif Odoo | Accepté MOA — mais conserver `public_categ_ids` et filtres attributs natifs en parallèle |
| `marketone.shop.collection` | Doublon sémantique vs catégories | ADR-030 : merchandising éditorial · ne remplace pas les catégories eCommerce |
| Modes `promo` / `pack` | Prévus en priorité mais **non implémentés** | Lot futur doit s’appuyer sur **pricelist / promo Odoo**, pas filtre custom prix |
| SEO portes `/shop?…` | URLs query non canonicalisées | Ticket SEO MOA séparé (déjà noté ADR-029+) — ne pas bloquer reprise front |

---

## 5. Matrice — fonctionnalités Odoo eCommerce à préserver

Légende :

| Symbole | Signification |
|---------|---------------|
| ✅ | **Préservé et exploité** aujourd’hui |
| 🟡 | **Préservé mais partiellement** ou enrichissement CK par-dessus |
| ⏳ | **Non implémenté CK** — standard Odoo doit rester **activable sans refonte** |
| ⚠️ | **Vigilance** — personnalisation front existante à ne pas aggraver |
| — | Hors périmètre Marketone actuel |

| Fonctionnalité Odoo | Module / mécanisme | État Marketone | Engagement cadrage2 |
|---------------------|-------------------|----------------|---------------------|
| **Catégories eCommerce** | `product.public.category`, `public_categ_ids` | ✅ Sidebar, portes, BO onglet Publication site | **Préserver** — source de vérité catalogue |
| **Attributs produit** | `product.attribute`, filtres `/shop` | ✅ Origines `no_variant` + filtres natifs sidebar | **Préserver** — pas d’attribut parallèle |
| **Variantes** | `product.product`, configurateur fiche | 🟡 Preview grille = variantes simples uniquement | **Préserver** configurateur natif fiche · ticket si UX variantes |
| **Listes de prix** | `product.pricelist`, règles pricelist | ⏳ Non utilisé en portes (modes `promo`/`pack` à venir) | **Préserver** — futurs lots promo = pricelist Odoo |
| **Promotions** | Pricelist promo, coupons Odoo 19 | ⏳ Non implémenté (priorité modes documentée) | **Préserver** — pas de moteur promo custom |
| **Panier** | `website_sale` cart | ✅ Tunnel natif · SCSS scoped Lot 5 | **Préserver** — pas de JS panier parallèle |
| **Wishlist** | `website_sale_wishlist` | ✅ Dépendance manifest · toggle overlay UX-4 | **Préserver** — pas de modèle wishlist CK |
| **Checkout** | `website_sale` checkout / address | ✅ Smoke natif · `checkout_layout` | **Préserver** — pas de pages checkout custom |
| **Paiement** | Acquéreurs `payment_*` | ⏳ Non testé MOA systématiquement (`payment_demo` optionnel Lot 5) | **Préserver** — activer acquéreurs sans toucher Marketone |
| **Livraison** | `delivery` / transporteurs | ⏳ Standard Odoo checkout — non stylé spécifiquement | **Préserver** — pas de calcul livraison front custom |
| **Portail client** | `portal` — `/my`, commandes | ⏳ Dépendance manifest · pas de thème portal CK | **Préserver** — personnalisation portal = ticket séparé |
| **SEO** | `website.seo.metadata`, slugs, sitemap | 🟡 Champs natifs produits · portes query non canonicalisées · Culture pages website | **Préserver** champs natifs · ticket SEO portes |

### 5.1 Dépendances module — état cible proposé

```python
# Socle figé cadrage2 (inchangé)
"depends": [
    "portal",
    "website",
    "website_sale",
    "website_sale_wishlist",  # validé MOA UX-4 — standard Odoo
]

# Explicitement HORS depends Marketone (sauf ticket MOA)
# "website_blog"
# "website_forum"
# "website_sale_comparison"  # optionnel — ticket séparé
```

---

## 6. Checklist avant reprise d’un lot front gelé

Todo **obligatoire** en début de ticket front :

- [ ] Quelle fonctionnalité Odoo native est concernée ?
- [ ] Le lot **hérite-t-il** du template / contrôleur standard ?
- [ ] Le lot **bloque-t-il** une activation future (pricelist, promo, multi-variantes, paiement, livraison) ?
- [ ] Recette inclut-elle un scénario **« sans Marketone »** ou **« standard Odoo visible »** ?
- [ ] Aucune nouvelle dépendance `website_blog` / `website_forum` sans ADR ?

---

## 7. Décisions MOA à valider

| # | Question | Proposition Dev | Choix MOA |
|---|----------|-----------------|-----------|
| **D1** | `website_blog` requis au socle CK ? | **Non** — Culture / Savoirs hors blog | ☑ Validé MOA |
| **D2** | `website_forum` requis au socle CK ? | **Non** — Savoirs modérés sans forum | ☑ Validé MOA |
| **D3** | Personnalisation front = compatible natif Odoo (règles F1–F9) ? | **Oui** — opposable aux futurs lots | ☑ Validé MOA |
| **D4** | Matrice §5 = liste de préservation explicite ? | **Oui** — référence recette boutique | ☑ Validé MOA |
| **D5** | Reprise lots front gelés autorisée après validation D1–D4 ? | **Oui**, lot par lot + non-régression | ☑ Validé MOA |

---

## 8. Prochaines étapes proposées

| Priorité | Action | Owner |
|----------|--------|-------|
| 1 | ~~**Validation MOA** de ce document (D1–D5)~~ | MOA ✓ |
| 2 | ~~Enregistrer **ADR-034**~~ | Dev ✓ |
| 3 | ~~Mettre à jour README cadrage2~~ | Dev ✓ |
| 4 | Backlog [`TICKET_MARKETONE_TEST_T5_IMPORT_JPEG_PILOTE.md`](../tickets/maintenance/TICKET_MARKETONE_TEST_T5_IMPORT_JPEG_PILOTE.md) | Dev ✓ ouvert |
| 5 | Ticket SEO portes `/shop` (canonical / noindex) | MOA / Dev |
| 6 | ~~Ticket Lot 6.3 **promo / pack**~~ — cadrage ouvert [`TICKET_LOT6_3_PORTE_PROMO_PACK.md`](./TICKET_LOT6_3_PORTE_PROMO_PACK.md) | Dev ✓ ouvert |
| 7 | GO cadrage MOA Lot 6.3 (M1–M7) ~~puis exécution~~ | MOA ✓ · Dev ✓ cadrage |
| 8 | ~~**Exécution Lot 6.3a Promo**~~ — [`TICKET_MARKETONE_LOT6_3A_PORTE_PROMO_EXEC.md`](../tickets/lots/TICKET_MARKETONE_LOT6_3A_PORTE_PROMO_EXEC.md) · [`RECEPTION_MOA_LOT6_3A_PROMO.md`](./RECEPTION_MOA_LOT6_3A_PROMO.md) | Dev ✓ · MOA ✓ clôture |
| 9 | ~~**Cadrage Lot 6.3b Kits & Coffrets**~~ — [`DECISION_MOA_LOT6_3B_KITS_COFFRETS.md`](./DECISION_MOA_LOT6_3B_KITS_COFFRETS.md) · GO avec réserves | MOA ✓ · Dev ✓ |
| 10 | ~~**Exécution Lot 6.3b**~~ — [`TICKET_MARKETONE_LOT6_3B_PORTE_PACK_EXEC.md`](../tickets/lots/TICKET_MARKETONE_LOT6_3B_PORTE_PACK_EXEC.md) · [`RECEPTION_MOA_LOT6_3B_PACK.md`](./RECEPTION_MOA_LOT6_3B_PACK.md) | Dev ✓ · MOA ✓ clôture |
| 11 | Port OCA `sale_product_pack` — [`TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md`](../tickets/maintenance/TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md) | Dev · reporté |
| 12 | Reprise autres lots front — [`REPRISE_LOTS_FRONT_CADRAGE2.md`](./REPRISE_LOTS_FRONT_CADRAGE2.md) | Dev |

---

## 9. Documents liés

| Document | Rôle |
|----------|------|
| [`DECISION_MOA_RECADRAGE_BO.md`](./DECISION_MOA_RECADRAGE_BO.md) | Clôture lot BO |
| [`RETOUR_EXPERT_RECADRAGE.md`](./RETOUR_EXPERT_RECADRAGE.md) | Analyse initiale |
| [`../cadrage/NOTE_UNIVERS_CK_MARKETONE.md`](../cadrage/NOTE_UNIVERS_CK_MARKETONE.md) | Trois univers |
| [`../cadrage/CONTRACTS.md`](../cadrage/CONTRACTS.md) | Contrats C1–C8 |
| [`../cadrage/DECISIONS.md`](../cadrage/DECISIONS.md) | ADR existantes |
| [`../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md) | Anti-régression `/shop` |
| [`TICKET_LOT6_3_PORTE_PROMO_PACK.md`](./TICKET_LOT6_3_PORTE_PROMO_PACK.md) | Cadrage Lot 6.3 — **GO MOA** |
| [`../tickets/lots/TICKET_MARKETONE_LOT6_3A_PORTE_PROMO_EXEC.md`](../tickets/lots/TICKET_MARKETONE_LOT6_3A_PORTE_PROMO_EXEC.md) | Exécution Lot 6.3a Promo — **GO clôture MOA** |
| [`TICKET_LOT6_3B_PORTE_KITS_COFFRETS.md`](./TICKET_LOT6_3B_PORTE_KITS_COFFRETS.md) | Cadrage Lot 6.3b — **GO MOA avec réserves** |
| [`DECISION_MOA_LOT6_3B_KITS_COFFRETS.md`](./DECISION_MOA_LOT6_3B_KITS_COFFRETS.md) | Décision MOA — GO cadrage avec réserves |
| [`../tickets/lots/TICKET_MARKETONE_LOT6_3B_PORTE_PACK_EXEC.md`](../tickets/lots/TICKET_MARKETONE_LOT6_3B_PORTE_PACK_EXEC.md) | Exécution 6.3b — **GO clôture MOA** |
| [`RECEPTION_MOA_LOT6_3B_PACK.md`](./RECEPTION_MOA_LOT6_3B_PACK.md) | Clôture MOA Lot 6.3b |
| [`../cadrage/DECISIONS.md`](../cadrage/DECISIONS.md#adr-035--activation-product_pack-lot-63b-kits--coffrets) | ADR-035 — **acceptée MOA** |
| [`RECEPTION_MOA_LOT6_3A_PROMO.md`](./RECEPTION_MOA_LOT6_3A_PROMO.md) | Clôture MOA Lot 6.3a |
| [`../recette/lots/RECETTE_MANUELLE_LOT6_3A_PROMO.md`](../recette/lots/RECETTE_MANUELLE_LOT6_3A_PROMO.md) | Recette Lot 6.3a |

---

## Verdict MOA (à compléter)

| Date | Verdict | Commentaire |
|------|---------|-------------|
| 2026-06-08 | ☑ Validé · ☐ Validé avec réserves · ☐ À retravailler | D1–D5 validés · doctrine « Odoo exécute. Marketone habille et oriente. » · ADR-034 |
