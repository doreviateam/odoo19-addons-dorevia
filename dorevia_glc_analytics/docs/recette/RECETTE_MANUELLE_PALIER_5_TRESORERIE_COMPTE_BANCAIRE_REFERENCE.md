# Recette manuelle — Palier 5 · Trésorerie & compte bancaire de référence

**Module :** `dorevia_glc_analytics` (extension Palier 5)  
**Version cible :** **`19.0.5.0.1`**  
**Prérequis :** Palier 4 réaligné **`19.0.4.9.0`** gelé  
**Statut document :** **GO complet MOA** — Palier 5 **`19.0.5.0.1`** (2026-05-29) · précondition bancaire OK · **95/95** post-install · TREF **7/7** · recette navigateur §2 à §5 OK

**Références :** [TICKET_PALIER_5_TRESORERIE_COMPTE_BANCAIRE_REFERENCE.md](../TICKET_PALIER_5_TRESORERIE_COMPTE_BANCAIRE_REFERENCE.md) · [TICKET_COCKPIT_COMPTE_BANCAIRE_REFERENCE.md](../TICKET_COCKPIT_COMPTE_BANCAIRE_REFERENCE.md) · [Recette période libre Palier 4](./RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md) · [PALIERS.md](../PALIERS.md)

---

## Invariant à prouver

> **Un cockpit = période + compte bancaire de référence + lecture trésorerie séparée.**  
> **Les KPI d’exploitation (Ressources · Cumul RH · Dépenses · Solde) ne changent jamais quand on change de compte bancaire.**

| Couche | Rôle |
|---|---|
| Compte bancaire de référence | Point de vue **trésorerie** (défaut GLC : compte courant) |
| Compte comptable | Nature comptable (classes 6/7, 512, 580…) |
| Compte analytique | Qualification métier GLC |

---

## Contexte de recette

```text
URL  : http://localhost:18079
Base : glc-rgl-test-import
Menu : Facturation → Pilotage GLC → Contrôle de gestion
```

*(Libellé technique ; équivalent MOA « Cockpit GLC »)*

---

## 1. Préconditions

### 1.1 Installation / upgrade

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d glc-rgl-test-import -u dorevia_glc_analytics \
  --stop-after-init --no-http

docker compose restart odoo
```

| Contrôle | Attendu | OK | Observations |
|---|---|:---:|---|
| Version module `dorevia_glc_analytics` | **`19.0.5.0.1`** | [x] | Rejeu confirmé 2026-05-29 |
| *(budget retiré)* | — | [x] | Inchangé |
| Worker Odoo redémarré après `-u` | Oui | [x] | |
| Hard refresh navigateur | `Cmd+Shift+R` | [x] | Recette navigateur § 2–5 validée |

### 1.2 Société GLC — journal bancaire par défaut

**Paramétrage MOA :** fiche **Société** → champ **Journal bancaire cockpit GLC** (`glc_default_bank_journal_id`).

> **Recette `glc-rgl-test-import` (2026-05-29) — précondition bancaire validée :** société **`My Company`** · journal par défaut **`Compte Courant GLC`** · journaux disponibles : `Compte Courant GLC`, `GLC - Livret Bleu`, `GLC - Livret OBNL`.

**Procédure *(référence)* :**

1. **Paramètres** → **Sociétés** → société GLC.
2. Renseigner **Journal bancaire cockpit GLC** = **`Compte Courant GLC`**.
3. Enregistrer · rouvrir le cockpit · vérifier le préremplissage du filtre **Compte bancaire de référence**.

| Contrôle | Attendu | OK | Observations |
|---|---|:---:|---|
| Société | **`My Company`** | [x] | |
| Champ société **Journal bancaire cockpit GLC** | **`Compte Courant GLC`** | [x] | Précondition bancaire OK |
| Journaux bancaires disponibles | Compte courant + livrets | [x] | `Compte Courant GLC` · `GLC - Livret Bleu` · `GLC - Livret OBNL` |
| Au moins un **second** journal pour TREF-03 / TREF-05 | Livret | [x] | `GLC - Livret Bleu` |
| Compte 512 dérivé visible sur le cockpit | Champ **Compte 512 de référence** | [x] | Related depuis le journal société |

### 1.3 Données de test

| Élément | Attendu | OK | Observations |
|---|---|:---:|---|
| Période de test choisie | Ex. un mois complet avec mouvements | [x] | `13 avr. → 31 mai 2026` |
| Cockpit ouvert sur cette période | Synthèse + Détail + Trésorerie alimentés ou message « aucune donnée » | [x] | Détail + Trésorerie alimentés |
| Écritures comptables sur compte courant | Encaissements / décaissements sur la période | [x] | Courant : entrées `14 272,07 €` · sorties `15 899,18 €` |
| Écriture virement interne courant ↔ livret *(optionnel)* | Sur la période | [x] | Couvert auto TREF-03 ; flux navigateur livrets observés |

---

## 2. Vérification du champ compte bancaire

**Zone :** groupe **Filtres de lecture** (formulaire cockpit).

| Réf. | Point de contrôle | Attendu | OK | Observations |
|---|---|---|:---:|---|
| P5-FIL-VIS | Champ **Compte bancaire de référence** visible | Oui | [x] | `reference_bank_journal_id` |
| P5-FIL-DOM | Liste proposée | Journaux **type banque** de la société uniquement | [x] | `Compte Courant GLC` · `GLC - Livret Bleu` · `GLC - Livret OBNL` |
| P5-FIL-DEF | Valeur à l’ouverture | Journal **compte courant** GLC (défaut société) | [x] | `Compte Courant GLC` |
| P5-FIL-512 | Compte 512 affiché | Cohérent avec le journal sélectionné | [x] | Courant `512001 Banque` · Livret Bleu `512004 GLC - Livret Bleu` |
| P5-FIL-PERS | Persistance au refresh | Compte sélectionné **conservé** après changement période / scénario / recalcul | [x] | Période `13 avr. → 31 mai` conservée |

**Procédure persistance :**

1. Sélectionner le journal **livret** (ou second compte bancaire).
2. Modifier la **date de fin** ou le **scénario budgétaire**.
3. Attendre le recalcul automatique (autosave filtres).
4. Vérifier que **Compte bancaire de référence** reste sur le livret.

**Résultat MOA navigateur (2026-05-29) :** **OK**.

| Réf. | Résultat observé |
|---|---|
| P5-FIL-VIS | Champ visible dans **Filtres de lecture** |
| P5-FIL-DOM | Journaux disponibles : `Compte Courant GLC`, `GLC - Livret Bleu`, `GLC - Livret OBNL` |
| P5-FIL-DEF | Valeur d'ouverture : `Compte Courant GLC` |
| P5-FIL-512 | Courant : `512001 Banque` · Livret Bleu : `512004 GLC - Livret Bleu` |
| P5-FIL-PERS | Période conservée `13 avr. → 31 mai` après bascule compte |

---

## 3. Vérification non-régression exploitation

**Objectif :** prouver que le Palier 4 reste **gelé** — seule la trésorerie réagit au compte bancaire.

### 3.1 Relevé initial (compte courant)

Période figée : du **13 avr.** au **31 mai 2026**

| KPI exploitation | Valeur relevée (compte courant) | Source UI |
|---|---|---|
| **Recette** | **7 794,00 €** | Onglet **Détail par axe analytique** · Total période |
| **Cumul RH** | **0,00 €** | Onglet **Détail par axe analytique** · Total période |
| **Dépense** | **4 851,51 €** | Onglet **Détail par axe analytique** · Total période |
| **Solde** | **2 942,49 €** | Onglet **Détail par axe analytique** · Total période |

*(Alternative détaillée : onglet **Détail par axe analytique** — totaux RECETTE | CUMUL RH | DÉPENSE | SOLDE.)*

### 3.2 Changement de compte bancaire

1. Noter les **quatre KPI** ci-dessus.
2. Changer **Compte bancaire de référence** → journal **livret** (ou autre compte).
3. Laisser le cockpit recalculer.

| KPI | Valeur après changement | Identique ? | OK |
|---|---|---|:---:|
| Recette | **7 794,00 €** | **Oui — obligatoire** | [x] |
| Cumul RH | **0,00 €** | **Oui — obligatoire** | [x] |
| Dépense | **4 851,51 €** | **Oui — obligatoire** | [x] |
| Solde | **2 942,49 €** | **Oui — obligatoire** | [x] |

**Verdict section 3 :**

- [x] **OK** — aucun KPI exploitation modifié
- [ ] **NO GO** — au moins un KPI exploitation a changé *(bloquant)*

---

## 4. Vérification onglet Trésorerie

**Onglet :** **Trésorerie** (bloc séparé de Synthèse et Détail).

Texte d’aide attendu : *« Les KPI Ressources · Cumul RH · Dépenses · Solde ne dépendent pas du compte bancaire sélectionné. »*

### 4.1 Compte courant sélectionné

| Indicateur trésorerie | Valeur relevée | OK | Observations |
|---|---|:---:|---|
| **Entrées trésorerie** | **14 272,07 €** | [x] | `treasury_inflow` |
| **Sorties trésorerie** | **15 899,18 €** | [x] | `treasury_outflow` |
| **Virements internes (entrées)** | **0,00 €** | [x] | Si virement reçu sur le compte observé |
| **Virements internes (sorties)** | **0,00 €** | [x] | Si virement émis depuis le compte observé |
| **Solde trésorerie période** | **-1 627,11 €** | [x] | Entrées − sorties · `treasury_net` |

Cohérence rapide : comparer avec les écritures **512** du journal courant sur la période (comptabilité → grand livre filtré).

### 4.2 Bascule vers le livret

1. Relever les indicateurs trésorerie du **compte courant** (§ 4.1).
2. Changer **Compte bancaire de référence** → **livret**.
3. Ouvrir à nouveau l’onglet **Trésorerie**.

| Contrôle | Attendu | OK | Observations |
|---|---|:---:|---|
| Montants trésorerie | **Différents** du compte courant (si mouvements sur le livret) | [x] | `GLC - Livret Bleu` : entrées `30 000,00 €` · sorties `0,00 €` · solde `30 000,00 €` |
| KPI exploitation (§ 3) | **Identiques** | [x] | Recette `7 794,00 €` · Cumul RH `0,00 €` · Dépense `4 851,51 €` · Solde `2 942,49 €` |
| Message si pas de mouvement | *« Aucun mouvement trésorerie sur le compte de référence… »* | [ ] | `treasury_has_data = False` |

**Verdict section 4 :**

- [x] **OK** — trésorerie réactive au compte · exploitation stable
- [ ] **GO avec réserve** — défaut UX sans impact calcul
- [ ] **NO GO** — trésorerie absente alors que mouvements 512 existent · ou exploitation impactée

---

## 5. Scénarios TREF manuels

Compléter sur **données réelles** ou jeux d’écritures dédiés sur `glc-rgl-test-import`.

| ID | Scénario | Préparation | Exploitation attendue | Trésorerie attendue | OK | Observations |
|---|---|---|---|---|:---:|---|
| **TREF-01** | Encaissement client | Crédit compte courant + recette analytique (ex. BAR) | **Recette** ↑ | **Entrée** trésorerie compte courant | [x] | Couvert auto |
| **TREF-02** | Paiement fournisseur | Débit compte courant + dépense analytique (ex. 626 / STRUCTURE) | **Dépense** ↑ | **Sortie** trésorerie | [x] | Couvert auto |
| **TREF-03** | Virement courant → livret | Écriture 512↔512 ou compte 580 | **Aucun** impact Ressources · Cumul RH · Dépenses · Solde | Visible : **sortie** courant · **entrée** livret | [x] | Couvert auto |
| **TREF-04** | Paie / 645 rapprochée banque | Charge 645 + analytique STRUCTURE + sortie banque | **Cumul RH** ↑ | **Sortie** trésorerie | [x] | Couvert auto |
| **TREF-05** | Changement compte de référence | Même période · courant puis livret | KPI exploitation **strictement identiques** | Flux **recalculés** selon nouveau POV | [x] | Validé auto + navigateur |

### Grille TREF-05 (détail MOA)

| KPI / indicateur | Compte courant | Livret | Égal exploitation ? |
|---|---|---|---|
| Recette | **7 794,00 €** | **7 794,00 €** | [x] Oui |
| Cumul RH | **0,00 €** | **0,00 €** | [x] Oui |
| Dépense | **4 851,51 €** | **4 851,51 €** | [x] Oui |
| Solde | **2 942,49 €** | **2 942,49 €** | [x] Oui |
| Entrées trésorerie | **14 272,07 €** | **30 000,00 €** | N/A *(peut différer)* |
| Sorties trésorerie | **15 899,18 €** | **0,00 €** | N/A |
| Solde trésorerie période | **-1 627,11 €** | **30 000,00 €** | N/A |

---

## 6. Tests automatisés (non-régression)

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d glc-rgl-test-import -u dorevia_glc_analytics \
  --test-enable --test-tags post_install \
  --stop-after-init --no-http
```

### Résultat rejeu serveur — GO technique (2026-05-29)

| Étape | Résultat |
|---|---|
| `-u dorevia_glc_analytics` | OK |
| Restart worker Odoo | OK |
| Précondition bancaire société | OK — **`Compte Courant GLC`** |
| Version `dorevia_glc_analytics` | **`19.0.5.0.1`** |
| Budget module | **Retiré** |
| Migration nomenclature legacy | OK — `19.0.5.0.1/post-migrate.py` |
| Post-install global | **95 tests · 0 failed · 0 error(s)** |
| Rejeu ciblé Palier 5 / TREF | **7/7 OK · 0 failed · 0 error(s)** |
| Recette navigateur §2 à §5 | **OK** |

**Migration `19.0.5.0.1` — réalignement codes Activités GLC** *(sans recréation de comptes ni déplacement d’écritures)* :

| Legacy | Cible |
|---|---|
| `STR_ADM` | `STRUCTURE` |
| `BAR_REST` | `BAR` |
| `PRESTA` | `PRESTATIONS` |
| `RES_EXT` | `RESIDENCES` |
| `DEPL_MIS` | `MISSIONS` |
| `LOC_PRIV` | `PRIVATISATIONS` |
| `LOC_RGL` | `LOCATION_RADIO` |

| Lot | Tests | Résultat |
|---|---|---|
| `TestGlcCoverageCockpit` (Palier 4) | 49 | **0 failed** |
| `TestGlcCoverageCockpitTreasury` (TREF auto) | 7 | **0 failed** |
| `TestGlcBudget` | 14 | **0 failed** *(SQL duplicate key attendus — contraintes unicité)* |
| Autres analytics (`test_analytic_setup`, …) | 25 | **0 failed** |
| **Total post-install** | **95** | **95 OK · 0 failed · 0 error(s)** |

**Périmètre Palier 5 + non-régression cockpit/budget :** **70/70 verts** (49 + 7 + 14).

| Réf. | Contrôle auto | OK |
|---|---|:---:|
| P5-AUTO-TREF | TREF-01 à TREF-05 automatisés | [x] |
| P5-AUTO-ISO | `test_tref05_reference_bank_change_preserves_exploitation_kpis` | [x] |
| P5-AUTO-VIR | `test_tref03_internal_transfer_excluded_from_exploitation` | [x] |
| P5-AUTO-PERS | `test_reference_bank_journal_persisted_on_refresh` | [x] |
| P5-AUTO-DEF | `test_default_reference_bank_from_company` | [x] |

---

## 7. Verdict recette

### Critères de décision MOA

| Verdict | Condition |
|---|---|
| **GO** | 70 tests cockpit/TREF/budget verts **et** recette manuelle § 2–5 confirme l’invariant · **95/95** |
| **GO technique serveur** | Rejeu auto complet **95/95** · préconditions § 1 OK · recette navigateur § 2–5 optionnelle |
| **GO avec réserve** | Calculs OK · défaut UX onglet Trésorerie sans impact métier |
| **NO GO** | Changement de compte bancaire modifie Ressources · Cumul RH · Dépenses · Solde **ou** virement interne compté en exploitation |

### Verdict MOA

- [ ] **GO technique serveur** — Palier 5 **`19.0.5.0.1`** *(2026-05-29)* · **95/95**
- [x] **GO complet** *(recette navigateur § 2–5 validée)*
- [ ] **NO GO**

**Verdict final Palier 5 :** **GO complet MOA avant PR / merge.**

| Champ | Valeur |
|---|---|
| Date rejeu serveur | **2026-05-29** (recette terminée) |
| Exécutant | MOA |
| Version testée | **`19.0.5.0.1`** |
| Base | `glc-rgl-test-import` |
| Société | **`My Company`** |
| Journal société (défaut cockpit) | **`Compte Courant GLC`** |
| Journaux banque disponibles | `Compte Courant GLC` · `GLC - Livret Bleu` · `GLC - Livret OBNL` |
| Tests cockpit + TREF + budget | **70/70 OK** |
| Rejeu ciblé TREF | **7/7 OK** |
| Post-install global | **95/95 OK** |
| Recette navigateur §2 à §5 | **OK** |
| Preuve invariant exploitation | Courant = Livret Bleu : Recette `7 794,00 €` · Cumul RH `0,00 €` · Dépense `4 851,51 €` · Solde `2 942,49 €` |
| Preuve trésorerie POV | Courant `-1 627,11 €` · Livret Bleu `30 000,00 €` |

**Réserves optionnelles (non bloquantes) :**

- Compléments manuels TREF-04 sur données réelles *(R14-645-REEL)*, déjà couvert côté tests automatisés ;
- Exports Excel/PDF, scénarios budget, projections et commentaires de gestion restent hors lot trésorerie S1.

---

## 8. Séquence de lecture cockpit (post-Palier 5)

1. **Exploitation** — Synthèse / Détail : Ressources · Cumul RH · Dépenses · Solde *(indépendant du compte bancaire)* ;
2. **Trésorerie** — onglet dédié : entrées / sorties / virements / solde période *(selon compte bancaire de référence)* ;
3. **Contrôle RH** — onglet Infos *(Palier 4 — inchangé)*.

---

*Recette Palier 5 `19.0.5.0.1` validée MOA le 2026-05-29. Ne pas confondre avec la recette Palier 4 période libre — celle-ci reste valide pour l’exploitation seule.*
