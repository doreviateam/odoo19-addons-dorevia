# Livraison MOA — Maquette CK V1.2.x · Vision complète

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` · C-Kreyol / CK |
| **Move** | **Move 6** — Maquette V1.2.x · clôture + arbitrage V1 |
| **Date livraison MOA** | 2026-06-13 |
| **Statut** | **Phase 2 OK partiel QA · GO Phase 3 conditionnel** |
| **Preview** | `http://127.0.0.1:8766/` (serveur statique depuis `artifact/`) |

```text
LIVRAISON MOA — MAQUETTE CK V1.2.x
PHASE 1 OK QA ACTÉ · GO EXÉCUTION PHASE 2 ACTÉ §5BIS
```

> Document **point d’entrée MOA** — synthèse de la livraison maquette, des verdicts QA et de la préparation arbitrage Odoo V1.

---

## 1. Verdicts MOA actés

| Verdict | Statut |
|---------|--------|
| **OK MAQUETTE CK V1.2.x LOT 1 + 2 + 3+** | ✅ Vision 9 pages |
| **OK arbitrage V1 traduisible** | ✅ Document recetté |
| **OK complément bloc dual Pro / newsletter** | ✅ Accueil · Contact · Pro |
| **GO reprise Odoo V1** | ⏸ Dictionnaire CE validé MOA · §5 acte explicite → Phase 1 |

Documents verdict :

* [`decision_moa_verdict_maquette_v1_2_x_vision_complete.md`](./decision_moa_verdict_maquette_v1_2_x_vision_complete.md)
* [`recette_qa_maquette_v1_2_x.md`](./recette_qa_maquette_v1_2_x.md)

---

## 2. Artifact livré — 9 pages + complément

| # | Page | Fichier | Lot |
|---|------|---------|-----|
| 1 | Accueil | [`artifact/index.html`](./artifact/index.html) | 1 |
| 2 | Shop | [`artifact/shop.html`](./artifact/shop.html) | 2 |
| 3 | Catégorie · Épicerie créole | [`artifact/categorie.html`](./artifact/categorie.html) | 2 |
| 4 | Fiche produit type | [`artifact/fiche-produit.html`](./artifact/fiche-produit.html) | 1 |
| 5 | Professionnels | [`artifact/professionnels.html`](./artifact/professionnels.html) | 1 |
| 6 | À propos | [`artifact/a-propos.html`](./artifact/a-propos.html) | 3+ |
| 7 | Fiche producteur type | [`artifact/fiche-producteur.html`](./artifact/fiche-producteur.html) | 3+ |
| 8 | Recettes & savoirs | [`artifact/recettes.html`](./artifact/recettes.html) | 3+ |
| 9 | Contact | [`artifact/contact.html`](./artifact/contact.html) | 3+ |

**Styles partagés** : [`artifact/ck-maquette.css`](./artifact/ck-maquette.css)

**Complément post-clôture** : bloc double Pro / newsletter sur Accueil · Contact · Professionnels — [`note_reference_bloc_double_pro_newsletter_ck.md`](./note_reference_bloc_double_pro_newsletter_ck.md)

---

## 3. Parcours validés QA

```text
Accueil → Shop → Catégorie → Fiche produit
Fiche produit → Fiche producteur → Shop / Recettes / Pro
Accès Pro cohérent · footer 4 colonnes · mobile 390 px OK
```

Contrôles MOA : desktop 1280 px · mobile 390 px · pas d’overflow · liens locaux · images OK.

---

## 4. Vision CK matérialisée

| Dimension | Contenu maquette |
|-----------|------------------|
| **Commerciale** | Promesse · catalogue · fiche achat · prix · origines |
| **Logistique** | Réassurance · confiance · distinction B2C/B2B |
| **Éditoriale** | À propos · recettes · usages · transmission |
| **Producteur** | Fiche type · lien produits · sélection CK |
| **B2B** | Pro · qualification CRM · pas portail |
| **Relation continue** | Bloc dual Pro / newsletter (mock · **M9 acté · newsletter si simple**) |

**Phrase de référence** : CK sélectionne, explique, rend désirable, rend accessible et fiabilise l’achat de produits créoles.

---

## 5. Livrables documentaires

| Document | Rôle |
|----------|------|
| [`CADRAGE_MAQUETTE_CK_V1_2_X.md`](./CADRAGE_MAQUETTE_CK_V1_2_X.md) | Cadrage · lots · blocs · classes |
| [`LIVRAISON_V1_2_X_LOT1.md`](./LIVRAISON_V1_2_X_LOT1.md) | Livraison Dev Lot 1 |
| [`LIVRAISON_V1_2_X_LOT2.md`](./LIVRAISON_V1_2_X_LOT2.md) | Livraison Dev Lot 2 |
| [`LIVRAISON_V1_2_X_LOT3.md`](./LIVRAISON_V1_2_X_LOT3.md) | Livraison Dev Lot 3+ |
| [`recette_qa_maquette_v1_2_x_lot2.md`](./recette_qa_maquette_v1_2_x_lot2.md) | Recette QA Lot 2 |
| [`recette_qa_maquette_v1_2_x_lot3.md`](./recette_qa_maquette_v1_2_x_lot3.md) | Recette QA Lot 3+ |
| [`ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md`](./ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md) | Arbitrage page × bloc × Odoo |
| [`RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md`](./RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md) | **Vérification CE dictionnaire Maquette ↔ Odoo** |
| [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) | Gouvernance · GO exécution §5 · Phase 1 |
| [`SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md`](./SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md) | Séquence préparation · 10 phases |
| [`rapport/RAPPORT_MOA_MAQUETTE_CK_V1_2_X_LOT1.pdf`](./rapport/RAPPORT_MOA_MAQUETTE_CK_V1_2_X_LOT1.pdf) | Rapport MOA PDF Lot 1 |

---

## 6. Arbitrage V1 — synthèse pour MOA

**Ce document ne vaut pas GO Odoo.** Il prépare les décisions.

| Classe | Exemples |
|--------|----------|
| **V1 prioritaire** | Home · shop · catégorie · fiche achat · Pro + CRM · contact · réassurance · colonne Pro bloc dual |
| **V1 possible** | Fiche producteur CMS · recettes statique · filtres visuels · **newsletter M9** |
| **V1 différée** | Annuaire · blog · cross-sell avancé · filtres AJAX |
| **Hors scope** | Portail · espace connecté · reprise intégrale prototype |

**Arbitrage clé M1** : fiche producteur = **Option A CMS pilote** recommandée (pas annuaire · pas portail).

Détail : [`ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md`](./ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md) · §11 · §12 · §15.

---

## 7. Décisions MOA actées — M1–M9 (2026-06-13)

| # | Décision |
|---|----------|
| M1 | Fiche producteur **CMS pilote** |
| M2 | Recettes **CMS statique** |
| M3 | Filtres avancés **différés** |
| M4 | Catégories home **si BO prêtes** |
| M5 | Copy réassurance **validée avant go-live** |
| M6 | **V1 complète maîtrisée** bloc par bloc |
| M7 | Traduction **bloc par bloc** |
| M8 | **GO préparation acté** · exécution §5 distinct |
| M9 | Pro **prioritaire** · newsletter **V1 possible avec réserve** · OK CE |
| **H1** | Header **Boutique · Découvrir · Producteurs · Pro** · mega Découvrir natif CE |

Détail : [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) · Séquence : [`SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md`](./SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md) · Guide : [`GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md`](./GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md)

---

## 8. Garde-fous maintenus

```text
Odoo en pause · pas de traduction automatique du prototype
Odoo 19 CE · Website Builder · snippets first · dorevia_ck_theme
Pas de portail B2B · pas d’annuaire producteurs · pas de blog complexe
Capital Odoo conservé : /professionnels · menu Pro · header
```

---

## 9. Discours MOA (livraison)

```text
La maquette CK V1.2.x est livrée et validée :
9 pages + complément Pro/newsletter.

La vision CK est matérialisée — commerciale, logistique, éditoriale, producteur.

Dictionnaire CE validé MOA · M9 OK CE avec réserve.
Phase 1 header + footer : OK QA acté MOA (2026-06-13).
Phase 2 home sobre : OK partiel QA (2026-06-13).
GO Phase 3 : conditionnel — confirmation visuelle 6 vedettes MOA requise.
Newsletter M9 : option V1 · non bloquante Phase 1.
```

---

## 10. Suite — intégration Odoo

| # | Action | Document |
|---|--------|----------|
| 1 | Valider recette QA dictionnaire CE | MOA | ✅ Validée |
| 2 | Acter §5 GO exécution Phase 1 | MOA | ✅ Acté 2026-06-13 |
| 3 | Exécuter Phase 1 — header + footer BO | Dev | ✅ Livré 2026-06-13 |
| 4 | Recette MOA/QA Phase 1 | MOA / QA | ✅ OK QA · §6.0 |
| 5 | Acter GO MOA Phase 2 | MOA | ✅ Acté §5bis · 2026-06-13 |
| 6 | Exécuter Phase 2 — Home sobre | Dev | ✅ Livré 2026-06-13 |
| 7 | Recette MOA/QA Phase 2 | MOA / QA | ✅ OK partiel · §6.0 |
| 8 | Confirmation MOA vedettes + GO Phase 3 | MOA | En attente |

---

*Livraison MOA maquette CK V1.2.x — vision complète · 2026-06-13.*
