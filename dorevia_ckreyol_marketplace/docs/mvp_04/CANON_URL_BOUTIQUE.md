# CK — Canon URL boutique (pré-ouverture)

## Objectif

Fixer une doctrine URL unique pour éviter les contradictions entre code, SEO, tickets et documentation.

## Canon retenu

### 1) Page boutique principale

- Canon: `/shop`
- Rôle: point d'entrée principal catalogue.
- Les filtres CK s'appliquent en query params (`ckr_*`) sur `/shop`.

### 2) Collections

- Canon fonctionnel: `/shop?ckr_collection=<slug>`
- Statut de `/collections/<slug>`: alias entrant accepté, redirigé vers le canon `/shop?ckr_collection=<slug>`.

### 3) Origines

- Canon fonctionnel: `/shop?ckr_origin=<slug>`
- Toute route dédiée historique doit rediriger vers ce canon.

### 4) Catégories

- Canon fonctionnel CK: `/shop?ckr_category=<slug>`
- Le chemin natif `/shop/category/<slug-categorie>` reste toléré en entrée, mais redirigé vers le canon CK.

## Règles de redirection et de cohérence

- Une intention fonctionnelle = une URL canonique publique.
- Les URL historiques/marketing restent optionnelles, mais doivent:
  - rediriger en 301 vers l'URL canonique ;
  - être documentées explicitement comme alias.
- Les docs, tickets et tests doivent référencer en priorité les URLs canoniques.

## Impacts attendus

- Réduction des ambiguïtés produit/dev.
- Alignement SEO et analytics.
- Réduction du risque de réintroduire une doctrine obsolète.

## Documents à aligner / marquer obsolètes

- `docs/mvp_01/CONTRAT_URL_COLLECTIONS.md` (sections qui parlent encore des URLs nobles `/collections/...` comme cible finale).
- `docs/mvp_01/CONTRAT_URL_ORIGINES.md` (passages orientés route dédiée vs canon `/shop`).
- `docs/mvp_01/CONTRAT_URL_CATEGORIES.md` (mentions de canon natif catégorie à harmoniser avec canon CK query param).
