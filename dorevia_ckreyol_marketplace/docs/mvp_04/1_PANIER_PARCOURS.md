# MVP 04 — Parcours panier (cadrage)

**Statut** : document de **cadrage produit / UX** ; routes, composants techniques et règles fines restent **à arbitrer** dans le ticket d’exécution.  
**Pilotage dossier** : [README MVP 04](README.md).  
**Doctrine / tunnel** : sanctuarisation du parcours achat — [ADR-CKR-009](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-009) ; alignement [DOCTRINE_CK_ECOMMERCE_B2C_B2B.md](../direction/DOCTRINE_CK_ECOMMERCE_B2C_B2B.md).

**Engagement documentaire** : aucune implémentation Odoo ou route n’est validée par ce document seul.

**Référence de contexte** : le header `Top_0/Top_1/Top_2` est figé en baseline V1 ; ce parcours panier s’appuie sur cette base sans relancer une refonte header.

---

## 1. Objectif de ce document

Décrire **comment** le visiteur **ajoute**, **consulte** et **poursuit** une commande depuis le **panier**, sur **desktop et mobile**, sans dégrader le **checkout** ni l’**achat invité**, dans la limite du périmètre [README — Lot 1](README.md#lot-1--panier).

---

## 2. Principes directeurs

1. **Conversion d’abord** — le panier est le hub entre vitrine et paiement ; il doit être **lisible**, **rassurant** et **cohérent** avec la suite du tunnel.
2. **Non-régression** — toute évolution habillage ou UX du panier préserve le **comportement standard** attendu (quantités, lignes, redirection checkout, session invité).
3. **Panier ≠ favoris** — pas de confusion fonctionnelle ni de libellés ambigus entre intention d’achat immédiat et liste de souhaits ([README — Doctrine](README.md#doctrine)).
4. **Friction maîtrisée** — si l’achat invité reste activé, le parcours panier → checkout **ne force pas** la création de compte ([README — Garde-fous](README.md#garde-fous)).

---

## 3. Points d’entrée et navigation

| Zone | Comportement attendu (cadrage) |
|------|--------------------------------|
| **Header** | Accès visible au panier (icône + **compteur** cohérent avec le contenu du panier). |
| **Mobile** | Même accessibilité qu’en desktop : zone tactile suffisante, pas de régression d’usage. |
| **Après ajout produit** | Le visiteur peut **continuer** ses achats ou **aller au panier** — flux à détailler en spec UX / ticket. |

---

## 4. États du panier (vue produit)

| État | Attente utilisateur (cadrage) |
|------|-------------------------------|
| **Vide** | Message clair ; lien vers la boutique ou le catalogue — pas de impasse. |
| **Rempli** | Liste des lignes **compréhensible** (produit, quantité, éléments de prix selon règles existantes) ; actions pour ajuster ou retirer ; **CTA** vers le checkout **visible**. |
| **Contraintes** (stock, indisponibilité) | Messages **explicites** sans casser le tunnel — détail technique au ticket. |

---

## 5. Invité vs connecté

- **Invité** : le panier reste utilisable jusqu’au checkout dans les limites de la configuration Odoo ; pas de création de compte **imposée** au seul motif du panier ([README](README.md)).
- **Connecté** : cohérence avec **Mon compte** / commandes — sans élargir le périmètre MVP 04 au-delà du nécessaire.

---

## 6. Checkout et cohérence

- Le panier doit **préparer** le checkout **sans surprise** (totaux, devise, messages de base).
- Les évolutions **MVP 04** ne constituent **pas** une refonte checkout — voir [Hors périmètre](README.md#hors-périmètre-implicite).

---

## 7. Hors périmètre rappel

Éléments explicitement **hors MVP 04** : [README — Hors périmètre implicite](README.md#hors-périmètre-implicite) (relance panier abandonné, recommandations, etc.).

---

## 8. Suite documentaire

- Spec UX écrans panier (états, messages, accessibilité) — à produire si besoin.  
- **Ticket d’exécution** : [TICKET_PANIER_PALIER_A_EXECUTION.md](TICKET_PANIER_PALIER_A_EXECUTION.md) — périmètre technique, critères d’acceptation, recette minimale.  
- Ticket de cadrage navigation/header : [TICKET_HEADER_NAV_MVP04.md](TICKET_HEADER_NAV_MVP04.md) — visibilité panier/favoris, mobile, découpage MVP04 vs chantier dédié.  
- Parcours **favoris** : [2_FAVORIS_PARCOURS.md](2_FAVORIS_PARCOURS.md) — **après** stabilisation du cadrage panier si l’équipe suit l’ordre des lots.

---

## 9. Critères d’acceptation — Panier (Palier A)

1. **Accès header** : l’icône panier est visible desktop/mobile, avec compteur cohérent.
2. **Panier vide** : un état vide explicite est affiché avec sortie claire vers la boutique.
3. **Panier rempli** : l’utilisateur peut modifier les quantités et retirer une ligne sans blocage.
4. **Passage checkout** : le CTA vers le checkout est visible et mène au flux attendu.
5. **Achat invité** : si activé dans la configuration, aucun blocage compte n’est introduit au niveau panier.
6. **Non-régression mobile** : actions principales (voir panier, ajuster, retirer, checkout) restent utilisables tactilement.

---

## 10. Scénarios de recette minimaux

- **S1 — Ajout simple** : ajout d’un produit depuis `/shop` puis vérification compteur + présence ligne panier.
- **S2 — Quantité** : passage de Q1 à Q2 puis retour Q1 ; total recalculé correctement.
- **S3 — Suppression** : retrait d’une ligne ; état panier cohérent (vide ou partiel).
- **S4 — Invité** : parcours invité panier -> checkout sans exigence de création de compte au niveau panier.
- **S5 — Connecté** : même parcours en session connectée, sans divergence fonctionnelle inattendue.
- **S6 — Mobile** : validation des actions panier principales sur viewport mobile.

---

## 11. Garde-fous de mise en œuvre

- Ne pas ouvrir une refonte checkout dans ce lot.
- Ne pas introduire de logique marketing (upsell, relance, recommandation).
- Ne pas modifier la doctrine `Panier ≠ Favoris`.
- Conserver un lot court, testable, et réversible rapidement en cas d’écart.
