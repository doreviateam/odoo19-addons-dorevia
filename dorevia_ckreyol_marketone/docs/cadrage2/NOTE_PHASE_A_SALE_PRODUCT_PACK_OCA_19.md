# Note Phase A — Port OCA `sale_product_pack` Odoo 19 CE

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-06-08 |
| **Ticket** | [`TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md`](../tickets/maintenance/TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md) |
| **Diagnostic amont** | [`DIAGNOSTIC_MOA_SALE_PRODUCT_PACK_19.md`](./DIAGNOSTIC_MOA_SALE_PRODUCT_PACK_19.md) |
| **Branche Dev OCA** | `odoo19-addons-oca` · `dev/phase-a-oca-sale-product-pack-19` · commit `e8c603b` |
| **Verdict Phase A** | **GO technique partiel MOA** (2026-06-08) — voir § Verdict MOA |

---

## Doctrine (inchangée)

```text
Odoo exécute. Marketone habille et oriente.
Aucun moteur Odoo remplacé.
```

**Aucune modification** de `dorevia_ckreyol_marketone` · **aucun** `depends` Marketone sur `sale_product_pack`.

---

## 1. PR / commits importés

| Module | Source | PR OCA | Commit / révision | État upstream |
|--------|--------|--------|-------------------|---------------|
| `sale_product_pack` | [OCA/product-pack](https://github.com/OCA/product-pack) branche **19.0** | **#244** merged | `0e7fdaa` (HEAD 19.0 post-merge) | **Mergé** 2026-05-06 |
| `stock_product_pack` | OCA **19.0** | **#227** merged | `0e7fdaa` | **Mergé** 2026-06-03 |
| `sale_stock_product_pack` | branche `19.0-mig-sale_stock_product_pack` (adhoc-dev fork) | **#230** ouverte | `e784280` | **Non mergé** · approved |
| `website_sale_product_pack` | — | **#229** ouverte | `37e3dd1` | **Non importé** Phase A |

**Commit Dorevia** (branche `dev/phase-a-oca-sale-product-pack-19`) :

```text
e8c603b — Sync OCA product-pack 19.0 migrated modules (Phase A)
```

---

## 2. Statut installation (sandbox Odoo 19.0-20260324)

### Base `ckr-marketone-01` (Marketone installé)

| Module | État après `-i` | Version |
|--------|-----------------|---------|
| `sale_product_pack` | **installed** | `19.0.1.0.0` |
| `stock_product_pack` | **installed** | `19.0.1.0.0` |
| `sale_stock_product_pack` | **installed** | `19.0.1.0.0` |
| `product_pack` | installed (inchangé) | `19.0.1.0.2` |

**Dépendances tirées** : `sale_stock`, `stock_delivery`, `website_sale_stock`, `website_sale_stock_wishlist` (déjà présents ou installés en cascade).

### Base dédiée `oca-pack-phase-a-01` (sans Marketone)

Chaîne installée **sans demo** — usage tests OCA isolés.

---

## 3. Résultats tests OCA

Commande :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d oca-pack-phase-a-01 \
  --test-tags=sale_product_pack,stock_product_pack,sale_stock_product_pack \
  --stop-after-init --http-port=0
```

| Module | Base | Résultat |
|--------|------|----------|
| `stock_product_pack` | `oca-pack-phase-a-01` | **2/2 OK** |
| `sale_stock_product_pack` | `oca-pack-phase-a-01` | **1/1 OK** (`test_delivered_quantities`) |
| `sale_product_pack` | `oca-pack-phase-a-01` | **ERREUR setUpClass** — `res_company.security_lead` NOT NULL |
| `sale_product_pack` | `ckr-marketone-01` | **ERREUR setUpClass** — `product_template.publish_date` NOT NULL (contrainte Marketone) |

**Analyse échec `sale_product_pack` tests** :

- Hérite de `product_pack.tests.common` qui crée une 2ᵉ société sans champs requis Odoo 19 (`security_lead`).
- Sur `ckr-marketone-01`, contraintes **Marketone** (`publish_date` obligatoire) bloquent aussi la création produits test OCA.
- **Ce n’est pas un échec d’installation module** — le code charge et fonctionne en shell.

### Non-régression Marketone (sans modification module)

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d ckr-marketone-01 \
  --test-tags=dorevia_marketone_lot6_3b_pack --stop-after-init --http-port=0
```

**13/13 OK** — avec `sale_product_pack` + chaîne stock **installés** sur la même base.

---

## 4. Comportement fonctionnel vérifié (shell `ckr-marketone-01`)

| Scénario | Lignes SO | Verdict |
|----------|-----------|---------|
| Pack **detailed** + composant (création test) | **2** (pack + composant) | **Explosion OK** |
| Pack recette **7** (`non_detailed`, config 6.3b) | **1** (pack seul) | **Comportement OCA attendu** |

→ **`sale_product_pack` installé ne change pas** le panier / SO v1 tant que les packs restent `non_detailed`.

---

## 5. Écarts restants

| # | Écart | Gravité | Traitement Phase B |
|---|-------|---------|------------------|
| E1 | PR **#230** `sale_stock_product_pack` non mergée upstream | Moyenne | Pinner `e784280` ou attendre merge OCA |
| E2 | Tests OCA `sale_product_pack` — setUpClass société | Faible | Patch OCA / override test local · ou base dédiée + fix `product_pack` common |
| E3 | Tests OCA sur `ckr-marketone-01` — contraintes Marketone BO | Info | Recette BO dédiée · pas les tests OCA bruts |
| E4 | `website_sale_product_pack` (#229) absent | Info | Phase B si packs **detailed** + checkout eCommerce |
| E5 | Config packs CK = `non_detailed` | **Fonctionnel** | Décision MOA Phase B obligatoire pour explosion composants |

---

## 6. Évaluation `website_sale_product_pack` (#229)

| Critère | Conclusion |
|---------|------------|
| Nécessaire pour chaîne BO vente/stock | **Non** |
| Nécessaire si checkout eCommerce + packs **detailed** | **Oui** — gère contextes `update_prices` / expansion lignes panier |
| Phase A | **Non importé** — PR ouverte · CI unstable |
| Impact front 6.3b (`non_detailed`) | **Aucun** attendu sans changement config produit |

---

## 7. Recommandation MOA — Phase B

| Option | Recommandation MOA |
|--------|-------------------|
| **B0 — Rester `non_detailed`** + modules installés | **Insuffisant** pour l’objectif « explosion composants vente/stock/prépa/facture » — chaîne active mais **1 ligne SO** |
| **B1 — Passer packs CK en `detailed`** + `pack_component_price` `totalized` ou `ignored` | **Recommandé** si MOA valide recette BO + impact visuel lignes commande |
| **B2 — Attendre merge OCA #230** (et #229 si eCommerce) | **Prudent** pour prod · Phase A prouve installabilité |
| **B3 — Module pont Dorevia minimal** | **Non requis Phase A** · réévaluer seulement si écart eCommerce post-#229 |
| **Activation prod** | **NO GO** — Phase B recette MOA + décision ADR-035 amendement si activation explicite |

**Verdict Phase A** : **GO MOA** — preuve d’installabilité Odoo 19 CE · tests stock OK · explosion **detailed** validée en shell · **non-régression 6.3b OK** · **activation prod NO GO**.

**PR plateforme MOA** : https://github.com/doreviateam/odoo19-addons-oca/pull/1

**Suite MOA (2026-06-08)** :

- **GO PR interne** `odoo19-addons-oca` branche `dev/phase-a-oca-sale-product-pack-19`
- **GO atelier Phase B** — [`ATELIER_MOA_PHASE_B_SALE_PRODUCT_PACK.md`](./ATELIER_MOA_PHASE_B_SALE_PRODUCT_PACK.md)
- **GO préparation recette BO** — [`PREP_RECETTE_PHASE_B_SALE_PRODUCT_PACK_BO.md`](./PREP_RECETTE_PHASE_B_SALE_PRODUCT_PACK_BO.md)

**Suite Dev suggérée** :

1. Merger / PR `odoo19-addons-oca` branche `dev/phase-a-oca-sale-product-pack-19` (sans toucher Marketone).
2. Atelier MOA Phase B : `non_detailed` vs `detailed` + périmètre #229.
3. Recette BO pack **7**/**8** : commande → picking → facture (pack detailed test).
4. Documenter amendement ADR-035 si activation prod actée.

---

## Références

- Branche : `doreviateam/odoo19-addons-oca` · `dev/phase-a-oca-sale-product-pack-19`
- [OCA/product-pack #222](https://github.com/OCA/product-pack/issues/222) — migration 19.0
- [PR #244](https://github.com/OCA/product-pack/pull/244) · [PR #227](https://github.com/OCA/product-pack/pull/227) · [PR #230](https://github.com/OCA/product-pack/pull/230) · [PR #229](https://github.com/OCA/product-pack/pull/229)
