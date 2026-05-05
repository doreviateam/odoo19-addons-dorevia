# PV — Recette compte client MVP 03

**Ticket** : [TICKET_COMPTE_CLIENT_MVP03.md](TICKET_COMPTE_CLIENT_MVP03.md)  
**Spec UX** : [2_COMPTE_CLIENT_SPEC_UX.md](2_COMPTE_CLIENT_SPEC_UX.md) — parcours : [1_COMPTE_CLIENT_PARCOURS.md](1_COMPTE_CLIENT_PARCOURS.md)

**Statut** : **Prêt pour recette technique** — livrable aligné avec [TICKET_COMPTE_CLIENT_MVP03.md](TICKET_COMPTE_CLIENT_MVP03.md) *(page `/demande-compte-professionnel`, CRM `website_crm`, traçabilité `referred`, tests)* ; **verdict MOA / technique à instruire** après session sur l’instance ci-dessous.  
**GO documentaire (ticket)** : **2026-05-05** — voir [TICKET_COMPTE_CLIENT_MVP03.md](TICKET_COMPTE_CLIENT_MVP03.md).  
**GO documentaire (PV)** : **2026-05-05** — base recette validée pour préparation des tests *(verdict technique toujours **non instruit** jusqu’à recette réelle)*.

**Pré-requis session recette** : `git pull` sur la branche courante ; mise à jour module **`-u dorevia_ckreyol_marketplace`** *(installe / aligne `crm` + `website_crm` selon dépendances)* ; base **`tenant_o7`** *(ou instance cible équivalente)*.

| Champ | Valeur |
|-------|--------|
| **Date recette** | *À compléter* |
| **Instance / version module** | *À compléter* |
| **Relecteur MOA** | *À compléter* |
| **Verdict** | *Non instruit* |

---

## Synthèse verdict *(à rédiger après recette)*

*Résumé GO / réserves / hors périmètre.*

---

## Alignement livraison *(référence — à cocher en recette)*

Points techniques livrés *(module **19.0.1.10.77+**, branche **`feature/shop-mvp22-visible-wave1`** au moment du dernier push)* :

| Point | Détail |
|-------|--------|
| Page dédiée | **`/demande-compte-professionnel`** |
| Chaîne CRM | Formulaire Website → **`crm.lead`** via **`website_crm`** |
| Merci | Redirection **`/demande-compte-pro-merci`** |
| Traçabilité | **`referred`** = **`CK-MVP03-demande-compte-pro`** ; nom **`Demande compte pro C-Kreyol MVP03 — …`** ; description préfixée **`[Demande compte pro C-Kreyol MVP03]`** |
| Garde-fous code | Pas de portail pro auto, pas de pricelist B2B auto, pas de validation statut pro auto |
| Entrées | Liens depuis **login** et **signup** |
| Tests auto | `test_ckr_mvp03_pro_account` *(module)* |

**CRM** : si besoin d’acheminement équipe, vérifier **Website → Configuration → CRM par défaut** (équipe / vendeur par défaut).

**Branche / traçabilité** : l’implémentation MVP03 est sur **`feature/shop-mvp22-visible-wave1`** ; une **PR dédiée** ou une autre convention de merge reste **à confirmer** côté pilotage *(pas de changement de branche imposé par le livrable)*.

---

## 1. Pré-requis et configuration *(à noter)*

- **§4 ticket** complété : `auth_signup`, URLs A/B, achat invité, chaîne demande pro, champs, notifications, comportement doublon email.
- Base alignée avec l’**instance cible** (CRM si `crm.lead`, etc.).

### 1.1 Arbitrages retenus pour cette recette

*À remplir avant ou au début de la session de test — évite de recourir à l’historique du ticket pendant la recette.*

| Sujet | Décision testée |
|-------|-----------------|
| `auth_signup` | Activé sur base test *(ex. `tenant_o7`)* — inchangé par MVP03 |
| Séparation A/B | **`/web/signup`** (B2C) · **`/demande-compte-professionnel`** (demande pro) |
| Achat invité | **`account_on_checkout`** = optional si configuré *(non forcé par MVP03)* |
| Chaîne demande pro | **`website` + `crm` + `website_crm`** ; formulaire → **`crm.lead`** |
| Champs formulaire B | Entreprise, contact, e-mail, téléphone, message *(type d’activité dans le message si besoin)* |
| Email / notification | Confirmation **web** + redirection merci ; pas d’email auto imposé par le code livré |
| Doublon email | Selon §4 ticket / recommandation *(non modifié spécifiquement par cette livraison)* |

---

## 2. Parcours A — compte particulier (B2C)

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| Entrées header / login vers **`/web/signup`** cohérentes si signup activé | [ ] | [ ] | [ ] | |
| Formulaire **sans** champs entreprise obligatoires mélangés au B2C | [ ] | [ ] | [ ] | |
| Erreurs formulaire **lisibles** (email invalide, mot de passe, etc.) | [ ] | [ ] | [ ] | |
| Après inscription : accès **`/my`** ou redirect checkout | [ ] | [ ] | [ ] | |
| **Non-régression** tunnel commande avec compte créé | [ ] | [ ] | [ ] | |

---

## 3. Parcours B — demande d’ouverture de compte pro

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| Entrée **distincte** du signup B2C (URL / section — selon arbitrage) | [ ] | [ ] | [ ] | |
| Copies **sans** promesse tarifs pro immédiate ([spec §5.3](2_COMPTE_CLIENT_SPEC_UX.md)) | [ ] | [ ] | [ ] | |
| **Aucune formulation interdite** visible (ex. « Accéder aux tarifs pro », « Activer mon compte pro », « Voir mes prix professionnels », etc. — [liste spec §5.3](2_COMPTE_CLIENT_SPEC_UX.md)) | [ ] | [ ] | [ ] | |
| **Confirmation web obligatoire** après envoi (message clair « demande transmise ») | [ ] | [ ] | [ ] | |
| **Pas** de création automatique d’utilisateur **portail pro** *(sauf arbitrage explicite)* | [ ] | [ ] | [ ] | |
| **Pas** de bascule pricelist / prix B2B après seule soumission formulaire | [ ] | [ ] | [ ] | |
| Emails / notifications additionnels conformes à **§4** ticket | [ ] | [ ] | [ ] | |
| Mentions / renvoi **privacy** visibles ou accessibles selon arbitrage (**`/privacy`** — [ticket §3.4](TICKET_COMPTE_CLIENT_MVP03.md)) | [ ] | [ ] | [ ] | |

---

## 4. Checkout invité

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| Si invité **activé** en config : option **commander sans compte** toujours visible et utilisable | [ ] | [ ] | [ ] | |
| Pas d’étape obligatoire « créer un compte » ajoutée par le livrable MVP03 | [ ] | [ ] | [ ] | |

---

## 5. Portail `/my`

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| Tant que profil pro **non validé** Odoo : **aucun** badge / zone / libellé « compte pro » trompeur ([spec §3 / §6](2_COMPTE_CLIENT_SPEC_UX.md)) | [ ] | [ ] | [ ] | |

---

## 6. Email déjà existant (doublon)

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| Comportement **explicite** côté visiteur **ou** traitement BO documenté (cf. §4 ticket — ligne doublon) | [ ] | [ ] | [ ] | |
| Pas **d’échec silencieux** ni message générique opaque | [ ] | [ ] | [ ] | |

---

## 7. Mobile

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| Distinction A/B **lisible** petit écran ; formulaires utilisables sans piège UX | [ ] | [ ] | [ ] | |

---

## 8. Accessibilité

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| Labels champs ; erreurs **textuelles** (pas seulement couleur) | [ ] | [ ] | [ ] | |
| Ordre de tabulation logique ; focus visible ([spec §7](2_COMPTE_CLIENT_SPEC_UX.md)) | [ ] | [ ] | [ ] | |

---

## 9. Traçabilité back-office Odoo

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| Demande pro **retrouvable** (lead / objet concerné) avec **identifiant** MVP03 : tag, source, nom de campagne ou équivalent ([critères ticket §7](TICKET_COMPTE_CLIENT_MVP03.md)) | [ ] | [ ] | [ ] | |
| Contenu suffisant pour **traitement métier** (champs arbitrés §4) | [ ] | [ ] | [ ] | |

---

## 10. Tests automatisés *(si livrés)*

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| Tag Odoo documenté en PR ; non-régression flux concernés | [ ] | [ ] | [ ] | |

---

## 11. Réserves / actions à ouvrir

| ID | Réserve / action | Gravité | Responsable | Statut |
|----|------------------|---------|-------------|--------|
| R1 | *À compléter* | *Bloquant / Mineur / Info* | *À compléter* | *Ouvert* |

---

## Historique

| Date | Événement |
|------|-----------|
| 2026-05-05 | Création **brouillon** : grilles recette alignées ticket + spec UX ; verdict après livraison. |
| 2026-05-05 | **GO documentaire** sur le dossier MVP 03 — PV prêt pour préparation des tests ; verdict après implémentation. |
| 2026-05-05 | Amendements : §1.1 arbitrages testés ; contrôle formulations interdites parcours B ; ligne RGPD / **`/privacy`** ; §11 réserves / actions à ouvrir — **GO documentaire** sur la base recette (dossier MVP 03 prêt arbitrage MOA / tech, alignement ticket). |
| 2026-05-05 | **Livraison dev alignée ticket** : section *Alignement livraison* ; statut **Prêt pour recette technique** ; §1.1 pré-rempli ; rappel **`tenant_o7`**, **`-u`**, branche **`feature/shop-mvp22-visible-wave1`**. |
