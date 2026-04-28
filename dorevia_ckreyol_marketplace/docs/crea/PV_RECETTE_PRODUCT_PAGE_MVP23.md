# PV — Recette Page produit MVP2.3

**Ticket** : [TICKET_PRODUCT_PAGE_MVP23.md](TICKET_PRODUCT_PAGE_MVP23.md)  
**Cadrage source** : [3_PRODUCT_PAGE.md](../mvp_02/3_PRODUCT_PAGE.md)  
**Date recette** : _(à compléter)_  
**Instance** : _(à compléter)_  
**Relecteur MOA** : _(à compléter)_

---

## Mode d’emploi recette (mini)

- Ce PV valide uniquement le périmètre fonctionnel MVP2.3 de la page produit.
- Exécuter la checklist telle quelle, sans rouvrir le cadrage ni étendre le périmètre.
- Consigner séparément les écarts **bloquants** et les **réserves non bloquantes**.
- S’appuyer sur les observations courtes pour objectiver chaque statut (OK/KO/NA).
- Conclure par un verdict unique : **GO**, **GO avec réserves** ou **NO GO**.

---

## Synthèse verdict

- [ ] **GO**
- [ ] **GO avec réserves**
- [ ] **NO GO**

**Commentaire synthèse** : _(à compléter)_.

---

## 1. Invariants bloquants (contrôle de conformité)

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| Structure desktop en 2 colonnes (médias gauche, info/achat droite) | [ ] | [ ] | [ ] | |
| Flux d’action principal unique (quantité + ajout panier) | [ ] | [ ] | [ ] | |
| Origine affichée en info non interactive (pas case à cocher) | [ ] | [ ] | [ ] | |
| Progressivité du détail (haut de fiche court, détail en bas) | [ ] | [ ] | [ ] | |
| Compatibilité native Odoo préservée | [ ] | [ ] | [ ] | |

---

## 2. Colonne gauche — galerie média

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| Image principale prioritaire et lisible | [ ] | [ ] | [ ] | |
| Miniatures disponibles en cas multi-médias | [ ] | [ ] | [ ] | |
| Changement média simple et stable | [ ] | [ ] | [ ] | |
| Rendu propre en cas de média unique | [ ] | [ ] | [ ] | |

---

## 3. Colonne droite — hiérarchie information/conversion

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| Ordre de lecture global conforme ticket | [ ] | [ ] | [ ] | |
| Titre produit clairement dominant | [ ] | [ ] | [ ] | |
| Promesse courte visible sous le titre | [ ] | [ ] | [ ] | |
| Prix immédiatement repérable | [ ] | [ ] | [ ] | |
| Description courte lisible (sans surcharge) | [ ] | [ ] | [ ] | |

---

## 4. Zone d’achat et actions secondaires

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| Zone quantité + ajout panier immédiatement identifiable | [ ] | [ ] | [ ] | |
| CTA `Ajouter au panier` visuellement prioritaire | [ ] | [ ] | [ ] | |
| Wishlist/comparaison plus discrètes que CTA principal | [ ] | [ ] | [ ] | |
| Fonctionnement ajout panier/quantité non régressé | [ ] | [ ] | [ ] | |

---

## 5. Bloc réassurance

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| Bloc présent, court, lisible | [ ] | [ ] | [ ] | |
| Formulations crédibles (pas de surpromesse) | [ ] | [ ] | [ ] | |
| Intégration visuelle sobre | [ ] | [ ] | [ ] | |

---

## 6. Sections basses — détail produit

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| Détail produit mieux structuré que l’état initial | [ ] | [ ] | [ ] | |
| Sections/accordéons lisibles et stables | [ ] | [ ] | [ ] | |
| Pas d’effet “mur de texte technique” | [ ] | [ ] | [ ] | |

---

## 7. Recommandations bas de page

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| Section affichée uniquement si données disponibles | [ ] | [ ] | [ ] | |
| Comportement cohérent avec capacités natives Odoo | [ ] | [ ] | [ ] | |
| Aucun ajout de logique complexe hors périmètre | [ ] | [ ] | [ ] | |

---

## 8. Non-régression fonctionnelle Odoo

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| Prix et variantes : affichage/actualisation corrects | [ ] | [ ] | [ ] | |
| Ajout panier : comportement standard conservé | [ ] | [ ] | [ ] | |
| Wishlist/comparaison : rendu propre selon modules actifs/inactifs | [ ] | [ ] | [ ] | |
| Responsive essentiel (desktop + mobile) validé | [ ] | [ ] | [ ] | |

---

## 9. Grille de recette ultra-courte — MVP2.3 (GO / GO avec réserves / NO GO)

| ID | Cas de test (MVP2.3) | Type | Statut (OK/KO/NA) | Observation courte |
|---|---|---|---|---|
| B1 | Produit **avec origine** : origine visible en haut, en badge/texte **non interactif** | Bloquant | [ ] | |
| B2 | Produit **sans origine** : aucun bloc vide/parasite lié à l’origine | Bloquant | [ ] | |
| B3 | Produit **avec promesse exploitable** : promesse affichée sous le titre | Bloquant | [ ] | |
| B4 | Produit **sans promesse exploitable** : promesse masquée (pas de génération artificielle) | Bloquant | [ ] | |
| B5 | Colonne droite : **pas de duplication** du texte descriptif | Bloquant | [ ] | |
| B6 | Produit **1 média** : affichage média stable et lisible | Bloquant | [ ] | |
| B7 | Produit **multi-médias** : navigation galerie fonctionnelle | Bloquant | [ ] | |
| B8 | **Achat + quantité** : modification quantité + ajout panier fonctionnels | Bloquant | [ ] | |
| B9 | **Desktop essentiel** : structure et lisibilité conformes (2 colonnes, actions accessibles) | Bloquant | [ ] | |
| B10 | **Mobile essentiel** : empilement lisible, actions achat accessibles | Bloquant | [ ] | |
| NB1 | **Wishlist** : conforme à la configuration active (présent+fonctionnel si activé, sinon absent sans erreur) | Non bloquant | [ ] | |
| NB2 | **Comparaison** : conforme à la configuration active (présent+fonctionnel si activé, sinon absent sans erreur) | Non bloquant | [ ] | |
| NB3 | Libellé réassurance (`Conditions générales`) potentiellement à adoucir (amélioration future) | Non bloquant | [ ] | |

### Synthèse décision

- **Nombre de KO Bloquants** : ___
- **Nombre de KO Non bloquants** : ___
- **Verdict final** : [ ] GO  /  [ ] GO avec réserves  /  [ ] NO GO

### Règle de décision

- **GO** : 0 KO bloquant (réserves mineures possibles).
- **GO avec réserves** : 0 KO bloquant + au moins 1 point non bloquant.
- **NO GO** : au moins 1 KO bloquant.

---

## 10. Réserves (si GO avec réserves)

1. **Amélioration future (non bloquante) — contenu produit / merchandising** : la grammaire MVP2.3 est validée, mais la fiche reste éditorialement pauvre (peu de médias, sections basses faiblement alimentées, bloc réassurance minimal, recommandations peu visibles). Ce point relève d’un chantier séparé, sans réouverture du ticket MVP2.3.  
2. _(à compléter)_  
3. _(à compléter)_

---

## 11. Décision finale MOA

- **Décision** : _(GO / GO avec réserves / NO GO)_  
- **Signataire MOA** : _(à compléter)_  
- **Date** : _(à compléter)_

---

## Historique

| Date | Changement |
|------|------------|
| 2026-04-28 | Création du PV de recette MVP2.3, aligné sur le ticket `TICKET_PRODUCT_PAGE_MVP23.md` et les invariants de `3_PRODUCT_PAGE.md`. |
| 2026-04-28 | Ajout d'une grille de recette ultra-courte checklistable (bloquant / non bloquant) avec règle de décision GO / GO avec réserves / NO GO. |
| 2026-04-28 | Ajout d'une réserve non bloquante sur la richesse éditoriale de la fiche (chantier futur séparé « contenu produit / merchandising », sans réouverture MVP2.3). |
