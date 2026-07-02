# Note MOA — Clôture CK-NAV-005 — Catégories niveau 0 cliquables

| Champ | Valeur |
| --- | --- |
| Date | 2 juillet 2026 |
| Projet | C-Kréyòl Marketone — navigation header |
| Destinataires | MOA, Produit, QA, Dev |
| Statut | **GO — clôturé** |
| Modules | `dorevia_ck_marketone_content` (QWeb + tests), `dorevia_ck_theme` (SCSS) |
| Versions livrées | `dorevia_ck_marketone_content` `19.0.1.81.0`, `dorevia_ck_theme` `19.0.1.119.0` |
| Base recette | `dorevia_ck_marketone_01` — http://localhost:18079 |
| Ticket | `TICKET_DEV_NAV_CATEGORY_ROOT_LINK_CK_NAV_005.md` |

---

## Décision confirmée

Chaque catégorie racine du catalogue ayant des sous-catégories (Épicerie,
Boissons, Artisanat sur l'instance de recette) est désormais un **vrai lien**
vers sa page catégorie, en desktop comme en mobile. Le dropdown/accordéon de
sous-catégories reste disponible via un toggle séparé (chevron desktop,
bouton accordéon mobile), sans neutraliser le clic sur le libellé.

Aucune classe `ck-nav-*` n'a été ajoutée aux entrées catalogue : le split est
branché sur le champ `ck_nav_category_id` déjà posé par CK-NAV-003, pas sur
un marqueur CSS. `test_catalogue_nav_no_legacy_css` (verrou de la doctrine
NAV-002/003 « nav DB-driven sans `ck-nav-*` ») reste vert.

---

## Livraison technique

| Fichier | Modification |
| --- | --- |
| `dorevia_ck_marketone_content/views/website_nav_ck_shop_v2.xml` | Nouvelle branche desktop dans `submenu_ck_nav_shop_desktop_split` (gardée sur `ck_nav_category_id and child_id and not is_mega_menu`) ; nouveau template `submenu_ck_nav_shop_mobile_accordion_split` (bloc accordéon mobile, jusque-là non intercepté) |
| `dorevia_ck_theme/static/src/scss/website_header.scss` | Nouvelles classes `.ck-nav-mobile-catalogue-split__header/__link/__toggle` (desktop réutilise le SCSS existant `.ck-nav-universe-split__*`, aucun changement) |
| `dorevia_ck_marketone_content/tests/test_ck_nav_catalogue_split_link.py` | 3 nouveaux tests HTTP (desktop avec/sans enfants, mobile) |
| `__manifest__.py` (les deux modules) | Bump de version |

Aucune modification de `nav_sync.py` ni des données `website.menu` : seul le
rendu QWeb change.

### Pourquoi pas une simple réactivation de l'existant

Un mécanisme de split lien/toggle existait déjà (Nav-Shop V2.1), mais il est
gardé par une classe CSS (`ck-nav-desktop-universe`) que NAV-003 ne pose
jamais par choix délibéré, et côté mobile il ne couvre que les menus sans
vrais enfants `website.menu` (schéma V2.2 révolu). Réutiliser tel quel aurait
cassé `test_catalogue_nav_no_legacy_css` et laissé le mobile non corrigé —
détail dans le ticket, §0.

---

## Recette effectuée

| Zone | Résultat | Commentaire |
| --- | ---: | --- |
| Versions installées | OK | `content 19.0.1.81.0`, `theme 19.0.1.119.0` en base |
| Desktop 1280 | OK | Épicerie / Boissons / Artisanat : lien `/shop/category/...` séparé du toggle dropdown |
| Clic desktop | OK | Toggle Boissons ouvre le dropdown sans changer d'URL ; lien Boissons → `/shop/category/boissons-123` |
| Mobile 390 | OK | Drawer : lien catégorie séparé du toggle accordéon |
| Clic mobile | OK | Toggle Boissons ouvre le panneau ; lien Épicerie → `/shop/category/epicerie-1` |
| Routes catégories | OK | Épicerie, Boissons, Artisanat → HTTP 200 |
| Verrou legacy CSS | OK | Pas de `ck-nav-desktop-universe` dans le HTML rendu |
| Tests automatisés | OK | 43 post-tests, 0 failed, 0 error(s) |

### Exécution tests

La première passe a buté sur le port `8069` déjà occupé par le serveur sandbox ;
relance sur le port interne `8079` → passe complète verte. Smoke HTML post-tests :
liens/toggles NAV-005 toujours présents, 3 routes catégorie toujours en 200.

### Limite recette

Contrôle visuel (chevron, alignement pixel) non capturé en screenshot — validé
via HTML rendu + CSS déjà existant (aucun nouveau style desktop introduit).
Navigation clavier non testée par un test automatisé dédié (deux éléments
focusables distincts, lien + bouton, comportement natif du navigateur —
cohérent avec le pattern V2.1 déjà en prod).

---

## Verdict

**CK-NAV-005 est clôturé — GO exploitation.** Comportement conforme à la
règle fonctionnelle : chaque catégorie racine avec sous-catégories est
cliquable, le dropdown/accordéon reste un raccourci, aucune régression sur
Boutique/Producteurs/Professionnels ni sur les catégories sans enfant.
Recette QA finale validée le 2 juillet 2026 (desktop 1280, mobile 390, tests
automatisés 43/43).
