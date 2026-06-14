# Livraison — Maquette CK V1

| Champ | Valeur |
|-------|--------|
| **Ticket** | `ticket_dev_maquette_01_open_design` |
| **Référence** | `design_01.md` v1.1 |
| **Date** | 2026-06-12 |
| **Statut** | Livré — en attente recette QA + arbitrage David |

---

## 1. Livrables produits

| # | Livrable | Chemin |
|---|----------|--------|
| 1 | Artefact HTML Open Design | `/Users/doreviateam/open-design/.od/projects/ck-marketone-maquette-v1/index.html` |
| 2 | Tokens design | `docs/design/maquette_01/tokens.md` |
| 3 | Annotations composants → Odoo | `docs/design/maquette_01/annotation_composants_odoo.md` |
| 4 | Note choix visuels | `docs/design/maquette_01/note_choix_visuels.md` |
| 5 | Points à arbitrer | `docs/design/maquette_01/points_a_arbitrer.md` |
| 6 | Présent document | `docs/design/maquette_01/LIVRAISON.md` |

**Ouverture maquette** : ouvrir `index.html` dans un navigateur (fichier local).

---

## 2. Écrans couverts

| Écran | Section HTML | Responsive |
|-------|--------------|------------|
| Accueil | `#accueil` | Hero + CTA pleine largeur mobile |
| Boutique `/shop` | `#shop` | Sidebar → drawer &lt; 1024px ; grille 3→2→1 cols |
| Fiche produit | `#produit` | Layout 2 cols → stack mobile ; buy box + CTA visibles |

Navigation inter-écrans : barre `screen-tabs` + ancres + liens header.

**Hors périmètre** : panier tunnel, checkout, portail B2B.

---

## 3. Direction visuelle retenue

Marchande alimentaire contemporaine : fond crème `#FFFBF7`, CTA corail `#D84315`, vert confiance `#2E7D4F` pour origines. Typo Fraunces + DM Sans. Produits et prix dominants — pas galerie, pas exotisme caricatural, pas ancienne DA terracotta/sauge.

Détail : `note_choix_visuels.md`.

---

## 4. Tokens documentés

Oui — `tokens.md` (couleurs, typo, espacements, radius, ombres, grille responsive, export SCSS suggéré).

---

## 5. Composants annotés

Oui — `annotation_composants_odoo.md` (tableau §17 design_01 + statuts phase 1).

---

## 6. Points conformes au référentiel

```text
□ Trois écrans phase 1 produits
□ design_01 v1.1 respecté (promesse, B2C, B2B secondaire, réassurance)
□ Prix et CTA visibles sur cartes et fiche
□ Packs = 1 carte / 1 prix (pas explosion checkout)
□ Entrée pro = signal + CTA formulaire (pas portail)
□ Mobile : drawer filtres, grilles adaptatives, hero responsive
□ Tokens documentés
□ Aucun développement Odoo
□ JS limité à démo filtres mobile + qty (annoté non spec)
□ Données fictives explicitement
```

---

## 7. Points d’écart ou d’attention

| Point | Détail |
|-------|--------|
| Photos produit | Zones placeholder (aplats) — photos réelles en prod |
| Google Fonts | Maquette uniquement — arbitrage typo prod |
| Filtre prix UI | Visible en sidebar — traduction Odoo non figée |
| Quick-add « + » | Lien vers fiche en V1 — pas ajout panier JS |
| Badge panier « 2 » | Décoratif démo |
| Barre `screen-tabs` | Aide navigation maquette — à retirer en prod |

---

## 8. Points à arbitrer par David

Voir `points_a_arbitrer.md` — priorité : packs `non_detailed`, origines/collections source Odoo, palette V1, quick-add obligatoire ou non.

---

## 9. Limites de la maquette

```text
Données HTML fictives
Pas de panier / checkout maquettés
Filtres = démo visuelle (drawer mobile)
Pas d’état vide catalogue
Pas de variantes produit sur fiche démo
V1 arbitrage MOA — pas DA finale senior
```

---

## 10. Proposition de suite

```text
1. QA — recette maquette (checklist design_01 §22 + §24 critères observables)
2. David — arbitrage DA + points_a_arbitrer.md
3. Dev — revue traduisibilité Odoo (post-recette)
4. Loulou — formalisation grille de traduction si GO maquette
5. Décision levée verrou base Odoo / dorevia_ck_theme (cadrage_01 §27)
```

---

## Critères d’acceptation ticket (§17)

```text
✅ Les trois écrans phase 1 sont produits
✅ Cohérent avec design_01.md v1.1
✅ Produits, prix, CTA visibles
✅ Fiche produit permet de décider l’achat
✅ B2B visible mais secondaire
✅ Mobile pris en compte
✅ Tokens documentés
✅ Composants structurants annotés
✅ Pas de boutique parallèle comme cible
✅ Points à trancher listés
✅ Aucun développement Odoo
```
