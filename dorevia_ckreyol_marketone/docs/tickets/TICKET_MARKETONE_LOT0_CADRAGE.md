# TICKET — Lot 0 Cadrage `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_LOT0_CADRAGE` |
| **Lot** | 0 — Cadrage et audit |
| **Statut** | GO (2026-05-18) |
| **Date** | 2026-05-18 |
| **Auteur cadrage** | Agent IA (audit + docs) |
| **Décision attendue** | GO / GO avec réserves / NO GO |

---

## Objectif

Créer le **socle doctrinal** du nouveau module Odoo 19 CE `dorevia_ckreyol_marketone` avant toute génération de code, en s’inspirant conceptuellement de `dorevia_ckreyol_marketplace` sans le copier.

**Livrable Lot 0** : documentation lisible, sobre et validable permettant de lancer le Lot 1 (socle installable) sans ambiguïté.

---

## Contexte

### Canal C-Kreyol

C-Kreyol est la marque et le canal e-commerce Dorevia autour de produits du monde créole et agro-transformés antillais. Le site doit être **retail**, **mobile-first**, crédible pour une ouverture commerciale réelle.

### Module legacy

`dorevia_ckreyol_marketplace` (v `19.0.1.10.141`, ~248 fichiers) a livré un canal fonctionnel avec :

- Portes catalogue (promo, packs, featured, origines, collections, catégories)
- Doctrine `/shop` conteneur unique
- Filtres via `product.template._search_get_detail`
- Tests taggés par périmètre (16 fichiers)
- Documentation riche (~132 fichiers `docs/`)

Il porte aussi une **dette importante** :

| Zone | Symptôme |
|------|----------|
| Manifeste | Changelog ~430 lignes dans `description` |
| Contrôleur | `website_sale_ckr.py` ~1870 lignes |
| SCSS | `_shop.scss` ~3363 lignes, CSS défensif |
| QWeb | `ckr_shop.xml` ~1046 lignes, xpath fragiles |
| Thème | Dépendance obligatoire `theme_classic_store` |
| Migrations | 11 scripts historiques |
| Doc | Contradictions collections URL nobles vs redirects 301 |

### Module cible

`dorevia_ckreyol_marketone` existe aujourd’hui comme **dossier documentation** uniquement (`docs/README.md` comme index + livrables Lot 0).

---

## Doctrine

```text
Odoo vend.
Marketone présente, clarifie, oriente.
```

| Principe | Application |
|----------|-------------|
| Standard Odoo d’abord | `website_sale` = moteur |
| Spécifique = front / UX / éditorial | Pas de moteur parallèle |
| Sobriété | Peu de dépendances, peu de JS, peu de xpath |
| Mobile-first | Dès le Lot 2 |
| Mémoire propre | `cadrage/CONTRACTS.md` + `cadrage/DECISIONS.md`, pas le manifeste |
| Pas de copie mécanique | Inspiration ≠ duplication |

---

## Périmètre Lot 0

### Inclus

- Audit structuré de `dorevia_ckreyol_marketplace`
- Production des documents :

```text
docs/cadrage/ARCHITECTURE.md
docs/pilotage/ROADMAP.md
docs/cadrage/CONTRACTS.md
docs/cadrage/DECISIONS.md
docs/tickets/TICKET_MARKETONE_LOT0_CADRAGE.md
```

- Décisions de cadrage figées (voir `cadrage/DECISIONS.md`)
- Matrice portes catalogue **documentée** pour Lot 6 (non implémentée)
- Critères GO/NO GO Lot 0 et lots suivants

### Hors périmètre Lot 0

- Tout fichier Python, XML, SCSS, JS
- Installation Odoo
- Tickets Lots 1–6 (à créer après GO Lot 0)
- Migration de données depuis marketplace
- Contenu éditorial (textes, images, produits)

---

## Architecture cible (résumé)

Voir `docs/cadrage/ARCHITECTURE.md`.

```text
Marketone = couche présentation (SCSS, QWeb, website léger)
website_sale = catalogue + panier + checkout
portal = compte client standard
```

**Dépendances Lot 1** : `website`, `website_sale`, `portal`

**Préfixe technique** : `marketone_` (ADR-006)

---

## Lots de développement

| Lot | Objectif | Bloqué par |
|-----|----------|------------|
| **0** | Cadrage | — |
| **1** | Socle installable | GO Lot 0 |
| **2** | Identité front minimale | GO Lot 1 |
| **3** | Boutique `/shop` lisible | GO Lot 2 |
| **4** | Fiche produit | GO Lot 3 |
| **5** | Panier / checkout smoke | GO Lot 4 |
| **6** | Portes catalogue | GO Lot 5 |

Détail et critères : `docs/pilotage/ROADMAP.md`

---

## Critères GO / NO GO — Lot 0

### GO

- [ ] Les 5 documents Lot 0 sont présents et cohérents entre eux
- [ ] La doctrine « Odoo vend / Marketone présente » est explicite
- [ ] Les dettes legacy à éviter sont listées avec exemples concrets
- [ ] Les principes à conserver sont identifiés (hooks, `/shop`, tests taggés)
- [ ] Aucune ambiguïté sur « pas de code avant validation »
- [ ] L’équipe humaine peut autoriser le Lot 1 sans question bloquante

### GO avec réserves

- [ ] Réserves documentées (ex. noms paramètres URL Lot 6, modèle collections)
- [ ] Ticket Lot 1 créé avec réserves reprises comme tâches

### NO GO

- [ ] Contradiction non résolue entre README et CONTRACTS
- [ ] Périmètre Lot 1 encore flou (dépendances, structure)
- [ ] Décision de copier mécaniquement l’ancien module
- [ ] Ambition Lot 6 présentée comme déjà livrée

---

## Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Scope creep dès Lot 1 | Moyenne | Élevé | Tickets par lot ; pas de feature hors ticket |
| Reprise mécanique legacy | Moyenne | Élevé | ADR-001 ; revue Codex sur diff |
| Co-installation marketplace + marketone | Faible | Critique | ADR + doc ; désinstaller l’ancien |
| XPath fragiles Odoo 19 | Élevée | Moyen | Contrat C5 ; xpath sur `#wrap` |
| Visuel « trop Odoo natif » sans thème tiers | Élevée | Faible | Tokens SCSS Lot 2 ; acceptation MOA |
| Portes avant tunnel stable | Moyenne | Élevé | ADR-010 ; Lot 6 bloqué |
| Doc legacy contradictoire | Moyenne | Moyen | Une vérité dans CONTRACTS ; pas de copie mvp_* |
| Paramètres URL SEO | Faible | Moyen | Canonical Lot 6 ; alias 301 documentés |
| `product_pack` requis pour Kits | Certaine (si porte Kits) | Moyen | Dépendance optionnelle ADR-005 |

---

## Règles de non-régression

Applicables dès le Lot 1 et à chaque lot suivant :

1. **Install / update** : `-u dorevia_ckreyol_marketone` sans traceback.
2. **`/shop`** : HTTP 200, grille produits visible (Lots ≥ 3).
3. **Panier invité** : ajout produit sans 500 (Lots ≥ 5).
4. **Checkout** : au moins une étape accessible sans 500 (Lot 5).
5. **Tests smoke** : tag `dorevia_marketone_smoke` vert à chaque livraison.
6. **Pas de régression** sur routes `website_sale` standard non touchées.
7. **Assets** : pas de fuite CSS hors scope `.marketone-*` vers le BO.

En Lot 0 : non-régression = **ne pas introduire de code**.

---

## Audit legacy — synthèse exécutive

### Conserver (principes)

1. Doctrine standard Odoo + `website_sale`
2. `/shop` conteneur unique + query string
3. Filtres via `_search_get_detail` + options contrôleur
4. Whitelist paramètres + priorité modes
5. Tests taggés + données recette
6. Séparation couches + mobile-first
7. Hooks idempotents pour menus (vs XML fragile)

### Éviter (dette)

1. Manifeste-journal et 11 migrations
2. `theme_classic_store` obligatoire
3. Monolithes contrôleur / SCSS / QWeb
4. CSS/QWeb `!important` défensif
5. XPath réparation thème
6. État implicite sur `request`
7. Features hors socle (CRM pro, newsletter, hero rotator, 6 JS)
8. Seed XML prod obligatoire

### Matrice portes (référence Lot 6 — non livré)

| Porte | Entrée visiteur (alias) | Rendu canonique | Filtre |
|-------|-------------------------|-----------------|--------|
| Promotions | `/promotions` → 301 | `/shop?…=promo` | Pricelist items |
| Kits | `/kits` → 301 | `/shop?…=pack` | `pack_ok` |
| Incontournables | `/incontournables` → 301 | `/shop?…=featured` | Collection featured |
| Origines | `/origines` → 301 | `/shop?…=origin` | Attribut Origine |
| Catégories | `/categories` → 301 | `/shop?ckr_category=…` → `marketone_category=…` | Public category |
| Collections | `/collections` → 301 | `/shop?…=collection` | M2M collection |

> Noms de paramètres : réserve Lot 0 — préfixe `marketone_*` à figer avant implémentation.

---

## Décision explicite — ne pas copier l’ancien module

```text
DECISION — Création de dorevia_ckreyol_marketone

Le module dorevia_ckreyol_marketone est créé comme nouveau module Odoo 19 CE.
Il s’inspire conceptuellement de dorevia_ckreyol_marketplace mais ne le copie pas.
website_sale reste le moteur e-commerce principal.
Le premier objectif est un socle sobre, maintenable, mobile-first
et compatible ouverture commerciale réelle.
Le développement ne commence qu’après validation humaine du cadrage Lot 0.
```

**Fichiers legacy à ne pas porter tels quels**

- `controllers/website_sale_ckr.py`
- `views/pages/ckr_shop.xml`
- `views/pages/ckr_shop_classic_tile_restore.xml`
- `static/src/scss/layout/_shop.scss`
- `__manifest__.py` (changelog)
- `migrations/*`
- Arborescence `docs/mvp_*` (référence ponctuelle uniquement)

---

## Organisation de travail

```text
Architecture : David + ChatGPT
Développement : Agent IA (exécution ticket validé)
Qualité : Codex (relecture, tests, régressions)
Décision GO : Humaine
```

**Rôle Dev (Lots ≥ 1)**

- Exécuter le ticket validé
- Ne pas redéfinir la doctrine
- Ne pas élargir le périmètre sans validation
- Signaler incohérences avant de coder

**Rôle Codex (après livraison)**

- Relire diff
- Exécuter tests taggés
- Détecter xpath fragiles et dépendances opportunistes
- Proposer corrections

---

## Livrables produits (Lot 0)

| Fichier | Statut |
|---------|--------|
| `docs/README.md` | ✅ Index documentaire |
| `docs/cadrage/BRIEF_INITIAL.md` | ✅ Brief initial (préexistant) |
| `docs/cadrage/ARCHITECTURE.md` | ✅ |
| `docs/pilotage/ROADMAP.md` | ✅ |
| `docs/cadrage/CONTRACTS.md` | ✅ |
| `docs/cadrage/DECISIONS.md` | ✅ |
| `docs/tickets/TICKET_MARKETONE_LOT0_CADRAGE.md` | ✅ Ce ticket |

---

## Prochaine étape après GO Lot 0

1. Décision humaine consignée (commentaire ou mise à jour statut ticket)
2. Création `docs/tickets/TICKET_MARKETONE_LOT1_SOCLE.md`
3. Génération du socle technique Lot 1 :
   - manifeste sobre
   - structure dossiers
   - test smoke install
   - assets déclarés vides ou minimaux

**Aucun code ne doit être produit tant que ce ticket n’est pas en statut GO.**

---

## Checklist validation humaine

```text
[ ] J’ai lu README, BRIEF_INITIAL, ARCHITECTURE, ROADMAP, CONTRACTS, DECISIONS
[ ] J’accepte la doctrine « Odoo vend / Marketone présente »
[ ] J’accepte l’absence de thème tiers au socle
[ ] J’accepte le report des portes catalogue au Lot 6
[ ] J’accepte les dépendances minimales Lot 1
[ ] Je valide la non-copie mécanique de marketplace

Décision : [ ] GO  [ ] GO avec réserves  [ ] NO GO

Réserves éventuelles :
_________________________________________________

Validé par : _______________  Date : __________
```
