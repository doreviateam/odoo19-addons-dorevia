# Rapport QA temporaire — Chantiers A & B · 2026-06-14

| Champ | Valeur |
|-------|--------|
| **Rôle** | QA temporaire (proxy technique + Playwright headless) |
| **Exécuteur** | Dev/QA Cursor · **ne remplace pas signature MOA** |
| **Verdicts MOA** | **Non signés** — A1 · clôture lots 6.3 B |

```text
Ce rapport prépare la décision MOA.
Seule la MOA signe A1-OK · A1-GO Dev · A1-KO · clôture recettes Chantier B.
```

---

## Chantier A — Session A1 header · proxy QA

**Instance** : `dorevia_ck_marketone_01` · modules `19.0.1.11.0` / `19.0.1.0.0`

### Gate automatisée

| Contrôle | Résultat |
|----------|----------|
| `ck_phase10_ci.sh` | ✅ upgrade + 3 tests Odoo + smoke 7 routes |
| Date | 2026-06-14 10:01 UTC |

### Proxy DOM (3 URLs)

| Contrôle | `/` | `/contactus` | `/shop` |
|----------|-----|--------------|---------|
| HTTP 200 | ✅ | ✅ | ✅ |
| `ck-header` | ✅ | ✅ | ✅ |
| Logo C-Kreyol · pas Your Logo | ✅ | ✅ | ✅ |
| Producteurs **dans header** | ✅ absent | ✅ | ✅ |
| Mega / Épicerie créole ref | ✅ | ✅ | ✅ |
| `/shop/category/epicerie-creole-1` | ✅ HTTP 200 | — | — |

**Nav extraite (header)** : Boutique · Découvrir · Épicerie créole (mega) · Professionnels · Contactez-nous · panier · wishlist · connexion.

### Playwright headless — desktop 1280 px

| # | Contrôle | Résultat | Note QA |
|---|----------|----------|---------|
| D1 | Logo C-Kreyol | ✅ | alt `C-Kreyol` · ~115×40 px |
| D3 | Nav principale | ✅ partiel | Boutique · Découvrir · Professionnels visibles dans `#top_menu` |
| D4 | Pas Producteurs nav | ✅ | |
| D5 | Mega Découvrir | ✅ | panel visible au clic · Épicerie créole dedans |
| D6 | Épicerie créole | ✅ | lien 200 |
| D11 | Overflow 1280 | ✅ | scrollW = clientW = 1280 |
| D12 | Header identique 3 URLs | ✅ | même chrome |
| D7 | Recherche / panier | ⚠️ non testé clic | présents DOM |
| D8 | Sticky header | ⚠️ **réserve** | `getComputedStyle` → `position: static` malgré SCSS `sticky` |
| D9 | Contraste / hover | ☐ | **MOA écran requis** |
| D10 | Cohérence CK globale | ☐ | **MOA écran requis** |
| — | Contactez-nous desktop | ✅ | visible nav principale (1 lien visible · doublon mobile caché) |

### Playwright headless — mobile 390 px

| # | Contrôle | Résultat | Note QA |
|---|----------|----------|---------|
| M1 | Offcanvas | ✅ | ouverture OK (toggler mobile Odoo) |
| M2 | Nav mobile | ✅ | Boutique · Découvrir · Professionnels · Contactez-nous · Se connecter |
| M7 | Overflow 390 | ✅ | scrollW = clientW = 390 |
| M9 | Contactez-nous | ✅ | visible offcanvas |
| M3 | Mega mobile | ⚠️ non conclusif | Découvrir présent · panel mega non testé en profondeur |
| M5–M6 | Touch targets | ☐ | **MOA pouce requis** |
| M8 | Branding offcanvas | ☐ | **MOA écran requis** |

### Synthèse QA proxy — recommandation MOA A1

| Nature | Verdict QA proxy |
|--------|------------------|
| Contrat fonctionnel header | ✅ **OK technique** |
| Overflow 1280 / 390 | ✅ |
| Logo · nav · mega · Épicerie · pas Producteurs | ✅ |
| Sticky header | ⚠️ **Réserve technique** — à confirmer scroll MOA |
| Cohérence visuelle CK · contraste · hover | ☐ **MOA écran** (~10 min) |

**Proposition QA → MOA** : base solide pour **A1-OK avec réserve sticky** ou **A1-OK** si MOA confirme sticky acceptable au scroll manuel.

**Non recommandé sans MOA** : A1-KO sur base proxy seule.

---

## Chantier B — Post-merge PR #62 · proxy QA

**Instance** : `ckr-marketone-01` · module **19.0.19.0.1** · merge `388e515`

### Gate automatisée

| Contrôle | Résultat |
|----------|----------|
| Upgrade `-u dorevia_ckreyol_marketone` | ✅ |
| Gate 72 tests (tags 6.3 + sidebar + wishlist + lot3) | ✅ **72/72 · 0 failed** |
| Date | 2026-06-14 10:03 UTC |

### Smoke HTTP

| Route | Résultat |
|-------|----------|
| `/promotions` | ✅ → `/shop?marketone_mode=promo` |
| `/kits` | ✅ → `/shop?marketone_mode=pack` |
| `/shop?marketone_mode=promo` | ✅ 200 |
| `/shop?marketone_mode=pack` | ✅ 200 |
| `/shop` | ✅ 200 |

### Playwright headless — header boutique

| Contrôle | Résultat |
|----------|----------|
| Chip Promotions | ✅ |
| Chip Kits & Coffrets | ✅ |
| Canonical `/shop` | ✅ `link[rel=canonical]` présent |

### Non exécuté (recette navigateur MOA)

| Document | Statut |
|----------|--------|
| `RECETTE_MANUELLE_LOT6_3A_PROMO.md` | ☐ MOA |
| `RECETTE_MANUELLE_LOT6_3B_PACK.md` | ☐ MOA |
| SEO portes shop (canonical/noindex cas limites) | ☐ MOA |

---

## Limites du rôle QA temporaire

| Limite | Impact |
|--------|--------|
| Pas de jugement esthétique MOA | Cohérence CK · contraste · hover |
| Playwright headless | Pas touch réel · sticky scroll imparfait |
| Pas signature go-live | Verdicts A1 · B clôture = MOA uniquement |
| Chantiers séparés | Aucun mélange périmètres |

---

## Suite — rôle QA temporaire

| Action | Responsable |
|--------|-------------|
| Signer A1 après lecture rapport + écran rapide MOA | **MOA** |
| Exécuter grilles recette navigateur 6.3a / 6.3b | **MOA** (+ QA proxy si demandé) |
| GO A7 Git CK | **MOA** · après A1 |

---

*Rapport QA temporaire · Chantiers A & B séparés · 2026-06-14.*
