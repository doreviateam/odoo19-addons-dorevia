# Recette fonctionnelle — Trajectoire de trésorerie V1

**Module** : `dorevia_cash_flow`  
**Objet** : Rapport graphique de trajectoire de trésorerie  
**Version** : V1  
**Statut** : Recette fonctionnelle à réaliser  
**Menu cible** : Comptabilité > Analyse > Trajectoire de trésorerie

**Scénario d’exécution manuelle** (pas à pas, tableau actions / contrôles) : **`RECETTE_MANUELLE_V1.md`**.

---

## 1. Objectif de la recette

Cette recette vise à vérifier que le module `dorevia_cash_flow` permet bien d’afficher une trajectoire de trésorerie lisible, à partir d’une projection de trésorerie existante.

Le rapport doit répondre à la question métier suivante :

> Comment la trésorerie a-t-elle évolué depuis le début de l’exercice, et où va-t-elle sur les 90 prochains jours à partir de la date de situation ?

La recette doit confirmer que le module est bien une couche de restitution graphique, sans recalculer la projection et sans porter de logique de simulation.

---

## 2. Rappel du comportement attendu

Le rapport doit afficher une trajectoire de trésorerie composée de deux parties :

1. **Constaté**
   - du début de l’exercice comptable courant ;
   - jusqu’à la date de situation de la projection sélectionnée.

2. **Projeté**
   - de la date de situation ;
   - jusqu’à date de situation + 90 jours ;
   - à partir des lignes de projection déjà produites par Cash Guard.

La trajectoire attendue est une **courbe unique** représentant le solde de trésorerie dans le temps.

La distinction constaté / projeté doit qualifier les segments de cette courbe, et non produire deux courbes concurrentes.

---

## 3. Pré-requis de recette

Avant de réaliser la recette, vérifier que :

- le module `account` est installé ;
- le module `dorevia_cash_guard` est installé ;
- le module `dorevia_cash_flow` est installé ;
- au moins une projection de trésorerie hebdomadaire existe ;
- cette projection contient des lignes hebdomadaires générées ;
- la projection possède une date de situation ;
- la projection possède un seuil d’alerte ;
- l’utilisateur de recette appartient au groupe autorisé Cash Guard.

---

## 4. Données de test attendues

La recette doit idéalement être réalisée avec une projection hebdomadaire comportant :

- une date de situation identifiable ;
- un solde constaté (`observed_balance`) ;
- plusieurs points constatés depuis le début de l’exercice ;
- plusieurs mailles projetées après la date de situation ;
- un horizon de projection cohérent avec `situation_date + 90 jours` ;
- un seuil d’alerte.

Exemple de lecture attendue :

| Zone | Période | Nature |
|------|---------|--------|
| Constaté | Début exercice → date de situation | Données réelles |
| Projeté | Date de situation → date de situation + 90 jours | Données projetées |
| Seuil | Toute la période affichée | Repère d’alerte |

---

## 5. Scénario principal de recette

### Étape 1 — Accès au menu

Aller dans :

**Comptabilité > Analyse > Trajectoire de trésorerie**

Résultat attendu :

- le menu est présent ;
- le libellé est compréhensible ;
- le rapport n’est pas placé dans le menu opérationnel des projections ;
- l’utilisateur accède à un assistant ou écran de sélection.

Statut :

- [ ] OK
- [ ] KO
- [ ] À revoir

Commentaires :

```text

```

---

### Étape 2 — Sélection d’une projection hebdomadaire

Sélectionner une projection de trésorerie existante avec une périodicité hebdomadaire.

Résultat attendu :

- seules les projections éligibles sont proposées, si le domaine le permet ;
- une projection hebdomadaire peut être sélectionnée ;
- la date de situation est affichée ou identifiable ;
- le seuil d’alerte est affiché ou identifiable ;
- l’action d’affichage de la trajectoire est disponible.

Statut :

- [ ] OK
- [ ] KO
- [ ] À revoir

Commentaires :

```text

```

---

### Étape 3 — Génération de la trajectoire

Cliquer sur l’action permettant d’afficher la trajectoire.

Résultat attendu :

- le rapport s’ouvre sans erreur ;
- une courbe de trésorerie est affichée ;
- la courbe représente le solde de trésorerie dans le temps ;
- les points sont ordonnés chronologiquement ;
- aucun recalcul Cash Guard n’est déclenché automatiquement.

Statut :

- [ ] OK
- [ ] KO
- [ ] À revoir

Commentaires :

```text

```

---

## 6. Vérification du rendu graphique

### 6.1 Courbe unique

Résultat attendu :

- le graphique affiche une trajectoire unique de trésorerie ;
- il ne présente pas deux courbes concurrentes « Constaté » et « Projeté » ;
- il n’y a pas de faux zéros avant ou après les segments ;
- la courbe ne retombe pas artificiellement à zéro ;
- le projeté ne vaut pas artificiellement zéro avant la date de situation.

Statut :

- [ ] OK
- [ ] KO
- [ ] À revoir

Commentaires :

```text

```

---

### 6.2 Axe temporel

Résultat attendu :

- l’axe X présente une lecture temporelle cohérente ;
- les points suivent l’ordre chronologique ;
- la période démarre au début de l’exercice comptable courant ;
- la période s’arrête à l’horizon `situation_date + 90 jours`.

Statut :

- [ ] OK
- [ ] KO
- [ ] À revoir

Commentaires :

```text

```

---

### 6.3 Axe des montants

Résultat attendu :

- l’axe Y représente un solde de trésorerie ;
- les montants sont lisibles ;
- les montants ne sont pas interprétés comme des flux mensuels ;
- les soldes ne sont pas additionnés de manière trompeuse.

Statut :

- [ ] OK
- [ ] KO
- [ ] À revoir

Commentaires :

```text

```

---

## 7. Vérification de la bascule constaté / projeté

### 7.1 Date de situation

Résultat attendu :

- la date de situation est clairement affichée dans le rapport ou le wizard ;
- elle correspond à la date de situation de la projection sélectionnée ;
- elle sert de frontière entre le constaté et le projeté.

Statut :

- [ ] OK
- [ ] KO
- [ ] À revoir

Commentaires :

```text

```

---

### 7.2 Ligne verticale de date de situation

Résultat cible :

- une ligne verticale matérialise la date de situation sur le graphique ;
- à gauche de cette ligne : partie constatée ;
- à droite de cette ligne : partie projetée.

Implémentation V1 : le **graphique de pilotage** (client action OWL ouvert par « Afficher la trajectoire ») trace cette ligne verticale. La vue Graph native Odoo, accessible via **Liste des points**, ne la reproduit pas : voir `RECETTE_VUE_GRAPH.md`.

Résultat acceptable si lecture uniquement via liste / wizard :

- la date de situation est affichée dans le bandeau ou le wizard ;
- la limite de la vue Graph native est documentée dans `RECETTE_VUE_GRAPH.md`.

Statut :

- [ ] OK
- [ ] KO
- [ ] Accepté avec réserve
- [ ] À revoir

Commentaires :

```text

```

---

### 7.3 Distinction constaté / projeté

Résultat cible :

- la partie constatée et la partie projetée sont distinguables visuellement ;
- idéalement : trait plein pour le constaté, trait pointillé pour le projeté ;
- à défaut : mention claire dans le bandeau / wizard.

Implémentation V1 : le graphique de pilotage applique **trait plein** (constaté) et **trait pointillé** (projeté) sur une seule trajectoire.

Résultat non acceptable :

- deux courbes concurrentes avec zéros artificiels ;
- histogramme mensuel agrégé ;
- lecture qui laisse penser que le constaté tombe à zéro après la date de situation.

Statut :

- [ ] OK
- [ ] KO
- [ ] Accepté avec réserve
- [ ] À revoir

Commentaires :

```text

```

---

## 8. Vérification du seuil d’alerte

### 8.1 Affichage du seuil

Résultat attendu :

- le seuil d’alerte de la projection est visible dans le rapport ou le wizard ;
- le seuil affiché correspond bien au seuil de la projection sélectionnée.

Statut :

- [ ] OK
- [ ] KO
- [ ] À revoir

Commentaires :

```text

```

---

### 8.2 Ligne horizontale de seuil

Résultat cible :

- une ligne horizontale matérialise le seuil d’alerte sur le graphique ;
- elle permet de voir immédiatement si la trajectoire passe sous le seuil.

Implémentation V1 : le graphique de pilotage trace cette ligne horizontale. La vue Graph native (liste des points) ne la reproduit pas : voir `RECETTE_VUE_GRAPH.md`.

Résultat acceptable si lecture uniquement via liste / wizard :

- le seuil est affiché clairement dans le bandeau ou le wizard ;
- l’absence de ligne horizontale sur la vue Graph native est documentée.

Statut :

- [ ] OK
- [ ] KO
- [ ] Accepté avec réserve
- [ ] À revoir

Commentaires :

```text

```

---

## 9. Vérification du point bas

Résultat attendu :

- le point bas est affiché dans le rapport ou le wizard ;
- il correspond au minimum des points effectivement affichés dans la trajectoire ;
- il n’est pas repris aveuglément depuis `forecast_min_balance` si celui-ci couvre un périmètre différent ;
- la date du point bas est lisible.

Statut :

- [ ] OK
- [ ] KO
- [ ] À revoir

Commentaires :

```text

```

---

## 10. Cas limites

### 10.1 Projection non hebdomadaire

Sélectionner ou tenter de sélectionner une projection mensuelle ou trimestrielle.

Résultat attendu :

- le rapport refuse la génération ;
- un message clair indique que la V1 ne prend en charge que les projections hebdomadaires ;
- aucune courbe incohérente n’est affichée.

Statut :

- [ ] OK
- [ ] KO
- [ ] À revoir

Commentaires :

```text

```

---

### 10.2 Projection sans lignes hebdomadaires

Tester une projection sans `weekly_line_ids` ou avec des mailles absentes.

Résultat attendu :

- le rapport n’affiche pas une courbe vide sans explication ;
- un message invite l’utilisateur à recalculer / actualiser la projection depuis Cash Guard ;
- le module `dorevia_cash_flow` ne déclenche pas lui-même de recalcul.

Statut :

- [ ] OK
- [ ] KO
- [ ] À revoir

Commentaires :

```text

```

---

### 10.3 Projection ancienne ou horizon incohérent

Tester une projection dont l’horizon technique ne semble pas aligné avec `situation_date + 90 jours`.

Résultat attendu :

- la règle métier du rapport reste `situation_date + 90 jours` ;
- aucun point projeté ne dépasse l’horizon attendu ;
- un éventuel écart technique peut être signalé mais ne doit pas casser la lecture.

Statut :

- [ ] OK
- [ ] KO
- [ ] À revoir

Commentaires :

```text

```

---

## 11. Hors périmètre confirmé

La recette doit confirmer que le module ne fait pas les choses suivantes :

- pas de recalcul de projection ;
- pas d’appel automatique à `action_recompute_projection()` ;
- pas d’écriture sur les documents Cash Guard ;
- pas de logique de simulation ;
- pas de sélection de devis ou commandes ;
- pas de comparaison multi-scénarios ;
- pas de comparaison N-1 / N-2 en V1 ;
- pas de reporting budgétaire ;
- pas de dashboard complexe.

Statut :

- [ ] OK
- [ ] KO
- [ ] À revoir

Commentaires :

```text

```

---

## 12. Résultat attendu global

La recette est considérée comme satisfaisante si :

- le module est accessible depuis le bon menu ;
- une projection hebdomadaire peut être sélectionnée ;
- le rapport affiche une courbe de trésorerie lisible ;
- la trajectoire est une courbe unique de solde dans le temps ;
- le constaté et le projeté sont compréhensibles ;
- la date de situation est clairement identifiée ;
- le seuil d’alerte est visible ;
- le point bas est identifiable ;
- aucune valeur artificielle à zéro ne fausse la lecture ;
- aucun recalcul automatique n’est déclenché ;
- les limites de la vue Graph native (liste des points) restent documentées dans `RECETTE_VUE_GRAPH.md` le cas échéant.

---

## 13. Décision de recette

### Verdict

- [ ] GO
- [ ] GO avec réserves
- [ ] NO GO

### Réserves éventuelles

```text

```

### Actions correctives demandées

```text

```

### Commentaire final

```text

```

---

## 14. Note sur le graphique de pilotage et la vue Graph native Odoo

La V1 ouvre par défaut un **graphique de pilotage** (client action OWL) après génération des points : une courbe unique, **ligne verticale** à la date de situation, **ligne horizontale** au seuil d’alerte, **constaté en trait plein** et **projeté en trait pointillé**. Le bouton **Liste des points** permet d’accéder à la vue liste et à la **vue Graph native** Odoo pour audit ou comparaison.

La vue Graph native ne permet pas, seule, d’obtenir tous les repères visuels ci-dessus sur une même lecture : ce comportement et les pièges de lecture sont détaillés dans `RECETTE_VUE_GRAPH.md`.

---

## 15. Synthèse fonctionnelle

Le rapport **Trajectoire de trésorerie** doit être compris comme une lecture de pilotage :

> Une seule courbe de trésorerie, du début de l’exercice jusqu’à l’horizon projeté à 90 jours, avec une bascule claire entre le constaté et le projeté.

La priorité fonctionnelle n’est pas de produire un graphique complexe, mais de fournir une lecture juste, sobre et compréhensible de la trajectoire de trésorerie.
