# CK — Design system

Ce dossier regroupe les décisions, patterns et composants UX/UI réutilisables de C-Kreyol.

Il ne remplace pas les tickets de développement : il sert de référence transversale pour stabiliser la grammaire visuelle, responsive et fonctionnelle de la boutique.

Le design system CK capitalise les patterns validés et aligne la conception, le développement et la recette sans ouvrir de nouvelle phase fonctionnelle.

Sa finalité est de réduire les régressions UI/UX en documentant un noyau commun stable et partageable.

## Convention de vocabulaire

Dans cette documentation :

- **pattern-bloc** = bloc UX/UI CK documenté comme référence de conception ;
- **snippet** = bloc technique Odoo (QWeb), potentiellement réutilisable/déposable dans l’éditeur Website.

Logique cible :

`Pattern-bloc` -> décrit la règle UX/UI CK  
`Template QWeb` -> implémente techniquement la structure  
`Snippet Odoo` -> bloc réutilisable/déposable dans l’éditeur  

## Doctrine — pattern-blocs vs snippets Odoo (2026)

- La **méthode principale** de consolidation UX/UI CK reste les **pattern-blocs** (`docs/design_system/pattern-blocs/`) : grammaire, intentions, responsive, GO / NO GO, réduction des régressions, guide pour futures pages — **sans** ouvrir pour l’instant un **chantier de production de snippets Odoo déposables** dans l’éditeur Website.
- **Par défaut** : **`pattern-bloc documenté ≠ snippet Odoo à créer`**. Un fichier `PATTERN_BLOC_*` ou un template QWeb modulaire **ne constituent pas**, seuls, une demande d’enregistrement snippet Website.
- Les **snippets Odoo déposables** restent une **option future**, à n’envisager **que si un besoin réel** apparaît (ex. composer plusieurs pages **éditoriales** dans l’éditeur avec les mêmes blocs CK, sans duplication manuelle abusive).
- **Priorité courante** : poursuivre la **consolidation du socle marchand** et **documentaire** ; éviter la **complexité technique prématurée** (snippet registry, données BO par bloc, doubles sources de vérité) tant que la valeur métier ne l’impose pas explicitement.

Voir aussi [`pattern-blocs/README.md`](pattern-blocs/README.md) et [`pattern-blocs/PV_PATTERN_BLOCS_HOME.md`](pattern-blocs/PV_PATTERN_BLOCS_HOME.md) (mention des options snippets).
