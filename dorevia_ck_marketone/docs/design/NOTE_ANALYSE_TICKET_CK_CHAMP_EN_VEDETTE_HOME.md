# Note d'analyse Dev — Champ BO `En vedette` · Section « Nos coups de cœur »

| Champ | Valeur |
|---|---|
| **Ticket MOA** | `TICKET_DEV_CK_CHAMP_EN_VEDETTE_HOME_COUPS_DE_COEUR.md` |
| **Statut** | Implémenté — branche `feat/ck-featured-field-home` · **19.0.1.28.3** |
| **Baseline code** | `main` post-merge H1.2 · `dorevia_ck_marketone_content` **19.0.1.28.2** |
| **Module cible** | `dorevia_ck_marketone_content` (périmètre principal) |
| **Branche suggérée** | `feat/ck-featured-field-home` |

---

## 1. Synthèse exécutive

Le ticket MOA demande de **découpler** la section homepage **« Nos coups de cœur »** de la catégorie e-commerce **« Coups de cœur »**, au profit d’un booléen explicite `product.template.ck_is_featured` (**En vedette**).

**Constat code actuel** : la source de vérité homepage est la catégorie `public_categ_coups_de_coeur` via `get_curated_featured_variants()`. Un **fallback automatique** (`get_ready_featured_variants`, seuil 5 produits) subsiste si la curation catégorie est vide — **explicitement interdit** par le ticket §5.4.

**Effort estimé** : lot **modéré**, concentré sur `dorevia_ck_marketone_content` (~8 fichiers code + migration + tests). **Aucun changement thème** attendu si le rendu card SSR reste inchangé.

**Recommandation Dev** : GO technique — le ticket est **opposable**, le code existant est bien localisé, la migration est idempotente et réversible côté données.

---

## 2. État des lieux — code existant

### 2.1 Pipeline homepage Section 3

```text
bootstrap_home_featured_products()
  └─ get_curated_featured_variants()     ← filtre public_categ_ids ∈ « Coups de cœur »
  └─ si vide → get_ready_featured_variants()   ← FALLBACK auto (5 produits) ⚠️
  └─ render_ck_featured_cards() → build_featured_ssr_arch() → patch arch home
```

Fichier pivot : `dorevia_ck_marketone_content/home_featured.py`

| Constante / fonction | Rôle actuel |
|---|---|
| `FEATURED_CATEGORY_XMLID` | `dorevia_ck_marketone_content.public_categ_coups_de_coeur` |
| `get_curated_featured_variants()` | Sélection BO via catégorie · max 8 · ordre `website_sequence, id` |
| `get_ready_featured_variants()` | Fallback PR #73 · 5 premiers produits publiés |
| `MIN_FEATURED_PRODUCTS = 5` | Seuil fallback |
| `_ensure_featured_category()` | Crée / fusionne doublons catégorie |
| Critères éligibilité | `is_published` + `website_published` + `sale_ok` + image exploitable |
| Variantes | 1 carte / variante si multi-variantes (ex. Manio) — `_template_featured_variant_cap()` |

### 2.2 Back-office produit

Fichier : `views/product_template_views.xml` — onglet **Ventes** restructuré CK.

Bloc **Classement boutique** actuel :

```text
Catégories (public_categ_ids)
Étiquettes produit (product_tag_ids)
```

→ Le champ **En vedette** doit s’insérer **juste après Étiquettes produit** (ticket §6).

Modèle : `models/product_template.py` — champs card (`ck_net_quantity`, etc.) + hooks refresh home.

| Mécanisme | Déclencheur actuel |
|---|---|
| `FEATURED_REFRESH_FIELDS` | write produit → rebuild home si champ touché |
| `_ck_touches_featured()` | True si produit ∈ catégorie « Coups de cœur » (curation active) |
| `product_public_category.write()` | Rebuild si `product_tmpl_ids` modifié sur catégorie vedettes |

### 2.3 Données seed

| Asset | Fichier |
|---|---|
| Catégorie BO | `data/ck_public_category_coups_de_coeur.xml` |
| Ruban « Nouveau » | `data/ck_product_ribbon_coups_de_coeur.xml` |
| Amorçage produits en catégorie | migration `19.0.1.18.0/post-migrate.py` (Confiture, Manio, Galettes, Savon) |

### 2.4 Navigation Nav-Shop (impact indirect)

La catégorie **« Coups de cœur »** est une **racine catalogue** avec produits publiés → elle remonte dans le header via `nav_sync.py` / `build_shop_nav_trees()`.

Le ticket §5.1 précise : la catégorie **peut rester** en catalogue, mais **ne pilote plus la homepage**.  
→ **Hors périmètre ticket** : retirer « Coups de cœur » du header Nav-Shop (backlog densité / arbitrage MOA séparé).

### 2.5 Tests existants (surface impactée)

| Fichier test | Dépendance catégorie |
|---|---|
| `test_ck_home_section3_curation.py` | **Forte** — 15+ tests centrés catégorie |
| `test_ck_home_section3_featured_compose.py` | Moyenne — curated vs fallback |
| `test_ck_home_lot2_*.py` | Faible — helpers `detach_featured_curation()` |
| `ck_home_lot2_utils.py` | Helpers neutralisent catégorie pour mode auto |
| `test_ck_featured_propagation.py` | Refresh hooks |
| `test_ck_phase10_header_compose.py` | Non-régression marker `ck-featured-products__grid--stable` |

---

## 3. Écart ticket MOA ↔ code actuel

| Exigence MOA | Code actuel | Action Dev |
|---|---|---|
| Source = `ck_is_featured` | Source = catégorie `Coups de cœur` | Refactor `get_curated_featured_variants()` |
| Défaut `False` | N/A | Nouveau champ |
| Champ BO sous Étiquettes produit | Absent | Vue XML |
| Migration catégorie → `ck_is_featured=True` | Produits seed en catégorie | Migration post-install |
| **Aucun fallback** si 0 vedette | Fallback `get_ready_featured_variants()` | **Supprimer** branche fallback bootstrap |
| Section masquée si 0 vedette | Section peut subsister (fallback) ou disparaître partiellement | `_patch_homepage_featured_arch('', …)` |
| Ruban indépendant | Déjà le cas (`website_ribbon_id`) | Aucun changement |
| Max 8 · ordre sequence+id | Déjà le cas | Conserver |
| Variantes sur `product.template` | Déjà le cas | Conserver |
| Catégorie peut rester catalogue | Catégorie existe + nav | **Ne pas supprimer** xmlid catégorie |

---

## 4. Plan d'implémentation proposé

### Phase A — Modèle & BO

1. **`models/product_template.py`**
   - Ajouter :
     ```python
     ck_is_featured = fields.Boolean(
         string='En vedette',
         default=False,
         help='Affiche ce produit dans la section Nos coups de cœur de la page d\'accueil.',
     )
     ```
   - Ajouter `'ck_is_featured'` à `FEATURED_REFRESH_FIELDS`.
   - Refactor `_ck_touches_featured()` :
     ```python
     return any(self.mapped('ck_is_featured'))
     ```
     (plus de dépendance à la catégorie pour le refresh ciblé)

2. **`views/product_template_views.xml`**
   - Insérer après `product_tag_ids` dans le groupe `ck_shop_classification` :
     ```xml
     <field name="ck_is_featured" widget="boolean_toggle"/>
     ```

### Phase B — Logique homepage

3. **`home_featured.py` — `get_curated_featured_variants()`**
   - Remplacer le domaine catégorie par :
     ```python
     ('ck_is_featured', '=', True),
     ('is_published', '=', True),
     ('website_published', '=', True),
     ('sale_ok', '=', True),
     ```
   - Conserver filtres image + expansion variantes + plafond 8 + ordre.

4. **`home_featured.py` — `bootstrap_home_featured_products()` / `_bootstrap_home_featured_products_lang()`**
   - **Supprimer** l’appel fallback `get_ready_featured_variants()`.
   - Logique cible :
     ```text
     variants = get_curated_featured_variants(env)
     si variants → render cards (min 1 carte en mode curaté)
     sinon → featured_arch = '' → section retirée de l'arch home
     ```
   - Retirer `_ensure_featured_category(env)` du chemin bootstrap (optionnel : garder pour hygiène catalogue, **sans** lien homepage).

5. **`models/product_public_category.py`**
   - **Retirer** ou neutraliser le hook refresh sur write catégorie vedettes (la catégorie ne pilote plus la home).
   - Alternative conservatrice : garder le hook mais il ne déclenchera plus de changement homepage significatif — préférer **suppression** pour clarté contractuelle.

6. **Fonctions legacy**
   - `get_ready_featured_variants()` + `MIN_FEATURED_PRODUCTS` : **conserver** le code pour compat tests lot2 historiques **ou** refactor tests lot2 pour utiliser `ck_is_featured` — recommandation : **refactor tests lot2** vers `ck_is_featured=True` et marquer `get_ready_featured_variants` deprecated / test-only.

### Phase C — Migration

7. **`migrations/19.0.1.28.3/post-migrate.py`** (version bump proposée)

   ```python
   def migrate(cr, version):
       # 1. Produits actuellement dans catégorie « Coups de cœur » → ck_is_featured=True
       # 2. bootstrap_home_featured_products() pour reconstruire arch home
   ```

   Requête idempotente :
   ```sql
   UPDATE product_template pt
      SET ck_is_featured = TRUE
     FROM product_public_category_product_template_rel rel
     JOIN product_public_category cat ON cat.id = rel.category_id
     JOIN ir_model_data imd ON imd.model = 'product.public.category'
                          AND imd.res_id = cat.id
                          AND imd.module = 'dorevia_ck_marketone_content'
                          AND imd.name = 'public_categ_coups_de_coeur'
    WHERE rel.product_template_id = pt.id
      AND (pt.ck_is_featured IS NOT TRUE);
   ```

   + fallback ORM si xmlid absent (recherche par nom `Coups de cœur`).

8. **Ne pas** retirer automatiquement la catégorie des produits migrés (ticket : migration booléen uniquement ; retrait catégorie = action BO ultérieure).

### Phase D — Tests

9. **Nouveau / adapté** : `tests/test_ck_home_section3_featured_field.py` (ou refactor `test_ck_home_section3_curation.py`)

   | Test MOA | Couverture auto proposée |
   |---|---|
   | T1 Champ BO | Vue arch contient `ck_is_featured` après `product_tag_ids` |
   | T2 Produit vedette affiché | `ck_is_featured=True` → variant ∈ curated + arch home |
   | T3 Non publié exclu | `is_published=False` → exclu |
   | T4 Non vendable exclu | `sale_ok=False` → exclu |
   | T5 Sans image exclu | pas d'image → exclu |
   | T6 Limite 8 | 10 vedettes → max 8, ordre sequence/id |
   | T7 Aucun vedette | tous False → section absente arch |
   | T8 Migration | produit en catégorie → `ck_is_featured=True` ; retirer catégorie → home inchangée |
   | T9 Ruban indépendant | ruban sans featured / featured sans ruban |
   | T10 Variantes | multi-variantes → comportement Manio conservé |

10. **Mettre à jour** :
    - `ck_home_lot2_utils.py` → `detach_featured_curation` remplacé par `clear_ck_is_featured(env)`
    - `test_ck_home_section3_featured_compose.py` → plus de branche fallback
    - Tag CI : conserver `dorevia_ck_marketone_home_section3_curation` ou renommer

### Phase E — Livraison

11. Bump `dorevia_ck_marketone_content` → **`19.0.1.28.3`**
12. Note recette : `NOTE_RECETTE_CK_CHAMP_EN_VEDETTE_HOME.md`
13. **Redémarrage Odoo post-upgrade** obligatoire pour charger le champ Python (`ck_is_featured field is undefined` sinon)
14. **Pas de bump thème** sauf ajustement CSS non prévu

---

## 5. Fichiers impactés (liste cible)

| Fichier | Nature |
|---|---|
| `models/product_template.py` | Champ + hooks refresh |
| `views/product_template_views.xml` | Vue BO |
| `home_featured.py` | Sélection + bootstrap sans fallback |
| `models/product_public_category.py` | Retrait hook catégorie (ou neutralisation) |
| `migrations/19.0.1.28.3/post-migrate.py` | Migration données |
| `__manifest__.py` | Version |
| `tests/test_ck_home_section3_curation.py` | Refactor complet |
| `tests/test_ck_home_section3_featured_compose.py` | Adaptation |
| `tests/ck_home_lot2_utils.py` | Helpers |
| `tests/test_ck_home_lot2_*.py` | Adaptation helpers |
| Docs obsolètes (post-livraison) | `NOTE_ARCHITECTURE_SECTION3_*`, `SPEC_SECTION3_*` — **mention mise à jour MOA**, hors scope Dev immédiat |

**Non modifiés (confirmé ticket §8)** :

- `nav_sync.py` / header Nav-Shop
- `dorevia_ck_theme` (rendu card)
- Fiche produit front · shop · checkout

---

## 6. Risques & points de vigilance

| Risque | Mitigation |
|---|---|
| Régression homepage seed post-migration | Migration + `bootstrap_home_featured_products()` dans même post-migrate |
| Tests lot2 basés fallback auto | Refactor helpers vers `ck_is_featured` |
| « Coups de cœur » reste dans nav header | Documenté backlog MOA — hors ticket |
| Docs architecture §3 obsolètes | Note recette + MOA informée |
| Gestionnaire confond catégorie vs En vedette | Aide champ explicite + note onboarding QA |
| Write `public_categ_ids` ne refresh plus home | Refresh via `ck_is_featured` write — OK si MOA coche le booléen |

---

## 7. Arbitrages MOA — confirmés vs à clarifier

### Confirmés (alignés ticket)

- Catégorie catalogue **peut subsister** — pas de suppression xmlid
- Ruban **indépendant** — aucun lien auto ruban ↔ vedette
- **Pas de fallback** — section masquée si 0 produit `ck_is_featured`
- Champ sur **`product.template`** uniquement

### Clarification optionnelle (non bloquante Dev)

| Question | Recommandation Dev par défaut |
|---|---|
| Retirer « Coups de cœur » du header Nav-Shop dans ce ticket ? | **Non** — ticket §8 exclut Nav-Shop |
| Désactiver auto `ck_is_featured` si retrait catégorie ? | **Non** — ticket T8 : home reste pilotée par booléen |
| Sync bidirectionnelle catégorie ↔ booléen à l’avenir ? | **Non** — coupure nette après migration |

---

## 8. Critères GO exécution Dev

Le Dev peut démarrer l’implémentation si :

- [x] Ticket MOA GO explicite (§12)
- [x] Analyse code validée (ce document)
- [ ] Validation MOA lecture note analyse *(optionnel — ticket déjà GO)*

---

## 9. Séquence d'exécution recommandée

```text
1. Branche feat/ck-featured-field-home depuis main
2. Champ + vue BO (Phase A)
3. Refactor home_featured + hooks (Phase B)
4. Migration 19.0.1.28.3 (Phase C)
5. Tests T1–T10 (Phase D)
6. -u dorevia_ck_marketone_content sur seed + recette visuelle home
7. PR vers main + note recette
```

**Tests CI cibles** (sandbox : **`--http-port=8078`**, pas `--no-http` seul — conflit port 8069) :

```bash
--test-tags=dorevia_ck_marketone_home_section3_curation,dorevia_ck_marketone_home_section3_featured_field,dorevia_ck_marketone_home_section3,dorevia_ck_marketone_home_lot2,dorevia_ck_marketone_catalog_manioc,dorevia_ck_product_sales_tab_bo
```

---

## 10. Phrase de synthèse Dev

```text
Remplacer la curation homepage par catégorie « Coups de cœur » par un booléen BO explicite ck_is_featured,
supprimer tout fallback automatique, migrer les produits existants, conserver le rendu card et la logique variantes.
```

---

*Document d'analyse pré-exécution — implémentation sur `feat/ck-featured-field-home`. Voir `NOTE_RECETTE_CK_CHAMP_EN_VEDETTE_HOME.md`.*
