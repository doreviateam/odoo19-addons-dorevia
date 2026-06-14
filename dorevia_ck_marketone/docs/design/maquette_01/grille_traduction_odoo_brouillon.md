# Grille de traduction Odoo — brouillon MOA

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Statut** | Brouillon — remplacé par [`grille_traduction_odoo_v1.md`](./grille_traduction_odoo_v1.md) |
| **Références** | `design_01.md` v1.1 · Maquette V1.1 · `revue_dev_traduisibilite_odoo.md` · `recette_qa_maquette_01.md` |
| **Verrou Odoo** | **Maintenu** — aucun code tant que David ne lève pas explicitement le verrou |
| **Date** | 2026-06-12 |

---

## 1. Objet de la grille

Ce document traduit la **maquette CK V1.1** en décisions d’implémentation Odoo futures :

```text
Thème        → dorevia_ck_theme (visuel, layout, tokens)
Template     → website_sale / website natif (comportement, données)
Extension    → uniquement si Odoo standard + thème insuffisent (arbitrage MOA)
Interdit     → front autonome, catalogue/panier/checkout parallèles
```

**Nature du document** : grille d’analyse et d’arbitrage pour David / MOA — **pas** un ordre de développement.

---

## 2. Doctrine MOA confirmée

```text
Odoo = source de vérité métier
website_sale = moteur boutique B2C phase 1
Maquette V1.1 = référence UX validée (QA + revue Dev favorable avec réserves)
dorevia_ckreyol_marketone = mémoire d’analyse, pas reprise automatique
```

### Répartition cible phase 1 (validée MOA)

| Couche | Part estimée | Rôle |
|--------|--------------|------|
| Thème `dorevia_ck_theme` | ~55 % | Identité, tokens, header/footer, tuiles, sidebar visuelle, responsive |
| Templates natifs Odoo | ~35 % | `/shop`, fiche, tri, pagination, buy box, recherche |
| Extensions | ~10 % max | Origines, collections, filtre prix — **si** arbitrage MOA |
| Front autonome | 0 % | Interdit |

### Décision MOA intégrée — catégories

```text
Catégories e-commerce phase 1 → product.public.category hiérarchiques
```

Arborescence cible (maquette V1.1) :

```text
Boutique
├── Épicerie créole
│   ├── Farines
│   ├── Galettes
│   ├── Biscuits
│   ├── Confitures
│   ├── Sauces & piments
│   └── Épices & condiments
├── Boissons
│   ├── Jus & nectars
│   ├── Sirops
│   └── Infusions
├── Coffrets & packs
│   ├── Découverte
│   ├── Cadeaux
│   └── Professionnels
└── Maison & bien-être
    ├── Savons artisanaux
    ├── Huiles
    └── Soins naturels
```

---

## 3. Dimension brick & mortar (complément MOA)

CK soutient **deux dimensions** :

```text
1. Valoriser les producteurs / transformateurs créoles.
2. Soutenir les distributeurs physiques qui référencent, achètent et revendent ces produits.
```

**CK ne court-circuite pas les distributeurs physiques.**

Distributeurs visés (brick & mortar) :

- boutiques physiques ;
- épiceries fines ;
- concept stores ;
- restaurants ;
- hôtels ;
- revendeurs spécialisés ;
- points de vente locaux ou européens.

L’entrée « Pro » ne se limite **pas** à « achat en volume ». Elle couvre aussi :

- demande de **référencement** ;
- **approvisionnement** de point de vente ;
- relation **revendeur / distributeur** ;
- **qualification** du type de professionnel ;
- soutien à la **distribution physique**.

Intentions UX à porter (phase 1 — signal, pas portail) :

```text
Vous êtes distributeur, restaurateur ou boutique spécialisée ?
Référencer des produits créoles dans votre point de vente.
Approvisionnement pour boutiques, restaurants, hôtels et revendeurs.
Demander un accès professionnel.
```

---

## 4. Grille par zone — Accueil

| Zone maquette | Couche | Traduction Odoo probable | Phase 1 | Arbitrage / note |
|---------------|--------|--------------------------|---------|------------------|
| Header (logo, nav, recherche, panier) | Thème + template | `website.layout` | Thème + natif | Panier = `sale_get_order()` |
| Hero promesse + CTA boutique | Thème / snippet | Snippet Website ou QWeb bloc | Thème | — |
| CTA / signal **Professionnels** | Thème / snippet + page | Lien vers page « Accès pro » | Template + contenu | Voir §5 brick & mortar |
| Pills univers (4 familles) | Template + thème | Liens `product.public.category` parentes | **Natif** | MOA validé |
| Produits vedettes | Snippet + thème | Snippet manuel ou produits `is_published` sélectionnés | Thème / template léger | Dynamique = option phase 2 |
| Bandeau réassurance | Thème / snippet | Snippet statique | Thème | — |
| Tokens (couleurs, typo, espacements) | Thème | SCSS `dorevia_ck_theme` | Thème | Typo prod à arbitrer |

**Verdict accueil** : implémentable en **thème + snippets + catégories natives** — pas d’extension requise.

---

## 5. Grille par zone — Entrée pro & brick & mortar

| Zone | Couche | Traduction Odoo probable | Phase 1 | Arbitrage requis |
|------|--------|--------------------------|---------|------------------|
| Lien header « Professionnels » | Thème + contenu | Page CMS `/professionnels` ou équivalent | Signal | **CMS vs `website_crm`** |
| Bandeau `/shop` revendeur | Snippet + thème | Bloc éditorial réutilisable | Signal | Reformuler texte brick & mortar |
| CTA « Demander un accès pro » | Template + CRM | Formulaire contact ou `website_crm` lead | Signal | Voir formulaire ci-dessous |
| Page intention pro (contenu) | CMS | Page Website expliquant référencement + approvisionnement | Contenu | Rédaction MOA |
| Formulaire pro | Template + CRM | `website.form` ou formulaire CRM Odoo | Signal | **À trancher** |
| Portail revendeur | — | — | **Hors phase 1** | Interdit phase 1 |
| Listes de prix B2B dynamiques | — | `product.pricelist` + règles partenaire | **Hors phase 1** | Futur post-arbitrage |
| Prix masqués / devis en ligne | — | — | **Hors phase 1** | Futur |

### Formulaire pro — champs envisagés (phase 1 signal)

| Champ | Type | Usage |
|-------|------|-------|
| Type de professionnel | Sélection | Boutique, restaurant, hôtel, épicerie fine, distributeur, autre |
| Nom de l’établissement | Texte | Qualification lead |
| Pays / zone de distribution | Texte / sélection | Brick & mortar géographique |
| Type de point de vente | Sélection | Physique, mixte, autre |
| Besoin principal | Sélection multiple | Référencement · Approvisionnement · Commande récurrente · Contact commercial |
| Message libre | Texte | Complément |
| Coordonnées contact | Email, tél. | Standard CRM |

### CRM / contacts — besoin futur (annotation, pas phase 1)

```text
Qualification contact B2B dans res.partner / crm.lead
Type partenaire : boutique, restaurant, hôtel, distributeur, revendeur
Rattachement pricelist B2B ultérieur
Pas de workflow commercial complet en phase 1
```

**Recommandation Dev (non décision)** : phase 1 = **page CMS + formulaire `website_crm`** — suffisant pour brick & mortar signal sans portail.

---

## 6. Grille par zone — Page `/shop`

| Zone maquette | Couche | Traduction Odoo probable | Phase 1 | Arbitrage requis |
|---------------|--------|--------------------------|---------|------------------|
| Titre + promesse boutique | Template + thème | Héritage `website_sale.products` | Natif + thème | — |
| Sidebar catégories (arborescence) | Template + thème | `product.public.category` hiérarchiques, liens `/shop/category/...` | **Natif** | MOA validé |
| Filtre origines | Template ou extension | **Option A** : `product.attribute` « Origine » | À trancher | **Attribut vs extension** |
| | | **Option B** : modèle dédié (ex. ancien Marketone) | Extension | Non reprise auto |
| Filtre collections | Template ou extension | **Option A** : catégories secondaires / tags | À trancher | **Tags/catégories vs modèle** |
| | | **Option B** : modèle `marketone.shop.collection` | Extension | Justification MOA |
| Filtre prix (fourchette) | Template ou extension | CE limité — catégories + pricelist ou extension | À trancher | **Conserver UI ou simplifier** |
| Tri toolbar | Template natif + thème | `?order=` `website_sale` | Natif | — |
| Grille produits | Template + thème | Tuiles `website_sale` | Natif + thème | — |
| Carte produit (image, prix, chips) | Thème + template | SCSS + QWeb tuile | Thème | — |
| Action « Voir » | Template natif | Lien `/shop/product/...` | **Natif** | Quick-add non retenu |
| Badge pack | Template + thème | Produit pack = 1 fiche Odoo | Template | **Packs `non_detailed`** |
| Pagination | Template natif + thème | Pager `/shop/page/N` | Natif | — |
| État vide catalogue | Template | QWeb conditionnel | Natif | Non maquetté V1.1 |
| Drawer filtres mobile | Thème | CSS offcanvas + liens filtre URL | Thème | Pas filtre JS catalogue |
| Bandeau pro (bas `/shop`) | Snippet | Bloc brick & mortar | Signal | Texte MOA |

**Verdict `/shop`** : **socle natif suffisant** si origines = attribut et collections = catégories/tags. Extensions = points d’arbitrage §9.

---

## 7. Grille par zone — Fiche produit

| Zone maquette | Couche | Traduction Odoo probable | Phase 1 | Arbitrage requis |
|---------------|--------|--------------------------|---------|------------------|
| Fil d’Ariane | Template natif + thème | Standard `website_sale` | Natif | — |
| Galerie images | Template natif + thème | Images produit Odoo | Natif | — |
| Buy box (prix, qty, CTA) | Template natif + thème | Widget fiche standard | Natif | — |
| Chips origine / catégorie | Template + thème | Attribut + `public_categ_ids` | Natif à moyen | Lié arbitrage origines |
| Bloc usage éditorial | Template + thème | `description_sale` ou champ léger | Natif | — |
| Réassurance fiche | Thème / snippet | Bloc statique | Thème | — |
| Produits liés | Template natif + thème | `alternative_product_ids` | Natif | — |
| Pack (si produit pack) | Template + métier | 1 produit, 1 ligne panier si `non_detailed` | Template | **Doctrine packs** |

**Verdict fiche** : **100 % natif + thème** — aucune extension obligatoire phase 1.

---

## 8. Zones hors maquette V1.1 (référence future)

| Zone | Couche | Traduction Odoo | Phase |
|------|--------|-----------------|-------|
| Panier | Template natif | `website_sale` cart | Natif — hors maquette |
| Checkout | Template natif | `website_sale` checkout | Natif — hors maquette |
| Portail client | Template natif | `portal` + commandes | Natif — phase ultérieure |
| Portail B2B revendeur | Extension | Portail custom + pricelists | **Hors phase 1** |
| Listes de prix pro | Métier Odoo | `product.pricelist` par partenaire | **Hors phase 1** |
| Logistique / sourcing BO | Métier Odoo | `stock`, `purchase`, etc. | Hors scope maquette |

---

## 9. Tableau de synthèse — Thème / Template / Extension

| Composant | Thème | Template natif | Extension | Statut décision |
|-----------|:-----:|:--------------:|:---------:|-----------------|
| Tokens SCSS | ● | | | Palette V1 validée — typo prod à arbitrer |
| Header / footer | ● | ○ | | Thème majoritaire |
| Hero accueil | ● | ○ | | Snippet |
| Catégories hiérarchiques | ○ | ● | | **MOA validé** — `product.public.category` |
| Tuile produit + « Voir » | ● | ● | | Natif |
| Sidebar filtres (visuel) | ● | ○ | | Thème habillage |
| Filtre origines | ○ | ○ | ? | **À trancher** |
| Filtre collections | ○ | ○ | ? | **À trancher** |
| Filtre prix | ○ | | ? | **À trancher** — simplifier possible |
| Tri / pagination | ○ | ● | | Natif |
| Fiche produit complète | ● | ● | | Natif |
| Produits liés | ○ | ● | | Natif |
| Réassurance | ● | ○ | | Snippet |
| Entrée pro (liens + bandeaux) | ● | ○ | | Signal brick & mortar |
| Page + formulaire pro | ○ | ● | ○ | **CMS vs `website_crm`** |
| CRM qualification B2B | | | ○ | Futur — annotation seulement |
| Pricelists B2B | | | ○ | **Hors phase 1** |
| Portail B2B | | | | **Interdit phase 1** |
| Packs affichage | ○ | ● | ○ | **Doctrine `non_detailed`** |

Légende : ● = couche principale · ○ = contribution · ? = arbitrage MOA requis

---

## 10. Arbitrages MOA encore requis avant code

| # | Sujet | Options | Impact grille | Décision David |
|---|-------|---------|---------------|--------------|
| 1 | **Packs `non_detailed`** | 1 produit = 1 ligne panier vs autre | Badge pack, fiche, checkout | ☐ À trancher |
| 2 | **Origines** | `product.attribute` vs modèle dédié | Sidebar + chips | ☐ À trancher — Dev recommande attribut phase 1 |
| 3 | **Collections** | Catégories/tags vs modèle custom | Filtre sidebar | ☐ À trancher — Dev recommande catégories/tags phase 1 |
| 4 | **Filtre prix** | UI complète vs simplifiée vs report | Sidebar | ☐ À trancher |
| 5 | **Entrée pro** | Page CMS vs `website_crm` | §5 brick & mortar | ☐ À trancher |
| 6 | **Typo production** | Fraunces/DM Sans self-host vs autre | Thème | ☐ À trancher |
| 7 | **Texte brick & mortar** | Formulations finales page pro + bandeaux | Contenu CMS | ☐ À trancher |
| 8 | **Levée verrou Odoo** | GO base dev + `dorevia_ck_theme` | Projet entier | ☐ **Décision explicite David** |

---

## 11. Ce qui reste interdit

```text
Catalogue parallèle (JS local, API custom boutique)
Panier / checkout parallèles
Front React/Vue/SPA embarqué
Portail B2B complet phase 1
Prix pro dynamiques phase 1
Reprise automatique code dorevia_ckreyol_marketone
Développement Odoo sans levée explicite du verrou
```

---

## 12. Séquence recommandée après validation grille

```text
1. David valide ou corrige cette grille (arbitrages §10)
2. Mise à jour maquette ou textes pro si besoin (brick & mortar — optionnel)
3. Décision explicite levée verrou Odoo
4. Ticket dorevia_ck_theme — socle tokens + layout (pas extensions)
5. Base Odoo dev + paramétrage catégories product.public.category
6. Extensions seulement si arbitrages §10 l’exigent
7. CRM / pricelists B2B / portail — phases ultérieures
```

---

## 13. Phrase de synthèse MOA

> La maquette V1.1 se traduit d’abord en un thème Odoo maîtrisé et en templates `website_sale` natifs, avec des catégories hiérarchiques et une entrée pro qui soutient la distribution physique (brick & mortar) sans portail B2B en phase 1. Les extensions restent limitées et soumises à arbitrage ; le verrou Odoo demeure jusqu’à décision explicite de David.

---

## 14. Statut du brouillon

```text
Document : grille d’analyse — PAS ticket de développement
En attente : validation / corrections David
Verrou Odoo : MAINTENU
```
