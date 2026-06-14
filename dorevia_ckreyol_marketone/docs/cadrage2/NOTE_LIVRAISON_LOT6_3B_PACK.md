# NOTE_LIVRAISON — Lot 6.3b Porte Kits & Coffrets · `19.0.18.0.0`

| Champ | Valeur |
|-------|--------|
| **Version** | `19.0.18.0.0` |
| **ADR** | ADR-034 · ADR-035 |
| **Contrat** | C3.E |
| **Décision MOA** | [`DECISION_MOA_LOT6_3B_KITS_COFFRETS.md`](./DECISION_MOA_LOT6_3B_KITS_COFFRETS.md) |
| **Ticket exécution** | [`TICKET_MARKETONE_LOT6_3B_PORTE_PACK_EXEC.md`](../tickets/lots/TICKET_MARKETONE_LOT6_3B_PORTE_PACK_EXEC.md) |
| **Recette** | [`RECETTE_MANUELLE_LOT6_3B_PACK.md`](../recette/lots/RECETTE_MANUELLE_LOT6_3B_PACK.md) — **GO clôture MOA** (2026-06-08) |
| **Préparation base** | [`PREP_RECETTE_LOT6_3B_PACK.md`](./PREP_RECETTE_LOT6_3B_PACK.md) |
| **Réception MOA** | [`RECEPTION_MOA_LOT6_3B_PACK.md`](./RECEPTION_MOA_LOT6_3B_PACK.md) — **GO clôture MOA** (2026-06-08) |

---

## En-tête recette (cadrage2)

**ADR-034 :** [`ARBITRAGE_ARCHITECTURE_CADRAGE2.md`](./ARBITRAGE_ARCHITECTURE_CADRAGE2.md)

**Fonctionnalité Odoo native préservée :** Produits pack · Listes de prix · Vente eCommerce

**Mécanisme Odoo concerné :** `product.template.pack_ok` · `product_pack` / `product.pack.line` · `website_sale`

**Non-régression référence boutique :** [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md) — B1 · B2 · B3 · B4 · B6 · B7

---

## Livrables Dev

| Couche | Détail |
|--------|--------|
| Manifest | `product_pack` · version `19.0.18.0.0` |
| Modèle | `product.template._search_get_detail` — branche `marketone_pack_only` |
| Contrôleur | Mode `pack` · alias `/kits` → 301 · priorité C3.4 |
| QWeb | `views/pages/shop_pack.xml` · chip header `header.xml` |
| Styles | `static/src/scss/_shop_pack.scss` |
| Tests | `dorevia_marketone_lot6_3b_pack` — **13/13 OK** |
| Script recette | `scripts/prep_recette_lot6_3b_pack.py` |

---

## Note de livraison (phrase obligatoire)

> **Aucun moteur Odoo remplacé** — les kits et coffrets s'appuient sur `product_pack` (`pack_ok`, composants natifs) et les listes de prix Odoo. Marketone présente et filtre la grille `/shop` uniquement.

---

## Réserve MOA (maintenue)

Explosion composants vente / stock / préparation / facturation — **hors v1** — [`TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md`](../tickets/maintenance/TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md).

---

## Tests automatisés (sandbox)

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d ckr-marketone-01 \
  --test-tags=dorevia_marketone_lot6_3b_pack \
  --stop-after-init --http-port=0
```

Non-régression :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d ckr-marketone-01 \
  --test-tags=dorevia_marketone_lot6_3a_promo,dorevia_marketone_lot6_1_featured,dorevia_marketone_lot6_2_origin,dorevia_marketone_lot3,dorevia_marketone_lot5 \
  --stop-after-init --http-port=0
```

---

## Statut

**Livré Dev** — **GO clôture MOA** (2026-06-08).
