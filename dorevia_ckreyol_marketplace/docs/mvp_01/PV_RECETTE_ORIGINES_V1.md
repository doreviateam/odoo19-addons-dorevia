# PV de recette — Porte **Origines** V1

**Module** : `dorevia_ckreyol_marketplace`
**Version cible** : `19.0.1.4.3`
**Base** : `tenant_o7`
**Date de recette** : [à compléter]
**Recetteur(s)** : [à compléter]
**Statut global** : [À compléter — Conforme / Conforme avec réserves / Non conforme]

---

## 1. Objet

La présente recette vise à valider la livraison de la porte **Origines** V1 dans la boutique C-Kreyol, conformément :

* au contrat métier `CONTRAT_URL_ORIGINES.md` ;
* à la spec d’implémentation `SPEC_IMPL_ORIGINES.md` ;
* aux arbitrages MOA/PV verrouillés avant développement ;
* et à la couverture automatisée associée au tag de tests `dorevia_ckr_origins`.

La recette couvre :

* la configuration back-office minimale ;
* le comportement de navigation `/origines` et `/shop?ckr_mode=origin...` ;
* l’affichage du bandeau et de l’état vide ;
* la visibilité des origines sur la fiche produit ;
* la non-régression sur les autres portes.

---

## 2. Préconditions de recette

À confirmer avant exécution :

* [ ] le module `dorevia_ckreyol_marketplace` est bien en version `19.0.1.4.3`
* [ ] la base testée est bien `tenant_o7`
* [ ] le stub `/origines` a bien été retiré
* [ ] l’attribut produit **Origine** existe
* [ ] au moins 2 valeurs existent dans l’attribut **Origine**
* [ ] au moins 2 produits publiés sont rattachés à des origines
* [ ] au moins 1 produit porte plusieurs origines
* [ ] au moins 2 profils `ckr.shop.origin` publiés existent
* [ ] au moins 1 profil `ckr.shop.origin` a une `context_phrase`
* [ ] au moins 1 origine valide n’a aucun produit rattaché (pour test état vide), ou cas simulé
* [ ] les tests tagués `dorevia_ckr_origins` ont été exécutés sur la version cible, ou leur exécution est planifiée dans la présente session

### Commande de test automatisé de référence

```bash
odoo -d tenant_o7 --test-enable --stop-after-init \
  --test-tags=dorevia_ckr_origins --http-port=8076
```

---

## 3. Données de test utilisées

### Origines configurées

* Origine 1 : [ex. Guadeloupe] — slug : [guadeloupe]
* Origine 2 : [ex. Martinique] — slug : [martinique]
* Origine 3 : [facultatif] — slug : [...]

### Produits de test

* Produit A : [nom] — origines : [...]
* Produit B : [nom] — origines : [...]
* Produit C : [nom] — origines : [...]
* Produit multi-origines : [nom] — origines : [...]

---

## 4. Cas de recette

| ID        | Cas de recette                                      | Résultat attendu synthétique                                                              | Couverture auto associée                                                          | Résultat observé | Statut              |
| --------- | --------------------------------------------------- | ----------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | ---------------- | ------------------- |
| **RC-01** | Présence du champ **Origines** sur la fiche produit | champ visible, éditable, multi-valeurs, limité aux valeurs de l’attribut Origine          | `TestCkrOriginPVModel.test_pv_rc01_form_view_contains_origin_field`               | [à compléter]    | [OK / KO / Réserve] |
| **RC-02** | Saisie multi-origines sur un produit                | 2 origines enregistrées, persistance correcte, cohérence de la fiche                      | `test_pv_rc02_ckr_origin_value_ids_multi_inverse`                                 | [à compléter]    | [OK / KO / Réserve] |
| **RC-03** | Gestion des profils `ckr.shop.origin`               | slug contrôlé, unicité correcte, menus et action présents                                 | `test_pv_rc03_*`, `test_pv_rc03_menus_and_action_exist`                           | [à compléter]    | [OK / KO / Réserve] |
| **RC-04** | Alias `/origines`                                   | redirection **301** vers `/shop?ckr_mode=origin`                                          | `TestCkrOriginPVHttp.test_pv_rc04_origines_alias_301`                             | [à compléter]    | [OK / KO / Réserve] |
| **RC-05** | `ckr_mode=origin` seul                              | **200**, catalogue complet, bandeau visible, phrase “Parcourez le catalogue par origine.” | `test_pv_rc05_origin_mode_alone_200_and_copy`, `test_search_detail_origin_only_*` | [à compléter]    | [OK / KO / Réserve] |
| **RC-06** | Une origine valide avec phrase                      | filtre correct, titre dynamique, `context_phrase` affichée                                | `test_pv_rc06_single_origin_with_context_phrase`                                  | [à compléter]    | [OK / KO / Réserve] |
| **RC-07** | Une origine valide sans phrase                      | filtre correct, fallback “Produits issus de {name_visitor}.”                              | `test_pv_rc07_single_origin_without_context_phrase`                               | [à compléter]    | [OK / KO / Réserve] |
| **RC-08** | Plusieurs origines valides                          | logique **OU**, titre “Origines”, phrase plurielle                                        | `test_pv_rc08_multi_origins_or`                                                   | [à compléter]    | [OK / KO / Réserve] |
| **RC-09** | Origine valide sans produit                         | bandeau `empty`, message dédié, rebonds fonctionnels                                      | `test_pv_rc09_empty_state`                                                        | [à compléter]    | [OK / KO / Réserve] |
| **RC-10** | Origine invalide / inconnue                         | redirection **302** vers `/shop` nu, sans paramètres CK                                   | `test_pv_rc10_invalid_slug_302`                                                   | [à compléter]    | [OK / KO / Réserve] |
| **RC-11** | Canonical multi-origines                            | slugs dédupliqués et triés de façon stable                                                | `test_pv_rc11_canonical_sorted_slugs`                                             | [à compléter]    | [OK / KO / Réserve] |
| **RC-12** | Fiche produit côté site                             | bloc **Origines** visible, liens corrects vers `/shop?ckr_mode=origin&ckr_origin=<slug>`  | `test_pv_rc12_product_page_origins_links`                                         | [à compléter]    | [OK / KO / Réserve] |
| **RC-13** | Non-régression autres portes                        | `/kits`, `/promotions`, `/categories`, `/shop` inchangés                                  | `test_pv_rc13_regression_other_gates`                                             | [à compléter]    | [OK / KO / Réserve] |

---

## 5. Contrôles complémentaires recommandés (manuels)

Ces points peuvent être couverts techniquement, mais méritent une validation visuelle / d’usage :

* [ ] lisibilité réelle du bandeau **Origines** sur desktop
* [ ] lisibilité réelle de la variante **empty**
* [ ] compréhension immédiate du champ **Origines** sur la fiche produit back-office
* [ ] cohérence perçue entre :

  * fiche produit back-office,
  * profil `ckr.shop.origin`,
  * fiche produit web,
  * navigation `/shop?ckr_mode=origin`
* [ ] qualité de lecture des liens d’origines sur la fiche produit web
* [ ] absence d’effet de bord visuel sur les autres portes

---

## 6. Exécution des tests automatisés

**Tag exécuté** : `dorevia_ckr_origins`
**Nombre de tests attendus** : `18`
**Résultat** : [à compléter — 18/18 OK, ou détail si échec]
**Base / environnement** : [à compléter]
**Date / heure** : [à compléter]

### Commentaire

[à compléter]

---

## 7. Synthèse des anomalies / réserves

| ID | Sujet         | Gravité                         | Description   | Décision      |
| -- | ------------- | ------------------------------- | ------------- | ------------- |
| A1 | [à compléter] | [Bloquante / Majeure / Mineure] | [à compléter] | [à compléter] |

---

## 8. Conclusion de recette

### Décision

* [ ] **Conforme**
* [ ] **Conforme avec réserves**
* [ ] **Non conforme**

### Commentaire de synthèse

[à compléter]

### Suites à donner

[à compléter]

---

## 9. Validation

**MOA / Recetteur**
Nom : [à compléter]
Date : [à compléter]
Visa : [à compléter]

**Développement / Intégration**
Nom : [à compléter]
Date : [à compléter]
Visa : [à compléter]
