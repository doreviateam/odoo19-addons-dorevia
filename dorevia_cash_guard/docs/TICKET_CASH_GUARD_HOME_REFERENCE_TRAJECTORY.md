# Ticket — Accueil Cash Guard centré sur la trajectoire de référence

**Module** : `dorevia_cash_guard`  
**Dépendance doctrine** : `docs/cash/DOCTRINE_CASH_MODULES.md` (§ *Réutilisation de la trajectoire de référence dans Cash Guard*)  
**Rapport avec Cash Flow** : cette évolution **ne remet pas en cause** le **GO V1.1** de `dorevia_cash_flow`. Elle formalise l’étape suivante : faire de la trajectoire la **vérité de référence visible au cœur** de l’expérience Cash (y compris depuis l’entrée atelier).

## État actuel de l’UI vs cible cockpit

> À l’état actuel, la trajectoire de référence est consultable dans `dorevia_cash_flow` via **Comptabilité > Analyse > Gestion > Trajectoire de trésorerie**.  
> Cash Guard reste l’atelier de projection, accessible via le menu **Projection > Trésorerie**.  
> Ce ticket décrit une évolution UX future : afficher cette même trajectoire de référence en lecture seule dans un cockpit d’accueil Cash Guard, avec les actions d’atelier autour.  
> Cette évolution n’est pas encore implémentée et ne remet pas en cause la séparation actuelle des rôles.

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

- [ ] Menu ou première vue Cash Guard présente un **cockpit** avec la trajectoire de référence visible.  
- [ ] La trajectoire est **strictement alignée** avec l’écran Cash Flow équivalent (même projection de référence, même période / repères selon règles produit).  
- [ ] Aucun contrôle d’UI sur la courbe dans ce contexte qui **modifie** la trajectoire sans passer par les écrans / flux prévus (Guard pour données, Flow pour lecture).  
- [ ] Les **actions d’atelier** listées ci-dessus sont accessibles depuis l’accueil (liens ou boutons clairs).  
- [ ] README ou SPEC Cash Guard mis à jour ; doctrine déjà mise à jour en amont.

---

## Notes d’implémentation (à affiner en conception)

- Vérifier **dépendance module** `dorevia_cash_guard` → `dorevia_cash_flow` si l’accueil embarque obligatoirement le graphique ; ou comportement **dégradé** (message + lien vers Cash Flow) si Flow absent — à trancher produit.  
- Réutiliser de préférence une **action client** / **embed** documentée côté Cash Flow pour éviter la duplication.

---

## Références

- `docs/cash/DOCTRINE_CASH_MODULES.md`  
- `dorevia_cash_flow/docs/SPEC_CASH_FLOW_TRAJECTORY.md`  
- `dorevia_cash_flow/docs/TICKET_CASH_FLOW_V1_1_TRAJECTOIRE_REFERENCE.md`
