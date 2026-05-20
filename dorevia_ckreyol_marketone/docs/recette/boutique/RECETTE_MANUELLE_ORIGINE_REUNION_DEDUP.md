# Recette manuelle — Dédoublonnage origine La Réunion / Reunion

| Champ | Valeur |
|-------|--------|
| **Ticket** | `TICKET_MARKETONE_ORIGINE_REUNION_DEDUP` |
| **Version** | `19.0.13.1.0` |
| **URL** | http://localhost:18079/shop |
| **Base** | `ckr-marketone-01` |

---

## Audit pré-correction (`ckr-marketone-01`, 2026-05-19)

### 1. Valeurs attribut Origines (id=3)

| id | Libellé | Produits (tmpl) |
|----|---------|-----------------|
| 19 | Guadeloupe | 13 |
| 20 | Martinique | 12 |
| 51 | La Réunion | 0 |
| 68 | Reunion | 7 |

### 2. Profil `marketone.shop.origin` slug `reunion`

| id | slug | name_visitor | attribute_value_id | libellé valeur |
|----|------|--------------|--------------------|----------------|
| 39 | reunion | La Reunion | 68 | Reunion |

### 3. Décision fusion

- **Canonique** : id **51** — libellé **`La Réunion`**
- **Doublon** : id **68** — `Reunion` (7 produits + profil porte)
- **Slug technique** : inchangé `reunion`

---

## Post-upgrade

```bash
odoo-bin -d ckr-marketone-01 -u dorevia_ckreyol_marketone --stop-after-init
# restart Odoo
```

---

## R1 — Sidebar une seule Réunion

| Étape | Action | Attendu |
|-------|--------|---------|
| 1 | `/shop` · rubrique **Origines** | Une ligne **La Réunion** |
| 2 | Vérifier | Pas de ligne **Reunion** |

## R2 — Filtre + chip UX-1

| Étape | Action | Attendu |
|-------|--------|---------|
| 1 | Cocher **La Réunion** | Grille filtrée · **7** produits (ex-recette) |
| 2 | Chip UX-1 | Libellé **La Réunion** |

## R3 — Porte Origines

| Étape | Action | Attendu |
|-------|--------|---------|
| 1 | `/shop?marketone_mode=origin&marketone_origin=reunion` | **200** |

## Tests auto

```bash
odoo-bin -d ckr-marketone-01 --test-tags=dorevia_marketone_origin_reunion_dedup --stop-after-init
odoo-bin -d ckr-marketone-01 --test-tags=dorevia_marketone_shop_regression,dorevia_marketone_shop_filter_state --stop-after-init
odoo-bin -d ckr-marketone-01 --test-tags=dorevia_marketone_culture_v2 --stop-after-init
```

---

## Verdict MOA post-merge (2026-05-19 — PR #7 `632e035`)

| Contrôle | Résultat |
|----------|----------|
| Valeur unique BO | **La Réunion** id `51` — plus de `Reunion` |
| Produits Réunion | **7/7** rattachés (6 actifs + 1 inactif) |
| Profil `reunion` | `attribute_value_id=51` · `name_visitor=La Réunion` · publié |
| Chip UX-1 | Libellé **La Réunion** · retrait → `/shop` |
| Porte Origines | `/shop?marketone_mode=origin&marketone_origin=reunion` **200** |
| Rustine QWeb | **Aucune** — PR #7 sans modification `views/` |

**GO technique / GO MOA données** — ticket clôturé.
