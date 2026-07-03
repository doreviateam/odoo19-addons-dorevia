# Note MOA — Clôture CK-UNIVERSE-BANNER-001 Lot A — Banner éditorial univers

| Champ | Valeur |
| --- | --- |
| Date | 3 juillet 2026 |
| Projet | C-Kréyòl Marketone — pages univers boutique |
| Destinataires | MOA, Produit, QA, Dev |
| Statut | **Clôturé techniquement** — commit `a3567caf` (3 juillet 2026) |
| Commit de référence | `a3567caf` — `feat(ck): CK-UNIVERSE-BANNER-001 Lot A bannière univers + tests CI stables` |
| Lot | **CK-UNIVERSE-BANNER-001 Lot A** (banner éditorial niveau 0 — Note 09) |
| Modules | `dorevia_ck_marketone_content` (modèle + template + tests) · `dorevia_ck_theme` (SCSS) |
| Versions livrées | `dorevia_ck_marketone_content` **19.0.1.82.0** · `dorevia_ck_theme` **19.0.1.120.0** |
| Base recette | `dorevia_ck_marketone_01` — http://localhost:18079 |
| Ticket | [`TICKET_DEV_UNIVERSE_BANNER_CK_NOTE_09_LOT_A.md`](TICKET_DEV_UNIVERSE_BANNER_CK_NOTE_09_LOT_A.md) |
| Cadrage | [`note_09.md`](note_09.md) · [`note_09_reponse.md`](note_09_reponse.md) |

---

## Synthèse exécutive

Le lot **réintroduit une bannière d'entrée d'univers** (`.ck-univers-banner`) sur les 4 rayons racine e-commerce : Épicerie, Boissons, Soin & Bien-être et Artisanat. Ce composant avait été retiré en Shop-U3 ; il est réactivé conformément à la Note 09 Lot A, sans toucher au header, à la navigation ni au tunnel d'achat.

Le parcours acheteur de référence reste inchangé :

> **Home → Univers → Rayon → Produit → Panier**

**Verdict QA : GO recette fonctionnelle.** Le comportement est conforme au cadrage : bannière uniquement sur les univers niveau 0, H1 unique, pas de régression sur `/shop` ni sur les sous-catégories. La recette navigateur en sandbox a validé le **mode fallback sans image** ; le mode image + accroche est couvert **structurellement** par test automatisé, mais la **validation visuelle finale** reste à faire après alimentation réelle des images et accroches BO sur les 4 univers.

**Clôture technique : confirmée** — commit `a3567caf` inclut l'implémentation Lot A, le correctif test CI et l'archivage des captures (cf. § Captures).

---

## Décision confirmée

| Règle fonctionnelle | Résultat recette |
| --- | --- |
| Bannière sur les 4 univers racine uniquement | **Conforme** — `.ck-univers-banner` présent sur Épicerie, Boissons, Soin, Artisanat |
| Pas de bannière sur `/shop` général | **Conforme** — H1 compact « Boutique C-Kréyòl » via `.ck-shop-intro--title-only` |
| Pas de bannière sur sous-catégorie | **Conforme** — H1 compact hérité de l'univers parent (ex. « Épicerie créole ») |
| Un seul H1 visible par page | **Conforme** — pas de doublon avec le titre natif Odoo |
| Pas de débordement horizontal mobile | **Conforme** — recette 390 px |
| Fallback sans image (`ck-univers-banner--no-image`) | **Conforme** — fond clair CK, texte brun, accent terracotta, pas de scrim |

Hors périmètre Lot A (inchangé) : accents couleur par univers (`ck_banner_variant`, Lot B) · fiche produit · nav/header · nettoyage backlog tuiles sous-familles inactives.

---

## Ce que voit le visiteur

| Page | Bannière | Titre (H1) |
| --- | --- | --- |
| `/shop` | Absente | « Boutique C-Kréyòl » (compact) |
| Univers racine (×4) | Présente — eyebrow « Univers », titre, séparateur terracotta | H1 unique dans la bannière |
| Sous-catégorie | Absente | H1 compact hérité de l'univers parent |

En mode fallback (état actuel sandbox) : fond `#F5F0EB`, texte `#3E2723`, accent `#C75B3A`, pas de photo ni d'accroche.

En mode complet (après alimentation BO) : image native catégorie + scrim brun chaud + accroche `ck_subtitle` optionnelle — rendu à valider visuellement par la MOA une fois le contenu renseigné.

---

## Recette effectuée

| Zone | Desktop 1280 | Mobile 390 | Commentaire |
| --- | ---: | ---: | --- |
| `/shop` | OK | OK | Pas de `.ck-univers-banner` · H1 compact conforme |
| Univers racines (×4) | OK | OK | Bannière + H1 unique sur chaque rayon |
| Sous-catégorie | OK | OK | Pas de bannière · H1 hérité « Épicerie créole » |
| Fallback no-image | OK | OK | État réel sandbox — les 4 univers sans `image_1920` ni `ck_subtitle` |
| Routes GET | OK | n/a | `/shop` + 4 univers + sous-catégorie → HTTP 200 |
| Tests lot (`dorevia_ck_universe_banner`) | OK | n/a | **0 failed / 0 error** |
| Non-régression globale | OK* | n/a | *1 timeout helper à 12 s · test isolé repassé OK |

Recette exécutée sur `dorevia_ck_marketone_01` après upgrade OK des modules.

### Exécution tests

Tag `dorevia_ck_universe_banner` : couverture Q1–Q6 du ticket (présence/absence bannière, H1 unique, fallback sans image, image + accroche en catégorie éphémère).

**Correctif test CI** (commit `a3567caf`) : dans `test_ck_shop_universe_banner.py`, le helper `_create_root_category` crée un produit publié minimal rattaché à la catégorie de test — Odoo masque les catégories publiques vides.

### Limite recette — mode image + accroche

| Niveau | Couverture | Statut |
| --- | --- | --- |
| Structure HTML/CSS (image, scrim, accroche, `aria-hidden`) | Test automatisé `test_banner_with_image_and_subtitle` | **OK** |
| Rendu visuel réel sur les 4 univers catalogue | Images et `ck_subtitle` absents en sandbox BO | **À faire** après alimentation MOA |

---

## Captures

Archivées dans [`docs/design/maquette_01.2/captures/ck_universe_banner_20260703/`](../design/maquette_01.2/captures/ck_universe_banner_20260703/) :

| Fichier | Contexte |
| --- | --- |
| [`ck_universe_banner_desktop_1280.png`](../design/maquette_01.2/captures/ck_universe_banner_20260703/ck_universe_banner_desktop_1280.png) | Desktop 1280 px — univers Épicerie (mode fallback) |
| [`ck_universe_banner_mobile_390.png`](../design/maquette_01.2/captures/ck_universe_banner_20260703/ck_universe_banner_mobile_390.png) | Mobile 390 px — univers Épicerie (mode fallback) |

---

## Actions avant clôture définitive

| Acteur | Action | Statut |
| --- | --- | --- |
| **Dev** | Committer l'implémentation Lot A + correctif fixture `test_ck_shop_universe_banner.py` | **Fait** — `a3567caf` (3 juillet 2026) |
| **Dev / QA** | Archiver les captures de recette dans le dossier projet | **Fait** — `a3567caf` (3 juillet 2026) |
| **MOA** | Alimenter `image_1920` et `ck_subtitle` des 4 univers en BO (Website → eCommerce → Catégories) | **À faire** pour démo commerciale aboutie |
| **MOA / QA** | Passe visuelle post-alimentation (image + scrim + accroche sur au moins un univers) | **À faire** après alimentation BO |

---

## Contrôles rapides MOA (3 minutes)

Sur `localhost:18079` ou URL démo :

1. **`/shop`** → pas de bannière · H1 « Boutique C-Kréyòl ».
2. **Clic header « Épicerie »** (CK-NAV-005) → bannière visible · un seul H1 · pas de scroll horizontal en 390 px.
3. **Sous-catégorie Épicerie** → pas de bannière · H1 « Épicerie créole ».
4. Échantillon Boissons / Soin / Artisanat.
5. *(Après alimentation BO)* vérifier image + accroche sur au moins un univers.

---

## Verdict MOA confirmé

```text
CK-UNIVERSE-BANNER-001 Lot A
→ Clôturé techniquement (commit a3567caf)
→ Exploitable en sandbox en mode fallback
→ Démo commerciale aboutie après alimentation BO des images et ck_subtitle des 4 univers
→ Lot B variantes couleur (ck_banner_variant) : NO GO — après recette visuelle Lot A alimenté
```

---

*Note MOA — C-Kréyòl Marketone · Clôture CK-UNIVERSE-BANNER-001 Lot A — 3 juillet 2026*
