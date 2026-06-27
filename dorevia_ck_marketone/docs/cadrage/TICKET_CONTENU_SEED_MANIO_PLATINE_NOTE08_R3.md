# Ticket contenu — R3 · Seed Manio Crackers + La Platine (Note 08)

| Champ | Valeur |
| --- | --- |
| Type | Contenu MOA / seed instance |
| Réserve | R3 (+ clôture progressive R4) |
| Priorité | Moyenne |
| Bloquant | Non (démo MOA enrichie) |

## Contexte

La recette QA Note 08 a validé le **socle technique** avec seed partiel. Pour une démo MOA complète, renseigner les champs V1.1 sur les pivots recette.

## Manio Crackers (`product.template`)

| Champ | Action |
| --- | --- |
| `ck_producer_id` | Lier **La Platine** |
| `ck_badge_ids` | Ex. Guadeloupe · Producteur identifié (selon MOA) |
| `ck_ingredients` | Liste ingrédients validée MOA |
| `ck_discover_html` | (optionnel) migrer depuis `website_description` |
| `ck_packaging_label` | Ex. Sachet 100 g |

## La Platine (`res.partner`)

| Champ | Action |
| --- | --- |
| `ck_is_producer` | Cocher |
| `ck_producer_short_description` | Texte court bloc Producteur |
| `ck_producer_location_label` | Ex. Guadeloupe |
| `image_1920` | Logo / photo si disponible |

## R4 — Migration fallback

Lorsque `ck_discover_html`, composition et conservation sont renseignés :

- vider ou archiver le contenu redondant dans `website_description` ;
- vérifier absence de double affichage front.

## Critères d’acceptation

- Fiche Manio : meta avec lien producteur · badges · ancres Composition / Producteur si contenu ;
- Bloc Producteur visible avec La Platine ;
- Recette script `ck_note08_recette_qa.mjs` : `informational.metaHasProducerLink` et `producerSectionOk` à true.

## Références

- `note_08.md` · `RECETTE_QA_NOTE_08_VERDICT.md` R3/R4
