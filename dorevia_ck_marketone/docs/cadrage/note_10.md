# NOTE DE SPEC DEV / QA — CK-CATALOG-ARCHI-001

## Gouvernance d'exposition des univers, catégories et cards produit CK

| Champ              | Valeur                                                                                                                                    |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Projet             | C-Kréyòl Marketone                                                                                                                        |
| Lot                | CK-CATALOG-ARCHI-001                                                                                                                      |
| Objet              | Gouvernance d'exposition des univers, catégories et cards produit                                                                         |
| Destinataires      | MOA, Produit, Architecture, Dev, QA                                                                                                       |
| Statut             | Version complète soumise Dev/QA — voir [`note_10_reponse.md`](note_10_reponse.md)                                                          |
| Référence contexte | Revue MOA / métier Home + Shop + catégories                                                                                               |
| Routes observées   | `/`, `/shop`, `/shop/category/epicerie-1`, `/shop/category/boissons-123`, `/shop/category/soin-bien-etre-2`, `/shop/category/artisanat-3` |

---

# 1. Contexte

Suite à la revue MOA / métier des pages suivantes :

* `/`
* `/shop`
* `/shop/category/epicerie-1`
* `/shop/category/boissons-123`
* `/shop/category/soin-bien-etre-2`
* `/shop/category/artisanat-3`

le site CK présente un socle technique globalement fonctionnel :

* les routes répondent ;
* la navigation catalogue dynamique est en place ;
* les pages boutique et catégories s'affichent ;
* la Home porte correctement la promesse de marque C-Kréyòl ;
* l'architecture multi-univers commence à apparaître dans l'expérience publique.

Cependant, la revue métier met en évidence un écart entre :

* l'architecture cible CK : une boutique multi-univers créole ;
* et la maturité réelle du catalogue actuellement exposé.

Le risque principal n'est pas technique mais commercial / UX :

> Certaines catégories ou univers sont visibles publiquement alors qu'ils ne semblent pas encore suffisamment riches, qualifiés ou cohérents pour convaincre un acheteur.

Cette note vise donc à cadrer une évolution d'architecture catalogue :

> **Dissocier l'existence technique d'une catégorie Odoo de son exposition publique dans l'expérience CK.**

---

# 2. Doctrine MOA validée

La doctrine à appliquer est la suivante :

> **L'arborescence Odoo structure le catalogue, mais l'exposition publique CK doit être pilotée par la maturité commerciale des univers.**

Autrement dit :

> **On ne montre pas une catégorie parce qu'elle existe ; on la montre parce qu'elle est prête à convaincre.**

Une catégorie ou un univers peut donc exister côté Odoo sans être automatiquement exposé dans :

* le header ;
* la Home ;
* le footer ;
* les blocs d'univers ;
* le SEO public ;
* les pages fortement mises en avant.

La V1 CK doit assumer une boutique encore limitée, mais elle ne doit jamais donner l'impression d'une boutique vide, incohérente ou prématurée.

---

# 3. Objectifs du lot

## 3.1 Objectifs fonctionnels

Ce lot vise à sécuriser l'architecture catalogue CK en V1.

Objectifs :

1. Éviter d'exposer publiquement des catégories vides ou trop pauvres.
2. Corriger les incohérences de catégorisation produit visibles.
3. Définir une règle claire de visibilité des univers CK.
4. Normaliser les informations affichées sur les cards produit.
5. Adapter la navigation Home / header / footer à la maturité réelle du catalogue.
6. Prévenir les pages SEO pauvres ou "thin content".
7. Garder l'ambition multi-univers CK sans donner une impression de catalogue vide.
8. Préserver le standard Odoo tout en ajoutant une couche d'exposition commerciale CK.
9. Rendre les règles testables côté QA.

## 3.2 Objectif métier

Faire percevoir CK comme une boutique :

* crédible ;
* claire ;
* qualitative ;
* cohérente ;
* commercialement assumée ;

même avec un catalogue encore limité.

## 3.3 Objectif architecture

Mettre en place une gouvernance claire entre :

* la publication technique Odoo ;
* l'intention MOA / marketing ;
* la qualification commerciale réelle ;
* l'exposition front ;
* le SEO.

---

# 4. Hors périmètre

Ne pas inclure dans ce lot :

* refonte graphique complète de la Home ;
* refonte complète de la page boutique ;
* nouveau moteur de filtres avancés complexe ;
* formulaire complet d'alerte email "m'avertir" ;
* système complet de précommandes ;
* création massive de sous-catégories sans contenu ;
* refonte checkout / panier ;
* refonte des fiches produit détaillées ;
* refonte des pages légales ;
* création de contenu éditorial définitif pour tous les univers.

Ce lot est un lot d'architecture catalogue et d'exposition publique, pas une refonte e-commerce globale.

---

# 5. Principes d'architecture

## 5.1 Séparer publication Odoo, exposition CK et qualification commerciale

Il faut distinguer trois notions.

| Niveau                                 | Rôle                                                                         |
| --------------------------------------- | ----------------------------------------------------------------------------- |
| `website_published`                    | Publication technique standard Odoo                                          |
| `ck_exposure_status`                   | Intention MOA / marketing d'exposition d'une catégorie                       |
| `ck_is_exposable` ou helper équivalent | Résultat calculé : la catégorie est-elle réellement exposable publiquement ? |

Le champ natif `website_published` ne doit pas être détourné.

Le champ `ck_exposure_status` exprime une intention CK.

La visibilité réelle en front doit cependant passer par une règle d'éligibilité commerciale, afin d'éviter qu'une catégorie vide ou incomplète soit exposée simplement parce qu'elle est marquée `active`.

Principe attendu :

```text
visible_en_navigation =
    website_published
    AND ck_exposure_status = active
    AND catégorie commercialement exploitable
```

Le Dev peut implémenter cette logique via :

* helper Python ;
* champ calculé ;
* méthode dédiée sur `product.public.category` ;
* service de navigation CK existant ;
* ou combinaison sobre compatible avec l'architecture actuelle.

Nom possible :

```text
ck_is_exposable
```

ou :

```text
_is_ck_exposable()
```

---

# 6. Statuts d'exposition des catégories

## 6.1 Champ proposé

Ajouter ou formaliser sur `product.public.category` :

```text
ck_exposure_status
```

Type :

```text
Selection
```

Valeurs proposées :

* `active`
* `promise`
* `hidden`
* `draft`
* `archived`

Le champ natif Odoo `website_published` reste utilisé, mais ne suffit pas à piloter l'exposition CK.

## 6.2 Définition des statuts

| Statut     | Signification                                                                                     |
| ---------- | ---------------------------------------------------------------------------------------------------|
| `active`   | Catégorie prête commercialement, visible en navigation forte et potentiellement indexable         |
| `promise`  | Univers de promesse, visible éventuellement dans un bloc éditorial mais pas comme rayon principal |
| `hidden`   | Catégorie existante côté Odoo mais non exposée publiquement dans les navigations CK               |
| `draft`    | Catégorie en préparation, non exposée et non indexable                                            |
| `archived` | Catégorie historique, non exposée, non indexable, préservée pour traçabilité ou redirection        |

## 6.3 Catégorie active

Une catégorie est considérée comme active si elle respecte les critères minimaux suivants :

* catégorie publiée côté Odoo ;
* statut CK `active` ;
* nombre minimal de produits publiés et qualifiés ;
* produits correctement catégorisés ;
* produits dotés d'images propres ;
* métadonnées cards cohérentes ;
* page catégorie non vide ;
* titre et description éditoriale disponibles ;
* absence de filtres absurdes ou non actionnables ;
* page acceptable SEO.

Seuil recommandé V1 :

* minimum 3 produits publiés et qualifiés pour exposition forte ;
* exception possible : 2 produits avec fiches complètes + page catégorie éditorialisée ;
* exception stratégique uniquement sur arbitrage MOA explicite.

Les seuils ne doivent pas être codés en dur si possible.

Constantes ou paramètres recommandés :

```text
CK_CATEGORY_ACTIVE_MIN_PRODUCTS = 3
CK_CATEGORY_FILTER_MIN_PRODUCTS = 5
```

## 6.4 Univers de promesse

Un univers de promesse peut être mentionné dans une logique de marque, mais ne doit pas être présenté comme un rayon riche si le catalogue ne suit pas.

Exemples :

* Boissons des îles ;
* Soin & bien-être ;
* Artisanat & culture ;
* Coffrets découverte.

Un univers `promise` peut apparaître dans une section éditoriale, mais pas nécessairement dans le header ou le footer comme entrée principale.

Règle :

> Si un univers `promise` est affiché visuellement sur la Home, son CTA doit être neutralisé ou pointer vers une page de promesse éditorialisée, jamais vers une page catégorie vide.

## 6.5 Catégorie hidden

Une catégorie `hidden` existe côté Odoo, mais ne doit pas apparaître dans :

* le header ;
* les blocs Home ;
* le footer ;
* les listes d'univers ;
* le sitemap public.

Elle peut rester utilisée pour structurer le catalogue en back-office.

## 6.6 Catégorie draft

Une catégorie `draft` est en préparation.

Elle ne doit pas être exposée publiquement.

Elle ne doit pas être indexable.

La route directe doit retourner un comportement stable défini plus bas.

## 6.7 Catégorie archived

Une catégorie `archived` est conservée pour historique ou migration.

Elle ne doit pas apparaître publiquement.

Si une catégorie remplaçante existe, une redirection 301 peut être prévue.

Champ optionnel recommandé :

```text
ck_replacement_category_id
```

ou mécanisme équivalent.

---

# 7. Produits : publication, qualification et exposition

## 7.1 Ne pas confondre produit publié et produit qualifié CK

Un produit peut être publié dans Odoo sans être éligible à toutes les mises en avant CK.

Il ne faut pas forcément repasser automatiquement un produit incomplet en brouillon Odoo.

En revanche, un produit incomplet ne doit pas être éligible :

* aux mises en avant Home ;
* aux coups de cœur ;
* aux univers actifs ;
* aux blocs éditoriaux marchands ;
* au SEO prioritaire ;
* aux sélections produit visibles comme vitrines CK.

Principe recommandé :

```text
ck_is_qualified_for_public_exposure = True / False
```

ou état équivalent :

```text
ck_quality_state = to_review / ready / blocked
```

Le Dev peut proposer la solution la plus sobre.

## 7.2 Produit orphelin

Un produit publié (`website_published=True`) mais sans catégorie active ou promise est considéré comme un **produit orphelin**.

Règle :

* il peut apparaître dans `/shop` si publié et vendable ;
* il ne doit pas apparaître dans les navigations par univers ;
* il ne doit pas être mis en avant sur la Home ;
* il doit être signalé en back-office pour qualification ou catégorisation.

Objectif :

> Ne pas bloquer brutalement la boutique globale, mais éviter de polluer les parcours par univers.

## 7.3 Qualification minimale produit

Avant d'être mis en avant sur la Home, dans les catégories actives ou dans les blocs commerciaux, un produit CK doit respecter une fiche minimale.

Champs attendus :

* nom clair ;
* image produit exploitable ;
* prix public ;
* catégorie correcte ;
* origine ou justification d'origine ;
* producteur, marque ou artisan ;
* format, poids, volume, matière ou dimension selon type produit ;
* badges cohérents ;
* disponibilité stock ou statut clair : `En stock`, `Sur commande`, `Rupture` ;
* aucune métadonnée contradictoire.

Un produit en rupture ne doit pas porter de badge "Nouveau" actif.

---

# 8. Encadrement des visuels produit

## 8.1 Image produit minimale

Une image produit exploitable doit respecter au minimum :

* image propre ;
* pas de placeholder générique ;
* fond uni ou contexte cohérent ;
* format carré ou portrait ;
* résolution minimale recommandée : 500 × 500 px ;
* rendu compatible cards Home / Shop / catégories.

## 8.2 Images générées IA

Les visuels IA sont acceptés :

* en démo ;
* en illustration éditoriale ;
* en placeholder de travail ;
* pour des produits conceptuels non encore photographiés.

Mais ils ne doivent pas être utilisés comme photo produit définitive d'un article réel sans validation MOA.

Ils ne doivent pas représenter de manière non confirmée :

* une certification ;
* un label ;
* un packaging ;
* une marque ;
* une origine ;
* une matière ;
* une texture exacte ;
* une propriété produit.

Règle :

> Une image IA ne doit jamais renforcer artificiellement une promesse de traçabilité, d'origine ou de certification non validée.

---

# 9. Produits à vérifier en priorité

| Produit            | Correction / vérification attendue                                                                               |
| ------------------- | ------------------------------------------------------------------------------------------------------------------|
| Pâte de manioc     | Doit être rattachée à l'épicerie, ne doit pas afficher "Bien-être" si non pertinent                              |
| Savon vétiver      | Doit être rattaché à Soin & bien-être si l'univers est actif                                                     |
| Chapeau Panama     | Doit être rattaché à Artisanat ou à une catégorie adaptée ; origine, matière, artisan ou producteur à renseigner |
| Jus Mont-Pelé      | Produit existant en base / image Home ; doit être correctement rattaché à Boissons si l'univers est actif        |
| Tambour            | Doit être rattaché proprement à Artisanat & culture si exposé                                                    |
| Coffret découverte | Doit être concret, qualifié ou traité comme promesse non marchande                                               |

Point spécifique Pâte de manioc :

* corriger toute remontée "Bien-être" ;
* ligne meta recommandée : `Guadeloupe · [Producteur] · 1 kg · 3,95 €/kg` ;
* `Sans gluten` doit être traité comme badge ou attribut contrôlé, pas comme métadonnée principale de ligne.

---

# 10. Normalisation des cards produit

Les cards doivent être cohérentes, mais pas identiques pour tous les types de produits.

La ligne meta doit être adaptée à la famille produit.

## 10.1 Modèle alimentaire solide

Format recommandé :

```text
Origine · Producteur · Poids · Prix/kg
```

Exemple :

```text
Guadeloupe · La Platine · 320 g · 17,19 €/kg
```

## 10.2 Modèle boisson

Format recommandé :

```text
Origine · Producteur · Volume · Prix/L
```

Exemple :

```text
Martinique · Mont-Pelé · 75 cl · 4,60 €/L
```

## 10.3 Modèle soin / cosmétique

Format recommandé :

```text
Origine · Producteur/marque · Format · Certification si applicable
```

Exemple :

```text
Guadeloupe · Savonnerie locale · 100 g · Bio
```

## 10.4 Modèle artisanat

Format recommandé :

```text
Origine · Artisan/producteur · Matière · Usage ou dimension
```

Exemple :

```text
Dominique · Artisanat local · Paille naturelle · Taille unique
```

## 10.5 Modèle coffret

Format recommandé :

```text
Composition · Nombre de pièces · Univers · Prix global
```

Exemple :

```text
Sélection découverte · 4 produits · Épicerie créole
```

## 10.6 Critère d'acceptation

Une card ne doit pas afficher de métadonnée incohérente avec son type produit.

Exemple KO :

```text
Pâte de manioc · Bien-être
```

si le produit est alimentaire.

---

# 11. Badges produit

## 11.1 Badges possibles

Badges possibles :

* Nouveau ;
* Coup de cœur ;
* Bio ;
* Producteur ;
* Origine ;
* Bientôt disponible, si utilisé.

## 11.2 Règles d'affichage

Les badges doivent rester lisibles et sobres.

Règles recommandées :

* maximum 2 badges visibles par card ;
* ne pas multiplier les pastilles ;
* ne pas créer un rendu marketplace criard ;
* conserver l'identité CK sobre, chaude et premium.

## 11.3 Priorité des badges

Si 3 badges ou plus sont applicables, ordre de priorité recommandé :

1. Bio, si certification fiable ;
2. Coup de cœur ;
3. Nouveau.

Exemples :

* Produit Bio + Nouveau → afficher Bio + Nouveau ;
* Produit Coup de cœur + Nouveau → afficher Coup de cœur + Nouveau ;
* Produit Bio + Coup de cœur + Nouveau → afficher Bio + Coup de cœur.

## 11.4 Badge Bio

Le badge `Bio` ne doit pas provenir d'une simple étiquette marketing libre non contrôlée.

Il doit s'appuyer sur une donnée fiable, validée et conforme.

Principe :

> Pas de badge Bio sans source de vérité structurée ou validation MOA.

---

# 12. Règles d'exposition publique

## 12.1 Header

Le header ne doit afficher comme entrées catalogue principales que les catégories racines réellement exposables.

Attendu :

* `Boutique` reste visible comme entrée globale ;
* les catégories racines `active` et exposables peuvent être affichées ;
* les catégories `hidden`, `draft` ou `archived` ne doivent pas apparaître ;
* les catégories `promise` ne doivent pas apparaître comme rayons principaux, sauf arbitrage MOA explicite.

Pour la V1, recommandation MOA :

* `Boutique` : visible ;
* `Épicerie créole` : visible fortement ;
* `Boissons`, `Soin & bien-être`, `Artisanat` : à masquer de la navigation forte si contenu insuffisant, ou à traiter comme promesses éditoriales.

## 12.2 Home

La Home doit éviter toute impression de catalogue vide.

Règles :

* la section "Coups de cœur" doit afficher au minimum 4 produits si possible ;
* si moins de 4 produits qualifiés sont disponibles, la section doit adopter un rendu grille compacte ou être fusionnée avec "Nouveautés" ;
* ne pas afficher une section produit qui donne l'impression d'un slider incomplet ou d'une grille tronquée ;
* les univers affichés dans "Acheter par univers" doivent être actifs ou explicitement traités comme promesses éditoriales ;
* aucun CTA Home d'univers ne doit pointer vers une catégorie vide ou incohérente ;
* si un univers n'est pas actif, son CTA doit être masqué, neutralisé ou réorienté vers une page de promesse éditorialisée.

## 12.3 Footer

Le footer doit refléter ce que CK assume publiquement.

Recommandation V1 pour le bloc Boutique :

* Tous les produits ;
* Épicerie créole ;
* Coffrets si page réellement prête ;
* autres univers seulement si actifs ou éditorialisés.

Ne pas afficher un lien footer vers une catégorie vide ou non traitée.

## 12.4 Pages catégories

Une page catégorie publique doit avoir un rendu crédible.

Attendu pour une catégorie active :

* H1 clair ;
* description courte éditoriale ;
* produits visibles ;
* cards cohérentes ;
* filtres contextuels ;
* breadcrumb fonctionnel ;
* SEO indexable si contenu suffisant.

Attendu pour une catégorie non active :

* soit non exposée ;
* soit page éditorialisée proprement ;
* soit `noindex` si page accessible mais pauvre ;
* jamais une simple page vide poussée depuis la navigation forte.

## 12.5 Page de promesse éditorialisée

Pour un univers `promise`, CK peut créer une page éditoriale dédiée.

Cette page ne doit pas être confondue avec une page catégorie marchande.

Elle peut contenir :

* titre ;
* description ;
* visuel ;
* texte de promesse ;
* CTA neutre ;
* mention "Bientôt disponible" ;
* éventuellement CTA "Soyez alerté" si fonctionnalité disponible.

Règle SEO :

* page `noindex` tant qu'il n'y a pas de contenu marchand réel.

---

# 13. Comportement des routes et SEO

## 13.1 Route `/shop`

La route `/shop` n'est pas une catégorie.

Elle reste la boutique globale.

Elle ne doit pas être gouvernée comme une catégorie `active`, `promise`, `hidden` ou `draft`.

Règle :

> Le statut d'exposition pilote les portes d'entrée et les univers, pas nécessairement l'existence du produit dans la boutique globale.

Donc :

* `/shop` reste accessible ;
* les produits publiés et vendables peuvent y apparaître ;
* les produits non qualifiés peuvent être exclus des mises en avant CK ;
* les catégories non exposables ne doivent pas apparaître comme filtres ou portes d'entrée fortes si cela crée de la confusion.

## 13.2 Routes catégories

Comportement recommandé :

| Statut catégorie | Route directe                                                | Navigation                      | SEO / sitemap                  |
| ----------------- | -------------------------------------------------------------- | ---------------------------------- | --------------------------------- |
| `active`         | 200 catégorie marchande                                      | visible si exposable            | index si contenu OK            |
| `promise`        | 200 page éditorialisée ou redirect vers page promesse dédiée | non visible en navigation forte | noindex, hors sitemap marchand |
| `hidden`         | 302 vers `/shop` ou 404 selon règle projet                   | invisible                       | hors sitemap                   |
| `draft`          | 404                                                          | invisible                       | hors sitemap                   |
| `archived`       | 301 vers catégorie remplaçante si connue, sinon 404          | invisible                       | hors sitemap                   |

Le comportement doit être stable et testable.

Il ne doit pas être décidé au cas par cas sans règle claire.

## 13.3 Sitemap

Règles :

* une catégorie `active` exposable peut être présente dans le sitemap ;
* une catégorie `promise` sans contenu marchand réel ne doit pas être dans le sitemap marchand ;
* une catégorie `hidden`, `draft` ou `archived` ne doit pas être dans le sitemap public ;
* une page `noindex` ne doit pas être présente dans le sitemap public.

Critère important :

> Une catégorie ne doit pas être à la fois `noindex` et présente dans le sitemap public.

---

# 14. Filtres et tri

## 14.1 Page `/shop`

La boutique globale doit permettre une navigation simple dès que le catalogue grossit.

Attendu recommandé :

* tri par prix ;
* tri par nouveauté ;
* filtre par univers ;
* filtre par origine ;
* filtre par producteur.

Si ces éléments existent déjà via Odoo ou modules CK, vérifier leur visibilité et leur cohérence.

## 14.2 Pages catégories

Les filtres doivent être contextuels.

Règles :

* ne pas afficher des filtres qui ne correspondent pas aux produits réellement présents dans la catégorie ;
* éviter les filtres trop larges sur une catégorie pauvre ;
* masquer les groupes de filtres non actionnables si nécessaire ;
* si une catégorie contient moins que le seuil défini, masquer les filtres et conserver seulement un tri simple.

Seuil recommandé :

```text
CK_CATEGORY_FILTER_MIN_PRODUCTS = 5
```

Le seuil doit être configurable ou centralisé.

Tri simple recommandé :

* prix croissant ;
* prix décroissant ;
* nouveauté.

Critère d'acceptation :

> Une catégorie avec un seul produit ne doit pas afficher une liste massive de filtres donnant l'impression d'un catalogue incohérent.

---

# 15. Sous-catégories

Ne pas créer ou exposer des sous-catégories uniquement pour "faire riche".

Règle recommandée :

> Une sous-catégorie devient visible seulement si elle contient au moins 3 produits publiés et qualifiés, ou 2 produits exceptionnels avec fiches complètes + page éditorialisée.

Pour Épicerie, les sous-catégories cibles peuvent être :

* Confitures & douceurs ;
* Farines & pâtes ;
* Condiments & épices ;
* Biscuits & snacks.

Mais elles ne doivent être affichées que si le contenu réel le justifie.

---

# 16. Comportement attendu par page

## 16.1 `/`

Attendu :

* Home cohérente ;
* minimum 4 produits visibles dans "Coups de cœur" si disponibles ;
* sinon rendu grille compacte ou fusion avec "Nouveautés" ;
* CTA univers uniquement vers pages crédibles ;
* pas de lien vers catégorie vide sans traitement ;
* coffret découverte concret ou traité comme promesse ;
* aucun CTA Home univers vers catégorie `hidden`, `draft`, `archived` ou vide ;
* mobile 390 px sans overflow horizontal ni zoom nécessaire pour ajouter au panier.

## 16.2 `/shop`

Attendu :

* catalogue global visible ;
* produits correctement qualifiés ou signalés comme à qualifier ;
* cards cohérentes par famille produit ;
* filtres/tri visibles ou préparés selon standard Odoo ;
* aucun produit avec tag incohérent ;
* pas d'effet "fourre-tout incompréhensible".

## 16.3 `/shop/category/epicerie-1`

Attendu :

* catégorie active V1 ;
* produits alimentaires cohérents ;
* prix/kg ou prix de référence si pertinent ;
* description éditoriale ;
* sous-catégories uniquement si contenu suffisant ;
* indexable si contenu suffisant.

## 16.4 `/shop/category/boissons-123`

Attendu selon statut retenu :

* si `active` : afficher produits boissons qualifiés, description, prix/L ;
* si `promise` : page éditorialisée, `noindex` ;
* si non active : ne pas exposer fortement ;
* si page pauvre : `noindex`, hors sitemap ou redirection selon statut.

## 16.5 `/shop/category/soin-bien-etre-2`

Attendu selon statut retenu :

* si `active` : afficher produits soin qualifiés ;
* savon vétiver à vérifier ;
* si `promise` : page éditorialisée, `noindex` ;
* si non active : ne pas exposer fortement ;
* si page pauvre : `noindex`, hors sitemap ou redirection selon statut.

## 16.6 `/shop/category/artisanat-3`

Attendu selon statut retenu :

* si `active` : afficher produits artisanat qualifiés ;
* vérifier chapeau, tambour ou autres produits ;
* origine, matière, artisan/producteur à renseigner ;
* si `promise` : page éditorialisée, `noindex` ;
* si non active : ne pas exposer fortement ;
* si page pauvre : `noindex`, hors sitemap ou redirection selon statut.

---

# 17. Priorités

## 17.1 P0 — Bloquant clôture propre

1. Ne plus exposer fortement des catégories vides ou pauvres sans traitement.
2. Corriger les catégorisations incohérentes :

   * Pâte de manioc : épicerie, pas bien-être ;
   * Savon vétiver : soin, si univers actif ;
   * Chapeau Panama : artisanat ou catégorie adaptée ;
   * Jus Mont-Pelé : boissons, bug de catégorisation si produit existant ;
   * Tambour : artisanat si exposé ;
   * Coffret : concret ou promesse.
3. Corriger tout CTA Home qui pointe vers une destination non conforme ou trop pauvre.
4. Éviter qu'une catégorie `noindex` soit présente dans le sitemap public.
5. Empêcher les catégories `hidden`, `draft`, `archived` d'apparaître dans le header.

## 17.2 P1 — Important

1. Introduire ou formaliser le statut d'exposition des catégories (`ck_exposure_status`).
2. Introduire ou formaliser une règle d'éligibilité commerciale (`ck_is_exposable` ou helper équivalent).
3. Adapter header / Home / footer à ces statuts.
4. Normaliser les métadonnées cards par famille produit.
5. Rendre les filtres contextuels ou les masquer si non pertinents.
6. Ajouter descriptions de catégories actives.
7. Signaler les produits orphelins en back-office.

## 17.3 P2 — Amélioration

1. Sous-catégories Épicerie si contenu suffisant.
2. Badges visuels plus lisibles mais sobres.
3. Gestion éditoriale enrichie des univers de promesse.
4. SEO fin : index / noindex selon maturité.
5. Page de promesse éditorialisée complète par univers.
6. Alerte email "m'avertir" si retenue plus tard.

---

# 18. Critères d'acceptation globaux

Le lot sera considéré conforme si :

1. Une catégorie vide ou quasi vide n'est plus exposée comme un rayon principal.
2. Le header ne pousse que les univers actifs et exposables, ou explicitement validés MOA.
3. La Home ne donne pas l'impression d'un catalogue vide.
4. Les CTA Home univers mènent vers des pages cohérentes.
5. Aucun CTA Home univers ne pointe vers une catégorie `hidden`, `draft`, `archived` ou vide.
6. Le footer ne renvoie pas vers des pages pauvres non traitées.
7. Les produits visibles ont des catégories cohérentes.
8. La ligne meta des cards est adaptée au type produit.
9. Les badges ne surchargent pas les cards.
10. Les pages catégories actives disposent d'un minimum éditorial.
11. Les catégories pauvres sont masquées, éditorialisées ou noindexées.
12. Aucune page `noindex` n'est présente dans le sitemap public.
13. Aucun produit alimentaire ne remonte avec une métadonnée "Bien-être" incohérente.
14. Aucun produit artisanal ne reste sans information minimale d'origine, matière ou producteur s'il est mis en avant.
15. Sur mobile 390 px, un utilisateur peut ajouter un produit au panier depuis la Home sans scroll horizontal ni zoom.
16. Les catégories `hidden`, `draft` et `archived` sont absentes du header.
17. Une catégorie `promise` n'est pas exposée comme rayon principal.
18. Les produits orphelins restent gérés proprement : visibles dans `/shop` si publiés et vendables, mais exclus des navigations par univers.

---

# 19. Recette attendue

## 19.1 Routes à contrôler

* `/`
* `/shop`
* `/shop/category/epicerie-1`
* `/shop/category/boissons-123`
* `/shop/category/soin-bien-etre-2`
* `/shop/category/artisanat-3`

Selon statuts appliqués, certaines routes peuvent être :

* 200 catégorie marchande ;
* 200 page de promesse éditorialisée ;
* 301 / 302 vers `/shop` ou page remplaçante ;
* 404 ;
* noindex.

Le comportement attendu doit être documenté dans les résultats de recette.

## 19.2 Viewports à contrôler

* desktop 1280 px ;
* mobile 390 px.

## 19.3 Points de contrôle recette

Pour chaque route :

* statut HTTP conforme au statut de catégorie ;
* pas d'erreur JS visible ;
* pas d'overflow horizontal mobile ;
* header cohérent ;
* footer cohérent ;
* breadcrumb cohérent ;
* cards lisibles ;
* CTA fonctionnels ;
* absence de page vide exposée fortement ;
* cohérence SEO index / noindex selon statut ;
* cohérence sitemap ;
* cohérence des cards produit ;
* cohérence des badges ;
* comportement mobile 390 px acceptable.

---

# 20. Tests automatisés recommandés V1

Tests V1 recommandés :

1. **Navigation header**

   * Une catégorie `hidden`, `draft` ou `archived` ne doit pas apparaître dans le header.

2. **Cohérence card alimentaire**

   * Un produit alimentaire ne doit pas afficher une métadonnée "Bien-être" incohérente.

3. **Exposition catégorie pauvre**

   * Une catégorie vide ou pauvre ne doit pas être exposée fortement.
   * Elle doit être masquée, redirigée, éditorialisée ou `noindex` selon statut.

4. **CTA Home univers**

   * Aucun CTA Home univers ne doit pointer vers une catégorie `hidden`, `draft`, `archived` ou vide.

5. **SEO sitemap / noindex**

   * Une catégorie `promise` ou pauvre ne doit pas être à la fois `noindex` et présente dans le sitemap public.

6. **Mobile Home panier**

   * Sur viewport 390 px, un utilisateur peut ajouter un produit au panier depuis la Home sans scroll horizontal ni zoom.

7. **Footer**

   * Le footer ne doit pas afficher de lien vers une catégorie `hidden`, `draft`, `archived` ou pauvre non traitée.

Tests complémentaires P2 possibles :

* sous-catégories visibles seulement si seuil atteint ;
* badge Bio affiché uniquement depuis donnée validée ;
* produit orphelin signalé ;
* filtres masqués sous seuil ;
* catégorie `archived` redirigée vers remplaçante si définie.

---

# 21. Attendu Dev

Le Dev est invité à proposer l'implémentation technique la plus sobre, compatible avec l'architecture CK existante.

Principes attendus :

* s'appuyer autant que possible sur le standard Odoo ;
* éviter une surcouche lourde ;
* éviter de détourner les champs natifs `website_published` ou catégories publiques ;
* privilégier une configuration explicite et maintenable ;
* conserver la navigation dynamique existante en l'enrichissant par une règle de maturité ;
* ne pas casser les routes catégories existantes sans règle documentée ;
* documenter clairement les règles appliquées ;
* rendre les règles testables ;
* centraliser les seuils ;
* éviter les comportements ad hoc par catégorie.

Implémentations possibles à discuter :

* champ `ck_exposure_status` sur `product.public.category` ;
* helper `ck_is_exposable` ;
* helper produit `ck_is_qualified_for_public_exposure` ;
* rapport ou signalement BO des produits orphelins ;
* logique sitemap filtrée par statut ;
* templates header / Home / footer lisant la règle CK ;
* redirection ou 404 selon statut.

---

# 22. Attendu QA

La QA doit valider non seulement que les pages répondent, mais que l'exposition publique est cohérente avec la doctrine CK.

La QA doit vérifier :

* la cohérence des statuts ;
* la cohérence des routes ;
* la cohérence navigation / Home / footer ;
* la cohérence SEO ;
* la cohérence mobile ;
* la cohérence des cards ;
* l'absence de catégorie vide mise en avant ;
* l'absence de produit incohérent en card ;
* la cohérence des CTA ;
* l'absence de régression sur `/shop`.

La QA doit produire un verdict du type :

```text
GO QA — exposition catalogue CK cohérente
```

ou :

```text
NO GO QA — catégorie / produit / route incohérent(e)
```

avec les routes et captures concernées.

---

# 23. Verdict MOA attendu après livraison

Ce lot doit permettre de passer de :

> "Le catalogue existe techniquement."

à :

> "Le catalogue exposé publiquement est crédible, cohérent et commercialement assumé."

La V1 CK peut avoir une ambition multi-univers, mais son exposition publique doit rester proportionnée à la maturité réelle du catalogue.

Doctrine finale :

> **CK peut avoir une ambition multi-univers, mais son exposition publique doit rester proportionnée à la maturité réelle du catalogue.**

Et règle de gouvernance à conserver :

> **On ne montre pas une catégorie parce qu'elle existe ; on la montre parce qu'elle est prête à convaincre.**

---

# 24. Statut de la présente note

Cette note constitue la base de cadrage Dev / QA pour le lot :

```text
CK-CATALOG-ARCHI-001
```

Elle devra être transformée en ticket(s) opérationnel(s) après validation MOA / Architecture.

Découpage recommandé :

1. Ticket A — Statut d'exposition catégories + navigation header/Home/footer.
2. Ticket B — Correction catégorisation produits + qualification cards.
3. Ticket C — SEO / sitemap / noindex / routes catégories.
4. Ticket D — Filtres contextuels et seuils d'affichage, si retenu dans le même sprint ou en lot suivant.
