# Décision MOA — Section 3 PR #73 · curation reportée

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-06-15 |
| **Objet** | Périmètre de la Section 3 « Nos coups de cœur » pour la PR #73 |
| **PR concernée** | #73 — `feat/ck-home-section3-featured-images` |
| **Verdict** | ✅ **GO PR #73** avec **sélection automatique conservée** · curation BO **reportée** en ticket séparé post-#73 |

> **Mise à jour 2026-06-16** : la curation BO (catégorie « Coups de cœur ») a été **livrée ensuite** (`content` ≥ `19.0.1.18.0`). Voir [`NOTE_ARCHITECTURE_SECTION3_VEDETTES_V1.md`](./NOTE_ARCHITECTURE_SECTION3_VEDETTES_V1.md) pour l'état actuel.

---

## 1. Décision

Pour la PR #73, la MOA **conserve la logique actuelle de sélection automatique** des produits vedettes.

La mise en place d'une **curation back-office** (catégorie dédiée « Coups de cœur », sélection manuelle et ordre piloté en BO) est jugée **pertinente, mais hors périmètre de la PR #73**. Elle sera traitée dans un **ticket séparé, après merge et recette de #73**.

---

## 2. Priorité PR #73 (périmètre conservé)

Finaliser la Section 3 sur son périmètre actuel :

- rendu maquette « Nos coups de cœur » ;
- affichage correct des images produits ;
- gestion correcte des variantes ;
- prix cohérents ;
- liens « Voir » corrects ;
- stabilité mobile 390 / desktop 1280 ;
- non-régression Sections 1 et 2 ;
- `/shop` natif inchangé.

---

## 3. Hors périmètre PR #73

À **ne pas** intégrer dans la PR #73 :

- curation BO des vedettes ;
- catégorie publique dédiée « Coups de cœur » ;
- nouvel ordre spécifique vedettes ;
- rendu live QWeb de sélection curatée ;
- pilotage BO dédié.

---

## 4. Suite (post-#73)

Après merge et recette de la PR #73 :

- ouverture d'un ticket dédié **« Section 3 — curation BO des coups de cœur »** (base : `SPEC_SECTION3_VEDETTES_CURATION_BO_V1.md`) ;
- arbitrage MOA sur : catégorie dédiée · ordre des vedettes · badges · rendu live (cf. §9 de la spec).

---

## 5. Articulation avec la recette QA #73

La revue QA (`RECETTE_QA_SECTION3_VEDETTES_PR73_V1.md`) portait précisément sur la **sélection automatique** : le verdict QA « GO sous réserves » est donc **aligné** avec ce GO MOA. Conditions de la recette QA maintenues :

1. rejouer la suite de tests sur la branche avant merge ;
2. réserve image (Galettes + Confiture de goyave) à lever en validation visuelle finale.

---

*Décision MOA · Section 3 PR #73 · 2026-06-15 — curation BO reportée post-#73.*
