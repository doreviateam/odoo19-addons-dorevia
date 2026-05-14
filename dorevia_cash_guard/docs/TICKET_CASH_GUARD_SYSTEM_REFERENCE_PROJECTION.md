# Ticket — Projection de trésorerie de **référence système** (Cash Guard)

**Module principal** : `dorevia_cash_guard`  
**Consommateur** : `dorevia_cash_flow` (trajectoire / **Cash Flow**)  
**Doctrine** : `docs/cash/DOCTRINE_CASH_MODULES.md` (§ *Projection de référence système*)  
**Lien UX** : `docs/TICKET_CASH_GUARD_HOME_REFERENCE_TRAJECTORY.md` (cockpit / projection de référence)

**Synthèse architecture** : la référence système est une projection **`dorevia.cash.guard` standard**, **taguée**, **unique** par société (active), **protégée** contre disparition silencieuse, et **consommée en priorité** par Cash Flow ; l’heuristique actuelle reste **fallback** transitoire ou de migration.

---

## Décision fonctionnelle

> Le système doit **générer ou maintenir au préalable** une **projection de trésorerie de référence** côté Cash Guard.  
> Cash Flow **consomme** ensuite cette projection pour afficher la trajectoire.

- **Non** : imposer à l’utilisateur métier, dans le **parcours nominal**, de **créer**, **activer** ou **choisir manuellement** une projection pour que **Cash Flow** fonctionne.  
- **Non** : que `dorevia_cash_flow` **fabrique** ou **installe** silencieusement un document `dorevia.cash.guard` de référence sans cadre explicite côté Guard (pas de « magie » hors périmètre Guard).  
- **Oui** : la **projection de référence** est une **donnée système** (ou pilotée **administrateur**), **hebdomadaire**, avec **date de situation**, **mailles** à jour, **identifiable** comme telle ; l’utilisateur métier ouvre **Comptabilité > Projection de trésorerie > Cash Flow** et voit **directement** la trajectoire.

**Parcours nominal attendu** :

1. Ouvrir **Comptabilité > Projection de trésorerie > Cash Flow** ;  
2. Voir la trajectoire de référence.

Si la référence **n’existe pas encore** : message clair + **remédiation** hors parcours métier courant (initialisation système, cron, assistant admin, ou action support) — **pas** « allez fabriquer votre référence à la main » comme étape obligatoire du même parcours.

> La projection de référence système est une **donnée structurante**. Elle ne doit pas pouvoir **disparaître silencieusement**.

---

## Décisions d’architecture — **modèle cible V1** (validé)

### Représentation : projection standard taguée (pas de modèle dédié)

Pour la **première implémentation**, la référence est un document **`dorevia.cash.guard` habituel**, marqué par un champ dédié — **pas** un modèle métier séparé (évite duplication de logique : mailles, recalcul, audit, champs, Cash Flow inchangé sur la forme des données).

**Champ V1** :

```text
is_system_reference = True   # Boolean sur dorevia.cash.guard
```

**Évolution possible** : ajouter plus tard un champ du type `reference_type` (ex. valeur `system_reference`) si d’autres familles de référence doivent coexister sans ambiguïté.

### Unicité et contraintes fonctionnelles

- **Au plus une** projection de référence système **active** par **`company_id`** (unicité métier à faire respecter par contrainte SQL et/ou `create` / `write` / contrainte Python).  
- **Périodicité** : hebdomadaire (alignement trajectoire Cash Flow actuelle).  
- **Horizon** : cohérent avec le pilotage **90 jours** (paramétrage / alignement période déjà porté par Guard).  
- **Cash Flow** : doit résoudre **en priorité** cette projection (`is_system_reference`, active, éligible) avant toute autre règle.

### Résolution côté Cash Flow

1. **Priorité** : recherche de la projection **taguée** référence système pour `env.company`.  
2. **Fallback transitoire / migration** : si aucune projection taguée n’est trouvée, conserver l’**heuristique** actuelle `_resolve_reference_guard` (document actif, hebdo, mailles, tri `situation_date`) jusqu’à bascule complète des bases.  
3. **Objectif** : à terme, le fallback ne sert que **migration** ou **secours** documenté, pas la définition durable de la « vérité » produit.

### Protection (archivage / suppression)

- Un **utilisateur métier** ne peut **pas** archiver ni supprimer la projection de référence système (règles `unlink` / `action_archive` / `write({'active': False})` selon groupes).  
- **Archivage / suppression** : réservé à un **profil admin / technique** ; toute opération qui retirerait la référence doit soit **exiger** une référence de remplacement, soit **déclencher** une recréation contrôlée (workflow à définir en implémentation).  
- Le **cockpit Cash Flow** ne doit **jamais** se retrouver **sans référence** de façon durable **sans message explicite** (pas d’écran vide silencieux).

### Initialisation (à détailler en implémentation)

Pistes validées comme **périmètre à cadrer techniquement** (une ou plusieurs peuvent coexister) :

- création **post-install** / post-migration si possible ;  
- création ou complément à l’**ouverture** du cockpit **uniquement via logique Cash Guard** (pas de création opaque depuis `dorevia_cash_flow`) ;  
- **cron** de maintien (recalcul / cohérence) ;  
- **action admin** du type « Créer / régénérer la référence système ».

---

## Messages utilisateur — actuel vs cible

**Tant que le ticket n’est pas implémenté**, les messages peuvent encore orienter vers l’atelier (**Comptabilité > Projection de trésorerie > Cash Guards**) — acceptable transitoirement.

**Cible** après livraison : ne **pas** faire porter la responsabilité à l’utilisateur métier pour un défaut de **donnée système**. Exemple de formulation :

> Aucune projection de référence système n’est disponible pour cette société. Veuillez contacter un administrateur ou initialiser la référence Cash Guard.

À appliquer côté **`dorevia_cash_flow`** (erreurs lecture trajectoire) et, le cas échéant, messages cohérents côté **Guard** lorsque l’admin initie les actions.

---

## État actuel (transparence)

Aujourd’hui, `dorevia_cash_flow` résout la « référence » via une **heuristique** sur les documents Guard existants (`_resolve_reference_guard` : actif, hebdo, mailles présentes, tri `situation_date`). Cela **satisfait** l’absence de formulaire dans le parcours lecture, mais **ne garantit pas** qu’une projection de référence **système** existe ni qu’elle soit **maintenue** sans action utilisateur sur les données.

Ce ticket formalise l’**écart** à combler entre cet état et la décision produit ci-dessus.

---

## Critères d’acceptation (brouillon)

- [ ] Champ **`is_system_reference`** (ou équivalent validé) sur `dorevia.cash.guard`, document **standard** (mêmes mailles, recalcul, audit).  
- [ ] **Unicité** : au plus une référence système **active** par société ; contrainte ou garde-fous documentés.  
- [ ] **Cash Flow** : résolution **prioritaire** sur la projection taguée ; heuristique actuelle en **fallback** migration / transitoire.  
- [ ] **Protection** : pas d’archivage / suppression par profil métier ; admin avec règles de remplacement ou recréation ; pas de disparition silencieuse.  
- [ ] **Parcours nominal Cash Flow** : courbe sans étape « choisir une projection » pour l’utilisateur métier.  
- [ ] **Messages** : formulation cible admin / initialisation (au moins pour les cas « référence système absente » une fois la feature livrée).  
- [ ] **Cash Flow** : toujours pas de création de `dorevia.cash.guard` depuis le module Flow.  
- [ ] Doctrine + SPEC + README mis à jour après livraison code.

---

## Sous-ticket dev

Implémentation code et tests : **`TICKET_IMPL_CASH_GUARD_SYSTEM_REFERENCE.md`** (champ, unicité, résolution Flow, protection, action admin, tests).

---

## Références

- `docs/cash/DOCTRINE_CASH_MODULES.md`  
- `dorevia_cash_guard/docs/TICKET_IMPL_CASH_GUARD_SYSTEM_REFERENCE.md` — implémentation (code + tests)  
- `dorevia_cash_flow/docs/SPEC_CASH_FLOW_TRAJECTORY.md` § 5.5  
- `dorevia_cash_flow/models/cash_flow_trajectory_wizard.py` (`_resolve_reference_guard`)
