# Cadrage MOA — SEO portes `/shop` Marketone

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-06-08 |
| **Ticket** | [`TICKET_MARKETONE_SEO_PORTES_SHOP.md`](../tickets/boutique/TICKET_MARKETONE_SEO_PORTES_SHOP.md) |
| **Statut** | **Décision MOA validée** — [`DECISION_MOA_SEO_PORTES_SHOP.md`](./DECISION_MOA_SEO_PORTES_SHOP.md) · implémentation **19.0.19.0.0** |
| **Module** | `dorevia_ckreyol_marketone` · version actuelle `19.0.18.0.0` |
| **Contexte** | Filière `sale_product_pack` **clôturée** — reprise priorité SEO portes |

---

## Doctrine opposable

```text
Odoo exécute. Marketone habille et oriente.
Aucun moteur Odoo remplacé.
```

| Règle | Référence |
|-------|-----------|
| `/shop` = **conteneur catalogue unique** | CONTRACTS **C2** |
| Portes = **query string** sur `/shop` | **C2.2** · **C3** |
| Alias = **301** vers URL canonique porte | **C2.4** · routes `website_sale.py` |
| **Pas** de page catalogue autonome Marketone | **C2** · ADR-034 |
| SEO = champs natifs Odoo d’abord | ARBITRAGE **F8** |

**Hors scope SEO** : panier · checkout · prix · promo · pack · tunnel achat — **aucune modification métier**.

---

## Périmètre URLs — portes livrées

| Porte MOA | Alias **301** | URL canonique porte |
|-----------|---------------|---------------------|
| **Incontournables** | `/incontournables` | `/shop?marketone_mode=featured` |
| **Origines** (porte seule) | `/origines` | `/shop?marketone_mode=origin` |
| **Origines** (facette) | — | `/shop?marketone_mode=origin&marketone_origin=<slug>` |
| **Promotions** | `/promotions` | `/shop?marketone_mode=promo` |
| **Kits & Coffrets** | `/kits` | `/shop?marketone_mode=pack` |
| **Catalogue général** | — | `/shop` |

Constantes code : `MARKETONE_*_CANONICAL_QUERY` dans `controllers/website_sale.py`.

**État technique actuel** :

| Élément | État |
|---------|------|
| Alias **301** | ✓ Implémentés · `sitemap=False` sur routes alias |
| `rel=canonical` portes | ✓ Extension `website._get_canonical_url` |
| `noindex` / `robots` | ✓ Layout `website.layout` · `noindex,follow` T4/T5 porte |
| Extension `website` canonical | ✓ `models/website.py` |

---

## Objectifs MOA

1. **Sécuriser** les URLs portes déjà livrées — pas de duplication indexable alias / paramètres bruit.
2. **Trancher** `canonical` et règles d’**indexation** par type d’URL.
3. **Garantir** non-régression portes 6.1 · 6.2 · 6.3a · 6.3b.
4. **Ne pas** ouvrir panier · checkout · prix · promo · pack.

---

## Typologie URLs (grille SEO)

| Classe | Exemple | Rôle |
|--------|---------|------|
| **T0 — Catalogue nu** | `/shop` | Grille complète sans porte |
| **T1 — Alias porte** | `/kits` | Entrée mémorable → **301** |
| **T2 — Porte canonique** | `/shop?marketone_mode=pack` | Landing porte MOA |
| **T3 — Porte + facette métier** | `/shop?marketone_mode=origin&marketone_origin=guadeloupe` | Landing origine |
| **T4 — Porte + filtres natifs** | `…&order=…` · `attribute_values=…` · `min_price=…` | Filtrage sidebar Odoo |
| **T5 — Pagination** | `…&page=2` | Liste paginée |
| **T6 — Params inconnus** | `?foo=bar` | Ignorés silencieusement (**C3.3**) |

---

## Proposition MOA — règles `canonical` / indexation

> **À valider MOA** — options tranchées en atelier ; exécution post-signature.

### Principes transverses

| # | Principe |
|---|----------|
| P1 | L’**alias** ne doit **jamais** être indexé — **301 permanent** suffit. |
| P2 | L’**URL canonique porte** (T2) est la **référence SEO** de la porte. |
| P3 | Les **params inconnus** n’apparaissent pas dans le `canonical`. |
| P4 | **`marketone_mode`** actif unique — priorité **C3.4** inchangée. |
| P5 | Panier / checkout / wishlist : **hors** grille portes — politique Odoo standard. |

### Matrice par porte (T2 — mode seul)

| Porte | URL canonique | Indexation proposée | `rel=canonical` proposé |
|-------|---------------|---------------------|-------------------------|
| Incontournables | `/shop?marketone_mode=featured` | **index** | **self** (URL normalisée) |
| Origines | `/shop?marketone_mode=origin` | **index** | **self** |
| Promotions | `/shop?marketone_mode=promo` | **index** | **self** |
| Kits & Coffrets | `/shop?marketone_mode=pack` | **index** | **self** |
| Catalogue | `/shop` | **index** | **self** |

### Matrice alias (T1)

| Alias | Cible 301 | Sitemap route | Indexation |
|-------|-----------|---------------|------------|
| `/incontournables` | `featured` | `False` ✓ | **non** (redirect) |
| `/origines` | `origin` | `False` ✓ | **non** |
| `/promotions` | `promo` | `False` ✓ | **non** |
| `/kits` | `pack` | `False` ✓ | **non** |

### Origines facettées (T3)

| URL | Indexation proposée | Canonical proposé |
|-----|---------------------|-------------------|
| `/shop?marketone_mode=origin&marketone_origin=<slug>` *(1 slug)* | **index** | **self** normalisé (slug unique, ordre stable) |
| Multi-slugs `marketone_origin` *(OU)* | **index** ou **noindex** *(MOA)* | **self** ou canonical porte seule *(MOA)* |

**Recommandation cadrage** : **index** si 1 slug publié — landing origine utile SEO · **noindex,follow** si combinaison multi-slugs rare.

### Filtres natifs + pagination (T4 · T5) — **choix MOA**

| Option | Comportement | Pour | Contre |
|--------|--------------|------|--------|
| **A — Canonical strict porte** | T4/T5 → canonical = **T2** (porte sans filtres) · `noindex,follow` sur URLs filtrées/paginées | Évite duplicate content · simple | Moins de longue traîne SEO filtres |
| **B — Canonical self filtré** | Chaque combinaison whitelistée a son canonical **self** | SEO filtres | Risque explosion URLs indexables |
| **C — Hybride** *(recommandé)* | T2/T3 **index** · T4/T5 **`noindex,follow`** + canonical **T2** ou **T3** | Équilibre e-commerce | Nécessite liste params « bruit » |

**Recommandation MOA** : **Option C** — indexer les **portes** et **facettes origine** ; **noindex,follow** sur combinaisons `order` · `page` · `min_price` · `max_price` · `attribute_values` · `marketone_category` · `marketone_collection` lorsqu’une porte T2/T3 est active.

### Params whitelist canonical (extension C9)

| Paramètre | Inclus canonical porte | Inclus canonical facette origine |
|-----------|----------------------|----------------------------------|
| `marketone_mode` | ✓ | ✓ |
| `marketone_origin` | — | ✓ *(slugs triés)* |
| `search` | ☐ bruit | ☐ bruit |
| `order` | ☐ bruit | ☐ bruit |
| `page` | ☐ bruit | ☐ bruit |
| `min_price` / `max_price` | ☐ bruit | ☐ bruit |
| `attribute_values` | ☐ bruit | ☐ bruit |
| `marketone_category` | ☐ bruit | ☐ bruit |
| `marketone_collection` | ☐ bruit | ☐ bruit |

---

## Non-régression exigée

| Zone | Tests / recette |
|------|---------------|
| Alias **301** | `dorevia_marketone_lot6_1_featured` · `lot6_2_origin` · `lot6_3a_promo` · `lot6_3b_pack` |
| Grilles portes | Contenu filtré inchangé |
| Chips header | Liens `/promotions` · `/kits` selon politique gate |
| Smoke REFERENCE_RECETTE_BOUTIQUE | Sections impactées |
| Panier / checkout | **0 régression** — hors diff SEO head |

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d ckr-marketone-01 \
  --test-tags=dorevia_marketone_lot6_1_featured,dorevia_marketone_lot6_2_origin,dorevia_marketone_lot6_3a_promo,dorevia_marketone_lot6_3b_pack \
  --stop-after-init --http-port=0
```

---

## Hors périmètre

| Sujet | Traitement |
|-------|------------|
| Collections `marketone_mode=collection` | Ticket Lot B / ADR-030 — hors ce cadrage |
| Culture `/culture/<slug>` | Politique SEO distincte |
| Savoirs | Hors scope |
| Sitemap XML custom complet | Phase 2 optionnelle — v1 = `sitemap=False` alias + head tags |
| `website_sale_product_pack` / checkout detailed | Filière pack **clôturée** |
| Refonte chips / navigation | Hors scope |
| Blog / forum | Interdit ADR-034 |

---

## Livrables attendus (post-validation MOA)

| # | Livrable | Responsable |
|---|----------|-------------|
| 1 | **Décision MOA** signée — option T4/T5 · multi-origin | MOA |
| 2 | Extension **`website`** (ou hook head `/shop`) — `canonical` + `robots` | Dev |
| 3 | Tests auto SEO portes | Dev |
| 4 | Recette manuelle SEO — vérif head + Search Console ready | MOA |
| 5 | Amendement **C9** / **ADR-036** si règles figées | Doc |

---

## Décisions MOA — tranchées (2026-06-08)

| # | Question | Verdict MOA |
|---|----------|-------------|
| D1 | Alias **301** non indexés | ✓ **Validé** |
| D2 | Portes **T2** indexables · canonical self | ✓ **Validé** |
| D3 | Facette origine **T3** (1 slug) indexable | ✓ **Validé** |
| D4 | T4 sur porte : **noindex,follow** + canonical T2/T3 | ✓ **Option C** |
| D5 | T5 pagination : navigable · pas page SEO principale | ✓ **Option C** |
| D6 | `/shop` nu indexable · canonical self | ✓ **Validé** |

**Document opposable** : [`DECISION_MOA_SEO_PORTES_SHOP.md`](./DECISION_MOA_SEO_PORTES_SHOP.md)

---

## Références

- [`CONTRACTS.md`](../cadrage/CONTRACTS.md) — C2 · C3 · **C9**
- [`TICKET_MARKETONE_CONSOLIDATION_PORTES_BOUTIQUE.md`](../tickets/boutique/TICKET_MARKETONE_CONSOLIDATION_PORTES_BOUTIQUE.md)
- [`REPRISE_LOTS_FRONT_CADRAGE2.md`](./REPRISE_LOTS_FRONT_CADRAGE2.md)
- [`DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md`](./DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md) — pack = article · filière pack fermée
- `controllers/website_sale.py` — alias · constantes canonical query

---

## Verdict cadrage

| Date | Statut |
|------|--------|
| 2026-06-08 | **GO MOA D1–D6** · implémentation livrée **19.0.19.0.0** |
