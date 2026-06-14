# Ticket MOA — Composition CMS CK 01 — Accueil · Vedettes · Page Pro

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Type** | Ticket MOA / contenu / Website Builder |
| **Module socle** | `dorevia_ck_theme` — **non modifiable dans ce ticket** |
| **Odoo** | 19 CE — `website`, `website_sale`, `website_crm` |
| **Instance cible** | `dorevia_ck_marketone_01` — [`REFERENCE_INSTANCE_RECETTE_DOREVIA_CK_THEME_01.md`](./REFERENCE_INSTANCE_RECETTE_DOREVIA_CK_THEME_01.md) |
| **Références** | [`note_05.md`](../cadrage/note_05.md) (doctrine · pause home) · [`brief_01_2.md`](./maquette_01.2/brief_01_2.md) (brief V1.2) · [`ticket_dorevia_ck_theme_01_socle_tokens_layout_snippets.md`](./ticket_dorevia_ck_theme_01_socle_tokens_layout_snippets.md) (clôturé socle) · Maquette V1.1.1 → **V1.2 Boutique élégante** · [`design_01.md`](./design_01.md) · [`grille_traduction_odoo_v1.md`](./maquette_01/grille_traduction_odoo_v1.md) |
| **Date** | 2026-06-12 |
| **Statut** | **Validé MOA** · **Odoo EN PAUSE** · maquette V1.2.x prioritaire ([`decision_moa_pause_odoo_iteration_maquette_v1_2_x`](./maquette_01.2/decision_moa_pause_odoo_iteration_maquette_v1_2_x.md)) |

---

## 0.2 Décision MOA — validation finale (2026-06-12)

La MOA **valide** ce ticket. L’**exécution CMS est autorisée** sur l’instance `dorevia_ck_marketone_01`.

```text
Ticket composition CMS CK 01 : VALIDÉ MOA
Exécution Website Builder : AUTORISÉE
GO général CK : NON DONNÉ
```

Micro-ajustements QA intégrés et conformes :

- formulaire Pro porté par `website_crm` natif, sans champ CRM custom ;
- menu « Professionnels » validé vers `/professionnels` ;
- produits vedettes via mécanisme natif Odoo / Website Builder, sans logique custom.

### Périmètre autorisé

```text
composition accueil · snippets CK Marketone · vedettes Dynamic Products / snippet natif
page /professionnels · formulaire website_crm natif · menu Professionnels
recette QA recette_qa_composition_cms_ck_01.md
```

### Hors périmètre maintenu

```text
modification dorevia_ck_theme · nouveau SCSS / QWeb · champ CRM custom · logique sélection custom
origines / collections / filtre prix avancé · B2B custom · pricelists / devis / portail client
panier / checkout custom · toute extension hors ticket 01
```

---

## 0.3 Itération MOA — pause home · note_05 (2026-06-13)

Référence : [`note_05.md`](../cadrage/note_05.md) · brief [`brief_01_2.md`](./maquette_01.2/brief_01_2.md)

```text
PREUVE DE FAISABILITÉ ODOO : OK (socle + première composition CMS)
HOME COMPLÈTE : EN PAUSE — réalignement maquette V1.2 « Boutique élégante »
ODOO N’EST PAS ABANDONNÉ — reprise composition bloc par bloc post-V1.2
```

**Doctrine révisée** : boutique claire, désirable, rassurante, orientée **conversion** — élégance au service de l’achat, pas vitrine contemplative.

**Hiérarchie cible home V1.2** (note_05 §4) — à traduire en maquette puis en Builder :

1. Header marchand · 2. Hero court · 3. Réassurance immédiate · 4. Produits mis en avant (prix visibles)
5. Catégories actionnables · 6. Packs / coffrets · 7. Espace pro · 8. Éditorial bas · 9. Footer CK

**Capital instance** (non perdu) : hero `s_ck_hero` · univers (`s_product_list` + cards) · amorce Dynamic Products · CTAs `/shop` · `/professionnels`.

**En pause** : finalisation home complète · ordre définitif des blocs · verdict `OK COMPOSITION CMS CK 01` sur home V1.1.1.

**Peut continuer** : données BO · config Dynamic Products · page `/professionnels` · menu Pro · non-régression `/shop`.

---

## 0.4 GO initial traduction Odoo — conservé · pause active V1.2.x (2026-06-13)

Référence : [`arbitrage_moa_maquette_01_2.md`](./maquette_01.2/arbitrage_moa_maquette_01_2.md) · [`recette_qa_maquette_01_2.md`](./maquette_01.2/recette_qa_maquette_01_2.md) · [`TABLEAU_TRADUCTION_ODOO_V1_2.md`](./maquette_01.2/TABLEAU_TRADUCTION_ODOO_V1_2.md)

```text
GO TRADUCTION ODOO — MAQUETTE CK V1.2
AVEC RÉSERVES MOA ACCEPTÉES
STATUT ACTUEL : ODOO EN PAUSE
HOME ODOO (Hero · réassurance · produits…) : ⏸ PAUSE — maquette V1.2.x vision complète
Référence : decision_moa_pause_odoo_iteration_maquette_v1_2_x.md
```

**Ordre d’exécution validé MOA** — cf. [`go_reprise_odoo_v1_2.md`](./maquette_01.2/go_reprise_odoo_v1_2.md) :

```text
1. ✅ /professionnels + menu Professionnels
2. ✅ Header marchand V1.2
3. ⏸ Home Odoo — PAUSE maquette V1.2.x (decision_moa_pause_odoo_iteration_maquette_v1_2_x.md)
4. ☐ Reprise Hero → … post-verdict maquette + arbitrage classes
```

**Réserves MOA acceptées** (non bloquantes pour démarrage structurel) :

| Réserve | Arbitrage |
|---------|-----------|
| Promesses commerciales | ACCEPTÉ AVEC RÉSERVE — reformulation tenable à la traduction |
| `/professionnels` | ACCEPTÉ — à produire en parallèle · obligatoire avant go-live |
| Routes fictives maquette | ACCEPTÉ POUR MAQUETTE — mapping BO à la traduction |
| Visuels placeholders | ACCEPTÉ structurel — réserve visuelle avant recette finale |
| Artisanat | ACCEPTÉ — non prioritaire phase 1 |

**Garde-fous maintenus** : Odoo 19 CE · Website Builder · snippets first · pas de surcouche · pas de catalogue parallèle · pas de panier/checkout custom · pas de B2B custom.

---

## 0.1 Relecture QA MOA (2026-06-12)

```text
VALIDABLE SOUS MICRO-AJUSTEMENTS — AUCUN POINT BLOQUANT
→ MICRO-AJUSTEMENTS INTÉGRÉS — VALIDATION MOA FINALE ACTÉE
```

Recette QA post-exécution : [`recette_qa_composition_cms_ck_01.md`](./recette_qa_composition_cms_ck_01.md)

---

## 0. Prérequis — socle ticket 01 validé

```text
OK SQUELETTE STATIQUE
→ OK INSTALLATION / QWEB
→ OK RECETTE VISUELLE POST-CORRECTION
→ SOCLE TICKET 01 VALIDÉ · CLÔTURÉ CÔTÉ DEV
```

Recettes : [`recette_qa_dorevia_ck_theme_01_visuelle_post_correction.md`](./recette_qa_dorevia_ck_theme_01_visuelle_post_correction.md)

### Référentiel obligatoire

```text
Odoo 19 CE · snippets first · pas de surcouche autonome
```

### Mode d’exécution

```text
Website Builder uniquement
Pas d’extension module · pas de surcouche · pas de B2B custom
```

---

## 1. Objet du ticket

Composer les **premières pages CK** dans Odoo Website Builder, à partir du socle thème validé, **sans nouveau développement module**.

| # | Livrable MOA |
|---|--------------|
| 1 | Page d’accueil composée (snippets CK Marketone) |
| 2 | Produits vedettes raccordés via mécanisme natif Odoo |
| 3 | Page Pro CMS `/professionnels` + formulaire `website_crm` |
| 4 | Navigation et liens internes cohérents |
| 5 | Recette MOA/QA de composition CMS |

Objectif initial : page cohérente maquette V1.1.1 — **sans pixel-perfect**.

**Post note_05** : la home cible est la **maquette V1.2 — Boutique élégante** (plus marchande, traduisible Builder). La composition Odoo home **reprend après validation MOA/QA V1.2**.

---

## 2. Périmètre IN

### 2.1 Page d’accueil

Composer l’accueil à partir des snippets du groupe **CK Marketone** (socle ticket 01) :

| Zone maquette | Snippet socle | Alternative Odoo natif |
|---------------|---------------|------------------------|
| Hero | `s_ck_hero` | Banner · Text-Image |
| Liens / univers | `s_ck_category_links` | Links · pills |
| Produits vedettes | `s_ck_featured_products` + zone `oe_structure` | **Dynamic Products** · Products |
| Réassurance | `s_ck_reassurance` | Features · Columns |
| Appel Pro | `s_ck_pro_banner` | Texte + CTA vers `/professionnels` |

Ordre indicatif (ajustable MOA) : hero → univers → vedettes → réassurance → bandeau Pro.

### 2.2 Produits vedettes

Mécanisme **Odoo natif uniquement** :

```text
Dynamic Products  ·  Products snippet  ·  sélection manuelle BO
```

> **Précision MOA — « sélection manuelle BO »** : configuration éditoriale via mécanisme natif Odoo / Website Builder / snippet produits, **sans mécanisme de sélection custom**.

| Autorisé | Interdit |
|----------|----------|
| Sélection produits publiés via snippet / Builder | Catalogue parallèle |
| Critère simple natif (ex. catégorie, tag) | Logique custom |
| Composition dans `oe_structure` du snippet vedettes | Développement module |
| Configuration éditoriale Dynamic Products / Products | Script ou domaine custom hors natif |

### 2.3 Page Pro CMS — `/professionnels`

Créer / composer une **page CMS** (pas de template custom).

**Contenu attendu** (arbitrages MOA §10 — [`note_transmission_arbitrage_david_01_v1_1.md`](./maquette_01/note_transmission_arbitrage_david_01_v1_1.md)) :

| Bloc | Contenu |
|------|---------|
| **Double cible** | Producteurs / transformateurs créoles · boutiques / restaurants / hôtels / distributeurs |
| **Doctrine CK** | CK relie fournisseurs créoles, distributeurs européens et canal B2C direct |
| **Prix B2C / B2B** | Prix publics affichés = canal B2C · conditions B2B = back-office Odoo (`product.pricelist`) — pas d’exposition publique B2B |
| **Formulaire** | Qualification commerciale via **`website_crm`** natif |

**Formulaire Pro / `website_crm`** — formulation MOA :

```text
Champ de qualification porté par le formulaire website_crm natif, sans création de champ CRM custom dans ce ticket ; si nécessaire, information capturée dans le message / description du lead.
```

Snippets utiles : `s_ck_pro_banner` · blocs texte CMS · formulaire CRM natif.

**UX MOA actée** : page Pro unique · deux blocs · deux CTA · **un seul formulaire** avec qualification — pas deux formulaires séparés phase 1.

### 2.4 Navigation

**Décision MOA — menu Professionnels** :

```text
Le menu Professionnels est validé dans ce ticket et doit pointer vers /professionnels.
```

| Élément | Cible |
|---------|-------|
| Menu principal | Accueil · Boutique · Contact · **Professionnels** → `/professionnels` |
| CTA hero accueil | `/professionnels` ou `/shop` selon contenu MOA (lien Pro recommandé si bandeau Pro présent) |
| Bandeau Pro `/shop` | Lien `/professionnels` (snippet `s_ck_shop_intro` / `s_ck_pro_banner` si composé) |
| Liens internes | Cohérence URLs · pas de liens morts |

### 2.5 Recette MOA/QA

Préparer et exécuter une recette de composition CMS : [`recette_qa_composition_cms_ck_01.md`](./recette_qa_composition_cms_ck_01.md).

| # | Point |
|---|-------|
| 1 | Rendu page accueil desktop |
| 2 | Rendu page `/professionnels` desktop |
| 3 | Snippets CK présents et éditables Website Builder |
| 4 | Vedettes alimentées (produits visibles) |
| 5 | Formulaire CRM fonctionnel |
| 6 | Responsive mobile accueil + Pro |
| 7 | Non-régression `/shop` · fiche produit · panier · checkout natifs |
| 8 | Aucune modification module `dorevia_ck_theme` |

---

## 3. Périmètre OUT (explicite)

```text
modification dorevia_ck_theme · nouveau SCSS · nouveau QWeb · nouveau snippet technique
champ CRM custom · extension formulaire website_crm hors natif
origines custom · collections custom · filtre prix avancé
portail B2B custom · configuration B2B complète
pricelists / devis / portail client en exécution
panier / checkout custom · catalogue parallèle · JS métier
front autonome · injection HTML maquette
logique transactionnelle hors Odoo standard
```

Toute limite Odoo constatée = **documenter** avant toute demande d’extension Dev.

---

## 4. Données minimales nécessaires

Créer ou vérifier en back-office avant composition :

| Donnée | Usage |
|--------|-------|
| Catégories e-commerce (`product.public.category`) | Pills univers · navigation shop |
| Produits publiés (`is_published`) | Grille `/shop` · vedettes |
| Produit représentatif type « savon vétiver » | Recette · démo MOA |
| 3–4 produits vedettes | Section accueil |
| Formulaire CRM website | Page Pro · lead qualification |

Instance recette : base `dorevia_ck_marketone_01` — produit test QA déjà présent possible.

---

## 5. Critères d’acceptation (recette MOA/QA)

```text
□ Accueil composé dans Website Builder
□ Snippets CK utilisés sans développement supplémentaire
□ Produits vedettes raccordés via Odoo natif (Dynamic Products / Products · config éditoriale)
□ Page /professionnels créée
□ Formulaire website_crm natif présent (sans champ CRM custom)
□ Qualification Pro capturée via message / description lead si besoin
□ Menu Professionnels → /professionnels
□ Message double cible Pro clair
□ Doctrine prix B2C publics / conditions B2B back-office clairement distinguée
□ Rendu desktop correct
□ Rendu mobile correct
□ /shop reste porté par website_sale
□ Panier / checkout natifs non régressés
□ Aucune extension module hors ticket 01
```

---

## 6. Verdict attendu

```text
OK COMPOSITION CMS CK 01
```

ou

```text
KO COMPOSITION CMS CK 01 — corrections CMS à reprendre
```

---

## 7. Gouvernance

| Question | Statut |
|----------|--------|
| Ticket validé MOA ? | ✅ Oui — 2026-06-12 |
| Exécution CMS autorisée ? | ✅ **Home V1.2 — reprise bloc par bloc** (arbitrage 2026-06-13) |
| Maquette V1.2 requise ? | ✅ Recettée · arbitrage acté |
| Ticket MOA / Website Builder | Pas de GO Dev |
| GO général CK | **Non donné** |
| Socle `dorevia_ck_theme` | Clôturé — hors périmètre modification |
| Extension / écart | Constat limite Odoo + arbitrage MOA + ticket séparé |
| Phase CMS MOA | ≠ autorisation surcouche ou B2B custom |

---

## 8. Séquence d’exécution proposée

```text
1. ✅ Relecture QA MOA — micro-ajustements intégrés
2. ✅ Validation MOA finale de CE ticket
3. ✅ Première composition home — preuve faisabilité (hero · univers · Dynamic Products)
4. ✅ Note d’itération MOA — note_05 · pause home complète
5. ✅ Maquette CK V1.2 livrée Dev — [`LIVRAISON_V1_2.md`](./maquette_01.2/LIVRAISON_V1_2.md)
5bis. ✅ Arbitrage MOA — [`arbitrage_moa_maquette_01_2.md`](./maquette_01.2/arbitrage_moa_maquette_01_2.md) · GO traduction Odoo
6. ☐ Préparation données BO (catégories · produits · coffrets · CRM)
7. ✅ Page /professionnels + menu Professionnels — [`COMPOSITION_PROFESSIONNELS_V1_2.md`](./maquette_01.2/COMPOSITION_PROFESSIONNELS_V1_2.md)
8. ✅ Reprise Header — [`COMPOSITION_HEADER_V1_2.md`](./maquette_01.2/COMPOSITION_HEADER_V1_2.md)
9. ☐ Reprise home blocs — Hero · Réassurance · …
9. ☐ Recette MOA/QA — recette_qa_composition_cms_ck_01.md (qualité perçue + efficacité commerciale)
10. ☐ Verdict tracé — OK ou KO composition CMS CK 01
```

---

## 9. Liens ticket 01

| Ticket 01 (clôturé) | Ce ticket MOA |
|---------------------|---------------|
| Snippets XML + registry | **Utilisation** en Builder |
| Tokens / SCSS / layout | **Hérités** — non modifiés |
| Placeholder vedettes `oe_structure` | **Rempli** par MOA (Dynamic Products) |
| Page Pro « cible CMS » | **Composée** par MOA |

---

*Ticket MOA — composition CMS CK 01 — validé MOA · GO traduction Odoo V1.2 · arbitrage 2026-06-13.*
