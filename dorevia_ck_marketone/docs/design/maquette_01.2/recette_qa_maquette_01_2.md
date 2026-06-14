# Recette QA — Maquette CK V1.2 · Boutique élégante

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Livraison** | Maquette CK V1.2 — Home boutique élégante |
| **Doctrine source** | [`note_05.md`](../../cadrage/note_05.md) — **actée MOA** |
| **Brief source** | [`brief_01_2.md`](./brief_01_2.md) |
| **Ticket Dev** | [`ticket_dev_maquette_01_2_open_design.md`](./ticket_dev_maquette_01_2_open_design.md) |
| **GO MOA** | [`go_moa_maquette_01_2.md`](./go_moa_maquette_01_2.md) — **GO OFFICIEL confirmé** |
| **Périmètre** | Home CK V1.2 · desktop + mobile |
| **Instance Odoo de référence** | `dorevia_ck_marketone_01` — [`REFERENCE_INSTANCE_RECETTE_DOREVIA_CK_THEME_01.md`](../REFERENCE_INSTANCE_RECETTE_DOREVIA_CK_THEME_01.md) |
| **Artefact** | [`artifact/index.html`](./artifact/index.html) · Open Design : `/Users/doreviateam/open-design/.od/projects/ck-marketone-maquette-v1_2/index.html` |
| **Livraison** | [`LIVRAISON_V1_2.md`](./LIVRAISON_V1_2.md) |
| **URL testée** | `http://127.0.0.1:8766/index.html` |
| **Date recette** | 2026-06-13 |
| **Statut QA** | **Recette QA exécutée — 2026-06-13** |
| **Verdict QA** | OK PARTIEL — critères bloquants validés |
| **Arbitrage MOA** | [`arbitrage_moa_maquette_01_2.md`](./arbitrage_moa_maquette_01_2.md) — **GO traduction Odoo** |
| **Verdict final** | **GO TRADUCTION ODOO — MAQUETTE CK V1.2 AVEC RÉSERVES MOA ACCEPTÉES** |

> Cette recette juge la **qualité perçue** et l’**efficacité commerciale** de la maquette V1.2. La composition Odoo reprend post-arbitrage — [`ticket_moa_composition_cms_ck_01`](../ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md) §0.4.

---

## 1. Objet de la recette

Cette recette vise à valider que la maquette CK V1.2 répond bien à la doctrine MOA actée :

> CK doit être une boutique claire, désirable et rassurante, capable de déclencher l’achat rapidement, tout en conservant une identité soignée.

La recette ne juge pas seulement la qualité visuelle.
Elle juge aussi la capacité commerciale de la maquette :

* visibilité produit ;
* prix assumés ;
* réassurance ;
* catégories actionnables ;
* parcours d’achat court ;
* entrée professionnelle claire ;
* traduisibilité réaliste dans Odoo Website Builder.

### 1.1 Contrôle technique — 2026-06-13

Artefact servi depuis [`artifact/index.html`](./artifact/index.html) · `python3 -m http.server 8766`.

| Plateforme | Viewport | Overflow horizontal | Preuves | Produits | Prix cartes | Ordre blocs | 1er écran |
|------------|----------|---------------------|---------|----------|-------------|-------------|-----------|
| **Desktop** | 1280×800 | ✅ non (`1280=1280`) | 4 | 6 | 7 affichés | ✅ hero→preuves→produits→… | ✅ réassurance ~350px |
| **Mobile** | 390×844 | ✅ non (`390=390`) | 4 | 6 | 7 affichés | ✅ preuves+produits avant éditorial | ✅ preuves ~555px · produits ~944px (1er scroll) |

Mesures complémentaires : CTA produits = `Voir` / `Découvrir` uniquement · lien `/professionnels` présent · 5 liens `/shop/category/…` · pas de lorem · pas de placeholder Odoo footer · pas de `Ajouter au panier`.

---

## 2. Rappel du contexte

Une première traduction de la home CK dans Odoo 19 CE a validé le socle technique :

```text
OK socle technique
OK faisabilité CMS
KO traduction cible commerciale complète
```

La V1.2 doit corriger l’écart commercial constaté sans remettre en cause la doctrine technique :

```text
Odoo 19 CE
Website Builder
snippets first
pas de surcouche autonome
pas de catalogue parallèle
pas de panier / checkout custom
```

---

## 3. Documents de référence

| Document | Rôle |
|----------|------|
| [`note_05.md`](../../cadrage/note_05.md) | Décision MOA · doctrine · pause home · cible V1.2 |
| [`go_moa_maquette_01_2.md`](./go_moa_maquette_01_2.md) | **GO OFFICIEL MOA** — Move 3 |
| [`brief_01_2.md`](./brief_01_2.md) | Commande opérationnelle de maquette V1.2 |
| [`ticket_dev_maquette_01_2_open_design.md`](./ticket_dev_maquette_01_2_open_design.md) | Ticket Dev — GO production |
| [`ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md`](../ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md) | Ticket CMS suspendu · reprise post-V1.2 |
| [`recette_qa_composition_cms_ck_01.md`](../recette_qa_composition_cms_ck_01.md) | État partiel de la composition Odoo |
| [`points_a_arbitrer.md`](../maquette_01/points_a_arbitrer.md) | Arbitrages ouverts ou à confirmer |

---

## 4. Méthode de recette

Chaque critère est évalué selon le statut suivant :

| Statut | Signification |
|--------|---------------|
| OK | Critère satisfait |
| KO | Critère non satisfait · correction nécessaire |
| RÉSERVE | Critère partiellement satisfait ou dépendant d’un arbitrage MOA |
| N/A | Non applicable au périmètre livré |

La maquette V1.2 ne pourra être validée que si les **critères bloquants** sont OK ou acceptés explicitement par la MOA.

**Critères bloquants** (grille §5) : #1 · #2 · #4 · #6 · #10 · #11 · #14 · #15 · #16.

---

## 5. Grille de recette QA

| # | Critère | Attendu | Statut | Commentaire QA |
|---|---------|---------|--------|----------------|
| 1 | Produits visibles rapidement | Produits visibles dans les **10 premières secondes** en desktop · au **1er scroll** mobile | OK | Desktop : début produits visible au premier écran. Mobile : produits accessibles immédiatement après hero + preuves, avant tout éditorial. |
| 2 | Prix visibles | Prix affiché sur **chaque carte produit** mise en avant | OK | 6 cartes produits + coffret avec prix visibles. |
| 3 | Premier écran desktop | Le 1er écran laisse entrevoir la réassurance **ou** le début des produits | OK | Réassurance visible sous hero et amorce produits visible en 1280×720. |
| 4 | Preuves de confiance | **Au moins 3** preuves visibles haut de page | OK | 4 preuves : livraison, paiement sécurisé, producteurs sélectionnés, service client. |
| 5 | Promesses tenables | Les preuves affichées sont réalistes et validables par la MOA | OK | Arbitrage MOA [`arbitrage_moa_maquette_01_2.md`](./arbitrage_moa_maquette_01_2.md) §2.1 : **ACCEPTÉ AVEC RÉSERVE** — reformulation tenable à la traduction si nécessaire. |
| 6 | Catégories actionnables | Catégories → routes / filtres Odoo plausibles (`/shop/category/…`) | OK | Routes catégories explicites et compatibles `product.public.category`. |
| 7 | Produits crédibles | Cartes avec exemples cohérents CK — pas de produits génériques | OK | Produits cohérents : goyavier, crackers manioc, galettes, colombo, savon vétiver, coffret. |
| 8 | CTA produit | CTA `Voir` · `Découvrir` · `Voir le produit` privilégiés | OK | CTA produits conformes : `Voir` et `Découvrir`. |
| 9 | CTA `Ajouter` | Pas de `Ajouter au panier` sans arbitrage MOA / faisabilité Odoo | OK | Aucun CTA `Ajouter au panier`. |
| 10 | CTA Pro | Lien ou ancre vers `/professionnels` ou section Pro prévue — **sans 404** | OK | Arbitrage MOA §2.2 : **ACCEPTÉ — À PRODUIRE EN PARALLÈLE ODOO** avant mise en ligne publique. |
| 11 | Aucun lien mort | Aucun CTA principal vers route morte ou non prévue | OK | Arbitrage MOA §2.3 : **ACCEPTÉ POUR MAQUETTE** — mapping BO à la traduction Odoo. |
| 12 | Footer CK | Footer sans placeholder Odoo ou contenu générique | OK | Footer CK propre, sans `Your Company`, contenu fictif Odoo ou texte générique. |
| 13 | Mention Odoo | Mention `Généré par Odoo` masquée si possible · ou réserve explicitée | OK | Pas de mention `Généré par Odoo`; mention maquette explicite uniquement. |
| 14 | Sections complètes | Aucun bloc vide · lorem ipsum · placeholder non assumé | OK | Arbitrage MOA §2.4 : **ACCEPTÉ POUR TRADUCTION STRUCTURELLE** — réserve visuelle à lever avant recette finale. |
| 15 | Mobile | **Maquette mobile obligatoire** · produits + preuves avant éditorial long | OK | Responsive 390 px vérifié : pas d’overflow horizontal, ordre correct, preuves et produits avant éditorial. |
| 16 | Traduisibilité Odoo | Chaque bloc mappable vers snippet natif Odoo ou snippet CK Marketone | OK | Tableau de traduction Odoo complété bloc par bloc. |
| 17 | Univers Artisanat | Statut confirmé · renommé · repoussé · ou réserve MOA | OK | Arbitrage MOA §2.5 : **ACCEPTÉ — ARTISANAT NON PRIORITAIRE PHASE 1**. |
| 18 | Espace professionnel | Double cible producteurs / distributeurs · orientée qualification | OK | Double cible explicite : fournisseur/transformateur et distributeur/point de vente ; CRM Odoo mentionné. |
| 19 | Packs / coffrets | Présence ou justification d’un axe coffrets / découverte | OK | Bloc coffret découverte dédié avec prix et CTA. |
| 20 | Cohérence DA | Maquette élégante · lisible · cohérente identité CK | OK | Direction claire, sobre, marchande et plus efficace que V1.1.1 ; désirabilité dépendra des vrais visuels. |
| 21 | Tableau traduction Odoo | Fichier [`TABLEAU_TRADUCTION_ODOO_V1_2.md`](./TABLEAU_TRADUCTION_ODOO_V1_2.md) complété · distinct de LIVRAISON | OK | Fichier présent et complété. |

---

## 6. Points d’attention spécifiques

### 6.1 Univers Artisanat

L’univers **Artisanat** doit être vérifié.

Décision attendue :

```text
Artisanat confirmé phase 1
ou
Artisanat renommé
ou
Artisanat repoussé
ou
Artisanat conservé avec réserve MOA
```

### 6.2 Produits indicatifs

La maquette doit s’appuyer sur des produits plausibles, par exemple :

* Confiture de goyave / goyavier ;
* Galettes de manioc ;
* Manio Crackers sucré ;
* Manio Crackers salé ;
* Savon vétiver ;
* Coffret découverte créole ;
* Épices colombo ;
* Sirop tamarin ;
* Café, biscuit ou farine selon catalogue disponible.

### 6.3 Réassurance

Les preuves affichées ne doivent pas être de simples promesses marketing.
Elles doivent être réalistes et tenables opérationnellement.

Exemples à valider :

* Livraison France / Europe ;
* Paiement sécurisé ;
* Producteurs sélectionnés ;
* Service client ;
* Conditions professionnelles sur qualification.

### 6.4 Liens principaux

Les liens suivants doivent être vérifiés :

* Boutique ;
* Catégories / Univers ;
* Professionnels ;
* Voir le produit ;
* Contact ;
* Panier ;
* Recherche si présente ;
* Coffrets / Packs si présents.

---

## 7. Grille de correspondance Odoo

Alignée sur [`brief_01_2.md`](./brief_01_2.md) §5.

| Bloc maquette V1.2 | Traduction Odoo attendue | Statut | Commentaire |
|--------------------|--------------------------|--------|-------------|
| Header marchand | Header Website / menu Odoo | OK | Mapping compatible ; logo `href="#"` à corriger en `/`. |
| Hero court | `s_ck_hero` · Banner · Text-Image | OK | Structure traduisible ; visuel à remplacer. |
| Réassurance | `s_ck_reassurance` · Features · Columns | OK | 4 items simples, traduisibles en colonnes/features. |
| Produits mis en avant | `s_ck_featured_products` · Dynamic Products | OK | Compatible Dynamic Products ; mapping produits BO à créer. |
| Catégories | `s_ck_category_links` · `product.public.category` · `/shop/category/…` | OK | Routes plausibles ; catégories BO à aligner. |
| Packs / coffrets | Produits Odoo ou catégorie dédiée | OK | Coffret modélisable comme produit ou catégorie dédiée. |
| Espace Pro | `s_ck_pro_banner` · page `/professionnels` · `website_crm` | RÉSERVE | Page `/professionnels` à composer avant reprise home. |
| Éditorial / SEO | Blocs CMS natifs | OK | Bloc bas de page simple, traduisible. |
| Footer | Footer Website personnalisé | OK | Footer CK propre ; lien `/legal` à confirmer. |

---

## 8. Verdict QA

### Verdict attendu si conforme

```text
OK MAQUETTE CK V1.2 — BOUTIQUE ÉLÉGANTE
```

### Verdict si corrections nécessaires

```text
KO MAQUETTE V1.2 — corrections à reprendre (critères §5 non satisfaits)
```

### Verdict intermédiaire possible

```text
OK PARTIEL MAQUETTE V1.2 — réserves à lever avant traduction Odoo
```

---

## 9. Décision QA

| Élément | Statut |
|---------|--------|
| Maquette desktop | OK |
| Maquette mobile | OK — responsive 390 px vérifié |
| Tableau [`TABLEAU_TRADUCTION_ODOO_V1_2.md`](./TABLEAU_TRADUCTION_ODOO_V1_2.md) | OK — fichier distinct et complété |
| Cohérence avec [`note_05.md`](../../cadrage/note_05.md) | OK |
| Cohérence avec [`brief_01_2.md`](./brief_01_2.md) | OK |
| Traduisibilité Odoo (§7) | OK — mapping clair · routes BO à créer à la traduction |
| Arbitrage MOA | ✅ Acté — [`arbitrage_moa_maquette_01_2.md`](./arbitrage_moa_maquette_01_2.md) |
| Verdict recette | OK PARTIEL — critères bloquants validés |
| Verdict final post-arbitrage | **GO TRADUCTION ODOO — MAQUETTE CK V1.2 AVEC RÉSERVES MOA ACCEPTÉES** |

---

## 10. Suite après verdict

### Si verdict OK

Reprendre l’exécution Odoo Website Builder bloc par bloc — cf. [`brief_01_2.md`](./brief_01_2.md) §11 :

1. Header ;
2. Hero ;
3. Réassurance ;
4. Produits mis en avant ;
5. Catégories ;
6. Packs / coffrets ;
7. Espace professionnel ;
8. Footer ;
9. Revalidation desktop + mobile — [`recette_qa_composition_cms_ck_01.md`](../recette_qa_composition_cms_ck_01.md).

### Si verdict KO

Retour maquettage avec liste des critères §5 non satisfaits.

### Si verdict OK partiel

Arbitrage MOA sur les réserves · correction ciblée · puis reprise Odoo.

**Statut 2026-06-13** : arbitrage acté — reprise Odoo autorisée — cf. [`arbitrage_moa_maquette_01_2.md`](./arbitrage_moa_maquette_01_2.md).

---

## 11. Principe de travail

Le projet CK est conduit par itérations courtes.

Chaque itération doit produire au moins l’un des résultats suivants :

* un meilleur rendu ;
* une meilleure compréhension ;
* une décision plus claire ;
* une réduction d’écart entre la maquette et Odoo ;
* une amélioration de la capacité commerciale du site.

Principe MOA retenu :

> Nous ne perdons jamais : nous apprenons, nous capitalisons, puis nous améliorons.

---

*Recette QA maquette CK V1.2 — exécutée 2026-06-13 · URL http://127.0.0.1:8766/index.html · arbitrage MOA acté · GO traduction Odoo.*
