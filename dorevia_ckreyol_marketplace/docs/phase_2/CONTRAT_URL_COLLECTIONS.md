# Contrat d’URL de la porte **Collections** — trame, arbitrages URL et **copies v1**

| Champ | Valeur |
|--------|--------|
| **Statut** | **Prête implémentation (v1) — zéro résidu documentaire** (MOA 2026-04-22) — **URL**, **S1**, **repli combinaison (A)**, **message 302** (flash / session), **copies minimales** **et** **priorité `ckr_mode`** (**pack > promo > origin > collection**, **§13** + [SPEC_IMPL §5.1](SPEC_IMPL_COLLECTIONS.md#51-constantes-alignement-packs--promos--origines--priorité-ckr_mode-figée-moa-2026-04-22)) : **tous actés**. **Spec** : **[SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md)**. **Recette** : **[PV_RECETTE_COLLECTIONS_V1.md](PV_RECETTE_COLLECTIONS_V1.md)** (**RC-01…RC-14**, tests **`dorevia_ckr_collections`**). **Base métier** : [CADRAGE_FONCTIONNEL_COLLECTIONS.md](CADRAGE_FONCTIONNEL_COLLECTIONS.md). |
| **Date** | 2026-04-22 (création du document à partir de la trame MOA). |
| **Périmètre** | **Comportement visiteur**, **contrat d’URL**, **résolution**, **replis**, **signal éditorial**, **canonical**, **compatibilité filtrage boutique** — en cohérence avec [ADR-CKR-007](../ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007) (convergence `/shop`) et [SPEC_SHOP_PORTES §4.2](SPEC_SHOP_PORTES.md#42-collections). |
| **Hors périmètre** | Redéfinition de l’**intention métier** (objet marketing, vue générale `/collections`, OU, repli 302, slug unique, navigation visible — figés dans le **cadrage**). |

Ce document **traduit** le cadrage en **URL**, **règles de résolution**, **replis**, **signal éditorial**, **canonical** et **compatibilité avec le filtrage boutique**. La **spec d’implémentation** détaillera le modèle de données, les droits, les hooks et les tests ; le **[PV de recette V1](PV_RECETTE_COLLECTIONS_V1.md)** enchaîne sur la **validation** fonctionnelle et la **preuve automatisée** (tag **`dorevia_ckr_collections`**).

**Suite** : implémentation module selon **[SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md)** et recette **[PV_RECETTE_COLLECTIONS_V1.md](PV_RECETTE_COLLECTIONS_V1.md)** — **zéro résidu documentaire**.

---

## 1. Objet du document

Ce document formalise le **comportement visiteur** et le **contrat d’URL** de la porte **Collections**, en cohérence avec :

* [CADRAGE_FONCTIONNEL_COLLECTIONS.md](CADRAGE_FONCTIONNEL_COLLECTIONS.md) ;
* la doctrine Explorer ([ADR-CKR-007](../ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007), [ADR-CKR-008](../ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008)) ;
* la **convergence cible** vers **`/shop`**.

Il **ne redéfinit pas** l’intention métier ; il la **traduit** en :

* **URL** ;
* **règles de résolution** ;
* **replis** ;
* **signal éditorial** ;
* **canonical** ;
* **compatibilité avec le filtrage boutique**.

---

## 2. Rappel des arbitrages métier déjà actés

Synthèse renvoyant au **cadrage** (détail et formulations dans [CADRAGE_FONCTIONNEL_COLLECTIONS.md](CADRAGE_FONCTIONNEL_COLLECTIONS.md)) :

* **Collection** = objet **marketing / thématique** de mise en avant (non réduit à un simple filtre ou taxonomie seule).
* **`/collections`** = **vue générale** ; produits ayant **au moins une** collection **active** et **visible** ; **exclusion** des produits hors collections ; titre **« Collections »**.
* **Collection précise** = liste restreinte à cette collection ; **titre dynamique** = titre affiché de la collection.
* **Multi-affectation** : un produit peut appartenir à **plusieurs** collections.
* **Filtrage boutique** sur **1 à n** collections = logique **OU**.
* **Collection indisponible** (slug inconnu, inactive, hors période, non résolvable) = **HTTP 302** vers **`/collections`** + **message léger** de contexte (formulation de travail actée au cadrage).
* **Slug** : auto-proposé depuis le titre affiché, **éditable**, **unique**, **stable** ; pas d’ambiguïté URL.
* Double rôle : **navigation visible** (y compris sous-menu horizontal) **et** **filtre** boutique.
* **Propriétés minimales stables** pour la navigation : titre affiché, slug unique, ordre d’affichage, Active, période de validité.

---

## 3. Question centrale du contrat d’URL

Le document doit **trancher** :

1. **Quelle est l’URL visible d’entrée** de la porte Collections (carte Explorer, liens marketing) ?
2. **Comment désigne-t-on une collection précise** dans l’URL ?
3. **Comment transporte-t-on 1 à n collections** en **URL publique** (chemins **§4** / **§7**) et, en interne, dans la logique boutique (spec d’impl.) ?
4. **Comment se comporte le repli** (cible exacte, conservation ou non de paramètres, message) ?
5. **Quel canonical** pour la vue générale, la vue collection précise, et le **multi-slugs** (dédupe + ordre stable) ?
6. ~~**Quelle syntaxe exacte** pour la **combinaison**~~ → **actée** : **S1** **`/collections/union/<slug-1>/…/<slug-n>`** (**§4.6**, **§7**). **Points résiduels** : copies, message **302**, raffinement des **replis** combinaison en spec.

---

## 4. Formes d’URL et convergence `/shop`

### 4.1 Entrée générale — **acté**

**URL publique de référence — vue générale** :

* **`/collections`**

**Comportement (cadrage)** :

* **`/collections`** = **vue générale Collections** ;
* affichage des produits appartenant à **au moins une** collection **active** et **visible** ;
* **titre affiché** : **Collections**.

### 4.2 Collection précise — **acté**

**URL publique de référence — une collection** :

* **`/collections/<slug>`**  
  où **`<slug>`** est le **slug unique** de la collection (identifiant stable — cadrage).

**Comportement attendu** : **§6** (liste restreinte, titre dynamique, états vides).

### 4.3 Décision MOA — **pas de référence publique « technique » sur `/shop` pour Collections**

**Acté** : la **forme publique de référence** pour la porte **Collections** **n’est pas** le schéma :

* **`/shop?ckr_mode=collection&ckr_collection=<slug>`**  
  (ni **`/collections` → 301** vers cette forme comme **substitut** de l’URL **affichée**, **partagée** ou **canonique visiteur** pour cette porte).

**Motifs** : **lisibilité**, **partage**, **noblesse** des chemins ; la collection est un **véritable objet de navigation public**.

**Règle de travail transverse** (priorisation documentaire, au-delà de cette seule porte) :

> Lorsqu’un objet est un **véritable objet de navigation public**, l’**URL exposée** au visiteur doit privilégier une **URL publique lisible** (chemin dédié), et **non** une **query string technique** sur **`/shop`** comme **forme de référence par défaut**.

**Extension (2026-04-22)** — **combinaisons** :

> Lorsque le visiteur construit une **combinaison** de collections (**filtrage multi**, logique **OU**), cette lecture fait partie de la **navigation publique partageable** et doit disposer d’une **URL publique noble dédiée**, **distincte** de la simple query **`/shop?ckr_mode=collection&ckr_collection=…&ckr_collection=…`**. La **syntaxe** retenue est **S1** (**§4.6**, **§7**).

**Cohérence [ADR-CKR-007](../ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007)** : la **convergence fonctionnelle** vers le **catalogue achetable** et le **moteur `/shop`** reste la cible ; l’implémentation peut **s’appuyer en interne** sur la logique boutique (domaines produits, gabarit, panier, etc.) **sans** imposer cette forme dans la **barre d’adresse** ni dans les **liens éditoriaux visibles**. Le détail (contrôleur, rendu, éventuel transfert interne) est porté par **`SPEC_IMPL_COLLECTIONS.md`**.

### 4.4 Voie non retenue comme **face publique** (référence historique)

L’**option Hybride H1** du type **`/collections` → 301 → `/shop?ckr_mode=collection`** + filtres en query sur **`/shop`** était une **piste de départ** alignée sur d’autres portes ; elle est **écartée** pour **Collections** au titre du **§4.3**. Les autres portes (**Kits**, **Promotions**, **Origines**, etc.) **ne sont pas réouvertes** par cette décision.

### 4.5 Paramètres internes (spec d’impl.)

Les noms **`ckr_mode`**, **`ckr_collection`**, etc. peuvent rester des **outils d’implémentation** (options de recherche, hooks, tests) **sans** constituer l’**URL publique de référence** pour cette porte — **y compris** pour une **combinaison** de collections (**§4.6**). Toute exposition résiduelle en query sera **justifiée** en spec si elle existe.

### 4.6 Combinaison de collections (**n ≥ 2**) — **principe acté** ; syntaxe **S1 actée**

**Acté (MOA)** : au-delà de la **vue générale** (**§4.1**) et de la **collection précise** (**§4.2**), une **combinaison** de collections (filtre **multi**, logique **OU** déjà actée au cadrage) dispose d’une **URL publique noble dédiée**, **lisible** et **partageable**, au même titre que les deux premiers niveaux.

**Exclu** comme **forme publique de référence** pour cette combinaison :

* **`/shop?ckr_mode=collection&ckr_collection=<slug1>&ckr_collection=<slug2>&…`** (query **technique** sur **`/shop`**, y compris avec **`ckr_collection`** répété).

**Syntaxe publique retenue — piste S1 (MOA, prioritaire sauf contre-argument technique / UX documenté en spec)** :

* **`/collections/union/<slug-1>/<slug-2>/…/<slug-n>`** avec **n ≥ 2** ;
* le segment littéral **`union`** désigne explicitement une **lecture « union »** (OU) de **plusieurs** collections ; il **n’est pas** un slug de collection.

**Réservation produit** : la valeur **`union`** est **interdite** comme **slug** de collection (validation back-office + contrôle à l’import), afin d’**éviter toute collision** avec la route **`/collections/<slug>`** du **§4.2**.

**Ordre canonique** : pour une même combinaison, l’URL **de référence** (partage, **canonical** — **§9**) utilise les slugs **distincts**, **dédupliqués**, puis triés par **ordre lexicographique strict** (code points du segment path, sens normal du tri URL).

**Normalisation** : si l’URL reçue contient des **doublons** ou un **ordre non canonique**, le serveur renvoie **HTTP 301** vers l’URL **S1 canonique** correspondante (même principe que pour les variantes d’URL à éviter pour le SEO). *Cas limite* : après **déduplication**, il ne reste qu’**un** slug → **301** vers **`/collections/<slug>`** (**§4.2**).

**Encodage** : chaque **`<slug-i>`** est le **slug métier** tel que défini au cadrage ; les caractères réservés au path sont **pourcent-encodés** selon les usages web (détail **RFC** / Odoo en spec d’impl.).

**Replis** (rappel — détail en **§7** / spec) : chemin **`union`** **incomplet** ou **invalide** (ex. **< 2** slugs valides après normalisation) ; **au moins un** slug **non résolvable** ou **hors périmètre** (inactif, hors période, inconnu) — **§7**.

---

## 5. Vue générale Collections

### Cas

Le visiteur arrive sur la **URL publique de référence** :

* **`/collections`** (**§4.1**).

### Comportement attendu (cadrage)

* produits ayant **au moins une** collection active et visible ;
* **exclusion** des produits hors collections ;
* titre : **Collections** ;
* **phrase de contexte** (bandeau) : **figée** (MOA 2026-04-22 — identique [SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md) **§8**) :

> Découvrez les collections actuellement disponibles.

---

## 6. Vue collection précise

### Cas

Le visiteur arrive sur la **URL publique de référence** :

* **`/collections/<slug>`** (**§4.2**).

### Comportement attendu (cadrage)

* liste **restreinte** aux produits de **cette** collection ;
* **titre dynamique** = **titre affiché** de la collection ;
* **phrase de contexte** si disponible (champ enrichi — **V1.1+** si le champ est introduit) ;
* **sans** phrase métier dédiée en base (cas V1) : bandeau avec la **copy minimale figée** (MOA 2026-04-22 — [SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md) **§8**) :

> Parcourez les produits rattachés à cette collection.

* si **0 produit** mais collection **valide** (active, dans période, résolvable) : **état vide dédié** — *à distinguer* du repli « collection indisponible» (voir **§12**).

### Distinction repli vs état vide

* **A.** collection **valide** mais **sans produit** visible → état vide **sur place** (pas 302 vers indisponible) — **copy** **§12 A** ;
* **B.** collection **non disponible** → **302** vers `/collections` + message (**§8**).

---

## 7. Filtrage boutique sur 1 à n collections

### Arbitrage déjà acté (cadrage)

* filtrage **multi-collections** ;
* logique **OU**.

### Comportement (cadrage)

* afficher les produits appartenant à **au moins une** des collections sélectionnées (**OU**).

### URL publique pour **n = 1** — rappel

* **`/collections/<slug>`** (**§4.2**).

### URL publique pour **n ≥ 2** — **syntaxe S1 actée** (**§4.6**)

**Forme de référence** :

* **`/collections/union/<slug-1>/<slug-2>/…/<slug-n>`** , **n ≥ 2** ;
* **OU** sur l’ensemble des collections désignées (**cadrage**).

**Titre** de la lecture union (**figé** MOA 2026-04-22) : **Collections sélectionnées** — avec sous-texte / bandeau minimal dans [SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md) **§8**.

**Pistes S2 / S3** (multi-segments ambigus, hash opaque, etc.) : **non retenues** pour la **V1** ; réouverture **uniquement** sur **contre-argument technique ou UX documenté** (rebasculer alors en atelier).

**Hors périmètre de référence publique** : combinaison uniquement via **query** sur **`/collections`** ou sur **`/shop`** — **non retenu** (**§4.3**, **§4.6**).

### Résolution et replis (combinaison)

* **`/collections/union`** sans slug suivant, ou **`/collections/union/<un_seul_segment>`** alors que la lecture **union** exige **au moins deux** slugs **distincts** valides : **HTTP 302** vers **`/collections`** + message de contexte (**§8**), *sauf* si la normalisation peut **301** vers **`/collections/<slug>`** (exactement **un** slug valide après **déduplication** — **§4.6**).
* **Au moins un** slug de la liste **inconnu**, **inactif**, **hors période** ou **non réservable** au sens navigation publique : **HTTP 302** vers **`/collections`** + message (**§8**), aligné sur l’esprit « collection indisponible ». **V1** : **option A uniquement** — **pas** de recomposition partielle ni de **301** vers une union résiduelle ([SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md) **§6**).

**Longueur d’URL** : limite pratique (**n** élevé) — **garde-fou** UX / serveur en spec (soft cap, message, etc.) si besoin.

---

## 8. Repli — collection non disponible

### Cas concernés

* slug **inconnu** ;
* collection **inactive** ;
* collection **hors période** de validité ;
* collection **non résolvable**.

### Comportement acté (cadrage)

* **HTTP 302** vers **`/collections`** (vue générale — pas vers `/shop` nu sauf décision contraire documentée) ;
* **message léger** de contexte.

### Formulation de travail (cadrage)

> Nous n’avons pas retrouvé exactement la collection demandée. Voici les collections actuellement disponibles.

### Transport du message — **acté (MOA 2026-04-22)**

* **Mécanisme retenu** : **flash / session** (ou équivalent **one-shot**), **sans** paramètre visible en **query** (pas de **`?ckr_notice=`**). Détail d’implémentation : [SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md) **§7**.

---

## 9. Canonical

### Vue générale — **aligné sur le §4.3**

* **Canonical visiteur** : **`/collections`** (URL absolue du site, **sans** substituer une query **`/shop?ckr_mode=collection`** comme référence).

### Vue collection précise — **aligné sur le §4.3**

* **Canonical visiteur** : **`/collections/<slug>`** pour la collection demandée ;
* **slug unique** → une collection.

### Combinaison **n ≥ 2** — **S1** (**§4.6**, **§7**)

* **Canonical visiteur** :  
  **`/collections/union/<slug-a>/<slug-b>/…`** où les **`<slug-*>`** sont les slugs **distincts**, **triés par ordre lexicographique strict** (forme **unique** pour une combinaison donnée).
* **Doublons** ou **ordre non canonique** dans le chemin : **HTTP 301** vers cette **URL canonique** ; si **un seul** slug subsiste après **déduplication** : **301** vers **`/collections/<slug>`**.
* Le lien **`rel="canonical"`** pointe vers cette **même** URL canonique S1 (pas de variante **`/shop?…`**).

---

## 10. Navigation visible

Le contrat doit **intégrer** (cadrage + §7.1 du cadrage) que les collections alimentent notamment :

* la **vue générale** `/collections` ;
* des **liens visibles** dans la boutique ;
* la **fiche produit** (**§11**) ;
* un **futur sous-menu horizontal**.

Donc :

* seules les collections **actives** et **visibles** (règle §2 cadrage) sont **proposées** ;
* l’**ordre d’affichage** est respecté ;
* la résolution reste **stable** par **slug unique**.

---

## 11. Fiche produit

### Attendu (cadrage + cohérence portes)

* affichage **simple** des collections du produit ;
* **liens** vers la **lecture** « collection précise » correspondante ;
* cohérence avec la **navigation** Collections.

### Cible des liens — **acté**

* **`/collections/<slug>`** — cohérent avec **§4.2** et la **navigation visible** (**§10**).

---

## 12. État vide — deux cas à distinguer

### A. Collection valide mais sans produit

La collection **existe**, est **active**, **dans** sa période, mais **aucun** produit n’est (ou n’est plus) rattaché / visible.

* **état vide dédié** sur la **lecture** collection (pas confondre avec le repli **B**) ;
* **copy minimale figée** (MOA 2026-04-22 — [SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md) **§8**) :
  * **Corps** : *Aucun produit n’est affiché pour cette collection pour le moment.*
  * **Lien** vers **`/collections`** : libellé **« Retour aux collections »**.

### B. Collection non disponible

Référence **non valable** au sens **§8**.

* **302** vers **`/collections`** ;
* message de contexte (**§8**).

---

## 13. Décisions à prendre dans ce document — checklist

* [x] **Famille d’URL publique de référence** : **chemins dédiés** **`/collections`** et **`/collections/<slug>`** ; **exclusion** de **`/shop?ckr_mode=collection&…`** comme référence publique par défaut (**§4.3**). ~~Hybride H1 comme face publique~~ **non retenu** pour Collections (**§4.4**).
* [x] **Forme exacte** de l’URL **collection précise** (chemin public) : **`/collections/<slug>`** (**§4.2**).
* [x] **Canonical** (vue générale + collection précise) : **auto-référence** **`/collections`** / **`/collections/<slug>`** (**§9**).
* [x] **Fiche produit** : liens vers **`/collections/<slug>`** (**§11**).
* [x] **Principe** — **combinaison** (**n ≥ 2**) : **URL publique noble dédiée** ; **exclusion** de **`/shop?ckr_mode=collection&ckr_collection=…&ckr_collection=…`** comme référence publique (**§4.6**, **§7**).
* [x] **Syntaxe S1** : **`/collections/union/<slug-1>/…/<slug-n>`** ; slug **`union`** **interdit** côté collection ; **ordre canonique** lexicographique ; **301** si variantes (**§4.6**, **§7**, **§9**).
* [x] **Canonical** + **normalisation** pour la **combinaison** : **§9** (aligné **§4.6**).
* [x] **Replis combinaison** (**V1**) : **option A** uniquement — **302** **`/collections`** + message ; **pas** de recomposition partielle (**§7**, [SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md) **§6**).
* [x] **Mécanisme** de transport du **message** après **302** : **flash / session** **one-shot** (**§8**, [SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md) **§7**).
* [x] **Copy** bandeau **vue générale** (**§5**).
* [x] **Copy** bandeau **vue collection précise** sans phrase métier dédiée en base (**§6**).
* [x] **Copy** état vide **« collection valide sans produit »** (**§12 A**).
* [x] **Titre** lecture **union** : **« Collections sélectionnées »** (**§7** + [SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md) **§8**).
* [x] **Conflit multi-`ckr_mode`** (si plusieurs modes dans une URL **interne** ou résiduelle) : **priorité déterministe figée** — **`pack`** > **`promo`** > **`origin`** > **`collection`** (collection **en dernier**, non-régression absolue ; aligné **§4.3** — `collection` **n’est pas** une URL publique de référence). Source de vérité : [SPEC_IMPL_COLLECTIONS.md §5.1](SPEC_IMPL_COLLECTIONS.md#51-constantes-alignement-packs--promos--origines--priorité-ckr_mode-figée-moa-2026-04-22) ; preuve auto : **RC-14** / `TestCkrCollectionsPVModel.test_ckr_col_rc14_effective_mode_priority`.

---

## 14. Synthèse opérationnelle (après décisions §4.3 / §4.6 / S1)

**Acté** :

* **URLs publiques nobles** : **`/collections`** ; **`/collections/<slug>`** ; **`/collections/union/<slug-1>/…/<slug-n>`** pour **n ≥ 2** (**S1** — **§4.6**, **§7**) ;
* **exclusion** des schémas **`/shop?ckr_mode=collection&…`** (y compris **multi-`ckr_collection`**) comme **référence publique** ;
* **règle de travail transverse** : navigation **partageable** → **chemins nobles** (**§4.3**, **§4.6**) ;
* **normalisation / canonical** combinaison : **tri lexicographique** des slugs **distincts**, **301** depuis variantes (**§4.6**, **§9**) ;
* **slug `union`** : **réservé**, **interdit** comme slug de collection (**§4.6**) ;
* **implémentation** : convergence **`/shop`** possible **en coulisse** (**§4.3**) ;
* **repli** unitaire ou **union** invalide : **302** **`/collections`** + message (**§8**, **§7**) ; **V1** : **pas** de variante « union résiduelle ».
* **Message** après **302** : **flash / session** **one-shot** (**§8**) ; **copies minimales** et **titre union** : **§5–§8**, **§12 A** + [SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md) **§8**.

**Suite** : implémentation selon **[SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md)** et validation **[PV_RECETTE_COLLECTIONS_V1.md](PV_RECETTE_COLLECTIONS_V1.md)** — **zéro résidu documentaire** (priorité **`ckr_mode`** figée **§13** + [SPEC_IMPL §5.1](SPEC_IMPL_COLLECTIONS.md#51-constantes-alignement-packs--promos--origines--priorité-ckr_mode-figée-moa-2026-04-22)).

---

## Historique

| Date | Événement |
|------|-----------|
| 2026-04-22 | **Création** du document à partir de la **trame MOA** : objet, rappel cadrage, questions centrales, H1 vs dédié, vues générale / précise, filtre OU, repli, canonical, navigation, fiche produit, états vides, checklist §13, recommandation §14. |
| 2026-04-22 | **Décision MOA structurante** : **formes publiques de référence** **`/collections`** et **`/collections/<slug>`** ; **exclusion** de **`/shop?ckr_mode=collection&…`** comme URL publique de référence par défaut ; **règle de travail** « navigation public → URL noble » (**§4.3**) ; réécriture **§4–§11**, **§9 canonical**, **§13–§14**. |
| 2026-04-22 | **Prolongement MOA** : la **combinaison** de collections (**n ≥ 2**) doit avoir une **URL publique noble dédiée** (même principe que vue générale / unitaire) ; **exclusion** de **`/shop?ckr_mode=collection&ckr_collection=…&…`** ; syntaxe **S1/S2/S3** en discussion (**§4.6**, **§7**) ; checklist **§13** mise à jour. |
| 2026-04-22 | **MOA** : **syntaxe S1 actée** — **`/collections/union/<slug-1>/…/<slug-n>`** ; **ordre canonique** lexicographique + **301** de normalisation ; **slug `union` interdit** ; **S2/S3** non retenus V1 ; **§4.6**, **§7**, **§9**, **§13–§14** alignés. |
| 2026-04-22 | Ouverture de **[SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md)** — trajectoire impl. v1 ; résidus **§13** (copies, **302**, replis, **`ckr_mode`**) à solder dans la spec + contrat. |
| 2026-04-22 | **MOA** : **repli union A** seul ; **message 302** flash / session ; **titre union** *Collections sélectionnées* ; **copies minimales** §5–§6, §8 union, §12 A — **§13** coché sauf **`ckr_mode`** ; statut **prête impl. v1**. |
| 2026-04-22 | **[PV_RECETTE_COLLECTIONS_V1.md](PV_RECETTE_COLLECTIONS_V1.md)** — recette **RC-01…RC-14** ; tag tests **`dorevia_ckr_collections`** ; en-tête + **Suite** (§0) alignés sur la validation pré-dev. |
| 2026-04-22 | **Dernier résidu soldé** : **priorité `ckr_mode`** figée **`pack > promo > origin > collection`** (insertion **en fin** de chaîne ; non-régression absolue). **§13** coché ; **§14 Suite** mise à jour — **feu vert code**. |
