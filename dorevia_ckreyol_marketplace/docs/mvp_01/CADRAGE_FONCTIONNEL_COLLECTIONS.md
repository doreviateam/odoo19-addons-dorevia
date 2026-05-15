# Cadrage fonctionnel — Porte **Collections** (C-Kreyol)

**Statut** : référence fonctionnelle et **arbitrages MOA** — base pour **`CONTRAT_URL_COLLECTIONS.md`** et pour **[SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md)**.  
**Module** : `dorevia_ckreyol_marketplace`  
**Alignement** : [SPEC_SHOP_PORTES.md §4.2](SPEC_SHOP_PORTES.md#42-collections), doctrine Explorer [ADR-CKR-007 / ADR-CKR-008](../direction/ARCHITECTURE_DECISION_RECORD.md).

---

## Suite documentaire prévue

| Document | Rôle |
|----------|------|
| **Ce fichier** (`CADRAGE_FONCTIONNEL_COLLECTIONS.md`) | Définition métier, visibilité, vues générale / précise, multi-affectation, OU, navigation visible (y compris sous-menus), propriétés minimales stables, slug, repli, synthèse. |
| **[CONTRAT_URL_COLLECTIONS.md](CONTRAT_URL_COLLECTIONS.md)** | **Prêt impl. v1** (2026-04-22) : **URLs nobles**, **S1**, **repli union A**, **302** + flash / session, **copies minimales** ; résidu **`ckr_mode`** (§13). **Slug `union` interdit** (§9.1). |
| **[SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md)** | Spec d’impl. **ouverte** (2026-04-22) : modèle CK, routes **`/collections`**, **S1**, intégration **`/shop`** en coulisse, canonical, copies résiduelles, tests. |
| **[PV_RECETTE_COLLECTIONS_V1.md](PV_RECETTE_COLLECTIONS_V1.md)** | **PV de recette V1** : cas **RC-01…RC-14**, exécution **`dorevia_ckr_collections`**, colonne *preuve auto* ; aligné sur [SPEC_IMPL §12](SPEC_IMPL_COLLECTIONS.md#12-tests-automatisés). |

Les points **strictement techniques** (paramètres d’URL exacts, mécanisme de message après repli, bornes jour inclus/exclus, etc.) sont laissés au **contrat d’URL** et à la **spec technique**, sous réserve des principes ci-dessous.

---

## 1. Définition fonctionnelle

Pour C-Kreyol, une **Collection** est un objet qui permet de **réunir plusieurs produits suivant un objectif marketing**.

En pratique :

* une Collection a une **visée marketing** ;
* elle repose sur un **thème** ;
* elle sert à **mettre en avant** un regroupement de produits ;
* elle **ne doit pas** être réduite à un simple filtre technique ni à un simple mécanisme de classement catalogue.

**Doctrine Explorer** : la Collection reste un **objet de navigation** au service de la boutique ; l’expérience d’achat et le **filtrage catalogue** s’articulent avec **`/shop`** (convergence cible [ADR-CKR-007](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007)). Le **premier clic** depuis la carte **Collections** de l’accueil mène à la **vue générale** décrite au §3 ; les formes d’URL pour la **collection précise** et le **filtre multi-collection** sur la boutique sont tranchées dans **`CONTRAT_URL_COLLECTIONS.md`**.

---

## 2. Visibilité dans le temps

La logique métier retenue est la suivante :

* une Collection dispose d’une **case à cocher « Active »** ;
* si **aucune période** de validité n’est renseignée, une Collection **active** est **affichée en permanence** (sous réserve des autres règles site / documents techniques) ;
* si une **période de validité** est renseignée, une Collection **active** n’est affichée **que pendant cette période** (bornes **jour calendaire** ; inclus / exclus : à préciser dans la spec technique) ;
* si la case **Active** n’est pas cochée, la Collection **n’est pas affichée**.

**Formule de lecture** :

> Une Collection est **visible** si et seulement si elle est **Active**, **et** si sa **période de validité** est respectée **lorsqu’elle existe**.

**Période de validité (V1)** : **date de début** optionnelle, **date de fin** optionnelle ; **sans** logique horaire ni statuts supplémentaires en V1.

---

## 3. Porte Explorer — vue générale **`/collections`**

Lorsque l’utilisateur clique sur la carte **Collections** depuis la page d’accueil, il doit entrer dans la **vue générale Collections**.

Arbitrages :

* **`/collections`** correspond à la **vue générale** des Collections ;
* cette vue affiche les produits appartenant à **au moins une** collection **active** et **visible** (au sens §2) ;
* les produits **sans** appartenance à une telle collection **ne doivent pas** apparaître dans cette lecture ;
* le **titre affiché** dans ce cas reste **« Collections »**.

---

## 4. Collection précise

Lorsqu’une **collection précise** est sélectionnée :

* la liste affichée doit être **restreinte** aux produits appartenant à **cette** collection ;
* le **titre affiché** doit devenir le **titre affiché** de la collection concernée (libellé visiteur).

**Synthèse UX** :

| Contexte | Titre affiché attendu |
|----------|------------------------|
| **Vue générale** | **Collections** |
| **Vue collection précise** | **Titre dynamique** de la collection sélectionnée |

Le **véhicule d’URL** (chemin dédié, paramètres sur `/shop`, etc.) est **hors périmètre** de ce cadrage : il sera fixé dans **`CONTRAT_URL_COLLECTIONS.md`**.

---

## 5. Multi-affectation produit

Un **produit peut appartenir à plusieurs collections**.

La Collection doit donc être pensée avec une logique **Many2many** (ou équivalent) côté données — cohérente avec sa nature d’**objet marketing** de mise en avant.

---

## 6. Filtrage dans la boutique

Dans la boutique, l’utilisateur doit pouvoir filtrer sur **1 à n** collections.

La logique retenue est une logique **OU** : si plusieurs collections sont sélectionnées, la liste affichée contient les produits appartenant à **au moins une** des collections sélectionnées.

---

## 7. Collections : navigation **et** filtre

Les **Collections** doivent être présentes **à la fois** :

* comme **entrées de navigation visibles** (liens / points d’accès cliquables) ;
* et comme **filtres de boutique** dans l’expérience catalogue.

La Collection est donc pensée **simultanément** comme **objet de navigation** et comme **critère de filtrage** — sans réduire l’objet au seul filtre (cf. §1).

### 7.1 Navigation visible et sous-menus *(arbitrage complémentaire MOA)*

L’**unicité stricte du slug** (§9.1) est **particulièrement importante** car les Collections doivent pouvoir servir de base à une **navigation visible**, y compris sous forme de **sous-menu horizontal par collection** (liens stables, ordonnés, filtrés par visibilité §2).

Cela **confirme** la lecture : la Collection est un **objet de navigation à part entière**, et **pas seulement** un filtre interne au catalogue — le filtre (§6) et la navigation (cartes, listes, sous-menus) **s’appuient** sur le **même objet métier** aux propriétés stables (§9.2).

Le **`CONTRAT_URL_COLLECTIONS.md`** et la **spec d’implémentation** devront **prendre en compte** cette intention (structure d’URL compatible avec des **liens de navigation** répétés, résolution stable par **slug** unique, exclusion des collections non visibles du menu).

---

## 8. Repli — collection non disponible

Lorsqu’une **collection précise** demandée **n’est pas résolvable**, **n’est pas active**, ou se situe **hors période de validité** :

* le **repli** se fait en **HTTP 302** vers **`/collections`** (vue générale — §3) ;
* un **message léger de contexte** doit être affiché au visiteur après repli, selon les principes suivants :
  * ne pas contredire le fait que la collection demandée n’a pas été retrouvée telle quelle ;
  * éviter un ton anxiogène ou trop technique ;
  * redonner immédiatement un **choix utile** au visiteur.

**Formulation de travail recommandée** :

> Nous n’avons pas retrouvé exactement la collection demandée. Voici les collections actuellement disponibles.

Le **mécanisme de portée** du message (query signée, flash session, bannière sur la vue générale, etc.) est **à trancher** dans **`CONTRAT_URL_COLLECTIONS.md`** et en spec d’implémentation.

---

## 9. Vocabulaire de travail

| Terme | Usage |
|--------|--------|
| **Titre affiché** | Nom visible côté site (libellé visiteur) ; alimente le titre dynamique en vue collection précise (§4) et les libellés de **navigation visible** (§7.1). |
| **Slug** | Identifiant **lisible**, **stable** et **non ambigu** dans l’URL — voir §9.1 ; **unicité** requise pour la navigation (§7.1). |
| **Ordre d’affichage** | Tri des collections dans les **listes de navigation** (sous-menu horizontal, listes sur `/collections`, etc.) — valeur entière ou équivalent ; détail en spec. |
| **Active** | Case à cocher pilotant l’affichage (indépendamment des produits). |
| **Période de validité** | Date de début / date de fin optionnelles (§2). |

### 9.1 Slug — génération, édition, unicité *(arbitrage complémentaire MOA)*

Le **slug** d’une collection doit être :

* **proposé automatiquement** à partir du **titre affiché** (normalisation à détailler en spec technique : casse, accents, caractères autorisés, alignement éventuel sur les règles des autres portes CK) ;
* **modifiable manuellement** par l’éditeur ;
* et **unique** : une même valeur de slug ne doit **jamais** désigner **plusieurs** collections (identifiant non ambigu dans l’URL). Cette exigence **soutient** la **navigation visible** et les **sous-menus** par collection (§7.1) : chaque entrée de menu doit résoudre **au plus une** collection.

**Règle produit** : à la **création** ou à la **modification** d’une collection, le système doit **empêcher les doublons** de slug (contrainte ou validation bloquante). En cas de **génération automatique** entrant en **collision** avec un slug déjà existant, le comportement attendu est soit le **refus** avec message explicite, soit la **proposition d’une variante unique** (suffixe numérique ou équivalent sobre) — le choix UX exact est **à trancher** en spec d’implémentation, sous réserve que l’**unicité** soit toujours garantie.

**Slug réservé (aligné [CONTRAT_URL_COLLECTIONS.md](CONTRAT_URL_COLLECTIONS.md) §4.6)** : la valeur **`union`** n’est **pas** autorisée comme **slug** de collection (segment réservé pour la route publique de **combinaison** **`/collections/union/…`**).

### 9.2 Propriétés minimales pour la navigation visible *(arbitrage complémentaire MOA)*

Pour alimenter une **navigation visible** (y compris **sous-menu horizontal par collection**), une collection doit disposer **au minimum** de propriétés **stables** et **exploitables côté site** :

* **titre affiché** ;
* **slug unique** ;
* **ordre d’affichage** ;
* **état Active** ;
* **période de validité** (optionnelle ; cf. §2).

Les **champs enrichis** (intro, visuel, etc.) restent **ouverts** en spec / phases ultérieures sans remettre en cause ce **noyau** pour la navigation.

---

## 10. Synthèse fonctionnelle

**Collections** = **objet marketing thématique** et **objet de navigation à part entière** (§7, §7.1 — y compris **sous-menu horizontal**), permettant de **réunir plusieurs produits** selon un objectif de **mise en avant**, **visible** selon la logique **Active + période** (§2), avec **propriétés minimales stables** (§9.2), **vue générale** sous **`/collections`** (§3) et **vue collection précise** au titre dynamique (§4), **multi-affectation** produit (§5), filtre boutique en **OU** sur **1 à n** collections (§6), **repli 302** vers **`/collections`** + **message de contexte** (§8) si la collection précise n’est pas disponible, **slug** auto depuis le titre affiché, éditable, **unique** (§9.1), et **convergence** de l’expérience d’achat catalogue avec **`/shop`** au sens [ADR-CKR-007](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007) (détail d’URL : **`CONTRAT_URL_COLLECTIONS.md`**).

---

## Historique

| Date | Événement |
|------|-----------|
| 2026-04-22 | **MOA** : cadrage initial versionné (définition, Active + période, vocabulaire). |
| 2026-04-22 | **MOA** : extension du cadrage — vue générale **`/collections`**, collection précise (titre dynamique), **multi-affectation**, filtre **OU** sur la boutique, double rôle **navigation + filtre**, **repli 302** vers **`/collections`** + message de contexte, synthèse §10. Document posé comme **base explicite** pour **`CONTRAT_URL_COLLECTIONS.md`**. |
| 2026-04-22 | **MOA** : **slug** — proposition **automatique** depuis le **titre affiché**, **édition manuelle**, **unicité** stricte (jamais deux collections pour une même valeur) ; création / modification : **blocage des doublons** ou **variante unique** en cas de collision sur génération auto (détail UX en spec). |
| 2026-04-22 | **MOA** : **navigation visible** — l’unicité du slug **sert** notamment une **navigation** y compris **sous-menu horizontal par collection** ; Collection = **navigation à part entière**, pas seul filtre interne ; **propriétés minimales stables** : titre affiché, slug unique, ordre d’affichage, Active, période (§9.2, §7.1). |
| 2026-04-22 | Ouverture de **[CONTRAT_URL_COLLECTIONS.md](CONTRAT_URL_COLLECTIONS.md)** — trame de contrat d’URL (checklist §13 à trancher) ; base métier = ce cadrage. |
| 2026-04-22 | **MOA** : arbitrage **URL publique noble** porté dans le **contrat** (**`/collections`**, **`/collections/<slug>`** ; pas de query **`/shop?ckr_mode=collection…`** comme référence visiteur par défaut) + **règle de travail** transverse navigation public → chemin lisible. |
| 2026-04-22 | **MOA** : prolongement contrat — **combinaison** (**n ≥ 2**) = **URL noble dédiée** ; syntaxe **S1** **`/collections/union/…`** actée dans le contrat ; **§9.1** : **slug réservé** **`union`**. |
| 2026-04-22 | Suite documentaire : **[SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md)** ouverte (impl. v1). |
| 2026-04-22 | Suite documentaire : **[PV_RECETTE_COLLECTIONS_V1.md](PV_RECETTE_COLLECTIONS_V1.md)** — recette V1 et rattachement tests **`dorevia_ckr_collections`**. |
| 2026-04-22 | **Contrat / spec Collections** : copies + replis + message **302** verrouillés pour **v1** ; lien suite documentaire **contrat** mis à jour. |
| 2026-04-22 | **Feu vert code MOA** : **dernier résidu §13** soldé — priorité **`ckr_mode`** figée **`pack > promo > origin > collection`** ([SPEC_IMPL §5.1](SPEC_IMPL_COLLECTIONS.md#51-constantes-alignement-packs--promos--origines--priorité-ckr_mode-figée-moa-2026-04-22)) ; suite documentaire Collections = **prête impl. v1, zéro résidu**. |
