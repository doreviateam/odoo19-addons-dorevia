# dorevia_glc_analytics — Suivi d'activité GLC

Module Odoo 19 CE — **Pilotage analytique associatif** pour GLC (Saint-Aignan-de-Grand-Lieu).

> Lecture de gestion par activité à partir du **réalisé comptable analytique** : ressources, cumul RH, dépenses, solde, trésorerie et audit.

**Version courante :** **`19.0.14.1.0`**

**État du module :** [docs/ETAT_MODULE_ACTUEL.md](./docs/ETAT_MODULE_ACTUEL.md)

---

## Menus (Facturation)

```text
Facturation → Fournisseurs → Pilotage GLC → Comptabilité → …

Pilotage GLC
├── Contrôle de gestion
├── Axes analytiques
└── Audit
```

---

## Périmètre actif

| Fonctionnalité | Statut |
|---|---|
| Plan analytique GLC (11 axes) | Actif |
| Contrôle de gestion (cockpit réalisé) | Actif |
| Audit analytique | Actif |
| Trésorerie cockpit · GQ-6 qualité/paiement | Actif |
| Ventilation salariale · budget prévisionnel | **Retirés** (mai 2026) |

Voir [PALIERS.md](./docs/PALIERS.md) et [RELEASE_NOTE_19.0.14_SIMPLIFICATION_PILOTAGE.md](./docs/RELEASE_NOTE_19.0.14_SIMPLIFICATION_PILOTAGE.md).

---

## Mise à jour module

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d <base> -u dorevia_glc_analytics --stop-after-init --no-http

docker compose restart odoo
```

Migration depuis `dorevia_glc_analytique` : voir section ci-dessous.

---

## Renommage module (`19.0.3.1.0`)

```text
dorevia_glc_analytique  →  dorevia_glc_analytics
```

Sur une base où **`dorevia_glc_analytique` est encore installé** :

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d <base> -i dorevia_glc_analytics --stop-after-init --no-http
```

Le `pre_init_hook` renomme `ir_module_module`, dépendances et `ir.model.data`.

---

## Documentation

| Document | Description |
|---|---|
| [État actuel du module](./docs/ETAT_MODULE_ACTUEL.md) | **Référence à jour** — menus, doctrine, versions |
| [Découpage en paliers](./docs/PALIERS.md) | Roadmap et statut |
| [Spec fonctionnelle V1.1](./docs/README.md) | Cahier des charges cible (partiellement implémenté) |
| [Contrôle de gestion — doctrine](./docs/TICKET_COCKPIT_REALIGNEMENT_CONTROLE_GESTION.md) | Règles métier cockpit |
| [Recette Contrôle de gestion](./docs/recette/RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md) | Exploitation MOA |
| [Recette Audit](./docs/RECETTE_MANUELLE_PALIER_1.md) | Assistant anomalies |
| [Nomenclature analytique](./docs/ETAT_NOMENCLATURE_ANALYTIQUE.md) | Plan unique 11 axes |

**Archives** (ne décrivent plus le produit installé) : Palier 2, Palier 3, [cadrage budget initial](./docs/CADRAGE_BUDGET_COCKPIT.md), [release Paliers 0–4](./docs/RELEASE_NOTE_GLC_ANALYTICS_BUDGET_PALIERS_0_4.md).

---

## Dépendances

```text
web
account
analytic
```

---

## Tests automatisés

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d glc-rgl-test-import -u dorevia_glc_analytics \
  --test-enable --test-tags=/dorevia_glc_analytics --stop-after-init --no-http
```
