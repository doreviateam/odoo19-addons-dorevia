# TICKET — Compte client MVP 03 (B2C / demande pro)

**ID** : `COMPTE-CLIENT-MVP03`  
**Date d’ouverture** : 2026-05  
**Priorité** : **P2** *(à confirmer pilotage)*  
**Statut** : **Brouillon — prêt pour arbitrage MOA / tech** *(pas de GO dev tant que §4 n’est pas complété et validé)*.  
**Module** : `dorevia_ckreyol_marketplace` (+ configuration Odoo site / CRM selon arbitrage).

**Sources de vérité produit / UX** :

| Document | Rôle |
|----------|------|
| [README MVP 03](README.md) | Intention dossier, doctrine, hors périmètre |
| [1_COMPTE_CLIENT_PARCOURS.md](1_COMPTE_CLIENT_PARCOURS.md) | Parcours A/B, états, points d’entrée, arbitrages métier |
| [2_COMPTE_CLIENT_SPEC_UX.md](2_COMPTE_CLIENT_SPEC_UX.md) | Spec UX, wording interdit/privilégié, garde-fou `/my`, recette interface |

Ce ticket devient **exécutable** uniquement après **complétion des arbitrages §4** ; avant cela, il sert de **cadrage d’exécution**.

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
- La demande pro **ne doit pas** créer automatiquement un **utilisateur portail** « professionnel », **sauf arbitrage explicite** MOA / tech — on évite de mélanger **demande commerciale** et **compte utilisateur**.

### 3.3 Emails et notifications *(arbitrage §4)*

- Selon décision MOA : email automatique au demandeur ; copie ou notification équipe CK ; alignement **web vs email** ([2_COMPTE_CLIENT_SPEC_UX §9](2_COMPTE_CLIENT_SPEC_UX.md)).

### 3.4 Conformité / légal *(rappel)*

- Finalités et mentions adaptées au traitement « demande pro » ; renvoi vers **`/privacy`** — implémentation page : [`ckr_privacy.xml`](../../views/pages/ckr_privacy.xml) ; autres pages légales existantes ([1_COMPTE_CLIENT_PARCOURS §7](1_COMPTE_CLIENT_PARCOURS.md)).

---

## 4. Arbitrages à trancher avant ou pendant le dev

Les lignes ci-dessous **bloquent** ou **orientent** l’implémentation ; cocher en réunion MOA / tech.

**Hypothèse MVP recommandée** *(non gelée — reste soumise à validation §4)* : page dédiée « Demande d’ouverture de compte pro » alimentant un objet standard Odoo (**`crm.lead`** via **`website_form`** si le module CRM est disponible et pertinent), **sans** création automatique de compte portail pro ni modification de pricelist.

| # | Sujet | Proposition initiale *(indicative)* | Décision figée (MOA / tech) |
|---|--------|--------------------------------------|----------------------------|
| 1 | **`auth_signup`** activé sur le site ? | À vérifier sur instance cible | |
| 2 | **Séparation A/B** | **Deux URLs** : signup standard B2C + **page dédiée** demande pro | |
| 3 | **Achat invité** | À **préserver** si activé sur l’instance | |
| 4 | **Demande pro** — chaîne technique | **`website_form` → `crm.lead`** si CRM disponible ; sinon alternative standard documentée | |
| 5 | **Champs** formulaire B (liste minimale) | Société, contact, email, téléphone, type d’activité, message *(à valider MOA)* | |
| 6 | **Email** | Confirmation **web** d’abord ; email auto au demandeur / copie CK **à arbitrer** | |
| 7 | **Validation métier** | Qui traite ; impact ultérieur sur pricelist / catégorie partenaire *(hors automatisation MVP si non validé)* | |
| 8 | **Email déjà existant** (doublon) | Comportement **non opaque** : message clair visiteur **ou** rattachement / traitement manuel côté Odoo selon solution retenue *(pas besoin de tout le dédoublonnage dans ce ticket)* | |
| 9 | **Tests Odoo** | Tag proposé `dorevia_ckr_account_mvp03` *(à valider)* | |

---

## 5. Contraintes techniques

- **Standard Odoo CE en priorité** : `website`, `portal`, `auth_signup`, `sale`, `contacts`, `crm` ou `website_form` selon arbitrage — pas de « double système de comptes » sans justification ([1_COMPTE_CLIENT_PARCOURS §2.1](1_COMPTE_CLIENT_PARCOURS.md)).
- **Pas** de boutique catalogue parallèle ; pas d’exposition prix B2B sur seule demande formulaire.
- **Pas** de création automatique d’**utilisateur portail** pour la seule demande pro (**§3.2**), sauf arbitrage explicite MOA / tech.
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
- [ ] La demande pro est **retrouvable** côté back-office Odoo avec un **libellé**, **tag**, **source** ou équivalent permettant de l’identifier comme demande **C-Kreyol MVP03**.
- [ ] Comportement en cas d’**email déjà existant** défini et **explicite** côté visiteur **ou** traitement documenté côté Odoo (arbitrage §4 — ligne *Email déjà existant*).

---

## 8. Recette

- **PV** : à produire après implémentation — **`PV_RECETTE_COMPTE_CLIENT_MVP03.md`** *(convention dossier `mvp_03`)*.
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
| 2026-05 | Amendements : statut « prêt pour arbitrage », exécutable si §4 complété ; hypothèse MVP ; pas d’utilisateur portail auto pour la demande pro ; §4 enrichi (propositions initiales, ligne doublon email) ; critères traçabilité BO + email dupliqué ; PV `PV_RECETTE_COMPTE_CLIENT_MVP03.md` ; lien `/privacy` clarifié. |
