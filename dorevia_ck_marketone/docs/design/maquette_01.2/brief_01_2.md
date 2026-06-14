# Brief maquette CK V1.2 — Boutique élégante

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Type** | Brief Dev / maquettage — évolution maquette home |
| **Base** | Maquette V1.1.1 · [`design_01.md`](../design_01.md) v1.1 |
| **Doctrine source** | [`note_05.md`](../../cadrage/note_05.md) — **actée MOA** |
| **Références** | [`note_05.md`](../../cadrage/note_05.md) · [`go_moa_maquette_01_2.md`](./go_moa_maquette_01_2.md) · [`recette_qa_maquette_01_2.md`](./recette_qa_maquette_01_2.md) · [`ticket_dev_maquette_01_2_open_design.md`](./ticket_dev_maquette_01_2_open_design.md) · [`ticket_moa_composition_cms_ck_01`](../ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md) · [`grille_traduction_odoo_v1.md`](../maquette_01/grille_traduction_odoo_v1.md) · [`points_a_arbitrer.md`](../maquette_01/points_a_arbitrer.md) |
| **GO MOA** | [`go_moa_maquette_01_2.md`](./go_moa_maquette_01_2.md) — **GO OFFICIEL confirmé** |
| **Date** | 2026-06-13 |
| **Statut** | **Livré Dev — en attente recette QA** |

> Ce brief décline opérationnellement la note d’itération MOA [`note_05.md`](../../cadrage/note_05.md). Il ne déclenche pas de développement Odoo — la composition Website Builder reprend **après** validation maquette V1.2.

---

## 1. Objet du brief

Ce brief demande l’évolution de la maquette CK vers une version V1.2 orientée e-commerce.

La V1.2 ne doit pas repartir de zéro. Elle doit reprendre l’identité visuelle déjà posée, mais renforcer la capacité commerciale de la home : produits visibles plus tôt, prix assumés, réassurance immédiate, catégories actionnables, coffrets / sélections et entrée professionnelle claire.

## 2. Contexte

Une première traduction de la maquette CK dans Odoo 19 CE a été menée sur l’instance `dorevia_ck_marketone_01`.

Cette phase a validé le socle technique :

* thème `dorevia_ck_theme` fonctionnel ;
* Website Builder exploitable ;
* snippets natifs Odoo utilisables ;
* catalogue Odoo capable de remonter des produits dans la home ;
* doctrine “Odoo 19 CE · snippets first · pas de surcouche autonome” confirmée.

La pause actuelle de la home Odoo n’est donc **pas** liée à un échec technique. Elle est liée à un écart de traduction commerciale.

### Verdict QA — home Odoo actuelle (2026-06-13)

```text
OK socle technique
OK faisabilité CMS
KO traduction cible commerciale complète
```

La home actuelle reste trop proche d’un squelette CMS et pas assez d’une boutique e-commerce active. La V1.2 doit combler cet écart **avant** reprise composition Odoo.

### Capital à préserver (V1.1.1 · instance)

La V1.2 **ne repart pas de zéro** :

| Élément | Source | Action V1.2 |
|---------|--------|-------------|
| Identité visuelle (palette · typo · ton) | Maquette V1.1.1 | Conserver · renforcer le marchand |
| Hero · promesse CK | Instance Odoo (`s_ck_hero`) | Raccourcir · CTAs boutique + Pro |
| Univers / catégories | Instance (`s_product_list` + cards) | Rendre actionnables · routes Odoo |
| Snippets CK Marketone | `dorevia_ck_theme` ticket 01 | Mapper chaque bloc maquette |
| Doctrine Pro double cible | Arbitrages MOA §10 | Maintenir · CTA `/professionnels` |

## 3. Doctrine MOA à appliquer

La maquette CK doit évoluer d’une logique de vitrine premium vers une logique de boutique élégante.

Doctrine cible :

> CK doit être une boutique claire, désirable et rassurante, capable de déclencher l’achat rapidement, tout en conservant une identité soignée.

L’élégance reste un critère de qualité, mais elle n’est pas la finalité.

La finalité est la **conversion**, entendue au sens MOA :

```text
Progression vers achat, consultation produit, ajout panier, contact professionnel ou qualification commerciale.
```

La conversion inclut la porte Pro et la qualification B2B, pas seulement le panier B2C.

Objectifs concrets par section :

* donner envie d’un produit ;
* faciliter l’accès à une catégorie ;
* montrer un prix ou une offre ;
* rassurer sur la livraison, le paiement ou la qualité ;
* orienter vers la boutique, le panier ou l’espace professionnel.

Une section belle mais qui ne montre ni produit, ni preuve, ni action utile doit être simplifiée, déplacée plus bas ou reformulée.

## 4. Rapport à Directos

Directos est une **référence d’efficacité e-commerce** — pas une référence d’identité CK.

```text
Directos = benchmark marchand (densité produit · prix · preuves · catégories)
Directos ≠ modèle graphique · identité · ton CK
```

À reprendre dans l’esprit :

* produits visibles rapidement ;
* prix visibles ;
* catégories actionnables ;
* messages de confiance répétés ;
* promesse logistique claire ;
* coffrets / sélections ;
* entrée professionnelle identifiable.

À ne pas reprendre :

* densité brute excessive ;
* empilement visuel ;
* identité graphique ;
* ton éditorial.

CK doit conserver une expérience plus élégante, plus respirante et plus soignée, mais sans perdre l’efficacité commerciale.

## 5. Structure cible de la home V1.2

La maquette V1.2 devra proposer une home structurée ainsi :

### 1. Header marchand clair

Objectif : supprimer tout effet générique / template.

À prévoir :

* marque CK / C-Kreyol clairement visible ;
* menu : Boutique, Catégories ou Univers, Professionnels ;
* recherche produit si possible ;
* panier visible ;
* suppression des éléments génériques type `Your Logo`, téléphone fictif, email fictif, `Nom de l’entreprise`.

### 2. Hero court et orienté action

Objectif : présenter la promesse sans monopoliser la page.

Le hero doit contenir :

* une promesse claire ;
* un CTA boutique ;
* un CTA professionnel ;
* un visuel cohérent avec les produits créoles, pas une image institutionnelle générique.

Le hero doit rester plus court qu’une vitrine contemplative, afin de laisser apparaître rapidement les preuves et les produits.

### 3. Réassurance immédiate

Objectif : lever les premiers doutes d’achat dès le haut de page.

Prévoir au moins 3 preuves visibles, par exemple :

* Livraison France / Europe ;
* Paiement sécurisé ;
* Producteurs sélectionnés ;
* Service client ;
* Conditions professionnelles sur qualification.

### 4. Produits mis en avant

Objectif : rendre la boutique concrète immédiatement.

Prévoir une section produits avec :

* 4 à 6 produits maximum ;
* nom produit ;
* prix visible ;
* origine ou famille si possible ;
* badge éventuel : nouveauté, coup de cœur, découverte ;
* CTA simple : Voir / Découvrir / Ajouter selon faisabilité Odoo ;
* visuel produit.

Cette section doit être pensée comme traduisible dans Odoo via snippet catalogue / produits dynamiques / produit natif.

### 5. Catégories / univers actionnables

Objectif : transformer les univers CK en portes d’achat.

Prévoir des entrées vers :

* Épicerie créole ;
* Maison & bien-être ;
* Artisanat ;
* Packs & découvertes.

Chaque entrée doit être liée à une route ou logique Odoo plausible, par exemple catégorie e-commerce `/shop/category/...`.

Les univers ne doivent pas être seulement décoratifs.

### 6. Packs / coffrets découverte

Objectif : renforcer la conversion et le panier moyen.

Prévoir une section ou un bloc mettant en avant :

* coffret découverte ;
* pack cadeau ;
* sélection première commande ;
* assortiment autour d’un usage.

Cette section peut être intégrée aux produits mis en avant ou devenir un bloc séparé si la maquette le justifie.

### 7. Espace professionnel

Objectif : maintenir la double cible CK.

Prévoir une section claire pour :

* producteurs / transformateurs créoles ;
* boutiques / distributeurs / restaurants / hôtels / revendeurs.

Le CTA doit pointer vers `/professionnels` ou une ancre dédiée, sans 404.

La section Pro doit être orientée qualification, pas portail B2B custom.

### 8. Contenu éditorial / SEO plus bas

Objectif : conserver la richesse éditoriale sans ralentir l’achat.

Le contenu de marque, les explications longues, le storytelling et le SEO doivent être placés après les blocs marchands prioritaires.

### 9. Footer CK propre

Objectif : supprimer tout contenu générique Odoo.

Le footer doit contenir :

* marque CK ;
* courte phrase de positionnement ;
* liens utiles ;
* contact ;
* mentions légales ou placeholder propre ;
* aucun texte générique type `produits disruptifs`, `yourcompany`, `Nom de l’entreprise`.

### Correspondance maquette → Odoo (indicative)

Chaque bloc V1.2 doit pouvoir être annoté pour traduction Builder. Correspondance cible :

| Bloc maquette V1.2 | Snippet CK / Odoo | Alternative native |
|--------------------|-------------------|--------------------|
| Header marchand | Layout thème + menu BO | `website` navbar |
| Hero court | `s_ck_hero` | Banner · Text-Image |
| Réassurance | `s_ck_reassurance` | Features · Columns |
| Produits vedettes | `s_ck_featured_products` + zone `oe_structure` | **Dynamic Products** · Products |
| Catégories / univers | `s_ck_category_links` | Links · pills · `s_product_list` |
| Coffrets / packs | Section produits ou bloc dédié | Dynamic Products (filtre catégorie) |
| Espace Pro | `s_ck_pro_banner` | Texte + CTA → `/professionnels` |
| Éditorial / SEO | Blocs texte CMS | Text · Image-Text |
| Footer CK | Footer thème + contenu BO | — |

La maquette doit indiquer, bloc par bloc, le mapping retenu (colonne « traduction Odoo » dans les livrables).

## 6. Mobile

La V1.2 doit être pensée mobile dès la maquette.

Sur mobile, l’ordre attendu est plus strict :

1. Hero court ;
2. Preuves / réassurance ;
3. Produits avec prix visibles ;
4. Catégories actionnables ;
5. Espace Pro ;
6. Éditorial / SEO ;
7. Footer.

Les produits et les preuves doivent apparaître avant tout contenu long.

## 7. Contraintes techniques

La maquette V1.2 doit rester traduisible dans Odoo 19 CE — cf. [`note_05.md`](../../cadrage/note_05.md) §6–7.

Contraintes à respecter :

* pas de front autonome ;
* pas de catalogue parallèle ;
* pas de panier / checkout custom ;
* pas de logique B2B custom ;
* pas de maquette impossible à traduire avec Website Builder ;
* privilégier les blocs mappables vers snippets natifs Odoo ou snippets CK Marketone existants.

La maquette peut améliorer l’intention visuelle, mais elle doit rester réaliste dans une exécution Odoo Website Builder.

## 8. Critères d’acceptation QA V1.2

Alignés sur [`note_05.md`](../../cadrage/note_05.md) §8. La maquette V1.2 sera **validée MOA/QA** si :

| # | Critère                 | Seuil attendu                                                                              |
| - | ----------------------- | ------------------------------------------------------------------------------------------ |
| 1 | Produits visibles       | Dans les 10 premières secondes en desktop, au premier scroll mobile                        |
| 2 | Prix visibles           | Prix affiché sur chaque carte produit mise en avant                                        |
| 3 | Preuves de confiance    | Au moins 3 preuves visibles haut de page                                                   |
| 4 | Catégories actionnables | Liens plausibles vers routes / catégories Odoo                                             |
| 5 | CTA Pro                 | Lien vers `/professionnels` ou ancre Pro, sans 404                                         |
| 6 | Footer                  | Aucun placeholder Odoo                                                                     |
| 7 | Sections complètes      | Aucun bloc vide ou lorem ipsum                                                             |
| 8 | Mobile                  | Produits + preuves avant éditorial long                                                    |
| 9 | Traduisibilité Odoo     | Chaque bloc doit pouvoir être mappé vers Odoo Website Builder / snippet natif / snippet CK |
| 10 | Liens / CTA             | Aucun lien principal vers une 404 non assumée                                              |
| 11 | Premier écran desktop   | La réassurance ou le début des produits doit être visible ou perceptible                    |

Verdict attendu :

```text
OK MAQUETTE CK V1.2 — BOUTIQUE ÉLÉGANTE
```

ou

```text
KO MAQUETTE V1.2 — corrections à reprendre (critères §8 non satisfaits)
```

Recette maquette : [`recette_qa_maquette_01_2.md`](./recette_qa_maquette_01_2.md).

## 9. Compléments QA à intégrer

### A. Clarification sur les univers phase 1

L’univers **Artisanat** doit être réinterrogé avant maquettage final.

La V1.2 doit éviter de rouvrir trop largement le périmètre catalogue. CK est prioritairement orienté vers :

* agro-transformation ;
* épicerie créole ;
* boissons / sirops ;
* coffrets découverte ;
* maison & bien-être lorsque le produit est cohérent avec l’univers CK.

Décision attendue MOA :

```text
Artisanat = à confirmer comme univers phase 1
ou
Artisanat = repoussé / renommé / fusionné avec une autre entrée
```

En attendant arbitrage, éviter de surdimensionner visuellement l’univers Artisanat dans la maquette.

### B. Produits indicatifs à utiliser dans la maquette

Pour éviter des cartes trop génériques, la maquette V1.2 devra utiliser des exemples de produits plausibles CK.

Liste indicative :

* Confiture de goyave / goyavier ;
* Galettes de manioc ;
* Manio Crackers sucré ;
* Manio Crackers salé ;
* Savon vétiver ;
* Coffret découverte créole ;
* Épices colombo ;
* Sirop tamarin ;
* Café, biscuit ou farine selon catalogue disponible.

Les produits utilisés dans la maquette ne sont pas nécessairement définitifs, mais ils doivent rester crédibles et cohérents avec le positionnement CK.

### C. CTA produit — préférence MOA

Pour les cartes produits de la home, privilégier les CTA suivants :

```text
Voir
Découvrir
Voir le produit
```

Le CTA `Ajouter au panier` ne doit être utilisé que si la faisabilité Odoo / Website Builder est confirmée et si la MOA valide explicitement ce niveau d’action depuis la home.

Doctrine retenue :

```text
Home V1.2 = orienter vite vers le produit
sans forcer un comportement e-commerce non maîtrisé.
```

### D. Réassurance — promesses tenables

Les éléments de réassurance doivent rester réalistes, tenables et validables par la MOA.

Exemples possibles :

* Livraison France / Europe, uniquement si la promesse logistique est réellement assumée ;
* Paiement sécurisé, si le parcours de paiement cible est confirmé ;
* Producteurs sélectionnés, si le processus de sélection est explicable ;
* Service client, si un canal de contact réel est prévu ;
* Conditions professionnelles sur qualification, si le formulaire / CRM permet la qualification.

Règle QA :

```text
Aucune promesse commerciale forte ne doit être affichée si elle n’est pas tenable opérationnellement.
```

### E. Liens et CTA — aucun lien mort

Tous les CTA et liens principaux de la maquette V1.2 doivent pointer vers :

* une route existante ;
* une ancre présente dans la page ;
* une route Odoo explicitement prévue ;
* ou une page à créer dans le périmètre du ticket.

Critère QA ajouté :

```text
Aucun lien principal ne doit aboutir à une 404 non assumée.
```

Ce point concerne notamment :

* Boutique ;
* Catégories / univers ;
* Professionnels ;
* Voir le produit ;
* Contact ;
* Panier ;
* Recherche si présente.

### F. Premier écran desktop

Sur desktop, le premier écran ne doit pas être entièrement consommé par un hero contemplatif.

Critère ajouté :

```text
Le premier écran desktop doit laisser entrevoir soit la réassurance,
soit le début des produits.
```

Objectif : rendre visible rapidement que CK est une boutique active, pas seulement une vitrine de marque.

### G. Footer et mention Odoo

Le footer doit être nettoyé de tout contenu générique :

* `Your Company` ;
* `Nom de l’entreprise` ;
* texte type “produits disruptifs” ;
* email ou téléphone fictif ;
* liens morts ;
* blocs non personnalisés.

Concernant la mention `Généré par Odoo` / promotion Odoo :

```text
À masquer si possible dans le cadre Odoo CE.
À défaut, l’écart devra être explicitement accepté comme contrainte technique temporaire.
```

La cible reste un footer CK propre, cohérent et sans effet template.

## 10. Livrable attendu

Livrable demandé :

```text
Maquette CK V1.2 — Home boutique élégante
```

Le livrable devra inclure :

* version desktop ;
* **version mobile obligatoire** — ou déclinaison responsive explicitement vérifiable ;
* structure des blocs ;
* textes principaux ;
* emplacement des produits ;
* emplacement des preuves de confiance ;
* entrée Pro ;
* footer propre ;
* [`TABLEAU_TRADUCTION_ODOO_V1_2.md`](./TABLEAU_TRADUCTION_ODOO_V1_2.md) — tableau traduction Odoo par bloc (cf. §5) ;
* [`LIVRAISON_V1_2.md`](./LIVRAISON_V1_2.md) — note de livraison · réserves · arbitrages.

## 11. Suite post-V1.2 — reprise Odoo

Arbitrage MOA acté — [`arbitrage_moa_maquette_01_2.md`](./arbitrage_moa_maquette_01_2.md) :

```text
GO TRADUCTION ODOO — MAQUETTE CK V1.2
AVEC RÉSERVES MOA ACCEPTÉES
```

```text
1. ✅ Validation MOA/QA maquette — recette + arbitrage
2. ✅ Tableau traduction V1.2 — TABLEAU_TRADUCTION_ODOO_V1_2.md
3. ☐ Reprise composition home Odoo — bloc par bloc (ticket CMS §0.4)
4. ☐ Page /professionnels + menu Professionnels (parallèle · obligatoire avant go-live)
5. ☐ Recette composition — recette_qa_composition_cms_ck_01.md
6. ☐ Verdict — OK ou KO composition CMS CK 01
```

En parallèle : config Dynamic Products · mapping routes BO · non-régression `/shop`.

## 12. Principe de travail

Le projet CK sera conduit par itérations courtes.

L’objectif n’est pas de produire une version parfaite du premier coup, mais d’améliorer progressivement :

* la clarté commerciale ;
* la qualité perçue ;
* la fidélité à la doctrine CK ;
* la traduisibilité Odoo ;
* la capacité de conversion.

Principe MOA retenu :

> Nous ne perdons jamais : nous apprenons, nous capitalisons, puis nous améliorons.

---

*Brief maquette CK V1.2 — déclinaison opérationnelle note_05 · transmis Dev/maquettage 2026-06-13.*
