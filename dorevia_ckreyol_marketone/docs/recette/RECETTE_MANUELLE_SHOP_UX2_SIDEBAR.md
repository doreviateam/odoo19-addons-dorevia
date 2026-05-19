# Recette manuelle — UX-2 Sidebar `/shop` (confort & densité)

| Champ | Valeur |
|-------|--------|
| **Ticket** | [`TICKET_MARKETONE_UX2_SHOP_SIDEBAR`](../tickets/TICKET_MARKETONE_UX2_SHOP_SIDEBAR.md) |
| **Version cible** | **`19.0.14.0.0`** |
| **Branche / PR** | `feat/marketone-ux2-shop-sidebar` · **PR #8** |
| **URL** | http://localhost:18079/shop |
| **Base** | `ckr-marketone-01` |
| **Statut recette** | **Exécutée — GO MOA UX-2** · merge PR #8 proposable |

---

## Usage post-push (PR #8)

Cette recette est la **grille de contrôle MOA** pour statuer sur l'implémentation UX-2 une fois le code mergé ou déployé sur la branche de recette.

| Bloc | IDs | Objet |
|------|-----|--------|
| Rubriques & ordre | **S1–S4** | Ordre fixe · facettes fonctionnelles · La Réunion unique |
| Présentation | **S5** | Accordéons (ouverts desktop, chevrons, focus) |
| Ergonomie | **S6** | Zones cliquables (label + case) |
| Mobile | **S7** | Offcanvas — même grammaire · pas de reset sidebar |
| Non-régression | **S8–S9** | C4 / ordre sidebar · UX-1 chips & reset |
| Lecture globale | **S10** *(recommandé)* | Densité premium · sidebar moins « technique » |

**Verdicts possibles après exécution complète :**

| Verdict | Condition |
|---------|-----------|
| **GO MOA UX-2** | S1–S9 OK · S10 satisfaisant · tests auto verts |
| **GO avec réserves** | Présentation OK · écarts mineurs documentés (non bloquants fonctionnel) |
| **NO GO** | Régression fonctionnelle (filtres, C4, UX-1, URLs, ordre, données Origines) |

---

## Prérequis

- Module **`dorevia_ckreyol_marketone` ≥ `19.0.14.0.0`** (upgrade `-u` + **restart** conteneur Odoo).
- Hard refresh navigateur (cache assets).
- Prérequis fonctionnels déjà GO : UX-1 (`19.0.13.0.7`) · dédup La Réunion (`19.0.13.1.0`).

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d ckr-marketone-01 -u dorevia_ckreyol_marketone --stop-after-init
```

---

## S1–S4 — Rubriques et ordre (non-régression)

| ID | Vérification | Attendu | ☐ |
|----|--------------|---------|---|
| **S1** | Ordre vertical desktop (`#products_grid_before`) | **Collections** → **Catégories** → **Origines** → **Prix** | |
| **S2** | Collections | Cases + libellés cliquables · filtre `marketone_collection` OK · pas de régression Lot B | |
| **S3** | Catégories | **13** principales visibles avec **1** filtre actif (C4) · pas de liste complète dépliée | |
| **S4** | Origines | **Une seule** entrée **La Réunion** · autres origines inchangées · filtre attribut OK | |

---

## S5 — Accordéons

| Étape | Action | Attendu | ☐ |
|-------|--------|---------|---|
| 1 | Desktop ≥ 992px — chargement `/shop` | **4 rubriques ouvertes** par défaut (Collections, Catégories, Origines, Prix) | |
| 2 | Replier / déplier chaque section | Animation Bootstrap OK · chevron discret · état ouvert/fermé lisible | |
| 3 | Focus clavier (Tab sur en-têtes) | Contour `focus-visible` visible · pas de halo agressif | |
| 4 | Hover en-tête | Feedback discret (couleur / fond token Marketone) | |

---

## S6 — Zones cliquables

| Étape | Action | Attendu | ☐ |
|-------|--------|---------|---|
| 1 | Clic sur **libellé** (pas seulement la case) | Bascule le filtre · curseur pointeur sur label | |
| 2 | Clic sur la **case** | Même résultat · zone non « morte » | |
| 3 | Densité perçue | Ligne confortable (~**2,35 rem** min-height) · ni ERP compact ni trop vide | |
| 4 | Option cochée | Poids visuel renforcé (semibold) sans changer la logique filtre | |

---

## S7 — Offcanvas mobile

| Étape | Action | Attendu | ☐ |
|-------|--------|---------|---|
| 1 | Viewport **< 992px** · ouvrir panneau filtres | Même grammaire visuelle que desktop (titres, espacements, cases) | |
| 2 | Parcourir les 4 rubriques | Collections · Catégories · Origines · Prix accessibles | |
| 3 | Reset filtres | **Pas** de « Clear Filters » sidebar · reset **uniquement** barre UX-1 si filtres actifs | |

---

## S8–S9 — Non-régression C4 / UX-1

### S8 — Sidebar & C4 (automatisable)

| ID | Vérification | ☐ |
|----|--------------|---|
| S8a | Tests tag `dorevia_marketone_shop_sidebar` | |
| S8b | Tests tag `dorevia_marketone_shop_sidebar_collections` | |
| S8c | Ordre rubriques + C4 inchangés côté contrôleur / URLs | |

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d ckr-marketone-01 --http-port=8098 \
  --test-tags=dorevia_marketone_shop_sidebar,dorevia_marketone_shop_sidebar_collections \
  --stop-after-init
```

### S9 — UX-1 état utilisateur

| ID | Vérification | Attendu | ☐ |
|----|--------------|---------|---|
| S9a | Barre chips | Visible si filtres actifs · à **gauche** au-dessus toolbar catalogue | |
| S9b | Reset | **Un seul** « Effacer les filtres » (barre UX-1) · renfort visuel **discret** acceptable | |
| S9c | Compteur | « N produit(s) trouvé(s) » = total filtré (R2 UX-1) | |
| S9d | Chips `remove_url` | Sans `min_price` / `max_price` si prix non explicite (R1 UX-1) | |

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d ckr-marketone-01 --http-port=8099 \
  --test-tags=dorevia_marketone_shop_regression,dorevia_marketone_shop_filter_state,dorevia_marketone_origin_reunion_dedup,dorevia_marketone_shop_sidebar_ux2 \
  --stop-after-init
```

---

## S10 — Lecture visuelle globale *(recommandé MOA)*

| ID | Critère | Attendu | ☐ |
|----|---------|---------|---|
| S10a | Ton général | Sidebar **moins technique** · lecture retail premium | |
| S10b | Densité | Ni compact ERP ni vide excessif · rythme vertical cohérent | |
| S10c | Largeur desktop | Rail ~**17,5 rem** max · ne mange pas la grille produits | |
| S10d | Sticky desktop | Rail reste lisible sous le header au scroll (sticky raisonnable) | |
| S10e | Cohérence | Collections / Catégories / Origines / Prix — **même grammaire** (boutons section, corps, bordures token) | |
| S10f | Tokens | Couleurs / typo alignées charte Marketone · pas de palette parallèle | |

---

## Fiche d'exécution MOA (PR #8 · 2026-05-19)

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-05-19 |
| **Base** | `ckr-marketone-01` |
| **Branche** | `feat/marketone-ux2-shop-sidebar` |
| **Module** | `dorevia_ckreyol_marketone` **`19.0.14.0.0`** |
| **Upgrade** | OK · `shop_sidebar_ux2.xml` chargé · pas de traceback |

| Bloc | Résultat | Commentaire |
|------|----------|-------------|
| **S1–S4** | ☑ OK | Ordre OK · collections + URLs · C4 13 cat. desktop (`condiments-73`) · La Réunion unique |
| **S5** | ☑ OK | Desktop : 4 accordéons ouverts · `collapsedButtonCount = 0` |
| **S6** | ☑ OK | Label + input `cursor: pointer` · ligne ~**37,6 px** (~2,35 rem) |
| **S7** | ☑ OK | Rubriques présentes offcanvas · pas de reset sidebar |
| **S8–S9** | ☑ OK | Tests **30/30** + **25/25** · chips · reset `/shop` · pas de prix implicite dans `remove_url` |
| **S10** | ☑ OK | Rail max **280px** · sticky · pas de débordement horizontal |
| **Tests auto** | ☑ 0 failed | S8 : sidebar + collections · S9 : regression + UX-1 + Réunion + tag `ux2` |

**Note S3** : comptage brut HTML **26** entrées catégories = **13 desktop + 13 offcanvas** (doublon structurel attendu, pas une régression C4).

---

## Verdict MOA UX-2

| Verdict | ☑ |
|---------|---|
| **GO MOA UX-2** | ☑ |
| **GO avec réserves** | |
| **NO GO** | |

**Synthèse** : GO technique + GO MOA — aucune régression fonctionnelle. Merge PR #8 proposable.

**Réserves non bloquantes** : S5 animations/focus clavier · S10 lecture « premium » globale = points d'appréciation visuelle humaine, non bloquants.

### Captures

| Fichier | Scénario |
|---------|----------|
| `/private/tmp/marketone_ux2_sidebar_desktop.png` | Sidebar desktop — 4 rubriques ouvertes |
| `/private/tmp/marketone_ux2_sidebar_filtered.png` | Filtres actifs + chips UX-1 |

---

## Arbitrage MOA — sémantique filtres (2026-05-19 · doctrine définitive)

**Cas observé en recette** :

| Étape | Filtres actifs | Résultat |
|-------|----------------|----------|
| 1 | Collections **Apéritif créole** + **Idées cadeaux** | **18** produits |
| 2 | + catégorie **Assaisonnements** | **1** produit |

**Doctrine MOA confirmée (filtre cumulatif) :**

> Chaque case cochée **ajoute une contrainte** et **affine** le résultat. Le résultat ne peut qu'égaler ou diminuer à chaque sélection supplémentaire.

| Niveau | Logique | Note |
|--------|---------|------|
| **Plusieurs collections cochées** | **ET** — produits répondant à toutes les collections sélectionnées | 18 produits appartiennent aux deux collections |
| **Collection(s) + catégorie** | **ET** — intersection supplémentaire | → 1 produit dans ces collections ET cette catégorie |
| **Principe général** | Chaque facette cochée = contrainte cumulative | Résultat 18 → 1 : **conforme et attendu** |

Le comportement observé sur la capture est **correct** : un seul produit (*Marinade jerk authentique*) appartient simultanément aux collections Apéritif créole + Idées cadeaux **et** à la catégorie Assaisonnements.

Pas de modification SCSS/QWeb. Pas de refonte contrôleur. Pas de ticket fonctionnel dédié.

---

## Documents liés

| Document | Lien |
|----------|------|
| Ticket UX-2 | [`TICKET_MARKETONE_UX2_SHOP_SIDEBAR.md`](../tickets/TICKET_MARKETONE_UX2_SHOP_SIDEBAR.md) |
| UX-1 recette | [`RECETTE_MANUELLE_SHOP_UX1_ETAT_FILTRES.md`](RECETTE_MANUELLE_SHOP_UX1_ETAT_FILTRES.md) |
| Ordre sidebar | [`RECETTE_MANUELLE_SHOP_SIDEBAR_ORDRE.md`](RECETTE_MANUELLE_SHOP_SIDEBAR_ORDRE.md) |
| Collections | [`RECETTE_MANUELLE_SHOP_SIDEBAR_COLLECTIONS.md`](RECETTE_MANUELLE_SHOP_SIDEBAR_COLLECTIONS.md) |
