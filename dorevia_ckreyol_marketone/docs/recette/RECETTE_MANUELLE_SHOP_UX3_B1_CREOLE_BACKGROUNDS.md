# Recette manuelle — UX-3 Palier B1 — Chaîne chromatique CK `/shop`

| Champ | Valeur |
|-------|--------|
| **Ticket** | `TICKET_MARKETONE_UX3_PALIER_B1_CREOLE_BACKGROUNDS` |
| **Version** | **`19.0.15.7.5`** |
| **Branche** | `feat/marketone-ux3-b1-creole-backgrounds` |
| **Doctrine** | Base sobre · body `#FFF` · pas dégradé · chaleur localisée |
| **URL** | http://localhost:18079/shop?db=ckr-marketone-01 |
| **Base** | `ckr-marketone-01` |
| **Statut** | **Base OK MOA** — recette finale avant GO merge |

---

## Prérequis

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d ckr-marketone-01 -u dorevia_ckreyol_marketone --stop-after-init
docker restart sandbox-odoo19-odoo-1
```

Hard refresh navigateur.

---

## Chaîne actuelle (B1.5)

```text
body / wrap shop     → #FFFFFF
sidebar rail         → #FFFDF8 (blanc chaud)
cartes               → #FFFDF8 + ombre écrin
zone image produit   → #F8EEDB (ajustement MOA 3.1)
chips                → pastel discrets
prix                 → #C4715A
```

**Interdit** : bloc beige conteneur · bloc vert sidebar · dégradés · saturation.

---

## Grille validation finale

| Scénario | Verdict | Notes |
|---|---|---|
| F1 — Fond global neutre premium | ☐ OK · ☐ réserve · ☐ KO | |
| F2 — Sidebar intégrée, pas dominante | ☐ OK · ☐ réserve · ☐ KO | |
| F3 — Cartes écrin lisibles | ☐ OK · ☐ réserve · ☐ KO | |
| F4 — Zone image `#F8EEDB` chaleur discrète | ☑ OK MOA 3.1 | |
| F4b — Bordures `#E2D4BC` chaudes (pas grises) | ☐ OK · ☐ réserve · ☐ KO | |
| F5 — Pas retour bloc vert / beige lourd | ☐ OK · ☐ KO | |
| F6 — Chips pastel secondaires | ☐ OK · ☐ réserve · ☐ KO | |
| V9 — Home hors scope | ☐ OK · ☐ KO | |
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
| **Base OK — ajustements fins** | ☑ (MOA 2026-05-20) |
| **NO GO** | |

---

## Historique

| Version | Verdict MOA |
|---|---|
| `19.0.15.3.0`–`19.0.15.5.0` | NO GO |
| `19.0.15.7.3` | Base sobre OK |
| `19.0.15.7.4` | 3.1 image `#F8EEDB` validé |
| `19.0.15.7.5` | 3.2 bordures `#E2D4BC` |
