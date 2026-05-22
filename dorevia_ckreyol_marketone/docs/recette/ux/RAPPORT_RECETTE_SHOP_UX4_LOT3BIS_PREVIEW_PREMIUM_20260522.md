# Rapport recette MOA — UX-4 Lot 3bis — Preview premium

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-05-22 |
| **Version** | `19.0.15.13.3` |
| **Branche** | `feat/marketone-ux4-lot3bis-preview-premium` |
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079/shop |
| **Exécuteur** | Codex |
| **Référence recette** | [`RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md`](RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md) — Lot 3bis |

---

## Pré-contrôles

| Contrôle | Observé | Verdict |
|----------|---------|---------|
| Branche | `feat/marketone-ux4-lot3bis-preview-premium` | OK |
| Version module | `19.0.15.13.3` | OK |
| Upgrade module | `-u dorevia_ckreyol_marketone` exécuté | OK |
| `/shop` avec base `ckr-marketone-01` | HTTP 200 | OK |

---

## Tests automatisés

Commande exécutée :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone \
  --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_shop_in_place,dorevia_marketone_shop_wishlist,dorevia_marketone_shop_regression,dorevia_marketone_shop_filter_state,dorevia_marketone_shop_sidebar,dorevia_marketone_shop_sidebar_collections,dorevia_marketone_smoke,dorevia_marketone_lot3_shop \
  --http-port=8073
```

**Résultat : 1 failed, 0 error(s) / 88 tests.**

Échec constaté :

| Test | Cause |
|------|-------|
| `TestMarketoneShopInPlacePreview.test_shop_grid_preview_shell_and_cta_data` | Le test attend la chaîne brute `Fermer l'aperçu`, alors que le HTML rendu contient l’attribut échappé `aria-label="Fermer l&#39;aperçu"` |

---

## Blocage assets / SCSS

Pendant la génération des assets, Odoo remonte :

```text
Internal Error: Incompatible units: 'vw' and 'rem'.
```

Le bundle concerné inclut notamment :

```text
/dorevia_ckreyol_marketone/static/src/scss/_shop_product_preview.scss
```

Contrôle navigateur :

| Surface | Observé | Verdict |
|---------|---------|---------|
| Desktop | Bandeau rouge `A CSS error occured, using an old style to render this page` + toast erreur de style | KO |
| Mobile 390 px | Même erreur CSS visible | KO |

Ce point bloque la recette visuelle Lot 3bis, car le jalon porte précisément sur la finition premium de la preview.

---

## Smoke fonctionnel observé

| Contrôle | Observé | Verdict |
|----------|---------|---------|
| `/shop` | Page chargée avec base `ckr-marketone-01` | OK |
| Mobile | Pas de débordement horizontal mesuré | OK |
| Preview mobile | Inline sous tuile | OK |
| Fermeture mobile | Bouton **Fermer** replie la preview | OK |
| Titre mobile | `Découvrir le produit` visible | OK |

Le smoke fonctionnel ne compense pas le blocage visuel et les tests rouges.

---

## Captures

| ID | Fichier |
|----|---------|
| C-V3bis-1 | [`capture_ux4_l3bis_13_3_desktop_open_20260522.png`](capture_ux4_l3bis_13_3_desktop_open_20260522.png) |
| C-V3bis-2 | [`capture_ux4_l3bis_13_3_desktop_closed_20260522.png`](capture_ux4_l3bis_13_3_desktop_closed_20260522.png) |
| C-V3bis-3 | [`capture_ux4_l3bis_13_3_mobile_open_20260522.png`](capture_ux4_l3bis_13_3_mobile_open_20260522.png) |
| C-V3bis-4 | [`capture_ux4_l3bis_13_3_mobile_closed_20260522.png`](capture_ux4_l3bis_13_3_mobile_closed_20260522.png) |

Résultat JSON : [`recette_ux4_l3bis_13_3_visual_result.json`](recette_ux4_l3bis_13_3_visual_result.json)

---

## Verdict MOA

| Verdict | Statut |
|---------|--------|
| **GO MOA Lot 3bis** | ☐ |
| **NO GO** | ☑ |

**Verdict : NO GO Lot 3bis.**

Motifs :

- tests auto rouges : `1 failed / 88` ;
- erreur SCSS `Incompatible units: 'vw' and 'rem'` ;
- erreur de style visible en desktop et mobile ;
- la recette visuelle premium ne peut pas être validée tant que le bundle frontend ne compile pas proprement.

## Actions attendues

1. Corriger la règle SCSS dans `_shop_product_preview.scss` qui mélange `vw` et `rem`.
2. Aligner le test `test_shop_grid_preview_shell_and_cta_data` sur le rendu HTML échappé ou sur un sélecteur/attribut robuste.
3. Relancer upgrade + tests auto.
4. Rejouer la recette visuelle desktop/mobile Lot 3bis.

---

## Reprise corrective — relance recette

| Champ | Valeur |
|-------|--------|
| **Date reprise** | 2026-05-22 |
| **Version** | `19.0.15.13.3` |
| **Branche** | `feat/marketone-ux4-lot3bis-preview-premium` |
| **Base** | `ckr-marketone-01` |

### Corrections constatées

| Point | Observé | Verdict |
|-------|---------|---------|
| Test `Fermer l'aperçu` | Assertion alignée sur `aria-label="Fermer l&#39;aperçu"` | OK |
| SCSS `vw` / `rem` | Assets frontend générés sans erreur `Incompatible units` | OK |
| `/shop` desktop | Plus de bandeau rouge `A CSS error occured` | OK |
| `/shop` mobile 390 px | Plus de bandeau rouge `A CSS error occured` | OK |

### Tests automatisés reprise

Même commande que ci-dessus.

**Résultat reprise : 88/88 OK · 0 failed · 0 error(s).**

### Recette visuelle reprise

| Critère | Desktop | Mobile 390 px | Verdict |
|---------|---------|---------------|---------|
| V3bis.1 — Fond pastel CK | Panneau premium, fond chaud | Inline sans erreur CSS | OK |
| V3bis.2 — Image contain | Image cadrée dans cadre pastel | Image contain, lisible | OK |
| V3bis.3 — Titre | `Découvrir le produit` | `Découvrir le produit` | OK |
| V3bis.4 — Fermeture | Croix lisible et cliquable | Bouton texte cliquable, libellé visuellement un peu tronqué (`Ferme`) | **Réserve** |
| V3bis.5 — Origines / Collections | Chips pastel visibles | Chips pastel visibles en scroll | OK |
| V3bis.6 — CTA panier | CTA pleine largeur respirant | Présent plus bas dans la preview | OK |
| V3bis.7 — Wishlist | Bouton coeur intégré au bloc actions | Non bloquant, couvert par tests Lot 3 | OK |
| V3bis.8 — Lien fiche complète | Lien secondaire séparé | Présent plus bas dans la preview | OK |
| V3bis.9 — Respiration globale | Bonne hiérarchie desktop | Mobile plus dense par contrainte 2 colonnes | OK avec réserve mineure |
| V3bis.10 — Palette CK | Pastel · terracotta · sauge | Cohérente | OK |
| V3bis.11 — Ressenti maison de sélection | Oui côté desktop | Acceptable côté mobile | OK |

### Smoke fonctionnel reprise

| Contrôle | Observé | Verdict |
|----------|---------|---------|
| URL `/shop` conservée | Desktop + mobile | OK |
| Fermeture preview | Desktop croix · mobile bouton exact `Fermer l'aperçu` | OK |
| Mobile sans débordement | `scrollWidth=390` pour `innerWidth=390` | OK |
| Console navigateur | Pas d’erreur bloquante sur la passe | OK |

### Captures reprise

| ID | Fichier |
|----|---------|
| C-V3bis-R1 | [`capture_ux4_l3bis_13_3_reprise_desktop_open_20260522.png`](capture_ux4_l3bis_13_3_reprise_desktop_open_20260522.png) |
| C-V3bis-R2 | [`capture_ux4_l3bis_13_3_reprise_desktop_closed_20260522.png`](capture_ux4_l3bis_13_3_reprise_desktop_closed_20260522.png) |
| C-V3bis-R3 | [`capture_ux4_l3bis_13_3_reprise_mobile_open_20260522.png`](capture_ux4_l3bis_13_3_reprise_mobile_open_20260522.png) |
| C-V3bis-R4 | [`capture_ux4_l3bis_13_3_reprise_mobile_closed_20260522.png`](capture_ux4_l3bis_13_3_reprise_mobile_closed_20260522.png) |

JSON reprise : [`recette_ux4_l3bis_13_3_reprise_visual_result.json`](recette_ux4_l3bis_13_3_reprise_visual_result.json) · [`recette_ux4_l3bis_13_3_reprise_mobile_result.json`](recette_ux4_l3bis_13_3_reprise_mobile_result.json)

## Verdict reprise

| Verdict | Statut |
|---------|--------|
| **GO MOA Lot 3bis avec réserve visuelle mineure** | ☑ |
| NO GO | ☐ |

**Verdict reprise : GO MOA Lot 3bis avec réserve visuelle mineure.**

Réserve :

- **R1 mobile 390 px** — le bouton texte de fermeture inline est cliquable et fonctionnel, mais son libellé peut apparaître tronqué (`Ferme`) dans la colonne produit. À harmoniser si l’on veut un rendu mobile parfaitement premium.

---

## Reprise V3bis.12 — retrait naturel

| Champ | Valeur |
|-------|--------|
| **Date reprise** | 2026-05-22 |
| **Version** | `19.0.15.13.4` |
| **Branche** | `feat/marketone-ux4-lot3bis-preview-premium` |
| **Commit** | `0ab149a` |
| **Base** | `ckr-marketone-01` |
| **URL** | `http://localhost:18079/shop` |

### Préparation

| Contrôle | Résultat |
|----------|----------|
| `git pull origin feat/marketone-ux4-lot3bis-preview-premium` | Déjà à jour |
| Upgrade module `-u dorevia_ckreyol_marketone` | OK |
| Redémarrage Odoo long-running | OK |
| Tests automatisés recette élargie | **88/88 OK · 0 failed · 0 error(s)** |

### V3bis.12 — Desktop

| Point | Observé | Verdict |
|-------|---------|---------|
| D1 — Ouvrir preview | Preview ouverte depuis `Voir`, URL `/shop` conservée | OK |
| D2 — Clic hors panneau | Retrait naturel, preview fermée, pas de navigation | OK |
| D3 — Scroll page hors preview | Retrait naturel, preview fermée, grille navigable | OK |
| D4 — Interaction dans preview | Interaction interne conservée sans fermeture ; à 1280x900 la preview n'a pas de scroll interne réel | OK |
| D5 — Smoke G3.9 | Croix, ESC et re-clic `Voir` ferment proprement | OK |
| D6 — Console | Aucune erreur JS bloquante ; pas de bandeau erreur CSS | OK |

### V3bis.12 — Mobile 390 px

| Point | Observé | Verdict |
|-------|---------|---------|
| M1 — Ouvrir inline | Preview inline ouverte, URL `/shop` conservée | OK |
| M2 — Scroll page hors preview | Retrait propre, preview fermée | OK |
| M3 — Interaction interne | Interaction dans la preview sans fermeture | OK |
| M4 — Tap hors preview | Retrait propre | OK |
| M5 — Bouton `Fermer` | Fermeture fonctionnelle via `aria-label="Fermer l'aperçu"` | OK |
| M6 — Largeur 390 px | `scrollWidth=390`, pas de débordement horizontal | OK |

### Garde-fous MOA

| Contrôle | Résultat |
|----------|----------|
| Effet modal / backdrop | Aucun `.modal.show`, `.modal-backdrop` ou `.offcanvas-backdrop` actif |
| Grille navigable | OK après retrait naturel |
| URL | `/shop` conservée sur desktop et mobile |
| Console | Aucune erreur bloquante |
| Réserve R1 mobile | Maintenue comme réserve visuelle acceptée |

### Captures et JSON V3bis.12

| ID | Fichier |
|----|---------|
| C-V3bis-12-D1 | [`capture_ux4_l3bis_13_4_desktop_open_20260522.png`](capture_ux4_l3bis_13_4_desktop_open_20260522.png) |
| C-V3bis-12-D2 | [`capture_ux4_l3bis_13_4_desktop_after_grid_click_20260522.png`](capture_ux4_l3bis_13_4_desktop_after_grid_click_20260522.png) |
| C-V3bis-12-D3 | [`capture_ux4_l3bis_13_4_desktop_after_scroll_20260522.png`](capture_ux4_l3bis_13_4_desktop_after_scroll_20260522.png) |
| C-V3bis-12-D4 | [`capture_ux4_l3bis_13_4_desktop_scroll_inside_20260522.png`](capture_ux4_l3bis_13_4_desktop_scroll_inside_20260522.png) |

JSON V3bis.12 : [`recette_ux4_l3bis_13_4_retrait_result.json`](recette_ux4_l3bis_13_4_retrait_result.json)

## Verdict V3bis.12

| Verdict | Statut |
|---------|--------|
| **GO final Lot 3bis** | ☑ |
| NO GO | ☐ |

**Verdict V3bis.12 : GO final Lot 3bis.**

Le critère global de retrait naturel est validé : la preview ne se comporte pas comme une modale, la grille reste navigable, les fermetures G3.9 restent fonctionnelles et le mobile 390 px ne présente pas de débordement horizontal.
