# Recette QA — Maquette CK V1.2.x · Lot 2

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Statut** | **Recette QA Lot 2 exécutée — 2026-06-13** |
| **GO MOA** | [`go_moa_maquette_v1_2_x_lot2.md`](./go_moa_maquette_v1_2_x_lot2.md) |
| **Livraison recettée** | [`LIVRAISON_V1_2_X_LOT2.md`](./LIVRAISON_V1_2_X_LOT2.md) |
| **Cadrage** | [`CADRAGE_MAQUETTE_CK_V1_2_X.md`](./CADRAGE_MAQUETTE_CK_V1_2_X.md) |
| **Périmètre** | `artifact/shop.html` · `artifact/categorie.html` · parcours Lot 1-2 |
| **Verdict QA Lot 2** | **OK MAQUETTE CK V1.2.x LOT 2 — catalogue et catégorie matérialisés** |

```text
ODOO EN PAUSE — recette maquette uniquement.
```

---

## 1. Pages contrôlées

| Page | Attendu | Statut | Commentaire QA |
|------|---------|--------|----------------|
| Shop | Catalogue lisible · produits · prix · origines · collections · filtres visuels | OK | 12 produits visibles, prix et origines présents, collections lisibles, signal Pro discret. |
| Catégorie · Épicerie créole | Page collection éditorialisée · guide achat · grille filtrée | OK | Hero éditorial clair, bloc “Comment choisir ?”, 7 produits, retour shop et lien fiche produit. |
| Parcours Lot 1-2 | Accueil → Shop → Catégorie → Fiche produit · accès Pro | OK | Liens relatifs principaux opérationnels dans l’artifact. |

---

## 2. Contrôles QA exécutés

| Point contrôlé | Résultat |
|----------------|----------|
| Disponibilité pages | OK — `shop.html` et `categorie.html` en HTTP 200 |
| Desktop 1280 px | OK — shop et catégorie sans overflow horizontal |
| Mobile 390 px | OK — shop et catégorie sans overflow horizontal (`scrollWidth = 390`) |
| Grille shop | OK — 12 cartes produit, prix, origines, familles, médias |
| Grille catégorie | OK — 7 cartes produit, prix, origines, médias |
| Tags `.arbitrage-tag` | OK — aucun tag visible au rendu |
| Images / backgrounds | OK — URLs Unsplash Lot 2 contrôlées en HTTP 200 |
| Navigation principale | OK — nav/header/footer vers `shop.html`, `categorie.html`, `fiche-produit.html`, `professionnels.html` |

---

## 3. Lecture QA

Le Lot 2 complète utilement le Lot 1 : CK n’est plus seulement une home et une fiche produit, mais une boutique avec une logique catalogue lisible.

Points forts :

* densité marchande plus crédible : 12 produits côté shop ;
* catégorie éditorialisée sans devenir une page magazine ;
* prix, origine et famille produit restent visibles ;
* signal Pro discret, cohérent avec la doctrine B2B qualifiée ;
* mobile propre, sans bande blanche ni débordement.

Point de vigilance :

```text
Plusieurs CTA produits restent en routes Odoo cibles (/shop/...)
et ne doivent pas être présentés comme des liens statiques de démo.
```

Cette réserve n’est pas bloquante pour la maquette : elle confirme le mapping Odoo à prévoir à la traduction.

---

## 4. Classes d’arbitrage

| Classe | Éléments Lot 2 |
|--------|----------------|
| **V1 prioritaire** | Shop natif · grille produits · prix TTC · origines · catégorie Odoo · breadcrumb · réassurance |
| **V1 possible** | Pills collections · filtres visuels · tri select · intro éditoriale catégorie · guide “Comment choisir ?” |
| **V1 différée** | Filtres réellement interactifs · pagination · facettes avancées · pages multiples de collection |
| **Réserve** | Routes Odoo absolues à mapper · promesses logistiques à confirmer · attributs origine/famille à structurer |
| **Hors scope** | Catalogue parallèle · filtres AJAX custom · moteur de recherche custom |

---

## 5. Verdict

```text
OK MAQUETTE CK V1.2.x LOT 2
```

Le Lot 2 est validable comme référence de direction catalogue pour arbitrage MOA.

Décision recommandée :

```text
Valider Lot 2.
Décider ensuite : Lot 3+ éditorial / contact
ou préparation de la traduction Odoo sur périmètre Lot 1 + Lot 2.
```

---

*Recette QA maquette CK V1.2.x Lot 2 · 2026-06-13.*
