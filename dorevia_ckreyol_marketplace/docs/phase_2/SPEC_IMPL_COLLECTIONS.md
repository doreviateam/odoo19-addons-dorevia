# Spec d’implémentation — Porte **Collections** (`/collections`, `/shop` en coulisse)

| Champ | Valeur |
|--------|--------|
| **Statut** | **Prête implémentation (v1)** — URL, **S1**, **repli combinaison (A)**, **message 302** (flash / session), **copies minimales** **et** **priorité `ckr_mode`** (§5.1) **figés** (MOA 2026-04-22). **Zéro résidu documentaire** avant ouverture du code. |
| **Date** | 2026-04-22 (création) ; **verrouillages MOA** : 2026-04-22. |
| **Module** | `dorevia_ckreyol_marketplace` (Odoo **19.0** CE) |
| **Références** | [CONTRAT_URL_COLLECTIONS.md](CONTRAT_URL_COLLECTIONS.md) (§4–§14), [CADRAGE_FONCTIONNEL_COLLECTIONS.md](CADRAGE_FONCTIONNEL_COLLECTIONS.md), [PV_RECETTE_COLLECTIONS_V1.md](PV_RECETTE_COLLECTIONS_V1.md) (recette **RC-01…RC-14** ↔ tests **`dorevia_ckr_collections`**), [SPEC_SHOP_PORTES §4.2](SPEC_SHOP_PORTES.md#42-collections), [ADR-CKR-007](../ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007), [SPEC_IMPL_ORIGINES.md](SPEC_IMPL_ORIGINES.md) (patrons hooks / canonical / conflit `ckr_mode`) |

La **validation** avant livraison s’appuie sur le **[PV de recette V1](PV_RECETTE_COLLECTIONS_V1.md)** : chaque **RC-** y est rattaché à des **méthodes de test** nommées dans le PV ; le **§12** ci-dessous matérialise le **plan technique** et le **tag** **`dorevia_ckr_collections`** (principe **[PV / tests Origines](PV_RECETTE_ORIGINES_V1.md)**).

Ce document **prescrit** la mise en œuvre **v1** : **modèle CK** collection, **routes publiques nobles**, **résolution** et **normalisation** (**301**), **replis** (**302** + message **flash / session**), **repli union (A)**, **copies minimales** (**§8**), **intégration catalogue** via la logique **`/shop`** **sans** exposer **`/shop?ckr_mode=collection&…`** comme référence visiteur, **canonical**, **fiche produit**. Les arbitrages **URL** et **S1** sont **figés** dans le **contrat** — **ne pas les réouvrir** ici sans décision MOA écrite.

---

## 1. Périmètre v1

| Inclus (v1) | Exclu / plus tard |
|---------------|-------------------|
| **Vue générale** **`/collections`** ; **unitaire** **`/collections/<slug>`** ; **combinaison S1** **`/collections/union/<slug-1>/…/<slug-n>`** (**n ≥ 2**) | **S2 / S3** (contrat : non retenus V1) |
| **Normalisation** : déduplication + **tri lexicographique** + **301** vers la forme canonique ; **301** vers **`/collections/<slug>`** si un seul slug subsiste | SEO avancé hors canonical de base |
| **Slug réservé** **`union`** (validation BO + import) | Contenu riche long par collection (hors noyau §9.2 cadrage) |
| **Repli** unitaire indisponible : **302** **`/collections`** + message (**§8** contrat) | Hub CMS dédié **obligatoire** |
| **Repli combinaison** (**V1**) : **option A uniquement** — **302** **`/collections`** + message si **au moins un** slug invalide / non visible ; **pas** de recomposition partielle (**§6**) | Option **B** (301 union résiduelle) : **hors périmètre V1** |

**Référence publique** : **aucune** URL visiteur de type **`/shop?ckr_mode=collection&…`** comme **cible** de liens éditoriaux ou **canonical** (contrat **§4.3**). L’usage interne de **`ckr_mode=collection`** / options de recherche reste **possible** pour factoriser le rendu liste (**§4.5** contrat).

---

## 2. Modèle de données CK (proposition v1)

Aligné sur le **cadrage** §9.2 + contrainte **slug `union` interdit** ([CADRAGE §9.1](CADRAGE_FONCTIONNEL_COLLECTIONS.md#91-slug--génération-édition-unicité-arbitrage-complémentaire-moa)).

### 2.1 Modèle **`ckr.shop.collection`** *(nom technique proposé)*

| Champ (proposition) | Type | Rôle |
|---------------------|------|------|
| `name` | `Char` | **Titre affiché** (visiteur / BO). |
| `slug` | `Char` | **Slug unique** par site ; utilisé dans **`/collections/<slug>`** et dans **`/collections/union/…`**. |
| `sequence` | `Integer` | **Ordre d’affichage** navigation. |
| `active` | `Boolean` | **Active** (cadrage §2 / §9.2). |
| `date_start` / `date_end` | `Date` (optionnels) | **Période de validité** (cadrage §2). |
| `product_template_ids` | `Many2many` → `product.template` | Produits **rattachés** à la collection (source de vérité filtre **OU** multi-collections). |
| `website_id` | `Many2one` → `website` | Si multi-site ; v1 = même pattern que **`ckr.shop.origin`** (mono-site acceptable avec site explicite). |

**Champs enrichis** (intro, média, etc.) : **hors v1** sauf besoin minimal documenté au fil du dev.

### 2.2 Contraintes et validation *(à détailler en dev)*

* **Unicité** : `unique(website_id, slug)` (SQL) + validation **`slug != "union"`** (`@api.constrains`) — aligné [CONTRAT_URL_COLLECTIONS.md](CONTRAT_URL_COLLECTIONS.md) **§4.6**.
* **Normalisation slug** : reprendre les règles déjà utilisées sur **`ckr.shop.origin`** (minuscules, tirets, caractères autorisés) pour **cohérence** maintenance.
* **Visibilité effective** (navigation + résolution URL) : **`active`** ET **période** ET publication site — **même esprit** que les autres portes CK ; détail domaine `_is_visible()` en code.

### 2.3 Droits d’accès *(alignement Origines)*

* **`ir.model.access.csv`** : pas de lecture publique ORM ; **designer site** CRUD ; employés lecture seule ou aucun selon politique retenue sur Origines.
* Pas d’exposition JSON-RPC publique des enregistrements.

---

## 3. Routes et résolution URL

### 3.1 Vue générale

* **Route** : servir **`GET /collections`** (contrôleur dédié ou `Website` page rendue par template CK — **sans** dépendre d’une **website.page** stub transitoire une fois la route livrée ; prévoir **cleanup** data comme pour Origines/Packs si stub existant).
* **Contenu** : liste produits ayant **au moins une** collection **visible** ; titre **« Collections »** ; navigation vers collections visibles (ordre **sequence**).

### 3.2 Collection unitaire

* **`GET /collections/<slug>`** : résoudre **`ckr.shop.collection`** par `slug` + visibilité ; domaine produit = **M2M** contient cette collection ; titre = **titre affiché** ; **§12** contrat (vide dédié si 0 produit mais collection valide).

### 3.3 Combinaison S1

* **`GET /collections/union/<s1>/<s2>/…/<sn>`** , **n ≥ 2** après segments.
* **Parser** les segments ; **dédupliquer** ; **trier** (ordre lexicographique strict — **même règle** que canonical [CONTRAT_URL_COLLECTIONS.md](CONTRAT_URL_COLLECTIONS.md) **§4.6** / **§9**) ; si différent de l’URL reçue → **301** vers le chemin canonique.
* Si après déduplication **un seul** slug → **301** **`/collections/<slug>`**.
* **Domaine produit** : templates ayant **au moins une** des collections résolues (**OU**).

### 3.4 Cas incomplets / invalides

* **`/collections/union`** seul ou **`/collections/union/<un_seul>`** sans résolution **deux** collections valides : **302** **`/collections`** + message (**contrat §7** ; harmoniser libellé avec §8).
* **Au moins un** slug inconnu / non visible : **302** **`/collections`** + message (**option A** — **§6**, sans recomposition partielle).

---

## 4. Rendu liste et convergence `/shop`

**Objectif** : **une seule** expérience de **grille produit** / panier / facettes natives, en **réutilisant** le rendu **`/shop`** **en interne** (QWeb `website_sale.products`, options de recherche, pagination) **sans** réécrire l’URL navigateur en **`/shop?ckr_mode=collection&…`** pour les parcours **publics** actés.

**Pistes d’implémentation** *(à trancher au premier spike technique, sous contrainte contrat)* :

1. **Sous-requête interne** : le contrôleur **`/collections`…** prépare le même **contexte** que `shop()` (domaine, `search`, pager) et **rend** le template boutique avec un **layout** Collections (bandeau, breadcrumb) ; **ou**
2. **`request.redirect` interne** invisible : **déconseillé** si elle exposerait **`/shop`** en URL ; **à proscrire** pour les cas **publics** du contrat ; **ou**
3. **Extraction** d’helpers communs depuis `WebsiteSale` (domaine + options) appelés depuis le contrôleur Collections.

**Pagination / tri** : conserver des **liens** qui restent sous **`/collections/…`** (ré-injecter slug ou chemin union dans les query kwargs de pagination — spec technique au moment du dev).

---

## 5. Hooks `WebsiteSale` et mode interne **`collection`**

### 5.1 Constantes *(alignement Packs / Promos / Origines)* — **priorité `ckr_mode` figée (MOA 2026-04-22)**

* Introduire **`CKR_MODE_COLLECTION = "collection"`** ; étendre **`CKR_MODES_ALLOWED`** et **`CKR_MODE_TITLES`**.
* **Ordre de priorité** dans **`_ckr_effective_mode()`** (constante **`CKR_MODE_PRIORITY`** de `controllers/website_sale_ckr.py`) — **figé** :

  1. **`pack`**
  2. **`promo`**
  3. **`origin`**
  4. **`collection`** *(nouvelle valeur — **en dernier**)*

* **Motivation** :
  * **Non-régression absolue** — l’insertion en **fin** de chaîne garantit qu’aucune requête existante (**pack** / **promo** / **origin**) ne change de mode effectif quand **`collection`** est ajouté à **`CKR_MODES_ALLOWED`**.
  * **Cohérence doctrinale** — **`/shop?ckr_mode=collection…`** n’est **pas** une URL publique de référence ([CONTRAT §4.3](CONTRAT_URL_COLLECTIONS.md#43-urls-publiques-de-référence)) ; en cas de **requête malformée** cumulant plusieurs modes, il est **normal** que les portes « publiques historiques » **l’emportent**.
  * **Alignement patron Origines** — [SPEC_IMPL_ORIGINES §4 / §215](SPEC_IMPL_ORIGINES.md) (priorité **pack > promo > origin** inchangée).
* **Implémentation attendue** *(extrait non normatif)* :

```python
CKR_MODE_COLLECTION = "collection"
CKR_MODES_ALLOWED = frozenset({
    CKR_MODE_PACK, CKR_MODE_PROMO, CKR_MODE_ORIGIN, CKR_MODE_COLLECTION,
})
CKR_MODE_PRIORITY = (
    CKR_MODE_PACK, CKR_MODE_PROMO, CKR_MODE_ORIGIN, CKR_MODE_COLLECTION,
)
```

* **Non-couvert** par cette règle : l’**URL visible** (route **`/collections/…`**) reste la **cible visiteur** ; `collection` n’a **pas** d’alias **`CKR_ALIAS_MODE`** vers `/shop` (contrairement à `/kits` / `/promotions` / `/origines`).
* **Preuve auto** : **`TestCkrCollectionsPVModel.test_ckr_col_rc14_effective_mode_priority`** (**RC-14** — PV) fige l’ordre ci-dessus dans un test unitaire (sans HTTP).

### 5.2 Filtre domaine

* Lorsque le **contexte** courant est une **lecture Collections** (y compris **union**), le hook **`_get_search_options`** pose **`options['ckr_collection_only'] = True`** **et** **`options['ckr_collection_template_ids'] = [ids]`** (pré-calcul via `_ckr_collection_resolve_template_ids`).
* Le **point unique** de filtrage catalogue est **`product.template._search_get_detail`** (recette MOA 2026-04-22 — module 19.0.1.6.1) : en Odoo 19, `website_sale._shop_lookup_products` passe par **`website._search_with_fuzzy`** qui consomme `_search_get_detail`, et **n'invoque plus** `_get_shop_domain`. Le hook `_get_shop_domain` reste surchargé pour garantir la cohérence du calcul min/max prix (facettes), mais **le point d'autorité** est `_search_get_detail`.
* Sémantique **stricte** : aucun template_id résolu (vue générale sans collection visible, collection unique sans produit, union vide côté rattachements) → domaine **canoniquement vide** (`('id', '=', 0)`) ; l'état vide §12 A est alors rendu par le bandeau, **sans** fuite catalogue.

### 5.3 `ckr_collection` interne *(optionnel)*

* Si des liens **internes** (pagination) passent par **`/shop`** en phase transitoire : **whitelist** stricte ; **ne pas** documenter comme URL publique. **Cible v1** : **tout rester** sur **`/collections/…`**.

---

## 6. Replis combinaison — **acté V1 (MOA 2026-04-22)**

**Option A uniquement** : si la lecture **`/collections/union/…`** contient **au moins un** slug **inconnu**, **inactif**, **hors période** ou **non visible** au sens navigation publique → **HTTP 302** vers **`/collections`** + **message** (**§7**), **sans** tentative de **recomposition partielle** (pas de **301** vers une union résiduelle en V1).

**Option B** (retrait des slugs invalides + **301** vers union résiduelle si **≥ 2** valides) : **hors périmètre V1** ; toute réouverture = **décision MOA écrite** + mise à jour **contrat** / **spec**.

---

## 7. Message après **302** — **acté (MOA 2026-04-22)**

* **Mécanisme** : **flash / session** (ou équivalent **one-shot** côté serveur), **sans** paramètre visible en **query** (pas de **`?ckr_notice=`**).
* **Implémentation** : réutiliser le **patron** déjà en place sur les autres portes CK si existant ; sinon clé de session dédiée (ex. `ckr_collections_notice`) **consommée une fois** sur le rendu de **`/collections`** après **302**.

**Formulation** du message après repli « lecture non disponible » (alignée [CONTRAT §8](CONTRAT_URL_COLLECTIONS.md#8-repli--collection-non-disponible)) :

> Nous n’avons pas retrouvé exactement la collection demandée. Voici les collections actuellement disponibles.

*(Même esprit pour repli depuis une **union** invalide : le message s’affiche sur la **vue générale** après **302**.)*

---

## 8. Copies minimales — **figées (MOA 2026-04-22)**

Les textes ci-dessous sont la **référence d’implémentation v1** ; ils sont **reproduits** dans le [CONTRAT_URL_COLLECTIONS.md](CONTRAT_URL_COLLECTIONS.md) (**§5**, **§6**, **§7**, **§12 A**) pour **verrouillage** documentaire croisé.

| Vue | Élément | Texte figé (FR) |
|-----|---------|-------------------|
| **`/collections`** (générale) | Bandeau / phrase de contexte | **Découvrez les collections actuellement disponibles.** |
| **`/collections/<slug>`** | Bandeau **lorsqu’aucune** phrase métier dédiée n’est renseignée en base (V1 sans champ enrichi) | **Parcourez les produits rattachés à cette collection.** |
| **`/collections/union/…`** | **Titre** de la lecture (H1 ou équivalent) | **Collections sélectionnées** |
| **`/collections/union/…`** | Sous-texte / bandeau minimal (OU) | **Voici les produits appartenant à au moins une des collections combinées.** |
| **`/collections/<slug>`** — **§12 A** | État vide « collection **valide** mais **sans** produit visible » | **Corps** : *Aucun produit n’est affiché pour cette collection pour le moment.* — **Lien** vers **`/collections`** : libellé **« Retour aux collections »**. |

**Titre** des pages : **vue générale** = **« Collections »** (cadrage) ; **vue unitaire** = **titre affiché** de la collection (contrat **§6**) ; **vue union** = ligne du tableau ci-dessus.

---

## 9. Canonical (`website._get_canonical_url`)

* **`/collections`** → canonical **self**.
* **`/collections/<slug>`** → canonical **self** (slug résolu).
* **`/collections/union/…`** → canonical **self** avec segments **déjà canoniques** (sinon le **301** a lieu **avant** la réponse HTML).
* **Ne pas** émettre de canonical **`/shop?ckr_mode=collection…`** pour ces lectures (**contrat §9**).

---

## 10. Fiche produit

* Bloc **collections** du produit : liens uniquement vers **`/collections/<slug>`** ([CONTRAT §11](CONTRAT_URL_COLLECTIONS.md#11-fiche-produit)).
* Pas de lien **union** depuis la fiche sauf **besoin** explicite MOA (hors périmètre v1 par défaut).

---

## 11. Données / nettoyage

* Retrait du **stub** **`/collections`** (`website.page` + vues) si présent — fichier **`data/ckr_cleanup_collections_stub.xml`** *(nom indicatif)* + retrait du manifest, **sur le modèle** Origines/Packs.

---

## 12. Tests automatisés

**Objectif** : couvrir les **invariants** du contrat (URL, **301**/**302**, canonical, repli **A**, copies visibles) et la **non-régression** des portes déjà livrées — sur le **même modèle** que **`tests/test_ckr_shop_origins.py`** (tags **`post_install`**, **`HttpCase`** + **`TransactionCase`**, données minimales en `setUpClass`).

**Recette fonctionnelle** : le **[PV_RECETTE_COLLECTIONS_V1.md](PV_RECETTE_COLLECTIONS_V1.md)** liste les cas **RC-01…RC-14** avec colonne *Couverture auto associée* ; les noms (**`TestCkrCollectionsPVModel.*`** / **`TestCkrCollectionsPVHttp.*`**) sont **verrouillés** avec **`tests/test_ckr_shop_collections.py`** — tout renommage = **mise à jour croisée** PV + spec + code.

### 12.0 Correspondance PV (RC) ↔ plan technique (§12.2–12.4)

| PV | Intitulé (rappel) | Grille technique §12 |
|----|-------------------|----------------------|
| **RC-01** … **RC-03** | BO produit + multi-collections + profils `ckr.shop.collection` (dont **Active + période**) | **§12.2** (**T1–T3**) + méthodes PV **RC-03** (slug, unicité, menus, **`test_ckr_col_rc03_visibility_active_and_period`**) |
| **RC-04** | Vue générale `/collections` | **H1** + **§12.5** (copy bandeau générale) |
| **RC-05** | Vue unitaire + fallback | **H2** + **§12.5** |
| **RC-06** | Union S1 + OU | **H10** + **§12.5** (union) |
| **RC-07** | **301** normalisation | **H4**, **H5** |
| **RC-08** | **302** replis | **H3**, **H6**, **H7** |
| **RC-09** | Message flash, pas `?ckr_notice=` sur Location | **H3** (entête) + assertion session si implémentée |
| **RC-10** | Copies §8 smoke | **§12.5** |
| **RC-11** | État vide §12 A contrat | **H8** + **§12.5** |
| **RC-12** | Canonical | **H9** |
| **RC-13** | Fiche produit | *(test dédié QWeb `/shop/product/…` — à ajouter en **HttpCase** comme Origines **RC-12**)* |
| **RC-14** | Non-régression | **N1–N4** |

### 12.1 Fichier et exécution

* **Fichier** : **`tests/test_ckr_shop_collections.py`** — **BO consolidé** (module 19.0.1.5.0) : **RC-01 / RC-02 / RC-03 (×4)** **implémentés** dans `TestCkrCollectionsPVModel` + **2** méthodes de support logique (ordre `_ckr_resolve_visible_slugs`, défense bornes `date_start > date_end`) ; **RC-14** modèle et **toute** la classe `TestCkrCollectionsPVHttp` restent en `skipTest` jusqu'à l'ouverture du contrôleur public (étape 3).
* **Tag** dédié : **`dorevia_ckr_collections`** (en plus de **`post_install`**, **`-at_install`**) pour filtrer la suite sans lancer tout le module.
* **Exemple** :

```bash
odoo -d <base> --test-enable --stop-after-init \
  --test-tags=dorevia_ckr_collections
```

* **Pré-requis** : `website_sale` ; données module (modèle **`ckr.shop.collection`**, éventuelles **fixtures XML** si le pattern du projet l’impose).

### 12.2 `TransactionCase` — modèle et règles BO

| # | Sujet | Attendu |
|---|--------|---------|
| T1 | **Slug réservé `union`** | `ValidationError` (ou équivalent) à la **création** / **écriture** d’une collection avec **`slug=union`**. |
| T2 | **Unicité** `(website_id, slug)` | `IntegrityError` (ou contrainte SQL) sur **doublon** de slug pour le **même site**. |
| T3 | **Visibilité** | Domaine / helper « collection **visible** navigation » : **Active** + **période** + site — **jeux de dates** bornes inclus/exclus selon règle retenue en code (docstring du test **`TestCkrCollectionsPVModel.test_ckr_col_rc03_visibility_active_and_period`** — PV **RC-03**). |

### 12.3 `HttpCase` — routes, codes HTTP, canonical

Préparer en **`setUpClass`** au moins **deux** collections visibles **A** et **B** (slugs distincts, produits **M2M** ou pas selon scénario), une collection **inactive** ou **hors période** **C**, et des produits publiés.

| # | Scénario | Attendu |
|---|----------|---------|
| H1 | **`GET /collections`** | **200** ; corps contenant la **copy** bandeau générale (**§8**) ; liste produits cohérente avec la règle « **au moins une** collection visible ». |
| H2 | **`GET /collections/<slug_A>`** | **200** ; titre / bandeau alignés (**titre affiché** + fallback **§8** si pas de phrase BO). |
| H10 | **`GET /collections/union/<slug_A>/<slug_B>`** *(chemin **déjà** canonique, **A** & **B** visibles)* | **200** ; liste = produits dans **A** **OU** **B** ; titre page **« Collections sélectionnées »** ; sous-texte **§8** (*Voici les produits…*). |
| H3 | **`GET /collections/<slug_inconnu>`** | **302** vers **`/collections`** ; **pas** de query **`ckr_notice=`** sur la **Location** ; *(optionnel)* session / flash consommable une fois sur la page d’arrivée. |
| H4 | **`GET /collections/union/b/a`** (ordre **non** lexicographique) | **301** vers **`/collections/union/a/b`**. |
| H5 | **`GET /collections/union/a/a`** (doublon) | **301** vers **`/collections/union/a`** puis **301** vers **`/collections/a`** *(chaîne ou **301** direct selon impl. — à figer dans l’assert : l’URL finale doit être **`/collections/a`)*. |
| H6 | **`GET /collections/union/a`** (un seul segment) | **302** **`/collections`** + message (**§6**). |
| H7 | **`GET /collections/union/a/slug_invalide`** | **302** **`/collections`** (**repli A** — **pas** de 301 résiduel). |
| H8 | **`GET /collections/<slug_A>`** avec collection **valide** mais **0 produit** visible | **200** ; état vide **§12 A** (copy **§8**) ; **pas** de **302**. |
| H9 | **Canonical** (`<link rel="canonical">` ou équivalent Odoo) sur **H1**, **H2**, **H10** (union canonique) | **href** = **URL publique** self (**pas** de **`/shop?ckr_mode=collection`**). |

Helpers recommandés (comme Origines) : **`url_open(..., allow_redirects=False)`**, assertion sur **`Location`**, extraction **`_canonical_href(html)`**.

### 12.4 Non-régression modes existants

| # | Scénario | Attendu |
|---|----------|---------|
| N1 | **`/shop?ckr_mode=pack`** (ou **`/kits`** → 301) | Comportement **inchangé** vs baseline (code **200** ou redirections déjà actées). |
| N2 | **`/shop?ckr_mode=promo`** | Idem. |
| N3 | **`/shop?ckr_mode=origin`** (ou **`/origines`** → 301) | Idem. |
| N4 | **`_ckr_effective_mode()`** avec query **multi-modes** artificielle | Ordre de priorité **documenté** (**§5.1**) ; **aucune** régression sur les modes existants lorsque **`collection`** est ajouté. |

### 12.5 QWeb / copies *(smoke)*

* Vérifier la **présence** des chaînes **figées §8** dans le HTML des réponses **200** (éviter les régressions de traduction / clé template). **Tolérance** : normalisation espaces / entités HTML si besoin (`html.unescape` côté test).

### 12.6 Hors V1 ou optionnel

* **Performance** / garde-fou **n** segments union (longueur d’URL) : **test manuel** ou **seuil** documenté sauf exigence CI.
* **E2E navigateur** (Playwright, etc.) : **hors** spec module sauf pipeline produit déjà en place.

---

## 13. Checklist livraison module

- [x] Modèle **`ckr.shop.collection`** + M2M produits + contraintes + droits *(étape 1 — module 19.0.1.4.0 ; complété recette : ACL **public** + **portal** read-only ajoutées en 19.0.1.6.1 pour fiche produit visiteur)*.
- [x] Routes **`/collections`**, **`/collections/<slug>`**, **`/collections/union/<slug>/(…)`** + **301**/**302** *(étape 3 — module 19.0.1.6.0 ; **validées** en recette 23/23 verts sur RC-04 à RC-08)*.
- [x] Intégration liste **`/shop`** (helpers / template) **sans** fuite d’URL publique **`/shop?ckr_mode=collection…`** *(étape 3 — contexte non-persistant `request._ckr_collection_ctx` consommé par les hooks natifs ; **filtre catalogue déplacé** en recette 19.0.1.6.1 de `_get_shop_domain` vers `product.template._search_get_detail` — point unique en Odoo 19)*.
- [x] **`CKR_MODE_COLLECTION`** + hooks + **`_ckr_effective_mode()`** mis à jour *(étape 3 — ajout **en fin** de `CKR_MODE_PRIORITY` : pack > promo > origin > collection ; validé en recette par `TestCkrCollectionsPVModel.test_ckr_col_rc14_effective_mode_priority`)*.
- [x] **`_get_canonical_url`** Collections *(étape 3 — canonical **self** : `models/website.py` limite la réécriture au seul `path == /shop`, les routes nobles `/collections[/…]` conservent leur path courant ; validé par `test_ckr_col_rc12_canonical_self_paths`)*.
- [x] Bandeaux + **copies** §8 (textes figés MOA 2026-04-22) + état vide **§12 A** *(étape 3 — `views/pages/ckr_shop.xml` template `ckr_shop_collection_banner` ; validé RC-04 / 05 / 06 / 10 / 11)*.
- [x] Fiche produit liens **`/collections/<slug>`** *(étape 3 — `views/pages/ckr_product.xml` template `ckr_product_collections_block` + helper `product.template._ckr_get_visible_collections` ; validé RC-13 après fix ACL publique)*.
- [x] Cleanup stub + **`tests/test_ckr_shop_collections.py`** (**§12**, tag **`dorevia_ckr_collections`**) + **PV** [PV_RECETTE_COLLECTIONS_V1.md](PV_RECETTE_COLLECTIONS_V1.md) (**RC-01…RC-14**, nombre de tests §6 PV) *(étape 3 — `data/ckr_cleanup_collections_stub.xml` + retrait `website_page_collections` + suppression `views/pages/ckr_collections.xml` ; **23** méthodes, **0** `skipTest`, run v2 **intégralement vert** — PV §6)*.
- [x] **Recette MOA (module 19.0.1.6.1)** — suite `dorevia_ckr_collections` **exécutée réellement** sur `ckr_collections_recette`, **23/23 verts** (9 Model + 14 HTTP, 13,92 s, 2 016 requêtes). Preuves : `docs/phase_2/evidences/` (`run_rc_collections_v2_summary.log` + `README.md`). PV §4 renseigné colonne *Résultat observé* ; §7 anomalies A1/A2/A3/A4 **résolues** ; §8 **Conforme** ; §9 visas MOA / Dev posés. **Checklist §13 clôturée.**

---

## Historique

| Date | Événement |
|------|-----------|
| 2026-04-22 | **Création** — spec d’impl. ouverte sur la base du [CONTRAT_URL_COLLECTIONS.md](CONTRAT_URL_COLLECTIONS.md) (**S1** actée) ; résidus **§13** regroupés (copies, **302**, replis union, **`ckr_mode`**). |
| 2026-04-22 | **MOA** : **repli combinaison** = option **A** seule (V1) ; **message 302** = flash / session **one-shot** ; **titre union** = *Collections sélectionnées* ; **copies minimales** §8 figées ; statut **prête impl.** (résidu **`ckr_mode`** §5.1). **Contrat** §5–§8, §12 A, §13–§14 alignés. |
| 2026-04-22 | **§12** : plan de **tests automatisés** (`TransactionCase` + `HttpCase`, tag **`dorevia_ckr_collections`**, parité avec **`test_ckr_shop_origins.py`**). |
| 2026-04-22 | **[PV_RECETTE_COLLECTIONS_V1.md](PV_RECETTE_COLLECTIONS_V1.md)** : recette **RC-01…RC-14** ; **§12.0** tableau d’alignement PV ↔ **T/H/N** ; checklist §13. |
| 2026-04-22 | **Squelette** : fichier **`tests/test_ckr_shop_collections.py`** (classes + tag **`dorevia_ckr_collections`**, méthodes **PV** en **skip**). |
| 2026-04-22 | **PV / §12** : alignement **strict** noms **Classe.méthode** ; **RC-03** + test **`test_ckr_col_rc03_visibility_active_and_period`** (Active + période) ; **T3** lié explicitement. |
| 2026-04-22 | **§5.1** : **priorité `ckr_mode`** **figée** (**pack > promo > origin > collection**) ; **statut** = *Prête impl. v1*, **zéro résidu documentaire** — feu vert code. |
| 2026-04-22 | **Étape 1 checklist §13 — module 19.0.1.5.0** : bump **`__manifest__.py`** (version + description porte Collections) ; création **`models/ckr_shop_collection.py`** (champs **§2.1** — `name` translate, `slug` unique par site, `sequence`, `active`, `date_start` / `date_end`, `product_template_ids` M2M, `website_id` optionnel ; contraintes **§2.2** — `unique(website_id, slug)` SQL, slug regex + **`union` réservé**, fenêtre de dates cohérente) ; helpers **RC-03** (`_ckr_visible_domain`, `_ckr_is_visible`, `_ckr_resolve_visible_slugs`) ; enregistrement **`models/__init__.py`** + ACL **`security/ir.model.access.csv`** (employé lecture / designer CRUD — patron Origines). Reste à faire : inverse M2M `product.template`, vues BO + menus, routes / hooks contrôleur (**§3**, **§4**, **§5**), bandeaux + copies §8, fiche produit, cleanup stub, implémentation tests RC-01…RC-14. |
| 2026-04-22 | **Étape 2 checklist §13 — modèle complet BO** (RC-01 / RC-02 prêts) : inverse M2M **`ckr_collection_ids`** sur **`product.template`** (même table de liaison que le forward — colonnes inversées) ; **`views/ckr_shop_collection_views.xml`** — search (actives / archivées / en période / expirées / à venir / regroupement site), **list** (handle `sequence`, `slug`, `name`, `product_template_count`, `date_start/end`, `website_id` optionnel, `active` toggle), **form** (ribbon archivée, identité URL, publication, période, **notebook Produits rattachés**), action + **menus** Configuration + Catalog (patron Origines, séquence 20 après Origines) ; **`views/product_template_ckr_collection_views.xml`** — extension héritée de **`product_template_form_view_ckr_origin`**, champ **`ckr_collection_ids`** `many2many_tags` placé **après** `ckr_origin_value_ids` dans l'onglet Ventes ; enregistrement manifest (ordre : après vues Origines — dépendance d'héritage). Reste à faire : routes / hooks contrôleur (**§5.1** constantes + priorité figée), bandeaux + copies §8, fiche produit visiteur, cleanup stub, implémentation tests RC-01…RC-14. |
| 2026-04-22 | **Consolidation BO (pré-étape 3 checklist §13)** — **`tests/test_ckr_shop_collections.py`** : implémentation des **6** méthodes **RC-01 / RC-02 / RC-03 (×4)** dans `TestCkrCollectionsPVModel` — champ `ckr_collection_ids` visible sur `product_template_form_view_ckr_collection` (RC-01) ; multi-affectation produit avec contrôle symétrique forward / inverse et `product_template_count` (RC-02) ; slug `union` **réservé** + regex + vide (RC-03) ; unicité SQL `(website_id, slug)` via `savepoint` + `IntegrityError` (RC-03) ; présence `menu_ckreyol_configuration_collections`, `menu_ckreyol_catalog_collections`, `action_ckr_shop_collection` (RC-03) ; visibilité **Active + période** avec 6 cas `at_date`-paramétrés, **bornes incluses** (`date_start = today`, `date_end = today`) et cohérence domaine ORM ↔ `_ckr_is_visible` (RC-03). **Support logique** : `_ckr_resolve_visible_slugs` préserve l'ordre d'apparition en dédupliquant et filtrant les slugs non visibles (expirés) ; défense de cohérence `date_start > date_end` → `ValidationError`. **RC-14** modèle reste en `skipTest` (dépend de `CKR_MODE_PRIORITY` — étape 3). Classe `TestCkrCollectionsPVHttp` toujours en `skipTest` — activable à l'ouverture du contrôleur public. Reste à faire : **étape 3** — routes / hooks contrôleur (**§5.1** constantes + priorité figée), bandeaux + copies §8, fiche produit visiteur, cleanup stub, activation des `skipTest` HTTP RC-04…RC-14. |
| 2026-04-22 | **Recette MOA / clôture §13 — module 19.0.1.6.1** — exécution réelle de la suite **`dorevia_ckr_collections`** sur base dédiée (`ckr_collections_recette`, sandbox Odoo 19). Le run v1 a révélé **6 FAIL HTTP** convergeant tous vers deux causes structurelles Odoo 19 et deux finitions mineures, désormais corrigées : **(i)** **`product.template._search_get_detail`** — ajout du bloc **`ckr_collection_only`** qui injecte `[('id', 'in', options['ckr_collection_template_ids'])]` dans le `base_domain` ; Odoo 19 ne passe plus par `_get_shop_domain` dans `_shop_lookup_products` (remplacé par `website._search_with_fuzzy`), faisant de `_search_get_detail` le **point unique** de filtrage catalogue. **(ii)** **`controllers/website_sale_ckr._get_search_options`** — pose de **`options['ckr_collection_template_ids']`** en paire avec `ckr_collection_only` ; un ensemble vide garantit un résultat vide canonique (état vide §12 A) plutôt qu'une fuite catalogue. **(iii)** **`security/ir.model.access.csv`** — ajout de deux ACL **read-only** sur `ckr.shop.collection` pour **`base.group_public`** et **`base.group_portal`** ; indispensable à la fiche produit visiteur qui rend le bloc Collections via le M2M inverse `product.template.ckr_collection_ids` (sans `sudo()` côté QWeb). **(iv)** **`views/ckr_shop_collection_views.xml`** — retrait de l'attribut `string="Regrouper par"` sur `<group>` en search view (Odoo 19 RNG : `RELAXNG_ERR_INVALIDATTR`). **(v)** **`tests/test_ckr_shop_collections.py`** — `TestCkrCollectionsPVHttp.setUpClass` utilise désormais **`date.today()`** (alignement strict avec `fields.Date.context_today` utilisé dans `_ckr_visible_domain`) afin que la fixture *collection expirée* soit réellement hors période. Run v2 : **23 tests verts** (9 `TestCkrCollectionsPVModel` + 14 `TestCkrCollectionsPVHttp`), **0 FAIL / 0 ERROR / 0 `skipTest`**, 13,92 s, 2 016 requêtes. Preuves : `docs/phase_2/evidences/run_rc_collections_v1_summary.log` (avant correctifs) + `run_rc_collections_v2_summary.log` (recette valide) + `README.md`. [PV_RECETTE_COLLECTIONS_V1.md](PV_RECETTE_COLLECTIONS_V1.md) : §4 colonne *Résultat observé* renseignée, §7 anomalies **A1–A4 résolues**, §8 **Conforme**, §9 visas posés. **Checklist §13 clôturée.** |
| 2026-04-22 | **Étape 3 checklist §13 livrée — module 19.0.1.6.0** — **contrôleur public Collections ouvert**. **`controllers/website_sale_ckr.py`** : constantes **`CKR_MODE_COLLECTION`** + **`CKR_MODE_PRIORITY`** figée (**pack > promo > origin > collection**, collection **en fin**) ; constantes dédiées Collections (**`CKR_COLLECTION_BASE_PATH`**, **`CKR_COLLECTION_UNION_SEGMENT`**, kinds `general` / `single` / `union`, **`CKR_COLLECTION_FLASH_SESSION_KEY`**, **`CKR_COLLECTION_UNAVAILABLE_NOTICE`**) ; helpers module-level (`_ckr_collection_ctx_get/set`, `_ckr_collection_flash_consume/set`, `_ckr_collection_redirect_unavailable`, `_ckr_collection_union_canonical_path`, `_ckr_collection_resolve_template_ids`) ; extension des hooks existants (`_get_search_options`, `_get_shop_domain`, `_get_additional_shop_values`) lisant le contexte non-persistant **`request._ckr_collection_ctx`** pour injecter le filtre produit `id IN <template_ids>` et les variables QWeb du bandeau (titre, sous-texte, flash, empty, base_path) sans **aucune** mutation de l'URL publique ; routes nobles **`@http.route('/collections')`** (générale), **`'/collections/<string:slug>'`** (unitaire), **`'/collections/union'`** (garde — 302 repli), **`'/collections/union/<path:path>'`** (union S1) avec **301** normalisation (tri lexicographique strict, collapse après dédup → **`/collections/<slug>`**), **302** replis (slug inconnu, union incomplète raw_count=1, union invalide **repli A**) en flash session one-shot **sans** `ckr_notice` en query, délégation finale à **`self.shop(**post)`**. **`models/product_template.py`** : helper **`_ckr_get_visible_collections(website=None)`** (filtré via `_ckr_is_visible`). **`views/pages/ckr_shop.xml`** : template **`ckr_shop_collection_banner`** (title / eyebrow / subtext, flash `role="status"` `aria-live="polite"`, empty §12 A + CTA *Retour aux collections*). **`views/pages/ckr_product.xml`** : template **`ckr_product_collections_block`** (liste ul/li `ckr-product-collections`, liens `/collections/<slug>`). **Cleanup stub** : `data/ckr_cleanup_collections_stub.xml` (delete `website.page` + `ir.ui.view` key `ckr_page_collections`) ; retrait `website_page_collections` dans `website_pages_data.xml` ; suppression **`views/pages/ckr_collections.xml`**. **`__manifest__.py`** : bump **19.0.1.6.0**, description Collections enrichie, entrée `data/ckr_cleanup_collections_stub.xml` substituée à l'ancienne vue. **Tests** : **activation intégrale** — `TestCkrCollectionsPVModel.test_ckr_col_rc14_effective_mode_priority` (priorité figée, multi-modes, `collection` seul reconnu) + **12** méthodes `TestCkrCollectionsPVHttp` (RC-04 / 05 / 06 / 07 ×2 / 08 ×3 / 09 flash / 10 smoke / 11 empty / 12 canonical / 13 fiche produit / 14 non-régression). `setUpClass` HTTP déterministe : **A** / **B** visibles avec produit, **C** visible sans produit (RC-11), **D** archivée, **E** expirée, **lonely** produit sans collection. **§6 PV** : **20** méthodes totales, **0** `skipTest`. |
