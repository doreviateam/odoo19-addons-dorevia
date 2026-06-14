# Revue Dev — Traduisibilité Odoo — Maquette CK V1.1

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Ticket** | `ticket_dev_maquette_01_open_design` |
| **Références** | `design_01.md` v1.1 · `cadrage_01.md` · `recette_qa_maquette_01.md` (V1.1 validée) |
| **Artefact** | `/Users/doreviateam/open-design/.od/projects/ck-marketone-maquette-v1/index.html` |
| **Date** | 2026-06-12 |
| **Auteur** | Dev de référence Odoo 19 CE |
| **Verrou Odoo** | **Maintenu** — cette revue ne lève pas le verrou |

---

## 1. Synthèse Dev

```text
VERDICT : MAQUETTE V1.1 TRADUISIBLE DANS ODOO
          sous réserve des arbitrages MOA listés en §8
          et d’une grille thème / template / extension validée par David
```

La maquette V1.1 est **compatible** avec la doctrine :

```text
Odoo = source de vérité métier
website_sale = moteur boutique
Thème Odoo = première implémentation visuelle
Extensions = minimales, justifiées MOA
```

**Pas de GO** base Odoo, module `dorevia_ck_theme`, QWeb ou SCSS à ce stade.

---

## 2. Checklist compatibilité Odoo (`design_01` §22)

| Critère | Statut | Commentaire Dev |
|---------|--------|-----------------|
| Acheteur comprend ce que CK vend | OK | Hero + boutique + catégories univers |
| Catégories principales visibles | OK | Pills accueil + arborescence sidebar |
| Produits visibles et désirables | OK | Placeholders acceptables phase 1 |
| Prix lisibles | OK | Cartes + fiche |
| CTA achat clair | OK | « Voir » grille → « Ajouter au panier » fiche |
| Fiche permet de décider | OK | Buy box complet |
| Réassurance visible | OK | Accueil + fiche |
| Entrée pro sans dominer B2C | OK | Header + bandeau |
| Pas de boutique parallèle comme cible | OK | QA V1.1 + action « Voir » |
| Origines / collections / prix annotés | OK | `annotation_composants_odoo.md` |
| Quick-add ≠ panier custom | OK | Non retenu MOA |
| Entrée pro = signal / formulaire | OK | Pas portail |
| Tokens documentés | OK | `tokens.md` — export SCSS possible |
| Filtres = navigation Odoo cible | OK | Pas catalogue JS comme spec |
| Panier / checkout = Odoo standard | OK | Hors maquette — `website_sale` |

**Score checklist : 15/15** — traduisibilité **acceptable** pour passage grille formelle.

---

## 3. Grille écran par écran

### 3.1 Accueil

| Élément maquette | Couche Odoo | Mécanisme Odoo 19 CE | Complexité |
|------------------|-------------|----------------------|------------|
| Header | Thème + template | Héritage `website.layout` | Faible |
| Hero promesse + CTA | Thème / snippet | Snippet Website Builder ou QWeb statique | Faible |
| Pills univers (4 familles) | Template + thème | Liens `product.public.category` parentes | Faible |
| Produits vedettes (4 cartes) | Snippet + thème | Snippet manuel ou dynamique produits mis en avant | Moyenne si dynamique |
| Bandeau réassurance | Thème / snippet | Snippet statique | Faible |
| Note `product.public.category` | Doc / cadrage | Paramétrage BO catégories e-commerce | Faible |

**Verdict accueil** : **≥ 80 % thème + snippets** — pas d’extension requise phase 1.

---

### 3.2 Page `/shop`

| Élément maquette | Couche Odoo | Mécanisme Odoo 19 CE | Complexité |
|------------------|-------------|----------------------|------------|
| Titre + promesse | Template + thème | Héritage `website_sale.products` | Faible |
| Arborescence catégories sidebar | Template natif + thème | `product.public.category` hiérarchiques, liens `/shop/category/...` | Faible à moyenne |
| Filtre origines | **À trancher** | Option A : `product.attribute` « Origine » + filtre attribut | Moyenne |
| | | Option B : extension modèle dédié (comme ancien Marketone) | Élevée — à justifier MOA |
| Filtre collections | **À trancher** | Option A : tags / catégories secondaires | Moyenne |
| | | Option B : modèle `marketone.shop.collection` | Élevée — non reprise auto |
| Filtre prix (fourchette) | **À trancher** | CE : limité — pricelist + catégories ou extension filtre | Moyenne à élevée |
| Tri toolbar | Template natif + thème | `?order=` natif `website_sale` | Faible |
| Grille produits | Template + thème | Tuiles `website_sale` | Faible |
| Carte produit (image, prix, chips) | Thème + template | SCSS tokens + QWeb tuile | Faible |
| Action « Voir » | Template natif | Lien vers `/shop/product/...` (comportement standard) | Faible |
| Badge pack | Template + thème | Produit pack = 1 fiche Odoo si `non_detailed` | Moyenne — doctrine MOA |
| Pagination | Template natif + thème | Pager Odoo | Faible |
| Drawer filtres mobile | Thème | CSS/JS léger sur layout Odoo — pas filtre JS catalogue | Faible |
| Bandeau pro | Snippet + page CMS | Page « Professionnels » + formulaire contact | Faible |

**Verdict `/shop`** : **socle natif `website_sale` suffisant** pour phase 1 si origines = attribut produit et collections = catégories/tags. Sinon extensions ciblées.

---

### 3.3 Fiche produit

| Élément maquette | Couche Odoo | Mécanisme Odoo 19 CE | Complexité |
|------------------|-------------|----------------------|------------|
| Fil d’Ariane | Template natif + thème | Standard `website_sale` | Faible |
| Galerie | Template natif + thème | Images produit Odoo | Faible |
| Buy box (prix, qty, CTA) | Template natif + thème | Widget fiche produit standard | Faible |
| Chips origine / catégorie | Template + thème | Attribut + `public_categ_ids` | Faible à moyenne |
| Bloc usage éditorial | Template + thème | `description_sale` ou champ custom léger | Faible |
| Réassurance fiche | Thème / snippet | Bloc statique ou snippet | Faible |
| Produits liés | Template natif + thème | `alternative_product_ids` | Faible |

**Verdict fiche** : **100 % template natif + thème** — aucune extension obligatoire phase 1.

---

## 4. Répartition globale estimée

| Couche | Part estimée phase 1 | Commentaire |
|--------|----------------------|-------------|
| **Thème** (`dorevia_ck_theme`) | ~55 % | Tokens, header, footer, cartes, sidebar visuelle, responsive, snippets réassurance |
| **Template natif** `website_sale` | ~35 % | Shop, fiche, tri, pagination, recherche, panier/checkout (hors maquette) |
| **Extension à justifier** | ~10 % | Origines, collections, filtre prix — selon arbitrage MOA |
| **Front autonome** | 0 % | Interdit |

---

## 5. Tokens → SCSS Odoo

Le fichier `tokens.md` est **directement transposable** en variables SCSS du futur `dorevia_ck_theme` :

```scss
// Mapping validé Dev — base V1 MOA
$ck-bg: #FFFBF7;
$ck-primary: #D84315;
$ck-secondary: #2E7D4F;
$ck-text: #1C1917;
// … voir tokens.md
```

**Points avant prod** :

- Fraunces + DM Sans : self-host ou polices Odoo — arbitrage MOA pré-prod ;
- Google Fonts en maquette uniquement — ne pas figer en prod sans décision.

---

## 6. Interactions maquette vs cible Odoo

| Interaction maquette V1.1 | Cible Odoo | Verdict |
|---------------------------|------------|---------|
| Liens ancres inter-écrans | Routes Odoo réelles | OK — maquette seulement |
| Drawer filtres mobile (JS démo) | Accordéon / offcanvas CSS + liens filtre URL | OK — pas de filtre JS catalogue |
| Menu burger mobile (JS démo) | Menu responsive thème ou offcanvas | OK |
| Qty +/- fiche (JS démo) | Widget qty natif fiche produit | OK |
| Badge panier « 2 » | `sale_get_order()` | OK — démo uniquement |
| Checkboxes filtres sidebar | Liens `/shop` avec domaine / attribut | OK — rechargement page |

**Aucune interaction** de la maquette V1.1 n’impose catalogue JS, panier localStorage ou checkout custom.

---

## 7. Rapport à `dorevia_ckreyol_marketone` (mémoire, pas reprise)

| Besoin maquette V1.1 | Existant Marketone | Recommandation Dev |
|----------------------|-------------------|-------------------|
| Catégories hiérarchiques | `product.public.category` + sidebar | **Natif Odoo** — ne pas reprendre modèle custom en premier choix |
| Origines sidebar | `marketone.shop.origin` | **Évaluer** `product.attribute` avant extension |
| Collections | `marketone.shop.collection` | **Évaluer** catégories/tags avant modèle dédié |
| Tuiles produit | SCSS + QWeb existants | **Référence visuelle** uniquement — pas reprise code auto |
| Portes SEO `/shop?…` | Routes custom | **Phase 2+** — pas requis phase 1 thème |

---

## 8. Arbitrages MOA encore requis avant implémentation

| # | Sujet | Impact traduction | Recommandation Dev (non décision) |
|---|-------|-------------------|----------------------------------|
| 1 | Packs `non_detailed` | Affichage pack, ligne panier | Confirmer doctrine — aligner produit pack Odoo standard |
| 2 | Origines | Sidebar + chips | Préférer `product.attribute` en phase 1 |
| 3 | Collections | Filtre sidebar | Préférer catégories secondaires ou tags en phase 1 |
| 4 | Filtre prix UI | Sidebar | Reporter ou extension légère si CE insuffisant |
| 5 | Entrée pro | CTA | Page CMS + `website.form` / `website_crm` — pas portail |
| 6 | Typo prod | Thème | Décision avant build `dorevia_ck_theme` |
| 7 | Levée verrou Odoo | Projet | Décision David explicite post-grille validée |

---

## 9. Risques identifiés (alertes Dev)

| Risque | Niveau | Mitigation |
|--------|--------|------------|
| Reprise auto code `dorevia_ckreyol_marketone` | Élevé | Doctrine : analyse seulement — grille §7 |
| Extension collections/origines trop tôt | Moyen | Phase 1 = natif Odoo max |
| Filtre prix bloquant | Moyen | UI optionnelle phase 1 prod |
| Google Fonts en prod | Faible | Self-host ou stack système |
| Barre `screen-tabs` maquette copiée en prod | Faible | Retirer — aide navigation maquette uniquement |

---

## 10. Décision Dev proposée

```text
Statut : REVUE TRADUISIBILITÉ ODOO — FAVORABLE AVEC RÉSERVES MOA

La maquette V1.1 peut servir de référence visuelle et UX
pour la grille thème / template / extension.

Prochaine étape MOA / Loulou :
  formaliser la grille validée (document opposable)

Prochaine étape technique (après décision David) :
  1. Arbitrer §8
  2. Rédiger ticket dorevia_ck_theme (socle tokens + layout)
  3. Créer base Odoo dev — uniquement si verrou levé
  4. Implémenter thème avant extensions
```

**Verrou Odoo** : **maintenu** jusqu’à :

```text
□ Grille thème / template / extension validée MOA
□ Arbitrages §8 tranchés (minimum : origines, collections, packs)
□ Décision David explicite de levée du verrou (cadrage_01 §27)
```

---

## 11. Synthèse une phrase

> La maquette CK V1.1 est traduisible en thème Odoo + templates `website_sale` natifs pour l’essentiel ; les seuls points structurants à trancher avant code sont origines, collections, filtre prix et doctrine packs — sans cela, on peut déjà démarrer un `dorevia_ck_theme` minimal (tokens, header, tuiles) après levée explicite du verrou.
