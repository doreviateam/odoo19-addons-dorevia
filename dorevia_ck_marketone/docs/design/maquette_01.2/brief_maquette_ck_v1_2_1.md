# Brief maquette CK V1.2.1 — Enrichissement · copy · polish · traduisibilité Odoo

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Type** | Brief Dev / maquettage — **enrichissement** V1.2 |
| **Base** | Maquette V1.2 · [`artifact/index.html`](./artifact/index.html) · [`LIVRAISON_V1_2.md`](./LIVRAISON_V1_2.md) |
| **GO MOA** | [`go_moa_maquette_v1_2_1.md`](./go_moa_maquette_v1_2_1.md) |
| **Doctrine** | [`note_05.md`](../../cadrage/note_05.md) · arbitrage [`arbitrage_moa_maquette_01_2.md`](./arbitrage_moa_maquette_01_2.md) |
| **Références** | [`brief_01_2.md`](./brief_01_2.md) · [`TABLEAU_TRADUCTION_ODOO_V1_2.md`](./TABLEAU_TRADUCTION_ODOO_V1_2.md) · [`recette_qa_maquette_01_2.md`](./recette_qa_maquette_01_2.md) |
| **Date** | 2026-06-13 |
| **Statut** | **Élargi** — voir [`decision_moa_pause_odoo_iteration_maquette_v1_2_x.md`](./decision_moa_pause_odoo_iteration_maquette_v1_2_x.md) |

> **Décision MOA active** : [`decision_moa_pause_odoo_iteration_maquette_v1_2_x.md`](./decision_moa_pause_odoo_iteration_maquette_v1_2_x.md) — périmètre élargi **vision V1.2.x multi-pages**. Cadrage : [`CADRAGE_MAQUETTE_CK_V1_2_X.md`](./CADRAGE_MAQUETTE_CK_V1_2_X.md).

```text
Ce brief (home enrichie) reste valide pour l’accueil · complété par le cadrage V1.2.x
Home Odoo : EN PAUSE — matérialisation vision maquette
```

> Ne déclenche pas Odoo. Travail `/professionnels` + header Odoo **conservé**.

---

## 1. Objet

Enrichir la maquette CK V1.2 pour en faire une **référence commerciale, visuelle et éditoriale** suffisamment mature avant reprise de la traduction Odoo bloc par bloc.

V1.2 a validé la **structure boutique élégante** et la **traduisibilité structurelle**. V1.2.1 vise à **réduire l’écart de perception** entre maquette et future intégration Odoo.

---

## 2. Contexte

| Élément | Statut |
|---------|--------|
| Maquette V1.2 structure | ✅ Livrée · recettée · arbitrage MOA |
| Odoo `/professionnels` + header | ✅ Composés · [`COMPOSITION_PROFESSIONNELS_V1_2.md`](./COMPOSITION_PROFESSIONNELS_V1_2.md) · [`COMPOSITION_HEADER_V1_2.md`](./COMPOSITION_HEADER_V1_2.md) |
| Odoo home V1.2 | ⏸ **En pause** — ancienne composition partielle encore visible |
| Réserves V1.2 connues | Placeholders visuels · copy réassurance à affiner · Artisanat non prioritaire phase 1 |

---

## 3. Doctrine MOA (inchangée)

> CK doit être une boutique claire, désirable et rassurante, capable de déclencher l’achat rapidement, tout en conservant une identité soignée.

**Maquette = spec · Odoo = exécution.** V1.2.1 renforce la spec sans changer la logique de conversion ni l’ordre des blocs V1.2.

---

## 4. Périmètre IN / OUT

### IN

| Zone | Détail |
|------|--------|
| **Home HTML** | Desktop + mobile responsive (~390 px) |
| **Visuels** | Hero · cartes produits · coffret · ambiance si pertinent |
| **Copy** | Tous blocs textuels — prêts reprise snippets Odoo |
| **Polish** | Densité mobile · CTA · badges · hover léger · enchaînement blocs |
| **Documentation** | Tableau bloc → snippet → route → réserve |

### OUT

| Zone | Raison |
|------|--------|
| Composition Odoo home | Pause MOA jusqu’à verdict V1.2.1 |
| Refonte `/shop` · fiche produit | Hors scope home V1.2.x |
| Dev module · SCSS · QWeb nouveau | Réserve = ticket séparé |
| Catalogue parallèle · panier custom | Doctrine note_05 |

---

## 5. Structure — héritée V1.2 (non négociable)

Ordre des blocs **identique V1.2** :

1. Header marchand  
2. Hero court  
3. Réassurance (4 preuves)  
4. Produits mis en avant (6 cartes · prix · CTA Voir)  
5. Catégories actionnables  
6. Coffret / découverte  
7. Espace professionnel  
8. Éditorial bas  
9. Footer CK  

Mobile : preuves + produits **avant** éditorial long (cf. note_05 §4).

---

## 6. Priorité 1 — Visuels réels ou quasi-réels

### Objectif

Remplacer les placeholders les plus faibles pour que la maquette **ressemble à une boutique**, pas à un wireframe.

### Zones cibles

| Zone | État V1.2 | Attendu V1.2.1 |
|------|-----------|----------------|
| **Hero** | Zone grise « Sélection produits CK » | Visuel produits créoles · agro · épicerie · ambiance chaleureuse · **pas** stock corporate générique |
| **Cartes produit (×6)** | Fond `--ck-image-zone` + forme neutre | Photo ou visuel quasi-réaliste par produit (goyavier · crackers · galettes · colombo · savon · etc.) |
| **Coffret découverte** | Carré placeholder | Visuel pack / coffret cohérent CK |
| **Ambiance** (optionnel) | — | Texture légère · props créoles si utile — sans surcharger |

### Sources visuelles

| Source | Usage |
|--------|-------|
| Catalogue recette / assets projet | Prioritaire si disponibles |
| Visuels libres de droits cohérents CK | Acceptable · documenter source |
| Placeholder amélioré (couleur · composition) | Acceptable **temporairement** si marqué réserve livraison |

### Contraintes Odoo

Les visuels doivent correspondre à ce qui sera **reproductible** via :

* images produit Odoo (`/web/image/product.template/…`) ;
* image hero éditoriale Website Builder ;
* ou réserve documentée si effet non natif.

---

## 7. Priorité 2 — Copy MOA complet

### Objectif

Tous les textes de la home doivent être **prêts à coller** dans les snippets Odoo — sans lorem · sans placeholder éditorial.

### Blocs et angles copy

| Bloc | Contenu à renforcer |
|------|---------------------|
| **Hero** | Promesse CK · livraison France/Europe · CTA boutique + Pro · ton marchand sobre |
| **Réassurance (×4)** | Livraison · paiement sécurisé · producteurs sélectionnés · service client — **formulations tenables** (arbitrage MOA §2.1) |
| **Produits** | Noms crédibles · micro-copy origine / catégorie · badges (coup de cœur · nouveau) |
| **Catégories** | Intention d’achat par univers · pas de texte décoratif |
| **Coffret** | Usage cadeau / première commande · prix assumé |
| **Pro home** | Double cible : producteurs/transformateurs · distributeurs/CHR · qualification (pas portail B2B) |
| **Éditorial** | Mission CK · origine · sélection · expérience d’achat B2C · renvoi Pro qualifié |
| **Footer** | Boutique · univers · Pro · contact · légal — sans placeholder Odoo |

### Thèmes copy transverses MOA

* **B2C** : prix visibles · achat simple · confiance · provenance compréhensible  
* **B2B signal** : double cible · qualification · conditions Pro back-office (pas prix B2B publics)  
* **Logistique** : France / Europe — formulation ajustable si promesse opérationnelle diffère  
* **Origine / sélection** : territoires créolophones · agro-transformé · producteurs sélectionnés  
* **Artisanat** : **non prioritaire phase 1** — ne pas créer un univers Artisanat dominant (arbitrage §2.5)

### Livrable copy

Fichier distinct ou section dans `LIVRAISON_V1_2_1.md` : **liste des textes finaux par bloc** (copier-coller snippets).

---

## 8. Priorité 3 — Polish mobile + traduisibilité Odoo

### Polish mobile (~390 px)

| Critère | Attendu |
|---------|---------|
| Overflow horizontal | **Aucun** |
| Densité | Lisible · pas de murs de texte avant produits |
| Enchaînement | Hero → preuves → produits visible au 1er scroll |
| CTA | Taille touch-friendly · contrastes OK |
| Badges | Lisibles sur cartes produit mobile |
| Burger / nav | Cohérent maquette (Boutique · Catégories · Pro) |
| Hover desktop | Léger si pertinent · **documenter** si non reproductible Odoo natif |

### Traduisibilité — tableau obligatoire

Compléter [`TABLEAU_TRADUCTION_ODOO_V1_2_1.md`](./TABLEAU_TRADUCTION_ODOO_V1_2_1.md) — **une ligne par bloc** :

| Colonne | Contenu |
|---------|---------|
| Bloc maquette | Nom section V1.2.1 |
| Contenu / copy clé | Résumé ou renvoi copy |
| Snippet CK / Odoo | ex. `s_ck_hero`, Dynamic Products… |
| Alternative native | Fallback Builder |
| Route / données BO | `/shop`, catégories, produits publiés… |
| Visuel V1.2.1 | Source · type (photo produit / hero éditorial…) |
| Statut traduction | ✅ natif · ⚠️ réserve · ❌ hors scope |
| Réserve éventuelle | Effet non natif · ticket Dev futur · workaround CMS |

### Garde-fou

```text
Réserve documentée ≠ obligation Dev immédiate
Effet impossible en snippet natif → simplifier en maquette OU marquer réserve MOA
```

---

## 9. Critères d’acceptation V1.2.1

| # | Critère | Seuil |
|---|---------|-------|
| 1 | Structure V1.2 conservée | Ordre blocs identique |
| 2 | Visuels hero + produits + coffret | Quasi-réels ou réserve MOA explicite |
| 3 | Copy complet | Aucun lorem · aucun placeholder éditorial |
| 4 | Réassurance | 4 preuves · copy tenable MOA |
| 5 | Mobile 390 px | Pas d’overflow · ordre note_05 |
| 6 | CTA produits | Voir / Découvrir uniquement |
| 7 | Tableau traduction V1.2.1 | Complété · distinct de LIVRAISON |
| 8 | Traduisibilité | Chaque bloc mappable ou réservé |
| 9 | Parité desktop / mobile | Contenu équivalent · hiérarchie respectée |

Verdict cible :

```text
OK MAQUETTE CK V1.2.1 — PRÊTE TRADUCTION ODOO
```

---

## 10. Livrables Dev

| # | Livrable | Emplacement |
|---|----------|-------------|
| 1 | Artifact HTML V1.2.1 | [`artifact/index.html`](./artifact/index.html) · Open Design |
| 2 | Note livraison | `LIVRAISON_V1_2_1.md` |
| 3 | Tableau traduction | [`TABLEAU_TRADUCTION_ODOO_V1_2_1.md`](./TABLEAU_TRADUCTION_ODOO_V1_2_1.md) |
| 4 | Recette QA | `recette_qa_maquette_v1_2_1.md` |
| 5 | Copy final (option intégré LIVRAISON) | Textes par bloc |

---

## 11. Séquence

```text
1. ✅ Décision MOA — go_moa_maquette_v1_2_1.md
2. ☐ Validation brief — ce document
3. ☐ Production artifact HTML V1.2.1
4. ☐ Recette QA — recette_qa_maquette_v1_2_1.md
5. ☐ Verdict MOA — prête traduction ?
6. ☐ Reprise Odoo home — Hero → … (go_reprise_odoo_v1_2.md)
```

---

## 12. Principe de travail

> Nous ne perdons jamais : nous apprenons, nous capitalisons, puis nous améliorons.

V1.2.1 est une **itération courte** : meilleur rendu · copy plus clair · moins d’écart maquette ↔ Odoo — **sans** repartir de zéro.

---

*Brief maquette CK V1.2.1 — enrichissement avant traduction Odoo · 2026-06-13.*
