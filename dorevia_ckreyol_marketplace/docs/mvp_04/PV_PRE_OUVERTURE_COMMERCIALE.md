# PV — Pré-ouverture commerciale CK

**Date** : 2026-05-07  
**Module** : `dorevia_ckreyol_marketplace`  
**Portée** : Consolidation pré-ouverture (P1 → P5)  
**Branche de travail** : `feature/shop-mvp22-visible-wave1`

---

## 1) Synthèse exécutive

Le socle front/catalogue CK est consolidé à un niveau permettant de préparer l’ouverture commerciale, avec une preuve technique minimale du tunnel marchand.

Les chantiers P1 (slugs), P2 (ACL clarifiée), P3 (canon URL), P4 (E2E checkout minimal), P5 (procédure smoke) sont cadrés et matérialisés en code/documentation.

Décision de ce PV : **GO technique minimal pré-ouverture**, sous réserve de suivi des risques résiduels listés ci-dessous.

---

## 2) Évidences principales

### P1 — Unicité slugs collections/origines

- Renforcement implémenté pour `website_id IS NULL` (cas PostgreSQL).
- Tests dédiés ajoutés sur collections et origines.
- Décision documentée dans `docs/mvp_04/DECISION_SLUGS_COLLECTIONS_ORIGINES.md`.

### P2 — ACL / exposition publique collections

- Position clarifiée et documentée : lecture publique utilitaire front maintenue à ce stade.
- Décision tracée dans `docs/mvp_04/DECISION_ACL_COLLECTIONS.md`.
- Audit record rules conservé en suite.

### P3 — Canon URL boutique

- Document canonique produit : `docs/mvp_04/CANON_URL_BOUTIQUE.md`.
- Doctrine consolidée vers un conteneur `/shop` + paramètres `ckr_*`.
- Points de nettoyage documentaire historique identifiés.

### P4 — Tunnel marchand E2E minimal

- Ticket dédié : `docs/mvp_04/TICKET_CHECKOUT_E2E_PRE_OUVERTURE.md`.
- Automatisation dédiée : tag `dorevia_ckr_checkout_e2e`.
- Résultat final d’exécution runtime partagé : **0 failed, 0 error(s)**.
- Alignement technique effectué sur endpoints Odoo 19 effectifs (`/shop/cart/add` JSON-RPC, `/shop/confirmation`).
- Micro-correction P4 intégrée : abandon de l’ajout panier via `/shop/cart/update` au profit du contrat runtime valide.

### P5 — Smoke install/update/rendu

- Procédure documentée : `docs/mvp_04/PROCEDURE_SMOKE_INSTALL_UPDATE.md`.
- Vérification `-u` et endpoints critiques cadrée.
- **Smoke live serveur persistant** exécuté et archivé : `docs/mvp_04/PV_SMOKE_LIVE_SERVEUR_CK.md` (**GO**, base `tenant_o7`, sans 500 ni traceback QWeb/XPath sur les URLs testées).

---

## 3) Risques résiduels

1. **ACL collections** : record rules fines public/portal à auditer et éventuellement durcir.
2. **Canon URL historique** : marquage obsolète/réécriture progressive des anciens documents à poursuivre.
3. **E2E marchand** : couverture encore minimale ; un lot ultérieur doit élargir checkout/paiement/livraison (cas complémentaires).
4. ~~**Smoke HTTP manuel serveur persistant**~~ : exécuté — preuve **`PV_SMOKE_LIVE_SERVEUR_CK.md`** (À reconduire après changements XPath/thème majeurs).

---

## 4) Décision

**GO technique minimal pré-ouverture** pour le palier actuel.

Ce GO ne signifie pas “ouverture publique immédiate”.

Il valide que :

- le socle front/catalogue a été consolidé selon la doctrine fixée ;
- les risques slugs / ACL / canon URL sont désormais identifiés et documentés ;
- une preuve automatisée minimale du parcours d’achat est disponible ;
- les risques restants sont connus, tracés et planifiés.

## 4.1) Non couvert par ce GO

Ce GO ne couvre pas encore :

- l’ouverture publique réelle ;
- la couverture complète checkout / paiement / livraison ;
- l’audit final ACL / record rules ;
- le nettoyage complet de l’historique documentaire ;
- ~~la validation smoke HTTP live avec serveur persistant~~ (réalisée ; voir `docs/mvp_04/PV_SMOKE_LIVE_SERVEUR_CK.md` — hors régressions futures) ;
- les aspects juridiques, CGV, mentions légales et conformité commerciale.

---

## 5) Prochaines actions recommandées

1. Finaliser l’audit ACL/record rules collections.
2. Poursuivre le nettoyage canon URL historique (obsolescence explicite puis convergence).
3. Ouvrir un lot E2E marchand étendu (scénarios additionnels checkout/paiement/livraison).
4. ~~Exécuter le smoke serveur persistant~~ — fait : `docs/mvp_04/PV_SMOKE_LIVE_SERVEUR_CK.md`. Poursuivre avec le lot E2E marchand étendu (hors smoke minimal).
