# Recette visuelle QA — Section 4 « Acheter par univers » V1

| Champ | Valeur |
|-------|--------|
| **Public** | Contrôleur qualité · MOA |
| **Date** | 2026-06-17 |
| **Périmètre** | Section 4 home uniquement — **recette visuelle** (pas de revalidation architecture globale home) |
| **Verdict attendu** | GO visuel · GO sous réserves · NO GO |
| **Instance** | `dorevia_ck_marketone_01` — http://localhost:18079/?db=dorevia_ck_marketone_01 |
| **Modules** | `dorevia_ck_marketone_content` ≥ **`19.0.1.21.7`** · `dorevia_ck_theme` ≥ **`19.0.1.30.3`** |
| **Branche / PR** | `feat/ck-home-section4-univers` — [PR #76](https://github.com/doreviateam/odoo19-addons-dorevia/pull/76) |
| **Références code** | `home_univers.py` · `website.scss` (`.ck-univers-cards`) · `ck_snippet_univers_cards.xml` · [`NOTE_ARCHITECTURE_SECTION4_UNIVERS_V1.md`](./NOTE_ARCHITECTURE_SECTION4_UNIVERS_V1.md) |

---

## 1. Ordre de mission QA

**Objectif** : valider visuellement et fonctionnellement la **Section 4 « Acheter par univers »** sur la home CK Marketone : 3 cards navigation catalogue **indépendantes et modifiables une par une**, visuels MOA, overlay chaud/sombre, texte blanc, CTA pill blanc, liens catégories BO, édition Website Builder par card.

**Hors périmètre** (ne pas bloquer sur ces points) :

- refonte `/shop` ou fiches produit ;
- Section 3 « Nos coups de cœur » (déjà recettée — cf. `RECETTE_VISUELLE_SECTION3_V1_1.md`) ;
- contenu détaillé de la section « Coffrets découverte » (Section 5) — vérifier uniquement son **positionnement** sous S4 ;
- ajout d'une 4ᵉ card ou intégration de « Packs & découvertes » dans la grille S4.

**Prérequis environnement** :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 --http-port=8079 --no-http \
  -u dorevia_ck_theme,dorevia_ck_marketone_content --stop-after-init
docker restart sandbox-odoo19-odoo-1
```

Puis **hard refresh** navigateur (`Cmd+Shift+R` / `Ctrl+Shift+R`) ou fenêtre privée sur `/`.

**Viewports obligatoires** :

| Viewport | Largeur | Usage |
|--------|---------|--------|
| Desktop | **1280** | Grille 3 colonnes · en-tête section |
| Tablette | **768** | Grille 2 colonnes |
| Mobile | **390** | 1 colonne · lisibilité overlay / CTA |

**Captures à déposer** : `docs/design/maquette_01.2/captures/recette_section4_univers_v1/`

| Fichier suggéré | Contenu |
|-----------------|---------|
| `s4_desktop_1280_full.png` | Section complète desktop (en-tête + 3 cards) |
| `s4_desktop_1280_card_epicerie.png` | Zoom card Épicerie créole |
| `s4_desktop_1280_hover.png` | Card au survol (élévation + zoom image + CTA) |
| `s4_tablet_768_grid.png` | Grille 2 colonnes |
| `s4_mobile_390_full.png` | Section complète mobile |
| `s4_editor_mode_visuel_epicerie.png` | Mode édition — zone « Visuel Épicerie créole » sélectionnée |
| `s4_editor_mode_visuel_soin.png` | Mode édition — zone « Visuel Soin & bien-être » sélectionnée |
| `s4_editor_after_single_card_change.png` | Après remplacement image **Épicerie seule** — Soin et Artisanat inchangés |

---

## 2. Jeu de données de référence (instance recette)

Vérifier en BO (**Site web → eCommerce → Catégories e-commerce**) avant la recette :

| Card home | Catégorie BO attendue | Lien typique |
|-----------|----------------------|--------------|
| Épicerie créole | **Épicerie créole** (ou **Épicerie**) | `/shop/category/epicerie-1` (slug peut varier) |
| Soin & bien-être | **Maison & bien-être** | `/shop/category/maison-bien-etre-2` |
| Artisanat & culture | **Artisanat** | `/shop/category/artisanat-3` |

**Visuels par défaut** (assets module, remplaçables en éditeur) :

| Card | Fichier |
|------|---------|
| Épicerie créole | `ck_univers_epicerie.jpg` — épices / madras |
| Soin & bien-être | `ck_univers_soin.jpg` — savons / lumière tropicale |
| Artisanat & culture | `ck_univers_artisanat.jpg` — atelier paniers / céramique CK |

---

## 3. Checklist — positionnement sur la home

| # | Contrôle | Attendu | ☐ | Note |
|---|----------|---------|---|------|
| P1 | Ordre des sections | **S3 Coups de cœur** → **S4 Acheter par univers** → **Coffrets découverte** | | |
| P2 | Ancienne section pills | **Absente** (pas de `Nos univers` / pills catégories legacy) | | |
| P3 | Packs dans la grille S4 | **Absent** — « Packs & découvertes » n'est **pas** une card de la grille | | |
| P4 | Carrousel | **Absent** dans S4 (pas de carousel Bootstrap) | | |

---

## 4. Checklist visuelle — en-tête de section

| # | Contrôle | Attendu visuel | ☐ | Note |
|---|----------|----------------|---|------|
| H1 | Titre | **« Acheter par univers »** | | |
| H2 | Intro | **« Trois univers pour entrer dans la boutique en un clic. »** | | |
| H3 | Alignement | En-tête **aligné à gauche** (pas centré) | | |
| H4 | Lisibilité | Intro en gris muted, largeur confortable (pas pleine largeur écran) | | |

---

## 5. Checklist visuelle — cards univers (×3)

Structure attendue **par card** :

```text
[Photo plein fond — object-fit cover]
[Overlay chaud/sombre modéré en bas]
  Titre (blanc)
  Description (blanc légèrement atténué)
  [CTA pill blanc]
```

| # | Contrôle | Attendu visuel | ☐ | Note |
|---|----------|----------------|---|------|
| U1 | Nombre de cards | **Exactement 3** | | |
| U2 | Titres | **Épicerie créole** · **Soin & bien-être** · **Artisanat & culture** | | |
| U3 | Descriptions | Textes livrés module (cf. `home_univers.py`) — lisibles sur overlay | | |
| U4 | CTA | **« Voir l'épicerie »** · **« Découvrir les soins »** · **« Explorer l'artisanat »** — boutons **pill blancs** | | |
| U5 | Overlay | Dégradé **chaud/sombre modéré** — photo visible en haut, texte lisible en bas (pas d'aplat opaque) | | |
| U6 | Texte | **Blanc** sur overlay (titre + description) | | |
| U7 | Images | Visuels **thématiques CK** (pas placeholders Odoo, pas stocks génériques type carottes/spa) | | |
| U8 | Ratio / crop | Image couvre la card (`object-fit: cover`), pas d'étirement | | |
| U9 | Hover desktop | Légère élévation card + zoom image (~3 %) + CTA renforcé | | |
| U10 | Grille responsive | 3 col. ≥992px · 2 col. tablette · 1 col. mobile | | |

---

## 6. Checklist fonctionnelle — navigation

| # | Contrôle | Attendu | ☐ | Note |
|---|----------|---------|---|------|
| N1 | Clic card Épicerie | Redirige vers la **catégorie épicerie** BO (pas `/shop` générique) | | |
| N2 | Clic card Soin | Redirige vers **Maison & bien-être** | | |
| N3 | Clic card Artisanat | Redirige vers **Artisanat** | | |
| N4 | Page catégorie | Liste produits cohérente avec l'univers (pas d'erreur 404) | | |

---

## 7. Checklist — édition Website Builder (**obligatoire**)

> **Règle MOA** : chaque card est une brique **indépendante**. Modifier l'image, le titre ou la description de **Épicerie** ne doit **pas** impacter Soin ni Artisanat.

### 7.1 Zones éditables par card

| Card | Zone éditable (`data-name`) | Image (`o_editable_media`) | Titre / description |
|------|-----------------------------|----------------------------|---------------------|
| Épicerie créole | **Univers Épicerie créole** | Oui — clic sur la photo | Oui |
| Soin & bien-être | **Univers Soin & bien-être** | Oui | Oui |
| Artisanat & culture | **Univers Artisanat & culture** | Oui | Oui |

*Hors édition inline aujourd'hui : libellé CTA (`span.ck-univers-card__cta`).*

### 7.2 Scénario de recette — modification **d'une seule** card

| # | Étape | Attendu | ☐ | Note |
|---|-------|---------|---|------|
| E1 | Activer **Modifier** sur `/` | Barre d'édition Odoo visible | | |
| E2 | Clic photo **Épicerie** | Sélection de la card **« Univers Épicerie créole »** (sous-snippet) — pas le bloc section global | | |
| E3 | Remplacer l'image Épicerie | Nouvelle image visible sur **cette** card seulement | | |
| E4 | Vérifier Soin + Artisanat | **Inchangés** (mêmes visuels qu'avant E3) | | |
| E5 | Modifier titre **Soin** (texte test) | Seul le titre Soin change ; Épicerie + Artisanat intacts | | |
| E6 | Sauvegarder + recharger `/` | Modifications conservées | | |
| E7 | Répéter E2 sur **Artisanat** | Zone **« Univers Artisanat & culture »** distincte des deux autres | | |

### 7.3 Persistance post-upgrade (spot check)

| # | Contrôle | Attendu | ☐ | Note |
|---|----------|---------|---|------|
| E8 | Après upgrade module (cf. §1) | Image custom Épicerie **non écrasée** | | |
| E9 | En-tête section | Titre + intro section restent éditables **au niveau section** (pas liés aux cards) | | |

---

## 8. Non-régression rapide

| # | Contrôle | Attendu | ☐ | Note |
|---|----------|---------|---|------|
| R1 | Section 3 | Toujours présente et inchangée visuellement (spot check) | | |
| R2 | Header / footer site | Pas de régression layout global | | |
| R3 | Console navigateur | Pas d'erreur JS bloquante au chargement home | | |

---

## 9. Prérequis dev — **GO avant intervention QA**

| Contrôle | Statut | Détail |
|----------|--------|--------|
| Instance recette à jour | ✅ | `dorevia_ck_marketone_01` — modules `21.7` / `30.3` |
| Tests auto Section 4 | ✅ | **12/12** — tag `dorevia_ck_marketone_home_section4` |
| Fiche de recette | ✅ | Ce document |

---

## 10. Tests automatisés (référence QA — rejeu possible)

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 --http-port=8079 --no-http \
  -u dorevia_ck_marketone_content \
  --test-tags dorevia_ck_marketone_home_section4 \
  --stop-after-init
```

**Attendu** : `0 failed, 0 error(s)` (12 tests post-install).

---

## 11. PV de recette (à remplir par QA)

| Champ | Valeur |
|-------|--------|
| **Recetteur** | QA Codex |
| **Date** | 2026-06-17 |
| **Commit / version module** | `dorevia_ck_marketone_content` `19.0.1.21.7` · `dorevia_ck_theme` `19.0.1.30.3` |
| **Verdict global** | ☑ GO · ☐ GO sous réserves · ☐ NO GO |

**Réserves** (si GO sous réserves) :

1. Sans objet.

**Bloquants** (si NO GO) :

1. Sans objet.

**Constat de validation QA** :

1. §3–§6 validés : ordre home conforme (`S3` → `S4` → `Coffrets découverte`), ancienne section pills absente, 3 cards visibles, responsive OK en `1280`, `768` et `390`, pas d'overflow horizontal.
2. Navigation conforme : `Épicerie créole` → `/shop/category/epicerie-1`, `Soin & bien-être` → `/shop/category/maison-bien-etre-2`, `Artisanat & culture` → `/shop/category/artisanat-3`, avec `Coffrets découverte` visible sous S4 avant le bloc Pro.
3. Rejeu §7 concluant sur la structure éditeur : le DOM expose bien la section `s_ck_univers_cards` et trois sous-snippets distincts `s_ck_univers_card` (`Univers Épicerie créole`, `Univers Soin & bien-être`, `Univers Artisanat & culture`), chacun portant son média `img.o_editable_media`.
4. En mode édition, l'ouverture du sélecteur média a été reconstatée depuis la card Épicerie puis depuis la card Soin ; le défaut initial de sélection unique du bloc global n'a pas été reproduit sur ce build.
5. Cycle complet de persistance rejoué sur la card Épicerie : modification enregistrée en base, présence confirmée après redémarrage HTTP, puis conservation confirmée après `-u dorevia_ck_theme,dorevia_ck_marketone_content` suivi d'un redémarrage du conteneur.
6. L'état d'origine a été restauré après test ; contrôle final live OK : Épicerie `ck_univers_epicerie.jpg`, Soin `ck_univers_soin.jpg`, Artisanat `ck_univers_artisanat.jpg`.
7. Spot check non-régression OK : Section 3 `Nos coups de cœur` toujours présente et inchangée visuellement sur les viewports testés.
8. Preuves déposées dans `docs/design/maquette_01.2/captures/recette_section4_univers_v1/` : `s4_desktop_1280_full.png`, `s4_desktop_1280_card_epicerie.png`, `s4_tablet_768_grid.png`, `s4_mobile_390_full.png`, `s4_editor_mode_visuel_epicerie.png`, `s4_editor_mode_visuel_soin.png`, `s4_editor_after_single_card_change.png`.

---

*Recette visuelle Section 4 « Acheter par univers » V1 — 2026-06-17 · **QA GO** · merge PR #76.*
