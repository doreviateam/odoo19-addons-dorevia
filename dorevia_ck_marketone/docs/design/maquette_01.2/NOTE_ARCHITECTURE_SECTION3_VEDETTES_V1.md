# Note d'architecture MOA / QA — Section 3 · Produits vedettes / Nos coups de cœur

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Section** | Home V1 — Section 3 |
| **Instance recette** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **Statut doc** | **Révision 2026-06-16** — alignée sur `dorevia_ck_marketone_content` **≥ `19.0.1.20.6`** |
| **Code** | `home_featured.py` · `product_template.py` · `ck_card_uom.py` · `product_public_category.py` · `ir_http.py` · `catalog_manioc_variants.py` · `website.scss` |

---

## Guide simple (lire en premier)

### C'est quoi, concrètement ?

Sur la page d'accueil, le bloc **« Nos coups de cœur »** affiche des **cartes produit** (photo, badge optionnel, origine, prix, bouton « Voir »). Ce n'est **pas** le carrousel Odoo standard de la boutique.

### Qui décide quels produits apparaissent ?

**Le gestionnaire en back-office**, via la catégorie e-commerce **« Coups de cœur »** (xmlid `public_categ_coups_de_coeur`).

| Action BO | Effet home |
|-----------|------------|
| Ajouter un produit à « Coups de cœur » | Peut apparaître sur la home |
| Retirer un produit de « Coups de cœur » | Disparaît de la home (après refresh, cf. ci-dessous) |
| Modifier `website_sequence` | Change l'ordre des cartes |
| Assigner un **ruban** (`website_ribbon_id`) | Affiche le badge en haut à droite de la carte |

**Ordre** : champ **« Séquence du site web »** (`website_sequence`) — le plus petit numéro en premier.

**Nombre de cartes** : variable selon la curation (ex. 3 cartes si Confiture + Manio seuls dans la catégorie → 3 cartes dont 2 pour les variantes Manio). Plafond **8** en mode curaté.

### Cas particulier : Manio Crackers

Un seul produit parent **Manio Crackers** dans « Coups de cœur » → **deux cartes** sur la home (salé / sucré), une par variante **Format**.

### Cas particulier : Galettes de manioc

Produit **séparé** de Manio Crackers — jamais une variante du parent Manio.

### Badges sur les cartes

Le badge (haut à droite) vient du **ruban e-commerce** du produit (`website_ribbon_id`, onglet eCommerce).

- Pas de ruban → pas de badge
- Ruban « Coup de cœur » → style orange CK
- Ruban « Nouveau ! » → style jaune CK
- Autre ruban → couleurs définies sur le ruban en BO

Ruban CK livré en données : `ribbon_coups_de_coeur` (Confiture de goyave amorcée en migration).

### Quantité nette et prix de référence (card V1.1)

Sous le titre, la card peut afficher une ligne commerciale (ex. `320 g · 18,13 €/kg`) :

| Champ BO (onglet eCommerce) | Rôle |
|-----------------------------|------|
| **Quantité nette** | Valeur affichée (ex. `320`) |
| **Unité de quantité nette** | Liste `dorevia.ck.card.uom` (ex. `g`) |
| **Afficher le prix au kg / litre** | Active le calcul prix de référence |
| **Unité du prix de référence** | Dénominateur (ex. `kg`) |

**Décision MOA** : ces unités ne sont **pas** les unités Inventaire (`uom.uom`) — voir §6. La liste se gère dans **Site web → Configuration → Unités card home**.

### Plan B si la catégorie est vide

Si **aucun** produit n'est dans « Coups de cœur », le code retombe sur la sélection automatique PR #73 : les **5 premiers** produits publiés avec image. Héritage technique — la MOA peut souhaiter le supprimer (cf. §8).

### Pourquoi la home n'est pas « live » comme `/shop` ?

Le HTML de la section est **pré-généré** (injecté dans l'arch de la page `/`). Il est **reconstruit** quand :

| Déclencheur | Mécanisme |
|-------------|-----------|
| Upgrade / migration module | `post-migrate.py` · `post_init_hook` |
| Modification **fiche produit** | `product_template.write()` — catégorie, publication, ordre, prix, image, ruban |
| Modification **fiche catégorie** « Coups de cœur » (liste produits) | `product_public_category.write()` |

Un simple F5 navigateur **sans** changement BO ne régénère pas la section. Après modification BO, la home doit se mettre à jour **automatiquement** ; si ce n'est pas le cas, ré-enregistrer la fiche produit ou catégorie.

### Set MOA historique (exemple initial, pas règle de cardinalité)

| Carte home | En BO |
|------------|-------|
| Confiture de goyave | Template simple · ruban « Coup de cœur » |
| Manio Crackers salé | Variante **Format** de **Manio Crackers** |
| Manio Crackers sucré | Variante **Format** de **Manio Crackers** |
| Galettes de manioc | Template séparé (optionnel en curation) |
| Savon vétiver | Template simple (optionnel en curation) |

> **Règle actuelle opposable** : seuls Confiture + Manio dans « Coups de cœur » → **3 cartes** à l'affichage. La home ne complète pas artificiellement avec Galettes ou Savon.

### En une phrase

**BO Odoo pilote la sélection (catégorie « Coups de cœur ») et les badges (ruban produit) ; un script CK fabrique les cartes maquette et les injecte dans la home.**

---

## 1. Vue d'ensemble (comment la section est construite)

```text
┌─────────────────────────────────────────────────────────────────┐
│  Back-office Odoo                                               │
│  public_categ_ids · website_sequence · website_ribbon_id        │
│  prix · images · variantes · publication                        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  Sélection — home_featured.py                                   │
│  1) Curation : catégorie xmlid « Coups de cœur » (prioritaire)  │
│  2) Repli    : 5 premiers publiés avec image (#73)              │
│  → expansion variantes → N cartes                               │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  Rendu cartes — build_featured_product_card_html()              │
│  image · badge ruban · chips · prix · CTA « Voir »              │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  Injection — bootstrap_home_featured_products()                 │
│  remplace la section dans view.arch_db de `/`                   │
│  déclenché : migration · write produit · write catégorie        │
└─────────────────────────────────────────────────────────────────┘
```

**Doctrine** : BO Odoo = source de vérité catalogue ; rendu home = SSR custom CK ; `/shop` natif inchangé.

---

## 2. Modes de sélection

| Étape | Fonction | Condition | Résultat |
|-------|----------|-----------|----------|
| **1 — Curation BO** | `get_curated_featured_variants()` | ≥ 1 produit publié dans la catégorie xmlid | Jusqu'à **8** cartes |
| **2 — Repli auto** | `get_ready_featured_variants()` | Catégorie vide | **5** cartes fixes |
| **3 — Masquage** | — | Repli impossible (< 5 produits avec image) | Section retirée |

### Curation BO

- Catégorie : `dorevia_ck_marketone_content.public_categ_coups_de_coeur`
- Fusion automatique des doublons de nom « Coups de cœur » vers le xmlid (`_merge_duplicate_featured_categories`)
- Filtres : `is_published` · `website_published` · `sale_ok` · image valide
- Seuil : **1 carte suffit** en mode curaté

### Gestionnaire — deux chemins BO équivalents

1. **Fiche produit** → onglet eCommerce → catégorie « Coups de cœur »
2. **Fiche catégorie** « Coups de cœur » → liste des produits

Les deux déclenchent la reconstruction de la home.

---

## 3. Règle variantes → cartes

| Cas | Cartes |
|-----|--------|
| Produit simple | 1 carte · nom = nom template |
| Multi-variantes (Manio Crackers) | 1 carte par variante publiée avec image |

**Libellé** : valeur d'attribut pour les multi-variantes (ex. « Manio Crackers salé »).

**Image** : variante → template → variante sœur (fallback `_get_featured_image_url`).

**Liens** : `variant.website_url` (avec `?attribute_values=` si applicable).

---

## 4. Contenu d'une carte

| Zone | Source BO |
|------|-----------|
| Média | `image_512` variante / template / sœur |
| **Badge** (haut droite) | `website_ribbon_id` → `product.ribbon` |
| Étiquettes sous le titre | `product_tag_ids` (ex. `Guadeloupe · Épicerie`) — source unique BO |
| Ligne commerciale | `ck_net_quantity` + `ck_net_quantity_uom_id` · prix de référence optionnel (ex. `320 g · 18,13 €/kg`) |
| Titre | Libellé variante (§3) |
| Prix | `_get_combination_info` (figé dans le HTML au bootstrap) |
| CTA « Voir le produit » | URL variante · card cliquable |

**Prix** : calculés au moment de la reconstruction HTML — alignés sur le BO **après** refresh, pas à chaque visite.

---

## 5. Cycle de vie technique

| Déclencheur | Fichier |
|-------------|---------|
| Install / upgrade | `hooks.post_init_hook` |
| Migrations `19.0.1.15.0` → `19.0.1.18.4` | `migrations/*/post-migrate.py` |
| Write produit (champs vedettes) | `models/product_template.py` |
| Write catégorie « Coups de cœur » (`product_tmpl_ids`) | `models/product_public_category.py` |

`bootstrap_home_featured_products()` :

1. retire toute section vedettes existante (`_remove_all_featured_sections`) — évite les doublons ;
2. calcule les variantes (curation → repli) ;
3. génère le HTML ;
4. insère entre trust-bar (S2) et catégories (S4).

Le snippet `s_ck_featured_products` reste un **squelette vide** ; le contenu est dans l'arch « cuite ».

---

## 6. Décision MOA — unités card home (pas Inventaire / `uom.uom`)

**Décision actée MOA — 2026-06-16** : les quantités nettes et prix de référence affichés sur les cards home **ne réutilisent pas** les unités Inventaire (`Inventaire → Configuration → Unités de mesure`, modèle `uom.uom`). Ils passent par un modèle dédié **`dorevia.ck.card.uom`**.

### Pourquoi ce choix

| Critère | Inventaire `uom.uom` | `dorevia.ck.card.uom` (retenu) |
|---------|----------------------|--------------------------------|
| **Rôle** | Unité opérationnelle : stock, vente, facturation, BOM | Libellé **commercial** sur la card home |
| **Exemple** | Produit vendu à l'**unité** | Card affiche **320 g** (contenu net) |
| **Qui configure** | Logistique / stock | Équipe **Site web / eCommerce** |
| **Impact d'une modification** | Peut impacter stock, achats, prix unitaire | Limité à l'affichage Section 3 |
| **Périmètre module** | Dépendance Stock | Reste dans `website_sale` (pas de couplage stock) |

En pratique, la quantité nette card et l'unité de vente sont **deux informations distinctes** : une confiture peut se vendre à l'unité tout en affichant `320 g` sur la home.

### Modèle retenu

| Élément | Détail |
|---------|--------|
| Modèle | `dorevia.ck.card.uom` |
| Champs produit | `ck_net_quantity` · `ck_net_quantity_uom_id` · `ck_reference_price_uom_id` · `ck_show_reference_price` |
| Jeu initial | g, kg, ml, cl, l, pièce (seed `ck_card_uom_data.xml`) |
| Calcul prix/kg ou €/l | `family` (masse / volume / pièce) + `ratio` vers kg ou l (`home_featured.py`) |
| Règle pièce | Pas de prix de référence · pluriel `pièces` si quantité > 1 |

### Configuration BO

| Action | Chemin |
|--------|--------|
| Gérer la liste des unités | **Site web → Configuration → Unités card home** |
| Renseigner sur un produit vedette | Fiche produit → onglet eCommerce → **Quantité commerciale** |
| Droits menu + CRUD unités | Responsable des ventes **ou** Éditeur du site web (`19.0.1.20.6`) |

> La fiche produit **ne permet pas** de créer une unité à la volée (`no_create` sur les Many2one) : la liste est maîtrisée au menu dédié.

### Quand réviser vers `uom.uom` ?

Uniquement si la MOA décide explicitement que :
- la quantité nette card = **toujours** l'unité de vente / le conditionnement réel ;
- une **seule** source de vérité doit couvrir stock, vente et affichage home ;
- l'équipe eCommerce assume la gouvernance des UoM Inventaire.

Hors périmètre V1.1 — lot ultérieur si arbitrage MOA.

---

## 7. Historique livraisons (migrations clés)

| Version | Apport |
|---------|--------|
| `19.0.1.15.0` | Cartes maquette SSR |
| `19.0.1.17.0` | Catalogue MOA Manio + Galettes |
| `19.0.1.18.0` | Catégorie « Coups de cœur » + curation BO + amorçage set MOA |
| `19.0.1.18.2` | Fusion catégories doublons · remplacement section sans doublon |
| `19.0.1.18.3` | Badges via `website_ribbon_id` · ruban « Coup de cœur » |
| `19.0.1.18.4` | Refresh home depuis **fiche catégorie** e-commerce |
| `19.0.1.19.0` | Card V1.1 : étiquettes `product_tag_ids` · quantité nette · prix de référence · CTA « Voir le produit » |
| `19.0.1.20.4` | Rebuild home fiable (étiquettes SQL · `ir_http` GET `/`) · recette QA GO |
| `19.0.1.20.5` | Unités paramétrables `dorevia.ck.card.uom` (remplace Selection codées en dur) |
| `19.0.1.20.6` | Menu unités visible aux **Éditeurs du site web** (en plus des Responsables ventes) |

---

## 8. Critères de recette Section 3

| # | Contrôle |
|---|----------|
| 1 | Titre · sous-titre · CTA « Toute la boutique » |
| 2 | Cartes = produits de « Coups de cœur » uniquement (pas de produit hors catégorie) |
| 3 | Retrait d'un produit de la catégorie → disparaît de la home (fiche produit **ou** fiche catégorie) |
| 4 | Manio salé / sucré = 2 cartes si parent en catégorie |
| 5 | Galettes = template séparé (si en catégorie) |
| 6 | Badge = ruban produit · position haut droite · absent si pas de ruban |
| 7 | Images hauteur stable · prix = BO (après refresh) |
| 8 | CTA « Voir le produit » → bonne fiche / variante |
| 9 | Étiquettes `product_tag_ids` visibles sous le titre (ex. `Guadeloupe · Épicerie`) |
| 10 | Ligne commerciale `320 g` · prix de référence `18,13 €/kg` si renseigné |
| 11 | `/shop` inchangé · mobile 390 · desktop 1280 |
| 12 | Non-régression S1 Hero · S2 trust-bar |

---

## 9. Points ouverts / dette MOA

| Sujet | État |
|-------|------|
| Curation BO par catégorie | ✅ Livré |
| Refresh write produit | ✅ Livré |
| Refresh write catégorie | ✅ Livré `18.4` |
| Badges `website_ribbon_id` | ✅ Livré `18.3` |
| Repli auto si catégorie vide | ✅ Actif — spec recommandait masquer |
| Rendu live QWeb (sans arch cuite) | ❌ Non implémenté |
| Ordre vedettes indépendant de `/shop` | ❌ Même `website_sequence` |
| N cartes paramétrable | ❌ 8 / 5 figés |
| Vue BO liste curation dédiée | ❌ Absente |
| Étiquettes card via `product_tag_ids` | ✅ Livré `19.0` |
| Quantité nette + prix de référence card | ✅ Livré `19.0` |
| Unités card paramétrables (`dorevia.ck.card.uom`) | ✅ Livré `20.5` · décision MOA §6 · **recette manuelle QA GO** `20.6` |
| Réutiliser `uom.uom` Inventaire | ❌ **Rejeté MOA** §6 — lot ultérieur si arbitrage |
| Chips origine/famille 100 % BO | ❌ Heuristiques démo subsistent (remplacées par `product_tag_ids` sur les cards curatées) |

---

## 10. Références Dev

| Fichier | Rôle |
|---------|------|
| `home_featured.py` | Sélection · cartes · bootstrap |
| `models/product_template.py` | Champs card V1.1 · refresh au write produit |
| `models/ck_card_uom.py` | Modèle unités commerciales card home |
| `models/ir_http.py` | Rebuild home si arch périmée (GET `/`) |
| `models/product_public_category.py` | Refresh au write catégorie vedettes |
| `views/ck_card_uom_views.xml` | Menu **Unités card home** |
| `data/ck_card_uom_data.xml` | Seed g, kg, ml, cl, l, pièce |
| `data/ck_public_category_coups_de_coeur.xml` | Catégorie xmlid |
| `data/ck_product_ribbon_coups_de_coeur.xml` | Ruban « Coup de cœur » |
| `catalog_manioc_variants.py` | Alignement catalogue Manio / Galettes |
| `dorevia_ck_theme/.../website.scss` | Styles `.ck-featured-products--maquette` · badge haut droite |

**Tests** :

```bash
docker exec sandbox-odoo19-odoo-1 bash -c \
  'odoo -d dorevia_ck_marketone_01 --http-port=8079 --no-http \
   -u dorevia_ck_theme,dorevia_ck_marketone_content \
   --test-tags dorevia_ck_marketone_home_section3,dorevia_ck_marketone_home_section3_curation,dorevia_ck_marketone_catalog_manioc \
   --stop-after-init'
```

Tags : `dorevia_ck_marketone_home_section3` · `dorevia_ck_marketone_home_section3_curation` · `dorevia_ck_marketone_catalog_manioc`.

**Docs liées** :

- `SPEC_SECTION3_VEDETTES_CURATION_BO_V1.md` — spec curation + matrice livraison
- `SPEC_DEV_CARD_PRODUIT_COUPS_DE_COEUR_V1_1.md` — spec card V1.1 (quantité nette · prix de référence)
- `NOTE_ARCHITECTURE_SECTION3_VEDETTES_V1.md` — Section 3 (précédente)
- `RECETTE_VISUELLE_SECTION3_V1_1.md` — PV recette visuelle QA GO
- `ONBOARDING_QA_SECTION3_PR73_V1.md` — checklist QA Section 3 (mise à jour post-#73)
- `DECISION_MOA_SECTION3_PR73_CURATION_REPORTEE_V1.md` — historique arbitrage 2026-06-15

---

*Note d'architecture Section 3 — révision 2026-06-16 · `content` ≥ `19.0.1.20.6` · décision MOA unités card home §6.*
