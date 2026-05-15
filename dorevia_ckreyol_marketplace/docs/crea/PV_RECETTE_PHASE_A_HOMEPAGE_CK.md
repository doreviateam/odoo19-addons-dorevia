# PV de recette — Phase A homepage CK

**Objet** : constater les résultats de la **Phase A** du ticket [TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md](TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md) sur la homepage CK, à structure de page constante.

**Date** : 2026-04-23  
**Statut** : **PV rempli — verdict MOA : GO avec réserves / Recette validée avec réserves** (lot 1 SCSS cartes sélection, PR `feat/homepage-phase-a`). Les sections de détail §4–§8 restent non cochées : la décision MOA est portée par le verdict global §3 et la décision finale §13, qui prévalent pour ce lot.

**Périmètre** : homepage uniquement (`website.homepage` / `ckr_page_homepage`) — **Phase A** : médias, copy hors gel, micro-ajustements visuels / SCSS.

**Documents de référence** :

- [TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md](TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md)
- [BRIEF_CRÉA_PHASE_A_HOMEPAGE.md](BRIEF_CRÉA_PHASE_A_HOMEPAGE.md)
- [PLATEFORME_MARQUE_CK_V1.md](PLATEFORME_MARQUE_CK_V1.md)
- [CADRAGE_DESIGN_CREATION_CK_V1.md](CADRAGE_DESIGN_CREATION_CK_V1.md)
- [SPEC_HERO_HOMEPAGE.md](../direction/SPEC_HERO_HOMEPAGE.md)
- [PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md](PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md)

---

## 1. Rappel du périmètre validé

La présente recette porte uniquement sur la **Phase A** :

- remplacement / amélioration des **médias** sur les blocs existants ;
- ajustements de **copy hors gel** ;
- ajustements **SCSS** de finition, de rythme et de désirabilité ;
- **sans** réordonnancement de blocs ;
- **sans** ajout de nouveaux snippets ou nouvelles portes d’entrée ;
- **sans** modification du **hero copy gelé** sauf amendement SPEC explicite.

---

## 2. Objectif de recette

Vérifier que la homepage gagne de façon perceptible :

- en **appétence**
- en **cohérence visuelle**
- en **qualité perçue**
- en **rythme**
- en **désirabilité marchande**

tout en respectant :

- les **gels documentaires**
- la **structure V1**
- les contraintes **responsive**
- les fondamentaux de **sobriété CK**

---

## 3. Synthèse de verdict

### Verdict global

- [ ] **GO**
- [x] **GO avec réserves**
- [ ] **NO GO**

### Appréciation synthétique MOA

La homepage gagne en tenue, en cohérence et en qualité perçue sur le bloc travaillé. Le rendu desktop comme mobile est propre, lisible et plus crédible. Le lot 1 améliore bien la sensation de finition sans casser la charpente ni dégrader la sobriété CK.

En revanche, le gain d’**appétence perçue** reste **partiel** : la homepage demeure globalement assez sage et l’écart principal avec l’ambition du cadrage reste situé dans le **rythme de page**, la **densité hiérarchisée** et la **partition d’ensemble**, non traités dans ce lot.

---

## 4. Vérification des gels

| Point gelé | Référence | Conforme | Observation |
|------------|-----------|----------|---------------|
| Hero 60/40 conservé | PROPOSITION §9 | [ ] Oui [ ] Non | |
| Supplier variante plane conservée | PROPOSITION §9 | [ ] Oui [ ] Non | |
| Editorial bandeau sobre sans `<h2>` | PROPOSITION §9 | [ ] Oui [ ] Non | |
| Selection garde-fou responsive conservé | PROPOSITION §9 | [ ] Oui [ ] Non | |
| Fil rouge amber respecté | PROPOSITION §9 | [ ] Oui [ ] Non | |
| Copy hero conforme SPEC §7 | SPEC Hero §7 | [ ] Oui [ ] Non | |
| Explorer sans changement structurel | ADR-007 / ticket | [ ] Oui [ ] Non | |

### Conclusion gels

- [ ] Aucun écart constaté
- [ ] Écarts mineurs documentés
- [ ] Écart bloquant nécessitant arbitrage

---

## 5. Recette par objectif perceptif

### 5.1 Site plus construit

La homepage donne-t-elle davantage une impression de page pensée et composée, plutôt que d’assemblage de blocs ?

- [ ] Oui
- [ ] Partiellement
- [ ] Non

**Observations**

- continuité entre sections :
- cohérence d’ensemble :
- sentiment de finition :

---

### 5.2 Site plus désirable

La homepage suscite-t-elle davantage l’envie d’explorer et d’acheter ?

- [ ] Oui
- [ ] Partiellement
- [ ] Non

**Observations**

- qualité des visuels :
- désirabilité des cartes produit :
- chaleur perçue :
- présence sensible de la matière produit :

---

### 5.3 Site plus cohérent visuellement

Les blocs mis à jour paraissent-ils appartenir à la même famille visuelle ?

- [ ] Oui
- [ ] Partiellement
- [ ] Non

**Observations**

- lumière / colorimétrie :
- cohérence des cadrages :
- homogénéité des images :
- cohérence des espacements :

---

### 5.4 Site plus rythmé

Le scroll donne-t-il une impression plus juste de respiration et de densité ?

- [ ] Oui
- [ ] Partiellement
- [ ] Non

**Observations**

- transitions entre blocs :
- sensation de page trop plate / moins plate :
- progression plus lisible :

---

### 5.5 Site toujours crédible et sobre

Le gain d’appétence a-t-il été obtenu sans glisser vers la surcharge, la sur-promesse ou le folklore ?

- [ ] Oui
- [ ] Partiellement
- [ ] Non

**Observations**

- ton :
- niveau de retenue :
- absence d’effets décoratifs parasites :

---

## 6. Recette par bloc

### 6.1 Hero

| Critère | OK | Réserve | NOK | Observation |
|---------|-----|---------|-----|---------------|
| Visuel plus solide / plus incarné | [ ] | [ ] | [ ] | |
| Continuité avec la charte CK | [ ] | [ ] | [ ] | |
| Copy conforme SPEC | [ ] | [ ] | [ ] | |
| CTA / layout inchangés | [ ] | [ ] | [ ] | |
| Mobile satisfaisant | [ ] | [ ] | [ ] | |

---

### 6.2 Explorer

| Critère | OK | Réserve | NOK | Observation |
|---------|-----|---------|-----|---------------|
| Aucune dérive structurelle | [ ] | [ ] | [ ] | |
| Lisibilité des cartes améliorée | [ ] | [ ] | [ ] | |
| Température éditoriale plus cohérente | [ ] | [ ] | [ ] | |
| Mobile non dégradé | [ ] | [ ] | [ ] | |

---

### 6.3 Supplier

| Critère | OK | Réserve | NOK | Observation |
|---------|-----|---------|-----|---------------|
| Visuel plus fort / plus incarné | [ ] | [ ] | [ ] | |
| Cohérence avec hero | [ ] | [ ] | [ ] | |
| Copy plus chaleureuse sans folklore | [ ] | [ ] | [ ] | |
| Variante plane respectée | [ ] | [ ] | [ ] | |

---

### 6.4 Sélection produits

| Critère | OK | Réserve | NOK | Observation |
|---------|-----|---------|-----|---------------|
| Produits mieux mis en désir | [ ] | [ ] | [ ] | |
| Images cohérentes | [ ] | [ ] | [ ] | |
| Cartes plus qualitatives | [ ] | [ ] | [ ] | |
| Hover / focus satisfaisants | [ ] | [ ] | [ ] | |
| Responsive intact | [ ] | [ ] | [ ] | |

---

### 6.5 Editorial

| Critère | OK | Réserve | NOK | Observation |
|---------|-----|---------|-----|---------------|
| Bloc garde sa sobriété | [ ] | [ ] | [ ] | |
| Copy apporte une profondeur utile | [ ] | [ ] | [ ] | |
| Pas de sur-explication | [ ] | [ ] | [ ] | |
| Pas de `<h2>` ajouté | [ ] | [ ] | [ ] | |

---

### 6.6 Trust

| Critère | OK | Réserve | NOK | Observation |
|---------|-----|---------|-----|---------------|
| Compréhension immédiate | [ ] | [ ] | [ ] | |
| Réassurance lisible | [ ] | [ ] | [ ] | |
| Pas de lourdeur textuelle | [ ] | [ ] | [ ] | |

---

## 7. Responsive & accessibilité

### Desktop

- [ ] Satisfaisant
- [ ] Réserves
- [ ] NOK

### Mobile

- [ ] Satisfaisant
- [ ] Réserves
- [ ] NOK

### Points à vérifier

| Point | OK | Réserve | NOK | Observation |
|-------|-----|---------|-----|-------------|
| Hiérarchie lisible sur mobile | [ ] | [ ] | [ ] | |
| Hero non dégradé | [ ] | [ ] | [ ] | |
| Explorer lisible | [ ] | [ ] | [ ] | |
| Sélection non cassée | [ ] | [ ] | [ ] | |
| Focus visibles | [ ] | [ ] | [ ] | |
| Contrastes conformes | [ ] | [ ] | [ ] | |

---

## 8. Performance & qualité d’intégration

| Point | OK | Réserve | NOK | Observation |
|-------|-----|---------|-----|-------------|
| Images correctement dimensionnées | [ ] | [ ] | [ ] | |
| Lazy loading pertinent | [ ] | [ ] | [ ] | |
| Pas de dégradation majeure perçue | [ ] | [ ] | [ ] | |
| Assets frontend propres | [ ] | [ ] | [ ] | |
| Bump version fait si nécessaire | [ ] | [ ] | [ ] | |

---

## 9. Avant / après — constats synthétiques

### Avant

Homepage sobre et sérieuse, mais encore un peu froide, avec une désirabilité limitée et peu de montée en intensité perceptive au-delà du hero.

### Après

Homepage plus propre, plus finie et légèrement plus désirable sur les cartes sélection, sans rupture de structure ni glissement promotionnel. Le gain est réel mais reste localisé ; il ne suffit pas à lui seul à combler l’écart d’appétence globale identifié dans le ticket.

---

## 10. Écarts résiduels vers Phase B / C

Lister ici ce qui reste **hors Phase A** et ne doit pas être rouvert improprement dans la recette.

### Reste à traiter en Phase B éventuelle

- réordonnancement de blocs :
- remontée éventuelle d’un bloc réassurance :
- ajustement de partition :

### Reste à traiter en Phase C éventuelle

- portes maîtresses :
- bloc Origines dédié :
- usages / blog :
- capture / newsletter :

---

## 11. Réserves / actions correctives

| ID | Sujet | Niveau | Action demandée | Ticket / suite |
|----|-------|--------|-----------------|----------------|
| R1 | Gain d’appétence limité au périmètre cartes sélection | Majeur | Ne pas considérer le ticket comme clos sur le fond ; conserver ouverte la question du rythme vertical / densité / partition pour un lot suivant. | Lot 2 ou Phase B selon arbitrage |
| R2 | Écart principal non traité sur la progression perceptive de la homepage | Majeur | Documenter explicitement dans le PV que le lot 1 est un polish ciblé et non une réponse complète à l’ambition design du ticket. | À rattacher au ticket mère `HOMEPAGE-APPETENCE-PARTITION-V1` |

---

## 12. Pièces jointes attendues

- captures **desktop**
- captures **mobile**
- éventuellement diff visuel avant / après
- lien PR / branche
- note courte de justification créative

---

## 13. Décision finale

- [ ] **Recette validée**
- [x] **Recette validée avec réserves**
- [ ] **Recette refusée**

### Commentaire de décision

Le lot 1 peut être accepté comme amélioration ciblée, propre et sans régression visible. Il ne clôt toutefois pas le sujet d’appétence homepage au sens du cadrage design, qui reste dépendant de travaux complémentaires sur les contenus et/ou sur la partition visuelle d’ensemble.

---

## 14. Historique du document

| Date | Changement |
|------|------------|
| 2026-04-23 | Création — trame de PV de recette pour la Phase A du ticket `HOMEPAGE-APPETENCE-PARTITION-V1`. |
| 2026-04-23 | **Remplissage verdict MOA lot 1** — GO avec réserves (R1 majeur : gain d’appétence limité au périmètre cartes sélection ; R2 majeur : écart principal sur progression perceptive non traité). Décision finale §13 : **recette validée avec réserves**. Les questions rythme vertical / densité / partition restent ouvertes pour un lot 2 ou Phase B. |
