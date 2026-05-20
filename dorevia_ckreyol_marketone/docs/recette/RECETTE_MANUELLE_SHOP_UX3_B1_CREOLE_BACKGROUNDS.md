# Recette manuelle — UX-3 Palier B1 — Fonds créoles premium `/shop`

| Champ | Valeur |
|-------|--------|
| **Ticket** | `TICKET_MARKETONE_UX3_PALIER_B1_CREOLE_BACKGROUNDS` |
| **Version** | **`19.0.15.3.0`** |
| **Branche** | `feat/marketone-ux3-b1-creole-backgrounds` |
| **Jalon** | ADR-031 · Palier A « Tenue » `19.0.15.2.0` |
| **URL** | http://localhost:18079/shop |
| **Base** | `ckr-marketone-01` |
| **Statut** | Recette visuelle MOA — avant merge |

---

## Prérequis

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d ckr-marketone-01 -u dorevia_ckreyol_marketone --stop-after-init
docker restart sandbox-odoo19-odoo-1
```

Hard refresh navigateur.

---

## Palette B1 (référence)

| Token | Hex | Usage |
|---|---|---|
| `$ck-bg-cream` | `#F7EFE4` | Fond page |
| `$ck-bg-green-soft` | `#D9E8D2` | Sidebar panneau |
| `$ck-bg-white` | `#FFFDF8` | Cartes · chip category |
| `#FAF4E8` | `$ck-bg-image` | Zone image produit |
| `$ck-bg-yellow-soft` | `#F6E4A8` | Chip collection · bandeau origin |
| `$ck-bg-red-soft` | `#F1CFC4` | Chip price |
| `$ck-border-soft` | `#E2D2C3` | Bordures |
| `$ck-terracotta` | `#C4715A` | Prix (inchangé Palier A) |

---

## Arbitrages MOA (validés)

| Sujet | Décision |
|---|---|
| Chips | Option B — type UX-1 |
| Chips fixes Tout/Promo/… | Report B2 |
| `$ck-bg-green-deep` | Pas de grand aplat |
| Fonds Palier A | Remplacés sur `/shop` |
| Zone haute | Bandeau SCSS léger |
| Prix terracotta | Conservé |

---

## Captures attendues

| # | Scénario | Fichier suggéré | ☐ |
|---|---|---|---|
| 1 | Avant (19.0.15.2.0) | `marketone_b1_avant_shop.png` | |
| 2 | Après B1 desktop grille | `marketone_b1_apres_desktop.png` | |
| 3 | Sidebar `#D9E8D2` | `marketone_b1_sidebar.png` | |
| 4 | Chips par type (filtre actif) | `marketone_b1_chips_filtre.png` | |
| 5 | Carte + zone image | `marketone_b1_carte_detail.png` | |
| 6 | Porte featured / origin (si dispo) | `marketone_b1_zone_haute.png` | |
| 7 | Mobile ≤768px | `marketone_b1_mobile.png` | |
| 8 | Home (hors scope) | `marketone_b1_home_non_impact.png` | |

---

## Grille validation

| Scénario | Verdict | Notes |
|---|---|---|
| V1 — Page plus chaude / créole | ☐ OK · ☐ réserve · ☐ KO | |
| V2 — Fonds rouge/jaune/vert/blanc harmonieux | ☐ OK · ☐ réserve · ☐ KO | |
| V3 — Premium / épicerie fine | ☐ OK · ☐ réserve · ☐ KO | |
| V4 — Produits prioritaires | ☐ OK · ☐ réserve · ☐ KO | |
| V5 — Cartes sobres (îlots blancs) | ☐ OK · ☐ réserve · ☐ KO | |
| V6 — Sidebar personnalité sans saturation | ☐ OK · ☐ réserve · ☐ KO | |
| V7 — Chips UX-1 par type | ☐ OK · ☐ réserve · ☐ KO | |
| V8 — Mobile lisible | ☐ OK · ☐ réserve · ☐ KO | |
| V9 — Hors scope (header/footer/checkout) | ☐ OK · ☐ KO | |
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
