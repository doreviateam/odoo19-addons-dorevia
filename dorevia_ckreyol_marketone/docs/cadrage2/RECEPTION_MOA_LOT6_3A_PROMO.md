# Réception MOA — Lot 6.3a Porte Promotions `19.0.17.0.0`

| Champ | Valeur |
|-------|--------|
| **Version** | `19.0.17.0.0` |
| **Date réception** | 2026-06-08 |
| **Date clôture** | 2026-06-08 |
| **Cadrage** | [`TICKET_LOT6_3_PORTE_PROMO_PACK.md`](./TICKET_LOT6_3_PORTE_PROMO_PACK.md) — GO MOA |
| **Ticket exécution** | [`TICKET_MARKETONE_LOT6_3A_PORTE_PROMO_EXEC.md`](../tickets/lots/TICKET_MARKETONE_LOT6_3A_PORTE_PROMO_EXEC.md) |
| **Livraison Dev** | [`NOTE_LIVRAISON_LOT6_3A_PROMO.md`](./NOTE_LIVRAISON_LOT6_3A_PROMO.md) |
| **Recette manuelle** | [`RECETTE_MANUELLE_LOT6_3A_PROMO.md`](../recette/lots/RECETTE_MANUELLE_LOT6_3A_PROMO.md) |
| **Préparation base** | [`PREP_RECETTE_LOT6_3A_PROMO.md`](./PREP_RECETTE_LOT6_3A_PROMO.md) |
| **Verdict livraison** | **Reçu — GO recette architecture + GO recette navigateur** |
| **Verdict grille P1–R4** | **Signée — GO** (2026-06-08) |
| **Clôture lot** | **GO MOA** (2026-06-08) |

---

## Réponse MOA

Lot `19.0.17.0.0` **clôturé GO MOA**.

```text
Odoo exécute. Marketone habille et oriente.
Aucun moteur Odoo remplacé.
```

### Points validés

| Point | Verdict |
|-------|---------|
| Source vérité promo = `product.pricelist` / `product.pricelist.item` | ✓ |
| Pricelist courante visiteur (M7) | ✓ |
| Pas de `product_pack` · `website_blog` · `website_forum` | ✓ |
| Alias `/promotions` → **301** → `/shop?marketone_mode=promo` | ✓ |
| Chip header **Promotions** · pas de `/kits` | ✓ |
| Prix affiché / calculé par Odoo — Marketone filtre et oriente | ✓ |
| En-tête recette ADR-034 obligatoire | ✓ |

### Tests automatisés (MOA)

| Suite | Résultat |
|-------|----------|
| `dorevia_marketone_lot6_3a_promo` | **18/18 OK** |
| `dorevia_marketone_lot3` + `dorevia_marketone_lot5` | **23/23 OK** |

---

## Clôture recette navigateur (2026-06-08)

Recette exécutée et signée sur `ckr-marketone-01` — détail : [`RECETTE_MANUELLE_LOT6_3A_PROMO.md`](../recette/lots/RECETTE_MANUELLE_LOT6_3A_PROMO.md) § Signature MOA.

| Zone | Résultat |
|------|----------|
| P1–P6 · P8 | **Validé** |
| P7 multi-pricelist | **S/O** — une seule pricelist active (`Default`, id 3) |
| N1–N3 | **Validé** |
| R1–R4 | **Validé** — smoke `/shop`, facettes, images, panier/checkout |

### Contrôles clés MOA

- Porte promo : **Maniocookies** + **Crackers** uniquement · **Pâtes de manioc Mayotte** absente en mode normal
- P4 état vide : items 39/40 expirés temporairement → message + grille vide
- P6 promo globale : item 41 activé temporairement → catalogue complet
- **État base restauré** : items 39/40 actifs · item 41 expiré (`2026-06-07 14:26:53`)

---

## Réserves et hors périmètre

| Sujet | Traitement |
|-------|------------|
| Échec isolé lot 6.2 (`test_origin_mode_alone_full_catalog`) | **Hors clôture 6.3a** — aucun impact constaté en recette navigateur |
| Lot **6.3b** Kits & Coffrets | **Hors périmètre** — cadrage séparé `product_pack` |
| P7 multi-pricelist | **S/O** sur base recette — non bloquant clôture |

---

## Verdict final

| Date | Verdict |
|------|---------|
| 2026-06-08 | ☑ **GO recette architecture** · ☑ **GO recette navigateur** · ☑ **GO clôture MOA** |

**Note livraison opposable** : *Aucun moteur Odoo remplacé.*

---

## Suite

- Lot **6.3b Kits & Coffrets** — **GO clôture MOA** [`RECEPTION_MOA_LOT6_3B_PACK.md`](./RECEPTION_MOA_LOT6_3B_PACK.md) · contrat **C3.E**
- Reprise progressive autres lots front gelés — [`REPRISE_LOTS_FRONT_CADRAGE2.md`](./REPRISE_LOTS_FRONT_CADRAGE2.md)
