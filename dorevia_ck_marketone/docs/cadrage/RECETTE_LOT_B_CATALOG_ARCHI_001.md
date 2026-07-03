# Recette Dev — Lot B CATALOG-ARCHI-001 (qualification produits + cards)

| Champ | Valeur |
| --- | --- |
| Date | 3 juillet 2026 |
| Référence | [`TICKET_DEV_CATALOG_ARCHI_001.md`](TICKET_DEV_CATALOG_ARCHI_001.md) — Lot B |
| Module | `dorevia_ck_marketone_content` v19.0.1.84.0 |
| Statut | Vérifié sur sandbox `dorevia_ck_marketone_01` (module upgrade réel + suite de tests + rendu HTTP réel) |

## Bugs trouvés et corrigés pendant l'implémentation

### BUG-B1 — origine avec repli étiquette géographique restauré

**Constat** : la première version de `_is_ck_qualified_for_public_exposure()` ne
testait que l'attribut produit « Origines » (`ck_origin_from_attribute`), sans
le repli par étiquette géographique (Option A) déjà utilisé par la ligne meta
des cards. Conséquence : « Confiture de goyave » (origine portée par le tag
« Guadeloupe », pas par un attribut) était disqualifiée à tort de la curation
Home — une régression métier, la doctrine CK ayant déjà posé ce repli comme
garde-fou contre les faux négatifs.

**Correctif** : réutilisation de `_get_featured_origin_and_tag_parts()` (la
même résolution que celle qui alimente la card) au lieu du seul attribut.
Fichier : `models/product_template.py`, méthode `_is_ck_qualified_for_public_exposure`.

**Vérification** : `Confiture de goyave → qualified: True` (confirmé par script
direct sur la base réelle après correctif).

### BUG-B2 — fixtures `test_ck_home_section3_curation.py` enrichies

**Constat** : le branchement de la qualification sur `get_curated_featured_variants()`
a fait échouer 14 tests pré-existants de ce fichier, dont les fixtures
(`_make_product`) ne posaient ni catégorie ni producteur — non testé jusqu'ici
car non pertinent avant ce lot.

**Correctif retenu** : enrichir le helper de fixture partagé (`_make_product`)
avec une catégorie et un producteur de test par défaut, plutôt que d'affaiblir
la règle de qualification. 4 tests qui vérifient le contenu **exact** de la
ligne meta (déjà qualifiés par un tag géographique) désactivent explicitement
le producteur par défaut (`ck_producer_id=False`) pour ne pas voir apparaître
un segment producteur non attendu dans leur assertion. Un test
(`test_category_removal_does_not_unfeature_home`) a reçu une seconde catégorie
permanente pour que son scénario (retrait d'UNE catégorie) reste valide sans
laisser le produit sans catégorie du tout.

### BUG-B3 — fixtures partagées Lot2/Section3 enrichies

**Constat** : même symptôme sur 2 autres fichiers partageant des helpers
distincts : `tests/ck_home_lot2_utils.py` (`ensure_featured_catalog`, utilisé
par `TestCkHomeLot2Compose`/`TestCkHomeLot2Hooks`/`TestCkHomeLot1Hooks` etc.)
et `tests/test_ck_home_section3_featured_field.py` (son propre `_make_product`).

**Correctif** : même principe — catégorie + producteur de test ajoutés aux
deux helpers.

## Points de contrôle demandés avant commit — tous vérifiés sur rendu réel

| Point | Résultat |
| --- | --- |
| Home vedettes : pas de perte involontaire de produits qualifiés | Confiture de goyave, Manio Crackers, Savon vétiver, Tambour Gro Ka restent qualifiés ; seul Chapeau Panama est exclu (volontaire, cf. ci-dessous) |
| Shop cards : ligne meta stable alimentaire/coffret/artisanat | Vérifié en direct sur `/shop` : `Guadeloupe · Komla · 320 g · 17,19 €/kg` (alimentaire), `Dominique (Ile) · Rwan Ltd · Bio · 125 g · 50,40 €/kg` (soin), `Martinique · 1 l · 5,00 €/l` (boisson) — formats §10 respectés, producteur désormais présent |
| Catégorie Épicerie : Confiture toujours visible | Confirmé — présente sur `/shop/category/epicerie-1` (HTTP 200) |
| Orphelins : Coffret signalé sans masquage brutal | `Coffret découverte créole` : `ck_is_orphan=True`, `is_published=True`, `sale_ok=True`, toujours présent sur `/shop` |
| Qualification : Chapeau Panama non-qualifié sans effet de bord sur /shop | `_is_ck_qualified_for_public_exposure() = False`, card rendue normalement sur `/shop`, lien produit fonctionnel |

## Point non corrigé (hors périmètre Dev, déjà acté au Lot A)

Constaté en direct sur `/shop` : un produit (Pâte de manioc) affiche encore
`Guadeloupe · Bien-être · Sans Gluten · 1 kg · 3,95 €/kg` — confirme en
conditions réelles le problème de catégorisation signalé au §9 de la note
CK-CATALOG-ARCHI-001. Reste une **correction de données BO/QA**, hors scope
Dev (cf. `note_10_reponse.md` §2.4).

## Suite de tests

Suite complète exécutée plusieurs fois (upgrade réel + `--test-enable`).
Après correctifs BUG-B1/B2/B3 : aucune régression réelle restante. Le run
complet exhibe une instabilité d'infrastructure préexistante et indépendante
du code (`psycopg2.errors.SerializationFailure: could not serialize access
due to concurrent update` sur la vue Home, réécrite très fréquemment par les
tests ; timeouts HTTP sous charge prolongée) — confirmée par isolation
répétée : les mêmes classes de tests passent à 100 % lorsqu'exécutées seules,
juste après un run complet qui les montrait en échec.

## Verdict

```text
Lot B — GO commit
→ BUG-B1/B2/B3 corrigés et documentés
→ 5 points de contrôle vérifiés sur rendu réel
→ pas de changement de doctrine
→ point catégorisation Pâte de manioc confirmé, toujours hors scope Dev
```
