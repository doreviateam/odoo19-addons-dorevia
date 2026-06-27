# Ticket polish — R1 · Accroche e-commerce fiche produit (Note 08)

| Champ | Valeur |
| --- | --- |
| Type | Polish BO / gouvernance contenu |
| Réserve | R1 (Note 08) |
| Priorité | Basse |
| Bloquant | Non |
| Statut | **Livré** (`19.0.1.54.0` content · `19.0.1.80.0` theme) |

## Contexte

`description_ecommerce` sert d’accroche courte zone haute. Aucune limite BO n’empêchait une saisie ~300 caractères, ce qui pouvait alourdir la zone achat (mobile 390 px).

## Solution retenue (combo 1 + 2 + 3)

1. **Gouvernance** — help BO « maximum 255 caractères (hors balises HTML) » ;
2. **Validation** — `@api.constrains` sur texte brut (`html2plaintext`) ≤ 255 car. ;
3. **CSS** — `line-clamp: 3` sur `.ck-product-purchase__lead` (filet visuel front).

## Critères d’acceptation

- Accroche longue ne casse pas la mise en page desktop / mobile ;
- Comportement documenté pour la MOA contenu ;
- Saisie > 255 car. refusée en BO avec message explicite.

## Références

- `note_08.md` §8 · `RECETTE_QA_NOTE_08_VERDICT.md` R1
- `models/product_template.py` · `views/product_template_views.xml`
- `dorevia_ck_theme/static/src/scss/product_page.scss`
