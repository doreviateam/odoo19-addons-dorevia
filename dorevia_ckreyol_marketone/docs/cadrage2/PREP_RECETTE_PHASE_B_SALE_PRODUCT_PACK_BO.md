# Préparation base — Recette BO Phase B `sale_product_pack`

| Champ | Valeur |
|-------|--------|
| **Base** | `ckr-marketone-01` |
| **URL BO** | http://localhost:18079/web |
| **Prérequis plateforme** | PR `odoo19-addons-oca` Phase A mergée · chaîne `sale_product_pack` / `stock_product_pack` / `sale_stock_product_pack` **installée** |
| **Atelier MOA** | [`ATELIER_MOA_PHASE_B_SALE_PRODUCT_PACK.md`](./ATELIER_MOA_PHASE_B_SALE_PRODUCT_PACK.md) |
| **Recette** | [`RECETTE_MANUELLE_PHASE_B_SALE_PRODUCT_PACK_BO.md`](../recette/maintenance/RECETTE_MANUELLE_PHASE_B_SALE_PRODUCT_PACK_BO.md) |
| **Statut** | **Prep exécutée** — merge PR #1 · modules installés · pack 7/8 configurés |
| **Décision MOA** | [`DECISION_MOA_PHASE_B_SALE_PRODUCT_PACK.md`](./DECISION_MOA_PHASE_B_SALE_PRODUCT_PACK.md) |

---

## Jeu de données MOA (2026-06-08)

| Rôle | Produit | ID template | Config Phase B |
|------|---------|-------------|----------------|
| **Pack pilote** | Maniocookies salés La Platine | **7** | `detailed` · `pack_component_price=ignored` |
| **Témoin pack** | Crackers manioc Sainte-Anne | **8** | `non_detailed` · `ignored` *(config 6.3b)* |
| **Témoin unitaire** | Pâtes de manioc Mayotte | **9** | `pack_ok=False` |

> **Accès sandbox** : base **`ckr-marketone-01`** via `/web/login`.

---

## Préparation BO (config MOA signée)

### Pack pilote **7** en `detailed` · pack **8** témoin `non_detailed`

```bash
# 1. Rejouer prep 6.3b (non_detailed par défaut sur 7 et 8)
docker exec -i sandbox-odoo19-odoo-1 odoo shell -d ckr-marketone-01 --no-http \
  < odoo19-addons-dorevia/dorevia_ckreyol_marketone/scripts/prep_recette_lot6_3b_pack.py

# 2. Basculer pack pilote 7 en detailed (MOA Phase B)
docker exec -i sandbox-odoo19-odoo-1 odoo shell -d ckr-marketone-01 --no-http <<'PY'
pack7 = env['product.template'].browse(7)
pack7.write({'pack_type': 'detailed', 'pack_component_price': 'ignored'})
for line in pack7.pack_line_ids:
    if line.product_id.type == 'consu':
        line.product_id.is_storable = True
# Pack 8 reste non_detailed (témoin)
pack8 = env['product.template'].browse(8)
print(f"pack 7: {pack7.pack_type} / {pack7.pack_component_price}")
print(f"pack 8: {pack8.pack_type} / {pack8.pack_component_price}")
env.cr.commit()
PY
```

### Vérifier modules installés

```bash
docker exec -i sandbox-odoo19-odoo-1 odoo shell -d ckr-marketone-01 --no-http <<'PY'
for n in ['sale_product_pack','stock_product_pack','sale_stock_product_pack']:
    m = env['ir.module.module'].search([('name','=',n)])
    print(n, m.state)
PY
```

---

## Scénarios recette BO (grille)

| # | Processus | Action | Attendu |
|---|-----------|--------|---------|
| **B1** | Commande | Devis · ajouter pack **7** × 1 | Lignes SO = pack + composants *(si detailed)* |
| **B2** | Confirmation | Confirmer commande | État `sale` · pas d’erreur |
| **B3** | Stock | Vérifier picking / moves | Moves sur **composants** stockables *(si detailed + stock)* |
| **B4** | Préparation | Valider picking | Qté livrée composants OK |
| **B5** | Facturation | Facturer selon politique | Lignes facture cohérentes · pas de double comptage |
| **B6** | Non-régression front | `/shop?marketone_mode=pack` | Porte 6.3b inchangée *(smoke)* |

---

## Restauration après recette

```bash
docker exec -i sandbox-odoo19-odoo-1 odoo shell -d ckr-marketone-01 --no-http \
  < odoo19-addons-dorevia/dorevia_ckreyol_marketone/scripts/prep_recette_lot6_3b_pack.py
```

Remet `non_detailed` + `ignored` sur packs **7**/**8** (config 6.3b clôturée).

---

## Références

- Phase A : [`NOTE_PHASE_A_SALE_PRODUCT_PACK_OCA_19.md`](./NOTE_PHASE_A_SALE_PRODUCT_PACK_OCA_19.md)
- Prep 6.3b : [`PREP_RECETTE_LOT6_3B_PACK.md`](./PREP_RECETTE_LOT6_3B_PACK.md)
