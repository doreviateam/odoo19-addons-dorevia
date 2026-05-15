# Recommandation atelier — MVP 03 Compte client

**Statut** : **pré-arbitrage MOA / tech** — orientations pour préparer l’[atelier §4](ATELIER_ARBITRAGE_COMPTE_CLIENT_MVP03.md) ; **non contractuel** jusqu’à validation en séance et **report dans le [ticket §4](TICKET_COMPTE_CLIENT_MVP03.md#4-arbitrages-à-trancher-avant-ou-pendant-le-dev)**.

**Sources** : alignement [1_COMPTE_CLIENT_PARCOURS.md](1_COMPTE_CLIENT_PARCOURS.md), [2_COMPTE_CLIENT_SPEC_UX.md](2_COMPTE_CLIENT_SPEC_UX.md), [TICKET_COMPTE_CLIENT_MVP03.md](TICKET_COMPTE_CLIENT_MVP03.md).

---

## Objectif

Compléter le §4 du ticket [`TICKET_COMPTE_CLIENT_MVP03.md`](TICKET_COMPTE_CLIENT_MVP03.md) afin de rendre le ticket **exécutable** côté dev.

L’atelier ne doit **pas** rouvrir la doctrine MVP 03. Il doit uniquement figer les décisions nécessaires pour une **première implémentation prudente**.

---

## Décision recommandée globale

Partir sur une **séparation nette** des comportements :

- **B2C / particulier** : création automatique du **compte client standard** via le mécanisme Odoo natif, si `auth_signup` est activé et correctement configuré ;
- **B2B / professionnel** : demande d’ouverture de compte pro captée comme **demande commerciale**, idéalement via **`website_form → crm.lead`** si CRM est disponible.

Logique cible :

```text
Particulier → création compte client standard / portail Odoo
Professionnel → demande commerciale à qualifier / CRM lead
```

---

## Doctrine opérationnelle recommandée

> On automatise ce qui est sans risque commercial : le compte particulier.  
> On met en attente ce qui engage les conditions commerciales : le compte professionnel.

| Parcours | Action automatique **autorisée** | Action automatique **interdite** |
|----------|----------------------------------|-------------------------------------|
| **B2C / particulier** | Création compte client standard via `auth_signup` / portail | Qualification pro, pricelist B2B, champs entreprise obligatoires sur le signup |
| **B2B / demande pro** | Création d’un **lead CRM** / demande à qualifier | Compte portail pro automatique, pricelist B2B, statut pro « validé » |

---

## 1. `auth_signup`

### Question

`auth_signup` est-il activé sur l’instance cible ?

### Réponse recommandée

À vérifier sur l’instance cible.

Si `auth_signup` est déjà activé proprement, le **conserver** pour le parcours particulier.

S’il n’est pas activé, l’**activer** uniquement si cela reste compatible avec Odoo CE, le portail client et le tunnel d’achat.

### Décision proposée

```text
Décision : À vérifier sur instance cible ; utiliser auth_signup pour créer automatiquement le compte particulier si activé / activable proprement.
Justification : rester au plus près du standard Odoo CE et éviter un système de comptes parallèle.
```

---

## 2. Séparation A / B

### Question

Comment distingue-t-on le compte particulier et la demande pro ?

### Réponse recommandée

Deux chemins distincts :

- **`/web/signup`** pour le compte particulier ;
- **page dédiée** pour la demande d’ouverture de compte professionnel.

### Décision proposée

```text
Décision : Deux URLs distinctes.
- Parcours A : /web/signup
- Parcours B : page dédiée demande pro

Justification : éviter la confusion entre inscription particulier et demande pro ; garder le signup standard Odoo lisible.
```

### URL indicative pour la page dédiée

Préférer **`/demande-compte-professionnel`** (plus explicite qu’un simple `/compte-professionnel`, qui peut suggérer une création immédiate de compte pro).

---

## 3. Achat invité

### Question

L’achat sans compte est-il activé et doit-il rester disponible ?

### Réponse recommandée

**Oui, à préserver** si activé dans la configuration Odoo. Le MVP 03 ne doit pas forcer la création de compte avant paiement.

### Décision proposée

```text
Décision : Préserver l’achat invité si activé sur l’instance cible.
Justification : ne pas augmenter la friction B2C ni dégrader le tunnel d’achat.
```

---

## 4. Parcours A — compte particulier B2C

### Question

La création de compte particulier doit-elle être automatique ?

### Réponse recommandée

**Oui**, si `auth_signup` est activé / activable proprement — cohérent avec l’e-commerce Odoo standard.

### Décision proposée

```text
Décision : Le parcours B2C crée automatiquement un compte client standard via le mécanisme Odoo natif.
Route cible : /web/signup
Type de compte : compte client / portail standard.
```

### Conditions

- standard Odoo ;
- pas de champs entreprise obligatoires sur ce parcours ;
- pas de modification automatique arbitraire de pricelist ;
- pas de statut « pro validé » ;
- ne pas dégrader le checkout invité si activé.

### Garde-fou

La création automatique concerne **uniquement** le compte **particulier / standard**. Elle ne vaut **pas** validation professionnelle.

---

## 5. Parcours B — demande compte professionnel

### Question

La demande pro doit-elle créer un compte automatiquement ?

### Réponse recommandée

**Non.** La demande pro reste une **demande commerciale** à qualifier, idéalement **`crm.lead`**.

### Décision proposée

```text
Décision : Le parcours B2B ne crée pas automatiquement de compte portail pro.
Route cible indicative : /demande-compte-professionnel
Objet cible recommandé : crm.lead
Chaîne recommandée : website_form → crm.lead
```

### Conditions

- pas d’utilisateur portail pro automatique ;
- pas de bascule automatique de pricelist ;
- pas de catégorie partenaire B2B automatique ;
- demande identifiable côté CRM ;
- traitement manuel ultérieur par l’équipe CK.

---

## 6. Chaîne technique demande pro

### Question

Comment la demande pro est-elle enregistrée côté Odoo ?

### Réponse recommandée

**`website_form → crm.lead`** si CRM est disponible et pertinent.

### Décision proposée

```text
Solution retenue : website_form → crm.lead si CRM disponible.
Modules : website_form + crm si présents sur l’instance.
Objet créé : crm.lead.
Tag / source indicative : Demande compte pro C-Kreyol MVP03.
Responsable de traitement : à définir côté exploitation CK / commercial.
```

### Variante si CRM non disponible

```text
Alternative : website_form vers email métier ou autre objet standard documenté.
Condition : demande traçable et retrouvable en back-office.
```

---

## 7. Champs du formulaire pro

### Question

Quels champs sont strictement nécessaires pour qualifier la demande ?

### Option sobre

Obligatoires : entreprise / organisation, contact, email, type d’activité, message — optionnels : téléphone, SIRET, adresse.

### Option commerciale recommandée

**Obligatoires** : entreprise / organisation, nom et prénom du contact, email, **téléphone**, type d’activité, message.

**Optionnels** : SIRET, adresse.

### Décision proposée

```text
Décision : retenir l’option commerciale recommandée.
Champs obligatoires : entreprise, contact, email, téléphone, type d’activité, message.
Champs optionnels : SIRET, adresse.
Exclus V1 : volume d’achat estimé, pièces jointes lourdes, infos bancaires, conditions commerciales négociées dans le formulaire.
Justification : qualification suffisante sans formulaire lourd.
```

---

## 8. Type d’activité

### Question

Type d’activité **libre** ou **liste** ?

### Réponse recommandée

**Liste fermée** + option **« Autre »**.

### Valeurs recommandées

```text
- Boutique / épicerie fine
- Restaurant / traiteur
- Distributeur
- Collectivité / comité d’entreprise
- Association / organisation
- Autre
```

### Décision proposée

```text
Décision : liste fermée avec option « Autre ».
Justification : qualification BO sans bloquer les cas imprévus.
```

---

## 9. Copies définitives

Les textes suivants sont **proposés** pour validation MOA (alignés [atelier §6](ATELIER_ARBITRAGE_COMPTE_CLIENT_MVP03.md)).

**Titre** : Demande d’ouverture de compte professionnel  

**Introduction** :  
Vous représentez une entreprise, une boutique, un restaurant, une collectivité ou une organisation ?  
Vous pouvez nous transmettre une demande d’ouverture de compte professionnel.  
L’accès aux conditions professionnelles est soumis à validation par l’équipe C-Kreyol.

**CTA** : Envoyer ma demande  

**Confirmation web** :  
Votre demande a bien été transmise.  
L’équipe C-Kreyol reviendra vers vous après vérification de votre demande.

### Point de prudence

Ne pas annoncer de délai du type « réponse sous 48 h » tant que l’organisation métier n’est pas prête à le tenir.

### Décision proposée

```text
Titre / intro / CTA / confirmation : valider tel quel sauf retour MOA.
```

---

## 10. Email / notification

### Réponse recommandée

**Minimum** : confirmation **web** obligatoire.

**Recommandé** si simple : **notification interne** CK. Email automatique au demandeur : **utile**, pas indispensable en V1 si cela complexifie.

### Décision proposée

```text
Confirmation web : obligatoire.
Email demandeur : optionnel V1 ; activer si standard Odoo simple.
Notification interne : recommandée.
Adresse / responsable : à définir côté CK.
```

### Priorité opérationnelle

1. confirmation web ;  
2. lead traçable ;  
3. notification interne ;  
4. email automatique demandeur si simple.

---

## 11. Email déjà existant

### Réponse recommandée

Ne pas **bloquer brutalement** la demande pro. Si possible : enregistrer la demande comme lead, signaler en BO qu’un contact existe déjà, message **clair** au visiteur.

### Message recommandé

```text
Votre demande a bien été transmise.
Si un compte existe déjà avec cette adresse, l’équipe C-Kreyol pourra le rattacher à votre demande après vérification.
```

### Décision proposée

```text
Comportement : pas d’échec silencieux ; enregistrer la demande ou message clair selon contrainte technique.
Message visiteur : clair, non technique.
Traitement BO : rattachement manuel ou vérification contact existant.
```

### Garde-fou

Pas de message brut type « email already exists » ; pas de blocage sans explication.

---

## 12. Traçabilité back-office

### Réponse recommandée

**Source / tag explicite**, par ex. **`Demande compte pro C-Kreyol MVP03`**.

### Décision proposée

```text
Tag / source : Demande compte pro C-Kreyol MVP03
Équipe : à définir côté CK
Étape indicative : Nouveau / À qualifier
Responsable : à définir côté exploitation
```

### Si `crm.lead`

Indications : nom de lead du type « Demande compte pro — [Entreprise] », source « Site C-Kreyol », tag comme ci-dessus.

---

## 13. Compte portail pro

### Réponse recommandée

**Aucune** création automatique d’utilisateur portail « pro » sur la seule demande formulaire.

```text
Décision : aucune création automatique d’utilisateur portail pro.
Justification : une demande commerciale n’est pas une validation de compte professionnel.
```

---

## 14. Pricelist / tarifs B2B

### Réponse recommandée

**Aucune** bascule automatique de pricelist ni changement des prix affichés après soumission du formulaire seul.

```text
Décision : aucune bascule automatique de pricelist après soumission.
Justification : accès conditions B2B = validation métier ultérieure dans Odoo.
```

---

## 15. Tests Odoo

### Proposition

```text
dorevia_ckr_account_mvp03
```

### Tests obligatoires recommandés

- accès signup particulier si `auth_signup` activé ;  
- création compte client standard B2C ;  
- absence de champs entreprise obligatoires sur B2C ;  
- affichage page demande pro ;  
- soumission formulaire demande pro ;  
- confirmation web ;  
- création lead CRM ou trace BO équivalente ;  
- pas de portail pro automatique ;  
- pas de bascule pricelist ;  
- demande retrouvable en BO ;  
- checkout invité non cassé si activé.

### Décision proposée

```text
Tag : dorevia_ckr_account_mvp03
Tests auto : non-régression B2C, demande pro, invité, absence activation B2B.
Complément manuel : mobile, accessibilité, doublon email.
```

---

## 16. Décision finale recommandée

### Statut cible proposé

```text
[ ] GO dev
[x] GO dev avec réserve
[ ] NO GO — arbitrages incomplets
```

### Pourquoi « GO dev avec réserve » ?

Hypothèse claire, mais **à confirmer sur l’instance** : `auth_signup`, CRM, `website_form → crm.lead`, achat invité, contacts internes CK.

### Réserve proposée

```text
GO dev avec réserve technique : confirmer sur l’instance cible auth_signup, CRM, website_form et achat invité avant gel de l’implémentation finale.
```

---

## 17. Tableau §4 pré-rempli recommandé *(aligné ticket)*

**Reporté dans** la colonne « Décision figée » du [ticket §4](TICKET_COMPTE_CLIENT_MVP03.md#4-arbitrages-à-trancher-avant-ou-pendant-le-dev) *(2026-05-05 — décision recommandée ; ajustements possibles après atelier MOA)*.

| # | Sujet | Décision figée recommandée *(à valider)* |
|---|--------|-------------------------------------------|
| 1 | **`auth_signup`** | À vérifier sur instance ; utiliser `auth_signup` pour création auto du **compte particulier** si activé / activable proprement (parcours A = standard Odoo, sans champs entreprise obligatoires ni statut pro). |
| 2 | **Séparation A/B** | **Deux URLs** : `/web/signup` (B2C) + **`/demande-compte-professionnel`** (demande pro). |
| 3 | **Achat invité** | **Préserver** si activé ; ne pas forcer la création de compte avant paiement. |
| 4 | **Demande pro — chaîne technique** | **`website_form` → `crm.lead`** si CRM disponible ; sinon alternative standard documentée ; **pas** de portail pro auto ni pricelist auto ; lead identifiable (tag / source type **Demande compte pro C-Kreyol MVP03**). |
| 5 | **Champs formulaire B** | **Obligatoires** : entreprise, contact, email, téléphone, type d’activité (liste + Autre), message. **Optionnels** : SIRET, adresse. |
| 6 | **Email / notification** | Confirmation **web obligatoire** ; **notification interne** recommandée ; email demandeur **optionnel** V1 si mise en œuvre simple. |
| 7 | **Validation métier** | Traitement **manuel** ultérieur ; **aucune** pricelist / catégorie B2B automatique dans le périmètre MVP 03 décrit. |
| 8 | **Email déjà existant** | Pas d’échec silencieux ; message clair et/ou lead + rapprochement BO ; voir §11 ci-dessus. |
| 9 | **Tests Odoo** | Tag **`dorevia_ckr_account_mvp03`** ; tests §15. |

---

## 18. Phrase de conduite atelier

> On ne cherche pas à concevoir tout le B2B CK ; on veut seulement capter proprement une demande pro, sans casser le parcours particulier ni sortir du standard Odoo CE.

---

## 19. Résumé final

```text
B2C : création automatique du compte client standard via Odoo, si auth_signup est activé / activable.
B2B : capture d’une demande professionnelle via lead CRM, sans activation automatique des droits pro.
```

Cette approche reste fluide pour les particuliers, prudente pour les pros, conforme au standard Odoo CE et à la doctrine CK B2C/B2B, exploitable en back-office.

---

## Références croisées

| Document | Usage |
|----------|--------|
| [ATELIER_ARBITRAGE_COMPTE_CLIENT_MVP03.md](ATELIER_ARBITRAGE_COMPTE_CLIENT_MVP03.md) | Déroulé de réunion et cases à cocher |
| [TICKET_COMPTE_CLIENT_MVP03.md](TICKET_COMPTE_CLIENT_MVP03.md) | Tableau §4 officiel à remplir |
| [PV_RECETTE_COMPTE_CLIENT_MVP03.md](PV_RECETTE_COMPTE_CLIENT_MVP03.md) | §1.1 arbitrages testés après décisions |

---

## Historique

| Date | Événement |
|------|-----------|
| 2026-05-05 | Création — doctrine opérationnelle, pré-arbitrages, tableau §4 aligné ticket, lien avec atelier et tests. |
| 2026-05-05 | Tableau §17 **reporté** dans [TICKET_COMPTE_CLIENT_MVP03.md §4](TICKET_COMPTE_CLIENT_MVP03.md#4-arbitrages-à-trancher-avant-ou-pendant-le-dev) — colonne « Décision figée » complétée. |
