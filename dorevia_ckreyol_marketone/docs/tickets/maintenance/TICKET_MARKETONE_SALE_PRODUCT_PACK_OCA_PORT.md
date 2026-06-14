# TICKET — Port OCA `sale_product_pack` Odoo 19 (backend packs)

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT` |
| **Statut** | **Clôturé MOA** — doctrine **`non_detailed`** · `sale_product_pack` **veille technique** |
| **Doctrine pack CK** | [`DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md`](../../cadrage2/DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md) — **GO doctrine pack = article** |
| **Priorité MOA** | **Clôturé** — filière fermée · reprise lots front ou autre sujet métier |
| **Diagnostic** | [`DIAGNOSTIC_MOA_SALE_PRODUCT_PACK_19.md`](../../cadrage2/DIAGNOSTIC_MOA_SALE_PRODUCT_PACK_19.md) |
| **Phase A** | [`NOTE_PHASE_A_SALE_PRODUCT_PACK_OCA_19.md`](../../cadrage2/NOTE_PHASE_A_SALE_PRODUCT_PACK_OCA_19.md) — **GO MOA** |
| **Phase B atelier** | [`ATELIER_MOA_PHASE_B_SALE_PRODUCT_PACK.md`](../../cadrage2/ATELIER_MOA_PHASE_B_SALE_PRODUCT_PACK.md) — **clôturé** |
| **Décision Phase B** | [`DECISION_MOA_PHASE_B_SALE_PRODUCT_PACK.md`](../../cadrage2/DECISION_MOA_PHASE_B_SALE_PRODUCT_PACK.md) |
| **Arbitrage post-recette** | [`ARBITRAGE_MOA_POST_PHASE_B_SALE_PRODUCT_PACK.md`](../../cadrage2/ARBITRAGE_MOA_POST_PHASE_B_SALE_PRODUCT_PACK.md) |
| **Pilote contrôlé** | [`DECISION_MOA_PILOTE_CONTROLE_SALE_PRODUCT_PACK.md`](../../cadrage2/DECISION_MOA_PILOTE_CONTROLE_SALE_PRODUCT_PACK.md) — **GO** |
| **Cadre observation** | [`CADRE_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md`](../../cadrage2/CADRE_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md) |
| **Exécution observation** | [`NOTE_EXECUTION_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md`](../../cadrage2/NOTE_EXECUTION_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md) |
| **Réception MOA** | [`RECEPTION_MOA_PHASE_B_SALE_PRODUCT_PACK.md`](../../cadrage2/RECEPTION_MOA_PHASE_B_SALE_PRODUCT_PACK.md) |
| **Prep recette BO** | [`PREP_RECETTE_PHASE_B_SALE_PRODUCT_PACK_BO.md`](../../cadrage2/PREP_RECETTE_PHASE_B_SALE_PRODUCT_PACK_BO.md) |
| **Recette BO** | [`RECETTE_MANUELLE_PHASE_B_SALE_PRODUCT_PACK_BO.md`](../../recette/maintenance/RECETTE_MANUELLE_PHASE_B_SALE_PRODUCT_PACK_BO.md) |
| **Branche OCA Dev** | `odoo19-addons-oca` · `dev/phase-a-oca-sale-product-pack-19` · `e8c603b` |
| **PR plateforme** | https://github.com/doreviateam/odoo19-addons-oca/pull/1 — **MERGED** `789fda8` |
| **Exécution étape 1** | [`NOTE_EXECUTION_ETAPE1_PHASE_B_SALE_PRODUCT_PACK.md`](../../cadrage2/NOTE_EXECUTION_ETAPE1_PHASE_B_SALE_PRODUCT_PACK.md) |
| **ADR** | ADR-035 · ADR-005 |

---

## Contexte

Lot **6.3b** clôturé **GO MOA** `19.0.18.0.0` — porte front `product_pack` OK.

La v1 **n’inclut pas** l’explosion composants vente / stock / préparation / facturation. Objectif MOA : sécuriser la profondeur Odoo **avant** reprise lots front gelés.

---

## État modules (post-Phase A — 2026-06-08)

| Module | Version | Manifest | `ckr-marketone-01` |
|--------|---------|----------|---------------------|
| `sale_product_pack` | `19.0.1.0.0` | `installable: True` | **installed** |
| `stock_product_pack` | `19.0.1.0.0` | `installable: True` | **installed** |
| `sale_stock_product_pack` | `19.0.1.0.0` | installable (défaut) | **installed** |
| `product_pack` | `19.0.1.0.2` | `installable: True` | installed (inchangé) |

---

## Verdict MOA (diagnostic 2026-06-08)

| Verdict | Décision |
|---------|----------|
| Activer `sale_product_pack` (copie locale) | **NO GO** |
| Moteur pack Marketone | **NON** — hors doctrine |
| **Reporter activation prod** | **GO** |
| **Plan port OCA minimal** (Phase A–D) | **GO** — voir diagnostic |

> **Point clé MOA** : packs recette 6.3b en `non_detailed` → `sale_product_pack` seul **n’explose pas** les lignes SO. Explosion composants = **`detailed`** + chaîne `sale_product_pack` / `stock_product_pack` / `sale_stock_product_pack` (+ `website_sale_product_pack` si eCommerce).

---

## Périmètre attendu

| Zone | Attendu |
|------|---------|
| Port OCA | Sync PR #244 · #227 · #230 (+ #229 si eCommerce) |
| Intégration Marketone | **Aucun** `depends` sur `dorevia_ckreyol_marketone` · pont Dorevia **conditionnel** |
| Vente web | Recette post-port si packs `detailed` |
| Stock / prépa / facture | Comportement natif OCA documenté MOA |
| Recette | Scénario BO pack recette **7** / **8** post-port |

**Hors périmètre** : porte front 6.3b · widget composants Marketone · `marketone.pack.*`.

---

## Plan de travail (issu diagnostic)

### Phase A — Alignement OCA (Dev plateforme)

- [x] Importer révisions migrées PR OCA 244 / 227 / 230
- [x] `installable: True` · install sandbox
- [x] Tests OCA verts *(stock 2/2 · sale_stock 1/1 · sale setUpClass bloqué)*

### Phase B — Décision MOA configuration produit

- [x] Trancher `non_detailed` (témoin **8**) vs `detailed` (pilote **7**)
- [x] Valider `pack_component_price` = **`ignored`**
- [x] **`website_sale_product_pack`** (#229) = **NON** Phase B

### Phase C — Module pont (conditionnel)

- [ ] Uniquement si écart résiduel post-OCA · pas d’explosion custom

### Phase D — Recette MOA

- [x] Commande · picking · facture · non-régression 6.3b front *(pack **7** `detailed`)*

### Phase E — Arbitrage post-recette · pilote contrôlé

- [x] Arbitrage MOA : **pilote 7 maintenu** · **NON généralisation catalogue** — [`ARBITRAGE_MOA_POST_PHASE_B_SALE_PRODUCT_PACK.md`](../../cadrage2/ARBITRAGE_MOA_POST_PHASE_B_SALE_PRODUCT_PACK.md)
- [x] **GO pilote contrôlé** — [`DECISION_MOA_PILOTE_CONTROLE_SALE_PRODUCT_PACK.md`](../../cadrage2/DECISION_MOA_PILOTE_CONTROLE_SALE_PRODUCT_PACK.md)
- [x] Observation technique pack **7** — [`CADRE_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md`](../../cadrage2/CADRE_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md)
- [x] **Verdict sortie pilote** : **GO doctrine `non_detailed`** — pack = article — [`DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md`](../../cadrage2/DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md)
- [x] **NON généralisation `detailed`** · **`sale_product_pack` veille technique** · **NO GO activation métier CK**

---

## Critères GO activation

- [ ] `sale_product_pack` **installable** et tests OCA **verts** sur Odoo 19 CE
- [ ] Chaîne stock activée si objectif picking composants
- [ ] Commande vente pack : comportement documenté et **validé MOA**
- [ ] Impact stock composants validé MOA
- [x] Décision MOA : config `pack_type` · modules activés · amendement ADR-035
- [ ] **Aucun** moteur pack dans Marketone

---

## Références

| Document | Rôle |
|----------|------|
| [`DIAGNOSTIC_MOA_SALE_PRODUCT_PACK_19.md`](../../cadrage2/DIAGNOSTIC_MOA_SALE_PRODUCT_PACK_19.md) | **Diagnostic complet** |
| [`RECEPTION_MOA_LOT6_3B_PACK.md`](../../cadrage2/RECEPTION_MOA_LOT6_3B_PACK.md) | Clôture front 6.3b |
| [`TICKET_MARKETONE_LOT6_3B_PORTE_PACK_EXEC.md`](../lots/TICKET_MARKETONE_LOT6_3B_PORTE_PACK_EXEC.md) | Porte front v1 |
| `odoo19-addons-oca/sale_product_pack/` | Source locale (gelée) |
| [OCA/product-pack #222](https://github.com/OCA/product-pack/issues/222) | Migration 19.0 |

---

## Verdict ticket

| Date | Verdict | Commentaire |
|------|---------|-------------|
| 2026-06-08 | **Ouvert** | Report MOA — réserve 6.3b · non bloquant front v1 |
| 2026-06-08 | **Diagnostic livré** | NO GO activation immédiate · GO plan port OCA |
| 2026-06-08 | **Phase A GO MOA** | GO PR plateforme · GO atelier Phase B · NO GO prod · voir note Phase A |
| 2026-06-08 | **Phase B GO configuration** | Pilote **7** `detailed` · **8** témoin `non_detailed` · `ignored` · NON #229 · **GO lancement recette BO** |
| 2026-06-08 | **Position MOA confirmée** | Lexique GO validé · prochaine marche validée — [`RECEPTION_MOA_PHASE_B_SALE_PRODUCT_PACK.md`](../../cadrage2/RECEPTION_MOA_PHASE_B_SALE_PRODUCT_PACK.md) |
| 2026-06-08 | **Étape 1 exécutée** | PR #1 mergée · sandbox à jour · prep 7/8 · smoke Dev B1–B5 OK — [`NOTE_EXECUTION_ETAPE1_PHASE_B_SALE_PRODUCT_PACK.md`](../../cadrage2/NOTE_EXECUTION_ETAPE1_PHASE_B_SALE_PRODUCT_PACK.md) |
| 2026-06-08 | **GO recette BO avec réserve perf sandbox** | B1–B6 exécutés · pack 7 detailed OK · pack 8 non_detailed panier 1 ligne · tests auto 6.3b timeouts HTTP 12 s sandbox |
| 2026-06-08 | **Arbitrage post-recette** | Pilote **7** maintenu · **NON généralisation catalogue** · **NO GO prod** — [`ARBITRAGE_MOA_POST_PHASE_B_SALE_PRODUCT_PACK.md`](../../cadrage2/ARBITRAGE_MOA_POST_PHASE_B_SALE_PRODUCT_PACK.md) |
| 2026-06-08 | **GO pilote contrôlé** | Observation pack **7** · cadre O1–O8 · **NON généralisation** · prod globale **NO GO** — [`DECISION_MOA_PILOTE_CONTROLE_SALE_PRODUCT_PACK.md`](../../cadrage2/DECISION_MOA_PILOTE_CONTROLE_SALE_PRODUCT_PACK.md) |
| 2026-06-08 | **Observation technique pilote exécutée** | O1–O6 + F1–F3 OK — [`NOTE_EXECUTION_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md`](../../cadrage2/NOTE_EXECUTION_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md) |
| 2026-06-08 | **Clôturé MOA — doctrine pack = article** | **GO `non_detailed`** · pack **8** = cible métier · **`sale_product_pack` veille technique** · **NO GO activation CK** — [`DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md`](../../cadrage2/DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md) |

### Critères Phase A

- [x] Sync PR OCA #244 / #227 + #230 (branch)
- [x] Modules **installables** sandbox Odoo 19
- [x] Installation `ckr-marketone-01` OK
- [x] Tests `stock_product_pack` **2/2** · `sale_stock_product_pack` **1/1**
- [ ] Tests `sale_product_pack` OCA **8/8** — setUpClass bloqué (contraintes CE / Marketone)
- [x] Non-régression fonctionnelle `dorevia_marketone_lot6_3b_pack` (Marketone inchangé) · réserve perf sandbox sur timeouts HTTP 12 s
- [x] Aucune modification `dorevia_ckreyol_marketone`
