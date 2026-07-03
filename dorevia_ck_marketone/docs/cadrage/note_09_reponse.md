# Retour Dev/QA — Note 09 · CK-UNIVERSE-BANNER-001 · Banner éditorial des pages Univers

| Champ | Valeur |
| --- | --- |
| Date | 3 juillet 2026 |
| Référence | `note_09.md` |
| Module cible | `dorevia_ck_marketone_content` (modèle + contenu) + `dorevia_ck_theme` (templates + SCSS) |
| Statut | Analyse Dev/QA — pas d'implémentation à ce stade (conforme §2 de la note) |
| Version module actuelle | `dorevia_ck_marketone_content` 19.0.1.81.0 · `dorevia_ck_theme` 19.0.1.119.0 |

---

## Synthèse

**Un socle quasi-complet existe déjà et a été volontairement désactivé côté rendu il y a 5 jours (ticket Shop-U3, commit `9bf83ef8`, 28/06/2026).** Le champ `ck_universe`, le contenu éditorial par univers (`RAYON_EDITORIAL`) et le SCSS `.ck-rayon-banner` sont toujours présents dans le code — seul l'affichage a été retiré, au profit d'un H1 compact. La note 09 ne part donc pas de zéro : il s'agit d'une **réactivation + extension image**, pas d'une création.

| Élément | Réponse |
| --- | --- |
| **Faisabilité** | Oui, socle existant réutilisable (backend) ; le SCSS visuel doit être en grande partie réécrit (l'ancien `.ck-rayon-banner` est un aplat couleur, sans image de fond) |
| **Approche** | Réactiver l'injection dans `website_sale_rayon_editorial.xml`, ajouter l'image native (`image.mixin` déjà présent sur `product.public.category`) + 2 champs CK (`ck_subtitle`, `ck_banner_variant`) |
| **Point de vigilance majeur** | Un test existant (`test_ck_shop_universe_banner.py`, tag `dorevia_ck_shop_u3`) **affirme explicitement l'absence** de bannière — il faudra le réécrire, pas juste l'adapter |

---

## 1. Audit de l'existant (§8 et Q1–Q5 de la note)

### 1.1 Chaîne de templates qui rend `/shop/category/...`

```
website_sale.products (Odoo standard)
  └─ dorevia_ck_theme.products_ck_shop_compose      (priority 20, injecte s_ck_shop_intro dans #oe_structure_website_sale_products_1)
       └─ dorevia_ck_marketone_content.website_sale_rayon_editorial   (hérite products_ck_shop_compose, insère le H1 compact avant s_ck_shop_intro)
       └─ dorevia_ck_marketone_content.website_sale_category_tiles   (hérite products_ck_shop_compose, tuiles sous-familles génériques hors Épicerie)
       └─ website_sale_rayon_editorial_hide_native_title (priority 40, masque le H1 natif Odoo si ck_rayon actif)
```

Fichiers : [website_sale_shop_compose.xml](../../dorevia_ck_theme/views/website_sale_shop_compose.xml), [website_sale_rayon_editorial.xml](../../dorevia_ck_marketone_content/views/website_sale_rayon_editorial.xml).

### 1.2 Composant CK de bannière univers — **existe déjà, désactivé**

- `product.public.category.ck_universe` (Selection epicerie/boissons/soin/artisanat) — [product_public_category.py:11](../../dorevia_ck_marketone_content/models/product_public_category.py#L11)
- `_get_ck_universe()` — remonte l'arborescence, héritage parent → enfant déjà géré ([product_public_category.py:20](../../dorevia_ck_marketone_content/models/product_public_category.py#L20))
- `get_ck_shop_banner(category=None)` — point d'entrée modèle appelé depuis QWeb ([product_public_category.py:30](../../dorevia_ck_marketone_content/models/product_public_category.py#L30))
- `RAYON_EDITORIAL` — dict titre + phrase par univers, clé = valeur `ck_universe`, fallback `boutique` interne non exposé BO ([shop_rayon_editorial.py:24](../../dorevia_ck_marketone_content/shop_rayon_editorial.py#L24))
- SCSS `.ck-rayon-banner` — toujours compilé (non commenté), lignes [website_sale.scss:78-96](../../dorevia_ck_theme/static/src/scss/website_sale.scss#L78) + variante mobile lignes 190-203. **C'est un aplat `background-color: $ck-primary`, sans image de fond ni scrim** — ne couvre pas le besoin §9 de la note (image cover + scrim).

**Ce qui a été retiré en Shop-U3** (commit `9bf83ef8`, 28/06/2026, message : *« Supprime le rendu .ck-rayon-banner/familles/highlights sur le parcours shop »*) : le rendu HTML du bloc bannière, familles et highlights. Le H1 seul (`ck_rayon['title']`) est conservé, injecté dans `.ck-shop-intro--title-only` ([website_sale_rayon_editorial.xml:16-20](../../dorevia_ck_marketone_content/views/website_sale_rayon_editorial.xml#L16-L20)).

**Raison probable du retrait** (à confirmer avec MOA, non documentée dans une note dédiée) : le message de commit et le test associé suggèrent un choix de sobriété/maturité sur le parcours shop plutôt qu'un problème technique — aucun bug ni régression mentionnés.

### 1.3 Champs CK déjà présents sur `product.public.category`

Un seul : `ck_universe` (§1.2). Aucun `ck_subtitle`, `ck_banner_enabled` ou `ck_banner_variant` n'existe — à créer (§17 Q3, §12).

### 1.4 Image native de la catégorie e-commerce (Q4, Q5, Q6)

`product.public.category` hérite du mixin standard `image.mixin` dans Odoo 19 CE (`addons/website_sale/models/product_public_category.py`), ce qui donne nativement `image_1920` / `image_1024` / `image_512` / `image_256` / `image_128`.

- **Déjà exposée en BO** : `product_public_category_form_view` (Odoo standard) affiche `image_1920` en widget avatar dans le formulaire catégorie — le MOA peut donc **déjà** uploader une image par univers sans aucun développement.
- **Non utilisée nulle part côté front CK aujourd'hui** — aucune occurrence dans les templates `dorevia_ck_theme` / `dorevia_ck_marketone_content` (grep négatif sur `image_1920`/`image_1024` liés à `product.public.category`).
- Recommandation : `<img t-att-src="'/web/image/product.public.category/%s/image_1024' % category.id"/>` en `<img>` HTML réel (pas CSS `background-image`), pour bénéficier du lazy-loading natif, de l'`alt` accessible et du cache image Odoo standard — cohérent avec §15 (« texte en HTML, jamais dans l'image », donc l'image reste un simple visuel, le scrim/texte restent en overlay HTML/CSS).

### 1.5 Tuiles sous-catégories (Note 07 Lot B) — composant voisin, à ne pas confondre

`website_sale_category_tiles.xml` affiche des tuiles visuelles des enfants directs, **uniquement quand `get_ck_rayon_editorial()` est falsy** (donc actuellement toujours, puisque tous les univers renvoient un contenu simple non vide... à vérifier : `get_ck_rayon_editorial()` renvoie toujours un dict non-vide donc toujours truthy → les tuiles ne s'affichent en réalité **jamais** en l'état actuel, sauf si le dict est vide, ce qui n'arrive plus depuis `ck_universe`). **Point à lever avec le Dev avant ticket final** : ce garde-fou semble caduc depuis l'introduction de `ck_universe` (tous les univers ont désormais un contenu RAYON_EDITORIAL non vide) — comportement à vérifier en recette avant d'ajouter la bannière, pour ne pas empiler deux composants d'entrée d'univers.

### 1.6 Migrations passées

- `19.0.1.56.0` — init `ck_universe` sur les 4 catégories racines par nom.
- `19.0.1.57.0` — Shop-U3, retrait du rendu bannière + durcissement bootstrap tags.

Prochaine migration à prévoir sur `dorevia_ck_marketone_content` (version courante 19.0.1.81.0) pour les nouveaux champs.

### 1.7 Tests existants sur `/shop/category/...`

`test_ck_shop_universe_banner.py` (tag `dorevia_ck_shop_u3`, `HttpCase`) — teste actuellement l'**absence** de bannière : `assertNotIn('ck-rayon-banner', html)`, un seul H1 visible, classe `ck-shop-intro--title-only` présente, sur les 5 chemins `/shop` + 4 univers. **Ce test devra être réécrit** (pas juste étendu) si la bannière est réintroduite — il contredit frontalement l'objectif de la note.

Autres tests connexes : `test_ck_shop_structure_s1.py`, `test_ck_shop_phase3_compose.py`, `test_ck_shop_toolbar.py`, `test_ck_shop_filter_drawer.py`, `test_ck_shop_product_card.py` — à revalider (non-régression) plutôt qu'à modifier a priori.

### 1.8 Accents couleur par univers (§11, Q9)

Aucun mapping existant. Les seules couleurs univers-spécifiques trouvées dans le code concernent le remap `$primary` → terracotta global CK (filmstrip pills, SCSS ligne 569), pas une déclinaison par univers. **C'est le seul point réellement neuf de la note** — tout le reste (champ, contenu, image, gabarit de template) a un précédent direct dans le code.

### 1.9 Breadcrumb / H1 (Q7, §16)

`website_sale_breadcrumb.xml` est un template indépendant (cf. mémoire Breadcrumb-U1) qui gère l'icône `fa-home`, sans lien avec `oe_structure_website_sale_products_1`. Risque d'interaction faible. Le H1 reste géré comme aujourd'hui : `ck_rayon['title']` dans la bannière = le H1 unique de la page (déjà la règle actuelle depuis Shop-U3, cf. `website_sale_rayon_editorial_hide_native_title`) — pas de double H1 à gérer, le mécanisme existe déjà et fonctionne (testé en 1.7).

---

## 2. Réponses aux 12 questions (§17)

1. **Quel template rend `/shop/category/...` ?** `website_sale.products` hérité par `products_ck_shop_compose` (dorevia_ck_theme) puis `website_sale_rayon_editorial` (dorevia_ck_marketone_content). Cf. §1.1.
2. **Composant CK bannière rayon/univers existant ?** Oui — désactivé, pas supprimé (Shop-U3). Cf. §1.2.
3. **Champs CK exploitables sur `product.public.category` ?** Seulement `ck_universe`. `ck_subtitle`, `ck_banner_variant` restent à créer.
4. **Image native accessible en QWeb ?** Oui, `image_1920`/`image_1024`/etc. via `image.mixin` standard, déjà exposée en BO. Cf. §1.4.
5. **Image déjà utilisée ailleurs ?** Non, aucune occurrence front CK actuellement.
6. **`<img>` ou `background-image` ?** `<img>` HTML réel en fond de section positionnée (object-fit: cover), pour lazy-loading + alt accessible ; scrim en overlay CSS séparé par-dessus.
7. **Gestion du H1 natif ?** Déjà résolu par le mécanisme Shop-U3 existant (`ck_rayon['title']` = H1 unique, natif masqué conditionnellement). Réutiliser tel quel.
8. **`ck_banner_enabled` ou affichage auto niveau 0 ?** Affichage automatique niveau 0 recommandé (`category and not category.parent_id and category._get_ck_universe()`), pas de booléen supplémentaire — cohérent avec le principe déjà en place où `get_ck_shop_banner` renvoie toujours un dict non-None (dégradé gracieux). Un champ booléen ajouterait un état à maintenir sans bénéfice fonctionnel identifié par la note.
9. **Accent visuel : mapping, selection, couleur libre ?** `Selection` `ck_banner_variant` (epicerie/boissons/bien_etre/artisanat/default) comme proposé en §11 de la note — cohérent avec le choix déjà fait pour `ck_universe` (éviter le champ libre). Le SCSS mappe la variante à un jeu de couleurs figées dans la charte.
10. **Tests à ajouter/adapter ?** Réécrire `test_ck_shop_universe_banner.py` (le test actuel affirme l'absence de bannière — contradictoire avec la cible). Ajouter : présence de l'image de fond, fallback sans image, fallback sans accroche, un seul H1 par page, non-régression `/shop` général et sous-catégories.
11. **Risque de régression `/shop`, sous-catégories, mobile ?** Faible sur `/shop` général et sous-catégories si la condition `not category.parent_id` est respectée strictement (déjà le pattern recommandé §13). Risque principal : interaction avec les tuiles sous-familles (§1.5, point à lever) et avec le test Shop-U3 existant qui doit être réécrit en connaissance de cause, pas silencieusement cassé.
12. **Un ticket ou deux lots ?** **Deux lots recommandés** : Lot A = image native + réactivation structurelle (titre + accroche + image + fallback), sans variante couleur (utilise l'accent CK par défaut partout) ; Lot B = `ck_banner_variant` + déclinaison couleur par univers. Permet une recette MOA intermédiaire sur le gabarit avant d'investir sur la charte couleur (qui est le seul point sans précédent, cf. §1.8).

---

## 3. Proposition technique recommandée

- Réactiver l'injection dans `website_sale_rayon_editorial.xml` (remplacer le bloc `.ck-shop-intro--title-only` par un bloc `.ck-univers-banner` complet), plutôt que créer un nouveau template parallèle.
- Étendre `get_ck_shop_banner()` / `RAYON_EDITORIAL` pour inclure l'URL image (calculée depuis `category.image_1024` côté modèle, pas côté template) et le futur `ck_subtitle` / `ck_banner_variant`.
- Réécrire le SCSS `.ck-rayon-banner` (pas de simple réactivation — l'existant n'a pas d'image de fond) avec un fond `<img>` `object-fit: cover`, scrim latéral brun chaud (gradient CSS, pas d'image), hauteur ~220px desktop / ~180px mobile.
- Garder la garde stricte niveau 0 uniquement (`category and not category.parent_id`), pas d'extension aux sous-catégories en V1, conformément à §5 et §13 de la note.
- Lever le point §1.5 (tuiles sous-familles) avec le Dev en amont du ticket final, pour éviter d'empiler deux blocs d'entrée d'univers sur la même page.

## 4. Fichiers pressentis à modifier

| Fichier | Nature du changement |
| --- | --- |
| `dorevia_ck_marketone_content/models/product_public_category.py` | Ajout champs `ck_subtitle`, `ck_banner_variant` ; méthode image banner |
| `dorevia_ck_marketone_content/shop_rayon_editorial.py` | Extension `RAYON_EDITORIAL` / `get_rayon_editorial()` pour renvoyer `image_url`, `subtitle`, `variant` |
| `dorevia_ck_marketone_content/views/website_sale_rayon_editorial.xml` | Remplacement du bloc `.ck-shop-intro--title-only` par le nouveau bloc bannière |
| `dorevia_ck_theme/static/src/scss/website_sale.scss` | Réécriture `.ck-rayon-banner` (image de fond, scrim, variantes couleur, responsive) |
| `dorevia_ck_marketone_content/tests/test_ck_shop_universe_banner.py` | Réécriture complète (le test actuel vérifie l'absence) |
| `dorevia_ck_marketone_content/migrations/19.0.1.82.0/post-migrate.py` (ou suivant) | Migration si valeurs par défaut à initialiser sur les 4 catégories racines |
| Vue formulaire BO `product.public.category` (à localiser — probablement dans `dorevia_ck_marketone_content/views/`) | Exposer `ck_subtitle` / `ck_banner_variant` à côté de `image_1920` déjà présent nativement |

## 5. Champs Odoo à créer ou réutiliser

| Champ | Type | Statut |
| --- | --- | --- |
| `ck_universe` | Selection | **Existant**, réutilisé tel quel |
| `image_1920` (et dérivés) | Binary (image.mixin) | **Existant standard Odoo**, réutilisé, non modifié |
| `ck_subtitle` | Char | À créer — accroche courte |
| `ck_banner_variant` | Selection (epicerie/boissons/bien_etre/artisanat/default) | À créer |
| `ck_banner_enabled` | — | **Non recommandé** — affichage automatique niveau 0 suffit (Q8) |

## 6. Risques identifiés

- Réactivation d'un composant retiré récemment sans note de retrait documentée : **valider avec MOA la raison du retrait Shop-U3 avant de relancer**, pour ne pas recréer un problème déjà résolu silencieusement.
- Test existant contredisant frontalement la cible (§1.7) — risque de faux-vert si le test est mal réécrit (ex. suppression pure et simple de l'assertion au lieu de l'inverser proprement).
- Chevauchement potentiel avec les tuiles sous-familles (§1.5) — à lever avant chiffrage.
- SCSS à réécrire entièrement pour le fond image (pas une simple réactivation) — effort sous-estimé si traité comme un « unhide ».

## 7. Tests à prévoir

- Réécriture `test_ck_shop_universe_banner.py` : présence bannière + image + un seul H1 sur les 4 univers, absence sur `/shop` général et sur les sous-catégories.
- Fallback sans image catégorie (catégorie test sans `image_1920`).
- Fallback sans `ck_subtitle`.
- Non-régression tuiles sous-familles / filmstrip / toolbar (tests existants déjà cités §1.7).
- Contrôle visuel mobile 390px (recette manuelle, cohérent avec la convention CK sur les tickets précédents).

## 8. Proposition de ticket Dev final

**CK-UNIVERSE-BANNER-001 — Lot A** (prêt à exécuter après validation MOA du point §1.5 et de la raison du retrait Shop-U3) :
1. Modèle : `ck_subtitle` sur `product.public.category` + vue BO.
2. `get_rayon_editorial()` : ajoute `image_url` (depuis `image_1024`, fallback None) et `subtitle` (fallback None) au dict retourné.
3. Template : bloc `.ck-univers-banner` (image `<img>` + scrim + titre + accroche), affiché uniquement si `category and not category.parent_id and ck_rayon`, accent CK par défaut unique pour tous les univers.
4. SCSS : nouveau bloc `.ck-univers-banner` (220px desktop / 180px mobile, scrim brun chaud, fallback fond clair CK sans image).
5. Tests : réécriture `test_ck_shop_universe_banner.py` + nouveaux cas fallback.
6. Migration si nécessaire pour données existantes.

**Lot B** (après recette Lot A) : `ck_banner_variant` + mapping couleur par univers (§11).

---

## Conclusion

**Pas de nouveau composant à créer de zéro** : le ticket final consiste à réactiver et étendre un socle existant (`ck_universe`, `RAYON_EDITORIAL`, `.ck-rayon-banner`) plutôt qu'à en bâtir un nouveau, avec deux ajouts réels (image native branchée + accroche courte) et un point à lever en amont avec le Dev (interaction tuiles sous-familles, raison du retrait Shop-U3).
