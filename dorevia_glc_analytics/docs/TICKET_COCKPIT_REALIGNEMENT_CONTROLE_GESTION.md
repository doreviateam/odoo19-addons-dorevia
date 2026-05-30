# Ticket — Réalignement cockpit GLC / contrôle de gestion

> **Addendum `19.0.14.0.2` (2026-05-30)** — Le corps de ce ticket décrit le GO **`19.0.4.9.0`**. Depuis la simplification MOA :
> - menu **Contrôle de gestion** (réalisé seul, sans budget ni overlay RH) ;
> - Palier 2 et module `dorevia_glc_budget` **retirés** ;
> - grammaire UI : **Ressources · Cumul RH · Dépenses · Solde**.
> État actuel : [ETAT_MODULE_ACTUEL.md](./ETAT_MODULE_ACTUEL.md).

**Module :** `dorevia_glc_analytics`  
**Version installée (réf.) :** `19.0.4.9.0`  
**Statut :** **GO livraison MOA** — Palier 4 réaligné **gelé** · **`19.0.4.9.0`** (2026-05-28) · branche poussée · **88 post-tests verts** · prochaine séquence : cadrage Palier 5 avant code  
**Date :** 2026-05-28

**Références :** [CADRAGE_FINAL_PALIER_4.md](./CADRAGE_FINAL_PALIER_4.md) · [TICKET_COCKPIT_SOURCE_REALISE.md](./TICKET_COCKPIT_SOURCE_REALISE.md) · [TICKET_COCKPIT_DOCTRINE_CLASSE_6_7.md](./TICKET_COCKPIT_DOCTRINE_CLASSE_6_7.md) · [TICKET_COCKPIT_COMPTE_BANCAIRE_REFERENCE.md](./TICKET_COCKPIT_COMPTE_BANCAIRE_REFERENCE.md) · [Recette période libre](./recette/RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md)

---

## 1. Contexte MOA

Le socle technique est solide :

- séparation `dorevia_glc_analytics` / `dorevia_glc_budget` ;
- budget prévisionnel simple ;
- réalisé basé sur `account.analytic.line` ;
- cockpit lisible (synthèse graphique + détail par axe) ;
- tests automatisés nombreux.

En revanche, le module a **franchi un cap fonctionnel** :

| Avant | Maintenant |
|---|---|
| Cockpit de **couverture des salaires** | Cockpit de **pilotage d'exploitation GLC** |

Question centrale devenue :

> Comment l'activité GLC se comporte-t-elle mois par mois, avec recettes, cumul RH, dépenses hors salaires, budget et écarts ?

**Risque si doctrine non réalignée :** le cockpit peut techniquement fonctionner tout en donnant une **lecture de gestion ambiguë** — non par erreur de calcul, mais par **périmètres non alignés** présentés comme comparables.

---

## 2. Doctrine actuelle (à figer partout)

| Flux | Rôle |
|---|---|
| **Réalisé cockpit** | Comptabilité analytique issue des écritures (principalement classes **6 / 7**), tous axes analytiques exploitables |
| **Ventilations RH Palier 2** | **Contrôle / comparaison / justification** — **ne fabriquent pas** le réalisé cockpit (anti double comptage) |
| **Budget Palier 3** | Prévisionnel — périmètre partiel documenté (voir §4) |
| **Grammaire UI MOA** | Ressources · Cumul RH · Dépenses · Solde |

Formule solde :

> **Solde = Recette − Cumul RH − Dépense**

---

## 3. Demandes par lot

### 3.1 — Aligner documentation, manifeste et doctrine

**Constat :** le manifeste `__manifest__.py` évoquait encore « réalisé analytique + ventilations Palier 2 + budget » comme sources équivalentes du réalisé.

**Demande :**

- [ ] Corriger manifeste, README / docs de recette, libellés obsolètes ;
- [ ] Expliciter : ventilations salariales Palier 2 = **contrôle de cohérence**, pas source primaire du réalisé cockpit.

**Statut :** manifeste aligné · libellés UI · filtre axe · budget · contrôle RH V1 — **`19.0.4.9.0`**

---

### 3.2 — Revoir les libellés « Frais généraux » / « Charges de structure »

**Constat :** le réalisé agrège les dépenses hors salaires sur **plusieurs axes analytiques**, pas uniquement `STRUCTURE`. Le libellé « Frais généraux » devient ambigu.

**Demande :**

Renommer côté UI les agrégats concernés en :

> **Dépenses hors salaires**

Alternative future (cockpit plus fin) : distinguer dépenses d'activité / structure / masse salariale.

**Point MOA :** « Dépenses hors salaires » = meilleur libellé générique pour le calcul réel actuel.

**Statut :** **implémenté** (priorité 1) — champs cockpit + lignes détail + onglet Charges.

---

### 3.3 — Écart de périmètre réalisé vs budget

**Constat :** le réalisé couvre toutes les activités avec mouvement ; le budget reste partiellement limité par familles :

- recettes : `BAR`, `PRESTATIONS`, `PRIVATISATIONS` ;
- dépenses : `STRUCTURE`.

**Risque :** une activité (`MISSIONS`, `RESIDENCES`, …) apparaît en réalisé sans budget comparable → écarts **non significatifs** présentés comme significatifs.

**Demande (minimum) :**

- [ ] Lecture explicite **« Réalisé non budgété »** / **« Non budgété »** (déjà amorcé en synthèse KPI) ;
- [ ] Étendre la cartographie budget **ou** masquer les écarts lorsque le budget est absent sur l'axe.

**Attendu MOA :** le cockpit ne doit **pas laisser croire** qu'un écart budget est pilotable si le budget n'existe pas sur le même périmètre.

**Statut :** **partiel** — `has_budget_data` + messages synthèse/détail ; cartographie budget multi-axes **à étendre**.

---

### 3.4 — Filtre activité / axe analytique

**Constat :** `activity_account_id` existait mais était masqué et vidé au refresh (`19.0.4.x`).

**Demande — choix explicite :**

| Option | Description | Préférence MOA |
|---|---|---|
| **A** | Réimplémenter un filtre fiable par axe analytique / activité GLC | **Préférée à terme** |
| **B** | Retirer complètement le filtre (champ, docs, ambiguïtés) | Acceptable si non maintenu ce palier |

**Interdit :** entre-deux où le champ existe sans être utilisable.

**Statut :** **implémenté** (option A) — filtre **Axe analytique** visible, conservé au refresh, titre dynamique.

---

### 3.5 — Contrôle « qualité des données cockpit »

**Constat :** exclusions (classe comptable, legacy, 4/5, analytique manquant) sont **invisibles** pour l'utilisateur.

**Demande :**

Onglet ou bloc **« Données exclues / à contrôler »** listant ou synthétisant :

- écritures 6/7 sans analytique ;
- analytique legacy ;
- comptes 4/5 avec analytique exclus ;
- lignes non classées / ignorées par périmètre.

**Objectif :** comprendre pourquoi un montant n'apparaît pas dans le cockpit.

**Statut :** **évolution** (durcissement fonctionnel).

---

### 3.6 — Contrôle RH global

**Constat :** masse salariale réalisée = écritures payroll analytiques (sain). Il manque une lecture de cohérence :

- paie comptable ;
- ventilations RH validées ;
- répartition par activité.

**Demande :**

KPI informatif **« Paie comptable vs ventilation RH »** :

- par mois / par activité / global période ;
- non bloquant ; statut « à contrôler » si écart.

Exemple :

| Indicateur | Valeur |
|---|---|
| Paie comptable | 20 608 € |
| Ventilée RH | 19 900 € |
| Écart | 708 € |
| Statut | À contrôler |

**Statut :** **V1 informatif** — onglet Infos : paie comptable, ventilation RH, écart, badge statut.

---

### 3.7 — Renforcer le module budget

**Constat :** `dorevia_glc_budget` propre mais minimal pour un pilotage régulier.

**Évolutions à prévoir :**

- import / export Excel ;
- duplication de scénario (`initial → revised`) ;
- commentaire par ligne ;
- statut de revue ;
- assistant répartition annuelle → 12 mois.

**Statut :** **hors cockpit immédiat** — indispensable pour budget réellement exploitable.

---

### 3.8 — Clarifier les versions de recette

**Constat :** décalage possible entre version manifeste, version recette et statut MOA.

**Demande :**

Synchroniser en permanence :

- version cible ;
- version installée ;
- version testée ;
- statut MOA / PV de recette.

**Statut :** recette alignée sur **`19.0.4.8.14`** (voir en-tête recette manuelle).

---

## 4. Priorité MOA recommandée

Avant usage régulier en pilotage :

| P | Sujet | Risque si non traité |
|---|---|---|
| **1** | Libellés « Frais généraux » → **Dépenses hors salaires** | Lecture trompeuse du périmètre dépenses |
| **2** | Périmètre **réalisé vs budget** | Écarts non significatifs présentés comme pilotables |
| **3** | **Filtre activité / axe** | Impossible de zoomer ; ambiguïté technique |
| **4** | **Contrôle RH global** | Écart compta / ventilation invisible |

Ensuite : qualité des données (§3.5), budget enrichi (§3.7).

---

## 5. Verdict MOA

### GO livraison — Palier 4 réaligné (2026-05-28)

**Décision MOA : GO livraison branche.** Le Palier 4 est considéré comme **réaligné et figé** en **`19.0.4.9.0`**.

| Point validé | Statut |
|---|---|
| Grammaire Ressources · Cumul RH · Dépenses · Solde | OK |
| Libellés « Dépenses hors salaires » | OK |
| Filtre Axe analytique conservé au refresh | OK |
| Titre dynamique selon axe filtré | OK |
| Messages budget absent (`has_budget_data`) | OK |
| Contrôle RH V1 (onglet Infos) | OK |
| Non-régression post-install | **88 tests · 0 failed · 0 error(s)** |
| Doctrine compte bancaire de référence | Consignée séparément ([db07117](https://github.com/doreviateam/odoo19-addons-dorevia/commit/db07117)) — **sans impact code** |

**Réserve structurante :** bloc trésorerie / compte bancaire de référence → **Palier 5**, non implémenté dans `19.0.4.9.0`.

**Décision :** Palier 4 réaligné **gelé** · prochaine séquence = **cadrage Palier 5 avant tout code**.

### Preuve technique recette R17

Rejeu serveur `glc-rgl-test-import` :

| Contrôle | Résultat |
|---|---|
| Upgrade `-u dorevia_glc_analytics` + restart worker | OK |
| Version confirmée | **`19.0.4.9.0`** (`dorevia_glc_budget` inchangé **`19.0.1.0.0`**) |
| Post-install analytics + budget | **88 tests · 0 failed · 0 error(s)** (84 + 14) |
| Filtre axe BAR, contrôle RH, libellés | Validés serveur + templates OWL |

**Note logs :** erreurs SQL `duplicate key` budget / ligne budget — **attendues** (tests contraintes unicité).

**Réserve non bloquante :** compléments manuels **R14-CAISSE / R14-OD / R14-645-REEL** — données réelles / poste MOA local.

**Lots suivants (hors Palier 4 gelé) :**

- budget multi-axes / réalisé non budgété par axe ;
- onglet **Données exclues / à contrôler** (§3.5) ;
- **Palier 5** — trésorerie / compte bancaire de référence ([TICKET_PALIER_5_TRESORERIE_COMPTE_BANCAIRE_REFERENCE.md](./TICKET_PALIER_5_TRESORERIE_COMPTE_BANCAIRE_REFERENCE.md)).

**GO trajectoire** — le module est un **tableau de bord de pilotage d'exploitation** avec réalignement métier **`19.0.4.9.0`**.

---

## 6. Séquence de lecture cockpit (validée MOA)

1. **Où en est-on ?** → KPI globaux (Synthèse)
2. **Quelle tendance ?** → Solde mensuel
3. **D'où vient le déséquilibre ?** → Structure mensuelle (Recette / Cumul RH / Dépense + courbe solde)
4. **Quels axes expliquent le résultat ?** → Solde par axe analytique (Détail)

---

## 7. Critères d'acceptation (à décliner par PR)

- [x] CA-DOC — Manifeste + docs + recette alignés sur doctrine réalisé / Palier 2 / budget
- [x] CA-LBL — « Dépenses hors salaires » en UI à la place de « Frais généraux » là où le calcul est multi-axes
- [x] CA-BUD — Message « non budgété » / `has_budget_data` si budget absent *(partiel — par axe : lot suivant)*
- [x] CA-FIL — Option A : filtre **Axe analytique** réimplémenté et conservé au refresh
- [ ] CA-QD — Bloc ou onglet données exclues (V1 synthétique acceptable)
- [x] CA-RH — KPI Paie comptable vs ventilation RH (informatif) — onglet Infos
- [x] CA-VER — Version recette = **`19.0.4.9.0`** au moment du GO technique R17

---

*Ticket ouvert post-GO UX synthèse + détail (`19.0.4.8.x`). Implémentation par lots — ne pas mélanger avec correctifs UX ponctuels sans mise à jour de ce ticket.*
