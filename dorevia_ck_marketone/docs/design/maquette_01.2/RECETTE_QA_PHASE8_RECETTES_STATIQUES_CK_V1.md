# Recette QA — Phase 8 · Recettes statiques / Savoirs · M2 · CK V1.2.x

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Instance** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **GO MOA** | [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) **§5nonies — ACTÉ 2026-06-14** |
| **Phase 7** | **Clôturée OK partiel MOA · 2026-06-14** |
| **Module** | `dorevia_ck_theme` **19.0.1.7.0** |
| **Statut** | **✅ Phases 1–8 clôturées (Phase 8 OK partiel MOA) · Phase 9 suspendue** |

> **Phase 8 — OK partiel MOA.** Page `/recettes` conforme au périmètre M2 : CMS statique · 6 cartes · liens BO réels · pas de blog · pas de commentaires · layout Odoo complet.

---

## 0. Rappel gouvernance

| Règle | Statut |
|-------|--------|
| Phases 1–7 clôturées | ✅ |
| Phase 8 clôture | ✅ **OK partiel MOA · 2026-06-14** |
| Réserve header/menu CK | Dette transversale go-live / Phase 1 · **non bloquante Phase 8** |
| Phase 9–10 | ☐ **Suspendues** — acte MOA distinct requis |

---

## 1. Périmètre Phase 8 (strict · livré)

| # | Livrable | Attendu | Résultat |
|---|----------|---------|----------|
| 8.1 | Page CMS | `/recettes` HTTP 200 | ✅ |
| 8.2 | Scope CMS | `ck-recipes-page` | ✅ |
| 8.3 | Hero éditorial | Titre · kicker · lead M2 | ✅ |
| 8.4 | Grille cartes | 6 cartes éditoriales statiques | ✅ |
| 8.5 | Liens catalogue | Liens BO réels · shop · producteur pilote | ✅ |
| 8.6 | Pas lien fictif | Pas URLs maquette · pas produits inventés | ✅ |
| 8.7 | Garde-fou M2 | Pas blog · pas commentaires · pas contribution | ✅ |
| 8.8 | Intégration website | `<html>` · assets · `website.layout` · `body.ck-theme` | ✅ |
| 8.9 | Non-régression | Phases 1–7 inchangées | ✅ |
| 8.10 | Header/footer | **Inchangés** sauf acte MOA post-recette | ✅ |

**Référence composition** : [`COMPOSITION_RECETTES_V1_2.md`](./COMPOSITION_RECETTES_V1_2.md)

---

## 1bis. Recontrôle MOA — cache-bust `/recettes?qa_ts=1`

| Contrôle | Attendu | Résultat recontrôle MOA |
|----------|---------|-------------------------|
| HTTP | 200 | ✅ |
| doctype html | présent | ✅ |
| `body.ck-theme` | présent | ✅ |
| `web.assets_frontend` | présent | ✅ |
| `ck-recipes-page` | présent | ✅ |
| Header / footer Odoo | visibles | ✅ |
| H1 | « Recettes & savoirs CK » | ✅ |
| Grille cartes | 6 cartes statiques visibles | ✅ |
| Garde-fou M2 | pas blog · pas commentaires | ✅ |
| Desktop | 1280 / 1280 · pas overflow | ✅ |
| Mobile | 390 / 390 · pas overflow | ✅ |
| Menu mobile | s’ouvre sans overflow | ✅ |

**Liens principaux contrôlés 200** :

```text
/recettes
/shop/confiture-de-goyave-3
/shop
/producteur/atelier-hauts-goyaviers
/a-propos
/contactus
```

---

## 2. Triptyque QA

| Niveau | Contrôle | Résultat |
|--------|----------|----------|
| **1. Contrat Odoo** | `--test-tags=dorevia_ck_theme_phase8` | ✅ **15/15** |
| **2. Smoke curl** | `ck_phase8_ci.sh` · `/recettes` · layout · non-régression | ✅ |
| **3. Playwright UX** | Desktop 1280 · mobile 390 px · pas overflow | ✅ |

---

## 3. Non-régression Phases 1–7

| Phase | Contrôle | Résultat |
|-------|----------|----------|
| Phase 2 home | vedettes SSR | ✅ |
| Phase 3 shop | `s_ck_shop_intro` | ✅ |
| Phase 4 fiche produit | `ck-product-page` | ✅ |
| Phase 5 pro | `ck-pro-page` | ✅ |
| Phase 6 contact / à-propos | marqueurs · layout | ✅ |
| Phase 7 producteur | `ck-producer-page` · layout | ✅ |

---

## 4. Réserve UX/UI header-menu (transversal · non bloquante)

Le **contenu page recettes** est stylé CK ; le **header/menu** reste très **Odoo natif** :

| Point observé | Détail recontrôle MOA |
|---------------|----------------------|
| Logo | `Your Logo` / placeholder |
| Header desktop | menu blanc standard · recherche standard · icônes natives |
| Offcanvas mobile | fonctionnel · peu brandé CK |
| Finition go-live | insuffisante vs page recettes stylée |

```text
Phase 8 — intégration page recettes conforme.
Réserve header/menu CK maintenue comme dette UX/UI transversale go-live / Phase 1.
Non bloquante Phase 8.
Lien mega-menu /recettes : non exposé (conforme périmètre strict Phase 8).
```

| Nature | Verdict |
|--------|---------|
| Intégration page `/recettes` | ✅ conforme périmètre M2 |
| Header/menu CK | Réserve transversale · dette go-live |
| Blocant Phase 8 | **Non** |

---

## 5. Verdict QA · **ACTÉ MOA 2026-06-14**

| Champ | Valeur |
|-------|--------|
| **Verdict Phase 8** | ☐ OK · ☑ **OK partiel MOA** · ☐ KO |
| **Motif OK partiel** | Livraison conforme périmètre M2 · réserve header/menu CK transversale (dette go-live / Phase 1) |
| **GO Phase 9** | ☐ **Suspendu** — acte MOA distinct requis |
| **Validé par** | MOA |
| **Date clôture** | **2026-06-14** |

```text
Phase 8 — OK partiel MOA.
Page /recettes conforme au périmètre M2 : CMS statique, 6 cartes, liens BO réels,
pas de blog, pas de commentaires, layout Odoo complet.
Réserve header/menu CK maintenue comme dette transversale go-live.
Phase 9 suspendue à acte MOA distinct.
```

---

*Recette QA Phase 8 — clôturée OK partiel MOA · 2026-06-14.*
