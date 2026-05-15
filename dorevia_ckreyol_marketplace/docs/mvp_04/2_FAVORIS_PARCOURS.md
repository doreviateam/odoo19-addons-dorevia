# MVP 04 — Parcours favoris (cadrage)

## Lot 2 Favoris — cadré produit / UX, exécution différée

Ce document est **à jour comme référence de cadrage** ; il ne doit pas être lu comme « sujet oublié » : le Lot 2 est **cadré**, l’**exécution n’est pas lancée**, les arbitrages techniques restent **ouverts**, et le chantier est **volontairement différé** après le **Lot 1 panier / checkout** — il **n’est pas bloquant** pour le GO technique minimal pré-ouverture actuel (voir [README MVP 04 — Lot 2 Favoris](README.md)).

> Le Lot 2 Favoris est cadré mais non lancé en exécution. Son traitement est différé après le Lot 1 panier / checkout et les jalons de pré-ouverture marchande. Il n’est pas bloquant pour le GO technique minimal pré-ouverture actuel.

**Rappels** :

- **Favoris** = intention **différée**, distincte du **panier**.
- Pas de marketing lourd ; pas d’**emailing automatique** ; pas de **partage de liste** ; pas de **compte forcé** sans arbitrage.
- Persistance **invité / connectée / fusion invité → connecté** : **à arbitrer** ; voir [`TICKET_FAVORIS_EXECUTION_LOT2.md`](TICKET_FAVORIS_EXECUTION_LOT2.md) (**non lancé**).

---

**Statut documentaire** : **cadrage produit / UX** ; stockage technique, routes et règles de fusion invité → connecté restent **à arbitrer** dans [`TICKET_FAVORIS_EXECUTION_LOT2.md`](TICKET_FAVORIS_EXECUTION_LOT2.md) (**préparation — non lancé**).  
**Pilotage dossier** : [README MVP 04](README.md).  
**Doctrine** : intention et retour différé — pas de confusion avec le panier ([README — Doctrine](README.md#doctrine)).

**Engagement documentaire** : aucune mécanique marketing, aucun emailing ni partage de liste n’est couvert par MVP 04 — [Hors périmètre](README.md#hors-périmètre-implicite).

**Référence de contexte** : le header `Top_0/Top_1/Top_2` est figé en baseline V1 ; ce parcours favoris s’appuie sur cette base sans relancer une refonte header.

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
- **Ticket préparation / arbitrage Lot 2** : [`TICKET_FAVORIS_EXECUTION_LOT2.md`](TICKET_FAVORIS_EXECUTION_LOT2.md) — statut **à arbitrer — non lancé** ; **aucune implémentation** engagée par ce document. Exécution réelle **différée** après stabilisation du **Lot 1 panier / checkout** et jalons pré-ouverture marchande.

---

## 8. Critères d’acceptation — Favoris (Lot 2)

1. **Ajout/retrait clair** : le cœur bascule proprement depuis carte produit et fiche produit.
2. **Cohérence visuelle** : un même produit ne présente pas d’état contradictoire entre listing et fiche.
3. **Liste dédiée** : l’utilisateur retrouve ses favoris dans une vue lisible avec liens vers les produits.
4. **Séparation panier/favoris** : aucun wording ambigu ne laisse penser qu’un favori est déjà au panier.
5. **Desktop + mobile** : actions principales accessibles dans les deux contextes.
6. **Périmètre maîtrisé** : aucune logique marketing ou collaborative n’est introduite.

---

## 9. Scénarios de recette minimaux

- **F1 — Ajout carte produit** : clic cœur depuis listing, état visuel mis à jour immédiatement.
- **F2 — Ajout fiche produit** : même comportement depuis page produit.
- **F3 — Retrait** : suppression depuis la liste favoris et vérification de disparition.
- **F4 — Persistance non connecté** : comportement conforme à l’arbitrage technique retenu (session/local).
- **F5 — Persistance connecté** : comportement conforme à l’arbitrage retenu côté compte.
- **F6 — Mobile** : validation tactile des actions cœur/liste sans régression.

---

## 10. Garde-fous de mise en œuvre

- Ne pas retarder le lot panier pour ajouter des options favoris.
- Ne pas introduire emailing, partage, ou recommandations dans ce lot.
- Ne pas forcer un compte utilisateur sans décision explicite d’arbitrage.
- Conserver une implémentation simple, testable, et alignée au cadrage MVP04.
