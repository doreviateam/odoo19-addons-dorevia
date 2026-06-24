# Rapport — Retour Dev Home & Shop CK · 2026-06-24

| Champ | Valeur |
|---|---|
| Projet | `dorevia_ck_marketone` |
| Statut | À arbitrer |
| Date | 2026-06-24 |
| Responsable | Dev |
| Remplace | — |
| Remplacé par | — |

---

## 1. Objet du document

Ce document répond à l'analyse MOA transmise le 2026-06-24 sur la Home page et la page Shop C-Kréyòl.

L'objectif n'est pas de produire immédiatement une spécification exécutable, mais de formuler un retour Dev détaillé, argumenté et actionnable :

- ce qui est confirmé par l'analyse du code existant ;
- ce qui doit être repris côté front Odoo ;
- ce qui relève de la donnée BO ;
- ce qui doit rester soumis à arbitrage MOA ;
- l'ordre recommandé des lots de mise en œuvre.

Lecture synthétique :

> La MOA a raison sur le diagnostic d'expérience : la Home est propre mais encore trop générique ; le Shop est fonctionnel mais encore trop catalogue.
>
> Côté Dev, le sujet n'est pas de repartir à zéro. Le socle technique contient déjà plusieurs bonnes briques. Le prochain travail doit les consolider, les hiérarchiser et les alimenter avec une donnée plus cohérente.

Précision d'intention :

> Nous ne cherchons pas à casser Odoo, ni à produire du sur-design.
>
> Mais C-Kréyòl n'est pas une marketplace générique : c'est un vaisseau amiral créole. Chaque page publique doit traduire la promesse CK : sélection, origine, producteur, confiance et achat rapide.
>
> Le retour technique doit donc expliquer comment atteindre cette intention avec l'existant, ce qui est simple, ce qui est risqué, et ce qui doit être découpé en lots séparés.

---

## 2. Clarification sur les modules et sources de référence

### 2.1 Modules actifs à corriger

Les développements à produire doivent cibler prioritairement :

| Module | Rôle recommandé |
|---|---|
| `dorevia_ck_theme` | Thème générique CK : tokens, SCSS, layout, héritages `website_sale`, snippets éditables. |
| `dorevia_ck_marketone_content` | Contenu métier CK : pages CMS, enrichissements catalogue, cards, curation Home, navigation, rayons éditorialisés. |

Cette séparation est saine et doit être conservée.

Le thème doit rester aussi générique que possible. Les textes et contenus spécifiques C-Kréyòl doivent rester dans le module contenu lorsque cela est pertinent.

### 2.2 Ancien module `dorevia_ckreyol_marketone`

Le module `dorevia_ckreyol_marketone` correspond à une ancienne version du projet.

Il ne doit pas être traité comme le module actif à corriger, mais il reste utile comme source d'inspiration interne.

Doctrine recommandée :

| Usage | Décision |
|---|---|
| Inspiration UX / fonctionnelle | Oui |
| Référence de patterns déjà explorés | Oui |
| Copie directe de vues, contrôleurs ou modèles | Non |
| Source de vérité du rendu actuel | Non |
| Base d'implémentation cible | Non |

Formulation de travail :

> `dorevia_ckreyol_marketone` peut inspirer la structure Shop, les logiques de rayons, les cards ou la navigation, mais l'implémentation cible doit être portée dans `dorevia_ck_theme` et `dorevia_ck_marketone_content`.

---

## 3. Verdict Dev

Le retour MOA est globalement confirmé.

La Home donne déjà une impression de boutique sérieuse, mais elle ne porte pas encore assez tôt la promesse C-Kréyòl : sélection, origine, producteurs, confiance d'achat.

Le Shop est le chantier prioritaire. Il est techniquement stable, mais sa première lecture reste celle d'une interface de catalogue :

- filtres ;
- recherche ;
- tri ;
- compteur ;
- grille produits.

Il doit devenir un rayon boutique :

- contextualisé ;
- organisé ;
- rassurant ;
- marchand ;
- cohérent avec la promesse CK.

Point important : le code existant ne justifie pas une refonte radicale. Plusieurs briques attendues par la MOA existent déjà partiellement :

- cards CK structurées ;
- origine en eyebrow au-dessus du titre produit ;
- ligne secondaire de card avec tags, format et prix de référence ;
- rubans produit Odoo ;
- CTA panier compact ;
- logique de rayons éditorialisés ;
- source technique d'origine géographique ;
- brique native Odoo pour les avis/rating.

Le bon chantier est donc :

> Reprendre la hiérarchie de page et la gouvernance des données, pas remplacer le socle.

### 3.1 Intention directrice

C-Kréyòl doit rester une boutique Odoo maintenable, mais ne doit pas se lire comme une marketplace générique.

La promesse publique doit être perceptible sur chaque page importante :

| Promesse CK | Traduction attendue côté front |
|---|---|
| Sélection | Le client comprend que les produits sont choisis, pas simplement listés. |
| Origine | L'origine est visible, fiable, non inventée. |
| Producteur / partenaire | La personne ou structure derrière le produit est identifiable quand la donnée est certaine. |
| Confiance | Prix, format, avis réels, livraison et informations clés sont lisibles. |
| Achat rapide | Le panier reste accessible, simple et non noyé dans l'éditorial. |

Le point d'équilibre Dev est le suivant :

```text
Odoo reste le moteur.
CK devient la lecture commerciale.
```

Il ne faut donc pas casser les mécanismes natifs de `website_sale`. Il faut les orchestrer différemment, les alléger quand ils dominent trop la page, et les enrichir avec les données CK déjà disponibles.

### 3.2 Lecture Dev : simple, prudent, risqué

| Niveau | Actions | Lecture Dev |
|---|---|---|
| Simple | Wording Shop/Home, harmonisation `C-Kréyòl`, CTA, intro Shop, micro-copy, masquage CSS léger | Faible risque, impact rapide, pas de logique métier nouvelle. |
| Simple mais dépendant BO | Origines, tags, quantité nette, prix de référence, rubans, produits en vedette | Techniquement disponible, mais dépend de la qualité de saisie catalogue. |
| Prudent | Masquer conditionnellement recherche Shop, tri ou slider prix selon seuil catalogue | À faire sans casser les URLs ni les comportements natifs Odoo. |
| Prudent | Activer les avis produit natifs et les afficher seulement si `rating_count > 0` | Brique native disponible, mais flux de modération à vérifier. |
| Risqué | Afficher un producteur en card depuis `seller_ids` | Risque de fausse promesse : un fournisseur Odoo n'est pas toujours un producteur. |
| Risqué | Réorganiser profondément les facettes en groupes Origines / Univers / Préférences | Utile UX, mais peut devenir fragile si on réécrit le moteur attributs Odoo. |
| Lot séparé | Modèle producteur officiel, relation produit-producteur, pages producteurs dynamiques | Sujet métier durable, à spécifier proprement. |
| Lot séparé | Workflow complet de modération avis avant publication | À séparer si la modération native ne suffit pas. |
| Lot séparé | Reprise massive de l'ancien module `dorevia_ckreyol_marketone` | À utiliser en inspiration, pas en migration brute. |

Cette lecture doit guider le découpage : on livre d'abord ce qui rend la promesse visible sans risque, puis on traite les sujets de données et de modèle dans des lots dédiés.

---

## 4. État technique constaté

### 4.1 Shop — intro actuelle insuffisante

Le snippet d'introduction Shop existe dans `dorevia_ck_theme/views/snippets/ck_snippet_shop_intro.xml`.

État actuel :

```text
Boutique C-Kreyol
```

Le template ne rend aujourd'hui qu'un titre. La phrase de contexte et les preuves prévues dans le SCSS ne sont pas exploitées.

Constat Dev :

- l'emplacement est bon ;
- la structure est légère ;
- le rendu est trop pauvre par rapport à la promesse MOA ;
- le nom public doit être harmonisé en `C-Kréyòl`.

Recommandation :

Ajouter une introduction courte, non marketing, proche de :

```text
Boutique C-Kréyòl

Des produits créoles sélectionnés, aux origines identifiées,
disponibles à la commande pour la France et l'Europe.

7 produits sélectionnés · Expédition suivie depuis Nantes
```

Le compteur doit rester dynamique si possible. Si l'information d'expédition n'est pas encore juridiquement ou logistiquement stabilisée, la ligne doit être validée MOA avant livraison.

### 4.2 Shop — barre catalogue encore trop technique

Le code a déjà introduit une barre catalogue unifiée, avec filmstrip catégories, compteur, recherche et tri.

Cette amélioration est utile techniquement, mais la lecture MOA reste correcte : avec un petit catalogue, la zone donne encore trop tôt une impression d'outil de filtrage.

À conserver :

- mécanismes natifs Odoo ;
- URLs de recherche ;
- tri ;
- filmstrip catégories ;
- panier rapide ;
- compatibilité mobile.

À réduire en poids visuel :

- recherche interne Shop, redondante avec la recherche globale header ;
- tri visible par défaut, peu utile avec 7 produits ;
- compteur isolé ;
- slider prix, disproportionné en V1.

Recommandation Dev :

Ne pas supprimer la logique native. Masquer ou déprioriser l'interface.

Exemples de règles raisonnables :

- masquer le slider prix tant que le catalogue publié reste sous un seuil ;
- garder le tri discret ;
- afficher la recherche Shop seulement si une recherche est active ou si le catalogue dépasse un seuil ;
- conserver les paramètres URL pour ne pas casser les liens existants.

### 4.3 Shop — sidebar filtres

Le style de sidebar existe et applique déjà une structure plus lisible.

Le problème MOA n'est pas que les filtres sont faux, mais qu'ils prennent trop de poids dans une page encore courte.

Recommandation :

- conserver la sidebar ;
- la repositionner mentalement comme outil secondaire ;
- ne pas en faire le premier signal de maturité boutique ;
- éviter une refonte du moteur facettes Odoo.

Pour les libellés :

| Actuel | Proposition |
|---|---|
| Filtres | Affiner ma sélection |
| Étiquettes | Origines & préférences ou Préférences |
| Fourchette de prix | Budget |
| Trier par | Trier |

Point de vigilance : certains libellés viennent du nom d'attribut ou de templates natifs Odoo. La modification peut donc relever soit du BO, soit d'un héritage QWeb très ciblé. Ne pas faire de remplacement fragile par texte libre si l'ancre native Odoo est instable.

### 4.4 Shop — cards produit

Les cards sont déjà nettement plus avancées que le rendu MOA ne le laisse penser.

Le module contenu expose :

- `get_ck_shop_card_origin_label()` pour l'origine en eyebrow ;
- `get_ck_shop_card_metadata_line()` pour la ligne secondaire ;
- `ck_net_quantity`, `ck_net_quantity_uom_id`, `ck_reference_price_uom_id`, `ck_show_reference_price` pour le format et le prix de référence ;
- `website_ribbon_id` pour les badges Odoo.

La logique actuelle est saine :

```text
Origine
Titre produit
Tags transversaux · format · prix comparatif
Prix · CTA panier
```

Ce qui manque n'est pas principalement le HTML, mais la complétude de la donnée.

À faire :

- renseigner systématiquement l'attribut `Origines` ;
- ne plus porter les origines via tags, sauf fallback transitoire ;
- renseigner quantité nette et unité de référence sur les produits éligibles ;
- clarifier les tags transversaux affichables ;
- limiter les rubans `Nouveau !` ;
- réserver `Coup de cœur` aux produits explicitement curatés.

### 4.5 Origine géographique

La source technique de référence existe :

```text
dorevia_ck_marketone_content/ck_product_origin.py
```

Doctrine actuelle :

- source de référence : attribut produit contenant `Origine` / `Origin` ;
- fallback transitoire : première étiquette géographique détectée ;
- tags produit : réservés aux étiquettes transversales.

Cette doctrine correspond bien à la MOA.

Recommandation :

Passer progressivement du fallback transitoire à une règle stricte :

```text
Origine publique = attribut produit "Origines" uniquement.
```

Mais seulement après reprise BO, afin d'éviter une régression visuelle immédiate.

### 4.6 Producteur / fournisseur

La MOA demande de mieux afficher qui est derrière le produit.

Techniquement, plusieurs sources possibles existent ou sont évoquées :

- `seller_ids.partner_id` via Odoo Purchase si le fournisseur est renseigné ;
- pages CMS producteurs ;
- contenus `website_description` ;
- navigation producteurs ;
- anciennes idées issues de `dorevia_ckreyol_marketone`.

Point Dev important :

> `seller_ids` ne signifie pas automatiquement "producteur".

Dans Odoo, le fournisseur peut être :

- un producteur ;
- un transformateur ;
- un distributeur ;
- un grossiste ;
- un importateur ;
- un partenaire logistique.

Recommandation :

Ne pas afficher `producteur` sur les cards tant que la source officielle n'est pas arbitrée.

Options possibles :

| Option | Avantage | Risque |
|---|---|---|
| Afficher `fournisseur` depuis `seller_ids` | Donnée standard Odoo | Moins émotionnel, pas toujours producteur |
| Créer/identifier une fiche producteur liée | Plus juste commercialement | Demande modèle ou convention robuste |
| Afficher seulement sur fiche produit | Moins dense en card | Moins visible au choix produit |
| Ne rien afficher en V1 | Pas de fausse promesse | Manque une preuve CK importante |

Décision recommandée :

```text
V1 : afficher origine + tags + format sur cards.
V1.1 : ajouter producteur/fournisseur uniquement après arbitrage de la source officielle.
```

### 4.7 Rating / avis clients

Odoo 19 fournit déjà une brique native exploitable :

- `website_sale` dépend de `portal_rating` ;
- `product.template` hérite de `rating.mixin` ;
- `product.rating_avg` et `product.rating_count` existent ;
- la vue native `website_sale.product_comment` existe, mais elle est inactive par défaut ;
- le domaine rating produit ne prend en compte que les avis non internes.

Conclusion Dev :

> Il ne faut pas inventer un système d'avis CK si le besoin V1 est simplement d'afficher des avis produit réels.

Périmètre recommandé :

1. Activer et adapter la vue native `website_sale.product_comment`.
2. Traduire/adapter les libellés publics.
3. Vérifier le flux de publication et de modération.
4. Afficher la note sur fiche produit.
5. Afficher la note en card uniquement si `rating_count > 0`.
6. Ne pas afficher d'étoiles vides en shop.
7. Ne pas ajouter de tri par note en V1.

Point de vigilance :

La brique native couvre le stockage, la moyenne, le compteur et le widget. En revanche, la modération "avant publication" doit être testée précisément. Si la MOA veut une validation préalable stricte, un complément de workflow peut être nécessaire.

### 4.8 Rayon éditorialisé

Le module `dorevia_ck_marketone_content` contient déjà une logique de rayon éditorialisé pour Épicerie.

Doctrine actuelle :

- seuil minimum de familles ;
- seuil minimum de produits publiés ;
- pas de fausses sous-familles ;
- images issues de vrais produits ;
- masquage automatique si le rayon n'est pas assez alimenté.

Cette logique est très alignée avec l'analyse MOA.

Recommandation :

Ne pas forcer le même traitement sur Boissons, Soin & bien-être ou Artisanat tant que ces rayons n'ont pas assez de profondeur.

La bonne approche est :

```text
Épicerie = rayon pilote éditorialisé.
Autres rayons = listing propre + attente enrichissement catalogue.
```

---

## 5. Analyse Home

### 5.1 Ce qui fonctionne

La Home n'est pas à refaire.

Le code contient déjà :

- un hero CK ;
- une promesse de livraison France & Europe ;
- une section `Nos coups de cœur` ;
- une logique de produits vedettes pilotée par `ck_is_featured` ;
- des cards SSR contrôlées ;
- un bloc éditorial bas de page ;
- des liens vers démarche, producteur, recettes ;
- une présence Pro.

Le problème est donc davantage éditorial que technique.

### 5.2 Limite actuelle

Le hero actuel reste compréhensible, mais générique :

```text
Les saveurs créoles, prêtes à commander.
```

Il dit bien ce que l'utilisateur peut faire, mais pas assez pourquoi C-Kréyòl est différent.

Même chose pour le CTA :

```text
Voir la boutique
```

Il fonctionne, mais ne porte pas la notion de sélection.

### 5.3 Recommandation Home V2

Ne pas engager une refonte lourde.

Faire une passe de storytelling léger :

- harmoniser `C-Kreyol` vers `C-Kréyòl` dans les textes publics ;
- renforcer le hero ;
- introduire un bloc court `Notre promesse` plus haut dans la page ;
- contextualiser les coups de cœur ;
- rendre le B2B un peu plus visible ;
- préserver la stabilité des cards et du panier rapide.

Exemple de promesse courte :

```text
Notre promesse

Nous sélectionnons des produits créoles dont l'origine, le producteur
et l'usage sont clairement identifiés. Chaque référence doit pouvoir être
comprise, achetée et partagée en confiance.
```

Exemples de CTA :

| CTA actuel | Alternative recommandée |
|---|---|
| Voir la boutique | Découvrir la sélection |
| Espace professionnel | Demande professionnelle |

---

## 6. Décisions de wording

### 6.1 Nom public

Décision recommandée :

```text
C-Kréyòl
```

Usage :

- titres publics ;
- header ;
- hero ;
- intro Shop ;
- footer ;
- pages CMS.

Exceptions possibles :

- slugs ;
- noms techniques ;
- clés XML ;
- commentaires historiques ;
- compatibilité ASCII si nécessaire.

### 6.2 Soin & bien-être

Décision recommandée :

```text
Soin & bien-être
```

Raison :

Le catalogue actuel semble davantage concerner savon, soin, cosmétique ou bien-être personnel que maison/décoration.

`Maison & bien-être` pourra revenir plus tard si l'univers maison/artisanat/décoration devient réellement structuré.

### 6.3 Badges

Doctrine recommandée :

| Badge | Sens |
|---|---|
| Nouveau ! | Produit récemment ajouté, usage limité |
| Coup de cœur | Produit explicitement curaté CK |
| Origine identifiée | Preuve structurelle, plutôt dans la meta ou la page que comme badge répétitif |
| Avis | Preuve sociale réelle uniquement |

Règle :

> Aucun badge ne doit servir à remplir visuellement une card.

---

## 7. Lots Dev recommandés

### Lot 1 — Shop Structure V1

Objectif :

> Faire passer `/shop` d'une interface catalogue à un rayon boutique CK clair, chaud et commercial.

Périmètre :

1. Enrichir l'intro Shop.
2. Harmoniser `Boutique C-Kreyol` en `Boutique C-Kréyòl`.
3. Ajouter une phrase de contexte.
4. Ajouter ou rétablir des preuves légères si elles sont validées.
5. Masquer ou déprioriser le slider prix avec petit catalogue.
6. Réduire le poids de la recherche Shop.
7. Garder le tri discret.
8. Conserver les mécanismes natifs Odoo.
9. Ne pas modifier prix, stock, panier, variantes.

Hors périmètre :

- refonte moteur facettes ;
- nouveau modèle catalogue ;
- avis/rating ;
- nouveau champ producteur ;
- changement de prix ;
- changement logistique.

Tests et recette :

- `/shop` desktop ;
- `/shop` mobile 390 ;
- `/shop/category/epicerie-1` ;
- recherche encore fonctionnelle si URL existante ;
- tri encore fonctionnel ;
- panier rapide encore fonctionnel ;
- absence d'overflow horizontal.

### Lot 2 — Gouvernance Données Produit

Objectif :

> Alimenter correctement les preuves visibles sur cards et fiches produit.

Périmètre :

1. Contrôler les produits publiés.
2. Renseigner l'attribut `Origines`.
3. Nettoyer les tags géographiques.
4. Réserver les tags aux préférences/univers.
5. Renseigner quantités nettes et unités.
6. Contrôler les prix de référence.
7. Rationaliser les rubans.
8. Identifier les produits réellement `Coup de cœur`.

Livrable attendu :

Un tableau de reprise BO :

```text
Produit · Origine · Tags transversaux · Quantité nette · Unité réf. · Ruban · En vedette
```

Hors périmètre :

- modèle producteur ;
- rating ;
- SEO long ;
- contenu réglementaire exhaustif.

### Lot 3 — Rating-1

Objectif :

> Activer les avis produit comme preuve de confiance réelle.

Périmètre :

1. Activer la vue native `website_sale.product_comment`.
2. Adapter les libellés en français.
3. Vérifier l'expérience utilisateur connecté / public.
4. Vérifier la visibilité publique des avis.
5. Mettre en place la règle d'affichage card :

```xml
t-if="product.rating_count > 0"
```

6. Afficher note moyenne et nombre d'avis.
7. Ne pas afficher d'étoiles vides sur les cards sans avis.
8. Ne pas activer de tri par note en V1.

Point à arbitrer :

La MOA doit confirmer si la modération native suffit ou si un workflow complémentaire est attendu.

### Lot 4 — Home V2 Storytelling Léger

Objectif :

> Passer d'une Home e-commerce propre à une Home CK plus incarnée.

Périmètre :

1. Ajuster wording hero.
2. Remplacer `Voir la boutique` par un CTA plus différenciant.
3. Ajouter un bloc court `Notre promesse`.
4. Mieux contextualiser `Nos coups de cœur`.
5. Rehausser la visibilité de l'espace Pro.
6. Conserver les mécanismes de cards SSR et panier rapide.

Hors périmètre :

- refonte complète Home ;
- nouveau moteur de curation ;
- nouvelle logique de prix ;
- nouveau modèle éditorial.

---

## 8. Points MOA à arbitrer avant exécution

Les points suivants doivent être décidés avant d'écrire le code définitif :

| Sujet | Décision attendue |
|---|---|
| Intro Shop | Texte exact |
| Nom public | Validation `C-Kréyòl` partout en public |
| Soin & bien-être | Validation du wording |
| Slider prix | Masquage en V1 ou seuil dynamique |
| Recherche Shop | Masquage, maintien ou affichage conditionnel |
| Producteur/fournisseur | Source officielle et libellé |
| Badges | Règles d'usage exactes |
| Rating | Modération native suffisante ou workflow complémentaire |
| Home CTA | Wording final |
| Promesse Home | Texte exact |

---

## 9. Recommandations d'implémentation Odoo

### 9.1 Rester dans les héritages QWeb ciblés

Ne pas réécrire `website_sale.products`.

Utiliser :

- héritages QWeb courts ;
- classes CSS existantes ;
- hooks et helpers déjà présents ;
- variables natives Odoo lorsque disponibles.

### 9.2 Ne pas casser les comportements natifs

À préserver :

- recherche ;
- tri ;
- filtres ;
- facettes attributs ;
- offcanvas mobile ;
- panier rapide ;
- wishlist si installée ;
- catégories Odoo ;
- URLs existantes.

Le masquage visuel doit être réversible.

### 9.3 Ne pas inventer de données

Règles :

- pas d'origine fictive ;
- pas de producteur si la source n'est pas validée ;
- pas d'avis fictif ;
- pas d'étoiles vides en card ;
- pas de sous-famille vide ;
- pas de badge décoratif.

### 9.4 Garder la séparation thème / contenu

Recommandation :

| Type de changement | Module cible |
|---|---|
| SCSS générique, layout Shop, classes card | `dorevia_ck_theme` |
| Texte CK, contenu Shop, rayons éditorialisés | `dorevia_ck_marketone_content` |
| Données produit, curation Home | `dorevia_ck_marketone_content` |
| Inspiration ancienne version | `dorevia_ckreyol_marketone` en lecture seulement |

---

## 10. Critères de réussite

### 10.1 Shop

Le lot Shop sera réussi si la page ne lit plus comme :

```text
interface Odoo avec filtres
```

mais comme :

```text
rayon boutique CK, organisé, rassurant et prêt à commander
```

Critères concrets :

- promesse CK visible avant la grille ;
- origine visible sur les produits alimentés ;
- filtre prix absent ou discret avec petit catalogue ;
- recherche/tri non dominants ;
- cards lisibles ;
- aucun produit avec donnée inventée ;
- panier rapide intact ;
- mobile 390 propre.

### 10.2 Home

Le lot Home sera réussi si :

- la promesse CK est perceptible sans scroll long ;
- les coups de cœur sont compris comme une sélection ;
- le CTA principal invite à découvrir une sélection, pas seulement à ouvrir un catalogue ;
- le B2B est visible sans dominer la page B2C ;
- aucune section ne devient un manifeste trop long.

### 10.3 Rating

Le lot Rating sera réussi si :

- les avis sont réels ;
- seuls les avis publiés sont pris en compte ;
- les cards sans avis n'affichent pas d'étoiles ;
- les fiches produit peuvent recueillir un avis ;
- la modération est documentée ;
- mobile et desktop sont testés.

---

## 11. Conclusion Dev

L'analyse MOA identifie bien le problème : C-Kréyòl ne doit pas être perçu comme une simple grille de produits créoles.

Mais le code actuel n'est pas un mauvais socle. Il contient déjà :

- des cards adaptées ;
- une logique d'origine ;
- une curation Home ;
- un début d'éditorialisation rayon ;
- des chemins vers producteurs ;
- la compatibilité rating native Odoo.

La bonne suite n'est donc pas :

```text
refaire Home et Shop
```

mais :

```text
réordonner la page Shop, fiabiliser les données produit,
activer les preuves réelles, puis renforcer la Home par petites touches.
```

Le cap produit est clair :

```text
Ne pas casser Odoo.
Ne pas sur-designer.
Mais faire lire CK comme un vaisseau amiral créole :
sélection, origine, producteur, confiance, achat rapide.
```

Priorité recommandée :

1. **Shop Structure V1** ;
2. **Gouvernance Données Produit** ;
3. **Rating-1** ;
4. **Home V2 Storytelling léger**.

Ce séquencement limite le risque technique, respecte Odoo, évite les fausses promesses et répond directement au besoin MOA : réinjecter la promesse CK au moment où le client choisit ses produits.
