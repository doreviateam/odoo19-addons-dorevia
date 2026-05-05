# MVP 04 — Parcours favoris (cadrage)

**Statut** : document de **cadrage produit / UX** ; stockage technique, routes et règles de fusion invité → connecté restent **à arbitrer** dans le ticket d’exécution.  
**Pilotage dossier** : [README MVP 04](README.md).  
**Doctrine** : intention et retour différé — pas de confusion avec le panier ([README — Doctrine](README.md#doctrine)).

**Engagement documentaire** : aucune mécanique marketing, aucun emailing ni partage de liste n’est couvert par MVP 04 — [Hors périmètre](README.md#hors-périmètre-implicite).

---

## 1. Objectif de ce document

Décrire **comment** le visiteur **marque** des produits pour **plus tard**, **consulte** sa liste de favoris et **ajoute ou retire** des articles, **sans** fusionner cette intention avec le panier ni avec des campagnes marketing, dans la limite du périmètre [README — Lot 2](README.md#lot-2--favoris).

**Priorité de lot** : le Lot 2 **ne doit pas retarder** le Lot 1 panier ([README — Priorité MVP 04](README.md#priorité-mvp-04)).

---

## 2. Principes directeurs

1. **Favoris = intention** — repérage et retour ultérieur ; pas un substitut du panier.
2. **Simplicité** — ajout / retrait **immédiat** depuis carte produit et fiche produit (icône cœur ou équivalent validé en UX).
3. **Pas de marketing lourd** — pas d’emailing automatique, pas de recommandations personnalisées dans MVP 04 ([README](README.md)).
4. **Lien compte optionnel** — connexion au **compte client** possible selon arbitrage ([README MVP 03](../mvp_03/README.md)), sans imposer un compte si la doctrine checkout / invité s’y oppose.

---

## 3. Points d’entrée et actions

| Lieu | Comportement attendu (cadrage) |
|------|--------------------------------|
| **Carte produit** | Indicateur favori (ex. cœur) ; bascule ajout / retrait avec **retour visuel** clair. |
| **Fiche produit** | Même logique que la carte — **cohérence** des états (favori / non favori). |
| **Liste des favoris** | Page ou vue dédiée listant les produits favoris ; possibilité de **retirer** ou **aller au détail** produit ; lien vers panier **distinct** de la notion de favori. |

---

## 4. Connecté vs non connecté

| Situation | Enjeu (cadrage) |
|-----------|-----------------|
| **Non connecté** | Persistance **locale ou session** selon arbitrage technique — à documenter au ticket ; pas de promesse de synchronisation multi-appareils sans spec. |
| **Connecté** | Persistance **associée au compte** si retenu — alignement avec portail / partenaire sans déborder du périmètre MVP 04. |

Les modalités exactes (cookies, `res.partner`, module tiers) sont **hors** de ce document de parcours.

---

## 5. Liste des favoris — attentes minimales

- Vue **scannable** (visuel produit, titre, lien vers fiche).
- **Aucune** obligation d’ajouter au panier depuis les favoris ; **accès** au panier reste un chemin **séparé**.
- **Mobile** : usage équivalent au desktop pour les actions principales.

---

## 6. Hors périmètre rappel

Partage de wishlist, wishlist collaborative, fidélité, promos déclenchées par les favoris : [README — Hors périmètre implicite](README.md#hors-périmètre-implicite).

---

## 7. Suite documentaire

- Spec UX (micro-copy, états du cœur, page liste) — si besoin.  
- **Ticket d’exécution** — après stabilisation du **Lot 1 panier**, conformément à la priorité dossier.
