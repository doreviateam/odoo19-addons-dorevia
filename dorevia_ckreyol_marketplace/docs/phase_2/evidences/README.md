# Preuves d'exécution — porte Collections (MOA / PV recette)

Ce dossier archive les traces d'exécution réelles de la suite de tests
`dorevia_ckr_collections` produites lors de la phase de recette MOA
(clôture checklist §13 de `SPEC_IMPL_COLLECTIONS.md`).

## Contexte d'exécution

* **Base de tests dédiée** : `ckr_collections_recette` (PostgreSQL sandbox).
* **Commande canonique** :

  ```shell
  cd /Users/doreviateam/sandbox-odoo19
  docker compose exec odoo odoo \
      -c /etc/odoo/odoo.conf \
      -d ckr_collections_recette \
      -i dorevia_ckreyol_marketplace \
      --test-enable --test-tags=dorevia_ckr_collections \
      --stop-after-init --without-demo=all \
      --log-level=test --http-port=8094
  ```

  (L'initial est remplacé par `-u dorevia_ckreyol_marketplace` pour les
  itérations après correctifs, même base conservée.)

## Fichiers

| Fichier | Contenu |
|---|---|
| `run_rc_collections_v1_summary.log` | Première exécution — 6 FAIL HTTP (RC-04/05/06/10/11/13). Filtrage catalogue par `_get_shop_domain` non appliqué en Odoo 19 (voir §Correctifs) ; fiche produit visiteur 403 (ACL publique manquante). |
| `run_rc_collections_v2_summary.log` | Exécution après correctifs — **23 tests `dorevia_ckr_collections` verts** (9 Model + 14 HTTP), 0 FAIL, 0 `skipTest`, 13,92 s. |

Les logs bruts complets (incluant les corps HTML de réponses /shop) ne sont
pas archivés ici pour lisibilité ; les résumés conservent toutes les
lignes significatives (`Starting …`, `FAIL:`, `AssertionError`,
`odoo.tests.stats`).

## Correctifs appliqués entre v1 et v2

Quatre correctifs mineurs, tous couverts par des commentaires inline dans
le code livré :

1. **`views/ckr_shop_collection_views.xml`** — retrait de
   `string="Regrouper par"` sur `<group>` dans la search view
   (Odoo 19 RNG : attribut `string` non autorisé sur `<group>` en
   `search`).
2. **`models/product_template.py::_search_get_detail`** — ajout d'un
   bloc `ckr_collection_only` qui injecte le domaine `('id', 'in',
   template_ids)` dans le `base_domain`. Odoo 19 n'invoque plus
   `_get_shop_domain` dans `_shop_lookup_products` ; `_search_get_detail`
   est le point unique de filtrage catalogue.
3. **`controllers/website_sale_ckr.py::_get_search_options`** — pose
   `options["ckr_collection_template_ids"]` en paire avec
   `ckr_collection_only` (consommé par le point ci-dessus). Un
   ensemble vide verrouille un résultat vide (état vide §12 A).
4. **`security/ir.model.access.csv`** — ajout de deux ACL **read-only**
   sur `ckr.shop.collection` pour `base.group_portal` et
   `base.group_public`. La fiche produit visiteur accède au M2M
   `product_template.ckr_collection_ids` (ORM public) pour rendre les
   liens `/collections/<slug>` ; sans ces droits la fiche produit
   renvoyait 403.
5. **`tests/test_ckr_shop_collections.py::setUpClass` (HTTP)** —
   passage de `today = date(2026, 6, 15)` à `today = date.today()` pour
   aligner les bornes `date_end` avec la véritable date `context_today`
   utilisée par `_ckr_visible_domain` (la collection « expirée » doit
   réellement se situer **dans le passé** vis-à-vis du jour
   d'exécution).

## Périmètre validé

* **Modèle / BO** : RC-01, RC-02, RC-03 (menus, slug unique par site web,
  slug réservé `union`, visibilité active + période), RC-14 modèle
  (priorité `_ckr_effective_mode()`), plus deux tests de support
  (contrainte `date_start ≤ date_end`, helper
  `_ckr_resolve_visible_slugs`).
* **HTTP / parcours visiteur** : RC-04 (vue générale), RC-05 (vue
  unitaire), RC-06 (union OU), RC-07 × 2 (301 normalisation —
  collapse + ordre/doublons), RC-08 × 3 (302 repli — slug inconnu,
  union incomplète, slug invalide), RC-09 (flash session sans
  query-string), RC-10 (copies fixes §8), RC-11 (état vide §12 A),
  RC-12 (canonical auto-cohérent), RC-13 (liens collections sur
  fiche produit), RC-14 HTTP (non-régression Kits / Promotions /
  Origines / Catégories).

**Conclusion recette MOA** : porte Collections **acceptée** — 23/23
verts sur le tag `dorevia_ckr_collections`, correspondance stricte PV
↔ méthodes de tests respectée, aucun `skipTest` résiduel. Checklist
§13 de `SPEC_IMPL_COLLECTIONS.md` clôturée.
