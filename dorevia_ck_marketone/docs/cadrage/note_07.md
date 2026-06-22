# Rapport de cadrage — Header C-Kréyòl V2.1

## Header média-commerce · e-commerce d’abord · origine identifiable · sobriété créole · socle Odoo maîtrisé

| Champ                    | Valeur                                                                                       |
| ------------------------ | -------------------------------------------------------------------------------------------- |
| Projet technique         | CK Marketone                                                                                 |
| Marque publique          | C-Kréyòl                                                                                     |
| Objet                    | Cadrage du header complet : logo, recherche, actions e-commerce, navigation, pages associées |
| Version                  | V2.1 — consolidée après relecture Carole                                                     |
| Statut                   | **Amendé MOA post-Nav-1** · arbitrages actés 2026-06-21                                     |
| Références structurelles | 750g, Boutique Abbaye de Sept-Fons · **Nav-1** (PR #78 · baseline navigation)              |
| Positionnement cible     | Boutique créole média-commerce, e-commerce prioritaire                                       |
| Suite recommandée        | Ticket Dev **H1** delta · [`TICKET_DEV_LOT_H1_HEADER_CK_V2_1.md`](../design/TICKET_DEV_LOT_H1_HEADER_CK_V2_1.md) |

---

# 1. Synthèse exécutive

Le header actuel de C-Kréyòl ne porte pas encore suffisamment la marque, la logique e-commerce et la profondeur éditoriale du projet. Il reste trop proche d’un header Odoo standard : lisible, mais pas encore assez incarné, pas assez marchand, pas assez mémorable.

La cible recommandée est un **header média-commerce**, conçu pour faire comprendre immédiatement que C-Kréyòl est d’abord une boutique e-commerce de produits créoles, enrichie par les origines, les usages, les fournisseurs/producteurs, les contenus éditoriaux et l’accès professionnel.

L’objectif n’est pas de copier 750g ni de copier la boutique de l’Abbaye de Sept-Fons. Ces deux références servent à éclairer deux dimensions complémentaires :

* **750g** apporte une référence de structure : marque forte, recherche centrale, navigation claire, rubriques éditoriales assumées.
* **Sept-Fons** apporte une référence de confiance marchande : sobriété, authenticité, légitimité produit, rapport direct à une origine et à un savoir-faire.

C-Kréyòl doit combiner ces deux logiques, mais avec une priorité claire :

> C-Kréyòl est d’abord une boutique e-commerce de produits créoles, enrichie par le contenu, les origines, les usages, les fournisseurs/producteurs et l’accès professionnel.

Le header doit donc répondre à trois fonctions immédiates :

1. **Acheter** : accéder aux produits, chercher, consulter le panier, se connecter.
2. **Comprendre** : découvrir les origines, les usages, les producteurs/fournisseurs, la marque.
3. **Faire confiance** : percevoir une marque sérieuse, chaleureuse, crédible et organisée.

---

# 2. Clarification de nommage

Il faut distinguer clairement le nom public de la marque et le nom technique du projet.

## 2.1. Marque publique

La marque affichée sur le site est :

```text
C-Kréyòl
```

C’est cette forme qui doit apparaître dans :

* le header ;
* le logo ;
* les pages publiques ;
* les titres institutionnels ;
* le footer ;
* les contenus de marque.

## 2.2. Nom technique

```text
CK Marketone
```

CK Marketone désigne le projet technique, le contexte Odoo, les modules, les tickets et les artefacts de développement.

Règle de doctrine :

> Le header public ne doit afficher que “C-Kréyòl”.
> “CK Marketone” reste un nom de projet technique et ne doit pas apparaître comme marque visible pour le client final.

---

# 3. Décision de marque : graphie officielle

La graphie retenue pour la marque publique est :

```text
C-Kréyòl
```

Cette graphie est préférée à “C-Kreyol” car elle donne au nom une présence plus finalisée, plus culturelle et plus identitaire.

Les accents doivent être assumés dans le logo et dans les contenus publics.

Règle :

> La forme officielle de la marque est “C-Kréyòl”. Toute variante non accentuée doit être considérée comme une forme technique, secondaire ou de compatibilité, mais non comme la forme de marque principale.

---

# 4. Doctrine catalogue : origine et fournisseur identifiables

Le catalogue C-Kréyòl repose sur une règle de gouvernance forte :

> Aucun produit ne doit être publié dans le catalogue C-Kréyòl si son fournisseur ou producteur n’est pas clairement identifiable.

Cette règle rend légitime la promesse de sélection en V1.

Cependant, la promesse visible dans le header doit rester cohérente avec ce que le site montre effectivement au visiteur.

En V1, C-Kréyòl peut assumer :

* des produits créoles sélectionnés ;
* des origines ou fournisseurs identifiables ;
* une première sélection construite.

En revanche, la promesse d’un grand réseau de producteurs éditorialisé doit être réservée à une étape ultérieure, lorsque les fiches producteurs/fournisseurs seront visibles et suffisamment structurées.

Fournisseurs déjà identifiés ou qualifiés dans la trajectoire projet :

* SARL La Platine ;
* Sweet Manihot ;
* Farimag ;
* Comla.

Les deux premiers sont considérés comme premiers fournisseurs qualifiés dans l’esprit du projet. Les deux suivants sont dans le viseur.

## 4.1. Précaution sur l’affichage public des fournisseurs

Les fournisseurs cités ci-dessus sont des éléments de trajectoire projet. Leur affichage public dépendra :

* de leur qualification effective ;
* de leur accord ;
* de la disponibilité des contenus nécessaires ;
* de la capacité à produire une page ou une mention fiable côté front.

La doctrine reste indépendante de cette liste :

> Même si certains fournisseurs ne sont pas encore affichés publiquement, aucun produit publié ne doit exister sans fournisseur/producteur clairement identifiable côté gestion et côté information produit.

---

# 5. Promesse “Origines identifiées” : condition de preuve front

Le bandeau V1 peut utiliser la formulation :

```text
Origines identifiées
```

Cette promesse est acceptable uniquement si elle est tenue au niveau produit.

En V1, la promesse “Origines identifiées” doit être tenue au minimum par l’affichage, sur les produits concernés, d’une information identifiable :

* origine ;
* fournisseur ;
* producteur ;
* lieu de fabrication ;
* ou mention équivalente suffisamment claire.

La page “Nos producteurs” peut rester provisoire en V1, mais la preuve de l’origine ne doit pas dépendre uniquement de cette page.

Règle :

> Le bandeau peut promettre “Origines identifiées” seulement si la fiche produit ou les métadonnées visibles permettent au visiteur de comprendre d’où vient le produit ou qui le fournit.

---

# 6. Diagnostic du header actuel

Le header actuel présente trois limites principales.

## 6.1. Présence de marque insuffisante

Le logo actuel agit davantage comme un libellé typographique que comme une vraie marque. Il est trop discret, trop léger, et ne crée pas encore d’ancrage visuel fort.

À l’inverse, un logo comme 750g fonctionne comme un signe : il est massif, mémorable, immédiatement identifiable.

C-Kréyòl n’a pas besoin de reproduire cette esthétique, mais doit gagner en présence.

Objectif :

> À l’arrivée sur le site, le visiteur doit comprendre immédiatement qu’il est sur une marque construite, pas sur une boutique générique.

---

## 6.2. Priorité e-commerce encore trop faible

Le header doit dire explicitement :

* je peux chercher un produit ;
* je peux accéder au panier ;
* je peux me connecter ;
* je peux parcourir les univers ;
* je peux acheter.

La présence du panier, de la recherche et des univers produits doit être plus assumée.

---

## 6.3. Navigation éditoriale encore insuffisamment structurée

C-Kréyòl ne vend pas seulement des produits. Le projet porte aussi :

* des origines ;
* des producteurs/fournisseurs ;
* des usages ;
* des recettes ;
* une culture ;
* une relation professionnelle B2B.

Ces dimensions ne doivent pas envahir le header, mais elles doivent être accessibles de manière claire, notamment via une entrée “Découvrir”.

---

# 7. Positionnement cible du header

Le header C-Kréyòl V2.1 doit être conçu comme une table d’orientation média-commerce.

Il doit permettre de comprendre en moins de trois secondes :

* où acheter ;
* quels univers produits existent ;
* où chercher ;
* où se trouve le panier ;
* où découvrir la marque ;
* où aller si l’on est professionnel.

Doctrine cible :

> Le header C-Kréyòl V2.1 doit faire comprendre immédiatement que le site est une boutique de produits créoles, mais aussi un espace de découverte des origines, des usages, des fournisseurs/producteurs et des offres professionnelles. La priorité reste l’e-commerce : chaque composant du header doit aider soit à acheter, soit à comprendre ce qu’on achète, soit à revenir acheter.

---

# 8. Architecture recommandée

Le header cible repose sur trois strates.

```text
STRATE 0 — Bandeau service discret
Produits créoles sélectionnés · Origines identifiées · Livraison suivie

STRATE 1 — Marque / recherche / actions e-commerce
Logo C-Kréyòl     Recherche     Compte     Panier

STRATE 2 — Navigation principale V1
Tous nos produits · Épicerie créole · Soin & bien-être · Découvrir · Professionnels
```

Cette structure permet de séparer clairement :

* la réassurance ;
* l’action e-commerce ;
* l’orientation dans le catalogue et le contenu.

> **Post-Nav-1** : la Strate 2 effective sur le site est **figée** par le Lot Nav-1 (PR #78). Voir **§8 bis** et **§11 bis**. Le lot **H1** ne rouvre pas la navigation.

---

## 8 bis. État post-Nav-1 — baseline navigation figée

| Champ | Valeur |
| --- | --- |
| **Lot** | Nav-1 · Navigation CK V2 |
| **Statut** | **Clôturé GO merge QA** · 2026-06-21 |
| **Modules** | `dorevia_ck_marketone_content` **19.0.1.26.1** · `dorevia_ck_theme` **19.0.1.37.1** |
| **Références** | [`note_06.md`](./note_06.md) · [`TICKET_DEV_LOT_NAV1_NAVIGATION_CK_V2.md`](../design/TICKET_DEV_LOT_NAV1_NAVIGATION_CK_V2.md) · [`NOTE_QA_LOT_NAV1_NAVIGATION_CK_V2.md`](../design/maquette_01.2/NOTE_QA_LOT_NAV1_NAVIGATION_CK_V2.md) |

### Règle MOA actée

> **H1 ne modifie pas** `nav_sync.py`, les entrées `website.menu` commerce, le mega Découvrir, le regroupement mobile **Nos univers**, ni les règles de visibilité §7 bis Nav-1.
> Tout pivot (Professionnels top-level, libellés « Épicerie créole », dropdown simple…) = **lot Nav-1 bis** distinct.

### Navigation desktop effective (instance seed)

```text
Tous nos produits · Épicerie · Soin & Bien-être · Découvrir
```

(Entrées masquées si catégorie absente / sans produit publié — Boissons · Artisanat hors menu tant que non exploitables.)

### Navigation mobile effective

```text
Tous nos produits · Nos univers · Découvrir
```

Sous **Nos univers** : Épicerie · Soin & Bien-être (univers visibles uniquement).

### Mega Découvrir (ordre livré)

1. Producteurs & territoires → `/producteur/atelier-hauts-goyaviers`
2. Recettes & usages → `/recettes`
3. Professionnels → `/professionnels`
4. Contactez-nous → `/contactus`

**Professionnels** : sous Découvrir — **pas** top-level (arbitrage MOA Nav-1 maintenu).

### Doublon BO volontaire

Un seul arbre `website.menu` porte deux représentations des univers (racine desktop + enfants sous **Nos univers** mobile). Le front filtre par classes CSS — comportement documenté et validé QA Nav-1.

---

# 9. Strate 0 — Bandeau service discret

## 9.1. Proposition V1 recommandée

```text
Produits créoles sélectionnés · Origines identifiées · Livraison suivie
```

## 9.2. Justification fonctionnelle

Ce bandeau répond aux freins d’achat immédiats :

* Est-ce que cette boutique est sérieuse ?
* Est-ce que les produits sont sélectionnés ?
* Est-ce que l’origine ou le fournisseur sont identifiables ?
* Est-ce que je peux être livré ?

Le wording “Produits créoles sélectionnés” est cohérent avec la V1, car le catalogue ne publiera pas de produit sans fournisseur/producteur identifiable.

Le wording “Origines identifiées” renforce la confiance sans promettre encore un grand réseau éditorial de producteurs.

Le wording “Livraison suivie” apporte une réassurance e-commerce concrète.

## 9.3. Pourquoi “Accès professionnels” n’est pas dans le bandeau V1

L’accès professionnel est déjà porté par l’entrée principale “Professionnels” dans la navigation V1.

Il n’est pas répété dans le bandeau V1 afin de préserver :

* la lisibilité ;
* la priorité B2C ;
* la clarté du message de réassurance ;
* la sobriété du header.

Règle V1 :

> Le bandeau rassure. La navigation oriente.
> L’accès professionnel est donc traité dans la navigation principale, pas dans le bandeau service.

## 9.4. Formulation V2+ possible

Lorsque les fiches producteurs/fournisseurs seront visibles et suffisamment structurées, ou lorsque la stratégie B2B devra être davantage exposée, le bandeau pourra évoluer vers :

```text
Sélection de producteurs créoles · Origines identifiées · Livraison suivie
```

ou :

```text
Produits créoles sélectionnés · Livraison suivie · Accès professionnels
```

ou, en version plus ambitieuse :

```text
Producteurs créoles sélectionnés · Livraison suivie · Accès professionnels
```

Ces formulations sont réservées à V2+.

## 9.5. Justification graphique

Le bandeau doit rester discret.

Recommandations :

* hauteur réduite ;
* texte court ;
* contraste lisible ;
* fond chaud ou rouge CK maîtrisé ;
* pas d’animation ;
* pas d’effet promotion agressif.

Il ne doit pas devenir une bannière publicitaire. Il doit créer une impression de sérieux et de confiance.

## 9 bis. Bandeau header global vs trust-bar home (Option A actée MOA)

### Décision MOA — 2026-06-21

**Option A actée** : bandeau service **global** dans le header (toutes les pages), wording V1 :

```text
Produits créoles sélectionnés · Origines identifiées · Livraison suivie
```

| Zone | Rôle | Lot |
| --- | --- | --- |
| **Strate 0 header** | Réassurance transversale boutique | **H1** |
| Trust-bar home S2 (`s_ck_reassurance`) | Réassurance page d’accueil | Existant — **ne pas dupliquer le même message** sur la home |

### Règle de coexistence home

Sur `/` uniquement : le bandeau header Strate 0 et la trust-bar Section 2 **ne doivent pas répéter le même triptyque**. Arbitrage H1 :

* soit trust-bar home **allégée / reformulée** ;
* soit trust-bar home **conservée** avec rôle distinct (détail livraison, sélection…) documenté en recette.

### Implémentation technique (piste Dev H1)

Héritage QWeb `website.layout` au-dessus de `#top` · SCSS dédié · hauteur réduite · pas d’animation.

---

# 10. Strate 1 — Marque, recherche et actions e-commerce

## Structure recommandée

```text
C-Kréyòl        [ Rechercher un produit, une saveur... ]        Compte   Panier
```

Cette strate est le cœur marchand du header.

---

## 10.1. Logo C-Kréyòl

### Présence fonctionnelle

Le logo sert à :

* identifier immédiatement la marque ;
* revenir à l’accueil ;
* mémoriser le site ;
* créer la confiance ;
* affirmer que C-Kréyòl est une destination commerciale et culturelle.

Il ne doit pas être traité comme un simple texte dans le menu.

### Présence graphique

Le logo doit gagner en présence.

Recommandations :

* utiliser la graphie officielle “C-Kréyòl” ;
* renforcer le poids visuel ;
* conserver le contraste noir / rouge ;
* assumer une palette créole et caribéenne avec mesure ;
* augmenter la taille dans le header ;
* prévoir une version spécifique “header” plus lisible et plus compacte ;
* prévoir à terme une version compacte ou monogramme pour mobile et favicon.

Règle graphique :

> Le logo doit être visible en une seconde, mais ne doit pas écraser la recherche et le panier.

---

## 10.2. Barre de recherche

### Placeholder V1 recommandé

```text
Rechercher un produit, une saveur...
```

Ce placeholder reste e-commerce et réaliste. Il ne promet pas encore une recherche éditoriale complète sur les producteurs, les recettes ou les origines si le moteur Odoo V1 ne les couvre pas.

### Placeholder V2+ possible

```text
Rechercher un produit, une origine, une recette...
```

Cette version ne doit être utilisée que lorsque la recherche pourra effectivement couvrir des contenus plus larges que les produits.

### Présence fonctionnelle

En V1, la recherche doit rester centrée sur :

* les produits ;
* les catégories ;
* les termes produits utiles ;
* éventuellement les saveurs ou mots-clés présents dans les fiches produits.

Le moteur de recherche avancé couvrant producteurs, recettes, origines et contenus éditoriaux est hors périmètre V1.

### Résultats vides : vigilance UX

En V1, le moteur Odoo standard peut produire des résultats vides si l’utilisateur cherche un contenu éditorial non encore couvert, par exemple :

```text
recette colombo
```

Ce point n’est pas bloquant pour H1, mais il doit être identifié comme vigilance UX.

Backlog H1 bis possible :

> Prévoir une page de résultat vide mieux éditorialisée, orientant l’utilisateur vers les produits, catégories ou suggestions disponibles.

Exemple de message futur :

```text
Aucun produit trouvé pour “recette colombo”.
Découvrez nos produits et ingrédients créoles associés.
```

Ce traitement est hors périmètre H1, sauf décision contraire.

### Présence graphique

La barre de recherche doit être large, lisible et rassurante.

Recommandations :

* position centrale ;
* fond blanc ;
* bordure fine chaude ;
* coins arrondis modérés ;
* icône loupe visible ;
* hauteur confortable ;
* placeholder lisible ;
* focus clair au clavier.

Elle constitue l’un des points d’entrée majeurs du site.

---

## 10.3. Compte client

### Présence fonctionnelle

Le compte client est indispensable à une boutique sérieuse.

Il sert à :

* consulter les commandes ;
* gérer les adresses ;
* préparer le réachat ;
* accéder plus tard à des fonctionnalités B2B ;
* renforcer la fidélisation.

### Limite V1

En V1, le compte client reste le compte standard Odoo.

La distinction B2B / B2C est hors périmètre H1 :

* prix professionnels ;
* conditions commerciales spécifiques ;
* tableau de bord professionnel ;
* espace revendeur ;
* compte pro différencié ;
* droits ou parcours spécifiques.

Ces sujets feront l’objet d’un chantier ultérieur si nécessaire.

Règle :

> Le header H1 affiche un accès compte standard Odoo. Il ne crée pas de logique de compte professionnel spécifique.

### Présence graphique

Sur desktop :

```text
Icône + Compte
```

Sur mobile :

```text
Compte rangé dans le menu mobile
```

Le compte doit rester visible, mais moins prioritaire que le panier.

---

## 10.4. Favoris

Les favoris sont pertinents à terme, mais ne doivent pas être intégrés au header V1 si la fonctionnalité n’est pas réellement prête.

Règle :

> Le favori est affiché uniquement si la fonctionnalité est réellement exploitable côté front.

Pour la V1, les favoris sont considérés comme hors périmètre du header.

---

## 10.5. Panier

### Présence fonctionnelle

Le panier est l’élément e-commerce prioritaire.

Il doit permettre de comprendre immédiatement que le site vend réellement.

Il doit être :

* visible ;
* accessible ;
* lisible ;
* accompagné d’un compteur ;
* éventuellement accompagné du montant si Odoo le gère proprement.

### Présence graphique

Le panier doit avoir plus de poids que le compte.

Recommandations :

* icône panier ;
* compteur visible ;
* accent rouge CK ;
* zone cliquable confortable ;
* maintien en desktop et mobile.

Le panier est le principal signe de conversion dans le header.

---

# 11. Strate 2 — Navigation principale

## 11.1. Navigation V1 recommandée

```text
Tous nos produits · Épicerie créole · Soin & bien-être · Découvrir · Professionnels
```

Cette ligne est volontairement plus courte que la cible long terme.

Elle privilégie :

* l’accès direct au catalogue ;
* les deux premiers univers réellement structurants ;
* la découverte éditoriale ;
* l’accès professionnel.

## 11.2. Navigation cible V2+

```text
Tous nos produits · Épicerie créole · Soin & bien-être · Artisanat & culture · Découvrir · Professionnels
```

“Artisanat & culture” entre dans la navigation principale uniquement lorsque l’univers dispose soit :

* d’un minimum de produits publiés ;
* soit d’une page éditorialisée propre ;
* soit d’une proposition suffisamment claire pour ne pas créer une page creuse.

---

## 11.3. Tous nos produits

### Présence fonctionnelle

C’est l’entrée directe vers le catalogue complet.

Elle répond au besoin :

> Je veux voir toute la boutique.

Elle est indispensable pour les visiteurs qui ne connaissent pas encore les univers.

### Présence graphique

Position recommandée : première entrée de navigation.

Libellé recommandé :

```text
Tous nos produits
```

Ce libellé est plus explicite que “Boutique”.

---

## 11.4. Épicerie créole

### Présence fonctionnelle

C’est probablement l’univers marchand principal du lancement.

Il porte les produits les plus immédiatement compréhensibles :

* biscuits ;
* confitures ;
* condiments ;
* boissons ;
* douceurs ;
* farines ;
* préparations.

Cette entrée doit être visible dès le header.

### Présence graphique

Elle doit avoir le même poids que les autres univers produits.

Effets possibles :

* soulignement au survol ;
* accent rouge CK ;
* fond chaud discret ;
* pas d’icône obligatoire en ligne desktop.

---

## 11.5. Soin & bien-être

### Présence fonctionnelle

Cette entrée permet d’élargir la perception de C-Kréyòl au-delà de l’alimentaire.

Elle peut accueillir :

* savons ;
* soins naturels ;
* huiles ;
* cosmétiques ;
* produits bien-être.

Elle contribue à installer C-Kréyòl comme une boutique d’univers créoles, pas seulement comme une épicerie.

### Présence graphique

Même poids que “Épicerie créole”.

Elle doit être traitée comme un univers marchand à part entière.

---

## 11.6. Artisanat & culture

### Statut V1

Hors navigation principale V1.

### Statut V2+

Cette entrée sera intégrée lorsque le contenu ou le catalogue sera suffisamment mûr.

### Présence fonctionnelle cible

Elle donnera de la profondeur à C-Kréyòl.

Elle pourra porter :

* artisanat ;
* objets ;
* livres ;
* textile ;
* créations ;
* éléments culturels.

Règle :

> Une entrée visible doit pointer vers une page existante et maîtrisée. Elle ne doit jamais mener à une page vide ou générique.

### Présence graphique cible

Cette entrée doit rester élégante, sobre et premium.

Risque à éviter : le folklore ou l’effet “souvenir touristique”.

---

## 11.7. Découvrir

### Présence fonctionnelle

“Découvrir” est l’entrée média-commerce principale.

Elle regroupe les contenus qui aident à comprendre et désirer les produits.

Dropdown V1 recommandé :

```text
À propos de C-Kréyòl
Nos producteurs
Recettes & usages
Contact
```

Toutefois, “Contact” doit rester considéré comme une page de service, pas comme une rubrique éditoriale.

### Règle d’accessibilité de Contact

Sur desktop :

```text
Contact accessible via dropdown Découvrir + footer
```

Sur mobile :

```text
Contact accessible directement dans le menu mobile + footer
```

Cette organisation permet de préserver une navigation desktop sobre tout en rendant le contact plus accessible sur mobile, où le footer est plus éloigné.

### Rubriques hors V1

Les rubriques suivantes sont réservées à V2+ :

```text
Nos engagements
Journal CK
Communauté
Forum
Régie pub maison
```

### Présence graphique

“Découvrir” peut ouvrir un dropdown éditorial simple.

En V1, il est recommandé de rester sobre, sans méga-menu complexe.

---

## 11.8. Professionnels

### Présence fonctionnelle

“Professionnels” doit rester visible dans le header principal.

Cette entrée sert à qualifier :

* revendeurs ;
* épiceries ;
* boutiques ;
* CHR ;
* distributeurs ;
* partenaires.

Elle porte une dimension stratégique du modèle C-Kréyòl.

Elle ne doit pas être noyée uniquement dans “Découvrir”.

### Limite V1

En V1, “Professionnels” mène à une page ou un formulaire de qualification.

Il ne crée pas automatiquement :

* compte pro spécifique ;
* prix B2B visibles ;
* portail revendeur ;
* conditions commerciales automatisées ;
* espace pro connecté.

Ces sujets sont hors périmètre H1.

### Présence graphique

Position recommandée : dernière entrée de navigation.

Traitement recommandé :

* poids visuel secondaire ;
* style différencié discret ;
* pas de gros CTA ;
* pas plus fort que les univers produits ;
* ne doit pas faire penser que le site est réservé aux professionnels.

Exemples de traitement :

* texte légèrement plus fin ;
* séparateur visuel ;
* contour discret ;
* accent rouge CK au survol uniquement.

Règle :

> “Professionnels” doit être visible, mais ne doit pas concurrencer la navigation B2C ni le panier.

## 11 bis. Navigation Strate 2 — réconciliation Nav-1 (MOA actée)

Le §11 ci-dessus décrit la **vision initiale** du cadrage V2.1. Après livraison **Nav-1**, la MOA acte la **baseline figée** suivante pour H1 et au-delà :

| Sujet | Vision initiale `note_07` §11 | **Baseline Nav-1 actée** |
| --- | --- | --- |
| Desktop commerce | Épicerie créole · Soin & bien-être · **Professionnels** top-level | **Épicerie** · **Soin & Bien-être** · **pas** Professionnels top-level |
| Découvrir | Dropdown simple V1 | **Mega-menu** natif CE |
| Contact | `/contact` · menu mobile direct | **`/contactus`** · **Contactez-nous** sous Découvrir |
| Recettes | `/recettes-usages` | **`/recettes`** |
| Producteurs | Hub `/producteurs` | Fiche pilote + hub **H2** |
| Mobile univers | Liste §13.2 initiale | **Nos univers** accordéon (Nav-1) |
| Mobile Contact | Entrée directe drawer | **Découvrir + footer** (Nav-1) |

### Navigation desktop H1+ (référence)

```text
Tous nos produits · Épicerie · Soin & Bien-être · Découvrir
```

### Navigation mobile H1+ (référence)

```text
Tous nos produits · Nos univers · Découvrir
```

### Écart libellés header ↔ home S4

| Zone | Libellé |
| --- | --- |
| Header Nav-1 | Épicerie · Soin & Bien-être |
| Home S4 cards | Épicerie créole · Soin & bien-être · Artisanat & culture |

**Accepté MOA** — pas de modification S4 dans H1.

### Lot Nav-1 bis (hors H1)

Tout retour à la navigation initiale §11 (Professionnels top-level, dropdown simple, libellés « Épicerie créole »…) fera l’objet d’un **ticket séparé** avec recette QA dédiée.

---

# 12. Pages provisoires et règle de contenu

## 12.1. Règle générale

Toute entrée visible dans le header doit pointer vers une page existante.

Si le contenu final n’est pas prêt, la page doit être créée avec :

* un titre clair ;
* une phrase d’intention ;
* un court contenu d’attente qualitatif ;
* un CTA utile ;
* aucun contenu générique Odoo laissé visible.

Règle MOA :

> Page stratégique pas prête = page provisoire propre.
> Fonctionnalité pas prête = pas affichée.

---

## 12.2. Pages V0 — URLs instance (post-Nav-1)

| Page | URL **instance** | Statut seed | Lot |
| --- | --- | --- | --- |
| À propos de C-Kréyòl | `/a-propos` | ✅ Publiée · `ck-about-page` | H2 spot check |
| Recettes & usages | `/recettes` | ✅ Publiée · `ck-recipes-page` | Nav-1 mega |
| Professionnels | `/professionnels` | ✅ Publiée · `ck-pro-page` | Nav-1 mega |
| Contact | `/contactus` | ✅ Publiée · `ck-contact-page` | Nav-1 mega |
| Producteurs & territoires (pilote) | `/producteur/atelier-hauts-goyaviers` | ✅ Fiche producteur | Nav-1 mega |
| Hub Nos producteurs | `/producteurs` | ⏳ **H2** — page provisoire MOA §12.3 | **H2** |

**Règle URLs** : ne pas migrer `/contactus` → `/contact` ni `/recettes` → `/recettes-usages` sans redirection 301 et arbitrage MOA.

### Tableau historique (vision initiale cadrage)

| Page | URL initiale `note_07` |
| --- | --- |
| Nos producteurs | `/producteurs` |
| Recettes & usages | `/recettes-usages` |
| Contact | `/contact` |

---

## 12.3. Exemple de contenu provisoire

```text
Nos producteurs

Cette page présentera bientôt les producteurs, fournisseurs, artisans et partenaires qui donnent vie aux produits proposés sur C-Kréyòl.

Chaque produit publié dans notre catalogue est associé à une origine ou à un fournisseur clairement identifiable.

En attendant, découvrez notre première sélection de produits créoles en boutique.

[Découvrir les produits]
```

---

# 13. Responsive mobile

Le header mobile ne doit pas reproduire toute la complexité du desktop.

## 13.1. Structure mobile retenue

```text
Menu     C-Kréyòl     Recherche     Panier
```

Cette structure est retenue pour H1.

Justification :

* menu à gauche : convention e-commerce lisible ;
* logo au centre : présence de marque ;
* recherche à droite : accès rapide ;
* panier à droite : conversion immédiate ;
* compte client rangé dans le menu mobile.

## 13.2. Menu mobile recommandé

```text
Tous nos produits
Nos univers
  - Épicerie créole
  - Soin & bien-être
Découvrir
  - À propos de C-Kréyòl
  - Producteurs
  - Recettes & usages
Professionnels
Compte
Contact
```

“Artisanat & culture” sera ajouté dans “Nos univers” lorsque la rubrique sera réellement prête.

## 13.3. Justification fonctionnelle

Sur mobile, les priorités sont :

* identifier la marque ;
* chercher ;
* accéder au panier ;
* ouvrir le menu ;
* acheter rapidement.

La navigation secondaire doit être rangée dans un menu clair.

## 13.4. Justification graphique

Le mobile doit rester léger.

À éviter :

* header trop haut ;
* logo trop petit ;
* trop d’icônes ;
* menus imbriqués trop profonds ;
* surcharges visuelles.

---

# 14. Direction graphique

## 14.1. Ambiance cible

Le header doit exprimer :

* boutique sérieuse ;
* chaleur créole ;
* premium accessible ;
* confiance ;
* clarté ;
* désir d’achat.

Il ne doit pas exprimer :

* folklore ;
* surcharge ;
* menu Odoo standard ;
* média pur ;
* marketplace froide ;
* boutique promotionnelle agressive.

---

## 14.2. Palette recommandée

La palette rouge / jaune / vert peut être utilisée comme évocation culturelle créole et caribéenne, avec une résonance guadeloupéenne assumée.

Elle ne doit pas être présentée comme reproduction littérale d’un drapeau officiel.

Doctrine couleur :

> Les couleurs rouge, jaune et vert évoquent la culture créole et caribéenne au sens large. Elles doivent être intégrées avec sobriété dans un système de marque e-commerce, sans effet décoratif excessif.

Recommandations :

* fond principal : blanc chaud / crème léger ;
* texte : brun profond ou noir doux ;
* accent principal : rouge CK ;
* accent secondaire : jaune / or ou vert, avec usage maîtrisé ;
* panier / CTA : rouge CK ;
* bandeau service : fond chaud ou rouge CK sobre.

---

## 14.3. Typographie et logo

La version logo doit être renforcée.

Recommandations :

* graphie officielle : C-Kréyòl ;
* poids visuel plus fort ;
* accents lisibles ;
* contraste noir / rouge ;
* version header dédiée ;
* version compacte à prévoir.

Objectif :

> Le logo doit devenir une ancre visuelle, pas un simple mot dans le header.

---

# 15. Méthode technique recommandée

Le header doit rester intégré à l’architecture Odoo 19 CE.

Approche recommandée :

* thème Odoo ;
* héritages QWeb maîtrisés ;
* SCSS propre ;
* classes CSS dédiées ;
* pas de front parallèle ;
* pas de header from scratch déconnecté du socle ;
* pas de HTML brut non maintenable ;
* respect de la navigation Odoo autant que possible.

Règle :

> L’objectif est d’obtenir une perception de marque plus forte dans le cadre du thème Odoo, pas de sortir du socle Odoo ni de créer une dette technique inutile.

---

# 16. Périmètre du chantier

Ce cadrage concerne le header de l’univers Boutique C-Kréyòl et sa dimension éditoriale associée.

Sont dans le périmètre :

* marque ;
* recherche ;
* compte ;
* panier ;
* navigation produits ;
* entrée Découvrir ;
* entrée Professionnels ;
* pages V0 liées au header.

Sont hors périmètre V1 :

* communauté ;
* forum ;
* régie pub maison ;
* blog complet ;
* journal éditorial complet ;
* moteur de recherche avancé ;
* méga-menu complexe ;
* refonte shop ;
* refonte home ;
* refonte fiche produit ;
* header from scratch hors Odoo ;
* univers Artisanat & culture si contenu/catalogue insuffisant ;
* compte professionnel spécifique ;
* prix B2B visibles ou automatisés ;
* favoris si fonctionnalité non prête ;
* page de résultats de recherche vide customisée, sauf arbitrage spécifique.

Note :

> Les univers Communautaire et Régie pub maison pourront disposer de leurs propres structures de navigation ultérieurement. Ils ne doivent pas être embarqués dans ce chantier Header V2.1 Boutique.

---

# 17. Critères de réussite MOA

## 17.1. Desktop 1280 px

Le header est réussi si l’utilisateur comprend en moins de trois secondes :

* où acheter ;
* quels sont les grands univers produits ;
* où chercher ;
* où accéder au panier ;
* où découvrir la marque ;
* où aller en tant que professionnel.

## 17.2. Mobile 390 px

Le header est réussi si :

* le logo est lisible ;
* le panier est accessible ;
* la recherche est accessible ;
* le menu est clair ;
* les univers sont regroupés proprement ;
* aucune entrée ne mène vers une page vide.

## 17.3. Qualité graphique

Le header est réussi si :

* il porte mieux la marque C-Kréyòl ;
* il donne envie d’acheter ;
* il inspire confiance ;
* il reste sobre ;
* il reste maintenable ;
* il ne donne pas l’impression d’un menu Odoo générique.

Ce dernier point ne signifie pas qu’il faut sortir du socle Odoo. Il signifie que l’habillage, la hiérarchie et la présence de marque doivent être suffisamment travaillés pour produire une expérience propre à C-Kréyòl.

---

# 18. Découpage recommandé en lots

## 18.1. Lot H1 — Structure header média-commerce

Objectif : poser le header cible V1.

Périmètre :

* bandeau service ;
* logo C-Kréyòl ;
* barre de recherche ;
* compte ;
* panier ;
* navigation principale V1 ;
* responsive mobile.

Hors périmètre :

* moteur de recherche avancé ;
* blog complet ;
* forum ;
* régie pub ;
* méga-menu complexe ;
* refonte shop ;
* refonte home ;
* refonte fiche produit ;
* favoris si fonctionnalité non prête ;
* Artisanat & culture si contenu non prêt ;
* compte professionnel spécifique ;
* prix B2B automatisés ;
* page de résultats vide customisée.

## 18.1 bis. Lot H1 — périmètre delta (MOA acté post-Nav-1)

Le lot **H1** ne reprend **pas** la navigation Strate 2 (Nav-1 figé). Il porte le **delta** suivant :

| Composant | Inclus H1 | Hors H1 |
| --- | --- | --- |
| **Strate 0** — bandeau global Option A | ✅ | — |
| **Strate 1** — logo **C-Kréyòl** renforcé | ✅ | — |
| **Strate 1** — recherche centrale + placeholder V1 | ✅ | Moteur multi-contenus |
| **Strate 1** — compte · panier (poids visuel) | ✅ | Compte pro · favoris |
| **Mobile** — chrome `Menu · C-Kréyòl · Recherche · Panier` | ✅ | Contenu drawer Nav-1 |
| **Strate 2** — navigation · mega · sync menus | ❌ | **Nav-1 baseline** |
| Refonte shop / home / fiche produit | ❌ | Tickets distincts |
| Hub `/producteurs` | ❌ | **H2** |
| Page résultats recherche vide custom | ❌ | **H1 bis** backlog |

**Ticket Dev** : [`TICKET_DEV_LOT_H1_HEADER_CK_V2_1.md`](../design/TICKET_DEV_LOT_H1_HEADER_CK_V2_1.md).

---

## 18.2. Lot H2 — Pages provisoires liées au header

Objectif : éviter les liens vides.

Pages à créer ou vérifier :

* À propos de C-Kréyòl ;
* Nos producteurs ;
* Recettes & usages ;
* Professionnels ;
* Contact.

Chaque page doit avoir :

* titre ;
* intention ;
* contenu provisoire propre ;
* CTA utile.

---

## 18.3. Lot H3 — Enrichissement navigation / dropdown

Objectif : enrichir “Découvrir” et éventuellement les univers.

Périmètre possible :

* dropdown simple ;
* structuration éditoriale ;
* liens vers producteurs ;
* liens vers recettes et usages ;
* futures pages d’engagement ;
* éventuel ajout d’Artisanat & culture si le contenu est prêt.

Ce lot ne doit venir qu’après stabilisation de H1 et H2.

---

## 18.4. Backlog H1 bis — UX recherche

Objectif éventuel : améliorer le traitement des résultats vides.

Périmètre possible :

* page zéro résultat personnalisée ;
* suggestions vers catégories ;
* suggestions vers produits associés ;
* message éditorial plus humain.

Ce backlog n’est pas inclus dans H1.

---

# 19. Décisions MOA à acter

> **Historique** — décisions initiales du cadrage V2.1. Les arbitrages **actés post-Nav-1** priment : voir **§19 bis**.

Avant rédaction du ticket Dev H1, les décisions suivantes devaient être confirmées :

1. Confirmer la graphie officielle : **C-Kréyòl**.
2. Confirmer la distinction : C-Kréyòl = marque publique ; CK Marketone = projet technique.
3. Valider la structure en trois strates.
4. Valider le bandeau V1 :
   `Produits créoles sélectionnés · Origines identifiées · Livraison suivie`
5. Confirmer que l’accès professionnel est porté par la navigation, pas par le bandeau V1.
6. Valider la navigation V1 :
   `Tous nos produits · Épicerie créole · Soin & bien-être · Découvrir · Professionnels`
7. Confirmer qu’Artisanat & culture est hors navigation V1 sauf contenu/catalogue suffisant.
8. Confirmer que Favoris est hors V1 si la fonctionnalité n’est pas prête.
9. Valider le placeholder de recherche V1 :
   `Rechercher un produit, une saveur...`
10. Confirmer que la recherche avancée origine/recette/producteur est hors H1.
11. Valider les pages V0 à créer.
12. Valider la règle Contact : desktop via dropdown + footer ; mobile via menu direct + footer.
13. Valider que le compte client reste standard Odoo en V1.
14. Valider que le B2B avancé est hors H1.
15. Valider que le chantier reste dans l’architecture thème Odoo 19 CE.
16. Confirmer que Communauté, Forum et Régie pub maison sont hors périmètre V1.
17. Valider la structure mobile :
    `Menu · C-Kréyòl · Recherche · Panier`
18. Valider que la page de résultat vide customisée est backlog H1 bis, non H1.

---

## 19 bis. Décisions MOA actées (post-Nav-1 · 2026-06-21)

Référence : [`note_07_reponse_moa.md`](./note_07_reponse_moa.md) · retour Dev [`note_07_retour_dev.md`](./note_07_retour_dev.md).

| # | Décision | Statut MOA |
| ---: | --- | --- |
| 1 | GO cadrage Header C-Kréyòl V2.1 | ✅ Acté |
| 2 | **H1 = delta** : Strate 0 + Strate 1 + chrome mobile | ✅ Acté |
| 3 | **Nav-1 = baseline figée** navigation Strate 2 | ✅ Acté |
| 4 | Professionnels **sous Découvrir** (pas top-level) | ✅ Acté |
| 5 | Libellés menu : **Épicerie** · **Soin & Bien-être** | ✅ Acté |
| 6 | Mobile : **Nos univers** conservé | ✅ Acté |
| 7 | Graphie publique header : **C-Kréyòl** + recette typo **ò** | ✅ Acté |
| 8 | Recherche centrale H1 · placeholder V1 · **produits only** | ✅ Acté |
| 9 | Bandeau global Option A (wording §9.1) | ✅ Acté |
| 10 | URLs : **`/contactus`** · **`/recettes`** conservées | ✅ Acté |
| 11 | Hub **`/producteurs`** | ⏳ **H2** |
| 12 | Contact mobile direct drawer | ❌ — Nav-1 (Découvrir + footer) |
| 13 | Pivot Nav-1 bis éventuel | Lot séparé |
| 14 | Doctrine origine/fournisseur §4–5 | ✅ — implémentation hors H1 |

**Suite** : ticket Dev [`TICKET_DEV_LOT_H1_HEADER_CK_V2_1.md`](../design/TICKET_DEV_LOT_H1_HEADER_CK_V2_1.md) — **pas d’exécution H1 avant relecture ticket**.

---

# 20. Recommandation finale

La direction recommandée est :

> Header C-Kréyòl V2.1 = header média-commerce premium, e-commerce d’abord, enrichi par l’origine identifiable, la confiance fournisseur/producteur et la culture créole.

La structure cible V1 :

```text
Bandeau service
→ rassurer

Logo + recherche + compte + panier
→ vendre

Navigation produits + découvrir + professionnels
→ orienter
```

La ligne de navigation V1 :

```text
Tous nos produits · Épicerie créole · Soin & bien-être · Découvrir · Professionnels
```

La phrase de cadrage finale :

> Le header C-Kréyòl V2.1 doit combiner la clarté d’orientation d’un média culinaire comme 750g avec la sobriété et la légitimité marchande d’une boutique de producteur comme Sept-Fons. La priorité reste e-commerce : recherche, panier, compte, univers produits et accès boutique. Mais le header doit aussi installer la confiance : produits sélectionnés, origines identifiées, fournisseurs/producteurs traçables, livraison et accès professionnel.

---

# 21. Verdict proposé

Le chantier Header C-Kréyòl V2.1 est pertinent et prioritaire.

Il touche à la colonne vertébrale du site : marque, navigation, recherche, conversion, confiance et accès professionnel.

Il doit être traité comme un chantier MOA structurant, puis découpé en tickets Dev courts et recettables.

Verdict recommandé :

```text
GO cadrage Header C-Kréyòl V2.1
Puis rédaction d’un ticket Dev H1 strictement borné
```
