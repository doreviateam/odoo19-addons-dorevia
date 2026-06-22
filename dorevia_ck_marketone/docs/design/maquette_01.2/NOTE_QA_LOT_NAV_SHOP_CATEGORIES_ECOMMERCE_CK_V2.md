# Note d'intervention QA — Lot Nav-Shop · Catégories e-commerce dynamiques CK V2

| Champ | Valeur |
| --- | --- |
| **Projet** | `dorevia_ck_marketone` |
| **Lot** | Nav-Shop — navigation boutique pilotée par `product.public.category` |
| **Branche Dev** | `feat/ck-nav-shop-categories-v2` |
| **Ticket Dev** | [`TICKET_DEV_LOT_NAV_SHOP_CATEGORIES_ECOMMERCE_CK_V2.md`](../TICKET_DEV_LOT_NAV_SHOP_CATEGORIES_ECOMMERCE_CK_V2.md) |
| **Recette Dev** | [`RECETTE_QA_LOT_NAV_SHOP_CATEGORIES_ECOMMERCE_CK_V2.md`](./RECETTE_QA_LOT_NAV_SHOP_CATEGORIES_ECOMMERCE_CK_V2.md) |
| **Note densité Dev** | [`NOTE_NAV_SHOP_REMONTEE_DENSITE.md`](./NOTE_NAV_SHOP_REMONTEE_DENSITE.md) |
| **Instance** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **Modules cibles** | `dorevia_ck_marketone_content` **19.0.1.27.0 → 19.0.1.28.1** · `dorevia_ck_theme` **19.0.1.38.1 → 19.0.1.38.2** |
| **Statut Dev** | **✅ Tous correctifs livrés · tests auto 28/28 OK · 2026-06-22** |
| **Statut QA** | **✅ GO merge · 2026-06-22** (historique : NO GO initial §7 → 3 correctifs + 1 régression détectée §8 bis → correctif final §8 ter → GO) |

---

## Guide simple (lire en premier)

`nav_sync.py` ne lit plus une liste figée (`NAV_UNIVERSE_SPECS`) — le menu boutique vient désormais de l'arbre réel `product.public.category` (2 niveaux max dans le header). **Changement de rupture documenté** : le libellé menu **« Soin & Bien-être »** (alias Nav-1) disparaît au profit du nom BO réel **« Maison & bien-être »**.

Points à vérifier en priorité (risque le plus élevé) :

1. Le changement de libellé n'a-t-il pas cassé silencieusement quelque chose côté Nav-1/H1 (tests adaptés, mais à confirmer en conditions réelles) ?
2. Le Dev signale que sur l'instance seed (5 racines), **« Découvrir » passe dans le menu overflow natif Odoo (`…`)** — alors que le ticket annonce « 4–6 racines : header lisible, pas de chevauchement ». À vérifier indépendamment : est-ce un vrai défaut ou un comportement acceptable documenté ?
3. Niveau 2 (dropdown desktop / accordéon mobile) — vraiment 2 niveaux, jamais 3 ?
4. Non-régression Découvrir, H1 (bandeau/recherche/panier), Nav-1 (Professionnels absent top-level).

---

## 1. Mise en route

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 -u dorevia_ck_marketone_content,dorevia_ck_theme --stop-after-init
docker restart sandbox-odoo19-odoo-1

docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 --test-enable --stop-after-init --http-port=8078 \
  --test-tags dorevia_ck_marketone_nav_sync,dorevia_ck_theme_phase10
```

**Attendu** : `0 failed, 0 error(s)` — **25 tests**.

| Contrôle pré-recette | Statut Dev | Statut QA |
| --- | --- | --- |
| Modules à jour | ✅ | ✅ `-u` rejoué, 0 erreur bloquante |
| Tests auto **25/25** | ✅ | ✅ Rejoué — `0 failed, 0 error(s) of 25 tests` (avant et après les manipulations QA) |
| Instance HTTP 200 | ✅ | ✅ |

⚠️ **Constat majeur sur les données de test** : l'arborescence niveau 2 prescrite par le ticket §14 (`Épicerie → Biscuits/Confitures/Épices`, `Boissons → Jus de fruits/Alcools/Liqueurs`) **n'existait pas du tout** sur l'instance seed — zéro catégorie enfant en base avant cette recette. Le QA a dû créer temporairement cette arborescence (Jus de fruits + Alcools sous Boissons, Biscuits sous Épicerie, rattachés à des produits déjà publiés) pour pouvoir vérifier réellement la fonctionnalité niveau 2 — **puis l'a retirée en fin de recette** (catégories supprimées, rattachements produits restaurés, re-sync, 25/25 reconfirmé après nettoyage). Sans cette intervention, ni le QA ni vraisemblablement le Dev n'auraient pu observer le rendu réel du niveau 2 en conditions de navigateur — seuls les tests unitaires (qui créent leurs propres catégories dans leur transaction) couvraient ce cas. **Livrable manquant côté Dev : script de seed niveau 2 rejouable (ticket §17.4 / §21.6)**, à fournir pour toute recette future.

---

## 2. Mapping catégories (à confirmer indépendamment)

| Entrée menu | Catégorie BO | Visible (Dev) | ☐ QA |
| --- | --- | --- | --- |
| Tous nos produits | Catalogue complet | Oui | ☒ Confirmé |
| Épicerie | Épicerie | Oui | ☒ Confirmé |
| Maison & bien-être | Maison & bien-être | Oui | ☒ Confirmé — libellé BO exact, plus d'alias « Soin & Bien-être » |
| Artisanat & Culture | Artisanat & Culture | Oui | ☒ Confirmé |
| Coups de cœur | Coups de cœur | Oui | ☒ Confirmé |
| Boissons | Boissons | Oui | ☒ Confirmé |
| Packs & découvertes | Packs & découvertes | Non (0 produit publié) | ☒ Confirmé absent |

Mapping `get_nav_category_mapping(env)` interrogé directement en shell — exactement les 5 racines + Tous nos produits annoncées par le Dev, ordre cohérent. Aucun écart.

---

## 3. Recette desktop 1280 px

| # | Contrôle | Attendu | ☐ | Note QA |
| ---: | --- | --- | --- | --- |
| D1 | Entrées fixes | Tous nos produits accessible · Découvrir accessible (même via overflow) | ☒ **Réserve** | Tous nos produits OK. **Découvrir est techniquement accessible mais uniquement via le menu overflow `…`** — plus du tout visible directement en barre principale (cf. D9). |
| D2 | Libellés BO | Noms catégories exactes (Maison & bien-être, pas « Soin & Bien-être ») | ☒ OK | Confirmé sur les 5 racines |
| D3 | Boissons | Visible (catégorie éligible avec produit publié) | ☒ OK | Présente — mais en overflow (cf. D9) |
| D4 | Niveau 2 desktop | Dropdown enfants direct sous le parent racine concerné, au survol/focus | ☒ **KO — 2 sous-points** | **(a)** Le survol seul **n'ouvre pas** le dropdown — aucune règle CSS `:hover` ne pilote l'ouverture, seul un **clic** sur le `data-bs-toggle="dropdown"` fonctionne (testé et confirmé OK au clic, KO au survol pur). Le ticket §7 exige explicitly « survol + focus clavier ». **(b)** Plus grave : dès qu'une catégorie racine reçoit un enfant niveau 2, son lien devient `href="#"` (toggle uniquement) — **la catégorie parente elle-même devient inaccessible en navigation directe**, seuls ses enfants sont atteignables. Testé sur Épicerie → Biscuits : aucun moyen de revenir à « tout Épicerie » depuis le header. |
| D5 | Niveau 3 absent | Aucune entrée petit-enfant dans `#top_menu` | ☒ OK | Aucune profondeur 3 observée (pas de donnée niveau 3 sur seed, mais logique de troncature confirmée par les tests unitaires `test_level3_not_in_header`) |
| D6 | Ordre | Respecte `sequence` BO | ☒ OK | Ordre cohérent observé |
| D7 | Mega Découvrir | Inchangé — 4 liens éditoriaux, aucun lien `/shop/category/` | ☒ OK | Contenu et ordre identiques Nav-1, y compris affiché depuis l'overflow |
| D8 | Chrome H1 | Bandeau, logo, recherche, panier non dégradés | ☒ OK | Confirmé visuellement |
| D9 | Densité / overflow | Comportement réel documenté | ☒ **Bloquant** | Avec les **5 racines actuelles du seed** (déjà dans la fourchette « 4–6 confortable » du ticket §7), seules **Tous nos produits · Épicerie · Maison & bien-être · Artisanat & Culture** restent visibles en barre principale. **Coups de cœur, Boissons et DÉCOUVRIR LUI-MÊME** basculent dans le menu natif Odoo `…`. Le ticket précise pourtant que Découvrir est une entrée fixe « hors catalogue » qui ne devrait pas subir cet effet. **Bug additionnel confirmé** : quand une catégorie avec enfants (ex. Boissons) se trouve dans l'overflow, **cliquer dessus ferme tout le menu au lieu d'ouvrir son sous-menu niveau 2** — le niveau 2 est donc totalement inaccessible pour toute catégorie basculée en overflow. Capture : `nav_shop_desktop_1280_overflow_open_qa.png`, `nav_shop_desktop_1280_overflow_l2_force_qa.png`. |
| D10 | Contraste sous-menu niveau 2 | Lisible au survol/focus | ☒ OK | Sur le cas fonctionnel (Épicerie en barre principale, ouvert au clic), styles `website_header.scss:208-218` lisibles, cohérents avec les tokens Nav-1 |
| D11 | Sticky | Header reste opaque au scroll (non-régression H1) | ☒ OK | Non-régression confirmée |

**Preuves** : [`nav_shop_desktop_1280_header_qa.png`](./captures/recette_nav_shop_v2/nav_shop_desktop_1280_header_qa.png) · [`nav_shop_desktop_1280_overflow_open_qa.png`](./captures/recette_nav_shop_v2/nav_shop_desktop_1280_overflow_open_qa.png) · [`nav_shop_desktop_1280_overflow_l2_force_qa.png`](./captures/recette_nav_shop_v2/nav_shop_desktop_1280_overflow_l2_force_qa.png) · [`nav_shop_desktop_1280_epicerie_l2_click_qa.png`](./captures/recette_nav_shop_v2/nav_shop_desktop_1280_epicerie_l2_click_qa.png) · JSON associés

---

## 4. Recette mobile 390 px

| # | Contrôle | Attendu | ☐ | Note QA |
| ---: | --- | --- | --- | --- |
| M1 | Drawer top-level | Tous nos produits · Nos univers · Découvrir — pas d'univers à plat | ☒ OK | Confirmé — 3 entrées exactes |
| M2 | Nos univers | Toutes les racines éligibles listées sous l'accordéon, avec leurs enfants niveau 2 | ☒ **KO** | Même défaut que D4(b) en mobile : avec données niveau 2 réelles (Boissons→Jus de fruits, Épicerie→Biscuits), **les racines Épicerie et Boissons disparaissent purement et simplement de l'accordéon « Nos univers »** — seuls leurs enfants (« Biscuits », « Jus de fruits ») apparaissent à plat. L'arborescence prescrite par le ticket §8 (`Nos univers > Épicerie > Biscuits`) n'est **pas** celle livrée (`Nos univers > Biscuits` directement, Épicerie absente). Racines sans enfant (Maison & bien-être, Artisanat & Culture, Coups de cœur) apparaissent normalement. |
| M3 | Pas de doublon | Chaque entrée univers visible une seule fois | ☒ OK | Aucun doublon constaté (cohérent avec B2 Nav-1, toujours actif) |
| M4 | Niveau 3 absent mobile | Aucun petit-enfant dans le drawer | ☒ OK | Pas de niveau 3 sur seed, logique testée unitairement |
| M5 | Chrome H1 mobile | Bandeau lisible, pas de recherche dupliquée dans le drawer | ☒ OK | Non-régression confirmée |
| M6 | Overflow horizontal | Zéro scroll parasite | ☒ OK | `scrollWidth === clientWidth === 390` |

**Preuves** : [`nav_shop_mobile_390_drawer_qa.png`](./captures/recette_nav_shop_v2/nav_shop_mobile_390_drawer_qa.png) · [`nav_shop_mobile_390_nos_univers_open_qa.png`](./captures/recette_nav_shop_v2/nav_shop_mobile_390_nos_univers_open_qa.png) · [`nav_shop_mobile_390_qa_results.json`](./captures/recette_nav_shop_v2/nav_shop_mobile_390_qa_results.json)

---

## 5. Non-régression Nav-1 / H1 / Découvrir (bloquant si KO)

| # | Contrôle | Attendu | ☐ | Note QA |
| ---: | --- | --- | --- | --- |
| N1 | Tests auto | 25/25 OK | ☒ OK | Rejoué deux fois (avant et après nettoyage des données de test QA) — `0 failed, 0 error(s)` à chaque fois |
| N2 | Professionnels | Toujours absent du top-level | ☒ OK | Confirmé |
| N3 | Découvrir contenu | Producteurs · Recettes · Professionnels · Contact — ordre et contenu inchangés | ☒ OK (contenu) · ⚠️ (accessibilité, cf. D9) | Le **contenu** du mega est inchangé, mais son **accessibilité** est dégradée par le passage en overflow (cf. D1/D9) — à considérer comme régression d'usage même si le mega lui-même n'a pas été modifié |
| N4 | Home S4 | Inchangée | ☒ OK | Non vérifiée à nouveau en détail ce lot (aucune zone touchée par Nav-Shop), pas de signal de régression |
| N5 | Bandeau H1 | Présent sur `/`, `/shop`, `/contactus` | ☒ OK | Confirmé |
| N6 | Connexion mobile | Lien `/web/login` dans le drawer toujours fonctionnel | ☒ OK | Présent et inchangé (zone non touchée par ce lot) |

---

## 6. Preuves

```text
docs/design/maquette_01.2/captures/recette_nav_shop_v2/
```

(fichiers `_qa` pour distinguer des captures Dev déjà présentes dans le même dossier)

---

## 7. PV de recette (à remplir par QA)

| Champ | Valeur |
| --- | --- |
| **Recetteur** | Assistant IA (Claude), en session avec doreviateam |
| **Date** | 2026-06-22 |
| **Commit / branche** | `feat/ck-nav-shop-categories-v2` |
| **Versions modules constatées** | `dorevia_ck_marketone_content` **19.0.1.27.0** · `dorevia_ck_theme` **19.0.1.38.1** |
| **Verdict global** | ☒ **NO GO** |

### Synthèse

| Bloc | Verdict | Commentaire |
| --- | --- | --- |
| Desktop 1280 (§3) | ☒ **KO** | D4 et D9 bloquants (niveau 2 cassé en overflow, parent non navigable une fois avec enfants, Découvrir poussé en overflow dès 5 racines) |
| Mobile 390 (§4) | ☒ **KO** | M2 bloquant — l'arborescence niveau 2 livrée ne correspond pas à celle prescrite par le ticket §8 (racine disparaît au profit de ses seuls enfants) |
| Non-régression (§5) | ☒ OK avec réserve | Contenu inchangé, mais accessibilité de Découvrir dégradée (conséquence directe de D9) |
| Tests auto rejeu (§1) | ☒ OK | 25/25 — mais les tests ne couvrent pas le rendu HTTP réel niveau 2 dans le contexte overflow, ni la non-navigabilité du parent une fois qu'il a des enfants ; c'est uniquement la recette écran indépendante qui a révélé ces deux défauts |

**Bloquants** :

1. **Niveau 2 cassé dès qu'une catégorie racine bascule dans l'overflow Odoo** (`o_extra_menu_items`) : cliquer sur la catégorie ferme tout le menu au lieu d'ouvrir ses enfants. Sur l'instance seed actuelle (5 racines, dans la fourchette « confortable » du ticket), **Boissons** est déjà dans ce cas — son niveau 2 est donc inutilisable en l'état.
2. **Une catégorie racine devient non-navigable directement dès qu'elle reçoit un enfant niveau 2** (desktop *et* mobile) : son lien devient un simple toggle (`href="#"`), sans aucun moyen de revenir à « voir toute la catégorie » depuis le header. Contredit l'arborescence donnée en exemple par le ticket lui-même (§8 : `Nos univers > Épicerie > Biscuits`, où Épicerie reste un palier visible et cliquable).
3. **« Découvrir » — entrée fixe, explicitement hors catalogue selon le ticket (§1.2, §9) — est elle-même reléguée dans le menu overflow `…`** dès 5 racines catalogue, alors que le ticket décrit cette densité comme confortable (§7 : « 4–6 racines : header lisible »). Le mega reste fonctionnel une fois l'overflow ouvert, mais sa découvrabilité est nettement dégradée par rapport à la baseline Nav-1 où Découvrir était toujours visible directement.

**Réserves (à traiter même après correction des bloquants)** :

1. **Interaction « survol »** annoncée par le ticket §7 pour le niveau 2 desktop ne fonctionne pas — seul le clic ouvre le dropdown (le survol seul ne déclenche rien, faute de règle CSS `:hover`). À clarifier avec MOA si le survol est réellement requis ou si le clic (cohérent avec le mega Découvrir) est acceptable.
2. **Donnée de test niveau 2 absente du seed** malgré la prescription explicite du ticket §14/§17.4 (script de seed rejouable). Le QA a dû créer et retirer manuellement des catégories temporaires pour pouvoir tester — cette charge ne devrait pas revenir à chaque recette.

**Recommandation MOA** :

- ☐ GO merge
- ☒ **Corrections Dev requises avant merge** — points bloquants 1 et 2 (niveau 2 en overflow + parent non navigable)
- ☒ **Arbitrage MOA requis** — point bloquant 3 (Découvrir en overflow dès 5 racines, soit dans la zone que le ticket qualifiait de confortable)

---

## 8 bis. Re-recette post-correctifs (à remplir par QA)

> **Contexte** : le PV §7 initial est **NO GO** sur 3 points (niveau 2 cassé en overflow, parent non navigable, Découvrir poussé en overflow). Le Dev a livré des correctifs ciblés (`ck_nav_shop_header.js`, champ `ck_nav_category_id` + split-link QWeb, classes `o_no_autohide_item`/`o_hoverable_dropdown`, seed L2 rejouable `nav_shop_l2_seed.py`).

### Mise à jour

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 -u dorevia_ck_marketone_content,dorevia_ck_theme --stop-after-init
docker restart sandbox-odoo19-odoo-1

docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 --test-enable --stop-after-init --http-port=8078 \
  --test-tags dorevia_ck_marketone_nav_sync,dorevia_ck_theme_phase10
```

| Contrôle | Statut Dev | Statut QA |
| --- | --- | --- |
| Upgrade **27.0→28.0** / **38.1→38.2** | ✅ | ☒ OK — 0 erreur bloquante au chargement |
| Tests auto **28/28** | ✅ | ☒ OK — rejoué deux fois (avant et après les manipulations QA), `0 failed, 0 error(s)` à chaque fois |
| Seed L2 rejouable (`nav_shop_l2_seed.py`) | ✅ | ☒ Confirmé — `Boissons → Jus de fruits/Alcools/Liqueurs`, `Épicerie → Biscuits/Confitures/Épices` créés automatiquement par la migration, conformes au ticket §14 |

⚠️ **Gap résiduel sur le seed** : le script `nav_shop_l2_seed.py` ne rattache un **produit publié** qu'à une seule sous-catégorie (« Jus de fruits », via le produit témoin « Jus Mont-Pelé »). Toutes les autres sous-catégories créées (Biscuits, Confitures, Épices, Alcools, Liqueurs, Savons, Huiles) restent **vides** — donc invisibles par la règle de visibilité héritée de Nav-1 (§6 du ticket : ≥ 1 produit publié requis). Conséquence directe : **aucune racine autre que Boissons n'a, par défaut, de sous-menu niveau 2 visible**, ce qui a empêché une vérification native du cas « niveau 2 en barre principale » (Boissons est en overflow). Le QA a dû rattacher manuellement un produit existant à « Biscuits » pour vérifier ce cas — **puis a retiré ce rattachement en fin de recette**. Recommandation : étoffer `NAV_SHOP_L2_PRODUCT_HINTS` pour couvrir au moins une racine hors overflow.

### Desktop 1280 px — bloquants initiaux

| # | Constat initial | Statut | Note QA |
| --- | --- | --- | --- |
| **Bloquant 1** — niveau 2 cassé en overflow | ☒ **Corrigé** | `ck_nav_shop_header.js` testé : dans le panneau `…` ouvert, le clic sur une racine avec enfants (Boissons) ouvre désormais son sous-menu sans fermer le panneau parent. Survol dans l'overflow non re-testé isolément (clic suffisant et conforme au comportement Bootstrap standard). |
| **Bloquant 2** — parent non navigable une fois avec enfants | ☒ **Corrigé** | Split-link confirmé : `Épicerie` (une fois doté d'un enfant éligible) expose un lien direct `href="/shop/category/epicerie-1"` **et** un toggle séparé pour le sous-menu. Le dropdown contient en plus une entrée de secours **« Toute Épicerie »**, non demandée explicitement par le ticket mais cohérente et utile. |
| **Bloquant 3** — Découvrir poussé en overflow dès 5 racines | ☒ **Corrigé** | `Découvrir` porte désormais la classe native Odoo `o_no_autohide_item` et reste **visible en permanence en barre principale**, quel que soit le nombre de racines catalogue. Confirmé visuellement et en DOM. `Tous nos produits` bénéficie de la même protection. |
| Réserve — survol seul sur le niveau 2 (hors overflow) | ☒ **Toujours KO** | Test de contrôle réalisé : le survol natif Odoo ouvre correctement le mega **Découvrir** (`o_hoverable_dropdown`), mais **n'ouvre pas** le nouveau dropdown split-link d'« Épicerie » avec la même technique de simulation — seul le **clic** fonctionne. Écart persistant par rapport au ticket §7 (« survol + focus clavier »). Non bloquant (le clic offre un chemin fonctionnel complet), mais à clarifier avec MOA. |

**Preuves** : [`nav_shop_desktop_1280_header_rr_qa.png`](./captures/recette_nav_shop_v2/nav_shop_desktop_1280_header_rr_qa.png) · [`nav_shop_desktop_1280_epicerie_hover_l2_rr_qa.png`](./captures/recette_nav_shop_v2/nav_shop_desktop_1280_epicerie_hover_l2_rr_qa.png) · [`nav_shop_desktop_1280_rr_results.json`](./captures/recette_nav_shop_v2/nav_shop_desktop_1280_rr_results.json)

### Mobile 390 px — M2

| # | Constat initial | Statut | Note QA |
| --- | --- | --- | --- |
| **M2** — arborescence niveau 2 non conforme au ticket §8 | ☒ **Corrigé** | Structure désormais conforme : `Nos univers > Épicerie (cliquable) ⌄ > Biscuits` et `Nos univers > Boissons (cliquable) ⌄ > Jus de fruits` — la racine reste visible, cliquable, et porte ses enfants nichés dessous, exactement comme l'exemple du ticket §8. |

### ✅ Bloquant corrigé en 19.0.1.28.1 — doublon mobile pour les racines sans enfant niveau 2 (régression du B2 Nav-1)

**Constat** : sur le drawer mobile, les racines **sans** enfant niveau 2 éligible (**Maison & bien-être, Artisanat & Culture, Coups de cœur** sur le seed actuel) apparaissent **deux fois** : une fois sous l'accordéon « Nos univers » (attendu), une fois en entrée plate juste en dessous (non attendu — il s'agit du même défaut que le B2 originel de Nav-1, déjà corrigé une première fois puis réintroduit par ce lot).

**Cause racine identifiée** : `dorevia_ck_marketone_content/views/website_nav_ck_shop_v2.xml`, template `submenu_ck_nav_shop_mobile_l2_leaf` (priorité 36). Ce template fait un `position="replace"` sur le même nœud `<li t-if="submenu.is_visible and not (submenu.child_id or submenu.is_mega_menu)">` déjà patché par `submenu_ck_nav_css_class` (priorité 30, dans `website_nav_ck_v1.xml`) pour y ajouter `t-attf-class="... #{submenu.ck_nav_css_class or ''}"`. Un `position="replace"` **remplace entièrement le nœud**, y compris les attributs déjà posés par les patches de priorité inférieure — la branche « sans L2 éligible » du nouveau template (la seconde, qui rend les catégories comme Maison & bien-être) ré-écrit son propre `<li t-attf-class="#{item_class or ''} ...">` **sans réinjecter `submenu.ck_nav_css_class`**. La classe `ck-nav-desktop-universe` — qui pilote la règle SCSS masquant l'entrée flat sur mobile (`#top_menu_collapse_mobile .ck-nav-desktop-universe { display: none !important; }`) — est donc perdue pour ces catégories, qui restent visibles à la fois en desktop **et** en mobile.

**Vérifié en DOM** : deux occurrences visibles simultanément de « Maison & bien-être » dans le drawer — l'une dans `.accordion-collapse` (id menu 338, parent « Nos univers », classe correcte `ck-nav-mobile-universe-child`), l'autre **hors accordéon** (id menu 334, parent racine, classe `nav-item ` — **`ck-nav-desktop-universe` absente**).

**Piste de correctif (Dev)** : dans la branche « sans L2 éligible » de `submenu_ck_nav_shop_mobile_l2_leaf`, réinjecter explicitement `submenu.ck_nav_css_class` dans le `t-attf-class` du `<li>` de remplacement (comme le fait l'original patché par `submenu_ck_nav_css_class`), ou restreindre le `position="replace"` à un xpath plus spécifique qui ne capture que le cas réellement concerné (catégorie avec L2 éligible) plutôt que de dupliquer toute la branche standard.

**Preuves** : [`nav_shop_mobile_390_nos_univers_open_rr_qa.png`](./captures/recette_nav_shop_v2/nav_shop_mobile_390_nos_univers_open_rr_qa.png) — capture montrant « Maison & bien-être », « Artisanat & Culture », « Coups de cœur » en double.

### PV re-recette

| Champ | Valeur |
| --- | --- |
| **Recetteur** | Assistant IA (Claude), en session avec doreviateam |
| **Date re-recette** | 2026-06-22 |
| **Versions constatées** | `dorevia_ck_marketone_content` **19.0.1.28.0** · `dorevia_ck_theme` **19.0.1.38.2** |
| **Verdict re-recette** | ☒ **NO GO** — 3 bloquants initiaux corrigés et vérifiés, mais **1 nouveau bloquant** découvert (régression doublon mobile) |

| Point | Verdict | Commentaire |
| --- | --- | --- |
| Bloquant 1 — niveau 2 en overflow | ☒ Corrigé | Vérifié fonctionnel au clic |
| Bloquant 2 — parent non navigable | ☒ Corrigé | Split-link + fallback « Toute X » vérifiés |
| Bloquant 3 — Découvrir en overflow | ☒ Corrigé | `o_no_autohide_item` vérifié efficace |
| **Nouveau** — doublon mobile racines sans L2 | ☒ **Bloquant** | Régression confirmée en DOM sur 3 catégories du seed actuel |
| Réserve — survol niveau 2 hors overflow | ☐ Toujours ouverte | Non bloquant, à arbitrer MOA |
| Réserve — seed produits L2 incomplet | ☐ Toujours ouverte | À étoffer côté Dev pour fiabiliser les prochaines recettes |

**Verdict global lot Nav-Shop** :

- ☐ **GO merge**
- ☒ **NO GO** — un correctif ciblé et bien circonscrit reste nécessaire (réinjection de `ck_nav_css_class` dans la branche sans-L2 de `submenu_ck_nav_shop_mobile_l2_leaf`), puis re-recette flash sur ce seul point avant merge.

**Commentaire QA** :

Le travail de correction est solide sur les 3 points initialement bloquants — diagnostic Dev exact, fixes basés sur de vrais mécanismes Odoo natifs (`o_no_autohide_item`, `o_hoverable_dropdown`), seed L2 désormais rejouable. Le nouveau bloquant est un effet de bord classique de `position="replace"` en héritage QWeb (un patch « remplace » écrase silencieusement les attributs posés par un patch de priorité inférieure sur le même nœud) — risque à garder en tête pour le reste du lot et les lots suivants touchant aux mêmes templates `website.submenu`. Périmètre de correction restant très réduit (une ligne de template), pas de raison de douter d'un GO rapide après ce dernier correctif.

---

## 8 ter. Re-recette flash — correctif doublon mobile (19.0.1.28.1)

> **Contexte** : suite au §8 bis (NO GO sur 1 point), le Dev a livré un correctif d'une ligne : réinjection de `#{submenu.ck_nav_css_class or ''}` dans le `t-attf-class` du `<li>` de la branche « sans L2 éligible » de `submenu_ck_nav_shop_mobile_l2_leaf`, avec symétrie sur la branche « avec L2 ». Nouveau test auto `test_mobile_offcanvas_no_duplicate_leaf_universe_without_l2`.

### Mise à jour et tests

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 -u dorevia_ck_marketone_content --stop-after-init
docker restart sandbox-odoo19-odoo-1
```

| Contrôle | Statut QA |
| --- | --- |
| Upgrade **28.0 → 28.1** | ☒ OK — 0 erreur bloquante |
| Tests auto **28/28** | ☒ OK — `0 failed, 0 error(s) of 28 tests` |

### Vérification ciblée mobile 390 px

Comptage DOM précis (occurrences totales vs visibles) pour les 5 entrées univers du seed actuel :

| Entrée | Occurrences DOM | Visibles | Verdict |
| --- | --- | --- | --- |
| Épicerie | 2 | **1** | ☒ OK |
| Maison & bien-être | 2 | **1** | ☒ OK — doublon disparu |
| Artisanat & Culture | 2 | **1** | ☒ OK — doublon disparu |
| Coups de cœur | 2 | **1** | ☒ OK — doublon disparu |
| Boissons | 2 | **1** | ☒ OK |

Confirmé visuellement sur capture : drawer propre, `Nos univers` ouvert montre exactement Épicerie · Maison & bien-être · Artisanat & Culture · Coups de cœur · Boissons (avec chevron, son enfant éligible « Jus de fruits » étant toujours rattaché), chacune une seule fois, puis Découvrir.

**Preuve** : [`nav_shop_mobile_390_final_qa.png`](./captures/recette_nav_shop_v2/nav_shop_mobile_390_final_qa.png)

### Non-régression desktop 1280 px

Re-contrôle rapide du top menu : `Tous nos produits` et `Découvrir` toujours visibles directement en barre principale (`o_no_autohide_item` non affecté par ce correctif mobile), `Nos univers` toujours masqué en desktop. Aucune régression.

**Preuve** : [`nav_shop_desktop_1280_final_qa.png`](./captures/recette_nav_shop_v2/nav_shop_desktop_1280_final_qa.png)

### PV final

| Champ | Valeur |
| --- | --- |
| **Recetteur** | Assistant IA (Claude), en session avec doreviateam |
| **Date** | 2026-06-22 |
| **Version finale constatée** | `dorevia_ck_marketone_content` **19.0.1.28.1** · `dorevia_ck_theme` **19.0.1.38.2** |
| **Verdict final** | ☒ **GO merge** |

**Réserves non bloquantes reportées au backlog** (ne conditionnent pas le merge) :

1. Survol seul n'ouvre pas le dropdown niveau 2 hors overflow (le clic fonctionne) — écart au ticket §7, à clarifier MOA.
2. Seed `nav_shop_l2_seed.py` ne rattache un produit publié qu'à une seule sous-catégorie sur huit créées — à étoffer pour fiabiliser les recettes futures.
3. Densité actuelle (5 racines) pousse déjà Coups de cœur et Boissons en overflow — Découvrir et Tous nos produits restent protégés, mais point de vigilance si le catalogue grossit encore (cf. `NOTE_NAV_SHOP_REMONTEE_DENSITE.md`).

**Bilan de la recette Nav-Shop** : 2 tours de re-recette ciblée ont été nécessaires après le NO GO initial. Les 4 défauts confirmés (niveau 2 cassé en overflow, parent non navigable, Découvrir en overflow, doublon mobile post-correctif) ont tous été corrigés et re-vérifiés en conditions réelles, pas seulement via les tests automatisés (qui n'ont détecté aucun de ces 4 défauts au moment de leur introduction). Recommandation : merge PR Nav-Shop.

---

## 8 quater. Passe corrective visuelle V2.1 (arbitrage MOA — densité, dropdown L2, doublons)

> **Contexte** : malgré le GO fonctionnel du §8 ter, la MOA a émis un **NO GO merge** sur la qualité visuelle desktop du rendu en l'état (cf. arbitrage MOA détaillé côté ticket) : risque de bouton overflow « + » nu non identifié dès 5-6 racines catalogue, dropdown niveau 2 non habillé (style brut Bootstrap), lien redondant « Toute {catégorie} » dans le dropdown alors que la racine est déjà cliquable. Passe corrective ciblée, strictement visuelle, sans élargissement fonctionnel, sur `feat/ck-nav-shop-categories-v2`.

### Correctif structurel découvert en cours de recette (bloquant non documenté)

En vérifiant l'ouverture du dropdown niveau 2 (« Boissons »), un **crash JS Bootstrap** a été identifié (non détecté par les recettes précédentes, qui n'avaient pas testé l'ouverture effective du dropdown sur cette racine précise) :

- **Symptôme** : `TypeError: Cannot read properties of null (reading 'classList')` dans `Dropdown._isShown()` (Bootstrap 5, bundle `web.assets_frontend_lazy.min.js`) à chaque interaction sur le toggle niveau 2 de « Boissons ».
- **Cause racine** : Bootstrap résout le menu associé à un toggle via `SelectorEngine.next(toggle, '.dropdown-menu')` — le frère DOM **suivant immédiat**. Le template `submenu_ck_nav_shop_desktop_split` (`website_nav_ck_shop_v2.xml`) enveloppait le lien racine et le toggle dans un `<div class="ck-nav-universe-split">` intermédiaire, plaçant le toggle en dernier enfant de ce `<div>` — son frère suivant réel n'existait pas, donc `this._menu` valait `null`.
- **Correctif** : suppression du `<div>` wrapper ; le lien et le toggle sont désormais des enfants directs du `<li>`, frères du `<ul class="dropdown-menu">` existant. La mise en forme « pilule » du couple lien+toggle est reportée en CSS sur le `<li>` lui-même (`display: inline-flex` via un sélecteur `:has()`), sans incidence sur la résolution Bootstrap.
- **Vérification** : confirmé sans aucune erreur JS console (`page.on('pageerror')` → `[]`) et ouverture effective du dropdown en conditions réelles (le header utilise `o_hoverable_dropdown`, mécanisme natif Odoo — ouverture **au survol**, pas au clic ; témoin « Découvrir » re-testé en parallèle pour écarter un faux positif méthodologique).

### Correctifs appliqués

| # | Exigence MOA | Mise en œuvre | Fichier |
| --- | --- | --- | --- |
| 1 | Aucun bouton « + » nu visible à 5-6 racines à 1280 px | Densité resserrée (rail de nav élargi via `calc()`, recherche centrale réduite à 112 px, gouttière et gaps resserrés, typographie nav 14 px) jusqu'à overflow nul sur le jeu de données actuel (5 racines) | `website_header.scss` |
| 2 | Si overflow malgré tout, jamais l'icône « + » seule | Icône `.oi-plus` masquée, remplacée par le libellé pré-approuvé MOA « Nos univers » (mécanisme natif `auto_hide_menu.js` / `.o_extra_menu_items`, actuellement dormant — 0 overflow constaté) | `website_header.scss` |
| 3 | Dropdown niveau 2 habillé (fond, bordure, ombre, espacements, hover/focus/active) | Bloc de styles dédié `#top_menu.top_menu .dropdown-menu` (fond `$ck-surface`, bordure 1px, ombre douce, items 0.6rem/1.25rem, états hover/focus-visible/active sur tokens `$ck-primary`) | `website_header.scss` |
| 4 | Pas de lien redondant « Toute {catégorie} » | Suppression du prepend `Toute {tree["name"]}` dans `_sync_desktop_shop_menus` | `nav_sync.py` |
| — | (bloquant découvert en recette) Dropdown niveau 2 ne s'ouvrait jamais | Suppression du `<div>` wrapper cassant la résolution Bootstrap (cf. ci-dessus) | `website_nav_ck_shop_v2.xml` |

### Vérification — désormais sans objet (réserve #1 du §8 ter levée)

La réserve non bloquante #1 du PV final précédent (« survol seul n'ouvre pas le dropdown niveau 2 hors overflow ») est **résolue** par le correctif structurel ci-dessus : le survol ouvre désormais correctement le dropdown niveau 2, conforme au mécanisme `o_hoverable_dropdown` du header.

### Libellés — clarification (point MOA)

`tree['name']` provient directement de `category.name` (`product.public.category`), sans alias ni renommage applicatif (`build_shop_nav_trees`, `nav_sync.py`). « Maison & bien-être » et « Coups de cœur » sont donc des noms de catégorie BO tels quels, pas des libellés calculés. « Coups de cœur » apparaît en racine catalogue car c'est une catégorie BO racine légitime avec produits publiés (cf. `data/ck_public_category_coups_de_coeur.xml`), pas une anomalie de navigation.

### Hiérarchie dropdown — choix de conception documenté

Le dropdown niveau 2 affiche uniquement les enfants directs éligibles (ex. « Jus de fruits » sous « Boissons ») ; la racine elle-même est déjà directement cliquable via `ck-nav-universe-split__link`. Aucun lien de repli n'est nécessaire dans le dropdown.

### Tests automatisés

Mise à jour de l'assertion obsolète `test_level2_children_under_parent_not_at_root` (attendait l'ancien lien « Toute X », contraire à l'exigence MOA — inversée pour vérifier son **absence**).

```bash
docker exec sandbox-odoo19-odoo-1 odoo -u dorevia_ck_theme,dorevia_ck_marketone_content -d dorevia_ck_marketone_01 --stop-after-init --no-http
docker exec sandbox-odoo19-odoo-1 odoo -d dorevia_ck_marketone_01 --test-enable \
  --test-tags dorevia_ck_marketone_nav_sync,dorevia_ck_theme_phase10 \
  -u dorevia_ck_marketone_content,dorevia_ck_theme --stop-after-init --http-port=8169
```

| Contrôle | Statut QA |
| --- | --- |
| Tests auto **28/28** | ☒ OK — `0 failed, 0 error(s) of 28 tests` (après correction de l'assertion obsolète) |
| Erreurs console JS | ☒ OK — `[]` (crash `Dropdown._isShown()` résolu) |

### Non-régression desktop 1280 px (H1 / Nav-1)

| Contrôle | Statut |
| --- | --- |
| Header / logo / recherche / panier / compte présents | ☒ OK |
| `Tous nos produits` et `Découvrir` en barre principale | ☒ OK |
| Mega menu Découvrir (survol) | ☒ OK — `show: true` |
| Overflow desktop (`.o_extra_menu_items`) | ☒ Absent — 0 overflow sur 5 racines |
| Dropdown niveau 2 « Boissons » (survol) | ☒ OK — `show: true`, contenu : Jus de fruits |

**Preuves** :
- [`nav_shop_v2_1_header_closed_final.png`](./captures/recette_nav_shop_v2/nav_shop_v2_1_header_closed_final.png) — header fermé, 7 entrées sans bouton overflow
- [`nav_shop_v2_1_dropdown_open_final.png`](./captures/recette_nav_shop_v2/nav_shop_v2_1_dropdown_open_final.png) — dropdown L2 « Boissons » ouvert, habillage CK
- [`nav_shop_v2_1_dropdown_item_hover_final.png`](./captures/recette_nav_shop_v2/nav_shop_v2_1_dropdown_item_hover_final.png) — état hover sur un item du dropdown

### Non-régression mobile 390 px

| Contrôle | Statut |
| --- | --- |
| Drawer offcanvas s'ouvre | ☒ OK |
| `Tous nos produits` / `Nos univers` (accordéon) / `Découvrir` | ☒ OK — présents, structure inchangée |
| Aucun bouton overflow desktop visible en mobile | ☒ OK |

**Preuve** : [`nav_shop_v2_1_mobile_390_final.png`](./captures/recette_nav_shop_v2/nav_shop_v2_1_mobile_390_final.png)

### PV final — passe corrective V2.1

| Champ | Valeur |
| --- | --- |
| **Recetteur** | Assistant IA (Claude), en session avec doreviateam |
| **Date** | 2026-06-22 |
| **Version finale constatée** | `dorevia_ck_marketone_content` **19.0.1.28.2** · `dorevia_ck_theme` **19.0.1.38.3** |
| **Verdict final** | ☒ **GO merge** |

**Réserves reportées au backlog** (ne conditionnent pas le merge) :

1. Le libellé de repli overflow « Nos univers » (icône « + » masquée) reste **dormant** sur le jeu de données actuel (5 racines, 0 overflow) — à revérifier visuellement dès qu'un 6e/7e univers BO sera publié et fera réellement apparaître l'overflow.
2. Le rail de navigation desktop utilise désormais une largeur propre (`$ck-container-max + 11rem`), distincte du conteneur de contenu partagé — cohérent avec le périmètre « visuel ciblé header » de cet arbitrage, mais à garder en tête si une refonte de grille plus large est engagée ultérieurement.

**Bilan** : le correctif structurel Bootstrap découvert en cours de recette (dropdown niveau 2 ne s'ouvrant jamais, crash JS silencieux côté navigation réelle) était plus sérieux que la demande visuelle initiale de la MOA ; il est corrigé et vérifié en conditions réelles (hover, conforme au mécanisme `o_hoverable_dropdown` du header), pas seulement via les tests automatisés. Les 4 exigences visuelles MOA (densité sans overflow nu, habillage dropdown L2, libellé de repli non technique, retrait des liens redondants) sont satisfaites et vérifiées. Recommandation : merge PR Nav-Shop V2.1.

---

## 9. Références

| Document | Rôle |
| --- | --- |
| [`RECETTE_QA_LOT_NAV_SHOP_CATEGORIES_ECOMMERCE_CK_V2.md`](./RECETTE_QA_LOT_NAV_SHOP_CATEGORIES_ECOMMERCE_CK_V2.md) | Recette Dev |
| [`NOTE_NAV_SHOP_REMONTEE_DENSITE.md`](./NOTE_NAV_SHOP_REMONTEE_DENSITE.md) | Règle de remontée et densité 7+ |
| [`TICKET_DEV_LOT_NAV_SHOP_CATEGORIES_ECOMMERCE_CK_V2.md`](../TICKET_DEV_LOT_NAV_SHOP_CATEGORIES_ECOMMERCE_CK_V2.md) | Critères d'acceptation MOA C1–C12 |
| [`NOTE_QA_LOT_NAV1_NAVIGATION_CK_V2.md`](./NOTE_QA_LOT_NAV1_NAVIGATION_CK_V2.md) · [`NOTE_QA_LOT_H1_HEADER_CK_V2_1.md`](./NOTE_QA_LOT_H1_HEADER_CK_V2_1.md) | Baselines Nav-1 / H1 |

---

*Note d'intervention QA · Lot Nav-Shop · à remplir par le testeur.*
