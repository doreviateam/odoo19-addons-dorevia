# Ticket — Projection de trésorerie de **référence système** (Cash Guard)

**Module principal** : `dorevia_cash_guard`  
**Consommateur** : `dorevia_cash_flow` (trajectoire / **Accueil graphique**)  
**Doctrine** : `docs/cash/DOCTRINE_CASH_MODULES.md` (§ *Projection de référence système*)  
**Lien UX** : `docs/TICKET_CASH_GUARD_HOME_REFERENCE_TRAJECTORY.md` (cockpit / accueil graphique)

---

## Décision fonctionnelle

> Le système doit **générer ou maintenir au préalable** une **projection de trésorerie de référence** côté Cash Guard.  
> Cash Flow **consomme** ensuite cette projection pour afficher la trajectoire.

- **Non** : imposer à l’utilisateur métier, dans le **parcours nominal**, de **créer**, **activer** ou **choisir manuellement** une projection pour que l’**Accueil graphique** fonctionne.  
- **Non** : que `dorevia_cash_flow` **fabrique** ou **installe** silencieusement un document `dorevia.cash.guard` de référence sans cadre explicite côté Guard (pas de « magie » hors périmètre Guard).  
- **Oui** : la **projection de référence** est une **donnée système** (ou pilotée **administrateur**), **hebdomadaire**, avec **date de situation**, **mailles** à jour, **identifiable** comme telle ; l’utilisateur métier ouvre **Projection > Trésorerie > Accueil graphique** et voit **directement** la trajectoire.

**Parcours nominal attendu** :

1. Ouvrir **Projection > Trésorerie > Accueil graphique** ;  
2. Voir la trajectoire de référence.

Si la référence **n’existe pas encore** : message clair + **remédiation** hors parcours métier courant (initialisation système, cron, assistant admin, ou action support) — **pas** « allez fabriquer votre référence à la main » comme étape obligatoire du même parcours.

---

## Périmètre technique à cadrer (implémentation future)

| Sujet | Questions / arbitrages |
|--------|-------------------------|
| **Identification** | Champ dédié (`is_system_reference` / `reference_type`) ? convention de nom ? lien `res.company` ? une seule active par société ? |
| **Création si absente** | Quand déclencher (install module, création société, cron quotidien, premier accès admin) ? paramètres par défaut (journaux, période, seuil) ? |
| **Recalcul** | Fréquence / événements (écritures banque, clôture, cron) ? éviter double recalcul massif ? |
| **Unicité** | Contrainte SQL ou règle métier « au plus une référence active par société » ? comportement si plusieurs documents « candidats » ? |
| **Réinitialisation** | Action réservée groupe manager / admin ? duplicata contrôlé ? archivage de l’ancienne référence ? |
| **Cash Flow** | Remplacer ou compléter `_resolve_reference_guard` par résolution **explicite** sur la projection marquée référence ; message d’erreur aligné sur l’absence de **donnée système**, pas sur « créez une projection au hasard ». |

---

## État actuel (transparence)

Aujourd’hui, `dorevia_cash_flow` résout la « référence » via une **heuristique** sur les documents Guard existants (`_resolve_reference_guard` : actif, hebdo, mailles présentes, tri `situation_date`). Cela **satisfait** l’absence de formulaire dans le parcours lecture, mais **ne garantit pas** qu’une projection de référence **système** existe ni qu’elle soit **maintenue** sans action utilisateur sur les données.

Ce ticket formalise l’**écart** à combler entre cet état et la décision produit ci-dessus.

---

## Critères d’acceptation (brouillon)

- [ ] Au moins une **projection de référence** par société (règle d’unicité documentée).  
- [ ] **Identification** stable pour Cash Flow (plus seulement heuristique « premier candidat »).  
- [ ] **Parcours nominal** Accueil graphique : courbe sans étape préalable « choisir une projection » pour l’utilisateur métier.  
- [ ] **Absence** de référence : message orienté **admin / système**, pas checklist atelier métier comme seule voie.  
- [ ] **Cash Flow** : lecture seule inchangée ; pas de création de `dorevia.cash.guard` depuis le module Flow.  
- [ ] Doctrine + SPEC + README mis à jour après livraison.

---

## Références

- `docs/cash/DOCTRINE_CASH_MODULES.md`  
- `dorevia_cash_flow/docs/SPEC_CASH_FLOW_TRAJECTORY.md` § 5.5  
- `dorevia_cash_flow/models/cash_flow_trajectory_wizard.py` (`_resolve_reference_guard`)
