# Spécification finale développeur — Card produit « Nos coups de cœur » V1.1

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Écran** | Page index `/` |
| **Section** | Home · Section 3 « Nos coups de cœur » |
| **Objet** | Enrichissement de la card produit home |
| **Statut** | Spécification finale dev à implémenter |
| **Base existante** | Section 3 curation BO livrée (`dorevia_ck_marketone_content` ≥ `19.0.1.18.4`) |

---

## 1. Décision MOA

La card **« Nos coups de cœur »** est une card e-commerce enrichie, pilotée depuis Odoo.

Elle n'est pas une card éditoriale figée, et elle ne doit pas contenir de données commerciales codées en dur.

Règle générale :

```text
Catégorie « Coups de cœur » → sélection home
Ruban produit → badge visuel
Étiquettes commerciales → ligne descriptive visible
Prix + quantité nette → information commerciale
Image + nom → contenu produit
```

La catégorie **« Coups de cœur »** est une catégorie de pilotage. Elle ne doit jamais être affichée comme information client dans la card.

---

## 2. Périmètre

### Inclus

- Card produit affichée dans la section home **« Nos coups de cœur »**.
- Données issues du catalogue Odoo.
- Rendu SSR custom CK existant (`home_featured.py`).
- Produits simples et variantes.
- Badge via ruban e-commerce Odoo.
- Ligne descriptive client.
- Quantité nette commerciale.
- Prix de référence au kg ou au litre quand calculable.
- CTA de card plus explicite.

### Exclu

- Refonte complète de la card `/shop`.
- Modification du tunnel panier / checkout.
- Ajout direct au panier depuis la home.
- Wishlist fonctionnelle.
- Moteur éditorial avancé.
- IA de recommandation.
- Règle automatique de diversification visuelle.

---

## 3. Sélection des produits

Cette spec ne modifie pas la règle de sélection déjà actée.

Un produit est éligible à la section si :

1. il appartient à la catégorie e-commerce **« Coups de cœur »** ;
2. il est publié sur le site ;
3. il est vendable ;
4. il possède une image exploitable ;
5. il respecte la règle variantes → cartes.

Règles complémentaires :

- nombre de cards variable ;
- plafond technique : **8 cards** en mode curaté ;
- fallback technique : **5 premiers produits publiés avec image** uniquement si la catégorie « Coups de cœur » est vide ;
- ne pas compléter artificiellement la grille avec Galettes, Savon ou tout autre produit hors catégorie.

---

## 4. Structure cible de la card

Structure visuelle attendue :

```text
┌────────────────────────────┐
│ [Image produit]     [Ruban]│
├────────────────────────────┤
│ Confiture de goyave        │
│ Réunion · Épicerie         │
│                            │
│ 5,80 €                     │
│ 320 g · 18,13 €/kg         │
│                            │
│ [Voir le produit]          │
└────────────────────────────┘
```

Amendement MOA/dev : l'icône d'étiquette et la wishlist ne sont pas retenues en V1.1. Elles ajoutent du bruit visuel et une dette fonctionnelle non nécessaire.

---

## 5. Sources de données

| Zone card | Source Odoo | État |
|-----------|-------------|------|
| Éligibilité | `product.public.category` xmlid `public_categ_coups_de_coeur` | Existant |
| Publication | `is_published` / `website_published` | Existant |
| Vendable | `sale_ok` | Existant |
| Image | `product.product.image_*` puis `product.template.image_*` | Existant |
| Nom | Nom variante si pertinent, sinon nom template | Existant |
| Prix TTC | `_get_combination_info()` / pricing website | Existant |
| Badge | `product.template.website_ribbon_id` | Existant |
| Ligne descriptive | Champ à arbitrer, voir §6 | Nouveau |
| Quantité nette | Champ custom à créer | Nouveau |
| Unité quantité nette | Champ custom à créer | Nouveau |
| Unité prix référence | Champ custom à créer | Nouveau |
| Affichage prix référence | Champ custom à créer | Nouveau |
| CTA | URL fiche produit / variante | Existant, libellé à modifier |

---

## 6. Ligne descriptive client

### 6.1 Besoin

La ligne descriptive sous le nom du produit affiche des informations compréhensibles par le client :

- origine ;
- famille commerciale ;
- univers ;
- type de produit ;
- sélection particulière.

Exemple :

```text
Réunion · Épicerie
```

### 6.2 Amendement technique

Le brouillon parle d'un champ **« Étiquettes »**. Ce champ ne doit pas être supposé existant sans vérification Odoo.

Implémentation recommandée V1.1 :

1. Ajouter un champ custom sur `product.template` :
   - nom technique proposé : `ck_featured_label_ids` ;
   - type : `many2many` vers un modèle simple `dorevia.ck.product.label` ;
   - libellé BO : **Étiquettes card home**.
2. Ajouter le modèle `dorevia.ck.product.label` :
   - `name` obligatoire ;
   - `sequence` entier ;
   - `active` booléen.

Alternative acceptable si le codebase dispose déjà d'un modèle standard de tags produit e-commerce exploitable en website :

- utiliser ce modèle standard ;
- documenter le champ exact ;
- garantir que la catégorie **« Coups de cœur »** n'est jamais affichée comme étiquette client.

### 6.3 Règles d'affichage

- Afficher les étiquettes dans l'ordre `sequence asc, name asc`.
- Séparer par ` · `.
- Masquer la ligne si aucune étiquette n'est renseignée.
- Ne pas afficher d'icône en V1.1.
- Ne jamais afficher **« Coups de cœur »** dans cette ligne.

---

## 7. Ruban / badge

Le badge haut droite provient du champ Odoo :

```text
website_ribbon_id
```

Règles :

- ruban renseigné → badge affiché ;
- ruban vide → aucun badge ;
- libellé affiché = libellé du ruban Odoo ;
- aucun badge générique forcé ;
- position : haut droite sur l'image.

Les styles existants `badge-new`, `badge-heart`, `badge-ribbon`, `badge-float` peuvent être conservés.

---

## 8. Quantité nette et prix de référence

### 8.1 Champs à créer

Ajouter les champs suivants sur `product.template`.

| Champ BO | Nom technique proposé | Type | Exemple |
|----------|-----------------------|------|---------|
| Quantité nette commerciale | `ck_net_quantity` | `Float` | `320` |
| Unité quantité nette | `ck_net_quantity_uom` | `Selection` | `g` |
| Unité prix de référence | `ck_reference_price_uom` | `Selection` | `kg` |
| Afficher le prix de référence | `ck_show_reference_price` | `Boolean` | `True` |

Les champs doivent apparaître dans l'onglet eCommerce de la fiche produit.

### 8.2 Variantes

V1.1 pragmatique :

- les champs sont portés par `product.template` ;
- toutes les variantes héritent de ces informations ;
- si une variante doit avoir une quantité différente, cela fera l'objet d'un lot ultérieur.

Amendement : le brouillon évoquait des informations propres à la variante. C'est pertinent, mais plus coûteux. Pour V1.1, on évite la sur-modélisation.

### 8.3 Unités acceptées

Minimum V1.1 :

```text
g
kg
ml
cl
l
pièce
```

Valeurs techniques proposées :

```text
g, kg, ml, cl, l, unit
```

Libellé affiché pour `unit` : `pièce`.

### 8.4 Calcul prix de référence

Le prix de référence est calculé à partir du prix TTC affiché sur le site.

Pour grammes → kilogramme :

```text
prix_kg = prix_ttc / (quantité_g / 1000)
```

Exemple :

```text
5,80 € / 0,320 kg = 18,125 €/kg → 18,13 €/kg
```

Pour millilitres → litre :

```text
prix_l = prix_ttc / (quantité_ml / 1000)
```

Pour centilitres → litre :

```text
prix_l = prix_ttc / (quantité_cl / 100)
```

Pour kilogrammes → kilogramme :

```text
prix_kg = prix_ttc / quantité_kg
```

Pour litres → litre :

```text
prix_l = prix_ttc / quantité_l
```

Pour `pièce`, ne pas calculer de prix de référence V1.1.

### 8.5 Règles d'affichage

Si quantité et unité sont renseignées :

```text
320 g
```

Si quantité, unité, prix et unité de référence sont calculables, et si `ck_show_reference_price = True` :

```text
320 g · 18,13 €/kg
```

Si le prix de référence n'est pas calculable :

```text
320 g
```

Si aucune quantité nette n'est renseignée :

- masquer la ligne ;
- ne pas afficher de placeholder.

---

## 9. CTA de card

V1.1 retient le CTA :

```text
Voir le produit
```

Raisons :

- l'ajout direct panier depuis home demande de gérer variantes, tracking panier, stock, erreurs et UX de confirmation ;
- le libellé actuel `Voir` est trop faible ;
- `Voir le produit` est explicite et compatible avec l'architecture actuelle.

Règles :

- lien vers `variant.website_url` si disponible ;
- sinon `product.template.website_url` ;
- fallback `/shop` uniquement si aucune URL produit n'est disponible.

---

## 10. Rendu HTML attendu

Le HTML peut rester généré par `build_featured_product_card_html()`.

Structure cible minimale :

```html
<article class="ck-product-card product-card">
  <a class="product-card-media ck-product-card__media" href="...">
    <span class="badge ... badge-float">Nouveau !</span>
  </a>
  <div class="product-card-body">
    <h3><a href="...">Confiture de goyave</a></h3>
    <p class="product-card-labels">Réunion · Épicerie</p>
  </div>
  <div class="product-card-foot">
    <div class="product-card-pricing">
      <span class="price">5,80 €</span>
      <span class="reference-price">320 g · 18,13 €/kg</span>
    </div>
    <a class="card-cta" href="...">Voir le produit</a>
  </div>
</article>
```

Amendement : le nom produit doit rester avant les étiquettes. Le prix et la quantité doivent être groupés visuellement pour éviter un pied de card trop horizontal et instable sur mobile.

---

## 11. Refresh / reconstruction

La section étant pré-rendue dans l'arch de la home, elle doit être reconstruite lorsque les champs suivants changent :

- `public_categ_ids` ;
- `is_published` ;
- `website_published` ;
- `website_sequence` ;
- `sale_ok` ;
- `website_ribbon_id` ;
- `list_price` ;
- `image_1920` ;
- `image_512` ;
- `ck_featured_label_ids` ;
- `ck_net_quantity` ;
- `ck_net_quantity_uom` ;
- `ck_reference_price_uom` ;
- `ck_show_reference_price`.

Ajouter ces nouveaux champs à la logique de refresh existante dans `models/product_template.py`.

---

## 12. Critères de recette

| # | Critère |
|---|---------|
| R1 | Produit publié, vendable, imagé, dans « Coups de cœur » → card affichée. |
| R2 | Produit retiré de « Coups de cœur » → card absente après reconstruction. |
| R3 | Produit non publié → absent même s'il est dans « Coups de cœur ». |
| R4 | Ruban `Nouveau !` → badge `Nouveau !`; sans ruban → pas de badge. |
| R5 | Étiquettes `Réunion`, `Épicerie` → `Réunion · Épicerie`. |
| R6 | La catégorie « Coups de cœur » n'apparaît jamais dans la ligne descriptive. |
| R7 | Quantité `320` + unité `g` → `320 g`. |
| R8 | Prix `5,80 €`, quantité `320 g`, référence `kg` → `320 g · 18,13 €/kg`. |
| R9 | Quantité absente → ligne quantité masquée. |
| R10 | Manio Crackers avec variantes salé/sucré → deux cards si le parent est dans « Coups de cœur ». |
| R11 | Trois cards éligibles → trois cards affichées, pas cinq forcées. |
| R12 | Plus de huit cards éligibles → huit premières selon `website_sequence`. |
| R13 | CTA affiché = `Voir le produit`, lien vers la bonne fiche / variante. |
| R14 | Mobile 390 : aucun chevauchement, prix et CTA lisibles. |
| R15 | Desktop 1280 : alignement visuel stable, cartes homogènes. |

---

## 13. Fichiers à modifier

| Fichier | Action |
|---------|--------|
| `dorevia_ck_marketone_content/home_featured.py` | Ajouter helpers labels, quantité nette, prix référence, nouveau HTML card. |
| `dorevia_ck_marketone_content/models/product_template.py` | Ajouter champs custom + refresh fields. |
| `dorevia_ck_marketone_content/views/product_template_views.xml` | Afficher les champs dans l'onglet eCommerce. |
| `dorevia_ck_marketone_content/security/ir.model.access.csv` | Accès au modèle d'étiquettes si modèle custom retenu. |
| `dorevia_ck_theme/static/src/scss/website.scss` | Styles card V1.1 : labels, pricing group, reference price, CTA long. |
| `dorevia_ck_marketone_content/tests/test_ck_home_section3_curation.py` | Tests labels, quantité, prix référence, CTA. |

Créer une migration `19.0.1.19.0` ou version suivante selon la séquence module.

---

## 14. Points d'attention dev

- Ne pas utiliser la catégorie **« Coups de cœur »** comme étiquette visible.
- Ne pas réintroduire le badge forcé par position.
- Ne pas forcer 5 cards en mode curaté.
- Échapper les libellés HTML (`escape`) comme pour les champs existants.
- Utiliser `format_amount` pour les montants.
- Gérer division par zéro et quantité négative ou nulle.
- Ne pas casser les tests Section 3 existants.
- Garder `/shop` inchangé.

---

## 15. Commande de vérification attendue

```bash
docker exec sandbox-odoo19-odoo-1 bash -c \
  'odoo -d dorevia_ck_marketone_01 --http-port=8079 --no-http \
   -u dorevia_ck_theme,dorevia_ck_marketone_content \
   --test-tags dorevia_ck_marketone_home_section3_curation,dorevia_ck_marketone_home_section3 \
   --stop-after-init'
```

---

## 16. Synthèse pour développement

La V1.1 doit enrichir la card sans changer le principe Section 3 :

```text
Sélection = catégorie Coups de cœur
Badge = ruban Odoo
Description = étiquettes client dédiées
Information commerciale = prix + quantité nette + prix référence
Action = Voir le produit
```

La priorité est la lisibilité commerciale et la maîtrise BO, sans refonte du système eCommerce.

