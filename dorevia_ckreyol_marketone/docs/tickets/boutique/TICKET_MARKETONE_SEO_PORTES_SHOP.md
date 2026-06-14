# TICKET — SEO portes `/shop` Marketone

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_SEO_PORTES_SHOP` |
| **Statut** | **GO MOA D1–D6** · implémentation **19.0.19.0.0** |
| **Décision** | [`DECISION_MOA_SEO_PORTES_SHOP.md`](../../cadrage2/DECISION_MOA_SEO_PORTES_SHOP.md) |
| **Priorité MOA** | **Haute** — reprise post-clôture filière pack |
| **Cadrage** | [`CADRAGE_SEO_PORTES_SHOP.md`](../../cadrage2/CADRAGE_SEO_PORTES_SHOP.md) |
| **Module** | `dorevia_ckreyol_marketone` |
| **ADR** | ADR-034 · CONTRACTS C2 · C9 |
| **Version cible** | **19.0.19.0.0** |

---

## Contexte

Lots portes **6.1 · 6.2 · 6.3a · 6.3b** livrés et clôturés MOA. SEO `canonical` / `noindex` était **documenté sans implémentation** (réserve M6 de chaque lot).

Filière **`sale_product_pack`** **clôturée** — doctrine pack = article · `non_detailed`. Reprise prioritaire : **SEO portes `/shop`**.

---

## Doctrine

```text
/shop reste le conteneur catalogue unique.
Les alias restent des entrées 301.
Marketone ne crée pas de pages catalogue autonomes.
Odoo exécute. Marketone habille et oriente.
```

---

## Objectif

Sécuriser les URLs des portes Marketone déjà livrées :

| Alias **301** | URL canonique |
|---------------|---------------|
| `/incontournables` | `/shop?marketone_mode=featured` |
| `/origines` | `/shop?marketone_mode=origin` |
| `/promotions` | `/shop?marketone_mode=promo` |
| `/kits` | `/shop?marketone_mode=pack` |

+ règles **`/shop`** nu · facette **`marketone_origin`**.

---

## Livrables

| # | Livrable |
|---|----------|
| 1 | Cadrage SEO **canonical** / **noindex** — [`CADRAGE_SEO_PORTES_SHOP.md`](../../cadrage2/CADRAGE_SEO_PORTES_SHOP.md) |
| 2 | Décision MOA signée (atelier D1–D6) |
| 3 | Implémentation head tags `/shop` *(extension `website` ou équivalent)* |
| 4 | Tests auto + recette manuelle SEO |
| 5 | Amendement CONTRACTS **C9** / ADR si figé |

---

## Hors périmètre (interdit)

- Modification **panier** · **checkout** · **prix** · **promo** · **pack**
- Moteur catalogue parallèle
- `sale_product_pack` · explosion composants
- Collections Lot B *(ticket séparé)*
- Refonte navigation / chips

---

## Non-régression

| Suite | Attendu |
|-------|---------|
| `dorevia_marketone_lot6_1_featured` | OK |
| `dorevia_marketone_lot6_2_origin` | OK |
| `dorevia_marketone_lot6_3a_promo` | OK |
| `dorevia_marketone_lot6_3b_pack` | OK |
| [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md) | Sections portes rejouées |

---

## Plan de travail

### Phase 1 — Cadrage MOA *(clôturé)*

- [x] Inventaire URLs portes livrées
- [x] Proposition règles canonical / noindex
- [x] **Atelier MOA** — D1–D6 validés
- [x] **Décision MOA** — [`DECISION_MOA_SEO_PORTES_SHOP.md`](../../cadrage2/DECISION_MOA_SEO_PORTES_SHOP.md)

### Phase 2 — Exécution Dev *(livré)*

- [x] Extension canonical / robots sur `/shop`
- [x] Normalisation params whitelist (**C9.1**)
- [x] Tests auto SEO portes — tag `dorevia_marketone_seo_portes_shop`

### Phase 3 — Recette MOA

- [ ] Recette manuelle head tags (5 portes + alias + origine facettée)
- [ ] Non-régression portes
- [ ] **GO MOA** livraison

---

## Références

| Document | Rôle |
|----------|------|
| [`CADRAGE_SEO_PORTES_SHOP.md`](../../cadrage2/CADRAGE_SEO_PORTES_SHOP.md) | **Cadrage complet** |
| [`TICKET_MARKETONE_CONSOLIDATION_PORTES_BOUTIQUE.md`](./TICKET_MARKETONE_CONSOLIDATION_PORTES_BOUTIQUE.md) | Matrice portes |
| [`REPRISE_LOTS_FRONT_CADRAGE2.md`](../../cadrage2/REPRISE_LOTS_FRONT_CADRAGE2.md) | Reprise lots front |
| [`DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md`](../../cadrage2/DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md) | Filière pack fermée |

---

## Verdict ticket

| Date | Verdict |
|------|---------|
| 2026-06-08 | **GO MOA D1–D6** · dev livré **19.0.19.0.0** · recette MOA Phase 3 en attente |
