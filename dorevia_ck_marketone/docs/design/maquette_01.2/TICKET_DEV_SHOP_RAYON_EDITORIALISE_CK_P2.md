# Ticket Dev — Shop CK P2 · page rayon editorialisee

| Champ | Valeur |
| --- | --- |
| Date | 2026-06-23 |
| Declencheur | Benchmark visuel avec bienmanger.com : la page CK `/shop` reste percue comme un listing produit, alors qu'une boutique mature construit d'abord une page de rayon. |
| Reference benchmark | `https://www.bienmanger.com/1L1305_Plats_Entrees.html` |
| Perimetre | `/shop` et pages categories `/shop/category/...` · en-tete de rayon · sous-familles · blocs preuves · transition vers grille produits |
| Hors perimetre | Refonte moteur filtres · logique catalogue Odoo · fiche produit · header P4 · contenus definitifs image/SEO si non disponibles |
| Modules probables | `dorevia_ck_theme` principalement · `dorevia_ck_marketone_content` si des blocs SSR/categorie doivent etre seeds |

---

## 1. Constat MOA

Le P1 a fait progresser `/shop` : intro plus compacte, sidebar plus lisible, barre catalogue plus coherente, cards mieux tenues.

Mais le benchmark montre un ecart plus profond :

```text
BienManger ne montre pas seulement une grille.
BienManger construit une page de rayon.
CK montre encore surtout un listing produit ameliore.
```

Chez CK, l'utilisateur arrive trop vite sur :

- un titre ;
- des filtres ;
- des chips categories ;
- une grille de cards.

Il manque une couche de lecture e-commerce mature :

- ou suis-je dans la boutique ;
- quels sous-univers puis-je explorer ;
- quelle promesse porte ce rayon ;
- pourquoi acheter ici ;
- comment passer naturellement du rayon aux produits.

---

## 2. Lecture benchmark

La page benchmark fonctionne car elle empile plusieurs signaux avant la grille produit :

| Signal | Effet utilisateur |
| --- | --- |
| Titre de rayon clair | On comprend immediatement l'univers marchand. |
| Sous-categories visibles | Le rayon parait profond, organise, exploratoire. |
| Bloc editorial illustre | Le rayon a une ambiance et une promesse, pas seulement des produits. |
| Preuves de service proches du contenu | Paiement, livraison, service client rassurent au moment de l'achat. |
| Texte d'introduction court | Le SEO et la promesse existent sans bloquer la lecture. |
| Sections de gamme | L'utilisateur peut naviguer par intention avant de scroller dans les produits. |

Le point important n'est pas de copier le style BienManger.

Le point important est de reprendre la grammaire :

```text
Rayon = orientation + preuve + sous-familles + produits
```

Actuellement CK est plutot :

```text
Rayon = intro courte + filtres + produits
```

---

## 3. Objectif P2

Faire passer `/shop` et les pages categories CK d'une logique de listing a une logique de rayon boutique.

Attendu MOA :

```text
Quand l'utilisateur arrive sur une page shop CK, il doit percevoir un univers marchand organise,
pas seulement une grille de produits filtrables.
```

Le rendu doit rester CK :

- chaleureux ;
- creole ;
- artisanal ;
- clair ;
- sobre ;
- non corporate sombre ;
- sans hero marketing lourd.

---

## 4. Axes Dev demandes

### 4.1 En-tete de rayon editorialise

Remplacer l'intro shop purement textuelle par un bloc compact mais plus structure.

Attendu pour `/shop` :

- titre : `Boutique C-Kreyol` ;
- sous-texte court ;
- pills de preuves CK ;
- eventuellement une image ou surface editoriale discrete si un asset propre existe.

Attendu pour `/shop/category/...` :

- titre categorie dynamique ;
- court texte de contexte si disponible ;
- fallback propre sinon ;
- aucun texte artificiel long.

Ne pas creer un hero tres haut. Le bloc doit installer le rayon, pas repousser les produits trop bas.

### 4.2 Bande de sous-familles / univers

Ajouter une zone visible de sous-familles ou univers sous l'intro, avant la grille.

Exemples CK :

Pour `/shop` :

- Epicerie ;
- Boissons ;
- Maison & Bien-etre ;
- Artisanat ;
- Coups de coeur.

Pour `Epicerie` :

- Condiments & sauces ;
- Douceurs & confitures ;
- Manioc & farines ;
- Epices & aromates ;
- Origines.

Regle importante :

```text
Aucune sous-famille vide ne doit etre exposee.
```

Si une categorie n'a pas assez de contenu, afficher moins d'entrees plutot que de creer une fausse profondeur.

### 4.3 Bloc preuve/service contextualise

Reprendre les preuves CK au niveau du shop, dans une forme legere.

Exemples :

- Origines identifiees ;
- Produits selectionnes ;
- Expedition depuis Nantes ;
- Livraison suivie.

Ce bloc ne doit pas concurrencer le header. Il doit rassurer dans le contexte d'achat.

### 4.4 Transition claire vers la grille

Avant la grille, ajouter une separation lisible :

- titre de section : `Tous les produits` ou titre categorie ;
- compteur produits ;
- tri ;
- recherche shop ;
- filtres.

La page doit raconter :

```text
Je decouvre le rayon -> je comprends les familles -> je suis rassure -> je choisis mes produits.
```

### 4.5 Sidebar filtres : conserver, mais remettre a sa place

Les filtres restent utiles, mais ils ne doivent pas etre le premier signal de maturite boutique.

Attendu :

- sidebar conservee ;
- styles P1 conserves ;
- la sidebar devient un outil secondaire de precision ;
- le haut de page doit d'abord porter l'univers marchand.

---

## 5. Contraintes techniques

- Utiliser les mecanismes Odoo natifs quand ils existent.
- Ne pas casser les pages `/shop/category/...`.
- Ne pas creer de fausses categories vides.
- Ne pas dupliquer la logique catalogue dans du HTML statique fragile.
- Les contenus editoriaux doivent avoir un fallback propre.
- Le P2 doit etre compatible desktop, tablette et mobile.

---

## 6. Livrables attendus

1. Audit rapide du rendu P1 :
   - `/shop` ;
   - une categorie alimentee ;
   - une categorie pauvre si disponible.

2. Proposition Dev P2 :
   - structure retenue ;
   - donnees disponibles ;
   - fallback contenu.

3. Implementation P2.

4. Captures avant/apres :
   - `/shop` desktop haut de page ;
   - `/shop` desktop zone grille ;
   - categorie Epicerie desktop ;
   - tablette 800 ;
   - mobile 390.

5. Verifications machine :
   - pas d'overflow horizontal ;
   - aucun lien vers categorie vide ;
   - nombre de produits stable ;
   - filtres toujours fonctionnels ;
   - tri/recherche shop toujours fonctionnels ;
   - panier rapide toujours fonctionnel.

6. Note de recette :
   - comparaison P1/P2 ;
   - decisions de structure ;
   - limites contenu ;
   - recommandations P3 eventuelles.

---

## 7. Critere de GO MOA

Le P2 sera considere reussi si la page ne lit plus comme :

```text
listing Odoo avec filtres
```

mais comme :

```text
rayon boutique CK, organise, rassurant et marchand
```

Le benchmark BienManger sert de reference de grammaire e-commerce, pas de reference graphique a copier.

---

## 8. Verdict MOA

Le P1 est utile mais insuffisant pour atteindre le niveau "boutique mature".

Le prochain saut qualitatif est un P2 de structure :

```text
editorialiser le haut de rayon
exposer les sous-familles utiles
contextualiser les preuves
mieux preparer l'entree dans la grille produit
```

Priorite recommandee : traiter d'abord `/shop`, puis generaliser aux categories seulement si le fallback contenu est robuste.

---

## 9. Arbitrage suite apres retour Dev

Le retour Dev est juste sur le fond : l'ecart avec le benchmark ne vient pas uniquement du CSS.

L'effet "boutique mature" repose sur trois couches :

| Couche | Nature | Action |
| --- | --- | --- |
| Architecture de page | Dev / theme | Faisable maintenant |
| Densite card produit | Dev / theme + donnees disponibles | Faisable maintenant |
| Editorial lifestyle / saisonnier | Contenu MOA + assets photo | A briefer avant implementation complete |

Decision MOA :

```text
Ne pas attendre tout le brief contenu pour avancer.
Mais ne pas promettre l'effet BienManger complet avec du CSS seul.
```

### 9.1 Lot P2A — faisable immediatement cote Dev

Demande :

- conserver le P1 ;
- densifier la card produit shop ;
- mieux hierarchiser marque / origine / titre / prix ;
- etudier un bouton panier plus compact ou moins dominant ;
- renforcer la structure "rayon" avec les donnees deja disponibles ;
- ne pas inventer de fausse notation si aucune donnee fiable n'existe ;
- ne pas ajouter de contenu saisonnier factice.

Pistes acceptees :

```text
Marque / producteur en petite ligne au-dessus du titre si disponible
Titre plus dense
Metadonnees origine / categorie / poids clarifiees
Prix mieux hierarchise
CTA panier moins massif si l'usage reste clair
Bouton icone panier possible uniquement si comprehensible et accessible
```

Point de vigilance :

```text
Le bouton panier plein largeur peut etre allege,
mais l'achat rapide doit rester evident.
```

### 9.2 Lot P2B — brief contenu a preparer

Pour atteindre le niveau complet du benchmark, il faudra un brief contenu par rayon.

Pour chaque rayon prioritaire :

- image lifestyle ou visuel categorie ;
- phrase editoriale courte ;
- 3 a 5 sous-familles utiles ;
- 1 a 3 mises en avant saisonnieres ou commerciales ;
- produits associes ;
- fallback si contenu insuffisant.

Rayons a prioriser :

```text
Epicerie
Boissons
Maison & Bien-etre
Artisanat si contenu suffisant
```

### 9.3 Reponse MOA au Dev

Reponse recommandee :

```text
Oui, vous pouvez attaquer maintenant la densification des cards et l'allegement du CTA panier,
mais en la traitant comme un P2A Dev faisable avec les donnees existantes.

En parallele, nous ouvrons un P2B contenu pour construire le vrai hub editorial par rayon :
photo lifestyle, mises en avant saisonnieres, annuaire de sous-categories et textes courts.

Merci de ne pas creer de notation, contenu saisonnier ou profondeur de rayon artificiels.
La cible BienManger est une reference de grammaire e-commerce, pas une promesse realisable
sans assets et brief contenu.
```
