# Recette manuelle — Contrôle de gestion · Filtre « Payé uniquement » (tableau détail)

> **Doc alignée `19.0.14.1.0`** — menu **Contrôle de gestion**. Sections historiques conservées.

**Module :** `dorevia_glc_analytics`  
**Version testée :** **`19.0.9.0.1`** *(min. **`19.0.14.1.0`** pour menus actuels)*  
**Prérequis :** Contrôle de gestion · Palier 5 trésorerie  
**Statut document :** **GO complet MOA** — serveur OK · validation visuelle MOA OK

**Références :** [TICKET_COCKPIT_DETAIL_PAYE_UNIQUEMENT.md](../TICKET_COCKPIT_DETAIL_PAYE_UNIQUEMENT.md) · [Recette période libre Palier 4](./RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md) · [Recette qualité / paiement](./RECETTE_MANUELLE_COCKPIT_QUALITE_PAIEMENT.md)

---

## Objectif

Prouver **indépendamment** de l’observation visuelle sur données historiques que le filtre **« Payé uniquement »** du tableau **Détail par axe analytique** :

- restitue la vue **engagée / comptable** lorsqu’il est décoché ;
- n’affiche que les montants **payés / encaissés / réconciliés** lorsqu’il est coché ;
- recalcule **Ressources · Cumul RH · Dépenses · Solde**, sous-totaux mensuels et total période ;
- filtre le **Cumul RH** selon le rapprochement réel (pas par construction) ;
- ne régresse pas le filtre **Budget ?**.

> **Note MOA importante :** si le Cumul RH reste identique entre les deux vues sur une période donnée, cela peut être **normal** lorsque toutes les écritures RH sont déjà réconciliées. Le cas **RT-PAY-08** (RH non réconciliée) est **obligatoire** pour prouver le comportement différentiel.

---

## Contexte de recette

```text
URL  : http://localhost:18079
Base : glc-rgl-test-import
Menu : Facturation → Pilotage GLC → Contrôle de gestion
Onglet : Détail par axe analytique
```

---

## 1. Préconditions

### 1.1 Installation / upgrade

```bash
cd sandbox-odoo19
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d glc-rgl-test-import -u dorevia_glc_analytics \
  --stop-after-init --no-http

docker compose restart odoo
```

| Contrôle | Attendu | OK | Observations |
|---|---|:---:|---|
| Version module | **`19.0.9.0.1`** ou supérieure | [ ] | |
| Hard refresh navigateur | `Cmd+Shift+R` | [ ] | |
| Cockpit **rechargé** après upgrade | Bouton Recharger | [ ] | Alimente les champs `*_paid` |

### 1.2 Jeu de données minimum (période test maîtrisée)

Sur **un même mois** (recommandé : **juin** d’une année isolée), disposer de :

| Situation | Axe analytique suggéré | Montant recette serveur | Réf. |
|---|---|---:|---|
| Ressource **encaissée** (facture client payée) | Bar | **1 100 €** | RT-PAY-03 |
| Ressource **non encaissée** (facture client impayée) | Bar | **820 €** | RT-PAY-04 |
| Dépense **payée** (facture fournisseur payée) | Structure & Administration | **430 €** | RT-PAY-05 |
| Dépense **non payée** | Structure & Administration | **310 €** | RT-PAY-06 |
| RH **payée / réconciliée** (facture fournisseur 645 payée) | Prestations | **520 €** | RT-PAY-07 |
| RH **non payée / non réconciliée** (facture 645 impayée) | Prestations | **610 €** | RT-PAY-08 |
| Écriture **banque sans facture** (OD journal bancaire + analytique) | Missions | **275 €** | RT-PAY-09 |
| Virement interne **580 + VIR_INT** (entrée banque) | Virement interne | **9 000 €** | RT-PAY-09 |

**Montants engagés attendus (juin, recette serveur) :**

| Colonne | Vue complète | Vue payée uniquement |
|---|---:|---:|
| Ressource | **10 920 €** *(1 100 + 820 + 9 000)* | **10 100 €** *(1 100 + 9 000)* |
| Cumul RH | **1 130 €** *(520 + 610)* | **520 €** |
| Dépense | **1 015 €** *(430 + 310 + 275)* | **705 €** *(430 + 275)* |
| Solde | **8 775 €** | **8 875 €** |

Formule : **Solde = Ressource − Cumul RH − Dépense** (sur les montants de la vue active).

### 1.3 Rejeu serveur automatisé (données maîtrisées)

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d glc-rgl-test-import -u dorevia_glc_analytics \
  --test-enable \
  --test-tags /dorevia_glc_analytics:TestGlcCoverageCockpitDetailPaidRecette \
  --stop-after-init --no-http
```

| Lot | Attendu | OK | Observations |
|---|---|:---:|---|
| `TestGlcCoverageCockpitDetailPaidRecette` | **2/2 OK** · 0 failed | [x] | Rejeu 2026-05-30 |
| Tests unitaires DET-PAY | **3/3 OK** | [x] | Rejeu 2026-05-30 · `TestGlcCoverageCockpitDetailPaid` |

### 1.4 Semence navigateur (optionnel)

Pour rejouer la recette visuellement sur la sandbox avec les montants § 1.2 :

```bash
docker compose exec -T odoo odoo shell -c /etc/odoo/odoo.conf \
  -d glc-rgl-test-import --no-http < /mnt/odoo19-addons-dorevia/dorevia_glc_analytics/scripts/recette_detail_paid_seed.py
```

Noter l’**ID cockpit** et la **période** affichés en sortie.

Exemple rejeu sandbox (2026-05-30) :

```text
Cockpit ID: 2830
Période: 2051-06-01 → 2051-06-30
Vue complète  — Ressource 10 920 € · RH 1 130 € · Dépense 1 015 € · Solde 8 775 €
Vue payée     — Ressource 10 100 € · RH 520 € · Dépense 705 € · Solde 8 875 €
```

---

## 2. Cas de test RT-PAY

### RT-PAY-01 — Vue complète, filtre décoché

| Étape | Action |
|---|---|
| 1 | Ouvrir le cockpit sur la période test (juin). |
| 2 | Onglet **Détail par axe analytique**. |
| 3 | **Décocher** « Payé uniquement ». |
| 4 | Relever par axe et sous-total mensuel : Ressources · Cumul RH · Dépenses · Solde. |

**Résultat attendu**

- Toutes les écritures éligibles visibles (payées **et** non payées).
- Comportement identique à la vue historique avant filtre.
- Sous-total mensuel = somme des lignes d’axes.
- Total période = somme des sous-totaux.

| Contrôle | Attendu recette § 1.2 | OK | Relevé |
|---|---|:---:|:---:|
| Bar · Ressource | **1 920 €** | [ ] | |
| Prestations · Cumul RH | **1 130 €** | [ ] | |
| Structure · Dépense | **740 €** | [ ] | |
| Missions · Dépense | **275 €** | [ ] | |
| VIR_INT · Ressource | **9 000 €** | [ ] | |
| Sous-total · Solde | **8 775 €** | [ ] | |

---

### RT-PAY-02 — Vue payée uniquement, filtre coché

| Étape | Action |
|---|---|
| 1 | **Cocher** « Payé uniquement » sur le même mois. |
| 2 | Relever les mêmes colonnes et sous-total. |

**Résultat attendu**

- Seuls les montants payés / encaissés / réconciliés restent.
- **Solde recalculé** : Ressource payée − Cumul RH payé − Dépense payée.
- Sous-total et total période **cohérents** avec les lignes (pas de totaux engagés).

| Contrôle | Attendu recette § 1.2 | OK | Relevé |
|---|---|:---:|:---:|
| Bar · Ressource | **1 100 €** | [ ] | |
| Prestations · Cumul RH | **520 €** | [ ] | |
| Structure · Dépense | **430 €** | [ ] | |
| Missions · Dépense | **275 €** | [ ] | |
| VIR_INT · Ressource | **9 000 €** | [ ] | |
| Sous-total · Solde | **8 875 €** | [ ] | |
| Lignes sans montant payé | Tirets **—** | [ ] | |

---

### RT-PAY-03 — Ressource payée conservée

| Préparation | Facture client **payée** sur **Bar** (ex. **1 100 €**). |
|---|---|

| Vue | Ressource Bar attendue | OK | Relevé |
|---|:---:|:---:|:---:|
| Filtre **décoché** | **≥ 1 100 €** (inclut aussi impayée si présente) | [ ] | |
| Filtre **coché** | **1 100 €** minimum (part payée visible) | [ ] | |

---

### RT-PAY-04 — Ressource non payée exclue

| Préparation | Facture client **impayée** sur **Bar** (ex. **820 €**). |
|---|---|

| Vue | Comportement attendu | OK |
|---|:---:|:---:|
| Filtre **décoché** | **820 €** visibles dans Ressource Bar | [ ] |
| Filtre **coché** | **820 €** absents du montant Ressource Bar | [ ] |
| Solde / sous-total | Recalculés sans les **820 €** | [ ] |

---

### RT-PAY-05 — Dépense payée conservée

| Préparation | Facture fournisseur **payée** sur **Structure** (ex. **430 €**). |
|---|---|

| Vue | Dépense Structure | OK |
|---|:---:|:---:|
| Décoché | **430 €** visibles | [ ] |
| Coché | **430 €** conservés | [ ] |

---

### RT-PAY-06 — Dépense non payée exclue

| Préparation | Facture fournisseur **impayée** sur **Structure** (ex. **310 €**). |
|---|---|

| Vue | Comportement | OK |
|---|:---:|:---:|
| Décoché | **310 €** visibles | [ ] |
| Coché | **310 €** exclus | [ ] |
| Solde | Recalculé sans **310 €** | [ ] |

---

### RT-PAY-07 — Cumul RH payé conservé

| Préparation | Facture fournisseur **645** payée sur **Prestations** (ex. **520 €**). |
|---|---|

| Vue | Cumul RH Prestations | OK |
|---|:---:|:---:|
| Décoché | **520 €** minimum (plus impayée si RT-PAY-08) | [ ] |
| Coché | **520 €** conservés | [ ] |

> Si toutes les RH de la période sont réconciliées, les deux vues peuvent afficher le **même** total RH : ce n’est **pas** une anomalie sans RT-PAY-08.

---

### RT-PAY-08 — Cumul RH non payé exclu *(obligatoire)*

| Préparation | Facture fournisseur **645 impayée** sur **Prestations** (ex. **610 €**). |
|---|---|

| Vue | Cumul RH Prestations | OK |
|---|:---:|:---:|
| Décoché | **1 130 €** *(520 + 610)* | [ ] |
| Coché | **520 €** *(610 exclus)* | [ ] |
| Solde | Augmente de **610 €** en vue payée vs engagée sur cet axe | [ ] |

**Ce test prouve que le Cumul RH est filtré** — il ne reste identique que si toutes les RH sont déjà payées.

---

### RT-PAY-09 — Écriture bancaire sans facture

| Préparation | OD journal bancaire : charge **622** + analytique **Missions** **275 €** (sans facture). Virement **580 → VIR_INT** **9 000 €**. |
|---|---|

| Écriture | Colonne | Vue payée | OK |
|---|---|:---:|:---:|
| Banque sans facture **275 €** | Dépense Missions | Visible (**275 €**) | [ ] |
| Virement **580** entrée | Ressource VIR_INT | Visible (**9 000 €**) | [ ] |

Règle : écriture sur compte **512 / 53 / 580** ou pièce contenant une ligne banque → **payée**.

---

### RT-PAY-10 — Non-régression Budget ?

| Combinaison | Attendu | OK |
|---|:---:|:---:|
| Payé **décoché** + Budget **décoché** | 5 colonnes · montants engagés | [ ] |
| Payé **coché** + Budget **décoché** | 5 colonnes · montants payés | [ ] |
| Payé **décoché** + Budget **coché** | 13 colonnes · écarts sur engagé | [ ] |
| Payé **coché** + Budget **coché** | 13 colonnes · écarts sur **payé** · budget inchangé | [ ] |

Contrôles supplémentaires :

- [ ] Aucune erreur JS / popup à la bascule des cases.
- [ ] Préférence « Payé uniquement » persistée après rechargement page (`localStorage`).
- [ ] KPI onglets **Ressources** / **Charges de structure** **inchangés** par le filtre détail.

---

## 3. Règle technique « payé » (rappel Dev)

| Source | Inclus en vue payée ? |
|---|---|
| Facture client / fournisseur / avoir | Oui si `payment_state = paid` uniquement |
| Écriture banque **512 / 53 / 580** | Oui |
| Pièce avec ligne banque | Oui |
| Ligne lettrée avec compte banque | Oui |
| Ligne analytique sans `move_line_id` | **Non** |
| Virement interne **580** qualifié (VIR_INT) | **Oui** (toujours) |

---

## 4. Critères de GO MOA

- [ ] **RT-PAY-01** — vue complète = historique
- [ ] **RT-PAY-02** — vue payée + solde recalculé + sous-totaux cohérents
- [ ] **RT-PAY-03 / 04** — ressource payée / non payée
- [ ] **RT-PAY-05 / 06** — dépense payée / non payée
- [ ] **RT-PAY-07 / 08** — RH payée / **RH non payée exclue**
- [ ] **RT-PAY-09** — banque sans facture + 580 VIR_INT
- [ ] **RT-PAY-10** — Budget ? sans régression
- [ ] Rejeu serveur **0 failed**

### Verdict

| Champ | Valeur |
|---|---|
| Date recette | |
| Exécutant | |
| Version testée | `dorevia_glc_analytics 19.0.9.0.1` |
| Période testée | `2051-06-01 → 2051-06-30` |
| Rejeu serveur | [x] **2/2 OK** (2026-05-30) |
| Rejeu DET-PAY | [x] **3/3 OK** (2026-05-30) |
| Semence sandbox | [x] **Cockpit ID 2830** |
| Rejeu navigateur | [x] **OK visuel MOA** — captures du 2026-05-30 |

- [x] **GO complet**
- [ ] **GO avec réserve**
- [ ] **NO GO**

---

## 5. Compte-rendu rejeu serveur indépendant

**Exécution :** 2026-05-30 · base `glc-rgl-test-import`

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d glc-rgl-test-import \
  --test-enable \
  --test-tags /dorevia_glc_analytics:TestGlcCoverageCockpitDetailPaidRecette \
  --stop-after-init --no-http
```

| Test | Cas couverts | Résultat |
|---|---|:---:|
| `test_rt_pay_recette_complete` | RT-PAY-01 … 09 · sous-totaux | **OK** |
| `test_rt_pay_10_budget_variance_unchanged` | RT-PAY-10 | **OK** |

**Verdict serveur :** **GO** — jeu RT-PAY reproductible et indépendant des données historiques sandbox.

### Rejeu complémentaire 2026-05-30

| Contrôle | Résultat |
|---|---:|
| `TestGlcCoverageCockpitDetailPaidRecette` | **2/2 OK** |
| `TestGlcCoverageCockpitDetailPaid` | **3/3 OK** |
| Échecs | **0 failed** |
| Erreurs | **0 error** |

Semence sandbox exécutée :

```text
Cockpit ID: 2830
Période: 2051-06-01 → 2051-06-30
URL: http://localhost:18079/web#id=2830&model=glc.coverage.cockpit&view_type=form
```

Montants serveur semencés :

| Vue | Ressource | Cumul RH | Dépense | Solde |
|---|---:|---:|---:|---:|
| Complète | `10 920 €` | `1 130 €` | `1 015 €` | `8 775 €` |
| Payée uniquement | `10 100 €` | `520 €` | `705 €` | `8 875 €` |

Tentative navigateur Codex :

```text
Bloquée par la politique réseau locale : accès refusé à http://localhost:18079.
```

**Verdict Codex :** **GO serveur**.

### Validation visuelle MOA 2026-05-30

Validation visuelle fournie par captures écran sur données historiques sandbox.

| Contrôle visuel | Résultat |
|---|---|
| Case **Payé uniquement** visible à côté de **Budget ?** | **OK** |
| Vue complète décochée lisible | **OK** |
| Vue payée uniquement cochée lisible | **OK** |
| Montants non payés remplacés par tirets dans la vue payée | **OK** |
| Sous-totaux mensuels recalculés | **OK** |
| Total période recalculé | **OK** |
| Solde recalculé selon la vue active | **OK** |
| Aucune anomalie visuelle bloquante remontée | **OK** |

Commentaire MOA :

```text
Pour moi d'un point de vue visuel, ça va.
```

**Verdict final : GO complet MOA.**

*Recette navigateur MOA : compléter § 2 avec les relevés colonne « Relevé » puis cocher le verdict § 4.*
