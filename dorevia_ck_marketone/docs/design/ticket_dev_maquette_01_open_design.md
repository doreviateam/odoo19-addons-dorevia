# ticket_dev_maquette_01_open_design — Production maquette CK via Open Design

## 1. Objet du ticket

Ce ticket demande au Dev de piloter Open Design afin de produire une première maquette CK.

Cette maquette doit s’appuyer sur le référentiel validé :

```text
docs/design/design_01.md v1.1
```

La mission porte sur la production d’une maquette V1 opérationnelle, marchande et testable.

Elle ne déclenche aucun développement Odoo.

---

## 2. Contexte

Le projet `dorevia_ck_marketone` est actuellement en phase :

```text
Open Design → maquette → revue Dev traduisibilité → recette QA → arbitrage David
```

Le cadrage MOA a confirmé :

```text
Nous ne maquettisons pas dans Odoo.
Nous maquettisons pour Odoo.
```

À ce stade :

```text
pas de base Odoo de développement
pas de module dorevia_ck_theme
pas de QWeb
pas de SCSS
pas de reprise automatique de dorevia_ckreyol_marketone
```

Open Design est utilisé comme outil de production de maquette, piloté par le Dev.

---

## 3. Rôles

```text
David = porteur de vision / décision MOA / arbitrage final
Loulou = cadrage MOA / doctrine / formalisation / critères
Dev = exécution et pilotage opérationnel d’Open Design
QA = recette maquette / parcours / preuves à l’écran
```

Le Dev utilise Open Design comme atelier de maquette.

Le Dev ne démarre pas de développement Odoo dans le cadre de ce ticket.

---

## 4. Source de référence

Document de référence obligatoire :

```text
docs/design/design_01.md v1.1
```

Le Dev doit respecter notamment :

- les écrans phase 1 ;
- les contraintes Odoo ;
- les interactions autorisées ;
- les interdits UX ;
- les preuves à l’écran ;
- l’annotation traduction Odoo par composant ;
- les règles mobile-first ;
- l’exigence de tokens design avant validation AMOA.

---

## 5. Objectif de la mission

Produire une première maquette CK V1 couvrant :

```text
Accueil
/shop
Fiche produit — layout achat
```

La maquette doit permettre à David, Loulou et QA d’évaluer :

- la promesse CK ;
- l’efficacité marchande ;
- la lisibilité de l’offre ;
- la visibilité des produits ;
- la visibilité des prix ;
- la clarté des CTA ;
- la réassurance ;
- la présence secondaire du B2B ;
- la compatibilité avec une future traduction Odoo.

---

## 6. Nature attendue de la maquette

La maquette attendue est une V1 opérationnelle.

Elle doit être :

```text
marchande
vivante
gourmande
claire
rassurante
mobile-first
testable QA
relisible Dev
compatible Odoo
```

Elle n’a pas vocation à remplacer une direction artistique définitive produite par un directeur artistique senior.

Elle doit être suffisamment qualitative pour permettre un arbitrage MOA et une recette maquette.

---

## 7. Écrans à produire

### 7.1 Accueil

L’accueil doit répondre rapidement à :

```text
Qu’est-ce que CK vend ?
Pourquoi acheter ici ?
Où commencer ?
```

Éléments attendus :

- promesse claire ;
- CTA principal vers la boutique ;
- signal secondaire vers les professionnels ;
- catégories fortes ;
- produits ou packs mis en avant ;
- réassurance livraison / paiement ;
- mention de la logique de sourcing ;
- ton vivant et gourmand.

L’accueil ne doit pas devenir une page éditoriale longue avant achat.

---

### 7.2 Page `/shop`

La page boutique est le cœur de la maquette.

Éléments attendus :

- header / navigation ;
- titre boutique ;
- promesse courte ;
- zone filtres ;
- catégories ;
- origines visibles mais source Odoo non figée ;
- collections / packs visibles si utile mais source Odoo non figée ;
- toolbar / tri ;
- grille produits ;
- cartes produits ;
- prix lisibles ;
- CTA achat ou accès rapide ;
- réassurance ;
- entrée pro secondaire ;
- pagination ou chargement ;
- état vide si pertinent.

La page `/shop` doit rester compatible avec `website_sale`.

---

### 7.3 Fiche produit — layout achat

La fiche produit doit permettre de décider l’achat.

Éléments attendus :

- grande image produit ;
- nom produit clair ;
- prix très lisible ;
- format / poids ;
- origine ;
- catégorie ;
- quantité ;
- CTA achat visible ;
- réassurance livraison / paiement ;
- court texte d’usage ;
- signal pack ou pro si utile ;
- produits liés ou suggestions si utile.

La fiche produit ne doit pas créer de checkout parallèle.

---

## 8. Hors périmètre

Ce ticket exclut explicitement :

```text
création base Odoo
développement Odoo
module dorevia_ck_theme
SCSS Odoo
QWeb Odoo
reprise de code dorevia_ckreyol_marketone
panier complet
checkout complet
portail revendeur
workflow devis B2B
listes de prix pro dynamiques
mécanique logistique complète
catalogue JS local comme cible
panier custom
checkout custom
front React/Vue autonome
```

---

## 9. Contraintes Open Design

Le Dev peut utiliser Open Design pour :

- produire les écrans ;
- explorer une direction visuelle ;
- générer ou structurer des artefacts HTML ;
- documenter les tokens ;
- annoter les composants ;
- préparer les exports utiles à la revue.

Mais Open Design ne doit pas devenir :

```text
une application front autonome
une bibliothèque importée dans Odoo
une source de vérité catalogue
une source de vérité prix
une source de vérité panier
un checkout alternatif
```

Le JavaScript de démonstration éventuellement présent dans l’artefact Open Design doit être considéré comme démonstration UX, jamais comme spécification Odoo.

---

## 10. Contraintes Odoo à respecter dans la maquette

La maquette doit rester compatible avec Odoo.

Règles :

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

Interactions autorisées :

```text
liens Odoo
navigation URL
rechargement de page
filtres traduits en URL / domaine
accordéons visuels
drawer mobile pour filtres
CTA vers panier Odoo
```

Interactions à éviter comme cible :

```text
filtrage catalogue purement JS
panier localStorage
checkout custom
état boutique autonome
API front dédiée sans nécessité
```

---

## 11. Annotation attendue par composant

Chaque composant structurant de la maquette doit être annoté selon la logique :

```text
Composant
→ Lecture design
→ Traduction Odoo probable
→ Couche : thème / template / extension éventuelle / à trancher
→ Statut phase 1
```

Les composants suivants doivent au minimum être couverts :

- header ;
- recherche ;
- hero accueil ;
- catégories ;
- origines ;
- collections ;
- packs ;
- carte produit ;
- prix ;
- filtre prix ;
- tri ;
- pagination ;
- état vide ;
- quick-add éventuel ;
- fiche produit ;
- quantité ;
- produits liés ;
- bandeau réassurance ;
- entrée pro ;
- panier ;
- checkout.

Règles spécifiques :

```text
Origines = visibles en maquette, source Odoo à décider.
Collections = visibles en maquette, mécanique Odoo à décider.
Filtre prix = visible en maquette possible, traduction à décider.
Quick-add = action Odoo standard ou décision ultérieure, jamais panier custom.
Entrée pro = page d’intention ou formulaire, pas portail B2B.
Packs = visibles comme produit/carte/prix, pas moteur pack autonome.
```

---

## 12. Mobile-first

La maquette doit inclure une lecture mobile-first.

Règles attendues :

```text
Grille mobile : 1 colonne, éventuellement 2 selon largeur.
Filtres mobile : drawer, accordéon ou panneau repliable.
CTA achat : visible sans effort.
Prix : lisible sur carte et fiche.
Réassurance : accessible sans chercher.
Header : compact et lisible.
Images : suffisamment grandes.
B2B : présent mais secondaire.
```

Le mobile ne doit pas être une simple réduction du desktop.

---

## 13. Tokens design attendus

Avant validation AMOA, la direction visuelle doit être documentée en tokens.

Tokens minimaux attendus :

```text
couleurs principales
couleurs secondaires
couleurs de fond
couleurs CTA
couleurs prix
couleurs badges
typographies
tailles de titres
tailles de textes
espacements
rayons / radius
ombres
grille responsive
```

Règle :

> Une direction visuelle ne peut pas être validée uniquement “à l’œil”. Elle doit pouvoir être traduite en variables SCSS et en règles de thème Odoo.

---

## 14. Preuves à l’écran attendues

La maquette doit rendre observables les preuves suivantes :

```text
□ Un acheteur comprend vite ce que CK vend.
□ Les catégories principales sont visibles.
□ Les produits sont visibles et désirables.
□ Les prix sont lisibles.
□ Le CTA achat est clair.
□ La fiche produit permet de décider.
□ La réassurance est visible.
□ L’entrée pro existe sans dominer.
□ La maquette ne suppose pas de boutique parallèle.
□ Les origines, collections, packs et filtres prix sont annotés avec leur source Odoo à décider.
□ Le quick-add éventuel ne suppose pas de panier custom.
□ L’entrée pro renvoie à une intention ou un formulaire, pas à un portail B2B complet.
□ La palette retenue est documentée en tokens.
```

---

## 15. Décisions métier à respecter

Les décisions suivantes doivent être respectées dans la maquette :

```text
Packs : ne pas recréer de checkout parallèle.
Packs non_detailed : la maquette peut représenter un pack comme 1 produit / 1 carte / 1 prix.
Collections : visibles en maquette, source Odoo à trancher plus tard.
Origines : visibles en maquette, source Odoo à trancher plus tard.
Prix B2B : pas de mécanique de prix pro en phase 1.
Entrée pro : signal ou page d’intention, pas portail revendeur.
Quick-add : jamais panier custom.
```

Point restant à arbitrer plus tard par David avant traduction Odoo :

```text
Packs non_detailed = doctrine opposable pour l’implémentation Odoo ?
```

Ce point n’est pas bloquant pour la maquette.

---

## 16. Livrables attendus

Le Dev doit livrer :

1. une maquette accueil ;
2. une maquette `/shop` ;
3. une maquette fiche produit — layout achat ;
4. une lecture mobile ou responsive pour les écrans clés ;
5. une liste de tokens design ;
6. une annotation composant → Odoo ;
7. une note courte expliquant les choix visuels ;
8. une note courte signalant les points à arbitrer avant traduction Odoo.

Les livrables peuvent être produits sous forme :

```text
artefact Open Design
HTML exportable
captures
zip
documentation markdown
ou combinaison de ces formats
```

---

## 17. Critères d’acceptation

Le ticket est acceptable si :

```text
□ Les trois écrans phase 1 sont produits.
□ La maquette est cohérente avec design_01.md v1.1.
□ Les produits, prix et CTA sont visibles.
□ La fiche produit permet de décider l’achat.
□ Le B2B est visible mais secondaire.
□ Le mobile est pris en compte.
□ Les tokens sont documentés.
□ Les composants structurants sont annotés.
□ Les interactions ne supposent pas de boutique parallèle.
□ Les points à trancher sont explicitement listés.
□ Aucun développement Odoo n’a été réalisé.
```

---

## 18. Retour attendu du Dev

Le Dev doit fournir un retour structuré :

```text
1. Livrables produits
2. Écrans couverts
3. Direction visuelle retenue
4. Tokens documentés
5. Composants annotés
6. Points conformes au référentiel
7. Points d’écart ou d’attention
8. Points à arbitrer par David
9. Limites de la maquette
10. Proposition de suite
```

---

## 19. Rappel de gouvernance

Ce ticket est une mission de maquette.

Il ne constitue pas :

```text
un ticket de développement Odoo
un go pour créer une base de dev
un go pour créer dorevia_ck_theme
un go pour écrire du QWeb
un go pour écrire du SCSS Odoo
un go pour reprendre dorevia_ckreyol_marketone
```

Décision :

> Le Dev pilote Open Design pour produire une maquette.  
> David et Loulou arbitrent.  
> QA recette la maquette.  
> La revue de traduisibilité Odoo vient après livraison de la maquette.

---

## 20. Synthèse

Mission :

> Produire une première maquette CK V1 via Open Design, couvrant accueil, `/shop` et fiche produit, à partir de `design_01.md v1.1`, sans développement Odoo, avec tokens, mobile-first, preuves à l’écran et annotation composant → Odoo.

Phrase finale :

> Cette maquette doit permettre de voir si CK peut devenir un site marchand Odoo vivant, gourmand et efficace, sans déplacer la vérité métier hors d’Odoo.
