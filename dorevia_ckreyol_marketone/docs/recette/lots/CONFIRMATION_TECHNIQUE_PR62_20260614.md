# Confirmation technique MOA — PR #62 · Chantier B

| Champ | Valeur |
|-------|--------|
| **Chantier** | **B — Boutique Marketone / cadrage2** |
| **PR** | https://github.com/doreviateam/odoo19-addons-dorevia/pull/62 |
| **Branche** | `feat/marketone-lot6-3-seo-reprise-20260614` |
| **Module** | `dorevia_ckreyol_marketone` **19.0.19.0.1** |
| **Instance QA** | `ckr-marketone-01` |
| **Date confirmation** | **2026-06-14** |
| **Décision B1** | **GO merge acté MOA · MERGED 2026-06-14** |
| **Commit main** | `388e515` · `19.0.19.0.1` |

```text
CHAMPIER B UNIQUEMENT — indépendant de la recette go-live CK (Chantier A).
Ne pas mélanger merge PR #62 avec verdict A1 header maquette.
```

---

## Confirmations demandées MOA

| # | Point | Résultat | Détail |
|---|-------|----------|--------|
| 1 | PR #62 mergeable | ✅ **OUI** | `mergeStateStatus: CLEAN` · `mergeable: MERGEABLE` |
| 2 | Tests gate 72/72 | ✅ **OUI** | Recontrôle **2026-06-14 09:52 UTC** sur branche PR |
| 3 | Conflit modules CK maquette | ✅ **AUCUN** | 82 fichiers · 100 % sous `dorevia_ckreyol_marketone/` |
| 4 | Périmètre inchangé | ✅ **OUI** | Promotions · Kits · SEO portes · BO recadrage · warnings Odoo 19 |
| 5 | Hors périmètre respecté | ✅ **OUI** | Pas `dorevia_glc_analytics` · pas `dorevia_ck_theme` · pas `dorevia_ck_marketone_content` |

---

## Gate QA exécutée (recontrôle 2026-06-14)

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf -d ckr-marketone-01 \
  -u dorevia_ckreyol_marketone --test-enable --stop-after-init --http-port=18082 \
  --test-tags=dorevia_marketone_shop_sidebar_collections,dorevia_marketone_shop_wishlist,dorevia_marketone_lot3,dorevia_marketone_lot6_3a_promo,dorevia_marketone_lot6_3b_pack,dorevia_marketone_seo_portes_shop
```

| Métrique | Valeur |
|----------|--------|
| post-tests | **72** |
| failed | **0** |
| error(s) | **0** |

---

## Périmètre PR #62 (rappel)

| Lot | Contenu |
|-----|---------|
| 6.3a | `/promotions` · pricelist · vue shop promo |
| 6.3b | `/kits` · `pack_ok` · vue shop pack |
| SEO | canonical / noindex portes `/shop` |
| BO | recadrage formulaire produit |
| Warnings | `hasclass()` · retrait `t-nocache` |
| Header | chips Promotions + Kits |

---

## Suite MOA — décision B1 · **ACTÉ · MERGÉ 2026-06-14**

```text
GO merge PR #62 acté MOA.
Merge exécuté : commit 388e515 sur main · dorevia_ckreyol_marketone 19.0.19.0.1.
Ne vaut PAS clôture MOA lots 6.3a / 6.3b / SEO.
Suite : recettes navigateur dédiées (grilles ci-dessous).
```

**Documents recette Chantier B — à exécuter post-merge** :

- [`RECETTE_MANUELLE_LOT6_3A_PROMO.md`](./RECETTE_MANUELLE_LOT6_3A_PROMO.md)
- [`RECETTE_MANUELLE_LOT6_3B_PACK.md`](./RECETTE_MANUELLE_LOT6_3B_PACK.md)
- [`RAPPORT_QA_DEV_REPRISE_MARKETONE_20260614.md`](./RAPPORT_QA_DEV_REPRISE_MARKETONE_20260614.md)

---

*Confirmation technique PR #62 · B1 merge acté · recettes navigateur en attente · 2026-06-14.*
