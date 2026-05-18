# TICKET — Cadrage Savoirs v1 — Recettes contributives `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_SAVOIRS_V1_CADRAGE` |
| **Univers** | **Savoirs** — transmettre |
| **Type** | **Cadrage uniquement** — aucun code |
| **Statut** | **Clôturé — GO cadrage avec réserves légères** (2026-05-18) |
| **Exécution** | [`TICKET_MARKETONE_SAVOIRS_V1_EXEC.md`](TICKET_MARKETONE_SAVOIRS_V1_EXEC.md) — **ouvert**, en attente GO MOA |
| **Version module de référence** | `19.0.9.0.0` |
| **Version cible exécution** | `19.0.10.0.0` (proposition) |
| **Arbitrage** | [`TICKET_MARKETONE_ARBITRAGE_PROCHAINE_ETAPE.md`](TICKET_MARKETONE_ARBITRAGE_PROCHAINE_ETAPE.md) — **GO** Option 2 |
| **ADR** | ADR-018, ADR-024, **ADR-028** |
| **Contrats** | **C9** |

---

## Objectif

Cadrer le premier lot **Savoirs** — recettes contributives — workflow, conteneur, liens Boutique/Culture, garde-fous. **Aucun code** dans ce ticket.

---

## Décisions MOA figées (2026-05-18)

| # | Décision |
|---|----------|
| **D1** | Modèle minimal **`marketone.savoir.recipe`** — pas `website_blog` ; pas pages website seules pour le workflow |
| **D2** | États `draft`, `pending`, `published`, `rejected`, `archived` — pas de `draft → published` sans modérateur |
| **D3** | Contributeur : portal + groupe dédié |
| **D4** | Rôles contributeur, modérateur, éditeur, public — fusion modérateur/éditeur **technique v1** possible |
| **D5** | `/savoirs/<slug-recette>`, `/savoirs/proposer` — **pas** de hub `/savoirs` v1 |
| **D6** | Produit lié **obligatoire** si publié ; origine / Culture optionnels ; bloc fiche « Idées & recettes » 0–3, **sous** CTA achat |
| **D7** | Titre, accroche, ingrédients, étapes, photo/temps/portions optionnels, auteur, produits — pas commentaires/likes/galerie/vidéo/nutrition/inline fiche |
| **D8** | File `pending` ; publier / refuser / archiver / modifier ; motif refus interne ; pas notification v1 |
| **D9** | SEO documentation seulement |
| **D10** | Exec indicatif : modèle, portal, modération BO, page publiée, lien fiche, tests `dorevia_marketone_savoirs_v1` |

### Réserves MOA

| # | Réserve |
|---|---------|
| R1 | Modèle **minimal** |
| R2 | Pas de hub `/savoirs` v1 |
| R3 | Pas de commentaires publics |
| R4 | Pas de publication automatique |
| R5 | Bloc recette **sous** CTA achat |
| R6 | Pas de 6.3 / Culture v3 en parallèle |

---

## Livrables cadrage

| # | Livrable | Statut |
|---|----------|--------|
| L1 | Décisions D1–D10 | ✅ |
| L2 | Workflow | ✅ |
| L3 | Conteneur D1 | ✅ |
| L4 | Contrat **C9** | ✅ |
| L5 | **ADR-028** | ✅ |
| L6 | Ticket exec | ✅ ouvert |
| L7 | Recette manuelle | ☐ au ticket exec |

---

## Décision de sortie (MOA)

```text
[ ] GO cadrage Savoirs v1
[x] GO cadrage avec réserves légères
[ ] NO GO
```

**Date** : 2026-05-18 · **Validé par** : MOA

---

## Prochaine étape

1. **MOA** : valider [`TICKET_MARKETONE_SAVOIRS_V1_EXEC.md`](TICKET_MARKETONE_SAVOIRS_V1_EXEC.md).
2. **Pas de code** avant GO exécution.

---

## Références

| Document | Rôle |
|----------|------|
| [`TICKET_MARKETONE_SAVOIRS_V1_EXEC.md`](TICKET_MARKETONE_SAVOIRS_V1_EXEC.md) | Exécution |
| [`NOTE_UNIVERS_CK_MARKETONE.md`](../cadrage/NOTE_UNIVERS_CK_MARKETONE.md) | §2.3, §7.3 |
| [`cadrage/DECISIONS.md`](../cadrage/DECISIONS.md) — ADR-028 | |
| [`cadrage/CONTRACTS.md`](../cadrage/CONTRACTS.md) — C9 | |
