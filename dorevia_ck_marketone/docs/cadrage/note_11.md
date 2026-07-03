# Mini-note d'approche — CATALOG-ARCHI-001 — Lot C

## Routes catégories · Noindex · Sitemap · Redirections

| Champ             | Valeur                                                                           |
| ----------------- | -------------------------------------------------------------------------------- |
| Projet            | C-Kréyòl / CK Marketone                                                          |
| Lot               | CATALOG-ARCHI-001 — Lot C                                                        |
| Objet             | Sécurisation SEO et comportement des routes catégories selon statut d'exposition |
| Statut            | Note d'approche préalable — aucun code avant validation                          |
| Pré-requis        | Lot A posé, Lot B clôturé, statuts d'exposition disponibles                      |
| Décision actuelle | NO GO code direct — validation architecture requise                              |

---

# 1. État actuel routes / sitemap / SEO

Le Lot C est le plus sensible du lot CATALOG-ARCHI-001, car il touche à la manière dont les routes catégories sont servies publiquement, indexées ou redirigées.

À ce stade, le site dispose déjà :

* des routes catégorie Odoo / CK ;
* de la boutique globale `/shop` ;
* de catégories publiques ;
* d'une logique d'exposition catalogue renforcée par les Lots A/B ;
* d'un socle de qualification produit ;
* d'une détection des incohérences catalogue.

En revanche, le Lot C introduit ou formalise des mécanismes plus risqués :

* comportement route selon statut `ck_exposure_status` ;
* redirections 301 / 302 ;
* pages 404 contrôlées ;
* injection `noindex` ;
* exclusion sitemap ;
* cohérence entre `noindex` et sitemap.

Point de vigilance :

> Une page ne doit jamais être à la fois `noindex` et présente dans le sitemap public.

---

# 2. Décision par statut de catégorie

Le comportement doit être stable, testable et non laissé à une décision ad hoc par catégorie.

## Matrice cible V1

| Statut     | Route directe                                        | Navigation                      | SEO / sitemap           |
| ---------- | ----------------------------------------------------- | ---------------------------------- | -------------------------- |
| `active`   | 200 catégorie marchande                              | visible si exposable            | indexable si contenu OK |
| `promise`  | 302 vers `/shop` en V1, sauf page promesse validée   | non visible en navigation forte | hors sitemap            |
| `hidden`   | 302 vers `/shop`                                     | invisible                       | hors sitemap            |
| `draft`    | 404                                                  | invisible                       | hors sitemap            |
| `archived` | 301 vers catégorie remplaçante si définie, sinon 404 | invisible                       | hors sitemap            |

## Arbitrage recommandé

Pour la V1, ne pas créer automatiquement de page promesse éditorialisée.

Donc :

* `promise` → 302 vers `/shop` ;
* future page promesse éditorialisée → backlog ou sous-lot dédié ;
* si une page promesse existe déjà et est validée MOA, elle peut être servie en 200 + `noindex`.

Objectif :

> Éviter de transformer le Lot C en chantier éditorial ou SEO complexe.

---

# 3. Stratégie `noindex`

## Principe

Le `noindex` doit protéger les pages pauvres ou non marchandes contre une indexation prématurée.

Pages concernées :

* catégorie `promise` servie en 200 ;
* page de promesse éditorialisée sans contenu marchand réel ;
* catégorie pauvre exceptionnellement accessible ;
* page temporaire de transition ;
* toute page catégorie non active que l'on choisit de servir en 200.

## Pages non concernées

Ne pas appliquer `noindex` à :

* `/shop` ;
* catégorie `active` exposable ;
* fiche produit qualifiée ;
* page catégorie riche et validée SEO.

## Règle V1 recommandée

En V1, limiter les cas `noindex`.

Si une catégorie n'est pas `active`, préférer :

* `302 /shop` pour `promise` ou `hidden` ;
* `404` pour `draft` ;
* `301` ou `404` pour `archived`.

Le `noindex` ne devient nécessaire que si l'on sert réellement une page 200 non indexable.

Critère :

> Pas de page 200 pauvre sans `noindex`.

---

# 4. Stratégie sitemap

## Principe

Le sitemap doit refléter uniquement les pages que CK assume comme indexables.

Doivent être exclus du sitemap :

* catégories `promise` ;
* catégories `hidden` ;
* catégories `draft` ;
* catégories `archived` ;
* toute page catégorie avec `noindex` ;
* toute catégorie non exposable selon `_is_ck_exposable()`.

Peuvent être présentes :

* `/shop` ;
* catégories `active` et exposables ;
* fiches produit qualifiées ;
* autres pages SEO validées.

## Garde-fou absolu

```text
noindex + sitemap = interdit
```

Critère QA :

* si une URL contient une balise `noindex`, elle ne doit pas apparaître dans `/sitemap.xml`.

---

# 5. Redirections 301 / 302 / 404

## Règles V1

| Cas                                   | Comportement                   |
| -------------------------------------- | --------------------------------- |
| Catégorie `active`                    | 200                            |
| Catégorie `promise`                   | 302 vers `/shop`               |
| Catégorie `hidden`                    | 302 vers `/shop`               |
| Catégorie `draft`                     | 404                            |
| Catégorie `archived` avec remplaçante | 301 vers catégorie remplaçante |
| Catégorie `archived` sans remplaçante | 404                            |

## Justification

* `302` pour `promise` / `hidden` : statut potentiellement réversible, ne pas figer SEO.
* `404` pour `draft` : contenu non public, non prêt.
* `301` pour `archived` avec remplaçante : ancienne URL remplacée définitivement.
* `404` pour `archived` sans remplaçante : éviter de maintenir une page morte.

## Champ recommandé

Pour `archived` :

```text
ck_replacement_category_id
```

Si renseigné :

```text
archived → 301 vers ck_replacement_category_id
```

---

# 6. Tests QA minimaux

## Routes à tester

* `/shop`
* `/shop/category/epicerie-1`
* `/shop/category/boissons-123`
* `/shop/category/soin-bien-etre-2`
* `/shop/category/artisanat-3`
* une catégorie `draft` de test si possible
* une catégorie `archived` de test si possible

## Tests fonctionnels

1. Catégorie `active`

   * route 200 ;
   * produits visibles ;
   * pas de `noindex` ;
   * présente dans sitemap si exposable.

2. Catégorie `promise`

   * 302 vers `/shop` en V1 ;
   * absente du header ;
   * absente du sitemap.

3. Catégorie `hidden`

   * 302 vers `/shop` ;
   * absente header/Home/footer ;
   * absente sitemap.

4. Catégorie `draft`

   * 404 ;
   * absente sitemap.

5. Catégorie `archived`

   * 301 vers remplaçante si définie ;
   * 404 sinon ;
   * absente sitemap.

6. Cohérence `noindex`

   * aucune URL `noindex` dans le sitemap.

7. Non-régression `/shop`

   * `/shop` reste accessible ;
   * les produits publiés et vendables restent visibles selon règles catalogue ;
   * pas d'effet de bord sur les cards Lot B.

## Viewports

* desktop 1280 px ;
* mobile 390 px.

---

# 7. Risques et rollback

## Risques principaux

### Risque 1 — Casser des URLs existantes

Les catégories sont déjà accessibles. Un changement trop brutal pourrait casser des liens partagés ou indexés.

Mitigation :

* privilégier `302` pour `promise` / `hidden` ;
* utiliser `301` uniquement pour `archived` avec remplaçante claire ;
* documenter les routes avant/après.

### Risque 2 — Incohérence SEO

Risque : une page `noindex` reste dans le sitemap.

Mitigation :

* test automatisé dédié ;
* contrôle manuel `/sitemap.xml`.

### Risque 3 — Trop de logique dans le contrôleur

Risque : surcharger fortement `CkWebsiteSaleController`.

Mitigation :

* isoler la décision dans un helper ;
* éviter une logique dispersée dans les templates ;
* centraliser la matrice de statut.

### Risque 4 — Confusion `promise`

Risque : `promise` devienne une pseudo-page vide.

Mitigation V1 :

* `promise` → 302 vers `/shop` ;
* page promesse réelle reportée hors Lot C sauf validation MOA.

### Risque 5 — Régression boutique globale

Risque : les produits vendables disparaissent de `/shop`.

Mitigation :

* rappeler que `/shop` n'est pas gouverné comme une catégorie ;
* le statut catégorie pilote les portes d'entrée, pas nécessairement l'existence du produit dans la boutique globale.

## Rollback

Rollback attendu :

1. désactiver la surcharge comportement route catégorie ;
2. revenir au comportement standard catégorie ;
3. conserver les champs `ck_exposure_status` et `ck_replacement_category_id` sans les utiliser pour les routes ;
4. retirer temporairement le filtrage sitemap si nécessaire ;
5. garder Lot A/B intacts.

Le Lot C doit donc être développé de manière isolable.

---

# Verdict d'approche

```text
CATALOG-ARCHI-001 — Lot C
→ GO approche architecture
→ NO GO code tant que la matrice routes/SEO n'est pas validée
→ V1 sobre recommandée :
   active   = 200
   promise  = 302 /shop
   hidden   = 302 /shop
   draft    = 404
   archived = 301 remplaçante sinon 404
→ noindex limité aux pages 200 non indexables
→ sitemap strictement aligné avec les pages indexables
```
