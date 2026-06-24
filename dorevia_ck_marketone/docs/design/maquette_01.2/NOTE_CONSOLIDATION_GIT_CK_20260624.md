# Note de consolidation Git CK - 2026-06-24

## Objectif

Remettre le chantier public C-Kreyol dans un etat versionne, lisible et poussable, apres une sequence de travail repartie sur plusieurs branches de lots.

Le principe retenu est volontairement prudent :

- ne pas supprimer de branche locale ou distante sans arbitrage explicite ;
- ne pas appliquer automatiquement les anciens stashes ;
- creer une branche de consolidation au nom explicite ;
- separer le commit applicatif du commit documentaire et recette.

## Branche de consolidation

Branche creee depuis `feat/ck-featured-field-home` :

`codex/ck-home-shop-consolidation-20260624`

Cette branche reprend l'historique deja present sur `feat/ck-featured-field-home`, puis consolide l'etat courant du chantier Home / Shop / Header / Rayons.

## Commits de consolidation

### Commit applicatif

`63a6aad feat(ck): consolider header V22 et experience shop`

Perimetre :

- module `dorevia_ck_marketone_content` ;
- module `dorevia_ck_theme` ;
- modeles, vues, migrations, droits, hooks, JS, SCSS, polices et tests ;
- header V22, mega menus, navigation shop, page producteurs, editorialisation rayons, cartes produit et composants shop.

### Commit documentaire et recette

Le second commit porte la documentation, les tickets, les scripts de recette et les captures associees au chantier.

Perimetre attendu :

- documents de cadrage MOA / Dev ;
- rapport de retour Dev Home / Shop ;
- preuves visuelles et JSON de recette ;
- scripts Playwright / QA utiles a la reproductibilite des controles.

## Points volontairement non modifies

Les branches existantes ne sont pas supprimees dans cette passe. Certaines representent des lots deja merges ou des pistes anciennes, mais leur suppression doit rester un acte d'arbitrage, pas un effet de menage automatique.

Les stashes existants ne sont pas appliques. Ils peuvent contenir du WIP ancien, contradictoire ou hors perimetre.

Stashes identifies :

- `stash@{0}` - `feat/ck-nav1-navigation-v2`: cadrage readme wip ;
- `stash@{1}` - `feat/ck-nav1-navigation-v2`: wip unrelated ;
- `stash@{2}` - `fix/ck-home-section4-editor-select`: nav1-wip-docs-captures ;
- `stash@{3}` - `feat/ck-home-section3-featured-images`: ticket-local-wip ;
- autres stashes Marketone / GLC hors consolidation CK immediate.

## Hygiene recommandee apres push

1. Ouvrir une PR de consolidation vers `main` lorsque la recette technique et MOA est prete.
2. Comparer les branches CK historiques encore actives avec cette branche de consolidation.
3. Supprimer uniquement les branches confirmees comme mergees, obsoletes ou remplacees.
4. Examiner les stashes CK un par un, puis les supprimer seulement apres decision.
5. Repartir des nouveaux travaux Home / Shop depuis cette branche ou depuis `main` apres merge.

## Rappel produit

C-Kreyol n'est pas une marketplace generique. La base saine doit permettre de continuer a traduire, page par page, la promesse CK :

- selection ;
- origine ;
- producteur ;
- confiance ;
- achat rapide.
