# Ticket polish — R1 · Accroche e-commerce fiche produit (Note 08)

| Champ | Valeur |
| --- | --- |
| Type | Polish BO / gouvernance contenu |
| Réserve | R1 (Note 08) |
| Priorité | Basse |
| Bloquant | Non |

## Contexte

`description_ecommerce` sert d’accroche courte zone haute. Aucune limite BO n’empêche une saisie ~300 caractères, ce qui peut alourdir la zone achat (mobile 390 px).

## Attendu

Choisir une option (MOA) :

1. **Gouvernance** — consigne éditoriale « accroche ≤ 255 caractères » dans le help BO ;
2. **Widget** — `Char` avec `size` ou validation Python légère ;
3. **CSS** — troncature visuelle avec `line-clamp` (si validé UX).

## Critères d’acceptation

- Accroche longue ne casse pas la mise en page desktop / mobile ;
- Comportement documenté pour la MOA contenu.

## Références

- `note_08.md` §8 · `RECETTE_QA_NOTE_08_VERDICT.md` R1
