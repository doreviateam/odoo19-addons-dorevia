# Ticket — `dorevia_ck_theme_01_socle_tokens_layout_snippets`

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Module cible** | `dorevia_ck_theme` |
| **Type** | Ticket de cadrage technique — **validé MOA** · **clôturé côté socle** |
| **Exécution** | **Socle livré et validé QA** — phase suivante = composition CMS MOA |
| **Odoo** | 19 CE |
| **Dépendances** | `website`, `website_sale`, `website_crm` |
| **Références** | [`note_approche_technique_dorevia_ck_theme_01.md`](./note_approche_technique_dorevia_ck_theme_01.md) (note d’approche **validée MOA**) · Maquette V1.1.1 · [`grille_traduction_odoo_v1.md`](./maquette_01/grille_traduction_odoo_v1.md) · [`tokens.md`](./maquette_01/tokens.md) · [`design_01.md`](./design_01.md) v1.1 |
| **Date** | 2026-06-12 |
| **Statut** | **Clôturé côté socle (2026-06-12)** · verrou ticket 01 levé · GO général CK non donné |

---

## 0. Décision MOA — GO exécution encadré

La MOA valide ce ticket comme **cadrage d’exécution** et lève formellement le **verrou Odoo pour ce ticket uniquement**.

```text
Note d’approche technique : validée MOA
Ticket dorevia_ck_theme_01 : validé MOA — exécution encadrée autorisée
Verrou Odoo : levé pour ticket 01 uniquement
Exécution hors périmètre ticket 01 : non autorisée
```

### Périmètre autorisé (strict)

Odoo 19 CE · `website` · `website_sale` · `website_crm` · tokens · variables · palette · typo (sous réserve technique) · espacements · boutons · cartes · layout · snippets éditables · adaptations visuelles légères · QWeb/SCSS minimal conforme au ticket.

### Hors périmètre maintenu

```text
origines custom · collections custom · filtre prix avancé
portail B2B custom · configuration B2B complète
pricelists / devis / portail client
module métier · extension e-commerce · catalogue parallèle
panier/checkout custom · front autonome · injection HTML maquette
logique transactionnelle hors Odoo standard
```

### Réserve opérationnelle

La mise à disposition de l’instance Odoo / environnement d’exécution reste à organiser séparément. Cette réserve ne modifie pas le GO sur le ticket : elle conditionne seulement les tests, l’installation et la recette sur instance.

### Rappel gouvernance

Ce GO ne vaut **pas** autorisation générale sur CK. Toute extension ou écart au périmètre requiert : constat limite Odoo · arbitrage MOA · ticket séparé · validation MOA/QA avant exécution.

---

## 1. Objet du ticket

Rédiger le cadrage d’exécution du **premier ticket** du futur module `dorevia_ck_theme`, strictement borné au **socle thème CK** :

```text
tokens · variables · palette · typo · espacements · boutons · cartes · layout · snippets éditables
```

```text
Référentiel obligatoire : Odoo 19 CE · snippets first · pas de surcouche autonome
```

### Ce que le cadrage autorise (post-validation MOA)

- Exécution encadrée du module `dorevia_ck_theme` — périmètre ticket 01 uniquement
- QWeb/SCSS minimal conforme aux §5–8
- Snippets éditables Website Builder

### Ce que le GO n’autorise pas

```text
Extension hors périmètre ticket 01
Module métier · front autonome · catalogue parallèle
Configuration B2B · pricelists / devis / portail client
GO général sur le projet CK
```

**Verrou Odoo** : levé **pour ce ticket uniquement**. Maintenu pour tout autre périmètre.

---

## 2. Contexte et doctrine

| Élément | Statut |
|---------|--------|
| Maquette V1.1.1 | Validée QA |
| Arbitrages §10 MOA | Tranchés |
| Note approche thème | **Validée MOA** |
| Ticket cadrage | **Validé MOA — exécution encadrée autorisée** |
| Verrou Odoo | **Levé ticket 01 uniquement** |

```text
Note d’approche technique : validée MOA
Ticket dorevia_ck_theme_01 : validé MOA — exécution encadrée autorisée
Verrou Odoo : levé pour ticket 01 uniquement
Instance Odoo : réserve opérationnelle — à organiser séparément
```

Jalons gouvernance :

```text
1. Validation MOA doctrine technique (note d’approche) — ✅ faite
2. Validation MOA ticket d’exécution — ✅ faite
3. Levée verrou Odoo ticket 01 — ✅ faite
4. Recette QA sur instance — ☐ en attente (réserve opérationnelle)
```

```text
Odoo = source de vérité métier
website_sale = moteur boutique B2C
Thème = habillage Odoo — pas front parallèle
Maquette HTML = référence visuelle uniquement
```

**B2B** : porté par Odoo natif (`res.partner`, `product.pricelist`, `crm.lead`, BO). **Hors exécution ticket 1** — pas d’activation pricelists / devis / portail client dans ce ticket.

La mention “B2B porté par Odoo natif” ne vaut pas activation ni configuration des pricelists, devis, portail client ou parcours B2B dans le ticket 1. Ces éléments restent hors périmètre de `dorevia_ck_theme` et relèveront d’un arbitrage / paramétrage séparé.

---

## 3. Périmètre IN

| # | Domaine | Détail |
|---|---------|--------|
| 1 | Tokens SCSS | Variables `$ck-*` depuis [`tokens.md`](./maquette_01/tokens.md) |
| 2 | Palette | Corail `#D84315` · vert `#2E7D4F` — base V1 |
| 3 | Typographie | Fraunces + DM Sans — **sous réserve technique prod** |
| 4 | Espacements / radius / ombres | Échelle tokens maquette |
| 5 | Boutons | Primary · secondary · pro (override Bootstrap/thème) |
| 6 | Cartes produit | Tuiles `website_sale` — badges, chips, hover |
| 7 | Layout général | `website.layout` — header sticky, footer, conteneur max 1200px |
| 8 | Héritages QWeb légers | `products`, `product` — classes et structure, pas recréation |
| 9 | Snippets CK | Enregistrement XML + zones éditables Website Builder |
| 10 | Pages CMS cible | Accueil et `/professionnels` — composition éditoriale / paramétrage Website Builder, hors logique module métier |

---

## 4. Périmètre OUT (explicite)

```text
origines custom · collections custom · filtre prix avancé
portail B2B transactionnel · configuration B2B complète
pricelists / devis / portail client en exécution
module métier · extension e-commerce dédiée
catalogue parallèle · panier/checkout custom
front autonome · injection HTML maquette
logique transactionnelle hors Odoo standard
filtres catalogue JS local
quick-add custom
```

---

## 5. Grille d’implémentation — zone par zone

Légende éditabilité :

- **Oui** = Website Builder / CMS
- **Partiel** = structure thème + contenu éditable
- **Non** = template métier stylé uniquement (justification en colonne)

### 5.1 Layout global

| Zone | Template / snippet Odoo | Éditabilité Builder | SCSS | QWeb | Justification non éditable |
|------|-------------------------|-------------------|------|------|--------------------------|
| Header | `website.layout` | Menu, logo, liens | Sticky, backdrop, typo | Héritage léger | Panier = `sale_get_order()` natif |
| Footer | `website.layout` | Liens, textes | Tokens | Héritage léger | — |
| Body / conteneur | `website.layout` | — | Max-width, gouttières | Classes body | Structure layout |

### 5.2 Accueil

| Zone | Template / snippet Odoo | Éditabilité Builder | SCSS | QWeb | Note |
|------|-------------------------|-------------------|------|------|------|
| Hero | Snippet **Banner** ou **Text-Image** | **Oui** | CTA, typo display | Enregistrement snippet XML | Pas de hero HTML monolithique |
| Pills univers | Snippet **Links** | **Oui** | Pills style | — | Liens → `/shop/category/<id>` |
| Produits vedettes | **Dynamic Products** ou **Products** | **Oui** | Cartes | — | Sélection produits BO phase 1 |
| Réassurance | **Features** / **Columns** | **Oui** | Icônes, grille | — | 4 blocs statiques éditables |

**Page accueil** : composition CMS de snippets — **pas** de page HTML unique injectée.

### 5.3 Boutique `/shop`

| Zone | Template / snippet Odoo | Éditabilité Builder | SCSS | QWeb | Note |
|------|-------------------------|-------------------|------|------|------|
| Intro + note B2C | Zone page shop ou snippet tête | **Partiel** | Note discrète italic | Snippet optionnel | Texte éditorial MOA |
| Grille produits | `website_sale.products` | **Non** | Tuiles, badges | **Héritage léger** | **Ne pas recréer** le template |
| Sidebar catégories | `product.public.category` natif | Catégories = BO | Sidebar, drawer mobile | Layout xpath minimal | Arborescence MOA §10 |
| Tri / pagination | `website_sale` natif | **Non** | Toolbar | Classes visuelles | Comportement standard |
| Bandeau Pro | Snippet CK léger | **Oui** | `.btn-pro` | XML snippet | Lien CMS `/professionnels` |
| Filtres origines | — | — | — | — | **Hors ticket 1** — attribut produit MOA ultérieur |
| Filtres collections | — | — | — | — | **Hors ticket 1** — catégories/tags MOA |
| Filtre prix | — | — | — | — | **Hors ticket 1** — simplifier/reporter MOA |

**Limite standard Odoo** : fourchette prix avancée incertaine en CE — ne pas anticiper en ticket 1.

### 5.4 Fiche produit

| Zone | Template / snippet Odoo | Éditabilité Builder | SCSS | QWeb | Note |
|------|-------------------------|-------------------|------|------|------|
| Galerie + buy box | `website_sale.product` | Description = BO | Buy box, prix | **Héritage léger** | Pas de checkout custom |
| Chips origine / catégorie | Template + attributs | **Partiel** | Chips SCSS | xpath minimal | Origines = attribut phase 1 (hors ticket 1 si non GO) |
| Réassurance fiche | Snippet optionnel | **Oui** | — | — | Bloc statique |
| Produits liés | `alternative_product_ids` natif | **Non** | Grille related | — | Natif |

### 5.5 Espace professionnel

| Zone | Template / snippet Odoo | Éditabilité Builder | SCSS | QWeb | Note |
|------|-------------------------|-------------------|------|------|------|
| Page `/professionnels` | **Page CMS** | **Oui** | Section Pro | — | Double cible V1.1.1 |
| Blocs producteur / distributeur | **Columns** | **Oui** | `.pro-block` | — | 2 CTA distincts |
| Formulaire | **`website_crm`** | **Oui** | Champs | — | Nature de la demande — pas rôle partenaire figé |
| Footnote prix B2C/B2B | Bloc CMS | **Oui** | Footnote | — | Doctrine MOA |

**Pas** de landing Pro en QWeb fixe non CMS.

### 5.6 Panier / checkout

| Zone | Statut ticket 1 |
|------|-----------------|
| Panier | **Hors ticket** — `website_sale` standard stylé éventuellement en phase ultérieure |
| Checkout | **Hors ticket** — natif uniquement |

---

## 6. Snippets CK à enregistrer (ticket 1)

| ID snippet proposé | Base Odoo | Usage | Éditable |
|--------------------|-----------|-------|----------|
| `ck_snippet_hero` | Banner / Text-Image | Accueil hero | Oui |
| `ck_snippet_category_links` | Links | Pills univers | Oui |
| `ck_snippet_featured_products` | Products / Dynamic | Vedettes | Oui |
| `ck_snippet_reassurance` | Features / Columns | Réassurance accueil | Oui |
| `ck_snippet_shop_intro` | Text block | Intro `/shop` + note B2C | Oui |
| `ck_snippet_pro_banner` | Text + CTA | Bandeau `/shop` | Oui |

Snippets **non requis ticket 1** : filtres custom, collections, origines.

---

## 7. Assets SCSS prévus (ticket 1)

| Fichier prévu | Contenu |
|---------------|---------|
| `static/src/scss/primary_variables.scss` | Tokens `$ck-*`, couleurs, typo |
| `static/src/scss/bootstrap_overridden.scss` | Boutons, radius |
| `static/src/scss/website_sale.scss` | Tuiles, chips, sidebar layout |
| `static/src/scss/website.scss` | Header, footer, snippets Pro |

**Règle** : pas de couleurs hardcodées dans QWeb — variables SCSS uniquement.

---

## 8. Héritages QWeb prévus (minimal)

| Template parent | Nature héritage | Interdit |
|-----------------|-----------------|----------|
| `website.layout` | Assets, classes, header/footer | Remplacement total layout |
| `website_sale.products` | Classes tuiles, sidebar, note B2C | Recréation grille / filtres JS |
| `website_sale.product` | Chips, spacing buy box | Buy box custom / panier parallèle |

Estimation xpath : **faible** — quelques `//div` classes, pas de duplication de logique métier.

---

## 9. Arbitrages MOA ultérieurs (hors exécution ticket 1)

| # | Sujet | Statut MOA | Impact ticket 1 |
|---|-------|------------|-----------------|
| 1 | Typo prod Fraunces + DM Sans | Sous réserve technique | À trancher en exécution si blocage |
| 2 | Levée verrou Odoo | **Levé ticket 01** | Hors ticket 01 : verrou maintenu |
| 3 | Filtre origines (attribut) | Tranché MOA — hors ticket 1 | Extension ou paramétrage post-thème |
| 4 | Filtre collections | Tranché MOA — hors ticket 1 | Idem |
| 5 | Filtre prix | Simplifier/reporter | Idem |
| 6 | Configuration B2B / pricelists | Hors ticket thème | Paramétrage BO séparé |

---

## 10. Critères d’acceptation (recette QA)

### 10.1 Squelette — validé QA statique (2026-06-12)

```text
✅ Pas de models / controllers / JS métier
✅ Dépendances website · website_sale · website_crm
✅ QWeb limité · snippets CK · tokens SCSS
✅ Périmètre ticket 01 respecté
```

Référence : [`recette_qa_dorevia_ck_theme_01_squelette.md`](./recette_qa_dorevia_ck_theme_01_squelette.md)

**Verdict** : OK squelette — OK install/QWeb · OK visuel post-correction (2026-06-12).

### 10.1.1 Correction ciblée `layout_ck_theme` — OK QA (2026-06-12)

```text
✅ Chaînage body_classname + priority="20" — conforme Odoo 19 · ticket 01
✅ Validé QA documentaire (website_layout.xml)
✅ Recette HTTP / · /shop · fiche produit post-correction
```

### 10.2 Recette fonctionnelle — OK install/QWeb · OK visuel post-correction (2026-06-12)

Référence : [`recette_qa_dorevia_ck_theme_01_fonctionnelle.md`](./recette_qa_dorevia_ck_theme_01_fonctionnelle.md)

```text
✅ Installation · xpath QWeb · snippets registry
✅ XPath layout_ck_theme (ck-theme sur body)
✅ Module installable sur Odoo 19 CE sans extension custom
✅ Compilation SCSS — @import Google Fonts retiré · bundle valide navigateur
✅ XPath product_details · snippets_registry validés
⚠️ Placeholder vedettes — composition CMS MOA
✅ /shop · fiche produit = templates website_sale natifs stylés
☐ Page Pro CMS — composition MOA
✅ Pas de catalogue JS · pas de panier parallèle · pas B2B UI
✅ Recette visuelle navigateur — OK post-correction
🔧 Typo — fallbacks système ticket 01 · Fraunces/DM Sans = arbitrage prod séparé
```

---

## 11. Séquence d’exécution

```text
1. ✅ Validation MOA de CE ticket
2. ✅ Levée verrou Odoo (ticket 01 uniquement)
3. ✅ Base dev Odoo 19 CE — instance `dorevia_ck_marketone_01`
4. ✅ Squelette dorevia_ck_theme livré — validé QA statique
5. ✅ Socle installé · recettes QA OK (install/QWeb · visuel post-correction)
6. ✅ **Clôture socle ticket 01** — 2026-06-12
7. ⏳ **Phase CMS MOA** — exécution autorisée — [`ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md`](./ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md)
8. Extensions uniquement si limite Odoo démontrée (ticket séparé + arbitrage MOA)
```

---

## 12. Gouvernance et validation

| Question | Statut |
|----------|--------|
| Note approche validée MOA ? | ✅ Oui |
| Ticket validé MOA/QA ? | ✅ Oui |
| Exécution autorisée ? | ✅ Socle livré — **clôturé côté Dev/QA** |
| Verrou Odoo ? | **Levé ticket 01 uniquement** — maintenu hors ticket 01 |
| Squelette validé QA statique ? | ✅ Oui |
| Recette fonctionnelle / visuelle ? | ✅ OK — [`recette_qa_dorevia_ck_theme_01_visuelle_post_correction.md`](./recette_qa_dorevia_ck_theme_01_visuelle_post_correction.md) |
| Clôture socle ticket 01 ? | ✅ **Oui — 2026-06-12** |

Exécution hors périmètre ticket 01, extensions ou écarts : **non autorisés** sans ticket séparé et validation MOA/QA.

### Validation MOA — actée

| Question | Décision |
|----------|----------|
| Périmètre ticket 1 conforme note approche ? | ✅ Oui |
| Snippets / templates / SCSS / QWeb acceptables ? | ✅ Oui |
| Hors périmètre suffisamment explicite ? | ✅ Oui |
| GO exécution encadré ticket 01 ? | ✅ Oui |

### Validation QA squelette — actée (2026-06-12)

| Question | Décision |
|----------|----------|
| Périmètre squelette conforme ticket 01 ? | ✅ Oui |
| Recette statique / documentaire ? | ✅ OK |
| Recette fonctionnelle ? | ✅ OK install/QWeb · OK visuel post-correction — 2026-06-12 |

---

## 13. Clôture socle — actée (2026-06-12)

```text
TICKET 01 dorevia_ck_theme — CLÔTURÉ CÔTÉ SOCLE
```

| Livrable socle | Statut |
|----------------|--------|
| Module `dorevia_ck_theme` (tokens · layout · snippets · QWeb minimal) | ✅ Livré |
| Recettes QA (statique · fonctionnelle · visuelle post-correction) | ✅ Validées |
| Instance recette `dorevia_ck_marketone_01` | ✅ Référence |

**Hors clôture socle** (réserves maintenues, non bloquantes ticket 01) : composition CMS accueil · Dynamic Products vedettes · page Pro · arbitrage typo prod · pixel-perfect maquette.

---

## 14. Phase suivante — composition CMS MOA

```text
Mode        : Website Builder uniquement
Périmètre   : composition éditoriale pages (accueil · /professionnels · contenus)
Interdit    : extension module · surcouche front · B2B custom · HTML maquette injecté
```

| Action MOA | Snippets / outils |
|------------|-------------------|
| Accueil | Groupe **CK Marketone** — hero · pills catégories · vedettes (Dynamic Products) · réassurance |
| Page Pro | CMS + `website_crm` — blocs éditables · formulaire natif |
| Contenus | Logo · textes · menu · catégories BO — sans développement additionnel |

**Ticket MOA** : [`ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md`](./ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md) — **validé MOA · home en pause** ([`note_05.md`](../cadrage/note_05.md)) · reprise post maquette V1.2.

**État instance (2026-06-13)** : hero · univers · amorce Dynamic Products composés — réassurance · bandeau Pro · ordre V1.2 en attente maquette.

Toute demande dépassant le Website Builder ou le socle livré = **constat limite Odoo + arbitrage MOA + ticket séparé**.

---

## 15. Rappel impératif

```text
GO exécution encadré ≠ autorisation générale CK
Verrou levé ticket 01 uniquement — maintenu pour tout autre périmètre
Extension / écart = constat limite Odoo + arbitrage MOA + ticket séparé
Phase CMS MOA ≠ autorisation Dev hors Website Builder
```

---

*Ticket `dorevia_ck_theme_01_socle_tokens_layout_snippets` — validé MOA · exécution encadrée autorisée · document opposable.*
