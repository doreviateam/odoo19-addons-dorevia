# Cadrage maquette CK V1.2.x — Matérialisation vision · arbitrage traduction Odoo

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Décision MOA** | [`decision_moa_pause_odoo_iteration_maquette_v1_2_x.md`](./decision_moa_pause_odoo_iteration_maquette_v1_2_x.md) |
| **Brief base** | [`brief_01_2.md`](./brief_01_2.md) |
| **Artefact** | [`artifact/`](./artifact/) |
| **Recette QA** | [`recette_qa_maquette_v1_2_x.md`](./recette_qa_maquette_v1_2_x.md) · [`recette_qa_maquette_v1_2_x_lot2.md`](./recette_qa_maquette_v1_2_x_lot2.md) · [`recette_qa_maquette_v1_2_x_lot3.md`](./recette_qa_maquette_v1_2_x_lot3.md) |
| **Rapport MOA PDF** | [`rapport/RAPPORT_MOA_MAQUETTE_CK_V1_2_X_LOT1.pdf`](./rapport/RAPPORT_MOA_MAQUETTE_CK_V1_2_X_LOT1.pdf) |
| **Arbitrage V1 Odoo** | [`ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md`](./ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md) |
| **Livraison MOA** | [`LIVRAISON_MOA_MAQUETTE_CK_V1_2_X.md`](./LIVRAISON_MOA_MAQUETTE_CK_V1_2_X.md) |
| **Date** | 2026-06-13 |
| **Statut** | **M1–M9 actés** · GO préparation · séquence V1 préparée · **Odoo exécution en pause (§5)** |

---

## 0. Plan de lots MOA

| Lot | Pages | Statut |
|-----|-------|--------|
| **Lot 1** | Accueil enrichie · Fiche produit type · Professionnels maquette | **Recetté QA Lot 1.1 — OK** |
| **Lot 2** | Shop · Catégorie / collection | **Recetté QA — OK** |
| **Lot 3+** | À propos · Fiche producteur · Recettes/savoirs · Contact | **Recetté QA — OK** |

**Motif Lot 3+** : confiance · producteur · éditorial · contact — compléter la vision avant arbitrage traduction.

**Phase actuelle** : maquette **close** · arbitrage V1 préparé · **Odoo en pause** jusqu’à GO MOA explicite.

---

## 1. Périmètre pages

| # | Page | Fichier artifact | Statut maquette | Classe arbitrage | Réserve |
|---|------|------------------|-----------------|------------------|---------|
| 1 | Accueil | `index.html` | ✅ Lot 1 livré | V1 prioritaire | Visuels Unsplash · routes shop Lot 2 |
| 2 | Boutique / Shop | `shop.html` | ✅ Lot 2 livré | V1 prioritaire | Filtres = visuels maquette |
| 3 | Catégorie / collection type | `categorie.html` | ✅ Lot 2 livré | V1 prioritaire | Épicerie créole · route Odoo |
| 4 | Fiche produit type | `fiche-produit.html` | ✅ Lot 1 livré | V1 prioritaire (achat) · possible/différée (enrich.) | Producteur = réserve fiche Odoo |
| 5 | Professionnels | `professionnels.html` | ✅ Lot 1 livré | V1 prioritaire | Maquette UX enrichie · Odoo composé conservé |
| 6 | À propos / démarche CK | `a-propos.html` | ✅ Lot 3+ livré | V1 prioritaire | Page CMS · pas boutique exotique froide |
| 6b | Fiche producteur type | `fiche-producteur.html` | ✅ Lot 3+ livré | V1 possible | Pas annuaire · pas portail producteur |
| 7 | Recettes / savoirs / éditorial | `recettes.html` | ✅ Lot 3+ livré | V1 possible | Blog natif / articles = réserve |
| 8 | Contact / demande pro | `contact.html` | ✅ Lot 3+ livré | V1 prioritaire | `/contactus` · Pro → CRM · proposition producteur |

---

## 2. Concepts matérialisés (§6 décision MOA)

| Concept | Présent maquette | Pages concernées | Classe | Traduisibilité Odoo | Réserve |
|---------|------------------|------------------|--------|---------------------|---------|
| Promesse CK | ✅ | Accueil · éditorial | V1 prioritaire | `s_ck_hero` + CMS | |
| Double cible B2C / B2B | ✅ | Accueil · Pro · fiche signal | V1 prioritaire | `s_ck_pro_banner` · page CMS | Pas portail B2B |
| Producteurs / fournisseurs | ✅ | Accueil · Fiche produit · Fiche producteur · À propos | V1 possible | Page CMS fiche producteur · champ fournisseur Odoo = réserve | Pas annuaire partenaires V1 |
| Distributeurs brick & mortar | ✅ | Pro · Accueil | V1 prioritaire | Page CMS + CRM | |
| Logistique | ✅ | Accueil · réassurance · Pro | V1 prioritaire | `s_ck_reassurance` · texte CMS | |
| Origines | ✅ | Shop · catégorie · fiche | V1 prioritaire | Attributs / tags produit | |
| Collections commerciales | ✅ | Shop · catégorie · accueil | V1 prioritaire + possible | `product.public.category` | Pills = V1 possible |
| Fiche produit enrichie | ✅ | Fiche produit | V1 prioritaire + possible | Fiche native + `oe_structure` | Recette/assoc = différée |
| Éditorial / recettes | ✅ | Accueil · recettes · fiche recette | V1 possible | Page CMS statique · blog = réserve | Pas forum · pas commentaires |
| Réassurance | ✅ | Accueil · fiche mini | V1 prioritaire | `s_ck_reassurance` | |
| Confiance / démarche CK | ✅ | À propos | V1 prioritaire | Page CMS | |
| Contact B2C | ✅ | Contact | V1 prioritaire | `/contactus` natif | Distinct CRM Pro |
| UX mobile 390 px | ✅ QA | Toutes pages artifact | V1 prioritaire | Thème CK responsive | Lots 1 + 2 + 3+ sans overflow |

**Classes** : V1 prioritaire · V1 possible · V1 différée · réserve · hors scope · abandonné.

---

## 3. Blocs par page — Accueil (base V1.2)

| Bloc | Copy clé | Visuel | Mobile | Snippet Odoo pressenti | Classe |
|------|----------|--------|--------|----------------------|--------|
| Header | Boutique · Catégories · Pro | Logo CK | Burger 900px | menu BO + thème | V1 prioritaire |
| Hero | Saveurs créoles · livraison EU | Photo épicerie | Court 2:1 | `s_ck_hero` | V1 prioritaire |
| Réassurance | Livraison · paiement · producteurs · SAV | Icônes | 2×2 grid | `s_ck_reassurance` | V1 prioritaire |
| Produits | 6 coups de cœur · prix TTC | Photos produit | 1 col &lt;480px | Dynamic Products | V1 prioritaire |
| Catégories | 3 univers actionnables | — | 1 col | `s_ck_category_links` | V1 différée (pages Lot 2) |
| Coffret | Coffret découverte 29,90 € | Photo pack | Stack | CMS / Dynamic Products | V1 possible |
| Pro home | Double cible · qualification | — | Stack | `s_ck_pro_banner` | V1 prioritaire |
| Éditorial | Mission CK · fiches enrichies | — | Bas de page | blocs texte CMS | V1 possible |
| Footer | Marque · liens | — | 1 col | footer BO | V1 prioritaire |

---

## 4. Blocs par page — à compléter

### 4.1 Boutique / Shop

| Bloc | Description | Classe | Réserve |
|------|-------------|--------|---------|
| En-tête catalogue | Titre · promesse · compteur | V1 prioritaire | Native `/shop` |
| Collections pills | Entrées commerciales | V1 possible | Liens catégories Odoo |
| Filtres origine / famille | Pills visuels | V1 possible | Attributs · pas de JS custom V1 |
| Grille produits dense | 12 produits · prix · origine | V1 prioritaire | `website_sale` grid |
| Tri select | Recommandés · prix | V1 possible | Tri natif Odoo limité |
| Réassurance compacte | Logistique · paiement | V1 prioritaire | Snippet ou footer zone |
| Signal Pro mini | Lien qualification | V1 prioritaire | CMS |

### 4.2 Catégorie / collection

| Bloc | Description | Classe | Réserve |
|------|-------------|--------|---------|
| Breadcrumb | Accueil · shop · catégorie | V1 prioritaire | Native |
| Hero éditorial | Intro Épicerie créole | V1 possible | CMS header catégorie |
| Guide usage | Comment choisir | V1 possible | Texte CMS |
| Grille produits filtrée | 7 produits collection | V1 prioritaire | Catégorie Odoo |
| Réassurance | 4 preuves | V1 prioritaire | Snippet |
| Signal Pro | Discret | V1 prioritaire | Lien CMS |

### 4.3 Fiche produit

| Bloc | Description | Classe | Réserve |
|------|-------------|--------|---------|
| Galerie + achat | Prix · qty · panier · confiance | V1 prioritaire | Native `website_sale` |
| Origine & usage | Terroir · saveur · texture · usages | V1 prioritaire | Description produit / onglets |
| Producteur | Atelier · sélection CK | V1 possible | Fiche fournisseur Odoo = réserve |
| Conservation | Avant/après ouverture | V1 possible | Attribut ou texte CMS |
| Associations | 3 produits complémentaires | V1 différée | Alternative products Odoo |
| Idée recette | Clafoutis goyavier | V1 différée | Blog / CMS · hors fiche V1 |
| Signal B2B | Bandeau pro · CTA | V1 prioritaire | Snippet ou bloc CMS |
| Cross-sell | Vous aimerez aussi | V1 différée | Dynamic Products |

### 4.4 Professionnels

| Bloc | Description | Classe | Réserve |
|------|-------------|--------|---------|
| Hero double entrée | Producteur / distributeur | V1 prioritaire | `s_title` + CMS |
| Double cible | 2 cartes critères | V1 prioritaire | `s_features` 2 col · Odoo ✅ |
| Process 3 étapes | Qualification | V1 possible | Texte CMS |
| Réassurance pro | Logistique · relation · réseau | V1 possible | `s_ck_reassurance` adapté |
| Formulaire CRM | Qualification lead | V1 prioritaire | `s_website_form` · Odoo ✅ |
| Note qualification | Pas commande B2B | V1 prioritaire | Texte CMS |

### 4.5 À propos

| Bloc | Description | Classe | Réserve |
|------|-------------|--------|---------|
| Hero mission | Pont créole / Europe · confiance | V1 prioritaire | Page CMS `/a-propos` |
| Grille 4 cartes | Mission · sélection · producteurs · logistique | V1 prioritaire | Blocs texte CMS |
| Engagements | 3 valeurs (pont · origines · relation) | V1 possible | Snippet ou texte CMS |
| Signal Pro | Lien espace professionnel | V1 prioritaire | Lien CMS |
| CTA transverses | Boutique · recettes | V1 prioritaire | Liens relatifs |

### 4.6 Recettes / savoirs

| Bloc | Description | Classe | Réserve |
|------|-------------|--------|---------|
| Hero éditorial | Usages · transmission · cuisine créole | V1 possible | Page CMS statique |
| Grille 6 cartes | Recettes · guides · packs · sirops · sélection | V1 possible | Blog multi-articles = différée |
| Liens catalogue | Fiche · shop · catégorie · à propos | V1 prioritaire | Liens produits Odoo |
| Réserve explicite | Pas blog / forum / commentaires | réserve | Arbitrage blog Odoo vs CMS |

### 4.7 Contact

| Bloc | Description | Classe | Réserve |
|------|-------------|--------|---------|
| 3 parcours | Question produit · général · partenaire → Pro | V1 prioritaire | Distinction B2C / B2B |
| Formulaire mock | Nom · email · sujet · message | V1 prioritaire | `/contactus` natif Odoo |
| Réassurance | Délai · livraison · données · renvoi Pro | V1 possible | Texte CMS |
| Distinction Pro | CRM séparé | V1 prioritaire | Pas de mélange formulaires |

### 4.8 Fiche producteur type

| Bloc | Description | Classe | Réserve |
|------|-------------|--------|---------|
| Hero producteur | Nom · territoire · visuel · tagline · CTA produits / Pro | V1 possible | Page CMS · pas annuaire |
| Présentation éditoriale | Histoire · savoir-faire · territoire · raison CK | V1 possible | Texte CMS |
| Critères sélection CK | 6 critères (qualité · origine · cohérence · commercial · appro · compatibilité) | V1 possible | Texte statique · pas scoring auto |
| Produits proposés | Grille cartes · visuel · prix · origine · lien fiche | V1 prioritaire | Lien produits Odoo natifs |
| Sélection CK | 2 produits emblématiques · badges · usage | V1 possible | Mise en avant CMS |
| Usage / conseil | Recette · associations · renvoi recettes | V1 différée | Blog / CMS |
| Signal logistique CK | Sélection · disponibilité · Europe · distinction B2B | V1 prioritaire | Réassurance · pas portail |
| CTA sortie | Boutique · collection · Pro · proposer producteur | V1 prioritaire | Liens relatifs maquette |

**Phrase de référence MOA** : la fiche producteur dit « d’où ça vient, qui le fait, pourquoi CK l’a choisi, quels produits découvrir ».

---

## 5. Logique UX transversale

| Parcours | Point d’entrée | CTA | Destination | Statut |
|----------|----------------|-----|-------------|--------|
| Découverte B2C | Accueil | Voir boutique | `shop.html` | ✅ Lot 2 |
| Achat | Fiche produit | Ajouter panier | `/shop/cart` | ✅ |
| Catalogue | Shop | Catégorie | `shop.html` → `categorie.html` | ✅ Lot 2 |
| Qualification B2B | Shop / catégorie | Espace pro | `professionnels.html` | ✅ |
| Origine | Fiche | Chips Réunion / Antilles | Attributs produit | ✅ |
| Éditorial | Accueil / recettes | Recettes & savoirs | `recettes.html` | ✅ Lot 3+ |
| Confiance | Footer / fiche | À propos | `a-propos.html` | ✅ Lot 3+ |
| Producteur | Fiche produit · recettes | Fiche producteur type | `fiche-producteur.html` | ✅ Lot 3+ |
| Contact B2C | Footer / recettes | Contact | `contact.html` | ✅ Lot 3+ |
| Contact B2B | Contact / shop | Espace Pro | `professionnels.html` | ✅ |

---

## 6. Copy principale — registre

| Zone | Ton | Statut rédaction |
|------|-----|------------------|
| Promesse hero | Marchand · chaleureux · Europe | ✅ |
| Réassurance | Tenables MOA | ✅ |
| B2C | Prix · confiance · origine | ✅ |
| B2B signal | Qualification · pas portail | ✅ |
| Producteurs | Respect · sélection · pont | ✅ |
| Logistique | Fiable · transparent | ✅ |

---

## 7. Visuels nécessaires

| Zone | Type | Source | Statut |
|------|------|--------|--------|
| Hero | Photo ambiance épicerie | Unsplash | ✅ |
| Produits ×6 | Photos produit | Unsplash | ✅ |
| Coffret | Pack cadeau | Unsplash | ✅ |
| Fiche produit | Confiture + producteur | Unsplash | ✅ |
| Shop | Grille · filtres visuels | Unsplash | ✅ Lot 2 |
| Recettes ×6 | Cartes éditoriales | Unsplash | ✅ Lot 3+ |
| Fiche producteur | Hero · produits · focus | Unsplash | ✅ Lot 3+ |

---

## 8. Responsive — contrôles 390 px

| Page | Overflow | Ordre blocs | CTA touch | Statut QA |
|------|----------|-------------|-----------|-----------|
| Accueil | OK QA | Ordre note_05 | CTA touch OK | OK |
| Shop | OK QA | Grille 2 col mobile | OK | OK Lot 2 |
| Catégorie | OK QA | Intro puis produits | OK | OK Lot 2 |
| Fiche produit | OK QA | Achat puis enrich. | OK | OK — image principale corrigée Lot 1.1 |
| Professionnels | OK QA | Stack mobile | OK | OK |
| À propos | OK QA | Stack mobile | OK | OK Lot 3+ |
| Fiche producteur | OK QA | Hero stack · grilles 1 col | OK | OK Lot 3+ |
| Recettes | OK QA | Grille 1 col mobile | OK | OK Lot 3+ |
| Contact | OK QA | 4 parcours · formulaire | OK | OK Lot 3+ |

---

## 9. Routes plausibles (maquette)

| Route maquette | Page | Odoo cible | Statut |
|----------------|------|------------|--------|
| `/` | Accueil | Home CMS | |
| `/shop` | Boutique | `website_sale` | |
| `/shop/category/…` | Catégorie | `product.public.category` | |
| `/shop/…` | Fiche | Fiche produit native | |
| `/professionnels` | Pro | Page CMS + CRM | Odoo ✅ |
| `/a-propos` | À propos | Page CMS | ✅ Lot 3+ |
| `/producteur/…` | Fiche producteur | Page CMS · champ fournisseur = réserve | ✅ Lot 3+ |
| `/recettes` ou `/savoirs` | Éditorial | Page CMS statique · blog = réserve | ✅ Lot 3+ |
| `/contactus` | Contact | Website natif | ✅ Lot 3+ |

---

## 10. Recette QA associée

La recette de la vision V1.2.x est suivie dans :

[`recette_qa_maquette_v1_2_x.md`](./recette_qa_maquette_v1_2_x.md)

Elle doit permettre de classer chaque page et chaque concept avant tout retour dans Odoo.

---

## 11. Synthèse arbitrage — post-recette QA Lot 1

*Recette QA Lot 1.1 exécutée — verdict OK.*

| Verdict | **OK MAQUETTE CK V1.2.x LOT 1** |
|---------|-------------------|
| Prête traduction Odoo (partielle / totale) | **Oui, sur périmètre Lot 1 validé** — sous réserve des arbitrages non bloquants |
| V1 prioritaire (liste blocs/pages) | Home marchande · fiche achat · Pro double cible + CRM |
| V1 possible | Producteur fiche · process Pro · coffret · badges |
| V1 différée | Associations · recette fiche · shop · catégorie · éditorial recettes |
| Réserves bloquantes | Aucune après Lot 1.1 |
| Réserves non bloquantes | Routes Odoo à mapper · promesses logistiques à confirmer · fiche fournisseur dédiée à arbitrer |

---

## 12. Synthèse arbitrage — post-recette QA Lot 2

*Recette QA Lot 2 exécutée — verdict OK.*

| Verdict | **OK MAQUETTE CK V1.2.x LOT 2** |
|---------|-------------------|
| Pages validées | Shop · Catégorie Épicerie créole |
| Parcours validé | Accueil → Shop → Catégorie → Fiche produit · accès Pro |
| V1 prioritaire | Grille shop native · catégorie Odoo · prix TTC · origines · breadcrumb · réassurance |
| V1 possible | Pills collections · filtres visuels · tri select · intro éditoriale catégorie · guide “Comment choisir ?” |
| V1 différée | Filtres interactifs · pagination · facettes avancées · collections multiples |
| Réserves bloquantes | Aucune |
| Réserves non bloquantes | Routes Odoo absolues `/shop/...` à mapper · promesses logistiques à confirmer · attributs origine/famille à structurer |

Décision recommandée :

```text
Valider Lot 2.
Arbitrer ensuite entre Lot 3+ éditorial/contact
ou préparation de la traduction Odoo Lot 1 + Lot 2.
```

---

## 13. Synthèse arbitrage — post-recette QA Lot 3+

*Recette QA Lot 3+ exécutée — fiche producteur incluse — verdict OK.*

| Verdict | **OK MAQUETTE CK V1.2.x LOT 3+** |
|---------|-----------------------------------|
| Pages validées | À propos · Fiche producteur type · Recettes · Contact |
| Vision CK | Expérience commerciale + logistique + éditoriale + relation producteur |
| V1 prioritaire | À propos CMS · contact `/contactus` · grille produits fiche producteur · logistique CK |
| V1 possible | Fiche producteur CMS · critères sélection · focus emblématiques · recettes statiques |
| V1 différée | Annuaire producteurs · blog · recettes auto-liées · portail producteur |
| Réserves bloquantes | Aucune |
| Réserves non bloquantes | CMS vs module fournisseur Odoo · pas d’annuaire V1 |

Décision MOA actée :

```text
OK MAQUETTE CK V1.2.x — VISION COMPLÈTE MATÉRIALISÉE (9 pages).
Odoo en pause.
Prochaine étape : arbitrage périmètre V1 traduisible — pas reprise automatique du prototype.
```

Voir [`decision_moa_verdict_maquette_v1_2_x_vision_complete.md`](./decision_moa_verdict_maquette_v1_2_x_vision_complete.md).

---

## 14. Synthèse arbitrage — vision complète (post-verdict MOA)

*Verdict MOA acté — 2026-06-13.*

| Verdict global | **OK MAQUETTE CK V1.2.x — VISION COMPLÈTE MATÉRIALISÉE** |
|----------------|----------------------------------------------------------|
| Pages | 9 — Accueil · Shop · Catégorie · Fiche produit · Pro · À propos · Fiche producteur · Recettes · Contact |
| Parcours clé | Accueil → Shop → Catégorie → Fiche produit · Fiche produit → Fiche producteur → Shop / Recettes / Pro |
| V1 prioritaire (extrait) | Home · shop · catégorie · fiche achat · Pro + CRM · contact · réassurance · grille produits producteur |
| V1 possible (extrait) | Fiche producteur CMS · bloc producteur fiche · recettes statiques · critères sélection · filtres visuels |
| V1 différée / hors scope | Annuaire · portail producteur · blog complexe · reprise intégrale prototype |
| Réserve clé | Page CMS producteur vs fournisseur Odoo natif |
| Odoo | **En pause** — GO traduction = décision distincte · arbitrage : [`ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md`](./ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md) |

---

*Cadrage maquette CK V1.2.x — document vivant · vision complète validée MOA · 2026-06-13.*
