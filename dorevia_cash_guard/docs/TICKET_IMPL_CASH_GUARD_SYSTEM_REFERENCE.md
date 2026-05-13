# Ticket dev — Implémentation **projection de référence système**

**Type** : sous-ticket d’implémentation (revue ciblée)  
**Cadrage produit / archi** : `TICKET_CASH_GUARD_SYSTEM_REFERENCE_PROJECTION.md`  
**Doctrine** : `docs/cash/DOCTRINE_CASH_MODULES.md` (§ *Projection de référence système*)

Ce document isole le **code** et les **tests** : il ne remplace pas la doctrine ni le ticket de cadrage.

---

## Objectif

Livrer en code les arbitrages V1 : projection **`dorevia.cash.guard`** standard taguée **`is_system_reference`**, **unique** par société (active), **résolue en priorité** par Cash Flow, **protégée** contre archivage / suppression métier, avec **action admin** d’initialisation / réinitialisation et **tests** associés.

---

## Périmètre livrable

1. **Champ** `is_system_reference` (`Boolean`, défaut `False`) sur `dorevia.cash.guard` — vue formulaire / liste (filtre) selon conventions du module ; pas de `reference_type` en V1 sauf arbitrage contraire en revue.

2. **Unicité** : au plus **une** projection avec `is_system_reference=True` et `active=True` par **`company_id`** — contrainte SQL (`EXCLUDE` / unique partiel selon support PG) et/ou contrainte Python `models.Constraint` + validation en `create` / `write`.

3. **`_resolve_reference_guard`** (`dorevia_cash_flow`, `dorevia.cash.flow.trajectory.wizard`) :  
   - recherche **d’abord** la référence système pour `env.company` (active, hebdomadaire, mailles si règle inchangée) ;  
   - **sinon** conserver l’**heuristique** actuelle (fallback migration / transitoire).

4. **Protection** : empêcher **utilisateur métier** (groupe Cash Guard user / règle existante) d’**archiver** ou **supprimer** (et si pertinent de **désactiver** le flag référence) sur le document référence système ; laisser **admin / groupe technique** (à définir : ex. `group_cash_guard_manager` ou groupe dédié) pour opérations sensibles.

5. **Action admin** (serveur ou wizard léger) : **initialiser / régénérer** la projection de référence système pour la société courante (paramètres par défaut documentés dans le ticket parent ou ici après atelier).

6. **Tests** :  
   - unicité (deuxième création / `write` rejeté) ;  
   - résolution Flow (tag prioritaire vs fallback) ;  
   - protection archive / unlink (métier vs admin) ;  
   - message ou comportement quand aucune référence (selon maturité du flux d’init).

---

## Hors périmètre (sauf décision explicite)

- Champ `reference_type` (préparation seulement si coût marginal).  
- Cron de maintien complet (peut être ticket suivant).  
- Création silencieuse à l’ouverture cockpit sans règle métier validée (documenter dans ticket parent avant de coder).

---

## Critères de fermeture (checklist)

- [ ] Migration / `ir.model.fields` + droits d’accès si besoin.  
- [ ] Contrainte unicité active + tests.  
- [ ] `_resolve_reference_guard` priorise le tag ; tests régression heuristique.  
- [ ] Règles archive / unlink / `is_system_reference` write.  
- [ ] Action admin documentée (README ou SPEC § touchée).  
- [ ] Messages erreur Cash Flow alignés **cible admin** lorsque la référence système est absente (si livré dans ce ticket).  
- [ ] SPEC § 5.5 + README ajustés si comportement observable change.

---

## Références code

- `dorevia_cash_guard/models/cash_guard.py` — modèle `dorevia.cash.guard`.  
- `dorevia_cash_flow/models/cash_flow_trajectory_wizard.py` — `_resolve_reference_guard`, `action_open_reference_trajectory`, `action_open_guard_cockpit`.  
- `dorevia_cash_guard/security/` — groupes pour distinguer métier / admin.
