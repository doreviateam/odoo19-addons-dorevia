# Contrat d’URL de la porte **Promotions** — analyse comparative

| Champ | Valeur |
|--------|--------|
| **Statut** | **Tranché et déployé** — six arbitrages validés le 2026-04-21 (§A, §B, paramètre CK, état vide, pré-requis ops, hook A3 ouvert mais non livré), implémentation complète livrée le même jour en 19.0.1.2.0. Voir §13 « Mise en service » ci-dessous. |
| **Date** | 2026-04-21 |
| **Périmètre** | Forme canonique de l’URL empruntée par la carte **Promotions** de la section Explorer, et **définition produit** de ce qui est servi sur `/shop` en mode promotion. |
| **Prérequis actés** | **Socle promotionnel = standard Odoo** ([SPEC_SHOP_PORTES §4.1](SPEC_SHOP_PORTES.md#41-promotions)) : listes de prix + remises / fidélité / cartes-cadeaux du build Odoo 19, pas de logique métier promo parallèle côté CK. Convergence commerciale **`/shop`** ([ADR-CKR-007](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007)). Patron technique Hybride H1 déjà **éprouvé** sur la porte Pack ([CONTRAT_URL_PACKS.md §12](CONTRAT_URL_PACKS.md)). |

Ce document **expose** les candidats pour les deux décisions, les évalue selon les **critères doctrinaux** du projet (identiques à ceux retenus pour Pack), puis formule une **recommandation motivée**. La décision finale revient à l’arbitrage produit / technique.

> **Point d’attention propre à cette porte** — contrairement à la porte Pack, qui bénéficie d’un **booléen unique** (`product_pack.pack_ok`) tranchant sans ambiguïté le statut d’un produit, **« en promotion » n’est pas un champ Odoo natif**. Le statut se **dérive** d’un ou plusieurs signaux (liste de prix datée avec remise, ribbon, programme loyalty, tag éditorial). Toute définition trop lâche fait le lit d’une porte **décorative** où les produits affichés ne sont pas ceux dont le prix est réellement réduit à la caisse ; toute définition trop restrictive fait le lit d’une porte **vide**. L’arbitrage §A doit donc précéder §B.

---

## 1. Cadre doctrinal rappelé

La décision doit respecter, dans l’ordre :

1. **Standard Odoo d’abord** ([ADR-CKR-001](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-001)) : aucune logique métier promotionnelle parallèle côté CK. Le socle promo est celui activé sur l’instance (voir §2).
2. **Convergence commerciale unique sur `/shop`** ([ADR-CKR-007](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007)) : pas d’univers commercial alternatif hors boutique native.
3. **Source de vérité alignée avec le prix réellement servi** : la liste des produits affichés en mode « promotion » doit refléter **ce que le visiteur paiera effectivement moins cher**. Une définition éditoriale déconnectée du mécanisme prix Odoo est **disqualifiée doctrinalement**, même si elle est plus simple à mettre en œuvre.
4. **Construction CK minimale et présentationnelle** ([ADR-CKR-002](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-002)) : la couche CK habille et fait le lien Explorer → `/shop` ; elle ne recompose pas la logique de remise.
5. **Capitalisation du patron technique déjà éprouvé** ([CONTRAT_URL_PACKS.md §13](CONTRAT_URL_PACKS.md)) : sauf raison forte, le **véhicule d’URL** doit réutiliser le patron Hybride H1 validé sur Pack — aucune réouverture de doctrine.

Une option qui **duplique** la source de vérité prix (CK réinvente sa notion de « promo »), qui **fragmente** le parcours (vitrine promotionnelle parallèle), ou qui **désaligne** l’affichage des prix réels est **disqualifiée par doctrine**.

---

## 2. État des lieux technique (instance `tenant_o7`, 2026-04-21)

### 2.1 Modules promotionnels installés

| Module | Rôle | Statut |
|--------|------|--------|
| **`loyalty`** | Programmes génériques (coupons, cartes-cadeaux, remises, fidélité, buy-X-get-Y, promo code…). | **Installé** |
| **`sale_loyalty`** | Intégration des programmes `loyalty` au flux vente. | **Installé** |
| **`website_sale_loyalty`** | Intégration site : application des programmes au **canal web**, saisie du code promo dans le tunnel, affichage des avantages. | **Installé** |
| **`product`** / **`website_sale`** | Listes de prix (`product.pricelist`, `product.pricelist.item`), moteur de prix e-commerce. | **Installés** |

**Synthèse** : **le socle promotionnel standard est entièrement disponible**. Il n’y a **aucun module OCA** promo installé et **aucun module à installer** en prérequis de cette porte.

### 2.2 Signaux promotionnels activables côté `product.template`

| Signal natif | Champ / modèle | Remarque |
|--------------|----------------|----------|
| **Ribbon produit** | `product.template.website_ribbon_id` → `product.ribbon` | 4 ribbons natifs présents sur l’instance : **`Sale`**, `Sold out`, `Out of stock`, `New!`. Affichage vignette sur `/shop`. |
| **Remise via liste de prix** | `product.pricelist.item` (colonnes `compute_price`, `percent_price`, `fixed_price`, `price_discount`, `date_start`, `date_end`, `pricelist_id`, `applied_on`, `product_tmpl_id` / `categ_id` / `product_id`) | **Source de vérité prix** : le moteur Odoo sert le prix de la pricelist du visiteur. C’est ce qui est **réellement facturé**. |
| **Programme loyalty type `promotion`** | `loyalty.program.program_type='promotion'` + `loyalty.rule` (éligibilité) + `loyalty.reward` (avantage) | Le **type `promotion`** est un des 8 types supportés (`coupons`, `gift_card`, `loyalty`, **`promotion`**, `ewallet`, `promo_code`, `buy_x_get_y`, `next_order_coupons`). Mécanisme standard pour promos automatiques publiques. |
| **Tag produit** | `product.tag` (Many2many avec `product.template`) | Pas de tag natif « Promo » ; à créer. Sert d’étiquette éditoriale / facette site. |

### 2.3 État peuplé de l’instance (à date)

| Objet | Nombre | Conséquence |
|-------|--------|-------------|
| `loyalty.program` actifs | **1** (*Gift Cards*, type `gift_card`) | **Aucun programme type `promotion`** en base. |
| `product.pricelist` | **0** | **Aucune liste de prix** n’existe encore (donc aucune remise datée `product.pricelist.item`). |
| `product.pricelist.item` | 0 | Voir ci-dessus. |
| `product.tag` | 0 | Aucun tag métier pour l’instant. |
| `product.ribbon` avec `classname` « sale » | 1 (`Sale`, natif Odoo) | Ribbon disponible, **pas encore affecté** à des produits. |

**Conséquence** : **quelle que soit la source de vérité retenue**, elle devra d’abord être **alimentée** (pricelist datée, programme promo, tag, ou ribbon affecté) avant que la porte n’ait un contenu visible. La porte peut être **câblée à vide** sans risque (l’état « liste vide » fait l’objet d’un cas d’arrêt documenté), mais elle ne montrera rien tant que le back-office n’aura pas alimenté la source retenue.

---

## 3. Critères d’évaluation (identiques §3 [CONTRAT_URL_PACKS](CONTRAT_URL_PACKS.md))

| # | Critère | Pondération |
|---|---------|-------------|
| C1 | **Alignement doctrinal** (ADR-001 / 007 + règle §1.3 : alignement prix affiché / prix servi) | **Élevée** |
| C2 | **Source de vérité unique** (pas de duplication avec le mécanisme prix Odoo) | **Élevée** |
| C3 | **Convergence `/shop`** (pas de silo parallèle) | **Élevée** |
| C4 | **Charge de construction CK** (routes, contrôleurs, calcul du domaine) | Moyenne |
| C5 | **URL lisible, partageable, SEO** (canonical, bookmark) | Moyenne |
| C6 | **Compatibilité filtres natifs** (`search`, `attrib`, `order`, pagination) | Moyenne |
| C7 | **Robustesse** (aucune promo active, visiteur non éligible, produit dépublié) | Moyenne |
| C8 | **Maintenabilité upgrade** (Odoo 19 → 20, évolution `sale_loyalty`) | Moyenne |
| C9 | **Effort d’alimentation back-office** (pricelist, programme, tag, ribbon…) | Faible mais à noter |

---

# PARTIE A — Source de vérité « en promotion »

## 4. Option A1 — **Ribbon produit `Sale`**

### Mécanisme
Le gestionnaire catalogue affecte **`website_ribbon_id` = ribbon *Sale*** sur les `product.template` à mettre en avant. Filtre `/shop` en mode promo = domaine `("website_ribbon_id.name", "=", "Sale")` (ou id exact).

### Évaluation
| Critère | Note | Justification |
|---------|------|---------------|
| C1 | **Faible** | Le ribbon est un **signal visuel** indépendant du prix : on peut afficher *Sale* sans remise active, ou inversement avoir un produit soldé sans ribbon. Rupture possible avec §1.3. |
| C2 | **Faible** | Source **éditoriale** parallèle au mécanisme prix. Deux sources de vérité coexistent (ribbon côté vignette + pricelist côté caisse). |
| C3 | OK | Domaine posable sur `/shop`, convergence respectée. |
| C4 | **Très faible** | Aucun code CK sur la source (le ribbon est natif) ; juste un filtre domaine. |
| C7 | Moyen | Robuste si le back-office discipline l’affectation, fragile sinon. |
| C9 | Élevé | Nécessite un **processus manuel** de synchronisation ribbon ↔ promo réelle. |

**Verdict** : **rejetée comme source principale** (C1/C2 doctrinalement bloquants). Le ribbon reste **utilisable en complément visuel** sur la vignette produit, mais pas comme définition du filtre.

---

## 5. Option A2 — **Liste de prix datée avec remise** *(recommandée)*

### Mécanisme
Un produit est considéré **« en promotion »** si, **pour la liste de prix courante du visiteur**, il existe un `product.pricelist.item` **actif** (`date_start ≤ now ≤ date_end`, bornes incluses ou ouvertes) dont le **prix calculé est inférieur** à la `list_price` de référence (ou à la pricelist parente). Le filtre `/shop` = **pré-calcul** des `product.template.id` éligibles en début de requête, puis ajout d’un domaine `("id", "in", [ids])` au `base_domain` de `_search_get_detail` (même point d’extension que Pack).

Pseudo-code côté contrôleur / model hook :

```python
def _ckr_promo_product_template_ids(self, website, pricelist):
    """Ids des product.template en promotion pour la pricelist courante.

    Source de vérité = product.pricelist.item : un item est « promo » si
    actif à l'instant t (date_start/date_end) ET produit un prix < référence.
    """
    now = fields.Datetime.now()
    domain = [
        ('pricelist_id', '=', pricelist.id),
        '|', ('date_start', '=', False), ('date_start', '<=', now),
        '|', ('date_end',   '=', False), ('date_end',   '>=', now),
        # item strictement réducteur (rejette les items neutres)
        '|', '|',
            '&', ('compute_price', '=', 'percentage'), ('percent_price', '>', 0.0),
            '&', ('compute_price', '=', 'fixed'),     ('fixed_price',   '>', 0.0),
                 ('compute_price', '=', 'formula'),
    ]
    items = self.env['product.pricelist.item'].sudo().search(domain)
    # Résolution applied_on → product_tmpl_id (avec dégradé categ / global)
    # ...
    return set_of_template_ids
```

### Évaluation
| Critère | Note | Justification |
|---------|------|---------------|
| C1 | **Élevée** | Source = **mécanisme prix Odoo**. Aligné §1.3 : un produit affiché comme « en promo » est **effectivement** réduit à la caisse pour ce visiteur. |
| C2 | **Élevée** | Unique et native : `product.pricelist.item`. Pas de duplication. |
| C3 | Élevée | Filtre posé sur `/shop` via le patron `_search_get_detail` déjà éprouvé pour Pack. |
| C4 | **Moyenne** | Un peu plus lourd que Pack (qui a un booléen direct) : il faut **résoudre la pricelist courante** et pré-calculer les ids. Pattern clair, pas complexe. |
| C5 | OK | URL = `/shop?ckr_mode=promo` (cf. §B). |
| C6 | **Élevée** | Le filtre s’ajoute au domaine natif : `search`, `attrib`, `order`, pagination continuent de fonctionner. |
| C7 | **Élevée** | Si aucune promo active → liste vide → état vide dédié. Si visiteur non connecté → pricelist par défaut du site. |
| C8 | Élevée | `product.pricelist.item` est une API très stable d’Odoo (≥ v14). |
| C9 | **Variable** | Nécessite que **le back-office crée au moins une pricelist** avec au moins un item en promotion datée pour que la porte ait du contenu. Aujourd’hui : **0 pricelist** — donc mise en service **à coordonner** avec une configuration catalogue. |

**Verdict** : **option recommandée**. Seule option qui respecte §1.3 (alignement prix affiché / prix servi) tout en restant dans le standard Odoo pur.

**Nuance — pricelists par client / B2B** : si plusieurs pricelists coexistent (visiteur public, clients B2B, etc.), le périmètre « en promo » **varie légitimement selon le visiteur** — c’est **la même logique que pour les prix servis**. Aucune anomalie : la porte Promotions reflète ce que le visiteur connecté voit effectivement. Documenter ce comportement dans le copy de l’état vide.

---

## 6. Option A3 — **Programme loyalty type `promotion`** (`sale_loyalty`)

### Mécanisme
Un produit est « en promotion » s’il est **éligible** à un `loyalty.program` actif avec `program_type='promotion'` et applicable au **canal web** (champ `website_id` / contexte site). L’éligibilité est portée par `loyalty.rule.product_domain` et `loyalty.rule.product_ids`.

### Évaluation
| Critère | Note | Justification |
|---------|------|---------------|
| C1 | **Élevée** | Mécanisme natif dédié aux promotions automatiques publiques. Aligné standard. |
| C2 | Élevée (avec nuance) | Source `loyalty.rule` — mais **indirection importante** : la règle porte un **domaine produit** et / ou une **liste explicite**, à résoudre côté Python. |
| C3 | Élevée | Domaine final posable sur `/shop`. |
| C4 | **Élevée (négative)** | **Complexe à traduire en domaine `product.template`** : il faut énumérer les programmes actifs, évaluer chaque `loyalty.rule.product_domain`, fusionner les domaines, puis pré-calculer les ids. La structure est plus riche que celle de `pricelist.item`. |
| C5 | OK | Idem A2 côté URL. |
| C6 | OK | Idem A2. |
| C7 | **Moyenne** | Programmes à **dates**, à **canaux**, à **règles conditionnelles** (min order amount, partner filter…) — certains cas visiteur-dépendants ne sont **pas** décidables en pré-calcul produit. |
| C8 | Moyenne | API `sale_loyalty` / `loyalty` a bougé récemment (v16 → v17 → v18) ; v19 stable mais vigilance upgrade. |
| C9 | Variable | Nécessite création d’au moins un programme `promotion` actif site. |

**Verdict** : **option pertinente mais trop coûteuse en coupe-temps immédiat**. À **réserver à une deuxième vague** (extension de la porte Promotions) si le back-office exprime le besoin de promos définies par **règle** (ex. *« -10 % sur tous les épices, du 1er au 15 mai »*) plutôt que par **item pricelist**. Recommandation : **documenter le hook d’extension** pour pouvoir ajouter A3 en **union** de A2 sans refactor, sans l’implémenter au premier temps.

---

## 7. Option A4 — **Tag produit « Promo »** (`product.tag`)

### Mécanisme
Création d’un `product.tag` nommé *Promo* exposé site (visible dans `website_sale_tags`). Affectation manuelle aux `product.template` concernés. Filtre `/shop` = domaine `("product_tag_ids.name", "=", "Promo")`.

### Évaluation
| Critère | Note | Justification |
|---------|------|---------------|
| C1 | **Faible** | Source **purement éditoriale** — identique critique qu’A1 : pas de lien avec le prix servi. |
| C2 | Faible | Duplication : l’info « en promo » vit dans 2 endroits (tag + pricelist / programme). |
| C3 | OK | Filtre posable. |
| C4 | Très faible | Domaine trivial. |
| C9 | Élevé | Process manuel de tagging et de détagging au fil des opérations commerciales. |

**Verdict** : **rejetée comme source principale** (mêmes griefs qu’A1). Utilisable comme **facette complémentaire** si besoin éditorial (ex. distinguer *« Promos de printemps »* de *« Déstockage »*), mais alors **elle-même alimentée** par la pricelist via un calcul planifié — ce qui revient à A2 comme source racine. **Écartée**.

---

## Synthèse §A — sources de vérité

| Option | C1 | C2 | C4 | C9 | Verdict |
|--------|----|----|----|----|---------|
| A1 — Ribbon `Sale` | Faible | Faible | Très faible | Élevé | **Rejetée** (signal visuel seulement) |
| **A2 — Pricelist datée** | **Élevée** | **Élevée** | Moyenne | Variable | **RECOMMANDÉE** |
| A3 — Programme loyalty `promotion` | Élevée | Élevée | Élevée (négatif) | Variable | Extension ultérieure en **union** avec A2 |
| A4 — Tag produit | Faible | Faible | Très faible | Élevé | **Rejetée** (source éditoriale) |

**Recommandation §A** : **A2 (pricelist datée avec remise)** comme **source principale**, avec un **hook d’extension** prévu pour ajouter **A3 (loyalty.program type `promotion`)** en **union** (sans refactor) quand le besoin se présentera. A1 reste utilisable comme **signal visuel** (ribbon sur vignette) **sans** être la source du filtre.

---

# PARTIE B — Véhicule d’URL

Les trois options demandées sont les mêmes qu’en [CONTRAT_URL_PACKS §4 à §7](CONTRAT_URL_PACKS.md) (catégorie publique, paramètre CK, route alias). L’évaluation est **structurellement identique** — je ne réouvre pas la doctrine, je **transpose** le résultat à Promotions.

## 8. Option B1 — **Catégorie publique « Promotions »**

### Mécanisme
Créer `product.public.category` *Promotions* et y rattacher manuellement les produits en promo. URL = `/shop/category/<id>-promotions`.

### Verdict
**Rejetée** — mêmes raisons que pour Pack (§4 de [CONTRAT_URL_PACKS](CONTRAT_URL_PACKS.md)) **amplifiées** pour Promotions :

- La catégorie publique **exige un rattachement** manuel à maintenir en permanence avec la source de vérité choisie §A. Pour A2, il faudrait un cron qui synchronise la catégorie avec la liste des ids « en promo active » — création d’un **mécanisme parallèle** disqualifié par doctrine §1.2 / ADR-001.
- L’URL expose « promotions » comme **catégorie** au sens taxonomie produit, ce qui est sémantiquement faux (un produit est **catégoriquement** « Épices » ou « Riz », **temporairement** en promotion).
- Rupture de convergence : la porte mène à `/shop/category/<id>-...`, pas à `/shop?...`. Légèrement moins cohérent avec le patron éprouvé.

**Rejetée.**

## 9. Option B2 — **Paramètre CK `ckr_mode=promo` sur `/shop`**

### Mécanisme
URL visiteur et technique confondues : `/shop?ckr_mode=promo`. Contrôleur hérité `WebsiteSale` interprète le paramètre et pose le domaine calculé en §A2.

### Verdict
**Admissible** — propre doctrinalement, convergence parfaite, réutilise intégralement les hooks déjà écrits pour Pack. **Faiblesse unique** : URL visiteur moins mémorisable qu’un chemin court type `/promotions`. Tolérable pour un usage interne (lien Explorer → `/shop?...`), moins pour le partage externe / bookmarks.

## 10. Option B3 — **Route `/promotions` résolue**

### Mécanisme
Route `/promotions` qui **rend directement** le template boutique (sans redirection). Le contrôleur pose le domaine et passe les mêmes variables QWeb.

### Verdict
**Rejeté** — même analyse que pour Pack (§6 de [CONTRAT_URL_PACKS](CONTRAT_URL_PACKS.md)) : deux URL rendant le **même contenu** (`/shop` et `/promotions`) créent un risque de **doublon SEO**, complexifient le canonical et démultiplient les points d’entrée à maintenir. **Disqualifié**.

## 11. Hybride **H1** — `/promotions` **301** → `/shop?ckr_mode=promo`

### Mécanisme
Identique au patron H1 éprouvé sur Pack ([CONTRAT_URL_PACKS §7](CONTRAT_URL_PACKS.md)) :

- **URL visiteur** (carte Explorer, bookmarks, partages) : **`/promotions`**.
- **Mécanisme** : contrôleur d’alias qui **redirige en HTTP 301** vers `/shop?ckr_mode=promo` en préservant les query params entrants.
- **URL technique canonique** : **`/shop?ckr_mode=promo`**.
- **`<link rel="canonical">`** : pointe sur `/shop?ckr_mode=promo`.
- **Paramètre CK whitelisté** : `ckr_mode` ∈ `{"pack", "promo"}` (extension naturelle de la whitelist Pack).
- **Filtre domaine** : ids calculés par l’algorithme §A2 (`product.pricelist.item` datées sur pricelist courante).

### Évaluation
Identique à l’analyse §7 de CONTRAT_URL_PACKS — **toutes les notes** sont transposables directement. **Bénéfice supplémentaire** propre à Promotions : **réutilisation à 100 %** du code CK déjà en place (contrôleur `WebsiteSaleCKR`, override canonical `Website._get_canonical_url`, hook `_search_get_detail` sur `product.template`) — seule la **résolution du domaine** change (pricelist au lieu de `pack_ok`).

### Verdict
**RECOMMANDÉ**. Patron doctrinalement validé, réutilise le code éprouvé, URL visiteur courte et partageable, canonical maîtrisé.

## 11 bis. Hybride **H2** — `/shop?ckr_mode=promo` direct + alias secondaire

Mêmes trade-offs qu’en [CONTRAT_URL_PACKS §8 H2](CONTRAT_URL_PACKS.md). **Non retenu** : H1 est strictement supérieur pour ce cas (URL visiteur explicite dans l’Explorer, canonical sans ambiguïté).

---

## 12. Synthèse — recommandation motivée (§A + §B)

### Ma recommandation (à valider)

| Axe | Décision recommandée | Conséquence concrète |
|-----|----------------------|----------------------|
| **§A — Source de vérité** | **A2 — Liste de prix datée avec remise** | Un produit est « en promotion » ssi, pour la pricelist courante du visiteur, il existe un `product.pricelist.item` actif (dates bornées `now`) produisant un prix strictement inférieur à la référence. Calcul en pré-résolution côté contrôleur, puis `("id", "in", ids)` au `base_domain`. |
| **§A — Extensibilité** | **Hook ouvert pour A3** (loyalty `promotion`) | Le domaine calculé pourra être **étendu en union** avec les ids issus des `loyalty.program` actifs type `promotion` dès qu’un besoin exprimé émerge, **sans refactor**. Non livré en première version. |
| **§A — Ribbon `Sale`** | Usage **visuel** uniquement | Conservé comme signal sur vignette, **indépendant** du filtre. Affectation libre au back-office (pas de contrainte de cohérence forcée par le code CK). |
| **§B — Véhicule d’URL** | **Hybride H1** (patron Pack réutilisé) | URL visiteur **`/promotions`** en **redirection HTTP 301** vers URL technique canonique **`/shop?ckr_mode=promo`**. Paramètre CK whitelisté `ckr_mode ∈ {"pack", "promo"}`. Canonical forcé sur `/shop?ckr_mode=promo` via l’override déjà en place. |
| **Titre visiteur** | **« Promotions »** | Mono-lexical (pas de règle de bi-lexique à gérer, contrairement à Kits/Pack). Bandeau `ckr_shop_promo_banner` sur le modèle de `ckr_shop_pack_banner`. |
| **État vide** | **Cas d’arrêt documenté** | Si l’algorithme A2 retourne un ensemble vide d’ids (aucune pricelist datée avec remise active), `/shop?ckr_mode=promo` affiche un **message dédié** (« Aucune offre en cours pour le moment »), pas un `/shop` nu qui donnerait l’illusion d’un catalogue intégralement promo. |
| **Stub `/promotions`** | **Aucun préexistant à retirer** | Différence avec Pack (où `/kits` existait comme `website.page` stub) : la carte Explorer Promotions pointe aujourd’hui sur `/shop` nu. Il suffit de **mettre en place `/promotions` directement via contrôleur** et de **basculer le `href` de la carte Explorer** de `/shop` vers `/promotions`. Pas de `data/ckr_cleanup_*.xml` nécessaire. |

### Pourquoi cette articulation

1. **A2 + H1** est l’unique combinaison qui tient les trois engagements doctrinaux simultanément :
   - **ADR-CKR-001 (standard d’abord)** : source = `product.pricelist.item`, mécanisme natif Odoo ; pas de notion « promo » inventée côté CK.
   - **ADR-CKR-007 (convergence `/shop`)** : URL technique unique `/shop?ckr_mode=promo`.
   - **Règle §1.3 (alignement prix affiché / prix servi)** : un produit listé est effectivement réduit à la caisse pour ce visiteur.

2. **Capitalisation maximale** : ~80 % du code écrit pour Pack est réutilisé (contrôleur hérité, override canonical, bandeau, SCSS, structure XML). Le **delta** pour Promotions est :
   - Un helper de résolution du domaine `product.pricelist.item` → `template_ids`.
   - L’extension de la whitelist `ckr_mode` (`"pack" | "promo"`).
   - Un contrôleur d’alias `/promotions` → `/shop?ckr_mode=promo` (code quasi-identique à `WebsiteSaleCKRKitsAlias`).
   - Un bandeau `ckr_shop_promo_banner` (copie-adaptation du bandeau pack, copy différent).
   - Une unité de style SCSS (ou ré-utilisation de la classe existante si la charte est alignée).

3. **Risque d’état vide transparent** : l’instance n’ayant aujourd’hui **aucune pricelist datée avec remise**, la porte affichera un état vide le jour du déploiement. C’est **cohérent avec la vérité fonctionnelle** (aucune promo en cours) et **non-bloquant** (le cas vide est prévu) ; la porte s’animera dès que le back-office créera la première pricelist promotionnelle.

---

## 13. Mise en service (2026-04-21 — module 19.0.1.2.0)

La vague d’implémentation a été **ouverte, livrée et validée fonctionnellement le jour même** des arbitrages, en réutilisant à 100 % le patron technique Hybride H1 éprouvé sur Pack (CONTRAT_URL_PACKS §13).

### 13.1 Arbitrages tranchés

| Axe | Décision | Statut |
|-----|----------|--------|
| §A source de vérité | **A2 — Pricelist datée avec remise** | **Validé** et implémenté |
| §A extensibilité A3 | **Hook ouvert, hors périmètre de cette vague** | **Validé** (commentaire de la méthode `_ckr_get_promo_template_ids` trace le point d’union) |
| §B véhicule d’URL | **H1 — `/promotions` 301 → `/shop?ckr_mode=promo`** | **Validé** et implémenté |
| Paramètre CK | **`ckr_mode=promo`** | **Validé** et implémenté |
| État vide | Message dédié **« Aucune offre en cours pour le moment »** | **Validé** et implémenté |
| Pré-requis ops | Alimentation **pricelist datée avec remise** | **Acte** comme non bloquant |

### 13.2 Livrables techniques

| Fichier | Rôle |
|---------|------|
| `controllers/website_sale_ckr.py` | Refactorisé en **multi-modes** (whitelist `{"pack", "promo"}`). Nouveau contrôleur `WebsiteSaleCKRAliases` qui porte **les deux routes d’alias** `/kits` et `/promotions` (301 vers `/shop?ckr_mode=<mode>` avec préservation des query params). |
| `models/product_pricelist.py` *(nouveau)* | Source de vérité A2 : méthode `_ckr_get_promo_template_ids(website, pricelist=None)`. Résout les `product.template.id` « en promotion » via items actifs (bornes dates) strictement réducteurs. Helpers `_ckr_active_items_domain` et `_ckr_item_is_reducer` exposés en méthodes pour override cible (ex. extension A3 ultérieure). Retourne `None` pour le cas « global promo », `set()` pour l’état vide, `set` non vide sinon. |
| `models/product_template.py` | Étendu pour consommer **aussi** l’option `ckr_promo_only` en plus de `ckr_pack_only` dans `_search_get_detail`. |
| `models/website.py` | Canonical override **multi-modes** : rétablit `ckr_mode=<value>` dans le canonical quand `/shop` est servi avec un mode CK whitelisté. |
| `views/pages/ckr_shop.xml` | Ajout du template `ckr_shop_promo_banner` (xpath sur `website_sale.products`, priorité 32). Rendu **conditionnel** sur `ckr_promo_mode` avec **bifurcation copy** via `ckr_promo_empty` : message dédié quand aucune offre active. |
| `static/src/scss/layout/_shop.scss` | Ajout de `.ckr-shop-promo-banner` + variante `.ckr-shop-promo-banner--empty` (ton atténué pour l’état vide). |
| `views/snippets/ckr_entries.xml` | Bascule du `href` de la carte Promotions de `/shop` vers **`/promotions`**. Bloc de commentaires documentaires mis à jour pour refléter l’état v19.0.1.2.0. |
| `__manifest__.py` | Version **19.0.1.1.0 → 19.0.1.2.0**, description étendue. |

**Aucun nouveau fichier `data/`** n’est nécessaire : contrairement à Kits/Pack (où `/kits` existait comme `website.page` stub à supprimer), la carte Explorer Promotions pointait sur `/shop` nu — il a suffi de basculer le `href` et d’ajouter la route contrôleur.

### 13.3 Vérification fonctionnelle (2026-04-21, `tenant_o7`)

Batterie de tests HTTP couvrant routage, rendu, filtrage et non-régression. Résumé :

| # | Scénario | Attendu | Observé | Statut |
|---|----------|---------|---------|:---:|
| 1 | `/promotions` | HTTP 301 vers `/shop?ckr_mode=promo` | ✅ | OK |
| 2 | `/promotions?search=foo&order=name%20asc` | 301 avec params préservés | `?search=foo&order=name+asc&ckr_mode=promo` | OK |
| 3 | `/kits` (non-régression Pack) | HTTP 301 vers `/shop?ckr_mode=pack` | ✅ | OK |
| 4 | `/shop?ckr_mode=promo` — HTTP | 200 | ✅ | OK |
| 5 | `/shop?ckr_mode=pack` — non-régression | 200 | ✅ | OK |
| 6 | `/shop` nu — non-régression | 200 | ✅ | OK |
| 7 | `/shop?ckr_mode=foobar` (hors whitelist) | 200 sans traitement CK | ✅ | OK |
| 8 | Bandeau `ckr-shop-promo-banner` présent en mode promo | rendu | ✅ | OK |
| 9 | Canonical `/shop?ckr_mode=promo` | `<link rel="canonical" ... ckr_mode=promo>` | ✅ | OK |
| 10 | Canonical `/shop?ckr_mode=pack` (non-régression) | inchangé | ✅ | OK |
| 11 | Canonical `/shop` nu — non-régression | sans qs | ✅ | OK |
| 12 | Canonical `/shop?ckr_mode=foobar` (hors whitelist) | sans qs (mode ignoré) | ✅ | OK |
| 13 | Carte Explorer Promotions — `href` | `/promotions` | ✅ | OK |
| 14 | Bandeau promo absent sur `/shop` nu | 0 mention | ✅ | OK |
| 15 | Bandeau pack absent sur `/shop?ckr_mode=promo` (exclusivité modes) | 0 mention | ✅ | OK |

**Test de chemin chargé** (pricelist temporaire créée puis supprimée, -20 % sur le template *Galette de manioc sucrée*) :

| Scénario | Attendu | Observé | Statut |
|----------|---------|---------|:---:|
| `/shop?ckr_mode=promo` : produit en promo apparaît | présent | 5 mentions (vignette + titre + ribbon) | OK |
| `/shop?ckr_mode=promo` : produit **hors** promo (*Kit colombo*) n’apparaît pas | 0 | 0 | OK |
| `/shop?ckr_mode=promo` : classe `--empty` absente | absente | ✅ | OK |
| `/shop` nu : tous les produits visibles | tous | Galette + Kit colombo | OK |
| `/shop?ckr_mode=pack` : *Kit colombo* présent, *Galette* absente (non-régression) | respecté | ✅ | OK |

**Tests unitaires du resolver A2** (transaction rollback) :

- ✅ Item `percentage`/`20 %` → inclus
- ✅ Item `percentage`/`0 %` (neutre) → rejeté
- ✅ Item `percentage`/`-10 %` (mark-up) → rejeté
- ✅ Cas `3_global` → retour `None` (sentinel « global promo »)
- ✅ Pricelist vide → retour `set()` (état vide)
- ✅ Paramètre `pricelist=` explicite → testabilité hors HTTP OK

### 13.4 Pré-requis ops confirmé

Le test chargé a révélé un **pré-requis supplémentaire** non anticipé dans la recommandation §12 : le groupe **`product.group_product_pricelist`** doit être activé sur l’instance. Sans ce groupe, Odoo **court-circuite toute résolution de pricelist par partenaire** (`_get_partner_pricelist_multi` ligne 351-353 du core `product/models/product_pricelist.py`), y compris `partner.property_product_pricelist`. Conséquence : les pricelists, même créées, **ne sont pas servies à la caisse**, donc la doctrine §1.3 (alignement prix affiché / prix servi) rend **cohérent** de retourner « aucune offre en cours » — c’est la vérité fonctionnelle.

Ce groupe a été **activé le 2026-04-21** sur `tenant_o7` au cours de la vérification fonctionnelle, et laissé activé : il est **logiquement impliqué** par le pré-requis ops déjà acté (« alimentation catalogue par au moins une pricelist datée avec remise » n’a de sens que si les pricelists sont effectivement consommées par le moteur de prix).

Le resolver reste **robuste** si le groupe est désactivé : il retourne proprement `set()` via la chaîne de fallback (`website._get_and_cache_current_pricelist()` court-circuité → `partner.property_product_pricelist` court-circuité → `set()`). Aucune 500, pas d’exception propagée.

### 13.5 État opérationnel au 2026-04-21 (post-livraison)

- **Instance** `tenant_o7` : feature `product.group_product_pricelist` **activé**, aucune pricelist promo configurée → la porte Promotions affiche **l’état vide dédié** (« Aucune offre en cours pour le moment »), ce qui est **cohérent avec la vérité fonctionnelle**.
- **Alimentation** : il suffira de créer côté back-office **une `product.pricelist`** attachée au website avec **au moins un `product.pricelist.item`** strictement réducteur (percentage > 0, fixed < list_price, ou formula avec price_discount > 0) et optionnellement borné en dates pour que la porte s’active côté visiteur.
- **Aucune donnée de test n’est persistée** : la pricelist créée pour la validation E2E a été supprimée après tests, l’instance est dans un état propre.

### 13.6 Patron technique — capitalisation

Cette deuxième livraison confirme le **patron Hybride H1 comme réutilisable** pour toute porte Explorer à venir :

1. **Declarer** la valeur de mode dans `CKR_MODES_ALLOWED` de `controllers/website_sale_ckr.py`.
2. **Ajouter** l’entrée dans `CKR_MODE_TITLES` et `CKR_ALIAS_MODE`.
3. **Brancher** la résolution de filtre dans les hooks `_get_search_options`, `_get_shop_domain`, `_get_additional_shop_values`.
4. **Implémenter** la source de vérité dans un modèle dédié ou des extensions ciblées (ex. `models/product_public_category.py` pour Catégories ; pour **Origines**, selon l’option retenue dans [CONTRAT_URL_ORIGINES.md](CONTRAT_URL_ORIGINES.md) §4).
5. **Ajouter** le bandeau QWeb dans `views/pages/ckr_shop.xml` (xpath `/oe_structure_website_sale_products_1` en position `before`).
6. **Ajouter** la route d’alias `@http.route("/<nouvelle-porte>")` dans `WebsiteSaleCKRAliases`.
7. **Basculer** le `href` de la carte Explorer correspondante.
8. **Tester** : routage 301, exclusivité du filtre, canonical, non-régression des autres portes.

**Variante « H1 — cible native »** (porte **Catégories**, v19.0.1.3.0 — [CONTRAT_URL_CATEGORIES.md §12](CONTRAT_URL_CATEGORIES.md)) : les étapes 1–3 et 5 (hooks + bandeau sur **`/shop?ckr_mode=…`**) **ne s’appliquent pas** ; la redirection 301 pointe vers **`/shop/category/<id>-<slug>`** (standard `website_sale`) ; pas d’extension `CKR_MODES_ALLOWED`. Les étapes **4** (résolveur sur `product.public.category`), **6** (route alias), **7** (carte Explorer), **8** (tests) restent valides *mutatis mutandis*.

Le coût marginal d’une nouvelle porte reste **faible** lorsque le standard couvre déjà le filtre (cas Catégories) ; pour **Origines** et **Collections**, la check-list complète ci-dessus s’applique en général dès qu’un **`ckr_mode`** ou un domaine CK est nécessaire.

---

## 14. Références

- [CONTRAT_URL_PACKS.md](CONTRAT_URL_PACKS.md) — patron technique Hybride H1 éprouvé (2026-04-21).
- [SPEC_SHOP_PORTES.md §4.1](SPEC_SHOP_PORTES.md#41-promotions) — cadrage initial porte Promotions (standard Odoo acté).
- [ARCHITECTURE_DECISION_RECORD.md](../direction/ARCHITECTURE_DECISION_RECORD.md) — ADR-CKR-001, 007, 008.
- Odoo 19 — [Listes de prix](https://www.odoo.com/documentation/19.0/applications/sales/sales/products_prices/prices/pricing.html), [Remises et fidélité](https://www.odoo.com/documentation/19.0/applications/sales/sales/products_prices/loyalty_discount.html).
- Code : modules installés `loyalty`, `sale_loyalty`, `website_sale_loyalty`, `product`, `website_sale` (vérifiés sur `tenant_o7`, 2026-04-21).

---

## Historique du document

| Date | Changement |
|------|------------|
| 2026-04-21 | Création — analyse comparative de la porte Promotions. Deux arbitrages structurants à trancher : §A source de vérité (4 candidats : ribbon `Sale`, pricelist datée, loyalty `promotion`, tag produit) ; §B véhicule d’URL (B1 catégorie publique rejetée, B2 paramètre seul admissible, B3 route résolue rejetée, H1 hybride recommandé par transposition du patron Pack). **Recommandation** : A2 (pricelist datée) + H1 (`/promotions` 301 → `/shop?ckr_mode=promo`). Hook A3 (loyalty) ouvert mais non livré en première version. Six cases à valider avant implémentation. |
| 2026-04-21 | **Validation des six arbitrages et livraison de l’implémentation le même jour** (module 19.0.1.2.0). §13 « Mise en service » ajoutée : livrables techniques, vérification fonctionnelle (15 tests HTTP + test chargé + 5 tests unitaires resolver), pré-requis ops confirmé (activation groupe `product.group_product_pricelist`), état opérationnel post-livraison, patron technique généralisé. Statut passé à « Tranché et déployé ». |
