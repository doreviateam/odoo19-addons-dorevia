# TICKET — Consolidation portes Boutique `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_CONSOLIDATION_PORTES_BOUTIQUE` |
| **Type** | **Cadrage uniquement** — aucun code |
| **Statut** | **Clôturé — GO consolidation** (2026-05-18) — document de référence ; aucun code |
| **Version module de référence** | `19.0.7.0.0` |
| **Base** | `ckr-marketone-01` |
| **Prérequis** | Lots 1–5 **GO** ; Lot 6.1 **GO avec réserves** ; Lot 6.2 **GO** ; **ADR-024** / **NOTE_UNIVERS_CK_MARKETONE** **GO** |
| **ADR** | [ADR-024](../../cadrage/DECISIONS.md#adr-024--structuration-c-kreyol-en-trois-univers-boutique-culture-savoirs), [ADR-023](../../cadrage/DECISIONS.md#adr-023--lot-61-porte-incontournables), [ADR-025](../../cadrage/DECISIONS.md#adr-025--lot-62-porte-origines-marketone_modeorigin) |
| **Contrats** | [C3](../../cadrage/CONTRACTS.md#c3--filtres-catalogue-lot-6), [C3.A](../../cadrage/CONTRACTS.md#c3a--porte-incontournables-lot-61--figé-cadrage-2026-05-18), [C3.B](../../cadrage/CONTRACTS.md#c3b--porte-origines-lot-62--figé-cadrage-2026-05-18) |
| **Note univers** | [`NOTE_UNIVERS_CK_MARKETONE.md`](../../cadrage/NOTE_UNIVERS_CK_MARKETONE.md) |
| **Roadmap** | [`ROADMAP.md`](../../pilotage/ROADMAP.md) |

---

## Objectif

Consolider la **grammaire des portes catalogue** de l’univers **Boutique** après les Lots **6.1** (Incontournables) et **6.2** (Origines), **avant** :

- d’ouvrir une **nouvelle porte** catalogue (Promotions, Kits, Collections…) ;
- ou de lancer un **premier cadrage Culture** (récit territoire).

```text
Livrable attendu (cadrage) :
Une photographie claire et partagée de ce qui existe aujourd’hui,
des prérequis BO / exploitation, des garde-fous et de la suite recommandée.
```

**Ce ticket ne livre aucun** fichier Python, XML, SCSS, test, ni ticket d’exécution Lot 6.3.

---

## Contexte — base saine actuelle

| Jalon | Statut |
|-------|--------|
| Socle Lots 1–5 | **GO** |
| Lot 6.1 Incontournables | **GO avec réserves** (`19.0.6.0.0`) |
| Lot 6.2 Origines | **GO MOA** (`19.0.7.0.0`) |
| ADR-024 / Note Univers | **GO** — grammaire Boutique · Culture · Savoirs |

**Grammaire univers (référence)** :

```text
Boutique  — acheter
Culture   — découvrir
Savoirs   — transmettre
```

**Origines — double lecture validée** :

| Face | Univers | Statut |
|------|---------|--------|
| Filtre / porte `/shop` | Boutique | **Livré** Lot 6.2 |
| Récit territoire | Culture | **Reporté** — hors consolidation code |

---

## 1. Matrice des portes existantes (photographie MOA)

### 1.1 Tous les produits (référence — pas une « porte » au sens Lot 6)

| Élément | Valeur |
|---------|--------|
| **Libellé MOA** | Tous les produits / catalogue général |
| **URL d’entrée** | `/shop` (sans `marketone_mode`) |
| **URL canonique** | `/shop` |
| **Alias 301** | — |
| **`marketone_mode`** | *(absent)* |
| **Facettes associées** | Filtres natifs Odoo (catégories, attributs, prix, tri) — sidebar `website_sale` |
| **Source de vérité BO** | Catalogue `product.template` publié / `sale_ok` — moteur `website_sale` |
| **Config manquante** | Comportement Odoo standard |
| **Bandeau Marketone** | Titre shop standard (pas bandeau porte 6.1 / 6.2) |
| **Mobile** | Grille native ; pas de scroll horizontal involontaire (C4.4) |
| **Panier / checkout** | Tunnel inchangé — pas de paramètre porte propagé par défaut |

### 1.2 Incontournables (Lot 6.1 — C3.A)

| Élément | Valeur |
|---------|--------|
| **Libellé MOA** | Incontournables |
| **URL d’entrée** | `/incontournables` **ou** lien direct |
| **URL canonique** | `/shop?marketone_mode=featured` |
| **Alias 301** | `GET /incontournables` → **301** → canonique |
| **`marketone_mode`** | `featured` |
| **Facettes associées** | — *(filtre implicite catégorie)* |
| **Source de vérité BO** | `ir.config_parameter` `dorevia_ckreyol_marketone.featured_public_category_id` → `product.public.category` nommée **Incontournables** |
| **Prérequis exploitation** | La catégorie publique **doit** avoir `website_id` = site courant (**My Website** en recette / pré-prod). **Obligatoire** — pas une simple réserve historique : sans rattachement site → **500** sur `/shop?marketone_mode=featured` |
| **Config manquante** | Paramètre vide ou catégorie absente → domaine vide (`id = 0`) — **pas de 500** ; catégorie existante mais **sans** `website_id` site courant → **500** |
| **Présentation** | Bandeau `marketone-shop-featured-intro` ; titre + intro + lien « Tous les produits » |
| **Mobile** | Recette MOA Lot 6.1 — bandeau lisible |
| **Panier / checkout** | Non-régression validée (tests + recette) |
| **Recette** | [`RECETTE_MANUELLE_LOT6_1.md`](../../recette/lots/RECETTE_MANUELLE_LOT6_1.md) |
| **Ticket exec** | [`TICKET_MARKETONE_LOT6_1_INCONTOURNABLES_EXEC.md`](../lots/TICKET_MARKETONE_LOT6_1_INCONTOURNABLES_EXEC.md) |

### 1.3 Origines (Lot 6.2 — C3.B)

| Élément | Valeur |
|---------|--------|
| **Libellé MOA** | Origines |
| **URL d’entrée** | `/origines` **ou** lien fiche produit |
| **URL canonique (porte seule)** | `/shop?marketone_mode=origin` |
| **URL canonique (facette)** | `/shop?marketone_mode=origin&marketone_origin=<slug>` |
| **Alias 301** | `GET /origines` → **301** → `/shop?marketone_mode=origin` |
| **`marketone_mode`** | `origin` |
| **Facettes associées** | `marketone_origin=<slug>` — logique **OU** si plusieurs slugs ; **pas** `ckr_origin` |
| **Source catalogue** | Attribut produit **Origine** (multi-valeurs, sans variante) |
| **Source profil visiteur** | `marketone.shop.origin` **minimal** : slug, nom visiteur, phrase, publié, `website_id`, lien `attribute_value_id` |
| **Mode seul (sans facette)** | **Catalogue complet** + bandeau Origines |
| **Slug invalide / non publié** | **302** → `/shop` **nu** (sans paramètres porte) |
| **Présentation** | Bandeau `marketone-shop-origin-intro` ; titre « Origines » ou nom visiteur si une facette |
| **Fiche produit** | Bloc `marketone-product-origins` ; lien optionnel vers porte filtrée |
| **Culture** | **Aucun** hub territoire ni contenu long sur `/shop` |
| **Mobile** | Recette MOA Lot 6.2 — 375 px sans débordement horizontal |
| **Panier / checkout** | Non-régression validée |
| **Recette** | [`RECETTE_MANUELLE_LOT6_2.md`](../../recette/lots/RECETTE_MANUELLE_LOT6_2.md) |
| **Ticket exec** | [`TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES_EXEC.md`](../lots/TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES_EXEC.md) |

### 1.4 Règles transverses portes (déjà en vigueur)

| Règle | Référence |
|-------|-----------|
| Conteneur unique | `/shop` + paramètres — pas de page catalogue parallèle |
| Un seul `marketone_mode` actif | C3.6 — pas `featured` + `origin` |
| Priorité si plusieurs modes dans l’URL | `pack` > `promo` > `featured` > `origin` > `collection` (C3.4) — seuls `featured` et `origin` sont implémentés |
| Paramètres inconnus | Ignorés silencieusement (C3.3) |
| Hooks techniques | `_get_search_options`, `_search_get_detail`, `_get_shop_domain`, `_get_additional_shop_values` — **pas** `request._marketone_*` |
| Filtres Odoo natifs | Sidebar, tri, attributs, prix **conservés** sur toutes les portes |

---

## 2. Exploitation et prérequis BO (checklist consolidation)

### 2.1 Après `-u` module (daemon long-running)

| Action | Portes concernées |
|--------|-------------------|
| Redémarrer Odoo (conteneur / service) | `/incontournables`, `/origines` — sinon **404** sur alias (routing HTTP non rechargé) |
| Runs `--stop-after-init` | Alias OK sans redémarrage |

Référence : [`ENV_REFERENCE.md`](../../recette/reference/ENV_REFERENCE.md).

### 2.2 Checklist BO minimale (recette consolidée)

| # | Prérequis | Porte | Contrôle |
|---|-----------|-------|----------|
| B1 | Catégorie publique **Incontournables** | featured | Existe ; produits rattachés ; **`website_id` = site courant obligatoire** (My Website) — prérequis exploitation recette / pré-prod |
| B2 | Paramètre système `featured_public_category_id` | featured | Id catégorie valide |
| B3 | Attribut catalogue **Origine** | origin | Multi-valeurs ; sans variante |
| B4 | Profils `marketone.shop.origin` | origin | Slug unique par site ; **publiés** ; `website_id` site courant |
| B5 | Produits avec valeurs **Origine** | origin | Au moins 1 produit par origine testée en recette |
| B6 | Alignement slug ↔ attribut | origin | `attribute_value_id` cohérent avec produits |

### 2.3 Tests automatiques de référence

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone \
  --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_smoke,dorevia_marketone_lot2,dorevia_marketone_lot2_1,dorevia_marketone_lot3,dorevia_marketone_lot4,dorevia_marketone_lot5,dorevia_marketone_lot6_1_featured,dorevia_marketone_lot6_2_origin \
  --http-port=8071
```

**Attendu** : 76 tests post-install, **0** échec (état au GO Lot 6.2).

---

## 3. Règle d’agencement univers (à figer dans la consolidation)

| Univers | Verbe | Rapport aux portes actuelles |
|---------|-------|------------------------------|
| **Boutique** | Acheter | Incontournables + Origines = **portes** `/shop` ; tunnel panier / checkout |
| **Culture** | Découvrir | Récit territoire / producteur — **pas** sur `/shop` ; suite naturelle post-consolidation |
| **Savoirs** | Transmettre | Recettes contributives (identifié → modération BO → publication) — **hors** ce ticket |

**Pont Origines → Culture (orientation, pas implémentation)** :

```text
Aujourd’hui : lien fiche → /shop?marketone_mode=origin&marketone_origin=<slug>
Demain (Culture) : page territoire dédiée, liée depuis la porte ou la fiche — sans moteur catalogue parallèle.
```

---

## 4. Backlog portes Boutique restantes (inventaire — pas de cadrage détaillé)

| Porte | `marketone_mode` (indicatif) | Source de vérité (indicatif) | Statut |
|-------|------------------------------|--------------------------------|--------|
| Promotions | `promo` | `product.pricelist.item` réducteur | **Non implémenté** — ticket futur |
| Kits / Packs | `pack` | `pack_ok` + dépendance `product_pack` ? | **Non implémenté** — décision MOA dépendance |
| Collections éditoriales | `collection` | Modèle ou catégories — **à trancher** | **Non implémenté** |
| Catégories merchandising | — | `product.public.category` (navigation générale) | Natif Odoo — hors « porte » Lot 6.x |
| Usages / prolongements Savoirs | — | Liens depuis fiche — univers **Savoirs** | Hors portes Boutique |

**Décision consolidation** : confirmer l’**ordre indicatif** MOA pour les prochains lots **6.3+** (sans ouvrir Promotions / Kits / Collections dans ce ticket).

---

## 5. Écart vs ancienne vision C-Kreyol (mémoire — pas copie)

Référence visuelle legacy : shop riche (hero terroir, chips multi-portes, sidebar **ORIGINES**, grille merchandising dense).

| Élément legacy | Marketone actuel | Consolidation |
|----------------|-----------------|---------------|
| Hero « terroirs créoles » sur shop | Bandeau **court** par porte | **Ne pas réintroduire** sans ticket |
| Chips Toute la sélection / Kits | Une porte à la fois | Backlog Kits — pas maintenant |
| Sidebar Origines | Filtre porte + attributs natifs | Documenter complémentarité |
| Menu Promotions / Collections / Communauté | Hors scope portes livrées | Backlog + Culture / Savoirs |
| `dorevia_ckreyol_marketplace` | Lecture seule | **Interdit** copie code (C11) |

---

## 6. Garde-fous (validation MOA consolidation)

| # | Garde-fou |
|---|-----------|
| G1 | **Pas de moteur catalogue parallèle** — tout passe par `website_sale` + hooks |
| G2 | **Pas de multi-portes simultanées** sans cadrage MOA explicite |
| G3 | **Pas de chips / Explorer legacy** réintroduits sans validation |
| G4 | **Pas de refonte `/shop`** dans une consolidation documentaire |
| G5 | **Pas de Culture dans `/shop`** (hub, récit long, hero territoire) |
| G6 | **Pas de dépendance** `dorevia_ckreyol_marketplace` |
| G7 | **Pas de code** dans ce ticket |
| G8 | **Pas d’ouverture Lot 6.3** en exécution depuis ce ticket |
| G9 | Produit d’abord — panier / checkout / fiche **non régressés** |

---

## 7. Livrables cadrage (documents — pas de code)

| # | Livrable | Responsable |
|---|----------|-------------|
| L1 | Matrice §1 validée MOA | ✅ |
| L2 | Checklist exploitation §2 — `ENV_REFERENCE` | ✅ |
| L3 | Recettes 6.1 + 6.2 (pas de fiche unique) | ✅ |
| L4 | Pont Culture §3 | ✅ |
| L5 | `ROADMAP` / renvois | ✅ |
| L6 | Décision sortie §8 | ✅ **GO consolidation** |

---

## 8. Décision de sortie (MOA)

```text
[x] GO consolidation
[ ] GO consolidation avec réserves
[ ] NO GO
```

**Date** : 2026-05-18 · **Validé par** : MOA

**Points validés** : matrice `/shop`, `/incontournables` → `featured`, `/origines` → `origin` ; alias 301 ; modes et facettes ; sources BO ; exploitation ; non-régression tunnel ; ADR-024 ; legacy lecture seule ; pas de code ; pas de Lot 6.3.

**Précision MOA (Incontournables)** : `website_id` = site courant sur la catégorie publique = **prérequis d’exploitation** (recette / pré-prod), pas seulement une réserve Lot 6.1.

**Orientation de sortie validée** :

| Priorité | Suite | Statut |
|----------|--------|--------|
| **1** | **Premier cadrage Culture / Territoires** — récit Origines hors `/shop` | **À ouvrir** |
| 2 | Porte Boutique 6.3+ (Promotions, Kits, Collections…) | **Après** Culture — pas d’exécution immédiate |
| 3 | Cadrage Savoirs contributif | Plus tard |

---

## 9. Hors périmètre (explicite)

| Exclusion | Raison |
|-----------|--------|
| Code Python / XML / SCSS / tests | Ticket **cadrage uniquement** |
| Lot 6.3 Promotions / Kits / Collections — cadrage détaillé | Reporté |
| Implémentation Culture / Savoirs | Tickets univers séparés |
| Navigation home multi-portes (Explorer) | Hors consolidation sauf décision MOA |
| SEO `canonical` / `noindex` par porte | Documenter seulement — décision MOA SEO |
| Seed XML produits / profils | BO manuel recette |

---

## 10. Critères GO consolidation

- [x] Matrice §1 **complète** et validée MOA pour les 3 entrées (shop nu, featured, origin)
- [x] Règles transverses (un mode, priorité, repli origine, alias) **sans ambiguïté**
- [x] Checklist exploitation §2 **acceptée** pour sandbox et prod future
- [x] Agencement univers §3 **aligné** ADR-024
- [x] Backlog §4 **inventorié** sans détail Promotions / Kits / Collections
- [x] Garde-fous §6 **acceptés**
- [x] Orientation suite §8 **tranchée** — **Culture / Territoires** avant porte 6.3

---

## Références

| Document | Rôle |
|----------|------|
| `cadrage/DECISIONS.md` — ADR-023, ADR-024, ADR-025 | Décisions architecture |
| `cadrage/CONTRACTS.md` — C2, C3, C3.A, C3.B | Contrats URL et portes |
| `cadrage/NOTE_UNIVERS_CK_MARKETONE.md` | Trois univers ; Origines hybride |
| `pilotage/ROADMAP.md` | Lots livrés et backlog |
| `recette/reference/ENV_REFERENCE.md` | Commandes et exploitation |
| `recette/RECETTE_MANUELLE_LOT6_1.md` | Recette Incontournables |
| `recette/RECETTE_MANUELLE_LOT6_2.md` | Recette Origines |
| `dorevia_ckreyol_marketplace` | Mémoire intuitions — **lecture seule** |

---

## Prochaine étape

1. **Valider** le cadrage [`TICKET_MARKETONE_CULTURE_TERRITOIRES_CADRAGE.md`](../culture/TICKET_MARKETONE_CULTURE_TERRITOIRES_CADRAGE.md) — pas de code.
2. **Ne pas** lancer Lot 6.3 (Promotions / Kits / Collections) en exécution sans décision MOA contraire.
3. **Référence** : ce document reste la **photographie** des portes Boutique (`19.0.7.0.0`).
