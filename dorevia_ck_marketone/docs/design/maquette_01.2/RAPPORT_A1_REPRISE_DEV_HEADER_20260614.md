# Rapport livraison Dev — A1 reprise visuelle header · 2026-06-14

| Champ | Valeur |
|-------|--------|
| **Chantier** | **A — `dorevia_ck_theme`** · header uniquement |
| **Verdict MOA amont** | **A1-GO Dev ciblé** (2026-06-14) |
| **Module** | `dorevia_ck_theme` **19.0.1.12.0** |
| **Instance** | `dorevia_ck_marketone_01` |
| **Rôle** | Livraison Dev ciblée · nouvelle recette A1 · **verdict MOA requis** |

```text
Périmètre strict MOA respecté : visuel header · pas de réouverture fonctionnelle · pas §3–§9 · pas Chantier B.
```

---

## Synthèse changements

| Fichier | Nature |
|---------|--------|
| `views/website_header.xml` | Logo typographique C-Kreyol · fonts Fraunces/DM Sans · sticky critical CSS |
| `static/src/scss/website_header.scss` | Reprise visuelle maquette : densité · nav centrée · hiérarchie · mega · mobile |
| `static/src/scss/primary_variables.scss` | Stacks typo Fraunces + DM Sans |
| `tests/test_ck_phase10_header_compose.py` | Assertion marque typographique · absence img logo générique |
| `migrations/19.0.1.12.0/post-migrate.py` | Migration vide (chrome only) |

---

## Corrections MOA adressées

| # MOA | Correction Dev |
|-------|----------------|
| Logo générique | Remplacé par marque typographique **`C-Kreyol`** (`Kreyol` en `$ck-primary`) — plus d’`<img>` logo website |
| Perception standard Odoo | Nav muted → hover soft · boutons utilitaires CK · mega typographié · offcanvas brandé |
| Structure / densité / hiérarchie | Header 60px · nav desktop centrée · container max 1200px · espacements maquette |
| Cohérence desktop + mobile | Même marque typo · offcanvas CK · touch targets ≥ 40px |
| Acquis techniques | Sticky · mega · overflow · Contactez-nous (utilitaires + offcanvas) **conservés** |

---

## Détail technique

### Logo typographique

```xml
<span class="ck-header__brand">C-<span class="ck-header__brand-accent">Kreyol</span></span>
```

- Héritage `website.option_header_brand_logo` (desktop + mobile)
- Image website masquée / remplacée · `aria-label="C-Kreyol — Accueil"`

### Typographie

- Google Fonts : **Fraunces** (display / logo / titres mega) · **DM Sans** (UI nav)
- Chargement via `<link>` QWeb (pas `@import` SCSS bundle)

### Layout desktop

- `#top_menu` centré (`flex: 1; justify-content: center`)
- Liens nav : 14px · couleur muted · hover fond `$ck-bg-soft`
- Fond header : `rgba(surface, 0.94)` + `blur(12px)`

### Non modifié (fonctionnel)

- Entrées menu BO · mega contenu · routes · Contactez-nous placement Odoo · panier / recherche

---

## Validation QA post-livraison

| Contrôle | Résultat |
|----------|----------|
| `ck_phase10_ci.sh` | ✅ OK |
| Tests `dorevia_ck_theme_phase10` | ✅ 3/3 |
| Recette visuelle Playwright | ✅ **27/27** |
| Sticky scroll | ✅ `position: sticky` · top 0 après scroll 1200px |
| Overflow 1280 / 390 | ✅ |
| Logo img générique | ✅ absent HTML |

---

## Captures post-correction

Dossier : [`rapport/a1_visuelle_20260614_v2/`](./rapport/a1_visuelle_20260614_v2/)

| Fichier | Usage MOA |
|---------|-----------|
| `desktop_1280_home.png` | Identité logo · nav · hiérarchie |
| `desktop_1280_home_scrolled.png` | Sticky |
| `desktop_1280_contact.png` · `desktop_1280_shop.png` | Cohérence 3 URLs |
| `mobile_390_home.png` | Header mobile |
| `mobile_390_offcanvas_open.png` | Menu burger |
| `mobile_390_mega_decouvrir.png` | Mega mobile |
| `a1_recette_results.json` | Résultats machine |

---

## Nouvelle recette A1 — proposition QA

| Grille | Résultat proxy post-Dev |
|--------|-------------------------|
| D1–D12 desktop | ✅ |
| M1–M9 mobile | ✅ |
| Arbitrage Contactez-nous | ✅ conservé |

**Proposition QA → MOA** : base **A1-OK** · relecture visuelle MOA sur captures v2 recommandée.

**Verdict MOA** : ☐ A1-OK · ☐ réserve · ☐ A1-GO Dev ciblé (itération)

---

## Reproductibilité

```bash
# Upgrade
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf -d dorevia_ck_marketone_01 \
  -u dorevia_ck_theme --stop-after-init

# Gate + recette
dorevia_ck_marketone/docs/design/maquette_01.2/scripts/ck_phase10_ci.sh
python3 dorevia_ck_marketone/docs/design/maquette_01.2/scripts/a1_recette_visuelle_playwright.py
```

URLs MOA :

```text
http://localhost:18079/?db=dorevia_ck_marketone_01&qa_ts=phase10a1v2
http://localhost:18079/contactus?db=dorevia_ck_marketone_01&qa_ts=phase10a1v2
http://localhost:18079/shop?db=dorevia_ck_marketone_01&qa_ts=phase10a1v2
```

---

## Documents liés

| Document | Rôle |
|----------|------|
| [`RECETTE_MOA_ECRAN_A1_HEADER_PHASE10.md`](./RECETTE_MOA_ECRAN_A1_HEADER_PHASE10.md) | Verdict A1-GO Dev ciblé · signature nouvelle recette |
| [`RAPPORT_A1_RECETTE_VISUELLE_20260614.md`](./RAPPORT_A1_RECETTE_VISUELLE_20260614.md) | Recette avant reprise (référence) |
| [`artifact/ck-maquette.css`](./artifact/ck-maquette.css) | Référence visuelle header |

**Hors périmètre** : commit docs · Phase 10 §3–§9 · A7 · Chantier B.

---

*Livraison Dev A1 header · MOA signature requise · 2026-06-14.*
