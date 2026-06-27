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

**Motif :** Le socle technique Note 08 est **conforme et couvert par 43 tests automatisés (0 failed)**. Deux bugs techniques ont été identifiés et corrigés en cours de recette (BUG-N08-001 et BUG-N08-002). Les réserves restantes (R3, R4) portent exclusivement sur le **contenu seed** non encore renseigné sur l'instance — ce ne sont pas des blocages techniques.

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
| `ck_is_producer` coché | 🔶 **R3** | La Platine non encore seedée comme producteur CK (0 partenaire `ck_is_producer=True` en base) |
| `ck_producer_short_description` renseigné | 🔶 **R3** | Contenu seed manquant |
| `ck_producer_location_label` renseigné | 🔶 **R3** | Contenu seed manquant |
| Image / logo disponible | 🔶 **R3** | Non renseigné |
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
| Badges non renseignés sur Manio | 🔶 **R3** | `ck_badge_ids = []` en base — contenu seed à renseigner |

---

# Passe 4 — Zone haute front — Manio Crackers

| Critère | Statut | Commentaire |
| --- | --- | --- |
| Catégorie chips (`public_categ_ids`) | ✅ | `ck-product-purchase__chips` · chip "Biscuits" confirmé |
| Pas de `categ_id` front | ✅ | Audit code + HTML |
| H1 produit | ✅ | `ck-product-purchase__title` présent |
| Méta ligne (`ck-product-purchase__meta`) | ✅ | `100 g · 36,00 €/kg` confirmé HTML |
| Origine = attribut Origines | ✅ | `ck-product-page__section--origin` présent |
| Producteur en métadonnées (lien `#ck-section-producer`) | 🔶 **R3** | Lien absent car `ck_producer_id` non renseigné sur Manio |
| Poids net commercial 100 g | ✅ | HTML confirmé |
| Prix réf. 36,00 €/kg | ✅ | `_format_featured_reference_price` |
| Accroche = `description_ecommerce` | ✅ | "Galettes croustillantes — univers apéritif CK." |
| Badges qualifiés | 🔶 **R3** | Aucun badge renseigné sur Manio seed |
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
| Composition absente (normal : pas d'ingrédients Manio) | ✅ | Ancre conditionnelle correcte |
| Producteur absent (normal : `ck_producer_id` vide) | ✅ **R3** | Ancre conditionnelle correcte — seed à renseigner |
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
| Bloc Producteur | 🔶 **R3** | Non renseigné (seed) |
| Captures produites | ✅ | `note08_mobile390_zone_haute.png` · `note08_mobile390_ancres.png` |

---

# Réserves finales QA

| ID | Sévérité | Zone | Description | Action |
| -- | -------- | ---- | ----------- | ------ |
| R1 | Mineure | Accroche | Pas de limite BO sur `description_ecommerce` | Gouvernance éditoriale ou limite widget ~255 car. — ticket polish |
| R2 | Mineure | Ancres | État actif JS au scroll à valider visuellement lors du prochain passage MOA | Valider sur Manio desktop + 390 px |
| R3 | Mineure | Contenu seed | Manio : `ck_producer_id` vide · `ck_badge_ids` vides · `ck_ingredients` absent. La Platine : `ck_is_producer` non coché · accroche/localisation non renseignées | Migration contenu MOA — ticket contenu |
| R4 | Info | Fallback | `website_description` reste actif pour catalogue seed | Accepté transitoirement (préambule MOA) |

**Note script QA** : Les checks `metaHasProducerLink`, `producerSectionOk` et `variantAbsolutePrices` sont **informatifs** (seed R3) — le gate pass/fail ne porte que sur overflow, réassurance, comparaison masquée, sticky, absence de delta variante et ordre relatif des ancres présentes.

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
Décision : GO avec réserves (R1–R4)
Bugs corrigés en cours de recette : BUG-N08-001 (label Contenance) · BUG-N08-002 (delta variante XPath)
Commentaires : Socle technique conforme. Seed contenu Manio / La Platine à renseigner par MOA avant présentation.
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
