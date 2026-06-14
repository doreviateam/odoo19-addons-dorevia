# Recette QA — Maquette CK V1.1

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Livraison** | Maquette CK V1.1 |
| **Ticket source** | `ticket_dev_maquette_01_open_design` |
| **Suite de** | `LIVRAISON.md` V1 + recette QA V1 |
| **Référence design** | `docs/design/design_01.md` v1.1 |
| **Compte rendu livraison** | `docs/design/maquette_01/LIVRAISON_V1_1.md` |
| **Artefact local** | `/Users/doreviateam/open-design/.od/projects/ck-marketone-maquette-v1/index.html` |
| **URL testée** | `http://127.0.0.1:8765/index.html` |
| **Date de recette** | 2026-06-12 |
| **Statut QA** | Validé pour revue de traduisibilité Odoo |

---

## 1. Synthèse QA

La maquette CK V1.1 corrige les réserves principales relevées en V1 :

- le quick-add ambigu `+` est remplacé par une action texte `Voir` ;
- le texte `/shop` ne promet plus un ajout panier en un clic ;
- le burger mobile ouvre désormais un menu fonctionnel ;
- les produits liés sont responsive en mobile ;
- la note JS ne mentionne plus un faux panier ;
- les catégories sont mieux structurées et rattachées à `product.public.category` comme cible ;
- le savon vétiver est conservé après arbitrage MOA dans le périmètre `Maison & bien-être`.

Verdict QA :

```text
RECETTE QA V1.1 VALIDÉE
```

La maquette peut passer à la revue Dev de traduisibilité Odoo, puis à la grille thème / template / extension.

Important :

```text
Cette validation QA ne lève pas le verrou Odoo.
Elle valide uniquement la maquette comme base de revue et d'arbitrage technique.
```

---

## 2. Périmètre vérifié

La recette V1.1 porte sur :

- accueil ;
- page boutique `/shop` ;
- fiche produit — layout achat ;
- navigation desktop et mobile ;
- drawer mobile des filtres ;
- grille produits principale ;
- grille produits liés ;
- action carte `Voir` ;
- réassurance ;
- entrée B2B secondaire ;
- tokens et documents de livraison ;
- annotation composant → Odoo mise à jour ;
- points à arbitrer mis à jour.

Hors périmètre inchangé :

- aucune base Odoo ;
- aucun module `dorevia_ck_theme` ;
- aucun QWeb Odoo ;
- aucun SCSS Odoo ;
- aucun panier réel ;
- aucun checkout réel ;
- aucun portail B2B ;
- aucune implémentation de listes de prix professionnelles.

---

## 3. Méthode de contrôle

Documents relus :

- `docs/design/maquette_01/LIVRAISON_V1_1.md` ;
- `docs/design/maquette_01/points_a_arbitrer.md` ;
- `docs/design/maquette_01/annotation_composants_odoo.md` ;
- artefact HTML `index.html`.

Contrôles navigateur réalisés sur `http://127.0.0.1:8765/index.html` :

- ouverture de la maquette ;
- vérification des CTA cartes ;
- vérification de l'absence de `.quick-add` ;
- vérification du texte `/shop` ;
- vérification de la note JS ;
- vérification du menu burger mobile ;
- vérification du drawer filtres mobile ;
- vérification de la grille boutique mobile ;
- vérification de la grille produits liés mobile ;
- vérification des éléments `product.public.category` ;
- vérification du maintien du produit `Savon artisanal vétiver`.

Viewport mobile testé :

```text
390 x 844
```

---

## 4. Critères d’acceptation V1.1

| Critère | Statut QA | Commentaire |
|---------|-----------|-------------|
| Trois écrans phase 1 produits | OK | Accueil, `/shop`, fiche produit présents. |
| Cohérence avec `design_01.md` | OK | Direction marchande, claire, vivante, compatible Odoo. |
| Accueil compréhensible | OK | Promesse, catégories, produits vedettes, CTA et réassurance visibles. |
| Boutique `/shop` exploitable | OK | Produits, prix, filtres, tri, catégories et entrée pro visibles. |
| Fiche produit utile à la décision | OK | Prix, format, origine, quantité, CTA, usage et réassurance présents. |
| Prix lisibles | OK | Prix visibles sur cartes et fiche. |
| CTA cartes non ambigus | OK | Boutons `Voir` avec `aria-label="Voir le produit"`. |
| CTA achat fiche visible | OK | Bouton `Ajouter au panier` présent sur fiche produit. |
| Réassurance visible | OK | Livraison, paiement, producteurs, service client. |
| B2B visible mais secondaire | OK | Lien et bloc pro, pas de portail. |
| Burger mobile fonctionnel | OK | Drawer mobile avec Accueil, Boutique, Catégories, Professionnels. |
| Drawer filtres mobile fonctionnel | OK | Sidebar et overlay ouverts correctement. |
| Grille boutique mobile | OK | 1 colonne en viewport 390 px. |
| Produits liés mobile | OK | 1 colonne en viewport 390 px. |
| Tokens documentés | OK | Déjà couverts par la livraison V1. |
| Composants annotés vers Odoo | OK | Annotation mise à jour : `Voir` vs quick-add. |
| Points à arbitrer actualisés | OK | Arbitrages MOA intégrés, reste à trancher listé. |
| Aucun développement Odoo | OK | Verrou respecté. |

---

## 5. Vérifications ciblées des corrections

### 5.1 Quick-add

Résultat QA : OK

Constats :

- aucun élément `.quick-add` restant ;
- aucun CTA carte `+` restant ;
- les cartes utilisent `card-cta` ;
- le texte visible est `Voir` ;
- les liens pointent vers `#produit` ;
- les `aria-label` sont uniformes : `Voir le produit`.

Décision :

```text
Réserve V1 levée.
```

### 5.2 Texte `/shop`

Résultat QA : OK

Texte V1.1 vérifié :

```text
Agro-transformation créole des territoires créolophones — prix clairs, origines lisibles, accès rapide au produit puis achat depuis la fiche.
```

Le texte ne promet plus un ajout panier en un clic.

Décision :

```text
Réserve V1 levée.
```

### 5.3 Burger mobile

Résultat QA : OK

En viewport `390x844` :

- burger visible ;
- clic burger ouvre le drawer ;
- overlay visible ;
- `aria-expanded="true"` après ouverture ;
- liens présents : Accueil, Boutique, Catégories, Professionnels.

Décision :

```text
Réserve V1 levée.
```

### 5.4 Drawer filtres mobile

Résultat QA : OK

En viewport `390x844` :

- bouton filtres visible ;
- clic filtres ouvre la sidebar ;
- overlay visible ;
- `aria-expanded="true"` après ouverture ;
- sidebar affichée.

Décision :

```text
Conforme.
```

### 5.5 Produits liés responsive

Résultat QA : OK

En viewport `390x844` :

- grille produits liés = 1 colonne ;
- première carte liée = largeur utile complète ;
- la classe `.related-grid` applique bien le responsive.

Décision :

```text
Réserve V1 levée.
```

### 5.6 Note JS

Résultat QA : OK

Texte vérifié :

```text
JS filtres/quantité = démo uniquement, pas spec Odoo
```

Décision :

```text
Réserve V1 levée.
```

### 5.7 Savon vétiver

Résultat QA : OK après arbitrage MOA

Le produit est conservé et mieux catégorisé :

```text
Maison & bien-être · Savons
```

Décision :

```text
Question MOA V1 tranchée.
Plus de réserve QA sur ce point.
```

---

## 6. Résultats par écran

### 6.1 Accueil

Statut QA : OK

Points validés :

- promesse claire ;
- CTA boutique ;
- signal professionnel secondaire ;
- familles / univers visibles ;
- mention `product.public.category` pour la cible catégories ;
- produits vedettes ;
- prix visibles ;
- action `Voir` ;
- réassurance.

### 6.2 Boutique `/shop`

Statut QA : OK

Points validés :

- page boutique identifiable ;
- promesse courte corrigée ;
- filtres visibles ;
- arborescence catégories ;
- origines visibles ;
- collections visibles ;
- filtre prix visible mais toujours à trancher côté Odoo ;
- tri ;
- grille produits ;
- prix lisibles ;
- action `Voir` ;
- pagination ;
- entrée pro secondaire.

Point à surveiller pour la suite :

```text
Origines, collections et filtre prix restent à trancher avant traduction Odoo.
```

### 6.3 Fiche produit

Statut QA : OK

Points validés :

- nom produit clair ;
- origine et catégorie ;
- format / poids / stock ;
- prix lisible ;
- quantité ;
- CTA `Ajouter au panier` ;
- usage produit ;
- réassurance ;
- produits liés responsive.

---

## 7. Parcours utilisateurs

| Persona | Statut QA V1.1 | Commentaire |
|---------|----------------|-------------|
| Particulier acheteur | OK | Comprend l'offre, voit les prix, accède aux fiches, peut décider depuis la fiche. |
| Professionnel / revendeur | OK | Entrée pro visible et secondaire, sans portail complet. |
| Acheteur par origine | OK | Origines visibles dans filtres et chips. Source Odoo encore à trancher. |
| Client prudent | OK | Livraison, paiement, producteurs et service client visibles. |
| Découvreur | OK | Univers, catégories, packs et produits vedettes aident l'exploration. |
| Acheteur pressé | OK | Prix et action `Voir` clairs ; achat ensuite depuis la fiche. |

---

## 8. Points encore à trancher avant traduction Odoo

Ces points ne bloquent pas la validation QA de la maquette V1.1, mais doivent être arbitrés avant implémentation :

1. Packs `non_detailed` : doctrine 1 ligne panier confirmée pour Odoo ?
2. Origines : attribut produit ou modèle dédié ?
3. Collections : tags, catégories ou extension ?
4. Filtre prix : conserver l'UI si la traduction Odoo CE est incertaine ?
5. Entrée pro : page CMS ou formulaire `website_crm` ?

---

## 9. Décision QA

```text
Statut : RECETTE QA V1.1 VALIDÉE
```

QA valide la maquette V1.1 comme base pour :

- arbitrage final MOA sur la maquette ;
- revue Dev de traduisibilité Odoo ;
- préparation de la grille thème / template / extension.

QA ne valide pas :

- le démarrage d'une base Odoo ;
- le développement de `dorevia_ck_theme` ;
- l'écriture de QWeb ;
- l'écriture de SCSS Odoo ;
- la reprise automatique de `dorevia_ckreyol_marketone`.

---

## 10. Suite recommandée

Ordre recommandé :

```text
1. Transmettre la validation QA V1.1.
2. Lancer la revue Dev de traduisibilité Odoo.
3. Formaliser la grille thème / template / extension.
4. Arbitrer les points encore ouverts.
5. Décider explicitement si le verrou Odoo peut être levé.
```

Verrou maintenu tant que la décision explicite n'est pas prise :

```text
Pas de base Odoo.
Pas de module dorevia_ck_theme.
Pas de QWeb.
Pas de SCSS Odoo.
Pas de reprise automatique de dorevia_ckreyol_marketone.
```

---

## 11. Conclusion

La V1.1 corrige correctement les réserves QA de la V1. Le parcours est plus clair, le mobile est utilisable, l'action carte n'induit plus un panier implicite, et les arbitrages MOA principaux ont été intégrés.

Conclusion QA :

```text
Maquette V1.1 validée.
Réserves QA principales levées.
Passage possible à la revue de traduisibilité Odoo.
Verrou de développement Odoo toujours maintenu.
```
