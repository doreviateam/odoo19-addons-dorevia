# TICKET — Collection commerciale — Lot A (modèle BO + rattachement produits)

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_COLLECTION_LOT_A` |
| **Univers** | **Boutique** — catalogue / intention d’achat |
| **Type** | **Cadrage exec** — premier lot collections (BO uniquement) |
| **Statut** | **Clôturé GO MOA** — Lot A `19.0.11.0.0` (2026-05-19) |
| **Version cible module** | `19.0.11.0.0` (proposition) |
| **Base** | `ckr-marketone-01` |
| **ADR** | [**ADR-030**](../../cadrage/DECISIONS.md#adr-030--collection-commerciale-marketone) — **brouillon validé MOA** |
| **Prérequis** | Sidebar catégories C4 **GO** — `19.0.10.9.0` · taxonomie ADR-029 · mapping catégories BO |
| **Lots suivants** | **Lot B** — sidebar Collections · **Lot C** — homepage / mise en avant |

---

## Objectif Lot A

Introduire l’objet métier **`marketone.shop.collection`** et le rattachement **BO** aux produits vendables, **sans** exposition visiteur :

- **pas** de facette sidebar Collections ;
- **pas** de filtre `/shop` ;
- **pas** de porte HTTP / homepage ;
- **pas** de migration des secondaires BO vers collections (décision D1 reportée).

```text
Critère GO Lot A :
Un éditeur crée une collection publiée avec slug, dates et image,
y rattache des product.template publiés (unitaires et/ou packs),
consulte la liste en BO —
sans régression des tests existants (dont dorevia_marketone_shop_sidebar).
```

---

## Décisions MOA validées (exec)

| # | Décision | Statut |
|---|----------|--------|
| **A1** | Modèle `marketone.shop.collection` | ✅ |
| **A2** | M2M · 0..n collections par produit | ✅ |
| **A3** | Packs autorisés si `sale_ok` + `website_published` | ✅ |
| **A4** | `date_start` / `date_end` BO · sans effet public Lot A | ✅ |
| **A5** | `homepage_featured` sans effet site v1 | ✅ |
| **A6** | Version `19.0.11.0.0` | ✅ |

### Nuance publication (MOA)

- Collection **publiée** (`website_published`) ⇒ **≥ 1** produit `sale_ok` + `website_published`.
- Collection **non publiée** ⇒ peut être créée **sans produit** (préparation BO).

---

## Doctrine (ADR-030 — rappel)

| Notion | Rôle |
|--------|------|
| Catégorie principale | Classe — « ce produit est quoi ? » |
| Origine | Situe — « d’où vient-il ? » |
| Pack | Compose une offre vendable |
| **Collection commerciale** | **Propose** — intention d’achat transversale |

Une collection peut regrouper des produits **indépendamment** de principale et origine ; **unitaires** et **packs** ; être **permanente** ou **temporaire**.

Les secondaires *Incontournables*, *Apéritif créole*, *Cuisine du manioc*, *Idées cadeaux* **préfigurent** des collections mais **ne sont pas** le modèle cible. Lot 6.1 `featured` reste **transitoire**.

---

## Périmètre inclus (Lot A)

### 1. Modèle `marketone.shop.collection`

| Champ | Type | Règle |
|-------|------|--------|
| `name` | Char | Obligatoire · libellé BO / visiteur |
| `slug` | Char | Obligatoire · unique par `website_id` · format `[a-z0-9-]+` (aligné `marketone.shop.origin`) |
| `teaser` | Char / Text | Description courte (optionnelle) |
| `image` | Image | Optionnelle |
| `product_ids` | M2M `product.template` | Produits de la collection |
| `date_start` | Date | Optionnelle — début de validité |
| `date_end` | Date | Optionnelle — fin de validité |
| `website_published` | Boolean | Publié / non publié |
| `active` | Boolean | Archive technique |
| `sequence` | Integer | Ordre d’affichage BO (préparation Lots B/C) |
| `website_id` | M2one `website` | Optionnel · filtre multi-site |
| `homepage_featured` | Boolean | **Optionnel v1** — flag préparation Lot C · **sans** vue site |

**Contraintes indicatives**

- `date_end` ≥ `date_start` si les deux renseignés.
- Slug unique par site (aligné `marketone.shop.origin`).
- Domaine M2M : produits **`sale_ok`** + **`website_published`** uniquement.
- **`website_published`** sur la collection ⇒ ≥ 1 produit vendable publié (contrainte Python).

### 2. Rattachement produits

| Règle | Détail |
|-------|--------|
| Cardinalité | **M2M** collection ↔ templates — **plusieurs collections par produit** autorisées (proposition D4 pour Lot A ; pas de limite v1 sauf perf) |
| Packs | Templates avec `pack_ok=True` **autorisés** dans `product_ids` (D3 : inclusion au rattachement ; pas de résolution composants en Lot A) |
| Catégories / origines | **Aucune** contrainte : un produit garde sa taxonomie ADR-029 |

### 3. Back-office

| Élément | Détail |
|---------|--------|
| Menu | Entrée Marketone — **Collections** (ou sous-menu Boutique) |
| Vues | Liste · formulaire · recherche par nom / slug |
| Fiche produit | Onglet ou champ **Collections** (M2M inverse) — lecture / édition depuis le produit |
| Sécurité | Groupes internes : lecture / édition ; **pas** d’accès portal contributeur en Lot A |

### 4. Données & technique

| Élément | Détail |
|---------|--------|
| Fichiers probables | `models/marketone_shop_collection.py` · `views/marketone_shop_collection_views.xml` · `security/` · `__manifest__.py` |
| Tests | Tag `dorevia_marketone_collection_lot_a` — création, slug, M2M, contraintes dates, domaine produits publiés |
| Recette | `docs/recette/RECETTE_MANUELLE_COLLECTION_LOT_A.md` (à créer à l’exec) |

---

## Hors périmètre Lot A

| Exclu | Lot / arbitrage |
|-------|-----------------|
| Sidebar rubrique **Collections** | **Lot B** |
| Facette `marketone_collection` · `search_product` · C4 | **Lot B** |
| Portes HTTP · `/collections/<slug>` · SEO D6 | **Lot B** ou ticket dédié |
| Homepage · blocs mise en avant | **Lot C** |
| Coexistence `marketone_mode=featured` vs collection | **D2** — hors Lot A |
| Migration / double rattachement **secondaires** | **D1** — hors Lot A |
| Refonte Lot 6.1 Incontournables | Hors Lot A |
| Données de démo recette (peuplement collections) | Optionnel post-GO · pas bloquant |
| Savoirs · `shop_ppg` | Hors périmètre |

---

## Décisions MOA à trancher avant exec

| # | Sujet | Proposition Lot A | Décideur |
|---|--------|-------------------|----------|
| **A1** | Nom technique modèle | `marketone.shop.collection` | MOA |
| **A2** | Cardinalité produit ↔ collection | M2M · **0..n** collections par produit | MOA |
| **A3** | Packs dans collection | Rattachables si `sale_ok` + `website_published` | MOA |
| **A4** | Fenêtre temporelle | Champs `date_start` / `date_end` en BO · **pas** de filtre public Lot A | MOA |
| **A5** | `homepage_featured` | Champ booléen **sans** effet site v1 | MOA |
| **A6** | Version module | `19.0.11.0.0` | MOA |

**Reportés** (ADR-030 D1, D2, D6) : secondaires, featured, URLs publiques.

---

## Critères GO — Lot A

| ID | Critère |
|----|---------|
| G1 | CRUD collection en BO (nom, slug, teaser, image, dates, publié) |
| G2 | Rattachement M2M **≥ 1** produit publié · packs autorisés si règle A3 validée |
| G3 | Slug unique par site · validation format |
| G4 | Fiche produit : collections visibles / éditables |
| G5 | Tests auto tag `dorevia_marketone_collection_lot_a` — **0** failed |
| G6 | Non-régression `dorevia_marketone_shop_sidebar` (et smoke si lancé) |
| G7 | **Aucune** route `/shop` ni sidebar Collections modifiée |

---

## Non-régression

| Zone | Attendu |
|------|---------|
| `/shop` sidebar | Inchangée (`19.0.10.9.0`) |
| `marketone_mode=featured` / `/incontournables` | Inchangé |
| Catégories C4 | Inchangé |
| Origines porte 6.2 | Inchangé |

---

## Validation ticket (checklist)

- [x] ADR-030 validé MOA
- [x] MOA périmètre Lot A et A1–A6
- [x] Nuance publication brouillon / publié
- [x] Implémentation `19.0.11.0.0`
- [x] Tests `dorevia_marketone_collection_lot_a` + non-régression sidebar
- [ ] Recette BO MOA
- [ ] Commit dédié (hors Savoirs · hors `shop_ppg`)

---

## Références

- ADR-030 : [`DECISIONS.md`](../../cadrage/DECISIONS.md#adr-030--collection-commerciale-marketone)
- Taxonomie : [`TAXONOMIE_CATALOGUE.md`](../../cadrage/TAXONOMIE_CATALOGUE.md)
- Modèle de référence (pattern slug / site) : `marketone.shop.origin`
- Sidebar C4 : [`TICKET_MARKETONE_SHOP_SIDEBAR_FACETTES_CONTEXTUELLES.md`](./TICKET_MARKETONE_SHOP_SIDEBAR_FACETTES_CONTEXTUELLES.md) — clôturé `19.0.10.9.0`
