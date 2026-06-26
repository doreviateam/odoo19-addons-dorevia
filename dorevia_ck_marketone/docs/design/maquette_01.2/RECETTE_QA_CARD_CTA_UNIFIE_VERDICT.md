# Verdict — Recette Cards Produit CK · CTA unifié Home / Boutique

| Champ | Valeur |
| --- | --- |
| Date | 26 juin 2026 |
| Base | `dorevia_ck_marketone_01` · `http://localhost:18079` |
| Exécutant | Dev / QA (automatisé + recette écran/fonctionnelle) |
| Modules | `dorevia_ck_theme` **19.0.1.65.0** · `dorevia_ck_marketone_content` **19.0.1.46.0** |
| Référence ticket | [`TICKET_DEV_CARD_CTA_UNIFIE_CK.md`](../../cadrage/TICKET_DEV_CARD_CTA_UNIFIE_CK.md) |
| Résultat global | **GO technique QA** |

**Preuves** :
- Rapport JSON : [`captures/card_cta_unifie_20260626/card_cta_unifie_results.json`](captures/card_cta_unifie_20260626/card_cta_unifie_results.json) (`technicalPass: true`, `failures: []`)
- Captures écran : `captures/card_cta_unifie_20260626/` (post-correctif **65.0**)

---

## 0. Historique recette

| Version | Verdict | Motif |
| --- | --- | --- |
| **19.0.1.64.0** | **NO GO** | CTA `visibility: hidden` < 992 px · grille 4 cols à 800 px · 2 cols à 390 px |
| **19.0.1.65.0** | **GO technique** | Correctif responsive CTA + grille `4 → 2 → 1` validé |

---

## 1. Prérequis

| # | Contrôle | Résultat |
| --- | --- | --- |
| P1 | Note 07 clôturée (GO technique) | ✅ |
| P2 | Upgrade `dorevia_ck_theme` | ✅ `19.0.1.65.0` (DB confirmée) |
| P3 | `website.shop_ppr = 4` | ✅ |
| P4 | Worker redémarré + hard refresh | ✅ |

**Tests auto (gate large)** : **44/44 · 0 failed · 0 error**

Tags : `dorevia_ck_shop_card`, `dorevia_ck_shop_s1`, `dorevia_ck_shop_note07_tiles`, `dorevia_ck_shop_note07_rebound`.

**Playwright** : `technicalPass: true` · `failureCount: 0`.

---

## 2. Synthèse livrable

| Objectif | Résultat |
| --- | --- |
| CTA texte « Ajouter au panier » (canon Home) | ✅ Desktop 1280 |
| Grille 4 colonnes desktop | ✅ `/shop` + Épicerie |
| CTA visible tablette 800 px | ✅ Hauteur 44 px |
| Grille 2 colonnes tablette | ✅ `/shop` + Épicerie |
| CTA visible mobile 390 px | ✅ Hauteur 44 px |
| Grille 1 colonne mobile | ✅ Pas d'overflow horizontal |
| Catégories pauvres (rebond) | ✅ Boissons / Soin / Artisanat |
| Non-régression Note 07 | ✅ Sidebar masquée · drawer · toolbar |

---

## 3. Contrôles fonctionnels

| Contrôle | Résultat |
| --- | --- |
| Ajout panier grille (`0 → 1`) | ✅ |
| Wishlist | ✅ |
| Filtre actif `/shop?tags=283` | ✅ |
| Fiche produit | ✅ |
| Panier / checkout | ✅ |
| Logs `dorevia_ck_marketone_01` | ✅ Aucun `ERROR` / `Traceback` / `QWeb` / `500` |

---

## 4. Réserves MOA (non bloquantes)

| # | Sujet | Statut |
| --- | --- | --- |
| R1 | Tuile « Jus de fruits » sur Boissons | Conforme helper Lot B si enfant direct publié — arbitrage catalogue MOA |
| R2 | Pagination (> 20 produits) | N/A — seed sans état pagination |
| R3 | Catégorie vide | N/A — pas de slug vide stable |

---

## 5. Fichiers livrés (65.0)

| Fichier | Rôle |
| --- | --- |
| `views/website_sale_product_card.xml` | Libellé CTA visible |
| `static/src/scss/website_sale.scss` | CTA pill · responsive CTA visibility · grille 4/2/1 |
| `data/website_shop_grid.xml` | `shop_ppr = 4` |
| `tests/test_ck_shop_structure_s1.py` | Assertion grille 4 cols |
| `dorevia_ck_marketone_content/tests/test_ck_shop_product_card.py` | CTA + grille |

---

## Verdict MOA

```text
Date    : 26 juin 2026
Verdict : GO technique QA
Version : dorevia_ck_theme 19.0.1.65.0
```

Ticket **CTA unifié Cards Produit CK** : **clôturé technique**. Prochaine étape produit : raffinements pages pauvres / rebond / toolbar (séquencement ticket §7).

---

*Verdict recette — 26 juin 2026 — sandbox `dorevia_ck_marketone_01`*
