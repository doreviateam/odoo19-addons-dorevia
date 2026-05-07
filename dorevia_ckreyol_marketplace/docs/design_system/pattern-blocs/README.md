# CK — Pattern-blocs UX

Ce dossier regroupe les pattern-blocs validés directionnellement pour C-Kreyol.

Objectif : consolider les sections réutilisables de l’interface CK sans ouvrir une refonte globale.

Ces pattern-blocs ne sont pas des tickets de développement : ce sont des références de conception validées.

Chaque pattern-bloc décrit :
- l’intention produit ;
- la structure attendue ;
- les règles responsive ;
- les comportements UX ;
- les critères GO / NO GO ;
- les points de vigilance dev.

Ces documents servent de référence pour les tickets, les recettes et les futures évolutions de la boutique.

Ils ne créent pas de nouveau périmètre fonctionnel : ils sécurisent les patterns déjà validés.

## Doctrine projet (pattern-blocs d’abord, snippets Odoo pas en chantier prioritaire)

- Les **pattern-blocs** sont la **voie maîtresse** pour stabiliser la grammaire CK, documenter les intentions et les critères recette, et guider les évolutions **sans** lancer pour l’instant une **production** de snippets Odoo **déposables** dans l’éditeur Website.
- **Par défaut** : **pattern-bloc documenté ≠ snippet Odoo à créer** (`../README.md`, section doctrine).
- Les snippets déposables pourront être **réouverts comme option** lorsqu’un besoin métier réel les justifiera (ex. multiplication de pages composer avec les mêmes blocs). En attendant : **priorité consolidation marchande et documentaire**, pas complexité snippet prématurée.

Inventaire aligné code + vocabulaire (**Home** comme première source) : [`INVENTAIRE_HOME_PATTERN_BLOCS.md`](./INVENTAIRE_HOME_PATTERN_BLOCS.md).

Clôture de passe — cartographie principale Home : [`PV_PATTERN_BLOCS_HOME.md`](./PV_PATTERN_BLOCS_HOME.md).

Layout global (**header** 3 niveaux) : [`PATTERN_BLOC_HEADER_NAV_3_NIVEAUX.md`](./PATTERN_BLOC_HEADER_NAV_3_NIVEAUX.md).

Home — **Explorer / portes catalogue** : [`PATTERN_BLOC_HOME_EXPLORER_PORTES.md`](./PATTERN_BLOC_HOME_EXPLORER_PORTES.md).

Home — **sélection produits** (grille courte) : [`PATTERN_BLOC_HOME_SELECTION_PRODUITS.md`](./PATTERN_BLOC_HOME_SELECTION_PRODUITS.md).

Home — **newsletter** (captation douce / `mass_mailing`) : [`PATTERN_BLOC_HOME_NEWSLETTER.md`](./PATTERN_BLOC_HOME_NEWSLETTER.md).
