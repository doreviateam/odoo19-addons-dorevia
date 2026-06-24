# Retour Dev — Direction UX Shop C-Kréyòl V1

| Champ | Valeur |
| --- | --- |
| Projet | `dorevia_ck_marketone` |
| Document analysé | Direction UX — Shop C-Kréyòl · V1 |
| Source | Retour UX Carole — Shop Structure V1 |
| Date | 2026-06-24 |
| Statut | Retour Dev détaillé · à arbitrer MOA avant exécution |
| Périmètre | Page `/shop` et impacts nécessaires sur `/shop/category/...` |
| Modules actifs | `dorevia_ck_theme`, `dorevia_ck_marketone_content` |
| Hors périmètre | Home, fiche produit, refonte moteur facettes, modèle producteur, rating complet |

---

## 1. Objet du document

Ce document transforme la **Direction UX Shop C-Kréyòl V1** en retour Dev détaillé.

Le texte source exprime une intention juste : faire passer `/shop` d'un catalogue Odoo propre mais générique à un **rayon boutique créole**. Il ne doit toutefois pas être appliqué comme une maquette figée ou comme une spécification technique brute.

La mission Dev est donc de cadrer :

- ce qui est déjà couvert par le code consolidé ;
- ce qui doit être ajusté en priorité ;
- ce qui est simple et peu risqué ;
- ce qui est prudent mais demande une vraie attention Odoo ;
- ce qui serait risqué dans le Lot Shop Structure V1 ;
- ce qui doit partir dans des lots séparés.

Position Dev synthétique :

> La direction UX est validable en intention. Techniquement, le bon chemin n'est pas de réécrire `website_sale`, mais d'orchestrer plus finement ses composants natifs : introduction, filmstrip, outils catalogue, sidebar, cards, données de confiance.

La doctrine reste la même que pour les lots CK précédents :

```text
Odoo reste le moteur.
CK devient la lecture commerciale.
```

---

## 2. Lecture Dev du document source

### 2.1 Ce que le document source valide réellement

Le document valide une direction d'expérience, pas encore une architecture technique.

Sont validés côté MOA :

- la priorité donnée à la promesse CK avant les outils catalogue ;
- le passage d'une lecture "filtres / tri / grille" à une lecture "rayon / sélection / origine / achat" ;
- la pyramide de lecture : intro, catégories, outils secondaires, grille ;
- le principe d'un Shop plus marchand et plus curaté ;
- le refus du sur-design décoratif ;
- le maintien des garde-fous Odoo.

Ne sont pas validés tels quels :

- les seuils définitifs ;
- les tailles exactes ;
- les couleurs exactes ;
- l'implémentation du rating ;
- les comportements conditionnels précis ;
- les remplacements de libellés natifs Odoo ;
- la structure finale des templates.

### 2.2 Ce que le document demande au Dev

La demande implicite n'est pas "appliquez ce texte".

La demande réelle est :

> Proposer une implémentation Odoo sobre, maintenable et réversible qui fasse lire `/shop` comme une boutique C-Kréyòl, sans casser les mécanismes natifs de vente, de recherche, de tri, de facettes et de panier.

Cela impose un double mouvement :

- renforcer le signal CK en haut de page ;
- diminuer le poids perceptif des outils Odoo sans les supprimer.

---

## 3. État du code consolidé au 2026-06-24

Le code actuel n'est pas un état vierge. Plusieurs briques demandées par la direction UX existent déjà partiellement.

### 3.1 Briques déjà présentes

| Zone | État constaté | Lecture Dev |
| --- | --- | --- |
| Intro Shop | `dorevia_ck_theme/views/snippets/ck_snippet_shop_intro.xml` injecté via `website_sale.products` | Emplacement propre, mais contenu trop pauvre et wording à corriger. |
| Composition Shop | `website_sale_shop_compose.xml` hérite `website_sale.products` avec XPath court | Bonne approche : on conserve Odoo. |
| Filmstrip catégories | Variant natif Odoo `website_sale.filmstrip_categories_pills` activé | Très bon choix : comportement natif conservé, rendu plus boutique. |
| Barre catalogue | `#o_wsale_products_header` habillé en bande CK | Déjà aligné avec la direction, à affiner. |
| Compteur produits | `search_count` affiché via `website_sale_toolbar_count.xml` | Utile, mais le document source souhaite plutôt le remonter dans l'intro. |
| Sidebar | Classe `.ck-shop-sidebar` et titre ajoutés | Structure OK, micro-copy encore à arbitrer. |
| Cards produit | Classes CK, origine en eyebrow, meta secondaire, CTA compact | Très proche de la cible UX. |
| Achat rapide | Bouton panier compact, accessible, non supprimé | Conforme à la priorité "achat rapide". |
| Origine | Affichage conditionnel, sans fallback inventé | Conforme à la promesse CK. |
| Rayons éditorialisés | `shop_rayon_editorial.py` + `website_sale_rayon_editorial.xml` | Déjà engagé côté Épicerie, mais hors cible stricte `/shop` V1 si on limite le lot. |

### 3.2 Briques encore faibles ou incomplètes

| Zone | Écart restant | Priorité |
| --- | --- | --- |
| Nom public | `Boutique C-Kreyol` sans accent dans l'intro | Haute |
| Intro | H1 seul, pas de phrase de promesse, pas de compteur dans l'intro | Haute |
| Promesse CK | Trop peu visible avant la barre catalogue | Haute |
| Filmstrip | Libellés dépendants des noms de catégories Odoo | Moyenne |
| Sidebar | Titre actuel `Filtres`, sections natives encore très techniques | Moyenne |
| Slider prix | Pas de règle de seuil clairement implémentée | Moyenne |
| Recherche Shop | Encore présente comme outil de premier rang | Moyenne |
| Rating | Pas d'emplacement conditionnel en card | Basse en V1, lot séparé recommandé |
| Producteur | Non affiché, et c'est correct en V1 | À ne pas faire |

### 3.3 Point de vigilance documentaire

Certains documents de recette antérieurs indiquent que P2B n'était pas encore implémenté. Le code consolidé contient désormais des briques de rayon éditorialisé, notamment pour Épicerie.

Il faut donc distinguer :

- **Shop Structure V1** : page `/shop`, hiérarchie globale, outils, cards ;
- **Rayon éditorialisé P2B** : pages catégories éligibles, contenu de rayon, sous-familles, preuves de rayon.

Le document source porte explicitement sur `/shop` uniquement. Le retour Dev recommande donc de ne pas mélanger les deux sujets dans un même lot d'exécution.

---

## 4. Diagnostic Dev

### 4.1 Le vrai problème n'est pas le style

La page Shop est techniquement fonctionnelle et déjà améliorée. Le problème restant est un problème de **hiérarchie de perception**.

Aujourd'hui, la lecture tend encore vers :

```text
Boutique
↓
outils catalogue
↓
filtres
↓
produits
```

La cible UX demande :

```text
Promesse C-Kréyòl
↓
portes d'entrée de découverte
↓
outils secondaires
↓
produits actionnables
```

La différence est subtile mais décisive : le client doit d'abord comprendre où il est et pourquoi la sélection est légitime, avant d'être mis devant les outils.

### 4.2 Le Shop ne doit pas devenir une landing page

Il faut éviter deux excès :

- garder un simple listing Odoo ;
- transformer `/shop` en page éditoriale lourde qui repousse les produits.

Le bon niveau V1 est :

> Une introduction courte, des catégories lisibles, des outils contenus, des cards denses et achetables.

Le Shop reste une page transactionnelle. L'éditorial doit soutenir l'achat, pas le remplacer.

### 4.3 La promesse CK doit passer par les données réelles

La direction UX insiste à juste titre sur :

- sélection ;
- origine ;
- producteur ;
- confiance ;
- achat rapide.

Mais en V1, toutes ces promesses ne peuvent pas être traitées au même niveau.

| Promesse | Faisabilité V1 | Commentaire Dev |
| --- | --- | --- |
| Sélection | Oui | Wording, compteur, catégories, produits visibles. |
| Origine | Oui si donnée saisie | Déjà affichée conditionnellement. Ne rien inventer. |
| Producteur | Non en card V1 | `seller_ids` n'est pas une preuve producteur fiable. |
| Confiance | Oui partiellement | Origine, prix, format, panier, absence de fausses étoiles. |
| Achat rapide | Oui | CTA panier compact déjà conforme. |

---

## 5. Proposition d'implémentation Lot Shop Structure V1

### 5.1 Objectif du lot

Objectif :

```text
Faire lire /shop comme un rayon boutique C-Kréyòl,
sans réécrire website_sale et sans inventer de données.
```

Ce lot doit rester limité à :

- l'intro Shop ;
- le positionnement et la hiérarchie du filmstrip ;
- le poids visuel de la barre catalogue ;
- la micro-copy de la sidebar ;
- quelques ajustements card mineurs si nécessaires ;
- la préparation d'un emplacement rating non affiché tant qu'il n'y a pas d'avis réel.

### 5.2 Non-objectifs du lot

Ne pas traiter dans ce lot :

- Home ;
- fiche produit ;
- modèle producteur ;
- pages producteurs dynamiques ;
- refonte du moteur de facettes ;
- nouveau contrôleur lourd `website_sale` ;
- rating complet ;
- tri par note ;
- pagination / "voir plus" ;
- logique de stock ;
- promesses logistiques non validées ;
- textures, motifs ou décor créole artificiel.

---

## 6. Zone 1 — Intro Shop

### 6.1 Intention UX

L'intro doit dire la promesse CK avant l'apparition des outils.

Le texte source propose :

```text
Boutique C-Kréyòl

Produits créoles sélectionnés, aux origines identifiées.

7 produits sélectionnés
```

Cette direction est correcte.

### 6.2 État actuel

Le snippet actuel affiche seulement :

```text
Boutique C-Kreyol
```

Écarts :

- accent manquant dans `C-Kréyòl` ;
- absence de phrase de promesse ;
- absence de compteur dans l'intro ;
- classes SCSS prévues pour `lead`, `note` et `trust` peu ou pas exploitées.

### 6.3 Recommandation Dev

Modifier `s_ck_shop_intro` en conservant le même point d'injection.

Structure recommandée :

```xml
<section class="s_ck_shop_intro ck-shop-intro">
  <div class="container">
    <h1>Boutique C-Kréyòl</h1>
    <p>Produits créoles sélectionnés, aux origines identifiées.</p>
    <p t-if="search_count">N produits sélectionnés</p>
  </div>
</section>
```

Points importants :

- utiliser `C-Kréyòl` dans les textes publics ;
- ne pas mentionner Nantes, France ou Europe dans ce lot si la promesse logistique n'est pas validée ;
- ne pas transformer l'intro en hero ;
- garder une hauteur compacte ;
- conserver la compatibilité mobile ;
- éviter un CTA primaire qui concurrencerait l'achat produit.

### 6.4 CTA "Découvrir la sélection"

Le CTA peut être utile en mobile, mais il doit rester secondaire.

Recommandation :

- ne pas en faire un bouton rouge ;
- utiliser un lien discret vers `#products_grid` ou une ancre native stable si disponible ;
- ne l'ajouter que si la recette mobile montre un vrai bénéfice ;
- ne pas l'ajouter en première passe si le scroll naturel suffit.

Statut recommandé :

```text
Optionnel V1, à arbitrer après capture mobile.
```

---

## 7. Zone 2 — Filmstrip catégories

### 7.1 Intention UX

Le filmstrip doit être lu comme une navigation de découverte, pas comme un filtre technique.

Le document source demande :

- position sous l'intro ;
- état actif clair ;
- `Tous` en première entrée ;
- libellés publics validés ;
- pas de `Coup de cœur` si la catégorie n'est pas réellement alimentée.

### 7.2 État actuel

Le code active le variant natif Odoo `filmstrip_categories_pills`.

C'est la bonne approche :

- pas de réécriture du filmstrip ;
- clics natifs conservés ;
- URLs Odoo conservées ;
- état actif géré par Odoo ;
- rendu plus léger que les tuiles image vides.

### 7.3 Recommandation Dev

Conserver le filmstrip natif en pills.

Ne pas recréer un composant custom tant que le composant Odoo suffit.

Actions recommandées :

1. Vérifier que le filmstrip est bien rendu sous l'intro sur `/shop`.
2. Vérifier que l'état actif reste visible sur `/shop/category/...`.
3. Vérifier que `Tous` reste la première entrée.
4. Corriger les libellés via données BO lorsque la catégorie publique doit changer.

### 7.4 Libellé "Soin & bien-être"

La direction UX valide :

```text
Soin & bien-être
```

et rejette :

```text
Maison & bien-être
```

Lecture Dev :

- si le nom public de la catégorie doit réellement être `Soin & bien-être`, le plus propre est de corriger la catégorie publique en BO ou via migration de données ;
- éviter un mapping QWeb fragile qui affiche un nom différent de la catégorie réelle ;
- vérifier l'impact SEO et les URLs existantes ;
- tester que les anciennes URLs restent servies ou redirigées correctement.

Recommandation :

```text
Lot contenu/données léger, pas hack template.
```

### 7.5 "Coup de cœur"

Règle Dev :

`Coup de cœur` ne doit apparaître dans le filmstrip que si c'est une vraie catégorie publique, alimentée, servie par Odoo, avec des produits publiés.

Sinon :

- le conserver comme badge produit ;
- ou comme logique de curation Home ;
- mais ne pas le présenter comme porte d'entrée catalogue.

---

## 8. Zone 3 — Barre catalogue

### 8.1 Intention UX

La barre catalogue doit rester utile, mais perdre son statut de premier signal.

Éléments à conserver :

- recherche Shop ;
- tri ;
- compteur ;
- filtres ;
- URLs natives ;
- comportements Odoo.

Éléments à réduire :

- poids visuel de la recherche ;
- poids visuel du tri ;
- slider prix en petit catalogue ;
- répétition du compteur si l'intro le porte déjà.

### 8.2 État actuel

Le code habille `#o_wsale_products_header` en bande CK et affiche `search_count`.

Ce choix est sain :

- pas de logique métier ajoutée ;
- `search_count` est déjà exposé par le contrôleur Odoo ;
- le rendu donne une bande cohérente.

### 8.3 Recommandation Dev

À faire :

- conserver l'habillage actuel ;
- déplacer ou dupliquer prudemment le compteur vers l'intro selon arbitrage ;
- si le compteur reste dans la toolbar, ne pas l'afficher deux fois ;
- garder recherche et tri discrets ;
- éviter de masquer la recherche si une requête est active.

### 8.4 Slider prix

La direction MOA recommandée est :

```text
Masquer le slider prix tant que le catalogue total publié est inférieur à 15 produits,
sauf si un filtre prix est déjà actif dans l'URL.
```

Lecture Dev :

Cette règle est pertinente UX, mais elle doit être définie techniquement.

Trois options existent.

| Option | Principe | Avantage | Risque |
| --- | --- | --- | --- |
| A — CSS simple | Masquer le bloc prix en petit catalogue par classe CSS | Très rapide | Pas vraiment conditionnel. |
| B — `search_count` | Masquer si le résultat courant est inférieur à 15 | Simple en QWeb | Ce n'est pas le catalogue total ; peut masquer sur une recherche filtrée. |
| C — compteur total publié | Calculer le total publié indépendamment des filtres | Plus fidèle à la MOA | Demande une injection propre de donnée, plus risquée. |

Recommandation V1 :

```text
Option B si on veut livrer vite, avec commentaire explicite.
Option C seulement si la règle devient durable et opposable.
```

Garde-fou :

Le slider doit rester visible si un prix min/max est actif dans l'URL, pour ne pas enfermer l'utilisateur dans un filtre invisible.

---

## 9. Zone 4 — Sidebar

### 9.1 Intention UX

La sidebar doit devenir une aide d'affinage, pas le premier signal de la page.

Micro-copy cible :

| Actuel / technique | Cible UX |
| --- | --- |
| `Filtres` | `Affiner ma sélection` |
| `Étiquettes` | `Origines & préférences` |
| `Fourchette de prix` | `Budget` |

### 9.2 État actuel

Le code ajoute déjà une classe `.ck-shop-sidebar` et un titre `Filtres`.

Les facettes natives restent intactes, ce qui est correct.

### 9.3 Recommandation Dev

Faire évoluer la micro-copy sans réécrire le moteur de facettes.

Ordre recommandé :

1. Renommer le titre CK ajouté en `Affiner ma sélection`.
2. Traiter `Étiquettes` et `Fourchette de prix` par traduction ou XPath ciblé si les ancres sont robustes.
3. Ne pas modifier les noms d'attributs en base si ces noms ont un usage BO ou technique.
4. Tester la sidebar desktop, tablette et mobile.

À éviter :

- remplacer tout le bloc facettes ;
- recréer les accordéons ;
- perdre l'état actif des filtres ;
- masquer un filtre actif.

---

## 10. Zone 5 — Cards produit

### 10.1 Intention UX

Chaque card doit devenir une preuve CK :

```text
Image produit
↓
Origine
↓
Titre produit
↓
Catégorie · format
↓
Prix de référence discret
↓
Rating si avis réel
↓
Prix principal + CTA
```

### 10.2 État actuel

Le code actuel couvre déjà l'essentiel :

- origine en eyebrow au-dessus du titre ;
- ligne secondaire issue des données existantes ;
- prix principal lisible ;
- CTA panier compact ;
- pas de producteur inventé ;
- pas de rating artificiel ;
- pas de valeur d'origine inventée.

Ce point est l'un des plus solides du chantier.

### 10.3 Recommandation Dev

Ne pas refondre la card.

Actions V1 possibles :

- vérifier le ratio image/card en desktop, tablette, mobile ;
- éviter que les cards deviennent trop hautes ;
- conserver la densité marchande ;
- garder le CTA compact ;
- ne pas ajouter de badge décoratif ;
- ne pas ajouter de producteur ;
- ne pas afficher d'étoiles vides.

Ratio recommandé :

```text
Conserver une zone image stable, proche d'un ratio 4:3 ou carré selon le rendu existant,
mais ne pas augmenter la hauteur de card si cela réduit la comparaison rapide entre produits.
```

Le point exact doit être validé par capture, pas uniquement par intention.

---

## 11. Rating et avis

### 11.1 Lecture Dev

Le rating est une bonne preuve de confiance à terme, mais ce n'est pas un sujet de structure Shop V1.

Règles à respecter :

- afficher uniquement si `rating_count > 0` ;
- ne jamais afficher d'étoiles vides ;
- ne pas créer de tri par note en V1 ;
- ne pas inventer de note ;
- tester le flux complet d'avis Odoo avant publication.

### 11.2 Recommandation

Découpage :

| Lot | Contenu |
| --- | --- |
| Shop Structure V1 | Prévoir l'emplacement dans la card si la donnée existe, mais ne rien afficher sans avis réel. |
| Rating-1 | Activer, tester et documenter le flux natif Odoo : dépôt, modération, affichage, permissions. |

Le rating doit donc rester un lot séparé.

---

## 12. Couleurs et système visuel

### 12.1 Intention UX

Le Shop doit être :

- sobre ;
- chaud ;
- clair ;
- lisible ;
- cohérent avec le header ;
- non décoratif.

### 12.2 Recommandation Dev

Utiliser les tokens existants :

- `$ck-bg` ;
- `$ck-bg-soft` ;
- `$ck-surface` ;
- `$ck-border` ;
- `$ck-primary` ;
- `$ck-primary-text` ;
- `$ck-text` ;
- `$ck-text-muted` ;
- `$ck-radius-*` ;
- `$ck-space-*`.

À éviter :

- couleurs hardcodées ;
- nouveaux rouges/oranges sans nom ;
- textures ;
- motifs créoles ;
- dégradés lourds ;
- images décoratives sans lien produit.

L'identité CK doit venir de :

- la hiérarchie ;
- le wording ;
- les produits ;
- les images réelles ;
- l'origine visible ;
- l'achat rapide ;
- la cohérence des composants.

---

## 13. Garde-fous Odoo

Le lot doit préserver :

- `website_sale.products` ;
- `website_sale.products_item` ;
- URLs `/shop` ;
- URLs `/shop/category/...` ;
- recherche ;
- tri ;
- facettes ;
- attributs ;
- prix ;
- variantes ;
- panier rapide ;
- offcanvas mobile ;
- header ;
- footer.

Méthode recommandée :

- héritages QWeb courts ;
- XPath sur IDs ou ancres stables ;
- classes CK ajoutées, pas remplacement massif ;
- SCSS réversible ;
- pas de nouveau modèle de données ;
- pas de contrôleur si une donnée native suffit ;
- tests sur `/shop` et au moins une catégorie.

---

## 14. Matrice de décision Dev

| Sujet | Décision recommandée | Niveau |
| --- | --- | --- |
| Corriger `C-Kreyol` en `C-Kréyòl` dans l'intro | À faire | Simple |
| Ajouter phrase courte de promesse | À faire | Simple |
| Afficher compteur dans l'intro | À faire si pas doublonné dans toolbar | Simple |
| Garder filmstrip pills natif | À conserver | Simple |
| Renommer `Filtres` en `Affiner ma sélection` | À faire | Simple |
| Renommer sections sidebar | À faire prudemment | Prudent |
| Masquer slider prix selon seuil | À cadrer techniquement | Prudent |
| Masquer recherche Shop si inactive | À éviter en V1 ou à traiter très prudemment | Prudent |
| Ajouter emplacement rating conditionnel | Préparer seulement si sans rendu vide | Prudent |
| Afficher rating réel | Lot séparé | Lot séparé |
| Afficher producteur en card | Ne pas faire V1 | Risqué |
| Recréer le filmstrip custom | Ne pas faire | Risqué |
| Réécrire les facettes | Ne pas faire V1 | Risqué |
| Traiter pages rayons éditorialisées | À séparer de Shop Structure V1 | Lot séparé |
| Reprendre la Home | Hors périmètre | Lot séparé |

---

## 15. Découpage recommandé

### Lot S1 — Shop Structure V1 sobre

Objectif : appliquer la direction UX sur `/shop` sans changer le moteur Odoo.

Contenu :

- intro Shop enrichie ;
- wording public `C-Kréyòl` ;
- compteur produits dans la zone la plus pertinente ;
- filmstrip conservé ;
- micro-copy sidebar ;
- poids visuel toolbar ajusté ;
- vérifications cards existantes.

Livrable :

- code léger ;
- captures desktop/tablette/mobile ;
- note de recette ;
- pas de nouveau modèle.

### Lot S2 — Règle slider prix et outils catalogue

Objectif : clarifier les comportements conditionnels.

Contenu :

- seuil `< 15 produits` ;
- conservation du slider si filtre prix actif ;
- choix `search_count` vs total publié ;
- tests de recherche, tri, prix.

Ce lot peut être fusionné avec S1 uniquement si la règle retenue reste simple.

### Lot S3 — Données publiques catégories

Objectif : aligner les libellés publics et les portes d'entrée.

Contenu :

- `Soin & bien-être` ;
- statut de `Coup de cœur` ;
- catégories vides ou pauvres ;
- impact URL / SEO ;
- recette des liens.

### Lot R1 — Rating réel

Objectif : activer la preuve d'avis sans mensonge UX.

Contenu :

- activation / configuration des avis Odoo ;
- modération ;
- affichage conditionnel ;
- tests produit sans avis / avec avis ;
- aucun tri par note en première passe.

### Lot P1 — Producteurs

Objectif : traiter la promesse "producteur" correctement.

Contenu :

- modèle producteur officiel ;
- relation produit-producteur ;
- pages producteur ;
- donnée de confiance ;
- distinction producteur / fournisseur / partenaire.

À ne pas mélanger avec Shop Structure V1.

---

## 16. Proposition de ticket Dev exécutable

### Titre

```text
Shop CK V1 — hiérarchie boutique et promesse C-Kréyòl sur /shop
```

### Périmètre

- `/shop` ;
- impact non régressif sur `/shop/category/...` ;
- templates et SCSS existants de `dorevia_ck_theme` ;
- données et helpers existants de `dorevia_ck_marketone_content` seulement si nécessaire.

### Tâches

1. Mettre à jour `s_ck_shop_intro`.
2. Corriger le wording public `C-Kréyòl`.
3. Ajouter une phrase courte de promesse.
4. Afficher le compteur produits dans l'intro ou conserver un seul compteur toolbar.
5. Conserver le filmstrip pills natif.
6. Renommer le titre sidebar ajouté en `Affiner ma sélection`.
7. Étudier le renommage des sections `Étiquettes` et `Fourchette de prix` sans casser Odoo.
8. Cadrer la règle du slider prix.
9. Vérifier que les cards restent compactes.
10. Ne pas ajouter rating, producteur, nouvelle facette ou hero.

### Critères d'acceptation

| Critère | Attendu |
| --- | --- |
| Promesse CK | Visible avant les outils catalogue. |
| Wording | `C-Kréyòl` affiché correctement. |
| Intro | Courte, compacte, non hero. |
| Filmstrip | Natif, actif, lisible, sous l'intro. |
| Outils | Recherche, tri et filtres fonctionnels. |
| Sidebar | Perçue comme aide d'affinage. |
| Cards | Origine visible si donnée, pas de donnée inventée. |
| Achat | CTA panier toujours accessible. |
| Rating | Aucune étoile vide. |
| Producteur | Aucun producteur affiché sans modèle officiel. |
| Mobile | 390 px sans overflow horizontal. |
| Catégories | `/shop/category/...` non régressé. |

### Tests / recette attendus

- `/shop` desktop 1280 haut de page ;
- `/shop` desktop zone grille ;
- `/shop` tablette 800 ;
- `/shop` mobile 390 ;
- `/shop/category/epicerie-1` desktop ;
- recherche Shop ;
- tri ;
- filtre par tag ;
- panier rapide ;
- contrôle absence d'overflow ;
- contrôle nombre de cards avant/après.

---

## 17. Réponse Dev aux questions ouvertes

| Sujet | Réponse Dev proposée |
| --- | --- |
| Où insérer l'intro ? | Conserver l'injection actuelle dans `website_sale.products` via `s_ck_shop_intro`. |
| CTA intro ? | Optionnel, secondaire, à valider sur mobile uniquement. |
| Filmstrip ? | Réutiliser l'existant, ne pas réécrire. |
| Slider prix ? | Masquage conditionnel à cadrer ; V1 possible via `search_count`, durable via total publié. |
| Recherche Shop ? | Garder visible mais discrète ; ne pas masquer si requête active. |
| Tri ? | Garder compact, ne pas changer la logique. |
| Sidebar ? | Micro-copy via héritage/traduction ciblée, pas remplacement moteur. |
| Cards ? | Conserver la card actuelle, contrôler la hauteur. |
| Rating ? | Lot séparé, aucun rendu sans avis réel. |
| Couleurs ? | Tokens SCSS CK uniquement. |

---

## 18. Verdict Dev

La Direction UX Shop C-Kréyòl V1 est techniquement saine si elle reste une **direction** et non une refonte imposée.

Le chantier prioritaire n'est pas de reconstruire `/shop`, mais de corriger sa première lecture :

```text
Avant : catalogue Odoo amélioré.
Après : rayon boutique C-Kréyòl, clair, sobre et achetable.
```

Le lot doit rester court :

- enrichir l'intro ;
- clarifier la promesse ;
- réduire le poids des outils ;
- améliorer la micro-copy ;
- conserver les cards CK existantes ;
- préserver Odoo.

Les sujets plus ambitieux — rating réel, producteurs, rayons éditorialisés complets, modèle de confiance — doivent rester séparés.

Cap recommandé :

```text
Livrer une V1 sobre et robuste.
Ne pas chercher à tout raconter dans /shop.
Faire sentir CK avant les outils, puis laisser les produits vendre.
```

