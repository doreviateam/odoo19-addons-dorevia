# TICKET — Lot 6.3 Portes Promotions & Packs (cadrage cadrage2)

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_LOT6_3_PORTE_PROMO_PACK` |
| **Lot** | 6.3 — Portes **Promotions** et **Packs** |
| **Statut** | **Clôturé — GO MOA** (2026-06-08) · **6.3a GO clôture MOA** · **6.3b GO clôture MOA** |
| **Priorité MOA** | **1ère reprise front** post-cadrage2 |
| **Version cible module** | `19.0.17.0.0` (indicatif — après GO cadrage) |
| **Base** | `ckr-marketone-01` |
| **Prérequis** | Lots 1–5 **GO** · 6.1 **GO** · 6.2 **GO** · collections sidebar **GO** · BO `19.0.16.0.0` **GO avec réserves** |
| **ADR** | [ADR-034](../cadrage/DECISIONS.md#adr-034--arbitrage-architecture-cadrage2-socle-odoo-natif) · ADR-002 · ADR-003 · C3.4 |
| **Contrats** | C2 · C3.1–C3.7 · sources vérité CONTRACTS § C3 (Promotions / Kits-Packs) |
| **Arbitrage** | [`ARBITRAGE_ARCHITECTURE_CADRAGE2.md`](./ARBITRAGE_ARCHITECTURE_CADRAGE2.md) §5 |
| **Reprise front** | [`REPRISE_LOTS_FRONT_CADRAGE2.md`](./REPRISE_LOTS_FRONT_CADRAGE2.md) |

---

## En-tête recette obligatoire (ADR-034 · REPRISE §2)

```markdown
**ADR-034 :** [ARBITRAGE_ARCHITECTURE_CADRAGE2.md](./ARBITRAGE_ARCHITECTURE_CADRAGE2.md)

**Fonctionnalité Odoo native préservée :** Listes de prix · Promotions · (Packs : product.template pack si activé)

**Mécanisme Odoo concerné :** product.pricelist · product.pricelist.item · règles de prix Odoo · (pack : product_pack / pack_ok)

**Non-régression référence boutique :** [REFERENCE_RECETTE_BOUTIQUE_MOA.md](../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md) — sections B1 · B2 · B3 · B4 · B6 · B7
```

> Recette détaillée : [`RECETTE_MANUELLE_LOT6_3.md`](../recette/lots/RECETTE_MANUELLE_LOT6_3.md) — 6.3a et 6.3b signées GO MOA.

---

## Objectif MOA

Définir comment Marketone **expose** les notions **promo** et **pack** en s’appuyant sur les **mécanismes standards Odoo**, sans limiter l’activation future des pricelists, promotions, coupons ou règles commerciales natives.

```text
Le front peut présenter, orienter et mettre en avant.
Le calcul et la vérité prix restent Odoo.
Aucun moteur prix / promo / pack parallèle côté Marketone.
```

---

## Doctrine applicable

| Principe | Application Lot 6.3 |
|----------|---------------------|
| **Odoo exécute. Marketone habille et oriente.** | Portes = query `/shop` + présentation QWeb · filtre = hook Odoo |
| **ADR-002** | `website_sale` souverain pour prix affichés, panier, checkout |
| **ADR-034** | Interdiction moteur promo/prix/pack Marketone · futur = pricelist / promotions Odoo |
| **C3.1–C3.2** | Filtre via `_search_get_detail` + options contrôleur — **pas** de domaine QWeb |
| **C3.4** | Priorité modes : **pack > promo > featured > origin > collection** |
| **C3.6** | **Un seul** `marketone_mode` actif par requête |
| **C3.7** | Filtres natifs sidebar (catégories, origines, collections, prix) **conservés** |

---

## Interdictions explicites (MOA · ADR-034)

| Interdit | Raison |
|----------|--------|
| Champ « prix promo » custom sur `product.template` | Double vérité prix |
| Table ou modèle `marketone.promo.*` | Moteur parallèle |
| Calcul remise en Python/JS front | Odoo pricelist engine |
| Route catalogue autonome `/promotions` ou `/kits` (hors alias 301) | C2 conteneur `/shop` unique |
| Filtrage promo par comparaison manuelle `list_price` vs prix affiché en QWeb | Fragile · bypass pricelist |
| Tunnel checkout / panier custom | ADR-002 |
| Dépendance `website_blog` / `website_forum` | ADR-034 D1–D2 |

---

## Périmètre Lot 6.3 — deux portes, une doctrine

| Sous-lot | Mode URL | Libellé visiteur | Source de vérité Odoo (proposée) |
|----------|----------|------------------|----------------------------------|
| **6.3a Promotions** | `marketone_mode=promo` | **Promotions** | `product.pricelist.item` **actifs**, **strictement réducteurs**, sur la **pricelist courante** du visiteur |
| **6.3b Packs** | `marketone_mode=pack` | **Kits & Coffrets** (ou **Packs** — à trancher MOA) | `product.template` avec **`pack_ok=True`** — module **`product_pack`** (OCA) si activé |

> **Inspiration conceptuelle uniquement** : marketplace legacy A2 (`product.pricelist._ckr_get_promo_template_ids`) — **ne pas copier** mécaniquement ; reprendre le **principe** adossé à Odoo standard.

---

## 6.3a — Porte Promotions (cadrage technique proposé)

### Source de vérité

Un produit est « en promotion » pour le visiteur **ssi** il existe sur la **pricelist courante** au moins un `product.pricelist.item` :

| Critère | Règle |
|---------|-------|
| Temporalité | Item **actif** à `now` (`date_start` / `date_end` ouvertes ou englobantes) |
| Réduction | Item **strictement réducteur** vs prix de référence (rejet mark-up / `percent_price=0`) |
| Périmètre pricelist | **Pricelist courante visiteur** — même chaîne que checkout (`website._get_and_cache_current_pricelist()` + fallback partenaire public) |
| Global promo | Si item `applied_on=3_global` réducteur actif → sémantique **boutique en promo** (filtre produit optionnel — à trancher MOA) |
| Coupons / loyalty Odoo 19 | **Hors scope 6.3a initial** — extension future via ticket + ADR (union avec `sale_loyalty` si activé) |

### Comportement `/shop`

| Élément | Proposition |
|---------|-------------|
| Canonique | `/shop?marketone_mode=promo` |
| Alias 301 | `GET /promotions` → **301** → `/shop?marketone_mode=promo` (C2.4) |
| Filtre grille | Option `marketone_promo_only` → `_search_get_detail` → domaine ids templates éligibles |
| État vide | 200 + message sobre — **pas** 404 · **pas** 500 |
| Présentation | Titre **Promotions** · intro courte · lien « Tous les produits » → `/shop` (pattern 6.1 / 6.2) |
| Prix affichés grille | **Comportement natif** `website_sale` (barre promo Odoo si applicable) — Marketone ne recalcule pas |

### Extension code (indicatif — après GO cadrage)

| Couche | Fichier / objet |
|--------|-----------------|
| Modèle | Extension `product.pricelist` — helper `_marketone_get_promo_template_ids()` (nom à confirmer) |
| Modèle | Extension `product.template._search_get_detail` — branche promo |
| Contrôleur | `WebsiteSale` hérité — `_marketone_apply_mode_options` branche `promo` · alias `/promotions` |
| QWeb | `views/pages/shop_promo.xml` (présentation minimale) |
| Tests | Tag `dorevia_marketone_lot6_3_promo` |

---

## 6.3b — Porte Packs (cadrage technique proposé)

### Source de vérité

| Critère | Règle |
|---------|-------|
| Produit pack | `product.template.pack_ok = True` (module **`product_pack`** OCA) |
| Publication | `sale_ok` + `is_published` / visibilité site standard |
| Composants | Résolution **native** `product_pack` — pas de liste composants codée en dur |
| Prix pack | **Pricelist Odoo** + règles pack natives — pas de prix pack Marketone |

### Dépendance `product_pack`

| Option | Description | Recommandation Dev |
|--------|-------------|-------------------|
| **A — Activer `product_pack`** | Dépendance manifest + ADR amendement | **Recommandé** si MOA veut porte Kits réelle |
| **B — Reporter 6.3b** | Livrer **6.3a Promotions** seul | Si MOA préfère découpler |

> ADR-005 : `product_pack` = optionnelle · activation **par ticket MOA**.

### Comportement `/shop`

| Élément | Proposition |
|---------|-------------|
| Canonique | `/shop?marketone_mode=pack` |
| Alias 301 | `GET /kits` → **301** → `/shop?marketone_mode=pack` (legacy marketplace) |
| Filtre | Domaine `[('pack_ok', '=', True)]` via `_search_get_detail` — **pas** liste hardcodée |
| Présentation | Titre **Kits & Coffrets** · intro · lien retour |

---

## Décisions MOA tranchées (cadrage GO 2026-06-08)

| # | Décision MOA |
|---|--------------|
| **M1** | Livrer **6.3a Promotions seul** — 6.3b Kits & Coffrets = lot séparé |
| **M2** | **Pas** de `product_pack` dans ce lot — arbitrage 6.3b avec analyse impacts vente / stock / préparation / facturation / UX |
| **M3** | Promo globale `3_global` **validée** — exclusivement via `product.pricelist.item` actifs strictement réducteurs sur pricelist courante |
| **M4** | Libellé visiteur pack : **Kits & Coffrets** — « Pack » = terme technique/interne |
| **M5** | Chip header **Promotions** (`/promotions`) **maintenant** — chip `/kits` reporté 6.3b |
| **M6** | SEO canonical : **note documentaire** uniquement — implémentation = ticket SEO séparé |
| **M7** | Mode promo = **pricelist courante visiteur** · aucun calcul prix custom · aucun moteur promo parallèle |

**Ticket cadrage 6.3b** : [`TICKET_LOT6_3B_PORTE_KITS_COFFRETS.md`](./TICKET_LOT6_3B_PORTE_KITS_COFFRETS.md) — **GO cadrage MOA avec réserves**

**Ticket exécution 6.3b** : [`TICKET_MARKETONE_LOT6_3B_PORTE_PACK_EXEC.md`](../tickets/lots/TICKET_MARKETONE_LOT6_3B_PORTE_PACK_EXEC.md)

**Ticket exécution 6.3a** : [`TICKET_MARKETONE_LOT6_3A_PORTE_PROMO_EXEC.md`](../tickets/lots/TICKET_MARKETONE_LOT6_3A_PORTE_PROMO_EXEC.md) — **GO clôture MOA**

---

## Décisions MOA à trancher (cadrage) — archivé

| # | Question | Verdict MOA |
|---|----------|-------------|
| **M1** | Découpage livraison | **6.3a puis 6.3b** |
| **M2** | Activer `product_pack` ? | **Oui** — acté en 6.3b via ADR-035 |
| **M3** | Promo globale (`3_global`) | **Validée** (conditions C3.D) |
| **M4** | Libellé visiteur pack | **Kits & Coffrets** |
| **M5** | Chips header | **Promotions oui** · **Kits oui en 6.3b** |
| **M6** | SEO canonical | **Note doc** |
| **M7** | Multi-pricelist | **Pricelist courante visiteur** |

---

## Non-régression obligatoire

| Document | Sections |
|----------|----------|
| [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md) | **B1** smoke · **B2** compteur/chips · **B3** sidebar · **B4** tuiles · **B6** portes existantes (featured, origin) · **B7** UX-4 si applicable |
| Portes 6.1 / 6.2 | `/incontournables` · `/origines` · modes featured / origin inchangés |
| Priorité modes | `pack` > `promo` > `featured` — tests explicites |
| Panier / checkout | Smoke Lot 5 — prix panier = moteur Odoo |

---

## Note de livraison (exécution — phrase obligatoire)

```text
Aucun moteur Odoo remplacé — prix, promotions et packs s’appuient sur
product.pricelist / product.pricelist.item et (si activé) product_pack.
Marketone présente et filtre la grille /shop uniquement.
```

---

## Hors périmètre Lot 6.3

- Coupons `sale_loyalty` · programmes fidélité (ticket ultérieur)
- Refonte chips header « Tout · Promo · Kits · … » (Palier B2 ADR-031)
- SEO avancé canonical / noindex (ticket MOA SEO)
- BO custom « gestion promo CK »
- Pages catalogue autonomes hors `/shop`
- Modification tunnel checkout / code promo saisie checkout (natif Odoo)

---

## Critères GO cadrage (avant exécution)

- [x] M1–M7 tranchées MOA (2026-06-08)
- [x] Source vérité promo = **pricelist items** validée
- [x] Décision `product_pack` actée pour 6.3b — ADR-035 acceptée
- [x] Contrats C3.D (Promo) / C3.E (Pack) rédigés dans `CONTRACTS.md`
- [x] ADR-035 acceptée — dépendance `product_pack` activée Lot 6.3b
- [x] Ticket exécution [`TICKET_MARKETONE_LOT6_3A_PORTE_PROMO_EXEC.md`](../tickets/lots/TICKET_MARKETONE_LOT6_3A_PORTE_PROMO_EXEC.md) ouvert

---

## Critères GO exécution (indicatif)

```text
/promotions et /kits → 301 → /shop?marketone_mode=…
Grille filtrée correcte · prix affichés = Odoo natif
Portes 6.1 / 6.2 / sidebar / panier : non-régression
Tests auto lot6_3 verts · recette MOA signée
Note livraison : « aucun moteur Odoo remplacé »
```

---

## Fichiers attendus (exécution — proposition)

```text
dorevia_ckreyol_marketone/
├── __manifest__.py                          # 19.0.17.x · [+ product_pack si M2=Oui]
├── models/
│   ├── product_pricelist.py                 # NEW — helper promo template ids
│   └── product_template.py                  # étendu — _search_get_detail promo + pack
├── controllers/
│   └── website_sale.py                      # modes promo/pack · alias 301
├── views/pages/
│   ├── shop_promo.xml                       # NEW
│   └── shop_pack.xml                        # NEW
├── tests/
│   └── test_marketone_lot6_3_promo_pack.py  # NEW
└── docs/
    ├── cadrage/CONTRACTS.md                 # C3.D · C3.E
    └── recette/lots/RECETTE_MANUELLE_LOT6_3.md
```

---

## Références

| Document | Rôle |
|----------|------|
| [`CONTRACTS.md`](../cadrage/CONTRACTS.md) § C3 | Sources vérité portes |
| [`TICKET_MARKETONE_LOT6_1_INCONTOURNABLES_EXEC.md`](../tickets/lots/TICKET_MARKETONE_LOT6_1_INCONTOURNABLES_EXEC.md) | Pattern porte |
| [`TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES_EXEC.md`](../tickets/lots/TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES_EXEC.md) | Pattern porte + facette |
| [`TAXONOMIE_CATALOGUE.md`](../cadrage/TAXONOMIE_CATALOGUE.md) | Distinction pack vs collection |
| Marketplace `product_pricelist._ckr_get_promo_template_ids` | Inspiration A2 — **non copie** |

---

## Verdict MOA cadrage

| Date | Verdict | Commentaire |
|------|---------|-------------|
| 2026-06-08 | ☑ GO cadrage · ☑ 6.3a GO clôture MOA · ☑ 6.3b GO clôture MOA · ☐ À retravailler | M1–M7 tranchées · 6.3a clôturé · 6.3b clôturé `19.0.18.0.0` |
