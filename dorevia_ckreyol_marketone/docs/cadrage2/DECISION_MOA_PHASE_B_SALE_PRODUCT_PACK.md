# Décision MOA — Phase B `sale_product_pack` · configuration packs CK

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-06-08 |
| **Verdict atelier** | **GO Phase B — configuration pilote tranchée** |
| **Activation prod** | **NO GO** — arbitrage post-recette : pilote maintenu |
| **Ticket** | [`TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md`](../tickets/maintenance/TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md) |
| **Atelier** | [`ATELIER_MOA_PHASE_B_SALE_PRODUCT_PACK.md`](./ATELIER_MOA_PHASE_B_SALE_PRODUCT_PACK.md) |
| **Phase A** | [`NOTE_PHASE_A_SALE_PRODUCT_PACK_OCA_19.md`](./NOTE_PHASE_A_SALE_PRODUCT_PACK_OCA_19.md) — GO MOA |
| **PR plateforme** | https://github.com/doreviateam/odoo19-addons-oca/pull/1 |
| **ADR** | [ADR-035](../cadrage/DECISIONS.md#adr-035--activation-product_pack-lot-63b-kits--coffrets) — amendement Phase B |
| **Réception MOA** | [`RECEPTION_MOA_PHASE_B_SALE_PRODUCT_PACK.md`](./RECEPTION_MOA_PHASE_B_SALE_PRODUCT_PACK.md) — lexique GO confirmé |
| **Arbitrage post-recette** | [`ARBITRAGE_MOA_POST_PHASE_B_SALE_PRODUCT_PACK.md`](./ARBITRAGE_MOA_POST_PHASE_B_SALE_PRODUCT_PACK.md) |
| **Doctrine pack CK** | [`DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md`](./DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md) — **clôture MOA** |

---

## Doctrine opposable

```text
Odoo exécute. Marketone habille et oriente.
Aucun moteur Odoo remplacé.
```

**Interdit** : `depends` Marketone sur `sale_product_pack` · `marketone.pack.*` · explosion custom · modification `dorevia_ckreyol_marketone` à ce stade.

---

## Décisions MOA Phase B

### B1 — Configuration pack pilote

| Paramètre | Décision MOA | Produit pilote |
|-----------|--------------|----------------|
| **`pack_type`** | **`detailed`** | Template **7** — Maniocookies salés La Platine |
| **`pack_component_price`** | **`ignored`** | Prix commercial **sur la ligne pack parent** · composants à **0** |
| **Témoin comparatif** | **`non_detailed`** conservé | Template **8** — Crackers manioc Sainte-Anne |
| **Témoin hors pack** | inchangé | Template **9** — `pack_ok=False` |

**Motif MOA** : valider la profondeur Odoo (explosion composants vente / stock / prépa / facture) sur **un seul pack pilote**, sans généraliser immédiatement tout le catalogue pack.

### B2 — Chaîne modules plateforme (hors Marketone)

| Module | Décision Phase B |
|--------|------------------|
| `sale_product_pack` | **GO sandbox / recette** après merge PR #1 |
| `stock_product_pack` | **GO sandbox / recette** |
| `sale_stock_product_pack` | **GO sandbox / recette** *(PR OCA #230 pinnée Phase A)* |
| `website_sale_product_pack` (#229) | **NON Phase B** — ticket / recette eCommerce **séparée** si besoin checkout **detailed** |

**Marketone** : aucun ajout de `depends` · version **`19.0.18.0.0`** inchangée.

### B3 — Périmètre recette MOA

| Zone | Inclus Phase B | Exclu Phase B |
|------|----------------|---------------|
| **Devis / commande BO** | ✓ pack **7** | — |
| **Confirmation vente** | ✓ | — |
| **Picking / stock composants** | ✓ composants stockables | — |
| **Facturation** | ✓ cohérence montant · pas double comptage | — |
| **Smoke front 6.3b** | ✓ porte `/shop?marketone_mode=pack` | — |
| **Checkout eCommerce detailed** | — | #229 + recette dédiée |
| **Généralisation tous packs CK** | — | après GO recette pilote |

### B4 — Comportement attendu (pilote pack **7**)

| Processus | Attendu OCA `detailed` + `ignored` |
|-----------|--------------------------------------|
| **Lignes SO** | 1 ligne pack parent + N lignes composants |
| **Prix** | Total = prix pack parent · lignes composants à **0** |
| **Picking** | Moves sur **composants** stockables |
| **Livraison pack** | `qty_delivered` pack dérivée des composants (`sale_stock_product_pack`) |
| **Facture** | Montant = pack parent · pas de double comptage composants |

### B5 — Front Marketone 6.3b (inchangé à ce stade)

| Élément | Décision |
|---------|----------|
| Porte pack · chip · alias `/kits` | **Inchangé** — clôture 6.3b préservée |
| Panier eCommerce pack **8** (`non_detailed`) | **1 ligne** — comportement v1 maintenu |
| Panier eCommerce pack **7** (`detailed`) | **Hors validation Phase B** — recette BO prioritaire · #229 reporté |

---

## Conditions GO activation production *(post-recette)*

| # | Condition | Statut |
|---|-----------|--------|
| C1 | PR plateforme [#1](https://github.com/doreviateam/odoo19-addons-oca/pull/1) **mergée** | ☑ `789fda8` |
| C2 | Recette BO B1–B6 **signée** sur pack **7** | ☑ Avec réserve perf sandbox |
| C3 | Non-régression `dorevia_marketone_lot6_3b_pack` **13/13** | ☐ Réserve timeouts HTTP 12 s sandbox |
| C4 | Décision MOA généralisation packs **`detailed`** (catalogue complet ou pilote seul) | ☑ **NON généralisation** — doctrine `non_detailed` — [`DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md`](./DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md) |
| C5 | Si eCommerce **detailed** en prod → #229 + recette checkout | ☐ / S/O |
| C6 | Amendement ADR-035 documenté | ☑ Phase B |

**Verdict activation prod actuel** : **NO GO**.

---

## Lexique statuts recette — validé MOA (2026-06-08)

| # | Libellé | Signification |
|---|---------|---------------|
| 1 | **GO lancement recette BO** | Autorisation MOA à **exécuter** la recette (post-merge PR #1) |
| 2 | **GO recette BO** | Grille **B1–B6 signée** après exécution — recette **clôturée** |
| 3 | **GO activation prod** | Décision distincte — post-recette + arbitrage pilote / généralisation |

Réception : [`RECEPTION_MOA_PHASE_B_SALE_PRODUCT_PACK.md`](./RECEPTION_MOA_PHASE_B_SALE_PRODUCT_PACK.md).

---

## Amendement ADR-035 (Phase B)

| Avant (clôture 6.3b) | Après atelier Phase B |
|----------------------|------------------------|
| Réserve : pas d’explosion composants backend | **Pilote autorisé** : pack **7** en `detailed` + chaîne OCA plateforme |
| `sale_product_pack` hors v1 | **Hors depends Marketone** · activation **plateforme** sandbox/recette |
| Panier front = 1 ligne pack v1 | **Maintenu** pour packs `non_detailed` · eCommerce **detailed** = #229 |

**Recette BO** (2026-06-08) : **GO avec réserve perf sandbox** — B1–B6 exécutés · lot **6.3b front non rouvert**.

---

## Prochaine marche — validée MOA

| # | Action | Statut |
|---|--------|--------|
| 1 | Merger **PR #1** `odoo19-addons-oca` | ☑ `789fda8` |
| 2 | Valider la chaîne OCA en sandbox · prep pack **7**/**8** | ☑ |
| 3 | Exécuter recette BO **B1–B6** — [`RECETTE_MANUELLE_PHASE_B_SALE_PRODUCT_PACK_BO.md`](../recette/maintenance/RECETTE_MANUELLE_PHASE_B_SALE_PRODUCT_PACK_BO.md) | ☑ Avec réserve perf sandbox |
| 4 | **Signer ou non** le **GO recette BO** | ☑ GO avec réserve perf sandbox |
| 5 | Arbitrer **pilote limité** vs **généralisation** avant GO prod | ☑ Pilote **7** maintenu · **NON** généralisation catalogue |
| 6 | Préparer **phase pilote contrôlé** — observation métier | ☑ GO — [`DECISION_MOA_PILOTE_CONTROLE_SALE_PRODUCT_PACK.md`](./DECISION_MOA_PILOTE_CONTROLE_SALE_PRODUCT_PACK.md) |
| 7 | Exécuter observation · verdict sortie pilote | ☑ **GO doctrine `non_detailed`** — [`DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md`](./DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md) |

---

## Verdict final atelier

| Date | Verdict |
|------|---------|
| 2026-06-08 | ☑ **`detailed` pilote 7** · ☑ **`ignored`** · ☑ chaîne OCA sandbox · ☑ **NON #229** Phase B · ☑ **GO recette BO avec réserve perf sandbox** · ☑ **Pilote maintenu · NON généralisation** · ☐ **GO activation prod** |
