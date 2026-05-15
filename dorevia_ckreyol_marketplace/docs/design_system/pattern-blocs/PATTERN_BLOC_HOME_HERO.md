# PATTERN-BLOC — HOME HERO

## Intention produit

Poser immédiatement l'univers C-Kreyol : matière produit, gourmandise maîtrisée, signature premium calme, avec orientation claire vers la boutique.

Le hero doit agir comme une porte d’entrée commerciale et éditoriale : donner envie, situer l’univers, puis inviter à explorer.

## Structure attendue

- Section hero immersive avec image de fond.
- Bloc texte principal : titre + sous-titre.
- Double CTA :
  - CTA principal : `Découvrir la sélection`
  - CTA secondaire : `Explorer les origines`
- Rotateur d'arrière-plan avec 4 visuels.

## Implémentation actuelle de référence

- Template : `views/snippets/ckr_hero.xml`
- Styles : `static/src/scss/components/_hero.scss`
- Rotation visuels : `static/src/js/ckr_homepage_hero_rotator.js`
- Mesure hauteur header pour le premier écran utile : `static/src/js/ckr_header_drawer.js`

## Règles responsive

- Desktop / laptop : cadrage matière validé, zone texte lisible à gauche, CTA alignés et accessibles.
- Tablette : même logique, sans rupture de hiérarchie.
- Mobile : hero compact, cadrage recentré sur la matière produit, continuité visuelle vers la suite de homepage.

Le mobile ne doit pas transformer le hero en panneau trop haut : l’utilisateur doit percevoir rapidement que la page continue.

## Comportements UX

- Rotation de fond douce, sans effet agressif.
- CTA principal immédiatement identifiable.
- CTA secondaire plus discret que le principal, mais restant tactile et lisible.
- Lisibilité texte sécurisée par overlay et contrastes maîtrisés.
- Aucun changement de visuel ne doit rendre le texte ou le CTA secondaire fragile.

## GO / NO GO

### GO

- Hero désirable et lisible sur desktop, tablette et mobile.
- Le premier écran mobile laisse sentir la suite de page.
- CTA principal clair.
- CTA secondaire compréhensible, lisible et tactile.
- Desktop / laptop non dégradés par les optimisations mobiles.

### NO GO

- Hero trop haut en mobile.
- Cadrage dominé par le contenant au détriment du produit / matière.
- CTA secondaire fragile en contraste selon les écrans.
- Overlay trop lourd qui ternit excessivement l’image.
- Modification mobile qui casse l’équilibre desktop.

## Points de vigilance dev

- Ne pas rouvrir la structure globale du hero sans besoin fort.
- Préserver la hiérarchie CTA et l'accessibilité focus / clavier.
- Toute modification d'overlay ou de cadrage mobile doit être vérifiée sur plusieurs tailles d'écran.
- Maintenir la liste des visuels du rotateur alignée avec les assets statiques réellement livrés.
- Ne pas casser la logique de hauteur utile dépendante du header mesuré : `--ckr-header-measured`.
- Les visuels actuels servent aussi de support de développement et de validation responsive ; la sélection iconographique définitive pourra être affinée dans un lot éditorial dédié.

Ce pattern-bloc documente un pattern stabilisé ; il ne constitue pas un ticket de nouvelle fonctionnalité.
