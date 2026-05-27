# Ticket Palier 4bis — Finition UX cockpit

**Module :** `dorevia_glc_analytics` *(extension)*  
**Branche cible :** `feat/glc-palier-4bis-cockpit-ux`  
**Version cible :** `19.0.4.1.0`  
**Statut :** **En cours** — Palier 4 moteur gelé MOA (`19.0.4.0.0`)

**Références :** [TICKET_PALIER_4.md](./TICKET_PALIER_4.md) · [CADRAGE_FINAL_PALIER_4.md](./CADRAGE_FINAL_PALIER_4.md) · [RECETTE_MANUELLE_PALIER_4.md](./RECETTE_MANUELLE_PALIER_4.md)

---

## 1. Contexte MOA

Le Palier 4 cockpit est **validé sur le plan moteur / calcul / invariants I1–I7**, mais l’interface n’est pas encore au niveau d’un **cockpit MOA exploitable** par GLC (libellés anglais, disposition, lisibilité).

**Décision MOA :** ouvrir un **Palier 4bis** de finition UX / wording **avant tout Palier 5**.

---

## 2. Objectif

Rendre le cockpit **lisible en français** et **présentable à GLC**, sans modifier le moteur de calcul (sauf bug identifié).

---

## 3. Périmètre

| Inclus | Exclus |
|---|---|
| Traduction / wording métier MOA de tous les libellés | Évolution du moteur d’agrégation I1–I7 |
| Disposition des KPI (réalisé vs budget) | Palier 5 (exports, scénarios, trésorerie…) |
| Bandeau d’alerte clarifié | Modification de `dorevia_glc_budget` |
| Tableau Activité × Mois lisible | Nouveaux indicateurs métier |
| Titre écran (fini le nom technique `glc.coverage.cockpit,N`) | |

---

## 4. Livrables

- Libellés français explicites sur tous les champs cockpit
- Vue formulaire retravaillée (filtres · synthèse · alertes · détail)
- Document recette UX (complément P4.1–P4.6)
- Tests automatisés : **non-régression** (46 tests GLC)

---

## 5. Critères d’acceptation

- [ ] CA-UX1 — Aucun libellé anglais auto-généré visible en interface `fr_FR`
- [ ] CA-UX2 — KPI regroupés Réalisé / Budget avec wording MOA
- [ ] CA-UX3 — Bandeau alerte compréhensible sans connaissance technique
- [ ] CA-UX4 — Tableau Activité × Mois en français métier
- [ ] CA-UX5 — Titre écran = libellé métier (pas le nom technique du modèle)
- [ ] CA-UX6 — 46 tests GLC verts, invariants I1–I7 inchangés

---

*Palier 5 en pause MOA.*
