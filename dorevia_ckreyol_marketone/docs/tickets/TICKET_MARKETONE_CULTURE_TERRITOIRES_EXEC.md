# TICKET — Exécution Culture v1 — Page territoire pilote `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_CULTURE_TERRITOIRES_EXEC` |
| **Univers** | **Culture** — découvrir |
| **Lot** | Culture v1 — **une page territoire pilote** |
| **Statut** | **Ouvert** — en attente validation MOA pour exécution |
| **Version cible module** | `19.0.8.0.0` (proposition) |
| **Base** | `ckr-marketone-01` |
| **Prérequis** | Cadrage **GO avec réserves légères** — [`TICKET_MARKETONE_CULTURE_TERRITOIRES_CADRAGE.md`](TICKET_MARKETONE_CULTURE_TERRITOIRES_CADRAGE.md) ; consolidation portes Boutique **GO** ; Lots 6.1 / 6.2 **GO** ; ADR-024 **GO** |
| **ADR** | ADR-024, ADR-025, **ADR-026** (proposition) |
| **Contrats** | **C8** (proposition) ; C7.4 ; non-régression C3.A / C3.B |

---

## Objectif

Livrer **une seule page Culture** territoire pilote (ex. Guadeloupe), **hors** `/shop`, pour raconter un territoire de façon **courte, élégante et visuelle**, avec CTA vers la **porte Origines** Boutique — **sans** hub « toutes les origines », **sans** modèle Culture dédié au v1, **sans** enrichir `marketone.shop.origin`.

```text
Critère GO Culture v1 :
Un visiteur atteint /culture/<slug-pilote> (page sobre, non encyclopédique),
comprend le territoire en quelques scrolls, et peut acheter via
/shop?marketone_mode=origin&marketone_origin=<slug> — sans régression des portes Boutique.
```

**Aucun code** tant que ce ticket d’exécution n’est pas validé MOA.

---

## Décisions MOA figées (cadrage 2026-05-18)

| # | Décision |
|---|----------|
| **D1** | Conteneur : **pages `website` + snippets / templates Marketone** sobres — **pas** de modèle `marketone.culture.*` au v1 sauf besoin technique **démontré** |
| **D2** | URLs : préfixe **`/culture/<slug>`** — ex. `/culture/guadeloupe`, `/culture/martinique` — **pas** de collision avec alias Boutique `/origines` → `/shop?marketone_mode=origin` |
| **D3** | Périmètre v1 : **une page pilote** — pas de hub « toutes les origines » |
| **D4** | Éditorial : chapô + 2–3 sections courtes + visuel léger + CTA porte Origines — **pas** de page encyclopédique |
| **D5** | Liens Boutique → Culture : **inclus v1** depuis fiche produit et bandeau Origines **facetté** (si profil / slug cohérent) — **pas** de hub Culture sur `/shop` |
| **D6** | Même **slug** que `marketone.shop.origin` possible — **pas** de fusion de modèles ; profil Boutique **inchangé** |
| **D7** | Navigation : **liens contextuels** v1 — entrée header « Culture / Découvrir » **reportée** jusqu’à validation visuelle page pilote |
| **D8** | SEO : **documentation** uniquement — pas de chantier SEO avancé v1 |

### Réserves MOA (légères)

| # | Réserve |
|---|---------|
| R1 | Page Culture **courte, élégante, visuelle** |
| R2 | Ne pas transformer Culture en **blog** complet |
| R3 | **Aucun** contenu Culture long injecté dans `/shop` |
| R4 | **Ne pas** enrichir `marketone.shop.origin` de champs éditoriaux longs |
| R5 | **Ne pas** ouvrir Savoirs / recettes dans le même lot |

---

## Périmètre inclus (exécution)

### 1. Routing HTTP

| Livrable | Détail |
|----------|--------|
| Route | `GET /culture/<slug>` — contrôleur dédié **ou** `website.page` avec URL fixe — **sans** conflit `/origines` |
| Slug pilote | **Un** territoire MOA (ex. `guadeloupe`) — convention documentée pour extensions futures |
| 404 | Slug inconnu ou page non publiée → 404 propre ou redirect documenté (pas de 500) |
| Redémarrage | Si route contrôleur : documenter besoin restart daemon post-`-u` (alignement portes Boutique) |

### 2. Page Culture (QWeb + SCSS)

| Bloc | Règle |
|------|-------|
| Conteneur | Racine `.marketone-culture` (ou `.marketone-root` + modificateur culture) — scoped SCSS |
| Titre | Nom territoire (ex. Guadeloupe) |
| Chapô | **1** paragraphe court |
| Visuel | Image **légère** optionnelle — pas de galerie |
| Sections | **2 à 3** blocs texte courts — pas de mur éditorial |
| CTA principal | Lien vers `/shop?marketone_mode=origin&marketone_origin=<slug>` — libellé achetable |
| CTA secondaire | Retour boutique `/shop` ou home — sobre |

**Interdit** : grille produits embarquée ; pricelist ; `website_sale` sur la page Culture ; hero type legacy shop.

### 3. Contenu BO (recette)

| Élément | Détail |
|---------|--------|
| Page pilote | Contenu saisi en BO (`website.page` + builder **ou** template statique + champs limités) — **pas** de seed XML récit long |
| Cohérence slug | Slug URL `/culture/guadeloupe` aligné avec `marketone.shop.origin` slug `guadeloupe` si profil existant |
| `website_id` | Page publiée sur site courant (**My Website**) |

### 4. Liens Boutique → Culture (D5)

| Emplacement | Comportement cible |
|-------------|-------------------|
| Fiche produit — bloc Origines | Lien existant porte filtrée **conservé** ; ajout lien **« Découvrir … »** (ou libellé MOA) → `/culture/<slug>` si profil publié et slug résolu |
| Bandeau `/shop` Origines **avec facette** | Lien optionnel « Découvrir [territoire] » → `/culture/<slug>` |
| Bandeau Origines **sans facette** | **Pas** de lien hub Culture |
| `/shop` nu, home, header | **Pas** de hub Culture ; **pas** d’entrée menu header (D7) |

### 5. Non-régression

| Zone | Attendu |
|------|---------|
| Tests auto existants | **76** tests portes Boutique — **0** régression |
| Tag tests | `dorevia_marketone_culture_v1` (proposition) — HTTP page pilote + liens |
| Panier / checkout / featured / origin | Inchangés |

### 6. Documentation

| Livrable | Fichier |
|----------|---------|
| ADR-026 | `cadrage/DECISIONS.md` |
| Contrat C8 | `cadrage/CONTRACTS.md` |
| Recette MOA | `docs/recette/RECETTE_MANUELLE_CULTURE_V1.md` (à créer à l’exécution) |
| `ENV_REFERENCE` | Route `/culture/…`, prérequis BO |

---

## Hors périmètre (explicite)

| Exclusion | Report |
|-----------|--------|
| Hub `/culture` index « toutes les origines » | Culture v2 |
| Modèle ORM `marketone.culture.territory` | Sauf besoin technique démontré — par défaut **non** |
| Entrée menu header Culture | Post validation visuelle pilote |
| SEO avancé (canonical, noindex, sitemap) | Note doc seulement |
| Blog, forum, commentaires | — |
| Savoirs / recettes | Ticket Savoirs |
| Lot 6.3 Promotions / Kits / Collections | Backlog Boutique |
| Portage `ckr.shop.origin` / marketplace | Interdit |
| JS non justifié | Interdit (C4.5) |
| Deuxième page territoire | Culture v2 |
| Refonte home / Explorer | Ticket séparé |

---

## Fichiers indicatifs (à créer à l’exécution)

```text
controllers/culture.py              # GET /culture/<slug> (proposition)
views/pages/culture_territory.xml   # template page pilote
static/src/scss/_culture.scss       # styles scoped
tests/test_marketone_culture_v1.py
views/pages/product_origin.xml      # lien Découvrir → /culture/<slug> (extension)
views/pages/shop_origin.xml         # lien bandeau faceté (extension)
__manifest__.py                     # 19.0.8.0.0, assets, data si page XML seed minimale
```

> La liste exacte peut être ajustée à l’implémentation — **pas** de modèle Python Culture au v1 par défaut.

---

## Critères GO / NO GO exécution

### GO

- [ ] `GET /culture/<slug-pilote>` → **200**, contenu court, classes `marketone-culture`
- [ ] CTA vers porte Origines filtrée fonctionne
- [ ] Liens depuis fiche (et bandeau faceté si prévu) → page Culture
- [ ] **Aucun** contenu Culture ajouté sur `/shop` hors lien discret
- [ ] `marketone.shop.origin` **non** modifié (champs inchangés)
- [ ] 76 + tests culture v1 verts
- [ ] Mobile 375 px — pas de débordement horizontal

### NO GO

- [ ] Page encyclopédique ou blog-like
- [ ] Hub Culture sur `/shop`
- [ ] Grille produits sur page Culture
- [ ] Régression featured / origin / tunnel
- [ ] Extension encyclopédique `marketone.shop.origin`

---

## Checklist validation MOA (exécution)

```text
[x] Cadrage Culture GO avec réserves légères
[x] D1–D8 figées
[x] Une page pilote uniquement
[ ] GO pour implémentation  [ ] En attente  [ ] NO GO
```

---

## Prochaine étape

1. **MOA** : valider ce ticket d’**exécution**.
2. **Dev** : implémentation `19.0.8.0.0` **après** GO exécution uniquement.
3. **Pas** de Lot 6.3 Boutique ni Savoirs en parallèle sans décision MOA.
