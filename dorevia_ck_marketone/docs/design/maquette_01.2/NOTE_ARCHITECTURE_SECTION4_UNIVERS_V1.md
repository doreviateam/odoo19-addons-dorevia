# Note d'architecture MOA / QA — Section 4 · Acheter par univers

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Section** | Home V1 — Section 4 |
| **Instance recette** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **Statut doc** | **Révision 2026-06-17** — alignée sur `dorevia_ck_marketone_content` **≥ `19.0.1.21.7`** · `dorevia_ck_theme` **≥ `19.0.1.30.3`** |
| **Code** | `home_univers.py` · `home_discovery_pack.py` · `ck_snippet_univers_cards.xml` · `ck_snippet_univers_card.xml` · `ck_univers_plugin.js` · `website.scss` |
| **PR** | [#76](https://github.com/doreviateam/odoo19-addons-dorevia/pull/76) — **recette QA GO** |

---

## Guide simple (lire en premier)

### C'est quoi, concrètement ?

Sur la page d'accueil, le bloc **« Acheter par univers »** affiche **3 cartes navigation catalogue** (photo plein fond, overlay chaud/sombre, texte blanc, CTA pill blanc). Chaque card mène vers une **catégorie e-commerce** BO.

Ce n'est **pas** :
- un carrousel ;
- la section pills legacy « Nos univers » (`s_ck_category_links`) ;
- la grille « Packs & découvertes » (Section 5 — **Coffrets découverte**, sous S4).

### Les 3 univers (figés V1)

| Card home | Catégorie BO | CTA |
|-----------|--------------|-----|
| **Épicerie créole** | `Épicerie créole` ou `Épicerie` | Voir l'épicerie |
| **Soin & bien-être** | `Maison & bien-être` | Découvrir les soins |
| **Artisanat & culture** | `Artisanat` | Explorer l'artisanat |

**Liens** : slugs Odoo (`/shop/category/epicerie-1`, etc.) — résolus au bootstrap via `ir.http._slug()`.

### Qui modifie quoi ?

| Zone | Qui | Comment |
|------|-----|---------|
| **Visuels par défaut** | Dev / module | JPG dans `static/img/ck_univers_{epicerie,soin,artisanat}.jpg` |
| **Image d'une card** | MOA / éditeur site | Website Builder → **Modifier** → clic photo card → sélecteur média |
| **Titre / description card** | MOA / éditeur site | Zones `o_editable` inline |
| **Titre / intro section** | MOA / éditeur site | En-tête section (`o_editable`) |
| **URL catégorie** | Code (bootstrap) | Recalculée si arch invalide ou migration ; **conservée** si arch valide + édition images |
| **Libellé CTA** | Code V1 | Non `o_editable` (span statique) |

### Édition card par card (décision MOA validée QA)

Chaque card est un **sous-snippet** `s_ck_univers_card` avec `data-name` distinct (`Univers Épicerie créole`, etc.).

Pattern Odoo 19 (aligné `s_company_team_basic`) :
- `<img class="o_editable_media">` dans wrapper `o_not_editable` ;
- navigation via `<a class="ck-univers-card__cover">` (désactivé en mode édition : `body.editor_enable`) ;
- plugin `ck_univers_plugin.js` pour l'éditeur Website Builder.

**Règle** : modifier l'image **Épicerie** ne doit **pas** impacter Soin ni Artisanat.

### Ordre sur la home

```text
S3 Nos coups de cœur → S4 Acheter par univers → Coffrets découverte → …
```

### Pourquoi la home n'est pas « live » comme `/shop` ?

Comme la Section 3, le HTML est **injecté** dans `view.arch_db` de `/`. Reconstruction quand :

| Déclencheur | Mécanisme |
|-------------|-----------|
| Upgrade / migration | `migrations/19.0.1.21.x/post-migrate.py` · `post_init_hook` |
| Arch invalide (ancien markup, liens BO périmés) | `bootstrap_home_univers()` réécrit la section |

Si l'arch est **valide** (`_univers_arch_matches_bo`) → **pas de réécriture** : les images modifiées en Website Builder sont **préservées** (validé QA : persistance après upgrade + restart).

### En une phrase

**Trois cards navigation catalogue injectées après les Coups de cœur ; chaque card est éditable individuellement dans le Website Builder ; les liens catégories viennent du BO Odoo.**

---

## 1. Vue d'ensemble

```text
┌─────────────────────────────────────────────────────────────────┐
│  Back-office Odoo                                               │
│  product.public.category (Épicerie · Maison & bien-être · …)      │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  Résolution — home_univers.py                                   │
│  _resolve_univers_cards() → href catégorie + specs card         │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  Rendu — build_home_univers_arch()                              │
│  section s_ck_univers_cards + 3× s_ck_univers_card              │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  Injection — bootstrap_home_univers()                           │
│  après S3 · puis bootstrap_home_discovery_pack() (S5)           │
└─────────────────────────────────────────────────────────────────┘
```

**Doctrine** : contenu métier + bootstrap dans `dorevia_ck_marketone_content` ; styles + snippets + plugin éditeur dans `dorevia_ck_theme`.

---

## 2. Markup card (référence)

```html
<div class="ck-univers-card ck-univers-card--epicerie"
     data-snippet="s_ck_univers_card"
     data-name="Univers Épicerie créole">
  <div class="ck-univers-card__media o_not_editable" contenteditable="false">
    <img src="…/ck_univers_epicerie.jpg"
         class="ck-univers-card__img o_editable_media" alt="…"/>
  </div>
  <a href="/shop/category/epicerie-1" class="ck-univers-card__cover" aria-label="…"/>
  <div class="ck-univers-card__overlay">
    <h3 class="ck-univers-card__title o_editable">…</h3>
    <p class="ck-univers-card__desc o_editable">…</p>
    <span class="ck-univers-card__cta">…</span>
  </div>
</div>
```

| Élément | Rôle |
|---------|------|
| `data-snippet="s_ck_univers_card"` | Sélection éditeur **par card** (pas le bloc section entier) |
| `o_editable_media` | Sélecteur média Odoo sur l'image |
| `ck-univers-card__cover` | Clic navigation browse ; `pointer-events: none` en édition |
| Overlay `pointer-events: none` | Clics traversent vers cover ; titre/desc `pointer-events: auto` pour édition texte |

---

## 3. Validation arch (`univers_arch_is_valid`)

L'arch Section 4 est considérée valide si :

- marqueur `ck-univers-cards` + snippet `s_ck_univers_cards` ;
- titre + intro MOA ;
- **exactement 3** cards (`ck-univers-card--`) ;
- **3** sous-snippets `data-snippet="s_ck_univers_card"` ;
- **3** `o_editable_media` + **3** `ck-univers-card__cover` ;
- **pas** d'ancien wrapper `<a class="ck-univers-card ck-univers-card--` ;
- pas de carousel · pas de « Packs & découvertes » dans la grille ;
- textes + CTA des 3 specs présents ;
- liens catégories BO à jour (`_univers_arch_matches_bo`).

---

## 4. Cycle de vie technique

| Déclencheur | Fichier |
|-------------|---------|
| Install / upgrade | `hooks.post_init_hook` → `bootstrap_home_univers` |
| Migrations `19.0.1.21.0` → `19.0.1.21.7` | `migrations/*/post-migrate.py` |

`bootstrap_home_univers()` :

1. retire sections univers existantes + legacy `s_ck_category_links` ;
2. si arch valide et liens BO OK → **ne réécrit pas** (préserve éditions MOA) ;
3. sinon génère et injecte après `s_ck_featured_products` ;
4. enchaîne `bootstrap_home_discovery_pack()` pour positionner S5.

---

## 5. Historique livraisons (migrations clés)

| Version | Apport |
|---------|--------|
| `19.0.1.21.0` | Section 4 initiale — 3 cards visuelles après S3 |
| `19.0.1.21.3` / `21.4` | Itérations visuels MOA |
| `19.0.1.21.5` | En-tête aligné à gauche |
| `19.0.1.21.6` | Tentative `o_editable` sur wrapper média (NO GO QA éditeur) |
| `19.0.1.21.7` | **Fix éditeur** : sous-snippet card · `o_editable_media` · cover link · plugin JS |
| `19.0.1.30.3` (theme) | Snippet `s_ck_univers_card` · SCSS cover/overlay · `ck_univers_plugin.js` |

---

## 6. Critères de recette Section 4

| # | Contrôle |
|---|----------|
| 1 | Ordre home : S3 → **S4** → Coffrets découverte |
| 2 | 3 cards · en-tête gauche · overlay chaud/sombre · CTA pill blanc |
| 3 | Responsive 1280 / 768 / 390 · pas d'overflow horizontal |
| 4 | Liens catégories BO (épicerie · maison-bien-être · artisanat) |
| 5 | **Édition** : sélection card `Univers …` individuelle · image Épicerie seule modifiable |
| 6 | **Persistance** : image custom conservée après upgrade module + restart |
| 7 | Non-régression S3 |
| 8 | Tests auto tag `dorevia_ck_marketone_home_section4` : 12/12 |

**PV QA** : GO — 2026-06-17 · `content 21.7` · `theme 30.3`.

---

## 7. Notes opérationnelles recette

| Sujet | Détail |
|-------|--------|
| Écriture directe `arch_db` | Sur `dorevia_ck_marketone_01`, visible en HTTP **après restart** du process web — comportement instance, pas le flux éditeur standard |
| Flux MOA attendu | Website Builder → Modifier → sauvegarde éditeur |
| Hard refresh | Recommandé après upgrade (`Cmd+Shift+R` / navigation privée) |

---

## 8. Points ouverts / dette MOA

| Sujet | État |
|-------|------|
| 3 univers figés V1 | ✅ Livré |
| Édition image card par card | ✅ Livré `21.7` · **QA GO** |
| Édition libellé CTA inline | ❌ Hors `o_editable` V1 |
| 4ᵉ card ou packs dans la grille | ❌ Hors périmètre MOA |
| Liens catégories auto-refresh si renommage slug | ⚠️ Re-bootstrap si arch invalidée |
| Visuels définitifs média Odoo (vs JPG module) | Optionnel post-édition MOA |

---

## 9. Références Dev

| Fichier | Rôle |
|---------|------|
| `home_univers.py` | Specs cards · bootstrap · validation arch |
| `home_discovery_pack.py` | Insertion S5 après S4 (`find_univers_section_end_index`) |
| `hooks.py` | Chaîne bootstrap home |
| `ck_snippet_univers_cards.xml` | Snippet section |
| `ck_snippet_univers_card.xml` | Snippet card unitaire |
| `ck_univers_plugin.js` | Éditeur — images dans `.o_not_editable` |
| `website.scss` | Styles `.ck-univers-cards` |
| `static/img/ck_univers_*.jpg` | Visuels par défaut MOA |

**Tests** :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 --http-port=8079 --no-http \
  -u dorevia_ck_theme,dorevia_ck_marketone_content \
  --test-tags dorevia_ck_marketone_home_section4 \
  --stop-after-init
```

**Docs liées** :

- `RECETTE_VISUELLE_SECTION4_UNIVERS_V1.md` — PV recette visuelle QA GO
- `NOTE_ARCHITECTURE_SECTION3_VEDETTES_V1.md` — Section 3 (précédente)

---

*Note d'architecture Section 4 — révision 2026-06-17 · `content` ≥ `19.0.1.21.7` · `theme` ≥ `19.0.1.30.3` · recette QA GO PR #76.*
