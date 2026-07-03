# Note MOA — Clôture CK-HOME-POLISH-001 — Corrections UX Home avant ouverture

| Champ | Valeur |
| --- | --- |
| Date | 2 juillet 2026 |
| Projet | C-Kréyòl Marketone — home |
| Destinataires | MOA, Produit, QA, Dev |
| Statut | **Clôturé GO exploitation démo** |
| Module contenu | `dorevia_ck_marketone_content` **19.0.1.80.0** |
| Module thème | `dorevia_ck_theme` **19.0.1.116.0** |
| Base recette | `dorevia_ck_marketone_01` |
| URL locale | http://localhost:18079 |
| URL démo publique | https://basename-prev-keith-panels.trycloudflare.com |

---

## Objet

Micro-lot de polish UX ciblé sur la Home CK, sans remise en cause de la structure validée (hero, vedettes, univers, coffrets, bloc pro, footer).

---

## Livrables validés

| Priorité | Sujet | Résultat |
| --- | --- | --- |
| P0 | Newsletter non fonctionnelle retirée de la Home | Plus de message « Merci pour votre inscription ! » · pas de formulaire trompeur |
| P0 | Header wishlist / panier | Cœur + panier distincts · badges masqués à zéro |
| P1 | Hero | Impact visuel renforcé · wording MOA inchangé |
| P1 | Prix cards vedettes | 15 px / graisse 700 · métadonnées conservées |
| P2 | Trust-bar | Lisibilité améliorée · 4 promesses visibles |
| P2 | Bloc Professionnels | Wording + CTA « Demander un accès professionnel » · aucun chiffre inventé |
| P3 | Alt images | Reporté — audit SEO/accessibilité séparé |

---

## Recette

### Recette principale (MOA / QA)

| Contrôle | Résultat |
| --- | --- |
| Home desktop 1280 | OK |
| Home mobile 390 | OK · pas d'overflow |
| Header cœur / panier | OK |
| Tunnel public Cloudflare | OK |
| Routes `/shop`, `/shop/wishlist`, `/shop/cart`, `/professionnels` | 200 |
| CTA Coffrets → `/kits` | OK → `/shop?marketone_mode=pack` |

### Addendum QA post-GO (§ 7 livraison)

| Contrôle | Résultat |
| --- | --- |
| Viewport 375 px (iPhone SE) | OK |
| Firefox desktop (Gecko) | OK |
| Cycle badge favoris | OK — tests Odoo `dorevia_ck_wishlist_u1` (3/3) |
| Route `/kits` | OK fonctionnel · `301` pack · absent sitemap |

---

## Réserves — non bloquantes

| Sujet | Décision |
| --- | --- |
| Canonical pack (`/shop?marketone_mode=pack`) | Vigilance **SEO future** — canonical générique `/shop` en sandbox |
| Wishlist hors session Odoo (Playwright externe) | Vigilance **technique sandbox** — couvert par tests HttpCase Odoo |
| Newsletter CK (Email Marketing, RGPD) | Lot futur dédié |

**Aucune réserve bloquante ne subsiste.**

---

## Verdict

```text
CK-HOME-POLISH-001 — CLÔTURÉ GO EXPLOITATION DÉMO

La Home CK est validée après correction des irritants P0/P1/P2.
L'addendum QA post-GO confirme les contrôles complémentaires.
Les points canonical pack et observation wishlist hors session Odoo
sont reportés en vigilance technique / SEO future.
```

> Livraison détaillée : [`NOTE_MOA_LIVRAISON_CK_HOME_POLISH_001_20260702.md`](NOTE_MOA_LIVRAISON_CK_HOME_POLISH_001_20260702.md)

---

*Note MOA — C-Kréyòl Marketone · Clôture CK-HOME-POLISH-001 — 2 juillet 2026*
