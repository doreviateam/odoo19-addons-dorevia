Tu travailles sur `dorevia_ckreyol_marketplace` sous Odoo 19 CE.

Réponds en français.

Doctrine :
- ADR-001 standard Odoo d’abord
- ADR-002 spécifique surtout front
- ADR-007 convergence des portes vers `/shop` ou chemin natif équivalent
- ADR-008 distinction Kits front vs Pack BO

Références à lire :
`README.md`, `docs/crea/PLATEFORME_MARQUE_CK_V1.md` (marque, promesse, ton, gel 2026-04-23), `docs/crea/CADRAGE_DESIGN_CREATION_CK_V1.md` (design, composition, gel 2026-04-23), `docs/direction/ARCHITECTURE_DECISION_RECORD.md`, `docs/direction/WIREFRAME_HOMEPAGE.md` (Bloc 3), `docs/mvp_01/SPEC_SHOP_PORTES.md`, `docs/prompting/prompt_dev.md`

Si le ticket concerne la homepage :
`docs/crea/PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md` — V1 implémentée le 2026-04-23, arbitrages §9 gelés ; ne pas les rouvrir sans ticket explicite.  
Évolution **appétence / partition** (cadrage vs impl.) : `docs/crea/TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md` (P2 ouvert ; voir aussi `docs/crea/TICKETS_HORS_PERIMETRE_V1.md` ticket 5).  
**Hero structurel V2 (immersif)** : `docs/mvp_02/DECISION_HERO_HOMEPAGE_V2.md`, `docs/crea/TICKET_HERO_HOMEPAGE_V2.md`, `docs/mvp_02/1_HOMEPAGE.md`, `docs/direction/SPEC_HERO_HOMEPAGE.md` §8.  
**Explorer grille MVP2** : `docs/mvp_02/DECISION_EXPLORER_HOMEPAGE_MVP2.md`, `docs/crea/TICKET_EXPLORER_HOMEPAGE_MVP2.md`, `docs/mvp_02/1_HOMEPAGE.md` §2.  
**Sélection produits MVP2.1 (`website_sale`)** : `docs/mvp_02/DECISION_PRODUITS_HOMEPAGE_MVP21.md`, `docs/crea/TICKET_SELECTION_PRODUITS_HOMEPAGE_MVP21.md`, `docs/mvp_02/1_HOMEPAGE.md` §3.  
**Ordre bas de page** (Éditorial avant Inscription) : `docs/mvp_02/DECISION_ORDRE_BLOCS_HOMEPAGE_MVP21.md`, `docs/mvp_02/1_HOMEPAGE.md` §4–6.  
**Pilotage MVP2.1** (ordre merge PR, précisions MOA, assets, recette à chaque PR) : `docs/mvp_02/README.md` section **Pilotage MVP2.1** ; **prompt de lancement** : `docs/prompting/prompt_lancement_mvp21.md`.  
**Inscription / newsletter MVP2.1** : `docs/crea/TICKET_INSCRIPTION_HOMEPAGE_MVP21.md`, `docs/crea/PV_RECETTE_INSCRIPTION_HOMEPAGE_MVP21_CK.md`, `docs/mvp_02/1_HOMEPAGE.md` §5.  
**Réassurance / confiance MVP2.1** : `docs/crea/TICKET_REASSURANCE_HOMEPAGE_MVP21.md`, `docs/crea/PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md`, `docs/mvp_02/1_HOMEPAGE.md` §6.

Contraintes :
- ne pas casser l’existant
- éviter de recréer du standard
- justifier toute dérogation
- rester maintenable

Format de réponse :
1. Compréhension
2. Analyse standard / OCA / spécifique
3. Proposition
4. Fichiers touchés
5. Changements à faire
6. Risques
7. Recette

Tâche immédiate :
[À COMPLÉTER]