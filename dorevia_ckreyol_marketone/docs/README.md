# Documentation — `dorevia_ckreyol_marketone`

Ce dossier regroupe la documentation Marketone par usage, pour éviter le dossier plat et faciliter les prochaines livraisons.

## Structure

| Dossier | Contenu | Usage |
|---------|---------|-------|
| [`cadrage/`](cadrage/) | Brief initial, architecture, contrats, décisions | Doctrine et arbitrages de référence |
| [`pilotage/`](pilotage/) | Roadmap | Suivi des lots et critères GO / NO GO |
| [`recette/`](recette/) | Recettes classées par usage | Validation MOA / technique |
| [`tickets/`](tickets/) | Tickets classés par domaine | Cadrage, exécution et clôture |
| [`annexes/`](annexes/) | Brouillons et matériaux non normatifs | Références de travail hors doctrine |

## Classement interne

| Zone | Sous-dossier | Contenu |
|------|--------------|---------|
| `recette/` | [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md) | **Point d'entrée recette `/shop`** — invariants + anti-régression |
| `recette/` | [`reference/`](recette/reference/) | Environnement, assets, commandes de base |
| `recette/` | [`lots/`](recette/lots/) | Recettes des lots socle 1-6 |
| `recette/` | [`boutique/`](recette/boutique/) | Catalogue, collections, sidebar, portes boutique |
| `recette/` | [`culture/`](recette/culture/) | Pages territoire Culture v1/v2 |
| `recette/` | [`ux/`](recette/ux/) | UX-1, UX-2, UX-3 |
| `tickets/` | [`lots/`](tickets/lots/) | Tickets chronologiques du socle |
| `tickets/` | [`boutique/`](tickets/boutique/) | Catalogue, collections, portes, sidebar |
| `tickets/` | [`culture/`](tickets/culture/) | Culture v1/v2 |
| `tickets/` | [`savoirs/`](tickets/savoirs/) | Savoirs v1 |
| `tickets/` | [`ux/`](tickets/ux/) | UX-1, UX-2, UX-3 |
| `tickets/` | [`maintenance/`](tickets/maintenance/) | Nettoyages techniques sans changement fonctionnel |
| `tickets/` | [`pilotage/`](tickets/pilotage/) | Arbitrages de trajectoire |

## Documents principaux

| Document | Role |
|----------|------|
| [`cadrage/BRIEF_INITIAL.md`](./cadrage/BRIEF_INITIAL.md) | Brief de départ du module |
| [`cadrage/ARCHITECTURE.md`](./cadrage/ARCHITECTURE.md) | Architecture cible |
| [`cadrage/CONTRACTS.md`](./cadrage/CONTRACTS.md) | Contrats fonctionnels |
| [`cadrage/DECISIONS.md`](./cadrage/DECISIONS.md) | ADR et arbitrages datés |
| [`cadrage/DECISIONS.md#adr-034--arbitrage-architecture-cadrage2-socle-odoo-natif`](./cadrage/DECISIONS.md#adr-034--arbitrage-architecture-cadrage2-socle-odoo-natif) | **ADR-034** — socle Odoo natif · Blog/Forum hors depends · reprise front |
| [`cadrage2/`](./cadrage2/) | Recadrage BO + arbitrage architecture cadrage2 |
| [`cadrage/TAXONOMIE_CATALOGUE.md`](./cadrage/TAXONOMIE_CATALOGUE.md) | Catégories e-commerce Odoo : principale + secondaires (ADR-029) |
| [`cadrage/DECISIONS.md#adr-030--collection-commerciale-marketone`](./cadrage/DECISIONS.md#adr-030--collection-commerciale-marketone) | Collection commerciale — **ADR-030 validé MOA** |
| Collections Lot A (BO) | [`tickets/TICKET_MARKETONE_COLLECTION_LOT_A.md`](./tickets/boutique/TICKET_MARKETONE_COLLECTION_LOT_A.md) | **Clôturé GO MOA** — `19.0.11.0.0` (2026-05-19) |
| — | [`recette/RECETTE_MANUELLE_COLLECTION_LOT_A.md`](./recette/boutique/RECETTE_MANUELLE_COLLECTION_LOT_A.md) | Recette BO collections Lot A — **GO MOA** |
| [`cadrage/MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md`](./cadrage/MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md) | Mapping 27 produits recette → catégories principales / secondaires |
| [`cadrage/NOTE_CK_IMAGE_NORMALIZER_SHOP_V1.md`](./cadrage/NOTE_CK_IMAGE_NORMALIZER_SHOP_V1.md) | Moteur normalisation images tuiles `/shop` V1 — **GO POC avec réserves MOA** (ADR-033) |
| CK Image Normalizer POC | [`tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_POC.md`](./tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_POC.md) | **Clôturé GO avec réserves** |
| CK Image Normalizer pilote | [`tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md`](./tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md) | **GO avec réserves** — P4 clôturé · 72 % exploitable |
| [`tickets/TICKET_MARKETONE_CATALOGUE_CATEGORIES_BO_RECETTE.md`](./tickets/boutique/TICKET_MARKETONE_CATALOGUE_CATEGORIES_BO_RECETTE.md) | Application BO catégories e-commerce (sans code) |
| [`recette/RECETTE_MANUELLE_CATALOGUE_CATEGORIES.md`](./recette/boutique/RECETTE_MANUELLE_CATALOGUE_CATEGORIES.md) | Recette manuelle catégories catalogue |
| [`pilotage/ROADMAP.md`](./pilotage/ROADMAP.md) | Roadmap par lots |
| [`recette/reference/ENV_REFERENCE.md`](./recette/reference/ENV_REFERENCE.md) | Base `ckr-marketone-01` et validation |
| **[`recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md`](./recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md)** | **Référence boutique MOA** — invariants + checklist anti-régression `/shop` |
| [`recette/reference/ASSETS_REFERENCE.md`](./recette/reference/ASSETS_REFERENCE.md) | Banque PNG marketplace (`docs/assets`) — recette BO |
| [`recette/RECETTE_MANUELLE.md`](./recette/lots/RECETTE_MANUELLE.md) | Plan de recette manuelle MOA (lots socle — **complété par la référence boutique pour `/shop`**) |
| [`recette/RECETTE_MANUELLE_LOT4.md`](./recette/lots/RECETTE_MANUELLE_LOT4.md) | **Recette manuelle Lot 4** (fiche produit) |

## Doctrine produit C-Kreyol

`CK` signifie `C-Kreyol`.

C-Kreyol est un canal e-commerce qui a vocation à proposer une offre de produits dont la particularité est d'être **produits dans des zones géographiques où l'on parle créole**. Le canal est éditorialisé autour de cette offre ; il ne doit pas être réduit à :

- un simple site de produits antillais ;
- une boutique exotique ;
- un marketplace générique ;
- un site uniquement agro-transformé.

La notion centrale est :

```text
produits issus de territoires créolophones
```

Cela inclut une logique de **territoire, de langue, de culture, de production et de transmission**.

Le site articule trois dimensions complémentaires :

| Dimension | Rôle | Priorité Marketone |
|-----------|------|--------------------|
| E-commerce | Vendre une sélection de produits issus de territoires créolophones | Socle prioritaire Lots 1-5 |
| Éditorial culturel | Raconter territoires, langues, producteurs, usages, histoires, imaginaires et savoir-faire | Après stabilisation du socle boutique |
| Partage de connaissance | Transmettre repères, recettes, vocabulaire, traditions et techniques | Lots ultérieurs, sans brouiller l'achat |

Doctrine d'agencement :

```text
Le produit d'abord.
Le récit ensuite.
Le savoir en prolongement.
```

Version courte :

```text
C-Kreyol articule trois dimensions — vendre, raconter, transmettre — sans jamais les confondre.
```

**Trois univers** (cadrage MOA 2026-05-18) : **Boutique** (acheter) · **Culture** (découvrir) · **Savoirs** (transmettre) — voir [`cadrage/NOTE_UNIVERS_CK_MARKETONE.md`](./cadrage/NOTE_UNIVERS_CK_MARKETONE.md) et ADR-024.

Progression Marketone (voir [`cadrage/ARCHITECTURE.md`](./cadrage/ARCHITECTURE.md) §2 et [`cadrage/DECISIONS.md`](./cadrage/DECISIONS.md) ADR-018) :

```text
Lots 1-5 : sécuriser le socle e-commerce
Lot 6    : portes catalogue
Lots suivants : premières couches éditoriales et connaissance
```

Garde-fous jusqu'à stabilisation du socle : pas de contenus culturels lourds dans `/shop` ; fiche produit non encyclopédique ; CTA d'achat prioritaire ; navigation complexe reportée ; possibilité éditoriale préparée sans implémentation prématurée.

### Références d'inspiration (MOA — ADR-019)

Sites de **référence d'intention** (pas de copie) :

| Site | Apport |
|------|--------|
| **750g** | Éditorial, recettes, usages, transmission de connaissance |
| **Caribshopper** | E-commerce territoires caribéens, pays, diaspora, nouveautés |

À ne pas reproduire au socle Marketone : densité média 750g, marketplace large Caribshopper. Détails : [`cadrage/ARCHITECTURE.md`](./cadrage/ARCHITECTURE.md) §2.5, [`cadrage/DECISIONS.md`](./cadrage/DECISIONS.md) ADR-019.

**Banque visuelle legacy** : packshots et moodboards dans `dorevia_ckreyol_marketplace/docs/assets/` — voir [`recette/reference/ASSETS_REFERENCE.md`](./recette/reference/ASSETS_REFERENCE.md) (ADR-020).

## Tickets disponibles

| Lot | Ticket | Statut |
|-----|--------|--------|
| 0 | [`tickets/TICKET_MARKETONE_LOT0_CADRAGE.md`](./tickets/lots/TICKET_MARKETONE_LOT0_CADRAGE.md) | GO |
| 1 | [`tickets/TICKET_MARKETONE_LOT1_SOCLE.md`](./tickets/lots/TICKET_MARKETONE_LOT1_SOCLE.md) | GO validé |
| 2 | [`tickets/TICKET_MARKETONE_LOT2_IDENTITE_FRONT.md`](./tickets/lots/TICKET_MARKETONE_LOT2_IDENTITE_FRONT.md) | GO validé |
| 3 | [`tickets/TICKET_MARKETONE_LOT3_SHOP.md`](./tickets/lots/TICKET_MARKETONE_LOT3_SHOP.md) | Livré |
| 2.1 | [`tickets/TICKET_MARKETONE_LOT2_1_DESIGN_SYSTEM_MINIMAL.md`](./tickets/lots/TICKET_MARKETONE_LOT2_1_DESIGN_SYSTEM_MINIMAL.md) | GO avec réserves (`19.0.3.1.0`) |
| 4 | [`tickets/TICKET_MARKETONE_LOT4_PRODUCT.md`](./tickets/lots/TICKET_MARKETONE_LOT4_PRODUCT.md) | GO avec réserves mineures (`19.0.4.0.0`, 2026-05-18) |
| 5 | [`tickets/TICKET_MARKETONE_LOT5_CART_CHECKOUT.md`](./tickets/lots/TICKET_MARKETONE_LOT5_CART_CHECKOUT.md) | GO (`19.0.5.0.0`, 2026-05-18) |
| 6.1 | [`tickets/TICKET_MARKETONE_LOT6_1_PORTE_INCONTOURNABLES.md`](./tickets/lots/TICKET_MARKETONE_LOT6_1_PORTE_INCONTOURNABLES.md) | Cadrage **GO avec réserves** (2026-05-18) |
| 6.1 exec | [`tickets/TICKET_MARKETONE_LOT6_1_INCONTOURNABLES_EXEC.md`](./tickets/lots/TICKET_MARKETONE_LOT6_1_INCONTOURNABLES_EXEC.md) | **GO avec réserves** (`19.0.6.0.0`, 2026-05-18) |
| 6.2 | [`tickets/TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES.md`](./tickets/lots/TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES.md) | **GO cadrage avec réserves** (2026-05-18) |
| 6.2 exec | [`tickets/TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES_EXEC.md`](./tickets/lots/TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES_EXEC.md) | **GO** (`19.0.7.0.0`, 2026-05-18) |
| — | [`tickets/TICKET_MARKETONE_CONSOLIDATION_PORTES_BOUTIQUE.md`](./tickets/boutique/TICKET_MARKETONE_CONSOLIDATION_PORTES_BOUTIQUE.md) | **GO consolidation** (2026-05-18) — référence portes Boutique |
| Culture | [`tickets/TICKET_MARKETONE_CULTURE_TERRITOIRES_CADRAGE.md`](./tickets/culture/TICKET_MARKETONE_CULTURE_TERRITOIRES_CADRAGE.md) | **GO cadrage** avec réserves légères (2026-05-18) |
| Culture exec | [`tickets/TICKET_MARKETONE_CULTURE_TERRITOIRES_EXEC.md`](./tickets/culture/TICKET_MARKETONE_CULTURE_TERRITOIRES_EXEC.md) | **Clôturé — GO MOA** `19.0.8.0.0` |
| Culture v2 cadrage | [`tickets/TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_CADRAGE.md`](./tickets/culture/TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_CADRAGE.md) | **GO cadrage avec réserves** (2026-05-18) |
| Culture v2 exec | [`tickets/TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_EXEC.md`](./tickets/culture/TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_EXEC.md) | **Clôturé — GO MOA** `19.0.9.0.0` |
| Arbitrage suite | [`tickets/TICKET_MARKETONE_ARBITRAGE_PROCHAINE_ETAPE.md`](./tickets/pilotage/TICKET_MARKETONE_ARBITRAGE_PROCHAINE_ETAPE.md) | **Clôturé GO** — Option 2 Savoirs v1 |
| Savoirs v1 cadrage | [`tickets/TICKET_MARKETONE_SAVOIRS_V1_CADRAGE.md`](./tickets/savoirs/TICKET_MARKETONE_SAVOIRS_V1_CADRAGE.md) | **GO cadrage avec réserves** (2026-05-18) |
| Savoirs v1 exec | [`tickets/TICKET_MARKETONE_SAVOIRS_V1_EXEC.md`](./tickets/savoirs/TICKET_MARKETONE_SAVOIRS_V1_EXEC.md) | **Ouvert** — en attente GO MOA (sans code) |
| Catalogue catégories BO | [`tickets/TICKET_MARKETONE_CATALOGUE_CATEGORIES_BO_RECETTE.md`](./tickets/boutique/TICKET_MARKETONE_CATALOGUE_CATEGORIES_BO_RECETTE.md) | **Clôturé GO MOA** (2026-05-19) |
| — | [`recette/RECETTE_MANUELLE_CATALOGUE_CATEGORIES.md`](./recette/boutique/RECETTE_MANUELLE_CATALOGUE_CATEGORIES.md) | Recette catégories catalogue — **GO MOA** |
| Sidebar filtres `/shop` | [`tickets/TICKET_MARKETONE_SHOP_SIDEBAR_FILTRES_CATEGORIES.md`](./tickets/boutique/TICKET_MARKETONE_SHOP_SIDEBAR_FILTRES_CATEGORIES.md) | **Clôturé GO MOA** — `19.0.10.8.0` (2026-05-19) |
| Sidebar facettes contextuelles | [`tickets/TICKET_MARKETONE_SHOP_SIDEBAR_FACETTES_CONTEXTUELLES.md`](./tickets/boutique/TICKET_MARKETONE_SHOP_SIDEBAR_FACETTES_CONTEXTUELLES.md) | **Clôturé GO MOA** — Lot 1 catégories `19.0.10.9.0` (2026-05-19) |
| — | [`recette/RECETTE_MANUELLE_LOT6_2.md`](./recette/lots/RECETTE_MANUELLE_LOT6_2.md) | Recette manuelle Lot 6.2 — GO |
| — | [`cadrage/NOTE_UNIVERS_CK_MARKETONE.md`](./cadrage/NOTE_UNIVERS_CK_MARKETONE.md) | Trois univers — **GO MOA** (ADR-024) |
| — | [`recette/RECETTE_MANUELLE_LOT6_1.md`](./recette/lots/RECETTE_MANUELLE_LOT6_1.md) | Recette manuelle Lot 6.1 — GO avec réserves |
| — | [`recette/RECETTE_MANUELLE_LOT5.md`](./recette/lots/RECETTE_MANUELLE_LOT5.md) | Recette manuelle Lot 5 |

## Règle de lecture rapide

Pour comprendre le module : lire `cadrage/ARCHITECTURE.md`, puis `cadrage/CONTRACTS.md`, puis `cadrage/NOTE_UNIVERS_CK_MARKETONE.md` (univers Boutique / Culture / Savoirs), puis `pilotage/ROADMAP.md`.

Pour exécuter ou vérifier un lot : partir du ticket dans [`tickets/`](tickets/), puis utiliser [`recette/reference/ENV_REFERENCE.md`](recette/reference/ENV_REFERENCE.md) pour les commandes.
