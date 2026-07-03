# Ticket Dev — Banner Univers CK · Lot A (Note 09)

| Champ | Valeur |
| --- | --- |
| Date | 3 juillet 2026 |
| Référence fonctionnelle | [`note_09.md`](note_09.md) |
| Référence technique | [`note_09_reponse.md`](note_09_reponse.md) |
| Projet | C-Kréyòl / CK Marketone |
| Base cible | `dorevia_ck_marketone_01` |
| Périmètre | Banner éditorial sur les 4 catégories e-commerce niveau 0 (Épicerie, Boissons, Soin & Bien-être, Artisanat) |
| Hors périmètre | Sous-catégories · `/shop` général · accents couleur par univers (`ck_banner_variant`, reporté Lot B) · fiche produit · nav/header |
| Modules | `dorevia_ck_marketone_content` (modèle + contenu + template) · `dorevia_ck_theme` (SCSS) |
| Version cible | `dorevia_ck_marketone_content` 19.0.1.81.0 → **19.0.1.82.0** · `dorevia_ck_theme` 19.0.1.119.0 → **19.0.1.120.0** (bump assets-only, `website_sale.scss` modifié — convention QA C6, pas de dossier `migrations/` requis) |
| Statut | **GO développement** (verdict MOA/QA du 3 juillet 2026, sous réserve des 5 ajustements §0bis + 5 compléments design §0ter) |

---

## 0bis. Ajustements MOA/QA intégrés (relecture du 3 juillet 2026)

| # | Ajustement demandé | Intégré en |
| --- | --- | --- |
| 1 | Bump version `dorevia_ck_theme` (SCSS modifié) | Header table + §4 |
| 2 | Fallback H1 compact sécurisé explicitement (`/shop` général + sous-catégories) | §3.3 T1/T1bis |
| 3 | `alt` image décorative → `alt=""` + `aria-hidden="true"` | §3.3 T4 |
| 4 | Tests sans URL hardcodée dépendante d'ID catégorie | §5 (Q1–Q3) |
| 5 | Réserve backlog — nettoyage tuiles sous-familles inactives | §8 (nouveau) |

## 0ter. Compléments design Carole intégrés (relecture du 3 juillet 2026)

| # | Complément demandé | Intégré en |
| --- | --- | --- |
| 1 | Séparateur visuel `.ck-univers-banner__accent` (40×3px, terracotta `#C75B3A`) | §3.3 T2bis + §3.4 S8 |
| 2 | Scrim verrouillé (dégradés desktop/mobile exacts, pas d'overlay noir) | §3.4 S3 |
| 3 | Fallback sans image verrouillé (`#F5F0EB` fond / `#3E2723` texte, pas de scrim) | §3.4 S5 |
| 4 | Exposition BO de `ck_universe` (en plus de `ck_subtitle`) | §3.5 V1/V1bis, §4, §6 (risque retiré) |

---

## 0. Confirmation technique demandée — tuiles sous-familles

Vérification effectuée sur [`website_sale_category_tiles.xml`](../../dorevia_ck_marketone_content/views/website_sale_category_tiles.xml#L14-L18) et [`shop_rayon_editorial.py`](../../dorevia_ck_marketone_content/shop_rayon_editorial.py#L92-L101) :

```python
t-value="(category.get_ck_category_family_tiles()
           if (category and not category.get_ck_rayon_editorial())
           else [])"
```

`get_ck_rayon_editorial()` appelle `get_rayon_editorial()`, qui **renvoie toujours un dict non-vide** (`{'title': ..., 'phrase': ...}` au minimum, jamais `None` ni `{}` — dégradé gracieux voulu dès la V1 shop banner). Un dict non-vide est toujours *truthy* en Python.

**Conséquence confirmée** : `not category.get_ck_rayon_editorial()` est toujours `False` dès qu'une `category` est présente → `ck_category_tiles` vaut systématiquement `[]` sur toute page catégorie aujourd'hui. Les tuiles sous-familles génériques (Note 07 Lot B) sont donc **déjà du code mort en l'état actuel**, indépendamment de ce ticket — pas seulement sur les 4 univers, mais sur *toute* catégorie ayant un `ck_universe` résolu (ce qui est le cas de toutes depuis l'introduction du champ).

**Implication pour ce ticket** : aucune action nécessaire pour « désactiver » les tuiles sur les univers — elles ne s'affichent déjà pas. Le Lot A n'a donc aucun risque de cumul banner + tuiles. Ce constat de code mort est signalé pour information mais **reste hors périmètre Lot A** (ne pas toucher `website_sale_category_tiles.xml` dans ce ticket, pour ne pas élargir la surface de changement).

---

## 1. Objectif

Réactiver et étendre le socle existant (`ck_universe`, `RAYON_EDITORIAL`, gabarit `.ck-rayon-banner`) pour afficher un banner éditorial complet sur les 4 catégories e-commerce niveau 0 : image native de catégorie, titre, accroche courte, scrim, accent CK unique (terracotta).

## 2. Décisions figées pour ce ticket

| # | Sujet | Décision retenue |
| --- | --- | --- |
| D1 | Composant | Extension de l'existant (`website_sale_rayon_editorial.xml`), pas de nouveau template parallèle |
| D2 | Activation | Automatique, `category and not category.parent_id and ck_rayon` — pas de champ `ck_banner_enabled` |
| D3 | Image | `<img>` HTML réel, `object-fit: cover`, source = `image_1024` natif de `product.public.category` |
| D4 | Accent couleur | Terracotta CK unique pour les 4 univers en Lot A (`ck_banner_variant` reporté Lot B) — matérialisé par le séparateur `.ck-univers-banner__accent`, seul accent couleur du lot (§3.3 T2bis) |
| D5 | Tuiles sous-familles | Aucune action requise — déjà inactives sur catégorie (cf. §0) |
| D6 | H1 | Mécanisme Shop-U3 conservé tel quel (`ck_rayon['title']` = H1 unique, natif masqué si `ck_rayon` actif) |

---

## 3. Axe d'implémentation — Lot A

### 3.1 Modèle — `product.public.category`

**Fichier** : `dorevia_ck_marketone_content/models/product_public_category.py`

| # | Tâche | Détail |
| --- | --- | --- |
| M1 | Nouveau champ | `ck_subtitle = fields.Char(string="Accroche banner univers", help="Accroche courte affichée dans le banner d'entrée d'univers (catégories niveau 0 uniquement). Laisser vide pour masquer le bloc accroche.")` |
| M2 | Pas de champ `ck_banner_enabled` | Cf. D2 |
| M3 | Pas de champ `ck_banner_variant` | Reporté Lot B (D4) |

### 3.2 Contenu éditorial

**Fichier** : `dorevia_ck_marketone_content/shop_rayon_editorial.py`

| # | Tâche | Détail |
| --- | --- | --- |
| C1 | Étendre `get_rayon_editorial()` | Ajouter au dict retourné : `'subtitle': category.ck_subtitle or None` et `'image_url': (f'/web/image/product.public.category/{category.id}/image_1024' if category and category.image_1920 else None)` — calcul uniquement quand `category` est fourni (le fallback `/shop` général garde `image_url: None`) |
| C2 | Fallback image absente | `image_url = None` si `category.image_1920` falsy — le template gère le fond clair CK de secours (§3.4 F2) |
| C3 | Fallback accroche absente | `subtitle = None` si `ck_subtitle` vide — le template masque le bloc sans laisser d'espace (§3.4 F3) |

**Note** : ne pas déclencher de recalcul d'image côté Python (pas de resize custom) — `image_1024` est déjà un champ dérivé standard `image.mixin`, aucun traitement additionnel nécessaire.

### 3.3 Template QWeb

**Fichier** : `dorevia_ck_marketone_content/views/website_sale_rayon_editorial.xml`

Remplacer le bloc actuel (lignes 15-20, `.ck-shop-intro--title-only`) par un bloc `.ck-univers-banner`, actif uniquement niveau 0 :

| # | Tâche | Détail |
| --- | --- | --- |
| T1 | Condition d'entrée niveau 0 | `t-set="ck_univers_banner" t-value="bool(ck_rayon and category and not category.parent_id)"` — variable explicite calculée une fois, pour éviter de dupliquer la condition composite dans plusieurs `t-if` |
| T1bis | **Branche fallback explicite (ajustement #2)** | `<section t-if="ck_univers_banner" class="ck-univers-banner">...</section>` **ET** `<section t-else="" t-if="ck_rayon" class="ck-shop-intro ck-shop-intro--title-only">...</section>` — les deux branches restent dans le même template, mutuellement exclusives sur la même variable `ck_univers_banner`. Le bloc `.ck-shop-intro--title-only` **n'est pas supprimé** : il devient la branche `else` explicite pour `/shop` général (`category` falsy) et les sous-catégories (`category.parent_id` truthy), garantissant qu'aucun état ne se retrouve sans H1 |
| T2 | Structure HTML (branche banner) | `<section class="ck-univers-banner">` → `<img>` fond (si `ck_rayon['image_url']`) → `<div class="ck-univers-banner__scrim">` → `<div class="container"><span class="ck-univers-banner__eyebrow">Univers</span><h1 class="ck-univers-banner__title" t-esc="ck_rayon['title']"/><p t-if="ck_rayon.get('subtitle')" class="ck-univers-banner__subtitle" t-esc="ck_rayon['subtitle']"/><div class="ck-univers-banner__accent"/></div>` |
| T2bis | **Séparateur visuel (complément design #1)** | `<div class="ck-univers-banner__accent"/>` — toujours rendu (pas de `t-if`), positionné en fin de `.container` : sous l'accroche si `ck_rayon.get('subtitle')` est présent, sinon directement sous le titre (ordre naturel du flux HTML, aucune condition supplémentaire nécessaire côté template — géré par le positionnement DOM) |
| T3 | Fallback sans image | `t-if`/`t-else` sur `ck_rayon['image_url']` → classe `ck-univers-banner--no-image` (fond clair CK, cf. SCSS S5) |
| T4 | **Alt image décorative (ajustement #3)** | Le titre et l'accroche sont déjà en texte HTML adjacent (T2) — l'image est donc purement décorative pour un lecteur d'écran. `<img alt="" aria-hidden="true" ...>` plutôt qu'un `alt` descriptif, pour éviter la répétition du H1/de l'accroche à la lecture assistée |
| T5 | H1 unique | Réutiliser tel quel `website_sale_rayon_editorial_hide_native_title` (lignes 26-39, **aucune modification**) — fonctionne identiquement quelle que soit la branche T1bis active, puisqu'il se base sur `ck_rayon`, pas sur `ck_univers_banner` |
| T6 | Loading | `loading="lazy"` sur l'`<img>` (cohérent avec les tuiles existantes) |

**Interdit** : toucher à `website_sale_category_tiles.xml` (cf. §0) et à `website_sale_rayon_editorial_hide_native_title` (déjà correct).

### 3.4 SCSS

**Fichier** : `dorevia_ck_theme/static/src/scss/website_sale.scss`

Nouveau bloc `.ck-univers-banner` (ne pas réutiliser `.ck-rayon-banner` tel quel — c'est un aplat couleur sans image, cf. `note_09_reponse.md` §1.2 ; le conserver inchangé, code mort mais non bloquant, hors périmètre de suppression pour ce ticket) :

| # | Règle | Détail |
| --- | --- | --- |
| S1 | Conteneur | `position: relative; height: 220px; overflow: hidden;` |
| S2 | Image de fond | `img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }` |
| S3 | **Scrim verrouillé — desktop (complément design #2)** | `.ck-univers-banner__scrim { background: linear-gradient(90deg, rgba(62, 39, 35, 0.78) 0%, rgba(62, 39, 35, 0.45) 45%, transparent 80%); }` — brun chaud CK exact, **jamais d'overlay noir** |
| S3bis | **Scrim verrouillé — mobile (complément design #2)** | Dans le media query S6 : `.ck-univers-banner__scrim { background: linear-gradient(to top, rgba(62, 39, 35, 0.80) 0%, rgba(62, 39, 35, 0.40) 50%, transparent 100%); }` — bascule latéral → vertical (`to top`) sous 767.98px |
| S4 | Texte | Eyebrow (`text-transform: uppercase`, petite taille), titre `$ck-font-display` / `$ck-text-3xl`, accroche `$ck-text-sm` max 2 lignes (`-webkit-line-clamp: 2`) |
| S5 | **Fallback sans image verrouillé (complément design #3)** | `.ck-univers-banner--no-image { background-color: #F5F0EB; } .ck-univers-banner--no-image .ck-univers-banner__title, .ck-univers-banner--no-image .ck-univers-banner__subtitle { color: #3E2723; } .ck-univers-banner--no-image .ck-univers-banner__scrim { display: none; }` — **pas de scrim** en mode sans image, valeurs CK exactes (pas de token générique) |
| S6 | Responsive mobile | `@media (max-width: 767.98px) { height: 180px; padding réduit; accroche 1 ligne si besoin (`-webkit-line-clamp: 1`) selon test visuel 390 px }` — inclut S3bis |
| S7 | Contraste | Vérifier ratio texte/scrim ≥ 4.5:1 (§15 note 09) sur l'image la plus claire du set (recette manuelle avec les 4 images réelles) — désormais vérifiable précisément puisque les valeurs de scrim sont fixées (S3/S3bis) |
| S8 | **Séparateur `.ck-univers-banner__accent` (complément design #1)** | `.ck-univers-banner__accent { width: 40px; height: 3px; background-color: #C75B3A; margin-top: <espacement cohérent avec $ck-space-2/3>; }` — ligne horizontale, unique accent couleur du Lot A. **Reste visible en mode fallback sans image** (S5 ne le masque pas, contrairement au scrim) puisqu'il ne dépend pas du contraste sur photo |

### 3.5 BO — exposition du champ

**Nouveau fichier** : `dorevia_ck_marketone_content/views/product_public_category_views.xml`

Aucune vue BO pour `product.public.category` n'existe actuellement dans le module — `ck_universe` n'était jusqu'ici modifiable qu'en base/migration, jamais en BO. **Complément design #4** : corrigé dans ce lot, coût marginal (même fichier de vue que `ck_subtitle`).

| # | Tâche | Détail |
| --- | --- | --- |
| V1 | Héritage `product_public_category_form_view` | Ajouter `ck_universe` **et** `ck_subtitle` à proximité de `image_1920` déjà présent nativement dans la vue standard |
| V1bis | **Champs exacts (complément design #4)** | `<field name="ck_universe"/>` puis `<field name="ck_subtitle" placeholder="Accroche courte du banner"/>` |
| V2 | Déclaration manifest | Ajouter `"views/product_public_category_views.xml"` dans `data`, avant `"views/website_sale_rayon_editorial.xml"` |

### 3.6 Migration

Pas de post-migration nécessaire : `ck_subtitle` est un nouveau champ optionnel, un `ck_subtitle` vide est un état valide et géré (fallback §3.2 C3). Bump version manifest `dorevia_ck_marketone_content` : `19.0.1.81.0` → `19.0.1.82.0` (convention QA C6 — bump systématique, dossier `migrations/` seulement si script requis, ce qui n'est pas le cas ici).

---

## 4. Fichiers pressentis

| Fichier | Nature |
| --- | --- |
| `dorevia_ck_marketone_content/models/product_public_category.py` | Ajout `ck_subtitle` |
| `dorevia_ck_marketone_content/shop_rayon_editorial.py` | Extension `get_rayon_editorial()` (`image_url`, `subtitle`) |
| `dorevia_ck_marketone_content/views/website_sale_rayon_editorial.xml` | Remplacement bloc `.ck-shop-intro--title-only` → `.ck-univers-banner` sur niveau 0 uniquement |
| `dorevia_ck_marketone_content/views/product_public_category_views.xml` *(nouveau)* | Exposition BO `ck_universe` **et** `ck_subtitle` (complément design #4) |
| `dorevia_ck_theme/static/src/scss/website_sale.scss` | Nouveau bloc `.ck-univers-banner` + media query mobile |
| `dorevia_ck_theme/__manifest__.py` | Bump version 19.0.1.119.0 → 19.0.1.120.0 (ajustement #1, assets-only) |
| `dorevia_ck_marketone_content/__manifest__.py` | Bump version + ajout entrée `data` |
| `dorevia_ck_marketone_content/tests/test_ck_shop_universe_banner.py` | Réécriture complète (cf. §5) |

---

## 5. Plan de tests

**Fichier** : `test_ck_shop_universe_banner.py` (`HttpCase`, réécriture — le test actuel affirme l'absence de bannière, contradictoire avec la cible)

**Ajustement #4 — résolution dynamique, pas d'URL hardcodée** : le test actuel (`SHOP_PATHS`, lignes 14-20) code en dur des slugs dépendants d'ID (`epicerie-1`, `boissons-123`...), fragiles à toute réinitialisation de séquence. `test_subcategory_inherits_parent_universe_h1()` (lignes 53-64) montre déjà le bon pattern dans le même fichier — à généraliser :

```python
category = self.env['product.public.category'].sudo().search(
    [('ck_universe', '=', 'epicerie')], limit=1)
slug = self.env['ir.http'].sudo()._slug(category)
html = self._shop_html(f'/shop/category/{slug}')
```

| # | Cas | Assertion |
| --- | --- | --- |
| Q1 | Banner présent sur les 4 univers niveau 0 | Pour chaque valeur de `ck_universe` (epicerie/boissons/soin/artisanat) : résoudre la catégorie racine par `search([('ck_universe', '=', valeur)])`, construire l'URL via `ir.http._slug()`, vérifier `ck-univers-banner` présent |
| Q2 | Absence sur `/shop` général | `ck-univers-banner` absent sur `/shop` (chemin fixe, pas d'ID — inchangé) |
| Q3 | Absence sur sous-catégorie | Réutiliser le pattern déjà en place lignes 53-77 (résolution/création dynamique d'un enfant) — `ck-univers-banner` absent, H1 compact conservé |
| Q4 | Image présente si catégorie renseignée | `<img` avec `object-fit`/classe attendue présent quand `image_1920` est set sur la catégorie de test |
| Q5 | Fallback sans image | Catégorie de test sans `image_1920` → classe `ck-univers-banner--no-image` présente, pas de `<img>` cassé |
| Q6 | Fallback sans `ck_subtitle` | Bloc `ck-univers-banner__subtitle` absent, pas d'espace vide (assertion structurelle, pas visuelle) |
| Q7 | Un seul H1 | Réutiliser `_visible_h1_texts()` existant — toujours exactement 1 H1 visible par page, sur les 5 chemins (`/shop` + 4 univers) |
| Q8 | Non-régression tuiles/toolbar/filtres | Rejouer `test_ck_shop_structure_s1.py`, `test_ck_shop_toolbar.py`, `test_ck_shop_filter_drawer.py`, `test_ck_shop_product_card.py` sans modification attendue |

**Recette manuelle complémentaire** (hors test automatisé) :
- Contrôle visuel 390 px sur les 4 univers avec images réelles.
- Contrôle contraste texte/scrim sur l'image la plus claire du set (§3.4 S7).
- Vérification qu'aucune tuile sous-famille ne s'affiche sur les 4 univers (confirmation du constat §0, pas une régression attendue de ce ticket).

---

## 6. Risques résiduels

| Risque | Commentaire |
| --- | --- |
| Contraste texte/scrim insuffisant selon l'image choisie | Pas de garantie automatique — contrôle manuel requis par image réelle (S7), pas testable unitairement |
| Poids image `image_1024` non optimisé | Champ standard `image.mixin`, pas de compression additionnelle prévue dans ce lot — à surveiller si les images sources sont volumineuses |
| `.ck-rayon-banner` (ancien SCSS) laissé en l'état, non supprimé | Code mort conservé pour ne pas élargir le diff — à traiter dans un ticket de nettoyage ultérieur si validé |
| Exposition BO élargie de `ck_universe` (complément #4) | Un changement de `ck_universe` en BO sur une catégorie déjà racine re-déclenche l'héritage `_get_ck_universe()` pour toute sa descendance — comportement déjà existant et voulu, mais désormais accessible sans passer par une migration ; à mentionner en recette MOA pour éviter une modification accidentelle |

---

## 7. Réserve backlog — hors périmètre (ajustement #5)

Ticket ultérieur à créer, non chiffré ici : **nettoyage / clarification des tuiles sous-familles génériques** (`website_sale_category_tiles.xml`, Note 07 Lot B). Constat §0 : la condition d'activation (`not category.get_ck_rayon_editorial()`) est toujours fausse depuis l'introduction de `ck_universe` — le composant est du code mort sur toute catégorie, pas seulement sur les 4 univers. À arbitrer en dehors de ce ticket : suppression, ou réactivation ciblée (ex. sous-catégories, hors scope banner) si le besoin fonctionnel est confirmé.

---

## 8. Statut

**GO développement CK-UNIVERSE-BANNER-001 Lot A** — verdict MOA/QA du 3 juillet 2026, après intégration des 5 ajustements §0bis et des 5 compléments design Carole §0ter. Lot B (`ck_banner_variant`, accents couleur par univers) reste **NO GO** à ce stade.
