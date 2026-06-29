# Release V1.0.0 — Boutique C-Kréyòl

**Date** : 2026-06-29  
**Tag** : `v1.0.0-boutique`  
**Commit** : `d2682ca4`  
**Version thème** : `19.0.1.103.1`  
**Version content** : `19.0.1.63.0`

## État : GO boutique

La partie achat est cohérente et exploitable.  
Le parcours client complet est validé :

> Home → Shop → fiche produit → panier → checkout → confirmation

## Validation live

| Étape | Preuve |
|-------|--------|
| Parcours FR | Commandes S00098, S00099, S00102, S00103 |
| Parcours EN | `/en/shop/cart`, `/en/shop/confirmation` |
| CGV | Case checkout + lien `/terms` |
| Email | Mailpit capture SMTP local |
| Mobile 390px | Tunnel complet sans blocage |

## Modules concernés

- `dorevia_ck_theme` (19.0.1.103.1)
- `dorevia_ck_marketone_content` (19.0.1.63.0)

## Scope validé (tag)

- Parcours Home → Shop → fiche → panier → checkout → confirmation (FR/EN)
- CGV checkout (vue `accept_terms_and_conditions` activée + bootstrap XML)
- SMTP confirmation email (Mailpit local, template `sale_confirmation` actif)
- Polish visuel U1–U4 (cards Home/Shop, rubans sémantiques, mobile 390px, wording)
- i18n `en_GB` panier vide et confirmation (U4b)

**Tests** : 38/38 verts (tags U1–U6, Polish, i18n)

## Dettes non bloquantes

| ID | Description | Priorité |
|----|-------------|----------|
| D1 | Titre Manio : 2 cards variantes Home vs 1 template Shop | V1.1 |
| D2 | Inline ruban Home fallback (Savon vétiver) | V1.1 |
| D3 | Breakpoint grille Home 480–575px | V1.1 |
| D4 | `#top_menu` inefficacité réseau (appel `/shop/wishlist?count=1`) | Backlog |

## Ce qui est hors V1

- Blog, communauté, forum, espace pro
- Filtres avancés, recherche full-text
- Stock dynamique, avis clients
- Upgrade Odoo
- Perfection esthétique

## Prochain sprint

Éditorial (contenu, producteurs, SEO) ou V1.1 technique si une dette devient visible en prod.

## Références

- Note MOA : [`dorevia_ck_marketone/docs/cadrage/NOTE_MOA_CLOTURE_V1_BOUTIQUE_20260629.md`](dorevia_ck_marketone/docs/cadrage/NOTE_MOA_CLOTURE_V1_BOUTIQUE_20260629.md)

---
*Cette release est figée. Ne pas modifier sans ouverture explicite d'un sprint V1.1.*
