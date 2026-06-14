# Tableau traduction Odoo — Maquette CK V1.2 · Home

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Maquette** | CK V1.2 — Boutique élégante |
| **Artefact** | [`artifact/index.html`](./artifact/index.html) |
| **GO MOA** | [`go_moa_maquette_01_2.md`](./go_moa_maquette_01_2.md) |
| **Date** | 2026-06-13 |
| **Statut** | **Complété — livraison Dev** |

---

## Grille de traduction par bloc

| Bloc maquette V1.2 | Zone / contenu maquette | Snippet CK / Odoo retenu | Alternative native | Route / données Odoo | Statut Dev |
|--------------------|-------------------------|--------------------------|--------------------|----------------------|------------|
| Header marchand | Logo CK · menu Boutique / Catégories / Professionnels · recherche · panier | Layout thème `dorevia_ck_theme` + menu BO | `website` navbar | `/shop` · `/professionnels` · menu Website | ✅ |
| Hero court | Promesse + CTA boutique + CTA Pro · visuel compact | `s_ck_hero` | Banner · Text-Image | `/shop` · `/professionnels` | ✅ |
| Réassurance | 4 preuves sous hero (livraison · paiement · producteurs · SAV) | `s_ck_reassurance` | Features · Columns | Contenu éditorial BO | ✅ |
| Produits vedettes | 6 cartes · prix · badges · CTA Voir | `s_ck_featured_products` + zone `oe_structure` | **Dynamic Products** · Products | Produits publiés · `website_sale` | ✅ |
| Catégories / univers | 3 cartes · routes explicites | `s_ck_category_links` | Links · pills · `s_product_list` | `product.public.category` · `/shop/category/…` | ✅ |
| Coffrets / packs | Bandeau coffret découverte | Section produits ou bloc CMS | Dynamic Products (filtre cat.) | Catégorie Packs & découvertes | ✅ |
| Espace Pro | Bandeau double cible · CTA Pro | `s_ck_pro_banner` | Texte + CTA | `/professionnels` · `website_crm` | ✅ |
| Éditorial / SEO | Texte marque bas de page | Blocs texte CMS | Text · Image-Text | Page accueil `oe_structure` | ✅ |
| Footer CK | Marque · liens boutique · contact · légal | Footer thème + contenu BO | — | Menus footer Website | ✅ |

---

## Mobile

| Bloc | Comportement mobile | Ordre respecté (note_05 §4) | Statut Dev |
|------|---------------------|----------------------------|------------|
| Hero | Grid 1 col · hero compact | 1. Hero | ✅ |
| Réassurance | Grille 2×2 | 2. Preuves | ✅ |
| Produits | Grille 1 col (<480px) · 2 col (tablet) | 3. Produits + prix | ✅ |
| Catégories | Cartes empilées | 4. Catégories | ✅ |
| Coffrets | Stack vertical | 5. (intégré avant Pro) | ✅ |
| Espace Pro | Bandeau stack · CTA full width | 6. Pro | ✅ |
| Éditorial | Texte bas | 7. Éditorial | ✅ |
| Footer | Colonnes empilées | 8. Footer | ✅ |

---

## Liens principaux maquette

| Lien | Route maquette | Odoo cible |
|------|----------------|------------|
| Boutique | `/shop` | `website_sale` catalogue |
| Catégories | `/shop/category/…` | `product.public.category` |
| Pro | `/professionnels` | Page CMS + CRM (à composer) |
| Voir produit | `/shop/{slug-id}` | Fiche produit native |
| Panier | `/shop/cart` | Panier natif |
| Contact | `/contactus` | Page contact Website |

---

*Tableau complété à la livraison Dev · maquette CK V1.2 · 2026-06-13.*
