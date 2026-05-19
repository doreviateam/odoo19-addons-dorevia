# Recette manuelle — Sidebar /shop — catégories principales

| Champ | Valeur |
|-------|--------|
| **Ticket** | [`TICKET_MARKETONE_SHOP_SIDEBAR_FILTRES_CATEGORIES`](../tickets/TICKET_MARKETONE_SHOP_SIDEBAR_FILTRES_CATEGORIES.md) |
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079/shop |
| **Version de référence** | **`19.0.10.8.0`** (sidebar + Effacer les filtres) |
| **Version précédente** | `19.0.10.7.0` (commit `1ced35e` — GO MOA signé) |
| **Statut recette** | **GO MOA** — `19.0.10.7.0` + repasse ciblée **`19.0.10.8.0`** signée (2026-05-19, `_108`) |

---

## Prérequis

| Élément | Détail |
|---------|--------|
| Ticket BO catégories | **Clôturé GO MOA** — [`RECETTE_MANUELLE_CATALOGUE_CATEGORIES.md`](RECETTE_MANUELLE_CATALOGUE_CATEGORIES.md) |
| Module | `dorevia_ckreyol_marketone` **≥ version cible** (voir en-tête) |
| Facette catégories | Query répétable `marketone_category=<slug>` (logique **OU**) |
| JS | `marketone_shop_sidebar.js` — catégories, attributs Origine, `data-url` prix |
| Données | 13 principales + 4 secondaires sur `ckr-marketone-01` |
| Tests auto | Tag `dorevia_marketone_shop_sidebar` — **13** tests, **0** failed (dont scénario **10**) |
| Navigateur | Hard refresh après upgrade (assets frontend) |

```bash
# Upgrade (obligatoire avant recette 19.0.10.8.0)
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf -d ckr-marketone-01 -u dorevia_ckreyol_marketone --stop-after-init

# Tests auto sidebar
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf -d ckr-marketone-01 --test-enable --stop-after-init --http-port=18084 --test-tags=dorevia_marketone_shop_sidebar
```

### Smoke (30 s — avant grille MOA)

| # | Contrôle | Attendu | OK |
|---|----------|---------|-----|
| S1 | `<body data-marketone-shop-sidebar-js="1">` | JS sidebar initialisé | ☑ |
| S2 | Cocher **Biscuits salés** | URL `?marketone_category=biscuits-sales-70` (ou slug équivalent) | ☑ |
| S3 | Avec catégorie active | Bouton **Effacer les filtres** visible (sidebar desktop) | ☑ |

---

## Règles fonctionnelles (référence MOA)

| Facette | Logique |
|---------|---------|
| **Catégories** (cases) | **OU** entre catégories cochées |
| **Origine** (attribut sidebar) | Lot 6.2 — `attribute_values` dans l’URL |
| **Combinaison** | Catégories **ET** Origine **ET** Prix = **AND** |
| **Conservation URL** | Changer une facette **ne supprime pas** les autres paramètres actifs |
| **Effacer les filtres** | Visible si au moins un filtre actif : `marketone_category`, `attribute_values`, prix, tags (standard Odoo) ; clic → catalogue global `/shop` |

**Exemple** : Biscuits salés + Épices + Martinique → (Biscuits salés **OU** Épices) **ET** Martinique.

---

## Grille de recette — par lot

Cocher **MOA** après validation. **Tech** = couverture tests auto (≠ GO MOA).

### Lot A — Présentation sidebar (`19.0.10.7.0` — déjà signé)

| # | Scénario | Action | Attendu | MOA | Tech |
|---|----------|--------|---------|-----|------|
| **1** | Ordre sidebar | `/shop` desktop | **Origine** → **Catégories** → **Fourchette de prix** | ☑ | ☑ |
| **2** | Bloc Catégories | Même | Accordéon ; **13 cases** ouvertes ; pas « Tous les produits » | ☑ | ☑ |
| **2b** | Accordéon | Clic en-tête **Catégories** | Pli / dépli ; chevron cohérent | ☑ | ☑ |
| **3** | Allowlist | Parcourir la liste | 13 principales ; **pas** les 4 secondaires | ☑ | ☑ |
| **5** | Filmstrip | Zone au-dessus grille | **Aucun** bandeau horizontal catégories | ☑ | ☑ |

### Lot B — Filtres catégories (`19.0.10.7.0` — déjà signé)

| # | Scénario | Action | Attendu | MOA | Tech |
|---|----------|--------|---------|-----|------|
| **4** | Mono | Cocher **Biscuits salés** | URL `marketone_category=…` ; grille cohérente ; case cochée | ☑ | ☑ |
| **4b** | Multi OR | **Biscuits salés** + **Épices** | 2× `marketone_category` ; 2 cases cochées | ☑ | ☑ |
| **4c** | Tout voir | Décocher toutes les catégories | `/shop` sans `marketone_category` | ☑ | ☑ |
| **10** | **Effacer les filtres** | **Biscuits salés** + **Biscuits sucrés** + **Épices** (sans Origine) | Bouton **Effacer les filtres** visible **au-dessus** d’Origine ; clic → `/shop` sans `marketone_category` ; cases décochées | ☑ | ☑ |

### Lot C — Combinaisons facettes (`19.0.10.7.0` — déjà signé)

| # | Scénario | Action | Attendu | MOA | Tech |
|---|----------|--------|---------|-----|------|
| **4d** | Catégories → Origine | **Biscuits salés** + **Épices** puis **Martinique** | Catégories restent cochées ; URL : 2× `marketone_category` + `attribute_values` | ☑ | ☑ |
| **4e** | Origine → Catégories | **Martinique** puis **Biscuits salés** | URL : `marketone_category` + `attribute_values=3-20` | ☑ | ☑ |
| **7** | Origine seule | **Martinique** sans catégorie | Grille filtrée ; pas de cases catégories parasites | ☑ | ☑ |
| **8** | Prix seul | Slider prix seul | `min_price` / `max_price` dans l’URL | ☑ | ☑ |
| **8b** | Prix après facettes | État **4d** puis slider prix | URL conserve catégories + origine + prix | ☑ | ☑ |
| **10b** | Effacer avec combinaison | **Biscuits salés** + **Martinique** puis **Effacer les filtres** | Retour `/shop` sans `marketone_category` ni `attribute_values` | ☑ | — |

### Lot D — Non-régression (`19.0.10.7.0`)

| # | Scénario | Action | Attendu | MOA | Tech |
|---|----------|--------|---------|-----|------|
| **6** | Porte Incontournables | `/incontournables` | **301** → `marketone_mode=featured` ; pas de `marketone_category` | ☑ | ☑ |
| **9** | BO produit | Fiche Crackers (optionnel) | Rattachements catégories BO inchangés | ☐ | — |

---

## Détail scénarios — pas à pas

### 10 — Effacer les filtres (`19.0.10.8.0`)

**Contexte** : réserve MOA — les catégories `marketone_category` n’étaient pas comptées comme filtres actifs.

1. Ouvrir `/shop` sans filtre → **pas** de bouton Effacer les filtres.
2. Cocher **Biscuits salés**, **Biscuits sucrés**, **Épices** (comme capture multi-catégories).
3. **Contrôles** :
   - Bouton **Effacer les filtres** (ou *Supprimer les filtres* offcanvas mobile) **visible** dans la sidebar, **au-dessus** du bloc Origine.
   - URL contient plusieurs `marketone_category=…`.
   - Grille filtrée (union OR).
4. Cliquer **Effacer les filtres**.
5. **Contrôles finaux** :
   - URL = `/shop` (sans `marketone_category`).
   - Aucune case catégorie cochée.
   - Catalogue global affiché.

### 10b — Effacer avec Origine (optionnel)

1. Reprendre état **4d** (2 catégories + Martinique).
2. Cliquer **Effacer les filtres**.
3. **Attendu** : `/shop` sans `marketone_category` ni `attribute_values` ; toutes les cases décochées.

### 4d / 4e / 8b

Voir historique correctifs `19.0.10.5.0` → `19.0.10.7.0` (conservation croisée des facettes).

---

## Retour MOA structuré — repasse `19.0.10.8.0`

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-05-19 |
| **Version module** | `19.0.10.8.0` |
| **Upgrade `-u`** | ☑ OK |
| **Tests auto 13/13** | ☑ OK |

| Scénario | Verdict | Commentaire |
|----------|---------|-------------|
| **Smoke S1–S3** | ☑ GO | JS init ; `marketone_category` au clic ; bouton visible |
| **10** | ☑ GO | 3 catégories → Effacer → `/shop` global, cases décochées |
| **10b** | ☑ GO | Catégorie + Martinique → Effacer → plus de `marketone_category` ni `attribute_values` |

**Verdict global `19.0.10.8.0`** : ☑ **GO MOA**

### Référence — GO MOA `19.0.10.7.0` (ne pas repasser sauf régression)

| Lot | Scénarios | Statut |
|-----|-----------|--------|
| A Présentation | 1, 2, 2b, 3, 5 | **GO** (repasse `_107`) |
| B Catégories | 4, 4b, 4c | **GO** |
| C Combinaisons | 4d, 4e, 7, 8, 8b | **GO** |
| D Non-régression | 6 | **GO** |

---

## Historique verdicts

| Date | Version | Verdict | Détail |
|------|---------|---------|--------|
| 2026-05-19 | `19.0.10.7.0` | **GO MOA** | Sidebar multi OR ; commit `1ced35e` ; repasse `_107` |
| 2026-05-19 | `19.0.10.8.0` | **En attente** | Correctif bouton **Effacer les filtres** + scénario **10** |

| Version | Correctif |
|---------|-----------|
| `19.0.10.5.0` | Conservation facettes 4d (Origine après catégories) |
| `19.0.10.6.0` | Init JS `#wrap.marketone-shop` |
| `19.0.10.7.0` | Symétrie 4e (catégorie après Origine) |
| `19.0.10.8.0` | `marketone_has_category_filter` + `keep(marketone_category=0)` |

---

## Notes techniques

| Sujet | Détail |
|-------|--------|
| Effacer les filtres (`19.0.10.8.0`) | QWeb `shop_clear_filters.xml` — condition Odoo étendue avec `marketone_has_category_filter` |
| Query `keep()` | `_shop_get_query_url_kwargs` inclut `marketone_category` pour purge correcte au clic |
| Init JS | `#wrap.marketone-shop` + descendant `.oe_website_sale` |
| Symétrie URL | JS fusionne `form.js_attributes` + cases catégories |

---

## Captures (hors git)

| Fichier | Scénario | Repasse |
|---------|----------|---------|
| `marketone_sidebar_107_shop.png` | 1, 2, 3, 5 | `_107` |
| `marketone_sidebar_107_biscuits.png` | 4 | `_107` |
| `marketone_sidebar_107_multi_or.png` | 4b | `_107` |
| `marketone_sidebar_107_4d_categories_origin.png` | 4d | `_107` |
| `marketone_sidebar_107_4e_origin_then_category.png` | 4e | `_107` |
| `marketone_sidebar_107_uncheck_all.png` | 4c | `_107` |
| `marketone_sidebar_107_8b_price_after_facets.png` | 8b | `_107` |
| `marketone_sidebar_108_clear_filters.png` | **10** | `_108` |
| `marketone_sidebar_108_clear_filters_combo.png` | **10b** | `_108` |

Emplacement : `/private/tmp/` (hors dépôt git).
