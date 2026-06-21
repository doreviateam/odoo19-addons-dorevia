# Acte MOA — Validation V1 Card Produit CK Home / Boutique

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-06-18 |
| **Périmètre** | Socle `ck-product-card` — Home Section 3 + grille Boutique |
| **Instance recette** | `dorevia_ck_marketone_01` |
| **Module content** | `dorevia_ck_marketone_content` `19.0.1.25.19` |
| **Module thème** | `dorevia_ck_theme` `19.0.1.33.1` |
| **Référence technique** | `product_card.scss` · `website_sale_product_card.xml` · `home_featured.py` · `get_ck_shop_card_metadata_line` |

---

## Périmètre

Validation du socle de card produit CK sur les vues :

- Home — section « Nos coups de cœur » ;
- Boutique — grille produits.

---

## Décisions MOA validées

La card produit CK repose désormais sur un socle commun `ck-product-card`, avec variantes contextuelles :

- Home : card de découverte, double CTA `Ajouter au panier` + `Voir le produit`.
- Boutique : card d'achat rapide, CTA unique `Ajouter au panier`.
- Boutique : cœur favori conservé via wishlist Odoo standard.
- Home : cœur favori absent pour ne pas surcharger la mise en avant éditoriale.
- Badge `Nouveau !` harmonisé orange CK, positionné en haut gauche.
- Ligne meta homogène Home / Boutique : catégorie ou famille · poids/format · prix de référence si disponible.

---

## Points validés

- Structure visuelle commune : padding, radius, ombre.
- Classes BEM partagées.
- Ligne meta affichée sur Home et Boutique.
- Badge `Nouveau !` harmonisé.
- CTA différenciés selon le contexte.
- Clic image / titre vers fiche produit prévu dans les deux contextes.
- Logique prix, variantes et panier non modifiée.
- Header, footer, filtres, recherche et tri non impactés.

---

## Couverture de tests

Tests automatisés : **25/25 OK**

Tags concernés :

- `dorevia_ck_shop_card`
- `dorevia_ck_marketone_home_section3`
- `dorevia_ck_marketone_card_markers`

Aucun échec constaté.

---

## Points de PV manuel optionnels

Pour un dossier QA complet, une passe manuelle peut encore cocher :

- absence de chevauchement badge / cœur / image ;
- clic wishlist Boutique et vérification compteur ;
- ajout / retrait panier en navigation réelle ;
- rendu desktop ≥ 1280 px ;
- rendu mobile < 400 px ;
- lisibilité de la ligne meta mobile ;
- utilisabilité du CTA mobile ;
- absence de régression visuelle Home / Boutique après hard refresh.

---

## Verdict MOA

```text
OK recette MOA — Card produit CK Home / Boutique validée V1.
```

Le socle `ck-product-card` est considéré comme **stable** pour la suite.

Les contrôles visuels / mobile / wishlist restants relèvent d'une passe PV manuelle complémentaire et **ne bloquent pas** la validation V1 du socle card.

---

## Suite

Chantier suivant identifié : **environnement Boutique** (titre, filtres, catégories rapides, recherche, tri, largeur de grille, rythme vertical) — sans rouvrir le rendu des cards.
