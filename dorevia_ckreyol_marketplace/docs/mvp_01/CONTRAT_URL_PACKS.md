# Contrat d’URL de la porte **Pack** *(libellé visiteur : **Kits**)* — analyse comparative

| Champ | Valeur |
|--------|--------|
| **Statut** | **Tranché et déployé** — **Hybride H1** retenu (2026-04-21) avec paramètre **`ckr_mode=pack`**, voir §12 ; **mise en service opérée en module 19.0.1.1.0** (voir §13 « Mise en service »). |
| **Date** | 2026-04-21 |
| **Périmètre** | Forme canonique de l’URL empruntée par la carte **Kits** de la section Explorer (libellé visiteur) et par tout lien partagé équivalent, pour arriver sur une **lecture boutique filtrée** sur les produits *« pack »* au sens du module OCA **`product_pack`**. |
| **Prérequis actés** | Source de vérité **`product.template.pack_ok`** ([SPEC_SHOP_PORTES §4.3](SPEC_SHOP_PORTES.md)) ; convergence commerciale **`/shop`** ([ADR-CKR-007](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007)) ; libellé visiteur **Kits** et règle de bi-lexique front / back-office ([ADR-CKR-008](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008)). |

Ce document a **exposé** les trois options demandées (plus variantes hybrides), les a évaluées selon les **critères doctrinaux** du projet, a formulé une **recommandation motivée**, et la décision a été **actée** le 2026-04-21 (voir §12).

> **Convention lexicale interne au document** — conformément à la règle de bi-lexique [ADR-CKR-008](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008) :
> - **Pack** est utilisé pour tout ce qui est **technique / source de vérité / implémentation** (champ `pack_ok`, module `product_pack`, titre de ce document).
> - **Kits** est utilisé pour ce qui est **libellé visiteur / URL visible / copy** (carte Explorer, `/kits`).
>
> Les deux ne désignent **pas** deux choses différentes : c’est **la même porte**, vue sous deux registres.

---

## 1. Cadre doctrinal rappelé

La décision d’URL doit respecter, dans l’ordre :

1. **Standard Odoo / brique OCA installée d’abord** ([ADR-CKR-001](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-001)) : pas de logique métier parallèle.
2. **Convergence commerciale unique sur `/shop`** ([ADR-CKR-007](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007)) : pas d’univers commercial alternatif hors boutique native.
3. **Source de vérité unique** : `product_pack.pack_ok`. Pas de second marqueur « pack » côté CK.
4. **Construction CK minimale et présentationnelle** ([ADR-CKR-002](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-002)) : la couche CK habille, elle ne recompose pas la logique.
5. **Bi-lexique front / back-office** ([ADR-CKR-008](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008)) : les **URL visibles** et les **libellés** côté visiteur utilisent la grille **Kits** (donc URL front `/kits`) ; les **paramètres et conventions internes** restent sur la grille **Pack** (domaine `pack_ok=True`, variable interne `ckr_mode=pack`…). Une option qui **force** l’exposition de « pack » côté visiteur (URL, titre) doit être écartée ; une option qui **force** l’exposition de « kits » côté code (nom de champ, filtre, server action) doit l’être aussi.

Une option qui **duplique** la source de vérité, qui **fragmente** le parcours d’achat, ou qui **reconstruit** une boutique parallèle est **disqualifiée par doctrine**, indépendamment de ses mérites techniques locaux.

---

## 2. État des lieux technique

**Module OCA `product_pack` installé sur `tenant_o7`** :

- Champ principal : **`product.template.pack_ok`** (booléen, libellé *« Is Pack? »*).
- Champs secondaires (comportement commande) : `pack_type` ∈ {`detailed`, `non_detailed`}, `pack_component_price` ∈ {`detailed`, `totalized`, `ignored`}.
- Composants : `product.pack.line` (accessible via `pack_line_ids`).
- Méthode composite : `_is_pack_to_be_handled()` (combine `pack_ok` + `pack_type` + contexte ; **utile vente / fiche**, **pas** pour le filtre boutique simple).
- **Aucun contrôleur web / route / surcharge `website_sale`** dans le module : la couche front est entièrement à construire côté CK si elle doit exister.

**Odoo `website_sale` — contrats d’URL standard disponibles** :

- `/shop` : liste complète publiée, avec paramètres `search`, `order`, `page`, facettes `attrib` (via attributs eCommerce).
- `/shop/category/<id>-<slug>` : liste filtrée par `product.public.category` (breadcrumb natif, sidebar catégories).
- `/shop/<product-slug>` : fiche produit.

**Stub CK actuel** :

- Route non dédiée : page `website.page` pointant sur le template `ckr_page_compositions`, URL **`/kits`** (alignée sur le libellé visiteur [ADR-CKR-008](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008)), contenu éditorial « Bientôt disponible ».

---

## 3. Critères d’évaluation

| # | Critère | Pondération qualitative |
|---|---------|-------------------------|
| C1 | **Alignement doctrinal** (ADR-001 / 007 / 008, incluant bi-lexique front *Kits* / back-office *Pack*) | **Élevée** |
| C2 | **Source de vérité unique** (pas de duplication avec `pack_ok`) | **Élevée** |
| C3 | **Convergence `/shop`** (pas de silo parallèle) | **Élevée** |
| C4 | **Charge de construction CK** (routes, contrôleurs, templates, data) | Moyenne |
| C5 | **URL lisible, partageable, SEO** (canonical, bookmark, alignée libellé visiteur **Kits**) | Moyenne |
| C6 | **Compatibilité filtres natifs** (`search`, `attrib`, `order`, pagination) | Moyenne |
| C7 | **Robustesse** (produit dépublié, `pack_ok` retiré, catalogue vide) | Moyenne |
| C8 | **Maintenabilité upgrade** (Odoo 19 → 20, évolutions OCA) | Moyenne |
| C9 | **Effort de migration** depuis le stub actuel `/kits` | Faible |

---

## 4. Option 1 — **Catégorie publique « Kits »**

### Mécanisme

Créer une **`product.public.category`** dédiée libellée **« Kits »** côté visiteur (racine ou sous-arbre) et y **rattacher** tous les produits avec `pack_ok=True`. URL obtenue : **`/shop/category/<id>-kits`** (forme standard Odoo, slug aligné sur le libellé visiteur [ADR-CKR-008](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008)).

Le rattachement peut être :

- **(1a) Manuel** : chaque produit « pack » est ajouté à la main à la catégorie publique par le gestionnaire catalogue.
- **(1b) Automatique** : un **compute / inverse** ou une **server action** CK synchronise l’appartenance à la catégorie en fonction de `pack_ok`.

### Avantages

- **Contrat d’URL 100 % natif Odoo** : `/shop/category/<id>-<slug>`, bookmarkable, SEO-friendly, présent dans le sitemap standard ; slug visiteur **`kits`** cohérent avec la règle de bi-lexique.
- **Sidebar catégories** : le visiteur voit « Kits » sélectionné, breadcrumb natif.
- **Compatibilité parfaite** avec `search`, `attrib`, `order`, `page` (C6).
- **Aucun contrôleur CK** côté route (C4 : charge faible **sur l’axe URL**).

### Limites / coûts

- **Duplication de la source de vérité** (C2) : l’appartenance à la catégorie n’est **pas** `pack_ok`, c’est un Many2many parallèle.
  - Variante **1a manuelle** : fragile (oubli humain, désynchronisation silencieuse, pas de garantie que « tous les packs » y soient ni que « seuls les packs » y soient).
  - Variante **1b automatique** : introduit du code CK (compute / server action) qui **reconstitue** logiquement `pack_ok` dans une autre structure — donc une **deuxième vérité partielle** vivant dans la base.
- **Sémantique impure** (C1) : les autres catégories publiques structurent par **famille de produit** (biscuits, boissons, épicerie…) ; glisser « Kits » au même niveau **mélange** *type d’article* et *statut d’assemblage*. Tension directe avec [ADR-CKR-008](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008) qui distingue explicitement **Catégories** (famille) et **Kits** (assemblage, logique Pack en interne).
- **Multi-catégorie** : un produit « pack » appartiendra à la fois à sa famille (« Épicerie ») et à « Kits » → acceptable côté Odoo mais brouille le lecteur qui voit le même produit dans deux rayons de nature différente.
- **Effort de synchro** continu : chaque changement de `pack_ok` en back-office doit être répercuté (humain ou automatique).
- **Upgrade / résilience** (C8) : si `pack_ok` disparaît à l’avenir (montée de version, remplacement OCA), la catégorie publique reste en base et doit être nettoyée.

### Verdict

Séduisant à la lecture rapide (« on reste dans du natif »), **mais** en réalité **crée** une seconde source de vérité là où `pack_ok` suffit déjà. Tension directe avec C2 et C1 (sémantique ADR-008). Plutôt **défavorable** sur la doctrine, malgré l’URL propre.

---

## 5. Option 2 — **Paramètre CK dédié sur `/shop`**

### Mécanisme

Conserver `/shop` comme URL de base et interpréter un paramètre CK explicite. Le serveur CK intercepte la requête (héritage léger du contrôleur `WebsiteSale`) et ajoute `("pack_ok", "=", True)` au domaine produit, puis laisse le rendu boutique standard opérer.

URL type : **`/shop?ckr_mode=pack`** (le paramètre est une **convention interne** alignée sur la **grille back-office** de la règle de bi-lexique [ADR-CKR-008](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008) ; la valeur alternative `ckr_mode=kits` serait cohérente avec la grille front, voir §11 *Décision attendue*).

> **Note d’exposition** : dans le schéma « Option 2 seule », le visiteur **voit** cette URL (ce qui expose la grille technique). Dans le schéma **Hybride H1**, l’URL visible est **`/kits`** (grille front), et `/shop?ckr_mode=pack` est **interne** (canonique ou alias selon direction retenue). C’est H1 qui permet de **respecter la règle de bi-lexique** sans concession.

### Avantages

- **Source de vérité respectée** (C2) : pas de duplication, filtre direct sur `pack_ok`.
- **Convergence `/shop` maximale** (C3) : littéralement l’URL de la boutique, simplement paramétrée.
- **Compatibilité filtres natifs** (C6) : `search`, `attrib`, `order`, `page` coexistent sans friction (`/shop?ckr_mode=pack&search=...&order=price asc`).
- **Alignement avec la doctrine générique des portes Explorer** : on peut imaginer demain `?ckr_mode=origin&ckr_ref=<id>`, `?ckr_mode=collection&ckr_ref=<id>`. Convention transverse stable.
- **Charge CK minimale** (C4) : un contrôleur hérité, whitelist simple du paramètre.
- **Robustesse** (C7) : si `pack_ok` n’est plus peuplé, `/shop?ckr_mode=pack` renvoie une liste vide gérée nativement par le template boutique (état vide standard).

### Limites / coûts

- **URL moins canonique** (C5) : paramètre query string, moins « joli » qu’une catégorie ou qu’une route dédiée.
- **Exposition de la grille technique côté visiteur (C1)** : prise **seule**, l’Option 2 expose `pack` dans l’URL et contredit la règle de bi-lexique. C’est ce qui justifie de la considérer **combinée à l’alias `/kits`** (H1).
- **Pas de breadcrumb natif** : la sidebar catégories reste dans son état « catalogue complet » ; l’état « je suis dans la porte Kits » doit être **rendu par un titre / surtitre CK** (habillage présentationnel, cf. ADR-002).
- **Dépend d’une convention CK** (`ckr_mode`) : il faut la **documenter** clairement et tenir une **whitelist** pour éviter une interface « filtres sauvages ».

### Verdict

**Très aligné doctrinalement** (C1, C2, C3). Le coût est essentiellement cosmétique (URL, breadcrumb) et se traite par la couche présentationnelle légitime ([ADR-CKR-002](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-002)). Fort candidat.

---

## 6. Option 3 — **Route `/kits` résolue vers `/shop`**

### Mécanisme

Créer une route CK **`/kits`** (contrôleur, alignée libellé visiteur [ADR-CKR-008](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008)) qui, au choix :

- **(3a)** réutilise **directement** le rendu boutique (`website_sale.products`) avec un domaine pré-appliqué `pack_ok=True` — « `/shop` servi sous une autre URL » ;
- **(3b)** effectue une **redirection 301/302** interne vers `/shop?ckr_mode=pack` (**converge alors avec l’Option 2**) ;
- **(3c)** renvoie vers `/shop/category/<id>-kits` si une catégorie publique a été aussi matérialisée (**converge avec l’Option 1**).

Les variantes 3b et 3c ne sont pas des options autonomes : elles **présupposent** Option 2 ou Option 1. Seule la **variante 3a** est « vraiment autonome ».

### Avantages (variante 3a, autonome)

- **URL canonique dédiée** (C5) : `/kits` est lisible, parlant, partageable, SEO-friendly, alignée sur le libellé visiteur.
- **Continuité** avec le stub actuel : l’URL `/kits` existe déjà, elle gagne simplement un contenu réel (C9 : migration très légère).
- **Source de vérité respectée** (C2) : le domaine `pack_ok=True` est appliqué sans duplication.
- **Lecture porte Explorer claire** : une porte = une URL, partageable par e-mail / réseaux sociaux.

### Limites / coûts

- **Tension avec ADR-CKR-007** (C3) : `/kits` n’est **pas** `/shop`. Soit on considère que c’est une **façade lisible** sur la même logique de liste boutique (acceptable si l’implémentation réutilise **strictement** le template `website_sale.products` sans divergence), soit on commence à construire une **seconde vitrine commerciale** (disqualifié par doctrine).
- **Compatibilité filtres natifs** (C6) : pour que `/kits?search=…&order=…&page=2` fonctionne identiquement à `/shop?…`, il faut **forwarder** tous les paramètres et réutiliser le rendu standard — ce qui ajoute de la charge de maintenance à chaque montée de version (C4, C8).
- **Charge CK** (C4) plus élevée qu’Option 2 : route dédiée + contrôleur qui réexpose un rendu existant + tests de non-régression.
- **Risque de divergence** à long terme : chaque évolution de `website_sale` (tri, facettes, pagination) demandera une **vérification** explicite sur `/kits`.
- **Généralisation** : si la doctrine adopte ce pattern pour les cinq portes (`/promotions`, `/collections`, `/kits`, `/categories`, `/origines`), on multiplie les routes miroirs et la dette de synchronisation avec le template boutique.

### Verdict

**Attrayant côté visiteur** (URL lisible), **coûteux côté maintenance** (synchronisation avec le template boutique sur chaque upgrade), **en tension** avec ADR-007 si la route vit sa vie. Défendable uniquement si elle reste **strictement une façade** sur la liste boutique — autant dans ce cas la rendre explicite comme **redirection** vers l’URL canonique (variante 3b).

---

## 7. Variantes hybrides

### 7.1 Hybride **H1 = Option 2 + alias `/kits` (redirection 301)** — incarne la règle de bi-lexique

- **URL visiteur** (front, carte Explorer, partage, copy, SEO) : **`/kits`** — alignée libellé visiteur.
- **URL technique / canonique** (filtre produit, paramétrage interne) : **`/shop?ckr_mode=pack`** — alignée grille back-office (`pack_ok`).
- **Direction par défaut recommandée** : `/kits` redirige en **301** vers `/shop?ckr_mode=pack` ; `canonical` pointe sur `/shop?ckr_mode=pack`. *Variante inverse possible* (cf. §10) : `/kits` canonique, `/shop?ckr_mode=pack` alias interne.
- La carte Explorer pointe **toujours** vers `/kits` (libellé visiteur ↔ URL visible).

**Avantages** : 
- URL visible **lisible et alignée sur le libellé visiteur** (`/kits`) — la règle de bi-lexique [ADR-CKR-008](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008) est **effective**, pas seulement documentée.
- **Canonique native `/shop`** côté interne : aucun univers commercial parallèle, ADR-CKR-007 respecté sans interprétation.
- **Aucune duplication** de source de vérité : `pack_ok` reste unique marqueur (C2).
- **Charge CK faible** : un contrôleur hérité + une route alias 301.
- **Continuité** du stub `/kits` : la page stub devient une 301 (ou reste une page de passage éditoriale qui redirige), migration indolore (C9).

**Limites** : deux URLs coexistent pour le même contenu — mitigé par le `canonical` et la redirection 301 ; nécessite de documenter clairement que `ckr_mode` est une convention interne.

**Verdict** : **combine les avantages** de 2 et 3 **sans leurs défauts majeurs**, **et** matérialise proprement la règle de bi-lexique. Candidat recommandé.

### 7.2 Hybride **H2 = Option 1 + route `/kits` (redirection)**

- Catégorie publique « Kits » créée + maintenue en synchro avec `pack_ok`.
- `/kits` → redirige vers `/shop/category/<id>-kits`.

**Avantages** : URL canonique 100 % native ; sidebar catégories « Kits » visible ; respect du libellé visiteur côté URL.

**Limites** : **cumule** le coût de synchronisation de l’Option 1 **et** la complexité de la route CK, **sans** supprimer la duplication de source de vérité (C2). Moins favorable que H1.

---

## 8. Synthèse comparative

**Échelle** : `+++` très favorable, `++` favorable, `+` neutre / acceptable, `−` défavorable, `−−` très défavorable.

| Critère | Option 1 (cat. publique « Kits ») | Option 2 seule (`?ckr_mode=pack`) | Option 3a (route `/kits` autonome) | **H1** (2 + alias `/kits`) | H2 (1 + route `/kits`) |
|---------|:-:|:-:|:-:|:-:|:-:|
| C1 — Alignement doctrinal (ADR-001/007/008, bi-lexique inclus) | − | + *(expose « pack » côté URL visiteur)* | + | **+++** | − |
| C2 — Source de vérité unique | −− | +++ | +++ | +++ | −− |
| C3 — Convergence `/shop` | + | +++ | + (si façade stricte) | +++ | + |
| C4 — Charge CK | ++ (1a) / + (1b) | ++ | + | ++ | − |
| C5 — URL lisible / SEO / alignée libellé visiteur | +++ | − | +++ | +++ | +++ |
| C6 — Compatibilité filtres natifs | +++ | +++ | + (à maintenir) | +++ | +++ |
| C7 — Robustesse état vide / dépublication | ++ | +++ | ++ | +++ | ++ |
| C8 — Maintenabilité upgrade | + | +++ | − | +++ | + |
| C9 — Effort de migration depuis stub | + | + *(stub `/kits` à remplacer, vs 301 en H1)* | +++ | +++ | + |

---

## 9. Recommandation motivée

**Recommandation : Hybride H1 = Option 2 (paramètre CK) + alias redirection 301 depuis `/kits`.**

Configuration cible :

| Élément | Valeur | Grille |
|---------|--------|--------|
| **URL visiteur** (carte Explorer, partage, copy) | `/kits` | Front (Kits) |
| **Paramètre CK interne** | `ckr_mode=pack` | Back-office (Pack) |
| **URL canonique** (`rel="canonical"`, SEO) — *direction par défaut* | `/shop?ckr_mode=pack` | Back-office (technique) |
| **Direction alternative** (§10) | `/kits` canonique, `/shop?ckr_mode=pack` alias interne | Front (SEO priorisé visiteur) |
| **Filtre appliqué au domaine produit** | `("pack_ok", "=", True)` | Back-office |

Motifs :

1. **C1 — règle de bi-lexique effective** ([ADR-CKR-008](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008)) : l’URL visible est **`/kits`** (grille front), les conventions internes restent **Pack** (`ckr_mode=pack`, `pack_ok`). La règle est **matérialisée**, pas seulement documentée.
2. **C2 — source de vérité** : `pack_ok` reste le seul marqueur, aucune structure parallèle.
3. **C3 — convergence `/shop`** : l’URL technique est **littéralement** la boutique ; ADR-CKR-007 est respecté sans interprétation.
4. **C1 — doctrine ADR-001/002** : la construction CK se limite à (a) un contrôleur hérité qui interprète `ckr_mode=pack` et (b) une route alias `/kits` qui redirige — tout est **présentationnel / navigation**, conforme à ADR-CKR-002.
5. **C5 — URL** : `/kits` est lisible, partageable, et **cohérente avec le libellé visiteur** ; l’alias garantit la continuité depuis le stub actuel ; le `canonical` gère le SEO.
6. **Généralisable aux autres portes** : `ckr_mode` peut devenir la **convention transverse** pour Collections / Origines (et pour Promotions si des signaux au-delà du standard Odoo sont nécessaires). Une doctrine d’URL Explorer cohérente, capable d’accueillir d’autres cas de bi-lexique à l’avenir.
7. **Maintenabilité** : le rendu reste le template boutique standard, pas de miroir à maintenir.

**Ce qu’impliquera H1, côté dev, une fois tranché (hors de la portée du présent document)** :

- Contrôleur CK héritant `WebsiteSale` pour whitelist du paramètre + extension du domaine (`pack_ok=True` si `ckr_mode=pack`).
- Route alias `/kits` → 301 vers `/shop?ckr_mode=pack` (ou l’inverse, selon direction du `canonical` retenue).
- Habillage présentationnel : titre / surtitre visible **« Kits »** quand `ckr_mode=pack` est actif (libellé visiteur).
- `canonical` explicite, aligné sur la direction choisie.
- Convention documentée de `ckr_mode` (whitelist des valeurs : `pack`, potentiellement `origin`, `collection`…), expliquant qu’il s’agit d’une **grille interne** et non d’un vocabulaire visiteur.
- Retrait ou repositionnement du contenu stub `/kits` (la route devient une 301, pas une page éditoriale) — sauf si `/kits` est retenue comme URL canonique, auquel cas la page sert le rendu filtré.

---

## 10. Contre-argumentation et conditions pour trancher autrement

- **Si** la sidebar catégories native Odoo est considérée comme **indispensable** à l’identité de la porte Kits (c.-à-d. le visiteur doit voir « Kits » dans le panneau latéral de `/shop`), alors l’Option 1 regagne du terrain. **Contre-poids** : le coût de synchro et la tension sémantique ADR-008 restent.
- **Si** la convention CK `?ckr_mode=…` est jugée **inopportune** (ex. direction de ne pas introduire de paramètre custom, même whitelisté), alors l’Option 3a devient envisageable, à condition d’accepter le coût de maintenance du miroir de template et le cadrage strict « `/kits` = façade `/shop` ».
- **Si** le besoin SEO exige une URL 100 % canonique sans paramètre CK, alors H1 doit être **inversé** : `/kits` devient l’URL canonique et `/shop?ckr_mode=pack` l’alias interne. La logique reste la même, seule la direction du `canonical` change — avantage : alignement maximal avec le libellé visiteur ; inconvénient : on s’écarte légèrement de la forme native `/shop`.
- **Si** la règle de bi-lexique est jugée **trop contraignante côté technique** (ex. souhait de voir apparaître « kits » partout, y compris dans `ckr_mode`), alors le paramètre devient **`ckr_mode=kits`**. Conséquence : on aligne le paramètre sur la grille front, au prix d’une petite indirection de relecture côté code (`ckr_mode=kits` → filtre `pack_ok=True`). Choix de cohérence : privilégier l’une ou l’autre grille sur cet objet précis.

---

## 11. Décision attendue *(clôturée — voir §12)*

### 11.1 Choix du véhicule d’URL

- [ ] **Option 1** — Catégorie publique « Kits ». Sous-variante : [ ] 1a manuelle / [ ] 1b automatique CK.
- [ ] **Option 2 seule** — Paramètre CK uniquement, **sans** alias `/kits` visible.
- [ ] **Option 3a** — Route `/kits` autonome (façade stricte `/shop`).
- [x] **Hybride H1 (recommandé)** — Option 2 + alias `/kits` (redirection 301). Sens du canonical : [x] vers `/shop?ckr_mode=pack` *(par défaut, URL technique canonique)* / [ ] vers `/kits` *(URL visiteur canonique, alignement maximal bi-lexique côté SEO)*.
- [ ] **Hybride H2** — Option 1 + route `/kits`.
- [ ] **Autre / autre variante** : _______________

### 11.2 Choix du nom du paramètre CK *(si Option 2 ou H1 retenue)*

- [x] **`ckr_mode=pack`** *(par défaut, recommandé)* — aligné sur la **grille back-office** (`pack_ok`, module `product_pack`). Cohérent avec la règle [ADR-CKR-008](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008) qui réserve la grille Pack aux conventions internes. Visible par le visiteur uniquement si l’URL `/shop?ckr_mode=pack` est canonique (sinon masquée derrière l’alias `/kits`).
- [ ] **`ckr_mode=kits`** — aligné sur la **grille front**. Cohérent si on considère que `ckr_mode` est une *interface utilisateur* de fait (exposée dès qu’elle apparaît dans l’URL), plutôt qu’une convention purement technique.

### 11.3 Suite

Les deux points sont désormais **tranchés** (voir §12). [SPEC_SHOP_PORTES §4.3](SPEC_SHOP_PORTES.md) est alignée en conséquence ; le développement du contrôleur CK et de la redirection peut être autorisé.

---

## 12. Décision finale actée

**Date** : 2026-04-21.

**Option retenue** : **Hybride H1** — paramètre CK `ckr_mode=pack` sur `/shop` + alias `/kits` (redirection 301) — avec `canonical` vers `/shop?ckr_mode=pack`.

### 12.1 Configuration figée

| Élément | Valeur actée | Registre doctrinal | Doctrine alignée |
|---------|--------------|--------------------|-------------------|
| **URL visiteur** (carte Explorer, partage, copy marketing) | `/kits` | Front (Kits) | [ADR-CKR-008](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008) |
| **URL technique canonique** (`<link rel="canonical">`) | `/shop?ckr_mode=pack` | Back-office (Pack) | [ADR-CKR-007](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007) (forme native `/shop`) + [ADR-CKR-008](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008) |
| **Paramètre CK** | `ckr_mode=pack` | Back-office (Pack) | [ADR-CKR-001](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-001) (source de vérité native) + [ADR-CKR-008](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008) |
| **Whitelist des valeurs** `ckr_mode` (phase courante) | `{"pack"}` | Back-office | Doctrine généralisable — d’autres valeurs (`origin`, `collection`…) pourront s’ajouter à la whitelist vague par vague. |
| **Filtre domaine produit** | `("pack_ok", "=", True)` | Back-office | [ADR-CKR-001](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-001) + `product_pack` |
| **Mécanisme `/kits`** | Redirection HTTP **301** vers `/shop?ckr_mode=pack` | Transition front → technique | [ADR-CKR-007](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007) (stubs = transitoires) |
| **Sort du stub `website.page` `/kits`** | **Retiré** (ou dépublié) — la route `/kits` devient une **redirection** portée par le contrôleur CK | Nettoyage | [ADR-CKR-007](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007) |
| **Titre / surtitre rendu sur `/shop?ckr_mode=pack`** | Libellé visiteur « **Kits** » (titre de porte, breadcrumb CK) | Front (Kits) | [ADR-CKR-002](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-002) (habillage front) + [ADR-CKR-008](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008) |
| **Combinatoire native** (`search`, `attrib`, `order`, `page`) | **Préservée** — le paramètre CK vient en addition, ne remplace rien | Compatibilité standard | [ADR-CKR-001](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-001) |
| **Référence invalide / catalogue vide** | État vide **natif** `website_sale` + éventuelle note CK | Robustesse | [ADR-CKR-001](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-001) |

### 12.2 Ce que la décision **ferme**

- Le véhicule d’URL de la porte **Pack / Kits** n’est plus à rediscuter : il est **H1**.
- Le paramètre CK est **nommé** et **whitelisté** : `ckr_mode=pack`.
- La carte Explorer pointe sur **`/kits`** ; le stub CMS actuel `/kits` devient une **redirection 301** portée par le contrôleur CK (la `website.page` `/kits` sera **dépubliée** ou **retirée** lors de la vague d’implémentation, afin que la route soit exclusivement servie par le contrôleur — pas de collision CMS).
- L’URL **canonique** vue par les moteurs est **`/shop?ckr_mode=pack`** — ce qui renforce [ADR-CKR-007](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007) (pas de vitrine parallèle à `/shop`).

### 12.3 Ce que la décision **ouvre** *(à traiter lors du développement, hors du présent document)*

- **Implémentation CK** :
  - Controller héritant `WebsiteSale` (`/shop`), extension du domaine si `ckr_mode=pack`, whitelist stricte.
  - Controller alias : `@route('/kits', type='http', auth='public', website=True, sitemap=False)` → redirection **301** vers `/shop?ckr_mode=pack` (en conservant `search`, `order`, `page`, `attrib` fournis).
  - Injection du `canonical` dans le layout `/shop` quand `ckr_mode` actif.
  - Titre / surtitre de porte (libellé « Kits »), éventuel breadcrumb CK.
- **Nettoyage de l’existant** :
  - Dépublication ou retrait du `website.page` `website_page_compositions` (URL actuelle `/kits`) dans `data/website_pages_data.xml`, au moment où le contrôleur prend le relais.
  - Migration ordonnée : d’abord contrôleur en production, ensuite retrait de la page stub — pour éviter un trou de 404.
- **Mise en avant fiche produit** :
  - Décision ultérieure sur l’**affichage des `pack_line_ids`** (composants) côté fiche produit — natif `product_pack` suffisant ou CK ajoute un bloc « contenu du kit » (voir [SPEC_SHOP_PORTES §4.3](SPEC_SHOP_PORTES.md)).
- **Généralisation éventuelle** :
  - À la vague B (Origines) et C (Collections), évaluer si `ckr_mode=origin` / `ckr_mode=collection` reprennent le même pattern H1, ou si un autre véhicule est plus pertinent porte par porte. Le pattern est **disponible**, il n’est **pas imposé** aux autres portes par cette décision.

### 12.4 Critères de succès à l’implémentation

1. `/kits` répond en **301** vers `/shop?ckr_mode=pack` (et préserve `search`, `order`, `page`, `attrib` si présents).
2. `/shop?ckr_mode=pack` affiche la liste produits filtrée sur `pack_ok=True`, dans le template boutique standard, avec le **titre visiteur « Kits »** rendu par CK.
3. La balise `<link rel="canonical" href=".../shop?ckr_mode=pack">` est présente sur les deux URLs.
4. Les filtres natifs (`search`, `attrib`, `order`, `page`) se combinent sans friction avec `ckr_mode=pack`.
5. Toute valeur `ckr_mode` non whitelistée est **ignorée** (pas d’injection de domaine arbitraire) — `/shop?ckr_mode=foo` = `/shop` nu.
6. La `website.page` stub `/kits` est dépubliée ou retirée **sans** créer de 404 transitoire (déploiement ordonné).

---

## 13. Mise en service

> Vague d’implémentation ouverte et livrée le 2026-04-21 dans la version **19.0.1.1.0** du module `dorevia_ckreyol_marketplace`, suite à la validation de la configuration gelée (§12) et à l’autorisation explicite d’ouverture du chantier *« contrôleur hérité, redirection 301, filtre `pack_ok = True`, titre visiteur « Kits », retrait ordonné du stub `/kits` »*.

### 13.1 Livraisons techniques

| Brique | Fichier(s) | Rôle |
|--------|------------|------|
| Dépendance manifest | [`__manifest__.py`](../../__manifest__.py) | Ajout de `product_pack` aux `depends`. |
| Contrôleur boutique | [`controllers/website_sale_ckr.py`](../../controllers/website_sale_ckr.py) — `WebsiteSaleCKR` | Hérite `WebsiteSale` et se greffe sur les **hooks natifs d’Odoo 19** (aucune surcharge frontale de `shop()`) : `_get_search_options` → option `ckr_pack_only` ; `_get_shop_domain` → cohérence calcul min / max prix ; `_shop_get_query_url_kwargs` → préservation de `ckr_mode` sur pagination / filtres ; `_get_additional_shop_values` → variables QWeb `ckr_pack_mode` / `ckr_pack_title`. |
| Alias `/kits` | [`controllers/website_sale_ckr.py`](../../controllers/website_sale_ckr.py) — `WebsiteSaleCKRKitsAlias` | Route `/kits` → `request.redirect(..., code=301)` vers `/shop?ckr_mode=pack`, **préserve les query params entrants** (`search`, `order`, etc.). |
| Filtre produit | [`models/product_template.py`](../../models/product_template.py) | Override `ProductTemplate._search_get_detail` : ajoute `[('pack_ok', '=', True)]` au `base_domain` quand `options.ckr_pack_only`. Se place sur le **même** chemin de recherche que les facettes natives → cohérence pagination / tri / calcul min-max prix. |
| Canonical ciblé | [`models/website.py`](../../models/website.py) | Override `Website._get_canonical_url` : réinjecte `ckr_mode=pack` **uniquement** pour le couple (path = `/shop`, param = `pack`). Seule dérogation au *« canonical URLs should not have qs »* natif (`ir_http._url_localized`), strictement délimitée à cette porte. |
| Bandeau visiteur | [`views/pages/ckr_shop.xml`](../../views/pages/ckr_shop.xml) — template `ckr_shop_pack_banner` | Xpath sur `website_sale.products`, titre « Kits » + intro (éditorial), conditionné par `t-if="ckr_pack_mode"` → absent sur `/shop` nu. |
| Style | [`static/src/scss/layout/_shop.scss`](../../static/src/scss/layout/_shop.scss) | Styles dédiés `ckr-shop-pack-banner` (bandeau intégré à la charte). |
| Retrait du stub | [`data/website_pages_data.xml`](../../data/website_pages_data.xml), [`data/ckr_cleanup_kits_stub.xml`](../../data/ckr_cleanup_kits_stub.xml) | Record `website_page_compositions` retiré du data set ; fichier `views/pages/ckr_compositions.xml` **supprimé** ; nettoyage des installations existantes par `<delete>` sur recherche (`url='/kits'` et `key='...ckr_page_compositions'`) — robuste aux installations historiques. |

### 13.2 Vérification des critères de succès (§12)

Les six critères de succès énoncés en §12 ont été **tous vérifiés** sur l’instance `tenant_o7` après redémarrage du conteneur Odoo :

| # | Critère §12 | Vérification |
|---|-------------|--------------|
| 1 | `/kits` répond 301 vers `/shop?ckr_mode=pack` | ✅ `HTTP/1.1 301 MOVED PERMANENTLY` / `Location: /shop?ckr_mode=pack` |
| 2 | Paramètres `search`, `order`, `page` préservés lors de la redirection et compatibles avec la porte | ✅ `/kits?search=colombo&order=name+asc` → `Location: /shop?search=colombo&order=name+asc&ckr_mode=pack` |
| 3 | `/shop?ckr_mode=pack` rend la **liste filtrée** sur `pack_ok = True`, titre visiteur **Kits** | ✅ Sur 2 produits publiés (1 pack + 1 non-pack), seule l’offre `pack_ok=True` (« Kit colombo ») est rendue ; `<h1 class="ckr-shop-pack-banner__title">Kits</h1>` injecté au sommet de la liste. |
| 4 | `canonical` pointe sur **`/shop?ckr_mode=pack`** depuis `/kits` comme depuis `/shop?ckr_mode=pack` | ✅ `<link rel="canonical" href="http://…/shop?ckr_mode=pack"/>` sur `/shop?ckr_mode=pack` ; et `/kits` étant une redirection 301, la page rendue est `/shop?ckr_mode=pack` (donc canonical identique). Sur `/shop` nu, canonical = `/shop` (non-régression). |
| 5 | `ckr_mode` strictement whitelisté ; valeur inconnue = 404 soft / ignorée | ✅ Whitelist de fait : seul `ckr_mode=pack` est interprété (test explicite dans `_ckr_is_pack_mode`) ; toute autre valeur de `ckr_mode` tombe sur `/shop` standard sans filtre ni bandeau. |
| 6 | La `website.page` stub `/kits` est dépubliée ou retirée **sans** 404 transitoire (déploiement ordonné) | ✅ Déploiement **atomique** : le contrôleur `/kits` est enregistré avant la suppression du record (les routes de contrôleur l’emportent sur les `website.page` au routing). Vérification base : `SELECT url FROM website_page` → `/kits` absent ; `curl /kits` → 301 comme attendu. |

### 13.3 Patron réutilisable pour les portes restantes

Le chantier livré constitue un **patron éprouvé** pour les portes Explorer restantes (Collections, Origines ; et éventuellement Promotions / Catégories si elles venaient à sortir du `/shop` nu) :

1. Ajouter le paramètre CK dédié au `_get_search_options` (option `ckr_<...>_*`).
2. Consommer l’option dans `_search_get_detail` du modèle de référence.
3. Assurer la cohérence dans `_get_shop_domain` et la préservation du param dans `_shop_get_query_url_kwargs`.
4. Exposer un titre visiteur via `_get_additional_shop_values` + xpath conditionnel sur `website_sale.products`.
5. (Optionnel) Ajuster le canonical via `Website._get_canonical_url` **uniquement** si la convergence commerciale l’exige.
6. Retirer le stub CMS en même temps que la mise en service du contrôleur, via `<delete>` par recherche.

Ce patron **n’introduit aucune logique métier parallèle** et ne touche jamais au corps de `shop()` : il s’aligne strictement sur ADR-CKR-001 (standard d’abord) et ADR-CKR-002 (CK borné au front / navigation).

---

## 14. Références

- [ADR-CKR-001](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-001) — standard Odoo d’abord.
- [ADR-CKR-002](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-002) — spécifique front-end uniquement.
- [ADR-CKR-007](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007) — convergence `/shop`.
- [ADR-CKR-008](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008) — cinq portes d’exploration, libellés pluriel, règle de bi-lexique front / back-office.
- [SPEC_SHOP_PORTES.md §4.3](SPEC_SHOP_PORTES.md) — fiche porte Pack *(libellé visiteur Kits)*, source de vérité.
- Module OCA `product_pack` — branche `19.0`, installé sur `tenant_o7` : `product.template.pack_ok`, `pack_line_ids`, onglet Pack.

---

## Historique du document

| Date | Changement |
|------|------------|
| 2026-04-21 | Création — trois options (catégorie publique / paramètre CK / route `/packs`) + deux hybrides ; critères C1–C9 ; tableau comparatif ; recommandation **H1** (paramètre CK + alias `/packs` 301) ; contre-arguments ; grille de décision attendue. |
| 2026-04-21 | **Intégration de la règle de bi-lexique** [ADR-CKR-008](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008) : titre refondu (**porte Pack** *(libellé visiteur Kits)*) ; URL visible alignée sur **`/kits`** (stub, route alias, option 3a, hybrides H1/H2) ; Option 2 seule repositionnée comme exposant la grille technique côté visiteur et donc non recommandée sans alias ; H1 reformulé comme **incarnation** de la règle de bi-lexique (URL visiteur `/kits` ↔ URL technique interne `/shop?ckr_mode=pack`) ; recommandation H1 confirmée ; §11 dédoublée : 11.1 (véhicule d’URL) + 11.2 (**choix du nom du paramètre CK : `pack` aligné back-office, par défaut, ou `kits` aligné front**) ; direction du `canonical` clarifiée. |
| 2026-04-21 | **Décision actée** — §11.1 **Hybride H1** + §11.2 **`ckr_mode=pack`** validés ; `canonical` → `/shop?ckr_mode=pack` *(défaut recommandé)*. Statut du document passé à **Tranché**. Ajout du **§12 « Décision finale actée »** : tableau de configuration figée (9 entrées, chacune tracée à son ADR), ce que la décision **ferme** / **ouvre**, 6 **critères de succès** d’implémentation. Renumérotation : ancien §12 Références → §13. |
| 2026-04-21 | **Mise en service — Hybride H1 déployé** (module **19.0.1.1.0**). Ajout du **§13 « Mise en service »** : (13.1) table des livraisons techniques traçant brique → fichier → rôle ; (13.2) vérification croisée des **6 critères de succès** §12 contre les tests fonctionnels exécutés sur `tenant_o7` (tous verts) ; (13.3) synthèse d’un **patron réutilisable** pour les portes Explorer restantes. Statut général du document passé à **Tranché et déployé**. Renumérotation : ancien §13 Références → §14. |
