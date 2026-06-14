# Reprise lots front gelés — Cadrage2 post ADR-034

| Champ | Valeur |
|-------|--------|
| **ADR** | [ADR-034](../cadrage/DECISIONS.md#adr-034--arbitrage-architecture-cadrage2-socle-odoo-natif) |
| **Arbitrage** | [`ARBITRAGE_ARCHITECTURE_CADRAGE2.md`](./ARBITRAGE_ARCHITECTURE_CADRAGE2.md) |
| **Doctrine** | **Odoo exécute. Marketone habille et oriente.** |
| **Statut** | **Autorisé MOA** — lot par lot (D5) |
| **Date** | 2026-06-08 |

---

## 1. Condition de reprise

La reprise d'un lot front gelé est autorisée **si et seulement si** :

1. Le ticket cite **ADR-034** ;
2. La recette inclut la ligne **« Fonctionnalité Odoo native préservée »** (§2) ;
3. La recette référence la **matrice eCommerce** ([ARBITRAGE §5](./ARBITRAGE_ARCHITECTURE_CADRAGE2.md#5-matrice--fonctionnalités-odoo-ecommerce-à-préserver)) ;
4. Les tests auto + [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md) § B sont rejoués.

---

## 2. Ligne obligatoire en tête de recette (template)

À copier en tête de **chaque** nouvelle recette manuelle front post-cadrage2 :

```markdown
**ADR-034 :** [`ARBITRAGE_ARCHITECTURE_CADRAGE2.md`](../cadrage2/ARBITRAGE_ARCHITECTURE_CADRAGE2.md)

**Fonctionnalité Odoo native préservée :** [catégorie matrice §5 — ex. « Panier · Wishlist · Variantes »]

**Mécanisme Odoo concerné :** [ex. `website_sale` cart · `website_sale_wishlist` · `product.template` variant picker]

**Non-régression référence boutique :** [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md) — sections B__
```

### Exemples remplis

| Lot type | Fonctionnalité Odoo native préservée | Mécanisme |
|----------|--------------------------------------|-----------|
| UX wishlist | Wishlist | `website_sale_wishlist` — pas de modèle CK |
| UX preview grille | Variantes (simples) | Configurateur natif non contourné sur fiches multi-variantes |
| Sidebar filtres | Catégories · Attributs | `product.public.category` · filtres attributs Odoo |
| Lot promo / pack | Listes de prix · Promotions | `product.pricelist` · règles promo Odoo — **pas** de filtre prix custom |

---

## 3. Checklist ticket (avant implémentation)

- [ ] Quelle ligne de la **matrice §5** est concernée ?
- [ ] Le lot **hérite** du template / contrôleur Odoo standard (F1–F9) ?
- [ ] Aucun tunnel checkout / panier / prix / promo / paiement / livraison parallèle ?
- [ ] Aucune dépendance `website_blog` / `website_forum` ajoutée ?
- [ ] Recette avec ligne §2 + non-régression REFERENCE_RECETTE_BOUTIQUE ?

---

## 4. Checklist livraison (avant GO MOA)

- [ ] Tests auto du ticket **verts** (écarts documentés si réserve).
- [ ] [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md) — sections impactées rejouées.
- [ ] Confirmation explicite dans la note de livraison : **« aucun moteur Odoo remplacé »**.
- [ ] Bump version module + recette manuelle datée.

---

## 5. Lots front gelés — repères connus

| Zone | État avant gel | Reprise |
|------|----------------|---------|
| UX-4 preview in-place | Livré partiellement | Corrections / régression uniquement sauf ticket MOA |
| UX-4 CTA tuile / panier | Livré partiellement | Idem |
| Lot 6.3a promo | Livré `19.0.17.0.0` | **GO MOA clôturé** — [`RECEPTION_MOA_LOT6_3A_PROMO.md`](../cadrage2/RECEPTION_MOA_LOT6_3A_PROMO.md) |
| Lot 6.3b Kits & Coffrets | Livré `19.0.18.0.0` | **GO MOA clôturé** — [`RECEPTION_MOA_LOT6_3B_PACK.md`](../cadrage2/RECEPTION_MOA_LOT6_3B_PACK.md) |
| SEO portes `/shop` | Documenté, non implémenté | **Cadrage ouvert** — [`TICKET_MARKETONE_SEO_PORTES_SHOP.md`](../tickets/boutique/TICKET_MARKETONE_SEO_PORTES_SHOP.md) · [`CADRAGE_SEO_PORTES_SHOP.md`](./CADRAGE_SEO_PORTES_SHOP.md) |

---

## 6. Backlog séparé (non bloquant reprise front)

| Sujet | Ticket |
|-------|--------|
| Test import JPEG pilote | [`TICKET_MARKETONE_TEST_T5_IMPORT_JPEG_PILOTE.md`](../tickets/maintenance/TICKET_MARKETONE_TEST_T5_IMPORT_JPEG_PILOTE.md) |

---

## Documents liés

| Document | Rôle |
|----------|------|
| [`ARBITRAGE_ARCHITECTURE_CADRAGE2.md`](./ARBITRAGE_ARCHITECTURE_CADRAGE2.md) | Matrice eCommerce · règles F1–F9 |
| [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md) | Anti-régression `/shop` |
| [`DECISION_MOA_RECADRAGE_BO.md`](./DECISION_MOA_RECADRAGE_BO.md) | Gel front initial (levé par ADR-034 D5) |
