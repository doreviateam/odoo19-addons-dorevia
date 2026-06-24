# Maquette et intégration Odoo V1.2.x

> **Dossier opérationnel principal.** Il contient la maquette validée, les décisions MOA, la traduction Odoo, les recettes et leurs preuves.

## Commencer ici

| Question | Document faisant foi |
|---|---|
| Quelle cible UX doit-on suivre ? | [Cadrage V1.2.x](./CADRAGE_MAQUETTE_CK_V1_2_X.md) |
| La maquette est-elle validée ? | [Verdict MOA vision complète](./decision_moa_verdict_maquette_v1_2_x_vision_complete.md) |
| Quel périmètre est traduisible en V1 ? | [Arbitrage V1](./ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md) |
| Qu’est-ce que la MOA a autorisé ? | [Décision GO reprise Odoo](./decision_moa_go_reprise_odoo_v1.md) |
| Dans quel ordre intégrer ? | [Séquence active](./SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md) |
| Comment traduire un bloc en Odoo ? | [Guide maquette → Odoo](./GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md) |
| Où voir la maquette HTML ? | [Prototype `artifact/`](./artifact/index.html) |

## Cycle de la maquette

| Étape | Documents |
|---|---|
| Brief | [Brief V1.2](./brief_01_2.md) · [Brief V1.2.1](./brief_maquette_ck_v1_2_1.md) |
| Cadrage cible | [Cadrage V1.2.x](./CADRAGE_MAQUETTE_CK_V1_2_X.md) |
| Livraisons | [Lot 1](./LIVRAISON_V1_2_X_LOT1.md) · [Lot 2](./LIVRAISON_V1_2_X_LOT2.md) · [Lot 3](./LIVRAISON_V1_2_X_LOT3.md) |
| Recette maquette | [Vision complète](./recette_qa_maquette_v1_2_x.md) · [Lot 2](./recette_qa_maquette_v1_2_x_lot2.md) · [Lot 3](./recette_qa_maquette_v1_2_x_lot3.md) |
| Décision finale | [Verdict MOA](./decision_moa_verdict_maquette_v1_2_x_vision_complete.md) |

## Intégration Odoo par phase

| Phase | Périmètre | Recette |
|---:|---|---|
| 1 | Header et footer | [Recette Phase 1](./RECETTE_QA_PHASE1_HEADER_FOOTER_CK_V1.md) |
| 2 | Home sobre | [Recette Phase 2](./RECETTE_QA_PHASE2_HOME_SOBER_CK_V1.md) |
| 3 | Boutique | [Recette Phase 3](./RECETTE_QA_PHASE3_SHOP_CK_V1.md) |
| 4 | Fiche produit | [Recette Phase 4](./RECETTE_QA_PHASE4_FICHE_PRODUIT_CK_V1.md) |
| 5 | Professionnels et CRM | [Recette Phase 5](./RECETTE_QA_PHASE5_PRO_CRM_CK_V1.md) |
| 6 | Contact et À propos | [Recette Phase 6](./RECETTE_QA_PHASE6_CONTACT_A_PROPOS_CK_V1.md) |
| 7 | Fiche producteur | [Recette Phase 7](./RECETTE_QA_PHASE7_FICHE_PRODUCTEUR_CK_V1.md) |
| 8 | Recettes statiques | [Recette Phase 8](./RECETTE_QA_PHASE8_RECETTES_STATIQUES_CK_V1.md) |
| 9 | Newsletter | [Recette Phase 9](./RECETTE_QA_PHASE9_NEWSLETTER_CK_V1.md) |
| 10 | Recette globale go-live | [Recette Phase 10](./RECETTE_QA_PHASE10_GO_LIVE_CK_V1.md) · [Rapport transversal](./RAPPORT_PHASE10_TRANSVERSALE_20260614.md) |

## Références maintenues après le socle V1.2.x

| Sujet | Architecture / décision | QA / synthèse |
|---|---|---|
| Produits vedettes / Coups de cœur | [Architecture Section 3](./NOTE_ARCHITECTURE_SECTION3_VEDETTES_V1.md) | [Recette visuelle V1.1](./RECETTE_VISUELLE_SECTION3_V1_1.md) · [Synthèse durcissement](./SYNTHESE_CAMPAGNE_DURCISSEMENT_SECTION3_PR1_PR4_V1.md) |
| Acheter par univers | [Architecture Section 4](./NOTE_ARCHITECTURE_SECTION4_UNIVERS_V1.md) | [Recette visuelle Section 4](./RECETTE_VISUELLE_SECTION4_UNIVERS_V1.md) |
| Carte produit | [Spécification](./SPEC_DEV_CARD_PRODUIT_COUPS_DE_COEUR_V1_1.md) | [Acte MOA](./ACTE_MOA_GO_CARD_PRODUIT_CK_HOME_BOUTIQUE_V1.md) |
| Curation BO | [Spécification](./SPEC_SECTION3_VEDETTES_CURATION_BO_V1.md) | [Onboarding QA](./ONBOARDING_QA_SECTION3_PR73_V1.md) |
| Traduction Odoo | [Guide](./GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md) | [Recette du dictionnaire](./RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md) |

## Annexes : où regarder, où ne pas commencer

- `artifact/` : prototype HTML/CSS de comparaison ; ce n’est pas le code Odoo livré.
- `captures/` : preuves visuelles classées par campagne ; partir du document de recette qui les cite.
- `scripts/` : scripts de recette et de génération ; partir du fichier `RECETTE_QA_…` correspondant.
- `rapport/` : restitutions HTML/PDF destinées au partage.
- `references/` : visuels de référence ponctuels.

## Documents historiques dans ce dossier

[La séquence pré-pause](./go_reprise_odoo_v1_2.md) est explicitement historique. Lorsqu’un document indique qu’il est remplacé ou pré-pause, suivre son renvoi vers la séquence ou la décision active ci-dessus.
