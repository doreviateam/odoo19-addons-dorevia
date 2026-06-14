# Annotation composants → Odoo — Maquette CK V1

| Artefact | `/Users/doreviateam/open-design/.od/projects/ck-marketone-maquette-v1/index.html` |
|----------|-------------------------------------------------------------------------------------|
| **Référence** | `design_01.md` §17 |

> Données maquette = **démonstration**. Comportement cible = Odoo `website_sale`.

---

| Composant | Lecture design (maquette V1) | Traduction Odoo probable | Couche | Statut phase 1 |
|-----------|------------------------------|--------------------------|--------|----------------|
| Header | Nav, logo CK, recherche, panier | `website.layout` | Thème / template | Autorisé |
| Recherche header | Champ recherche produit | Route recherche `website_sale` | Template natif + thème | Autorisé |
| Hero accueil | Promesse + CTA boutique + signal pro | Snippet / bloc `website` | Thème / snippet | Autorisé |
| Bandeau catégories accueil | Familles produits (épicerie, condiments…) | Liens catégories e-commerce | Template + thème | Autorisé |
| Produits vedettes accueil | 3–4 cartes produit | Snippet dynamique ou manuel | Snippet + thème | Autorisé |
| Bandeau réassurance | Livraison, paiement, sourcing | Snippet statique | Thème / snippet | Autorisé |
| Titre `/shop` | « Boutique » + promesse courte | Héritage page shop | Template + thème | Autorisé |
| Sidebar filtres | Catégories, origines, collections, prix | Filtres URL / domaine | Template (+ extension TBD) | Visible — source à trancher |
| Filtre catégories | Checkboxes → liens | `product.public.category` | Template natif | Autorisé |
| Filtre origines | Checkboxes Réunion, Guadeloupe… | Attribut produit ou extension | À trancher | Visible — source à décider |
| Filtre collections | Sélection marché, petits producteurs | Tags / catégories / modèle custom | À trancher | Visible — mécanique à décider |
| Filtre prix | Fourchette min–max | Prudence CE — extension possible | À trancher | Visible — traduction non figée |
| Toolbar tri | Pertinence, prix, nouveautés | Paramètre `order` `website_sale` | Template natif + thème | Autorisé |
| Grille produits | Cartes 3–4 colonnes | `website_sale` products | Template + thème | Autorisé |
| Carte produit | Image, nom, prix, origine, CTA | Tuile `website_sale` | Thème + template | Autorisé |
| Action carte « Voir » | Accès fiche depuis grille | Lien tuile `website_sale` standard | Template natif + thème | **Retenu V1.1** |
| Quick-add (hypothèse future) | Ajout panier depuis carte | Héritage template si validé MOA | Template métier léger | **Non retenu** phase 1 |
| Badge pack | Coffret / pack | Produit pack 1 ligne (`non_detailed` TBD) | Template + décision MOA | Visible — doctrine à confirmer David |
| Pagination | Pages 1 2 3 | Pager `/shop/page/N` | Template natif + thème | Autorisé |
| État vide | Message + CTA effacer filtres | QWeb conditionnel | Template | Autorisé (non montré en V1) |
| Fiche produit — galerie | Image principale + miniatures | Galerie `website_sale.product` | Template natif + thème | Autorisé |
| Fiche — buy box | Prix, qty, CTA Ajouter | Widget natif fiche produit | Template natif + thème | Autorisé |
| Fiche — origine / usage | Bloc éditorial court | Champ produit / snippet | Template + thème | Autorisé |
| Produits liés | 3 suggestions | `alternative_product_ids` | Template natif + thème | Autorisé |
| Entrée pro | Lien « Professionnels » + bloc revendeur | Page CMS + formulaire `website_crm` | Snippet + page | Signal uniquement |
| Icône panier header | Badge démo « 2 » | `sale_get_order()` Odoo | Template natif | **Démo UX — pas spec** |
| Panier / checkout | Non maquettés | `website_sale` standard | Hors maquette V1 | Non maquetté |

---

## Règles rappelées

```text
JS filtre local dans l’artefact = démonstration visuelle uniquement.
Cible Odoo = navigation URL / rechargement / domaine website_sale.
Action « Voir » ≠ quick-add. Quick-add non exigé phase 1.
Entrée pro ≠ portail revendeur.
Packs = 1 carte / 1 prix en maquette (pas explosion checkout).
```
