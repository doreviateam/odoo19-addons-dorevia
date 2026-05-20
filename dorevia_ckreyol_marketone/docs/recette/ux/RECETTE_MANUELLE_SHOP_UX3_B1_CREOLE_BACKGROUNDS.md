# Recette manuelle — UX-3 Palier B1 — Chaîne chromatique CK `/shop`

| Champ | Valeur |
|-------|--------|
| **Ticket** | [`TICKET_MARKETONE_UX3_PALIER_B1_CREOLE_BACKGROUNDS`](../../tickets/ux/TICKET_MARKETONE_UX3_PALIER_B1_CREOLE_BACKGROUNDS.md) |
| **Version** | **`19.0.15.7.6`** |
| **Branche** | `feat/marketone-ux3-b1-creole-backgrounds` |
| **Doctrine** | Base sobre · body `#FFF` · pas dégradé · chaleur localisée |
| **URL** | http://localhost:18079/shop?db=ckr-marketone-01 |
| **Base** | `ckr-marketone-01` |
| **Statut** | **GO visuel MOA final** — merge autorisé (2026-05-20) |

---

## Chaîne livrée (jalon B1)

```text
body / wrap shop     → #FFFFFF
sidebar rail         → #FFFDF8
cartes corps         → #FDF9F0
zone image produit   → #F8EEDB
bordures             → #E2D4BC
chips                → pastel discrets (type UX-1)
prix                 → #C4715A
```

---

## Grille validation finale

| Scénario | Verdict | Notes |
|---|---|---|
| F1 — Fond global neutre premium | ☑ OK | |
| F2 — Sidebar intégrée | ☑ OK | |
| F3 — Cartes écrin | ☑ OK | |
| F4 — Zone image `#F8EEDB` | ☑ OK | MOA 3.1 |
| F4b — Bordures `#E2D4BC` | ☑ OK | MOA 3.2 |
| F5 — Pas bloc vert / beige lourd | ☑ OK | |
| F6 — Chips pastel | ☑ OK | |
| V9 — Home hors scope | ☑ OK | |
| V10 — Tests auto 21/21 | ☑ OK | |

---

## Verdict MOA

| Verdict | ☑ |
|---|---|
| **GO visuel B1 — merge autorisé** | ☑ (2026-05-20) |

---

## Historique

| Version | Verdict MOA |
|---|---|
| `19.0.15.3.0`–`19.0.15.5.0` | NO GO |
| `19.0.15.7.3`–`19.0.15.7.5` | Base OK + ajustements fins |
| `19.0.15.7.6` | **GO visuel final** |
