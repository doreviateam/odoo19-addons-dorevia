# Ticket Dev — Header & Mega-menus CK V2.2

| Champ | Valeur |
| --- | --- |
| Projet | `dorevia_ck_marketone` |
| Module principal | `dorevia_ck_theme` |
| Module éventuel complémentaire | `dorevia_ck_marketone_content` / module dédié si nécessaire |
| Type | UX/UI front + navigation + structure mega-menus |
| Priorité | P0 |
| Statut | À exécuter |
| Référence MOA | `docs/design/maquette_01.2/SPEC_HEADER_MEGA_MENUS_CK_V2_2.md` |
| Version cible | Header CK V2.2 |

---

## 1. Objectif

Implémenter le Header C-Kréyòl V2.2 conformément à la spécification MOA figée.

Le header doit devenir un véritable système d’orientation e-commerce, structuré en trois niveaux :

```text
N1 — Promesse / confiance
N2 — Marque + recherche + achat
N3 — Orientation catalogue
```

L’objectif n’est pas seulement d’ajouter des liens, mais de rendre le header immédiatement lisible, marchand, professionnel et cohérent avec l’identité C-Kréyòl.

---

## 2. Périmètre fonctionnel

### 2.1 Niveau 1 — Bandeau promesses

Implémenter un bandeau promesse visible au chargement.

Contenu cible :

```text
Produits sélectionnés · Origines identifiées · Livraison suivie · Stocké/expédié depuis Nantes
```

Comportement attendu :

* visible au chargement desktop ;
* disparaît au scroll ;
* visible sous forme compacte sur mobile ;
* non sticky permanent en V2.2 ;
* style terracotta CK ;
* hauteur cible desktop environ 32 px.

### 2.2 Niveau 2 — Barre fonctionnelle

Structure attendue :

```text
[Logo C-Kréyòl + baseline]   [Recherche large]   [Se connecter] [Panier + compteur]
```

Règles :

* afficher le logo C-Kréyòl ;
* afficher la baseline desktop : `épicerie créole` ;
* recherche centrée, large, visible, actionnable ;
* placeholder de travail : `Rechercher un produit, une saveur, une île...` ;
* conserver le comportement standard Odoo si possible ;
* afficher `Se connecter` ;
* afficher le panier avec compteur ;
* au scroll, la barre reste lisible ;
* le logo peut être réduit mais doit rester lisible ;
* ne pas réduire le logo en `C-K` en V2.2.

### 2.3 Niveau 3 — Navigation principale

Navigation retenue :

```text
Tous nos produits · Épicerie · Boissons · Maison & Bien-être · Artisanat · Coups de cœur · Coffrets · Nos producteurs · Espace pro
```

Cette navigation est dense mais ne doit pas être perçue comme une simple liste plate de 9 liens.

Elle doit être organisée visuellement en trois groupes :

```text
Rayons catalogue
Tous nos produits · Épicerie · Boissons · Maison & Bien-être · Artisanat

Sélections commerciales
Coups de cœur · Coffrets

Confiance / Relation
Nos producteurs · Espace pro
```

Le rendu doit créer une respiration visuelle entre ces groupes via l’un des moyens suivants :

* espacement plus large ;
* séparateur discret ;
* variation légère de graisse ;
* traitement plus relationnel pour `Nos producteurs` ;
* traitement bouton/pill sobre pour `Espace pro`.

---

## 3. Règle d’intensité des menus

Toutes les entrées ne reçoivent pas le même comportement.

| Entrée | Comportement attendu |
| --- | --- |
| Tous nos produits | Lien direct catalogue global |
| Épicerie | Mega-menu complet 4 colonnes |
| Boissons | Mega-menu complet 4 colonnes |
| Maison & Bien-être | Mega-menu complet 4 colonnes |
| Artisanat | Mega-menu complet si contenu suffisant |
| Coups de cœur | Lien direct uniquement |
| Coffrets | Lien direct par défaut / mini-dropdown conditionnel |
| Nos producteurs | Lien direct vers `/nos-producteurs` |
| Espace pro | Dropdown simple |

Doctrine : plus l’entrée est structurante pour le catalogue, plus le menu peut être riche. Plus l’entrée est transversale ou relationnelle, plus le comportement doit rester léger.

---

## 4. Grammaire commune des mega-menus produit

Les mega-menus produit doivent suivre la structure commune suivante :

```text
Colonne 1 — Acheter par famille
Colonne 2 — Sélections CK
Colonne 3 — Origines & producteurs / artisans
Colonne 4 — Mise en avant visuelle
```

Règles communes :

* libellés front accentués autorisés ;
* slugs techniques sans accents ;
* familles pilotées par catégories Odoo si possible ;
* sélections pilotées par tags ou mécanisme standard Odoo équivalent ;
* bloc visuel éditable depuis le BO ;
* pas de prix dans les mega-menus ;
* pas de recherche interne aux mega-menus ;
* mobile en accordéon sans bloc visuel.

---

## 5. Mega-menu Épicerie

Statut MOA : FIGÉ.

Familles :

```text
Biscuits & crackers
Confitures & douceurs
Farines & manioc
Sauces & condiments
Chocolat & cacao
Café & infusions
```

Sélections :

```text
Coups de cœur
Nouveautés
Coffrets découverte
Produits La Platine
Idées cadeaux
```

Origines :

```text
Guadeloupe
Martinique
Dominique
Guyane
Voir les producteurs
```

Règle spécifique :

```text
Café & infusions restent en Épicerie V2.2.
```

---

## 6. Mega-menu Boissons

Statut MOA : FIGÉ.

Familles :

```text
Jus & nectars
Sirops créoles
Boissons locales
Boissons fraîches
Apéritifs & boissons festives
Préparations à boire
```

Règle spécifique :

```text
Boissons fraîches est une famille conditionnelle.
Elle ne doit être publiée que si la capacité logistique CK le permet.
```

Tags spécifiques :

```text
sans_alcool
aperitif
```

---

## 7. Mega-menu Maison & Bien-être

Statut MOA : FIGÉ.

Familles :

```text
Savons & soins solides
Huiles & baumes
Senteurs & bougies
Maison & décoration
Accessoires bien-être
Rituels créoles
```

Règles spécifiques :

* aucun claim médical ou thérapeutique ;
* huile alimentaire = Épicerie ;
* huile de massage / soin = Maison & Bien-être.

Tags spécifiques :

```text
bien_etre_naturel
maison
```

---

## 8. Artisanat

Statut MOA : FIGÉ conditionnel.

Condition :

```text
Mega-menu complet activable si au moins 3 familles Artisanat sont alimentées ou rapidement alimentables.
```

Familles :

```text
Objets décoratifs
Arts de la table
Textile & accessoires
Bijoux & créations
Papeterie & affiches
Créations artisanales
```

Colonne 3 :

```text
Origines & artisans
```

Règle :

* aucune famille Artisanat vide ne doit être exposée publiquement ;
* si contenu insuffisant, Artisanat reste un lien direct ou un dropdown allégé transitoire.

---

## 9. Entrées transversales

### 9.1 Coups de cœur

Comportement :

```text
Lien direct uniquement
```

Source fonctionnelle :

```text
tag produit `coup_de_coeur`
```

Pas de mega-menu, pas de mini-dropdown en V2.2.

### 9.2 Coffrets

Comportement :

```text
Lien direct par défaut
Mini-dropdown léger uniquement si au moins 3 angles commerciaux sont prêts
```

Angles possibles :

```text
Découverte
Cadeau
Entreprise / pro
Saison / fête
Origine / territoire
```

Source possible :

```text
tag produit `coffret`
```

ou logique pack / bundle Odoo selon faisabilité.

### 9.3 Nos producteurs

Comportement :

```text
Lien direct vers /nos-producteurs
```

Pas de mega-menu.
Pas de dropdown en V2.2.

Condition de publication de la page :

```text
Au moins 2 producteurs/artisans disposent d’une fiche minimale qualifiée.
```

Fiche minimale :

* nom clair ;
* origine / territoire renseigné ;
* au moins un produit associé publié ou publiable ;
* texte court validé ;
* image/logo ou fallback propre.

### 9.4 Espace pro

Comportement :

```text
Dropdown simple
```

Structure :

```text
Espace pro
├── Acheter pour mon commerce
├── Demander les conditions pro
├── Devenir partenaire / distributeur
└── Contacter C-Kréyòl
```

Liens :

```text
/professionnels#acheter
/professionnels#conditions
/professionnels#partenaire
/professionnels#contact
```

Hors périmètre V2.2 :

* tarifs B2B publics ;
* commande pro autonome ;
* compte pro automatisé ;
* portail distributeur ;
* logique de devis avancée.

---

## 10. Modèle BO — Bloc visuel mega-menu

Créer ou adapter un modèle BO permettant de gérer le bloc visuel des mega-menus produit.

Champs requis :

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

Règle d’affichage :

* si plusieurs blocs actifs existent, afficher celui dont la séquence est la plus basse ;
* si des dates sont renseignées, respecter la période ;
* si aucun bloc valide n’existe, masquer la colonne 4 ou afficher un fallback sobre à valider.

---

## 11. Mobile

Structure mobile cible :

```text
Bandeau promesse compact
[Menu] [C-Kréyòl] [Recherche] [Panier]
Menu latéral / accordéons
```

Règles :

* baseline `épicerie créole` conditionnelle ;
* pas de bloc visuel dans les menus mobiles ;
* accordéon par section ;
* ordre identique au desktop ;
* toutes les entrées N3 accessibles ;
* pas de surcharge en chips sur toutes les pages ;
* chips possibles sur home ou shop uniquement si utiles.

---

## 12. Hors périmètre V2.2

| Élément | Motif |
| --- | --- |
| Recherche interne aux mega-menus | Barre N2 suffisante |
| Prix dans les mega-menus | Trop variable |
| Stock temps réel dans menu | Complexité non prioritaire |
| Multi-blocs visuels rotatifs | V2.3 |
| A/B testing menu | V2.3 |
| Personnalisation par profil utilisateur | V2+ |
| Switcher Boutique / Éditorial / Communauté | V2+ |
| Filtres avancés par producteur individuel | Après page producteurs |

---

## 13. Contraintes techniques / principes Dev

* Respecter autant que possible les mécanismes standards Odoo 19 CE.
* Ne pas créer de moteur de recherche custom en V2.2.
* Ne pas casser le comportement standard du panier, login, recherche, `/shop`, catégories publiques.
* Préserver la capacité d’édition BO.
* Ne pas coder en dur les blocs visuels saisonniers.
* Les URLs proposées dans la spec MOA sont des intentions fonctionnelles : les adapter à la mécanique réelle Odoo si nécessaire.
* Les slugs techniques doivent rester sans accents.
* Le rendu doit rester compatible desktop et mobile.
* Ne pas introduire de fausses profondeurs : aucune famille vide visible publiquement.

---

## 14. Critères de recette QA

* Le header affiche bien les 3 niveaux au chargement desktop.
* Le bandeau promesse disparaît au scroll.
* La barre fonctionnelle reste lisible au scroll.
* La navigation N3 affiche les 9 entrées dans une hiérarchie visuelle perceptible.
* Les trois groupes N3 sont lisibles : rayons, sélections, confiance/relation.
* Les rayons catalogue déclenchent le bon comportement menu.
* Épicerie, Boissons, Maison & Bien-être affichent des mega-menus complets.
* Artisanat applique correctement la règle conditionnelle.
* Coups de cœur est un lien direct uniquement.
* Coffrets est un lien direct par défaut, avec mini-dropdown uniquement si condition remplie.
* Nos producteurs est un lien direct vers `/nos-producteurs`.
* Espace pro est un dropdown simple.
* Sur mobile, le bandeau promesse compact est visible, puis la ligne `[Menu] [C-Kréyòl] [Recherche] [Panier]`.
* Les mega-menus mobiles sont rendus en accordéons sans bloc visuel.
* Aucun prix, stock temps réel ou recherche interne n’est ajouté dans les mega-menus.
* Aucune famille vide n’est exposée publiquement.

---

## 15. Livrables attendus

* Implémentation front du header CK V2.2.
* Intégration navigation N3 hiérarchisée.
* Mega-menus produit conformes à la grammaire 4 colonnes.
* Gestion mobile en accordéons.
* Modèle BO pour bloc visuel mega-menu ou solution standard équivalente.
* Documentation Dev courte des choix techniques.
* Captures desktop et mobile pour recette.
* Liste des adaptations éventuelles liées aux contraintes Odoo 19 CE.

---

## 16. Découpage recommandé

### Lot 1 — Socle header

* N1 bandeau promesses.
* N2 barre fonctionnelle.
* N3 navigation principale.
* Hiérarchie visuelle N3.
* Sticky desktop.
* Mobile header de base.

### Lot 2 — Socle mega-menu

* Layout desktop 4 colonnes.
* Règles hover/click/fermeture.
* Mobile accordéon.
* Modèle BO bloc visuel.
* Fallback colonne 4.

### Lot 3 — Rayons catalogue

* Épicerie.
* Boissons.
* Maison & Bien-être.
* Artisanat conditionnel.

### Lot 4 — Entrées transversales

* Coups de cœur.
* Coffrets.
* Nos producteurs.
* Espace pro.

### Lot 5 — Recette / polish

* Tests desktop.
* Tests mobile.
* Non-régression panier / login / recherche / shop.
* Ajustements visuels.
