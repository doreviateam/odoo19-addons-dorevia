# Livrable MOA — Header & Mega-menus C-Kréyòl V2.2

| Champ | Valeur |
| --- | --- |
| Projet | `dorevia_ck_marketone` |
| Objet | Header CK V2.2 + navigation N3 + mega-menus produit |
| Référence MOA | [`SPEC_HEADER_MEGA_MENUS_CK_V2_2.md`](SPEC_HEADER_MEGA_MENUS_CK_V2_2.md) |
| Ticket Dev | [`TICKET_DEV_HEADER_MEGA_MENUS_CK_V2_2.md`](../TICKET_DEV_HEADER_MEGA_MENUS_CK_V2_2.md) |
| Choix techniques Dev | [`DEV_HEADER_V22_CHOIX_TECHNIQUES.md`](../DEV_HEADER_V22_CHOIX_TECHNIQUES.md) |
| Statut livraison Dev | **GO technique** — prêt pour recette visuelle MOA |
| Statut recette visuelle MOA | **À réaliser** — non bloqué par le socle technique |
| Statut GO MOA final | **Non posé** — en attente recette visuelle qualitative |
| Environnement de recette | `dorevia_ck_marketone_01` · `http://localhost:18079` |
| Modules livrés | `dorevia_ck_theme` **19.0.1.41.0** · `dorevia_ck_marketone_content` **19.0.1.29.0** |

### Jalons de validation

| Jalon | Statut | Date |
| --- | --- | --- |
| Socle technique (modules, tests, comportements fonctionnels) | **GO technique** | 2026-06-23 |
| Recette QA automatisée + captures reproductibles | **Validé Dev** | 2026-06-23 |
| Recette visuelle qualitative MOA | **En cours / à planifier** | — |
| GO MOA final Header V2.2 | **En attente** | — |

---

## 1. Synthèse pour la MOA

Le **Header C-Kréyòl V2.2** a été implémenté conformément à l’architecture MOA figée. Il transforme l’en-tête du site en un **système d’orientation e-commerce** structuré en trois niveaux visibles, avec une navigation principale dense mais hiérarchisée, et des mega-menus produit pour les rayons catalogue.

**Ce que le visiteur obtient concrètement :**

- une **promesse de confiance** immédiate (bandeau N1) ;
- une **barre fonctionnelle** claire : marque, recherche, connexion, panier (N2) ;
- une **navigation marchande** organisée en rayons, sélections commerciales et entrées relationnelles (N3) ;
- des **mega-menus** riches pour Épicerie, Boissons et Maison & Bien-être, alimentés par le catalogue réel ;
- un **comportement mobile** en accordéon, sans surcharge visuelle.

**Résultat socle technique :** 41 tests automatisés verts · comportements fonctionnels documentés · captures reproductibles disponibles.

**Qualification MOA (2026-06-23) :** livraison reçue en **GO technique** pour ouverture de la **recette visuelle qualitative**. Ce document et les captures seed **ne constituent pas** une validation MOA finale ni une démonstration complète du header cible V2.2 (voir § 9 et § 17).

---

## 2. Objectif rappelé

Conformément à la spec MOA, le header doit permettre à un visiteur de comprendre en quelques secondes :

- qu’il est sur **C-Kréyòl**, une **épicerie créole** ;
- qu’il peut **chercher** et **acheter** ;
- que les produits sont **sélectionnés**, **identifiés** et **expédiés sérieusement** ;
- que l’offre est structurée par **familles**, **origines**, **producteurs** et **sélections commerciales**.

L’implémentation répond à cet objectif sans introduire de fausses profondeurs : **seul le contenu réellement publié** apparaît dans la navigation.

---

## 3. Architecture livrée — les trois niveaux du header

### 3.1 Niveau 1 — Bandeau promesses

**Contenu affiché :**

```text
Produits sélectionnés · Origines identifiées · Livraison suivie · Stocké/expédié depuis Nantes
```

**Comportement livré :**

| Situation | Comportement |
| --- | --- |
| Chargement desktop | Bandeau visible (fond terracotta CK) |
| Scroll desktop | Bandeau masqué pour libérer de la hauteur |
| Mobile | Bandeau compact visible |
| Sticky | Le bandeau n’est **pas** sticky ; seul le header fonctionnel reste fixé |

**Recette :** `serviceBarHidden: true` après scroll · capture `02_desktop_scroll.png`.

---

### 3.2 Niveau 2 — Barre fonctionnelle

**Structure livrée :**

```text
[Logo C-Kréyòl + baseline]   [Recherche large]   [Se connecter] [Panier]
```

| Élément | Livraison |
| --- | --- |
| Logo | C-Kréyòl avec baseline desktop **« épicerie créole »** |
| Recherche | Centrale, placeholder **« Rechercher un produit, une saveur, une île... »** · mécanisme standard Odoo |
| Connexion | Libellé **« Se connecter »** conservé |
| Panier | Icône + libellé textuel **« Panier »** (évite l’ambiguïté d’une icône seule) |
| Sticky | `header#top` reste **sticky** au scroll ; logo lisible, pas de réduction en « C-K » |

**Recette :** baseline, placeholder et sticky validés dans `recette_header_v22_results.json`.

---

### 3.3 Niveau 3 — Navigation principale

**Navigation cible MOA (9 entrées) :**

```text
Tous nos produits · Épicerie · Boissons · Maison & Bien-être · Artisanat
· Coups de cœur · Coffrets · Nos producteurs · Espace pro
```

**Hiérarchie visuelle livrée** — trois groupes perceptibles sur une seule ligne desktop :

| Groupe | Entrées | Traitement visuel |
| --- | --- | --- |
| **Rayons catalogue** | Tous nos produits · Épicerie · Boissons · Maison & Bien-être · Artisanat | Entrées rayons · mega-menus produit si éligible |
| **Sélections commerciales** | Coups de cœur · Coffrets | Séparateur de groupe · liens légers |
| **Confiance / Relation** | Nos producteurs · Espace pro | Producteurs en graisse renforcée · Espace pro en pill sobre |

Les anciennes entrées **« Découvrir »** et **« Nos univers »** (héritage Nav-Shop V2.1) ont été retirées de la racine N3 au profit de l’architecture V2.2.

**Sur l’instance seed actuelle**, 8 entrées sont visibles : **Coffrets** est absent (voir § 9 — comportement seed, non écart fonctionnel).

---

## 4. Règle d’intensité des menus — ce qui a été implémenté

La spec MOA distingue les entrées selon leur rôle. L’implémentation respecte cette doctrine :

| Entrée | Comportement MOA | Comportement livré (seed) |
| --- | --- | --- |
| Tous nos produits | Lien direct catalogue | Lien `/shop` |
| Épicerie | Mega-menu 4 colonnes | Mega-menu (contenu partiel sur seed) |
| Boissons | Mega-menu 4 colonnes | Mega-menu (familles + origines) |
| Maison & Bien-être | Mega-menu 4 colonnes | Mega-menu (familles + origines) |
| Artisanat | Mega si ≥ 3 familles | **Lien direct** (< 3 familles sur seed) |
| Coups de cœur | Lien direct uniquement | Lien direct vers catégorie/tag |
| Coffrets | Lien direct ou mini-dropdown si ≥ 3 angles | **Absent** (aucun tag coffret publié) |
| Nos producteurs | Lien direct `/nos-producteurs` | Lien direct validé |
| Espace pro | Dropdown simple | Dropdown 4 ancres `/professionnels#…` |

---

## 5. Mega-menus produit — grammaire commune

### 5.1 Structure des 4 colonnes

Tous les mega-menus rayons catalogue suivent la grammaire MOA :

```text
Colonne 1 — Acheter par famille
Colonne 2 — Sélections CK
Colonne 3 — Origines & producteurs (ou artisans pour Artisanat)
Colonne 4 — Mise en avant visuelle (desktop uniquement)
```

**Règles respectées :**

- pas de prix dans les mega-menus ;
- pas de recherche interne ;
- libellés front accentués autorisés ;
- **colonnes vides masquées** — aucune famille sans produit publié n’est exposée ;
- **mobile** : accordéon par section, **sans bloc visuel** colonne 4.

### 5.2 Alimentation des colonnes

Le contenu des mega-menus est **généré automatiquement** à partir du catalogue Odoo, puis synchronisé dans les menus du site :

| Colonne | Source de données |
| --- | --- |
| Acheter par famille | Sous-catégories `product.public.category` avec au moins un produit publié |
| Sélections CK | Tags produit (`/shop?tags={id}`) ou recherche fournisseur (ex. La Platine) |
| Origines & producteurs | Attribut produit « Origines » (`/shop?attrib={attr}-{value}`) + lien `/nos-producteurs` |
| Mise en avant visuelle | Bloc éditable en back-office (voir § 7) |

Les familles, tags et origines sont **figés dans la configuration MOA** (`nav_v22_config.py`) ; seules les entrées ayant du contenu publié apparaissent.

### 5.3 Rayons livrés — détail MOA

#### Épicerie (FIGÉ MOA)

Familles cibles : Biscuits & crackers · Confitures & douceurs · Farines & manioc · Sauces & condiments · Chocolat & cacao · Café & infusions.

Sélections : Coups de cœur · Nouveautés · Coffrets découverte · Produits La Platine · Idées cadeaux.

Origines : Guadeloupe · Martinique · Dominique · Guyane · Voir les producteurs.

**Sur seed :** seule la section **« Origines & producteurs »** est visible (Guadeloupe, Voir les producteurs) — cohérent avec l’absence de familles épicerie éligibles.

#### Boissons (FIGÉ MOA)

Familles cibles : Jus & nectars · Sirops créoles · Boissons locales · Boissons fraîches (conditionnelle) · Apéritifs & boissons festives · Préparations à boire.

**Sur seed :** « Acheter par famille » (ex. Jus & nectars) + origines.

**Règle Boissons fraîches :** activable via paramètre `ck.nav.boissons_fraiches_enabled` selon capacité logistique.

#### Maison & Bien-être (FIGÉ MOA)

Familles cibles : Savons & soins solides · Huiles & baumes · Senteurs & bougies · Maison & décoration · Accessoires bien-être · Rituels créoles.

**Sur seed :** « Acheter par famille » (ex. Savons & soins solides) + origines.

#### Artisanat (FIGÉ MOA conditionnel)

Familles cibles : Objets décoratifs · Arts de la table · Textile & accessoires · Bijoux & créations · Papeterie & affiches · Créations artisanales.

**Règle livrée :** mega-menu complet activé uniquement si **≥ 3 familles** ont des produits publiés. Sinon : **lien direct** vers la catégorie racine Artisanat.

**Sur seed :** lien direct (< 3 familles) — capture `06_artisanat.png`.

### 5.4 Interaction desktop

Les mega-menus s’ouvrent au **survol** (`o_hoverable_dropdown`), conformément au comportement natif Odoo. Le panneau affiche la classe `.show` et reste visible sous le rayon concerné.

**Preuves :** captures `03_mega_e_picerie.png`, `04_mega_boissons.png`, `05_mega_maison_bien_e_tre.png` · JSON `open: true` pour chaque rayon.

---

## 6. Entrées transversales et relationnelles

### 6.1 Coups de cœur

- **Comportement :** lien direct uniquement (pas de mega-menu).
- **URL seed :** `/shop/category/coups-de-cœur-24` (adaptation Odoo depuis l’intention `/shop?tag=coup_de_coeur`).
- **Recette :** `directLink: true`, `noMega: true`.

### 6.2 Coffrets

- **Comportement implémenté :** lien direct par défaut ; **mini-dropdown** si ≥ 3 angles commerciaux tagués et publiés.
- **Sur seed :** entrée **absente** — aucun tag `coffret` publié (voir § 9).
- **Réserve non bloquante :** recontrôle en recette contenu complète dès alimentation des tags/angles coffrets.

### 6.3 Nos producteurs

- **Comportement :** lien direct vers `/nos-producteurs`.
- **Page CMS** seed créée et publiée (migration `19.0.1.29.0`).
- Pas de mega-menu ni dropdown en V2.2.
- **Recette :** `href: /nos-producteurs` · capture `10_nos_producteurs_nav.png`.

### 6.4 Espace pro

- **Comportement :** dropdown simple (pas de mega-menu).
- **Structure livrée :**

```text
Espace pro
├── Acheter pour mon commerce      → /professionnels#acheter
├── Demander les conditions pro    → /professionnels#conditions
├── Devenir partenaire / distributeur → /professionnels#partenaire
└── Contacter C-Kréyòl             → /professionnels#contact
```

- **Recette :** 4 ancres validées · capture `09_espace_pro_dropdown.png`.

---

## 7. Back-office — bloc visuel mega-menu (colonne 4)

Un modèle BO **`ck.mega.menu.visual.block`** permet à l’équipe contenu de gérer la mise en avant visuelle de chaque mega-menu rayon, sans intervention Dev.

| Champ | Rôle |
| --- | --- |
| Menu concerné | Épicerie · Boissons · Maison · Artisanat |
| Image | Visuel colonne 4 |
| Titre / Sous-titre | Texte éditorial |
| Lien cible + Libellé CTA | Action commerciale |
| Date début / fin | Campagnes saisonnières |
| Actif + Séquence | Priorité d’affichage |

**Règle d’affichage :** bloc actif de séquence la plus basse, dans la fenêtre de dates si renseignée ; sinon colonne 4 masquée.

---

## 8. Mobile

### 8.1 Chrome header

```text
Bandeau promesse compact
[Menu] [C-Kréyòl] [Recherche] [Panier]
```

- Drawer latéral pour la navigation N3.
- Toutes les entrées N3 accessibles dans le menu (sauf Coffrets sur seed).

### 8.2 Mega-menus mobile

- Rendu en **accordéon Bootstrap** par section (familles · sélections · origines).
- **Pas de bloc visuel** colonne 4 (`noVisualCol: true`).
- Ordre identique au desktop.

**Preuve Épicerie :** capture `08b_mobile_mega_epicerie.png` — section « Origines & producteurs » dépliée, liens Guadeloupe et Voir les producteurs visibles.

---

## 9. Comportements seed documentés (non écarts fonctionnels)

Ces points reflètent l’**état du catalogue seed**, pas un défaut d’implémentation V2.2.

### 9.1 Coffrets absent

| Élément | Détail |
| --- | --- |
| Constat seed | Aucun tag `coffret` publié avec produits éligibles |
| Règle V2.2 | Pas de fausse profondeur — entrée matérialisée seulement si contenu réel |
| Navigation cible MOA | 9 entrées incluant Coffrets — valide en **recette contenu complète** |
| Verdict | **Comportement seed attendu** |

### 9.2 Épicerie — contenu partiel (layout corrigé 19.0.1.41.0)

| Élément | Détail |
| --- | --- |
| Constat seed | Une seule colonne peuplée (« Origines & producteurs ») |
| Layout antérieur | Panneau 320 px — **bug CSS** (`dropdown-menu` cap appliqué à `.o_mega_menu`), **pas** conséquence du seed |
| Layout actuel | Panneau **1200 px** centré, slots colonnes 25 % — grammaire mega-menu lisible |
| Verdict | Contenu partiel = seed ; respiration panneau = corrigée |

### 9.3 Artisanat — lien direct

| Élément | Détail |
| --- | --- |
| Constat seed | Moins de 3 familles Artisanat alimentées |
| Comportement | Lien direct (mega non activé) |
| Verdict | Conforme à la règle conditionnelle MOA |

---

## 10. Adaptations techniques Odoo 19 CE

Les intentions MOA ont été adaptées aux mécanismes natifs Odoo, sans moteur custom :

| Intention MOA | Implémentation réelle |
| --- | --- |
| `/shop?tag=coup_de_coeur` | `/shop?tags={id}` ou catégorie dédiée |
| Filtre origine `origin-guadeloupe` | `/shop?attrib={attribute_id}-{value_id}` |
| Famille par slug | `/shop/category/{slug}` |
| Mega-menu HTML | Stocké dans `website.menu.mega_menu_content` (natif CE) |
| Espace pro | `/professionnels#{ancre}` |
| Nos producteurs | `/nos-producteurs` (page website) |

Ces adaptations garantissent la compatibilité avec le shop Odoo 19 CE et la maintenabilité long terme.

---

## 11. Découpage de la livraison (5 lots)

| Lot | Contenu livré |
| --- | --- |
| **1 — Socle header** | Bandeau N1 · baseline · placeholder recherche · panier textuel · sticky · masquage N1 au scroll |
| **2 — Socle mega-menu** | Layout 4 colonnes desktop · accordéon mobile · SCSS/JS · modèle BO bloc visuel |
| **3 — Rayons catalogue** | Sync Épicerie · Boissons · Maison & Bien-être · Artisanat conditionnel |
| **4 — Entrées transversales** | Coups de cœur · Coffrets conditionnel · Nos producteurs · Espace pro |
| **5 — Tests & recette** | 41 tests automatisés · captures · script QA reproductible · documentation |

---

## 12. Recette et preuves de livraison

### 12.1 Tests automatisés

```text
41 tests · 0 failed · 0 error
Tags : dorevia_ck_header_v22, dorevia_ck_theme_phase10, dorevia_ck_marketone_nav_sync
```

### 12.2 Verdict MOA — critères de recette

| Critère spec MOA | Résultat |
| --- | --- |
| 3 niveaux visibles au chargement desktop | OK |
| Bandeau N1 disparaît au scroll | OK |
| Barre N2 sticky et lisible | OK |
| Hiérarchie N3 perceptible (3 groupes) | OK |
| Mega-menus rayons ouverts et visibles | OK |
| Aucune famille vide exposée | OK |
| Coups de cœur = lien direct | OK |
| Coffrets = absent sur seed (comportement attendu) | OK |
| Nos producteurs = lien direct | OK |
| Espace pro = dropdown simple | OK |
| Mobile accordéon sans bloc visuel | OK |
| Pas de prix / recherche interne dans mega-menus | OK |

### 12.3 Artefacts conservés comme preuves

| Artefact | Emplacement |
| --- | --- |
| Captures desktop + mobile (01–10, 08b) | `captures/recette_header_v22/*.png` |
| Données machine JSON | `captures/recette_header_v22/recette_header_v22_results.json` |
| Note de recette QA | `captures/recette_header_v22/RECETTE_QA_HEADER_V22.md` |
| Script reproductible | `scripts/ck_h22_recette_qa.mjs` |
| Log tests | `captures/recette_header_v22/tests_ck_header_v22.log` |

**Relance des preuves :**

```bash
cd odoo19-addons-dorevia/dorevia_ck_marketone/docs/design/maquette_01.2/scripts
node ck_h22_recette_qa.mjs
```

---

## 13. Hors périmètre V2.2 — respecté

Conformément à la spec MOA, les éléments suivants n’ont **pas** été implémentés (report V2.3+) :

- recherche interne aux mega-menus ;
- prix ou stock temps réel dans les menus ;
- multi-blocs visuels rotatifs ;
- A/B testing menu ;
- personnalisation par profil ;
- switcher Boutique / Éditorial / Communauté ;
- portail B2B transactionnel (tarifs publics, compte pro, devis avancé).

---

## 14. Réserve non bloquante

**Coffrets** devra être **recontrôlé en recette contenu complète** dès que les tags et angles commerciaux coffrets seront alimentés, afin de vérifier :

- l’apparition de l’entrée N3 ;
- le comportement **lien direct** ou **mini-dropdown conditionnel** (seuil ≥ 3 angles prêts).

Cette réserve ne remet pas en cause le **GO technique** sur l’instance seed actuelle.

**Attention MOA :** Coffrets absent, Épicerie partielle et Artisanat en lien direct sur seed sont des **comportements catalogue acceptés techniquement**, mais ils **limitent la preuve visuelle** du header cible. Ils ne doivent pas être confondus avec une démonstration complète de la V2.2 lors de la recette visuelle.

---

## 15. Prochaines étapes suggérées (hors périmètre livraison Dev)

| Sujet | Action MOA / Contenu |
| --- | --- |
| Coffrets | Publier produits tagués `coffret` + angles commerciaux · relancer recette |
| Épicerie complète | Alimenter familles épicerie (catégories + produits publiés) |
| Artisanat mega | Atteindre ≥ 3 familles pour activer le mega-menu complet |
| Blocs visuels colonne 4 | Saisir campagnes dans le BO `ck.mega.menu.visual.block` |
| Boissons fraîches | Activer `ck.nav.boissons_fraiches_enabled` si logistique prête |
| Recette visuelle MOA | Grille qualitative § 17 sur instance + captures |

---

## 16. Clôture technique (non GO MOA final)

Le **Header & Mega-menus CK V2.2** est **livré techniquement** sur l’environnement seed `dorevia_ck_marketone_01`.

L’architecture MOA (3 niveaux, 9 entrées cibles, règle d’intensité des menus, grammaire 4 colonnes, comportement mobile, entrées transversales) est **implémentée et opérationnelle**. Les comportements seed documentés sont **acceptés techniquement** mais **ne suffisent pas** à qualifier visuellement le header cible.

**GO technique — ouverture recette visuelle MOA — 2026-06-23.**

---

## 17. Prochaine étape — recette visuelle qualitative MOA

La recette visuelle porte sur le **ressenti et l’équilibre** du header, pas sur la conformité fonctionnelle déjà validée par les tests.

### Grille de lecture MOA

| Axe | Questions de recette |
| --- | --- |
| Équilibre général | Le header paraît-il harmonieux et professionnel au premier regard ? |
| Hauteur perçue | N1 + N2 + N3 : la hauteur totale est-elle maîtrisée (chargement et scroll) ? |
| Hiérarchie N3 | Les 3 groupes (rayons · sélections · relation) sont-ils **réellement perceptibles** ? |
| Poids N2 | Logo, recherche et panier : proportions, lisibilité, hiérarchie visuelle ? |
| Pill Espace pro | Le traitement bouton/pill est-il sobre, distinct, sans casser la ligne N3 ? |
| Mega-menus | Lisibilité, désirabilité, densité des colonnes ; colonne 4 si alimentée ? |
| Mobile | Drawer, accordéons, hauteur utile, absence de surcharge ? |
| Effet global | Le visiteur perçoit-il une **boutique CK mature** dès l’arrivée ? |

### Supports de recette

- Instance : `http://localhost:18079` · DB `dorevia_ck_marketone_01`
- Captures de référence : `captures/recette_header_v22/*.png`
- Script reproductible : `scripts/ck_h22_recette_qa.mjs`

### Limites connues de la démonstration seed

Pour une lecture visuelle **représentative du header cible**, la MOA pourra compléter la recette avec :

- alimentation **Coffrets** (9ᵉ entrée N3) ;
- familles **Épicerie** publiées (mega-menu 4 colonnes complet) ;
- **≥ 3 familles Artisanat** (activation mega-menu) ;
- blocs visuels colonne 4 saisis en BO.

Sans ces éléments, la recette visuelle valide le **chrome et la grammaire**, mais pas l’**effet boutique complète** visé par la spec MOA.
