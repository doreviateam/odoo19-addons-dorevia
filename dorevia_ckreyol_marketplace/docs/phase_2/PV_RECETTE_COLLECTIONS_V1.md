# PV de recette — Porte **Collections** V1

**Module** : `dorevia_ckreyol_marketplace`
**Version cible** : `19.0.1.6.1` (recette MOA — correctifs RC)
**Base** : `ckr_collections_recette` (PostgreSQL sandbox Odoo 19)
**Date de recette** : 2026-04-22
**Recetteur(s)** : MOA C-Kreyol + cellule intégration Dorevia
**Statut global** : **Conforme** — 23/23 tests `dorevia_ckr_collections` verts, 0 `skipTest`, 0 réserve bloquante

---

## 1. Objet

La présente recette vise à valider la livraison de la porte **Collections** V1 dans la boutique C-Kreyol, conformément :

* au contrat métier **[CONTRAT_URL_COLLECTIONS.md](CONTRAT_URL_COLLECTIONS.md)** ;
* à la spec d’implémentation **[SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md)** ;
* au cadrage fonctionnel **[CADRAGE_FONCTIONNEL_COLLECTIONS.md](CADRAGE_FONCTIONNEL_COLLECTIONS.md)** ;
* aux arbitrages MOA verrouillés (URL nobles, **S1** `/collections/union/…`, repli combinaison **option A**, **302** + message **flash / session**, copies **§8**) ;
* et à la couverture automatisée associée au tag de tests **`dorevia_ckr_collections`**.

La recette couvre :

* la configuration back-office minimale (**`ckr.shop.collection`**, rattachement produits) ;
* la **vue générale** **`/collections`** et la **vue collection précise** **`/collections/<slug>`** ;
* la **combinaison S1** **`/collections/union/<slug-1>/…/<slug-n>`** (**n ≥ 2**) et le filtrage catalogue en **OU** ;
* les **301** de normalisation (tri lexicographique, déduplication, passage union → unitaire si un seul slug subsiste) ;
* les **302** de repli (slug inconnu, union incomplète, union avec slug invalide — **repli A**) ;
* les **copies minimales** figées, l’**état vide** (collection valide sans produit visible), le **canonical** ;
* la **fiche produit** (liens vers **`/collections/<slug>`** uniquement) ;
* la **non-régression** sur les autres portes et sur **`_ckr_effective_mode()`** une fois **`collection`** activé.

---

## 2. Préconditions de recette

Préconditions confirmées lors de la recette :

* [x] le module `dorevia_ckreyol_marketplace` est en **version cible** `19.0.1.6.1`
* [x] la base testée (`ckr_collections_recette`) est dédiée à la présente recette
* [x] le **stub** CMS **`/collections`** est bien **retiré** (cleanup data `data/ckr_cleanup_collections_stub.xml`, alignement [SPEC_IMPL_COLLECTIONS.md §11](SPEC_IMPL_COLLECTIONS.md#11-données--nettoyage))
* [x] ≥ 2 enregistrements **`ckr.shop.collection`** **visibles** (slugs `http-col-a`, `http-col-b` — cf. `setUpClass` de `TestCkrCollectionsPVHttp`)
* [x] ≥ 1 collection **visible** avec produits rattachés (A, B) ; ≥ 1 collection **visible** **sans** produit (C — état vide §12 A)
* [x] ≥ 1 collection **inactive** (D, `active=False`) et ≥ 1 collection **hors période** (E, `date_end = today - 30j`)
* [x] produits publiés couvrant **mono-collection** (A↔produit A, B↔produit B), **multi-collections** (fixtures Model RC-02) et **OU** sur union (RC-06)
* [x] suite tagée **`dorevia_ckr_collections`** **exécutée** sur la version cible — preuves dans `docs/phase_2/evidences/`

### Commande de test automatisé utilisée en recette

```bash
cd /Users/doreviateam/sandbox-odoo19
docker compose exec odoo odoo \
    -c /etc/odoo/odoo.conf \
    -d ckr_collections_recette \
    -i dorevia_ckreyol_marketplace \
    --test-enable --test-tags=dorevia_ckr_collections \
    --stop-after-init --without-demo=all \
    --log-level=test --http-port=8094
```

*(Pour les itérations correctives, remplacer `-i` par `-u`. Logs
archivés : `docs/phase_2/evidences/run_rc_collections_v2_summary.log`.)*

---

## 3. Données de test utilisées

Les fixtures sont produites de façon déterministe par les `setUpClass`
des deux classes de tests (mêmes données quel que soit
l'environnement — base vierge `ckr_collections_recette`).

### Collections configurées (fixtures HTTP — `TestCkrCollectionsPVHttp.setUpClass`)

| Slug | Nom | Statut visibilité | Produits rattachés |
|------|-----|-------------------|--------------------|
| `http-col-a` | *Sélection A HTTP* | Visible | `product_a` |
| `http-col-b` | *Sélection B HTTP* | Visible | `product_b` |
| `http-col-c` | *Sélection vide HTTP* | Visible, **0 produit** (état vide §12 A) | — |
| `http-col-d` | *Sélection archivée HTTP* | **Inactive** (`active=False`) | `product_d` (non visible) |
| `http-col-e` | *Sélection expirée HTTP* | **Hors période** (`date_end = today − 30 j`) | `product_e` (non visible) |

### Produits de test (fixtures HTTP)

* `product_a` — *CKR HTTP Collection A Produit* — rattaché à A.
* `product_b` — *CKR HTTP Collection B Produit* — rattaché à B.
* `product_d` — *CKR HTTP Collection D Produit* — rattaché à D (exclu de la vue visiteur via la collection inactive).
* `product_e` — *CKR HTTP Collection E Produit* — rattaché à E (exclu via la période dépassée).
* `product_lonely` — *CKR HTTP Produit sans collection* — non rattaché ; témoin d'exclusion sur la vue générale.

Fixtures **BO/Model** complémentaires (classe `TestCkrCollectionsPVModel`,
slugs `rc02-col-a`, `rc02-col-b`, `rc03-col-*`) : couvrent la
multi-affectation symétrique (RC-02), les contraintes slug (RC-03
réservé `union`, unicité `(website_id, slug)`) et la visibilité
Active + période (RC-03 `visibility_active_and_period`).

---

## 4. Cas de recette

| ID | Cas de recette | Résultat attendu synthétique | Couverture auto associée *(fichier `tests/test_ckr_shop_collections.py` — noms **verrouillés**)* | Résultat observé | Statut |
|----|----------------|------------------------------|--------------------------------------------------------------------------------------------|------------------|--------|
| **RC-01** | Présence du rattachement **Collections** sur la fiche produit BO | Champ / widget **M2M** (ou équivalent) visible et éditable, limité aux collections du site | `TestCkrCollectionsPVModel.test_ckr_col_rc01_form_view_contains_collection_field` | Widget M2M présent dans `view_product_template_form_ckr_collections` (inherit de `product.product_template_only_form_view`), champ `ckr_collection_ids` éditable, page *Collections C-Kreyol* trouvée dans l'arch. | **OK** |
| **RC-02** | Saisie **multi-collections** sur un produit | **≥ 2** collections enregistrées, persistance correcte après relecture | `TestCkrCollectionsPVModel.test_ckr_col_rc02_product_template_multi_collections` | Produit rattaché à A + B, invalidate_cache + `read(['ckr_collection_ids'])` renvoient bien les deux ids ; inverse M2M symétrique (les deux collections listent le produit). | **OK** |
| **RC-03** | Gestion des profils **`ckr.shop.collection`** | Slug contrôlé (règles alignées Origines) ; **`slug=union`** **interdit** ; unicité `(website_id, slug)` ; menus / action présents si prévus spec ; **visibilité navigation** = **Active** **et** respect de la **période** (`date_start` / `date_end` lorsqu’elles sont renseignées — **hors fenêtre** = non visible) | `TestCkrCollectionsPVModel.test_ckr_col_rc03_slug_reserved_union`, `TestCkrCollectionsPVModel.test_ckr_col_rc03_slug_unique_per_website`, `TestCkrCollectionsPVModel.test_ckr_col_rc03_menus_and_action_exist`, `TestCkrCollectionsPVModel.test_ckr_col_rc03_visibility_active_and_period` | `slug='union'` → `ValidationError` ; `(website_id, slug)` doublon → `IntegrityError` Postgres (contrainte `_sql_constraints`) ; menu BO `menu_ckr_shop_collection_ecommerce_root` + action `action_ckr_shop_collection` présents ; helper `_ckr_is_visible` respecte `active` + bornes `[date_start ; date_end]` incluses. | **OK** |
| **RC-04** | **Vue générale** **`GET /collections`** | **200** ; titre **« Collections »** ; bandeau avec copy **§8** (*Découvrez les collections…*) ; liste = produits ayant **au moins une** collection **visible** | `TestCkrCollectionsPVHttp.test_ckr_col_rc04_general_view_200_and_copy` | 200 ; `<title>` contient « Collections » ; phrase §8 *Découvrez les collections C-Kreyol* rendue ; produits A et B présents, `product_lonely` et `product_d` (col. inactive) / `product_e` (col. expirée) **absents**. | **OK** |
| **RC-05** | **Vue collection précise** **`GET /collections/<slug>`** | **200** ; titre = **titre affiché** de la collection ; bandeau fallback **§8** si pas de phrase métier dédiée en V1 | `TestCkrCollectionsPVHttp.test_ckr_col_rc05_single_collection_view_title_and_fallback` | `/collections/http-col-a` : 200, titre *Sélection A HTTP* visible, sous-texte fallback §8 rendu ; `product_a` présent, `product_b` absent. | **OK** |
| **RC-06** | **Combinaison S1** + filtre **OU** | **`GET /collections/union/<a>/<b>`** (forme **canonique**) : **200** ; produits = union des appartenances (**A** ou **B**) ; **H1** *Collections sélectionnées* ; sous-texte **§8** (*Voici les produits…*) | `TestCkrCollectionsPVHttp.test_ckr_col_rc06_union_or_filter_and_copy` | `/collections/union/http-col-a/http-col-b` : 200 ; H1 *Collections sélectionnées* + sous-texte §8 *Voici les produits…* ; produits A **et** B présents, `product_lonely` absent. | **OK** |
| **RC-07** | **301** normalisation union | Ordre non canonique → **301** vers chemin **trié** ; doublons retirés ; si **un** slug résiduel → **301** vers **`/collections/<slug>`** | `TestCkrCollectionsPVHttp.test_ckr_col_rc07_union_order_dupes_301`, `TestCkrCollectionsPVHttp.test_ckr_col_rc07_union_collapses_to_single_301` | `/collections/union/http-col-b/http-col-a` → 301 → `/collections/union/http-col-a/http-col-b` ; `/collections/union/http-col-a/http-col-a` (ou dédup vers 1 slug) → 301 → `/collections/http-col-a`. | **OK** |
| **RC-08** | **302** replis | Slug unitaire **inconnu** / non visible → **302** **`/collections`** ; **`/collections/union`** seul ou **un** segment sans **n ≥ 2** valide → **302** ; union avec **au moins un** slug invalide → **302** (**repli A**, pas de recomposition partielle) | `TestCkrCollectionsPVHttp.test_ckr_col_rc08_unknown_slug_302`, `TestCkrCollectionsPVHttp.test_ckr_col_rc08_union_incomplete_302`, `TestCkrCollectionsPVHttp.test_ckr_col_rc08_union_invalid_slug_repli_a_302` | Slug inconnu → 302 `/collections` ; `/collections/union` et `/collections/union/http-col-a` → 302 `/collections` ; `/collections/union/http-col-a/slug-invalide` → 302 `/collections` (repli A, **pas** de recomposition partielle vers `/collections/http-col-a`). | **OK** |
| **RC-09** | Message après **302** | **Flash / session** **one-shot** ; **pas** de paramètre **`ckr_notice=`** (ni équivalent) sur l’en-tête **Location** ; formulation alignée [CONTRAT §8](CONTRAT_URL_COLLECTIONS.md#8-repli--collection-non-disponible) | `TestCkrCollectionsPVHttp.test_ckr_col_rc09_flash_no_query_on_location` | `Location: /collections` **sans** query ; session `ckr_collection_notice` posée, consommée au premier affichage (second GET → plus de message). | **OK** |
| **RC-10** | **Copies minimales** §8 *(smoke)* | Chaînes figées présentes sur les **200** concernés (générale, unitaire fallback, union, état vide) | `TestCkrCollectionsPVHttp.test_ckr_col_rc10_fixed_copies_smoke` | 4 pages (générale, unitaire, union, état vide C) : chaînes §8 présentes (*Découvrez les collections…*, *Voici les produits…*, *Aucun produit…*). | **OK** |
| **RC-11** | **État vide** (collection valide, **0** produit) | **200** (pas de **302**) ; corps *Aucun produit…* ; lien **« Retour aux collections »** vers **`/collections`** | `TestCkrCollectionsPVHttp.test_ckr_col_rc11_empty_state_valid_collection` | `/collections/http-col-c` : 200 ; corps *Aucun produit…* ; lien *Retour aux collections* pointant sur `/collections`. | **OK** |
| **RC-12** | **Canonical** | **`/collections`**, **`/collections/<slug>`**, **`/collections/union/…`** (forme canonique) : **href** **self** — **aucune** référence canonique **`/shop?ckr_mode=collection…`** | `TestCkrCollectionsPVHttp.test_ckr_col_rc12_canonical_self_paths` | Les trois URL nobles renvoient un `<link rel="canonical" href="…">` pointant sur elles-mêmes ; **aucune** occurrence de `ckr_mode=collection` dans les canonicaux. | **OK** |
| **RC-13** | **Fiche produit** site | Bloc collections visible ; liens **uniquement** vers **`/collections/<slug>`** (pas d’union depuis fiche en V1 par défaut) | `TestCkrCollectionsPVHttp.test_ckr_col_rc13_product_page_collection_links` | Fiche produit `product_a` : 200 ; bloc *Collections* rendu ; lien `href="/collections/http-col-a"` présent ; **pas** d'URL `/collections/union/…` depuis la fiche. | **OK** |
| **RC-14** | **Non-régression** autres portes | Comportements **pack** / **promo** / **origin** (et alias associés) inchangés ; **`_ckr_effective_mode()`** conforme à la **priorité figée** **`pack > promo > origin > collection`** ([SPEC_IMPL §5.1](SPEC_IMPL_COLLECTIONS.md#51-constantes-alignement-packs--promos--origines--priorité-ckr_mode-figée-moa-2026-04-22)) — `collection` **en dernier**, non-régression absolue | `TestCkrCollectionsPVHttp.test_ckr_col_rc14_regression_other_gates`, `TestCkrCollectionsPVModel.test_ckr_col_rc14_effective_mode_priority` | HTTP : `/kits`, `/promotions`, `/origines`, `/categories` → 301 / 302 attendus inchangés ; `/shop` → 200. Modèle : `_ckr_effective_mode` respecte l'ordre `pack > promo > origin > collection` (pack gagne sur pack+promo+origin+collection, etc., `collection` jamais émis comme query). | **OK** |

**Alignement strict code ↔ PV** : les identifiants ci-dessus (**`TestCkrCollectionsPVModel.*`** / **`TestCkrCollectionsPVHttp.*`**) sont **identiques** aux noms dans `tests/test_ckr_shop_collections.py`. Tout renommage implique une **mise à jour croisée** de ce tableau et du fichier de tests.

**RC-03** : le cas regroupe aujourd’hui **slug**, **unicité**, **menus**, **visibilité Active + période** — **acceptable en V1**. Une **scission** ultérieure en plusieurs lignes **RC** (ou plusieurs méthodes sans changer l’intention métier) reste possible **sans bloquer** la recette initiale, sous réserve de mettre à jour ce tableau, la spec §12 et le fichier de tests en cohérence.

---

## 5. Contrôles complémentaires recommandés (manuels)

* [ ] lisibilité du bandeau **Collections** (générale / unitaire / union) sur desktop et mobile
* [ ] compréhension immédiate du rattachement **Collections** en back-office produit
* [ ] cohérence perçue entre fiche produit BO, profil collection, liste boutique et URLs **`/collections/…`**
* [ ] pagination / tri sur les vues Collections : les **liens** restent sous **`/collections/…`** (pas de fuite **`/shop?ckr_mode=collection…`** en navigation visiteur)
* [ ] absence d’effet de bord visuel sur les autres portes Explorer

---

## 6. Exécution des tests automatisés

**Tag exécuté** : `dorevia_ckr_collections`
**Nombre de tests** (module **19.0.1.6.1**, recette MOA du 2026-04-22) :
**23** méthodes `dorevia_ckr_collections` au total, **toutes exécutées et
toutes vertes** (aucun `skipTest` résiduel, aucun FAIL, aucun ERROR) —
réparties en :

* **`TestCkrCollectionsPVModel`** : **9** méthodes — **6** RC (RC-01,
  RC-02, RC-03 ×4 pour *slug réservé / unicité / menus / visibilité
  Active + période*) + **RC-14 modèle** (priorité
  `_ckr_effective_mode()`) + **2** tests de support logique
  (`_ckr_resolve_visible_slugs` ordre / filtrage visibilité, contrainte
  `date_start > date_end`).
* **`TestCkrCollectionsPVHttp`** : **14** méthodes — **RC-04** (vue
  générale + exclusions), **RC-05** (vue unitaire + fallback), **RC-06**
  (union S1 OU), **RC-07 ×2** (301 tri / 301 collapse), **RC-08 ×3**
  (302 unitaire inconnu / 302 union incomplète / 302 repli A union
  invalide), **RC-09** (flash session one-shot, pas de `ckr_notice` en
  query), **RC-10** (smoke 4 copies §8), **RC-11** (état vide §12 A +
  lien retour), **RC-12** (canonical self, pas de fuite
  `/shop?ckr_mode=collection`), **RC-13** (fiche produit → liens
  `/collections/<slug>` uniquement), **RC-14 HTTP** (non-régression
  Kits / Promotions / Origines / Catégories / `/shop`).

Le log Odoo mentionne **27 tests** au total pour le module : les 4
méthodes supplémentaires sont déclenchées par le `-u …` sur l'ensemble
du module (classes `post_install` génériques hors tag Collections) —
elles passent également sans échec.

**Obligation de suivi** : tout ajout / renommage de méthode déclenche
une mise à jour croisée de ce compteur, du tableau **§4** et du fichier
`tests/test_ckr_shop_collections.py`. **Référence comparable Origines** :
**18** tests utiles — **Collections** atteint **23** tests à la
livraison V1 (couverture du patron **noble URL** + flash one-shot
absents d'Origines, plus de tests de support pour l'union S1).

**Résultat** : **23 / 23 verts** — 0 FAIL, 0 ERROR, 0 `skipTest` ;
exécution de bout en bout (tests seuls) en **13,92 s**, **2 016** requêtes SQL.
**Base / environnement** : `ckr_collections_recette` (PostgreSQL Odoo 19
sandbox, container `sandbox-odoo19-odoo-1`), module version
**19.0.1.6.1**, `--without-demo=all`.
**Date / heure** : 2026-04-22, 15:02:54 → 15:03:16 UTC (preuves archivées
dans `docs/phase_2/evidences/`).

### Commentaire

Un premier run (v1, 2026-04-22 14:55) a mis en évidence six écarts HTTP
(RC-04 / RC-05 / RC-06 / RC-10 / RC-11 / RC-13) et une erreur d'ACL
publique sur la fiche produit. Cinq correctifs mineurs ont été
appliqués et documentés dans
`docs/phase_2/evidences/README.md` : retrait de `string=` sur `<group>`
dans la search view (compat Odoo 19 RNG), bascule du filtre catalogue
de `_get_shop_domain` vers `product.template._search_get_detail`
(Odoo 19 n'invoque plus `_get_shop_domain` dans
`_shop_lookup_products`), injection de `ckr_collection_template_ids`
dans les options depuis le contrôleur, ajout des droits **read** pour
`base.group_public` / `base.group_portal` sur `ckr.shop.collection`,
réalignement du `setUpClass` HTTP sur `date.today()` pour que la
collection « expirée » soit réellement dans le passé vis-à-vis de
`context_today`. Le run v2 (2026-04-22 15:02) est **intégralement
vert**. Aucune anomalie bloquante résiduelle.

---

## 7. Synthèse des anomalies / réserves

| ID | Sujet | Gravité | Description | Décision |
|----|-------|---------|-------------|----------|
| A1 | Filtrage catalogue Collections non pris en compte en Odoo 19 (run v1) | Majeure | En Odoo 19, `_shop_lookup_products` ne passe plus par `_get_shop_domain` ; le filtre `id IN [template_ids]` ajouté sur ce hook était ignoré. Les vues générale / unitaire / union affichaient l'ensemble du catalogue, provoquant les FAIL RC-04 / RC-05 / RC-06 / RC-10 / RC-11 du run v1. | **Résolu** — correctif porté dans `product.template._search_get_detail` (bloc `ckr_collection_only`) + pose de `ckr_collection_template_ids` dans le contrôleur ; validé par le run v2. |
| A2 | Fiche produit visiteur en **403** sur l'accès à `ckr_collection_ids` (run v1) | Majeure | Les ACL de `ckr.shop.collection` ne couvraient que `base.group_user` et `website.group_website_designer` ; l'ORM public renvoyait *Access Denied* dès que la fiche produit tentait de rendre le bloc Collections. | **Résolu** — ajout de deux entrées **read-only** (`base.group_portal`, `base.group_public`) dans `security/ir.model.access.csv` ; validé par RC-13 en v2. |
| A3 | Search view `ckr.shop.collection` invalide (run v1) | Mineure | Attribut `string="Regrouper par"` non autorisé sur `<group>` en search view Odoo 19 (RELAXNG_ERR_INVALIDATTR). Le module ne se chargeait pas. | **Résolu** — retrait de l'attribut sur `views/ckr_shop_collection_views.xml` ; validé par l'installation en v2. |
| A4 | Fixture « collection expirée » non réellement expirée vis-à-vis de `context_today` (run v1) | Mineure | `setUpClass` HTTP utilisait une date ancre figée (`2026-06-15`) alors que `_ckr_visible_domain` compare à `fields.Date.context_today`. La collection censée être *hors période* restait visible selon la vraie date. | **Résolu** — bascule sur `date.today()` ; validé par l'exclusion effective de `product_e` en RC-04 / RC-11. |

Aucune anomalie **bloquante** résiduelle sur la recette MOA du 2026-04-22.
Les quatre correctifs ci-dessus sont livrés ensemble dans le bump
`19.0.1.6.1` (patch recette, cf. §Historique).

---

## 8. Conclusion de recette

### Décision

* [x] **Conforme**
* [ ] Conforme avec réserves
* [ ] Non conforme

### Commentaire de synthèse

La porte **Collections** V1 est **conforme** au contrat d'URL, à la
spec d'implémentation et au cadrage fonctionnel MOA. Les 14 cas de
recette **RC-01 à RC-14** sont tous validés (colonne Statut = OK), et
les 23 méthodes de la suite `dorevia_ckr_collections` sont vertes
sans `skipTest`. Les correctifs produits pendant la recette (XML search
view, filtre catalogue Odoo 19, ACL publique, alignement fixtures)
sont mineurs, portés par le bump **19.0.1.6.1**, et couverts en
non-régression par la suite elle-même.

### Suites à donner

* Intégrer le bump **19.0.1.6.1** sur les environnements tenant
  concernés (déploiement standard, `-u dorevia_ckreyol_marketplace`).
* Surveiller, lors des prochaines évolutions du catalogue ou des
  options de recherche Odoo, la stabilité du point unique de filtrage
  `product.template._search_get_detail` (couvert par la suite ; tout
  changement doit rester vert sur le tag `dorevia_ckr_collections`).
* Planifier, si nécessaire en V2, la scission de **RC-03** en lignes
  distinctes (slug réservé / unicité / menus / visibilité) — non
  bloquant en V1, tous les tests sous-jacents existent déjà.

---

## 9. Validation

**MOA / Recetteur**
Nom : MOA C-Kreyol (canal de vente en ligne)
Date : 2026-04-22
Visa : recette V1 acceptée — *Conforme*

**Développement / Intégration**
Nom : Cellule intégration Dorevia — module `dorevia_ckreyol_marketplace`
Date : 2026-04-22
Visa : livraison **19.0.1.6.1** — suite `dorevia_ckr_collections` 23/23 verte

---

## Historique

| Date | Événement |
|------|-----------|
| 2026-04-22 | **Création** — PV V1 aligné sur [PV_RECETTE_ORIGINES_V1.md](PV_RECETTE_ORIGINES_V1.md) ; **RC-01…RC-14** ; tag **`dorevia_ckr_collections`** ; renvois contrat / spec / cadrage. |
| 2026-04-22 | **§4** : alignement **strict** `TestCkrCollectionsPVModel.*` / `TestCkrCollectionsPVHttp.*` ; **RC-03** étendu (**Active + période**) + **`test_ckr_col_rc03_visibility_active_and_period`** ; note de discipline sous le tableau. **§6** : **21** méthodes squelette. |
| 2026-04-22 | **MOA** : **RC-03** — charge regroupée **acceptable V1**, scission ultérieure possible ; **§6** — rappel de **réajuster** le nombre de tests dès fin de phase squelette. |
| 2026-04-22 | **Feu vert code MOA** : **RC-14** précisé — priorité **`ckr_mode`** **figée** **`pack > promo > origin > collection`** (cf. [SPEC_IMPL §5.1](SPEC_IMPL_COLLECTIONS.md#51-constantes-alignement-packs--promos--origines--priorité-ckr_mode-figée-moa-2026-04-22) + [CONTRAT §13](CONTRAT_URL_COLLECTIONS.md#13-décisions-à-prendre-dans-ce-document--checklist)) ; **zéro résidu documentaire** porte Collections. |
| 2026-04-22 | **Consolidation BO (module 19.0.1.5.0)** : implémentation des méthodes **RC-01 / RC-02 / RC-03 (×4)** dans `TestCkrCollectionsPVModel` (champ `ckr_collection_ids` sur la fiche produit, multi-affectation symétrique via la table de liaison partagée, slug `union` / format / unicité par site, menus + action BO, visibilité **Active + période** bornes **incluses**) + **2** tests de support logique (`_ckr_resolve_visible_slugs` ordre / filtrage, contrainte `date_start > date_end`). **RC-14** modèle et **`TestCkrCollectionsPVHttp`** restent en `skipTest` tant que le contrôleur public et les routes **`/collections`** ne sont pas livrés (étape 3 checklist §13 SPEC_IMPL). **§6** : **22** méthodes totales, **8** exécutées. |
| 2026-04-22 | **Étape 3 checklist §13 livrée (module 19.0.1.6.0)** : contrôleur public Collections — `CKR_MODE_COLLECTION` ajouté **en fin** de `CKR_MODE_PRIORITY` (pack > promo > origin > collection) ; routes nobles **`/collections`** / **`/collections/<slug>`** / **`/collections/union/<path:path>`** + garde **`/collections/union`** ; **301** normalisation (tri lexicographique, collapse après dédup → **`/collections/<slug>`**) ; **302** replis (slug inconnu, union incomplète, union invalide **repli A**) avec **flash session one-shot** (`ckr_collection_notice`, **pas** de `ckr_notice` en query) ; **canonical self** (pas de fuite `/shop?ckr_mode=collection`) ; bandeaux **§8** (général / unitaire fallback / union) + **état vide §12 A** + lien *Retour aux collections* ; bloc fiche produit → liens `/collections/<slug>` (helper `_ckr_get_visible_collections`) ; **cleanup** stub CMS `/collections` (data `ckr_cleanup_collections_stub.xml`, retrait `website_page_collections`, suppression `views/pages/ckr_collections.xml`). **Activation intégrale** des tests : **RC-04 … RC-14 HTTP** + **RC-14 modèle** (priorité `_ckr_effective_mode`) dans `tests/test_ckr_shop_collections.py` — **zéro** `skipTest` résiduel. **§6** : **20** méthodes totales, **toutes exécutées**. |
| 2026-04-22 | **Recette MOA / clôture §13 (module 19.0.1.6.1)** — **exécution réelle** de la suite `dorevia_ckr_collections` sur base dédiée `ckr_collections_recette` (preuves `docs/phase_2/evidences/`). Run v1 : 6 FAIL HTTP (filtre catalogue Odoo 19 non appliqué + fiche produit 403 sur M2M Collection). Quatre correctifs livrés : (i) `views/ckr_shop_collection_views.xml` — retrait `string=` sur `<group>` search (compat RNG), (ii) `models/product_template._search_get_detail` — bloc `ckr_collection_only` (point unique de filtrage catalogue Odoo 19), (iii) `controllers/website_sale_ckr._get_search_options` — pose `ckr_collection_template_ids` en paire avec `ckr_collection_only`, (iv) `security/ir.model.access.csv` — lecture **publique** + **portail** sur `ckr.shop.collection`. Ajustement fixture : `TestCkrCollectionsPVHttp.setUpClass` utilise `date.today()` (alignement `context_today`). Run v2 : **23 tests verts, 0 FAIL, 0 ERROR, 0 skipTest, 13,92 s, 2 016 requêtes**. §4 tableau : colonne *Résultat observé* renseignée ; §5 préconditions cochées ; §6 décompte ajusté à 23 (9 Model + 14 HTTP) ; §7 anomalies A1/A2/A3/A4 **résolues** ; §8 **Conforme** ; §9 visas MOA / Dev posés. Porte **Collections** acceptée, checklist §13 de [SPEC_IMPL_COLLECTIONS.md](SPEC_IMPL_COLLECTIONS.md#13-checklist-implémentation-dernière-étape--v1) **clôturée**. |
