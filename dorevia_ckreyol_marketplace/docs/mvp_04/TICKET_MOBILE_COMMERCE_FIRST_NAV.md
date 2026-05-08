# TICKET — Doctrine navigation mobile CK "Commerce First" (cadrage)

**ID** : `NAV-MOBILE-COMMERCE-FIRST-MVP04`  
**Date d'ouverture** : 2026-05  
**Priorité** : **P1 (cadrage)**  
**Statut** : **À valider (doctrine et mapping)**  
**Module** : `dorevia_ckreyol_marketplace`

**Dossier lié** : `docs/mvp_04/`  
**Références** : [README.md](README.md), [TICKET_HEADER_NAV_MVP04.md](TICKET_HEADER_NAV_MVP04.md), [TICKET_CONSOLIDATION_PRE_OUVERTURE.md](TICKET_CONSOLIDATION_PRE_OUVERTURE.md)

---

## 1. Objectif

Formaliser la doctrine de navigation CK avant toute nouvelle évolution du drawer/header mobile.

Le cadrage doit rendre explicite la priorité mobile suivante :

- **desktop** : équilibre commerce / éditorial / promotionnel / communautaire ;
- **mobile** : commerce d abord, éditorial en soutien, communautaire différé.

Ce ticket est **documentaire**. Il ne déclenche pas de refonte immédiate.

---

## 2. Doctrine

La navigation mobile CK n est pas une réduction mécanique du desktop.  
Elle priorise l action marchande : **boutique, recherche, panier, favoris, promotions**.

Principes directeurs :

- la première lecture mobile doit orienter vers l achat ;
- l éditorial reste présent, mais en soutien du parcours marchand ;
- le communautaire reste accessible, mais non prioritaire au premier niveau mobile ;
- la richesse desktop est préservée sur desktop, sans duplication brute en mobile.

---

## 3. Mapping des entrees (L1 / L2 / L3)

Le mapping ci-dessous constitue la base de travail. Il devra être ajusté à l état réel du menu publié.

## 3.1 L1 — Action commerce (prioritaire mobile)

- Boutique ;
- Recherche ;
- Panier ;
- Favoris ;
- Promotions ;
- Kits / Packs (si la porte est active dans la navigation cible).

Précision :

- `Recherche`, `Panier` et `Favoris` ne sont pas forcément des liens de menu textuels classiques ;
- ils peuvent rester exposés comme actions du header ;
- leur classement en L1 signifie surtout qu ils doivent être immédiatement accessibles en mobile.

## 3.2 L2 — Soutien éditorial (utile au parcours)

- Origines ;
- Collections ;
- Idees cadeaux ;
- Recettes.

## 3.3 L3 — Communautaire differe

- Communaute ;
- Blog ;
- contenus relationnels ou non directement marchands.

---

## 4. Règles non négociables

1. Acces rapide a la boutique en premier niveau mobile.
2. Recherche, panier et favoris restent accessibles sans friction.
3. Aucun état hybride entre navigation horizontale desktop et drawer mobile.
4. Le cadrage mobile n impose pas de modification de la doctrine desktop.
5. Panier/favoris ne sont pas relégués sous des rubriques éditoriales.
6. Le communautaire n occupe pas le premier niveau mobile.
7. La navigation mobile reste actionnable (libellés clairs, hiérarchie courte, pas de surcharge).

---

## 5. Scope IN / OUT

## 5.1 IN

- doctrine responsive mobile-first pour la navigation CK ;
- mapping L1/L2/L3 ;
- règles de recette fonctionnelles pour valider la hiérarchie mobile ;
- hypothèse de future implémentation drawer, sans exécution immédiate.

## 5.2 OUT

- modification immédiate du header/drawer ;
- refonte desktop ;
- création de nouveaux contenus éditoriaux ;
- réarchitecture des pages éditoriales ;
- instrumentation réelle si elle n est pas déjà disponible.

---

## 6. Critères GO / NO GO (cadrage)

## 6.1 GO

Le cadrage est validé si :

- la hiérarchie mobile est explicite et exploitable ;
- le desktop reste inchangé dans l arbitrage ;
- les entrées L1 privilégient clairement l achat ;
- éditorial et communautaire restent accessibles sans prendre la priorité.

## 6.2 NO GO

Le cadrage est refusé si :

- le mobile reproduit mécaniquement le desktop ;
- le drawer devient long sans hiérarchie priorisée ;
- panier/recherche/favoris ne sont pas prioritaires ;
- la doctrine force une refonte header non arbitrée.

---

## 7. Règles de recette du cadrage (avant implémentation)

Checklist de validation documentaire :

- la doctrine mobile-first est comprise et partagée (produit, design, dev) ;
- chaque entrée de menu est rattachée à L1, L2 ou L3 ;
- aucune ambiguïté sur le fait que mobile != desktop condensé ;
- le ticket ne contient aucune exigence de refonte immédiate ;
- la suite est explicitement séparée dans un ticket implémentation.

---

## 8. Suite (ticket séparé, après validation)

Après validation de ce cadrage uniquement, ouvrir :

`TICKET_IMPLEMENTATION_DRAWER_MOBILE_COMMERCE_FIRST.md`

Ce ticket d implémentation devra :

- traduire L1/L2/L3 dans le drawer mobile ;
- conserver la doctrine desktop existante ;
- rester dans un diff ciblé navigation mobile (sans refonte globale header).

---

## 9. Décision

La doctrine `mobile commerce-first` est retenue comme cadrage de navigation CK.

Elle ne modifie pas la doctrine desktop, qui conserve un équilibre entre commerce, éditorial, promotionnel et communautaire.

Elle ne déclenche pas de refonte immédiate du header/drawer.

Toute implémentation devra faire l objet d un ticket séparé, avec un diff ciblé sur la navigation mobile.

