# Arbitrage V1 traduisible Odoo — Maquette CK V1.2.x

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Maquette source** | [`artifact/`](./artifact/) — 9 pages · verdict MOA OK |
| **Cadrage** | [`CADRAGE_MAQUETTE_CK_V1_2_X.md`](./CADRAGE_MAQUETTE_CK_V1_2_X.md) |
| **Recette QA** | [`recette_qa_maquette_v1_2_x.md`](./recette_qa_maquette_v1_2_x.md) |
| **Verdict maquette** | [`decision_moa_verdict_maquette_v1_2_x_vision_complete.md`](./decision_moa_verdict_maquette_v1_2_x_vision_complete.md) |
| **Thème / snippets** | [`ticket_dorevia_ck_theme_01`](../ticket_dorevia_ck_theme_01_socle_tokens_layout_snippets.md) |
| **Date** | 2026-06-13 |
| **Statut** | **Arbitrage acté · M1–M9 intégrés · guide opérationnel actif** |
| **Guide intégration** | [`GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md`](./GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md) |

```text
DOCUMENT D’ARBITRAGE DÉTAILLÉ — RÉFÉRENCE HISTORIQUE ET COMPLÉMENTAIRE
Pour l’intégration et la recette : utiliser GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md
GO exécution §5 acté · Phase 1 autorisée
```

> Objectif : construire une **V1 Odoo cohérente, maîtrisée et fidèle** à l’expérience CK validée — **sans traduire toute la maquette d’un coup**.

---

## 0. Lecture Odoo — légende

| Code | Signification |
|------|---------------|
| **Odoo standard** | Fonctionnalité native sans développement thème |
| **Snippet natif Odoo** | Snippet Website Builder standard (`s_title`, `s_features`, Dynamic Products…) |
| **Snippet CK thème** | Snippet `dorevia_ck_theme` (`s_ck_*`) |
| **`website_sale` natif** | Catalogue · fiche · panier · catégories e-commerce |
| **Page CMS** | Page Website Builder · contenu éditorial |
| **Formulaire `website_crm`** | Formulaire CRM natif sur page CMS |
| **Catégorie e-commerce** | `product.public.category` |
| **Attribut / tag produit** | Attributs variantes · tags · champs custom produit |
| **Champ produit** | Description · onglets · champs BO produit |
| **Configuration BO** | Menu · footer · paramètres website |
| **Réserve** | Arbitrage MOA requis avant implémentation |
| **Hors scope V1** | Non retenu en V1 |

**Complexité** : Faible · Moyenne · Élevée

**Décision MOA** : `À valider` · `Recommandé V1` · `Différer` · `Hors scope`

---

## 1. Transversal — toutes pages

| Page | Bloc | Rôle métier / UX | Classe | Choix V1 proposé | Traduction Odoo pressentie | Snippet / composant cible | Complexité | Réserve | Décision MOA |
|------|------|-------------------|--------|------------------|----------------------------|---------------------------|------------|---------|--------------|
| Toutes | Header | Navigation · recherche · panier · accès Pro | V1 prioritaire | Intégrer | Configuration BO + thème | Layout `dorevia_ck_theme` · menu Website | Faible | Menu catégories = liens BO réels | À valider |
| Toutes | Footer 4 col | Boutique · Découvrir · CK · liens légaux | V1 prioritaire | Intégrer | Configuration BO | Footer thème + menus footer | Faible | Liens fiche producteur = page CMS à créer | À valider |
| Toutes | Responsive 390 px | Lisibilité mobile · CTA touch | V1 prioritaire | Intégrer | Snippet CK thème | Tokens CSS thème CK | Moyenne | Recette mobile post-traduction | À valider |
| Toutes | Signal Pro discret | Qualification B2B sans portail | V1 prioritaire | Intégrer | Page CMS + lien menu | `/professionnels` · menu BO | Faible | Déjà partiellement en Odoo | À valider |

---

## 2. Accueil (`index.html`)

| Page | Bloc | Rôle métier / UX | Classe | Choix V1 proposé | Traduction Odoo pressentie | Snippet / composant cible | Complexité | Réserve | Décision MOA |
|------|------|-------------------|--------|------------------|----------------------------|---------------------------|------------|---------|--------------|
| Accueil | Hero | Promesse CK · CTA boutique · CTA Pro | V1 prioritaire | Intégrer | Snippet CK thème | `s_ck_hero` | Faible | Visuels réels à remplacer | Recommandé V1 |
| Accueil | Réassurance | 4 preuves confiance sous hero | V1 prioritaire | Intégrer | Snippet CK thème | `s_ck_reassurance` | Faible | Promesses logistiques à confirmer MOA | Recommandé V1 |
| Accueil | Produits vedettes ×6 | Coups de cœur · prix TTC · origine | V1 prioritaire | Intégrer | `website_sale` natif | Dynamic Products · `s_ck_featured_products` | Faible | Sélection produits BO | Recommandé V1 |
| Accueil | Catégories ×3 | Entrées univers commerciaux | V1 possible | Intégrer si simple | Catégorie e-commerce | `s_ck_category_links` · liens `/shop/category/…` | Moyenne | Dépend catégories BO structurées | À valider |
| Accueil | Coffret découverte | Pack cadeau · prix · CTA | V1 possible | Intégrer si produit existe | `website_sale` natif | Dynamic Products ou bloc CMS | Faible | Produit pack à créer en BO | À valider |
| Accueil | Bandeau Pro | Double cible · qualification | V1 prioritaire | Intégrer | Snippet CK thème | `s_ck_pro_banner` → `/professionnels` | Faible | — | Recommandé V1 |
| Accueil | **Bloc double Pro / newsletter** | B2B visible + relation continue | V1 prioritaire (Pro) · V1 possible (news) | Intégrer Pro · newsletter à arbitrer | Snippet CK thème · mass mailing | `s_ck_dual_engage` · [`note_reference`](./note_reference_bloc_double_pro_newsletter_ck.md) | Moyenne | Pas ton promo référence · RGPD newsletter | À valider |
| Accueil | Éditorial bas de page | Mission · liens à propos · producteur · recettes | V1 possible | Intégrer partiel | Page CMS | Blocs texte CMS · `oe_structure` | Faible | Liens vers pages Lot 3+ à créer | À valider |
| Accueil | SEO / structure | Ordre blocs note_05 | V1 prioritaire | Intégrer | Odoo standard | Composition home CMS | Faible | Ordre : hero → réassurance → produits → … | Recommandé V1 |

---

## 3. Shop (`shop.html`)

| Page | Bloc | Rôle métier / UX | Classe | Choix V1 proposé | Traduction Odoo pressentie | Snippet / composant cible | Complexité | Réserve | Décision MOA |
|------|------|-------------------|--------|------------------|----------------------------|---------------------------|------------|---------|--------------|
| Shop | En-tête catalogue | Titre · promesse · compteur produits | V1 prioritaire | Intégrer | `website_sale` natif | `/shop` · intro `s_ck_shop_intro` si disponible | Faible | Texte intro = CMS ou snippet | Recommandé V1 |
| Shop | Grille produits dense | Catalogue B2C · prix · origines | V1 prioritaire | Intégrer | `website_sale` natif | Grille native shop · thème CK | Faible | Attributs origine à structurer BO | Recommandé V1 |
| Shop | Collections pills | Entrées commerciales rapides | V1 possible | Intégrer si simple | Catégorie e-commerce | Liens catégories · pills CSS thème | Moyenne | Pas de filtre AJAX custom V1 | À valider |
| Shop | Filtres origine / famille | Pills visuels filtres | V1 possible | Différer | Attribut / tag produit | Attributs natifs shop (limités) | Élevée | Filtres maquette ≠ facettes Odoo natives ; simplification possible en V1.1 si natif suffisant | Différer |
| Shop | Tri select | Recommandés · prix | V1 possible | Intégrer natif | `website_sale` natif | Tri Odoo disponible | Faible | Options tri limitées vs maquette | À valider |
| Shop | Réassurance compacte | Logistique · paiement | V1 prioritaire | Intégrer | Snippet CK thème | `s_ck_reassurance` (variante compacte) | Faible | — | Recommandé V1 |
| Shop | Signal Pro mini | Lien qualification pro | V1 prioritaire | Intégrer | Page CMS | Lien `/professionnels` | Faible | — | Recommandé V1 |

---

## 4. Catégorie / collection (`categorie.html`)

| Page | Bloc | Rôle métier / UX | Classe | Choix V1 proposé | Traduction Odoo pressentie | Snippet / composant cible | Complexité | Réserve | Décision MOA |
|------|------|-------------------|--------|------------------|----------------------------|---------------------------|------------|---------|--------------|
| Catégorie | Breadcrumb | Fil d’Ariane navigation | V1 prioritaire | Intégrer | `website_sale` natif | Breadcrumb catégorie native | Faible | — | Recommandé V1 |
| Catégorie | Hero éditorial | Intro Épicerie créole | V1 possible | Intégrer | Page CMS | Description catégorie BO · `oe_structure` header | Faible | Texte éditorial par catégorie | À valider |
| Catégorie | Guide « Comment choisir ? » | Aide achat collection | V1 possible | Intégrer | Page CMS | Bloc texte dans header catégorie | Faible | Contenu éditorial BO | À valider |
| Catégorie | Grille produits filtrée | Produits de la collection | V1 prioritaire | Intégrer | Catégorie e-commerce | `product.public.category` · grille native | Faible | Catégorie Épicerie créole à créer BO | Recommandé V1 |
| Catégorie | Réassurance | 4 preuves | V1 prioritaire | Intégrer | Snippet CK thème | `s_ck_reassurance` | Faible | — | Recommandé V1 |
| Catégorie | Signal Pro | Lien discret espace pro | V1 prioritaire | Intégrer | Page CMS | Lien `/professionnels` | Faible | — | Recommandé V1 |

---

## 5. Fiche produit type (`fiche-produit.html`)

| Page | Bloc | Rôle métier / UX | Classe | Choix V1 proposé | Traduction Odoo pressentie | Snippet / composant cible | Complexité | Réserve | Décision MOA |
|------|------|-------------------|--------|------------------|----------------------------|---------------------------|------------|---------|--------------|
| Fiche produit | Galerie + achat | Prix · qty · panier · confiance mini | V1 prioritaire | Intégrer | `website_sale` natif | Fiche produit native · thème CK | Faible | — | Recommandé V1 |
| Fiche produit | Chips origine / famille | Aide décision · terroir | V1 prioritaire | Intégrer | Attribut / tag produit | Attributs · tags produit BO | Moyenne | Modèle attributs à définir | À valider |
| Fiche produit | Origine & usage | Terroir · saveur · texture · usages | V1 prioritaire | Intégrer | Champ produit | Description produit · onglets e-commerce | Faible | Structure description à standardiser | Recommandé V1 |
| Fiche produit | Bloc producteur (mini) | Lien confiance · atelier | V1 possible | Intégrer | Page CMS | Lien vers page CMS producteur | Moyenne | **Voir §10 arbitrage producteur** | À valider |
| Fiche produit | Conservation | Avant / après ouverture | V1 possible | Intégrer | Champ produit | Texte description ou attribut | Faible | — | À valider |
| Fiche produit | Signal B2B | Bandeau pro · CTA qualification | V1 prioritaire | Intégrer | Snippet CK thème | `s_ck_pro_banner` ou bloc CMS | Faible | — | Recommandé V1 |
| Fiche produit | Associations produits | 3 compléments | V1 différée | Différer | `website_sale` natif | Alternative / optional products Odoo | Moyenne | Natif partiel · pas prioritaire V1 | Différer |
| Fiche produit | Idée recette inline | Clafoutis goyavier | V1 différée | Différer | Page CMS | Lien page recettes · pas bloc fiche V1 | Faible | Renvoi vers page recettes statique | Différer |
| Fiche produit | Cross-sell | Vous aimerez aussi | V1 différée | Différer | `website_sale` natif | Dynamic Products zone `oe_structure` | Moyenne | — | Différer |

---

## 6. Professionnels (`professionnels.html`)

| Page | Bloc | Rôle métier / UX | Classe | Choix V1 proposé | Traduction Odoo pressentie | Snippet / composant cible | Complexité | Réserve | Décision MOA |
|------|------|-------------------|--------|------------------|----------------------------|---------------------------|------------|---------|--------------|
| Professionnels | Hero double entrée | Producteur / distributeur | V1 prioritaire | Intégrer | Page CMS | `s_title` + texte CMS | Faible | Page déjà partiellement composée Odoo | Recommandé V1 |
| Professionnels | Double cible ×2 cartes | Critères producteur vs distributeur | V1 prioritaire | Intégrer | Snippet natif Odoo | `s_features` 2 col | Faible | Odoo ✅ existant | Recommandé V1 |
| Professionnels | Process 3 étapes | Qualification · délais | V1 possible | Intégrer | Page CMS | Blocs texte · `s_process_steps` si thème | Faible | — | À valider |
| Professionnels | Réassurance pro | Logistique · relation · réseau | V1 possible | Intégrer | Snippet CK thème | `s_ck_reassurance` adapté | Faible | — | À valider |
| Professionnels | Formulaire CRM | Qualification lead B2B | V1 prioritaire | Intégrer | Formulaire `website_crm` | `s_website_form` · CRM natif | Faible | Odoo ✅ · recette soumission | Recommandé V1 |
| Professionnels | Note qualification | Pas commande B2B en ligne | V1 prioritaire | Intégrer | Page CMS | Texte CMS | Faible | — | Recommandé V1 |

---

## 7. À propos / démarche CK (`a-propos.html`)

| Page | Bloc | Rôle métier / UX | Classe | Choix V1 proposé | Traduction Odoo pressentie | Snippet / composant cible | Complexité | Réserve | Décision MOA |
|------|------|-------------------|--------|------------------|----------------------------|---------------------------|------------|---------|--------------|
| À propos | Hero mission | Pourquoi CK · pont créole / Europe | V1 prioritaire | Intégrer | Page CMS | `/a-propos` · `s_title` + lead | Faible | Page à créer BO | Recommandé V1 |
| À propos | Grille 4 cartes | Mission · sélection · producteurs · logistique | V1 prioritaire | Intégrer | Page CMS | `s_features` · blocs texte | Faible | — | Recommandé V1 |
| À propos | Engagements ×3 | Valeurs pont · origines · relation | V1 possible | Intégrer | Page CMS | `s_ck_reassurance` ou `s_features` | Faible | — | À valider |
| À propos | Signal Pro | Lien espace professionnel | V1 prioritaire | Intégrer | Page CMS | `s_ck_pro_banner` ou CTA | Faible | — | Recommandé V1 |
| À propos | CTA transverses | Boutique · fiche producteur · recettes | V1 prioritaire | Intégrer | Page CMS | Liens internes website | Faible | Pages cibles à créer | Recommandé V1 |

---

## 8. Fiche producteur type (`fiche-producteur.html`) — point sensible

| Page | Bloc | Rôle métier / UX | Classe | Choix V1 proposé | Traduction Odoo pressentie | Snippet / composant cible | Complexité | Réserve | Décision MOA |
|------|------|-------------------|--------|------------------|----------------------------|---------------------------|------------|---------|--------------|
| Fiche producteur | Hero producteur | Nom · territoire · visuel · tagline · CTA | V1 possible | Intégrer | Page CMS | Page CMS dédiée `/producteur/…` | Moyenne | **Option A recommandée** : 1 page CMS type · pas annuaire | À valider |
| Fiche producteur | Présentation éditoriale | Histoire · savoir-faire · territoire | V1 possible | Intégrer | Page CMS | Blocs texte · `s_image_text` | Faible | Option B fournisseur Odoo = réserve | À valider |
| Fiche producteur | Critères sélection CK | Pourquoi CK sélectionne | V1 possible | Intégrer si simple | Page CMS | Liste statique CMS | Faible | Pas de scoring auto V1 | À valider |
| Fiche producteur | **Produits proposés** | Grille cartes · lien achat | V1 prioritaire | Intégrer | `website_sale` natif | Dynamic Products filtré · liens produits BO | Moyenne | Lier produits via tags ou catégorie interne | Recommandé V1 |
| Fiche producteur | Sélection CK focus ×2 | Produits emblématiques · badges | V1 possible | Simplifier | `website_sale` natif | 2 blocs Dynamic Products ou CMS manuel | Moyenne | Peut fusionner avec grille produits | À valider |
| Fiche producteur | Usage / conseil | Recette · associations | V1 différée | Différer | Page CMS | Lien page recettes | Faible | Hors fiche producteur V1 minimale | Différer |
| Fiche producteur | Signal logistique CK | Rôle CK · distinction B2B | V1 prioritaire | Intégrer | Snippet CK thème | `s_ck_reassurance` + texte CMS | Faible | — | Recommandé V1 |
| Fiche producteur | CTA sortie | Shop · collection · Pro · proposer | V1 prioritaire | Intégrer | Page CMS | Liens CMS · contact · Pro | Faible | — | Recommandé V1 |

---

## 9. Recettes / savoirs (`recettes.html`)

| Page | Bloc | Rôle métier / UX | Classe | Choix V1 proposé | Traduction Odoo pressentie | Snippet / composant cible | Complexité | Réserve | Décision MOA |
|------|------|-------------------|--------|------------------|----------------------------|---------------------------|------------|---------|--------------|
| Recettes | Hero éditorial | Usages · transmission · cuisine créole | V1 possible | Intégrer | Page CMS | `/recettes` page statique | Faible | Pas blog V1 | À valider |
| Recettes | Grille 6 cartes | Recettes · guides · liens produits | V1 possible | Intégrer statique | Page CMS | Cartes manuelles · `s_card` / blocs image-texte | Moyenne | **Option A** : page CMS fixe · **Option B différée** : blog Odoo | À valider |
| Recettes | Liens catalogue | Fiche · shop · catégorie · producteur | V1 prioritaire | Intégrer | Odoo standard | Liens website internes | Faible | — | Recommandé V1 |
| Recettes | Réserve blog / forum | Garde-fou hors scope | Réserve | Ne pas intégrer | Hors scope V1 | — | — | Forum · commentaires · RSS = hors V1 | Hors scope |

---

## 10. Contact (`contact.html`)

| Page | Bloc | Rôle métier / UX | Classe | Choix V1 proposé | Traduction Odoo pressentie | Snippet / composant cible | Complexité | Réserve | Décision MOA |
|------|------|-------------------|--------|------------------|----------------------------|---------------------------|------------|---------|--------------|
| Contact | 4 parcours | Question produit · général · pro · proposer producteur | V1 prioritaire | Intégrer | Page CMS | Blocs texte + liens ancre / Pro | Faible | Pro → `/professionnels` · pas CRM contact | Recommandé V1 |
| Contact | Formulaire contact B2C | Nom · email · sujet · message | V1 prioritaire | Intégrer | Odoo standard | `/contactus` · formulaire website natif | Faible | Distinct formulaire CRM Pro | Recommandé V1 |
| Contact | Réassurance contact | Délai · données · renvoi Pro | V1 possible | Intégrer | Page CMS | Texte CMS | Faible | Délai 48 h = promesse MOA | À valider |
| Contact | **Bloc double Pro / newsletter** | Rappel B2B + inscription | V1 possible | Intégrer si M9 validé | Page CMS · mass mailing | Variante compacte | Faible | Doublon accueil si partout | À valider |
| Contact | Distinction Pro / B2C | Pas mélange formulaires | V1 prioritaire | Intégrer | Formulaire `website_crm` | Pro = page `/professionnels` séparée | Faible | — | Recommandé V1 |

---

## 11. Arbitrage spécifique — fiche producteur

La fiche producteur est **validée en maquette** et **stratégique pour la confiance CK**, mais **non triviale en Odoo V1**.

### Options MOA

| Option | Description | Avantages | Limites | Complexité | Recommandation Dev |
|--------|-------------|-----------|---------|------------|-------------------|
| **A — Page CMS producteur** | 1 page CMS par producteur mis en avant (type Atelier Les Hauts Goyaviers) | Fidèle maquette · éditorial · rapide · pas de dev module | Manuel · pas d’annuaire auto · duplication si N producteurs | Moyenne | **Recommandée V1** |
| **B — Champ / partner Odoo** | Réutiliser `res.partner` fournisseur · affichage limité | Données structurées · lien stock | Peu éditorial natif · pas de grille produits auto sans dev · risque portail | Élevée | Réserve · V1.5+ |
| **C — Hybride** | CMS éditorial + tag produit « producteur X » pour grille | Bon compromis catalogue | Nécessite convention tags BO | Moyenne | Possible si Option A retenue |
| **D — Annuaire multi-producteurs** | Listing + fiches dynamiques | Scalable | Hors garde-fous V1 · dev · portail | Élevée | **Hors scope V1** |

### Proposition V1

```text
Option A + C :
- 1 page CMS type fiche producteur (pilote : Atelier Les Hauts Goyaviers)
- Grille produits = Dynamic Products filtrés par tag / catégorie interne BO
- Bloc mini producteur sur fiche produit = lien vers page CMS
- Pas d’annuaire · pas de portail · pas d’espace connecté
```

**Décision MOA à prendre** : valider Option A (+ C) ou ouvrir étude Option B.

---

## 12. Synthèse MOA — périmètre V1 recommandé

### 12.1 V1 prioritaire recommandée

Pages et blocs à traduire en **premier lot Odoo** :

| Domaine | Éléments |
|---------|----------|
| **Home** | Header · hero · réassurance · produits vedettes · bandeau Pro · footer |
| **Commerce** | Shop natif · catégories · fiche produit achat · origines en attributs · breadcrumb |
| **B2B** | Page `/professionnels` · formulaire CRM · signal Pro transversal |
| **Confiance** | Page `/a-propos` · contact `/contactus` |
| **Producteur (minimal)** | 1 fiche CMS type · grille produits liés · bloc mini sur fiche produit |

**Ordre d’exécution suggéré** (cf. [`ticket_moa_composition_cms_ck_01`](../ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md)) :

```text
1. Header + footer (BO)
2. Home : hero → réassurance → produits → Pro
3. Shop + catégories BO
4. Fiche produit : achat + description enrichie + attributs origine
5. Page Pro + CRM (consolidation)
6. À propos + Contact
7. Fiche producteur CMS pilote + page recettes statique
8. Recette composition + mobile 390 px
```

### 12.2 V1 possible si simple

| Élément | Condition |
|---------|-----------|
| Catégories home pills | Si catégories BO prêtes |
| Coffret / pack home | Si produit pack existe |
| **Bloc dual Pro / newsletter** | Accueil · M9 · mass mailing Odoo |
| Hero + guide catégorie éditorial | Texte BO disponible |
| Filtres shop visuels | Uniquement si attributs natifs suffisants |
| Critères sélection CK (fiche producteur) | Texte statique CMS |
| Focus ×2 fiche producteur | Fusionnable avec grille produits |
| Page recettes statique 6 cartes | CMS manuel · pas blog |
| Process 3 étapes Pro | Texte CMS |

### 12.3 V1 différée

| Élément | Motif |
|---------|-------|
| Filtres shop interactifs avancés | Facettes · AJAX · custom |
| Associations / cross-sell fiche produit | Natif partiel · pas prioritaire |
| Recette inline fiche produit | Renvoi page recettes suffit V1 |
| Usage / conseil fiche producteur | Lien recettes |
| Blog multi-articles recettes | CMS statique suffit V1 |
| Annuaire multi-producteurs | Hors garde-fous |
| Module fournisseur Odoo natif (Option B) | Complexité · réserve |
| Automatisations CRM custom | Hors scope |

### 12.4 Réserves

| # | Réserve | Impact |
|---|---------|--------|
| R1 | Promesses logistiques (48–72 h · France/Europe) | Reformulation copy avant go-live |
| R2 | Routes Odoo `/shop/…` · catégories · produits | Mapping BO obligatoire |
| R3 | **Fiche producteur : CMS vs fournisseur Odoo** | Décision MOA §11 |
| R4 | Attributs origine / famille produit | Modèle BO à définir |
| R5 | Visuels Unsplash maquette | Assets réels avant recette finale |
| R6 | Page recettes : CMS statique vs blog natif | Arbitrage contenu |

### 12.5 Hors scope V1

```text
Portail B2B · checkout pro · catalogue parallèle
Annuaire partenaires · portail producteur · espace connecté
Page « Partenaires » générique
Blog complexe · forum · commentaires · RSS · communauté
Workflow custom · automation CRM au-delà du natif
Reprise intégrale automatique des 9 pages HTML
Filtres AJAX custom · moteur recherche custom
Pricing pro public · scoring producteur automatique
```

### 12.6 Points MOA à arbitrer avant GO Odoo

| # | Point | Options | Impact |
|---|-------|---------|--------|
| **M1** | Fiche producteur V1 | A CMS · B fournisseur · C hybride | Périmètre dev · contenu BO |
| **M2** | Page recettes V1 | CMS statique · blog limité · différer | Charge éditoriale |
| **M3** | Filtres shop V1 | Natifs seuls · visuels non cliquables · différer | UX catalogue |
| **M4** | Catégories home | 3 pills V1 ou différer | Dépend arborescence BO |
| **M5** | Promesses réassurance | Copy finale opérationnelle | Légal · SAV |
| **M6** | Périmètre lot 1 Odoo | Home seule vs Home+Shop vs vision complète V1 | Planning · risque |
| **M7** | Méthode traduction | Bloc par bloc CMS · pas big bang | Doctrine note_05 |
| **M8** | GO reprise Odoo | Décision explicite distincte du verdict maquette | Gouvernance |
| **M9** | Newsletter / bloc dual | Accueil seul · accueil+contact · différer · mass mailing Odoo | UX · RGPD · charge éditoriale |

---

## 13. Garde-fous — rappel

```text
Odoo 19 CE · Website Builder · snippets first · dorevia_ck_theme
Pas de surcouche autonome · pas de catalogue parallèle
Pas de panier/checkout custom · pas de logique B2B custom V1
```

Ce document **ne déclenche pas seul** la reprise Odoo — cf. [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) §5.

**GO Odoo acté** (2026-06-13) · Phase 1 autorisée · dictionnaire opérationnel : [`GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md`](./GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md).

Décisions M1–M9 : actées dans [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) §1.

---

## 14. Documents liés

| Document | Rôle |
|----------|------|
| [`CADRAGE_MAQUETTE_CK_V1_2_X.md`](./CADRAGE_MAQUETTE_CK_V1_2_X.md) | Cadrage lots · blocs · classes |
| [`TABLEAU_TRADUCTION_ODOO_V1_2.md`](./TABLEAU_TRADUCTION_ODOO_V1_2.md) | Tableau home V1.2 (historique) |
| [`decision_moa_verdict_maquette_v1_2_x_vision_complete.md`](./decision_moa_verdict_maquette_v1_2_x_vision_complete.md) | Verdict maquette · phase close |
| [`ticket_moa_composition_cms_ck_01`](../ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md) | Ticket composition CMS |
| [`recette_qa_composition_cms_ck_01.md`](../recette_qa_composition_cms_ck_01.md) | Recette post-traduction Odoo |
| [`GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md`](./GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md) | **Dictionnaire opérationnel Maquette ↔ Odoo** |
| [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) | Gouvernance · M1–M9 · GO exécution §5 · Phase 1 |
| [`note_05.md`](../../cadrage/note_05.md) | Doctrine · séquence opérationnelle |

---

## 15. Complément — bloc double Pro / newsletter

*Référence visuelle MOA · matérialisé en maquette complémentaire.*

| Page artifact | Statut |
|---------------|--------|
| Accueil | ✅ Bloc dual pleine largeur |
| Contact | ✅ Variante compacte |
| Professionnels | ✅ Variante compacte · CTA Pro → `#ck-pro-form` |
| Shop / footer global | ☐ Non matérialisé · à arbitrer |

Document détaillé : [`note_reference_bloc_double_pro_newsletter_ck.md`](./note_reference_bloc_double_pro_newsletter_ck.md)

Point MOA ajouté : **M9 — Newsletter V1** dans [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md).

**Verdict QA complément** : OK — desktop + mobile 390 px · mock newsletter · ton CK sans promo.

---
