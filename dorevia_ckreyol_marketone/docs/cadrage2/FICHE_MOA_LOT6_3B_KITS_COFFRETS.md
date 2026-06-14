# Fiche MOA — Arbitrage Lot 6.3b Kits & Coffrets

| Champ | Valeur |
|-------|--------|
| **Date réunion** | 2026-06-08 |
| **Lot** | 6.3b — Porte **Kits & Coffrets** |
| **Verdict** | **GO cadrage avec réserves** |
| **Décision** | [`DECISION_MOA_LOT6_3B_KITS_COFFRETS.md`](./DECISION_MOA_LOT6_3B_KITS_COFFRETS.md) |
| **Ticket cadrage** | [`TICKET_LOT6_3B_PORTE_KITS_COFFRETS.md`](./TICKET_LOT6_3B_PORTE_KITS_COFFRETS.md) |
| **Ticket exécution** | [`TICKET_MARKETONE_LOT6_3B_PORTE_PACK_EXEC.md`](../tickets/lots/TICKET_MARKETONE_LOT6_3B_PORTE_PACK_EXEC.md) |

---

## Doctrine opposable

```text
Odoo exécute. Marketone habille et oriente.
Aucun moteur Odoo remplacé.
```

---

## K1–K9 — verdict MOA

| # | Décision | Verdict |
|---|----------|---------|
| **K1** | `product_pack` activé | ☑ **Oui** |
| **K2** | `sale_product_pack` non exigé en v1 | ☑ **Non en v1** |
| **K3** | Filtre `pack_ok=True` uniquement | ☑ **Validé** |
| **K4** | Chip header Kits & Coffrets | ☑ **Oui** |
| **K5** | Libellé « Kits & Coffrets » | ☑ **Validé** |
| **K6** | Composants natif OCA · aucun widget Marketone | ☑ **Validé** |
| **K7** | État vide porte | ☑ **Validé** |
| **K8** | Non-régression portes + panier | ☑ **Validé** |
| **K9** | ADR-035 | ☑ **Acceptée** |

---

## Impacts métier — MOA

| Zone | Verdict |
|------|---------|
| Vente panier 1 ligne pack | ☑ **OK** |
| Prix pricelist Odoo | ☑ **OK** |
| Stock comportement standard | ☑ **OK** |
| Préparation coffret unité visuelle | ☑ **OK** |
| Facturation alignée OCA | ☑ **OK** |
| BO 2–4 coffrets pilote `pack_ok` | ☑ **OK** |

---

## Réserve MOA

La **v1** ne couvre **pas** l’explosion composants **vente / stock / préparation / facturation** via `sale_product_pack` (non installable Odoo 19).

**Report** : [`TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md`](../tickets/maintenance/TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md)

---

## Verdict réunion

| Date | Verdict |
|------|---------|
| 2026-06-08 | ☑ **GO cadrage avec réserves** — exécution `19.0.18.0.0` autorisée |

---

## Documents de référence

| Document | Usage |
|----------|-------|
| [`DECISIONS.md`](../cadrage/DECISIONS.md#adr-035--activation-product_pack-lot-63b-kits--coffrets) | ADR-035 acceptée |
| [`CONTRACTS.md`](../cadrage/CONTRACTS.md) § C3.E | Contrat figé |
| [`TICKET_LOT6_3B_PORTE_KITS_COFFRETS.md`](./TICKET_LOT6_3B_PORTE_KITS_COFFRETS.md) | Cadrage complet |
