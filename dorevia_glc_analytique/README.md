# dorevia_glc_analytique — Suivi d'activité GLC

Module Odoo 19 CE — **Pilotage analytique associatif** pour GLC (Saint-Aignan-de-Grand-Lieu).

> Passer d'une lecture comptable analytique partielle à une **lecture de gestion par activité** : dépenses directes, salaires ventilés, bénévolat et coût complet.

## Périmètre du premier commit — Palier 0 uniquement

Ce commit livre **strictement** le socle analytique installable :

- plans `GLC - Activités` et `GLC - Financements` ;
- 11 comptes analytiques (7 + 4) ;
- extension légère de `account.analytic.account` — **source de vérité = analytique Odoo standard** ;
- groupes de sécurité de base ;
- applicabilités Odoo 19 **non bloquantes** (`optional`) ;
- documentation et tests.

**Hors périmètre** (paliers suivants) : contrôles d'anomalies, ventilation salariale, registre bénévole, rapport CA, clôture analytique.

La [spec V1.1](./docs/README.md) reste la cible fonctionnelle globale. Voir [docs/PALIERS.md](./docs/PALIERS.md).

## Palier 0 — contenu installé

| Élément | Détail |
|---|---|
| Plans | `GLC - Activités`, `GLC - Financements` |
| Comptes | `STRUCTURE`, `BAR`, `PRESTATIONS`, `RESIDENCES`, `MISSIONS`, `PRIVATISATIONS`, `LOCATION_RADIO`, `ADHESIONS`, `DONS`, `SUBVENTIONS`, `RESSOURCES_PROPRES` |
| Extension | `glc_activity_type`, `glc_display_sequence`, `glc_report_active`, `glc_pilotage_comment` |
| Menu | Comptabilité → **Pilotage GLC** |
| Sécurité | `Utilisateur GLC`, `Gestionnaire GLC` |
| Applicabilités | Activités : optional (factures) ; Financements : optional (ventes), unavailable (achats) |

## Documentation

| Document | Description |
|---|---|
| [Spécification fonctionnelle V1.1](./docs/README.md) | Cahier des charges complet (cible) |
| [Recette manuelle Palier 0](./docs/RECETTE_MANUELLE_PALIER_0.md) | Scénario de test MOA — socle analytique |
| [Découpage en paliers](./docs/PALIERS.md) | Roadmap de développement |
| [Règles d'affectation](./docs/REGLES_AFFECTATION.md) | Matrice double axe (application Palier 1+) |
| [Matrice de migration](./docs/MATRICE_MIGRATION.md) | Correspondance ancien plan → plan cible |

## Dépendances

```text
account
analytic
```

## Version

**Palier 0** — `19.0.1.0.0` — **Validé MOA** (recette 2026-05-27, base `glc-rgl-test-import`)
