# Livraison MOA — `dorevia_glc_analytics`

**Version livrée :** **`19.0.15.0.0`**  
**Date de gel :** 2026-05-30  
**Statut :** **Terminé — prêt pour recette et acceptation MOA**  
**Base recette :** `glc-rgl-test-import` (sandbox)  
**Tests automatisés :** **106 / 106 verts** (`/dorevia_glc_analytics`)

---

## 1. Objet de la livraison

Module Odoo 19 **`dorevia_glc_analytics`** — pilotage GLC sur **réalisé comptable analytique** :

| Entrée menu | Fonction |
|---|---|
| **Contrôle de gestion** | Tableau de bord + détail exploitation (Ressources · Cumul RH · Dépenses · Solde) |
| **Axes analytiques** | Paramétrage des 11 axes du plan GLC |
| **Audit** | Contrôles analytiques A1–A2, A4–A6 |

**Chemin :** Facturation → Pilotage GLC

---

## 2. Périmètre livré (IN)

| Domaine | Détail |
|---|---|
| Plan analytique unique | 11 axes (`GLC - Activités`) |
| Contrôle de gestion | Tableau de bord, détail par axe, charges de structure |
| Période libre | Sélecteur compact, recalcul automatique |
| Trésorerie | Compte bancaire de référence, onglet dédié |
| Qualité & paiement | Contrôles qualité (Q1–Q2), tiers & paiements (Q3), KPI lettrage |
| Audit analytique | Assistant anomalies, smart buttons |
| Sécurité | Groupes Utilisateur GLC / Gestionnaire GLC |
| Tests | Suite automatisée module |

---

## 3. Hors périmètre (OUT — lots ultérieurs)

| Sujet | Statut | Référence |
|---|---|---|
| Budget prévisionnel | Reporté — module séparé | [MEMO_ARBITRAGE_BUDGET_GLC.md](../../dorevia_glc_budget/MEMO_ARBITRAGE_BUDGET_GLC.md) |
| Ventilation salariale Palier 2 | Retiré `19.0.13` | Archive TICKET_PALIER_2 |
| Registre bénévole | Reporté V1.1 | README spec |
| Rapport CA PDF | Reporté V1.1 | README spec |
| Exports Excel/PDF cockpit | Non livré | Palier 5+ |

---

## 4. UX finale — Contrôle de gestion

### 4.1 Bandeau et période

- **Alertes** rouge / orange / vert selon couverture des charges de structure
- **Période par défaut** à l’ouverture menu : **3 derniers mois calendaires** (mois courant inclus), fin = **aujourd’hui**
- **Sélecteur** : icône calendrier + dates compactes, **sans** bouton Actualiser (recalcul auto)

### 4.2 Onglets

| Onglet | Visible |
|---|---|
| **Tableau de bord** | Oui — KPI + graphiques |
| **Détail par axe analytique** | Oui — tableau mensuel |
| **Charges de structure** | Oui |
| **Trésorerie** | Oui |
| **Contrôles qualité** | Oui |
| **Tiers & paiements** | Oui |
| Ressources | Masqué |
| Infos | Masqué |

### 4.3 Tableau de bord — KPI

| KPI | Règle d’affichage |
|---|---|
| Solde | `Ressources − Cumul RH − Dépenses` |
| Couverture du Cumul RH | Couleur = bandeau alerte ; si > 100 % → affiche **`> 100 %`** |
| Lettrage clients / fournisseurs | Libellés courts (sans « Taux ») |

Pas de bloc texte introductif sous le titre.

### 4.4 Détail par axe analytique

- Pas de bloc « Filtres de lecture » visible (tableau direct)
- **Payé uniquement** : case à cocher (mémorisée par utilisateur / société)
- **Tri des mois** : sélecteur « Plus récent d’abord » / « Plus ancien d’abord » (mémorisé)

---

## 5. Doctrine réalisé (figée)

| Indicateur | Source |
|---|---|
| **Ressources** | Écritures analytiques classe 7 (+ financements sur axes dédiés) |
| **Cumul RH** | Classe 6 — comptes paie (631, 633, 641, 645…) |
| **Dépenses** | Classe 6 hors paie |
| **Solde** | `Ressources − Cumul RH − Dépenses` |

- Source unique : **`account.analytic.line`** (pièces comptabilisées)
- Aucune écriture générée par le module
- Trésorerie : lecture indépendante (compte bancaire de référence)

---

## 6. Déploiement

### 6.1 Prérequis

- Odoo 19 Community
- Modules : `web`, `account`, `analytic`
- Comptabilité analytique activée

### 6.2 Installation / mise à jour

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d <base> -u dorevia_glc_analytics --stop-after-init --no-http

docker compose restart odoo
```

Puis **Ctrl+Shift+R** dans le navigateur.

### 6.3 Vérification post-déploiement

1. Menu **Facturation → Pilotage GLC** — 3 entrées
2. **Contrôle de gestion** — période 3 mois, Tableau de bord actif
3. Version module ≥ **`19.0.15.0.0`** (Apps → Dorevia GLC Analytics)

---

## 7. Recette MOA — checklist d’acceptation

Cocher après validation sur base de recette ou production pilote.

### 7.1 Navigation & accès

| ID | Critère | OK |
|---|---|---|
| MOA-N1 | Menu Pilotage GLC visible entre Fournisseurs et Comptabilité | [ ] |
| MOA-N2 | Utilisateur GLC accède au Contrôle de gestion | [ ] |
| MOA-N3 | Gestionnaire GLC accède à l’Audit | [ ] |

### 7.2 Contrôle de gestion — période & tableau de bord

| ID | Critère | OK |
|---|---|---|
| MOA-C1 | Ouverture menu → période ≈ 3 derniers mois, fin = aujourd’hui | [ ] |
| MOA-C2 | Changement de dates → recalcul sans bouton Actualiser | [ ] |
| MOA-C3 | Tableau de bord : 6 KPI + 3 graphiques cohérents | [ ] |
| MOA-C4 | Bandeau alerte cohérent avec Couverture du Cumul RH | [ ] |
| MOA-C5 | Couverture > 100 % affichée « > 100 % » en couleur alerte | [ ] |

### 7.3 Détail par axe analytique

| ID | Critère | OK |
|---|---|---|
| MOA-D1 | Tableau sans bloc filtres en tête | [ ] |
| MOA-D2 | Tri mois modifiable (récent / ancien) | [ ] |
| MOA-D3 | « Payé uniquement » recalcule les montants | [ ] |
| MOA-D4 | Grammaire colonnes : Ressources · Cumul RH · Dépenses · Solde | [ ] |

### 7.4 Trésorerie & qualité

| ID | Critère | OK |
|---|---|---|
| MOA-T1 | Onglet Trésorerie — compte bancaire de référence | [ ] |
| MOA-Q1 | Contrôles qualité Q1–Q2 exploitables | [ ] |
| MOA-Q2 | Tiers & paiements Q3 + liens listes | [ ] |

### 7.5 Audit & paramétrage

| ID | Critère | OK |
|---|---|---|
| MOA-A1 | Audit — lancement assistant sur période | [ ] |
| MOA-A2 | 11 axes visibles dans Axes analytiques | [ ] |

### 7.6 Non-régression

| ID | Critère | OK |
|---|---|---|
| MOA-R1 | Pas de menu Budget / Ventilation / Coûts salariés | [ ] |
| MOA-R2 | Réalisé = comptabilité analytique (pas de double source) | [ ] |

**Décision MOA :**

- [ ] **GO** — acceptation livraison `19.0.15.0.0`
- [ ] **GO avec réserves** — préciser :
- [ ] **NO GO** — préciser :

---

## 8. Documentation remise

| Document | Rôle |
|---|---|
| [ETAT_MODULE_ACTUEL.md](./ETAT_MODULE_ACTUEL.md) | État produit et technique |
| [PALIERS.md](./PALIERS.md) | Roadmap paliers |
| [RELEASE_NOTE_19.0.15.0.0.md](./RELEASE_NOTE_19.0.15.0.0.md) | Notes de version livraison |
| [recette/RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md](./recette/RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md) | Recette détaillée cockpit |
| [recette/RECETTE_MANUELLE_COCKPIT_QUALITE_PAIEMENT.md](./recette/RECETTE_MANUELLE_COCKPIT_QUALITE_PAIEMENT.md) | Recette qualité & paiement |
| [recette/RECETTE_MANUELLE_PALIER_5_TRESORERIE_COMPTE_BANCAIRE_REFERENCE.md](./recette/RECETTE_MANUELLE_PALIER_5_TRESORERIE_COMPTE_BANCAIRE_REFERENCE.md) | Recette trésorerie |
| [TICKET_COCKPIT_REALIGNEMENT_CONTROLE_GESTION.md](./TICKET_COCKPIT_REALIGNEMENT_CONTROLE_GESTION.md) | Doctrine contrôle de gestion |

---

## 9. Suite projet (hors cette livraison)

1. **Budget** — arbitrage MOA ([MEMO_ARBITRAGE_BUDGET_GLC.md](../../dorevia_glc_budget/MEMO_ARBITRAGE_BUDGET_GLC.md))
2. **Bénévolat** — registre et valorisation heures (V1.1)
3. **Exports / rapport CA** — reporting direction

---

*Document de livraison — gel fonctionnel `dorevia_glc_analytics` — 2026-05-30*
