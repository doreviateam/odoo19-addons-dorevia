# TICKET — Arbitrage prochaine étape Marketone `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_ARBITRAGE_PROCHAINE_ETAPE` |
| **Type** | **Cadrage / arbitrage produit** — aucun code |
| **Statut** | **Ouvert** — en attente décision MOA |
| **Version module actuelle** | `19.0.9.0.0` |
| **Base** | `ckr-marketone-01` |
| **ADR** | ADR-018, ADR-024, ADR-026, ADR-027 |
| **Note univers** | [`NOTE_UNIVERS_CK_MARKETONE.md`](../cadrage/NOTE_UNIVERS_CK_MARKETONE.md) |
| **Roadmap** | [`ROADMAP.md`](../pilotage/ROADMAP.md) |

---

## Objectif

Après clôture **Culture v2 légère** (GO MOA), **choisir une seule prochaine orientation** avant tout nouveau code — pause d’architecture produit, pas empilement de portes ou d’univers en parallèle.

```text
Critère de sortie :
MOA tranche une option prioritaire (ou report explicite),
avec périmètre, risques et ticket de cadrage / exec suivant identifié.
```

**Ce ticket ne livre aucun** fichier Python, XML, SCSS, test, ni implémentation.

---

## État actuel validé (2026-05-18)

```text
Marketone 19.0.9.0.0
Tests : 91 post-tests, 0 failed

Boutique (GO — socle stable)
  /shop
  /incontournables  → marketone_mode=featured
  /origines         → marketone_mode=origin (+ facette marketone_origin)
  fiche produit, panier, checkout

Culture (GO MOA)
  /culture/guadeloupe
  /culture/martinique
  /culture/reunion
  — pas de hub /culture
  — pas de menu header Culture
  — grammaire réplicable (v1 + v2 légère)

Savoirs
  — à cadrer (univers annoncé, non implémenté)
```

| Jalon récent | Statut |
|--------------|--------|
| Consolidation portes Boutique | **GO** |
| Culture v1 (`guadeloupe`) | **GO MOA** `19.0.8.0.0` |
| Culture v2 légère (`martinique`, `reunion`) | **GO MOA** `19.0.9.0.0` |
| Lot 6.3 Boutique (Promotions, Kits, Collections) | **Gel MOA** |

**Doctrine** (ADR-018 / ADR-024) :

```text
Le produit d'abord.
Le récit ensuite.
Le savoir en prolongement.
```

---

## Contraintes MOA (arbitrage)

| # | Contrainte |
|---|------------|
| A1 | **Une** orientation prioritaire — pas deux lots d’exécution en parallèle |
| A2 | **Pas de code** dans ce ticket |
| A3 | Respecter les garde-fous univers (NOTE §8) — retail-first, modération Savoirs, pas de forum |
| A4 | Lot 6.3 : **une porte à la fois** si Boutique retenue (Collections **ou** Promotions, pas les deux) |
| A5 | Culture v3 : **pas** de retour encyclopédique ni hub massif sans cadrage dédié |
| A6 | Savoirs v1 : **cadrage** workflow identifié → proposition → validation BO → publication |
| A7 | Non-régression : **91** tests et socle Boutique / Culture actuels inchangés |

---

## Options à comparer

### Option 1 — Culture v3 (hub léger + navigation)

| | |
|---|---|
| **Intention** | Rendre les **3 territoires** découvrables sans repasser par la Boutique ; hub `/culture` **léger** ; éventuelle entrée header « Découvrir » |
| **Univers** | Culture |
| **Livrables indicatifs** | Page index `/culture` (liste courte 3 territoires, pas encyclopédie) ; lien header optionnel ; ADR-028 ; ticket exec |
| **Pour** | Complète le parcours Culture après v2 ; UX découverte territoires ; cohérent avec 3 slugs actifs |
| **Contre** | Risque **mini-portail** ou pression contenu ; navigation globale à valider visuellement ; peut précéder Savoirs alors que le 3ᵉ univers reste vide |
| **Risques** | Hub déguisé type legacy Explorer ; SEO / indexation ; confusion Boutique / Culture |
| **Effort estimé** | Moyen (routing + QWeb + gouvernance éditoriale) |
| **Prérequis** | Culture v1 + v2 **GO** ✅ |

**Questions MOA** :

- Le hub liste-t-il **uniquement** les territoires publiés (3 lignes max.) ?
- L’entrée header est-elle **obligatoire** ou optionnelle en v3 ?
- Faut-il un **4ᵉ territoire** avant le hub ?

---

### Option 2 — Savoirs v1 (cadrage recettes contributives) ⭐ recommandation MOA

| | |
|---|---|
| **Intention** | Cadrer le **3ᵉ univers** : recettes / usages en **prolongement** Boutique — utilisateur **identifié** → proposition → **validation BO** → publication |
| **Univers** | Savoirs |
| **Livrables indicatifs** | Ticket cadrage `TICKET_MARKETONE_SAVOIRS_V1_CADRAGE` ; workflow ; modèle contenu (website vs module dédié) ; liens fiche produit ; **pas** d’implémentation dans ce lot |
| **Pour** | Équilibre **Boutique + Culture** déjà solide ; Savoirs = différenciation métier C-Kreyol ; évite d’empiler une porte commerce (6.3) avant la doctrine complète ; aligné NOTE §7.3 et ADR-018 |
| **Contre** | Pas de livrable visible court terme (cadrage seul) ; complexité gouvernance / modération à trancher |
| **Risques** | Scope creep (forum, UGC, blog massif) ; cannibalisation SEO sur `/shop` ; dépendance legacy marketplace |
| **Effort estimé** | **Cadrage** : 1 ticket MOA ; **Exec** ultérieure : élevé |
| **Prérequis** | Socle identité / portal ✅ ; inspiration 750g en lecture seule |

**Périmètre v1 cadrage (proposition)** :

| Inclus cadrage | Exclu |
|----------------|-------|
| Workflow proposition → modération → publication | Forum, commentaires libres |
| Lien discret fiche produit → 1–3 recettes | Publication automatique sans BO |
| URL / modèle de contenu (hypothèses) | SEO recettes avancé |
| Rôles (contributeur, modérateur) | Lot 6.3 en parallèle |

**Questions MOA** :

- Conteneur : `website.blog`, pages `website`, ou modèle `marketone.savoir.recipe` ?
- Qui peut proposer (portal user, signup, cercle abonnés) ?
- Lien obligatoire produit / origine / territoire Culture ?

---

### Option 3 — Boutique 6.3 (une nouvelle porte catalogue)

| | |
|---|---|
| **Intention** | Ajouter **une** porte `marketone_mode=…` : **Collections** **ou** **Promotions** (MOA choisit **une** seule) |
| **Univers** | Boutique |
| **Livrables indicatifs** | Cadrage porte 6.3 ; ticket exec ; filtre catalogue ; bandeau `/shop` ; tests ; alias 301 optionnel |
| **Pour** | Enrichit le parcours achat ; MOA connaît le pattern 6.1 / 6.2 ; valeur commerce directe |
| **Contre** | **3ᵉ univers Savoirs** toujours absent ; risque « encore une porte » alors que Culture vient de stabiliser 3 territoires ; gel MOA explicite sur 6.3 |
| **Risques** | Cumul modes ; dette portes ; confusion avec legacy `/kits`, `/promotions` |
| **Effort estimé** | Moyen–élevé (même gabarit 6.1 / 6.2) |
| **Prérequis** | Consolidation portes **GO** ✅ |

**Sous-options (une seule retenue)** :

| Porte | Indication |
|-------|------------|
| **6.3.A Collections** | Rubriques éditoriales achetables — modèle `marketone.shop.collection` (décision en attente DECISIONS.md) |
| **6.3.B Promotions** | Offres / prix — dépendances pricing, risque complexité |

**Questions MOA** :

- Collections **ou** Promotions en premier ?
- Lien avec Culture (porte collection liée territoire) — oui / non / plus tard ?

---

## Matrice de comparaison (synthèse)

| Critère | Culture v3 | Savoirs v1 cadrage ⭐ | Boutique 6.3 |
|---------|------------|----------------------|--------------|
| Complète la doctrine 3 univers | Partiel (Culture seulement) | **Oui** (3ᵉ univers) | Partiel (Boutique) |
| Livrable visible court terme | Oui (pages) | Non (cadrage) | Oui (porte shop) |
| Risque scope creep | Moyen (hub) | Élevé si mal cadré | Moyen |
| Charge dev immédiate | Moyenne | **Nulle** (cadrage) | Moyenne–élevée |
| Alignement « pause architecture » | Moyen | **Fort** | Faible |
| Cohérence post Culture v2 | Bonne | **Très bonne** | Moins prioritaire |

---

## Recommandation rédaction ticket (non contraignante)

**Préférence MOA exprimée** : **Option 2 — Savoirs v1 en cadrage uniquement**.

**Motifs** :

1. Boutique + Culture sont **stables** et testés (91 tests).
2. Le troisième univers mérite une **doctrine et un workflow** avant tout code.
3. Reporter Culture v3 évite un hub prématuré avec seulement 3 territoires.
4. Reporter 6.3 respecte le **gel MOA** et la règle **une porte à la fois**.

**Si MOA choisit autrement** : documenter la décision et le ticket enfant dans ce ticket (section Décision de sortie).

---

## Décision de sortie (MOA)

```text
[ ] Option 1 — Culture v3 (hub léger + navigation)
[ ] Option 2 — Savoirs v1 — cadrage recettes contributives  ⭐ recommandé
[ ] Option 3 — Boutique 6.3 — préciser : Collections [ ] / Promotions [ ]
[ ] Report / autre : ___
```

**Date** : ___ · **Validé par** : ___

### Ticket enfant à ouvrir (après arbitrage)

| Option retenue | Ticket suivant (proposition) |
|----------------|------------------------------|
| Culture v3 | `TICKET_MARKETONE_CULTURE_V3_HUB_CADRAGE` |
| Savoirs v1 | `TICKET_MARKETONE_SAVOIRS_V1_CADRAGE` |
| Boutique 6.3 | `TICKET_MARKETONE_LOT6_3_PORTE_*_CADRAGE` |

---

## Hors périmètre (ce ticket)

| Exclusion | Raison |
|-----------|--------|
| Implémentation quelconque | Arbitrage seulement |
| Lot 6.3 **et** Savoirs **et** Culture v3 en parallèle | Contrainte A1 |
| Refonte home / Explorer legacy | Ticket séparé |
| Portage `dorevia_ckreyol_marketplace` | Interdit |
| SEO avancé cross-univers | Report |

---

## Prochaine étape

1. **MOA** : trancher une option (ou report motivé).
2. **Rédiger** le ticket de cadrage enfant correspondant — **sans code**.
3. **Ne pas** ouvrir d’exécution tant que le cadrage enfant n’est pas **GO**.

---

## Références

| Document | Rôle |
|----------|------|
| [`NOTE_UNIVERS_CK_MARKETONE.md`](../cadrage/NOTE_UNIVERS_CK_MARKETONE.md) §7–8 | Backlog univers |
| [`TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_EXEC.md`](TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_EXEC.md) | Dernier GO Culture |
| [`TICKET_MARKETONE_CONSOLIDATION_PORTES_BOUTIQUE.md`](TICKET_MARKETONE_CONSOLIDATION_PORTES_BOUTIQUE.md) | Grammaire Boutique |
| [`cadrage/DECISIONS.md`](../cadrage/DECISIONS.md) | ADR-018, ADR-024, ADR-026, ADR-027 |
| [`cadrage/CONTRACTS.md`](../cadrage/CONTRACTS.md) | Contrats portes et Culture |
