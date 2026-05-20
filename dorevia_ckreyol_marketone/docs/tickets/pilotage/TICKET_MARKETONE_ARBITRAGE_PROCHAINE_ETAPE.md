# TICKET — Arbitrage prochaine étape Marketone `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_ARBITRAGE_PROCHAINE_ETAPE` |
| **Type** | **Cadrage / arbitrage produit** — aucun code |
| **Statut** | **Clôturé — GO MOA** (2026-05-18) |
| **Décision** | **Option 2** — Savoirs v1 — cadrage recettes contributives |
| **Ticket enfant** | Cadrage **GO** — exec [`TICKET_MARKETONE_SAVOIRS_V1_EXEC.md`](../savoirs/TICKET_MARKETONE_SAVOIRS_V1_EXEC.md) **ouvert** |
| **Version module actuelle** | `19.0.9.0.0` |
| **Base** | `ckr-marketone-01` |
| **ADR** | ADR-018, ADR-024, ADR-026, ADR-027 |
| **Note univers** | [`NOTE_UNIVERS_CK_MARKETONE.md`](../../cadrage/NOTE_UNIVERS_CK_MARKETONE.md) |
| **Roadmap** | [`ROADMAP.md`](../../pilotage/ROADMAP.md) |

---

## Objectif

Après clôture **Culture v2 légère** (GO MOA), **choisir une seule prochaine orientation** avant tout nouveau code — pause d’architecture produit, pas empilement de portes ou d’univers en parallèle.

**Résultat** : **GO arbitrage** — **Savoirs v1 cadrage** retenu. Culture v3 et Boutique 6.3 **reportés**.

---

## État actuel validé (2026-05-18)

```text
Marketone 19.0.9.0.0 — 91 post-tests, 0 failed

Boutique (stable)
Culture (3 territoires — GO MOA)
Savoirs (à cadrer — ce arbitrage)
```

---

## Décision MOA (2026-05-18)

```text
GO arbitrage prochaine étape :
Option 2 — Savoirs v1 — cadrage recettes contributives
```

| Option | Décision |
|--------|----------|
| **1. Culture v3** (hub `/culture` + menu) | **Reporté** — 3 territoires suffisants |
| **2. Savoirs v1 cadrage** | **Retenu** ⭐ |
| **3. Boutique 6.3** (Collections ou Promotions) | **Reporté** — gel MOA ; risque densité legacy |

### Motifs MOA

- Boutique **stabilisée** (portes, tunnel).
- Culture **amorcée et réplicable** (`guadeloupe`, `martinique`, `reunion`).
- Le **3ᵉ univers** doit être cadré avant nouvel empilement commercial ou hub Culture.

---

## Options comparées (archive)

Voir sections détaillées ci-dessous — matrice et questions conservées pour référence.

### Option 1 — Culture v3 — **reportée**

Hub `/culture` léger + navigation — **non retenu** à ce stade.

### Option 2 — Savoirs v1 — **retenue**

Cadrage recettes : identifié → proposition → modération BO → publication.

→ [`TICKET_MARKETONE_SAVOIRS_V1_CADRAGE.md`](../savoirs/TICKET_MARKETONE_SAVOIRS_V1_CADRAGE.md)

### Option 3 — Boutique 6.3 — **reportée**

Une porte (Collections **ou** Promotions) — **non retenue** ; alignement gel MOA.

---

## Contraintes MOA (arbitrage) — respectées

| # | Contrainte | Statut |
|---|------------|--------|
| A1 | Une orientation prioritaire | ✅ Savoirs v1 |
| A2 | Pas de code dans ce ticket | ✅ |
| A7 | Non-régression 91 tests | ✅ inchangé |

---

## Décision de sortie (MOA)

```text
[ ] Option 1 — Culture v3
[x] Option 2 — Savoirs v1 — cadrage recettes contributives
[ ] Option 3 — Boutique 6.3
[ ] Report / autre
```

**Date** : 2026-05-18 · **Validé par** : MOA

### Ticket enfant

| Option retenue | Ticket |
|----------------|--------|
| Savoirs v1 | [`TICKET_MARKETONE_SAVOIRS_V1_CADRAGE.md`](../savoirs/TICKET_MARKETONE_SAVOIRS_V1_CADRAGE.md) |

---

## Prochaine étape

1. **MOA** : valider le cadrage [`TICKET_MARKETONE_SAVOIRS_V1_CADRAGE.md`](../savoirs/TICKET_MARKETONE_SAVOIRS_V1_CADRAGE.md) (D1–D10).
2. **Ne pas** ouvrir Culture v3, 6.3, ni exec Savoirs en parallèle.
3. Ticket exec Savoirs — **après** GO cadrage.

---

## Références

| Document | Rôle |
|----------|------|
| [`TICKET_MARKETONE_SAVOIRS_V1_CADRAGE.md`](../savoirs/TICKET_MARKETONE_SAVOIRS_V1_CADRAGE.md) | Cadrage en cours |
| [`NOTE_UNIVERS_CK_MARKETONE.md`](../../cadrage/NOTE_UNIVERS_CK_MARKETONE.md) | Doctrine Savoirs |
| [`TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_EXEC.md`](../culture/TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_EXEC.md) | Dernier GO Culture |
