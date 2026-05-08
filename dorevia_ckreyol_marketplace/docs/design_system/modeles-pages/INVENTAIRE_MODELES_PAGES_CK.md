# CK — Inventaire initial des modèles de page

## 1. Objectif

Inventorier les types de pages nécessaires à CK et leur logique de composition, sans créer de pages ni modifier le code.

Cadre :

- inventaire **documentaire** uniquement ;
- alignement avec la doctrine responsive CK ;
- préparation d’un backlog de cadrage, pas d’implémentation.

---

## 2. Échelle de statut / priorité

Statut :

- **Existant** : page et logique présentes dans le produit.
- **À cadrer** : intention claire, composition à formaliser.
- **À créer** : modèle nécessaire mais non décrit/livré.
- **Différé** : hors timing MVP actuel.

Priorité :

- **P1** : critique parcours marchand.
- **P2** : important court terme.
- **P3** : utile moyen terme.
- **P4** : faible / différé.

---

## 3. Inventaire des modèles

## MODELE_PAGE_HOME

- **Objectif** : page d’univers qui ouvre le parcours CK (marque + portes commerce + réassurance).
- **Statut** : Existant.
- **Priorité** : P1.
- **Nature** : mixte (marchande + éditoriale + promotionnelle + communautaire).
- **Pattern-blocs mobilisables** : header 3 niveaux, hero, explorer portes, sélection produits, newsletter, en pratique, footer.
- **Routes / liens Odoo associés** : `/` ; liens vers `/shop`, `/promotions`, `/collections`, `/origines`, `/shop?ckr_mode=pack` selon portes actives.
- **Logique responsive desktop** : Home riche et équilibrée.
- **Logique responsive mobile** : Home orientée achat ; portes commerce, sélection produits et réassurance remontées ; éditorial en soutien.
- **Hors périmètre** : refonte globale du header ; refonte SEO ; création de nouveaux snippets.
- **Remarques / risques** : risque de surcharge mobile si hiérarchie des blocs non explicitée.

## MODELE_PAGE_SHOP_CONTAINER

- **Objectif** : container catalogue et facettes, point d’entrée transactionnel principal.
- **Statut** : Existant.
- **Priorité** : P1.
- **Nature** : marchande.
- **Pattern-blocs mobilisables** : header, hero shop, chips/raccourcis commerce, grille produits, sidebar/filtres, pagination, footer.
- **Routes / liens Odoo associés** : `/shop`, `/promotions`, `/kits`, `/origines`, `/incontournables`, paramètres `ckr_mode`.
- **Logique responsive desktop** : densité de comparaison produit + filtres visibles.
- **Logique responsive mobile** : action rapide (recherche, filtres utiles, ajout panier), lecture compacte des cartes.
- **Hors périmètre** : refonte moteur de recherche ; refonte des règles de pricing.
- **Remarques / risques** : dérive vers trop de portes simultanées, perte de lisibilité mobile.

## MODELE_PAGE_PRODUIT

- **Objectif** : convaincre et convertir sur une fiche produit.
- **Statut** : Existant (base Odoo + adaptation CK à cadrer finement).
- **Priorité** : P1.
- **Nature** : marchande.
- **Pattern-blocs mobilisables** : galerie, prix/variantes, CTA panier, réassurance, produits liés, avis (si activés), footer.
- **Routes / liens Odoo associés** : `/shop/product/<slug>`.
- **Logique responsive desktop** : informations riches (visuel, attributs, contexte, cross-sell).
- **Logique responsive mobile** : conversion-first (prix, disponibilité, CTA, réassurance visibles tôt), contenu long plus bas.
- **Hors périmètre** : refonte complète PDP ; nouveau moteur d’avis.
- **Remarques / risques** : perte de conversion si l’éditorial remonte avant le CTA.

## MODELE_PAGE_PANIER

- **Objectif** : permettre révision rapide du panier puis passage checkout.
- **Statut** : Existant.
- **Priorité** : P1.
- **Nature** : transactionnelle.
- **Pattern-blocs mobilisables** : tableau/lignes panier, quantité, suppression, total, CTA checkout, lien continuer achats.
- **Routes / liens Odoo associés** : `/shop/cart`.
- **Logique responsive desktop** : vue complète des lignes et résumé.
- **Logique responsive mobile** : actions clés tactiles d’abord (quantité, suppression, total, CTA).
- **Hors périmètre** : mini-panier avancé ; marketing panier complexe.
- **Remarques / risques** : friction mobile si CTA checkout trop bas ou ambigu.

## MODELE_PAGE_FAVORIS

- **Objectif** : relier intention et conversion via wishlist.
- **Statut** : Existant — incrément minimal wishlist standard habillé CK.
- **Priorité** : P2.
- **Nature** : marchande (soutien conversion).
- **Pattern-blocs mobilisables** : grille wishlist, actions produit, CTA retour boutique.
- **Routes / liens Odoo associés** : `/shop/wishlist`.
- **Logique responsive desktop** : consultation/confort de comparaison.
- **Logique responsive mobile** : accès rapide aux actions achat depuis favoris.
- **Hors périmètre** : refonte fonctionnelle wishlist native.
- **Remarques / risques** : confusion panier vs favoris si wording/action non cohérents.

## MODELE_PAGE_OFFRIR

- **Objectif** : parcours “idées cadeaux” orienté conversion thématique.
- **Statut** : À cadrer.
- **Priorité** : P2.
- **Nature** : mixte (promotionnelle + marchande).
- **Pattern-blocs mobilisables** : hero thématique, entrées cadeaux, sélections produits, réassurance livraison, CTA.
- **Routes / liens Odoo associés** : `/offrir` (si publiée), relais depuis navigation.
- **Logique responsive desktop** : storytelling cadeau + portes achat.
- **Logique responsive mobile** : accès rapide à sélections achetables ; éditorial condensé.
- **Hors périmètre** : création immédiate de nouveaux contenus marketing.
- **Remarques / risques** : page trop éditoriale sans débouché achat.

## MODELE_PAGE_PROFESSIONNELS

- **Objectif** : qualifier la demande B2B et orienter vers le formulaire.
- **Statut** : Existant (parcours demande compte pro).
- **Priorité** : P2.
- **Nature** : transactionnelle (lead gen pro).
- **Pattern-blocs mobilisables** : proposition de valeur B2B, preuves/réassurance, formulaire, contact.
- **Routes / liens Odoo associés** : `/demande-compte-professionnel`.
- **Logique responsive desktop** : argumentaire + formulaire lisible.
- **Logique responsive mobile** : accès direct formulaire et points de réassurance essentiels.
- **Hors périmètre** : refonte CRM ; tunnel B2B complet.
- **Remarques / risques** : taux d’abandon si formulaire trop dense mobile.

## MODELE_PAGE_ORIGINES

- **Objectif** : valoriser terroirs/origines tout en menant à l’achat.
- **Statut** : Existant comme porte commerciale / à cadrer comme modèle éditorial complet.
- **Priorité** : P2.
- **Nature** : mixte (éditoriale + marchande).
- **Pattern-blocs mobilisables** : intro origine, filtres/portes origine, grille produits.
- **Routes / liens Odoo associés** : `/origines` -> `/shop?ckr_mode=origin`.
- **Logique responsive desktop** : contenu culturel + navigation produit.
- **Logique responsive mobile** : filtrage et accès produits prioritaires ; éditorial en soutien.
- **Hors périmètre** : refonte encyclopédique des origines.
- **Remarques / risques** : dilution commerciale si le récit remplace la navigation produit.

## MODELE_PAGE_RECETTES

- **Objectif** : inspirer l’usage produit et renvoyer vers l’achat.
- **Statut** : À cadrer.
- **Priorité** : P3.
- **Nature** : éditoriale en soutien marchand.
- **Pattern-blocs mobilisables** : listing recettes, détail recette, produits associés, CTA shop.
- **Routes / liens Odoo associés** : `/recettes` ; éventuellement `/blog` catégorie recette selon setup.
- **Logique responsive desktop** : lecture éditoriale confortable + recommandations produits.
- **Logique responsive mobile** : accès rapide ingrédients/produits ; contenu long après actions utiles.
- **Hors périmètre** : CMS recette complet.
- **Remarques / risques** : page consommée sans rebond marchand.

## MODELE_PAGE_PRODUCTEUR

- **Objectif** : mettre en valeur un producteur et ses produits.
- **Statut** : À créer.
- **Priorité** : P3.
- **Nature** : mixte (éditoriale + marchande).
- **Pattern-blocs mobilisables** : portrait court, preuves qualité, sélection produits producteur, CTA.
- **Routes / liens Odoo associés** : route dédiée à définir ; possible lien depuis fiches produit/origines.
- **Logique responsive desktop** : narration marque + assortiment.
- **Logique responsive mobile** : produits et CTA d’abord ; portrait condensé.
- **Hors périmètre** : annuaire producteurs exhaustif.
- **Remarques / risques** : coût éditorial élevé si modèle non industrialisé.

## MODELE_PAGE_COLLECTION

- **Objectif** : présenter une collection thématique achetable.
- **Statut** : Existant comme logique shop / à cadrer si landing dédiée.
- **Priorité** : P2.
- **Nature** : marchande avec soutien éditorial léger.
- **Pattern-blocs mobilisables** : hero collection, intro courte, grille produits, filtres/tri, CTA.
- **Routes / liens Odoo associés** : `/collections` ; paramètres collection sur `/shop`.
- **Logique responsive desktop** : richesse visuelle + profondeur catalogue.
- **Logique responsive mobile** : accès rapide aux produits collection ; éditorial secondaire.
- **Hors périmètre** : refonte taxonomie catalogue.
- **Remarques / risques** : confusion entre collection éditoriale et filtre technique.

## MODELE_PAGE_LEGALE

- **Objectif** : conformité légale et confiance.
- **Statut** : Existant / à consolider selon pages (CGV, mentions, confidentialité, etc.).
- **Priorité** : P1 conformité.
- **Nature** : légale.
- **Pattern-blocs mobilisables** : structure texte, sommaire, ancrages, contact, footer légal.
- **Routes / liens Odoo associés** : pages légales publiées (URLs à inventorier précisément).
- **Logique responsive desktop** : lecture structurée longue.
- **Logique responsive mobile** : lisibilité, ancrages et accès contact ; pas d’encombrement non légal.
- **Hors périmètre** : audit juridique de fond.
- **Remarques / risques** : risque conformité si inventaire des pages légales incomplet.

---

## 4. Logique responsive transversale (rappel)

### Desktop

- rôle de page complet ;
- équilibre commerce / éditorial / promotionnel / communautaire ;
- composition riche quand pertinente.

### Mobile

- rôle commerce-first ;
- blocs marchands prioritaires ;
- éditorial en soutien ;
- communautaire différé ;
- accès rapide aux actions clés.

---

## 5. Hors périmètre de cet inventaire

- développement QWeb/SCSS/JS ;
- création de nouvelles pages publiées ;
- refonte header/drawer ;
- création de snippets Odoo ;
- instrumentation analytics nouvelle.

---

## 6. Décision

Cet inventaire est retenu comme première cartographie des modèles de page CK.

Il ne déclenche pas de développement.

Il sert à :

- éviter de créer les futures pages CK de manière isolée ;
- relier chaque page aux pattern-blocs existants ;
- intégrer la doctrine responsive desktop/mobile dès le cadrage ;
- préparer les futurs tickets de cadrage ou d’implémentation.

Toute création ou refonte de page devra faire l’objet d’un ticket séparé.

