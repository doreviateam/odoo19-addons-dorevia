# note_04 — Rôles, responsabilités et circuit de validation

## 1. Objet de la note

Cette note formalise l’organisation humaine et opérationnelle du projet `dorevia_ck_marketone`.

Elle a un objectif principal :

> Délester la charge mentale de David en rendant explicite qui fait quoi, qui décide quoi, comment les retours sont traités et comment une décision devient opposable.

Cette note complète :

- `note_01.md` — doctrine initiale ;
- `note_03.md` — vision CK, arbitrage MOA et réponse au retour Dev.

Elle ne remplace pas les notes produit. Elle fixe le cadre de coordination entre les quatre acteurs du projet.

---

## 2. Les quatre acteurs

Le projet s’organise autour de quatre rôles.

```text
David   = porteur de vision / décision MOA / arbitrage final
Loulou  = cerveau IA / architecte associé / cadrage / formalisation / doctrine
Dev     = analyse technique / faisabilité / implémentation / alerte risques
Testeur = recette fonctionnelle / parcours utilisateur / non-régression / preuve d’acceptation
```

Ces rôles sont complémentaires.

Aucun acteur ne doit porter seul l’ensemble de la trajectoire.

---

## 3. Principe de gouvernance

Règle centrale :

> Tout sujet qui nécessite un arbitrage doit être transformé en décision écrite, pas porté mentalement par David.

La coordination doit être documentée.

Les intuitions, alertes, objections et propositions doivent être transformées en :

- note ;
- décision ;
- ticket ;
- critère d’acceptation ;
- scénario de recette ;
- arbitrage explicite.

---

## 4. Rôle de David

David porte :

- la vision CK ;
- la compréhension métier ;
- l’intuition produit ;
- le rapport au marché ;
- les priorités ;
- les arbitrages MOA ;
- la décision finale.

David décide notamment :

- ce qui est conforme ou non à la vision CK ;
- ce qui est prioritaire ;
- ce qui est accepté, refusé, reporté ou à revoir ;
- si une proposition technique peut être intégrée ;
- si une maquette est validée ;
- si une livraison est acceptée.

David ne doit pas être contraint de porter seul :

- la reformulation des retours ;
- la structuration des notes ;
- la préparation des tickets ;
- la coordination implicite entre Dev et Testeur ;
- la transformation des alertes en décisions ;
- la rédaction systématique des critères d’acceptation.

Ces tâches doivent être formalisées et partagées.

---

## 5. Rôle de Loulou

Loulou est le cerveau IA d’architecture, de recul, de formalisation et de mise en ordre.

Loulou aide David à :

- clarifier les intuitions ;
- structurer la doctrine ;
- rédiger les notes ;
- formuler les arbitrages ;
- préparer les prompts/tickets ;
- analyser les retours du Dev ;
- analyser les retours du Testeur ;
- distinguer vision, architecture, exécution et recette ;
- transformer les discussions en documents opposables.

Loulou peut proposer :

- une synthèse ;
- une reformulation ;
- une décision candidate ;
- un format de ticket ;
- une grille d’analyse ;
- une note de cadrage ;
- un plan de recette ;
- une réponse au Dev ou au Testeur.

Loulou ne décide pas à la place de David.

Règle :

> Loulou aide à penser, formaliser et structurer. David arbitre.

---

## 6. Rôle du Dev

Le Dev est responsable de l’analyse technique, de la faisabilité et de l’implémentation.

Le Dev doit :

- lire les notes de cadrage ;
- signaler les incohérences techniques ;
- alerter sur les risques ;
- distinguer thème, template métier et extension ;
- proposer des solutions compatibles Odoo ;
- estimer la complexité ;
- préparer ou modifier le code lorsque le ticket est validé ;
- documenter les choix techniques ;
- livrer via PR ou livrable identifiable ;
- fournir les éléments nécessaires à la recette.

Le Dev peut dire :

```text
Techniquement, je recommande ceci.
```

ou :

```text
Ce choix introduit tel risque.
```

ou :

```text
Ce point relève du thème, celui-ci du template métier, celui-ci d’une extension.
```

Le Dev ne décide pas seul :

- de la vision produit ;
- de la doctrine CK ;
- de la direction artistique ;
- du maintien ou de l’abandon de l’existant ;
- de l’introduction d’une nouvelle couche applicative ;
- de la création d’un catalogue, panier ou checkout parallèle ;
- du changement de trajectoire fonctionnelle.

Règle :

> Le Dev éclaire la faisabilité, mais ne porte pas l’arbitrage produit.

---

## 7. Rôle du Testeur

Le Testeur est responsable de la recette fonctionnelle, des parcours utilisateur et de la non-régression.

Le Testeur doit :

- lire les notes et tickets validés ;
- transformer les critères d’acceptation en scénarios de test ;
- tester les parcours utilisateur ;
- vérifier l’expérience réelle ;
- identifier les anomalies ;
- distinguer anomalie bloquante, non bloquante, amélioration et question MOA ;
- vérifier les non-régressions ;
- produire un retour exploitable.

Le Testeur doit notamment regarder :

- compréhension de la page ;
- parcours de recherche produit ;
- filtres ;
- fiche produit ;
- ajout panier ;
- panier ;
- checkout ;
- responsive ;
- lisibilité des prix ;
- réassurance ;
- cohérence B2C / B2B ;
- absence de rupture avec la promesse CK.

Le Testeur peut dire :

```text
À l’usage, ce parcours ne fonctionne pas.
```

ou :

```text
Ce comportement ne correspond pas au critère d’acceptation.
```

ou :

```text
Cette anomalie empêche la validation.
```

Le Testeur ne décide pas seul :

- de l’architecture ;
- de la doctrine produit ;
- de la priorité finale ;
- du changement de périmètre ;
- de l’acceptation d’une dérive technique.

Règle :

> Le Testeur éclaire l’usage et la conformité de la livraison, mais la validation finale reste MOA.

---

## 8. Circuit de travail standard

Le circuit de travail cible est le suivant :

```text
1. David + Loulou cadrent la vision ou le besoin
2. Loulou formalise une note, une décision ou un ticket
3. David valide ou corrige le cadrage
4. Le Dev analyse la faisabilité et les risques
5. Le Testeur prépare les scénarios de recette si nécessaire
6. David + Loulou arbitrent les retours
7. Le Dev implémente uniquement sur ticket validé
8. Le Testeur recette
9. David valide, refuse, reporte ou demande correction
10. Loulou formalise la décision ou la suite
```

Ce circuit peut être allégé pour les micro-tâches, mais il doit rester la référence.

---

## 9. Traitement d’un retour Dev

Un retour Dev doit être lu selon quatre catégories.

| Catégorie | Traitement |
|---|---|
| Confirmation | À intégrer comme validation technique |
| Alerte risque | À transformer en arbitrage ou contrainte |
| Proposition technique | À évaluer face à la doctrine MOA |
| Objection de trajectoire | À traiter comme décision produit, pas comme simple détail technique |

Un retour Dev ne doit pas déclencher automatiquement du développement.

Il doit d’abord être converti en :

```text
décision
ticket
question MOA
contrainte technique
ou point à tester
```

Règle :

> Aucun retour Dev important ne doit rester implicite.

---

## 10. Traitement d’un retour Testeur

Un retour Testeur doit être classé en :

| Type | Description | Traitement |
|---|---|---|
| Bloquant | Empêche l’usage ou viole un critère d’acceptation | Correction obligatoire |
| Majeur | Dégrade fortement le parcours | Arbitrage MOA |
| Mineur | Gêne limitée | Correction ou report |
| Suggestion | Amélioration possible | Backlog |
| Question MOA | Ambiguïté fonctionnelle | Décision écrite |

Le Testeur ne doit pas avoir à deviner l’intention produit.

Chaque test doit se rattacher à :

- une note ;
- un ticket ;
- un critère d’acceptation ;
- une décision MOA ;
- une maquette validée.

---

## 11. Format attendu d’un ticket Dev

Un ticket destiné au Dev doit idéalement contenir :

```text
Projet :
Contexte :
Objectif :
Périmètre :
Hors périmètre :
Doctrine applicable :
Contraintes Odoo :
Éléments Open Design concernés :
Éléments existants à analyser :
Livrables attendus :
Critères d’acceptation :
Tests attendus :
Interdictions :
Questions ouvertes :
```

Règle :

> Le Dev ne doit pas avoir à reconstruire la doctrine depuis des échanges dispersés.

---

## 12. Format attendu d’un ticket Testeur

Un ticket destiné au Testeur doit idéalement contenir :

```text
Objet de la recette :
Contexte utilisateur :
Parcours à tester :
Données de test :
Critères d’acceptation :
Points de vigilance :
Non-régressions à vérifier :
Résultat attendu :
Format du retour :
```

Règle :

> Le Testeur doit vérifier une intention validée, pas interpréter une vision floue.

---

## 13. Règle sur les décisions

Une décision devient opposable lorsqu’elle est formulée explicitement dans :

- une note ;
- un ticket validé ;
- un compte rendu de recette ;
- une réponse MOA formalisée ;
- une section “Décision” d’un document projet.

Les décisions doivent être formulées avec des verbes clairs :

```text
Validé
Refusé
Reporté
À analyser
À tester
À abandonner
À conserver
À simplifier
À transformer en ticket
```

Exemple :

```text
Décision MOA :
L’existant dorevia_ckreyol_marketone est utilisé comme matière d’analyse, mais ne constitue pas la base technique automatique de la suite.
```

---

## 14. Application immédiate à CK

Dans le contexte actuel de `dorevia_ck_marketone`, les décisions déjà actées sont :

```text
CK = sourcing + commerce + logistique agro-transformée créole
Odoo = source de vérité métier
Open Design = atelier de maquette et référentiel UX
Ancienne DA terracotta/sauge/pastel = historique, non cible
dorevia_ckreyol_marketone = matière d’analyse, non socle automatique
dorevia_ck_theme = pas de développement avant maquette validée
Pas de catalogue parallèle
Pas de panier parallèle
Pas de checkout parallèle
```

La prochaine étape opérationnelle ne doit pas être lancée tant que les rôles et le circuit de validation ne sont pas partagés entre les quatre acteurs.

---

## 15. Ce que chaque acteur doit recevoir maintenant

### Dev

Le Dev doit recevoir :

- `note_03.md` ;
- `note_04.md` ;
- la confirmation que son retour est intégré ;
- la clarification qu’aucun développement n’est encore lancé ;
- la future demande de grille d’analyse uniquement lorsque le circuit est validé.

### Testeur

Le Testeur doit recevoir :

- la vision CK simplifiée ;
- son rôle dans la recette ;
- la distinction entre validation d’usage et arbitrage produit ;
- les futurs critères de recette lorsqu’ils seront produits.

### David

David doit conserver :

- l’arbitrage final ;
- la vision ;
- le pouvoir de dire oui/non ;
- la capacité à corriger la trajectoire.

David ne doit pas porter seul :

- la coordination implicite ;
- la reformulation des retours ;
- la transformation des alertes en décisions ;
- le suivi mental des rôles de chacun.

### Loulou

Loulou doit aider à :

- mettre en forme ;
- synthétiser ;
- arbitrer par écrit ;
- préparer les messages ;
- préparer les notes ;
- préparer les tickets ;
- réduire la charge mentale de David.

---

## 16. Phrase de synthèse

> Le projet CK doit être piloté par une organisation claire : David porte la vision et l’arbitrage, Loulou structure et formalise, le Dev éclaire et implémente, le Testeur vérifie et sécurise l’usage. Toute décision importante doit être écrite afin que la charge mentale ne repose pas uniquement sur David.
