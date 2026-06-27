# Ticket Dev — Fiche produit CK · Modèle de données & architecture d’information V1.1

| Champ             | Valeur                                                        |
| ----------------- | ------------------------------------------------------------- |
| **Projet**        | `dorevia_ck_marketone` · C-Kréyol / CK                        |
| **Module cible**  | `dorevia_ck_theme` / module CK produit à confirmer par le Dev |
| **Type**          | Modèle de données + BO produit + template fiche produit       |
| **Priorité**      | Haute — socle catalogue B2C                                   |
| **Statut MOA**    | GO transmission Dev                                           |
| **Référence MOA** | `CK-SPECS-DATA-V1.1.md` + wireframe fiche produit CK          |

## 1. Objectif

Mettre en place le socle de données et l’architecture d’affichage de la fiche produit CK B2C.

L’objectif immédiat est de mieux vendre les produits disponibles en B2C, avec une fiche produit plus claire, plus rassurante et mieux structurée, sans ouvrir à ce stade le chantier B2B.

Le B2B doit rester discret en V1. Il sera traité dans un chantier dédié ultérieur.

## 2. Documents de référence

Le développement doit s’appuyer sur les documents MOA suivants :

* `CK-SPECS-DATA-V1.1.md` — spécification modèle de données validée ;
* `ck_fiche_produit_wireframe.html` — wireframe de référence pour l’organisation des blocs ;
* architecture cible validée : zone haute B2C, puis sections `Découvrir · Composition · Conservation · Infos pratiques · Producteur`, puis produits associés.

Attention : le wireframe valide l’organisation des blocs, mais ne valide pas les textes produits, données alimentaires, allergènes, DDM, labels ou promesses commerciales affichés à titre d’exemple.

## 3. Phase 0 obligatoire — Audit d’existant avant développement

Avant toute implémentation, merci de produire une courte note d’impact technique confirmant :

1. les champs CK déjà existants sur `product.template` ;
2. la source actuelle de la catégorie visible en front ;
3. la source actuelle de l’origine produit, notamment l’attribut produit `Origines` ;
4. la logique existante de prix affiché côté `website_sale` ;
5. la logique existante de prix de référence kg/l utilisée dans les cards produit CK ;
6. la logique de disponibilité stock utilisée côté website ;
7. l’emplacement BO recommandé pour les nouveaux champs ;
8. le ou les modules à modifier.

Aucun champ ne doit être créé si un champ standard Odoo ou un champ CK existant couvre déjà correctement le besoin.

## 4. Modèle de données produit à créer ou confirmer

Sur `product.template`, créer ou confirmer les champs suivants selon audit :

| Champ                    | Type                          | Usage                                        |
| ------------------------ | ----------------------------- | -------------------------------------------- |
| `ck_short_description`   | `Char(255)`                   | Accroche courte en zone haute                |
| `ck_producer_id`         | `Many2one(res.partner)`       | Producteur lié au produit                    |
| `ck_badge_ids`           | `Many2many(ck.product.badge)` | Badges qualifiés affichés en zone haute      |
| `ck_discover_html`       | `Html`                        | Section “Découvrir”                          |
| `ck_ingredients`         | `Text`                        | Ingrédients                                  |
| `ck_allergens`           | `Text`                        | Allergènes déclarés                          |
| `ck_nutrition_html`      | `Html`                        | Tableau ou contenu nutritionnel optionnel    |
| `ck_conservation_before` | `Text`                        | Conservation avant ouverture                 |
| `ck_conservation_after`  | `Text`                        | Conservation après ouverture                 |
| `ck_packaging_label`     | `Char`                        | Libellé conditionnement client               |
| `ck_net_weight_label`    | `Char`                        | Poids net commercial affichable, ex. `100 g` |

Important : `ck_net_weight_label` sert au poids net commercial client. Il ne doit pas être confondu avec `weight`, qui peut être un poids logistique.

## 5. Champs à ne pas créer en V1

Ne pas créer les champs suivants en V1 :

* `ck_origin_id` ;
* `ck_logistics_note` ;
* `ck_price_per_kg` ;
* `ck_variant_price` ;
* `ck_content_validated` ;
* tout champ préfixé `x_`.

L’origine reste portée par l’attribut produit `Origines`, conformément à la doctrine CK existante.

## 6. Producteur — Extension de `res.partner`

Le producteur doit rester un `res.partner` enrichi. Ne pas créer de modèle producteur séparé.

Créer ou confirmer les champs suivants :

| Champ                           | Type      | Usage                                       |
| ------------------------------- | --------- | ------------------------------------------- |
| `ck_is_producer`                | `Boolean` | Identifie les partenaires producteurs       |
| `ck_producer_short_description` | `Text`    | Texte court affiché dans le bloc producteur |
| `ck_producer_story_html`        | `Html`    | Contenu long pour future fiche producteur   |
| `ck_producer_location_label`    | `Char`    | Libellé géographique libre affichable       |
| `image_1920`                    | standard  | Image, logo ou photo producteur             |

Le champ `ck_producer_id` sur produit doit être filtré sur les partenaires dont `ck_is_producer = True`.

`ck_producer_location_label` est un libellé marketing libre, par exemple `Abymes, Guadeloupe`. Il ne doit pas être dérivé automatiquement de l’adresse Odoo.

## 7. Modèle `ck.product.badge`

Créer un modèle dédié `ck.product.badge`.

Champs attendus :

| Champ                 | Type        | Usage                                                                |
| --------------------- | ----------- | -------------------------------------------------------------------- |
| `name`                | `Char`      | Libellé affiché                                                      |
| `code`                | `Char`      | Code technique unique                                                |
| `badge_type`          | `Selection` | `origin`, `ingredient`, `producer`, `platform`, `dietary`, `quality` |
| `icon`                | `Char`      | Emoji ou classe CSS                                                  |
| `sequence`            | `Integer`   | Ordre d’affichage                                                    |
| `requires_validation` | `Boolean`   | Badge nécessitant une preuve                                         |
| `is_sensitive_claim`  | `Boolean`   | Allégation sensible ou réglementée                                   |
| `active`              | `Boolean`   | Archivage                                                            |

En V1, les badges sont sélectionnés manuellement par la MOA sur chaque produit.

Ne pas créer de règle automatique d’attribution des badges en V1.

Badges autorisés en V1, à titre d’exemple :

* `Guadeloupe` ;
* `Farine de manioc` ;
* `Producteur identifié`.

Badges interdits en V1 sauf preuve formelle :

* `Sans gluten` ;
* `Bio` ;
* `Naturel` ;
* `Artisanal` ;
* `Sans additif`.

## 8. Organisation BO produit

Ajouter les champs CK dans l’onglet produit approprié, idéalement dans la continuité de l’organisation CK déjà validée dans l’onglet “Ventes”.

Proposition de regroupement :

### Bloc “Accroche & mise en avant”

* `ck_short_description`
* `ck_badge_ids`

### Bloc “Origine & producteur”

* attribut `Origines`, si déjà visible ailleurs ;
* `ck_producer_id`

### Bloc “Contenu fiche produit”

* `ck_discover_html`
* `ck_ingredients`
* `ck_allergens`
* `ck_nutrition_html`
* `ck_conservation_before`
* `ck_conservation_after`

### Bloc “Infos pratiques”

* `ck_packaging_label`
* `ck_net_weight_label`
* champs standards utiles en lecture ou déjà présents : référence, poids, catégorie, etc.

Le Dev doit vérifier les attributs `name` des groupes existants avant héritage XML afin de ne pas casser les vues déjà livrées.

## 9. Architecture front cible

La fiche produit CK doit suivre l’organisation suivante.

### Zone haute

Colonne gauche :

* image produit / galerie standard ;
* badge éventuel de mise en avant, si déjà géré.

Colonne droite :

1. catégorie visible front ;
2. nom produit ;
3. ligne métadonnées : origine · producteur · poids net commercial · prix de référence ;
4. accroche courte ;
5. badges qualifiés ;
6. prix affiché contextualisé ;
7. variantes ;
8. quantité + favori ;
9. bouton principal `Ajouter au panier` ;
10. réassurance.

### Sections sous ligne de flottaison

Ordre fixe :

1. `Découvrir`
2. `Composition`
3. `Conservation`
4. `Infos pratiques`
5. `Producteur`

Une ancre ne doit jamais apparaître si sa section est vide.

### Bas de fiche

Conserver ou adapter les produits associés selon la logique CK existante.

## 10. Règles d’affichage conditionnel

Afficher `Découvrir` si :

* `ck_discover_html` est renseigné et non vide.

Afficher `Composition` si au moins un des champs suivants est renseigné :

* `ck_ingredients` ;
* `ck_allergens` ;
* `ck_nutrition_html`.

Afficher `Conservation` si au moins un des champs suivants est renseigné :

* `ck_conservation_before` ;
* `ck_conservation_after`.

Afficher `Infos pratiques` si au moins une donnée utile est disponible :

* `ck_net_weight_label` ;
* `ck_packaging_label` ;
* `default_code` ;
* catégorie visible ;
* origine ;
* producteur.

Afficher `Producteur` si :

* `ck_producer_id` est renseigné ;
* le partenaire lié a `ck_is_producer = True`.

## 11. Prix, variantes et prix de référence

Le prix principal affiché en front doit être le prix contextualisé `website_sale` selon :

* variante sélectionnée ;
* taxes ;
* liste de prix ;
* contexte website.

Ne pas afficher `list_price` brut si Odoo calcule un prix contextualisé.

Le sélecteur de variantes doit afficher des prix absolus, jamais un delta de prix comme information centrale.

Exemple attendu :

```text
Saveur :
[ Manio Crackers Salé   3,60 € ]
[ Manio Crackers Sucré  3,50 € ]
```

Le prix de référence kg/l doit être calculé à partir de la logique CK existante de quantité commerciale / poids net commercial, pas depuis `weight` si `weight` correspond au poids logistique.

## 12. Stock et réassurance

Ne pas exposer `qty_available` ou `virtual_available` brut en front.

La fiche doit s’appuyer sur la logique standard `website_sale` de disponibilité produit.

Réassurance V1 à afficher :

```text
✓ En stock — expédié depuis Nantes
✓ Livraison suivie 2 à 3 jours ouvrables
✓ Retour selon conditions de vente
```

Ne pas afficher `Satisfaction garantie — remboursement sous 30 jours` tant que les CGV définitives ne sont pas validées.

## 13. Catégorie visible front

Ne pas supposer que `categ_id` est la catégorie visible en front.

Le Dev doit auditer la source utilisée par CK/Odoo pour la catégorie boutique :

* `public_categ_ids` ;
* catégorie e-commerce ;
* champ CK existant ;
* ou autre logique déjà en place.

La catégorie affichée dans la fiche produit doit être cohérente avec la boutique, les cards produit et les filtres.

## 14. Contraintes de conformité et de gouvernance

Le développement ne doit pas introduire de contenu factuel non vérifié.

Ne pas afficher ou générer automatiquement :

* données alimentaires ;
* allergènes ;
* DDM/DLC ;
* valeurs nutritionnelles ;
* labels ;
* allégations santé ;
* promesses commerciales non validées.

Tout contenu produit doit provenir d’un champ renseigné par la MOA ou d’une source standard fiable.

## 15. Ce que le Dev ne doit pas faire

* Ne pas créer de champ `x_...`.
* Ne pas réutiliser `website_description` pour `ck_discover_html`.
* Ne pas générer automatiquement de badges sans validation MOA.
* Ne pas afficher de badge sensible sans preuve.
* Ne pas coder de règle `applies_to` sur les badges en V1.
* Ne pas créer de modèle producteur dédié.
* Ne pas afficher `remboursement 30 jours` tant que les CGV ne sont pas validées.
* Ne pas coder `ck_logistics_note` en V1.
* Ne pas afficher d’ancre si sa section est vide.
* Ne pas laisser un delta de prix comme information centrale.
* Ne pas utiliser `categ_id` comme catégorie front sans audit.
* Ne pas afficher `list_price` brut en front si un prix website contextualisé existe.
* Ne pas calculer le prix/kg depuis `weight` si `weight` est logistique.
* Ne pas exposer `qty_available` ou `virtual_available` brut au client.

## 16. Livrables attendus

Merci de livrer :

1. note d’impact technique préalable ;
2. modèles Python / champs ;
3. vues BO produit et partenaire ;
4. modèle `ck.product.badge` + vues BO ;
5. adaptation template fiche produit QWeb ;
6. SCSS minimal aligné CK ;
7. règles d’affichage conditionnel ;
8. adaptation du sélecteur de variantes ;
9. tests.

## 17. Tests attendus

Prévoir au minimum les tests suivants :

### Modèle de données

* création produit avec champs CK ;
* création producteur `res.partner` avec `ck_is_producer` ;
* filtrage du champ `ck_producer_id` ;
* création et affectation badges.

### Affichage conditionnel

* aucune ancre vide affichée ;
* ancre `Découvrir` affichée uniquement si contenu ;
* ancre `Composition` affichée uniquement si au moins un champ composition ;
* ancre `Conservation` affichée uniquement si contenu ;
* ancre `Infos pratiques` affichée uniquement si données disponibles ;
* ancre `Producteur` affichée uniquement si producteur valide.

### E-commerce

* prix principal contextualisé ;
* variante avec prix absolu ;
* absence de delta prix central ;
* stock non exposé en quantité brute ;
* réassurance V1 affichée ;
* absence de promesse `remboursement 30 jours`.

### Régression

* fiche produit standard Odoo toujours fonctionnelle ;
* cards produit CK non régressées ;
* shop et filtres non régressés ;
* mobile 390 px sans overflow horizontal.

## 18. Critères d’acceptation MOA

La livraison sera considérée recevable si :

* le modèle de données respecte `CK-SPECS-DATA-V1.1.md` ;
* aucun champ inutile ou redondant n’est créé ;
* les blocs de fiche produit suivent l’architecture validée ;
* aucune donnée non renseignée n’est affichée ;
* aucun badge sensible n’est affiché sans saisie MOA ;
* les prix affichés sont contextualisés ;
* les variantes sont lisibles avec prix absolus ;
* le stock brut n’est pas exposé ;
* la fiche reste cohérente avec l’identité CK ;
* le rendu mobile 390 px est propre.

## 19. Hors périmètre V1

Sont hors périmètre :

* chantier B2B fiche produit ;
* demande de devis pro ;
* tarifs revendeurs visibles en front ;
* avis clients ;
* moteur de recommandations avancées ;
* automatisation des badges ;
* workflow de validation réglementaire ;
* fiche producteur complète ;
* promesse commerciale de remboursement 30 jours ;
* refonte complète du checkout.

## 20. Commentaire MOA

Ce chantier vise à poser un socle propre, durable et gouverné pour la fiche produit CK.

La priorité n’est pas de surcharger la page, mais de structurer l’information produit afin de mieux vendre en B2C : comprendre vite, faire confiance, choisir facilement, acheter sans friction, puis approfondir si besoin.
