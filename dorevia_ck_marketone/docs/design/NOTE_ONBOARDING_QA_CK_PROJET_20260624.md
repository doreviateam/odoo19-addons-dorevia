# Note — Onboarding QA · Projet C-Kréyòl Marketone

| Champ | Valeur |
| --- | --- |
| Projet | `dorevia_ck_marketone` |
| Statut | Actif — note d’accueil QA |
| Date | 2026-06-24 |
| Responsable | Dev (rédaction) · Architecte (validation périmètre) |
| Audience | QA expert Odoo — prise de poste |
| Remplace | — |
| Remplacé par | — |

---

## 1. Objet de cette note

Bienvenue sur le projet **C-Kréyòl Marketone** : boutique Odoo 19 CE orientée e-commerce B2C, avec une promesse forte (sélection créole, origines identifiées, confiance d’achat).

Cette note décrit **l’état actuel du projet** au moment de votre arrivée : organisation, environnement, lots livrés, documentation, méthode de recette et points ouverts. Elle ne remplace pas les recettes détaillées par lot ; elle indique **où les trouver** et **comment travailler** avec l’équipe.

---

## 2. Rôles dans l’équipe

| Rôle | Mission | Votre interface |
| --- | --- | --- |
| **Architecte projet** | Vision produit, arbitrages MOA, découpage des lots, validation d’intention UX | Cadrage, GO/NO GO fonctionnel, priorisation des réserves |
| **Dev expert Odoo** (référent technique) | Implémentation, héritages QWeb/SCSS, tests automatisés, notes de recette Dev, non-régression Odoo | Spécifications exécutables, correctifs, scripts QA, réponses sur le « comment c’est codé » |
| **QA expert Odoo** (vous) | Recette manuelle et structurée, validation des livrables par lot, remontée des écarts avec preuves, consolidation des verdicts | Protocoles `RECETTE_*`, captures, checklists MOA, signalement des régressions |

**Doctrine partagée :**

```text
Odoo reste le moteur.
C-Kréyòl devient la lecture commerciale.
```

Le QA ne valide pas une refonte hors Odoo : il contrôle que l’expérience CK est correcte **sans casser** recherche, tri, filtres, URLs, panier, catégories et responsive.

---

## 3. Périmètre technique — ce qui compte

### 3.1 Modules actifs (seuls à recetter)

| Module | Version (juin 2026) | Rôle |
| --- | --- | --- |
| `dorevia_ck_theme` | 19.0.1.56.0 | Thème CK : tokens SCSS, layout, snippets, header, shop, cards, héritages `website_sale` |
| `dorevia_ck_marketone_content` | 19.0.1.38.0+ | Contenu métier : navigation, pages CMS, curation home, données catalogue, rayons éditoriaux |

**Dépôt code :** `odoo19-addons-dorevia` (GitHub `doreviateam/odoo19-addons-dorevia`).  
**Branche de référence :** `main` (HEAD stabilisé juin 2026 : `2feac7e`).

### 3.2 Dossier documentation (pas un module Odoo)

`dorevia_ck_marketone/docs/` — cadrage MOA, specs, recettes, scripts Playwright, captures. **Ne pas confondre avec du code installable.**

### 3.3 Modules à ignorer en recette CK

| Module | Statut |
| --- | --- |
| `dorevia_ckreyol_marketone` | Ancienne version — **désinstallé** sur l’instance seed. Inspiration uniquement. |
| `dorevia_ckreyol_marketplace` | Ancien canal — hors périmètre instance actuelle. |

Recetter uniquement ce qui est **servi** par `dorevia_ck_theme` + `dorevia_ck_marketone_content` sur la base cible.

### 3.4 Séparation thème / contenu

| Type de changement | Module cible |
| --- | --- |
| SCSS, layout, snippets génériques, header, shop structure | `dorevia_ck_theme` |
| Textes métier, navigation, seed, curation produits, pages CMS | `dorevia_ck_marketone_content` |
| Données produit (origines, tags, vedettes, catégories) | Back-office Odoo + parfois migrations `dorevia_ck_marketone_content` |

---

## 4. Environnement de recette

### 4.1 Sandbox de référence

| Paramètre | Valeur |
| --- | --- |
| URL | `http://localhost:18079` |
| Base PostgreSQL | `dorevia_ck_marketone_01` |
| Conteneur Docker | `sandbox-odoo19-odoo-1` |
| Login local | `admin` / `admin` |
| Thème website actif | `dorevia_ck_theme` (**obligatoire** — sinon assets CK non compilés) |

### 4.2 Pièges fréquents

1. **Sans contexte de base**, `/shop` peut répondre **404**. Toujours utiliser :
   - `?db=dorevia_ck_marketone_01` dans l’URL, ou
   - header HTTP `X-Odoo-Database: dorevia_ck_marketone_01` (scripts Playwright).
2. Après `-u dorevia_ck_theme` ou `dorevia_ck_marketone_content`, **redémarrer** le conteneur si le HTML semble figé.
3. Les tests Odoo `--test-enable` ne doivent **pas** réutiliser le port 8069 du worker live : utiliser un port alternatif (`8077`, `8078`, `8079`).

### 4.3 Mise à jour modules (exemple)

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d dorevia_ck_marketone_01 \
  -u dorevia_ck_theme,dorevia_ck_marketone_content --stop-after-init --no-http

docker restart sandbox-odoo19-odoo-1
```

---

## 5. État des livraisons — juin 2026

### 5.1 Lot S1 — Shop Structure V1 (**recevable · clôturé**)

**Objectif :** faire lire `/shop` comme un **rayon boutique C-Kréyòl**, pas comme un catalogue Odoo générique.

**Références :**
- Recette : `docs/design/maquette_01.2/RECETTE_SHOP_STRUCTURE_S1_20260624.md`
- Commit clôture recette : `97113e0`
- Merge `main` : `3508a19` · stabilisation doc : `2feac7e`
- Captures : `docs/design/maquette_01.2/captures/shop_structure_s1/`

**Attendu sur `/shop` :**
- H1 **Boutique C-Kréyòl**
- Promesse : *Produits créoles sélectionnés, aux origines identifiées.*
- Compteur dynamique dans l’intro (**pas** de doublon dans la toolbar)
- Sidebar : **Affiner ma sélection** · facettes tags → **Origines & préférences**
- Filmstrip catégories natif (pills), recherche et tri **fonctionnels mais discrets**
- Slider prix masqué si catalogue &lt; 15 produits (option B — lot S2 pour règle durable)

**Tests auto :** tag `dorevia_ck_shop_s1` — **6/6 au vert**.

**Réserves MOA notées hors S1 :**
- Mentions Nantes / livraison / producteurs encore visibles dans **header** ou **mega-menu** (lot séparé)
- Tuile famille sans image sur `/shop/category/epicerie-1` (contenu BO)
- Pills catalogue serrées en mobile 390 — acceptable S1

---

### 5.2 Header V2.2 (**GO technique · réserves seed**)

**Références :**
- `docs/design/maquette_01.2/captures/recette_header_v22/RECETTE_QA_HEADER_V22.md`
- `docs/design/maquette_01.2/LIVRABLE_MOA_HEADER_CK_V2_2.md`

**Attendu :** header 3 niveaux (bandeau réassurance · identité/recherche · navigation), mega-menus rayons, marque **C-Kréyòl**, Espace pro en dropdown.

**Tests auto :** tags `dorevia_ck_header_v22`, `dorevia_ck_theme_phase10`, `dorevia_ck_marketone_nav_sync` — **41 tests au vert** (référence header).

**Réserves :** seed navigation partiel (familles Épicerie, visuels mega-menu placeholders).

---

### 5.3 Home — champ « En vedette » (`ck_is_featured`)

**Référence :** `docs/design/NOTE_RECETTE_CK_CHAMP_EN_VEDETTE_HOME.md`

La section **Nos coups de cœur** sur `/` est pilotée par le booléen BO **En vedette** (`ck_is_featured`), plus par la catégorie « Coups de cœur » seule. Max 8 cards ; section masquée si aucune vedette.

**Tests :** tags `dorevia_ck_marketone_home_section3*`, `dorevia_ck_marketone_featured_propagation`, etc.

---

### 5.4 Autres zones déjà engagées (socle phases 1–10)

Home (hero, trust-bar, univers), fiche produit, page Pro, contact, producteurs, recettes, newsletter — recettes phase dans `docs/design/maquette_01.2/README.md`.

Le **test global Odoo** documenté (`RECETTE_TEST_GLOBAL_CK_20260624.md`) était **rouge** fin juin 2026 (~20 échecs sur contrats obsolètes). **Préférer les tests par tag** tant que le réalignement global n’est pas livré.

---

## 6. URLs et parcours de recette prioritaires

### Boutique

| URL | Contrôle type |
| --- | --- |
| `/shop` | Intro S1, filmstrip, grille, recherche, tri, sidebar |
| `/shop/category/epicerie-1` | Non-régression catégorie · header rayon éditorial si publiable |
| `/shop?search=manioc` | Recherche |
| `/shop?order=list_price+desc` | Tri |
| `/shop?attrib=2-5` | Filtre origine (Guadeloupe) |
| `/shop/cart` | Panier |

### Home et conversion

| URL | Contrôle type |
| --- | --- |
| `/` | Hero, trust-bar, vedettes `ck_is_featured`, univers, liens Pro |
| `/professionnels` | Page Pro + ancres |
| `/nos-producteurs` | Lien header N3 |
| `/contactus` | Formulaire, RGPD, a11y de base |

### Viewports de référence

- Desktop : **1280 px**
- Tablette : **800 px**
- Mobile : **390 px**

Contrôler systématiquement : **pas d’overflow horizontal**, CTA panier accessible, HTTP **200** sur les routes ci-dessus.

---

## 7. Documentation — où commencer

| Besoin | Document |
| --- | --- |
| Index général V1.2 | `docs/design/maquette_01.2/README.md` |
| Conventions nommage / cycle de vie docs | `docs/CONVENTIONS.md` |
| Instance et prérequis thème | `docs/design/REFERENCE_INSTANCE_RECETTE_DOREVIA_CK_THEME_01.md` |
| Shop S1 (lot le plus récent) | `RECETTE_SHOP_STRUCTURE_S1_20260624.md` |
| Header V2.2 | `captures/recette_header_v22/RECETTE_QA_HEADER_V22.md` |
| Vedettes home | `NOTE_RECETTE_CK_CHAMP_EN_VEDETTE_HOME.md` |
| Cartographie champs produit | `docs/design/CARTOGRAPHIE_CHAMPS_PRODUIT_CK_V1.md` |
| Retour Dev Home/Shop (contexte MOA) | `RAPPORT_RETOUR_DEV_HOME_SHOP_CK_20260624.md` |

**Règle :** les captures et JSON dans `captures/` sont des **annexes** ; le verdict vit dans le `RECETTE_*.md` qui les cite.

---

## 8. Tests automatisés — mode d’emploi QA

### 8.1 Principe

Les tests Odoo CK utilisent `@tagged('post_install', '-at_install', '<tag>')`. Ils nécessitent une base avec les modules installés et un **port HTTP dédié** pendant l’exécution.

### 8.2 Tags utiles au quotidien

| Tag | Périmètre |
| --- | --- |
| `dorevia_ck_shop_s1` | Shop structure S1 (6 tests) |
| `dorevia_ck_header_v22` | Header V2.2 |
| `dorevia_ck_theme_phase10` | Chrome header / menu |
| `dorevia_ck_marketone_nav_sync` | Navigation / mega-menus |
| `dorevia_ck_shop_card` | Cards produit shop |
| `dorevia_ck_marketone_home_section3*` | Section vedettes home |
| `dorevia_ck_product_origin` | Origine produit |

### 8.3 Exemples de commandes

**Shop S1 :**
```bash
docker exec sandbox-odoo19-odoo-1 odoo -d dorevia_ck_marketone_01 \
  --test-enable --stop-after-init --http-port=8078 \
  --test-tags="dorevia_ck_shop_s1"
```

**Header + nav :**
```bash
docker exec sandbox-odoo19-odoo-1 odoo -d dorevia_ck_marketone_01 \
  --test-enable --stop-after-init --http-port=8077 \
  --test-tags="dorevia_ck_header_v22,dorevia_ck_theme_phase10,dorevia_ck_marketone_nav_sync"
```

### 8.4 Scripts Playwright / CI locale

Dossier : `docs/design/maquette_01.2/scripts/`

| Script | Usage |
| --- | --- |
| `ck_shop_structure_s1_captures.mjs` | Captures shop S1 |
| `ck_h22_recette_qa.mjs` | Captures header V2.2 |
| `ck_phase3_ci.sh` … `ck_phase10_ci.sh` | Gates par phase (upgrade + smoke) |

Prérequis : Node.js, Playwright, Chrome channel.

### 8.5 CI GitHub

Pas de workflow Actions complet identifié dans le dépôt. **GitGuardian** sur les PRs (secrets). La qualité repose surtout sur **tests Odoo ciblés + recette manuelle documentée**.

---

## 9. Méthode de recette recommandée

### 9.1 À chaque lot livré

1. Lire la **note / recette Dev** du lot (`RECETTE_*`, `PLAN_*`).
2. Vérifier le **commit ou PR** sur `main`.
3. Mettre à jour la sandbox (`git pull` addons + `-u` modules concernés).
4. Exécuter les **tests auto du lot** (tags dédiés).
5. Suivre la **checklist manuelle** (URLs, viewports, parcours e-commerce).
6. Produire **captures** si le lot l’exige.
7. Rédiger le **verdict** : recevable / recevable avec réserves / non recevable — avec preuves.

### 9.2 Format de remontée d’anomalie

Pour chaque écart :

- **Route** (ex. `/shop`, mobile 390)
- **Attendu** (citation recette ou spec)
- **Constaté** (texte + capture si visuel)
- **Sévérité** : bloquant / majeur / mineur / hors périmètre
- **Lot concerné** ou « régression »

### 9.3 Ce qui n’est pas un bug S1

- Wording Nantes/livraison dans le header global
- Image manquante sur une sous-famille Épicerie en BO
- Écart entre nom catégorie nav (« Maison & Bien-être ») et filmstrip (« Soin & Bien-être ») — lot S3 données

Le QA doit **classer** l’écart : bug du lot en cours vs réserve déjà arbitrée vs nouveau sujet MOA.

---

## 10. Lots ouverts — horizon court / moyen

| Lot | Sujet | Priorité typique |
| --- | --- | --- |
| **S2** | Slider prix durable (total publié vs `search_count`) | Shop |
| **S3** | Alignement libellés catégories publiques BO | Shop / nav |
| **Header / réassurance** | Harmoniser première impression globale (hors intro shop) | Transversal |
| **H2** | Home storytelling V2 | Home |
| **R1** | Rating / avis réels Odoo | Confiance |
| **P1** | Modèle producteur officiel | Données |
| **P2B** | Rayons éditorialisés complets | Catégories |
| **Test global** | Réaligner ~20 tests obsolètes | Dette QA auto |

L’**Architecte** arbitre la priorisation ; le **Dev** estime la faisabilité Odoo ; le **QA** prépare les protocoles de recette des lots suivants.

---

## 11. Workflow Git

```
feat/ck-* | fix/ck-* | docs/ck-*  →  PR  →  review  →  merge main
```

Après merge : mise à jour sandbox, recette sur `main`, puis clôture documentaire (`RECETTE_*` + captures).

**Ne pas recetter** une branche feature abandonnée sans accord Dev/Architecte.

---

## 12. Contacts et escalade

| Sujet | Interlocuteur |
| --- | --- |
| Intention UX, GO MOA, priorisation lots | Architecte projet |
| Comportement Odoo, correctifs, tests auto, scripts | Dev expert Odoo |
| Verdict recette, consolidation preuves, non-régression | QA (vous) |

En cas de doute sur le périmètre d’un lot : **ne pas qualifier seul** — remonter avec la recette du lot et la réserve « hors périmètre » éventuelle.

---

## 13. Synthèse — état au 2026-06-24

```text
Code     : main @ 2feac7e — S1 mergé et sandbox à jour
Shop     : recevable — baseline stable
Header   : GO technique — réserves seed
Home     : vedettes par ck_is_featured — recette documentée
Dette QA : test global partiellement obsolète — privilégier tests par tag
Prochain : arbitrage MOA sur S2 / S3 / header-réassurance
```

Bienvenue dans l’équipe. Cette note sera mise à jour à chaque jalon majeur ; en cas d’écart avec `main`, **faire foi** l’état du dépôt et la recette la plus récente datée du lot concerné.
