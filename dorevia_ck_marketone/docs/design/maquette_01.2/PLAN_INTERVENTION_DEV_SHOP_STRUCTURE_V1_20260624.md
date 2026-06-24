# Plan d'intervention Dev — Shop Structure V1 sobre

| Champ | Valeur |
| --- | --- |
| Projet | `dorevia_ck_marketone` |
| Date | 2026-06-24 |
| Statut | Plan d'intervention Dev · prêt pour exécution après GO |
| Lot | S1 — Shop Structure V1 sobre |
| Périmètre principal | `/shop` |
| Périmètre de non-régression | `/shop/category/...`, notamment `/shop/category/epicerie-1` |
| Modules concernés | `dorevia_ck_theme` principalement, `dorevia_ck_marketone_content` seulement si nécessaire |
| Objectif | Faire lire `/shop` comme un rayon boutique C-Kréyòl, sans réécrire Odoo |

---

## 1. Mandat donné au Dev

Mettre en œuvre un premier lot sobre et maîtrisé sur la page `/shop`.

L'objectif n'est pas de refaire la boutique, ni de créer une nouvelle expérience hors Odoo. L'objectif est de corriger la première lecture de la page :

```text
Avant : catalogue Odoo amélioré.
Après : rayon boutique C-Kréyòl, clair, sobre et achetable.
```

Le Dev doit donc renforcer la promesse CK en haut de page, tout en conservant les mécanismes natifs Odoo :

- recherche ;
- tri ;
- filtres ;
- URLs catalogue ;
- pages catégories ;
- panier rapide ;
- cards produit ;
- responsive mobile.

Doctrine technique :

```text
Odoo reste le moteur.
CK devient la lecture commerciale.
```

---

## 2. Documents de référence à lire avant intervention

Le Dev doit lire ces documents avant de coder :

1. `RAPPORT_RETOUR_DEV_HOME_SHOP_CK_20260624.md`
2. `RETOUR_DEV_DIRECTION_UX_SHOP_CK_V1_20260624.md`
3. `NOTE_CONSOLIDATION_GIT_CK_20260624.md`

Lecture attendue :

- comprendre l'intention CK : sélection, origine, confiance, achat rapide ;
- comprendre ce qui est déjà codé ;
- comprendre ce qui est volontairement hors lot ;
- éviter de repartir sur une refonte large.

---

## 3. Objectif produit du lot

La page `/shop` doit faire comprendre immédiatement :

```text
C-Kréyòl propose une sélection de produits créoles,
aux origines identifiées,
dans une expérience d'achat simple et rassurante.
```

La page ne doit plus se lire en premier comme :

```text
Filtres · recherche · tri · grille produits
```

Elle doit se lire comme :

```text
Promesse CK · catégories de découverte · outils secondaires · produits achetables
```

---

## 4. Périmètre autorisé

### 4.1 Intro Shop

Actions attendues :

- corriger le wording public en `Boutique C-Kréyòl` ;
- ajouter une phrase courte de promesse ;
- afficher le nombre de produits sélectionnés si cela ne crée pas de doublon avec la toolbar ;
- conserver une intro compacte ;
- ne pas créer de hero marketing.

Texte cible proposé :

```text
Boutique C-Kréyòl

Produits créoles sélectionnés, aux origines identifiées.

7 produits sélectionnés
```

Le compteur doit être dynamique si possible. Si la donnée disponible est `search_count`, elle peut être utilisée, mais il faut éviter de l'afficher deux fois de manière redondante.

### 4.2 Filmstrip catégories

Actions attendues :

- conserver le filmstrip natif Odoo en mode pills ;
- ne pas recréer un composant custom ;
- vérifier que `Tous` reste la première entrée ;
- vérifier l'état actif sur `/shop/category/...` ;
- conserver les URLs natives.

Point de vigilance :

`Coup de cœur` ne doit apparaître comme entrée de navigation que si c'est une vraie catégorie publique alimentée. Sinon, cela reste un badge ou une logique de curation, pas une porte d'entrée catalogue.

### 4.3 Barre catalogue

Actions attendues :

- conserver recherche et tri ;
- réduire leur poids visuel si nécessaire ;
- ne pas casser les paramètres d'URL ;
- ne pas masquer la recherche si une recherche est active ;
- ne pas ajouter de nouvelle logique de tri.

La barre catalogue doit devenir une zone d'outils secondaires, pas le premier signal de la page.

### 4.4 Sidebar filtres

Actions attendues :

- conserver les facettes natives Odoo ;
- conserver les accordéons et états actifs ;
- renommer le titre ajouté `Filtres` en `Affiner ma sélection` ;
- étudier prudemment le renommage de sections :
  - `Étiquettes` → `Origines & préférences` ;
  - `Fourchette de prix` → `Budget`.

Méthode recommandée :

- traduction ou héritage ciblé ;
- pas de remplacement massif du moteur facettes ;
- pas de modification de données BO si le libellé a un usage technique.

### 4.5 Cards produit

Actions attendues :

- conserver la card actuelle ;
- vérifier que l'origine reste visible quand la donnée existe ;
- vérifier que le prix principal reste lisible ;
- vérifier que le CTA panier reste accessible ;
- vérifier que la card reste compacte ;
- ne pas ajouter de producteur ;
- ne pas ajouter d'étoiles vides.

Le Dev peut ajuster légèrement les espacements si la recette montre une card trop haute, mais il ne doit pas relancer une refonte card.

---

## 5. Hors périmètre explicite

Ne pas traiter dans ce lot :

- Home page ;
- fiche produit ;
- modèle producteur ;
- affichage producteur en card ;
- pages producteurs dynamiques ;
- rating complet ;
- tri par note ;
- refonte du moteur de facettes ;
- nouvelle facette custom ;
- nouveau contrôleur catalogue lourd ;
- pagination ou bouton "voir plus" ;
- rayons éditorialisés complets ;
- promesse logistique non validée ;
- textures, motifs ou décoration créole artificielle.

Règle simple :

```text
Si le changement exige de réinventer une mécanique Odoo,
il sort du Lot S1.
```

---

## 6. Séquence d'intervention recommandée

### Étape 0 — Préparation

Avant toute modification :

1. Vérifier la branche de travail.
2. Vérifier que le worktree est propre ou identifier les fichiers hors périmètre.
3. Relire les documents de référence.
4. Inspecter les vues et SCSS existants :
   - `views/snippets/ck_snippet_shop_intro.xml` ;
   - `views/website_sale_shop_compose.xml` ;
   - `views/website_sale_toolbar_count.xml` ;
   - `views/website_sale_sidebar.xml` ;
   - `views/website_sale_product_card.xml` ;
   - `static/src/scss/website_sale.scss` ;
   - `static/src/scss/product_card.scss`.

### Étape 1 — Intro Shop

1. Modifier le snippet existant, sans changer son point d'injection.
2. Corriger `C-Kreyol` en `C-Kréyòl`.
3. Ajouter la phrase courte de promesse.
4. Décider où afficher le compteur :
   - intro ;
   - ou toolbar ;
   - mais éviter un doublon visible.

Critère de réussite :

```text
La promesse CK est visible avant les outils catalogue.
```

### Étape 2 — Filmstrip et barre catalogue

1. Conserver le filmstrip pills natif.
2. Vérifier la lisibilité de l'état actif.
3. Vérifier que la barre catalogue reste compacte.
4. Ne pas changer le comportement de recherche et tri.

Critère de réussite :

```text
Le filmstrip se lit comme navigation de découverte,
la recherche et le tri comme outils secondaires.
```

### Étape 3 — Sidebar

1. Renommer le titre CK ajouté en `Affiner ma sélection`.
2. Tester la sidebar desktop.
3. Tester le comportement mobile / offcanvas si applicable.
4. Étudier le renommage des sections sans fragiliser Odoo.

Critère de réussite :

```text
Les filtres restent utilisables et ne deviennent pas le premier signal visuel.
```

### Étape 4 — Cards

1. Vérifier les cards après les changements de haut de page.
2. Contrôler la hauteur globale.
3. Contrôler l'origine conditionnelle.
4. Contrôler le CTA panier.
5. Ne modifier les cards que si une régression visuelle est constatée.

Critère de réussite :

```text
Les cards restent denses, lisibles et directement achetables.
```

### Étape 5 — Vérifications fonctionnelles

Contrôler :

- `/shop` ;
- `/shop/category/epicerie-1` ;
- recherche Shop ;
- tri ;
- filtre par tag ;
- panier rapide ;
- responsive 1280 / 800 / 390 ;
- absence d'overflow horizontal ;
- nombre de cards avant/après.

---

## 7. Règle du slider prix

Le document UX recommande :

```text
Masquer le slider prix tant que le catalogue total publié est inférieur à 15 produits,
sauf si un filtre prix est déjà actif dans l'URL.
```

Pour le Lot S1, le Dev doit seulement cadrer cette règle et proposer l'option retenue.

Options possibles :

| Option | Description | Décision recommandée |
| --- | --- | --- |
| A | Masquage CSS simple | Trop approximatif, à éviter si présenté comme règle métier. |
| B | Masquage via `search_count < 15` | Acceptable pour V1 rapide, à documenter comme approximation. |
| C | Total publié indépendant des filtres | Plus propre, mais peut justifier un mini-lot séparé. |

Garde-fou :

Le slider doit rester visible si un filtre prix est déjà actif, afin que l'utilisateur puisse comprendre et retirer son filtre.

Statut recommandé :

```text
À instruire pendant S1, à implémenter seulement si l'option retenue reste simple.
```

---

## 8. Livrables attendus

### 8.1 Code

Livrer uniquement les modifications nécessaires au Lot S1.

Le code doit rester :

- lisible ;
- réversible ;
- localisé ;
- conforme aux patterns existants ;
- sans réécriture globale de `website_sale`.

### 8.2 Captures

Produire les captures suivantes :

| Vue | Attendu |
| --- | --- |
| `/shop` desktop 1280 haut de page | Intro + filmstrip + outils visibles |
| `/shop` desktop 1280 zone grille | Cards + sidebar + CTA |
| `/shop/category/epicerie-1` desktop | Non-régression catégorie |
| `/shop` tablette 800 | Pas d'overflow, lecture propre |
| `/shop` mobile 390 | Intro compacte, cards lisibles, CTA accessible |

### 8.3 Note de recette

Créer une note courte indiquant :

- ce qui a été modifié ;
- ce qui a été volontairement laissé hors périmètre ;
- les captures produites ;
- les tests effectués ;
- les limites restantes ;
- les arbitrages demandés à la MOA.

---

## 9. Critères d'acceptation

| Critère | Attendu |
| --- | --- |
| Promesse CK | Visible avant les outils catalogue. |
| Wording public | `C-Kréyòl` correctement écrit. |
| Intro | Courte, compacte, non hero. |
| Filmstrip | Natif, actif, lisible, sous l'intro. |
| Recherche | Fonctionnelle, non cassée, URL conservée. |
| Tri | Fonctionnel, non réécrit. |
| Filtres | Facettes natives conservées. |
| Sidebar | Perçue comme aide d'affinage. |
| Cards | Compactes, lisibles, non régressées. |
| Origine | Visible si donnée disponible, jamais inventée. |
| Producteur | Aucun affichage producteur en V1. |
| Rating | Aucune étoile vide. |
| Achat rapide | CTA panier accessible et fonctionnel. |
| Mobile | Aucun overflow horizontal en 390 px. |
| Catégories | `/shop/category/...` non régressé. |
| Données | Pas de fausse promesse logistique ou producteur. |

---

## 10. Tests recommandés

### 10.1 Tests machine

À minima :

```text
/shop répond 200
/shop/category/epicerie-1 répond 200
aucun overflow horizontal en 1280 / 800 / 390
nombre de cards inchangé
filtre tag utilisable
tri utilisable
recherche utilisable
panier rapide fonctionnel
```

### 10.2 Tests Odoo

Lancer les tests ciblés existants si disponibles :

- tests cards shop ;
- tests origine produit ;
- tests composition header/shop si impact indirect ;
- tests nav shop si le filmstrip ou les catégories sont touchés.

### 10.3 Recette visuelle

Comparer avant/après :

- hauteur d'intro ;
- visibilité de la promesse ;
- lisibilité du filmstrip ;
- poids de la toolbar ;
- densité des cards ;
- comportement mobile.

---

## 11. Points d'arbitrage MOA à remonter si nécessaire

Le Dev doit remonter ces sujets sans les implémenter en douce :

| Sujet | Question |
| --- | --- |
| Compteur | Doit-il être dans l'intro, dans la toolbar, ou les deux avec hiérarchie différente ? |
| Slider prix | Option B rapide ou option C durable ? |
| Sidebar | Peut-on renommer les sections natives si cela implique traduction globale ? |
| `Soin & bien-être` | Correction BO/migration ou affichage spécifique front ? |
| `Coup de cœur` | Catégorie publique réelle ou simple logique badge/curation ? |
| CTA intro | Utile en mobile ou inutile en V1 ? |

---

## 12. Découpage après Lot S1

À ne pas lancer en même temps que S1, mais à prévoir ensuite :

| Lot | Sujet |
| --- | --- |
| S2 | Règle durable slider prix / outils catalogue conditionnels |
| S3 | Alignement données catégories publiques |
| R1 | Rating réel et flux d'avis Odoo |
| P1 | Modèle producteur officiel |
| P2B | Rayons éditorialisés complets |
| H2 | Direction UX Home V2 |

---

## 13. Formulation courte de GO Dev

```text
GO Dev sur le Lot S1 — Shop Structure V1 sobre.

Merci d'améliorer la première lecture de /shop afin que la page se lise comme
un rayon boutique C-Kréyòl, sans réécrire website_sale.

Périmètre : intro Shop, filmstrip natif, barre catalogue, sidebar, vérification cards.

Garde-fous : conserver recherche, tri, filtres, URLs, panier rapide et pages catégories.
Ne pas traiter rating complet, producteur, Home, fiche produit, refonte facettes ou rayons éditorialisés complets.

Livrables : code léger, captures 1280 / 800 / 390, contrôle /shop et /shop/category/epicerie-1, note de recette.
```

---

## 14. Verdict

Le Lot S1 est prêt à être confié au Dev.

Le périmètre est assez clair pour coder, mais assez borné pour éviter l'effet tunnel.

Le succès du lot ne se mesurera pas à la quantité de changements, mais à une lecture plus juste :

```text
Sélection.
Origine.
Confiance.
Achat rapide.
Odoo intact.
```

