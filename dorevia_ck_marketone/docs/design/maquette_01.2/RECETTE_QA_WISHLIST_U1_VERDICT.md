# Verdict — Recette QA Wishlist-U1 · Compteur favoris header visiteur

| Champ | Valeur |
| --- | --- |
| Date recette Dev/QA | 29 juin 2026 |
| Référence | Wishlist-U1 — compteur header KO après refresh (visiteur) |
| Base | `dorevia_ck_marketone_01` |
| Module | `dorevia_ck_theme` **19.0.1.95.0** |
| Tag tests Odoo | `dorevia_ck_wishlist_u1` (+ non-régression `dorevia_ck_header_v22`) |

---

## Verdict QA

| Résultat | Choix |
| --- | --- |
| GO fonctionnel | ☑ |
| GO avec réserves | ☐ |
| NO GO | ☐ |

---

## Cause racine (BUG-WL-U1-001)

| Champ | Valeur |
| --- | --- |
| Sévérité | Bloquante UX visiteur |
| Fichier | `website_sale_wishlist/controllers/main.py` (Odoo natif) |
| Symptôme | Compteur `1` après ajout, `0` après refresh (visiteur) |
| Cause | `add_to_wishlist` enregistre `wishlist_ids` en session **sans** `session.touch()`, contrairement au retrait. Le cookie de session n’est pas persisté ; au reload le SSR rend `0` et `WishlistNavbar.willStart()` synchronise `sessionStorage` depuis le serveur (vide). |
| Correction CK | `dorevia_ck_theme/controllers/website_sale_wishlist.py` — override `add_to_wishlist` + `request.session.touch()` pour visiteur public |

---

## Scénarios QA

| # | Scénario | Statut |
| --- | --- | --- |
| A | Visiteur — add → refresh → compteur `1` | ✅ `test_anonymous_wishlist_header_count_persists_after_reload` |
| A | Visiteur — remove → refresh → compteur `0` | ✅ `test_anonymous_wishlist_remove_resets_counter_after_reload` |
| B | Connecté — add → refresh → compteur conservé | ✅ `test_logged_user_wishlist_header_count_after_reload` |
| — | Header CK non régressé | ✅ `dorevia_ck_header_v22` |

**Tests :** 3/3 Wishlist-U1 · 17/17 header v22 — **20/20** au total sur la passe combinée.

---

## Hors périmètre (inchangé)

Breadcrumb-U1 · fiche produit · variantes · panier · refonte header.

---

## Recommandation MOA

**GO Wishlist-U1** avec `dorevia_ck_theme` **≥ 19.0.1.95.0**.

La réserve isolée de la recette Breadcrumb-U1 + fiche produit est **levée** pour ce point.
