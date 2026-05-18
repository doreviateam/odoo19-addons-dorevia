# TICKET — Cadrage Culture / Territoires `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_CULTURE_TERRITOIRES_CADRAGE` |
| **Univers** | **Culture** — découvrir |
| **Type** | **Cadrage uniquement** — aucun code |
| **Statut** | **Clôturé — GO cadrage avec réserves légères** (2026-05-18) |
| **Exécution** | [`TICKET_MARKETONE_CULTURE_TERRITOIRES_EXEC.md`](TICKET_MARKETONE_CULTURE_TERRITOIRES_EXEC.md) — **ouvert**, en attente GO MOA |
| **Version module de référence** | `19.0.7.0.0` |
| **Base** | `ckr-marketone-01` |
| **Prérequis** | Socle Lots 1–5 **GO** ; portes 6.1 / 6.2 **GO** ; consolidation portes Boutique **GO** ; **ADR-024** / **NOTE_UNIVERS_CK_MARKETONE** **GO** |
| **ADR** | [ADR-024](../cadrage/DECISIONS.md#adr-024--structuration-c-kreyol-en-trois-univers-boutique-culture-savoirs), [ADR-018](../cadrage/DECISIONS.md#adr-018--articulation-des-trois-dimensions-c-kreyol) |
| **Boutique liée** | [ADR-025](../cadrage/DECISIONS.md#adr-025--lot-62-porte-origines-marketone_modeorigin) — porte Origines ; [C3.B](../cadrage/CONTRACTS.md#c3b--porte-origines-lot-62--figé-cadrage-2026-05-18) |
| **Consolidation** | [`TICKET_MARKETONE_CONSOLIDATION_PORTES_BOUTIQUE.md`](TICKET_MARKETONE_CONSOLIDATION_PORTES_BOUTIQUE.md) (**GO**) |
| **Note univers** | [`NOTE_UNIVERS_CK_MARKETONE.md`](../cadrage/NOTE_UNIVERS_CK_MARKETONE.md) §2.2, §4.2, §7.2 |
| **Roadmap** | [`ROADMAP.md`](../pilotage/ROADMAP.md) |

---

## Objectif

Définir comment C-Kreyol pourra **raconter les territoires / origines** dans l’univers **Culture**, **sans** :

- transformer `/shop` en page éditoriale ;
- créer un moteur catalogue parallèle ;
- confondre le profil Boutique `marketone.shop.origin` avec un modèle éditorial Culture.

```text
Critère attendu (cadrage validé) :
Un visiteur peut découvrir un territoire / une origine dans un espace Culture dédié,
tout en achetant via la Boutique existante (porte Origines, fiche produit, tunnel).
Le produit reste prioritaire ; le récit enrichit sans brouiller.
```

**Ce ticket ne livre aucun** fichier Python, XML, SCSS, test, ni ticket d’exécution.

---

## Contexte — ce qui existe déjà

### Boutique (ne pas refondre)

| Élément | Statut | Rôle |
|---------|--------|------|
| `/shop` | Livré | Catalogue général |
| Porte **Incontournables** | GO avec réserves | `marketone_mode=featured` |
| Porte **Origines** | GO | `marketone_mode=origin` + `marketone_origin=<slug>` |
| `marketone.shop.origin` | Livré | Profil **minimal** : slug, nom visiteur, phrase courte, lien attribut **Origine** |
| Fiche produit | Lot 4 | Bloc **Origines** léger ; lien optionnel vers porte filtrée |
| Consolidation portes | **GO** | Référence grammaire Boutique |

### Culture (à cadrer)

| Élément | Statut |
|---------|--------|
| Pages territoire / récit origine | **Non défini** |
| Navigation « Culture » | **Non implémentée** (home oriente Boutique) |
| Lien Boutique → Culture | **Partiel** : fiche → porte `/shop?…` uniquement (achat, pas récit) |
| Legacy `ckr.shop.origin` | Mémoire — **ne pas porter** tel quel |

**Double lecture Origines (validée MOA)** :

| Couche | Univers | Où |
|--------|---------|-----|
| Filtre achetable | **Boutique** | `/shop` + `marketone_mode=origin` — **livré** |
| Récit territoire | **Culture** | Espace dédié — **ce ticket** |

---

## Contraintes MOA (non négociables)

| # | Contrainte |
|---|------------|
| C1 | **Culture hors `/shop`** — pas de hero territoire, hub ou mur éditorial sur la grille boutique |
| C2 | **Pas de refonte Boutique** — portes 6.1 / 6.2, tunnel panier / checkout inchangés sauf liens explicitement cadrés |
| C3 | **Pas de hub Culture massif** dès le premier lot d’exécution (pas d’encyclopédie multi-territoires, pas de portail « toutes les origines » type legacy Explorer) |
| C4 | **Pas de contenu long** sur la fiche produit — retail-first (C7.4) ; prolongement Culture = pages ou blocs secondaires |
| C5 | **Liens** depuis porte Origines ou fiche produit vers Culture — **autorisés en principe**, détail (libellé, URL, placement) **à trancher** dans ce cadrage ; pas d’implémentation avant GO |
| C6 | **`marketone.shop.origin` reste minimal** — pas d’extension encyclopédique ; pas de fusion avec un futur modèle Culture sans décision MOA |
| C7 | **Pas de moteur catalogue parallèle** — les produits d’un territoire restent trouvés via `/shop` + porte Origines |
| C8 | **Pas de dépendance** `dorevia_ckreyol_marketplace` — lecture seule pour intuitions |
| C9 | **Pas de code** dans ce ticket |
| C10 | **Pas de Savoirs** (recettes contributives) — ticket séparé ultérieur |

**Agencement ADR-018 / ADR-024** :

```text
Le produit d'abord.
Le récit ensuite.
Le savoir en prolongement.
```

---

## Décisions à trancher (MOA + archi)

### D1 — Conteneur technique Culture (premier lot)

| Option | Description | Pour | Contre |
|--------|-------------|------|--------|
| **A — Pages `website` + snippets Marketone** | Une page par territoire (ou rubrique) ; QWeb scoped `marketone-culture` | Simple, éditorial BO, pas de couplage shop | Gouvernance contenu, pas de lien fort slug origine sans convention |
| B — Modèle dédié `marketone.culture.territory` (ou similaire) | Champs structurés, slug, publication | Cohérence slug avec `marketone.shop.origin` | Risque modèle trop tôt ; tentation champs encyclopédiques |
| C — Réutiliser / étendre `marketone.shop.origin` | Un seul modèle | Moins de tables | **Rejeté** par contrainte C6 — mélange Boutique / Culture |
| D — Blog Odoo / `website_blog` | Articles par territoire | Natif Odoo | Bruit SEO, hors identité Marketone |

**Recommandation cadrage** : **A** pour un **premier lot minimal** ; **B** seulement si MOA exige slug unique partagé avec profil origine — alors modèle Culture **séparé** avec clé étrangère optionnelle vers `marketone.shop.origin`, sans alourdir ce dernier.

**Décision MOA** : ☑ **A** — pages `website` + snippets Marketone sobres. **Pas** de modèle Culture dédié au v1 sauf besoin technique démontré.

---

### D2 — URL et slug territoire

| Option | Exemple | Note |
|--------|---------|------|
| **A — Préfixe Culture dédié** | `/culture/guadeloupe`, `/culture/martinique` | **Retenu MOA** |
| B — Alignement slug porte | `/origines/guadeloupe` (hors `/shop`) | Rejeté — collision sémantique avec alias `/origines` |
| C — Sous-pages website | `/page/guadeloupe` (slug CMS) | Rejeté v1 |

**Décision MOA** : ☑ **`/culture/<slug>`** — ex. `/culture/guadeloupe`. Alias Boutique `/origines` → `/shop?marketone_mode=origin` **inchangé**.

**Règle slug** : alignement avec `marketone.shop.origin.slug` **recommandé** — **sans** fusion des modèles.

---

### D3 — Périmètre du premier lot Culture (exécution future)

| Option | Périmètre | Pour | Contre |
|--------|-----------|------|--------|
| **A — Une page territoire pilote** | 1 origine (ex. Guadeloupe) : titre, chapô, 2–3 sections courtes, CTA vers porte Boutique | Livrable MOA rapide ; pas de hub | Navigation globale Culture absente ou minimale |
| B — Rubrique + 2–3 territoires | Index sobre + pages filles | Meilleure démonstration univers | Scope creep |
| C — Hub « Toutes les origines » | Liste cartes territoires | Proche legacy | **Rejeté** par contrainte C3 pour v1 |

**Recommandation cadrage** : **A** — une page pilote + convention URL ; index Culture **reporté** lot suivant.

**Décision MOA** : ☑ **A** — une seule page territoire pilote. **Pas** de hub « toutes les origines » au premier lot Culture.

---

### D4 — Contenu d’une page territoire (niveau éditorial max v1)

Champs ou blocs **autorisés** (proposition — à valider) :

| Bloc | Autorisé v1 | Interdit v1 |
|------|-------------|-------------|
| Titre territoire | ☑ | |
| Chapô (1 paragraphe court) | ☑ | Mur de texte |
| Image ou visuel hero **léger** | ☑ optionnel | Galerie lourde |
| 2–3 sections texte courtes | ☑ | Encyclopédie |
| CTA **Acheter les produits de …** → porte Origines filtrée | ☑ | Grille produits embarquée |
| Carte interactive / timeline | | ☑ |
| Producteur détaillé / B2B | | ☑ (lot ultérieur) |
| Recettes | | ☑ — univers **Savoirs** |

**Décision MOA** : ☑ Chapô + sections courtes + CTA porte Origines. **Pas** de page encyclopédique. Page **courte, élégante, visuelle** (réserve R1).

---

### D5 — Liens Boutique → Culture

| Emplacement | Comportement actuel | Options cadrage |
|-------------|---------------------|-----------------|
| Bandeau porte `/shop?marketone_mode=origin` | Intro courte ; lien « Tous les produits » | **Option** : lien « Découvrir [territoire] » si facette unique → page Culture |
| Bandeau mode seul (sans facette) | Catalogue complet + bandeau Origines | **Pas** de hub Culture sur `/shop` ; lien éventuel vers **index Culture** seulement si D3=B |
| Fiche produit — bloc Origines | Lien → porte filtrée (Boutique) | **Option** : second lien « En savoir plus » → page Culture (même slug) |
| Home | CTA Boutique uniquement | Entrée Culture **reportée** ou lien discret secondaire |

**Recommandation cadrage** : v1 — lien Culture depuis **fiche produit** (facette connue) et **bandeau origine facetée** uniquement ; pas de refonte home.

**Décision MOA** : ☑ Liens possibles depuis **fiche produit** et **bandeau Origines facetté** — **implémentation** au ticket exec. **Pas** de hub Culture dans `/shop`.

---

### D6 — Relation `marketone.shop.origin` ↔ contenu Culture

| Règle | Détail |
|-------|--------|
| Profil Boutique | Inchangé : slug, `name_visitor`, `context_phrase`, visibilité, `attribute_value_id` |
| Contenu Culture | Stocké ailleurs (page ou modèle D1) |
| Liaison | **Option** : même `slug` + `website_id` ; pas de FK obligatoire en v1 si pages CMS |
| BO | Éviter un seul écran « origine encyclopédique » |

**Décision MOA** : ☑ Même slug possible. **Pas** de fusion de modèles. `marketone.shop.origin` reste profil Boutique **minimal** (réserve R4).

---

### D7 — Navigation et entrée univers Culture

| Option | Description |
|--------|-------------|
| A | Pas de menu Culture au premier lot — accès par lien contextuel depuis Boutique |
| B | Entrée header « Découvrir » → page index Culture sobre (2–3 liens) |
| C | Reprise menu legacy (Communauté, etc.) | **Déconseillé** |

**Recommandation cadrage** : **A** ou **B minimal** — pas de menu multi-mondes legacy.

**Décision MOA** : ☑ **Liens contextuels** en v1. Entrée header Culture **reportée** tant que la page pilote n’est pas validée visuellement.

---

### D8 — SEO et indexation

| Sujet | Options |
|-------|---------|
| Pages Culture | Indexables ou `noindex` jusqu’à maturité contenu ? |
| Lien avec porte `/shop?marketone_mode=origin` | Canoniques distincts ; pas de duplicate shop |

**Décision MOA** : ☑ **Documentation seulement** — pas de chantier SEO avancé au premier lot Culture.

---

## Référence legacy (lecture seule)

| Intuition utile | Source legacy | Reprise Marketone |
|-----------------|---------------|-------------------|
| Hero territoires | `ckr_hero.xml` | **Non** sur `/shop` ; hero **léger** page Culture seulement si MOA valide |
| Origines structurées | `ckr.shop.origin` | **Non** porter — `marketone.shop.origin` reste minimal |
| Bloc fournisseur / éditorial | snippets masqués MVP | Inspiration **Culture** — lots séparés |
| CTA « Explorer les origines » | homepage / hero | Remplacer par entrée Culture explicite, pas par porte shop seule |

Références : `NOTE_UNIVERS_CK_MARKETONE.md` §4.2 ; `dorevia_ckreyol_marketplace/docs/direction/VISION_CK_MEDIA_COMMERCE.md`.

---

## Garde-fous

| # | Garde-fou |
|---|-----------|
| G1 | Aucun contenu Culture principal sur `/shop` |
| G2 | Aucun catalogue produit hors `website_sale` |
| G3 | Fiche produit : pas d’encyclopédie ; pas de JS lourd |
| G4 | Premier lot : **petit** — une page pilote ou rubrique minimale |
| G5 | Pas de forum, commentaires libres, UGC |
| G6 | Pas de code sans ticket d’**exécution** Culture GO |
| G7 | Non-régression tests portes Boutique (76 tests) |
| G8 | Séparation Savoirs (recettes) — ticket distinct |

---

## Hors périmètre (explicite)

| Exclusion | Report |
|-----------|--------|
| Code, maquettes implémentées | Ticket exécution post-GO cadrage |
| Lot 6.3 Promotions / Kits / Collections | Backlog Boutique |
| Module recettes / Savoirs contributifs | Ticket Savoirs |
| Refonte home Explorer / chips multi-portes | Décision MOA séparée |
| Portage `ckr.shop.origin` | Interdit |
| Hub « toutes les origines » v1 | Interdit (C3) |
| Contenu producteur B2B, CRM, newsletter | Backlog |

---

## Livrables cadrage (documents)

| # | Livrable |
|---|----------|
| L1 | Décisions D1–D8 tranchées MOA | ✅ |
| L2 | Schéma URL `/culture/<slug>` | ✅ |
| L3 | Wireframe texte — ticket exec | ✅ |
| L4 | Contrat **C8** dans `CONTRACTS.md` | ✅ |
| L5 | **ADR-026** dans `DECISIONS.md` | ✅ |
| L6 | Ticket exec | ✅ ouvert |

---

## Critères GO cadrage

- [x] Conteneur Culture (D1) tranché — pas d’extension encyclopédique de `marketone.shop.origin`
- [x] URLs Culture (D2) `/culture/<slug>` — sans collision `/origines` Boutique
- [x] Périmètre v1 (D3–D4) **petit** et validé — pas de hub massif
- [x] Liens Boutique → Culture (D5) explicités — implémentation au ticket exec
- [x] Navigation Culture (D7) tranchée
- [x] Garde-fous G1–G8 acceptés
- [x] Hors périmètre accepté
- [x] Ticket exécution rédigé

---

## Décision de sortie (MOA)

```text
[ ] GO cadrage Culture / Territoires
[x] GO cadrage avec réserves légères
[ ] NO GO — reporter ou reformuler
```

**Date** : 2026-05-18 · **Validé par** : MOA

### Réserves légères

| # | Réserve |
|---|---------|
| R1 | Première page Culture : **courte, élégante, visuelle** |
| R2 | Ne pas transformer Culture en **blog** complet |
| R3 | Ne pas injecter de contenu Culture **long** dans `/shop` |
| R4 | Ne pas enrichir `marketone.shop.origin` de champs éditoriaux longs |
| R5 | Ne pas ouvrir **Savoirs / recettes** dans le même lot |

---

## Prochaine étape

1. **MOA** : valider le ticket d’**exécution** [`TICKET_MARKETONE_CULTURE_TERRITOIRES_EXEC.md`](TICKET_MARKETONE_CULTURE_TERRITOIRES_EXEC.md).
2. **Pas de code** tant que l’exécution n’est pas **GO**.
3. **Ne pas** lancer Lot 6.3 Boutique en parallèle sans décision MOA.

---

## Références

| Document | Rôle |
|----------|------|
| `cadrage/NOTE_UNIVERS_CK_MARKETONE.md` | Univers Culture ; audit legacy |
| `cadrage/DECISIONS.md` — ADR-018, ADR-024, ADR-025 | Doctrine et porte Origines |
| `cadrage/CONTRACTS.md` — C3.B, C7 | Boutique ; fiche retail-first |
| `tickets/TICKET_MARKETONE_CONSOLIDATION_PORTES_BOUTIQUE.md` | Grammaire portes GO |
| `tickets/TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES.md` | Séparation Boutique / Culture Origines |
| `pilotage/ROADMAP.md` | Planning |
