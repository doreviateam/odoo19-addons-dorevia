# Note recette — Lot H1.2 · Header CK 3 niveaux

| Champ | Valeur |
|---|---|
| **Lot** | H1.2 — Réorganisation header desktop CK |
| **Branche** | `feat/ck-h1-2-header-three-levels` |
| **Module** | `dorevia_ck_theme` **19.0.1.39.0** |
| **Instance** | `dorevia_ck_marketone_01` — http://localhost:18079 |

---

## Organisation en 3 niveaux

| Niveau | Rôle | Implémentation |
|---|---|---|
| **0** | Promesse / réassurance | Bandeau terracotta existant (`ck-header-service-bar`) — inchangé |
| **1** | Identité + achat | `ck-header__identity-row` : logo · recherche élargie · compte · panier |
| **2** | Exploration catalogue + éditoriale | `ck-header__nav-row` : `#top_menu` pleine largeur, centrée |

**Choix hiérarchie parent/enfants (dropdown L2)** : le parent reste cliquable dans la barre niveau 2 ; le dropdown affiche uniquement les enfants L2 (sans lien « Toute {racine} » — règle Nav-Shop V2.1 conservée).

---

## Fichiers modifiés

| Fichier | Nature |
|---|---|
| `dorevia_ck_theme/views/website_header_h1_2.xml` | QWeb — structure 3 niveaux desktop |
| `dorevia_ck_theme/views/website_header.xml` | Attribut `data-extra-items-toggle-aria-label` pour overflow 7+ |
| `dorevia_ck_theme/static/src/scss/website_header.scss` | Layout 3 niveaux · dropdown CK · recherche élargie |
| `dorevia_ck_theme/tests/test_ck_phase10_header_compose.py` | Test structure H1.2 |
| `dorevia_ck_theme/__manifest__.py` | Bump **19.0.1.39.0** |

Héritage V2.1 Nav-Shop (branche parente) : suppression « Toute {racine} », split-link L2, styles dropdown — **non régressés**.

---

## Résultats recette (1280 px · seed)

| Critère | Verdict |
|---|---|
| 3 niveaux visibles | ✅ |
| Recherche lisible (niveau 1) | ✅ |
| 5 racines catalogue + `Tous nos produits` + `Découvrir` (**7 entrées** au total) sur une ligne | ✅ |
| Bouton `+` overflow absent | ✅ |
| Mobile 390 px non régressé | ✅ |
| Tests `dorevia_ck_marketone_nav_sync` + `dorevia_ck_theme_phase10` | **29/29 ✅** |

Captures : `docs/design/maquette_01.2/captures/recette_h1_2_header/`

---

## Libellés catalogue (§10 ticket)

| Entrée header | Source |
|---|---|
| `Épicerie`, `Boissons`, `Maison & bien-être`, `Artisanat & Culture`, `Coups de cœur` | `product.public.category` niveau 1 (libellé BO) |
| `Tous nos produits` | Entrée fixe Nav-Shop → `/shop` |
| `Découvrir` | Entrée éditoriale fixe (mega menu) |

`Coups de cœur` : catégorie catalogue seed dédiée (ribbon + curation home) — présence justifiée par le périmètre contenu MOA.

---

## Cas 7+ racines

Non observé sur seed actuel (**5 racines** catalogue visibles à 1280 px · 7 entrées nav au total, sans overflow). Si le catalogue dépasse 7 racines, le libellé overflow autorisé est **« Plus de catégories »** (jamais icône `+` seule) — arbitrage MOA requis pour stratégie durable.
