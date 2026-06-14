# TICKET — Lot 6.3a Exécution Porte Promotions `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_LOT6_3A_PORTE_PROMO_EXEC` |
| **Lot** | 6.3a — Porte **Promotions** (implémentation) |
| **Statut** | **Clôturé — GO MOA** (2026-06-08) |
| **Version cible module** | `19.0.17.0.0` |
| **Base** | `ckr-marketone-01` |
| **Prérequis** | Lots 1–5 **GO** · 6.1 **GO** · 6.2 **GO** · BO `19.0.16.0.0` **GO avec réserves** · cadrage **GO** — [`TICKET_LOT6_3_PORTE_PROMO_PACK.md`](../../cadrage2/TICKET_LOT6_3_PORTE_PROMO_PACK.md) |
| **ADR** | [ADR-034](../../cadrage/DECISIONS.md#adr-034--arbitrage-architecture-cadrage2-socle-odoo-natif) · ADR-002 · ADR-003 |
| **Contrats** | C2 · C3.1–C3.7 · **C3.D** |
| **Arbitrage** | [`ARBITRAGE_ARCHITECTURE_CADRAGE2.md`](../../cadrage2/ARBITRAGE_ARCHITECTURE_CADRAGE2.md) §5 |
| **Recette** | [`RECETTE_MANUELLE_LOT6_3A_PROMO.md`](../../recette/lots/RECETTE_MANUELLE_LOT6_3A_PROMO.md) |

---

## En-tête recette obligatoire (ADR-034 · REPRISE §2)

```markdown
**ADR-034 :** [ARBITRAGE_ARCHITECTURE_CADRAGE2.md](../../cadrage2/ARBITRAGE_ARCHITECTURE_CADRAGE2.md)

**Fonctionnalité Odoo native préservée :** Listes de prix · Promotions

**Mécanisme Odoo concerné :** product.pricelist · product.pricelist.item · règles de prix Odoo

**Non-régression référence boutique :** [REFERENCE_RECETTE_BOUTIQUE_MOA.md](../../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md) — sections B1 · B2 · B3 · B4 · B6 · B7
```

---

## Objectif

Implémenter la porte catalogue **Promotions** sans moteur prix/promo parallèle, en s’appuyant exclusivement sur **`product.pricelist.item`** de la **pricelist courante du visiteur**.

```text
Critère GO Lot 6.3a :
La porte Promotions oriente la grille /shop vers les produits éligibles promo Odoo,
affiche les prix via website_sale natif, et ne remplace aucun moteur Odoo.
```

**Hors scope immédiat** : Lot **6.3b Kits & Coffrets** (`product_pack` — cadrage séparé).

---

## Décisions MOA figées (cadrage GO 2026-06-08)

| # | Décision |
|---|----------|
| **M1** | Livrer **6.3a Promotions seul** — 6.3b Kits & Coffrets = lot séparé |
| **M2** | **Pas** de dépendance `product_pack` dans ce lot |
| **M3** | Sémantique **promo globale** (`applied_on=3_global`) **validée** : si item global actif strictement réducteur sur pricelist courante → **catalogue complet** sans filtre produit supplémentaire ; sinon filtre sur ids templates éligibles |
| **M4** | Libellé visiteur futur pack : **Kits & Coffrets** — « Pack » = terme technique/interne uniquement (préparation 6.3b) |
| **M5** | **Chip header Promotions** maintenant — lien `/promotions` · **pas** de chip `/kits` avant 6.3b |
| **M6** | SEO canonical / noindex : **note documentaire** uniquement — implémentation = ticket SEO séparé |
| **M7** | Mode promo = **pricelist courante visiteur** uniquement · **aucun** calcul prix custom Marketone · **aucun** moteur promo parallèle |

**Doctrine opposable** : **Odoo exécute. Marketone habille et oriente.**

---

## Périmètre inclus

### 1. Modèle `product.pricelist` — résolveur promo (source vérité C3.D)

| Livrable | Détail |
|----------|--------|
| Méthode | `_marketone_get_promo_template_ids(website=None, pricelist=None)` |
| Retour | `None` = promo globale active · `set()` = état vide · `set` non vide = ids templates éligibles |
| Items | Actifs à `now` · **strictement réducteurs** · pricelist courante visiteur |
| `applied_on` | `0_product_variant` · `1_product` · `2_product_category` · `3_global` |
| Chaîne pricelist | Paramètre explicite → `website._get_and_cache_current_pricelist()` → fallback `partner.property_product_pricelist` |
| Helpers | `_marketone_active_pricelist_items_domain` · `_marketone_pricelist_item_is_reducer` (noms indicatifs) |
| Extensibilité | Point d’union documenté pour `sale_loyalty` futur — **hors scope 6.3a** |

**Interdit** : champ promo custom · table `marketone.promo.*` · comparaison manuelle `list_price` vs prix affiché.

> **Inspiration conceptuelle** : marketplace `_ckr_get_promo_template_ids` — **ne pas copier** mécaniquement ; reprendre le **principe** adossé Odoo 19 + préfixe `marketone_*`.

### 2. Modèle `product.template` — filtre grille

Extension `_search_get_detail` :

| Option | Comportement |
|--------|--------------|
| `marketone_promo_only=True` | Applique domaine promo |
| Promo globale (`None`) | **Pas** de restriction domaine produit supplémentaire |
| État vide (`set()`) | Domaine impossible `[('id', '=', 0)]` |
| Ids non vides | `[('id', 'in', ids)]` |

### 3. Contrôleur — extension `WebsiteSale`

| Règle | Application |
|-------|-------------|
| Mode | Ajouter `promo` à `MARKETONE_IMPLEMENTED_MODES` |
| Whitelist | `marketone_mode=promo` — un seul mode actif (C3.6) |
| Priorité | `pack > promo > featured > origin > collection` (C3.4) — tests si cumul query |
| Options | Injection `_get_search_options` → `marketone_promo_only` |
| Alias | `GET /promotions` → **301** → `/shop?marketone_mode=promo` |
| Prix panier | Inchangé — moteur Odoo |
| Filtres sidebar | **Conservés** (C3.7) |

Variables QWeb indicatives : `marketone_promo_mode`, `marketone_promo_empty`, `marketone_shop_grid_title` = **Promotions**.

### 4. QWeb — bandeau porte `/shop`

Héritage `website_sale.products` sous `.marketone-shop` (pattern 6.1 / 6.2) :

| Élément | Contenu |
|---------|---------|
| Titre | **Promotions** |
| Intro | 1–2 phrases courtes |
| Lien retour | « Tous les produits » → `/shop` (sans `marketone_mode`) |
| État vide | Message sobre si aucun item promo actif |
| Prix grille | **Natif** `website_sale` — Marketone ne recalcule pas |

Fichier indicatif : `views/pages/shop_promo.xml`.

### 5. Chip header navigation (M5)

| Élément | Règle |
|---------|-------|
| Libellé | **Promotions** |
| Cible | `/promotions` (alias 301 — amendement C3.D vs C2.4 générique) |
| Emplacement | Header site (`.marketone-chrome`) — **pas** barre chips filtres actifs (UX-1 G10) |
| Exclus | Chip **Kits & Coffrets** / `/kits` — reporté **6.3b** |
| Tests | Mettre à jour garde-fous Lot 3 : autoriser `/promotions` dans **header global** ; interdit dans toolbar grille / sidebar / chips filtres |

### 6. SEO (M6)

Note documentaire uniquement dans ce lot — pas d’implémentation `canonical` / `noindex` (ticket SEO séparé).

### 7. Données recette BO

| Élément | Détail |
|---------|--------|
| Pricelist site | Items **actifs** strictement **réducteurs** sur pricelist visiteur |
| Jeu minimal | ≥ 2 produits promo · ≥ 1 produit hors promo |
| Global promo | Scénario optionnel item `3_global` documenté recette |
| Seed | **Manuel BO** — pas de seed XML produits (C10) |

---

## Périmètre exclu

- Lot **6.3b** Kits & Coffrets · dépendance `product_pack`
- Alias `/kits` · chip header Kits
- Coupons / `sale_loyalty` / programmes fidélité
- BO custom « gestion promo CK »
- SEO canonical / noindex implémenté
- Refonte Palier B2 complète (Tout · Promo · Kits · …)
- Modification tunnel checkout / saisie code promo

---

## Tests — tag `dorevia_marketone_lot6_3a_promo`

| Test | Attendu |
|------|---------|
| `test_promo_shop_200` | `/shop?marketone_mode=promo` → 200 |
| `test_promotions_301` | `/promotions` → 301 · Location canonique |
| `test_promo_filters_products` | Grille ⊆ produits avec item réducteur actif |
| `test_promo_global_no_product_filter` | Item `3_global` actif → catalogue complet visible |
| `test_promo_empty_state` | Aucun item actif → 200 · grille vide · message |
| `test_promo_respects_current_pricelist` | Changement pricelist visiteur → jeu promo cohérent |
| `test_unknown_mode_ignored` | `marketone_mode=unknown` → shop standard |
| `test_featured_origin_unchanged` | Portes 6.1 / 6.2 non régressées |
| `test_header_promotions_chip` | Lien `/promotions` présent header · absent chips filtres |
| `test_no_kits_chip` | Pas de lien `/kits` exposé |
| `test_cart_checkout_regression` | Panier + checkout OK · prix = Odoo |
| Non-régression | Suites existantes + lot6_3a vertes |

Fichier indicatif : `tests/test_marketone_lot6_3a_promo.py`.

---

## Fichiers attendus

```text
dorevia_ckreyol_marketone/
├── __manifest__.py                          # 19.0.17.0.0
├── models/
│   ├── __init__.py                          # import product_pricelist
│   └── product_pricelist.py                 # NEW
├── models/product_template.py               # étendu — promo branch
├── controllers/website_sale.py              # mode promo · alias · chip context
├── views/pages/shop_promo.xml               # NEW
├── views/layout/header.xml                  # chip Promotions (M5)
├── tests/test_marketone_lot6_3a_promo.py    # NEW
├── docs/cadrage/CONTRACTS.md                # C3.D figé
└── docs/recette/lots/RECETTE_MANUELLE_LOT6_3A_PROMO.md
```

**Pas** de dépendance `product_pack` dans `__manifest__.py`.

---

## Note de livraison (phrase obligatoire)

```text
Aucun moteur Odoo remplacé — les promotions s’appuient sur product.pricelist
/ product.pricelist.item (pricelist courante visiteur). Marketone présente et
filtre la grille /shop uniquement.
```

---

## Critères GO exécution

- [ ] `/promotions` → 301 → `/shop?marketone_mode=promo`
- [ ] Grille filtrée selon C3.D · prix affichés = Odoo natif
- [ ] Chip header **Promotions** visible · **pas** de chip Kits
- [ ] Portes 6.1 / 6.2 · sidebar · panier : non-régression
- [ ] Tests `dorevia_marketone_lot6_3a_promo` verts
- [ ] Recette MOA signée
- [ ] Note livraison : **« aucun moteur Odoo remplacé »**

---

## Références

| Document | Rôle |
|----------|------|
| [`TICKET_LOT6_3_PORTE_PROMO_PACK.md`](../../cadrage2/TICKET_LOT6_3_PORTE_PROMO_PACK.md) | Cadrage clôturé GO |
| [`TICKET_MARKETONE_LOT6_1_INCONTOURNABLES_EXEC.md`](./TICKET_MARKETONE_LOT6_1_INCONTOURNABLES_EXEC.md) | Pattern porte |
| [`TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES_EXEC.md`](./TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES_EXEC.md) | Pattern porte |
| Marketplace `product_pricelist._ckr_get_promo_template_ids` | Inspiration A2 — non copie |

---

## Verdict MOA exécution

| Date | Verdict | Commentaire |
|------|---------|-------------|
| 2026-06-08 | ☑ **GO clôture MOA** | P1–P8 · N1–N3 · R1–R4 signés · P7 S/O · [`RECEPTION_MOA_LOT6_3A_PROMO.md`](../../cadrage2/RECEPTION_MOA_LOT6_3A_PROMO.md) |
