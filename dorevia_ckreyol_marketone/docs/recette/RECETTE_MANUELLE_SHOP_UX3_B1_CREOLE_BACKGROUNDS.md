# Recette manuelle — UX-3 Palier B1 — Chaîne chromatique CK `/shop`

| Champ | Valeur |
|-------|--------|
| **Ticket** | `TICKET_MARKETONE_UX3_PALIER_B1_CREOLE_BACKGROUNDS` |
| **Version** | **`19.0.15.7.0`** (B1.4 — premium first, ocre dilué) |
| **Branche** | `feat/marketone-ux3-b1-creole-backgrounds` |
| **Doctrine** | **Aucun dégradé** · aplats + bordures chaudes + rappels localisés |
| **URL** | http://localhost:18079/shop?db=ckr-marketone-01 |
| **Base** | `ckr-marketone-01` |
| **Statut** | Recette MOA à exécuter |

---

## Prérequis

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d ckr-marketone-01 -u dorevia_ckreyol_marketone --stop-after-init
docker restart sandbox-odoo19-odoo-1
```

Hard refresh. **Safari** : désactiver « HTTPS uniquement » ou utiliser Chrome/Firefox pour `http://localhost:18079`.

---

## Palette source CK (référence — non saturée à l’écran)

| Hex | Nom | Usage B1 |
|---|---|---|
| `#43350F` | Brun | Chaleur texte / page |
| `#A41756` | Baie | → rouge pastel chips |
| `#2ABD2A` | Vert vif | → **dilué** mist / sidebar / actifs |
| `#A86F08` | Ocre | → vanille / jaune doux |
| `#7286AE` | Ardoise | Hors scope B1 fonds |

Voir ticket §15 pour la table de traduction complète.

---

## Chaîne chromatique (MOA)

```text
body quasi neutre (hors scope)
→ fond page #F5E4D0 (ocre dilué)
→ sidebar #F3EDE5 (lin, filet sauge)
→ cartes #FFFDF8
→ image #F8EDD4
→ chips jaune / vert / rouge pastel
→ prix #C4715A
```

**Interdit** : `linear-gradient`, sidebar verte massive `#D9E8D2`, patchwork, rendu lavé type landing page.

---

## Grille validation B1.4 (premium first)

| Scénario | Verdict | Notes |
|---|---|---|
| P1 — Épicerie fine, pas bio-discount | ☐ OK · ☐ réserve · ☐ KO | |
| P2 — Chaleur ocre sans saturation | ☐ OK · ☐ réserve · ☐ KO | |
| P3 — Sidebar discrète (lin, pas bloc vert) | ☐ OK · ☐ réserve · ☐ KO | |

## Grille validation B1.3

| Scénario | Verdict | Notes |
|---|---|---|
| C1 — Progression page → sidebar → cartes lisible | ☐ OK · ☐ réserve · ☐ KO | |
| C2 — Aucun dégradé visible | ☐ OK · ☐ KO | inspecteur CSS |
| C3 — Ligne CK portée (pas trop pâle) | ☐ OK · ☐ réserve · ☐ KO | |
| C4 — Sidebar végétal pâle, pas bloc vert | ☐ OK · ☐ réserve · ☐ KO | |
| C5 — Cartes écrin vs fond page | ☐ OK · ☐ réserve · ☐ KO | |
| C6 — Chips pastel secondaires | ☐ OK · ☐ réserve · ☐ KO | |
| C7 — Premium / pas bio-discount | ☐ OK · ☐ réserve · ☐ KO | |
| V9 — Hors scope home | ☐ OK · ☐ KO | |
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
| **GO visuel B1 — merge** | |
| **GO avec réserves** | |
| **NO GO** | |

---

## Historique

| Version | Verdict |
|---|---|
| `19.0.15.3.0`–`19.0.15.5.0` | NO GO — juxtaposition / trop lavé / dégradés |
| `19.0.15.6.x` | NO GO / fix SCSS |
| `19.0.15.7.0` | Recette B1.4 premium first |
