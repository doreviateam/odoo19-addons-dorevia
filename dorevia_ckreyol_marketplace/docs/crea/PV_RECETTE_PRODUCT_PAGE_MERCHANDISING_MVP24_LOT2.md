# PV — Recette Page produit merchandising MVP2.4 Lot 2

**Ticket** : [TICKET_PRODUCT_PAGE_MERCHANDISING_MVP24_LOT2.md](TICKET_PRODUCT_PAGE_MERCHANDISING_MVP24_LOT2.md)  
**Références** : [TICKET_PRODUCT_PAGE_MERCHANDISING_MVP24.md](TICKET_PRODUCT_PAGE_MERCHANDISING_MVP24.md), [PV_RECETTE_PRODUCT_PAGE_MERCHANDISING_MVP24.md](PV_RECETTE_PRODUCT_PAGE_MERCHANDISING_MVP24.md)  
**Date recette** : _(à compléter)_  
**Instance** : _(à compléter)_  
**Relecteur MOA** : _(à compléter)_

---

## Mode d’emploi recette (mini)

- Ce PV valide la méthode durable Lot 2 (contenu/merchandising), pas une refonte technique.
- Évaluer séparément les points **bloquants** et **non bloquants**.
- Marquer `NA — donnée absente` quand le contenu n’existe pas encore, sans l’assimiler à un KO dev.
- Vérifier l’absence de régression MVP2.3 / MVP2.4 Lot 1.
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
| Aucun chantier de refonte template (MVP2.3 inchangé) | [ ] | [ ] | [ ] | |
| Lot 1 MVP2.4 non rouvert (acquis conservés) | [ ] | [ ] | [ ] | |
| Pas de modification routes/shop/checkout/catalogue | [ ] | [ ] | [ ] | |
| Démarche centrée contenu/médias/merch simple | [ ] | [ ] | [ ] | |
| Compatibilité Odoo maintenue | [ ] | [ ] | [ ] | |

---

## 2. Grille de recette Lot 2 (GO / GO avec réserves / NO GO)

| ID | Cas de test Lot 2 | Type | Statut (OK/KO/NA) | Observation courte |
|---|---|---|---|---|
| B1 | Charte éditoriale produite (promesse, description utile, bénéfices/usages, ton C-Kreyol, sincérité) | Bloquant | [ ] | |
| B2 | Matrice de contenu opérationnelle (obligatoires/recommandés/manquants) | Bloquant | [ ] | |
| B3 | Règle “pas de section vide” appliquée dans la méthode d’exécution | Bloquant | [ ] | |
| B4 | Standards médias définis (packshot, détail/texture, usage, origine/ambiance si dispo) | Bloquant | [ ] | |
| B5 | Critères médias minimaux fixés (qualité, ratio, poids, cohérence visuelle) | Bloquant | [ ] | |
| B6 | Règles simples de recommandations documentées (famille, complémentarité, origine, collection) | Bloquant | [ ] | |
| B7 | Aucune logique complexe non native Odoo introduite | Bloquant | [ ] | |
| B8 | Backlog d’enrichissement structuré (pauvre/moyenne/riche) et priorisé | Bloquant | [ ] | |
| B9 | Contrôle recette sur 3 fiches représentatives (pauvre, moyenne, riche) | Bloquant | [ ] | |
| B10 | Aucune régression MVP2.3 / MVP2.4 Lot 1 | Bloquant | [ ] | |
| NB1 | Lisibilité et adoption de la méthode par l’équipe contenu | Non bloquant | [ ] | |
| NB2 | Progression mesurable (taux de complétion fiches) engagée | Non bloquant | [ ] | |
| NB3 | Gouvernance d’amélioration continue (rythme de revue backlog) définie | Non bloquant | [ ] | |

---

## 2.b Résultat par fiche — Vague A (P1) — pré-remplissage initial

### Fiche 1 — Manio Crackers sucrée

- Promesse courte : [x] OK / [ ] KO / [ ] NA
- Description utile (3–6 lignes) : [ ] OK / [ ] KO / [x] NA
- Sections basses utiles renseignées : [ ] OK / [ ] KO / [x] NA
- Aucune section vide visible : [x] OK / [ ] KO / [ ] NA
- Médias (packshot + 1 visuel mini) : [ ] OK / [ ] KO / [x] NA
- Recommandations simples fiables (ou fallback propre) : [ ] OK / [ ] KO / [x] NA
- Quantité + ajout panier : [ ] OK / [ ] KO / [x] NA
- Non-régression MVP2.3/Lot1 : [x] OK / [ ] KO / [ ] NA
- Observation courte : Base actuelle pauvre ; structure/fallback propres, enrichissement contenu/médias/reco à produire.

### Fiche 2 — Kit colombo

- Promesse courte : [ ] OK / [ ] KO / [x] NA
- Description utile (3–6 lignes) : [ ] OK / [ ] KO / [x] NA
- Sections basses utiles renseignées : [ ] OK / [ ] KO / [x] NA
- Aucune section vide visible : [ ] OK / [ ] KO / [x] NA
- Médias (packshot + 1 visuel mini) : [ ] OK / [ ] KO / [x] NA
- Recommandations simples fiables (ou fallback propre) : [ ] OK / [ ] KO / [x] NA
- Quantité + ajout panier : [ ] OK / [ ] KO / [x] NA
- Non-régression MVP2.3/Lot1 : [ ] OK / [ ] KO / [x] NA
- Observation courte : Fiche publiée mais non enrichie ; tests complets à réaliser après alimentation minimale.

### Synthèse Vague A — état initial

- KO bloquants : 0
- KO non bloquants : 0
- NA (donnée absente / test non exécuté) : 12
- Décision Vague A : [ ] GO / [x] GO avec réserves / [ ] NO GO
- Actions suivantes : enrichir contenu + médias + reco sur les 2 fiches P1, puis revalidation manuelle (desktop/mobile + quantité/panier).

### Synthèse décision

- **Nombre de KO Bloquants** : ___
- **Nombre de KO Non bloquants** : ___
- **Nombre de cas NA (donnée absente)** : ___
- **Verdict final** : [ ] GO  /  [ ] GO avec réserves  /  [ ] NO GO

### Règle de décision

- **GO** : 0 KO bloquant.
- **GO avec réserves** : 0 KO bloquant + au moins 1 réserve non bloquante ou cas NA.
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
| 2026-04-28 | Création du PV Lot 2 MVP2.4, aligné sur le ticket durable contenu/merchandising, avec grille bloquant/non bloquant et contrôle de non-régression MVP2.3/Lot1. |
