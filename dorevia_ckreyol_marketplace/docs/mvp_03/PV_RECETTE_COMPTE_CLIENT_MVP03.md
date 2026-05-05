# PV — Recette compte client MVP 03

**Ticket** : [TICKET_COMPTE_CLIENT_MVP03.md](TICKET_COMPTE_CLIENT_MVP03.md)  
**Spec UX** : [2_COMPTE_CLIENT_SPEC_UX.md](2_COMPTE_CLIENT_SPEC_UX.md) — parcours : [1_COMPTE_CLIENT_PARCOURS.md](1_COMPTE_CLIENT_PARCOURS.md)

**Statut** : **Brouillon** — structure de recette **avant livraison dev** ; verdict, date et instance à compléter après implémentation.

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

## 1. Pré-requis et configuration *(à noter)*

- **§4 ticket** complété : `auth_signup`, URLs A/B, achat invité, chaîne demande pro, champs, notifications, comportement doublon email.
- Base alignée avec l’**instance cible** (CRM si `crm.lead`, etc.).

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
| **Confirmation web obligatoire** après envoi (message clair « demande transmise ») | [ ] | [ ] | [ ] | |
| **Pas** de création automatique d’utilisateur **portail pro** *(sauf arbitrage explicite)* | [ ] | [ ] | [ ] | |
| **Pas** de bascule pricelist / prix B2B après seule soumission formulaire | [ ] | [ ] | [ ] | |
| Emails / notifications additionnels conformes à **§4** ticket | [ ] | [ ] | [ ] | |

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
| Pas de échec **silencieux** ni message générique opaque | [ ] | [ ] | [ ] | |

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

## Historique

| Date | Événement |
|------|-----------|
| 2026-05 | Création **brouillon** : grilles recette alignées ticket + spec UX ; verdict après livraison. |
