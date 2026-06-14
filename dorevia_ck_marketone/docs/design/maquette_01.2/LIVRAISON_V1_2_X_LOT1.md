# Livraison Dev — Maquette CK V1.2.x · Lot 1

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **GO MOA** | [`go_moa_maquette_v1_2_x_lot1.md`](./go_moa_maquette_v1_2_x_lot1.md) |
| **Date livraison** | 2026-06-13 |
| **Statut** | **Lot 1.1 livré Dev** — correctifs QA · [`§7`](#7-correctifs-lot-11) |

```text
ODOO EN PAUSE — AUCUNE TRADUCTION ODOO EXÉCUTÉE
```

---

## 1. Artifact HTML livré

| Page | Fichier | URL locale (serveur statique) |
|------|---------|-------------------------------|
| Accueil enrichie | [`artifact/index.html`](./artifact/index.html) | `http://127.0.0.1:8766/index.html` |
| Fiche produit type | [`artifact/fiche-produit.html`](./artifact/fiche-produit.html) | `…/fiche-produit.html` |
| Professionnels | [`artifact/professionnels.html`](./artifact/professionnels.html) | `…/professionnels.html` |
| Styles partagés | [`artifact/ck-maquette.css`](./artifact/ck-maquette.css) | — |

**Test local** : depuis `artifact/`, servir le dossier (`python3 -m http.server 8766`).

---

## 2. Enrichissements Lot 1

### Accueil (`index.html`)

- Visuels quasi-réels (Unsplash) : hero · 6 produits · coffret
- Copy MOA : promesse · réassurance · double cible Pro · éditorial
- Liens inter-pages maquette (accueil ↔ fiche ↔ pro)
- Routes Odoo conservées en hints (`/shop`, `/shop/category/…`) — Lot 2 pour shop/catégorie
- Fiche produit type accessible depuis « Confiture goyavier »

### Fiche produit (`fiche-produit.html`)

Produit type : **Confiture goyavier · Réunion · 8,90 €**

Blocs matérialisés :

| Bloc | Contenu |
|------|---------|
| Achat | Galerie · prix TTC · quantité · panier · confiance mini |
| Origine & usage | Terroir · saveur · texture · usages |
| Producteur | Atelier Les Hauts Goyaviers · sélection CK |
| Conservation | Avant / après ouverture |
| Associations | 3 produits complémentaires |
| Idée recette | Clafoutis créole au goyavier |
| Signal B2B | Bandeau pro · CTA qualification |
| Cross-sell | 3 produits « Vous aimerez aussi » |

### Professionnels (`professionnels.html`)

- Hero double entrée (producteur / distributeur)
- Double cible : 2 cartes détaillées + listes critères
- Process qualification en 3 étapes
- Réassurance logistique / relation / sélection / réseau
- Formulaire mock aligné `website_crm` → `crm.lead`
- Note qualification (pas de commande B2B en ligne)

> Maquette = **cible UX enrichie**. Instance Odoo `/professionnels` conservée comme preuve faisabilité — pas copiée pixel-perfect.

---

## 3. Documents complétés

| Document | Action |
|----------|--------|
| [`CADRAGE_MAQUETTE_CK_V1_2_X.md`](./CADRAGE_MAQUETTE_CK_V1_2_X.md) | Pages Lot 1 · blocs · concepts · classes arbitrage |
| [`TABLEAU_TRADUCTION_ODOO_V1_2_1.md`](./TABLEAU_TRADUCTION_ODOO_V1_2_1.md) | Grille enrichie Lot 1 + fiche + pro |

---

## 4. Première lecture classes d’arbitrage (synthèse)

| Classe | Éléments Lot 1 |
|--------|----------------|
| **V1 prioritaire** | Header · hero · réassurance · produits vedettes · achat fiche (prix/panier) · double cible Pro · formulaire CRM |
| **V1 possible** | Bloc producteur fiche · étapes process Pro · coffret home · badges produit |
| **V1 différée** | Associations fiche · idée recette · cross-sell · page shop/catégorie (Lot 2) |
| **Réserve** | Fiche fournisseur Odoo dédiée · blog/recettes · univers Artisanat |
| **Hors scope** | Portail B2B · checkout pro · catalogue parallèle |

---

## 5. Responsive 390 px

Contrôles Dev (preview) :

- Burger menu · pas d’overflow horizontal observé
- Ordre mobile accueil : hero → réassurance → produits → catégories → coffret → pro → éditorial
- Fiche produit : colonne unique · CTA panier full-width
- Pro : cartes empilées · formulaire une colonne

Recette formelle : [`recette_qa_maquette_v1_2_x.md`](./recette_qa_maquette_v1_2_x.md) — **OK Lot 1.1**.

**Rapport MOA PDF** : [`rapport/RAPPORT_MOA_MAQUETTE_CK_V1_2_X_LOT1.pdf`](./rapport/RAPPORT_MOA_MAQUETTE_CK_V1_2_X_LOT1.pdf)

---

## 6. Suite MOA

```text
1. ✅ GO MOA Lot 1
2. ✅ Production artifact HTML Lot 1 — ce document
3. ✅ Recette QA maquette Lot 1.1 — OK
4. ✅ Rapport MOA PDF — rapport/RAPPORT_MOA_MAQUETTE_CK_V1_2_X_LOT1.pdf
5. ✅ GO Lot 2 — [`LIVRAISON_V1_2_X_LOT2.md`](./LIVRAISON_V1_2_X_LOT2.md)
6. ☐ Reprise Odoo post-arbitrage — en pause
```

---

## 7. Correctifs Lot 1.1 (post-QA MOA)

| # | Réserve QA | Correction Dev | Statut |
|---|------------|----------------|--------|
| 1 | Image principale fiche produit · Unsplash 404 | URL remplacée (`photo-1551024506`) · audit autres visuels accueil (crackers · savon) | ✅ |
| 2 | Tags `.arbitrage-tag` visibles en démo | Masqués via CSS · HTML conservé pour cadrage MOA | ✅ |

**Preview** : `http://127.0.0.1:8766/fiche-produit.html`

---

*Livraison Dev maquette CK V1.2.x Lot 1 · 2026-06-13 · Lot 1.1 2026-06-13.*
