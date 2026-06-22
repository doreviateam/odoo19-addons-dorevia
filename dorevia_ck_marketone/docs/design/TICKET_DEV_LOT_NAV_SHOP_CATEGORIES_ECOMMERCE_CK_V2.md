# Ticket Dev — Lot Nav-Shop · Navigation boutique CK pilotée par l’arborescence e-commerce Odoo · V2

| Champ | Valeur |
| --- | --- |
| **Projet** | `dorevia_ck_marketone` · C-Kréyòl / CK Marketone |
| **Lot** | **Nav-Shop** — navigation catalogue dynamique (post Nav-1 + H1) |
| **Modules** | `dorevia_ck_marketone_content` (principal · `nav_sync.py`) · `dorevia_ck_theme` (SCSS / QWeb si besoin) |
| **Type** | Navigation / header e-commerce · lot technique recettable |
| **Priorité** | Haute |
| **Statut** | **GO MOA exécution** — décision §23 · retours Carole intégrés V2 |
| **Instance recette** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **Baseline mergée** | Nav-1 PR **#78** · H1 PR **#79** sur `main` |
| **Versions baseline** | `dorevia_ck_marketone_content` **19.0.1.26.1** · `dorevia_ck_theme` **19.0.1.38.0** |
| **Documents source** | [`note_06.md`](../cadrage/note_06.md) · brief Carole V2 · [`TICKET_DEV_LOT_NAV1_NAVIGATION_CK_V2.md`](./TICKET_DEV_LOT_NAV1_NAVIGATION_CK_V2.md) · [`TICKET_DEV_LOT_H1_HEADER_CK_V2_1.md`](./TICKET_DEV_LOT_H1_HEADER_CK_V2_1.md) |

```text
Objectif : remplacer la liste figée NAV_UNIVERSE_SPECS par une navigation boutique
construite depuis product.public.category (2 niveaux max dans le header).

Découvrir reste éditorial · H1 (bandeau, C-Kréyòl, recherche, chrome mobile) inchangé.
```

---

## 0. Synthèse V2 · amendements post-livraison Nav-1 / H1

### Règle centrale MOA

```text
Le header CK doit refléter l’arborescence des catégories e-commerce Odoo avec 2 niveaux visibles maximum :
- niveau 1 → entrées principales du menu ;
- niveau 2 → sous-menus / accordéon mobile ;
- niveau 3+ → hors header (page catégorie, shop, filtres).
```

### Apports V2 (retours Carole + alignement projet)

| Apport | Détail |
| --- | --- |
| Source de vérité catalogue | `product.public.category` · parenté · séquence Odoo |
| Fin de la liste figée | Remplacement de `NAV_UNIVERSE_SPECS` dans `nav_sync.py` |
| Niveau 2 explicite | Dropdown desktop · enfants sous parent mobile |
| Densité desktop | Cible 4–6 racines · cas 7+ documenté / arbitrage MOA |
| Interaction niveau 2 | Hover + focus clavier desktop · clic mobile |
| Breadcrumb | Écart toléré `Tous nos produits` / `Tous les produits` |
| Contraste | Non-régression tokens Nav-1 / H1 (`$ck-primary-text` / `#bf360c`) |
| Baseline technique | Conserver sync `website.menu` + classes `ck-nav-*` Nav-1 |

### Diagnostic actuel (instance seed · post Nav-1)

Menu desktop visible aujourd’hui :

```text
Tous nos produits · Épicerie · Soin & Bien-être · Découvrir
```

`Boissons` est déclarée dans `NAV_UNIVERSE_SPECS` mais **absente** si la catégorie BO n’existe pas ou n’a pas de produit publié — comportement Nav-1 voulu, mais **toute nouvelle catégorie racine** exige aujourd’hui une modification code (`category_names`, `menu_label`, `sequence`).

**Ce ticket lève cette dette** : une catégorie e-commerce réelle, éligible et structurée dans Odoo remonte sans patch thème.

---

## 1. Contexte

### 1.1 Problème

Le header CK ne doit pas dépendre d’une table de correspondance manuelle pour les univers boutique.

Une nouvelle catégorie racine (ex. `Boissons`, `Packs & découvertes`) doit apparaître dans la navigation quand le catalogue Odoo le permet — **sans** ajout dans `NAV_UNIVERSE_SPECS`.

### 1.2 Ce qui reste figé (hors périmètre de ce ticket)

| Zone | Statut |
| --- | --- |
| Bandeau Strate 0 · logo C-Kréyòl · recherche · panier | H1 — **ne pas modifier** |
| Entrée `Tous nos produits` → `/shop` | Fixe |
| Entrée `Découvrir` + mega éditorial | Nav-1 — **ne pas modifier le contenu** |
| Professionnels top-level | **Interdit** — reste sous Découvrir |
| Home S4 · fiche produit · checkout · shop layout | Hors lot |

### 1.3 Architecture retenue (continuité Nav-1)

Nav-1 a validé la synchronisation via `nav_sync.py` → `website.menu` + classes `ck-nav-desktop-universe` / `ck-nav-mobile-univers`.

**Décision Dev pour Nav-Shop** : conserver ce pattern (pas de menu HTML parallèle non maintenable), en **refactorisant** la génération des entrées commerce depuis l’arbre `product.public.category`.

> Le ticket source évoquait d’éviter la duplication manuelle dans `website.menu` — ici la sync reste **automatisée** par Python, pas saisie BO manuelle.

---

## 2. Périmètre IN (Lot Nav-Shop)

| # | Livrable |
| ---: | --- |
| NS-1 | Refactor `nav_sync.py` : lecture dynamique des catégories racine (niveau 1) |
| NS-2 | Génération des sous-menus niveau 2 (enfants directs) par entrée niveau 1 |
| NS-3 | Règle profondeur : niveau 3+ **jamais** dans le header |
| NS-4 | Ordre menu = `sequence` Odoo des `product.public.category` |
| NS-5 | Règle de visibilité catalogue (§6) — héritage Nav-1 + alignement MOA |
| NS-6 | Mobile : groupe **Nos univers** alimenté par le même arbre (niveau 1 + 2) |
| NS-7 | Desktop : dropdown niveau 2 si enfants éligibles |
| NS-8 | Règle densité desktop 4–6 racines · cas 7+ documenté (§8 bis) |
| NS-9 | Non-régression Découvrir · H1 · contraste · sticky |
| NS-10 | Tests `dorevia_ck_marketone_nav_sync` + `dorevia_ck_theme_phase10` mis à jour |
| NS-11 | Recette QA desktop **1280** + mobile **390** + captures densité |
| NS-12 | Note courte règle de remontée + mapping BO pour MOE |
| NS-13 | Bump version `dorevia_ck_marketone_content` (minimum) |

---

## 3. Hors périmètre (interdit)

| Zone | Raison |
| --- | --- |
| Contenu mega **Découvrir** · Nav-2 éditorial | Ticket Nav-2 / H2 |
| Hub `/producteurs` | Lot H2 |
| Refonte graphique header H1 | Interdit |
| Home · fiche produit · shop · checkout · cards · prix | Tickets distincts |
| Blog · forum · communauté | Hors V1 |
| Création massive de catégories catalogue (hors seed test minimal) | MOE catalogue |
| SEO pages catégories | Hors lot |
| Harmonisation globale breadcrumb | Ticket séparé si besoin |
| Stratégie regroupement 7+ racines sans arbitrage MOA | Interdit |

---

## 4. Source de vérité technique

### Modèle Odoo 19 CE

```text
product.public.category
```

Champs / comportements à exploiter :

| Élément | Usage Nav-Shop |
| --- | --- |
| `parent_id` | Niveau 1 = racine · niveau 2 = enfant direct |
| `sequence` | Ordre header |
| `name` | Libellé menu (= libellé catégorie BO, pas d’alias figé) |
| URL | `_slug` / route standard `/shop/category/<slug>` |
| Site | Filtrage `website_id` si applicable |

### Ce qui disparaît

```python
NAV_UNIVERSE_SPECS = (
    {'menu_label': 'Épicerie', 'category_names': (...), 'sequence': 20},
    ...
)
```

Remplacé par une fonction du type `_iter_nav_shop_categories(env, website)` parcourant l’arbre réel.

`get_nav_category_mapping()` doit refléter le nouvel algorithme (recette / doc MOE).

---

## 5. Règle de profondeur

### Niveau 0 — Entrée globale (fixe)

```text
Tous nos produits  →  /shop
```

### Niveau 1 — Entrées principales desktop

Catégories `product.public.category` **sans parent** (racines), éligibles §6.

Exemple cible :

```text
Tous nos produits · Épicerie · Boissons · Soin & Bien-être · Artisanat & culture · Découvrir
```

### Niveau 2 — Sous-menu

Enfants **directs** d’une racine — **pas** d’entrées principales séparées.

Exemple `Boissons` :

```text
Boissons
├── Jus de fruits
├── Alcools
└── Liqueurs
```

Implémentation attendue : `website.menu` enfants sous le menu parent `Boissons`, ou mécanisme Odoo dropdown natif équivalent.

### Niveau 3+

```text
Boissons → Jus de fruits → Jus tropicaux
```

`Jus tropicaux` **n’apparaît pas** dans le header. Accessible via page catégorie / shop.

---

## 6. Règle d’affichage / visibilité

### Candidat navigation

Une catégorie est candidate si :

```text
niveau 1 ou 2 dans l’arborescence
+ rattachée au site courant (si champ applicable)
+ au moins 1 produit publié dans son sous-arbre (règle Nav-1 conservée)
```

**Alignement MOA** : le ticket source V2 mentionnait « visible côté site Odoo ». En pratique CK conserve la **règle Nav-1** (`_category_has_published_products`) pour éviter des entrées menu vers des catégories vides — comportement déjà validé en recette Nav-1.

Si le MOA souhaite afficher une catégorie sans produit publié, cela nécessite un **amendement explicite** hors implémentation par défaut.

### Pas de gouvernance parallèle

Pas de seconde table « menu éditorial boutique ». Le MOE pilote via le catalogue Odoo.

---

## 7. Règle desktop (§8 + §8 bis)

### Structure cible

```text
Tous nos produits · [catégories niveau 1…] · Découvrir
```

### Densité

| Cas | Attendu |
| --- | --- |
| **4–6 racines** | Header lisible à 1280 px · pas de chevauchement logo / recherche H1 / compte / panier |
| **7–8 racines** | Rendu sans casse **ou** documentation + demande arbitrage MOA |

**Solutions autorisées** (7+) en attente MOA :

- deux lignes nav si rendu propre ;
- regroupement temporaire documenté ;
- limitation technique documentée sans perte d’accès `/shop`.

**Interdit** sans arbitrage MOA :

- masquer silencieusement des catégories éligibles ;
- tronquer des libellés sans indication ;
- casser le chrome H1.

### Interaction niveau 2 (§9)

```text
Desktop : survol + focus clavier (composant Odoo / Bootstrap existant).
Mobile  : clic / tap dans le drawer.
```

Pas de refonte JS lourde. Signaler en recette si l’accessibilité native est insuffisante.

---

## 8. Règle mobile (§10)

Structure cible (libellé groupe = **Nos univers**, conservé Nav-1) :

```text
Tous nos produits

Nos univers
  Épicerie
    Biscuits
    Confitures
  Boissons
    Jus de fruits
    Alcools
  Soin & Bien-être
    …

Découvrir
```

Même source que desktop. Niveau 3+ hors navigation principale.

**Classes CSS** : conserver / étendre `ck-nav-mobile-univers`, `ck-nav-mobile-universe-child`, `ck-nav-desktop-universe` — **ne pas supprimer** le filtrage CSS Nav-1 sans recette de non-régression.

---

## 9. Découvrir — statut inchangé (§11)

```text
Découvrir = entrée éditoriale · hors product.public.category
```

Ne pas modifier :

- `DECOUVRIR_LINK_SPECS` ;
- ordre mega (Pro · Recettes · Professionnels · Contact…) ;
- contenu `ck-nav-decouvrir-links`.

Non-régression obligatoire : tests phase10 mega + nav_sync Découvrir.

---

## 10. Cas concret — Boissons (§13)

| Étape | Attendu |
| --- | --- |
| Catégorie racine `Boissons` en BO | Oui |
| ≥ 1 produit publié (ex. `Jus Mont-Pelé`) | Oui |
| Menu desktop | `… · Boissons · …` entre racines selon `sequence` |
| Absence de `Boissons` alors que éligible | **Défaut bloquant** |

---

## 11. Breadcrumb / libellés (§14)

| Zone | Libellé |
| --- | --- |
| Header | `Tous nos produits` |
| Breadcrumb Odoo natif | `Tous les produits` (toléré) |

Documenter l’écart en recette · pas de refonte breadcrumb dans ce lot.

---

## 12. Spécifications techniques

### Fichiers probables

| Composant | Emplacement |
| --- | --- |
| Algorithme navigation catalogue | `dorevia_ck_marketone_content/nav_sync.py` |
| Champ CSS menu (existant) | `models/website_menu.py` |
| Styles dropdown / densité | `dorevia_ck_theme/static/src/scss/website_header.scss` |
| QWeb nav (si besoin niveau 2) | `dorevia_ck_theme/views/website_nav_ck_v1.xml` |
| Tests sync | `dorevia_ck_marketone_content/tests/test_ck_nav_sync.py` |
| Tests header | `dorevia_ck_theme/tests/test_ck_phase10_header_compose.py` |

### Principes

- Refactor ciblé `nav_sync.py` — **autorisé et requis** dans ce lot (contrairement au verrou H1).
- Pas de slugs ni libellés codés en dur pour les catégories.
- Conserver `bootstrap_ck_navigation()` comme point d’entrée recette / tests.
- Bump version content à chaque livraison.

### À éviter

- Duplication manuelle des catégories dans le BO `website.menu` ;
- Mélange catégories e-commerce et liens Découvrir ;
- Casser les tests Nav-1 non liés au catalogue (Professionnels top-level, mega sans commerce, etc.).

---

## 13. Non-régression H1 + Nav-1 (§16 + §16 bis)

Préserver sans régression :

| Élément | Référence |
| --- | --- |
| Bandeau Strate 0 | H1 |
| Logo **C-Kréyòl** · recherche produits · panier | H1 |
| Chrome mobile Menu · Recherche · Panier · compte drawer | H1 |
| Sticky header | H1 |
| Contraste liens nav / mega / sous-menus | Nav-1 B2 · `$ck-primary-text` |
| Professionnels absent top-level | Nav-1 |
| Mega Découvrir sans doublons commerce | Nav-1 |

Adaptations CSS **strictement nécessaires** pour dropdown niveau 2 et densité.

---

## 14. Données de test (§18)

Arborescence minimale recette :

```text
Épicerie
  Biscuits · Confitures · Épices
Boissons
  Jus de fruits · Alcools · Liqueurs
Soin & Bien-être
  Savons · Huiles
```

Produit témoin : `Jus Mont-Pelé` dans `Boissons`.

Pour densité : ajouter temporairement `Artisanat & culture`, `Packs & découvertes`, `Maison créole` (6–8 racines).

Seed module ou script recette documenté — pas de dépendance à la saisie manuelle non rejouable.

---

## 15. Recette fonctionnelle (§19)

| # | Scénario | Viewport |
| ---: | --- | --- |
| R1 | Remontée `Boissons` niveau 1 | Desktop 1280 |
| R2 | Sous-catégories niveau 2 sous `Boissons` uniquement | Desktop |
| R3 | Niveau 3 absent du header | Desktop |
| R4 | Ordre suit `sequence` BO | Desktop |
| R5 | Mobile : niveau 1 + 2 sous Nos univers | 390 |
| R6 | Non-régression H1 (bandeau, logo, recherche, panier) | 1280 + 390 |
| R7 | Non-régression Découvrir / mega | Desktop |
| R8 | Densité 6 racines | 1280 |
| R9 | Densité 7–8 racines · comportement documenté | 1280 |
| R10 | Contraste sous-menu niveau 2 | Desktop + mobile |
| R11 | Breadcrumb produit Boissons · écart libellé documenté | Desktop |

Livrable recette : `RECETTE_QA_LOT_NAV_SHOP_CATEGORIES_ECOMMERCE_CK_V2.md` (à créer en fin de lot).

---

## 16. Tests automatisés (§20)

| Tag | Attendu |
| --- | --- |
| `dorevia_ck_marketone_nav_sync` | Refactor + cas niveau 1/2/3 · ordre sequence · Boissons |
| `dorevia_ck_theme_phase10` | Non-régression H1 + Nav-1 · présence catégories dynamiques |

Cas minimum :

- racine éligible visible ;
- enfants niveau 2 sous parent ;
- niveau 3 absent du HTML `#top_menu` ;
- `Tous nos produits` + `Découvrir` présents ;
- Professionnels absent top-level ;
- ordre cohérent avec `sequence`.

Commande recette :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 --test-enable --stop-after-init --http-port=8078 \
  --test-tags dorevia_ck_marketone_nav_sync,dorevia_ck_theme_phase10
```

---

## 17. Livrables fin de lot (§21)

1. Code Nav-Shop (content + theme si besoin).
2. `nav_sync.py` sans `NAV_UNIVERSE_SPECS` figé.
3. Note règle de remontée + comportement densité 7+.
4. Recette QA + captures `captures/recette_nav_shop_v2/`.
5. Scripts Playwright recette (optionnel · même pattern Nav-1 / H1).
6. Bump `dorevia_ck_marketone_content` (+ theme si SCSS).
7. PV QA `NOTE_QA_LOT_NAV_SHOP_…md` avant merge.

---

## 18. Critères d’acceptation MOA (§22)

| # | Critère | Attendu |
| ---: | --- | --- |
| C1 | Source de vérité | `product.public.category` · plus de liste figée thème |
| C2 | Boissons | Remonte si catégorie + produit publié |
| C3 | Niveau 2 | Sous-menu parent uniquement |
| C4 | Niveau 3+ | Hors header |
| C5 | Ordre | `sequence` Odoo |
| C6 | Mobile | Cohérent desktop · Nos univers |
| C7 | Fixes | `Tous nos produits` · `Découvrir` intacts |
| C8 | Découvrir | Non régressé |
| C9 | H1 | Chrome header non dégradé |
| C10 | Densité | 6 racines testées · 7+ documenté |
| C11 | Contraste | Sous-menus conformes |
| C12 | Tests | nav_sync + phase10 verts |

---

## 19. Décision MOA (§23)

```text
GO pour faire de l’arborescence des catégories e-commerce Odoo la source de vérité
de la navigation boutique CK.

2 niveaux max dans le header · Tous nos produits et Découvrir hors catalogue.
Découvrir reste éditorial et ne doit pas être régressé.
À partir de 7 catégories racines, arbitrage MOA avant regroupement durable.
```

---

## 20. Séquencement projet

```text
Nav-1  ✅ mergé (#78) — structure navigation + Découvrir
H1     ✅ mergé (#79) — chrome header
Nav-Shop → CE TICKET — catalogue dynamique
H2     → hub /producteurs (après ou en parallèle selon MOA)
Nav-2  → enrichissement éditorial Découvrir
H1 bis → UX recherche vide
```

**Branche suggérée** : `feat/ck-nav-shop-categories-v2`

---

## 21. Phrase de synthèse (§24)

```text
Le header CK doit refléter l’arborescence product.public.category avec 2 niveaux visibles
maximum, en remplacement de NAV_UNIVERSE_SPECS, tout en préservant Découvrir, le chrome
H1 et la lisibilité desktop à 1280 px.
```

---

*Ticket Dev Lot Nav-Shop · Navigation boutique e-commerce dynamique · V2 · amendé post Nav-1 / H1 · 2026-06-22.*
