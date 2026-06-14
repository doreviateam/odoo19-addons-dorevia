# Recette QA — Maquette CK V1.2.x · Vision complète

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Statut** | **Recette QA Lot 1.1 + Lot 2 + Lot 3+ exécutée — 2026-06-13** |
| **Décision MOA** | [`decision_moa_pause_odoo_iteration_maquette_v1_2_x.md`](./decision_moa_pause_odoo_iteration_maquette_v1_2_x.md) · [`decision_moa_verdict_maquette_v1_2_x_vision_complete.md`](./decision_moa_verdict_maquette_v1_2_x_vision_complete.md) |
| **Arbitrage V1 Odoo** | [`ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md`](./ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md) |
| **Cadrage** | [`CADRAGE_MAQUETTE_CK_V1_2_X.md`](./CADRAGE_MAQUETTE_CK_V1_2_X.md) |
| **Base** | [`brief_01_2.md`](./brief_01_2.md) · [`artifact/index.html`](./artifact/index.html) |
| **Périmètre** | Maquette HTML multi-pages · desktop + mobile 390 px |
| **Date création** | 2026-06-13 |
| **Livraisons recettées** | [`LIVRAISON_V1_2_X_LOT1.md`](./LIVRAISON_V1_2_X_LOT1.md) · [`LIVRAISON_V1_2_X_LOT2.md`](./LIVRAISON_V1_2_X_LOT2.md) · [`LIVRAISON_V1_2_X_LOT3.md`](./LIVRAISON_V1_2_X_LOT3.md) |
| **Verdict QA courant** | **OK MAQUETTE CK V1.2.x LOT 1 + LOT 2 + LOT 3+ — vision complète matérialisée** |

```text
QA V1.2.x = vérifier que la maquette exprime la vision CK complète
avant toute reprise Odoo.
```

---

## 1. Objet

Cette recette contrôle la maquette comme **référence cible** :

* commerciale ;
* éditoriale ;
* visuelle ;
* UX ;
* B2C / B2B ;
* producteurs / distributeurs ;
* logistique ;
* expérience d’achat.

La recette ne déclenche pas la reprise Odoo. Elle sert à classer les concepts matérialisés avant arbitrage de traduction.

---

## 2. Statuts QA

| Statut | Sens |
|--------|------|
| OK | Critère satisfait |
| KO | Critère non satisfait · correction requise |
| RÉSERVE | Acceptable en maquette mais à arbitrer |
| N/A | Non applicable à la page ou au concept |

Classes d’arbitrage post-recette :

```text
V1 prioritaire
V1 possible
V1 différée
Réserve
Hors scope
Abandonné
```

---

## 3. Pages à contrôler

| # | Page | Attendu | Statut | Commentaire QA |
|---|------|---------|--------|----------------|
| 1 | Accueil | Boutique élégante · promesse · produits · réassurance · B2B signal | OK | Page convaincante : promesse claire, réassurance haute, 6 produits avec prix/origine, coffret, entrée Pro, éditorial. Mobile 390 px sans overflow. |
| 2 | Boutique / Shop | Catalogue lisible · filtres ou entrées utiles · densité marchande | OK | Lot 2 recetté : 12 produits, prix, origines, collections, filtres visuels, réassurance, signal Pro. |
| 3 | Catégorie / collection type | Entrée commerciale claire · origine ou usage lisible | OK | Lot 2 recetté : catégorie Épicerie créole, guide “Comment choisir ?”, 7 produits, lien fiche type. |
| 4 | Fiche produit type | Origine · usage · saveur · conservation · association · signal B2B si pertinent | OK | Concept très bon et commercialement fort. Image principale corrigée en Lot 1.1 ; tags d’arbitrage masqués en CSS. |
| 5 | Professionnels | Producteurs + distributeurs · qualification · pas portail B2B custom | OK | Double cible très lisible, process qualification clair, promesse B2B maîtrisée, formulaire mock CRM cohérent. Mobile 390 px OK. |
| 6 | À propos / démarche CK | Mission · sélection · producteurs · pont territoires créoles / Europe | OK | Lot 3+ recetté : mission, sélection, relation producteurs/fournisseurs, logistique et confiance sont lisibles. |
| 6b | Fiche producteur type | Producteur · origine · savoir-faire · produits · usage · logistique CK | OK | Lot 3+ recetté : Atelier Les Hauts Goyaviers, chaîne producteur → produits → usage → achat, sans portail ni annuaire partenaires. |
| 7 | Recettes / savoirs / éditorial | Usages · recettes · conseils · transmission | OK | Lot 3+ recetté : page éditoriale simple, utile et non communautaire. Blog, forum et portail restent hors périmètre V1. |
| 8 | Contact / demande pro | Parcours clair · route plausible · formulaire ou CTA cohérent | OK | Lot 3+ recetté : contact général, demande produit, partenariat et renvoi Pro sont clairs. Formulaire mock assumé maquette. |

---

## 4. Concepts à contrôler

| # | Concept | Attendu QA | Statut | Classe | Commentaire |
|---|---------|------------|--------|--------|-------------|
| 1 | Promesse CK | Adresse européenne pour découvrir, acheter et comprendre les produits créoles | OK | V1 prioritaire | La promesse est lisible dès l’accueil et renforcée par la fiche. |
| 2 | Double cible B2C / B2B | Le site ne semble ni uniquement B2C ni uniquement Pro | OK | V1 prioritaire | Bon équilibre : achat B2C + qualification Pro sans portail B2B. |
| 3 | Producteurs / fournisseurs | Sélection · respect · pont territoires créoles / clients européens | OK | V1 possible | Bien matérialisé par la fiche produit et la fiche producteur type ; traduction Odoo à arbitrer entre page CMS et fournisseur Odoo natif. |
| 4 | Distributeurs / brick & mortar | Persona boutiques physiques / CHR / revendeurs lisible | OK | V1 prioritaire | Page Pro claire pour boutiques, CHR, revendeurs et distributeurs. |
| 5 | Logistique | Disponibilité · emballage · livraison · délais · conditions pro visibles | OK | V1 prioritaire | Logistique visible sur accueil, fiche et Pro ; promesses à confirmer opérationnellement. |
| 6 | Origines | Origines comme aide à la découverte, pas décor | OK | V1 prioritaire | Origines visibles dans les cartes et la fiche produit. |
| 7 | Collections commerciales | Incontournables · manioc · sucré · salé · packs · nouveautés · coups de cœur | OK | V1 prioritaire + possible | Lot 2 matérialise shop et catégorie ; filtres interactifs avancés restent différés. |
| 8 | Fiche produit enrichie | Au-delà nom / prix / panier | OK | V1 prioritaire + possible | Très bonne base : usage, saveur, producteur, conservation, B2B, recette, associations. |
| 9 | Éditorial / savoirs / recettes | Boutique chaleureuse, pas froide | OK | V1 possible | Lot 3+ matérialise une page recettes/savoirs statique ; blog multi-articles, commentaires, forum et RSS restent différés/hors scope. |
| 10 | Réassurance | Promesses visibles et tenables | OK | V1 prioritaire | Réassurance claire ; validation opérationnelle livraison/service à conserver en réserve MOA. |
| 11 | UX mobile 390 px | Lisibilité · CTA · cards · formulaires · pas d’overflow | OK | V1 prioritaire | 9 pages testées en 390 px : pas d’overflow horizontal. |

---

## 5. Critères transverses

| # | Critère | Seuil | Statut | Commentaire QA |
|---|---------|-------|--------|----------------|
| 1 | Cohérence commerciale | La maquette donne envie d’acheter et de consulter les produits | OK | Accueil + fiche créent un vrai parcours d’achat. |
| 2 | Cohérence éditoriale | CK raconte plus qu’une boutique exotique générique | OK | Origine, usage, producteur et recette donnent une profondeur CK. |
| 3 | Cohérence visuelle | Direction élégante, lisible, non contemplative | OK | Direction bonne ; image fiche corrigée et tags d’arbitrage masqués en Lot 1.1. |
| 4 | Clarté CTA | Chaque page propose une action utile | OK | Accueil : boutique/pro ; fiche : panier/pro ; Pro : producteur/distributeur/formulaire. |
| 5 | Promesses tenables | Aucune promesse forte non assumable opérationnellement | RÉSERVE | Livraison France/Europe, délais 48–72h, service client et sourcing à confirmer MOA/opérations. |
| 6 | Routes plausibles | Les routes peuvent être traduites dans Odoo ou sont réservées | RÉSERVE | Parcours relatif Lot 1 OK. Routes `/shop`, `/legal`, catégories et produits restent cibles Odoo à mapper. |
| 7 | Traduisibilité Odoo | Chaque bloc est mappable, simplifiable ou classé hors scope | OK PARTIEL | Tableaux complétés ; routes Odoo absolues et filtres réels restent à mapper avant traduction. |
| 8 | Mobile | Aucun overflow, confort de scroll, contenu priorisé | OK | 9 pages contrôlées en 390 px : `scrollWidth = 390`, fiche producteur incluse. |

---

## 6. Verdicts possibles

```text
OK MAQUETTE CK V1.2.x — VISION MATÉRIALISÉE
```

```text
OK PARTIEL MAQUETTE CK V1.2.x — concepts visibles, réserves à arbitrer
```

```text
KO MAQUETTE CK V1.2.x — vision insuffisamment matérialisée
```

---

## 7. Contrôle correctif Lot 1.1

| Point contrôlé | Résultat QA |
|----------------|-------------|
| Fiche produit — image principale | OK — image chargée (`naturalWidth > 0`) desktop et mobile |
| Visuels Unsplash artifact | OK — 10/10 URLs contrôlées en HTTP 200 |
| Tags `.arbitrage-tag` | OK — HTML conservé, aucun tag visible au rendu |
| Mobile 390 px | OK — accueil, fiche et Pro sans overflow horizontal (`scrollWidth = 390`) |
| Desktop 1280 px | OK — accueil, fiche et Pro sans overflow horizontal |

Verdict correctif :

```text
Lot 1.1 = réserves bloquantes levées.
```

---

## 8. Sortie attendue

| Élément | Résultat |
|---------|----------|
| Pages validées | Accueil OK · Shop OK · Catégorie OK · Fiche produit OK · Professionnels OK · À propos OK · Fiche producteur OK · Recettes OK · Contact OK |
| Concepts V1 prioritaires | Home marchande · shop · catégorie · réassurance · produits prix/origine · achat fiche · signal Pro · page Pro + formulaire CRM · contact simple · grille produits producteur |
| Concepts V1 possibles | Bloc producteur fiche · fiche producteur CMS · process Pro · coffret · badges produit · réassurance pro · page À propos · recettes/savoirs statiques |
| Concepts différés | Associations fiche avancées · cross-sell avancé · blog multi-articles · filtres éditoriaux · automatisations CRM · annuaire multi-producteurs |
| Réserves bloquantes | Aucune après Lot 1.1 |
| Réserves non bloquantes | Routes Odoo à mapper (`/shop`, catégories, produits, `/legal`) ; promesses logistiques à confirmer ; fiche fournisseur dédiée à arbitrer |
| Hors scope / abandonné | Portail B2B · checkout pro · catalogue parallèle · pricing pro public |
| Verdict courant | **OK MAQUETTE CK V1.2.x LOT 1 + LOT 2 + LOT 3+ — vision complète matérialisée** |

---

## 9. Contrôle Lot 2

Voir recette dédiée :

[`recette_qa_maquette_v1_2_x_lot2.md`](./recette_qa_maquette_v1_2_x_lot2.md)

Synthèse :

| Élément | Résultat |
|---------|----------|
| Pages validées | Shop OK · Catégorie Épicerie créole OK |
| Parcours | Accueil → Shop → Catégorie → Fiche produit · accès Pro OK |
| Mobile | OK — shop et catégorie sans overflow horizontal |
| Visuels | OK — URLs Lot 2 contrôlées en HTTP 200 |
| Réserve non bloquante | CTA produits en routes Odoo absolues `/shop/...` à mapper à la traduction |
| Verdict Lot 2 | **OK MAQUETTE CK V1.2.x LOT 2 — catalogue et catégorie matérialisés** |

---

## 10. Contrôle Lot 3+

Voir recette dédiée :

[`recette_qa_maquette_v1_2_x_lot3.md`](./recette_qa_maquette_v1_2_x_lot3.md)

Synthèse :

| Élément | Résultat |
|---------|----------|
| Pages validées | À propos OK · Fiche producteur OK · Recettes OK · Contact OK |
| Parcours | Fiche produit → Fiche producteur → Shop / Recettes OK ; navigation et footer raccordés aux pages existantes |
| Mobile | OK — À propos, Fiche producteur, Recettes et Contact sans overflow horizontal |
| Garde-fous | OK — pas de portail, pas de blog complexe, pas de logique communautaire, pas de workflow custom |
| Réserve non bloquante | Traduction Odoo à arbitrer après validation de la vision complète ; page CMS producteur vs fournisseur Odoo natif à trancher |
| Verdict Lot 3+ | **OK MAQUETTE CK V1.2.x LOT 3+ — confiance, producteur, éditorial et contact matérialisés** |

---

*Recette QA maquette CK V1.2.x — créée suite décision MOA pause Odoo · mise à jour Lot 3+ · 2026-06-13.*
