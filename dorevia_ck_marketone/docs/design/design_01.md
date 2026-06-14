# DESIGN_01.md CK — C-Kreyol / Marketone — v1.1

## 1. Statut du document

Ce document est la version 1.1 du référentiel design CK pour la phase Open Design du projet `dorevia_ck_marketone`.

Cette version intègre les retours QA et Dev sur `design_01.md` : enrichissement de la grille de traduction Odoo, clarification des packs, précision de l’entrée pro, rappel mobile-first et exigence de tokens design avant validation AMOA.

Il est destiné à guider la production des maquettes :

```text
Accueil
/shop
Fiche produit — layout achat
```

Il ne déclenche aucun développement Odoo.

Il sert à produire une cible visuelle et UX validable par la MOA, relisible par le Dev et testable par le QA.

---

## 2. Vision design

CK doit devenir un vrai site marchand pour les productions agro-transformées issues des zones créoles.

Le design doit soutenir trois promesses :

```text
Sourcer
Valoriser
Vendre
```

Le design ne doit pas seulement “faire joli”. Il doit aider à :

- comprendre l’offre ;
- avoir envie de découvrir ;
- avoir confiance ;
- voir les produits ;
- lire les prix ;
- passer à l’achat ;
- percevoir la dimension B2B sans complexifier le parcours B2C ;
- rester traduisible dans Odoo.

Phrase directrice :

> CK doit être marchand, vivant, gourmand, clair et traduisible dans Odoo.

---

## 3. Promesse utilisateur

### 3.1 Pour le particulier

> Je découvre et j’achète facilement des produits créoles de qualité, avec des prix clairs, des produits bien présentés et une livraison rassurante.

### 3.2 Pour le professionnel

> Je comprends rapidement que CK peut aussi servir des boutiques, restaurants, distributeurs ou acheteurs en volume, même si le parcours pro complet n’est pas encore développé en phase 1.

### 3.3 Pour le découvreur

> Je peux explorer des produits que je ne connais pas encore, comprendre leur origine, leur usage et leur intérêt.

---

## 4. Ton

Le ton doit être :

```text
marchand
chaleureux
direct
vivant
gourmand
simple
rassurant
professionnel
```

Le ton ne doit pas être :

```text
trop institutionnel
trop poétique
trop folklorisant
trop premium distant
trop technique
trop marketplace impersonnelle
```

Exemples de formulation souhaitée :

```text
Découvrez les saveurs créoles à cuisiner, offrir et partager.
Des produits créoles sélectionnés, prêts à être livrés chez vous.
Vous êtes professionnel ? Parlons volumes, régularité et approvisionnement.
```

---

## 5. Ambiance visuelle

L’ambiance doit être :

```text
vivante
gourmande
lumineuse
claire
structurée
commerciale
rassurante
```

Le design doit laisser la place aux produits.

Les images produits doivent être les éléments les plus parlants.

La couleur doit guider, hiérarchiser et donner envie, mais ne doit pas concurrencer les produits.

---

## 6. Direction artistique

La direction artistique est réouverte.

Les anciennes pistes suivantes sont historiques et ne sont pas la cible obligatoire :

```text
terracotta
sauge
crème
pastel premium
warm-editorial comme direction imposée
ancien prototype CK
ancienne mémoire Open Design
```

Le design peut explorer une nouvelle palette plus marchande, alimentaire et vivante.

Critères de choix couleur :

```text
mettre les produits en valeur
garder une très bonne lisibilité
soutenir l’action d’achat
éviter l’effet galerie décorative
éviter l’exotisme caricatural
rester compatible thème Odoo
```

---

## 7. Inspiration

L’inspiration “efficacité directos.eu” est retenue pour :

- promesse immédiate ;
- catégories fortes ;
- produits très visibles ;
- prix lisibles ;
- CTA directs ;
- réassurance claire ;
- ton vivant ;
- profondeur catalogue ;
- packs / lots / offres visibles ;
- contenus utiles à l’achat ;
- orientation conversion.

Cette inspiration ne doit pas être copiée graphiquement.

Règle :

> On retient l’efficacité marchande, pas l’identité graphique.

---

## 8. Écrans phase 1

La phase 1 doit couvrir explicitement :

```text
Accueil
/shop
Fiche produit — layout achat
```

### Hors périmètre phase 1

```text
panier complet
checkout complet
portail revendeur
workflow devis B2B
listes de prix pro dynamiques
gestion logistique avancée
```

Le panier et le checkout peuvent être indiqués comme continuité Odoo, mais ne doivent pas être maquettés comme tunnel complet autonome.

---

## 9. Accueil — règles design

L’accueil doit répondre rapidement à trois questions :

```text
Qu’est-ce que CK vend ?
Pourquoi acheter ici ?
Où commencer ?
```

Éléments attendus :

- promesse claire au-dessus de la ligne de flottaison ;
- CTA principal vers la boutique ;
- CTA secondaire ou signal vers les professionnels ;
- catégories fortes ;
- produits ou packs mis en avant ;
- réassurance livraison/paiement ;
- mention de la logique de sourcing ;
- ton vivant et gourmand.

L’accueil ne doit pas devenir une page éditoriale longue avant l’achat.

---

## 10. Page `/shop` — règles design

La page boutique est le cœur de la phase 1.

Elle doit permettre :

- lecture immédiate des produits ;
- navigation par catégories ;
- compréhension des origines ;
- lecture des prix ;
- accès rapide à l’achat ;
- réassurance visible ;
- signal B2B secondaire ;
- exploration agréable.

Structure attendue :

```text
Header / navigation
Titre boutique + promesse courte
Zone filtres
Toolbar / tri
Grille produits
Cartes produits
Réassurance
Entrée pro secondaire
Pagination ou chargement
```

La page `/shop` doit rester compatible avec `website_sale`.

---

## 11. Fiche produit — règles design

La fiche produit doit permettre de décider l’achat.

Éléments attendus :

- image produit dominante ;
- nom produit clair ;
- prix très lisible ;
- format / poids ;
- origine ;
- catégorie ;
- quantité ;
- CTA achat visible ;
- réassurance livraison / paiement ;
- court texte d’usage ;
- éventuel signal pack / pro ;
- produits liés ou suggestions si utile.

La fiche produit ne doit pas créer un checkout parallèle.

---

## 12. Carte produit — règles design

La carte produit est un composant central.

Elle doit contenir au minimum :

```text
image produit
nom produit
prix
origine ou zone
catégorie ou famille
CTA achat ou accès rapide
```

Elle peut contenir :

```text
badge nouveauté
badge pack
format / poids
indication pro discrète
court usage
```

Preuves à l’écran :

```text
Le prix est visible.
Le CTA est visible.
L’image donne envie.
Le nom est lisible.
La carte ne dépend pas d’un comportement JS local.
```

---

## 13. B2C / B2B phase 1

### Positionnement — matrice fournisseur / distributeur

```text
CK n’est pas seulement une boutique B2C.
CK est une plateforme d’intermédiation commerciale et logistique entre producteurs / transformateurs créoles et commerces spécialisés.

Archétype fournisseur : La Platine.
Archétype distributeur brick & mortar : Kemet Exotique.

Le B2C reste une vitrine marchande et un canal de vente directe.
L’entrée professionnelle prépare la qualification de deux familles :
1. fournisseurs / producteurs souhaitant proposer leurs produits ;
2. distributeurs physiques souhaitant référencer et approvisionner leur point de vente.
```

### Lecture phase 1

La lecture phase 1 est :

```text
B2C = parcours principal visible et achetable
B2B = entrée secondaire visible, non complète
```

### B2C

Le B2C est le cœur du parcours.

Le particulier doit pouvoir acheter sans comprendre toute la vision CK.

### B2B

Le B2B doit être visible mais secondaire.

Éléments possibles :

```text
Lien “Professionnels”
Bloc “Vous êtes revendeur ?”
CTA “Demander un accès pro”
Mention “Achat en volume”
Bloc “Boutiques, restaurants, distributeurs”
```

Ne pas concevoir à ce stade :

```text
portail complet
prix masqués
listes de prix dynamiques
workflow devis
logique commerciale B2B complète
```

---

## 14. Réassurance

La réassurance doit être visible dans le parcours boutique.

Thèmes de réassurance :

```text
livraison
paiement sécurisé
origine des produits
sélection des producteurs
service client
offre pro
promesse logistique
```

Preuves à l’écran :

```text
La livraison est mentionnée.
Le paiement est rassurant.
Le contact ou service client est trouvable.
L’origine produit est compréhensible.
L’entrée pro existe mais reste secondaire.
```

---

## 15. Mobile-first

Le design doit être mobile-first.

Règles :

```text
Grille mobile : 1 colonne, éventuellement 2 selon largeur.
Filtres mobile : drawer, accordéon ou panneau repliable.
CTA achat : visible sans effort.
Prix : lisible sur carte et fiche.
Réassurance : accessible sans chercher.
Header : compact et lisible.
Images : suffisamment grandes.
B2B : présent mais secondaire.
```

Le mobile ne doit pas être une réduction maladroite du desktop.

---

## 16. Contraintes Odoo

La maquette doit être traduisible dans Odoo.

Contraintes :

```text
Odoo reste la source de vérité métier.
website_sale reste le moteur boutique.
Le panier reste Odoo.
Le checkout reste Odoo.
Les prix viennent d’Odoo.
Les produits viennent d’Odoo.
Les catégories et attributs doivent pouvoir être traduits en logique Odoo.
Les composants visuels doivent pouvoir devenir thème, QWeb ou snippets.
```

Interdits techniques pour la cible :

```text
catalogue JS local
panier simulé comme comportement cible
checkout hors website_sale
prix figés dans le HTML comme source cible
SPA React/Vue comme boutique
front autonome
```

---

## 17. Annotation traduction Odoo par composant

Cette section prépare la future grille de traduction entre la maquette Open Design et Odoo.

Elle ne déclenche aucun développement.  
Elle permet seulement d’identifier, composant par composant, ce qui relèvera plus tard :

```text
du thème
du template website_sale
d’un snippet / bloc éditorial
d’une extension éventuelle
d’un arbitrage MOA ultérieur
```

| Composant | Lecture design | Traduction Odoo probable | Couche | Statut phase 1 |
|---|---|---|---|---|
| Header | navigation, recherche, panier | `website.layout` | Thème / template | Autorisé |
| Recherche header | recherche produit | route recherche `website_sale` | Template natif + thème | Autorisé |
| Hero accueil | promesse + CTA | snippet / bloc website | Thème / snippet | Autorisé |
| Catégories | entrée catalogue | catégories e-commerce Odoo | Template + thème | Autorisé |
| Origines | navigation par zone | attribut produit ou extension | À trancher | Visible en maquette, source Odoo à décider |
| Collections | mise en avant commerciale | tags, catégories dédiées ou modèle custom | À trancher | Visible en maquette, mécanique à décider |
| Packs | offre commerciale | produit pack / décision MOA conservée | À trancher | Autorisé si pas de checkout parallèle |
| Carte produit | vendre depuis grille | `website_sale` + styles CK | Thème + template | Autorisé |
| Prix | affichage marchand | pricelist Odoo | Template | Autorisé |
| Prix B2B | signal offre pro | page / contact / demande accès pro | Hors mécanique phase 1 | Signal uniquement |
| Filtre prix | navigation prix | prudence Odoo CE / extension possible | À trancher | Maquette autorisée, traduction non figée |
| Tri toolbar | ordre d’affichage | paramètre `order` natif `website_sale` | Template natif + thème | Autorisé |
| Pagination | navigation catalogue | pager Odoo `/shop/page/N` | Template natif + thème | Autorisé |
| État vide | aucun produit trouvé | QWeb conditionnel `website_sale` | Template | Autorisé |
| Quick-add éventuel | achat rapide depuis carte | action Odoo / héritage template | Template métier léger | Autorisé seulement si Odoo standard, pas panier custom |
| Fiche produit | décision d’achat | `website_sale.product` | Template + thème | Autorisé |
| Quantité fiche produit | choix quantité | widget natif fiche produit | Template natif + thème | Autorisé |
| Produits liés | suggestions / alternatives | `alternative_product_ids` ou équivalent Odoo | Template natif + thème | Autorisé |
| Bandeau réassurance | confiance achat | snippet statique ou bloc éditorial | Thème / snippet | Autorisé |
| Entrée pro | signal B2B | page CMS + formulaire contact / `website_crm` éventuel | Snippet + page | Signal uniquement, pas portail |
| Panier | continuité achat | Odoo standard | Hors maquette complète | Non maquetté comme tunnel |
| Checkout | finalisation achat | Odoo standard | Hors maquette complète | Non maquetté comme tunnel |

Règles :

```text
La maquette peut montrer des entrées visuelles.
La maquette ne doit pas figer un modèle métier non arbitré.
Les origines, collections, packs et filtres prix doivent rester annotés “source Odoo à décider” tant que la grille de traduction n’est pas validée.
Le quick-add ne doit jamais être interprété comme panier custom.
L’entrée pro doit rester un signal ou une page d’intention en phase 1, pas un portail B2B.
```

---

## 18. Interactions autorisées

Interactions compatibles avec la cible :

```text
liens Odoo
navigation URL
rechargement de page
filtres traduits en URL / domaine
accordéons visuels
drawer mobile pour filtres
CTA vers panier Odoo
```

Interactions à éviter comme cible :

```text
filtrage catalogue purement JS
panier localStorage
checkout custom
état boutique autonome
API front dédiée sans nécessité
```

---

## 19. Décisions MOA métier conservées

Cette section identifie les décisions métier issues de l’existant ou des arbitrages précédents qui doivent rester visibles dans la phase design.

Objectif :

> Ne pas reprendre automatiquement le code `dorevia_ckreyol_marketone`, mais ne pas oublier les décisions métier encore pertinentes.

| Sujet | Décision de référence | Statut design phase 1 |
|---|---|---|
| Packs | Ne pas recréer de checkout parallèle | Opposable |
| Packs `non_detailed` | Un pack peut être vendu comme un produit / une ligne panier si cette doctrine est conservée | À confirmer définitivement par David avant traduction Odoo |
| Collections | Peuvent être visibles en maquette | Source Odoo à trancher après maquette |
| Origines | Peuvent être visibles en maquette | Attribut produit ou extension à trancher après maquette |
| Prix B2B | Pas de mécanique de prix pro en phase 1 | Signal uniquement : “offre pro sur demande” ou “accès pro à venir” |
| Entrée pro | L’entrée pro doit exister sans concurrencer le B2C | Page d’intention ou formulaire, pas portail revendeur |
| Quick-add | Autorisé comme intention commerciale légère | Action Odoo standard ou décision Dev ultérieure, jamais panier custom |

Règles :

```text
La maquette ne doit pas exploser les packs en lignes de checkout.
La maquette ne doit pas inventer un moteur de packs autonome.
La maquette ne doit pas afficher de prix B2B dynamiques.
La maquette ne doit pas suggérer un portail revendeur complet.
Les collections et origines sont des entrées visuelles acceptées, mais leur source Odoo reste à décider.
```

L’existant `dorevia_ckreyol_marketone` reste une mémoire d’analyse, pas un socle technique automatique.

---

## 19 bis. Tokens design avant validation AMOA

Toute direction graphique proposée par Open Design devra être documentée en tokens avant validation AMOA.

Les tokens minimaux attendus sont :

```text
couleurs principales
couleurs secondaires
couleurs de fond
couleurs CTA
couleurs prix
couleurs badges
typographies
tailles de titres
tailles de textes
espacements
rayons / radius
ombres
grille responsive
```

Règle :

> Une direction visuelle ne peut pas être validée uniquement “à l’œil”. Elle doit pouvoir être traduite en variables SCSS et en règles de thème Odoo.

---

## 20. Preuves à l’écran

Chaque intention doit avoir une preuve visible.

| Intention | Preuve attendue |
|---|---|
| Marchand | prix, CTA, grille produit, panier visible |
| Gourmand | images produit dominantes, mise en avant usage |
| Vivant | catégories, packs, rythme visuel |
| Clair | hiérarchie, navigation simple, textes courts |
| Rassurant | livraison, paiement, origine, contact |
| B2B visible | entrée pro secondaire |
| Compatible Odoo | filtres, prix, panier et checkout non parallèles |
| Mobile-first | grille, CTA et filtres utilisables sur mobile |

---

## 21. Interdits design / UX

Sont interdits :

```text
site galerie sans achat clair
boutique trop décorative
cartes produit sans prix
CTA achat invisible
filtres impossibles à traduire dans Odoo
logique panier hors Odoo
checkout alternatif
catalogue statique hors Odoo
front autonome
effets visuels qui concurrencent les produits
ancienne DA réinjectée par défaut
```

Règle :

> Le design doit servir l’achat, la compréhension et la confiance.

---

## 22. Critères de validation

Le DESIGN.md CK est validable s’il permet de produire une maquette :

```text
marchande
vivante
gourmande
claire
rassurante
orientée achat
compatible Odoo
mobile-first
non dépendante d’un front autonome
testable par le QA
relisible par le Dev
arbitrable par David
```

La future maquette devra permettre de vérifier :

```text
□ Un acheteur comprend vite ce que CK vend.
□ Les catégories principales sont visibles.
□ Les produits sont visibles et désirables.
□ Les prix sont lisibles.
□ Le CTA achat est clair.
□ La fiche produit permet de décider.
□ La réassurance est visible.
□ L’entrée pro existe sans dominer.
□ La maquette ne suppose pas de boutique parallèle.
□ Les origines, collections, packs et filtres prix sont annotés avec leur source Odoo à décider.
□ Le quick-add éventuel ne suppose pas de panier custom.
□ L’entrée pro renvoie à une intention ou un formulaire, pas à un portail B2B complet.
□ La palette retenue est documentée en tokens.
```

---

## 23. Synthèse

La cible est :

```text
DESIGN.md CK
    → maquette accueil + /shop + fiche produit
        → revue Dev traduisibilité Odoo
            → recette QA maquette
                → arbitrage David
                    → décision Odoo ultérieure
```

Phrase finale :

> CK doit devenir un site marchand Odoo vivant, gourmand et efficace, capable de valoriser les produits créoles sans déplacer la vérité métier hors d’Odoo.
