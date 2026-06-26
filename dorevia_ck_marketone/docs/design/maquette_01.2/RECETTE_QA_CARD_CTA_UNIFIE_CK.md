# Recette QA — Cards Produit CK · CTA unifié Home / Boutique

| Champ | Valeur |
| --- | --- |
| Date | 26 juin 2026 |
| Ticket | [`TICKET_DEV_CARD_CTA_UNIFIE_CK.md`](../../cadrage/TICKET_DEV_CARD_CTA_UNIFIE_CK.md) |
| Instance | `dorevia_ck_marketone_01` · `http://localhost:18079` |
| Modules cibles | `dorevia_ck_theme` ≥ **19.0.1.65.0** (correctif responsive CTA + grille) |
| Prérequis | Note 07 livrée et stable · Axe C clôturé |
| Viewports | Desktop **1280 px** · Tablette **800 px** · Mobile **390 px** |
| Statut | **GO technique QA** — voir [`RECETTE_QA_CARD_CTA_UNIFIE_VERDICT.md`](RECETTE_QA_CARD_CTA_UNIFIE_VERDICT.md) |

---

## 1. Objectif recette

Valider que le CTA des cards catalogue est un **bouton texte « Ajouter au panier »** visuellement aligné sur la Home, sans régression layout Note 07 ni fonctionnelle panier / wishlist.

**Critère de succès global** : un visiteur ne distingue plus deux grammaires CTA entre Home et Boutique.

---

## 2. Préparation

| Étape | Action |
| --- | --- |
| P1 | Mettre à jour modules (`-u dorevia_ck_theme`) |
| P2 | Redémarrer worker Odoo |
| P3 | Hard refresh (`Cmd+Shift+R`) ou navigation privée |
| P4 | Comparer avec captures **avant** si fournies par le Dev |

**URLs de référence** (slugs sandbox — confirmer si différents) :

| Page | URL |
| --- | --- |
| Home | `/` |
| Boutique | `/shop` |
| Épicerie (riche) | `/shop/category/epicerie-creole-1` |
| Boissons (pauvre) | `/shop/category/boissons-2` |
| Recherche | `/shop?search=manioc` (ou terme avec résultats) |

---

## 3. Checklist — CTA unifié

### 3.1 Desktop 1280 px

| # | Scénario | Attendu | OK |
| --- | --- | --- | --- |
| C1 | Home — section « Nos coups de cœur » | Bouton pill terre cuite **Ajouter au panier** — **référence visuelle** | ☐ |
| C2 | `/shop` — première card | Même grammaire CTA que C1 (texte visible, pas icône ronde seule) | ☐ |
| C3 | `/shop` — toutes les cards | Aucune card avec icône panier 38×38 px comme CTA principal | ☐ |
| C4 | Épicerie — grille | CTA texte identique à `/shop` | ☐ |
| C5 | Boissons — 1 produit | Card compacte, CTA texte lisible, pas de ligne vide | ☐ |
| C6 | Recherche active | Cards résultats = même canon CTA | ☐ |
| C7 | `/shop` desktop 1280 px | **4 cards visibles par rangée** (si ≥ 4 produits dans la page) | ☐ |
| C8 | Épicerie desktop | Idem — 4 colonnes max sur la première rangée | ☐ |

### 3.2 Grille — densité horizontale

| # | Scénario | Attendu | OK |
| --- | --- | --- | --- |
| G1 | Home — Coups de cœur | 4 colonnes desktop (référence) | ☐ |
| G2 | `/shop` — `--o-wsale-ppr` ou équivalent | Valeur **4** dans le HTML / style grille | ☐ |
| G3 | Tablette 800 px | 2 colonnes | ☐ |
| G4 | CTA texte à 4 colonnes | Bouton lisible, pas de troncature critique | ☐ |

### 3.3 Mobile 390 px

| # | Scénario | Attendu | OK |
| --- | --- | --- | --- |
| M1 | `/shop` | 1 colonne · pas d’overflow horizontal | ☐ |
| M2 | `/shop` — CTA | Bouton texte lisible · zone cliquable confortable (≥ 44 px hauteur) | ☐ |
| M3 | Catégorie pauvre | Card + CTA sans chevauchement prix/bouton | ☐ |
| M4 | Home | Inchangée vs référence pré-livraison | ☐ |

---

## 4. Checklist — Structure card

| # | Élément | Attendu | OK |
| --- | --- | --- | --- |
| S1 | Image | Ratio carré, pas de régression zoom hover | ☐ |
| S2 | Badge | Visible haut-gauche si produit badgé (ex. Nouveau, Bio) | ☐ |
| S3 | Wishlist | Cœur haut-droite, cliquable (boutique uniquement) | ☐ |
| S4 | Origine | Eyebrow au-dessus du titre si renseignée — absent sinon | ☐ |
| S5 | Ligne méta | Catégorie/format/prix réf. si dispo — **pas de séparateur orphelin** (`·` seul) | ☐ |
| S6 | Prix | Lisible, position cohérente | ☐ |
| S7 | Prix référence | Affiché seulement si autorisé (ex. pas sur Chapeau Panama) | ☐ |
| S8 | Champs absents | Aucune ligne blanche fantôme sous titre ou au pied | ☐ |

---

## 5. Checklist — Fonctionnel

| # | Action | Attendu | OK |
| --- | --- | --- | --- |
| F1 | Clic **Ajouter au panier** depuis `/shop` | Produit ajouté · compteur header +1 | ☐ |
| F2 | Clic depuis catégorie | Idem | ☐ |
| F3 | Clic wishlist | Produit en favoris · pas de conflit avec CTA | ☐ |
| F4 | Clic titre / image | Navigation fiche produit | ☐ |
| F5 | Home — ajout panier | Toujours fonctionnel (non-régression) | ☐ |

---

## 6. Checklist — Non-régression Note 07

| # | Élément | Attendu | OK |
| --- | --- | --- | --- |
| N1 | Grille pleine largeur | Pas de sidebar desktop réapparue | ☐ |
| N2 | Toolbar | Filtrer · Recherche · Tri alignés | ☐ |
| N3 | Drawer filtres | S’ouvre et filtre correctement | ☐ |
| N4 | Bloc rebond | Présent sur Boissons (état initial) | ☐ |
| N5 | Fiche produit | `/shop/product/...` inchangée | ☐ |
| N6 | Checkout | Flux intact | ☐ |

---

## 7. Tests automatisés (gate technique)

```bash
odoo-bin -d dorevia_ck_marketone_01 --test-tags dorevia_ck_shop_card --stop-after-init
```

| Résultat | OK |
| --- | --- |
| Tous tests `dorevia_ck_shop_card` verts | ☐ |

---

## 8. Verdict

| Verdict | Condition |
| --- | --- |
| **GO** | Tous les items C*, G*, M*, F*, N* critiques cochés · tests auto verts |
| **GO avec réserves** | Écart cosmétique mineur documenté (ex. alignement desktop prix/CTA) |
| **NO GO** | Icône ronde encore visible · overflow mobile · panier cassé · régression Home |

**Réserves acceptables** : micro-écarts desktop prix/CTA en ligne si mobile validé.

**Bloquant** : CTA icône seule · ajout panier KO · overflow 390 px · régression toolbar Note 07.

---

### Verdict MOA

```text
Date    : 26 juin 2026
Verdict : GO technique QA
Version : dorevia_ck_theme 19.0.1.65.0
```

Détail : [`RECETTE_QA_CARD_CTA_UNIFIE_VERDICT.md`](RECETTE_QA_CARD_CTA_UNIFIE_VERDICT.md)

---

## 9. Annexes

| Document | Lien |
| --- | --- |
| Réponse Dev | [`note_card_cta_reponse.md`](../../cadrage/note_card_cta_reponse.md) |
| Note livraison | [`NOTE_LIVRAISON_CARD_CTA_UNIFIE_CK.md`](../../cadrage/NOTE_LIVRAISON_CARD_CTA_UNIFIE_CK.md) |
| État P2A (supersédé) | [`RECETTE_SHOP_DENSIFICATION_P2A.md`](RECETTE_SHOP_DENSIFICATION_P2A.md) |
| Recette Note 07 | [`RECETTE_QA_NOTE_07_VERDICT.md`](RECETTE_QA_NOTE_07_VERDICT.md) |
