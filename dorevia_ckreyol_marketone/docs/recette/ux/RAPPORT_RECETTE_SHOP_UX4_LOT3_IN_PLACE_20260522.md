# Rapport recette MOA — UX-4 Lot 3 — Preview « Voir » in-place

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-05-22 |
| **Version** | `19.0.15.13.1` (correctif recette interactions preview) |
| **Branche** | `feat/marketone-ux4-lot3-preview-voir` |
| **PR** | **#14** — [`[CK][UX-4] Lot 3 — Preview Voir sans sortie de /shop`](https://github.com/doreviateam/odoo19-addons-dorevia/pull/14) |
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079/shop |
| **Exécuteur** | Codex (Playwright headless + tests auto sandbox) |
| **Référence recette** | [`RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md`](RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md) § Lot 3 |

---

## Contrôle avant recette

| Contrôle | Attendu | Observé | Verdict |
|----------|---------|---------|---------|
| Branche | `feat/marketone-ux4-lot3-preview-voir` | OK | OK |
| Version module | `19.0.15.13.x` | `19.0.15.13.1` | OK |
| Base | `ckr-marketone-01` | OK | OK |
| URL | `/shop` HTTP 200 | OK | OK |
| PR | #14 · pas de merge | OK | OK |

---

## Tests automatisés

```bash
docker run … odoo -c /etc/odoo/odoo.conf -d ckr-marketone-01 \
  --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_shop_in_place --http-port=8079
```

**Résultat : 13/13 · 0 failed**

---

## Correctif recette (13.0.1)

**Symptôme initial :** panier depuis preview offcanvas — compteur header inchangé (`0→0`) · handlers Lots 1–2 non attachés au fragment injecté.

**Cause :** contenu preview injecté dynamiquement sans `startInteractions` · sélecteur panier Lot 2 limité à `.marketone-shop` (offcanvas hors grille).

**Correctif :**

- `marketone_shop_preview.js` — `startInteractions` / `stopInteractions` sur fragment preview ;
- `marketone_shop_cart_add.js` — sélecteur étendu à `.marketone-shop-preview .marketone-shop-card-cart`.

**Recontrôle post-correctif :** panier preview `0→1` · wishlist preview `0→1` · URL `/shop` conservée.

---

## Critères GO G3.1–G3.10

| ID | Critère | Verdict | Détail |
|----|---------|---------|--------|
| **G3.1** | Preview visible · URL `/shop` | **OK** | Clic « Voir » (Maniocookies) · pas de navigation fiche |
| **G3.2** | Desktop offcanvas droit non modal | **OK** | `#marketone_shop_preview_offcanvas.show` · `data-bs-backdrop=false` · grille visible |
| **G3.3** | Mobile 390 px inline · une preview | **OK** | `innerWidth=390` · `scrollWidth=390` · slot `--open` unique |
| **G3.4** | Photo + titre → fiche | **OK** | href `/shop/maniocookies-sales-la-platine-7` conservés |
| **G3.5** | Contenu V1 minimal | **OK** | Image · titre · prix · origines · collections · description · CTA |
| **G3.6** | Panier depuis preview · `/shop` | **OK** | Compteur `0→1` post-correctif 13.0.1 |
| **G3.7** | Wishlist depuis preview · `/shop` | **OK** | Toggle add · compteur cohérent · URL `/shop` |
| **G3.8** | « Voir la fiche complète » | **OK** | Lien présent · navigation fiche validée (B10) |
| **G3.9** | Fermeture × / ESC / re-clic | **OK** | Pas d’erreur JS bloquante (polices Google Fonts : réserve non bloquante) |
| **G3.10** | Régression B + tests auto | **OK** | B1 · B4 · B7 · B8 · B9 · B10 · 13/13 auto |

---

## Scénario L3

| Étape | Verdict | Observé |
|-------|---------|---------|
| L3.1 | **OK** | Preview ouverte · URL `/shop` |
| L3.2 | **OK** | Offcanvas droit · pas de modal |
| L3.3 | **OK** | Inline sous tuile · 390 px sans débordement |
| L3.4 | **OK** | Lien fiche complète → navigation fiche |
| L3.5 | **OK** | Photo / titre tuile → fiche (gel MOA) |
| L3.6 | **OK** | Fermeture ESC + re-clic « Voir » |
| L3.7 | **OK** | Contenu V1 complet |
| L3.8 | **OK** | Panier + wishlist depuis preview |
| **L3.V1** | **Réserve documentaire** | **0 produit** multi-variante / configurable publié sur 50 produits catalogue — fallback non rejoué en conditions réelles |

---

## Régression Lot 3

| Section | Verdict | Détail |
|---------|---------|--------|
| **B1** | **OK** | `/shop` · `/shop/cart` · `/shop/wishlist` HTTP 200 |
| **B4** | **OK** | 24 tuiles · CTA Voir · coquille preview · structure conversion conservée |
| **B7** | **OK** | Toggle wishlist grille in-place |
| **B8** | **OK** | Panier grille in-place |
| **B9** | **OK** | Preview « Voir » in-place · pas de modal |
| **B10** | **OK** | Destinations secondaires (titre → fiche) |

---

## Captures

| ID | Fichier |
|----|---------|
| C-L3-1 | [`capture_ux4_l3_desktop_open_20260522.png`](capture_ux4_l3_desktop_open_20260522.png) |
| C-L3-2 | [`capture_ux4_l3_mobile_open_20260522.png`](capture_ux4_l3_mobile_open_20260522.png) |
| C-L3-3 | [`capture_ux4_l3_desktop_content_20260522.png`](capture_ux4_l3_desktop_content_20260522.png) |
| C-L3-4 | [`capture_ux4_l3_mobile_closed_20260522.png`](capture_ux4_l3_mobile_closed_20260522.png) |

Résultat JSON : [`recette_ux4_l3_20260522_result.json`](recette_ux4_l3_20260522_result.json)

---

## Doctrine MOA — preview légère

| Contrôle | Verdict |
|----------|---------|
| Pas de modal popup | **OK** |
| Pas de deep-link preview V1 | **OK** |
| Pas de configurateur dans preview | **OK** |
| Preview ≠ fiche produit bis | **OK** — contenu V1 minimal · lien fiche explicite |

---

## Verdict MOA proposé

| Verdict | Condition |
|---------|-----------|
| ☑ **GO avec réserve documentaire** | G3.1–G3.10 OK · L3.1–L3.8 OK · régression B4/B7/B8/B9/B10 OK · desktop + mobile 390 px · tests auto 13/13 |
| ☐ GO | — |
| ☐ NO GO | — |

**Réserves (non bloquantes) :**

1. **L3.V1** — aucun produit multi-variante / configurable publié en catalogue sandbox ; fallback fiche non démontré en conditions réelles (règle couverte par tests auto `_marketone_preview_full_allowed`).
2. Polices Google Fonts — erreurs réseau CORS sandbox (héritage Lots 1–2).

**Règle merge :** verdict MOA formel requis avant merge PR #14.

---

## Grille d’exécution (mise à jour proposée)

| Date | Lot | Version | Exécuteur | Verdict | Rapport |
|------|-----|---------|-----------|---------|---------|
| 2026-05-22 | L3 | `19.0.15.13.1` | Codex | **GO avec réserve documentaire (proposé)** | ce document |
