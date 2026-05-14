# TICKET — Cash Flow V1.1 — Trajectoire automatique de référence

**Module** : `dorevia_cash_flow`  
**Priorité** : P1  
**Type** : évolution UX / fonctionnelle  
**Statut** : **Implémenté et recetté GO V1.1** (terrain 2026-05-13 — voir `docs/PV_RECETTE_MANUELLE_V1.md`, module `19.0.2.0.0`, `SPEC_CASH_FLOW_TRAJECTORY.md` § 5.5, `README.md` parcours V1.1)  
**Références V1** : `docs/SPEC_CASH_FLOW_TRAJECTORY.md`, `docs/PV_RECETTE_MANUELLE_V1.md`  
**Doctrine transverse** : `../../docs/cash/DOCTRINE_CASH_MODULES.md` (racine dépôt `odoo19-addons-dorevia`)  
**Recette manuelle** : `docs/RECETTE_MANUELLE_V1.md`

---

## 1. Constat

La V1 du module `dorevia_cash_flow` permet d’afficher une trajectoire de trésorerie lisible et validée en recette.

Cependant, le parcours actuel repose encore sur une sélection manuelle d’une projection Cash Guard par l’utilisateur.

Or, pour un rapport d’analyse, l’utilisateur ne devrait pas avoir à fabriquer lui-même la référence à afficher.

Le système dispose déjà des données nécessaires pour construire automatiquement la trajectoire de trésorerie de référence.

---

## 2. Objectif

Faire évoluer le rapport **Trajectoire de trésorerie** afin qu’il s’ouvre directement sur une trajectoire de référence pour la société courante.

L’objectif est que l’utilisateur puisse ouvrir :

**Comptabilité > Analyse > Trajectoire de trésorerie**

et voir immédiatement la courbe, sans devoir sélectionner manuellement une projection dans le parcours nominal.

---

## 3. Décision fonctionnelle

`dorevia_cash_flow` ne doit pas être seulement un visualiseur d’une projection choisie.

Il doit devenir le rapport de trajectoire de trésorerie de référence.

La projection Cash Guard reste une source technique pour alimenter la partie projetée, mais elle ne doit plus être un choix obligatoire pour l’utilisateur dans le parcours principal.

---

## 4. Règle de sélection automatique

À l’ouverture du rapport, le module doit rechercher automatiquement une projection Cash Guard de référence.

Règle retenue :

1. société courante ;
2. projection active ;
3. périodicité hebdomadaire : `periodicity == 'week'` ;
4. mailles hebdomadaires présentes ;
5. projection la plus récente selon `situation_date` (puis `write_date`, puis `id` pour départager).

La projection retenue sert à construire la trajectoire affichée.

---

## 5. Parcours utilisateur cible

### Parcours nominal

1. L’utilisateur ouvre **Comptabilité > Analyse > Trajectoire de trésorerie**.
2. Le rapport identifie automatiquement la projection de référence.
3. La courbe s’affiche directement.
4. Le bandeau indique clairement :

   * la projection utilisée ;
   * la date de situation ;
   * le seuil d’alerte ;
   * éventuellement le point bas.

### Parcours secondaire

Une action secondaire permet de changer de projection si besoin :

* menu **Trajectoire (choix de projection)** ;
* ou bouton **Changer de projection** sur le graphique.

Ce mode est utile pour audit, diagnostic ou comparaison ponctuelle, mais ne doit pas être le parcours principal.

---

## 6. Cas sans projection exploitable

Si aucune projection exploitable n’est trouvée, afficher un message clair.

Exemple :

> Aucune projection hebdomadaire active avec des lignes calculées n’a été trouvée pour la société courante. Veuillez créer ou actualiser une projection de trésorerie dans **Comptabilité > Projection de trésorerie > Cash Guards**.

Le rapport ne doit pas afficher une courbe vide ou trompeuse.

---

## 7. Hors périmètre

Ne pas intégrer dans ce ticket :

* nouveau moteur de projection ;
* recalcul automatique Cash Guard ;
* logique de simulation ;
* comparaison N-1 / N-2 ;
* comparaison multi-projections ;
* choix multi-sociétés ;
* refonte graphique avancée.

---

## 8. Critères de recette

Le ticket est validé si :

* l’ouverture du menu **Trajectoire de trésorerie** affiche directement une courbe quand une projection de référence existe ;
* aucune sélection manuelle n’est nécessaire dans le parcours nominal ;
* la projection utilisée est clairement indiquée dans le bandeau ;
* la projection retenue respecte la règle société courante + active + hebdomadaire + mailles présentes + `situation_date` la plus récente ;
* un message clair est affiché si aucune projection exploitable n’existe ;
* l’utilisateur peut encore changer de projection via un parcours secondaire ;
* aucun recalcul Cash Guard n’est déclenché automatiquement.

---

## 9. Formule de synthèse

**Cash Flow n’est pas un visualiseur de projection choisie.  
Cash Flow affiche automatiquement la trajectoire de trésorerie de référence de la société courante.**

---

## 10. Implémentation (trace technique)

| Élément | Détail |
|--------|--------|
| Résolution | `dorevia.cash.flow.trajectory.wizard._resolve_reference_guard` + `action_open_reference_trajectory` |
| Menu nominal | `ir.actions.server` → ouverture client graphique |
| Menu secondaire | `ir.actions.act_window` sur le wizard + bouton **Changer de projection** (OWL) |
| Tests | `tests/test_cash_flow_trajectory.py` (référence, erreur si aucun guard, priorité `situation_date`) |
