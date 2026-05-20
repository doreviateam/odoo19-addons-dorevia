# Recette manuelle — UX-3 Palier B1 — Fonds créoles premium `/shop`

| Champ | Valeur |
|-------|--------|
| **Ticket** | `TICKET_MARKETONE_UX3_PALIER_B1_CREOLE_BACKGROUNDS` |
| **Version** | **`19.0.15.5.0`** (B1.2 — palette harmonie MOA) |
| **Branche** | `feat/marketone-ux3-b1-creole-backgrounds` |
| **Jalon** | ADR-031 · Palier A « Tenue » `19.0.15.2.0` |
| **URL** | http://localhost:18079/shop |
| **Base** | `ckr-marketone-01` |
| **Statut** | **Recette B1.2 à exécuter** |

---

## Prérequis

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d ckr-marketone-01 -u dorevia_ckreyol_marketone --stop-after-init
docker restart sandbox-odoo19-odoo-1
```

Hard refresh navigateur.

---

## Historique verdicts MOA

| Version | Verdict |
|---|---|
| `19.0.15.3.0` | **NO GO** — juxtaposition crème / bloc vert / cartes blanches |
| `19.0.15.4.0` | **NO GO** (même diagnostic — harmonie insuffisante) |
| `19.0.15.5.0` | Recette en attente |

**Critère GO** : on ne voit plus « beige + vert + blanc » en trois blocs, mais une harmonie crème / vanille / végétal doux / terracotta au service des produits.

---

## Palette B1.2 (MOA)

| Token | Hex | Usage |
|---|---|---|
| `$ck-bg-page` | `#F8EFE3` | Ambiance globale |
| `$ck-bg-card` | `#FFFDF8` | Cartes écrin |
| `$ck-bg-image` | `#FAF1D6` | Zone image vanille |
| `$ck-bg-green-mist` | `#EEF5E9` | Sidebar diluée (fin → page) |
| `$ck-bg-green-soft` | `#D9E8D2` | **Détails / actifs uniquement** |
| `$ck-bg-yellow-soft` | `#F8EAC0` | Liant chaleur |
| `$ck-bg-yellow-halo` | `#FFF4D8` | Halo subtil |
| `$ck-bg-red-soft` | `#F1CFC4` | Chip prix |
| `$ck-border-soft` | `#E6D4C3` | Bordures |
| `$ck-terracotta` | `#C4715A` | Prix |

Sidebar : dégradé `#EEF5E9` → `#F8EFE3` — **pas** d’aplat `#D9E8D2` plein.

Cartes : ombre `0 10px 24px rgba(42,31,24,0.07)`.

---

## Grille validation B1.2

| Scénario | Verdict | Notes |
|---|---|---|
| H1 — Composition globale (pas 3 blocs) | ☐ OK · ☐ réserve · ☐ KO | |
| H2 — Sidebar accompagne, ne domine pas | ☐ OK · ☐ réserve · ☐ KO | fondue vers page |
| H3 — Jaune/vanille liant (image, filets, bandeaux) | ☐ OK · ☐ réserve · ☐ KO | |
| H4 — Cartes écrin premium vs fond page | ☐ OK · ☐ réserve · ☐ KO | |
| H5 — Rappels vert/rouge discrets (chips, hover) | ☐ OK · ☐ réserve · ☐ KO | |
| H6 — Pas bio-discount / patchwork | ☐ OK · ☐ réserve · ☐ KO | |
| V4 — Produits prioritaires | ☐ OK · ☐ réserve · ☐ KO | |
| V8 — Mobile ≤768px | ☐ OK · ☐ réserve · ☐ KO | |
| V9 — Hors scope | ☐ OK · ☐ KO | |
| V10 — Tests auto 21/21 | ☐ OK · ☐ KO | |

---

## Tests auto

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d ckr-marketone-01 --http-port 8071 \
  --test-tags dorevia_marketone_shop_regression,dorevia_marketone_shop_filter_state,dorevia_marketone_shop_sidebar_ux2 \
  --stop-after-init
```

---

## Verdict MOA

| Verdict | ☐ |
|---|---|
| **GO visuel B1 — merge autorisé** | |
| **GO avec réserves** | |
| **NO GO** | |

**Merge** : uniquement sur GO visuel explicite MOA.
