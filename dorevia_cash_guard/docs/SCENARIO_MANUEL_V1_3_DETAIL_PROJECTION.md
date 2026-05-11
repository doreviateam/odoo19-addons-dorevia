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
7. Par défaut, consulter **Non sécurisées seulement** : seules les lignes `Risque`, `Tension` et `Vigilance` doivent être visibles.
8. Basculer sur **Toutes** pour vérifier que les lignes `Confort` restent disponibles en lecture.
9. Vérifier que chaque facture apparaît sur la **Période** (ex. `Sxx`) correspondant à la date projetée `max(échéance, date de situation)`.
10. Vérifier les **signes** : client positif, fournisseur négatif ; avoirs inversés.
11. Identifier une période en **Risque** dans le suivi et la **pièce** associée dans le détail ; ouvrir la facture via la **colonne Pièce** (`move_id`) ou l’**icône lien** en fin de ligne (infobulle *Ouvrir la facture*). Un clic sur le **reste de la ligne** ne doit pas ouvrir le formulaire technique `dorevia.cash.guard.period.move`.
12. **Payer** une facture listée ; recalculer.
13. Vérifier que la pièce **disparaît** du détail et que les totaux de la maille se mettent à jour.

## Points de contrôle

- Les **flux complémentaires** n’apparaissent pas dans le détail V1.3 (uniquement `account.move` factures/avoirs ouverts).
- Aucune ligne de détail pour facture **brouillon** ou **soldée** (`amount_residual = 0`).
- Une facture **échue** avant la date de situation apparaît avec **Date projetée** = date de situation et **Échue** = Oui.

## Grille Détail projection (UX validée recette)

- Sous-onglet **Non sécurisées seulement** : filtre de lecture sur `Risque` + `Tension` + `Vigilance`.
- Sous-onglet **Toutes** : toutes les pièces de projection, y compris `Confort`.
- **Statut** : première lecture métier, triée par défaut en `Risque`, puis `Tension`, puis `Vigilance`, puis `Confort`.
- **Période** : repère temporel conservé juste après le statut (ex. `S20`, `S31`).
- **Impact net période** : montant agrégé pour la période (répété sur chaque ligne de la même période — limitation one2many sans `group_by` ; évolution possible plus tard) ; **masquée par défaut**, réactivable depuis le sélecteur de colonnes de la liste.
- **Date projetée** : **masquée par défaut** (même mécanisme).
- **Nb pièces** : **masquée par défaut** (`optional="hide"`), réactivable si besoin d’agrégat période.
- **Pièce** : **Many2one** `account.move` en lecture seule (référence, lien vers la facture selon les droits).
- **Action** : icône discrète en fin de ligne (même ouverture que la pièce, infobulle *Ouvrir la facture*).
- **Échue** : **Oui** / **Non** (pas une case seule).
- **Impact** : ligne pièce ; total colonne **Impact** affiché en liste.

Le `group_by` natif dans le one2many embarqué n’est pas utilisé : Odoo valide le contexte de groupement sur le modèle parent. Le compromis V1.3 est donc un **tri métier** :

```text
Statut -> Période -> Date projetée -> Impact
```

Objectif : faire apparaître en premier les pièces des périodes en **Risque**, puis **Tension**, puis **Vigilance**, puis **Confort**, tout en gardant la période visible.

Recette UI : **GO V1.3** sur la compréhension métier ; réserve mineure : répétition des colonnes période/statut — acceptable pour le jalon, vue groupée envisageable ultérieurement.
