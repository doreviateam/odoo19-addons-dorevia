# État actuel du module — `dorevia_glc_analytics`

**Version de référence :** **`19.0.14.1.0`**  
**Dernière mise à jour doc :** 2026-05-30  
**Base recette :** `glc-rgl-test-import` (sandbox)

---

## 1. Périmètre livré aujourd'hui

| Domaine | Statut |
|---|---|
| Socle analytique (plan unique 11 axes) | **Actif** |
| Audit analytique (ex anomalies A1–A2, A4–A6) | **Actif** |
| Contrôle de gestion (ex cockpit couverture) | **Actif** — réalisé seul |
| Trésorerie cockpit (compte bancaire de référence) | **Actif** |
| Qualité comptable & suivi paiement (GQ-6) | **Actif** |
| Ventilation salariale Palier 2 | **Retiré** (`19.0.13.0.0`) |
| Budget prévisionnel Palier 3 (`dorevia_glc_budget`) | **Retiré** (`19.0.14.0.0`) |
| Colonnes budget / écarts prévu-réalisé dans le cockpit | **Retiré** (`19.0.12.0.0` → `19.0.13.0.0`) |

---

## 2. Navigation (Facturation)

Barre principale :

```text
Facturation → … → Fournisseurs → Pilotage GLC → Comptabilité → …
```

Sous-menu **Pilotage GLC** :

| Ordre | Menu | Rôle | Groupe |
|---|---|---|---|
| 1 | **Contrôle de gestion** | Tableau de bord réalisé (Ressources · Cumul RH · Dépenses · Solde) | Utilisateur GLC |
| 2 | **Axes analytiques** | Paramétrage des comptes du plan GLC | Utilisateur GLC |
| 3 | **Audit** | Assistant de contrôle analytique (A1–A2, A4–A6) | Gestionnaire GLC |

Chemin type recette :

```text
Facturation → Pilotage GLC → Contrôle de gestion
Facturation → Pilotage GLC → Audit
```

---

## 3. Doctrine réalisé (Contrôle de gestion)

| Indicateur UI | Source |
|---|---|
| **Ressources** | Écritures analytiques classe 7 (+ financements sur axes dédiés) |
| **Cumul RH** | Écritures analytiques classe 6 — comptes paie (631, 633, 641, 645…) |
| **Dépenses** | Écritures analytiques classe 6 hors paie |
| **Solde** | `Ressources − Cumul RH − Dépenses` |

- Pas de double source : **uniquement** `account.analytic.line` (écritures comptabilisées).
- Pas de prévisionnel, pas de ventilation salariale overlay, pas d'écriture générée par le module.

---

## 4. Dépendances module

```text
web
account
analytic
```

(`hr` retiré — plus de modèles salariés internes.)

---

## 5. Mise à jour technique

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

## 6. Historique simplification (2026-05-30)

| PR | Version | Changement |
|---|---|---|
| [#50](https://github.com/doreviateam/odoo19-addons-dorevia/pull/50) | `19.0.13.0.0` | Cockpit réalisé seul · retrait budget UI · Palier 2 · règles financement A3 |
| [#51](https://github.com/doreviateam/odoo19-addons-dorevia/pull/51) | `19.0.14.0.0` | Suppression module `dorevia_glc_budget` |
| [#52](https://github.com/doreviateam/odoo19-addons-dorevia/pull/52) | `19.0.14.0.2` | Menus MOA · Contrôle de gestion · Audit · ordre barre Facturation |
| Doc | `19.0.14.1.0` | Alignement documentation module |

Détail : [RELEASE_NOTE_19.0.14_SIMPLIFICATION_PILOTAGE.md](./RELEASE_NOTE_19.0.14_SIMPLIFICATION_PILOTAGE.md)

---

## 7. Documents de référence (à jour)

| Document | Usage |
|---|---|
| [PALIERS.md](./PALIERS.md) | Roadmap et statut par palier |
| [TICKET_COCKPIT_REALIGNEMENT_CONTROLE_GESTION.md](./TICKET_COCKPIT_REALALIGNEMENT_CONTROLE_GESTION.md) | Doctrine contrôle de gestion |
| [TICKET_COCKPIT_SOURCE_REALISE.md](./TICKET_COCKPIT_SOURCE_REALISE.md) | Règles agrégation réalisé |
| [ETAT_NOMENCLATURE_ANALYTIQUE.md](./ETAT_NOMENCLATURE_ANALYTIQUE.md) | Plan analytique unique |
| [recette/RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md](./recette/RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md) | Recette exploitation Contrôle de gestion |

Documents **Palier 2**, **Palier 3**, **budget/cockpit initial** : conservés comme **archives** — ne décrivent plus le produit installé.
