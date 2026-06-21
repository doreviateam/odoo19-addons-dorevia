# Note d'intervention QA — Lot Nav-1 · Navigation CK V2

| Champ | Valeur |
| --- | --- |
| **Projet** | `dorevia_ck_marketone` |
| **Lot** | Nav-1 — header / navigation uniquement |
| **Branche Dev** | `feat/ck-nav1-navigation-v2` |
| **Ticket Dev** | [`TICKET_DEV_LOT_NAV1_NAVIGATION_CK_V2.md`](../TICKET_DEV_LOT_NAV1_NAVIGATION_CK_V2.md) |
| **Recette Dev** | [`RECETTE_QA_LOT_NAV1_NAVIGATION_CK_V2.md`](./RECETTE_QA_LOT_NAV1_NAVIGATION_CK_V2.md) |
| **Brief MOA** | [`note_06.md`](../../cadrage/note_06.md) |
| **Instance** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **Modules cibles** | `dorevia_ck_marketone_content` **19.0.1.26.1** · `dorevia_ck_theme` **19.0.1.37.1** |
| **Statut Dev** | **✅ Correctifs B1/B2 livrés · tests auto 15/15 OK · 2026-06-21** |
| **Statut QA** | **✅ GO merge — re-recette B1/B2 OK · 2026-06-21** (PV initial NO GO → corrigé) |

---

## Guide simple (lire en premier)

### C'est quoi, concrètement ?

Le **header** du site CK passe à la **Navigation V2 MOA** :

- menu commerce renommé et réordonné ;
- **Professionnels** et **Contactez-nous** relocalisés sous le mega **Découvrir** ;
- **CTA fort Contact** retiré à droite du header ;
- sur mobile, regroupement **Nos univers** (accordéon) pour garder un drawer lisible à 390 px.

Ce n'est **pas** :

- une refonte Home S4 ;
- une modification fiche produit / checkout ;
- l'activation Blog ou Forum ;
- la création de pages éditoriales manquantes (Histoires de produits, Communauté, Contribuer).

### Menu attendu sur l'instance seed (règle visibilité incluse)

**Desktop 1280 px** — entrées **visibles** aujourd'hui :

```text
Tous nos produits · Épicerie · Soin & Bien-être · Découvrir
```

> **Boissons** et **Artisanat** sont **absents volontairement** : catégories absentes ou sans produit publié sur l'instance seed. Ce n'est **pas** un bug Nav-1 — cf. ticket §7 bis.

**Mobile 390 px** :

```text
Tous nos produits · Nos univers · Découvrir
```

Sous **Nos univers** : Épicerie · Soin & Bien-être.

### Ce que QA doit trancher

| Zone | Question QA |
| --- | --- |
| Desktop | Menu conforme MOA · mega Découvrir · pas de legacy · tenue visuelle **Soin & Bien-être** |
| Mobile | Drawer court · accordéon **Nos univers** · zéro overflow horizontal |
| Contraste | Liens nav + mega lisibles (hover/focus terracotta texte `#bf360c`) |
| Non-régression | Home S4 inchangée · routes Pro / Contact / shop OK |

---

## 1. Mise en route (obligatoire avant recette écran)

### 1.1 Accès instance

| Paramètre | Valeur |
| --- | --- |
| URL | http://localhost:18079 |
| Base | `dorevia_ck_marketone_01` |
| Login recette | `admin` / `admin` (local uniquement) |
| Conteneur | `sandbox-odoo19-odoo-1` |

**Multi-base** : ajouter `?db=dorevia_ck_marketone_01` à l'URL ou sélectionner la base au login.  
En requête HTTP directe : header `X-Odoo-Database: dorevia_ck_marketone_01`.

**Cache-bust recommandé** : `?qa_ts=nav1` sur chaque page contrôlée.

### 1.2 Mise à jour modules (si branche non déployée)

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 \
  -u dorevia_ck_marketone_content,dorevia_ck_theme \
  --stop-after-init
```

Puis redémarrer le worker Odoo si les pages renvoient 500 après upgrade :

```bash
docker restart sandbox-odoo19-odoo-1
```

### 1.3 Rejeu tests auto (sanity check Dev)

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 --test-enable --stop-after-init --http-port=8078 \
  --test-tags dorevia_ck_marketone_nav_sync,dorevia_ck_theme_phase10
```

**Attendu** : `0 failed, 0 error(s)` — **15 tests** (13 initiaux + 2 cas B1/B2).

| Contrôle pré-recette | Statut Dev | Statut QA |
| --- | --- | --- |
| Branche / modules à jour | ✅ | ✅ `-u dorevia_ck_marketone_content,dorevia_ck_theme` rejoué, 0 erreur |
| Tests auto Nav-1 verts | ✅ 13/13 | ✅ Rejoué — `0 failed, 0 error(s) of 13 tests` |
| Instance accessible (HTTP 200 sur `/` ou `/shop`) | ⚠️ vérifier post-restart | ✅ 200 sur `/` et `/shop` post-restart |

⚠️ **Constat méthodologique** : les tests `HttpCase` (`test_ck_nav_sync`) appellent `bootstrap_ck_navigation()` à chaque test sans isolation transactionnelle complète vis-à-vis de la base partagée — un rejeu de la suite laisse transitoirement le menu réel dans un état non représentatif (entrées legacy `Boutique` / `Professionnels` top-level visibles). **Toujours rejouer `bootstrap_ck_navigation(env)` manuellement et vérifier l'état réel après un passage de tests**, avant toute recette écran. Non bloquant pour ce lot (la recette ci-dessous a été faite sur l'état rebootstrappé propre), mais à signaler côté Dev pour fiabiliser la recette future.

---

## 2. Mapping de référence (ne pas réinventer)

Utiliser ce tableau pour valider les URLs — détail complet dans la [recette Dev](./RECETTE_QA_LOT_NAV1_NAVIGATION_CK_V2.md#1-mapping-catalogue-bo-instance-seed--post-sync).

| Entrée menu | Catégorie BO | URL attendue | Visible seed |
| --- | --- | --- | --- |
| Tous nos produits | Catalogue | `/shop` | Oui |
| Épicerie | Épicerie (id 1) | `/shop/category/epicerie-1` | Oui |
| Boissons | — | — | **Non** |
| Soin & Bien-être | **Maison & bien-être** (id 2) | `/shop/category/maison-bien-etre-2` | Oui |
| Artisanat | — | — | **Non** |

**Mega Découvrir** (ordre) :

1. Producteurs & territoires → `/producteur/atelier-hauts-goyaviers`
2. Recettes & usages → `/recettes`
3. Professionnels → `/professionnels`
4. Contactez-nous → `/contactus`

**Absents du mega** : Blog · Communauté · Contribuer · liens commerce dupliqués.

---

## 3. Recette desktop 1280 px

Viewport : **1280 × 800** (Chrome ou Firefox). Pages : `/` · `/shop`.

| # | Contrôle | Attendu | ☐ | Note QA |
| ---: | --- | --- | --- | --- |
| D1 | Menu top-level | **Tous nos produits · Épicerie · Soin & Bien-être · Découvrir** visibles | ☒ **KO partiel** | Les 4 entrées attendues sont bien là, **mais une 5ᵉ entrée « Nos univers » (dropdown) reste visible en desktop** — devrait être masquée. Voir bug B1 ci-dessous. |
| D2 | Absences conformes | **Pas** Boissons · **pas** Artisanat · **pas** Boutique · **pas** Professionnels top-level | ☒ OK | Boutique et Professionnels bien absents du top-level sur l'état rebootstrappé propre. |
| D3 | CTA Contact header | **Aucun** bouton terracotta « Contactez-nous » à droite (pas de `.btn_cta`) | ☒ OK | `document.querySelectorAll('header .btn_cta').length === 0` |
| D4 | Tous nos produits | Clic → `/shop` · page 200 · produits listés | ☒ OK | 200 · 6 produits dans la grille |
| D5 | Épicerie | Clic → `/shop/category/epicerie-1` · ≥ 1 produit | ☒ OK | 200 · 4 produits |
| D6 | Soin & Bien-être | Clic → `/shop/category/maison-bien-etre-2` · libellé menu = **Soin & Bien-être** (pas « Soin » seul) | ☒ OK | 200 · 1 produit · libellé conforme |
| D7 | Mega Découvrir ouvert | Pro puis Contact · pas Blog / Communauté / Contribuer | ☒ OK | Ordre exact : Producteurs & territoires → Recettes & usages → Professionnels → Contactez-nous |
| D8 | Mega sans commerce | Aucun lien Épicerie / Boissons / Soin / Artisanat / `/shop` dans le mega | ☒ OK | 4 liens du mega tous éditoriaux/contact, aucun lien commerce |
| D9 | Chrome header | Logo C-Kreyol · recherche · compte · panier OK | ☒ OK | Les 4 éléments présents et détectés |
| D10 | Contraste mega | Au survol / focus, liens mega lisibles (terracotta texte, pas orange pâle illisible) | ☒ OK | `color: rgb(191, 54, 12)` = `#bf360c` exact au hover |

**Preuve** : [`nav1_desktop_1280_header.png`](./captures/recette_nav1_v2/nav1_desktop_1280_header.png) · [`nav1_desktop_1280_results.json`](./captures/recette_nav1_v2/nav1_desktop_1280_results.json)

### §10 bis — vigilance desktop « Soin & Bien-être »

| Point | Attendu | ☐ | Note QA |
| --- | --- | --- | --- |
| V1 | Aucun libellé menu sur 2 lignes | ☒ OK | Confirmé visuellement sur capture — une seule ligne |
| V2 | Pas de troncature illisible | ☒ OK | Texte complet, aucune ellipse |
| V3 | Pas de chevauchement logo / chrome droit | ☒ OK | Aucun chevauchement détecté (bounding boxes disjointes) |

---

### 🔴 Bug B1 — « Nos univers » non masqué en desktop (D1, C2, C9)

**Constat** : l'entrée dropdown « Nos univers » (destinée au mobile uniquement) reste visible et fonctionnelle en desktop 1280 px, en plus des entrées plates Épicerie / Soin & Bien-être. Le menu desktop affiche donc **5 entrées commerce** au lieu des **4** spécifiées (ticket §4, NOTE_QA §"Menu attendu").

**Cause racine identifiée** : `dorevia_ck_marketone_content/views/website_nav_ck_v1.xml` patch le template core `website.submenu` via :

```xml
<xpath expr="//li[@role='presentation']" position="attributes">
    <attribute name="t-attf-class" add="#{submenu.ck_nav_css_class or ''}" separator=" "/>
</xpath>
```

Le template core `website.submenu` (`addons/website/views/website_templates.xml`) définit **deux `<li role="presentation">` mutuellement exclusifs** (`t-if`/`t-elif`) : un pour les entrées **feuilles** (sans enfants), un pour les entrées **dropdown/accordéon** (avec enfants, ex. « Nos univers »). Une xpath `position="attributes"` ne patche que le **premier** nœud trouvé — donc seul le `<li t-if>` (feuille) reçoit `ck_nav_css_class`. Les entrées de type dropdown comme « Nos univers » passent par le `<li t-elif="show_dropdown">` et **ne reçoivent jamais** la classe `ck-nav-mobile-univers`, donc la règle SCSS `#top_menu.top_menu > .nav-item.ck-nav-mobile-univers { display: none !important; }` (`website_header.scss:112`) ne s'applique jamais.

**Vérifié en base** : `env['website.menu'].browse(37).ck_nav_css_class` retourne bien `'ck-nav-mobile-univers'` (donnée correcte) — mais `<li class="nav-item   dropdown">` rendu côté HTML n'a jamais cette classe.

**Piste de correctif (Dev)** : remplacer l'unique xpath par deux xpaths distincts ciblant chacune des deux branches (`//li[@t-if][@role='presentation']` et `//li[@t-elif][@role='presentation']`), ou ajouter `t-attf-class` directement dans une vue dédiée plus bas dans l'arbre (ex. sur l'élément `<a>` plutôt que sur le `<li>` ambigu).

---

### 🔴 Bug B2 — Doublon Épicerie / Soin & Bien-être en mobile (M1, C10)

**Constat** : dans le drawer mobile, Épicerie et Soin & Bien-être apparaissent **deux fois** : une fois sous l'accordéon « Nos univers » (attendu), une fois en entrées plates juste en dessous (non attendu — explicitement interdit par M1 : *« pas les univers en doublon plat »*).

**Cause racine identifiée** : `dorevia_ck_theme/static/src/scss/website_header.scss:309` :

```scss
.ck-theme .offcanvas,
.ck-theme #top_menu_collapse_mobile.offcanvas {
    ...
    #top_menu_collapse_mobile .ck-nav-desktop-universe {
        display: none !important;
    }
}
```

`#top_menu_collapse_mobile` **est** l'élément `.offcanvas` lui-même (`<div id="top_menu_collapse_mobile" class="offcanvas ...">`), pas un ancêtre distinct. La règle imbriquée re-préfixe `#top_menu_collapse_mobile` **à l'intérieur** d'un bloc déjà scopé sur ce même élément — la sélecteur compilé exige que l'offcanvas soit son propre ancêtre (impossible). Résultat : la règle ne matche jamais, malgré la classe `ck-nav-desktop-universe` correctement présente sur les `<li>` concernés (vérifié : `display: list-item`, `visible: true` en mobile).

**Piste de correctif (Dev)** : supprimer le préfixe redondant — la règle interne doit être simplement `.ck-nav-desktop-universe { display: none !important; }` (le scope `#top_menu_collapse_mobile` est déjà fourni par le sélecteur parent).

**Preuve** : [`nav1_mobile_390_nos_univers_open.png`](./captures/recette_nav1_v2/nav1_mobile_390_nos_univers_open.png) — capture montrant Épicerie/Soin & Bien-être en double sous l'accordéon ouvert.

### ✅ Correctifs Dev livrés (2026-06-21)

| Bug | Correctif | Fichier | Version |
| --- | --- | --- | --- |
| **B1** | Deux xpath distincts (`t-if` + `t-elif`) pour appliquer `ck_nav_css_class` sur les dropdowns | `dorevia_ck_marketone_content/views/website_nav_ck_v1.xml` | **19.0.1.26.1** |
| **B2** | Suppression du préfixe `#top_menu_collapse_mobile` redondant dans la règle `.ck-nav-desktop-universe` | `dorevia_ck_theme/static/src/scss/website_header.scss` | **19.0.1.37.1** |

Tests auto renforcés : `test_desktop_top_menu_mobile_univers_has_hide_class` · `test_mobile_offcanvas_no_duplicate_universe_entries` — **15/15 OK**.

> **Re-recette QA demandée** — cf. **§8 bis** (D1 · M1 · M3 uniquement). Le reste du PV §8 initial reste acquis sans reprise.

> Si une réserve mineure est constatée (espacement serré avec 6 entrées futures), la **documenter** sans bloquer le merge MOA — cf. ticket §10 bis.

---

## 4. Recette mobile 390 px

Viewport : **390 × 844**. Ouvrir le **burger / offcanvas**.

| # | Contrôle | Attendu | ☐ | Note QA |
| ---: | --- | --- | --- | --- |
| M1 | Entrées drawer | **Tous nos produits · Nos univers · Découvrir** (pas les univers en doublon plat) | ☒ **KO** | Épicerie et Soin & Bien-être apparaissent **en double** : une fois sous l'accordéon « Nos univers », une fois en entrées plates juste en dessous. Voir bug B2 ci-dessus. |
| M2 | Nos univers — déplier | Clic sur **Nos univers** **déplie** le sous-menu · **ne change pas de page** | ☒ OK | URL inchangée après clic · `accordion-collapse` passe en classe `show` |
| M3 | Nos univers — enfants | Épicerie · Soin & Bien-être naviguent vers les bonnes catégories | ☒ OK | hrefs corrects (`/shop/category/epicerie-1`, `/shop/category/maison-bien-etre-2`) — mais doublon visuel cf. M1 |
| M4 | Découvrir | Mega / sous-liens accessibles · Pro + Contact OK | ☒ OK | 4 liens identiques au desktop, ordre conforme |
| M5 | Overflow | **Zéro** scroll horizontal sur le drawer et la page | ☒ OK | `scrollWidth === clientWidth === 390` drawer fermé et ouvert |
| M6 | Chrome mobile | Burger · panier · recherche utilisables | ☒ OK | Les 3 éléments présents et fonctionnels |

**Preuves** : [`nav1_mobile_390_closed.png`](./captures/recette_nav1_v2/nav1_mobile_390_closed.png) · [`nav1_mobile_390_drawer.png`](./captures/recette_nav1_v2/nav1_mobile_390_drawer.png) · [`nav1_mobile_390_nos_univers_open.png`](./captures/recette_nav1_v2/nav1_mobile_390_nos_univers_open.png) · [`nav1_mobile_390_results.json`](./captures/recette_nav1_v2/nav1_mobile_390_results.json)

---

## 5. Non-régression (spot checks)

| # | Parcours | Attendu | ☐ | Note QA |
| ---: | --- | --- | --- | --- |
| N1 | Home S4 | Section **Acheter par univers** inchangée (3 cards · libellés S4 d'origine) | ☒ OK | 3 cards : Épicerie créole · Soin & bien-être · Artisanat & culture — identique baseline |
| N2 | `/professionnels` | Page `ck-pro-page` · 200 | ☒ OK | 200 · marker présent |
| N3 | `/contactus` | Page contact · 200 (footer + mega) | ☒ OK | 200 · marker présent |
| N4 | `/recettes` | Page recettes · 200 | ☒ OK | 200 · marker présent |
| N5 | Ajout panier shop | Ajouter un produit depuis `/shop` · compteur panier OK | ☒ OK | Compteur `0` → `1`, badge `d-none` retiré (vérifié avec le bon sélecteur `.o_wsale_product_btn_primary`) |
| N6 | Console navigateur | Pas d'erreur JS bloquante au chargement header | ☒ OK avec observation | Aucune erreur JS liée au header/Nav-1. Une requête externe `fonts.gstatic.com` (famille **Inter / Inter Tight**) est émise au chargement de la home — absente du code `dorevia_ck_theme`/`dorevia_ck_marketone_content` (grep négatif), donc **non liée à Nav-1**. Contredit néanmoins l'engagement « polices auto-hébergées, pas de CDN Google » (cf. [`TICKET_DEV_CONTRASTE_WCAG_AA_ORANGE_TEXTE_CK_V1.md`](../TICKET_DEV_CONTRASTE_WCAG_AA_ORANGE_TEXTE_CK_V1.md) / tests `test_ck_fonts_self_hosted_no_google_cdn`). À signaler en dehors de ce lot — origine probablement un autre module installé sur le sandbox. |

**Preuve** : [`nav1_home_s4_spotcheck.png`](./captures/recette_nav1_v2/nav1_home_s4_spotcheck.png) · [`nav1_nonregression_results.json`](./captures/recette_nav1_v2/nav1_nonregression_results.json)

**Hors périmètre — ne pas ouvrir de ticket Nav-1 si constat isolé sur** : checkout · fiche produit · Blog · Forum.

---

## 6. Pièges connus / faux positifs

| Situation | Interprétation |
| --- | --- |
| Boissons / Artisanat absents du menu | **Normal** sur seed — règle visibilité §7 bis |
| Libellé menu « Soin & Bien-être » vs catégorie BO « Maison & bien-être » | **Normal MOA** — mapping documenté |
| Home S4 affiche « Épicerie créole » / « Soin & bien-être » | **Normal** — S4 non modifiée dans Nav-1 |
| Blog absent du mega | **Normal** — `website_blog` non installé |
| HTTP 500 sur instance après upgrade | Vérifier restart conteneur · base `dorevia_ck_marketone_01` sélectionnée |

---

## 7. Preuves attendues

Déposer les captures dans :

```text
docs/design/maquette_01.2/captures/recette_nav1_v2/
```

| Fichier suggéré | Contenu |
| --- | --- |
| `nav1_desktop_1280_header.png` | Menu + mega Découvrir ouvert |
| `nav1_mobile_390_drawer.png` | Offcanvas fermé / ouvert |
| `nav1_mobile_390_nos_univers_open.png` | Accordéon Nos univers déplié |
| `nav1_home_s4_spotcheck.png` | Spot check S4 inchangée |
| `nav1_desktop_1280_header_postfix.png` | Re-recette B1 — desktop 4 entrées |
| `nav1_mobile_390_nos_univers_open_postfix.png` | Re-recette B2 — accordéon sans doublon |

---

## 8. PV de recette (à remplir par QA)

| Champ | Valeur |
| --- | --- |
| **Recetteur** | Assistant IA (Claude), en session avec doreviateam |
| **Date** | 2026-06-21 |
| **Commit / branche** | `feat/ck-nav1-navigation-v2` |
| **Versions modules constatées** | `dorevia_ck_marketone_content` **19.0.1.26.0** · `dorevia_ck_theme` **19.0.1.37.0** |
| **Verdict global** | ☒ **NO GO** (2 bugs ciblés, correctifs identifiés et bien scopés — pas de refonte) |

### Synthèse

| Bloc | Verdict | Commentaire |
| --- | --- | --- |
| Desktop 1280 (§3) | ☒ **KO** | D1 seul échoue : « Nos univers » non masqué → 5 entrées au lieu de 4 (bug B1). D2–D10 tous OK. |
| Mobile 390 (§4) | ☒ **KO** | M1 seul échoue : Épicerie/Soin & Bien-être dupliqués (bug B2). M2–M6 tous OK. |
| §10 bis vigilance | ☒ OK | V1, V2, V3 tous conformes — pas de réserve à documenter |
| Non-régression (§5) | ☒ OK avec observation | N1–N5 OK. N6 : requête Google Fonts hors-périmètre Nav-1 (à signaler séparément). |
| Tests auto rejeu (§1.3) | ☒ OK | 13/13 — mais voir observation méthodologique §1.3 (état post-tests non représentatif sans rebootstrap manuel) |

**Bloquants** (si NO GO) :

1. **Bug B1** — « Nos univers » reste visible en desktop (devrait être masqué). Cause : xpath `website_nav_ck_v1.xml` ne patche que la branche `t-if` (feuille) du template core `website.submenu`, jamais la branche `t-elif` (dropdown) utilisée par « Nos univers ». Détail et piste de correctif : §3 ci-dessus.
2. **Bug B2** — Épicerie / Soin & Bien-être dupliqués dans le drawer mobile (entrées plates + entrées accordéon simultanément visibles). Cause : règle SCSS `website_header.scss:309` imbriquée avec un préfixe `#top_menu_collapse_mobile` redondant qui rend le sélecteur compilé impossible à matcher. Détail et piste de correctif : §3 ci-dessus.

Les deux correctifs sont **ciblés et de faible risque** (pas de refonte de `nav_sync.py` ni de la donnée — uniquement template XML pour B1, uniquement SCSS pour B2). Tout le reste du lot (mapping catégories, règle de visibilité §7 bis, mega Découvrir, retrait CTA Contact, contraste WCAG, routes, panier) est **conforme et vérifié**.

**Recommandation MOA** :

- ☐ GO merge PR Nav-1
- ☒ **Corrections Dev requises avant merge** — B1 et B2 uniquement, reste du lot acquis
- ☐ Enchaînement Lot Nav-2 (pages éditoriales Découvrir)

---

## 8 bis. Re-recette post-correctifs B1 / B2 (à remplir par QA)

> **Contexte** : le PV §8 initial est **NO GO** sur B1 et B2 uniquement. Les correctifs Dev sont livrés (versions **19.0.1.26.1** / **19.0.1.37.1**).  
> **Ne pas refaire** l'intégralité des grilles §3–§5 — reprendre **uniquement** les contrôles ci-dessous + sanity §1.3.

### Prérequis re-recette

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 \
  -u dorevia_ck_marketone_content,dorevia_ck_theme \
  --stop-after-init

docker restart sandbox-odoo19-odoo-1

docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 --test-enable --stop-after-init --http-port=8078 \
  --test-tags dorevia_ck_marketone_nav_sync,dorevia_ck_theme_phase10
```

**Attendu** : `0 failed, 0 error(s) of 15 tests`.

| Contrôle | Statut Dev | Statut QA |
| --- | --- | --- |
| Upgrade modules **26.1** / **37.1** | ✅ | ✅ `-u` rejoué, 0 erreur bloquante |
| Tests auto **15/15** | ✅ | ✅ Rejoué — `0 failed, 0 error(s) of 15 tests` |
| Instance HTTP 200 (`/` · `/shop`) | ✅ post-restart | ✅ 200 sur les deux |

⚠️ Comme pour le PV initial : `bootstrap_ck_navigation(env)` rejoué manuellement après le passage des tests (résidu transitoire constaté §1.3), avant la recette écran ci-dessous.

### Grille ciblée — desktop 1280 px (Bug B1)

| # | Contrôle | Attendu | ☐ | Note QA |
| ---: | --- | --- | --- | --- |
| RR-D1 | Menu top-level desktop | **Exactement 4 entrées** visibles : Tous nos produits · Épicerie · Soin & Bien-être · Découvrir | ☒ OK | `["Tous nos produits","Épicerie","Soin & Bien-être","Découvrir"]` — 4 entrées exactes, confirmé visuellement |
| RR-D1b | Absence « Nos univers » desktop | **Aucune** entrée « Nos univers » visible à 1280 px (masquée par CSS · classe `ck-nav-mobile-univers` sur le `<li>`) | ☒ OK | `<li class="nav-item dropdown ck-nav-mobile-univers">` avec `display: none` confirmé — la classe s'applique désormais correctement (xpath `t-elif` opérant) |

**Preuve** : [`nav1_desktop_1280_header_postfix.png`](./captures/recette_nav1_v2/nav1_desktop_1280_header_postfix.png)

### Grille ciblée — mobile 390 px (Bug B2)

| # | Contrôle | Attendu | ☐ | Note QA |
| ---: | --- | --- | --- | --- |
| RR-M1 | Drawer sans doublon | **Tous nos produits · Nos univers · Découvrir** — **pas** d'entrées plates Épicerie / Soin en plus de l'accordéon | ☒ OK | Entrées `.ck-nav-desktop-universe` toujours présentes dans le DOM (attendu, pour le fallback) mais `display: none` confirmé — plus aucune visible en plat |
| RR-M2 | Accordéon Nos univers ouvert | Épicerie · Soin & Bien-être **une seule fois** chacun (sous Nos univers) | ☒ OK | `epicerieVisible: 1/2`, `soinVisible: 1/2` — une seule occurrence visible chacun, confirmé aussi visuellement sur capture |
| RR-M3 | Navigation enfants | Clic Épicerie → `/shop/category/epicerie-1` · Soin → `/shop/category/maison-bien-etre-2` | ☒ OK | hrefs exacts vérifiés sur les liens visibles de l'accordéon |

**Preuves** : [`nav1_mobile_390_drawer_postfix.png`](./captures/recette_nav1_v2/nav1_mobile_390_drawer_postfix.png) · [`nav1_mobile_390_nos_univers_open_postfix.png`](./captures/recette_nav1_v2/nav1_mobile_390_nos_univers_open_postfix.png)

### PV re-recette (à compléter)

| Champ | Valeur |
| --- | --- |
| **Recetteur** | Assistant IA (Claude), en session avec doreviateam |
| **Date re-recette** | 2026-06-21 |
| **Versions constatées** | `dorevia_ck_marketone_content` **19.0.1.26.1** · `dorevia_ck_theme` **19.0.1.37.1** |
| **Verdict re-recette B1/B2** | ☒ **GO** |

| Bug | Verdict | Commentaire |
| --- | --- | --- |
| B1 — Nos univers masqué desktop | ☒ OK | Correctif xpath (`t-if` + `t-elif`) vérifié efficace — classe `ck-nav-mobile-univers` désormais appliquée et règle CSS opérante |
| B2 — pas de doublon mobile | ☒ OK | Correctif SCSS (suppression du préfixe redondant) vérifié efficace — une seule occurrence visible par entrée univers en mobile |

**Verdict global lot Nav-1** (après re-recette) :

- ☒ **GO merge** — PV §8 initial + §8 bis OK

**Commentaire QA** :

1. Les deux correctifs B1/B2 sont confirmés efficaces, sans effet de bord détecté sur le reste du périmètre déjà validé en §8 (mega Découvrir, CTA, contraste, routes, panier, S4). Tests auto 15/15. Recommandation : merge.
2. Rappel non bloquant déjà noté en §8 : la requête externe Google Fonts (Inter/Inter Tight, N6) reste à signaler en dehors de ce lot — non liée à Nav-1.
3. Rappel process déjà noté en §1.3 : toujours rejouer `bootstrap_ck_navigation(env)` manuellement après un passage de tests `HttpCase` avant toute recette écran sur cette instance partagée.

---

## 9. Références

| Document | Rôle |
| --- | --- |
| [`RECETTE_QA_LOT_NAV1_NAVIGATION_CK_V2.md`](./RECETTE_QA_LOT_NAV1_NAVIGATION_CK_V2.md) | Recette Dev · mapping · tests · §10 bis pré-rempli |
| [`TICKET_DEV_LOT_NAV1_NAVIGATION_CK_V2.md`](../TICKET_DEV_LOT_NAV1_NAVIGATION_CK_V2.md) | Critères d'acceptation MOA C1–C17 |
| [`COMPOSITION_HEADER_V1_2.md`](./COMPOSITION_HEADER_V1_2.md) | Baseline header pré-Nav-1 |
| [`REFERENCE_INSTANCE_RECETTE_DOREVIA_CK_THEME_01.md`](../REFERENCE_INSTANCE_RECETTE_DOREVIA_CK_THEME_01.md) | Accès instance · thème actif |

---

*Note d'intervention QA · Lot Nav-1 · Navigation CK V2 · **clôturée GO merge · 2026-06-21**.*
