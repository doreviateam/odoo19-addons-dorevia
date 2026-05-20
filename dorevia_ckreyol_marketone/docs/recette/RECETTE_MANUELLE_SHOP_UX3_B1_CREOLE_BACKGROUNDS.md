# Recette manuelle — UX-3 Palier B1 — Fonds créoles premium `/shop`

| Champ | Valeur |
|-------|--------|
| **Ticket** | `TICKET_MARKETONE_UX3_PALIER_B1_CREOLE_BACKGROUNDS` |
| **Version** | **`19.0.15.3.0`** |
| **Branche** | `feat/marketone-ux3-b1-creole-backgrounds` |
| **Jalon** | ADR-031 · Palier A « Tenue » `19.0.15.2.0` |
| **URL** | http://localhost:18079/shop |
| **Base** | `ckr-marketone-01` |
| **Statut** | **GO visuel proposable** — merge après validation mobile MOA si besoin |

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

## Recette exécutée (2026-05-20)

**Environnement** : `feat/marketone-ux3-b1-creole-backgrounds` · `19.0.15.3.0`.

### Technique

| Contrôle | Résultat |
|---|---|
| Upgrade `-u dorevia_ckreyol_marketone` | OK |
| Restart conteneur | OK |
| Smoke `/shop` | `200` |
| Smoke filtre collection | `200` |
| Smoke featured / origin | `200` |
| Tests auto regression · filter_state · sidebar_ux2 | **21/21 OK** (`0 failed, 0 error`) |
| Home hors scope `/` | OK — `marketone-root`, pas `marketone-shop` |

### Contrôles visuels / calculés

| Point | Résultat |
|---|---|
| Fond `/shop` `#F7EFE4` | OK |
| Sidebar `#D9E8D2` | OK |
| Cartes `#FFFDF8`, bordure `#E2D2C3`, radius `14px` | OK |
| Zone image `#FAF4E8`, `contain`, `mix-blend-mode: normal` | OK |
| Prix terracotta `#C4715A` | OK |
| Chip collection jaune `#F6E4A8` | OK |
| Bandeau featured vert doux | OK |
| Bandeau origin jaune doux | OK |
| Scroll horizontal | Non détecté |

### Captures produites

| Scénario | Fichier | ☐ |
|---|---|---|
| Desktop grille | `/private/tmp/marketone_b1_apres_desktop.png` | ☑ |
| Sidebar | `/private/tmp/marketone_b1_sidebar.png` | ☑ |
| Chips filtre actif | `/private/tmp/marketone_b1_chips_filtre.png` | ☑ |
| Détail carte | `/private/tmp/marketone_b1_carte_detail.png` | ☑ |
| Zone haute featured | `/private/tmp/marketone_b1_zone_haute_featured.png` | ☑ |
| Zone haute origin | `/private/tmp/marketone_b1_zone_haute_origin.png` | ☑ |
| Home non impactée | `/private/tmp/marketone_b1_home_non_impact.png` | ☑ |
| Avant `19.0.15.2.0` | Non produite (environnement maintenu sur branche B1) | — |
| Mobile ≤768px | Non validé (viewport outil) | ☐ réserve |

---

## Grille validation

| Scénario | Verdict | Notes |
|---|---|---|
| V1 — Page plus chaude / créole | ☑ OK | |
| V2 — Fonds rouge/jaune/vert/blanc harmonieux | ☑ OK | |
| V3 — Premium / épicerie fine | ☑ OK | |
| V4 — Produits prioritaires | ☑ OK | |
| V5 — Cartes sobres (îlots blancs) | ☑ OK | |
| V6 — Sidebar personnalité sans saturation | ☑ OK | |
| V7 — Chips UX-1 par type | ☑ OK | collection jaune confirmée |
| V8 — Mobile lisible | ☐ réserve | CSS responsive Palier A inchangé |
| V9 — Hors scope | ☑ OK | Home OK |
| V10 — Tests auto 21/21 | ☑ OK | |

---

## Verdict recette

| Verdict | ☑ |
|---|---|
| **GO technique** | ☑ |
| **GO visuel proposable** | ☑ |
| **GO merge** | ☐ — validation mobile MOA optionnelle puis GO explicite |
| **Réserve** | Capture avant 19.0.15.2.0 absente · mobile 768px non capturé |

**Merge** : uniquement sur **GO explicite MOA** post-revue captures.
