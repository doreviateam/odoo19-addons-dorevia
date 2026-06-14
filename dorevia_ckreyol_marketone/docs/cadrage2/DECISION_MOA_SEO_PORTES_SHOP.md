# Décision MOA — SEO portes `/shop` · D1–D6

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-06-08 |
| **Verdict** | **GO cadrage SEO D1–D6** · exécution autorisée |
| **Ticket** | [`TICKET_MARKETONE_SEO_PORTES_SHOP.md`](../tickets/boutique/TICKET_MARKETONE_SEO_PORTES_SHOP.md) |
| **Cadrage** | [`CADRAGE_SEO_PORTES_SHOP.md`](./CADRAGE_SEO_PORTES_SHOP.md) |
| **ADR** | [ADR-036](../cadrage/DECISIONS.md#adr-036--seo-portes-shop-d1d6) |
| **Module** | `dorevia_ckreyol_marketone` |

---

## Doctrine opposable

```text
/shop reste le conteneur catalogue unique.
Les portes Marketone sont des entrées SEO maîtrisées.
Les combinaisons de filtres sont des états de navigation, pas des pages SEO à pousser.
Odoo exécute. Marketone habille et oriente.
```

---

## Décisions MOA validées

| # | Sujet | Décision |
|---|-------|----------|
| **D1** | Alias **301** | **Validé** — `/incontournables`, `/origines`, `/promotions`, `/kits` restent des entrées **301** vers les URLs canoniques `/shop?marketone_mode=…` · **non indexés** comme pages autonomes |
| **D2** | Portes simples **T2** | **Validé** — indexables · `rel=canonical` **self** normalisé : `featured` · `origin` · `promo` · `pack` |
| **D3** | Origine facettée **T3** | **Validé** — 1 slug publié indexable · canonical **self** normalisé : `/shop?marketone_mode=origin&marketone_origin=<slug>` |
| **D4** | Filtres sur porte **T4** | **Validé option C** — combinaisons porte + filtres additionnels : **`noindex,follow`** · canonical vers la porte **T2/T3** correspondante |
| **D5** | Pagination **T5** | **Validé option C** — pages paginées ou combinées avec filtres **navigables** · **pas** pages SEO principales |
| **D6** | `/shop` nu **T0** | **Validé** — `/shop` reste **indexable** · canonical **self** |

### Compléments opposables (cadrage)

| Sujet | Règle |
|-------|-------|
| Multi-slugs `marketone_origin` | **`noindex,follow`** · canonical porte origine seule (`/shop?marketone_mode=origin`) |
| Params « bruit » canonical | `search` · `order` · `page` · `min_price` · `max_price` · `attribute_values` · `marketone_category` · `marketone_collection` — **exclus** du canonical |
| Params whitelist canonical | `marketone_mode` · `marketone_origin` *(T3, 1 slug)* |
| Implémentation v1 | **Head tags only** — extension `website._get_canonical_url` + `robots` layout · pas refonte sitemap |

---

## Matrice URLs

| Classe | Exemple | Index | Canonical |
|--------|---------|-------|-----------|
| **T0** | `/shop` | index | self |
| **T1** | `/kits` | non (301) | cible T2 |
| **T2** | `/shop?marketone_mode=pack` | index | self normalisé |
| **T3** | `/shop?marketone_mode=origin&marketone_origin=guadeloupe` | index *(1 slug)* | self normalisé |
| **T4** | T2/T3 + filtres | **noindex,follow** | T2 ou T3 sans bruit |
| **T5** | T2/T3 + `page` | **noindex,follow** | T2 ou T3 sans bruit |

---

## Hors périmètre (maintenu)

Panier · checkout · prix · promo · pack · moteur catalogue · refonte UX · collections Lot B · sitemap XML custom v1.

---

## Non-régression exigée

| Suite | Attendu |
|-------|---------|
| `dorevia_marketone_lot6_1_featured` | OK |
| `dorevia_marketone_lot6_2_origin` | OK |
| `dorevia_marketone_lot6_3a_promo` | OK |
| `dorevia_marketone_lot6_3b_pack` | OK |
| `dorevia_marketone_seo_portes_shop` | OK |

---

## Verdict

| Date | Verdict |
|------|---------|
| 2026-06-08 | **GO MOA D1–D6** · implémentation SEO portes autorisée |
