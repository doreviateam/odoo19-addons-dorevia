# MVP 03 — Parcours compte client (cadrage)

**Statut** : document de **cadrage produit / UX** ; les routes, écrans et règles métier détaillés ci-dessous sont **orientations** jusqu’à arbitrage dans des tickets d’exécution.  
**Pilotage dossier** : [README MVP 03](README.md).  
**Doctrine** : [DOCTRINE_CK_ECOMMERCE_B2C_B2B.md](../direction/DOCTRINE_CK_ECOMMERCE_B2C_B2B.md) (**§2.1** contextualisation par compte et pricelists ; **§8** implications comptes B2B) ; [ADR-CKR-010](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-010).

**Engagement documentaire** : **aucune** route nouvelle, **aucun** champ obligatoire et **aucun** workflow Odoo ne sont validés par ce document seul. Ces éléments devront être confirmés dans des **tickets d’exécution** séparés.

---

## 1. Objectif de ce document

Décrire **qui** crée **quel type de relation** avec C-Kreyol au moment du **compte client**, **comment** les deux intentions (particulier vs demande professionnelle) se distinguent pour le visiteur, et **quelles attentes** sont raisonnables **sans** promettre d’emblée tarifs ou conditions **B2B**.

Ce document **ne remplace pas** la configuration Odoo (partenaires, pricelists, équipes commerciales) ; il fixe le **langage parcours** et les **garde-fous** pour les specs et PR ultérieures.

---

## 2. Principes directeurs

1. **Catalogue unique** — pas de vitrine ou catalogue « parallèle » réservé aux pros pour le MVP décrit ici ; alignement [doctrine §2.1](../direction/DOCTRINE_CK_ECOMMERCE_B2C_B2B.md).
2. **Contexte Odoo** — prix affichés, remises et conditions dépendent du **profil** du visiteur une fois identifié (compte, listes de prix, règles natives).
3. **Standard d’abord** ([ADR-CKR-001](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-001)) — `website`, `portal`, `auth_signup`, `sale`, `contacts`, `pricelist`, `crm` ou `website_form` : réutiliser les mécanismes natifs tant qu’ils suffisent ; spécifique CK pour l’habillage et les points de choix **B2C / demande pro** uniquement si nécessaire.
4. **Sanctuarisation** du tunnel d’achat ([ADR-CKR-009](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-009)) — pas de détournement publicitaire dans le parcours compte ou commande.
5. **Prudence B2B** — un compte professionnel **demandé** n’est pas un compte professionnel **validé** ; aucune demande pro ne doit activer **automatiquement** les tarifs ou conditions B2B.
6. **Friction minimale B2C** — le parcours particulier doit rester **court** et ne pas devenir plus **administratif** qu’un parcours e-commerce standard.

### 2.1 Prudence Odoo CE / standard d’abord

Le chantier MVP 03 doit rester **prudent** et s’appuyer autant que possible sur les mécanismes **standards** d’Odoo CE.

**Objectifs** :

- ne pas créer un **système de comptes parallèle** ;
- ne pas complexifier **prématurément** le portail client ;
- ne pas développer une logique B2B **spécifique** tant que le besoin métier n’est pas validé ;
- utiliser d’abord les objets natifs : `res.partner`, `portal`, `auth_signup`, `website`, `sale`, `pricelist`, `crm` ou `website_form` selon arbitrage.

Le **spécifique CK** doit se limiter autant que possible à :

- clarifier l’**entrée de parcours** entre particulier et demande pro ;
- adapter les **libellés** et **messages** ;
- **habiller** l’expérience visuellement ;
- créer une **demande pro qualifiable**, sans activer automatiquement les **droits B2B**.

**Règle de prudence** :

> Un compte professionnel **demandé** n’est pas un compte professionnel **validé**.

Tant qu’un compte n’est pas validé côté exploitation Odoo, le visiteur reste dans une **lecture B2C** du catalogue.

---

## 3. Personae et états (vue simplifiée)

| Persona / état | Description | Prix boutique affichés (principe doctrine) |
|----------------|-------------|-----------------------------------------------|
| **Visiteur anonyme** | Pas de compte | Lecture **B2C** par défaut — typiquement **prix public conseillé** sur la vitrine. |
| **Particulier connecté** | Compte client **particulier** validé | Reste en lecture **B2C** tant que le partenaire n’est pas basculé en **profil pro** avec pricelist adaptée. |
| **Demandeur pro** | Formulaire « entreprise » envoyé, **validation en attente** | **Pas** de bascule automatique vers prix partenaire ; message clair sur le **délai / traitement** ; affichage boutique inchangé **B2C** jusqu’à traitement métier. |
| **Professionnel validé** | Compte autorisé en **B2B** côté Odoo (pricelist, catégorie partenaire, etc.) | **Affichage commercial contextualisé** — selon paramétrage : **prix partenaire distributeur**, conditions associées. |

Le statut **« demandeur pro »** est un **état d’attente** : il **ne modifie pas** l’expérience tarifaire tant que la **validation métier** n’a pas été effectuée dans Odoo.

Les transitions **Demandeur pro → Professionnel validé** sont **métier + Odoo** (pas seulement front).

---

## 4. Deux parcours distincts (intention utilisateur)

### 4.1 Parcours A — Compte **particulier** (B2C)

**Intention** : acheter en tant que personne physique (ou usage équivalent grand public), avec un compte **simple**.

**Comportement attendu (cadrage)** :

- Accès depuis les points habituels du site : **Connexion** / **Créer un compte** (selon activation Odoo `auth_signup`), liens **Mon compte** vers **`/my`** après session — implémentation header CK : [`ckr_header.xml`](../../views/layout/ckr_header.xml).
- Parcours **court** : peu de champs obligatoires ; pas de confusion avec le formulaire pro.
- Après création : accès **portail** standard (commandes, adresses, etc.) — voir habillage existant `views/portal/ckr_portal.xml`.

Le **MVP 03** ne doit **pas dégrader** la possibilité d’**acheter sans compte** si cette option reste **activée** dans la configuration Odoo (checkout invité).

**Ce que ce parcours n’est pas** : une demande de tarifs distributeur ni une préinscription aux prix partenaire.

### 4.2 Parcours B — **Demande** de compte professionnel / entreprise

**Intention** : signaler une activité **professionnelle** et demander l’ouverture de conditions **B2B** **ultérieures**, sous **validation**.

**Comportement attendu (cadrage)** :

- Entrée **explicite** avec un libellé du type **« Compte professionnel »** / **« Demande d’ouverture de compte pro »** — **à figer** avec la MOA (libellé plus large que seul « distributeur », qui ne couvre pas restaurants, traiteurs, collectivités, etc.).
- Collecte des informations **minimales utiles** à la qualification (ex. société, contact, secteur, message — **arbitrage métier**). *Tout champ supplémentaire doit être justifié par un usage métier clair côté Odoo.*
- **Confirmation** après envoi : la demande est **prise en charge** ; **aucune** promesse de délai irréaliste ni d’accès immédiat aux tarifs pro.
- Côté Odoo, exploitation possible via **lead**, **opportunité**, **activité**, **tag partenaire** ou **étape de validation** — **à spécifier en ticket**, en restant **standard** d’abord.
- La demande pro peut créer une **opportunité**, une **activité** ou un **contact qualifié** côté Odoo, mais **ne doit pas** modifier **automatiquement** les **droits commerciaux** du visiteur (pricelist B2B, affichage prix pro, validation statut, conditions commerciales).

**Ce que ce parcours n’est pas** : un second tunnel d’inscription qui délivrerait **automatiquement** la même expérience tarifaire qu’un partenaire validé.

---

## 5. Cartographie des points d’entrée (site public)

Les chemins exacts seront figés au ticket ; référence **Odoo 19 CE** courante :

| Point d’entrée | Usage typique | Parcours visé |
|----------------|---------------|---------------|
| **`/web/login`** | Connexion | A ou B selon lien « Créer un compte » / « Demande pro » |
| **`/web/signup`** | Inscription si module signup activé | Surtout **A** ; ne pas mélanger B sans clarification UI |
| **`/my`** | Portail connecté | Post-connexion — **A** une fois compte particulier créé |
| **Header** « Mon compte » / **Connexion** | Entrée rapide | Redirection login ou portail — [`ckr_header.xml`](../../views/layout/ckr_header.xml) |
| **Tunnel checkout** (invité vs compte) | Encourage la création de compte **A** pour facilité de commande | Ne doit pas **forcer** le parcours B ; si achat invité activé, **ne pas le casser** |

**Règle de clarté** : à tout moment où l’utilisateur **choisit** « professionnel », il doit comprendre qu’il **demande** une activation, pas qu’il « devient pro » en un clic.

---

## 6. Cohérence avec la boutique et les prix

- Tant que le visiteur n’a **pas** un contexte **B2B** validé en Odoo, la boutique continue d’afficher la **lecture B2C** (prix public conseillé) sur les fiches et le panier — sauf règles promotionnelles **grand public** déjà en place.
- La **double lecture** B2C / B2B du **même catalogue** est portée par le **contexte** (compte + pricelists), pas par une URL catalogue différente — [doctrine §2.1](../direction/DOCTRINE_CK_ECOMMERCE_B2C_B2B.md).

---

## 7. Messages et conformité (orientations)

- **RGPD** : finalités du compte particulier vs traitement des données « demande pro » ; renvoi vers la page **Politique de confidentialité** ([`ckr_privacy.xml`](../../views/pages/ckr_privacy.xml)) et pages légales existantes.
- **CGV** : pour toute ouverture ultérieure de **conditions de vente pro**, renvoi vers `/terms` ou document dédié **quand** le métier l’aura prévu — hors périmètre technique de ce seul document.

---

## 8. Arbitrages à trancher avant développement

| Sujet | Question ouverte |
|-------|------------------|
| **Signup** | `auth_signup` activé sur le site ? Séparation A/B sur **une** page ou **deux** URLs ? |
| **Achat invité** | Le checkout **sans compte** reste-t-il autorisé dans la configuration Odoo ? Le MVP 03 ne doit **pas** le dégrader si oui. |
| **Demande pro** | Formulaire **website_form** vers **CRM** vs **portail** vs **email** métier ? |
| **Réponse demande pro** | Email automatique uniquement ou prise de contact humaine systématique ? **Message de confirmation** exact ? |
| **Validation** | Qui valide (sales, équipe CK) ; impact sur **pricelist** et **catégorie partenaire** ? |
| **Données pro** | Quels champs sont **strictement nécessaires** pour qualifier la demande ? (société, SIRET, secteur, téléphone, message — **minimum utile**.) |
| **Partenaire unique** | Un `res.partner` « en attente » vs doublon contrôlé — règles de dédoublonnage email / SIRET. |
| **Tests auto** | Tag Odoo dédié (`dorevia_ckr_account_…`) et parcours HTTP (`HttpCase`) à définir. |

---

## 9. Critères de recette cible (quand le chantier sera livré)

- [ ] Parcours **A** : création compte particulier + connexion + accès `/my` sans régression checkout.
- [ ] Le parcours particulier reste **court** et ne rend **pas** obligatoire une qualification professionnelle.
- [ ] Si l’**achat invité** est activé côté Odoo, le MVP 03 **ne le casse pas**.
- [ ] Parcours **B** : soumission demande pro + message de confirmation + **aucune** exposition automatique des prix partenaire avant validation métier / Odoo.
- [ ] **Mobile et desktop** : lisibilité des deux entrées (pas d’ambiguïté B2C vs demande pro).
- [ ] **Accessibilité** : labels, erreurs formulaire, focus — alignement avec les exigences déjà posées sur le module CK.
- [ ] Cohérence avec la **doctrine** et absence de **deuxième catalogue** sans décision documentée.

---

## 10. Références croisées

| Document | Lien |
|----------|------|
| README MVP 03 | [README.md](README.md) |
| Doctrine B2C / B2B | [DOCTRINE_CK_ECOMMERCE_B2C_B2B.md](../direction/DOCTRINE_CK_ECOMMERCE_B2C_B2B.md) |
| Login CK (existant) | `views/auth/ckr_login.xml` |
| Portail CK (existant) | `views/portal/ckr_portal.xml` |

---

## Historique

| Date | Événement |
|------|-----------|
| 2026-05 | Première version — parcours particulier vs demande pro, points d’entrée, états, arbitrages et critères de recette cible. |
| 2026-05 | Intégration **synthèse recommandations** MOA / produit : §2.1 prudence CE, garde-fous « non ticket exécutable », friction B2C, achat invité, libellés pro, arbitrages réponse/données, critères enrichis. |
