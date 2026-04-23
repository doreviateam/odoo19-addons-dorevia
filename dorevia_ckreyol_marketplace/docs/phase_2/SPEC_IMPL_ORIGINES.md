# Spec d’implémentation — Porte **Origines** (`/shop`)

| Champ | Valeur |
|--------|--------|
| **Statut** | **Prête implémentation** — **verrouillages MOA/PV** intégrés (2026-04-22, voir §12 historique) + **§10 soldé** (copy S2, unicité SQL, droits modèle). |
| **Date** | 2026-04-22 (création + verrouillages MOA/PV + **clôture §10**). |
| **Module** | `dorevia_ckreyol_marketplace` (Odoo **19.0** CE) |
| **Références** | [CONTRAT_URL_ORIGINES §13](CONTRAT_URL_ORIGINES.md), [CONTRAT_URL_PROMOTIONS §13.6](CONTRAT_URL_PROMOTIONS.md), [ADR-CKR-007](../ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007), [ADR-CKR-001](../ARCHITECTURE_DECISION_RECORD.md#adr-ckr-001) |

Ce document **prescrit** la trajectoire d’implémentation **v1** : données, routes, hooks `WebsiteSale`, recherche boutique, bandeaux QWeb, fiche produit, comportements d’erreur. Les arbitrages **§3.2–§3.4** et **§4** (conflit `ckr_mode`) sont **verrouillés** (MOA/PV). Le **résidu §10** (copy S2, unicité SQL du slug, droits du modèle) est désormais **soldé** (**§2.2**, **§2.3**, **§6.1**). **Prête pour dev**.

---

## 1. Périmètre v1

| Inclus (v1) | Exclu / plus tard |
|---------------|-------------------|
| `ckr_mode=origin` + filtre **OU** lorsque **`ckr_origin`** présent ; **`ckr_mode=origin` seul** = **catalogue complet** + bandeau (**§3.2** acté) | Hub CMS **obligatoire** (**§13.8** : non requis) |
| Métadonnées **§3.1** du contrat (nom visiteur, phrase, slug, ordre, visibilité) | **Image** obligatoire par origine ; **contenu riche** long |
| Bandeau liste + **état vide dédié** + **repli** `/shop` nu si référence invalide | SEO avancé hors canonical de base |
| **Visibilité** origine sur **fiche produit** (forme simple) | Parcours multi-étapes marketing |
| Alias **`/origines`** → **301** → `/shop?…` | Réouverture **§13** (interdit sans MOA écrite) |

---

## 2. Décision technique recommandée (résidu §12 — source A1 + couche CK)

**Alignement [CONTRAT §13.3](CONTRAT_URL_ORIGINES.md#133-source-de-vérité-principes)** : privilégier le **socle catalogue standard** pour le **rattachement produit ↔ valeurs d’origine**, et une **couche CK légère** pour les **métadonnées éditoriales §3.1** non entièrement couvertes par le standard.

### 2.1 Socle catalogue (piste **A1**)

1. Créer (data ou script) un **`product.attribute`** dédié — ex. libellé interne *« Origine »* — configuré pour le **e-commerce** (`create_variant` = **jamais** / pas de variante, selon le modèle Odoo 19 retenu sur l’instance) afin d’autoriser **plusieurs valeurs** par `product.template` (**§13.1**).
2. Les **`product.attribute.value`** (ou équivalent selon build) portent le **libellé catalogue** ; les fiches produits sont alimentées en back-office comme aujourd’hui pour tout attribut filtrable boutique.

### 2.2 Couche CK « profil origine » (piste **A2 légère**, non A5)

Modèle dédié **minimal** — propos de nom : **`ckr.shop.origin`** — **une ligne par origine exposée sur le site** (scopée `website_id` si multi-site plus tard ; v1 = site courant acceptable).

| Champ (proposition) | Type | Rôle |
|---------------------|------|------|
| `attribute_value_id` | `Many2one` → `product.attribute.value` | **Lien** à la valeur catalogue « source de rattachement » (unicité **logique** : une ligne CK par valeur **et** par site si besoin). |
| `name_visitor` | `Char` | **Nom visiteur** (**§3.1**) ; fallback : `attribute_value_id.name`. |
| `context_phrase` | `Char` / `Text` | **Phrase courte** (**§3.1**). |
| `slug` | `Char` | **Slug stable** (**§3.1**), unique par site ; utilisé dans l’URL. |
| `sequence` | `Integer` | **Ordre** (**§3.1**). |
| `website_published` | `Boolean` | **Visibilité site** (**§3.1**). |

**Règle** : la **vérité** « ce produit est rattaché à telle origine géographique » reste portée par le **M2M catalogue** (lignes d’attribut sur le template) ; **`ckr.shop.origin`** ne **duplique pas** la liste des produits : il ne fait que **décorer** et **router** la lecture visiteur (**cohérence §12.3 item 5**).

**Contraintes SQL *(verrouillé §10)*** :

* `_sql_constraints = [("ckr_shop_origin_slug_website_uniq", "unique(website_id, slug)", "Le slug d'une origine doit être unique par site.")]` — **unicité logique** du slug **par site** (multi-site prévu, v1 acceptable avec `website_id` renseigné explicitement ou `NULL` si mono-site).
* `_sql_constraints` complémentaire recommandé : `unique(website_id, attribute_value_id)` — **une seule** ligne CK par **valeur d’attribut catalogue** et par site (empêche les doublons de profil pour la même origine).
* Validation Python (`@api.constrains("slug")`) : slug non vide, **normalisé** (minuscules, tirets, sans caractères spéciaux) — règle portable si multi-site ajouté plus tard.

**Droits d’accès *(verrouillé §10)*** :

* **`ir.model.access.csv`** :
  * **lecture publique** : **aucune** (`perm_read = 0`) — les profils sont **lus** côté serveur par le contrôleur (`sudo()`), **jamais** exposés via ORM public.
  * **groupe `base.group_user`** (employés internes) : **lecture seule** (`perm_read=1, write=0, create=0, unlink=0`).
  * **groupe `website.group_website_designer`** (ou `website.group_website_publisher` selon build Odoo 19 retenu) : **CRUD complet** (`perm_read=1, write=1, create=1, unlink=1`) — administration du modèle encadrée **uniquement** par les profils qui publient déjà le site.
* **`ir.rule`** : pas de règle multi-site v1 (mono-site). Si multi-site activé plus tard, ajouter une règle `website_id in allowed_websites` alignée sur le patron `website.multi_website_*` standard.
* **Pas** d’accès portail / public : conforme à l’exigence « administration encadrée back-office, sans complexifier v1 ».

**Si A1 insuffisant** (cas métier documenté au PV) : adapter le lien (`Many2one` vers autre référentiel) **sans** contredire §13 (pas de tag libre, pas de texte faible comme seule vérité).

### 2.3 Nom du modèle et conventions *(verrouillé §10)*

* **Nom technique** : **`ckr.shop.origin`** (singulier, cohérent avec `ckr.shop.*` existants).
* **Table SQL** : **`ckr_shop_origin`** (auto-dérivée).
* **Fichier Python** : `models/ckr_shop_origin.py`.
* **Fichier sécurité** : `security/ir.model.access.csv` (entrées dédiées `access_ckr_shop_origin_user`, `access_ckr_shop_origin_manager`).
* **Menu back-office** : **optionnel v1** — si exposé, sous **Site Web → Configuration → CK Réyol → Origines** (groupe `website.group_website_designer`).

---

## 3. Contrat d’URL et paramètres (Hybride H1)

### 3.1 Valeurs et whitelist

* Étendre dans `controllers/website_sale_ckr.py` :
  * `CKR_MODE_ORIGIN = "origin"`
  * `CKR_MODES_ALLOWED |= {"origin"}`
  * `CKR_MODE_TITLES["origin"] = "Origines"` — **valeur de repli** ; le **titre affiché** du bandeau suit la règle **§6.1** (dynamique si une seule origine active).
* `CKR_ALIAS_MODE["/origines"] = CKR_MODE_ORIGIN`
* Nouvelle route **`ckr_origines_alias`** → `_ckr_redirect(CKR_MODE_ORIGIN, kwargs)` (même helper que Kits/Promo).

### 3.2 Sélection d’origine(s) sur `/shop` *(verrouillé MOA/PV)*

* **`ckr_mode=origin` seul** (aucun `ckr_origin`) : **catalogue complet** (aucun filtre restrictif implicite sur les templates) + **bandeau** porte Origines actif (**§13** + intention MOA : pas de filtre caché qui réduirait le catalogue).
* **`ckr_origin=<slug>`** répété **plusieurs fois** → logique **OU** (**§13.2**) : résolution des profils **`ckr.shop.origin`** par `slug` + `website_published` + site ; domaine produit = **union** des `product.template` qui portent **au moins une** des valeurs d’attribut liées.

**Alternatives** rejetées pour v1 : `ckr_origin` en liste comma-separated ; ID interne seul sans slug (contre §3.1 du contrat).

### 3.3 Référence invalide *(verrouillé MOA/PV)*

* Slug inconnu, profil **non publié**, ou `attribute_value_id` **orphelin** : **redirection HTTP 302** vers **`/shop`** **nu** (**sans** `ckr_mode`, **sans** `ckr_origin`) — politique **« ne pas indexer »** / repli propre (**§13.9**). **Pas** de 500 ; **pas** de contexte erroné conservé.

### 3.4 Canonical *(verrouillé MOA/PV — multi-origines)*

* Étendre `website._get_canonical_url` comme Pack/Promo : pour `path == /shop` et `ckr_mode=origin` **whitelisté**, réinjecter `ckr_mode=origin`.
* Si **plusieurs** `ckr_origin` : reconstruire la portion `ckr_origin` du canonical avec un **ordre stable déterministe** : **dédupliquer** les slugs, puis **trier par ordre lexicographique croissant** (ASCII / `C` locale) ; réémettre les paires `ckr_origin=<slug>` dans cet ordre uniquement. **Objectif** : une seule URL canonique pour un même **ensemble** d’origines, quelle que soit l’ordre d’apparition dans la requête entrante.

---

## 4. Hooks `WebsiteSale` (non-surcharge de `shop()`)

Même architecture que [Pack/Promo](CONTRAT_URL_PROMOTIONS.md) :

| Hook | Effet mode `origin` |
|------|---------------------|
| `_get_search_options` | Passer `ckr_origin_only=True` et éventuellement `ckr_origin_slugs=[...]` (liste résolue côté contrôleur). |
| `_get_shop_domain` | Si **au moins un** `ckr_origin` valide résolu : **AND** avec domaine « templates ayant **au moins une** des valeurs d’attribut cibles » (**OU**). Si **`ckr_mode=origin` seul** : **ne pas** ajouter de filtre origine (catalogue complet — **§3.2**). |
| `_shop_get_query_url_kwargs` | Préserver `ckr_mode` + tous les `ckr_origin` dans pagination / tri (**re-sérialiser** les `ckr_origin` dans l’**ordre canonique** §3.4 pour stabilité des liens internes — recommandé). |
| `_get_additional_shop_values` | Flags QWeb : `ckr_origin_mode`, titres, textes, `ckr_origin_empty`, profil(s) actif(s) pour le bandeau (**§6**). |

**Conflit `ckr_mode` *(verrouillé MOA/PV)*** : une **seule** valeur de mode est **effective** par requête. Si la query contient **plusieurs** valeurs pour la clé `ckr_mode` (cas rare, lien malformé, concaténation d’URL) ou si plusieurs modes whitelistés seraient **lisibles** : **normaliser** en ne retenant que **la première valeur** rencontrée dans l’**ordre de priorité fixe** suivante : **`pack`** → **`promo`** → **`origin`** (i.e. si `pack` est présent parmi les candidats, il l’emporte ; sinon si `promo` est présent, il l’emporte ; sinon `origin`). Toute autre valeur est **ignorée** (pas d’erreur HTTP). **Implémentation** : fonction utilitaire unique `_ckr_effective_mode()` appelée partout où le mode est lu, pour aligner contrôleur, canonical et hooks.

---

## 5. `product.template._search_get_detail`

* Si `options.get("ckr_origin_only")` :
  * **sans** liste de slugs (mode « origine » mais **filtre géographique** non demandé — **§3.2**) : **ne pas** restreindre le `base_domain` (catalogue complet).
  * **avec** slugs résolus : domaine = **union** des templates portant les valeurs d’attribut cibles (**OU**).
  * si **au moins un** slug demandé mais **aucun** slug valide après résolution → traiter comme **référence invalide** côté contrôleur (**§3.3**, **302** `/shop` nu) **avant** d’atteindre la recherche si possible ; sinon sentinel + empty.
  * si **union** vide (origines valides mais **0** produit) → état vide dédié (**§13.10**).

**Performance** : préférer **une** requête SQL / `search` sur `product.template` avec sous-domaine sur `attribute_line_ids` / équivalent Odoo 19 plutôt que **N** requêtes par slug (détail impl. au dev).

---

## 6. Projection front — liste `/shop`

### 6.1 Template `ckr_shop_origin_banner`

* Fichier : `views/pages/ckr_shop.xml` (xpath analogue **avant** `oe_structure_website_sale_products_1`, priorité **33** ou cohérente avec Pack=31, Promo=32).
* **Condition** : `ckr_origin_mode`.
* Contenu minimal :
  * **S1 — titre *(verrouillé MOA/PV)*** : si **exactement une** origine est active (un seul `ckr_origin` valide résolu) → titre = **`name_visitor`** de ce profil (fallback `CKR_MODE_TITLES["origin"]` = « Origines »). Sinon → titre **« Origines »**.
  * **S2 — phrase de contexte *(verrouillé §10)*** :
    * **Aucune origine filtrée** (`ckr_mode=origin` seul) : **« Parcourez le catalogue par origine. »**
    * **Une seule origine active** : `context_phrase` du profil si renseignée ; **à défaut** → **« Produits issus de {name_visitor}. »**
    * **Plusieurs origines actives** (filtre OU) : **« Produits issus des origines sélectionnées. »** (formulation sobre, sans énumération — évite les phrases longues et préserve la stabilité i18n ; l’énumération reste possible ultérieurement si besoin métier).
  * Variante **`--empty`** si `ckr_origin_empty` *(verrouillé §10)* :
    * **Titre** : **« Aucun produit pour cette sélection. »**
    * **Message** : **« Cette origine n’a pas encore de produit disponible. »**
    * **Rebond principal** : lien **« Voir tout le catalogue »** → **`/shop`** nu.
    * **Rebond secondaire *(optionnel v1)*** : lien **« Parcourir les origines »** → **`/shop?ckr_mode=origin`** (catalogue complet + bandeau).

### 6.2 SCSS

* `static/src/scss/layout/_shop.scss` : classes **`.ckr-shop-origin-banner`** (+ `--empty`), alignées visuellement sur Pack/Promo.

---

## 7. Fiche produit

* **`views/pages/ckr_product.xml`** (ou héritage existant) : bloc **lisible** listant les **noms visiteur** des origines du produit (résolution **profil CK** si présent, sinon valeur attribut). **Forme simple** v1 : texte ou liste à puces.

---

## 8. Données initiales et migration stub

1. **XML data** : attribut *Origine* + quelques **valeurs** exemples (optionnel, peut être vide en prod).
2. **Profils `ckr.shop.origin`** : data seed ou écran back-office (si menu **paramètres** CK ajouté — **hors obligation** v1 si chargement manuel par SQL/XML suffit).
3. **Retrait stub `/origines`** : même schéma que [data/ckr_cleanup_kits_stub.xml](data/ckr_cleanup_kits_stub.xml) — supprimer `website.page` conflictuelle si présente ; retirer `ckr_page_origines` du manifest si le template ne sert plus.
4. **`views/snippets/ckr_entries.xml`** : `href` carte **Origines** → **`/origines`** (déjà attendu).

---

## 9. Tests de recette (E2E)

| # | Scénario | Attendu |
|---|----------|---------|
| 1 | `GET /origines` | **301** → `/shop?ckr_mode=origin` (params préservés hors `ckr_mode` conflictuel). |
| 2 | `GET /shop?ckr_mode=origin&ckr_origin=<slug_valide>` | **200**, bandeau, liste filtrée **OU** si multi-slugs. |
| 3 | `GET /shop?ckr_mode=origin&ckr_origin=inconnu` | **302** → `/shop` nu sans paramètres invalides (**§3.3**). |
| 4 | Origine valide, **0** produit | Bandeau **empty** + message dédié. |
| 5 | Non-régression `/kits`, `/promotions`, `/categories`, `/shop` nu | Inchangé. |
| 6 | Canonical sur `/shop?ckr_mode=origin&ckr_origin=…` (multi-slugs) | Slugs **triés** lexicographiquement dans le canonical (**§3.4**) ; même ensemble = même canonical. |
| 7 | Fiche produit avec 2 origines | Affichage **deux** libellés visiteur. |
| 8 | `GET /shop?ckr_mode=origin` (seul) | **200**, bandeau, **liste complète** catalogue (pas de filtre origine implicite). |
| 9 | `GET /shop?ckr_mode=promo&ckr_mode=origin` | Un **seul** mode effectif selon **§4** (priorité `pack` > `promo` > `origin` → ici **promo**). |

---

## 10. Points ouverts (résidu mineur avant dev) — **SOLDÉ 2026-04-22**

- [x] **Copy S2** : formulations figées en **§6.1** (aucune / une / plusieurs origines + variante `--empty`).
- [x] **Unicité SQL** `ckr.shop.origin.slug` : `unique(website_id, slug)` + `unique(website_id, attribute_value_id)` actés en **§2.2**.
- [x] **Nom modèle + droits** : `ckr.shop.origin`, `ir.model.access.csv` (lecture employé / CRUD `website.group_website_designer`), pas d’accès public ; détail **§2.2 / §2.3**.

**Résultat** : plus de résidu bloquant — la spec est **intégralement implémentable**. Les ajustements ultérieurs (copy i18n, menu back-office optionnel, règle multi-site) seront portés par des itérations dédiées hors v1.

---

## 11. Correspondance check-list [CONTRAT §12.2](CONTRAT_URL_ORIGINES.md)

| §12.2 | Livrable technique |
|-------|---------------------|
| A1 / A2 écrit | §2 de ce document (**acté**). |
| Paramètres URL + HTTP repli | §3 (**302** invalide, **§3.3**). |
| Copy | Textes QWeb figés **§6.1** (S1 + S2 + `--empty`) — **§10 soldé**. Export `.pot` à produire à la construction. |
| Canonical + SEO | §3.4 + test E2E §9 n°6 |
| Fiche produit | §7 |

---

## 12. Historique du document

| Date | Changement |
|------|------------|
| 2026-04-22 | **Création** — spec d’implémentation v1 : A1 + `ckr.shop.origin`, `ckr_mode=origin`, `ckr_origin` multi, hooks, bandeau, stub, tests, §10 ouvert. |
| 2026-04-22 | **Verrouillages MOA/PV** : (1) `ckr_mode=origin` seul = **catalogue complet** + bandeau ; (2) titre bandeau **dynamique** si une seule origine sinon **« Origines »** ; (3) repli référence invalide = **302** `/shop` nu ; (4) canonical multi-`ckr_origin` = slugs **dédupliqués + tri lexicographique** ; (5) conflit multi-`ckr_mode` = **priorité** `pack` > `promo` > `origin` via `_ckr_effective_mode()`. §9 tests 3/6/8/9 ; §4/§5 alignés ; §10 réduit. Statut → **Prête implémentation**. |
| 2026-04-22 | **Clôture §10** : (a) **copy S2** figée en **§6.1** (aucune / une / plusieurs origines + variante `--empty` : titre, message, rebonds) ; (b) **contraintes SQL** verrouillées en **§2.2** — `unique(website_id, slug)` + `unique(website_id, attribute_value_id)` + validation Python du slug ; (c) **nom modèle + droits** en **§2.2 / §2.3** — `ckr.shop.origin`, `ir.model.access.csv` (employé lecture seule, `website.group_website_designer` CRUD, pas d’accès public), pas d’`ir.rule` v1. **§10 marqué SOLDÉ** — **prêt dev**. |
