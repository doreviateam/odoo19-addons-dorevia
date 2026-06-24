# Ticket Dev — Shop CK V1 · polish boutique mature

| Champ | Valeur |
| --- | --- |
| Date | 2026-06-23 |
| Déclencheur | Recette visuelle `/shop` après validation Header P4 : le header lit désormais « enseigne », mais la page boutique reste trop proche d'un listing Odoo propre. |
| Périmètre | Page `/shop` desktop/tablette/mobile · intro boutique · filtres · toolbar · grille produits · cards shop |
| Hors périmètre | Moteur de recherche Odoo · facettes natives · logique catalogue · fiche produit · header P4 · contenus définitifs produits |
| Modules probables | `dorevia_ck_theme` principalement · `dorevia_ck_marketone_content` seulement si contenu/SSR doit être re-baké |

---

## 1. Diagnostic MOA

La page `/shop` est fonctionnelle et les cards produits sont déjà plus solides que l'état initial, mais le rendu global reste en dessous du niveau atteint par le header P4.

Constats sur capture desktop 1280 :

| Zone | Constat |
| --- | --- |
| Intro shop | H1 très grand, beaucoup de blanc, texte utile mais peu marchand. L'intro répète la marque sans orienter assez vite vers l'achat. |
| Filtres gauche | Bloc fonctionnel mais sec : `Étiquettes`, prix, cases à cocher. Peu de hiérarchie, peu de chaleur CK, pas assez de lecture « outil boutique ». |
| Zone catégories / recherche / tri | Les chips, la recherche et le tri sont séparés visuellement. On ne lit pas une vraie barre de pilotage de catalogue. |
| Grille produits | Cards lisibles, mais l'ensemble manque de densité organisée. Les CTA rouges répétés créent une masse visuelle forte. |
| Preuves CK | Les preuves existent dans le header, mais ne réapparaissent pas dans le contexte d'achat du shop. |
| Maturité boutique | La page est propre, mais encore trop « Odoo listing customisé » plutôt que boutique CK éditorialisée. |

Objectif : faire passer `/shop` de « catalogue propre » à « rayon boutique CK mature », sans casser les mécaniques natives Odoo.

---

## 2. Direction P1 recommandée

### 2.1 Intro shop plus compacte et marchande

Réduire la hauteur perçue de l'intro et lui donner un rôle d'orientation.

Attendu :

- H1 conservé mais moins monumental.
- Texte resserré.
- Ajout possible d'une courte ligne de preuves en pills :
  - Origines identifiées
  - Expédié depuis Nantes
  - Sélection créole
- Ne pas créer un hero marketing lourd.

But : libérer plus vite la grille produits tout en gardant le signal CK.

### 2.2 Sidebar filtres plus structurée

Transformer la colonne gauche en vraie surface d'outil.

Attendu :

- Titre global clair : `Filtres`.
- Sections mieux nommées :
  - `Origines & labels` plutôt que seulement `Étiquettes`, si techniquement faisable sans changer les facettes.
  - `Prix`.
- Fond/padding/radius cohérents avec P4.
- Espacements plus réguliers.
- Option desktop : sidebar sticky sous header si non risqué.

Contraintes :

- Ne pas réécrire les facettes Odoo.
- Ne pas masquer des filtres actifs.
- Ne pas casser mobile.

### 2.3 Barre catalogue unifiée

Regrouper visuellement les catégories, la recherche interne et le tri.

Attendu :

- Une zone de pilotage claire au-dessus de la grille.
- Chips catégories avec état actif plus lisible.
- Recherche shop et tri mieux alignés.
- Ajout d'un compteur si disponible sans surcharge : `14 produits` ou équivalent.

But : donner une lecture de tableau de bord boutique plutôt que des éléments posés les uns sous les autres.

### 2.4 Cards shop : réduire l'effet « mur de CTA »

Les cards sont bonnes, mais les boutons rouges répétés dominent fortement.

Pistes à tester :

- Conserver `Ajouter au panier` comme action principale.
- Réduire légèrement la hauteur/padding du bouton sur `/shop`.
- Travailler l'état hover/focus plutôt qu'un gros aplat trop présent sur chaque card.
- Ne pas supprimer le CTA en desktop sans arbitrage MOA.

But : garder l'efficacité e-commerce sans faire de la grille une succession de barres rouges.

### 2.5 Responsive

À vérifier explicitement :

- Desktop 1280.
- Tablette 800.
- Mobile 390.

Mobile attendu :

- Intro compacte.
- Filtres accessibles via l'UI Odoo existante ou bouton natif.
- Pas de débordement horizontal.
- Cards lisibles, CTA accessible.

---

## 3. Non-objectifs

Ne pas faire dans ce lot :

- refonte du moteur de filtres ;
- AJAX custom ;
- nouvelle logique de tri ;
- refonte complète des cards produit ;
- changement du nombre de colonnes sans mesure ;
- nouveau contenu marketing lourd ;
- modification du header P4.

---

## 4. Livrables attendus

1. Audit rapide code avant modification :
   - templates hérités `website_sale.products` ;
   - SCSS `website_sale.scss` / `product_card.scss` ;
   - impact éventuel sur `/shop/category/...`.

2. P1 implémenté en prototype conservé ou en piste avant arbitrage selon risque.

3. Captures :
   - `/shop` desktop 1280 haut de page ;
   - `/shop` desktop scroll grille ;
   - tablette 800 ;
   - mobile 390 ;
   - une catégorie `/shop/category/...` si disponible.

4. Vérifications machine :
   - pas d'overflow horizontal ;
   - nombre de cards inchangé ;
   - `/shop` et `/shop/category/...` répondent 200 ;
   - les filtres restent utilisables ;
   - le panier rapide reste fonctionnel si déjà présent.

5. Note de recette :
   - avant/après ;
   - décisions prises ;
   - limites ou points à arbitrer.

---

## 5. Critères de GO MOA

| Critère | Attendu |
| --- | --- |
| Maturité boutique | La page lit davantage « boutique CK » que « listing Odoo ». |
| Lisibilité catalogue | Catégories, recherche, tri et filtres sont plus faciles à scanner. |
| Efficacité achat | Les cards restent claires et actionnables. |
| Sobriété | Pas de hero lourd, pas de décor gratuit. |
| Cohérence P4 | La page s'accorde au header P4 sans le concurrencer. |
| Mobile | Aucun recul d'usage. |

---

## 6. Verdict MOA initial

Priorité recommandée :

1. Intro shop compacte + preuves CK.
2. Barre catalogue unifiée.
3. Sidebar filtres plus mature.
4. Ajustement léger CTA cards shop.

Le lot doit rester un polish structurant, pas une refonte catalogue.
