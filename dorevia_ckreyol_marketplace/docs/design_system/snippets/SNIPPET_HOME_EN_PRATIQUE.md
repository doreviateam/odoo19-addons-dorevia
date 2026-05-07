# SNIPPET — HOME EN PRATIQUE

## Intention produit

Transformer la réassurance homepage en module court, lisible et premium : informer sans bavardage, rassurer sans sur-promesse.

Le module doit donner des repères pratiques au visiteur sans ralentir la lecture de la home.

## Structure attendue

- Sur-titre + titre de section.
- Liste d'items de réassurance.
- Chaque item en ligne compacte :
  - icône à gauche ;
  - titre + texte à droite.

## Implémentation actuelle de référence

- Template : `views/snippets/ckr_trust.xml`
- Styles : `static/src/scss/components/_trust.scss`
- Pattern structurel clé : wrapper `ckr-trust__item__body` pour stabiliser l'alignement icône / contenu.

## Règles responsive

- Mobile-first : lignes compactes, rythme vertical maîtrisé.
- Desktop / tablette : conserver la lisibilité et l’équilibre sans surdimensionner le module.
- Séparateurs subtils entre items.
- Équilibre titre / liste soigné : pas de vide excessif, pas d'effet tassé.
- Textes courts : le module ne doit pas devenir une FAQ ou un bloc éditorial long.

## Comportements UX

- Lecture rapide au scroll.
- Hiérarchie texte claire :
  - titre d'item lisible ;
  - descriptif secondaire.
- Icônes harmonisées :
  - taille ;
  - alignement ;
  - distance au texte.
- Le bloc doit rassurer sans détourner l’utilisateur du parcours principal.

## GO / NO GO

### GO

- Bloc perçu comme module de réassurance maîtrisé.
- Bonne lisibilité mobile sans effet “liste brute”.
- Ambiance sobre, éditoriale, épicerie fine.
- Icônes et textes forment un ensemble visuel cohérent.
- Rendu desktop / tablette non dégradé.

### NO GO

- Espacements trop hauts.
- Icônes flottantes ou mal alignées.
- Effet dashboard / cartes lourdes.
- Textes trop longs ou trop explicatifs.
- Séparateurs trop visibles ou décoratifs.

## Points de vigilance dev

- Garder des séparateurs discrets.
- Éviter d'alourdir les titres au détriment du texte court.
- Vérifier le rendu sur mobiles étroits et densités d'écran variées.
- Éviter toute dérive vers des cartes épaisses : le module doit rester une liste éditoriale compacte.
- Préserver le wrapper `ckr-trust__item__body`, qui stabilise l’alignement entre icône et contenu.

Ce snippet documente un pattern stabilisé ; il ne constitue pas un ticket de nouvelle fonctionnalité.
