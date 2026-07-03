# Retour Dev — Note 11 · CATALOG-ARCHI-001 Lot C · Vérification technique de l'approche

| Champ | Valeur |
| --- | --- |
| Date | 3 juillet 2026 |
| Référence | [`note_11.md`](note_11.md) |
| Statut | Analyse technique — **toujours NO GO code**, cette note ne fait que vérifier la faisabilité de la matrice avant validation finale |
| Module cible | `dorevia_ck_marketone_content` (controllers/website_sale.py, sitemap) |

---

## Synthèse

La matrice de la note 11 est **techniquement faisable telle quelle**, avec deux précisions qui réduisent le risque/effort estimé au Lot B pour le point noindex, et une confirmation du point de vigilance principal (surcharge contrôleur).

## 1. Route catégorie — point d'accroche confirmé

La route standard Odoo (`website_sale/controllers/main.py`, méthode `shop()`) résout la catégorie **dès la première ligne utile** :

```python
category = self._validate_and_get_category(category)
```

C'est exactement le point d'insertion pour la matrice statut → 200/302/404 : le contrôleur CK doit **redéclarer la route** `shop()` (pas juste étendre `_get_additional_shop_values` comme aujourd'hui) pour intercepter `category` avant le reste du traitement et retourner `request.redirect(...)` ou lever un 404 selon `ck_exposure_status`. Confirme le Risque 3 de la note (surcharge du contrôleur) — il faut isoler cette décision dans un helper pur (`ck_category_route_action(category)` par ex.) et garder `shop()` lui-même minimal.

## 2. Sitemap — mécanisme identifié précisément

Le sitemap des catégories est généré par une fonction `sitemap_shop(env, rule, qs)` passée en paramètre `sitemap=` du décorateur `@route` de `shop()`. Elle énumère **toutes** les catégories du domaine site sans aucun filtre d'exposabilité :

```python
for cat in Category.search(dom):
    ...
    yield {'loc': loc}
```

Pour appliquer la règle "hors sitemap si non actif/exposable", le contrôleur CK doit fournir **sa propre fonction `sitemap=`** en redéclarant la route (même contrainte que le point 1 — les deux se résolvent dans la même redéclaration de route, pas un surcoût séparé).

## 3. Noindex — mécanisme partiellement réutilisable (correction de l'estimation Lot A/note_10_reponse)

Bonne nouvelle : `website.layout` a **déjà** un mécanisme `noindex` générique :

```xml
<t t-set="no_index" t-value="
    (main_object and 'website_indexed' in main_object and not main_object.sudo().website_indexed)
    ..."/>
<meta t-if="no_index" name="robots" content="noindex"/>
```

Mais il est conditionné à un champ `website_indexed`, qui existe sur `website.page` (et `theme.website.page`) — **pas** sur `product.public.category` (celle-ci hérite de `website.seo.metadata`, qui ne porte pas ce champ). Deux options :

* (a) ajouter un champ `website_indexed`-like sur `product.public.category` pour que le mécanisme générique s'applique tel quel ;
* (b) rendre directement `<meta name="robots" content="noindex"/>` dans un template CK dédié, conditionné à `ck_exposure_status`/`_is_ck_exposable()`, sans dépendre du mécanisme générique.

Recommandation : (a) est plus sobre et cohérente avec le standard Odoo (un seul point de vérité, réutilisable ailleurs) — **corrige à la baisse** l'estimation du Lot C portée par le ticket actuel ("aucun équivalent existant à créer" → en réalité juste un champ à ajouter + brancher `main_object`).

## 4. Aucune correction sur les points 4 à 7 de la note

La matrice de redirections, le champ `ck_replacement_category_id`, les tests QA et les risques/rollback proposés sont cohérents avec l'architecture actuelle et n'appellent pas d'amendement technique.

## Conclusion

```text
Note 11 — approche techniquement validée
→ Route + sitemap : une seule redéclaration de route dans CkWebsiteSaleController
→ Noindex : moins coûteux que prévu (champ + branchement main_object, pas un mécanisme à créer de zéro)
→ Toujours NO GO code — en attente du GO MOA sur la matrice V1
```
