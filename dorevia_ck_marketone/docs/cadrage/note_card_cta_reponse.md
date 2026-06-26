# Retour Dev / QA — Cards Produit CK · CTA unifié Home / Boutique

| Champ | Valeur |
| --- | --- |
| Date | 26 juin 2026 |
| Référence | [`TICKET_DEV_CARD_CTA_UNIFIE_CK.md`](TICKET_DEV_CARD_CTA_UNIFIE_CK.md) |
| Destinataires | Produit / UX, Lead Tech |
| Statut | **Validé faisabilité** — prêt implémentation |
| Modules actuels | `dorevia_ck_theme` **19.0.1.63.0** · `dorevia_ck_marketone_content` **19.0.1.46.0** |

---

## Synthèse

| Élément | Réponse |
| --- | --- |
| **Faisabilité** | **Oui** — correction ciblée template + SCSS, sans nouveau modèle |
| **Approche** | Inverser la décision P2A CTA icône ; réutiliser le mixin `ck-product-card-cta-cart` déjà présent pour la Home |
| **Estimation** | **0,5–1 j-h Dev** + **0,5 j-h QA** |
| **Risque principal** | Conflit SCSS entre `product_card.scss` (pill texte) et `website_sale.scss` (surcharge 38×38 px P2A) — résolu en retirant la surcharge shop |

---

## Réponses aux 5 questions pré-implémentation

### Q1 — La card Home et la card catalogue partagent-elles déjà un composant ou des classes communes ?

**Oui, partiellement — socle BEM commun, rendu divergent sur le CTA boutique.**

| Couche | Home | Boutique |
| --- | --- | --- |
| Classes racine | `ck-product-card ck-product-card--home` | `ck-product-card ck-product-card--shop` |
| SCSS socle | `product_card.scss` — mixins partagés | Idem + surcharges `website_sale.scss` |
| HTML | SSR Python `home_featured.py` → `build_featured_product_card_html` | Héritage QWeb `website_sale.products_item` |
| Métadonnées | Ligne meta combinée | Eyebrow origine + ligne secondaire via `products_item_ck_card_metadata` |
| CTA panier | `.card-cart-cta` texte visible + `ck_featured_cart_add.js` (home uniquement) | `.card-cart-cta` + classe Odoo `o_wsale_product_btn_primary` — **libellé masqué** + **SCSS icône ronde** |

Fichiers clés :

- `dorevia_ck_theme/views/website_sale_product_card.xml` — `products_item_ck_card`, `shop_product_buttons_ck_card`
- `dorevia_ck_marketone_content/views/website_sale_product_card.xml` — métadonnées shop
- `dorevia_ck_theme/static/src/scss/product_card.scss` — mixin `ck-product-card-cta-cart`
- `dorevia_ck_marketone_content/home_featured.py` — rendu home

---

### Q2 — Quel template Odoo exact porte aujourd’hui le CTA icône ronde ?

**Deux fichiers en cascade :**

1. **`website_sale.shop_product_buttons`** (natif Odoo 19) — structure bouton primaire grille.
2. **`dorevia_ck_theme.shop_product_buttons_ck_card`** — héritage CK :
   - ajoute `card-cart-cta` sur `button.o_wsale_product_btn_primary` ;
   - remplace le `span.o_label` par un libellé **`.visually-hidden`** (« Ajouter au panier »).

Le rendu icône ronde n’est **pas** dans le QWeb : il vient du SCSS shop dans `website_sale.scss` (bloc commenté « P2A allègement CTA », règles `width/height: 38px`, `border-radius: 999px`, icône `.fa-shopping-cart` visible).

Le pied de card en **ligne** prix | bouton (au lieu de colonne) est aussi imposé par ce même fichier SCSS (`.ck-product-card__foot` en `flex-direction: row`).

---

### Q3 — L’harmonisation peut-elle se faire par héritage léger, sans duplication de template ?

**Oui.**

| Action | Détail |
| --- | --- |
| QWeb | Dans `shop_product_buttons_ck_card` : retirer `visually-hidden` du `span.o_label` (ou laisser le libellé natif Odoo visible) |
| SCSS | Retirer le bloc P2A icône 38×38 px dans `website_sale.scss` ; laisser `product_card.scss` appliquer `@include ck-product-card-cta-cart` sur `.card-cart-cta` |
| Layout pied | Réaligner le pied shop sur la Home : **colonne** sur mobile (prix puis bouton pleine largeur) ; desktop optionnel en ligne via `ck-product-card-foot-desktop` si souhaité |
| JS | **Aucun** — le bouton shop conserve le comportement natif `website_sale` (soumission / interaction grille) |

Pas de nouveau template, pas de duplication du HTML home en Python.

---

### Q4 — Le comportement natif Odoo permet-il un état temporaire « Ajouté ✓ » sans JavaScript custom ?

**Non pour un swap de libellé sur le bouton lui-même.**

| Contexte | Comportement actuel |
| --- | --- |
| Home | `ck_featured_cart_add.js` — RPC `/shop/cart/add`, toast `cartNotificationService`, sync compteur header — **pas** de libellé « Ajouté ✓ » sur le bouton |
| Boutique | Interaction native Odoo 19 sur `o_wsale_product_btn_primary` — ajout panier + notifications stock / erreur natives |

**Recommandation ticket** : ne pas introduire d’état « Ajouté ✓ » sur le bouton en V1 — hors périmètre explicite, et contraire à la contrainte « pas de JS custom sauf justification ». Le feedback utilisateur repose sur :

- mise à jour du compteur panier header ;
- toast / notification panier native Odoo.

Si MOA exige un feedback in-card plus tard, s’inspirer du pattern `dorevia_ckreyol_marketone` (`shop_product_tile_conversion.xml`) — **module non installé sur la base CK**, à traiter en ticket séparé.

---

### Q5 — Quel rendu mobile recommandez-vous pour garantir la lisibilité à 390 px ?

**Recommandation Dev :**

| Zone | Rendu 390 px |
| --- | --- |
| Grille | **1 colonne** — déjà en place (Note 07) |
| Pied de card | **Colonne** : prix au-dessus, bouton **pleine largeur** en dessous |
| CTA | Pill texte « Ajouter au panier » — `min-height` ≥ 44 px, `font-size` 12–13 px |
| Prix + CTA | **Ne pas** conserver le layout P2A « prix à gauche · icône à droite » sur mobile — trop dense pour un CTA texte |
| Overflow | Vérifier `white-space: nowrap` sur le libellé : autoriser `normal` ou réduire padding si débordement sur petits libellés longs |

Desktop ≥ 768 px : le mixin `ck-product-card-foot-desktop` (déjà sur `--home`) peut être étendu à `--shop` si le MOA souhaite prix et CTA sur une même ligne — **optionnel**, secondaire à la lisibilité mobile.

---

### Q6 — Grille 4 produits à l’horizontale (complément MOA)

**Oui, faisable — alignement Home + maquette CK.**

| Zone | État actuel | Cible |
| --- | --- | --- |
| Home « Coups de cœur » | CSS Grid `repeat(4, 1fr)` — `website.scss` l. 670–681 | Inchangé (référence) |
| Boutique `/shop` | Grille native Odoo — `ppr` non configuré CK (défaut Odoo **3** colonnes lg) | **`shop_ppr = 4`** |

Odoo 19 expose le nombre de colonnes via `website.shop_ppr` → variable CSS `--o-wsale-ppr` et classes `g-col-lg-{{12 // ppr}}` (4 colonnes = `g-col-lg-3`).

**Approche recommandée (faible risque)** :

1. Fichier data CK (pattern déjà validé Marketone) :

```xml
<function model="website" name="write">
    <value eval="[ref('website.default_website')]"/>
    <value eval="{'shop_ppr': 4}"/>
</function>
```

2. Post-Note 07, `hasLeftColumn` est faux (sidebar masquée) → Odoo active le mode **4 colonnes desktop** sans conflit sidebar.
3. Recette visuelle **après** CTA texte pill : si 4 colonnes à 1280 px compriment le bouton, arbitrage Dev → garder 4 cols avec CTA compact **ou** descendre à 3 cols (priorité lisibilité ticket §3.5).

**Breakpoints attendus** (natif Odoo, cohérent maquette) :

```text
≥ lg (992 px+) : 4 colonnes (ppr=4)
md (~768–991)   : 2 colonnes
≤ 575 px        : 1 colonne (SCSS Note 07 déjà en place)
```

Pas de réécriture du template `website_sale.products` — uniquement paramètre site + éventuel renfort SCSS scopé `.ck-shop-page`.

---

## État des lieux — écart P2A vs cible

| Élément | P2A (actuel) | Cible ticket |
| --- | --- | --- |
| CTA visible | Icône panier 38×38 px | Texte « Ajouter au panier » |
| Libellé DOM | `visually-hidden` | Visible |
| Pied card | Row prix \| icône | Colonne mobile · pill Home |
| Référence UX | bienmanger.com densité | Canon Home Coups de cœur |

---

## Tests existants à adapter

Tag : `dorevia_ck_shop_card` — fichier `test_ck_shop_product_card.py`

| Test | Action |
| --- | --- |
| `test_shop_card_ctas_french` | Conserver — libellé déjà asserté dans le chunk HTML |
| `test_shop_home_non_regression` | **Corriger** — `Voir le produit` n’est plus dans le pied de card home (CTA secondaire retiré migration 33.0) ; remplacer par assertions sur `card-cart-cta` + titre cliquable |
| Nouveau (recommandé) | Vérifier absence de classe / style icône seule : pas de `visually-hidden` sur `card-cart-cta__label` dans l’arch bouton shop |

Couverture complémentaire : exécuter la recette manuelle [`RECETTE_QA_CARD_CTA_UNIFIE_CK.md`](../design/maquette_01.2/RECETTE_QA_CARD_CTA_UNIFIE_CK.md).

---

## Verdict Dev

```text
GO implémentation — lot court, faible risque, pas de migration données.
Bump theme 19.0.1.64.0 recommandé après livraison.
```
