# SNIPPET — FOOTER RESPONSIVE

## Intention produit

Clore la page avec un footer compact, rassurant et premium, évitant l'impression de longue liste administrative.

## Structure attendue

- Bloc marque en pleine largeur.
- Rubriques de navigation.
- Bas légal toujours visible et compact.

## Règle mobile

- Toute rubrique avec plus de 2 items est repliable (accordéon/drill-down).
- Rubrique avec 1 ou 2 items: affichage direct.
- État initial court au premier affichage.

## Règles responsive

- Mobile:
  - accordéons lisibles et tactiles ;
  - chevron discret ;
  - ouverture/fermeture claire ;
  - bas légal visible sans surcharge.
- Desktop:
  - rendu ouvert/classique conservé ;
  - pas de dégradation de la lecture.

## Comportements UX

- Comportement mobile préféré: accordéon exclusif (ouvrir une rubrique referme l'autre).
- Navigation simple, sans effet application froide.
- Hiérarchie visuelle stable (marque -> rubriques -> légal).

## Accessibilité attendue

- Contrôles accordéon via boutons (ou équivalent sémantique natif).
- `aria-expanded` synchronisé.
- Focus clavier visible.
- Zones tactiles confortables.

## GO / NO GO

### GO
- Footer mobile court au premier affichage.
- Rubriques accessibles et lisibles.
- Bas légal compact mais clair.

### NO GO
- Footer interminable en mobile.
- Accordéon ambigu ou difficile à manipuler.
- Trop de filets ou décoration parasite.

## Points de vigilance dev

- Préserver un nombre limité de séparateurs.
- Ne pas casser le rendu desktop.
- Vérifier les états accordéon sur viewport très étroit.
