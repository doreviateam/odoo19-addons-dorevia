# Spécification détaillée — Header & Mega-menus C-Kréyòl V2.2

| Champ | Valeur |
| --- | --- |
| Projet | `dorevia_ck_marketone` |
| Objet | Architecture header + navigation + mega-menus |
| Version | V2.2 consolidée |
| Statut | Architecture MOA figée — prêt découpage Dev |

---

## 1. Objet du document

Ce document formalise l’architecture visuelle et fonctionnelle du header C-Kréyòl V2.2, ainsi que la grammaire des mega-menus associés à la navigation principale.

L’objectif est de donner à C-Kréyòl une structure de header professionnelle, immédiatement compréhensible, efficace en e-commerce, tout en conservant l’identité propre de la marque.

Le header doit permettre à un visiteur de comprendre en quelques secondes :

* qu’il se trouve sur C-Kréyòl ;
* qu’il s’agit d’une boutique / épicerie créole ;
* qu’il peut chercher un produit ;
* qu’il peut acheter ;
* que les produits sont sélectionnés, identifiés et expédiés sérieusement ;
* que l’offre est structurée par familles, origines, producteurs et sélections commerciales.

---

## 2. Architecture générale du Header CK V2.2

Le header C-Kréyòl V2.2 est structuré en trois niveaux visibles.

```text
Niveau 1 — Bandeau promesses
Niveau 2 — Barre fonctionnelle
Niveau 3 — Navigation principale
```

Chaque niveau a une fonction propre.

| Niveau | Fonction principale | Rôle |
| --- | --- | --- |
| Niveau 1 | Confiance | Installer immédiatement la promesse CK |
| Niveau 2 | Fonction e-commerce | Identifier, chercher, se connecter, accéder au panier |
| Niveau 3 | Orientation catalogue | Présenter les rayons, collections et accès stratégiques |

---

## 3. Niveau 1 — Bandeau promesses

### 3.1 Contenu cible

```text
Produits sélectionnés · Origines identifiées · Livraison suivie · Stocké/expédié depuis Nantes
```

### 3.2 Rôle

Le bandeau promesses doit rassurer immédiatement le visiteur.

Il porte les notions suivantes :

* sélection ;
* origine / traçabilité ;
* sérieux logistique ;
* expédition depuis Nantes ;
* promesse e-commerce fiable.

### 3.3 Comportement

| Situation | Comportement |
| --- | --- |
| Chargement desktop | Visible |
| Scroll desktop | Disparaît pour libérer de la hauteur |
| Mobile | Visible sous forme compacte |
| Sticky | Non permanent en V2.2 |

### 3.4 Style attendu

* fond terracotta CK ;
* hauteur cible : environ 32 px desktop ;
* texte court, lisible, centré ou aligné selon maquette ;
* pas de surcharge iconographique.

---

## 4. Niveau 2 — Barre fonctionnelle

### 4.1 Structure

```text
[Logo C-Kréyòl + baseline]   [Recherche large]   [Se connecter] [Panier + compteur]
```

### 4.2 Bloc marque

Le bloc marque contient :

```text
C-Kréyòl
épicerie créole
```

La baseline “épicerie créole” est obligatoire en V2.2 sur desktop.

Elle qualifie immédiatement le service et évite que C-Kréyòl soit perçu comme un simple média ou une marque culturelle sans fonction marchande.

### 4.3 Recherche

La recherche est un élément P0 du header.

Règles :

* position centrale ;
* largeur importante ;
* placeholder orienté usage ;
* bouton recherche clairement identifiable ;
* comportement standard Odoo si possible ;
* aucun moteur custom en V2.2 sauf nécessité démontrée.

Placeholder de travail :

```text
Rechercher un produit, une saveur, une île...
```

### 4.4 Actions droite

Actions visibles :

```text
Se connecter
Panier + compteur
```

Règles :

* le panier doit afficher un retour visuel clair ;
* compteur visible dès que possible ;
* en V2.2, le panier ne doit pas être une icône seule ambiguë ;
* “Se connecter” est conservé plutôt que “Compte” au lancement.

### 4.5 Comportement sticky

Au scroll :

* le bandeau promesses disparaît ;
* la barre fonctionnelle reste visible ;
* le logo peut être réduit mais doit rester lisible ;
* pas de réduction en “C-K” en V2.2 ;
* recherche et panier restent accessibles.

---

## 5. Niveau 3 — Navigation principale

### 5.1 Navigation retenue

```text
Tous nos produits · Épicerie · Boissons · Maison & Bien-être · Artisanat · Coups de cœur · Coffrets · Nos producteurs · Espace pro
```

### 5.2 Doctrine

La navigation principale est volontairement dense.

Objectif :

* donner une impression de boutique installée ;
* exposer les familles d’offre ;
* rendre visibles les leviers commerciaux ;
* afficher les piliers stratégiques CK : producteurs et espace pro.

### 5.2 bis — Hiérarchie visuelle du Niveau 3

La navigation principale CK V2.2 contient 9 entrées, mais elles ne doivent pas être perçues comme 9 liens équivalents.

Elle est organisée en 3 groupes fonctionnels :

1. **Rayons catalogue**
   Tous nos produits · Épicerie · Boissons · Maison & Bien-être · Artisanat

2. **Sélections commerciales**
   Coups de cœur · Coffrets

3. **Confiance / Relation**
   Nos producteurs · Espace pro

Cette organisation peut rester sur une seule ligne desktop, mais elle doit créer une respiration visuelle entre les groupes.

La séparation peut être obtenue par :

* un espacement plus large entre groupes ;
* un séparateur discret ;
* une variation légère de graisse ou de traitement ;
* un traitement plus relationnel pour “Nos producteurs” ;
* un traitement bouton/pill sobre pour “Espace pro”.

Objectif : éviter l’effet “barre pleine” et faire comprendre que la ligne N3 est structurée en rayons, sélections et relation.

### 5.3 Entrées

| Entrée | Type | Rôle |
| --- | --- | --- |
| Tous nos produits | Catalogue | Portail global vers le shop |
| Épicerie | Mega-menu produit | Cœur alimentaire sec / épicerie fine |
| Boissons | Mega-menu produit | Produits liquides ou à préparer comme boisson |
| Maison & Bien-être | Mega-menu produit | Soin, maison, senteurs, rituels |
| Artisanat | Mega-menu produit conditionnel | Objets, créations, savoir-faire |
| Coups de cœur | Collection transversale | Sélection commerciale éditorialisée |
| Coffrets | Collection transversale | Cadeaux, découverte, bundles |
| Nos producteurs | Page de confiance | Origines, producteurs, artisans |
| Espace pro | Dropdown / accès B2B | Cible professionnelle |

### 5.4 Règle de visibilité

Une entrée de navigation doit être visible si elle dispose :

* d’une page prête ;
* ou d’un contenu réel ;
* ou d’un contenu rapidement activable ;
* ou d’une justification stratégique forte.

Les entrées “Nos producteurs” et “Espace pro” sont considérées comme stratégiques.

### 5.5 — Règle d’intensité des menus

Toutes les entrées de navigation ne reçoivent pas le même niveau de menu.

Les mega-menus complets 4 colonnes sont réservés aux familles de catalogue.

| Entrée | Comportement V2.2 |
| --- | --- |
| Tous nos produits | Lien direct catalogue global |
| Épicerie | Mega-menu complet 4 colonnes |
| Boissons | Mega-menu complet 4 colonnes |
| Maison & Bien-être | Mega-menu complet 4 colonnes |
| Artisanat | Mega-menu complet si contenu suffisant |
| Coups de cœur | Lien direct ou mini-dropdown |
| Coffrets | Lien direct ou mini-dropdown |
| Nos producteurs | Lien direct vers page de confiance |
| Espace pro | Dropdown simple |

Doctrine : plus l’entrée est structurante pour le catalogue, plus le menu peut être riche. Plus l’entrée est transversale ou relationnelle, plus le comportement doit rester léger.

---

## 6. Grammaire commune des mega-menus produit

Les mega-menus produit utilisent une structure commune en 4 colonnes.

```text
Colonne 1 — Acheter par famille
Colonne 2 — Sélections CK
Colonne 3 — Origines & producteurs / artisans
Colonne 4 — Mise en avant visuelle
```

### 6.1 Rôle des colonnes

| Colonne | Intention utilisateur |
| --- | --- |
| Acheter par famille | Je sais ce que je cherche |
| Sélections CK | Je veux être guidé |
| Origines & producteurs | Je cherche une origine, un territoire, un acteur |
| Mise en avant visuelle | Je me laisse inspirer / convaincre |

### 6.2 Règles communes

* Les libellés front peuvent être accentués.
* Les slugs techniques sont sans accents.
* Les familles sont pilotées par catégories Odoo si possible.
* Les sélections sont pilotées par tags ou mécanisme standard Odoo équivalent.
* Le bloc visuel est éditable depuis le BO.
* Le mobile utilise un accordéon, sans bloc visuel.
* Les mega-menus ne contiennent pas de prix.
* Les mega-menus ne contiennent pas de recherche interne en V2.2.

---

## 7. Mega-menu Épicerie CK V2.2

### 7.1 Statut

```text
FIGÉ MOA
```

### 7.2 Doctrine

Épicerie regroupe les produits secs, de garde, à préparer ou à consommer comme denrées d’épicerie fine.

Exception V2.2 : café & infusions restent rattachés à Épicerie.

### 7.3 Familles

| Libellé front | Slug technique |
| --- | --- |
| Biscuits & crackers | biscuits-crackers |
| Confitures & douceurs | confitures-douceurs |
| Farines & manioc | farines-manioc |
| Sauces & condiments | sauces-condiments |
| Chocolat & cacao | chocolat-cacao |
| Café & infusions | cafe-infusions |

### 7.4 Sélections CK

| Libellé | Source |
| --- | --- |
| Coups de cœur | tag `coup_de_coeur` |
| Nouveautés | tag `nouveaute` |
| Coffrets découverte | tag `coffret` |
| Produits La Platine | fournisseur = La Platine |
| Idées cadeaux | tag `cadeau` |

### 7.5 Origines

| Libellé | Filtre |
| --- | --- |
| Guadeloupe | origin-guadeloupe |
| Martinique | origin-martinique |
| Dominique | origin-dominique |
| Guyane | origin-guyane |
| Voir les producteurs | `/nos-producteurs` |

### 7.6 Arbitrage Épicerie / Boissons

```text
Épicerie = produits secs, de garde, épicerie fine.
Boissons = produits liquides ou à préparer comme boisson.
Café & infusions restent en Épicerie V2.2.
```

---

## 8. Mega-menu Boissons CK V2.2

### 8.1 Statut

```text
FIGÉ MOA
```

### 8.2 Doctrine

Boissons regroupe les produits dont l’usage principal est la boisson liquide, prête à consommer ou à préparer.

### 8.3 Familles

| Libellé front | Slug technique | Note |
| --- | --- | --- |
| Jus & nectars | jus-nectars | Produit liquide prêt à boire |
| Sirops créoles | sirops-creoles | Produit à diluer |
| Boissons locales | boissons-locales | Boissons typiques / identitaires |
| Boissons fraîches | boissons-fraiches | Publication conditionnelle |
| Apéritifs & boissons festives | aperitifs-boissons-festives | Alternative sobre à “mocktails” |
| Préparations à boire | preparations-a-boire | Bases ou préparations liquides |

### 8.4 Règle spécifique

La famille “Boissons fraîches” est conditionnelle.

Elle ne doit être publiée que si la capacité logistique CK permet de gérer correctement :

* conservation ;
* transport ;
* température ;
* délais ;
* conformité produit.

### 8.5 Tags spécifiques

```text
sans_alcool
aperitif
```

---

## 9. Mega-menu Maison & Bien-être CK V2.2

### 9.1 Statut

```text
FIGÉ MOA
```

### 9.2 Doctrine

Maison & Bien-être regroupe les produits non alimentaires liés au soin, aux senteurs, aux rituels, à la maison et à l’art de vivre créole.

### 9.3 Familles

| Libellé front | Slug technique |
| --- | --- |
| Savons & soins solides | savons-soins-solides |
| Huiles & baumes | huiles-baumes |
| Senteurs & bougies | senteurs-bougies |
| Maison & décoration | maison-decoration |
| Accessoires bien-être | accessoires-bien-etre |
| Rituels créoles | rituels-creoles |

### 9.4 Règles spécifiques

#### Vigilance réglementaire

Les contenus Maison & Bien-être ne doivent pas contenir de promesses médicales ou thérapeutiques.

À éviter :

* guérit ;
* traite ;
* anti-douleur ;
* anti-stress garanti ;
* effet médical ;
* soulage une pathologie.

Formulations acceptables :

* rituel ;
* senteur ;
* soin ;
* confort ;
* art de vivre ;
* bien-être ;
* usage traditionnel, si formulé prudemment.

#### Distinction alimentaire / soin

| Produit | Classement |
| --- | --- |
| Huile alimentaire | Épicerie |
| Huile de massage / soin | Maison & Bien-être |

### 9.5 Tags spécifiques

```text
bien_etre_naturel
maison
```

---

## 10. Mega-menu Artisanat CK V2.2

### 10.1 Statut

```text
FIGÉ MOA conditionnel
```

Condition :

```text
Mega-menu complet activable si au moins 3 familles Artisanat sont alimentées ou rapidement alimentables.
```

### 10.2 Nom du rayon

```text
Artisanat
```

Raison : court, clair, marchand, compréhensible immédiatement en navigation N3.

### 10.3 Doctrine

Artisanat regroupe les objets, créations et savoir-faire créoles non alimentaires, avec priorité aux petites séries, artisans, créateurs et usages cadeau/décoration.

Cette doctrine garde la dimension culturelle du rayon sans perdre la logique e-commerce.

### 10.4 Règle d’intensité spécifique

Artisanat peut recevoir un mega-menu complet uniquement si le contenu le justifie.

En V2.2 :

* si au moins 3 familles Artisanat sont alimentées ou rapidement alimentables, Artisanat utilise la grammaire commune des mega-menus produit ;
* si le contenu est encore réduit, Artisanat peut rester en lien direct ou en version allégée ;
* aucune famille Artisanat vide ne doit être exposée en navigation publique.

### 10.5 Familles figées

| Libellé front | Slug technique |
| --- | --- |
| Objets décoratifs | objets-decoratifs |
| Arts de la table | arts-de-la-table |
| Textile & accessoires | textile-accessoires |
| Bijoux & créations | bijoux-creations |
| Papeterie & affiches | papeterie-affiches |
| Créations artisanales | creations-artisanales |

### 10.6 Arbitrage libellé

Libellé retenu :

```text
Créations artisanales
```

Libellé non retenu en navigation :

```text
Savoir-faire créoles
```

Motif : “Créations artisanales” est plus immédiatement marchand et plus simple à comprendre dans une navigation e-commerce.

“Savoir-faire créoles” reste pertinent pour un bloc visuel, une page producteur/artisan, ou une section éditoriale “Découvrir”.

### 10.7 Sélections CK

| Libellé | Source possible |
| --- | --- |
| Coups de cœur | tag `coup_de_coeur` |
| Nouveautés | tag `nouveaute` |
| Idées cadeaux | tag `cadeau` |
| Créateurs à découvrir | tag `createur` |
| Petites séries | tag `petite_serie` |

### 10.8 Colonne 3

```text
Origines & artisans
```

Motif : cohérent avec “Artisanat”, plus concret, et compatible avec les créateurs sans sur-spécialiser la navigation.

### 10.9 Règle de visibilité

Une famille Artisanat ne doit être visible que si elle contient au moins :

* un produit publié ;
* ou une collection prête à être alimentée ;
* ou une justification stratégique validée MOA.

### 10.10 Version allégée si contenu insuffisant

Si le contenu Artisanat ne justifie pas encore un mega-menu complet, le comportement recommandé est :

```text
Artisanat → lien direct vers une page ou catégorie Artisanat
```

ou :

```text
Artisanat
├── Objets & décoration
├── Créateurs à découvrir
└── Idées cadeaux
```

Cette version allégée doit rester transitoire et ne pas introduire de fausses profondeurs.

---

## 11. Entrées transversales restantes

### 11.1 Coups de cœur

Statut :

```text
FIGÉ MOA
```

Lecture actuelle :

```text
Collection transversale, pas forcément mega-menu lourd.
```

Doctrine proposée :

```text
Coups de cœur regroupe une sélection éditorialisée et commerciale de produits prioritaires, choisis par CK pour guider l’achat, soutenir la découverte et mettre en avant les produits à forte valeur d’image ou de conversion.
```

Objectif :

* mettre en avant une sélection commerciale CK ;
* renforcer la découverte ;
* soutenir les produits prioritaires ;
* créer une entrée simple pour les visiteurs qui veulent être guidés sans choisir un rayon.

Source possible :

```text
product.template tag `coup_de_coeur`
```

Comportement V2.2 recommandé :

```text
Lien direct uniquement
```

Règle d’intensité :

```text
Coups de cœur ne reçoit pas de mega-menu complet en V2.2.
```

Justification :

* entrée transversale, non rayon catalogue ;
* sélection amenée à varier ;
* lecture plus claire sous forme de page collection ;
* évite de répéter les familles déjà présentes dans les rayons.

URL cible pressentie :

```text
/shop?tag=coup_de_coeur
```

ou page collection dédiée filtrée par tag `coup_de_coeur` si la mise en scène éditoriale est prioritaire.

Verdict MOA :

```text
Coups de cœur = page / collection filtrée par tag `coup_de_coeur`.
```

Libellé N3 retenu :

```text
Coups de cœur
```

### 11.2 Coffrets

Statut :

```text
FIGÉ MOA conditionnel
```

Lecture actuelle :

```text
Collection commerciale transversale.
```

Doctrine proposée :

```text
Coffrets regroupe les offres cadeaux, découvertes, bundles et compositions thématiques CK, avec une logique d’achat guidé, de première commande, d’occasion saisonnière ou de panier prêt à offrir.
```

Objectif :

* cadeaux ;
* découverte ;
* bundles ;
* paniers thématiques ;
* offres saisonnières ;
* faciliter l’achat sans expertise préalable des rayons.

Source possible :

```text
product.template tag `coffret`
```

ou logique pack / bundle Odoo selon faisabilité.

Comportement V2.2 recommandé :

```text
Lien direct par défaut
Mini-dropdown léger uniquement si au moins 3 angles commerciaux sont prêts
```

Règle d’intensité :

```text
Coffrets ne reçoit pas de mega-menu complet en V2.2.
```

Comportement par défaut :

```text
Lien direct vers une collection Coffrets
```

Mini-dropdown autorisé uniquement si au moins 3 angles commerciaux sont prêts.

Angles commerciaux possibles :

```text
Découverte
Cadeau
Entreprise / pro
Saison / fête
Origine / territoire
```

Structure mini-dropdown possible :

```text
Coffrets
├── Coffrets découverte
├── Idées cadeaux
└── Coffrets pro
```

URL cible pressentie :

```text
/shop?tag=coffret
```

ou page collection dédiée si les coffrets nécessitent une mise en scène éditoriale.

Verdict MOA :

```text
Coffrets = lien direct collection `coffret` tant que 3 angles commerciaux ne sont pas prêts.
```

Libellé N3 retenu :

```text
Coffrets
```

### 11.3 Nos producteurs

Statut :

```text
FIGÉ MOA
```

Ce n’est pas un mega-menu produit classique.

Doctrine :

```text
“Nos producteurs” présente les producteurs, artisans et partenaires d’origine des produits C-Kréyòl, afin de rendre visible la promesse d’origines identifiées, de renforcer la confiance et de relier chaque produit à un acteur réel.
```

Rôle dans le header :

```text
Entrée preuve / confiance
```

Ce n’est pas une entrée catalogue.
Ce n’est pas une sélection commerciale.

Elle doit dire implicitement :

```text
Les produits CK ne viennent pas de nulle part.
Ils sont rattachés à des producteurs, artisans ou partenaires identifiables.
```

Objectif :

* présenter les producteurs ;
* présenter les artisans ;
* renforcer la traçabilité ;
* donner de la profondeur à la promesse “origines identifiées”.

URL cible :

```text
/nos-producteurs
```

Comportement V2.2 recommandé :

```text
Lien direct
```

Règle d’intensité :

```text
Pas de mega-menu.
Pas de dropdown en V2.2.
```

L’entrée doit rester légère dans la navigation N3, mais visible car stratégique.

Structure minimale de la page :

```text
/nos-producteurs

1. Intro courte
   Pourquoi CK affiche ses producteurs / artisans.

2. Grille producteurs
   - Nom
   - Origine / territoire
   - Type de produits
   - Image ou logo
   - Court texte de présentation
   - Lien vers produits associés

3. Filtrage simple possible
   - Origine
   - Famille produit
   - Producteur / artisan

4. CTA
   - Voir les produits
   - Proposer un producteur / devenir partenaire
```

Règle de publication producteur :

```text
Un producteur ne doit être affiché que s’il est suffisamment qualifié.
```

Critères minimaux :

* nom clair ;
* origine / territoire renseigné ;
* au moins un produit associé publié ou publiable ;
* court texte de présentation validé ;
* image/logo disponible ou fallback propre.

Condition de publication de la page :

```text
La page peut être publiée dès lors qu’au moins 2 producteurs/artisans disposent d’une fiche minimale qualifiée.
```

### 11.4 Espace pro

Statut :

```text
FIGÉ MOA
```

Doctrine :

```text
Espace pro est une entrée relationnelle B2B destinée aux commerces, distributeurs, CHR, épiceries spécialisées et partenaires professionnels souhaitant acheter, référencer ou distribuer des produits C-Kréyòl.
```

L’objectif V2.2 n’est pas de vendre tout de suite en mode B2B transactionnel complet.

L’objectif est de dire :

```text
CK est aussi ouvert aux professionnels, et il existe un chemin clair pour entrer en relation.
```

Objectif :

* rendre visible la cible B2B ;
* orienter distributeurs, commerces, CHR, épiceries spécialisées ;
* permettre une prise de contact rapide.

Comportement V2.2 recommandé :

```text
Dropdown simple
```

Règle d’intensité :

```text
Pas de mega-menu.
Pas de gros panneau.
Pas de complexité inutile.
```

Espace pro doit rester une entrée relationnelle, pas un rayon catalogue.

Structure figée :

```text
Espace pro
├── Acheter pour mon commerce
├── Demander les conditions pro
├── Devenir partenaire / distributeur
└── Contacter C-Kréyòl
```

Page cible :

```text
/professionnels
```

Chaque entrée du dropdown pointe vers une section de la page :

```text
/professionnels#acheter
/professionnels#conditions
/professionnels#partenaire
/professionnels#contact
```

Condition de publication :

```text
Espace pro peut être visible même avec peu de contenu, car c’est une promesse relationnelle stratégique.
```

Conditions minimales :

* page `/professionnels` existante ;
* formulaire ou moyen de contact fonctionnel ;
* message clair sur la cible pro ;
* aucune promesse commerciale B2B non tenue.

Hors périmètre V2.2 :

* tarifs B2B affichés publiquement ;
* commande pro autonome ;
* compte pro automatisé ;
* portail distributeur ;
* logique de devis avancée.

Verdict MOA :

```text
Espace pro = dropdown simple / relation B2B.
```

---

## 12. Modèle BO — Bloc visuel mega-menu

Le bloc visuel de chaque mega-menu doit être éditable depuis le back-office.

### 12.1 Champs requis

| Champ | Type | Obligatoire |
| --- | --- | --- |
| Menu concerné | Sélection | Oui |
| Image | Image | Oui |
| Titre | Char(60) | Oui |
| Sous-titre | Char(120) | Non |
| Lien cible | URL | Oui |
| Libellé CTA | Char(30) | Oui |
| Date début | Date | Non |
| Date fin | Date | Non |
| Actif | Boolean | Oui |
| Séquence | Integer | Oui |

### 12.2 Règle d’affichage

Si plusieurs blocs actifs existent pour un même menu :

* afficher celui dont la séquence est la plus basse ;
* si des dates sont renseignées, vérifier que la date courante est comprise dans la période ;
* si aucun bloc valide n’existe, masquer la colonne 4 ou afficher un fallback sobre selon arbitrage Dev/MOA.

---

## 13. Mobile

### 13.1 Structure mobile générale

```text
Bandeau promesse compact
[Menu] [C-Kréyòl] [Recherche] [Panier]
Menu latéral / accordéons
```

La baseline “épicerie créole” reste souhaitable, mais elle est conditionnelle sur mobile.

Règle mobile :

```text
Baseline visible uniquement si la hauteur reste maîtrisée.
Sinon, baseline affichée dans le drawer ou sous le logo en version compacte.
```

### 13.2 Règles mobile mega-menu

* pas de bloc visuel ;
* accordéon par section ;
* ordre identique au desktop ;
* CTA producteurs visible en bas ;
* toutes les entrées de la navigation principale doivent être accessibles ;
* pas de surcharge en chips sur toutes les pages ;
* chips catégories possibles sur home ou shop uniquement si utiles.

---

## 14. Hors périmètre V2.2

| Élément | Motif |
| --- | --- |
| Recherche interne aux mega-menus | Barre N2 suffisante |
| Prix dans les mega-menus | Trop variable |
| Stock temps réel dans menu | Complexité non prioritaire |
| Multi-blocs visuels rotatifs | V2.3 |
| A/B testing menu | V2.3 |
| Personnalisation par profil utilisateur | V2+ |
| Switcher Boutique / Éditorial / Communauté | V2+ |
| Filtres avancés par producteur individuel | À traiter après page producteurs |

---

## 15. Décisions actées V2.2

### 15.1 Navigation N3 dense, mais non équivalente

La densité de la navigation principale est assumée, mais organisée.

Lecture officielle :

```text
Rayons catalogue
Tous nos produits · Épicerie · Boissons · Maison & Bien-être · Artisanat

Sélections commerciales
Coups de cœur · Coffrets

Confiance / Relation
Nos producteurs · Espace pro
```

### 15.2 Mega-menu complet seulement pour les rayons

```text
Épicerie           → mega-menu complet
Boissons           → mega-menu complet
Maison & Bien-être → mega-menu complet
Artisanat          → mega-menu complet si contenu suffisant
```

Les entrées transversales ou relationnelles utilisent des comportements plus légers :

```text
Coups de cœur   → lien direct uniquement
Coffrets        → lien direct par défaut / mini-dropdown conditionnel
Nos producteurs → lien direct
Espace pro      → dropdown simple
```

### 15.3 Mobile : priorité usage

Sur mobile, l’ordre officiel devient :

```text
Bandeau promesse compact
[Menu] [C-Kréyòl] [Recherche] [Panier]
Menu latéral / accordéons
```

La baseline est conditionnelle afin de préserver la hauteur utile.

---

## 16. Verdict de clôture MOA

Le Header CK V2.2 est considéré comme figé en architecture MOA.

Les trois niveaux du header, la navigation N3, la hiérarchie des entrées, la règle d’intensité des menus, les quatre rayons catalogue, les sélections commerciales, les entrées confiance/relation et le comportement mobile sont validés.

Le document est prêt pour découpage Dev, sous réserve de recette visuelle et d’adaptation technique Odoo 19 CE.

---

## 17. Critères de recette QA

* Le header affiche bien les 3 niveaux au chargement desktop.
* Le bandeau promesse disparaît au scroll.
* La barre fonctionnelle reste lisible au scroll.
* La navigation N3 affiche les 9 entrées dans une hiérarchie visuelle perceptible.
* Les rayons catalogue déclenchent le bon comportement menu.
* Coups de cœur est un lien direct uniquement.
* Coffrets est un lien direct par défaut, avec mini-dropdown uniquement si condition remplie.
* Nos producteurs est un lien direct vers `/nos-producteurs`.
* Espace pro est un dropdown simple.
* Sur mobile, le bandeau promesse compact est visible, puis la ligne `[Menu] [C-Kréyòl] [Recherche] [Panier]`.
* Les mega-menus mobiles sont rendus en accordéons sans bloc visuel.
