# Micro-lot 3B — Drawer filtres boutique CK

**Date :** 2026-06-26  
**Modules :** `dorevia_ck_marketone_content` 19.0.1.52.1 · `dorevia_ck_theme` 19.0.1.77.0  
**Sandbox :** `dorevia_ck_marketone_01`

## Objectif

Réorganiser le drawer filtres `/shop` en trois sections métier (**Origines**, **Producteurs**, **Préférences**) tout en conservant le moteur natif Odoo `product.tag` (`?tags=`, checkboxes `name="tags"`, reset, desktop + mobile).

## Tags classés (données visibles filtrables)

| Groupe | Tags (si rattachés à des produits publiés) |
|--------|---------------------------------------------|
| **Origines** | Guadeloupe, Dominique (Ile), Martinique, Réunion* |
| **Producteurs** | Komla, La Platine, Rwan Ltd |
| **Préférences** | Sans Gluten, Agriculture Bio |

\* Réunion n’apparaît que si le tag est rattaché à des produits publiés dans le périmètre shop courant.

## Données modifiées (migration 52.0 / 52.1)

- Champ `product.tag.ck_shop_filter_group` : `origin` · `producer` · `preference`
- `Guadeloupe` → groupe **Origines**, `visible_to_customers = True`
- `Dominique (Ile)` → groupe **Origines** (inférence variantes avec parenthèses)
- `Agriculture Bio` → tag filtrable **Préférences** + rattachement aux produits portant le ruban homonyme
- `Bien-être` → `visible_to_customers = False` (hors drawer public)
- Tags navigation transversaux (`Épicerie`, `Artisanat`, etc.) : exclus du drawer via inférence / visibilité

## Fonctionnement du regroupement

1. Le contrôleur shop enrichit le contexte QWeb avec `ck_shop_filter_tag_groups` (sections ordonnées + état actif).
2. Seuls les tags `visible_to_customers = True` **avec** `ck_shop_filter_group` renseigné alimentent le drawer.
3. **Mobile (offcanvas)** : trois accordéons natifs, checkboxes `website_sale.filter_products_tags_list`.
4. **Desktop (sidebar)** : trois blocs titrés, mêmes checkboxes.
5. **Réinitialiser les filtres** : lien outline terre cuite sous la recherche offcanvas ; footer natif masqué.

Aucune valeur métier n’est codée en dur dans les templates.

## Limites V1

- Pas de bascule vers l’attribut produit **Origine** (chantier gouvernance catalogue séparé).
- Cohérence ruban / tag **Agriculture Bio** : migration ponctuelle ; pas de synchro automatique continue.
- Le tag `Origine: Guadeloupe` (legacy) reste visible s’il est sur des produits mais **non classé** (absent du drawer).
- Sections vides masquées : seules les sections avec tags disponibles dans le shop courant sont affichées.
- Pas de slider prix, autocomplete producteur, filtres « Nouveau » / « Coup de cœur ».

## Captures

Répertoire : `docs/design/maquette_01.2/captures/micro_lot_3b/`

- `shop_filtres_drawer_desktop_1280.png`
- `shop_filtres_drawer_mobile_390.png`
- `shop_filtres_drawer_filtre_actif_mobile_390.png`
- `shop_filtres_grille_filtree_mobile_390.png`

## Tests

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d dorevia_ck_marketone_01 \
  --test-enable --test-tags dorevia_ck_shop_filter_drawer --stop-after-init --http-port=8079
```

## Règle catalogue MOA (à maintenir en données)

> Si un produit porte le ruban `Agriculture Bio`, il doit aussi porter le tag filtrable `Agriculture Bio`.
