# Doctrine C-Kreyol — Pack vs Kit

**Statut :** Intégrée au dépôt — référence métier pour le catalogue e-commerce  
**Périmètre :** C-Kreyol / eCommerce / Produits composés  
**Objet :** Clarifier la distinction métier entre **pack** et **kit** dans le catalogue de vente.

**Articulation technique :** cette doctrine **ne remplace pas** la règle de bi-lexique [ADR-CKR-008](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008) (porte Explorer **Kits** ↔ implémentation **`pack_ok`** / `product_pack`). Elle guide **libellés, copy et structuration éditoriale** ; le détail d’implémentation reste dans [SPEC_SHOP_PORTES.md](../mvp_01/SPEC_SHOP_PORTES.md) et [CONTRAT_URL_PACKS.md](../mvp_01/CONTRAT_URL_PACKS.md).

---

## 1. Principe général

Dans C-Kreyol, les notions de **pack** et de **kit** désignent toutes deux des offres pouvant être affichées comme des produits vendables en eCommerce.

La différence principale porte sur la **nature de l’assemblage** :

- le **pack** repose sur une composition **homogène** ;
- le **kit** repose forcément sur une composition **hétérogène**.

Cette distinction doit rester compréhensible côté client, exploitable côté catalogue, et cohérente avec la gestion commerciale dans Odoo.

---

## 2. Définition du pack

Un **pack** est une offre commerciale affichée comme un produit, composée d’un assemblage de produits **homogènes**.

Le pack représente un **conditionnement commercial** : il permet de vendre ou d’acheter un regroupement d’unités composantes sans faire disparaître l’existence du produit vendu ou acheté à l’unité.

### Règle métier

> Un pack regroupe des produits homogènes.  
> Il peut être vendu ou acheté en tant que pack, tout en conservant la possibilité de vendre ou d’acheter séparément les unités qui le composent.

### Exemples

| Produit unitaire | Pack correspondant |
|---|---|
| Jus goyave 33 cl | Pack de 6 jus goyave 33 cl |
| Pot de confiture goyave | Pack de 3 confitures goyave |
| Bouteille de sirop de groseille | Pack de 2 sirops de groseille |
| Sachet de biscuits coco | Pack de 6 sachets de biscuits coco |

### Logique principale

Le pack relève principalement d’une logique de :

- conditionnement ;
- volume ;
- remise commerciale ;
- achat ou vente groupée ;
- facilité de transport ou de stockage ;
- exposition commerciale d’un produit homogène.

---

## 3. Définition du kit

Un **kit** est une offre commerciale affichée comme un produit, composée forcément d’un assemblage de produits **hétérogènes**.

Le kit ne représente pas seulement un regroupement d’unités. Il représente une **composition d’usage**, une **recette**, un **moment de consommation** ou une **expérience**.

### Règle métier

> Un kit rassemble des produits de natures différentes autour d’un usage, d’une recette, d’un moment ou d’une expérience.

### Exemples

| Kit | Composition possible |
|---|---|
| Kit apéro créole | Chips, sauce, boisson, biscuits salés |
| Kit colombo | Épices, sauce, riz, accompagnement |
| Kit goûter antillais | Gâteau, confiture, boisson, douceurs |
| Kit découverte créole | Produits variés issus de plusieurs familles |

### Logique principale

Le kit relève principalement d’une logique de :

- usage ;
- recette ;
- moment de consommation ;
- découverte ;
- expérience client ;
- narration éditoriale.

---

## 4. Règle de distinction

La règle de distinction doit rester simple :

> Si les composants sont homogènes, c’est un **pack**.  
> Si les composants sont hétérogènes, c’est un **kit**.

---

## 5. Tableau de synthèse

| Critère | Pack | Kit |
|---|---|---|
| Nature de l’assemblage | Homogène | Hétérogène |
| Logique principale | Conditionnement commercial | Usage, recette, moment, expérience |
| Affichage eCommerce | Produit vendable | Produit vendable |
| Vente à l’unité des composants | Oui, possible | Oui, possible selon les composants |
| Achat à l’unité des composants | Oui, possible | Oui, possible selon les composants |
| Sens commercial | Acheter plus d’un même produit | Composer une expérience |
| Exemple type | Pack de 6 jus goyave | Kit apéro créole |

---

## 6. Conséquence pour C-Kreyol

Dans C-Kreyol, le mot **pack** doit être réservé aux offres homogènes.

Le mot **kit** doit être réservé aux compositions hétérogènes, lorsqu’il existe une intention d’usage, de recette, de moment ou d’expérience.

Cette distinction permet d’éviter la confusion entre :

- une offre de volume ;
- une composition éditorialisée ;
- une promotion ;
- une collection ;
- une simple catégorie produit.

---

## 7. Formulation courte de référence

> **Pack = conditionnement commercial homogène.**  
> **Kit = composition hétérogène d’usage ou d’expérience.**

---

## 8. Formulation longue de référence

Dans C-Kreyol, un **pack** désigne une offre commerciale affichée comme un produit, composée exclusivement de produits homogènes. Il constitue un niveau de conditionnement commercial au-dessus du produit unitaire : le client peut acheter le produit à l’unité ou sous forme de pack.

Un **kit** désigne une composition hétérogène de produits de natures différentes. Il est pensé autour d’un usage, d’une recette, d’un moment de consommation ou d’une expérience client.

Cette distinction doit guider la structuration du catalogue, les libellés utilisés en front-office, les portes d’entrée eCommerce, ainsi que les règles de présentation produit.

---

## Références croisées

- [ADR-CKR-008](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008) — porte Explorer, bi-lexique **Kits** / **Pack** technique ;
- [SPEC_SHOP_PORTES.md §4.3](../mvp_01/SPEC_SHOP_PORTES.md) — matrice porte Pack / `ckr_mode=pack` ;
- [CONTRAT_URL_PACKS.md](../mvp_01/CONTRAT_URL_PACKS.md) — URL `/kits`, filtre `pack_ok`.
