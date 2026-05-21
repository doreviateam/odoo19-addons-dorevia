# Recette manuelle — UX-1 État utilisateur `/shop`

| Champ | Valeur |
|-------|--------|
| **Ticket** | `TICKET_MARKETONE_UX1_SHOP_ETAT_UTILISATEUR` |
| **Version cible** | **`19.0.15.9.4`** |
| **URL** | http://localhost:18079/shop |
| **Base** | `ckr-marketone-01` |
| **Statut recette** | **GO MOA** — wording état vide **`9.4`** validé navigateur |
| **Rapport exécution** | [`RAPPORT_RECETTE_SHOP_UX1_ETAT_FILTRES_20260521.md`](./RAPPORT_RECETTE_SHOP_UX1_ETAT_FILTRES_20260521.md) |

---

## Prérequis

- Module `dorevia_ckreyol_marketone` **≥ 19.0.13.0.4** (upgrade `-u` + **restart** conteneur Odoo).
- Assets frontend recompilés (mode dev ou `-u`).

---

## Règles MOA (R1–R4)

| ID | Règle |
|----|--------|
| **R1** | Sans filtre prix **explicite**, les `remove_url` des chips **ne doivent pas** contenir `min_price` / `max_price`. Les bornes calculées pour le slider ne sont pas des filtres actifs. |
| **R2** | Compteur haut : **`{n} produits disponibles`** / **`1 produit disponible`** · si **0 avec filtres actifs** → **`Aucun produit trouvé`** (pas « disponible ») · si **0 sans filtre** → **`Aucun produit disponible`**. |
| **R3** | Les chips actives peuvent afficher un compteur **`(n)`** entre parenthèses si fiable · **pas** de chiffre sur la chip prix. |
| **R4** | État vide central (filtres / recherche · 0 résultat) : **`Aucun produit ne correspond à cette sélection`** · CTA **`Effacer les filtres`** conservé. |

---

## U1 — Compteur sans filtre (MOA Q1 + R2)

> **Mise à jour `19.0.15.8.5`** — ligne principale compacte : compteur gauche · recherche centre · tri droite · chips L2. Voir [`RECETTE_MANUELLE_SHOP_GRID_TITLE.md`](../boutique/RECETTE_MANUELLE_SHOP_GRID_TITLE.md) § V0.

| Étape | Action | Attendu |
|-------|--------|---------|
| 1 | Ouvrir `/shop` sans paramètres | **`N produits disponibles`** à **gauche** · recherche **centrée** · tri **droite** · **même ligne** |
| 2 | Avec filtres | Compteur **« disponibles »** inchangé · chips **ligne 2** avec `(n)` optionnel |
| 3 | Pagination | Compteur = total catalogue filtré (pas cartes page seule) |
| 4 | Recherche sans filtre sidebar | Compteur « disponibles » · pas de chips |

---

## U2 — Chips collection (R1)

| Étape | Action | Attendu |
|-------|--------|---------|
| 1 | Cocher une collection sidebar | Chip **`Nom (n)`** si n fiable · sans « Collection : » |
| 2 | Inspecter l’URL de la croix **avant** clic | **Pas** de `min_price` / `max_price` |
| 3 | Cliquer la croix | Collection retirée · autres filtres inchangés |

---

## U3 — Chips catégorie (R1)

| Étape | Action | Attendu |
|-------|--------|---------|
| 1 | Filtrer « Biscuits salés » | Chip **`Biscuits salés (n)`** · n cohérent avec la catégorie dans le contexte |
| 2 | Inspecter `remove_url` | **Pas** de `min_price` / `max_price` si prix non filtré |
| 3 | Retirer la chip | Catégorie inactive · grille élargie |

---

## U4 — Chips origine (R1)

| Étape | Action | Attendu |
|-------|--------|---------|
| 1 | Filtrer Origine « Martinique » | Chip **`Martinique (n)`** (sans préfixe) |
| 2 | Combiner catégorie + origine | Deux chips |
| 3 | Retirer la chip catégorie | Origine conservée · URL **sans** prix implicite |
| 4 | Retirer la chip origine | Catégorie conservée si encore active |

---

## U5 — Chip prix (MOA Q3)

| Étape | Action | Attendu |
|-------|--------|---------|
| 1 | Ajuster le slider prix (fourchette ≠ bornes catalogue) | Chip **« Prix : … »** **sans `(n)`** · URL avec `min_price` / `max_price` |
| 2 | Retirer la chip prix | Paramètres prix retirés de l’URL |
| 3 | Avec prix actif + catégorie | Retirer la chip catégorie **conserve** `min_price` / `max_price` |

---

## U6 — Reset global + pastels chips (`19.0.13.0.7`)

| Étape | Action | Attendu |
|-------|--------|---------|
| 1 | Plusieurs filtres actifs | Barre **ligne secondaire** · sous la ligne principale · au-dessus de la grille |
| 2 | Ordre barre | **Effacer les filtres** à **gauche**, puis les chips (`reset \| chip × chip × …`) |
| 3 | Couleurs chips | Fonds pastel **différenciés** · rotation déterministe par rang (sable, pêche, sauge, rosé, lilac) |
| 4 | Sidebar | **Pas** de « Clear Filters » (desktop ni offcanvas) |
| 5 | Clic « Effacer les filtres » | `/shop` propre · plus de chips |

---

## U7 — Porte sans chip (MOA Q2)

> **Mise à jour `19.0.15.8.4`** — portes catalogue : voir [`RECETTE_MANUELLE_SHOP_GRID_TITLE.md`](../boutique/RECETTE_MANUELLE_SHOP_GRID_TITLE.md) § V6.

| Étape | Action | Attendu |
|-------|--------|---------|
| 1 | `/shop?marketone_mode=origin` | Pas de chip porte · titre porte **Origines** (pas le compteur catalogue) |

---

## U8 — Compteurs chips `(n)` (`19.0.15.9.0`)

| Étape | Action | Attendu |
|-------|--------|---------|
| 1 | Filtrer catégorie + origine | Chips **`Catégorie (n)`** · **`Origine (n)`** · compteur global = intersection |
| 2 | Chip prix active | **Pas** de `(n)` sur la chip prix |
| 3 | Retirer une chip | Compteur global et `(n)` des chips restantes se recalculent |
| 4 | Chips à 0 résultat | `(0)` acceptable si fiable (ex. combo restrictive) |

---

## U9 — État vide 0 résultat (`19.0.15.9.2` / `19.0.15.9.3`)

> **R4** — distinguer compteur haut et message central. Voir aussi [`RECETTE_MANUELLE_SHOP_GRID_TITLE.md`](../boutique/RECETTE_MANUELLE_SHOP_GRID_TITLE.md) § état vide.

### Cas A — Recherche sans hit

| Étape | Action | Attendu |
|-------|--------|---------|
| 1 | `/shop?search=zzzzmarketone-zero-zzzz` | Compteur **`Aucun produit trouvé`** |
| 2 | Zone centrale | **`Aucun produit ne correspond à cette sélection`** · CTA **`Effacer les filtres`** visible |
| 3 | Paragraphe Odoo « Aucun résultat pour… » | **Absent** (masqué en contexte filtré) |

### Cas B — Combo sidebar restrictive (capture MOA)

Scénario illustré : **Biscuits salés** + **La Réunion** + **Apéritif créole** → grille vide.

| Étape | Action | Attendu |
|-------|--------|---------|
| 1 | Cocher catégorie **Biscuits salés**, origine **La Réunion**, collection **Apéritif créole** | Grille vide |
| 2 | Compteur haut | **`Aucun produit trouvé`** |
| 3 | État central | **`Aucun produit ne correspond à cette sélection`** |
| 4 | Chips | Visibles · ex. `Biscuits salés (0)` · `La Réunion (0)` · `Apéritif créole (0)` |
| 5 | Référence visuelle **KO avant 9.3** | [`capture_recette_ux1_avant_wording_etat_vide_20260521.png`](./capture_recette_ux1_avant_wording_etat_vide_20260521.png) |

---

## U10–U14 — Non-régression

| ID | Vérification |
|----|----------------|
| U10 | Ordre sidebar : Collections → Catégories → Origines → Prix |
| U11 | C4 : avec **1 catégorie** cochée, les **13 principales** restent visibles |
| U12 | Compteur ligne résultat = total filtré · libellés R2 · ≠ cartes page seule |
| U13 | Pas de warning `@class` au chargement |
| U14 | Mobile : chips en wrap · reset lisible |

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
| `test_r2_grid_title_in_header_not_toolbar` | Compteur ligne résultat · absent de la zone tri (pas de doublon) |
| `test_ux1_chip_bar_after_toolbar_above_grid` | Chips sous la ligne recherche / résultat / tri |

Suite complète UX-1 + sidebar (recette 2026-05-21) :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone \
  --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_shop_regression,dorevia_marketone_shop_filter_state,dorevia_marketone_shop_sidebar,dorevia_marketone_shop_sidebar_collections \
  --http-port=8073
```

Attendu : **`0 failed, 0 error(s) of 58 tests`** (relance post-`9.3` : **OK**).

**Contrôle manuel express** (30 s) après upgrade **≥ 9.3** :

1. Cocher **Condiments** → sidebar : **13** principales toujours visibles.
2. `/shop?search=zzzzmarketone-zero-zzzz` → **`Aucun produit disponible`** + état central **`Aucun produit ne correspond à vos critères`**.
3. Combo **U9 cas B** (capture) → mêmes libellés · chips `(0)` visibles.

---

## Historique recette (synthèse)

| Version | Verdict | Note |
|---------|---------|------|
| `8.5`/`8.6` | GO | Layout L1 compact · CSS Sass OK |
| `9.0` | GO | Compteur « disponibles » · chips `(n)` · 55 tests |
| `9.1` | GO | Sidebar Collections → Catégories |
| `9.2` | Livré | État vide contextualisé |
| `9.4` | **GO MOA** | Compteur zéro filtré **`Aucun produit trouvé`** · état central **`…cette sélection`** |

**Valeurs compteur validées (`9.0`+)** — libellé **toujours** « …disponible(s) » :

| URL | Compteur haut |
|-----|---------------|
| `/shop` | `50 produits disponibles` |
| `?marketone_category=condiments-73` | `4 produits disponibles` |
| `?marketone_category=biscuits-sales-70` | `6 produits disponibles` |
| `?…biscuits-sales-70&attribute_values=3-20` | `1 produit disponible` |
| `?marketone_collection=aperitif-creole` | `8 produits disponibles` |
| `?search=zzzz…` ou combo 0 résultat | **`Aucun produit disponible`** (`9.3`) |

Captures GO : [`capture_recette_ux1_ok_biscuits_20260521_2104.png`](./capture_recette_ux1_ok_biscuits_20260521_2104.png) · [`capture_recette_ux1_ok_mobile_combo_20260521_2104.png`](./capture_recette_ux1_ok_mobile_combo_20260521_2104.png)

---

## Verdict MOA (2026-05-19 — historique fonctionnel)

| Volet | Verdict |
|-------|---------|
| **Visuel sans filtre** | GO — compteur « trouvés », pas de chips, sidebar / grille OK |
| **Visuel avec filtres** | **GO final** — reset à gauche · pastels · barre L2 sous ligne principale (`8.5`/`8.6`) |
| **Hors UX-1** | Réunion/Reunion (BO) · densité sidebar / accordéons (UX-2) · images (UX-3) |
| **Réserve non bloquante** | Lien « Effacer les filtres » : renforcement visuel possible en UX-2+ |

### Clôture fonctionnelle — **GO MOA** (2026-05-19)

| # | Cas | Résultat navigateur | Auto |
|---|-----|---------------------|------|
| **F1** | Retrait chip **Apéritif créole** | `href` = `/shop`, pas de prix | ☑ |
| **F2** | Retrait chip **Condiments** | `href` = `/shop`, pas de prix | ☑ |
| **F3** | **Condiments + Martinique** → retirer catégorie | `/shop?attribute_values=3-20`, origine conservée | ☑ |
| **F4** | Reset barre = sidebar | les deux `href` = `/shop` | ☑ |

Tests : `dorevia_marketone_shop_regression` + `dorevia_marketone_shop_filter_state` **19/19 OK** (`19.0.13.0.7`).

---

## Références

| Document | Rôle |
|----------|------|
| [`RECETTE_MANUELLE_SHOP_GRID_TITLE.md`](../boutique/RECETTE_MANUELLE_SHOP_GRID_TITLE.md) | Haut grille / compteur / état vide `19.0.15.9.3` |
| [`TICKET_MARKETONE_UX1_SHOP_ETAT_UTILISATEUR.md`](../../tickets/ux/TICKET_MARKETONE_UX1_SHOP_ETAT_UTILISATEUR.md) | Cadrage UX-1 |

---

## Signal Dev post-recette

```text
Recette UX-1 /shop — GO MOA wording état vide 9.4 — Aucun produit trouvé + …cette sélection — Effacer les filtres OK — chips (0) OK — réserve non bloquante : discrétion compteur haut.
```
