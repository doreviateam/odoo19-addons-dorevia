# Pattern-bloc — Home « Sélection produits »

Ce document décrit le bloc **Notre sélection du moment** sur la homepage C-Kreyol : **mise en avant marchande courte**, distincte de la grille catalogue `/shop`.

Ce n’est pas un ticket d’implémentation : cette passe **ne prescribe pas** de modification QWeb, SCSS, Python ni l’ajout d’un **snippet Odoo déposable** dans l’éditeur Website.

**Références de cadrage projet** : [`docs/mvp_02/DECISION_PRODUITS_HOMEPAGE_MVP21.md`](../../mvp_02/DECISION_PRODUITS_HOMEPAGE_MVP21.md)  
**Vocabulaire** : [`../README.md`](../README.md)

---

## 1. Intention produit

Le bloc doit :

- **Montrer une sélection limitée** de produits (cible actuelle : jusqu’à **quatre** fiches) pour donner une **preuve concrète de l’offre** dès la Home ;
- **Rendre le prix lisible** (prix « visiteur » / combinaison courante conformément aux helpers métier), pour ancrer l’aspect marchand sans détour vers une liste interminable ;
- **Inviter au détail produit** (lien carte → fiche) puis, au pied de section, vers **toute la boutique** (`/shop`) — sans remplacer le rôle du `/shop` filtré ni du Explorer.

Ce pattern répond au besoin : **voir du produit réel vite**, tout en gardant la Home lisible comme **orientation**, pas comme mini-catalogue.

---

## 2. Distinction importante (Home vs grille `/shop`)

- La sélection Home utilise les classes **`ckr-selection__*`** : principalement **`ckr-selection__card`**, médias **`ckr-selection__card__img`**, en-tête **`ckr-selection__card__head`**, **`ckr-selection__card__price`**, **`ckr-selection__card__product-cta`**, etc.
- La grille **`/shop`** repose sur le DOM **`website_sale`** et souvent **`theme_classic_store`** — **autre structure**, autres contraintes de filtre et de mise en page.
- **Ne pas fusionner** ces deux patterns dans une seule référence « card produit » : toute évolution visuelle doit préciser si elle cible **`ckr-selection`** ou **listing boutique**.

Voir aussi l’inventaire : distinction parallèle pour les cards Explorer vs cards catalogue.

---

## 3. Structure attendue

**Source QWeb** : `views/snippets/ckr_selection.xml` (template `ckr_snippet_selection`).

1. **Données** : `ckr_sel_cards` = `website.sudo()._get_ckr_homepage_selection_cards()` (nécessite un `request` HTTP — hors requête, liste vide).
2. **En-tête de section** (`ckr-section-title`) :
   - sur-titre (eyebrow + règle) : « Sélection » ;
   - titre : « Notre sélection du moment » ;
   - intro courte (alignée MVP2.1 dans le fichier).
3. **Grille** : `div.ckr-selection__grid`, `role="list"` lorsqu’il y a des cartes.
4. **Par produit** : lien carte unique (`<a class="ckr-selection__card" role="listitem">`) vers `product.website_url` :
   - **Image** carrée (ratio 1:1 en SCSS) : `listing_image_url` Odoo ou repli **`ckr-selection__card__photo-fallback`** (marque « C-K », pas l’icône générique `/web`) ;
   - **Nom** (`<h3>`) ;
   - **Prix** via widget monétaire à partir de `combination_info` ;
   - **Ligne origine** optionnelle : affichée seulement si la règle d’homogénéité côté Python est satisfaite (§9.4 / décision produits homepage) ;
   - **Texte de CTA** : « Voir le produit » (pas d’ajout panier sur la grille — intention MVP2.1).
5. **État vide** : message explicite + renvoi configuration **Site web → Configuration → Sites** (groupe C-Kreyol), `role="status"`.
6. **Sortie de section** : bouton secondaire « Voir tous les produits » → **`/shop`**.

### Alimentation des produits (résumé fonctionnel)

Implémentation : `models/website.py` — résolution jusqu’à **4** `product.template` via `_get_ckr_homepage_featured_product_list()` :

- Priorité aux **produits choisis sur le site** (`ckr_homepage_featured_1` … `_4`) s’ils sont **éligibles** (publiés, vendables, etc., voir code) ;
- **Complément automatique** parmi les modèles publiés vendables du site jusqu’à combler les emplacements libres ;
- `_get_ckr_homepage_selection_cards()` enrichit chaque ligne : image listing, infos combinaison / prix, règle d’affichage **origine**.

Toute évolution « qui apparaît sur la Home » doit rester alignée avec cette logique ou la faire évoluer **dans un ticket dédié**.

---

## 4. Règles responsive

Implémentation : `static/src/scss/components/_selection.scss`.

- **Bande** `ckr-selection--band` : respiration verticale (padding généreux), léger dégradé et filets — cohérent avec d’autres blocs MVP2.1, sans voler la vedette au hero / Explorer.
- **Grille** :
  - **&lt; 768px** : **2 colonnes** ;
  - **≥ 768px** : **4 colonnes** (une carte par intention « slot » sur une ligne complète quand il y a 4 produits).
- **Carte** : colonne flex, image carrée, titre + prix sur une ligne (titre tronqué sur 2 lignes max, prix en `nowrap`), CTA texte en bas — garde-fous déjà commentés en SCSS (MOA / accessibilité).

### Comportement avec 1, 2, 3 ou 4 produits

Le moteur peut retourner **entre 1 et 4** cartes. La grille CSS **ne centre pas** automatiquement les cartes sur une ligne : avec **peu de produits**, surtout en **desktop 4 colonnes**, des **cellules vides** peuvent apparaître visuellement (grille clairsemée). Ce n’est pas un bug documentaire : c’est un **point de recette UX** — si le MOA exige un rendu plus équilibré à 1–2 produits, il faudra un **ticket** (ajustement grid, `auto-fit`, ou règle éditoriale « toujours 4 produits publiés »).

Sur **mobile 2 colonnes**, 1 ou 3 produits donnent un **déséquilibre** classique (ligne incomplète) : acceptable si la hiérarchie reste claire ; à surveiller en recette.

Objectifs de ce pattern :

- **mobile lisible** : cartes pas « géantes » isolément grâce à la densité 2-col et au contenu resserré ;
- **éviter** une impression de **mosaïque décorative** sans prix ni nom exploitables (NO GO ci-dessous).

---

## 5. GO / NO GO

### GO

- Sélection **courte**, **claire**, **marchande** (noms + prix visibles, lien fiche explicite).
- Distinction **documentée** avec la grille `/shop` (classes et rôle produit différents).
- **Mobile** propre : cartes tactiles, focus visible clavier (styles `:focus-visible` sur la carte).
- **État vide** compréhensible pour l’éditeur (où configurer les produits).
- CTA « Voir tous les produits » renvoie au **conteneur catalogue** `/shop`, cohérent avec la doctrine d’entrée boutique.

### NO GO

- Grille **trop décorative** : belles images mais hiérarchie floue, prix illisibles ou absents.
- Cards **disproportionnées** par rapport au nombre de produits **sans** arbitrage MOA (surtout desktop).
- **Confusion** volontaire ou involontaire avec les cards du **listing** `/shop` dans la doc ou le design system (même nom de pattern pour deux DOM différents).
- **Dépendance** à des visuels **trop spécifiques** one-shot si cela casse le rendu quand les produits changent (le pattern doit rester robuste avec images catalogue ou fallback).

---

## 6. Points de vigilance

- **Vérifier** systématiquement `ckr_selection.xml` après évolution prix / `website_url` / publication produit.
- **Vérifier** les classes **`ckr-selection__card*`** lors de refactos SCSS : ne pas réutiliser les mêmes noms pour le listing boutique.
- **Données dynamiques** : la liste effective dépend du **site**, des **champs homepage** CK et du **catalogue publié** — les tests et la recette doivent prévoir bases avec 0 / 1 / 4 produits.
- **Ne pas modifier** dans cette passe documentaire les fichiers code — tout changement (ex. grille centering, 5e produit) = **ticket**.
- **Snippet Odoo déposable** : non requis ici ; si un jour Bloc Édition Website, traiter séparément (duplication données, risque de divergence avec résolution `_get_ckr_homepage_selection_cards`).
- **Compatibilité** : le rendu s’appuie sur `request` ; attention aux contextes sans requête HTTP (aperçus, certains tests) où la liste peut être vide.

---

## Statut du document

**Créé** — décrit le pattern **tel qu’implémenté** (template, classes, logique `website.py`, SCSS) et le **contraste** avec la grille `/shop`, sans ouvrir de refonte.
