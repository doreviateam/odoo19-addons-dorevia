# Ticket Dev — Card produit « Nos coups de cœur » V1.1

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Type** | Ticket Dev · Home Section 3 |
| **Objet** | Enrichir la card produit « Nos coups de cœur » |
| **Spec de référence** | [`SPEC_DEV_CARD_PRODUIT_COUPS_DE_COEUR_V1_1.md`](./SPEC_DEV_CARD_PRODUIT_COUPS_DE_COEUR_V1_1.md) |
| **Base technique** | `dorevia_ck_marketone_content` ≥ `19.0.1.18.4` |
| **Statut** | À développer |

---

## Message au dev

La Section 3 **« Nos coups de cœur »** est maintenant actée comme une vitrine produit pilotée par Odoo :

```text
Sélection = catégorie e-commerce « Coups de cœur »
Badge = ruban Odoo
Nombre de cards = variable, max 8
Fallback = 5 premiers produits uniquement si catégorie vide
```

Le prochain lot ne change pas cette logique. Il enrichit uniquement la **card produit home** pour améliorer la lisibilité commerciale.

---

## Objectif du lot V1.1

Faire évoluer la card actuelle :

```text
image · badge · origine/famille · nom · prix · Voir
```

vers une card enrichie :

```text
image · badge ruban
nom produit / variante
étiquettes client
prix TTC
quantité nette · prix de référence
Voir le produit
```

---

## Décisions MOA à respecter

- La catégorie **« Coups de cœur »** est une catégorie de pilotage, jamais une information affichée client.
- Ne pas forcer 5 cards en mode curaté.
- Ne pas compléter avec des produits hors catégorie.
- Ne pas réintroduire un badge forcé par position.
- Le CTA V1.1 est **« Voir le produit »**, pas `Ajouter au panier`.
- Pas de wishlist fonctionnelle en V1.1.
- Pas de refonte de `/shop`.

---

## Implémentation attendue

### 1. Étiquettes client

Ajouter une donnée BO pour afficher une ligne de type :

```text
Réunion · Épicerie
```

Recommandation spec :

- modèle `dorevia.ck.product.label` ;
- champ `product.template.ck_featured_label_ids` ;
- affichage `sequence asc, name asc` ;
- masquer si vide ;
- exclure systématiquement « Coups de cœur ».

### 2. Quantité nette

Ajouter sur `product.template` :

| Champ | Nom technique proposé |
|-------|-----------------------|
| Quantité nette commerciale | `ck_net_quantity` |
| Unité quantité nette | `ck_net_quantity_uom` |
| Unité prix de référence | `ck_reference_price_uom` |
| Afficher le prix de référence | `ck_show_reference_price` |

Unités minimales :

```text
g, kg, ml, cl, l, pièce
```

### 3. Prix de référence

Afficher :

```text
320 g · 18,13 €/kg
```

si le calcul est possible.

Sinon :

```text
320 g
```

Si quantité vide : masquer la ligne.

### 4. CTA

Remplacer le libellé :

```text
Voir
```

par :

```text
Voir le produit
```

Le lien doit rester la fiche produit / variante.

---

## Fichiers à modifier

| Fichier | Action |
|---------|--------|
| `dorevia_ck_marketone_content/home_featured.py` | Helpers labels, quantité, prix référence, HTML card. |
| `dorevia_ck_marketone_content/models/product_template.py` | Champs custom + refresh fields. |
| `dorevia_ck_marketone_content/views/product_template_views.xml` | Champs dans l'onglet eCommerce. |
| `dorevia_ck_marketone_content/security/ir.model.access.csv` | Accès modèle labels si modèle custom. |
| `dorevia_ck_theme/static/src/scss/website.scss` | Styles card V1.1. |
| `dorevia_ck_marketone_content/tests/test_ck_home_section3_curation.py` | Tests nouveaux critères. |

Prévoir une migration `19.0.1.19.0` ou version suivante selon la séquence module.

---

## Critères d'acceptation minimum

| # | Critère |
|---|---------|
| A1 | Produit avec labels `Réunion`, `Épicerie` → affiche `Réunion · Épicerie`. |
| A2 | « Coups de cœur » n'apparaît jamais dans la ligne labels. |
| A3 | Quantité `320`, unité `g` → affiche `320 g`. |
| A4 | Prix `5,80 €`, `320 g`, référence `kg` → affiche `320 g · 18,13 €/kg`. |
| A5 | Sans quantité → ligne quantité absente. |
| A6 | Ruban renseigné → badge ; sans ruban → pas de badge. |
| A7 | CTA = `Voir le produit`. |
| A8 | Section 3 conserve la curation BO, le nombre variable et le plafond 8. |
| A9 | Mobile 390 : pas de chevauchement, CTA lisible. |
| A10 | `/shop` inchangé. |

---

## Commande de validation attendue

```bash
docker exec sandbox-odoo19-odoo-1 bash -c \
  'odoo -d dorevia_ck_marketone_01 --http-port=8079 --no-http \
   -u dorevia_ck_theme,dorevia_ck_marketone_content \
   --test-tags dorevia_ck_marketone_home_section3_curation,dorevia_ck_marketone_home_section3 \
   --stop-after-init'
```

Attendu :

```text
0 failed, 0 error(s)
```

---

## Point d'attention

Le HTML de la section est pré-rendu dans l'arch de la home. Tout nouveau champ affiché dans la card doit être ajouté aux champs déclenchant le refresh dans `models/product_template.py`.

