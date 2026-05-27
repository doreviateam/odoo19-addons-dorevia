# Recette manuelle — dorevia_glc_analytique · Palier 1

**Module :** `dorevia_glc_analytique`  
**Version cible :** `19.0.2.0.0` (Palier 1 — à confirmer au release)  
**Rôle testeur :** Gestionnaire GLC / MOA  
**Prérequis :** Palier 0 validé MOA · [TICKET_PALIER_1.md](./TICKET_PALIER_1.md) implémenté  
**Références :** [REGLES_AFFECTATION.md](./REGLES_AFFECTATION.md) · [RECETTE_MANUELLE_PALIER_0.md](./RECETTE_MANUELLE_PALIER_0.md)

**Hors périmètre :** ventilation salariale, bénévolat, rapport CA, clôture, blocage comptable.

---

## Contexte de recette

```text
URL  : http://localhost:18079
Base : glc-rgl-test-import
Module : dorevia_glc_analytique (Palier 1)
```

> Reprendre ou compléter les données de test Palier 0 (partenaire `Recette GLC Palier 0`, factures existantes).

---

## Avant de commencer

| # | Contrôle | ☐ |
|---|---|---|
| A1 | Palier 0 installé et menus Pilotage GLC visibles | ☐ |
| A2 | Utilisateur **Gestionnaire GLC** | ☐ |
| A3 | Menu **Anomalies analytiques** présent | ☐ |
| A4 | Paramètre date de bascule renseigné (si test A5) | ☐ |

---

## Jeu de données de test (à préparer)

| Jeu | Description | Contrôle attendu |
|---|---|---|
| T1 | Facture fournisseur validée, ligne charge **sans** analytique Activités | A1 |
| T2 | Facture client validée **sans** analytique | A2 |
| T3 | Facture client avec `BAR` + `RESSOURCES_PROPRES` | Aucune anomalie A2 |
| T4 | Écriture compte `641*` (ou paie) **avec** analytique | A4 |
| T5 | Facture post-bascule avec ancien compte `BAR_RESTAU` | A5 (si date bascule) |
| T6 | Charges activités majoritairement sur `STRUCTURE` (> seuil) | A6 synthèse |

---

## Parcours nominal

| Pas | Action | Contrôles | OK | Observations |
|---|---|---|---|---|
| P1.1 | Ouvrir **Pilotage GLC → Anomalies analytiques** | Wizard période affiché | ☐ | |
| P1.2 | Période = mois courant, validées uniquement | Options cochées par défaut cohérentes | ☐ | |
| P1.3 | Cliquer **Analyser** | Liste anomalies générée sans erreur | ☐ | |
| P1.4 | Vérifier T1 (fournisseur sans activité) | Anomalie A1 présente | ☐ | |
| P1.5 | Vérifier T2 (client incomplet) | Anomalie A2 présente | ☐ | |
| P1.6 | Vérifier T3 (BAR + RESSOURCES_PROPRES) | **Absente** des anomalies A2 | ☐ | |
| P1.7 | Vérifier T4 (paie + analytique) | Anomalie A4 présente | ☐ | |
| P1.8 | Vérifier T5 (ancien compte) | Anomalie A5 si date bascule ; sinon skip documenté | ☐ | |
| P1.9 | Vérifier bandeau / synthèse A6 | Alerte poids STRUCTURE si seuil dépassé | ☐ | |
| P1.10 | Ouvrir une pièce depuis une ligne anomalie | Navigation vers `account.move` OK | ☐ | |
| P1.11 | Valider une **nouvelle** facture sans analytique | Validation **acceptée** (non bloquant CA7) | ☐ | |

---

## Critères d'acceptation (mapping ticket)

| CA | Pas recette | ☐ |
|---|---|---|
| CA1 | P1.1 | ☐ |
| CA2 | P1.4 | ☐ |
| CA3 | P1.5 | ☐ |
| CA4 | P1.6 | ☐ |
| CA5 | P1.7 | ☐ |
| CA6 | P1.8 | ☐ |
| CA7 | P1.11 | ☐ |
| CA8 | Tests auto CI verts | ☐ |

---

## Verdict recette Palier 1

| Verdict | Condition |
|---|---|
| **GO MOA Palier 1** | P1.1–P1.11 OK · CA1–CA8 OK |
| **GO avec réserves** | A3 limité documenté · écarts mineurs UX |
| **NO GO** | Faux positifs massifs · blocage validation · régression Palier 0 |

**Verdict :** ☐ GO MOA Palier 1 · ☐ GO avec réserves · ☐ NO GO

**Testeur :** __________________ **Date :** __________

---

## Après validation Palier 1

1. Décision MOA : maintien `optional` vs durcissement progressif `mandatory`.
2. Cadrage **Palier 2** — ventilation salariale.
3. Ne pas confondre avec clôture analytique (Palier 5).
