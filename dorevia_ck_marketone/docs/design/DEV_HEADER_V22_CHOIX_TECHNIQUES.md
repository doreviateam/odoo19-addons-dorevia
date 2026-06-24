# Header CK V2.2 — choix techniques Dev

Référence MOA : `SPEC_HEADER_MEGA_MENUS_CK_V2_2.md`
Ticket : `TICKET_DEV_HEADER_MEGA_MENUS_CK_V2_2.md`

## Modules

| Périmètre | Module |
| --- | --- |
| Chrome header N1/N2, SCSS, JS scroll | `dorevia_ck_theme` |
| Navigation N3, mega-menus, bloc visuel BO | `dorevia_ck_marketone_content` |

## Navigation N3

- Sync centralisée dans `nav_sync.py` (V2.2) — remplace Nav-Shop V2.1 + mega « Découvrir ».
- 9 entrées figées MOA avec classes CSS de groupe (`ck-nav-n3-rayon`, `ck-nav-n3-selection`, `ck-nav-n3-relation`).
- `Découvrir` et `Nos univers` (mobile) supprimés de la racine N3.

## Mega-menus produit

- HTML 4 colonnes généré à la sync (`nav_mega_menu.py`) et stocké dans `website.menu.mega_menu_content` (mécanisme natif Odoo CE).
- Desktop : grille 4 colonnes ; mobile : accordéon Bootstrap (`d-lg-none`) sans colonne visuelle.
- Colonne 1 : familles = sous-catégories `product.public.category` éligibles (produits publiés uniquement).
- Colonne 2 : sélections = tags produit (`/shop?tags={id}`) ou recherche fournisseur.
- Colonne 3 : origines = attribut « Origines » (`/shop?attrib={attr}-{value}`).
- Colonne 4 : bloc visuel BO `ck.mega.menu.visual.block` (séquence + fenêtre dates).

## Règles conditionnelles

| Règle | Implémentation |
| --- | --- |
| Familles vides masquées | Filtrage à la génération mega-menu |
| Boissons fraîches | `ir.config_parameter` `ck.nav.boissons_fraiches_enabled` |
| Artisanat mega | Activé si ≥ 3 familles alimentées |
| Coffrets mini-dropdown | Si ≥ 3 angles tag prêts, sinon lien direct `coffret` |
| Coups de cœur | Lien direct tag `coup_de_coeur` (fallback catégorie racine) |

## URLs adaptées Odoo 19 CE

| Intention MOA | URL réelle |
| --- | --- |
| `/shop?tag=coup_de_coeur` | `/shop?tags={product.tag.id}` |
| Filtre origine | `/shop?attrib={attribute_id}-{value_id}` |
| Catégorie famille | `/shop/category/{slug}` |
| Espace pro | `/professionnels#{ancre}` |
| Nos producteurs | `/nos-producteurs` (page CMS seed) |

## Header chrome

- Bandeau promesses : 4 items MOA, masqué au scroll via `ck_header_v22.js` (hors sticky `header#top`).
- Baseline desktop : `épicerie créole` sous logo typographique.
- Panier : icône + libellé « Panier » (xl+).

## Mega-menu desktop — correctif layout (19.0.1.41.0)

Bug : `#top_menu .dropdown-menu { max-width: 320px }` s’appliquait aussi à `.o_mega_menu`.

Correctifs SCSS :

- `:not(.o_mega_menu)` sur le cap dropdown simple ;
- `.o_mega_menu:has(.ck-mega-menu)` — `max-width: $ck-container-max`, centrage ;
- `.ck-mega-menu__col` — slots 25 % (grille 4 colonnes).

Le seed pauvre aggrave le symptôme visuel (peu de colonnes peuplées) mais **n’était pas la cause** du plafond 320 px.

## Mega-menu desktop — stabilisation hover (19.0.1.43.0)

Bug : après correction de l’ancrage vertical sous N3, le panneau pouvait se fermer pendant la traversée pointeur entre l’entrée N3 et le contenu du mega-menu.

Correctifs :

- `margin-top: 0` sur `.o_mega_menu:has(.ck-mega-menu)` pour supprimer la zone morte verticale ;
- interaction JS `ck_header_mega_menu_hover_bridge` dans `ck_header_v22.js` ;
- maintien du dropdown si le pointeur reste dans le rectangle entrée N3 + panneau ;
- fermeture différée courte seulement en sortie réelle de cette zone.

Recette automatisée : `ck_h22_recette_qa.mjs` contrôle `mega_hover_bridge.pass: true` en traversant Épicerie jusqu’au lien `Guadeloupe`.

## Mega-menu desktop — rafraîchissement hover horizontal (19.0.1.45.0)

Bug : en balayant les rayons N3 de droite à gauche puis dans l’autre sens, plusieurs panneaux pouvaient rester ouverts ou le contenu affiché ne correspondait pas toujours au dernier item survolé.

Correctifs `ck_header_v22.js` :

- suivi d’un `activeRecord` unique pour les rayons mega-menu ;
- fermeture forcée des autres panneaux à chaque entrée sur un nouveau rayon ;
- nettoyage explicite des classes `.show` sur item, panneau, toggle et `aria-expanded=false` ;
- maintien du hover bridge uniquement sur le rayon actif.

Recette automatisée : `ck_h22_recette_qa.mjs` contrôle `mega_hover_switch.pass: true` sur la séquence `Épicerie → Boissons → Maison & Bien-être → Boissons → Épicerie`.

## P3 pilote — surfaces header et fallback éditorial (19.0.1.44.0 / 19.0.1.30.0)

Objectif : renforcer la perception « boutique mature » sans modifier l’architecture MOA.

Changements `dorevia_ck_theme` :

- N3 portée par une bande full-bleed `$ck-bg-soft` sur desktop ;
- `z-index: 0` sur `.ck-header__nav-row` pour créer le contexte d’empilement local du pseudo-élément ;
- bouton de recherche en aplat `$ck-primary`.

Changements `dorevia_ck_marketone_content` :

- `_visual_column()` génère un fallback éditorial CK quand aucun `ck.mega.menu.visual.block` actif n’est saisi ;
- copie fallback par rayon (`Épicerie créole`, `Boissons créoles`, `Maison & Bien-être`, `Artisanat créole`) ;
- migration `19.0.1.30.0` : re-sync navigation pour régénérer les contenus mega-menu.

Recette visuelle : `P3_RECETTE_VISUELLE_HEADER_V22.md`.

## Recette

- Tests : tag `dorevia_ck_header_v22` + mise à jour `dorevia_ck_theme_phase10` / `dorevia_ck_marketone_nav_sync`.
- Migration `19.0.1.29.0` : re-bootstrap navigation + page `/nos-producteurs`.
- Migration `19.0.1.30.0` : re-sync navigation avec fallback éditorial colonne 4.
