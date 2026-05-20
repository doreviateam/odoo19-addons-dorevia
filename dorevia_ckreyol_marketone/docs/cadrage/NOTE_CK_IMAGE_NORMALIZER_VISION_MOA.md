# Pourquoi voulons-nous ce moteur image ? — Vision MOA

| Champ | Valeur |
|-------|--------|
| **Type** | Doctrine produit — **enjeu stratégique** du moteur CK Image Normalizer |
| **Statut** | **Validé MOA** (2026-05-20) |
| **ADR** | [ADR-033](./DECISIONS.md#adr-033--ck-image-normalizer-v1--poc-tuiles-commerce-shop) |
| **Cadrage technique** | [`NOTE_CK_IMAGE_NORMALIZER_SHOP_V1.md`](./NOTE_CK_IMAGE_NORMALIZER_SHOP_V1.md) |
| **Recette active** | `ck_shop_tile_v1.1` — image pleine, sans transparence |

---

## Enjeu

Nous voulons ce moteur parce qu’à terme, **C-Kreyol / Marketone** doit pouvoir accueillir des photos produits venant de vendeurs, producteurs ou partenaires, **sans dépendre à chaque fois d’une retouche manuelle lourde**.

L’objectif est que les vendeurs puissent un jour **déposer eux-mêmes** leurs photos produits, sans avoir à maîtriser :

- la taille exacte attendue ;
- le format optimal ;
- le cadrage ;
- le poids du fichier ;
- l’homogénéité visuelle de la grille ;
- les contraintes de rendu des tuiles `/shop`.

---

## Rôle du moteur

Le moteur doit jouer le rôle de **sas qualité média** entre la photo brute fournie par le vendeur et l’image affichée dans la boutique.

Son rôle **n’est pas** de « faire de la magie » ni de corriger n’importe quelle mauvaise source.

Son rôle **est** de **normaliser**, **contrôler**, **qualifier** et **alerter**.

---

## Vision cible

```text
un vendeur dépose une photo produit ;
le moteur prépare une version adaptée à la tuile commerce ;
le système indique si l’image est exploitable, exploitable avec réserve, à revoir, ou à redemander ;
la boutique conserve une grille propre, cohérente et premium.
```

---

## Pourquoi c’est important pour CK

Ce moteur est important parce que la **qualité visuelle de la boutique** ne doit pas dépendre uniquement de la compétence photo de chaque vendeur.

Il doit permettre de protéger la promesse CK :

- une boutique propre ;
- des produits lisibles ;
- une grille homogène ;
- une perception premium ;
- une expérience d’achat rassurante ;
- une industrialisation progressive du catalogue.

---

## Formulation courte

> Le moteur image sert à transformer des sources vendeurs hétérogènes en visuels commerce contrôlés, sans faire porter toute la charge à l’humain, et sans dégrader la qualité de la boutique.

---

## Limite apprise au pilote

Le pilote nous a aussi appris une limite importante :

> **Le moteur ne remplace pas la gouvernance source.**

Un packshot mal cadré, une scène lifestyle trop dense, ou une source non adaptée ne se résout pas par sur-ingénierie technique — ils relèvent de la **qualité source**, du **recadrage**, du **fallback** ou d’une **demande fournisseur**.

---

## Doctrine finale

Voir **[`DOCTRINE_IMAGE_V2.md`](./DOCTRINE_IMAGE_V2.md)** — validée MOA (2026-05-20).

```text
Deux images · trois décisions · validated_grid seul affiché en grille
```

---

## Phrase Dev

> L’enjeu du moteur n’est pas seulement de retraiter nos images actuelles. Il est de préparer un futur flux vendeur où des producteurs pourront déposer leurs photos sans connaître nos contraintes techniques, tout en garantissant que la grille `/shop` reste propre, homogène et premium.

---

## Référence visuelle tuile `/shop` (MOA)

**Référence comportementale** : tuile **Colombo des Antilles** — image lifestyle pleine, bord à bord dans la zone photo, sans effet « image dans l'image », sans fond transparent, sans produit flottant.

Toutes les tuiles commerce doivent converger vers ce rendu :

- `object-fit: cover` — la photo remplit la zone ;
- coins supérieurs arrondis alignés sur la carte ;
- fond conteneur discret (`#FDFCFA`) visible uniquement si la source l'exige ;
- tuiles v1.1 normalisées : crop CSS du padding baked-in pour retrouver le même effet plein cadre.

---

## Références

| Document | Lien |
|----------|------|
| Pilote 43/50 | [`RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md`](../recette/boutique/RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md) |
| Implémentation V1.5 | [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION.md`](../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION.md) |
| Retrait alpha | [`RAPPORT_RETRAIT_V12_ALPHA_EXECUTION.md`](../recette/boutique/RAPPORT_RETRAIT_V12_ALPHA_EXECUTION.md) |
