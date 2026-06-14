# note_03 — Vision CK, arbitrage MOA et réponse au retour Dev

## 1. Objet de la note

Cette note complète `note_01.md` et tient compte des retours du Dev sur :

- l’existence de `dorevia_ckreyol_marketone` ;
- le rôle réel d’Open Design ;
- le risque de repartir de zéro sans tenir compte de l’existant ;
- la frontière entre thème Odoo, templates métier et couche applicative ;
- la volonté MOA de reprendre la trajectoire CK sur une base plus simple et plus maîtrisée.

Elle acte une décision importante :

> Nous ne repartons pas de zéro par ignorance de l’existant.  
> Nous repartons presque de zéro parce que la trajectoire produit doit être réalignée sur une doctrine plus simple, plus lisible et plus proche d’Odoo.

---

## 2. Vision CK

CK n’est pas seulement un site e-commerce de produits créoles.

CK a vocation à devenir une plateforme de sourcing, de commerce et de logistique pour les productions agro-transformées issues des zones créoles.

Phrase fondatrice :

> CK a pour ambition de sourcer, valoriser et distribuer les productions agro-transformées du monde créole, en assurant le lien logistique entre la porte du producteur et la porte de l’acheteur, en B2B comme en B2C.

Le périmètre initial est volontairement centré sur l’agro-transformé :

- farines ;
- galettes ;
- biscuits ;
- confitures ;
- sauces ;
- piments ;
- épices ;
- condiments ;
- boissons non alcoolisées ;
- conserves ;
- préparations culinaires ;
- produits à base de manioc ;
- coffrets et packs découverte.

Ce périmètre est déjà suffisamment large pour constituer une première phase ambitieuse.

---

## 3. Positionnement métier

CK doit articuler trois promesses.

### 3.1 Sourcer

Identifier, sélectionner et valoriser :

- producteurs ;
- artisans ;
- transformateurs ;
- marques locales ;
- petites unités agroalimentaires ;
- produits traditionnels ;
- produits rares ou peu distribués ;
- nouveautés issues des zones créoles.

### 3.2 Vendre

Proposer ces produits dans un parcours e-commerce clair, en B2C et en B2B :

- catalogue lisible ;
- catégories fortes ;
- prix visibles ;
- packs ;
- offres professionnelles ;
- commande simple ;
- paiement ;
- suivi.

### 3.3 Acheminer

Organiser la chaîne logistique :

- collecte ou expédition depuis le producteur ;
- regroupement éventuel ;
- stockage éventuel ;
- préparation de commande ;
- transport ;
- suivi ;
- livraison jusqu’à la porte de l’acheteur.

La promesse CK n’est donc pas uniquement visuelle ou éditoriale. Elle est commerciale et logistique.

---

## 4. Doctrine produit

La doctrine produit est réaffirmée :

```text
Odoo = source de vérité métier
Open Design = atelier de maquette et référentiel UX
dorevia_ck_theme = première implémentation visuelle maîtrisée dans Odoo
dorevia_ck_marketone = trajectoire projet CK, non app autonome par défaut
```

Règle centrale :

> Odoo vend. CK présente, valorise, structure l’expérience et organise la promesse commerciale.

Ce que nous voulons :

```text
Un vrai site Odoo
Un thème CK maîtrisé
Une expérience e-commerce claire
Une capacité B2C et B2B
Une identité propre
Une logistique pilotable
Une donnée métier centralisée dans Odoo
```

Ce que nous refusons :

```text
Une boutique parallèle
Un catalogue parallèle
Un panier parallèle
Un checkout parallèle
Une multiplication d’apps propriétaires
Une logique front autonome
Un Marketone qui deviendrait l’ERP bis de CK
```

---

## 5. Correction de direction artistique

Les éléments de direction artistique précédemment évoqués ne sont plus reconduits automatiquement.

Sont considérés comme historiques, non comme cible actuelle :

- terracotta ;
- sauge ;
- crème ;
- pastel premium ;
- warm-editorial comme direction imposée ;
- ancien prototype CK comme référence visuelle directe.

Décision MOA :

> La direction visuelle CK est réouverte.

Le futur site doit être :

- marchand ;
- vivant ;
- clair ;
- gourmand ;
- efficace ;
- professionnel ;
- rassurant ;
- orienté achat ;
- capable de porter une vraie profondeur catalogue ;
- capable de parler à la fois aux particuliers et aux acheteurs professionnels.

L’inspiration récente se rapproche davantage de sites marchands efficaces de type `directos.eu`, non pas pour copier leur identité graphique, mais pour retenir leur efficacité commerciale :

- promesse immédiate ;
- catégories très lisibles ;
- produits visibles ;
- prix lisibles ;
- réassurance ;
- ton vivant ;
- packs ;
- contenus utiles autour de l’achat ;
- orientation forte vers la conversion.

Phrase de cadrage :

> CK ne doit pas être une galerie décorative. CK doit être un vrai site marchand, vivant, gourmand et structuré, capable de rendre visible une filière.

---

## 6. Rôle d’Open Design après retour Dev

Le retour Dev confirme que la doctrine est tenable si Open Design est traité comme :

```text
atelier de maquette + référentiel visuel
```

et non comme :

```text
librairie importable
couche applicative
stack front autonome
application React/Vue à embarquer dans Odoo
```

Lecture validée :

```text
Open Design produit la maquette cible et le DESIGN.md CK.
Odoo produit le comportement métier.
Le thème Odoo est la première implémentation visuelle.
```

Chaîne cible :

```text
DESIGN.md CK
    → maquette HTML cible Open Design
        → validation AMOA
            → tokens SCSS + structure QWeb minimale
                → module thème Odoo
                    → données & flux = Odoo natif website_sale
```

Open Design doit servir à :

- construire la direction visuelle CK ;
- produire une maquette cible ;
- critiquer les choix UX ;
- comparer plusieurs directions ;
- formaliser un `DESIGN.md` CK ;
- préparer la traduction vers Odoo.

Open Design ne doit pas :

- se brancher à Odoo ;
- gérer le catalogue ;
- gérer les prix ;
- gérer le stock ;
- gérer le panier réel ;
- gérer le checkout ;
- générer une application autonome ;
- être copié tel quel dans Odoo.

Chemin local Open Design sur le poste de travail :

```text
/Users/doreviateam/open-design
```

---

## 7. Rapport à l’existant `dorevia_ckreyol_marketone`

Le retour Dev rappelle l’existence d’un module déjà avancé :

```text
dorevia_ckreyol_marketone
```

avec :

- vues ;
- SCSS ;
- tests ;
- documentation ;
- ADR ;
- recettes ;
- sidebar ;
- collections ;
- packs ;
- portes SEO ;
- décisions MOA passées.

Ce retour est techniquement juste.

Cependant, la décision MOA est la suivante :

> `dorevia_ck_marketone` n’est pas la poursuite automatique de `dorevia_ckreyol_marketone`.

L’existant est reconnu comme :

```text
matière d’analyse
mémoire fonctionnelle
réservoir d’apprentissages
source de scénarios de recette
base de comparaison
```

Mais il n’est pas validé comme :

```text
socle obligatoire
continuité technique automatique
architecture cible
modèle applicatif à prolonger sans arbitrage
```

Phrase d’arbitrage :

> L’existant n’est pas ignoré, mais il n’impose pas la suite. Il est analysé à la lumière de la nouvelle doctrine CK.

---

## 8. Pourquoi repartir presque de zéro

La reprise quasi greenfield est assumée pour des raisons de doctrine produit.

Le risque identifié dans l’ancienne trajectoire est le suivant :

```text
Odoo devient un simple back-office.
Marketone devient la vraie boutique.
Des apps spécifiques se multiplient.
La logique commerciale se disperse.
La dépendance technique augmente.
Le projet devient plus propriétaire que nécessaire.
```

Ce risque est incompatible avec la doctrine actuelle.

Décision :

> Nous repartons presque de zéro pour éviter d’hériter d’une trajectoire qui ne correspond plus à la vision produit.

Mais cette reprise n’est pas une remise à zéro naïve :

```text
On garde les apprentissages.
On garde les alertes.
On garde les scénarios utiles.
On garde les décisions encore pertinentes.
On ne garde pas automatiquement le code ni les modèles.
```

---

## 9. Frontière thème / template métier / extension

La frontière validée est la suivante.

### 9.1 Thème

Relève du thème ce qui concerne l’apparence et peut être retiré sans casser le comportement e-commerce.

Exemples :

- tokens SCSS ;
- couleurs ;
- typographies ;
- espacements ;
- radius ;
- ombres ;
- bordures ;
- header/footer ;
- boutons ;
- badges ;
- chips ;
- cartes visuelles ;
- habillage sidebar ;
- blocs éditoriaux ;
- snippets purement visuels ;
- assets.

Règle pratique :

> Si on retire uniquement les assets du thème et que l’ajout au panier fonctionne encore, c’est probablement du thème.

### 9.2 Template métier

Relève du template métier tout élément qui lit ou écrit la vérité Odoo.

Exemples :

- grille produits ;
- prix affichés ;
- variantes ;
- disponibilité ;
- catégories e-commerce ;
- filtres ;
- ajout au panier ;
- panier ;
- checkout ;
- tri ;
- pagination ;
- état vide ;
- fiche produit ;
- compte client ;
- commandes ;
- règles de livraison.

Règle pratique :

> Si l’élément dépend de `website_sale`, des produits, des prix, du stock ou du panier, ce n’est plus du thème pur.

### 9.3 Extension Marketone

Une extension Marketone ne doit être envisagée que si Odoo standard + thème ne suffisent pas.

Elle doit être justifiée par :

- un besoin métier écrit ;
- une limite Odoo identifiée ;
- une décision MOA explicite ;
- des critères d’acceptation ;
- des tests ;
- une absence de duplication catalogue/prix/stock/panier/checkout.

---

## 10. Ligne rouge applicative

Les signaux d’alerte sont les suivants :

| Risque | Symptôme | Décision |
|---|---|---|
| Catalogue parallèle | Produits filtrés ou stockés hors Odoo | Interdit |
| Panier simulé | État panier en JS/localStorage | Interdit |
| Prix hors Odoo | Prix codés dans HTML/JS | Interdit |
| Stock hors Odoo | Disponibilité non issue d’Odoo | Interdit |
| Checkout parallèle | Tunnel commande hors `website_sale` | Interdit |
| App front autonome | React/Vue/SPA embarquée comme boutique | Interdit |
| API boutique custom | Endpoints JSON catalogue/panier sans nécessité | À refuser par défaut |
| Multiplication d’apps | Une app par besoin UX | À éviter strictement |

Les petits JS de maquette Open Design peuvent exister comme démonstration UX, mais ne doivent jamais être interprétés comme une spécification technique Odoo.

---

## 11. Nouvelle séquence de travail

La séquence projet est révisée.

### Phase 1 — Direction et maquette

1. Créer un `DESIGN.md` CK dédié dans Open Design.
2. Ne pas reprendre automatiquement l’ancienne palette.
3. Produire une ou plusieurs directions visuelles.
4. Valider une direction AMOA.
5. Produire la maquette cible `/shop`.

### Phase 2 — Grille de traduction Odoo

Pour chaque écran, produire une grille :

```text
Élément de maquette
→ thème pur
→ template métier Odoo
→ extension éventuelle
→ source de vérité
→ critères d’acceptation
```

Écrans prioritaires :

- accueil ;
- `/shop` ;
- fiche produit ;
- panier ;
- checkout ;
- page B2B / revendeurs ;
- page producteur / origine ;
- contenus éditoriaux utiles à l’achat.

### Phase 3 — Thème Odoo

Créer ou stabiliser `dorevia_ck_theme` seulement après validation de la maquette.

Le thème doit viser :

- tokens ;
- header/footer ;
- style global ;
- cards ;
- sidebar visuelle ;
- boutons ;
- badges ;
- snippets décoratifs ;
- cohérence responsive.

### Phase 4 — Extensions minimales

N’ajouter une extension Marketone que si :

```text
Odoo standard + thème ne suffisent pas
```

et uniquement après arbitrage MOA explicite.

---

## 12. Réponse au Dev — position MOA

Réponse à transmettre ou à intégrer dans l’échange Dev :

> Merci pour ton retour.  
> Ta lecture de l’existant est juste et utile : nous ne devons pas ignorer `dorevia_ckreyol_marketone`, ses documents, ses recettes, ses ADR et les décisions déjà prises.  
>  
> En revanche, la décision MOA est de ne pas prolonger automatiquement cette trajectoire. Ce qui nous fait tiquer, c’est le risque de transformer progressivement Odoo en simple back-office et Marketone en vraie boutique autonome, avec multiplication d’apps et dette propriétaire.  
>  
> Nous assumons donc une reprise quasi greenfield, non par ignorance de l’existant, mais pour réaligner CK sur une doctrine plus simple : Odoo reste la source de vérité métier, Open Design sert d’atelier de maquette, le thème Odoo porte l’identité visuelle, et toute extension métier doit être justifiée par une limite réelle du standard.  
>  
> L’existant sera utilisé comme matière d’analyse, mémoire fonctionnelle et source de scénarios de recette, mais il ne constitue pas automatiquement la base technique à poursuivre.  
>  
> La prochaine étape n’est donc pas de développer `dorevia_ck_theme`, mais de produire un `DESIGN.md` CK réouvert, puis une maquette cible `/shop` validée AMOA. Ensuite seulement nous déciderons ce qui relève du thème, du template métier Odoo ou d’une extension Marketone minimale.

---

## 13. Livrables immédiats attendus

Les livrables immédiats sont :

1. `DESIGN.md` CK dans Open Design ;
2. une maquette cible `/shop` ;
3. une grille thème / template métier / extension ;
4. une analyse de l’existant `dorevia_ckreyol_marketone` uniquement comme matière de comparaison ;
5. une décision explicite avant tout développement Odoo.

---

## 14. Synthèse

La trajectoire CK est désormais :

```text
Vision filière agro-transformée créole
    → site marchand Odoo vivant et efficace
        → Open Design pour maquette et DESIGN.md
            → validation AMOA
                → thème Odoo maîtrisé
                    → extensions minimales seulement si nécessaire
```

Phrase de synthèse :

> CK ne doit pas devenir une surcouche propriétaire au-dessus d’Odoo. CK doit devenir un vrai site marchand Odoo, maîtrisé par Dorevia, capable de sourcer, valoriser, vendre et acheminer les productions agro-transformées du monde créole en B2C et en B2B.
