# TICKET — Exécution Savoirs v1 — Recettes contributives `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_SAVOIRS_V1_EXEC` |
| **Univers** | **Savoirs** — transmettre |
| **Lot** | Savoirs v1 — recettes contributives (premier lot) |
| **Statut** | **Ouvert** — en attente validation MOA pour exécution |
| **Version cible module** | `19.0.10.0.0` (proposition) |
| **Base** | `ckr-marketone-01` |
| **Prérequis** | Cadrage **GO avec réserves légères** — [`TICKET_MARKETONE_SAVOIRS_V1_CADRAGE.md`](TICKET_MARKETONE_SAVOIRS_V1_CADRAGE.md) ; arbitrage **GO** Option 2 ; Culture v1+v2 **GO MOA** ; Boutique 6.1/6.2 **GO** ; **ADR-018**, **ADR-024**, **ADR-028** |
| **ADR** | ADR-018, ADR-024, ADR-028 |
| **Contrats** | **C9** ; C7.4 ; C8 ; non-régression C3.A / C3.B |
| **Recette** | `docs/recette/RECETTE_MANUELLE_SAVOIRS_V1.md` (à créer à l’exécution) |

---

## Objectif

Livrer le **premier lot Savoirs** : recettes **contributives** avec workflow **identifié → proposition → modération BO → publication**, **hors** `/shop`, en **prolongement** de la fiche produit — **sans** forum, hub `/savoirs`, ni parallèle Culture v3 / Lot 6.3.

```text
Critère GO Savoirs v1 :
Un contributeur portal soumet une recette (pending),
un modérateur la publie,
le public la lit sur /savoirs/<slug>,
et la fiche produit liée affiche 1–3 recettes sous le CTA achat —
sans régression des 91 tests existants.
```

**Aucun code** tant que ce ticket d’exécution n’est pas validé MOA.

---

## Décisions MOA figées (cadrage 2026-05-18)

| # | Décision |
|---|----------|
| **D1** | Modèle minimal **`marketone.savoir.recipe`** — **pas** `website_blog` ; **pas** pages website seules pour le workflow |
| **D2** | États : `draft`, `pending`, `published`, `rejected`, `archived` — **`draft → published` interdit** sans modérateur |
| **D3** | Contributeur : utilisateur **portal** + groupe dédié |
| **D4** | Rôles : contributeur, modérateur, éditeur, public — fusion modérateur/éditeur **technique v1** possible si doctrine distincte documentée |
| **D5** | URLs : `/savoirs/<slug-recette>`, `/savoirs/proposer` — **pas** de hub `/savoirs` v1 |
| **D6** | Produit lié **obligatoire** si publié ; origine / Culture **optionnels** ; bloc fiche **« Idées & recettes »** 0–3 recettes **sous** CTA achat |
| **D7** | Contenu minimal : titre, accroche, ingrédients, étapes, photo/temps/portions optionnels, auteur, produits liés |
| **D8** | File BO `pending` ; publier / refuser / archiver / modifier ; motif refus interne ; **pas** notification contributeur v1 |
| **D9** | SEO : documentation seulement |
| **D10** | Voir périmètre exécution § ci-dessous |

### Réserves MOA

| # | Réserve |
|---|---------|
| R1 | Modèle recette **minimal** |
| R2 | **Pas** de hub `/savoirs` v1 |
| R3 | **Pas** de commentaires publics |
| R4 | **Pas** de publication automatique |
| R5 | Recettes fiche produit **sous** CTA achat |
| R6 | **Pas** de Lot 6.3 ni Culture v3 en parallèle |

---

## Périmètre inclus (exécution)

### 1. Modèle `marketone.savoir.recipe` (minimal)

| Élément | Règle |
|---------|--------|
| Champs | Titre, slug, accroche, ingrédients (texte/HTML court), étapes, image optionnelle, temps/portions optionnels, état, auteur (`res.users`), produits M2M **obligatoire** si `published`, origine / lien Culture optionnels |
| États | Selection : `draft`, `pending`, `published`, `rejected`, `archived` |
| Contraintes | Transition vers `published` réservée modérateur/éditeur |
| **Interdit** | Commentaires, likes, nutrition avancée, champs encyclopédiques |

### 2. Sécurité et rôles

| Groupe | Droits indicatifs |
|--------|-------------------|
| `marketone_savoir_contributor` | CRUD **ses** brouillons ; submit → `pending` |
| `marketone_savoir_moderator` (+ éditeur si fusion) | File `pending` ; publish / reject / archive ; edit any |
| Public | Lecture `published` via site uniquement |

### 3. Routes HTTP

| Route | Rôle |
|-------|------|
| `GET /savoirs/<slug>` | Page recette publiée — template `.marketone-savoir` |
| `GET/POST /savoirs/proposer` | Formulaire portal contributeur |
| `GET /savoirs` | **404** ou redirect documenté — **pas** de hub index v1 |

### 4. Présentation front

| Livrable | Détail |
|----------|--------|
| Template recette | QWeb scoped `.marketone-savoir` |
| SCSS | `_savoirs.scss` scoped |
| Fiche produit | Extension : bloc **Idées & recettes** (0–3 liens) **après** CTA achat |
| **Interdit** | Recette complète inline sur fiche ; grille recettes sur `/shop` |

### 5. Back-office

| Livrable | Détail |
|----------|--------|
| Vues | Liste / formulaire `marketone.savoir.recipe` |
| File modération | Filtre `pending` ; actions publier / refuser / archiver |
| Motif refus | Champ texte interne (pas de mail auto v1) |

### 6. Tests

| Fichier | Tag |
|---------|-----|
| `tests/test_marketone_savoirs_v1.py` | `dorevia_marketone_savoirs_v1` |

**Scénarios minimum** :

| # | Test |
|---|------|
| T1 | Workflow : contributeur crée `pending` ; modérateur `published` |
| T2 | `draft → published` direct **refusé** pour contributeur |
| T3 | `GET /savoirs/<slug>` **200** si `published` |
| T4 | Recette non publiée → **404** public |
| T5 | Fiche produit : bloc recettes **sous** zone achat ; liens `/savoirs/…` |
| T6 | `GET /savoirs` → **pas** de hub (404 ou redirect documenté) |
| T7 | Non-régression Culture + Boutique (suite **91+** tests) |

### 7. Documentation

| Livrable | Fichier |
|----------|---------|
| Recette MOA | `RECETTE_MANUELLE_SAVOIRS_V1.md` |
| `ENV_REFERENCE` | Routes, groupes, tag tests |
| ADR-028 | Déjà dans `DECISIONS.md` (cadrage) |

### 8. Version

`__manifest__.py` → **`19.0.10.0.0`**

---

## Fichiers indicatifs (exécution)

```text
models/marketone_savoir_recipe.py
security/marketone_savoir_security.xml
security/ir.model.access.csv
controllers/savoirs.py
views/marketone_savoir_recipe_views.xml
views/pages/savoir_recipe.xml
views/pages/savoir_propose.xml
views/pages/product_savoirs.xml          # extension fiche produit
static/src/scss/_savoirs.scss
tests/test_marketone_savoirs_v1.py
__manifest__.py                            # 19.0.10.0.0
```

---

## Hors périmètre (explicite)

| Exclusion | Report |
|-----------|--------|
| Hub `/savoirs` index | Savoirs v2 |
| Menu header Savoirs | v2 |
| Commentaires, likes, forum | Interdit |
| Notification email contributeur | v2 |
| `website_blog` comme conteneur | Interdit (D1) |
| Culture v3, Lot 6.3 | Arbitrage — report |
| SEO avancé | Documentation |
| Portage marketplace | Interdit |
| Vidéo, galerie, nutrition | Backlog |

---

## Critères GO / NO GO exécution

### GO

- [ ] Modèle minimal + états workflow conformes D2
- [ ] Portal proposition + file modération BO
- [ ] `/savoirs/<slug>` public si `published` ; `/savoirs/proposer` pour contributeur
- [ ] **Pas** de hub `/savoirs`
- [ ] Fiche produit : 0–3 recettes **sous** CTA ; produit obligatoire si publié
- [ ] Tag `dorevia_marketone_savoirs_v1` + **91+** tests **0** failed
- [ ] Recette MOA validée
- [ ] Mobile 375 px OK (recette)

### NO GO

- [ ] Publication sans modération
- [ ] Recettes au-dessus du CTA achat
- [ ] Hub ou commentaires publics
- [ ] Régression Boutique / Culture

---

## Checklist validation MOA (exécution)

```text
[x] Cadrage Savoirs v1 GO avec réserves légères
[x] D1–D10 figées
[ ] GO pour implémentation  [ ] En attente  [ ] NO GO
```

---

## Prochaine étape

1. **MOA** : valider ce ticket d’**exécution**.
2. **Dev** : implémentation `19.0.10.0.0` **après** GO exec uniquement.
3. **Ne pas** ouvrir Culture v3, 6.3, en parallèle.

---

## Références

| Document | Rôle |
|----------|------|
| [`TICKET_MARKETONE_SAVOIRS_V1_CADRAGE.md`](TICKET_MARKETONE_SAVOIRS_V1_CADRAGE.md) | Cadrage — **clôturé GO** |
| [`TICKET_MARKETONE_ARBITRAGE_PROCHAINE_ETAPE.md`](TICKET_MARKETONE_ARBITRAGE_PROCHAINE_ETAPE.md) | GO Option 2 |
| [`cadrage/DECISIONS.md`](../cadrage/DECISIONS.md) — ADR-028 | Savoirs v1 |
| [`cadrage/CONTRACTS.md`](../cadrage/CONTRACTS.md) — C9 | Contrat Savoirs |
