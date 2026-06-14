# Recette manuelle BO — Phase B `sale_product_pack`

| Champ | Valeur |
|-------|--------|
| **Ticket** | [`TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md`](../../tickets/maintenance/TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md) |
| **Atelier MOA** | [`ATELIER_MOA_PHASE_B_SALE_PRODUCT_PACK.md`](../../cadrage2/ATELIER_MOA_PHASE_B_SALE_PRODUCT_PACK.md) — **clôturé** |
| **Décision MOA** | [`DECISION_MOA_PHASE_B_SALE_PRODUCT_PACK.md`](../../cadrage2/DECISION_MOA_PHASE_B_SALE_PRODUCT_PACK.md) |
| **Réception MOA** | [`RECEPTION_MOA_PHASE_B_SALE_PRODUCT_PACK.md`](../../cadrage2/RECEPTION_MOA_PHASE_B_SALE_PRODUCT_PACK.md) — lexique GO confirmé |
| **Préparation** | [`PREP_RECETTE_PHASE_B_SALE_PRODUCT_PACK_BO.md`](../../cadrage2/PREP_RECETTE_PHASE_B_SALE_PRODUCT_PACK_BO.md) |
| **Base** | `ckr-marketone-01` |
| **Statut** | **Clôturé MOA** — doctrine **`non_detailed`** · pack = article |
| **Doctrine pack CK** | [`DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md`](../../cadrage2/DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md) |
| **Exécution étape 1** | [`NOTE_EXECUTION_ETAPE1_PHASE_B_SALE_PRODUCT_PACK.md`](../../cadrage2/NOTE_EXECUTION_ETAPE1_PHASE_B_SALE_PRODUCT_PACK.md) |
| **Exécution recette** | [`NOTE_EXECUTION_RECETTE_PHASE_B_SALE_PRODUCT_PACK.md`](../../cadrage2/NOTE_EXECUTION_RECETTE_PHASE_B_SALE_PRODUCT_PACK.md) |
| **Activation prod** | **NO GO** |

---

## Doctrine

```text
Odoo exécute. Marketone habille et oriente.
Aucun moteur Odoo remplacé.
```

**Hors périmètre** : modification `dorevia_ckreyol_marketone` · moteur pack Marketone · activation prod sans **GO recette BO** (B1–B6 signés).

> **Lexique validé MOA** (2026-06-08) : **GO lancement recette BO** = autorisation à exécuter cette grille · **GO recette BO** = B1–B6 cochés et signés · **GO activation prod** = post-recette + arbitrage explicite. Voir [`RECEPTION_MOA_PHASE_B_SALE_PRODUCT_PACK.md`](../../cadrage2/RECEPTION_MOA_PHASE_B_SALE_PRODUCT_PACK.md).

**Clôture MOA** : **pack = article** · doctrine **`non_detailed`** · pack **8** = cible métier · **`sale_product_pack` veille technique**.

---

## Prérequis

| Élément | Détail |
|---------|--------|
| **Modules plateforme** | `sale_product_pack` · `stock_product_pack` · `sale_stock_product_pack` installés |
| **Décision MOA** | Pack **7** `detailed` · `pack_component_price=ignored` · pack **8** témoin `non_detailed` |
| **Pack recette** | Template **7** pilote · **8** témoin comparatif |
| **Front 6.3b** | Non-régression smoke après recette BO |

---

## Grille recette BO

| # | Scénario | Action | Attendu | MOA |
|---|----------|--------|---------|-----|
| **B1** | Lignes commande | Devis · pack **7** × 1 | **1 ligne pack + 5 composants** (`detailed` + `ignored`) | ☑ |
| **B1b** | Témoin | Devis · pack **8** × 1 | **1 ligne pack** (`non_detailed`) | ☑ |
| **B2** | Confirmation | Confirmer devis | Commande confirmée · pas d’erreur OCA | ☑ |
| **B3** | Picking / stock | Ouvrir transfert généré | **6 moves** dont composants stockables | ☑ |
| **B4** | Préparation | Valider picking (qtés) | Picking `done` · `qty_delivered` parent = **1** | ☑ |
| **B5** | Facturation | Créer facture | Total facture **4,17 €** · composants à **0** · pas de double comptage | ☑ |
| **B6** | Smoke front | `/shop?marketone_mode=pack` · `/kits` | Porte Kits **6.3b inchangée** · packs **7**/**8** visibles · **ne rouvre pas** le lot 6.3b | ☑ |
| **B6b** | Panier témoin | Ajouter pack **8** au panier | **1 ligne** via `website_sale` / `_cart_add` *(non_detailed)* | ☑ |
| **B6c** | Pack 7 front | *(optionnel)* fiche pack **7** visible porte | Pas de recette checkout **detailed** (#229 hors Phase B) · pas de régression chip/alias/filtre | ☑ |

---

## Non-régression Marketone 6.3b

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d ckr-marketone-01 \
  --test-tags=dorevia_marketone_lot6_3b_pack \
  --stop-after-init --http-port=0
```

Résultat recette 2026-06-08 :

- Recette fonctionnelle B1–B6 : **OK**.
- Tests auto 6.3b relancés 2 fois : **0 échec fonctionnel**, mais **timeouts sandbox** sur rendus HTTP `/shop` ou `/shop?marketone_mode=pack` au seuil 12 s pendant / après régénération assets. Les mêmes URLs répondent ensuite en **200**.
- Réserve : performance / stabilité sandbox à suivre, hors décision métier Phase B.

---

## Réserves

| Sujet | Traitement |
|-------|------------|
| PR OCA #230 | Pinnée Phase A · suivre merge upstream |
| Tests OCA 8/8 `sale_product_pack` | Hors recette MOA BO · setup CE |
| `website_sale_product_pack` | **NON Phase B** — ticket séparé si checkout **detailed** requis |
| Tests auto Marketone 6.3b | Réserve perf sandbox : timeouts HTTP 12 s sur `/shop`, URLs rendues ensuite en 200 |
| État base | Restaurer config 6.3b via `prep_recette_lot6_3b_pack.py` |

---

## Verdict MOA

| Date | Verdict | Commentaire |
|------|---------|-------------|
| 2026-06-08 | ☑ **GO lancement recette BO exécuté** | Merge PR #1 · sandbox · prep · smoke Dev B1–B5 |
| | ☑ **GO recette BO avec réserve perf sandbox** | B1–B6 exécutés · réserve tests auto 6.3b timeouts HTTP 12 s |
| | ☑ **Verdict sortie pilote** | **GO doctrine `non_detailed`** — [`DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md`](../../cadrage2/DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md) |
| | ☑ **`sale_product_pack` veille technique** | **NO GO activation métier CK** |
