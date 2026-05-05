# TICKET — Compte client MVP 03 (B2C / demande pro)

**ID** : `COMPTE-CLIENT-MVP03`  
**Date d’ouverture** : 2026-05  
**Priorité** : **P2** *(à confirmer pilotage)*  
**Statut** : **Brouillon** — **validation MOA + arbitrages §4 requis** avant branche dev dédiée.  
**Module** : `dorevia_ckreyol_marketplace` (+ configuration Odoo site / CRM selon arbitrage).

**Sources de vérité produit / UX** :

| Document | Rôle |
|----------|------|
| [README MVP 03](README.md) | Intention dossier, doctrine, hors périmètre |
| [1_COMPTE_CLIENT_PARCOURS.md](1_COMPTE_CLIENT_PARCOURS.md) | Parcours A/B, états, points d’entrée, arbitrages métier |
| [2_COMPTE_CLIENT_SPEC_UX.md](2_COMPTE_CLIENT_SPEC_UX.md) | Spec UX, wording interdit/privilégié, garde-fou `/my`, recette interface |

**Doctrine** : [DOCTRINE_CK_ECOMMERCE_B2C_B2B.md](../direction/DOCTRINE_CK_ECOMMERCE_B2C_B2B.md) ; [ADR-CKR-001](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-001) (standard d’abord) ; [ADR-CKR-009](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-009) (sanctuarisation tunnel) ; [ADR-CKR-010](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-010) (B2C/B2B).

---

## 1. Contexte

Le site doit distinguer sans ambiguïté :

1. **Parcours A** — **compte particulier** (B2C), friction minimale, aligné portail Odoo standard.
2. **Parcours B** — **demande** d’ouverture de compte professionnel ; **aucune** activation automatique des tarifs ou conditions B2B tant que le profil n’est pas validé côté Odoo.

Les habillages existants à respecter ou étendre : [`views/auth/ckr_login.xml`](../../views/auth/ckr_login.xml), [`views/portal/ckr_portal.xml`](../../views/portal/ckr_portal.xml), [`views/layout/ckr_header.xml`](../../views/layout/ckr_header.xml).

---

## 2. Objectif livrable

- Rendre **évidents** les deux chemins (particulier vs demande pro) depuis **login** / **signup** (ou page dédiée — arbitrage).
- Garantir que le parcours B **ne promet pas** un accès immédiat aux tarifs pro (copies conformes [2_COMPTE_CLIENT_SPEC_UX.md §5.3](2_COMPTE_CLIENT_SPEC_UX.md)).
- Préserver l’**achat invité** si activé en configuration Odoo ([1_COMPTE_CLIENT_PARCOURS §4.1](1_COMPTE_CLIENT_PARCOURS.md)).
- Sur **`/my`** : **aucun** badge, zone ou libellé « pro » tant que le partenaire n’est pas validé B2B ([2_COMPTE_CLIENT_SPEC_UX.md §3 et §6](2_COMPTE_CLIENT_SPEC_UX.md)).

---

## 3. Périmètre fonctionnel (exécutable)

### 3.1 Parcours A — inscription / connexion particulier

- Liens cohérents depuis le header vers **`/web/login`** et **`/web/signup`** si `auth_signup` est activé.
- Formulaire inscription **sans** champs entreprise obligatoires mélangés au B2C.
- Messages d’erreur **lisibles** (accessibilité minimale — [2_COMPTE_CLIENT_SPEC_UX §7](2_COMPTE_CLIENT_SPEC_UX.md)).
- Non-régression : accès **`/my`** après création ; checkout **sans** casse si invité autorisé.

### 3.2 Parcours B — demande compte pro

- **Entrée** dédiée (URL, section signup, ou page séparée — **à figer §4**). Modal **non recommandée par défaut** si elle brouille la distinction A/B ([2_COMPTE_CLIENT_SPEC_UX §9](2_COMPTE_CLIENT_SPEC_UX.md)).
- Formulaire avec **champs minimum utiles** (société, contact, message, secteur — **liste figée MOA + ticket**).
- **Confirmation** après envoi (écran ou message) : ton « demande transmise / en traitement », **sans** promesse de délai non validée métier.
- **Back-end** : création **lead / opportunité / activité** ou équivalent **standard** Odoo — **sans** basculer automatiquement pricelist ou catégorie partenaire B2B ([1_COMPTE_CLIENT_PARCOURS §4.2](1_COMPTE_CLIENT_PARCOURS.md)).

### 3.3 Emails et notifications *(arbitrage §4)*

- Selon décision MOA : email automatique au demandeur ; copie ou notification équipe CK ; alignement **web vs email** ([2_COMPTE_CLIENT_SPEC_UX §9](2_COMPTE_CLIENT_SPEC_UX.md)).

### 3.4 Conformité / légal *(rappel)*

- Finalités et mentions adaptées au traitement « demande pro » ; renvois vers [`/privacy`](../../views/pages/ckr_privacy.xml) et pages légales existantes ([1_COMPTE_CLIENT_PARCOURS §7](1_COMPTE_CLIENT_PARCOURS.md)).

---

## 4. Arbitrages à trancher avant ou pendant le dev

Les lignes ci-dessous **bloquent** ou **orientent** l’implémentation ; cocher en réunion MOA / tech.

| # | Sujet | Décision attendue |
|---|--------|-------------------|
| 1 | **`auth_signup`** activé sur le site ? | oui / non |
| 2 | **Séparation A/B** : une page avec deux blocs vs **deux URLs** (ex. signup vs `/demande-compte-pro`) | |
| 3 | **Achat invité** : confirmé activé — le livrable **ne doit pas** le masquer | oui / n/a |
| 4 | **Demande pro** : chaîne technique retenue (`website_form` + CRM, contrôleur dédié, email métier, etc.) | |
| 5 | **Champs** obligatoires formulaire B (liste minimale) | |
| 6 | **Email** : auto au demandeur ? copie CK ? message type ? | |
| 7 | **Validation métier** : qui traite ; impact ultérieur sur pricelist / catégorie partenaire *(hors automatisation MVP si non validé)* | |
| 8 | **Tests Odoo** : tag dédié proposé `dorevia_ckr_account_mvp03` *(à valider)* | |

---

## 5. Contraintes techniques

- **Standard Odoo CE en priorité** : `website`, `portal`, `auth_signup`, `sale`, `contacts`, `crm` ou `website_form` selon arbitrage — pas de « double système de comptes » sans justification ([1_COMPTE_CLIENT_PARCOURS §2.1](1_COMPTE_CLIENT_PARCOURS.md)).
- **Pas** de boutique catalogue parallèle ; pas d’exposition prix B2B sur seule demande formulaire.
- Incrémenter le **`version`** du manifeste après livraison ; documenter les dépendances `__manifest__.py` si nouveaux modules.

---

## 6. Hors périmètre (sauf ticket ultérieur)

- Workflow complet **validation B2B** (équipe sales, relances) au-delà de la **capture** de la demande et du message de confirmation.
- Personnalisation poussée du portail (tableaux de bord pro) non requis pour clôturer ce ticket si non prévu MOA.
- Évolution doctrine prix / trois mondes.

---

## 7. Critères d’acceptation

- [ ] Distinction **claire** particulier / demande pro (desktop + mobile).
- [ ] Parcours A : création compte + login + `/my` **sans** régression checkout ; invité **toujours** disponible si configuré.
- [ ] Parcours B : envoi demande + confirmation UX ; **aucune** suggestion d’activation tarifs pro immédiate (repère [2_COMPTE_CLIENT_SPEC_UX §5.3](2_COMPTE_CLIENT_SPEC_UX.md)).
- [ ] Portail `/my` : **pas** de signal « compte pro » avant validation Odoo.
- [ ] Accessibilité minimale : labels, erreurs textuelles, focus ([2_COMPTE_CLIENT_SPEC_UX §7](2_COMPTE_CLIENT_SPEC_UX.md)).
- [ ] Tests automatisés : au minimum **non-régression** sur flux concernés ; tag Odoo **figé en PR** ([1_COMPTE_CLIENT_PARCOURS §8](1_COMPTE_CLIENT_PARCOURS.md)).
- [ ] Doctrine [ADR-010](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-010) respectée (pas de second catalogue implicite).

---

## 8. Recette

- **PV** : à produire après implémentation — `PV_RECETTE_COMPTE_CLIENT_MVP03_CK.md` *(nom indicatif)*.
- Jeux manuels : parcours A, parcours B, invité, erreurs formulaire, **petit écran**.

---

## 9. Prêt pour dev — checklist

1. [ ] **GO MOA** sur copies définitives (titres, CTA, message confirmation B).
2. [ ] **Arbitrages §4** complétés (au minimum 1–6 pour démarrer).
3. [ ] **Branche** et responsable dev assignés.
4. [ ] **Base de test** : `auth_signup` / invité / CRM alignés avec l’environnement cible.

---

## Historique

| Date | Événement |
|------|-----------|
| 2026-05 | Création du ticket d’exécution MVP 03 à partir des docs parcours, spec UX et structure tickets module. |
