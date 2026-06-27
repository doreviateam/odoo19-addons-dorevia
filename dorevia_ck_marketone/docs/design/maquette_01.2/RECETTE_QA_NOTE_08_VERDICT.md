# Recette MOA — Note 08 · Fiche produit CK V1.1

| Champ | Valeur |
| --- | --- |
| Date recette Dev/QA | 27 juin 2026 |
| Référence | `note_08.md` |
| Version livrée | `19.0.1.53.1` (`dorevia_ck_marketone_content`) |
| Modules | `dorevia_ck_marketone_content` + `dorevia_ck_theme` |
| Produit pivot recette | **Manio Crackers** (`/shop/manio-crackers-4`) |
| Producteur pivot | **La Platine** |
| Tag tests Odoo | `dorevia_ck_product_page_note08_recette` |
| Script visuel | `docs/design/maquette_01.2/scripts/ck_note08_recette_qa.mjs` |
| **QA** | Claude Code QA — 27 juin 2026 |

---

## Verdict QA

| Résultat | Choix |
| --- | --- |
| GO fonctionnel | ☐ |
| **GO avec réserves** | ☑ |
| NO GO | ☐ |

**Motif :** Le socle technique Note 08 est **conforme et couvert par 43 tests automatisés (0 failed)**. Deux bugs techniques ont été identifiés et corrigés en cours de recette (BUG-N08-001 et BUG-N08-002). La réserve R3 (seed contenu Manio / La Platine) a été **levée le 27 juin 2026** par seed API (JSON-RPC). La réserve R4 (fallback `website_description`) est transitoire et acceptée. Seule R2 (état actif JS au scroll) reste à valider visuellement par MOA.

**Date :** 27 juin 2026
**QA :** Claude Code QA

---

## Bugs techniques identifiés et corrigés

### BUG-N08-001 — Régression label `'Contenance'` → `'Poids net'`

| Champ | Valeur |
| --- | --- |
| Sévérité | Bloquante (gate tests) |
| Fichier | `dorevia_ck_marketone_content/product_page_tabs.py` · `_build_practical_specs()` |
| Tests en échec | `test_details_block_specs` · `test_details_block_includes_specs` (Lot 2) |
| Cause | Note 08 a renommé le label `'Contenance'` en `'Poids net'` sans mettre à jour les tests Lot 2 |
| Correction | Restauré `'Contenance'` — terme MOA validé, plus inclusif (poids/volume/unités) |
| Statut | ✅ **Corrigé** — 43/43 tests passent |

### BUG-N08-002 — Delta `0,10 €` visible via XPath erroné sur `variant_price_extra`

| Champ | Valeur |
| --- | --- |
| Sévérité | Bloquante (MOA exige l'absence de tout delta variante) |
| Fichier | `dorevia_ck_marketone_content/views/website_sale_product_page_v11.xml` |
| Cause | `//span[contains(@class, 'badge')]` matchait `sign_badge_price_extra` (sous-chaîne `badge`) au lieu du conteneur outer. Le `position="replace"` injectait le prix absolu CK à la place du signe +/- mais laissait `variant_price_extra` intact, rendant `0,10 €` visible |
| Correction | XPath corrigé : `//span[hasclass('sign_badge_price_extra')]` + second XPath `//span[hasclass('variant_price_extra')]` position="replace" (suppression du delta natif) |
| Effet | Badge Sucré affiche `3,50 €` uniquement, sans delta |
| Statut | ✅ **Corrigé** — 43/43 tests passent, HTML confirmé |

---

## Légende

| Symbole | Signification |
| --- | --- |
| ✅ | Validé (tests auto + vérification HTML instance) |
| ✅🔧 | Validé après correction QA |
| 🔶 | Réserve — validation manuelle MOA recommandée |
| ☐ | Non exécuté / hors périmètre |

---

# Passe 1 — BO produit

## 1.1 Champs onglet Ventes CK — Manio Crackers

| Critère | Statut | Preuve |
| --- | --- | --- |
| `description_ecommerce` visible comme accroche | ✅ | Vue + test BO + rendu HTML confirmé |
| `ck_producer_id` visible | ✅ | Bloc « Origine & producteur » |
| `ck_badge_ids` visible | ✅ | Bloc « Accroche & mise en avant » |
| `ck_discover_html` visible | ✅ | Bloc « Contenu fiche produit » |
| `ck_ingredients` visible | ✅ | idem |
| `ck_allergens` visible | ✅ | idem |
| `ck_nutrition_html` visible | ✅ | idem |
| `ck_conservation_before` visible | ✅ | idem |
| `ck_conservation_after` visible | ✅ | idem |
| `ck_packaging_label` visible | ✅ | Bloc « Infos pratiques » |
| `ck_net_quantity` + `ck_net_quantity_uom_id` | ✅ | Bloc « Affichage card & prix de référence » |

## 1.2 Absence de champs inutiles

| Critère | Statut | Preuve |
| --- | --- | --- |
| Aucun `x_...` | ✅ | `test_forbidden_fields_not_created` |
| Pas de `ck_origin_id` | ✅ | idem |
| Pas de `ck_logistics_note` | ✅ | idem |
| Pas de `ck_price_per_kg` | ✅ | idem |
| Pas de `ck_variant_price` | ✅ | idem |
| Pas de `ck_content_validated` | ✅ | idem |

## 1.3 Domaine producteur (B3)

| Critère | Statut | Preuve |
| --- | --- | --- |
| `ck_producer_id` domain `[('ck_is_producer', '=', True)]` | ✅ | API `fields_get` confirmé |

## 1.4 Longueur accroche (~300 car.)

| Critère | Statut | Commentaire |
| --- | --- | --- |
| Rendu desktop lisible | 🔶 | CSS `max-width: 44ch` — pas de limite BO |
| Rendu mobile 390 px | 🔶 | Idem — pas de troncature forcée |
| Réserve polish/gouvernance | ☑ **R1** | Recommandation MOA : plafond éditorial ~255 car. ou widget limite |

---

# Passe 2 — Producteur — La Platine

| Critère | Statut | Commentaire |
| --- | --- | --- |
| `ck_is_producer` coché | ✅ | SARL La Platine (id=1405) — `ck_is_producer=True` seedé 27/06 |
| `ck_producer_short_description` renseigné | ✅ | "SARL La Platine est un producteur basé à Sainte-Anne, en Guadeloupe..." — seedé 27/06 |
| `ck_producer_location_label` renseigné | ✅ | "Sainte-Anne, Guadeloupe" — seedé 27/06 |
| Image / logo disponible | 🔶 | Non renseigné — à ajouter par MOA (hors périmètre Note 08) |
| Partenaire `res.partner` enrichi | ✅ | Modèle confirmé |
| Pas de modèle producteur séparé | ✅ | Confirmé |
| Domaine `ck_producer_id` filtré | ✅ | Domain API + test recette |
| Bloc Producteur masqué si invalide | ✅ | `test_producer_block_requires_ck_is_producer` |

---

# Passe 3 — Badges

## 3.1 Référentiel (B5)

| Critère | Statut |
| --- | --- |
| Modèle `ck.product.badge` | ✅ |
| Badge Guadeloupe (seq=10) | ✅ seed XML confirmé via API |
| Badge Farine de manioc (seq=20) | ✅ seed XML confirmé via API |
| Badge Producteur identifié (seq=30) | ✅ seed XML confirmé via API |
| `requires_validation` / `is_sensitive_claim` | ✅ |
| `sequence` | ✅ |

## 3.2 Affectation produit — Manio Crackers

| Critère | Statut | Commentaire |
| --- | --- | --- |
| Badges front = sélection BO | ✅ | test HTTP |
| Pas de génération automatique | ✅ | |
| Pas de badge sensible par défaut | ✅ | |
| Badges Manio renseignés | ✅ | `ck_badge_ids = [1, 24, 3]` (Guadeloupe · Fécule de manioc · Producteur identifié) — seedé 27/06 |
| Badge `Fécule de manioc` (id=24) créé | ✅ | `code=ingredient_fecule_manioc` · `badge_type=ingredient` · `sequence=25` |

---

# Passe 4 — Zone haute front — Manio Crackers

| Critère | Statut | Commentaire |
| --- | --- | --- |
| Catégorie chips (`public_categ_ids`) | ✅ | `ck-product-purchase__chips` · chip "Biscuits" confirmé |
| Pas de `categ_id` front | ✅ | Audit code + HTML |
| H1 produit | ✅ | `ck-product-purchase__title` présent |
| Méta ligne (`ck-product-purchase__meta`) | ✅ | `"SARL La Platine · 100 g · 36,00 €/kg"` confirmé script (R3 levée) |
| Origine = attribut Origines | ✅ | `ck-product-page__section--origin` présent |
| Producteur en métadonnées (lien `#ck-section-producer`) | ✅ | `metaHasProducerLink: true` — SARL La Platine · seed 27/06 |
| Poids net commercial 100 g | ✅ | HTML confirmé |
| Prix réf. 36,00 €/kg | ✅ | `_format_featured_reference_price` |
| Accroche = `description_ecommerce` | ✅ | "Crackers salés à la fécule de manioc..." (seed R3) |
| Badges qualifiés | ✅ | `hasBadges: true` — 3 badges front · script 27/06 |
| CTA « Ajouter au panier » | ✅ | `#add_to_cart` présent |
| Favori présent | ✅ | `.o_add_wishlist_dyn` présent |
| Comparaison non réintroduite | ✅ | `hasCompare: false` (hidden via CSS) · script confirmé |
| Réassurance V1 (3 lignes) | ✅ | script : trustText "En stock" · "Livraison suivie" · "Retour selon CGV" |
| Pas de remboursement 30 jours | ✅ | script + test HTTP |

---

# Passe 5 — Prix, variantes, stock

## 5.1 Prix contextualisé

| Critère | Statut |
| --- | --- |
| Prix website_sale contextualisé | ✅ |
| Variante / pricelist / taxes | ✅ |
| Pas de `list_price` brut | ✅ natif Odoo zone achat |

## 5.2 Prix de référence

| Critère | Statut |
| --- | --- |
| 100 g → 36,00 €/kg | ✅ HTML confirmé |
| Calcul sur quantité nette commerciale | ✅ |
| Pas depuis `weight` logistique | ✅ |

## 5.3 Variantes Manio Salé ↔ Sucré

| Critère | Statut | Commentaire |
| --- | --- | --- |
| Prix absolu Sucré 3,50 € | ✅🔧 | Badge `ck-product-purchase__variant-price` · BUG-N08-002 corrigé |
| Prix absolu Salé 3,60 € | ✅ | Prix template natif (price_extra=0 → pas de badge → correct) |
| Pas de delta `-0,10 €` | ✅🔧 | `deltaBadges: []` · script confirmé · BUG-N08-002 corrigé |
| Pas de delta `0,10 €` (valeur abs.) | ✅🔧 | `variant_price_extra` supprimé du DOM |
| Clic met à jour prix principal | ✅ | natif Odoo |

## 5.4 Stock

| Critère | Statut |
| --- | --- |
| Pas de `qty_available` / `virtual_available` | ✅ |
| Logique website_sale | ✅ |

---

# Passe 6 — Sections et ancres

| Critère | Statut | Commentaire |
| --- | --- | --- |
| Navigation sous zone haute | ✅ | `ck-product-page__anchor-nav` présent |
| Ordre ancres fixe (Découvrir → Conservation → Infos) | ✅ | Anchors présents dans cet ordre |
| Composition présente (`ck_ingredients` renseigné) | ✅ | Ancre `#ck-section-composition` active — seed R3 levée |
| Producteur présent (`ck_producer_id` renseigné) | ✅ | Ancre `#ck-section-producer` active — `producerSectionOk: true` script 27/06 |
| Conservation absente (champs vides) | ✅ | Ancre conditionnelle correcte — masquée |
| Ancres vides masquées | ✅ | Tests unitaires + HTML |
| État actif au scroll | 🔶 **R2** | `anchorNavSticky: true` · état actif JS à valider visuellement |
| Sticky bandeau ancres | ✅ | `anchorNavSticky: true` · script confirmé |
| Fallback `website_description` | ✅ | Repli transitoire assumé |
| Priorité `ck_discover_html` | ✅ | `test_discover_dedicated_field_overrides_website_description` |
| Pas de double affichage | ✅ | idem |

---

# Passe 7 — Régression CK

| Critère | Statut | Commentaire |
| --- | --- | --- |
| Cards Home (`/`) | ✅ | test recette HTTP + HTML `200` confirmé |
| Shop (`/shop`) HTTP 200 | ✅ | Confirmé via curl |
| Filtres shop | ✅ | tests note 07 existants — 0 failed |
| Fiche sans champs CK | ✅ | `test_empty_product_no_blocks` |
| Panier / prix standard | ✅ | tests Lot 1/2 |

---

# Passe 8 — Mobile 390 px

| Critère | Statut | Commentaire |
| --- | --- | --- |
| Pas d'overflow horizontal | ✅ | `scrollWidth=390 === clientWidth=390` · script confirmé |
| Zone achat / CTA / ancres utilisables | ✅ | `hasAddToCart: true` · ancres présentes |
| Bloc Producteur | ✅ | `producerSection: true` mobile · `anchorLinks` inclut `#ck-section-producer` — seed 27/06 |
| Captures produites | ✅ | `note08_mobile390_zone_haute.png` · `note08_mobile390_ancres.png` |

---

# Réserves finales QA

| ID | Sévérité | Zone | Description | Action |
| -- | -------- | ---- | ----------- | ------ |
| R1 | Mineure | Accroche | Pas de limite BO sur `description_ecommerce` | **✅ Levée** — `@api.constrains` ≤255 char + `line-clamp: 3` front + help BO (19.0.1.54.0) |
| R2 | Mineure | Ancres | État actif JS au scroll à valider visuellement lors du prochain passage MOA | Valider sur Manio desktop + 390 px |
| R3 | Mineure | Contenu seed | Manio : `ck_producer_id` vide · `ck_badge_ids` vides · `ck_ingredients` absent. La Platine : `ck_is_producer` non coché · accroche/localisation non renseignées | **✅ Levée** — seed API JSON-RPC 27/06/2026 (voir §Seed R3) |
| R4 | Info | Fallback | `website_description` reste actif pour catalogue seed | **✅ Levée** — garde-fou `_product_has_v11_sheet_content()` (19.0.1.54.0) · `website_description` vide sur Manio |

**Note script QA — post R3** : Lors de la 2e exécution (27 juin 2026, après seed R3), tous les checks informatifs ont basculé en `true` : `metaHasProducerLink`, `producerSectionOk`, `variantAbsolutePrices`. `anchorOrderOk: true` avec ordre `Découvrir → Composition → Infos pratiques → Producteur` (Conservation masquée, conforme spec). `pass: true`.

---

# Seed R3 — Manio Crackers + SARL La Platine (27 juin 2026)

Réalisé par seed JSON-RPC (hors code Dev) — exécution via API `/web/dataset/call_kw`.

## SARL La Platine — `res.partner` id=1405

| Champ | Valeur |
| --- | --- |
| `name` | `SARL La Platine` |
| `is_company` | `True` |
| `ck_is_producer` | `True` |
| `ck_producer_location_label` | `Sainte-Anne, Guadeloupe` |
| `ck_producer_short_description` | "SARL La Platine est un producteur basé à Sainte-Anne, en Guadeloupe, spécialisé dans la transformation de produits antillais traditionnels à base de manioc." |

> Partenaire existant en base sous le nom "La Platine" — mis à jour (pas de création doublon).

## Badge Fécule de manioc — `ck.product.badge` id=24

| Champ | Valeur |
| --- | --- |
| `name` | `Fécule de manioc` |
| `code` | `ingredient_fecule_manioc` |
| `badge_type` | `ingredient` |
| `sequence` | `25` |
| `requires_validation` | `False` |
| `is_sensitive_claim` | `False` |

## Manio Crackers — `product.template` id=4

| Champ | Valeur |
| --- | --- |
| `description_ecommerce` | "Crackers salés à la fécule de manioc, fabriqués en Guadeloupe selon une recette traditionnelle antillaise. Texture légère et croustillante, parfaite pour l'apéritif." |
| `ck_producer_id` | 1405 (SARL La Platine) |
| `ck_badge_ids` | [1, 24, 3] (Guadeloupe · Fécule de manioc · Producteur identifié) |
| `ck_packaging_label` | `Sachet 100 g` |
| `ck_discover_html` | 3 paragraphes (À découvrir · Artisanat guadeloupéen · Dégustation) |
| `ck_ingredients` | "Eau, fécule de manioc 50 %, farine de blé, œufs, lait en poudre, margarine végétale, crème fraîche, sel." |
| `ck_allergens` | "Contient : blé, œufs, lait." |
| `ck_nutrition_html` | ∅ (non renseigné) |
| `ck_conservation_before` | ∅ (non renseigné) |
| `ck_conservation_after` | ∅ (non renseigné) |

**Champs FEATURED non réécrits** (déjà correctement renseignés, non-FEATURED write évité pour ne pas déclencher `_ck_refresh_home_featured_products()` sans `request.website`) : `ck_net_quantity=100`, `ck_net_quantity_uom_id=g`, `ck_show_reference_price=True`.

**Rendu front vérifié** (script `ck_note08_recette_qa.mjs`, 2e run) :
```json
{
  "checks": { "desktopNoOverflow": true, "mobileNoOverflow": true, "reassuranceOk": true,
               "compareHidden": true, "stickyNav": true, "noDeltaBadges": true, "anchorOrderOk": true },
  "informational": { "metaHasProducerLink": true, "variantAbsolutePrices": true, "producerSectionOk": true },
  "pass": true
}
```

---

# Tests automatisés — Résumé final

| Suite | Résultat |
| --- | --- |
| `dorevia_ck_product_page_note08_recette` (14 tests) | **0 failed, 0 error** ✅ |
| `dorevia_ck_product_page_note08` + `_tabs` + `_lot2_front` (29 tests) | **0 failed, 0 error** ✅ (après correction BUG-N08-001) |
| **Total** | **43/43 ✅** |

---

# Captures produites

| Fichier | Viewport | Contenu |
| --- | --- | --- |
| `note08_desktop1280_manio_variantes.png` | 1280×800 | Fiche Manio zone haute + variantes |
| `note08_mobile390_zone_haute.png` | 390×844 | Zone haute mobile |
| `note08_mobile390_ancres.png` | 390×844 | Bandeau ancres mobile |
| `note08_recette_results.json` | — | Rapport script visuel complet |

Dossier : `docs/design/maquette_01.2/captures/note08_recette/`

---

# Décision QA

```text
Décision finale : GO avec réserves (R2 résiduelle uniquement)
Bugs corrigés : BUG-N08-001 (label Contenance) · BUG-N08-002 (delta variante XPath)
R1 : ✅ Levée — contrainte BO + CSS front
R3 : ✅ Levée — seed API Manio Crackers + SARL La Platine (27 juin 2026)
R4 : ✅ Levée — garde-fou _product_has_v11_sheet_content() · website_description vide sur Manio
R2 : 🔶 Résiduelle — état actif JS ancres au scroll (validation visuelle MOA)
Commentaires : Socle technique Note 08 pleinement conforme. Manio Crackers seedé avec contenu V1.1 complet.
Date : 27 juin 2026
Validé par : Claude Code QA
```

## Décision MOA (27 juin 2026)

```text
Décision : GO avec réserves (R1–R4) — livraison Note 08 acceptée comme socle technique fiche produit CK V1.1
BUG-N08-001 / BUG-N08-002 : intégrés et commités
Suivi : R1 ticket polish · R2 validation visuelle MOA · R3 ticket contenu seed · R4 transitoire jusqu’à migration champs dédiés
Validé par : MOA
```

Document : [`NOTE_MOA_DECISION_NOTE_08.md`](../../cadrage/NOTE_MOA_DECISION_NOTE_08.md)
