# MODELE_PAGE_HOME — Home CK (modèle de référence)

## 1. Intention du modèle

La Home CK est la page d’entrée principale.

Elle doit :

- installer l’univers de marque ;
- orienter rapidement vers les portes commerce ;
- montrer une preuve produit ;
- rassurer sur la proposition de valeur ;
- capter l’intérêt sans surcharge ;
- garder une ouverture vers l’éditorial et le communautaire, sans les placer en priorité mobile.

---

## 2. Composition actuelle de référence

Composition visible actuelle, dans l’ordre :

1. Header / navigation ;
2. Hero ;
3. Explorer / portes ;
4. Sélection produits ;
5. Newsletter ;
6. En pratique ;
7. Footer.

Blocs présents mais masqués/différés dans l’assemblage actuel (sous flag) :

- Fournisseur ;
- Éditorial.

Référence de principe : ces blocs existent dans la structure Home mais ne constituent pas le flux par défaut tant que le flag de queue Home n’est pas activé.

---

## 3. Pattern-blocs associés

- `PATTERN_BLOC_HEADER_NAV_3_NIVEAUX.md`
- `PATTERN_BLOC_HOME_HERO.md`
- `PATTERN_BLOC_HOME_EXPLORER_PORTES.md`
- `PATTERN_BLOC_HOME_SELECTION_PRODUITS.md`
- `PATTERN_BLOC_HOME_NEWSLETTER.md`
- `PATTERN_BLOC_HOME_EN_PRATIQUE.md`
- `PATTERN_BLOC_FOOTER_RESPONSIVE.md`

---

## 4. Logique responsive desktop

Doctrine desktop pour la Home :

- Home d’univers riche et équilibrée ;
- commerce, éditorial, promotionnel et communautaire peuvent coexister ;
- rythme plus narratif accepté ;
- respiration visuelle assumée ;
- accès au catalogue visible sans écraser l’identité de marque.

---

## 5. Logique responsive mobile — commerce-first

Doctrine mobile :

- ne pas rediriger automatiquement vers `/shop` ;
- conserver `/` comme Home ;
- remonter plus vite les contenus marchands.

Implications de composition mobile :

- Hero plus compact ;
- CTA boutique très clair ;
- portes commerce visibles tôt :
  - Promotions ;
  - Kits / Packs ;
  - Collections ;
  - Origines ;
  - Catégories ;
  - Incontournables (si activé) ;
- sélection produits courte rapidement visible ;
- réassurance `En pratique` proche du parcours d’achat ;
- newsletter plus basse ;
- éditorial et communautaire différés ou en soutien.

---

## 6. Ordre de priorité mobile recommandé

Lecture cible recommandée (doctrine, sans imposer une refonte immédiate) :

1. Header mobile : recherche / panier / favoris accessibles ;
2. Hero compact avec CTA boutique ;
3. Portes commerce ;
4. Sélection produits ;
5. Réassurance ;
6. Newsletter ;
7. Éditorial / communautaire plus bas ou différés.

---

## 7. GO / NO GO

### GO

- la Home installe CK sans ralentir l’accès au commerce ;
- en mobile, l’utilisateur comprend vite comment acheter ;
- les portes commerce sont accessibles tôt ;
- la sélection produits et la réassurance soutiennent l’achat ;
- l’éditorial reste présent mais ne bloque pas le parcours mobile.

### NO GO

- Home mobile trop narrative avant l’accès produit ;
- `/shop` caché ou trop tardif ;
- portes commerce trop basses ;
- surcharge communautaire au premier écran mobile ;
- redirection automatique mobile vers `/shop` sans décision spécifique.

---

## 8. Hors périmètre

- pas de refonte immédiate ;
- pas de nouvelle page ;
- pas de snippets Odoo ;
- pas de modification QWeb / SCSS dans cette passe ;
- pas de nouvel ordre de blocs imposé sans ticket d’implémentation.

---

## 9. Décision

`MODELE_PAGE_HOME` est retenu comme premier modèle de page CK détaillé.  
Il sert de référence pour articuler Home d’univers desktop et Home commerce-first mobile.  
Toute évolution réelle de l’ordre des blocs ou du rendu responsive devra faire l’objet d’un ticket séparé.

---

## 10. Références

- `docs/design_system/modeles-pages/INVENTAIRE_MODELES_PAGES_CK.md`
- `docs/design_system/pattern-blocs/INVENTAIRE_HOME_PATTERN_BLOCS.md`
- `docs/design_system/pattern-blocs/PATTERN_BLOC_HEADER_NAV_3_NIVEAUX.md`
- `docs/design_system/pattern-blocs/PATTERN_BLOC_HOME_HERO.md`
- `docs/design_system/pattern-blocs/PATTERN_BLOC_HOME_EXPLORER_PORTES.md`
- `docs/design_system/pattern-blocs/PATTERN_BLOC_HOME_SELECTION_PRODUITS.md`
- `docs/design_system/pattern-blocs/PATTERN_BLOC_HOME_NEWSLETTER.md`
- `docs/design_system/pattern-blocs/PATTERN_BLOC_HOME_EN_PRATIQUE.md`
- `docs/design_system/pattern-blocs/PATTERN_BLOC_FOOTER_RESPONSIVE.md`
- `views/pages/ckr_homepage.xml` (template Home de référence)

