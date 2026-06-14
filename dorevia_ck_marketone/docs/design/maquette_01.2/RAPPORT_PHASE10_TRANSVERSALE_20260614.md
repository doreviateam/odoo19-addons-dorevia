# Rapport Phase 10 §3–§9 transversale · CK V1.2.x · 2026-06-14

| Champ | Valeur |
|-------|--------|
| **Chantier** | **A — `dorevia_ck_marketone_01`** |
| **Modules** | `dorevia_ck_theme` **19.0.1.12.0** · `dorevia_ck_marketone_content` **19.0.1.0.0** |
| **Grille source** | [`RECETTE_QA_PHASE10_GO_LIVE_CK_V1.md`](./RECETTE_QA_PHASE10_GO_LIVE_CK_V1.md) §3–§9 |
| **Prérequis** | **A1-OK** signé · header **non rouvert** |
| **Rôle** | Recette proxy transversale · **OK partiel MOA signé** |
| **Exécuteur** | QA Cursor · 2026-06-14 |

```text
Périmètre exécuté : §3 transversale · §4 critères · §5 garde-fous · §9 checklist proxy.
§2 header : CLÔTURÉ A1-OK — référence uniquement · pas de réouverture.
Hors scope exécution : A7 · Chantier B · commit global.
Hero / contenus accueil : dettes hors A1 · arbitrage MOA ci-dessous.
```

---

## Synthèse MOA — restitution

| Nature | Verdict proxy QA |
|--------|------------------|
| Gates Phases **3–10** | ✅ **8/8 OK** |
| Routes / liens critiques §3.3 | ✅ **9/9 HTTP 200** |
| Mobile **390** overflow (9 pages) | ✅ **0 overflow** |
| Footer liens | ✅ **5 liens · 0 dead** |
| Newsletter / formulaires / séparation | ✅ |
| Panier / checkout CE | ✅ |
| **Bloquant §4.1** | ✅ **Aucun ouvert** |
| Dettes non bloquantes §4.2 | ⚠️ **6 points d’arbitrage** (voir § Arbitrages) |

**Proposition QA → MOA** : ~~base favorable OK partiel~~ → **OK partiel MOA signé · 2026-06-14**.

---

## §2 Header — clôture A1 (référence · non rejoué)

| Élément | Statut |
|---------|--------|
| Verdict MOA | **A1-OK** · 2026-06-14 |
| Module | **19.0.1.12.0** |
| Traçabilité | [`RECETTE_MOA_ECRAN_A1_HEADER_PHASE10.md`](./RECETTE_MOA_ECRAN_A1_HEADER_PHASE10.md) · [`rapport/a1_visuelle_20260614_v2/`](./rapport/a1_visuelle_20260614_v2/) |
| Réouverture header | ❌ **Interdite** |

---

## §3.1 Mobile 390 px — toutes pages Phases 1–9

| Page | Marqueur | Overflow 390 | Proxy |
|------|----------|--------------|-------|
| `/` | vedettes SSR | ✅ 390=390 | ✅ |
| `/shop` | `s_ck_shop_intro` | ✅ | ✅ |
| `/shop/confiture-de-goyave-3` | fiche produit | ✅ | ✅ |
| `/shop/cart` | panier | ✅ | ✅ |
| `/professionnels` | `ck-pro-page` | ✅ | ✅ |
| `/contactus` | `ck-contact-page` | ✅ | ✅ |
| `/a-propos` | `ck-about-page` | ✅ | ✅ |
| `/recettes` | `ck-recipes-page` | ✅ | ✅ |
| `/producteur/atelier-hauts-goyaviers` | `ck-producer-page` | ✅ | ✅ |

Captures : [`rapport/phase10_transversale_20260614/mobile390_*.png`](./rapport/phase10_transversale_20260614/)

---

## §3.2 Footer / mentions

| # | Contrôle | Proxy | Note MOA |
|---|----------|-------|----------|
| F1 | Footer structure | ✅ | Footer présent · ~4 colonnes |
| F2 | Liens footer réels | ✅ | `/shop` · catégorie · contact · pro · `/` — **0×404** |
| F3 | Mentions légales | ⚠️ | **Absentes** footer · non bloquant si MOA diffère V1 |
| F4 | Liens Phases 6–8 footer | ⚠️ | `/a-propos` · `/recettes` **non** en footer · option MOA |

---

## §3.3 Liens morts · routes

| Route | HTTP | Proxy |
|-------|------|-------|
| `/` | 200 | ✅ |
| `/shop` | 200 | ✅ |
| `/shop/cart` | 200 | ✅ |
| `/contactus` | 200 | ✅ |
| `/professionnels` | 200 | ✅ |
| `/a-propos` | 200 | ✅ |
| `/recettes` | 200 | ✅ |
| `/producteur/atelier-hauts-goyaviers` | 200 | ✅ |
| `/shop/category/epicerie-creole-1` | 200 | ✅ |
| `/shop/confiture-de-goyave-3` | 200 | ✅ |

Mega **Épicerie créole** : ✅ · Mega **/recettes** · **/a-propos** : absent (gate MOA documenté · non bloquant V1).

---

## §3.4 Copy M5 (réassurance)

| Emplacement | Proxy | Note |
|-------------|-------|------|
| Home | ✅ `s_ck_reassurance` / `ck-reassurance` | Présent |
| Shop | ✅ `ck-reassurance` (snippet M5 via compose) | Copy **relecture MOA métier** recommandée |
| Fiche produit | ⚠️ absent | **Non bloquant V1** si MOA acte · pas snippet M5 sur fiche |

---

## §3.5 Checkout / panier

| # | Contrôle | Proxy |
|---|----------|-------|
| C1 | `/shop/cart` HTTP 200 | ✅ |
| C2 | Produit publié disponible | ✅ `confiture-de-goyave-3` |
| C3 | Parcours CE natif | ✅ container checkout présent |
| C4 | Pas surcouche custom Phase 10 | ✅ |

---

## §3.6 Newsletter (Phase 9)

| # | Contrôle | Proxy |
|---|----------|-------|
| N1 | Contact · `#ck-newsletter-subscribe` | ✅ |
| N2 | Pro · newsletter distincte | ✅ |
| N3 | Mailing list BO | ✅ (gate phase9) |
| N4 | Subscribe endpoint | ✅ (tests phase9) |
| N5 | RGPD · désinscription | ✅ mention présente contact |
| N6 | Pas popup | ✅ |
| N7 | Home dual Phase 2 | ✅ `ck-dual-engage` |

---

## §3.7 Formulaires · séparation parcours

| Parcours | Proxy | Détail |
|----------|-------|--------|
| Contact B2C | ✅ | `contactus_form` · `mail.mail` |
| CRM Pro | ✅ | `#ck-pro-form` · `crm.lead` |
| Séparation | ✅ | Pas `contactus_form` sur `/professionnels` |

---

## §3.8 Assets / cache

| # | Contrôle | Proxy |
|---|----------|-------|
| A1 | `web.assets_frontend` | ✅ pages clés |
| A2 | `body.ck-theme` | ✅ |
| A4 | SSR vedettes home | ✅ `ck-featured-products__grid--stable` |
| A5 | Favicon BO | ✅ `/web/image/website/1/favicon` · **relecture asset MOA** |

---

## §3.9 Non-régression Gates Phases 3–10

| Gate | Résultat | Date |
|------|----------|------|
| `ck_phase3_ci.sh` | ✅ | 2026-06-14 |
| `ck_phase4_ci.sh` | ✅ | 2026-06-14 |
| `ck_phase5_ci.sh` | ✅ | 2026-06-14 |
| `ck_phase6_ci.sh` | ✅ | 2026-06-14 |
| `ck_phase7_ci.sh` | ✅ | 2026-06-14 |
| `ck_phase8_ci.sh` | ✅ | 2026-06-14 |
| `ck_phase9_ci.sh` | ✅ | 2026-06-14 |
| `ck_phase10_ci.sh` | ✅ | 2026-06-14 |

---

## §4 — Bloquants / dettes

### §4.1 Bloquants go-live

```text
Aucun bloquant proxy ouvert sur la passe transversale §3–§9.
```

### §4.2 Dettes non bloquantes · **actées MOA 2026-06-14**

| # | Sujet | Décision MOA |
|---|-------|--------------|
| 1 | **Hero / contenus accueil** | Dette hors A1 · **lot dédié** · non bloquant séquence |
| 2 | Mega origines · recettes / à-propos | **Absence acceptée V1** · report volontaire |
| 3 | **Mentions légales** footer | Non bloquant A7 · **bloquant go-live public** |
| 4 | Footer `/a-propos` · `/recettes` | **Accepté temporairement** |
| 5 | M5 fiche produit | **Acceptable V1** · recontrôle lot fiche/boutique |
| 6 | Copy M5 home/shop | **Relecture métier MOA** · non bloquant |
| 7 | Favicon BO | **Relecture identité MOA** · non bloquant |

---

## §5 Garde-fous Phase 10

| Garde-fou | Proxy |
|-----------|-------|
| Pas nouvelle feature | ✅ |
| Pas refonte fonctionnelle | ✅ |
| Pas réouverture split thème/contenu | ✅ |
| Pas modification checkout profonde | ✅ |
| Header non rouvert | ✅ A1-OK clôturé |

---

## §9 Checklist verdict Phase 10 (proxy)

| # | Item | Proxy |
|---|------|-------|
| 1 | §2 header A1-OK | ✅ clôturé |
| 2 | Mobile 390 §3.1 | ✅ |
| 3 | Footer / liens §3.2–3.3 | ✅ proxy · arbitrages F3/F4 |
| 4 | Copy M5 §3.4 | ✅ partiel · relecture MOA |
| 5 | Checkout §3.5 | ✅ |
| 6 | Newsletter §3.6 | ✅ |
| 7 | Formulaires §3.7 | ✅ |
| 8 | Assets §3.8 | ✅ |
| 9 | Gates §3.9 | ✅ 8/8 |
| 10 | Aucun bloquant §4.1 | ✅ |
| 11 | Dettes §4.2 actées | ☑ **MOA 2026-06-14** |
| 12 | Garde-fous §5 | ✅ |

### Verdict MOA Phase 10 · **signé 2026-06-14**

| Champ | Valeur |
|-------|--------|
| **Instance** | `dorevia_ck_marketone_01` |
| **Verdict recette Phase 10 transversale** | ✅ **OK partiel** |
| **Verdict go-live V1** | **GO partiel interne** · **NO GO public** (mentions légales) |
| **A1 header** | ✅ **A1-OK clôturé** · non rouvert |
| **Validé par** | **MOA CK** |
| **Date** | **2026-06-14** |

**Résultats favorables actés MOA** : gates phase3–10 · routes · mobile 390 · footer · newsletter · formulaires · panier/checkout CE · aucun bloquant §4.1.

```text
Suite séquence MOA :
  1. ✅ Phase 10 §3–§9 — OK partiel MOA
  2. A7 Git modules CK — acte MOA explicite dédié requis (non lancé)
  3. Chantier B navigateur — après A7
  4. Go-live public — NO GO tant que mentions légales non traitées
Documentation locale mise à jour · aucun commit global sans demande explicite.
```

---

## Reproductibilité

```bash
export CK_CI_SKIP_RESTART=1
# Upgrade once, then:
for n in 3 4 5 6 7 8 9 10; do
  bash dorevia_ck_marketone/docs/design/maquette_01.2/scripts/ck_phase${n}_ci.sh
done
python3 dorevia_ck_marketone/docs/design/maquette_01.2/scripts/phase10_transversale_recette.py
```

JSON : [`rapport/phase10_transversale_20260614/phase10_transversale_results.json`](./rapport/phase10_transversale_20260614/phase10_transversale_results.json)

---

## Documents liés

| Document | Rôle |
|----------|------|
| [`RECETTE_QA_PHASE10_GO_LIVE_CK_V1.md`](./RECETTE_QA_PHASE10_GO_LIVE_CK_V1.md) | Grille complète · mis à jour §3–§9 |
| [`RECETTE_MOA_ECRAN_A1_HEADER_PHASE10.md`](./RECETTE_MOA_ECRAN_A1_HEADER_PHASE10.md) | A1-OK clôturé |
| [`RAPPORT_A1_REPRISE_DEV_HEADER_20260614.md`](./RAPPORT_A1_REPRISE_DEV_HEADER_20260614.md) | Traçabilité header v2 |

**Hors périmètre** : A7 · Chantier B · commit · réouverture header.

---

*Rapport Phase 10 §3–§9 transversale · **OK partiel MOA** · GO partiel interne · NO GO public (mentions légales) · 2026-06-14.*
