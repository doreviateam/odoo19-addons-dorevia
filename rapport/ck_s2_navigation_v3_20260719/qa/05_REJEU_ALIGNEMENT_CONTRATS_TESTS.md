# Rejeu post-alignement contrats de tests S2

**Date :** 2026-07-19  
**Objectif :** aligner les assertions obsolètes sur le comportement scellé `ck-nav-shop-root` / Accueil, sans toucher au code fonctionnel.

## Scellé fonctionnel inchangé

| | |
|---|---|
| Commit fonctionnel GO QA | `58327b68faa80404a006df7417809bb3953790ea` |
| Diff fonctionnel vs ce SHA | **vide** (tests + `rapport/` uniquement) |

## Corrections de tests

1. `test_catalogue_nav_no_legacy_css` — autorise `ck-nav-shop-root` ; interdit les marqueurs V1/V2.2 (n3, mega, mobile-univers, etc.).
2. `test_v1_boutique_no_special_css` → `test_v1_boutique_shop_root_css` — V1 délègue à V3 ⇒ Boutique porte `ck-nav-shop-root`, pas mega ni rayon V2.2.
3. `test_ck_header_v22.py` — assertions header alignées V3 (plus de Communauté / Espace pro / N3) ; Accueil `fa-home` conservé.

## Rejeu

```text
db              = ck_s2_test_align3 (jetable, DROP après)
db-filter       = ^ck_s2_test_align3$
tags            = dorevia_ck_nav_s2,dorevia_ck_nav_catalogue,dorevia_ck_nav_v1,dorevia_ck_header_v22
post-tests      = 76
result          = 0 failed, 0 error(s)
exit            = 0
```

Couverture : idempotence S2, collisions séquences, catalogue (dont split-link HttpCase), délégation V1, header thème (icône Accueil).

Environnement HTTP : `db-filter` exact = nom de base (évite le filtre local `ck_marketone_local`).

Contre-recette visuelle mobile 390 px : non rejouée (aucun fichier fonctionnel modifié).
