# Ticket Dev — Fiche produit CK · Renforcement confiance & conversion V1

| Champ | Valeur |
| --- | --- |
| **Référence spec** | [`SPEC_UX_FICHE_PRODUIT_RENFORCEMENT_CONFIANCE_V1.md`](./SPEC_UX_FICHE_PRODUIT_RENFORCEMENT_CONFIANCE_V1.md) |
| **Modules impactés** | `dorevia_ck_marketone_content` · `dorevia_ck_theme` |
| **Version cible content** | `19.0.1.55.0` |
| **Version cible theme** | `19.0.1.81.0` |
| **Date ticket** | 27 juin 2026 |
| **Statut** | ✅ Livré |
| **Priorité** | Normale |

---

## Périmètre

Cinq points UX sur la fiche produit CK B2C — renforcement confiance et conversion sur Manio Crackers (produit pivot).

| ID | Section spec | Type | Fichiers |
| --- | --- | --- | --- |
| S1 | Encart Allergènes | CSS | `product_page.scss` |
| S2 | Lien Producteur focus/hover | CSS | `product_page.scss` |
| S3 | Micro-copy réassurance CTA | Template + CSS | `website_sale_product_page.xml` (theme) + `product_page.scss` |
| S4 | Galerie — thumbnails | CSS | `product_page.scss` |
| S5 | Bloc Recommandations | Python + Template + CSS | `product_template.py` + `website_sale_product_page.xml` (x2) + `product_page.scss` |

---

## S1 — Encart Allergènes

**Fichier :** `dorevia_ck_theme/static/src/scss/product_page.scss`

Override CSS pour `.ck-product-page__section--allergens` dans le bloc composition :
- Fond `#fff5f0`, bordure `#f0d5c8`
- Label "ALLERGÈNES" en `$ck-primary` avec icône `🌾` `::before`
- `padding: 16px`, `border-radius: 8px`
- Encart masqué si `ck_allergens` vide (géré côté Python — déjà ok)

---

## S2 — Lien Producteur Zone Haute

**Fichier :** `dorevia_ck_theme/static/src/scss/product_page.scss`

`.ck-product-purchase__meta-link` — compléments WCAG :
- `focus-visible { outline: 2px solid $ck-primary; outline-offset: 2px; border-radius: 2px; }`
- Zone tactile mobile ≥ 44 px : `padding-block: 0.55rem` si `max-width < 767px`

Le hover/color et scroll smooth sont déjà implémentés (Note 08).

---

## S3 — Micro-copy Réassurance CTA

**Fichier :** `dorevia_ck_theme/views/website_sale_product_page.xml` (template `product_ck_terms_fr`)

Ajout d'une ligne compacte AVANT la liste bullets existante :
```
Paiement sécurisé · Livraison suivie · Expédié depuis Nantes
```
CSS : `.ck-product-purchase__trust-strip` — `font-size: 0.75rem`, `color: $ck-text-muted`, `text-align: center`.

---

## S4 — Galerie Front

**Fichier :** `dorevia_ck_theme/static/src/scss/product_page.scss`

Style des thumbnails du carrousel natif Odoo (`#o-carousel-product`) dans `.ck-product-layout__gallery` :
- Thumbnails `80×80 px`, `border-radius: 4px`, bordure active `$ck-primary`
- `gap: 8px`, `margin-bottom: 12px`
- Transition `opacity 0.3s ease` sur l'image principale

---

## S5 — Bloc Recommandations

### Python — `dorevia_ck_marketone_content/models/product_template.py`

Nouvelle méthode `get_ck_related_products()` :
- Domaine : `is_published + sale_ok + id != self.id`
- Priorité 1 : même producteur (`ck_producer_id`)
- Priorité 2 : même catégorie (`public_categ_ids`)
- Retourne `product.template` recordset, 4 max, seulement si ≥ 2 trouvés

### Template — `dorevia_ck_marketone_content/views/website_sale_product_page.xml`

Ajout du `t-set` :
```xml
<t t-set="ck_related_products" t-value="product.get_ck_related_products()"/>
```

### Template — `dorevia_ck_theme/views/website_sale_product_page.xml`

Bloc `ck-product-page__recommendations` après `ck-product-page__pro-gateway` dans `product_ck_long_zone`.
Cards avec image + nom + méta-ligne (via `get_ck_shop_card_metadata_line()`).
Scroll horizontal, snap mobile, 4 cards max, masqué si < 2 produits.

### CSS — `product_page.scss`

`.ck-product-page__recommendations-*` : conteneur flex overflow-x, cards 200/160 px, image 160/120 px.

---

## Critères d'acceptation

- [ ] Encart allergènes → fond chaud distinct, non affiché si champ vide (Manio Crackers : affiché ✓)
- [ ] Lien SARL La Platine → hover orange ✓ · focus outline visible ✓ · zone tactile ≥ 44 px mobile
- [ ] Ligne compacte "Paiement sécurisé · Livraison suivie · Expédié depuis Nantes" visible sous CTA
- [ ] Galerie → thumbnails actifs avec bordure orange si ≥ 2 images BO
- [ ] Bloc recommandations → masqué si 0–1 produit similaire ; affiché si ≥ 2 ; scroll horizontal fluide mobile
- [ ] Manio Crackers auto-exclu de ses recommandations
- [ ] `pass: true` sur `ck_note08_recette_qa.mjs` après modifications
- [ ] 0 régression tests suites Lot 2 + Note 08

---

## Non périmètre (V2+)

- Lightbox galerie plein écran
- Flèches navigation recommandations desktop
- Prix barrés / "Indisponible" dans recommandations
- Icônes cadenas/camion micro-copy
- Contenu dynamique micro-copy depuis BO
