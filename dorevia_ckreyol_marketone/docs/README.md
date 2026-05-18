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

Progression Marketone (voir [`cadrage/ARCHITECTURE.md`](cadrage/ARCHITECTURE.md) §2 et [`cadrage/DECISIONS.md`](cadrage/DECISIONS.md) ADR-018) :

```text
Lots 1-5 : sécuriser le socle e-commerce
Lot 6    : portes catalogue
Lots suivants : premières couches éditoriales et connaissance
```

Garde-fous jusqu'à stabilisation du socle : pas de contenus culturels lourds dans `/shop` ; fiche produit non encyclopédique ; CTA d'achat prioritaire ; navigation complexe reportée ; possibilité éditoriale préparée sans implémentation prématurée.

## Tickets disponibles

| Lot | Ticket | Statut |
|-----|--------|--------|
| 0 | [`tickets/TICKET_MARKETONE_LOT0_CADRAGE.md`](tickets/TICKET_MARKETONE_LOT0_CADRAGE.md) | GO |
| 1 | [`tickets/TICKET_MARKETONE_LOT1_SOCLE.md`](tickets/TICKET_MARKETONE_LOT1_SOCLE.md) | GO validé |
| 2 | [`tickets/TICKET_MARKETONE_LOT2_IDENTITE_FRONT.md`](tickets/TICKET_MARKETONE_LOT2_IDENTITE_FRONT.md) | GO validé |
| 3 | [`tickets/TICKET_MARKETONE_LOT3_SHOP.md`](tickets/TICKET_MARKETONE_LOT3_SHOP.md) | Livré |
| 2.1 | [`tickets/TICKET_MARKETONE_LOT2_1_DESIGN_SYSTEM_MINIMAL.md`](tickets/TICKET_MARKETONE_LOT2_1_DESIGN_SYSTEM_MINIMAL.md) | GO avec réserves (`19.0.3.1.0`) |
| 4 | [`tickets/TICKET_MARKETONE_LOT4_PRODUCT.md`](tickets/TICKET_MARKETONE_LOT4_PRODUCT.md) | Ticket prêt — validation humaine avant exécution |

## Règle de lecture rapide

Pour comprendre le module : lire `cadrage/ARCHITECTURE.md`, puis `cadrage/CONTRACTS.md`, puis `pilotage/ROADMAP.md`.

Pour exécuter ou vérifier un lot : partir du ticket dans `tickets/`, puis utiliser `recette/ENV_REFERENCE.md` pour les commandes.
