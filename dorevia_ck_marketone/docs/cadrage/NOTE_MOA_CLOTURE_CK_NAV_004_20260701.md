# Note MOA — Clôture CK-NAV-004 — Centrage desktop navigation N3

| Champ | Valeur |
| --- | --- |
| Date | 1 juillet 2026 |
| Projet | C-Kréyòl Marketone — navigation header |
| Destinataires | MOA, Produit, QA, Dev |
| Statut | **GO recette / GO commit / GO push** |
| Commit de référence | `c01a2be7` — `feat(ck-nav): CK-NAV-004 centrage desktop navigation N3` |
| Module | `dorevia_ck_theme` |
| Version livrée | `19.0.1.112.0` |
| Base recette | `dorevia_ck_marketone_01` — http://localhost:18079 |

---

## Décision MOA confirmée

Après NAV-003 (navigation catalogue dynamique sans classes `ck-nav-*`), la bande N3 desktop doit **centrer** les items de navigation au lieu de les aligner à gauche.

Doctrine validée :

- Desktop **≥ 992 px** : items `Boutique · [catégories] · Producteurs · Professionnels` centrés dans la bande N3.
- Mobile **< 992 px** : inchangé — la règle est scoped dans `@media (min-width: 992px)`.
- Dropdowns Bootstrap : positionnés en absolu relative à leur `<li>` parent, indépendants du `justify-content` du conteneur flex.
- Le mécanisme `margin-left: auto` V2.2 (`:has(.ck-nav-n3-group-end)`) ne se déclenche plus sans classes legacy — le centrage est sans effet de bord.

---

## Livraison technique

Changement minimal — une ligne SCSS + bump version :

| Fichier | Modification |
| --- | --- |
| `website_header.scss:293` | `justify-content: flex-start !important` → `center !important` sur `#top_menu.top_menu` |
| `__manifest__.py` | `19.0.1.111.0` → `19.0.1.112.0` |

**Pourquoi c'est aussi simple :** Odoo QWeb ajoute déjà `justify-content-center` (Bootstrap, `!important`) sur `#top_menu`. La règle `flex-start !important` existait pour contrecarrer Bootstrap (requis en V2.2 avec le groupe secondaire poussé à droite). En NAV-003, on rejoint le comportement Bootstrap au lieu de le contredire.

---

## Recette

Contrôles effectués sur `c01a2be7`.

| Contrôle | Résultat |
| --- | --- |
| Upgrade `-u dorevia_ck_theme` | OK, sans exception bloquante |
| Version DB `dorevia_ck_theme` | `19.0.1.112.0` |
| Tests `dorevia_ck_nav_catalogue,dorevia_ck_nav_v1,dorevia_ck_phase10_header,dorevia_ck_header_v22` | 50 post-tests, 0 failed, 0 error |
| CSS compilé `web.assets_frontend.min.css` | `#top_menu.top_menu { justify-content: center !important }` — pas de `flex-start` résiduel |
| HTML desktop `/shop` | Nav complète : `Boutique · Épicerie · Soin & Bien-être · Artisanat · Boissons · Producteurs · Professionnels` |
| Dropdowns Bootstrap | `Épicerie`, `Artisanat`, `Boissons` — enfants L2 directs |
| Legacy `Communauté` / `Espace pro` | Absents |
| Classes `ck-nav-*` sur items nav | Absentes |
| Mobile offcanvas (structure HTML) | Accordéon `Épicerie` → L2 uniquement ; `Producteurs` / `Professionnels` en liens plats |
| Logs Odoo `dorevia_ck_marketone_01` | Aucune erreur bloquante constatée |

### Limite recette

Centrage visuel desktop non mesuré en pixels (pas de capture viewport). Validé via règle CSS compilée + classes Bootstrap QWeb (`justify-content-center` sur `#top_menu`). Structure mobile validée via HTML offcanvas ; le centrage desktop n'impacte pas le menu hamburger (`d-none d-lg-flex` / offcanvas).

---

## Verdict final

**CK-NAV-004 est clôturé en GO.**

Lot minimal, techniquement et fonctionnellement aligné avec NAV-003 : navigation catalogue centrée en desktop, mobile inchangé, sans régression header.
