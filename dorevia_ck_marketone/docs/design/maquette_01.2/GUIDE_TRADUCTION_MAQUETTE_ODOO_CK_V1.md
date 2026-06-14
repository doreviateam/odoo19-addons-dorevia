# Guide traduction Maquette ↔ Odoo — CK V1.2.x

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Rôle** | **Dictionnaire opérationnel** Maquette ↔ Odoo · intégration · recette |
| **Maquette source** | [`artifact/`](./artifact/) — 9 pages · V1 mature de référence |
| **Gouvernance** | [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) — M1–M9 + H1 actés |
| **Séquence** | [`SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md`](./SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md) |
| **Arbitrage détaillé** | [`ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md`](./ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md) |
| **Recette QA CE** | [`RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md`](./RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md) |
| **Date** | 2026-06-14 |
| **Statut** | **Phases 1–8 clôturées · Phase 9 Dev livrée · clôture MOA en attente** |

```text
USAGE : dictionnaire opérationnel Maquette ↔ Odoo
VÉRIFICATION CE : RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md
```

> La maquette V1.2.x est **mature de référence**, pas définitive. Traduction **bloc par bloc · par paliers · avec recette MOA/QA à chaque phase**.

---

## 0. Légende — colonne Action V1

| Action V1 | Signification |
|-----------|---------------|
| **Phase N · Intégrer** | Inclus V1 · à traduire en Phase N |
| **Phase N · En cours** | Palier actuellement autorisé MOA |
| **Conditionnel · Mx** | Intégrer si condition MOA remplie (ex. M4 BO prêtes · M9 simple) |
| **Différer · Mx** | Reporté V1 · réserve actée |
| **Hors scope V1** | Non retenu en V1 |
| **Consolidation** | Déjà partiellement en instance · aligner |

**Phases** : cf. [`SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md`](./SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md)

| Phase | Périmètre | GO MOA |
|-------|-----------|--------|
| **1** | Header + footer BO | ✅ **OK QA acté MOA** | — |
| **2** | Home sobre | ✅ **OK partiel QA · Q1 levée** | Phase 2 clôturée |
| 3 | Shop + catégorie | ✅ **Clôturée OK partiel maîtrisé** | Gate [`ck_phase3_ci.sh`](./scripts/ck_phase3_ci.sh) |
| 4 | Fiche produit | ✅ **Clôturée OK partiel MOA** | [`RECETTE_QA_PHASE4_FICHE_PRODUIT_CK_V1.md`](./RECETTE_QA_PHASE4_FICHE_PRODUIT_CK_V1.md) |
| 5 | Pro + CRM | ✅ **Clôturée OK partiel MOA** | [`RECETTE_QA_PHASE5_PRO_CRM_CK_V1.md`](./RECETTE_QA_PHASE5_PRO_CRM_CK_V1.md) |
| 6 | Contact + À propos | ✅ **Clôturée OK MOA** | [`RECETTE_QA_PHASE6_CONTACT_A_PROPOS_CK_V1.md`](./RECETTE_QA_PHASE6_CONTACT_A_PROPOS_CK_V1.md) |
| 7 | Fiche producteur CMS (M1) | ✅ **Clôturée OK partiel MOA** | [`RECETTE_QA_PHASE7_FICHE_PRODUCTEUR_CK_V1.md`](./RECETTE_QA_PHASE7_FICHE_PRODUCTEUR_CK_V1.md) |
| 8 | Recettes statiques (M2) | ✅ **Clôturée OK partiel MOA** | [`RECETTE_QA_PHASE8_RECETTES_STATIQUES_CK_V1.md`](./RECETTE_QA_PHASE8_RECETTES_STATIQUES_CK_V1.md) |
| 9 | Newsletter M9 simple | ✅ **Clôturée OK partiel MOA · 2026-06-14** | [`RECETTE_QA_PHASE9_NEWSLETTER_CK_V1.md`](./RECETTE_QA_PHASE9_NEWSLETTER_CK_V1.md) |
| 10 | Recette globale · go-live | 📋 **Dossier préparé** · recette MOA en attente | [`RECETTE_QA_PHASE10_GO_LIVE_CK_V1.md`](./RECETTE_QA_PHASE10_GO_LIVE_CK_V1.md) · §5undecies |

---

## 1. Transversal — toutes pages · header & navigation

> **Décision MOA H1** : cible **4 entrées** (`Boutique · Découvrir · Producteurs · Professionnels`). **Phase 1 livrée** : **3 entrées** (Producteurs absent — pas de CMS) · mega **Épicerie créole** seule (Packs différé · 0 produit publié).
>
> **Clarification post-Phases 7–8 (gouvernance actuelle)** :
> - Lien mega **`/recettes`** : **option post-recette MOA** — **hors périmètre strict Phase 8** (Phase 8 = page CMS `/recettes` uniquement).
> - Entrée nav **Producteurs** : **dette transverse / option post-recette** — non livrée Phase 1 · **hors Phase 8**.

### 1.1 Header — structure actée (H1)

| Page maquette | Bloc maquette | Rôle métier / UX | Traduction Odoo | Snippet / composant | Action V1 | Réserve |
|---------------|---------------|------------------|-----------------|---------------------|-----------|---------|
| Toutes | Header — barre principale | Navigation sobre · recherche · panier | Configuration BO + thème | `website.layout` · `dorevia_ck_theme` | **Phase 1 · Intégrer** | Consolidation menus doublons instance |
| Toutes | Entrée **Boutique** | Accès catalogue B2C | Lien menu | `/shop` | **Phase 1 · Intégrer** | — |
| Toutes | Entrée **Découvrir** | Découverte riche CK · remplace « Catégories » | **Mega-menu natif CE** | `is_mega_menu` · `mega_menu_content` | **Phase 1 · Intégrer** | Libellé **Découvrir** acté (pas Univers) |
| Toutes | Mega — Acheter par univers | 5 univers commerciaux | Liens catégories BO | `/shop/category/…` | Phase 1 · **Conditionnel M4** | Pas de liens fictifs |
| Toutes | Mega — Explorer par origine | Guadeloupe · Martinique · Réunion | Attributs / tags BO | Attributs produit | **Conditionnel** | Si BO prêtes · sinon différer colonne |
| Toutes | Mega — Comprendre et cuisiner | Recettes · usage · découverte | Liens CMS | `/recettes` · `/a-propos` | **Option post-recette MOA** | `/a-propos` livré Phase 6 · `/recettes` page Phase 8 · **lien mega hors Phase 8** |
| Toutes | Entrée **Producteurs** | Confiance · sélection CK | **Lien simple ou dropdown léger** | `website.menu` enfant | **Différer · option post-recette** | **Non livré Phase 1** · pas annuaire M1 · **hors Phase 8** |
| Toutes | Entrée **Professionnels** | Qualification B2B · accès rapide | **Lien direct** | `/professionnels` | **Phase 1 · Intégrer** | Pas sous-menu · pas friction |
| Toutes | Header mobile | Burger · accordéon | Natif offcanvas | Accordéon mega CE | **Phase 1 · Intégrer** | Recette 390 px obligatoire |
| Toutes | Style mega-menu CK | Typo · couleurs CK | CSS thème | `mega_menu_classes` · `.o_mega_menu` | Phase 1 · **Conditionnel** | CSS léger si natif insuffisant |

### 1.2 Transversal — autres blocs

| Page maquette | Bloc maquette | Rôle métier / UX | Traduction Odoo | Snippet / composant | Action V1 | Réserve |
|---------------|---------------|------------------|-----------------|---------------------|-----------|---------|
| Toutes | Footer 4 col | Boutique · Découvrir · CK · liens légaux | Configuration BO | Footer thème + menus footer | **Phase 1 · Intégrer** | Lien fiche producteur = page CMS Phase 7 |
| Toutes | Responsive 390 px | Lisibilité mobile · CTA touch | Tokens CSS thème CK | `dorevia_ck_theme` · recette mobile | Phase 10 · Intégrer | Recette post-traduction · mega accordéon |
| Toutes | Signal Pro discret | Qualification B2B sans portail | Page CMS + lien menu | `/professionnels` · menu BO | **Phase 1 · Consolidation** | Déjà partiellement en instance |

---

## 2. Accueil — `artifact/index.html`

| Page maquette | Bloc maquette | Rôle métier / UX | Traduction Odoo | Snippet / composant | Action V1 | Réserve |
|---------------|---------------|------------------|-----------------|---------------------|-----------|---------|
| Accueil | Hero | Promesse CK · CTA boutique · CTA Pro | Snippet CK thème | `s_ck_hero` | Phase 2 · Intégrer | Visuels réels à remplacer |
| Accueil | Réassurance | 4 preuves confiance sous hero | Snippet CK thème | `s_ck_reassurance` | Phase 2 · Intégrer | **M5** · copy opérationnelle avant go-live |
| Accueil | Produits vedettes — **5 CK réels en V1, cible 6 différée** | Coups de cœur · prix TTC · origine | Grille SSR stable · `website_sale` cartes | `s_ck_featured_products` + `.ck-featured-products__grid--stable` | Phase 2 · **Livré SSR** | **Réserve V1** : remplacement Dynamic Products / carousel — recette dédiée si réintroduction · voir RECETTE §6septies |
| Accueil | Catégories ×3 | Entrées univers commerciaux | Catégorie e-commerce | `s_ck_category_links` · `/shop/category/…` | **Conditionnel · M4** | Uniquement si catégories BO prêtes |
| Accueil | Coffret découverte | Pack cadeau · prix · CTA | `website_sale` natif | Dynamic Products ou bloc CMS | Conditionnel | Si produit pack existe en BO |
| Accueil | Bandeau Pro | Double cible · qualification | Snippet CK thème | `s_ck_pro_banner` → `/professionnels` | Phase 2 · Intégrer | — |
| Accueil | Bloc dual Pro / newsletter | B2B visible + relation continue | Snippet CK · `website_mass_mailing` | `s_newsletter_subscribe_form` dans dual CMS | **Phase 2 · Livré** | **M9** · recontrôle Phase 9 · **pas modification home Phase 9** |
| Accueil | Éditorial bas de page | Mission · liens à propos · producteur · recettes | Page CMS | Blocs texte · `oe_structure` | Phase 2 · partiel | Liens vers pages Phases 6–8 |
| Accueil | SEO / ordre blocs | Structure home note_05 | Composition CMS | Ordre blocs Website Builder | Phase 2 · Intégrer | hero → réassurance → produits → … |

---

## 3. Shop — `artifact/shop.html`

| Page maquette | Bloc maquette | Rôle métier / UX | Traduction Odoo | Snippet / composant | Action V1 | Réserve |
|---------------|---------------|------------------|-----------------|---------------------|-----------|---------|
| Shop | En-tête catalogue | Titre · promesse · compteur produits | `website_sale` natif | `/shop` · `s_ck_shop_intro` si disponible | Phase 3 · Intégrer | Texte intro = CMS ou snippet |
| Shop | Grille produits dense | Catalogue B2C · prix · origines | `website_sale` natif | Grille native shop · thème CK | Phase 3 · Intégrer | Attributs origine BO |
| Shop | Collections pills | Entrées commerciales rapides | Catégorie e-commerce | Liens catégories · pills CSS thème | Phase 3 · Intégrer | Pas filtre AJAX |
| Shop | Filtres origine / famille | Pills visuels filtres | — | Attributs natifs shop (limités) | **Différer · M3** | Pas AJAX · pas search custom |
| Shop | Tri select | Recommandés · prix | `website_sale` natif | Tri Odoo disponible | Phase 3 · Intégrer | Options tri limitées vs maquette |
| Shop | Réassurance compacte | Logistique · paiement | Snippet CK thème | `s_ck_reassurance` (variante compacte) | Phase 3 · Intégrer | **M5** copy |
| Shop | Signal Pro mini | Lien qualification pro | Page CMS | Lien `/professionnels` | Phase 3 · Intégrer | — |

---

## 4. Catégorie — `artifact/categorie.html`

| Page maquette | Bloc maquette | Rôle métier / UX | Traduction Odoo | Snippet / composant | Action V1 | Réserve |
|---------------|---------------|------------------|-----------------|---------------------|-----------|---------|
| Catégorie | Breadcrumb | Fil d’Ariane navigation | `website_sale` natif | Breadcrumb catégorie native | Phase 3 · Intégrer | — |
| Catégorie | Hero éditorial | Intro Épicerie créole | Page CMS | Description catégorie BO · `oe_structure` header | Phase 3 · Intégrer | Texte éditorial par catégorie |
| Catégorie | Guide « Comment choisir ? » | Aide achat collection | Page CMS | Bloc texte header catégorie | Phase 3 · Intégrer | Contenu éditorial BO |
| Catégorie | Grille produits filtrée | Produits de la collection | Catégorie e-commerce | `product.public.category` · grille native | Phase 3 · Intégrer | Catégorie BO à créer |
| Catégorie | Réassurance | 4 preuves | Snippet CK thème | `s_ck_reassurance` | Phase 3 · Intégrer | **M5** |
| Catégorie | Signal Pro | Lien discret espace pro | Page CMS | Lien `/professionnels` | Phase 3 · Intégrer | — |

---

## 5. Fiche produit — `artifact/fiche-produit.html`

> **Phase 4 clôturée OK partiel MOA** · lien producteur (Phase 4.3) et recette inline **différés** · producteur pilote livré Phase 7.

| Page maquette | Bloc maquette | Rôle métier / UX | Traduction Odoo | Snippet / composant | Action V1 | Réserve |
|---------------|---------------|------------------|-----------------|---------------------|-----------|---------|
| Fiche produit | Galerie + achat | Prix · qty · panier · confiance mini | `website_sale` natif | Fiche produit native · thème CK | Phase 4 · Intégrer | — |
| Fiche produit | Chips origine / famille | Aide décision · terroir | Attribut / tag produit | Attributs · tags produit BO | Phase 4 · Intégrer | Modèle attributs à définir |
| Fiche produit | Origine & usage | Terroir · saveur · texture · usages | Champ produit | Description · onglets e-commerce | Phase 4 · Intégrer | Structure description à standardiser |
| Fiche produit | Bloc producteur (mini) | Lien confiance · atelier | Page CMS | Lien fiche producteur M1 | Phase 4 · **Conditionnel** | Uniquement si cible CMS réelle · sinon différer |
| Fiche produit | Conservation | Avant / après ouverture | Champ produit | Texte description ou attribut | Phase 4 · Intégrer | — |
| Fiche produit | Signal B2B | Bandeau pro · CTA qualification | Snippet CK thème | `s_ck_pro_banner` ou bloc CMS | Phase 4 · Intégrer | — |
| Fiche produit | Associations produits | 3 compléments | `website_sale` natif | Alternative / optional products | **Différer** | Natif partiel · pas prioritaire V1 |
| Fiche produit | Idée recette inline | Clafoutis goyavier | Page CMS | Lien page recettes | **Différer · M2** | Renvoi page recettes suffit |
| Fiche produit | Cross-sell | Vous aimerez aussi | `website_sale` natif | Dynamic Products `oe_structure` | **Différer** | — |

---

## 6. Professionnels — `artifact/professionnels.html`

> **Phase 5 clôturée OK partiel MOA** — bootstrap portable · M9 bloc dual **différé Phase 9**.

| Page maquette | Bloc maquette | Rôle métier / UX | Traduction Odoo | Snippet / composant | Action V1 | Réserve |
|---------------|---------------|------------------|-----------------|---------------------|-----------|---------|
| Professionnels | Hero double entrée | Producteur · fournisseur · distributeur · boutique | Page CMS | `s_title` + texte CMS | **Phase 5 · Consolidation** | Déjà partiellement composée |
| Professionnels | Double cible ×2 cartes | Critères par profil B2B | Snippet natif Odoo | `s_features` 2 col | **Phase 5 · Consolidation** | Existant instance |
| Professionnels | Process 3 étapes | Qualification · délais | Page CMS | Blocs texte · `s_process_steps` | **Phase 5 · Intégrer** | Simplification V1 possible |
| Professionnels | Réassurance pro | Logistique · relation · réseau | Snippet CK thème | `s_ck_reassurance` adapté | **Phase 5 · Intégrer** | **M5** |
| Professionnels | Formulaire CRM | Qualification lead B2B | Formulaire `website_crm` | `s_website_form` · `#ck-pro-form` · CRM natif | **Phase 5 · Consolidation** | Recette soumission CRM · pas champ custom |
| Professionnels | Note qualification | Pas commande B2B en ligne | Page CMS | Texte CMS | **Phase 5 · Intégrer** | — |
| Professionnels | Bloc dual compact | Pro + newsletter variante | Page CMS · mass mailing | Variante M9 · CTA → `#ck-pro-form` | **Phase 9 · Intégré** | **M9** |

---

## 7. À propos — `artifact/a-propos.html`

> **Phase 6 clôturée OK MOA** · `/a-propos` livrée · lien producteur **livré Phase 7** · lien recettes **différé Phase 8** (option CTA post-recette).

| Page maquette | Bloc maquette | Rôle métier / UX | Traduction Odoo | Snippet / composant | Action V1 | Réserve |
|---------------|---------------|------------------|-----------------|---------------------|-----------|---------|
| À propos | Hero mission | Pourquoi CK · pont créole / Europe | Page CMS | `/a-propos` · `ck-about-page` · `s_title` + lead | **Phase 6 · Intégrer** | Page à créer BO |
| À propos | Grille 4 cartes | Mission · sélection · producteurs · logistique | Page CMS | `s_features` · blocs texte | **Phase 6 · Intégrer** | Simplifier si besoin V1 |
| À propos | Engagements ×3 | Valeurs pont · origines · relation | Page CMS | `s_ck_reassurance` ou `s_features` | **Phase 6 · Intégrer** | **M5** |
| À propos | Signal Pro | Lien espace professionnel | Page CMS | Lien `/professionnels` | **Phase 6 · Intégrer** | — |
| À propos | CTA transverses | Boutique · Pro · Contact | Page CMS | `/shop` · `/professionnels` · `/contactus` | **Phase 6 · Intégrer** | Pas recettes/producteur Phase 6 |
| À propos | CTA recettes · producteur | Découverte éditoriale | Page CMS | Liens internes | **Différer · option post-recette** | Producteur pilote Phase 7 · recettes Phase 8 · **pas lien mega Phase 8** |

---

## 8. Fiche producteur — `artifact/fiche-producteur.html` (M1)

> **Phase 7 clôturée OK partiel MOA · 2026-06-14** · route `/producteur/atelier-hauts-goyaviers` · produits via liens BO publiés.

| Page maquette | Bloc maquette | Rôle métier / UX | Traduction Odoo | Snippet / composant | Action V1 | Réserve |
|---------------|---------------|------------------|-----------------|---------------------|-----------|---------|
| Fiche producteur | Hero producteur | Nom · territoire · visuel · tagline · CTA | Page CMS | `/producteur/atelier-hauts-goyaviers` · `ck-producer-page` | **Phase 7 · Intégrer** | **M1** · 1 fiche pilote |
| Fiche producteur | Présentation éditoriale | Histoire · savoir-faire · territoire | Page CMS | Blocs texte · `s_image_text` | **Phase 7 · Intégrer** | Option B fournisseur = hors scope |
| Fiche producteur | Critères sélection CK | Pourquoi CK sélectionne | Page CMS | Liste statique CMS | **Phase 7 · Intégrer** | Pas scoring auto |
| Fiche producteur | Produits proposés | Grille cartes · lien achat | `website_sale` / CMS | Dynamic Products ou cartes manuelles | **Phase 7 · Conditionnel** | Si tag BO · sinon CMS sobre |
| Fiche producteur | Sélection CK focus ×2 | Produits emblématiques | `website_sale` / CMS | Fusionnable grille principale | **Phase 7 · Simplifier** | Option V1 |
| Fiche producteur | Usage / conseil | Recette · associations | Page CMS | Lien page recettes | **Différer · Phase 8** | Hors fiche minimale V1 |
| Fiche producteur | Signal logistique CK | Rôle CK · distinction B2B | Snippet CK thème | `s_ck_reassurance` + texte CMS | **Phase 7 · Intégrer** | **M5** |
| Fiche producteur | CTA sortie | Shop · contact · Pro | Page CMS | `/shop` · `/contactus` · `/professionnels` | **Phase 7 · Intégrer** | — |
| Fiche producteur | Lien depuis fiche produit | Mini bloc confiance | Fiche produit Phase 4 | Lien CMS | **Hors scope Phase 7** | Phase 4.3 différé |

---

## 9. Recettes — `artifact/recettes.html` (M2)

> **Phase 8 clôturée OK partiel MOA · 2026-06-14** · page CMS `/recettes` livrée · pas modification header/mega.

| Page maquette | Bloc maquette | Rôle métier / UX | Traduction Odoo | Snippet / composant | Action V1 | Réserve |
|---------------|---------------|------------------|-----------------|---------------------|-----------|---------|
| Recettes | Hero éditorial | Usages · transmission · cuisine créole | Page CMS | `/recettes` page statique | **Phase 8 · Intégré** | **M2** · pas blog V1 |
| Recettes | Grille 6 cartes | Recettes · guides · liens produits | Page CMS | Cartes manuelles · `s_card` / image-texte | **Phase 8 · Intégré** | CMS manuel · pas moteur éditorial |
| Recettes | Liens catalogue | Fiche · shop · catégorie · producteur | Odoo standard | Liens website internes | **Phase 8 · Intégré** | — |
| Recettes | Blog / forum / commentaires | Garde-fou hors scope | — | — | **Hors scope V1** | Pas contribution utilisateur |

---

## 10. Contact — `artifact/contact.html`

> **Phase 6 clôturée OK MOA** · `/contactus` consolidé · O1 résolu · bloc dual M9 **pressenti Phase 9 §5decies**.

| Page maquette | Bloc maquette | Rôle métier / UX | Traduction Odoo | Snippet / composant | Action V1 | Réserve |
|---------------|---------------|------------------|-----------------|---------------------|-----------|---------|
| Contact | 4 parcours | Question produit · général · pro · proposer producteur | Page CMS | Blocs texte + liens · Pro → `/professionnels` | **Phase 6 · Intégrer** | Pro distinct CRM · producteur différé Phase 7 |
| Contact | Formulaire contact B2C | Nom · email · sujet · message | Odoo standard | `/contactus` · formulaire website natif | **Phase 6 · Intégrer** | Distinct formulaire CRM Pro |
| Contact | Réassurance contact | Délai · données · renvoi Pro | Page CMS | Texte CMS | **Phase 6 · Intégrer** | Délai = promesse **M5** tenable |
| Contact | Nettoyage O1 | Retrait contenu démo Odoo corps page | Page CMS | Consolidation bootstrap | **Phase 6 · Consolidation** | O1 Phase 1 |
| Contact | Bloc dual Pro / newsletter | Rappel B2B + inscription | Page CMS · mass mailing | Variante compacte · `#ck-newsletter-subscribe` | **Phase 9 · Intégré** | **M9** |
| Contact | Distinction Pro / B2C | Pas mélange formulaires | Formulaire `website_crm` | Pro = `/professionnels` séparé | **Phase 6 · Intégrer** | — |

---

## 11. Index rapide — correspondances clés

| Bloc maquette | Traduction Odoo | Snippet / composant | Phase |
|---------------|-----------------|---------------------|-------|
| Hero accueil | Snippet CK thème | `s_ck_hero` | 2 |
| Réassurance | Snippet CK thème | `s_ck_reassurance` | 2 · 3 |
| Produits vedettes | Grille SSR stable (V1 · 5 produits) | `s_ck_featured_products` · `.ck-featured-products__grid--stable` | 2 · **carousel / Dynamic Products interdit V1** |
| Shop | Route native | `/shop` · `website_sale` | 3 |
| Catégorie | Catégorie e-commerce | `product.public.category` + header CMS optionnel | 3 |
| Fiche produit achat | Fiche native | `website_sale` | 4 |
| Origine / usage produit | Champ produit | Description · attributs · tags | 4 |
| Page Pro | Page CMS + CRM | `/professionnels` · `website_crm` · `s_website_form` | 5 |
| Fiche producteur | Page CMS pilote | `/producteur/atelier-hauts-goyaviers` · `ck-producer-page` | 7 |
| Recettes | Page CMS statique | `/recettes` · cartes manuelles | 8 |
| Newsletter dual | Mass mailing · subscribe natif | `s_newsletter_subscribe_form` · `/website_mass_mailing/subscribe` | 2 (home) · 9 (contact/pro) |
| Contact | Route native | `/contactus` + liens Pro | 6 |
| À propos | Page CMS | `/a-propos` · `ck-about-page` | 6 |
| Header / footer | Configuration BO | Menus · mega-menu natif | Phase **1** |

---

## 12. Décisions MOA → guide (rappel)

| # | Impact sur ce guide |
|---|---------------------|
| **M1** | §8 fiche producteur = CMS pilote · pas annuaire |
| **M2** | §9 recettes = CMS statique · pas blog |
| **M3** | §3 filtres shop = **Différer** |
| **M4** | §2 catégories home = **Conditionnel** |
| **M5** | Toutes réassurances · copy à valider avant go-live |
| **M6** | Périmètre complet maîtrisé · pas reprise intégrale HTML |
| **M7** | Un bloc = un levier Odoo · pas big bang |
| **M8** | GO par paliers · recette entre chaque phase |
| **M9** | §2 home dual livré · §10 contact + §5 pro dual **Phase 9** · newsletter simple · OK CE |
| **H1** | Cible 4 entrées · **Phase 1 livrée : 3 entrées** · mega Épicerie seule · `/recettes` mega et nav Producteurs = **option post-recette · hors Phase 8** |

---

## 13. Recette par palier

Après chaque phase :

| Contrôle | Attendu |
|----------|---------|
| Desktop 1280 px | Lisibilité · CTA · pas d’overflow |
| Mobile 390 px | Navigation · touch · ordre blocs |
| Navigation | Pas de 404 · liens BO valides |
| Non-régression | `/shop` · `/professionnels` · panier |
| Copy M5 | Promesses tenables (avant go-live final) |
| Verdict MOA/QA | **GO phase suivante** ou correction |

Recette référence : [`recette_qa_composition_cms_ck_01.md`](../recette_qa_composition_cms_ck_01.md)

---

## 14. Documents liés

| Document | Rôle |
|----------|------|
| [`note_reference_header_mega_menu_decouverte_ck_v1.md`](./note_reference_header_mega_menu_decouverte_ck_v1.md) | Header · mega-menu Découvrir · vérification CE |
| [`SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md`](./SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md) | Détail phases · tickets |
| [`ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md`](./ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md) | Arbitrage détaillé · options · réserves historiques |
| [`COMPOSITION_HEADER_V1_2.md`](./COMPOSITION_HEADER_V1_2.md) | Phase 1 header |
| [`RECETTE_QA_PHASE6_CONTACT_A_PROPOS_CK_V1.md`](./RECETTE_QA_PHASE6_CONTACT_A_PROPOS_CK_V1.md) | Recette Phase 6 · prérequis §5septies |
| [`RECETTE_QA_PHASE8_RECETTES_STATIQUES_CK_V1.md`](./RECETTE_QA_PHASE8_RECETTES_STATIQUES_CK_V1.md) | Recette Phase 8 · clôturée OK partiel MOA |
| [`RECETTE_QA_PHASE9_NEWSLETTER_CK_V1.md`](./RECETTE_QA_PHASE9_NEWSLETTER_CK_V1.md) | Recette Phase 9 · GO §5decies · Dev livrée |
| [`note_reference_bloc_double_pro_newsletter_ck.md`](./note_reference_bloc_double_pro_newsletter_ck.md) | Copy dual Pro/newsletter · M9 |
| [`COMPOSITION_PROFESSIONNELS_V1_2.md`](./COMPOSITION_PROFESSIONNELS_V1_2.md) | Capital Pro conservé |

---

*Guide traduction Maquette ↔ Odoo CK V1 — Phases 1–8 clôturées · Phase 9 Dev livrée · 2026-06-14.*
