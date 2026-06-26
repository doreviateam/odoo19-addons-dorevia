# Verdict — Recette Card Shop · alignement canon Homepage

| Champ | Valeur |
| --- | --- |
| Date | 26 juin 2026 |
| Base | `dorevia_ck_marketone_01` · `http://localhost:18079` |
| Modules | `dorevia_ck_theme` **19.0.1.67.0** · `dorevia_ck_marketone_content` **19.0.1.47.0** |
| Référence | Brief MOA « Alignement Card Shop sur le canon Homepage » |
| Résultat global | **GO technique QA** |

**Preuves** :
- Rapport JSON : [`captures/card_shop_canon_home_20260626/card_shop_canon_home_results.json`](captures/card_shop_canon_home_20260626/card_shop_canon_home_results.json) (`technicalPass: true`, `failures: []`)
- Script : [`scripts/ck_card_shop_canon_home_recette.mjs`](scripts/ck_card_shop_canon_home_recette.mjs)
- Captures : `captures/card_shop_canon_home_20260626/`

---

## 1. Prérequis

| # | Contrôle | Résultat |
| --- | --- | --- |
| P1 | Upgrade sandbox 67.0 / 47.0 | ✅ |
| P2 | Worker redémarré | ✅ |
| P3 | Tests auto `dorevia_ck_shop_card` + `dorevia_ck_shop_s1` | ✅ **22/22** |

---

## 2. Critères d'acceptation (brief MOA)

| Critère | Résultat |
| --- | --- |
| Pas de label origine séparé (`GUADELOUPE` au-dessus du titre) | ✅ `originEyebrowCount: 0` sur toutes les pages shop |
| Méta : `Origine · Producteur · Poids · Prix/kg` | ✅ ex. `Guadeloupe · Komla · 320 g · 17,19 €/kg` |
| Pas de séparateur orphelin / ligne vide | ✅ |
| CTA compact desktop | ✅ largeur ~96 px (réf. Home ~114 px) |
| Prix gauche + CTA droite, même ligne (desktop) | ✅ `sameLineDesktopish: true`, `footColumnish: false` |
| Séparateur horizontal méta / pied | ✅ `hasSeparator: true` |
| Wishlist shop conservée | ✅ (non-régression 65.0) |
| Homepage inchangée | ✅ section vedettes + cards `--home` intactes |
| Mobile 390 px — pas d'overflow | ✅ |
| Mobile 390 px — CTA tactile ≥ 44 px | ✅ hauteur 44 px, pied colonne |
| Toolbar catégorie non cassée | ✅ visible sur `/shop` desktop |

---

## 3. Parité Shop / Home (échantillon Confiture de goyave)

| Mesure | Home | Shop desktop 1280 |
| --- | --- | --- |
| Ligne méta | `Guadeloupe · Komla · 320 g · 17,19 €/kg` | identique |
| CTA largeur | 114 px | 96 px |
| Pied ligne | prix \| CTA | prix \| CTA |
| Hauteur card | 331 px | 377 px |

Écart hauteur résiduel : wishlist + zone image Odoo shop (ratio cover vs contain Home) — **hors périmètre brief**.

---

## 4. Contrôles fonctionnels

| Contrôle | Résultat |
| --- | --- |
| Ajout panier grille (`0 → 1`) | ✅ |
| HTTP 200 — `/shop`, Épicerie, Soin, Artisanat | ✅ |
| Logs récents | ✅ Aucune `ERROR` / `Traceback` / `QWeb` / `500` |

---

## 5. Pages recettées

| Page | Desktop 1280 | Mobile 390 |
| --- | --- | --- |
| Home (non-régression) | ✅ | — |
| `/shop` | ✅ | ✅ |
| `/shop/category/epicerie-1` | ✅ | — |
| `/shop/category/soin-bien-etre-2` | ✅ | — |
| `/shop/category/artisanat-3` | ✅ | ✅ |

---

## Verdict MOA

```text
Date    : 26 juin 2026
Verdict : GO technique QA
Version : dorevia_ck_theme 19.0.1.67.0 · dorevia_ck_marketone_content 19.0.1.47.0
```

Prêt pour **commit + push** sur message suggéré :
`[UX] Aligne la card shop CK sur le canon homepage`

---

*Verdict recette — 26 juin 2026 — sandbox `dorevia_ck_marketone_01`*
