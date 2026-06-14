# Recette QA — Dictionnaire Maquette ↔ Odoo CE V1

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Instance** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **Conteneur** | `sandbox-odoo19-odoo-1` |
| **Base vérifiée** | `dorevia_ck_marketone_01` |
| **Date contrôle** | 2026-06-13 |
| **Contre-vérification M9** | 2026-06-13 — §0bis |
| **Verdict M9 Newsletter** | **OK M9 CE avec réserve** — **validé MOA** |
| **Méthode** | Shell Odoo 19 CE + HTTP instance réelle (header `X-Odoo-Database`) |
| **Dictionnaire source** | [`GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md`](./GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md) |
| **Statut QA** | **Validée MOA · passe pré-Phase 1 OK · ne vaut pas GO exécution §5 seul** |
| **Passe QA pré-Phase 1** | **OK réserves classées** — Codex · 2026-06-13 — §0quater |

```text
RECETTE QA DICTIONNAIRE CE — VALIDÉE MOA
PASSE QA PRÉ-PHASE 1 — OK RÉSERVES CLASSÉES (CODEX · 2026-06-13)
GO EXÉCUTION §5 : ACTÉ (2026-06-13) — PHASE 1 EN COURS
M9 NEWSLETTER : OK CE AVEC RÉSERVE — V1 POSSIBLE · NON BLOQUANTE PHASE 1
```

> Cette recette **sécurise** le dictionnaire Maquette ↔ Odoo sur l’instance réelle. Elle **ne remplace pas** l’acte MOA §5 GO exécution.

---

## 0. Méthode et prérequis instance

### Modules vérifiés (shell · 2026-06-13)

| Module | État instance | Rôle V1 |
|--------|---------------|---------|
| `website` | ✅ installed | Website Builder · CMS · menus |
| `website_sale` | ✅ installed | `/shop` · fiche · panier · catégories |
| `website_crm` | ✅ installed | Formulaire Pro `/professionnels` |
| `dorevia_ck_theme` | ✅ installed | Snippets CK · layout · thème actif |
| `mass_mailing` | ✅ **installed** *(contre-vérification M9 · 2026-06-13)* | Email Marketing · mailing lists |
| `website_mass_mailing` | ✅ **installed** *(contre-vérification M9)* | Snippets newsletter · subscribe site |
| `link_tracker` | ✅ installed *(auto · dep mass_mailing)* | Dépendance CE |
| `website_blog` | ❌ uninstalled | Hors scope M2 |

> **État initial recette (2026-06-13 matin)** : `mass_mailing` et `website_mass_mailing` étaient **disponibles mais non installés** — pas absents du catalogue CE. Contre-vérification M9 §0bis.

### Snippets CK thème — registre instance

| Snippet | Clé QWeb | Statut instance |
|---------|----------|-----------------|
| CK Hero | `dorevia_ck_theme.s_ck_hero` | ✅ disponible |
| CK Réassurance | `dorevia_ck_theme.s_ck_reassurance` | ✅ disponible |
| CK Produits vedettes | `dorevia_ck_theme.s_ck_featured_products` | ✅ disponible · **placeholder** (`oe_structure` vide) |
| CK Liens univers | `dorevia_ck_theme.s_ck_category_links` | ✅ disponible |
| CK Intro boutique | `dorevia_ck_theme.s_ck_shop_intro` | ✅ disponible |
| CK Bandeau pro | `dorevia_ck_theme.s_ck_pro_banner` | ✅ disponible |
| CK Bloc dual Pro/newsletter | `s_ck_dual_engage` | ❌ **à créer** thème |

### Snippets natifs utiles — registre instance

| Snippet | Clé QWeb | Statut |
|---------|----------|--------|
| Titre | `website.s_title` | ✅ |
| Features | `website.s_features` | ✅ |
| Formulaire website/CRM | `website.s_website_form` | ✅ |
| CTA | `website.s_call_to_action` | ✅ |
| Image + texte | `website.s_image_text` | ✅ |
| Dynamic Products | `website_sale.s_dynamic_snippet_products` | ✅ |
| Dynamic catégories | `website_sale.s_dynamic_snippet_category_list` | ✅ |
| Newsletter subscribe | `website_mass_mailing.s_newsletter_subscribe_form` | ✅ *(après install M9)* |
| Newsletter block | `website_mass_mailing.s_newsletter_block` | ✅ |
| Newsletter box / grid / centered | `website_mass_mailing.s_newsletter_*` | ✅ |

### Données BO instance (état recette)

| Élément | Quantité | Note |
|---------|----------|------|
| Produits publiés | 6 | ✅ |
| Catégories e-commerce | 4 | Épicerie créole · Maison & bien-être · Artisanat · Packs & découvertes |
| Attributs produit | 0 | ⚠️ origine/famille à structurer BO |
| Tags produit | 0 | ⚠️ utiles fiche producteur M1 |
| Pages CMS | 5 | `/` · `/contactus` · `/professionnels` · thank-you |
| Pages manquantes V1 | — | `/a-propos` · `/recettes` · `/producteur/…` |

### Routes HTTP vérifiées (header `X-Odoo-Database: dorevia_ck_marketone_01`)

| Route | HTTP | Marqueurs confirmés |
|-------|------|---------------------|
| `/` | 200 | `ck-theme` · `s_ck_hero` |
| `/shop` | 200 | `ck-shop-page` · `o_wsale` |
| `/shop/category/epicerie-creole-1` | 200 | breadcrumb |
| `/shop/confiture-de-goyave-3` | 200 | `ck-product` · `ck-product-chips` · add_to_cart |
| `/shop/cart` | 200 | panier natif |
| `/professionnels` | 200 | `s_website_form` · `crm.lead` |
| `/contactus` | 200 | formulaire contact natif |
| `/website_mass_mailing/subscribe` | 200 JSON-RPC | inscription list_id=1 · toast success |

> **Note recette multi-base** : sans header `X-Odoo-Database` ou session DB explicite, les routes frontend renvoient 404 (« No database is selected »). Prévoir ce header ou login DB pour les contrôles QA automatisés.

---

## 0ter. Vérification header — mega-menu natif CE (2026-06-13)

**Demande MOA** : étudier header simple + mega-menu de découverte · vérifier CE / thème · intégrer au dictionnaire.

**Verdict mega-menu** :

```text
OK CE NATIF — website.menu.is_mega_menu + mega_menu_content
Configuration BO Website Builder · pas de dev obligatoire V1 minimale
Adaptation CSS CK légère possible · pas de snippet CK mega requis en V1
```

| Question | Résultat |
|----------|----------|
| Mega-menu natif CE ? | ✅ `website.menu` · champs `is_mega_menu` · `mega_menu_content` · `mega_menu_classes` |
| Enterprise requis ? | ❌ Non — module `website` CE |
| Configuration | Site → Edit Menu → badge **Mega Menu** · éditeur contenu HTML |
| Rendu desktop | ✅ `o_mega_menu` · `dropdown-menu` · pleine largeur |
| Rendu mobile | ✅ Accordéon offcanvas natif |
| `dorevia_ck_theme` | Pas de mega custom · SCSS `.o_mega_menu` **optionnel** |
| Test instance | Mega-menu QA temporaire · HTML confirmé · retiré |

**Décision MOA H1 actée (2026-06-13)** :

```text
Boutique · Découvrir (mega CE) · Producteurs (léger) · Professionnels (lien direct /professionnels)
Libellé Découvrir retenu — pas Univers · pas mega-menu Producteurs V1 · pas liens fictifs
```

| Question H1 | Verdict acté |
|-------------|--------------|
| Libellé Découvrir vs Univers | ✅ **Découvrir** |
| Mega-menu sur | **Découvrir uniquement** |
| Producteurs V1 | Lien simple ou dropdown léger · **pas mega lourd** · pas annuaire |
| Professionnels V1 | **Lien direct** `/professionnels` |

Détail colonnes mega-menu · garde-fous : [`note_reference_header_mega_menu_decouverte_ck_v1.md`](./note_reference_header_mega_menu_decouverte_ck_v1.md) · [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) §1bis

**Classification V1** : Phase 1 · **OK configuration BO** · liens origines/recettes **conditionnels** selon BO/phases.

---

## 0quater. Verdict QA passe pré-Phase 1 — Codex (2026-06-13)

| Champ | Valeur |
|-------|--------|
| **Responsable QA** | Codex |
| **Date** | 2026-06-13 |
| **Verdict** | **OK avec réserves classées** |
| **Bloquants nouveaux** | **Non** pour H1 / Phase 1 limitée |
| **Recommandation MOA** | **GO §5 Phase 1 autorisé avec réserves classées** *(acte §5 MOA toujours requis)* |

### 1. Cohérence documentaire H1 — OK

Documents alignés : `decision_moa_go_reprise_odoo_v1.md` §1bis · note H1 · guide traduction §1 · séquence Phase 1 · recette §0ter · `COMPOSITION_HEADER_V1_2.md`.

Points validés : header **Boutique · Découvrir · Producteurs · Professionnels** · mega uniquement sur Découvrir · Producteurs sans mega V1 · Pro lien direct · §5 non acté · M9 non bloquant Phase 1.

### 2. Contre-vérification technique CE — OK

Modules confirmés : `website` · `website_sale` · `website_crm` · `dorevia_ck_theme` · `mass_mailing` · `website_mass_mailing`.

Test mega-menu natif ponctuel :

* entrée QA temporaire créée puis supprimée ;
* `website.menu.is_mega_menu = True` confirmé ;
* rendu HTML : `o_mega_menu` · `dropdown-menu` · `o_mega_menu_is_offcanvas` ;
* baseline restaurée : **Boutique · Catégories · Professionnels**.

Routes vérifiées (conteneur · `X-Odoo-Database: dorevia_ck_marketone_01`) :

```text
200 /
200 /shop
200 /shop/category/epicerie-creole-1
200 /professionnels
200 /contactus
```

### 3. Matrice liens mega-menu Phase 1

**Activables dès Phase 1** :

| Lien | Cible |
|------|-------|
| Boutique | `/shop` |
| Épicerie créole | `/shop/category/epicerie-creole-1` |
| Packs & découvertes | catégorie BO existante — URL exacte à confirmer |
| Professionnels | `/professionnels` |

**À différer / masquer** :

| Élément | Motif |
|---------|-------|
| Colonne origines (Guadeloupe · Martinique · Réunion) | 0 attribut BO → **masquer** |
| Recettes & savoirs | `/recettes` absent |
| Conseils d’usage · À propos | `/a-propos` absent |
| Manioc & dérivés · Incontournables CK · Nouveautés | catégorie/tag BO à confirmer |
| Producteurs mega | H1 → lien simple si cible CMS réelle |

Détail opérationnel : [`note_reference_header_mega_menu_decouverte_ck_v1.md`](./note_reference_header_mega_menu_decouverte_ck_v1.md) §2bis.

### 4. Réserves à surveiller

| # | Point | Impact Phase 1 |
|---|-------|----------------|
| R1 | Accès HTTP hôte intermittent pendant passe | Contrôle interne conteneur OK |
| R2 | Cron erreur base `glc-audit-paliers-0-3` (`glc_default_bank_journal_id`) | Hors base CK · bruit serveur |
| R3 | Liens mega vers pages/catégories absentes | **Interdit** — gate M4 / matrice §3 |

### 5. Conditions exécution Phase 1 (rappel QA)

```text
§5 explicitement passé à Acté par MOA
Phase 1 limitée header + footer BO
Mega-menu natif CE uniquement · aucun lien fictif
Colonne origines masquée tant que 0 attribut BO
/recettes et /a-propos exclus du mega tant qu’absentes
Recette mobile 390 px obligatoire après livraison Phase 1
```

**Conclusion QA** : OK avec réserves · aucun bloquant technique nouveau pour ouvrir Phase 1 limitée.

---

**Demande MOA** : confirmer factuellement la disponibilité CE de `mass_mailing` / `website_mass_mailing` sur `dorevia_ck_marketone_01`, sans supposer ni différer sur une hypothèse non vérifiée.

**Verdict M9** :

```text
OK M9 CE AVEC RÉSERVE
Newsletter simple possible en Odoo 19 CE — option V1, pas prérequis bloquant
Colonne Pro du bloc dual reste prioritaire
```

### 1. `mass_mailing` — disponibilité CE

| Question | Résultat instance / CE |
|----------|------------------------|
| Présent dans la liste des modules ? | ✅ Oui — **Email Marketing** (`mass_mailing`) |
| État initial instance | `uninstalled` — **disponible, non activé** |
| Installable CE sans Enterprise ? | ✅ Oui — toutes dépendances `to_buy=False` |
| Dépendances installées auto | `link_tracker` · `website_links` *(via chaîne)* |
| Licence | LGPL-3 · addon standard `/usr/lib/python3/dist-packages/odoo/addons/mass_mailing` |
| Test install instance | ✅ **Réussi** — module `installed` |

### 2. `website_mass_mailing` — disponibilité CE

| Question | Résultat |
|----------|----------|
| Présent / installable ? | ✅ Oui — dépend `website` + `mass_mailing` + `google_recaptcha` |
| État après test install | ✅ `installed` |
| Auto-install | Oui si `website` + `mass_mailing` actifs |
| Enterprise ? | ❌ Non — `to_buy=False` |

### 3. Snippets Website Builder — inscription mailing list

Snippets confirmés après installation (groupe **Contact and Forms**) :

| Snippet | Clé QWeb |
|---------|----------|
| Newsletter (formulaire) | `website_mass_mailing.s_newsletter_subscribe_form` |
| Newsletter Block | `website_mass_mailing.s_newsletter_block` |
| Newsletter Box | `website_mass_mailing.s_newsletter_box` |
| Newsletter Centered | `website_mass_mailing.s_newsletter_centered` |
| Newsletter Grid | `website_mass_mailing.s_newsletter_grid` |
| Newsletter Popup | `website_mass_mailing.s_newsletter_subscribe_popup` |

Endpoint public confirmé : **`/website_mass_mailing/subscribe`** (JSON-RPC · `auth='public'`).

### 4. Mailing list + inscription depuis le site

| Test | Résultat |
|------|----------|
| Modèle `mailing.list` | ✅ disponible après install |
| Liste par défaut instance | « Newsletter » (id=1) |
| Création liste test QA | ✅ « Newsletter CK QA test » (id=2) |
| Inscription HTTP test | ✅ `list_id=1` · email test · **toast « Merci de vous être abonné ! »** |
| reCAPTCHA clés instance | ⚠️ non configurées — inscription **fonctionne sans token** en recette |

### 5. Compatibilité besoin V1 MOA

| Critère M9 | Compatible ? | Commentaire |
|------------|--------------|-------------|
| Inscription newsletter **simple** | ✅ | Snippet natif + mailing list BO |
| Sans automation marketing avancée | ✅ | Subscribe seul · pas de tunnel obligatoire |
| Sans promesse promotionnelle | ✅ | Copy éditoriale CMS · gate MOA |
| Colonne Pro **prioritaire** | ✅ | Newsletter = option · pas prérequis Phase 1 |
| Bloc dual maquette | ⚠️ | `s_ck_dual_engage` **à créer** ou composer Pro + `s_newsletter_subscribe_form` |
| RGPD / consentement | ⚠️ **Réserve MOA** | Texte légal · opt-in · politique données |
| Configuration snippet | ⚠️ **Réserve Dev** | Lier `data-list-id` à liste BO · recette soumission |

### 7. Garde-fous M9 maintenus (validés MOA)

```text
Colonne Pro V1 prioritaire
Newsletter V1 possible avec réserve — option · pas prérequis bloquant
Newsletter non obligatoire si intégration devient trop lourde
Newsletter ne doit pas retarder Phase 1 header + footer · navigation · recette palier 1
Pas d’automation marketing avancée · pas de tunnel complexe · pas de promo excessive
Test install QA mass_mailing ≠ GO exécution §5
```

**Réserves à cadrer avant intégration effective newsletter** : copy RGPD · mailing list cible · `data-list-id` · snippet natif vs `s_ck_dual_engage` · reCAPTCHA · ton CK.

### 8. Correction vs recette initiale

| Affirmation initiale | Correction factuelle |
|---------------------|----------------------|
| « mass_mailing non disponible » | ❌ Inexact — **disponible CE, non installé** |
| « M9 différer confirmé (non installé) » | ❌ Remplacé — **OK M9 CE avec réserve** |
| Implication CE indisponible | ❌ — module standard Odoo 19 CE |

---

## 1. Légende — Résultat QA

| Résultat QA | Signification |
|-------------|---------------|
| **OK CE standard** | Fonctionnalité native Odoo CE confirmée instance |
| **OK snippet natif** | Snippet Website Builder natif disponible |
| **OK website_sale** | Module e-commerce natif confirmé |
| **OK page CMS** | Composition CMS / page website confirmée ou faisable |
| **OK website_crm** | Formulaire CRM natif confirmé |
| **OK configuration BO** | Réalisable via menus / website / produits BO |
| **OK snippet CK existant** | Snippet `dorevia_ck_theme` installé |
| **OK avec snippet CK à créer** | Faisable mais snippet thème absent |
| **Partiel / simplification** | Disponible avec adaptation ou contenu BO manquant |
| **Différer** | Réserve MOA actée · non prioritaire V1 |
| **Hors scope V1** | Non retenu |

---

## 2. Transversal — toutes pages · header

| Page | Bloc maquette | Traduction Odoo pressentie | Vérification Odoo CE | Résultat QA | Action recommandée |
|------|---------------|----------------------------|----------------------|-------------|-------------------|
| Toutes | Header barre | Configuration BO + thème | Menus · recherche/panier HTTP 200 | **Partiel / simplification** | Phase 1 · consolider doublons racine |
| Toutes | Entrée Boutique | Lien `/shop` | Route 200 ✅ | **OK CE standard** | Phase 1 |
| Toutes | Entrée **Découvrir** | Mega-menu natif CE | `is_mega_menu` ✅ · test rendu `o_mega_menu` | **OK CE natif · H1 acté** | Phase 1 · remplacer « Catégories » |
| Toutes | Mega-menu colonnes | 3 colonnes BO H1 | `mega_menu_content` HTML éditable | **OK configuration BO** | Univers M4 · origines si BO · recettes Phase 6–8 |
| Toutes | Entrée Producteurs | **Lien simple ou dropdown léger** | Enfants menu natifs ✅ | **OK CE standard · H1** | **Pas mega V1** · Phase 7 contenu fiche pilote |
| Toutes | Entrée Professionnels | **Lien direct** `/professionnels` | HTTP 200 ✅ | **OK page CMS · H1** | Pas sous-menu |
| Toutes | Header mobile mega | Accordéon offcanvas | Template natif accordion | **OK CE natif** | Recette 390 px |
| Toutes | Style mega CK | CSS thème | `mega_menu_classes` · SCSS | **OK avec réserve** | CSS léger thème si besoin |

### 2bis. Transversal — footer & autres

| Page | Bloc maquette | Traduction Odoo pressentie | Vérification Odoo CE | Résultat QA | Action recommandée |
|------|---------------|----------------------------|----------------------|-------------|-------------------|
| Toutes | Responsive 390 px | Tokens CSS thème | `body.ck-theme` confirmé · recette mobile antérieure OK | **OK snippet CK existant** | Recette mobile à chaque phase |
| Toutes | Signal Pro discret | `/professionnels` menu | Page 200 · menu sequence 30 · lien présent | **OK page CMS** | Phase 1 · consolidation lien |

---

## 3. Accueil — `index.html`

| Page | Bloc maquette | Traduction Odoo pressentie | Vérification Odoo CE | Résultat QA | Action recommandée |
|------|---------------|----------------------------|----------------------|-------------|-------------------|
| Accueil | Hero | `s_ck_hero` | Snippet installé · présent sur `/` (HTTP) | **OK snippet CK existant** | Phase 2 · réaligner copy/visuels |
| Accueil | Réassurance | `s_ck_reassurance` | Snippet installé · non composé home actuelle | **OK snippet CK existant** | Phase 2 · composer + gate M5 copy |
| Accueil | Produits vedettes ×6 | Dynamic Products | `s_ck_featured_products` = placeholder · `website_sale.s_dynamic_snippet_products` ✅ | **Partiel / simplification** | Phase 2 · Dynamic Products dans zone vedettes |
| Accueil | Catégories ×3 | `s_ck_category_links` | Snippet ✅ · 4 catégories BO ✅ | **OK snippet CK existant** | Phase 2 · **conditionnel M4** |
| Accueil | Coffret découverte | Dynamic Products / CMS | Catégorie « Packs & découvertes » existe · pas produit pack dédié | **Partiel / simplification** | Conditionnel · si produit pack BO |
| Accueil | Bandeau Pro | `s_ck_pro_banner` | Snippet ✅ · `/professionnels` ✅ | **OK snippet CK existant** | Phase 2 |
| Accueil | Bloc dual Pro / newsletter | `s_ck_dual_engage` ou Pro + `s_newsletter_subscribe_form` | Pro ✅ · mailing ✅ installé · dual CK absent | **OK M9 CE avec réserve** | Phase 2 Pro prioritaire · newsletter si simple · dual à composer |
| Accueil | Éditorial bas de page | Blocs CMS | `oe_structure` natif ✅ · pages cibles absentes | **Partiel / simplification** | Phase 2 partiel · liens après Phases 6–8 |
| Accueil | SEO / ordre blocs | Composition CMS | Website Builder ✅ | **OK CE standard** | Phase 2 |

---

## 4. Shop — `shop.html`

| Page | Bloc maquette | Traduction Odoo pressentie | Vérification Odoo CE | Résultat QA | Action recommandée |
|------|---------------|----------------------------|----------------------|-------------|-------------------|
| Shop | En-tête catalogue | `/shop` natif · `s_ck_shop_intro` | `/shop` 200 · snippet intro ✅ | **OK website_sale** | Phase 3 |
| Shop | Grille produits dense | Grille native | 6 produits · grille `o_wsale` ✅ | **OK website_sale** | Phase 3 |
| Shop | Collections pills | Liens catégories | 4 catégories · URLs `/shop/category/…` 200 | **OK website_sale** | Phase 3 |
| Shop | Filtres origine / famille | Attributs natifs | 0 attribut BO · pas facettes custom | **Différer** | **M3** confirmé · pas AJAX |
| Shop | Tri select | Tri Odoo natif | `shop_default_sort` = `website_sequence asc` · tri présent HTML | **OK website_sale** | Phase 3 · options limitées vs maquette |
| Shop | Réassurance compacte | `s_ck_reassurance` | Snippet ✅ · non composé shop | **OK snippet CK existant** | Phase 3 |
| Shop | Signal Pro mini | Lien `/professionnels` | Route 200 ✅ | **OK page CMS** | Phase 3 |

---

## 5. Catégorie — `categorie.html`

| Page | Bloc maquette | Traduction Odoo pressentie | Vérification Odoo CE | Résultat QA | Action recommandée |
|------|---------------|----------------------------|----------------------|-------------|-------------------|
| Catégorie | Breadcrumb | Natif catégorie | Confirmé HTTP catégorie | **OK website_sale** | Phase 3 |
| Catégorie | Hero éditorial | Description catégorie BO | Champ description catégorie disponible · contenu à saisir | **OK configuration BO** | Phase 3 |
| Catégorie | Guide « Comment choisir ? » | Header catégorie CMS | `oe_structure` / éditeur catégorie ✅ | **OK page CMS** | Phase 3 · contenu BO |
| Catégorie | Grille produits filtrée | `product.public.category` | Catégorie Épicerie créole 200 · produits listés | **OK website_sale** | Phase 3 |
| Catégorie | Réassurance | `s_ck_reassurance` | Snippet ✅ | **OK snippet CK existant** | Phase 3 |
| Catégorie | Signal Pro | Lien Pro | `/professionnels` 200 ✅ | **OK page CMS** | Phase 3 |

---

## 6. Fiche produit — `fiche-produit.html`

| Page | Bloc maquette | Traduction Odoo pressentie | Vérification Odoo CE | Résultat QA | Action recommandée |
|------|---------------|----------------------------|----------------------|-------------|-------------------|
| Fiche produit | Galerie + achat | Fiche native | `/shop/confiture-de-goyave-3` 200 · add_to_cart ✅ | **OK website_sale** | Phase 4 |
| Fiche produit | Chips origine / famille | Attributs / tags | `ck-product-chips` CSS ✅ · **0 attribut BO** | **Partiel / simplification** | Phase 4 · créer attributs/tags BO |
| Fiche produit | Origine & usage | Description produit | Champs `description_ecommerce` · `website_description` ✅ · contenu vide sur échantillon | **OK configuration BO** | Phase 4 · standardiser contenu |
| Fiche produit | Bloc producteur (mini) | Lien CMS | Pas de page producteur · lien CMS faisable sans dev | **Partiel / simplification** | Phase 4 lien · Phase 7 page |
| Fiche produit | Conservation | Champ produit | Description / onglets ✅ | **OK configuration BO** | Phase 4 |
| Fiche produit | Signal B2B | `s_ck_pro_banner` | Snippet ✅ | **OK snippet CK existant** | Phase 4 |
| Fiche produit | Associations produits | Optional products | Champs `optional_product_ids` · `alternative_product_ids` ✅ · non configurés | **Différer** | V1 différée confirmée |
| Fiche produit | Idée recette inline | Lien recettes | Page `/recettes` absente | **Différer · M2** | Phase 8 |
| Fiche produit | Cross-sell | Dynamic Products zone | `oe_structure` fiche ✅ · non prioritaire | **Différer** | V1 différée confirmée |

---

## 7. Professionnels — `professionnels.html`

| Page | Bloc maquette | Traduction Odoo pressentie | Vérification Odoo CE | Résultat QA | Action recommandée |
|------|---------------|----------------------------|----------------------|-------------|-------------------|
| Professionnels | Hero double entrée | Page CMS · `s_title` | Page publiée · contenu présent | **OK page CMS** | Phase 5 · consolidation |
| Professionnels | Double cible ×2 | `s_features` | `s_features` + double cible confirmés arch | **OK snippet natif** | Phase 5 |
| Professionnels | Process 3 étapes | Blocs CMS | Snippets texte natifs ✅ | **OK page CMS** | Phase 5 |
| Professionnels | Réassurance pro | `s_ck_reassurance` | Snippet ✅ | **OK snippet CK existant** | Phase 5 |
| Professionnels | Formulaire CRM | `website_crm` · `s_website_form` | `crm.lead` + `s_website_form` confirmés HTTP | **OK website_crm** | Phase 5 · recette soumission lead |
| Professionnels | Note qualification | Texte CMS | Présent page composée | **OK page CMS** | Phase 5 |
| Professionnels | Bloc dual compact | Variante M9 | Pro ✅ · snippets newsletter ✅ · dual CK absent | **OK M9 CE avec réserve** | Phase 5 Pro · newsletter optionnelle |

---

## 8. À propos — `a-propos.html`

| Page | Bloc maquette | Traduction Odoo pressentie | Vérification Odoo CE | Résultat QA | Action recommandée |
|------|---------------|----------------------------|----------------------|-------------|-------------------|
| À propos | Hero mission | Page CMS `/a-propos` | Page **absente** · snippets natifs ✅ | **OK page CMS** | Phase 6 · créer page |
| À propos | Grille 4 cartes | `s_features` | Snippet ✅ | **OK snippet natif** | Phase 6 |
| À propos | Engagements ×3 | `s_features` / réassurance | Snippets ✅ | **OK snippet natif** | Phase 6 |
| À propos | Signal Pro | CTA Pro | `/professionnels` ✅ | **OK page CMS** | Phase 6 |
| À propos | CTA transverses | Liens internes | Liens faisables · cibles partiellement absentes | **Partiel / simplification** | Phase 6 |

---

## 9. Fiche producteur — `fiche-producteur.html` (M1)

| Page | Bloc maquette | Traduction Odoo pressentie | Vérification Odoo CE | Résultat QA | Action recommandée |
|------|---------------|----------------------------|----------------------|-------------|-------------------|
| Fiche producteur | Hero producteur | Page CMS pilote | Pas de page · CMS + snippets ✅ | **OK page CMS** | Phase 7 · **M1** |
| Fiche producteur | Présentation éditoriale | Blocs CMS | `s_image_text` ✅ | **OK snippet natif** | Phase 7 |
| Fiche producteur | Critères sélection CK | Texte CMS statique | Faisable sans dev | **OK page CMS** | Phase 7 |
| Fiche producteur | Produits proposés | Dynamic Products filtré | Dynamic Products ✅ · **0 tags** BO | **Partiel / simplification** | Phase 7 · convention tags |
| Fiche producteur | Sélection CK focus ×2 | Dynamic Products / CMS | Idem | **Partiel / simplification** | Phase 7 · simplifier si besoin |
| Fiche producteur | Usage / conseil | Lien recettes | Page recettes absente | **Différer** | Hors fiche minimale V1 |
| Fiche producteur | Signal logistique CK | `s_ck_reassurance` | Snippet ✅ | **OK snippet CK existant** | Phase 7 |
| Fiche producteur | CTA sortie | Liens CMS | Routes shop/pro/contact ✅ | **OK page CMS** | Phase 7 |

---

## 10. Recettes — `recettes.html` (M2)

| Page | Bloc maquette | Traduction Odoo pressentie | Vérification Odoo CE | Résultat QA | Action recommandée |
|------|---------------|----------------------------|----------------------|-------------|-------------------|
| Recettes | Hero éditorial | Page CMS `/recettes` | Page absente · CMS ✅ · blog non installé | **OK page CMS** | Phase 8 · **M2** |
| Recettes | Grille 6 cartes | Cartes manuelles CMS | Snippets image-texte ✅ | **OK page CMS** | Phase 8 |
| Recettes | Liens catalogue | Liens internes | Shop/catégories ✅ | **OK CE standard** | Phase 8 |
| Recettes | Blog / forum | — | `website_blog` non installé | **Hors scope V1** | **M2** confirmé |

---

## 11. Contact — `contact.html`

| Page | Bloc maquette | Traduction Odoo pressentie | Vérification Odoo CE | Résultat QA | Action recommandée |
|------|---------------|----------------------------|----------------------|-------------|-------------------|
| Contact | 4 parcours | Blocs CMS + liens | `/contactus` 200 · édition CMS ✅ | **OK page CMS** | Phase 6 · enrichir contenu |
| Contact | Formulaire contact B2C | `/contactus` natif | Route + formulaire website ✅ | **OK CE standard** | Phase 6 |
| Contact | Réassurance contact | Texte CMS | Faisable CMS | **OK page CMS** | Phase 6 · gate M5 |
| Contact | Bloc dual Pro / newsletter | Variante compacte | Pro ✅ · `s_newsletter_subscribe_form` ✅ | **OK M9 CE avec réserve** | Phase 6 Pro · newsletter optionnelle |
| Contact | Distinction Pro / B2C | Pro séparé | `/professionnels` CRM distinct ✅ | **OK website_crm** | Phase 6 |

---

## 12. Synthèse QA — classification

### 1. Blocs confirmés CE standard

Contact `/contactus` · panier `/shop/cart` · composition CMS · tri shop natif · champs description produit · `oe_structure` · routes internes.

### 2. Blocs confirmés — mega-menu header (CE natif)

`website.menu.is_mega_menu` · `mega_menu_content` · rendu `o_mega_menu` · mobile accordéon · header 4 entrées MOA.

### 3. Blocs confirmés via snippets natifs

`s_title` · `s_features` · `s_website_form` · `s_call_to_action` · `s_image_text` · `website_sale.s_dynamic_snippet_products` · `website_sale.s_dynamic_snippet_category_list`.

### 4. Blocs confirmés via `website_sale`

`/shop` · catégories `/shop/category/…` · fiche produit · prix · panier · breadcrumb · grille produits · classes thème `ck-shop-page` · `ck-product` · `ck-product-chips`.

### 4. Blocs confirmés via page CMS / configuration BO

Header/footer menus · **mega-menu Découvrir natif** · `/professionnels` · pages À propos / recettes / producteur **à créer** · contenu catégories · copy réassurance.

### 5. Blocs confirmés via `website_crm`

Formulaire Pro `/professionnels` · modèle `crm.lead` · pas de champs CRM custom (conforme V1).

### 6. Blocs nécessitant snippet CK — existants

`s_ck_hero` · `s_ck_reassurance` · `s_ck_category_links` · `s_ck_shop_intro` · `s_ck_pro_banner` · `s_ck_featured_products` (structure).

### 7bis. Blocs confirmés via Email Marketing CE (M9)

`mass_mailing` · `mailing.list` · `website_mass_mailing.s_newsletter_subscribe_form` · endpoint `/website_mass_mailing/subscribe`.

### 7. Blocs nécessitant snippet CK — à créer

| Snippet | Bloc | Impact |
|---------|------|--------|
| `s_ck_dual_engage` | Bloc dual Pro/newsletter | **Non bloquant** · alternative : Pro + snippet natif newsletter |

### 8. Blocs à simplifier (partiel)

| Bloc | Écart | Mesure |
|------|-------|--------|
| Header | Doublons menus racine · nav pas encore footer 4 col | Phase 1 consolidation |
| Produits vedettes | Placeholder sans Dynamic Products composé | Phase 2 composition |
| Chips origine / famille | 0 attribut · 0 tag BO | Phase 4 modèle BO |
| Fiche producteur grille | 0 tags produit | Phase 7 convention BO |
| Bloc dual | Snippet dual CK absent · newsletter CE OK | Composer Pro + `s_newsletter_subscribe_form` · gate RGPD MOA |

### 9. Blocs à différer — confirmés instance

Filtres shop avancés (**M3**) · associations / cross-sell fiche · recette inline fiche · usage fiche producteur.

> **Newsletter M9** : **retirée de la liste différer** — cf. §0bis **OK M9 CE avec réserve**.

### 10. Hors scope V1 — confirmés

Blog · forum · annuaire producteurs · portail · reprise intégrale HTML.

---

## 13. Points bloquants avant GO Phase 1

| # | Point | Bloquant ? | Verdict |
|---|-------|------------|---------|
| B1 | Modules socle (`website` · `website_sale` · `website_crm` · thème) | — | ✅ **Non bloquant** — installés |
| B2 | Routes shop / pro / contact fonctionnelles | — | ✅ **Non bloquant** — HTTP 200 confirmé |
| B3 | Snippets CK Phase 1 (header/footer = BO) | — | ✅ **Non bloquant** — configuration BO |
| B4 | Footer 4 col non configuré | — | ⚠️ **Travail Phase 1** — pas blocage dictionnaire |
| B5 | Menus header à consolider | — | ⚠️ **Travail Phase 1** — pas blocage dictionnaire |
| B6 | Newsletter M9 · `mass_mailing` | M9 | ✅ **Non bloquant Phase 1** — **OK M9 CE avec réserve** · option V1 |
| B7 | `s_ck_dual_engage` absent | M9 | ✅ **Non bloquant** — alternative snippet natif newsletter |
| B8 | Attributs/tags produit absents | Phase 4 | ✅ **Non bloquant Phase 1** |
| B9 | Header `X-Odoo-Database` requis recette multi-base | QA | ⚠️ **Note procédure** — documenter en recette |

```text
VERDICT QA DICTIONNAIRE CE : OK AVEC RÉSERVES CLASSÉES
AUCUN BLOQUANT TECHNIQUE IDENTIFIÉ POUR PHASE 1 (HEADER + FOOTER BO)
M9 NEWSLETTER : OK M9 CE AVEC RÉSERVE (mass_mailing disponible et installable · simple subscribe confirmé)
```

---

## 14. Suite MOA / Dev

| # | Action | Responsable |
|---|--------|-------------|
| 1 | **Validation MOA** de cette recette QA dictionnaire CE | MOA | ✅ **Validée** |
| 1bis | **Passe QA pré-Phase 1** (H1 · mega-menu · matrice liens) | QA Codex | ✅ **OK réserves classées** · §0quater |
| 2 | **Acter §5 GO exécution** — Phase 1 uniquement | MOA | ✅ **Acté 2026-06-13** |
| 3 | Exécuter Phase 1 header + footer BO | Dev | ✅ **Livré 2026-06-13** |
| 4 | Recette MOA/QA Phase 1 | MOA / QA | ✅ **OK QA** · §6.0 |
| 5 | Acter GO MOA Phase 2 | MOA | En attente |
| 5 | Cadrer réserves M9 avant intégration newsletter effective | MOA / Dev | Option · Phases 2+ |

---

## 15. Documents liés

| Document | Rôle |
|----------|------|
| [`GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md`](./GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md) | Dictionnaire opérationnel |
| [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) | Gouvernance · §5 |
| [`SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md`](./SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md) | Phases d’exécution |
| [`note_reference_header_mega_menu_decouverte_ck_v1.md`](./note_reference_header_mega_menu_decouverte_ck_v1.md) | Header · mega-menu · proposition MOA |

---

*Recette QA dictionnaire Maquette ↔ Odoo CE V1 — Phase 1 OK QA · GO Phase 2 recommandé · 2026-06-13.*
