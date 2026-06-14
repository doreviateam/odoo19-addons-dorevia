# Décision MOA — Pilote contrôlé `sale_product_pack` · pack 7

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-06-08 |
| **Verdict** | **GO pilote contrôlé** |
| **Ticket** | [`TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md`](../tickets/maintenance/TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md) |
| **Arbitrage post-recette** | [`ARBITRAGE_MOA_POST_PHASE_B_SALE_PRODUCT_PACK.md`](./ARBITRAGE_MOA_POST_PHASE_B_SALE_PRODUCT_PACK.md) |
| **Recette Phase B** | [`RECETTE_MANUELLE_PHASE_B_SALE_PRODUCT_PACK_BO.md`](../recette/maintenance/RECETTE_MANUELLE_PHASE_B_SALE_PRODUCT_PACK_BO.md) — GO avec réserve perf sandbox |
| **Cadre observation** | [`CADRE_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md`](./CADRE_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md) |
| **Activation prod globale** | **NO GO** |

---

## Doctrine opposable

```text
Odoo exécute. Marketone habille et oriente.
Aucun moteur Odoo remplacé.
```

---

## Contexte

La recette BO Phase B a validé **fonctionnellement** la chaîne OCA (`sale_product_pack` + `stock_product_pack` + `sale_stock_product_pack`) avec **réserve perf sandbox** uniquement.

La généralisation `detailed` au catalogue n’est **pas** actée. MOA souhaite **observer le comportement réel à l’usage** avant toute décision de généralisation ou d’activation prod globale.

---

## Décision MOA

| Sujet | Décision |
|-------|----------|
| **GO pilote contrôlé** | ☑ **Accordé** — pack **7** uniquement |
| **Pack 7** | **`detailed`** · `pack_component_price=ignored` |
| **Pack 8** | **`non_detailed`** · témoin comparatif conservé |
| **Généralisation catalogue** | **NON** — reportée |
| **Marketone** | **Aucune modification** · pas de `depends` |
| **Lot front 6.3b** | **Non rouvert** |
| **Moteur pack Marketone** | **Interdit** |
| **Activation prod globale** | **NO GO** |

---

## Objectif du pilote

Observer concrètement l’impact du **`detailed`** sur :

| Domaine | Question métier |
|---------|-----------------|
| **Commandes** | Lisibilité des lignes pack + composants en usage réel |
| **Lignes composants** | Utilité opérationnelle vs bruit visuel |
| **Préparation** | Adéquation picking / moves composants |
| **Stock** | Impact sur suivi composants et disponibilité |
| **Facturation** | Cohérence montants · pas de double comptage en conditions réelles |
| **Lisibilité BO** | Acceptabilité équipes vente / logistique / compta |
| **Intérêt métier** | Gain réel **`detailed`** vs témoin **`non_detailed`** (pack **8**) |

---

## Périmètre pilote

| Inclus | Exclu |
|--------|-------|
| Pack **7** en `detailed` sur environnement d’observation | Généralisation `detailed` catalogue |
| Pack **8** témoin `non_detailed` | Modification `dorevia_ckreyol_marketone` |
| Commandes BO simulées ou réelles encadrées | Réouverture lot **6.3b front** |
| Comparatif 7 vs 8 sur mêmes processus | `website_sale_product_pack` (#229) |
| Chaîne OCA plateforme déjà installée sandbox | **Activation prod globale** chaîne OCA |

**Environnement d’observation principal** : sandbox **`ckr-marketone-01`**. Extension prod pack **7** seul = **GO MOA distinct** post-pilote.

---

## Lexique GO — post-décision pilote

| Niveau | Statut |
|--------|--------|
| **GO recette BO** | ☑ Avec réserve perf sandbox |
| **Arbitrage post-recette** | ☑ Pilote maintenu · NON généralisation |
| **GO pilote contrôlé** | ☑ **Accordé** |
| **GO généralisation** | ☐ **Reporté** |
| **GO activation prod globale** | ☐ **NO GO** |

---

## Critères de sortie pilote *(à trancher MOA post-observation)*

| Option | Description |
|--------|-------------|
| **A — Maintien pilote seul** | Pack **7** `detailed` · reste du catalogue `non_detailed` |
| **B — Extension limitée** | `detailed` sur N packs identifiés MOA |
| **C — GO généralisation** | Bascule catalogue pack CK — décision MOA explicite |
| **D — Retour non_detailed pilote** | Pack **7** repasse témoin si intérêt métier insuffisant |

---

## Interdits maintenus

- Généraliser `detailed` sans **GO généralisation** signé
- Ajouter `sale_product_pack` aux `depends` Marketone
- Créer `marketone.pack.*` ou explosion custom
- Rouvrir le lot **6.3b front**
- Activer prod globale sans critères C1–C6 + décision MOA

---

## Verdict MOA

| Date | Verdict |
|------|---------|
| 2026-06-08 | ☑ **GO pilote contrôlé pack 7** · ☐ **GO généralisation** · ☐ **GO activation prod globale** |
| 2026-06-08 | ☑ **Clôture pilote** — **GO doctrine `non_detailed`** — [`DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md`](./DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md) |

**Suite** : doctrine pack = article · `sale_product_pack` **veille technique**.
