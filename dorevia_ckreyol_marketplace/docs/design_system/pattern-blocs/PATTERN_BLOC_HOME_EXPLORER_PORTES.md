# Pattern-bloc — Home « Explorer / Par où commencer »

Ce document décrit le bloc **Explorer** de la homepage C-Kreyol comme **pattern d’orientation** vers les portes catalogue CK. Il privilégie la **logique produit** (parcours visiteur, doctrine URL) au-delà du seul rendu décoratif.

Ce n’est pas un ticket d’implémentation : cette passe **ne prescribed pas** de refonte shop, ni l’ajout d’un **snippet Odoo déposable** dans l’éditeur Website.

**Références** :

- Doctrine URL : [`docs/mvp_04/CANON_URL_BOUTIQUE.md`](../../mvp_04/CANON_URL_BOUTIQUE.md)
- Vocabulaire pattern-bloc : [`../README.md`](../README.md)

---

## 1. Intention produit

Le bloc doit :

- **Aider à entrer dans l’offre** sans imposer une liste catalogue « brute » comme première lecture après le hero ;
- **Distribuer les principales intentions d’exploration** CK (offres, coffrets, familles de produits, sélections éditoriales, territoires) sous forme de **portes lisibles** ;
- **Relier explicitement la Home au conteneur catalogue `/shop`** : les clics résolvent sur `/shop` enrichi des paramètres fonctionnels CK (`ckr_*`, modes d’exploration), conformément au canon boutique.

Ce module complète le hero (promesse globale) en offrant une **carte cognitive** du catalogue : où cliquer selon ce que le visiteur veut faire.

---

## 2. Portes concernées

### Lecture fonctionnelle (familles de portes)

Les familles suivantes couvrent l’intention métier :

| Famille | Rôle pour le visiteur |
| --- | --- |
| **Boutique / tout voir** | Accès au conteneur catalogue général lorsqu’on veut parcourir sans filtre thématique préalable |
| **Promotions** | Offres et prix attractifs |
| **Collections** | Sélections éditoriales (coups de cœur, saison, thématiques) |
| **Kits / packs** | Coffrets, assortiments, « prêts à offrir / à découvrir » |
| **Catégories** | Entrée par **familles produit** (navigation par type) |
| **Origines** | Entrée par **territoires / savoir-faire** |
| **Incontournables** | Mise en avant produits phares (« featured »), si la doctrine commerciale le retient |

### Implémentation actuelle de référence (`views/snippets/ckr_entries.xml`)

À la date de ce document, la section « Par où commencer » expose **cinq portes** en grille :

| Libellé carte | Cible `href` | Commentaire |
| --- | --- | --- |
| Promotions | `/shop?ckr_mode=promo` | Aligné canon (alias marketing `/promotions` → 301 vers équivalent query, voir tests module) |
| Kits | `/shop?ckr_mode=pack` | Même logique pour `/kits` → canon `ckr_mode=pack` |
| Catégories | `/shop` | Entrée générale catalogue sans paramètre CK : sert de porte **parcours par familles** côté UX (le détail filtre catégorie reste le canon `ckr_category` sur `/shop` quand on choisit une catégorie) |
| Collections | `/shop?ckr_collection_scope=all` | Porte « toutes les collections » cohérente avec la doctrine conteneur catalogue (éviter les anciennes routes nobles comme destination éditoriale finale) |
| Origines | `/shop?ckr_mode=origin` | Canon modes origines ; slug précis via `ckr_origin=` une fois dans le contexte shop |

**Pas de carte dédiée dans ce bloc** :

- **« Boutique / tout voir »** comme libellé distinct : l’intention est partiellement couverte par **Catégories → `/shop`** et par d’autres CTA (ex. hero). Si le MOA souhaite une **sixième porte** explicitement « Toute la boutique », ce serait une **évolution** à trancher hors refonte imposée par ce pattern-bloc.
- **Incontournables** : la route marketing historique et le mode `ckr_mode=featured` existent côté projet (redirections tests) ; **la carte n’est pas présente** dans `ckr_entries.xml` actuellement — à ajouter uniquement si stratégie et recette le valident.

---

## 3. Structure attendue

- **Ancre de section** : ex. `id="explorer-catalogue"` (liens internes, accessibilité au saut de contenu).
- **En-tête de section** (`ckr-section-title`) :
  - **sur-titre** (eyebrow) : ex. « Explorer » ;
  - **titre** : ex. « Par où commencer » ;
  - **intro courte** : ligne d’orientation (éviter une longue prose).
- **Grille de portes** : chaque porte est un **lien entier** (`<a>`) englobant média + corps (meilleure zone tactile que le seul libellé).
- **Par porte** :
  - **titre** (`<h3>`) clair ;
  - **texte d’aide** optionnel mais recommandé une ligne ;
  - **indicateur de suite** (ex. flèche / « Voir … ») pour la lisibilité conversion ;
  - **visuel** décoratif : image module ; `alt` vide sur image si le texte du lien porte le sens (pattern actuel : `aria-hidden` sur média + texte dans la carte).
- **Sémantique** : conteneur navigation avec `role="navigation"` et `aria-label` explicite pour regrouper les portes.

Référence visuelle et commentaires d’assemblage MVP : en-tête du fichier QWeb `ckr_entries.xml`.

---

## 4. Doctrine URL

Règles à respecter lors de toute évolution des liens :

1. **Conteneur canon** : **`/shop`** pour tout ce qui relève du catalogue CK filtrable.
2. **Paramètres CK** : préférer les query params documentés (`ckr_mode`, `ckr_collection`, `ckr_collection_scope`, `ckr_category`, `ckr_origin`, etc.) comme dans [`CANON_URL_BOUTIQUE.md`](../../mvp_04/CANON_URL_BOUTIQUE.md) et les contrôleurs associés.
3. **Anciennes URLs marketing** (`/promotions`, `/kits`, `/collections`, `/origines`, …) : utilisables **uniquement** si elles **redirigent proprement** (301) vers le canon — pour le bloc Explorer, les liens directs vers **`/shop?...`** sont préférés pour **stabilité analytics** et pour ne pas dépendre du schéma de redirection.
4. **Ne pas réintroduire** de doctrine obsolète (routes nobles comme destination finale, canon catégorie ambigu, etc.) — se référer au document canon et aux tests HTTP du module pour les attentes de redirection.

Les `href` présents dans **`ckr_entries.xml`** sont conformes à l’esprit **conteneur unique + query** pour les portes concernées.

---

## 5. Règles responsive

Implémentation SCSS : `static/src/scss/components/_entries.scss`.

- **Mobile** : grille **une colonne**, cartes empilées — lecture verticale rapide, zones tactiles hautes (carte complète cliquable).
- **Tablette** : grille asymétrique avec **promotions** et **kits** en pleine largeur relative, tuiles plus petites en dessous selon breakpoints.
- **Desktop** : grille **12 colonnes** — **Promotions** très visible (8 cols), **Kits** secondaire fort (4 cols) sur la même ligne ; rangée suivante pour **Catégories**, **Collections**, **Origines** (4+4+4). Cela instaure une **hiérarchie** entre mises en avant commerciales et portes « structure ».
- À éviter en recette : surcharge visuelle type **mosaïque dense** sans relief, ou trop de portes **sans différenciation** de poids.

---

## 6. GO / NO GO

### GO

- Le visiteur comprend **en quelques secondes** « par où commencer » sans lire tout le site.
- Les liens ouvrent les **bonnes intentions** sur `/shop` et restent **alignés** avec `CANON_URL_BOUTIQUE.md`.
- Le bloc reste **compact** sur mobile : empilement lisible, peu de friction.
- Cohérence avec le **header N2** et la Home (pas de double discours contradictoire sur les entrées majeures sans raison).

### NO GO

- Liens **obsolètes** ou **contradictoires** avec le canon `/shop` documenté.
- Bloc surtout **illustratif** sans valeur d’orientation (texte vide, intitulés génériques sans cible claire).
- **Trop de portes** au même niveau sans hiérarchie (saturation cognitive).
- Rendu mobile **trop long** (trop de cartes, trop de texte) ou ordre **illisible**.

---

## 7. Points de vigilance

- **Distinction Home Explorer vs `/shop`** : ce pattern est un **tableau d’orientation rédactionnel** sur la Home. Les **filtres, chips et états de liste** sur `/shop` sont un autre sous-système UX : ne pas les confondre dans la doc ni dupliquer leur logique sans besoin.
- **Vérifier les `href` dans le template** à chaque évolution de canon ou de contrôleur ; faire suivre les **tests HTTP** du module si les URL changent.
- **Ne pas rouvrir une refonte globale du shop** sous prétexte de ce bloc : les ajustements attendus ici sont **surgicals** (copy, ordre des portes, hiérarchie, liens).
- **Pas de snippet Odoo déposable** dans cette passe documentaire : si un jour le bloc devient éditorial, ce sera une **décision séparée** (enregistrement Website, données structurées, gouvernance contenu).
- **Cohérence visuelle** : les assets `explorer_porte_*.png` doivent rester alignés avec les **références créa** versionnées (`docs/assets/` / README module) pour limiter la dérive hors charte.

---

## Statut du document

**Créé** — décrit le comportement et l’intention du bloc **tel qu’implémenté** dans `ckr_entries.xml`, avec distinction explicite entre **portes présentes** et **portes absentes** ou **à ajouter** (ex. Incontournables, « Toute la boutique »).
