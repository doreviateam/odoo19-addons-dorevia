# Atelier MOA — Phase B `sale_product_pack` · configuration packs CK

| Champ | Valeur |
|-------|--------|
| **Date atelier** | 2026-06-08 |
| **Ticket** | [`TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md`](../tickets/maintenance/TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md) |
| **Décision MOA** | [`DECISION_MOA_PHASE_B_SALE_PRODUCT_PACK.md`](./DECISION_MOA_PHASE_B_SALE_PRODUCT_PACK.md) |
| **Réception MOA** | [`RECEPTION_MOA_PHASE_B_SALE_PRODUCT_PACK.md`](./RECEPTION_MOA_PHASE_B_SALE_PRODUCT_PACK.md) — lexique GO confirmé |
| **Phase A** | [`NOTE_PHASE_A_SALE_PRODUCT_PACK_OCA_19.md`](./NOTE_PHASE_A_SALE_PRODUCT_PACK_OCA_19.md) — GO MOA |
| **PR plateforme** | https://github.com/doreviateam/odoo19-addons-oca/pull/1 |
| **Statut** | **Clôturé — GO configuration pilote** |
| **Activation prod** | **NO GO** — recette BO signée (B1–B6) requise |

---

## Doctrine

```text
Odoo exécute. Marketone habille et oriente.
Aucun moteur Odoo remplacé.
```

---

## Synthèse décisions MOA

| Sujet | Décision |
|-------|----------|
| **`pack_type`** | **`detailed`** — pack pilote **7** uniquement |
| **`pack_component_price`** | **`ignored`** — prix sur parent pack |
| **Témoin pack 8** | **`non_detailed`** conservé |
| **Chaîne OCA** | `sale_product_pack` + `stock_product_pack` + `sale_stock_product_pack` — sandbox/recette |
| **`website_sale_product_pack`** | **NON** Phase B |
| **Marketone** | **Aucune modification** · pas de `depends` |
| **Recette** | **GO lancement recette BO** · B1–B6 sur pack **7** · smoke front 6.3b · **à signer** |
| **Activation prod** | **NO GO** |

---

## Rationale MOA

1. **Un pack pilote `detailed`** suffit pour valider commande → stock → préparation → facture sans généraliser le catalogue.
2. **`ignored`** preserve le prix commercial coffret sur la ligne parent — aligné avec la config 6.3b et évite le double comptage.
3. **Pack 8 `non_detailed`** sert de témoin comparatif BO et maintient le comportement front v1 sur au moins un produit visible porte pack.
4. **`website_sale_product_pack`** reporté : Phase B = profondeur **BO** ; le checkout eCommerce **detailed** est un lot distinct.
5. **Aucun moteur Marketone** : la chaîne reste 100 % OCA côté plateforme.

---

## Verdict atelier

| Date | Verdict |
|------|---------|
| 2026-06-08 | ☑ **GO Phase B configuration** · ☑ **GO lancement recette BO** · ☐ **GO recette BO** (B1–B6) · ☐ **GO activation prod** |

**Suite** : recette BO B1–B6 → signature **GO recette BO** — [`RECETTE_MANUELLE_PHASE_B_SALE_PRODUCT_PACK_BO.md`](../recette/maintenance/RECETTE_MANUELLE_PHASE_B_SALE_PRODUCT_PACK_BO.md) · PR #1 **mergée** `789fda8`.
