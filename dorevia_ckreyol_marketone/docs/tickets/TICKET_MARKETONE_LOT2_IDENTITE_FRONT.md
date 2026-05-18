# TICKET — Lot 2 Identité front `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_LOT2_IDENTITE_FRONT` |
| **Lot** | 2 — Identité front minimale |
| **Statut** | GO validé (2026-05-18) |
| **Base** | `ckr-marketone-01` |
| **Prérequis** | GO Lot 1 validé (2026-05-18) |
| **Version cible module** | `19.0.2.0.0` |

---

## Objectif

Poser une **identité C-Kreyol sobre et mobile-first** sur le site, sans refonte lourde ni modification du moteur `website_sale`.

```text
Critère GO Lot 2 :
La home devient identifiable C-Kreyol de manière sobre et mobile-first,
sans casser le thème Odoo ni modifier le comportement standard de website_sale.
```

---

## Contexte

| Élément | État |
|---------|------|
| Lot 1 | Module installable, assets placeholder, tests `dorevia_marketone_smoke` OK |
| Base | `ckr-marketone-01` — socle `website` + `website_sale` + `portal` |
| Front actuel | Thème Odoo 19 CE natif, home par défaut |
| Legacy | `dorevia_ckreyol_marketplace` — **référence palette uniquement**, pas de portage |

La charte C-Kreyol (direction « épicerie fine tropicale ») existe conceptuellement dans le legacy (`tokens/_colors.scss`, `_typography.scss`). Le Lot 2 **réécrit** des tokens Marketone légers, sans importer les monolithes SCSS legacy.

---

## Doctrine (rappel)

```text
Odoo vend. Marketone présente, clarifie, oriente.
```

| Règle | Lot 2 |
|-------|-------|
| Standard Odoo d’abord | Pas de surcharge `WebsiteSale` |
| Scope CSS | `.marketone-root` + classes `marketone-*` |
| Pas de JS | Sauf nécessité démontrée et documentée (ADR) |
| Pas de portes | Pas de liens `/shop?marketone_mode=…` |
| Contrats | C4, C6 dans `cadrage/CONTRACTS.md` |

---

## Périmètre inclus

### 1. Tokens SCSS

Créer des partials **simples** (pas de map Odoo `$o-color-palette` global) :

| Fichier | Contenu |
|---------|---------|
| `static/src/scss/_tokens.scss` | Point d’agrégation `@forward` |
| `static/src/scss/_tokens_colors.scss` | Palette C-Kreyol (voir § palette) |
| `static/src/scss/_tokens_typography.scss` | Stacks serif + sans, échelle mobile-first |
| `static/src/scss/_tokens_spacing.scss` | 4–6 espacements nommés |

**Préfixe variables** : `$marketone-*` (pas `$ckr-*`).

**Palette de référence** (reprise conceptuelle charte Phase 1 — à figer au commit, pas copie fichier legacy) :

| Token | Valeur indicative | Usage |
|-------|-------------------|--------|
| `$marketone-primary` | `#A0522D` | CTA, accents marque |
| `$marketone-secondary` | `#87A878` | Accents secondaires |
| `$marketone-accent` | `#D4A373` | Micro-accents |
| `$marketone-bg` | `#F5F1E8` | Fond page |
| `$marketone-bg-soft` | `#FCF9F7` | Fond alternatif (optionnel home) |
| `$marketone-text` | `#2C2C2C` | Texte principal |
| `$marketone-text-muted` | `#707070` | Texte secondaire |
| `$marketone-border` | `#D9D0BA` | Bordures fines |

Typo indicative : titres **Playfair Display**, corps **Inter** (chargement webfonts via QWeb layout — pas de JS).

### 2. Fichiers SCSS structure

| Fichier | Rôle |
|---------|------|
| `static/src/scss/marketone.scss` | Entrée bundle : `@import` tokens → layout → home |
| `static/src/scss/_layout.scss` | Règles `.marketone-root` (typo, fond, liens) — **scope strict** |
| `static/src/scss/_home.scss` | Styles blocs home `marketone-home-*` uniquement |

**Règles SCSS**

- Cibler `.marketone-root` (et descendants), jamais `body` ni `.o_main` sans scope.
- Pas de `!important` (contrat C4.3).
- Pas de règles sur `.o_wsale_*`, `#o_wsale_products_grid`, panier, checkout.
- Mobile-first : `clamp()` ou breakpoints Bootstrap existants ; pas de scroll horizontal.

### 3. QWeb minimal (home)

| Fichier | Rôle |
|---------|------|
| `views/layout/website_layout.xml` | Héritage `website.layout` : charger polices (link Google Fonts ou équivalent), **optionnel** classe sur `#wrap` si homepage |
| `views/pages/home.xml` | Héritage page d’accueil : ajouter `marketone-root` sur `#wrap` + **une** section éditoriale simple |

**Contenu minimum section home** (pas de hero rotatif, pas d’Explorer 5 portes) :

```text
- Sur-titre court (ex. « Épicerie fine créole »)
- Titre H1 marque (ex. « C-Kreyol »)
- Accroche 1–2 lignes (retail, mobile-first)
- CTA primaire → /shop (libellé ex. « Découvrir la boutique »)
- Bandeau réassurance courte (3 puces max, texte statique)
```

**XPath** : privilégier `//div[@id='wrap']` avec `position="attributes"` pour `class`, ou insert **inside** `#wrap` en tête — pas de `replace` massif.

**Snippets** : optionnel Lot 2 — un seul snippet `s_marketone_home_intro` si plus maintenable qu’un bloc inline ; sinon bloc unique dans `home.xml`.

### 4. Manifeste

- Version : `19.0.2.0.0`
- `data` : déclarer `views/layout/website_layout.xml`, `views/pages/home.xml` (et `views/snippets/snippets.xml` si snippet)
- `assets` : ordre explicite dans `web.assets_frontend` :

```text
_tokens_colors.scss
_tokens_typography.scss
_tokens_spacing.scss
_tokens.scss
_layout.scss
_home.scss
marketone.scss
```

### 5. Tests

| Tag | Fichier | Tests |
|-----|---------|-------|
| `dorevia_marketone_smoke` | `test_marketone_smoke.py` | **Doit rester vert** (non-régression Lot 1) |
| `dorevia_marketone_lot2` | `test_marketone_lot2_home.py` | Nouveau |

**Tests Lot 2 proposés** (`HttpCase`, `post_install`) :

1. `test_home_http_200` — `/` retourne 200
2. `test_home_contains_marketone_root` — HTML contient `marketone-root` ou `marketone-home`
3. `test_home_contains_brand_marker` — texte « C-Kreyol » (ou libellé MOA figé)
4. `test_home_cta_shop_link` — présence lien vers `/shop`
5. `test_shop_unchanged_http_200` — `/shop` toujours 200 (pas de régression)
6. `test_shop_no_marketone_shop_scope` — pas de classe `marketone-shop` sur `/shop` (Lot 3)

Importer le fichier dans `tests/__init__.py`.

### 6. Documentation

- Mettre à jour `recette/ENV_REFERENCE.md` (commandes test Lot 2)
- ADR-015 dans `cadrage/DECISIONS.md` après livraison
- `pilotage/ROADMAP.md` : statut Lot 2

---

## Hors périmètre

| Exclusion | Report |
|-----------|--------|
| Boutique `/shop` (cartes, sidebar, chips) | Lot 3 |
| Fiche produit | Lot 4 |
| Panier / checkout | Lot 5 |
| Portes catalogue, filtres, alias URL | Lot 6 |
| Header / footer custom complets | Lot 2+ ou ticket dédié MOA |
| Hero rotatif, carrousel, vidéo | Jamais au Lot 2 |
| Grille Explorer 5 portes | Lot 6 |
| `website_sale` héritages | Lot 3+ |
| Contrôleur, modèle Python | Non |
| JS fonctionnel | Non |
| Thème tiers, wishlist, comparaison | Non |
| Données produit / CMS volumineuses | Non |
| Portage `ckr_*.scss`, `ckr_*.xml` | Non |

---

## Livrables attendus (checklist exécution)

```text
[ ] _tokens_colors.scss, _tokens_typography.scss, _tokens_spacing.scss, _tokens.scss
[ ] _layout.scss, _home.scss, marketone.scss (entrée)
[ ] views/layout/website_layout.xml (polices, scope minimal)
[ ] views/pages/home.xml (marketone-root + section intro)
[ ] __manifest__.py → 19.0.2.0.0 + data + assets ordonnés
[ ] tests/test_marketone_lot2_home.py + import tests/__init__.py
[ ] -u sans erreur sur ckr-marketone-01
[ ] dorevia_marketone_smoke : 6/6 OK
[ ] dorevia_marketone_lot2 : tous OK
[ ] Revue visuelle mobile + desktop (capture ou PV court)
```

---

## Critères GO / NO GO

### GO

- [ ] Home identifiable C-Kreyol (palette chaude, typo éditoriale, message marque)
- [ ] Mobile-first : lisible sur viewport ~375px sans scroll horizontal
- [ ] `/shop` inchangé fonctionnellement (200, pas de styles `marketone-shop`)
- [ ] Tests `dorevia_marketone_smoke` + `dorevia_marketone_lot2` verts
- [ ] Aucune dépendance ajoutée au manifeste
- [ ] Aucun module interdit installé (marketplace, theme_classic_store, wishlist)
- [ ] Pas de `!important` ni `<style>` inline massif en QWeb

### GO avec réserves

- [ ] Identité home OK mais polices web à optimiser (self-host Lot 2.1)
- [ ] Textes placeholder en attente copies MOA

### NO GO

- [ ] Régression 500 sur `/` ou `/shop`
- [ ] Styles qui fuient hors `.marketone-root` vers BO ou checkout
- [ ] Surcharge `website_sale` ou logique catalogue introduite
- [ ] JS ajouté sans ADR
- [ ] Liens vers portes catalogue non implémentées

---

## Risques

| Risque | Mitigation |
|--------|------------|
| Fuite CSS globale (`$primary`, `body`) | Tokens **non** mappés Bootstrap global ; scope `.marketone-root` |
| XPath homepage fragile upgrade Odoo | Xpath `#wrap` ; test HTTP Lot 2 |
| Polices externes (RGPD / perf) | `preconnect` + subset ; documenter dans ADR |
| Home Odoo par défaut vs page custom | Tester sur base vierge `ckr-marketone-01` |
| Tentation d’étendre au header/footer | Hors ticket ; ticket séparé si MOA |

---

## Règles de non-régression

1. Tous les tests Lot 1 (`dorevia_marketone_smoke`) restent verts.
2. `/shop` : HTTP 200, aucun xpath Marketone sur templates `website_sale`.
3. Install/update module sans traceback.
4. Modules interdits toujours `uninstalled`.

---

## Commandes de validation

```bash
# Mise à jour module
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone --stop-after-init

# Tests Lot 1 (non-régression)
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone \
  --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_smoke --http-port=8071

# Tests Lot 2
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone \
  --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_lot2 --http-port=8071

# Smoke HTTP manuel
curl -sS -H 'X-Odoo-Database: ckr-marketone-01' http://localhost:18079/ | head
curl -sS -o /dev/null -w '%{http_code}\n' \
  -H 'X-Odoo-Database: ckr-marketone-01' http://localhost:18079/shop
```

**Recette visuelle** (humaine) : navigateur incognito, base `ckr-marketone-01`, `/` puis `/shop` — la home doit « sentir » C-Kreyol ; la boutique reste Odoo standard.

---

## Architecture cible (delta Lot 2)

```text
dorevia_ckreyol_marketone/
├── __manifest__.py                    # 19.0.2.0.0
├── static/src/scss/
│   ├── _tokens_colors.scss
│   ├── _tokens_typography.scss
│   ├── _tokens_spacing.scss
│   ├── _tokens.scss
│   ├── _layout.scss
│   ├── _home.scss
│   └── marketone.scss
├── views/
│   ├── layout/website_layout.xml
│   └── pages/home.xml
└── tests/
    └── test_marketone_lot2_home.py
```

Toujours **absents** : `controllers/`, `models/`, `static/src/js/`.

---

## Décision explicite — pas de copie legacy

```text
Le Lot 2 s’inspire de la charte C-Kreyol (couleurs, typo, ton retail)
sans importer les fichiers SCSS/QWeb du module dorevia_ckreyol_marketplace.
Aucun préfixe ckr_* dans le code livré.
```

---

## Organisation

| Rôle | Action |
|------|--------|
| MOA | Valider textes home (H1, accroche, CTA, réassurance) avant ou pendant exécution |
| Dev | Exécuter ce ticket sur `ckr-marketone-01` |
| Qualité | Relecture scope CSS + tests + PV visuel court |

---

### Résultats automatises (2026-05-18)

| Commande | Résultat |
|----------|----------|
| `-u dorevia_ckreyol_marketone` | OK (v `19.0.2.0.0`) |
| `--test-tags=dorevia_marketone_smoke` | **6/6** OK |
| `--test-tags=dorevia_marketone_lot2` | **7/7** OK |
| `curl /` | `marketone-root`, C-Kreyol, CTA présents |
| `curl /shop` | 200, sans `marketone-shop` |

---

## Checklist validation humaine (post-livraison)

```text
[ ] Home identifiable C-Kreyol (sobre, mobile-first)
[ ] /shop reste standard Odoo (visuel + HTTP 200)
[ ] Tests smoke + lot2 OK
[ ] Aucune dépendance / module interdit
[ ] Pas de JS, pas de portes catalogue

Décision : [ ] GO  [ ] GO avec réserves  [ ] NO GO

Réserves :
_________________________________________________

Validé par : _______________  Date : __________
```

---

## Prochaine étape après GO Lot 2

Préparer ou exécuter **Lot 3** — boutique `/shop` lisible (SCSS scoped `marketone-shop`, xpath minimal sur `#wrap`).
