# Recette manuelle — Lot 5 (panier / checkout smoke)

| Champ | Valeur |
|-------|--------|
| **Lot** | 5 — Panier / checkout smoke |
| **Module** | `dorevia_ckreyol_marketone` **`19.0.5.0.0`** |
| **Base** | `ckr-marketone-01` — http://localhost:18079 |
| **Durée indicative** | 20–25 min |
| **Ticket** | [`TICKET_MARKETONE_LOT5_CART_CHECKOUT.md`](../tickets/TICKET_MARKETONE_LOT5_CART_CHECKOUT.md) |

---

## Avant de commencer

- [ ] Session **invité** (navigation privée), panier vidé
- [ ] Produit de référence : Crackers manioc Sainte-Anne — http://localhost:18079/shop/crackers-manioc-sainte-anne-8
- [ ] Mobile ~375 px + desktop

**Note Odoo 19 CE** : `/shop/checkout` redirige souvent vers **`/shop/address`** pour un invité sans adresse — c’est la **première étape checkout** standard (pas une anomalie).

---

## Parcours MOA

| # | Test | Attendu | OK | KO |
|---|------|---------|----|----|
| L5-01 | Ajout depuis fiche | CTA → produit dans le panier | ☑ | ☐ |
| L5-02 | `/shop/cart` | 200, lignes visibles, prix €, `marketone-cart` (body ou #wrap) | ☑ | ☐ |
| L5-03 | Modifier quantité | Mise à jour sans 500 | ☑ | ☐ |
| L5-04 | Supprimer ligne | Ligne retirée | ☑ | ☐ |
| L5-05 | Retour `/shop` | 200, `marketone-shop` intact | ☑ | ☐ |
| L5-06 | Checkout invité | `/shop/checkout` → `/shop/address` (ou checkout) 200, `marketone-checkout` | ☑ | ☐ |
| L5-07 | Pas `marketone-cart` au checkout | Scope checkout seul | ☑ | ☐ |
| L5-08 | Non-régression `/` | `marketone-root` OK | ☑ | ☐ |
| L5-09 | Non-régression fiche | `marketone-product` OK | ☑ | ☐ |
| L5-10 | Mobile 375 px | Panier + checkout sans scroll horizontal | ☑ | ☐ |

---

## Tests auto

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone \
  --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_smoke,dorevia_marketone_lot2,dorevia_marketone_lot2_1,dorevia_marketone_lot3,dorevia_marketone_lot4,dorevia_marketone_lot5 \
  --http-port=8071
```

**Attendu** : `0 failed, 0 error(s)` (49 tests).

---

## Verdict MOA

| Décision | ☐ |
|----------|---|
| **GO** | ☑ |
| **GO avec réserves** | |
| **NO GO** | |

**Date** : 2026-05-18 · **Validé par** : MOA

**Réserve non bloquante** : compteur panier à `3` sur certaines captures (test modification quantité) — pas une anomalie.
