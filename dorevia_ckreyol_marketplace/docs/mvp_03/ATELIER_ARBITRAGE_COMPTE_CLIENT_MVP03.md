# Atelier arbitrage — MVP 03 Compte client

**Objectif** : compléter le §4 du [`TICKET_COMPTE_CLIENT_MVP03.md`](TICKET_COMPTE_CLIENT_MVP03.md#4-arbitrages-à-trancher-avant-ou-pendant-le-dev) afin de rendre le ticket **réellement exécutable** côté dev.

**Durée cible** : 30 à 45 minutes  
**Participants souhaités** : MOA / produit + dev + référent Odoo fonctionnel  
**Sortie attendue** : tableau §4 complété + copies validées + prérequis dev confirmés

> Ne pas rouvrir l’ensemble du dossier MVP 03 : ne figer que les **décisions** qui débloquent l’implémentation.

---

## 1. Activation du signup

### Question

`auth_signup` est-il activé sur l’instance cible ?

### Décision à noter

- Oui
- Non
- À activer
- À vérifier

### Impact

Si `auth_signup` n’est pas activé, le parcours A « création de compte particulier » ne peut pas être traité comme un simple habillage du standard Odoo.

---

## 2. Séparation des parcours A / B

### Question

Comment distingue-t-on le compte particulier et la demande pro ?

### Options

1. `/web/signup` pour le compte particulier + page dédiée demande pro
2. Une seule page avec deux blocs clairement séparés
3. Autre approche documentée

### Recommandation MVP

Deux URLs :

- `/web/signup` : compte particulier standard
- page dédiée : demande d’ouverture de compte pro

### Décision à noter

```text
Décision :
Justification :
```

---

## 3. Achat invité

### Question

L’achat sans compte est-il activé et doit-il rester disponible ?

### Décision à noter

- Oui, à préserver
- Non, non applicable
- À vérifier sur instance cible

### Garde-fou

Le MVP 03 ne doit pas ajouter une obligation de création de compte avant paiement si l’achat invité est activé.

---

## 4. Chaîne technique demande pro

### Question

Comment la demande pro est-elle enregistrée côté Odoo ?

### Options

1. `website_form → crm.lead`
2. `website_form → res.partner` avec tag / source
3. Email métier simple
4. Contrôleur spécifique
5. Autre solution standard documentée

### Recommandation MVP

`website_form → crm.lead` si CRM est disponible et pertinent.

### Décision à noter

```text
Solution retenue :
Module Odoo requis :
Objet créé :
Tag / source :
Responsable de traitement :
```

---

## 5. Champs du formulaire pro

### Question

Quels champs sont strictement nécessaires pour qualifier la demande ?

### Proposition minimale

- Nom de l’entreprise / organisation
- Nom et prénom du contact
- Email
- Téléphone
- Type d’activité
- Message

### À arbitrer

- SIRET obligatoire ou optionnel ?
- Adresse obligatoire ou non ?
- Type d’activité en liste fermée ou champ libre ?

### Décision à noter

```text
Champs obligatoires :
Champs optionnels :
Champs exclus de la V1 :
```

---

## 6. Copies définitives

### À valider

#### Titre page demande pro

```text
Demande d’ouverture de compte professionnel
```

#### Texte d’introduction

```text
Vous représentez une entreprise, une boutique, un restaurant, une collectivité ou une organisation ?
Vous pouvez nous transmettre une demande d’ouverture de compte professionnel.
L’accès aux conditions professionnelles est soumis à validation par l’équipe C-Kreyol.
```

#### CTA

```text
Envoyer ma demande
```

#### Confirmation web

```text
Votre demande a bien été transmise.
L’équipe C-Kreyol reviendra vers vous après vérification de votre demande.
```

### Décision à noter

```text
Titre validé :
Intro validée :
CTA validé :
Confirmation validée :
```

---

## 7. Email / notification

### Question

Que se passe-t-il après envoi de la demande ?

### Points à trancher

- Confirmation web uniquement ?
- Email automatique au demandeur ?
- Notification interne CK ?
- Copie email à une adresse métier ?
- Création d’activité Odoo ?

### Décision à noter

```text
Confirmation web :
Email demandeur :
Notification interne :
Adresse / responsable :
```

---

## 8. Email déjà existant

### Question

Que se passe-t-il si l’email saisi existe déjà ?

### Options

1. Message clair côté visiteur
2. Demande enregistrée quand même pour traitement manuel
3. Rattachement à un contact existant
4. Blocage avec invitation à se connecter

### Garde-fou

Pas d’échec silencieux. Pas de message technique opaque.

### Décision à noter

```text
Comportement retenu :
Message visiteur :
Traitement back-office :
```

---

## 9. Traçabilité back-office

### Question

Comment l’équipe retrouve-t-elle les demandes MVP03 ?

### Options

- Tag `C-Kreyol MVP03`
- Source `Demande compte pro`
- Campagne `MVP03 Compte pro`
- Équipe commerciale dédiée
- Étape CRM dédiée

### Décision à noter

```text
Tag / source :
Équipe :
Étape :
Responsable :
```

---

## 10. Tests

### Question

Quel tag de test Odoo est retenu ?

### Proposition

```text
dorevia_ckr_account_mvp03
```

### Décision à noter

```text
Tag de test :
Tests obligatoires :
Tests manuels complémentaires :
```

---

## Décision de fin d’atelier

À la fin de l’atelier, choisir un statut :

```text
[ ] GO dev
[ ] GO dev avec réserve
[ ] NO GO — arbitrages incomplets
```

### Conditions minimales pour GO dev

- `auth_signup` clarifié ;
- séparation A/B décidée ;
- achat invité clarifié ;
- chaîne demande pro décidée ;
- champs formulaire B figés ;
- copies principales validées ;
- comportement email existant défini ;
- traçabilité back-office définie.

---

## Références

| Document | Lien |
|----------|------|
| Ticket §4 | [TICKET_COMPTE_CLIENT_MVP03.md §4](TICKET_COMPTE_CLIENT_MVP03.md#4-arbitrages-à-trancher-avant-ou-pendant-le-dev) |
| PV — §1.1 arbitrages testés | [PV_RECETTE_COMPTE_CLIENT_MVP03.md](PV_RECETTE_COMPTE_CLIENT_MVP03.md) |

---

## Historique

| Date | Événement |
|------|-----------|
| 2026-05-05 | Création du support d’atelier pour compléter le §4 ticket MVP03. |
