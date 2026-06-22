# Recette QA — Lot Nav-Shop · Catégories e-commerce dynamiques CK V2

| Champ | Valeur |
| --- | --- |
| **Projet** | `dorevia_ck_marketone` |
| **Ticket** | [`TICKET_DEV_LOT_NAV_SHOP_CATEGORIES_ECOMMERCE_CK_V2.md`](../TICKET_DEV_LOT_NAV_SHOP_CATEGORIES_ECOMMERCE_CK_V2.md) |
| **Branche Dev** | `feat/ck-nav-shop-categories-v2` |
| **Instance seed** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **Modules** | `dorevia_ck_marketone_content` **19.0.1.27.0** · `dorevia_ck_theme` **19.0.1.38.1** |
| **Périmètre** | Sync `product.public.category` → header · non-régression Nav-1 / H1 / Découvrir |

```text
Nav-Shop — arborescence BO dynamique (nav_sync.py)
Libellés menu = noms catégories BO · 2 niveaux max header
Tous nos produits + Découvrir inchangés · chrome H1 conservé
```

---

## 1. Mapping catalogue BO (post-sync)

Extrait via `bootstrap_ck_navigation()` + `get_nav_category_mapping(env)` — **2026-06-22**.

| Entrée menu | Catégorie BO | Visible | ≥ 1 produit publié |
| --- | --- | --- | --- |
| **Tous nos produits** | Catalogue complet | Oui | Oui |
| **Épicerie** | Épicerie | Oui | Oui |
| **Maison & bien-être** | Maison & bien-être | Oui | Oui |
| **Artisanat & Culture** | Artisanat & Culture | Oui | Oui |
| **Coups de cœur** | Coups de cœur | Oui | Oui |
| **Boissons** | Boissons | Oui | Oui |
| **Packs & découvertes** | Packs & découvertes | Non | Non |

**Changement Nav-Shop** : fin de l’alias Nav-1 « Soin & Bien-être » → libellé BO **Maison & bien-être**.

### Mega Découvrir — non-régression

| Libellé | URL | Visible |
| --- | --- | --- |
| Producteurs & territoires | `/producteur/atelier-hauts-goyaviers` | Oui |
| Recettes & usages | `/recettes` | Oui |
| Professionnels | `/professionnels` | Oui |
| Contactez-nous | `/contactus` | Oui |

Aucun lien `/shop/category/` dupliqué dans `ck-nav-decouvrir-links`.

---

## 2. Tests automatisés

### Commandes

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 -u dorevia_ck_marketone_content,dorevia_ck_theme --stop-after-init

docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 --test-enable --stop-after-init --http-port=8078 \
  --test-tags dorevia_ck_marketone_nav_sync,dorevia_ck_theme_phase10
```

### Résultat — **2026-06-22**

| Tag | Module | Tests | Résultat |
| --- | --- | ---: | --- |
| `dorevia_ck_marketone_nav_sync` | `dorevia_ck_marketone_content` | 11 | **OK** |
| `dorevia_ck_theme_phase10` | `dorevia_ck_theme` | 14 | **OK** |
| **Total** | | **25** | **0 failed · 0 error** |

### Couverture (extraits)

| Cas | Statut |
| --- | --- |
| Arborescence dynamique · fin `NAV_UNIVERSE_SPECS` | ✅ |
| Boissons visible si produit publié | ✅ |
| Niveau 2 desktop sous parent · pas à la racine | ✅ |
| Niveau 3 absent du header | ✅ |
| Ordre `sequence` BO | ✅ |
| Mobile Nos univers + enfants | ✅ |
| Mega Découvrir sans commerce | ✅ |
| Non-régression H1 (service bar · recherche · mobile chrome) | ✅ |
| B1/B2 Nav-1 (Nos univers masqué desktop · pas de doublon mobile) | ✅ |

---

## 3. Recette desktop 1280 px

Scripts : [`ck_nav_shop_recette_desktop_1280.mjs`](./scripts/ck_nav_shop_recette_desktop_1280.mjs)  
Captures : [`captures/recette_nav_shop_v2/`](./captures/recette_nav_shop_v2/)

| # | Scénario | Attendu | Résultat | Preuve |
| --- | --- | --- | --- | --- |
| R1 | Entrées fixes | Tous nos produits · Découvrir accessibles | **OK** | D2 · D4 |
| R2 | Libellés BO | Noms catégories (ex. Maison & bien-être) | **OK** | D1 · D3 |
| R3 | Boissons | Visible si éligible | **OK** | Mapping §1 · extra menu |
| R4 | Mega Découvrir | 4 liens éditoriaux · sans commerce | **OK** | D4 |
| R5 | Chrome H1 | Bandeau · recherche · marque · panier | **OK** | D5 |
| R6 | Contraste mega | Couleur lisible au survol | **OK** | D7 `rgb(28, 25, 23)` |
| R7 | Densité 5 racines | Pas de chevauchement logo / panier | **OK** | D6 `overlapChrome: false` |
| R8 | Overflow Odoo | 7 entrées → `o_extra_menu_items` | **Documenté** | D2 `decouvrirInExtraMenu: true` |

**Comportement densité (5 racines seed)** : les entrées **Coups de cœur · Boissons · Découvrir** passent dans le menu overflow natif Odoo (`…`) faute de place à 1280 px — voir [`NOTE_NAV_SHOP_REMONTEE_DENSITE.md`](./NOTE_NAV_SHOP_REMONTEE_DENSITE.md). Accès Découvrir vérifié via overflow · mega fonctionnel.

Visibles en barre principale : **Tous nos produits · Épicerie · Maison & bien-être · Artisanat & Culture · …**

---

## 4. Recette mobile 390 px

Script : [`ck_nav_shop_recette_mobile_390.mjs`](./scripts/ck_nav_shop_recette_mobile_390.mjs)

| # | Scénario | Attendu | Résultat | Preuve |
| --- | --- | --- | --- | --- |
| M1 | Drawer top-level | Tous nos produits · Découvrir · pas univers desktop plats | **OK** | M1 · M3 |
| M2 | Nos univers | 5 racines BO sous accordéon | **OK** | M2 (5 hrefs catégorie) |
| M3 | Pas de doublon | Chaque univers visible 1× | **OK** | M3 counts = 1 |
| M4 | Chrome H1 mobile | Bandeau · burger · pas recherche dans drawer | **OK** | M4 |
| M5 | Overflow horizontal | Aucun scroll parasite | **OK** | M5 |

Captures : `nav_shop_mobile_390_drawer.png` · `nav_shop_mobile_390_nos_univers_open.png`

---

## 5. Documents associés

| Document | Rôle |
| --- | --- |
| [`NOTE_NAV_SHOP_REMONTEE_DENSITE.md`](./NOTE_NAV_SHOP_REMONTEE_DENSITE.md) | Règle de remontée · densité 7+ · contrainte mobile 2 niveaux Odoo |
| [`TICKET_DEV_LOT_NAV_SHOP_CATEGORIES_ECOMMERCE_CK_V2.md`](../TICKET_DEV_LOT_NAV_SHOP_CATEGORIES_ECOMMERCE_CK_V2.md) | Spécification MOA validée |

---

## 6. Synthèse Dev

| Livrable | Statut |
| --- | --- |
| Refactor `nav_sync.py` | ✅ |
| Bump `dorevia_ck_marketone_content` 19.0.1.27.0 | ✅ |
| Bump `dorevia_ck_theme` 19.0.1.38.1 (dropdown L2) | ✅ |
| Migration post-sync 19.0.1.27.0 | ✅ |
| Tests nav_sync + phase10 | ✅ 25/25 |
| Recette QA + captures 1280/390 | ✅ |
| Note remontée + densité | ✅ |

**Point MOA densité** : avec **5 racines éligibles** sur seed, le header atteint le seuil overflow Odoo — arbitrage MOA recommandé avant ajout d’une 6ᵉ racine si **Découvrir** doit rester en barre principale visible sans `…`.
