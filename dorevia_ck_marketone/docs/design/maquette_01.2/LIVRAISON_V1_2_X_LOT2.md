# Livraison Dev — Maquette CK V1.2.x · Lot 2

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **GO MOA** | [`go_moa_maquette_v1_2_x_lot2.md`](./go_moa_maquette_v1_2_x_lot2.md) |
| **Date livraison** | 2026-06-13 |
| **Statut** | **Livré Dev — recetté QA OK** |

```text
ODOO EN PAUSE — AUCUNE TRADUCTION ODOO
```

---

## 1. Artifact HTML livré

| Page | Fichier | Route Odoo cible |
|------|---------|------------------|
| Boutique / Shop | [`artifact/shop.html`](./artifact/shop.html) | `/shop` |
| Catégorie · Épicerie créole | [`artifact/categorie.html`](./artifact/categorie.html) | `/shop/category/epicerie-creole-1` |

**Preview** : `http://127.0.0.1:8766/shop.html` · `…/categorie.html`

---

## 2. Parcours maquette complet

```text
index.html → shop.html → categorie.html → fiche-produit.html
         ↘ professionnels.html
```

Liens mis à jour depuis l’accueil Lot 1 (hero · catégories · footer · nav).

---

## 3. Shop (`shop.html`)

| Bloc | Contenu |
|------|---------|
| Fil d’Ariane | Accueil · Boutique |
| En-tête | Titre · promesse catalogue |
| Collections | Pills : Tous · Épicerie créole · Manioc · Incontournables · Packs · Nouveautés |
| Filtres | Origine · famille produit (visuels · sans logique custom) |
| Toolbar | Compteur 12 produits · tri (select natif) |
| Grille | 4 col desktop · prix · origine · familles · badges |
| Réassurance | Livraison · paiement · producteurs · expédition |
| Signal Pro | Bandeau discret → professionnels.html |

---

## 4. Catégorie (`categorie.html`)

Collection type : **Épicerie créole**

| Bloc | Contenu |
|------|---------|
| Fil d’Ariane | Accueil · Shop · Épicerie créole |
| Hero éditorial | Intro courte · tags origines · usages |
| Guide achat | Bloc « Comment choisir ? » origine / usage |
| Grille | 7 produits collection · lien fiche type (confiture) |
| Réassurance | 4 preuves compactes |
| Signal Pro | Discret · qualification |

---

## 5. Classes d’arbitrage — première lecture Lot 2

| Classe | Éléments |
|--------|----------|
| **V1 prioritaire** | Grille shop native · prix TTC · catégorie Odoo · chips origine · breadcrumb · réassurance |
| **V1 possible** | Pills collections · filtres visuels · tri select · intro éditoriale catégorie |
| **V1 différée** | Filtres interactifs · pagination · facettes avancées · collections multiples pages |
| **Réserve** | Filtres origine = attributs produit ou tags · tri = natif website_sale |
| **Hors scope** | Catalogue parallèle · filtres AJAX · search custom |

---

## 6. Documents mis à jour

| Document | Action |
|----------|--------|
| [`CADRAGE_MAQUETTE_CK_V1_2_X.md`](./CADRAGE_MAQUETTE_CK_V1_2_X.md) | Pages Lot 2 · blocs · parcours · concepts |
| [`artifact/ck-maquette.css`](./artifact/ck-maquette.css) | Styles shop · catégorie |
| [`artifact/index.html`](./artifact/index.html) | Liens Lot 2 |

---

## 7. Suite MOA

```text
1. ✅ GO MOA Lot 2
2. ✅ Production artifact Lot 2 — ce document
3. ✅ Recette QA maquette Lot 2 — OK
4. ☐ Verdict MOA · arbitrage classes
5. ☐ Lot 3+ ou reprise Odoo — post-arbitrage
```

---

*Livraison Dev maquette CK V1.2.x Lot 2 · 2026-06-13.*
