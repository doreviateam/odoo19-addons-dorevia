# Cartographie technique — champs produit CK V1

**Instance de référence** : `dorevia_ck_marketone_01`  
**Document MOA** : Fiche produit BO type CK — V1 amendée  
**Module principal CK** : `dorevia_ck_marketone_content` (19.0.1.25.26)  
**Vue BO Ventes CK** : `product_template_form_view_ck_featured_card`  
**Date cartographie** : juin 2026

---

## Synthèse Dev

| Décision | Constat |
|----------|---------|
| Champs CK dédiés produit | **4** sur `product.template` + modèle support `dorevia.ck.card.uom` |
| Onglet Ventes CK | **7 blocs** — réorganisation XML uniquement, validée MOA |
| Nouveau champ dans cette passe | **Aucun** |
| Front fiche produit | **Suspendu** jusqu’à arbitrage MOA post-cartographie |

**Modules Odoo requis par `dorevia_ck_marketone_content`** : `account`, `dorevia_ck_theme`, `website_sale`, `website_crm`, `mass_mailing`, `website_mass_mailing` (→ tire `product`, `sale`, `website`, `uom`, etc.).

**Modules souvent co-installés sur l’instance e-commerce** (à confirmer par module list) : `stock`, `purchase`, `website_sale_wishlist`, `website_sale_comparison`.

---

## Légende colonnes

| Colonne | Signification |
|---------|---------------|
| **Présent onglet Ventes ?** | Visible dans la vue CK réorganisée (`//page[@name='sales']`) |
| **Utilisé front/card ?** | Oui / Non / Calculé / Configuration / Partiel |

---

## 1. Identité commerciale

| Information métier CK | Champ technique | Modèle Odoo | Module d’origine | Statut | Présent onglet Ventes ? | Utilisé front/card ? | Commentaire |
| --------------------- | --------------- | ----------- | ---------------- | ------ | ------------------------ | -------------------- | ----------- |
| Nom produit | `name` | `product.template` | `product` | Standard Odoo | Non | Oui | Onglet **Général** (en-tête formulaire). Titre card + fiche. |
| Type de produit | `type` | `product.template` | `product` | Standard Odoo | Non | Partiel | `consu` / `service` / `combo` — onglet Général. Impacte quick-add panier. |
| Image principale | `image_1920` | `product.template` | `product` | Standard Odoo | Non | Oui | Onglet Général. Priorité image variante `image_variant_1920` sur card si renseignée. |
| Référence interne | `default_code` | `product.template` | `product` | Standard Odoo | Non | Non | Onglet Général / Inventaire selon config. |
| Code-barres | `barcode` | `product.product` | `product` | Standard Odoo | Non | Non | Variante ; onglet Général ou Inventaire. |
| Marque | — | — | — | À arbitrer MOA | Non | Non | Pas de champ dédié identifié sur l’instance CK. |
| Producteur visible | — / `seller_ids` ? | `product.template` | `purchase` (si installé) | À arbitrer MOA | Non | Partiel | Fournisseur via `seller_ids` possible ; pas de bloc « producteur » front dédié aujourd’hui. |
| Origine géographique | attribut « Origines » | `product.template` / attributs | Configuration | **Arbitré MOA** | Non (attribut : onglet Attributs & variantes) | Oui | **Source unique** : attribut produit « Origines » (`ck_product_origin.ck_origin_from_attribute`). Card + fiche produit. Fallback temporaire Option A sur tags géographiques si attribut vide. |

---

## 2. Publication & mise en avant

| Information métier CK | Champ technique | Modèle Odoo | Module d’origine | Statut | Présent onglet Ventes ? | Utilisé front/card ? | Commentaire |
| --------------------- | --------------- | ----------- | ---------------- | ------ | ------------------------ | -------------------- | ----------- |
| Produit publié sur le site | `is_published` | `product.template` | `website` (mixin) | Standard module installé | **Oui** (`ck_publication_highlight`) | Oui | Champ BO « Est publié ». Pilote visibilité boutique. |
| Visibilité site courant | `website_published` | `product.template` | `website` | Standard module installé | Non (lié) | Calculé | Related / computed depuis `is_published` + `website_id`. |
| Site web | `website_id` | `product.template` | `website` | Standard module installé | **Oui** | Partiel | Multi-site uniquement (`website.group_multi_website`). |
| Ruban produit / badge | `website_ribbon_id` | `product.template` | `website_sale` | Standard module installé | **Oui** | Oui | Modèle `product.ribbon`. Badge card SSR (`home_featured._featured_ribbon_html`). Ex. ruban « Nouveau ! » seed CK. |
| Séquence site web | `website_sequence` | `product.template` | `website_sale` | Standard module installé | **Oui** | Oui | Ordre catalogue / vedettes (mode auto). Groupe `base.group_no_one`. |
| Mise en avant Home / Coups de cœur | `public_categ_ids` → catégorie | `product.template` / `product.public.category` | Configuration CK | Configuration | **Oui** (catégories) | Oui | Catégorie e-commerce `Coups de cœur` (`dorevia_ck_marketone_content.public_categ_coups_de_coeur`). Curation Section 3 home. |
| Favori / wishlist | — (action front) | — | `website_sale_wishlist` | Standard module installé | Non | Oui (Boutique) | Pas de champ produit : interaction wishlist Odoo. Cœur **Boutique** uniquement (pas Home vedettes). À confirmer module installé. |

---

## 3. Classement boutique

| Information métier CK | Champ technique | Modèle Odoo | Module d’origine | Statut | Présent onglet Ventes ? | Utilisé front/card ? | Commentaire |
| --------------------- | --------------- | ----------- | ---------------- | ------ | ------------------------ | -------------------- | ----------- |
| Catégories e-commerce | `public_categ_ids` | `product.template` | `website_sale` | Standard module installé | **Oui** (`ck_shop_classification`) | Oui | Classement boutique + filtres. Exclure « Coups de cœur » de la ligne meta card. |
| Catégorie interne produit | `categ_id` | `product.template` | `product` | Standard Odoo | Non | Non | Gestion interne — onglet Général. Distinct de l’e-commerce. |
| Étiquettes produit | `product_tag_ids` | `product.template` | `product` | Standard Odoo | **Oui** | Oui (transversal) | **Tags transversaux uniquement** (Épicerie, Artisanal, Nouveau, etc.). Ne portent plus l'origine géographique. Ligne meta card : tags transversaux après le segment origine. Refresh home SSR si modifié. |
| Étiquettes variante | `additional_product_tag_ids` | `product.product` | `product` | Standard Odoo | Non | Oui (transversal) | Union avec template sur cards. Édition fiche variante. |
| Collection commerciale | — / catégories | `product.public.category` | Configuration | À arbitrer MOA | Non | Partiel | Pas de modèle `collection` CK sur cette instance (contrairement à `dorevia_ckreyol_marketone`). |
| Univers CK | racine `public_categ_ids` | `product.public.category` | Configuration | Configuration | **Oui** (via catégories) | Oui | Arborescence e-commerce (ex. Épicerie créole). Pas de champ dédié. |
| Origine en filtre boutique | attribut « Origines » | `product.attribute` | `website_sale` (natif) | Configuration | Non | Oui (si attribut filtrable) | Filtre shop = facettes attributs Odoo natif (`website_sale.products_attributes`). Pas de filtre sur `product_tag_ids`. À activer en BO eCommerce si absent. |

---

## 4. Affichage card & prix de référence

| Information métier CK | Champ technique | Modèle Odoo | Module d’origine | Statut | Présent onglet Ventes ? | Utilisé front/card ? | Commentaire |
| --------------------- | --------------- | ----------- | ---------------- | ------ | ------------------------ | -------------------- | ----------- |
| Prix public | `list_price` | `product.template` | `product` / `sale` | Standard Odoo | Non | Oui | Onglet **Général** ou **Ventes** standard. Prix card + fiche. |
| Prix variante | `lst_price` / `list_price` | `product.product` | `product` | Standard Odoo | Non | Oui | Édition prix variante BO. Cas Manio sucré/salé validé. |
| Supplément variante | `price_extra` | `product.template.attribute.value` | `product` | Standard Odoo | Non | Oui | Attributs & variantes. |
| Quantité nette | `ck_net_quantity` | `product.template` | `dorevia_ck_marketone_content` | Spécifique CK | **Oui** (`ck_card_reference_price`) | Oui | Ex. `320` → segment meta `320 g`. |
| Unité quantité nette | `ck_net_quantity_uom_id` | `product.template` → `dorevia.ck.card.uom` | Spécifique CK | Spécifique CK | **Oui** | Oui | Référentiel unités card (`ck_card_uom_data.xml`). |
| Prix de référence activé | `ck_show_reference_price` | `product.template` | Spécifique CK | Spécifique CK | **Oui** | Oui | Boolean — affiche €/kg ou €/L si calcul possible. |
| Unité de référence | `ck_reference_price_uom_id` | `product.template` → `dorevia.ck.card.uom` | Spécifique CK | Spécifique CK | **Oui** | Oui | Ex. `kg`, `L`. |
| Ligne meta card | — (méthode) | `product.template` | Spécifique CK | Calculé | Non | Oui | `get_ck_shop_card_metadata_line()` → `home_featured._get_featured_card_metadata_line` : **origine (attribut) · tags transversaux · quantité · prix réf.** |
| Badge card | `website_ribbon_id` | `product.template` | `website_sale` + rendu CK | Configuration + Calculé | **Oui** (ruban) | Oui | SSR home : HTML ruban depuis `product.ribbon`. |
| CTA Home | — | — | `dorevia_ck_theme` | Spécifique CK | Non | Oui | Templates QWeb snippet vedettes — pas un champ produit. |
| CTA Boutique | — | — | `dorevia_ck_theme` | Spécifique CK | Non | Oui | `shop_product_buttons_ck_card` — libellé FR. |
| Cœur favori Boutique | — | — | `website_sale_wishlist` | Standard + CK front | Non | Oui | SCSS + widget wishlist ; pas de champ BO produit. |

---

## 5. Accroche e-commerce

| Information métier CK | Champ technique | Modèle Odoo | Module d’origine | Statut | Présent onglet Ventes ? | Utilisé front/card ? | Commentaire |
| --------------------- | --------------- | ----------- | ---------------- | ------ | ------------------------ | -------------------- | ----------- |
| Accroche courte e-commerce | `description_ecommerce` | `product.template` | `website_sale` | Standard module installé | **Oui** (`ck_ecommerce_description`) | Oui | **Non créé par CK.** Phrase lead zone achat fiche produit (`product_page_details._purchase_lead_plain`). |
| Description e-commerce (libellé historique) | `description_ecommerce` | `product.template` | `website_sale` | Standard module installé | **Oui** | Oui | Même champ — bloc renommé « Accroche e-commerce » MOA. |
| Résumé card | — | — | — | — | Non | Non | Les cards n’utilisent **pas** `description_ecommerce` ; meta = tags + format + prix réf. |

---

## 6. Description longue produit

| Information métier CK | Champ technique | Modèle Odoo | Module d’origine | Statut | Présent onglet Ventes ? | Utilisé front/card ? | Commentaire |
| --------------------- | --------------- | ----------- | ---------------- | ------ | ------------------------ | -------------------- | ----------- |
| Description longue web | `website_description` | `product.template` | `website_sale` | Standard module installé | Non | Oui | Onglet **Ventes** standard (hors vue CK replace) ou **Site web**. Parsée en sections Lot 2 fiche (`product_page_details`). |
| Description interne | `description` | `product.template` | `product` | Standard Odoo | Non | Non | Notes internes produit — onglet Général. |
| Description vente / notes documents | `description_sale` | `product.template` | `sale` | Standard module installé | **Oui** (`ck_commercial_documents`) | Partiel | Bloc « Notes commerciales ». **Fallback front actif** si `website_description` vide (voir `NOTE_CLARIFICATION_PARSER_WEBSITE_DESCRIPTION_CK_V1.md`) — à ne pas utiliser ; suppression recommandée (Option B). |
| Usage conseillé | contenu dans `website_description` | `product.template` | Contenu éditorial | À arbitrer MOA | Non | Oui | Extrait `<strong>Usage :</strong>` ou section h3 Usage. **Gabarit HTML** : voir `NOTE_CLARIFICATION_PARSER_WEBSITE_DESCRIPTION_CK_V1.md`. |
| Moment de consommation | contenu dans `website_description` | — | Contenu éditorial | À arbitrer MOA | Non | Partiel | Pas de champ dédié — texte libre V1. |
| Goût / texture | contenu dans `website_description` | — | Contenu éditorial | À arbitrer MOA | Non | Partiel | Idem. |
| Conseil CK | contenu dans `website_description` | — | Contenu éditorial | À arbitrer MOA | Non | Partiel | Sections structurées `ck-product-enrich` (bootstrap hooks). |

---

## 7. Composition, conservation et informations réglementaires

| Information métier CK | Champ technique | Modèle Odoo | Module d’origine | Statut | Présent onglet Ventes ? | Utilisé front/card ? | Commentaire |
| --------------------- | --------------- | ----------- | ---------------- | ------ | ------------------------ | -------------------- | ----------- |
| Ingrédients | section `website_description` | `product.template` | Contenu éditorial | À arbitrer MOA | Non | Oui | Parser h3 « Ingrédients & allergènes ». |
| Allergènes | section `website_description` | — | Contenu éditorial | À arbitrer MOA | Non | Oui | Idem — pas de champ structuré V1. |
| DDM / DLC | lots / `expiration_date` | `stock.lot` etc. | `stock` (si installé) | À arbitrer MOA | Non | Non | Hors périmètre fiche produit Ventes CK. |
| Conservation avant ouverture | section `website_description` | — | Contenu éditorial | À arbitrer MOA | Non | Oui | Section Conservation parsée. |
| Conservation après ouverture | section `website_description` | — | Contenu éditorial | À arbitrer MOA | Non | Oui | Sous-titres Avant/Après ouverture. |
| Pays / territoire fabrication | attribut / tags / fournisseur | — | Configuration | À arbitrer MOA | Non | Partiel | Attribut Origine ou tags géographiques. |
| Mentions réglementaires | `website_description` / documents | `product.document` | Contenu éditorial | À arbitrer MOA | Non | Partiel | Documents produit `product_document_ids` (nutrition via nom fichier). |
| Valeurs nutritionnelles | document produit | `product.document` | Standard + parsing CK | À arbitrer MOA | Non | Partiel | Lien si document nommé « nutrition ». |

---

## 8. Galerie e-commerce

| Information métier CK | Champ technique | Modèle Odoo | Module d’origine | Statut | Présent onglet Ventes ? | Utilisé front/card ? | Commentaire |
| --------------------- | --------------- | ----------- | ---------------- | ------ | ------------------------ | -------------------- | ----------- |
| Image principale produit | `image_1920` | `product.template` | `product` | Standard Odoo | Non | Oui | Hors bloc galerie — onglet Général. |
| Galerie e-commerce | `product_template_image_ids` | `product.template` | `website_sale` | Standard module installé | **Oui** (`ck_ecommerce_media`) | Partiel | Modèle `product.image`. Médias complémentaires site. |
| Images complémentaires | `product_template_image_ids` | `product.template` | `website_sale` | Standard module installé | **Oui** | Partiel | Kanban « Ajouter un média ». |
| Images variantes | `image_variant_1920` | `product.product` | `product` | Standard Odoo | Non | Oui | Fiche variante — prioritaire sur card si présente. |
| Vidéo produit | média embarqué | `website_description` / HTML | Hors V1 | Hors V1 | Non | Partiel | Possible via éditeur HTML ; pas de champ dédié V1. |

---

## 9. Recommandations produit

| Information métier CK | Champ technique | Modèle Odoo | Module d’origine | Statut | Présent onglet Ventes ? | Utilisé front/card ? | Commentaire |
| --------------------- | --------------- | ----------- | ---------------- | ------ | ------------------------ | -------------------- | ----------- |
| Produits optionnels | `optional_product_ids` | `product.template` | `sale` / `website_sale` | Standard module installé | **Oui** (`ck_product_recommendations`) | Partiel | Upsell panier / devis. Groupe `upsell` conservé. |
| Produits accessoires | `accessory_product_ids` | `product.template` | `sale` / `website_sale` | Standard module installé | **Oui** | Partiel | Cross-sell panier. |
| Produits alternatifs | `alternative_product_ids` | `product.template` | `website_sale` | Standard module installé | **Oui** | Partiel | Bas de fiche produit Odoo standard. |
| Conditionnements | `uom_ids` | `product.template` | `product` | Standard Odoo | **Oui** | Non | Libellé CK « Conditionnements ». Packagings Odoo. **Candidat futur bloc logistique.** |
| Produits complémentaires CK | = optionnels / accessoires | — | — | À arbitrer MOA | **Oui** | Partiel | Pas de champ CK dédié. |
| Collection associée | `public_categ_ids` | — | Configuration | À arbitrer MOA | **Oui** (catégories) | Partiel | Pas de M2M collection sur cette instance. |

---

## 10. Données de vente

| Information métier CK | Champ technique | Modèle Odoo | Module d’origine | Statut | Présent onglet Ventes ? | Utilisé front/card ? | Commentaire |
| --------------------- | --------------- | ----------- | ---------------- | ------ | ------------------------ | -------------------- | ----------- |
| Disponible à la vente | `sale_ok` | `product.template` | `sale` | Standard module installé | Non | Oui | Case onglet Général — conditionne visibilité vente. |
| Prix public | `list_price` | `product.template` | `product` | Standard Odoo | Non | Oui | Voir §4. |
| Taxes client | `taxes_id` | `product.template` | `account` | Standard module installé | Non | Oui | Onglet Comptabilité / Général. |
| Unité de mesure | `uom_id` | `product.template` | `uom` | Standard Odoo | Non | Oui | UDM vente principale. |
| Unité d’achat | `uom_po_id` | `product.template` | `purchase` | Standard Odoo | Non | Non | Si module `purchase` installé. |
| Variantes | `attribute_line_ids` | `product.template` | `product` | Standard Odoo | Non | Oui | Onglet **Attributs & variantes**. |
| Prix supplémentaire variante | `price_extra` | `product.template.attribute.value` | `product` | Standard Odoo | Non | Oui | Voir §4. |
| Listes de prix B2B | `item_ids` / pricelists | `product.pricelist` | `sale` | Standard module installé | Non | Partiel | Hors périmètre V1 B2C ; sync variante CK sur items `fixed`. |
| Devis / commandes | lignes `sale.order.line` | — | `sale` | Standard module installé | Non | Oui | Comportement Odoo standard. |

---

## 11. Données logistiques minimales

| Information métier CK | Champ technique | Modèle Odoo | Module d’origine | Statut | Présent onglet Ventes ? | Utilisé front/card ? | Commentaire |
| --------------------- | --------------- | ----------- | ---------------- | ------ | ------------------------ | -------------------- | ----------- |
| Poids | `weight` | `product.template` | `product` / `stock` | Standard Odoo | Non | Non | Onglet Inventaire / Expédition. |
| Volume | `volume` | `product.template` | `product` / `stock` | Standard Odoo | Non | Non | Idem. |
| Stock disponible | `qty_available` etc. | `product.product` | `stock` | Standard module installé | Non | Partiel | Smart button Stock — si `stock` installé. |
| Suivi stock | `tracking` | `product.template` | `stock` | Standard module installé | Non | Non | Onglet Inventaire. |
| Fournisseurs | `seller_ids` | `product.template` | `purchase` | Standard module installé | Non | Non | Si `purchase` installé. |
| Délai fournisseur | `delay` sur `supplierinfo` | `product.supplierinfo` | `purchase` | Standard module installé | Non | Non | Fiche fournisseur produit. |
| Conditionnements / packagings | `uom_ids` | `product.template` | `product` | Standard Odoo | **Oui** (Recommandations) | Non | Voir §9 — placement provisoire MOA. |
| Fragilité | — | — | — | À arbitrer MOA | Non | Non | Pas de champ standard identifié. |
| Durée de conservation | — / texte | — | À arbitrer MOA | Non | Partiel | Texte `website_description` V1. |
| Température / stockage | — | — | À arbitrer MOA | Hors V1 | Non | Non | — |

---

## 12. Notes commerciales

| Information métier CK | Champ technique | Modèle Odoo | Module d’origine | Statut | Présent onglet Ventes ? | Utilisé front/card ? | Commentaire |
| --------------------- | --------------- | ----------- | ---------------- | ------ | ------------------------ | -------------------- | ----------- |
| Notes commerciales | `description_sale` | `product.template` | `sale` | Standard module installé | **Oui** (`ck_commercial_documents`) | Partiel | Documents Odoo uniquement. Groupe `description` conservé. |
| Mention commerciale document | `description_sale` | `product.template` | `sale` | Standard module installé | **Oui** | Non | Distinct de l’accroche e-commerce. |
| Réserve commerciale | `description_sale` | `product.template` | `sale` | Standard module installé | **Oui** | Non | Même champ — usage métier à cadrer en saisie. |

---

## Champs spécifiques CK — récapitulatif

| Champ technique | Modèle | Module | BO (onglet Ventes) | Front / card |
| --------------- | ------ | ------ | -------------------- | ------------ |
| `ck_net_quantity` | `product.template` | `dorevia_ck_marketone_content` | `ck_card_reference_price` | Meta card · prix réf. |
| `ck_net_quantity_uom_id` | `product.template` | `dorevia_ck_marketone_content` | `ck_card_reference_price` | Idem |
| `ck_show_reference_price` | `product.template` | `dorevia_ck_marketone_content` | `ck_card_reference_price` | Idem |
| `ck_reference_price_uom_id` | `product.template` | `dorevia_ck_marketone_content` | `ck_card_reference_price` | Idem |
| `dorevia.ck.card.uom` | modèle support | `dorevia_ck_marketone_content` | Menu config CK | Référentiel unités card |

**Méthodes CK (pas des champs)** :

| Méthode | Usage |
|---------|-------|
| `get_ck_shop_card_metadata_line(variant)` | Ligne meta card Boutique |
| `get_ck_product_page_detail_sections()` | Sections longues fiche produit Lot 2 |

---

## Informations métier CK non couvertes par un champ dédié (V1)

| Information | Recommandation MOA V1 |
|-------------|----------------------|
| Marque | Rester sans champ ; arbitrer si besoin catalogue |
| Producteur visible | Fournisseur (`seller_ids`) ou contenu éditorial |
| Origine structurée | Attribut produit « Origines » | `ck_product_origin.py` — card, fiche, filtre shop natif |
| Ingrédients / allergènes structurés | `website_description` V1 ; champs dédiés = arbitrage post-V1 |
| Fragilité / température stockage | Note interne ou description longue |
| Collection commerciale dédiée | Catégories e-commerce + tags |
| Résumé card textuel | Non requis — meta = origine (attribut) + tags transversaux + format + prix réf. |

---

## Règle origine géographique vs étiquettes produit (juin 2026)

> **Origine géographique** : source de référence = attribut produit **« Origines »**.
> Les étiquettes produit (`product_tag_ids`, `additional_product_tag_ids`) ne doivent plus porter l'origine géographique ; elles sont réservées aux **tags transversaux**.

| Type | Exemples autorisés en tag | Exemples à ne plus porter par tag |
|------|---------------------------|-----------------------------------|
| Transversal | Épicerie, Artisanal, Coup de cœur, Nouveau, Sélection CK, Sans alcool, Idée cadeau | — |
| Géographique | — (attribut « Origines ») | Guadeloupe, Martinique, Réunion, Guyane, Haïti, Sainte-Lucie, Dominique |

**Implémentation** : `ck_product_origin.py` — helper partagé card (`home_featured`) et fiche (`product_page_details`).

**Fallback temporaire (Option A MOA)** : si l'attribut est vide, la card peut encore lire une étiquette géographique existante pour éviter une régression visuelle sur les produits déjà saisis. Cible : Option B (attribut seul) après reprise de données.

---

## Héritages XML & XPath — contrôle

| Élément | Détail | Risque |
|---------|--------|--------|
| Vue CK Ventes | `//page[@name='sales']` `replace` — priorité 35 | Faible — point d’entrée unique |
| Groupe `upsell` | Conservé sous `ck_product_recommendations` | Faible — xpath `sale`/`website_sale` compatibles |
| Groupe `description` | Conservé sous `ck_commercial_documents` | Faible |
| Coquille `extra_info` | `invisible="1"` — compat xpath Marketone | Néant si module Marketone non installé |
| Champs masqués duplicate | `description_ecommerce` invisible dans `upsell` | Évite doublon formulaire |

**Module `dorevia_ckreyol_marketone`** : xpaths sur `extra_info` / `ecom_description` — **non chargé** sur instance CK Marketone seule.

---

## Mapping onglet Ventes CK → blocs

| Bloc `name` | Champs principaux |
|-------------|-------------------|
| `ck_publication_highlight` | `is_published`, `website_ribbon_id`, `website_sequence`, `website_id` |
| `ck_shop_classification` | `public_categ_ids`, `product_tag_ids` |
| `ck_card_reference_price` | `ck_net_quantity`, `ck_net_quantity_uom_id`, `ck_show_reference_price`, `ck_reference_price_uom_id` |
| `ck_ecommerce_description` | `description_ecommerce` |
| `ck_ecommerce_media` | `product_template_image_ids` |
| `ck_product_recommendations` | `uom_ids`, `optional_product_ids`, `accessory_product_ids`, `alternative_product_ids` |
| `ck_commercial_documents` | `description_sale` |

---

## Verdict Dev pour la MOA

| Question MOA | Réponse cartographie |
|--------------|---------------------|
| Champs suffisants en V1 ? | **Oui** pour publication B2C pilote — sous réserve données éditoriales dans `website_description`. |
| Description longue ? | Porter usage / conservation / ingrédients dans `website_description` en V1. |
| Configuration vs champs ? | Univers, vedettes, badges = catégories + rubans + tags. |
| Vrais manques à arbitrer ? | Marque, producteur visible, origine structurée, allergènes structurés, logistique avancée. |
| Reprise front fiche produit ? | **Possible après** validation de cette cartographie — aucun nouveau champ requis pour reprendre le design. |

**Décision MOA rappelée** : GO cartographie · front suspendu · aucun nouveau champ sans arbitrage explicite.

---

## Documents liés

- `NOTE_BO_PRODUIT_ONGLET_VENTES_CK_V1.md` — audit + validation réorganisation Ventes
- `maquette_01.2/NOTE_ARCHITECTURE_SECTION3_VEDETTES_V1.md` — cards Home Section 3
- Fiche produit BO type CK — V1 amendée (document MOA source)
