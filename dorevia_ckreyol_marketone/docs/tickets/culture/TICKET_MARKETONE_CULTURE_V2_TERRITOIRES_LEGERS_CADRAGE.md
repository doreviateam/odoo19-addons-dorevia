# TICKET — Cadrage Culture v2 légère — Territoires additionnels `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_CADRAGE` |
| **Univers** | **Culture** — découvrir |
| **Type** | **Cadrage uniquement** — aucun code |
| **Statut** | **Clôturé — GO cadrage avec réserves** (2026-05-18) |
| **Exécution** | [`TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_EXEC.md`](./TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_EXEC.md) — **clôturé GO MOA** `19.0.9.0.0` |
| **Version module de référence** | `19.0.8.0.0` (Culture v1 **GO MOA**) |
| **Version cible exécution** | `19.0.9.0.0` (proposition) |
| **Base** | `ckr-marketone-01` |
| **Prérequis** | Culture v1 **GO MOA** — [`TICKET_MARKETONE_CULTURE_TERRITOIRES_EXEC.md`](./TICKET_MARKETONE_CULTURE_TERRITOIRES_EXEC.md) (`19.0.8.0.0`) ; cadrage v1 — [`TICKET_MARKETONE_CULTURE_TERRITOIRES_CADRAGE.md`](./TICKET_MARKETONE_CULTURE_TERRITOIRES_CADRAGE.md) ; portes Boutique 6.1 / 6.2 **GO** ; consolidation portes **GO** ; **ADR-024**, **ADR-026**, **ADR-027**, contrat **C8** |
| **ADR** | ADR-024, ADR-026, **ADR-027** |
| **Contrats** | C8 (v2) ; C7.4 ; non-régression C3.A / C3.B |
| **Recette v1** | [`RECETTE_MANUELLE_CULTURE_V1.md`](../../recette/culture/RECETTE_MANUELLE_CULTURE_V1.md) |
| **Roadmap** | [`ROADMAP.md`](../../pilotage/ROADMAP.md) |

---

## Objectif produit

Vérifier que le format Culture **`/culture/<slug>`** n’est **pas** une page isolée (pilote Guadeloupe), mais une **grammaire éditoriale réplicable** sur **deux territoires supplémentaires**, sans ouvrir un portail Culture massif.

```text
Critère attendu (cadrage validé) :
Un visiteur atteint /culture/martinique et /culture/reunion,
retrouve la même structure sobre que le pilote guadeloupe,
et peut acheter via la porte Origines filtrée — sans hub /culture,
sans menu header Culture, sans régression du socle Boutique.
```

**Ce ticket ne livre aucun** fichier Python, XML, SCSS, test, ni ticket d’exécution exécutable.

---

## Décisions MOA figées (2026-05-18)

| # | Décision |
|---|----------|
| **D1** | **+2 territoires** : slugs **`martinique`**, **`reunion`** — sous réserve profils BO ; ajustement avant exec si écart |
| **D2** | **Option A** : aucun code fonctionnel nouveau si infra v1 couvre slugs publiés — BO + recette (+ tests) |
| **D3** | Sections **génériques** ; varient `name_visitor`, `context_phrase`, slug, CTA |
| **D4** | **Pas** d’image par territoire v2 |
| **D5** | **Aucun** lien croisé entre territoires |
| **D6** | Menu header Culture **reporté** |
| **D7** | SEO : documentation seulement |
| **D8** | Tag `dorevia_marketone_culture_v2` — HTTP slugs v2 + liens Boutique + non-régression v1 et Boutique |

### Réserves MOA

| # | Réserve |
|---|---------|
| R1 | Slugs `martinique` / `reunion` sous réserve profils BO |
| R2 | Pas de champs éditoriaux longs |
| R3 | Pas de hub `/culture` |
| R4 | Pas de menu header Culture |
| R5 | Pas de Lot 6.3 ni Savoirs en parallèle |

---

## Contexte — décision MOA de suite

| Décision | Détail |
|----------|--------|
| **Ne pas ouvrir Lot 6.3 Boutique** | Socle Boutique **stable** |
| **Prochaine étape** | Culture v2 légère — territoires additionnels |

---

## Contexte — Culture v1 (référence)

Route `GET /culture/<slug>`, template `.marketone-culture`, liens Boutique contextuels, pilote **`guadeloupe`** — **GO MOA** `19.0.8.0.0`. L’infra v1 résout **tout slug** publié sur `marketone.shop.origin`.

---

## Périmètre v2 légère (résumé)

| Inclus | Exclu |
|--------|-------|
| `/culture/martinique`, `/culture/reunion` | Hub `/culture` |
| Format identique v1 | Menu header Culture |
| CTA porte Origines | Modèle Culture lourd |
| Liens contextuels (déjà génériques) | Lot 6.3, Savoirs |

---

## Garde-fous

| # | Garde-fou |
|---|-----------|
| G1–G8 | Reprise v1 — voir ticket exec v2 |

---

## Livrables cadrage

| # | Livrable | Statut |
|---|----------|--------|
| L1 | Décisions D1–D8 | ✅ |
| L2 | Slugs `martinique`, `reunion` | ✅ (réserve BO) |
| L3 | Delta technique D2 = A | ✅ |
| L4 | Contrat C8 v2 | ✅ |
| L5 | ADR-027 | ✅ |
| L6 | Ticket exec | ✅ ouvert |
| L7 | Recette v2 | ☐ au ticket exec |

---

## Critères GO cadrage

- [x] Territoires v2 : **martinique**, **reunion**
- [x] Delta technique D2 = **A** (pas de modèle lourd)
- [x] Sections génériques ; pas d’image v2
- [x] Pas de hub ; pas de menu header
- [x] Lot 6.3 et Savoirs hors parallèle
- [x] Ticket exec rédigé

---

## Décision de sortie (MOA)

```text
[ ] GO cadrage Culture v2 légère
[x] GO cadrage avec réserves légères
[ ] NO GO
```

**Date** : 2026-05-18 · **Validé par** : MOA

---

## Prochaine étape

1. **MOA** : valider le ticket d’**exécution** [`TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_EXEC.md`](./TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_EXEC.md).
2. **Point de contrôle BO** sur `ckr-marketone-01` avant GO exec.
3. **Pas de code** avant GO exécution.

---

## Références

| Document | Rôle |
|----------|------|
| [`TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_EXEC.md`](./TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_EXEC.md) | Exécution v2 |
| [`TICKET_MARKETONE_CULTURE_TERRITOIRES_EXEC.md`](./TICKET_MARKETONE_CULTURE_TERRITOIRES_EXEC.md) | Culture v1 |
| [`cadrage/DECISIONS.md`](../../cadrage/DECISIONS.md) — ADR-027 | Culture v2 |
| [`cadrage/CONTRACTS.md`](../../cadrage/CONTRACTS.md) — C8 | Contrat |
