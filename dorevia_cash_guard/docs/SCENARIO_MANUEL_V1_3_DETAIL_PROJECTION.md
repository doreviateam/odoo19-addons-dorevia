# Scénario manuel — V1.3 Détail projection (factures ouvertes)

**Ticket** : `CG-V1.3-01-PROJECTION-PERIOD-EXPLANATION`  
**Module** : `dorevia_cash_guard`

## UI — Flux complémentaires

Sur le formulaire document de projection, l’onglet **Flux complémentaires** est masqué par **`invisible="1"`** (inconditionnel : même en tant qu’administrateur, l’onglet ne doit pas apparaître tant que le rôle métier des flux manuels n’est pas recadré). Le modèle `dorevia.cash.guard.line` et le menu **Flux complémentaires** (liste des lignes) restent disponibles pour du support / réintroduction ultérieure.

## Prérequis

- Utilisateur avec droit **Cash Guard** ;
- Société avec au moins un journal banque/caisse et plan comptable permettant la facturation.

## Parcours

1. Ouvrir un **document de projection** existant ou en créer un.
2. Vérifier la trajectoire dans l’onglet **Suivi de trésorerie** (Projection / Couverture / Statut).
3. Créer une **facture client** postée, ouverte, avec **échéance** dans une semaine couverte par le document.
4. Créer une **facture fournisseur** postée, ouverte, avec **échéance** dans une autre semaine couverte.
5. Rouvrir le document ou attendre le recalcul (selon configuration) ; forcer un recalcul si besoin.
6. Ouvrir l’onglet **Détail projection**.
7. Vérifier que chaque facture apparaît sur la **Période** (ex. `Sxx`) correspondant à la date projetée `max(échéance, date de situation)`.
8. Vérifier les **signes** : client positif, fournisseur négatif ; avoirs inversés.
9. Identifier une période en **Risque** dans le suivi et la **pièce** associée dans le détail.
10. **Payer** une facture listée ; recalculer.
11. Vérifier que la pièce **disparaît** du détail et que les totaux de la maille se mettent à jour.

## Points de contrôle

- Les **flux complémentaires** n’apparaissent pas dans le détail V1.3 (uniquement `account.move` factures/avoirs ouverts).
- Aucune ligne de détail pour facture **brouillon** ou **soldée** (`amount_residual = 0`).
- Une facture **échue** avant la date de situation apparaît avec **Date projetée** = date de situation et **Échue** = Oui.

## Grille Détail projection (UX validée recette)

- **Période** : première colonne (ex. `S20`, `S31`).
- **Impact net période** : montant agrégé pour la période (répété sur chaque ligne de la même période — limitation one2many sans `group_by` ; évolution possible plus tard).
- **Nb pièces** : nombre de pièces comptabilisées pour la période (idem répétition par ligne).
- **Échue** : **Oui** / **Non** (pas une case seule).
- **Impact** : ligne pièce ; total colonne **Impact** affiché en liste.

Recette UI : **GO V1.3** sur la compréhension métier ; réserve mineure : répétition des colonnes période — acceptable pour le jalon, vue groupée envisageable ultérieurement.
