# Recette technique — Test global CK

| Champ | Valeur |
| --- | --- |
| Date | 2026-06-24 |
| Base | `dorevia_ck_marketone_01` |
| Conteneur | `sandbox-odoo19-odoo-1` |
| Commande | `odoo -c /etc/odoo/odoo.conf -d dorevia_ck_marketone_01 -u dorevia_ck_theme,dorevia_ck_marketone_content --test-enable --test-tags /dorevia_ck_theme,/dorevia_ck_marketone_content --stop-after-init --log-level=test --http-port=8079` |
| Log complet | `/private/tmp/ck_global_tests.log` |
| Statut | Echec global · 20 failures · 0 errors |

---

## 1. Resume

Le test global des deux modules CK a ete lance avec mise a jour des modules :

- `dorevia_ck_theme`
- `dorevia_ck_marketone_content`

Resultat Odoo :

```text
382 tests
20 failed
0 error(s)
```

Details par module :

```text
dorevia_ck_marketone_content : 442 tests declares / 91.68s / 51590 queries
dorevia_ck_theme             : 42 tests declares / 8.80s / 3169 queries
```

Le serveur principal est reste actif apres le run.

---

## 2. Echecs constates

### 2.1 Home featured — ancien contrat 5 produits

```text
TestCkCatalogManiocVariants.test_featured_selection_five_moa_products
```

Assertion :

```text
4 not greater than or equal to 5
```

Lecture :

```text
Le test attend encore au moins 5 produits vedettes,
alors que le lot recent a acte 4 cards "Nos coups de coeur".
```

### 2.2 Home featured propagation — 16 tests

Famille :

```text
TestCkFeaturedPropagation
```

Tests en echec :

- `test_change_price_propagates`
- `test_each_variant_card_has_its_own_product_id`
- `test_rename_product_propagates_to_card_title`
- `test_rename_ribbon_propagates_to_badge`
- `test_simple_product_price_change_regression`
- `test_template_republish_restores_its_variant_cards`
- `test_template_sale_ok_false_removes_its_cards`
- `test_template_unpublish_removes_its_variant_cards`
- `test_two_variants_simultaneous_price_change_are_distinct`
- `test_variant_additional_tag_propagates_to_labels`
- `test_variant_attribute_value_rename_propagates_to_title`
- `test_variant_change_keeps_other_template_card_identical`
- `test_variant_image_clear_reverts_to_template`
- `test_variant_price_change_does_not_contaminate_other`
- `test_variant_specific_image_triggers_refresh`
- `test_variant_unlisted_field_write_repairs_stale_card`

Lecture :

```text
Cette famille de tests semble encore raisonner sur un contrat ancien de propagation
des produits vedettes dans la home.

Les lots recents ont modifie le contrat :
- 4 cards au lieu de 8 / 5 ;
- CTA simplifie ;
- selection saturee par seed existant ;
- nouveaux comportements de refresh.
```

Ces echecs avaient deja ete signales comme preexistants / hors scope lors des lots home featured.

### 2.3 Home lot4 — newsletter / pro banner

```text
TestCkHomeLot4Hooks.test_bootstrap_replaces_dual_and_removes_pro_banner
```

Assertion :

```text
Texte RGPD newsletter attendu absent de l'arch home.
```

Lecture :

```text
Echec deja identifie precedemment comme preexistant au ticket "Nos coups de coeur".
```

### 2.4 Shop Phase 3 — tests obsoletes apres P2B Epicerie

```text
TestCkShopPhase3Compose.test_category_page_when_epicerie_exists
TestCkShopPhase3Compose.test_shop_has_phase3_compose_blocks
```

Assertions :

```text
o_wsale_category_description absent
s_ck_reassurance absent
```

Lecture :

```text
Ces tests verifient l'ancien contrat Phase 3 du shop.
Le rayon Epicerie P2B masque volontairement / remplace une partie du rendu natif
par le nouveau header editorial de rayon.
```

Ces tests doivent etre relus et mis a jour pour le contrat P1/P2A/P2B actuel.

---

## 3. Ce qui reste rassurant

Malgre le statut global rouge :

- 0 error technique ;
- le chargement des modules va au bout ;
- les tests header V2.2 demarrent et passent dans le run ;
- les tests shop cards P2A demarrent et passent dans le run ;
- les routes publiques principales vues pendant le run repondent `200` :
  - `/`
  - `/shop`
  - `/shop/cart`
  - `/professionnels`
  - `/contactus`
  - `/a-propos`
  - `/recettes`
  - pages produit testees.

---

## 4. Verdict

```text
Le test global n'est pas vert.
Il echoue sur 20 tests, sans erreur serveur.
Les echecs semblent majoritairement lies a des contrats de tests anciens
ou non realignes avec les decisions recentes Home featured / Shop P2A / Epicerie P2B.
```

Priorite recommandee :

1. Mettre a jour les tests `TestCkFeaturedPropagation` pour le contrat home featured actuel.
2. Mettre a jour `test_featured_selection_five_moa_products` pour le cap 4 cards.
3. Revoir les deux tests Shop Phase 3 en distinguant :
   - `/shop` general ;
   - categorie Epicerie avec header editorial P2B ;
   - categories sans bloc P2B.
4. Relancer le global.
