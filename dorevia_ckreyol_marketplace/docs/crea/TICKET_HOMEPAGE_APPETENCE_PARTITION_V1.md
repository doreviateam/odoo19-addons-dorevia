# TICKET — Homepage : appétence perçue & partition (alignement cadrage design)

**ID** : `HOMEPAGE-APPETENCE-PARTITION-V1`  
**Date d’ouverture** : 2026-04-23  
**Priorité** : **P2** (impact UX visible, arbitrages produit / édito / structure de page ; ne pas confondre avec un simple patch copy).  
**Statut** : **Ouvert**  
**Module** : `dorevia_ckreyol_marketplace`  
**Périmètre** : **page d’accueil uniquement** (`website.homepage` / template `ckr_page_homepage` et snippets `ckr_*` associés).

---

## 0. Prêt pour dev — Phase A (checklist MOA / pilotage)

Avant d’ouvrir la **PR dev** pour la **Phase A** uniquement ([BRIEF_CRÉA_PHASE_A_HOMEPAGE.md](BRIEF_CRÉA_PHASE_A_HOMEPAGE.md)), cocher ou tracer une décision écrite pour chaque point :

1. [ ] **GO MOA Phase A** — médias + copy hors gel SPEC hero + SCSS ; **pas** de réordonnancement ni nouveaux snippets sans repasser en Phase B/C.
2. [ ] **Hero copy** — inchangé conforme [SPEC_HERO_HOMEPAGE.md](../SPEC_HERO_HOMEPAGE.md) §7 **ou** amendement SPEC versionné **avant** merge (pas de retouche hero « discrète » hors gel).
3. [ ] **Visuel hero** — brief / livrables alignés [BRIEF_VISUEL_HERO_PHASE1.md](../BRIEF_VISUEL_HERO_PHASE1.md) ; fichiers ou **échéance + responsable** (studio / BO) pour ne pas bloquer l’intégration.
4. [ ] **Copy hors hero** — textes **validés MOA** (supplier, editorial, micro Explorer si applicable) disponibles pour la PR (fichier, tableau ou ticket annexe).
5. [ ] **Médias supplier + sélection** — liste d’assets ou règle d’alimentation Odoo (qui met à jour les images en BO) clarifiée.
6. [ ] **Intégration** — branche cible, **relecteur**, instance de test, procédure **`-u dorevia_ckreyol_marketplace`** + rechargement assets navigateur.
7. [ ] **Bump `__manifest__.py`** — règle de numéro de version si le frontend change (qui valide le patch).
8. [ ] **Recette** — personne désignée pour compléter [PV_RECETTE_PHASE_A_HOMEPAGE_CK.md](PV_RECETTE_PHASE_A_HOMEPAGE_CK.md) après livraison (captures desktop + mobile, verdict §13).

---

## 1. Contexte

La **homepage V1** a été livrée et gelée (arbitrages §9 de [PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md](PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md), plan [PLAN_IMPL_HOMEPAGE_MONTEE_EN_GAMME_V1.md](PLAN_IMPL_HOMEPAGE_MONTEE_EN_GAMME_V1.md)).

Parallèlement, la **plateforme de marque** et le **cadrage design & créa** fixent une ambition plus forte : site **construit**, **dense hiérarchisée**, **désirable** sans folklore ni agressivité commerciale — cf. [PLATEFORME_MARQUE_CK_V1.md](PLATEFORME_MARQUE_CK_V1.md) (effet §13, promesse) et [CADRAGE_DESIGN_CREATION_CK_V1.md](CADRAGE_DESIGN_CREATION_CK_V1.md) (§2–§8, §13, §19–§21).

**Constat MOA** : l’expérience actuelle paraît **insuffisamment appétente** (peu de désir perçu, sensation parfois « maquette » / froide), tout en restant sobre.

---

## 2. Problème à résoudre

1. **Écart de partition** — Le cadrage décrit une **séquence cible** (promesse → portes maîtresses → réassurance → origines → sélections → profondeur de marque → usages → contenus → capture).  
   L’implémentation actuelle (`views/pages/ckr_homepage.xml`) est : **Hero → Explorer (5 portes catalogue) → Supplier → Sélection → Éditorial → Trust**.  
   En particulier : **réassurance** en bas uniquement ; **pas de bloc Origines** dédié ; **pas** de grille « Découvrir / Origines / À offrir / Nouveautés » telle que décrite au §8.2 du cadrage ; pas de blocs usages / blog / capture du §8.7–8.9.

2. **Appétence** — La promesse est surtout **rationnelle** ; la **matière** (photo, rythme, hiérarchie du désir) ne compense pas encore assez la sobriété pour atteindre l’effet recherché (clarté + singularité + crédibilité + **désir** — plateforme §13).

---

## 3. Objectif

Rapprocher la homepage de :

- la **partition** et le **rythme** du cadrage (sans copier une référence externe) ;
- une **appétence perçue** légitime pour CK : *désir par la matière, la clarté, la preuve de sélection et la progression de page* — pas par surcharge promo ni exotisme décoratif.

**Non-objectifs** (hors ticket sauf spin-off) : refonte menu global, refonte `/shop` complète, blog entier, fiche produit (hors snippets présents sur la homepage).

---

## 4. Gels et contraintes (non négociables sans amendement explicite)

| Gel | Document / lieu | Conséquence |
|-----|-----------------|---------------|
| Homepage V1 §9 | `PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md` | Hero **60/40** ; Supplier **plane** ; Editorial **bandeau sobre sans `<h2>`** ; Selection **garde-fou responsive** ; **fil rouge** amber selon arbitrages. **Ne pas modifier** ces points sans **ticket + décision MOA** (éventuellement gel V1.1). |
| Copy hero gelée | `docs/SPEC_HERO_HOMEPAGE.md` §7 | Toute évolution de texte hero au-delà de micro-ajustements = **amendement SPEC** + historique. |
| Explorer | ADR-007, WIREFRAME Bloc 3 | Les **5 portes** restent des **modes de lecture catalogue** ; le rail **manuel** (pas de carrousel auto). Remplacer par une grille « portes maîtresses » du cadrage = **décision d’architecture** (coexistence, remplacement, ou variante) **à trancher avant code**. |
| Standard Odoo | ADR-001 | Pas de contournement lourd du moteur e-commerce. |

---

## 5. Périmètre d’exécution proposé (phases — à valider MOA)

### Phase A — « Appétence sans déplacer la charpente » (priorité si risque de scope)

**Brief créatif opérationnel** : [BRIEF_CRÉA_PHASE_A_HOMEPAGE.md](BRIEF_CRÉA_PHASE_A_HOMEPAGE.md) (checklist livrables, brief par bloc, critères succès MOA).

- **Médias** : brief + remplacement des visuels hero / supplier / sélection (cohérence lumière, cadrage, ratios — cadrage §14).
- **Copy** : sous réserve SPEC hero, enrichissement **sensoriel / usage** **minimal** ailleurs (supplier, editorial, titres de section) si hors gel ou avec amendement ciblé.
- **SCSS** : polish **cartes sélection**, hover/focus, **rythme** espacements entre blocs (cadrage §11), sans violer §9.

**Livrable** : homepage même ordre de blocs, sensation plus **finie** et plus **désirable**.

### Phase B — « Partition » (réordonnancement)

- Exemples à arbitrer : monter **Trust** plus tôt ; intercaler un **bloc réassurance court** dédié ; ordre Supplier / Selection.
- Chaque permutation = recette responsive + outline accessibilité.

**Livrable** : `ckr_homepage.xml` mis à jour + recette.

### Phase C — « Nouveaux blocs cadrage » (plus lourd)

- **Grille portes maîtresses** (Découvrir, Origines, À offrir, Nouveautés) vs ou **en plus** du rail Explorer actuel.
- **Bloc Origines** (visuel + lien catalogue filtré / page dédiée selon doctrine URL).
- **Teasers usages / blog / capture** (newsletter).

**Livrable** : nouveaux snippets + assets + mise à jour `WIREFRAME_HOMEPAGE.md` / `DESIGN.md` §7 si la structure cesse d’être celle de la V1 documentée.

**Recommandation** : valider **A** avant **B** ; trancher **Explorer vs portes maîtresses** avant d’investir **C**.

---

## 6. Critères d’acceptation (homepage)

1. Le visiteur ressent au scroll les **quatre axes** plateforme §13 dans une proportion jugée satisfaisante par MOA (dont **désir** sans perte de **crédibilité**).
2. Aucune régression sur les **gels §9** listés au §4 sans trace écrite d’accord.
3. **Accessibilité** : contrastes charte, focus visibles, titres cohérents avec la structure réelle des headings après changement.
4. **Mobile** : pas de régression sur le hero, le rail Explorer (si conservé), la sélection.
5. **Performance** : pas de dégradation majeure (images dimensionnées / lazy si pertinent).

---

## 7. Livrables attendus (exécution)

- Branche / PR avec changements **QWeb + SCSS** (+ éventuellement images module ou doc brief si assets externes).
- Bump `__manifest__.py` si assets frontend modifiés.
- Mise à jour des docs **si** la structure ou le sens des blocs change : au minimum lien depuis ce ticket vers les fichiers modifiés ; mise à jour `WIREFRAME_HOMEPAGE.md` / proposition si la homepage n’est plus la « V1 » documentaire stricte.
- **PV de recette** : compléter [PV_RECETTE_PHASE_A_HOMEPAGE_CK.md](PV_RECETTE_PHASE_A_HOMEPAGE_CK.md) (desktop + mobile, verdict, gels).

---

## 8. Risques

| Risque | Mitigation |
|--------|------------|
| Conflit cadrage vs gel §9 | Découper en tickets fils ; amendement PROPOSITION/SPEC si besoin. |
| Doublon fonctionnel Explorer / nouvelles portes | Atelier 30 min MOA + schéma unique de navigation. |
| Scope creep blog / shop | Garder le périmètre **homepage** ; ouvrir tickets liés. |

---

## 9. Dépendances

- **MOA** : choix Phase A / B / C et arbitrage Explorer vs portes maîtresses.
- **Édito / studio** : visuels et textes pour Phase A.
- **Dev** : implémentation + recette.

---

## 10. Historique du ticket

| Date | Changement |
|------|------------|
| 2026-04-23 | Création du ticket — constat appétence, écart partition vs [CADRAGE_DESIGN_CREATION_CK_V1.md](CADRAGE_DESIGN_CREATION_CK_V1.md), périmètre homepage, phases A/B/C, gels §9 + SPEC hero. |
| 2026-04-23 | Lien vers [BRIEF_CRÉA_PHASE_A_HOMEPAGE.md](BRIEF_CRÉA_PHASE_A_HOMEPAGE.md) dans la section Phase A — brief créatif opérationnel pour l’équipe créa / intégration. |
| 2026-04-23 | Livrables §7 : renvoi explicite vers [PV_RECETTE_PHASE_A_HOMEPAGE_CK.md](PV_RECETTE_PHASE_A_HOMEPAGE_CK.md) comme trame de recette Phase A. |
| 2026-04-23 | Ajout **§0 Prêt pour dev — Phase A** : checklist MOA / pilotage (8 points) avant ouverture PR. |
| 2026-04-23 | **Phase A — Lot 1 SCSS (PR draft `feat/homepage-phase-a`)** : polish cartes sélection (ombre sobre au repos, montée d’ombre au hover, micro zoom image `scale(1.04)` hover/focus-visible). Aucun changement QWeb, aucun déplacement de bloc, aucune modification copy hero. Bump `__manifest__.py` **19.0.1.6.16 → 19.0.1.6.17** (bundle frontend modifié). Médias hero / supplier / sélection, copy hors hero et consignes BO : en attente livrables MOA (§0 checklist, points 3–5). |
