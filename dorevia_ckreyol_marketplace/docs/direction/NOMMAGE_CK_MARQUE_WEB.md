# Note marque — Nommage C-Kreyol / C-Kréyòl

## Décision

Deux formes sont maintenues, avec des usages distincts :

```text
C-Kreyol  = version web / pratique / ASCII
C-Kréyòl  = version marque / culturelle / éditoriale
```

## Usage attendu

### 1) Version marque

Utiliser `C-Kréyòl` pour :

- logo ;
- supports éditoriaux ;
- titres et éléments visuels de marque ;
- contenus où l'identité culturelle est assumée.

Le logo est donc traité comme une stylisation SVG de `C-Kréyòl`.

### 2) Version web / technique

Conserver `C-Kreyol` pour :

- URLs ;
- slugs ;
- fichiers ;
- code et variables ;
- identifiants techniques sans accents.

## Garde-fous

- Ne pas introduire d'accents dans routes, slugs ou noms de fichiers.
- Vérifier que la police utilisée dans le logo SVG rend correctement `é` et `ò`.
- Conserver un fallback de police lisible pour le mot-symbole.
- Ne pas remplacer automatiquement toutes les occurrences techniques de `C-Kreyol`.

## Application immédiate

- Nom affiché du logo header : `C-Kréyòl`.
- Nommages techniques (module, chemins, ids, routes) : `C-Kreyol`.

## Synthèse

```text
Nom affiché / logo / éditorial : C-Kréyòl
Nom technique / web / code : C-Kreyol
```
