# Documentation — `dorevia_ckreyol_marketone`

Ce dossier regroupe la documentation Marketone par usage, pour éviter le dossier plat et faciliter les prochaines livraisons.

## Structure

| Dossier | Contenu | Usage |
|---------|---------|-------|
| [`cadrage/`](cadrage/) | Brief initial, architecture, contrats, décisions | Doctrine et arbitrages de référence |
| [`pilotage/`](pilotage/) | Roadmap | Suivi des lots et critères GO / NO GO |
| [`recette/`](recette/) | Environnement de référence | Commandes et contexte de validation |
| [`tickets/`](tickets/) | Tickets par lot | Exécution et validation des lots |

## Documents principaux

| Document | Role |
|----------|------|
| [`cadrage/BRIEF_INITIAL.md`](cadrage/BRIEF_INITIAL.md) | Brief de départ du module |
| [`cadrage/ARCHITECTURE.md`](cadrage/ARCHITECTURE.md) | Architecture cible |
| [`cadrage/CONTRACTS.md`](cadrage/CONTRACTS.md) | Contrats fonctionnels |
| [`cadrage/DECISIONS.md`](cadrage/DECISIONS.md) | ADR et arbitrages datés |
| [`pilotage/ROADMAP.md`](pilotage/ROADMAP.md) | Roadmap par lots |
| [`recette/ENV_REFERENCE.md`](recette/ENV_REFERENCE.md) | Base `ckr-marketone-01` et validation |
| [`recette/ASSETS_REFERENCE.md`](recette/ASSETS_REFERENCE.md) | Banque PNG marketplace (`docs/assets`) — recette BO |
| [`recette/RECETTE_MANUELLE.md`](recette/RECETTE_MANUELLE.md) | Plan de recette manuelle MOA (tous lots) |
| [`recette/RECETTE_MANUELLE_LOT4.md`](recette/RECETTE_MANUELLE_LOT4.md) | **Recette manuelle Lot 4** (fiche produit) |

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

**Trois univers** (cadrage MOA 2026-05-18) : **Boutique** (acheter) · **Culture** (découvrir) · **Savoirs** (transmettre) — voir [`cadrage/NOTE_UNIVERS_CK_MARKETONE.md`](cadrage/NOTE_UNIVERS_CK_MARKETONE.md) et ADR-024.

Progression Marketone (voir [`cadrage/ARCHITECTURE.md`](cadrage/ARCHITECTURE.md) §2 et [`cadrage/DECISIONS.md`](cadrage/DECISIONS.md) ADR-018) :

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

À ne pas reproduire au socle Marketone : densité média 750g, marketplace large Caribshopper. Détails : [`cadrage/ARCHITECTURE.md`](cadrage/ARCHITECTURE.md) §2.5, [`cadrage/DECISIONS.md`](cadrage/DECISIONS.md) ADR-019.

**Banque visuelle legacy** : packshots et moodboards dans `dorevia_ckreyol_marketplace/docs/assets/` — voir [`recette/ASSETS_REFERENCE.md`](recette/ASSETS_REFERENCE.md) (ADR-020).

## Tickets disponibles

| Lot | Ticket | Statut |
|-----|--------|--------|
| 0 | [`tickets/TICKET_MARKETONE_LOT0_CADRAGE.md`](tickets/TICKET_MARKETONE_LOT0_CADRAGE.md) | GO |
| 1 | [`tickets/TICKET_MARKETONE_LOT1_SOCLE.md`](tickets/TICKET_MARKETONE_LOT1_SOCLE.md) | GO validé |
| 2 | [`tickets/TICKET_MARKETONE_LOT2_IDENTITE_FRONT.md`](tickets/TICKET_MARKETONE_LOT2_IDENTITE_FRONT.md) | GO validé |
| 3 | [`tickets/TICKET_MARKETONE_LOT3_SHOP.md`](tickets/TICKET_MARKETONE_LOT3_SHOP.md) | Livré |
| 2.1 | [`tickets/TICKET_MARKETONE_LOT2_1_DESIGN_SYSTEM_MINIMAL.md`](tickets/TICKET_MARKETONE_LOT2_1_DESIGN_SYSTEM_MINIMAL.md) | GO avec réserves (`19.0.3.1.0`) |
| 4 | [`tickets/TICKET_MARKETONE_LOT4_PRODUCT.md`](tickets/TICKET_MARKETONE_LOT4_PRODUCT.md) | GO avec réserves mineures (`19.0.4.0.0`, 2026-05-18) |
| 5 | [`tickets/TICKET_MARKETONE_LOT5_CART_CHECKOUT.md`](tickets/TICKET_MARKETONE_LOT5_CART_CHECKOUT.md) | GO (`19.0.5.0.0`, 2026-05-18) |
| 6.1 | [`tickets/TICKET_MARKETONE_LOT6_1_PORTE_INCONTOURNABLES.md`](tickets/TICKET_MARKETONE_LOT6_1_PORTE_INCONTOURNABLES.md) | Cadrage **GO avec réserves** (2026-05-18) |
| 6.1 exec | [`tickets/TICKET_MARKETONE_LOT6_1_INCONTOURNABLES_EXEC.md`](tickets/TICKET_MARKETONE_LOT6_1_INCONTOURNABLES_EXEC.md) | **GO avec réserves** (`19.0.6.0.0`, 2026-05-18) |
| 6.2 | [`tickets/TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES.md`](tickets/TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES.md) | **GO cadrage avec réserves** (2026-05-18) |
| 6.2 exec | [`tickets/TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES_EXEC.md`](tickets/TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES_EXEC.md) | **GO** (`19.0.7.0.0`, 2026-05-18) |
| — | [`tickets/TICKET_MARKETONE_CONSOLIDATION_PORTES_BOUTIQUE.md`](tickets/TICKET_MARKETONE_CONSOLIDATION_PORTES_BOUTIQUE.md) | **GO consolidation** (2026-05-18) — référence portes Boutique |
| Culture | [`tickets/TICKET_MARKETONE_CULTURE_TERRITOIRES_CADRAGE.md`](tickets/TICKET_MARKETONE_CULTURE_TERRITOIRES_CADRAGE.md) | **GO cadrage** avec réserves légères (2026-05-18) |
| Culture exec | [`tickets/TICKET_MARKETONE_CULTURE_TERRITOIRES_EXEC.md`](tickets/TICKET_MARKETONE_CULTURE_TERRITOIRES_EXEC.md) | **Clôturé — GO MOA** `19.0.8.0.0` |
| Culture v2 cadrage | [`tickets/TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_CADRAGE.md`](tickets/TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_CADRAGE.md) | **GO cadrage avec réserves** (2026-05-18) |
| Culture v2 exec | [`tickets/TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_EXEC.md`](tickets/TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_EXEC.md) | **Livré** `19.0.9.0.0` — Option A (tests + recette) |
| — | [`recette/RECETTE_MANUELLE_LOT6_2.md`](recette/RECETTE_MANUELLE_LOT6_2.md) | Recette manuelle Lot 6.2 — GO |
| — | [`cadrage/NOTE_UNIVERS_CK_MARKETONE.md`](cadrage/NOTE_UNIVERS_CK_MARKETONE.md) | Trois univers — **GO MOA** (ADR-024) |
| — | [`recette/RECETTE_MANUELLE_LOT6_1.md`](recette/RECETTE_MANUELLE_LOT6_1.md) | Recette manuelle Lot 6.1 — GO avec réserves |
| — | [`recette/RECETTE_MANUELLE_LOT5.md`](recette/RECETTE_MANUELLE_LOT5.md) | Recette manuelle Lot 5 |

## Règle de lecture rapide

Pour comprendre le module : lire `cadrage/ARCHITECTURE.md`, puis `cadrage/CONTRACTS.md`, puis `cadrage/NOTE_UNIVERS_CK_MARKETONE.md` (univers Boutique / Culture / Savoirs), puis `pilotage/ROADMAP.md`.

Pour exécuter ou vérifier un lot : partir du ticket dans `tickets/`, puis utiliser `recette/ENV_REFERENCE.md` pour les commandes.
