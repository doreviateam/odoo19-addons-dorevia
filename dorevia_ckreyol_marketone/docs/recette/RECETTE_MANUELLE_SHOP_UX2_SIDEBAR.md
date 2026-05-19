# Recette manuelle — UX-2 Sidebar `/shop` (confort & densité)

| Champ | Valeur |
|-------|--------|
| **Ticket** | `TICKET_MARKETONE_UX2_SHOP_SIDEBAR` |
| **Version** | `19.0.14.0.0` (cible) |
| **URL** | http://localhost:18079/shop |
| **Base** | `ckr-marketone-01` |

---

## Prérequis

- Module **≥ `19.0.13.1.0`** (UX-1 + La Réunion unique).
- Upgrade + **restart** Odoo · hard refresh navigateur.

```bash
odoo-bin -d ckr-marketone-01 -u dorevia_ckreyol_marketone --stop-after-init
```

---

## S1–S4 — Rubriques et ordre (non-régression)

| ID | Vérification | Attendu |
|----|--------------|---------|
| S1 | Ordre vertical | Collections → Catégories → Origines → Prix |
| S2 | Collections | Cases cliquables · filtre OK |
| S3 | Catégories | 13 principales visibles avec 1 filtre (C4) |
| S4 | Origines | Une seule **La Réunion** · autres origines OK |

---

## S5 — Accordéons

| Étape | Action | Attendu |
|-------|--------|---------|
| 1 | Replier / déplier chaque rubrique | Animation Bootstrap OK · chevron visible |
| 2 | Focus clavier (Tab) | Contour focus visible sur bouton section |

---

## S6 — Zones cliquables

| Étape | Action | Attendu |
|-------|--------|---------|
| 1 | Clic sur **libellé** (pas seulement la case) | Bascule le filtre |
| 2 | Surface minimale perçue | Ligne confortable (~40px zone utile) |

---

## S7 — Offcanvas mobile

| Étape | Action | Attendu |
|-------|--------|---------|
| 1 | Viewport &lt; 992px · ouvrir filtres | Même grammaire que desktop |
| 2 | Pas de « Clear Filters » EN | Reset uniquement barre UX-1 si filtres actifs |

---

## S8–S9 — Non-régression fonctionnelle

| ID | Vérification |
|----|--------------|
| S8 | C4 + ordre sidebar (tests auto sidebar) |
| S9 | UX-1 : chips, reset à gauche, compteur, pas de prix implicite |

```bash
odoo-bin -d ckr-marketone-01 --test-tags=dorevia_marketone_shop_sidebar,dorevia_marketone_shop_sidebar_collections --stop-after-init
odoo-bin -d ckr-marketone-01 --test-tags=dorevia_marketone_shop_regression,dorevia_marketone_shop_filter_state --stop-after-init
```

---

## Verdict MOA

| Volet | Verdict |
|-------|---------|
| Desktop | ☐ GO · ☐ réserves |
| Mobile offcanvas | ☐ GO · ☐ réserves |
| Non-régression | ☐ GO |
