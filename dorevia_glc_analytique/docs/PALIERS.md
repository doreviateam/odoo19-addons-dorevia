# Découpage en paliers — dorevia_glc_analytique

**Version :** V1.1 (référence fonctionnelle)  
**Doctrine de livraison :** la spec V1.1 reste le document cible ; le développement avance par paliers installables.

> GLC pilote ses activités avec deux axes : **ce que l'association fait**, et **ce qui finance ce qu'elle fait**.

---

## Vue d'ensemble

| Palier | Objectif | Statut |
|---|---|---|
| **0** | Socle analytique installable | **Validé MOA** (2026-05-27 · `glc-rgl-test-import`) |
| **1** | Règles d'affectation et contrôles | **Validé MOA** (2026-05-27 · `glc-rgl-test-import`) · [PR #25](https://github.com/doreviateam/odoo19-addons-dorevia/pull/25) |
| **2** | Ventilation salariale | **Validé MOA** (2026-05-27 · `glc-rgl-test-import`) · [PR #26](https://github.com/doreviateam/odoo19-addons-dorevia/pull/26) |
| **3** | Registre bénévole | À faire |
| **4** | Rapport CA mensuel | À faire |
| **5** | Clôture analytique mensuelle | À faire |

La V1.1 fonctionnelle = paliers 0 à 5. Ne pas livrer tout le bloc d'un coup.

---

## Palier 0 — Socle analytique installable

**Ticket :** Installer le socle analytique GLC : plans, comptes, sécurité minimale, documentation et tests.

### Livrables

- Plan analytique `GLC - Activités` (7 comptes)
- Plan analytique `GLC - Financements` (4 comptes)
- Extension légère `account.analytic.account` (type, ordre, rapport) — **pas de modèle activité parallèle**
- Groupes de sécurité de base (`Utilisateur GLC`, `Gestionnaire GLC`)
- Applicabilités Odoo 19 **non bloquantes** (`optional` sur factures ; Financements masqué sur achats)
- Tests d'installation et de nomenclature
- Documentation embarquée ([recette manuelle Palier 0](./RECETTE_MANUELLE_PALIER_0.md))

### Applicabilités Palier 0 vs Palier 1

| Plan | Palier 0 (install) | Palier 1 (contrôles) |
|---|---|---|
| GLC - Activités | `optional` sur factures clients et fournisseurs | `optional` + rapport anomalies **non bloquant** |
| GLC - Financements | `optional` sur factures clients ; `unavailable` sur achats | `optional` + contrôles A2/A3 (A3 si mapping explicite) |

Le Palier 0 **prépare** l'usage des deux axes sans bloquer la comptabilité courante.

### Hors périmètre Palier 0

- Paramètres métier avancés (seuils, taux bénévolat, loyer Radio)
- Contrôles d'anomalies
- Ventilation salariale
- Registre bénévole
- Rapport PDF CA
- Clôture analytique mensuelle

---

## Palier 1 — Règles d'affectation et contrôles

**Ticket :** [TICKET_PALIER_1.md](./TICKET_PALIER_1.md)  
**Recette :** [RECETTE_MANUELLE_PALIER_1.md](./RECETTE_MANUELLE_PALIER_1.md)  
**Référence :** [REGLES_AFFECTATION.md](./REGLES_AFFECTATION.md)

### Livrables

- Wizard + liste **Anomalies analytiques GLC** (`glc.analytic.anomaly.wizard` / `.line`)
- Contrôles A1–A6 (cf. ticket)
- Paramètres : date de bascule, seuil STRUCTURE
- Tests automatisés CA1–CA8
- **Non bloquant** — applicabilités `optional` conservées par défaut

### Hors périmètre Palier 1

Identique au ticket §7 (pas de ventilation, CA, clôture, corrections auto).

---

## Palier 2 — Ventilation salariale

**Ticket :** [TICKET_PALIER_2.md](./TICKET_PALIER_2.md)  
**Recette :** [RECETTE_MANUELLE_PALIER_2.md](./RECETTE_MANUELLE_PALIER_2.md)  
**Référence :** spec §8.2, §9.2, [MATRICE_MIGRATION.md](./MATRICE_MIGRATION.md)

### Livrables

- `glc.salary.allocation` + lignes
- `glc.employee.cost.line` (historique coût mensuel chargé)
- Ventilation heures ou pourcentage
- Validation, contrôle total = 100 %
- Comparaison masse salariale comptable (écart > 5 % → alerte)

**Règle :** pas d'écriture analytique salariale — overlay de gestion uniquement.

---

## Palier 3 — Registre bénévole

**Référence :** spec §7.3, §9.3

### Livrables

- `glc.volunteer.timesheet`
- Contact bénévole, activité, durée, justificatif signé
- Workflow validation (papier signé → saisie → contrôle)
- Agrégats heures par activité

---

## Palier 4 — Rapport CA mensuel

**Référence :** spec §11

### Livrables

- Tableau Activité × Mois
- Trois niveaux de solde (brut / gestion / complet)
- Note méthodologique obligatoire
- 4 KPI page 1
- Export PDF (XLSX en V1.1 si effort compatible)
- Référence `GLC-RPT-AAAA-MM-v1`
- **Pas de détail nominatif salarié** dans le PDF CA

---

## Palier 5 — Clôture analytique mensuelle

**Référence :** spec §8.7

### Livrables

- Snapshot ou période mensuelle (`glc.activity.period` ou équivalent)
- Statuts : ouvert / contrôlé / verrouillé
- Archivage PDF
- Chatter et réouverture contrôlée
- Lien avec `dorevia_posted_lock` si installé

---

## Décisions d'architecture validées

| Sujet | Décision |
|---|---|
| Modèle activité | Réutiliser `account.analytic.account` — pas de modèle parallèle |
| Plans analytiques | `GLC - Activités` et `GLC - Financements` |
| Codes comptes | `STRUCTURE`, `BAR`, `PRESTATIONS`, etc. (cf. spec §4.2–4.3) |
| Migration | Ancien plan en lecture seule ; pas de reclassement massif V1 |
| Subvention affectée | Double axe : Activité projet + `SUBVENTIONS` |
| `RESSOURCES_PROPRES` | Recettes d'activité économique uniquement — pas don/adhésion/subvention |
| Automatisation | Discipline de saisie d'abord ; automatismes ensuite (V2) |

---

## Migration — doctrine

Cf. [MATRICE_MIGRATION.md](./MATRICE_MIGRATION.md) :

1. Inventorier les 9 comptes actuels (Phase 0 métier)
2. Date de bascule + mois pilote non officiel
3. `RH_PERSONNEL` → ventilation salariale, pas de solde migré
4. Premier rapport CA officiel après validation du mois pilote

---

## Structure module cible (vision)

```text
dorevia_glc_analytique/
├── data/           # Palier 0
├── security/       # Palier 0 (+ affiné palier 2–5)
├── models/
│   ├── account_analytic_account.py     # Palier 0
│   ├── glc_salary_allocation.py        # Palier 2
│   ├── glc_volunteer_timesheet.py      # Palier 3
│   └── glc_activity_period.py          # Palier 5
├── views/
├── reports/                            # Palier 4
├── wizard/                             # Palier 1 (anomalies)
└── tests/
```

**Premier commit = Palier 0 uniquement.**
