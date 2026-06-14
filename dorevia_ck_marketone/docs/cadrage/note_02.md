# note_02 — Open Design comme référence UX pour la maquette CK

| Champ | Valeur |
|-------|--------|
| **Suite de** | [`note_01.md`](./note_01.md) |
| **Date** | 2026-06-12 |
| **Statut** | Retour développeur de référence — analyse Open Design local |
| **Dépôt Open Design** | `/Users/doreviateam/open-design` (instance locale) |
| **Décision sur l'existant** | **Non tranchée** — `dorevia_ckreyol_marketone` reste matière d'analyse |

---

## 1. Objet de cette note

Cette note précise le rôle d'**Open Design** dans le projet `dorevia_ck_marketone`, dans le cadre de la doctrine MOA :

```text
Odoo = source de vérité métier
Open Design = référence UX
Maquette = pont entre UX et Odoo
Thème Odoo = première implémentation maîtrisée
```

L'intention n'est **pas** de remplacer Odoo ni de repartir dans une application front autonome.

Phrase doctrine :

> Open Design produit la cible visuelle ; Odoo produit le comportement ; le thème est la première traduction maîtrisée.

---

## 2. Comment lire Open Design (dépôt local)

Open Design n'est **pas** une bibliothèque de composants importables dans Odoo (pas de package React/Odoo à brancher). C'est un **atelier de prototypage** et un **référentiel de design** :

| Couche | Emplacement | Rôle pour CK |
|--------|-------------|--------------|
| Design systems | `design-systems/*/DESIGN.md` | Règles opposables : couleurs, typo, composants, grille, do/don't |
| Skills | `skills/*/SKILL.md` | Méthode pour produire et critiquer des artefacts HTML |
| Projets | `.od/projects/` | Maquettes HTML exportables (HTML / PDF / ZIP) |
| Mémoire projet | `.od/memory/project_c_kreyol_*.md` | Doctrine CK injectée aux sessions de design |

### Éléments CK déjà présents dans l'instance locale

| Élément | Chemin |
|---------|--------|
| Doctrine 3 univers | `.od/memory/project_c_kreyol_marketone.md` |
| Direction « marché créole contemporain » | `.od/memory/project_c_kreyol_design_direction.md` |
| Alignement premium Odoo | `.od/memory/project_c_kreyol_premium_odoo.md` |
| Audience maquette | `.od/memory/project_c_kreyol_prototype_audience.md` |
| Prototype HTML CK | `.od/projects/44de8203-38b0-4405-af76-2f09c97c5f02/index.html` |
| Critique auto (4/5) | `.od/projects/44de8203-…/critique.json` |

### Chaîne de travail retenue

```text
DESIGN.md CK (+ mémoire Open Design)
    → artefact HTML maquette cible
        → tokens SCSS + structure QWeb de référence
            → module dorevia_ck_theme
                → données et flux = Odoo natif (website_sale)
```

---

## 3. Ce qu'Open Design peut réellement apporter pour la maquette CK

### Apports concrets

**a) Accélérer la production de la maquette cible `/shop`**

Les skills `frontend-design`, `design-md` et `design-review`, ainsi que la boucle de critique en cinq axes, permettent d'itérer rapidement sur la hiérarchie, la grille, les cartes produit, la sidebar, le responsive et les états interactifs — **sans toucher Odoo**.

**b) Fournir un référentiel visuel opposable**

Le design system `warm-editorial` (`design-systems/warm-editorial/DESIGN.md`) est le meilleur point de départ du catalogue pour CK : terracotta, papier chaud, serif + sans, pas de dégradés, retenue éditoriale. Il est proche de la ligne premium Odoo déjà actée en mémoire CK.

**c) Formaliser la direction CK dans un `DESIGN.md` dédié**

Il n'existe pas encore de `design-systems/c-kreyol-marketone/`. Le créer verrouillerait palette MOA, typo Garamond/Hanken, règles anti-exotisme et grilles boutique comme **source UX unique** avant traduction Odoo.

**d) S'appuyer sur un prototype déjà amorcé**

Le `index.html` CK couvre déjà : accueil, boutique (sidebar + grille), fiche produit, culture, panier/checkout en mise en page statique. C'est une base de discussion AMOA, **pas** une spécification technique Odoo.

### Ce qu'Open Design ne fait pas

- Ne se connecte pas à Odoo
- Ne gère pas catalogue, prix, stock ni panier réel
- Ne remplace pas `website_sale`, les snippets Website Builder ni la recette MOA

---

## 4. Composants et patterns UX repris ou adaptables

### Reprenables quasi tels quels (visuel + structure)

| Pattern (prototype CK) | Traduction Odoo visée |
|------------------------|----------------------|
| Topbar sticky, logo, nav 3 univers, recherche, icône panier | Layout `website.layout` + header QWeb |
| Section-head (kicker + titre + sous-texte éditorial) | Bloc éditorial `/shop` ou snippet |
| Shop layout sidebar + zone principale | Grille Bootstrap / layout Odoo |
| Filter groups (légende + cases) | **Apparence** des filtres ; données = catégories Odoo, attributs, collections si validées |
| Product card (media, meta origine/catégorie, titre, micro-récit, prix, CTA) | Tuile `website_sale` — structure HTML/CSS |
| Shop toolbar (filtres actifs + tri) | Rendu visuel ; tri = mécanisme Odoo |
| Buy box fiche produit (prix, quantité, CTA, réassurance) | Héritage template produit Odoo |
| Culture strip (cartes origine) | Pages éditoriales / snippets — pas moteur catalogue |
| Tokens CSS (`:root` couleurs, radius, ombres) | Fichiers SCSS du thème |

### À adapter (écarts identifiés)

| Prototype OD actuel | Action attendue |
|---------------------|-----------------|
| Accent vert + dégradés produit | Réaligner sur mémoire premium + `warm-editorial` |
| Filtres en checkboxes JS locales | Conserver en maquette ; en Odoo = liens / query params `website_sale` |
| Filtre **Prix** absent de la sidebar prototype | Ajouter en maquette si MOA le confirme (widget pricelist Odoo) |
| Compteur panier simulé en JS | Démo UX uniquement ; Odoo = `sale_get_order()` |
| Polices système (Avenir, SF Pro) | Remplacer par EB Garamond + Hanken Grotesk |

### Design systems du catalogue utiles comme inspiration (pas copie)

- **`warm-editorial`** — ligne CK premium
- **`airbnb` / `nike`** — grilles retail, anatomie des cartes produit
- **À éviter pour CK : `shopify`** — esthétique dark/neon incompatible avec la doctrine artisanale

---

## 5. Ce qui reste strictement visuel / thème

Tout ce qui **ne change pas le comportement métier** si on retire le module thème :

```text
Tokens SCSS
  couleurs, typographies, espacements, radius, ombres, bordures

Chrome global
  header, footer, navigation, boutons, badges visuels, chips, liens

Habillage composants
  .product-card, .filter-group, .btn-primary, .origin-chip
  (classes CSS sur le markup Odoo existant)

Snippets purement décoratifs
  bandeaux éditoriaux, séparateurs, blocs Culture statiques

Assets
  logos, icônes, polices web
```

Règle pratique :

> Si c'est supprimable en ne retirant que `static/` et `assets.xml` sans casser l'ajout au panier, c'est du **thème**.

Le module `dorevia_ck_theme` devrait porter au minimum :

- tokens SCSS (`_tokens_*.scss`) ;
- surcharge header / footer ;
- styles des tuiles produit et de la sidebar ;
- snippets visuels CK réutilisables.

---

## 6. Ce qui bascule dans du template métier Odoo

Dès qu'un élément **lit ou écrit la vérité Odoo**, c'est du template métier (QWeb + héritages), pas du thème seul :

| Élément maquette | Couche Odoo |
|------------------|-------------|
| Grille produits, prix affiché | Templates `website_sale` + pricelist |
| Filtres catégories | `product.public.category` + URLs `/shop` |
| Filtre origine | Attribut produit Odoo ou modèle dédié — **décision métier** |
| Filtre collections | Entité métier + vue, ou tag/attribut Odoo natif |
| Filtre prix | Widget pricelist / domaine Odoo |
| Ajout panier, wishlist | Contrôleurs `website_sale` |
| Fiche produit (variantes, stock) | Templates produit Odoo |
| Panier / checkout | `website_sale` — ne pas re-maquetter en parallèle |
| Portes boutique (`/shop?…`) | Routage + domaine — template métier |
| Tri, pagination, état vide | Logique `website_sale` + QWeb conditionnel |

Frontière clé :

```text
Thème     = à quoi ça ressemble
Template  = quelles données Odoo, quels liens, quels champs
```

Exemple sidebar « Collections » :

- **Visuel** (titres, espacements, accordéon) → thème ;
- **Liste des collections cliquables** → template métier branché sur un modèle ou champ Odoo.

---

## 7. Ce qui risque de recréer une couche applicative autonome

### Signaux d'alerte (ligne rouge)

| Risque | Symptôme | Pourquoi c'est interdit |
|--------|----------|-------------------------|
| Catalogue client | JS qui filtre des produits hors requête Odoo | Catalogue parallèle |
| Panier simulé | État panier en `localStorage` / compteur custom | Checkout parallèle |
| Données produit dans le HTML | Prix, stock, SKU en dur dans l'artefact | Prix / stock hors Odoo |
| Module « Marketone » fourre-tout | Modèles, contrôleurs, routes pour ce qu'Odoo fait déjà | ERP bis |
| App React / Vue embarquée | Skill `web-artifacts-builder`, SPA dans Odoo | Front autonome |
| API custom boutique | Endpoints JSON catalogue / panier | Couche de dépendance |
| Multiplication d'apps | `theme` + `shop` + `collections` + `origins` indépendants | Dette de gouvernance |

### Dans le prototype Open Design actuel

Le JavaScript de démo (compteur panier fictif, filtres locaux) est **sain en maquette** et **dangereux** s'il est traité comme spécification fonctionnelle Odoo.

```text
Maquette OD  →  démonstration UX
Odoo         →  website_sale + QWeb + données réelles
```

### Dans l'existant `dorevia_ckreyol_marketone` (matière d'analyse)

Éléments qui dépassent un thème pur et devront être arbitrés **après** validation de la maquette cible :

- `marketone.shop.collection` (modèle dédié) ;
- `marketone.shop.origin` (modèle dédié) ;
- extensions `product.template`, `website`, `product.public.category` ;
- vues QWeb shop / cart / checkout nombreuses.

Ce n'est pas automatiquement « mauvais » : c'est de la couche de présentation branchée Odoo. Cela devient problématique si ces éléments **dupliquent** catalogue, prix ou stock, ou imposent une logique qu'`website_sale` ne peut pas porter nativement.

---

## 8. Tension identifiée : mémoire CK vs prototype actuel

La mémoire Open Design impose l'alignement sur la ligne premium Odoo déjà validée :

```text
terracotta #C4715A · sauge #5A8A6E · crème
EB Garamond + Hanken Grotesk
pas de palette verte type marketplace startup
pas de dégradés décoratifs
```

Le prototype HTML actuel part sur une autre direction (accent vert OKLch, dégradés sur visuels produit, polices système).

Décision attendue :

> La maquette cible AMOA doit être alignée sur la mémoire premium Odoo, pas sur l'exploration visuelle du premier artefact.

---

## 9. Actions recommandées avant de trancher sur l'existant

```text
1. Créer design-systems/c-kreyol-marketone/DESIGN.md
   (fusion mémoire OD premium + tokens Odoo + warm-editorial)

2. Refaire ou corriger le prototype CK dans Open Design
   (palette MOA, retirer dégradés, ajouter filtre Prix si validé)

3. Valider AMOA la maquette comme référence UX officielle
   (pas le code HTML brut)

4. Rédiger une grille de traduction maquette → thème vs template métier
   (une page par écran : /shop, fiche, panier, checkout)

5. Ensuite seulement : décider du sort de dorevia_ckreyol_marketone
   (prolonger, simplifier, extraire le visuel, ou analyser écran par écran)
```

### Ce qu'il ne faut pas faire

```text
Poursuivre le prototype vert actuel comme référence officielle
Utiliser web-artifacts-builder / React pour la boutique Odoo
Lancer dorevia_ck_theme sans maquette CK validée et sans DESIGN.md dédié
Copier le HTML Open Design en module Odoo autonome
```

---

## 10. Position sur la suite du projet

La doctrine de `note_01` est **cohérente** avec Open Design, à condition de respecter la chaîne :

```text
Open Design  →  maquette cible validée AMOA
Maquette     →  tokens + grilles de référence
Thème Odoo   →  première implémentation maîtrisée
Odoo         →  comportement et vérité métier
```

Il est possible de repartir sur une trajectoire plus simple **sans abandonner l'investissement passé**, en traitant `dorevia_ckreyol_marketone` comme matière d'analyse le temps de :

1. figer la maquette CK dans Open Design (alignée premium) ;
2. implémenter d'abord un thème Odoo maîtrisé (`dorevia_ck_theme`) ;
3. n'ajouter du template métier **que là où Odoo standard + thème ne suffisent pas**, avec critère écrit et validé MOA.

---

## 11. Phrase de synthèse

> Open Design sert à produire et valider la maquette cible CK ; le thème Odoo en est la première traduction visuelle ; Odoo reste seul maître du catalogue, du panier et du checkout. L'existant `dorevia_ckreyol_marketone` n'est pas prolongé automatiquement : il sera arbitré écran par écran une fois la maquette et la grille de traduction validées.
