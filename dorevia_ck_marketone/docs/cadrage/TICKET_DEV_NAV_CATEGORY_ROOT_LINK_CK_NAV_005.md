# Ticket Dev — CK-NAV-005 — Rendre les catégories niveau 0 cliquables

Statut : **GO ouverture**, prêt pour mise en place.
Relecture Dev effectuée sur le code réel (`nav_sync.py`, `website_menu.py`,
`website_nav_ck_shop_v2.xml`, template Odoo core `website.submenu`) avant
ouverture. Cette relecture a renuméroté le ticket et identifié le mécanisme
technique exact à mettre en œuvre — détaillé en §0.

Base locale : `dorevia_ck_marketone_01`
Module concerné : `dorevia_ck_marketone_content`
Version de référence avant lot : `19.0.1.80.0`
Version cible après lot : `19.0.1.81.0`

---

## 0. Corrections Dev apportées à la note MOA reçue

### 0.1 Renumérotation — CK-NAV-004 est déjà pris

La note MOA intitule ce ticket **CK-NAV-004**. Cet identifiant est déjà
clôturé (`NOTE_MOA_CLOTURE_CK_NAV_004_20260701.md`, 1ᵉʳ juillet 2026 —
centrage desktop + icône `fa-home` sur « Boutique », module
`dorevia_ck_theme`, sans rapport avec le sujet ici). **Ce ticket est donc
ouvert sous CK-NAV-005.**

### 0.2 Cause racine confirmée dans le template Odoo core

Vérifié directement dans le conteneur sandbox
(`/usr/lib/python3/dist-packages/odoo/addons/website/views/website_templates.xml`,
template `website.submenu`) : dès qu'un `website.menu` a des enfants
(`child_id`), le rendu stock Odoo produit :

- **Desktop** : `<a href="#" data-bs-toggle="dropdown">` — le `href` réel de
  la catégorie n'est jamais utilisé, seul `#` est rendu.
- **Mobile** (accordéon) : `<a href="#" class="accordion-button" data-bs-toggle="collapse">`
  — même chose, jamais de lien réel.

C'est un comportement Bootstrap/Odoo standard, pas un bug CK : confirme le
diagnostic de la note MOA et la nécessité de séparer libellé et toggle.

### 0.3 Un mécanisme de split existe déjà dans le code, mais il est éteint sur la nav actuelle

`dorevia_ck_marketone_content/views/website_nav_ck_shop_v2.xml`
(`submenu_ck_nav_shop_desktop_split`, Nav-Shop V2.1) surcharge déjà ce même
`<a data-bs-toggle="dropdown">` pour produire exactement le motif demandé
(libellé cliquable + chevron toggle séparé), avec le SCSS associé déjà en
place (`ck-nav-universe-split__link` / `__toggle`,
`website_header.scss:319-424`).

Mais ce mécanisme est conditionné à `submenu._ck_nav_is_desktop_universe()`,
c'est-à-dire à la présence de la classe CSS `ck-nav-desktop-universe`
(`website_menu.py:26-28`). Or la navigation catalogue **actuellement active**
(`sync_ck_catalogue_navigation_for_website`, CK-NAV-003) ne pose jamais cette
classe sur ses entrées — c'est une décision délibérée, verrouillée par un
test de non-régression :

```
tests/test_ck_nav_catalogue_sync.py::test_catalogue_nav_no_legacy_css
  assertFalse(any ck_nav_css_class contenant 'ck-nav-' après sync catalogue)
```

**Réutiliser tel quel le split V2.1 (en pausant la classe `ck-nav-desktop-universe`
sur les catégories NAV-003) casserait ce test et irait à l'encontre de la
doctrine NAV-002/003 « navigation catalogue DB-driven, jamais de classe
`ck-nav-*` ».** Ce n'est donc pas la bonne voie d'implémentation, même si le
symptôme visuel serait correct.

### 0.4 Le split mobile existant ne couvre pas non plus le cas présent

`submenu_ck_nav_shop_mobile_l2_leaf` (même fichier) ne s'applique qu'aux
`<li>` **sans** `child_id` (`t-if="... not (submenu.child_id or submenu.is_mega_menu) ..."`)
— pattern hérité de l'ancien schéma V2.2 où les sous-catégories du mega-menu
n'existaient pas comme vrais `website.menu` enfants (récupérées à la volée
via `ck_nav_category_id`).

Les catégories racines NAV-003, elles, ont de vrais enfants `website.menu`
(créés via `child_menus=child_specs` dans `nav_sync.py:706-731`). Sur mobile,
elles tombent donc dans le bloc **accordéon stock** d'Odoo (`website.submenu`
lignes 44-70 du template core), qui n'est intercepté par aucune surcharge CK
actuelle. **Un nouveau point d'extension QWeb est donc nécessaire côté
mobile, ce n'est pas un simple flag à activer.**

### 0.5 Voie d'implémentation retenue

Ajouter deux nouvelles branches dans `website_nav_ck_shop_v2.xml`, gardées
sur `submenu.ck_nav_category_id and submenu.child_id and not submenu.is_mega_menu`
(champ déjà renseigné par NAV-003 sur toute catégorie racine ayant des
sous-catégories éligibles — `nav_sync.py:727`, testé par
`test_catalogue_nav_category_id_set_on_root_entries`) — **sans aucune classe
CSS `ck-nav-*`** :

- **Desktop** : nouvelle branche sur le même xpath que `submenu_ck_nav_shop_desktop_split`
  (`//li[@t-elif='show_dropdown']/a[@data-bs-toggle='dropdown']...`), rendant
  libellé cliquable (`href` via `submenu._ck_nav_category_shop_url()`, déjà
  disponible sur le modèle, `website_menu.py:86-94`) + chevron toggle séparé.
  Réutiliser directement les classes SCSS existantes
  `ck-nav-universe-split__link` / `ck-nav-universe-split__toggle` — pas de
  nouveau style desktop à écrire a priori.
- **Mobile** : nouvelle branche sur le bloc accordéon stock (`//div[@t-elif='is_accordion_nav'][@class='accordion-item']`
  dans `website.submenu`), même logique de split (libellé lien + bouton
  `accordion-button` séparé pour ouvrir/fermer les enfants).

Aucun changement requis dans `nav_sync.py` ni dans les données `website.menu`
existantes — le champ `ck_nav_category_id` est déjà posé, seul le rendu QWeb
change. `test_catalogue_nav_no_legacy_css` reste vert (aucune classe
`ck-nav-*` introduite).

### 0.6 Version et migration

Changement de rendu QWeb pur, aucune donnée à réécrire : bump manifest
`dorevia_ck_marketone_content` `19.0.1.80.0` → `19.0.1.81.0` suffit, un
upgrade module standard recharge la vue. **Pas de script
`post-migrate.py` nécessaire** (à confirmer en recette : aucun ancien HTML
en cache ne doit subsister après upgrade + redémarrage).

---

## 1. Contexte

La navigation catalogue CK (CK-NAV-003) affiche en niveau 0 les catégories
e-commerce racines ayant des produits publiés (Épicerie, Boissons, Soin &
Bien-être, Artisanat selon la base). Chaque catégorie ayant des
sous-catégories éligibles ouvre un dropdown (desktop) / accordéon (mobile),
mais l'item parent n'est aujourd'hui jamais un lien réel : cliquer sur
« Épicerie » ouvre uniquement le menu, sans jamais mener à la page catégorie
racine correspondante.

Objectif : chaque item de navigation niveau 0 ayant une destination doit
être un vrai lien cliquable, le dropdown restant un raccourci vers les
sous-catégories.

---

## 2. Règle fonctionnelle (reprise de la note MOA)

| Item header | Comportement attendu | Statut actuel |
| --- | --- | --- |
| Boutique | lien vers `/shop` | déjà cliquable (pas de dropdown) |
| Épicerie / Boissons / Soin & Bien-être / Artisanat | lien vers la catégorie racine + dropdown sous-catégories | **non cliquable si dropdown présent — objet du ticket** |
| Producteurs | lien vers `/producteurs` | déjà cliquable (pas de dropdown) |
| Professionnels | lien vers `/professionnels` (conditionnel) | déjà cliquable (pas de dropdown) |

Seules les catégories ayant des sous-catégories éligibles (donc un
dropdown) sont concernées par le bug. Les catégories sans enfant (lien
simple) fonctionnent déjà correctement.

---

## 3. Comportement attendu desktop

- Clic sur le libellé (« Épicerie ») → navigue vers la page catégorie
  racine (`submenu._ck_nav_category_shop_url()`).
- Chevron séparé (élément distinct, `aria-label="Sous-catégories {nom}"`) →
  ouvre/ferme le dropdown des sous-catégories, sans navigation.
- Chaque sous-catégorie du dropdown reste un lien simple vers sa page
  catégorie (inchangé).

---

## 4. Comportement attendu mobile (offcanvas < 992 px)

- Libellé parent cliquable → navigue vers la catégorie racine.
- Bouton séparé (chevron/`accordion-button`) → ouvre/ferme la liste des
  sous-catégories dans l'offcanvas, sans navigation.
- Pas de double affichage ni de perte d'accès aux sous-catégories.

---

## 5. Contraintes techniques

- Pas de mega-menu éditorial (hors périmètre, cf. NAV-002).
- Pas d'URL en dur : toujours dérivée de `product.public.category` via
  `_ck_nav_category_shop_url()`.
- **Aucune classe `ck-nav-*` introduite** sur les entrées catalogue NAV-003
  — `test_catalogue_nav_no_legacy_css` doit rester vert.
- Aucune modification de `nav_sync.py` attendue (le champ
  `ck_nav_category_id` est déjà posé par NAV-003).
- Ne pas toucher Producteurs / Professionnels (déjà des liens simples).
- Ne pas modifier le wording des libellés ni le design global du header
  hors ajustement du chevron/toggle.
- Profondeur nav inchangée (racine + niveau 2 uniquement).

---

## 6. Critères d'acceptation

1. Chaque catégorie racine avec sous-catégories (ex. Épicerie) est
   cliquable en desktop et mène à sa page catégorie.
2. Le dropdown reste accessible via le chevron séparé, sans déclencher de
   navigation.
3. Comportement identique pour toutes les catégories racines concernées
   (Boissons, Soin & Bien-être, Artisanat le cas échéant selon éligibilité).
4. Sur mobile (offcanvas, 390 px), le libellé parent navigue et le bouton
   séparé ouvre/ferme les sous-catégories.
5. Navigation clavier : le lien et le toggle sont deux éléments focusables
   distincts, chacun actionnable (Enter sur le lien = navigation, Enter/Space
   sur le toggle = ouverture dropdown/accordéon).
6. `test_catalogue_nav_no_legacy_css` reste vert (aucune classe `ck-nav-*`
   ajoutée).
7. Aucune régression sur les catégories racines sans sous-catégorie (lien
   simple déjà fonctionnel — non concernées par le split).
8. Aucune régression sur Boutique / Producteurs / Professionnels.
9. Aucun retour au mega-menu.
10. Aucun changement visuel majeur du header (chevron seul ajouté/déplacé).

---

## 7. Tests à ajouter

Fichier `dorevia_ck_theme/tests/test_ck_phase10_header_compose.py` (assertions
HTML, module qui porte déjà les tests de rendu du header) ou nouveau fichier
dédié dans `dorevia_ck_marketone_content/tests/` :

- Sur une catégorie racine avec sous-catégories publiées : le HTML contient
  un `<a>` avec le `href` de la catégorie **distinct** du toggle
  `data-bs-toggle="dropdown"` (desktop).
- Idem côté offcanvas mobile (`data-bs-target`/`accordion-button` séparé du
  lien catégorie).
- Sur une catégorie racine **sans** sous-catégorie : toujours un lien simple
  (pas de régression — pas de toggle superflu).
- `test_catalogue_nav_no_legacy_css` : pas de modification attendue, doit
  rester vert tel quel.

## 8. Recette QA

Sur `dorevia_ck_marketone_01` (http://localhost:18079) :

**Desktop**
- `/`, `/shop`
- Clic sur chaque catégorie racine ayant un dropdown → arrive bien sur
  `/shop/category/...`
- Ouverture du dropdown via le chevron → sous-catégories accessibles
- Navigation clavier (Tab + Enter) sur libellé puis sur chevron

**Mobile 390 px**
- Ouverture offcanvas
- Clic libellé catégorie → navigation
- Clic bouton séparé → ouverture accordéon sous-catégories, pas de
  navigation
- Pas de conflit lien/toggle

---

## 9. Hors périmètre

Refonte graphique du header, mega-menu, structure SEO des catégories,
création/reclassement de produits ou catégories, wording des rayons, page
`/shop` elle-même, `nav_sync.py` (aucune modification attendue).

---

## 10. Message de commit proposé

```
fix(ck-nav): CK-NAV-005 rendre les catégories niveau 0 cliquables (lien + toggle séparés, desktop et mobile)
```
