# Rapport recette visuelle — A1 Header CK · Phase 10 §2 · 2026-06-14

| Champ | Valeur |
|-------|--------|
| **Chantier** | **A — `dorevia_ck_theme` + `dorevia_ck_marketone_content`** |
| **Instance** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **Grille source** | [`RECETTE_MOA_ECRAN_A1_HEADER_PHASE10.md`](./RECETTE_MOA_ECRAN_A1_HEADER_PHASE10.md) |
| **Rôle** | Recette visuelle QA (Playwright + gate) · **ne signe pas A1 MOA** |
| **Exécuteur** | QA Cursor · 2026-06-14 |
| **Preuves** | [`rapport/a1_visuelle_20260614/`](./rapport/a1_visuelle_20260614/) · 9 captures + JSON |

```text
Chantier A uniquement — pas de mélange Chantier B.
Verdict A1 (A1-OK · A1-GO Dev ciblé · A1-KO) = signature MOA uniquement.
Rapport local · hors Git (gouvernance MOA inchangée).
```

---

## Synthèse recette visuelle

| Nature | Résultat |
|--------|----------|
| Gate `ck_phase10_ci.sh` | ✅ **OK** (upgrade + 3 tests + smoke 7 routes) |
| Desktop 1280 — grille D1–D12 | ✅ **OK** (1 nuance Contactez-nous · voir § arbitrage) |
| Mobile 390 — grille M1–M9 | ✅ **OK** |
| Sticky scroll (D8) | ✅ **OK** — header reste en haut après scroll 1200 px |
| Mega Découvrir + Épicerie créole | ✅ |
| Overflow 1280 / 390 | ✅ |

**Proposition QA → MOA** : base **A1-OK** · relecture rapide des captures (~5 min) pour cohérence visuelle CK et arbitrage `Contactez-nous`.

---

## Gate technique

```bash
dorevia_ck_marketone/docs/design/maquette_01.2/scripts/ck_phase10_ci.sh
```

| Étape | Résultat |
|-------|----------|
| Upgrade modules CK | ✅ |
| Tests `dorevia_ck_theme_phase10` | ✅ **3/3** |
| Smoke 7 routes | ✅ |

---

## Grille MOA — desktop 1280 px

| # | Contrôle | Recette visuelle | Preuve | MOA |
|---|----------|------------------|--------|-----|
| **D1** | Logo C-Kreyol | ✅ | alt `C-Kreyol` · ~115×40 px · pas Your Logo | ☐ |
| **D2** | Taille / alignement logo | ✅ | max-height cohérent · respiration header | ☐ |
| **D3** | Nav principale | ✅ | Boutique · Découvrir · Professionnels · **Contactez-nous** (zone utilitaires droite) | ☐ |
| **D4** | Pas Producteurs (nav) | ✅ | absent `#top_menu` et liens header visibles | ☐ |
| **D5** | Mega Découvrir | ✅ | panel visible au clic | ☐ |
| **D6** | Épicerie créole | ✅ | `/shop/category/epicerie-creole-1` · HTTP 200 | ☐ |
| **D7** | Recherche / panier | ✅ | icônes présentes header | ☐ |
| **D8** | Sticky header | ✅ | scroll 1200 px · header `top: 0` · `position: fixed` en scroll | ☐ |
| **D9** | Contraste nav | ✅ proxy | couleur `rgba(0,0,0,0.65)` · **validation œil MOA sur capture** | ☐ |
| **D10** | Cohérence CK | ✅ proxy | `body.ck-theme` · `ck-header` · **validation œil MOA sur captures** | ☐ |
| **D11** | Overflow 1280 | ✅ | scrollW = clientW = 1280 (3 URLs) | ☐ |
| **D12** | Header identique 3 URLs | ✅ | même chrome `/` · contact · shop | ☐ |

### Nuance D3 — placement `Contactez-nous`

```text
Contactez-nous est visible desktop dans le header (lien utilitaire droite),
hors cluster central #top_menu (Boutique · Découvrir · Professionnels).
Comportement Odoo standard · présent aussi en offcanvas mobile (M9 OK).
```

---

## Grille MOA — mobile 390 px

| # | Contrôle | Recette visuelle | Preuve | MOA |
|---|----------|------------------|--------|-----|
| **M1** | Burger / offcanvas | ✅ | ouverture · fermeture btn-close OK | ☐ |
| **M2** | Nav mobile complète | ✅ | Boutique · Découvrir · Professionnels · Contactez-nous | ☐ |
| **M3** | Mega mobile Découvrir | ✅ | accessible offcanvas | ☐ |
| **M4** | Épicerie créole mobile | ✅ | lien `/shop/category/epicerie-creole-1` | ☐ |
| **M5** | Recherche / panier mobile | ✅ | présents header | ☐ |
| **M6** | Touch targets | ✅ | burger ~40×42 px | ☐ |
| **M7** | Overflow 390 | ✅ | scrollW = clientW = 390 (3 URLs) | ☐ |
| **M8** | Branding offcanvas | ✅ proxy | `ck-header` · capture offcanvas | ☐ |
| **M9** | Contactez-nous mobile | ✅ | présent offcanvas | ☐ |

---

## Sticky header (D8) — détail technique

| État | `position` | `top` | Note |
|------|------------|-------|------|
| Au chargement | `static` | 0 | SCSS `sticky` · comportement Odoo scroll |
| Après scroll 1200 px | `fixed` | 0 | Header reste visible · pas de saut layout mesuré |

**Conclusion QA** : comportement sticky **fonctionnel** au scroll · réserve proxy 2026-06-14 levée par mesure scroll.

---

## Arbitrages MOA — proposition QA

| Sujet | Observation recette | Proposition QA → MOA |
|-------|---------------------|----------------------|
| **Contactez-nous en nav** | Présent desktop (droite) + mobile offcanvas | ☐ **Conserver** · cohérent instance |
| **Producteurs en nav** | Absent | ☐ **Conforme absent** |
| **Mega recettes / à-propos** | Non exposé mega actuel | ☐ **Différer** V1 |
| **Effet natif Odoo résiduel** | Habillage `ck-header` actif | ☐ **Accepté V1** si MOA valide captures |

---

## Captures écran (preuves locales)

| Fichier | Contenu |
|---------|---------|
| `desktop_1280_home.png` | Accueil · header + hero |
| `desktop_1280_home_scrolled.png` | Accueil après scroll · sticky |
| `desktop_1280_contact.png` | Page contact |
| `desktop_1280_shop.png` | Page shop |
| `mobile_390_home.png` | Accueil mobile |
| `mobile_390_offcanvas_open.png` | Menu burger ouvert |
| `mobile_390_mega_decouvrir.png` | Mega Découvrir mobile |
| `mobile_390_contact.png` | Contact mobile |
| `mobile_390_shop.png` | Shop mobile |
| `a1_recette_results.json` | Résultats machine-readable |

Dossier : `docs/design/maquette_01.2/rapport/a1_visuelle_20260614/`

---

## Verdict A1 — **non signé · proposition QA**

| Option | Proposition QA | Condition MOA |
|--------|----------------|---------------|
| **A1-OK** | ✅ **Recommandé** | Relecture rapide captures D9/D10/M8 · arbitrage Contactez-nous acté |
| A1-GO Dev ciblé | Non requis proxy | — |
| A1-KO | Non recommandé proxy | — |

```text
MOA : cocher verdict dans RECETTE_MOA_ECRAN_A1_HEADER_PHASE10.md
      · relecture captures ~5 min recommandée
      · signature A1 débloque Phase 10 §3–§9 et suite Chantier B
```

---

## Script reproductible

```bash
python3 dorevia_ck_marketone/docs/design/maquette_01.2/scripts/a1_recette_visuelle_playwright.py
```

---

## Documents liés

| Document | Rôle |
|----------|------|
| [`RECETTE_MOA_ECRAN_A1_HEADER_PHASE10.md`](./RECETTE_MOA_ECRAN_A1_HEADER_PHASE10.md) | Grille signature MOA |
| [`RAPPORT_QA_TEMPORAIRE_20260614.md`](./RAPPORT_QA_TEMPORAIRE_20260614.md) | Proxy initial · sticky réserve levée |
| [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) | Gouvernance §5undecies |

**Hors périmètre** : Chantier B · commit docs · signature MOA.

---

*Recette visuelle A1 · Chantier A · verdict MOA en attente signature · 2026-06-14.*
