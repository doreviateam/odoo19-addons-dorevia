# Tableau traduction Odoo — Maquette CK V1.2.x · Lot 1

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Maquette** | CK V1.2.x Lot 1 |
| **Livraison** | [`LIVRAISON_V1_2_X_LOT1.md`](./LIVRAISON_V1_2_X_LOT1.md) |
| **Cadrage** | [`CADRAGE_MAQUETTE_CK_V1_2_X.md`](./CADRAGE_MAQUETTE_CK_V1_2_X.md) |
| **Statut** | **Complété Dev Lot 1** — arbitrage MOA pending QA |

---

## Grille Accueil

| Bloc | Copy clé | Snippet CK / Odoo | Route / BO | Visuel | Classe | Réserve |
|------|----------|-------------------|------------|--------|--------|---------|
| Header | Boutique · Catégories · Pro | Layout thème + menu BO | `/shop` · `/professionnels` | Logo CK | V1 prioritaire | Odoo déjà aligné |
| Hero | Saveurs créoles · EU | `s_ck_hero` | `/shop` · `/professionnels` | Photo épicerie | V1 prioritaire | |
| Réassurance | 4 preuves confiance | `s_ck_reassurance` | Contenu BO | — | V1 prioritaire | |
| Produits vedettes | 6 produits · prix TTC | Dynamic Products | Produits publiés | Photos | V1 prioritaire | |
| Catégories | 3 univers | `s_ck_category_links` | `/shop/category/…` | — | V1 différée | Pages Lot 2 |
| Coffret | 29,90 € découverte | Dynamic Products / CMS | Catégorie packs | Photo pack | V1 possible | |
| Espace Pro | Double cible | `s_ck_pro_banner` | `/professionnels` | — | V1 prioritaire | |
| Éditorial | Mission CK | Blocs texte CMS | `oe_structure` | — | V1 possible | |
| Footer | Liens CK | Footer thème + BO | Menus | — | V1 prioritaire | |

---

## Grille Fiche produit (`fiche-produit.html`)

| Bloc | Snippet / Odoo | Classe | Réserve |
|------|----------------|--------|---------|
| Galerie + prix + panier | Fiche `website_sale` native | V1 prioritaire | |
| Origine · usage · saveur | Description / onglets produit | V1 prioritaire | |
| Producteur | CMS sous fiche ou champ fournisseur | V1 possible | Fiche fournisseur = réserve |
| Conservation | Attribut ou texte | V1 possible | |
| Associations | Alternative products | V1 différée | |
| Idée recette | Blog / page CMS | V1 différée | Hors fiche V1 |
| Signal B2B | Bloc CMS + lien Pro | V1 prioritaire | |
| Cross-sell | Dynamic Products | V1 différée | |

---

## Grille Professionnels (`professionnels.html`)

| Bloc | Snippet / Odoo | Classe | Réserve |
|------|----------------|--------|---------|
| Hero + double CTA | `s_title` + texte | V1 prioritaire | |
| Double cible 2 cartes | `s_features` 2 col | V1 prioritaire | Instance Odoo ✅ |
| Process 3 étapes | `s_text_block` / steps | V1 possible | Pas workflow custom |
| Réassurance pro | Adaptation `s_ck_reassurance` | V1 possible | |
| Formulaire CRM | `s_website_form` → `crm.lead` | V1 prioritaire | Instance Odoo ✅ |
| Note qualification | Texte CMS | V1 prioritaire | |

---

## Mobile Lot 1

| Page | Comportement | Statut Dev |
|------|--------------|------------|
| Accueil | Ordre note_05 · burger · 2 col trust | ✅ preview |
| Fiche produit | 1 col · CTA full | ✅ preview |
| Professionnels | Stack cartes · form 1 col | ✅ preview |

---

## Effets transverses

| Effet maquette | Reproductible Odoo ? | Classe |
|----------------|----------------------|--------|
| Hover cartes produit | CSS thème | V1 possible |
| Badges coup de cœur / nouveau | Tags produit / promo | V1 possible |
| Sticky header | Thème CK | V1 prioritaire ✅ |
| Visuels Unsplash | Médias BO produits | V1 prioritaire |
| Tags arbitrage (`.arbitrage-tag`) | Doc only — hors prod | hors scope |

---

*Tableau traduction Odoo · maquette CK V1.2.x Lot 1 · 2026-06-13.*
