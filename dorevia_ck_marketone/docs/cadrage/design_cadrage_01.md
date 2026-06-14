# design_cadrage_01 — CK / Marketone — Brief Open Design avant DESIGN.md

## 1. Objet du cadrage design

Ce document prépare la production du futur `DESIGN.md CK`.

Il sert de brief pour la phase Open Design du projet `dorevia_ck_marketone`.

Objectif :

> Donner une direction claire à Open Design avant toute maquette, sans entrer dans Odoo, sans reprendre automatiquement l’ancienne direction artistique, et sans créer une logique d’application front autonome.

Ce document ne décrit pas encore la maquette finale.

Il fixe :

- l’intention visuelle ;
- l’ambiance recherchée ;
- les parcours prioritaires ;
- les contraintes Odoo ;
- les composants à concevoir ;
- les interdits ;
- les livrables attendus.

---

## 2. Rappel de la vision CK

CK n’est pas seulement un site e-commerce de produits créoles.

CK a vocation à devenir une plateforme de sourcing, de commerce et de logistique pour les productions agro-transformées issues des zones créoles.

Phrase fondatrice :

> CK a pour ambition de sourcer, valoriser et distribuer les productions agro-transformées du monde créole, en assurant le lien logistique entre la porte du producteur et la porte de l’acheteur, en B2B comme en B2C.

Le site doit donc être compris comme :

```text
un outil marchand
un outil de confiance
un outil de découverte
un outil de valorisation filière
un outil préparant une future logistique maîtrisée
```

CK doit vendre, mais aussi rendre visible une filière.

---

## 3. Périmètre design phase 1

La phase design 1 ne couvre pas l’intégralité de la vision CK.

Elle couvre prioritairement :

```text
Accueil
/shop
Parcours B2C principal
Signaux B2B visibles
Signaux logistiques visibles
Réassurance achat
```

Elle ne couvre pas encore :

```text
mécanique complète B2B
portail revendeur
listes de prix professionnelles
demande de devis complète
workflow logistique complet
gestion avancée producteurs
gestion avancée stocks / entrepôts
```

Décision :

> La première direction design doit rendre CK immédiatement marchand et compréhensible, sans prétendre résoudre toute la mécanique B2B/logistique.

---

## 4. Ce que le site doit faire ressentir

Le futur site CK doit faire ressentir :

- la gourmandise ;
- la vitalité ;
- la confiance ;
- la clarté ;
- le sérieux marchand ;
- l’accessibilité ;
- l’origine créole ;
- la qualité produit ;
- l’envie de découvrir ;
- l’envie d’acheter.

Le site ne doit pas être :

- froid ;
- institutionnel ;
- contemplatif ;
- décoratif sans efficacité ;
- trop premium au point de freiner l’achat ;
- trop “galerie” ;
- trop éditorial au détriment du commerce ;
- trop exotisant ;
- trop sombre ;
- trop startup marketplace générique.

Phrase de direction :

> CK doit être marchand, vivant, gourmand, clair et traduisible dans Odoo.

---

## 5. Ce que le site doit permettre de faire

Le site doit permettre à un visiteur de :

- comprendre rapidement ce qui est vendu ;
- identifier les grandes familles de produits ;
- accéder facilement à la boutique ;
- voir les produits sans friction ;
- voir les prix ;
- comprendre les origines ;
- être rassuré sur la livraison ;
- percevoir qu’il existe une offre professionnelle ;
- ajouter un produit au panier ;
- comprendre le chemin vers l’achat ;
- découvrir des produits qu’il ne connaît pas encore.

Le site doit aussi préparer une lecture plus ambitieuse :

```text
CK source les produits
CK les valorise
CK les vend
CK prépare leur acheminement
CK parle aux particuliers et aux professionnels
```

Mais cette ambition doit rester lisible et simple en phase 1.

---

## 6. Direction artistique réouverte

Les directions précédentes ne sont pas reconduites automatiquement.

Sont considérés comme historiques, non comme cible obligatoire :

```text
terracotta
sauge
crème
pastel premium
warm-editorial comme direction imposée
ancien prototype CK
ancienne mémoire Open Design
```

Le futur `DESIGN.md CK` devra repartir d’une intention neuve.

Cette intention peut s’inspirer de l’efficacité des sites marchands alimentaires contemporains, mais sans copie graphique.

La priorité n’est pas de produire une esthétique “jolie”.

La priorité est de produire une esthétique :

```text
qui donne faim
qui donne confiance
qui montre les produits
qui rend l’achat évident
qui reste maîtrisable dans Odoo
```

---

## 7. Inspiration utile

L’inspiration de type `directos.eu` est retenue pour son efficacité commerciale, non pour sa charte graphique.

Ce qui est utile :

- promesse immédiate ;
- catégories fortes ;
- produits très visibles ;
- prix lisibles ;
- CTA directs ;
- réassurance claire ;
- ton vivant ;
- profondeur catalogue ;
- packs / lots / offres visibles ;
- contenus utiles à l’achat ;
- expérience orientée conversion.

Ce qui ne doit pas être copié :

- identité visuelle ;
- structure exacte ;
- textes ;
- images ;
- marque ;
- mise en page spécifique ;
- logique technique.

Règle :

> On s’inspire de l’efficacité marchande, pas du design en tant que copie.

---

## 8. Contraintes Odoo à intégrer dès le design

Open Design doit produire une maquette traduisible dans Odoo.

Cela signifie que la maquette doit respecter les contraintes suivantes :

```text
Odoo reste la source de vérité métier.
website_sale reste le moteur boutique.
Le panier reste Odoo.
Le checkout reste Odoo.
Les prix viennent d’Odoo.
Les produits viennent d’Odoo.
Les catégories et attributs doivent pouvoir être traduits en logique Odoo.
Les composants visuels doivent pouvoir devenir thème, QWeb ou snippets.
```

Checklist de compatibilité design :

```text
□ Pas de catalogue JavaScript local comme logique cible.
□ Pas de panier simulé comme comportement cible.
□ Pas de checkout hors website_sale.
□ Pas de prix figés dans le HTML comme source cible.
□ Pas de SPA React/Vue comme boutique.
□ Pas d’interaction impossible à traduire en Odoo sans extension majeure.
□ Tokens visuels exportables en SCSS.
□ Grille responsive compatible avec logique Odoo / Bootstrap.
□ Filtres traduisibles en catégories, attributs, domaines ou URL Odoo.
□ Signaux B2B/logistique visibles sans imposer leur mécanique complète.
```

---

## 9. Composants à concevoir

Open Design doit aider à concevoir les composants suivants.

### 9.1 Composants globaux

- header ;
- navigation principale ;
- entrée boutique ;
- entrée professionnels ;
- recherche ;
- icône panier ;
- footer ;
- bandeau de réassurance ;
- CTA principaux ;
- CTA secondaires.

### 9.2 Composants boutique `/shop`

- titre de page boutique ;
- sous-titre marchand ;
- sidebar ou zone de filtres ;
- catégories ;
- origines ;
- collections / packs si utile ;
- prix / fourchette prix ;
- toolbar ;
- tri ;
- badges ;
- carte produit ;
- état vide ;
- pagination ou chargement ;
- zone de réassurance.

### 9.3 Carte produit

La carte produit doit rendre visibles :

- image produit ;
- nom produit ;
- origine ou zone ;
- catégorie ;
- prix ;
- badge utile ;
- CTA achat ;
- éventuellement format / poids ;
- éventuellement indication “pro” ou “pack”.

Elle doit donner envie d’acheter sans surcharger.

### 9.4 Réassurance

La maquette doit prévoir des signaux de confiance :

- livraison ;
- paiement sécurisé ;
- origine / producteurs ;
- service client ;
- B2C / B2B ;
- retours ou conditions ;
- promesse logistique.

---

## 10. Parcours prioritaires

La direction design doit être pensée à partir de parcours réels.

| Persona | Objectif | Parcours à vérifier |
|---|---|---|
| Particulier acheteur | Acheter un produit créole | Accueil → boutique → produit → panier |
| Professionnel / revendeur | Comprendre qu’une offre pro existe | Accueil ou boutique → entrée pro |
| Acheteur par origine | Chercher une zone créole | Boutique → origine → produits |
| Client prudent | Être rassuré avant achat | Boutique / fiche → livraison / paiement / contact |
| Découvreur | Explorer des produits inconnus | Accueil → catégories / packs / contenus |
| Acheteur pressé | Aller vite à l’achat | Boutique → carte produit → panier |

Ces parcours serviront plus tard à la recette maquette.

---

## 11. B2C / B2B en phase design 1

La lecture phase 1 est :

```text
B2C = parcours principal visible et achetable
B2B = entrée secondaire visible, non complète
```

### 11.1 B2C

Le B2C doit être immédiatement compréhensible.

Un particulier doit pouvoir :

- comprendre l’offre ;
- voir les produits ;
- voir les prix ;
- acheter ;
- être rassuré.

### 11.2 B2B

Le B2B doit être visible, mais il ne doit pas dominer la phase 1.

Il peut être représenté par :

- un lien “Professionnels” ;
- un bloc “Vous êtes revendeur ?” ;
- un CTA “Demander un accès pro” ;
- une mention “Achat en volume” ;
- un bloc “Boutiques, restaurants, distributeurs”.

Mais il ne faut pas encore concevoir :

- le portail complet ;
- les prix masqués ;
- les listes de prix dynamiques ;
- le workflow de devis ;
- la logique commerciale B2B complète.

---

## 12. Interdits design / UX

Sont interdits dans la direction design cible :

```text
site galerie sans achat clair
boutique trop décorative
cartes produit sans prix
CTA achat invisible
filtres impossibles à traduire dans Odoo
logique panier hors Odoo
checkout alternatif
catalogue statique hors Odoo
front autonome
effets visuels qui concurrencent les produits
ancienne DA réinjectée par défaut
```

Règle :

> Le design doit servir l’achat, la compréhension et la confiance.

---

## 13. Livrable attendu : DESIGN.md CK

Le prochain livrable doit être un `DESIGN.md CK`.

Il devra contenir :

```text
1. Vision design
2. Promesse utilisateur
3. Ton
4. Ambiance
5. Principes visuels
6. Palette exploratoire ou règles de choix couleur
7. Typographies
8. Grille
9. Composants
10. Règles produits
11. Règles /shop
12. Règles B2C/B2B phase 1
13. Réassurance
14. Contraintes Odoo
15. Interdits
16. Critères de validation
```

Ce `DESIGN.md CK` deviendra la référence visuelle opposable.

Il primera sur les anciennes mémoires Open Design relatives à CK.

---

## 14. Critères de réussite du DESIGN.md CK

Le `DESIGN.md CK` sera considéré satisfaisant s’il permet de produire une maquette qui est :

```text
marchande
vivante
gourmande
claire
rassurante
orientée achat
compatible Odoo
non dépendante d’un front autonome
testable par le QA
relisible par le Dev
arbitrable par David
```

---

## 15. Synthèse

La phase actuelle est :

```text
Cadrage design
    → DESIGN.md CK
        → maquette /shop
            → revue Dev traduisibilité Odoo
                → recette QA maquette
                    → arbitrage David
                        → seulement ensuite décision Odoo
```

Phrase de synthèse :

> Le design CK doit donner envie d’acheter des produits créoles, rendre la filière lisible, rassurer l’acheteur, et rester traduisible dans Odoo sans créer de boutique parallèle.
