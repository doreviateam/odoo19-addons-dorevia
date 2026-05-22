# Note d’arbitrage MOA — UX-4 Lot 3ter · Clic image tuile → preview

| Champ | Valeur |
|-------|--------|
| **Statut** | **Validé Dev** — en attente recette MOA |
| **Date** | 2026-05-22 |
| **Prérequis** | Lot 3bis **GO** · version réf. **`19.0.15.13.4`** |
| **Ticket** | [`TICKET_MARKETONE_UX4_SHOP_IN_PLACE.md`](TICKET_MARKETONE_UX4_SHOP_IN_PLACE.md) |
| **Recette** | § **Lot 3ter** [`RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md`](../recette/ux/RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md) |
| **Version cible** | **`19.0.15.13.5`** |
| **Branche** | `feat/marketone-ux4-lot3ter-image-preview-click` |
| **PR cible** | `[CK][UX-4] Lot 3ter — Clic image tuile → preview` |

---

## 1. Contexte MOA

L’image produit est la zone naturelle d’exploration. Depuis le GO preview Lot 3 / 3bis, le CTA **Voir** ouvre la mini-fiche in-page. MOA demande d’**aligner le clic image** sur ce comportement, tout en conservant le **titre** comme lien fiche complète.

**PR #16 mergée** — ce point est traité en **Lot 3ter isolé**.

---

## 2. Arbitrage figé

| Zone clic | Comportement |
|-----------|--------------|
| **Image tuile** (hors overlays) | **Preview in-page** — identique CTA **Voir** |
| **Bouton panier** overlay | **Ajout panier in-place** (Lot 2) — inchangé |
| **Bouton wishlist** overlay | **Toggle wishlist** (Lot 1) — inchangé |
| **Titre produit** | **Lien fiche complète** — inchangé |
| **CTA Voir** | Preview — inchangé |
| **Produit configurable / fallback** | Navigation fiche (href conservé) |

**Invariants :** URL `/shop` · offcanvas non modal desktop · inline mobile · pas deep-link · pas configurateur · pas modal.

---

## 3. Solution technique (légère)

| Couche | Détail |
|--------|--------|
| **QWeb** | `form.oe_product_cart` — `data-product-template-id` · `data-marketone-preview-allowed` (partagés avec CTA) |
| **JS** | Extension `marketone_shop_preview.js` — selector `.oe_product_image` + handler partagé · garde-fous overlays panier/wishlist · clic limité à la zone photo |
| **SCSS** | `cursor: pointer` sur lien image si preview autorisée |

**Non impactés :** routes · panier handler · wishlist handler · preview fragment · titre tuile.

---

## 4. Recette MOA

§ **V3ter.1–V3ter.8** dans [`RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md`](../recette/ux/RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md).

Smoke obligatoire : **G3.6–G3.9** · **G3.1** · **G3.3** · Lots 1–2 panier/wishlist.

---

## 5. Verdict

| Verdict | Condition |
|---------|-----------|
| **GO MOA Lot 3ter** | V3ter OK · smoke non-régression OK |
| **NO GO** | Régression panier / wishlist / titre / preview |

---

## 6. Historique

| Date | Événement |
|------|-----------|
| 2026-05-22 | Arbitrage MOA clic image → preview |
| 2026-05-22 | Implémentation Lot 3ter · branche autorisée post-PR #16 |
