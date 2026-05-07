# CK — Inventaire des pattern-blocs (page Home)

## 1. Objectif

Cartographier les **zones structurantes** de la page d’accueil C-Kreyol, qualifier leur **statut documentaire**, et préciser leur **potentiel** de mutation future en **snippet Odoo déposable** (éditeur Website).

**Convention** (voir [`../README.md`](../README.md)) :

- **pattern-bloc** — référence UX/UI documentée sous `docs/design_system/pattern-blocs/` ;
- **snippet Odoo** — bloc QWeb technique, éventuellement enregistré comme bloc **réutilisable / déposable** dans l’éditeur (`website` snippets), généralement sous `views/snippets/`.

Flux de décision :

```text
Identifier le pattern → documenter comme pattern-bloc → décider ensuite s’il devient snippet Odoo déposable
```

Cette note est **exclusivement documentaire** : elle ne prescrit pas de refonte ni la création de nouveaux snippets éditoriaux.

---

## 2. Source de vérité technique (composition actuelle)

L’ordre et la présence des blocs dans le `#wrap` de la Home sont définis par :

- **Assemblage** : `views/pages/ckr_homepage.xml` (héritage de `website.homepage`, priority élevée).
- **Drapeau QWeb** : `ckr_hpage_mvp1_tail_blocks` (valeur par défaut **0**) — lorsqu’il vaut **0**, les blocs **Fournisseur** et **Éditorial** ne sont **pas** rendus.

**Séquence effective par défaut** (`ckr_hpage_mvp1_tail_blocks = 0`) :

1. Hero (`ckr_snippet_hero` → `views/snippets/ckr_hero.xml`)
2. Explorer / portes (`ckr_snippet_entries` → `ckr_entries.xml`)
3. Sélection produits (`ckr_snippet_selection` → `ckr_selection.xml`)
4. Newsletter (`ckr_snippet_circle` → `ckr_circle.xml`)
5. En pratique / réassurance (`ckr_snippet_trust` → `ckr_trust.xml`)

**Blocs présents dans le fichier mais hors flux par défaut** (`t-if="ckr_hpage_mvp1_tail_blocks"`)

- Fournisseur (`ckr_snippet_supplier` → `ckr_supplier.xml`)
- Éditorial (`ckr_snippet_editorial` → `ckr_editorial.xml`)

Le **header** et le **footer** ne sont pas dans `#wrap` : ils relèvent du layout global (`views/layout/ckr_header.xml`, `views/layout/ckr_footer.xml`).

---

## 3. Précision importante : « template snippet » vs « snippet déposable »

Dans le code CK, plusieurs blocs Home portent un id de template préfixé `ckr_snippet_*` et vivent sous `views/snippets/`. Cela reflète une **implémentation QWeb modulaire**, pas nécessairement un **enregistrement** en snippet Website **glissable-déposable** dans l’UI.

Dans les colonnes ci-dessous, **« Candidat snippet Odoo ? »** vise le **cas d’usage éditorial** (bloc réutilisable par un éditeur de page), pas le simple fait d’exister en fichier `views/snippets/`.

---

## 4. Table d’inventaire (validée / ajustée par rapport au code)

| Zone / lecture | Pattern-bloc candidat | Statut doc | Candidat snippet Odoo déposable ? | Implémentation de référence & commentaire |
| --- | --- | --- | --- | --- |
| Layout — header global | [`PATTERN_BLOC_HEADER_NAV_3_NIVEAUX.md`](./PATTERN_BLOC_HEADER_NAV_3_NIVEAUX.md) | **Créé** | Non / partiel | `views/layout/ckr_header.xml` — pattern **global** (layout), pas un bloc Home isolé. Les trois lectures N0 / N1 / N2 sont matérialisées par `ckr-header__top0`, `ckr-header__inner` (top1), `ckr-header__top2` + drawer mobile. |
| Header N0 — flash / infos | *(dans ce doc)* | **Créé** (cf. header) | Non | **Écart vs lecture « Home »** : le bandeau rotatif `ckr-header__top0` n’est rendu que si le chemin commence par **`/shop`** (`t-if="ckr_path.startswith('/shop')"`) — **pas affiché sur la Home `/`**. À traiter comme pattern **boutique**, pas comme élément systématique de la Home. |
| Header N1 — services & recherche | *(dans ce doc)* | **Créé** (cf. header) | Non | Logo, recherche (desktop), locale, compte, favoris, panier, burger — même fichier. |
| Header N2 — navigation utile | *(dans ce doc)* | **Créé** (cf. header) | Non | Barre desktop `ckr-header__top2` + menu drawer (structure Odoo `website.menu_id`). |
| Home — hero | `PATTERN_BLOC_HOME_HERO.md` | **Créé** | Peut-être | `ckr_hero.xml` + `_hero.scss` + `ckr_homepage_hero_rotator.js`. Bon candidat **éditorial** à terme si besoin de dupliquer un hero ailleurs qu’en Home. |
| Home — Explorer / portes | [`PATTERN_BLOC_HOME_EXPLORER_PORTES.md`](./PATTERN_BLOC_HOME_EXPLORER_PORTES.md) | **Créé** | Oui, potentiellement | `views/snippets/ckr_entries.xml` + `_entries.scss` — articulation Home ↔ doctrine `/shop` ; candidat snippet déposable ultérieurement. |
| Home — sélection produits | `PATTERN_BLOC_HOME_SELECTION_PRODUITS.md` | À créer | Partiel | `ckr_selection.xml` — section + grille pilotée par le **site** (jusqu’à 4 produits). Pattern utile ; dépend du catalogue et de la config Website. |
| Home — carte produit « sélection » | `PATTERN_BLOC_PRODUCT_CARD_CATALOGUE.md` | À créer | Non libre | Rendu **interne** à la sélection Home : classes `ckr-selection__card*`. Distinct de la **card grille /shop** (autre contexte DOM). Documenter comme composant **pattern**, pas comme snippet éditorial autonome. |
| Home — newsletter | `PATTERN_BLOC_HOME_NEWSLETTER.md` | À créer | Oui | `ckr_circle.xml` (id historique `ckr_snippet_circle`) — formulaire, messages `cc_nl`, endpoint dédié. Très bon candidat snippet déposable **si** enregistré côté Website. |
| Home — En pratique | `PATTERN_BLOC_HOME_EN_PRATIQUE.md` | **Créé** | Oui | `ckr_trust.xml` — pattern déjà stabilisé ; bon candidat snippet déposable. |
| Layout — footer | `PATTERN_BLOC_FOOTER_RESPONSIVE.md` | **Créé** | Non | `ckr_footer.xml` + `_footer.scss` + `ckr_footer_fold.js` — **global**, pas spécifique Home. |
| Transverse — titres de section | `PATTERN_BLOC_SECTION_TITLE.md` | À créer plus tard | Non / micro | Ex. `ckr-section-title` dans `ckr_selection.xml` (et réutilisable ailleurs). Micro-pattern. |
| Transverse — duo CTA | `PATTERN_BLOC_CTA_DUO.md` | À créer plus tard | Non / micro | Présent notamment dans le hero ; micro-pattern. |
| Home — fournisseur (V1) | `PATTERN_BLOC_HOME_FOURNISSEUR.md` *(nom indicatif)* | À créer si réactivation MOA | Partiel | `ckr_supplier.xml` — **masqué** tant que `ckr_hpage_mvp1_tail_blocks` reste à 0. À inventorier si le MOA réactive le « bas de page V1 ». |
| Home — éditorial (V1) | `PATTERN_BLOC_HOME_EDITORIAL.md` *(nom indicatif)* | À créer si réactivation MOA | Partiel | `ckr_editorial.xml` — même drapeau que ci-dessus. |

---

## 5. Synthèse : la Home comme première source d’inventaire

La lecture produit est validée :

> La **Home** sert de **première source d’inventaire** des pattern-blocs CK. Certains restent des **références UX/UI** (layout global, micro-patterns). D’autres pourront, **plus tard**, devenir des **snippets Odoo déposables** après décision éditoriale et enregistrement Website.

**Ajustements majeurs par rapport à une lecture « tableau initial » seule** :

1. **Header N0** : pattern réel mais **conditionné `/shop`** — ne pas le compter comme visible sur la Home telle qu’implémentée aujourd’hui.
2. **Fournisseur + Éditorial** : présents dans le fichier Home mais **absents du rendu par défaut** ; à suivre sous forme de blocs « gel V1 » ou hors périmètre tant que le drapeau reste à 0.
3. **Card produit** : préciser **sous-contexte** (sélection Home vs catalogue `/shop`) pour éviter une doc trop générique.

---

## 6. Fichiers pattern-blocs déjà disponibles

- [`PATTERN_BLOC_HEADER_NAV_3_NIVEAUX.md`](./PATTERN_BLOC_HEADER_NAV_3_NIVEAUX.md)
- [`PATTERN_BLOC_HOME_EXPLORER_PORTES.md`](./PATTERN_BLOC_HOME_EXPLORER_PORTES.md)
- [`PATTERN_BLOC_HOME_HERO.md`](./PATTERN_BLOC_HOME_HERO.md)
- [`PATTERN_BLOC_HOME_EN_PRATIQUE.md`](./PATTERN_BLOC_HOME_EN_PRATIQUE.md)
- [`PATTERN_BLOC_FOOTER_RESPONSIVE.md`](./PATTERN_BLOC_FOOTER_RESPONSIVE.md)
