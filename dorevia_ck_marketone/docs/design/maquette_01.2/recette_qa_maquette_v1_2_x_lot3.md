# Recette QA — Maquette CK V1.2.x · Lot 3+

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Statut** | **Recette QA Lot 3+ exécutée — 2026-06-13** |
| **GO MOA** | [`go_moa_maquette_v1_2_x_lot3.md`](./go_moa_maquette_v1_2_x_lot3.md) |
| **Livraison recettée** | [`LIVRAISON_V1_2_X_LOT3.md`](./LIVRAISON_V1_2_X_LOT3.md) |
| **Cadrage** | [`CADRAGE_MAQUETTE_CK_V1_2_X.md`](./CADRAGE_MAQUETTE_CK_V1_2_X.md) |
| **Périmètre** | `a-propos.html` · **`fiche-producteur.html`** · `recettes.html` · `contact.html` · liens Lots 1–2 |
| **Verdict QA Lot 3+** | **OK MAQUETTE CK V1.2.x LOT 3+ — validé MOA** |
| **Verdict global** | [`decision_moa_verdict_maquette_v1_2_x_vision_complete.md`](./decision_moa_verdict_maquette_v1_2_x_vision_complete.md) |

```text
ODOO EN PAUSE — recette maquette uniquement.
```

---

## 1. Pages contrôlées

| Page | Attendu | Statut | Commentaire QA |
|------|---------|--------|----------------|
| À propos | Mission · sélection · producteurs · logistique · confiance | OK | Lien fiche producteur type présent. |
| **Fiche producteur** | Hero · éditorial · critères · **grille produits** · focus · usage · logistique · CTA | OK | Atelier Les Hauts Goyaviers · 4 produits visuels · lien fiche-produit.html. |
| Recettes & savoirs | Axe éditorial · 6 cartes · réserve blog | OK | Carte sélection CK → fiche producteur. |
| Contact | 4 parcours · formulaire mock · distinction Pro | OK | Proposition producteur ajoutée. |
| Parcours producteur | Fiche produit → fiche producteur → shop / recettes | OK | Chaîne Producteur → Produits → Achat matérialisée. |

---

## 2. Contrôles QA exécutés

| Point contrôlé | Résultat |
|----------------|----------|
| Disponibilité pages | OK — HTTP 200 sur les 4 pages Lot 3+ |
| Fiche producteur — grille produits | OK — 4 cartes · prix · origines · visuels |
| Liens fiche produit ↔ producteur | OK — bidirectionnel |
| Footer cohérent | OK — « Fiche producteur » sur 9 pages |
| Images Unsplash | OK — hero + produits en HTTP 200 |
| Garde-fous | OK — pas d’annuaire · pas de portail · réserve explicite |
| Mobile 390 px | OK — grilles CSS responsive (hero stack · 1 col) |

---

## 3. Lecture QA

Le Lot 3+ complète la vision CK avec la **couche producteur** demandée par MOA : éditoriale, commerciale, reliée aux produits — sans page « Partenaires » générique.

Points forts :

* fiche producteur = pont confiance → achat (grille produits + focus CK) ;
* cohérence narrative avec fiche produit Confiture goyavier ;
* critères de sélection CK lisibles ;
* distinction logistique B2C / qualification B2B ;
* contact enrichi (proposition producteur).

Réserve non bloquante :

```text
Fiche producteur = page CMS maquette.
Arbitrage Odoo requis : CMS statique vs fiche fournisseur native.
Pas d’annuaire multi-producteurs en V1.
```

---

## 4. Classes d’arbitrage

| Classe | Éléments Lot 3+ |
|--------|-----------------|
| **V1 prioritaire** | À propos CMS · contact `/contactus` · grille produits fiche producteur · logistique CK |
| **V1 possible** | Fiche producteur CMS · critères sélection · focus emblématiques · recettes statiques |
| **V1 différée** | Annuaire producteurs · blog · recettes auto-liées · module fournisseur Odoo |
| **Réserve** | CMS vs fournisseur Odoo · workflow proposition producteur · forum |
| **Hors scope** | Portail producteur · espace connecté · annuaire partenaires |

---

## 5. Verdict

```text
OK MAQUETTE CK V1.2.x LOT 3+
```

Vision CK V1.2.x matérialisée : **expérience commerciale + logistique + éditoriale + relation producteur**.

Décision MOA actée :

```text
Vision complète matérialisée (9 pages).
Odoo en pause.
Prochaine étape = arbitrage périmètre V1 traduisible.
```

---

*Recette QA maquette CK V1.2.x Lot 3+ · 2026-06-13.*
