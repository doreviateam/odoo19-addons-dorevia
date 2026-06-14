# Recette QA — Phase 7 · Fiche producteur CMS pilote · M1 · CK V1.2.x

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Instance** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **GO MOA** | [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) **§5octies — ACTÉ 2026-06-13** |
| **Module** | `dorevia_ck_theme` **19.0.1.6.0** |
| **Statut** | **✅ Phases 1–7 clôturées (Phase 7 OK partiel MOA) · Phase 8 suspendue** |

---

## 0. Incident MOA · intégration website (19.0.1.5.0)

| Contrôle | Attendu | Résultat 19.0.1.5.0 |
|----------|---------|---------------------|
| Structure HTML | `<html>` · `<head>` | ❌ fragment `<div id="wrap">` seul |
| Assets frontend | `web.assets_frontend` | ❌ |
| Header / footer Odoo | visibles | ❌ |
| CSS thème | actif | ❌ |

**Verdict MOA corrigé** : **KO visuel / KO intégration website** — Phase 7 **non clôturée**.

**Correction Dev 19.0.1.6.0** : `_wrap_website_page_arch()` dans `_bootstrap_cms_page()` · enveloppe `t-call="website.layout"` · gate renforcé (`<html>` · assets).

---

## 1. Périmètre Phase 7 (strict)

| # | Livrable | Attendu | Résultat |
|---|----------|---------|----------|
| 7.1 | Fiche pilote | `/producteur/atelier-hauts-goyaviers` HTTP 200 | ✅ |
| 7.2 | Scope CMS | `ck-producer-page` | ✅ |
| 7.3 | Présentation | Atelier Les Hauts Goyaviers · territoire · savoir-faire | ✅ |
| 7.4 | Critères CK | Statiques · visibles · « Pourquoi CK sélectionne » | ✅ |
| 7.5 | Produits associés | Liens BO réels (confiture goyave) | ✅ |
| 7.6 | Pas lien fictif | Pas `/recettes` · pas URLs maquette | ✅ |
| 7.7 | CTA | `/shop` · `/contactus` · `/professionnels` | ✅ |
| 7.8 | Fiche produit | **Inchangée** · pas lien producteur | ✅ |
| 7.9 | Nav Producteurs | **Non exposée** (conforme gate) | ✅ |
| 7.10 | **Intégration website** | `<html>` · assets · header/footer · CSS | ✅ acte MOA |

---

## 1bis. Recontrôle MOA 19.0.1.6.0 — intégration page producteur

| Contrôle | Attendu | Résultat recontrôle MOA |
|----------|---------|-------------------------|
| Layout Odoo complet | `<html>` · `<head>` · `<body>` | ✅ |
| Assets frontend | `web.assets_frontend` | ✅ |
| Classe thème | `body.ck-theme` | ✅ |
| Contenu page producteur | typo · boutons · blocs stylés | ✅ |
| Scope CMS | `ck-producer-page` | ✅ |
| Mobile 390 | pas overflow · `390/390` | ✅ |
| Menu mobile | tiroir fonctionnel | ✅ |
| Sous-menu Découvrir | ouverture fonctionnelle | ✅ |

**Verdict intégration page producteur (19.0.1.6.0)** : **corrigée** — layout · assets · CSS page actifs · contenu stylé.

**Contrôle MOA recommandé (alignement écran)** :

```
http://localhost:18079/producteur/atelier-hauts-goyaviers?db=dorevia_ck_marketone_01&qa_ts=1
```

Puis rechargement forcé (`Cmd+Shift+R`). Si l’écran affiche encore une page brute sans `<html>` / sans style : vérifier base `dorevia_ck_marketone_01` · cache navigateur · assets non rafraîchis.

---

## 1ter. Réserve UX/UI header-menu — confirmée et renforcée (transversal)

Le **contenu page producteur** est stylé CK ; le **header/menu** reste très **Odoo natif** et **en retard d’habillage** par rapport au reste de la page :

| Point observé | Détail recontrôle MOA |
|---------------|----------------------|
| Logo | `Your Logo` / placeholder |
| Header desktop | menu blanc standard · recherche standard · icônes natives |
| Menu mobile fermé | rendu natif Odoo |
| Offcanvas mobile | fonctionnel · peu habillé CK |
| Sous-menu Découvrir | fonctionnel · austère |
| Contraste page vs header | page producteur stylée · header/menu générique |

```text
Phase 7 — intégration page producteur corrigée.
Mais réserve UX/UI header-menu confirmée et renforcée :
le menu est fonctionnel, mais son habillage CK paraît en retard
par rapport au reste de la page.
```

| Nature | Verdict |
|--------|---------|
| Intégration page producteur | **OK** — pas KO |
| Header/menu CK | **Réserve UX/UI transversale confirmée** — **non reclassée KO applicatif Phase 7** |
| Écart visuel | Page stylée vs header natif — dette go-live / capital Phase 1 |

**Rattachement gouvernance** : capital Phase 1 header · [`note_reference_header_mega_menu_decouverte_ck_v1.md`](./note_reference_header_mega_menu_decouverte_ck_v1.md).

### Acte MOA — verdict intermédiaire Phase 7 · **ACTÉ 2026-06-14**

| Décision | Statut |
|----------|--------|
| Intégration technique page producteur (19.0.1.6.0) | ☑ **Corrigée** — pas KO applicatif Phase 7 |
| Bug historique 19.0.1.5.0 (fragment sans layout) | ☑ **Distinct et corrigé** |
| Réserve UX/UI header-menu | ☑ **Confirmée** — transversale · capital Phase 1 / go-live |
| Reclassification réserve en KO Phase 7 | ☐ **Refusée** |
| Recette Dev (contenu + triptyque) | ☑ **Finalisée** — cf. §1 · §2 · §3 |
| Signature finale Phase 7 | ☑ **OK partiel MOA** · cf. §1quater · **2026-06-14** |
| GO Phase 8 | ☐ **Suspendu** — verdict MOA/QA Phase 7 explicite requis |

**Verdict MOA intermédiaire** :

```text
Intégration technique page producteur : corrigée (19.0.1.6.0).
Réserve UX/UI header-menu : confirmée — non bloquante Phase 7.
Dette transverse go-live (Phase 1) — bloquante go-live uniquement si acte MOA ultérieur.
```

**Contrôle écran MOA en cours** :

```
/producteur/atelier-hauts-goyaviers?db=dorevia_ck_marketone_01&qa_ts=1
```

Rechargement forcé (`Cmd+Shift+R`). Attendu : page stylée dans layout Odoo · header encore natif → **pas KO Phase 7**.

---

## 2. Triptyque QA

| Niveau | Contrôle | Résultat |
|--------|----------|----------|
| **1. Contrat Odoo** | `--test-tags=dorevia_ck_theme_phase7` | ✅ **13/13 tests** · 2026-06-14 |
| **2. Smoke curl** | `ck_phase7_ci.sh` · `<html>` · `web.assets_frontend` | ✅ · 2026-06-14 |
| **3. Playwright UX** | Desktop 1280 · mobile 390 px · pas overflow | ✅ · 2026-06-14 |

**Détail Playwright desktop** : `ck-producer-page` · `#ck-producer-products` · critères CK · CTA shop/contact/pro · titre H1 · non-régression routes 200.

**Détail Playwright mobile 390** : producteur · contact · à-propos · pro · shop · home — `scrollWidth/clientWidth = 390/390` · pas overflow.

---

## 3. Non-régression Phases 1–6

| Phase | Contrôle | Résultat |
|-------|----------|----------|
| Phase 2 home | vedettes SSR | ✅ |
| Phase 3 shop | `s_ck_shop_intro` | ✅ |
| Phase 4 fiche produit | `ck-product-page` · pas lien producteur | ✅ |
| Phase 5 pro | `ck-pro-page` · layout | ✅ |
| Phase 6 contact / à-propos | marqueurs · layout | ✅ |

---

## 1quater. Contrôle QA MOA final · cache-bust · **2026-06-14**

**URL contrôlée** :

```
http://localhost:18079/producteur/atelier-hauts-goyaviers?db=dorevia_ck_marketone_01
```

| Preuve technique | Résultat |
|------------------|----------|
| `doctype: html` | ✅ |
| `body.ck-theme` | ✅ |
| `web.assets_frontend` | ✅ |
| `ck-producer-page` | ✅ |
| `header` | ✅ |
| `footer` | ✅ |
| Desktop | **1280 / 1280** |
| Mobile | **390 / 390** |
| Menu mobile | s’ouvre · pas overflow |

**Réserve bloquante levée** : la page n’est plus un fragment brut · layout Odoo complet chargé.

**Réserve maintenue (transversale)** :

```text
Réserve UX/UI transversale :
header/menu encore très Odoo natif, logo placeholder "Your Logo",
offcanvas mobile peu brandé CK, finition go-live insuffisante.
Non bloquant Phase 7, mais à traiter avant mise en ligne.
```

---

## 4. Verdict QA

| Champ | Valeur |
|-------|--------|
| **Verdict Phase 7 (19.0.1.5.0)** | ☑ **KO** — fragment sans layout · **historique corrigé** |
| **Verdict Phase 7 (19.0.1.6.0)** | ☑ **OK partiel MOA** · **2026-06-14** |
| **Intégration website / CSS page** | ☑ **Validée** |
| **Recette Dev (contenu + triptyque)** | ☑ **OK** |
| **Réserve header/menu** | ☑ **Transversale · dette go-live / Phase 1 · non bloquante Phase 7** |
| **GO Phase 8** | ☐ **Suspendu** — dossier §5nonies préparé · acte MOA requis |
| **Validé par** | MOA CK |
| **Date clôture Phase 7** | **2026-06-14** |

```text
Phase 7 — OK partiel MOA.
Intégration website/CSS corrigée et validée.
Réserve header/menu maintenue comme dette UX/UI transversale go-live / Phase 1.
Phase 8 suspendue à acte MOA distinct.
```

---

*Recette QA Phase 7 — **CLÔTURÉE OK partiel MOA** · 2026-06-14.*
