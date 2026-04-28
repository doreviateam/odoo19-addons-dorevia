# PV recette — contrat `/shop` conteneur unique (HTTP / canonical)

**Référence code** : `tests/test_ckr_shop_container_contract.py`  
**Tag Odoo** : `dorevia_ckr_shop_contract`

## Exécution sandbox (preuve 2026-04-27)

| Élément | Valeur |
|--------|--------|
| Base PostgreSQL | `ckr_collections_recette` |
| Conteneur Odoo | `sandbox-odoo19-odoo-1` |
| Port HTTP processus de test | `8070` (le service principal utilise déjà `8069` dans le conteneur) |

**Commande** (depuis l’hôte, avec le conteneur déjà up) :

```bash
docker exec sandbox-odoo19-odoo-1 odoo \
  -c /etc/odoo/odoo.conf \
  -d ckr_collections_recette \
  --test-enable --stop-after-init \
  --test-tags=dorevia_ckr_shop_contract \
  -u dorevia_ckreyol_marketplace \
  --http-port=8070
```

**Résultat attendu** (module ≥ **19.0.1.10.62**) : **31 tests, 0 échec** (les skips ne devraient plus apparaître sur une base neuve après `-u`).

## Jeu de données reproductible (sans shell)

À partir de **19.0.1.10.62**, le fichier `data/ckr_shop_contract_recette_seed_data.xml` complète le démo nominal : **Martinique** + collection **Découverte** + **deux** `product.public.category` (site par défaut) et rattachements `public_categ_ids` sur les fiches vitrine Sélection. Un ``-u dorevia_ckreyol_marketplace`` sur une instance de recette / CI recharge ce jeu.

## Skips acceptables

Sur une base **antérieure** à ce fichier ou sans ``-u``, certains tests peuvent encore se mettre en `skip` si la base ne fournit pas les données minimales. Après chargement du seed versionné, l’objectif est **zéro skip** pour la batterie `dorevia_ckr_shop_contract`.

## Correctifs d’intégration validés (alignés avec cette recette)

- Canonical CK : chemins boutique **localisés** (`…/shop`) via `path.endswith(CKR_CANONICAL_PATH)`.
- Construction de la query canonical : `urllib.parse.urlencode` (robuste, clés répétables dont plusieurs `ckr_mode`).
- Tests : `html.unescape` sur l’`href` du `<link rel="canonical">` avant `parse_qs` (HTML avec `&amp;`).

## Suite éventuelle (hors urgence)

Mini-tour navigateur ciblée : interactions sidebar **Toutes ↔ facettes** (Collections / Origines), en complément du contrat HTTP déjà vert.

## Recette navigateur (comportement UI — après déploiement JS / `-u`)

Vider cache / forcer rechargement des assets si besoin. Vérifier notamment :

1. Sur `/shop`, **Toutes** cochée (Catégories, Collections, Origines).
2. Cocher une origine → **Toutes** origines décochée, URL sur le chemin boutique + `ckr_origin`, pas de navigation « ancienne » exclusive.
3. Cocher une deuxième origine → les deux slugs dans la query (OU).
4. Ajouter une collection → les origines restent dans l’URL (ET entre groupes).
5. Chip **Promotions** → ajoute `ckr_mode=promo` **sans** effacer les facettes sidebar (href généré serveur).
6. Chip **Tout** → chemin boutique nu, tout revient à **Toutes**.
7. Catégories : multi-sélection en **OU** via `ckr_category` répété, sans `/shop/category/…` pour le filtre sidebar.
