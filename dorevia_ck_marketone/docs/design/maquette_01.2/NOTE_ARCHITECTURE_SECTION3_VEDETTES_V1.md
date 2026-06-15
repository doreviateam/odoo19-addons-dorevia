# Note d'architecture MOA / QA — Section 3 · Produits vedettes / Nos coups de cœur

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Section** | Home V1 — Section 3 |
| **Instance recette** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **Statut** | **Acté MOA** |
| **Code** | `home_featured.py` · `catalog_manioc_variants.py` · `website.scss` |

---

## 1. Principe retenu

La Section 3 de la home CK — **Nos coups de cœur** — ne repose pas sur le rendu standard Odoo `website_sale` tel quel.

Le catalogue, les produits, les variantes, les prix, les images et les URLs restent issus du **modèle standard Odoo**.

En revanche, le rendu de la section home est une **couche SSR custom CK** destinée à se rapprocher de la maquette.

## 2. Ce qui reste standard Odoo

Le paramétrage BO reste standard :

- `product.template` pour la fiche produit parent ;
- `product.attribute` pour les attributs ;
- `product.product` pour les variantes vendables ;
- prix calculé via les mécanismes Odoo ;
- URL variante via les URLs Odoo standard ;
- image variante si renseignée, sinon fallback template ;
- rendu `/shop` natif inchangé.

Exemple validé :

- template : **Manio Crackers** ;
- attribut : **Format** ;
- variantes :
  - **Manio Crackers salé** ;
  - **Manio Crackers sucré**.

## 3. Ce qui est spécifique CK sur la home

La home utilise une logique custom CK pour générer les cartes de la section **Nos coups de cœur**.

Objectif :

- obtenir un rendu proche de la maquette ;
- afficher des cartes visuelles éditorialisées ;
- permettre l'affichage d'une carte par variante lorsque le produit parent porte plusieurs variantes pertinentes ;
- conserver les URLs, prix et images issus d'Odoo.

Ainsi, **Manio Crackers** peut produire deux cartes visibles sur la home :

- **Manio Crackers salé** ;
- **Manio Crackers sucré**.

Ce comportement n'est pas un automatisme du snippet natif Odoo. Il est porté par la couche SSR CK.

## 4. Choix de libellé carte

Pour les variantes, la carte home peut utiliser le **libellé d'attribut** comme nom visible, afin d'éviter un affichage trop technique du type :

`Manio Crackers (Manio Crackers salé)`

Le rendu cible est plus lisible côté client :

- `Manio Crackers salé`
- `Manio Crackers sucré`

## 5. Règle métier MOA

La MOA retient la règle suivante :

- un produit simple publié donne une carte ;
- un produit multi-variantes peut donner une carte par variante si les variantes sont commercialement significatives ;
- les données affichées doivent rester cohérentes avec le BO Odoo ;
- aucun produit absent du catalogue BO publié ne doit apparaître dans les vedettes home.

## 6. Cas Galettes de manioc

**Galettes de manioc** ne doit pas être traité comme une variante de **Manio Crackers**.

Si **Galettes de manioc** est maintenu dans le catalogue V1, il doit exister comme `product.template` séparé, publié, avec image, prix et données e-commerce cohérentes.

Sinon, il doit être retiré de la section home.

## 7. Critères de recette Section 3

La recette Section 3 devra vérifier :

- affichage des produits réellement publiés en BO ;
- absence de produit orphelin ou supprimé ;
- affichage correct des variantes **Manio Crackers salé** et **Manio Crackers sucré** ;
- liens **Voir** pointant vers les bonnes variantes Odoo ;
- images visibles avec hauteur stable ;
- prix cohérents avec Odoo ;
- rendu proche de la maquette **Nos coups de cœur** ;
- `/shop` natif non modifié.

## 8. Décision MOA

La MOA valide le principe suivant :

**BO Odoo standard pour les données produit ; rendu SSR custom CK pour la section home Nos coups de cœur.**

Ce choix est assumé pour rapprocher la home de la maquette tout en conservant Odoo comme source de vérité catalogue.

---

## Références Dev

| Fichier | Rôle |
|---------|------|
| `dorevia_ck_marketone_content/home_featured.py` | SSR cartes · sélection variantes · bootstrap homepage |
| `dorevia_ck_marketone_content/catalog_manioc_variants.py` | Alignement catalogue MOA (Manio + Galettes séparées) |
| `dorevia_ck_theme/static/src/scss/website.scss` | Styles `.ck-featured-products--maquette` |
| `dorevia_ck_theme/views/snippets/ck_snippet_featured_products.xml` | Squelette snippet éditeur |

Migrations : `19.0.1.15.0` (cartes maquette) · `19.0.1.16.0` · `19.0.1.17.0` (catalogue MOA + régénération vedettes).
