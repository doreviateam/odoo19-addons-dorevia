# MVP 04 — Panier & favoris C-Kreyol

Dossier de **cadrage** pour la vague **MVP 04** : stabiliser les éléments d’**achat immédiat** (panier) et de **sélection personnelle** (favoris), après **`docs/mvp_01/`** (catalogue / portes `shop`), **`docs/mvp_02/`** (homepage, boutique wave 1…), **`docs/mvp_03/`** (comptes client / demande pro).

**Statut documentaire** : intention et priorités **cadrées** ; ticket d’exécution, spec UX détaillée et arbitrages tech **à produire** avant GO dev.

> Alignement doctrine e-commerce CK : [DOCTRINE_CK_ECOMMERCE_B2C_B2B.md](../direction/DOCTRINE_CK_ECOMMERCE_B2C_B2B.md). Ordre des chantiers : [CHANTIERS_CK_ORDRE.md](../direction/CHANTIERS_CK_ORDRE.md).

**Hors périmètre de ce dossier** : la **compatibilité snippets Odoo Website** (Website Builder, blocs réutilisables) est un chantier **transverse** piloté depuis **`docs/direction/`** — [COMPATIBILITE_SNIPPETS_WEBSITE_CK.md](../direction/COMPATIBILITE_SNIPPETS_WEBSITE_CK.md). Ce n’est **pas** un livrable des lots panier / favoris ci-dessous.

**Documents du dossier**

| Document | Rôle |
|----------|------|
| [README.md](README.md) | Intention, lots 1 / 2, doctrine, garde-fous, hors périmètre — **source de vérité produit** pour MVP 04 |
| [1_PANIER_PARCOURS.md](1_PANIER_PARCOURS.md) | Parcours **panier** : points d’entrée, états, invité / connecté, alignement checkout |
| [2_FAVORIS_PARCOURS.md](2_FAVORIS_PARCOURS.md) | Parcours **favoris** : ajout / retrait, liste, persistance, lien éventuel compte |
| [TICKET_HEADER_NAV_MVP04.md](TICKET_HEADER_NAV_MVP04.md) | Ticket de pilotage : posture **Header CK V1** (Top_0/Top_1/Top_2) et livraison en lots V1.1/V1.2/V1.3 |
| [PISTE_CREA_HEADER_NAV_MVP04_V1.md](PISTE_CREA_HEADER_NAV_MVP04_V1.md) | Piste créa / UX V1 : composition desktop/mobile et hiérarchie visuelle pour panier, favoris, professionnels |

---

## Intention

Stabiliser les éléments d’achat et de sélection personnelle dans l’expérience C-Kreyol.

- Le **panier** permet d’**acheter maintenant**.
- Les **favoris** permettent de **conserver une intention pour plus tard**.

---

## Priorité MVP 04

Le **Lot 1 — Panier** est prioritaire : il conditionne directement la conversion et la non-régression du checkout. Le **Lot 2 — Favoris** ne doit pas retarder la stabilisation du panier.

### Lot 1 — Panier

**Objectif** : rendre le panier **clair**, **accessible** et **rassurant**.

À cadrer :

- icône panier dans le header ;
- compteur panier ;
- état panier vide ;
- panier rempli ;
- accès depuis desktop et mobile ;
- cohérence checkout ;
- achat invité ;
- non-régression du tunnel de commande.

**Ticket lié (navigation)** : [TICKET_HEADER_NAV_MVP04.md](TICKET_HEADER_NAV_MVP04.md) — première refonte structurante **Header CK V1** (Top_0/Top_1/Top_2) livrée en lots.

### Lot 2 — Favoris

**Objectif** : permettre au visiteur de **garder une sélection**.

À cadrer :

- icône cœur sur carte produit ;
- icône cœur sur fiche produit ;
- ajout / retrait favori ;
- liste des favoris ;
- comportement connecté / non connecté ;
- persistance ;
- lien éventuel avec compte client.

---

## Doctrine

**Panier ≠ favoris.**

| Mécanisme | Rôle |
|-----------|------|
| **Panier** | Achat **immédiat**. |
| **Favoris** | **Intention**, repérage, retour plus tard. |

---

## Garde-fous

- Ne pas complexifier le tunnel d’achat.
- Ne pas forcer la création de compte si l’achat invité reste activé.
- Ne pas mélanger favoris et panier.
- Ne pas créer de mécanique marketing lourde en MVP 04.

---

## Hors périmètre implicite

Sauf ticket ultérieur, MVP 04 ne couvre pas :

- relance panier abandonné ;
- recommandations personnalisées ;
- emailing marketing lié aux favoris ;
- partage de wishlist ;
- wishlist collaborative ;
- programme fidélité ;
- promotions automatiques liées aux favoris ;
- refonte complète du checkout.
