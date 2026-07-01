# Note MOA — Clôture CK-NAV-004 — Navigation N3 desktop (centrage + icône Boutique)

| Champ | Valeur |
| --- | --- |
| Date | 1 juillet 2026 |
| Projet | C-Kréyòl Marketone — navigation header |
| Destinataires | MOA, Produit, QA, Dev |
| Statut | **GO recette / GO commit / GO push** |
| Commits de référence | `c01a2be7` (centrage) · commit icône Boutique · `ef53451d` (note initiale) |
| Module | `dorevia_ck_theme` |
| Version livrée | `19.0.1.113.0` |
| Base recette | `dorevia_ck_marketone_01` — http://localhost:18079 |

---

## Décision MOA confirmée

Après NAV-003 (navigation catalogue dynamique sans classes `ck-nav-*`), la bande N3 desktop doit :

1. **Centrer** les items de navigation.
2. **Substituer visuellement** le libellé « Boutique » par une icône sac boutique FA4 (`fa-shopping-bag`, `\f290`), tout en conservant le texte dans le DOM pour l'accessibilité.

Doctrine validée :

- Desktop **≥ 992 px** : items centrés ; `Boutique` affiché en icône ; catégories · `Producteurs` · `Professionnels` en libellés texte.
- Mobile **< 992 px** : inchangé — texte « Boutique » conservé dans l'offcanvas.
- Dropdowns Bootstrap : positionnés en absolu relative à leur `<li>` parent.
- Aucune classe `ck-nav-*` ajoutée — compatible `test_catalogue_nav_no_legacy_css`.
- Pas de changement QWeb, Python ni migration — assets SCSS uniquement.

---

## Livraison technique

| Fichier | Modification |
| --- | --- |
| `website_header.scss:293` | `justify-content: flex-start !important` → `center !important` sur `#top_menu.top_menu` |
| `website_header.scss:302-314` | Icône Boutique desktop via `[href="/shop"]` + `::before` FA4 `fa-shopping-bag` |
| `__manifest__.py` | `19.0.1.112.0` → `19.0.1.113.0` (icône storefront) |

### Arbitrages icône Boutique

| Décision | Raison |
| --- | --- |
| `font-size: 0` (pas `display:none`) | Les AT lisent le DOM — « Boutique » reste accessible |
| `color: inherit` sur `::before` | Hover/focus du `.nav-link` hérités naturellement |
| `display: inline-block` | Reste dans le flux inline ; padding du lien = zone de clic |
| Scoped `@media (min-width: 992px)` | Mobile offcanvas garde le texte |
| Sélecteur CSS pur `[href="/shop"]` | Pas de `ck-nav-*` sur les entrées menu BO |
| `\f290` `fa-shopping-bag` FontAwesome 4 | Pas de `fa-storefront` en FA4 ; glyphe boutique distinct du panier `fa-shopping-cart` |

---

## Recette

Contrôles effectués sur `19.0.1.113.0` (centrage + icône `fa-shopping-bag`).

| Contrôle | Résultat |
| --- | --- |
| Upgrade `-u dorevia_ck_theme` | OK, sans exception bloquante |
| Version DB `dorevia_ck_theme` | `19.0.1.113.0` |
| Tests `dorevia_ck_nav_catalogue,dorevia_ck_breadcrumb_u1` | 24 post-tests, 0 failed, 0 error |
| CSS compilé — centrage | `#top_menu.top_menu { justify-content: center !important }` |
| CSS compilé — icône | `nav-link[href="/shop"] { font-size: 0 }` + `::before { content: '\f290'; font-family: FontAwesome }` |
| HTML desktop `/shop` | `<span>Boutique</span>` présent dans le DOM ; icône rendue via CSS |
| HTML mobile offcanvas | Texte « Boutique » conservé (`nav-link p-3 text-wrap`) |
| Nav complète desktop | `Boutique(icon) · Épicerie · Soin & Bien-être · Artisanat · Boissons · Producteurs · Professionnels` |
| Dropdowns Bootstrap | `Épicerie`, `Artisanat`, `Boissons` — enfants L2 directs |
| Legacy / `ck-nav-*` | Absents |
| Logs Odoo `dorevia_ck_marketone_01` | Aucune erreur bloquante constatée |

### Limite recette

Centrage et rendu icône non mesurés en pixels (pas de capture viewport). Validés via CSS compilé + structure HTML. Mobile validé via offcanvas HTML.

---

## Verdict final

**CK-NAV-004 est clôturé en GO.**

Lot minimal aligné NAV-003 : navigation catalogue centrée en desktop, icône Boutique accessible, mobile inchangé, sans régression header.
