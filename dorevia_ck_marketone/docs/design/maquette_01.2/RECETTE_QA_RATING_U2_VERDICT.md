# Verdict — Recette QA Rating-U2 · Note compacte cards Shop + Home

| Champ | Valeur |
| --- | --- |
| Date recette Dev/QA | 28 juin 2026 |
| Référence | Rating-U2 — Livraison (note cards ★ 4,8 · 12 avis) |
| Base | `dorevia_ck_marketone_01` · sandbox Docker `sandbox-odoo19-odoo-1` |
| Modules livrés | `dorevia_ck_theme` **19.0.1.92.0** · `dorevia_ck_marketone_content` **19.0.1.59.0** |
| Tag tests Odoo | `dorevia_ck_shop_card` (+ non-régression `dorevia_ck_product_page_note08_recette`) |
| **QA** | Cursor Agent — 28 juin 2026 |

---

## Verdict QA

| Résultat | Choix |
| --- | --- |
| GO fonctionnel | ☑ |
| GO avec réserves | ☐ |
| NO GO | ☐ |

**Motif :** L’implémentation Rating-U2 est **conforme** après correction d’un bug bloquant ACL (voir BUG-U2-001). **22/22** tests `dorevia_ck_shop_card` et **16/16** tests Rating-U1 passent. Shop et Home partagent le même format FR, la même accessibilité de base et le pattern Odoo `sudo()` pour la note moyenne.

**Date :** 28 juin 2026

---

## Bug identifié et corrigé en recette

### BUG-U2-001 — 403 `/shop` pour visiteur public si produit noté

| Champ | Valeur |
| --- | --- |
| Sévérité | **Bloquante** |
| Fichier | `dorevia_ck_theme/views/website_sale_product_card.xml` |
| Cause | `product.rating_avg` lu sans `sudo()` — le visiteur public n’a pas le droit de lecture sur ce champ (`rating` mixin). Dès qu’un produit avait `rating_count > 0`, la page `/shop` renvoyait **403 Interdit**. |
| Correction | Alignement sur le canon Odoo 19 (`product_tile_templates.xml`) : `product.sudo().rating_avg` dans le calcul `ck_rating_fmt`. |
| Version | `dorevia_ck_theme` **19.0.1.91.0 → 19.0.1.92.0** |
| Statut | ✅ **Corrigé** — test HTTP `test_rating_u2_shop_card_with_reviews` vert |

---

## Livrables validés

| Zone | Fichier | Contrôle |
| --- | --- | --- |
| Shop QWeb | `dorevia_ck_theme/views/website_sale_product_card.xml` | Vue `products_item_ck_card_rating` (priority 48), `t-if="product.rating_count > 0"`, xpath `o_wsale_product_information_text` |
| Shop SCSS | `dorevia_ck_theme/static/src/scss/product_card.scss` | `.ck-card-rating` + enfants |
| Home SSR | `dorevia_ck_marketone_content/home_featured.py` | `_build_featured_rating_html()` + injection `{rating_html}` dans `build_featured_product_card_html()` |
| Bootstrap home | `migrations/19.0.1.59.0/post-migrate.py` | Appelle `bootstrap_home_featured_products(env)` au upgrade |
| Tests | `tests/test_ck_shop_product_card.py` | 5 scénarios Rating-U2 (vue, unit HTML, shop HTTP, home HTTP) |

---

## Grille de recette MOA (8 scénarios)

| # | Scénario | Attendu | Statut | Preuve |
| --- | --- | --- | --- | --- |
| 1 | Card shop — produit avec avis | ★ 4,8 · 12 avis visible, bien positionné | ✅ | `test_rating_u2_shop_card_with_reviews` — HTML public `/shop` |
| 2 | Card shop — produit sans avis | Rien, pas d’espace mort | ✅ | `t-if="product.rating_count > 0"` + `test_rating_u2_shop_card_without_reviews` |
| 3 | Grille mixte | Hauteur homogène (`h-100`), pied ancré | ✅🔶 | `oe_product_cart h-100` natif conservé ; validation visuelle grille mixte recommandée MOA |
| 4 | Mobile 390 px | Note lisible, CTA intact, pas d’overflow | 🔶 | SCSS compact 12 px ; pas de script 390 px exécuté dans cette passe |
| 5 | Lecteur d’écran | « Note 4,8 sur 5, 12 avis » | ✅🔶 | `visually-hidden` + `aria-hidden` sur ★ — conforme au code ; spot-check VoiceOver/NVDA MOA |
| 6 | Locale FR | Virgule décimale (4,8), pas de `.0` | ✅ | `('%g' % round(avg, 1)).replace('.', ',')` — `test_rating_u2_featured_rating_html` |
| 7 | Home Coups de cœur | Idem scénarios 1–2 après bootstrap | ✅ | `test_rating_u2_home_featured_with_reviews_after_bootstrap` + migration post-upgrade |
| 8 | Badges, wishlist, toolbar | Inchangés | ✅ | Non-régression `test_shop_home_wishlist_non_regression` + lot card existant |

**Légende :** ✅ validé auto · ✅🔶 validé code + spot-check MOA recommandé · 🔶 validation manuelle MOA uniquement

---

## Point opérationnel — Home (frozen content)

Les cards home sont **SSR-freezées** dans l’arch de la page. Toute modification de `home_featured.py` nécessite un rebootstrap :

```python
# Shell Odoo (sandbox recette) :
from odoo.addons.dorevia_ck_marketone_content.home_featured import bootstrap_home_featured_products
bootstrap_home_featured_products(env)
```

En **upgrade module** `19.0.1.59.0`, la migration `post-migrate.py` exécute cet appel automatiquement.

**Message QA sandbox :** après déploiement manuel sans migration, lancer le bootstrap ci-dessus avant de valider le scénario 7.

---

## Tests automatisés

| Suite | Résultat |
| --- | --- |
| `dorevia_ck_shop_card` | **22/22** — 0 failed |
| `dorevia_ck_product_page_note08_recette` (Rating-U1) | **16/16** — 0 failed |

Commande recette :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 --test-enable --stop-after-init \
  --http-port=8078 --test-tags dorevia_ck_shop_card
```

---

## Architecture retenue (confirmée)

| Surface | Mécanisme | Condition affichage |
| --- | --- | --- |
| `/shop` + catégories | Héritage QWeb `website_sale.products_item` | `rating_count > 0` uniquement |
| Home Coups de cœur | Python `build_featured_product_card_html()` | Chaîne vide si `rating_count == 0` |

Format partagé : `★ {note} · {n} avis` — note FR sans zéro traînant (`5` pas `5,0`).

---

## Hors périmètre U2 (inchangé)

- Chips filtres avis (Chips-U1)
- Pseudonymisation auteur avis
- JSON-LD `aggregateRating`
- Modération custom → V2

---

## Recommandation MOA

**Valider Rating-U2 en production** après upgrade `dorevia_ck_theme` **≥ 19.0.1.92.0** (correctif ACL obligatoire) et `dorevia_ck_marketone_content` **≥ 19.0.1.59.0**.

Contrôles manuels rapides suggérés (5 min) :

1. `/shop` — produit noté : ligne rating visible sous le titre
2. `/shop` — produit sans avis : pas de ligne rating
3. `/` — section Coups de cœur : même rendu après upgrade
4. Mobile 390 px — pas de régression CTA panier
