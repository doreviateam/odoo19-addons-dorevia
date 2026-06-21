# Note technique — BO Produit CK · onglet Ventes (Lot 1)

**Instance** : `dorevia_ck_marketone_01`  
**Module** : `dorevia_ck_marketone_content`  
**Vue** : `product_template_form_view_ck_featured_card` (priorité 35)  
**Héritage** : `website_sale.product_template_form_view`

---

## Phase 0 — Audit groupes existants (avant réorganisation)

| Groupe actuel | `name` | Origine | Champs principaux | XPath / risque |
|---------------|--------|---------|-------------------|----------------|
| Upsell & Cross-Sell | `upsell` | `product` + `sale` + `website_sale` | `uom_ids`, `optional_product_ids`, `accessory_product_ids`, `alternative_product_ids`, `description_ecommerce` (hidden) | `sale` / `website_sale` `position="inside"` — **conservé** sous `ck_product_recommendations` |
| Extra Info / Boutique eCommerce | `extra_info` | `product` + `website_sale` + **CK** | publication, catégories, ruban, tags, quantité commerciale CK | CK `position="replace"` (ancien) — **remplacé par coquille invisible** `extra_info` |
| eCommerce Media | `product_template_images` | `website_sale` | `product_template_image_ids` | xpath `//page[@name='sales']/group[@name='sale']` — **déplacé** vers `ck_ecommerce_media` |
| Ecommerce Description | `ecom_description` | `website_sale` | `description_ecommerce` | xpath avant `description` — **déplacé** vers `ck_ecommerce_description` |
| Quotation Description | `description` | `product` | `description_sale` | standard — **déplacé** vers `ck_commercial_documents` |
| Sale (conteneur) | `sale` | `product` | sous-groupes | **supprimé** au profit de blocs CK plats (champs conservés) |

Champs CK (`dorevia_ck_marketone_content`) : `ck_net_quantity`, `ck_net_quantity_uom_id`, `ck_show_reference_price`, `ck_reference_price_uom_id`.

---

## Conditions générales de vente (hors périmètre)

| Élément | Source |
|---------|--------|
| Lien « Conditions générales de vente » sous CTA fiche produit | Template `dorevia_ck_theme.product_ck_terms_fr` héritant `website_sale.product_terms_and_conditions` |
| URL `/terms` | Page CMS créée par `dorevia_ck_marketone_content` (`legal_pages.py` / `hooks.py`) |
| Contenu CGV | `TERMS_PAGE_ARCH` — module content, pas champ produit |

**Décision MOA** : non modifié, non déplacé dans l’onglet Ventes.

- `CARTOGRAPHIE_CHAMPS_PRODUIT_CK_V1.md` — audit + validation réorganisation Ventes
- `NOTE_CLARIFICATION_PARSER_WEBSITE_DESCRIPTION_CK_V1.md` — format `website_description` & fallback `description_sale`

---

## Structure cible livrée (7 blocs · 2 colonnes par ligne)

| Ligne | Colonne gauche | Colonne droite |
|-------|----------------|----------------|
| 1 | `ck_publication_highlight` | `ck_shop_classification` |
| 2 | `ck_card_reference_price` | `ck_ecommerce_description` |
| 3 | `ck_ecommerce_media` | `ck_product_recommendations` |
| 4 | `ck_commercial_documents` | — |

Champs par bloc inchangés (voir v1.25.23). Mise en page : paires de `<group>` dans un conteneur parent sans `colspan="2"`.

Alertes vente / dépenses Odoo standard conservées en bas de page.

---

## XPath utilisé

```xml
<xpath expr="//page[@name='sales']" position="replace">…</xpath>
```

Aucun champ technique renommé. Aucun nouveau modèle / champ. Aucun changement front.

---

## Tests

`dorevia_ck_marketone_content.tests.test_ck_product_sales_tab_bo` — tag `dorevia_ck_product_sales_tab_bo`

---

## Recette MOA — verdict (consolidation BO)

**Verdict** : OK avec réserves légères · **GO consolidation BO** · pas de reprise front fiche produit tant que la fiche produit BO type CK n’est pas définie.

### Ajustements libellés (v1.25.25)

| Bloc `name` | Libellé BO | Clarification |
|-------------|------------|---------------|
| `ck_ecommerce_description` | **Accroche e-commerce** | `description_ecommerce` — phrase courte tête de fiche site (lead zone achat CK). |
| `ck_ecommerce_media` | **Galerie e-commerce** | `product_template_image_ids` (website_sale) — médias site, hors image principale et hors images variantes. |
| `ck_commercial_documents` | **Notes commerciales** | `description_sale` — note commandes / devis / factures Odoo. Nom technique du groupe inchangé. |

### Conditionnements (`uom_ids`)

| Élément | Détail |
|---------|--------|
| Champ | `product.template.uom_ids` |
| Module | `product` (libellé Odoo source : « Packagings ») |
| Rôle | Unités de vente additionnelles sur devis / commandes |
| Placement actuel | Groupe `upsell` → bloc `ck_product_recommendations` (héritage vue standard) |
| Décision MOA | **Conservé** dans Recommandations pour cette passe · candidat futur bloc logistique / conditionnement |

### Héritages XML — contrôle non-régression

| XPath / groupe | Module cible | Statut |
|----------------|--------------|--------|
| `//page[@name='sales']` replace | CK content | Seul point d’entrée CK |
| `group[@name='upsell']` | sale / website_sale | **Conservé** (imbriqué dans `ck_product_recommendations`) |
| `group[@name='description']` | product | **Conservé** (sous `ck_commercial_documents`) |
| `group[@name='extra_info']` invisible | website_sale + xpath Marketone | **Coquille vide** conservée |
| `dorevia_ckreyol_marketone` xpaths `extra_info` / `ecom_description` | Marketone (si installé) | Non impacté sur instance CK Marketone seule |

Aucun champ technique renommé. Aucun impact front.
