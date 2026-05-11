# PV_RECETTE_DOREVIA_CASH_GUARD_V1_PLUS_EXTENSIONS

*Nom de fichier conservé : `PV_RECETTE_DOREVIA_CASH_GUARD_V1.md` (liens et historique).*

## 1. Objet

Procès-verbal de recette du module `dorevia_cash_guard` (Odoo 19 CE).

Ce document acte les résultats de recette des Lots A, B et C, la décision de clôture V1, puis les extensions **V1.2** (solde projeté depuis factures ouvertes) et **V1.3** (détail projection par période + recette UI).

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

- création d’un document de projection ;
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

- colonne **Projection** sur le suivi de trésorerie (`dorevia.cash.guard.week`) ; colonne **État** (Constaté / Situation / Projeté) ;
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
| Baseline sans facture ouverte | **Solde** = **Projection** = 2 520,00 € (ligne **État** = Situation) |
| Facture client future +300 € | Intégration à la **Projection** sur la **période d’échéance** |
| Facture fournisseur future −500 € | Diminution de la **Projection** sur la **période d’échéance** |
| Facture client payée | Résiduel 0,00 € ; **exclue** du projeté |
| Facture brouillon (future) | **Ignorée** |
| Facture client validée **échue** +150 € | Impact sur le projeté **dès la ligne Situation** (exigible à la date de situation) |
| Facture brouillon **échue** | **Ignorée** |
| Flux complémentaires | **Aucune** ligne `dorevia.cash.guard.line` créée automatiquement pour les factures |

### 10.5 Doctrine validée

```text
Solde de trésorerie constaté ± factures postées ouvertes (à la date projetée) = Projection (colonne UI)
```

### 10.6 Commits de référence (branche)

Branche : `feature/shop-mvp22-visible-wave1`

- `daa012e` — `feat(cash_guard): add projected balance from open invoices`
- `622f64d` — `chore(cash_guard): docs V1.1/V1.2, i18n, tests et migrations`

### 10.7 Décision

Décision : **V1.2 — GO** (recette produit validée sur `tenant_o8`).

Date d’acte :

- **2026-05-10**

### 10.8 Points hors jalon à traiter ultérieurement

- projection attendue issue du budget ;
- règles de ventilation de trésorerie ;
- simulations avancées ;
- intégration éventuelle LYNKR / Vault ;
- amélioration du chatter.

*(Le périmètre V1.2 acté ci-dessus couvre uniquement la **projection engagée par factures ouvertes**.)*

---

## 11. Signature / Validation (mise à jour V1.2)

Statut après extension :

- **Dorevia Cash Guard V1 étendue V1.2 — GO**

*(À compléter : validateur produit, validateur technique, signature si formalisme interne.)*

---

## 12. Extension V1.3 — Détail projection (pièces par période)

### 12.1 Périmètre

Ticket : `CG-V1.3-01-PROJECTION-PERIOD-EXPLANATION`.

Inclus :

- onglet **Détail projection** : lignes `dorevia.cash.guard.period.move` liées aux factures/avoirs ouverts ;
- colonnes métier (vue par défaut) : **Statut** ; **Période** ; **Pièce** (`move_id`, lien facture) ; **Partenaire** ; **Type** ; **Échéance** ; **Impact** (total) ; **Échue** ; action discrète (icône, fin de ligne) ; **Impact net période** / **Nb pièces** / **Date projetée** en colonnes optionnelles masquées par défaut ; ouverture `account.move` avec droits standards ; pas d’ouverture du formulaire technique `dorevia.cash.guard.period.move` au clic sur la ligne ;
- tri par défaut **Risque → Tension → Vigilance → Confort** (champ technique `period_risk_sequence`), puis période, date projetée, impact ; décorations liste par statut (rouge / orange / bleu / vert) ;
- mode focus **Non sécurisées seulement** dans l’onglet détail : lignes `Risque` + `Vigilance` uniquement, avec bascule **Toutes** conservant les lignes `Sécurisé` ;
- masquage UI de l’onglet **Flux complémentaires** sur le formulaire document (`invisible="1"`), modèle et menu liste conservés.

Référence scénario manuel : `docs/SCENARIO_MANUEL_V1_3_DETAIL_PROJECTION.md`.

### 12.2 Environnement de recette V1.3

- Base : `tenant_o8`
- Module : `dorevia_cash_guard`
- Version module relevée en recette : **`19.0.5.0.8`**

### 12.3 Recette UI — compréhension métier

Verdict : **GO V1.3** (compréhension métier de l’onglet **Détail projection**). Tests automatisés V1.3 : **OK**. Formalisation : présent PV + signatures internes selon process.

Constats produit :

- **Statut** + tri métier : les pièces des périodes en **Risque** apparaissent avant **Tension**, puis **Vigilance**, puis **Confort** (non-regression testée : ordre `risk`, `tension`, `warning`, `safe`) ;
- **Non sécurisées seulement** : filtre de lecture sur les lignes **Risque** + **Tension** + **Vigilance**, sans suppression des lignes **Confort** disponibles dans **Toutes** ;
- **Échue** en **Oui / Non** : lecture immédiate ;
- **Impact net période** : effet global de la période sans regroupement natif (Odoo ne permet pas `group_by` utile dans le one2many embarqué) ; compromis = tri + colonnes répétées — acceptable V1.3 ;
- **Nb pièces** : nombre de pièces expliquant la période ;
- pièces critiques identifiables en tête de liste (ex. ligne **Risque / S31 / FACTU/2026/06/0001 / −4 000,00 €**, puis **Vigilance / S22**, etc.).

Lecture métier validée sur un jeu contrôlé :

| Période | Impact net période | Lecture |
| ------- | ------------------ | ------- |
| S20 | +150 € | compensation client / fournisseur |
| S22 | −500 € | sortie nette |
| S24 | +200 € | entrée nette |
| S31 | −4 000 € | tension / risque expliqué |

### 12.4 Réserve UX (non bloquante V1.3)

**Statut**, **Impact net période** et **Nb pièces** sont répétés sur chaque ligne d’une même période. Une vue groupée par période serait plus élégante en évolution ultérieure (hors contrainte one2many).

### 12.5 Décision

Décision : **V1.3 — GO** (recette UI compréhension métier + tests automatisés V1.3 **OK**).

Date d’acte (rédaction PV) :

- **2026-05-10**

---

## 13. Extension V1.4 — Taux de confirmation bancaire

### 13.1 Périmètre

Nouvel indicateur **Taux de confirmation bancaire** ajouté au bloc **Situation constatée** du document de projection.

Définition :

```text
Taux de confirmation bancaire
= somme(abs(mouvements de trésorerie rapprochés avec un relevé bancaire))
  / somme(abs(mouvements de trésorerie totaux))
× 100
```

Périmètre : journaux de trésorerie du document, écritures postées, jusqu'à la date de situation.

Un mouvement est « confirmé » lorsque la ligne comptable est liée à une ligne de relevé bancaire (`statement_line_id` renseigné sur `account.move.line`).

Le dénominateur inclut également les **paiements bancaires en transit** (`account.payment` postés, `is_matched = False` sur les journaux du périmètre), ce qui empêche le taux d'atteindre 100 % tant que des paiements restent à rapprocher.

Sens métier :

- **100 %** : tous les mouvements de trésorerie sont confirmés ET aucun paiement bancaire en transit ;
- **taux partiel** : une partie des mouvements reste à confirmer ou des paiements sont en attente de rapprochement ;
- **0 %** : aucune confirmation bancaire détectée.

### 13.2 UX

Affiché dans le formulaire, bloc **Situation constatée**, sous le solde constaté, avec un widget barre de progression.

### 13.3 Environnement de recette V1.4

- Base : `tenant_o8`
- Module : `dorevia_cash_guard`
- Version : `19.0.5.3.3`

### 13.4 Résultat de recette

L'indicateur **Taux de confirmation bancaire** est visible dans le bloc **Situation constatée**, sous le **Solde de trésorerie constaté**.

Exemple constaté en recette (après correction V1.4) :

```text
Taux de confirmation bancaire : 97 %
```

Le taux n'est plus 100 % car 520 € de paiements bancaires non rapprochés sont inclus dans le dénominateur.

### 13.5 Lecture métier validée

L'indicateur qualifie la fiabilité du solde constaté sans polluer la projection.

Lecture utilisateur :

- le solde indique combien de trésorerie est constatée à date ;
- le taux de confirmation bancaire indique dans quelle mesure ce solde est confirmé par les relevés bancaires importés / rattachés.

Lecture globale validée :

```text
Situation constatée
→ combien j'ai
→ à quel point c'est confirmé par la banque

Projection
→ ce qui va se passer
→ couverture / statut / pièces explicatives
```

### 13.6 Tests

Suite `dorevia_cash_guard` relancée sur `tenant_o8`.

Résultat :

```text
0 failed, 0 errors
```

Warnings Odoo connus uniquement (`odoo.osv` déprécié).

### 13.7 Décision

**V1.4 — Taux de confirmation bancaire : GO produit.**

Date d'acte (rédaction PV) :

- **2026-05-11**

### 13.8 Correction doctrine V1.4 — paiements en transit

**Problème** : le taux affichait 100 % alors que le tableau de bord Banque montrait encore des paiements à traiter/confirmer.

**Cause** : le calcul V1 ne tenait compte que des `account.move.line` avec `statement_line_id`. Les paiements enregistrés (`account.payment` postés, `is_matched = False`) étaient invisibles pour le taux.

**Correction** (version `19.0.5.3.3`) : le dénominateur du taux intègre désormais `abs(amount)` des paiements non rapprochés sur les journaux du périmètre. Ces paiements gonflent le dénominateur sans augmenter le numérateur, ce qui empêche le 100 % tant qu'il reste des paiements en transit.

**Formule corrigée** :

```text
taux = abs(mouvements confirmés) / (abs(mouvements totaux) + abs(paiements en transit)) × 100
```

**Résultat sur tenant_o8** :

```text
Avant correction : 99 %
Après correction  : 97 %  (520 € de paiements en transit détectés)
```

**Tests** : 53 tests, 0 failed, 0 errors (nouveau test : `test_bank_confirmation_rate_below_100_with_outstanding_payment`).

---

## 14. Signature / Validation (mise à jour V1.4)

Statut après extension :

- **Dorevia Cash Guard V1 étendue V1.2, V1.3 et V1.4 — GO** (V1.4 : Taux de confirmation bancaire validé produit, correction paiements en transit appliquée ; V1.3 : compréhension métier Détail projection validée ; formalisation signatures inchangée section 11 si besoin.)
