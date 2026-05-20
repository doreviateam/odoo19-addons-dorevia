# TICKET — Lot 1 Socle `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_LOT1_SOCLE` |
| **Lot** | 1 — Socle module installable |
| **Statut** | GO validé (2026-05-18) |
| **Base** | `ckr-marketone-01` |
| **Prerequis** | GO Lot 0 + base reference validee |

---

## Objectif

Livrer un module Odoo 19 CE **installable et testable**, sans modifier le comportement standard de `website_sale`.

---

## Perimetre livre

| Element | Statut |
|---------|--------|
| `__manifest__.py` sobre | OK |
| Depends `portal`, `website`, `website_sale` | OK |
| `__init__.py` | OK |
| Assets `marketone.scss` (placeholder vide) | OK |
| Tests `dorevia_marketone_smoke` | OK |
| Controleurs / modeles / vues / JS | Non (Lot 2+) |

---

## Hors perimetre

- Refonte front, portes catalogue, moteur filtre
- Dependances optionnelles (wishlist, theme tiers, marketplace)
- Portage legacy

---

## Validation

```bash
# Installation
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -i dorevia_ckreyol_marketone --stop-after-init

# Update
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone --stop-after-init

# Smoke tests
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_smoke
```

**Critere GO Lot 1** : install + update sans erreur ; tests smoke verts ; `/shop` reste standard.

### Resultats automatises (2026-05-18)

| Commande | Resultat |
|----------|----------|
| `-i dorevia_ckreyol_marketone` | OK |
| `-u dorevia_ckreyol_marketone` | OK |
| `--test-tags=dorevia_marketone_smoke` | **6/6** tests OK |
| `curl /shop` | **200** |

---

## Checklist validation humaine

```text
[ ] Install -i sans traceback
[ ] Update -u sans traceback
[ ] Tests dorevia_marketone_smoke OK
[ ] / et /shop HTTP 200
[ ] marketplace et theme_classic_store toujours absents

Decision : [x] GO  [ ] GO avec reserves  [ ] NO GO
```
