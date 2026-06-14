# note_01 — Cadrage initial `dorevia_ck_marketone`

## 1. Décision de projet

Le nouveau projet est nommé :

```text
dorevia_ck_marketone
```

Il vise à construire une expérience e-commerce moderne pour C-Kreyol, en s’appuyant sur Odoo comme socle métier.

La doctrine retenue est la suivante :

```text
Odoo = source de vérité métier
Open Design = bibliothèque UX / référence de composants
dorevia_ck_marketone = projet global d’expérience e-commerce CK
dorevia_ck_theme = premier module concret de maîtrise visuelle
```

Le projet ne doit pas devenir une boutique parallèle ni un système propriétaire autonome qui dupliquerait Odoo.

---

## 2. Rôles et gouvernance

Notre organisation de travail est clarifiée :

```text
Nous = architectes / MOA / cadrage / doctrine / recette
Développeur = exécutant technique
Codex = assistant de préparation / test / analyse
Claude = outil gardé au chaud pour l’instant
GitHub = trace des décisions et livraisons
PR = unité de livraison
```

Règle de gouvernance :

> Le développeur choisit ses outils d’exécution, mais il ne choisit pas la doctrine produit.

Nous parlons au développeur par prompts optimisés, sous forme de tickets d’exécution structurés.

Un prompt de mission doit inclure :

- contexte ;
- objectif ;
- périmètre ;
- hors périmètre ;
- contraintes d’architecture ;
- livrables attendus ;
- critères d’acceptation ;
- interdictions ;
- tests attendus.

---

## 3. Doctrine Odoo

Odoo reste la source de vérité métier.

Les objets et flux suivants doivent rester pilotés dans Odoo :

- produits ;
- variantes ;
- catégories e-commerce ;
- prix ;
- listes de prix ;
- stock ;
- clients ;
- paniers ;
- commandes ;
- paiements ;
- factures ;
- livraison ;
- règles métier e-commerce.

Interdictions structurantes :

```text
Ne pas créer de catalogue parallèle.
Ne pas maintenir de prix hors Odoo.
Ne pas maintenir de stock hors Odoo.
Ne pas créer de panier ou checkout parallèle.
Ne pas créer de commandes hors Odoo sans synchronisation maître.
Ne pas transformer Marketone en ERP bis.
```

Phrase doctrine :

> Nous acceptons une couche d’expérience, pas une couche de dépendance.

---

## 4. Thème vs template métier

Distinction validée :

```text
Thème = apparence globale du site
Template métier = écran fonctionnel branché aux données Odoo
```

Le thème porte :

- couleurs ;
- typographies ;
- boutons ;
- espacements ;
- ombres ;
- arrondis ;
- header/footer ;
- cards ;
- badges ;
- ambiance visuelle.

Les templates métier portent :

- `/shop` ;
- fiche produit ;
- panier ;
- checkout ;
- portail client ;
- commandes ;
- factures ;
- actions métier liées aux objets Odoo.

Règle :

> Le thème habille l’expérience ; le template métier porte le comportement Odoo.

Pour CK, nous voulons totalement maîtriser le thème, mais sans casser les écrans métier Odoo.

---

## 5. Structure projet retenue

Structure de départ :

```text
dorevia_ck_marketone/
├── docs/
├── dorevia_ck_theme/
│   └── __init__.py
└── __init__.py
```

Structure cible minimale proposée :

```text
dorevia_ck_marketone/
├── docs/
│   ├── README.md
│   └── THEME_DOCTRINE.md
├── dorevia_ck_theme/
│   ├── __init__.py
│   ├── __manifest__.py
│   ├── static/
│   │   └── src/
│   │       └── scss/
│   │           └── ck_theme.scss
│   └── views/
│       └── assets.xml
└── README.md
```

---

## 6. `dorevia_ck_marketone` vs `dorevia_ck_theme`

Distinction validée :

```text
dorevia_ck_marketone = projet global / doctrine / expérience
dorevia_ck_theme = premier module Odoo concret
```

### `dorevia_ck_theme`

Rôle :

> Donner à CK une identité visuelle maîtrisée dans Odoo, sans réinventer le moteur e-commerce.

Il portera :

- palette CK ;
- typographies ;
- styles de boutons ;
- cards produits ;
- header/footer ;
- badges ;
- spacing ;
- ombres ;
- sidebar ;
- snippets/blocs CK réutilisables ;
- ajustements SCSS ;
- personnalisation du Website Builder.

### `dorevia_ck_marketone`

Rôle :

> Construire une expérience e-commerce moderne autour d’Odoo, sans créer de boutique parallèle.

Il englobe :

- thème CK ;
- organisation boutique ;
- collections ;
- univers Boutique / Culture / Savoirs ;
- règles UX ;
- éventuelle couche d’expérience enrichie ;
- futurs composants spécifiques si le standard Odoo bloque.

Phrase doctrine :

> Marketone commence comme un thème maîtrisé, pas comme une application parallèle.

---

## 7. Open Design

Open Design est retenu comme bibliothèque UX / design system de référence.

Son rôle :

- structurer la maquette ;
- inspirer les composants ;
- guider la grille ;
- guider les cards ;
- guider la sidebar ;
- guider les filtres ;
- guider les boutons ;
- guider la hiérarchie typographique ;
- guider les espacements ;
- guider le responsive.

Mais Open Design ne remplace pas Odoo.

Doctrine :

```text
Open Design donne la qualité d’expérience.
Odoo donne la vérité métier.
La maquette fait le pont entre les deux.``

Le chemin pour open-design : /Users/doreviateam/open-design
```

---

## 8. Maquette avant développement

Décision importante :

> Avant de produire le thème Odoo, nous devons produire une maquette.

La séquence retenue :

```text
1. Maquette UX / DA
2. Validation AMOA
3. Découpage en composants Odoo
4. Développement du module dorevia_ck_theme
5. Recette dans Odoo Website / eCommerce
```

La première maquette à produire doit porter sur la page boutique `/shop`, car c’est le cœur commercial.

Contenu attendu de la maquette `/shop` :

- header sobre ;
- titre “Boutique” ;
- sous-titre éditorial court ;
- sidebar : Origines, Catégories, Collections, Prix ;
- grille produit 4 ou 5 colonnes selon largeur ;
- carte produit CK ;
- image produit bien mise en valeur ;
- prix lisible ;
- badge origine / nouveauté / collection ;
- action achat claire ;
- logique responsive.

La maquette doit rester traduisible dans Odoo Website / eCommerce.

---

## 9. Séquence de travail proposée

La trajectoire retenue est :

```text
Phase 1 — Maquette
Open Design → maquette CK → validation AMOA

Phase 2 — Thème
Maquette validée → dorevia_ck_theme → recette Odoo

Phase 3 — Extensions UX
Snippets CK, blocs éditoriaux, collections, univers

Phase 4 — Marketone avancé
Seulement si Odoo standard montre une limite réelle
```

---

## 10. Rôle de Codex dans la recette

Nous nous appuierons autant que possible sur Codex pour préparer et structurer les tests manuels.

Codex peut aider à :

- transformer une spécification en checklist de recette ;
- identifier les parcours à tester ;
- relire une PR ;
- identifier les risques de régression ;
- produire des scénarios de test ;
- proposer des jeux de données ;
- rédiger un compte rendu de recette.

Mais Codex ne remplace pas la recette MOA.

Doctrine :

```text
Codex prépare le terrain.
Nous validons le métier.
Le développeur corrige.
La recette tranche.
```

Phrase de gouvernance :

> Codex assiste la recette, mais la validation reste MOA.

---

## 11. Position sur Claude

Claude est gardé au chaud pour l’instant.

La décision immédiate est de travailler avec notre développeur actuel, qui choisira ses propres outils de développement adaptés à nos demandes d’architectes / AMOA.

Claude pourra éventuellement servir plus tard d’exécutant technique ou d’assistant de développement, mais il n’est pas intégré au processus pour le moment.

---

## 12. Ligne rouge produit

Le risque identifié avec certaines approches type couche moderne / multiples apps est de recréer progressivement un système propriétaire parallèle.

La ligne rouge est donc :

> Moderniser l’expérience sans déplacer le cœur métier.

Ce que nous voulons :

```text
Odoo = moteur métier
dorevia_ck_theme = maîtrise visuelle
Open Design = référence UX
Marketone = expérience, pas ERP bis
```

Ce que nous refusons :

```text
Front autonome qui devient la vraie boutique
Multiplication d’apps indépendantes
Catalogue parallèle
Prix parallèles
Stock parallèle
Checkout parallèle
Dépendance propriétaire non maîtrisée
```

---

## 13. Phrase de synthèse

> `dorevia_ck_marketone` commence par la production d’une maquette CK appuyée sur Open Design, traduisible dans Odoo, puis par le développement d’un module `dorevia_ck_theme` permettant de maîtriser totalement l’identité visuelle de C-Kreyol sans réinventer le moteur e-commerce ni dupliquer la donnée métier Odoo.
