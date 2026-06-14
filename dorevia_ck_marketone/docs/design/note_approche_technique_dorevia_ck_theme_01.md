# Note d’approche technique — `dorevia_ck_theme`

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Type** | Note d’approche Dev — préalable levée verrou Odoo |
| **Module cible** | `dorevia_ck_theme` — **livré · socle ticket 01 clôturé** |
| **Odoo cible** | 19 CE — `website`, `website_sale`, `website_crm` |
| **Références** | Maquette V1.1.1 validée QA · [`grille_traduction_odoo_v1.md`](./maquette_01/grille_traduction_odoo_v1.md) · [`note_transmission_arbitrage_david_01_v1_1.md`](./maquette_01/note_transmission_arbitrage_david_01_v1_1.md) · [`tokens.md`](./maquette_01/tokens.md) |
| **Date** | 2026-06-12 |
| **Statut** | **Validée MOA** — ticket 01 clôturé côté socle · phase CMS MOA |
| **Chemin canonique** | `docs/design/note_approche_technique_dorevia_ck_theme_01.md` |

> **Transmission MOA** : ce fichier contient la note d’approche Dev **intégrale**. Il ne s’agit pas d’un raccourci.

### Référentiel technique projet

```text
Odoo 19 CE · snippets first · pas de surcouche autonome
```

| Pilier | Lecture |
|--------|---------|
| **Odoo 19 CE** | `website`, `website_sale`, `website_crm` — source de vérité métier et moteur e-commerce |
| **Snippets first** | Website Builder, snippets natifs, pages CMS — contenu éditorial éditable avant tout custom |
| **Pas de surcouche autonome** | Pas de front parallèle, pas de HTML maquette injecté, pas de catalogue/panier/checkout custom |

Ce référentiel s’applique au futur `dorevia_ck_theme` et à toute implémentation post-levée du verrou.

---

## Grille de vérification MOA (synthèse)

| Point MOA | Engagement Dev | Section |
|---------|----------------|---------|
| Usage **prioritaire** des snippets Odoo natifs | Oui — accueil, Pro, réassurance en snippets ; shop en `website_sale` natif | §1, §4.1 |
| **Absence** de page front autonome | Oui — pas de HTML maquette injecté ; pas de catalogue/panier parallèle | §1, §2, §4.5 |
| **Éditabilité** Website Builder | Oui — hero, Pro, bandeaux, formulaire CRM éditables ; shop stylé seulement | §4.4 |
| Périmètre **strict** `dorevia_ck_theme` | Oui — tokens + layout + snippets ; hors ticket 1 = extensions interdites | §3 |
| QWeb/SCSS **minimal** seulement | Oui — héritages layout/products/product + assets ; pas de shop recréé | §4.2, §4.3 |
| **Pas** de portail B2B custom ni surcouche front | Oui — B2B = Odoo natif BO ; CRM qualification ; pas tunnel custom | §2, §3, §4.6 |

---

## Objet

Avant toute levée du verrou Odoo, confirmer que le futur thème CK suivra une approche **Odoo-native / snippets first**, et non une reproduction autonome de la maquette HTML sous forme de gros blocs indépendants.

```text
Maquette V1.1.1 validée QA ≠ GO Dev général CK.
Arbitrages MOA §10 tranchés ≠ GO Dev général CK.
Verrou levé ticket 01 uniquement — hors ticket 01 : verrou maintenu.
```

**Autorisé ticket 01** (GO exécution encadré MOA) : module `dorevia_ck_theme` · QWeb/SCSS minimal · snippets — périmètre strict ticket 01.

**Interdit hors ticket 01** : extension · module métier · front autonome · configuration B2B · tout écart sans ticket séparé + arbitrage MOA.

---

## 1. Principe attendu

Le futur thème CK **ne doit pas** être une page front autonome plaquée dans Odoo.

Il doit s’appuyer **prioritairement** sur :

```text
snippets Odoo natifs
zones éditables du Website Builder
structures standard Odoo Website
classes, grilles et mécanismes compatibles avec l’édition Odoo
tokens / variables / ajustements de thème
adaptations légères de layout et de style
```

**Principe directeur Dev** :

> Habiller Odoo proprement — ne pas réinventer le site.

```text
Priorité 1 : snippets natifs + Website Builder
Priorité 2 : tokens SCSS + héritages légers website_sale
Priorité 3 : QWeb minimal (layout, hooks)
Priorité 4 : extension custom — hors ticket thème 1, si limite Odoo démontrée
```

---

## 2. Ce que nous voulons éviter

```text
gros blocs HTML/CSS autonomes étrangers aux snippets Odoo
sections non éditables dans le Website Builder
page reconstruite hors logique Odoo
thème rendant le contenu difficile à maintenir par un utilisateur fonctionnel
empilement de QWeb/SCSS custom alors que le standard Odoo peut porter le besoin
implémentation qui réinvente le site au lieu d’habiller proprement Odoo
catalogue / panier / checkout parallèles
portail B2B transactionnel custom phase 1
```

| Visé | Évité |
|------|-------|
| Snippets réutilisables et éditables | Surcouche front indépendante |
| Tuiles `website_sale` stylées | Catalogue JS local comme spec |
| Page CMS Pro + `website_crm` | Landing Pro HTML monolithique |
| Filtres = URLs / domaine natif | Filtres maquette en JS local |
| B2B = partenaires + pricelists Odoo BO | Prix B2B publics / tunnel custom |

---

## 3. Périmètre du futur ticket (si GO ultérieur)

**Module** : `dorevia_ck_theme` — **strictement borné**.

### Autorisé (ticket 1)

```text
socle tokens · variables de thème · palette
typographie (sous réserve validation technique)
espacements · boutons · cartes · layout général
adaptation visuelle légère des snippets / pages Odoo standard
enregistrement snippets CK réutilisables
```

### Hors périmètre (ticket 1)

```text
origines custom · collections custom · filtre prix avancé
portail B2B custom · tunnel B2B spécifique · module métier
catalogue parallèle · front autonome · logique transactionnelle hors standard Odoo
```

**B2B** : porté naturellement par Odoo — `res.partner`, `product.pricelist`, `crm.lead`, devis, commandes, portail client, back-office. **Pas dans le ticket thème 1.**

Cette mention ne vaut pas activation ni configuration des pricelists, devis, portail client ou parcours B2B dans le ticket 1. Ces éléments restent hors périmètre de `dorevia_ck_theme` et relèveront d’un arbitrage / paramétrage séparé.

---

## 4. Réponses Dev aux questions MOA

### 4.1 Quels snippets Odoo natifs pour la structure maquette ?

| Zone maquette | Snippet / natif Odoo | Éditable Builder |
|---------------|----------------------|------------------|
| Header / footer | Héritage `website.layout` | Menu, logo, footer |
| Hero accueil | **Banner** ou **Text-Image** | Oui |
| Pills univers | **Links** → `/shop/category/...` | Oui |
| Produits vedettes | **Dynamic Products** / **Products** | Oui (sélection BO) |
| Réassurance | **Features** / **Columns** | Oui |
| Intro `/shop` | Texte page shop ou snippet tête | Partiel |
| Grille produits | `website_sale.products` — **non recréé** | Produits = BO |
| Sidebar catégories | `product.public.category` / snippet **Categories** | Catégories = BO |
| Tri / pagination | Natif `website_sale` | Non |
| Bandeau Pro `/shop` | Snippet + lien CMS `/professionnels` | Oui |
| Espace Pro | **Page CMS** + **Columns** + formulaire **`website_crm`** | Oui |
| Fiche produit | `website_sale.product` | Description = BO |
| Note prix B2C | Snippet ou bloc CMS shop / Pro | Oui |

La maquette single-page HTML = **référence visuelle**. En Odoo : **pages CMS + snippets + templates website_sale**.

---

### 4.2 Quelles parties = thème / CSS / tokens uniquement ?

| Élément | Couche |
|---------|--------|
| Palette corail / vert | Variables SCSS `$ck-*` ([`tokens.md`](./maquette_01/tokens.md)) |
| Typo Fraunces + DM Sans | À valider prod — `@font-face` ou thème parent |
| Espacements, radius, ombres | SCSS thème |
| Boutons primary / secondary / pro | Override Bootstrap / thème Odoo |
| Cartes produit, badges, chips | SCSS sur tuiles `website_sale` |
| Header sticky, drawer filtres mobile | SCSS + offcanvas sur structure Odoo |

**Estimation** : ~55 % effort visuel = tokens + SCSS (grille v1).

---

### 4.3 Quelles parties nécessitent du QWeb ?

QWeb **minimal** — hooks d’intégration uniquement :

| Zone | Rôle |
|------|------|
| `website.layout` (héritage) | Assets SCSS, classes body, header/footer |
| `website_sale.products` (héritage léger) | Layout sidebar, classes tuiles, note B2C |
| `website_sale.product` (héritage léger) | Chips, spacing buy box |
| Snippets XML | Enregistrement snippets CK dans le builder |

**Pas de QWeb** : panier, checkout, portail, filtres custom, logique B2B.

---

### 4.4 Quelles parties restent éditables Website Builder ?

| Éditable | Non éditable (templates métier stylés) |
|----------|--------------------------------------|
| Hero, réassurance, bandeaux Pro | Grille shop |
| Page Espace pro, double cible, CTA | Buy box, panier, checkout |
| Formulaire `website_crm` | Tri, pagination, recherche |
| Menu, footer, pages légales | |
| Textes intro, note prix B2C | |

---

### 4.5 Quoi ne pas reproduire à l’identique ?

| Maquette | Raison |
|----------|--------|
| Single-page `#accueil` `#shop` `#pro` `#produit` | Routes Odoo distinctes |
| Filtres checkboxes JS | URLs / attributs natifs ; filtre prix simplifié ou reporté |
| Formulaire Pro HTML statique | `website_crm` |
| Quick-add | Non retenu MOA |
| Catégories figées HTML | `product.public.category` BO |
| Données prix/stock fictives | Catalogue réel |

---

### 4.6 Risques de dérive front autonome

| Risque | Mitigation |
|--------|------------|
| Shop recréé en QWeb | Héritage + SCSS seulement |
| Catalogue JS | Interdit — doctrine projet |
| Hero / Pro non snippet | Enregistrer snippets + page CMS |
| Extension précoce origines/collections/prix | Hors ticket 1 ; MOA §10 |
| B2B UI sur site public | CRM + pricelists back-office |
| Copier-coller HTML maquette en `/static` | Interdit |

---

### 4.7 Règle de décision proposée

```text
Standard Odoo suffit SI :
  → website_sale / website / website_crm couvre le comportement
  → besoin visuel ou éditorial (tokens, snippet)
  → contenu modifiable par utilisateur fonctionnel
  → pas de nouvelle donnée métier

Custom minimal (SCSS / xpath léger) SI :
  → standard existe mais rendu natif insuffisant pour lisibilité MOA
  → héritage template existant, pas de logique métier dupliquée

Extension séparée (hors ticket 1) SI :
  → limite Odoo démontrée après thème + natif
  → arbitrage MOA explicite
```

**Phrase opérationnelle** :

> Snippet ou natif d’abord · SCSS ensuite · xpath minimal · module métier en dernier recours.

---

## 5. Décision projet actuelle

| Élément | Statut |
|---------|--------|
| Maquette V1.1.1 | Validée QA |
| Arbitrages §10 MOA | Tranchés |
| Documentation | Alignée |
| Cette note | **Validée MOA** |
| Ticket 01 | **Validé MOA — squelette validé QA statique** |
| Verrou Odoo | **Levé ticket 01 uniquement** |
| GO Dev général CK | **Non** |
| Recette fonctionnelle | **Suspendue — instance Odoo 19 CE** |

```text
Squelette dorevia_ck_theme : OK QA statique (recette_qa_dorevia_ck_theme_01_squelette.md)
Prochaine étape : instance Odoo 19 CE + recette fonctionnelle
Hors ticket 01 : verrou maintenu · ticket séparé requis
```

---

## 6. Séquence si validation MOA + levée verrou

```text
1. ✅ Validation MOA de cette note
2. ✅ Validation MOA ticket 01
3. ✅ Levée verrou Odoo (ticket 01 uniquement)
4. ✅ Squelette dorevia_ck_theme — validé QA statique
5. ⏳ Instance Odoo 19 CE + recette QA fonctionnelle
6. Pages CMS Pro + website_crm (post-instance)
7. Extensions uniquement si limite Odoo démontrée (ticket séparé + arbitrage MOA)
```

---

## 7. Validation MOA attendue

| Question | Décision MOA |
|----------|--------------|
| Approche snippets first validée ? | ✅ Oui |
| Périmètre ticket 1 validé ? | ✅ Oui |
| Levée verrou Odoo | ✅ Levé ticket 01 · ☐ Levé projet entier |

---

*Document dédié — note d’approche technique. Exécution encadrée ticket 01 autorisée MOA — verrou levé ticket 01 uniquement.*
