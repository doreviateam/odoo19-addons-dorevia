# TICKET — UX-2 — Sidebar `/shop` (confort, densité, zones cliquables)

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_UX2_SHOP_SIDEBAR` |
| **Type** | **UX** — présentation sidebar filtres · SCSS (+ QWeb classes minimales si besoin) |
| **Statut** | **À valider MOA** (ticket seul — pas de code avant GO ticket) |
| **Version cible** | **`19.0.14.0.0`** |
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079/shop |
| **Branche suggérée** | `feat/marketone-ux2-shop-sidebar` |
| **Prérequis** | `main` **≥ `19.0.13.1.0`** (UX-1 + dédup La Réunion) · recettes sidebar **GO** (`19.0.12.x`) |

---

## Contexte

Les fondations sidebar sont **GO MOA** :

| Lot | Statut |
|-----|--------|
| Ordre rubriques (Collections → Catégories → Origines → Prix) | GO `19.0.12.1.0` |
| Collections Lot B · Catégories C4 | GO |
| UX-1 état utilisateur (chips, compteur, reset barre) | GO `19.0.13.0.7` |
| Données Origines (La Réunion unique) | GO `19.0.13.1.0` |

**Problème restant** : la sidebar est **fonctionnelle** mais encore **trop « technique »** — densité, respiration, accordéons et zones cliquables perfectibles pour une lecture retail premium.

**Doctrine** (alignée UX-1) :

- Présentation uniquement sous **`.marketone-shop`** ;
- Tokens `_tokens_*.scss` — pas de palette parallèle ;
- **Pas** de changement de logique filtre (URLs, AND, C4, `keep()`, contrôleur facettes).

**Référence interne** (inspiration, pas copie) : styles sidebar du module `dorevia_ckreyol_marketplace` (`_shop.scss` § `#products_grid_before`) — à **traduire** en tokens Marketone.

---

## Objectif MOA

Améliorer le **confort de lecture** et l’**ergonomie** de la sidebar filtres desktop + offcanvas mobile :

1. **Accordéons** — en-têtes lisibles, états ouvert/fermé clairs, chevrons discrets ;
2. **Espacements** — rythme vertical cohérent entre rubriques et options ;
3. **Densité** — ni trop serré (fatigue), ni trop aéré (perte de scan) ;
4. **Zones cliquables** — labels, cases et boutons de section avec surface tactile confortable (desktop + mobile) ;
5. **Cohérence** — Collections, Catégories, Origines, Prix sur la même grammaire visuelle.

**Réserve UX-1 reportée ici (optionnelle, si MOA OK)** : renforcer légèrement le lien **« Effacer les filtres »** de la barre UX-1 (poids / contraste), **sans** réintroduire un reset sidebar.

---

## Périmètre

### In

| Zone | Détail |
|------|--------|
| **Desktop** | `#products_grid_before` · `.o_wsale_products_grid_before_rail` |
| **Rubriques** | Collections (`marketone-shop-collections-accordion`) · Catégories (`marketone-shop-categories-accordion`) · Origines (`products_attributes_filters`) · Prix (`#o_wsale_price_range_option`) |
| **Offcanvas** | `#o_wsale_offcanvas` — **même** grammaire visuelle que desktop |
| **SCSS** | Nouveau partial dédié ex. `_shop_sidebar.scss` · import manifest |
| **QWeb** | Classes BEM **uniquement** si le ciblage SCSS natif est fragile (éviter `!important` massif) |
| **Tests** | Suites sidebar + régression UX-1 **inchangées** (pas de régression fonctionnelle) |
| **Recette** | [`RECETTE_MANUELLE_SHOP_UX2_SIDEBAR.md`](../recette/RECETTE_MANUELLE_SHOP_UX2_SIDEBAR.md) |

### Hors périmètre

| Hors scope | Lot / note |
|------------|------------|
| Logique filtres · `remove_url` · C4 · ordre rubriques | Gel fonctionnel |
| UX-1 chips / compteur / placement barre | Gel `19.0.13.0.7` |
| UX-3 images produits | UX-3 |
| Savoirs · `shop_ppg` | — |
| Paramétrage BO séquence sidebar | ADR-030 (évolution) |
| Module `dorevia_ckreyol_marketplace` | Hors dépôt Marketone (référence seule) |
| Réintroduction « Clear Filters » sidebar | Interdit (UX-1) |

---

## Cible visuelle (indications MOA)

| Élément | Attendu |
|---------|---------|
| **Rail sidebar** | Fond transparent / fond page · pas de colonne blanche « bloc » · largeur max ~`17.5rem` desktop |
| **En-tête section** | Bande légère crème · bordure basse discrète · typo heading sans |
| **Corps section** | Padding homogène · filets entre rubriques |
| **Options (checkbox)** | `form-check` espacés · label cliquable sur toute la ligne · état coché lisible |
| **Accordéon** | Chevron aligné · focus visible · hover terracotta doux |
| **Prix** | Slider et bornes min/max alignés avec le reste |
| **Sticky** (desktop) | Rail sticky raisonnable sous le header (si MOA Q2) |

---

## Implémentation proposée (après GO ticket)

| Étape | Livrable |
|-------|----------|
| **E1** | `_shop_sidebar.scss` — scope `.marketone-shop #products_grid_before` + offcanvas |
| **E2** | Ajustements QWeb mineurs (classes `marketone-sidebar__*` sur accordéons si nécessaire) |
| **E3** | Recette manuelle + capture avant/après |
| **E4** | Vérification tests auto existants |

**Fichiers touchés (estimation)** :

- `static/src/scss/_shop_sidebar.scss` (nouveau)
- `__manifest__.py` (import assets + version)
- `views/pages/shop_sidebar_*.xml` (optionnel, classes)
- `docs/recette/RECETTE_MANUELLE_SHOP_UX2_SIDEBAR.md`

**Pas de modification** : `controllers/website_sale.py` (sauf bug bloquant constaté en recette).

---

## Critères GO MOA

| # | Critère | Méthode |
|---|---------|---------|
| G1 | Sidebar desktop : **4 rubriques** lisibles, ordre inchangé | Recette S1–S4 |
| G2 | Accordéons : ouverture/fermeture **fluide** · chevron et focus visibles | Recette S5 |
| G3 | Zones cliquables : clic sur **libellé** = clic case (Collections, Catégories, Origines) | Recette S6 |
| G4 | Densité perçue **premium** (ni compact ERP, ni vide) | Validation visuelle MOA |
| G5 | Offcanvas mobile : **même grammaire** que desktop | Recette S7 |
| G6 | **Non-régression** C4 (13 catégories visibles avec 1 filtre) | Recette S8 + tests |
| G7 | **Non-régression** UX-1 (chips, reset, compteur) | Recette S9 + tests |
| G8 | Pas de warning `@class` nouveau à l’upgrade | Log upgrade |

---

## Tests auto (cible — non-régression)

```bash
odoo-bin -d ckr-marketone-01 --test-tags=dorevia_marketone_shop_sidebar,dorevia_marketone_shop_sidebar_collections --stop-after-init
odoo-bin -d ckr-marketone-01 --test-tags=dorevia_marketone_shop_regression,dorevia_marketone_shop_filter_state --stop-after-init
odoo-bin -d ckr-marketone-01 --test-tags=dorevia_marketone_origin_reunion_dedup --stop-after-init
```

Tag dédié UX-2 (optionnel post-implémentation) : `dorevia_marketone_shop_sidebar_ux2` — smoke HTML classes présentes.

---

## Questions ouvertes MOA (avant GO implémentation)

| # | Question | Proposition par défaut |
|---|----------|------------------------|
| Q1 | Accordéons **ouverts** par défaut sur desktop ? | Oui pour les 4 rubriques (comme Collections aujourd’hui) |
| Q2 | Rail sidebar **sticky** desktop ? | Oui, `top` ~`1.2rem` sous le header |
| Q3 | Largeur max sidebar | `17.5rem` aligné maquette marketplace |
| Q4 | Renfort visuel lien reset UX-1 | Oui, discret (semi-bold déjà · + contraste hover) |
| Q5 | Kit graphique Carole dédié UX-2 | Non fourni — s’appuyer sur tokens Marketone + capture MOA |

---

## Enchaînement produit

| Ordre | Lot |
|-------|-----|
| 1 | **Ce ticket** — sidebar confort |
| 2 | **UX-3** — images produits / cartes grille |

---

## Références

| Document | Lien |
|----------|------|
| Recette ordre sidebar | [`RECETTE_MANUELLE_SHOP_SIDEBAR_ORDRE.md`](../recette/RECETTE_MANUELLE_SHOP_SIDEBAR_ORDRE.md) |
| Recette collections | [`RECETTE_MANUELLE_SHOP_SIDEBAR_COLLECTIONS.md`](../recette/RECETTE_MANUELLE_SHOP_SIDEBAR_COLLECTIONS.md) |
| Recette C4 | [`RECETTE_MANUELLE_SHOP_SIDEBAR_CATEGORIES_C4_MULTI.md`](../recette/RECETTE_MANUELLE_SHOP_SIDEBAR_CATEGORIES_C4_MULTI.md) |
| UX-1 (gel fonctionnel) | [`TICKET_MARKETONE_UX1_SHOP_ETAT_UTILISATEUR.md`](TICKET_MARKETONE_UX1_SHOP_ETAT_UTILISATEUR.md) |
| SCSS actuel sidebar (minimal) | [`static/src/scss/_shop.scss`](../../static/src/scss/_shop.scss) § `#products_grid_before` |
| Tokens | [`static/src/scss/_tokens_*.scss`](../../static/src/scss/) |

---

## Verdict ticket

| Date | Verdict | Commentaire |
|------|---------|-------------|
| 2026-05-19 | **Brouillon — attente GO MOA ticket** | Ticket rédigé après clôture dédup Réunion · base catalogue assainie |
