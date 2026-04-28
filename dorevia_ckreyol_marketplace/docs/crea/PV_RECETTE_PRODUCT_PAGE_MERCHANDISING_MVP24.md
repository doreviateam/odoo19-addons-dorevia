# PV — Recette Page produit merchandising MVP2.4

**Ticket** : [TICKET_PRODUCT_PAGE_MERCHANDISING_MVP24.md](TICKET_PRODUCT_PAGE_MERCHANDISING_MVP24.md)  
**Références** : [TICKET_PRODUCT_PAGE_MVP23.md](TICKET_PRODUCT_PAGE_MVP23.md), [PV_RECETTE_PRODUCT_PAGE_MVP23.md](PV_RECETTE_PRODUCT_PAGE_MVP23.md)  
**Date recette** : _(à compléter)_  
**Instance** : _(à compléter)_  
**Relecteur MOA** : _(à compléter)_

---

## Mode d’emploi recette (mini)

- Ce PV valide uniquement la vague merchandising MVP2.4, sans rouvrir la refonte MVP2.3.
- Exécuter la checklist telle quelle et rester dans le périmètre du ticket MVP2.4.
- Noter séparément les écarts **bloquants** et les **réserves non bloquantes**.
- Vérifier explicitement l’absence de régression sur les invariants MVP2.3.
- Conclure par un verdict unique : **GO**, **GO avec réserves** ou **NO GO**.

---

## Synthèse verdict

- [ ] **GO**
- [ ] **GO avec réserves**
- [ ] **NO GO**

**Commentaire synthèse** : _(à compléter)_.

---

## 1. Invariants de périmètre (contrôle de conformité)

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| Vague limitée à l’enrichissement contenu/merchandising MVP2.4 | [ ] | [ ] | [ ] | |
| Aucune modification routes catalogue / moteur shop | [ ] | [ ] | [ ] | |
| Aucune modification checkout/panier | [ ] | [ ] | [ ] | |
| Invariants MVP2.3 conservés (origine, promesse, achat, quantité, 2 colonnes) | [ ] | [ ] | [ ] | |
| Aucun ajout de logique de recommandation complexe custom | [ ] | [ ] | [ ] | |

---

## 2. Grille de recette ultra-courte — MVP2.4 merchandising (GO / GO avec réserves / NO GO)

| ID | Cas de test (MVP2.4) | Type | Statut (OK/KO/NA) | Observation courte |
|---|---|---|---|---|
| B1 | Wording réassurance remplacé par **`Achat en confiance`** | Bloquant | [ ] | |
| B2 | Aucune section vide affichée | Bloquant | [ ] | |
| B3 | Sections utiles alimentées quand données présentes (description, ingrédients, conservation, conseils, spécifications) | Bloquant | [ ] | |
| B4 | Galerie enrichie quand plusieurs médias existent | Bloquant | [ ] | |
| B5 | Rendu propre et stable quand un seul média existe (fallback) | Bloquant | [ ] | |
| B6 | Recommandations visibles uniquement si données fiables | Bloquant | [ ] | |
| B7 | Fallback propre si recommandations absentes/instables (bloc masqué sans artefact) | Bloquant | [ ] | |
| B8 | Pas de régression MVP2.3 : origine non interactive + promesse + achat/quantité + structure deux colonnes | Bloquant | [ ] | |
| B9 | Aucune modification routes/shop/checkout/moteur catalogue constatée | Bloquant | [ ] | |
| NB1 | Objectif 3 visuels vérifié sur fiches test quand possible (packshot, détail/texture, usage) | Non bloquant | [ ] | |
| NB2 | Recette exécutée sur 3 fiches représentatives : bonne / moyenne / pauvre | Non bloquant | [ ] | |
| NB3 | Qualité éditoriale globale perçue en hausse (lisibilité/crédibilité), sans refonte template | Non bloquant | [ ] | |

### Synthèse décision

- **Nombre de KO Bloquants** : ___
- **Nombre de KO Non bloquants** : ___
- **Verdict final** : [ ] GO  /  [ ] GO avec réserves  /  [ ] NO GO

### Règle de décision

- **GO** : 0 KO bloquant (réserves mineures possibles).
- **GO avec réserves** : 0 KO bloquant + au moins 1 point non bloquant.
- **NO GO** : au moins 1 KO bloquant.

---

## 3. Réserves (si GO avec réserves)

1. _(à compléter)_  
2. _(à compléter)_  
3. _(à compléter)_

---

## 4. Décision finale MOA

- **Décision** : _(GO / GO avec réserves / NO GO)_  
- **Signataire MOA** : _(à compléter)_  
- **Date** : _(à compléter)_

---

## Historique

| Date | Changement |
|------|------------|
| 2026-04-28 | Création du PV de recette MVP2.4 merchandising, aligné strictement sur `TICKET_PRODUCT_PAGE_MERCHANDISING_MVP24.md` avec grille compacte bloquant / non bloquant et règle GO / GO avec réserves / NO GO. |
