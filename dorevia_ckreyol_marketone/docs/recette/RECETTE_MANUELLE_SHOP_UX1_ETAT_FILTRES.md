# Recette manuelle — UX-1 État utilisateur `/shop`

| Champ | Valeur |
|-------|--------|
| **Ticket** | `TICKET_MARKETONE_UX1_SHOP_ETAT_UTILISATEUR` |
| **Version** | `19.0.13.0.5` |
| **URL** | http://localhost:18079/shop |
| **Base** | `ckr-marketone-01` |

---

## Prérequis

- Module `dorevia_ckreyol_marketone` **≥ 19.0.13.0.4** (upgrade `-u` + **restart** conteneur Odoo).
- Assets frontend recompilés (mode dev ou `-u`).

---

## Règles MOA (R1 / R2)

| ID | Règle |
|----|--------|
| **R1** | Sans filtre prix **explicite**, les `remove_url` des chips **ne doivent pas** contenir `min_price` / `max_price`. Les bornes calculées pour le slider ne sont pas des filtres actifs. |
| **R2** | Le compteur affiche le **total des résultats filtrés** (toutes pages), libellé **« N produit(s) trouvé(s) »** — pas le nombre de cartes visibles sur la page courante. |

---

## U1 — Compteur sans filtre (MOA Q1 + R2)

| Étape | Action | Attendu |
|-------|--------|---------|
| 1 | Ouvrir `/shop` sans paramètres | Compteur « **N** produit(s) trouvé(s) » dans la toolbar |
| 2 | Vérifier | Pas de barre chips au-dessus de la grille |
| 3 | Si pagination (ex. 27 total, 24 cartes page 1) | Le compteur reste **27 produits trouvés** (pas 24) |

---

## U2 — Chips collection (R1)

| Étape | Action | Attendu |
|-------|--------|---------|
| 1 | Cocher une collection sidebar | Chip avec **nom seul** (sans « Collection : ») |
| 2 | Inspecter l’URL de la croix **avant** clic | **Pas** de `min_price` / `max_price` |
| 3 | Cliquer la croix | Collection retirée · autres filtres inchangés |

---

## U3 — Chips catégorie (R1)

| Étape | Action | Attendu |
|-------|--------|---------|
| 1 | Filtrer « Biscuits salés » | Chip « Biscuits salés » |
| 2 | Inspecter `remove_url` | **Pas** de `min_price` / `max_price` si prix non filtré |
| 3 | Retirer la chip | Catégorie inactive · grille élargie |

---

## U4 — Chips origine (R1)

| Étape | Action | Attendu |
|-------|--------|---------|
| 1 | Filtrer Origine « Martinique » | Chip « Martinique » (sans préfixe) |
| 2 | Combiner catégorie + origine | Deux chips |
| 3 | Retirer la chip catégorie | Origine conservée · URL **sans** prix implicite |
| 4 | Retirer la chip origine | Catégorie conservée si encore active |

---

## U5 — Chip prix (MOA Q3)

| Étape | Action | Attendu |
|-------|--------|---------|
| 1 | Ajuster le slider prix (fourchette ≠ bornes catalogue) | Chip **« Prix : … »** · URL avec `min_price` / `max_price` |
| 2 | Retirer la chip prix | Paramètres prix retirés de l’URL |
| 3 | Avec prix actif + catégorie | Retirer la chip catégorie **conserve** `min_price` / `max_price` |

---

## U6 — Reset global (MOA Q4 + reset unique `19.0.13.0.5`)

| Étape | Action | Attendu |
|-------|--------|---------|
| 1 | Plusieurs filtres actifs | « Effacer les filtres » dans la **barre chips** (même ligne, après les chips) |
| 2 | Sidebar | **Pas** de bouton « Clear Filters » (desktop ni offcanvas) |
| 3 | Clic « Effacer les filtres » | `/shop` propre · plus de chips |

---

## U7 — Porte sans chip (MOA Q2)

| Étape | Action | Attendu |
|-------|--------|---------|
| 1 | `/shop?marketone_mode=origin` | Pas de chip porte · compteur « N produits trouvés » visible |

---

## U8–U12 — Non-régression

| ID | Vérification |
|----|----------------|
| U8 | Ordre sidebar : Collections → Catégories → Origines → Prix |
| U9 | C4 : avec **1 catégorie** cochée, les **13 principales** restent visibles (pas seulement Condiments + Fécules) |
| U10 | Compteur = total filtré · libellé **trouvé(s)** · ≠ cartes page seule (R2) |
| U11 | Pas de warning `@class` au chargement |
| U12 | Mobile : chips en wrap · reset lisible |

---

## Tests auto

**Détection régressions connues (R1 + C4 + R2)** — tag dédié, ~30 s :

```bash
odoo-bin -d ckr-marketone-01 \
  --test-tags=dorevia_marketone_shop_regression \
  --stop-after-init
```

| Test | Régression détectée |
|------|---------------------|
| `test_r1_chip_remove_category_no_implicit_price` | Prix implicite dans `remove_url` chip |
| `test_c4_sidebar_keeps_primaries_when_category_active` | Catégories sidebar qui disparaissent au clic |
| `test_r2_counter_wording_trouves` | Compteur sans libellé « trouvé(s) » |

Suite complète UX-1 + sidebar :

```bash
odoo-bin -d ckr-marketone-01 --test-tags=dorevia_marketone_shop_filter_state --stop-after-init
odoo-bin -d ckr-marketone-01 --test-tags=dorevia_marketone_shop_sidebar,dorevia_marketone_shop_sidebar_collections --stop-after-init
```

**Contrôle manuel express** (30 s) après upgrade :

1. Cocher **Condiments** → sidebar : **13** principales toujours visibles.
2. Inspecter la croix chip **Condiments** → URL **sans** `min_price` / `max_price`.

---

## Verdict MOA (recette 2026-05-19)

| Volet | Verdict |
|-------|---------|
| **Visuel sans filtre** | GO — compteur « trouvés », pas de chips, sidebar / grille OK |
| **Visuel avec filtres** | GO proposable — chips, reset, compteur, cohérence sidebar |
| **Hors UX-1** | Réunion/Reunion (BO) · densité sidebar / espacement chips (UX-2) · images (UX-3) |

### Clôture fonctionnelle — **GO MOA** (2026-05-19)

| # | Cas | Résultat navigateur | Auto |
|---|-----|---------------------|------|
| **F1** | Retrait chip **Apéritif créole** | `href` = `/shop`, pas de prix | ☑ |
| **F2** | Retrait chip **Condiments** | `href` = `/shop`, pas de prix | ☑ |
| **F3** | **Condiments + Martinique** → retirer catégorie | `/shop?attribute_values=3-20`, origine conservée | ☑ |
| **F4** | Reset barre = sidebar | les deux `href` = `/shop` | ☑ |

Tests : `dorevia_marketone_shop_regression` **3/3 OK**.

Captures : `marketone_ux1_cloture_f1_collection.png` … `f4_after_reset.png` (`/private/tmp/`).

```bash
odoo-bin -d ckr-marketone-01 --test-tags=dorevia_marketone_shop_regression --stop-after-init
```
