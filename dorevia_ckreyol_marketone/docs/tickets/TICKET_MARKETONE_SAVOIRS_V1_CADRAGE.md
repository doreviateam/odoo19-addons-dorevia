# TICKET — Cadrage Savoirs v1 — Recettes contributives `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_SAVOIRS_V1_CADRAGE` |
| **Univers** | **Savoirs** — transmettre |
| **Type** | **Cadrage uniquement** — aucun code |
| **Statut** | **Ouvert** — en attente validation MOA |
| **Exécution** | *À créer après GO cadrage* — `TICKET_MARKETONE_SAVOIRS_V1_EXEC` (proposition) |
| **Version module de référence** | `19.0.9.0.0` |
| **Base** | `ckr-marketone-01` |
| **Arbitrage** | [`TICKET_MARKETONE_ARBITRAGE_PROCHAINE_ETAPE.md`](TICKET_MARKETONE_ARBITRAGE_PROCHAINE_ETAPE.md) — **GO** Option 2 (2026-05-18) |
| **Prérequis** | Boutique Lots 1–6.2 **GO** ; Culture v1 + v2 **GO MOA** ; consolidation portes **GO** ; **ADR-018**, **ADR-024** |
| **ADR** | ADR-018, ADR-024 — **ADR-028** (proposition à la clôture cadrage) |
| **Contrats** | **C9** (proposition) ; C7.4 ; C8 |
| **Note univers** | [`NOTE_UNIVERS_CK_MARKETONE.md`](../cadrage/NOTE_UNIVERS_CK_MARKETONE.md) §2.3, §7.3, §8 |

---

## Objectif

Cadrer le **premier lot Savoirs** — **recettes contributives** — pour compléter la doctrine des trois univers, **sans** code, **sans** exécution, **sans** ouvrir Culture v3 ni Lot 6.3 Boutique en parallèle.

```text
Critère attendu (cadrage validé) :
Le workflow « identifié → proposition → modération BO → publication » est tranché,
le conteneur technique et les liens Boutique / Culture sont définis,
les garde-fous (pas de forum, pas d’auto-publication) sont acceptés,
et un ticket d’exécution peut être rédigé — toujours sans implémenter dans ce ticket.
```

**Formule de référence** (NOTE univers) :

```text
Ceux qui savent transmettent à ceux qui découvrent.
```

**Ce ticket ne livre aucun** fichier Python, XML, SCSS, test, ni ticket d’exécution implémentable.

---

## Contexte — arbitrage MOA (2026-05-18)

| Décision | Détail |
|----------|--------|
| **GO arbitrage** | **Option 2** — Savoirs v1 cadrage recettes contributives |
| **Reporté** | Culture v3 (hub `/culture`, menu header) — 3 territoires suffisants pour l’instant |
| **Reporté** | Boutique 6.3 (Promotions / Collections / Kits) — gel ; risque densité legacy marketplace |

### Socle validé (ne pas refondre)

| Univers | État |
|---------|------|
| **Boutique** | `/shop`, Incontournables, Origines, fiche produit, panier, checkout — **stable**, 91 tests |
| **Culture** | `/culture/guadeloupe`, `martinique`, `reunion` — grammaire réplicable — **GO MOA** |
| **Savoirs** | **Non implémenté** — stub legacy `/recettes` ; `opt_recipes` newsletter |

---

## Contraintes MOA (non négociables)

| # | Contrainte |
|---|------------|
| S1 | **Savoirs hors `/shop`** — pas de mur recettes sur la grille boutique |
| S2 | **Retail-first** (C7.4) — CTA achat prioritaire sur fiche produit ; recettes en **prolongement** |
| S3 | **Pas de publication automatique** — proposition ≠ publication |
| S4 | **Utilisateur identifié** pour proposer (portal / compte) |
| S5 | **Modération BO obligatoire** avant mise en ligne |
| S6 | **Pas de forum**, commentaires libres, wiki ou UGC sans modération |
| S7 | **Pas de portage** `dorevia_ckreyol_marketplace` (lecture seule intuitions) |
| S8 | **Pas de code** dans ce ticket |
| S9 | **Pas** de Lot 6.3, Culture v3, Savoirs exec en parallèle de ce cadrage |
| S10 | **Pas de SEO recettes avancé** au premier cadrage |

**Agencement** (ADR-018 / ADR-024) :

```text
Le produit d'abord.
Le récit ensuite.
Le savoir en prolongement.
```

---

## Décisions à trancher (MOA + archi)

### D1 — Conteneur technique (premier lot exécution future)

| Option | Description | Pour | Contre |
|--------|-------------|------|--------|
| **A — Pages `website` + template Marketone** | Une page par recette publiée ; QWeb scoped `marketone-savoir` | Cohérent Culture v1 ; éditorial BO ; pas de module lourd | Gouvernance slug ; workflow état à modéliser ailleurs |
| B — `website.blog` + posts | Blog Odoo natif | Rapide à prototyper | Bruit navigation ; moins de contrôle workflow Marketone |
| C — Modèle dédié `marketone.savoir.recipe` (ou `marketone.knowledge.recipe`) | Champs structurés, états, liens M2M produit / origine | Workflow clair ; modération native | Risque scope ; tentation encyclopédie |
| D — Hybride C + pages website | Modèle minimal + page rendue | Séparation données / présentation | Deux couches à maintenir |

**Recommandation cadrage** : **C** (modèle dédié **minimal**) **ou** **A** si MOA refuse tout ORM au premier lot — dans ce cas workflow porté par `mail.activity` + pages website + statut CMS. **Rejeter B** comme conteneur principal (identité Marketone).

**Décision MOA** : ☐ A ☐ C ☐ D ☐ B ☐ autre : ___

---

### D2 — Workflow proposition → publication

Étapes cibles (à figer) :

```text
1. Contributeur identifié (portal)
2. Création brouillon recette (formulaire / BO selon rôle)
3. Soumission « en attente de modération »
4. Modérateur / éditeur BO : accepter | refuser | demander correction
5. Publication → visible site public
6. (Optionnel) Dépublier / archiver
```

| État proposé | Visible public | Qui agit |
|--------------|----------------|----------|
| `draft` | Non | Contributeur |
| `pending` | Non | Contributeur (submit) |
| `published` | Oui | Modérateur |
| `rejected` | Non | Modérateur |
| `archived` | Non | Éditeur |

**Règle** : aucune transition `draft` → `published` **sans** rôle modérateur.

**Décision MOA** : ☐ valider états ☐ ajuster : ___

---

### D3 — Qui peut proposer (contributeur)

| Option | Description |
|--------|-------------|
| **A — Utilisateur portal** (compte site) | Inscription / login portal ; groupe `marketone_savoir_contributor` |
| B — Abonné newsletter `opt_recipes` seulement | Trop faible pour v1 — pas d’identité garantie |
| C — Tout utilisateur interne BO seulement | Pas contributif public — **rejeté** pour Savoirs |

**Recommandation cadrage** : **A** — portal + groupe dédié.

**Décision MOA** : ☐ A ☐ autre : ___

---

### D4 — Rôles et permissions (BO)

| Rôle | Droits indicatifs |
|------|-------------------|
| **Contributeur** | Créer / éditer **ses** brouillons ; soumettre ; **pas** publier |
| **Modérateur** | Voir file d’attente `pending` ; publier ; refuser ; commenter interne |
| **Éditeur** | Tout modifier ; dépublier ; liens produit / origine |
| **Public** | Lecture recettes `published` uniquement |

**Décision MOA** : ☐ valider rôles ☐ fusion modérateur + éditeur : ___

---

### D5 — URL et découverte (premier lot)

| Option | Exemple | Note |
|--------|---------|------|
| **A — Préfixe Savoirs dédié** | `/savoirs/<slug-recette>`, `/savoirs/proposer` | Parallèle `/culture/<slug>` |
| B — `/recettes/<slug>` | Alignement legacy stub | Sémantique claire ; vérifier collision SEO |
| C — Blog path | `/blog/recettes/…` | Dépend D1=B — **déconseillé** |
| D — Sous `/shop` | — | **Rejeté** (S1) |

**Recommandation cadrage** : **A** ou **B** — MOA tranche une grammaire unique ; **pas** de liste recettes sur `/shop`.

| Entrée navigation v1 | Options |
|---------------------|---------|
| Menu header « Savoirs » | Reporté (comme Culture avant validation) |
| Lien fiche produit | **Oui** — 1 à 3 recettes liées |
| Lien page Culture | Optionnel — recette territoire |
| Hub `/savoirs` index | **Reporté** v1 exec (comme Culture v1 sans hub) |

**Décision MOA** : ☐ préfixe URL : ___ ☐ pas de hub v1 ☐ liens contextuels seulement

---

### D6 — Liens avec Boutique et Culture

| Lien | Obligation v1 | Règle |
|------|---------------|-------|
| **Produit** (`product.template`) | **Recommandé** — au moins 1 produit lié par recette publiée | CTA « Acheter » vers fiche ou panier |
| **Origine** (`marketone.shop.origin` / attribut) | Optionnel | Cohérence territoire |
| **Culture** (`/culture/<slug>`) | Optionnel | Lien « Découvrir le territoire » |
| **Grille `/shop`** | **Interdit** comme conteneur principal | S1 |

**Fiche produit** (prolongement C7.4) :

| Bloc | Comportement cible |
|------|-------------------|
| Section « Idées & recettes » | 0–3 recettes **publiées** liées ; **sous** CTA achat |
| Longueur | Titre + accroche courte — **pas** recette complète inline |

**Décision MOA** : ☐ produit obligatoire ☐ produit optionnel ☐ lien Culture optionnel

---

### D7 — Contenu minimal d’une recette (v1)

| Champ / bloc | Autorisé v1 | Interdit v1 |
|--------------|-------------|-------------|
| Titre | ☑ | |
| Accroche (1–2 phrases) | ☑ | |
| Ingrédients (liste courte) | ☑ | Base nutritionnelle complète |
| Étapes (liste numérotée courte) | ☑ | Vidéo longue embarquée |
| Photo principale | ☑ optionnel | Galerie |
| Temps / portions | ☑ optionnel | |
| Auteur / contributeur (affichage) | ☑ | Profil social complet |
| Produits liés | ☑ | Catalogue embarqué |
| Commentaires publics | | ☑ |
| Notation / likes | | ☑ |

**Décision MOA** : ☐ valider plafond éditorial ☐ ajuster : ___

---

### D8 — Modération et conformité

| Sujet | Proposition |
|-------|-------------|
| File modération | Menu BO dédié — recettes `pending` |
| Motif refus | Champ texte interne ; notification contributeur (phase 2 ?) |
| RGPD / contenu | Pas de données sensibles ; charte contributeur (doc) |
| Spam | Captcha ou limite débit proposition (exec) |

**Décision MOA** : ☐ valider ☐ report notifications contributeur

---

### D9 — SEO et indexation

| Sujet | Options |
|-------|---------|
| Recettes publiées | Indexables ou `noindex` jusqu’à maturité ? |
| Cannibalisation `/shop` | Pages Savoirs distinctes ; pas de duplicate produit |

**Décision MOA** : ☑ **Documentation seulement** — pas de chantier SEO avancé v1 (aligné Culture).

---

### D10 — Périmètre premier lot exécution (indicatif post-cadrage)

| Inclus v1 exec (proposition) | Exclu v1 |
|----------------------------|----------|
| Formulaire proposition (portal) | Forum |
| File modération BO | Commentaires |
| 1 page recette publiée type | Hub `/savoirs` index |
| Lien fiche produit (recettes liées) | Menu header Savoirs |
| Tests tag `dorevia_marketone_savoirs_v1` | SEO avancé |
| | Traduction multilingue lourde |

**Décision MOA** : ☐ valider périmètre exec indicatif ☐ ajuster : ___

---

## Référence legacy (lecture seule)

| Intuition utile | Source legacy | Reprise Marketone |
|-----------------|---------------|-------------------|
| Page `/recettes` stub | `ckr_recettes.xml` | **Non** copier stub — vrai workflow |
| Menu Recettes | header legacy | Reporté navigation v1 |
| `opt_recipes` | `ckr_circle_subscriber` | Inspiration audience — pas seul critère contributeur |
| Inspiration 750g | ADR-019 | Structure ingrédients / étapes — densité maîtrisée |
| Bloc recettes fiche | — | À **créer** Marketone — prolongement produit |

**Interdit** : portage `ckr_*` models, forum legacy, publication sans modération.

---

## Garde-fous

| # | Garde-fou |
|---|-----------|
| G1 | Aucun contenu Savoirs principal sur `/shop` |
| G2 | Fiche produit : CTA achat **au-dessus** des recettes |
| G3 | Publication uniquement après modération BO |
| G4 | Pas de forum ni UGC libre |
| G5 | Pas de code sans ticket exec **GO** |
| G6 | Non-régression **91** tests existants |
| G7 | Une orientation : pas 6.3 + Culture v3 + Savoirs exec en parallèle |
| G8 | Modèle recette **minimal** — pas d’encyclopédie |

---

## Hors périmètre (explicite)

| Exclusion | Report |
|-----------|--------|
| Code, maquettes implémentées | Ticket exec post-GO cadrage |
| Culture v3, Lot 6.3 | Arbitrage MOA — report |
| Forum, wiki, commentaires | Interdit |
| Portage marketplace | Interdit |
| Newsletter / CRM recettes avancé | Backlog |
| Vidéo, live, UGC social | Backlog |

---

## Livrables cadrage (attendus)

| # | Livrable | Statut |
|---|----------|--------|
| L1 | Décisions D1–D10 tranchées MOA | ☐ |
| L2 | Workflow états validé | ☐ |
| L3 | Conteneur technique (D1) | ☐ |
| L4 | Contrat **C9** dans `CONTRACTS.md` | ☐ |
| L5 | **ADR-028** dans `DECISIONS.md` | ☐ |
| L6 | Ticket exec `TICKET_MARKETONE_SAVOIRS_V1_EXEC` | ☐ après GO cadrage |
| L7 | Esquisse recette manuelle (dans exec) | ☐ |

---

## Critères GO cadrage

- [ ] Workflow identifié → modération → publication **figé**
- [ ] Conteneur technique (D1) tranché — **pas** de blog seul comme solution finale sans justification
- [ ] Rôles contributeur / modérateur **clairs**
- [ ] Liens produit (et optionnel origine / Culture) **explicités**
- [ ] Garde-fous S1–S10 et G1–G8 **acceptés**
- [ ] Pas de parallèle 6.3 / Culture v3 / exec Savoirs
- [ ] Ticket exec rédigé (après GO)
- [ ] Hors périmètre accepté

---

## Décision de sortie (MOA)

```text
[ ] GO cadrage Savoirs v1
[ ] GO cadrage avec réserves légères
[ ] NO GO — reporter ou reformuler
```

**Date** : ___ · **Validé par** : ___

### Réserves proposées (à confirmer)

| # | Réserve |
|---|---------|
| R1 | Recette **courte** — pas de blog culinaire exhaustif |
| R2 | **Pas** de Savoirs dans `/shop` |
| R3 | Modération **humaine** obligatoire v1 |
| R4 | **Pas** d’ouverture 6.3 en parallèle |

---

## Prochaine étape

1. **MOA** : trancher D1–D10 et valider ce cadrage.
2. **Rédiger** `TICKET_MARKETONE_SAVOIRS_V1_EXEC` — **sans code** avant GO exec.
3. **Ne pas** implémenter tant que l’exécution n’est pas **GO**.

---

## Références

| Document | Rôle |
|----------|------|
| [`TICKET_MARKETONE_ARBITRAGE_PROCHAINE_ETAPE.md`](TICKET_MARKETONE_ARBITRAGE_PROCHAINE_ETAPE.md) | GO Option 2 |
| [`NOTE_UNIVERS_CK_MARKETONE.md`](../cadrage/NOTE_UNIVERS_CK_MARKETONE.md) | §2.3 Savoirs, §7.3 |
| [`cadrage/DECISIONS.md`](../cadrage/DECISIONS.md) | ADR-018, ADR-024 |
| [`cadrage/CONTRACTS.md`](../cadrage/CONTRACTS.md) | C7.4, C8 |
| [`TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_EXEC.md`](TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_EXEC.md) | Culture — GO MOA |
| [`pilotage/ROADMAP.md`](../pilotage/ROADMAP.md) | Planning |
