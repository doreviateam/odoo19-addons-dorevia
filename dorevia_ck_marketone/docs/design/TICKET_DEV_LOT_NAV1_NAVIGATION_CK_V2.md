# Ticket Dev — Lot Nav-1 · Navigation CK V2 : menu commerce + Découvrir

| Champ | Valeur |
| --- | --- |
| **Projet** | `dorevia_ck_marketone` · C-Kreyol / CK |
| **Lot** | **Nav-1** — Phase 1 navigation |
| **Modules** | `dorevia_ck_marketone_content` (menus, catégories, bootstrap) · `dorevia_ck_theme` (tests header, styles mega si besoin) |
| **Type** | Navigation / header · lot technique recettable |
| **Priorité** | Haute |
| **Statut** | **GO MOA — exécution Nav-1** |
| **Instance recette** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **Documents source** | [`note_06.md`](../cadrage/note_06.md) · [`note_06_reponse_moa.md`](../cadrage/note_06_reponse_moa.md) · [`note_06_retour_dev.md`](../cadrage/note_06_retour_dev.md) |

```text
Objectif : transformer les arbitrages MOA Navigation V2 en livraison technique recettable —
header / menus uniquement. Pas de reprise Home, fiche produit, communauté ni checkout.

Nav-1 organise la navigation cible et applique la règle de visibilité des liens.
Il ne crée pas encore les capacités éditoriales ou communautaires sous-jacentes.
Header / menu maintenant · activation Blog / Forum sur tickets dédiés.
```

---

## 1. Contexte

Le brief Navigation CK V2 a été **amendé MOA** (2026-06-21) après retour Dev. Les arbitrages sont actés :

* pivot assumé depuis le header Phase 1 livré ;
* menu commerce top-level + **Découvrir** éditorial ;
* **Professionnels** relocalisé sous Découvrir ;
* règle de visibilité des liens (pas de 404) ;
* **Home S4 hors périmètre**.

**État de départ (Phase 1 livré)** :

> Boutique · Découvrir · Professionnels

**Cible Lot Nav-1 (desktop 1280 px)** :

> Tous nos produits · Épicerie · Boissons · Soin & Bien-être · Artisanat · Découvrir

**Cible mobile 390 px** (regroupement autorisé — voir §4 bis) :

> Tous nos produits · Nos univers · Découvrir

Le mega-menu **Découvrir** ne doit **plus** dupliquer les entrées commerce (« Acheter par univers » retiré du mega).

---

## 2. Périmètre IN (Lot Nav-1)

| # | Livrable |
| --- | --- |
| 1 | Assumer le **pivot Navigation V2** (retrait top-level Boutique / Professionnels au profit de la cible MOA) |
| 2 | Menu principal cible synchronisé (`website.menu`) |
| 3 | Mega-menu **Découvrir** avec sous-entrées cible (ordre MOA) |
| 4 | **Professionnels** → sous **Découvrir** (`/professionnels`) · plus en top-level |
| 5 | Correspondance entrées commerce ↔ `product.public.category` (tableau §5) |
| 6 | **Règle de visibilité** : aucun lien menu/mega visible si cible absente, non publiée ou 404 |
| 7 | Vérification / création catégories racines BO si nécessaire (seed module ou doc MOE) |
| 8 | Mise à jour tests header (`dorevia_ck_theme_phase10` et tags associés) |
| 9 | Recette documentée desktop **1280 px** + mobile **390 px** (regroupement **Nos univers** si implémenté) |
| 10 | Non-régression : recherche · compte · panier · boutique · accès Professionnels · parcours contact |
| 11 | Retrait CTA fort **Contactez-nous** du header · relocalisation Découvrir ou footer (§4 ter) |
| 12 | Contraste WCAG texte header (`#bf360c` · usages `color:` uniquement — §4 quater) |
| 13 | Règle visibilité catégories renforcée + tests cas limites (§7 bis) |

---

## 3. Hors périmètre (à ne pas toucher)

Rappel explicite — **interdit dans ce lot** :

* refonte **Home S4** (« Acheter par univers ») ;
* refonte **fiche produit** ;
* **activation automatique** de `website_blog` (voir §3 bis) ;
* **activation** d’un module forum / parcours communautaire réel (voir §3 bis) ;
* forum complet ;
* contribution utilisateur ;
* modération ;
* compte contributeur ;
* marketplace ;
* panier / checkout ;
* automatisation avancée des contenus liés aux produits ;
* refonte shop complète ;
* nouveau modèle métier éditorial / communautaire ;
* pages teaser **Communauté** / **Contribuer** non validées MOA.

Toute évolution sur ces sujets = **ticket distinct** + arbitrage MOA.

---

## 3 bis. Précision MOA — Blog et Forum / Communauté

**Le lot Nav-1 ne donne pas de GO automatique pour activer Blog ou Forum.**

Nav-1 pose la **structure de navigation** et la **règle de visibilité**. Il ne déploie pas les capacités éditoriales ou communautaires sous-jacentes.

### Forum / Communauté

| Règle MOA | Exigence Lot Nav-1 |
| --- | --- |
| Module forum | **Ne pas activer** |
| Parcours communautaire réel | **Ne pas créer** |
| Contribution · modération · compte contributeur | **Hors lot** (déjà §3) |
| Entrées **Communauté** et **Contribuer** | **Masquées** tant qu’aucune page teaser publiée n’a été **validée MOA** |

### Blog

| Règle MOA | Exigence Lot Nav-1 |
| --- | --- |
| `website_blog` | **Ne pas activer automatiquement** sans arbitrage MOA |
| Module déjà actif + `/blog` OK | Le lien **Le blog CK** **peut** apparaître dans Découvrir |
| Module inactif ou route KO | Lien **masqué** |
| Activation + structuration éditoriale | **Lot séparé**, sauf décision MOA explicite |

### Conséquence Dev

* le mega Découvrir peut être **partiellement peuplé** à la livraison Nav-1 (ex. **Professionnels** + entrées CMS déjà publiées) ;
* l’absence de liens Blog / Communauté / Contribuer en recette Nav-1 est **conforme MOA**, pas un échec de livraison ;
* ne pas installer de module ni bootstrapper de contenu blog/forum « pour remplir le menu ».

---

## 3 ter. Amendement Nav-1 bis — Header / mobile / visibilité (MOA)

Ces points **ne changent pas le périmètre fonctionnel** Nav-1 (navigation / header uniquement).

### 1. Bouton « Contactez-nous »

| Règle MOA | Exigence |
| --- | --- |
| Parcours contact | **Conservé** (`/contactus`) — pas de suppression |
| CTA terracotta fort à droite du header | **Retiré** en Nav-1 (6 entrées top-level desktop) |
| Relocalisation | **Priorité** : mega **Découvrir**, **après Professionnels** · **à défaut** : footer existant |
| Concurrence visuelle | Éviter tout CTA fort concurrent avec le menu commerce + Découvrir |

### 2. Mobile 390 px — regroupement « Nos univers »

Desktop **1280 px** : menu plat à 6 entrées (cf. §4).

Mobile **390 px** : regroupement **autorisé et recommandé** :

> Tous nos produits · **Nos univers** · Découvrir

Sous **Nos univers** (accordéon / sous-menu drawer) :

* Épicerie ;
* Boissons ;
* Soin & Bien-être ;
* Artisanat.

Objectifs : drawer plus court · lisibilité · **zéro overflow horizontal**.

Implémentation : CSS / structure offcanvas Odoo ou regroupement menu enfant `website.menu` — **sans** modifier le rendu desktop.

### 3. Libellé « Soin & Bien-être »

Remplacer **Soin** par **Soin & Bien-être** (menu desktop, sous-menu mobile, mega si applicable).

Mapping BO : aligner ou **documenter** si la catégorie technique conserve un autre nom (ex. `Maison & bien-être`).

### 4. Contraste WCAG — usages texte header uniquement

Si `#d84315` (`$ck-primary`) est utilisé comme **couleur de texte** dans le header ou les liens nav :

* remplacer par **`#bf360c`** (token existant `$ck-primary-text` / `$ck-primary-hover` dans `ck_tokens.scss`) ;

**Ne pas** modifier aveuglément les fonds bouton / badge / CTA où le primary reste en background.

Périmètre correction Nav-1 : **header + liens navigation + mega-menu Découvrir** (usages `color:` uniquement).

### 5. Règle de visibilité catégories

Voir **§7 bis** — matrice des cas limites (absent / vide / unpublished-only / published).

### 6. Tests complémentaires

Voir **§9** et critères **C15–C17** — CTA Contact · mobile Nos univers · visibilité catégories · libellé Soin & Bien-être.

---

## 4. Menu principal cible

### Desktop 1280 px

Ordre et libellés **figés MOA** :

| Seq. | Libellé menu | Type | Cible attendue |
| ---: | --- | --- | --- |
| 10 | **Tous nos produits** | Lien simple | `/shop` |
| 20 | **Épicerie** | Lien catégorie | Catégorie racine Épicerie (slug BO) |
| 30 | **Boissons** | Lien catégorie | Catégorie racine Boissons |
| 40 | **Soin & Bien-être** | Lien catégorie | Catégorie racine Soin (nom BO à mapper — §6) |
| 50 | **Artisanat** | Lien catégorie | Catégorie racine Artisanat |
| 60 | **Découvrir** | Mega-menu natif CE | `#` + `mega_menu_content` |

### Mobile 390 px

Voir §3 ter · regroupement **Nos univers** (recommandé MOA).

**Retraits attendus du top-level** :

* ~~Boutique~~ → remplacé par **Tous nos produits** ;
* ~~Professionnels~~ → relocalisé sous Découvrir ;
* ~~CTA fort **Contactez-nous**~~ à droite du header → retiré · relocalisé §5 ;

**Entrées transverses inchangées** (hors menu principal) : logo → `/` · recherche · compte · panier.

---

## 5. Sous-menu Découvrir — ordre et rôle

Mega-menu **sans colonne commerce**. Ordre cible :

| # | Libellé | Rôle | Cible type | Visibilité |
| ---: | --- | --- | --- | --- |
| 1 | Producteurs & territoires | Confiance · origine | Page(s) CMS / hub | Si page publiée |
| 2 | Histoires de produits | Profondeur produit | Page(s) CMS | Si page publiée |
| 3 | Recettes & usages | Usage · cuisine | `/recettes` ou hub | Si page publiée |
| 4 | Le blog CK | Éditorial marque | `/blog` | **Si** `website_blog` installé **et** `/blog` répond · sinon **masqué** · pas d’activation auto |
| 5 | **Professionnels** | Parcours B2B | `/professionnels` | **Oui** (page existante Phase 9) |
| 6 | **Contactez-nous** | Parcours contact | `/contactus` | **Oui** — relocalisé depuis CTA header · **après Professionnels** |
| 7 | Communauté | Teaser communautaire | Page CMS | **Masqué** sauf page teaser **validée MOA** et publiée |
| 8 | Contribuer | Teaser contribution | Page CMS | **Masqué** sauf page teaser **validée MOA** et publiée |

**Interdit dans le mega** : liens dupliqués vers Épicerie · Boissons · Soin & Bien-être · Artisanat · `/shop`.

**Fallback contact** : si le lien n’est pas retenu dans le mega, vérifier préservation du parcours via **footer** (non-régression `/contactus`).

---

## 6. Correspondance catalogue BO (MOE / Dev)

Tableau opérationnel à **compléter en recette** sur l’instance seed. Stratégie MOA validée ; slugs à confirmer côté BO.

| Entrée menu | Catégorie Odoo cible | URL / slug | Statut instance | Produit publié min. |
| --- | --- | --- | --- | --- |
| Tous nos produits | Catalogue complet | `/shop` | Existant | Oui |
| Épicerie | Racine Épicerie | ex. `/shop/category/epicerie-…` | À confirmer / aligner | Oui |
| Boissons | Racine Boissons | À confirmer | À confirmer / créer | Oui |
| Soin & Bien-être | Racine Soin / `Maison & bien-être` | ex. slug BO à confirmer | Libellé menu MOA · nom catégorie BO documenté si différent | ≥ 1 produit **publié site** |
| Artisanat | Racine Artisanat | ex. `/shop/category/artisanat-…` | À confirmer | Oui |

**Tâche Dev** :

1. inventorier les `product.public.category` publiées sur l’instance seed ;
2. mapper ou créer les racines manquantes (data XML module si reproductible) ;
3. ne **pas** exposer en menu une catégorie sans **au moins un produit publié sur le site** (cf. §7 bis) ;
4. documenter le mapping final dans ce ticket (§ complété post-dev) ou note recette dédiée.

**Note Home S4** : les libellés S4 (Épicerie créole · Soin & bien-être · Artisanat) peuvent différer temporairement du header Nav V2 — **accepté MOA** ; ne pas modifier S4 dans ce lot.

---

## 7. Règle de visibilité des liens

Règle **validée MOA** — à implémenter :

> Un lien ne doit apparaître en navigation que si la cible existe, est publiée et ne génère pas de 404.

S’applique à :

* entrées catégories commerce ;
* entrées mega Découvrir ;
* **Le blog CK** : visible uniquement si module blog actif et route `/blog` valide — **sans installation module dans ce lot** ;
* **Communauté** / **Contribuer** : visibles uniquement si page teaser **validée MOA** et publiée.

**Comportement attendu** :

* catégorie absente ou vide → entrée **masquée** (pas de lien mort) ;
* page CMS non publiée → entrée mega **absente** ;
* `/professionnels` → **visible** sous Découvrir (page bootstrap existante) ;
* `website_blog` absent ou `/blog` en échec → **Le blog CK** **absent** du mega ;
* **Communauté** / **Contribuer** → **absents** par défaut Nav-1 (pas de teaser MOA acté).

Implémentation recommandée : synchronisation menus via hook post-init / migration module (`dorevia_ck_marketone_content`) avec contrôle programmatic (catégorie + count produits publiés, `website.page` publiée, HTTP 200 en test ou check BO).

---

## 7 bis. Règle de visibilité catégories (renforcée MOA)

Une entrée catégorie du menu ne doit apparaître **que si** :

1. la catégorie **existe** ;
2. elle est **publiée / exploitable** côté site ;
3. elle contient **au moins un produit publié sur le site** ;
4. l’URL cible ne conduit pas à une expérience **vide** ou **404-like**.

### Cas limites à tester explicitement

| Cas | Entrée menu attendue |
| --- | --- |
| Catégorie absente | **Masquée** |
| Catégorie existante mais vide (0 produit) | **Masquée** |
| Catégorie avec produits **non publiés** uniquement | **Masquée** |
| Catégorie avec **≥ 1 produit publié** sur le site | **Visible** |

Ces règles s’appliquent desktop et sous-entrées **Nos univers** mobile.

---

## 8. Implémentation attendue

### 8.1 Principes

* Odoo 19 CE · mega-menu natif (`is_mega_menu` · `mega_menu_content`) ;
* pas de surcouche front autonome · pas de HTML maquette injecté ;
* menus reproductibles module (data XML + hook), pas configuration manuelle instance-only ;
* **ne pas** ajouter `website_blog` ni module forum aux dépendances / hooks Nav-1 ;
* styles header existants (`website_header.scss`) — CSS additionnel **minimal** si densité 6 entrées + mega + regroupement mobile ;
* contraste texte nav : `$ck-primary-text` (`#bf360c`) sur usages `color:` header — **pas** de changement global des fonds primary ;
* bump version module(s) touché(s) + `-u` documenté.

### 8.2 Fichiers probables

| Zone | Fichiers / zone |
| --- | --- |
| Menus + seed catégories | `dorevia_ck_marketone_content/data/` · `hooks.py` (sync nav) |
| Tests header | `dorevia_ck_theme/tests/test_ck_phase10_header_compose.py` · tests sync menu catégories (`dorevia_ck_marketone_content`) |
| Styles mega (si besoin) | `dorevia_ck_theme/static/src/scss/website_header.scss` |
| Recette | `docs/design/maquette_01.2/RECETTE_QA_LOT_NAV1_NAVIGATION_CK_V2.md` (à créer post-dev) |

### 8.3 Pivot explicite

Documenter dans le commit / recette :

* header Phase 1 = structure initiale historique ;
* Lot Nav-1 = **évolution assumée**, non régression accidentelle.

---

## 9. Tests à mettre à jour

| Test / tag | Action |
| --- | --- |
| `dorevia_ck_theme_phase10` · `test_header_ck_chrome_on_home` | Remplacer assertions `Boutique` / top-level `Professionnels` par cible Nav V2 |
| Idem | Vérifier **Tous nos produits** · **Soin & Bien-être** · catégories visibles · **Découvrir** + `o_mega_menu` |
| Idem | **Professionnels** via mega · **pas** top-level |
| CTA Contact | **Absence** du CTA fort terracotta `Contactez-nous` en top-level header |
| CTA Contact | Présence lien contact dans mega Découvrir (après Professionnels) **ou** footer — parcours `/contactus` OK |
| Mobile 390 | Si regroupement implémenté : entrée **Nos univers** + sous-entrées commerce · drawer ≤ 3 top-level |
| Visibilité catégories | Catégorie vide → entrée absente · produits non publiés seuls → entrée absente · ≥ 1 publié → visible |
| Routes non-régression | `/shop` · `/professionnels` · `/contactus` · recherche · panier — inchangées |
| Sync menu (recommandé) | Tests unitaires hook nav : cas §7 bis (absent / vide / unpublished-only / published) |

Commande recette :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 --test-enable --stop-after-init --http-port=8076 \
  --test-tags dorevia_ck_theme_phase10
```

Upgrade post-livraison :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 -u dorevia_ck_marketone_content,dorevia_ck_theme --stop-after-init
```

---

## 10. Recette QA (Dev + Testeur)

### Desktop 1280 px

| # | Scénario | Attendu |
| ---: | --- | --- |
| R1 | Menu principal visible | Tous nos produits · Épicerie · Boissons · **Soin & Bien-être** · Artisanat · Découvrir |
| R2 | Tous nos produits | `/shop` · 200 |
| R3 | Chaque catégorie visible | URL catégorie · 200 · ≥ 1 produit publié listé |
| R4 | Mega Découvrir ouvert | Sous-entrées selon §7 · **Professionnels** · **Contactez-nous** après Pro · Blog / Communauté / Contribuer absents si §3 bis |
| R5 | Mega sans commerce | Aucun lien dupliqué Épicerie/Boissons/Soin & Bien-être/Artisanat/shop |
| R6 | Top-level | **Pas** Professionnels · **pas** CTA fort Contactez-nous à droite |
| R7 | Chrome header | Recherche · panier · compte · logo OK · contraste texte nav + mega (usages `color:` → `#bf360c`) |
| R8 | Tenue visuelle 1280 | **Soin & Bien-être** sans retour ligne · troncature · chevauchement logo ou chrome (cf. §10 bis) |

### Mobile 390 px

| # | Scénario | Attendu |
| ---: | --- | --- |
| M1 | Burger / offcanvas | **Tous nos produits · Nos univers · Découvrir** (si regroupement retenu) · zéro overflow horizontal |
| M2 | Nos univers | Accordéon : clic parent **déplie sans naviguer** · enfants naviguent · pas de confusion déplier/page (cf. §10 bis) |
| M3 | Professionnels · Contact | Accessibles depuis Découvrir · `/professionnels` · `/contactus` OK |
| M4 | Non-régression | Panier · recherche · ajout produit shop OK |
| M5 | Visibilité catégories | Entrées masquées si catégorie vide ou sans produit publié (§7 bis) |

### Non-régression fonctionnelle

| Parcours | Attendu |
| --- | --- |
| Recherche | Modal / barre OK |
| Compte | Lien connexion OK |
| Panier | Compteur + `/shop/cart` OK |
| Boutique | `/shop` + filtre catégorie OK |
| Professionnels | `/professionnels` · contenu `ck-pro-page` intact |
| Contact | `/contactus` accessible (mega Découvrir et/ou footer) |
| Home S4 | **Inchangée** — 3 cards univers · pas de diff arch home |

---

## 10 bis. Recette fin de lot — points de vigilance (non bloquants MOA)

À vérifier **en fin de lot** par Dev / Testeur. Ces points **ne bloquent pas** le GO merge s’ils sont documentés avec reserve mineure MOA, mais doivent être contrôlés explicitement dans la recette Nav-1.

### 1. Desktop 1280 px — libellé « Soin & Bien-être »

Le libellé est **validé MOA**. Vérifier la **tenue visuelle** du menu à 6 entrées top-level :

| Point de contrôle | Attendu |
| --- | --- |
| Retour à la ligne | Aucun libellé menu sur 2 lignes |
| Troncature | Aucune ellipse / texte coupé illisible |
| Logo | Pas de chevauchement avec la marque |
| Chrome droit | Pas de chevauchement avec recherche · compte · panier |
| Espacement | Rythme lisible — pas d’entrées trop serrées |

Si un ajustement CSS minimal est nécessaire (gap, `font-size`, padding) : **périmètre header autorisé** — sans modifier le libellé MOA.

### 2. Contraste dans le mega-menu Découvrir

La correction contraste couvre **tous les usages texte de navigation**, y compris les liens du mega-menu Découvrir.

| Point de contrôle | Attendu |
| --- | --- |
| Liens header top-level | Aucun `color: #d84315` si contraste AA échoue |
| Liens mega Découvrir | Idem — terracotta en `color:` → token texte `$ck-primary-text` / `#bf360c` |
| Fonds bouton / badge | **Inchangés** — ne pas remplacer aveuglément `$ck-primary` en background |

### 3. Mobile 390 px — comportement « Nos univers »

**Si** le regroupement mobile est implémenté :

| Point de contrôle | Attendu |
| --- | --- |
| Clic sur **Nos univers** | **Déplie** le sous-menu · **ne navigue pas** |
| Liens enfants | Épicerie · Boissons · Soin & Bien-être · Artisanat → navigation correcte |
| Drawer / offcanvas | Comportement compréhensible · hiérarchie claire |
| Overflow | **Zéro** overflow horizontal |
| UX | Pas de confusion entre « déplier » et « ouvrir une page » |

Documenter le comportement retenu (natif Odoo vs CSS/JS minimal) dans la recette post-dev.

---

## 11. Critères d’acceptation MOA

| # | Critère | Attendu |
| ---: | --- | --- |
| C1 | Pivot Navigation V2 | Documenté · header cible conforme brief amendé |
| C2 | Menu commerce | Libellés MOA incl. **Soin & Bien-être** |
| C3 | Professionnels | Sous Découvrir · parcours `/professionnels` non régressé |
| C4 | Mega Découvrir | Ordre MOA · **Contactez-nous** après Professionnels · pas de duplication commerce |
| C5 | Visibilité liens | Aucun lien menu/mega vers 404 · règle §7 bis appliquée |
| C6 | Catégories BO | Mapping documenté · masquage si absent / vide / unpublished-only |
| C7 | Home S4 | **Non modifiée** |
| C8 | Tests header | Tags phase10 + sync nav · cas §9 couverts |
| C9 | Desktop 1280 | Recette R1–R8 OK |
| C10 | Mobile 390 | Recette M1–M5 OK · regroupement Nos univers · pas d’overflow |
| C10 bis | Vigilance fin de lot | §10 bis contrôlé · réserves documentées si besoin |
| C11 | Hors périmètre | Aucun diff fiche produit / checkout / communauté backend |
| C12 | Blog | Pas d’activation auto `website_blog` · lien masqué si module/route absent |
| C13 | Forum / Communauté | Pas de module forum · **Communauté** / **Contribuer** masqués sans teaser MOA |
| C14 | Périmètre Nav-1 | Navigation + visibilité seulement · pas de capacité éditoriale/communautaire créée |
| C15 | CTA Contact header | **Pas** de CTA fort terracotta top-level · contact via Découvrir ou footer |
| C16 | Contraste header + mega | Usages **texte** nav et mega Découvrir en `#bf360c` · fonds boutons/badges inchangés |
| C17 | Catégories — cas limites | Tests §7 bis verts (absent / vide / unpublished-only / published) |

---

## 12. Livrables fin de lot

1. Code menus + seed / sync catégories (PR module).
2. Tests header mis à jour · CI / `--test-tags` verts.
3. Tableau §6 complété (slugs réels instance).
4. Recette QA `RECETTE_QA_LOT_NAV1_NAVIGATION_CK_V2.md` incluant checklist **§10 bis**.
5. Bump versions `__manifest__.py` des modules touchés.

---

## 13. Verdict attendu

| Rôle | Verdict |
| --- | --- |
| Dev | Lot Nav-1 livré · recette auto OK |
| Testeur | Recette desktop + 390 px · non-régression OK |
| MOA | GO merge · enchaînement **Lot Nav-2** (pages éditoriales Découvrir) · **Lot Blog** / **Lot Communauté** sur tickets dédiés si arbitrage MOA |

---

*Ticket Dev Lot Nav-1 · Navigation CK V2 · GO exécution MOA · amendements Blog/Forum + Nav-1 bis + recette §10 bis.*
