Tu es une IA de développement senior spécialisée Odoo 19 Community Edition.

Nous allons créer un nouveau module Odoo nommé :

`dorevia_ckreyol_marketone`

Ce module repart de zéro, mais doit s’inspirer intelligemment du module existant :

`dorevia_ckreyol_marketplace`

Important :
Ne copie pas mécaniquement l’ancien module. Il sert de référence conceptuelle, pas de base à dupliquer.

---

## Objectif général

Concevoir puis développer progressivement un nouveau module e-commerce C-Kreyol plus propre, plus sobre, plus maintenable, en conservant les apprentissages du module actuel.

C-Kreyol (`CK`) est un canal e-commerce éditorialisé autour de **produits issus de territoires créolophones** (zones où l'on parle créole). Ce n'est ni un simple site antillais, ni une boutique exotique, ni un marketplace générique, ni un site uniquement agro-transformé.

Doctrine produit détaillée : `cadrage/ARCHITECTURE.md` §2 et `cadrage/DECISIONS.md` ADR-018.

Le site doit être crédible, retail, mobile-first, clair, et compatible avec une ouverture commerciale réelle.

---

## Doctrine technique

* Odoo 19 Community Edition.
* Standard Odoo d’abord.
* `website_sale` reste le moteur e-commerce principal.
* Le spécifique doit surtout porter sur le front, l’UX, l’éditorial et la navigation.
* Ne pas recréer un moteur catalogue, panier, checkout ou paiement parallèle.
* Éviter les XPaths fragiles et les surcharges lourdes.
* Ajouter les dépendances seulement quand elles sont nécessaires.
* Ne pas reprendre la dette historique de `dorevia_ckreyol_marketplace`.

Formule de référence :

> Odoo vend.
> Marketone présente, clarifie, oriente.

---

## Module cible

Nom technique :

`dorevia_ckreyol_marketone`

Dépendances initiales recommandées :

* `website`
* `website_sale`
* `portal`

Dépendances à garder optionnelles tant qu’un besoin clair n’est pas validé :

* `website_sale_wishlist`
* `website_crm`
* `mass_mailing`
* `product_pack`
* thème tiers comme `theme_classic_store`

---

## Mission demandée

Avant tout développement, tu dois :

1. Analyser le module existant `dorevia_ckreyol_marketplace`.
2. Identifier ce qu’il faut conserver comme principes.
3. Identifier ce qu’il faut éviter de reprendre.
4. Proposer l’architecture cible du nouveau module.
5. Proposer un plan de développement progressif par lots.
6. Ne produire le socle minimal du module qu’après validation humaine explicite.

Important :
Aucun fichier Python, XML, SCSS ou JS ne doit être généré avant validation du cadrage.

---

## Ce qu’il faut conserver de l’ancien module

* La doctrine “standard Odoo d’abord”.
* La séparation claire entre modèles, contrôleurs, vues, assets, données, tests et documentation.
* La logique de contrats fonctionnels documentés.
* Les tests par périmètre : homepage, boutique, panier, checkout, newsletter, etc.
* La centralisation des filtres catalogue dans les hooks Odoo au lieu de logiques front parallèles.
* Le soin apporté à l’expérience mobile.
* L’idée de portes catalogue, mais seulement après stabilisation du socle.

---

## Ce qu’il ne faut pas reprendre tel quel

* L’historique long du manifeste.
* Les migrations anciennes.
* Les correctifs successifs accumulés.
* Les surcharges CSS défensives trop spécifiques.
* Les XPaths conçus pour réparer des thèmes ou états anciens.
* La dette documentaire contradictoire.
* Les fonctionnalités non indispensables au premier socle.
* Les dépendances non strictement nécessaires.
* Les logiques qui doublonnent `website_sale`.

---

## Architecture cible recommandée

Structure initiale proposée :

```text
dorevia_ckreyol_marketone/
├── __init__.py
├── __manifest__.py
├── controllers/
│   ├── __init__.py
│   └── main.py
├── models/
│   ├── __init__.py
│   └── website.py
├── security/
│   └── ir.model.access.csv
├── data/
├── views/
│   ├── layout/
│   │   └── website_layout.xml
│   ├── pages/
│   │   ├── home.xml
│   │   └── shop.xml
│   └── snippets/
│       └── snippets.xml
├── static/
│   └── src/
│       ├── scss/
│       │   ├── marketone.scss
│       │   ├── _tokens.scss
│       │   ├── _layout.scss
│       │   ├── _home.scss
│       │   ├── _shop.scss
│       │   └── _product.scss
│       └── js/
│           └── marketone.js
├── tests/
│   ├── __init__.py
│   └── test_marketone_smoke.py
└── docs/
    ├── README.md
    ├── cadrage/
    │   ├── BRIEF_INITIAL.md
    │   ├── ARCHITECTURE.md
    │   ├── CONTRACTS.md
    │   └── DECISIONS.md
    ├── pilotage/
    │   └── ROADMAP.md
    ├── recette/
    │   └── ENV_REFERENCE.md
    └── tickets/
```

Les fichiers `cadrage/CONTRACTS.md` et `cadrage/DECISIONS.md` sont importants : ils doivent permettre de conserver une mémoire propre des arbitrages sans polluer le manifeste ou le code.

---

## Lots de développement proposés

### Lot 0 — Cadrage et audit de l’ancien module

Objectif : extraire les enseignements sans copier.

Livrables attendus :

```text
docs/README.md
docs/cadrage/BRIEF_INITIAL.md
docs/cadrage/ARCHITECTURE.md
docs/pilotage/ROADMAP.md
docs/cadrage/CONTRACTS.md
docs/cadrage/DECISIONS.md
```

Décisions à figer :

* `website_sale` reste moteur.
* `/shop` reste route centrale.
* Aucun moteur catalogue parallèle.
* Pas de B2B/B2C avancé au socle initial.
* Pas de thème tiers obligatoire.
* Mobile-first dès le départ.
* Pas de reprise mécanique de l’ancien module.

Critère GO :

```text
Le cadrage est lisible, sobre, validable par un humain, et permet ensuite de générer le socle technique sans ambiguïté.
```

---

### Lot 1 — Socle module installable

Objectif : créer un module Odoo 19 CE vide mais propre.

Contenu attendu :

* manifeste ;
* dépendances minimales ;
* fichiers `__init__.py` ;
* contrôleur vide ou minimal ;
* modèle `website.py` minimal ;
* assets SCSS/JS déclarés ;
* test smoke d’installation ;
* documentation initiale.

Critère GO :

```text
Le module s’installe sans erreur sur une base Odoo 19 CE avec website_sale.
```

---

### Lot 2 — Identité front minimale

Objectif : poser une empreinte C-Kreyol légère.

Contenu possible :

* tokens SCSS ;
* classes propres ;
* quelques sections home simples ;
* pas de hero rotatif au départ ;
* pas de JS inutile ;
* layout sobre.

Critère GO :

```text
La home est identifiable C-Kreyol sans casser le thème Odoo.
```

---

### Lot 3 — Boutique /shop propre

Objectif : améliorer la lisibilité de la boutique sans réinventer `website_sale`.

Contenu possible :

* micro-ajustements visuels ;
* meilleure respiration mobile ;
* cartes produits plus lisibles ;
* CTA visibles ;
* cohérence prix / image / titre ;
* aucune logique catalogue parallèle.

Critère GO :

```text
La page /shop reste une page website_sale standard, mais plus claire et plus retail.
```

---

### Lot 4 — Fiche produit

Objectif : rendre la fiche produit crédible pour l’ouverture commerciale.

Contenu possible :

* promesse courte ;
* origine informative ;
* blocs éditoriaux simples ;
* réassurance ;
* lisibilité mobile.

Attention : uniquement si les données sont propres.

Garde-fous doctrine (ADR-018) :

* le produit et le CTA d'achat restent prioritaires ;
* récit et savoir en appui, pas en substitution de l'achat ;
* ne pas transformer la fiche en article encyclopédique.

Critère GO :

```text
Une fiche produit peut être consultée, comprise et ajoutée au panier sans friction.
```

---

### Lot 5 — Panier / checkout smoke

Objectif : sécuriser le tunnel standard.

Contenu attendu :

* tests panier ;
* tests checkout minimal ;
* pas de refonte checkout ;
* éventuels micro-ajustements visuels.

Critère GO :

```text
Un client invité peut ajouter au panier et progresser dans le tunnel sans erreur 500 ni rupture visuelle majeure.
```

---

### Lot 6 — Portes catalogue

Objectif : réintroduire prudemment l’idée de portes catalogue.

Uniquement après stabilisation :

* home ;
* shop ;
* product ;
* cart ;
* checkout.

Portes possibles :

* Promotions ;
* Incontournables ;
* Kits/Packs ;
* Origines ;
* Collections.

Doctrine :

```text
Les portes orientent.
Les filtres Odoo sélectionnent.
Marketone ne crée pas un moteur parallèle.
```

---

## Premier livrable demandé

Le premier livrable attendu n’est pas du code.

Produire d’abord un ticket de cadrage :

```text
docs/tickets/TICKET_MARKETONE_LOT0_CADRAGE.md
```

Objectif du ticket :

```text
Créer le socle doctrinal du nouveau module dorevia_ckreyol_marketone avant génération du code.
```

Ce ticket doit contenir :

* objectif ;
* contexte ;
* doctrine ;
* périmètre ;
* hors périmètre ;
* architecture cible ;
* lots de développement ;
* critères GO / NO GO ;
* risques ;
* règles de non-régression ;
* décision explicite de ne pas copier l’ancien module.

---

## Contraintes fortes

* Ne pas produire de code sans validation humaine explicite.
* Ne pas copier-coller l’ancien module.
* Ne pas ajouter de dépendance opportuniste.
* Ne pas modifier la logique standard de panier / checkout / paiement.
* Ne pas créer de modèle catalogue parallèle.
* Ne pas introduire de JS si du SCSS ou du QWeb suffit.
* Ne pas documenter une ambition non implémentée comme si elle était déjà livrée.
* Ne pas mélanger dette historique et nouveau socle.
* Ne pas masquer les limites : toute réserve doit être explicitement indiquée.

---

## Organisation de travail

Chaîne de responsabilité :

```text
Architecture : David + ChatGPT
Développement : Claude IA
Qualité : Codex
```

Rôle attendu du Dev :

```text
Exécuter le ticket validé.
Ne pas redéfinir la doctrine.
Ne pas élargir le périmètre sans validation.
Signaler les incohérences ou risques avant de coder.
```

Rôle attendu de Codex ensuite :

```text
Relire.
Tester.
Détecter les régressions.
Contrôler les dépendances.
Identifier les surcharges fragiles.
Proposer des corrections.
```

Décision finale :

```text
GO / GO avec réserves / NO GO
```

reste humaine.

---

## Décision de départ à appliquer

```text
DECISION — Création de dorevia_ckreyol_marketone

Le module dorevia_ckreyol_marketone est créé comme nouveau module Odoo 19 CE.
Il s’inspire conceptuellement de dorevia_ckreyol_marketplace mais ne le copie pas.
website_sale reste le moteur e-commerce principal.
Le premier objectif est un socle sobre, maintenable, mobile-first et compatible ouverture commerciale réelle.
Le développement ne commence qu’après validation humaine du cadrage Lot 0.
```

Merci de commencer par produire uniquement le cadrage Lot 0 et le ticket `docs/tickets/TICKET_MARKETONE_LOT0_CADRAGE.md`.

Aucun code pour l’instant.
