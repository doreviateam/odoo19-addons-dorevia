# Ticket Dev — Raffinement Cards Produit CK · CTA unifié Home / Shop / Catégories

| Champ | Valeur |
| --- | --- |
| Date | 26 juin 2026 |
| Référence UX | Pivot MOA post-Note 07 — canon Home « Nos coups de cœur » |
| Référence technique | [`note_card_cta_reponse.md`](note_card_cta_reponse.md) |
| Projet | C-Kréyòl / CK Marketone |
| Base cible | `dorevia_ck_marketone_01` · `http://localhost:18079` |
| Modules | `dorevia_ck_theme` (principal) · `dorevia_ck_marketone_content` (métadonnées card, tests) |
| Type | Raffinement UX / conversion |
| Priorité | **Haute** — **préalable** aux raffinements pages pauvres / rebond / toolbar |
| Estimation | **0,5–1 j-h Dev** + **0,5 j-h QA** |
| Statut | **GO technique QA** — clôturé `19.0.1.65.0` |
| Périmètre | Cards produit Home (référence), `/shop`, `/shop/category/...`, recherche catalogue |
| Hors périmètre | Fiche produit · checkout · BO · nouveaux champs · moteur de filtres · layout Note 07 (déjà livré) |

---

## 1. Contexte

La Note 07 a stabilisé le layout catalogue (grille pleine largeur, drawer filtres, rebond, mobile 390 px). Le lot P2A (juin 2026) avait ensuite **allégé** le CTA boutique en **icône panier ronde** (38×38 px) pour une grammaire « boutique mature » type bienmanger.com.

**Nouvelle direction MOA** : l’expérience Home et Boutique doit être **homogène**. La card de la section Home **« Nos coups de cœur »** redevient le **canon visuel et comportemental** pour toutes les grilles catalogue.

Écart principal à corriger : remplacer l’icône panier ronde seule par un bouton texte explicite **« Ajouter au panier »** (pill terre cuite, texte blanc).

```text
État actuel boutique : prix à gauche · bouton icône ronde à droite (P2A)
État cible           : même grammaire CTA que la Home — bouton texte pill
```

**Ordre de priorité produit** : ce ticket précède tout raffinement complémentaire sur les pages pauvres, le bloc de rebond ou la toolbar — on stabilise d’abord la brique card produit.

---

## 2. Objectif

> Un visiteur ne doit pas avoir à réapprendre l’interface entre la Home et la Boutique.

Uniformiser le rendu des cards produit entre la Home et les pages catalogue, sans régression sur la Home ni sur l’ajout panier natif.

---

## 3. Demande fonctionnelle

### 3.1 CTA unifié

Remplacer, dans les cards catalogue, l’icône panier ronde seule par un bouton texte :

> **Ajouter au panier**

Le bouton reprend la grammaire visuelle de la Home :

- fond terre cuite (`$ck-primary`) ;
- texte blanc ;
- forme pill (`border-radius` arrondi) ;
- hover cohérent (`$ck-primary-hover`) ;
- hauteur tactile suffisante (cible ≥ 44 px sur mobile recommandé).

### 3.2 Structure card commune

Structure homogène sur toutes les grilles produit :

1. image produit ;
2. badges si disponibles ;
3. cœur wishlist en haut à droite (boutique uniquement) ;
4. origine si disponible (eyebrow) ;
5. nom produit ;
6. ligne méta si disponible ;
7. prix ;
8. bouton **Ajouter au panier**.

### 3.3 Données optionnelles

Les champs optionnels disparaissent proprement s’ils sont absents :

- origine ;
- producteur / tags ;
- format ;
- prix de référence ;
- badge.

> Aucun séparateur orphelin, aucune ligne vide, aucun espace fantôme.

*Note : la logique `t-if` est déjà en place (Note 07 Lot D + P2A eyebrow). Ce ticket est surtout un **audit visuel** post-changement de pied de card.*

### 3.4 Prix de référence

Conserver la logique CK existante (`get_ck_shop_card_metadata_line` / `_get_featured_card_metadata_line`). Affichage uniquement si données disponibles **et** autorisation produit — ne pas forcer sur les produits où le prix réf. a été désactivé (ex. Chapeau Panama post-Axe C).

### 3.5 Responsive

Sur mobile 390 px :

- aucune rupture de layout ;
- bouton lisible, touch target suffisante ;
- aucun overflow horizontal.

Priorité : **lisibilité de la card avant densité**. Le nombre de colonnes mobile reste celui livré en Note 07 (1 colonne).

### 3.6 Grille catalogue — 4 produits à l’horizontale

Aligner la boutique sur la Home et la maquette CK (`grille 4 cols → 2 → 1`) :

| Viewport | Colonnes cible | Remarque |
| --- | --- | --- |
| Desktop ≥ 1280 px | **4** | Pleine largeur post-Note 07 (sidebar masquée) |
| Tablette ~800 px | **2** | Natif Odoo `g-col-md-6` |
| Mobile 390 px | **1** | Déjà en place (Note 07 Lot D) |

Règle produit :

> **Autant que possible**, afficher **4 cards par rangée** sur desktop lorsque la largeur container le permet. Si le CTA texte pill rend la card illisible à 4 colonnes sur un viewport donné, le Dev **descend d’un cran** (3 colonnes) plutôt que de compresser le bouton.

Implémentation pressentie : paramètre natif Odoo `website.shop_ppr = 4` (cf. pattern `dorevia_ckreyol_marketone/data/marketone_website_shop_grid.xml`) + recette visuelle post-CTA texte.

---

## 4. Contraintes

**Ne pas modifier :**

- fiche produit détaillée ;
- checkout ;
- back-office ;
- moteur de filtres ;
- logique fonctionnelle d’ajout panier (soumission native grille Odoo).

**Ne pas ajouter :**

- champ quantité dans la card ;
- nouveau champ produit ;
- nouveau modèle ;
- JavaScript custom, sauf nécessité explicitement justifiée (voir §6 Q4).

**Ne pas :**

- réécrire entièrement les templates Odoo si un héritage ciblé suffit ;
- casser la Home existante ;
- rouvrir le layout Note 07 (sidebar, drawer, rebond).

---

## 5. Implémentation pressentie (indicatif Dev)

| # | Fichier | Action attendue |
| --- | --- | --- |
| I1 | `dorevia_ck_theme/views/website_sale_product_card.xml` | Template `shop_product_buttons_ck_card` — retirer `visually-hidden` sur le libellé ; conserver `aria-label` / `title` |
| I2 | `dorevia_ck_theme/static/src/scss/website_sale.scss` | Supprimer ou inverser le bloc P2A `.card-cart-cta` 38×38 px circulaire (l. ~333–419) ; restaurer pied de card type Home (colonne mobile, pill pleine largeur ou alignement cohérent desktop) |
| I3 | `dorevia_ck_theme/static/src/scss/product_card.scss` | S’assurer que le mixin `ck-product-card-cta-cart` s’applique sur `.ck-product-card--shop` sans surcharge conflictuelle |
| I4 | `dorevia_ck_marketone_content/tests/test_ck_shop_product_card.py` | Ajouter assertion : libellé **visible** (pas seulement dans le DOM) ; corriger `test_shop_home_non_regression` si obsolète (`Voir le produit` retiré des cards home) |
| I5 | `dorevia_ck_theme/data/website_shop_grid.xml` *(nouveau)* ou migration | `website.shop_ppr = 4` sur le site CK |
| I6 | `dorevia_ck_theme/static/src/scss/website_sale.scss` *(optionnel)* | Renfort `--o-wsale-ppr: 4` scopé `.ck-shop-page` si le paramètre site ne suffit pas |
| I7 | `dorevia_ck_theme/tests/test_ck_shop_structure_s1.py` | Assertion grille : `--o-wsale-ppr: 4` ou `g-col-lg-3` sur les cards |
| I8 | Bump version | `dorevia_ck_theme` → **19.0.1.64.0** (indicatif) |

**Hors scope ticket** : état temporaire bouton « Ajouté ✓ » — non requis ; le feedback natif (toast panier + compteur header) suffit.

---

## 6. Critères d’acceptation

- [ ] `/shop` affiche des cards avec bouton texte **Ajouter au panier** (visible, pas icône seule).
- [ ] Les pages catégories affichent le même canon de card que la Home (CTA).
- [ ] L’icône panier ronde seule n’apparaît plus comme CTA principal dans les cards catalogue.
- [ ] La Home reste inchangée visuellement (pas de régression).
- [ ] Les badges restent visibles.
- [ ] Le cœur wishlist reste visible et correctement positionné (boutique).
- [ ] Le prix reste lisible et correctement positionné.
- [ ] Le prix de référence reste cohérent avec la logique CK existante.
- [ ] Aucun champ optionnel absent ne génère de ligne vide.
- [ ] Aucun séparateur orphelin dans la ligne méta.
- [ ] Mobile 390 px sans overflow horizontal.
- [ ] Le bouton reste lisible et cliquable sur mobile.
- [ ] L’ajout panier fonctionne depuis la grille (compteur header mis à jour).
- [ ] La toolbar catégorie (breadcrumb, tri, filtres) n’est pas décalée ni cassée.
- [ ] Résultats de recherche catalogue : même card unifiée.
- [ ] Desktop 1280 px : **4 cards par rangée** sur `/shop` (si ≥ 4 produits visibles).
- [ ] Tablette : 2 colonnes · mobile 390 px : 1 colonne — sans régression Note 07.

---

## 7. Livrables attendus

| Livrable | Détail |
| --- | --- |
| Commit | Message suggéré : `[UX] Uniformise la carte produit sur les grilles shop CK` |
| Note de livraison | Templates, SCSS, tests modifiés — voir [`NOTE_LIVRAISON_CARD_CTA_UNIFIE_CK.md`](NOTE_LIVRAISON_CARD_CTA_UNIFIE_CK.md) |
| Recette QA | [`RECETTE_QA_CARD_CTA_UNIFIE_CK.md`](../design/maquette_01.2/RECETTE_QA_CARD_CTA_UNIFIE_CK.md) |
| Captures avant / après | Home · `/shop` · catégorie riche · catégorie pauvre · mobile 390 px |

---

## 8. Références

| Document | Rôle |
| --- | --- |
| [`ACTE_MOA_GO_CARD_PRODUIT_CK_HOME_BOUTIQUE_V1.md`](../design/maquette_01.2/ACTE_MOA_GO_CARD_PRODUIT_CK_HOME_BOUTIQUE_V1.md) | Socle card V1 (à réaligner sur CTA texte boutique) |
| [`RECETTE_SHOP_DENSIFICATION_P2A.md`](../design/maquette_01.2/RECETTE_SHOP_DENSIFICATION_P2A.md) | État P2A **supersédé** sur le CTA (icône ronde) |
| [`RECETTE_QA_NOTE_07_VERDICT.md`](../design/maquette_01.2/RECETTE_QA_NOTE_07_VERDICT.md) | Layout catalogue — ne pas régresser |
| [`RECETTE_QA_CARD_CTA_UNIFIE_VERDICT.md`](../design/maquette_01.2/RECETTE_QA_CARD_CTA_UNIFIE_VERDICT.md) | **GO technique QA** 26/06 — version finale **65.0** |
| [`RECETTE_QA_CARD_CTA_UNIFIE_CK.md`](../design/maquette_01.2/RECETTE_QA_CARD_CTA_UNIFIE_CK.md) | Checklist recette |
| [`note_card_cta_reponse.md`](note_card_cta_reponse.md) | Réponses Dev aux 5 questions pré-implémentation |
