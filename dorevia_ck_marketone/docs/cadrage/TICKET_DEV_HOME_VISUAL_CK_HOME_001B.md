# Ticket Dev — CK-HOME-001B — Réserves visuelles home (vedettes + coffrets)

Statut : **GO ouverture MOA** — périmètre serré **001B-a + 001B-b uniquement**.

Base locale : `dorevia_ck_marketone_01` — http://localhost:18079  
Versions de référence avant lot :

```text
dorevia_ck_marketone_content : 19.0.1.75.0
dorevia_ck_theme             : 19.0.1.114.0
```

Version cible après lot : `dorevia_ck_marketone_content : 19.0.1.76.0` (+ bump thème **uniquement** si correctif SCSS vedettes requis — cf. §3.1).

Références MOA : [`NOTE_MOA_CADRAGE_CK_HOME_001B_20260702.md`](NOTE_MOA_CADRAGE_CK_HOME_001B_20260702.md) · [`RECETTE_QA_RAPPROCHEMENT_HOME_MAQUETTE_V1.md`](../design/maquette_01.2/RECETTE_QA_RAPPROCHEMENT_HOME_MAQUETTE_V1.md) (réserves E1/E2).

---

## Gouvernance — renommage lot « producteurs home »

L’intention initiale « **CK-HOME-001B = bloc producteurs / transformateurs** » est **dépréciée**.

| Ancien sens | Nouveau sens CK-HOME-001B | Futur lot producteurs home |
| --- | --- | --- |
| Bloc producteurs / transformateurs en home | **Réserves visuelles** post-001A (vedettes + coffret) | **`CK-HOME-002`** ou **`CK-HOME-PRODUCERS-001`** — à cadrer séparément |

Ne pas mélanger les deux dans ce ticket.

---

## 1. Contexte

La home est **stabilisée** sur le fond et la structure :

| Lot | Statut | Ne pas rouvrir |
| --- | --- | --- |
| CK-HOME-001C | GO | Marque · newsletter FR · 4 univers |
| CK-HOME-001A | GO | Hero · CTA `/producteurs` · CA6 mobile |
| Navigation Option C | GO | Header catalogue |
| Tunnel achat V1 | Gel | Shop → checkout |

Il reste deux **réserves visuelles P1** documentées en recette QA (juin 2026), toujours observables en démo :

| ID | Bloc | Constat |
| --- | --- | --- |
| **E1** | Vedettes `ck-featured-products` | Produits · prix · liens OK — **zones image non visibles** (hauteur calculée `0px` en recette Playwright) |
| **E2** | Coffrets `ck-discovery-pack` | Bloc présent · CTA `/kits` OK — **fallback éditorial beige** (`ck-discovery-pack__visual--editorial`) faute de produit pack image en BO |

---

## 2. Objectif

Rendre les sections **« Nos coups de cœur »** et **« Coffrets découverte »** **présentables en démo** : images visibles, pas d’impression de catalogue incomplet.

Correction **visuelle ciblée** de la home existante — **sans refonte globale**.

---

## 3. Périmètre

### 3.1 — CK-HOME-001B-a — Vedettes (E1)

**Fichiers principaux**

| Fichier | Rôle |
| --- | --- |
| `home_featured.py` | SSR cartes · `build_featured_product_card_html()` · `bootstrap_home_featured_products()` |
| `dorevia_ck_theme/static/src/scss/website.scss` | Bloc `.ck-featured-products--maquette` · `.ck-product-card--home` · `aspect-ratio` image |
| `tests/test_ck_home_lot2_hooks.py` | Validation fragments · bootstrap |
| `tests/test_ck_home_lot2_compose.py` | Rendu HTTP home |

**Diagnostic Dev (point de départ)**

- Les cartes SSR portent bien un `background-image:url('/web/image/product…')` (validé par `card_fragment_is_valid` et `_CARD_IMAGE_RE`).
- Le markup actuel sépare le lien cover (`<a class="ck-product-card__cover">`) de la zone image (`<div class="ck-product-card__image …">`).
- Le SCSS impose `aspect-ratio: 1 / 1` sur `.ck-product-card__image` (l.684–697 `website.scss`) mais la recette QA a mesuré **hauteur `0px`** en runtime — investiguer collapse grid/flex ou conflit avec `.ck-product-card__cover`.

**Pistes de correction (choix Dev, borne visuelle)**

- Garantir une **hauteur visible** stable sur desktop 1280 et mobile 390 px (SCSS et/ou markup minimal).
- Alternative acceptable : `<img>` produit à la place du seul `background-image`, si plus fiable — sans changer la logique curation ni les CTA.
- **Ne pas** refondre la card shop ni la grille catalogue.

**Inchangé fonctionnellement**

- Curation `ck_is_featured` · `get_curated_featured_variants()` · prix · liens `/shop/...` · ajout panier · wishlist.

### 3.2 — CK-HOME-001B-b — Coffrets (E2)

**Fichiers principaux**

| Fichier | Rôle |
| --- | --- |
| `home_discovery_pack.py` | `get_discovery_pack_product()` · `_discovery_visual_html()` · `bootstrap_home_discovery_pack()` |
| `dorevia_ck_theme/static/src/scss/website.scss` | `.ck-discovery-pack__visual--editorial` (fallback beige) |
| `tests/test_ck_home_lot3_hooks.py` | Bootstrap · validateur arch |
| `tests/test_ck_home_lot3_compose.py` | Rendu HTTP |

**Diagnostic Dev**

- `get_discovery_pack_product()` cherche un produit publié avec image (`pack_ok=True` ou nom `ilike 'coffret'`).
- Si aucun produit : `_discovery_visual_html()` retourne le fallback **`ck-discovery-pack__visual--editorial`** (dégradé beige + icône cadeau).
- Le validateur `discovery_pack_arch_is_valid()` **n’exige pas** une vraie image — d’où la réserve E2.

**Pistes de correction (choix Dev, au moins une)**

1. **Seed catalogue** : produit coffret démo publié avec image BO (content module) — réutiliser `get_discovery_pack_product()` existant.
2. **Asset statique CK** : image coffret dans `dorevia_ck_marketone_content/static/` ou thème, branchée quand pas de produit BO.
3. **Renforcer le validateur** : après correction, `discovery_pack_arch_is_valid()` doit **rejeter** le fallback `--editorial` en production home (forcer re-bootstrap).

**Inchangé fonctionnellement**

- CTA `Découvrir` → `/kits` · comportement redirection pack · textes éditoriaux par défaut si pas de produit.

---

## 4. Hors scope (strict)

- Hero CK-HOME-001A (`home_hero.py`)
- Hygiène CK-HOME-001C (newsletter · marque · univers 4 cartes · `home_univers.py`)
- Navigation header · footer · démo tunnel
- **`/promotions`** (réserve P2 — **001B-c** — ticket ultérieur)
- Bloc producteurs / transformateurs home → futur **CK-HOME-002** / **CK-HOME-PRODUCERS-001**
- Copy éditorial bas de page (`home_editorial.py`)
- Refonte home complète · Lot 6 polish global
- SEO canonical · déploiement prod
- Tunnel achat · fiches produit (hors non-régression)

---

## 5. Critères d’acceptation

### CA1 — Vedettes visibles (001B-a)

- Chaque carte « Nos coups de cœur » affiche une **image produit visible** (hauteur > 0, pas de zone vide) sur **desktop 1280** et **mobile 390 px**.
- Les URLs `/web/image/product…` répondent **200** (pas de broken image).
- Prix, titres, liens fiche produit et CTA panier **inchangés**.

### CA2 — Coffret qualifié (001B-b)

- Le bloc coffrets n’affiche **plus** le fallback beige `ck-discovery-pack__visual--editorial` sur la home sandbox recettée.
- Un **visuel qualifié** est visible (`<img src="/web/image/…">` produit seedé **ou** asset statique CK documenté).
- CTA `/kits` fonctionnel.

### CA3 — Mobile 390 px

- Home complète : `scrollWidth` = `clientWidth` = 390 (pas d’overflow horizontal).
- Vedettes et coffret lisibles en viewport 390 px.
- Capture ou métriques JSON archivées (patron CA6 de 001A).

### CA4 — Non-régression

- Hero 001A (textes + CTA `/producteurs`) inchangé.
- Section univers 4 cartes (001C) inchangée.
- Dual Pro / Newsletter présent et fonctionnel.
- `/shop` et fiche produit témoin : **200** · ajout panier OK.
- Ordre blocs home conservé : Hero → Réassurance → Vedettes → Univers → Coffrets → Dual → Éditorial.

### CA5 — Tests automatisés

- Tags existants **verts** : `dorevia_ck_marketone_home_lot2`, `dorevia_ck_marketone_home_lot3`.
- Smoke home lot1 (`dorevia_ck_marketone_home_lot1`) : **0 failed**.

---

## 6. Recette QA / tests

### 6.1 Tests automatisés (obligatoires)

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 \
  --test-tags dorevia_ck_marketone_home_lot2,dorevia_ck_marketone_home_lot3,dorevia_ck_marketone_home_lot1 \
  --stop-after-init
```

### 6.2 Smoke manuel / Playwright

| Contrôle | Viewport |
| --- | --- |
| Images vedettes visibles | 1280 + **390** |
| Coffret sans fallback beige | 1280 + **390** |
| Overflow horizontal | 390 (`scrollWidth`/`clientWidth`) |
| Hero 001A non régressé | 1280 |
| `/shop` + fiche témoin | 1280 |

Scripts réutilisables (à adapter si assertions obsolètes) :

- `docs/design/maquette_01.2/scripts/ck_lot2_product_mobile390.mjs`
- `docs/design/maquette_01.2/scripts/ck_lot3_home_discovery_qa.mjs` (créer si absent — patron lot1/001A)
- Patron mobile : capture hero 001A (`ck_home_001a_hero_mobile_390.png`)

### 6.3 Migration

- Bump `__manifest__.py` → `19.0.1.76.0`
- Créer `migrations/19.0.1.76.0/post-migrate.py` sur le patron `19.0.1.75.0` :
  - `bootstrap_home_featured_products(env)`
  - `bootstrap_home_discovery_pack(env)`
  - `cr.commit()` + log métier CK-HOME-001B

### 6.4 Livrables documentation

- Note MOA clôture `NOTE_MOA_CLOTURE_CK_HOME_001B_20260702.md` (ou date livraison réelle)
- Captures desktop + mobile 390 px (vedettes + coffret)

---

## 7. Implémentation — checklist Dev

- [ ] Reproduire E1/E2 sur sandbox post-upgrade `19.0.1.75.0`
- [ ] Corriger visibilité images vedettes (SCSS et/ou markup — acte thème si nécessaire)
- [ ] Remplacer fallback coffret beige par image qualifiée (seed produit et/ou asset statique)
- [ ] Mettre à jour validateurs / tests lot2 et lot3 si critères visuels renforcés
- [ ] Migration `19.0.1.76.0` + upgrade sandbox + restart
- [ ] Recette 1280 + 390 px documentée
- [ ] Vérifier hero 001A / univers 001C / dual inchangés

---

## 8. Message de commit proposé

```text
fix(ck-home): CK-HOME-001B images vedettes visibles et visuel coffret qualifié
```

---

*Ticket Dev — C-Kréyòl Marketone · CK-HOME-001B — 2 juillet 2026*
