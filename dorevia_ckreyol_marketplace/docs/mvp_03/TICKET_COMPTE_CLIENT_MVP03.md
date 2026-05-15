# TICKET — Compte client MVP 03 (B2C / demande pro)

**ID** : `COMPTE-CLIENT-MVP03`  
**Date d’ouverture** : 2026-05  
**Priorité** : **P2** *(à confirmer pilotage)*  
**Statut** : **§4 renseigné** — décisions alignées sur [RECOMMANDATION_ATELIER_COMPTE_CLIENT_MVP03.md](RECOMMANDATION_ATELIER_COMPTE_CLIENT_MVP03.md) ; **GO dev avec réserve réduite** *(voir [§ Complément technique — chaîne demande pro vers CRM](#complément-technique--chaîne-demande-pro-vers-crm) : installer `crm` + `website_crm` sur `tenant_o7`, configurer formulaire ; parcours B2C déjà aligné sur l’instance)* — validation MOA / pickup équipe si nécessaire.  
**GO documentaire** : **2026-05-05** — validation du périmètre et des garde-fous du présent ticket *(voir aussi statut ci-dessus pour §4)*.  
**Module** : `dorevia_ckreyol_marketplace` (+ configuration Odoo site / CRM selon arbitrage).

**Sources de vérité produit / UX** :

| Document | Rôle |
|----------|------|
| [README MVP 03](README.md) | Intention dossier, doctrine, hors périmètre |
| [1_COMPTE_CLIENT_PARCOURS.md](1_COMPTE_CLIENT_PARCOURS.md) | Parcours A/B, états, points d’entrée, arbitrages métier |
| [2_COMPTE_CLIENT_SPEC_UX.md](2_COMPTE_CLIENT_SPEC_UX.md) | Spec UX, wording interdit/privilégié, garde-fou `/my`, recette interface |

Le **§4 est complété** avec les décisions recommandées ; le ticket sert de **brief exécutable** pour le dev (**réserve réduite** : installation / config **`crm` + `website_crm`** et formulaire sur **`tenant_o7`** — voir [complément technique](#complément-technique--chaîne-demande-pro-vers-crm) ; pilotage équipe). Les arbitrages formalisés en atelier MOA peuvent **ajuster** les lignes ci-dessous.

**Doctrine** : [DOCTRINE_CK_ECOMMERCE_B2C_B2B.md](../direction/DOCTRINE_CK_ECOMMERCE_B2C_B2B.md) ; [ADR-CKR-001](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-001) (standard d’abord) ; [ADR-CKR-009](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-009) (sanctuarisation tunnel) ; [ADR-CKR-010](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-010) (B2C/B2B).

### Pickup dev *(réserve réduite)*

Ticket **prêt pour pickup** ; détail dans les sections suivantes et [Complément technique](#complément-technique--chaîne-demande-pro-vers-crm).

**Vérifié sur `tenant_o7`**

- **`auth_signup`** installé ;
- **`/web/signup`** OK ;
- **achat invité** aligné (`account_on_checkout` = optional).

**Décision technique — demande pro**

- installer **`crm`** ;
- installer / confirmer **`website_crm`** ;
- créer **`/demande-compte-professionnel`** ;
- formulaire Website avec action **Create an Opportunity** ;
- identifier les demandes comme **`Demande compte pro C-Kreyol MVP03`**.

**Garde-fous**

- pas de portail pro automatique ;
- pas de pricelist B2B automatique ;
- pas de statut pro validé automatiquement.

**Branche proposée** : **`feat/mvp03-compte-client`**.

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

Les lignes ci-dessous **bloquent** ou **orientent** l’implémentation. La colonne **Décision figée** reprend la **décision recommandée** du document [RECOMMANDATION_ATELIER_COMPTE_CLIENT_MVP03.md](RECOMMANDATION_ATELIER_COMPTE_CLIENT_MVP03.md) *(sections **17** tableau §4 et **16** GO avec réserve)* — **GO dev avec réserve réduite** : sur **`tenant_o7`**, **`auth_signup`** et **achat invité** sont déjà alignés ; il reste à **installer `crm` + `website_crm`** et à **configurer le formulaire** (voir [Complément technique](#complément-technique--chaîne-demande-pro-vers-crm)).

**Support d’atelier** : [ATELIER_ARBITRAGE_COMPTE_CLIENT_MVP03.md](ATELIER_ARBITRAGE_COMPTE_CLIENT_MVP03.md) — checklist structurée (durée cible 30–45 min, sorties attendues).

**Doctrine et détail** : [RECOMMANDATION_ATELIER_COMPTE_CLIENT_MVP03.md](RECOMMANDATION_ATELIER_COMPTE_CLIENT_MVP03.md) — B2C/B2B, champs, copies, doublon email, traçabilité BO.

**Hypothèse MVP** *(alignée §4 + complément technique)* : page dédiée « Demande d’ouverture de compte pro » (**`/demande-compte-professionnel`**) avec formulaire Website (**action** *Create an Opportunity*) → **`crm.lead`** via **`website_crm`** une fois **`crm`** installé, **sans** création automatique de compte portail pro ni modification de pricelist.

| # | Sujet | Proposition initiale *(indicative)* | Décision figée (MOA / tech) |
|---|--------|--------------------------------------|----------------------------|
| 1 | **`auth_signup`** activé sur le site ? | À vérifier sur instance cible | À vérifier sur instance ; utiliser **`auth_signup`** pour création auto du **compte particulier** si activé / activable proprement (parcours A = standard Odoo, sans champs entreprise obligatoires ni statut pro). |
| 2 | **Séparation A/B** | **Deux URLs** : signup standard B2C + **page dédiée** demande pro | **Deux URLs** : **`/web/signup`** (B2C) + **`/demande-compte-professionnel`** (demande pro). |
| 3 | **Achat invité** | À **préserver** si activé sur l’instance | **Préserver** si activé ; ne pas forcer la création de compte avant paiement. |
| 4 | **Demande pro** — chaîne technique | Formulaire Website → **`crm.lead`** via **`website_crm`** si **`crm`** installé ; sinon alternative standard documentée | **Décision figée** : **`website` + `crm` + `website_crm`** — page **`/demande-compte-professionnel`**, snippet formulaire, action **Create an Opportunity** ; **pas** de portail pro auto ni pricelist auto ; lead identifiable (tag / source type **Demande compte pro C-Kreyol MVP03**). Détail : [Complément technique](#complément-technique--chaîne-demande-pro-vers-crm). |
| 5 | **Champs** formulaire B (liste minimale) | Société, contact, email, téléphone, type d’activité, message *(à valider MOA)* | **Obligatoires** : entreprise, contact, email, téléphone, type d’activité (**liste + Autre**), message. **Optionnels** : SIRET, adresse. |
| 6 | **Email / notification** | Confirmation **web obligatoire** ; email auto au demandeur et/ou notification interne CK **à arbitrer** | Confirmation **web obligatoire** ; **notification interne** recommandée ; email demandeur **optionnel** V1 si mise en œuvre simple. |
| 7 | **Validation métier** | Qui traite ; impact ultérieur sur pricelist / catégorie partenaire *(hors automatisation MVP si non validé)* | Traitement **manuel** ultérieur ; **aucune** pricelist / catégorie B2B automatique dans le périmètre MVP 03 décrit. |
| 8 | **Email déjà existant** (doublon) | Comportement **non opaque** : message clair visiteur **ou** rattachement / traitement manuel côté Odoo selon solution retenue *(pas besoin de tout le dédoublonnage dans ce ticket)* | Pas d’échec silencieux ; message clair et/ou lead + rapprochement BO — détail : [RECOMMANDATION_ATELIER_COMPTE_CLIENT_MVP03.md](RECOMMANDATION_ATELIER_COMPTE_CLIENT_MVP03.md) §11. |
| 9 | **Tests Odoo** | Tag proposé `dorevia_ckr_account_mvp03` *(à valider)* | Tag **`dorevia_ckr_account_mvp03`** ; périmètre : [RECOMMANDATION_ATELIER_COMPTE_CLIENT_MVP03.md](RECOMMANDATION_ATELIER_COMPTE_CLIENT_MVP03.md) §15. |

### Vérification instance cible — base **`tenant_o7`** (2026-05-05)

Contrôle technique sur environnement local **`http://localhost:18079/`** (sélection base **`?db=tenant_o7`**). Aucun identifiant consigné dans ce document.

| Contrôle | Résultat |
|----------|----------|
| **`auth_signup`** | **installé** |
| **Site web** (id 1) — nom | **C-KREYOLE** |
| **`auth_signup_uninvited`** | **`b2c`** |
| **`account_on_checkout`** | **`optional`** (pas d’obligation de compte avant paiement, aligné ticket) |
| **`/web/signup`** | Page signup **OK** (formulaire présent après entrée session avec `db=tenant_o7`) |
| **`crm`** | **non installé** — **à installer** sur **`tenant_o7`** pour la chaîne formulaire → **`crm.lead`** |
| **`website_crm`** | **non installé** — **à installer** après **`crm`** *(souvent via **auto_install**)* |
| Formulaires site (**pas** de module séparé **`website_form`**) | **Attendu en Odoo 19 CE** : snippets formulaire portés par **`website`** ; pont CRM = **`website_crm`** — voir [Complément technique](#complément-technique--chaîne-demande-pro-vers-crm) |

**Suite** : décision technique **figée** — [Complément technique — chaîne demande pro vers CRM](#complément-technique--chaîne-demande-pro-vers-crm) ; compléter la checklist **§9** point 4 après installation / config sur **`tenant_o7`**.

---

## Complément technique — chaîne demande pro vers CRM

La solution standard retenue pour le **parcours B** est :

```text
Page dédiée /demande-compte-professionnel
→ bloc formulaire Website (snippet)
→ action Create an Opportunity
→ crm.lead via website_crm
```

### Modules / configuration

- **`crm`** doit être **installé** sur **`tenant_o7`**.
- **`website_crm`** (Apps : *Contact Form*) est le **pont standard** entre formulaire Website et CRM ; il **dépend** de **`website`** et **`crm`** uniquement — **pas** de module séparé **`website_form`** à prévoir : en Odoo **19**, le formulaire est porté par **`website`** (blocs / snippets).
- **`website_crm`** peut s’**auto-installer** une fois **`website`** + **`crm`** disponibles ; sinon l’**installer explicitement** depuis Applications.

### Réglage CRM

Dans **CRM → Configuration → Settings → Leads** :

- si l’option **Leads** est activée : les envois peuvent être créés comme **leads** ;
- sinon : **opportunités** — dans les deux cas l’objet **`crm.lead`** reste exploitable côté CRM.

### Réglage formulaire Website

Sur la page **`/demande-compte-professionnel`** : bloc formulaire Website (snippet), puis :

```text
Action : Create an Opportunity
```

(cf. [documentation Odoo 19 — opportunities from web forms](https://www.odoo.com/documentation/19.0/applications/sales/crm/acquire_leads/opportunities_form.html))

### Garde-fous

- Ne pas créer automatiquement d’**utilisateur portail pro**.
- Ne pas modifier automatiquement la **pricelist**.
- Ne pas attribuer automatiquement une **catégorie partenaire B2B**.
- Garder la demande comme **objet CRM à qualifier**.
- **Identifier** la demande comme **Demande compte pro C-Kreyol MVP03** (voir ci-dessous).

### Traçabilité recommandée

À choisir en implémentation **minimale** :

- équipe commerciale **dédiée** ;
- préfixe dans le **sujet** : `Demande compte pro — [Entreprise]` ;
- **source / campagne / UTM** si déjà utilisés ;
- **tag CRM** si disponible sans spécifique lourd ;
- sinon **petite extension CK** pour valeur par défaut (tag, champ, etc.).

### Décision technique

```text
Décision : installer crm, utiliser website_crm, créer la page /demande-compte-professionnel
avec un formulaire Website configuré en Create an Opportunity.

Pas de module website_form séparé à prévoir — les formulaires sont portés par website.
```

---

## 5. Contraintes techniques

- **Standard Odoo CE en priorité** : `website`, `portal`, `auth_signup`, `sale`, `contacts`, **`crm`**, **`website_crm`** (formulaire → lead — voir complément technique ci-dessus) — pas de « double système de comptes » sans justification ([1_COMPTE_CLIENT_PARCOURS §2.1](1_COMPTE_CLIENT_PARCOURS.md)).
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

- **PV** : **[PV_RECETTE_COMPTE_CLIENT_MVP03.md](PV_RECETTE_COMPTE_CLIENT_MVP03.md)** — brouillon de préparation recette ; à compléter après livraison (verdict, date, instance).
- Jeux manuels : parcours A, parcours B, invité, erreurs formulaire, **petit écran**.

---

## 9. Prêt pour dev — checklist

1. [ ] **GO MOA** sur copies définitives (titres, CTA, message confirmation B) — propositions dans [RECOMMANDATION_ATELIER_COMPTE_CLIENT_MVP03.md](RECOMMANDATION_ATELIER_COMPTE_CLIENT_MVP03.md) §9 sauf ajustement atelier.
2. [x] **Arbitrages §4** complétés — colonne « Décision figée » renseignée ([RECOMMANDATION_ATELIER_COMPTE_CLIENT_MVP03.md](RECOMMANDATION_ATELIER_COMPTE_CLIENT_MVP03.md) §17) ; chaîne CRM **décisionnelle** : [Complément technique](#complément-technique--chaîne-demande-pro-vers-crm).
3. [ ] **Branche** et responsable dev assignés — **branche proposée** : **`feat/mvp03-compte-client`**.
4. [ ] **Base de test** **`tenant_o7`** :
   - [x] **`auth_signup`** aligné ;
   - [x] **achat invité** aligné (`account_on_checkout` = optional) ;
   - [ ] **`crm`** à installer sur **`tenant_o7`** ;
   - [ ] **`website_crm`** à installer / confirmer après installation CRM *(auto_install possible)* ;
   - [ ] **formulaire** page **`/demande-compte-professionnel`** configuré en **Create an Opportunity**.

---

## Historique

| Date | Événement |
|------|-----------|
| 2026-05 | Création du ticket d’exécution MVP 03 à partir des docs parcours, spec UX et structure tickets module. |
| 2026-05 | Amendements : statut « prêt pour arbitrage », exécutable si §4 complété ; hypothèse MVP ; pas d’utilisateur portail auto pour la demande pro ; §4 enrichi (propositions initiales, ligne doublon email) ; critères traçabilité BO + email dupliqué ; PV `PV_RECETTE_COMPTE_CLIENT_MVP03.md` ; lien `/privacy` clarifié. |
| 2026-05 | §4 ligne *Email / notification* : confirmation web = minimum obligatoire ; emails auto / internes à arbitrer ; lien vers PV recette brouillon. |
| 2026-05-05 | **GO documentaire** — tampon date ; validation du document pour arbitrage §4 puis exécution ([PV recette brouillon](PV_RECETTE_COMPTE_CLIENT_MVP03.md)). |
| 2026-05-05 | Lien vers support d’atelier [ATELIER_ARBITRAGE_COMPTE_CLIENT_MVP03.md](ATELIER_ARBITRAGE_COMPTE_CLIENT_MVP03.md) pour compléter le §4 en réunion MOA / tech. |
| 2026-05-05 | Référence [RECOMMANDATION_ATELIER_COMPTE_CLIENT_MVP03.md](RECOMMANDATION_ATELIER_COMPTE_CLIENT_MVP03.md) — pré-arbitrages et tableau §4 pré-rempli recommandé. |
| 2026-05-05 | **§4 complété** : colonne « Décision figée » alignée sur [RECOMMANDATION_ATELIER_COMPTE_CLIENT_MVP03.md](RECOMMANDATION_ATELIER_COMPTE_CLIENT_MVP03.md) §17 ; statut **GO dev avec réserve instance**. |
| 2026-05-05 | **Vérification instance** : base **`tenant_o7`** sur `localhost:18079` — tableau sous §4 ; réserve **CRM non installé** ; pas de secrets dans le doc. |
| 2026-05-05 | **Complément technique** : chaîne standard **`website` + `crm` + `website_crm`** ; pas de module `website_form` séparé ; checklist §9 point 4 détaillée ; statut **GO dev avec réserve réduite**. |
| 2026-05-05 | **Pickup dev** : synthèse **`tenant_o7`** + décision technique + garde-fous ; section *Pickup dev* ; branche proposée **`feat/mvp03-compte-client`**. |
