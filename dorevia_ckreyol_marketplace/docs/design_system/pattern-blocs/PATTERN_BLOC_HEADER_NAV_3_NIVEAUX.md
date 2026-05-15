# Pattern-bloc — Header CK : navigation en 3 niveaux (N0 / N1 / N2)

Ce document décrit **l’architecture fonctionnelle** du header C-Kreyol tel qu’il est **conçu et rendu** aujourd’hui : trois niveaux de lecture (**signal boutique**, **services & recherche**, **navigation utile**). Ce n’est pas un ticket de développement : aucune refonte ni nouveau snippet Odoo n’est prescrit par ce texte.

**Alignement vocabulaire** : voir [`../README.md`](../README.md) (pattern-bloc vs snippet Odoo déposable). Le header reste un **composant de layout global** ; il n’est pas ciblé comme snippet éditorial à glisser-déposer.

---

## Intention produit

Offrir une **colonne vertébrale de navigation** stable et premium :

- **N0** : signal court, contextualisé, utile au parcours d’achat ou à la réassurance — sans encombre permanent sur tout le site.
- **N1** : tout ce qui permet d’**agir vite** : identité marque, recherche, compte, favoris, panier, ouverture du menu mobile.
- **N2** : tout ce qui **structure l’entrée dans l’offre** CK (boutique, promotions, mises en avant, territoires / origines, rubriques éditoriales ou communautaires selon évolution projet).

Le header doit rester **sobre**, **lisible**, et **cohérent** avec la boutique sans voler la place au contenu des pages.

---

## Structure attendue (logique des 3 niveaux)

### N0 — Signal boutique contextuel

- Bandeau **court** (messages de service, livraisons, informations commerciales temporaires, etc.).
- **Affiché seulement dans certains contextes** — pas un niveau systématique sur toutes les URLs.
- **Ne doit pas être qualifié** comme partie standard de la **Home `/`** si le périmètre contextuel choisi est la boutique ou une sous-arborescence (voir implémentation actuelle).
- Rôle : **réassurance** et **orientation marchande ponctuelle**.
- À éviter : **bandeau publicitaire agressif** ou **permanent** si le contexte ne le justifie pas.

### N1 — Services & recherche

- **Logo / marque** (retour accueil).
- **Recherche** (accès rapide au catalogue).
- **Compte** (connexion / espace client selon état de session).
- **Favoris**.
- **Panier** (avec quantité visible pour `website_sale`).
- **Menu mobile** (burger ; panneau latéral avec navigation complémentaire).
- Rôle : **outillage d’achat et de service** sans duplication de la grille de parcours N2 sur desktop.

### N2 — Navigation utile

- Entrées de **parcours boutique** et de **Découverte** : par exemple tous les produits, promotions, mises en avant type **kits / packs** ou **incontournables**, **origines**, ou autres **portes catalogue** pertinentes CK.
- Rôle : **orienter dans l’offre** et les grands motifs d’exploration sans remplacer le contenu de la Home ni le `/shop`.

**Important** : la liste ci-dessus exprime **l’intention** et les **familles d’entrées** visées par ce pattern-bloc. Le **catalogue exact de liens** peut évoluer (MOA, SEO, saisonnalité). L’implémentation de référence ci-dessous reste **source de vérité** pour ce qui est **effectivement livré dans le fichier QWeb**.

---

## Implémentation actuelle de référence

| Couche | Fichiers principaux |
| --- | --- |
| Marquage QWeb | `views/layout/ckr_header.xml` (template `ckr_header`, héritage `website.layout`, remplacement `//header`) |
| Styles | `static/src/scss/layout/_header.scss` |
| Comportements | `static/src/js/ckr_header_drawer.js` |
| Décisions associées | `docs/direction/ARCHITECTURE_DECISION_RECORD.md` (ADR-CKR-003), `docs/direction/STRUCTURE_MENU_PRINCIPAL.md` |

**Détail technique utile** :

- **`id="top"`** sur `<header>` et classe **`o_header_fixed`** : compatibilité avec les attentes Odoo Website / `website_sale` (ex. compteur panier).
- **Hook** `<ul class="top_menu" …>` masqué : évite une erreur du script standard Odoo cherchant `.top_menu` dans le header.
- **Mesure dynamique de hauteur** : `--ckr-header-measured` sur `:root` (pour le rendu immersif hero et le calcul du premier écran utile).

### N0 en code

- Conteneur : `ckr-header__top0` → rotateur `ckr-header__top0-rotator` avec entrées textuelles.
- **Condition de rendu** : `ckr_path.startswith('/shop')` uniquement (`t-set ckr_path` sur `request.httprequest.path`).
- Conséquences documentaires : **absent sur la Home `/`** et sur la plupart des pages hors `/shop*` dans l’état actuel — conforme au positionnement « **signal boutique contextuel** ».

### N1 en code

- Barre : `div.ckr-header__inner.ckr-header__top1`.
- Logo (SVG plusieurs variantes, activation par CSS), formulaire recherche desktop (`action="/shop"`, `name="search"`), bloc **locale** (langues + listes de prix Odoo via `t-call`), cluster compte / favoris / panier avec **`<sup class="my_cart_quantity …>`** pour le cache `website_sale`, burger + panneau drawer.

### N2 en code

- Barre desktop : `nav.ckr-header__top2` avec liens directs et un sous-menu **`details`** (ex. « Communauté »).
- **Rendu actuel (à valider régulièrement dans le fichier)** : notamment liaisons vers `/shop`, `/promotions`, `/collections`, un panel déroulant communautaire, et un lien métiers (ex. `/demande-compte-professionnel`). Les entrées futures du type **Kits / packs**, **Incontournables**, **Origines** sont **À placer sous cette même logique N2** lorsqu’elles seront ajoutées en QWeb ou via menu — sans confondre avec le bloc **Explorer** de la Home.
- **Mobile** : la barre N2 desktop est **`d-none d-lg-block`** ; la navigation primaire passe par **`website.menu_id.child_id`** dans le drawer (structure éditoriale Odoo — peut diverger du libellé exact de la barre N2 tant que les deux pipelines coexistent).

---

## Règles responsive

- **Desktop (≥ lg)** : N2 visible sous N1 ; recherche champ libre dans N1 ; locale visible.
- **Mobile (&lt; lg)** : pas de bandeau de recherche plein champ dans la barre (entrée recherche/icône vers `/shop` selon breakpoints) ; **drawer** pour le menu principal ; locale en bas du drawer.
- Header **sticky** en tête (`position: sticky` ; z-index harmonisé avec le stack Bootstrap / overlays).
- Hauteur réduite en mobile dans les styles (`min-height` N1 plus basse pour densifier la barre).
- Rotateur N0 : typographie et `min-height` ajustés sous `991.98px` dans `_header.scss`.

---

## Comportements UX

- **N0** : rotation douce des messages sur desktop ; sous **`prefers-reduced-motion: reduce`**, le rotateur CSS est neutralisé et **un seul message reste lisible** (premier item).
- **Drawer** : ouverture / fermeture pilotée par checkbox `ckr_drawer_toggle` ; libellés / `aria-expanded` synchronisés côté JS ; fermeture sur **Escape**, clic hors zone (backdrop), clic sur lien de navigation ; refermeture forcée au passage desktop pour éviter un menu « coincé ».
- **Menu compte desktop** (`details.ckr-header__user-menu`) : fermeture clic extérieur et Escape avec retour focus sur `summary`.

---

## Accessibilité

- Landmark cohérent : **`<header id="top">`**.
- Recherche : `role="search"`, étiquette associée au champ (`visually-hidden` + `for`).
- Drawer : **`aria-controls`**, **`aria-expanded`** burger mis à jour par script ; fermeture clavier avec retour focus.
- Boutons/icônes : `aria-label` / texte réservé quand pertinent ; icônes décoratives `aria-hidden="true"`.
- Sous-menu N2 **`details`** : structure native ; sous-liens avec `role="menuitem"` dans le panel.
- **Reduced motion** : pris en charge pour N0 comme ci-dessus.

---

## GO / NO GO

### GO

- Les trois niveaux sont **distincts fonctionnellement** : signal (quand présent), outils, puis parcours.
- N1 reste utilisable sans surcharge sur mobile ; N2 lisible et calme sur desktop.
- Pas de rupture **`website_sale`** (compteur panier dans le format attendu).
- Header **sticky** lisible sans chevauchement aberrant avec le contenu principal.
- Respect des préférences utilisateur (**réduction du mouvement** sur N0).

### NO GO

- N0 affiché **partout sans justification** métier ou devenant **banner invasif** / tonalité trop promotionnelle.
- **Duplication confuse** entre N2 desktop et drawer mobile sans règle de gouvernance (double vérités contradictoires sur les entrées critiques).
- **Régression accessible** sur le burger, le panier ou la recherche.
- Modifications qui **cassent** `--ckr-header-measured` sans recette sur hero / première vue.

---

## Points de vigilance dev

- Toute évolution du **contexte N0** (`startswith('/shop')` ou autres règles) doit être **explicitement arbitrée** avec MOA ; documenter dans ce pattern-bloc si la règle change.
- **`my_cart_quantity`** : conserver la forme compatible `website_sale` (évite erreurs serveur ou cache panier KO).
- Conserver **l’hypothèque** `top_menu` cachée tant que le script Odoo natif impose ce garde-fou.
- Tester **sticky + drawer + modales** (z-index) après tout changement de pile visuelle.
- Si l’on enrichit N2 (**origines**, **kits**, etc.), vérifier la **cohérence** avec la doctrine URLs boutique ([`docs/mvp_04/CANON_URL_BOUTIQUE.md`](../../mvp_04/CANON_URL_BOUTIQUE.md)) et le menu Odoo utilisé dans le drawer.
- Ne pas **confondre** ce layout header avec un **snippet Odoo déposable** : changements ici impactent **toutes** les pages du site utilisant ce layout.

---

## Statut du document

**Créé** — décrit le header **existant**. Les écarts éventuels entre **intention N2** (kits, incontournables, origines) et les **libellés/URL actuels** dans `ckr_header.xml` relèvent d’une **phase éditoriale / road-map** hors refonte automatique prescrite par ce pattern-bloc.
