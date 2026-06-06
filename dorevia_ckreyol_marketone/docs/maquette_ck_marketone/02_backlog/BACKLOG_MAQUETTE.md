# Backlog maquette CK Marketone

File vivante : une iteration = un ID. Statuts : `todo` · `maquette` · `arbitrage` · `odoo` · `fait` · `pause`

**Doctrine** : toute iteration respecte le premium Odoo MOA — voir [CADRAGE_PREMIUM_MAQUETTE_ODOO.md](../00_brief/CADRAGE_PREMIUM_MAQUETTE_ODOO.md).

## En cours

| ID | Sujet | Statut | Notes |
|----|-------|--------|-------|
| — | Piste 1 base (scroll complet) | `fait` | Exploration structure · **couleurs non prod** |
| **M-05** | **Alignement premium Odoo (tokens + typo)** | `todo` | **P0 — gate avant autres iterations visuelles** |

## Prochaines iterations (priorite suggeree)

| ID | Sujet | Statut | Zone | Effort |
|----|-------|--------|------|--------|
| M-05 | Piste 1 bis : `$ck-*` + Garamond/Hanken · export `piste_1bis_artisanal_terroir/` | `todo` | Global | M |
| M-01 | Drawer navigation mobile (Boutique / Culture / Savoirs) | `todo` | Header | S |
| M-02 | Page ou section **Savoirs** (recettes, vocabulaire) | `todo` | Nouvelle section | M |
| M-03 | Empty state boutique (0 resultat filtre) | `todo` | `#boutique` | S |
| M-04 | Empty panier + message retour shop | `todo` | `#checkout` | S |
| M-06 | Tuile : bouton « Voir » / preview (alignement UX4 Odoo) | `todo` | Grille produit | S |
| M-07 | Fiche : galerie photo realiste (ratio, pas gradient seul) | `todo` | `#produit` | S |
| M-08 | Accueil : lien direct collections / origines | `todo` | `#accueil` | S |
| M-09 | Culture : maquette portail (pas seulement strip) | `todo` | `#culture` | L |
| M-10 | Checkout : code promo + frais livraison explicites | `todo` | `#checkout` | S |

## Alignement Odoo (apres arbitrage maquette)

| ID | Sujet | Statut | Fichiers Odoo cibles |
|----|-------|--------|----------------------|
| O-01 | Harmoniser CTA primary maquette → `$ck-terracotta` / sauge | `pause` | `_buttons.scss`, `_tokens_colors.scss` |
| O-02 | Header chrome : search + icons comme maquette | `pause` | `_header.scss` |
| O-03 | Filter pills : rendu maquette vs `_shop_filter_state.scss` | `pause` | `_shop_filter_state.scss` |

## Journal des iterations

| Date | ID | Action | Export |
|------|-----|--------|--------|
| 2026-06-01 | piste-1 | Generation initiale Open Design + sync repo | `piste_1_marche_creole_contemporain/` |

---

Pour lancer une iteration : copier l'ID (ex. `M-01`) dans le prompt ou demander a Cursor « prepare M-01 ».
