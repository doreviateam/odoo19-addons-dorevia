# Note MOA + Tech — CK Marketone « déployable » (seed code-first)

| Champ | Valeur |
| --- | --- |
| Date | 10 juillet 2026 |
| Projet | C-Kréyòl Marketone — Odoo 19 CE |
| Destinataires | MOA, Produit, QA, Dev, Exploitation |
| Statut | **Prêt signature MOA — §4 corrigé vs mesures 18079 (10 juil. 2026)** |
| Référence visuelle & fonctionnelle | Sandbox `dorevia_ck_marketone_01` — http://localhost:18079 |
| Stratégie actée (proposition) | **Option 1 — seed code-first** (cf. §2) |
| Remplace / corrige | [NOTE_MOA_ETAT_DES_LIEUX_DEPLOYABILITE_20260709.md](NOTE_MOA_ETAT_DES_LIEUX_DEPLOYABILITE_20260709.md) § « GO technique » (barre trop basse) |

---

## Synthèse exécutive

**« Install fraîche + verify vert » ≠ « conforme MOA ».**  
La pré-prod et le local ont prouvé que le socle deploy (Docker, scripts, hero HTTP) peut être vert alors que la home, le catalogue et la langue divergent de la sandbox recettée.

**Décision proposée :** arrêter les rustines (rsync, patch `.diff`, WIP serveur) et livrer **un artefact unique** :

```text
git pull (deploy + modules) → make install (base neuve) → make accept-moa → rendu = sandbox 18079
```

Le catalogue pilote, les images et la composition Home passent **dans le repo modules** (`dorevia_ck_marketone_content`), pas dans le filestore ni dans des éditions BO manuelles.

**La sandbox `18079` sert une seule fois** comme source d’extraction — pas comme mécanisme de livraison permanent.

---

## 1. Définition unique : « CK Marketone déployable »

Un environnement est **déployable MOA** si et seulement si, après **`make install`** sur base **neuve** (`--without-demo=all`), sans filestore préexistant, sans rsync, sans édition BO :

| Zone | Critère |
| --- | --- |
| **Langue & branding** | Site `fr_FR` · `website.name` = C-Kréyòl · société / email noreply CK · **pas** de tel `555-555` · cookies FR |
| **Home — composition** | Ordre : Hero MOA → Réassurance (4 items) → Vedettes (**4 cartes** affichées, cap `FEATURED_CURATED_MAX`) → Univers (4) → Coffret → Dual Pro → Éditorial |
| **Home — hero** | 3 visuels statiques MOA (crêpe / pâte manioc / marché) · dual CTA · carrousel |
| **Header / nav** | Barre service CK · recherche FR · nav : accueil boutique + **Épicerie** (+ rayons L1 seed) · Producteurs · Professionnels |
| **Catalogue pilote** | **9 templates** publiés (liste figée §4.1) · **6** `ck_is_featured` (7 variantes) · images **200** sur `/shop` et fiches · Manio 2 variantes + Galettes distinctes |
| **Footer** | 4 colonnes CK · © C-Kréyòl · liens légaux **200** · zéro `yourcompany` / `Company name` |
| **CMS** | `/contactus` · `/professionnels` · `/a-propos` · `/recettes` · fiche producteur pilote — **200** |
| **Gate unique** | `make accept-moa` **vert** (spec §3) |

Tout écart = **non déployable**, même si `make verify` (socle HTTP) est vert.

---

## 2. Stratégie actée : Option 1 — seed code-first

### Pourquoi pas le snapshot (Option 2)

| Option 2 (snapshot PG + filestore) | Problème |
| --- | --- |
| Dump `dorevia_ck_marketone_01` | Base dev **sale** (historique migrations, edits BO, multi-bases) |
| Blob binaire hors Git | Non diffable, drift silencieux, gate teste le dump pas le code |
| Prod / pré-prod | Héritent d’un artefact opaque |

**Option 2 acceptable uniquement** en **pont ≤ 1 semaine** (deadline démo immédiate), avec date de fin et migration vers Option 1.

### Option 1 — contenu technique

| Élément | Mécanisme Odoo idiomatique |
| --- | --- |
| Produits pilote | `data/ck_catalog_seed_*.xml` (noupdate=1 où BO doit rester souple) |
| Images produit | Fichiers `static/img/catalog/` + chargement `image_1920` via helper (`file_open` + base64) — **pas** de dépendance filestore |
| Catégories / ribbons / featured | Data XML + champs `ck_is_featured` |
| Home compose | Bootstrap **insert** (pas replace-only) · échec **explicite** si bloc manquant après post_init |
| Langue | `res.lang` fr_FR activée · `website.default_lang_id` forcé au post_init |
| Univers / coffret | Assets statiques déjà amorcés — généraliser le pattern hero/galettes |

**Module porteur :** `dorevia_ck_marketone_content` (seed MOA §4bis).  
**Deploy :** `ck-marketone-deploy` ne porte que l’infra ; la gate `accept-moa` vit dans deploy et appelle Playwright + odoo shell.

---

## 3. Ce qu’on arrête (effectivement)

| Pratique | Statut |
| --- | --- |
| rsync ciblé de fichiers modules vers le serveur | **Interdit** (sauf incident prod avec rollback documenté) |
| patch `.diff` flottants hors branche | **Interdit** |
| working tree dirty sur pré-prod / prod | **Interdit** — `git pull` + SHA tagué uniquement |
| déployer WIP non mergé sur pré-prod | **Interdit** |
| `make verify` seul comme critère de livraison MOA | **Remplacé** par `make accept-moa` |
| « tests post_install échouent pareil qu’avant » = OK | **Rejeté** — séparer tests **seed-required** (tag `ck_moa_seed`) vs tests unitaires purs |
| sync filestore sandbox comme procédure standard | **Remplacé** par images statiques versionnées |
| note « GO déployabilité » basée sur 6 checks HTTP | **Révoquée** — voir note 20260709 corrigée par cadrage présent |

---

## 4. Périmètre catalogue de référence (extraction 18079)

Liste **minimale MOA** à capturer en seed (alignée recettes Home 001B / NAV / DEMO-ONLINE) :

### 4.1 Produits (templates publiés) — liste figée réf. 18079

Mesure sandbox `dorevia_ck_marketone_01` (juillet 2026) : **9 publiés, 9/9 avec image**.

| # | Produit | `ck_is_featured` | Variantes | Rôle seed / recette |
| --- | --- | :---: | :---: | --- |
| 1 | Chapeau Panama | ✅ | 1 | Vedette · UOM card |
| 2 | Confiture de goyave | ✅ | 1 | Vedette · fiche shop · origine |
| 3 | Manio Crackers | ✅ | 2 (salé / sucré) | Vedette · variantes MOA |
| 4 | Pâte de manioc | ✅ | 1 | Vedette · catalogue manioc |
| 5 | Savon vétiver | ✅ | 1 | Vedette · univers soin |
| 6 | Tambour Gro Ka | ✅ | 1 | Vedette · univers artisanat |
| 7 | Coffret découverte créole | ❌ | 1 | Bloc coffret Home (hors vedettes) |
| 8 | Galettes de manioc | ❌ | 1 | Catalogue manioc · image statique MOA |
| 9 | Jus Mont-Pelé | ❌ | 1 | MOA-2 UOM · univers boissons |

**Vedettes — distinction seed vs affichage (important) :**

| Niveau | Valeur réf. 18079 | Règle |
| --- | --- | --- |
| **Seed (`ck_is_featured`)** | **6 templates** (7 variantes comptées côté `product.product`) | Tous flagués + image réelle (non placeholder) — reproduit la curation BO |
| **Home (affichage)** | **4 cartes** max | Cap code `FEATURED_CURATED_MAX = 4` dans `home_featured.py` — la home n’affiche que les 4 premières variantes éligibles après tri `website_sequence` |

Le seed **ne doit pas** se limiter à 4 produits flagués : sous-spécifier casserait la curation (Chapeau Panama, Pâte de manioc, Tambour Gro Ka absents du pool).

### 4.2 Catégories publiques

**Racines L1 (noms exacts BO réf. 18079) :**

| Catégorie | Rôle |
| --- | --- |
| **Épicerie** | Rayon L1 · slug `/shop/category/epicerie-1` (tuile univers « épicerie créole », nom catégorie = `Épicerie`) |
| **Boissons** | Rayon L1 |
| **Soin & Bien-être** | Rayon L1 |
| **Artisanat** | Rayon L1 · accueille Tambour Gro Ka |
| **Coups de cœur** | Catégorie vedettes — **obligatoire** au seed (conditionne la grille Home + routing featured) |

Sous-catégories L2 : documentées dans NAV-003 · inventaire Phase 1 (§6).

### 4.3 Données associées

- 1 producteur pilote (fiche `/producteur/atelier-hauts-goyaviers`)
- Ribbons / badges « Nouveau » · « Coup de cœur »
- Pages CMS déjà bootstrapées (footer links)

### 4.4 Hors périmètre seed v1

- Catalogue complet Excel MOA (> 9 produits)
- Multi-site · multi-langue EN
- Paiement / livraison prod

---

## 5. Gate `make accept-moa` — spécification

**Commande :** `make accept-moa` (deploy) = `scripts/accept-moa.sh`  
**Prérequis :** instance up après `make install` (base neuve ou CI éphémère).  
**Échec :** exit code ≠ 0 · rapport JSON + captures dans `rapport/accept_moa_<stamp>/`.

### 5.1 Checks automatisés (bloquants)

| ID | Assertion | Méthode |
| --- | --- | --- |
| A1 | `website.default_lang_id.code` = `fr_FR` | odoo shell |
| A2 | `website.name` contient C-Kréyòl · pas `My Website` | odoo shell |
| A3 | `res.company` sans phone `555` · email CK | odoo shell |
| B1 | Home HTML : `ck-hero--marketone-v1` + 3 assets MOA | curl |
| B2 | Home HTML : `s_ck_reassurance` + « Livraison France » | curl |
| B3 | Home HTML : bloc `ck-featured-products` + **exactement 4** cartes produit visibles, chaque image `/web/image/` **200** (cap affichage — cf. §4.1) | curl + HTTP · sélecteur DOM figé Phase 1 |
| B3b | odoo shell : **6** templates `ck_is_featured=True` publiés · **7** variantes éligibles vedettes (réf. 18079) | odoo shell |
| B4 | Home HTML : `ck-univers` · `ck-discovery-pack` · `ck-dual-engage` | curl |
| B5 | Footer : 4 colonnes CK · © C-Kréyòl · **0** `yourcompany` / `Company name` | curl |
| C1 | `/shop` **200** · **exactement 9** templates publiés (§4.1) | odoo shell |
| C2 | Tout produit publié : image non-placeholder (`b64_len` ≥ 500) | odoo shell |
| C3 | `/shop/category/epicerie-1` **200** (slug seed) | curl |
| D1 | Routes CMS : `/contactus` `/professionnels` `/a-propos` `/recettes` `/producteurs` **200** | curl |
| D2 | Fiche producteur pilote **200** | curl |
| E1 | Playwright desktop 1280 : home + shop · **pas** overflow horizontal | Playwright |
| E2 | Playwright mobile 390 : home + shop · **pas** overflow | Playwright |
| E3 | Capture : home hero · shop grid · footer · 1 fiche produit | PNG |

### 5.2 Relation avec `make verify`

| Script | Rôle |
| --- | --- |
| `make verify` | Socle infra (Odoo up, modules installés, hero HTTP minimal) — **CI deploy** |
| `make accept-moa` | **Conformité MOA complète** — **gate merge modules + release pré-prod/prod** |

`accept-moa` **inclut** verify ou le duplique — un seul vert public : `accept-moa`.

### 5.3 Tests Odoo (pytest)

| Tag | Signification |
| --- | --- |
| `ck_moa_seed` | Nécessite seed complet — **doit passer** sur install fraîche après Option 1 |
| `ck_unit` | Logique pure — toujours vert |
| post_install sans tag MOA | Ne bloque pas si data optionnelle absente |

---

## 6. Plan d’extraction sandbox → seed versionné

**Source :** `dorevia_ck_marketone_01` @ http://localhost:18079  
**Cible :** `dorevia_ck_marketone_content/`  
**Durée estimée :** 3–5 j · **1 chantier unique** (pas de micro-patches).

### Phase 0 — Gel

- [ ] MOA valide cette note (Option 1 + périmètre §4)
- [ ] Geler pré-prod : plus de deploy hors `main` mergé
- [ ] Branche unique : `feat/ck-catalog-seed-moa-v1`

### Phase 1 — Inventaire (readonly sandbox)

1. Export liste `product.template` publiés (id, name, price, categ, ck_is_featured, default_code)
2. Export `product.public.category` arbre L1/L2
3. Export `res.partner` producteurs pilote
4. Liste attachments images produit → hash → mapping fichier cible
5. Snapshot HTML home `/` (ordre blocs) comme référence ordre
6. **Sélecteurs DOM gate B3** : confirmer sur 18079 le markup vedettes Home (`ck-product-card__img` vs `.oe_product img` / shop) — figer dans l’inventaire avant implémentation `accept-moa.sh`

**Livrable :** `docs/cadrage/INVENTAIRE_CATALOGUE_SEED_18079.md` (auto-généré, commité).

### Phase 2 — Assets statiques

```text
dorevia_ck_marketone_content/static/img/catalog/
  confiture_goyave.webp
  manio_crackers_sale.webp
  ...
```

- Conversion webp (poids MOA) · nommage stable · pas de `/web/image/` en dur dans le seed
- Script dev one-shot : `scripts/export_sandbox_images.py` (reste dans repo, usage extraction uniquement)

### Phase 3 — Data XML + loader Python

- Fichiers `data/ck_catalog_seed_products.xml` · `data/ck_catalog_seed_categories.xml`
- Helper unique `catalog_seed.py` :
  - `load_product_image(static_path) → base64`
  - `ensure_catalog_seed(env)` idempotent
- Remplacer les placeholders crème par images réelles **à la création**
- `post_init_hook` : `ensure_catalog_seed` **avant** `bootstrap_all_marketone_content`

### Phase 4 — Bootstrap durci

- Corriger tous les `_patch_*` : **insert if missing**, jamais `return False` silencieux
- Si après post_init un bloc Home manque → **raise** ou log ERROR + test `ck_moa_seed` rouge
- `bootstrap_brand_name` étendu : langue FR · phone vide · website metadata

### Phase 5 — Gate & CI

- Implémenter `scripts/accept-moa.sh` + cible Makefile
- Job CI (ou `make fresh-install-test` étendu) : install → accept-moa
- Mettre à jour NOTE deployabilité 20260709 → statut **GO MOA** seulement si accept-moa vert

### Phase 6 — Déploiement pré-prod / prod

1. Merge `feat/ck-catalog-seed-moa-v1` → `main` modules
2. Merge deploy (accept-moa + doc)
3. Pré-prod : **nouvelle base** ou drop + `install` (pas update sur base squelettique)
4. Recette MOA navigateur sur URL publique · archive rapport

---

## 7. Critères de clôture chantier

| # | Critère |
| --- | --- |
| 1 | `make install` base neuve → `make accept-moa` **vert** en local |
| 2 | Même SHA → pré-prod **identique** à 18079 (smoke + captures) |
| 3 | Aucun rsync module / patch `.diff` utilisé pour la livraison |
| 4 | NOTE deployabilité 20260709 amendée ou supersédée |
| 5 | MOA signe recette sur URL pré-prod |

---

## 8. Validation MOA

| Décision | Choix |
| --- | --- |
| Stratégie seed | ☐ Option 1 confirmée · ☐ Option 2 pont (date fin : ______) |
| Périmètre catalogue §4 | ☐ OK · ☐ à ajuster : ______ |
| Gate `accept-moa` §5 | ☐ OK · ☐ à ajuster : ______ |
| Gel patchs §3 | ☐ OK |

**Validé par :** _________________ **Date :** _________

---

*Document rédigé sans modification de code — base de travail pour chantier unique ≥ 90.0.*
