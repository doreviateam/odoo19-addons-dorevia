# Arbitrage MOA — Post-Phase B `sale_product_pack`

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-06-08 |
| **Contexte** | Recette BO B1–B6 **GO avec réserve perf sandbox** |
| **Ticket** | [`TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md`](../tickets/maintenance/TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md) |
| **Décision Phase B** | [`DECISION_MOA_PHASE_B_SALE_PRODUCT_PACK.md`](./DECISION_MOA_PHASE_B_SALE_PRODUCT_PACK.md) |
| **Recette** | [`RECETTE_MANUELLE_PHASE_B_SALE_PRODUCT_PACK_BO.md`](../recette/maintenance/RECETTE_MANUELLE_PHASE_B_SALE_PRODUCT_PACK_BO.md) |
| **Verdict arbitrage** | **Pilote maintenu** · **NON généralisation catalogue** · **NO GO activation prod** |
| **Pilote contrôlé** | [`DECISION_MOA_PILOTE_CONTROLE_SALE_PRODUCT_PACK.md`](./DECISION_MOA_PILOTE_CONTROLE_SALE_PRODUCT_PACK.md) — **GO pilote contrôlé** |

---

## Doctrine opposable

```text
Odoo exécute. Marketone habille et oriente.
Aucun moteur Odoo remplacé.
```

**Interdit** : généralisation `detailed` automatique post-recette · `depends` Marketone · moteur pack Marketone · activation prod sans décision explicite.

---

## Contexte arbitrage

La recette BO **B1–B6** valide fonctionnellement la chaîne `sale_product_pack` + `stock_product_pack` + `sale_stock_product_pack` sur le pack pilote **7** (`detailed` / `ignored`), avec témoin **8** (`non_detailed`).

La **généralisation** `detailed` à tout le catalogue pack modifierait la lecture métier des **commandes**, **lignes composants**, **préparation**, **stock** et potentiellement **facturation**. Elle ne peut pas être déduite automatiquement d’une recette technique réussie.

---

## Décision MOA

| Sujet | Décision |
|-------|----------|
| **Pack pilote 7** | **Maintenu** en `detailed` · `pack_component_price=ignored` |
| **Pack témoin 8** | **Conservé** en `non_detailed` · `ignored` |
| **Généralisation catalogue** | **NON** à ce stade — pas de bascule `detailed` sur tous les packs CK |
| **Activation production** | **NO GO** |
| **Phase suivante** | **Pilote contrôlé** — observation métier avant toute décision de généralisation |

### Motif MOA

1. La chaîne OCA est **fonctionnelle** — recette signée avec réserve perf sandbox uniquement.
2. La généralisation impacte les **processus métier** (vente, stock, prépa, facture) — décision **métier**, pas technique.
3. Le témoin **8** `non_detailed` conserve une **référence comparatif** BO et front v1.
4. Le lot **6.3b front** reste **clôturé** — pas de réouverture.

---

## Lexique GO — post-arbitrage

| Niveau | Signification | Statut |
|--------|---------------|--------|
| **GO recette BO** | B1–B6 validés | ☑ **Avec réserve perf sandbox** |
| **Arbitrage post-recette** | Pilote vs généralisation | ☑ **Pilote maintenu · NON généralisation** |
| **GO pilote contrôlé** | Déploiement / observation métier encadrée | ☑ **Accordé** — [`DECISION_MOA_PILOTE_CONTROLE_SALE_PRODUCT_PACK.md`](./DECISION_MOA_PILOTE_CONTROLE_SALE_PRODUCT_PACK.md) |
| **GO généralisation** | Bascule `detailed` catalogue pack CK | ☑ **NON** — doctrine `non_detailed` |
| **GO activation prod** | Chaîne OCA en production | ☐ **NO GO** |

---

## Périmètre pilote contrôlé — **GO MOA 2026-06-08**

| Élément | Attendu |
|---------|---------|
| **Pack concerné** | Template **7** uniquement en `detailed` |
| **Témoin** | Template **8** `non_detailed` conservé |
| **Marketone** | Inchangé · pas de `depends` |
| **Front 6.3b** | Non rouvert · smoke non-régression |
| **eCommerce detailed** | #229 hors scope — ticket séparé si requis |
| **Observation métier** | Cadre O1–O8 — [`CADRE_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md`](./CADRE_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md) |
| **Critère sortie pilote** | Décision MOA : maintien pilote · extension limitée · ou **GO généralisation** |

---

## Interdits maintenus

| Interdit | Statut |
|----------|--------|
| Généraliser `detailed` sans décision MOA | ✓ |
| Ajouter `sale_product_pack` aux `depends` Marketone | ✓ |
| Créer `marketone.pack.*` ou explosion custom | ✓ |
| Activer prod sans **GO pilote contrôlé** ou **GO généralisation** + critères C1–C6 | ✓ |
| Rouvrir lot **6.3b front** | ✓ |

---

## Verdict MOA

| Date | Verdict |
|------|---------|
| 2026-06-08 | ☑ **GO recette BO avec réserve perf sandbox** |
| 2026-06-08 | ☑ **Pilote 7 maintenu** · ☑ **NON généralisation catalogue** · ☐ **GO activation prod** |
| 2026-06-08 | ☑ **GO pilote contrôlé** · ☐ **GO généralisation** · ☐ **GO activation prod** |
| 2026-06-08 | ☑ **GO doctrine `non_detailed`** · ☑ **`sale_product_pack` veille technique** — [`DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md`](./DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md) |

---

## Références

- [`RECEPTION_MOA_PHASE_B_SALE_PRODUCT_PACK.md`](./RECEPTION_MOA_PHASE_B_SALE_PRODUCT_PACK.md)
- [`NOTE_EXECUTION_RECETTE_PHASE_B_SALE_PRODUCT_PACK.md`](./NOTE_EXECUTION_RECETTE_PHASE_B_SALE_PRODUCT_PACK.md)
- [ADR-035](../cadrage/DECISIONS.md#adr-035--activation-product_pack-lot-63b-kits--coffrets)
