# Ticket — Accueil Cash Guard centré sur la trajectoire de référence

**Module** : `dorevia_cash_guard`  
**Dépendance doctrine** : `docs/cash/DOCTRINE_CASH_MODULES.md` (§ *Réutilisation de la trajectoire de référence dans Cash Guard*)  
**Rapport avec Cash Flow** : cette évolution **ne remet pas en cause** le **GO V1.1** de `dorevia_cash_flow`. Elle formalise l’étape suivante : faire de la trajectoire la **vérité de référence visible au cœur** de l’expérience Cash (y compris depuis l’entrée atelier).

## État actuel de l’UI vs cible cockpit

> La trajectoire de référence est consultable dans `dorevia_cash_flow` via **Comptabilité > Analyse > Gestion > Trajectoire de trésorerie**.  
> Avec **`dorevia_cash_flow`** installé, **Projection > Cockpit trésorerie** affiche la **même** trajectoire de référence en lecture seule, avec raccourcis atelier (implémentation dans `dorevia_cash_flow` pour éviter une dépendance circulaire Guard → Flow).  
> **Projection > Trésorerie** ouvre toujours la liste des documents de projection.

---

## Objectif

Faire de l’entrée **Cash Guard** une **page d’accueil / cockpit** centrée sur la **trajectoire de référence** du pilotage cash, tout en conservant Cash Guard comme **atelier de projection** (pas un second producteur de « vérité courbe »).

---

## Comportement attendu

1. **Trajectoire en lecture seule**  
   Afficher la même trajectoire que celle portée par **`dorevia_cash_flow`** (résolution de référence, points, repères alignés sur la SPEC Cash Flow). Aucune modification de cette trajectoire **depuis** l’UI Cash Guard (pas d’édition graphique parallèle, pas de second jeu de règles de courbe).

2. **Actions de travail autour** (atelier)  
   Autour du bloc trajectoire, proposer explicitement les parcours métier :  
   - ouvrir la **projection source** ;  
   - **recalculer / actualiser** la projection ;  
   - consulter les **documents explicatifs** ;  
   - ajuster les **paramètres de projection** ;  
   - tester des **hypothèses** ;  
   - accéder aux **simulations** (modules concernés).

3. **Réutilisation technique**  
   **Réutiliser** `dorevia_cash_flow` (actions client, vues, services ou extrait documenté) plutôt que **recoder** une trajectoire ou un moteur graphique concurrent dans Cash Guard. Toute dépendance (manifest, bridge) doit être **explicite** et documentée dans le README / SPEC du guard.

---

## Hors périmètre / interdits (doctrine)

- Créer une **seconde trajectoire « officielle »** dans Cash Guard.  
- Porter une **logique dupliquée** de construction des points de courbe ou un **second moteur** graphique concurrent.  
- Donner l’impression que la courbe d’accueil Guard serait **éditable** ou **définissable** sans passer par la chaîne Guard / Flow documentée.

---

## Critères d’acceptation (brouillon)

- [x] Menu ou première vue Cash Guard présente un **cockpit** avec la trajectoire de référence visible (**Projection > Cockpit trésorerie**, livré dans `dorevia_cash_flow`).  
- [x] La trajectoire est **strictement alignée** avec l’écran Cash Flow équivalent (même résolution de référence, même `_prepare_chart_action` / client action).  
- [x] Aucun contrôle d’UI sur la courbe dans ce contexte qui **modifie** la trajectoire sans passer par les écrans / flux prévus (pas « Changer de projection » sur le graphique cockpit ; audit via lien dédié).  
- [x] Les **actions d’atelier** principales sont accessibles depuis le cockpit (ouvrir projection, actualiser, liste, audit, vue Analyse).  
- [x] README / doctrine mis à jour en lien avec cette livraison.

---

## Notes d’implémentation (à affiner en conception)

- **Dépendance** : le cockpit est livré dans **`dorevia_cash_flow`** (`action_open_guard_cockpit`, menu **Projection > Cockpit trésorerie**) pour éviter `dorevia_cash_guard` → `dorevia_cash_flow` (cycle).  
- **Rafraîchissement** : `action_refresh_points_from_guard` sur l’assistant régénère les points après `action_recompute_projection` sur le document Guard.

---

## Références

- `docs/cash/DOCTRINE_CASH_MODULES.md`  
- `dorevia_cash_flow/docs/SPEC_CASH_FLOW_TRAJECTORY.md`  
- `dorevia_cash_flow/docs/TICKET_CASH_FLOW_V1_1_TRAJECTOIRE_REFERENCE.md`
