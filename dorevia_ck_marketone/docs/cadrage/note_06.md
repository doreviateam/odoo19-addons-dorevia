# Brief MOA — Navigation CK V2

## Acheter · Apprendre · Contribuer

| Champ     | Valeur                                                                       |
| --------- | ---------------------------------------------------------------------------- |
| Projet    | C-Kreyol / CK Marketone                                                      |
| Objet     | Refonte de la logique de navigation principale                               |
| Statut    | **Amendé MOA** — révision 2026-06-21 · prêt ticket Lot Nav-1                  |
| Type      | Cadrage produit / UX / e-commerce                                            |
| Priorité  | Haute                                                                        |
| Périmètre | Header, menu principal, entrée “Découvrir”, articulation commerce ↔ contenus |
| Retour Dev | [`note_06_retour_dev.md`](./note_06_retour_dev.md) — verdict **À AMENDER** (2026-06-21) |
| Réponse MOA | [`note_06_reponse_moa.md`](./note_06_reponse_moa.md) — arbitrages intégrés (2026-06-21) |
| Ticket Dev | [`../design/TICKET_DEV_LOT_NAV1_NAVIGATION_CK_V2.md`](../design/TICKET_DEV_LOT_NAV1_NAVIGATION_CK_V2.md) — Lot Nav-1 |

---

## 1. Contexte

CK ne doit pas être conçu uniquement comme une boutique e-commerce classique, ni comme un simple site éditorial autour de la culture créole.

La plateforme porte une ambition plus large : vendre des produits du monde créole, transmettre des savoirs autour de ces produits, et permettre progressivement aux utilisateurs de contribuer à cette transmission.

La navigation principale doit donc rester efficace pour l’achat, tout en préparant la dimension culturelle, éditoriale et communautaire de CK.

Le sujet n’est pas seulement de “faire un menu”. Il s’agit de clarifier l’architecture de navigation autour de trois intentions utilisateur :

> Acheter.
> Apprendre.
> Contribuer.

---

## 2. Doctrine produit validée

CK repose sur trois intentions utilisateur principales :

> Acheter les produits du monde créole.
> Apprendre sur les produits, les usages, les cultures et les territoires.
> Contribuer aux savoirs, recettes, récits et pratiques autour de ces produits.

Cette doctrine doit guider l’organisation du header, du menu principal, des futures pages éditoriales et des futurs espaces communautaires.

CK doit rester une boutique efficace, mais ne doit pas devenir une boutique froide. La dimension commerciale doit financer et soutenir une plateforme plus large, capable de créer de la connaissance, de l’attachement et de la contribution autour des produits créoles.

---

## 3. Clarification “Découvrir” vs “Apprendre”

Le terme **Apprendre** désigne l’intention utilisateur dans la doctrine CK.

Le terme **Découvrir** désigne le libellé de navigation retenu dans le menu principal.

Cette distinction est volontaire :

* **Apprendre** structure la vision produit ;
* **Découvrir** est plus naturel, plus souple et plus engageant en interface utilisateur.

La MOE ne doit donc pas remplacer automatiquement **Découvrir** par **Apprendre** dans le header ou dans les maquettes, sauf arbitrage MOA explicite.

Doctrine à retenir :

> Acheter est porté par les catégories commerce.
> Apprendre est porté en navigation par l’entrée Découvrir.
> Contribuer est préparé progressivement dans l’espace Découvrir.

---

## 4. Décision de navigation cible

Le menu principal CK doit rester prioritairement marchand.

Menu cible :

> Tous nos produits · Épicerie · Boissons · Soin · Artisanat · Découvrir

Les entrées **Tous nos produits**, **Épicerie**, **Boissons**, **Soin** et **Artisanat** constituent les portes d’entrée e-commerce principales.

L’entrée **Découvrir** porte les dimensions d’apprentissage, d’inspiration, de transmission et de contribution.

Cette organisation permet de séparer clairement deux parcours :

* le parcours d’achat ;
* le parcours d’attachement.

Cette séparation ne signifie pas que la dimension culturelle est secondaire en valeur. Elle signifie que le header doit rester lisible, efficace et orienté utilisateur.

### Pivot assumé depuis le header V1.2

Le header actuellement livré en Phase 1 :

> Boutique · Découvrir · Professionnels

reste la **structure de phase initiale**. La Navigation CK V2 constitue un **pivot maîtrisé**, non un simple renommage : l’écart avec le header livré est volontaire et documenté (voir [`note_06_reponse_moa.md`](./note_06_reponse_moa.md) §3).

---

## 4 bis. Correspondance catalogue BO (MOE)

Taxonomie racine **validée MOA** : Épicerie · Boissons · Soin · Artisanat.

Tableau opérationnel à compléter côté BO Odoo avant et pendant le Lot Nav-1 :

| Entrée menu | Catégorie Odoo cible | URL / slug | Statut | Produit publié minimum |
| --- | --- | --- | --- | --- |
| Tous nos produits | Catalogue complet | `/shop` | Existant / à confirmer | Oui |
| Épicerie | Catégorie racine Épicerie | À confirmer | À confirmer / créer si besoin | Oui |
| Boissons | Catégorie racine Boissons | À confirmer | À confirmer / créer si besoin | Oui |
| Soin | Catégorie racine Soin | À confirmer | À confirmer / créer si besoin | Oui |
| Artisanat | Catégorie racine Artisanat | À confirmer | À confirmer / créer si besoin | Oui |

**Règle de visibilité (validée MOA)** :

> Un lien ne doit apparaître en navigation que si la cible existe, est publiée et ne génère pas de 404.

Si une cible n’est pas prête, l’entrée est masquée ou différée — sauf décision MOA explicite de publier une page teaser.

---

## 4 ter. Entrées transverses (hors menu principal)

Les éléments suivants restent dans le header mais **ne figurent pas** dans le menu principal cible :

* recherche ;
* compte / connexion ;
* panier ;
* logo → accueil `/`.

**Professionnels** : n’est plus une entrée top-level. Le parcours `/professionnels` est relocalisé sous **Découvrir** (voir §6).

---

## 5. Rôle des entrées commerce

### Tous nos produits

Accès direct au catalogue complet.

Objectif : permettre à l’utilisateur d’entrer immédiatement dans l’offre commerciale, sans devoir comprendre l’arborescence complète.

### Épicerie

Catégorie racine pour les produits alimentaires secs ou d’épicerie :

* biscuits ;
* confitures ;
* galettes ;
* condiments ;
* épices ;
* farines ;
* préparations ;
* produits salés ou sucrés d’épicerie.

### Boissons

Catégorie racine pour les boissons créoles non alcoolisées :

* jus ;
* nectars ;
* sirops ;
* cafés ;
* thés ;
* infusions ;
* boissons découverte.

Les boissons alcoolisées ne sont pas intégrées dans le périmètre V1, sauf arbitrage métier, légal et logistique spécifique.

### Soin

Catégorie racine pour les produits liés au corps, au bien-être et à l’usage cosmétique :

* savons ;
* huiles ;
* soins du corps ;
* senteurs ;
* produits naturels ou artisanaux de soin.

Le libellé court **Soin** est retenu pour garder un menu compact. Une évolution vers **Soin & Beauté** reste possible si la MOA juge ce libellé plus lisible côté client final.

### Artisanat

Catégorie racine pour les produits non alimentaires issus de savoir-faire, d’objets ou d’arts de vivre :

* objets ;
* textile ;
* décoration ;
* créations artisanales ;
* maison ;
* culture matérielle.

---

## 6. Rôle de l’entrée “Découvrir”

L’entrée **Découvrir** ne doit pas être comprise comme un simple blog.

Elle doit devenir la porte d’entrée vers les dimensions **Apprendre**, **Contribuer** et l’**écosystème professionnel** (parcours Professionnels).

**Rôle clarifié (MOA)** : Découvrir ne porte **plus** la logique « Acheter par univers » lorsque les univers marchands sont au top-level. Le mega-menu Découvrir **ne doit pas dupliquer** les entrées commerce principales.

Sous-menu cible :

> Producteurs & territoires
> Histoires de produits
> Recettes & usages
> Le blog CK
> Professionnels
> Communauté
> Contribuer

Cet ordre suit une logique de maturité et de dépendance technique.

Les contenus **Producteurs & territoires** et **Histoires de produits** peuvent être alimentés directement par CK dès le lancement, sans dépendre de contributions utilisateurs.

Les contenus **Recettes & usages** peuvent être enrichis progressivement par CK, puis à terme par les utilisateurs.

**Professionnels** : relocalisation du parcours B2B existant (`/professionnels`) — non suppression.

Les espaces **Communauté** et **Contribuer** portent l’ambition participative, mais peuvent être activés par étapes.

---

## 7. Description des sous-entrées “Découvrir”

### Producteurs & territoires

Espace destiné à présenter les producteurs, artisans, maisons, territoires et zones créolophones liés aux produits proposés.

Objectif : renforcer la confiance, l’origine, la transparence et la relation entre le produit et son contexte réel.

### Histoires de produits

Espace destiné à raconter l’origine, les usages, les traditions ou les récits associés à certains produits.

Objectif : donner de la profondeur aux produits, au-delà de leur simple fiche commerciale.

### Recettes & usages

Espace destiné à expliquer comment utiliser les produits, les cuisiner, les associer ou les intégrer dans des pratiques du quotidien.

Objectif : aider l’utilisateur à passer de l’achat à l’usage, puis à la satisfaction.

### Le blog CK

Espace éditorial porté par CK :

* articles ;
* actualités ;
* sélections ;
* conseils ;
* dossiers ;
* contenus de marque.

Objectif : faire vivre l’univers CK, soutenir le référencement naturel et nourrir la relation avec les utilisateurs.

### Professionnels

Espace destiné au parcours B2B et à l’écosystème professionnel CK :

* accès gateway professionnels ;
* qualification et orientation pro ;
* relation avec les acteurs de la filière.

Objectif : conserver le parcours `/professionnels` sans concurrencer les catégories marchandes dans le menu principal.

**Arbitrage MOA** : entrée retirée du top-level · relocalisée sous Découvrir.

### Communauté

Espace destiné à préparer la logique communautaire :

* échanges ;
* discussions ;
* partages ;
* appartenance ;
* liens entre utilisateurs.

Objectif : faire de CK une plateforme vivante et pas seulement une boutique transactionnelle.

### Contribuer

Espace destiné à préparer la contribution utilisateur :

* proposer une recette ;
* partager un conseil d’usage ;
* raconter une tradition familiale ;
* recommander un produit ou un producteur ;
* enrichir les savoirs autour d’un produit.

Objectif : permettre progressivement aux utilisateurs de devenir créateurs de contenu dans CK.

---

## 8. Principe UX

La navigation CK doit articuler deux parcours complémentaires.

### Parcours d’achat

L’utilisateur veut trouver un produit, comprendre l’offre, ajouter au panier et acheter.

Ce parcours est porté par :

> Tous nos produits · Épicerie · Boissons · Soin · Artisanat

Ce parcours doit être direct, lisible et marchand.

### Parcours d’attachement

L’utilisateur veut comprendre, apprendre, s’inspirer, transmettre ou participer.

Ce parcours est porté par :

> Découvrir

Ce parcours doit créer de la confiance, de la préférence et de l’attachement à CK.

### Cohérence Home S4 (hors Lot Nav-1)

La section Home **« Acheter par univers »** (S4) reste structurée sur **trois cards** en V1.2.x. Un écart temporaire avec le header Navigation V2 (cinq entrées commerce + Boissons) est accepté MOA.

> Le **Lot Nav-1 ne modifie pas la Home S4**. Toute reprise S4 fera l’objet d’un arbitrage ou ticket distinct.

La cohérence header ↔ Home S4 ↔ catégories BO doit néanmoins être **contrôlée** en recette.

---

## 9. Positionnement stratégique

CK doit être présenté comme une plateforme marchande et communautaire dédiée aux produits du monde créole.

Formulation cible :

> CK permet d’acheter les produits du monde créole, d’apprendre à les connaître et à les utiliser, et de contribuer aux savoirs, recettes et récits qui les entourent.

Version courte :

> Acheter · Apprendre · Contribuer autour des produits du monde créole.

Cette formulation doit guider la navigation, les contenus, les fiches produit et les futures évolutions communautaires.

---

## 10. Articulation commerce ↔ culture

La dimension culturelle ne doit pas être isolée dans un espace séparé du commerce.

Même si le premier lot ne prévoit pas de refonte complète des fiches produit, les fiches produit peuvent intégrer ou préparer des liens simples vers des contenus éditoriaux associés lorsque ces contenus existent ou sont créés sous forme de pages CMS.

Exemples :

* lien vers une histoire de produit ;
* lien vers une recette associée ;
* lien vers un producteur ;
* lien vers un territoire ;
* lien vers un conseil d’usage.

Cette possibilité permet de commencer à relier le parcours marchand au parcours culturel dès la Phase 1, sans engager de développement lourd ni de refonte fonctionnelle de la fiche produit.

Principe cible :

> Le produit se vend dans le catalogue, mais il peut aussi ouvrir vers une histoire, un usage ou une contribution.

---

## 11. Principe de phasage

### Lot Nav-1 — Phase 1 · Navigation marchande claire

**Périmètre strict** — navigation uniquement :

* menu principal cible :

  > Tous nos produits · Épicerie · Boissons · Soin · Artisanat · Découvrir

* relocalisation **Professionnels** sous Découvrir ;
* synchronisation `website.menu` + mega Découvrir (liens réels, règle de visibilité §4 bis) ;
* vérification / alignement catégories BO ;
* adaptation tests header ;
* recette desktop + **mobile 390 px** ;
* non-régression recherche, compte, panier, boutique, accès professionnels.

**Hors périmètre Lot Nav-1** : refonte Home S4 · refonte fiche produit · forum · contribution utilisateur · modération · compte contributeur · marketplace · panier / checkout.

Objectif : rendre le catalogue immédiatement lisible et orienté vente, sans mélanger avec la reprise Home.

### Phase 2 — Structuration de “Découvrir”

Créer ou préparer les pages permettant d’apprendre :

* producteurs & territoires ;
* histoires de produits ;
* recettes & usages ;
* blog CK.

Objectif : renforcer la confiance, l’usage et la profondeur culturelle.

### Phase 3 — Contribution utilisateur

Ajouter progressivement les mécanismes permettant aux utilisateurs de contribuer :

* formulaire de proposition de recette ;
* contribution d’usage ;
* témoignage ;
* discussion communautaire ;
* modération.

Objectif : transformer CK en plateforme vivante, pas seulement en boutique.

---

## 12. Hors périmètre du premier lot (Lot Nav-1)

Le Lot Nav-1 ne doit pas embarquer :

* refonte Home S4 ;
* développement d’un forum complet ;
* système complet de publication utilisateur ;
* modération avancée ;
* compte contributeur ;
* marketplace multi-vendeurs ;
* refonte complète du shop ;
* refonte complète des fiches produit ;
* modification du panier ou du checkout ;
* nouveau modèle métier complexe ;
* automatisation avancée des contenus liés aux produits.

Le Lot Nav-1 doit uniquement poser une architecture de navigation cohérente, évolutive et compatible avec la stratégie CK.

Point de précision (hors Lot Nav-1, phases ultérieures) :

> Les fiches produit peuvent intégrer ou préparer des liens simples vers des contenus éditoriaux associés — recettes, histoires de produits, producteurs, territoires — lorsque ces contenus existent ou sont créés sous forme de pages CMS.

---

## 13. Principes de mise en œuvre attendus

La mise en œuvre devra respecter les principes déjà retenus pour CK :

* Odoo 19 CE comme socle ;
* approche snippets first ;
* pas de surcouche front autonome ;
* pas de HTML maquette injecté ;
* pas de refonte complète non demandée ;
* respect de l’identité visuelle CK actuelle ;
* compatibilité avec le Website Builder autant que possible ;
* progression par lots courts et recettables.

La navigation doit rester simple en V1. Les sous-menus pourront être enrichis progressivement, lorsque le catalogue et les contenus le justifieront.

---

## 14. Critères de validation MOA

Critères validés MOA (révision 2026-06-21) :

1. le triptyque stratégique : **Acheter · Apprendre · Contribuer** ;
2. le menu principal cible :
   **Tous nos produits · Épicerie · Boissons · Soin · Artisanat · Découvrir** ;
3. la distinction **Apprendre** (intention produit) / **Découvrir** (libellé navigation) ;
4. le pivot de navigation depuis le header V1.2 est **explicitement assumé** ;
5. **Professionnels** relocalisé sous Découvrir (plus de top-level) ;
6. taxonomie racine **Épicerie / Boissons / Soin / Artisanat** validée ;
7. chaque entrée navigation pointe vers une cible **existante et publiée** (règle §4 bis) ;
8. Découvrir **ne duplique pas** les entrées commerce principales ;
9. ordre cible du sous-menu Découvrir :

   * Producteurs & territoires ;
   * Histoires de produits ;
   * Recettes & usages ;
   * Le blog CK ;
   * Professionnels ;
   * Communauté ;
   * Contribuer ;

10. le **Lot Nav-1 ne modifie pas** la Home S4 ;
11. cohérence header ↔ catégories BO ↔ pages publiées vérifiée en recette ;
12. recette **mobile 390 px** obligatoire ;
13. tests header mis à jour en cohérence Navigation V2 ;
14. phasage progressif en lots · contribution utilisateur hors Lot Nav-1 ;
15. liens simples fiche produit ↔ contenus éditoriaux possibles hors refonte fiche (phases ultérieures).

---

## 15. Verdict MOA

> **Verdict : AMENDÉ MOA — PRÊT TICKET DEV LOT NAV-1**
> Commentaire MOA : Retour Dev accepté — arbitrages intégrés · voir [`note_06_reponse_moa.md`](./note_06_reponse_moa.md)
> Date : 2026-06-21
> Validateur : MOA
