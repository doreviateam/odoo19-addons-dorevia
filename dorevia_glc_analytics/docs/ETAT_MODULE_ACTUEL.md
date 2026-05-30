# État actuel du module — `dorevia_glc_analytics`

**Version de référence :** **`19.0.15.0.0`**  
**Statut :** **Terminé — livraison MOA**  
**Dernière mise à jour doc :** 2026-05-30  
**Base recette :** `glc-rgl-test-import` (sandbox)  
**Tests :** **106 / 106 verts**

**Documents livraison :** [LIVRAISON_MOA.md](./LIVRAISON_MOA.md) · [RELEASE_NOTE_19.0.15.0.0.md](./RELEASE_NOTE_19.0.15.0.0.md)

---

## 1. Périmètre livré

| Domaine | Statut |
|---|---|
| Socle analytique (plan unique 11 axes) | **Livré** |
| Audit analytique (A1–A2, A4–A6) | **Livré** |
| Contrôle de gestion | **Livré** — réalisé seul |
| Trésorerie cockpit (compte bancaire de référence) | **Livré** |
| Qualité comptable & suivi paiement (GQ-6) | **Livré** |
| Ventilation salariale Palier 2 | **Retiré** (`19.0.13.0.0`) |
| Budget prévisionnel (`dorevia_glc_budget`) | **Hors périmètre** — lot ultérieur |
| Colonnes budget / écarts dans le cockpit | **Retiré** (`19.0.13.0.0`) |

---

## 2. Navigation (Facturation)

```text
Facturation → … → Fournisseurs → Pilotage GLC → Comptabilité → …
```

| Ordre | Menu | Rôle | Groupe |
|---|---|---|---|
| 1 | **Contrôle de gestion** | Tableau de bord + détail réalisé | Utilisateur GLC |
| 2 | **Axes analytiques** | Paramétrage plan GLC | Utilisateur GLC |
| 3 | **Audit** | Contrôles analytiques | Gestionnaire GLC |

---

## 3. Contrôle de gestion — UX livrée

### Période

- Défaut à l’ouverture menu : **3 derniers mois calendaires**, fin = **aujourd’hui**
- Sélecteur compact (icône calendrier), recalcul automatique

### Onglets visibles

Tableau de bord · Détail par axe analytique · Charges de structure · Trésorerie · Contrôles qualité · Tiers & paiements

*(Onglets Ressources et Infos masqués.)*

### Tableau de bord

- KPI : Solde, Ressources, Charges de structure, Couverture du Cumul RH, Lettrage clients, Lettrage fournisseurs
- Couverture RH : couleur alignée sur bandeau alerte ; affichage **> 100 %** si taux > 100 %
- 3 graphiques : Solde mensuel, Structure mensuelle, Solde par axe

### Détail par axe analytique

- Tableau direct (sans bloc filtres visible)
- Options : **Payé uniquement**, tri mois **récent / ancien** (préférences mémorisées)

---

## 4. Doctrine réalisé

| Indicateur UI | Source |
|---|---|
| **Ressources** | Écritures analytiques classe 7 (+ financements) |
| **Cumul RH** | Classe 6 — comptes paie |
| **Dépenses** | Classe 6 hors paie |
| **Solde** | `Ressources − Cumul RH − Dépenses` |

Source unique : **`account.analytic.line`**. Aucune écriture générée par le module.

---

## 5. Dépendances

```text
web · account · analytic
```

---

## 6. Mise à jour technique

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d <base> -u dorevia_glc_analytics --stop-after-init --no-http

docker compose restart odoo
```

Tests :

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d glc-rgl-test-import -u dorevia_glc_analytics \
  --test-enable --test-tags=/dorevia_glc_analytics --stop-after-init --no-http
```

---

## 7. Historique versions

| Version | Jalons |
|---|---|
| `19.0.13` – `19.0.14.1` | Simplification MOA — réalisé seul, menus, retrait budget |
| `19.0.14.5.x` | Finitions UX cockpit |
| **`19.0.15.0.0`** | **Gel livraison MOA** |

Détail : [RELEASE_NOTE_19.0.14_SIMPLIFICATION_PILOTAGE.md](./RELEASE_NOTE_19.0.14_SIMPLIFICATION_PILOTAGE.md) · [RELEASE_NOTE_19.0.15.0.0.md](./RELEASE_NOTE_19.0.15.0.0.md)

---

## 8. Documents de référence

| Document | Usage |
|---|---|
| [LIVRAISON_MOA.md](./LIVRAISON_MOA.md) | **Acceptation MOA** |
| [PALIERS.md](./PALIERS.md) | Roadmap |
| [TICKET_COCKPIT_REALIGNEMENT_CONTROLE_GESTION.md](./TICKET_COCKPIT_REALIGNEMENT_CONTROLE_GESTION.md) | Doctrine |
| [recette/RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md](./recette/RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md) | Recette cockpit |

Archives Palier 2 / budget / tickets `19.0.4.x` : addendum en tête de fichier — ne pas utiliser comme spec active.

---

## 9. Suite projet (hors module)

| Lot | Référence |
|---|---|
| Budget prévisionnel | [MEMO_ARBITRAGE_BUDGET_GLC.md](../../dorevia_glc_budget/MEMO_ARBITRAGE_BUDGET_GLC.md) |
| Bénévolat | Spec V1.1 — reporté |
| Rapport CA PDF | Spec V1.1 — reporté |
