# MVP 03 — Spec UX compte client

**Statut** : **spec UX / comportements d’interface** pour la vague MVP 03 ; complète [1_COMPTE_CLIENT_PARCOURS.md](1_COMPTE_CLIENT_PARCOURS.md) sans la remplacer. Les écrans exacts, routes et champs **techniques** restent à figer dans des **tickets d’exécution**.

**Pilotage dossier** : [README MVP 03](README.md).

**Engagement documentaire** : même principe que le document « parcours » — **aucun** écran, **aucun** libellé définitif et **aucun** workflow Odoo ne sont **gelés** par ce fichier seul sans validation MOA et ticket dev.

---

## 1. Objectif de ce document

Traduire le [cadrage parcours](1_COMPTE_CLIENT_PARCOURS.md) en **attentes UX** concrètes :

- hiérarchie de l’information sur les écrans **connexion / inscription / demande pro** ;
- **ton** et **messages** (confirmation, attente, erreur) ;
- **réduction de friction** parcours particulier vs **clarté** du parcours demande pro ;
- **cohérence** avec l’habillage existant (**login** CK, **portail**, **header**) et la charte C-Kreyol.

Ce document **ne prescrit pas** les modules Odoo activés ni la structure base ; il sert de **brief UX** pour maquettes, copies et recette interface.

---

## 2. Principes UX (alignés parcours)

1. **Deux intentions visibles** — le visiteur identifie sans ambiguïté **« compte particulier »** vs **« demande d’ouverture de compte pro »** (libellés MOA à figer — voir parcours §4.2).
2. **Pas de fausse promesse B2B** — aucun message ne suggère un **accès immédiat** aux tarifs ou conditions professionnels après une simple demande.
3. **Friction minimale B2C** — le parcours particulier reste **aussi court** que raisonnable ; pas de champs « entreprise » mélangés au formulaire grand public.
4. **Checkout protégé** — si l’**achat invité** est activé côté Odoo, l’UX MVP 03 **ne doit pas** le masquer ni ajouter d’étape obligatoire « créer un compte » avant paiement (sauf évolution MOA explicite).
5. **Charte CK** — typo, couleurs CTA, ton **calme et premium** : reprendre les réflexes du module ([login CK](../../views/auth/ckr_login.xml), `ckr_portal`, header).

---

## 3. Points d’entrée et navigation

| Zone | Comportement UX attendu |
|------|-------------------------|
| **Header** — « Connexion » / « Mon compte » | Accès **clair** au login ; une fois connecté, « Mon compte » mène au **portail** (`/my`) — implémentation [`ckr_header.xml`](../../views/layout/ckr_header.xml). |
| **Login** `/web/login` | Page déjà habillée CK ; prévoir **lien secondaire** vers **Créer un compte** (si signup activé) et, si retenu au ticket, entrée distincte **demande pro**. |
| **Signup** `/web/signup` *(si activé)* | Parcours **A** par défaut ; si une **entrée B** existe sur la même page, elle doit être **visuellement séparée** (bloc, onglet ou page dédiée — arbitrage §8 du parcours). |
| **Portail** `/my` | Liste commandes / adresses / données : **pas** de confusion avec une « zone pro » tant que le partenaire n’est pas validé B2B. |

Tant que le **profil professionnel** n’est pas validé côté Odoo, le portail **`/my`** ne doit **pas** afficher de zone, badge ou libellé laissant penser que le compte est déjà professionnel (voir aussi §6).

---

## 4. Parcours A — Compte particulier (B2C)

### 4.1 Structure d’écran (cible)

- **Titre** — identité CK cohérente avec [login](../../views/auth/ckr_login.xml) (« Mon compte » / équivalent validé MOA).
- **Formulaire** — champs **limités** au standard nécessaire (email, mot de passe, nom — selon config Odoo). Pas de bloc « société » dans ce parcours.
- **CTA primaire** — « Créer mon compte » / « S’inscrire » (validation MOA).
- **Lien discret** — « Déjà un compte ? Se connecter » vers `/web/login`.

### 4.2 Feedback

- **Succès** — redirection vers `/my` ou contexte **redirect** (checkout) ; message optionnel **non intrusif** si le standard Odoo le permet.
- **Erreur** — messages **explicites** (email déjà utilisé, mot de passe invalide) ; pas seulement une couleur rouge sans texte (**accessibilité**).

### 4.3 Checkout invité

- Si activé : le tunnel doit toujours proposer **Commander sans créer de compte** (libellé Odoo ou équivalent CK) **sans** le noyer sous les CTA « créer un compte ».

---

## 5. Parcours B — Demande d’ouverture de compte pro

### 5.1 Structure d’écran (cible)

- **Titre** — ex. « Demande d’ouverture de compte professionnel » — **à figer MOA** (éviter seul le terme « distributeur », trop étroit).
- **Introduction courte** — expliquer que la demande est **étudiée** ; **pas** d’accès tarifs pro immédiat ; délai **non garanti** si non validé métier.
- **Formulaire** — **minimum utile** : au minimum une façon de **joindre** le demandeur et d’**identifier** l’activité (champs exacts : ticket + MOA). Éviter les longs questionnaires dans une V1 UX.
- **CTA** — « Envoyer la demande » / équivalent sobre (pas un CTA « Accéder aux tarifs pro »).

### 5.2 Après envoi

- **Écran ou message de confirmation** — « Votre demande a bien été transmise. » + phrase sur le **traitement interne** sans promesse de délai irréaliste.
- **Pas de changement** des prix affichés sur la boutique pour ce visiteur tant que le **profil Odoo** n’est pas validé (cohérence parcours §6).

### 5.3 Ce que l’UX ne doit pas suggérer

- Qu’un **compte pro est déjà actif** après envoi du formulaire.
- Que les **prix affichés** vont basculer au prochain chargement de page sans action métier.

**Exemples de formulations à éviter** :

- « Accéder aux tarifs pro »
- « Activer mon compte pro »
- « Voir mes prix professionnels »
- « Créer mon compte distributeur »
- « Obtenir mes remises pro »

**Formulations à privilégier** :

- « Demande d’ouverture de compte professionnel »
- « Envoyer ma demande »
- « Demande soumise à validation »
- « Votre demande a bien été transmise »

---

## 6. États et messages (synthèse)

| Situation | Orientations UX |
|-----------|-------------------|
| Particulier connecté | Expérience **B2C** habituelle ; pas de badge « pro » sans validation réelle. |
| Demande pro envoyée, en attente | Message unique cohérent partout (portail ou email — arbitrage) : **demande en cours de traitement**. |
| Compte pro validé (métier) | Hors périmètre détail UX ici ; l’affichage tarifaire suit **Odoo** — pas de doublon doc dans cette spec sauf besoin MOA. |
| Erreur réseau / serveur | Message **calme**, invitation à réessayer ; pas de jargon technique. |

Tant que le profil professionnel n’est pas validé côté Odoo, le portail **`/my`** ne doit pas afficher de zone, badge ou libellé laissant penser que le compte est déjà professionnel — alignement [parcours](1_COMPTE_CLIENT_PARCOURS.md) (principe *compte pro demandé ≠ validé*).

---

## 7. Accessibilité

- **Labels** visibles ou équivalent **accessible** pour tous les champs ; les erreurs ne reposent **pas** uniquement sur la couleur.
- **Ordre de tabulation** logique ; focus visible sur champs et boutons (alignement avec les exigences déjà appliquées sur le module CK, ex. bloc newsletter).
- **Contrastes** : respect des couples texte / fond charte Phase 1.

---

## 8. Critères UX de recette (à cocher en fin de chantier)

- [ ] Distinction **claire** entre entrée **particulier** et **demande pro** (pas de libellés ambigus).
- [ ] Parcours **A** perçu comme **rapide** et **non administratif**.
- [ ] Parcours **B** **sans** promesse implicite de tarifs pro immédiats.
- [ ] **Checkout invité** toujours utilisable si activé en configuration.
- [ ] Messages **confirmation / erreur** compréhensibles ; **accessibilité** minimale respectée.
- [ ] Cohérence visuelle avec **login**, **portail** et **header** CK existants.

---

## 9. Arbitrages UX à trancher avec la MOA

| Sujet | Question |
|-------|----------|
| **Placement** | Demande pro : **page dédiée** vs **section** sur signup vs **modal**. La modal est déconseillée **par défaut** si elle ajoute de la charge cognitive ou **brouille la distinction A/B**. |
| **Copies** | Titres et sous-titres définitifs pour A et B ; ton « nous vous répondons sous X jours » **oui/non**. |
| **Email confirmation** | Envoi d’un **email automatique** au demandeur pro : oui/non ? **Copie interne** à l’équipe CK : oui/non ? *(Alignement message web / email, délai annoncé ou ton neutre — à trancher sans figer le workflow Odoo ici.)* |
| **Marque** | Logo / bandeau identique au login ou variante sobre pour la demande pro. |
| **Mobile** | Priorité **scroll** : formulaire B **sans** plier sous dix champs sur le premier écran si évitable. |

---

## 10. Références croisées

| Document | Rôle |
|----------|------|
| [1_COMPTE_CLIENT_PARCOURS.md](1_COMPTE_CLIENT_PARCOURS.md) | Parcours, états, doctrine, arbitrages métier / Odoo |
| [README MVP 03](README.md) | Intention dossier |
| [CHARTE_GRAPHIQUE_PHASE1.md](../direction/CHARTE_GRAPHIQUE_PHASE1.md) | Tokens couleur / typo |
| Login CK | `views/auth/ckr_login.xml` |
| Portail CK | `views/portal/ckr_portal.xml` |

---

## Historique

| Date | Événement |
|------|-----------|
| 2026-05 | Première version — spec UX suite au document parcours ; principes écrans, messages, recette UX, arbitrages MOA. |
| 2026-05 | Amendements : correction « distinction claire », réserve modal (distinction A/B), garde-fou portail `/my`, formulations interdites / à privilégier (parcours B), arbitrage email de confirmation. |
