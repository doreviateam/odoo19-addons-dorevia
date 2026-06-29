# Verdict — Recette QA Breadcrumb-U1 + fiche produit CK

| Champ | Valeur |
| --- | --- |
| Date recette MOA/QA | 29 juin 2026 |
| Référence | Breadcrumb-U1 · fiche produit CK (Note 08 / layout achat) |
| Base | `dorevia_ck_marketone_01` · sandbox Docker · http://localhost:18079 |
| Module | `dorevia_ck_theme` **19.0.1.94.0** (recette initiale sur 93.0, corrigée puis bump 94.0 post-fix XPath) |
| Navigateur | Chromium local / navigateur intégré Codex |
| Viewports | Desktop **1440×900** · Mobile **390×844** |
| Tag tests Odoo | `dorevia_ck_breadcrumb_u1` · `dorevia_ck_shop_s1` · non-régression `dorevia_ck_product_page_note08_recette` |

---

## Verdict global

| Lot | Résultat |
| --- | --- |
| **Breadcrumb-U1** | **GO** |
| **Fiche produit CK — desktop** | **GO** |
| **Fiche produit CK — mobile 390** | **GO** |
| **Variantes produit** | **GO** |
| **Wishlist compteur header** | **KO** → ticket **Wishlist-U1** (hors périmètre Breadcrumb-U1) |

---

## 1. Breadcrumb-U1

| Critère | Résultat | Détail |
| --- | --- | --- |
| Icône maison racine catalogue | ✅ | `fa-home`, lien `/shop` |
| Accessibilité | ✅ | `aria-label`, `title`, `aria-hidden` sur icône, `visually-hidden` |
| Absence libellés EN natifs | ✅ | Pas de `Products` / `All Products` |
| `/shop` sans catégorie | ✅ | Aucun breadcrumb (conforme spec) |
| Catégories testées | ✅ | `/shop/category/epicerie-1`, `/shop/category/epicerie-confitures-184` |
| Fiches produit testées | ✅ | `/shop/confiture-de-goyave-3`, `/shop/manio-crackers-4?attribute_values=2` |

**Nuance Odoo 19 :** `/shop?categ_id=…` n’active pas une catégorie — utiliser `/shop/category/<slug>`.

**Bug bloquant corrigé avant GO :** XPath initial sur `href="/shop"` incompatible avec le natif `t-att-href="keep(shop_path)"` → remplacement du 1er `li.breadcrumb-item` (voir `website_sale_breadcrumb.xml`).

---

## 2. Fiche produit CK — desktop (1440×900)

| Critère | Résultat |
| --- | --- |
| Layout 2 colonnes (image gauche / achat droite) | ✅ |
| Titre, prix, CTA, quantité, favori visibles | ✅ |
| Pas d’overflow horizontal | ✅ |
| Pas de chevauchement | ✅ |

**Produits couverts :** Confiture de goyave · Manio Crackers · Jus Mont-Pelé · Pâte de manioc · Savon vétiver.

**Cas galerie :** Pâte de manioc — 4 visuels, galerie multi-images OK.

---

## 3. Fiche produit CK — mobile (390×844)

| Critère | Résultat |
| --- | --- |
| Pas d’overflow horizontal | ✅ |
| Image adaptée à la largeur | ✅ |
| Bloc achat lisible | ✅ |
| CTA panier + quantité visibles | ✅ |
| Favori produit visible | ✅ |
| Breadcrumb replié / layout stable | ✅ |

**Produits couverts :** Confiture de goyave · Manio Crackers · Pâte de manioc.

---

## 4. Variantes

| Critère | Résultat |
| --- | --- |
| URL testée | `/shop/manio-crackers-4?attribute_values=2` |
| Bloc « Saveur » visible | ✅ |
| Variante salée active par défaut | ✅ |
| Bascule vers sucré | ✅ — URL `attribute_values=3`, prix `3,50 €` |

---

## 5. Hors périmètre — Wishlist-U1 (KO à traiter)

| Scénario | Résultat |
| --- | --- |
| Utilisateur **connecté** | ✅ Compteur OK après ajout, refresh, retrait |
| Visiteur **non connecté** | ❌ Compteur passe à `1` après ajout, **revient à `0` après refresh** |

**Action :** ouvrir ticket **Wishlist-U1** — aucun correctif dans le lot Breadcrumb-U1.

---

## Tests automatisés (complément recette manuelle)

| Suite | Résultat |
| --- | --- |
| `dorevia_ck_breadcrumb_u1` | 3 scénarios HTTP — vert |
| `dorevia_ck_shop_s1` | Non-régression shop — vert |

---

## Recommandation MOA

**Valider Breadcrumb-U1 en production** avec `dorevia_ck_theme` **≥ 19.0.1.94.0**.

La recette fiche produit CK (desktop + mobile + variantes) est **GO** sur l’état sandbox actuel.

**Ne pas bloquer** Breadcrumb-U1 sur le KO wishlist visiteur — sujet isolé Wishlist-U1.
