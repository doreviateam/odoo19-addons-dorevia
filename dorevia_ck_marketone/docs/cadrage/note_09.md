---

# Note de cadrage Dev/QA — CK-UNIVERSE-BANNER-001

## Banner éditorial des pages Univers

## 1. Contexte

La navigation C-Kréyòl est désormais structurée autour du parcours marchand suivant :

**Home → Univers → Rayon → Produit → Panier**

Dans Odoo, les **Univers** correspondent aux catégories e-commerce de niveau 0 :

* Épicerie
* Boissons
* Soin & Bien-être
* Artisanat

Ces catégories racines sont maintenant des entrées de navigation cliquables depuis le header. Elles mènent vers les pages catégories Odoo correspondantes, du type :

```text
/shop/category/...
```

Le comportement attendu est désormais clair :

* l’utilisateur entre dans un **Univers** ;
* il peut ensuite descendre dans un **Rayon** / sous-catégorie ;
* puis accéder à une **fiche produit** ;
* puis au **panier**.

Aujourd’hui, les pages Univers restent encore proches d’une page catégorie Odoo standard : titre, filtres, grille produits.
Il manque un repère visuel d’entrée d’univers, cohérent avec le positionnement CK : **épicerie premium des Outre-mer, chaleureuse, fiable et orientée logistique maîtrisée**.

## 2. Objectif de la demande

Cette note ne demande pas encore une implémentation immédiate.

Elle demande au Dev/QA de :

1. analyser le code actuel ;
2. identifier ce qui existe déjà autour des pages catégories / univers / bannières ;
3. vérifier comment Odoo 19 CE expose l’image native des catégories e-commerce ;
4. proposer le ticket technique propre pour implémenter un banner Univers modifiable et maintenable.

## 3. Besoin fonctionnel cible

Sur chaque page de **catégorie e-commerce niveau 0**, afficher un banner éditorial appelé provisoirement :

**Banner Univers / Porte d’entrée**

Ce banner doit :

* identifier immédiatement l’univers visité ;
* donner une respiration entre le header et la grille produits ;
* rester léger, pas un hero de Home ;
* utiliser l’image native associée à la catégorie e-commerce Odoo ;
* permettre une accroche éditoriale courte modifiable ;
* rester cohérent desktop/mobile ;
* ne pas impacter les sous-catégories dans une V1.

## 4. Parcours concerné

Le banner concerne uniquement l’étape **Univers** du parcours :

```text
Home
  ↓
Univers = catégorie e-commerce niveau 0
  ↓
Rayon = sous-catégorie e-commerce
  ↓
Produit = fiche produit
  ↓
Panier
```

Exemple :

```text
Home
  ↓
Épicerie
  ↓
Biscuits / Confitures / Farines / Condiments
  ↓
Manio Crackers
  ↓
Panier
```

## 5. Périmètre V1 souhaité

### Inclus

Afficher un banner complet sur les catégories e-commerce racines :

* Épicerie
* Boissons
* Soin & Bien-être
* Artisanat

Le banner doit contenir :

* un eyebrow fixe, par exemple `Univers` ;
* le nom de la catégorie ;
* une accroche courte ;
* une image de fond ;
* un séparateur / accent visuel discret.

### Hors périmètre V1

Ne pas traiter dans cette V1 :

* les sous-catégories avec un banner complet ;
* une refonte de `/shop` ;
* une refonte de la grille produits ;
* un mega-menu ;
* un système de landing pages CMS indépendantes ;
* un snippet totalement libre éditable sans cadre ;
* la création d’une nouvelle arborescence de navigation.

## 6. Principe éditorial retenu

Le banner doit être un **bandeau de rayon premium**, pas un hero de Home.

Direction validée :

* hauteur contenue ;
* structure commune pour les 4 univers ;
* variation par image et accent visuel ;
* image incarnée, liée à l’univers ;
* texte HTML, pas intégré dans l’image ;
* lisibilité mobile prioritaire.

Exemples d’ambiances attendues :

| Univers          | Ambiance attendue                                           |
| ---------------- | ----------------------------------------------------------- |
| Épicerie         | épices, fruits tropicaux, produits du quotidien, bois clair |
| Boissons         | bouteilles, verre, fraîcheur, feuilles, lumière             |
| Soin & Bien-être | plantes, savons, matières naturelles, lin, terre cuite      |
| Artisanat        | vannerie, bois, objets, mains, matières                     |

Les fonds abstraits peuvent servir de maquette structurelle, mais ne doivent pas devenir la direction finale.

## 7. Utilisation du standard Odoo

Point important : le BO Odoo permet déjà d’associer une image à une catégorie e-commerce.

La V1 doit donc étudier l’usage de cette image native plutôt que créer immédiatement un champ image CK supplémentaire.

Principe souhaité :

| Élément banner  | Source envisagée                                            |
| --------------- | ----------------------------------------------------------- |
| Titre           | `name` de la catégorie e-commerce                           |
| Image de fond   | image native de la catégorie e-commerce                     |
| Accroche courte | champ CK dédié à créer si nécessaire                        |
| Accent visuel   | variante cadrée ou mapping contrôlé                         |
| Activation      | à étudier : affichage automatique niveau 0 ou champ booléen |

## 8. Point d’attention : code existant

Le Dev/QA doit impérativement vérifier s’il existe déjà un socle lié aux bannières / univers / rayons dans les modules CK.

À auditer notamment :

* templates hérités de `website_sale.products` ;
* éventuels templates liés à une bannière univers ou rayon ;
* logique existante autour de `ck_universe` ;
* fichiers de type `website_sale_rayon_editorial.xml` ou équivalent ;
* champs déjà ajoutés sur `product.public.category` ;
* migrations déjà passées sur les catégories Épicerie / Boissons / Soin & Bien-être / Artisanat ;
* SCSS existant côté shop/category ;
* éventuels tests existants sur pages `/shop/category/...`.

Objectif : **ne pas dupliquer un mécanisme déjà présent**.
Si un socle existe, proposer une évolution propre plutôt qu’un nouveau composant parallèle.

## 9. Direction visuelle cible

### Desktop

* hauteur indicative : environ 220 px ;
* image de fond en `cover` ;
* texte aligné à gauche dans le container ;
* scrim latéral brun chaud CK, pas d’overlay noir ;
* titre en typographie CK ;
* accroche courte sur deux lignes maximum ;
* ligne d’accent discrète.

### Mobile

* hauteur indicative : environ 180 px ;
* padding réduit ;
* texte lisible ;
* accroche éventuellement limitée à une ligne selon tests ;
* scrim adapté en bas ou latéral selon meilleur rendu ;
* aucune perte de lisibilité en 390 px.

## 10. Typographies

Conserver les typographies CK existantes :

* titres : **Fraunces** ;
* textes : **DM Sans**.

Ne pas introduire de nouvelle police.

## 11. Couleurs / accents

La proposition design évoque des accents par univers :

| Univers          | Accent proposé |
| ---------------- | -------------- |
| Épicerie         | terracotta     |
| Boissons         | vert d’eau     |
| Soin & Bien-être | sable doré     |
| Artisanat        | ocre terre     |

Le Dev/QA doit proposer l’approche la plus propre.

Préférence MOA : éviter un champ hex libre non contrôlé.
Une sélection cadrée ou un mapping contrôlé est préférable.

Exemple possible :

```text
ck_banner_variant = epicerie / boissons / bien_etre / artisanat / default
```

Puis le front applique les couleurs prévues par la charte.

## 12. Champs à étudier

Champs potentiels sur `product.public.category` :

| Champ               | Type envisagé     | Commentaire                      |
| ------------------- | ----------------- | -------------------------------- |
| `ck_subtitle`       | Char / Text court | Accroche courte du banner        |
| `ck_banner_enabled` | Boolean           | Optionnel, à discuter            |
| `ck_banner_variant` | Selection         | Préféré à un champ couleur libre |
| image native Odoo   | champ standard    | À réutiliser si adapté           |

Le Dev/QA doit confirmer les noms exacts, types, vues BO et impacts migration.

## 13. Règles d’affichage à analyser

Comportement cible V1 :

* afficher le banner si une catégorie est active ;
* afficher uniquement si la catégorie est de niveau 0 ;
* ne pas afficher sur `/shop` général ;
* ne pas afficher sur les sous-catégories en V1 ;
* prévoir un fallback propre si l’image catégorie est absente ;
* prévoir un fallback propre si l’accroche est vide.

Condition indicative à vérifier :

```python
category and not category.parent_id
```

À confirmer selon la structure réelle des catégories publiques Odoo et le contexte `website_sale`.

## 14. Fallbacks attendus

Si image absente :

* fond clair chaud CK ;
* texte brun CK ;
* pas de zone cassée ;
* pas d’image placeholder générique visible.

Si accroche absente :

* masquer le bloc accroche ;
* conserver le titre ;
* ne pas laisser d’espace vide disgracieux.

Si variante absente :

* utiliser l’accent CK par défaut.

## 15. Accessibilité

Le ticket proposé devra inclure une vérification accessibilité minimale :

* contraste suffisant texte/fond ;
* texte en HTML, jamais dans l’image ;
* pas de perte de lisibilité mobile ;
* pas d’élément interactif inutile dans le banner ;
* structure de titres cohérente avec la page catégorie.

Point à étudier : si le banner contient le H1, éviter de dupliquer le H1 natif Odoo de façon incohérente.

## 16. Impacts attendus

À analyser côté Dev/QA :

* impact sur `website_sale.products` ;
* impact sur breadcrumb / titre catégorie existant ;
* interaction avec la toolbar boutique ;
* interaction avec les filtres ;
* interaction avec les pages catégories existantes ;
* interaction avec les traductions ;
* impact mobile ;
* impact cache / multi-website si applicable.

## 17. Questions à instruire par Dev/QA

Merci d’analyser et de répondre aux points suivants :

1. Quel template actuel rend les pages `/shop/category/...` ?
2. Existe-t-il déjà un composant CK de bannière rayon / univers ?
3. Existe-t-il déjà des champs CK sur `product.public.category` exploitables ?
4. L’image native de la catégorie e-commerce est-elle accessible facilement en QWeb ?
5. Cette image est-elle déjà utilisée ailleurs ?
6. Faut-il utiliser l’image standard en background ou via une balise `<img>` ?
7. Comment gérer proprement le H1 natif ?
8. Faut-il un champ `ck_banner_enabled`, ou l’affichage automatique niveau 0 suffit-il ?
9. Quelle solution recommander pour l’accent visuel : mapping, selection, couleur libre ?
10. Quels tests automatisés ajouter ou adapter ?
11. Quel est le risque de régression sur `/shop`, sous-catégories et mobile ?
12. Quel découpage ticket recommandez-vous : un seul ticket ou deux lots ?

## 18. Livrable attendu du Dev/QA

Le livrable attendu n’est pas encore le développement.

Nous attendons :

1. une analyse courte de l’existant ;
2. la proposition technique recommandée ;
3. les fichiers pressentis à modifier ;
4. les champs Odoo à créer ou réutiliser ;
5. les risques identifiés ;
6. les tests à prévoir ;
7. une proposition de ticket Dev final prêt à exécuter.

## 19. Critères de validation du futur ticket

Le futur ticket sera considéré bien cadré s’il permet de livrer :

1. un banner visible sur les catégories e-commerce niveau 0 ;
2. un rendu cohérent desktop ;
3. un rendu cohérent mobile 390 px ;
4. l’usage de l’image native catégorie Odoo ;
5. une accroche modifiable côté BO ;
6. un fallback propre sans image ;
7. aucun impact sur `/shop` général ;
8. aucun impact non voulu sur les sous-catégories ;
9. aucun retour à un design trop lourd ou générique ;
10. une couverture QA suffisante.

## 20. Verdict MOA

**GO analyse Dev/QA.**

Objectif : obtenir une proposition technique solide avant lancement du développement du banner Univers.

Le cap fonctionnel est validé :
**les pages Univers doivent devenir des portes d’entrée marchandes identifiables, éditorialisées et cohérentes avec l’identité CK, tout en s’appuyant autant que possible sur le standard Odoo.**
