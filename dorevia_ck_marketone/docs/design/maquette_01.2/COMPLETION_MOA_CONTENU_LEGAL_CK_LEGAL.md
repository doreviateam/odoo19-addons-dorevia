# Complétion MOA — contenu juridique CK Marketone · `/legal` · `/privacy` · `/terms`

| Champ | Valeur |
|-------|--------|
| **Statut** | **Complétion MOA partielle · brouillons V1 prêts relecture · intégration Dev en standby** |
| **Date structure** | 2026-06-14 |
| **Date complétion partielle** | 2026-06-14 |
| **Environnement** | **Local / sandbox / recette interne** — données fictives autorisées si signalées |
| **Go-live public** | **NO GO** tant que données réelles non validées MOA |
| **Module cible** | `dorevia_ck_marketone_content` 19.0.1.1.0 (local · non commité) |
| **Chantier B** | **Suspendu** |

```text
Doctrine MOA (2026-06-14) :
  · Recette interne : OK données fictives clairement marquées.
  · Go-live public   : NO GO tant que données légales réelles non validées.
  · Intégration Dev  : standby — acte requis « GO intégration Dev contenu légal local ».
  · Commit / PR      : en attente après verdict « mentions légales OK » recette interne.
```

---

## 0. Arbitrages MOA confirmés

| ID | Décision | Statut |
|----|----------|--------|
| **D1** | Page **`/privacy`** dédiée | ✅ Confirmé |
| **C1** | Page **`/terms`** dédiée (CGV) | ✅ Confirmé |

| Route | Rôle | Footer (cible) |
|-------|------|----------------|
| `/legal` | Mentions légales | « Mentions légales » ✅ en place |
| `/privacy` | Politique de confidentialité / RGPD | « Confidentialité » (post-intégration) |
| `/terms` | Conditions générales de vente | « CGV » → `/terms#cgv` (post-intégration) |

---

## 1. Fiche MOA — valeurs renseignées

> **Légende** : valeurs **réelles MOA** · valeurs **[FICTIF]** = recette interne uniquement · **non publiable** en l’état.

### 1.1 Éditeur du site

| ID | Champ | Valeur MOA |
|----|-------|------------|
| **E1** | Raison sociale | **Marketone SAS** |
| **E2** | Forme juridique | **SAS** |
| **E3** | Siège social | **12 rue Example, 44000 Nantes, France** — `[DONNÉE FICTIVE — À REMPLACER AVANT GO-LIVE PUBLIC]` |
| **E4** | SIREN | **123 456 789** — `[SIREN FICTIF — NON PUBLIABLE]` |
| **E5** | RCS | **RCS Nantes 123 456 789** — `[DONNÉE FICTIVE — À REMPLACER AVANT GO-LIVE PUBLIC]` |
| **E6** | TVA intracommunautaire | **FR 12 123456789** — `[TVA FICTIVE — NON PUBLIABLE]` |
| **E7** | Capital social | **10 000 €** — `[DONNÉE FICTIVE — À REMPLACER AVANT GO-LIVE PUBLIC]` |
| **E8** | Directeur de la publication | **Doreviateam** |
| **E9** | E-mail officiel | **contact.ck@marketone.com** |
| **E10** | Téléphone contact | **+33 (0)2 40 00 00 00** — `[TÉLÉPHONE FICTIF — NON PUBLIABLE]` |

### 1.2 Hébergement

| ID | Champ | Valeur MOA |
|----|-------|------------|
| **H1** | Nom commercial | **IONOS France** |
| **H2** | Raison sociale | **1&1 IONOS SARL** |
| **H3** | Adresse | **7 place de la Gare, BP 70109, 57201 Sarreguemines Cedex, France** |
| **H4** | Téléphone | **+33 (0)970 808 911** (service client IONOS France — à confirmer si ligne dédiée hébergement) |
| **H5** | Infra réelle | ☑ **Oui — IONOS France / 1&1 IONOS SARL** · `[SOUS RÉSERVE CONFIRMATION FINALE INFRA]` |

### 1.3 Données personnelles / RGPD

| ID | Champ | Valeur MOA |
|----|-------|------------|
| **D1** | Politique | ☑ Page **`/privacy`** |
| **D2** | Responsable traitement | **Marketone SAS** (identique éditeur) |
| **D3** | Contact RGPD | **contact.ck@marketone.com** |
| **D4** | Conservation | Newsletter : durée inscription active + 3 ans max archives · Contact : 3 ans · Commandes : obligations comptables · CRM Pro : durée relation + 3 ans — `[DURÉES RECETTE — À VALIDER MOA/JURIDIQUE]` |
| **D5** | Base légale newsletter | ☑ **Consentement explicite** (formulaire newsletter site) |

### 1.4 CGV

| ID | Champ | Valeur MOA |
|----|-------|------------|
| **C1** | Emplacement CGV | ☑ Page **`/terms`** |
| **C2** | Tunnel Odoo | ☐ Oui · ☐ Non · ☑ **À configurer** — lien `/terms` / case acceptation checkout · recette interne |
| **C3** | Rétractation 14 j | ☑ Mentionné §2.3 (produits alimentaires / hygiène : exclusions légales rappelées) |
| **C4** | Médiateur | **Médiateur de la consommation** — `[MÉDIATEUR À CONFIRMER AVANT PUBLICATION — coordonnées fictives §2.3]` |
| **C5** | Livraison / retours | France métropolitaine + UE selon offre · délais indicatifs checkout · `[MODALITÉS LOGISTIQUES RECETTE — À STABILISER MOA]` |

### 1.5 Footer & pages

| ID | Élément | Statut |
|----|---------|--------|
| **F1** | `/legal` structure | ✅ |
| **F2** | Lien « Mentions légales » | ✅ |
| **F3** | Contact sur `/legal` | ✅ structure |
| **F4** | `/privacy` + lien footer | ☐ post-intégration Dev |
| **F5** | `/terms` + lien footer CGV | ☐ post-intégration Dev |

---

## 2. Brouillons V1 — contenu intégral proposé

> **Bandeau recette** (à afficher en tête de chaque page en sandbox, retirable avant go-live public) :
>
> *« Version recette interne — certaines coordonnées légales sont fictives ou provisoires. Non publiable en l’état. »*

---

### 2.1 Page `/legal` — Mentions légales

#### Titre & introduction

**Mentions légales**

Informations légales relatives à la boutique en ligne **C-Kreyol**, éditée par **Marketone SAS**.

*Version recette interne — voir bandeau ci-dessus.*

#### Éditeur du site

Le site **C-Kreyol** est édité par :

**Marketone SAS**, société par actions simplifiée (SAS), au capital de **10 000 €** `[DONNÉE FICTIVE — À REMPLACER AVANT GO-LIVE PUBLIC]`, dont le siège social est situé **12 rue Example, 44000 Nantes, France** `[DONNÉE FICTIVE — À REMPLACER AVANT GO-LIVE PUBLIC]`.

Immatriculée au **RCS Nantes 123 456 789** `[DONNÉE FICTIVE]` — **SIREN 123 456 789** `[SIREN FICTIF — NON PUBLIABLE]`.

Numéro de TVA intracommunautaire : **FR 12 123456789** `[TVA FICTIVE — NON PUBLIABLE]`.

**Directeur de la publication** : Doreviateam.

**Contact** : [contact.ck@marketone.com](mailto:contact.ck@marketone.com) — [formulaire de contact](/contactus).

Téléphone : **+33 (0)2 40 00 00 00** `[TÉLÉPHONE FICTIF — NON PUBLIABLE]`.

#### Hébergement

Conformément aux obligations légales, le prestataire d’hébergement assurant le stockage du site est :

- **IONOS France**
- **1&1 IONOS SARL**
- **7 place de la Gare, BP 70109, 57201 Sarreguemines Cedex, France**
- Téléphone : **+33 (0)970 808 911**

*Hébergeur acté MOA sous réserve de confirmation finale de l’infrastructure de production.*

#### Propriété intellectuelle

L’ensemble des éléments composant le site (structure, textes, visuels, logos, marques lorsqu’elles sont protégées) est la propriété de **Marketone SAS** ou fait l’objet d’une autorisation d’utilisation. Toute reproduction ou représentation non autorisée est interdite.

#### Données personnelles

Les données personnelles collectées sur ce site (formulaires contact, newsletter, espace professionnel, commandes) sont traitées conformément à notre [politique de confidentialité](/privacy).

Pour exercer vos droits : **contact.ck@marketone.com** ou [/contactus](/contactus).

#### Conditions générales de vente

Les ventes sur la boutique en ligne C-Kreyol sont soumises aux [conditions générales de vente](/terms) acceptées électroniquement lors de la commande.

Contact SAV : **contact.ck@marketone.com** — [/contactus](/contactus).

---

### 2.2 Page `/privacy` — Politique de confidentialité (V1 prudente)

#### Titre & introduction

**Politique de confidentialité**

La présente politique décrit comment **Marketone SAS** traite les données personnelles collectées sur la boutique en ligne **C-Kreyol**, dans le respect du **RGPD** et de la loi « Informatique et Libertés ».

*Version recette interne — certaines durées et sous-traitants sont indicatifs `[À VALIDER MOA/JURIDIQUE]`.*

#### Responsable du traitement

**Marketone SAS** — contact : **contact.ck@marketone.com**.

Coordonnées complètes : [mentions légales](/legal).

#### Données collectées

Selon votre navigation et vos interactions, nous pouvons traiter :

| Contexte | Données | Finalité |
|----------|---------|----------|
| **Formulaire contact** | Identité, e-mail, téléphone, message | Répondre à votre demande |
| **Newsletter** | E-mail, préférences d’abonnement | Envoi d’informations CK (avec consentement) |
| **Espace professionnel** | Identité pro, société, message qualification | Traitement demande B2B / CRM |
| **Commande boutique** | Identité, adresse, e-mail, historique commande | Exécution contrat, livraison, SAV |
| **Compte client** (si activé) | Identifiants, coordonnées, historique | Gestion compte et commandes |
| **Navigation** | Logs techniques, cookies (voir ci-dessous) | Sécurité, mesure audience `[SI ACTIVÉ — À PRÉCISER]` |

#### Bases légales

- **Commande / compte** : exécution du contrat.
- **Contact / SAV** : intérêt légitime ou mesures précontractuelles.
- **Newsletter** : **consentement explicite** (case dédiée).
- **Obligations légales** : conservation comptable le cas échéant.

#### Durées de conservation `[RECETTE — À VALIDER]`

- **Newsletter** : jusqu’à désinscription, puis suppression ou anonymisation sous 30 jours.
- **Contact** : 3 ans à compter du dernier échange.
- **Commandes** : durée légale comptable et commerciale (generally 10 ans pièces comptables — `[À CONFIRMER COMPTABLE]`).
- **CRM Pro** : durée de la relation commerciale + 3 ans.

#### Destinataires

Données accessibles aux personnes habilitées de **Marketone SAS** et, le cas échéant :

- **Hébergeur** : 1&1 IONOS SARL (hébergement site).
- **Prestataire e-mail / newsletter** : `[SOUS-TRAITANT À LISTER — ex. Odoo / provider SMTP]`.
- **Prestataire paiement** : `[À LISTER SELON PASSERELLE CHECKOUT ODOO]`.

Tous sous-traitants sont choisis avec des garanties appropriées (RGPD art. 28).

#### Vos droits

Vous disposez des droits d’**accès**, **rectification**, **effacement**, **limitation**, **opposition** et **portabilité** lorsque applicable.

Exercice : **contact.ck@marketone.com** ou [/contactus](/contactus).

Réclamation : [CNIL](https://www.cnil.fr).

#### Désinscription newsletter

Lien de désinscription présent dans chaque e-mail, ou demande à **contact.ck@marketone.com**.

#### Cookies et traceurs

Le site peut utiliser des cookies strictement nécessaires au fonctionnement (session, panier, sécurité).

Cookies analytics ou marketing : **`[NON ACTIVÉ EN RECETTE / À DOCUMENTER SI ACTIVATION]`**.

Paramétrage : bandeau cookies ou navigateur selon configuration Odoo CE `[À COMPLÉTER SI BANNIÈRE ACTIVÉE]`.

#### Mise à jour

Dernière mise à jour : **2026-06-14** (version recette interne).

---

### 2.3 Page `/terms` — Conditions générales de vente (V1 prudente)

#### Titre & introduction

**Conditions générales de vente**

Les présentes conditions générales de vente (CGV) régissent les ventes de produits sur la boutique en ligne **C-Kreyol**, exploitée par **Marketone SAS**.

*Version recette interne — modalités logistiques et médiateur indicatifs `[À STABILISER MOA]`.*

#### Identification du vendeur

**Marketone SAS** (SAS) — siège : **12 rue Example, 44000 Nantes** `[FICTIF]` — **SIREN 123 456 789** `[FICTIF]` — **RCS Nantes 123 456 789** `[FICTIF]`.

Contact : **contact.ck@marketone.com** — [/contactus](/contactus).

#### Objet

Les CGV définissent les droits et obligations des parties dans le cadre de la vente en ligne de produits alimentaires et bien-être créoles proposés sur **C-Kreyol**.

#### Produits et prix

Les produits sont décrits sur les fiches produit. Les photographies n’engagent pas le vendeur au-delà des caractéristiques essentielles.

Les prix sont indiqués **en euros TTC** (TVA incluse) avant validation de la commande. Les frais de livraison sont indiqués avant paiement.

#### Commande

La commande est validée après confirmation du paiement et envoi de l’e-mail de confirmation.

Marketone SAS se réserve le droit d’annuler toute commande en cas de litige antérieur, d’erreur manifeste de prix ou de rupture de stock.

#### Paiement

Paiement en ligne via les moyens proposés au checkout Odoo (carte bancaire, etc.) `[MODALITÉS SELON CONFIGURATION ODOO — RECETTE]`.

#### Livraison `[MODALITÉS RECETTE — À STABILISER MOA]`

- **Zones** : France métropolitaine ; Union européenne selon produits et transporteurs disponibles.
- **Délais** : indicatifs, communiqués avant validation de commande.
- **Transfert des risques** : à la remise au transporteur ou au client selon mode choisi.

#### Droit de rétractation

Conformément au Code de la consommation, le client consommateur dispose d’un délai de **14 jours** à compter de la réception pour exercer son droit de rétractation, **sous réserve des exclusions légales** (notamment denrées périssables, produits descellés après livraison et ne pouvant être renvoyés pour des raisons d’hygiène ou de protection de la santé).

Modalités : contact **contact.ck@marketone.com** avec numéro de commande.

Frais de retour : `[À PRÉCISER MOA — sauf produit non conforme ou erreur vendeur]`.

#### Garanties légales

Le client bénéficie de la garantie légale de conformité et de la garantie contre les vices cachés, dans les conditions du Code de la consommation et du Code civil.

#### Médiation de la consommation

En cas de litige non résolu avec le service client, le consommateur peut recourir gratuitement à un médiateur de la consommation :

**[Nom du médiateur — MÉDIATEUR À CONFIRMER AVANT PUBLICATION]**

**[Adresse / site web du médiateur — FICTIF RECETTE]**

*Plateforme européenne de règlement en ligne des litiges :* [https://ec.europa.eu/consumers/odr](https://ec.europa.eu/consumers/odr)

#### Responsabilité

La responsabilité de Marketone SAS est limitée aux dommages directs prouvés, dans la limite permise par la loi. Force majeure : obligations suspendues.

#### Droit applicable

Les CGV sont soumises au **droit français**. Tribunaux compétents selon règles de procédure applicables au consommateur.

#### Contact

**contact.ck@marketone.com** — [/contactus](/contactus)

---

## 3. Footer cible (post-intégration Dev)

Colonne **Découvrir** (ou bandeau légal bas de footer) :

```text
/contactus          Contact
/legal              Mentions légales
/privacy            Confidentialité
/terms#cgv          CGV
```

Formulaires :

- Newsletter → lien « politique de confidentialité » → `/privacy`
- Checkout → case CGV → `/terms` (C2 à configurer Odoo)

---

## 4. Synthèse — état complétion

| Zone | Statut |
|------|--------|
| Fiche P0 E1, E2, E8, E9, H5 | ✅ **Renseignés MOA** |
| Fiche E3–E7, E10 | ✅ **Fictifs signalés** (recette interne) |
| Brouillon `/legal` §2.1 | ✅ **Proposé V1** |
| Brouillon `/privacy` §2.2 | ✅ **Proposé V1 prudente** |
| Brouillon `/terms` §2.3 | ✅ **Proposé V1 prudente** |
| Intégration `hooks.py` · `/legal` · `/privacy` · `/terms` · footer | ✅ **Intégré local** (2026-06-14) |
| Contrôleur `/terms` (priorité CMS sur account Odoo) | ✅ **Corrigé** (2026-06-14) |
| Tests `dorevia_ck_marketone_legal` | ✅ **8/8 OK** |
| Recette HTTP `/legal` · `/privacy` · `/terms` · footer `/` · `/shop` | ✅ **OK** |
| Go-live public | **NO GO** |

**Champs encore à valider MOA avant publication publique** : E3–E7, E10 (remplacer fictifs), H5 (confirmation infra finale), C2 (checkout), C4 (médiateur), C5 (logistique), sous-traitants D4/privacy.

---

## 5. Procédure — prochaines étapes

| # | Étape | Responsable | Statut |
|---|-------|-------------|--------|
| 1 | Complétion fiche + brouillons V1 | Dev / MOA | ✅ **Fait** (2026-06-14) |
| 2 | **Relecture MOA** brouillons §2.1–2.3 | **MOA** | ☐ En cours |
| 3 | Acte **GO intégration Dev contenu légal local** | **MOA** | ✅ **Signé** (2026-06-14) |
| 4 | Intégration `hooks.py` · `/privacy` · `/terms` · footer | Dev | ✅ **Fait** (19.0.1.2.0) |
| 5 | Recette interne + tests | Dev | ✅ **8/8 + curl OK** |
| 6 | Verdict « contenu légal local OK » | MOA | ☐ **À signer** |
| 7 | Remplacement fictifs → données réelles + GO public | MOA | ☐ |
| 8 | Commit / PR | MOA | ☐ |

---

## 6. Acte MOA — relecture brouillons V1 (à signer)

```text
Relecture contenu juridique V1 — CK Marketone (recette interne)

☐ Brouillon §2.1 /legal validé (ou corrections en annexe)
☐ Brouillon §2.2 /privacy validé
☐ Brouillon §2.3 /terms validé
☐ Données fictives §1 acceptées pour recette interne uniquement
☐ Arbitrages D1 / C1 confirmés

Verdict relecture :
  ☐ GO intégration Dev contenu légal local
  ☐ Réserve — corrections listées

Go-live public :
  ☑ NO GO maintenu (données réelles requises)

Validé par : ____________________
Date : ____________________
```

---

## Documents liés

| Document | Rôle |
|----------|------|
| [`RAPPORT_LOT_MENTIONS_LEGALES_GO_LIVE_20260614.md`](./RAPPORT_LOT_MENTIONS_LEGALES_GO_LIVE_20260614.md) | Livraison structure |
| [`RECETTE_QA_PHASE10_GO_LIVE_CK_V1.md`](./RECETTE_QA_PHASE10_GO_LIVE_CK_V1.md) | Contrôle F3 |
| `dorevia_ck_marketone_content/hooks.py` | Source technique · **non modifié** |

---

*Complétion MOA partielle · brouillons V1 · standby Dev · local non commité · 2026-06-14.*
