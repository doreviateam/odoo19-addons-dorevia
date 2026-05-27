# Ticket Palier 4bis — Finition UX cockpit

**Module :** `dorevia_glc_analytics` *(extension)*  
**Branches :** `feat/glc-palier-4bis-cockpit-ux` (P4bis période libre) · `feat/glc-cockpit-detail-groupby` (UX-GROUPBY)  
**Version livrée :** `19.0.4.4.2`  
**Statut :** **GO MOA** sur `19.0.4.4.2` — Palier 4 période libre **GO avec réserves** sur `19.0.4.2.5` ; UX-GROUPBY **GO MOA** (Option C composant OWL custom) → [TICKET_UX_GROUP_BY_DETAIL_COCKPIT.md](./TICKET_UX_GROUP_BY_DETAIL_COCKPIT.md)

**Références :** [TICKET_PALIER_4.md](./TICKET_PALIER_4.md) · [CADRAGE_FINAL_PALIER_4.md](./CADRAGE_FINAL_PALIER_4.md) · [RECETTE_MANUELLE_PALIER_4.md](./RECETTE_MANUELLE_PALIER_4.md) · [Recette période libre](./recette/RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md)

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
| Onglets détail : Activité × Mois · Ressources · Charges de structure (verdict en haut) | |

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
- [ ] CA-UX5 — Titre métier complet dans l'en-tête Odoo uniquement (pas de doublon H1 dans le corps)
- [ ] CA-UX6 — 46 tests GLC verts, invariants I1–I7 inchangés
- [ ] CA-UX7 — Filtres · alerte visible · onglets : Détail par activité · Ressources · Charges de structure · Infos
- [ ] CA-UX8 — Wording lecture CA : filtres FR, colonnes tableau courtes, période cohérente avec le mois sélectionné
- [ ] CA-UX9 — Breadcrumb / nom d'enregistrement = titre métier courant (`display_title`), sans répétition dans le corps
- [ ] CA-UX10 — Ouverture directe état par défaut + recalcul auto ; pas de bouton Actualiser visible
- [ ] CA-UX11 — Pas d'en-tête technique Odoo (breadcrumb / titre d'enregistrement) dans l'écran cockpit
- [ ] CA-UX12 — Wording charges de structure (dont masse salariale / frais généraux, solde et alertes alignés MOA)
- [ ] CA-UX13 — Onglet Détail sans ligne : état vide explicite, bandeau alerte masqué
- [ ] CA-UX14 — Filtre Activité retiré de la vue ; titre sans mention d'activité ; toutes activités actives
- [ ] CA-UX15 — Champ Mois analysé retiré des filtres visibles (redondant avec titre, Mois et Période analysée)
- [ ] CA-P4-PERIOD — Filtres date de début / date de fin + regroupement mensuel automatique
- [x] CA-P4-R10 — Recalcul immédiat des lignes et KPI au changement date_from / date_to / scénario (totaux mensuels et total période)
- [x] CA-UX-GROUPBY — Détail par activité structuré par mois avec sous-totaux mensuels + total période ; lignes `activity` seules en base ; anti-double comptage UX-G5 par construction backend → [TICKET_UX_GROUP_BY_DETAIL_COCKPIT.md](./TICKET_UX_GROUP_BY_DETAIL_COCKPIT.md) *(arbitrage final MOA : Option C composant OWL custom `glc_coverage_detail` — `19.0.4.4.2`)*

---

*Palier 5 en pause MOA.*
