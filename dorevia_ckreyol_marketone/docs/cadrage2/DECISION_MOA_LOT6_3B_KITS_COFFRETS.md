# Décision MOA — Lot 6.3b Cadrage Kits & Coffrets

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-06-08 |
| **Lot** | 6.3b — Porte **Kits & Coffrets** |
| **Verdict** | **GO cadrage avec réserves** |
| **Ticket cadrage** | [`TICKET_LOT6_3B_PORTE_KITS_COFFRETS.md`](./TICKET_LOT6_3B_PORTE_KITS_COFFRETS.md) |
| **Fiche réunion** | [`FICHE_MOA_LOT6_3B_KITS_COFFRETS.md`](./FICHE_MOA_LOT6_3B_KITS_COFFRETS.md) |
| **ADR** | [ADR-035](../cadrage/DECISIONS.md#adr-035--activation-product_pack-lot-63b-kits--coffrets) — **Acceptée MOA** |
| **Ticket exécution** | [`TICKET_MARKETONE_LOT6_3B_PORTE_PACK_EXEC.md`](../tickets/lots/TICKET_MARKETONE_LOT6_3B_PORTE_PACK_EXEC.md) — **autorisé** |

---

## Doctrine opposable

```text
Odoo exécute. Marketone habille et oriente.
Aucun moteur Odoo remplacé.
```

---

## Décisions K1–K9

| # | Décision MOA |
|---|--------------|
| **K1** | **`product_pack` activé** dans le manifest Marketone |
| **K2** | **`sale_product_pack` non exigé en v1** |
| **K3** | Filtre porte = **`pack_ok=True` uniquement** |
| **K4** | **Chip header Kits & Coffrets** autorisé (`/kits` → 301) |
| **K5** | Libellé visiteur **« Kits & Coffrets »** confirmé |
| **K6** | Composants = **comportement natif OCA** uniquement · **aucun widget Marketone** |
| **K7** | État vide = message sobre + grille vide *(pattern 6.3a)* |
| **K8** | Non-régression portes **6.1 · 6.2 · 6.3a** + smoke panier **obligatoire** |
| **K9** | **ADR-035** rédigée et acceptée |

---

## Réserve MOA

La **v1 Lot 6.3b** ne couvre **pas** l’explosion composants **vente / stock / préparation / facturation** via `sale_product_pack`, module **non installable** Odoo 19 au stade actuel.

**Report** : ticket OCA / backend séparé — [`TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md`](../tickets/maintenance/TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md).

Cette réserve **n’empêche pas** le GO exécution de la porte front catalogue.

---

## Suite Dev

1. Implémentation `19.0.18.0.0` selon ticket exécution
2. Prep recette · recette manuelle · tests auto `dorevia_marketone_lot6_3b_pack`
3. Clôture MOA après recette navigateur signée
