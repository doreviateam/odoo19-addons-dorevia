# PV_RECETTE_DOREVIA_CASH_GUARD_V1

## 1. Objet

Procès-verbal de recette du module `dorevia_cash_guard` (Odoo 19 CE).

Ce document acte les résultats de recette des Lots A, B et C, la décision de clôture V1, puis **l’extension V1.2** (solde projeté depuis factures ouvertes).

---

## 2. Périmètre V1 recensé

- Lot A : fondation (scaffold, modèles, contraintes, moteur de calcul).
- Lot B : sécurité, workflow, UI, prévu/réalisé simple.
- Lot C : référentiel documentaire des postes budgétaires + cron optionnel.

Hors périmètre confirmé V1 :

- seed XML automatique sans mapping comptable validé ;
- matching bancaire intelligent ;
- scénarios de simulation complexes ;
- dépendances MIS Builder ;
- intégrations externes (LYNKR, Vault).

---

## 3. Environnement de recette

- URL : `http://localhost:18079`
- Base : `tenant_o8` *(lettre **o**, pas `tenant_08` avec un zéro ; les recettes Lots A/B/C documentées historiquement sous `tenant_01` restent valables sur une base équivalente.)*
- Module : `dorevia_cash_guard`
- Version Odoo : `19.0-20260324`
- Addons path module : `/mnt/odoo19-addons-dorevia/dorevia_cash_guard`

---

## 4. Résultats de recette

### 4.1 Lot A

Verdict : **GO**

Résultat constaté :

- 19 OK / 0 KO

Points validés :

- création point de trésorerie ;
- calculs `initial_balance`, `forecast_final_balance`, `forecast_min_balance`, `min_balance_date` ;
- statuts `safe` / `warning` / `risk` ;
- cas critique (final positif, point bas négatif => `risk`) ;
- contraintes métiers ;
- tri déterministe ;
- simulation prise en compte ;
- variance simple.

### 4.2 Lot B

Verdict final : **GO**  
(après un NO GO initial corrigé)

Résultat constaté :

- 26 OK / 0 KO

Run recette :

- `20260509084518`

Points validés :

- ACL/groupes/règles multi-société ;
- workflow `draft -> validated -> closed -> draft` ;
- verrouillages user non-manager hors brouillon ;
- verrou serveur `action_close` pour non-manager ;
- UI workflow et readonly cohérents ;
- search views points/lignes ;
- prévu/réalisé et variance.

### 4.3 Lot C

Verdict : **GO**

Résultat constaté :

- 16 OK / 0 KO

Run recette :

- `20260509091036`

Points validés :

- référentiel documentaire 20 postes présent ;
- pas de seed automatique dangereux ;
- mapping comptes manuel documenté ;
- cron présent, quotidien, désactivé par défaut ;
- cron testé puis remis inactif ;
- recalcul limité à `draft` et `validated` ;
- exclusion des points `closed` ;
- non-régression indicateurs/workflow.

---

## 5. Correctifs majeurs actés en V1

- sécurisation du calcul du solde initial via lecture comptable contrôlée (`sudo`) avec résultat agrégé uniquement ;
- protection anti-récursion du recalcul ;
- verrou serveur explicite sur actions manager (`action_close`, `action_reopen`) ;
- adaptation Odoo 19 (contrainte `_sql_constraints` remplacée côté métier) ;
- documentation de recette complète (`SCENARIO_MANUEL_LOT_A/B/C.md`).

---

## 6. Commits de référence (branche de travail)

Branche :

- `feature/shop-mvp22-visible-wave1`

Commits principaux V1 :

- `3098883` — fondation module
- `766dd0a` — durcissement recalcul + recette Lot A
- `cd8c0bc` — livraison Lot B
- `fbd8bca` — correctif NO GO Lot B (solde initial + permissions close)
- `d15f393` — livraison Lot C (référentiel postes budgétaires + cron optionnel)
- `eabc767` — scénario manuel Lot C (C1/C2)

---

## 7. Décision de clôture V1

Décision : **V1 clôturée**.

Justification :

- Lots A/B/C validés en recette ;
- aucun KO ouvert sur le périmètre V1 ;
- conformité fonctionnelle et technique au cadrage documentaire (`README`, `SPEC_TECHNIQUE`, `TICKET_DEV_EXECUTABLE_V1`).

---

## 8. Points de vigilance post-clôture

- `test_cash_guard_workflow.py` présent mais non activé dans l’environnement courant (contraintes custom `res.users/res.partner`) ;
- seed XML de postes budgétaires à n’activer qu’après validation locale du mapping comptable.

---

## 9. Signature / Validation

Date de clôture V1 :

- 2026-05-09

Statut final :

- **Dorevia Cash Guard V1 — GO**

---

## 10. Extension V1.2 — Solde projeté depuis factures ouvertes

### 10.1 Périmètre

Ticket : `CG-V1.2-01-PROJECTED-BALANCE-FROM-OPEN-INVOICES`.

Inclus :

- colonne **Solde projeté** sur le suivi de trésorerie (`dorevia.cash.guard.week`) ;
- calcul agrégé depuis `account.move` : pièces **postées** avec **`amount_residual ≠ 0`** ;
- date projetée : `max(invoice_date_due or invoice_date or situation_date, situation_date)` ;
- statuts de ligne et statut global du point basés sur la **trajectoire projetée forward** (à partir de la date de situation).

Hors périmètre V1.2 (confirmé) :

- budget, devis, simulations avancées, lignes de flux automatiques `dorevia.cash.guard.line` pour les factures.

Référence scénario manuel : `docs/SCENARIO_MANUEL_V1_2_FACTURES_OUVERTES.md`.

### 10.2 Environnement de recette V1.2

- URL : `http://localhost:18079`
- Base : `tenant_o8`
- Module : `dorevia_cash_guard`
- Version module relevée en recette : **`19.0.4.0.7`**

### 10.3 Point de recette contrôlé

Libellé interne :

- `CGV12 20260510 0512 Point recette factures ouvertes`

### 10.4 Résultats validés (produit)

Verdict recette : **GO V1.2**.

Constats :

| Contrôle | Résultat |
| -------- | -------- |
| Baseline sans facture ouverte | **Solde** = **Solde projeté** = 2 520,00 € (ligne Situation) |
| Facture client future +300 € | Intégration au **Solde projeté** sur la **période d’échéance** |
| Facture fournisseur future −500 € | Diminution du **Solde projeté** sur la **période d’échéance** |
| Facture client payée | Résiduel 0,00 € ; **exclue** du projeté |
| Facture brouillon (future) | **Ignorée** |
| Facture client validée **échue** +150 € | Impact sur le projeté **dès la ligne Situation** (exigible à la date de situation) |
| Facture brouillon **échue** | **Ignorée** |
| Flux prévisionnels | **Aucune** ligne `dorevia.cash.guard.line` créée automatiquement pour les factures |

### 10.5 Doctrine validée

```text
Solde de trésorerie constaté ± factures postées ouvertes (à la date projetée) = Solde projeté
```

### 10.6 Commits de référence (branche)

Branche : `feature/shop-mvp22-visible-wave1`

- `daa012e` — `feat(cash_guard): add projected balance from open invoices`
- `622f64d` — `chore(cash_guard): docs V1.1/V1.2, i18n, tests et migrations`

### 10.7 Décision

Décision : **V1.2 — GO** (recette produit validée sur `tenant_o8`).

Date d’acte :

- **2026-05-10**

---

## 11. Signature / Validation (mise à jour V1.2)

Statut après extension :

- **Dorevia Cash Guard V1 + V1.2 — GO**

*(À compléter : validateur produit, validateur technique, signature si formalisme interne.)*
