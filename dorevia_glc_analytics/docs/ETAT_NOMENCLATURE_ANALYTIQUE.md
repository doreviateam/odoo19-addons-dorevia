# État nomenclature analytique GLC

**Version module :** `19.0.8.0.0`  
**Date :** 2026-05-29

---

## Doctrine en vigueur sur `main`

| Élément | État |
|---|---|
| Plan analytique visible | **Un seul : `GLC - Activités`** |
| Nombre d'axes | **11** (7 activités + 4 financements) |
| Plan `GLC - Financements` | **Archivé** sur bases migrées · **absent** des nouvelles installations |
| Codes financement | `ADHESIONS` · `DONS` · `SUBVENTIONS` · `RESSOURCES_PROPRES` |
| Distinction activité / financement | Par **code** et `glc_activity_type`, plus par plan séparé |

---

## Historique — pourquoi FINANCEMENTS est réapparu

1. **Palier 0–5 officiel** : 2 plans (Activités + Financements).
2. **WIP plan unique** (`wip/glc-analytic-parametrage-type-glc-plan-unique`) : suppression du 2ᵉ plan — **non mergé** (Option C).
3. **GQ-6 (`19.0.7.0.x`)** : hook `_normalize_glc_official_analytic_seed` **restaurait** le 2-plan pour corriger une sandbox polluée → conflit avec votre suppression manuelle.
4. **`19.0.8.0.0`** : plan unique **officiel sur `main`** · hook remplacé par `migrate_glc_analytic_nomenclature` · plus de restauration du plan Financements.

---

## Déploiement

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d <base> -u dorevia_glc_analytics --stop-after-init --no-http

docker compose restart odoo
```

**Obligatoire :** redémarrer le worker après `-u`.

---

## Vérification UI attendue

- **Comptabilité → Configuration → Plans analytiques** : un plan actif **`GLC - Activités`** avec 11 comptes.
- Plan **`GLC - Financements (archivé)`** peut subsister en lecture seule sur bases migrées — sans comptes rattachés.
- Menu **Pilotage GLC → Axes analytiques GLC** : les 11 axes.
- Menu **Financements GLC** : filtre les 4 axes ressources sur le plan unique.

---

## Branche WIP historique

`wip/glc-analytic-parametrage-type-glc-plan-unique` reste une référence avec **renommages de codes** (`BAR_REST`, `FIN_EXT`, …) **non retenus** sur `main`.  
`main` conserve les **codes Palier 4/5** (`BAR`, `SUBVENTIONS`, …) sur plan unique.
