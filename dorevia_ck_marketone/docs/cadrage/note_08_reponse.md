# Retour Dev — Note 08 · Fiche produit CK · Modèle de données & architecture d’information V1.1

| Champ | Valeur |
| --- | --- |
| Date | 27 juin 2026 |
| Référence | `note_08.md` |
| Module cible | `dorevia_ck_marketone_content` (+ templates `dorevia_ck_theme`) |
| Statut | **GO MOA avec réserves (R1–R4)** — [`NOTE_MOA_DECISION_NOTE_08.md`](./NOTE_MOA_DECISION_NOTE_08.md) |
| Version module | `19.0.1.53.1` |

---

## Synthèse

| Élément | Réponse |
| --- | --- |
| **Faisabilité** | **Oui** — socle déjà amorcé (Lot 1/2 fiche produit, cartographie champs CK) |
| **Approche** | Champs dédiés MOA sur `product.template` + `ck.product.badge` + extension `res.partner` ; repli transitoire parser `website_description` pour catalogue seed existant |
| **Champs non créés (audit)** | `ck_short_description` → **`description_ecommerce`** ; `ck_net_weight_label` → **`ck_net_quantity` + `ck_net_quantity_uom_id`** |

---

## 1. Phase 0 — Audit d’existant

### 1.1 Champs CK déjà présents sur `product.template`

| Champ | Statut |
| --- | --- |
| `ck_net_quantity` | Existant — quantité nette commerciale |
| `ck_net_quantity_uom_id` | Existant — unité affichage (g, L, pièce…) |
| `ck_reference_price_uom_id` | Existant — unité prix de référence (kg, L) |
| `ck_show_reference_price` | Existant — toggle affichage €/kg ou €/L |
| `ck_is_featured` | Existant — curation home |
| `description_ecommerce` | Standard Odoo — **accroche courte zone haute** (équivalent MOA `ck_short_description`) |
| `website_description` | Standard Odoo — contenu long parsé Lot 2 (repli transitoire) |

### 1.2 Catégorie visible front

**Source confirmée : `public_categ_ids`** (`product.public.category`).

Utilisée dans :
- chips zone haute fiche (`dorevia_ck_theme.product_ck_title_chips`) ;
- ligne meta cards (`home_featured._get_featured_card_metadata_line`) ;
- filtres shop natifs Odoo.

`categ_id` (catégorie interne) **n’est pas** utilisée en front CK.

### 1.3 Origine produit

**Source unique : attribut produit « Origines »** via `ck_product_origin.ck_origin_from_attribute()`.

Doctrine CK existante confirmée — pas de création `ck_origin_id`.

### 1.4 Prix affiché `website_sale`

Pipeline contextualisé déjà en place dans `home_featured._get_featured_price_amount()` :
- pricelist website ;
- `lst_price` variante ;
- taxes + position fiscale (`_apply_taxes_to_price`).

Le front natif Odoo (`combination_info`) reste la source zone achat ; les cards CK utilisent le helper Python ci-dessus.

### 1.5 Prix de référence kg/L cards

Calcul existant : `ck_net_quantity` × `ck_net_quantity_uom_id` + prix contextualisé → `_format_featured_reference_price()`.

**Ne pas utiliser `weight`** (poids logistique Odoo).

### 1.6 Disponibilité stock website

Logique standard `website_sale` / `_is_add_to_cart_possible()` — **aucune exposition** de `qty_available` ou `virtual_available` en front CK.

### 1.7 Emplacement BO recommandé

Onglet **Ventes** CK (`product_template_form_view_ck_featured_card`) — blocs ajoutés :

| Bloc BO | Champs |
| --- | --- |
| Accroche & mise en avant | `description_ecommerce`, `ck_badge_ids` |
| Origine & producteur | `ck_producer_id` (+ attribut Origines en onglet Attributs) |
| Contenu fiche produit | `ck_discover_html`, `ck_ingredients`, `ck_allergens`, `ck_nutrition_html`, `ck_conservation_*` |
| Infos pratiques | `ck_packaging_label`, `default_code`, `weight`, `public_categ_ids` |

Référentiel badges : menu **Badges produit CK** (`ck.product.badge`).

Producteur : onglet partenaire **Producteur CK** sur `res.partner`.

### 1.8 Modules modifiés

| Module | Périmètre |
| --- | --- |
| `dorevia_ck_marketone_content` | Modèles, logique sections, vues BO, templates QWeb V1.1, tests |
| `dorevia_ck_theme` | SCSS fiche produit, bloc producteur, réassurance V1.1 |

---

## 2. Livrables implémentés

### Modèle de données

- `ck.product.badge` + seed MOA (Guadeloupe, Farine de manioc, Producteur identifié)
- Extension `res.partner` : `ck_is_producer`, `ck_producer_short_description`, `ck_producer_story_html`, `ck_producer_location_label`
- Champs produit : `ck_producer_id`, `ck_badge_ids`, `ck_discover_html`, `ck_ingredients`, `ck_allergens`, `ck_nutrition_html`, `ck_conservation_before`, `ck_conservation_after`, `ck_packaging_label`

### Architecture front V1.1

Zone haute :
- catégorie (`public_categ_ids`) ;
- métadonnées enrichies (`get_ck_product_page_metadata_line`) : origine · producteur · poids net · prix réf. ;
- accroche (`description_ecommerce`) ;
- badges qualifiés (`ck_badge_ids`) ;
- prix contextualisé natif ;
- variantes avec **prix absolus** (héritage `website_sale.badge_extra_price`) ;
- navigation ancres **sticky** + état actif au scroll (`ck_product_page_anchors.js`) ;
- réassurance V1 (sans remboursement 30 jours).

Sections sous ligne de flottaison (ordre fixe, ancres conditionnelles) :
1. Découvrir
2. Composition
3. Conservation
4. Infos pratiques
5. Producteur

Repli transitoire : produits seed avec `website_description` structuré conservent le rendu Lot 2 tant que les champs dédiés ne sont pas renseignés.

### Tests

Tag Odoo : `dorevia_ck_product_page_note08` · `dorevia_ck_product_page_note08_recette`

Couverture :
- création champs CK + domaine producteur ;
- affichage conditionnel ancres ;
- réassurance V1 sans promesse 30 jours ;
- badges + bloc producteur front.

---

## 3. Points MOA / recette

| Point | Action recette |
| --- | --- |
| Migration contenu | Renseigner progressivement les champs dédiés BO ; le parser `website_description` reste actif en repli |
| Badges sensibles | Ne pas affecter Bio / Sans gluten / etc. sans preuve — champs `requires_validation` / `is_sensitive_claim` en BO |
| Wireframe HTML | Document `ck_fiche_produit_wireframe.html` non présent dans le dépôt — organisation validée via note 08 §9 |
| Spec data V1.1 | Document `CK-SPECS-DATA-V1.1.md` non présent — implémentation alignée sur `note_08.md` + cartographie existante |

---

## 4. Déploiement

```bash
-u dorevia_ck_marketone_content,dorevia_ck_theme
```

Tests ciblés :

```bash
odoo-bin -d <base> --test-tags dorevia_ck_product_page_note08_recette --stop-after-init
odoo-bin -d <base> --test-tags dorevia_ck_product_page_note08,dorevia_ck_product_page_tabs,dorevia_ck_product_page_lot2_front --stop-after-init
```

---

## 5. Clôture recette QA (27 juin 2026)

| Élément | Résultat |
| --- | --- |
| **Verdict** | **GO avec réserves (R1–R4)** |
| **Tests auto** | **43/43** (0 failed, 0 error) |
| **Bugs corrigés en recette** | BUG-N08-001 (label `Contenance`) · BUG-N08-002 (XPath delta variante) |
| **Décision MOA** | **GO avec réserves (R1–R4)** — [`NOTE_MOA_DECISION_NOTE_08.md`](./NOTE_MOA_DECISION_NOTE_08.md) |
| **Verdict détaillé** | [`RECETTE_QA_NOTE_08_VERDICT.md`](../design/maquette_01.2/RECETTE_QA_NOTE_08_VERDICT.md) |

**Suivi réserves** : R1 [`TICKET_POLISH_ACCROCHE_ECOMMERCE_NOTE08_R1.md`](./TICKET_POLISH_ACCROCHE_ECOMMERCE_NOTE08_R1.md) · R2 validation visuelle MOA · R3 [`TICKET_CONTENU_SEED_MANIO_PLATINE_NOTE08_R3.md`](./TICKET_CONTENU_SEED_MANIO_PLATINE_NOTE08_R3.md) · R4 transitoire (migration contenus dédiés).
