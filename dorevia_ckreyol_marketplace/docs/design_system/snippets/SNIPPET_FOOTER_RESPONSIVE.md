# SNIPPET — FOOTER RESPONSIVE

## Intention produit

Clore la page avec un footer compact, rassurant et premium, évitant l'impression de longue liste administrative.

Le footer doit rester un repère de fin de page : marque, navigation secondaire et informations légales, sans dominer le contenu principal.

## Structure attendue

- Bloc marque en pleine largeur.
- Rubriques de navigation.
- Bas légal toujours visible et compact.

## Implémentation actuelle de référence

- Template : `views/layout/ckr_footer.xml`
- Styles : `static/src/scss/layout/_footer.scss`
- Comportement accordéon : `static/src/js/ckr_footer_fold.js`

## Règle mobile

- Toute rubrique avec plus de 2 items est repliable : accordéon / drill-down.
- Rubrique avec 1 ou 2 items : affichage direct.
- État initial court au premier affichage.
- Le bloc marque reste visible et stable en pleine largeur.
- Le bas légal reste visible, compact et secondaire.

## Règles responsive

- Mobile :
  - accordéons lisibles et tactiles ;
  - chevron discret ;
  - ouverture / fermeture claire ;
  - bas légal visible sans surcharge ;
  - hauteur globale maîtrisée.

- Desktop :
  - rendu ouvert / classique conservé ;
  - pas de dégradation de la lecture ;
  - les panneaux restent ouverts ;
  - pas d'effet accordéon desktop.

## Comportements UX

- Comportement mobile préféré : accordéon exclusif, ouvrir une rubrique referme l'autre.
- Navigation simple, sans effet application froide.
- Hiérarchie visuelle stable : marque → rubriques → légal.
- Le footer mobile doit rester court au premier affichage, tout en donnant accès aux rubriques.

## Accessibilité attendue

- Contrôles accordéon via boutons ou équivalent sémantique natif.
- `aria-expanded` synchronisé.
- Focus clavier visible.
- Zones tactiles confortables.
- Tap/clic actif sur toute la ligne de titre, pas seulement sur le chevron.

## GO / NO GO

### GO

- Footer mobile court au premier affichage.
- Rubriques accessibles et lisibles.
- Accordéon mobile compréhensible.
- Bas légal compact mais clair.
- Desktop non dégradé.

### NO GO

- Footer interminable en mobile.
- Accordéon ambigu ou difficile à manipuler.
- Trop de filets ou décoration parasite.
- Bloc marque noyé ou trop réduit.
- Comportement accordéon appliqué au desktop.

## Points de vigilance dev

- Préserver un nombre limité de séparateurs.
- Ne pas casser le rendu desktop.
- Vérifier les états accordéon sur viewport très étroit.
- Vérifier les attributs a11y : `aria-expanded`, focus visible, zone tactile.
- Vérifier que l’ouverture d’une rubrique referme proprement l’autre en mobile.
- Maintenir le footer comme un composant global : toute modification peut impacter home, shop, panier et checkout.

Ce snippet documente un pattern stabilisé ; il ne constitue pas un ticket de nouvelle fonctionnalité.
