# Livraison — Maquette CK V1.1 (corrections QA + arbitrages MOA)

| Champ | Valeur |
|-------|--------|
| **Ticket** | `ticket_dev_maquette_01_open_design` |
| **Suite de** | `LIVRAISON.md` (V1) · `recette_qa_maquette_01.md` |
| **Date** | 2026-06-12 |
| **Artefact** | `/Users/doreviateam/open-design/.od/projects/ck-marketone-maquette-v1/index.html` |
| **URL test** | `http://127.0.0.1:8765/index.html` |

---

## Corrections appliquées

| Réserve QA / MOA | Correction V1.1 |
|------------------|-----------------|
| Quick-add `+` ambigu | Bouton texte **« Voir »** (`card-cta`) + `aria-label` uniforme |
| Texte « ajout au panier en un clic » | Reformulé : accès rapide au produit puis achat depuis la fiche |
| Burger mobile inactif | Menu mobile drawer (Accueil, Boutique, Catégories, Professionnels) |
| Produits liés non responsive | Classe `.related-grid` : 3 → 2 → 1 colonnes |
| Note JS « filtres/panier » | **« JS filtres/quantité = démo uniquement »** |
| Catégories peu lisibles | Arborescence sidebar + univers accueil ; note `product.public.category` |
| Savon vétiver | Conservé — chip **Maison & bien-être · Savons** |

---

## Arbitrages MOA intégrés

```text
Palette corail #D84315 + vert #2E7D4F     → validée base V1 (pas DA finale)
Fraunces + DM Sans                        → validées maquette
Périmètre produit                         → agro-transformation créole (pas strictement alimentaire)
Savon vétiver                             → conservé, catégorie Maison & bien-être
Quick-add                                 → non retenu phase 1 — action « Voir » uniquement
Packs                                     → 1 produit / 1 carte / 1 prix en maquette
Origines / collections / filtre prix      → visibles, source Odoo à trancher
Entrée pro                                → signal / formulaire, pas portail
```

---

## Hors périmètre (inchangé)

```text
Pas d’Odoo · pas de base dev · pas de dorevia_ck_theme · pas de QWeb/SCSS
Pas de reprise dorevia_ckreyol_marketone
```

---

## Suite

```text
1. QA — passe courte V1.1
2. Si OK → revue Dev traduisibilité Odoo
3. Grille thème / template / extension
4. Décision levée verrou Odoo
```
