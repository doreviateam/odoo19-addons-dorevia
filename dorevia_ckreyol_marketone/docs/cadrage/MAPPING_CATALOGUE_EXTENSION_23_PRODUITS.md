# Extension catalogue — 23 produits (27 → 50 SKU)

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-05-20 |
| **Base** | `ckr-marketone-01` |
| **Ticket pilote** | [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA`](../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md) |
| **Script seed** | [`scripts/seed_catalogue_extension_23.py`](../scripts/seed_catalogue_extension_23.py) |
| **Statut** | **Appliqué BO** — 50 produits vendables publiés avec image |

---

## Objectif

Combler l’écart **23 SKU** pour atteindre **50 produits** (pilote média catalogue), en respectant ADR-029 (1–4 catégories e-commerce · origine indépendante).

---

## Synthèse

| Métrique | Avant | Après |
|----------|------:|------:|
| Produits vendables publiés | 27 | **50** |
| Avec `image_1920` | 27 | **50** |
| Codes internes | — | `CK-MO-028` … `CK-MO-050` |

Images initiales : banque `dorevia_ckreyol_marketplace/docs/assets/` (recette BO — à remplacer par visuels fournisseur si besoin).

---

## Table des 23 produits ajoutés

| Réf | Produit | Principale | Origine | URL |
|-----|---------|------------|---------|-----|
| CK-MO-028 | Sauce scotch bonnet créole | Sauces | Martinique | `/shop/ck-mo-028-sauce-scotch-bonnet-creole-467` |
| CK-MO-029 | Confiture goyave rose | Confitures | Guadeloupe | `/shop/ck-mo-029-confiture-goyave-rose-468` |
| CK-MO-030 | Pochette curry des Antilles | Épices | Martinique | `/shop/ck-mo-030-pochette-curry-des-antilles-469` |
| CK-MO-031 | Marinade jerk citron vert | Assaisonnements | Martinique | `/shop/ck-mo-031-marinade-jerk-citron-vert-470` |
| CK-MO-032 | Biscuits banane confiture | Biscuits sucrés | Guadeloupe | `/shop/ck-mo-032-biscuits-banane-confiture-471` |
| CK-MO-033 | Palettes coco vanille | Biscuits sucrés | Martinique | `/shop/ck-mo-033-palettes-coco-vanille-472` |
| CK-MO-034 | Chips patate douce créole | Biscuits salés | Guadeloupe | `/shop/ck-mo-034-chips-patate-douce-creole-473` |
| CK-MO-035 | Crackers sarrasin Réunion | Biscuits salés | La Réunion | `/shop/ck-mo-035-crackers-sarrasin-reunion-474` |
| CK-MO-036 | Sauce chien antillaise | Condiments | Guadeloupe | `/shop/ck-mo-036-sauce-chien-antillaise-475` |
| CK-MO-037 | Tapenade agrumes confits | Condiments | Martinique | `/shop/ck-mo-037-tapenade-agrumes-confits-476` |
| CK-MO-038 | Confiture christophine gingembre | Confitures | Guadeloupe | `/shop/ck-mo-038-confiture-christophine-gingembre-477` |
| CK-MO-039 | Confiture papaye muscovado | Confitures | La Réunion | `/shop/ck-mo-039-confiture-papaye-muscovado-478` |
| CK-MO-040 | Quatre épices créoles | Épices | Guadeloupe | `/shop/ck-mo-040-quatre-epices-creoles-479` |
| CK-MO-041 | Poudre colombo créole | Épices | Martinique | `/shop/ck-mo-041-poudre-colombo-creole-480` |
| CK-MO-042 | Bouillon légumes des îles | Assaisonnements | Guadeloupe | `/shop/ck-mo-042-bouillon-legumes-des-iles-481` |
| CK-MO-043 | Rougail tomate créole | Assaisonnements | La Réunion | `/shop/ck-mo-043-rougail-tomate-creole-482` |
| CK-MO-044 | Sirop jambosier | Sirops | Martinique | `/shop/ck-mo-044-sirop-jambosier-483` |
| CK-MO-045 | Sirop banane flambée | Sirops | Guadeloupe | `/shop/ck-mo-045-sirop-banane-flambee-484` |
| CK-MO-046 | Jus goyave passion | Boissons | Guadeloupe | `/shop/ck-mo-046-jus-goyave-passion-485` |
| CK-MO-047 | Infusion bois bandé | Boissons | Martinique | `/shop/ck-mo-047-infusion-bois-bande-486` |
| CK-MO-048 | Farine banane plantain | Farines | Guadeloupe | `/shop/ck-mo-048-farine-banane-plantain-487` |
| CK-MO-049 | Flocons manioc instantanés | Fécules | La Réunion | `/shop/ck-mo-049-flocons-manioc-instantanes-488` |
| CK-MO-050 | Miel polyfloral créole | Miels | Martinique | `/shop/ck-mo-050-miel-polyfloral-creole-489` |

*(Secondaires systématiques : Incontournables + jusqu’à 2 rayons contextuels — max 4 catégories.)*

---

## Réexécution (idempotent)

```bash
docker exec -i sandbox-odoo19-odoo-1 odoo shell -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 --no-http \
  < odoo19-addons-dorevia/dorevia_ckreyol_marketone/scripts/seed_catalogue_extension_23.py
```

---

## Suite pilote média

- Export images BO → `tools/ck_image_normalizer/input/pilote/`
- Compléter `manifest.pilote.csv` (50 lignes) — voir [`catalogue_pilote_50_produits.csv`](./catalogue_pilote_50_produits.csv)
- Signal MOA : `GO exécution pilote média — 50 SKU sélectionnés — manifest prêt`

---

## Références

- Mapping initial 27 : [`MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md`](../cadrage/MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md)
- Préparation pilote : [`PREPARATION_MOA_PILOTE_MEDIA_50SKU.md`](./PREPARATION_MOA_PILOTE_MEDIA_50SKU.md)
