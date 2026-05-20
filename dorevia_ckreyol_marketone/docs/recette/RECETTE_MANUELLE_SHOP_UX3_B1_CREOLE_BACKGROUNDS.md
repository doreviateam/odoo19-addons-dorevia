# Recette manuelle — UX-3 Palier B1 — Fonds créoles premium `/shop`

| Champ | Valeur |
|-------|--------|
| **Ticket** | `TICKET_MARKETONE_UX3_PALIER_B1_CREOLE_BACKGROUNDS` |
| **Version** | **`19.0.15.4.0`** (B1.1 harmonie — après NO GO `19.0.15.3.0`) |
| **Branche** | `feat/marketone-ux3-b1-creole-backgrounds` |
| **Jalon** | ADR-031 · Palier A « Tenue » `19.0.15.2.0` |
| **URL** | http://localhost:18079/shop |
| **Base** | `ckr-marketone-01` |
| **Statut** | **Recette B1.1 à exécuter** — post-ajustement harmonie MOA |

---

## Prérequis

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d ckr-marketone-01 -u dorevia_ckreyol_marketone --stop-after-init
docker restart sandbox-odoo19-odoo-1
```

Hard refresh navigateur (vider cache assets si besoin).

---

## Historique verdicts

| Version | Verdict MOA |
|---|---|
| `19.0.15.3.0` | **NO GO visuel** — juxtaposition crème / bloc vert / cartes blanches |
| `19.0.15.4.0` | Recette en attente |

---

## Palette B1.1 (référence dev)

| Token | Hex / intention | Usage |
|---|---|---|
| `$ck-bg-page` | `#F0E6D8` | Fond page — plus chaud/mat que les cartes |
| `$ck-bg-cream` | `#F7EFE4` | Fin dégradé sidebar · bandeaux |
| `$ck-bg-green-mist` | `#EEF5E9` | Début dégradé sidebar · chip origin |
| `$ck-bg-yellow-vanille` | `#FBF3E0` | Zone image · titres · liant chaleur |
| `$ck-bg-white` | `#FFFDF8` | Cartes |
| `$ck-bg-yellow-soft` | `#F6E4A8` | Chip collection · filets |
| `$ck-border-card` | `#D4C4B4` | Bordure carte |
| `$ck-sauge-border` | rgba sauge ~38% | Hover carte · filet sidebar |
| `$ck-terracotta` | `#C4715A` | Prix (inchangé) |

Sidebar : `linear-gradient(180deg, #EEF5E9 → #F7EFE4)` + filet gauche sauge — **pas** d’aplat `#D9E8D2`.

---

## Grille validation B1.1

| Scénario | Verdict | Notes |
|---|---|---|
| H1 — Harmonie globale (pas juxtaposition) | ☐ OK · ☐ réserve · ☐ KO | |
| H2 — Sidebar discrète, pas bloc vert massif | ☐ OK · ☐ réserve · ☐ KO | dégradé + filet |
| H3 — Vert « répond » dans la grille (hover, bandeaux) | ☐ OK · ☐ réserve · ☐ KO | |
| H4 — Fond page ≠ cartes (hiérarchie écrin) | ☐ OK · ☐ réserve · ☐ KO | |
| H5 — Jaune/vanille comme liant chaleur | ☐ OK · ☐ réserve · ☐ KO | |
| H6 — Premium créole, pas bio discount | ☐ OK · ☐ réserve · ☐ KO | |
| V4 — Produits prioritaires | ☐ OK · ☐ réserve · ☐ KO | |
| V8 — Mobile ≤768px | ☐ OK · ☐ réserve · ☐ KO | |
| V9 — Hors scope home/header | ☐ OK · ☐ KO | |
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
| **GO visuel B1.1 — merge autorisé** | |
| **GO avec réserves** | |
| **NO GO** | |

**Merge** : uniquement sur GO visuel explicite MOA.

---

## Annexe — Recette `19.0.15.3.0` (archivée)

GO technique · NO GO visuel MOA. Captures `marketone_b1_*` sur `/private/tmp/`. Détail : commit `e4c1694` / ticket §11.
